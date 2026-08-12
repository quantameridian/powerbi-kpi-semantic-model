# Power BI Desktop Acceptance Test

Run this test on Windows with a current Power BI Desktop version. Record the Desktop version, Git commit and test date with the result.

## Open And Refresh

1. Start from a clean checkout and run `make qa`.
2. Open `powerbi/OperationsKPI.pbip`.
3. Confirm the report is bound to `OperationsKPI.SemanticModel` and no recovery copy is loaded.
4. Review `GitHubRawBaseUrl`. Use the raw URL for the commit or branch under test.
5. Refresh all queries using anonymous access to the public source.
6. Save, close and reopen the PBIP. Refresh once more to rule out reliance on a stale cache.

The model should show 11 tables, 31 explicit measures, 10 relationships and the `Service Area Manager` role. No ambiguous relationship warning or query error is acceptable.

## Reconcile Results

With no service area filter, confirm:

| Measure | Expected |
| --- | ---: |
| Total Items | 32 |
| Open Items | 14 |
| Backlog Items | 16 |
| Overdue Active Items | 14 |
| Closed Items With Valid SLA Inputs | 13 |
| SLA Met Items | 9 |
| SLA Met Rate | 69.2% |
| SLA Target Rate | 82.1% |
| Data Readiness Issue Count | 7 |
| Data Readiness Rate | 78.1% |

The month end backlog series should be 2, 4, 7, 9, 11 and 16 from January through June. Closed items should be 3, 3, 2, 3, 2 and 2.

## Test Security

Use View As for the `Service Area Manager` role with these identities:

- `manager.sa01@example.invalid`: 9 total items and 5 backlog items.
- `manager.multi@example.invalid`: 16 total items and 8 backlog items.
- `unmapped@example.invalid`: no operational rows.

Confirm that page visuals, table rows and drill context all respect the same service area restriction.

## Review Rendering

Check both pages at 1280 by 720 and at the normal laptop viewport. Text must not clip, visuals must not overlap, table headers must remain readable and the four value card must display all labels. Select each service area and confirm that cards, charts and tables respond consistently.

Inspect the assurance table for the seven known issue records. Confirm that missing owners remain visible and that blank due dates do not appear in the overdue count.

## Acceptance Record

The run passes only when open, refresh, reconciliation, security and rendering all pass against the same commit. Record failures rather than silently updating expected values. Screenshots may be added after acceptance, labelled with the commit and Desktop version.
