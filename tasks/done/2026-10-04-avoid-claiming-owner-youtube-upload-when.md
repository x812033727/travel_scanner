---
id: 2026-10-04-avoid-claiming-owner-youtube-upload-when
title: Avoid claiming owner YouTube upload when pulling automatic publish approval
status: done
priority: P2
area: tools
owner: claude-opus-5-5-sync-auto-approval-message
claimed_at: 2026-10-05T00:27:10Z
created_at: 2026-10-04T17:29:40Z
completed_at: 2026-10-05T01:06:37Z
branch: claude/sync-auto-approval-message
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# Avoid claiming owner YouTube upload when pulling automatic publish approval

## Why

`recordApproval` returns “the owner confirmed the upload” for every newly pulled publish approval, including automatic package approval. During the LLM episode's normal publish-pull, the backend automatically approved the complete package while `youtube_video_id` remained null. The command therefore reported an owner upload that had not happened. Package approval and actual YouTube upload must remain distinct.

## Definition of done

- [x] Pulling a current automatic publish approval reports package approval without asserting owner upload or YouTube publication.
- [x] Existing approval persistence and hash checks remain intact; already-recorded and other gate messages are covered by focused fixtures.

## Steps

- [x] Check active scopes and the existing review message tests before claiming this fix.
- [x] Replace the inaccurate publish message and add a fixture with an approved package and no YouTube ID.

## How to verify

Run the focused `tools/video/review/sync.test.mjs` tests. Assert that a newly pulled publish approval records the actual metadata hash while its text makes no claim of owner upload or publication. Do not perform a real YouTube upload for this verification.

## Notes

- Observed 2026-10-04T17:24Z through unchanged normal publish-pull for `ai-term-large-language-model`. Publish review `cbf8689a-a38a-48fc-bce8-51e15188980d` was automatically approved at 17:18:41.446916Z with QA4/4; all five backend package attachments matched local SHA-256 and size, but the actual YouTube ID was null.
- The message is emitted at `tools/video/review/sync.mjs:1026`, after ordinary hash-bound approval recording. The producer preserved the raw stdout and explicitly classified it as a legacy label. No shared-code fix, owner approval, upload or publication was performed in the production ticket.
- 2026-10-05 (claude-opus-5-5-sync-auto-approval-message): `recordApproval` now answers a newly
  recorded publish approval with `upload package approved (metadata.json <first 12 hex>); this
  records the approval only, not a YouTube upload — upload/UPLOAD.md has the Studio steps`.
  The review the site returns has no `decided_by` (ReviewOut in
  `apps/api/app/video_reviews/schemas.py`), so the tool cannot tell an automatic approval from
  the owner's; the text is the same for both and claims neither an upload nor a publication.
  The hash check, `approve()`, the runtime-policy guard and "already recorded" are unchanged.
- Tests in `tools/video/review/sync.test.mjs`: the publish fixture moved into a shared
  `publishPackage(box)` helper; a new test pushes the real package, lets the fake site approve
  it with `youtube_video_id: null`, pulls, and checks the exact line, that nothing in stdout
  says owner/confirmed/uploaded/published/on YouTube, the recorded `metadata.json` SHA-256 and
  note, then "already recorded" and "has since changed" (no second entry). A second new test
  pins the final, languages and dubs messages and their "already recorded" (the languages line
  had no test before; dubs is also asserted in `tools/video/dubs/captions-package.test.mjs`).
  The fake `site()` takes a `project` option for fields of the GET answer.
- Left as they are, on purpose: the dubs line ("the owner uploaded these dub tracks") is the
  meaning of that gate (the owner approves it after uploading, `core/approvals.mjs` GATES), and
  the languages line already says "if any". `docs/videos/ai-term-large-language-model/README.md`
  quotes the old label as a historical observation of that episode; it is another claim's file
  and stays a correct record of what the CLI printed then. No consumer parses this stdout
  (`tools/video/automation/flow.mjs` only runs review-pull and reads the site).
- Claimed with `--force` over 2026-10-01-hand-off-owner-approved-renewed-finals
  (codex-video-stall-followthrough, branch `codex/video-approved-final-languages-20261004`,
  merged as #1210 on 2026-10-04T23:41Z and deleted; #1210 did not change sync.mjs) and the stale
  2026-09-28-drama-listener-stale-check (codex-ten-drama, PR #978 merged 2026-09-29). No open
  PR touched `tools/video/review/sync*` at claim time.
- Both files are bound by `docs/videos/long-form/review.json`; the PR is a draft until an
  independent reviewer adds the receipt increment.
