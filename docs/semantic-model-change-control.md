# Semantic Model Change Control

A model change is ready when another person can understand why the result changed, inspect the source difference and repeat the acceptance checks.

## Assess The Change

Changes to wording or layout usually affect PBIR only. Changes to a measure, relationship, table grain, source type, target rule or access path affect the semantic contract. A measure rename affects both TMDL and every PBIR binding that references it.

Before editing, record the business reason, affected measures and whether history should be restated. If the denominator or target interpretation changes, the KPI owner should approve it before implementation.

## Build And Review

Make the smallest coherent source change. Update `contracts/model-contract.json`, the KPI dictionary and expected result snapshot when their meaning changes. Run `make qa`; the report binding check will catch renamed or missing model objects.

For a result changing update, compare the old and new expected values and explain each movement. A passing test that merely accepts an unexplained new number is not useful evidence.

RLS changes need an allowed identity, a multi area identity and an unmapped identity test. Relationship changes need a path review for ambiguity and filter direction. Source changes need a clean refresh rather than a refresh that depends on an existing local cache.

## Promote Or Roll Back

Only an accepted commit should be deployed. Keep environment identifiers and credentials outside the project. If the Desktop or service result differs from the reviewed source, stop promotion and return to the last accepted commit.

Where a change alters published history, retain the previous result, the new result, the effective period and the approval decision. That record is more important than a generic version number because it explains what report users experienced.
