---
id: 2026-10-15-curio-h10-research-outline
title: Prepare Curio H10 Franklin source refresh and outline choices
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-h10-freshness-coda
claimed_at: 2026-10-16T01:18:26Z
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

## 2026-10-16 獨立正式劇本史料查核

查核員 `codex-gpt6-h10-h11-fact` 對版號 SHA-256 `58E37C2EB2BC8190BA16AA4B9DC5050397819A12E263B29CF3A0641DBA7C306B` 完成逐句、逐景資料與上架文字查核；[verify-1.md](../../docs/videos/curio-h10/verify-1.md) 記錄全部 80 句／78 景、來源、存取限制及聽眾檢查。沒有史實修改或未解主張，lint 0 errors／2 視覺提示詞 warnings。嚴格敘事盲評仍指出 `h3369d03` 的搜尋位置問句缺少具體回收，因此**正式劇本尚不得送審**。此收據只覆核當前 SHA；修文後要重新綁定新 SHA 並至少定向重查變動句。未送後台、未付費。

## 2026-10-16 第二輪敘事退修

第二輪嚴格盲評 11／12 項必答通過，唯一未過 `payoffs`：`h3369d03` 把因紐特口述直接問成下一次海底搜尋位置，`h725fbb3` 卻說 2014 年岸上零件使隊伍改位。原評審答案保存於 `narrative-round2.json`；作者只做最後一輪定向修訂，詳見 `narrative-revision-2.md`。新版 video SHA-256 `236e94b49168e52e57f6c063c9cd377fdf2086cc91fb0907932a3d13fc3389ac`。兩句旁白改為把口述界定範圍與岸上物件導致改位分開，loop 由 `h725fbb3` 回收；80 句、估時 9.615 分，lint 0 errors／原有視覺警告 2。`script.md`、逐句主張與估時已跟版；未將作者修文當成盲評通過，舊 `verify-1.md` 仍綁舊 SHA，須獨立重查變動句並重做嚴格盲評。尚未送後台劇本、未付款。

## 2026-10-16 獨立史料第 2 輪與新鮮度 HOLD

獨立新查核員 `codex-gpt6-h10-fact-round2` 對 SHA-256 `236E94B49168E52E57F6C063C9CD377FDF2086CC91FB0907932A3D13FC3389AC` 完成兩句改稿與舊版 78 個已確認主張中固定種子抽樣 26 句（含兩句改稿）的直接原始頁複查，26／26 可支持、事實修文 0。完整來源、HTTP 200 讀回、逐句表與聽眾檢查見 [verify-2.md](../../docs/videos/curio-h10/verify-2.md)。

另找到 [University of Waterloo 2026-05-06 發布](https://uwaterloo.ca/news/media/dna-matches-identify-four-more-sailors-franklin-expedition)：再辨認四名船員，累計六名。現有結尾仍以 2024 Fitzjames 作最後新資訊；台詞沒有直接錯誤，但對 2026-10-16 的資料查核標示而言有近況缺口。**正式劇本史料關卡 HOLD，不送站主劇本核准。**本查核員只建議於 Fitzjames 回收後加很短的 2026 身分研究後記並同步來源／說明；不自行改稿。後續改字應綁新 SHA 重查事實與敘事盲評，必要時重走 brief 核准。本輪未付費、未送後台。

## 2026-10-16 身分研究後記修稿

作者 `codex-gpt6-h10-freshness-coda` 依獨立查核的新鮮度 HOLD，直接閱讀 Waterloo 2026-05-06 公告，於 2024 Fitzjames 紙條簽名回收之後加兩句短後記：2026 年五月再辨認四名船員、累計六名。原 A 案 brief 完全未動；原劇本 80 句未改字；完整變更與邊界見 [freshness-coda.md](../../docs/videos/curio-h10/freshness-coda.md)。

本版 `video.json` SHA-256 `4EF199C9FC35E0761004A64EF32434EEA483DFAF5B25AC4DB28D0C154C024680`；`script.md` SHA-256 `A4A64B02732D97C9DDB216B2CD42F789D95A0B0ADEB8AB3CE22B3C9CA679E596`。82 句、文字估時 9.829 分；lint 0 errors、2 個既有畫面警告，沒有付費呼叫。**第 2 輪 verify-2 的 HOLD 尚未解除**：須請新的獨立史料查核員做第 3 輪，並由獨立敘事盲評者針對新版劇本重新評分；兩者都通過才由主代理送站主正式劇本核准。本作者不送後台、不開始製作。
