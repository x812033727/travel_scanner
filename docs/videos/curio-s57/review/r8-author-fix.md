# S57 R8｜作者窄修與五檔凍結

2026-10-21 UTC。**R8 僅是作者候選。**[R7 獨立史料及書面畫面](r7-source-independent.md)均 PASS，但[R7 正式雙盲固定 OR](r7-merge/summary.md)為 **11／13 HOLD**，兩位讀者均否決 `no_recap,no_detour`。本作者紀錄沒有替 R8 判獨立史料、畫面、敘事或政策 PASS。[R7→R8 精確 diff](r8-author-diff.patch) SHA-256 `6c486083ce301cf0223c21bf50ace32815433751ead4c4ca1aa7114af8cab0d5`。

| 創作檔 | R7 SHA-256 | R8 凍結 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0474bc0e793cbda07021da98b3ea972a50b60fe87eacb708baf85457bdf554f6` | `5eadc760e95287cebc97c61007333007348939c18ec505d38ddd9acc5cb88abd` |
| `claims.md` | `d4b8958f6f9c7b7fd62ec172ae39279d096086f22f4bdcc1fb2c07ef79401d38` | `cff4abfd700e501ecdc32700138fda27d143320f0f666f233d2792266e0cc861` |
| `video.json` | `f3befaaeb100cb0d9c275be56851691b174ef423777f1955375e520119bb71e7` | `bb0cf8d70f565a0c34d0923c08678665b26e24c6637d208d96f474dafb5841d4` |
| `script.md` | `185558e4d0e0ca51794126d8289ffb0d54065191d00cc010a2a6b72ff4d0245f` | `d9605ab9b06528780454cdecd6af3604e34e1be3e09a379ac14e4b46a3fa674d` |

## 修稿範圍與來源

- **重返村：**`s57100` 只說 **12 月 13 日**兩人回烏吉吉；`s57101` 改記 **15 日**李文斯頓準備往東取自己的貨，不再重複「回村」。兩日見[固定 L5420–5428](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5420-L5428)。
- **書信／電報岔段：**`s57101,s57104,s57105` 的領事信、亞丁電報、未收同類信件換成準備東行、**16 日**雇到通韋的划船者與嚮導、**19–20 日**裝大鐵箱並寫明器物要由史丹利送回家；原文[L5427–5435](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5427-L5435)。**刪 `s57106`** 的重複十五日準備句。託送是日記計畫，不宣稱十二月已交箱或已運到家；新 prompt 都是一人一動作。
- **二十日新事實：**`s57143` 仍記**20 日**有人拿出舊藏布，`s57144` 改講同日收到女兒艾格妮絲的四件法蘭絨襯衫及結帳後尚缺 **436½ 碼**，不再重播藏布追回或 **18 日**新援助；見[L5812–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5812-L5818)。艾格妮絲為女兒見[L5741–5749](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5749)。`s57008` 補給是否改變主意的 loop payoff 移至 `s57149`，貨到後仍等同行人手才走；不讓新的襯衫／缺布句硬答選擇問題。
- `claims.md` 的 `s57189` Waller／1874 書名與刊記連結補足到 L60，修正 R7 獨立覆核指出的標籤範圍。其餘來源分層、精確相遇日 HOLD、二月 **18 新援助→19 藥箱與藥品→20 藏布**順序均保留。未增加未查的逐字對白、真地圖或史實結論。

**集合：**改五景旁白／claims `s57100,s57101,s57104,s57105,s57144`；刪一景 `s57106`；改四景 prompt `s57101,s57104,s57105,s57144`；改一條 loop payoff `s57008→s57149`；`s57189` 僅補引註標籤／行範圍；更新企劃狀態與章節説明。`script.md` 由工具重生，後段序號隨刪景遞減，但未另改後段旁白。

## 作者機械檢查與交審

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**；162 句、工具估時 **13.76 分鐘**，開場 **00:45**。正文 **2,606 漢字**，按每分鐘 325 字約 **8.02 分鐘**；`cute-mystery` 插畫鏡頭 **144／162 = 88.9%**，18 排版卡、15 條 loops。固定 5 秒片頭及 21 秒片尾／連結槽位在企劃；尚無可點長片 ID。
- `claims.md`、`video.json`、`script.md` **162／162 ID 與旁白逐字對齊**，ID 無重複。`npm run test:docs-videos` **236 pass／0 fail**；`npm run check:tasks` exit 0（其他既有逾時／重疊警示）。
- 下一步必須由**未參與 R8 修稿者**按本表五檔 SHA 獨立覆核新句史料與書面畫面，再由兩位全新隔離讀者只讀本版 `script.md` 各答固定 13 題，按固定 OR 正式 CLI 合併。R7 的 PASS 不能轉借給 R8。政策、付費語音、插圖、配樂、組片、上傳及站主人工核准皆未執行。
