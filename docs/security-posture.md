# Security Posture

This public repository contains synthetic data, project source and validation tools. It must remain safe to clone without exposing client data, tenant metadata, credentials or cached model contents.

## Controls In Source

GitHub workflows use read only repository permission except for the security event permission required by CodeQL and Scorecard. Action references are pinned to commit SHAs. npm and NuGet dependencies are pinned in lock files and monitored by Dependabot.

Power BI cache files, local settings, unapplied query changes, PBIX files and common development outputs are ignored. The TMDL validator rejects personal machine paths and obvious credential patterns. Source queries use HTTPS and contain no authentication material.

The security fixture uses `example.invalid` identities. The role denies operational rows when no active identity mapping exists.

## Repository Settings

GitHub settings should keep secret scanning, push protection, dependency alerts and private vulnerability reporting enabled. Protect `main` with required CI checks, blocked force pushes and a review requirement. Keep the default workflow token read only.

## Power BI Deployment

Do not publish this fixture and then substitute real identities or data in the public branch. A private deployment should source entitlements from a controlled system, manage credentials through Fabric or a gateway, and assign groups rather than individual accounts where practical.

RLS controls row visibility; it does not secure model metadata in the way object level security can. It also does not replace workspace, app, sharing or Build permission design. Export and downstream reuse need their own policy.

## Residual Risk

PBIP, TMDL and PBIR are preview formats that can change with Desktop versions. The project has not completed a Windows refresh or service deployment test. The public web source is suitable for reproducibility, not for confidential or high availability reporting.

Report suspected exposure privately using the route in `SECURITY.md`.
