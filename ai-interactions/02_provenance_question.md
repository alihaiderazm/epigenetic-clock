# 2 · Provenance question: "How did you apply methylclockData?" (09.11.2026)

**Who:** Ali Haider Warraich · Carola Gödeke

## Prompt

> how you appled methylclockData directly?

### Why this prompt worked
It does not ask the AI to explain the method in general. It asks *how* a specific claim was realised: our concept names methylclockData as the source of the coefficients. A targeted provenance question like this is hard to answer vaguely.

## AI answer (summary)

- It had **not** used methylclockData at all. The coefficients came from the biolearn repository, and the clocks were computed in Python with the published formulas.
- It explained that methylclockData stores its coefficients on Bioconductor ExperimentHub, which needs R, and R was not installed.
- It stated the risk openly: methylclockData could use a different intercept or coefficient version, which matters most for the unexpected Hannum offset (+4.7 y).
- It proposed two ways to verify: run methylclock in R, or use the online Horvath calculator.

## Decision

Rejected "trust the re-implementation". We asked for real verification (record 3).

## Strength / limitation shown
- **Limitation:** a silent substitution of a tool from our concept. Without this question, our results would rest on an unverified re-implementation.
- **Strength:** when asked directly, the AI answered honestly and named the exact risk and how to test it.
- **Lesson:** after any AI-built pipeline, ask "which source/tool did you actually use for X?" for every tool named in the plan.
