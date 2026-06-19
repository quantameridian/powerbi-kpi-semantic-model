# Contributing

This repository is primarily a portfolio artifact, but contributions and review
comments are welcome if they improve clarity, correctness, or reproducibility.

## Before opening a pull request

1. Keep all data synthetic and non-client.
2. Do not add PBIX, PBIP, screenshots, or report exports unless they were
   created from a real validated Power BI Desktop build.
3. Run:

   ```bash
   make test
   ```

4. Update README or docs when model scope, measures, or validation status change.
5. Explain the business reason for the change, not only the documentation edit.

## Review standard

A change is not ready if it makes the project look more complete than it is.
Power BI artifacts must be real, refreshed, and checked before they are claimed.
