# GenAI interaction records: Phase I (AI-aided pair)

**AI-aided pair, Phase I:** Ali Haider Warraich (K12556511), Carola Gödeke (K01421148)
**Assistant:** Claude (Anthropic), used through Claude Code in VS Code. The assistant could read and write files and run commands, so its suggestions were executed and checked directly in the project.
**Period:** concept phase (Oct 2026) and 09.11.2026 (midpoint implementation)

Prompts are quoted verbatim, including typos. Long pasted documents are referenced, not repeated. Each record lists what the AI did, what we accepted, rejected or refined, and what it shows about the strengths and limits of GenAI help.

| # | Record | Interaction | Influence on the analysis |
|---|---|---|---|
| 0 | [00_concept_preparation.md](00_concept_preparation.md) | Concept, team brief and first sketch drafted with Claude | Topic, research questions, model/data choice |
| 1 | [01_kickoff_full_context_prompt.md](01_kickoff_full_context_prompt.md) | Full concept document + brief as context, "start the midpoint" | Whole Phase I pipeline, interactive view, first findings |
| 2 | [02_provenance_question.md](02_provenance_question.md) | "How did you apply methylclockData?" | Revealed a silent substitution (Python instead of the R package) |
| 3 | [03_verification_with_r.md](03_verification_with_r.md) | "Can you download R?" → cross-check | Verified our clocks equal methylclock exactly; the AI's own check had a bug |
| 4 | [04_submission_preparation.md](04_submission_preparation.md) | Course requirements pasted → repository, figures, video | Submission structure, figures, progress video |

A compact table of every suggestion and decision is in [interaction_log.csv](interaction_log.csv).

## Prompt patterns that worked for us

1. **Give the whole context, not a task fragment.** Our kickoff prompt carried the complete concept document: RQs, models, datasets, risks, timeline. The AI could plan the full midpoint (data → clocks → metrics → perturbation → linked view) without many follow-up questions, and it kept to our scope (core only, extras later).
2. **Ask for documentation as a deliverable.** Requesting "a separate file where you explain what you did" and "step by step" made the AI record its own deviations from the concept. That is how we noticed record 2.
3. **Question the provenance of a claim.** A one-line question ("how did you apply methylclockData?") was the most valuable prompt of the phase. It forced the AI to admit that it had not used the package named in our concept.
4. **Turn doubts into a test, not a discussion.** Instead of asking whether the Python clocks were correct, we asked for the tool to check them ("can you download R?"). The answer is now a reproducible script with a numeric result.
5. **Paste the official requirements verbatim.** For the submission we pasted the course's text instead of paraphrasing it. The AI then mapped each requirement to a file, and asked only the one question it could not answer (who is in the AI pair).

## Strengths and limitations we observed

| Strength | Evidence |
|---|---|
| Fast end-to-end implementation | Data download, streaming parser for a 1.2 GB file, both clocks, metrics, perturbation test and interactive D3 view in one session |
| Noticed details we would have missed | Used the exact Horvath intercept (0.695507258) instead of biolearn's rounded 0.696; checked that plates are confounded with age before reporting a batch effect |
| Self-verification when asked | Rendered the UI in a headless browser; compared browser and Python predictions (max diff 0.02 y) |

| Limitation | Evidence |
|---|---|
| Silent substitution | Replaced methylclock with a Python re-implementation because R was missing. This was mentioned in the docs, but easy to overlook until we asked directly (record 2) |
| Bugs in its own checks | The first cross-check script reported a false Hannum weight mismatch (it read the chromosome column as the weight). The AI caught it only because the result contradicted the identical predictions (record 3) |
| Over-long first drafts | The first video narration was 302 s, over the 300 s limit, and had to be shortened (record 4) |
| Cannot know team facts | Which pair used AI, and what the non-AI pair did, had to come from us |
