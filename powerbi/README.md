# Power BI Artefact Plan

## Current status

No Power BI report, PBIP project, PBIR folder, semantic model export, or screenshots are currently included in this repository.

This is intentional. These artefacts should be created from a real Power BI Desktop build, not invented as static files.

## Planned folder use

| Folder | Intended contents | Current status |
| --- | --- | --- |
| `powerbi/semantic-model/` | Power BI semantic model project artefacts once generated from Power BI Desktop | Scaffold only |
| `powerbi/report/` | Power BI report project artefacts once generated from Power BI Desktop | Scaffold only |
| `powerbi/screenshots/` | Screenshots captured from the actual report build | Scaffold only |

## Why PBIP/PBIR files are not hand-created here

PBIP and PBIR files are Power BI project artefacts. A valid baseline should be created by Power BI Desktop so the report and semantic model can be opened, refreshed, and checked.

This repository may later hold PBIP/PBIR files, but only after:

1. synthetic sample CSV data exists;
2. a Power BI semantic model has been built;
3. report pages have been created;
4. the project has been saved or exported from Power BI Desktop;
5. the generated files have been reopened and validated.

## Manual build steps

1. Create or confirm the sample data files in `data/`.
2. Open Power BI Desktop.
3. Import the sample CSV files.
4. Use Power Query to set data types and rename columns consistently.
5. Build the semantic model relationships.
6. Add DAX measures from the `measures/` folder.
7. Apply `theme/report-theme.json`.
8. Build the pages described in `docs/report-navigation.md`.
9. Save as a Power BI Project if available.
10. Place generated project artefacts in this `powerbi/` folder.
11. Reopen the project from the saved files and confirm it loads.
12. Capture screenshots only after the report is validated.

## Acceptance criteria before public release

- The report opens in Power BI Desktop.
- The model refreshes against repository sample data.
- The DAX measures match the KPI dictionary.
- Report pages match the navigation plan.
- Screenshots, if included, match the actual report.
- No local-only paths or personal workspace details are required for a reviewer to understand the project.

