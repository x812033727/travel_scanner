---
id: 2026-11-06-ci-docs-only-and-selftest
title: CI 減量：只改文件時跳過 e2e／容器／整站測試，加上推送前自測 selftest
status: review
priority: P1
area: meta
owner: claude-opus-5.5
claimed_at: 2026-11-06T05:59:17Z
created_at: 2026-11-06T05:58:40Z
completed_at:
branch: claude/ci-docs-only-selftest
depends_on: []
scope:
  - .github/workflows/ci.yml
  - .github/workflows/seo-audit.yml
  - .github/workflows/planner-premium.yml
  - .github/workflows/travel-discovery.yml
  - .github/workflows/food-map-reservations.yml
  - .github/BRANCH_PROTECTION.md
  - tools/selftest.mjs
  - tools/selftest.test.mjs
  - package.json
  - AGENTS.md
---

# CI 減量：只改文件時跳過 e2e／容器／整站測試，加上推送前自測 selftest

## Why

站主 2026-11-06 想把 repo 改成私有，私有庫的 GitHub Actions 每月只有 2,000 分鐘（Pro 3,000）。
量 11-03 到 11-06 三天：約 19,000 計費分鐘（每月約 19 萬）。CI 一次約 105 分鐘（十幾個分片、每個 job
無條件進位到分鐘），SEO 16、Food map 6、Planner 5、Travel discovery 5。最近 60 個合併的 PR 有 21 個只改
docs/ 或 tasks/（劇本、分鏡、企劃），卻照跑全部。

## Definition of done

- [x] 只改 docs/、tasks/、根目錄 .md 的 PR：CI 跳過 web-e2e、containers、full-stack-smoke，SEO／Planner／
      Travel discovery／Food map 不啟動；必要檢查照樣是綠的。
- [x] `npm run selftest`：依 diff 在本機跑該跑的檢查，說出哪些只有 CI 能跑，`--mark` 回報 commit 狀態。
- [ ] 合併後第一個只改文件的 PR 實際看到四個必要檢查都過、略過的 job 是 skipped。

## Steps

- [x] tools/selftest.mjs（isDocsOnly、planChecks）與測試。
- [x] ci.yml `changes` job、三個 job 的 if、web 閘門只在 docs_only 時接受 skipped 的 web-e2e。
- [x] 四支非必要 workflow 加 paths-ignore。
- [x] AGENTS.md、BRANCH_PROTECTION.md、package.json。

## How to verify

`node --test tools/selftest.test.mjs`；`npm run selftest -- --dry-run`；開一個只改 docs/ 的 PR 看 checks。

## Notes

- 單元測試**不能**因為只改文件就跳過：api 測試、vitest、tools、docs-videos 都會讀 docs/videos。能跳過的只有
  不讀 docs 的：Playwright（spec 不讀 docs）、容器（.dockerignore 排除 docs）、full-stack-smoke。
- 估計省下：只改文件的 PR 約省 71／137 分鐘（約五成），乘上約三成五的比例，總量約省一成五到兩成，不是三成。
- `changes` 失敗時 docs_only 是空字串，各 job 的 if 寫成 `!= 'true'` 所以會照跑；web 閘門要求 changes 成功。
- 光靠這個到不了 2,000 分鐘；轉私有前還要自架 runner（或把分片合併、e2e 改每日一次），另開票處理。
