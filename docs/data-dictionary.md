# Data Dictionary

All four CSV files are synthetic. Empty source fields are converted to null before type conversion.

## Operational Items

`sample-operational-data.csv` has one row per item. `item_id` is the stable key and `item_reference` is the report label. Opened, due and closed dates support intake, timeliness and completion analysis. `reporting_period` is retained for traceability but hidden because the conformed date table controls report periods.

`service_area_id`, `owner_id`, `category_id`, `status` and `priority` join to controlled dimensions. `target_key` joins to the effective target. Evidence status, evidence link, review flag and notes support assurance detail.

Blank owner, due date and closure date values are deliberate. They exercise readiness measures and denominator rules.

## Targets

`sample-targets.csv` has one row per `target_key`. Each row identifies its category, priority, target days, target met rate, effective dates and accountable role.

The current SLA measure uses the recorded due date and the target rate. `target_days` is retained for governance, but it is not used to recalculate the supplied due date.

## References

`sample-reference-data.csv` stores five reference types in one source file: service area, owner, category, status and priority. Power Query separates them into dimensions.

`parent_reference_id` links owner roles to a service area in the source. The model does not add an Owner to Service Area relationship because both dimensions already filter the fact and a second path would risk ambiguity.

## Access Grants

`sample-security-access.csv` has one row per identity and service area grant. `active_flag` participates in the role filter. Every identity uses the reserved `example.invalid` domain.

The access file is a test fixture. A deployed model should read an approved entitlement source and retain the same deny by default behaviour for unmapped identities.
