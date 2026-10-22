---
id: 2026-10-22-renew-long-form-duration-review-music
title: Renew independent long-form duration review after music guard changes
status: blocked
priority: P1
area: tools
owner: codex-gpt6-duration-independent-review
claimed_at: 2026-10-22T03:40:46Z
created_at: 2026-10-22T03:38:44Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Renew independent long-form duration review after music guard changes

## Why

PR #1669 threads a measured generated-music duration into assembly and changes
the music test fixture. Those edits change two files bound by the independent
long-form duration receipt. Its review gate correctly fails until another
reviewer checks the new bytes and renews the SHA-bound report and receipt.

## Definition of done

- [ ] An independent reviewer confirms the 480-second unwrapped body guard is
      unchanged and records the actual compatibility increment in review.md.
- [ ] review.json binds the current exact files and report; both shipped review
      tests and the long-form `check` command pass.

## Steps

- [x] Read-only audit of the two changed bound files and CI failures.
- [ ] Resolve or release overlapping board ownership without forced claim.
- [ ] Claim this ticket, write the independent review increment, and test it.

## How to verify

`node --test tools/video/long-form/review.test.mjs` and
`node tools/video/long-form/cli.mjs check` must both pass. Compare the two
reviewed file hashes with the receipt and report table.

## Notes

2026-10-22 independent read-only audit: `tools/video/assemble/cli.mjs` still
calls `animeBodyDurationProblems` before media inputs, and its only changed
duration path passes the current `timeline.total_frames / FPS` to
`musicInputs`. `tools/video/media/clips.test.mjs` changes a fake MP3 fixture to
a real one and tests short-track hold, cache reuse, corrupt-file refusal and
paid-ledger retention. No edit in either file relaxes the 480-second body rule.
At this revision their SHA-256 values are respectively
`b0826429abaeb5572586c5dff0294f6081378d6246fe473057e959d65950c18c`
and `be0b8a4e0c4b905ca059a29e92c131811512f64b5b2d2cd46a55637670c2bb69`.

The 2026-10-22 Linux `smoke` and `video-tests` jobs each failed only two
tests: the expected stale duration review binding for those files, and a new
2-second MP3 fixture whose full decode measured 1.986372 seconds against an
overly narrow >=1.99 assertion. The music-test author separately corrected
the cross-platform test tolerance in commit `319515565`; this reviewer did not
author that code.

Board `claim` refused this ticket because its review-file scope overlaps
`2026-10-09-duration-review-stalled-fixes-rebase` (status review),
`2026-10-19-imported-video-languages-eight` (in-progress), and
`2026-10-19-worker-video-languages-five` (status review). The first and third
branches have merged PRs #1387 and #1614; the imported-languages branch has
no PR under its recorded head. Their task claims remain open, so this ticket
is blocked and the protected review files were not edited or rebound.
