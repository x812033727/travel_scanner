# S53 R10｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS，限 R10 精確稿的來源、逐句主張、六景書面畫面及兩個 loop 端點。** 我未撰寫 R10 作者稿，也未把 [R9 來源 PASS](r9-source-independent.md) 或 R9 盲評移作本版的敘事結論。實際語音、生成圖片、正式新盲評與網站關卡仍須另驗。

| 凍結檔 | 本次實算 SHA-256 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84` |
| `video.json` | `6e271778492bdcd97e1ffb3ee700e99fe848f0fd8d077bb705a6972b3e29a9f5` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |

五檔均與 [R10 作者凍結](author-freeze-10.md)一致。重新讀取 `research.md` 指定的固定 R／C 原文暫存檔並算 SHA：1913 年 *San Francisco Relief Survey* `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`；1906 年 Morris 編書 `4f001abb09f44aa630059d2325de55bd8f88d8304fa21ce97322d57e0fa3213c`。兩者均與研究檔的固定 Git 提交相符。本輪八項改動只使用 R；C 仍沒有被當作統計佐證。R 是 1913 年編纂的機構調查，以下日期、計數與訪查方法都應保留此歸屬。

與 SHA 分別為 `11f814d0…`／`7dec1a98…`／`dd5a82bb…` 的 R9 凍結 `claims.md`／`video.json`／`script.md` 逐物件比較：只有 `s53043/083/099/100/101/102/103/104` 八句及對應八列 claims 更改；僅 `s53083/099/100/101/103/104` 六個 prompt 更改；僅 `s53083→s53084` 和 `s53100→s53101` 兩個 loop 更改。`video.json` 其餘頂層欄位和 scene、`claims.md` 其餘列與文字均未改；`brief.md`、`research.md` 與 R9 位元組相同。未改部分的逐句來源核查依 [R9 獨立收據](r9-source-independent.md)及其所承接的 R8 收據。

| R10 差分 | 固定來源核對與判定 |
| --- | --- |
| `s53043` | [R L10450–10460](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10450-L10460) 記完工於 1907-03-19；[R L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941) 記 1906-08-17 起最多一年。到 1907-08-17 尚餘 151 日，不到五個月；一年中的 214 日已過，確為大半。`s53038` 已給完工日期，本句沒有再報日期。**PASS**。 |
| `s53083` | [R L4998–5001](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4998-L5001) 明記營地共遷出 5,343 棟；本句只問總數，不把它當建成的 5,610 棟。下一景 `s53084` 統計卡直接答 5,343，章節與 loop 均接上。**PASS**。 |
| `s53099` | [R L10502–10504](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10502-L10504) 的「not a few cases ownership was exchanged many times」直接支持「有些……幾度易主」；無姓名、數量或個案細節被補造。**PASS**。 |
| `s53100` | 問「先有什麼線索」，其前提是訪查搬屋地址；[R L10504–10510](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10504-L10510) 直記地址與其局限。下一景交代答案。**PASS**。 |
| `s53101` | 開場 `s53001/008` 在 1907 年並問隔年八月，故指 1908-08；[R L10194–10197](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10194-L10197) 明記此時開始訪查，[R L10504–10510](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10504-L10510) 明記搬屋時留下的地址。此景作 `s53100` 問句直接 payoff；沒有稱那些地址都準確。**PASS**。 |
| `s53102` | [R L10194–10196](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10194-L10196) 記接下來三個月的家庭訪談與旁證查詢；[R L10214–10220](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10214-L10220) 記另可用會議、個案及審計等紀錄。「約三個月」「向其他紀錄核對」均屬窄述。**PASS**。 |
| `s53103` | [R L10504–10506](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10504-L10506) 記訪查員走訪 1,137 棟**已搬出小屋的地址**，沒有說全部 5,343 棟均受訪；「嘗試尋訪」未把 1,137 說成完整訪談數。**PASS**。 |
| `s53104` | [R L10504–10506](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10504-L10506) 用「680 fairly complete records」。本句只問較完整家庭紀錄份數，下一景 `s53105` 直接答 680；沒有混入其餘 457。**PASS**。 |

六個新提示詞 `s53083/099/100/101/103/104` 均是無姓名、無可讀名冊或地址的概念插圖：空白小屋計數物、所有權卡、封閉資料夾／城市圖、無字地址卡、空白小屋卡及訪談資料夾。其年代安排為稍後檔案室或 1908 年訪查，與上述 R 段落相容；未畫成保存的原始文件，也未虛構搬屋機械、特定家庭或取得完整紀錄的比例。**書面畫面 PASS；生成圖仍須逐張驗收。**

機械覆核：124 景、126 句、126 列 claims，ID／順序／口播文字逐一相同，無重複 ID；16 個 loop 端點均存在且先設後收。`screenplay(doc)` 與 `script.md` 位元組一致；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json` 回報 **0 errors／0 warnings**。`estimateTimeline` 在 250／325 CPM 下，`s53010` 開始前為 **49.93／40.53 秒**，從 `s53010` 至 `outro` 前正文為 **595.77／485.37 秒**（最快約 **8:05.37**）。這是書面估時，不是 R10 實際 TTS 或成片證明。
