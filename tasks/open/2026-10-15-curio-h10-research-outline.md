---
id: 2026-10-15-curio-h10-research-outline
title: Prepare Curio H10 Franklin source refresh and outline choices
status: in-progress
priority: P2
area: docs
owner: codex-curio-h10-h11-scripts
claimed_at: 2026-10-15T23:53:03Z
created_at: 2026-10-15T16:33:45Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-h10
---

# Prepare Curio H10 Franklin source refresh and outline choices

## Why

使用者要求接續製作五集奇聞檔案局。H10 富蘭克林遠征需要更新來源、兩個可選的完整大綱及主張邊界，交站主與獨立審核員一起檢視；本任務只處理 H10 前製。

## Definition of done

- [x] research.md 登錄 2026-10-16 實際打開的來源與限制。
- [x] claims.md 可將兩案重要敘述對回來源，修正 4 月 25 日所記「明日 26 日」南行計畫。
- [x] brief.md 提供 A／B、可朗讀 30–60 秒開場、六章、3–5 轉折、loops 與結尾新資訊。
- [x] 獨立審核員讀回修正版；大綱層級通過，非正式劇本十三題通過。
- [x] 完成獨立覆核與手動 outline 送審交接，後台讀回 pending。
- [x] 原版與補格式版均讀回站主選 A；本集 US$6／本批 US$30 估算停手上限已核准。
- [x] 延伸完成本機 A 案 video.json、script.md、逐句來源、loops 與作者檢查。
- [ ] 正式劇本通過獨立史料與十三題覆核後，交站主核准。

## Steps

- [x] 閱讀現行 curio-episode／youtube-video／script-writing，參考 H01-v2 前 30 景與 H09 brief。
- [x] 唯讀參考 949bb91fc 題庫，重開 Parks Canada、加拿大歷史博物館、Waterloo 與原始研究來源。
- [x] 補入 2024 Fitzjames 身分研究與 2024–2025 官方成果背景。
- [x] 按獨立覆核意見，把開場物件清單改成可朗讀場景和三個未揭曉行動時刻。
- [x] 大綱階段送審後曾釋出票；當時尚無 video.json、未啟動付費工人。

## How to verify

`git diff --check`；`npm run check:tasks`；逐一讀 research.md、claims.md、brief.md 的交叉引用、六章時長和 loops；核對開場朗讀量為 30–60 秒。正式稿增加 `node tools/video/cli.mjs lint --slug curio-h10 --json`、逐句映射／來源 ID／SHA 檢查；音訊與獨立敘事 QA 尚未通過。

## Notes — 大綱前階段歷史（目前狀態見下方正式稿交接）

工作樹為 curio-next-five，base a77a9416d。此 task 的 UTC 產生日期為 10/15，文件查核日採 Asia/Taipei 10/16。H10 九個採用來源均取得正文或指定專節；主線不加入血腥遺骸、食人畫面或死因排行榜。共同預算為每集 US$6／五集 US$30 估算停手提案，尚未授權；本任務實際外部付費 US$0，未啟動付費工人、未推送。獨立覆核者 curio_h12_m09_planning 已確認主要史實並讀回開場修訂，無剩餘阻擋項。凍結 brief SHA-256：725991c44d9129668377c291efd0aa8edfc9306635abe551c6fc2616397e45ff。git diff --check 與 check:tasks 通過（1895 票；既有長期認領／scope 警告保留）。

2026-10-16 01:01（Asia/Taipei），主代理完成五集手動 outline 送審並讀回 pending；H10 review ID：`72a82580-0901-476f-b0b6-e7ddfa30e7c5`，對應上述最新 brief SHA。獨立覆核與送審交接完成，釋出認領但不標 done。下一位接手者須先讀回站主 A／B 選擇及本批 US$30 明確授權；目前兩者均未核准。送審卡未啟動付費製作。已送審 brief 維持原樣，由主代理統一 commit／PR。

## 2026-10-16 正式稿交接（目前狀態）

原版及補格式版 A 均已核准，收據見 `docs/videos/curio-next-five-20261016/decision-20261016.json`、`format-decision-20261016.json`。本集 US$6／五集 US$30 已授權，本作者尚未付費。原 research-outline 任務延伸正式稿，owner 保持 `codex-curio-h10-h11-scripts`，保留 claim 供盲評修稿，不另開重疊票。

video SHA-256 `e11a22a7a29086a06a8261943cd3e78bea6775223705cb3eab9b8dbdffa1a559`；brief `ab081206f4055046c18b7a89016f05c9f885aa6bdd37ea3c2e2c661f2d74aa0d`。82 句，文字時間軸估算 9.75 分鐘；純口播估算 502.56 秒。lint 0 errors／2 warnings，詳見 `script-validation.json`。完整正文、逐句來源、loops、估時與作者十三題自檢均在本集目錄。

兩個提示詞 warning 為 historical／modern 時代描述；已記錄場景實際變化，不以同義字消除警告。待獨立正式稿覆核及站主劇本核准；未送劇本後台、未配音、未產圖、未發布。

本輪 `git diff --check`、逐句／來源／SHA 一致性檢查通過；`npm run check:tasks` 通過，驗證 1895 票，保留其他任務既有長期認領／重疊警告。作者收據並不充當盲評。

## 2026-10-16 第一輪敘事退修

獨立盲評未過：chapters_link, payoffs, no_detour。已完成第 1 輪結構修訂，原答案保留在 `narrative-round1.json`，逐項回應在 `narrative-revision-1.md`。新版 video SHA `58e37c2eb2bc8190ba16aa4b9dc5050397819a12e263b29cf3a0641dba7c306b`；80 句，估算 9.60 分。lint 0 errors／2 warnings；未標 narrative pass。提交後釋出認領，供獨立事實覆核接手。無後台劇本送審、無付費呼叫。

第 1 輪修訂驗證：逐句文字及時間軸句序、主張／來源 ID、video／brief SHA 一致；`git diff --check` 與 `npm run check:tasks` 通過（1895 票，只有其他既有認領警告）。
