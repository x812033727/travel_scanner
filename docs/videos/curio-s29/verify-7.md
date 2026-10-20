# S29 R5｜R4 獨立盲讀後的集中修稿

2026-10-20。**R5 是待新讀者審核的前製稿；沒有付費合成或站主親自審片的核准。** R4 的全新、先只讀稿的十三題盲評，鎖定 `script.md` SHA `3c39392d9072370ae1a8138cbf1957a63fbd8228cf76bdc792b362b76ff89fe1`，結果 **10／13**：`payoffs`、`no_recap`、`no_detour` 各一題否。原盲讀紀錄留在本次工作環境 `/tmp/curio_s29_r4_fresh_blind_seal.md`；本頁保存失敗原因與改稿處置，不把它當成 R5 通過證明。

## R4 三個失敗與 R5 修正

| R4 問題 | R5 逐項處置 |
| --- | --- |
| `boat055`–`boat060` 問辨蛇、睡醒，卻只說父親答對，不交代答案；`payoffs` 未過。 | 保留有來源的「七日內答不出，國家將覆滅」和大臣第一次到地下請教的事件，刪除兩道支線謎面的問答。`boat061` 改作「後來又問」白象重量，不假裝兩道中間的考題未發生。 |
| `boat039`／`boat040` 連續重說回到同一水痕；`boat068`／`boat070`／`boat071` 連續重說石頭，`no_recap` 未過。 | 刪 `boat040`、`boat071`；`boat068` 只交代佛經的「量石著中」和先量後載，`boat069` 才指出「即以此船」，`boat070` 只講畫線的比較結果。刪再問動詞的 `boat074`、結尾重述的 `boat089`／`boat093`。 |
| 蛇、睡醒以及一掬水和白馬的題目拖離船量象與文本比較，`no_detour` 未過。 | 刪 `boat056`–`boat060`、`boat082`–`boat083` 的支線謎題；保留經文持續出題的事實，讓主線從老父被藏、白象答案、國王追問，接到漢譯年代和可否證明借用。 |

R5 讓藏父情節有明確的事件階梯：`boat080`–`boat085` 從持續出題走到藏父違法的風險；`boat086`–`boat087` 依 [B3] 補出天神贈寶並允諾護國、國王問答題來源、大臣先求不治罪、國王答應，最後才揭露父親。`boat085` 新增「逐老法令會否送走答題老人」伏筆，`boat088` 以國王撤令並尊父為師回收。`boat055`、`boat068`、`boat081` 和新場景提示詞已對回各自旁白；新圖仍只是 cute-mystery 的卡通示意。

## 固定檔、來源與本地檢查

| 檔案 | SHA-256 |
| --- | --- |
| R5 `video.json` | `483ebde58834462f74b8e63a8cfe51a85a69178b35af4ccdb89f49ab66c2be44` |
| R5 `script.md` | `eeb3713583652ec8ccfd1b4b788dea370e3ae329c2123f473cbd67a5c98e210b` |
| R5 `claims.md` | `473d3010c09a8a4c0babc087c0414a308e596abc00a686de538dddf0d46aa893` |
| 《三國志》固定 HTML，重取後重算 | `dec2ae1713a56e2a33d367d691904004db60740f9490023b52695bfd3740bbc8` |
| CBETA《雜寶藏經》固定 XML，重取後重算 | `0b0d59c2c02da42fae95e3ed48f64e20813602b6f48032770a0ce557a6ff90b1` |

固定 URL、原文行號和「物／刻／施行」對「石／畫／以答」的界線見 [research.md](research.md)；[claims.md](claims.md)現與 **94／94** 句及稿本逐字對位。`video.json` 含 **92 張 still 插圖、11 組伏筆**。`estimateTimeline`：開場 44.57 秒、**正文 505.33 秒／8 分 25 秒**、全片估 561.13 秒／9 分 21 秒。這只是發聲前估時；TTS 與組片後須重新量正文，不拿片頭片尾湊八分鐘。

- `node tools/video/cli.mjs lint --slug curio-s29`：**0 errors、0 warnings**。
- `node tools/video/cli.mjs script --slug curio-s29`：重產 R5 稿；敘事內部版號 `c9826db4e4da4c99`。
- 逐行／逐 ID 本地校對：94 句稿、JSON、claims 對位；93 個場景 ID 唯一，92 張仍圖，11 組伏筆的 setup/payoff 存在。
- `npm run test:docs-videos`：**236／236 通過**；`npm run check:tasks`：**exit 0**，其他既有任務的警告不涉及 S29；`git diff --check` 通過。

**下一關**：用全新、未讀本集任何舊評語的對話先只讀 R5 `script.md`，再單獨回答官方 `narrative --slug curio-s29 --json` 十三題；封存逐題證據後，另一位讀者重開上述兩份固定來源，核對全部 94 句主張及 92 張圖的提示詞。R4 的 10／13 和本次作者自查都不是 R5 的獨立通過記錄。新審通過且相應關卡完成前，不跑付費 TTS、MiniMax、音樂或成片。
