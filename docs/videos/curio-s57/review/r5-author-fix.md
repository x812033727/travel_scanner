# S57 R5｜作者敘事窄修與凍結交接

2026-10-20 UTC。**R5 是作者候選稿，不是獨立 PASS 或媒體放行。**[R4 獨立來源與書面畫面覆核](r4-source-independent.md)對固定 R4 五檔 PASS；[R4 正式雙盲合併](r4-merge/summary.md)為 **9／13 HOLD**，未過 `chapters_link`、`payoffs`、`no_recap`、`no_detour`。本次只對這四項具體斷點改寫，保留原先 2 月 18→19→20 日時序。完整逐行版本差異見 [R4→R5 patch](r5-author-diff.patch)，SHA-256 `7683e45c445dace072739b75531f52be691248264c40f0566e2a29b26272201a`。

| 檔案 | R4 SHA-256 | R5 凍結 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `50b4f5f48f9ef82b18f25ff8f681014bd658cb45955101e109574658f34de139` | `25cf00d5d86c8703c459fc1de8774f7adef27059fe4006c93a1b40d7ba14e43f` |
| `claims.md` | `07c3d2ea5ea29d7d7ce68deb020c09b72a0dd424cfe548224a32039473e30b72` | `c238f42f44a612ef92c15a1f14f9ad4d0ef86e8f88724888ceecbba016a65230` |
| `video.json` | `bf2d6d429fca78f3a66620b114ee8333b4f91d2e37262a25d24fedac3ea1d4a8` | `07bebbb202143a25f9d942565303da91859c431c402a31c36f6d2824d9d060d9` |
| `script.md` | `a375377e0ced91d83be01650bb4e55fb6845de4e463d542302938d3de58fe6ce` | `464ba2b1bb7dfd5aedaaf3727e4fcaae28d598050e132e72f1dd1bb99b163452` |

## 四個阻擋點的具體修訂

- **章節連接：**開場分路問題之後，首章 `s57011` 改成帶病回烏吉吉尋續行補給的動作，不再重複「分路難題」標籤；對應 [L5181–5228](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5181-L5228)。章五已說往東離村，章六首景 `s57113` 現直接進入首日盧伊切河渡河障礙，[L5455–5466](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5455-L5466)，不再報一次離烏吉吉。
- **問題回收：**`s57107` 從無法回答的「舊箱還剩多少」改問是否**完整**，`s57136` 明答舊貨仍短少，[L5783–5794](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5783-L5794)。`s57128` 分開問史丹利自己的儲物間是否有貨，由 `s57133` 回答；`s57117→s57120` 問答水陸兩隊會合，`s57122→s57127` 以日記自估五十四天回答行程長度。`loops` 相應更新為 15 組。
- **免重述：**移去 `s57049–s57051` 的名句出處停頓及重複入屋敘述，單一來源界線仍留在研究／企劃；`s57069` 問李文斯頓日記如何記選擇，`s57072` 直接回答，刪 `s57070–s57071` 同一勸歸提議的重演。`s57139` 用「抵達當天」承接 `s57131` 的 2 月 18 日，`s57184–s57186` 的找到人、等人手與無保證總結刪去，直接回答 `s57183` 的回家問題。完整對白仍只歸史丹利出版節錄本；日記只記勸歸及本人判斷，[S10270–10282](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L10270-L10282)、[L5741–5751](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5751)。
- **免岔題：**`s57114–s57123` 由天氣、岩坡畫面串列，改成渡河、前方無糧而先買豆、風暴停留、水陸隊伍待會合、病倒後再動身的時序。這些障礙共同回答為何找貨走了五十四天；刪 `s57124–s57126,s57130` 的地形與來源重述。新逐日主張及 prompt 依 [L5458–5502](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5458-L5502)，沒有把所有行程畫成精確路線圖。

為區分舊貨與新援助，`s57020` 明引日記所述原存 **三千碼布／七百磅珠**，`s57133–s57136` 分開史丹利的儲物間與李文斯頓原有箱子，`s57144` 明說 20 日拿回一包後**仍缺四百多碼**，且回指 18 日新援助已作續行本錢，[L5219–5228](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5219-L5228)、[L5796–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5818)。這些均歸屬日記記述，沒有替失貨指控定罪或把史丹利援助當成找回的舊箱。相遇日仍只說 1871 年晚秋，尼羅河源仍只作本人當時信念。

精確變更集合：**24 個口播／claims 列** `s57011,s57020,s57069,s57072,s57107,s57113,s57114,s57115,s57116,s57117,s57118,s57119,s57120,s57121,s57122,s57123,s57127,s57128,s57129,s57133,s57135,s57136,s57139,s57144`；**12 個刪除景及其 claims 列** `s57049,s57050,s57051,s57070,s57071,s57124,s57125,s57126,s57130,s57184,s57185,s57186`；**19 個 prompt** 隨口播或刪景修正，清單以 diff 為準。`research.md` 未改；`script.md` 由新版 `video.json` 重新生成。

## 版本檢查與後續

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，171 句、13.98 分鐘估算；開場仍為 45 秒。第一章起的正文有 **2,621 漢字**，按 325 字／分約 **8.06 分鐘**。153／171 景為可愛懸疑插圖（**89.5%**），18 張資訊卡，15 條 setup/payoff；固定 5 秒片頭與 21 秒片尾卡仍在企劃。
- 主張表與口播 **171／171 逐字吻合**，171 個 ID 唯一，全部 loop 端點存在。`npm run test:docs-videos`：**236 pass／0 fail**。`npm run check:tasks`：exit 0，僅印其他既有任務提示。
- R4 來源 PASS 只適用 R4 五檔。R5 必須另請獨立來源／書面畫面覆核、兩位無前情讀者各自盲讀與正式合併；此作者收據不代替任何一關。未呼叫付費語音、插圖、配樂，未自行宣稱人工核准。
