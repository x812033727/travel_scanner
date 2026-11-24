# S60 R2｜隔離盲看 B 敘事票

**判定：8 / 13 題是。** 以第一次聽完整段 zh-TW 旁白為準；這是敘事票，不是史實或畫面核查。

## 閱讀收據

- 只讀 `brief.md`、`script.md`、`video.json`，以及 `node tools/video/cli.mjs narrative --slug curio-s60 --json` 輸出的旁白與 13 題問卷；未讀其他審查或研究文件。
- 三份檔案的 SHA-256：`brief.md` `357f2c2706bd1fca6c77e9ccad45771a745ddadc91ba41da4d73f656ab2c5acc`；`script.md` `1ac4ee6548edae5a61f507c4e99edd75f5a81668d9acfa418b0ec22de8ea8b91`；`video.json` `bf8d95565857f0a8b976ef6f2d89e730fd88fabcab44201e75a05bd67dabba9c`。
- 上述命令原樣輸出的 SHA-256：`a2105c01d34ac221c702ed92b92c3939355576fffe67c34c911d5035b8f24494`。`script.md` 與 `video.json` 的 110 個場景 ID 和逐句旁白相同。

## 13 題

| 題目 ID | 票 | 第一次觀看的具體理由 |
| --- | --- | --- |
| `scene_first` | 是 | s60001–s60004 立即給 1912-01-18、南極雪原、史考特走向帳篷並讀到轉寄請求；有正在發生的事。 |
| `no_spoiler` | 否 | s60006 已直說阿蒙森升旗時「不知道腳下是不是精確的南極點」，提前交出 s60047 的主要發現。s60005 的黑旗仍停在「它告訴他什麼」，不算同樣問題。 |
| `one_line` | 否 | 開場倒敘之後大致按 10 月、12 月、1 月走，但 s60060 已說「抵達新營地」，下一章 s60061 又回到往新營地走，s60063 再次抵達；這裡短暫回捲同一動作。 |
| `no_toc` | 是 | s60005–s60008 是黑旗、測位、信件去向的具體懸念，沒有宣告章節順序或念後續內容清單。 |
| `chapters_link` | 否 | s60060 留下「新營地拿什麼作證」，s60061 卻退回布亞蘭德在新路前方，直至 s60063 才再搭帳；章首先回捲而非承接疑問。s60075 問為何不帶信走，s60076 只預告出版書將解釋，答案到 s60078 才來。 |
| `open_loops` | 是 | 全片無明顯超過 90 秒的無懸念長段：例如 s60014/s60017 的裂縫疑問、s60031/s60037 的方向與測位、s60055 的三人返營、s60074–s60075 的信件原因、s60098 的帳篷位置。 |
| `payoffs` | 否 | s60055 問三人沒有指南針、腳印若被雪蓋住「怎麼回來」；s60057 只報三人都回來，沒有新的返營方法。另 s60007 的「做了什麼才敢留帳」在設定的 s60065 只得到另一個問句；s60068 說仍不能宣稱精確踩點，後面沒有清楚解釋這個測位疑問如何轉成留信的把握。 |
| `no_recap` | 否 | 太陽高度變化小在 s60038、s60051、s60066–s60067 反覆解說；雪標協助返程在 s60029、s60085–s60086 再說一次；s60074 和 s60075 連問同一個為何不帶信走。這些不是有新事實的點名回呼。 |
| `chapters_are_events` | 是 | 七個標題都是帳篷留信、出發、穿山、插旗、連續觀測、託信、找到帳篷等事件或揭曉，沒有以「背景／結論」命名。 |
| `outro_no_next` | 是 | s60108–s60110 只請觀眾看原文、思考備份與訂閱，沒有預告下一集。 |
| `opening_hooks` | 是 | 首個帳篷場景後，s60005 留黑旗含義、s60007 留測位後的行動、s60008 留可證送達對象，至少三個後續時刻。 |
| `one_thread` | 是 | 主線是阿蒙森如何留下可被發現的到達消息：返程危險 s60014–s60024、位置證據 s60043–s60070、留信 s60072–s60080、史考特發現 s60099–s60107 都往這個難題走。 |
| `no_detour` | 是 | 裂縫救橇 s60018–s60024 稍長，但具體展示 s60078 所說回程出事的風險；高原測位也解釋為何他們先要確定留下什麼證據。s60087 的眼睛舒服是可刪的一句，尚不構成整段岔題。 |

## 整體感受

日期線在 s60090–s60103 特別清楚：1 月 16 日黑旗、17 日仍未見小帳、18 日看到並收下短箋、七天後阿蒙森回基地。s60105 讓「史考特能否帶回」落在明確的悲劇後果；s60106–s60107 誠實留下國王是否收到的證據邊界，足以回答開場的核心問題。結尾略被兩次「無法證明送達」及 s60109 的抽象反問沖淡，但不應把未知硬寫成送達。

## 官方 CLI 收據

- 引證格式答案：[r2-isolated-blind-b.answers.json](r2-isolated-blind-b.answers.json)，SHA-256 `f05c3d57af58081e65e860a0e8b6d58579fea4373c8f311866a51707dffda32d`。13 題順序和是／否票與上表一致。
- 執行：`node tools/video/cli.mjs narrative --slug curio-s60 --answers docs/videos/curio-s60/review/r2-isolated-blind-b.answers.json --workdir /tmp/s60-r2-blind-b-official --json`。正式輸出 [stdout](r2-isolated-blind-b.official-stdout.json)、[stderr](r2-isolated-blind-b.official-stderr.txt)、[exit](r2-isolated-blind-b.official-exit.txt) 已保存。退出碼 `1`；CLI 成功讀入 13 票、列出 8 是／5 否，因 5 題必需條件投否而判 `passed: false`。第一次用裸陣列被當成「no answer」的失敗格式也保存為 `official-attempt1-*`，不作為最終票。
- CLI 在 `/tmp/s60-r2-blind-b-official/curio-s60/review/narrative.json` 產生的正式記錄已複製為 [r2-isolated-blind-b.official-narrative.json](r2-isolated-blind-b.official-narrative.json)，SHA-256 `22d4a74b90387eedece7ef48e6c07927ff2e9c9ec2dde4a64e1cf90d3f65e1a3`；stdout SHA-256 `beec7227cb7a0c9d6fb3f064fb9e9b6f27959bc0c31fb729b3a87c84c8e19759`。
- 正式記錄內建綁定：`narrative_hash=3d2d798dab2ccbf4`、`script_hash=0f5b0fce4074b7b926faf34b06d3d6edb7b651254370d76311458e4c22245d89`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、`panel_narration_sha256=e217d8df9fa11cc31078f8886c7830def7917eb4f1d4ff7009a8f26e41c7d8f4`、`round=2`。
