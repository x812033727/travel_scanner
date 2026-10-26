---
id: 2026-10-26-curio-s31-new-rules
title: Complete Curio S31 under the October 25 story rules
status: in-progress
priority: P1
area: docs
owner: codex-curio-s31-f29b
claimed_at: 2026-10-26T14:14:29Z
created_at: 2026-10-26T14:14:25Z
completed_at:
branch: codex/curio-s31-new-rules-20261026
depends_on: []
scope:
  - docs/videos/curio-s31-v2
---

# Complete Curio S31 under the October 25 story rules

## Why

Owner 2026-10-26 requested continuation of「楊貴妃的荔枝，怎麼送到長安？｜奇聞檔案局」curio-s31 under the latest rules. The existing cut and eight-language work belong to PR #1800 (`claude/suspicious-antonelli-878480`), so this task isolates the 2026-10-25 specification in `curio-s31-v2` and retains the original media, approvals and translations.

## Definition of done

- [x] Revised, independently reviewed Chinese script targets 13 minutes with a source-bound claim map, five-step opening, conversational delivery, 45-second hooks, burned-in Chinese captions and bold thumbnail.
- [x] Preserve existing paid illustrations/music where valid and quote all incremental production before incurring new charges.
- [ ] After owner approval, generate and review the Chinese narration/storyboard, assemble with channel intro and v4 end screen, verify actual duration and QA, and submit the final cut.
- [ ] Refresh selected translations, CC and dubs against the revised script, then prepare the upload package; publication remains owner controlled.

## Steps

- [x] Check branches, open PRs and actual local/host artifacts before modifying anything.
- [x] Read current curio, script-writing and production rules; isolate new scope from PR #1800.
- [x] Rewrite from the existing 52-row source check and independently verify new wording.
- [x] Run lint and two fresh narrative readers; prepare media reuse and incremental budget receipts.
- [x] Obtain the one episode-wide script/production decision.
- [ ] Synthesize and verify narration, recover/reconcile original illustrations, draw remaining shots within the cap, then assemble, verify and deliver the full selected-language package.

## How to verify

`node tools/video/cli.mjs lint --slug curio-s31-v2`; fresh `narrative --slug curio-s31-v2` readers; `npm run check:tasks`. Paid steps require approved episode-wide scope. Actual timeline and assembled media, not planned seconds, establish runtime.

## Notes

- Live host 2026-10-26: `/var/lib/mokaair/video-work/curio-s31` lacks current timeline/keyframes; this is not the active local workdir.
- Local existing media: `C:/Users/x8120/mokaair-work/videos/curio-s31/final.mp4` (182,401,881 bytes), QA receipt says 19,421 frames, SHA-256 `64896215da89ee6f978d3d9e0b41600eacf9b3c21827a1462a955429637343af`. Six dub files exist (en/es/id/ja/ko/pt), vi has a partial directory, th has no track. This is the old specification and is not v2 completion.
- Original audio/storyboard approvals are dated 2026-10-24 and belong to the original media hashes. Never copy them as v2 approval.
- Original source is about 2,307 Chinese characters, target [9,11], burn_in=false, four opening previews. New rules: 13 minutes, approximately 3,500 characters at 4.5/s, opening stakes/scene/max-two-previews/promise/question, every chapter addresses viewer and has narrator reaction, burn_in=true, bold thumbnail.
- Same source chronology and unresolved evidence boundaries remain: relay documented; origin, exact days and freshness unresolved. The ten-station decree concerns exiled officials, not a lychee delivery manifest.
- Final r6: 212 lines, 3,206 Han units, 150 scenes / 129 shots (66 original + 63 new), 24 loops. Source audit 212/212 PASS; speechHash `8af0af8b6fb7d1e4`. Lint 0 errors / 0 warnings. Final readers K=13/13, L=11/13; official two-reader merge=13/13, exact evidence in `narrative-review.json` and all six rounds in `narrative-rounds.json`.
- 2026-10-26 owner directly approved revised script plus US$6 image/judge cap, then instructed「用你推薦的選擇就好 不用問我」and「做完後陸續做s15 s12 s16 s19 s20 s21」. Exact continuation policy and ordered queue are in `batch-queue.md`; this delegates routine QA choices, not claims that the owner personally watched/listened or permission to publish on YouTube.
- New outline/script approvals recorded against the actual new files with the owner's direct words. No old approvals copied. TTS session `84228` completed; private log `~/mokaair-work/curio-s31-v2-preflight/tts-production-r6.txt`.
- Current workdir: `~/mokaair-work/videos/curio-s31-v2/`; verified original cache provenance is in `recovery/source-media.json`. Selected original images 68/68 hash verified, 87 valid completed cache entries copied, one stale historical cache entry excluded; original source files untouched.
- Final dry-run: TTS 171 requests / 4,270 billable characters, Sulafat ready; images 129 shots at image-01 1K, full worst-case three takes US$5.22 before cache deduction. Existing bed reused. Do not exceed the owner US$6 image/judge limit even though the server's general per-video cap is US$200.
- `test:docs-videos`: 235/236 passed, one pre-existing Windows native child-process crash under system Node 24.13.0 (3221226505). The same isolated test passed 1/1 under documented bundled Node 24.19.0. Full suite was not reported green. `check:tasks` passed with existing stale/overlap warnings.
- Continuation heartbeat created in this chat, automation id `s31`, every 20 minutes, quiet on unchanged/non-actionable state. It reads this task and `batch-queue.md`, resumes after the active command ends, preserves paid journals/locks, processes the seven episodes sequentially and disables itself when verified delivery packages are complete.
- Draft PR #1874: https://github.com/x812033727/travel_scanner/pull/1874 (`no-auto-merge` applied at creation); production evidence remains in progress. Subsequent six-episode read-only inventory is in `next-episodes-inventory.md`. S15/S12 require remote media recovery before any repaint; their approved review attachments still exist.
- Latest continuation: TTS completed with 171 synthesized requests, 4,430 billable characters, 0 reused; narration 28,379 frames / 30fps = 15:45.967. Per-line WAV sum is 773.440s (12:53.440), about 4.15 Han units/s including each clip's internal pauses; total timeline adds 169.4s configured gaps plus 3.127s grid padding. Keep the verified speech; no need to buy another narration to meet the target rate. There is no series maximum runtime.
- `check-audio` session `73612` finished: 212 checked, 31 flags, no premature approval. Original WAV hashes bind the offline second opinion; see `batch-queue.md` for live process/recovery details.
- All eight 212-line worksheets translated and independently reviewed; concrete corrections applied and merged. Delta readback is ongoing. Timed dub fit uses full slide-state windows; initial per-line max_chars exceptions must be explicit and tested against actual speech, never silently remove names, dates or claims.
- Keyframes session `91825` stopped on HTTP502 after v2-add-037 image was already cached; preserve it for judgement without regeneration. Existing 65 old verdicts retained. Exhausted consort-basket prompt simplified after producer stopped; speech/narrative/script-check bindings verified unchanged. Early orphan cache/pending state is now reconciled offline using the existing exact image and fresh read-only server receipt; ledger remains US$0.4895. Failed judge-response fees have an additional US$0.05 accounting contingency, conservative total US$0.5395.
- Preview render completed: 21 cards, 212 subtitle strips, nine thumbnails, no layout errors. All nine thumbnails and card contact sheet inspected; final film/audio/storyboard gates remain pending. Private downloader credential-file collision fixed, recovered image SHA verified, but official local video-tool login must be allowed again in the admin pairing flow. Until pairing restores the token, do not submit paid requests; all other offline preparations have been saved.
