# Limitations

The project source is structurally validated, but the current commit has not been opened and refreshed in Power BI Desktop on Windows. It therefore does not claim rendered page acceptance, DAX engine execution, Power Query refresh acceptance or role simulation.

The synthetic dataset contains 32 items across six months. It is useful for checking definitions and failure cases, not for proving scale, compression, query folding, incremental refresh or capacity performance.

The source records current status rather than status events. Historical backlog can be reconstructed from opened and closed dates, but time spent paused and earlier status transitions cannot be recovered. Closed records without a closure date remain a readiness issue and cannot be placed in a completion period.

SLA uses calendar days and the recorded due date. It does not calculate working days, holidays, pause adjustments or target days from first principles. Evidence checks confirm that a value or link exists; they do not open the link or judge evidence quality.

The dynamic role is present in TMDL, but no Fabric workspace, Microsoft Entra group assignment or service permission test is included. The public identity mappings are non routable fixtures.

The default source is the public GitHub `main` branch. It has no availability guarantee and is not an appropriate production data source. A real deployment needs governed storage, credential management, refresh monitoring and an agreed recovery objective.

Screenshots are withheld until Desktop acceptance is complete. A repository image created by another renderer would not prove that Power BI opened these files or produced the shown result.
