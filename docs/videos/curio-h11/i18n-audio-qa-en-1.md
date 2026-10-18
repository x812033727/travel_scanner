# H11 英語配音與逐句 QA

日期：2026-10-16（Asia/Taipei）。站主已核准「四葉」修正版繁中劇本與 9:34 成片；本收據只記錄英語配音及自動辨識／離線分流，不代替站主試聽或 YouTube Studio 上傳。

## 綁定檔案

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `4D2AE2A2C3D12D634A1333317FD25A816785B8A44DC6BB6E68C1E27A305532DF` |
| `i18n/en.json` | `97D38C2A67649E6ADC3A92A884240C2A5F24D89B373387032703B4CFD09A290F` |
| 本機 `dubs/en.m4a` | `1F99A4E972FF550487ABF83DFB04F16F7283B3B84B9169E5C3A8A9CB0E7475F9` |
| 本機 `dubs/en/narration.wav` | `349BEEFB38005CA237319083CC8B4A2C52CBC1CF17FADDF8D7300FBA1AE457BB` |
| 本機 `dubs/en/timeline.json` | `AE1FCC9AB1765852F0F1F8E76843F52A9F3E9A0521DA799C13936859BEF47A84` |
| 本機 `review/check.en.json` | `83C0C9439A5A026239F28157B332CC8B3733EF596305B5ED1BF3BE9355AE8EB5` |
| 本機 `review/check-flags.en.json` | `04DD087DAD57AC7D4815C416790F560AE1D959C0341673A6BD55BF06E31AB639` |
| 本機 `review/whisper-small-en-flags-20261016.txt` | `D2D057B602D1C6A75743D465925C1D57B10C7BB229DFD1EC7348BC80BDEEEB31` |
| 本機 `review/dub-en.html` | `C0275FB2E92E01F202C8F4344847CFD99DFC121C849C7E562900A94EFB137D18` |

`dub --locale en --dry-run` 為 73 請求、5,641 計費字元。實跑 73/73 句組全部合成、0 重用；73 個時槽均不用加速，也沒有超出。成品 `dubs/en.m4a` 由 `ffprobe` 量得 574.300 秒。先在五集共用帳本預留 US$0.15，再依工具回報保守估算核銷 US$0.15；供應商最終美元帳單不可得。

`check-audio --locale en` 完成 75／75 句 Gemini 轉寫、1 次 TypeSafe Jev 判讀：64 句逐字一致、5 句 Jev 接受、6 句自動旗標。QA 先預留並核銷 US$0.50；英語目前新增合計 US$0.65／核准的 H11 多語 US$2.00 上限。離線複核使用 faster-whisper small、CPU int8、英文、beam 5、無 VAD／無前文提示；它不等於真人聽辨。

| 句 ID | Gemini 差異 | 離線轉寫 | 分流 |
| --- | --- | --- | --- |
| `v766e7f7` | 句首多出 `thought` | 無 `thought`，但句尾寫作 `raised doubts` | Gemini 句首辨識偏差；站主可順聽開頭排除真有雜音。 |
| `v57b521e` | `turned` 取代 `turn` | `turn` | 離線支持核准稿；無重錄依據。 |
| `va5b5d45` | `raise` 取代 `raised` | `raised` | 離線支持核准稿；無重錄依據。 |
| `v439465f` | `Marcie` 取代 `Marci` | `Marcy` | 人名的同音拼寫；未見內容錯誤。 |
| `v2ebbd0d` | `Nybes` 取代 `Naibbe` | `NIBIS` | 兩套皆為陌生模型名稱的音近轉寫，不能由拼寫確認發音；請站主試聽。 |
| `vb393dd6` | `texts` 取代 `text` | `texts` | 兩套均聽到複數；意義仍是可造相似文本、不能翻譯原稿。請站主試聽確認。 |

目前沒有足夠依據自行重錄任何句子。逐句試聽頁先顯示六句旗標，可切換全部 75 句：`<home>/mokaair-work/videos/curio-h11/review/dub-en.html`。仍需站主聽感判定，並另做日、韓配音與 QA、重建上傳包和語言送審；尚未上傳 YouTube。

站主其後已試聽並回覆「英語旁白可以」。此結果確認本版英語音軌可沿用，不等於新版上傳包、`languages` 審核卡或 Studio 音軌上傳已完成；上述自動旗標與離線轉寫原樣留存。
