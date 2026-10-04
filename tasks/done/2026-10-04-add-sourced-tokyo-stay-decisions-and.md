---
id: 2026-10-04-add-sourced-tokyo-stay-decisions-and
title: Add sourced Tokyo stay decisions and published city articles
status: done
priority: P1
area: web
owner: codex-gpt6-city
claimed_at: 2026-10-04T08:18:36Z
created_at: 2026-10-04T08:14:39Z
completed_at: 2026-10-04T08:44:48Z
branch: codex/adsense-content-fixes-20261004
depends_on: []
scope:
  - apps/web/components/destination-guide.tsx
  - apps/web/components/destination-guide.test.tsx
  - apps/web/lib/destinations-copy.ts
  - apps/web/lib/destinations-copy.json
  - apps/web/lib/destination-decisions.ts
  - apps/web/lib/destination-decisions.json
  - apps/web/app/[locale]/destinations/[destinationId]/page.tsx
  - apps/web/app/[locale]/destinations/[destinationId]/page.test.tsx
  - docs/adsense-tokyo-sources.md
  - docs/adsense-about-drafts.md
---

# Add sourced Tokyo stay decisions and published city articles

## Why

The city page currently lists area names and filtered article hubs without enough context to compare Tokyo bases or preview real published articles. Readers need sourced transport trade-offs and language-specific articles before partner options.

## Definition of done

- [x] Tokyo renders four sourced stay decision cards in all five locales before partner options.
- [x] City pages render up to three current published travel articles in the selected locale and destination, with honest empty and unavailable states.
- [x] Other city area lists and filtered article hub links remain available.
- [x] About/editorial copy is preserved as an unpublished five-locale draft with owner fact checks outside public copy.
- [x] Focused component and route tests pass; integration verification is handed to the root agent.

## Steps

- [x] Read content, task, development, i18n, and local Next.js guidance; verify official Tokyo area and transit sources.
- [x] Add factual five-locale decision data and SSR cards.
- [x] Connect the existing moderated published guide reader and verify states and filtering.

## How to verify

From apps/web, run focused Vitest for components/destination-guide.test.tsx and app/[locale]/destinations/[destinationId]/page.test.tsx with one worker. The coordinating root agent handles broader lint, i18n, typecheck, and integration checks.

## Notes

Working on the existing shared codex/adsense-review-audit-20261004 branch by root authorization; no branch change or commit. Draft copies and source evidence also live outside the repository under `<home>/mokaair-work/adsense-review-20261004/`. No browser, CMS, SSH, deployment, or publication actions are included in this task.

- Focused validation on 2026-10-04: `npx vitest run components/destination-guide.test.tsx 'app/[locale]/destinations/[destinationId]/page.test.tsx' --maxWorkers=1 --fileParallelism=false` passed 2 files / 38 tests, exit 0. Scoped `git diff --check` passed, exit 0.
- Coverage checks all five locales, city+section+locale request filters and limit 3, non-Tokyo areas, empty vs unavailable articles, filtered hub links, and SSR decision/source/article HTML ordering before partner options.
- Parent review corrected the About text in all five languages to refer to any update or verification dates actually shown, rather than implying every article displays an update date.
- The coordinating root agent completed integration review and broader checks before task closure. No live-published or AdSense-approved state is claimed.
- Staged i18n review found the newly added Chinese article-state strings in the TypeScript copy module. Expanded scope to `destinations-copy.json`, moved all current 5-locale / 28-key copies there without changing any strings, and retained the existing English fallback. The migration compared the full JSON payload against the pre-migration values and checked matching keys.
- Staged only `destinations-copy.ts` and `destinations-copy.json` for this follow-up. `npm run check:i18n` passed (5 locales / 25 namespaces), exit 0. Focused single-worker Vitest including the existing `lib/destinations-copy.test.ts` passed 3 files / 48 tests, exit 0; staged scoped `git diff --check` passed, exit 0.
- Root-reported local integration on 2026-10-04: full web typecheck, staged i18n checks, scoped ESLint, and `next build --webpack` passed with exit 0.
- Root-reported Chrome verification used a local synthetic API: desktop and mobile Tokyo pages plus all five locale city routes showed four sourced decision cards and twelve official links before article cards and partner options. This confirms the local rendered flow against test data, not the current production article inventory or a deployment.
- About/editorial documents remain unpublished drafts with owner fact checks outside the public copy. This task does not establish AdSense approval, actual ad serving, or production publication.
