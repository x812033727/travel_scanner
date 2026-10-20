# S52 R14｜五月鏡頭時序定點修正

2026-10-20 UTC。R13 作者修稿後的獨立畫面查核發現 `s52053` 的提示詞把五月儀器問題畫在 `late May 1769`，而下一句 `s52310` 引述 1771 年原報，說儀器到 **5 月 10 日** 已安置妥當。R14 僅把這一景的 `late May 1769` 改成 `early May 1769`；相同鏡頭其餘文字、運鏡、畫面類型不變。提示詞只是相關插畫，不重建特定日子的儀器或觀測站。

| R14 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `f133ff0dbed147fb7c06130db9a2f39a1202c6d73ca4e3d67c1f5aa6f2dde53d` |
| `video.json` | `e04880a6bec0b9cdcb517e0215de9060bb65844021d2f05e20a8234251a8a445` |
| `script.md` | `e1d04c2bd2e126baf5f777f8237cc1e4c075fdfc465ef6a183ec861fd212ae9c` |

R13 舊 `video.json` SHA-256 為 `46ccd8047247b5a7ed143de1da813814c74e9371995745103ea764188c1ca328`；其餘四檔完全未改。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s52 --json` 仍為 **0 errors／0 warnings**，`git diff --check` 通過。R13 的旁白長度估算不變。須由另一人核 R14 精確分鏡差分與史料相容，再以相同 `script.md` 的兩位全新隔離盲讀判定敘事；本輪沒有付費媒體。
