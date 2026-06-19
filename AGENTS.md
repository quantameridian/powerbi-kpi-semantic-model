# AGENTS.md

This repository is a public technical portfolio project for Power BI semantic modelling, KPI definition, reporting architecture, and decision-support roles.

## Working rules

- Keep changes narrow and intentional.
- Do not introduce fake client claims, protected data, official data, internal workplace material, or exaggerated outcomes.
- Use only realistic non-client sample data.
- Do not pretend Power BI artefacts exist before they have been created and validated.
- Do not add screenshots unless they are generated from the actual report.
- Prefer clear semantic-model structure over unnecessary complexity.
- Keep documentation consistent with the actual files in the repository.
- Avoid generic tutorial-style content and vague marketing language.
- Do not rewrite the whole repository unless explicitly requested.

## Power BI standards

- Define KPI logic before building visuals.
- Keep measure names clear and business-readable.
- Separate facts, dimensions, targets, and measures.
- Document table grain, relationships, filter direction, and caveats.
- Keep DAX measures aligned to the KPI dictionary.
- Avoid hiding critical business logic only in visuals.
- Use Power Query for repeatable preparation steps when the model is implemented.
- Validate model behaviour in Power BI Desktop before claiming outputs exist.

## Documentation standards

Every major layer should explain:

- the reporting problem;
- the intended audience;
- the management questions;
- the model design;
- the KPI definitions;
- the data route;
- how to open or validate artefacts when they exist;
- what outputs are produced;
- what is not covered;
- how the work would translate to a real organisation.

## Verification

Before considering a task complete, check:

- README accuracy;
- no fake client claims;
- no protected or sensitive data;
- no internal workplace references;
- no invented screenshots or report files;
- no broken placeholder sections;
- documentation matches actual repo contents;
- limitations are honest;
- wording is specific and practical.
