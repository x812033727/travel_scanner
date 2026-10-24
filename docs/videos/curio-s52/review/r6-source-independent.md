# S52 R6｜獨立逐句史料與書面畫面覆核：PASS／PASS

2026-10-20 UTC。以固定 Cook／Kippis 全文重新核對 [R6 作者凍結](r6-author-freeze.md)的精確五檔、[R5 獨立 HOLD](r5-source-independent.md)的三處必修項、逐句主張表及 119 景書面畫面。**旁白／主張表 PASS；書面畫面 PASS**，只綁下列 hash；不替代隔離盲讀、政策、站台、真實音檢、原生生成圖或成片驗收。

| R6 精確檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `31b4a238af41093392dad81f303ec06512ada452bea37d66eeffa57408ed00d7` |
| `research.md` | `8a2bdbb0767089b1dd5c71397a325618ff3d55437de2bf45815eac3962e7a7a1` |
| `claims.md` | `7caba4680fb2d7db561124b298152eb28606b4e4670b7ce6cd766c9ce1e4c95f` |
| `video.json` | `a515ca252e09d656771f6a4b6ccd510fced1f723211d62f23d52d43644173366` |
| `script.md` | `aeae2ec0be77ec3fe229ac42b561d434136c9b2d7a73b30c1f689b88b5ae0b6f` |

重開 `/tmp/curio-s52-sources/cook-8106.txt` SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`，及 `kippis-7777.txt` SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`；固定 commit URL 見 [research.md](../research.md)。前者是 Cook 日誌經 Wharton 1893 年編輯轉錄，前言另有層級；後者是後出傳記，不是第二套獨立觀測記錄。

| R5 HOLD 位置 | R6 獨立結果 |
| --- | --- |
| `s52204` 口播 | [Kippis L1168–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1168-L1178)末格為下午 **3:32:10**；`video.json`、`claims.md`、重生 `script.md` 均已明確寫「下午三點三十二分**十秒**」，不再多出「分」。前面三格仍為 09:25:42、09:44:04、15:14:08。 |
| `s52205` 主張表 | 「庫克說」現另引 Cook [L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)，其中 L5967–5969 明說兩次內接觸尤其受干擾；Kippis [L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)保留給四格時間及六小時跨度。歸屬和算術各有其來源。 |
| `s52074` 書面畫面 | Cook [L5957–5960](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5957-L5960)寫六月二日 `Very early this morning` 派 Hicks 往島的東面；新提示詞 `early on 2 June 1769`、`cool early-morning light` 與旁白「隔天清早」相符，不虛報精確日出時刻。全景提示詞／卡片再掃未見新的來源或旁白矛盾。 |

復算 Kippis **同一格林表內**：`09:44:04 − 09:25:42 = 18:22`，`15:32:10 − 15:14:08 = 18:02`，進、出兩段相差 **20 秒**，首尾相距 **06:06:28**。R6 `s52201/07/08` 和書面無字表格仍把它們表述為一人的兩段間隔，不冒稱 Cook、Green、Solander 三人彼此的讀秒差。Kippis 在表前散文 `According to Mr. Green`，未被寫成格林原刊或原表欄名。Cook [L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)的六月三日無雲、極清空氣、幾乎無風、午間溫度計、暗影與三人時刻分歧均維持原有來源界線；Wharton 前言的 `June 1st` 誤記未進旁白。四月十五日 Cook [L5370–5425](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5370-L5425)記英國守衛隊奉命開槍打死一名大溪地人，Cook 和 Banks 在半英里外聞槍才回；R6 未把 Cook 畫或寫成現場目擊，也未補死者動機或當地人的獨立證詞。

核 R5→R6 漂移時，將目前 `video.json` 只逆轉 `s52204` 一句及 `s52074` 一個提示詞，重算 SHA 得 R5 凍結值 `bd48108a0f6124baf3ee61f034b4a05b6badbe1ef7e7af7c22b80867e2918603`；同一假設檔的 `screenplay(doc)` 得 R5 `script.md` SHA `76b73d658feb761eea44504cfb65d4b5d7c88ce061938df5e10a99dd7107fafe`。將目前 `claims.md` 只逆轉 `s52204` 文字與 `s52205` 的 Cook 引用／層級，亦得 R5 SHA `fdce7802e559952ee7faa8b7f20cf59bf94731d89acc7a569a49257a8f48176c`。這證明三份逐句／畫面檔除上述三處外沒有差分。`brief.md`／`research.md` 檢過新版本與審查狀態段，未見新增史實來源或變更故事界線。主張表 121 列中 119 列共 149 個固定文字引用，連結格式及行錨有效；另兩列為觀眾互動。

機械重算：119 景＝114 插畫、4 卡、1 片尾，正文插畫 114/118＝96.6%；121/121 句 ID 唯一且與 `claims.md` 依序同字，119 景 ID 唯一，`screenplay(doc)` 與 `script.md` 逐位元相同；114/114 插畫提示詞非空，19 組 setup/payoff 存在且順序有效。`lint --slug curio-s52 --json` **0 errors／0 warnings**；`npm run check:tasks` 驗證 **2,124** 票，`git diff --check` 通過。250／300／325 CPM 的估時開場 **42.90／37.00／34.90 秒**，正文 **557.37／481.60／455.00 秒**；325 CPM 仍只有 **7:35.00**，須真實 TTS 驗證正文八分鐘硬關。`s52014` 檔案室與船旁複合構圖仍屬生成圖時的可讀性 WATCH，沒有把它當史料實景。

**裁決：R6 旁白／主張表 PASS；書面畫面 PASS。** 下一關仍是對 R6 精確劇本的兩位全新隔離讀者盲評，然後才可依關卡做政策、網站及真實語音／畫面；本輪沒有修改作者內容或製作媒體。
