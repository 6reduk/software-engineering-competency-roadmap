#!/usr/bin/env python3
"""Rewrite local links after the one-time public repository layout migration."""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py"}
OLD_ROOTS = (
    "docs",
    "matrix",
    "metamodel",
    "pilot",
    "registry",
    "reviews",
    "routes",
    "work-packages",
)

EXACT_RULES = {
    "docs/01-vision-and-scope.md": "curriculum/program/vision-and-scope.md",
    "docs/02-track-map.md": "curriculum/program/track-map.md",
    "docs/03-level-model.md": "curriculum/program/level-model.md",
    "docs/04-learning-flow.md": "curriculum/program/learning-flow.md",
    "docs/05-content-standard.md": "authoring/standards/content-standard.md",
    "docs/06-information-architecture.md": (
        "governance/architecture/information-architecture.md"
    ),
    "docs/07-diagnostic-and-routing.md": (
        "curriculum/program/diagnostic-and-routing.md"
    ),
    "docs/08-audience-and-use-cases.md": (
        "curriculum/program/audience-and-use-cases.md"
    ),
    "docs/09-editorial-standard.md": "authoring/standards/editorial-standard.md",
    "docs/10-content-author-workflow.md": (
        "authoring/workflow/content-author-workflow.md"
    ),
    "routes/README.md": "curriculum/roles/README.md",
    "routes/backend-distributed-systems.md": (
        "curriculum/roles/backend-distributed-systems.md"
    ),
    "routes/architecture-technical-leadership.md": (
        "curriculum/roles/architecture-technical-leadership.md"
    ),
    "matrix/README.md": "curriculum/tracks/README.md",
    "matrix/role-summary.md": "curriculum/roles/role-summary.md",
    "pilot/M1.3-pilot-selection.md": "governance/planning/M1.3-pilot-selection.md",
    "STATUS.md": "governance/state/STATUS.md",
    "MODULE-STATE.md": "governance/state/MODULE-STATE.md",
    "OPEN-QUESTIONS.md": "governance/state/OPEN-QUESTIONS.md",
    "PROGRAM-AUTHORING-CLOSEOUT.md": (
        "governance/state/PROGRAM-AUTHORING-CLOSEOUT.md"
    ),
    "DECISIONS.md": "governance/decisions.md",
    "EXECUTION-PLAN.md": "governance/planning/execution-plan.md",
    "PUBLICATION-AND-CONTINUITY-TODO.md": (
        "governance/planning/publication-and-continuity-todo.md"
    ),
    "REPOSITORY-STRUCTURE.md": "governance/planning/repository-structure.md",
    "REVIEW-PROTOCOL.md": "authoring/workflow/review-protocol.md",
}

PREFIX_RULES = (
    ("matrix/tracks/", "curriculum/tracks/catalog/"),
    ("matrix/intakes/", "governance/planning/intakes/"),
    ("pilot/b2/", "curriculum/tracks/b2/"),
    ("pilot/b3/", "curriculum/tracks/b3/"),
    ("pilot/b5/", "curriculum/tracks/b5/"),
    ("metamodel/", "governance/architecture/metamodel/"),
    ("registry/", "governance/registry/"),
    ("reviews/", "governance/reviews/"),
    ("work-packages/", "governance/work-packages/"),
)

LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def map_old_path(old: str) -> str:
    old = PurePosixPath(old).as_posix()
    if old in EXACT_RULES:
        return EXACT_RULES[old]
    for source, target in PREFIX_RULES:
        if old.startswith(source):
            return target + old[len(source) :]
    return old


def unmap_new_path(new: str) -> str:
    reverse_exact = {value: key for key, value in EXACT_RULES.items()}
    if new in reverse_exact:
        return reverse_exact[new]
    for source, target in PREFIX_RULES:
        if new.startswith(target):
            return source + new[len(target) :]
    return new


def files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts
    )


def old_manifest() -> dict[str, str]:
    result = {rel(path): map_old_path(rel(path)) for path in files()}
    targets = list(result.values())
    if len(targets) != len(set(targets)):
        collisions = sorted({item for item in targets if targets.count(item) > 1})
        raise ValueError(f"migration target collisions: {collisions}")
    for target in targets:
        resolved = (ROOT / target).resolve()
        if ROOT not in resolved.parents and resolved != ROOT:
            raise ValueError(f"target escapes repository: {target}")
    return result


def split_destination(destination: str) -> tuple[str, str, str]:
    left = ""
    right = ""
    value = destination.strip()
    if value.startswith("<") and value.endswith(">"):
        left, right, value = "<", ">", value[1:-1]
    if "#" in value:
        path, anchor = value.split("#", 1)
        return left + path, "#" + anchor, right
    return left + value, "", right


def rewrite_link(
    destination: str,
    old_source: str,
    new_source: str,
    old_files: set[str],
) -> str:
    raw = destination.strip()
    if not raw or raw.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return destination

    path_part, anchor, closing = split_destination(raw)
    opening = "<" if path_part.startswith("<") else ""
    if opening:
        path_part = path_part[1:]
    if not path_part:
        return destination

    old_candidate = posixpath.normpath(
        posixpath.join(posixpath.dirname(old_source), path_part)
    )
    if old_candidate not in old_files:
        root_candidate = posixpath.normpath(path_part)
        if root_candidate in old_files:
            old_candidate = root_candidate
        else:
            return destination

    new_target = map_old_path(old_candidate)
    new_relative = posixpath.relpath(new_target, posixpath.dirname(new_source) or ".")
    if new_relative == ".":
        new_relative = PurePosixPath(new_target).name
    return f"{opening}{new_relative}{anchor}{closing}"


def rewrite_text(
    text: str,
    old_source: str,
    new_source: str,
    old_files: set[str],
) -> str:
    def replace_link(match: re.Match[str]) -> str:
        return (
            match.group(1)
            + rewrite_link(match.group(2), old_source, new_source, old_files)
            + match.group(3)
        )

    return LINK_RE.sub(replace_link, text)


def rewrite(path_prefix: str | None = None) -> int:
    if any((ROOT / item).exists() for item in OLD_ROOTS):
        print("ERROR: old layout still exists; perform the declared git mv set first")
        return 2

    migration_map = "governance/planning/repository-structure.md"
    migration_tool = "tools/migrate_repository_layout.py"
    current_files = files()
    old_files = {unmap_new_path(rel(path)) for path in current_files}
    changed = 0
    for path in current_files:
        current = rel(path)
        if path_prefix and not current.startswith(path_prefix.rstrip("/") + "/"):
            continue
        if (
            current in {migration_map, migration_tool}
            or path.suffix.lower() not in TEXT_SUFFIXES
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        old_source = unmap_new_path(current)
        updated = rewrite_text(text, old_source, current, old_files)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="")
            changed += 1
    print(f"REWRITE_OK changed_files={changed}")
    return 0


def check() -> int:
    old_layout = [item for item in OLD_ROOTS if (ROOT / item).exists()]
    manifest = old_manifest()
    if old_layout:
        moved = sum(source != target for source, target in manifest.items())
        print(
            f"MIGRATION_PLAN_OK files={len(manifest)} moved={moved} "
            f"old_roots={len(old_layout)}"
        )
        return 0

    missing = [target for target in manifest.values() if not (ROOT / target).exists()]
    if missing:
        print(f"ERROR: mapped targets missing: {missing[:10]}")
        return 2

    stale_links = []
    broken_links = []
    checked_links = 0
    for path in files():
        if path.suffix.lower() != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in LINK_RE.finditer(text):
            destination = match.group(2).strip().strip("<>")
            if not destination or destination.startswith(
                ("#", "http://", "https://", "mailto:", "data:")
            ):
                continue
            checked_links += 1
            destination_path = destination.split("#", 1)[0]
            target = (path.parent / destination_path).resolve()
            if ROOT not in target.parents and target != ROOT:
                broken_links.append(f"{rel(path)} -> escapes repo: {destination}")
            elif not target.exists():
                broken_links.append(f"{rel(path)} -> missing: {destination}")
            elif target != ROOT and target.relative_to(ROOT).parts[0] in OLD_ROOTS:
                stale_links.append(f"{rel(path)} -> {destination}")
    if stale_links:
        print("ERROR: links still target old layout")
        print("\n".join(stale_links[:50]))
        return 2
    if broken_links:
        print("ERROR: broken local links")
        print("\n".join(broken_links[:50]))
        return 2

    print(
        f"MIGRATION_LAYOUT_OK files={len(manifest)} "
        f"local_links={checked_links} stale_links=0 broken_links=0"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rewrite", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--path-prefix")
    args = parser.parse_args()
    if args.rewrite == args.check:
        parser.error("choose exactly one of --rewrite or --check")
    return rewrite(args.path_prefix) if args.rewrite else check()


if __name__ == "__main__":
    sys.exit(main())
