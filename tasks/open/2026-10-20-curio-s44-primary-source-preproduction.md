---
id: 2026-10-20-curio-s44-primary-source-preproduction
title: Curio S44 primary source history episode preproduction
status: in-progress
priority: P2
area: docs
owner: codex-s44-source
claimed_at: 2026-10-20T09:24:41Z
created_at: 2026-10-20T09:24:37Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s44
---

# Curio S44 Broad Street pump and cholera source preproduction

## Why

John Snow's 1855 firsthand account says the Broad Street pump handle was removed on 8 September 1854, while new fatal attacks were already falling. The usual one-action cure story therefore needs a source-bound correction. Build an 8–10 minute single-investigation history episode that follows his questions, records, exceptional households and cautious conclusion. Only this ticket and `docs/videos/curio-s44` are in scope; S41/S43 and shared topic-bank files belong to other workers.

## Definition of done

- [x] Independently checked, fixed 1855 source text and A/B site-readable outline; source boundaries distinguish observation from inference. Scene-level claims wait for the owner's outline choice.
- [ ] One 8-minute-plus narration body with 30–60 second condensed opening, installed-branding plan, at least 70% illustration shots, source/channel links and a one-Short draft.
- [ ] Two independent exact-script blind reads and an independent full source/visual review; local lint and tests pass; scope-only commit and push.
- [ ] Hand off the **outline** to the manual site gate. Script site gate and paid TTS/art/music wait for the owner's outline choice and script approval.

## Steps

- [x] Search S01–S43 and H/M/P/U/L topic bank for the same Snow/Broad Street story; create and claim S44 scope.
- [x] Reopen and independently verify pinned GITenberg transcription and map image; record exact line ranges and evidentiary limits.
- [x] Draft parser-ready A/B brief and submit the outline to manual review; **pending owner**.
- [ ] After owner choice, draft scene-by-scene claims, script and shot plan; run local checks.
- [ ] Freeze exact hashes for two source-isolated narrative readers and separate source/visual reader, then record receipts.
- [x] Submit outline through supported manual site gate; Jev recommends A, owner choice pending.
- [x] Push only S44 files and this task file (`21fe9dd475927f552747188a646c0a18fbe49cf5`).

## How to verify

Compare pinned source SHA-256 to `research.md`; reopen every linked line range. Run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s44`, the narrative check, `npm run test:docs-videos` and `npm run check:tasks`. Use site report-only preflight before manual outline push; `pending owner` is not approval.

## Notes

2026-10-20: Independent new task claim `codex-s44-source`. Initial dedup search found only incidental cholera in S26, no Snow or Broad Street episode. Proposed title question: 「1854 年醫生拆掉水泵把手，真的立刻止住霍亂？」 Fixed source is John Snow, *On the Mode of Communication of Cholera*, enlarged second edition (1855), GITenberg commit `6a27453cc0bb85c3fc125c5e13900c8f3a8b48db`, raw `72894-0.txt` SHA-256 `3f3e71972f603e5fa50a0e71045afffa994ae38a86a8912dda3e90c8babb37af`. Snow's own attack table and text at lines 1655–1767 say attacks had fallen before the handle was removed and he could not decide if the well still carried active cholera; preliminary chapter at 1344–1545 supplies his field investigation. Site/paid media not started.

2026-10-20 outline handoff: Two independent read-only scouts re-fetched the exact Snow text; one also checked the 1855 printed map image and the other checked S01–S43 plus H/M/P/U/L bank for overlap. They corroborated the hard boundaries: Snow's first edition was 1849, the later map includes deaths through 30 September, the 616-case table counts **fatal attacks** with partly inferred onset, the 8 September handle removal followed a descending curve, and Snow could not prove its instantaneous effect or the contamination route. Exact citations are in `docs/videos/curio-s44/research.md`. Brief parser finds complete A/B; `review-push --report-only` succeeded, `--gate outline` returned Jev A 1.00 but **pending owner**, and `review-pull` returned `waiting for the owner` (exit 3). Bound brief SHA `44f332d8c1a4d50550c4ba17927964523ed0a7a2fc0a2ebf5227fba898ff63de`; details in `docs/videos/curio-s44/verify-site-gates.md`. A local R0 scene draft was moved to `/tmp/s44-preoutline-draft-20261020/` and was deliberately not committed: lint found unresolved names and cadence warnings, and no narrative or full source/visual check exists. Do not use it for site script or media. Next action after the owner picks A or B: write and fully audit that exact script, then submit manual script gate. No paid media or media assets for S44.

2026-10-20: Source/outline/site receipt scoped commit `21fe9dd475927f552747188a646c0a18fbe49cf5` is on the shared remote branch. A concurrent worker's push returned a ref-lock race to this worker, but `git ls-remote` then read back this exact SHA from the remote. No S41/S43 files were staged in this commit.
