# S57 R8｜獨立盲讀 B

2026-10-21 00:25 UTC。**12／13；`no_recap` = NO，敘事關卡 HOLD。**我未撰寫此版劇本，先讀凍結版口播稿與固定十三題自行評分；之後只查看同版 `video.json` 的場景 ID／迴圈表來核對引用，沒有查閱作者修稿、前輪評語、讀者 A 或史料覆核結論。沒有修改五份創作檔、付費媒體或網站審核。此票只代表讀者 B，須與讀者 A 依固定 OR 規則正式合併。

## 凍結版本與評分方法

| 創作檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `5eadc760e95287cebc97c61007333007348939c18ec505d38ddd9acc5cb88abd` |
| `claims.md` | `cff4abfd700e501ecdc32700138fda27d143320f0f666f233d2792266e0cc861` |
| `video.json` | `bb0cf8d70f565a0c34d0923c08678665b26e24c6637d208d96f474dafb5841d4` |
| `script.md` | `d9605ab9b06528780454cdecd6af3604e34e1be3e09a379ac14e4b46a3fa674d` |

這些雜湊在評分前後相同。原始十三題 [答案](r8-blind-b/answers.json)以 `NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s57 --answers ... --workdir /tmp/curio-s57-r8-blind-b --json` 跑在獨立 `/tmp` 工作目錄。工具[原始輸出](r8-blind-b/cli.stdout.json)、[stderr](r8-blind-b/cli.stderr.txt)、[exit code](r8-blind-b/cli.exit-code.txt)與[正式記錄](r8-blind-b/official-narrative-record.json)均封存；exit **1** 是因必答題 `no_recap` 未過，`passed:false`、`failed:["no_recap"]`，不是工具故障。固定 panel rules SHA-256 為 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

## 十三題投票

| 題 | 票 | 腳本依據 |
| --- | --- | --- |
| `scene_first` | YES | [s57001](../script.md) 直接進入 1872 年 3 月封日記的動作；[s57002](../script.md) 交代兩人。 |
| `no_spoiler` | YES | [s57004](../script.md)、[s57008](../script.md) 留住人要往哪裡去、物資能否改變決定；結局未在開場說出。 |
| `one_line` | YES | 從 [s57011](../script.md) 缺貨、[s57036](../script.md) 相遇、[s57063](../script.md) 勸歸、[s57139](../script.md) 交援助，推進同一個分路問題。 |
| `no_toc` | YES | [s57083](../script.md)、[s57138](../script.md)、[s57164](../script.md) 問的都是當下情節，不宣告影片章節或清單。 |
| `chapters_link` | YES | [s57035→s57036](../script.md)、[s57062→s57063](../script.md)、[s57083→s57084](../script.md)、[s57138→s57139](../script.md)、[s57164→s57165](../script.md) 的問答接續清楚。 |
| `open_loops` | YES | [s57017](../script.md)、[s57061](../script.md)、[s57107](../script.md)、[s57122](../script.md)、[s57164](../script.md)、[s57183](../script.md) 等未解問題持續出現。 |
| `payoffs` | YES | [s57008](../script.md) 的補給／去向由 [s57139–s57156](../script.md) 的新援助、待人手與南西行計畫回答；[s57117→s57120](../script.md) 水陸會合、[s57134→s57143](../script.md) 舊布、[s57183→s57187](../script.md) 回家與否均給新資訊。 |
| `no_recap` | **NO** | [s57161](../script.md) 已說三月接連寫信；[s57162](../script.md) 和 [s57163](../script.md) 連續再說幾天寫字、仍寫信，直到 [s57165](../script.md) 才有具體收件者。[s57179](../script.md) 已說蘇西、楚馬在告別隊伍，[s57180](../script.md) 緊接著只換句話說路上不只兩人。 |
| `chapters_are_events` | YES（參考題） | 「烏吉吉的空箱」「蘇西跑來報信」「五十四天的東行」「日記走了，人留下」均是事件節拍。 |
| `outro_no_next` | YES | [s57187–s57189](../script.md) 收在人與日記的後來，沒有下一集預告。 |
| `opening_hooks` | YES | 第一個封日記場景後，[s57004](../script.md)、[s57008](../script.md)、[s57009](../script.md)、[s57010](../script.md) 至少四個未揭曉問句。 |
| `one_thread` | YES | 李文斯頓的健康、缺貨、補給、研究打算與史丹利帶他回家的嘗試，從 [s57001](../script.md) 一直貫穿到 [s57182](../script.md)。 |
| `no_detour` | YES | [s57084–s57097](../script.md) 湖行說明研究難題，[s57113–s57138](../script.md) 東行與短貨說明補給條件，[s57161–s57168](../script.md) 寫信封日記通往告別；沒有整段離開主問題。 |

`no_recap` 的兩組句子應只留各自一個必要動作，再把多出的時間用新的、有來源的因果細節補足；正文已接近八分鐘下限，不能單純大段刪除。修稿後，這一票不沿用到新檔案雜湊。
