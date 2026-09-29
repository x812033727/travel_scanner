# 插圖投影片（illustrated slides）：讓全自動影片生動起來

2026-09-29 定案。站主看過現有的全自動投影片影片後說「太死板」，要至少像黑貓研究院（`@qiqiqushi0`：一個問題講到底的說書旁白、每 4–6 秒換一張插圖加運鏡、配樂與音效）或 Gary Chen（`@garychenai`：每 5–10 秒一個畫面物件）那樣生動，或更好。這份寫**做了什麼決定、`video.json` 多了什麼、產線多了哪幾步、雜湊怎麼綁、節奏怎麼量、要花多少錢**；操作步驟在 skill `youtube-video` 的 `references/automated.md`，頻道規格在 [`README.md`](README.md)，漫劇的零件在 [`DRAMA.md`](DRAMA.md)。

## 站主的決定（2026-09-29）

| 項目 | 決定 |
| --- | --- |
| 範圍 | 全自動投影片影片（`format: "slides"`）與 Shorts；漫劇與原來如此事務所不動 |
| 成本 | 加 AI 插圖，每支長片約 US$8–15：每 5–8 秒一張插圖加運鏡，加配樂、音效、動態卡片、轉場與更活的旁白 |
| 燒錄文字 | 不燒錄：長片的字幕只做 CC（Shorts 既有的字幕條是另一個設計決定，保留） |
| 旁白口吻 | 說書式：反常識開場、「你以為…其實…」、章節結尾留懸念、具體場景與比喻；Gemini `voice.style` 有戲、有起伏 |
| 配樂 | 站主提供授權音樂檔（YouTube 音效庫或已購授權），放 `<VIDEO_WORKDIR>/_music/`；不用 Lyria，不需 AI 揭露 |
| 音效 | 站主提供一小組授權音效檔，放 `<VIDEO_WORKDIR>/_sfx/<set>/`，工具依規則自動放 |
| 插圖核准 | 一開始就自動：judge 分數過門檻即核准分鏡，站主只看成片 |
| 第一支試片 | 新開一支：〈Jev 決策模型〉，與 Gary Chen 的參考片同題，可直接並排比較 |

做法是把漫劇路線已有的零件（靜圖運鏡、溶接、配樂床、生圖與 judge、分鏡關卡）接到投影片路線，而不是把科技解說搬去漫劇路線：投影片保有自己的教學撰稿與查核提示詞、pace QA、dubs 狀態、大綱關卡，不會繼承劇本關卡與「一律揭露」。

## `video.json` 多了什麼

| 欄位 | 意思 | 規則 |
| --- | --- | --- |
| `look` | 插圖的畫風預設 | 有 `shot` 就必須有；預設 `tech-story`（配深色主題：深藍綠底、奶油白、青綠與橘強調，扁平帶畫報感的編輯插畫；negative 擋文字、logo、真人相貌、寫實）；沒有 `shot` 的投影片不能帶 `look` |
| `shot` 場景 | 一張插圖：`data.prompt`（英文 ≤1000 字）、`data.camera`（push in／pull out／pan left／pan right／tilt up／tilt down／drift）、`data.visual: "still"`、`data.transition?`（cut／dissolve） | 只准 still；不得有 `characters`、`fit`、`start_frame`、`end_frame`；shot 的句子不能 `reveal` |
| `music` | `{ track, sha256?, gain_db?, duck_db?, fade_in_ms?, fade_out_ms? }`，檔案在 `<work base>/_music/` | 任何格式都可以帶（`prompt` 走 Lyria 也還在，但站主決定用授權檔） |
| `sfx` | `{ set, gain_db? }`，音效組在 `<work base>/_sfx/<set>/` | 預設 gain −12 dB |

音效組的 `manifest.json`（站主寫）：

```json
{ "set": "studio-a", "sounds": {
  "stamp":  { "file": "stamp.wav",  "sha256": "…", "source": "YouTube 音效庫", "licence": "https://…" },
  "whoosh": { "file": "whoosh.wav", "sha256": "…", "source": "…", "licence": "…" },
  "pop":    { "file": "pop.wav",    "sha256": "…", "source": "…", "licence": "…" } } }
```

範例：`tools/video/core/fixtures/illustrated/video.json`（含 `brief.md`）。

## 產線多了哪幾步

`core/state.mjs` 的 `ILLUSTRATED_STEPS`：投影片的 12 步在「旁白核准」後多 `keyframes drawn`、`storyboard approved`，在「畫面渲染」後多 `music generated`（沒有 `music` 就沒有這步）。純投影片仍是 12 步。

| 步 | 指令 | 說明 |
| --- | --- | --- |
| 插圖 | `keyframes --slug` | 每個 shot 一張 1920×1080，judge 評分、最多 3 次換 seed；沒有角色所以沒有 look 關卡；rubric 在不燒錄字幕時沒有 `subtitle_band`。dry-run 印一輪與最多 N 次的成本 |
| 分鏡關卡 | `review-push --gate storyboard` | 順序 outline → audio → storyboard → final；站主決定一開始就自動核准（伺服器的 `slides_auto_approve_storyboard`，票 `2026-09-29-video-slides-media-api`） |
| 配樂 | `music --slug` | `music.track` 只核對檔案與 sha，不呼叫伺服器 |
| 合成 | `assemble --slug` | 走漫劇的混合版面：shot＝關鍵影格加運鏡；**單狀態卡片**（title、chapter、big、quote、cta、outro）在 drift 與 push-in 之間輪流漂移；多狀態卡片維持逐條出現；轉場規則＝第一景與章節卡硬切、其餘溶接、撰稿的 `data.transition` 優先；配樂床側鏈壓低；音效軌 |

音效的規則（`assemble/sfx.mjs`）：章節卡開始→`stamp`（章節卡即使被撰稿設成溶接也是 stamp，不放 whoosh）；溶接前 5 格→`whoosh`；每個 reveal 狀態開始→`pop`；任兩個音效至少隔 1.5 秒，pop 每 2 秒最多一個，第 0 格不放。

## 雜湊怎麼綁

| 檔案 | 綁什麼 | 為什麼 |
| --- | --- | --- |
| `keyframes/manifest.json` | `look_hash` ＋ `pictures_hash`（每個 shot 的 id、prompt、camera） | 改卡片文字不重畫、不重判、分鏡核准不失效；改 camera 或 prompt 只重畫那一張（其他張由快取回，只多 judge US$0.01） |
| `checks.json` | `speech_hash`、`visual_hash`、`look_hash`、`pictures_hash`（`keyframesHash`：實際用的每張圖的 sha）、`mix_hash`（有配樂時）、`sfx_hash`（有音效時） | 圖重畫、配樂或音效換了，`status` 會說要重新合成，`package` 不會拿舊成片 |
| `timeline.json` | `speech_hash`（含 `voice.style`） | 改口吻＝全部重錄＋旁白關卡重審 |

## 節奏怎麼量（`core/cadence.mjs`）

| 常數 | 值 | 意思 |
| --- | --- | --- |
| `MAX_PICTURE_SECONDS` | 8 | 一張畫面（卡片狀態或插圖）最多停多久 |
| `TARGET_AVERAGE_SECONDS` | 6 | 平均多久換一次畫面 |
| `MIN_ILLUSTRATION_SHARE` | 0.5 | 插圖至少佔多少時間，其餘是放數字的卡片 |
| `HOOK_SECONDS` | 20 | 開場章節要在幾秒內落鉤 |

lint 在估計時間軸上把這些當**警告**（撰稿不會因估計被擋；前五支證明撰稿能達標後再升成錯誤）；shot 超過 12 秒仍是錯誤（沿用漫劇的 `MAX_SHOT_SECONDS`）。最終關卡的 QA `pace` 項在合成後的真實時間軸上量：狀態超過 8 秒或插圖不到一半就不過，平均太慢只是警告。

## 揭露

`qa/checks.mjs` 的 `disclosureDecision`：漫劇一律勾；插圖投影片用風格化預設（`tech-story`、`flat-explainer`、`anime-2d`、`ink-wash`）加授權配樂→不需揭露；`cinematic-3d` 這種可能被當成真的畫風，或 Lyria 生成的配樂→勾。注意 [`SHORTS.md`](SHORTS.md) 寫「AI 音樂要揭露」而 [`DESIGN.md`](DESIGN.md) 的規則表寫「只有擬真內容要揭露」，兩份文件對 AI 音樂的說法不一致；本計畫用授權檔所以不觸發，工具採保守的一邊。

## 成本（估計，試片後改成實測）

| 項目 | 每支 10 分鐘 |
| --- | --- |
| 插圖 55–75 張 × gemini-3.1-flash-image US$0.067 ＋ judge US$0.01，平均 1.3 次 | 約 US$5.5–7.5；最壞 3 次 US$13–17 |
| 配樂 | US$0（授權檔） |
| 旁白 Gemini TTS | 不到 US$1 |
| **合計** | **約 US$6–9，最壞 US$15–18** → 投影片的單支上限設 20 |

用全站預設的 gemini-3-pro-image（US$0.134）會變 US$10–14；所以投影片要有自己的影像模型（票 `2026-09-29-video-slides-media-api`），過渡期把試片登記成一集的系列並設 `image_model`，或全站切 Flash。每月圖額度 1500、judge 3000 與漫劇共用，約夠 10 支；每小時生圖 240 次、judge 360 次，一支最多 225 次，工人一小時只跑一支。

## 說書式旁白（票 `2026-09-29-video-storytelling-prompts`）

第一句是反常識的說法或觀眾的問題、20 秒內落鉤；第一章至少一個「你以為…其實…」；每章最後一句是下一章要回答的問題；每章至少一個具體場景或比喻；長短句交替；`pause_after_ms` 節拍（冷開場後 900、「其實」前 600、章末懸念後 1200）；不寫「接下來我們來看」。`voice.style` 範例：「台灣國語說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，『你以為』放慢放輕，『其實』亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。」站主在 `/admin/videos` 設定分頁貼上就生效（`settle()` 抄進每支新影片）。規則的原文是 `tools/video/automation/register.mjs` 的 `REGISTER_RULES`，工具附在企劃、撰稿、聽稿三個階段的提示詞後（漫劇與原來如此事務所的提示詞不變）。已經寫好的影片用 `node tools/video/cli.mjs restyle --slug <slug>` 改口吻：聽稿模型的 `register` 變體逐句重講，數字、拉丁字詞、字典詞變了的句子退回（`rewrite.mjs`）、lint 不過就整份還原，`brief.md` 與 line id 不動（大綱核准與翻譯的 id 都還有效），改完 `verified=false`，工人下一輪重新查核、重錄、重審旁白；`--dry-run` 只量現況（幾個「你以為」、幾章以問題收尾、幾個節拍），結果寫在 `review/restyle.json`。

## 分期與票

| 期 | 票 | 狀態 |
| --- | --- | --- |
| 1 格式、lint、狀態、審核順序 | `2026-09-29-video-illustrated-slides-schema` | 做完 |
| 2 生圖與配樂階段 | `2026-09-29-video-illustrated-slides-media` | 做完 |
| 3 混合合成、音效 | `2026-09-29-video-illustrated-slides-assemble` | 做完 |
| 3b 配音音軌帶配樂 | `2026-09-29-video-dubs-carry-bed` | 已落地：`dub` 用成片同一套 `measureMixArgs`／`mixArgs`（自己的上傳格式）混配樂床，重用成片的 `build/sfx.wav`；dub 的 timeline 記 `mix_hash`／`sfx_hash`，不符就 stale |
| 4 QA、揭露、文件 | `2026-09-29-video-illustrated-slides-qa-docs` | 做完 |
| 5 伺服器開關、Flash、自動核准分鏡 | `2026-09-29-video-slides-media-api` | 已落地：設定列的 `slides` 物件（`slides_media_enabled` 預設關、`slides_image_model` 預設 gemini-3.1-flash-image、`slides_max_usd_per_video` 20、`slides_auto_approve_storyboard` 預設開、`slides_music_track`、`slides_sfx_set`；migration 0114），教學分頁的「投影片影片的插畫」區塊；`GET /api/video/media/status` 多回 `slides_enabled`、`slides_image`、`slides_max_usd_per_video`；`submit_job` 依 `VideoProject.format` 放行，投影片專案不接片段 |
| 6 工人 | `2026-09-29-video-illustrated-slides-worker` | 開著 |
| 7 說書式提示詞、`restyle` | `2026-09-29-video-storytelling-prompts` | 已落地 |
| 8 Shorts | `2026-09-29-video-shorts-motion-music` | 已落地：`tools/video/shorts/motion.mjs`（一景一段、透明字卡疊在運鏡的圖或漂移的底色上、景間溶接）、schema 2 的 `camera`／`music`／`sfx`、`from-episode` 接插圖投影片（主題 `cut:illustrated`）、頻道聲音的 style 改說書式；細節在 `SHORTS.md` §工具端 |
| 9 試片〈Jev〉 | `2026-09-29-video-pilot-jev-decision-model` | 開著 |

## 試片的數字表（試片後填）

| 項目 | 值 |
| --- | --- |
| 插圖張數／重做次數／judge 一次過比例 | |
| 媒體花費（US$） | |
| 從發起到成片的分鐘數 | |
| 站主審成片的分鐘數 | |
| 最長畫面／平均換畫面秒數／插圖佔比 | |
| 與 Gary Chen `2mtn-Qp59y4` 並排的觀察 | |

## 沒做、留給後面

- 多狀態卡片（bullets、steps、table 逐條出現）的整景連續運鏡。
- 插圖上沒有章節進度條（chrome 只在卡片上）；要的話把 chrome 截成透明疊層蓋在運鏡段上。
- Shorts 的逐句合成加固定 0.18 秒間隔：口吻改了節奏還是平，要改整景合成再切段（動到 phrase↔clip↔caption↔check 的對應）。
- Gemini 影像介面只送長寬比（1K），運鏡再放大 1.25×：試片看 push-in 的銳利度。
