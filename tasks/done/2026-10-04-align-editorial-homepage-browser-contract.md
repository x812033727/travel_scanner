---
id: 2026-10-04-align-editorial-homepage-browser-contract
title: Align editorial homepage browser contract
status: done
priority: P1
area: web
owner: codex-gpt6-home-e2e
claimed_at: 2026-10-04T08:58:01Z
created_at: 2026-10-04T08:57:50Z
completed_at: 2026-10-04T09:05:54Z
branch: codex/adsense-content-fixes-20261004
depends_on: []
scope:
  - apps/web/e2e/frontend-flow.spec.ts
---

# Align editorial homepage browser contract

## Why

PR #1206's intentional homepage change places site context and published article
entrances before Discovery. The existing frontend-flow browser test still requires
the first Discovery card title to appear above the fold immediately on mobile,
causing all five mobile locale cases in discovery-browser run 37190290731 to fail.
The test must verify the new reading/search contract instead of restoring the old
feed-first layout or weakening its numeric assertion.

## Definition of done

- [x] The contract asserts site context and available published title/summary groups before the feed.
- [x] The contract asserts the initial search CTA is fully in the viewport and above mobile nav.
- [x] The contract scrolls the first Discovery card and asserts full visibility above mobile nav.
- [x] Existing detail-dialog, link, navigation, dark/large/reduced-motion checks remain intact.
- [x] Both projects and all five editorial locales remain in the existing discovery workflow;
  CI execution is required integration validation, not claimed complete by this task.

## Steps

- [x] Check exact scope collisions, existing queue entries and landed/open PR work; claim.
- [x] Update only the existing frontend-flow spec and this task record.
- [x] Run scoped lint, diff and task-format checks; record the local server setup refusal.
- [x] Stop this agent's own synthetic API session after coordinating with root.

## How to verify

The existing GitHub discovery workflow must run `e2e/frontend-flow.spec.ts` on
both desktop-chromium and mobile-chromium against its production-mode build and
synthetic runtime API. Root verifies the new head's CI result after integration.
Scoped ESLint, diff and task-format checks validate the implementation locally.

## Notes

2026-10-04: exact `apps/web/e2e/frontend-flow.spec.ts` collision audit found no
active task or open PR touching the file. Root keeps responsibility for PR/CI
integration and closure; this agent does not commit or push.

Fixture boundary: `tools/e2e-runtime-api.mjs` publishes homepage how-to articles
only in en and lifestyle articles only in zh-TW. Assert those actual titles and
summaries before Discovery. ja/ko/zh-CN legitimately have no homepage article
group in this fixture; verify their intro, initial search CTA and scroll/card
visibility without inventing translated fallback articles. The shared API stays
unchanged as instructed by root.

2026-10-04 implementation evidence:

- The initial search CTA must have the locale-specific `/search/new` href and be
  entirely in the viewport before any scroll. On mobile its lower edge must be
  above the measured bottom-navigation top, rather than a hardcoded viewport
  offset. The site intro and actual en/zh-TW article title/summary groups must
  precede the Discovery main in DOM order.
- After `scrollIntoViewIfNeeded`, the entire first card and its title must be in
  the viewport. The card's lower edge must be above the measured mobile nav top.
  Remaining Explore, detail-dialog, link and URL assertions were retained.
- Verified Node v24.19.0 scoped ESLint for `e2e/frontend-flow.spec.ts` completed
  with exit 0. `tools/tasks.mjs check` completed with exit 0 (1,411 task files;
  pre-existing unrelated stale/overlap warnings remain in the full local log).
- Local synthetic API started on free port 18831 in owned exec session 93188.
  Starting Next on port 18832 with `API_INTERNAL_URL=http://127.0.0.1:18831`
  was rejected at CreateProcess by automatic approval review. The only stated
  reason was `blocked by policy`; no additional reason was supplied. No retry
  or alternate launch was attempted.
- Root instructed using the existing isolated CI instead. This local spec was
  not executed, and no local browser pass or CI pass is claimed. The synthetic
  API session was stopped with Ctrl-C (intentional termination exit 1).
- Implementation-only closure is authorized by root; the new-head desktop/mobile
  CI result remains a required root integration check. No shared API, product
  source, build, production endpoint, commit or push was changed by this agent.
- Root's independent review caught that matching every paragraph containing
  `Mokaair` would select both eyebrow and intro in some languages. The final
  locator selects the section's single direct intro paragraph, asserting both
  visibility and brand text. Scoped diff check completed with exit 0.
