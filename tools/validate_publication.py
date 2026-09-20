#!/usr/bin/env python3
"""Read-only validation of the repository publication surface."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EMAILS = {"6reduk@gmail.com"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".txt"}
LOCAL_PATH_PATTERNS = (
    re.compile(r"[A-Za-z]:[\\/]Users[\\/]", re.IGNORECASE),
    re.compile(r"/(?:Users|home)/[^/\s]+/"),
    re.compile(r"\bAppData[\\/]", re.IGNORECASE),
    re.compile(r"\bYandexDisk[\\/]", re.IGNORECASE),
    re.compile(r"file://", re.IGNORECASE),
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{24,}\b", re.IGNORECASE),
)
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


class PublicationError(RuntimeError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise PublicationError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PublicationError(message)


def run(*args: str) -> str:
    process = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(process.returncode == 0, f"command failed: {' '.join(args)}\n{process.stderr.strip()}")
    return process.stdout.strip()


def tracked_files() -> list[Path]:
    if (ROOT / ".git").exists():
        output = run("git", "-c", f"safe.directory={ROOT.as_posix()}", "ls-files", "-z")
        return [ROOT / item for item in output.split("\0") if item]
    # Release archives downloaded without .git must remain independently
    # verifiable. Hidden VCS data and transient cache files are not part of the
    # publication surface.
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )


def text_files(files: list[Path]) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = path.read_bytes()
        require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM is not allowed: {path.relative_to(ROOT)}")
        try:
            result[path] = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PublicationError(f"invalid UTF-8: {path.relative_to(ROOT)}: {exc}") from exc
    return result


def validate_front_matter(texts: dict[Path, str]) -> int:
    ids: dict[str, Path] = {}
    for path, text in texts.items():
        metadata: Any = None
        if path.suffix.lower() == ".md" and text.startswith("---\n"):
            end = text.find("\n---\n", 4)
            require(end >= 0, f"unclosed front matter: {path.relative_to(ROOT)}")
            metadata = yaml.load(text[4:end], Loader=UniqueKeyLoader)
        elif path.suffix.lower() in {".yaml", ".yml"}:
            metadata = yaml.load(text, Loader=UniqueKeyLoader)
        if not isinstance(metadata, dict) or "id" not in metadata:
            continue
        semantic_id = metadata["id"]
        require(isinstance(semantic_id, str) and semantic_id.strip(), f"invalid id: {path.relative_to(ROOT)}")
        require(semantic_id not in ids, f"duplicate id {semantic_id}: {ids.get(semantic_id)} and {path}")
        ids[semantic_id] = path
    return len(ids)


def validate_hygiene(texts: dict[Path, str]) -> int:
    emails: set[str] = set()
    for path, text in texts.items():
        relative = path.relative_to(ROOT)
        require(re.search(r"^(?:<<<<<<<|=======|>>>>>>>)", text, re.MULTILINE) is None,
                f"conflict marker: {relative}")
        require(all(not line.endswith((" ", "\t")) for line in text.splitlines()),
                f"trailing whitespace: {relative}")
        # The validator contains the literal detection patterns it applies to
        # every other tracked text file, so scanning its own pattern table
        # would be a deterministic false positive.
        if relative.as_posix() != "tools/validate_publication.py":
            for pattern in LOCAL_PATH_PATTERNS:
                require(pattern.search(text) is None, f"local absolute path marker: {relative}")
            for pattern in SECRET_PATTERNS:
                require(pattern.search(text) is None, f"secret-like value: {relative}")
        for email in EMAIL_PATTERN.findall(text):
            emails.add(email.lower())
    unexpected = emails - ALLOWED_EMAILS
    require(not unexpected, f"unexpected email addresses: {sorted(unexpected)}")
    return len(emails)


def validate_contracts() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require("два черновых представления" in readme, "RoleView lifecycle disclosure is missing")
    require("governance/README.md" in readme, "governance navigation is missing")
    require("CC BY 4.0" in readme and "MIT" in readme, "README license summary is incomplete")

    decisions = (ROOT / "governance/decisions.md").read_text(encoding="utf-8")
    for decision_id in ("D-084", "D-085"):
        require(re.search(rf"^\| {decision_id} \|.*\| accepted \|", decisions, re.MULTILINE) is not None,
                f"missing accepted {decision_id}")

    probe = ROOT / "governance/work-packages/evidence/m1-9-5-se01-gate0/probe.py"
    warning = probe.with_name("README.md").read_text(encoding="utf-8")
    require("не запускать в общей среде" in warning.lower(), "probe safety warning is missing")


def main() -> int:
    try:
        state_one = run(sys.executable, "tools/validate_state.py")
        state_two = run(sys.executable, "tools/validate_state.py")
        require(state_one == state_two, "state validator is not idempotent")
        layout = run(sys.executable, "tools/migrate_repository_layout.py", "--check")
        require(layout.startswith("MIGRATION_LAYOUT_OK"), "repository layout validation failed")

        files = tracked_files()
        texts = text_files(files)
        semantic_ids = validate_front_matter(texts)
        email_count = validate_hygiene(texts)
        validate_contracts()
    except (OSError, PublicationError, yaml.YAMLError) as exc:
        print(f"PUBLICATION_ERROR {exc}", file=sys.stderr)
        return 1

    print(
        "PUBLICATION_OK "
        f"tracked={len(files)} "
        f"text={len(texts)} "
        f"ids={semantic_ids} "
        f"emails={email_count} "
        f"state=({state_one})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
