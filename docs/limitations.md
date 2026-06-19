# Limitations

## Current stage

This repository is currently a Power BI semantic-model proof, KPI dictionary, and DAX measure catalogue.

It is not yet a finished Power BI report. No Power BI Desktop model, PBIP/PBIR project, PBIX file, report page, generated screenshot, or validated semantic model artefact is included.

That boundary is deliberate. Power BI artefacts should only be added after they have been created in Power BI Desktop, refreshed against the repository sample data, reopened successfully, and checked against the documentation.

## Data limitations

- The included CSV files are synthetic and non-client.
- The data is small and simplified, so it should not be treated as an operational benchmark.
- Some missing or incomplete fields are deliberate so readiness measures can flag them.
- Evidence paths are illustrative text values only; the repo does not verify whether evidence exists or is sufficient.
- The sample data is designed for model and measure review, not for statistical analysis.
- No protected data, official data, internal workplace material, copied report content, or client data should be introduced.

## Model limitations

- The semantic model is documented but has not yet been built in Power BI Desktop.
- Relationship behaviour has not been tested in Power BI Desktop.
- The intended date model needs validation, especially opened date, due date, closed date, and reporting period behaviour.
- Target logic uses a simplified target key and sample due dates.
- The model intentionally avoids enterprise deployment concerns such as tenant administration, deployment pipelines, row-level security, incremental refresh, and certification.

## DAX limitations

- DAX measures exist as a catalogue in the `measures/` folder.
- The measures are designed against the planned table names and fields in `docs/model-design.md`.
- The measures have not yet been pasted into Power BI Desktop or validated for syntax, filter context, totals, or visual behaviour.
- Trend measures assume a date table and active date context that still need to be confirmed in the Power BI model.
- Target and SLA measures may need adjustment once relationships and date logic are tested.

## Reporting limitations

- No report pages currently exist.
- No screenshots are included.
- Screenshots should only be added after they are captured from a real report built from the repository sample data.
- Report navigation is a build plan, not evidence of an implemented report.
- The repo should not claim live deployment, formal approval, production use, or management adoption.

## Refresh and handover limitations

- Refresh steps are manual build instructions until a Power BI project exists.
- File paths, privacy levels, data types, and refresh behaviour still need to be tested in Power BI Desktop.
- Handover material describes the expected operating approach, not a completed production support process.
- Measure-change control is documented as a recommended practice and has not yet been applied to a live semantic model.

## Portfolio scope limitations

- This repo focuses on Power BI semantic modelling, KPI definitions, DAX planning, report structure, refresh assumptions, and handover.
- It should not duplicate the Python exception register in `operational-data-quality-engine`.
- It should not duplicate the dbt mart in `analytics-engineering-service-mart`.
- It should not become a full decision-support architecture playbook.

## Before publishing Power BI artefacts

Before adding PBIP/PBIR/PBIX files, report screenshots, or claims that a report exists:

1. Build the model in Power BI Desktop from the repository CSV files.
2. Confirm table names and data types match the documentation.
3. Create relationships and validate filter behaviour.
4. Add the DAX measures and check for syntax errors.
5. Reconcile key KPI outputs against the sample CSV rows.
6. Save the Power BI project and reopen it successfully.
7. Refresh the model from the repository data path.
8. Capture screenshots only from the validated report.
9. Update README and related docs to reflect the actual artefacts.
