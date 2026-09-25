---
id: 2026-09-25-add-web-i18n-e2e-skill
title: Add the web-i18n-e2e skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5-web-i18n-e2e
claimed_at: 2026-09-25T15:11:31Z
created_at: 2026-09-25T15:11:07Z
completed_at: 2026-09-25T15:27:03Z
branch: claude/skill-web-i18n-e2e
depends_on: []
scope:
  - .agents/skills/web-i18n-e2e
  - .claude/skills/web-i18n-e2e
---

# Add the web-i18n-e2e skill

## Why

Every change that adds UI text or a browser test in `apps/web` re-derives the same rules
from `tools/check-i18n.mjs`, `apps/web/playwright.config.ts`, `tools/e2e-runtime-api.mjs`
and half a dozen flake tickets: which five files a key goes in, why `check:i18n` says
"translation keys differ" without naming the key, why the Han-text check only fires after
`git add`, the seven places a new namespace touches (two of which no check covers), which
server the e2e data comes from, how an admin spec signs in, and what made past specs flaky.
A shared skill loads that on demand instead.

## Definition of done

- [x] `.agents/skills/web-i18n-e2e/` exists with SKILL.md, four references, a read-only
      key-diff script and `agents/openai.yaml`; `.claude/skills/web-i18n-e2e/SKILL.md` is its
      byte-identical copy.
- [x] Every command, path, flag and symbol in it was checked against main `98cce24b`.
- [x] `node --test tools/skills.test.mjs` passes.

## Steps

- [x] Read `tools/check-i18n.mjs`, `tools/json-duplicate-keys.mjs`, `docs/ui-text-overrides.md`,
      `apps/web/i18n/request.ts`, `apps/web/vitest.setup.tsx`, `apps/web/lib/ui-text.ts`,
      `apps/api/app/ui_text/schemas.py` and the `lib/*-copy.ts` modules.
- [x] Read `apps/web/playwright.config.ts`, `tools/e2e-runtime-api.mjs`, `apps/web/e2e/session.ts`,
      the admin specs and every workflow that runs Playwright.
- [x] Read the flake tickets in `tasks/done` (navigation, offline-today, modal-escape,
      duplicate runs, recurring CI flakes) and the two open ones (midnight rollover, admin news mock).
- [x] Write SKILL.md, `references/{i18n,check-i18n,e2e-local,flake-lessons}.md`, `scripts/i18n-diff.mjs`.

## How to verify

```bash
node --test tools/skills.test.mjs
node .agents/skills/web-i18n-e2e/scripts/i18n-diff.mjs     # "No differences across 25 namespace(s)."
npm run check:i18n
```

## Notes

- Verified by running: `check:i18n` output for a missing key and for staged Han text,
  the key-diff script against a deliberately broken `ja/foods.json`, the plural-branch
  parameter trap, and `playwright test --list`. A real Playwright run was not possible in a
  worktree without its own `node_modules` (dev server fails on `.next/dev/.../build-manifest.json`),
  and the dev server rewrote `apps/web/next-env.d.ts`; both are now in `references/e2e-local.md`.
- Stale: `docs/ui-text-overrides.md` still says 22 namespaces; there are 25 (24 editable).
- Nine specs run in no workflow (admin-analytics, admin-hotspot-ai-search, claude-code-series,
  csp, deployments, flight-status, gemini-series, hotspot-guides, hotspot-review-editor).
  Listed in the skill; not changed here.
- `apps/web/i18n/request.ts` and `apps/web/vitest.setup.tsx` each hardcode the namespace list
  and nothing checks them against `messages/en`; a drift guard would be a small follow-up.
- Only SKILL.md is mirrored under `.claude/skills/`, as with every other shared skill; the
  references and script live once under `.agents/` (see the header of `tools/skills.test.mjs`).
