# Narration script
Read aloud one paragraph per slide (generated from video/slides.json).

## Slide 1: When does the epigenetic clock get your age wrong, and why?  (~16 s)

Hi, we are team Neural Ninjas: Ali Haider Warraich, Carola Gödeke, Abrar Ahmad and Haseeb Ahmed. This is our Phase One progress update on the question: when does the epigenetic clock get your age wrong, and why?

## Slide 2: The problem  (~32 s)

Epigenetic clocks are pre-trained linear models that read DNA methylation at a few hundred CpG sites and estimate a person's age. We investigate two published clocks, Horvath and Hannum, first as black boxes. Research question one: for whom are the clocks wrong, and is the error systematic? Research question two: how stable are the predictions under noise and missing CpGs? Our hypothesis: the clocks underestimate very old people.

## Slide 3: Data and models  (~28 s)

Our dataset is GSE40279: 656 people aged 19 to 101, whole blood, Illumina 450K array, with sex, ethnicity and processing plate. Horvath uses 353 CpGs from many tissues. Hannum uses 71 CpGs and was trained on this very dataset, so its results here are optimistic.

## Slide 4: Pipeline and verification  (~24 s)

We keep the 418 clock CpGs from the 1.2 gigabyte matrix; no values were missing. We apply both clocks in Python and cross-checked them against the official methylclock R package: identical for all 656 people. For research question two, we add noise or remove CpGs, twenty times per setting.

## Slide 5: Pair A (with GenAI): interactive Phase I view  (~27 s)

Pair A, Ali and Carola, worked with generative AI and built this interactive view. Each dot is one person, predicted against real age. Filters for clock, sex, ethnicity and age range update everything live. The noise and missing CpG sliders recompute both clocks directly in the browser, and a summary table breaks the error down by age band, sex, ethnicity or plate.

## Slide 6: Finding 1: the error depends on age  (~29 s)

Finding one: the error depends on age. Both clocks lose about two years per decade. They overestimate young people and underestimate old people. For the Horvath clock, the mean error goes from plus two years for people under forty to minus seven and a half years for people over eighty, where half of all people are off by more than eight years. This is systematic bias, not random noise, and it supports our hypothesis.

## Slide 7: Finding 2: Hannum overestimates almost everyone  (~27 s)

Finding two: the Hannum clock overestimates almost everyone, by about 4.7 years on average, even though it was trained on this data. Because methylclock gives exactly the same numbers, this is how the published clock behaves, not a bug in our code. Hannum looks good for the oldest group only because its offset cancels the old-age underestimate. It also overestimates men more than women.

## Slide 8: Finding 3: batch effect, confounded with age  (~23 s)

Finding three: at first, the processing plates look like a big source of error. But plates are confounded with age and ethnicity. All Hispanic participants are on three plates, and the mean age per plate ranges from 39 to 76. After removing the age trend, a batch effect of about plus or minus three years remains.

## Slide 9: Finding 4: stability (RQ2)  (~23 s)

Finding four is about stability. At realistic array noise the clocks are robust, and the error grows by less than one year. With more noise, the Horvath clock degrades about twice as fast as Hannum, because its weights are larger and are multiplied by twenty-one when converted to years. Missing CpGs hurt both clocks about equally.

## Slide 10: Pair B (without GenAI): independent findings  (~37 s)

Pair B, Abrar and Haseeb, worked without generative AI. They ran the pipeline themselves and confirmed the same core pattern: Horvath has lower overall error, but both clocks show a strong age-dependent bias. Young adults are overestimated, the oldest group is underestimated by about seven and a half years on Horvath, and half of those over eighty are off by more than eight years. Hannum overestimates almost everyone, especially men. The residual-to-age correlation of about minus point five shows the error is systematic, not random.

## Slide 11: GenAI experience and next steps  (~31 s)

Our GenAI lessons: it works best with full context, like our whole concept document. Critical follow-up questions mattered most: asking how it applied methylclock revealed a silent substitution and led to the cross-check. Its own verification script also had a bug, caught because the result contradicted other evidence. In Phase Two the pairs swap, and we open the models with per-CpG contribution waterfalls and an aging DNA view. Thank you.
