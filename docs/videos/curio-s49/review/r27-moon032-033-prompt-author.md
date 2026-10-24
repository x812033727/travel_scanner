# S49 R27｜`moon032/033` 兩景原圖退件後提示詞窄修

2026-10-22 UTC。**作者候選，待另一人獨立紙審；本輪沒有付費重畫。**[R26 原圖停批](r26-next-chapter-two-native-stop.md)直接看原生圖後判 `moon032` 的六格紙與紅頭金屬器材、`moon033` 的童貌東亞式衣帽及現代頂燈均不合 1835 年虛構報導。機器 9.29／10、10／10 PASS 不能取代人工結論。本次只修這兩景的 `data.prompt` 與 [claims.md](../claims.md) 同列畫面欄；`moon034–039` 六個已獨立書審 PASS 的提示詞、全部台詞、劇本、來源、章節與前 26 張 KEEP 景逐字不動。

| 景 | R27 書面畫面修法 |
| --- | --- |
| `moon032` | 改為一名側鬢、鬍子與成人肩型明確的 1835 年成年讀者，在想像的英國室內，從高處百葉開口指向下方陰暗空牆；一束自然窗光作「焦點進暗室」的視覺比喻。場內物件限人、牆、椅與開口，不再要求易畫成工程圖的紙上圓方格，也不指定實物器材。 |
| `moon033` | 用同年代成熟男性、側鬢鬍子、深色高領禮服外套、普通素面橢圓牆鏡及側邊自然光，承載報導中「反射鏡接住影像」的構想；畫面限定素牆與簡木椅，不用未定年代工作室或「燈光」提示。鏡面是文章構想的想像示意，不稱真實器材。 |

固定 1859 年重印本 [L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520) 記**虛構** Herschel／Brewster 談無鏡筒高物鏡、焦像進暗室及由反射鏡承接；新畫面只讓觀眾理解這段文字的空間與反射概念，不冒充已建造的望遠鏡、原報插圖或可驗證的實驗室。旁白的「兩人想讓…」「布魯斯特說…」及 claims 史實與錨點不變。

[兩項逐字可逆差分](r27-moon032-033-prompt-structured-diff.json) SHA-256 `0883596f5c9e0da59f5393d09f0cfe1c73262f99dd5ec1322ce435b7c8eb3a77`，以 `after→before` 回填可還原 R26 `video.json` SHA `57027ce7870f736e8662b6774ed4f6e85922d153e6ac864fb8a9ca1cf389ca22`、`claims.md` SHA `ced02136c94ec5f93f34a62ad5bddfd635b8fde8af93297cff531f91ae40bbcc`。R27 新 SHA：`video.json` **`02fdb0f2ac142634d42ac24f7108bb12424e7a4625756ca559b90d52912552a3`**、`claims.md` **`779a8e22e6e7e202249cf7ec645a91a7ade7139c5c0e6ee2bb70c4fa50f2bd2f`**；`script.md` 仍為 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。JSON 遞迴比較只變兩個指定 `data.prompt`，claims 只變同兩列視覺欄。CLI lint exit 0、**0 errors／0 warnings、131 句**；MiniMax 不付費 dry-run 的兩景提示詞各為 489／1068、446／1070 字元預算，模型 ready；stdout／stderr／exit 同目錄保存。

本輪沒有改動私人圖單或媒體：manifest SHA `57d169e58776fd22bb03e5c42cdda984a91bff3fcb45643baf49cc9a120e1be8` 尚綁 R26 `visual_hash=5781d6810538eb41`，且 `moon032/033` 的機器 PASS 圖仍是人工 **REJECT** 證據，不能送 storyboard。R27 新 `visual_hash=74c5cc0713c7766d`，先由另一人核兩景與可逆差分，後續安全重綁並驗證前 26 張 KEEP，才能評估有上限的定點原圖重試。ledger SHA `bdd5c8ebb1b7821f05532cb82af58b888424c31a98443b030a336f427d7067de`，仍 **US$1.0260／76 image／76 judge／0 預約**，低於 US$5.30；jobs 空、`STOP` 在位。全片分鏡、網站卡、人耳及成片仍待。
