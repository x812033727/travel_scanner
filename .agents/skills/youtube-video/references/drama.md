# AI 漫劇路線：角色設定圖、關鍵影格、圖生影片、多角色配音、燒錄字幕、配樂

這條路線的成品是一支像《山海经之万兽图鉴》那樣的 AI 動畫劇：每個鏡頭是一段 AI 生成的動態片段（先出關鍵影格，再圖生影片），旁白加多個角色配音，底部燒錄繁中字幕，有背景音樂，五語 CC。設計與為什麼這樣做在 `docs/videos/DRAMA.md`；這份只寫**怎麼做**。投影片路線的共通部分（一次性設定、發音字典、CC 翻譯、上架包）在 `.agents/skills/youtube-video/references/automated.md`，這裡不重複。

站主把關的關卡比投影片多兩個：

1. 選大綱（`outline`）
2. **選每個角色的設定圖**（`look`）：在花任何片段的錢之前先砍掉不對的角色概念
3. 聽旁白（`audio`）
4. **看分鏡**（`storyboard`）：每鏡的關鍵影格；後台設定「分鏡自動核准」開著且 judge 全過時伺服器會自己核准
5. 看成片（`final`）、確認可以上架（`publish`）

都在 `/admin/videos` 做，工具用 `review-push --gate <關卡>` 送、`review-pull` 讀回；核准綁檔案雜湊。

## 一次性設定（站主做）

| 項目 | 怎麼做 | 沒做會怎樣 |
| --- | --- | --- |
| 開啟漫劇 | 後台「影片審核 → 設定」的 AI 漫劇區：`drama_enabled`、圖片／片段／音樂的供應商與模型、片段解析度與預設秒數、每月預算（片段秒、圖片、judge 次數、音樂首數）、單支上限 `max_usd_per_video`、judge 門檻、分鏡自動核准、風格預設、角色聲音池 | `look`／`keyframes`／`clips`／`music` 結束碼 3 |
| 供應商金鑰 | 圖片與片段用網站既有的 Gemini 金鑰（`hotspot_guide_gemini_api_key`）；MiniMax 當第二 adapter 用 `minimax_api_key`。金鑰只在 API 容器 | `media-status` 顯示 NO KEY |
| 影片工具權杖、ffmpeg、瀏覽器 | 同投影片路線（`automated.md` 的一次性設定）；`look`／`keyframes` 的聯絡表也用瀏覽器畫，沒有瀏覽器只會少一張聯絡表 | — |
| 站主自帶的音樂 | 放在 `<VIDEO_WORKDIR>/_music/<檔名>`（mp3／m4a／wav／flac），`video.json` 寫 `music.track`，有 `music.sha256` 就核對 | `music` 結束碼 3 |

`node tools/video/cli.mjs media-status --slug <SLUG>` 印出伺服器目前的供應商、預算、儲存空間，以及這支影片到目前為止的花費。

## 主幹

`status --slug <SLUG>` 列的是漫劇的 18 步（`tools/video/core/state.mjs` 的 `DRAMA_STEPS`；沒有 `music` 的影片少一步）。

| # | 階段 | 誰 | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 1 | 企劃：故事聖經（前提、角色、幕）＋ 2–3 個大綱（提示 `.agents/skills/youtube-video/references/prompts/planner-drama.md`） | 企劃代理 | `<VIDEO_DOCS>/brief.md`（章節「故事前提」「角色」「站主觀點」是 lint 要求的） | `review-push --gate outline`；站主選大綱 |
| 2 | 撰稿：劇本與分鏡表（提示 `prompts/writer-drama.md`） | 撰稿代理 | `video.json`（`format: "drama"`）、`claims.md`（改編時） | `lint` 零錯誤：每鏡 ≤ 12 秒、一句一個說話者、角色 ≤ 3 |
| 3 | 查核：連貫性與設定一致（提示 `prompts/verifier-drama.md`） | **另一個**代理 | `verify-1.md` | 改編的事實照投影片的規矩查 |
| 4 | `look`：每角色幾張設定圖，judge 打分，聯絡表 | 工具 | `characters/manifest.json`、`characters/<角色>/*.png` | `review-push --gate look`（每角色一張審核）；**站主選一張**；`review-pull` 寫 `characters/choice.json` 並記核准 |
| 5 | `tts`：依說話者分批，情緒併進 Gemini 的 style | 工具 | `audio/`、`narration.wav`、`timeline.json` | `--dry-run` 先看每個聲音的字數；角色聲音不在允許清單會指名角色 |
| 6 | `check-audio` → `review-push --gate audio` | 工具、站主 | `review/check-flags.json` | 站主核准旁白 |
| 7 | `keyframes`：每鏡一張 1920×1080，參考選定的設定圖，judge 不過換 seed（最多 3 次） | 工具 | `keyframes/manifest.json`、`keyframes/*.png`、聯絡表 | `review-push --gate storyboard`；站主看分鏡（或自動核准）；`review-pull` |
| 8 | `render`：卡片、字幕條、縮圖（以指定鏡頭的關鍵影格當底圖） | 工具 | `frames/`（含 `frames/sub-*.png`） | 缺字結束碼 1 |
| 9 | `clips`：每鏡圖生影片，ffmpeg 與 judge 品檢，不過換 seed（最多 2 次），送出前對單支上限把關 | 工具 | `clips/manifest.json`、`clips/*.mp4` | **第一支先單獨跑一鏡**看主機地區有沒有被 Gemini 擋 |
| 10 | `music`：生成或核對自帶曲子 | 工具 | `music/manifest.json` | — |
| 11 | `assemble`：片段對齊句子（截、慢放、凍格）、疊字幕條、溶接、音樂壓低、串接、檢查 | 工具 | `final.mp4`、`checks.json`（六個雜湊） | 自動檢查全過 |
| 12 | CC 翻譯、`captions`、`review-push --gate final`、`package`、`review-push --gate publish` | 同投影片路線 | `captions/`、`upload/` | `UPLOAD.md` 多了合成內容揭露、劇情獨立、音樂授權三項 |

每個媒體階段之間都看 `STOP` 檔；中斷後重跑接著做：同一個請求不付第二次（`media/cache.json`），還在跑的伺服器工作接著輪詢（`media/jobs.json`），花費都在 `media/ledger.json`。

## 指令

```bash
node tools/video/cli.mjs media-status --slug <SLUG>
node tools/video/cli.mjs look      --slug <SLUG> [--candidates 3] [--character <角色 id>] [--dry-run] [--channel msedge]
node tools/video/cli.mjs look      --slug <SLUG> --choose jingwei=2,yandi=1     # 後台頁用不了時本機選圖，再 approve --gate look
node tools/video/cli.mjs tts       --slug <SLUG> --dry-run                      # 分聲音印字數與額度
node tools/video/cli.mjs keyframes --slug <SLUG> [--shot a,b] [--takes 3] [--force] [--dry-run] [--channel msedge]
node tools/video/cli.mjs render    --slug <SLUG> [--channel msedge]             # 漫劇要先有 timeline（字幕條依旁白切）與關鍵影格（縮圖底圖）
node tools/video/cli.mjs clips     --slug <SLUG> [--shot a,b] [--takes 2] [--force] [--dry-run]
node tools/video/cli.mjs music     --slug <SLUG> [--dry-run]
node tools/video/cli.mjs assemble  --slug <SLUG>
node tools/video/cli.mjs review    --slug <SLUG>                                # 也寫 review/look.html（本機看候選設定圖）
node tools/video/cli.mjs review-push --slug <SLUG> --gate outline|look|audio|storyboard|final|publish
node tools/video/cli.mjs review-pull --slug <SLUG>
node tools/video/cli.mjs approve   --slug <SLUG> --gate look|storyboard [--note "…"]   # 後台頁不能用時的備援
node tools/video/assemble/smoke.mjs --fixture drama [--channel msedge]          # 合成替身跑 render → assemble → review → package，不碰任何服務
```

結束碼同投影片路線：1 品檢或 lint 沒過（`needs_review` 進 manifest，改提示詞再跑）；2 順序不對（例如 look 還沒核准就 `keyframes`、storyboard 還沒核准就 `clips`）；3 要站主（漫劇沒開、沒金鑰、單支上限、核准）；4 供應商或額度；5 ffmpeg 或瀏覽器沒裝。

## video.json 的重點

- `format: "drama"`；範例 `tools/video/core/fixtures/drama/video.json`（精衛填海，兩個角色、四個鏡頭、一張結尾卡）。規則在 `tools/video/core/drama.mjs`（`validateDrama`、`shotProblems`）。
- `look`：`preset`（`cinematic-3d`／`anime-2d`／`ink-wash`／`custom`）加可覆寫的 `style`、`negative`、`motion`（英文，給圖片與影片模型）、`candidates`（每角色幾張設定圖）、`style_frames`（`<VIDEO_DOCS>` 裡的參考圖）。
- `characters[]`：`id`（小寫，不可是 `narrator`）、`name`（字幕與審核頁用）、`appearance`（英文 ≤ 800 字，設定圖與每個鏡頭都用它）、`voice`（同 `voice` 的物件；Gemini 聲音才有 `style`）、`sheet_prompt`（可選）。
- 鏡頭場景 `template: "shot"`，`data`：`prompt`（英文 ≤ 1000 字，畫面本身）、`camera`、`motion`（給圖生影片）、`characters`（≤ 3 個 id，決定參考圖與 judge 的 identity 題）、`fit`（`auto`／`freeze`／`slow`／`trim`，片段比句子短或長時怎麼對齊）、`transition`（`cut`／`dissolve`）、`start_frame: { shot, at: "last" }`（接續更早的鏡頭；目前是把上一鏡最後一格當參考圖，片段仍從自己的關鍵影格開始）、`end_frame: { prompt }`（另出一張當片段的末格）。卡片場景（`title`／`chapter`／`outro`）照投影片版型。
- 句子：`speaker`（`narrator` 或角色 id，預設旁白）、`emotion`（≤ 80 字，Gemini 聲音會併進 style；Azure 忽略並警告）。**句子仍是時鐘**：一個鏡頭的長度是它的句子加停頓，lint 對估計超過 12 秒的鏡頭報錯、10 秒警告，中位數低於 3 秒也警告——長旁白拆成更多鏡頭。
- `music`：`prompt`（Lyria 生成）或 `track`＋`sha256`（自帶），`gain_db`（−20）、`duck_db`（−10）、`fade_in_ms`、`fade_out_ms`。
- `subtitles`：`burn_in`（漫劇預設 true）、`style`（`drama`：白字黑邊；`plain`：黑底框）、`speaker_prefix`（角色句前加「【名字】」）。
- `thumbnail.data.shot`：縮圖以那個鏡頭的關鍵影格當底圖。
- 名詞一致：故事聖經裡的名字寫進發音字典與 `claims.md`；觀眾最會抱怨的就是「一下九嬰一下九影」。

## 品檢與重做

| 階段 | 自動檢查 | 不過怎麼辦 |
| --- | --- | --- |
| `look` | judge：辨識度、符合外觀、風格、乾淨（手指、臉）、無文字；通過者中最高分是 `suggested` | 全部不過補一輪（seed 101…）；仍不過結束碼 1，改 `appearance` 或 `sheet_prompt` 再跑 |
| `keyframes` | judge：每角色 `identity_<id>`、符合提示、風格、乾淨、無文字、主體避開底部字幕帶；相鄰鏡頭 dHash 太近警告 | 換 seed 最多 3 次；仍不過 `needs_review`，改 `prompt`／`camera` 再跑（`--shot` 只跑那幾鏡） |
| `clips` | ffmpeg：解析度、fps、時長、黑格、旁白範圍內的凍格、模型自己切鏡、第 0 格對關鍵影格 PSNR ≥ 22 且比相鄰關鍵影格高 3 dB；judge：每角色最後一格 identity、動作自然、符合 motion、乾淨、無文字 | 換 seed 最多 2 次；仍不過 `needs_review`，改 `motion`／`camera` 或拆短鏡頭 |
| `assemble` | 格數、響度、音樂床 ≤ −24 LUFS、每鏡片段第 0 格對關鍵影格、凍格 > 60 格（`fit: "freeze"` 除外） | `checks.json` 寫哪一鏡；片段太短就換 `fit` 或補句子 |

門檻集中在 `tools/video/media/qc.mjs` 的 `THRESHOLDS`（片段）與 assemble 的常數；judge 門檻是後台的 `judge_min_score`（預設 7，單項低於 4 也不過）。試作時再校準，不要為了讓一支過而調低。

## 成本

- 價目表在 `apps/api/app/video_media/catalog.py`：圖片 Gemini 3 Pro Image 約 US$0.134／張；片段 Gemini Omni 1.1 Flash US$0.15／秒（1080p）、Veo 3.1 US$0.40／秒、MiniMax H3 US$0.13／秒；音樂 Lyria US$0.08／首；judge 每次以 US$0.01 記。
- 一集 3 分鐘、30 鏡 × 6 秒、重做係數 1.5：片段約 US$40（Omni），圖片約 US$12，配音與音樂不到 US$1。站主 2026-09-26 決定先不設上限，設定預設開很大（每月 3,000 片段秒、單支 US$200），第一支做完再依實際花費調低。
- 每個階段都有 `--dry-run` 印估價與伺服器本月剩餘；每次送出前用 `media/ledger.json` 對單支上限把關（超過結束碼 3）；每月預算由伺服器以 429 擋，請求不會送到供應商。

## 坑

- **主機地區**：Gemini 的影片功能在歐洲經濟區部分不開放，主機地區沒查過。第一支的第一鏡先 `clips --shot <第一鏡>` 單獨跑；被擋就到後台把 `clip_provider` 改成 `minimax`，並把結果記回 `docs/videos/DRAMA.md`。
- **順序**：`keyframes` 要 look 核准且每角色有選定的圖（沒選就用 judge 建議）；`clips` 要 storyboard 核准；`render` 要 timeline（字幕條依旁白切）與縮圖鏡頭的關鍵影格；`assemble` 要六個雜湊都對（`look_hash`、`clips_hash`、`subtitles_hash`、`mix_hash` 加原本兩個）。改了 `look` 或角色外觀，設定圖、關鍵影格、片段全部過期；改音樂增益只重混音。
- **judge 說片段太大**（413）：工具會自動做 720p 代理檔上傳再判，不用手動。
- **接續鏡頭**：`start_frame: { shot, at: "last" }` 目前只把上一鏡最後一格當參考圖，片段仍從自己的關鍵影格開始，所以 assemble 的第 0 格檢查仍成立；要真的從上一格接下去，等供應商支援時要一起改 assemble 的比對來源。
- **Windows 本機**：Playwright 用 `--channel msedge`；整套測試並行時 `media/cache.json` 偶爾遇到 rename 的 EPERM（Windows 檔案鎖），單跑會過，CI 是 Linux 不受影響。
- **字幕條**：不用 libass（內建字型只有 woff2，fontconfig 會悄悄換系統字型），每個不同的字幕文字一張 1920×260 透明 PNG，行高 1.5（Noto Sans TC 字框約 1.45 em，較緊會被版面檢查擋）。
- **上架**：3D 寫實的 AI 畫面與 AI 配樂一律勾「變造或合成內容」；每集劇情要獨立，不是換名字的模板；音樂只用 Lyria 或站主自己有授權的檔；分鏡、提示詞與參考圖留在工作區當作者證據。

## 站主從後台發起

站主在 `/admin/videos` 填故事前提（或選一篇文章改編）、風格與長度，伺服器排進 `video_drama_requests`；主機工人下一輪先做這一支（`GET /video/automation/drama-requests/next` → `POST …/{id}/start`），做完標 done；影片列表看得到每支的 `format`、`media_usd`、`clip_seconds`。工人端接上這條與後台的表單頁還在票 `2026-09-26-video-drama-automation` 與 `2026-09-26-video-drama-owner-controls-ui`。
