---
id: 2026-10-30-zhong-tian-fold-the-e033-pilot
title: "Zhong-tian: fold the e033 pilot lessons into the H3 docs and the cast anchors"
status: done
priority: P2
area: docs
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-30T14:29:40Z
created_at: 2026-10-30T14:26:49Z
completed_at: 2026-10-30T14:31:26Z
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

- [x] `lessons.md`: the anchor-grin lesson (1), prop size (2), topknot text versus portrait (3), push-in
      overshoot (4), two seeds per retake (5).
- [x] `three-stage.md`: Ref2VA route comparison and numbers (route A versus B on e033 s08/s09/s21; stages
      2-3 keep stage-1 motion and identity; run 2+3 in one session; `_1080.mp4` output names).
- [x] `cast.json`: Xu Yan's and Wang Erniu's anchors carry no smile words, and Xu Yan's hair reads
      "gathered up into a topknot on the crown and tied with a cloth band". Regenerate the e034-e040
      Ref2VA lists only if they were built from the old anchors.
- [x] `production/colab/README.md`: from e033 the series runs route A on G4.

## Steps

- [x] Wait for, or ask the owners of, the three tickets above to release; claim this one.
- [x] Copy the lessons from the pilot ticket's Notes, keeping the receipts there.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
npm run check:tasks
```

## Notes

- Exact wording that worked on e033 is in the pilot ticket; the retake prompts are in
  `/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/pilot-a/retake/prompts/` of that session.

- 2026-10-30 done: lessons.md §2 (three bullets) and new §6; three-stage.md §7; colab README section for e033 on; cast.json anchors of xuyan and erniu. The three blocking tickets were closed or released the same day (their sessions had no credit). Only `.agents/` holds the references; `.claude/skills/minimax-h3-colab/` has SKILL.md only. No e034-e040 Ref2VA list existed yet, so nothing to regenerate; `ref2manifest.mjs` reads the anchors from cast.json at build time (checked: the regenerated e033 list carries the new text in all 14 Xu Yan prompts). Other characters keep their smile words (the dandy's scornful smile, the magistrate's smile): they are characterisation, not tested here.
