# AI 修補 PR 教學續作交接 — 2026-10-08

## 最新製作快照 — 2026-10-08

觀察 UTC：`2026-10-08T02:08:17.850773+00:00`。本段更新下方歷史快照的現況，舊記錄保留原文。

**目前：現稿文字與字卡節奏已覆核，新旁白及原生畫面已完成；音訊仍有 13 個 flags，未通過。** 離線第二轉寫器在 13 個 clips 上等待 36 分鐘後 timeout，未取得的 second opinion 沒有算成通過。尚無本輪 `final.mp4`，沒有本輪 audio／final／publish 核准或 owner 聆聽／播放驗收；既有大綱核准只綁 `brief.md`。完整任務保持 open。

### 現稿與技術綁定

| 項目 | 本次實際狀態／完整 SHA256 |
|---|---|
| `video.json` | 133 句、47 scenes；`4608bffb664b8d5a99667daae019184750b73fdaefe32256b08c0494f88c6cca` |
| `claims.md` | `8173695736493aa0f44e544d56354d898009c659d0180cf21dc8e3210c5eb809` |
| [第四輪全稿覆核](verify-4.md) | 350 項：164 CONFIRMED、186 OUT OF SCOPE、0 NOT FOUND；`255a7b05fa89c8785b52e71fbd26e6060f7ec2352b3b990b77e04cd65d781a9d` |
| `timeline.json` | 17881 frames／30 fps，596.033 秒；`dd583f584d719b2b59b8bba80a1cf6f657a5540351ebf4f8fbdbbec3b5b2ba87` |
| `narration.wav` | 原生完整 PCM／WAV 重建相符；`36913b8b9ed31b1cd132b243a38ac7e81c1ee82aaa9001f29cd27f6dc11df5a6` |
| `frames/manifest.json` | 47 scenes／88 states；`ca93ec80626c714eefb26a7ac078fd95eafbd0e8c81fd932f61b2831ccfb1b3d` |
| `audio/cache.json` | 133 原音與逐句 key 保持；`bf6e9eff38ce119eaf05ae796dd3592709ede9dc45fbafbecea436b98b700940` |
| `frames/cache.json` | 本次 manifest 所用 cached layout／glyph／font problems 為 0；`82c989e3b5354fd6cc5f33eb61549269ad1a86f29cd28562115f79506dd562a6` |

Native speech hash `2343b0c92135e5fa`、visual hash `7331c1203421e9d9`。對原 `7cdd…e0d4` 的 133 句逐項核對：全音檔 SHA、逐句 cache keys、文字及非 reveal line fields 相同，`staleTakes=0`。17482 增至 17881 frames，差額 399 frames／13.3 秒只來自 19 個新增 scene 的 700ms 間隔；沒有放慢語音、增加旁白或造新案例。原生實測節奏為 88 states、最長 13 秒、0 個超過 15 秒。

第四輪重新讀取 133 句、201 項 visual-data、7 項 metadata、3 項縮圖與 6 項章節。文字 VERIFIED 不等於音訊／成片驗收；原始 Claude 執行歸因仍不能由保留 patch、重跑或今日官方文件補證，現稿採可公開重跑的本地修補敘述。

### 新旁白已製作，後續刷新沒有重買

站主在得知舊媒體未找到及重複製作風險、看到新 28-request 計畫後再次說「繼續」，協調者據此開始本輪新主旁白。133 句新原音現已保存，已付答案與本機恢復證據保留。28 groups 是初始計畫；scene 分割 fallback／答案重用會影響實際呼叫數。續跑輸出的 288 billable characters 只屬續跑摘要，不能當整集總帳單。

- Native `tts --refresh-evidence` 真實 exit 0：`0 requests synthesized`、`0 billable characters`、47 reused。
- Canonical native render 真實 exit 0：0 drawn、88 reused、162 秒，沒有付費影像供應商。
- 只讀 consumer 重建完整 measured timeline／旁白，核對 133 WAV、88 actual stills 的完整 SHA、current render keys 與 state 位置。Transition 的存在／size 對原採用收據核實，完整 transition SHA 沿用該收據，本次 final closure 未逐張重 hash。這是技術完整性／節奏檢查，不是全部新字卡的目視驗收或影片播放。

### 音訊仍未通過，後續 gate 未完成

`check-audio` 於 `2026-10-08T02:01:57.468933Z` closed exit 1（`STOPPED_REVIEW_RESULT`）：133/133 checked，98 word-for-word、18 same-sound／filler、4 Jev judged fine、**13 flagged（threshold 0.5）**。第二轉寫器對 13 clips timeout 後，原 flags 仍成立；沒有下調門檻、把缺答案當 pass，或宣稱第二意見已完成。私有轉寫內容不複製到公開稿。

下一階段由協調者處理這 13 個 flags，保存實際改稿／retake／重查證據，再完成組片、timed CC、metadata、11 項成片 QA、audio／final／publish review 與 package 檢查。任何未知 paid request 保留證據與 hold，不能因本段推論可 retry。其他影片的韓語未知請求、Embedding 及 Citation holds 沒有由本輪釋出。

Metadata 文字已包含在第四輪全稿覆核，draft title 為「AI 修好 Bug 就能合併？三個 PR 檢查點」。實際 upload metadata 尚待原生產生及覆核：完整來源 URL／第一行 CTA、六個章節的最新實測時鐘、所選語言 title／description／tags／thumbnail，以及 SRT／VTT 身分、CPS／切分都須綁最終版本。四語文字草稿不是 timed CC 或 dub fit 證據；locale thumbnail words 的缺口仍在。語言只依站主正式選擇，本段未替站主選語言或核准 QA。尚未上傳或發布。

### 本快照私有證據索引

`<private>` 指本輪 repo 外工作目錄。下列索引不公開主機使用者、token 或私有轉寫。

- Current consumer：`<private>/recovery-audit/current-canonical-consumer-2026-10-08T01-55-06.028Z-97bd96f0-026a-4e66-97f0-40b49400b769/receipt.v2.json`；SHA256 `b986d62a9d1346b89b96de7f19c441ad2b06d6ef4dd9af0af83ec90df2f37db2`。
- Refresh：`<private>/runs/tts-20261008T012235951109Z-6ee65b76-6402-47a3-8f6d-d143d1bc7c5d/receipt.json`；SHA256 `06bdbd2237a09369447deae46d5fe74ed56b318312535cd5164d6f8074550c61`。
- Render：`<private>/runs/render-20261008T012557613909Z-736887ee-c807-4f7a-b0ab-a8905d6d3cea/receipt.json`；SHA256 `b184dedbca6a356d4b5de91d9aa01e34423f66e7e3046eae8d49bb9b60850b6c`。
- 音訊未通過：`<private>/runs/check-audio-20261008T012527754062Z-83ff6cf4-d490-4357-b637-ac1b802b805f/receipt.json`；SHA256 `d70674e9e6f668fb7c56d10ae291ef0044eb95025921a206832383008600eb6d`；output SHA256 `231ef7a95e86fd24423c6b681eed5ba3aeae8158c5bb23c9c53be0129b79d686`。
- Current flags：`<private>/media/ai-bug-fix-pr-review/review/check-flags.json`；13 個，SHA256 `d86168e03788bdfa1939bc80d2b7f0473b83ca26ae18fc7b26c7f2a8d0caf88a`。
- 原 133 原音：`<private>/private-audio-evidence/main-narration-integrity-20261008T004220205Z-13bb4193-7bec-4ff5-9ce9-6da84feaca2d.json`；SHA256 `4abffa6520b1e6cc2ddd459cb982ae3d21e3ec0256845c917ce53d16fd7df787`。

下方是新主旁白製作前的歷史快照，記錄當時未完成與授權界線，不覆寫上面現況。

## 歷史快照 — 2026-10-08，新主旁白製作前

本輪完成現稿事實修正、全稿第三輪獨立查核、四語字幕文字差異覆核與免費字卡重畫。旁白、時間軸、成片與待上架包仍未在本輪完成。對應任務保留在 `tasks/open/2026-09-27-developer-ai-bug-fix-pr-review.md`。

## 已驗證的內容

- 現稿 133 句、28 場景，完整 SHA256 `7cddf570305b4afa8d87833aec8fac92ab3469648674fd6d17d085fd0dffe0d4`。`claims.md` SHA256 `a0e439c36cd833291827c993c64e2ecd8d495fc83228b950fa93c3e7b434c983`。
- 第二輪保留七處 Claude 歷史作者歸因的 NOT FOUND；不覆蓋該輪報告。後續修正共五句旁白、四處字卡，保留 line／scene IDs。
- [第三輪全稿查核](verify-3-20261008.md) 逐項覆核 261 項：131 confirmed、2 changed、0 not found、128 編輯項。兩位覆核者分別實際重跑起始碼 2/2、事後驗收 1/4（預期 exit 1）、保留 patch 後 13/13（exit 0）。原始 Claude 命令、JSON、退出紀錄仍未找到；可重現的 patch 不證明工具作者。
- [四語字幕文字差異覆核](caption-delta-review-20261008.md)：en、ja、ko、zh-CN 共 20/20 修改句語意通過；每語 133/133 來源綁定 current，其餘 128 條完整 entry 和所有 metadata 維持原值。沒有將未改句稱為本輪重新逐語審閱。
- 兩個官方 URL 的實際 HTTP 200、raw body、解析文字、確認日期與完整 SHA256，均列在獨立查核報告。GitHub 文件支援 review 操作；Claude 文件不證實歷史執行。三關方法是本片的編輯建議。

## 免費本機製作

最終來源的 `lint` 實際 exit 0、零錯誤零警告；估計 10.2 分鐘、133 句、2286 spoken units。估計章節時間不是成片時間軸。

`render --channel msedge` 實際 exit 0，重畫 28 張 1920×1080 slide states，產生 contact sheet、主縮圖與轉場影格。`--channel chromium` 的前一次嘗試因 `spawn UNKNOWN` 失敗，保留失敗紀錄。沒有使用付費影像供應商。

協調者實際檢視全 28 張 contact sheet、四張修改場景（patch-source、diff-core、red-first、test-output）的完整影像，以及主縮圖；未見文字截斷或秘密／個資。這不是成片播放或旁白聆聽。四語目前沒有自己的縮圖文字，原生 renderer 使用主縮圖作 fallback，沒有替站主選新增語言或配音。

## 媒體缺口及重做界線

9/28 任務筆記曾記錄 Gemini Sulafat 133 句旁白與 18,255 影格、約 10:08 的 1080p 成片完成；它沒有可追溯的現存媒體 SHA 或原始工作目錄。本輪在預設影片路徑、已知工作目錄與 G 槽交付索引的有限查找沒有找到檔案。這不代表從未付費、已刪除，或所有磁碟均已查完。沒有為補歷史證據重跑 Claude，也沒有重買旁白。

最終稿的實際 `tts --dry-run` 為 28 requests、28 pending、4041 個原生 billable-character 估值，voice `gemini:Sulafat` ready；只做 speech-status GET，沒有 synthesis POST。這個估值與網站額度不是費用帳單或美元報價。

正式站 GET 快照（2026-10-07T23:22:03.961Z）僅有已核准且雜湊相符的大綱；沒有本輪 audio／final／publish 核准、語言選擇或 YouTube ID。未部署、未上傳、未發布。

後續先取得舊媒體／備份路徑，驗證原來源、音檔 cache、內容雜湊、原生狀態與不確定請求。若找回檔案，讓原生預檢計算可重用範圍，不能直接假定只要重錄五句。若要全新合成，先取得站主對已知重複製作風險的授權，再刷新 lease、STOP／hold、實際請求 journal 與額度；任何不確定的 provider 請求保留證據，不能盲目重試。

旁白完成後，依序作音訊品檢、組片、字幕計時、11 項成片 QA 與上架包檢查。語言只按站主勾選製作。上傳與發布由站主操作。

## 私有證據位置

生成物均在 repo 外的本輪 `<private>` 工作目錄。原稿及四語完整備份：`source-repair/20261007T234441233150Z/`；原始 source SHA256 `a17181e2c1058d0582d5968bc2fa143668f86ab5af4f424f5af18a4114a04741`。

本輪免費預檢：`preflight/20261007T235535491272Z-3c0278ca-aefa-4d5f-8272-5769b4d66fc3/receipt.json`；render 收據：`preflight/render-20261007T235009971443Z-983ba9f8-e7e2-49a0-b615-d4b0bdb6dfa1/receipt.json`。本地視覺 manifest 綁 visual hash `ffadd2e98aa7df20`。語音句子在 render 期間作最後一次修正，沒有改視覺資料；視覺相符不代表 speech hash 或舊旁白仍有效。

有限媒體與 CLI 查找：`recovery-audit/limited-media-and-cli-provenance-search-20261007T233825278658Z.json`，完整 SHA256 `c65d7599ca814e9cc0a12f5df6afad754da57869119eaac22ab5694477b85b12`。完整來源、語言、試跑及來源擷取收據的雜湊另見兩份獨立覆核報告。
