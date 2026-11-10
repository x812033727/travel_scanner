# S59 R6｜獨立史料、逐句與書面畫面覆核

2026-10-21 UTC。**110 句口播與逐句引註可由固定原文支持；書面畫面 HOLD。** R6 修好了 `s59027`，但未改的 `s59017` 仍把螺旋槽寫在紙盤上；`research.md` 的 P06 也把針簡寫成「貼著發聲薄片」，與原文的中介橡膠墊不夠一致。本收據只適用於下列五檔；我不是 R6 作者，沒有更動創作檔、做敘事投票、付費媒體或網站核准。

| 凍結檔 | 自行實測 SHA-256 |
| --- | --- |
| `research.md` | `d0077504f3dbe828363158a25c7e7dade955089f49dbb03a734893739e12467e` |
| `brief.md` | `9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3` |
| `claims.md` | `96a84699644630305f3966de3f9c2d07a3eed501456a6e0a14587eaa99c59981` |
| `video.json` | `5a6293a9c93352f848b697625c97b21a8783b0fc49f14ce236bfc1513e154cf1` |
| `script.md` | `7a474081830f7bfe230a6a02a166dab3ec03b834f2e1c86df8727d70cab620c9` |

## 固定原文與差分

我重新下載固定 GITenberg commit 的 [D：杜蒙塞爾 1878 法文原版](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt)、[E：1910 愛迪生傳記中的本人回憶](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt)及只作術語輔助的 [T：1892 英譯](https://github.com/GITenberg/The-telephone-the-microphone-the-phonograph_75683/blob/6b0cda8809aa60bf44270a64853c9aaf9ea5c546/75683-0.txt)。原始位元組 SHA-256 依序是 `c48361e94523ebacc000172ebab34895bb20c0b7e458ac3e122f90a3cc9e717c`、`9818547c6dd15e488c1923bad5cc09cb4fa3f447641daaaf77b2f539b4d49d34`、`cb9e9fbeee72750d6335413a9f91a450c09b9a40377fbc1c42c7822a79c598c9`，全與研究固定值吻合。D 是同代參與者；D 引的匿名來信不是會議逐字稿。E 的愛迪生話語是三十多年後的回憶，不能替巴黎現場作證；T 也不是第二位獨立證人。

我不只採信[作者差分](r6-author-structured-diff.json)：把四個 R6 JSON 葉節點逐一逆換，`video.json` 回到 R5 SHA `77a9ab9de42dd36f9af3b94a6c28312e18e6f846418e38ee2fe0d9ace30b06f7`；`claims.md` 唯一新口播逆換後回到 R5 SHA `e19a8aa75c7d61bbba54b4d747db3b7025ac34599964ac0c4c115fbacd8d8c0b`。用工具的 `screenplay()` 從逆換後 JSON 重建 `script.md`，得 R5 SHA `5b18eb40b5c3434599abbd939d3231fc30837e360bfaff0ea00d23cdca89cf48`；`research.md`、`brief.md` 與 R5 相同。遞迴 JSON 比對恰四葉：`s59027` prompt，以及 `s59040` 的口播、卡片主字、副字。`visualHash` 自算 R5 `7417dce22257dbfe`、R6 `3deadad1dfc94743`；R6 `narrativeHash` `0b0423546b1b067e`、`speechHash` `0629d7a46d9b81bf`。其餘 109 句口播與其他畫面 prompt 沒改；R5 的敘事或畫面結論不能當 R6 的新版票。

## 逐句、機械細節與書面畫面

`video.json` 有連續且唯一的 `s59001–s59110`；`claims.md` 有相同 110 行，口播與 JSON **110／110 逐字相同**；`script.md` 的 110 個場景及全文與工具從 JSON 生成的劇本逐位元組相同。逐句表的 122 個 D／E 連結實例全部指向固定 commit，16 個 P ID 均在研究表定義，逐句引用無未知 ID 或缺鏈；P12 是來源身分註，不在口播逐句表引用。保留的句子因上述精確逆換，可沿用 R5 對 110 句的來源核對；我另讀 D6680–6694、6872–7049 與 E5195–5241、5262–5273 重新抽核本集主張與所有 R6 新字。

- **`s59027` 已修妥。** [E5195–5205](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5205) 說螺旋槽在承盤 *platen*；圓紙盤覆於其上，電磁鐵壓針把訊號壓在紙盤，另一機的接點讀回。R6 改寫為紙盤上「沿螺旋路徑的小型凸起壓痕」、接點停在痕跡上方，沒有讓手指讀痕、宣稱紙盤自身刻槽或預演成功播出；這是合理的概念插圖。
- **`s59040–41` 的新口播與卡片有據。** [D6876–6885](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6876-L6885) 明寫針不直接固定於振動薄片、由彈簧支承，橡膠墊在兩者間傳遞震動而不使之悶住；[T7023–7034](https://github.com/GITenberg/The-telephone-the-microphone-the-phonograph_75683/blob/6b0cda8809aa60bf44270a64853c9aaf9ea5c546/75683-0.txt#L7023-L7034) 可輔助確認語意。`s59039` 先講圓筒槽與錫箔，`s59040` 現轉到彈簧／震動如何跨越，`s59041` 再用橡膠回答；不再逐句重複槽的帶路作用。`s59041` 的排版箭頭「薄片→橡膠→針」與 D 的中介件相符。
- **仍有阻擋：`s59017`。** R6 未改的 `shot` prompt 是 `one inventor studies a round embossed paper disk **with a spiral groove** beside a desk lamp`。自然讀法和生圖指令都是「紙盤本身有螺旋槽」，而 E5197–5204 只把槽放在紙盤下方的承盤；紙盤承受的是訊號壓痕。這與 R5 `s59027` 曾有的同類錯誤一樣，不能只靠日後圖片評分猜測模型畫到哪一層。R4/R5 舊覆核只指出 `s59027`，在此應修正「唯一畫面阻擋」的舊判斷。`s59013` 的 `spiral track on a paper disk` 可理解為壓痕路徑，卻也可能被畫成紙上原有槽；一併澄清其為路徑較穩妥。
- **研究表 P06 需精確化。** 它稱「貼著發聲薄片的針」，容易讓人以為針直接貼住薄片；D6878–6883 卻在中間放橡膠墊。R6 的 `s59040–41` 口播與卡片是正確說法，但研究表應改成「彈簧支承的針經橡膠墊接收薄片振動」之類的意思，避免同一凍結包內互相打架。其餘 D 對錫箔圓筒、回放、轉速、磨損、匿名來信、重試與杜蒙塞爾失敗原因，以及 E 對電報紙盤、十八美元草圖和紐約展示，與本版口播的來源層級相合；未見新增的逐句口播阻擋。

`node tools/video/cli.mjs lint --slug curio-s59 --json` 實測 **0 error／0 warning**，110 句、100 張 `shot`、10 張 `big`，估 13.33 分鐘。這個 lint 不辨識紙盤／承盤的物件錯置。**綜合結論：口播逐句來源可過；五檔書面包與書面畫面 HOLD。** 請作者窄修 `s59017`（並消除 `s59013` 的可誤讀措詞）、研究 P06，重新凍結 SHA，再由未寫修訂者複核確切差分。R6 的全新雙盲敘事、正式合票、站主審稿與語音／分鏡／成片審核均另屬後續關卡；本收據不開啟付費製作。
