# Synthetic Data

These files describe a fictional service operation from January through June 2026. Names refer to generic teams and roles; identities use the reserved `example.invalid` domain.

The sample includes successful closures, late closures, active overdue work, paused work, missing owners, missing due dates and missing closure evidence. Those imperfections are intentional because the model is expected to show reporting risk rather than silently clean it away.

File contracts and row counts are held in `contracts/model-contract.json`. `make qa` checks headers, keys, references, target matches and access mappings before it validates the Power BI source.

Do not replace these files with client, employee or operational data. Use a private governed source for any real implementation.
