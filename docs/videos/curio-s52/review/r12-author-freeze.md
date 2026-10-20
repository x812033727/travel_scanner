# S52 R12｜書面畫面一處數量修正

2026-10-20 UTC。R11 [獨立來源／書面畫面覆核](r11-source-independent.md)判**史料 PASS、書面畫面 HOLD**，唯一必修處是 `s52128` 畫面提示詞的 `three unfilled off-site timing columns`，誤將兩支外派隊畫成三個外派地點。R12 僅將該詞改為 `two unfilled off-site timing columns`；旁白、主張、來源、分鏡 ID、章名與其他提示詞均未改。第三處是主觀測站，不能說成第三支外派隊。

| R12 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `8b5ece5ba66ecd672f6d8b89dd8191f087734f1d7277abce1fedca32b663f699` |
| `video.json` | `a23d2d57147f327e2f0c61283395e71ee5ede03374ef95e7468d815ffd14ceed` |
| `script.md` | `b9bae5c830d5e1260c4a034318f8bcede8a9824affa482b24d50a0e4a032be99` |

舊 `video.json` SHA-256 `3b4ae5f3dfda56df5b7d5a18fa397e62ced2e0936bec2350bae03cdc613721c9`；其餘四檔與 R11 精確相同。`script --slug curio-s52` 重生後 `script.md` 雜湊也相同。`lint --slug curio-s52 --json` 仍為 0 errors／0 warnings；118 景＝115 插畫／2 卡／1 片尾，120 句、21 伏筆。`estimateTimeline` 的 250／300／325 CPM 濃縮開場為 43.87／37.80／35.63 秒，正文為 10:19.70／8:53.40／8:22.63；改提示詞不改時長。`git diff --check` 通過。

需由另一位工作者對 **R12 精確 `video.json`** 做書面畫面差分覆核，並將 R11 史料簽核所綁的其餘四檔逐一比對；R11 的畫面 HOLD 不能由作者自行宣布 PASS。兩名新讀者的敘事審核、真實 TTS 八分鐘與媒體關卡仍各自待辦；本輪無付費媒體。
