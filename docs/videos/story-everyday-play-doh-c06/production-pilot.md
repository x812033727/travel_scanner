# C06 Play-Doh｜本機試片執行紀錄

本片依 [站主核准收據](reviews/owner-script-production-approval.md)執行：80 張插圖、每張最多三次，94 句旁白、一首配樂，整支 US$25 停線。僅製作本機試片；不匯入、不上傳、不發布。舊的 [製作前報價](production-quote.md)保留為核准前快照，凡稱「尚未核准」之處，以本紀錄與核准收據的較新狀態為準。

## 專屬發音字典

- 從 C06 Treatment 的確切提交 `3e49a964aa61f20fcf12743140984588a6a1c488` 建立隔離工作樹；在其 `video.json` 尚不存在時，以 PR #1676 `series.json` 的 16 個 `names` 呼叫 `initializeStoryLexicon`。本集工作資料夾在呼叫前不存在，影片工作資料夾的全域 `STOP` 不存在。
- 嚴格讀回 `videoLexicon({requireSnapshot:true})`：`mode=snapshot`，`sequence=1`，字典 SHA-256 `7dfd45e09466d424522c405627249ae59c42716572c7246979507bfff09c2477`，事件 SHA-256 `42b422ea8a45c866fb5fabd0a29e18ae74a15412a39dde1802a721dd13f8caa7`。
- 隨後合入 PR #1676 的逐字稿與逐鏡；`script.md`、`video.json`、`visual-plan.tsv` 三個 SHA-256 均與站主核准版本相同。沒有以偽造 `auto.json` 或遷移舊故事來越過字典關卡。
- 本次續做按先前站主採用的 C06 Treatment 方向，把其衍生的 `brief.md` 記入本機 outline gate，SHA-256 `C519DBB59D21C9E81D6EDA4A6E96D42B7031BF483D66854B1D8F66B8CC2900B0`；原 Treatment 的確切核准收據仍在 `reviews/owner-treatment-approval.md`。另以 `verify-1.md` 索引獨立代理已完成的 94／94 逐句 PASS 收據，沒有自稱新做一次來源查核。

## 停線與讀回

| 階段 | 實際結果 | 可核算支出 |
| --- | --- | ---: |
| 字典初始化與稿件合入 | 完成，嚴格讀回 sequence 1 | US$0 |
| 配音 dry run／額度預檢 | 已通過：94 個請求，約 2,716 個本輪計費字元；伺服器回報 `gemini:Sulafat` 可用、本月餘額 7,887,491 字元 | US$0（唯讀） |
| 94 句配音、正文量長與音訊查核 | 首次正式執行於 2026-10-22 05:33 UTC 遇供應商 429 並停下；容量恢復後同一稿件續跑，94／94 句已合成。第 02–06 章 86 句純音訊樣本合計 **505.94 秒**，超過 480 秒門檻；音訊逐句查核仍待執行 | TTS 回報本次 2,716 個計費字元；美元費用未有可拆收據，不能記為零 |
| 最多 80 張插圖及最多各三次品質評審 | 正文時長已通過；**仍須完成音訊查核與站主音訊關卡** | 待帳本讀回 |
| 一首配樂、組片與本機 QA | 待前階段通過 | 待帳本讀回 |

原報價可見圖片、評審與配樂上界約 US$3.32；正文旁白及其餘實際費用尚未拆定價，不能用差額推算可花額度。先前 `media-status` 讀回本片圖片、片段、配樂、評審均為零，該媒體帳本為 **US$0.00**；它不涵蓋旁白供應商的美元帳。容量恢復後的本次配音產出 94 個 WAV、`timeline.json` 與 `narration.wav`。整段檔案由 `ffprobe` 量得 645.933 秒；純旁白按 `timeline.lines[*].audio_samples / 48000` 加總，開場 8 句 43.83 秒，正文 86 句 505.94 秒，不用整段長度或章節空隙冒充正文。`timeline.json` SHA-256 為 `BBCF63328CBDF7BE5D017714AA657CDBC6DF45BAA4C93C53511D0E0773D37E65`，`narration.wav` 為 `FCDB56CD51CD5E3032172FECF6C47342F468790008285BF872AE220ABCDD5038`。音訊查核與站主聆聽尚未通過，圖片仍停線。

## 本機容量關卡

2026-10-22 05:47 UTC 讀回 C: 僅約 0.8 GB 可用，G: 是共用本機空間的 Google Drive，P: 是 pCloud 虛擬雲碟；不把同步雲碟直接當本機活躍媒體工作區。這一輪安裝的 C06 pilot `node_modules` 約 598 MiB，可重裝，兩支工作樹的 `package-lock.json` SHA-256 相同。嘗試對其**確切路徑**做 `Remove-Item -LiteralPath ... -Recurse -Force` 時，自動核准審查回 `blocked by policy`；沒有改用另一種刪除方式。即使語音 429 解除，買圖與組片前仍需先確認足夠的可靠本機容量，避免半成品耗盡 C:。

同日站主續做時重新讀回 C: **19.34 GiB** 可用，遂解除容量停線；未刪除前述遭政策拒絕的目錄。配音完成後 C: 仍約 19 GiB。每個大型媒體階段前仍須再讀回容量。

## 逐句音訊查核的預算停線

2026-10-22 08:16（臺北時間）開始的 `check-audio` 已保存 **71／94** 句轉錄；尚未對全片做 Jev 判讀，也沒有有效的逐句 PASS／旗標總表。讀回的 `review/check.json` SHA-256 為 `AFAB6BE842FF0C44AC6D644E2F142C69724EEC077412E8B2C089B508F6CEDF2A`。工具回報 `STOP found; transcripts so far are saved, rerun to continue`，專案 LEASE 已釋放；精確的 `<home>\mokaair-work\videos\story-everyday-play-doh-c06\STOP` 保留作停線標記。已完成的轉錄由工具快取，不能把 71／94 稱為音訊 QA 通過。

停線原因是本集 slug 尚未列入後端 `PILOT_SLUGS` 的單片預算表，而本機 `media-status` 只涵蓋圖片、評審、片段、配樂，不含 TTS、轉錄與 Jev 的美元用量。先前 US$3.32 的可見媒體項上界與 2,716 個 TTS 計費字元，均不足以核實整支 US$25 停線。現階段不再送出新付費請求、不移除 STOP、不買圖；須先取得可核算的語音／轉錄用量，或可執行的單片上限，再從快取續做並重新核對正文時長及站主音訊關卡。
