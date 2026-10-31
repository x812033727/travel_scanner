# S49 R7｜煙的回收、重述與支線：作者凍結

2026-10-20 UTC。這是**作者修稿與機械自查**，不是 R7 獨立來源／書面畫面裁決，也不是正式敘事雙盲 PASS。[R6 獨立來源覆核](review/r6-source-independent.md)對其列出的精確 R6 雜湊為 PASS；兩名全新 script-only 讀者的 [A](review/r6-fresh-panel-a.md)／[B](review/r6-fresh-panel-b.md) 都在 `payoffs`、`no_recap` 答 No，A 另在 `no_detour` 答 No。R6 票不能移作 R7 核准。

R7 保留 133 個編號景、136 句與既有 scene ID，只改 `moon009/013/067–069/072–074/095` 的台詞、`moon013/068/069` 的書面提示詞，並同步 `claims.md`、重生 `script.md`。`brief.md`、全部 `loops`、其他 scene、七張字卡、來源固定文本、片頭片尾規劃不動。

| R6 讀者指出 | R7 修復與新資訊 |
| --- | --- |
| A/B `payoffs`：`moon073` 問煙是否能證明文明，`moon074–075` 未直接回答 | `moon072` 根據 [L1009–1015](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1009-L1015)加入「幾乎每座小屋」；`moon073` 精確問煙能否證明用火；`moon074` 立即答「不能」，指出報導把從煙而來的推論寫成原文的 *no doubt*。保留這是虛構報導的邊界。 |
| A `no_recap`：`moon013` 第三次說赫歇爾在南方 | `moon009` 明示回呼開場真名；`moon013` 改成真實研究結束、報紙開始替他寫另一種發現的前進動作，不再重述地點。真實南天研究與報紙冒稱分別錨定 J4050–4080、L168–254。 |
| B `no_recap`：`moon095` 再說等待未交出的書 | `moon095` 直接回答前句：皇家學會文件與未來的書在當時不能替這些發現作證；作者用「將來會公開」推進下一頁奇景。分別錨定 [L233–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L233-L254)、[L1240–1244](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1240-L1244)。 |
| A `no_detour`：`moon069` 談「後來的講法」與獨角獸標籤 | `moon067–069` 改為虛構文章中單角小獸出現、觀測者伸手摸鬍子、影像中的牠跳開，均見 [L843–860](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L843-L860)。`research.md` P08 也修正舊註解：*Valley of the Unicorn* 在 [L884–889](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L884-L889)是山谷名，原文沒有直接把動物命名為神話獨角獸。 |

| R7 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md`（未改） | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `0728ecd77e4933406db1dc72533fcdc1fd8acfd5cc4bdf886891fb6cd13943c1` |
| `script.md`（CLI 重生） | `e31d202d5cb25b622839b50dab1448327585a7e5842f76d505dcb3e0994a56e3` |
| `video.json` | `756d156dc25e390bf7e5bf771a376122f177f330df706408954616ac5d2777d6` |

`script --slug curio-s49` 的 narrative 短碼為 `a5ad79cf310a499b`。`lint --slug curio-s49 --json` 是 **0 errors／0 warnings**。JSON 與 CLI 劇本逐字一致；136/136 台詞、133/133 claims ID 與台詞、126/126 shot 提示詞、7/7 big 字卡文字同序一致，ID 唯一。開場前八景 **176 spoken units＝32.49 秒**；正文 **2,698 units＝498.09 秒（8:18.09）**，皆按較快的 325 units／分鐘保守估時，未有實際 TTS 長度。`npm run test:docs-videos` **236 pass／0 fail**；`npm run check:tasks` 成功，僅倉庫其他票既有 stale／scope overlap 提醒；`git diff --check` 通過。

下一步由未參與 R7 修稿者重讀固定 L／J，按本表新 SHA 核對九句、三景提示詞、P08 與 claims 的來源差分；然後讓**兩名全新、只讀精確 R7 `script.md` 及固定十三題**的讀者正式雙盲。這些審核完成前，不送站台劇本卡、不跑政策、不啟動 TTS、付費圖、配樂或成片。本作者未跑政策或任何付費媒體。
