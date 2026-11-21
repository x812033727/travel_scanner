# S57 R9｜作者窄修與五檔凍結

2026-10-21 UTC。**R9 仍是作者候選，不能用本收據自判史料、畫面、敘事或政策 PASS。**[R8 獨立來源與書面畫面](r8-source-independent.md)均 PASS；[R8 正式雙盲合併](r8-merge/summary.md)為 **12／13 HOLD**，唯一共同 NO `no_recap`。R8 B 承襲前輪高層狀態、A 的 `fork_turns:none` 無法證實；本版另派兩名真正 `fork_turns:none` 新讀者。R8→R9 的[精確差分](r9-author-diff.patch) SHA-256 `64899a0941250700708a076ce6e697324a7a3c7920baff00427df454ded776c3`。

| 創作檔 | R8 SHA-256 | R9 凍結 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `5eadc760e95287cebc97c61007333007348939c18ec505d38ddd9acc5cb88abd` | `c7900d23f61699c506abbde288aadbe2d32c0e5020721a2e2c44ee04ff2876ea` |
| `claims.md` | `cff4abfd700e501ecdc32700138fda27d143320f0f666f233d2792266e0cc861` | `241f5a2fa4b25e977baf832907213b7be98cda7a9cfa55ea58331f0a31466beb` |
| `video.json` | `bb0cf8d70f565a0c34d0923c08678665b26e24c6637d208d96f474dafb5841d4` | `940046297c87511a82c9e42eb5d0c0fbcf8bdaa9b5528ce17234ac77c7cf8588` |
| `script.md` | `d9605ab9b06528780454cdecd6af3604e34e1be3e09a379ac14e4b46a3fa674d` | `7edc924366e588787794e9c2ceac53ce8f5131188f19aa9c0a71a3543c326b43` |

## 四組重述的窄修

1. **村中市場：**`s57016` 原與 `s57018` 都說市集食物／休養，改為商人迎接與**傍晚**才傳來託管貨物壞消息，保留 `s57018` 食物可買但未解長途補給。這兩個不同事件按[日記 L5219–5223](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5219-L5223)的日內次序；`s57019` 才揭示貨物被賣。新 prompt 只畫一名商人舉手。
2. **班奈特派令：**`s57029` 留下委派人與任務；`s57032` 原重報「找到這個人」，改為史丹利出版回憶中的**自行規劃尋人及分批提領路費**，接上 `s57031` 必要時帶物資的條件。詳見[固定節錄 S89–109](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L89-L109)；不是班奈特另一份獨立證詞，不演逐字對話或假地圖。新 prompt 在巴黎 Grand Hotel 只畫記者整理素面紙張。
3. **三月託付：**`s57161–s57163` 原三景連續重報寫信。現在 `s57161` 是**3 月 10 日**五千盧比有條件備用支票交史丹利，先前款用盡才可兌；日記原文[L5868–5871](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5868-L5871)。`s57162` 為[L5873](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5873)的**12 日「寫字」**；刪掉再說他仍寫信的 `s57163`。下一章 `s57165–s57166` 才說**13 日**完成給班奈特與格蘭維爾的兩份文件，未提前揭曉。支票只畫一人折素面紙，沒有說已兌。
4. **告別在場者：**保留 `s57179` 所述蘇西與楚馬在隊伍裡，刪 `s57180`「路上不只兩人」的換句重述；這一在場記載歸[史丹利出版回憶 S14396–14443](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L14396-L14443)，不讓人物在畫面消失。

**精確集合：**改四句旁白及 claims `s57016,s57032,s57161,s57162`；刪兩景及 claims `s57163,s57180`；改三個 prompt `s57016,s57032,s57161`；更新 `brief.md`、`claims.md` R9 版本標籤。其餘 parsed `video.json` 未改。`research.md`、S 出版節錄／L 身後編刊來源層級、精確相遇日 HOLD、二月 **18 日新援助→19 日藥品→20 日舊藏布**時序未變。劇本由工具重生，刪景後序號下降，後段旁白沒有另改。

## 作者機械檢查與交審

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**；160 句，工具估時 **13.78 分鐘**，濃縮開場 **00:45**；正文 **2,618 漢字**，按每分鐘 325 字約 **8.06 分鐘**。142／160 景 `cute-mystery` 插畫（**88.8%**）、18 張資訊卡、15 條 loops；固定 5 秒片頭及 21 秒片尾／可點連結槽位在企劃，尚無真實長片 ID。
- `claims.md`、`video.json`、`script.md` **160／160 ID、順序、旁白逐字對齊**，無重複 ID；`npm run test:docs-videos` **236 pass／0 fail**；`npm run check:tasks` 在凍結時 **exit 0，Validated 2347 task files**。
- R9 新版已交一名非作者來源／書面畫面審查者及兩位 `fork_turns:none`、只讀凍結 `script.md` 與固定 13 題的新隔離讀者。所有 PASS／NO 均由他們另行判定，再固定 OR 合併；本收據不替代任何獨立票。未執行付費語音、插圖、配樂、組片、上傳、政策核准或站主人工審核。
