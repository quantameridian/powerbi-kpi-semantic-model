# Sample Data Plan

## Files created

| File | Rows | Purpose |
| --- | ---: | --- |
| `data/sample-operational-data.csv` | 32 | Operational work-item sample data |
| `data/sample-targets.csv` | 16 | Category/priority target thresholds |
| `data/sample-reference-data.csv` | 27 | Reference values for dimensions |

## Scenarios covered

- operational volume across January to June 2026;
- open, in-progress, paused, closed, and cancelled items;
- target comparison by category and priority;
- backlog and overdue examples;
- high-priority and critical unresolved work;
- closed items with and without evidence;
- records with missing owner or due-date fields;
- service-area, owner, category, status, and priority segmentation.

## Deliberate data-readiness issues

The sample data includes a small number of intentional gaps so later Power BI measures can demonstrate readiness warnings:

- missing owner IDs;
- missing due dates;
- closed records with missing closure evidence;
- open high-priority records past due date;
- target combinations that should be assessed through `target_key`.

These gaps are included to support KPI and semantic-model design. Detailed exception-register generation remains the scope of the `operational-data-quality-engine` repo.

## Safety statement

All rows are synthetic and non-client. Owner values are generic role labels, not real people. The data does not describe a real organisation, official process, workplace system, or client engagement.
