# S05 R20：雙讀者裁決、正式收據與委派劇本關卡

2026-10-19。本文只對 `script.md` SHA-256 `707fddeac7f72fae577bbcff087eab8f0390203588ff0f883f5a7ed8e12a9eb8`、`video.json` SHA-256 `68a06d6a13676b517309d6e96c49e121ca7d170bafee4fb21f3429c8a19f2136` 生效。盲讀隔離、98/98 句來源覆核、90/90 景逐句對照、lint 0 errors／0 warnings 的細節在 [`verify-15.md`](verify-15.md)。

## 正式敘事收據

- Panel A 純劇本盲讀：必答 **9/12**；`no_spoiler`、`chapters_link`、`payoffs` 為否，參考題 `chapters_are_events` 亦否。[可讀副本](blind-20-panel-a.md)；[原始封存壓縮檔](blind-20-panel-a.md.gz) 解開後 SHA-256 `08b6625c244719ab89575a5dc1d4c37f989203f3cbf3b75ad65e336a1e183ab3`。
- Panel B 另一名純劇本盲讀者：必答 **12/12**，參考題亦是。[可讀副本](blind-20-panel-b.md)；[原始封存壓縮檔](blind-20-panel-b.md.gz) 解開後 SHA-256 `5e067cfa2946df823517e7b3ca26eb9b9692c356ae26ad8d0635e8e636c50a58`。B 的原判詞和聽眾理解問答沒有被改寫；[`blind-20-panel-b.json`](blind-20-panel-b.json) 只把原判詞各題的真實逐句引證轉成 CLI 所需的 `[eg...]` 括號格式。

兩份可讀副本只去掉原始 Markdown 換行尾端的兩個空格，以通過儲存庫格式檢查；逐字原始位元組在 `.md.gz`，以 `gzip -cd <檔案> | sha256sum` 可重算上列封存雜湊。A／B 的實際判分和引證文字都沒有改動。
- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s05 --answers docs/videos/curio-s05/blind-20-panel-b.json --json` 寫入 `/workspace/.video-work/curio-s05/review/narrative.json` **round 23**：`passed: true`，12 個必答 `yes`，參考題 `yes`，`failed: []`、`advisory: []`；收據 `narrative_hash` 為 `ddcca55181535b25`。這是 **B 單人正式收據**，不是捏造 A 全過；A 的三項必答否決仍如上保留。依系列同題須兩名獨立讀者都否才退稿的規則，這輪沒有共同否決，編輯裁決為通過。

## 劇本送審與委派核准

以正確的媒體工作根 `/workspace/.video-work` 呼叫 `review-push --slug curio-s05 --gate script`，網站回報已送審、狀態 `pending`。隨後 `approve --slug curio-s05 --gate script` 對上列精確 `script.md` SHA-256 寫入本機委派核准，時間 `2026-10-19T23:49:57.939Z`。核准註記引用站主先前「以你推薦的就好不用問我」的製作委派、A／B 真實分數與雙讀者準則，並明說**站主未親自讀此稿**。網站送審的 `pending` 與本機委派核准是兩個各自記錄的狀態，不冒充網站已由站主點選同意。

## 旁白階段

現有舊版 `timeline.json`、`review/check.json` 與十個舊 flag 均不屬 R20，不作本輪通過證據或重錄清單。以正確工作根的 `tts --dry-run` 報價：94 個請求、其中 8 個需新合成、約 239 個計費字元；全片文字共 2,373 字元，頻道聲音 `gemini:Sulafat` 已可用。S38 正在使用同一 TTS 供應端，本輪 S05 的實際合成待其結束後啟動。音訊關卡尚未核准，也沒有聲稱站主親耳聽過。
