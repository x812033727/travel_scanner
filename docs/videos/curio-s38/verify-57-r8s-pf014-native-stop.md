# S38 R8s｜PF014 原生試畫：黑寬帶退件，STOP

2026-10-22 UTC。依 [R8s 獨立書面 PASS](verify-56-r8s-fallback-independent.md)，只對 `pf014` 跑一次原生試畫。**未裁切 1280×720 原生 JPEG 人工 REJECT；PF014 仍 HOLD。** PF009／PF013 已改為日記引句卡，本輪沒有再為它們購圖；PF015–022 和其他未畫鏡頭也沒有生成。

## 原圖驗收

新 PF014 未裁切原圖 SHA-256 **`52c1c81d51bba9930a242af9ae0bd322485eb038cdf6b32ff8c65a2e67d3a237`**；所選裁邊版 SHA-256 **`a3a93714832b2f84c205739dd570d78e243fe5f79e962a05dff1f3b8fd833bf8`**。兩張均已直接以原解析度打開。

一名成年漫畫人物在高處石欄前雙手抓欄、面帶擔憂，背景有大片煙柱和遠處屋頂；它能作「佩皮斯在塔上掛念橋邊熟人」的概念示意，沒有把 Michell 家已燒提前畫成確證，也沒有 Tower Bridge 輪廓。人物與場景大致合系列卡通語法。但**原圖頂部和底部有連續黑色 letterbox 寬帶**；裁邊版把黑帶切掉，無法改變未裁切原圖的滿框失敗。機器亦判 **9.71/10 FAIL**，唯一列出的 `frame` 問題正是上下黑帶。故不能因高分、來源安全或裁邊效果把這張收為 KEEP。

## 有界執行、帳本與圖單

私有前備份在 `/workspace/.video-work/curio-s38/review/r8s-pf014-pre/`，含 STOP、ledger、manifest、舊 PF014 原圖／裁圖及九張 KEEP entry 基線。只在 EXIT trap 期間暫解 STOP，執行 `NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work PLAYWRIGHT_BROWSERS_PATH=/workspace/.video-work/playwright-system node tools/video/cli.mjs keyframes --slug curio-s38 --shot pf014 --takes 1`，無 `--force` 或 seed offset。執行日誌及退出碼私存 `review/r8s-pf014-native.log`／`review/r8s-pf014-native.exit`，SHA-256 `6952dc454161b12661adcf4460260143b8dcedbc5abe9812f9bcf83a9c290fce`／`4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`；**exit 1** 是圖片內容關卡 `needs_review=true`。後狀態備份在 `review/r8s-pf014-post/`。STOP 已恢復在位。

Ledger 從 **US$0.5695／37 image／36 judge／1 music** 增至 **US$0.5830／38 image／37 judge／1 music**，恰只增一張 US$0.0035 image 和一次 US$0.01 judge，合計 **US$0.0135**；舊 PF003 US$0.0035 reservation 未動，仍低於整集 **US$4.58** 硬上限。新 ledger SHA-256 `660db85effcba9197da0b1b3802ca05cab2a54a4950103f848139498c4df35ea`。新 manifest SHA-256 `3da69280990b2639f2efdc657f55b3a3239f5fbab64cb478412379fc554f118d`，只列九張沿用的 KEEP 圖與新 PF014；九張 KEEP manifest entries 及各所選檔案 SHA 與批前逐項相同。PF014 request key 由舊運鏡的 `7c46410b56e9e8dc` 轉為新運鏡的 `e6af2b6a3ed4d84f`，新 shot 只有一個 take、`judge.passed=false`、`needs_review=true`。

R8s `video.json` SHA-256 仍為 `f3f49ce1fdd64ac11189dbe8b64bb7bc486e4c03566795a500f9f8b636f3de34`；`script.md`／`claims.md` 仍為 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`／`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。日記卡的**書面 PASS** 仍有效；本張原圖則明確 HOLD。未追加第二張或啟動更大批次。

後續任務邊界見 [verify-58-r8s-pf014-next-task.md](verify-58-r8s-pf014-next-task.md)。
