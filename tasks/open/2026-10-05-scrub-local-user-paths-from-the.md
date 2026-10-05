---
id: 2026-10-05-scrub-local-user-paths-from-the
title: Scrub local user paths from the T27 trash-bin evidence and rebind its digests
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T06:55:22Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/sothatswhy-t27
  - tools/repo-hygiene.test.mjs
---

# Scrub local user paths from the T27 trash-bin evidence and rebind its digests

## Why

The repository is public, and ten files under `docs/videos/sothatswhy-t27/` still carry the
local Windows profile path (315 matches in all: `visual-review.json` 234,
`final-runtime-review.json` 42, `runtime-audit.json` 11, `branding-adoption.json` 9,
`runtime-audit.md` 7, `fact-source-audit.json` 6, two each in `final-runtime-review.md` and
`visual-review.md`, one each in `author-note.md` and `production-record.md`).
`tools/repo-hygiene.test.mjs` tolerates them in its `KNOWN` table. They were listed there when
#1148 landed because the T27 episode (#1144, task 2026-10-02-produce-one-t27-japan-trash-bin)
was still another ticket's work; that task is done now, so nobody will clean them on a later
edit.

Two of the files are hash-bound inside the folder, so a plain scrub would break receipts:
`fact-source-audit.json` is recorded by `final-runtime-review.json`, `production-record.md`,
`runtime-audit.json` and `runtime-audit.md`; `visual-review.json` by `final-runtime-review.json`,
`final-runtime-review.md`, `runtime-audit.json` and `runtime-audit.md`. On 2026-10-05 no other
tracked file recorded a digest (raw, LF or CRLF SHA-256, base64, SHA-1, MD5 or git blob id) of
any of the ten.

## Definition of done

- [ ] None of the ten files contains a local user path; `<home>` (or `<repo>` for the main
      checkout) stands in its place.
- [ ] Every digest of a changed file recorded in the folder matches the new bytes, each with a
      dated sentence saying why it changed and which commit holds the original.
- [ ] Their entries are gone from `KNOWN` in `tools/repo-hygiene.test.mjs`.

## Steps

- [ ] Re-run the binder search first (the files may have changed since 2026-10-05).
- [ ] Scrub from the committed bytes with a script that keeps line endings and leaves JSON
      valid; then rebind in chain order (the bound file first, then each receipt that records it).
- [ ] Remove the ten entries from `KNOWN`.

## How to verify

```bash
node --test tools/repo-hygiene.test.mjs
npm run test:tools
git grep -n <each old digest>   # expect no hit outside an explicitly historical record
```

## Notes

- Found while doing 2026-10-02-rebind-receipts-after-scrubbing-host-details, which rebound the
  eleven files it named and left these alone (outside its scope). Its Notes describe the method:
  substitutions from `git show HEAD:<path>`, digests computed rather than typed, and a note
  next to every rewritten digest naming the commit with the original bytes.
