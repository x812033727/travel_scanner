# S49 獨立固定來源與書面畫面覆核 R1

**結論：HOLD（截至 2026-10-20）。**已逐一對照 `moon001`–`moon133` 的旁白、`claims.md` 錨點、`video.json` 書面提示及 `script.md`。主線有保住「1835 年報導／1859 年重印與出版者序／1902 年 Jacoby 評論」三個層級，沒有把發行量自述當實測，也沒有把 Jacoby 引用當另一份原報。不過 `moon083` 的旁白與原文相反，`moon066`、`moon079` 的圖像提示與原文明顯衝突，另有數個逐句錨點需補正。修正並重核後才可進入圖生圖或對外成片。

本覆核先獨立讀兩份固定原文及五份前製檔，**未先讀 `verify-1.md`**。以下 `L` 是 `/tmp/s49-moon-hoax-62779.txt`（Locke 名下 1859 重印），`J` 是 `/tmp/s49-jacoby-53396.txt`（Jacoby 1902）。所有行號指各固定文字的實際行號，非 1835 年原紙行號。

## 必修：說法與書面圖像互相矛盾

| ID | 現稿／提示 | 固定原文與改法 |
| --- | --- | --- |
| `moon083` | 旁白「先說遠處**像鳥**，拉近才像人」。 | [L 1175–1189](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1175-L1189) 首次看見時即寫 *“large winged creatures, wholly unlike any kind of birds”*，放入鏡片後才說像人。應改為「先說**不像鳥**，拉近才像人」或同義句。`moon078` 的「像鳥嗎？」是提問，沒有同樣錯誤。 |
| `moon066` | 旁白談類野牛額頭肉瓣；`video.json` 提示為 *“hornless animal sketch”*。 | [L 825–842](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L825-L842) 同時寫 *“semi-circular horns”* 與眼上的肉質構造。提示不可指定無角；可寫有彎角及額頭肉瓣的簡化草圖。 |
| `moon079` | 旁白明說「四群」有翼生物降落；提示只畫 *“a single small winged figure alighting”*。 | [L 1175–1187](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1175-L1187) 先說 *“four successive flocks”*，拉近後可細數三隊。此景應讓畫面表示多群降落，或改為讀者看著標示「四群」的字卡／圖稿，避免單隻與當句數量相反。 |

## 逐句錨點修正

`Pxx` 指 `research.md` 的錨點名稱。下表是現有**唯一**錨點沒有涵蓋整句時應補的來源；不是重新認定旁白都錯。尤其 `moon123` 是資料類別放錯，需先改。

| ID | 現有錨點的缺口 | 應補或改用 |
| --- | --- | --- |
| `moon001` | `P03` 從 L168 開始，沒有「1835 年八月」日期。 | `P02`：[L 164–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L164-L165) 說 1835 年八、九月首登《太陽報》。 |
| `moon003` | `P03` 只記載報導使用 Herschel 名字與好望角；「當時**真的**遠在南方」須由後出查核支持。 | 加 `P06`：[J 4054–4058](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4054-L4058)。 |
| `moon016`, `moon018`, `moon019`, `moon026` | `P03` 的 L168–254 在「our Journal」的虛構正文裡，沒有明寫被冒稱的刊名或「supplement」；`moon019` 尤其完整唸出《愛丁堡科學期刊》增刊。 | 加 `P02`：[L 164–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L164-L165)，並可用 [J 4063–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4063-L4070) 證明「取自增刊」只是偽稱。`moon026` 的 Grant 與皇家學會文件仍由 `P03` L224–239 支持。 |
| `moon029` | `P01` 是 1859 封面／版權頁 L30–85；它不能單獨證明全篇主張與轉折「都能逐行查」。 | 保留 `P01` 識別版本，另連到文章本體 `P03`–`P12`，或把這句標成對整份固定文本的編輯說明。 |
| `moon052` | `P05` 的 J4083–4125 批評虛構儀器，並未交代真 Herschel **研究南天**的工作。 | 加 `P06`：[J 4054–4058](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4054-L4058)、[J 4133–4137](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4133-L4137)。 |
| `moon093`, `moon094` | `P10` [L 1240–1244](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1240-L1244) 有將來的 Herschel 書，沒有前文提到的皇家學會文件。 | 加 `P03`：[L 232–239](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L232-L239)。 |
| **`moon123`** | `P13` 的 L2055–2193 是報紙反應選錄；全段沒有發行量五倍。 | **改 `P02`**：[L 122–131](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L122-L131)。這是 1859 出版者序，與 `moon124` 同源，沒有獨立帳簿。 |
| `moon129` | `P06` 的 [J 4054–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4054-L4070) 支持真旅程及偽增刊，但未出現助手名字／書信。 | 加 `P03`：[L 224–240](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L224-L240) 交代 Grant 在稿中的身分；仍只可說「稿件虛構的傳遞路線」。 |
| `moon130` | `P07` L720–840 可支持樹，沒有巨鏡製作或有翼生物。 | 並列 `P05`：[L 445–500](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L445-L500) 與 `P10`：[L 1175–1248](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1175-L1248)。 |
| `moon131`, `moon132` | 這是編輯歸納，不是 `P13` 報紙反應單段即可支持的「如何裝成證據／前一說法支撐後一說法」全程。 | 保留作結論；索引補 `P03`、`P05`、`P07`、`P10` 作完整來源鏈。`moon131` 若談「多少人」，可另加 `P02` 說明唯一量化說法只是出版者自述。 |

另有錨點表內部範圍不一致：`research.md` 把 `P12` 定義為 [L 1525–1565](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1525-L1565)，而 `claims.md` 對 `moon099`–`moon110` 的 `P12` 連結延到 L1635。`moon108`–`moon109` 的土星「發現」與精確數字在 [L 1563–1617](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1563-L1617)，**逐句連結足以查到**，但 `research.md` 的 `P12` 說明／範圍也應同步擴充。

## 需留意的用語與畫面

- `moon080` 說「沒有交給讀者**原始底片**」，而這份假記事交代的是觀測圖、版畫與布幕上的放大影像：[L 240–245](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L240-L245)、[L 1185–1196](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1185-L1196)。「底片」會把攝影式證據框架帶進 1835 敘事；建議說「可核對的原始觀測紀錄／圖稿」。書面提示的 *image card* 同理宜改成普通圖稿。
- `moon124` 提示「bookseller checking a clean **sales ledger**」，但這段只能核到出版者宣傳，現稿自己在 `moon125` 說沒有獨立帳本。雖寫 *clean*，若畫成真實有內容的帳簿會暗示本集查到了銷售紀錄。可讓書商看小冊或空白記帳頁；圖生圖驗收需檢查沒有可讀銷量。
- `moon125`「兩個數字當成測過的**銷量**」稍把「報紙發行量五倍」與「小冊售出六萬」併作同一銷量。可改「核實過的發行與銷售數據」。來源區分見 [L 124–131](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L124-L131)。

## 已核實的主要邊界

- [L 35、48、75–80](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L35-L80) 是 Rosse **1856** 圖題與 Locke 名、Gowans **1859** 版；[L 164–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L164-L165) 才宣稱 1835 年八、九月首登《太陽報》。`moon027`、`moon030`、`moon117` 卡片有標重印／原報未核對；書面畫面沒有把 1856 Rosse 圖當 1835 插圖。
- [J 72–74](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L72-L74) 確認 1902 版；[J 4054–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4054-L4070) 區分 Herschel 真實南天旅行與紐約製造的假增刊；[J 4105–4109](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4105-L4109) 稱假 Brewster 對話是無可理解的光學術語拼貼。`moon035`–`moon049` 與相關數字卡把器材歸屬報紙說法，正確。
- [L 2055–2191](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2055-L2191) 收有《Daily Advertiser》贊同、《Mercantile Advertiser》稱似真文件、對《Journal of Commerce》懷疑的《太陽報》回應、以及《Evening Post》Peter Wilkins 反諷；[J 4180–4193](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4180-L4193) **明說**這些引文取自同一本稀有重印，不是第二份獨立原報。`moon112`–`moon122` 的反應分裂與來源歸屬大體正確，亦未引用重印本可疑的 `_N. Y. Times_` 標籤。
- [L 122–147](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L122-L147) 是 1859 出版者署名宣傳，不是 1835 報紙發行帳。`moon123`–`moon127` 的**口語限定**與卡片「出版者自述／缺獨立帳簿」正確，僅 `moon123` 的索引連錯。

檢查數量：133 個 `moon` 場景、133 句正文；另 1 個 `outro` 含 3 句，共 136 句。`claims.md`、`script.md`、`video.json` 的 133 句逐字一致；127 個 `shot`、6 個 `big`、1 個 `outro`，書面插圖比例 127/133 = 95.5%。書面 `shot` 提示與 `claims.md` 均一致。這只核書面材料；未驗 TTS、實際生成圖片或成片。

## 本次核對的精確 SHA-256

| 檔案 | SHA-256 |
| --- | --- |
| `/tmp/s49-moon-hoax-62779.txt` | `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` |
| `/tmp/s49-jacoby-53396.txt` | `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` |
| `docs/videos/curio-s49/brief.md` | `48c3dc196b668c3ce3d58b4b3ffc26973262eb450587abfcc39d10d421057568` |
| `docs/videos/curio-s49/research.md` | `222638413339caaf05d48d984a2888c9c2c10e08f329eee24bb82c6881a58e8a` |
| `docs/videos/curio-s49/claims.md` | `d4b82e50b3a159827c59272983a9b086598bec92e2660e51f46e1643936eee34` |
| `docs/videos/curio-s49/script.md` | `0ddbd2976d478a1ea67abb8ba1ae9f2b5b3311e581a3861b52d83b031e14a9e2` |
| `docs/videos/curio-s49/video.json` | `e5ad1e333281ae47ef709cf94c319260d72b0f62b73cd083676f0c0f35860bf4` |
