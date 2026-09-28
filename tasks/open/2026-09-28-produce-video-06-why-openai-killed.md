---
id: 2026-09-28-produce-video-06-why-openai-killed
title: Produce video 06: why OpenAI killed Sora, and what AI video costs per second now
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-28T10:08:50Z
created_at: 2026-09-28T10:08:25Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/why-openai-killed-sora
---

# Produce video 06: why OpenAI killed Sora, and what AI video costs per second now

## Why

Season video 6 (`docs/ai-video-en-season-01/README.md`, brief `briefs/06-why-openai-killed-sora.md`): OpenAI closed the Sora app on 4/26 and the API on 9/24. The worked example is a cost-per-second-of-video table from each video model's official price page today. zh-TW master with five-language CC and en/ja/ko dubs, like videos 1–4.

## Definition of done

- [ ] `brief.md` in zh-TW with the eight sections and 2–3 outline options; the owner picked one on the outline gate.
- [ ] Script written, verified twice, listener-reviewed; zh-TW narration recorded and checked (Whisper for any flag); no slide state over 15 s.
- [ ] CC in zh-TW, zh-CN, ja, ko, en (each reviewed by a second model); dubs en, ja, ko recorded `--line-by-line` and fitted.
- [ ] Final, publish and dubs gates approved; the owner uploads private; `scoreboard.csv` rows filled.

## Steps

- [ ] Planner writes `docs/videos/why-openai-killed-sora/brief.md` from the season brief, re-reading every changeable fact on its official page.
- [ ] `review-push --gate outline`; then writer, two verifiers, listener review.
- [ ] Narration and dubs wait for the Gemini month to reset on 2026-10-01 (8,106 characters left on 2026-09-28).

## How to verify

```bash
node tools/video/cli.mjs lint --slug why-openai-killed-sora
node tools/video/cli.mjs status --slug why-openai-killed-sora --workdir <VIDEO_WORKDIR>
```

## Notes

- The owner asked on 2026-09-28 to keep planning after the first three were packaged (「繼續計畫別的」).
- Schedule slot: 2026-11-10 15:00 UTC in `schedule.csv`.
