#!/usr/bin/env python3
"""Read-only validation of the canonical program state manifest."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - explicit operator guidance
    raise SystemExit(
        "STATE_ERROR PyYAML is required: "
        "python -m pip install -r requirements-validation.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance/state/current-state.yaml"
REQUIREMENTS = ROOT / "requirements-validation.txt"
EXPECTED_STATES = {
    "closed-for-authoring": 10,
    "partial": 3,
    "blueprint-only": 14,
    "not-started": 0,
}


class StateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise StateError(message)


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise StateError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(data, dict), "manifest root must be a mapping")
    return data


def repository_path(value: Any, field: str) -> Path:
    require(isinstance(value, str) and value.strip() != "", f"{field} must be a path")
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise StateError(f"{field} leaves repository: {value}") from exc
    require(candidate.is_file(), f"{field} does not exist: {value}")
    return candidate


def validate_front_matter(path: Path, expected_status: str) -> None:
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"missing front matter: {path.relative_to(ROOT)}")
    end = text.find("\n---\n", 4)
    require(end >= 0, f"unclosed front matter: {path.relative_to(ROOT)}")
    try:
        metadata = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        raise StateError(f"invalid front matter in {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(metadata, dict), f"front matter must be a mapping: {path.relative_to(ROOT)}")
    require(metadata.get("status") == expected_status, f"unexpected status in {path.relative_to(ROOT)}")


def validate_manifest(data: dict[str, Any]) -> None:
    require(data.get("schema_version") == 1, "unsupported schema_version")
    require(data.get("status") == "accepted", "current state must be accepted")

    requirements_text = REQUIREMENTS.read_text(encoding="utf-8").strip()
    require(requirements_text == "PyYAML==6.0.3", "validation dependency pin drifted")
    require(yaml.__version__ == "6.0.3", "installed PyYAML does not match requirements-validation.txt")

    repository = data.get("repository")
    require(isinstance(repository, dict), "repository must be a mapping")
    origin = repository.get("manifest_origin")
    require(isinstance(origin, dict), "manifest_origin must be a mapping")
    require(origin.get("stage") == "P3" and origin.get("decision") == "D-082",
            "manifest origin drifted")
    require(origin.get("public_commit_claim") == "none-pre-snapshot-history-is-local",
            "manifest origin must not claim a public pre-snapshot commit")
    require(repository.get("public_history_policy") == "sanitized-snapshot",
            "public history policy drifted")
    require(repository.get("governance_archive_policy") == "included-historical-non-normative",
            "governance archive policy drifted")
    repository_path(repository.get("layout"), "repository.layout")

    lifecycle = data.get("lifecycle")
    require(isinstance(lifecycle, dict), "lifecycle must be a mapping")
    require(lifecycle.get("program_mode") == "publication-preparation", "unexpected program_mode")
    require(lifecycle.get("authoring_phase") == "closed", "authoring_phase must remain closed")
    for field in ("learner_execution", "proficiency_confirmation"):
        item = lifecycle.get(field)
        require(isinstance(item, dict) and item.get("status") == "out-of-scope", f"{field} boundary changed")

    gate = lifecycle.get("last_accepted_gate")
    require(isinstance(gate, dict) and gate.get("id") == "G35", "last accepted gate must be G35")
    acceptance = repository_path(gate.get("acceptance"), "last_accepted_gate.acceptance")
    validate_front_matter(acceptance, "accepted")
    repository_path(gate.get("closeout"), "last_accepted_gate.closeout")

    publication = data.get("publication")
    require(isinstance(publication, dict), "publication must be a mapping")
    completed = publication.get("completed_stages")
    require(isinstance(completed, list) and completed, "completed_stages must be a non-empty list")
    expected_completed = [f"P{index}" for index in range(len(completed))]
    require(completed == expected_completed, "completed publication stages must be contiguous from P0")
    require(publication.get("last_completed_stage") == completed[-1], "last_completed_stage must match completed_stages")
    next_action = publication.get("next_action")
    require(isinstance(next_action, dict), "exactly one next_action mapping is required")
    expected_next = f"P{len(completed)}"
    require(next_action.get("id") == expected_next, f"next action must be {expected_next}")
    repository_path(publication.get("plan"), "publication.plan")
    repository_path(next_action.get("source"), "publication.next_action.source")

    module_state = data.get("module_state")
    require(isinstance(module_state, dict), "module_state must be a mapping")
    require(module_state.get("defined_modules") == 27, "defined module count drifted")
    require(module_state.get("counts") == EXPECTED_STATES, "module state counts drifted")
    require(sum(EXPECTED_STATES.values()) == 27, "module state total is invalid")
    require(module_state.get("track_skeleton_only") == 12, "track skeleton count drifted")
    module_path = repository_path(module_state.get("source"), "module_state.source")
    module_text = module_path.read_text(encoding="utf-8")
    module_rows: list[list[str]] = []
    for line in module_text.splitlines():
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 4 and cells[1].strip("`") in EXPECTED_STATES:
            module_rows.append(cells)
    require(len(module_rows) == 27, f"MODULE-STATE has {len(module_rows)} module rows, expected 27")
    for state, count in EXPECTED_STATES.items():
        actual = sum(row[1].strip("`") == state for row in module_rows)
        require(actual == count, f"MODULE-STATE has {actual} rows for {state}, expected {count}")

    verticals = data.get("deep_verticals")
    require(isinstance(verticals, list) and [item.get("id") for item in verticals] == ["B2", "B3", "B5"], "deep verticals drifted")
    for index, item in enumerate(verticals):
        require(isinstance(item, dict), f"deep_verticals[{index}] must be a mapping")
        repository_path(item.get("source"), f"deep_verticals[{index}].source")
        acceptance_path = repository_path(item.get("closeout_acceptance"), f"deep_verticals[{index}].closeout_acceptance")
        validate_front_matter(acceptance_path, "accepted")

    debt = data.get("debt")
    require(isinstance(debt, list) and debt, "debt must be a non-empty list")
    debt_ids: set[str] = set()
    for index, item in enumerate(debt):
        require(isinstance(item, dict), f"debt[{index}] must be a mapping")
        for field in ("id", "owner", "disposition", "trigger", "source"):
            require(isinstance(item.get(field), str) and item[field].strip(), f"debt[{index}].{field} is required")
        require(item["id"] not in debt_ids, f"duplicate debt id: {item['id']}")
        debt_ids.add(item["id"])
        repository_path(item["source"], f"debt[{index}].source")

    traceability = data.get("traceability")
    require(isinstance(traceability, dict), "traceability must be a mapping")
    for field, value in traceability.items():
        repository_path(value, f"traceability.{field}")

    decisions = (ROOT / traceability["decisions"]).read_text(encoding="utf-8")
    for decision_id in ("D-079", "D-080", "D-081", "D-082", "D-083", "D-084", "D-085", "D-086"):
        require(
            re.search(rf"^\| {decision_id} \|.*\| accepted \|", decisions, re.MULTILINE) is not None,
            f"{decision_id} is missing",
        )

    if "P5" in completed:
        plan = (ROOT / publication["plan"]).read_text(encoding="utf-8")
        status = (ROOT / traceability["program_status"]).read_text(encoding="utf-8")
        require("### P5. Подготовить публичный README и лицензию — выполнено" in plan,
                "P5 completion is missing from publication plan")
        require("| P5 Публичный README и лицензирование | Завершён |" in status,
                "P5 completion is missing from STATUS")
        require(next_action["id"] in plan, "next action is missing from publication plan")

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        require(
            "две черновые подборки навыков" in readme
            and "Обе подборки имеют статус `drafting`" in readme,
            "README must disclose drafting competency-selection status",
        )
        require("governance/README.md" in readme,
                "README must link the governance normative boundary")

        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        notice_text = (ROOT / "NOTICE").read_text(encoding="utf-8")
        for marker in ("CC BY 4.0", "The MIT License", "Shestakov Dmitriy <6reduk@gmail.com>"):
            require(marker in license_text, f"LICENSE marker is missing: {marker}")
        for marker in ("CC BY 4.0", "MIT License", "Shestakov Dmitriy <6reduk@gmail.com>"):
            require(marker in notice_text, f"NOTICE marker is missing: {marker}")

        for relative in (
            "governance/README.md",
            "governance/reviews/README.md",
            "governance/work-packages/README.md",
            "governance/work-packages/evidence/m1-9-5-se01-gate0/README.md",
        ):
            repository_path(relative, f"publication boundary {relative}")


def main() -> int:
    try:
        data = load_yaml(MANIFEST)
        validate_manifest(data)
    except StateError as exc:
        print(f"STATE_ERROR {exc}", file=sys.stderr)
        return 1

    counts = data["module_state"]["counts"]
    print(
        "STATE_OK "
        f"schema={data['schema_version']} "
        f"mode={data['lifecycle']['program_mode']} "
        f"gate={data['lifecycle']['last_accepted_gate']['id']} "
        f"modules={counts['closed-for-authoring']}/{counts['partial']}/{counts['blueprint-only']}/{counts['not-started']} "
        f"debt={len(data['debt'])} "
        f"next={data['publication']['next_action']['id']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
