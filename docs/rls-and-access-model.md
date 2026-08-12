# Row Level Security And Access

The model contains one dynamic role named `Service Area Manager`. It filters the hidden `Access Bridge` table to active rows whose synthetic user principal name matches `USERPRINCIPALNAME()`.

The bridge relationship permits the security filter to reach `Service Area`. From there, the normal one direction relationship filters operational items. This is the only bidirectional path in the model.

## Sample Mappings

The fixture uses the reserved `.invalid` domain and cannot identify a real account.

| Test identity | Allowed service area | Expected total items | Expected current backlog |
| --- | --- | ---: | ---: |
| `manager.sa01@example.invalid` | SA01 | 9 | 5 |
| `manager.sa02@example.invalid` | SA02 | 9 | 6 |
| `manager.sa03@example.invalid` | SA03 | 7 | 3 |
| `manager.sa04@example.invalid` | SA04 | 7 | 2 |
| `manager.multi@example.invalid` | SA01 and SA03 | 16 | 8 |

An unmapped identity should receive no operational rows. This deny by default result is part of the Desktop acceptance test.

## Deployment Responsibilities

The public fixture demonstrates model logic, not service membership. A deployment must replace the sample identities with an approved entitlement source, assign Microsoft Entra security groups to the semantic model role and keep consumers on permissions that allow RLS to be enforced.

Workspace administrators, members and contributors can have permissions that make RLS behave differently from a view only consumer. Role testing therefore needs both Desktop simulation and a service test account with the intended workspace and semantic model permissions.

The access owner should review dormant grants, duplicate mappings and leavers. The BI owner should monitor whether changes to relationships create an unintended path around the secured dimension.

## Known Boundary

TOM confirms that the role and security relationship are valid model objects. It does not evaluate identities. The role has not been simulated in Power BI Desktop or assigned in a Fabric workspace for this commit.
