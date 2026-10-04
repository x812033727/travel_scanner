---
id: 2026-10-04-align-editorial-homepage-browser-contract
title: Align editorial homepage browser contract
status: done
priority: P1
area: web
owner: codex-gpt6-home-e2e
claimed_at: 2026-10-04T09:47:15Z
created_at: 2026-10-04T08:57:50Z
completed_at: 2026-10-04T09:52:15Z
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

The first revision then failed on head 8c1d in discovery-browser run 37191157140:
the workflow uses the real isolated API seed, not the local synthetic guide
listings, and four card-border intersection checks returned ratios below 1.
This same task is reopened to correct those test contracts without changing
homepage ordering, product source or shared fixtures.

## Definition of done

- [x] The contract asserts site context and every actually rendered published title/summary group before the feed without assuming fixture titles or locales.
- [x] The contract asserts the initial search CTA is fully in the viewport and above mobile nav.
- [x] After one deliberate native wheel scroll placing the card beneath the measured sticky header, the title, card-body metadata/summary/source paragraphs and all accessible controls must be fully in the viewport, clear the header and remain above measured mobile nav; required save/plan actions remain present and usable.
- [x] Homepage horizontal overflow and geometry evidence are checked before navigating to Explore.
- [x] Existing detail-dialog, link, navigation, dark/large/reduced-motion checks remain intact.
- [x] Both projects and all five editorial locales remain in the existing discovery workflow;
  CI execution is required integration validation, not claimed complete by this task.

## Steps

- [x] Check exact scope collisions, existing queue entries and landed/open PR work; claim.
- [x] Update only the existing frontend-flow spec and this task record.
- [x] Run scoped lint, diff and task-format checks; record the local server setup refusal.
- [x] Stop this agent's own synthetic API session after coordinating with root.
- [x] Safely reopen and reclaim this same owned task, review the real workflow/seed and second-round failure evidence, then update the contract within its existing single-file scope.

## How to verify

The existing GitHub discovery workflow must run `e2e/frontend-flow.spec.ts` on
both desktop-chromium and mobile-chromium against its production-mode build and
real isolated API seeded by `apps/api/tests/fixtures/frontend_flow_seed.py`.
Root verifies the new head's CI result after integration.
Scoped ESLint, diff and task-format checks validate the implementation locally.

## Notes

2026-10-04: exact `apps/web/e2e/frontend-flow.spec.ts` collision audit found no
active task or open PR touching the file. Root keeps responsibility for PR/CI
integration and closure; this agent does not commit or push.

Fixture correction: the original local plan relied on `tools/e2e-runtime-api.mjs`
guide titles. The discovery workflow actually starts the real API and the
frontend-flow seed only inserts a TravelHotspot, with no guides. `page.route`
does not intercept server-side homepage guide loading. The revised contract
checks every available SSR article group's nonempty titles/descriptions and
locale-specific internal article hrefs and DOM order, honestly allowing no groups
in this isolated seed. Existing filled
homepage SSR tests cover all three populated groups. No fixture or API changes
or additional network requests were introduced.

2026-10-04 implementation evidence:

- The initial search CTA must have the locale-specific `/search/new` href and be
  entirely in the viewport before any scroll. On mobile its lower edge must be
  above the measured bottom-navigation top, rather than a hardcoded viewport
  offset. The site intro and actual available article title/summary groups must
  precede the Discovery main in DOM order.
- The first revision's whole-card border intersection check is superseded by
  reader content and operation checks described below. Remaining Explore,
  detail-dialog, link and URL assertions were retained.
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

2026-10-04 second CI correction evidence:

- Discovery run 37191157140 / job 111403438623 reported 44 passed, 2 skipped and
  8 failed: four hardcoded Synthetic article-title assertions, and four whole
  card ratio-1 assertions (desktop zh-CN/ja/ko: 0.9977413415908813; mobile zh-CN:
  0.9966421127319336). Analytics downloaded the artifact and found no failing
  screenshots or traces, only error contexts. The original border geometry is
  unknown; pixel rounding or a 1px cause has not been established.
- After a single card scroll, title, direct card-body paragraphs and accessible
  links/buttons retain ratio 1 and explicit left/top/right/bottom viewport
  bounds. On mobile every lower edge must be above the measured nav top. The
  fixture's metadata, summary and source require at least three body paragraphs;
  the exact mock summary must also be present and fully visible. Awaiting the
  unique mock title first proves client replacement of the different SSR seed
  title/id, so this summary check does not assume the seed's content. Removing
  or hiding the summary fails the contract. Guest save and plan actions
  must be present, controls must be enabled, and a real client-rect fragment's
  center must hit the control or its descendant. No target is individually
  scrolled to make separate frames pass. Card decoration is not the reader-flow
  acceptance target; the ratio was not reduced.
- The test attaches title/paragraph/control/nav bounding boxes before geometry
  assertions, checks initial search and mobile-nav 44px targets, and checks home
  overflow before the existing Explore flow.
- `tools/tasks.mjs` commandStatus explicitly refuses done tasks, so the same
  owned file was reopened with a native single-file Move-Item after checking
  resolved source/target stay within the workspace and the destination is absent.
  Frontmatter was reset and the original owner reclaimed it (exit 0).
- Local server launch remains blocked by automatic approval review's stated
  `blocked by policy`. It was not retried; this revision's browser cases have
  not been executed locally. Root must validate desktop/mobile and all five
  locales in the new-head isolated discovery workflow. No local or new-head CI
  browser pass is claimed by this task.
- Final scoped ESLint with verified Node v24.19.0 exited 0, git diff --check
  exited 0, and task-format check exited 0 (1,411 files; existing unrelated
  stale/scope warnings remain). Full logs are stored outside the repo at
  `<home>/mokaair-work/adsense-review-20261004/frontend-contract-second-ci-eslint.log`
  and `frontend-contract-second-ci-tasks-open.log` in the same directory.
- Independent read-only review by the monetization research agent found no
  blocking selector/path finding, including the exact client summary and
  locale-specific guide/life article href additions. Implementation-only
  closure remains authorized by root, with new-head CI integration still required.

2026-10-04 native reader-scroll correction:

- On head ec64cc5, discovery run 37192596399 / job 111407752725 reported
  50 passed, 2 skipped and 2 failed, both mobile zh-TW/zh-CN. The paragraph
  loop failed its unchanged mobile-nav bound: bottom 764.8125 exceeded nav top
  759.421875 by 5.390625 CSS pixels. Title and exact summary checks had already
  passed. The error contexts show metadata, title, summary, source/language,
  then actions; this strongly points to source/language text, but no individual
  bounds were saved, so the exact target and before/after scroll position were
  not directly measured. It is not evidence of a failed control assertion.
- The packaged Playwright code dispatches conditional scrolling through CDP
  DOM.scrollIntoViewIfNeeded. Its layout-viewport visibility does not prove
  clearance from the fixed navigation. Existing product CSS gives page-end
  space and top scroll-padding; it does not establish what that conditional
  call did in this failed run. No product CSS defect or pixel-rounding cause is
  claimed, and no product files were changed.
- Root authorized a corrected reading action: wait for save/plan readiness,
  measure card/header/document bounds, move the pointer over the document
  midpoint, then issue exactly one native wheel scroll to place the card below
  the header with 16px reading space. The target is bounded by the document's
  scroll range; a condition poll waits for target scrollY and stable card
  geometry. Every existing full-visibility/nav bound and hit test remains;
  header clearance is additionally required. No per-target scrolling, fixed
  delay, threshold reduction or retry was added.
- Previous info.attach(body) geometry was not persisted under test-results,
  the workflow's upload directory. The corrected test writes before/after
  scrollY, scrollHeight/maxScrollY, card/header/nav and reader/control rectangles
  to info.outputPath("first-card-reader-geometry.json"), then attaches that path.
  A finally block saves evidence even if the scroll-settlement poll fails.
- This same owned task was safely reopened/reclaimed again (claim exit 0).
  Local server launch and browser execution remain unattempted after the earlier
  automatic approval refusal. Latest-head isolated CI remains root's required
  integration validation, not a local or CI pass claimed by this task.
- Final independent read-only review found no blocker: the wheel is issued
  once, clamp/settlement use actual scroll position and stable card geometry,
  and full reader/header/nav/hit assertions and persisted diagnostic output
  remain intact. This is static review, not a browser pass or CSS-cause proof.
- Native-wheel revision scoped ESLint with verified Node v24.19.0 exited 0;
  task check exited 0 (1,411 files), and git diff --check exited 0. Logs remain
  outside the repo at
  `<home>/mokaair-work/adsense-review-20261004/frontend-contract-native-wheel-eslint.log`
  and `frontend-contract-native-wheel-tasks-open.log` in the same directory.
  Root again authorized implementation-only task closure before new-head CI.
