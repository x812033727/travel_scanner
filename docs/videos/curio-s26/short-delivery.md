# S26 直式精華短片本機交接（2026-10-20）

七幕依序比較卡爾 1841 年帶保留語氣的皇后署名，與盧梭更早、只稱「一位偉大的公主」的引文。文字及固定 K41／R-FR／R-EN 原件見 [short-verify-1.md](short-verify-1.md)。使用長片既有七句旁白與七張已選圖，沒有新 TTS 或圖片請求。

本機成品目錄：`/workspace/.video-work/shorts/curio-s26-short-1/0f623d2c42813c39-1792493810189/`。

| 項目 | 現行結果 |
| --- | --- |
| 來源版次 | 長片 `video.json` SHA-256 `bb524cc7846a17a102d8b8c50322061977cdc897b097b7473c5b22e9edd77996`；`shorts.json` SHA-256 `d9f59d6c925ec637a6696a5941da9df5332a1922370b4a98461c36a2e1684850`；`from-episode --check` 為 1 Short valid、七圖檔 SHA 相合。 |
| 成品與語音 | `script.json` SHA-256 `13bfa382e792b8c98fc811134bc4dc383e88ceae2497da6c671a1c179c8c43a7`；`upload/final.mp4` SHA-256 `ec20dd8b44897237c679712352ffb7fba738fec90f5dff979c6c339bbea592b8`。1080×1920、30 fps、1270 格／42.333 秒；−14.02 LUFS、真峰值 −1.25 dBTP。長片 `ma007` 原 WAV 只在停頓拆成兩段，後段 PCM 降 1 dB，詞與樣本長度未變。原音對照表 `source-map.json` SHA-256 `f91f8b12dd126e21fda8d950574e3f7a565cb519adc0ea4de98f2a32149021ac`；`check-audio` 8/8、0 flags，收據 `check.json` SHA-256 `5d930f2d2afeb8c0217f122502aec2208e79771f2b525857f79df3390a493a29`。 |
| 原生畫格 | 製作者逐幕檢查實際成片 0.5／3／9／14.8／18.2／21.5／27.2／33.4／39.3／41.8 秒：七幕標題與繁中字卡可讀，無史料假字、明顯年代錯物或字幕溢出。第六幕 `ma031` 直式中心裁切只見空白書頁、人物在畫外，構圖 WATCH；未反轉「盧梭未留下公主姓名」的來源主張。首末回環 PSNR 39.5 dB。 |
| 來源／字幕 | `verify.json` SHA-256 `e0a2d91afb7a7dd1d1d54af20983a94e196c0e984fd135577daa476f84b57922` 綁 `script.json`、四項來源結論 PASS。繁中／英／日／韓各八 cue 均對齊 `timeline.json`；`caption-validation.json` SHA-256 `5a972d120764da1af45c88b6f21dbda87b6c4d8b2438609e5cc24ab00d0230d8`。英／日／韓字幕由製作者翻譯與時碼核對，尚無獨立語義審閱。 |
| 後台草稿 | 僅可逆 `client.report`，`draft-report-receipt.json` SHA-256 `438d5bd21e62ee978c18227e2e1dc5374986e28d3cc241070ae3c3d5674e324e`；讀回 `shorts_line=cut`、`source_slug=curio-s26`、`reviews=[]`、`youtube_video_id=null`。未呼叫 `submit`、`push` 或發布。 |
| 品管／上架包 | `qa.json` SHA-256 `1b54ed8d1f7a34d7bdf2adabc4f9caf2378f67935d0872bb864da8f4cf19009f`，**11/13**；精華 policy PASS（0.81），只有 `metadata`、`links` 因尚無真實長片 YouTube URL 未過。`package.json` SHA-256 `a074184badf8deb8ac351c2a8291a2f34342b9ab63edeceaaffcc912cf34c5d1`，**3/4**；影片、四語字幕、封面及生成圖揭露齊備，說明欄缺回連長片網址。兩條固定史料 URL 已在說明欄。 |

工具的 evidence 項依站台現有記錄回傳 PASS；它不能當成站主本人已核准 S26 長片現行 final 的證據。長片 exact MP4 有透明記載的本機委派驗收，站台 `hand_pushed` final 仍待站主審閱。Short 目前只是本機成片與可逆草稿。取得真正長片 YouTube ID 後，應讓工具產生回連網址並重跑 `qa`／`package`，確認同一成片 SHA 與全部項目均通過，才送 Short 正式審核。
