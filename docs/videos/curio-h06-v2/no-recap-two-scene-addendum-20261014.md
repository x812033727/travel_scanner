# H06 v2｜無重錄刪除重複揭露的正式稿補記

日期：2026-10-14。本補記接在[來源圖卡與兩個新鏡的免費正式預檢](formal-source-card-adoption-20261014.md)之後。前文記錄的 104 句、15,028 格、場景次序／時窗、`7,617/15,028` 比例，以及當時各項雜湊均是**修訂前快照**，不再是現行稿的綁定。來源圖卡本身的史料界線和免費渲染紀錄仍可追溯；沒有以本補記替其成圖或成片驗收。

> **本頁已是歷史快照；後續現行稿見[兩句 DNA 比對回扣修稿](dna-payoff-two-lines-20261014.md)。**站主先採行下文的 `ftkk`／`court-proof-steps` 刪除方案；本頁前半的 83 景、102 句與 14,698 格是第二輪盲審 FAIL 時的狀態，末段的 82 景、101 句、14,558 格與雜湊則是下一輪 `payoffs` 盲審 FAIL 時的狀態。FAIL 原件均保留，新兩句稿尚待獨立盲審。

## 修訂內容

片頭一分鐘多內連續三次說明女子沒有留下本名，獨立敘事盲審在 `no_recap` 項判為未過。保留較早的運河事件敘述，刪除後段 `berlin-name-blank`（`rbd5`，原生 `big`，177 格）及 `berlin-name-card`（`e773`，`shot`，153 格）兩個 scene／兩句。第二章「病院裡有人叫她公主」移至下一景 `berlin-hospital-window`；其餘 102 句文字、順序和原逐句 WAV 不變，沒有重錄或新增付費圖片。

原 `berlin-name-blank` 承載的畫面揭露「開場插圖為 AI 情境示意，非現場照片」移至 `berlin-staff-corridor.data.sub`，成為片頭後第一張原生 `big` 卡的副標；YouTube 說明欄中的揭露保留。該副標與相鄰兩行繁中 CC 在 1920×1080 和 1280×720 的本地模擬抽格清楚、互不遮擋。這是靜格壓測，實際播放器的字幕設定與實速觀看仍待驗收。

## 現行檔案綁定與正文時窗

| 項目 | 修訂前來源圖卡預檢 | 本次無重錄修訂後 |
| --- | --- | --- |
| 場景／口播 | 85 景、104 句 | **83 景、102 句** |
| 正文 | 15,028 格／500.933 秒 | **14,698 格／489.933 秒（8:09.93）** |
| planned `shot` | 7,617／15,028 格＝50.6854% | **7,464／14,698 格＝50.7824%**；高於 50% 門檻 115 格 |
| 正式 `video.json` SHA-256 | `17492a61530c2b09c9547f4cc71c824c993dc628ebddd8d3a97a47f0dee67ed2` | `8f9b6a49225b3333db407ba6080013422b86e044530005706bcc74550d1a7400` |
| 正式 `script.md` SHA-256 | 見當時外部預檢收據 | `139e49ed3181bba09431b0ec2a7271488498a86fd102969de6c10c0bf1045471` |
| narrative hash | `096ba9d5bcc08524` | `7700f13d7d0820e1` |
| speech hash | `9ae95e3507d3809f` | `f3df23120ab8d774` |
| visual hash | `fc00fc2a753ca90d` | `eee72dfd24b09f61` |
| pictures／look hash | `c6ed3e494f6582a7`／`d57461da98a0ba9b` | `3e10a9516500e30d`／`d57461da98a0ba9b` |

用保留的 102 個逐句 WAV 樣本數重建的**未核准預測時間軸**為 14,698 格／30 fps，99 個畫面狀態，最長 8 秒、平均 4.9 秒；`cadenceProblems=[]`，章節與 loop 檢查無問題，`staleTakes=[]`。兩個待生圖鏡 `dna-hair-and-box`、`grave-fragments-limit` 的限定 dry-run 通過。上述 `shot` 分子只計腳本模板與預測時窗；兩鏡仍需實際生成、judge 及人工驗圖，最終影片仍需重算接受的有效影格，才能宣稱 50% 成片門檻達成。

## 收據、盲審與後續關卡

本次先將修改前 `video.json`、`script.md`、正式 `timeline.json`、`narration.wav`、104 個逐句 WAV、approval、manifest、ledger 等複製至隔離目錄，再編輯正式稿。快照與修訂收據均位於 `<home>/mokaair-work/videos/curio-h06-v2/review/no-recap-two-scene-20261014T052340Z/`：

| 外部證據 | SHA-256／狀態 |
| --- | --- |
| `snapshot.json` | `e33ee7985b0e0b78e59815e593e289ba235b9684cba96dda918ff58b523efd15` |
| `postflight-receipt.json` | `5fc5aee4c69505d3e738f149423a404dfb73f402d0ed985ae287e1c66aeb884a` |
| `timeline-projected-unapproved.json` | `a10fd70e5f135340e6abae7111c147099ed1d8916675dea0794143f28f8e2ff6` |
| `blind-payload.json` | `b8bb6bdc5cb1698000e434036d99cc2606db0b855318e161f373912a1e5f3add`；只含 narration 與 11 問，不含答案 |

`lint --slug curio-h06-v2` 為 0 errors、1 個既有 `generic` 提示詞警告；`git diff --check` 通過。正式舊 `timeline.json`、`narration.wav`、`approvals.json`、keyframes manifest 與媒體 ledger 均未修改，現有音訊核准**不適用**新 speech hash／時間軸；正式時間軸與合成旁白須用既有 WAV 零合成重綁，再由站主審聽核准。新版 11 問獨立盲審亦尚待結果；不得引用前文舊盲審或舊音訊核准作現行過關證據。沒有執行 TTS、後台動作或付費生圖。

## 第二輪獨立盲審結果與暫停點

本補記鎖定後，由另一位只讀上述 payload 的盲審員完成 11 題，結果 **10 YES／1 NO**。唯一未過 `no_recap`：`[28mj] 怎麼辨認她？親友可以作證，但接待她還不能證明身分。` 與稍後 `[ftkk] 但有人相信她，仍不能替代身分證明。` 重述同一證據界線，後句沒有點名回呼或加入新的身分證據。原始答案存於同一外部目錄的 `narrative-answers-second-blind.json`；正式 `review/narrative.json` 已記錄此輪 FAIL。這是繼前一輪 `no_recap` 退件後的第二輪內容未過，不能寫作敘事關卡完成。

依 `youtube-video` 兩輪未過的站主決策關卡，**H06 先不重綁音訊、不送新音訊卡，也不呼叫兩張已授權的 MiniMax 小樣**。已提出窄修選項供站主決定：刪除 `ftkk` 及其 `court-proof-steps` 原生圖卡（140 格，不重錄），或保留圖卡但改寫並重錄該句。若採前者，離線預估會成 14,558 格、`shot` 7,464 格／14,558 格，約 51.27%；這仍只是時窗推算，須修訂正式稿、重做獨立盲審、零合成音訊重綁及新雜湊核准後才能生圖。當時兩種方案均尚未採行；站主後來選定刪除方案，執行結果見下節。

## 第三次窄修已採行：刪除 `ftkk`，等待新盲審

站主選定上述**刪除**方案。從第二輪 FAIL 所綁定的正式稿，只移除 `court-proof-steps` 獨立 `steps` scene 與其唯一的 `[ftkk] 但有人相信她，仍不能替代身分證明。`，縮去 140 格；其餘 101 句文字和原逐句 WAV 不變。c05、c06 的訴訟及判決主張仍在其他場景敘述，來源界線仍見 [claims.md](claims.md)。片頭 AI 情境示意副標與說明欄揭露不變。未改 TTS、後台或付費圖片。

| 現行綁定 | 值 |
| --- | --- |
| 場景／口播與預測正文 | **82 景、101 句、14,558 格／30 fps＝485.267 秒（8:05.27）** |
| planned `shot` | **7,464／14,558 格＝51.2708%**；高於 50% 門檻 185 格，仍須以接受的實圖與成片重算 |
| 正式 `video.json` SHA-256 | `9f23d92b9ba2ad3d6577586356fbe26743de2b38761d4282a6fecb406100b627` |
| 正式 `script.md` SHA-256 | `404bf876904549b4122372c28ba7d8d1e2c270a0da3745a39cfd421054f76c0d` |
| narrative／speech／visual hash | `d9124141b968b88f`／`3e82b41f5ea2d748`／`373e3953f50e6b1c` |

這次用 101 個留存 WAV 的樣本數和 SHA 逐句重算，**未核准預測時間軸**為 98 個畫面狀態，最長 8 秒、平均 5 秒；`cadenceProblems=[]`，敘事機械檢查 0 errors／0 warnings。預測合成旁白只在記憶體中產生雜湊 `83cbce829d1401abdba7b525b5a55c90757581f4f8244d47dbad2e34f8fa583d`，沒有寫入正式 `narration.wav`。正式時間軸、舊音訊核准與第二輪敘事 FAIL 紀錄均未改；新音訊須零合成重綁並重新核准。

新隔離目錄：`<home>/mokaair-work/videos/curio-h06-v2/review/no-recap-ftkk-20261014T053555Z/`。`before/` 與 `before-receipt.json` 在修改前複製正式稿、上一版預測時間軸／payload／收據、第二輪盲審原始答案及正式 `review/narrative.json` FAIL 紀錄。`before-receipt.json` SHA-256 `e9cb471ee45ae076cff5039e9d4451266e383482a2d33af93deeeb4c37c9bf03`；保留的原始答案 SHA-256 `ce1125a4b9bd93a21869946918aa6b5c88ecb492224678f55a2015f19de33898`、FAIL 紀錄 SHA-256 `51d78e8724188456648be0add317bd1c063771972954f8c04919cd09c4c5d270`。修訂後 `timeline-projected-unapproved.json` SHA-256 `9c0bee5ab70b263b2b963b0c5b622399481579975e9ef8200603926ebd15f302`；新 `blind-payload.json` SHA-256 `f907f25d20d72904626c8a02e738a78eecfc121d49868bb9c36339022434c72d`，只含 narration 與 11 問、沒有答案。這是送審輸入，並非通過結果。

同目錄的 `postflight-receipt.json` 記錄修訂後文件與音檔雜湊、逐句 WAV 核對、時間軸／占比、lint 和差異檢查；這份收據不表示新敘事或音訊已核准。
