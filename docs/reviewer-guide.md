# Technical Review Guide

This route separates evidence that can be checked in source control from behaviour that still needs Power BI Desktop.

## Ten Minute Review

Start with the model rather than the report layout.

1. Open `powerbi/OperationsKPI.SemanticModel/definition/model.tmdl` and confirm that implicit measures are disabled.
2. Read `relationships.tmdl`. The opened date path is active, while due and closed date paths are inactive.
3. Inspect `tables/Measures.tmdl`, especially `Closed Items`, `Backlog As At`, `SLA Met Rate` and `Data Readiness Issue Count`.
4. Inspect the dynamic role in `roles/Service Area Manager.tmdl` and the synthetic mappings in `data/sample-security-access.csv`.
5. Open the PBIR page folders and check that every visual binds to a real TMDL object.
6. Read `docs/validation-report.md`, then run `make qa` if the local toolchain is available.

## Questions Worth Asking

The important modelling questions are practical ones. Why does a completion measure need to change the active date path? How is a target deemed valid for a closed item? Can the historical backlog be restated from the available fields? What happens when an identity has no access mapping? Which incomplete records are excluded from SLA and which remain visible as assurance warnings?

The answers are in executable model source and tests, not only in documentation.

## What Automation Proves

Microsoft TOM parses the complete TMDL object graph. Microsoft’s PBIR CLI checks report schemas, visual roles, object bindings, theme registration and canvas bounds. Python checks source contracts, reference integrity and the expected KPI values independently of DAX.

Those checks are meaningful, but they do not run the VertiPaq engine or render Power BI pages. The remaining acceptance work is recorded in `docs/desktop-acceptance-test.md`.

## Evidence Boundary

No screenshot or deployment claim should be accepted for this version. There is no checked Windows Desktop run, Fabric workspace, gateway, refresh schedule or service role assignment. The source is ready for that acceptance stage; it is not evidence that the stage has happened.
