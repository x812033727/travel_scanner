# S57 R5｜獨立史料與書面畫面覆核

2026-10-20 UTC。**史料／逐句主張 PASS；書面畫面 PASS，僅限下列固定 R5 五檔。**我未參與 R5 作者修稿；先讀 [R4 獨立來源 PASS](r4-source-independent.md)、[R4 正式敘事 HOLD](r4-merge/summary.md)、[R5 作者交接](r5-author-fix.md)與完整 [R4→R5 差異](r5-author-diff.patch)，再讀完五檔，逐 ID 對照兩份固定電子原文。R5 差異檔 SHA-256 是 `7683e45c445dace072739b75531f52be691248264c40f0566e2a29b26272201a`。本報不是敘事雙盲、政策、實際生成插圖、語音、配樂或成片的核准；未改五份創作檔，未呼叫付費媒體。

| 固定檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `25cf00d5d86c8703c459fc1de8774f7adef27059fe4006c93a1b40d7ba14e43f` |
| `claims.md` | `c238f42f44a612ef92c15a1f14f9ad4d0ef86e8f88724888ceecbba016a65230` |
| `video.json` | `07bebbb202143a25f9d942565303da91859c431c402a31c36f6d2824d9d060d9` |
| `script.md` | `464ba2b1bb7dfd5aedaaf3727e4fcaae28d598050e132e72f1dd1bb99b163452` |

## 固定原文與全稿對齊

重新核對 [S：史丹利《How I Found Livingstone》節錄出版文字](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt)，原始檔 SHA-256 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`；以及 [L：Waller 1874 年身後編刊《最後日記》第二卷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt)，原始檔 SHA-256 `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`。S 的書名頁明記 *Abridged*；L 是編刊文本，末段死訊另據蘇西、楚馬追述與編者判斷。以下行號只屬上述固定電子文字，不能當親筆手稿頁碼或現場錄音。

全稿核對結果：`video.json` **171 個唯一場景**，`claims.md` **171 列**與 `script.md` **171 句**按 ID、順序及口播文字 **171／171 相同**；八個章名與起點一致。153 個 `shot`、18 個 `big`，15 條 `loops` 的端點存在且 setup 在 payoff 之前。`claims.md` 有 **197 次引用、48 個不同固定原文連結**，皆指向 S／L 指定提交且行號在原文範圍內。逐句閱讀仍以原文語義為準，這些機械檢查不能單獨證明史實。

## R5 改動的史料與時序

| R5 位置 | 固定原文與判讀 |
| --- | --- |
| `s57010→s57011` 回溯到 1871 年晚秋李文斯頓帶病回烏吉吉尋續行補給；`s57020` 說他日記所述原存三千碼布、七百磅珠。 | [L5181–5188](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5181-L5188) 記痛楚與虛弱，[L5219–5228](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5219-L5228) 記託管貨短少與數字。片中仍把失貨歸屬他的記述，不獨立判定罪責；「晚秋」未假定有爭議的精確相遇日。 |
| 刪 `s57049–s57051` 名句出處岔段；`s57069→s57072` 改為一問一答的兩個視角。 | 名句只在 [S9530–9555](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9530-L9555) 的出版敘述；刪除不引入新史實。勸歸與先完成工作可對 [S10270–10282](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L10270-L10282) 及 [L5741–5751](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5751)；完整對白仍只歸 S，六七個月只作其刊出的當事人估計。 |
| `s57107→s57136` 現問舊箱是否完整、回答仍短少；`s57128→s57133` 另問史丹利自己的儲物間有無援助。 | [L5783–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5783-L5804) 明分李原有貨與史丹利貨，[S13786–13797](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L13786-L13797) 另記開李的舊箱。R5 不虛構舊箱「剩餘總量」，書面 prompt 把兩批貨分開。 |
| `s57111→s57113` 直接由東行接第一天盧伊切河；`s57114–s57123` 依渡河、缺糧買豆、新年風暴、一月二日立旗、四日仍待陸隊、五日到齊且史丹利發燒、六日轉好推進；`s57127` 報五十四天自估。 | [L5455–5502](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5455-L5502) 逐日支持；四日日記說獨木舟**前夜**已離開，口播用「已離開」，沒有改成當天出發。[L5779–5781](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5779-L5781) 自估 12 月 26 日到 2 月 18 日為五十四天、三百多英里；另頁 [L5458–5459](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5458-L5459) 記 27 日離村，所以 R5 只說東行第一天，未強定離村日。 |
| `s57137–s57144` 先提舊布去處，18 日抵達與新援助、19 日藥箱和藥品、20 日舊布包取出且仍缺四百多碼；18 日續行判斷是明示回指。 | [L5783–5794](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5783-L5794) 只記有人提到布包，不是已取回；[L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804) 記 18 日史丹利援助與續行計畫；[L5806–5810](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5806-L5810) 記 19 日藥箱／藥品；[L5812–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5812-L5818) 記 20 日拿出布包後還缺 **436½ 碼**。新援助沒有畫成拿回的舊布。 |
| `s57183→s57187` 直接回答後來是否返家，刪 `s57184–s57186` 的重述。 | [L5873–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881) 記 1872 年 3 月 14 日分別與五道封印；[L9976–9985](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L9976-L9985)、[L10254–10272](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L10254-L10272) 是身後編刊追述與編者推斷，片中保留「1873 年 5 月初」而非確定死於 5 月 1 日。 |

## 書面畫面裁決與界線

R5 新增與修改的 prompt 已逐景對照口播和固定原文。舊貨箱與史丹利援助分開呈現；`s57137` 只畫關閉的貨倉，`s57143` 才畫布包拿出；東行呈現當地搬運者、船夫與陸隊，並未畫出精確路線圖。`s57119` 的離舟畫面配口播「四日的日記記……已離開」，只作前夜離開的示意，不應在實際圖片／剪接標成四日當下啟航。`s57121` 的 `closed-cover journal` 字面較不清楚，實際生成圖須見到抄寫動作與不可讀頁面；這是後續圖片驗收的清晰度點，未形成固定稿內的歷史反證。其餘書面 prompt 未查到顛倒二月時序、將假說畫成確證、偽造可讀原件、抹掉在地參與者或把未走路線畫成已完成的阻擋矛盾。**實際生成畫面仍須另關檢查。**

相遇精確日仍有 [S9305–9307 的 11 月 10 日](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9305-L9307) 與 [L5252–5263 斜體圓括號的 10 月 28 日](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5263) 歧異；旁白、卡片和縮圖只到年份／季節。尼羅河源仍明指當事人當時的研究信念。這些界線延續 R4，R5 沒有越界。

## 檢查與下一關

`node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，171 句、估時 **13.976 分鐘**。`npm run test:docs-videos`：**236 pass／0 fail**。`npm run check:tasks`：**exit 0**，列其他任務既有 stale／scope 警告。以上均在五檔 SHA 未變時執行。史料／書面畫面 PASS 只允許這份 R5 凍結稿進兩位新讀者的隔離敘事盲評與正式合併；敘事、政策及媒體關卡仍各自獨立。
