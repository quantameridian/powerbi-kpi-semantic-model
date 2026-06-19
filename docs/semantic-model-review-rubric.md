# Semantic Model Review Rubric

## Purpose

This rubric defines the evidence a commercial reviewer should expect before the
repository can be treated as a serious Power BI semantic-model artifact.

The current repository passes repository-consistency validation only. It has not
yet passed a Power BI Desktop, PBIP/TMDL, or Tabular Editor validation gate.

## Review Levels

| Level | Evidence | Current status |
| --- | --- | --- |
| 1. Documented model plan | Source data, model contract, KPI dictionary, DAX catalogue, and validation report exist | Passed |
| 2. Repository consistency | CSV shape, JSON syntax, model contract, relationships, and DAX references are checked by script | Passed |
| 3. Power BI Desktop build | Model opens, refreshes, relationships load, and all measures evaluate in Power BI Desktop | Not passed |
| 4. Source-controlled artifact | Valid PBIP/TMDL or equivalent text-based project is committed and can be reopened from a clean clone | Not passed |
| 5. Semantic model quality | Best Practice Analyzer or equivalent review is run and material findings are fixed or justified | Not passed |
| 6. Reviewer evidence | Screenshots, report pages, and README claims are generated only from the validated artifact | Not passed |

## Commercial Review Questions

A serious reviewer should challenge the model on these points:

- Are fact and dimension grains explicit and stable?
- Are relationship cardinality and filter direction intentional?
- Are measures centralized instead of embedded in visuals?
- Are denominator, blank, target, and excluded-record behaviors documented?
- Do KPI names match business definitions and DAX measure names?
- Does the model avoid implying deployment, approval, or real client usage?
- Can another developer rebuild the model from source-controlled files?
- Are limitations visible before screenshots or report-design claims?

## Current Hard Gaps

- There is no PBIP, TMDL, PBIR, PBIX, or Tabular Editor model file.
- DAX is reviewable as text but not engine-validated.
- Relationship behavior is specified by contract but not proven in Power BI Desktop.
- No Best Practice Analyzer output exists.
- No visuals or screenshots exist and none should be added until they come from a validated build.

## Upgrade Path

1. Build the model in Power BI Desktop from the CSV files in `data/`.
2. Save as PBIP with source-control-friendly semantic model metadata.
3. Confirm table and relationship names against `powerbi/semantic-model/model-contract.json`.
4. Validate all DAX measures in the Desktop engine.
5. Run Best Practice Analyzer or equivalent semantic-model checks.
6. Commit the PBIP/TMDL artifact only after reopening and refreshing from a clean checkout.
7. Add screenshots only after the report is built from the committed artifact.
