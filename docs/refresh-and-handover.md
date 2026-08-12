# Refresh And Handover

The checked project reads public synthetic files from GitHub. `GitHubRawBaseUrl`, `AsAtDate` and `DueSoonDays` are Power Query parameters in `expressions.tmdl`.

## Local Refresh

Open `powerbi/OperationsKPI.pbip` in a current Power BI Desktop installation on Windows. The default source points to the `main` branch. To test an unmerged branch or a fork, change `GitHubRawBaseUrl` to its raw content root and keep the trailing slash.

Refresh all queries and check for four common failures first: a renamed CSV column, a blocked anonymous web request, a malformed date, or a source key that no longer matches its reference table. `make qa` catches the structural versions of these problems before Desktop, but only Desktop can confirm that Power Query and the model engine accept the refreshed data.

After refresh, reconcile the headline values with `docs/validation-report.md`. A difference is a release blocker until it is explained by an approved data or definition change.

## Moving Beyond The Sample

A controlled environment should replace the public raw URL with an approved lakehouse, warehouse, dataflow or governed file store. Keep credentials in the gateway, connection or deployment environment. Do not put tokens, tenant identifiers or local paths into TMDL.

The source replacement should preserve the published table contract. If it changes grain, keys, data types or late arriving behaviour, treat it as a model change rather than a connection edit.

## Operating Ownership

The source owner is accountable for schema and extract timing. The KPI owner approves definitions and restatement decisions. The BI owner maintains Power Query, relationships, measures and report bindings. The access owner approves role mappings. One person can cover several roles in a small team, but the approvals should remain distinguishable.

## Release Evidence

A releasable change contains:

- passing `make qa` output;
- a clean Desktop refresh from the intended source;
- reconciled expected values;
- role tests for an allowed, multi area and unmapped identity;
- a rendered page check at the supported display size;
- a note when KPI history needs restatement;
- updated operating and limitation documents.

The Git commit is the version identifier for that evidence. Screenshots, when produced, should name the commit they represent so they do not silently outlive the model.

## Recovery

If a change breaks refresh or report rendering, return to the last accepted commit, reopen the PBIP and refresh again. Do not repair a production copy in the service without bringing the corresponding source change back through review; that creates a model the repository can no longer reproduce.
