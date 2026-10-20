---
id: 2026-10-20-curio-s33-hunminjeongeum-story
title: Produce sourced Curio S33 Hunminjeongeum story
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s33-history
claimed_at: 2026-10-20T05:59:50Z
created_at: 2026-10-20T05:59:50Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s33
---

# Produce sourced Curio S33 Hunminjeongeum story

## Why

S35 郵寄兒童題材缺可重開的一手個案；S33 的《世宗實錄》則有可固定的 1443、1444、1446 原文。依站主延續歷史系列的授權，製作以崔萬理奏疏與世宗回應為主線的下一支來源可查影片。這張票只認領 `docs/videos/curio-s33/**`，不動 S01／S09／S18 或共用題庫。

## Definition of done

- [ ] 固定原文與逐項譯解、史料限制寫入研究與 claims；區分「是月」和真正逐日紀錄。
- [ ] 兩個方案的企劃、推薦版至少八分鐘正文劇本；每句可回查來源，獨立讀者盲讀結案。
- [ ] 站台企劃及劇本 gate 如實保持手動；未經實際核准不配音、不購圖。
- [ ] 只提交本票檔案和 task 交接；若 gate 未完成，記清後續動作而不虛稱交付影片。

## Steps

- [x] 核題目、認領及來源可達性；來源固定 commit `96b837bb84afad9b038c5322d8720d33b0dc9363`。
- [x] 摘出 1443 創制、1444 奏疏／回應與次日處置、1446 成書及年底考試的原文，寫 research/claims。
- [x] 企劃與推薦版劇本、開場濃縮、鉤子、插圖對應及片頭片尾設計（候選稿，尚待獨立覆核和站主核准）。
- [ ] 逐句史料覆核與雙讀者盲讀；任何錯誤先修稿再綁定新 SHA。
- [ ] 如來源、前製通過，送真實後台 gate 等站主；付費媒體仍停在核准後。

## How to verify

重開 research 所列固定 GitHub XML，對照 SHA-256；檢 `claims.md` 中每一件可核對事實與 `script.md`；`npm run tasks -- check`，視定稿形式跑 `node tools/video/cli.mjs lint --slug curio-s33` 與 `narrative`。站台 `review-pull` 只接受實際批准。

## Notes

第三方 GitHub 鏡像 README 自述源於韓國國史編纂委員會 2022-11-03 原文資料；政府原站在本雲端未開，不能聲稱核過原始掃描。XML 結構含原文、韓文編輯標題、實錄卷頁；`是月` 條目不可換成一天。崔萬理「等」只是具名奏疏者，不是朝廷全員；奏疏的動機與世宗御製序中的理由要分開歸屬。

2026-10-20 候選稿：`video.json` 93 景／87 插圖／5 引文卡、95 句、`lint` 0 errors、3 個視覺提詞重複 warnings，估 9.7 分鐘；一讀逐句史料收據見 `docs/videos/curio-s33/verify-1.md`。封存劇本 SHA-256 `8e7b24833ce37cb20df3999034a6eac14c62307963aabd6773d9fb9356aeabdb`、claims SHA `9f15f85fc27e881c1967506d1814338d9da3e4c15b205c9d8c888e870e548aed`。下一步：獨立劇本盲讀＋史料二讀；修訂後重新 lint 與記錄新 SHA，再送 outline/script 真實後台 gate。尚無 gate 核准，不可 TTS 或購圖。
