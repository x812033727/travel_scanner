# S54 R15｜雙讀者敘事合併與政策關卡

2026-10-20 UTC。**R15 正式敘事 13／13 PASS；同版 Jev 政策 PASS。** 這是配音前關卡，不核准 R15 語音、實際插圖、網站手推審核卡或成片。本關卡執行及驗收時 `/workspace/.video-work/curio-s54/STOP` 仍在；本任務沒有重配音或改稿。後續音訊製作者可另依新關卡處理 STOP。

## 凍結輸入

五檔 SHA-256 與 [R15 作者凍結](../r15-author-oral-repair.md)、[獨立史料與書面畫面 PASS](../r15-source-independent.md)一致：`brief.md` `c581e4776448e0945906cf215bf605a3711b126759d8ba419352ba1c59bf3102`；`research.md` `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae`；`claims.md` `734af0adfaedcc25ff052c76a3fc1b18e8ad4e7e79f747facfc9df2f9ede46e9`；`video.json` `37192bb794f6641cc8d181ef92fa7ed9e6ac57e9deba95ddbec696a07128d5f2`；`script.md` `9ff874df7b67045c24fc7bbf000ea2dbba3da0d1c8cfa1280e6311dff4eb0270`。

兩位隔離讀者的 [A 原票](../r15-clean-blind-a/answers.json) SHA `e503167c6ea211d71bce227bfd27ac7c15b4d0b8ec129c06b1f489a00e19b5ee`、[B 原票](../r15-clean-blind-b/answers.json) SHA `d76c40db88b08d723c222ebca9447453400257db114764a8d3a50afc6c426166`；官方單人回條的 `panel_rules_sha256` 都是 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`，`panel_narration_sha256` 都是 `21dcf8b7ce3144b1a35ae148ae546904e3d133b66e4c2e66950ecf9b7e0c91c5`。我重算五檔與兩票雜湊，並用 `panelVerdict` 比對每一票與官方單人回條；沒有改原票。

## 正式合併

[完整合併稽核](merge-audit.json)由官方 `mergePanelVerdicts([A, B])` 的固定 **OR** 規則產出。A 為 13／13 yes；B 在 `payoffs`、`no_detour` 投 no，其餘 11 題 yes。B 的兩項異議及行號都保留在稽核中：開場信件秤重的問題沒有點名回收，以及三句主管報告像連續清單。由於每題至少一位讀者給有行號的 yes，合併為 **13／13 yes、0 required fail、0 advisory fail**。這是既定雙讀者規則，沒有將 B 的原票改成 yes。

[合併答案](merged-answers.json)交給 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r15-merge-policy/merged-answers.json --json`，官方 CLI exit 0；[原樣回條](merged-narrative-cli-receipt.json) SHA-256 `2924e33a717446b7d46d6ae3845c653767661da92e55f5efa9ed37c35d455f64`，round 3、`passed:true`、`failed:[]`、`advisory:[]`。工作目錄的 `review/narrative.json` 已與歸檔回條相同。

## Jev 政策

用同一版完整 `video.json` 與 `brief.md` 的 `policyRequest({doc, brief})` 組 [精確請求](policy-request-body.json)，SHA-256 `4b3f7bb0ab5d4b4b139ea4b9e39e74726859ee7bb31048b99970ff5c4ffd3afd`：旁白 3,537 個字元、站主觀點 72 個字元。只向網站 `/api/video/automation/judge/policy` 送 **一次** POST，HTTP 200；[原樣回覆](policy-response.raw.json) SHA-256 `da08ad643820a77a1e891e8ad8b8e58180a758965c579d6451f2f62124fffae3`，[判定回條](policy-receipt.json) SHA-256 `726815abf29c455500d11ffe812c29251660a1476bb2a88fa6bd71f663a40add`。Jev 解說題組 `passed:true`：立場 0.66、示範不適用、建議 0.01、業配 0.22。

**下一關：**此精確 R15 版可作新的定點 TTS 與完整音檢；R14 的 148 句語音和 17 旗標不能當 R15 PASS。`STOP` 需由音訊製作者按新關卡與舊 ledger 審慎處理。網站手推音訊卡及站主實際聽辨仍以現況為準。
