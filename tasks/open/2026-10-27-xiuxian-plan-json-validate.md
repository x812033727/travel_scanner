---
id: 2026-10-27-xiuxian-plan-json-validate
title: 修仙獎勵企劃包 JSON 化與 validate
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-27T23:39:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/xiuxian-jiangli
---

# 修仙獎勵企劃包 JSON 化與 validate

## Why

《種田娶妻打天下》的企劃包是 `setting.json`、`outline.json`、`season-NN.json` 加 `validate.mjs`、`build.mjs`，規則用程式擋（三個鉤子不同、結尾類型不重複、主角不連輸、連續四集收線）。修仙獎勵的六篇現在是手寫 Markdown（`chapter-01.md` 到 `chapter-06.md`），規則靠人看。要擴充（插篇章）或讓多個模型同時寫下一季時，JSON 化加檢查才不會散。

## Definition of done

- [ ] `setting.json`、`outline.json`、`season-01.json` 照《種田》的欄位轉過去，Markdown 改由 `build.mjs` 產生
- [ ] `validate.mjs` 零錯誤：每集三個不同鉤子、相鄰結尾類型不重複、篇末反轉、主角不連輸、連續四集至少一個 payoff、短線先 setup 才 payoff
- [ ] `npm run test:docs-videos` 仍過

## How to verify

`node docs/videos/series-plans/xiuxian-jiangli/validate.mjs`、`build.mjs --check`。

## Notes for the next person

不急；第 1 集小樣與第 2–12 集分鏡先。轉的時候別改劇情，只改形狀。
