# H06 v2｜運河與空白姓名原生圖卡交接

**後續正式關卡：**此文以下的「候選」數字是改卡當下的離線快照。兩張卡的現行 `narrative_hash=a8b72a5524beace9` 已由獨立盲評 **11/11 通過**。先封存舊時間軸、WAV、核准及語音檢查到外部 `review/native-card-audio-refresh-20261014/before/`，再確認 dry-run **0 to synthesize**，執行 `tts --refresh-evidence`：實際 **0 合成、0 計費字元、99 段沿用**。正式 `timeline.json` SHA-256 `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2` 已等於先前候選；104 個 line ID、音檔 SHA、逐句及場景時窗與舊版逐一相同，整段 WAV SHA-256 仍是 `528671067cbc165ca7d0ac32b487311dc147dc89a98eafe62515072cad57db0a`。正式節奏問題 0，49 個 `shot`／7,560 幀／50.3061%，最長狀態 239 幀／7.967 秒。新版音訊已送 `/admin/videos`，後台讀回 **pending** 且綁定新時間軸 SHA；須等站主核准後再 `review-pull`，目前不能稱音訊已核准。這些關卡仍不代表全片分鏡或縮圖完成。

日期：2026-10-14。這是前兩鏡付費小樣退件後的**離線畫面修訂**，供獨立敘事盲評、時間軸音訊核准及後續分鏡審查使用；不是已渲染成片，也沒有新增 TTS、MiniMax 或後台審核費用。退件原圖、裁切圖、judge、原始 manifest、ledger 與封存收據均保留於外部 `review/pilot-single-20261014/`。不得把退件圖當作可用 keyframe 或縮圖。

## 可核對的設計

| 場景／旁白句 | 原始時窗 | 現行圖卡 | 來源界線 |
| --- | ---: | --- | --- |
| `hook-canal-rail`／`j6u5` | 0–155 幀，5.17 秒 | [canal-concept.svg](diagrams/canal-concept.svg)：原創直線河岸與水帶概念 | 只依 [c02](claims.md) 表示 1920 年 2 月柏林運河；畫面標明非事發現場重建，無人物、救援細節或確切地點。 |
| `hook-canal-rail-beat-2`／`v201` | 155–293 幀，4.60 秒 | [unknown-name.svg](diagrams/unknown-name.svg)：原創斷開色帶與問號 | 只依 c02 表示警方未查出本名；畫面標明非警方文件、非當年物件。 |

兩場景從 `shot` 改為 renderer 原生 `diagram`，保留所有 scene ID、line ID、口播、章節與場景順序。SVG 的文字由本機向量圖確定呈現；不使用 AI 假字、假史料、人物或原始 1920 年現場照片。`thumbnail.data.shot=hook-canal-rail` 已移除，避免再指向退件圖。現有無圖縮圖只供版面預覽，右半留白，**不可視為已核准的封面**；先前有來源的 Dalldorf 病院史照封面概念留在外部 `review/source-thumbnail-concept-20261014/`，但正式工具尚無已驗證的直接導入途徑。

## 版本及離線驗證

| 項目 | SHA-256／雜湊 |
| --- | --- |
| 現行 `video.json` | `499fcab1f69d8eb9e9e25d65f9f89eb37ccd686142637092b8526762ba9b68a` |
| 現行 `script.md` | `f234894d5e77e672087838f22a23789394aa18a64b460dce33014f0995365cc4` |
| `canal-concept.svg`／`unknown-name.svg` | `0d5c9954aedf6da353d5545a19f9c3390cfa49d88837624b7815477fc2ee972d`／`7cca264ac4877317fc1cef79054d36267defa2f8d4a5f5f267d9ac2aec149295` |
| 新 `narrative_hash`／未變 `speech_hash` | `a8b72a5524beace9`／`9ae95e3507d3809f` |
| 新 `pictures_hash`／未變 `look_hash`／新 `visual_hash` | `a455e29bcc1b05ab`／`d57461da98a0ba9b`／`a7822161830bae74` |
| 尚在工作目錄的**舊**正式 `timeline.json`／未變 `narration.wav` | `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84`／`528671067cbc165ca7d0ac32b487311dc147dc89a98eafe62515072cad57db0a` |
| 同逐句音檔重建的**候選**時間軸副本 | `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2`；外部 `review/native-canal-cards-20261014/timeline-candidate.json`，**尚未成為正式時間軸或獲音訊核准** |

以正式時間軸中 104 句 `audio_samples` 重新跑 `buildTimeline`，逐句 ID、scene、`start_frame`、`end_frame`、樣本數及所有 scene ID、起訖影格與舊正式檔逐一相同。候選檔只把前兩個 scene 的 `template` 改為 `diagram`；不重錄旁白，不改 15,028 幀／30 fps（500.933 秒）正文。`script` 已重新生成；`lint --json` 為 **0 errors、1 warning**：49 個 shot 中 17 個含 `generic`，是兩鏡轉卡後分母縮小造成，並非節奏合格證明。未為消警告而擴改第三鏡提示。`renderProblems=[]`；依實測 WAV 時窗計算 `cadenceProblems=[]`、101 畫面狀態、最長 8.0 秒、平均 5.0 秒。

插圖規格為正文至少 50%：15,028 幀至少要有 **7,514 shot 幀**。本版 49 個 shot 合計 **7,560 幀／50.3061%**，只多 **46 幀（1.53 秒）**。這是依已量到的時間軸所作離線精確核算，不代表最終合成已過關。後續如實測片頭、片尾、轉場或任一 shot 時窗使正式 QA 低於 50%，**立即停下重新設計**；不能以退件圖、重播同圖、虛構現場或手改 manifest 補數。

隔離的 Chromium 預覽在外部 `review/native-canal-cards-20261014/`：`hook-canal-rail.png` SHA-256 `cf8db0b4b63d7cc7b8688817a71271862e7b0d224f6793186d24366ff9de7f0c`、`hook-canal-rail-beat-2.png` SHA-256 `4e291d5cfbd27733e39c9b10c857905e82b502e629c281de759df67cefbf3cfc`；兩張版面問題均為 0，已離線目視可讀。`thumbnail-flat-preview.jpg` SHA-256 `8655f97daea7fdbc125bb48f4b579bc3c3e2bc3a54f0da02ee09db69f3078242` 只是無圖 placeholder，並非封面交付。`preflight.mjs`、`preflight-receipt.json`、`handoff-receipt.json` 和時間軸候選檔留在同目錄，方便重跑與逐檔核對。

正文繁中 SRT／VTT 已用新 `video.json` 重跑**離線預覽**：104/104 句、104 cue，`checkCues=[]`，SRT `c4c7bb509e45d34e65cf8617532def8e6869a8bb083471c09287b48824370231`、VTT `74411a7dd5fb22fcee01b2905f38042150bb3fcbe7b5e8b753ce2cadf7890866` 均與舊預覽相同；更新收據在外部 `review/preassembly-captions-body-only-20261014/receipt.json`，原收據副本另存本目錄 `captions-before-receipt.json`。正式字幕仍須在 assemble 後依品牌時間軸產生、核對 `final.mp4`。

## 尚未通過的關卡

`narrative_hash` 因 template 變更已更新，原敘事盲評對此版本為 stale，需獨立盲評。`status` 暫讀到 `[x] narration approved` 只因**工作目錄仍是舊正式 timeline SHA**；一旦採用新 template 的正式時間軸，舊 SHA 的站主音訊核准不得延用，須送新時間軸供站主重核並讀回。舊 keyframe manifest 的圖片與 `pictures_hash` 不相符；目前仍缺 49 個現行 shot 的合格圖，分鏡、正式渲染、assemble、成片 QA、完整觀看、封面與上架包皆未完成。純色縮圖預覽與來源病院照片概念都不宣稱為最終縮圖。
