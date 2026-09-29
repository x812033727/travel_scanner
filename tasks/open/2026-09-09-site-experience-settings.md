---
id: 2026-09-09-site-experience-settings
title: Mokaair site experience palettes and managed information pages
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-09T10:58:08Z
completed_at:
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/web/e2e/site-experience.spec.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/e2e/site-pages.spec.ts
  - docs/site-experience.md
---

# Mokaair site experience palettes and managed information pages

## Why

Implement the approved Mokaair frontend, six palettes and managed information pages plan. Preserve the original dirty checkout; work from origin/main 95122362 in an isolated worktree. Policies remain unpublished drafts. The user authorized PR #380 merge on 2026-09-09 after the incomplete manual acceptance was disclosed; deployment and policy publication remain unauthorized.

## Definition of done

- [x] All valid card topics wrap; reading links are grouped; empty detail sections disappear.
- [x] Language is reachable at the top, six palettes share state, existing planner palettes remain selectable.
- [x] Four five-language information documents support draft, preview, CAS, audited publication and revision restoration.
- [x] Safe frontend close/back/focus flows have automated regression coverage and
      historical desktop/mobile evidence from merged #380; the separate manual
      acceptance below remains open.
- [x] Relevant local checks and full CI pass; revalidate any base-branch reconciliation before the authorized merge.

## Steps

- [x] API/revisions/first drafts: hotspot_sources_kaohsiung.
- [x] Theme/root navigation: hotspot_sources_taipei.
- [x] Interaction/planner guards: archive_publication_audit.
- [x] CMS Web, discovery cards, integration, automated verification and PR: root.
- [ ] Built-in-browser manual acceptance on an approved isolated preview: root.

## How to verify

API pytest/Ruff/mypy/migration checks; Web component tests/typecheck/lint/i18n/build; scoped Playwright desktop and Pixel 7 plus built-in browser verification. Never submit production edits or paid provider actions.

## Notes

Task ownership: old review claims overlap this follow-up but their product changes are already on the verified main ancestry: PR 374 (a899437a), 375 (f6ab3d64), 378 (95122362). The task tool's explicit force option was used solely for this completed-work overlap; other owners' task records are not modified. One shared task covers the disjoint subagent file ownership above.

Initial verification: API focused 86 passed / 18 skipped (PostgreSQL-only cases require CI); root CMS/discovery 50 passed; earlier agent-focused theme and interaction suites passed apart from one subsequently fixed mobile focus regression. Production webpack build including TypeScript passed; final overlay integration changed afterward and is included in CI. Full local parallel tests were stopped because available RAM fell below 40 MB; no full-pass claim. A local preview server launch was rejected by the execution policy, so built-in browser palette evidence remains pending. No policies published, no merge or deployment.

Draft PR: https://github.com/x812033727/travel_scanner/pull/380. Follow-up evidence and exact remaining manual acceptance are recorded in docs/site-experience.md. CI-discovered strict types, managed-metadata/root-provider fixtures and admin registry navigation have been corrected. At that earlier checkpoint, current-head CI and approved-preview manual browser verification were both still open; the final code verification follows below.

Code revision 470d16d6 and the documentation-only head 552637d7 are fully green: API 2,805 passed / 15 skipped; Web units 1,445 passed; browser UI 376 passed / 4 skipped; migrations, Ruff, mypy, i18n, TypeScript, lint, build, containers, full-stack, planner and discovery workflows passed. Native multi-entry Back and the admin topbar overlap are fixed and verified. Twelve final-code palette screenshots were inspected. Main d9ef8fcd was incorporated without changing its hotel fixes.

Merge follow-up (2026-09-09): the user explicitly authorized merging PR #380. Reconcile main 73f893a2 (#383) by retaining both browser test lists and regenerating the task board; rerun CI on the combined head before a SHA-guarded merge. This task stays blocked only on the outstanding built-in-browser manual acceptance: an approved isolated preview URL is still needed after local preview startup was rejected by execution policy. No alternative launcher, deployment, policy publication or production mutation is authorized by this merge request. Automatic browser evidence is not a substitute for that manual checklist.

The integrated head 660b55b1 passed all push/PR checks: API 2,847 passed / 15 skipped; Web 1,496 passed; browser UI 410 passed / 4 skipped. Main then advanced to 584dd438 (#381 catalog-review call limits); reconciliation has no application-code conflicts, only the generated task board. Keep that upstream functionality unchanged and gate the combined head on fresh CI before merging. Manual preview acceptance remains blocked, not completed by this merge authorization.

Integration CI on a52ef7a8: all push checks passed. The PR run found two independent failures: a community setup GET /community/me transport ECONNRESET before recovery/deletion assertions, and an existing discovery test's raw "999" substring check falsely matching timestamp microseconds 729996. Relevant community/BFF code was unchanged, and the same-head push full-stack passed. Preserve that original browser failure and rerun unchanged with the next CI. Replace only the erroneous discovery test's text scan with structural private-field/value assertions plus deterministic timestamp/identifier coverage; do not change production serializers or relax publication gates.

### 釋出認領（由站主授權，2026-09-19）

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

程式已隨 PR #380 於 2026-09-09 合併。這張票從那之後以 blocked 狀態持有 scope，擋住 17 張票，原持有者是 codex-site-experience（2026-09-09 認領），所以改回 open。

剩下兩項：前端關閉／返回／焦點流程的回歸測試與桌面／手機瀏覽器證據；在核准的隔離預覽上用內建瀏覽器做人工驗收。人工驗收要站主本人參與，接手前先問站主。

### 2026-09-29 local P1 reconciliation (codex-p1-product)

Claimed for the owner-authorized P1 review. The matching implementation PRs are
merged and no matching open PR or active same-feature implementation was found.
The former broad scopes have been narrowed to this local acceptance work. Forced
claims only bypass historical/shared scope metadata; no other agent application
changes are taken over. No production or cloud-account access is included.

Current local Next production build and TypeScript passed with 348 generated
pages. The earlier blanket claim that regression coverage still needs writing is
stale: `docs/site-experience.md` already records the successful same-document
Back tests, desktop/Pixel 7 and twelve palette screenshots before #380 merged.

The remaining built-in-browser acceptance could not be completed here. CUA
inventory returned no browser surfaces; IAB tab creation returned `Browser is not
available: iab`; Chrome tab creation timed out and reset the kernel. Separately,
automatic approval review rejected starting this completed build on loopback
`127.0.0.1:3317`, returning only `rejected: blocked by policy`. No alternate
launcher or server was used to bypass the rejection. No new rendered-browser
evidence, six-palette manual check or owner visual approval is claimed.

Keep this task open for an available approved isolated preview and the original
manual checklist. Existing automated evidence does not replace it.
