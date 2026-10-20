# S49 R15｜刪去重複判斷、保留事件推進

2026-10-20 UTC。R14 的兩名**隔離新讀者**各自對 `no_recap` 答否；[正式合併](r14-isolated-official-merge.md)為 12/13 HOLD。讀者 B 指出 `moon082→083` 連說「拉近後像人」；讀者 A 指出 `moon064/070` 和 `moon075/097` 都在反覆宣告虛構文字不是觀測證據。R15 只處理這些具體重複及刪句後的一處轉場；不以作者自檢取代新版獨立審查。

| 場景 | R15 改動 | 為何仍有新資訊／來源 |
| --- | --- | --- |
| `moon064` | 改為「還有一種樹，輪廓像橡樹，寬葉像月桂，枝上垂著黃花。」；畫面提示改為讀者在乾淨紙上畫闊葉與垂花，不描成 1835 原報影像。 | 1859 重印的**虛構報導**實寫這些樹木細節，[L 804–806](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L804-L806)；不再提前重說 `moon070` 的證據界線。 |
| `moon075` | 刪除「報導說得再仔細，也無法讓想像中的海狸變成標本」及其重複鏡頭／claims 行。 | `moon070` 已作過證據界線；`moon074` 回答海狸會用火的問句後可直接前進。 |
| `moon076` | 改為「海狸的屋子之外，這片紙上月面還住著誰？」 | 刪句後直接銜接小屋與下一章有翼生物；保留原 `moon076→082` loop 端點，明說是紙上情節。 |
| `moon083` | 改為「它甚至報出下一段觀測距離；究竟近到什麼程度？」 | 不再重說 `moon082` 的「像人」；`moon084` 隨即回答虛構記事宣稱的八十碼，[L 1182–1198](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1182-L1198)。 |
| `moon097` | 刪除「這不是建築遺址的觀測資料，只是同一篇虛構文字的下一頁」及其重複鏡頭／claims 行。 | `moon096` 寫完神殿與居民吃果子後，`moon098` 直接問下一天巨鏡出了什麼事，情節更順。 |

只有 `video.json` 的上述文字、`moon064` 提示詞與兩個冗餘 scene 刪除，以及 `claims.md` 對應行、來源錨點和刪行；`script.md` 由 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s49` 重生。未碰 `brief.md`、`research.md`、其餘旁白與提示詞、配樂、卡片、精華開頭及片尾。固定 L／J 原文檔 SHA 仍為 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`／`f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。

| R15 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `b9658ef9df619b6c92ba440ff395065a7702206690a72be863da24bcf098e8e9` |
| `research.md` | `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` |
| `claims.md` | `a9e869d51c898ad1cdd11d02291aff52198067c3cc8c154db899205fedc351f5` |
| `script.md` | `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` |
| `video.json` | `1cc788913568dc241e57221692b979fb9a699c7c0c36becacdb3e0c65109a37d` |

生成器 narrative `b3763737fac71100`、speech `96f0b30e8cb408c7`。128/128 claims 與編號 scenes 同 ID、同序、同旁白；122 shot、6 big、11 loop，端點全在；另有三句片尾，**131 唯一 line ID**。`lint --slug curio-s49 --json` **0 errors／0 warnings**，工具估全片 13.685 分鐘。正文 2,633 spoken units，即使按快語速 325 units/min 估算仍有 **8:06.09**；這只是文字估時，新版實際 TTS 尚未量。`npm run test:docs-videos` **236/236 PASS**，`npm run check:tasks` **2127 票驗證成功**，`git diff --check -- docs/videos/curio-s49` PASS。

**下一關：**另一位工作者按 R15 精確雜湊獨立覆核來源與書面畫面；兩名全新隔離讀者只讀 R15 旁白回答正式十三題，合併並保留 CLI 回條。R14 的敘事 HOLD 與 R12 舊音訊均不移轉。政策、網站劇本審核和 131 句音檢仍須按新版實情處理；音訊零旗標前不做插圖、配樂或成片。
