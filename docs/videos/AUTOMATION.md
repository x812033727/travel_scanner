# 影片產線在主機上自動跑：設計

2026-09-25 定案。前提是 `docs/videos/DESIGN.md` 的產線（企劃 → 撰稿 → 查核 → 聽眾審稿 → 旁白 → 旁白檢查 → 畫面 → 成片 → 五語 CC → 送審）。原本整條由一個 Claude session 在站主的電腦上帶著代理跑；這份設計把它搬到正式站主機上，照後台的設定定時產生草稿。工作分成 5 張票，id 都是 `2026-09-25-video-auto-*`。

## 站主的決定

| 項目 | 決定 |
| --- | --- |
| 在哪裡跑 | 正式站主機 |
| 後台設定 | 各階段的 AI 模型、草稿排程與題材、成片參數、預算上限，都放在「影片審核」頁的「設定」分頁 |
| 關卡 | **旁白由 Jev 判斷，全數通過就自動核准**。2026-09-27 起（設計在 [`HANDS-OFF.md`](HANDS-OFF.md)）另外三關也由 AI 決定：**選大綱**由 Jev 依「頻道立場」挑（立場空白或開關關著時仍等站主；Jev 沒挑出過關的大綱就退回企劃模型重寫，兩次仍不過才交給站主，卡片附上 Jev 的表）、**看成片**由自動品管（`qa` 的 11 項全過就核准）、**確認上架**由上傳包檢查（4 項全過就核准，影片進「可以上架」）；站主只決定上架時間。仍然找站主的只有：品管或上傳包有項目沒過、Jev 兩次重寫仍不過、卡住的影片、上架時間 |
| 寫稿的模型 | **主機上登入的 Claude 訂閱帳號（Claude Code）**，預設 Claude Sonnet 5 寫、Claude Opus 5.5 查核。每個階段也可以改用網站的 API 金鑰 |
| 題目來源 | 先看站上已查證的新聞與已發布的文章，不夠再用 Brave 搜尋補 |

**訂閱帳號**：
- 站主先決定用 API 金鑰，後來改成用 `/admin/ai-accounts` 管的 Claude 訂閱帳號。之前提醒過：2026-09-24 的票（`tasks/done/2026-09-24-refresh-claude-plan-usage-automatically-from.md`）記錄，網站自己的功能放在個人訂閱上，可能違反 Anthropic 與 OpenAI 的消費者條款，而且額度用完就會整個停住。站主 2026-09-25 表示自己看過條款，決定用訂閱全自動。
- 額度那一點的處理：沒有用量上限（站主 2026-09-26 的決定）。帳號依 A、B、C… 的順序輪流，一個帳號的 5 小時或每週額度用滿才換下一個，最後一個用滿再回到 A。全部帳號都用滿就等額度重置，不會自己改用 API 金鑰。舊的「用到幾 % 就先停」欄位已拿掉，資料表欄位還在但不再讀取。
- **只提供 Claude Code**：`claude -p --tools ""` 可以關掉所有工具，只收文字、只回文字。`codex exec` 沒有關掉 shell 的開關，read-only 沙箱仍然讀得到這個服務能讀的所有檔案，包括網站的 `.env`；工人又會把網頁內容送進提示詞，所以 Codex 不提供。

## 架構

```
後台「影片審核 → 設定」──寫入──> video_automation_settings（一列）
                                      │
video-worker 容器（Node＋Chromium＋ffmpeg，compose profile video）
  每 5 分鐘：GET /video/automation/next ──> 這一輪該做什麼（新草稿？哪支影片的下一步？）
             漫劇（DRAMA-FLOW.md）：GET /video/automation/series/messages/next（討論）──> GET /video/automation/series/next（文件、下一集）
  文字階段 ──> POST /video/automation/run（伺服器照該階段的設定）
                 ├─ 訂閱：API ──HMAC──> 主機的 AI 帳號代理（ai_accounts_agent.runs）──> claude -p --tools ""
                 └─ API 金鑰：API 直接呼叫廠商（金鑰不出 API 容器）
  查核     ──> 工人自己抓 claims.md 列的網址（Mokaair-editorial UA），把頁面文字交給查核模型
  旁白     ──> 既有的 /video/speech、/video/speech/transcribe、/video/speech/judge
  畫面／成片／字幕 ──> 容器裡的 tools/video（render、assemble、captions）
  送審     ──> 既有的 /video/reviews（review-push）；站主在 /admin/videos 決定，工人 review-pull
```

- **工人是現在的本機工具搬進容器**。`tools/video` 的每個階段照舊，只是企劃、撰稿、查核、聽眾審稿、翻譯這些原本由代理做的步驟，改成呼叫 `/video/ai/run`，提示詞沿用 skill 裡的 `references/prompts/*.md`。站主的電腦上也能跑同一個指令（`node tools/video/cli.mjs auto`），方便除錯。
- **金鑰只在 API 容器**。工人只持有一組影片工具權杖，用既有的配對流程取得：工人第一次啟動時印出驗證碼，站主在後台按「允許」，權杖存在工人的 volume。
- **排程在工人裡**，不另開 scheduler 容器：工人每 5 分鐘問 API 下一步，API 依設定判斷，同一時間只做一件事。這跟新聞自動化的 60 秒迴圈同一個思路，但影片一輪要跑幾十分鐘，用單一工人就夠了。
- **工作區**是具名 volume `video_work`（取代本機的 `~/mokaair-work/videos`）。成片、音檔不進資料庫，送審時照舊上傳到 `video_reviews`。

## 設定（`video_automation_settings`）

2026-09-27 起設定分頁分成**教學影片**、**漫劇**、**共用**三個部分，各自儲存（[`DRAMA-FLOW.md`](DRAMA-FLOW.md) §一）；工人依影片的 `format` 讀教學或漫劇那一欄，漫劇的欄位是 `null`（模型、旁白聲音）或站還沒有時，就用教學的值。仍是一列。

| 群組 | 教學影片 | 漫劇 | 共用 |
| --- | --- | --- | --- |
| 開關 | `enabled`（自動產生草稿，預設關） | `drama_enabled`（接單集請求與作品，預設關） | — |
| 排程與題材 | 多久產生一次新草稿（72 小時）、每次幾個題目（1）、等站主的草稿達到幾支就先不產生（3）、題材範圍（AI、科技、AI 工具教學）、題目來源（站上新聞與文章／Brave 搜尋，都開） | 沒有排程：漫劇一律由站主發起；`drama_topic_scope`（山海經、民間傳說、原創玄幻）給企劃當原創題材的參考 | 要避開的題材（投資建議、醫療建議、選舉政治） |
| 各階段模型 | `stage_models`：企劃、撰稿、查核、聽眾審稿、字幕翻譯、字幕審稿各選「Claude Code（訂閱帳號）」或某家 API 的模型；預設全用訂閱帳號，企劃、撰稿、翻譯用 Claude Sonnet 5，查核、聽眾審稿、字幕審稿用 Claude Opus 5.5 | `drama_stage_models`：可勾「跟教學一樣」（存 `null`）；伺服器的 `stage_choice` 依 `/video/automation/run` 帶的 `format` 選 | 都在「AI 設定 › 各功能模型」選 |
| 各階段常設指示 | `stage_instructions`：六個階段各一段（每格最多 4000 字），工人接在該階段提示詞之後；清空就是不加 | `drama_stage_instructions`：同樣六格，只給漫劇（單集與作品的每一集）；遷移時從教學的複製一份 | 「目前的提示詞」依格式與 variant 分開顯示（`video_stage_prompts`） |
| 聲音 | `voice`：頻道聲音（Gemini Sulafat，沿用 `docs/videos/README.md`） | `drama_voice`：旁白，`null` 就跟教學一樣；角色聲音池 `character_voice_pool` | — |
| 長度 | 目標長度 8–12 分鐘 | 每個請求與作品各自帶 `target_minutes` | — |
| 語言預設 | `caption_locales`（en、ja、ko、zh-CN）：語言面板「照預設勾選」的預先勾選 | `drama_caption_locales`（預設空） | 工人不再讀這兩欄：每支影片做哪些語言由站主在成片核准後決定（[`LANGUAGES.md`](LANGUAGES.md)，下面「語言」） |
| 流程上限 | 每支最多查核幾輪（3）、旁白最多重錄幾輪（2） | `drama_max_verify_rounds`（3）、`drama_max_retake_rounds`（2）、每鏡最多重做幾次、一支最多幾段片段、文件退回後最多重寫幾輪 `series_doc_rewrites`（2；討論出的新版本不算） | — |
| 預算 | 每月最多幾支草稿（8） | 每月片段秒、圖片、judge 次數、音樂首數、單支美元上限、作品每月幾集 `series_episodes_per_month`、同時最多幾集在做 `series_max_in_flight`（1–2） | 每月模型 token 上限（百萬，只算 API 金鑰的呼叫，20）；旁白每月字數與 Jev 每日次數沿用既有欄位 |
| 關卡 | 旁白 Jev 全過自動核准、Jev 挑大綱、自動品管全過核准成片與上架確認（都開） | `drama_auto_approve_audio`、`drama_auto_approve_final`（遷移時從教學的複製）、設定圖自動選 `auto_pick_look`（關）、分鏡自動核准 `auto_approve_storyboard`（關）、「劇本先給我看」`series_script_gate`（開；單集與作品的每一集） | — |
| 頻道立場 | — | — | `channel_stance` |
| 目前的提示詞 | 教學的六個階段 | 漫劇的階段與 variant（`planner:setting`、`planner:bible`、`writer:episode`、`planner:discuss`、`writer:discuss`…），唯讀 | — |
| 用量 | 本月草稿數 | —（本月片段秒、圖片、judge、音樂、美元在 `media-status`／`GET /video/media/status`） | 本月 token（API 金鑰的對上限；訂閱帳號的另計）與呼叫次數 |

「訂閱帳號用到幾 % 就先停」欄位自 2026-09-26 起不再讀取（見上）。

超過任何一個預算時，工人停在目前的步驟，審核頁顯示原因，不會悄悄降級成較便宜的模型。

模型交不出能用的答案時：
- 原文會存到 `<工作區>/<slug>/answers/`，這一輪就結束，不會馬上重試。
- 同一個階段連續兩輪都失敗，這支影片就標成卡住，審核頁清單的第一項會寫出原因。
- 外部服務暫時失敗，例如旁白檢查或送審，同樣會結束這一輪，但不算進卡住的次數。

2026-09-25 曾經有一輪在兩分鐘內重問撰稿模型 6 次，花了約 10.6 萬 token，所以加上這條規則。

要讓工人整個停下來，在工作區放一個 `STOP` 檔：`docker compose -f docker-compose.prod.yml exec -T video-worker touch /var/lib/mokaair/video-work/STOP`。刪掉這個檔，下一輪就會繼續。

## 一支影片的自動流程

1. **選題**：從站上最近 14 天已發布的 AI／科技新聞與文章，加上 Brave 搜尋結果，排除已經做過的題目與避開的題材。由企劃模型挑出題目、寫 `brief.md`（含 2–3 個大綱與「站主觀點」；有頻道立場時第一行寫「套用立場：N、M」）→ 先問 Jev 挑哪一個（[`HANDS-OFF.md`](HANDS-OFF.md)）→ 送審「選大綱」。Jev 過關的伺服器直接核准；沒過就把原因交回企劃模型重寫，兩次仍不過、或立場空白，才**停下來等站主**。
2. **大綱選定**之後：撰稿 → lint（錯誤會把 lint 訊息餵回撰稿模型，最多改 3 次）→ 查核（改超過 3 個事實就再查一輪，每輪都是新的對話、看不到上一輪的結論，等於換人查；最多照設定的輪數）→ 聽眾審稿 → lint。
3. **旁白**：tts → check-audio → 被標的句子重錄，最多照設定的輪數。全數通過且設定開著，就自動核准旁白；否則送審等站主。
4. **成片**：render → assemble → captions（只有繁體中文）→ `qa`（11 項自動品管，字幕與標題說明兩項只看 zh-TW 加已選的語言）→ 送審「看成片」，報告一起送。全過的伺服器直接核准；有項目沒過才**停下來等站主**。翻譯不再擋成片：其他語言在成片核准後由站主決定（下面「語言」）。
5. **成片核准**之後：package（寫完就跑上傳包檢查，揭露答案寫進 `metadata.json`）→ 送審「確認上架」，附完整上傳包。4 項全過的伺服器直接核准。站主隨時可以在 Studio 上傳成私人、在後台貼上網址；影片要語言都做好才算「可以上架」、排程才會送出（[`LANGUAGES.md`](LANGUAGES.md) §上架流程）。工人下一輪把影片 id 寫進工作區的 `video.json`，影片就算完成。

站主退回時，退回的理由存在審核紀錄。工人會把它交給下一次撰稿或聽眾審稿的模型。

**放棄一支影片**：影片頁最下面有「放棄這支影片」，要寫原因，並再確認一次。
- 放棄之後，等站主決定的項目都會關掉，預覽檔會刪除，工具也不能再送審這支影片。
- 工人下一輪會把它標成「已放棄」，不再處理，它也不再佔「等站主的草稿」名額。
- 這支影片的題目仍算做過。
- 放棄不能復原。退回大綱的話，工人會用同一個代號重寫，所以題目本身不對時要用放棄，不要用退回。

**不重複選題**（2026-09-25 第一支自動草稿挑到第二批已經做好的題目之後加上）：
- 企劃模型會收到以下幾類影片，每支附上它改寫的站內文章（`source_guide`）：
  - `docs/videos` 裡的影片；
  - 工人自己做過的影片；
  - `/admin/videos` 上的每一支影片，包括分支上做的、已放棄的。
- 企劃的主要文章（`source_guide`，沒有的話取它引用的第一篇站內文章）如果跟前面任何一支相同，這份企劃就不採用。
- 分支上的影片用 `review-push --report-only` 登記到審核頁，這個指令不會送出任何審核項目。

## 漫劇（2026-09-26 加，設計在 `DRAMA.md`）

工人也會做 AI 漫劇。它不挑題：**站主在 `/admin/videos` 發起**（「新的漫劇」：故事前提或改編的文章、風格、長度；「新的作品」：前提、面向、集數）。漫劇設定（`?tab=settings&section=drama`）的 `drama_enabled` 要開著，否則表單被拒、工人也不問。語言與上架的順序在 [`LANGUAGES.md`](LANGUAGES.md)。

### 2026-09-27 起：單集與作品走同一條，一輪多一段「討論」

設計在 [`DRAMA-FLOW.md`](DRAMA-FLOW.md)。單集是一部 `kind = one-off`、只有一集的作品：「新的漫劇」送出時伺服器建作品（slug `one-off-<請求 id 前 8 碼>`）、第 1 集與指向它的請求列；文件只有一份故事聖經（`bible`），站主核准故事聖經而不是選大綱；每支漫劇都有劇本關卡；文件與劇本都可以討論。工人的一輪（`Automation.step()`）依序是：

1. 手上的影片：站主在 `/admin/videos` 放棄的、貼了 YouTube 網址的，然後每支 `active` 影片推進一步（`advance`）或做它的語言。
2. **討論**（`discussStep()`，在任何作品工作之前，一輪最多回一則）：`GET /video/automation/series/messages/next` 拿最舊的未回覆站主訊息，連同整條串、文件最新版（劇本串給那一集，劇本由工人從自己的檔案讀）與作品脈絡；文件交給企劃模型（variant `discuss`）、劇本交給撰稿模型（variant `discuss`），答案 `{ reply, revised }`，`POST /video/automation/series/messages/{id}/answer {reply_md, revised?}`。文件的新版本由站上存成等站主的 `review` 版本（被取代的那版備註「討論後出了新版本」，不算 `series_doc_rewrites`，也不算每月草稿）；劇本的新版本由工人寫回 `video.json`（每句 id 保留、過 lint），之後的輪次重跑查核與聽眾審稿、重寫 `script.md`、再送一次劇本關卡。模型給不出可用答案就代它回一則說明，串停著等站主，不重試。沒有輪數上限；要停就關 `drama_enabled` 或放 `STOP` 檔。
3. **作品**（`seriesStep()`）：`GET /video/automation/series/next`——`bible`（單集）或 `setting`／`outline`／`chapter`（作品）由企劃模型寫文件 `POST …/series/{slug}/docs` 等站主；`episode` 就 `POST …/episodes/{n}/start` 開下一集（單集是 `one-off-<…>-e001`），寫 `series.json` 與 `brief.md`（`## 大綱` 只有選項 A，本機核准，備註「依故事聖經」或 `planned by chapter <n>'s approved outline`），不送「選大綱」。
4. 舊的單集請求（`GET /video/automation/drama-requests/next` 只回單集變成作品之前排進、沒有 `series_id` 的請求），照下面的舊路。
5. 排程的教學草稿。

每一集的步驟是 `DRAMA_STEPS` 的 19 步（`status` 會印）：撰稿 → 連貫性查核 → 聽眾審稿 → **劇本關卡**（`script.md` 只含敘事；`review-push --gate script`，站主在影片頁讀、討論、核准；「劇本先給我看」`series_script_gate` 關著就本機核准；退回走撰稿 FIX 模式最多 `MAX_PROMPT_FIX_ROUNDS` 輪）→ **look**（judge 打分，`auto_pick_look` 開著就核准 judge 建議的那張，沒過才找站主）→ tts → check-audio → 旁白關卡（Jev 全過自動核准）→ **keyframes** → storyboard 關卡（`auto_approve_storyboard`）→ render → **clips**（最貴，送出前對單支上限把關）→ music → assemble → 繁中字幕 → 成片關卡（自動品管）→ package → 上架確認（`POST …/episodes/{n}/done`）→ 語言。劇本關卡在任何圖片或片段花錢之前。

### 舊路：單集變成作品之前排進的請求

工人每輪在做排程草稿之前問 `GET /video/automation/drama-requests/next`，有就用 `planner-drama.md` 寫 `brief.md`（含大綱選項）、`POST …/{id}/start` 認領（寫下影片代號），然後照投影片的規矩送審「選大綱」。只有規劃這一段不同：大綱選定、lint 之後的步驟同上（`DRAMA_STEPS` 的 19 步）；上架確認後工人 `POST …/{id}/done`。

三種失敗各有處理：

- **品檢沒過（結束碼 1）**：`look`／`keyframes`／`clips` 把沒過的角色或鏡頭連 judge 的評語留在 manifest（`needs_review`），工人交給撰稿模型的 FIX 模式改提示詞（只改那幾個 id），下一輪重跑該階段；每種最多 2 輪，之後卡住並在審核頁寫原因。站主退回 look 或 storyboard 時也走同一條，退回的話一起交給模型。
- **要站主（結束碼 3）**：單支上限、漫劇沒開、沒金鑰、關卡沒核准——卡住，理由寫在審核頁的清單第一列。
- **供應商或額度（結束碼 4）**：這一輪結束，下一輪再試；每月預算由伺服器以 429 擋，請求不會送到供應商。

`settle()` 依設定寫進 `video.json`：`format: "drama"`、`look.preset`（模型沒寫時用設定的風格預設）、`subtitles.burn_in`、關掉音樂時拿掉 `music`。工人回報影片時帶 `format`，後台列表才分得出漫劇並顯示 `media_usd`。

## 長篇作品（2026-09-27 加，設計在 `SERIES.md`）

工人每輪先回一則討論（上面「討論」，`GET /video/automation/series/messages/next`），再問 `GET /video/automation/series/next`（單集的故事聖經與第 1 集也從這裡來），再問舊的單集請求，再看排程草稿。作品層的工作是 `setting`／`outline`／`chapter`／`episode`，單集只有 `bible` 與 `episode`：`setting`／`outline`／`chapter` 是企劃模型（variant `setting`、`outline`、`chapter`）寫一份文件送到站上等站主；`episode` 是在站上開始下一集（影片 slug 為 `<作品>-e001` 這種），工人寫 `docs/videos/<slug>/series.json`（人物表、本集細綱、前情、謎團、設定集全文）與 `brief.md`（只有選項 A，本機直接核准），之後照上面每一集的 19 步走（劇本關卡每支漫劇都有），作品的集只多兩件事：撰稿與查核用作品變體（`writer:episode`、`verifier:episode`，查核另輸出 `coverage` 與 `problems` 到 `review/script-check.json`）；`look` 先查作品存檔 `<VIDEO_WORKDIR>/_series/<作品>/characters/`，有核准過的設定圖就沿用並直接核准 look，只畫新角色（`review-pull` 核准 look 時把選中的圖存進去）。合成完成後查核模型（variant `recap`）寫 150 字前情 `POST …/recap`；上架確認後 `POST …/done`，站上依 `series_max_in_flight`、`series_auto_continue` 與前一集是否完成決定下一集何時開始。文件被退回帶 `previous` 與 `owner_note` 重寫，站上限制 `series_doc_rewrites` 輪；討論出的新版本另計，沒有上限。

## 品牌故事（2026-09-28 加，設計在 `STORY.md`）

品牌故事是 12–15 分鐘、只有旁白、約 90 張卡通靜態圖的非虛構短片，影片是漫劇，100 個故事是一部 `kind: "story"` 作品的 100 集（`hands_off`、`visual_tier: "stills"`）。企劃清單事先查核、由站主匯入，工人從 `GET /video/automation/series/next` 拿到 `kind: "episode"` 的工作，集數的 `beats` 就是整份企劃。實作在 `tools/video/automation/story.mjs`，操作步驟在 skill 的 `references/story.md`。

一集的做法跟漫劇的集只差在稿子怎麼來：

1. **開始**：用企劃定好的 `slug` 呼叫 `POST …/episodes/{n}/start`（別的代號伺服器回 409），寫 `series.json`（`kind: "story"`、`names`、人物、畫風、圖片模型、企劃）與 `brief.md`，大綱在本機核准。沒有模型呼叫。
2. **一步最多一次模型呼叫**，每一次都帶 variant，不算進每月排程草稿：撰稿一章一次（`writer:story`，六章存在工作區的 `story/chapters/`，六章齊了合併成 `video.json`、`claims.md` 並 lint，錯誤落在哪一章就退回那一章）→ 查核一章一次（`verifier:story`，新 session，回句子 patch 與那一章的主張表，不回整份稿）→ 聽眾審稿一章一次（`listener:story`，只回 patch）。正常一支 18 次呼叫；量過最大的一次請求約 71 KB，一章的回答不到 10,000 字，都在轉送的 295 秒與輸出上限之內。
3. **查核照企劃**：企劃的事實是查核過的，查核模型確認稿子說的跟企劃一樣，只在頁面裡找撰稿模型自己加的數字、年份、人名；`attributed` 的要說是誰的說法，`reviewer_only` 的照企劃的寫法、不去找頁面，`caveats` 照辦。工人讀整頁文字（`pageReader({ whole: true })`，其他呼叫者不變），用那一章的數字、年份（含昭和、平成、令和、民國）與名字切出段落交給模型，讀不到的 PDF 交企劃的 `supports`，並註明不是這次讀的。
4. **劇本關卡在本機核准**，備註寫原因；故事不寫前情、不做合集、不送劇本關卡。之後照漫劇的步驟：有企劃人物才有 `look`，`tts` 之後先量長度（13 分鐘要在 11:30–15:30，否則撰稿模型砍最長的一章或補最瘦的一章，最多兩輪；段落沒有更多可講就卡住給站主決定，不塞內容），再 `check-audio`、`keyframes`、分鏡（伺服器依 judge 決定）、`render`、`clips`（全靜態圖只寫 manifest）、`music`、`assemble`、字幕、成片、上傳包、上架確認（`POST …/done`）。
5. **圖片**：提示詞不得出現企劃 `names` 裡的名字、商標、文字或真人長相，lint 擋；沒過 judge 的鏡頭只把那幾鏡交給撰稿模型修（`writer:story-fix`），修正也先 lint 才保存。

站主在影片頁退回旁白並寫原因時，聽眾審稿帶著那句話把六章再聽一次；在故事的劇本討論串留言，工人回一則說明（故事的稿子不從討論串整份重寫）。漫劇設定的「各階段常設指示」也會接在故事的提示詞後面。

## 語言（2026-09-27 加，設計在 `LANGUAGES.md`）

每支影片先只做繁體中文。成片核准後站主在 `/admin/videos` 的影片頁決定加哪些語言（en、ja、ko、zh-CN）、每種加什麼（標題與說明、CC、配音），或按「只出繁體中文」；`caption_locales` 只是面板的預先勾選。工人每一輪從影片清單（`ProjectSummary.locales`、`locales_decided_at`、`languages`）看每支成片已核准的影片：沒決定就什麼都不做；決定了，就把選擇抄成工作區的 `languages.json`（`captions`、`package`、`qa`、`review-push` 都從這個檔讀，本機手動跑也一樣），再對站上還標成「製作中」的部件做一件事：

1. **翻譯**（一輪一個語言）：`i18n-sheet --locale <l> --parts <勾了的 metadata,captions>`（勾配音時每句帶 `max_chars`）→ 翻譯模型 → 字幕審稿模型 → `i18n-merge`。工作表沒有勾的部件就沒有那一段，merge 也不動它。
2. **配音**（一輪一個語言，`docs/videos/DUBS.md`）：`dub --locale <l>`；結束碼 1（有視窗加速到 1.15 倍仍塞不下）→ 翻譯模型的縮短模式（`translator:shorten`，只給 `fit.json` 的句子與預算；不縮短或改了數字的答案丟掉）→ captions-only 的工作表 → `i18n-merge` → 再 `dub`，最多 `MAX_DUB_SHORTEN_ROUNDS`（2）輪；做出音軌後 `check-audio --locale <l>` → 被標的句子 `dub --redo`，最多 `MAX_DUB_RETAKE_ROUNDS`（2）輪；重錄後句子變長、塞不回視窗時，回到縮短模式，不直接放棄。重錄完仍被標的句子多半是同音字（轉寫每次都聽成同一個詞，2026-09-29 當天 8 條配音都因此整條放棄），交給翻譯模型的改寫模式（`translator:reword`，帶轉寫聽到的字與預算；沒改、超過預算或改了數字的答案丟掉）→ 同樣走工作表與 `i18n-merge` → 再 `dub`（只重錄改過的句子）與 `check-audio`，最多 `MAX_DUB_REWORD_ROUNDS`（2）輪。仍不行、或 `dub` 說要站主（Azure 聲音、沒金鑰）就寫 `dubs/<l>/skipped.json` 記下原因，**不擋影片**；服務暫時掛掉（結束碼 4）這一輪結束、下一輪再試。
3. **全部做好**：`captions`（只寫 zh-TW 與勾了 CC 的語系；有配音的跟配音時間軸；沒勾的語系的字幕檔刪掉）→ `package`（`upload/` 只放 zh-TW 與勾了的：`description.<l>.txt`、`captions/<l>.srt`、`dubs/<l>.m4a`；`metadata.json` 多 `language_choice`）→ `review-push --gate languages`：payload 每語每部件 `ready` 或 `{status: "skipped", reason}`，檔案 `description_<l>`、`captions_<l>`、`dub_<l>`（語系小寫、連字號改底線）。沒有配音的批次伺服器直接核准；有配音的等站主在 Studio 上傳後按「已在 Studio 上傳配音」。

之後多勾的部件，站上會再標成「製作中」，工人再做一批、再送一筆（舊的 superseded）；影片已經在 YouTube 上也一樣。站主沒勾或只出繁體中文的影片，`captions` 與 `package` 只有 zh-TW，其他檔案一個位元組都不變。

成本：翻譯每個語言一次翻譯加一次審稿呼叫；配音見 `DUBS.md` §成本（一條 10 分鐘約 US$0.135，月額度 `video_speech_gemini_monthly_character_limit` 要先調高）；YouTube 配額見 `LANGUAGES.md` §成本。

## 一鍵合集（2026-09-27 加，設計在 `BINGE.md`）

作品有 `hands_off`、`compilation`、`genre`、`visual_tier` 時（後台的「一鍵開拍」全部帶上），工人在作品模式多做三件事：

1. **判文件**：企劃寫完設定集、總綱或細綱後，先由查核模型在新 session 出裁決（variant `verifier:series-doc`：每個必要項目「有／弱／無」、`problems`、`similar_works`），連同文件 `POST …/series/{slug}/docs`（`judge` 欄位）；伺服器依 `series_doc_passed` 當場核准（備註「查核：…，依作品設定自動核准」）或退回重寫（備註「[auto] 查核沒過：…」，既有的 `series_doc_rewrites` 循環接手），重寫用完才停在待審。裁決拿不到就不帶 `judge` 送件，文件照舊等站主。有節奏規格的題材，細綱每集還要有 `hook_type`、`lead_arc`、至少 2 個 `satisfaction`，工人與伺服器都檢查（`retentionProblem`／`_retention_problem`）。
2. **劇本本機裁決**：查核（`verifier:episode`）多回 `coverage.satisfaction` 與 `retention` 指名的句子 id，工人用估計時間軸算秒數（`retentionNumbers`），再用與伺服器同一套規則自己判一次（`scriptVerdict`：四個節拍沒有「無」、「弱」≤ 1、沒有連貫性與雷同問題、鉤子 ≤ 8 秒、第一個爽點 ≤ 30 秒、爽點 ≥ 2、懸念是最後一句）；不過就交撰稿 FIX 模式（最多 `MAX_PROMPT_FIX_ROUNDS` 輪）再查核、再聽眾審稿，過了才 `review-push --gate script`，伺服器依 `script_check_passed` 當場核准。設定圖與分鏡在免關卡作品上視為自動開關開著。每集的 `series.json` 帶 `visual_tier` 與 `compilation`：lint 擋超過等級上限的片段數，合集模式的第一個場景不能是片頭卡；`clips` 只買 `visual: "clip"` 的鏡頭，`assemble` 把 `still` 鏡頭的關鍵影格做成運鏡段。
3. **合集**：全部集數完成後 `GET …/series/next` 回 `{kind: "compilation"}`，工人 `POST …/series/{slug}/compilation/start`（`{slug: "<作品>-full"}`）拿到每集與脈絡，建 `docs/videos/<作品>-full/video.json`（`compilation` 區塊、章節卡、outro、佔位標題）與 `compilation.json`，之後照 `COMPILATION_STEPS` 走：企劃寫標題／說明／標籤／縮圖（variant `planner:compilation`，縮圖底圖從前三集的關鍵影格挑一張複製到 `keyframes/thumb-source.png`）→ `render` 章節卡與縮圖 → `compile`（`-c copy` 串接每集成片、音訊重編一次、合併五語字幕、寫章節；結束碼 4 下一輪再試，其餘非 0 卡住）→ 翻譯四語標題與說明（variant `translator:compilation`）→ `qa`（6 項）→ 成片與上架確認照 HANDS-OFF 自動核准 → 站主貼網址後 `POST …/compilation/done`。合集的 1080p 成片不進審核檔案區（只送 720p 預覽），站主從後台下載。

## 清理工作區（2026-09-28 加）

工作區（volume `video_work`）原本什麼都不刪，一支品牌故事就留下 1.3–2 GB（`STORY.md` §上限與成本）。工人每一輪做完手上的工作之後清一次（`tools/video/automation/tidy.mjs`）：

- **哪些影片**：`auto.json` 說已經結束的——`status: done` 而且記下了 YouTube id，或站主放棄（`dropped`）——而且結束滿保留天數（預設 7 天，跟審核檔案區刪 mp4 的 `PREVIEW_RETENTION` 一樣）。
- **從哪天算**：放棄的從 `dropped.at` 算。上了 YouTube 的，`auto.json` 沒有記日期（`recordVideoId` 只寫 `status` 與 `youtube_video_id`），所以照網站刪 mp4 的規則（`prune_published_previews`）：上架確認核准的時間（工作區 `approvals.json` 的 `publish` 項，與每輪影片清單的 `publish_approved_at`，取較晚的）和站主設的公開時間（`youtube_publish_at`），再取較晚的。沒有可用的日期就不清，那一輪印一行說明。
- **先留著**：還在做、卡住、等站主的影片，不管多舊都不動。已上 YouTube 但語言還沒決定或還在做（影片清單的 `locales_decided_at`、`languages`）、開了合集的作品裡合集還沒上 YouTube 的集數（合集要接每一集的成片與字幕，縮圖取前三集的關鍵影格）、工作區裡有 `STOP` 檔的，也先留著。
- **刪什麼**：`final.mp4`、`upload/final.mp4`（上傳包的副本；合集是硬連結）、`upload/dubs/`、`segments/`、`build/`、`audio/`、`narration.wav`、`frames/`、`keyframes/`、`clips/`、品牌故事讀過的來源頁面 `story/pages/`（整頁文字，一頁一個 JSON）、配音的 `dubs/<語系>/audio/`、`dubs/<語系>/narration.wav`、`dubs/<語系>.<格式>`，以及 `review/` 裡送審用的預覽（`preview-<雜湊>.mp4`、`narration-<雜湊>.m4a`）。
- **一定留**：`auto.json`、`state.json`、`checks.json`、`approvals.json`、`timeline.json`、`captions/`、`i18n/`、`languages.json`、`media/`（帳本、快取、工作）、`answers/`、`review/` 的 JSON 與頁面、上傳包的文字檔（`metadata.json`、`UPLOAD.md`、說明、字幕）與縮圖、`characters/`、`music/`、`thumbnail.jpg`、`contact-sheet.png`、品牌故事的 `story/chapters/`（每一章的稿子與查核結果，很小，出問題時要看）。工作區根目錄的 `_series/`、`_music/` 與任何 `_` 開頭的資料夾從不讀、從不刪。
- **拒絕**：工作區根目錄是空白、相對路徑、磁碟根目錄、在 repo 裡或包住 repo，整個不跑。要刪的路徑一定在那支影片自己的資料夾裡，而那個資料夾直接在工作區根目錄底下。路上遇到連結（symbolic link、Windows junction）就不穿過；連結本身當成一個名字刪掉，它指到的東西不動。
- **一輪一支**，最早結束的先清。印一行：哪一支、刪了什麼、釋放多少位元組。刪不掉的檔案（Windows 上被鎖住）與已經不見的，列在同一行，這一輪照常結束。清完在 `auto.json` 原子寫入 `tidied_at` 與 `tidied`（刪了什麼、多少位元組、哪些刪不掉），之後不再看這一支。
- **什麼時候跑**：每一輪 `auto` 在工作之後跑一次，不管這一輪有沒有進度；設定裡自動草稿關著、或找到 `STOP` 檔，就不跑。
- **清完之後**：`status` 不再寫「Next: …assemble」，改寫檔案哪天清掉、上面讀那些檔案的步驟會顯示沒做完、不會再做。工人也不會重做：`done` 的影片不再 `advance`，語言那一步看到 `auto.json` 的 `tidied_at` 就不翻譯、不配音、不打包（見下一段）。

只在工人設定，網站（API、資料庫、後台設定）不用改：

| 環境變數 | 預設 | 意思 |
| --- | --- | --- |
| `VIDEO_TIDY_DAYS` | `7` | 結束幾天後清，1–3650；`off` 關掉。填錯（例如 `7d`）時那一輪不清，印一行說明 |

工人容器只收 compose 列出的環境變數：在 `docker-compose.prod.yml` 的 `video-worker.environment` 加一行，重建工人容器就生效。

手動跑：`node tools/video/cli.mjs tidy --dry-run` 列出下一輪會清哪一支、刪什麼、多少位元組，以及哪些影片還在等、為什麼留著；不加 `--dry-run` 就真的清一支。它要讀站上的影片清單，所以要先 `login`。主機上是 `docker compose -f docker-compose.prod.yml exec -T video-worker node tools/video/cli.mjs tidy --dry-run`。

清完之後就做不到的事：

- 清理之後才勾的語言做不出來（成片與旁白都不在了，`package` 也要 `final.mp4`）。工人下一輪把每個還在「製作中」的部件送成一筆 `languages` 審核，部件是 `{status: "skipped", reason: "工作檔已在 <日期> 清掉，…"}`（跟放棄的配音 `dubs/<語系>/skipped.json` 同一種回報），沒有音軌所以伺服器直接核准；語言面板那一格顯示「跳過」與原因，卡片不再停在「語言製作中」。這一筆只列新勾的部件，清理前做好的照舊。
- 合集的 1080p 成片（`upload/final.mp4`）在上 YouTube 滿保留天數後一起清掉，後台的下載按鈕就沒有檔案可下載——跟審核檔案區刪 mp4 的規則一致。
- 從長片關鍵影格剪 Shorts（`shorts/cli.mjs from-episode`，#904）要在長片清掉之前做。

## 安全與成本

- `/video/automation/run` 只接受設定裡列出的階段名稱，模型由伺服器依設定決定，工人不能指定。每次呼叫都記下階段、模型、token 數與影片代號。上限有兩個，超過都回 429：
  - 每月 token 上限，只算 API 金鑰的呼叫；
  - 每月草稿數，訂閱與 API 都算。
- 訂閱帳號的執行一律經過主機的 AI 帳號代理，帶 HMAC 簽章，走 Unix socket。
  - 代理用 `--tools ""` 關掉所有工具，也不載入任何 MCP、不留 session。
  - 執行環境從零建立，帶不到代理的金鑰；工作資料夾用完就刪。
  - 同一時間只跑一個。
  - 工人容器碰不到帳號的登入憑證。
- 工人抓網頁只用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 當 User-Agent，每個網域間隔至少 1 秒，不登入任何網站。
- 工人容器照其他服務的加固方式：`cap_drop: ALL`、`no-new-privileges`、非 root 使用者、唯讀根目錄加上工作區 volume。
- 模型費用粗估：一支影片大約 40 萬輸入、10 萬輸出 token（企劃、撰稿、兩輪查核、聽眾審稿、四語翻譯與審稿）。實際數字在第一支自動影片之後記進這份文件。

## 分期與票

| 票 | 內容 | scope |
| --- | --- | --- |
| `video-auto-settings` | 設定表（遷移）、後台 API、工具讀取端點、「設定」分頁、旁白自動核准的規則 | `apps/api/app/video_automation`、遷移、`apps/web` 的影片審核元件與 admin.json |
| `video-auto-model-runner` | `/video/ai/run`、用量紀錄與每月上限、`/video/automation/topics`（站上新聞與文章＋Brave） | `apps/api/app/video_automation` 的 ai 與 topics 模組 |
| `video-auto-orchestrator` | `tools/video/automation`：自動流程的狀態機、呼叫模型、抓查核網頁、`auto` 指令 | `tools/video/automation`、`tools/video/cli.mjs` |
| `video-auto-worker-image` | 工人映像（Node＋Chromium＋ffmpeg＋字型）、compose 服務與 volume、工人迴圈 | `ops/video`、`docker-compose.prod.yml` |
| `video-auto-rollout` | 部署腳本加 `--profile video`（要站主同意）、配對工人、開啟設定、跑第一支 | 主機；repo 只改文件 |

前兩張依序做（都會改 `apps/api/app/models.py` 並各帶一個遷移）；第三張靠前兩張的端點；第四張可以和第三張同時做。
