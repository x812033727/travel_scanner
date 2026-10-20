# S49 R4 獨立固定來源與書面畫面覆核

2026-10-20。**來源包 HOLD；R4 旁白及書面畫面 PASS。**我沒有參與 R4 作者改稿，直接重讀 Locke 名下 1859 年重印本與 Jacoby 1902 年評論的固定全文，核對本版 `moon128`–`moon130`、`claims.md`、`research.md` 和五份交付檔。R3 的唯一旁白 HOLD 已由 R4 單句修復；但 `research.md` 留有同一個過度歸因，因此來源包尚不可標為完整 PASS。此處的書面畫面 PASS 只指提示詞，不是生成圖片驗收。R2 的正式雙盲 FAIL 也不能沿用為 R4 PASS。

`J`：`/tmp/s49-jacoby-53396.txt`，SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`；`L`：`/tmp/s49-moon-hoax-62779.txt`，SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`。行號皆屬這兩份固定文字，並非 1835 年原報頁面。

## R4 差分事實與畫面

| 景／檔 | 原文核對與裁決 | 書面畫面 |
| --- | --- | --- |
| `moon128` | [J 4178–4205](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4178-L4205) 確有 Jacoby 引用各報反應；問這些引句從哪裡來，PASS。 | 一本書內的無字剪報，是普通示意，沒有冒充存世原報影像。PASS。 |
| `moon129` | 新句「把雅各比的各報引句逐一對照，也都能在重印書裡找到。」是**本次跨文本比對**，沒有再說 Jacoby 自己「明說」了報紙引句的直接來源。J 4183–4192 的 *Daily Advertiser*、*Mercantile Advertiser* 文字對應 [L 2092–2102](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2092-L2102)；J 4193–4205 的 *Evening Post* 反諷文字對應 [L 2110–2120](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2110-L2120)。標點與節錄長短有差異，核心引句相同。`claims.md` 同列 J／L 錨點。旁白及 claims **PASS**。 | 天文學家指向一本普通重印書，旁邊是無字報紙；沒有可讀 1835 年原紙。PASS。 |
| `moon130` | J 4178–4205 僅提供這段後出評論及摘句，L 2055–2120 是 1859 年重印本選錄；「後出的評論沒有替重印本選錄補上一張獨立的原報頁面」只談 Jacoby 此處，未概括世上不存在原報。PASS。 | 書與無字剪報均屬示意。PASS。 |
| `research.md` 固定來源 J 列 | **HOLD。**現寫「Jacoby 的報紙引句**明說取自稀有重印本**」。[J 4178–4182](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4178-L4182) 實際說前面所摘月球騙局正文引文來自稀有重印書，且該書**也收有**各報意見；未以直接句式聲明隨後的每一條報紙引句均取自該書。J 4183–4205 與 L 2092–2120 的逐句重合足以支持交叉比對結論，但不能把推論寫成 Jacoby 明說。`research.md` 的 P13「Jacoby 1902 借同一本重印引用」亦應明標「J／L 引句交叉比對可見」，免得再次被讀成 Jacoby 的明文自述。 | 不影響當前提示詞的 PASS，但來源文件須修。 |

建議只修 `research.md` 的兩處來源描述，保留固定網址及文本不動。例如 J 列改成「Jacoby 說騙局正文引文取自稀有重印本，該書也收各報意見；其後報紙引句逐一可在該重印本找到，這是兩文交叉比對的結果，並非另一份獨立的 1835 原紙。」P13 改成「Jacoby 1902 引用的各報段落，與同一本重印書的選錄逐一相合，並指出《Evening Post》是反諷」。這屬來源註解修正，若沒有動 `video.json`／`script.md`，可只對新 `research.md` 差分覆核；R4 敘事盲讀仍須由兩位全新隔離讀者對本版旁白重新評分。

## 一致性與界線

直接核對現行 `video.json` 的 132 個編號景：125 `shot`、7 `big`，加含三句旁白的 `outro` 共 **135** 句。132 句編號景與 `claims.md` 的旁白及 `shot` 提示詞／`big` 字卡完全一致；`script.md` 的 132 個編號景加片尾三句與 `video.json` 同文同序。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` 報 **0 errors、0 warnings、135 lines**；`git diff --check` 通過。11 組 `loops`、影片說明中的兩份固定來源連結和片頭片尾計畫在這輪沒有變更。未生成或驗收圖片、TTS、配樂、成片；沒有 1835 年原報、獨立發行帳或 Herschel 原信。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `48c3dc196b668c3ce3d58b4b3ffc26973262eb450587abfcc39d10d421057568` |
| `research.md`（待修） | `9476f53555e51da2471a72f75249e7e5fc8ed4ce3e30627578ce86cf4198c327` |
| `claims.md` | `8434bb5e2a25382d8a766759aa782ef529e0e891c44863f571bc58bc7a31d060` |
| `script.md` | `da1dca236ce6b26d4785177f018d945df76f4fd1e149b547b808b3408d6e350d` |
| `video.json` | `7c26a60db37f4e2cb866f2491a44e18dd5c458373f39677d4b350288a3578131` |

**下一步：**作者只修上述 `research.md` 兩句並記下新雜湊；另一位獨立覆核者確認差分後，才可將來源包改標 PASS。新雙盲正式通過前不啟動 TTS 或圖片。
