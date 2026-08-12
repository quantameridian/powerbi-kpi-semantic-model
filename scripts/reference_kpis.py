"""Independent reference calculations for the synthetic KPI model."""

from __future__ import annotations

import calendar
import csv
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _date(value: str) -> Optional[date]:
    return date.fromisoformat(value) if value else None


def _round(value: float) -> float:
    return round(value, 6)


def calculate_reference_kpis(root: Path = ROOT) -> Dict[str, object]:
    """Calculate the semantic intent of the headline DAX measures."""
    items = _read_csv(root / "data/sample-operational-data.csv")
    target_rows = _read_csv(root / "data/sample-targets.csv")
    targets = {row["target_key"]: row for row in target_rows}
    as_at_date = date(2026, 6, 30)
    active_statuses = {"Open", "In Progress"}

    closed_items = [row for row in items if row["status"] == "Closed"]
    valid_sla_items = []
    for item in closed_items:
        target = targets.get(item["target_key"])
        opened_date = _date(item["opened_date"])
        due_date = _date(item["due_date"])
        closed_date = _date(item["closed_date"])
        if not (target and opened_date and due_date and closed_date):
            continue
        if _date(target["effective_from"]) <= opened_date <= _date(target["effective_to"]):
            valid_sla_items.append((item, target))

    def has_readiness_issue(item: Dict[str, str]) -> bool:
        missing_evidence = item["status"] == "Closed" and (
            item["evidence_status"] == "Missing"
            or (
                item["evidence_status"] != "Not required"
                and not item["closure_evidence_link"]
            )
        )
        return (
            not item["owner_id"]
            or not item["due_date"]
            or item["target_key"] not in targets
            or missing_evidence
        )

    cycle_times = [
        (_date(item["closed_date"]) - _date(item["opened_date"])).days
        for item in closed_items
        if _date(item["closed_date"]) and _date(item["opened_date"])
    ]

    metrics = {
        "total_items": len({item["item_id"] for item in items}),
        "open_items": sum(item["status"] in active_statuses for item in items),
        "paused_items": sum(item["status"] == "Paused" for item in items),
        "backlog_items": sum(
            item["status"] in active_statuses | {"Paused"} for item in items
        ),
        "closed_items": len(closed_items),
        "overdue_active_items": sum(
            item["status"] in active_statuses
            and _date(item["due_date"]) is not None
            and _date(item["due_date"]) < as_at_date
            for item in items
        ),
        "due_soon_items": sum(
            item["status"] in active_statuses
            and _date(item["due_date"]) is not None
            and as_at_date <= _date(item["due_date"]) <= as_at_date + timedelta(days=7)
            for item in items
        ),
        "average_cycle_time_days": _round(sum(cycle_times) / len(cycle_times)),
        "closed_items_with_valid_sla_inputs": len(valid_sla_items),
        "sla_met_items": sum(
            _date(item["closed_date"]) <= _date(item["due_date"])
            for item, _ in valid_sla_items
        ),
        "high_priority_active_items": sum(
            item["status"] in active_statuses
            and item["priority"] in {"High", "Critical"}
            for item in items
        ),
        "high_priority_overdue_items": sum(
            item["status"] in active_statuses
            and item["priority"] in {"High", "Critical"}
            and _date(item["due_date"]) is not None
            and _date(item["due_date"]) < as_at_date
            for item in items
        ),
        "missing_owner_count": sum(not item["owner_id"] for item in items),
        "missing_due_date_count": sum(not item["due_date"] for item in items),
        "missing_target_count": sum(
            item["target_key"] not in targets for item in items
        ),
        "target_matched_items": sum(
            item["target_key"] in targets for item in items
        ),
        "closed_missing_evidence_count": sum(
            item["status"] == "Closed"
            and (
                item["evidence_status"] == "Missing"
                or (
                    item["evidence_status"] != "Not required"
                    and not item["closure_evidence_link"]
                )
            )
            for item in items
        ),
        "review_flag_count": sum(item["review_flag"] == "Yes" for item in items),
        "data_readiness_issue_count": sum(has_readiness_issue(item) for item in items),
    }
    metrics["target_coverage_rate"] = _round(
        metrics["target_matched_items"] / metrics["total_items"]
    )
    metrics["data_readiness_rate"] = _round(
        1 - metrics["data_readiness_issue_count"] / metrics["total_items"]
    )
    metrics["sla_met_rate"] = _round(
        metrics["sla_met_items"] / metrics["closed_items_with_valid_sla_inputs"]
    )
    metrics["sla_target_rate"] = _round(
        sum(float(target["target_met_rate"]) for _, target in valid_sla_items)
        / len(valid_sla_items)
    )
    metrics["sla_variance_to_target"] = _round(
        metrics["sla_met_rate"] - metrics["sla_target_rate"]
    )

    monthly = []
    for month in range(1, 7):
        cutoff = date(2026, month, calendar.monthrange(2026, month)[1])
        opened = sum(
            _date(item["opened_date"]).year == 2026
            and _date(item["opened_date"]).month == month
            for item in items
        )
        closed = sum(
            _date(item["closed_date"]) is not None
            and _date(item["closed_date"]).year == 2026
            and _date(item["closed_date"]).month == month
            for item in items
        )
        backlog = sum(
            _date(item["opened_date"]) <= cutoff
            and item["status"] != "Cancelled"
            and (
                (_date(item["closed_date"]) and _date(item["closed_date"]) > cutoff)
                or (not _date(item["closed_date"]) and item["status"] != "Closed")
            )
            for item in items
        )
        monthly.append(
            {
                "period": f"2026-{month:02d}",
                "opened_items": opened,
                "closed_items": closed,
                "backlog_as_at": backlog,
            }
        )

    return {
        "as_at_date": as_at_date.isoformat(),
        "metrics": metrics,
        "monthly": monthly,
    }
