# KPI Dictionary

The model uses a fixed sample date of 30 June 2026. Counts remain filterable by service area, owner, category and priority unless the definition says otherwise.

## Workload And Flow

| Measure | Definition | Important interpretation |
| --- | --- | --- |
| `Total Items` | Distinct work items in the opened date context | This is intake when a date filter is applied |
| `Open Items` | Current status is Open or In Progress | Ignores date filters because it describes the current state |
| `Paused Items` | Current status is Paused | Reported separately from active work |
| `Backlog Items` | Current status is Open, In Progress or Paused | Current queue, not a historical snapshot |
| `Opened Items` | Alias of `Total Items` | Named for use on flow visuals |
| `Closed Items` | Closed records evaluated through `Closed Date` | Uses the inactive closed date relationship |
| `Backlog As At` | Opened on or before the selected cutoff and not closed by it | Suitable for a month end series with the stated history limitation |

## Timeliness And SLA

| Measure | Definition | Important interpretation |
| --- | --- | --- |
| `Overdue Active Items` | Current active work with a due date before 30 June 2026 | Blank due dates are excluded and shown as a readiness issue |
| `Due Soon Items` | Current active work due from 30 June through 7 July 2026 | The window is controlled by `DueSoonDays` |
| `Average Cycle Time Days` | Mean calendar days from opening to closure | Excludes records without both dates; sensitive to long running work |
| `Closed Items With Valid SLA Inputs` | Closed records with both dates and an effective matching target | This is the SLA denominator |
| `SLA Met Items` | Eligible records closed on or before due date | Calendar days, not working days |
| `SLA Met Rate` | SLA met items divided by eligible closed items | Read with the denominator and target coverage |
| `SLA Target Rate` | Average target rate across eligible closed items | Item weighted, not a simple average of visible target rows |
| `SLA Variance To Target` | Actual rate minus weighted target rate | Negative means performance is below target |

## Assurance

| Measure | Definition | Important interpretation |
| --- | --- | --- |
| `Target Coverage Rate` | Work items with a matching target divided by all work items | Matching does not prove that the target is correct |
| `Missing Owner Count` | Work items without an owner key | A source accountability warning |
| `Missing Due Date Count` | Work items without a due date | These records cannot be classified as overdue |
| `Closed Missing Evidence Count` | Closed work marked Missing, or requiring evidence without a link | The model checks presence, not whether the evidence is sufficient |
| `Data Readiness Issue Count` | Distinct records with any owner, due date, target or closure evidence issue | A record with several problems is counted once |
| `Data Readiness Rate` | One minus issue records divided by total records | A reporting readiness indicator, not service performance |
| `Review Flag Count` | Records explicitly marked Yes for review | The flag criteria are assumed to be governed by the source process |
| `High Priority Overdue Items` | High or Critical active work past due | A focused escalation count |

The complete 31 measure catalogue, including previous month helpers, is in `powerbi/OperationsKPI.SemanticModel/definition/tables/Measures.tmdl`. Format strings and display folders are part of that source.
