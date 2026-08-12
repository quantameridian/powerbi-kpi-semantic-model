# Model Design

The model supports a monthly operational review without hiding data readiness problems. One synthetic work item is the central fact. Service area, owner, category, status, priority, target and date tables provide controlled filtering around it.

## Grain And Sources

| Table | Grain | Source |
| --- | --- | --- |
| `Operational Item` | One row per work item | `sample-operational-data.csv` |
| `Target` | One row per category and priority target | `sample-targets.csv` |
| `Date` | One row per calendar date | Power Query calendar for 2026 |
| `Service Area`, `Owner`, `Category`, `Status`, `Priority` | One row per controlled reference | Filtered views of `sample-reference-data.csv` |
| `Access Bridge` | One row per identity and service area grant | `sample-security-access.csv` |
| `Model Settings` | One row containing the sample date and warning window | Power Query parameters |
| `Measures` | One hidden placeholder row | Inline Power Query table |

The fact stores source keys but hides them from report users. Names come from dimensions, which prevents slightly different labels from appearing on different pages.

## Relationship Behaviour

Every business dimension filters the fact in one direction. The active date relationship uses `Opened Date`, so an ordinary date selection describes intake. The due and closed relationships remain inactive until a measure explicitly needs them.

`Closed Items`, cycle time and the SLA measures activate the closed date relationship with `USERELATIONSHIP`. They also disable the opened date relationship with `CROSSFILTER(..., NONE)`. Without that second step, a monthly filter could require an item to be both opened and closed in the same month.

The access bridge is the one intentional bidirectional relationship. Its security filter must reach `Service Area`, which then filters the fact through the normal one direction path. No other business relationship uses bidirectional filtering.

## Current And Historical Backlog

`Backlog Items` counts records whose current status is Open, In Progress or Paused. It deliberately ignores the date table because it describes the current queue.

`Backlog As At` is different. It takes the last date in the current context and reconstructs work that had opened but had not closed at that point. Cancelled work is excluded. A record marked Closed without a closure date is not treated as historical backlog because the available fields cannot place its closure in time; it remains a data readiness problem instead.

## Target Eligibility

Targets join by `target_key`, which represents category and priority. A closed item enters the SLA denominator only when it has a due date, a closure date, a matching target and an opened date inside that target’s effective range.

The report compares actual SLA performance with the average target rate across eligible closed items. This weighting means each eligible item contributes once. It avoids using the highest or lowest visible target as an overall threshold.

## Deterministic Sample Context

`AsAtDate` is fixed at 30 June 2026 and `DueSoonDays` is fixed at seven. They are Power Query parameters exposed through `Model Settings`. The fixed date prevents `TODAY()` from changing overdue results between test runs.

Production use would replace the sample date with a controlled refresh date or reporting calendar. That change would need a reviewed update to the expected results and release evidence.

## Deliberate Boundaries

The model imports public synthetic CSV files over HTTPS. It does not attempt query folding, incremental refresh or large volume optimisation. It also does not retain a status event history. Historical backlog can be reconstructed from opened and closed dates, but historical status transitions such as time spent paused cannot be recovered from one current row per item.
