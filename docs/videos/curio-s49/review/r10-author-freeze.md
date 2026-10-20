# S49 R10｜兩處重述的作者窄修與精確凍結

2026-10-20 UTC。[R9 正式雙盲](r9-official-panel.md)兩位全新讀者都只否決必答的 `no_recap`，但指出**不同**段落：A 指 `moon014/015` 緊鄰重複標題裡的赫歇爾名字；B 指 `moon023`、`moon026/027`、`moon029` 連續重述未交出的文件。本輪同時修兩處，不把同一結論搬到另一句，也不移動報紙虛構與固定史料的界線。

| 段落 | R10 差分 | 敘事及來源理由 |
| --- | --- | --- |
| `moon014/015` | 保留 `moon014` 交代標題使用赫歇爾姓名；`moon015` 只問「可一個名字，能替月球上的發現作證嗎？」 | 問題現在追問證據力，不再重說標題上的姓名。`moon015→016` 接出文章再搬來增刊的下一步。`moon014` 的 claims 直接錨點補至 [P02：1859 重印標題 L152–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L152-L165)，沒有把重印本當作已核對的 1835 原紙影像。 |
| `moon023` 至 `moon030` | 保留 `moon023` 對開場 `moon004` 助手來信的直接回答，以及 `moon024/025` 的皇家學會文件主張與其可核限度；刪除重列三項材料的 `moon026`、同義回答兼字卡的 `moon027`、再說未交文件的 `moon029`。`moon028` 保留文章對格蘭特消息與學會文件的**讀者興趣**比較，接著問望遠鏡如何看清月面；`moon030` 立刻開始那架虛構儀器的說法。 | 三個重述場景及其 claims／畫面直接移除，未在別處重安插文件清單。`moon028` 的「一樣引人入勝」對應 [P03 L224–239](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L224-L239) 的 *equal, in general interest at least*，沒有宣稱證據力相同；其望遠鏡疑問再連 [P05 L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520) 的虛構儀器對話。`moon004→moon023`、`moon031→moon032` 等 loop／跨章接點均未失聯。 |

固定全文仍是 Locke 名下 **1859 重印本** L SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，以及 Jacoby **1902 後出評論** J SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。`research.md` 的 P02／P03／P05／P06／P12／P13 歸屬、1859 出版者序與選錄層級、影片兩份固定來源 URL 都未改；沒有新增 1835 原報、Herschel 原信或獨立發行帳的主張。其餘旁白（含 30–60 秒開場、結尾建議及三句片尾）與保留場景的提示詞／字卡同文。R9 六句語音可辨性措辭中，`moon011/012/030/100` 保留，`moon015` 縮句，`moon026` 隨重述場景刪除。

| R10 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `f12b37209b51cb4888b0ff41c6f70bc5b7fecbeb721edf25a7c5fe60d189b034` |
| `script.md` | `c6389ff27c36856a914442644b71f746c66a89ddb1bd8f0f14a3f086d09fa51c` |
| `video.json` | `86361df066e0df920c5ae55055307eb4c6a46f1cae597c56569cb041f2732e80` |

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s49` 重生劇本；narrative 短碼 `1972fbd67094dfb5`、speech 短碼 `6222debc5607b665`。相對 R9 已修錨點稿，只有 `moon015/028` 兩句重寫、`moon026/027/029` 三景與其 claims 行刪除，以及 `moon014/028` 兩個 claims 來源欄補精確錨點。沒有其他台詞、`loops`、聲音設定、畫面提示詞或字卡內容改動。現有 130 編號景（124 `shot`、6 `big`）加一個三句片尾，共 **133/133** 劇本台詞同文同序；**130/130** claims ID／旁白同序，**124/124** shot 提示詞及 **6/6** big 卡片與 claims 視覺欄一致；scene／line ID 均唯一，11 組 loop 的 setup／payoff 均存在。

`lint --slug curio-s49 --json`：**0 errors／0 warnings、133 lines**。`npm run test:docs-videos`：退出碼 **0**、0 skipped。`npm run check:tasks`：退出碼 **0**、驗證 2,124 票；其餘票的既有 stale／scope overlap 提醒不影響此退出碼。`git diff --check -- docs/videos/curio-s49 tasks/open/2026-10-20-curio-s49-1835-moon-hoax-source.md` 通過。前八景開場 176 spoken units，按偏快 325 units／分鐘估 **32.49 秒**；正文 2,658 units，同速估 **490.71 秒（8:10.71）**；片尾 59 units。這些是文字估時，並非 R10 音訊實長。

**R10 狀態：作者稿已凍結，尚未獨立核准。** 下一位依上列**精確五檔**差分重核固定來源／書面畫面；另請兩位**全新且隔離**讀者按新稿做正式 13 題雙盲，不能沿用 R9 的 12/13。之後才做必要後續關卡與新稿音訊。R9 音訊仍為 HOLD；R8／R9 WAV 均不代表 R10 新 speech hash。此輪未做政策、本站關卡、TTS、付費插畫、配樂或成片。
