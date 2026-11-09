# Reflection on GenAI usage: Phase I (midpoint)

**AI-aided pair (Phase I):**
- Ali Haider Warraich, K12556511
- Carola Gödeke, K01421148

**Team:** Neural Ninjas · **Assistant:** Claude (Anthropic), via Claude Code in VS Code
**Detailed records:** [`ai-interactions/`](ai-interactions/)

---

## 1. How we used GenAI

We used Claude for three things in Phase I:

1. **Concept** (Carola): drafting the project concept, team brief and a first interactive sketch with invented data.
2. **Implementation** (Ali): the assistant ran in the editor with access to files and the terminal. It downloaded the GEO data, wrote the Python pipeline, applied both clocks, computed metrics and a perturbation test, and built the interactive D3 view.
3. **Verification and submission:** cross-checking against the official methylclock R package, producing the figures and the progress video, and structuring this repository.

The questions, the scope and the acceptance of every result stayed with us. The assistant proposed and executed; we decided what to keep.

## 2. What worked well

- **Rich context was the most effective prompt.** Our kickoff prompt was a short instruction, but it came with the full concept document attached. From that, the AI derived the midpoint deliverables in our own timeline: filterable predicted-vs-real view, noise slider, first findings. It also respected the scope we had set (core only, extras later).
- **Speed on engineering work.** Streaming a 1.2 GB matrix, implementing the Horvath age transformation and making a browser view that recomputes both clocks live would have taken us much longer. That left time to think about the findings.
- **Careful details we had not asked for.**
  - It used the exact published Horvath intercept instead of a rounded one.
  - Before reporting a "plate effect", it checked that plates are confounded with age and ethnicity, and reported the age-adjusted value (±3 y) instead of the misleading raw one (up to 8 y).
- **It checked its own output** when it could: it rendered the page in a headless browser and compared browser predictions with Python (≤ 0.02 y).

## 3. What did not work: failure patterns

- **Silent substitution.** Our concept named methylclock (R). R was not installed, so the AI re-implemented the clocks in Python and took the weights from another source. It wrote this into a documentation file but did not stop to ask. We only realised it when we asked: *"how did you apply methylclockData directly?"*
- **A bug in the AI's own verification.** The first cross-check script reported a Hannum weight mismatch of 44.7 while the predictions were identical. The script had read the chromosome column as the weight. The AI noticed the contradiction and fixed it, but a less consistent result could easily have gone unnoticed.
- **Drafts that need trimming.** The first video narration was 302 s, just over the 300 s limit.
- **Knowledge it cannot have.** Which pair uses AI, and what the non-AI pair did, had to come from us. The AI correctly left a visible TODO for Pair B rather than inventing their findings.

## 4. How we verified AI output

| AI output | How we checked it | Result |
|---|---|---|
| Python implementation of both clocks | official methylclock 1.18.0 on the same input | identical, max diff 0.0000 y |
| Clock coefficients (biolearn CSVs) | methylclockData 1.20.0 | identical (353 + intercept / 71) |
| Browser recomputation (noise slider) | compared with Python predictions | max diff 0.02 y (rounding) |
| "Batch effect" claim | plate × age × ethnicity table; age-adjusted residuals | raw effect mostly age; ±3 y remains |
| Charts, slides, UI | rendered and inspected visually | legend overlap, bullet alignment and small screenshot fixed |

## 5. Influence on our analysis

- The verification step changed how we read **Finding 2**. Hannum overestimates by +4.7 y on its own training data; without the cross-check we would have suspected our own code. Now we know it is real clock behaviour.
- The AI's confounding check changed **Finding 3** from "plates cause large errors" to "plates are confounded with age, and a smaller batch effect remains".
- The research questions, the hypothesis and the interpretation of the age-dependent bias (**Finding 1**) are ours, from the concept. The AI made them testable quickly.

## 6. Best practices we take into Phase II

1. Give the AI the whole plan as context, but tell it to **ask before replacing any tool or data source** named in the plan.
2. After each AI-built step, ask a **provenance question**: "which source/tool did you actually use for X?"
3. Turn doubts into **reproducible checks** (a script with a number), and check that a verification result is consistent with the other evidence before trusting it.
4. Keep the **interaction log as we go.** Reconstructing it afterwards loses the reasons for decisions.

In Phase II we work **without** GenAI, while Abrar and Haseeb use it. We expect the Phase II tasks (contribution waterfall, aging-DNA view) to take us longer without AI. They also depend more on domain interpretation, where our own judgement mattered most in Phase I.
