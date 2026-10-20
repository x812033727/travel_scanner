---
id: 2026-10-20-curio-s33-hunminjeongeum-story
title: Produce sourced Curio S33 Hunminjeongeum story
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T05:59:50Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s33
---

# Produce sourced Curio S33 Hunminjeongeum story

## Why

S35 郵寄兒童題材缺可重開的一手個案；S33 的《世宗實錄》則有可固定的 1443、1444、1446 原文。依站主延續歷史系列的授權，製作以崔萬理奏疏與世宗回應為主線的下一支來源可查影片。這張票只認領 `docs/videos/curio-s33/**`，不動 S01／S09／S18 或共用題庫。

## Definition of done

- [x] 固定原文與逐項譯解、史料限制寫入研究與 claims；區分「是月」和真正逐日紀錄。
- [x] 兩個方案的企劃、推薦版至少八分鐘正文劇本；每句可回查來源，獨立讀者盲讀結案。
- [x] 站台企劃及劇本 gate 如實保持手動；未經實際核准不配音、不購圖。
- [x] 只提交本票檔案和 task 交接；若 gate 未完成，記清後續動作而不虛稱交付影片。

## Steps

- [x] 核題目、認領及來源可達性；來源固定 commit `96b837bb84afad9b038c5322d8720d33b0dc9363`。
- [x] 摘出 1443 創制、1444 奏疏／回應與次日處置、1446 成書及年底考試的原文，寫 research/claims。
- [x] 企劃與推薦版劇本、開場濃縮、鉤子、插圖對應及片頭片尾設計（候選稿，尚待獨立覆核和站主核准）。
- [x] 逐句史料覆核與雙讀者盲讀；任何錯誤先修稿再綁定新 SHA。
- [x] 如來源、前製通過，送真實後台 gate 等站主；付費媒體仍停在核准後。

## How to verify

重開 research 所列固定 GitHub XML，對照 SHA-256；檢 `claims.md` 中每一件可核對事實與 `script.md`；`npm run tasks -- check`，視定稿形式跑 `node tools/video/cli.mjs lint --slug curio-s33` 與 `narrative`。站台 `review-pull` 只接受實際批准。

## Notes

第三方 GitHub 鏡像 README 自述源於韓國國史編纂委員會 2022-11-03 原文資料；政府原站在本雲端未開，不能聲稱核過原始掃描。XML 結構含原文、韓文編輯標題、實錄卷頁；`是月` 條目不可換成一天。崔萬理「等」只是具名奏疏者，不是朝廷全員；奏疏的動機與世宗御製序中的理由要分開歸屬。

2026-10-20 前製定稿：`video.json` 93 景／87 插圖提詞／5 引文卡、95 句、`lint` 0 errors、3 個視覺提詞重複 warnings，估 9.8 分鐘。逐句史料一讀、獨立原文二讀及每輪差分見 `docs/videos/curio-s33/verify-1.md` 與其連結收據；最新 `script.md` SHA-256 `3db98a782e552385def131784e1dc4c8096e2bceb36e10e58cb75a277e004815`、`claims.md` `496caad73962337fbc9b18640f8f1cdf276dbd210af3af90432d3b8451807581`、`video.json` `f88c9269709a34272a58ccc6bb59bdacf1b417d0a95e10c8bcb99ab6b4f572ef`。最新兩位隔離讀者 R6 11/13、R7 13/13；依系列規則沒有兩人同判 No 的題目，保留編輯判斷見 `verify-r6-r7-editorial.md`。

已透過 `review-push` 送出真實 `outline` 與 `script` 卡片；新版 `brief.md` SHA-256 `b1cfc6aff2db4cf64a4f3e3fa1784d929d97f5a441ee23328101bf0c81f946a2` 有可被後台識別的 A／B 兩個選項，前一次零選項提卡另有較舊雜湊，審核應以新版為準。Jev 建議 A，但本機手動推送仍由站主在 `/admin/videos` 決定；`review-pull --gate outline`、`--gate script` 均回 exit 3 `waiting for the owner`。尚無站主實際核准，**不可**把 Jev 建議當成站主批准，也未 TTS 或購圖。`docs/videos/curio-s33/handover.md` 記下一步。

### 2026-10-20 13:25 UTC 接續狀態

後台已在 08:37:51.658928Z **真實選擇 A**（對上表 `brief.md` exact SHA），08:37:55.235935Z 真實核准當時的 R7 `script.md` SHA `3db98a782e552385def131784e1dc4c8096e2bceb36e10e58cb75a277e004815`；13:22 UTC 本機 `review-pull` 兩關均回 exit 0，回條存在 `/workspace/.video-work/curio-s33/approvals.json`。這是舊稿的站主核准，並非其後新版的核准。

配音前對 R7 exact script 做一次 Jev 政策預檢，業配 0.36 > 0.30、**FAIL**。只把片尾 `hj999c` 訂閱口播改成提示說明欄的《世宗實錄》原文連結，原片尾訂閱圖形保留；R8 `script.md` SHA `1a1d52712593055ed5d427696b273bdc7cf28de7736ef90c5ee98a0431a3556e`、`video.json` `e0d7fed0c81ce7db2ff2a971e177d4fdef831d5bea5afe6523804f9d8ad965ae`、`claims.md` `2f38d279e7eb2d6b34584c9ed853e3de1efd695a6d5a87921685d5c116e68fd0`。R8 一次新政策預檢 **PASS**（立場 0.86、建議 0.01、業配 0.01）；`lint` 0 errors、4 warnings。作者差分見 `docs/videos/curio-s33/verify-r8-source-delta.md`，另一人獨立史料／書面畫面差分 `/tmp/s33-r8-root-independent-source-visual.md` **PASS**。

R8 尚待兩名**全新**盲讀者對同一 SHA 完成正式 13 題敘事檢查，再如實送站台新版 `script` 卡片；R7 站台核准已因 SHA 改變失效。使用者授權採推薦決定，符合前置查核後可另記**本機代決**精確 R8 劇本以繼續語音，惟不可冒稱站台對 R8 真實核准。`tts --dry-run` 的 95 句、約 2,327 Gemini 計費字及 `keyframes --dry-run` 的 87 圖、三次嘗試最高約 US$3.52 都只讀報價；截至此節**沒有實際 TTS／購圖／配樂**。R8 後續需全句音質檢查、正文實際 ≥8 分鐘、原生插圖 pilot 與開場濃縮／片頭片尾 QA。

### 2026-10-20 R10 最新狀態

上段為當時快照。R8 後續兩位新盲讀者同判 `no_recap` **No**；R9 刪重、補來源中的答辯，另一人來源與書面畫面差分 PASS，但兩位再換新的盲讀者同判 `payoffs` **No**，因開場追問二月十六日至二十日**精確上書時機的原因**，史料只能給先後和反對理由。R10 只把這題改問反對後新字是否仍用於選官，`hj086` 以 1446 年吏員試《訓民正音》的王命明點回收；`hj019` 同時改成下一句能回答的「事大」規矩。精確五檔 SHA、來源界線與驗證見 `docs/videos/curio-s33/verify-r10-source-delta.md`。`lint` 0 errors、95/95 主張逐字對應、開場估 44 秒、正文 1,916 漢字。R10 **待獨立差分及兩名全新盲讀者**；R7 網站劇本核准對 R10 已失效，R9 政策 PASS 也不當成 R10 收據。仍無付費語音或插圖。

### 2026-10-20 14:25 UTC 音訊硬停點

上段 R10 待審狀態已更新：獨立來源差分 PASS、兩名全新讀者合併 PASS（A 對 `payoffs` 一項 No 保留）、R10 exact Jev 政策 PASS；網站新版劇本卡 `hand_pushed` pending，本機代決 exact 劇本已如實標 `LOCAL DELEGATED`。98 句頻道語音全部合成，11 句語意風險各補錄一次；實測正文 **9:41.533**。完整音檢先 35 旗標、後 **32 旗標**，不能當作旁白通過。所有精確時間、雜湊、兩次原始 check/flags、風險分級見 `docs/videos/curio-s33/verify-r10-audio.md`。未送 audio gate、未購 MiniMax 圖或配樂；三景 pilot 計畫與整集 US$3.65 上限已寫，但音質零旗標前不開畫。後續須獨立第二轉錄或實聽辨認剩餘旗標，再對確實讀錯的句子作定點修復。
