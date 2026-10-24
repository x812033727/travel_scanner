# S52 R4｜史料 HOLD 與雙盲 FAIL 後的作者定點修訂

2026-10-20 UTC。R3 的[獨立逐句來源與書面畫面](r3-source-independent.md)為 **HOLD／HOLD**，兩位新讀者的[正式合併敘事](r3-official-panel.md)為 **FAIL**（共同 `chapters_link`、`no_recap`）。R4 只是一份**作者候選**；以下檢查不能當作 R4 的獨立來源、書面畫面、敘事或媒體放行。

| R4 五檔內容 | SHA-256 |
| --- | --- |
| `brief.md` | `b210bf20e6889582698219c1d312484e1a2719b232df28a48dac781db97e3853` |
| `research.md` | `c2f4be9174b3bd38b9f8266c203ab9b0230e0884be4a574a6c7c9a21b64832af` |
| `claims.md` | `2e71db60d895537048ff4924be6d6a24e22c525b1b4131b9998f16891c832c2a` |
| `video.json` | `c04ac4cf66e38741299072a28c3625f95c4a8f1de2df811972d76aa2eacca134` |
| `script.md`（CLI 重生） | `89d271cea67b1e355f343f21fc90793218edc6d3880c2f0c50858fea3d818996` |

## R3 → R4 精確修補

| 位置 | 改動與來源邊界 |
| --- | --- |
| `s52009–14` | 章首第一句直接說皇家學會**為金星凌日**向國王請船，接住開場的觀測難題；後五句改成南太平洋目的地、2 月 15 日請求書、歐洲其他宮廷的關注、國王答應及 4 月 3 日找到船的順序，刪去 R3 連續重說派船目的的口吻。均見固定 Kippis [P L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)；`s52012/13` 的提示詞同步從經費帳與天象圖改為無字請求／人選資料。 |
| `s52019→s52026` | 撤掉「派船者主要想拿互相比較觀測」的超證據因果。K [P L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)列當時的候選島嶼，尚未定大溪地；新句問最後在哪裡落腳，`s52026` 船抵大溪地回收，並添一條實際伏筆。`s52025` 收成找觀測岸地；研究 R01 不再聲稱多地比較是派船者的首要目的。 |
| `s52028–53` | 保留 4 月 15 日沙岸設觀測處、船炮射程、當地人與歐瓦、英國人畫線、理解不確定、守衛隊開槍打死一名大溪地人、庫克非現場目擊及次日船移近岸；刪去 4 個重述／過場景（`s52031/39/43/51`），把小堡、歐瓦和留守者合入鄰句。`s52048/53` 直接把開槍與武裝岸界接回觀測站能否繼續準備，處理盲讀者的旁支疑慮。Cook 固定日誌 [C L5375–5437](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5375-L5437)為**庫克視角**；沒有增造死者動機、當地同意或現場目擊。`s52028` 畫面刪近旁屋舍，因 C L5393–5396 明說選址**不在住處旁**，保留有人生活的海灣。 |
| `s52065/66` | 刪去「三處都能看見，下一關？」接「仍要記接觸時刻」的假回收和對應伏筆；`s52064` 後直接進六月一日分遣，主線與鉤子仍連續。 |
| `s52076` | 書面畫面從 `April 1769` 改 `early June 1769`，對齊旁白所在的六月二日等待階段；只改提示詞，不改該句史實。 |
| `s52090/94`、`s52104`、`s52117–20` | 前段只先念四個接觸時刻及 Kippis 的表，不提前說表是格林**單人**；刪去後段重說「兩次內接觸」的 `s52104`。結尾改成 Kippis **表前散文** `According to Mr. Green,`，再說表沒有庫克／索蘭德的秒數；刪掉 `s52119/20` 兩句重述。表前引介與四時刻見 [K L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)。`s52116/17` 提示詞改無字書頁前引介與四列，刪掉假的「格林表頭／姓名欄」。卡片仍註 `Kippis 後出轉錄`，不冒充格林原刊。 |
| `s52135` | 將「島上的人沒有在兩本書裡自己說話」收窄為**沒有死者或同行大溪地人的獨立證詞**；承認英國文本仍有轉述其言行。畫面改成後來查證桌，不把後出的編輯畫在 1769 年岸邊。 |

固定原文仍是 `/tmp/curio-s52-sources/cook-8106.txt` SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536` 與 `kippis-7777.txt` SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`；無新來源。除上表 9 個刪除 ID、17 處句子與 8 個提示詞外，其餘景與資料仍沿 R3；`brief.md`／`research.md` 只同步流程與已查的來源界線。無付費呼叫。

作者本地核對：`video.json` **128 景**（123 插圖、4 卡、1 片尾），**130/130** 句 ID 唯一且與 `claims.md` 同序同字，123/123 插圖提示詞非空，17 條伏筆有效。`lint --slug curio-s52 --json` 為 **0 errors／0 warnings**。`estimateTimeline` 在 250／300／325 CPM 時濃縮開場 **42.43／36.60／34.53 秒**，其後至片尾前正文 **596.03／515.20／486.87 秒**；最快 **8:06.87** 是文字估值，仍須真實 TTS 實測。`npm run test:docs-videos` **236/236**、`npm run check:tasks` **2,123** 票通過（其他票有既有提醒）、`git diff --check` 通過。供新盲讀者的純旁白與固定題規 `/tmp/s52-r4-narrative-input.json` SHA `0ad12dfe7b64b371567cbe787470de54bd99e888aaff65ca209de88c39d8f2f2`。

**下一關：**另一位工作者按上表 R4 精確五檔與固定原文獨立覆核新句、畫面及未改部分的層級；兩位此前未讀 R4 的隔離讀者各只讀新劇本按 13 題盲評。R3 的 HOLD／FAIL 與作者本地檢查均不放行 R4 的政策、站台審核、語音、插畫、配樂、成片或上傳。
