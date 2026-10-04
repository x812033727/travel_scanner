---
id: 2026-10-04-ai-term-large-language-model
title: AI terms: produce the large language model explainer
status: in-progress
priority: P2
area: docs
owner: codex-ai-series-continuation
claimed_at: 2026-10-04T10:23:54Z
created_at: 2026-10-04T10:23:14Z
completed_at:
branch: codex/ai-series-continuation-20261004
depends_on: []
scope:
  - docs/videos/ai-term-large-language-model
---

# AI terms: produce the large language model explainer

## Why

The owner requested ongoing AI-series production and verified G-drive backup before removing completed local media. The existing 81-term backlog lists `large-language-model` at tier 1 / order 3, without an existing video. The pilot episodes and engineering overview have active production processes; this episode has a separate, unoccupied source scope.

## Definition of done

- [x] A source-checked, independently reviewed LLM episode answers what a language model does, where its answer comes from, and when to use records or tools.
- [ ] The current narration and completed video each contain at least eight minutes of substantive content; audio, storyboard, final, captions and upload-package checks pass without fabricated approvals.
- [ ] Backend delivery is read back with the actual media hashes and selected languages complete.
- [ ] Completed media is archived to a new G-drive batch, cloud synchronization and restore integrity are verified, and only eligible, unused local media is removed with a journal.

## Steps

- [x] Check worktrees, remote branches, open PRs, source backlog and local production processes.
- [x] Claim a narrow source scope and create a thread heartbeat for continued work.
- [x] Write the brief, complete narration/storyboard source, claims and reproducible fictional-record demonstration.
- [x] Obtain independent fact and listener review, resolve changes and pass lint.
- [x] Submit the outline through the existing Jev policy; read its hash-bound decision back.
- [ ] Preflight existing TTS/media budgets and continue production within those limits.
- [ ] Complete media QA and backend delivery, then selected languages.
- [ ] Archive and verify new completed media before eligible local cleanup.

## How to verify

`node tools/video/cli.mjs lint --slug ai-term-large-language-model`

`python docs/videos/ai-term-large-language-model/demo.py`

`node tools/video/cli.mjs status --slug ai-term-large-language-model`

Continue the standard `youtube-video` gates with the existing paired local tool. Compare backend attachment SHA-256 against the current upload package. Use the private archive runbook/helper in `C:/Users/x8120/mokaair-work/ai-series-continuation-20261004`; a DriveFS cloud ID, correct size and MD5, no pending operations, ZIP integrity, source hashes, protected/shared dependencies and active-process checks are prerequisites for deletion.

## Notes

- 2026-10-04: Human authorization is ongoing video production and backup-then-delete of completed local media. It does not authorize YouTube publication, enabling the deliberately disabled uploader, increasing budgets, owner approvals, merge or deployment.
- Thread heartbeat `ai-g` is ACTIVE every 30 minutes on chat `01a1066c-b865-7c03-b19e-b5fb32607794`; notify only for a new completed video, verified archive/cleanup, real failure or necessary owner decision.
- Current backend GET confirmed `auto_pick_outline=true`, an eight-minute minimum, and channel stance points 4 (check cited sources), 6 (only call real tests tests; mark illustrations) and 7 (one practical next action). Apply those points to this episode. No settings changed.
- Local active jobs included context-window/RAG keyframes and engineering-overview assembly. Preserve their outputs and avoid duplicate work. The shared terms registry and lexicon remain owned by the pilot task and are outside this scope.
- G is a Google Drive mount with approximately 27.8 GiB available at preflight. Use `G:/我的雲端硬碟/Backup/Mokaair/ai-series-continuation-20261004/<fresh timestamp>` for a new batch. Historical `delivered-20261003-2010` helpers hard-code their own roots and cannot be rerun for this batch.
- No newly inspected local AI episode was eligible for cleanup: incomplete production, outstanding selected-language decisions, failed/pending QA or active jobs must be preserved. No source media has been deleted in this run.
- Source freeze: video SHA-256 `f18c6c619c2e9928c34593f921a63f33e679ce92a0005b70f217c97b3a511a83`, brief SHA-256 `b23f074132fe526115f9908c49d430881f028272b0b064375d64376c3f7c8ca9`. There are 108 scenes, 75 original illustration prompts and 138 narration lines. `verify-1.md` independently covers all narration, visuals, metadata, demo and both Shorts; 36 claims plus ten supplementary checks have no unresolved facts. Lint has zero errors and zero warnings. Estimate 13.84 minutes is not measured media.
- `review-push --gate outline` selected A under the existing Jev policy and the backend automatically approved it. `review-pull` recorded the exact brief hash at `2026-10-04T10:50:23.673Z`; no owner approval was invented.
- Final TTS dry-run: 108 scene requests, 3,677 billable characters, Sulafat ready, 9,876,279 characters remaining in the existing monthly allowance. Actual `tts` is running with log `C:/Users/x8120/mokaair-work/ai-series-continuation-20261004/llm-tts.log`. Recheck live processes and this log before resuming; do not run a duplicate paid job. After synthesis, measure current body duration, every chapter (including the short cold open), card states and illustration proportion before later gates.
- Private backup helper `archive_candidates.py` SHA-256 `66dd2df61daa6daefa4795b4afc6fc902b1b6c597c497d2f1f005dddadc2155e` has 28 passing fake-media/restore/refusal tests and one Windows symlink-permission skip. `VALIDATION.json` records the read-only live process and DriveFS probes. This validates the helper's tested behavior; no real completed media was copied or deleted. Follow `RUN.md` and `BACKUP-RUNBOOK.md` for fresh evidence before any deletion.
