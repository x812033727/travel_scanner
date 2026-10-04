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
| `look` | 插圖的畫風預設 | 有 `shot` 就必須有；沒寫時工人依 slug 從五個版畫預設裡輪流挑（§第二輪：`riso-teal`／`riso-navy`／`riso-forest`／`riso-plum`／`linocut-teal`）；`tech-story`（配深色主題：深藍綠底、奶油白、琥珀與一點磚紅；2026-10-03 起寫成版畫師的工單：墨線粗細不勻、網印平塗帶紙紋與套印微偏、手剪的陰影、焦點在畫面中間三分之一而兩側有不對稱的前後景、小小的簡筆人物（點狀眼睛或背影）、霧面；negative 擋文字、logo、真人相貌、寫實、光澤、霓虹光暈、無臉人偶、鏡像對稱）；沒有 `shot` 的投影片不能帶 `look` |
| `shot` 場景 | 一張插圖：`data.prompt`（英文 ≤1000 字，依序寫景別、地點與時間、正在發生的事、視線落點的物件與材質、光從哪來；不寫風格與顏色）、`data.camera`（push in／pull out／pan left／pan right／tilt up／tilt down／drift）、`data.visual: "still"`、`data.transition?`（cut／dissolve，通常不寫） | 只准 still；不得有 `characters`、`fit`、`start_frame`、`end_frame`；shot 的句子不能 `reveal`；連續三張同一種運鏡是 lint 錯誤（§畫面不像 AI） |
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
| 插圖 | `keyframes --slug` | 每個 shot 一張，伺服器的插圖模型有 2K 價時向 Gemini 要 2K（`imageSize`），否則 1K；judge 評分、最多 3 次換 seed；沒有角色所以沒有 look 關卡；rubric 在不燒錄字幕時沒有 `subtitle_band`，插圖投影片多一項 `craft`（像不像人手畫的印刷插畫）。dry-run 印尺寸、一輪與最多 N 次的成本 |
| 分鏡關卡 | `review-push --gate storyboard` | 順序 outline → audio → storyboard → final；站主決定一開始就自動核准（伺服器的 `slides_auto_approve_storyboard`，票 `2026-09-29-video-slides-media-api`） |
| 配樂 | `music --slug` | `music.track` 只核對檔案與 sha，不呼叫伺服器 |
| 合成 | `assemble --slug` | 走漫劇的混合版面：shot＝關鍵影格加運鏡（smoothstep 緩入緩出、位移量隨鏡頭長度放大到 6 秒為止、drift 依場景 id 決定左右）；**單狀態卡片**（title、chapter、big、quote、cta、outro）在 drift 與 push-in 之間輪流漂移，漂移的卡片左右輪流；多狀態卡片維持逐條出現；轉場規則＝撰稿的 `data.transition` 優先，否則第一景與章節卡硬切、前一景最後一句有 ≥600 ms 的停頓節拍才溶接、其餘硬切；配樂床側鏈壓低；音效軌 |

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
| 插圖 55–75 張 × gemini-3.1-flash-image **2K** US$0.101 ＋ judge US$0.01，平均 1.3 次 | 約 US$8–11；最壞 3 次 US$18–25 |
| 配樂 | US$0（授權檔） |
| 旁白 Gemini TTS | 不到 US$1 |
| **合計** | **約 US$9–12，最壞 US$19–26** → 投影片的單支上限 20 在最壞情況會擋到；要放寬就在設定分頁改 25 |

2026-10-03 起插圖改要 2K（1K 圖放大 1.25× 再裁切，在 1080p 看得出軟）：Flash 的 2K 是 US$0.101（1K 是 0.067，貴一半），gemini-3-pro-image 的 1K 與 2K 同價 US$0.134，所以用 Pro 畫會變 US$10–14 但不再多付；漫劇的關鍵影格仍是 1K（它們是片段的第一格）。每月圖額度 1500、judge 3000 與漫劇共用，約夠 10 支；每小時生圖 240 次、judge 360 次，一支最多 225 次，工人一小時只跑一支。

## 說書式旁白（票 `2026-09-29-video-storytelling-prompts`）

第一句是反常識的說法或觀眾的問題、20 秒內落鉤；第一章至少一個「你以為…其實…」；每章最後一句是下一章要回答的問題；每章至少一個具體場景或比喻；長短句交替；`pause_after_ms` 節拍（冷開場後 900、「其實」前 600、章末懸念後 1200）；不寫「接下來我們來看」。`voice.style` 範例：「標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，『你以為』放慢放輕，『其實』亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。」站主在 `/admin/videos` 設定分頁貼上就生效（`settle()` 抄進每支新影片）。規則的原文是 `tools/video/automation/register.mjs` 的 `REGISTER_RULES`，工具附在企劃、撰稿、聽稿三個階段的提示詞後（漫劇與原來如此事務所的提示詞不變）。已經寫好的影片用 `node tools/video/cli.mjs restyle --slug <slug>` 改口吻：聽稿模型的 `register` 變體逐句重講，數字、拉丁字詞、字典詞變了的句子退回（`rewrite.mjs`）、lint 不過就整份還原，`brief.md` 與 line id 不動（大綱核准與翻譯的 id 都還有效），改完 `verified=false`，工人下一輪重新查核、重錄、重審旁白；`--dry-run` 只量現況（幾個「你以為」、幾章以問題收尾、幾個節拍），結果寫在 `review/restyle.json`。

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

## 畫面不像 AI、不單調（2026-10-03）

站主看了插圖投影片的畫面後說「粗糙、單調、畫面無趣、AI 感太重，要更像真人做的」。先量了三支試片稿（`ai-term-token`、`ai-term-context-window`、`ai-term-retrieval-augmented-generation`）的分鏡：97 張裡 97 張都以「flat editorial illustration」開頭並把色盤抄進提示詞、「desk」出現在 51 張、「lamp」在 62 張裡出現 24 張、65 張沒寫景別、有一段連續三張 push in；畫風預設寫的是「flat editorial illustration with a painterly touch… anonymous figures」，所以每張圖都是同一張桌子、同一盞燈、同一個無臉人偶在青綠底上置中。單調與 AI 感是**提示詞和規則**造成的，不是模型挑錯；改了五個地方，一支影片的每一張都會不一樣，而且像印刷品：

| 層 | 改了什麼 | 在哪 |
| --- | --- | --- |
| 畫風 | `tech-story` 改成版畫師的工單：墨線粗細不勻、網印平塗帶紙紋與套印微偏、手剪陰影、焦點在畫面中間三分之一（Shorts 從 16:9 蓋滿 9:16 只留中間約 32% 寬，所以不對稱來自主體兩側的前後景，不是把主體推到一邊）、小小的簡筆人物（點狀眼睛或背影）、霧面；negative 多擋 glossy、airbrushed、smooth gradients、neon glow、lens flare、bokeh、stock vector、corporate flat icon、isometric、faceless mannequin、floating objects、mirror symmetry | `core/drama.mjs` `PRESETS["tech-story"]`（改了 `look_hash`：已有的 tech-story 影片會整支重畫，試片三支當時還沒畫） |
| 撰稿 | shot 的 prompt 照攝影師給插畫家的工單順序寫：景別 → 地點與時間 → 正在發生的事（一個人做一件具體的事，背影、側面或小小的在畫面裡，有簡單的臉，不是無臉人偶）→ 視線落點的物件與材質 → 光從哪來；不寫風格、顏色、「illustration」（look 會加）；主體在畫面中間三分之一（Shorts 只留那一條）；不畫表面是字的東西（打開的書頁、招牌、鐘面、螢幕）；camera 依畫面挑、不跟上一張一樣；transition 不寫；每章一個自己的地點與道具、同一個地點或物件不超過三分之一的 shot；比喻來自觀眾的日常（廚房、夜市、月台、工坊、教室、港口、屋頂），不用科技意象（筆電、螢幕、機器人、電路、大腦、雲、燈泡、頒獎台、沙漏、對話泡泡、發光的東西） | `automation/prompts.mjs` `TEMPLATE_GUIDE`；範例 `core/fixtures/illustrated/video.json` |
| lint | `pictureVarietyProblems`（只對插圖投影片）：連續三張同一種運鏡＝錯誤（撰稿修正迴圈會改）；沒寫景別、把 look 的字抄進 prompt、一個地點或物件出現在超過三分之一的 shot（≥6 張才算）＝每支各一條警告 | `core/drama.mjs`，經 `shotProblems` 進 lint |
| judge | 插圖投影片的關鍵影格多一項 `craft`（權重 1；由影片決定，不看鏡頭有沒有角色，所以 3D 漫劇的空鏡與畫風允許無臉人物的原來如此事務所都不評）：像不像人手為印刷畫的——有紋理與小瑕疵的線與色、不對稱的構圖與一個焦點、有層次、人物有簡單的臉或背對、沒有光澤／光暈／電腦算圖的表面 | `media/keyframes.mjs` `keyframeRubric` |
| 運鏡與剪接 | 運鏡 smoothstep 緩入緩出、位移量隨鏡頭長度放大（6 秒以上滿額、短鏡頭至少一半，速度大致一致）、drift 依場景 id 決定往左或往右、漂移的卡片左右輪流；轉場改成剪接師的習慣：預設硬切，前一景最後一句有 ≥600 ms 的停頓節拍（說書口吻的節拍：冷開場後 900、「其實」前 600）才溶接，章節卡硬切，撰稿的 `transition` 優先。Shorts 仍用線性運鏡（`shorts/motion.mjs` 另一張票的範圍） | `assemble/drama.mjs`（`MOTION_ENCODER_VERSION` v3，舊的運鏡段會重編） |
| 尺寸 | 插圖投影片與原來如此事務所的關鍵影格向 Gemini 要 2K（`ImageJobIn.size`，伺服器放進 `resolution`，Gemini adapter 送 `imageConfig.imageSize`）；只有目錄裡有 `usd_per_image_2k` 的模型才能要（Pro 同價、Flash US$0.101、MiniMax 沒有 → 422）；`GET /api/video/media/status` 的 `image`／`slides_image` 多回 `usd_per_image_2k`，工具據此決定尺寸與估價；作品（`series.json` 的 `image_model`）另指定模型時一律畫 1K、照 1K 估價，因為那個 2K 價是設定裡那個模型的 | `media/stages.mjs` `imageSizeFor`、`apps/api/app/video_media/{schemas,jobs,catalog,meter}.py`、`providers/gemini_images.py` |

要驗的事：試片的第一張 2K 圖（確認 `imageSize` 被 Gemini 接受、檔案約 2048×1152）、judge 的 `craft` 分數分布（太嚴就把權重留 1 但把門檻 `judge_min_score` 看一眼）、以及與第 1 版畫面的並排比較，寫回上面的數字表。

已上線：2026-10-03 04:31Z 隨 `90c52e19e` 部署。API 映像的目錄有 2K 價（Pro 0.134、Flash 0.101、MiniMax 沒有），影片工人的工具讀到 `image` 與 `slides_image` 兩個選擇的 `usd_per_image_2k`。當時正式站的「替投影片影片畫插圖」開關讀起來是關的（`slides_enabled: false`）：在它打開之前，投影片的圖走漫劇的開關與模型（Pro，2K 與 1K 同價），工具的預估卻用 Flash 的 2K 價，帳本記的是伺服器實收（票 `2026-10-03-illustrated-slides-lint-heuristics-the-shorts`）。

## 第二輪：版畫輪替、畫風樣張、審圖與光線（2026-10-03）

同一天站主再說「AI 感太嚴重，影片與投影片的插畫都要更好」。正式站從早上部署到這時沒畫過任何一張插圖投影片的圖（工人說自動草稿關著、每支都在等站主；七支插圖投影片在開關打開前就卡在「插畫沒開」，要站主按重試），所以這一輪先用本機工具經正式站真的畫了樣張再改：第 1 版畫風（`tech-story`，Flash 2K）六張、四種版畫候選各四張、再用其中一張當參考圖畫三張（`mokaair-work/videos/_audition/look-20261003/`，約 US$3）。看到的事：

- `tech-story` 的「墨線加平塗」被模型畫成**童書式的乾淨數位漫畫**：每樣東西都描一圈均勻的線、同一款可愛的臉、一樣的構圖——這就是觀眾讀成 AI 的東西。真正會讀成「人印的」是**版畫的物理痕跡**：網點、套印、油墨沒蓋滿、刻刀的毛邊。四種候選裡 risograph（網點、兩色套印）與 linocut（刻版）最像印刷品；gouache 像 AI 概念畫；pen-and-watercolour 最像人畫，但模型把它畫成**攤開的筆記本**（有頁邊、連價格牌的字都寫上去）。
- 寫「full-bleed, edge to edge」會讓模型**畫出紙邊**（印刷品有留白）；judge 的 `clean` 也抓到一張直式圖兩側補模糊條。所以畫風改寫成「畫面延伸出畫框四邊」、negative 擋 paper border／white margin／pillarbox／blurred side bars。寫「no ink outlines」模型照樣描線，只是 judge 扣 style 分，刪掉。
- 把一張畫好的圖當 `role: "style"` 的參考圖，其餘三張的網點、油墨、人物畫法**完全一致**，而且沒抄場景——這就是同一位插畫家畫一整支的辦法。

改了四層：

| 層 | 改了什麼 | 在哪 |
| --- | --- | --- |
| 畫風輪替 | 五個版畫預設：`riso-teal`（深青綠＋螢光珊瑚橘）、`riso-navy`（墨藍＋芥末黃）、`riso-forest`（深森林綠＋橘）、`riso-plum`（深李紫＋金赭）四組雙色 risograph，與 `linocut-teal`（青黑主版＋赭＋磚紅）。沒寫 `look` 的投影片影片由**slug 決定**用哪一個（`slidesPresetFor`：同一支永遠同一個，因為 look 在 `look_hash` 裡；不同支輪流，所以每支是自己的一刷），撰稿只在題材需要時點名；`tech-story` 保留給點名的影片。預設負面詞 ≤400 字可以抄進 `video.json` | `core/drama.mjs` `SLIDES_PRESETS`、`slidesPresetFor`；`automation/flow.mjs` `settle()` |
| 畫風樣張 | `keyframes` 對插圖投影片**先畫一張樣張**（`STYLE_PLATE_PROMPT`：小鎮街角、下午、兩個人、一隻貓、磚與玻璃與雨後的路；judge 同一套 rubric、最多 3 個 seed、沒過也取最高分），存 `keyframes/plate.json`（綁 `look_hash`，所以改一張 prompt 只重畫那一張、換 look 才重畫樣張與全部）、記進 `keyframes/manifest.json` 的 `plate`；之後每張 shot 都帶它當 `role: "style"` 的參考圖（放在參考圖最後），judge 也拿到它（標籤 `style plate`）並以「同一隻手、同一張紙」評 `style`。站主自己給 `look.style_frames` 時不畫樣張。多一張圖的錢（約 US$0.11–0.41）。伺服器端 Gemini adapter 對 `style` 參考圖改說「最後一張是畫風樣張：用它的技法、線、色、紋理與完成度畫，不取它的場景」，不再對所有參考圖說「保持角色一致」 | `media/keyframes.mjs` `stylePlate`、`readStylePlate`；`apps/api/app/video_media/providers/gemini_images.py` |
| 審圖 | `craft` 改問「是不是人為印刷做的而不是生成的：媒材的痕跡與小瑕疵、沒有把每樣東西描一圈均勻的線、不是到處都一樣細的細節、不對稱構圖一個焦點、簡單的臉或背影、沒有光澤／噴槍／光暈／算圖的完成度」；`clean` 多問「一張圖填滿整個畫框，沒有邊條、邊框、留白或模糊側條」。rubric 每題 ≤400 字（伺服器上限） | `media/keyframes.mjs` `keyframeRubric` |
| 撰稿與 lint | 撰稿：一支影片活在一整天裡，夜景與燈下的圖最多一半；每章至少一張兩三個人互相做事（討價還價、交東西、排隊、教、吵）、一張手裡拿著東西的特寫、偶爾一個小笑點（不該在那裡的貓、唯一一個面向錯邊的人）；`look` 不寫、交給工人。lint：夜景／燈下超過一半＝每支一條警告（≥6 張才算）；景別只在句首或接 shot／view／angle／of 時算景別（「a medium bowl」不算），接受 low-angle、bird's eye、top down、over-the-shoulder 的寫法；「cream」在冰淇淋、鮮奶油、咖啡裡不算色盤，risograph／linocut／gouache／halftone 算抄畫風；複數折成單數（ferries／shelves／boxes／potatoes；shoes 與 series 不動）；連三張同運鏡的錯誤指向真正帶運鏡的欄位（`camera` 或 `motion`） | `automation/prompts.mjs` `TEMPLATE_GUIDE`；`core/drama.mjs` `pictureVarietyProblems`、`SHOT_SIZE`、`LOOK_WORDS`、`DARK_LIGHT`、`motifOf` |

第五層是**裁邊**（`media/trim.mjs`）：寫了負面詞模型還是常把紙邊畫出來（樣張五張有四張），運鏡時紙邊會跟著畫面跑。`keyframes` 對填滿畫框的靜圖（插圖投影片、原來如此事務所、樣張）在 judge 之後用 ffmpeg 讀一張 512×288 的灰階縮圖，從四邊往內走到不再平坦（標準差 >10 或色調差 >8），任一邊超過 0.6% 就取邊內最大的 16:9 框裁掉再放大回原尺寸，存成 `<id>-<seed>-trim.png`；manifest、樣張參考圖與後面的合成都用裁過的檔，judge 看的是原圖（`takes[].margins` 記每邊的百分比）。沒有 ffmpeg 或讀不了的圖就照原樣用。

另外修了票 `2026-10-03-illustrated-slides-lint-heuristics-the-shorts` 的急件：`choiceFor` 只在 `slides_enabled` 時用投影片的模型，開關關著時跟伺服器一樣用漫劇的模型估尺寸與價錢（之前第一張圖就以 `video_media_model_changed` 失敗）。範例的 `race` 兩個跑者改在中間三分之一、`podium` 與 `race` 改成白天；`shorts/motion.mjs` 與 `SHORTS.md` 的 56% 改成 32%。

要驗的事：第一支部署後的插圖投影片在 `keyframes/plate.json` 看樣張與分數、聯絡表上每張圖的網點與油墨是不是同一刷；judge 的 `craft` 分布（樣張時 craft 約 6.5–7，門檻 7，三個 seed 內多半會過一張）；七支卡在「插畫沒開」的影片站主按重試後是否畫出來、單支花費（多一張樣張）。

## 成片大小（2026-10-04 實測，票 `2026-10-04-illustrated-slides-finals-fit-the-review`）

第一支在本機做完的網點版畫插圖投影片 `openai-devday-2026-recap`（`riso-navy`、74 張插圖、107 景、13:22）成片是 **895 MB**（67 MB／分鐘、平均 8.9 Mbit/s），`review-push --gate publish` 被站台擋下（413 `video_review_file_too_large`，當時單檔上限 400 MB）。`HANDS-OFF.md` 寫的「成片約 90–100 MB」是純投影片的數字。

**位元組在哪裡**（CRF 18，各段的檔案大小）：

| 段 | 段數 | 時長 | 大小 | 平均位元率 |
| --- | --- | --- | --- | --- |
| 插圖加運鏡（`motion`） | 74 | 422 秒（53%） | 804 MB（90%） | 15.3 Mbit/s，最低 6.6、最高 24.4 |
| 會漂移的單狀態卡片（也是 `motion`） | 11 | 60 秒 | 18 MB | 2.4 Mbit/s |
| 多狀態卡片（`stills`，`-tune stillimage`） | 22 | 321 秒 | 41 MB | 1.0 Mbit/s |
| 聲音（AAC 384 kbps） | | 802 秒 | 33 MB | |

網點與紙紋每一格都被 `zoompan` 重新取樣，CRF 18 照單全收：push-in 平均 19.4、pull-out 18.9、drift 17.5–18.8、pan 12.2–13.0、tilt 10.6–11.7 Mbit/s。YouTube 對 1080p、30 fps、SDR 上傳的建議是 **8 Mbit/s**（[Recommended upload encoding settings](https://support.google.com/youtube/answer/1722171)），運鏡段平均是它的兩倍、最高三倍。

**怎麼量的**：八個鏡頭（43.1 秒；每種運鏡至少一個，CRF 18 下從 6.6 到 24.4 Mbit/s 都有），用 `motionSegmentArgs` 同一條濾鏡鏈輸出無損參考，再用同一組編碼參數只換受測的設定去編，對參考算 VMAF（`libvmaf`，另記每個鏡頭最差 1% 的格）與亮度 PSNR；CRF 18 這樣編出來的大小與正式分段一致（`steamer-lift` 14.12 對 14.13 Mbit/s）。最後一欄是「觀眾看到的」：把每個版本再用 x264 以 4 Mbit/s 轉一次（代替平台轉檔，只量了前五個鏡頭），仍對無損參考算 VMAF。

| 運鏡段的設定 | 平均位元率 | 大小 | VMAF | 最差鏡頭的最差 1% | PSNR-Y | 再轉一次後的 VMAF |
| --- | --- | --- | --- | --- | --- | --- |
| CRF 18（原本） | 16.6 Mbit/s | 100% | 97.7 | 94.2 | 41.4 dB | 93.4 |
| CRF 20 | 12.5 | 75% | 97.3 | 93.3 | 39.8 | |
| CRF 22 | 9.3 | 56% | 96.7 | 92.4 | 38.3 | |
| **CRF 18＋`-maxrate 8M -bufsize 16M`（採用）** | **8.3** | **50%** | **96.7** | **91.0** | **38.4** | **92.4** |
| CRF 23 | 8.0 | 48% | 96.4 | 91.9 | 37.5 | |
| CRF 24 | 6.8 | 41% | 96.0 | 91.2 | 36.7 | 92.5 |
| CRF 20＋`-maxrate 6M -bufsize 12M` | 6.3 | 38% | 95.9 | 89.8 | 37.0 | 92.0 |
| CRF 24＋`-maxrate 6M -bufsize 12M` | 5.6 | 33% | 95.4 | 89.6 | 36.0 | |
| CRF 26 | 5.0 | 30% | 94.9 | 89.6 | 35.2 | 91.9 |
| CRF 28 | 3.7 | 22% | 93.4 | 87.7 | 33.8 | 91.2 |

`-tune film` 拿掉（CRF 23）只差 4% 大小、分數在同一條線上，不是槓桿。P 幀與 B 幀的 PSNR 差在 CRF 18 是 1.4 dB，上限 8 Mbit/s 時 0.55 dB：壓低位元率沒有讓畫面一格一格地閃。

**看畫面**（最吃位元的 `kitchen-wide` 第 112 格，滿版密網點，原生 23.9 Mbit/s）：1:1 看，8 Mbit/s 上限與 CRF 18、無損參考分不出來；放大兩倍，最密的網點區比 CRF 18 多一點不均勻（CRF 18 自己對無損也有）。到「三分之一大小」的設定（6 Mbit/s 上限、CRF 26–28）就不乾淨了：放大兩倍網點成塊，CRF 28 在 1:1 就看得出最密的網點糊成一片灰。所以**三分之一做不到**：整支片要到三分之一，運鏡段得壓到約 3.9 Mbit/s，是 YouTube 建議值的一半。

**決定**：運鏡段維持 CRF 18，加上 YouTube 建議的 8 Mbit/s 上限、兩秒緩衝（`assemble/drama.mjs` 的 `MOTION_MAX_RATE`、`MOTION_RATE_BUFFER`，`MOTION_ENCODER_VERSION` v4）。原本就低於上限的畫面（漂移的卡片、平塗畫風、`three-kilns` 這種 6.6 Mbit/s 的鏡頭）照舊（`three-kilns` 的 PSNR 前後都是 45.5 dB）；超過的鏡頭實測落在 8.4–9.1 Mbit/s（短鏡頭開頭可以先用掉緩衝），最難的三個鏡頭 PSNR 從 39.2 降到 34.3 dB、VMAF 從 98.9 到 97.2。再轉一次之後與 CRF 18 的母片差 1.0 分（轉檔本身就掉 4.8 分）。漫劇的片段段（`CLIP_ENCODER_VERSION`）沒量、沒動。

**改完的大小**：同一支片在複製的工作區用新設定重跑 `assemble`：`final.mp4` **535 MB**（原本的 60%，40 MB／分鐘、整支平均 5.3 Mbit/s），`checks.json` 全過、24,061 格不變。74 段插圖從 804 MB（15.3 Mbit/s）變成 444 MB（8.4 Mbit/s），最高的一段 10.0（2.1 秒的短鏡頭把緩衝用掉），原本就低於上限的 `three-kilns` 與 11 張漂移卡片（合計 18.2 MB）大小差不到 0.2%。107 段裡重編 85 段（插圖與漂移卡片；多狀態卡片沿用快取），在同時跑量測的 8 核筆電上花 32 分鐘。之後估大小用這幾個數字：

| 畫面 | 每分鐘 | 十分鐘 |
| --- | --- | --- |
| 純投影片（卡片與靜態圖） | 約 10 MB | 約 100 MB |
| 插圖投影片（一半時間是運鏡的插圖） | 約 40 MB | 約 400 MB |
| 最壞情況：整支都是頂到上限的運鏡 | 約 70 MB | 約 700 MB |

**站台的單檔上限**：`VIDEO_REVIEW_MAX_FILE_BYTES` 的預設從 400 MB 改成 1.5 GB（`apps/api/app/config.py`）。400 MB 是照純投影片訂的，新設定下 13 分鐘的插圖投影片仍超過它；1.5 GB 容得下最壞情況的 20 分鐘、一般情況的 35 分鐘以上。磁碟成本在 `HANDS-OFF.md` §上傳包與「可以上架」。

**已經做好的成片不用動**：`MOTION_ENCODER_VERSION` 一變，下次 `assemble` 會把那支片的運鏡段全部重編，`final.mp4` 的雜湊跟著變，成片核准要重來。不要為了縮小檔案去重跑已核准的成片（`openai-devday-2026-recap` 就維持 895 MB 那一份）；新設定只用在之後才 `assemble` 的影片。

**順帶看到、沒在這裡修**：運鏡其實是走一步停幾格（關鍵影格是 JPEG 時 `zoompan` 的裁切窗只落在偶數像素上；pan 有一半的相鄰格完全相同），票 `2026-10-04-still-shot-camera-moves-travel-in`。修它會讓每一格都不同、位元率再變，上限會把大小擋住。

## 沒做、留給後面

- 樣張沒放進聯絡表（`review/sync.mjs` 用張數切頁，多一格會錯位）；要看就開 `keyframes/plate-N.png`。
- 多狀態卡片（bullets、steps、table 逐條出現）的整景連續運鏡。
- 插圖上沒有章節進度條（chrome 只在卡片上）；要的話把 chrome 截成透明疊層蓋在運鏡段上。
- Shorts 的逐句合成加固定 0.18 秒間隔：口吻改了節奏還是平，要改整景合成再切段（動到 phrase↔clip↔caption↔check 的對應）。
- Shorts 的運鏡還是線性、不隨長度縮放（`shorts/motion.mjs` 在 `2026-09-28-sothatswhy-shorts-from-episode` 的範圍裡）。
- lint 的變化警告只給人看；工人的撰稿修正迴圈只吃錯誤，所以景別、抄色盤、同一地點太多這三條要靠撰稿規則本身。試片三支的舊稿（抄色盤、桌子太多）要重寫提示詞才會變；RAG 那支有一段連續三張 push in，部署後工人會用撰稿修正迴圈改掉。
- 原來如此事務所（`flat-explainer`）的畫風與撰稿規則沒改，只拿到 2K（它的畫風允許無臉人物，不套 `craft`）。
