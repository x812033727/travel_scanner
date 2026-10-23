---
id: 2026-10-23-import-owner-approved-c19-script-card
title: Import owner-approved C19 script card
status: done
priority: P1
area: tools
owner: codex-c-series-integration
claimed_at: 2026-10-23T18:12:23Z
created_at: 2026-10-23T18:12:11Z
completed_at: 2026-10-23T18:19:20Z
branch: codex/c19-narrative-v6-20261024
depends_on: []
scope:
  - tools/video/review/script-intake.mjs
  - tools/video/review/script-intake.test.mjs
  - docs/videos/brand-stories-everyday-reversals-20261020/approved-scripts.json
---

# Import owner-approved C19 script card

## Why

The backend already has the C19 episode plan, but the approved script intake
manifest still names only ten earlier scripts. C19 needs an exact-source,
owner-approved pending review card so the backend can show its real
preproduction state without mistaking a script for a finished video.

## Definition of done

- [x] The local intake dry run recognizes C19's exact approved 79-line script.
- [x] A changed C19 script hash fails before any backend request.
- [x] The backend has one pending C19 script card for the approved hash, verified by readback.
- [x] The episode remains planned and the finished-video count remains zero after import;
      the separate preproduction-progress UI ticket will display the new script card.

## Steps

- [x] Add C19 and PR #1795 approval provenance to the fixed manifest.
- [x] Extend the strict intake ID set and local tests to 11 approved scripts.
- [x] Apply the one-episode import against the paused series and inspect the resulting card.

## How to verify

Local: `node --test tools/video/review/script-intake.test.mjs` and
`node tools/video/review/script-intake.mjs --id C19`.

With authenticated backend access: run the same command with `--id C19 --apply`,
then read back `/api/video/reviews/story-everyday-seven-bank-c19`
and verify a pending `script` gate card with the exact source hash.

## Notes

The approved LF script bytes hash to
`b4af0f8a47d57e57d35a86a6092851f0282d52b5b5ca95dd62dfe036d0588e8f`.
Owner approved the v13 79-line script and storyboard in this chat for PR #1795;
this did not approve paid generation, upload, or publication. Local dry run
returned `dry-run-local-only`, 79 lines, this exact hash. Six focused tests pass,
including a C19 edit that causes a SHA mismatch before any transport call.
On 2026-10-24, the authenticated apply returned `submitted` with review ID
`78946e32-854e-4beb-83ad-6f3d29712064`. Independent GET readback showed
project slug `story-everyday-seven-bank-c19`, series
`brand-stories-everyday-reversals`, episode 19, format `drama`, one pending
script card at that ID, exact card hash and `source_md` SHA-256 both
`b4af0f8a47d57e57d35a86a6092851f0282d52b5bca95dd62dfe036d0588e8f`,
79 scenes and 17,191 UTF-8 source bytes. A second apply returned
`already-present`, creating no duplicate. Series context after import still
showed paused, planned 20, finished 0; C19 stayed planned. The site UI needs
the separate `2026-10-23-show-brand-story-preproduction-intake-progress` ticket
to display plan and script counts beside finished films.
