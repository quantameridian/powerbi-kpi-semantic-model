"""Validate the source controlled Power BI project and its sample evidence."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import unquote

from reference_kpis import calculate_reference_kpis

CONTRACT_PATH = Path("contracts/model-contract.json")
MODEL_PATH = Path("powerbi/OperationsKPI.SemanticModel/definition")
REPORT_PATH = Path("powerbi/OperationsKPI.Report")
VALIDATION_REPORT_PATH = Path("docs/validation-report.md")
EXPECTED_KPIS_PATH = Path("tests/expected-kpis.json")
THEME_PATH = Path("theme/report-theme.json")
REGISTERED_THEME_PATH = REPORT_PATH / "StaticResources/RegisteredResources/OperationsKPI.json"

REQUIRED_DOCS = [
    Path("README.md"),
    Path("docs/reviewer-guide.md"),
    Path("docs/model-design.md"),
    Path("docs/kpi-dictionary.md"),
    Path("docs/refresh-and-handover.md"),
    Path("docs/rls-and-access-model.md"),
    Path("docs/semantic-model-change-control.md"),
    Path("docs/security-posture.md"),
    Path("docs/limitations.md"),
    Path("docs/desktop-acceptance-test.md"),
]

RETIRED_INTERNAL_FILES = [
    Path("AGENTS.md"),
    Path("docs/commercial-review-scorecard.md"),
    Path("docs/dax-measures.md"),
    Path("docs/implementation-roadmap.md"),
    Path("docs/powerbi-build-qa-checklist.md"),
    Path("docs/public-readiness-audit.md"),
    Path("docs/sample-data-plan.md"),
    Path("docs/semantic-model-review-rubric.md"),
    Path("docs/test-plan.md"),
    Path("measures/core-measures.dax"),
    Path("measures/quality-measures.dax"),
    Path("measures/trend-measures.dax"),
    Path("powerbi/README.md"),
    Path("powerbi/report/README.md"),
    Path("powerbi/screenshots/README.md"),
    Path("powerbi/semantic-model/README.md"),
    Path("powerbi/semantic-model/model-contract.json"),
]


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _csv_header(path: Path) -> List[str]:
    with path.open(newline="", encoding="utf-8") as file:
        return next(csv.reader(file))


def _tmdl_name(value: str) -> str:
    value = value.strip()
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def _parse_tmdl_model(errors: List[str]) -> Dict[str, Set[str]]:
    objects: Dict[str, Set[str]] = {}
    table_pattern = re.compile(r"^table (.+)$", re.MULTILINE)
    column_pattern = re.compile(r"^\tcolumn ('[^']+'|[^\s=]+)(?:\s*=.*)?$", re.MULTILINE)
    measure_pattern = re.compile(r"^\tmeasure ('[^']+'|[^=]+?)\s*=", re.MULTILINE)

    for path in sorted((MODEL_PATH / "tables").glob("*.tmdl")):
        text = path.read_text(encoding="utf-8")
        table_match = table_pattern.search(text)
        if not table_match:
            errors.append(f"{path}: missing table declaration")
            continue
        table_name = _tmdl_name(table_match.group(1))
        fields = {_tmdl_name(value) for value in column_pattern.findall(text)}
        fields.update(_tmdl_name(value.strip()) for value in measure_pattern.findall(text))
        if table_name in objects:
            errors.append(f"duplicate TMDL table: {table_name}")
        objects[table_name] = fields

    return objects


def _validate_dax_delimiters(text: str, errors: List[str]) -> int:
    pattern = re.compile(
        r"^\tmeasure\s+('(?:[^']|'')+'|[^=]+?)\s*=\s*"
        r"(?:```(?P<block>.*?)```|(?P<inline>[^\n]+))",
        re.MULTILINE | re.DOTALL,
    )
    pairs = {")": "(", "]": "[", "}": "{"}
    measure_count = 0

    for match in pattern.finditer(text):
        measure_count += 1
        name = match.group(1).strip()
        expression = match.group("block") or match.group("inline") or ""
        stack: List[str] = []
        in_string = False
        index = 0
        while index < len(expression):
            char = expression[index]
            if char == '"':
                if in_string and index + 1 < len(expression) and expression[index + 1] == '"':
                    index += 2
                    continue
                in_string = not in_string
            elif not in_string and char in "([{":
                stack.append(char)
            elif not in_string and char in pairs:
                if not stack or stack.pop() != pairs[char]:
                    errors.append(f"{name}: unbalanced DAX delimiter {char}")
                    break
            index += 1
        else:
            if in_string:
                errors.append(f"{name}: unterminated DAX string")
            elif stack:
                errors.append(f"{name}: unclosed DAX delimiter {stack[-1]}")

    return measure_count


def _find_entity(node: object) -> Optional[str]:
    if isinstance(node, dict):
        source_ref = node.get("SourceRef")
        if isinstance(source_ref, dict) and isinstance(source_ref.get("Entity"), str):
            return source_ref["Entity"]
        for value in node.values():
            entity = _find_entity(value)
            if entity:
                return entity
    elif isinstance(node, list):
        for value in node:
            entity = _find_entity(value)
            if entity:
                return entity
    return None


def _report_bindings(node: object) -> Iterable[Tuple[str, str]]:
    if isinstance(node, dict):
        for object_type in ("Column", "Measure"):
            field = node.get(object_type)
            if isinstance(field, dict) and isinstance(field.get("Property"), str):
                entity = _find_entity(field.get("Expression"))
                if entity:
                    yield entity, field["Property"]
        for value in node.values():
            yield from _report_bindings(value)
    elif isinstance(node, list):
        for value in node:
            yield from _report_bindings(value)


def _validate_json_files(errors: List[str], notes: List[str]) -> None:
    paths = []
    for root in (Path("contracts"), Path("powerbi"), Path("tests"), Path("theme")):
        paths.extend(root.rglob("*.json"))
    paths.extend([Path("package.json"), Path("package-lock.json")])
    paths += list(Path("powerbi").rglob("*.pbip"))
    paths += list(Path("powerbi").rglob("*.pbir"))
    paths += list(Path("powerbi").rglob(".platform"))
    for path in sorted(set(paths)):
        try:
            _load_json(path)
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{path}: invalid JSON: {error}")
    notes.append(f"Parsed {len(set(paths))} JSON project files")


def _validate_sources(contract: dict, errors: List[str], notes: List[str]) -> None:
    for file_name, expected in contract["source_files"].items():
        path = Path(file_name)
        if not path.exists():
            errors.append(f"missing source file: {path}")
            continue
        if _csv_header(path) != expected["columns"]:
            errors.append(f"{path}: header does not match model contract")
        row_count = len(_read_csv(path))
        if row_count != expected["row_count"]:
            errors.append(
                f"{path}: expected {expected['row_count']} rows, found {row_count}"
            )

    items = _read_csv(Path("data/sample-operational-data.csv"))
    targets = _read_csv(Path("data/sample-targets.csv"))
    references = _read_csv(Path("data/sample-reference-data.csv"))
    access = _read_csv(Path("data/sample-security-access.csv"))

    item_ids = [row["item_id"] for row in items]
    target_keys = [row["target_key"] for row in targets]
    if len(item_ids) != len(set(item_ids)):
        errors.append("operational item IDs must be unique")
    if len(target_keys) != len(set(target_keys)):
        errors.append("target keys must be unique")

    reference_ids = {
        reference_type: {
            row["reference_id"]
            for row in references
            if row["reference_type"] == reference_type
        }
        for reference_type in ("service_area", "owner", "category", "status", "priority")
    }
    target_key_set = set(target_keys)
    for row in items:
        checks = {
            "service_area": row["service_area_id"],
            "category": row["category_id"],
            "status": row["status"],
            "priority": row["priority"],
        }
        if row["owner_id"]:
            checks["owner"] = row["owner_id"]
        for reference_type, value in checks.items():
            if value not in reference_ids[reference_type]:
                errors.append(
                    f"{row['item_id']}: unknown {reference_type} reference {value}"
                )
        if row["target_key"] not in target_key_set:
            errors.append(f"{row['item_id']}: unknown target key {row['target_key']}")

    for row in access:
        if not row["user_principal_name"].endswith("@example.invalid"):
            errors.append("security sample identities must use example.invalid")
        if row["service_area_id"] not in reference_ids["service_area"]:
            errors.append(
                f"access mapping has unknown service area: {row['service_area_id']}"
            )

    notes.append(
        f"Checked {len(items)} work items, {len(targets)} targets, "
        f"{len(references)} references and {len(access)} access grants"
    )


def _validate_tmdl(contract: dict, errors: List[str], notes: List[str]) -> Dict[str, Set[str]]:
    objects = _parse_tmdl_model(errors)
    expected_tables = set(contract["tables"])
    if set(objects) != expected_tables:
        errors.append(
            f"TMDL tables differ from contract: expected {sorted(expected_tables)}, "
            f"found {sorted(objects)}"
        )

    expected_measures = set(contract["measures"])
    found_measures = objects.get("Measures", set()) - {"Value"}
    if found_measures != expected_measures:
        errors.append(
            f"TMDL measures differ from contract: missing "
            f"{sorted(expected_measures - found_measures)}, extra "
            f"{sorted(found_measures - expected_measures)}"
        )

    for relationship in contract["relationships"]:
        for endpoint in (relationship["from"], relationship["to"]):
            table_name, field_name = endpoint.split(".", 1)
            if table_name not in objects or field_name not in objects[table_name]:
                errors.append(f"relationship endpoint missing from TMDL: {endpoint}")

    all_tmdl = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(MODEL_PATH.rglob("*.tmdl"))
    )
    dax_measure_count = _validate_dax_delimiters(
        (MODEL_PATH / "tables/Measures.tmdl").read_text(encoding="utf-8"), errors
    )
    if dax_measure_count != len(expected_measures):
        errors.append(
            f"DAX structure check found {dax_measure_count} measures, "
            f"expected {len(expected_measures)}"
        )
    for forbidden in ("C:\\Users\\", "/Users/", "client_secret", "password="):
        if forbidden.lower() in all_tmdl.lower():
            errors.append(f"TMDL contains forbidden local or secret pattern: {forbidden}")
    if "TODAY(" in all_tmdl.upper():
        errors.append("TMDL must not use TODAY() in deterministic sample measures")
    if "discourageImplicitMeasures" not in all_tmdl:
        errors.append("model must disable implicit measures")
    if "USERPRINCIPALNAME()" not in all_tmdl:
        errors.append("dynamic RLS role must use USERPRINCIPALNAME()")
    if "securityFilteringBehavior: bothDirections" not in all_tmdl:
        errors.append("access bridge relationship must propagate security filtering")

    notes.append(
        f"Matched {len(objects)} TMDL tables and {len(found_measures)} explicit "
        "measures to contract, including balanced DAX delimiters"
    )
    return objects


def _validate_report(
    contract: dict, objects: Dict[str, Set[str]], errors: List[str], notes: List[str]
) -> None:
    project = _load_json(Path(contract["project"]["pbip"]))
    report_path = project["artifacts"][0]["report"]["path"]
    if report_path != "OperationsKPI.Report":
        errors.append("PBIP report path does not target OperationsKPI.Report")

    definition = _load_json(REPORT_PATH / "definition.pbir")
    model_path = definition["datasetReference"]["byPath"]["path"]
    if model_path != "../OperationsKPI.SemanticModel":
        errors.append("PBIR model path does not target OperationsKPI.SemanticModel")

    pages_metadata = _load_json(REPORT_PATH / "definition/pages/pages.json")
    pages_by_name = {page["name"]: page for page in contract["report_pages"]}
    found_page_names = []
    visual_count = 0
    for page_id in pages_metadata["pageOrder"]:
        page_dir = REPORT_PATH / "definition/pages" / page_id
        page = _load_json(page_dir / "page.json")
        found_page_names.append(page["displayName"])
        visual_types = []
        for visual_path in sorted(page_dir.glob("visuals/*/visual.json")):
            visual = _load_json(visual_path)
            visual_types.append(visual["visual"]["visualType"])
            visual_count += 1
            for entity, field in _report_bindings(visual):
                if entity not in objects:
                    errors.append(f"{visual_path}: unknown model table {entity}")
                elif field not in objects[entity]:
                    errors.append(f"{visual_path}: unknown model field {entity}[{field}]")
        expected_types = set(pages_by_name[page["displayName"]]["required_visual_types"])
        if not expected_types.issubset(set(visual_types)):
            errors.append(
                f"{page['displayName']}: missing required visual types "
                f"{sorted(expected_types - set(visual_types))}"
            )

    if found_page_names != list(pages_by_name):
        errors.append(
            f"report page order differs from contract: found {found_page_names}"
        )
    if _load_json(THEME_PATH) != _load_json(REGISTERED_THEME_PATH):
        errors.append("registered report theme differs from theme/report-theme.json")

    notes.append(f"Checked {len(found_page_names)} report pages and {visual_count} visuals")


def _validate_reference_results(errors: List[str], notes: List[str]) -> dict:
    actual = calculate_reference_kpis()
    expected = _load_json(EXPECTED_KPIS_PATH)
    if actual != expected:
        errors.append("reference KPI results differ from tests/expected-kpis.json")
    notes.append(f"Reconciled {len(actual['metrics'])} reference KPI results")
    return actual


def _validate_public_surface(errors: List[str], notes: List[str]) -> None:
    for path in REQUIRED_DOCS:
        if not path.exists():
            errors.append(f"missing operating document: {path}")
    for path in RETIRED_INTERNAL_FILES:
        if path.exists():
            errors.append(f"retired internal file remains public: {path}")

    readme = Path("README.md").read_text(encoding="utf-8")
    for phrase in ("OperationsKPI.pbip", "TMDL", "PBIR", "make qa"):
        if phrase not in readme:
            errors.append(f"README is missing required project reference: {phrase}")
    if re.search(r"screenshot(?:s)? (?:is|are) included", readme, re.IGNORECASE):
        errors.append("README must not claim that report screenshots are included")

    markdown_paths = set(Path(".").glob("*.md"))
    markdown_paths.update(Path(".github").glob("*.md"))
    markdown_paths.update(Path("data").glob("*.md"))
    markdown_paths.update(Path("docs").glob("*.md"))
    local_link_count = 0
    for path in sorted(markdown_paths):
        text = path.read_text(encoding="utf-8")
        for raw_target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target):
                continue
            local_link_count += 1
            linked_path = path.parent / unquote(target)
            if not linked_path.exists():
                errors.append(f"{path}: broken local link {raw_target}")

    notes.append(
        f"Checked {len(REQUIRED_DOCS)} public operating documents and "
        f"{local_link_count} local links"
    )


def _write_report(notes: List[str], results: dict) -> None:
    metrics = results["metrics"]
    rows = [
        ("Total items", metrics["total_items"]),
        ("Current backlog", metrics["backlog_items"]),
        ("Overdue active items", metrics["overdue_active_items"]),
        ("SLA met rate", f"{metrics['sla_met_rate']:.1%}"),
        ("Weighted SLA target", f"{metrics['sla_target_rate']:.1%}"),
        ("Data readiness rate", f"{metrics['data_readiness_rate']:.1%}"),
    ]
    VALIDATION_REPORT_PATH.write_text(
        "\n".join(
            [
                "# Validation Evidence",
                "",
                "Generated by `scripts/validate_powerbi_assets.py --write-report`.",
                "",
                "## Automated Gates",
                "",
                *[f"- {note}." for note in notes],
                "",
                "## Reference Results",
                "",
                f"Results use the fixed sample date `{results['as_at_date']}`.",
                "",
                "| Measure | Expected result |",
                "| --- | ---: |",
                *[f"| {name} | {value} |" for name, value in rows],
                "",
                "## Validation Boundary",
                "",
                "Microsoft TOM deserializes the TMDL during `make qa`, and the Microsoft PBIR authoring CLI validates report structure, bindings and layout. The Python calculations independently reconcile semantic intent against the CSV sources. Power BI Desktop open, refresh, role simulation and rendered page review remain the Windows acceptance gate in `docs/desktop-acceptance-test.md`.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    errors: List[str] = []
    notes: List[str] = []
    contract = _load_json(CONTRACT_PATH)
    if contract.get("status") != "source_controlled_pbip":
        errors.append("model contract must identify the source controlled PBIP state")

    _validate_json_files(errors, notes)
    _validate_sources(contract, errors, notes)
    objects = _validate_tmdl(contract, errors, notes)
    _validate_report(contract, objects, errors, notes)
    results = _validate_reference_results(errors, notes)
    _validate_public_surface(errors, notes)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.write_report:
        _write_report(notes, results)
        notes.append(f"Wrote {VALIDATION_REPORT_PATH}")

    for note in notes:
        print(note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
