# Reviewer Guide

## What To Review First

1. [README.md](../README.md) for the repository state and hard limitation.
2. [powerbi/semantic-model/model-contract.json](../powerbi/semantic-model/model-contract.json) for the planned table, column, relationship, and measure contract.
3. [docs/kpi-dictionary.md](kpi-dictionary.md) for KPI definitions, owners, caveats, and interpretation rules.
4. [docs/dax-measures.md](dax-measures.md) and [measures](../measures) for the DAX catalogue.
5. [docs/semantic-model-review-rubric.md](semantic-model-review-rubric.md) before treating this as an implemented model.

## What This Repository Proves

| Skill | Evidence |
| --- | --- |
| KPI design | KPI dictionary defines meaning, formula, owner, interpretation, limitation, and quality risk |
| Semantic modelling | Model contract documents planned facts, dimensions, relationships, and grain |
| DAX planning | Measures are grouped into core, quality, and trend catalogues for review |
| Governance | Refresh, handover, artifact-boundary, and screenshot rules are explicitly documented |
| Public repo hygiene | CI, validator, CodeQL, OpenSSF Scorecard, and Power BI security posture docs are present |

## Fast Local Review

```bash
make qa
```

Expected result:

- JSON theme parses;
- source CSV headers and row counts match the model contract;
- planned relationships reference known tables and columns;
- DAX measure names and table-column references match the contract;
- review, limitation, and security documents remain present.

## Good Reviewer Questions

- Are KPI denominators and exclusions clear?
- Does the star-schema plan support the management questions?
- Are target and data-readiness behaviors documented?
- Are the missing PBIP/TMDL/PBIX artifacts clearly acknowledged?
- What evidence would be required before screenshots are credible?

## Current Limitations

- No PBIP, TMDL, PBIR, PBIX, report pages, or screenshots yet.
- DAX is text-reviewed but not Power BI Desktop validated.
- Relationship behavior is planned, not engine-proven.
- No Tabular Editor Best Practice Analyzer output yet.
