# 長篇漫劇（作品、篇章、集）：設計

2026-09-27 定案。前提是 [`DRAMA.md`](DRAMA.md) 的單集漫劇路線（已上線）與 [`HANDS-OFF.md`](HANDS-OFF.md) 的分工（站主只管故事與上架時間）。這份寫在單集路線之上要加的東西：一部約 100 集、分成篇章的原創仙俠長篇，怎麼規劃、怎麼一集接一集地做、怎麼讓角色與故事在 100 集裡不漂移。票的 id 都是 `2026-09-26-video-series-*`。

## 站主的決定（2026-09-27）

| 項目 | 決定 |
| --- | --- |
| 作品結構 | 一部長篇，分成幾個「篇章」（約 10 篇、每篇約 10 集） |
| 規劃關卡 | 設定集與整體 100 集的總綱先核准；篇章細綱再逐篇核准 |
| 劇本關卡 | 每一集的劇本（旁白與對白）在花錢做圖與片段之前先給站主看 |
| 集與集之間 | 自動接續：一集核准上架後自動開始下一集；同時最多 1–2 集 |
| 參考面向 | 仙俠修真世界觀（門派世家、修為、正道與魔道）；群像與羈絆；前世今生、倒敘插敘、伏筆反轉、懸念連載；古風仙俠美術、點黑暗懸疑、鬼怪與符籙 |
| 情感線 | 雙男主知己羈絆，留白不點明 |
| 結局 | 第一部約 100 集只做「階段性收束」，主線不封死，為續作鋪梗；篇章與集數之後要能再加 |

**原創與版權**：站主拿《魔道祖師》當類型與敘事手法的參考。世界、人名、門派名、情節一律原創；企劃與撰稿的提示詞明寫「不得使用任何既有作品的人物、名詞、情節」，查核階段有一題「是否與知名作品雷同」。每集都有站主核准的劇本與設定集，這是 YouTube「非原創內容」政策下的作者證據。

## 名稱

| 站主看到的 | 內部 | 內容 |
| --- | --- | --- |
| 作品 | `series` | 這一部長篇：名稱、前提、參考面向、情感線尺度、風格預設、每集長度、預計集數、每篇集數、是否開放結局、狀態 |
| 設定集 | `setting` | 世界觀與規則（門派世家、修為體系、正道與魔道、力量的代價）、人物表（雙男主、5–8 個配角、反派；外觀提示詞、聲音、性格、關係圖）、語氣與畫面基調、命名規則、**長線謎團清單**（id、問題、預定揭曉區間；幾個標成「保留給續作」）、不做的事 |
| 總綱 | `outline` | 第一部的整體走向：篇章劃分（每篇主題、起點→終點、章末大轉折）、每集一句話、前世／今生兩條時間線的排程、謎團揭曉排程、全季張力地圖 |
| 篇章細綱 | `chapter` | 一篇約 10 集，每集：開場鉤子、本集主要衝突、轉折、結尾懸念（類型）、埋下與回收的伏筆（謎團 id）、情緒張力曲線、出場角色、場景、主題句 |
| 劇本 | `script` | 每集的場景、旁白、對白（說話者與情緒）、每鏡英文提示詞；連貫性與張力查核的結果 |
| 前情 | `recap` | 每集做完後自動寫的 150 字摘要、角色狀態變化、伏筆狀態，給下一集用 |

## 流程與關卡

```
作品建立（後台表單）
  → 設定集（企劃模型）→ 【站主核准／退回】
  → 總綱（企劃模型）→ 【站主核准／退回】
  → 第 1 篇細綱（企劃模型）→ 【站主核准／退回】
  → 第 1 集：企劃書由細綱直接生成（沒有大綱選項、不等人）→ 劇本（撰稿）→ 連貫性與張力查核 → 聽眾審稿
     → 【劇本關卡：站主核准／退回】
     → 角色設定圖（第一次生成，之後沿用作品的設定圖）→ 旁白 → 關鍵影格 → 分鏡 → 片段 → 配樂 → 合成 → 字幕 → 成片 → 上架包 → 上架確認
     → 前情摘要寫回作品 → 自動開始第 2 集
  → 第 k 篇做到剩 2 集時，先生成第 k+1 篇細綱送審（站主也可以隨時按「先規劃下一篇」）
```

站主真正要做的：核准設定集、總綱、每篇細綱、每集劇本（都可帶備註退回；模型依備註重寫，每份最多 `series_doc_rewrites` 輪，之後停在待審讓站主自己改），以及上架。其餘關卡依 `HANDS-OFF.md` 自動化：設定圖依 judge 分數自動選（票 `2026-09-26-video-hands-off-drama-look`）、旁白 Jev 全過自動核准、分鏡自動核准（設定已有開關）、成片自動品管（票 `hands-off-qa`／`judge`）。那些票落地前，這些關卡照舊等站主。

**作品的集數不走「選大綱」關卡**：這一集的大綱就是核准過的篇章細綱那一列。企劃書直接由它生成並在本機自動核准（備註「依第 k 篇細綱」）。HANDS-OFF 的「Jev 挑大綱」寫給教學片（要有示範或實算），不套到漫劇集數上。

**自動接續**（伺服器算，工人問）：作品 `active`、該集所在篇章的細綱已核准、前一集已「上架確認」（或已有 YouTube id）或被跳過、進行中的集數少於 `series_max_in_flight`（預設 1，可 2）。站主可暫停作品、跳過某集、要求「現在開始下一集」。

## 緊張感與追看感：寫進提示詞與查核的規格

1. **設定集**要有衝突引擎：正道與魔道的結構性矛盾、雙男主各自的秘密與代價、每個門派世家想要什麼；長線謎團 8–12 個，每個標「埋於第幾篇、揭曉區間、保留給續作與否」。
2. **總綱**要有全季張力地圖：每篇的賭注高過上一篇（個人→門派→天下）；第 5 篇左右一次翻轉世界觀的大揭露；每篇章末一個改變局勢的轉折；前世線倒敘插敘，每篇至少 1–2 集是前世；每集一句話要看得出「回答一個問題、丟出一個更大的問題」。
3. **篇章細綱**每集固定欄位：`hook`（開場 20 秒內的鉤子）、`conflict`、`turn`（中段轉折）、`cliffhanger`（類型：危機／揭露／抉擇／反轉／情感）、`setups`／`payoffs`（引用謎團 id）、`tension`（五個節拍各 1–5 分，結尾 ≥ 4，不能一路平）、`characters`、`locations`、`theme`。規則：相鄰兩集的懸念類型不同；每 3–4 集至少收一個伏筆；每篇最後一集的懸念必須改變觀眾對前面某件事的理解。
4. **撰稿**依細綱寫：鉤子在第一場、轉折在中段、最後一場只做懸念不做總結；對白留白（羈絆不點明）；每集 2–4 分鐘、每鏡 ≤ 10 秒；角色外觀與聲音逐字沿用設定集。
5. **查核（張力與連貫性）**：對照細綱檢查 hook／turn／cliffhanger 是否真的在劇本裡、伏筆是否對得上謎團清單、人物設定與前情是否一致、是否與知名作品雷同；輸出 `beat_coverage`（每個節拍：有／弱／無）與 `continuity_problems`，顯示在劇本關卡的卡片最上面。
6. **前情**：每集完成後由查核模型寫 150 字摘要、角色狀態、伏筆狀態；下一集的撰稿與查核拿最近 3 集的全文、更早的只拿一句話。

## 伺服器（`apps/api/app/video_automation/`）

新表（migration 編號取實作當時的 head；一律「不存在才建」）：

- `video_drama_series`：`id`、`slug`（唯一，`^[a-z0-9][a-z0-9-]{1,39}$`）、`title`、`premise`、`aspects`（JSON）、`tone`（String(40)）、`style_preset`、`target_minutes`、`planned_episodes`（1–500）、`episodes_per_chapter`（4–20）、`open_ended`、`status`（`draft|setting|outline|active|paused|finished`）、`note`、`created_by_user_id`、時間欄。
- `video_drama_docs`：`series_id`、`kind`（`setting|outline|chapter`）、`chapter_number`、`version`、`body_md`、`body_json`、`status`（`generating|review|approved|rejected`）、`note`、`decided_at`、`decided_by_user_id`、`created_at`；唯一 `(series_id, kind, chapter_number, version)`；舊版本留著當歷史。
- `video_drama_episodes`：`series_id`、`number`、`chapter_number`、`title`、`logline`、`beats`（JSON）、`status`（`planned|ready|queued|started|done|skipped`）、`slug`、`request_id`、`recap`、`state_json`、`started_at`、`finished_at`。
- `video_drama_requests` 加 `series_id`、`episode_number`：作品的每一集仍走請求佇列與 `draftDrama` 路徑；`next_request` 先作品集數（依 `(series, number)`，且該作品沒有 `started` 的集）再單集請求。
- `video_projects` 加 `series_slug`、`episode_number`；`GET /admin/videos` 加 `?format=`／`?series=` 篩選。
- 關卡 `script`：`Gate` Literal 與 `ck_video_review_gate` 重建（同 0095 的做法）；`CHOICE_GATES` 不變。
- `video_stage_prompts` 主鍵加 `variant`；`StageRunIn.variant`（`setting|outline|chapter|episode|recap|fix`）；「目前的提示詞」依 variant 分開。
- 設定：`series_max_in_flight`（1–2）、`series_script_gate`、`series_auto_continue`、`series_chapter_ahead`（剩幾集先規劃下一篇，預設 2）、`series_doc_rewrites`（預設 2）、`series_episodes_per_month`（預設 30）。作品集數不算 `max_drafts_per_month`；作品層文件的企劃呼叫也不算草稿。

| 誰 | 端點 | 做什麼 |
| --- | --- | --- |
| 後台（content.read） | `GET /admin/video-automation/series`、`GET …/series/{slug}` | 作品列表；作品詳情（文件最新版與狀態、集數表含 stage、待審數、花費） |
| 後台（content.manage） | `POST …/series`、`PATCH …/series/{slug}` | 建立；改前提、面向、集數、狀態（暫停、繼續、完結） |
| 後台（content.manage） | `POST …/series/{slug}/docs/{kind}[/{chapter}]/decision` | 核准或退回（退回要備註） |
| 後台（content.manage） | `PUT …/series/{slug}/docs/{kind}[/{chapter}]` | 站主自己改文件（新版本） |
| 後台（content.manage） | `PUT …/series/{slug}/episodes/{n}` | 開始前改集名、一句話、細綱欄位 |
| 後台（content.manage） | `POST …/series/{slug}/actions/{plan-next-chapter\|start-next\|skip/{n}}` | 手動推進 |
| 工人（VideoTool） | `GET /video/automation/series/next` | 下一件作品層的工作：`{kind: setting\|outline\|chapter\|episode, series, chapter_number?, episode?, context}` |
| 工人 | `POST …/series/{slug}/docs`、`POST …/episodes/{n}/start`、`POST …/episodes/{n}/recap`、`POST …/episodes/{n}/done` | 寫回 |
| 工人 | `GET …/series/{slug}/context?episode=n` | 提示詞的脈絡：設定集、總綱、該篇細綱、前 3 集前情全文與所有集的一句話、謎團狀態 |

`AppError` 只在 `admin_api.py`；模組丟 `SeriesRefused`。後台路徑不需要四語錯誤。

## 工具端（`tools/video`）

- `video.json` 頂層新增可選 `series: { slug, episode, chapter }`；lint：作品集數的 `characters` 必須是設定集人物表的子集且 `appearance`／`voice`／`sheet_prompt` 逐字相同，角色依 id 排序（`lookHash` 只在 cast 變動時改變）。
- `DRAMA_STEPS` 在 `fact-checked` 之後加 `script approved`；`GATES.script` 綁 `docDir/script.md`；`REVIEW_GATES`、`STEP_LABELS`、`nextGate`（drama：outline → script → look → audio → storyboard → final）、`scriptSubmission`。
- **劇本檔** `screenplay(doc)` → `docs/videos/<slug>/script.md`。**關卡雜湊只算敘事**（場景順序、每句的 id／文字／說話者／情緒），不算鏡頭提示詞：look／keyframes／clips 的自動修圖不會讓已核准的劇本變 stale；旁白被退回而改了台詞才要再看。送審 payload：`{scenes:[{id, chapter, lines:[{speaker, name, text, emotion}], prompt}], beats, coverage, continuity_problems, minutes}`。
- `automation/series.mjs`：`seriesStep()` 排在 `dramaNext()` 之前：`setting`／`outline`／`chapter` 跑企劃模型（`stage("planner", "series-<slug>", payload, 32_000, "drama", variant)`）並 `POST docs`；`episode` 就 `POST episodes/{n}/start` 再走 `draftEpisode`。退回帶 `owner_note` 重寫，超過 `series_doc_rewrites` 停在待審。
- `flow.mjs`：`draftEpisode(request)`：企劃書由細綱生成（`## 故事前提`＝作品前提＋本集一句話、`## 角色` 逐字來自設定集、`## 站主觀點` 來自頻道立場或作品備註、`## 幕`＝beats、`## 大綱` 單一選項），本機直接核准 outline；`scriptPayload` 多帶 `series` 脈絡；`advance()` 在 listener 之後加 `scriptGate`（送審／等／退回→撰稿 FIX 模式）；`video assembled` 後跑 `recap` 並寫回；上架確認後 `POST done`。
- 提示詞：skill `references/prompts/series-setting.md`、`series-outline.md`、`series-chapter.md`、`writer-series.md`、`verifier-series.md`，規格照上一節；`DRAMA_INSTRUCTIONS.planner` 的「不重複前一支的角色」在作品模式改成「延續作品的角色」。
- **設定圖沿用**：作品存檔 `<VIDEO_WORKDIR>/_series/<series>/characters/<id>/<sheetKey>.png`＋`index.json`（`sheetKey = hash(id, appearance, sheet_prompt, resolvedLook)`）。`look` 對每個角色先查存檔，有核准過的就放進這一集的 manifest 當唯一候選並寫 `choice.json` 與 approvals（備註「沿用作品設定圖」），只為新角色生成；核准後把選中的圖複製進存檔。`keyframes` 每集本來就會把選中的圖重新上傳到該 slug 的媒體庫。
- 詞彙表：設定集階段就把人名、門派名、術語連同讀音寫進 `docs/videos/lexicon.json`（`speechHash` 含整份詞彙表，之後才加詞會讓進行中的集重錄旁白）。

## 後台（`apps/web`）

- `/admin/videos` 三個分頁：**教學影片**（現有列表，篩 `format !== "drama"`）、**漫劇**（新）、**設定**（`?tab=settings` 深連結保留）。查詢鍵 `series`（`?tab=drama&series=<slug>`），`video=` 仍優先開單集頁。
- 審核卡片與關卡 body 在 `admin-video-review-card.tsx`（W0 抽出），列表頁與作品頁都用它。
- `admin-video-series.tsx`：作品列表卡（進度、狀態、花費、待站主的項目數）＋「新的作品」表單；作品頁：控制（暫停／繼續、先規劃下一篇、現在開始下一集）、設定集／總綱／每篇細綱各一個可展開區塊（細綱用表格：集數、鉤子、衝突、轉折、懸念、伏筆、張力、狀態）、每份文件「核准」「退回＋備註」「自己改」、集數表。單集的「新的漫劇」與佇列也搬來這裡。
- 新關卡卡片 `ScriptBody`：最上面是 beat_coverage 與連貫性問題，接著逐場景【角色】台詞、可展開的鏡頭提示詞；核准、退回＋備註。

## 與 HANDS-OFF 的關係

方向一致：站主只管故事與上架時間。要接的地方：`hands-off-drama-look` 的自動選與本設計的沿用都改 `review/sync.mjs`（沿用先查存檔、沒有才自動選）；`hands-off-web` 與本設計都改 `admin-video-reviews.tsx`（W0 先抽卡片檔）；`hands-off-settings` 的 migration 先進；`hands-off-worker` 動 `tools/video/automation`，本設計把新東西放 `series.mjs`。不套用 Jev 挑大綱。

## 一鍵合集與免關卡（2026-09-27 加，設計在 [`BINGE.md`](BINGE.md)）

作品表多了一組欄位（遷移 `0103_video_binge_series`），讓後台的一顆按鈕就能建立一部約兩小時、不留任何關卡、做完自動接成一支長片的爽文合集：

| 欄位 | 預設 | 用途 |
| --- | --- | --- |
| `genre` | `xianxia-bonds` | 題材預設（六個）：企劃寫哪種故事、有沒有節奏規格；既有作品落在預設，提示詞與規則不變 |
| `lead` | `dual-male` | 主角：`female`、`male`、`dual-male` |
| `hands_off` | false | **免關卡**：設定集、總綱、細綱由查核模型出裁決、伺服器依 `series_doc_passed` 核准或退回重寫；劇本由 `script_check_passed` 判；設定圖與分鏡視為自動開關開著 |
| `compilation` | false | 全部集數 `done\|skipped` 後，`next_job_for` 多給一種工作 `compilation`；`start_compilation`／`finish_compilation` 記 `compilation_slug`（`<作品>-full`）與時間；站主也可在完結的作品按「做合集」（`actions/compile`） |
| `visual_tier` | `clips` | 每集有多少鏡頭買片段（`clips`、`hybrid` 四成、`stills` 一成），lint 依 `series.json` 擋 |
| `total_minutes` | null | 一鍵表單給的總長度（30–480）；`binge_shape` 由它算 `planned_episodes` 與 `episodes_per_chapter` |

`series_max_in_flight` 的上限從 2 放到 6。上面流程圖裡的每個【站主核准／退回】，在 `hands_off` 作品上都由查核與伺服器規則代替；「站主真正要做的」只剩暫停／放棄、關掉免關卡回到人審、下載合集成片上傳與選上架時間。門檻常數、節奏規格、題材預設、合集的 `compile` 指令與後台表單都在 `BINGE.md`。

## 成本與節奏（估計，試作後改）

- 作品層文件：設定集、總綱各 1 次企劃呼叫（32k 輸出），每篇細綱 1 次；用 Claude Code 訂閱帳號不另計費。
- 每集：撰稿 1–3 次、查核 1–2 次、聽眾 1 次、前情 1 次；媒體約 US$40–55；第一部 100 集約 US$4,000–6,000。
- 節奏：月預算 3,000 片段秒 ≈ 11 集／月；`series_max_in_flight=1` 時一集約 1–2 小時機器時間加站主看劇本的時間。

## 分期與票

| 票 | 做什麼 | 依賴 |
| --- | --- | --- |
| `video-series-review-card-file`（W0） | 審核卡片與關卡 body 抽成 `admin-video-review-card.tsx` | — |
| `video-series-api`（A1） | 三張表、`script` 關卡、請求佇列的作品順序、`series/next`、文件版本與退回、篩選、`variant` 提示詞、月集數預算 | hands-off-settings（migration 順序） |
| `video-series-web-routes`（A2） | 工人的作品路由轉送 | — |
| `video-series-core-script-gate`（T1） | `series` 欄位與 lint、`script.md` 與敘事雜湊、`script approved`、`GATES.script`、`scriptSubmission` | — |
| `video-series-planning`（T2） | `series.mjs` 的三種文件、提示詞、`references/series.md` | A1、A2 |
| `video-series-episodes`（T3） | `draftEpisode`、作品脈絡、劇本關卡、前情、自動接續、設定圖沿用 | T1、T2、hands-off-drama-look |
| `video-series-admin-tab`（W1） | 三個分頁、作品頁、文件核准、集數表、`ScriptBody` | A1、W0 |
| `video-series-pilot`（P1） | 第一部：設定集、總綱、第 1 篇細綱核准，第 1–3 集做到上架，記數字 | 全部＋部署 |

順序：W0 → A1（A2、T1 平行）→ T2 → T3 → W1 → 部署 → P1。
