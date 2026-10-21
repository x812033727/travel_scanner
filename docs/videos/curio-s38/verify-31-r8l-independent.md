# S38 R8l｜`pf007` 蠟燭近景第二次修詞獨立覆核

2026-10-21 00:48 UTC。**PASS：僅准許 `pf007` 最後一次指名 `1 take + 1 judge` 的紙上方案；R8l 尚無合格原生圖，整集分鏡、網站審核與成片仍 HOLD。**我沒有撰寫新提示詞、修改創作檔、移動私有 `STOP`、清帳本或執行付費生成。

## 版本與唯一差分

實測 R8l `video.json` SHA-256 **`2e9ec8c6f2962b420719ef62185d38def7f915bac3fac2e55fb0f16b231c6778`**、`visualHash` **`859769ddb7cef27f`**。我從現檔原始位元組把新 `pf007` 提示詞換回[作者差分](verify-30-r8l-structured-diff.json)中的 R8k 字串，整檔 SHA-256 精確還原為 **`d98065c80a7153ce252bcb77d06cf6fb72d7bb51c0d1931ed70c25493e79a6f3`**、舊 `visualHash` **`3305195e7268b31e`**。遞迴比對解析 JSON，只有 **`scenes[6].data.prompt`** 一個葉節點變動；`pf007` 的 ID、template、`camera: pan left`、`visual`、旁白，以及其餘 111 景的台詞、chapter、模板、運鏡和資料都未改。`brief.md`、`research.md`、`claims.md`、`script.md` SHA-256 仍為 `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。

Lint 實測 **0 errors／0 warnings**。`--shot pf007 --takes 1 --dry-run` 僅列這一景，MiniMax `image-01` ready，無生成呼叫。私有 manifest 還綁 R8k `visual_hash=3305195e7268b31e`，`pf007` 仍是舊拒收圖（`judge.passed=false`、`needs_review=true`）；舊圖不可冒充 R8l 方案通過。`pf001/002/004/005` 仍在 manifest 為 passed，但 R8l 逐景 request key／judge stamp 沿用須由正式工具核對。

## 史料與原生退件

再次對照固定 Pepys 日記 `4200.txt`（SHA-256 **`3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`**）的 1666 年 9 月 2 日：Jane 約凌晨三時叫醒佩皮斯；他穿 `nightgowne`、到她看的窗邊，覺得火遠後又睡。現有 `pf007` 旁白「她叫醒佩皮斯。他套上睡袍，走到窗邊。」沒有更動。R8l 只指定**一位成年男子一次走向木窗的動作**，改以一支蠟燭照亮臉與牆；1666 年使用蠟燭合時代，且避免前圖的電燈，但日記沒有說這一刻的燈具、桌木、牆面、鬍鬚或房間配置。`middle-aged`／短鬍是卡通角色提示，不可標成佩皮斯精確年齡或肖像重建；原文的「她的窗」也不能由畫面解說成他自己的窗。約凌晨三時的窗外應仍顯夜色，若生成明亮白天窗景須退件。

我直接看過[R8k 原生 1280×720 JPEG](verify-29-r8k-pf007-native-stop.md)，SHA-256 **`5d52a3b49838b386faaa661d98a4fbd4a5fdae626356e77d9beedd1a4f6bc8ec`**：現代電吊燈與桌燈、過亮的窗、電影式 3D 房間質感都清楚可見。manifest 雖有總分 9，`style=0`、`details=7` 且 `passed=false`，判退正確。R8l 從整室寬鏡頭收窄至單人近景，明確一支蠟燭並保留木窗，正對這兩項退件。提示詞不塞畫風字，由既定 `cute-mystery` look 控制；一景仍可因 3D、現代燈或黑邊而再退件，紙上 PASS 不保證生成效果。

## 預算、STOP 與下一停點

私有 `STOP` 實測存在。ledger 實測 **US$0.3165**（19 image、17 judge、1 music），包含舊 `pf003` **US$0.0035 reserved**、key `3a06e8acfb085b26`；整集原硬上限 **US$4.58** 未改。最後一次 `pf007` 的一張 image＋一次 judge 依前兩次實際最多新增 **US$0.0135**，累計至多 **US$0.3300**，舊 reservation 已計入，不能清除或重送。工具 dry-run 的約 US$0.01 是四捨五入，不能取代帳本計數。

負責人若依既有流程執行，只暫解 `STOP` 跑 `pf007` 一次並以退出處理立即恢復；逐景確認其他四張 passed 圖吃快取，`pf003` 未重送。須看完整原生圖及九題評審：**平面可愛插圖、無現代照明與黑邊、成年男子穿睡袍向窗邊移動、窗外保持約凌晨三時的夜色**，機器 PASS 與人工視覺一致才可 KEEP。這是此景第三張圖、第二輪修詞；若仍不過，就依系列三圖兩修停點停止購圖，另提有史料與卡片上限支持的無新圖方案，不自動把行動旁白變成泛用文字卡。即使成功，第一章仍 **28.90 秒**，其餘未畫景與後台審核仍未完成。
