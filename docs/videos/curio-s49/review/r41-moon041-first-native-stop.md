# S49 R41｜`moon041` 首張原圖退件停批與 32 張 KEEP 恢復

2026-10-22 UTC。`moon041` scene／claims 對 Git `04b58276b` 逐位元相同，故沿用 [R40 八景非作者來源／畫面紙審](r40-moon044-045-mature-glassworker-independent-paper.md) SHA-256 `ca7696ff6f43632a98e215714fe0d18fd2d913d9a382f034328c51bec48e9d07` 的書面 PASS。R41 只改 `moon040` 並已單獨紙審；本輪不重綁，也沒有更動音訊或其他畫面文字。受守衛只買 **`moon041` 一張 1280×720 原圖和一個 judge**；機器 **7.59／10 FAIL**，我與另一位原尺寸審查者均 **HUMAN REJECT**，立刻停在 `moon041`，`moon042` 零付費。

## 原圖與退件原因

現行 `video.json` SHA `36d9ddcc442a686f6f88ddadd10e9f8dfc37d58400a07b716979993d0f379461`，`claims.md` SHA `fc4b77a6fe7929903d7492eb4afef0c1f0c566ea6116739934e7e927f8787b80`，`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；`moon041` 旁白說「**照亮桌上的影像，不會替月亮送回更多細節**」。這是 Locke 1859 重印本中虛構光學說法與 Jacoby 1902 評論之間的概念比較，不是存世赫歇爾器材的復原圖。提示原要求一位成熟讀者、**小型年代油燈只照桌面**、窗外較暗月亮，不能有通向月球的光束或現代燈。

原圖 `keyframes/moon041-1.jpg` SHA **`b75188f16ad55c8d5144b4ad9b7964d292412c2be59e9f8bd5acad8304cda147`**；機器暫選的 8% 紙邊裁圖 `keyframes/moon041-1-trim.jpg` SHA **`c5bc4a14d5cc21634c56dfb85cb474adce74a34bdc3508bc391d7afddb5d217c`**，兩張都 1280×720。原圖有黑色電影式上下邊，裁圖去除；讀者確實成熟灰鬢、月亮在窗外且沒有光束打到月球。然而桌上是**大得佔左半畫面的帶電線聚光燈／舞台燈**，向巨大白色圓盤投強光，並非 1830 年代的小油燈。人物和全景呈**半寫實 3D 木偶質感**，偏離固定 `cute-mystery` 的平面可愛插畫；兩個關鍵問題在裁圖中仍在。機器 `style=0`、`details=7`、`generated=4`、總 **7.59 FAIL** 與目視一致。這張仍是想像場景，沒有冒充真實照片，但時代道具與系列畫風足以退件。[獨立原尺寸收據](r41-moon041-first-native-independent-visual.md) SHA-256 **`58ea645d1a87aa04de30e437a433b139e9bbf89ceacf7bc2c9c43acefa149a0c`** 同判 **HUMAN REJECT**。

## 費用、恢復與後續

付費前在 STOP/jobs 空下逐一驗 **32 張 KEEP 入選紀錄與實檔 SHA**；active manifest SHA `a28a741c18e0760a2545c3b224f1f5e8c75943dd281a5108063a9c36cd1c8c2d`，`visual_hash=540e3ad9a6188297`。確認 `moon041` scene／claims 與 R40 紙審版本一致。新鮮 MiniMax `image-01` status ready、圖片餘 **9,924**、judge 餘 **8,085**；本景只讀 dry-run **436／1070**，單張連 judge US$0.0135，累積及餘景估算均低於整集 US$5.30。守衛後暫解 STOP **一次**執行 `keyframes --slug curio-s49 --shot moon041 --takes 1`；CLI exit 1 是 judge 退件，仍真實付費一張圖及一個 judge，退出恢復 STOP。

機器 manifest SHA **`978d49f513c693d66fafab5f0c5465b10d4bda841a596ed16e7ef8c902d25fe3`** 曾暫列 `moon041 needs_review`。退件原圖、裁圖、機器暫時圖單／contact sheets、媒體狀態和前後帳本封存在私人 `review/r41-next-eight-native/moon041/`；[逐圖 SHA 庫存](r41-moon041-first-native-stop-inventory.json) SHA-256 **`272439306480423cc14e2d795f59f6e71c4b754595bba823fc92ff36339569d3`** 列完整 32 KEEP 與退圖。在 STOP 下把付費前 **32-KEEP manifest 位元恢復**，並復原前輪 KEEP contact sheets。現 active manifest 仍 SHA **`a28a741c18e0760a2545c3b224f1f5e8c75943dd281a5108063a9c36cd1c8c2d`**、32 張 KEEP 的檔案 SHA 全對、`moon041` 未入選；`keyframeProblems` 只有 **85 景未畫**、其餘 0。帳本保留真實付款，SHA `e83580ba8bac039590c71bf9e80d9596d0c3459239c35c4492119fefb7d62a97` → **`3d7a25ca6c2f15ba2dafeaafe6eeb03268d805aaecb3a0f270f76f58eabec92a`**，US$1.2285／91 image／91 judge → **US$1.2420／92 image／92 judge／0 預約**，低於 US$5.30；STOP 在位，jobs 空。

下一步只修 `moon041` 的**年代桌面光源與非寫實插畫觸發詞**，同步 claims 畫面註解，先交另一位做精確來源／畫面紙審。原句、其他 128 景、既收 32 張原圖均保留；審查前不重綁、不買第二張，也不續畫 `moon042`。若第二張仍畫現代燈或 3D，立即停止並評估有來源註記的字卡或借用已驗收圖的書面方案。全章 storyboard／成片仍 HOLD。
