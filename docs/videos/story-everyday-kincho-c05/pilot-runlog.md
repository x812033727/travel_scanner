# C05 金鳥蚊香｜本機試片執行紀錄

狀態：**正式旁白已完成，音訊查核未過；不買圖、不合成、不上傳。** 本集站主授權見 [核准收據](reviews/owner-pilot-approval.md)，整支 US$25 停線。2026-10-22 製作前 C: 約 19.3 GiB 可用，全站與本集 `STOP` 均不存在。與 C06 共用 Gemini 聲音供應商，C05 付費請求與 C06 錯峰執行。

## 固定輸入

| 檔案 | SHA-256 |
| --- | --- |
| `treatment.md` | `4A1C596B9A8A6E9278C99205E9EE381E4FD5AF4EAD5CDC6C448A852D5E7FC8D0` |
| `source-matrix.md` | `A7EB8401ABCC5715C46352187C0EFE100FA3AA47E22A020A1FC16FFD55504516` |
| `script.md` | `D49FE268109DDCE4BF6E44A3E75831467735DEC23E58D11BCC92065EE533288D` |
| `visual-plan.md` | `7908331CE21FE658321D8117D7429ECCA3C1F48C3D558E57B0885E5F26138CAE` |
| 原 `production-quote.md` | `73455BCB2E1A9A7A9E29023F6E39717E439DB20DCF27C1A02037868EFCD9DD36` |

`script.md` 正文表格的 79 個不同句 ID 與 `video.json` 的 79 個 `lines[]` 逐字相符；稿後另有 13 個重用句 ID 的鉤子索引列，不是新增旁白。核准稿第 2–6 章 71 句共 2,207 字元，詳見[估價勘誤](production-quote-erratum.md)。專屬發音字典已在 `story-lexicon/` 初始化；本機工作目錄的 `approvals.json` 已記錄站主劇本核准的精確 SHA。

## 非付費檢查

- `lint`：0 errors、13 warnings。警告含少數長句、鏡頭景別與規則式鉤子偵測；不把估計時間當媒體實測，也不改動已核准句子。
- `tts --dry-run`：79 句待合成，當下工具計 2,353 billable characters，伺服器顯示 Gemini Sulafat 可用。**乾跑沒有旁白秒數。**
- `keyframes --dry-run --takes 3`：目前 63 個付費 shot，最多 189 次生成，工具示圖片費一輪約 US$0.85、三輪約 US$2.55；另有 16 張本機後製字卡。站主核准的上限仍為 86 張獨特圖、每張最多三次，不能把乾跑工具的 US$2.55 當整支費用，品質評審及其他項都受 US$25 約束。
- TTS 前 `media-status`：本集 US$0.00，0 圖、0 片段秒數、0 首音樂、0 次評審。此媒體台帳不包含語音供應商費用，不能據此推論整支花費為零。

## 正式旁白與音訊查核（2026-10-22）

- 單次正式 `tts` 完成，79／79 句、2,353 billable characters、0 個重用 take，無 HTTP 429。`narration.wav` 48 kHz、79 句；`timeline.json` 總長 596.87 秒、全片純語音 515.81 秒。只加總第 2–6 章 71 句的 `audio_samples / sample_rate` 為 **484.74 秒**，比 480 秒門檻多 4.74 秒；任何重錄後都必須重新計算。
- 第一輪 `check-audio` 完成，79／79 句取得逐句轉錄、一次 Jev 判斷；35 句逐字相同、10 句僅同音或語助詞差異、10 句 Jev 放行、**24 句仍標記**，因此工具以 exit 1 結束。標記包括人名、品牌、工序與年份差異，不能直接視作音訊合格，也不能把所有轉錄差異直接當作配音錯誤。
- 不變更媒體或重買 take 的局部獨立檢查：本機 faster-whisper medium 對 `c050102` 轉出「金鳥回顧，它大約20公分長」、對 `c050107` 轉出「今天拿起一對螺旋，點燃前還要做一個動作」、對 `c050206` 轉出「金曜工廠說，用做原料的是白花除蟲菊，成分主要藏在花裡」。前兩句顯示 Gemini 轉錄可有誤；第三句品牌首字讀音相同，但本機轉錄仍非逐字相同。獨立程式只輸出到終端，未形成工具的正式第二意見收據；為避免重複吃 CPU 已中止其餘 21 句。待 C06 的音訊查核結束後，使用 `check-audio --second-opinion` 的正式路徑保留逐句證據，再依結果縮小重錄清單。
- `media-status` 不記 TTS／逐句轉錄／Jev 支出。本次未取得供應商逐請求美元收據，故不把 US$25 上限判作已驗證；任何下一步付費前要把語音費與媒體台帳合併估算並保持停線。

## 整支費用停線核算

以下是**模型允許的嚴格上界，不是實際帳單**。本集 `story-everyday-kincho-c05` 不在主機程式 `video_budget/models.py` 的 `PILOT_SLUGS`，所以主機沒有對 C05 逐請求預留／結算 US$25。主機的 Gemini 3.8 Flash TTS 價目為每百萬文字輸入 US$0.50、音訊輸出 US$9；每請求的模型上限 8,192／16,384 tokens，為 US$0.151552。Gemini 3.8 Flash 轉錄為每百萬輸入 US$0.75、輸出 US$3.75；非 pilot 路線沒有 `maxOutputTokens: 4096`，按照模型完整 1,048,576／65,536 tokens 算，每請求上界 US$1.032192。Jev 每百萬輸入 US$0.042、每請求至多 64,000 tokens，為 US$0.002688。價目和保守上界來自主機的 `video_speech/admin_api.py`、`video_speech/gemini.py`、`ai/jev.py`；Google [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) 為供應商價目。

| 情境 | 嚴格請求上界 |
| --- | ---: |
| 已執行：79 次 TTS、79 次轉錄、1 次 Jev | **US$93.518464** |
| 再加：86 圖各最多三次、逐圖評審及一首音樂 | **US$97.151464** |
| 若額外重錄 24 句、轉錄該 24 句，再做第二意見與重錄後各 1 次 Jev | **US$125.566696** |

即使不算轉錄的輸入，只算轉錄**輸出**可能達到的 79 × 65,536 tokens，加上 TTS 和可見媒體項，仍為 US$35.020648。這些上界遠高於站主核准的 US$25，不代表實際花了這麼多；已收到的 79 段短音頻與轉錄文字顯示實際用量應較低，但回傳的 provider token usage／金額沒有寫入 C05 的本機收據。**因此目前無法核證整支 US$25 停線，新增付費請求先停**；可繼續只讀本機音訊及來源查核。要續付費，須取得能歸屬 C05 的實際使用量／帳單，或有能在每次請求前強制卡住餘額的上界機制，再逐步核算剩餘額度。不把媒體台帳的 US$0.00 誤讀成全片 US$0.00。

可查帳途徑也有界線：Google [Billing 文件](https://ai.google.dev/gemini-api/docs/billing/) 指向 AI Studio Usage／Cloud Billing，但資料可能延後且按專案彙總；C05 與 C06 共用金鑰時，不能把專案總額直接分攤為 C05。Google [Logs 文件](https://ai.google.dev/gemini-api/docs/logs-datasets) 說 `generateContent` 預設不保存逐請求，只有當時已開啟專案記錄或明確存檔才可能從 Logs 讀回；目前本機沒有 158 次 Gemini 請求的 `usageMetadata`，也沒有那 1 次 Jev 的 token 收據。受保護 pilot 路線的白名單同時寫在主機與 CLI 的 TTS／媒體 client，單靠本機設定不能把已送出的 C05 請求追認成有額度預留的 pilot。

## 下一步與停線

1. 等 C06 共用語音供應商上的音訊查核結束，並解決上述整支費用停線的核算缺口後，對 C05 既有轉錄與 Jev 收據跑正式本機 Whisper 第二意見；此路線通常重用已付費轉錄，但可能新增 Jev 請求。
2. 僅對正式第二意見仍證明有唸錯的句子討論窄範圍重錄；重錄後重新量第 2–6 章純配音。低於 480 秒就停在音訊關，不買圖；改稿須重新查核、盲讀與站主核准。
3. 音訊 QA 合格後依奇聞檔案局流程送站主聽並取得音訊關核准，接著才檢查逐鏡實際時長、畫面與剩餘預算；圖像最多 86 張／每張三次，整支 US$25 停線，無上傳或發布授權。
