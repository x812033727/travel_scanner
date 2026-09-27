# 一鍵漫劇合集（binge）：設計

2026-09-27 定案。前提是 [`SERIES.md`](SERIES.md) 的長篇作品（設定集、總綱、篇章細綱、逐集製作、劇本關卡）、[`DRAMA.md`](DRAMA.md) 的單集漫劇路線與 [`HANDS-OFF.md`](HANDS-OFF.md) 的分工。這份寫在作品路線之上要加的東西：後台**一個按鈕**就自動產出一部約兩小時（長度可設）、一口氣看完的原創爽文漫劇合集——文件由查核模型判、每集不留關卡、全部做完接成一支長片、成片從後台下載。票的 id 都是 `2026-09-27-video-binge-*`。

站主給的參考是 YouTube `zH9N0JXvhlQ`（花影漫剧FlowAnimation，「重生回游戏开服当天，她觉醒逆天女帝天赋…背叛者还在做梦，她已磨好刀」）：約兩小時的「一口氣看完」AI 漫劇合集，重生／遊戲系統／復仇打臉爽文，女主角，旁白加角色配音，燒錄字幕，多語 CC。要求：按一個按鈕就產出一部長度可設、品質在參考之上、每集劇情都好、黏著度很高的劇。

## 站主的決定（2026-09-27）

| 項目 | 決定 |
| --- | --- |
| 畫面 | **混合（hybrid）**：約四成鏡頭生成影片片段，其餘用關鍵影格加運鏡；全片段與全靜圖仍可選 |
| 關卡 | **完全自動，不留任何關卡**：設定集、總綱、細綱由查核模型出裁決、伺服器依規則核准或退回重寫；劇本由查核的節拍覆蓋與量測節奏決定；設定圖與分鏡視為開關開著；成片與上架包照 HANDS-OFF 的自動品管。站主只能暫停／放棄、把作品的「免關卡」關掉回到人審，以及決定上架時間 |
| 範圍 | 這次全部做完：八張票在同一條分支實作到可部署 |
| 長度 | 預設 120 分鐘，30–480 分鐘可設；每集 2–4 分鐘；集數與每篇集數由總長度算出 |
| 題材 | 六個題材預設（仙俠羈絆保留今天的規則；重生復仇、系統遊戲、都市歸來、女帝崛起、自訂帶節奏規格）；主角女／男／雙男主 |
| 上架 | 仍由站主在 Studio 上傳（HANDS-OFF 第一步）；合集多一條「從後台下載 1080p 成片」的路徑 |

**不變的前提**：旁白台灣國語（Gemini Sulafat＋角色聲音）、燒錄繁中字幕、en／ja／ko／zh-CN CC、合成內容揭露一律勾、原創規則（不用任何既有作品的人物、名詞、情節，查核有雷同檢查）、`STOP` 檔、預算由伺服器以 429 擋。舊作品不受影響：`genre=xianxia-bonds`、`hands_off=false`、`visual_tier=clips` 是預設，提示詞在該題材保留原文，lint 對沒有 `visual` 的鏡頭視為 clip。

## 名稱

| 站主看到的 | 內部 | 內容 |
| --- | --- | --- |
| 合集作品 | 有 `total_minutes` 的 `series` | 一鍵表單建立的作品：題材、主角、總長度、每集分鐘、畫面等級、免關卡、要做合集；slug `<題材>-<yyyymmdd>-<4 hex>`，名稱先是「〈題材〉合集 （企劃命名中）」，設定集核准時若 `body_json.title` 有名字就改成它 |
| 題材預設 | `genre`、`GENRE_SPECS` | 企劃寫什麼故事：前提種子、衝突引擎、爽點類型、套路、標題公式、縮圖公式、不做的事、有沒有節奏規格 |
| 爽點 | `satisfaction` | 觀眾為它留下來的那一下：打臉、身份揭露、反殺、升級、首殺、背叛者遭報、反派低頭、藏拙露鋒、當眾平反、及時救場、反轉（`SATISFACTION_TYPES` 的 11 個 id） |
| 裁決 | `judge`／`verdict` | 查核模型對一份文件的判斷：每個必要項目「有／弱／無」、問題清單、雷同作品清單、一行備註 |
| 免關卡 | `hands_off` | 文件、劇本、設定圖、分鏡都由查核與伺服器規則決定 |
| 畫面等級 | `visual_tier`、鏡頭的 `visual` | 一集裡多少鏡頭買片段：`clips` 全部、`hybrid` 四成、`stills` 一成；其餘鏡頭是 `visual: "still"`，關鍵影格加運鏡 |
| 合集 | `compilation`、影片 `<作品>-full` | 全部集數完成後，把每集成片依序接成一支：集間 2 秒章節卡、片尾 4 秒卡、章節＝每集、五語字幕合併、企劃寫標題／說明／標籤／縮圖 |
| 冷開場 | — | 合集模式的每一集沒有片頭卡：第一句就是鉤子，最後一句是懸念，之後沒有任何總結 |

## 流程

```
一鍵開拍（後台表單：題材、主角、前提可空、總長度、每集分鐘、畫面等級、風格、備註）
  → 伺服器算集數與每篇集數，建立作品（hands_off、compilation 都開）
  → 設定集（企劃模型）→ 查核模型裁決 → 伺服器：過就核准；不過就退回重寫（series_doc_rewrites 輪）；用完才等站主
  → 總綱（同上）
  → 第 1 篇細綱（同上；帶節奏欄位）
  → 第 1 集：企劃書由細綱生成 → 撰稿 → 查核（coverage、retention）→ 聽眾審稿
     → 工人先自己判劇本（scriptVerdict）：不過就交撰稿 FIX（最多 MAX_PROMPT_FIX_ROUNDS 輪）→ 送審 → 伺服器依 script_check_passed 當場核准
     → 設定圖（judge 最高分自動選）→ 旁白（Jev）→ 關鍵影格 → 分鏡（judge 自動核准）→ 片段（只買 visual: clip 的鏡頭）→ 配樂 → 合成（still 鏡頭走 zoompan）→ 字幕 → qa → 成片自動核准 → 上傳包 → 上架確認自動核准
     → 前情寫回 → 自動開下一集（series_max_in_flight 集同時）
  → 全部集數 done：作品 finished → 工人拿到 compilation 工作
  → 合集：企劃寫標題／說明／標籤／縮圖 → render 章節卡與縮圖 → compile 串接 → 五語標題與說明 → qa（6 項）→ 成片自動核准 → 上傳包 → 進「可以上架」
  → 站主從作品頁或「可以上架」卡下載 1080p 成片 → Studio 上傳私人 → 貼網址、選上架時間
```

仍然會找站主的只有：查核退回重寫用完仍不過的文件（停在待審，附查核的問題）、劇本被退回 `MAX_PROMPT_FIX_ROUNDS` 輪後卡住、自動品管有項目沒過、卡住的影片（同一階段連續失敗、預算、缺金鑰、磁碟）、上架時間。

## 資料模型（遷移 `0102_video_binge_series`，接在 `0101_video_dub_locales` 後）

`video_drama_series` 的新欄位（`apps/api/app/video_automation/models.py` 的 `VideoDramaSeries`；比照 0100 的「不存在才建」寫法）：

| 欄位 | 型別／預設 | 用途 |
| --- | --- | --- |
| `genre` | String(32) `xianxia-bonds`；CHECK `ck_video_drama_series_genre` in (`xianxia-bonds`, `rebirth-revenge`, `system-game`, `urban-return`, `empress-rise`, `custom`) | 題材預設；既有作品落在 `xianxia-bonds`，行為不變 |
| `lead` | String(12) `dual-male`；CHECK `ck_video_drama_series_lead` in (`female`, `male`, `dual-male`) | 主角 |
| `hands_off` | Boolean false | 文件、劇本、設定圖、分鏡全部自動決定 |
| `compilation` | Boolean false | 全部集數完成後做合集 |
| `visual_tier` | String(8) `clips`；CHECK `ck_video_drama_series_tier` in (`clips`, `hybrid`, `stills`) | 鏡頭用片段的比例上限 |
| `total_minutes` | Integer nullable；CHECK `ck_video_drama_series_total_minutes`：NULL 或 30–480 | 站主要的合集長度；集數由它推出 |
| `compilation_slug` | String(80) nullable，唯一 `uq_video_drama_series_compilation_slug` | 合集影片的 slug（`<作品>-full`）；null＝還沒開始 |
| `compilation_started_at`／`compilation_finished_at` | DateTime nullable | 合集開始、可以上架的時間 |

`video_automation_settings`：`ck_video_drama_series` 重建成 `series_max_in_flight BETWEEN 1 AND 6`（原 1–2）。不加新的全域開關：免關卡是每部作品的旗標。`video_projects` 不加欄位：合集影片以 `series_slug IS NOT NULL AND episode_number IS NULL` 辨識（伺服器用 `compilation_slugs()` 查作品表）。降級在任何設定列 `series_max_in_flight > 2`、或任何作品 `hands_off`／`compilation` 為真時拒絕。

`SeriesSummary`／`SeriesOut` 多回這九個欄位；舊的 API 列讀成經典作品。

## 一鍵表單與報價（`apps/api/app/video_automation/admin_api.py`、`series.py`）

沒有另開端點：`POST /admin/video-automation/series` 的 `SeriesIn` 多了 `genre`、`lead`、`hands_off`、`compilation`、`visual_tier`、`total_minutes`（30–480）。表單留白 `slug`、`title`、`premise`，伺服器補（`series_values`）：

| 表單給的 | 伺服器算 |
| --- | --- |
| `total_minutes`、`target_minutes`（每集分鐘；表單限 2–4，API 1–8） | `binge_shape(total, episode)`：`planned_episodes = round(total / episode)`（1–500）；≤ 10 集就一篇；否則每篇 6–10 集，取最後一篇最滿的、平手取大的。120／3 → 40 集 4 篇；30／3 → 10 集 1 篇；35／2 → 18 集 9 集一篇；128／4 → 32 集 8 集一篇 |
| 沒有 `slug` | `auto_slug`：`<genre 前 16 字>-<yyyymmdd>-<4 hex>` |
| 沒有 `title` | `auto_title`：「〈題材 label〉合集 （企劃命名中）」；設定集核准（`_apply_approval`）時若 `body_json.title` 有字且名稱仍含 `AUTO_TITLE` 就換掉 |
| 沒有 `premise` | 「由企劃依「〈題材〉」題材預設自擬前提」；`custom` 題材一定要有前提（422） |

後台的一鍵表單固定送 `hands_off: true`、`compilation: true`、`open_ended: false`。作品建立時 audit `video_series_created` 記下這幾個欄位。

**報價** `GET /admin/video-automation/series/binge-quote?total_minutes&episode_minutes=3&visual_tier=hybrid`（content.read）→ `BingeQuoteOut`：`{episodes, chapters, episodes_per_chapter, clip_seconds, images, judge_calls, usd, budgets: {clip_seconds, images, judge_calls, episodes_per_month: {needed, monthly, ok}}, ok}`。純函式 `binge_quote`：每分鐘 10 鏡（`SHOTS_PER_MINUTE`）× 6 秒（`SHOT_SECONDS`）× 1.5 重做（`RETAKE_FACTOR`）× 等級比例 `TIER_CLIP_SHARE = {clips: 1.0, hybrid: 0.4, stills: 0.1}`；圖片＝鏡數 × 1.3（`KEYFRAME_TAKES`）＋ 18 張設定圖（`SHEET_IMAGES`）；judge＝鏡數＋片段鏡數＋18；單價從 `apps/api/app/video_media/catalog.py` 依設定的模型讀（沒有就 US$0.15／秒、US$0.134／張），judge `JUDGE_USD_PER_CALL` US$0.01，每集再加 US$1（配音、音樂、字幕）。120／3／hybrid → 40 集 4 篇、4,320 片段秒、1,578 張、1,698 次 judge、US$916.43。`ok` 為假的項目表單標紅。

## 伺服器規則（純函式，`apps/api/app/video_automation/judge.py`，比照 `outline_pick_passed`）

### 文件：`series_doc_passed(judge, kind)`

工人送 `SeriesDocSubmitIn.judge`（可選）：

```json
{"verdicts": {"originality": "有", "conflict_engine": "弱", …}, "problems": ["zh-TW 句子"], "similar_works": ["…"], "notes": "一行"}
```

| 常數 | 值 | 意思 |
| --- | --- | --- |
| `VERDICT_VALUES` | `有`、`弱`、`無` | 每個項目只能是這三個字 |
| `REQUIRED_VERDICTS["setting"]` | `originality`、`conflict_engine`、`genre_fit`、`cast_playable` | 原創、衝突引擎、題材契合、人物可拍 |
| `REQUIRED_VERDICTS["outline"]` | `originality`、`escalation`、`midpoint_reveal`、`chapter_turns`、`satisfaction_schedule` | 原創、賭注升級、中段翻轉、每篇章末轉折、爽點排程 |
| `REQUIRED_VERDICTS["chapter"]` | `originality`、`tension_rules`、`hooks`、`satisfaction`、`alternation`、`escalation` | 原創、張力規則、鉤子、爽點、交錯、升級 |
| `MAX_WEAK_VERDICTS` | 1 | 最多一個「弱」 |

通過＝必要項目都在、沒有「無」、「弱」≤ 1、`problems` 與 `similar_works` 都是空清單。少一個鍵、多一句問題，都不過：沉默不算通過。

`auto_doc_status(series, payload, version, rewrites)`（`series.py`）決定送進來的版本的狀態：

| 情況 | 狀態 | 備註（`note`） |
| --- | --- | --- |
| 作品不是免關卡，或送件沒帶 `judge` | `review`（等站主） | 無 |
| 通過 | `approved`，跑 `_apply_approval` | 「查核：originality 有、…，依作品設定自動核准」 |
| 不過，`version - 1 < series_doc_rewrites` | `rejected` → 既有 `_rewrite_job` 的重寫循環接手（帶 `previous` 與 `owner_note`） | 「[auto] 查核沒過：〈problems〉；與既有作品雷同：…；缺少：…」 |
| 不過，重寫用完 | `review`（等站主，卡片顯示問題） | 同上 |

每筆自動決定寫 audit `video_series_doc_auto_approved`／`video_series_doc_auto_rejected`（帶 `verdicts`）。工人拿不到可用裁決（`OUTPUT_INVALID` 兩次）就不帶 `judge` 送件，文件照舊等站主，不擋。

### 劇本：`script_check_passed(payload, retention_required)`

payload 是 `tools/video/review/sync.mjs` 送審 `script` 關卡時的 `coverage`、`continuity_problems`、`similar_works`、`retention`（來自 `review/script-check.json`）：

```json
{"coverage": {"hook": "有", "conflict": "有", "turn": "弱", "cliffhanger": "有", "satisfaction": "有"},
 "continuity_problems": [], "similar_works": [],
 "retention": {"hook_seconds": 4.8, "satisfaction": {"count": 2, "first_seconds": 22.3, "positions": [22.3, 118.0]}, "cliffhanger_last": true}}
```

| 常數 | 值 | 規則 |
| --- | --- | --- |
| `COVERAGE_BEATS` | `hook`、`conflict`、`turn`、`cliffhanger` | 四個都在（`有` 或 `弱`），沒有 `無`，`弱` ≤ `MAX_WEAK_VERDICTS`（1） |
| — | — | `continuity_problems` 與 `similar_works` 都空 |
| `RETENTION_GENRES` | `rebirth-revenge`、`system-game`、`urban-return`、`empress-rise`、`custom` | 只有這些題材再看下面四條（`retention_required_for(genre)`）；`xianxia-bonds` 到這裡就過 |
| — | — | `coverage.satisfaction` 是 `有` 或 `弱` |
| `HOOK_MAX_SECONDS` | 8.0 | `retention.hook_seconds`（鉤子那句結束的秒數）≤ 8 |
| `MIN_SATISFACTION` | 2 | `retention.satisfaction.count` ≥ 2 |
| `FIRST_SATISFACTION_MAX_SECONDS` | 30.0 | `retention.satisfaction.first_seconds` ≤ 30 |
| — | — | `retention.cliffhanger_last` 為真（懸念那句是劇本最後一句） |

只在 `hands_off` 作品上判（`auto_approves_script` → `hands_off_series`），舊工人沒帶這些欄位的 payload 永遠不自動過。過了伺服器當場核准，備註 `SCRIPT_AUTO_APPROVED_NOTE`「查核對照細綱：四個節拍都在、沒有連貫性問題，依作品設定自動核准」（`admin_service.submit_review` 的 `gate == "script"` 分支）。沒過就照舊等站主——但工人在送審**之前**已經自己判過一次（下一節），所以送上來的多半會過。

**秒數不是模型估的**：查核只指出 `hook_line`、`satisfaction_lines`、`cliffhanger_line` 這幾個句子 id，工人的 `retentionNumbers` 用估計時間軸（每分鐘 250 字）算 `hook_seconds`（鉤子句的結束）、`first_seconds`／`positions`（每個爽點句的開始）與 `cliffhanger_last`（最後一句的 id 是不是它）。提示詞寫「鉤子 ≤ 5 秒」，量測門檻放寬到 8 秒，是給估計誤差留的餘裕。

### 設定圖、分鏡、成片

- `auto_picks_look`／`auto_approves_storyboard`（`settings.py`）多收 `series_slug`：影片屬於 `hands_off` 作品時視為開關開著，門檻仍是 `judge_min_score`。
- `final_qa_passed(payload, sha, required)` 多一個參數：合集影片（slug 在 `compilation_slugs()`）用 `COMPILATION_QA_ITEMS = ("assemble", "captions", "metadata", "links", "thumbnail", "disclosure")`，而且報告要有 `kind: "compilation"`；每一集自己已經過完 11 項。

### 合集工作

- `next_job_for`：作品 `status == "finished"`、`compilation` 為真、`compilation_slug is None`、有集數且每一集都 `done|skipped`、至少一集 `done` → `NextJob(kind="compilation")`。`finish_episode` 照舊在全部完成且集數達 `planned_episodes` 時把作品設成 `finished`；合集工作就從 `finished` 出發。
- `start_compilation(session, token, slug, video_slug)`：寫 `compilation_slug`／`compilation_started_at`，回 `SeriesCompilationStartOut`：作品摘要、`done` 的集（依序，含 slug、標題、一句話、前情）、`context`（設定集、所有前情）。作品沒完結、沒開合集、已在做、或 slug 已被用都是 409。
- `finish_compilation(session, slug)`：寫 `compilation_finished_at`。
- `act(session, actor, slug, "compile")`：站主在完結、沒設定合集的作品上按「做合集」；把 `compilation` 設真，工人下一輪開始。一部作品只有一部合集（工人固定叫它 `<作品>-full`，slug 被第一部占著，清掉 `compilation_slug` 也會讓第一部的下載失效）：正在做時 409 `video_series_compiling`，做過了 409 `video_series_compiled`；要重做，改的是那支合集影片本身（重跑它的步驟）。
- 工人路由：`POST /video/automation/series/{slug}/compilation/start`（body `{slug: "<作品>-full"}`）、`…/compilation/done`；網站轉送在 `apps/web/app/api/video/automation/series/[slug]/compilation/`。

### 下載

`GET /admin/videos/{slug}/download`（`apps/api/app/video_reviews/admin_api.py`，content.manage）：只給合集影片；`FileResponse` 串流 `<VIDEO_WORK_DIR>/<slug>/upload/final.mp4`（`config.py` 的 `video_work_dir`，預設 `/var/lib/mokaair/video-work`），`Content-Disposition: attachment; filename=<slug>.mp4`、`Cache-Control: private, no-store`、支援 Range。不是合集、檔案還不在、或 API 沒掛載都是 404 `video_download_not_found`（訊息說明是哪一種）。`ProjectSummary`／`ProjectOut` 多 `compilation` 與 `download_available`。BFF `apps/web/app/api/admin-video-download/[slug]/route.ts` 比照 `admin-video-files` 串流並傳 Range。

## 節奏規格（寫進提示詞與查核；`tools/video/automation/prompts.mjs` 的 `RETENTION_RULES`）

只套在 `GENRE_SPECS[genre].retention` 為真的題材（除 `xianxia-bonds` 外皆真）。`genreBlock(series)` 把題材段落接在企劃、撰稿、查核三個階段的提示詞後面（`GENRE_STAGES`）。

| 規格 | 寫進提示詞 | 量測／檢查 |
| --- | --- | --- |
| 鉤子 | 第一句就是鉤子：沒有片頭卡、沒有問候、沒有佈景；約 5 秒（一句約 25 字）內觀眾知道誰有麻煩或什麼不可能；類型 `question`／`danger`／`image`／`line`／`reversal` | `hook_seconds` ≤ 8（`HOOK_MAX_SECONDS`） |
| 衝突 | 約 10 秒內說清或演出本集衝突 | `coverage.conflict` |
| 第一個爽點 | 30 秒內 | `first_seconds` ≤ 30 |
| 情緒節點 | 每 20–30 秒（每 2–3 鏡）一個：一句刺人的話、一個眼神、反轉、揭露、威脅 | `coverage.turn`、`tension` 曲線 |
| 交錯 | 爽點之後馬上是更大的麻煩；每集至少 2 個爽點（`MIN_SATISFACTION`），用題材的類型 id | `count` ≥ 2、`coverage.satisfaction` |
| 懸念 | 最後 5–10 秒就是懸念，之後沒有總結、沒有教訓、沒有「下集」 | `cliffhanger_last`；查核把懸念後面接總結的判成 `弱` |
| 主角走向 | 不能連續兩集主角只挨打（`lead_arc`：`wins`／`suffers`／`mixed`）；每篇賭注高過上一篇；全劇中段一次翻轉世界觀 | 細綱檢查（下面） |
| 對白 | 短而利：旁白帶速度，角色帶刀 | 聽眾審稿 |

**爽點類型**（`SATISFACTION_TYPES`，伺服器 `COMMON_SATISFACTIONS` 同一份；六個題材目前都用全部 11 個）：

| id | 內容 |
| --- | --- |
| `face_slap` | 打臉：看不起主角的人當場被事實打臉 |
| `identity_reveal` | 身份揭露：藏著的身份、實力或關係攤開 |
| `counter_kill` | 反殺：被逼到絕路的人反過來解決對手 |
| `level_up` | 升級：能力、境界、資源躍升一級 |
| `first_clear` | 首殺／首通：別人做不到的事第一個做到 |
| `betrayer_punished` | 背叛者遭報：前世或此前的背叛得到報應 |
| `villain_humbled` | 反派低頭：囂張的人被迫收斂或求饒 |
| `hidden_power` | 藏拙露鋒：一直藏著的底牌亮出來 |
| `public_vindication` | 當眾平反：誤解在眾人面前被推翻 |
| `rescue` | 及時救場：在最後一刻救下要緊的人或事 |
| `reversal` | 反轉：局面在一句話或一個動作之後翻過來 |

**細綱的新欄位**（每集，`planner:chapter` 的 `body_json.episodes[]`；伺服器 `_retention_problem` 與工人 `retentionProblem` 同一套，不合 422 `video_series_doc_invalid`）：

| 欄位 | 規則 |
| --- | --- |
| `hook_type` | `HOOK_TYPES` 之一：`question`、`danger`、`image`、`line`、`reversal` |
| `lead_arc` | `LEAD_ARCS` 之一：`wins`、`suffers`、`mixed`；相鄰兩集不能都是 `suffers` |
| `satisfaction` | `[{beat, type}]` 至少 2 筆；`beat` ∈ `BEATS`（`opening`、`first_half`、`midpoint`、`second_half`、`ending`）、`type` ∈ 題材的爽點 id；第一筆在 `opening` 或 `first_half` |
| `payoffs` | 任何連續 4 集裡至少 1 集有回收 |

原有的 `hook`、`conflict`、`turn`、`cliffhanger {type, text}`、`setups`／`payoffs`、`tension`（五個 1–5，結尾 ≥ 4）、相鄰懸念類型不同，照 `SERIES.md`。工人寫進 `brief.md` 的「幕」多了「爽點：〈節拍｜類型〉」「主角走向」，合集模式再多一行「冷開場」。查核 `verifier:episode` 多回 `coverage.satisfaction` 與 `retention: {hook_line, satisfaction_lines, cliffhanger_line}`。

## 題材預設（`GENRE_SPECS`；伺服器 `GENRE_LABELS` 同名）

| id | label | 節奏規格 | 主角 | 衝突引擎（摘要） | 標題公式 | 不做的事 |
| --- | --- | --- | --- | --- | --- | --- |
| `xianxia-bonds` | 仙俠羈絆 | 否（保留今天的提示詞） | 雙男主／男／女 | 正道與魔道的界線不在人們說的地方；每個門派都藏著想要的東西；力量有沒人願付的代價 | 《作品名》第 N 集：一句話的懸念 | 借用既有作品的人名、門派、術語；說教；血腥 |
| `rebirth-revenge` | 重生復仇 | 是 | 女／男 | 背叛她的人還對她笑；她需要他們的信任才走得到他們倒下的那一刻；每一步都誘惑她提早出手再輸一次 | 重生回{關鍵時點}，{主角}覺醒{逆天能力}，{具體爽點}，{背叛者}還在做夢，她已磨好刀 | 主角忘記前世；背叛者一集就死；說教；性暗示；血腥 |
| `system-game` | 系統遊戲 | 是 | 女／男 | 主角每升一級都被想要她力量或性命的公會盯著；系統的隱藏規則是不讀規則者的陷阱；盟友在 boss 出現前都是對手 | {開服／降臨的一天}，{主角}覺醒{逆天天賦}，{轉職／速通／首殺}，{對手}還在{做夢／排隊}，她已{具體爽點} | 借用真實遊戲的名稱、道具、地圖；數字灌水到看不懂；說教 |
| `urban-return` | 都市歸來 | 是 | 男／女 | 把他看扁的人不知道自己需要他；每次亮身份都燒掉一座橋；把他送走的敵人還在城裡 | {幾年}後{主角}歸來，{看不起他的人}還在{嘲笑}，{身份／實力}一亮，{具體爽點} | 真實企業、政府、軍隊的名稱；羞辱女性；說教 |
| `empress-rise` | 女帝崛起 | 是 | 女 | 每個盟友都有價碼；每往上一步都把舊友變成新敵；王座要她發誓不給的東西 | {被當棋子的她}{覺醒／重生}，{反殺／平反}，{對手}還在做夢，她已{登上／握住}{位置} | 借用真實朝代的人物；性暗示；說教 |
| `custom` | 自訂 | 是 | 女／男／雙男主 | 從站主的前提推：誰要什麼、什麼擋著、代價是什麼；不加任何與前提矛盾的設定 | {開場設定}，{主角}{覺醒／歸來／重生}，{具體爽點}，{對手}還在做夢 | 借用既有作品；說教 |

每個題材另有 `premise_seed`（前提留白時企劃從它起筆）、`tropes`（觀眾為之而來的套路）、`thumbnail_formula`（縮圖公式：主角的臉占三分之一、四到六個大字）。`SERIES_COMMON` 不再寫死仙俠：依 payload 的 `series.genre`、`lead` 描述作品，題材段落接在最後。

## 畫面等級（`tools/video/core/drama.mjs`、`media/clips.mjs`、`assemble/drama.mjs`、`core/lint.mjs`）

| 等級 | 片段比例上限 `TIER_CLIP_SHARE_MAX` | 30 鏡一集最多幾個 clip | 提示詞 `VISUAL_TIER_RULES` | 報價比例 `TIER_CLIP_SHARE` |
| --- | --- | --- | --- | --- |
| `clips` | 1 | 30 | 每鏡都是片段；`visual` 可省 | 1.0 |
| `hybrid` | 0.4 | 12（`ceil(0.4 × 30)`） | 最多四成 `visual: "clip"`，留給每個節拍的高潮：那一巴掌、揭露、出手、變臉；其餘 `visual: "still"` 並寫 `camera` | 0.4 |
| `stills` | 0.1 | 3 | 最多一成 clip，一篇一個高潮；其餘 still | 0.1 |

- **`visual` 欄位**：鏡頭 `data.visual` ∈ `VISUAL_MODES = ["clip", "still"]`，預設 `clip`（`shotVisual`）。`clipShotScenes`／`stillShotScenes` 分兩堆；`clipsHash` 只算 clip 鏡頭。
- **lint**（`core/lint.mjs`）從 `docs/videos/<slug>/series.json` 的 `visual_tier` 讀等級（`draftEpisode` 從作品寫進去；沒有就不檢查）：超過上限是錯誤（`visualTierProblems`），`clips` 等級裡出現 still 只警告。合集模式（`series.json` 的 `compilation` 為真）第一個場景是 `title` 卡也是錯誤：冷開場。
- **`clips`**（`media/clips.mjs`）只為 clip 鏡頭生成；still 鏡頭在 manifest 記 `{ still: true, file, sha256 }` 指向它的關鍵影格（要通過 judge，`needs_review` 的不收），什麼都不買；`--dry-run` 分開印兩堆。全部是 still 也寫 manifest。
- **`assemble`**（`assemble/drama.mjs`）：`layoutDrama` 對 still 鏡頭回 `kind: "motion"`、關鍵影格與 `move: motionMove(data)`。`motionSegmentArgs`：`-loop 1 -framerate 30 -t <秒> -i keyframe` → `scale` 放大 1.25 倍（`MOTION_SOURCE_SCALE`，裁切窗永遠不小於輸出）→ `zoompan=z=…:x=…:y=…:d=1:s=1920x1080:fps=30`（表達式用 `on`／(frames−1)，最後一格剛好到位）→ `scale=1920:1080:out_color_matrix=bt709:out_range=tv,format=yuv420p`（關鍵影格是 RGB 的 PNG，沒有色彩描述；這一步指明用 BT.709 矩陣轉 YUV，跟投影片路線一樣，否則 swscale 預設用 BT.601 轉、再被標成 BT.709，still 會比旁邊的片段偏色）→ `trim=end_frame` → 字幕條、溶接、`COLOUR` 與片段段完全相同，x264 參數相同，所以 `-c copy` 串接不變；獨立 `MOTION_ENCODER_VERSION = "x264-high-crf18-film-g60-bf2-bt709-motion-v2"`；`motionSegmentKey` 含關鍵影格雜湊、運鏡、字幕、溶接。幅度刻意小：push／pull 10%（`MOTION_ZOOM`）、pan／tilt 固定 1.08 倍（`MOTION_PAN_ZOOM`）、drift 4%（`MOTION_DRIFT_ZOOM`）——still 要像有生命的持鏡，不像運鏡。
- **運鏡關鍵字**（`motionMove`：先看 `camera` 再看 `motion`，第一個命中的算，都沒有就 `drift`）。運鏡以**畫面看起來怎麼動**命名，所以 pan 跟攝影機用語相反、tilt 保留攝影機用語：

| 運鏡 | 命中的字（小寫） | 第 0 格是原圖 |
| --- | --- | --- |
| `push-in` | push、dolly in、zoom in、closer、move in | 是 |
| `pull-out` | pull、zoom out、widen、back away | 否 |
| `pan-right`（畫面往左跑，攝影機向左搖） | pan left、pan to the left、left to right | 否 |
| `pan-left`（攝影機向右搖） | pan right、pan to the right、right to left | 否 |
| `tilt-up` | tilt up、crane up、rise | 否 |
| `tilt-down` | tilt down、crane down、descend | 否 |
| `drift`（預設） | 其他 | 是 |

- **檢查**（`assemble/cli.mjs`）：`push-in` 與 `drift` 第 0 格是整張關鍵影格（zoom 1.0），用 `motionFramePsnrArgs` 直接對畫面鏈算 PSNR（≥ 22 成立）；其他運鏡跳過 PSNR、只驗格數；motion 鏡頭不會凍格；`checks.json.metrics.shots` 記 `kind: "motion"` 與 `move`。
- **成本**：一鏡 6 秒的片段約 US$0.90（Omni）＋關鍵影格 US$0.134；still 只有關鍵影格。混合一集 30 鏡約 12 個 clip，片段費從約 US$40 降到約 US$16。

## 合集（`tools/video/core/compilation.mjs`、`tools/video/compile/`、`automation/compilation.mjs`）

**文件** `docs/videos/<作品>-full/video.json`（`compilationDocument` 建、`validateCompilation` 驗；schema 頂層允許 `compilation`）：

```json
{"schema_version": 1, "slug": "<作品>-full", "format": "drama", "voice": {…},
 "compilation": {"series": "<作品>", "episodes": ["<作品>-e001", …], "chapter_cards": true, "outro": true, "titles": {"<作品>-e001": "…"}, "numbers": {…}},
 "youtube": {"category_id": 24, "made_for_kids": false, "default_language": "zh-TW", "title": "（合集標題待企劃）", "description": "（合集說明待企劃）", "tags": [], "video_id": null},
 "thumbnail": {"template": "thumb", "data": {"headline": "（待企劃）", "shot": "thumb"}},
 "scenes": [{"id": "card-1", "template": "chapter", "chapter": "第 1 集 〈標題〉", …}, …, {"id": "outro", "template": "outro", "data": {"title": "全集完", "cta": "每一集都在頻道裡"}}]}
```

合集是「有卡片與縮圖的漫劇」：不能有 `characters`、`look`、`music`、`series`、鏡頭場景，不能 `burn_in`（每集成片已燒錄）；場景由 `compilation` 區塊推出（每集一張 `chapter` 卡 `card-<N>`「第 N 集 〈標題〉」，最後一張 `outro`），`numbers` 讓跳過的集數留空號。章節卡 2 秒（`CARD_FRAMES = 60`）、片尾 4 秒（`OUTRO_FRAMES = 120`）；`chapter_cards: false`／`outro: false` 就不放。`category_id` 是 24（娛樂），不是教學片的 28。`lintCompilation` 對佔位標題只警告（工人先建文件再由企劃命名；`status` 會等）。

**步驟** `COMPILATION_STEPS`（`core/state.mjs` 的 `stepsFor(doc)`；後台標籤在 `review/sync.mjs` 的 `STEP_LABELS`）：

| 步驟 | 誰 | 做什麼 |
| --- | --- | --- |
| `metadata planned`（合集標題與說明） | 工人 `planMetadata` → 企劃模型 variant `planner:compilation` | payload：作品、`genre_spec`、每集（編號、標題、一句話、前情）、`description_budget_bytes`、`thumbnail_candidates`（前 3 集有人物在框內、judge 分最高的關鍵影格，最多 12 張）。答案：`title`（≤ 100 字、無角括號、照題材標題公式）、`titles`（兩個備案）、`description`（≤ 預算）、`tags`（合計 ≤ 500 字，含 漫劇、AI漫劇、一口氣看完）、`thumbnail {headline ≤ 12 字, tag ≤ 6 字或 null, episode, shot}`。工人寫進 `youtube` 與 `thumbnail`，把選中的關鍵影格複製到 `<工作區>/keyframes/thumb-source.png` 並登記在 `keyframes/manifest.json` 的 `shots.thumb`，另存 `metadata-plan.json`（三個標題案）；lint 不過就下一輪再試 |
| `cards rendered`（章節卡與縮圖） | `render` | 章節卡與 outro 的畫面、`thumbnail.jpg`（`thumb` 版型畫在 `thumb-source.png` 上；沒有候選就畫在主題底色上） |
| `video compiled`（合集串接） | `compile` | 下面 |
| `metadata translated`（五語標題與說明） | 工人 `translateMetadata` → 翻譯模型 variant `translator:compilation` | 每個語系一次：`i18n/<locale>.json` 的 `title`、`description`、`tags`、`chapters`（鍵是每集 slug） |
| `final video approved` → `upload package` → `on YouTube` | 沿用 | `qa`（6 項）→ `review-push --gate final`（自動核准）→ `package` → `review-push --gate publish`（自動核准，進「可以上架」）→ 站主貼網址 → 工人 `POST …/compilation/done` |

`advanceCompilation` 對 `compile` 的結束碼：4 下一輪再試；其餘非 0 卡住（理由寫在審核頁）。

**`compile` 指令**（`node tools/video/cli.mjs compile --slug <作品>-full [--workdir D] [--force] [--dry-run]`）：

| 讀 | 條件 |
| --- | --- |
| `docs/videos/<作品>-full/video.json` | 有 `compilation` 區塊、lint 零錯誤 |
| 每集 `<工作區>/<集>/final.mp4` | 雜湊等於 `approvals.json` 最後一筆 `final` 核准的雜湊（量測，不信任）；`checks.json.ok`；`timeline.json.total_frames` |
| `<工作區>/<作品>-full/frames/manifest.json` | `visual_hash` 等於文件的（章節卡改了要先 `render`） |
| 磁碟 | 空間 ≥ 每集成片總量 × 1.5 ＋ 2.5 GB（`DISK_FACTOR`、`DISK_RESERVE_BYTES`） |

| 寫（`<工作區>/<作品>-full/`） | 內容 |
| --- | --- |
| `segments/<card>-<key>.mp4` | 每張卡的靜態片段（`segmentArgs`，投影片編碼參數，可 `-c copy`），以 key 快取，改過的卡刪舊段 |
| `build/join.ffconcat`、`build/final.partial.mp4` | ffconcat `[card-1][e001][card-2][e002]…[outro]`；影像 `-c copy`；音訊每個輸入 `atrim`／`apad` 到剛好等於格數 × 1,600 個取樣（AAC 每段會多出最多 3 格，40 段抄過去會漂 0.1 秒），卡片用 `anullsrc` 靜音，`concat` 後只重編一次 AAC 384k 48 kHz，faststart（`joinArgs`） |
| `final.mp4` | 成片。沒有片頭卡（冷開場＝第 1 集第一鏡的鉤子），結尾是第 N 集的懸念接 outro |
| `checks.json` | `{ok, compilation_hash, visual_hash, problems, metrics: {frames, loudness, episodes: [{slug, start_frame, frames, sha256}]}, ffmpeg, encoded_segments, seconds}`：`ffprobe` 總格數＝Σ；響度 −14 ± 1.5 LU（`LOUDNESS_TOLERANCE_LU`，每集已各自正規化，不重做）；真峰值 ≤ −0.5 dBTP |
| `captions/<locale>.srt`、`.vtt`、`captions/manifest.json` | `mergeCaptions`：每集 `captions/<locale>.srt` 的 cue 依起始格位移（`frameToMs`）；`manifest` 記 `compilation_hash`、每語系 cue 數與重疊問題、`skipped`（哪些集沒有那個語系的字幕檔） |
| `compile/manifest.json` | `{compilation_hash, visual_hash, total_frames, layout, chapters, episodes}` |
| `timeline.json` | `compilationTimeline`：只有章節與總長，沒有句子（`speech_hash: null`），加 `compilation_hash` |

`compilation_hash` = 每集 (slug, sha256) 序列 ＋ `chapter_cards` ＋ `outro`：某一集在核准後重剪，合集就過期。結束碼：0 完成（含被 `STOP` 檔停下，重跑接續）；1 lint 錯誤或 `checks.json` 沒過；2 不是合集、某集未清、`frames` 過期、卡片沒畫；3 磁碟不夠；5 沒有 ffmpeg。`--dry-run` 印每段的時鐘與長度、每集雜湊與磁碟結論。

**章節**：一集一章，從它的章節卡開始（沒卡就從成片開始），取整秒（`chapterList`）；標題「第 N 集 〈集名〉」，集名 ≤ 40 字（`TITLE_MAX_CHARS`）。

**說明欄位元組預算**：YouTube 5,000 位元組；每章一行約 150 位元組（`CHAPTER_LINE_BYTES`）、工具自己的行保留 400（`DESCRIPTION_RESERVE_BYTES`）→ 企劃的本文預算 `descriptionBudget(n) = max(500, 5000 − 400 − 150 n)`，40 集就是 500 位元組（約 166 個中文字，只寫得下「這是什麼故事、給誰看」）。組說明時仍超過 5,000，`descriptionWithinBudget` 把每章標題退成「第 N 集」（en「Episode N」、ja「第N話」、ko「N화」）並警告；`checkYoutubeFields` 最後把關。

**品管與上架**：`qa --slug <作品>-full` 走 `COMPILATION_ITEM_IDS` 六項（assemble＝checks 對上這批成片與卡片；captions＝五語都合併且翻譯沒過期；metadata＝每語系上限與章節；links；thumbnail；disclosure），報告帶 `kind: "compilation"`。`review-push --gate final` 的 720p 預覽對合集加 `-maxrate 2M -bufsize 4M`（`previewArgs`；兩小時約 ≤ 2 GB，所以 `VIDEO_REVIEW_MAX_FILE_BYTES` 要調到 2.5 GB）。`package` 把 `final.mp4` 硬連結（連不到才複製）進 `upload/`，`metadata.json` 多 `compilation: true`、`download: "upload/final.mp4"`、`size_bytes`、`episodes`，`UPLOAD.md` 多一節「合集」（幾集、幾 GB、到「可以上架」卡下載）。`review-push --gate publish` 不上傳 `final.mp4`，payload 多 `download: {path, bytes, sha256}` 與 `episodes`，摘要寫「合集 X GB，成片從網站下載後上傳」；工人回報影片時只帶 `series_slug`（沒有 `episode_number`），後台因此認得它是合集。

## 後台（`apps/web/components/admin-video-series.tsx`、`admin-video-review-card.tsx`）

- **一鍵開拍**（`NewBingeForm`，漫劇分頁最上面）：題材六張卡（名稱＋一句話）、主角（女主／男主／雙男主）、故事前提（選填；自訂必填）、總長度（30–480，預設 120）、每集分鐘（2–4）、畫面做法（全片段／混合／靜圖，各一句說明）、風格預設、備註；改動 300 ms 後向 `binge-quote` 要估算，顯示「N 集，M 篇（每篇 K 集）· 片段 S 秒 · 圖片 I 張 · 約 US$X」與四條預算，不夠的標紅並寫「先到設定分頁調高」；按「一鍵開拍」→ `POST …/series`（`hands_off: true`、`compilation: true`、`open_ended: false`）→ 開作品頁。
- **作品卡與作品頁**（`BingePills`）：題材、畫面等級、「免關卡」、合集狀態（等每集完成／等工人開始／製作中／完成）、「共 N 分鐘」。作品頁多「免關卡」勾選（`PATCH` `hands_off`，關掉就回到逐份核准）、完結後「做合集」（`POST …/actions/compile`）。文件區塊照舊顯示每版的備註，所以自動核准的裁決與退回理由（「查核：…」「[auto] 查核沒過：…」）都看得到。
- **合集區**：合集影片的標題、目前步驟（`STEP_LABELS`）、待站主數、「開影片」，以及 `CompilationDownload`：`download_available` 時「下載 1080p 成片」（`/api/admin-video-download/<slug>`），否則「成片還在工人的工作區」。
- **可以上架**：合集的卡片寫「作品 X 的合集」，同一個下載連結；上傳包的其他檔（縮圖、五語字幕與說明）照舊從審核檔案區下載。
- **設定**：`series_max_in_flight` 上限 6（`SERIES_IN_FLIGHT_MAX`）。
- 字串在 `admin.videoSeries.binge.*`、`genres.*`、`leads.*`、`tiers.*`、`compilation*`、`admin.videoReviews.downloadCompilation` 等，五語都有（`npm run check:i18n`）。

## 主機（`docker-compose.prod.yml`、`.env.example`）

| 項目 | 值 |
| --- | --- |
| `api` 掛載 | `video_work:/var/lib/mokaair/video-work:ro`（工人的工作區，唯讀；API 只讀 `<slug>/upload/final.mp4`） |
| `api` 環境變數 | `VIDEO_WORK_DIR=/var/lib/mokaair/video-work` |
| `.env` | `VIDEO_REVIEW_MAX_FILE_BYTES=2500000000`（合集 720p 預覽）、`VIDEO_REVIEW_MAX_TOTAL_BYTES=30000000000`、`VIDEO_WORK_DIR` |
| 工人 | 不變：串接是串流，3 GB 記憶體夠；沒有 GPU 也不用 minterpolate |

**磁碟估計（120 分鐘、40 集；試作後改）**：每集成片（CRF 18、1080p、3 分鐘）約 150–250 MB → 40 集 6–10 GB；`compile` 需要成片總量 × 1.5 ＋ 2.5 GB 的空位（`final.mp4` 與 partial 各一份、段、預覽、硬連結失敗時的複製）；720p 預覽 ≤ 2 GB 進審核檔案區；合集工作區完成後約 6–10 GB（`final.mp4` 與 `upload/` 是同一個 inode）。合計約 **25 GB／兩小時**。每集的工作區另外各 1.5–2 GB（`DRAMA.md` 的估計：關鍵影格、片段、音檔），上架後既有的清理只刪審核檔案區的 mp4，不動 `video_work`——磁碟要靠試作觀察（票 P8）。

## 成本與吞吐（120 分鐘、40 集 × 3 分鐘；`binge_quote` 的算法與 DRAMA.md 單價）

| 等級 | 片段秒（× 1.5 重做） | 每部媒體費 | 每月片段預算至少 | 機器時間（`series_max_in_flight` 3，估計） |
| --- | --- | --- | --- | --- |
| `clips` | 10,800 | 約 US$1,900（片段 1,620、圖片 211、judge 24、其餘 40） | 12,000 | 2–4 天 |
| **`hybrid`（選定）** | 4,320 | 約 US$916（片段 648、圖片 211、judge 17、其餘 40） | 6,000 | 1–2 天 |
| `stills` | 1,080 | 約 US$430（片段 162、圖片 211、judge 13、其餘 40） | 現有 3,000 夠 | 約 1 天 |

站主按按鈕前要在設定分頁調（報價會把不足的項目標紅）：

| 設定 | 預設 | 調成 | 為什麼 |
| --- | --- | --- | --- |
| `monthly_clip_seconds_budget` | 3,000 | 6,000 | hybrid 一部 4,320 秒 |
| `monthly_images_budget` | 1,500 | 3,000 | 一部 1,578 張 |
| `series_episodes_per_month` | 30 | 60 | 一部 40 集，一個月內做完 |
| `series_max_in_flight` | 1 | 3 | 同時做三集，機器時間從 3–4 天壓到 1–2 天 |
| `max_waiting_drafts` | 3 | ≥ 4 | 工人的 `room()` 用它算「還能不能再開一支」，進行中的集數也算在內，要比 in-flight 大 |
| `monthly_judge_calls_budget` | 3,000 | 不用調 | 一部 1,698 次 |

模型呼叫走訂閱帳號不另計費（每集撰稿 1–3 次、查核 1–2 次、聽眾 1 次、前情 1 次；每份文件企劃 1 次＋裁決 1 次；合集企劃 1 次＋翻譯 4 次）。

## 風險與對策

| 風險 | 對策 |
| --- | --- |
| YouTube 非原創／量產內容政策 | 站主仍是作者（選題材、寫前提、隨時可暫停或退回）；每集有劇本、細綱、裁決紀錄與 audit 當作者證據；合成內容揭露一律勾；提示詞明寫原創，查核出 `similar_works` 就退回；每集劇情獨立，不是換名字的模板 |
| 查核誤放行 | 門檻常數（`有／弱／無`、`弱` ≤ 1、零問題、8 秒、30 秒、2 個爽點）寫在 `judge.py`、`series.mjs` 與這份文件；試作後對照站主自己會不會過來調；站主可把作品的「免關卡」關掉回到人審 |
| 兩小時檔案 | 成片 6–10 GB 不進審核檔案區，只放 720p 壓縮預覽（≤ 2 GB）；1080p 從 API 唯讀掛載的 `video_work` 串流下載；`compile` 先算磁碟（不夠結束碼 3，理由寫在審核頁） |
| 預算用完卡在中途 | 伺服器 429 → 工人結束該輪、下一輪再試，作品不會壞；報價先把不足標紅；表單寫「調高之後自動繼續」 |
| 卡住的影片要人處理 | 合集模式一集卡住會停住整部（下一集等前一集 done）；作品頁與影片頁顯示原因；既有票 `2026-09-27-a-blocked-video-can-only-be`（「再試一次」）與本案獨立 |
| 說明欄 5,000 位元組 | 40 章節約 6,000 位元組已超標：企劃本文限 `descriptionBudget`（40 集＝500 位元組），組合時超標退成「第 N 集」，`checkYoutubeFields` 最後擋 |
| 某集在核准後重剪 | `compilation_hash` 含每集 sha，`compile` 量測每集雜湊對 `approvals.json`，不對就結束碼 2；`qa` 的 assemble 項與 `package` 都會發現 |
| 舊作品被波及 | 預設值等於舊行為；`xianxia-bonds` 沒有節奏規格；沒有 `series.json` 的 `visual_tier` 就不檢查等級 |

## 實作與原計畫不同的地方

- 裁決不是 0–10 分數，而是每項「有／弱／無」（跟劇本 `coverage` 同一套字），門檻是「沒有無、弱 ≤ 1、零問題」。
- 沒有另開 `POST …/series/binge` 端點：`SeriesIn` 直接多欄位，`total_minutes` 有值就走一鍵的算法；`total_minutes` 範圍 30–480；`lead` 是 `female|male|dual-male`。
- 劇本沒有 `final_round` 放寬規則：工人在送審前自己判並修（最多 `MAX_PROMPT_FIX_ROUNDS` 輪），送上去不過就留給站主。
- 合集有片尾 4 秒 outro 卡（可關），`category_id` 24；預覽是 `-crf 26 -maxrate 2M -bufsize 4M`。
- 合集工作從作品 `finished` 出發，`finish_episode` 照舊把作品設成 `finished`。
- 提示詞鏡射檔叫 `verifier-series-doc.md` 與 `planner-compilation.md`。

## 票（`tasks/`，scope 互不重疊）

| # | 票 | area | scope | 狀態（2026-09-27） |
| --- | --- | --- | --- | --- |
| A1 | `2026-09-27-video-binge-api` | api | `apps/api/app/video_automation`、`apps/api/app/video_reviews`、`apps/api/app/config.py`、遷移 0102、對應測試 | done |
| T2 | `2026-09-27-video-binge-worker` | tools | `tools/video/automation` | in-progress |
| T3 | `2026-09-27-video-binge-visual-tier` | tools | `tools/video/core/drama.mjs`、`lint.mjs`、fixtures、`tools/video/media/clips.mjs`、`tools/video/assemble` | in-progress |
| T4 | `2026-09-27-video-binge-compile` | tools | `tools/video/compile`、`tools/video/cli.mjs`、`core/state.mjs`、`core/schema.mjs`、`tools/video/qa`、`package`、`review` | in-progress |
| W5 | `2026-09-27-video-binge-web` | web | `apps/web/components/admin-video-series*`、`admin-video-reviews*`、`admin-video-review-card.tsx`、`admin-video-drama-settings.tsx`、`apps/web/app/api/admin-video-download`、`apps/web/app/api/video/automation/series`、`apps/web/messages` | in-progress |
| O6 | `2026-09-27-video-binge-ops` | ops | `docker-compose.prod.yml`、`.env.example` | done |
| D7 | `2026-09-27-video-binge-docs` | docs | `docs/videos`、`.agents/skills/youtube-video`、`.claude/skills/youtube-video` | 這份 |
| P8 | `2026-09-27-video-binge-pilot` | docs | `docs/videos/BINGE.md`（把實測數字寫回） | open，部署後 |

順序：A1 → T2（靠 A1 的端點契約）；T3、T4 與 A1 平行；W5 靠 A1；O6、D7 隨時；P8 部署後。部署走 `deploy` skill，是合併後另一步。

## 試作計畫（票 P8）

1. 設定分頁調上面那六個數字；確認 `.env` 的 `VIDEO_REVIEW_MAX_FILE_BYTES`、`VIDEO_WORK_DIR` 與 `api` 的掛載都在（`deploy` 之後）。
2. **30 分鐘 `stills`**（10 集、1 篇）：題材選重生復仇、女主、前提留白。看作品頁每份文件的裁決與備註（有沒有被退回、退了幾次、理由對不對）、每集的 `coverage` 與 `retention` 數字、劇本被工人自己修了幾輪、still 鏡頭的運鏡看起來如何、每集實際花費與機器時間；合集出現在「可以上架」後下載 1080p、Studio 上傳私人、貼網址。
3. **120 分鐘 `hybrid`**（40 集、4 篇）：同上，另記磁碟（`video_work` 的用量、`compile` 的空位結論）、`compile` 花的秒數、720p 預覽大小、說明欄退成「第 N 集」了沒。
4. 把數字寫回這份文件的成本表與磁碟估計；對照站主自己會不會核准那些文件與劇本，決定門檻常數要不要動。
