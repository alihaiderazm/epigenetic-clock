# 1 · Kickoff: full-context prompt to build Phase I (09.11.2026)

**Who:** Ali Haider Warraich · Carola Gödeke
**Assistant:** Claude Code (VS Code)

## Prompt

Attached and pasted as context:
1. our complete concept document (`Epigenetic_Clock_Project_Concept.txt`: idea, RQ1–RQ3, hypothesis, model table, datasets, solution steps, three linked views, AI4VIS plan, risks, timeline)
2. the full team brief (data/tool links, AI4VIS reading, glossary)

Then the instruction:

> Create new folder named Epigenetic clock. We have a project where have to submit the midpoint submission for this go and download the datasource from the given links. Make a seperate file where you explain what you did in the code. Start working on it and also make step by step for the things of what you did.

### Why this prompt worked
- **Context over instructions:** the instruction is short, but the attached concept defines scope, models, data, research questions and even the deliverable views. The AI derived the midpoint plan (Phase I: filterable predicted-vs-real view, noise slider, first findings, AI4VIS log) from our own timeline table.
- **Documentation as a deliverable:** asking for an explanation file and a step-by-step record made the AI write down where it deviated from the concept.
- **Self-contained goal:** "go and download … start working" let it work end to end instead of returning a plan.

*What we would improve:* name the expected outputs explicitly ("Phase I view + CSV of predictions + first findings"), and ask the AI to *stop and ask* before replacing a tool named in the concept.

## What the AI did

1. Set up the folder structure and a Python virtual environment, and found that **R is not installed**.
2. Found the GEO file sizes. The GSE40279 series matrix is 1.24 GB. The GSE87571 series matrix contains only metadata. The GPL13534 family file is far too large, so it deferred both to later phases.
3. Got the clock weights from the biolearn repository, because methylclockData only serves them via R/ExperimentHub.
4. Wrote a streaming parser: 473,034 CpGs × 656 people reduced to 418 clock CpGs. Result: 0 missing values.
5. Implemented both clocks in Python, then computed group metrics and a perturbation test (noise and missing CpGs, 20 repeats each).
6. Built the interactive D3 page with live recomputation of both clocks.
7. Rendered the page in headless Edge and compared browser vs. Python predictions (max diff 0.02 y).
8. On seeing large plate differences, checked on its own whether plates are confounded with age and ethnicity. They are, so it reported the age-adjusted effect (±3 y) instead of the raw one.

## Decisions

| AI suggestion | Decision | Reason |
|---|---|---|
| Re-implement the clocks in Python instead of methylclock | Accepted, then **questioned** (record 2) and **verified** (record 3) | Keeps the team in Python; risk of a formula error |
| Exact Horvath intercept 0.695507258 instead of biolearn's 0.696 | Accepted | Matches the paper |
| Median imputation instead of kNN | Accepted; in the end not needed (0 missing) | Simple, documented |
| Defer GSE87571 and GPL13534 | Accepted | Not needed for the midpoint |
| Report the plate effect age-adjusted | Accepted | Avoids over-claiming a batch effect |
| Page layout: scatter, error-by-age, stability chart, metrics table, person panel | Accepted, will be refined in Phase II | Covers RQ1 + RQ2; person panel is the hook for the Phase II waterfall |

## Strength / limitation shown
- **Strength:** end-to-end delivery from a short instruction plus rich context, with its own verification (screenshots, numeric check) and a careful statistical step (confounding).
- **Limitation:** it substituted a tool named in our concept (methylclock) without stopping to ask. It was documented, but only in a doc we had not read closely yet.
