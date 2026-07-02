# Reviewer Guide

This guide is for an external reviewer checking whether the repo shows useful Power BI thinking without overstating what exists. It separates semantic model planning evidence from the Power BI Desktop artifact that is still missing.

## What To Review First

1. [README.md](../README.md) for the repository state and hard limitation.
2. [powerbi/semantic-model/model-contract.json](../powerbi/semantic-model/model-contract.json) for the planned table, column, relationship, and measure contract.
3. [docs/kpi-dictionary.md](kpi-dictionary.md) for KPI definitions, owners, caveats, and interpretation rules.
4. [docs/dax-measures.md](dax-measures.md) and [measures](../measures) for the DAX catalogue.
5. [docs/rls-and-access-model.md](rls-and-access-model.md) for planned role and access boundaries.
6. [docs/semantic-model-change-control.md](semantic-model-change-control.md) for model promotion and change gates.
7. [docs/commercial-review-scorecard.md](commercial-review-scorecard.md) for the plain assessment of the repo.
8. [docs/semantic-model-review-rubric.md](semantic-model-review-rubric.md) before treating this as an implemented model.

## What This Repository Proves

| Skill | Evidence |
| --- | --- |
| KPI design | KPI dictionary defines meaning, formula, owner, interpretation, limitation, and quality risk |
| Semantic modelling | Model contract documents planned facts, dimensions, relationships, and grain |
| DAX planning | Measures are grouped into core, quality, and trend catalogues for review |
| BI governance | RLS and access design plus semantic model change control are documented before the build |
| Governance | Refresh, handover, artifact boundaries, and screenshot rules are explicit |
| Public repo hygiene | CI, validator, CodeQL, OpenSSF Scorecard, and Power BI security posture docs are present |

## Portfolio Reading

The strongest evidence is the design path before the Desktop build. Read `docs/kpi-dictionary.md`, then `docs/model-design.md`, the model contract, and the DAX files in `measures/`. The checklist in `docs/powerbi-build-qa-checklist.md` explains what still has to happen before any screenshot or PBIX claim should be trusted. This is valuable BI portfolio evidence, but it is not yet proof that the semantic model runs inside Power BI Desktop.

## Fast Local Review

```bash
make qa
```

Expected result:

- JSON theme parses;
- source CSV headers and row counts match the model contract;
- planned relationships reference known tables and columns;
- DAX measure names and table column references match the contract;
- review, limitation, and security documents remain present.

## Good Reviewer Questions

- Are KPI denominators and exclusions clear?
- Does the star schema plan support the management questions?
- Are target and data readiness behaviours documented?
- Are the missing PBIP/TMDL/PBIX artifacts clearly acknowledged?
- What evidence would be required before screenshots should be trusted?

## Current Limitations

- No PBIP, TMDL, PBIR, PBIX, report pages, or screenshots yet.
- DAX is reviewed as text but not Power BI Desktop validated.
- Relationship behaviour is planned, not proven in the engine.
- No Tabular Editor Best Practice Analyzer output yet.

## Strongest Interview Angle

Use this repo to discuss semantic model design, KPI definition, DAX measure planning, access design, and why a serious BI portfolio should not show screenshots until the model has been built and validated.
