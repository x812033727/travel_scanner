# H11 韓語配音與逐句 QA

日期：2026-10-16（Asia/Taipei）。此收據涵蓋已核准的「四葉」版 H11 之韓語音軌，不代表多語上傳包已經核准或 YouTube Studio 音軌已上傳。

## 綁定檔案

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `4D2AE2A2C3D12D634A1333317FD25A816785B8A44DC6BB6E68C1E27A305532DF` |
| `i18n/ko.json` | `CB661D008D449E5FF5B46082F0C9F902ED3764BEE09ADF72BD441551ABC840E6` |
| 本機 `dubs/ko.m4a` | `BE09949E8773DF5686C4D9F94EF8C3E1B26D4257C3291CF3B460BCE1D46D1A3A` |
| 本機 `dubs/ko/narration.wav` | `A4A70C72941A3AB24B96447DDCCF022223C0FD157C405326BDE4759363DD9140` |
| 本機 `dubs/ko/timeline.json` | `CEFAAAE35E088A28FA36B68F5B2024C517ED49F5FFC0B4FD18DBF3802F482EEA` |
| 本機 `review/check.ko.json` | `8C2DD3CC650AD8CB9072801B6D31B680ED55DA71F2F2243229750975405844E9` |
| 本機 `review/check-flags.ko.json` | `7FAAA45156E71E2083AEA019CB288B158E16FC3EA8996F7EAB6F816829571907` |
| 本機 `review/whisper-small-ko-flags-20261016.txt` | `BBF2D3050828309DD0AA37BED6559F4782353FCBED132FED22F831FE4DAAA7A0` |
| 本機 `review/dub-ko.html` | `6172400BD867E18B015A57ADE86A9B08FA7987148C8C3009BF3865175B15D166` |

`dub --locale ko --dry-run` 為 73 請求、2,878 計費字元，預估 11 個視窗可能加速、0 無法塞入。實跑 73／73 組合成，0 重用；量得 73 視窗 0 加速、0 超出，`dubs/ko.m4a` 為 574.300 秒。先在共用帳本預留 US$0.15，再以工具回報核銷同額保守估算。

`check-audio --locale ko` 轉寫 75／75 句，1 次 TypeSafe Jev 差異判讀：57 句逐字相符、2 句 Jev 接受、16 句自動旗標。QA 先預留後核銷 US$0.50。H11 全集保守估算 US$4.298／8；三語新增 US$1.95／2，餘下 US$0.05 緩衝。供應商最終美元帳單不可得。

離線第二套 faster-whisper small（CPU int8、韓語、beam 2、無 VAD／前文提示）只核對兩句，因 U09 本機編碼正在佔用 CPU 而停止；不把離線轉寫冒充聽感。`v0e564e3` 核准稿「네 엽」被 Gemini 寫成「뇌엽」、離線寫成「내엽」，兩套都是近音字；`va972623` 稿「글만으로」被 Gemini 寫成「그림 안으로」，離線「굴만으로」在讀音上支持稿件。其他旗標及兩句對照保留在 `review/check.ko.json`、`check-flags.ko.json` 與逐句頁。

**站主已試聽並回覆「韓語旁白可以」。** 因此本版韓語音軌可沿用；不因自動旗標定向重錄，也不把此聽感核准視為多語上傳包、`languages` 後台卡或 Studio 上傳完成。

逐句試聽頁：`<home>/mokaair-work/videos/curio-h11/review/dub-ko.html`（先顯示 16 句旗標，可切換全部 75 句）。
