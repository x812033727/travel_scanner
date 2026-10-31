# S49 R27｜`moon032/033` 非作者書面覆核

2026-10-22 UTC。對 R26 連續兩張原生圖人工退件後的窄修作獨立覆核：**兩景史料／逐句主張 2／2 PASS；兩個 R27 提示詞 2／2 書面 PASS**。此結論只放行有上限的定點原圖重試，並非原生圖、第二章或全片 storyboard 收圖。

## 固定證據與版本

- 實際重開固定 L（1859 年《The Moon Hoax》重印本）`/tmp/s49-moon-hoax-62779.txt`，SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)；又重開 J（Jacoby 1902）`/tmp/s49-jacoby-53396.txt`，SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)。L 把高處物鏡、暗室焦像與反射鏡寫在 Herschel／Brewster 的**虛構對話**裡；J 明稱這是 imaginary conversation 和 optical jargon，不能用作真實儀器史。
- R27 `video.json` SHA-256 `02fdb0f2ac142634d42ac24f7108bb12424e7a4625756ca559b90d52912552a3`；`claims.md` `779a8e22e6e7e202249cf7ec645a91a7ade7139c5c0e6ee2bb70c4fa50f2bd2f`；`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；`research.md` `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750`。獨立重跑 CLI lint：exit 0、0 errors、0 warnings、131 句。
- 對 [作者的逐字差分](r27-moon032-033-prompt-structured-diff.json)（SHA-256 `0883596f5c9e0da59f5393d09f0cfe1c73262f99dd5ec1322ce435b7c8eb3a77`）逐條核 `after` 與現稿：解析後只有 `scenes[28].data.prompt`／`scenes[29].data.prompt` 變動；claims 只改相應兩列的畫面欄。將兩個 `after→before` 倒填並重新按原 JSON 格式序列化，得到 R26 `video.json` SHA `57027ce7870f736e8662b6774ed4f6e85922d153e6ac864fb8a9ca1cf389ca22`、`claims.md` SHA `ced02136c94ec5f93f34a62ad5bddfd635b8fde8af93297cff531f91ae40bbcc`。`moon034–039`、全部台詞、章節與運鏡未被改動。工具獨立計算 R27 `visual_hash=74c5cc0713c7766d`、`look_hash=98a370ae40badbaf`。

## 逐景判定

| 景 | 史料與書面圖像 | 原圖驗收重點 |
| --- | --- | --- |
| `moon032` | **PASS**。旁白「兩人想讓物鏡架在高處，把焦點影像投進暗室」合 L 的虛構方案；新稿明寫 *plainly imagined* 與 *visual metaphor*，只讓一位 1835 年成年人物指向高百葉開口、陰暗牆和一束日光，撤掉先前被模型變成六格工程紙與紅頭現代器材的物件。開口和光束是**空間比喻**，不是聲稱真實焦像已進暗室；提示詞沒有假稱這是存世設計圖。 | 若輸出像已建實驗設備、現代器材、可讀字、孩童、後世服飾或黑邊，人工退件；也要確認畫面能跟旁白所說的高處／暗室形成可理解的空間關係。不得把普通窗光當作真的物鏡成像證據。 |
| `moon033` | **PASS**。L 的 Brewster 對話明說暗室焦像由反射鏡承接。新稿用一位明顯成年、1835 年英式禮服外套人物指向普通素面橢圓牆鏡，側百葉自然光照到鏡面，且明寫想像室內；沒有暗示真 Herschel 器材或原件照片。R26 原圖的童貌、東亞式衣帽和現代頂燈都不是新稿要求。 | 拒絕童貌、東亞式衣帽、現代頂燈／工坊、非素面鏡、真天文台或黑邊。鏡子必須可辨為鏡子，人物動作要能對應「指向反射鏡」。 |

## 私人圖單與費用界線

現行私人 manifest SHA-256 `57d169e58776fd22bb03e5c42cdda984a91bff3fcb45643baf49cc9a120e1be8`，仍綁 **R26** `visual_hash=5781d6810538eb41`，其中 `moon032/033` 雖機器 PASS，已由原生圖審核判 **人工 REJECT**，不可當 KEEP。獨立比較 R26 付費前備份的 26 個 KEEP 條目與現行 manifest，26／26 完全相同；26 張所選檔案 SHA 逐張相符、judge pass、無 `needs_review`。新一輪付費前須把這 26 個 KEEP 保全地重綁 R27，丟棄兩張退件的舊請求鍵／所選圖，核對 `keyframeProblems` 與新的 manifest 雜湊，不能直接沿用 R26 binding。

ledger SHA-256 `bdd5c8ebb1b7821f05532cb82af58b888424c31a98443b030a336f427d7067de`，US$1.0260／76 image／76 judge／0 預約，低於本集 US$5.30 上限；`media/jobs.json` 是空 job 物件且 `STOP` 存在。此審查**沒有付費媒體呼叫**。書面 PASS 後可依原停止條件每景有上限試畫，逐張看 1280×720 原圖及任何裁圖；若再次出現同型錯誤，停批，不因機器分數高而收圖。
