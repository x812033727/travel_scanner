---
id: 2026-10-05-scrub-local-user-paths-from-the
title: Scrub local user paths from the T27 trash-bin evidence and rebind its digests
status: done
priority: P3
area: docs
owner: claude-opus-5-5-t27-scrub-paths
claimed_at: 2026-10-05T13:12:08Z
created_at: 2026-10-05T06:55:22Z
completed_at: 2026-10-05T13:51:03Z
branch: claude/t27-scrub-paths
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

- [x] None of the ten files contains a local user path; `<home>` (or `<repo>` for the main
      checkout) stands in its place.
- [x] Every digest of a changed file recorded in the folder matches the new bytes, each with a
      dated sentence saying why it changed and which commit holds the original.
- [x] Their entries are gone from `KNOWN` in `tools/repo-hygiene.test.mjs`.

## Steps

- [x] Re-run the binder search first (the files may have changed since 2026-10-05).
- [x] Scrub from the committed bytes with a script that keeps line endings and leaves JSON
      valid; then rebind in chain order (the bound file first, then each receipt that records it).
- [x] Remove the ten entries from `KNOWN`.

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

### 2026-10-05 claude-opus-5-5-t27-scrub-paths

- **Claim.** who-is-on-it found no active task and no open PR on either scope path. The only
  commit on the folder was bc5f18db8 (#1144), and the last one on the test was f69542616
  (#1271). The scope is unchanged.
- **Binder search, before.** For each of the ten files at HEAD, the search covered raw, LF and
  CRLF SHA-256 (hex and base64), SHA-1, MD5, the git blob id and the parsed-JSON SHA-256
  (compact, 2-space, and 2-space plus newline), each also as a 16-character prefix, across all
  tracked files. The result matches the Why section: only `fact-source-audit.json` is recorded
  (once in `final-runtime-review.json`, in `production-record.md`, twice in
  `runtime-audit.json`, and in `runtime-audit.md`), and only `visual-review.json` (twice in
  `final-runtime-review.json`, and once each in `final-runtime-review.md`,
  `runtime-audit.json` and `runtime-audit.md`). No file records a digest of a receipt.
  `docs/videos/long-form/plans.json` and `apps/api/app/video_plans/data/catalog.json` name
  the episode by slug only. No repository tool writes or reads these files (the episode's
  helper stayed outside the repository), so nothing could be regenerated, and the digests were
  rebound by script.
- **Scrub.** Each file was rebuilt from `git show HEAD:<path>` with one substitution: the
  drive-and-profile root became `<home>` in all three spellings found here (126 with forward
  slashes, 182 JSON-escaped with double backslashes, 7 with single backslashes). That is 315
  in all, and each file's count equals its old `KNOWN` entry. The rest of each path is kept:
  `<home>/.codex/...` for the Codex visualizations and managed worktree, and
  `<home>/mokaair-work/...` for the media folder outside the repository. None of them is the
  main checkout, so `<repo>` was not used. Every file was LF and stays LF. Every JSON file
  still parses and is still exactly `JSON.stringify(value, null, 2)` plus a newline. All the
  Markdown hits were already inside code spans.
- **Rebind, in chain order.** The two bound files were done first: `fact-source-audit.json`
  went from `1917da87…` to `fff4ae7c…` and `visual-review.json` from `47a69279…` to
  `ef00f943…`. Then the receipts that record them:
  - `final-runtime-review.json`: three values, with a `redaction_note` in
    `reviewer_relationship` and another in `binding`.
  - `final-runtime-review.md`: one value and a note paragraph.
  - `production-record.md`: one value and a note paragraph.
  - `runtime-audit.json`: three values, with a `redaction_note` at the top level, one in
    `final_closure` and one in `final_closure.visual_review`.
  - `runtime-audit.md`: two values and two note paragraphs.

  Each of the nine notes is dated 2026-10-05, names this task and says the originals are in
  commit bc5f18db8 (#1144). The bound files and the three other leaf files got placeholders
  only, as #1259 did.
- **Independent check.** A second script applied only the substitution and the two digest
  swaps to the HEAD bytes and compared the result with the working tree. Every file matches,
  apart from the nine added notes (the JSON files were compared after dropping
  `redaction_note`). A second binder search found the new digests in exactly the eight
  places the old ones were, found no file recording any receipt, and found no remaining
  `git grep` hit for either old digest.
- **Left alone.** The `KNOWN` entry for `tasks/2026-10-02-produce-one-t27-japan-trash-bin.md`
  stays. That task file is outside this scope.
- **Checks (Windows, 2026-10-05).**
  - `node --test tools/repo-hygiene.test.mjs`: 3/3 pass.
  - `node tools/video/long-form/cli.mjs check`: PASS, with no stale binding, because no file
    in the duration receipt changed.
  - `node tools/tasks.mjs check`: exit 0.
  - `npm run test:tools` (`node --test --test-concurrency=3`, same file set): 1,695 tests,
    1,690 pass, 3 skipped, 2 fail. Neither failure touches this change:
    - The known Windows-only `tts/check` test ("a second transcript clears a line only
      Gemini misheard").
    - `nginx-install.test.mjs`. Its 300-round bash loop hit the 90 s spawn timeout on a
      loaded machine, as it did for the previous rebind task. It reads only
      `ops/nginx/install.sh`.

    The run borrowed the shared `node_modules`. That copy was installed from an older
    `package-lock.json`, and the only lock change since then (#1252) bumps web packages.
