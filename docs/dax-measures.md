# DAX Measures

## Purpose

This document explains the DAX measure catalogue for the planned Power BI KPI semantic model. The measures are stored as plain-text `.dax` files so they can be reviewed in GitHub before a Power BI model exists.

No Power BI Desktop validation has been performed yet. The DAX should be treated as a catalogue and implementation draft until the semantic model tables and relationships are created.

## Files

| File | Measure group | Purpose |
| --- | --- | --- |
| `measures/core-measures.dax` | Core workload, timeliness, target, and priority measures | Main operational KPI measures |
| `measures/quality-measures.dax` | Data readiness and quality guardrails | Warnings about missing fields and weak KPI coverage |
| `measures/trend-measures.dax` | Period comparison measures | Month-on-month movement for selected KPIs |

## Expected model dependencies

The measures assume the planned semantic model documented in `docs/model-design.md`:

- `fact_operational_item`
- `fact_target`
- `dim_date`

The planned fact table grain is one row per operational item. The measures also assume that Power Query or the semantic model has created date-typed fields for `opened_date`, `due_date`, and `closed_date`.

## Core measures

| Measure | Plain-English meaning | Main fields used |
| --- | --- | --- |
| `[Total Items]` | Distinct count of operational items. | `item_id` |
| `[Open Items]` | Active unresolved work where status is `Open` or `In Progress`. | `status`, `item_id` |
| `[Paused Items]` | Unresolved work that is paused rather than actively progressing. | `status`, `item_id` |
| `[Closed Items]` | Work marked as completed. | `status`, `item_id` |
| `[Backlog Items]` | All unresolved work, including paused items. | `status`, `item_id` |
| `[Overdue Active Items]` | Active unresolved work with a due date before the report date. | `status`, `due_date` |
| `[Due Soon Items]` | Active unresolved work due in the next seven calendar days. | `status`, `due_date` |
| `[Average Cycle Time Days]` | Average calendar days between opened and closed date for closed items. | `opened_date`, `closed_date`, `status` |
| `[SLA Met Rate]` | Closed items completed on or before due date divided by closed items with valid SLA inputs. | `closed_date`, `due_date`, `target_key` |
| `[High Priority Active Items]` | Active unresolved high or critical priority work. | `status`, `priority` |
| `[High Priority Overdue Items]` | Active high or critical priority work that is past due. | `status`, `priority`, `due_date` |
| `[Review Flag Count]` | Items explicitly marked for management review. | `review_flag` |

## Quality measures

| Measure | Plain-English meaning | Why it matters |
| --- | --- | --- |
| `[Missing Owner Count]` | Counts records without an owner role. | Ownership gaps weaken accountability and follow-up. |
| `[Missing Due Date Count]` | Counts records without a due date. | Overdue and due-soon measures cannot assess these records. |
| `[Missing Target Key Count]` | Counts records without a target key. | Target-based KPI logic cannot assess these records. |
| `[Target Coverage Rate]` | Share of records that match a target row. | Low coverage means SLA performance is not ready for confident review. |
| `[Closed Missing Evidence Count]` | Counts closed records with missing closure evidence. | Closed-item performance may need assurance review before formal use. |
| `[SLA Excluded Closed Items]` | Closed records excluded from SLA calculation because required inputs are missing. | Explains why the SLA denominator is smaller than total closed items. |
| `[Data Readiness Issue Count]` | Simple sum of selected readiness issue counts. | Gives reviewers a compact warning signal, not a full quality score. |
| `[Records With Review Flag Rate]` | Share of records marked for review. | Indicates how much of the dataset may need management attention. |

## Trend measures

| Measure | Plain-English meaning |
| --- | --- |
| `[Open Items Previous Month]` | Prior-month value for open items. |
| `[MoM Open Item Change]` | Difference between current and previous month open items. |
| `[MoM Open Item Change %]` | Percentage movement in open items from previous month. |
| `[Closed Items Previous Month]` | Prior-month value for closed items. |
| `[MoM Closed Item Change]` | Difference between current and previous month closed items. |
| `[MoM Closed Item Change %]` | Percentage movement in closed items from previous month. |
| `[MoM Overdue Active Item Change]` | Change in overdue active work from the previous month. |
| `[MoM SLA Met Rate Change]` | Percentage-point movement in SLA met rate from the previous month. |
| `[MoM Average Cycle Time Change]` | Movement in average cycle time from the previous month. |

## Important implementation notes

- `[Report Date]` uses the selected `dim_date[date]` value when available and falls back to `TODAY()`. A live reporting process should use a controlled reporting date or refresh cut-off date.
- Trend measures assume `dim_date[date]` is the active date context. If the final model uses opened date, due date, and closed date as separate role-playing dates, the trend measures should be revised.
- `[SLA Met Rate]` currently uses the sample due date as the assessment point. It does not yet derive due date from `target_days`.
- `[Data Readiness Issue Count]` is a simple warning measure. It is not a weighted data-quality score.
- The DAX files intentionally do not claim that a report, screenshot, PBIP, PBIR, or PBIX file exists.

## Validation checklist for a later Power BI layer

Before using these measures in report pages:

1. Load the sample CSVs into Power BI Desktop.
2. Create or confirm the planned table names.
3. Confirm column data types, especially dates and text status fields.
4. Create relationships described in `docs/model-design.md`.
5. Add the measures and confirm they evaluate without syntax errors.
6. Reconcile key measure outputs against the sample CSV rows.
7. Update this document if the final table names, relationship paths, or date logic change.
