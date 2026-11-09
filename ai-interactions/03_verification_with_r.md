# 3 · Turning the doubt into a test: install R and cross-check (09.11.2026)

**Who:** Ali Haider Warraich · Carola Gödeke

## Prompt

> can you download the R?

### Why this prompt worked
Instead of discussing whether the Python clocks are correct, it asks for the tool that can *prove* it. The result is a script with a number, not an opinion.

## What the AI did

1. Installed R 4.6.2 (`winget install RProject.R`). The per-user install failed, so it retried machine-wide.
2. Installed methylclock 1.18.0 and methylclockData 1.20.0 from Bioconductor.
3. Wrote [`scripts/05_methylclock_crosscheck.R`](../scripts/05_methylclock_crosscheck.R):
   - compares the coefficients (methylclockData vs. our CSVs)
   - runs `DNAmAge()` with the same input
   - compares all 656 predictions

## The AI's own bug

The first run reported:

```
Hannum coefficients: max |weight diff| = 44.7
Hannum predictions:  max |diff| = 0.0000 y
```

These two lines contradict each other: identical predictions are impossible with different weights. The AI flagged the contradiction and inspected the table. methylclockData's Hannum table has the *chromosome* in column 2, and the script had read it as the weight. It fixed the column selection by name and reran:

| Clock | Coefficients | Predictions (n = 656) |
|---|---|---|
| Horvath | identical (353 CpGs, intercept 0.695507258) | max diff 0.0000 y, r = 1.000000 |
| Hannum | identical (71 CpGs, no intercept) | max diff 0.0000 y, r = 1.000000 |

## Influence on the analysis

- Our Python clocks are now **verified**, and Phase II can build on them: the contributions `w·β` come from the same code.
- The surprising Hannum offset (+4.7 y on its own training data) is **real clock behaviour**, not our bug. It became Finding 2.

## Decision

Accepted after the fix.

## Strength / limitation shown
- **Limitation:** an AI-written verification script can be wrong itself, and here it was. A check is only trustworthy if its result is consistent with the other evidence.
- **Strength:** the AI noticed the inconsistency rather than reporting the mismatch as a finding.
