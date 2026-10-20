# S54 R12｜無背景盲讀後的作者定點修稿凍結

2026-10-20 UTC。[R11 兩位空白背景讀者的正式 OR](r11-clean-merge.md) **12／13 FAIL**，共同未過 `no_detour`：五月郵票的主問題已有答案，尾端 `s54144–47` 卻跳到 1848 年的回信貼票用法。B 另指出開場付款難題的回收過泛、郵差等收錢重述；這兩題正式 OR 通過，但本輪一併做最窄修正。本紀錄只是作者凍結，並非獨立史料、畫面或敘事 PASS。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `0eabd20a735ba729c9b22f4a2c035a29230d07d0a95f134ffdf8050d46dd0f11` |
| `research.md` | `a0456817c7d5a2bf19f5dc940d0dadca456bcbffea908328e90ef16f301cad34` |
| `claims.md` | `f517635d938fe01c161b3bc76cc5b8766a91df9936dba656f734ffb49f7cefc5` |
| `video.json` | `a18316bc5ec45f1512b3268b2c5f95be3771ec4ffffeab77a4927a47dd36a9b2` |
| `script.md` | `b0583005ab8442335e1874c2881a5fc47d8e8d67f1f8db4cbb61bc7531003d3d` |

## 差分與依據

- `s54005` 從無法細答的「付款時碰上什麼麻煩」收窄為「大廳收郵資的辦法撐得住嗎」；`s54094` 以希爾 1 月 11 日日記明寫的收款辦法不足、大廳混亂回收。[H 13221–13225](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13221-L13225)沒有櫃台流程細節，本稿不編造哪個機器或職員失靈。
- `s54031` 只保留希爾希望免去逐封收款帳目的新理由，刪去重述郵差在收件人門口等錢的 `s54032`。[H 9612–9614、9638–9642](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9612-L9642)限定這是希爾的方案目的。
- 保留五月同一條時間線與 `s54109` 四月政府規劃室畫面修正；將 1848 年 Leavitt 的 `s54144–47` 全數移出口播。片尾以 [希爾的銷記敘述和 5 月 21、29 日日記 H 13410–13463](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13410-L13463)繼續推進：黑票紅墨、漏蓋、票面預塗薄層可洗墨、求助化學師，以及一名郵局主管認為總局供墨後花招似乎減少。這是希爾轉述的**暫時判斷**，沒有說弊端消失。新增畫面只是無字卡通示意，不畫真的郵票肖像或可讀原件。
- `s54144` 留下「希爾接著找誰幫忙」並由 `s54145` 回答；`s54141` 的防重用問題在 `s54146` 收到具體的當時處理進展。`loops` 的該筆 payoff 改綁 `s54146`。說明欄仍列固定的法案、希爾、Leavitt 和頻道連結；Leavitt 現只作 1 月／5 月日期交叉來源，不再進入片尾敘事。

`video.json` 有 145 個敘事場（138 插圖、7 工具字卡）另有 3 句 outro，`claims.md` 145／145 與場景逐字對齊、23 組 loop。開場 153 漢字，正文 2,630 漢字；以最快每分鐘 325 字估為 **8 分 05.54 秒**。`lint --slug curio-s54 --json` 為 **0 errors／0 warnings**、7 章、工具書面總估 13.87 分鐘。這仍非 TTS 實測。`git diff --check` 通過。

下一關：不同工作者重開固定史料，獨立核 `s54005`、`s54031`、`s54094`、`s54142–46` 與新畫面，再讓兩位**無先前對話背景**的讀者重做 13 題敘事；R11 的通過項和 Jev 政策判定不套到 R12。舊稿 S54 TTS 在第 6／148 句後安全 STOP，只有 `s54001–06` 六段草稿快取，當中的 `s54005` 已改字必須重合成；沒有 R12 `narration.wav`、時間線、圖片或成片。請勿清除 `/workspace/.video-work/curio-s54/STOP`，直到新稿獨立敘事與來源皆過。
