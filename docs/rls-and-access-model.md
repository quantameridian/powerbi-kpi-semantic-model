# RLS and Access Model

## Purpose

This document defines the planned security and access model for the future Power
BI semantic model. It is a design artifact only. No PBIP, TMDL, PBIX, workspace,
tenant, gateway, or deployed semantic model currently exists in this repository.

The model should define who can see what before report pages are treated as
trusted management outputs.

## Access Principles

- Use role based access rather than individual user logic.
- Keep row level security logic in the semantic model where possible.
- Avoid embedding security logic inside visuals.
- Validate security roles in Power BI Desktop before publication.
- Document any role that can see all data.
- Keep tenant IDs, workspace IDs, group IDs, and user principal names out of the public repository.

## Planned Roles

| Role | Intended audience | Planned data access | Review risk |
| --- | --- | --- | --- |
| Executive reviewer | Senior management reviewing aggregate service performance | All service areas at aggregate and drillthrough level | Broad access must be explicitly approved |
| Service area manager | Manager responsible for one or more service areas | Filtered to assigned service area IDs | Mapping table must be correct and current |
| Team owner | Owner responsible for a specific operational team or owner group | Filtered to assigned owner IDs or team IDs | Blank owner values must remain visible to assurance |
| Assurance reviewer | Reporting assurance or quality reviewer | All rows, with quality and caveat measures visible | Must not hide failed data readiness records |
| Report consumer | General reporting user | Aggregate pages only, no sensitive detail pages | Requires separate report/page permission design |

## Planned Security Tables

The current sample data does not include a security bridge table. A real PBIP
build should add a table similar to:

| Field | Purpose |
| --- | --- |
| `role_name` | Semantic model role or audience group |
| `security_scope_type` | Service area, owner, team, all, or aggregate only |
| `security_scope_id` | Key value that maps to the relevant dimension |
| `active_from` | Effective date for the access rule |
| `active_to` | End date for retired access |
| `approved_by_role` | Role accountable for approving access |

The bridge table must use synthetic values in this public repo unless a real
private implementation is being handled outside GitHub.

## RLS Validation Checklist

Before this repo can claim implemented RLS:

1. Build a real Power BI Desktop model from the sample CSV files.
2. Add a security bridge table with synthetic values.
3. Create roles in Power BI Desktop.
4. Test each role using "View as" or equivalent role validation.
5. Confirm blank owners and data quality failures are not hidden from assurance roles.
6. Document any role that can see all data and its approval route.
7. Reopen and refresh the PBIP from a clean checkout.
8. Add screenshots only after the validated artifact exists.

## Hard Stop Conditions

Do not claim RLS is implemented if:

- role definitions exist only in this document;
- no Power BI Desktop role validation has been performed;
- security mapping uses personal emails, tenant IDs, or private group IDs;
- blank or failed quality records disappear from assurance views;
- screenshots are not generated from the current committed model.

## Current Verdict

The repository currently shows RLS and access design thinking. It does not yet
prove implemented Power BI row level security.
