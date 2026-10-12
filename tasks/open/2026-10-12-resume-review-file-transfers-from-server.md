---
id: 2026-10-12-resume-review-file-transfers-from-server
title: Resume review file transfers from server acknowledged parts
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-12T04:22:02Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# Resume review file transfers from server acknowledged parts

## Why

The review upload client sends every 4 MiB part again after an interrupted transfer, even though the server returns the list of already received part indices. H03's 193 MB approved final stopped after 27 committed parts when the API became unavailable. Resending the whole file would repeat 113 MB of verified data. A bounded external recovery compared every stored part hash with the local approved final and sent only the missing indices; shared code was not changed.

## Definition of done

- [ ] Restarting a review transfer reuses server-acknowledged parts for the same full-file SHA and size.
- [ ] Only valid acknowledged indices are skipped; completion still requires the server's full-file SHA and size verification.
- [ ] Interruptions and resumptions retain actionable progress and terminal results without creating duplicate reviews or changing approved media.

## Steps

- [ ] Inspect upload() in tools/video/review/sync.mjs and the existing ReviewStore part contract.
- [ ] Implement bounded resumption using acknowledgements, with progress reporting and targeted interrupted-transfer tests.

## How to verify

Run the review sync tests with an upload fixture interrupted after multiple committed parts. Resume it and assert those confirmed parts are not sent again, the reconstructed file matches the original SHA, and exactly one review is created. Cover invalid received indices and a server that already holds the complete file.

## Notes

Observed 2026-10-12 while delivering curio-h03. apps/api/app/video_reviews/storage.py keeps numeric parts under slug/.parts/fullSHA and returns received plus complete. The client currently checks complete but ignores received. H03-specific preflight and per-part recovery receipts remain in its external _audit directory. Do not use the approved production episode as a destructive test fixture.
