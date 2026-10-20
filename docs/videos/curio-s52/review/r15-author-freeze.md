# S52 R15｜相鄰句重述的最小刪除

2026-10-20 UTC。R14 的[兩位真正隔離的敘事盲讀正式合併](r14-isolated-merge.md)為 **HOLD：`no_recap` 唯一共同否決**。相鄰 `s52122` 和 `s52315` 都說 1771 年原報分列格林、庫克、索蘭德，後句未加入新事實。R15 **只刪整個 `s52315` 插畫場景及其主張列**；`loops` 裡開場 `s52007` 的回答點由 `s52315` 改成既有的 `s52122`。其餘口播、畫面提示詞、來源、企劃與研究均未改。劇本由 `video.json` 重生，所以刪除後的序號自動連續。

| R15 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `aed770f9ac194db89305ff8aa4ac3fdf87e800c356a32280c189a2690b0fd977` |
| `video.json` | `9ab5b5cc77ef6f0ea0fed5ce056a90e390964b6f63f44042657bd58c0f655068` |
| `script.md` | `1764cc03aa5bb5ea402e89b7e21e163d676045c6e42611dfaa54fdc69fa62131` |

R14 舊 `claims.md`／`video.json`／`script.md` SHA-256 分別為 `f133ff0dbed147fb7c06130db9a2f39a1202c6d73ca4e3d67c1f5aa6f2dde53d`、`e04880a6bec0b9cdcb517e0215de9060bb65844021d2f05e20a8234251a8a445`、`e1d04c2bd2e126baf5f777f8237cc1e4c075fdfc465ef6a183ec861fd212ae9c`。

`node tools/video/cli.mjs script --slug curio-s52` 已重生劇本；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s52 --json` 為 **0 errors／0 warnings**，`git diff --check` 通過。現有 117 景＝114 插畫／2 卡／1 片尾，119 句、21 伏筆。`estimateTimeline` 在 250／300／325 CPM 的濃縮開場為 43.87／37.80／35.63 秒，正文為 10:06.67／8:42.40／8:12.37；真正八分鐘仍須等 TTS 後量。R15 新雜湊須另一人獨立覆核來源／書面畫面，並由兩位全新隔離讀者評敘事。沒有 TTS 或付費媒體。
