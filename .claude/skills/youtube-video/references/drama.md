# AI 漫劇路線：角色設定圖、關鍵影格、圖生影片、多角色配音、可開關CC、配樂

這條路線的成品是一支像《山海经之万兽圖鉴》那樣的 AI 動畫劇：每個鏡頭是一段 AI 生成的動態片段（先出關鍵影格，再圖生影片），旁白加多個角色配音，不燒錄字幕，有背景音樂與可開關繁中 CC；其他語言的標題說明與 CC 依核定範圍製作（下面第 14 步）。設計與為什麼這樣做在 `docs/videos/DRAMA.md`，單集與作品走同一條流程的設計在 `docs/videos/DRAMA-FLOW.md`；這份只寫**怎麼做**。投影片路線的共通部分（一次性設定、發音字典、CC 翻譯、上架包）在 `.agents/skills/youtube-video/references/automated.md`，作品多做的事（設定集、總綱、篇章細綱、討論串、一致性）在 `references/series.md`，這裡不重複。

**單集就是一集的作品**：「新的漫劇」表單建立的是一部 `kind = one-off` 的作品，只有一集、只有一份文件——**故事聖經**（doc kind `bible`）。作品（`kind = series`）的文件是設定集 → 總綱 → 每篇細綱。之後每一集的步驟一樣。

站主把關的關卡只有兩個，都可以先討論再核准：

1. **文件**：單集的故事聖經；作品的設定集、總綱、每篇細綱。在 `/admin/videos` 的「漫劇」分頁核准，每份文件有一條討論串（subject `bible`、`setting`、`outline`、`chapter:<n>`）：站主寫一句話，工人下一輪讓企劃模型回覆或出新版本，滿意了才核准。
2. **劇本**（`script`）：稿子通過檢查與連貫性查核、聽眾審稿之後，工人寫 `script.md` 並 `review-push --gate script`；站主在影片頁的劇本卡片讀、討論（subject `script:<集數>`）、核准。這一關在任何設定圖或片段花錢**之前**。漫劇設定的「劇本先給我看」（`series_script_gate`）關著時，工人在本機核准（備註「「劇本先給我看」關著，依設定自動核准」）。

之後四關自動決定（`docs/videos/HANDS-OFF.md`），沒過的才在 `/admin/videos` 找站主：設定圖 `look`（`auto_pick_look`：judge 最高分達門檻、沒有問題就核准該角色）、旁白 `audio`（Jev 全過就核准，`drama_auto_approve_audio`）、分鏡 `storyboard`（`auto_approve_storyboard` 開著且 judge 全過）、成片 `final`（自動品管，`drama_auto_approve_final`）。上架確認（`publish`）與語言（`languages`）照投影片路線。

漫劇**沒有「選大綱」卡片**：`brief.md` 由工人從核准的文件寫出，`## 大綱` 只有選項 A，`outline` 關卡在本機直接核准（單集備註「依故事聖經」，作品的集備註 `planned by chapter <n>'s approved outline`）。Jev 挑大綱與 `auto_pick_outline` 只管教學影片。

關卡都在 `/admin/videos` 做，工具用 `review-push --gate <關卡>` 送、`review-pull` 讀回；核准綁檔案雜湊。


2026-10-01 十部動畫使用 [animation-production.md](animation-production.md) 與 source-bound `production-design.json`：`subtitles.burn_in: false`、先完成 zh-TW 台灣口音正片再做 ja/ko/en 音軌與各自 CC；目前漫劇多語角色配音尚未實作，不宣稱已可自動產出。此批 `production.profile.visual_tier: clips`，每鏡最多 8 秒且不得用 still/凍結補秒。下文 still/hybrid 與較長鏡頭只是其他既有路線能力。

## 一次性設定（站主做）

| 項目 | 怎麼做 | 沒做會怎樣 |
| --- | --- | --- |
| 開啟漫劇 | 後台「影片審核 → 漫劇」分頁最上面的**漫劇設定**（`/admin/videos?tab=drama`）：`drama_enabled`、圖片／片段／音樂的供應商與模型、片段解析度與預設秒數、每月預算（片段秒、圖片、judge 次數、音樂首數）、單支上限 `max_usd_per_video`、judge 門檻、風格預設、角色聲音池、漫劇自己的旁白聲音與常設指示；關卡開關 `auto_pick_look`、`auto_approve_storyboard`、`drama_auto_approve_audio`、`drama_auto_approve_final`、「劇本先給我看」`series_script_gate`；文件退回後最多重寫幾輪 `series_doc_rewrites` | 「新的漫劇」與「新的作品」被 409 `video_drama_disabled` 拒絕；工人不問討論串與作品；`look`／`keyframes`／`clips`／`music` 結束碼 3 |
| 供應商金鑰 | 圖片與片段用網站既有的 Gemini 金鑰（`hotspot_guide_gemini_api_key`）；MiniMax 當第二 adapter 用 `minimax_api_key`。金鑰只在 API 容器 | `media-status` 顯示 NO KEY |
| 影片工具權杖、ffmpeg、瀏覽器 | 同投影片路線（`automated.md` 的一次性設定）；`look`／`keyframes` 的聯絡表也用瀏覽器畫，沒有瀏覽器只會少一張聯絡表 | — |
| 站主自帶的音樂 | 放在 `<VIDEO_WORKDIR>/_music/<檔名>`（mp3／m4a／wav／flac），`video.json` 寫 `music.track`，有 `music.sha256` 就核對 | `music` 結束碼 3 |

`node tools/video/cli.mjs media-status --slug <SLUG>` 印出伺服器目前的供應商、預算、儲存空間，以及這支影片到目前為止的花費。

## 主幹

`status --slug <SLUG>` 列的是漫劇的 19 步（`tools/video/core/state.mjs` 的 `DRAMA_STEPS`；`fact-checked` 之後是 `script approved`；沒有 `music` 的影片少一步）。工人（`node tools/video/cli.mjs auto`）照這個順序自己跑；代理手動做一支時也照它。

有角色的漫劇，每一集撰稿前讀 `.agents/skills/youtube-video/references/drama-craft.md`（開場、鏡位與剪點、鏡頭與台詞長度的規格），`lint` 之後跑 `node .agents/skills/youtube-video/scripts/drama_craft_check.mjs <VIDEO_DOCS>/video.json`：沒過的項目改掉，或在回報裡逐項寫這一集為什麼不同；查核改完再跑一次。它量的是分鏡的結構，不擋任何指令、不改任何指令的結束碼；沒有角色的漫劇（解說、品牌故事）它會說明並跳過。

首次選定美術方向、製作代表 pilot 或收到「粗糙／沒有吸引力」的回饋時，先用 `.agents/skills/youtube-video/references/visual-quality.md` 檢查美術、表演、鏡頭與聲畫節奏。角色圖只是身份參考；首格無變形、片段可解碼與 judge 過線仍不足以放量。既有流程可在授權內繼續修正；只把需要使用者決定的風格、品質取捨或預算問題交給使用者，不逐鏡新增確認。

| # | 階段 | 誰 | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 1 | 文件：單集由企劃模型（variant `bible`，提示 `.agents/skills/youtube-video/references/prompts/series-bible.md`）寫**故事聖經**（前提、角色、幕、一個大綱、素材、不做的事）→ `POST /video/automation/series/<slug>/docs`（`kind: "bible"`）；作品是設定集 → 總綱 → 篇章細綱（`series.md`）。核准後那一集變 `ready`，工人 `POST …/series/<slug>/episodes/<n>/start`，寫 `<VIDEO_DOCS>/series.json`（人物表、本集細綱、前情、設定全文）與 `brief.md` | 企劃模型、工人 | 站上的文件版本；`<VIDEO_DOCS>/series.json`、`brief.md`（章節「故事前提」「角色」「站主觀點」是 lint 要求的；工人另寫 `## 幕` 與 `## 大綱`，`## 大綱` 只有選項 A，`outline` 關卡讀它） | **站主核准故事聖經**（先在討論串問或要求改也可以；subject `bible`）；退回帶備註最多 `series_doc_rewrites` 輪，討論出的新版本不算；`outline` 關卡由工人本機核准，備註「依故事聖經」 |
| 2 | 撰稿：劇本與分鏡表（提示 `prompts/writer-drama.md`；作品的集用 variant `episode`） | 撰稿代理 | `video.json`（`format: "drama"`）、`claims.md`（改編時） | `lint` 零錯誤：每鏡 ≤ 12 秒、一句一個說話者、角色 ≤ 3；角色逐字沿用文件的人物表 |
| 3 | 查核：連貫性與設定一致（提示 `prompts/verifier-drama.md`）→ 聽眾審稿 | **另一個**代理 | `verify-1.md`；作品的集另有 `review/script-check.json`（`coverage`、`problems`） | 改編的事實照投影片的規矩查 |
| 4 | **劇本關卡**：`script --slug <SLUG>` 由 `video.json` 寫 `script.md`（只含場景順序與每句的 id／文字／說話者／情緒）→ `review-push --gate script`（payload 帶場景與提示詞、人物、`beats`、`coverage`、`continuity_problems`） | 工具、站主 | `<VIDEO_DOCS>/script.md` | **站主讀劇本、討論（subject `script:<集數>`）、核准** → `review-pull`。「劇本先給我看」關著時工人本機核准。退回：撰稿模型 FIX 模式重寫，重跑查核與聽眾審稿再送，`MAX_PROMPT_FIX_ROUNDS` 輪後卡住；討論要求改：撰稿模型（variant `discuss`）改 `video.json`，過 lint 後同樣重跑查核與聽眾審稿、再送一次，沒有輪數上限 |
| 5 | `look`：每角色幾張設定圖，judge 打分，聯絡表；作品有存檔就沿用，只畫新角色 | 工具 | `characters/manifest.json`、`characters/<角色>/*.png` | `review-push --gate look`（每角色一張審核）；`auto_pick_look` 開著就核准 judge 建議的那張，沒過或關著才**由站主選一張**；`review-pull` 寫 `characters/choice.json` 並記核准 |
| 6 | `tts`：依說話者分批，情緒併進 Gemini 的 style | 工具 | `audio/`、`narration.wav`、`timeline.json` | `--dry-run` 先看每個聲音的字數；角色聲音不在允許清單會指名角色 |
| 7 | `check-audio` → `review-push --gate audio` | 工具 | `review/check-flags.json` | Jev 全過就自動核准（`drama_auto_approve_audio`）；還有被標的句子才由站主核准旁白 |
| 8 | `keyframes`：每鏡一張 1920×1080，參考選定的設定圖，judge 不過換 seed（最多 3 次） | 工具 | `keyframes/manifest.json`、`keyframes/*.png`、聯絡表 | `review-push --gate storyboard`；`auto_approve_storyboard` 開著且 judge 全過就自動核准，否則站主看分鏡；`review-pull` |
| 9 | `render`：卡片、縮圖；只有明確使用舊burn-in版本才產字幕條（以指定鏡頭的關鍵影格當底圖） | 工具 | `frames/`（此批CC-only不含燒錄字幕條） | 缺字結束碼 1 |
| 10 | `clips`：每鏡圖生影片，ffmpeg 與 judge 品檢，不過換 seed（最多 2 次），送出前對單支上限把關 | 工具 | `clips/manifest.json`、`clips/*.mp4` | **第一支先單獨跑一鏡**看主機地區有沒有被 Gemini 擋 |
| 11 | `music`：生成或核對自帶曲子 | 工具 | `music/manifest.json` | — |
| 12 | `assemble`：片段對齊句子、轉場、音樂壓低、串接、檢查；此批只裁切足長素材，不凍格補秒、不疊字幕條；作品的集此時寫前情 `POST …/episodes/<n>/recap` | 工具 | `final.mp4`、`checks.json`（六個雜湊） | 自動檢查全過 |
| 13 | `captions`（只有繁中）、`review-push --gate final`、`package`、`review-push --gate publish`；上架確認後 `POST …/series/<slug>/episodes/<n>/done` | 同投影片路線 | `captions/`、`upload/` | 成片自動品管全過就核准（`drama_auto_approve_final`）；`UPLOAD.md` 多了合成內容揭露、劇情獨立、音樂授權三項 |
| 14 | 語言（`docs/videos/LANGUAGES.md`）：成片核准後站主在影片頁勾每個語言的標題說明與 CC（漫劇的配音是第二期，面板上灰掉；「照預設勾選」讀漫劇設定的 `drama_caption_locales`）→ 工人只做勾了的：`i18n-sheet --parts` → 翻譯與審稿代理 → `i18n-merge` → `captions` → `package` → `review-push --gate languages` | 站主、工具、翻譯代理 | `<VIDEO_DOCS>/i18n/<語系>.json`、`captions/<語系>.srt`、`upload/` | 沒有配音的批次伺服器直接核准；都做好影片才進「可以上架」。步驟細節同 `automated.md` 第 13 步 |

每個媒體階段之間都看 `STOP` 檔；中斷後重跑接著做：同一個請求不付第二次（`media/cache.json`），還在跑的伺服器工作接著輪詢（`media/jobs.json`），花費都在 `media/ledger.json`。

## 指令

```bash
node tools/video/cli.mjs media-status --slug <SLUG>
node tools/video/cli.mjs script      --slug <SLUG>                              # 由 video.json 寫 script.md（只含敘事），劇本關卡綁它的雜湊
node tools/video/cli.mjs review-push --slug <SLUG> --gate script                # 劇本關卡：站主在 /admin/videos 讀、討論、核准
node tools/video/cli.mjs review-pull --slug <SLUG>                              # 站主決定後讀回；每個關卡都用它
node tools/video/cli.mjs look      --slug <SLUG> [--candidates 3] [--character <角色 id>] [--dry-run] [--channel msedge]
node tools/video/cli.mjs look      --slug <SLUG> --choose jingwei=2,yandi=1     # judge 沒選出、後台頁又用不了時本機選圖，再 approve --gate look
node tools/video/cli.mjs tts       --slug <SLUG> --dry-run                      # 分聲音印字數與額度
node tools/video/cli.mjs keyframes --slug <SLUG> [--shot a,b] [--takes 3] [--force] [--dry-run] [--channel msedge]
node tools/video/cli.mjs render    --slug <SLUG> [--channel msedge]             # 漫劇要先有 timeline（字幕條依旁白切）與關鍵影格（縮圖底圖）
node tools/video/cli.mjs clips     --slug <SLUG> [--shot a,b] [--takes 2] [--force] [--dry-run]
node tools/video/cli.mjs music     --slug <SLUG> [--dry-run]
node tools/video/cli.mjs assemble  --slug <SLUG>
node tools/video/cli.mjs review    --slug <SLUG>                                # 也寫 review/look.html（本機看候選設定圖）
node tools/video/cli.mjs review-push --slug <SLUG> --gate outline|script|look|audio|storyboard|final|publish
node tools/video/cli.mjs approve   --slug <SLUG> --gate outline|script|look|storyboard|audio|final|publish [--note "…"]   # 後台頁不能用時的備援
node tools/video/assemble/smoke.mjs --fixture drama [--channel msedge]          # 合成替身跑 render → assemble → review → package，不碰任何服務
```

結束碼同投影片路線：1 品檢或 lint 沒過（`needs_review` 進 manifest，改提示詞再跑）；2 順序不對（例如 look 還沒核准就 `keyframes`、storyboard 還沒核准就 `clips`）；3 要站主（漫劇沒開、沒金鑰、單支上限、核准）；4 供應商或額度；5 ffmpeg 或瀏覽器沒裝。

## video.json 的重點

- `format: "drama"`；範例 `tools/video/core/fixtures/drama/video.json`（精衛填海，兩個角色、四個鏡頭、一張結尾卡）。規則在 `tools/video/core/drama.mjs`（`validateDrama`、`shotProblems`）。
- **解說片（`flat-explainer`）**：「原來如此事務所」那種一集回答一個「為什麼」的插畫解說（`docs/videos/so-thats-why/`）。後台發起漫劇時風格選「扁平插畫解說」：單集作品的故事聖經改用解說版（`planner:bible-explainer`，`characters` 為空、`outline` 有 question／answer／reasons／hook／sources，API 與工人都照這個形狀擋），brief 由聖經寫成解說版章節，撰稿與查核用 `writer:explainer`／`verifier:explainer`，撰稿順手寫 `shorts.json`（`tools/video/automation/prompts.mjs` 的 `EXPLAINER_INSTRUCTIONS`）。lint 要求 `characters: []`、每個鏡頭都是 `visual: "still"`，卡片多了 `big`、`stats`、`compare` 可放數字與對比；brief 的必填章節是「問題」「一句答案」「站主觀點」。範例 `tools/video/core/fixtures/explainer/`。
- **沒有角色的漫劇沒有 look**：`characters` 是空陣列時，`status` 不列「look generated／look approved」，審核順序跳過 look 關卡，`keyframes` 不等設定圖，直接畫；`look` 指令會拒絕並叫你跑 `keyframes`。
- `look`：`preset`（`cinematic-3d`／`anime-2d`／`ink-wash`／`flat-explainer`／`custom`）加可覆寫的 `style`、`negative`、`motion`（英文，給圖片與影片模型）、`candidates`（每角色幾張設定圖）、`style_frames`（`<VIDEO_DOCS>` 裡的參考圖）。
- `characters[]`：`id`（小寫，不可是 `narrator`）、`name`（字幕與審核頁用）、`appearance`（英文 ≤ 800 字，設定圖與每個鏡頭都用它）、`voice`（同 `voice` 的物件；Gemini 聲音才有 `style`）、`sheet_prompt`（可選）。
- `characters[].shot_looks: [{id, appearance}]`：核定的同角色命名造型目錄；`appearance`只換當前服裝、傷勢、持物等狀態，不換人物ID或聲線。`scene.data.character_looks: {characterId: lookId}`逐鏡選目錄中的造型；不造新ID。基底與命名造型都保留，同集前後換衣/摘冠/交出物件用不同鏡頭選擇，不可整集覆蓋。
- 鏡頭場景 `template: "shot"`，`data`：`prompt`（英文 ≤ 1000 字，畫面本身）、`camera`、`motion`（給圖生影片）、`characters`（≤ 3 個 id，決定參考圖與 judge 的 identity 題）、`fit`（`auto`／`freeze`／`slow`／`trim`，片段比句子短或長時怎麼對齊）、`transition`（`cut`／`dissolve`）、`start_frame: { shot, at: "last" }`（接續更早的鏡頭；目前是把上一鏡最後一格當參考圖，片段仍從自己的關鍵影格開始）、`end_frame: { prompt }`（另出一張當片段的末格）、`visual`（`clip` 預設／`still`：見下一點）。卡片場景（`title`／`chapter`／`outro`）照投影片版型。
- **`visual: "still"`**（僅其他既有路線；此批production profile拒絕still，前製animatic仍可用靜畫。長篇作品的畫面等級，設計在 `docs/videos/BINGE.md`）：這一鏡不買片段，`clips` 在 manifest 記 `{ still: true }` 指向它的關鍵影格，`assemble` 把關鍵影格做成一段慢運鏡（`zoompan`，編碼參數與片段段相同，仍 `-c copy` 串接）。運鏡由 `camera`（其次 `motion`）的關鍵字決定（`tools/video/assemble/drama.mjs` 的 `motionMove`），以**畫面看起來怎麼動**命名，所以 pan 跟攝影機用語相反：

  | 寫在 `camera` 的字 | 運鏡 | 效果 |
  | --- | --- | --- |
  | push、dolly in、zoom in、closer、move in | `push-in` | 放大 10%，第 0 格是原圖 |
  | pull、zoom out、widen、back away | `pull-out` | 從 1.10 倍縮回原圖 |
  | pan left、pan to the left、left to right | `pan-right` | 1.08 倍，裁切窗從右滑到左（畫面往左跑） |
  | pan right、pan to the right、right to left | `pan-left` | 1.08 倍，裁切窗從左滑到右 |
  | tilt up、crane up、rise | `tilt-up` | 1.08 倍，從下滑到上 |
  | tilt down、crane down、descend | `tilt-down` | 1.08 倍，從上滑到下 |
  | 其他或沒寫 | `drift` | 放大 4% 並略往右，第 0 格是原圖 |

  `still` 鏡頭的 `camera` 一定要寫表裡的運鏡：`camera` 沒有命中時 `motionMove` 會去讀 `motion`，角色的動作（pushes、pulls、rises）會被當成運鏡。

  等級上限（`series.json` 的 `visual_tier`，lint 擋）：`hybrid` 最多四成鏡頭是 clip、`stills` 一成、`clips` 不限；沒有 `series.json` 就全視為 clip。still 鏡頭的關鍵影格要通過 judge（`needs_review` 的 `assemble` 會拒絕）。
- 句子：`speaker`（`narrator` 或角色 id，預設旁白）、`emotion`（≤ 80 字，Gemini 聲音會併進 style；Azure 忽略並警告）。**句子仍是時鐘**：一個鏡頭的長度是它的句子加停頓，lint 對估計超過 12 秒的鏡頭報錯、10 秒警告，中位數低於 3 秒也警告——長旁白拆成更多鏡頭。有角色的漫劇照 drama-craft.md 的目標寫（中位數 2.5–3.5 秒、一句 12 字以內為主、長短要有差）；中位數落在 2–3 秒而觸發那條警告時保留鏡頭，在回報裡註明。每個場景至少一句台詞（lint 的錯誤），反應鏡與插鏡放畫外那個人正在說的那一句。
- `music`：`prompt`（Lyria 生成）或 `track`＋`sha256`（自帶），`gain_db`（−20）、`duck_db`（−10）、`fade_in_ms`、`fade_out_ms`。
- `subtitles`：`burn_in: false`（新自動產線為可開關CC；舊核准burn-in檔不在此自動重製）、`style`（`drama`：白字黑邊；`plain`：黑底框）、`speaker_prefix`（角色句前加「【名字】」）。
- `thumbnail.data.shot`：縮圖以那個鏡頭的關鍵影格當底圖。
- 名詞一致：故事聖經裡的名字寫進發音字典與 `claims.md`；觀眾最會抱怨的就是「一下九嬰一下九影」。

## 品檢與重做

| 階段 | 自動檢查 | 不過怎麼辦 |
| --- | --- | --- |
| `look` | judge：辨識度、符合外觀、風格、乾淨（手指、臉）、無文字；通過者中最高分是 `suggested` | 全部不過補一輪（seed 101…）；仍不過結束碼 1，改 `appearance` 或 `sheet_prompt` 再跑 |
| `keyframes` | judge：每角色 `identity_<id>`、符合提示、風格、乾淨、無文字、主體避開底部字幕帶；相鄰鏡頭 dHash 太近警告 | 換 seed 最多 3 次；仍不過 `needs_review`，改 `prompt`／`camera` 再跑（`--shot` 只跑那幾鏡） |
| `clips` | ffmpeg：解析度、fps、時長、黑格、旁白範圍內的凍格、模型自己切鏡、第 0 格對關鍵影格 PSNR ≥ 22 且比相鄰關鍵影格高 3 dB；judge：每角色最後一格 identity、動作自然、符合 motion、乾淨、無文字 | 換 seed 最多 2 次；仍不過 `needs_review`，改 `motion`／`camera` 或拆短鏡頭 |
| `assemble` | 格數、響度、音樂床 ≤ −24 LUFS、每鏡片段第 0 格對關鍵影格、凍格 > 60 格（`fit: "freeze"` 除外） | `checks.json` 寫哪一鏡；此批片段太短須拆鏡/重做足長素材，不能換freeze或補無意義句子 |

門檻集中在 `tools/video/media/qc.mjs` 的 `THRESHOLDS`（片段）與 assemble 的常數；judge 門檻是後台的 `judge_min_score`（預設 7，單項低於 4 也不過）。試作時再校準，不要為了讓一支過而調低。

## 成本

- 此批指定模型與當日核實價目來源在 `docs/videos/series-plans/production-20261001/profile.json`：`veo-3.1-lite-generate-preview`，1080p素材固定8秒/24fps，無referenceImages/extension，可用首格；不自動換供應商。以下舊路線估算不是此批報價。
- 其他舊路線價目表在 `apps/api/app/video_media/catalog.py`：圖片 Gemini 3 Pro Image 約 US$0.134／張；片段 Gemini Omni 1.1 Flash US$0.15／秒（1080p）、Veo 3.1 US$0.40／秒、MiniMax H3 US$0.13／秒；音樂 Lyria US$0.08／首；judge 每次以 US$0.01 記。
- 一集 3 分鐘、30 鏡 × 6 秒、重做係數 1.5：片段約 US$40（Omni），圖片約 US$12，配音與音樂不到 US$1。照 drama-craft.md 的節奏，同樣 3 分鐘大約是 50–70 個鏡頭：圖片與 judge 隨鏡頭數增加，片段的錢要用「鏡頭數 × 模型最短片段秒數」重算，不能沿用這個例子；每個階段的 `--dry-run` 會印實際估價。站主 2026-09-26 決定先不設上限，設定預設開很大（每月 3,000 片段秒、單支 US$200），第一支做完再依實際花費調低。
- 每個階段都有 `--dry-run` 印估價與伺服器本月剩餘；每次送出前用 `media/ledger.json` 對單支上限把關（超過結束碼 3）；每月預算由伺服器以 429 擋，請求不會送到供應商。

## 坑

- **主機地區**：Gemini 的影片功能在歐洲經濟區部分不開放，主機地區沒查過。第一支的第一鏡先 `clips --shot <第一鏡>` 單獨跑；被擋先回報；此批不可自行改核定Veo模型或供應商，其他路線只有取得對應授權才到後台把 `clip_provider` 改成 `minimax`，並把結果記回 `docs/videos/DRAMA.md`。
- **順序**：劇本關卡在 `look` 之前——工人不會在劇本核准前跑 `look`，手動做也不要，設定圖是第一筆花錢的東西；`keyframes` 要 look 核准且每角色有選定的圖（沒選就用 judge 建議）；`clips` 要 storyboard 核准；`render` 要 timeline（字幕條依旁白切）與縮圖鏡頭的關鍵影格；`assemble` 要六個雜湊都對（`look_hash`、`clips_hash`、`subtitles_hash`、`mix_hash` 加原本兩個）。改了 `look` 或角色外觀，設定圖、關鍵影格、片段全部過期；改音樂增益只重混音。
- **劇本關卡的雜湊只算敘事**：look／keyframes／clips 自動修提示詞不會讓核准失效；旁白退回或討論改了台詞才要再看。
- **judge 說片段太大**（413）：工具會自動做 720p 代理檔上傳再判，不用手動。
- **still 鏡頭的 PSNR**：只有 `push-in` 與 `drift` 的第 0 格是整張關鍵影格，`assemble` 對它們算 PSNR；pan、tilt、pull-out 一開始就裁掉邊緣，只驗格數。`checks.json.metrics.shots` 記 `kind: "motion"` 與 `move`，看到 `drift` 多半是 `camera` 沒寫或用了表裡沒有的字。
- **接續鏡頭**：`start_frame: { shot, at: "last" }` 目前只把上一鏡最後一格當參考圖，片段仍從自己的關鍵影格開始，所以 assemble 的第 0 格檢查仍成立；要真的從上一格接下去，等供應商支援時要一起改 assemble 的比對來源。
- **Windows 本機**：Playwright 用 `--channel msedge`；整套測試並行時 `media/cache.json` 偶爾遇到 rename 的 EPERM（Windows 檔案鎖），單跑會過，CI 是 Linux 不受影響。
- **舊burn-in字幕條**（此批關閉，只出CC）：不用 libass（內建字型只有 woff2，fontconfig 會悄悄換系統字型），每個不同的字幕文字一張 1920×260 透明 PNG，行高 1.5（Noto Sans TC 字框約 1.45 em，較緊會被版面檢查擋）。
- **上架**：3D 寫實的 AI 畫面與 AI 配樂一律勾「變造或合成內容」；每集劇情要獨立，不是換名字的模板；音樂只用 Lyria 或站主自己有授權的檔；分鏡、提示詞與參考圖留在工作區當作者證據。

## 站主從後台發起

站主在 `/admin/videos` 的「漫劇」分頁按「新的漫劇」，填故事前提（或選一篇文章改編）、風格與長度（`POST /admin/video-automation/drama-requests`；漫劇設定要先開啟，否則 409 `video_drama_disabled`）。伺服器建一部 `kind = one-off` 的作品（slug `one-off-<請求 id 前 8 碼>`，`planned_episodes = 1`），第 1 集 `planned`，請求列指向它；表單送出後開那部作品的頁面。主機工人下一輪從 `GET /video/automation/series/next` 拿到 `kind: "bible"` 的工作，企劃模型寫故事聖經 → `POST …/series/<slug>/docs`，等站主；站主在作品頁的故事聖經 `DocPanel` 讀、討論、核准（可以自己改，也可以退回帶備註）。核准後第 1 集變 `ready`，工人 `POST …/series/<slug>/episodes/1/start`（影片 slug `<作品 slug>-e001`），寫 `series.json` 與 `brief.md`，接著照上表走；上架確認後 `POST …/episodes/1/done`。

後台的「單集漫劇」清單列的是 `kind = one-off` 的作品（`GET /admin/video-automation/series?kind=one-off`）；單集的影片頁最上面是它的故事聖經 `DocPanel`（含討論），下面才是劇本卡片與製作的關卡；作品列表卡顯示等模型回覆的訊息數與等站主核准的文件數。影片列表看得到每支的 `format`、`media_usd`、`clip_seconds`。

`GET /video/automation/drama-requests/next` 只剩下單集變成作品之前排進的舊請求（沒有 `series_id`）；那些仍走 `planner-drama.md` 寫 `brief.md` 與大綱選項、`POST …/drama-requests/{id}/start`、送審「選大綱」的舊路，做完 `POST …/{id}/done`。新的請求不會出現在那裡。
