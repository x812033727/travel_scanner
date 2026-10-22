---
id: 2026-10-22-draft-c11-ucc-story-script-and
title: Draft C11 UCC story script and visual plan
status: done
priority: P2
area: docs
owner: codex-c11-ucc-script
claimed_at: 2026-10-22T14:26:20Z
created_at: 2026-10-22T14:26:13Z
completed_at: 2026-10-22T14:40:22Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/script.md
  - docs/videos/story-everyday-ucc-c11/visual-plan.md
  - docs/videos/story-everyday-ucc-c11/visual-plan.json
  - docs/videos/story-everyday-ucc-c11/script-source-notes.md
---

# Draft C11 UCC story script and visual plan

## Why

The owner adopted the SHA-bound C11 Treatment. It needs a complete narration and one-to-one visual plan before an independent line-by-line source review, two cold reads, script approval, and any paid media decision. The core story separates three barriers: a returnable bottle, a stable milk-coffee can that stores and travels, and a can that opens without a separate tool.

## Definition of done

- [x] Six-chapter Chinese narration has stable line IDs and per-line source attribution.
- [x] A one-to-one visual plan targets cute-mystery illustrations, with no logos, readable words, real portraits, or false period reenactments.
- [x] Script-source notes preserve Mira 1965 versus the UCC museum's narrower milk-coffee claim, and distinguish company retrospective from audited sales.
- [x] Draft PR stays unmerged with no-auto-merge; next gates are recorded without claiming TTS duration or paid production.

## Steps

- [x] Write narration from approved Treatment and reopened primary pages.
- [x] Map every narration ID to a distinct image or brief postproduction card.
- [x] Run structural checks and record exact SHA-256 values.

## How to verify

Check ID order and 1:1 mapping with a local script; count shot/card balance and consecutive cards; `npm run check:tasks`, `npm run test:docs-videos`, and `git diff --check`.

## Notes

- Treatment SHA-256 `C53FC5E995DA9B245C892E9B5F0DA9AF10DC8D949FC398948F6E3C9FACF5A43D`; matrix SHA-256 `931F3B19791740CDFFEFD665C284C4AF0F7B1E2228C2911687B16D68F1483E8B`. Owner adopted this version; neither file is in this task scope.
- Reopened UCC 2026 and 2025 retrospective pages, UCC museum and company history, Hamada municipal and Shimane prefectural pages. UCC is the source for the railway anecdote and Expo effect; they are not contemporaneous records. Hamada's newer page at `https://www.city.hamada.shimane.jp/www/contents/1445997212239/index.html` explicitly records Mira's September 14, 1965 sale, while the adopted matrix's older H1 page also recounts it.
- No paid TTS, images, music, import, upload, or release authorized for C11.
- Draft structure: 83/83 IDs in matching order; 70 shot / 13 stats; longest stats run 2; zero brand/product/real-person names in image prompts; body chapters 2–6 have 75 lines and 2,076 characters. This is not actual duration evidence. Intro 5s after c110108; v4 outro 21s after c110615.
- `npm run check:tasks` PASS, 2,098 task files (unrelated stale/overlap warnings). `git diff --check` PASS. Fresh worktree initially lacked npm dependencies, so first docs-video test run had 6 `pinyin-pro` module failures. After `npm ci --no-audit --no-fund`, `npm run test:docs-videos` ran 236 tests: 235 PASS, 1 pre-existing Windows portable-runtime process exit `3221226505` in `docs/videos/imported-long-languages/runner.test.mjs:679`; not in C11 scope. Do not mark the suite fully passing.
- The complete script still needs a separate agent to verify every line against direct sources, two fresh narration-only readers and visual preflight, then owner script/visual approval. Paid TTS duration >=480s is unproven, as is actual illustrated-time share >=70%.
- `tasks done` wrote this `done` record but Windows left the original same-ID file under `tasks/open/`. I verified both absolute paths inside this worktree and this record's `status: done`, then one exact `Remove-Item -LiteralPath` was rejected by automatic approval review as `blocked by policy`. I did not retry through another route. The open duplicate remains **untracked locally only** and must not be committed; the PR includes this done record. Local `check:tasks` will see a duplicate until the exact open copy can be removed through an allowed route.
