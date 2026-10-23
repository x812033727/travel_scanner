# U09 英語字幕第 91 cue 時長修正

日期：2026-10-17（Asia/Taipei）。`captions --slug curio-u09` 以現行英語配音時間軸重產 104 個英語 cue 時，唯一問題為 `fcd9695d` 第 91 cue：`08:32.133–08:34.243`，兩行 `Another paper will take`／`a different approach.`，44 個可見字元（換行也計入則 45）在 2.110 秒內顯示；工具診斷 21.3 CPS，超過英語 20 CPS 門檻。下一 cue 於 `08:37.000` 才開始。

只將第 91 cue 結束延至 `08:34.500`，同一文字顯示 2.367 秒、約 18.6 可見 CPS，距下一 cue 仍有 2.5 秒，不重疊。英語已審譯文 `i18n/en.json`、英文配音、繁中成片及其雜湊均未更動。英語字幕尚未送語言審核，後續上傳包要使用此版字幕。這是本集輸出檔的定向修正；再次執行 `captions` 會覆蓋它，屆時須重新套用並重查，不可沿用本次結果。

| 檔案 | 自動產生版 SHA-256 | 修正版 SHA-256 |
| --- | --- | --- |
| `captions/en.srt` | `7E4B965596EE161E390845683B6A579F46CC1FFEF059874F7F5004BCFD7A17A8` | `EC348773D0C455C959472D242793C20FB1765AE9ADDDE7B2109061E68A7417F3` |
| `captions/en.vtt` | `A3C511E6530E14836CEA86D660C2D2BCA4BB410939957240A5C0F9F438AA1E02` | `E21CD9DE10EDB405ACCB035235CB903F889C75A492571063FBA08A2BB5F57FA5` |
| `captions/manifest.json` | `5D5E480CA00B1A28549AE59D902AFE8557FCC944C6622005054A15DC6A424B6A` | `0E3C494B5328E087C9D925691A5C154D781DD88D2DDAFE599081148EF916D693` |

本機定向腳本 `review/fix_en_caption_cue91_20261017.mjs` 綁定三個自動產生版雜湊，只改 SRT／VTT 同一個時間戳，並在 manifest 的英語項記錄 `cue_overrides`，問題清單改為空。腳本執行後雙重讀回三個檔案；第 91 cue 文字和第 92 cue 開始時間均核對。韓語重錄後再次執行 `captions`，再套用同一個有雜湊護欄的修正；`review/verify_en_caption_cue91_20261017.mjs` 用現行工具 `checkCues` 複核修正版 104 cue 為 **0 問題**，SRT／VTT 每 cue 的文字與時間一致，第 91 cue 可見 44 字／18.6 CPS、到下一 cue 間隔 2,500 ms。日、韓字幕由同一次 `captions` 產生，分別 109 cue、manifest 0 問題；繁中 105 cue、0 問題。正式 `package` 與語言審核尚未執行。
