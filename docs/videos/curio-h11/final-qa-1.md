# H11 成片 QA 與人工送審

日期：2026-10-16（Asia/Taipei）。本收據記錄繁中成片的本機檢查與後台送審，不代表站主已核准成片、選定其他語言或上傳 YouTube。

- 站主已核准的 `script.md` SHA-256 仍為 `484436B7CA89D3D2F0E372D87768F0533B319B72ED40FCFE4413ADB26FE8E108`；75 句劇本與已核准旁白未改。70／70 張插畫的分鏡也已由站主核准。
- `render` 畫出 3 個卡片狀態；`clips` 使用 70 張 still，沒有付費影片片段。`assemble` 完成 17,226 格／30 fps＝574.2 秒（9:34.2）的 `final.mp4`，SHA-256 `060B86C335008868EA93CC1977417A64EBE0A63D7F2994762671D7BBF27D3A15`。合成收據為 -14 LUFS、true peak -1 dBFS、9 格與投影片比對通過。繁中 CC 為 104 cue，`captions/zh-TW.srt` SHA-256 `17A4BA0D7993D20501120C5A5AE6571CABBFFD8A95BCFF0C9219D8D02DA92A62`。
- 第一次 `qa` 為 8／11：片尾 `outro` 單一卡片 22 秒超過 15 秒、語言尚未決定卻按舊預設要求 en／ja／ko 字幕、Phys.org 的 2011 年轉載頁回 HTTP 403。Jev 政策判讀已通過。
- 來源項已改連結至 [Greg Hodgins 寄給 Yale 的 2009 年原始放射性碳定年報告](https://www.voynich.nu/papers/Carbon_GH_2009.pdf)，此 PDF 由第三方鏡站提供，不假稱仍在亞利桑那大學網站。報告第 1 頁記錄四葉取樣與處理，第 3 頁明說定年對象是羊皮紙而非落筆時間，第 8 頁列出合併區間 1404–1438 年；工具所用 GET／User-Agent 實測 HTTP 200。只更新 `video.json` 的來源標題與網址，版本 SHA-256 `FED1B627BD30491F9356FA7D9E061E9A872B9E7FFB8EE7B446409D4678363316`，`lint` 仍為 0 errors／0 warnings。
- 語言本機檔 `languages.json` 為 `{"locales": {}, "decided_at": null}`，依 `docs/videos/LANGUAGES.md`，時間為 `null` 表示站主尚未決定；這不是「只出繁中」的決定。成片階段只驗已做好的繁中 CC，待站主核准成片並選語言後才製作或送其他語言。
- `review-push --gate final --manual-review` 內建 QA 為 **10／11**，報告 SHA-256 `B7BE9ED1DDC41AF9724E0DB70B5EB5D3FBA6EAC0C34A6E409720F51D563E80BB`；唯一未過為片尾 `outro state 0 (22 s)`。其餘 assemble、render、narration、captions、metadata、facts、links（7／7）、thumbnail、Jev policy、disclosure 全過。保留已核准的劇本、音訊及分鏡，不自行把片尾畫面改版或將 10／11 寫成全過。
- 720p 後台預覽 `review/preview-060b86c335008868.mp4` 為 20,217,501 bytes，SHA-256 `CAF24A5CAB61FE1460BF2747B3C6981FEA5F418BFBB7315A00A121BC4C21E8EC`。`review-push` 回報 pending，隨後 `review-pull --gate final` 現場讀回 `final: waiting for the owner`。站主可從 `<home>/mokaair-work/videos/curio-h11/review/final.html` 或 `/admin/videos` 看預覽，判定片尾停留是否接受；未取得核准前不做上傳包。
- 最終 QA 含兩次 Jev 政策判讀（第一次獨立 QA、第二次送審內建 QA），共用停手帳本以 **US$0.05** 保守估算結算，沒有供應商最終美元帳單。H11 含旁白、音訊 QA、插畫的累計估算為 **US$2.208／US$6**，沒有 H11 未結預留。
