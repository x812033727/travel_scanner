# Netflix X03｜固定畫風重製候選（僅前製，2026-10-20）

**狀態：可審核的重製候選，尚未開始付費重畫；舊 MP4 仍只供概念審看。** 本資料夾刻意不叫工具預設會讀的 `video.json`／`shorts.json` 路徑，避免 `from-episode` 或 `keyframes` 誤用舊工作區的 SVG 衍生圖和待審選圖。正式切換前須以本頁的雜湊與關卡重驗。

| 項目 | 固定值／目前結果 |
| --- | --- |
| 現行概念稿 `../video.json` SHA-256 | `08c931bb000f373fbf5778d02b0703ef1a8b5144c665bfa30afda7c44ed3e5ac`；舊 MP4／收據仍指向這版，不得改寫其身分 |
| 本候選 `strict-look-video.json` SHA-256 | `4ba2b46746b6bc83960cdf45aa557ba408f280a8e9c4086d27ff99cafd638d8b` |
| 差異 | 僅刪除 `/look/style`；`look` 精確等於 `{ "preset": "cute-mystery" }`。80 句口播、80 個句 ID、65 個 shot 提示詞、12 張後製數字卡、1 張 outro、來源、配樂與上架文案位元組內容均未變 |
| 既有獨立審查 | 候選檔雜湊**恰好等於**先前 [25 鏡來源審查](../reviews/source-review-visual-revision.md)、[提示詞審查](../reviews/visual-prompt-review.md)及 [結構化收據](../reviews/visual-prompt-revision.json)所審的版本。該審查只核准稿件／提示詞，不核准任何媒體。文字的兩位盲讀綁前一版口播修訂稿；結構化收據證明後續只改畫面提示詞，沒有重寫口播。 |
| 影像計畫 | 65 張 `shot` 均須重新由 MiniMax `image-01` 在新工作區依本候選畫出並通過逐張審查；12 張後製卡單獨製作。若全數是真正 MiniMax 圖，正文插圖比例為 **65／77＝84.4%**；目前僅是目標，**不是**已產出的合規比例。 |
| 時長 | 舊時間軸嚴格扣除 50.03 秒開場與最後三句後，正文 **8:00.70**；新剪輯不得沿用這個極窄餘量，必須重算影格。 |
| Shorts | [兩支腳本](shorts.json) 各 6 景、157／166 字，按 250 字／分鐘只可粗估 37.7／39.8 秒；實際 TTS 後須驗 25–55 秒。它們與候選稿的 scene ID 和格式檢查無誤，尚未配音、裁切、合成或上架。 |

## 來源與驗證

[Shorts 逐拍來源複查](short-source-review.md)把每一景對回 Netflix 的 2006、2007、2010、2023 年 SEC Form 10-K 和既有 [逐句來源矩陣](../source-matrix.md)。這次沒有新增長片史實；短片的標題、說明和旁白也須在後續獨立盲讀／成片 QA 確認沒有把「全年寄出總片數」、「人均月租片數」及「多數訂戶各自的觀看方式」混成同一分母。兩支 Short 的 SEC 原件網址已放在 `links`；正式長片網址不存在，不得先填假連結。

唯讀檢查已證明 `strict-look-video.json` 除 `/look/style` 外與現行 JSON 相同、現有專案 context 下 `lintProject` **0 錯誤／0 警告**、`episodeShortsProblems` **0 問題**、全部 Shorts 引用有效 shot。這些只查文本結構，不替代逐張影像、聽審或費用核對。

## 尚未通過的製作關卡

1. **全額費用 HOLD。** 舊媒體台帳只見 US$1.7135（122 張候選圖、121 次評審與一首配樂）；語音、轉錄、額外複查和稅費的供應商明細未齊。舊版對 65 景、最多三次的唯讀估價約 US$2.63，只是圖片與評審估算，不能當整集 US$25 的剩餘額；新版正式開畫前再乾跑，並能證明累計全額加最壞重做不超過 US$25。
2. **隔離重畫與逐鏡驗收 HOLD。** 不匯入舊 `keyframes/manifest.json`、手繪 SVG 衍生 PNG 或先前 `look.style` 的 MiniMax 圖。新工作區每鏡記 `image-01` 任務、實際檔案 SHA、提示詞、評審、人工畫面判斷；尤其查假字、擬人郵袋、三片上限、2006／2007／2010／2023 時序和跨年份重複圖。未過鏡頭保留 `needs_review`，不得合成為正式畫面。
3. **時長、聲音與 Shorts HOLD。** 沿用的 80 句聲音仍需人耳驗聽；新主片重新核算排除開場及結尾三句的正文，至少 8 分鐘。兩支 Short 要在合規主片影格可用後，搬到預設 `shorts.json`，分別做 TTS、25–55 秒量測、9:16 裁切、安全區、繁中字幕、聲音與來源 QA；主片核准且有正式公開網址前，不送 `package`／`push`。
4. **正式品牌與上架 HOLD。** 目前只有明標概念的 5 秒／21 秒動畫；正式已選片頭片尾、人工核准及 YouTube Studio 兩個可點影片元素和訂閱元素的連結驗證仍缺。不得把現有 MP4 描述成正式成片或已公開影片。

切換時先保存舊概念稿及其收據，再將候選檔移到 `../video.json`，在**新的** X03 媒體工作區重新乾跑、生成、審查、合成與記錄候選 SHA；切勿從舊工作區續跑。候選稿的既有審查鏈只核准文字與提示詞，Shorts 的新敘事仍待獨立盲讀收據綁定 `shorts.json` SHA。

**付費明細的唯讀複查：** 本機配對工具 `media-status --json` 的 X03 總額 US$1.7135 分解為 122 張 MiniMax 圖 US$0.4235、121 次 Gemini 畫面評審 US$1.21、1 首 Lyria US$0.08；其 `totals` 沒有語音、逐句轉錄、語音評審或稅費。`tts --dry-run` 回既有語音 2,332 計費字元、目前待合成 0 字及月字數額度，沒有美元帳；站台 `/speech/status` 的資料結構也只列字元與額度。這些資料仍無法封閉整集 US$25 上限，因此維持 HOLD。

不能單靠公開定價推翻 HOLD：X03 不是站上有逐次美元結算的 pilot slug。`apps/api/app/video_speech/admin_api.py` 對非 pilot 轉錄不設 4,096 output-token pilot 上限；`apps/api/app/video_speech/checking.py` 送出的 `max_output_tokens` 為 `None`，本機的 `review/check*.json` 留下文字而非每次 `usageMetadata`。Gemini 3.8 Flash 公開模型最大 65,536 output tokens，以程式記載的 US$3.75／百萬 output tokens 算，每次最壞可達 US$0.24576；首輪 80 句、15 句重錄再查、12 句改詞再查，光這約 107 次轉錄的最壞 output 上界就約 **US$26.30**，尚未加 input、TTS、畫面與稅。實際費用很可能低許多，但可見逐字稿長度無法限制供應商內部 output／thinking tokens；沒有完整 usage 收據時不能宣稱 US$25 已確保。
