# 0 · Concept, team brief and first sketch (October 2026)

**Who:** Ali Haider Warraich · Carola Gödeke
**Assistant:** Claude

## What was done with AI

As stated in our concept document ("this concept and the first sketch were prepared with Claude"), the following were drafted with Claude:
- the project concept: research questions RQ1–RQ3, the hypothesis, the choice of the Horvath and Hannum clocks, the datasets GSE40279 / GSE87571 / GPL13534, the risk table and the timeline
- the team brief with the glossary
- a first interactive sketch with **invented** data, showing three linked views

## Our decisions

| Suggestion | Decision | Why |
|---|---|---|
| Lean core (Horvath + Hannum, GSE40279 only) with optional extras | Accepted | Realistic for seven weeks |
| Sketch with invented data | Accepted *as orientation only* | The non-AI pair was told not to use it as a template |
| Interpretation of the AI4VIS rules (pairs swap in Phase II) | Accepted, open question in the Moodle forum | The slide does not specify it |

## Original prompts

Key prompts from the October Claude session (Carola):

**Prompt 1 – initial framing**
> We are a student team in the AI and Visualization Lab at JKU Linz. The course requires us to investigate an AI model (or models) with visualization, first as a black box (Phase I) and later as a white box (Phase II).  
> Topic idea: epigenetic clocks that predict chronological age from DNA methylation.  
> Can you help me draft a short project concept that includes: research questions, a working hypothesis, two concrete published clocks, suitable public datasets, risks, and a realistic 7-week timeline? Keep the core lean; extras can be optional.

**Prompt 2 – refining the clocks and data**
> Focus on the two most-cited clocks: Horvath 2013 (multi-tissue) and Hannum 2013 (blood).  
> Dataset preference: something with age, sex, ethnicity and technical batch information. GSE40279 looks promising because it has 656 samples and plate info.  
> Also flag that Hannum was trained on GSE40279 so any evaluation on it will be optimistic. Suggest one independent test set we could use later if time allows.

**Prompt 3 – research questions & hypothesis**
> Turn this into three research questions:  
> RQ1 – where / for whom the clocks fail (bias vs random error)  
> RQ2 – robustness to noise and missing CpGs  
> RQ3 – (Phase II) which CpGs drive the errors  
> Working hypothesis: the clocks underestimate very old people because some CpG sites saturate.  
> Keep the language precise enough that we can later measure whether the hypothesis is supported.

**Prompt 4 – team brief + sketch request**
> From the concept above, produce a short team brief with a glossary of the key terms (CpG, beta value, epigenetic clock, residual, age acceleration).  
> Also sketch a simple interactive visualization (invented data is fine) that would let us explore predicted vs real age, filter by group, and later add a noise slider. This is only for orientation; the other pair should not treat it as a template.

These four prompts produced the concept document, the team brief and the first interactive sketch that are referenced in the repository.
