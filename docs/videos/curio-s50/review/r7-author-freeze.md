# S50 R7｜`fire019` 窗邊站位的作者限縮修稿

2026-10-20 UTC。[R6 獨立來源與書面畫面覆核](r6-source-independent.md)只在 `fire019` 判 **HOLD**：佩皮斯日記記載珍妮叫醒他，然後他才走到她的窗邊，沒有說她從窗邊呼叫。R7 是依此意見修正的**作者候選稿**；本收據不作獨立來源、畫面、盲評、政策、網站或音檢放行。

| R6→R7 精確改動 | R7 內容與理由 |
| --- | --- |
| `fire019` 口播 | 「有人叫了起來；床上的佩皮斯還不知道橋頭燒成什麼樣。」刪去呼叫者的窗邊站位；下一句 `fire020` 才說明叫醒他的是珍妮。 |
| `fire019` 待畫提示詞 | `Medium shot in a plain bedroom before dawn, one diarist stirs in bed as an unseen person calls to him, pale light`。畫面只有佩皮斯起身和未入鏡的呼叫者，不給呼叫者位置。 |
| `claims.md` 的 `fire019` | 明記來源只支持珍妮約三點叫醒佩皮斯；佩皮斯其後才到她的窗邊。橋頭火線承接前述文森特事後著作，非佩皮斯此刻所見。 |
| `fire019→fire020` 伏筆 `what` | 「誰在凌晨叫醒佩皮斯」，刪去沒有來源支持的窗邊站位。 |
| `script.md` | 由本集 CLI 重生，與 `video.json` 119 句字面一致。 |

固定依據是 Pepys 1666 年 9 月 2 日日記 [D L65788–65804](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65788-L65804)，本地原文 `/tmp/new-pepys/4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。R6 七句音訊修稿、其餘 118 句、112 個其他畫面提示詞、其餘 28 條伏筆、標題、章節和企劃均未改。

| R7 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b` |
| `research.md` | `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95` |
| `claims.md` | `4e07795ddf55b4b686431851664cb1c686333233417e378b87b9e96c1180bedc` |
| `video.json` | `e2c2537dc0fe97807e1f686a7d511b5f64d03680f89c1c0461cec3bbe8ad0234` |
| `script.md` | `5f9ae7f8b89b5f898c982dd51215c5d148901820bf715e10e6d43f8872ef782b` |

作者機械核對：119 個唯一口播 ID、119/119 主張列同 ID／文字／順序、119/119 劇本口播同文字／順序；113/113 個 `shot` 提示詞非空，29/29 條伏筆均先 setup 後 payoff。`lint --slug curio-s50 --json` 為 **0 errors／1 舊 warning**（片尾沒有口頭訂閱提醒；畫面 CTA 仍在）。估時按 250／300／325 CPM，濃縮開場 **48.23／41.40／38.97 秒**、正文 **10:44.00／9:13.40／8:41.00**；最快估時仍超過八分鐘，這**不是 R7 實配音長**。`npm run check:tasks` 通過（2124 件；既有 stale claim／scope 警告），`npm run test:docs-videos` **236/236 PASS**，`git diff --check` 通過。

**下一關：**另一位工作者獨立核對上述精確五檔、`fire019` 日記先後及書面畫面；兩名未讀 R7 的新讀者對同一 `script.md` 雙盲。其後依最終版重綁政策、網站劇本卡、改句配音及全片 119 句零旗標音檢。R5 的真實音訊仍是七句 HOLD；本輪沒有 TTS、音檢、插圖、配樂或成片付費呼叫。
