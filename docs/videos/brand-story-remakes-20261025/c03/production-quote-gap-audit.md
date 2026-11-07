# C03 全片報價與入場缺口：唯讀實作稽核

結論是 **HOLD**：現有證據還不能交付「含八語配音、全部允許重試與未明費用，保證 US$25 內完成」的全片報價。這與「所有未來 model-wide 單次預留相加一定要 ≤25 才能啟動」不同；後者**不是現行程式的入場公式**。本次沒有解除 hold、建帳、改價、派送付費、重寫既有收據，或宣告 source／native pipeline／故事媒體 PASS。

## 綁定與證據範圍

- 精確新 slug：`story-everyday-moleskine-c03-remake-20261025`。
- 現 `video.json` SHA：`9639d356ca5bdcb18e85c3631ea754a0f69888949358111f452541654ac7fdd9`。
- canonical runtime `script.md` SHA：`4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`。作者附來源 `c03/script.md` 是另一檔，不混用。
- 實際字典內容 SHA：`2db18c4c1ad647bb8891514977fbc6591fbfb15e7aeec80549b6ae588a9f26cc`；純函式重算 speech hash：`37aab4572320064b`。
- checkout HEAD：`4970d1be5a9affd0c84131c1930371cffaf5aa6c`。遠端 main 另以 `git ls-remote origin refs/heads/main` 讀得 `87d427ffe8164c3f7dd3b837903d30a9eaeab547`，再 `git fetch --no-write-fetch-head origin <精確SHA>`、`git show` 讀物件。沒有切分支；本地 `origin/main` 仍是 `8c338dfc264dedaf200e4e50da816631285c207a`，不稱它為最新 main。遠端快照與記錄時間、30 個程式檔兩版本 SHA 全列在配套 JSON／外部 manifest。
- 三個關鍵 policy 檔 `video_budget/models.py`、`service.py`、`pending-pilot-budget.mjs` 在上述 HEAD／遠端 main 相同。main 的 check-audio 更新是多語文字比對與第二轉寫判定，**沒有改成跨句 ASR**；flow 的差異是角色 look 重畫，本稿沒有角色。正式主機程式版本仍**未知**，不假設與任一版本相同。
- 08:22 UTC 正常 native credential 的 `GET /api/video/speech/status` 與 `/media/status` 均 HTTP 200；08:23 UTC 再取必要 image/music 價目 subset。Sulafat 可用，TTS allowlist 含 `gemini-3.8-flash-tts`；圖片選 `minimax/image-01`，配樂選 `gemini/lyria-3.5`，圖片設定重試 2 次。沒有印 token、環境、DSN、全站帳戶或呼叫供應商。
- `/speech/status` 不揭露 ASR、圖片 judge、Jev 實選模型、計費帳戶／區域／帳戶價格；原／新 C03 沒列在 `/media/status` 仍不能證明 DB 沒帳戶。先前 Node 直接 fetch 的失敗、urllib 摘要器讀 models 形狀失敗均保留外部紀錄；結論依後續完整正常 GET，不拿失敗當主機證據。

## 逐階段真正會怎麼數

純本地呼叫目前 `planRequests`、`dubScript`、`speechLexicon`、`speechHash`，沒有執行 TTS 或以假 timeline 冒充實聲。九軌都是 143 句、120 個初始 TTS requests；其中 22 個多句 request 共 45 句。

| 軌道 | 初始 TTS requests | 目前計費字元 |
| --- | ---: | ---: |
| zh-TW | 120 | 4,194 |
| en | 120 | 12,277 |
| ja | 120 | 6,036 |
| ko | 120 | 6,815 |
| es | 120 | 12,420 |
| pt | 120 | 13,163 |
| id | 120 | 13,300 |
| vi | 120 | 12,257 |
| th | 120 | 11,187 |
| 合計 | 1,080 | 91,649 |

八語翻譯均無 missing/stale line；本結果只重算當前文字／請求，沒有提升原本的文字、語意或 native 審核等級。八語 metadata／CC／dub 已由後台實選 all true，不能在報價裡默默去掉配音。

`tts/requests.mjs` 依 scene、聲音與語氣／1500 字限制切組；`tts/synthesis.mjs` 先買整組，再按靜音切句。多句組切分不合理時，已付的整組音訊擱置，再逐句買。因此每軌首輪最壞 **120+45=165** 次，九軌最多 **1,485** 次；不是只買 120 次就保證拿齊句檔。字元是 Gemini 月額度與乾跑資訊，供應商美元公式採 input/output tokens，不能用字元直接當音訊成本上限。

**ASR 的 grouping 已可確定。** `tts/check.mjs` 對每軌每個 line ID 的 WAV 各呼叫一次 `transcribeClip`，由 48k 降成 16k mono；API `TranscribeIn` 也只收一段 line clip，沒有跨句合併。冷快取且九軌實際音訊都存在、格式合法時，首輪為 **9×143=1,287 次 ASR**；單軌是 143。真 WAV 尚未產生，故實際 ASR 次數仍是 0。無須等待 duration 才能數首輪 line 數；必須等待真 WAV 才能驗每段 ≤75 秒、配音 fitting、實際 tokens、重錄範圍。clip hash 與 hints 相同的重跑用快取，改了才重轉；連續 3 次服務轉寫失敗會提早停。

**Jev 才分組。** 先做文字／同音等本地比對，只把 mismatch 跨 scene 每最多 40 句送一個 Jev request，143 句每軌每檢查輪 **0–4 次**。若啟用第二轉寫，仍有疑慮的第二份結果最多再 4 次 Jev。第二轉寫是外部可設定 command；repository 的 Whisper 是本地運算，但未知主機 command 不能先當成免費或已配置。

圖片是 100 個 drawn shot，無角色設定圖、無 end-frame 生成、無影片片段生成、無 style-plate 生成；本稿圖片與 MiniMax image-01 不需 plate。按本批已定含首次最多 3 take，最多 300 張與 300 次圖片 judge。兩個正式 bookend 檔是 reuse，故事生成媒體仍 0。繁中燒錄／clean export、CC、音軌 mix 是本地處理，沿用同組付費素材。

## 四種金額不要混用

| 類別 | 現行實作／結論 |
| --- | --- |
| 目錄／retail estimate | image-01 每張 0.0035、圖片 judge 每次估 0.01、Lyria 每首 0.08；100 景×3 take 的 4.05 是這一層，不是圖片 judge 的正式最高 reserve。 |
| 每 operation reservation | TTS 0.151552；ASR 與圖片 judge 各 1.032192；Jev speech/policy 0.002688。這些有模型與價格期限條件，不是每次預期真的付這麼多。 |
| ledger 的 actual | 語音／ASR／judge 由回傳 token usage 套碼內價率結算；缺 usage 留 uncertain。圖片／音樂 ready 時以 `job.usd_estimate` 結算，沒有抓 supplier invoice。尚不能把 ledger 欄位名稱 actual 當成已核對帳戶帳單。 |
| 累計停線與完成保證 | 下一筆 reserve 前檢 `settled + reserved（含 uncertain）+ next ceiling ≤25`；足夠餘額才派送。逐筆以小額實耗結算可騰出額度，但未替未來所有交付保留資金，不保證所有配音與重試都能完成。若真帳單超預留，程式記 overrun 並停後續，不能撤回已發生的費用。 |

碼內價格有效期至 2026-12-31，本報告沒有上網重新核供應商公告或帳戶價格。TTS 的模型最高 8192 input／16384 audio-output tokens，單次 `(8192×0.50 +16384×9)/1e6 =0.151552`。ASR 與圖片 judge 使用 Gemini 3.8 Flash 模型最大 1,048,576 input／65,536 output（含 thinking），單次 `(1048576×0.75+65536×3.75)/1e6 =1.032192`。Jev 64,000 input tokens、0.042/M，單次 0.002688。

已存在的較窄**輸入／generation 限制**沒有變成較窄的美元 reserve：

- TTS 有已知短文本與 1500 source 字限制，但 provider request 沒有 maxOutputTokens 或硬 audio duration，reserve 固定用模型上限；字典 alias、style 也使字元不等於完整 token 數。
- ASR 已驗 16k mono PCM、≤75 秒，也送 `maxOutputTokens=4096`；碼註明 audio input 約 32 tokens/s。然而 reserve 與 usage 接受範圍刻意仍用模型最大 input／output。沒有完整 provider prompt token 計數與可驗證的「此請求最高應付」函式，不能在報告中自行換成 4096-output 價格。
- 圖片 judge 限 stored still、最大邊 1536，亦送 maxOutputTokens=4096，reserve 仍是模型最大值，非 0.01。
- Jev 的 40 句／欄位長度與 rough token estimator 可提早拒絕過大輸入，但 reserve 仍是 vendor 64k 最大值；rough estimate 沒有用來作較低美元上界。
- image/music 已採單張／單首固定目錄價預留。帳戶／區域／計價單位是否與該價相符，仍須供應商資料確認。

## 可重算數字的意義

| 項目 | 單次 cap／目錄價相加（US$） |
| --- | ---: |
| zh-TW 首輪 120 TTS | 18.186240 |
| zh-TW 首輪含所有切分 fallback，165 TTS | 25.006080 |
| 九軌首輪 1080 TTS | 163.676160 |
| 九軌含所有切分 fallback，1485 TTS | 225.054720 |
| 九軌各一次檢查，1287 ASR | 1328.431104 |
| 300 張圖本身 | 1.050000 |
| 300 次圖片 judge 正式 cap | 309.657600 |
| 九軌最多 36 次首份語音 Jev（無第二份） | 0.096768 |
| 一次 policy Jev／一首 Lyria | 0.002688／0.080000 |

取三 take 圖像、上述首輪語音及一份 policy，**未含 retake／未知費用**的相加為 1802.994320；若所有 TTS 切分 fallback，為 1864.372880。它們是「沒有被 US25 提前停線時，把現行每筆最大值相加」的示意上界，**不是 retail expected quote、實際帳單、或可以發出的承諾額**。硬停線會在額度不夠時截斷這條路徑，可能留下未完成片。

這些數字說明目前 model-wide reserve 方法不能證明全片在最壞情境必完成，**不能單憑總和 >25 推論任何合法順序工作流都不能啟動**。若未來完成受審啟用／核價，一筆結算後剩餘餘額足以容納下一筆 cap，現有程式可以續做。原 `pricing-and-entry.json` 的 169.919696 是明標「假設單軌143 ASR」的局部示例，保留不改；它未含八語、retakes、圖片 judge 真 reserve 與未明費用，不能充當全片報價。凡舊交接把該示例推成「所有未來 model-wide caps 的 sum 必須 ≤25 才可開工」，本稽核明確修正此推論。

## 重試、八語完成與尚未封住的邊界

- zh-TW 自動 retake 輪數來自有效 `max_retake_rounds`／drama 覆寫，本輪必要 GET 不揭露它。單次整軌全重錄含切分 fallback 最多 165 TTS、重新 ASR 最多 143；固定稿的條件式為 `165×(1+R)`／`143×(1+R)`。worker 另有最多 2 次旁白改詞，但本任務未授權改 frozen canonical；要走那條路必須另綁新稿與 quote，不能當這版原有媒體。
- 每個 dub 自動生命週期最多 2 shorten、2 retake、2 reword；在固定 143 IDs／同聲音分組、沒有人工 reset/force 的條件下，保守 TTS 最多 7 個全失效 pass，即 **1155 requests/語**。shorten 在可檢查前做，ASR 最多 initial+2 retake+2 reword =5 個全換 clip pass，即 **715 ASR/語**；語音 Jev 最高 20 次/語，第二轉寫另計。八語分別為 9240 TTS、5720 ASR、160 首份 Jev；這些是條件式 counterfactual 上界，US25 停線會先截斷，也不是本次新增重試授權。
- 八語可能需要最多 32 個未來 shorten/reword 文字 stage。現有已審翻譯可以重用，無須為相同 metadata/CC 再買初譯；pilot 的 API-priced text 明確以未知 bounded USD 拒絕，durable subscription stage 則還需核有效模型／帳戶／可用額度與成本範圍。未知文字費用不填零。
- 圖片「3 take」是目前批次／prompt set 的設定與授權範圍，CLI 實際接受 1–6、seed offset／prompt change／force 可建立新 set；不是每景終生三張的不可變 ledger 配額。現有 300 count 只能用於 frozen 這批，不能涵蓋任意新 prompt、人工重試與重抽。不得因此加買；若要機器保證該總量，需把整批 allowance 綁成跨新 set 的計數。
- lost answer／缺 usage 的支出保留 uncertain，speech journal 與 operation ID 防止自動再買；pilot media 一旦已 reserve，後續失敗也留 uncertain。只有能證實未收費的拒絕才釋放。重跑快取不是重買額度，逐階段釋放不是全片最壞保證。
- worker 可在 fitting／聽檢仍失敗時寫 `skipped.json` 放棄該語配音；all true 的語言選擇不是「一定交付八條配音」的保證。
- 配樂目前只報一首固定單位 0.08，request seconds 由真 timeline 算、夾在10–600秒；供應商可能回短音訊。已有曲目會保留，換 request／缺檔須先核對，不默默再買；story 短曲 loop 另有既定 owner 決定。沒有真 timeline／音檔時，不宣稱配樂時長或 loop 已驗收。

## 真正的規則與最小合法下一步

明文根據是 brand-story skill 預算列「一支整片上限 US$25；付費生成前把整批張數與總額一次報給站主、一次核准」，以及 `video_budget/PENDING_EVERYDAY.md` activation 前第1項「Reserve the worst payable amount for each TTS, ASR, Jev, image, music and text operation under one film ledger」。`service.reserve()` 只查目前帳本+下一筆，沒有 whole-film quote 資料模型、整批 future reserve sum 檢查，或把零餘額當成完成。報價／審核要求與 exact-slug activation 仍必須完整履行，沒有被本報告放寬。

1. 等站主已選 Claude 執行的**既有固定 old/new 唯讀 host probe**回傳真安全 JSON：確認部署 budget SHA／migration、原集歷史結案、精確新帳戶與 operations／餘額。尚未取得結果，不能假定 host 已連通、account 存在或可花。既有 probe 只解帳本部分，沒有供應商核價；不為了報價改它或重開登入。
2. 另取得最小 allowlisted 唯讀 runtime／supplier quote 資料：TTS default／explicit model、ASR `gemini_model`、圖片 judge `hotspot_guide_gemini_model`、Jev model、zh-TW retake allowance、後續 text stage provider/model/account/quota，以及對應計費身分／區域／帳戶價率／可用餘額與未明費用。只回非秘密必要摘要，不印 token 或完整設定，不透過一次 synthesis/transcription/judge/music 測價。
3. 以這份九軌 planner、100 景三 take、單首保留／loop 規則與明定重試，整理**精確新 slug、US25** 的可審全片 quote 及 protected activation 方案。若採順序 hard stop，必須誠實標明成片／八語完成仍有停線可能；不能把帳本安全等同完成保證。後續 activation 是另一個受審 code/account 步驟；本次不執行。
4. **只有若要求嚴格「最壞仍必完成」envelope**，現有功能不能憑短文本／真 WAV 自動縮 reserve，需要另一個受審 bounded-request 能力或可驗 supplier 對該 request 的封頂報價。設計須綁完整 prompt／metadata tokens、音訊與圖片 token 規則、provider-supported output/總thinking/audio限制、immutable 九軌清單與跨重試總 allowance、計費 account/model/rates/expiry/quote digest；驗出安全上界才 reserve。不能先把常數降低來 fit25，也不能先假定新界就會 ≤25。安全 fixture 可覆蓋長 alias/style、maxOutputTokens 缺失／不支援、candidate+thought 總量、>75s/非mono/錯格式 WAV、部分／全組 fallback、40/41 Jev分批、並發 reserve、uncertain/duplicate/overrun 與跨prompt三take計數；本次只列設計，未改code。

完整計算、30 檔程式 SHA、HTTP安全摘要 SHA、條件式與缺口在 [production-quote-gap-audit.json](production-quote-gap-audit.json)。原始小型 evidence 位於 `/workspace/work/brand-story-20261025/c03-audit/quote-gap/`；只讀 GET 與 planner 不等於主機、媒體或製片入場 PASS。
