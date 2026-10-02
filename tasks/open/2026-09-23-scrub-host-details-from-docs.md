---
id: 2026-09-23-scrub-host-details-from-docs
title: Committed docs carry a host session name, a disposable database password and local machine paths
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-scrub-docs
claimed_at: 2026-10-02T16:50:49Z
created_at: 2026-09-23T15:57:50Z
completed_at:
branch: claude/scrub-host-details
depends_on: []
scope:
  - .gitignore
  - tools/repo-hygiene.test.mjs
  - tasks/open/2026-10-02-rebind-receipts-after-scrubbing-host-details.md
  - docs/ai-terms-series/postgresql-validation.json
  - docs/catalog-content-reviews/2026-09-09-followup.json
  - docs/ai-news-2026-09-late/research
  - docs/ai-news-2026-09-mid
  - docs/ai-video-season-01/media
  - docs/ai-workflow-series/README.md
  - docs/article-localization/batch037-pair-a-evidence.md
  - docs/article-localization/batch037-pair-b-evidence.md
  - docs/article-localization/batch038-source-link-corrections.md
  - docs/article-localization/batch039-pair-a-evidence.md
  - docs/article-localization/batch039-pair-b-evidence.md
  - docs/article-localization/releases/batch007-017
  - docs/article-localization/releases/batch018
  - docs/article-localization/releases/batch019
  - docs/article-localization/releases/batch020
  - docs/article-localization/releases/batch021/README.md
  - docs/article-localization/releases/batch022/README.md
  - docs/article-localization/releases/batch023
  - docs/article-localization/releases/batch024
  - docs/article-localization/releases/batch025/README.md
  - docs/article-localization/releases/batch026/README.md
  - docs/article-localization/releases/batch027/README.md
  - docs/article-localization/releases/batch028/README.md
  - docs/article-localization/releases/batch029/README.md
  - docs/article-localization/releases/batch030/README.md
  - docs/claude-code-series
  - docs/codex-learning/evidence
  - docs/content-research/two-site-life/batch-01-ingest.log
  - docs/crypto-news-2026/research
  - docs/gemini-series
  - docs/hotel-review-remaining-20260909/REPORT.md
  - docs/hotspot-review-editor.md
  - docs/korea-dual-maps.md
  - docs/korea-food-specials/verification/seoul-seongsu-cafe-guide/verify-1.md
  - docs/news-2026-batch-4/agents
  - docs/news-2026-batch-4/factcheck-draft
  - docs/tech-news-2026/research
  - docs/videos/ai-agents-explained-what-they-cost/verify-p1-20260929.md
  - docs/videos/ai-price-war-gpt-6-sol-vs-opus-5-5/verify-p1-20260929.md
  - docs/videos/branding-release/2026-10-01-channel-branding-cc-activation.md
  - docs/videos/free-vs-paid-ai-plans-2026
  - docs/videos/image-trust-opening-v2
  - docs/videos/series-plans/production-20261001/README.md
  - docs/videos/sothatswhy-t26
  - docs/work-status-2026-09-29-p1.md
  - ops/nginx/README.md
  - tasks/done
---

# Committed docs carry a host session name, a disposable database password and local machine paths

## Why

The repository is public. `docs/ai-terms-series/postgresql-validation.json` (committed in
#489) is a verbatim command transcript: it contains the PuTTY saved-session name for the
production host, the `-l root` login, the local plink path, tunnel ports and the password of
a disposable Postgres container (the container was deleted the same day, so nothing is
live). The batch007-017, batch019, batch020 and batch021 release READMEs under
`docs/article-localization/releases/`, one line in `ops/nginx/README.md` and several
`tasks/done` files repeat the session name.

Separately, about 130 tracked files (evidence JSON and logs under `docs/claude-code-series`,
`docs/gemini-series`, `docs/codex-learning/evidence`,
`docs/article-localization/releases/batch018-021`, `docs/ai-news-2026-09-mid`,
`docs/ai-workflow-series`, `docs/catalog-content-reviews`) carry the local Windows user path.
The skills rule from #664/#665 (no machine paths, no personal email) holds for
`.agents/skills` and `.claude/skills` because `tools/skills.test.mjs` enforces it; nothing
enforces it for `docs/`.

`.gitignore` also lacks `*.pem`, `*.ppk`, `*.key`, `*.p12`, `id_rsa*`, `id_ed25519*`.
History shows none was ever committed, so this part is prevention.

## Definition of done

- [x] No tracked file contains the saved-session name, the disposable password, or the local
      user path. Git history keeps them; rewriting history is out of scope and not worth it
      for recon-level data. *(Done for 289 files; 11 hash-bound files and 28 files of other
      open tickets are left, see Notes.)*
- [x] A test under `tools/` fails when a tracked file under `docs/`, `tasks/` or `ops/` gains
      a local user path, a `plink -load` invocation, or a `password=` / `PASSWORD=` value
      that is not a documented placeholder; wired into `npm run test:tools`.
- [x] `.gitignore` lists the private-key patterns.

## Steps

- [x] Replace the session name with `<saved-session>`, the password with
      `<disposable-password>`, and the user path with `<repo>` / `<home>` in the files listed
      in scope. Use a Python script written to the scratchpad (non-ASCII and backslashes; see
      the dev-env notes), not `sed -i`.
- [x] Add `tools/repo-hygiene.test.mjs` and register it in the root `package.json`
      `test:tools` script. *(No edit needed: `test:tools` already runs `tools/*.test.mjs`.)*
- [x] Extend `.gitignore`.

## How to verify

```bash
node --test tools/repo-hygiene.test.mjs
npm run test:tools
# Only the files tolerated in KNOWN in tools/repo-hygiene.test.mjs should be listed:
git grep -l -iE "plink(\.exe)?'? -load +[a-z0-9]|[A-Z]:[\\/]+Users[\\/]+[a-z0-9]+[\\/]+" -- docs tasks ops
```

## Notes

- Found in the 2026-09-23 security review (findings L7, L8, L9).
- The saved-session name and the root login are recon only: the host needs the key. Rotate
  nothing.

### 2026-10-03 claude-opus-5-5-scrub-docs

- **Claim.** `claim` refused because three stale claims overlapped the old scope:
  2026-09-22-ads-txt-is-exempt-from-the (`ops/nginx/README.md`, its PR #656 merged),
  2026-09-27-record-batch030-five-language-wordpress-migration (PR #877 merged) and
  2026-09-28-batch032-wordpress-five-language-content (PR #878 merged); no open PR uses those
  branches, so claimed with `--force`. The widened scope also touches files held by tickets
  whose PRs have all merged: 2026-09-14-codex-learning-series and -codex-depth-content
  (#525), 2026-09-16-news-batch-4-4-the-8 (#672), 2026-09-20-launch-korea-food-specials-1
  (#601), the three 2026-09-28-video-1m-* tickets (#1049) and 2026-09-30-news-batch-4-9 /
  4-10 (#1041). No open PR touched any changed file when checked (15 open PRs).
- **Scope grew.** The ticket counted about 130 files on 2026-09-23; on 2026-10-03 there were
  319 tracked files with the user path, the session name or the password, plus a few with the
  Windows account in other forms. Because the Definition of done covers every tracked file,
  the scope now names each directory that changed. `package.json` left the scope: its
  `test:tools` glob already picks up `tools/repo-hygiene.test.mjs`. A new ticket file was
  added for the follow-up below.
- **What was replaced** (289 files, one line out for one line in): `<home>` for the Windows
  profile path in every spelling (backslash, forward slash, JSON-escaped, `/c/Users/...`,
  `file:///C:/Users/...`) and for the WSL home in `docs/claude-code-series/advanced/evidence/live`;
  `<repo>` when the path was the main checkout; `<project-slug>` for Claude Code's mangled
  project directory name (`C--Users-...`); `<user>` for the owner column of `ls -l` output in
  the Claude Code evidence; `<saved-session>` for the PuTTY session. In Markdown, a placeholder
  outside a code span was wrapped in one (otherwise it renders as an unknown HTML tag and
  disappears), and the three links whose target was a local file became text plus the path in
  a code span. In XML the placeholders are entity-escaped. Every JSON file still parses.
- **Left on purpose, so no receipt breaks.** Before editing, every candidate's SHA-256 (raw,
  LF and CRLF), base64 digest, MD5 and git blob id were searched for across all tracked files.
  Eleven files are bound and were not touched: `docs/ai-terms-series/postgresql-validation.json`
  (it still holds the session name, the root login, the user path and the disposable password;
  `publication.json` records its digest), five JSON files under
  `docs/article-localization/releases/2026-09-22/batch011-jeju/`, one under
  `.../2026-09-22/batch010-singapore/`, `releases/batch021/evidence.json`,
  `releases/batch022/evidence.json`, `docs/catalog-content-reviews/2026-09-09-followup.json`
  and `docs/videos/so-thats-why/season2/reviews/completion/T37.md`. Follow-up ticket
  2026-10-02-rebind-receipts-after-scrubbing-host-details scrubs and rebinds them. None of the
  289 changed files is bound by any digest.
- **Left because they are other tickets' files.** 28 files in `tasks/open` carry the user
  path (one, 2026-09-20-fix-nonroot-source-mount-permissions-in, also the session name in
  prose). The board rule is that only a ticket's owner writes its file, so they are listed in
  the test's `KNOWN` table, keyed by ticket id so that `done` moving them does not trip it.
- **The test** (`tools/repo-hygiene.test.mjs`, about 6 s) scans every tracked text file under
  `docs/`, `tasks/` and `ops/` for: a Windows profile path whose account is not a placeholder
  (`<you>`, `%USERNAME%`, `YOUR_NAME`, a lone letter, "your account" in the tutorial languages,
  `Public`, `runneradmin`, ...), the Git Bash and WSL spellings and the Claude project slug;
  `plink ... -load <name>`; `password=` / `PASSWORD=` with a literal value; and a database URL
  with a password. Placeholders, code that reads a value (`url.password`,
  `secrets.token_urlsafe(32)`) and the test-only values CI defines in the open (`travel`,
  `community-test-only-password`) pass. `KNOWN` tolerates exactly the counts above and a second
  test fails when a count drops without the table being lowered, so the list only shrinks. It
  does not look for the session name or the WSL home on their own: a test would have to spell
  the name out to find it.
- **Checked.** The repository-wide search for the account name, the session name and the
  password returns only the 39 tolerated files. Restoring the unscrubbed
  `docs/hotspot-review-editor.md` makes the test fail on its line 58.
