# S49 R10｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**結論：R10 固定來源／逐句主張 PASS；書面畫面 PASS。**這是對下列精確五檔的文字、來源錨點與分鏡提示覆核，不是新稿的正式敘事雙盲、實際配音或生成影像驗收。我未參與 R10 作者改稿，亦未修改五份作者檔。

| 固定材料 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `f12b37209b51cb4888b0ff41c6f70bc5b7fecbeb721edf25a7c5fe60d189b034` |
| `script.md` | `c6389ff27c36856a914442644b71f746c66a89ddb1bd8f0f14a3f086d09fa51c` |
| `video.json` | `86361df066e0df920c5ae55055307eb4c6a46f1cae597c56569cb041f2732e80` |
| L `/tmp/s49-moon-hoax-62779.txt` | `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` |
| J `/tmp/s49-jacoby-53396.txt` | `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` |

L 是 Locke 名下 **1859 年重印本**，包含出版者序與選錄，不是我已核對的 1835 年《太陽報》原紙。J 是 Jacoby **1902 年後出天文評論**，不是 Herschel 原信或第二張獨立原報。`brief.md`、`research.md` 的雜湊與 [R9 錨點獨立覆核](r9-anchor-independent.md)相同；P02／P03／P05／P06／P12／P13 歸屬與這兩層來源的限制未移動。未見取得原報、原信、皇家學會文件或獨立發行帳的新增主張。

## 差分與原文

以倉庫 `HEAD` 的 R8 精確基線、[R9 六句來源覆核](r9-source-independent.md)、[R9 錨點覆核](r9-anchor-independent.md)及 [R10 作者凍結](r10-author-freeze.md)核對目前五檔。遞迴比較 `video.json`：頂層設定、`sources`、`voice`、`music`、11 組 `loops`、全部保留景的 `data`／提示詞／字卡／情緒欄均與 R8 相同；共同場景只有 `moon011/012/015/028/030/100` 的第一句 `text` 葉值有差異，其中 `moon011/012/030/100` 已在 R9 來源覆核通過，R10 保留其文字。只有 `moon026/027/029` 三景被刪，沒有新景。`claims.md` 相對 R8 僅這三列刪除，以及 `moon011/012/014/015/028/030/100` 的旁白或來源欄差異；所有保留列的視覺欄與 R8 同文。R9 的 `moon012/015` 錨點修補仍在，R10 增補的是 `moon014/028` 的直接錨點。正文其餘台詞和三句片尾無差異。

| ID | 固定原文與 R10 判斷 | 書面畫面 |
| --- | --- | --- |
| `moon014` | [L 152–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L152-L165) 的**重印標題**在 L158 具名 Herschel，L164–165 自稱首登《太陽報》。新增 P02 直接錨點涵蓋兩者；旁白沒有聲稱親見 1835 原紙。**PASS。** | `moon014` 是排字工人持無字標題紙條的普通示意，沒有仿原紙字樣；提示詞未改。**PASS。** |
| `moon015` | [L 152–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L152-L165) 給出標題姓名，[L 212–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L212-L254) 給出文內虛構發現。新問句「可一個名字，能替月球上的發現作證嗎？」只追問證據力，不重念標題上的姓名，也不宣稱 Herschel 證實發現；沿用的兩個直接錨點仍有效。**PASS。** | 一位讀者看無字紙張的示意，沒有真實月面或原件形象；提示詞未改。**PASS。** |
| `moon023–025` 與刪除的 `moon026/027/029` | [L 224–239](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L224-L239) 是文章**自稱** Grant 通信及皇家學會收到文件。`moon023` 仍回答開場 `moon004`：沒有查到實際來信；`moon024/025` 限定文件為文內說法，沒有把未交材料變成已驗證原件。三個重述列連同視覺欄已整列消失，未移到別處。**PASS。** | 三景對應的書面畫面不再列入；保留景的空信封、無字紙疊與遠處普通資料夾仍是讀報示意。**PASS。** |
| `moon028` | [L 224–239](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L224-L239) 原句是 *equal, in general interest at least*（L230–232）。「一樣引人入勝」準確保留**讀者興趣**比較，未說兩份材料有相同證據力；新 P03 連結 L212–254 包含此句。其後「望遠鏡怎麼看清月面？」接 [L 390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520) 的虛構儀器對話，新增 P05 錨點有效。`moon030` 立即以「故事先安排」進入該對話。**PASS。** | 同一位讀者比較兩張**無字**普通紙的舊提示詞，未標成皇家學會原件；旁白明說「它還說」。`moon030` 的無管望遠鏡草圖仍以 imagined 限定。**PASS。** |

逐列檢查目前 `claims.md` 的 157 個直接 URL：均指向 L／J 固定 commit、合理行號範圍；以上改動錨點另按本地固定原文逐行核對。這個檢查不把 J 的引文算成獨立 1835 原紙；1859 出版者的五倍發行量／六萬份說法仍只歸出版者。

## 對齊與範圍

- `video.json` 現有 130 個編號景：124 `shot`、6 `big`，另有一景三句片尾。`script.md` 的 131 個場景標題及 **133/133** 旁白文字、情緒與 JSON 同序；**130/130** claims ID／旁白與編號景同序。場景 ID、旁白 ID 均唯一。
- **124/124** shot 的提示詞、**6/6** big 的 `kicker/text/sub` 與 claims 視覺欄同文。11 組 loop 的 setup／payoff 仍存在且順序正確，包括 `moon004→moon023` 和 `moon031→moon047`；新接點 `moon028→moon030`、原有跨章 `moon031→moon032` 均通順。
- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` 回報 **0 errors／0 warnings、133 lines**；`git diff --check -- docs/videos/curio-s49 tasks/open/2026-10-20-curio-s49-1835-moon-hoax-source.md` 通過。以 repo `spokenUnits` 及偏快 325 units／分鐘重算：前八景 176 units／32.49 秒、正文 2,658 units／490.71 秒（**8:10.71**）、片尾 59 units。這是文字估時，尚非 R10 音訊實長。

**範圍結論：來源與書面畫面 PASS，只綁定表列 R10 SHA。**新稿仍須兩位全新隔離讀者完成正式十三題雙盲；R9/R8 舊 WAV 不代表 R10 speech hash，完整音檢及後續關卡仍待新稿執行。本覆核沒有做政策、本站核准、TTS、付費插畫、配樂或成片。
