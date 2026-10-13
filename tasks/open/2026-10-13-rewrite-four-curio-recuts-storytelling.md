---
id: 2026-10-13-rewrite-four-curio-recuts-storytelling
title: Rewrite the four remaining Curio recuts under the storytelling rules
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-curio-rewrites
claimed_at: 2026-10-13T03:23:44Z
created_at: 2026-10-13T03:23:41Z
completed_at:
branch: claude/youtube-narrative-flow-1cadbc
depends_on: []
scope:
  - docs/videos/curio-h02-v2
  - docs/videos/curio-h03-v2
  - docs/videos/curio-l08-v2
  - docs/videos/curio-u02-v2
---

# Rewrite the four remaining Curio recuts under the storytelling rules

## Why

The owner, 2026-10-13, after seeing H01 rewritten under the new storytelling rules
(`2026-10-13-narrated-videos-tell-one-story-with`, PR #1478): 「五支重製片也照新規則重做」. H01
already has its second version in `docs/videos/curio-h01-v2`; this task is the other four.

The delivered recuts were built from the old rules, so each one reads as sections stitched
together: chapters named by their job (流傳的版本, 保密 58 年的方法, 專家怎麼解釋), label
sentences opening them, an opening condensation that gives away the reveals the body then tells
again, and a close that names the next file.

Two of the four have no script in this repository. The recut package says those source folders are
kept separately, so H02 and H03 are written fresh from their fact checks
(`docs/videos/history-curiosity/topic-checks/H02.md` and `H03.md`, both checked and independently
reviewed on 2026-10-10) rather than re-told from an old script. U02 and L08 do have their scripts,
claims and research here, and are re-told from them with no new facts.

## Definition of done

- [x] `docs/videos/curio-u02-v2`, `curio-l08-v2`, `curio-h02-v2`, `curio-h03-v2` each hold
      `brief.md`, `video.json`, `claims.md` and `NOTES.md`, written to the new rules: one story in
      the order it happened, chapters as beats named by what happens in them, a condensation that
      is one scene told up to the first fact that makes no sense, a `loops` table with every hook
      paid off and named, and a close that says nothing about the next file.
- [x] Each one: `cli.mjs lint --slug <slug>` with 0 errors and no unexplained narrative warning,
      and `cli.mjs narrative --slug <slug> --answers <file>` passing the ten blind questions.
- [x] Every fact traces to the episode's own checked sources (the old `claims.md` for U02 and L08,
      the topic check for H02 and H03). Nothing new is researched or invented.
- [x] `NOTES.md` gives the owner the old chapter names against the new, the shipped opening against
      the new one, where each loop lands, and what was deliberately dropped.
- [ ] The owner has read the four and said whether they go on to pictures and narration.

## Steps

- [x] Four scripts, one agent each (done in parallel on 2026-10-13).
- [ ] Owner reads them beside the shipped films.
- [ ] If the owner says go: produce each under its NEW slug, and stop the old project on
      /admin/videos first (the owner's rule of 2026-10-11: an approved slug never has its content
      swapped). Pictures are about US$2–3 an episode on MiniMax, then narration, four-language
      captions and the dubs; every gate is the owner's.

## How to verify

```bash
for s in curio-u02-v2 curio-l08-v2 curio-h02-v2 curio-h03-v2; do node tools/video/cli.mjs lint --slug $s; done
node tools/video/cli.mjs narrative --slug curio-h02-v2   # the panel, for a blind reader
```

## What the blind panel found, round by round

The writer of each script answered the ten questions itself and passed itself. An independent
reader that saw only the narration text then failed every single one of the five, including the H01
rewrite that had already been shown to the owner as the proof. A writer marking its own work is not
evidence; this is the finding to keep.

Every first independent read failed the same question, `no_recap`, in the same place: the close
re-told the body. Three rounds of rewriting went into that one question across the five scripts.

The readers also found three faults in the rules themselves, each of which is now fixed in
`script-writing.md`, `register.mjs` and the panel's own question text:

- Question 4 forbade announcing what was coming while question 6 asked for a forward hook that says
  so. Two readers stopped mid-answer to say the rubric contradicted itself. Both were right.
- Nothing said that a payoff owes the listener something new, so writers named a hook and then
  re-read the line that planted it.
- Nothing said that a named callback needs distance, so chapters opened with 「還記得…嗎」 about
  something said four seconds earlier.
- The close's 「用數字回答」 is impossible for a file stamped 未結, and the last chapter's 45 to 60
  seconds was being read as a floor to pad rather than a budget.

Two readers, independently, also said the explicit 「等一下它會回來」 was scaffolding the withheld
fact did not need. That is now one per episode.

## Notes

- A rewrite never reuses the delivered slug: new slug, old project stopped in the backend. That is
  the owner's rule of 2026-10-11, because an approved outline, final cut and publish gate stay
  bound to the old content.
- H02's fact check refuses four things the popular version says: the colonist count (the sources
  run from about 100 to about 150), 「樹上刻著 CROATOAN」 (the full word was on a palisade post, the
  tree had CRO), 「主流看法」 for the Croatoan merger (the park service calls it one of the most
  popular, not settled), and the 2026 inland announcement (the foundation's own page, no report, no
  third-party assessment yet).
- H03's refuses 「八千萬棵樹」 as a count: a 2025 paper traces it to a 1933 estimate over an area
  overstated about fourfold. The body, the energy, the burst height, Lake Cheko and whether anyone
  died are all unsettled, so the file closes 未結.
- L08 is the one that already linked its chapters reasonably; keep what works there.
- No media, no uploads and no spending in this task. Scripts only.
