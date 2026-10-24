# S57 R4｜正式雙盲敘事合併診斷

2026-10-20 UTC。**敘事 HOLD：固定 OR 合併 9／13 YES，四個必答題未過。**這是兩位無前情讀者對下表精確 R4 劇本的敘事票合併，不是作者自評、史料、政策或媒體放行。[R4 獨立來源／書面畫面覆核](../r4-source-independent.md)已對同一五檔給來源 PASS；該結果與本敘事 HOLD 分屬不同關卡。沒有修改五份創作檔或執行付費媒體。

| 凍結創作檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `50b4f5f48f9ef82b18f25ff8f681014bd658cb45955101e109574658f34de139` |
| `claims.md` | `07c3d2ea5ea29d7d7ce68deb020c09b72a0dd424cfe548224a32039473e30b72` |
| `video.json` | `bf2d6d429fca78f3a66620b114ee8333b4f91d2e37262a25d24fedac3ea1d4a8` |
| `script.md` | `a375377e0ced91d83be01650bb4e55fb6845de4e463d542302938d3de58fe6ce` |

## 原始票、轉錄與正式執行

兩位讀者各自聲明只讀 R4 `script.md` 與官方 13 題。原始 [A 票](raw-ballot-a.md)與 [B 票](raw-ballot-b.md)逐字封存，SHA-256 分別為 `629260b65f6ad26580af68607c060af06565c730492ed487e2892ace1eee9a25`、`3064f0e7e514652571916b760a3415437833a4f967d141cca6313639c4a85e48`，與原 review 檔相同。A 為 **9 YES／4 NO**；B 為 **8 YES／5 NO**。我依兩份原票各 13 列轉為[官方形狀 A 答案](ballot-a.json)、[B 答案](ballot-b.json)：布林票逐項不變，引用從固定 `script.md` 補為含場景 ID 的逐字句。A／B 答案 SHA-256 分別為 `50ef1fd40b70df281de0883ba176ba04e1f968d49f96dfd2d6e39481c43aa3f5`、`9a03072d52ff6462c14420e8f3eb22ac622a902e200de08c8e39ee9d8c21100e`。[完整稽核](merge-audit.json)保留每題原票理由、引用 ID、逐字稿句、是否在原票理由中逐字列出該 ID、檔案 SHA，以及 `panelVerdict` 原票和 `mergePanelVerdicts` 合併結果；原票只給範圍或章名時，轉錄選其範圍中的代表句作官方引用，沒有增改判斷。

使用 `tools/video/core/narrative.mjs` 的 **`panelVerdict` 與 `mergePanelVerdicts` 固定 OR**：同題任一讀者有帶場景 ID 的 YES，合併即 YES；僅兩位都 NO 才未過。官方規則 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`；[合併答案](merged-answers.json) SHA-256 `74211a97cd4ee9fdc60bd99b76b3bf35a4237f33163f0f285a6e77732f1f4325`。`one_line` 是 **A YES、B NO，按 OR 合併 YES**；B 的異議仍在原票與稽核，沒有改寫為一致通過。其餘四項下表均是兩票共同 NO。

執行前後均核對上述五檔 SHA 全部吻合。以 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r4-merge/merged-answers.json --workdir /tmp/curio-s57-r4-merge-formal-20261020 --json` 跑正式關卡：**exit 1、`passed:false`、4 個 required fail、0 advisory fail**。保留[原樣 stdout](cli.stdout.json)、[空 stderr](cli.stderr.txt)、[exit code](cli.exit-code.txt)、[命令與前後 hash 狀態](cli-status.json)及[工具產生的官方敘事紀錄](official-narrative-record.json)。官方紀錄的 `panel_narration_sha256` 為 `44f05cb06f452a3d7fcf987b2895f05ea9c495db776667de43d755e924f557a8`，紀錄檔 SHA-256 為 `ff0c11b17c09aa5f016981a0582182e2a469c10c0a5f8fa6dd989c8bcee37804`。工具把 slug 附加在 `--workdir` 根目錄下，實際紀錄位於 `/tmp/curio-s57-r4-merge-formal-20261020/curio-s57/review/narrative.json`，已複製封存於此。

| 兩票共同 NO | R4 精確斷點與下輪修稿界線 |
| --- | --- |
| `chapters_link` | A 指開場 `s57010` 問為何分路，下一章首句 `s57011` 只說「分路的難題」已現形，仍是概括標籤，未立刻讓聽眾聽到病況／缺貨如何接上選擇。B 另指出 `s57111–s57112` 已說離湖向東，次章 `s57113` 又說年底離開烏吉吉，章首重報出發而未推進事件。兩個邊界都需照原票處理。 |
| `payoffs` | A、B 都指出 `s57107` 問「往東的箱子，還能替他留下多少？」；`s57133–s57143` 只說史丹利有貨、李原有貨短少、後來取回一包布，並未給**還剩多少**的答案。固定來源不能量出這個問句要求的總量；應改成後文確能答的具體疑問或刪問，不能編造數量。 |
| `no_recap` | A 指 `s57052` 已說找到人、`s57184` 再報一次，`s57149` 的等海岸人手續行在 `s57185` 重述；`s57064` 與 `s57070–s57071` 兩份記載中的返家休養再回來也有重播感。B 另指 `s57111→s57113` 重報離開，`s57131→s57139` 重說二月十八日。這些是兩票各自點名的重複，不可只刪其中一組就宣稱全題已修。 |
| `no_detour` | 兩票都指 `s57049–s57050` 的名句文本比較暫停了「為何沒有帶回家」的因果線；`s57114–s57125` 的豆子、牲畜、天氣、岩石與坡道使抵達補給箱的結果拖延。應留住必需的來源層級與行程時序，但讓每一段推進返家選擇與補給問題。 |

**另保留 B 的單票異議：**`one_line` 在 B 是 NO，指 `s57063–s57068` 先述史丹利版本的勸歸，`s57069–s57072` 又以日記重過同一提議；A 判 YES，故本次正式合併依規則通過，但下輪作者可連同 `no_recap` 診斷處理，不應將 B 票抹去。

**交接：**R4 的來源 PASS 與正式敘事 HOLD 都只綁定本報五個 SHA。正式 CLI 與前後 freeze 已封存後，才放行 R5 作者修改創作檔。R5 須另凍結五檔，重交獨立來源／書面畫面、兩位新盲讀及正式合併；R4 不進政策、語音、插圖、配樂或成片關卡。

歸檔後檢查：原票副本、合併答案、CLI 紀錄與預期四項失敗的 SHA／內容一致；`npm run test:docs-videos` **236 pass／0 fail**；`npm run check:tasks` **exit 0**，僅列既有其他任務的 stale／scope 警告。這些機械檢查不改變正式敘事 HOLD。
