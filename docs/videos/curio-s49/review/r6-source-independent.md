# S49 R6｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS：R6 新台詞、主張錨點與四景書面畫面。**本裁決綁定下列精確檔案；它不是敘事雙盲、生成原圖驗收、旁白試聽或成片核准。我未參與 R6 修稿，重新開啟固定的 L／J 轉錄，直接核對新增 P05a、`moon049–051` 三句、`moon049–051/103` 四個提示詞，並重跑全稿對齊與 lint。R5 對其餘旁白／書面畫面的獨立裁決見 [r5-source-independent.md](r5-source-independent.md)。

固定 `L` 是 Locke 名下 **1859 重印本**，本地 SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`；`J` 是 Jacoby **1902 後出評論**，SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。兩者不是 1835 原報；J [4085–4109](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4085-L4109)明說該巨鏡描述是想像器材與光學術語拼貼。R6 仍把器材和運輸留在「報導又說／文章又說」的框內。

| R6 景 | 原文與台詞核對 | 書面畫面裁決 |
| --- | --- | --- |
| `moon049` | 台詞「報導又說，鏡片先運到倫敦，再替它造顯微鏡與轉動架。」[L 501–511](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L501-L511)記完成的鏡片運往 *the metropolis*，其後建顯微鏡與可水平、垂直動作的架子；L 553–554 又明指從倫敦出航，故此處把首都稱倫敦合乎上下文。 | **PASS。**想像的 1830 年代工坊、普通模型鏡片和無標記可動架；明排除 Herschel 真器材。 |
| `moon050` | 台詞「它要怎麼跨海抵達好望角？」是轉折提問；[L 509–511、553–559](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L509-L559)先說將器材送到目的地，後寫一行人從倫敦出航、抵岸後移送鏡片與觀測台架。 | **PASS。**讀者在無字地圖上比劃空白海路；沒有捏造可讀的航線或原始遠征文件。 |
| `moon051` | 台詞「文章又說，一行人從倫敦出航，抵岸後把鏡片和支架送上高地。」[L 553–568](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L553-L568)直接寫出航、抵達、把 *lens* 和 *frame of the large observatory* 送往高地，並寫牛隊協助登坡。「支架」是對觀測台架的簡稱；台詞沒說那是真實器材史。 | **PASS。**從虛構報導想像的高地、牛隊及有蓋器材載荷；未畫可辨真站點、原船或 Herschel 肖像。牛隊和載荷並列是故事插圖，不能在後續圖像／說明欄升格成「牛隊是搬鏡片的唯一工具」或真實運送紀錄；原文沒有這兩項結論。 |
| `moon103` | 原台詞明說「這是虛構報導裡的火，不是赫歇爾真實觀測站的火災紀錄。」[L 1525–1564](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1525-L1564)的起火只屬假文章敘事。 | **PASS，解除 R5 的單景 HOLD。**現在是讀者合上關於虛構火災的無字報紙，旁置普通天文台示意圖；明排除火焰、可辨真站點與 Herschel 肖像。舊提示詞 `at a real modest observatory` 已不存在。 |

新增 `research.md` P05a 固定到 L 501–568，正確分開「報導自述的鏡片運輸」與經查核的真實器材史，也明說原文未指定牛隊為搬鏡片的唯一工具。四景 `claims.md` 的台詞、來源連結和視覺欄與 `video.json` 相符。

機械覆核：`video.json` 有 133 個編號景（126 `shot`、7 `big`）及 3 句片尾；**136/136** 台詞與 `script.md` 同文同序，**133/133** `claims.md` 的 ID／台詞與 JSON 相同且無重複，**126/126** 圖像提示詞在主張表逐字出現，**7/7** 字卡的標籤／主文／副文相符。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` 回報 **0 errors／0 warnings**；`git diff --check` 通過。`npm run check:tasks` 成功（只有倉庫既有的持有時間／範圍重疊警告）。

| R6 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `73eb8e6f49f10ac4a0f275511913ccfff5c3f18eec6958cc6b25595eb20506d2` |
| `claims.md` | `a9f13314a1ab2776de217423b8cfc537ca5739ea09535f4d241a2d9791fc95ff` |
| `script.md` | `dfc5ae984d4720f4c104edaf23cf1d7ff6bca5b05793b51fe32fdd59995fb8f8` |
| `video.json` | `5dc1602b0aeb254ea1c2b3d45ab9fbff15450fe73f80e06c202059cd6f3934b4` |

R6 尚需兩名**全新、只讀精確 `script.md`** 的讀者按固定 13 題完成正式敘事雙盲；本來源 PASS 不能代替。尚無原生圖、TTS、配樂、成片或 Studio 可點片尾元素。生成圖若呈現真實 Herschel 器材或可辨真火災站點，仍須按原圖重新判定。
