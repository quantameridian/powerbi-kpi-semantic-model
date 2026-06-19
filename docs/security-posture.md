# Security Posture

## Scope

This is a public portfolio repository for Power BI semantic-model planning. It
contains synthetic CSV files, DAX text, model documentation, and validation
scripts. It must not contain real business data, tenant-specific configuration,
Power BI credentials, refresh tokens, private workspace IDs, or screenshots from
non-public reports.

## Current Controls

- GitHub Actions CI uses read-only repository contents permission.
- CodeQL scans the Python validation script.
- OpenSSF Scorecard runs on the public repository and uploads SARIF results.
- Dependabot version updates are configured for GitHub Actions.
- The repository validator checks JSON, CSV shape, DAX references, and hard-stop
  limitation documents.
- Security reporting instructions are documented in `SECURITY.md`.

## Power BI Artifact Boundary

No PBIP, PBIR, PBIX, TMDL, screenshot, or deployed semantic model artifact is
currently committed. Future Power BI artifacts must be reviewed before commit.

Do not commit:

- real report data or exported client datasets;
- Power BI tenant IDs, workspace IDs, gateway details, or refresh credentials;
- OAuth tokens, service principal secrets, certificates, or private keys;
- screenshots from internal or non-public reports;
- PBIX/PBIP files that contain cached real data;
- personal paths, local machine names, or private source connection strings.

## GitHub Settings To Keep Enabled

These controls live in GitHub repository settings rather than source files:

- secret scanning and push protection;
- Dependabot alerts and Dependabot security updates;
- branch protection or repository rulesets for `main`;
- required CI checks before merging;
- blocked force pushes and branch deletion;
- default workflow token permission set to read-only.

## Residual Risk

The repository is not yet a validated Power BI model. Security review should not
treat the DAX text or model contract as proof that a Desktop model has safe
refresh behavior, correct tenant isolation, row-level security, or clean
credential handling. Those controls must be reviewed after a real PBIP/TMDL
artifact exists.
