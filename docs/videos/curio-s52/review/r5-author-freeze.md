# S52 R5｜敘事 FAIL 後的作者修稿凍結

2026-10-20 UTC。[R4 獨立史料及書面畫面](r4-source-independent.md)只對當時精確稿 PASS／PASS；[R4 官方雙盲](r4-official-panel.md)因兩位讀者共同判 `no_recap` No 而 **FAIL**。讀者 B 另指出四月岸界佔用第二條故事線與首章抽象標題。R5 是作者候選，以下本地檢查均不構成新版獨立簽核，也不放行政策、站台或任何付費媒體。

| R5 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `55cf7f8e9c2c8daa2dbeb5154d2c276b9f607e4d6a82429b1da27cc5ef2bb069` |
| `research.md` | `211fd9d4a38a287237ca5d5724d84131533349b0ac50e4207cacad0281b0eb06` |
| `claims.md` | `fdce7802e559952ee7faa8b7f20cf59bf94731d89acc7a569a49257a8f48176c` |
| `video.json` | `bd48108a0f6124baf3ee61f034b4a05b6badbe1ef7e7af7c22b80867e2918603` |
| `script.md`（CLI 重生） | `76b73d658feb761eea44504cfb65d4b5d7c88ce061938df5e10a99dd7107fafe` |

## R4 → R5 差分與證據界線

| 位置 | 作者修改與理由 |
| --- | --- |
| `s52001` 章名、`s52005` | 首章改為事件「六月三日，三人看見金星」；開場原本追問岸界，現問皇家學會為何派人遠赴南太平洋，直接掛上讀時主線與 `s52016` 目的說明。`s52005` 書面畫面改為無字請求書與天象示意，不再提前切去岸界。 |
| 四月章 `s52028–53` | 由 **22 景收為 14 景**，章名改「四月十五日，選定觀測岸地」。刪除 `s52032/33/34/37/40/45/50/52` 八個旁枝或重問；章前 `s52027` 亦刪。保留有人生活的海灣、英國選址與武裝安排、當地人未帶武器、庫克不知道對方是否聽懂、守衛隊開槍打死一人、庫克不在現場以及次日觀測安排繼續。`s52038` 加一句短問，隨即由 `s52041` 回答；`s52048→53` 明接觀測站準備。來源仍限 Cook 經 1893 年轉錄的日誌 [C L5375–5437](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5375-L5437)；不補死者動機或大溪地人同意。 |
| `s52083` 與 `s52206` | `s52083` 不再原字重說開場無雲，改用 Cook 日誌新資訊「空氣極清、幾乎無風」；`s52206` 記中午曝曬的溫度計達庫克此前未遇過的熱度，沒有虛報溫度數字。兩句只烘托有利觀測天氣，仍由眼前接觸邊緣的問題推進主線。[C L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975) |
| `s52201–05/07/08` | 新加格林表內的時間進程：早上 09:25:42 → 09:44:04 是 **18:22**；下午 15:14:08 → 15:32:10 是 **18:02**；兩段相差 **20 秒**，首尾共六個多小時。這是**同一人表內兩段接觸間隔**的直接算術，不是庫克、格林、索蘭德彼此的秒差。下午兩格的原數字第一次在片中說出；新問句引向 `s52097` 的兩次內接觸難判。[K L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)。畫面為原創空白／無可讀數字的示意表，不冒充原件。 |
| `s52096`、`s52108`、`s52129–31`、`s52133–35` | 刪去重問哪兩格難看、再說晴天、重講三人秒差無法算出、以及片尾將故事拉回岸界的句子。四月事件的來源限制仍在 `s52041/42/47/48` 與說明欄；結尾沿六月四日「成功」的來源層級回到接觸時刻。 |

兩份固定全文仍是 `/tmp/curio-s52-sources/cook-8106.txt` SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536` 與 `kippis-7777.txt` SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`。未加新來源；`brief.md`／`research.md` 只同步版本、下一關和算術核查點。R4 的獨立 PASS 不沿用到這五個 R5 hash。

作者本地機械檢查：`video.json` **119 景**（114 插圖、4 卡、1 片尾），**121/121** 旁白 ID 唯一且與 `claims.md` 同序同字，`screenplay(doc)` 與 `script.md` 逐位元相同，**19 組** setup/payoff 均存在且順序有效；`lint --slug curio-s52 --json` **0 errors／0 warnings**。`estimateTimeline` 在 250／300／325 CPM 的濃縮開場 **42.90／37.00／34.90 秒**，開場後到片尾前正文 **557.60／481.80／455.20 秒**。最快估值 **7:35.20** 低於八分鐘，故實測語音時長是硬關；若不足八分鐘，須先補有來源且不重複的內容，再重做獨立審查，不以靜音拉長。

`npm run test:docs-videos` **236/236**、`npm run check:tasks` **2,124 票**、`git diff --check` 通過。沒有製作或支付 S52 語音、插圖、配樂、動畫、成片。下一手對上述五個精確 hash 重新獨立核逐句來源和書面畫面，特別重算 Kippis 表的三個算術值；另交兩位此前未讀 R5 的隔離讀者只讀此版劇本做固定 13 題。來源／畫面與雙人敘事都通過後，再走政策、站台劇本卡、真實音檢及媒體關卡。
