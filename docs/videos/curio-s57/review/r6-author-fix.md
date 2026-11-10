# S57 R6｜作者窄修與凍結交接

2026-10-20 UTC。**R6 只是作者候選稿，尚無新版本的獨立來源或敘事 PASS。**[R5 獨立來源／書面畫面報告](r5-source-independent.md)對固定 R5 五檔 PASS；[R5 正式雙盲合併](r5-merge/summary.md) **12／13 HOLD**，唯一共同未過 `no_recap`。A 單票另異議 `payoffs`、`no_detour`，B 兩題均 YES，正式 OR 已過；本次順手刪去 A 指出的已知答案問句與一個低因果旅途小景。完整 R5→R6 逐行差異見 [patch](r6-author-diff.patch)，SHA-256 `47f68d1af3aa32f5eaabef0a9717e1b27ac8ff792e451e8d6ff839182a9b3695`。

| 五份創作檔 | R5 SHA-256 | R6 凍結 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `25cf00d5d86c8703c459fc1de8774f7adef27059fe4006c93a1b40d7ba14e43f` | `48f287375b22a77929130046c15c55079c78d9376996a033709dc7a1d625b933` |
| `claims.md` | `c238f42f44a612ef92c15a1f14f9ad4d0ef86e8f88724888ceecbba016a65230` | `71b0f3405bd254e7be0d464d34d81c98fb78b08951e046b331ec79a34af03919` |
| `video.json` | `07bebbb202143a25f9d942565303da91859c431c402a31c36f6d2824d9d060d9` | `e766dbe4ac40932abfa5bea1a89713604b2fbb64158bf3523376bde0aa0131cc` |
| `script.md` | `464ba2b1bb7dfd5aedaaf3727e4fcaae28d598050e132e72f1dd1bb99b163452` | `f2d8c42f6b71698121199d7c3c26ddde958eddf1d25be96783356c8ef404ef87` |

## 精確修法

- **共同 `no_recap`：**刪 `s57082`，只留 `s57081` 說初次勸歸早於二月新援助；刪 `s57152`，人手需求、由誰送來、非奴隸條件依 `s57149–s57151` 各說一次。`s57101` 不再重報北岸未定與失貨，改接 **12 月 13 日**史丹利收到美國領事信；`s57104` 接同日亞丁電報，`s57105` 留李文斯頓沒有自己的信，`s57106` 接 **15 日**準備往東取寄存貨。這四景依 [L5420–5430](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5420-L5430) 推進，海岸領事背景另見 [S12363–12384](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L12363-L12384)。`s57189` 不再重報 `s57182` 日記與人分路，明指**回看開場封日記**，收在其水源假說與先完成考察的本人判斷；把假說留作當時信念，[L5741–5769](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5769)。
- **單票異議：**刪 `s57158`「誰送消息」：開場與前句已給史丹利，後面的 `s57164→s57165–s57166` 仍用具體信件回答出發前寫完什麼。刪 `s57119` 獨木舟離開的小景；東行分隊由 `s57117` 問能否會合、`s57118` 立旗，直接到 `s57120` 人與羊到齊，[L5482–5499](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5482-L5499)。其餘東行障礙仍與五十四天找貨路相連，沒有新增純延時段落。

**精確集合：**刪除 `s57082,s57119,s57152,s57158` 四景及對應 claims；更動口播／claims `s57101,s57104,s57106,s57149,s57150,s57151,s57189` 七景；更動 prompt `s57101,s57104,s57106,s57149,s57150,s57151` 六景。新／舊貨、18→19→20 日援助與藏布時序、相遇日僅稱晚秋、S 節錄本與 L 身後編刊日記的證據層級都保留；`research.md` 未改。`script.md` 從新版 `video.json` 重生，15 條 loop 的 setup/payoff 端點仍存在。

## 檢查與交審

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，167 句、工具估時 13.845 分鐘，首章仍在 00:45（30–60 秒濃縮開場）。正文 **2,605 漢字**，按每分鐘 325 字約 **8.02 分鐘**。149／167 景是可愛懸疑插圖（**89.2%**），18 張資訊卡；固定 5 秒片頭及 21 秒片尾卡規格見企劃。
- `claims.md` 與 `video.json` **167／167 逐字對齊**，167 個 ID 唯一。`npm run test:docs-videos`：**236 pass／0 fail**。`npm run check:tasks`：exit 0，僅列其他既有任務提示。
- R5 來源 PASS 與 R5 正式敘事 HOLD 均只適用 R5 雜湊。R6 須重新由獨立來源／書面畫面覆核、兩位新讀者隔離盲讀及正式合併；本報不能替它們判 PASS。未執行付費語音、插圖、配樂，未聲稱人工核准。
