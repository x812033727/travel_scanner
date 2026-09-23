---
id: 2026-09-23-scrub-host-details-from-docs
title: Committed docs carry a host session name, a disposable database password and local machine paths
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-23T15:57:50Z
completed_at:
branch:
depends_on: []
scope:
  - docs/ai-terms-series/postgresql-validation.json
  - docs/article-localization/releases/batch007-017/README.md
  - docs/article-localization/releases/batch018
  - docs/article-localization/releases/batch019
  - docs/article-localization/releases/batch020
  - docs/article-localization/releases/batch021
  - docs/ai-news-2026-09-mid
  - docs/ai-workflow-series/README.md
  - docs/claude-code-series
  - docs/gemini-series
  - docs/codex-learning/evidence
  - docs/catalog-content-reviews/2026-09-09-followup.json
  - ops/nginx/README.md
  - tasks/done
  - .gitignore
  - tools/repo-hygiene.test.mjs
  - package.json
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

- [ ] No tracked file contains the saved-session name, the disposable password, or the local
      user path. Git history keeps them; rewriting history is out of scope and not worth it
      for recon-level data.
- [ ] A test under `tools/` fails when a tracked file under `docs/`, `tasks/` or `ops/` gains
      a local user path, a `plink -load` invocation, or a `password=` / `PASSWORD=` value
      that is not a documented placeholder; wired into `npm run test:tools`.
- [ ] `.gitignore` lists the private-key patterns.

## Steps

- [ ] Replace the session name with `<saved-session>`, the password with
      `<disposable-password>`, and the user path with `<repo>` / `<home>` in the files listed
      in scope. Use a Python script written to the scratchpad (non-ASCII and backslashes; see
      the dev-env notes), not `sed -i`.
- [ ] Add `tools/repo-hygiene.test.mjs` and register it in the root `package.json`
      `test:tools` script.
- [ ] Extend `.gitignore`.

## How to verify

```bash
npm run test:tools
git grep -c -iE "plink -load|[A-Z]:[\\/]+Users[\\/]+[a-z0-9]+[\\/]+mokaair" -- docs tasks ops | wc -l   # expect 0
```

## Notes

- Found in the 2026-09-23 security review (findings L7, L8, L9).
- The saved-session name and the root login are recon only: the host needs the key. Rotate
  nothing.
