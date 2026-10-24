# S57 R10｜作者窄修與五檔凍結

2026-10-21 UTC。**R10 仍是作者候選；本收據不自判史料、書面畫面、敘事或政策 PASS。**[R9 獨立史料與書面畫面](r9-source-independent.md)為 PASS／PASS；[R9 正式雙盲合併](r9-merge/summary.md)為 12／13 HOLD，兩票共同 NO `no_recap`，A 單票 NO `no_spoiler`。R9→R10 的[精確差分](r10-author-diff.patch) SHA-256 為 `1e6af359f9e2992fe60f0946f1a98ded9f9486664710a35e779083a1c117808c`。

| 創作檔 | R9 SHA-256 | R10 凍結 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `c7900d23f61699c506abbde288aadbe2d32c0e5020721a2e2c44ee04ff2876ea` | `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd` |
| `claims.md` | `241f5a2fa4b25e977baf832907213b7be98cda7a9cfa55ea58331f0a31466beb` | `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` |
| `video.json` | `940046297c87511a82c9e42eb5d0c0fbcf8bdaa9b5528ce17234ac77c7cf8588` | `0275fe764a2a79ee0d122780853bb3bfa21922c86a4f650475c7dc6c1fb39d2f` |
| `script.md` | `7edc924366e588787794e9c2ceac53ce8f5131188f19aa9c0a71a3543c326b43` | `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` |

## R9 意見的局部處理

1. **開場留待後章揭示失貨。**`s57007` 改為「病痛之外，他還得替下一段路備貨」，依[李文斯頓日記 L5219–5228](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5219-L5228)；畫面改為合上素面行李箱，不揭空箱。`s57008` 改成「等物資到手，他就會改變主意嗎？」並只望向遠處小徑；[L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804)記後段新援助，開場未說已送到或預告最終抉擇。
2. **兩年歐洲消息只說一次。**`s57053` 合併「兩年沒聽到」與「史丹利帶來不少」，刪除原先再說兩年的 `s57055` 資訊卡；`s57054` 仍給大西洋電報線這一具體新聞。依[日記 L5262–5268](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5262-L5268)。
3. **明確回收開場日記。**`s57167` 明說「還記得開場那本日記嗎」，並按[日記 L5878–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5878-L5881)交代三月十四日封好託給正要出發的史丹利。這是開場預告的回扣；書面畫面仍單人、單動作，不重建兩人交接。

解析 `video.json` 的精確集合是改四句 `s57007,s57008,s57053,s57167`、刪 `s57055`、改兩個 prompt `s57007,s57008`；其餘場景及頂層元資料未改。`brief.md`、`claims.md` 同步 R10 狀態與逐句來源，`script.md` 由 `node tools/video/cli.mjs script --slug curio-s57` 重生。`research.md` 不變。史丹利出版節錄與 Waller 身後編刊日記的來源層級、精確相遇日 HOLD、二月 **18 日新援助→19 日藥品→20 日舊藏布**的順序均不變。

## 作者機械檢查與交審界線

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，159 句，工具估時 **13.80 分鐘**，濃縮開場 **00:45**；開場後正文 **2,627 漢字**，按每分鐘 325 字約 **8.08 分鐘**。142／159 景為 `cute-mystery` 插畫（**89.3%**），17 張資訊卡，15 條 loops。
- `claims.md`、`video.json`、`script.md` **159／159 ID、順序及旁白逐字對齊**，無重複 ID；`npm run test:docs-videos` **236 pass／0 fail**；`npm run check:tasks` 凍結時 **exit 0，Validated 2366 task files**。
- [企劃](../brief.md)保留 30–60 秒濃縮開場、第一章後固定 5 秒品牌動畫、固定 21 秒全站片尾及推薦／訂閱連結槽位；真實影片 ID 仍待製片後取得。
- 需由非作者對以上五個**精確 SHA**重新覆核史料與書面 prompt，並由兩位全新 `fork_turns:none` 讀者只讀新 `script.md` 和固定 13 題，在各自原票凍結後正式固定 OR 合併。本作者收據不替代那些票。未執行付費語音、插圖、配樂、組片、上傳、政策核准或站主核准。
