# S49 R36｜`moon037` 成年起身構圖非作者紙審

2026-10-22 UTC。**固定史料與逐句主張 PASS；R36 `moon037` 提示詞書面 PASS。** 此結論只放行這一景的有界原生圖重試；R35 原圖仍為 HUMAN REJECT，R36 尚無原生圖裁決，不放行 `moon038–039` 或全片分鏡。

## 精確綁定與差分

- 基底 commit `14fdbcf8346c8db111fbd7aa5e9b9eee71443e3d`。R36 `video.json` SHA-256 **`9b6700ec1d71ac253c1176ca90ac9c2945670c30ad08adb3327ce46190c5b08d`**，`claims.md` **`3a10691415c01c5f067564e04554e5e84f0f28e7e70e3421def2d78cfc04a682`**；未改 `script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750`。
- 獨立核對 [R36 結構差分](r36-moon037-mature-rise-structured-diff.json) SHA-256 `b8cffbc637e19d1e039c3d56ac021c74395e07427eac3071b5acc0239cacdebc`。將唯一 `scenes[33].data.prompt` 的 `after` 換回 `before`，`video.json` **逐位元**恢復基底 SHA `fe4e3c2b3fd6691fa467d253965b4efa8c44c870582159fe110160dd16b029c3`；將唯一 `moon037` claims 行 `after` 換回 `before`，`claims.md` **逐位元**恢復 `824d15a121e9ca7ae147acfe60e1fa92e4e6aa871e70c788f9606c0750b0da79`。兩項替換在現稿各只命中一次。解析後全片 129 scenes，`moon037` 以外 **128 scenes 全等**；非 scenes 頂層、`moon037` 台詞／運鏡／視覺／章界均全等，131 句不變。claims 也僅一行變動。
- 親跑 `lint --slug curio-s49 --json` exit 0，**0 errors／0 warnings／131 lines**；`keyframes --slug curio-s49 --shot moon037 --takes 1 --dry-run` exit 0，服務顯示 MiniMax `image-01` ready，提示詞 **524／1071** 字元。兩項是只讀檢查；本紙審 **0 付費呼叫**。

## 史料與畫面裁決

重新開啟固定 L（Locke 名下 1859 重印本）本地原文 SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` [L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)：虛構對話裡 Herschel 提出反射鏡和照明顯微鏡，接著明寫「Sir David sprung from his chair in an ecstacy of conviction」。固定 J（Jacoby 1902）原文 SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` [J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) 同樣引述起身段落，並明稱這段是荒謬的想像對話。現行旁白和 claims 均把起身者指為布魯斯特；畫面限定 `plainly imagined`，也排除器材、圖解和可讀字，沒有把此事當 Herschel 實驗紀錄。

原 [R26 非作者紙審](r26-next-chapter-eight-prompt-independent-pass.md) SHA-256 `9224ac098475dde5dd7e63c66c19acaa28d7faf85e3a7ea0ee7bddbe584480a2` 放行兩位可見成年人，同時明列少年形象退件。R35 [停批記錄](r35-moon037-native-stop.md)及[庫存](r35-moon037-native-stop-inventory.json)指出機器 7.88／10 PASS，但原尺寸人眼 REJECT。我重看封存的 **1280×720** 原圖 SHA-256 `41e41c41e07f017a2c20675ce04d2c9584ed66a578ef7b823fa57f514cbe5553`：右側坐者圓臉、大眼、紅頰及短小身形尤其像少年；左側半蹲、椅子偏小，服飾年代感不足以解決年齡問題。保留 R35 記載的另一位審看者 KEEP 異議，但本紙審同意該圖退件。

R36 改為**一名可見的晚中年男子**、灰鬢、濃鬢角、面頰紋路、成年肩寬和 1830 年代高領禮服；他已從身後**正常尺寸**木椅完全站直，舉手轉向畫外說話者。這足以在單幅中表達 Brewster 聽到 Herschel 主意後起身的敘事關係；第二人留在畫外仍符合對話及旁白，不要求把兩位都塞回畫面。`no other people` 限制畫內人物，與畫外 speaker 不衝突。全片 `look.preset` 仍為 `cute-mystery`，dry-run 也確實附加「chibi characters with big round heads, large expressive eyes」；R36 沒有取消卡通統一風格。局部灰鬢、紋路、肩寬、全身站直與成人服飾給模型可畫出**卡通成年人物**的明確指令，故紙面 PASS；風格仍可能使成圖讀成少年，紙面不能預先替原圖判 KEEP。

## 放行界線與狀態

當前私人 manifest SHA-256 `8fa67b2e39426dcc5b98220624ec17096cad69444d37a6c870465de1b40c8ff4` 仍有 **R35** `visual_hash=87f0c570cd6211b0`、`look_hash=98a370ae40badbaf`，`moon037` 未入選。逐一核對 R35 庫存所列 **29 張**已選 file、manifest SHA 與實檔 SHA，全數一致。STOP 在位，`media/jobs.json` 為空；ledger SHA-256 `dd9b74f40ece0c756800fa4de3a6a70fc4e162bedac4ab87fa6af255b43ed87b`，US$1.1475／85 image／85 judge／0 預約，距本集 US$5.30 上限餘 US$4.1525。R36 文字改動後、任何付費重試前，須在 STOP/jobs 空的守衛下**離線重綁 R36 visual hash**，並維持 29 KEEP 所選檔與實檔 SHA、`look_hash`、退件 `moon037` 未入選、帳本與上限。

只准按此固定 SHA 的文稿對 `moon037` 做有界一張原生圖與 judge；取回 1280×720 原圖後，獨立人眼核**清楚成年面貌、完全站直、正常椅子、對畫外說話者的反應**，以及 1830 年代場景、無多肢體、現代物件、可讀字或冒充真實器材。若仍讀成少年、蹲坐或小椅，即使機器 PASS 也 REJECT 並停批。R36 書面 PASS 不代表新的 manifest 已重綁，也不代表原生圖、人耳、整章或全片通過。
