# S52 R5｜獨立逐句史料與書面畫面覆核：HOLD／HOLD

2026-10-20 UTC。重開兩份固定全文，逐行核對 R5 [主張表](../claims.md)、[分鏡資料](../video.json)、[劇本](../script.md)、企劃與研究；以 [R4 獨立 PASS](r4-source-independent.md)及 [R5 作者差分](r5-author-freeze.md)定位修訂，但不沿用舊版裁決。**旁白／主張表 HOLD；書面畫面 HOLD**，只對下列五個精確檔案有效。本審查不代表雙人敘事、政策、站台、實測語音或生成媒體通過。

| R5 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `55cf7f8e9c2c8daa2dbeb5154d2c276b9f607e4d6a82429b1da27cc5ef2bb069` |
| `research.md` | `211fd9d4a38a287237ca5d5724d84131533349b0ac50e4207cacad0281b0eb06` |
| `claims.md` | `fdce7802e559952ee7faa8b7f20cf59bf94731d89acc7a569a49257a8f48176c` |
| `video.json` | `bd48108a0f6124baf3ee61f034b4a05b6badbe1ef7e7af7c22b80867e2918603` |
| `script.md` | `76b73d658feb761eea44504cfb65d4b5d7c88ce061938df5e10a99dd7107fafe` |

固定原文：`/tmp/curio-s52-sources/cook-8106.txt` SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`（Cook 當日日誌經 Wharton 1893 年轉錄；編者前言另層），`kippis-7777.txt` SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`（後出傳記，不是第二組獨立觀測）。完整固定 commit URL 見 [research.md](../research.md)。檢查主張表 121 列中 119 列的 148 個引用：均指向這兩份固定文字及有效行錨；另外兩列是觀眾互動。不過行錨格式正確不保證每條都覆蓋所說內容。

## R5 差分與原文核對

| 範圍 | 獨立核對 |
| --- | --- |
| 開場與四月章 | `s52005` 向皇家學會派人之因設問，Kippis [L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)確記請船觀測金星凌日；章名已指向六月三日事件。四月章由 R4 的 22 景縮成 14 景，所留 `s52028–49` 與 Cook [L5370–5437](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5370-L5437)相符：四月十五日英國人選岸地、留守隊奉令開槍打死一名大溪地人，Cook 與 Banks 約半英里外，聞槍後才返回；次日船移近岸。旁白未補死者動機、當地人同意或 Cook 現場目擊。`s52048` 明稱是他回來後的記述。 |
| 天氣與器材 | 新 `s52083` 的空氣極清、幾乎無風及 `s52206` 的午間曝曬溫度計達此前未遇熱度，均直接見 Cook [L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)；未捏造溫度數值。凌日日期依 Cook **六月三日當日日誌**，未沿用 Wharton 前言 [L1069–1073](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L1069-L1073)的 `June 1st` 誤記。 |
| 格林四格與算術 | Kippis [L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)在表**前散文**寫 `According to Mr. Green`，然後列 09:25:42、09:44:04、15:14:08、15:32:10。重算上午 `09:44:04 − 09:25:42 = 18:22`，下午 `15:32:10 − 15:14:08 = 18:02`，兩段相差 `00:20`，首尾 `06:06:28`。R5 `s52201/07/08` 明說這是格林**同一人表內**的進、出兩段，不是 Cook／Green／Solander 的觀測者秒差。`s52097` 所問兩次內接觸難判，直接見 Cook [L5967–5970](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5967-L5970)。 |
| 仍保留的來源界線 | 1893 編者 [L793–803](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L793-L803)才說觀測為改善日地距離；Cook [L5967–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5967-L5975)的「大氣或暗影」未被改成已證實的現代單因。六月四日分遣隊 `return'd with success` [L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)仍明歸 Cook 的評語，不虛構另外兩隊各人秒數。 |

## 必修項

| 位置 | 問題與最窄修補 |
| --- | --- |
| `s52204`，`video.json`／`claims.md`／`script.md` | Kippis 末格是 **15:32:10**；口播目前寫「下午三點三十二分**十分秒**」，秒的量詞多出一個「分」，聽來不是清楚的 15:32:10。應改「下午三點三十二分**十秒**」，同步主張表及重生劇本。算術本身正確，但精確到秒的口播須可明確唸出。 |
| `s52205`，`claims.md` | 「庫克說哪兩格最難看清？」的唯一引用是 Kippis [L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)，未覆蓋 **Cook 說** 及兩次內接觸較難判；補 Cook [L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)，原 Kippis 引用留作六小時算術依據。此為引用不完整，事實在 Cook 原文有據。 |
| `s52074`，`video.json` | 旁白「隔天**清早**，希克斯又往大溪地東面走」與 Cook [L5957–5960](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5957-L5960) `Very early this morning` 一致；提示詞卻指定 `late afternoon light`。改為清晨光線再審新 `video.json` hash。這處沿自 R4，前次 PASS 遺漏了畫面時間矛盾。 |

其餘已書面核的畫面沒有新的史實衝突：`s52005` 無可讀字請求書，`s52201–05/07/08` 無可讀數字的示意表／未標數值間隔，不冒作格林原稿或把 20 秒畫成三人差；`s52206` 無虛構溫度刻度；`s52046` 是非血腥、註來源層級的死亡卡，`s52047/48` 沒畫 Cook 目擊槍擊。R4 `s52014` 同景的檔案室與船旁構圖及 `s52128` 的「成功」便條，留待生成圖時檢查空間可讀性與便條不可讀字；它們不構成本次另項來源 HOLD。

機械重算：119 景＝114 插畫、4 卡、1 片尾；正文插畫 114/118＝96.6%；121 句 ID、119 景 ID 均唯一，`claims.md` 121/121 依序同字，`screenplay(doc)` 與 `script.md` 逐位元相同；114/114 插畫提示詞非空，19 組 setup/payoff 有效且順序正確。CLI `lint --slug curio-s52 --json` **0 errors／0 warnings**；`git diff --check` 通過；`npm run check:tasks` 驗證 **2,124** 票（既有警告）。`estimateTimeline` 250／300／325 CPM 開場為 42.90／37.00／34.90 秒，正文為 557.60／481.80／455.20 秒；最快僅 **7:35.20**，真實 TTS 正文時長仍是硬關。機械綠燈不抵上述史料呈現與畫面矛盾。

**裁決：R5 旁白／主張表 HOLD；書面畫面 HOLD。** 由作者修三處、重生劇本、記新五檔 hash，再交另一位工作者對新精確稿重核；兩位新隔離讀者盲評、政策／網站審查、真實語音與付費媒體仍各自待辦。本輪無作者檔案或媒體改動。
