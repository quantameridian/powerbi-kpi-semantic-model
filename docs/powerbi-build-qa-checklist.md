# Power BI Build QA Checklist

## Purpose

This checklist defines the minimum evidence required before this repository can
claim to contain an implemented Power BI semantic model or report.

The current repository is validated as a source-controlled model plan. It is not
yet a PBIP, PBIR, PBIX, or deployed semantic model.

## Build gate

Before adding a Power BI artifact:

1. Build the model in Power BI Desktop from the CSV files in `data/`.
2. Save as a Power BI Project (`.pbip`) so model/report metadata is source-control friendly.
3. Confirm table names match `powerbi/semantic-model/model-contract.json`.
4. Confirm relationships match the documented relationship plan.
5. Validate all DAX measures in Power BI Desktop.
6. Check measures against `docs/kpi-dictionary.md`.
7. Confirm visuals use shared measures, not visual-only calculations.
8. Refresh the report from a clean checkout.
9. Reopen the PBIP after saving and refresh again.
10. Capture screenshots only from the validated report.

## Semantic model quality gate

Before publication, review:

- fact and dimension grain;
- hidden technical columns;
- measure naming;
- format strings;
- relationship direction;
- inactive date paths;
- blank owner and due-date behavior;
- target coverage behavior;
- row counts against the source CSV files.

## Recommended external checks

- Power BI Desktop relationship and measure validation.
- Tabular Editor Best Practice Analyzer for semantic-model quality.
- Manual KPI owner review against the KPI dictionary.
- README and screenshot review to confirm no stale artifact claims.

## Hard stop conditions

Do not publish or screenshot the report if:

- any DAX measure fails to evaluate;
- a relationship is many-to-many without a documented reason;
- screenshots do not match the current model state;
- the PBIP cannot be reopened and refreshed;
- the README claims an artifact exists before it is committed.
