# 4 · Submission preparation: requirements pasted verbatim (09.11.2026)

**Who:** Ali Haider Warraich · Carola Gödeke

## Prompt (excerpt)

Pasted as context: the course's *Midpoint Submission* text, the *organizational details* for the repository (team-info.json, workload.json, README.md, `ai-interactions/`, `ai_reflection_midpoint.md`), and our team list with student IDs. Then:

> Now start preparing a repo for submission, According to above criteria. […] And make a video and charts in separate folder. Also remove the folder where you created md files for my explanation. Also the students have equal distribution of workload 0.25
>
> Also create a video and images of graphs.

### Why this prompt worked
- The **official requirement text** was pasted, not paraphrased, so every required file could be mapped one to one.
- The team facts (IDs, names, equal workload) were given directly, so they did not have to be guessed.

## What the AI did

1. Asked one clarifying question it could not answer itself: **which pair used AI** (answer: Ali + Carola).
2. Created `team-info.json`, `workload.json` (0.25 each), the README (task, models, datasets, results) and this folder.
3. Wrote [`scripts/06_make_figures.py`](../scripts/06_make_figures.py): five charts in `figures/`, plus UI screenshots taken with headless Edge.
4. Wrote [`scripts/07_make_video.py`](../scripts/07_make_video.py): slides from `video/slides.json`, narration via Windows text-to-speech, assembled with ffmpeg into `video/progress_update.mp4`.
5. Checked its own output visually and fixed:
   - a legend overlapping bars
   - misaligned bullet points
   - an unreadably small UI screenshot (cropped it)
6. Moved the earlier explanation notes into the README and these records, and removed the old `docs/` folder as requested.

## Decisions

| AI suggestion | Decision | Reason |
|---|---|---|
| First narration: 302 s | **Rejected**, shortened to 268 s | Limit is 300 s, and Pair B needs time for their part |
| Text-to-speech narration | Accepted for the draft | Can be replaced with our own voices; `video/narration_script.md` is the script |
| Pair B slide with a visible TODO | Accepted | The AI cannot know what the non-AI pair did; this must come from Abrar and Haseeb |
| Keep the 1.2 GB raw data out of git | Accepted | GitHub file limit; reproducible via script 01 |

## Strength / limitation shown
- **Strength:** turned an administrative checklist into concrete files quickly and checked its own visual output.
- **Limitation:** content about the other pair, and personal reflections, cannot come from the AI. The reflection was drafted from these records and must be reviewed by us.
