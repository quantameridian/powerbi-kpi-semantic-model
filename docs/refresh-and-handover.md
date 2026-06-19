# Refresh and Handover

## Purpose

This document defines the expected refresh, validation, ownership, change-control, and handover approach for the Power BI KPI semantic model project.

The repository currently contains sample data, model design, KPI definitions, a DAX catalogue, report navigation planning, and a theme draft. It does not yet contain a Power BI Desktop model, PBIP/PBIR project, PBIX file, report page, or screenshot.

## Current data sources

The planned Power BI build should use the synthetic CSV files already included in the repository:

| File | Role in model | Refresh expectation |
| --- | --- | --- |
| `data/sample-operational-data.csv` | Main operational item fact source | Refresh with every model validation |
| `data/sample-targets.csv` | Target thresholds by category and priority | Refresh when target logic changes |
| `data/sample-reference-data.csv` | Service area, owner, category, status, and priority reference values | Refresh when reference values change |

These files must remain synthetic and non-client. They should not be replaced with real workplace data.

## Expected refresh approach

Until a Power BI project exists, refresh is a manual design step:

1. Open Power BI Desktop.
2. Load the three CSV files from the repository `data/` folder.
3. In Power Query, set data types for IDs, dates, status, priority, owner, category, target keys, and evidence fields.
4. Split reference data into the planned dimensions or create filtered reference queries.
5. Create or generate a date table that covers the sample reporting period.
6. Build relationships according to `docs/model-design.md`.
7. Add DAX measures from the `measures/` folder.
8. Apply `theme/report-theme.json`.
9. Build the report pages described in `docs/report-navigation.md`.
10. Refresh the model and reconcile key measures against the source rows.
11. Save as a Power BI Project only if the installed Power BI Desktop version supports it.
12. Reopen the saved project and confirm it refreshes.

## Data quality checks before refresh

Before a report refresh is treated as reviewable, check:

| Check | Reason |
| --- | --- |
| Required files are present | Prevents refresh from depending on missing local files |
| Column names match the data dictionary | Prevents Power Query steps and DAX measures from breaking |
| Date fields parse correctly | Supports overdue, due-soon, cycle-time, and trend measures |
| Status and priority values match expected lists | Prevents filters and accepted-value logic from splitting categories |
| `target_key` values match target rows | Supports target coverage and SLA-style measures |
| Owner, category, and service area IDs match reference rows | Keeps dimension filtering reliable |
| Closed records have closure dates where required | Supports cycle-time and closed-item reporting |
| Evidence fields are populated where expected | Supports readiness and assurance measures |

These checks are not a replacement for a full exception-register process. They are the minimum checks before using the Power BI model for review.

## Ownership model

| Area | Expected owner | Responsibility |
| --- | --- | --- |
| Source CSV structure | Report owner | Confirms files, columns, and sample-data assumptions remain stable |
| KPI definitions | KPI owner or reporting lead | Approves formula, grain, interpretation, and limitations |
| Power Query preparation | Power BI developer or analytics engineer | Maintains data types, reference splits, date table, and query naming |
| Semantic model relationships | Power BI developer or analytics engineer | Maintains model structure and relationship behaviour |
| DAX measures | Power BI developer with KPI owner review | Implements, tests, and documents measure changes |
| Report pages | Report owner | Confirms pages answer the intended management questions |
| Refresh validation | Report owner and Power BI developer | Confirms refresh completes and key values reconcile |
| Handover pack | Report owner | Keeps instructions, caveats, and ownership notes current |

In a small portfolio project, one person may perform all roles. The role split still matters because it shows how the work would be controlled in a real setting.

## Maintenance routine

| Timing | Activity | Evidence to keep |
| --- | --- | --- |
| Before model changes | Review whether sample data, KPI definitions, or DAX assumptions have changed | Change note |
| During refresh/build | Refresh source files, Power Query steps, relationships, and measures | Refresh result and reconciliation notes |
| Before screenshots | Confirm visuals are generated from the current model and sample data | Screenshot date and report version |
| Before publication | Check README, limitations, screenshots, and Power BI artefacts match the actual repo state | Public-readiness checklist |
| After measure changes | Update measure files, KPI dictionary if needed, and DAX documentation | Measure-change record |
| Periodic review | Re-check sample data safety, stale wording, and artefact claims | Audit note |

## Measure-change control

DAX measure changes should not be made silently once report pages or screenshots exist. A small change record should capture:

- measure name;
- reason for change;
- old calculation summary;
- new calculation summary;
- affected KPI dictionary entry;
- expected effect on totals, trends, or targets;
- validation performed in Power BI Desktop;
- date changed;
- reviewer or owner.

Changes that alter interpretation should also update `docs/kpi-dictionary.md` and `docs/dax-measures.md`.

## PBIP/PBIR handling

Do not hand-create PBIP or PBIR project files without a valid Power BI Desktop baseline.

Reason:

- PBIP and PBIR files are structured project artefacts created by Power BI Desktop.
- Invalid hand-created files can stop the project opening.
- A credible public repo should only include Power BI project files that have been opened, refreshed, and checked.

When the report is built:

1. Create the model and report in Power BI Desktop.
2. Save or export the work as a Power BI Project if available.
3. Place generated project artefacts under `powerbi/`.
4. Reopen the project from the saved files.
5. Confirm it loads and refreshes against the repository sample data.
6. Update README and limitations to reflect the actual artefacts.

## Handover pack

A reviewer should be able to understand and maintain the model from a compact handover pack.

Minimum handover contents:

- reporting purpose and intended audience;
- sample data files and expected columns;
- Power Query preparation notes;
- fact and dimension table design;
- relationship diagram or model notes;
- KPI dictionary;
- DAX measure catalogue;
- measure-change log;
- report page navigation plan;
- refresh steps;
- data-quality checks before refresh;
- known limitations;
- screenshot policy;
- instructions for adding valid PBIP/PBIR/PBIX artefacts;
- public-readiness checklist.

## Known failure points

When the report is built, document how to handle:

- broken local file paths;
- CSV column changes;
- date parsing errors;
- missing target rows;
- unmatched reference values;
- relationship ambiguity;
- DAX measures returning blank or unexpected totals;
- report visuals not updating after refresh;
- screenshots becoming stale after measure or model changes.
