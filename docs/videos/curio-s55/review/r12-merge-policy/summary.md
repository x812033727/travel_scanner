# S55 R12｜正式雙讀者合併與政策關卡

2026-10-20 UTC。**獨立來源／書面畫面 PASS、正式敘事 13／13 PASS、同版 Jev 政策 PASS。** 這是語音開工前關卡，不代表 R12 旁白、實際插圖、網站手推審核卡或成片通過；本任務沒有改稿或生成媒體。

## 精確輸入

五檔 SHA-256 與 [R12 作者凍結](../r12-author-source-fix.md)及[獨立來源／書面畫面覆核](../r12-source-independent.md)一致：`brief.md` `c1f45453a7b13de1857a192b4c64571bbf1fce7cf12943a48a2369c829e04070`；`research.md` `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb`；`claims.md` `317c50ab5142b13cf097cbc09a45a128068a6b27dd478f8a130f54a25c64409f`；`video.json` `5aac04b0f097c9c5611874a946dc73d963a00109489a3ed361e5fb20953c119a`；`script.md` `4a36cef7c4ba278089cb8fc49398a4470bb288822d6a59ab73794e8323b5b38a`。本版 lint 為 **0 errors／0 warnings**。

兩份隔離[讀者 A 原票](../r12-clean-blind-a/answers.json) SHA `801244a5282c582d9765c3409a894eacbe9325caa7321fea2e1772221df7e672` 與[讀者 B 原票](../r12-clean-blind-b/answers.json) SHA `a742680d5aa99b05b8752e6b6437aa689dd7d659ff6f0d4e584a0ca543042af6` 均對應同一個 `script_hash=104f4186e4291874e9687fac1c2f54db9ae9ff6b19072239d70c4feb5e99f7c6`、規則 SHA `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、旁白 SHA `db2be9b5040889541b28851ad3472a1939b33d8f49ad02b94066fe503530e38d`。原票逐題與各自官方 CLI 回條對齊。

## 正式合併

[稽核檔](merge-audit.json)由正式 `mergePanelVerdicts([A, B])` 的固定 **OR** 規則產出，SHA `390ebcd4af0e46ca95e6ed08268594401bbd6fcb06bb7cc2491e53631045cc02`。A 對 `no_recap` 投 no：`s55124` 再述冷卻與緩降；B 對 `no_detour` 投 no：`s55041` 的科學院資助旁支。兩票異議各自保留，沒有改寫成 yes。其餘題均由兩位投 yes，因此逐題合併為 **13／13 yes**、沒有 required 或 advisory failure。

[合併答案](merged-answers.json) SHA `6e3515a43d0b29f4a8132a2ee04ff775614cb77cc6333bc70c2ef5ce3392ae31` 經正式 `narrative --slug curio-s55 --answers .../merged-answers.json --json` 判 **PASS**，exit 0；[CLI 原樣輸出](merged-narrative-cli-receipt.json) SHA `2e4012b4baa252b43ac991f91b77fabe7ebe6f2123e4e39cf0462b639c93dbc3`。同時保存[工作目錄官方紀錄](official-narrative-record.json) SHA `1e117643cae1b8401dae4f50aa810aaa585eddc7c3c566d5c8d231f8a9e4dc1b`，`round=1`、`passed:true`、`failed:[]`、`advisory:[]`，仍綁同一規則與旁白 SHA。

## Jev 政策

同版完整 `video.json` 與 `brief.md` 組成 `policyRequest({doc, brief})`：[精確傳送請求](policy-request-body.json) SHA `c7e7bb9976fa3c6d03e66003f764796577ee180fb327eddd05afbf61eb7af78b`，旁白與觀點字數見[去憑證中繼資料](policy-request-meta.json)。網站 `/api/video/automation/judge/policy` **只送一次** POST，HTTP 200；[原樣回覆](policy-response.raw.json) SHA `2bae7b7d8abb446c916e6482282205fca47039328a98609b7d3491757f6e99f1`，[判定回條](policy-receipt.json) SHA `5e9991546e6476ef2d71f820723df67ca864cb7fd851d7059c6feea3334d5c33`。網站使用 `explainer` 題組，`passed:true`：立場 0.69、示範不適用、建議 0.01、業配 0.16。

**下一關：**本精確 R12 版可做定點 TTS 與完整 140 句音檢。R10 的 14 句殘餘旗標與舊稿音檔不構成 R12 音訊 PASS；音訊製作者須記錄新版快取命中、重錄範圍及完整檢查。網站手推審核卡與站主實際聽辨仍按現況處理。
