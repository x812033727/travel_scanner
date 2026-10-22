---
id: 2026-10-22-polish-c11-ucc-spoken-flow-after
title: Polish C11 UCC spoken flow after blind reads
status: done
priority: P2
area: docs
owner: codex-c11-ucc-script
claimed_at: 2026-10-22T15:15:12Z
created_at: 2026-10-22T15:14:54Z
completed_at: 2026-10-22T15:22:26Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/script.md
  - docs/videos/story-everyday-ucc-c11/script-source-notes.md
  - docs/videos/story-everyday-ucc-c11/visual-plan.json
  - docs/videos/story-everyday-ucc-c11/visual-plan.md
---

# Polish C11 UCC spoken flow after blind reads

## Why

The C11 UCC script passed an independent 83/83 source review and two genuinely narration-only blind reads at script SHA `BF58A5C51F248806D56CBF37705737B1DAA7FEB4F7B43593CC702426E6D0C887`. Both readers independently heard repetition around the milk-coffee development, the can lining, and Expo, plus a slow Mira callback after the 1981 pull-tab payoff. Polish spoken flow before owner review without moving factual boundaries.

## Definition of done

- [x] Preserve all 83 ordered line IDs, six chapters, the Mira-versus-UCC-milk distinction, the 1969 two-hole opening and 1981 pull tab.
- [x] Replace narrator-facing fact-check/editing language and repeated explanation with source-supported spoken lines; pair changed lines to accurate visual rows.
- [x] Bind a fresh script/visual SHA; identify exact changed IDs and historical receipt limits for independent recheck and new blind reads.

## Steps

- [x] Read both blind-reader receipts and official UCC/Hamada pages relevant to the edits.
- [x] Edit only this episode's script, visual plan, and author source notes.
- [x] Run focused structural and text checks; commit/push to draft PR #1691 without paid production or merge.

## How to verify

`git diff --check`; parse `visual-plan.json` and compare its ordered `line_id` list to the script's table IDs; inspect changed-line IDs against the base commit; verify visual-plan.md/JSON pairing and shot/card counts; inspect the PR head and draft/no-auto-merge fields after push. Independent source and narration decisions belong to separate reviewers.

## Notes

Claim required `--force` only because this branch still contains untracked `tasks/open` copies of the author's two earlier **done** C11 tasks. Their tracked `tasks/done` copies are committed, both old owners are this same author, and no other active scope was overridden. An earlier exact deletion of an orphan open copy was auto-review rejected `blocked by policy`; do not bypass that denial. Old source and blind receipts remain historical after this script SHA changes.

Current author draft: script SHA-256 `C24907438D46BF2607CCC559D3A950D969E9F347538A2A37827F469CDDF2E3BC`; visual JSON SHA-256 `AF25C403FD1C4D0F9CB08CC78BFB3114761E6BAFA861B246ABF81D952FF491F9`; readable visual table SHA-256 `BED98CB29CA19148D58C84A3245501D71A626787736885AF8CB7E90340B38D84`; author source notes SHA-256 `F6C0DD148F1A93739DAE2BBDC2AE53CBA313A5CE281C2FBFFA7CD395ED9071DE`. Exact changed narration IDs: `c110304, c110306, c110307, c110309, c110310, c110311, c110312, c110407, c110408, c110409, c110511, c110512, c110514, c110610, c110611, c110612, c110613`. Visual rows changed: `c110304, c110311, c110512, c110612, c110613`. U2 directly supports `c110512`'s company-attributed summer demand and production claim; no numeric production or growth amount was added.

Focused checks: `git diff --check` PASS (Git warned about working-tree CRLF normalization in the readable table); parsed script/JSON/readable table as 83 unique, ordered, exactly matched IDs and content; 70 shots, 13 postproduction cards, max 2 consecutive cards, 0 forbidden brand/person names in image prompts; 75 body rows/1,968 characters including punctuation, **not** measured audio. `npm run check:tasks` FAILS locally because five previously completed C11 task files persist as untracked open duplicates after interrupted `done` moves, including two from other reviewers. Their tracked done copies are in this PR. Do not bypass the previous policy denial to remove them. A clean checkout of committed files is needed for CI interpretation.
