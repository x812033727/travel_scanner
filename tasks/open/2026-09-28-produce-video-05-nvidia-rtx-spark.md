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

- [ ] Planner writes `docs/videos/rtx-spark-local-ai/brief.md` from the season brief, re-reading every changeable fact on its official page.
- [ ] `review-push --gate outline`; then writer, two verifiers, listener review.
- [ ] Narration and dubs wait for the Gemini month to reset on 2026-10-01 (8,106 characters left on 2026-09-28).

## How to verify

```bash
node tools/video/cli.mjs lint --slug rtx-spark-local-ai
node tools/video/cli.mjs status --slug rtx-spark-local-ai --workdir <VIDEO_WORKDIR>
```

## Notes

- The owner asked on 2026-09-28 to keep planning after the first three were packaged (「繼續計畫別的」).
- Schedule slot: 2026-10-27 15:00 UTC in `schedule.csv` (after shipping, so real reviews exist to compare with).
