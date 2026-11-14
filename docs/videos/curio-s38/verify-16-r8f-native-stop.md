# S38 R8f｜pf004 單景原生圖停點

2026-10-21 00:19 UTC。**STOP：pf004 首次修詞試畫未過，pf005／pf006 未試；不得續開整集插圖隊列。** 這份收據只記一次指定景的圖像與 judge，沒有變更旁白、劇本、站台核准或其他景提示詞。

## 付費前固定條件

- `video.json` SHA-256 `084ff89c7df3dbfc0c150263eec6d96c3dabf85fc1baacd864a7e40f41416616`，與 [R8f 獨立紙上覆核](verify-15-r8f-independent.md)相同；原有 `visualHash` `9dce146d046f75cf`。`keyframes --slug curio-s38 --shot pf004 --takes 1 --dry-run` 確認 MiniMax `image-01` 已就緒且只涉及一景。
- 開畫前本集 ledger 為 US$0.2220，其中舊 `pf003` 的 US$0.0035 仍為未解預約；既有整集圖、judge、配樂累計硬上限仍是 US$4.58。網站音訊卡仍顯示等待站主，本機按站主廣泛委派作的決定不代表站主親耳試聽。
- 私有 `STOP` 僅為這次 `pf004` 指定景執行暫停，外層 shell `EXIT` trap 在命令結束時恢復；已實測 `/workspace/.video-work/curio-s38/STOP` 存在。未送出 `pf005／006` 或其餘 105 景。

## 原生圖與帳本

唯一正式命令為 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs keyframes --slug curio-s38 --shot pf004 --takes 1`，執行 32 秒，exit 1。原始 stdout/stderr 保存於私有 `/tmp/curio-s38-r8f-pf004-pilot.log`，SHA-256 `1937d4925ef9b482f9a90b0d9c4a92c6ff03930a2be7d6ce3f9842067b22015b`。工具回報 1 張新圖、機器 judge **9/10 且未通過**：全身廣角變成中景，背景是攝影式景深／柔焦，未符合系列平面卡通畫風。

`keyframes/pf004-1.jpg` 是 1280×720 原生圖片，SHA-256 **`153d7687e6f0c0d8074d720e3ced300115025f26918e4af6a195611f313d1070`**。我親自檢視原圖：主角明顯童貌且只見半身，房屋更像近代住宅，火就在庭院前，無法讀成 1666 年倫敦成年人從花園望向遠處大火；因此即使機器總分 9，仍 **REJECT**。`manifest.json` 的 `visual_hash` 已更新到 R8f，但 `pf004` 只記 `takes[0].judge.passed=false`，不是合格選圖。`pf001／002` 兩張已通過的圖由工具報 `2 of 4 drawn shots are unchanged and keep their verdicts`，無新付款。

本次 image + judge 新增 **US$0.0135**；本集 ledger 目前 **US$0.2355**，13 次 image、11 次 judge、1 首 music，其中 `pf003` 的 US$0.0035 reservation 繼續算入。此處停畫原因是原生畫面與年代／成人角色不符，不是上限用盡。命令另因本容器缺對應 Playwright Chromium 而無法製 contact sheet；已直接檢查原生 JPEG，並不把 contact sheet 錯誤視作圖片通過。

## 下一關

依 [三景紙上試畫規則](verify-14-art-paper-independent.md)，先只修 `pf004` 提示詞並讓未撰寫者重新核對確切差分、固定日記及畫面規格；`pf004` 至多再試 **一次 1 take + 1 judge**。若第二次仍 REJECT，維持 STOP，不再為同一修詞方向購買第三張。`pf005／006` 尚未開始 R8f 原生試畫，`pf003` 不明預約仍不可重送；在三景 3／3 原生 KEEP 且預約處理完以前，整體分鏡及成片仍 HOLD。
