# Review Scorecard

## Verdict

Current grade: 6.8 / 10 for a public Power BI portfolio repo.

This is useful as a semantic model plan and KPI governance artifact. It is not yet useful as Power BI implementation evidence because there is no PBIP, TMDL, PBIX, Desktop validation, Tabular Editor output, report page, or screenshot.

For a hiring reviewer, the honest signal is modelling judgement. The repo shows how the KPI layer should be defined and governed before visuals are built. That is useful, but it needs a real Power BI artifact before the grade can move into strong implementation territory.

## Research Alignment

This repo lines up with BI expectations around:

- semantic model planning before report design;
- clear KPI definitions and denominators;
- model relationship planning;
- DAX catalogue organization;
- RLS and access design thinking;
- change control and handover.

Reference expectations:

- Microsoft Power BI semantic models: reusable sources of data prepared for reporting and analysis.
- Microsoft/Fabric semantic model guidance: model quality materially affects accuracy and usefulness.
- GitHub and OpenSSF guidance: public repo security hygiene and supply chain checks.

## Strengths

| Area | Assessment |
| --- | --- |
| KPI governance | KPI meaning, denominator, owner, caveat, and quality risk are visible |
| Semantic design | Planned fact/dimension model and relationships are documented |
| Artifact honesty | README is clear that no PBIP/PBIX/screenshots exist yet |
| Validation | JSON, CSV shape, DAX references, and required review docs are checked |
| Enterprise thinking | RLS/access model and semantic model change control are now explicit |

## Portfolio Signal

The repo gives a credible BI design story, but it must be described with care. It shows KPI dictionary design, semantic model planning, DAX catalogue organisation, access and RLS thinking, refresh and handover planning, change control, and clear artifact boundaries around PBIP, PBIX, and screenshots.

## Weaknesses

| Gap | Why it matters |
| --- | --- |
| No PBIP/TMDL | This is the largest blocker; reviewers cannot inspect a real semantic model |
| DAX not validated in the engine | Text validation cannot prove measures evaluate correctly |
| No screenshots | Correctly absent, but visual/report evidence is therefore missing |
| No Tabular Editor/BPA output | No independent semantic model quality review exists |
| No performance evidence | No model size, refresh, relationship, or query behavior evidence exists |

## Best Next Upgrades

1. Build the model in Power BI Desktop using the committed sample CSV files.
2. Save as PBIP/TMDL and commit metadata after clean reopen and refresh.
3. Validate every DAX measure inside Power BI Desktop.
4. Run Tabular Editor Best Practice Analyzer or equivalent checks and document findings.
5. Add screenshots only after the committed artifact is validated.

## Hard Bar

This repo should not be presented as a completed Power BI build. It is a useful
semantic model design artifact, but it needs a real PBIP/TMDL artifact before it
becomes serious BI portfolio evidence.
