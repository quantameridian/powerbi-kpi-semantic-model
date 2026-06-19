"""Validate source-controlled Power BI planning assets.

This script deliberately does not claim to validate DAX inside Power BI Desktop.
It checks repository consistency: JSON, CSV shape, model contract, and DAX
catalogue references.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

CONTRACT_PATH = Path("powerbi/semantic-model/model-contract.json")
THEME_PATH = Path("theme/report-theme.json")
REPORT_PATH = Path("docs/validation-report.md")
REQUIRED_REVIEW_DOCS = [
    Path("docs/reviewer-guide.md"),
    Path("docs/powerbi-build-qa-checklist.md"),
    Path("docs/semantic-model-review-rubric.md"),
    Path("docs/security-posture.md"),
    Path("docs/limitations.md"),
]

TABLE_COLUMN_RE = re.compile(r"'([^']+)'\[([^\]]+)\]")
MEASURE_DEFINITION_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 %/-]+?)\s*=\s*$")


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _read_csv_header_and_count(path: Path) -> tuple[list[str], int]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        row_count = sum(1 for _ in reader)
    return header, row_count


def _extract_measure_definitions(path: Path) -> set[str]:
    measures: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MEASURE_DEFINITION_RE.match(line.strip())
        if match:
            measures.add(match.group(1))
    return measures


def _validate_balanced_parentheses(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count("(") != text.count(")"):
        errors.append(f"{path}: unbalanced parentheses count")


def _validate_contract(contract: dict, errors: list[str], notes: list[str]) -> None:
    if contract.get("status") != "planned_contract_not_pbip":
        errors.append("model contract status must remain explicit that this is not PBIP")

    tables = contract.get("tables", {})
    for file_name, expected in contract.get("source_files", {}).items():
        path = Path(file_name)
        if not path.exists():
            errors.append(f"missing source file: {file_name}")
            continue

        header, row_count = _read_csv_header_and_count(path)
        if header != expected.get("columns"):
            errors.append(f"{file_name}: header does not match model contract")
        if row_count != expected.get("row_count"):
            errors.append(
                f"{file_name}: expected {expected.get('row_count')} rows, found {row_count}"
            )

    for table_name, table in tables.items():
        if not table.get("grain"):
            errors.append(f"{table_name}: missing grain")
        if not table.get("columns"):
            errors.append(f"{table_name}: missing columns")

    for relationship in contract.get("relationships", []):
        for endpoint_name in ("from", "to"):
            endpoint = relationship[endpoint_name]
            table_name, column_name = endpoint.split(".", 1)
            if table_name not in tables:
                errors.append(f"relationship references missing table: {endpoint}")
            elif column_name not in tables[table_name]["columns"]:
                errors.append(f"relationship references missing column: {endpoint}")

    notes.append(f"Validated {len(tables)} planned model tables")
    notes.append(f"Validated {len(contract.get('relationships', []))} planned relationships")


def _validate_dax(contract: dict, errors: list[str], notes: list[str]) -> None:
    tables = contract["tables"]
    expected_measures = set(contract.get("measures", []))
    found_measures: set[str] = set()
    table_refs: set[tuple[str, str]] = set()

    for file_name in contract.get("measure_files", []):
        path = Path(file_name)
        if not path.exists():
            errors.append(f"missing DAX file: {file_name}")
            continue

        _validate_balanced_parentheses(path, errors)
        text = path.read_text(encoding="utf-8")
        found_measures.update(_extract_measure_definitions(path))
        table_refs.update(TABLE_COLUMN_RE.findall(text))

    missing_measures = expected_measures - found_measures
    extra_measures = found_measures - expected_measures
    if missing_measures:
        errors.append(f"contract measures missing from DAX files: {sorted(missing_measures)}")
    if extra_measures:
        errors.append(f"DAX files contain measures missing from contract: {sorted(extra_measures)}")

    for table_name, column_name in sorted(table_refs):
        if table_name not in tables:
            errors.append(f"DAX references missing table: {table_name}")
        elif column_name not in tables[table_name]["columns"]:
            errors.append(f"DAX references missing column: {table_name}[{column_name}]")

    notes.append(f"Validated {len(found_measures)} DAX measure definitions")
    notes.append(f"Validated {len(table_refs)} DAX table-column references")


def _validate_review_docs(errors: list[str], notes: list[str]) -> None:
    required_phrases = {
        Path("docs/reviewer-guide.md"): [
            "What This Repository Proves",
            "Current Limitations",
            "PBIP",
        ],
        Path("docs/semantic-model-review-rubric.md"): [
            "Power BI Desktop build",
            "Source-controlled artifact",
            "Best Practice Analyzer",
        ],
        Path("docs/powerbi-build-qa-checklist.md"): [
            "PBIP",
            "DAX measures",
            "Hard stop conditions",
        ],
        Path("docs/security-posture.md"): [
            "Power BI Artifact Boundary",
            "tenant IDs",
            "refresh credentials",
        ],
        Path("docs/limitations.md"): [
            "not yet a finished Power BI report",
        ],
    }

    for path in REQUIRED_REVIEW_DOCS:
        if not path.exists():
            errors.append(f"missing review document: {path}")
            continue

        text = path.read_text(encoding="utf-8")
        for phrase in required_phrases.get(path, []):
            if phrase not in text:
                errors.append(f"{path}: missing required review phrase: {phrase}")

    notes.append(f"Validated {len(REQUIRED_REVIEW_DOCS)} review and limitation documents")


def _write_report(notes: list[str]) -> None:
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Validation Report",
                "",
                "This report is generated by `scripts/validate_powerbi_assets.py`.",
                "",
                "Important limitation: this validates repository consistency only. It does not validate DAX inside Power BI Desktop and does not prove a PBIP/PBIX artifact exists.",
                "",
                "Commercial-readiness limitation: the repository still fails the implemented-model standard until a real PBIP/TMDL artifact is built, reopened, refreshed, and checked.",
                "",
                "## Checks",
                "",
                *[f"- {note}" for note in notes],
                "",
                "## Current Verdict",
                "",
                "The repository is internally consistent for a planned semantic model, but it still needs a real Power BI Desktop PBIP/TMDL build before it should be treated as an implemented semantic model.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    notes: list[str] = []

    _load_json(THEME_PATH)
    notes.append(f"Validated JSON theme: {THEME_PATH}")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract, errors, notes)
    _validate_dax(contract, errors, notes)
    _validate_review_docs(errors, notes)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.write_report:
        _write_report(notes)
        notes.append(f"Wrote {REPORT_PATH}")

    for note in notes:
        print(note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
