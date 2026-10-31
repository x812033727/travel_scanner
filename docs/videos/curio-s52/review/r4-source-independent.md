# S52 R4｜獨立逐句史料與書面畫面覆核：PASS

2026-10-20 UTC。另以固定 Cook／Kippis 原文核對目前 R4 [劇本](../script.md)、[主張表](../claims.md)和所有書面畫面，不以 [R4 作者凍結](r4-author-freeze.md)的自評當史料證據。**旁白史料 PASS；書面畫面 PASS**，只綁下列精確五檔。本裁決不替代兩位隔離盲讀、政策、網站選案、真實音檢、生成原圖或成片。

| 精確 R4 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `b210bf20e6889582698219c1d312484e1a2719b232df28a48dac781db97e3853` |
| `research.md` | `c2f4be9174b3bd38b9f8266c203ab9b0230e0884be4a574a6c7c9a21b64832af` |
| `claims.md` | `2e71db60d895537048ff4924be6d6a24e22c525b1b4131b9998f16891c832c2a` |
| `video.json` | `c04ac4cf66e38741299072a28c3625f95c4a8f1de2df811972d76aa2eacca134` |
| `script.md` | `89d271cea67b1e355f343f21fc90793218edc6d3880c2f0c50858fea3d818996` |

重開 `/tmp/curio-s52-sources/cook-8106.txt`，SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`，及 `kippis-7777.txt`，SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`；固定 commit URL 見 [research.md](../research.md)。Cook 是 1893 年 Wharton 編輯轉錄的 1769 年日誌；其前言不是當日口供。Kippis 是後出英國傳記，不能算第二組獨立天文記錄。

## R3 HOLD 與 R4 主要差分

| 位置 | 對原文與畫面的獨立判讀 |
| --- | --- |
| `s52009–14` | Kippis [L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)明記 1768-02-15 皇家學會請求派船觀測 1769 金星凌日、其他歐洲宮廷的關注、王室同意由學會選人、04-03 回報已找到船；新章首及日期、機構歸屬有據。畫面用空白請求、封緘和資料卡，不冒作可讀原件。`s52016–18` 把日地距離目的明歸 Wharton **1893 年前言** [C L793–803](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L793-L803)。 |
| `s52019→26` | K L598–624 的候選地是馬克薩斯或友誼群島，沒有把大溪地列成已定落腳點。R4 `s52019` 問最後去哪裡，`s52026` 才說船到大溪地，已撤去 R3 無直接來源的「派船者重點是互相比較」斷言。`s52026–28` 的海灣有人、沙岸開闊，與 Cook [C L5375–5396](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5375-L5396)同時記當地人在場和選址 `not near to any of their Habitations` 相容；`s52028` 新提示詞已刪近旁屋舍，不把整個海灣說成無人。 |
| `s52033–53` | C [L5375–5437](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5375-L5437)支持交換物資、英國人畫界而庫克不確定對方是否懂、留守隊帶隊者下令開槍打死一名大溪地人、庫克與 Banks 約半英里外聽槍才返、次日船移近岸並有人帶椰子來。R4 把死亡明歸**庫克回來後的日誌**，不增造死者動機、當地集體同意或庫克現場目擊；`s52046` 是非血腥文字卡。刪四個過場後，`s52048/53` 把武裝岸界與觀測站是否續設連回金星觀測。`s52050` 的「控制岸線」對應 C 4 月 16 日 `command all the shore`。 |
| `s52065/66`、`s52076` | 兩句假回收及其伏筆已撤，後文仍按 C [L5941–5961](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5941-L5961)記 05-30 練儀器、06-01 Gore／Banks 等去 Eimeo、06-02 Hicks 往大溪地東面。`s52076` 畫面日期已從四月改 `early June 1769`，沒有把等待六月三日畫成四月當天。 |
| `s52090/94`、`s52116–18` | K [L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)在四列時間**之前的散文**寫 `According to Mr. Green,`，表內沒有格林姓名標題或欄。R4 說「表前只註明」，`s52116/17` 提示詞改成無字表前散文與四列，移除 R3 虛構表頭；卡片仍標 Kippis 後出轉錄。09:25:42、09:44:04 與 K 表相同；此表只印格林一組，故不拿它計 Cook／Solander 的秒差。 |
| `s52135` | 現說這兩份**英國文本**沒有死者或同行大溪地人的**獨立證詞**，不再暗示完全沒有大溪地人的言行。K [L1026–1030](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1026-L1030)仍轉述 Owhaw 以手勢傳話；R4 限定詞與此相容，畫面是後來證據桌，未把編輯畫成 1769 岸邊見證。 |

其餘保留的核心邊界再核：Cook [C L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)當日日誌確定是 **06-03** 無雲、三人觀測、內接觸受「大氣或暗影」干擾、記時差超預期、Solander 倍率較大；C 編者前言 L1069–1073 的 `June 1st` 誤記未被正文沿用。R4 沒把暗影斷定為現代單一光學成因，也沒畫裸眼直視太陽或捏造濾光器構造。C [L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)的 `return'd with success` 被明說是 Cook 的評語，沒有據此填補其他兩隊的精確秒數或宣稱全任務失敗。

機械對齊獨立重算：`video.json` **128 景**，其中 123 個 `shot`、4 卡、1 片尾；正文插圖 **123/127 = 96.9%**。**130/130** 句 ID 唯一，`claims.md` 依 ID、順序、旁白字面 **130/130** 相同，`screenplay(doc)` 與 `script.md` 逐位元同一份；123/123 提示詞非空，17 組伏筆 setup/payoff 均指有效且前後有序。`lint --slug curio-s52 --json` **0 errors／0 warnings**，`git diff --check` 通過。`estimateTimeline` 在 250／300／325 CPM 的濃縮開場 **42.43／36.60／34.53 秒**，其後到片尾前正文 **596.03／515.20／486.87 秒**；最快仍為 **8:06.87**，這是估值，尚需 TTS 實測。`s52014` 的「檔案室」與「船旁」同景構圖可能使生成圖空間不清，屬原生畫面驗收時的 WATCH，沒有當作某張歷史照片或原件重建。

**裁決：R4 旁白史料 PASS；書面畫面 PASS。** R3 的 HOLD 不沿用成 R4；本 R4 裁決也不能讓缺少的雙人盲讀、政策、網站或媒體關卡自動過。未製作付費媒體。
