---
id: 2026-10-04-address-adsense-low-value-content-before
title: Address AdSense low-value content before requesting review
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-04T07:55:29Z
completed_at:
branch: codex/adsense-content-fixes-20261004
depends_on: []
scope:
  - docs/adsense-review-readiness.md
  - docs/frontend-monetization-plan.md
---

# Address AdSense low-value content before requesting review

## Why

AdSense still shows Needs attention / low-value content for mokaair.com on 2026-10-04.
Ownership is verified, public ads.txt answers correctly, and the Google CMP message is
Published. The remaining work is editorial/site-value acceptance, not an ID or CMP reset.
The limited evidence and priority order are in docs/adsense-review-readiness.md.

## Definition of done

- [ ] Record a meaningful sample of each public content type/localized hub, including thin or repeated pages.
- [x] Track the scoped corrections and original value with sources, limitations and dated review evidence.
- [ ] Confirm homepage identity/curation and an improved city-guide example in the live user flow.
- [ ] Prepare truthful About/editorial/AI assistance/corrections text; obtain owner verification and publication approval before CMS writes.
- [x] Confirm FAQ repair locally and current ads.txt account status separately from content acceptance.
- [ ] Ask the owner to submit/authorize rereview only after improvements are concrete and reviewed; record the result without promising approval.

## Steps

- [x] Claim this coordination scope; file/claim exact source paths separately before any code/content edits.
- [ ] Review the listed samples and extend the inventory according to site topics; preserve the owner's decision to retain lifestyle topics indexed.
- [x] Do not claim AI-assisted content is low value solely because of its origin or use a fixed article count/waiting period as a Google threshold.
- [x] Prepare reviewable corrections, validate them, and distinguish drafted, published, rereview submitted and Ready states.

## How to verify

Use current AdSense Sites details, public rendered pages, dated editorial evidence and
docs/adsense-review-readiness.md. HTTP 200 and local tests do not establish originality
or Google approval. Account and CMS changes require the precise owner-approved action.

## Notes

2026-10-04 audit only: no CMS changes, ad/CMP settings changes, deployment or rereview.
Examples to address include generic discovery reasons before substantial home content,
Tokyo's name-only planning sections, an article FAQ reading defect (separate task
2026-10-04-keep-article-faq-headings-and-answers), and About text that still describes only
travel. Google did not identify any of these URLs as the rejection cause. The existing
ads.txt host/logging ticket remains intact; its account follow-up is not complete.

2026-10-04 repair handoff: FAQ/home/Tokyo code and five-locale About drafts are
prepared and independently reviewed. Focused unit regressions total 227 passed;
local Chrome verifies desktop/mobile FAQ and layout using a synthetic API.
Full web lint, typecheck, staged i18n and production `next build --webpack` passed,
exit 0. The isolated FAQ Playwright case passed desktop and mobile (2 tests,
13.8s, exit 0). Complete CI is tracked on the implementation PR's latest head.
Public ads.txt is still correct; the account still says Not found with its 9/23
timestamp and no Check updates control in the inspected site-detail view. Across
13 retained crawl logs, all 55 matching ads.txt requests answered 200, including
two 9/22 source addresses matching current Google-published crawler ranges.
This task remains open for a broader editorial sample, owner fact/publication
approval for About, deployment and live-page acceptance, and an eventual policy
rereview decision. Do not repeat account setup or mark Google Ready from local checks.
The audit-document PR #1205 merged while this work was being prepared; code fixes
use the separate codex/adsense-content-fixes-20261004 branch.

2026-10-04 08:55 UTC read-only production preflight: another session deployed
main `41f2f363b` at 08:52 UTC, including #1202/#1203/#1205. Host checkout is clean,
deploy lock free, hold absent, no flagged unactivated release. This supersedes
the earlier live `0768b8a` snapshot; repair PR #1206 remains a draft and is not live.
CI discovered five old mobile frontend-flow assertions requiring the discovery
card in the initial viewport. The homepage intentionally leads with site context
and articles; scoped task `2026-10-04-align-editorial-homepage-browser-contract`
updated the tests to verify those plus initial search access and discovery visibility
after scrolling rather than restoring feed-first order. Scoped lint/diff/task checks
passed; the new cases require actual confirmation on the latest head's isolated CI.
Manual local server launch for this additional spec was rejected by automatic
approval review (`blocked by policy` only); no alternate launch was attempted.
Existing build-backed local FAQ tests still passed. The new homepage spec is not
claimed locally executed; all five locales and both projects will be checked in CI.
The account was independently reopened before 09:01 UTC and still showed Not found,
the 9/23 timestamp, and Needs attention/low-value content. Fresh screenshot saved;
no account, payment, policy rereview or CMS action was performed.

Second CI integration (8c1dcea): API/web/container checks passed, but the revised
homepage browser spec incorrectly assumed the local mock's guide titles. The
actual discovery workflow uses a real test API and seeds a hotspot, without guide
articles. The follow-up verifies whatever article groups are actually available;
the filled article/order case is separately covered by the homepage SSR tests.
Whole-card border intersection ratios were slightly below 1 in four cases, without
failure screenshots or geometry. Do not call this proven rounding or a product
overflow defect. Reader text and actionable links/buttons must be fully visible
after scrolling, within viewport bounds and above mobile navigation. The corrected
new-head browser and required CI results remain necessary before release approval.

The final follow-up was independently reviewed and passed scoped lint, diff and
task checks. Its exact client summary, every card-body paragraph and accessible
control retain full viewport and mobile-nav clearance assertions after one scroll;
geometry is attached before assertions for CI diagnosis. No product-source or
server-launch change was made in this integration follow-up. Latest-head CI is
the remaining technical check; broader editorial and owner publication/release
decisions remain open in this task.
