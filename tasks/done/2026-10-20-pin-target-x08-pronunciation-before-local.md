---
id: 2026-10-20-pin-target-x08-pronunciation-before-local
title: Pin Target X08 pronunciation before local media
status: done
priority: P1
area: docs
owner: codex-x08-media
claimed_at: 2026-10-20T18:00:33Z
created_at: 2026-10-20T18:00:30Z
completed_at: 2026-10-20T18:02:44Z
branch: codex/brand-story-target-x08
depends_on: []
scope:
  - docs/videos/story-everyday-target-x08/story-lexicon
  - docs/videos/story-everyday-target-x08/reviews/lexicon-bootstrap.json
  - tasks/open/2026-10-20-pin-target-x08-pronunciation-before-local.md
---

# Pin Target X08 pronunciation before local media

## Why

X08 Target Canada has a reviewed manually composed `video.json`, but no pinned story pronunciation snapshot. The paid TTS guard correctly returns `STORY_LEXICON_MIGRATION_REQUIRED`: normal genesis refuses an existing script, while the old-chapter migration requires a genuine worker chapter directory that X08 never had. A reviewed manual bootstrap pins the shared dictionary and X08 `series.json` names before any speech, without inventing worker history or changing the frozen narration and Shorts.

## Definition of done

- [x] An independently reviewed immutable X08 story lexicon snapshot matches the exact reviewed `video.json`, `series.json`, shared dictionary and three source/narrative evidence files.
- [x] The transaction has a committed work-volume receipt, strict read-back succeeds, and paired TTS dry-run lists requests without media charges. No audio, timeline, approvals, paid media or published URL is claimed by this task.

## Steps

- [x] Confirm frozen script, series, shared lexicon and independent evidence SHA-256 values; prove no prior X08 snapshot, work directory, STOP, audio, timeline, approvals, or pending transaction.
- [x] Build the pure genesis plan from reviewed `series.json` names and compare its version/event hashes with independent root calculation.
- [x] Prepare the exact manual-bootstrap review receipt, then obtain independent `/root` sign-off before any publication.
- [x] Run the tested manual-bootstrap dry-run against this repo root and `/workspace/.brand-video-workdir`; require all checks `allowed` with unchanged hashes and helper bytes.
- [x] Apply the single transaction, verify strict read-back and zero-charge TTS dry-run; commit/push the reviewed receipt, lexicon artifacts and task to draft PR #1625.

## How to verify

Use the tested standalone helper in `/workspace/travel_scanner_netflix/tools/video/lexicon-manual-bootstrap.mjs` through `runManualBootstrapCli(args, { root: '/workspace/travel_scanner_target_x08' })`; the X08 `--workdir` media base is `/workspace/.brand-video-workdir`. Verify strict `readStoryLexicon` returns `mode: snapshot`, sequence 1 and the planned SHA values. Then run paired `tts --slug story-everyday-target-x08 --dry-run --workdir /workspace/.brand-video-workdir`; confirm only request list, no files under `audio/`, no timeline and no paid ledger. Run `node tools/video/cli.mjs lint --file docs/videos/story-everyday-target-x08/video.json --json`, `npm run check:tasks`, `git diff --check`.

## Notes

- Frozen `video.json` SHA-256 `a6ffe45d1944839e0ae35c9e8418e340dacef578e7faa5304219b80fe4118bb4`; `series.json` `c154166429738fed3a3aa8796cefa7e6729c9f6d45c3b23a815fef5bdd84c7d4`; shared `docs/videos/lexicon.json` `95abdb67972cac70fe7c16b51faf4d94fe671e55aba9a1c3114fddb5a6cc613a`.
- Independent exact-SHA evidence: `reviews/source-audit-v5.md` `74fb8dc1b1990b9f92e4a2c3abc75e169a64f133e95a030a2cf60b4faf3febda`, `reviews/blind-a-v5.md` `34a4be846b65d37e9ae8d958e533ad2d547d7bfd976925be881706f53add3e4e`, `reviews/blind-b-v5.md` `51846c6198fe56ae95ec10431e1ddd77b0072ae62831b1654cb1c16b9884d1a1`.
- Pure `genesisBytes` + `planInitialStoryLexicon` seeds `Target`, `Canada`, `Zellers`, `Brian`, `Cornell` as null terms from names `Target`, `Target Canada`, `Zellers`, `Brian Cornell`, `Cornell`; planned lexicon SHA-256 `ec1cafa975b5bd7a4085862ec1a7b6759206859f6a8948f58f89aafc6cca41b3`, initial event `27747301c1733a88a2402957beb36ecd6d59e6c2cf90e603119f25fa5e5e64ae`.
- The X03-tested helper is not in X08's base branch; call it from the Netflix worktree with an explicit X08 root. Its standalone CLI SHA-256 is `d554b53c538a6039662385e08580d17c59a9e82081c933238ac2196b8e6acd18`, paired core helper `05580631571ec62adf58d3d93f241ba7e73b1009cd202d4556f0a25b313826bd`, and `lexicon-migration.mjs` `c9bf13dce7611c24bf308636fb7e27ad04477ad28194c30a8a3828923926c0fb`. Recheck before apply; do not copy or hand-roll the transaction.
- At 2026-10-20 18:00 UTC, `docs/videos/story-everyday-target-x08/story-lexicon/` and `/workspace/.brand-video-workdir/story-everyday-target-x08/` did not exist. Therefore there were no X08 `auto.json`, chapter files, `audio/`, `narration.wav`, `timeline.json`, `approvals.json`, media ledger or lexicon work intents. There was no global or project `STOP`. The media base and repository were real directories, not symlinks; media base is outside the repository. The generic migration dry-run refused `STORY_LEXICON_MIGRATION_WORKDIR_UNPROVEN`, as expected; it was read-only.
- X08 preproduction was completed in draft PR #1625 and its prior ticket moved to `tasks/done/` per task-board guidance before this new scoped claim. This bootstrap must not alter source-frozen `video.json` or `shorts.json`. Official branding files and Studio links remain later gates.
- `/root` independently approved the exact candidate receipt SHA-256 `7e8074abf40dedc712a19341922a81e1896a445db39fa16e773ce7b093ff1f0e` after rechecking the video, series, shared lexicon, three evidence hashes, empty workdir and genesis plan. The approved bytes were copied unchanged into `reviews/lexicon-bootstrap.json`. The tested X03 helper dry-run returned `allowed` for all seven checks and the exact expected SHAs; it created no work directory. The helper's 12 focused tests passed before publication.
- The single transaction committed as ID `8370ba59-c910-49b4-be6f-f552f200da49`; immutable manual-provenance sidecar SHA-256 `11d17ef80ccb5bfda81ea376300f1e5f5fecaa0d5a937e2e70ef78bf66a1e419`, work receipt SHA-256 `449c30e2293ccf31aa3c09ca9bea275f3b0437362e68e6fe46906101ce171ee8`. Strict reader returned `snapshot`, sequence 1, version `ec1cafa9…`, event `27747301…`, with the five expected null terms. `pending.json` and all work-intent files are absent (the empty intent directory remains).
- Paired `tts --dry-run` with `NODE_USE_ENV_PROXY=1` and secure home `/workspace/.video-tool-home` returned **130 requests, 2,602 billable characters**, voice `gemini:Sulafat` ready, 8,563,008 Gemini characters remaining this month; it did not synthesize or charge. Post-check: no X08 `audio/`, `narration.wav`, `timeline.json`, `approvals.json`, media ledger or worker `auto.json`; original main video and Shorts SHA-256 values remain unchanged. Real TTS and the all-in US$25 budget gate are later work.
