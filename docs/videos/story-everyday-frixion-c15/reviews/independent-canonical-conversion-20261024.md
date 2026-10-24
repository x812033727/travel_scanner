# C15 FriXion｜正式專案檔獨立轉換覆核

日期：2026-10-24。結論：**非付費、機器專案轉換 PASS；媒體製作 HOLD**。本覆核只讀核准原件及新專案檔，未生成語音、圖片、音樂或影片。

## 鎖定輸入與核對方式

覆核者由 Git `HEAD:` 讀取原件、由 Git index `:path` 讀取本次新檔，逐項比對 `owner-script-approval.md`、轉換收據及資料內容；不以工作檔換行或紙上估時代替原件。

| 核准原件 | SHA-256 |
| --- | --- |
| script.md | C75E85C881F51942C8CAD0BDD0185615F2CBDB6A2CCF2F6EED846724A6ECEBD4 |
| script-source-notes.md | 5429A1B0B04C412A0A50E8F47A4B39123CAE06D9E79771FCBEE9F26F23F2C121 |
| visual-plan.md | 60CD58C0F2BA2874550B34714132CDA8B56712DB81C43C1103F0644B2BB35A45 |
| visual-plan.json | B9E67726FDB99B71B3D6086AC38765EE513171F57E2261213FC843B66BC992A5 |
| treatment.md | D84494C81E2034B116C0322EF416E17C3DDE860B58626D12DE2E73501980D9C0 |
| source-matrix.md | 6E030F4399F6FD2AE99550DE89B5B46658D708CF870910199804069A784C4C09 |

| 新專案檔 | SHA-256 |
| --- | --- |
| video.json | FB222CAC8FD95FC773F9AEED5F0CAC028C83260C42F604FE9A2568F2FBFCC2F8 |
| series.json | 2CDB882A5037E00B7E2C92BEB8B727EDD3786CC7B14D3F6B2A00D5A619568191 |
| brief.md | 542EA469419527554C2D599FE763157A42C076008FF47829924AC7D2BA7C1C3F |
| claims.md | 49A2559169B2FE55ABF337589DB64E48CEE580BCA1B6D6B21299910927C07EB4 |
| verify-1.md | 6B83984E1C8D1383A0E79A4289BB58B5D4AFEB343DFFB9E74F5AACE8EA3C5F14 |

## 逐項結果

- 87／87 唯一句 ID、順序及旁白逐字吻合核准 script 與 visual JSON；87 景含 72／72 張 still 候選插圖及 15／15 張後製字卡。72 個 prompt、15 個卡片 value 皆逐字相同。
- 六章起點為 H01／O01／I01／E01／T01／N01；87／87 個 claims 引用原句，87／87 個 verify 狀態為 CONFIRMED，12 個 say_for 皆綁定相應原句 SHA-256 前 12 位。
- I16／I17 保留「另一色仍可見」；E08／E09、N07／N08 分開兩種溫度資料，I11／T10 分開微膠囊與筆尖。S1–S5 是直接敘事來源；S6 專利僅供來源矩陣背景核對，未借其支撐旁白。
- 全稿 2,350 字、開場 212 字、正文 2,138 字，紙上正文 513.12 秒，紙上 still 406.80 秒（79.28%）；均非實測 TTS 或成片片格。
- `video.json` 只有候選 prompt、沒有生成媒體或實測時間軸，`youtube.video_id` 為 null。原分鏡的畫面護欄保留於 visual-plan／claims；生成前須逐圖套用與驗收，不能只拿 prompt 當最終畫面核准。

## 後續停線

站主核准的本機試片仍以 US$25 硬停線：72 張基礎插圖、最多另 12 張、每槽最多三次，15 卡、87 句旁白、一首配樂。首筆付費前須讀回可歸因的單集預算路由、歷史費用與未結請求、供應商價格及最壞預留。購圖前須實測片頭後 O01–N20 配音至少 480 秒；成片須驗收繁中音訊、字幕及故事內容插圖片格占比至少 70%。本次沒有取得這些證據，也沒有匯入後台、上傳或發布。

核准 script.md 頂部沿用的舊「待重核」文字由較新的站主核准與差異收據解釋；不可為清理狀態而改動受雜湊綁定的原稿。C15「日本文字」的 lint 假陽性已由同分支、另案認領的 core 窄修解決：重新 lint 為 0 error／6 warnings，50／50 lint 單元測試 PASS；這只解除靜態規則錯誤，不解除上述媒體停線。
