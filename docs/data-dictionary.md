# Data Dictionary

## Purpose

This dictionary describes the synthetic CSV files used to design the Power BI semantic model. The files are safe sample data for portfolio use and do not represent a real organisation or client.

## Source files

| File | Grain | Row count | Intended model role |
| --- | --- | ---: | --- |
| `data/sample-operational-data.csv` | One row per operational item | 32 | Fact table source |
| `data/sample-targets.csv` | One row per target key | 16 | Target comparison table |
| `data/sample-reference-data.csv` | One row per reference value | 27 | Dimension source |

## `sample-operational-data.csv`

| Field | Type | Meaning | Notes |
| --- | --- | --- | --- |
| `item_id` | Text | Stable operational item key | Planned primary key for `fact_operational_item` |
| `item_reference` | Text | Human-readable item reference | Synthetic, not copied from any real tracker |
| `opened_date` | Date | Date the item was opened | Supports trend and cycle-time measures |
| `due_date` | Date | Date the item is expected to complete | Some rows are blank to support readiness measures |
| `closed_date` | Date | Date the item was completed | Blank for unresolved items |
| `reporting_period` | Text | Month bucket for early reporting examples | Format `YYYY-MM`; later Power BI model should derive period from date tables |
| `service_area_id` | Text | Service area reference key | Joins to service-area rows in reference data |
| `owner_id` | Text | Owner role reference key | Some rows are blank to support missing-owner measures |
| `category_id` | Text | Work category key | Joins to category rows in reference data |
| `status` | Text | Current item status | Expected values: `Open`, `In Progress`, `Paused`, `Closed`, `Cancelled` |
| `priority` | Text | Management priority | Expected values: `Critical`, `High`, `Medium`, `Low` |
| `target_key` | Text | Category/priority key for target comparison | Joins to `sample-targets.csv` |
| `evidence_status` | Text | Evidence state for reporting readiness | Expected values: `Present`, `Missing`, `Pending`, `Not required` |
| `closure_evidence_link` | Text | Synthetic evidence path | Blank where no evidence exists or item is not closed |
| `review_flag` | Text | Indicates whether a management review flag should be visible | Expected values: `Yes`, `No` |
| `notes` | Text | Short synthetic context note | Included for model review, not intended for KPI aggregation |

## `sample-targets.csv`

| Field | Type | Meaning | Notes |
| --- | --- | --- | --- |
| `target_key` | Text | Category/priority key | Planned relationship key from operational items |
| `target_id` | Text | Stable target identifier | Useful for target coverage checks |
| `category_id` | Text | Category the target applies to | Joins to category reference rows |
| `priority` | Text | Priority the target applies to | Joins conceptually to priority reference rows |
| `target_days` | Integer | Expected completion window in calendar days | Used for SLA/timeliness measures |
| `target_met_rate` | Decimal | Illustrative target rate for aggregated review | Example: `0.85` means 85 percent |
| `effective_from` | Date | Target start date | Simplified for this sample |
| `effective_to` | Date | Target end date | Simplified for this sample |
| `target_owner_role` | Text | Role accountable for target interpretation | Role labels only, not real people |
| `notes` | Text | Target context | Not intended for numeric aggregation |

## `sample-reference-data.csv`

| Field | Type | Meaning | Notes |
| --- | --- | --- | --- |
| `reference_type` | Text | Reference group | Values include `service_area`, `owner`, `category`, `status`, `priority` |
| `reference_id` | Text | Reference key | Used to build dimensions |
| `reference_name` | Text | Display label | Role-based and generic |
| `parent_reference_id` | Text | Parent grouping where applicable | Owner rows link to service areas |
| `active_flag` | Boolean text | Whether the reference value is active | Values: `true`, `false` |
| `sort_order` | Integer | Display order | Useful for report slicers |
| `notes` | Text | Reference context | Explains safe synthetic use |

## Planned dimensions from reference data

The single reference CSV can be split in Power Query into:

- `dim_service_area` from `reference_type = "service_area"`;
- `dim_owner` from `reference_type = "owner"`;
- `dim_category` from `reference_type = "category"`;
- `dim_status` from `reference_type = "status"`;
- `dim_priority` from `reference_type = "priority"`.

## Known sample-data imperfections

The data deliberately includes:

- blank `owner_id` values;
- blank `due_date` values;
- closed records with `evidence_status = "Missing"`;
- unresolved high-priority or critical items;
- late closures where `closed_date` is after `due_date`;
- paused items that should not be treated the same as active in-progress work without a clear measure definition.

These imperfections exist to support reporting-readiness and caveat measures in Power BI. They are not intended to imply real operational performance.
