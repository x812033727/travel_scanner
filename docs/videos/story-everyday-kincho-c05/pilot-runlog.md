# C05 金鳥蚊香｜本機試片執行紀錄

狀態：**付費旁白尚未開始；不買圖、不合成、不上傳。** 本集站主授權見 [核准收據](reviews/owner-pilot-approval.md)，整支 US$25 停線。2026-10-22 製作前 C: 約 19.3 GiB 可用，全站與本集 `STOP` 均不存在。與 C06 共用 Gemini 聲音供應商，C06 正進行正式 TTS；C05 此刻只跑非付費乾跑，等待錯峰。

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
- `media-status`：本集 US$0.00，0 圖、0 片段秒數、0 首音樂、0 次評審。本集媒體工作目錄目前只見發音字典交易。

## 下一步與停線

1. C06 正式 TTS 結束後，再確認 C: 空間、STOP、稿件 SHA、核准狀態與媒體台帳。只做**一輪** C05 正式 TTS；若 HTTP 429，記錄結果立即停，不人工連續重送。
2. 若成功，以實際音檔／`timeline.json` 計第 2–6 章純配音是否至少 480 秒，跑 `check-audio`。未達門檻就停在音訊關，不買圖；改稿須重新查核、盲讀與站主核准。
3. 達標且音訊合格後再檢查逐鏡實際時長、畫面與剩餘預算；圖像最多 86 張／每張三次，整支 US$25 停線，無上傳或發布授權。
