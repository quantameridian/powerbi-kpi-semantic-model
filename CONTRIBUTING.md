# Contributing

Changes are welcome when they improve the model, report, evidence or operating clarity without weakening the public data boundary.

Before opening a pull request, run `make install` once and `make qa` for the change. Keep the sample synthetic. Update the model contract, KPI dictionary and expected results when their meaning changes.

A result changing pull request should explain the business reason, old result, new result and restatement decision. A relationship change should explain filter direction. An access change should include allowed, multi area and unmapped identity tests.

Do not commit PBIX files, cached model data, local settings, credentials, tenant details or screenshots from private reports. Desktop screenshots from this project belong only after the acceptance test passes and should identify the tested commit.
