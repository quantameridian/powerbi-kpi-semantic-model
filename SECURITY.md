# Security Policy

## Reporting A Vulnerability

Do not open a public issue for suspected secret exposure, unsafe report access or a vulnerable dependency. Use GitHub private vulnerability reporting when it is available, or contact the repository owner through the GitHub profile.

Include the affected file or workflow, a safe reproduction, the likely impact and any proposed remediation. Do not attach real credentials or confidential data to the report.

## Supported Scope

The maintained scope is the current default branch. This repository is a synthetic example and is not approved for client, employee or protected data.

## Data And Credential Boundary

Never commit real report exports, cached semantic model data, tokens, service principal details, tenant or workspace identifiers, gateway configuration, private source URLs or internal screenshots. A deployment must manage those values outside versioned PBIP source.

The implemented controls and residual risks are described in `docs/security-posture.md`.
