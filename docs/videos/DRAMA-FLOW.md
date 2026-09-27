# 漫劇與教學分開：設定分頁、一條漫劇流程、劇本討論（設計）

2026-09-27 起草。前提是 [`DRAMA.md`](DRAMA.md)（單集漫劇）、[`SERIES.md`](SERIES.md)（長篇作品）、[`HANDS-OFF.md`](HANDS-OFF.md)（站主只決定上架時間）與 [`AUTOMATION.md`](AUTOMATION.md)（主機工人）。這份寫三件事：後台「影片審核」的設定分頁怎麼把**教學影片**與**漫劇**分開；漫劇從想法到上架只走**一條**流程，單集與作品的關卡一樣；站主怎麼跟模型**討論**設定集、細綱與劇本，而不是只能「退回＋備註」。語言（標題說明、CC、配音）與上架的順序另寫在 [`LANGUAGES.md`](LANGUAGES.md)。票的 id 是 `2026-09-27-video-split-*`（設定）與 `2026-09-27-video-drama-room-*`（流程與討論）。

## 站主的要求（2026-09-27）與這份的解讀

| 站主說的 | 這份怎麼做 |
| --- | --- |
| 影片審核的漫劇跟教學設定應該也要分開 | 設定分頁拆成三個子分頁：**教學影片**、**漫劇**、**共用**。每個子分頁各自儲存；會因格式而不同的欄位（常設指示、旁白聲音、語言預設、查核與重錄輪數、旁白與成片的自動核准、各階段模型）漫劇有自己的一份 |
| 整個順一下漫劇的製作流程 | 單集與作品走同一條：**文件 → 劇本 → 製作 → 語言 → 上架**。單集就是「一集的作品」，文件只有一份「故事聖經」；「選大綱」的 A／B／C 卡片只留給教學影片 |
| 討論劇本跟製作劇本的方式 | 每份文件與每集劇本都有一條**討論串**：站主寫一句話（問題、想法、要改什麼），工人下一輪讓企劃或撰稿模型回覆，要改就出新版本；站主滿意了才核准。「製作劇本」是核准的文件變成 `video.json` 與 `script.md`，站主在劇本關卡再讀一次（也可以繼續討論） |

其餘照 HANDS-OFF：核准之後的設定圖、旁白、分鏡、成片都由 AI 或 Jev 決定，站主只在出錯時被找。

## 一、設定分開

### 現況

`/admin/videos?tab=settings` 是一張表單：教學的排程與題材在最上面，漫劇是最下面一節，中間的「各階段常設指示」寫著「投影片與漫劇每一支都適用」，旁白聲音、字幕語系、查核輪數、旁白與成片的自動核准都只有一份，儲存鈕一按整張表單一起送。想給漫劇不一樣的旁白、不一樣的常設指示（例如「結尾留懸念」只該給漫劇）做不到；改教學的排程也會把漫劇的欄位一起重送。

### 之後：三個子分頁，各自儲存

`?tab=settings&section=tutorial|drama|shared`，預設 `tutorial`。每個子分頁一顆儲存鈕，只送自己的欄位（`SettingsSave` 改成每個欄位都可省略，省略就是不改）。

| 群組 | 教學影片 | 漫劇 | 共用 |
| --- | --- | --- | --- |
| 開關 | `enabled`（自動產生草稿） | `drama_enabled`（接單集請求與作品） | — |
| 排程與題材 | `draft_interval_hours`、`topics_per_run`、`max_waiting_drafts`、`topic_scope`、`topic_from_site`、`topic_from_search` | 沒有排程：漫劇一律由站主發起。`drama_topic_scope` 給企劃當原創題材的參考 | `topic_avoid`（兩種都要避開的題材） |
| 各階段模型 | `stage_models`（在 AI 設定頁選） | `drama_stage_models`，可勾「跟教學一樣」（存 `null`） | AI 設定頁的連結 |
| 常設指示 | `stage_instructions` | `drama_stage_instructions` | — |
| 聲音 | `voice`（頻道聲音） | `drama_voice`（旁白；`null` 就跟教學一樣）＋ `character_voice_pool`（角色） | — |
| 長度 | `target_minutes_min`／`max` | 每個請求與作品各自帶 `target_minutes`，不在設定裡 | — |
| 語言預設 | `caption_locales` → 改名顯示為「語言面板預先勾選」（[`LANGUAGES.md`](LANGUAGES.md)） | `drama_caption_locales`（預設空：漫劇燒錄繁中字幕） | — |
| 流程上限 | `max_verify_rounds`、`max_retake_rounds` | `drama_max_verify_rounds`、`drama_max_retake_rounds`、`max_retakes_per_shot`、`max_clips_per_video`、`series_doc_rewrites` | — |
| 預算 | `max_drafts_per_month` | 媒體的四個月預算、`max_usd_per_video`、`series_episodes_per_month`、`series_max_in_flight` | `monthly_token_budget_millions`（模型 token 是同一個帳） |
| 關卡 | `auto_approve_audio`、`auto_pick_outline`、`auto_approve_final` | `drama_auto_approve_audio`、`drama_auto_approve_final`、`auto_pick_look`、`auto_approve_storyboard`、`series_script_gate` → 顯示為「劇本先給我看」，單集與作品都適用 | — |
| 頻道立場 | — | — | `channel_stance` |
| 目前的提示詞 | 教學的六個階段 | 漫劇的階段與 variant（`planner:setting`、`writer:episode`、`planner:discuss`…） | — |
| 用量 | 本月草稿數 | 本月片段秒、圖片、judge、音樂、美元 | 本月 token（API 與訂閱） |

漫劇的媒體模型、片段規格、風格預設、角色聲音池、切換開關照舊，只是搬進漫劇子分頁。

### 資料模型

`video_automation_settings` 仍是一列，新欄位接在 `0101` 之後的遷移（開工時再查 main 的 head）：

| 欄位 | 型別與預設 | 說明 |
| --- | --- | --- |
| `drama_stage_models` | JSON，`NULL` | `null` ＝ 跟教學一樣；有值時六個階段都要有 |
| `drama_stage_instructions` | JSON，`'{}'` | 遷移時複製 `stage_instructions`，部署後行為不變 |
| `drama_voice` | JSON，`NULL` | `null` ＝ 跟教學一樣 |
| `drama_caption_locales` | JSON，`'[]'` | 語言面板的預先勾選 |
| `drama_auto_approve_audio`、`drama_auto_approve_final` | bool | 遷移時複製教學的值 |
| `drama_max_verify_rounds`、`drama_max_retake_rounds` | int，3、2 | 同教學的上下限 |

這些都放進既有的 `DramaSettings` 巢狀物件（`settings.py` 的 `_flat` 會把它們攤到欄位上，欄名就是欄位名，和 `drama_enabled`、`drama_aspect` 一樣）。伺服器端讀取的地方改成依格式選：`ai.stage_choice(row, stage, format)`（`StageRunIn` 已帶 `format`）、`auto_approves_audio`／`auto_approves_final` 依 `video_projects.format`。`ToolSettingsView` 帶出全部新欄位。

工人（`tools/video/automation/flow.mjs`）依 `state.format` 取值：`instructionsFor` 的 standing、`settle()` 寫進 `video.json` 的旁白 `voice`、查核與重錄的輪數、語言預設。教學影片一個位元組都不變。

### 後台

- `admin-video-settings.tsx` 拆成殼（子分頁、載入、共用區）與 `admin-video-settings-tutorial.tsx`、`admin-video-settings-drama.tsx`；各自的 `saveBody` 只含自己的欄位。
- AI 設定頁（`admin-video-model-settings.tsx`）多一塊「漫劇各階段」：一個「跟教學一樣」勾選（存 `null`）與六個階段的選單。
- 「新的漫劇」「新的作品」的說明文字「設定分頁要先開啟『AI 漫劇』」改成「漫劇設定要先開啟」，並連到 `?tab=settings&section=drama`。
- 五個語系的 `admin.json` 都要有字串；`npm run check:i18n`。

## 二、一條漫劇流程

### 現況

| | 單集（`video_drama_requests`） | 作品的一集（`SERIES.md`） |
| --- | --- | --- |
| 站主給的 | 前提、風格、長度、備註 | 前提、面向、情感線、集數 |
| 文件 | 沒有：企劃寫 `brief.md`，站主在「選大綱」卡片選 A／B／C | 設定集、總綱、篇章細綱，各自核准／退回／自己改 |
| 劇本 | **沒有關卡**：大綱選完直接到設定圖 | 劇本關卡（核准或退回） |
| 退回 | 企劃重寫最多 2 次，之後卡住 | 文件重寫 `series_doc_rewrites` 輪，之後停在待審；劇本 FIX 最多 `MAX_PROMPT_FIX_ROUNDS` 輪 |
| 討論 | 只能退回＋備註 | 只能退回＋備註 |

兩條路的關卡不一樣、頁面不一樣，而且單集沒有劇本關卡：站主第一次看到台詞是在聽旁白的時候，設定圖的錢已經花了。

### 之後：單集就是一集的作品

```
站主發起（單集：前提；作品：前提、面向、集數）
  → 文件（討論／自己改／核准）
      單集：一份「故事聖經」（前提、角色、幕、一個大綱、素材、不做的事）
      作品：設定集 → 總綱 → 每篇細綱（不變）
  → 製作劇本：撰稿 → 連貫性查核 → 聽眾審稿 → 【劇本關卡：討論／核准】
  → 製作（全自動）：設定圖（judge 選）→ 旁白（Jev）→ 關鍵影格 → 分鏡（judge）→ 片段 → 配樂 → 合成 → 繁中字幕 → 成片（自動品管）→ 上傳包
  → 語言（站主選；LANGUAGES.md）→ 上架時間（站主）
```

- `video_drama_series.kind`：`series`｜`one-off`。「新的漫劇」表單留著，但送出時建立一部 `one-off` 作品（`planned_episodes = 1`、`episodes_per_chapter = 1`，兩個 CHECK 放寬到 ≥ 1；slug 由站主填或自動 `one-off-<日期>`），文件只有一份 `bible`（`DOC_KINDS` 加 `bible`）。核准後第 1 集自動開始，之後跟作品的一集完全一樣。`video_drama_requests` 留著當運送用的列（它已經有 `series_id`、`episode_number`）。
- 漫劇不再用「選大綱」卡片。`brief.md` 仍由工人從核准的文件寫出（`## 大綱` 只有選項 A，本機直接核准，備註「依故事聖經／第 k 篇細綱」），撰稿模型讀的東西不變。Jev 挑大綱與 `auto_pick_outline` 只管教學影片。
- 劇本關卡對**每一支**漫劇都開（`stepsFor` 拿掉 `|| doc.series` 的條件；`series_script_gate` 顯示為「劇本先給我看」，關掉就自動核准）。劇本關卡在任何圖片或片段花錢之前。
- 之後的製作照 HANDS-OFF：`auto_pick_look`、`auto_approve_storyboard` 由站主看過第一支之後打開；旁白 Jev 全過自動核准；成片自動品管。站主被找的只有出錯的項目。
- 遷移把還在 `queued` 的單集請求各建成一部 `one-off` 作品（bible 待寫）；已 `started` 的走完舊路。

站主真正要碰的：單集是「前提 → 故事聖經 → 劇本 → 語言 → 上架時間」，作品是「前提 → 設定集 → 總綱 → 每篇細綱 → 每集劇本 → 語言 → 上架時間」。

## 三、討論（劇本室）

### 為什麼

退回＋備註是單向的：站主寫一段，模型重寫整份，來回兩次就卡住。站主想要的是能問「第二幕為什麼要死一個人」、說「把師兄改成沉默寡言」、要「多給我兩個開場」，再決定。所以每份文件與每集劇本都有一條討論串，模型的回覆與新版本都留在串裡。

### 資料模型

新表 `video_drama_messages`（遷移接在 head 之後）：

| 欄位 | 內容 |
| --- | --- |
| `id`、`series_id`（FK，CASCADE） | |
| `subject` | `setting`、`outline`、`chapter:<n>`、`bible`、`script:<集數>` |
| `author` | `owner`｜`planner`｜`writer` |
| `body_md` | ≤ 8,000 字 |
| `refers_to` | 文件的版本號，或劇本 `script.md` 的 SHA-256 前 12 碼：讀的人知道這句話是對哪一版說的 |
| `answered_at` | 站主的訊息有模型回覆時寫；`null` 就是「等模型回覆」 |
| `created_at`、`created_by_user_id` | |

索引 `(series_id, subject, created_at)`。

### 端點

| 誰 | 端點 | 做什麼 |
| --- | --- | --- |
| 後台（content.read） | `GET /admin/video-automation/series/{slug}/messages?subject=` | 一條討論串 |
| 後台（content.manage） | `POST …/messages` `{subject, body}` | 站主發言；`admin_audit_logs` 一筆 |
| 工人 | `GET /video/automation/series/messages/next` | 最舊的、還沒回覆的站主訊息，連同：文件最新版（或劇本）、整條串、作品脈絡（`context_view`） |
| 工人 | `POST …/messages/{id}/answer` `{reply_md, revised?}` | 存回覆並標 `answered_at`；`revised` 有東西時，文件就多一個 `review` 版本（走 `submit_doc`），劇本就由工人自己寫回 `video.json` 與 `script.md`、重跑查核與聽眾審稿、再送一次劇本關卡 |

### 工人

`discussStep()` 排在 `seriesStep()` 之前：一輪最多回一則。文件用企劃模型 variant `discuss`，劇本用撰稿模型 variant `discuss`（提示詞在 `tools/video/automation/prompts.mjs` 的 `VARIANT_INSTRUCTIONS`；給代理用的同一份在 skill 的 `references/prompts/discuss.md`）。輸入：文件或 `video.json`、整條串、這則訊息、作品脈絡、頻道立場。輸出一個 JSON：`{ reply, revised }`。

模型要守的規矩（寫進提示詞）：

- 用繁體中文回覆，300 字以內，除非站主要的就是文字。
- 站主問問題就只回答（`revised: null`）；站主要改才出新版本，並在回覆裡列出改了什麼。
- 只改站主要求的部分。劇本要保留每句 id、過 lint；文件不能動到上面已核准的文件（討論細綱時不能改設定集，只能建議，站主再去設定集那條串說）。
- 給不出可用答案時，回覆說明原因，串停在那裡等站主，不自動重試。

討論的每一輪是一次模型呼叫（`variant: "discuss"`，提示詞紀錄 `planner:discuss`、`writer:discuss`），不算 `series_doc_rewrites`（那個只管單純的退回），也不算每月草稿。沒有輪數上限：站主在場才會有訊息；要停就關 `drama_enabled` 或放 `STOP` 檔。

### 後台

- 作品頁的每個 `DocPanel` 多一節「討論」：訊息列（站主／模型、對哪一版說的、時間）、輸入框與「送出」；原本的核准、退回、自己改都留著。有未回覆的訊息時顯示「等模型回覆」。
- 劇本關卡的卡片（`ScriptBody`）同樣一節，subject `script:<集數>`（影片列帶 `series_slug`、`episode_number`，單集也有）。
- 單集的影片頁最上面顯示它的故事聖經 `DocPanel`（含討論），下面才是劇本卡片與製作的關卡。「單集漫劇」清單改成列出 `kind = one-off` 的作品。
- 有討論的文件被核准時，串留著當紀錄，不再接受新訊息。

## 與既有文件的關係

- `DRAMA.md` 的「產線與關卡」：第 1 步的「站主選大綱」改成「站主核准故事聖經」，第 3 步之後加劇本關卡；其餘不變。
- `SERIES.md`：流程圖裡每個【站主核准／退回】變成【討論／核准】；「單集不走選大綱」那一段的理由仍成立，只是現在單集也是作品。
- `AUTOMATION.md`：工人的一輪多「討論」一段，排在作品之前；設定表依上面的三欄改寫。
- skill `youtube-video`：路線表的「AI 漫劇」與「長篇漫劇」合成一列；`drama.md` 的關卡從六個變成「文件、劇本」加自動的四個。

## 票

| 票 | 內容 | scope | 依賴 |
| --- | --- | --- | --- |
| `video-split-settings-api` | 新欄位與遷移、`DramaSettings` 擴充、`SettingsSave` 全部可省略、`stage_choice` 與自動核准依格式、`ToolSettingsView` | `apps/api/app/video_automation`、`apps/api/app/video_reviews/admin_service.py`、遷移、測試 | — |
| `video-split-settings-web` | 三個子分頁各自儲存、AI 設定頁的漫劇模型、說明文字、五語字串 | `admin-video-settings*.tsx`、`admin-video-model-settings.tsx`、`admin-video-series.tsx`、`admin.json` | api |
| `video-split-settings-worker` | 依格式讀聲音、常設指示、輪數、語言預設；`settle()`；`AUTOMATION.md` 設定表 | `tools/video/automation`、`docs/videos/AUTOMATION.md` | api |
| `video-drama-room-one-off-series` | `kind`、`bible` 文件、CHECK 放寬、請求表單建作品、`series/next` 出 `bible`、遷移轉換排隊中的請求 | `apps/api/app/video_automation`、遷移、測試 | — |
| `video-drama-room-messages-api` | `video_drama_messages`、後台與工人端點、audit | `apps/api/app/video_automation`、遷移、測試 | — |
| `video-drama-room-worker` | `discussStep`、`discuss` 兩個 variant、每支漫劇都有劇本關卡、由文件寫 `brief.md`、測試 | `tools/video/automation`、`tools/video/core/state.mjs`、skill 的 `references/prompts` | one-off-series、messages-api |
| `video-drama-room-web` | 討論串（文件與劇本）、單集頁、清單 | `admin-video-series.tsx`、`admin-video-review-card.tsx`、`admin-video-reviews.tsx`、測試、`admin.json` | messages-api |
| `video-drama-room-skill-docs` | skill 路線表與 `drama.md`、`series.md`；`DRAMA.md`、`SERIES.md`、`AUTOMATION.md` 對照上一節改 | `.agents/skills/youtube-video`、`.claude/skills/youtube-video`、`docs/videos` 三份 | worker、web |

順序：split 三張可以馬上做（api 先，web 與 worker 平行）；drama-room 的 one-off-series 與 messages-api 平行（兩支遷移，後落地的改號）→ worker、web → skill-docs。語言與上架的票在 [`LANGUAGES.md`](LANGUAGES.md)。
