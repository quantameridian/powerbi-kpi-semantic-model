# KPI Dictionary

## Purpose

This document defines the KPI dictionary for the planned Power BI semantic model. The measures are designed against the included sample data and model design, but no Power BI Desktop model or DAX validation exists yet.

The dictionary exists so KPI meaning, calculation scope, ownership, interpretation, and data-quality risks are explicit before visuals are built.

## Source tables

| Source | Role | Notes |
| --- | --- | --- |
| `data/sample-operational-data.csv` | Work-item fact source | One row per operational item |
| `data/sample-targets.csv` | Target lookup source | One row per `target_key` |
| `data/sample-reference-data.csv` | Reference source | Split into service area, owner, category, status, and priority dimensions |

## Shared assumptions

- Reporting date for examples is the report refresh date unless a report page explicitly supplies an as-at date.
- Unresolved items are records where `status` is `Open`, `In Progress`, or `Paused`.
- Active unresolved items are records where `status` is `Open` or `In Progress`; paused items are reported separately.
- Cancelled items are excluded from closure and SLA performance measures unless the measure explicitly says otherwise.
- SLA-style target checks use `target_key` to connect operational items to target rows.
- Dates are calendar days in this sample model. Working-day logic is out of scope until explicitly modelled.

## KPI dictionary

| KPI name | Business meaning | Formula | Grain | Expected owner | Refresh expectation | Interpretation | Limitation | Potential data quality risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Open Items | Count of unresolved work that is actively waiting or being worked. | Count `item_id` where `status` in `Open`, `In Progress`. | Valid by reporting period, service area, owner, category, priority, and status. | Service Manager | Recalculate on every dataset refresh. | Higher values show active workload pressure. Review alongside overdue and priority measures before drawing conclusions. | Excludes paused and cancelled items, so it is not a full queue count. | Incorrect or stale `status` values can understate or overstate active work. |
| Paused Items | Count of unresolved items waiting on a dependency or outside the normal work route. | Count `item_id` where `status = Paused`. | Valid by reporting period, service area, owner, category, and priority. | Service Manager | Recalculate on every dataset refresh. | Helps distinguish workload pressure from work that is blocked or deliberately paused. | Does not explain why the item is paused unless notes or a later dependency field is added. | Teams may use `Paused` inconsistently instead of `Open` or `In Progress`. |
| Closed Items | Count of items completed in the selected period. | Count `item_id` where `status = Closed` and `closed_date` is in the selected date context. | Valid by closed date, reporting period, service area, owner, category, and priority. | Reporting Lead | Recalculate on every dataset refresh. | Shows completed throughput. Compare with opened items and backlog before assessing capacity. | Excludes cancelled items and depends on a populated closure date. | Missing or incorrect `closed_date` values will distort period totals. |
| Backlog Items | Count of work still unresolved at the selected reporting point. | Count `item_id` where `status` in `Open`, `In Progress`, `Paused`. | Valid by service area, owner, category, priority, and as-at date logic. | Service Manager | Recalculate on every dataset refresh; as-at logic should be reviewed before formal reporting. | Shows remaining queue size. Use with priority and overdue views to identify where action is needed. | Current sample uses current status rather than full historical as-at reconstruction. | If historical status changes are not retained, backlog cannot be accurately restated for prior periods. |
| Overdue Active Items | Count of active unresolved items past due date. | Count `item_id` where `status` in `Open`, `In Progress` and `due_date` is before reporting date. | Valid by service area, owner, category, priority, and reporting date. | Service Manager | Recalculate on every dataset refresh. | Highlights active work that has missed the expected completion date. | Does not include paused items; a separate paused-past-due measure may be needed. | Blank or inaccurate `due_date` values can hide overdue work. |
| Due Soon Items | Count of active unresolved items due within the next review window. | Count `item_id` where `status` in `Open`, `In Progress` and `due_date` is between reporting date and reporting date plus 7 calendar days. | Valid by service area, owner, category, priority, and reporting date. | Service Manager | Recalculate on every dataset refresh. | Supports forward-looking review before items become overdue. | The 7-day window is a design assumption and may not fit all operating cadences. | Missing `due_date` values exclude records from the warning window. |
| Average Cycle Time Days | Average elapsed calendar days for completed items. | Average of `closed_date - opened_date` where `status = Closed` and both dates are populated. | Valid by closed date, service area, owner, category, and priority. | Reporting Lead | Recalculate on every dataset refresh. | Higher values indicate slower completion for closed work. Review distribution or median before acting on a small sample. | Excludes open, paused, cancelled, and records missing dates. Averages can be skewed by long-running outliers. | Incorrect opened or closed dates can produce misleading durations. |
| SLA Met Rate | Share of closed target-covered items completed on or before due date. | Count closed items where `closed_date <= due_date` and `target_key` is valid divided by count closed items with valid `target_key`, `due_date`, and `closed_date`. | Valid by closed date, service area, category, priority, and target key. | Reporting Lead | Recalculate on every dataset refresh; target table changes should be reviewed before publication. | Shows whether completed work is meeting expected timescales. Read with target coverage. | Uses sample due dates as the assessment point; does not yet derive due dates from `target_days`. | Missing due dates, missing target keys, or late data entry can shift the rate materially. |
| Target Coverage Rate | Share of operational items that can be matched to a target row. | Count `item_id` with `target_key` found in target table divided by count all `item_id`. | Valid overall and by service area, category, priority, and reporting period. | Reporting Lead | Recalculate on every dataset refresh and whenever target data changes. | Low coverage means SLA or target-performance views are not ready for confident review. | Coverage does not prove target values are correct, only that a target row exists. | Invalid `target_key`, category, or priority values can reduce coverage. |
| Missing Owner Count | Count of work items without an owner role. | Count `item_id` where `owner_id` is blank. | Valid by reporting period, service area, category, status, and priority. | Service Manager | Recalculate on every dataset refresh. | Indicates where accountability is unclear before the report is used for follow-up. | It identifies missing ownership, not whether the assigned owner has capacity. | Blank owner values may be caused by extract issues rather than true operational gaps. |
| Missing Due Date Count | Count of items without a due date. | Count `item_id` where `due_date` is blank. | Valid by reporting period, service area, owner, category, status, and priority. | Reporting Lead | Recalculate on every dataset refresh. | Shows where timeliness and overdue KPIs cannot be trusted for specific records. | Some item types may legitimately not need a due date, but that rule is not modelled yet. | Missing due dates directly suppress overdue and due-soon counts. |
| Closed Missing Evidence Count | Count of closed records without closure evidence. | Count `item_id` where `status = Closed` and (`evidence_status = Missing` or `closure_evidence_link` is blank). | Valid by closed date, service area, owner, category, and priority. | Assurance Lead | Recalculate on every dataset refresh. | Flags closed work that may need supporting evidence before formal review. | Evidence rules are simplified and do not validate whether a link is accessible or sufficient. | Text values in `evidence_status` may be inconsistent; blank links can be ambiguous for records marked `Not required`. |
| High Priority Active Items | Count of active unresolved high-priority or critical work. | Count `item_id` where `status` in `Open`, `In Progress` and `priority` in `High`, `Critical`. | Valid by service area, owner, category, status, and reporting date. | Service Manager | Recalculate on every dataset refresh. | Shows unresolved work that should receive management attention before lower-priority backlog. | Priority is treated as categorical, not weighted by impact or effort. | Inconsistent priority assignment can create false escalation signals. |
| High Priority Overdue Items | Count of active high-priority or critical work that is past due. | Count `item_id` where `status` in `Open`, `In Progress`, `priority` in `High`, `Critical`, and `due_date` is before reporting date. | Valid by service area, owner, category, priority, and reporting date. | Service Manager | Recalculate on every dataset refresh. | Strong escalation signal for management review. Should be investigated before broad backlog commentary. | Excludes paused work and assumes due date is the right escalation threshold. | Blank or stale due dates can hide high-priority overdue items. |
| Review Flag Count | Count of items marked for management review. | Count `item_id` where `review_flag = Yes`. | Valid by reporting period, service area, owner, category, status, and priority. | Assurance Lead | Recalculate on every dataset refresh. | Gives reviewers a controlled list of records needing attention. | The flag is only useful if the criteria for setting it are maintained outside the visual. | Free-text or inconsistent flag values can break the measure. |
| Month-on-Month Open Item Change | Movement in active unresolved work compared with the previous reporting period. | `[Open Items]` for selected period minus `[Open Items]` for previous period. | Valid by reporting period and any stable dimension that exists in both periods. | Reporting Lead | Recalculate on every dataset refresh after period/date table refresh. | Positive values show workload growth; negative values show reduction. Interpret with closed items and new intake. | The sample data has limited history and uses a simple month bucket. | If `reporting_period` is manually populated or inconsistent, trend movement will be unreliable. |

## Measure naming guidance

Planned DAX measure names should match the KPI names unless a shorter report label is needed. Recommended measure names:

- `[Open Items]`
- `[Paused Items]`
- `[Closed Items]`
- `[Backlog Items]`
- `[Overdue Active Items]`
- `[Due Soon Items]`
- `[Average Cycle Time Days]`
- `[SLA Met Rate]`
- `[Target Coverage Rate]`
- `[Missing Owner Count]`
- `[Missing Due Date Count]`
- `[Closed Missing Evidence Count]`
- `[High Priority Active Items]`
- `[High Priority Overdue Items]`
- `[Review Flag Count]`
- `[MoM Open Item Change]`

## Refresh expectations

For this portfolio model, all KPIs are expected to refresh with the Power BI dataset. In a real implementation, refresh ownership would need to define:

- who owns the source extract;
- when the source extract is cut off;
- whether late updates are allowed after a reporting pack is issued;
- who approves changes to target thresholds;
- who reviews KPI changes before a measure is used in a management meeting.

## Data-quality guardrails

The following measures should be visible to report reviewers when interpreting performance KPIs:

- `Missing Owner Count`;
- `Missing Due Date Count`;
- `Closed Missing Evidence Count`;
- `Target Coverage Rate`;
- count of records excluded from SLA calculations.

These guardrails are report-level warnings. They do not replace the separate Python data quality engine, which is responsible for fuller exception-register generation.
