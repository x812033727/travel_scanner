---
id: 2026-10-30-zhong-tian-fold-the-e033-pilot
title: "Zhong-tian: fold the e033 pilot lessons into the H3 docs and the cast anchors"
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-30T14:26:49Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/minimax-h3-colab/references/lessons.md
  - .claude/skills/minimax-h3-colab/references/lessons.md
  - .agents/skills/minimax-h3-colab/references/three-stage.md
  - .claude/skills/minimax-h3-colab/references/three-stage.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/cast.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/README.md
---

# Zhong-tian: fold the e033 pilot lessons into the H3 docs and the cast anchors

## Why

The e033 route pilot (2026-10-30) learned eight things, written in the Notes of
`tasks/open/2026-10-30-zhong-tian-e033-g4-pilot.md` ("Pilot receipts and lessons"). They could not go
into the docs that day: every file below sat in the scope of a still-active ticket
(`2026-10-28-31-colab-h3`, `2026-10-30-h3-colab-three-stage`, `2026-10-19-30-1-24`). Until they are folded
in, the next episode (e034-e040) repeats the grinning-through-strain shots and the A100 surprise.

## Definition of done

- [ ] `lessons.md`: the anchor-grin lesson (1), prop size (2), topknot text versus portrait (3), push-in
      overshoot (4), two seeds per retake (5).
- [ ] `three-stage.md`: Ref2VA route comparison and numbers (route A versus B on e033 s08/s09/s21; stages
      2-3 keep stage-1 motion and identity; run 2+3 in one session; `_1080.mp4` output names).
- [ ] `cast.json`: Xu Yan's and Wang Erniu's anchors carry no smile words, and Xu Yan's hair reads
      "gathered up into a topknot on the crown and tied with a cloth band". Regenerate the e034-e040
      Ref2VA lists only if they were built from the old anchors.
- [ ] `production/colab/README.md`: from e033 the series runs route A on G4.

## Steps

- [ ] Wait for, or ask the owners of, the three tickets above to release; claim this one.
- [ ] Copy the lessons from the pilot ticket's Notes, keeping the receipts there.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
npm run check:tasks
```

## Notes

- Exact wording that worked on e033 is in the pilot ticket; the retake prompts are in
  `/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/pilot-a/retake/prompts/` of that session.
