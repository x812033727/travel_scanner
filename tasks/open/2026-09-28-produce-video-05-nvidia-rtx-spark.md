---
id: 2026-09-28-produce-video-05-nvidia-rtx-spark
title: Produce video 05: NVIDIA RTX Spark and local AI, can a laptop replace ChatGPT
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-28T10:08:48Z
created_at: 2026-09-28T10:08:16Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/rtx-spark-local-ai
---

# Produce video 05: NVIDIA RTX Spark and local AI, can a laptop replace ChatGPT

## Why

Season video 5 (`docs/ai-video-en-season-01/README.md`, brief `briefs/04-rtx-spark-local-ai.md`): NVIDIA's RTX Spark PCs ship in October; the question viewers search is whether a laptop can finally replace ChatGPT. The worked example is the memory arithmetic of which open-weight models fit in 128 GB at which precision, from the model cards. We never claim to have tested a Spark. zh-TW master with five-language CC and en/ja/ko dubs, like videos 1–4.

## Definition of done

- [ ] `brief.md` in zh-TW with the eight sections and 2–3 outline options; the owner picked one on the outline gate.
- [ ] Script written, verified twice, listener-reviewed; zh-TW narration recorded and checked (Whisper for any flag); no slide state over 15 s.
- [ ] CC in zh-TW, zh-CN, ja, ko, en (each reviewed by a second model); dubs en, ja, ko recorded `--line-by-line` and fitted.
- [ ] Final, publish and dubs gates approved; the owner uploads private; `scoreboard.csv` rows filled.

## Steps

- [x] Planner writes `docs/videos/rtx-spark-local-ai/brief.md` from the season brief, re-reading every changeable fact on its official page.
- [x] `review-push --gate outline`; then writer, two verifiers, listener review.
- [ ] Narration and dubs. They were to wait for the Gemini month to reset on 2026-10-01 (8,106 characters left on
      2026-09-28), but the site's Gemini limit went from 300,000 to 2,000,000 and then 5,000,000 characters a month
      around 15:00 UTC on 2026-09-28, so narration started the same day.

## How to verify

```bash
node tools/video/cli.mjs lint --slug rtx-spark-local-ai
node tools/video/cli.mjs status --slug rtx-spark-local-ai --workdir <VIDEO_WORKDIR>
```

## Notes

- The owner asked on 2026-09-28 to keep planning after the first three were packaged (「繼續計畫別的」).
- Schedule slot: 2026-10-27 15:00 UTC in `schedule.csv` (after shipping, so real reviews exist to compare with).
- 2026-09-28: brief written (three outlines, A recommended) and sent for the owner's pick as outline review `786f8faa-d5d1-4ebf-ac04-15e695827413`. `review-push` needs a video.json, so the outline went up through the automation client's calls instead (report, judge — the stance is blank, so it waits for the owner — then submit), the same steps `flow.mjs` `submitOutline` takes.
- 2026-09-28 10:57 UTC: the owner picked outline A (recorded by `review-pull`; bound to brief.md's hash, so the brief is frozen). Writer dispatched with the season's lessons (pace, `say` for versions/years/percents, date-proof wording, dictionary additions through a locked append script).
- 2026-09-28 evening: script done and verified three times (the owner kept the theoretical speed ceilings, labelled 理論上限／不是實測／每步一個 token; see `claims.md`), listener pass done. Translations: zh-CN (reviewed; one fix, ujr7 专家的参数是 4 位多) and en (review running); ja and ko in progress. Narration started at about 15:25 UTC after the Gemini limit was raised (see Steps).
