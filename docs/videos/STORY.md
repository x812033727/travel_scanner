# 品牌故事路線（story）：設計

2026-09-28 定案。這是 AI 漫劇路線（[`DRAMA.md`](DRAMA.md)）底下的一種作品類型，不是第三種格式：影片的 `format` 仍是 `drama`，作品的 `kind` 是 `story`。畫面是卡通插畫的靜態圖加緩慢運鏡，只有旁白，字幕燒進畫面，內容是查核過的非虛構故事：一個品牌、一件日用品或一個大家天天用卻沒想過的標準，背後的生意怎麼運作。這份只寫**為什麼這樣做**與各部分怎麼接起來；操作步驟之後放在 skill `youtube-video` 的 `references/story.md`（票 `2026-09-28-video-story-worker`）。工作分成 12 張票，id 都是 `2026-09-28-video-story-*`。

## 目標與已定的選擇

站主給的參考是 YouTube 頻道「黑猫研究院」（`@qiqiqushi0`），要求先規劃 100 個這樣的故事，並讓主機每天做出兩支。

| 項目 | 決定（2026-09-28 站主） |
| --- | --- |
| 題材 | 混合三類：日常用品與隱形標準 40、日本／韓國／台灣旅途會遇到的品牌 40、科技與軟體 20 |
| 規格 | 16:9、12–15 分鐘、卡通插畫靜態圖加緩慢運鏡、只有旁白、燒錄繁中字幕、五語 CC |
| 頻道 | 放在 Mokaair 現有頻道 |
| 自動化 | 主機全自動：工人每天從企劃清單依序做兩支，站主只決定上架 |
| 圖片模型 | Gemini 3.1 Flash Image、1K 尺寸；清晰度不夠才改 2K，改之前先問站主 |
| 吉祥物 | 不要；只固定畫風 |

## 參考頻道教了什麼

2026-09-28 讀了該頻道的影片清單（324 支裡抓到 311 支的標題、觀看數、片長）與一支影片的分鏡縮圖。

- 近一個月觀看數最高的都是「日常用品加上隱藏的商業邏輯」：石英錶約 50 萬、米其林指南 38 萬、A4 紙 35 萬、杜比 31 萬、WD-40 17 萬。一年前的「小知識」與大品牌通史多半只有幾百到幾千次。題材選對比片長重要。
- 片長 10–16 分鐘。畫面是同一種卡通插畫，約每 9 秒換一張，一支約 80 張；底部燒錄白字字幕；第一句是反直覺的問題。
- 標題公式：「一家賣 A 的公司，為什麼能決定 B？」「你每天都在用的 X，憑什麼…？」「靠一個配方賺 70 年」。
- 敘事結構：反直覺的問題 → 起點與人物 → 關鍵點子 → 生意怎麼運作 → 代價或反轉 → 現況與一句觀察。

**只學類型，不抄內容。** 企劃清單避開該頻道做過的主題；稿子從原始來源寫，不讀它的逐字稿；標題與縮圖自己想。這也是 YouTube「非原創內容」政策的要求（[`HANDS-OFF.md`](HANDS-OFF.md) §頻道立場）。

## 為什麼是作品類型，不是新格式

兩種做法都評估過。

| 做法 | 要動的地方 | 結論 |
| --- | --- | --- |
| 第三種格式 `story` | `tools/video` 裡約 20 個以 `isDrama` 分支的檔案、兩條資料庫 CHECK（`ck_video_project_format`、`ck_video_stage_prompt_format`）、`VideoFormat` 與 `PromptFormat`、後台分頁與篩選、每種格式一份的設定、新的題目表與四個端點 | 乾淨，但工期約兩倍，而且與進行中的 PR #870 大面積重疊 |
| 作品類型 `kind: "story"` | 一支遷移、`next_job_for` 的一個分支、一個匯入指令、工人的一個模組、幾條放寬 | **採用** |

故事需要的畫面能力，漫劇已經有了：靜態鏡頭的運鏡（`tools/video/assemble/drama.mjs` 的 `motionMove`、`zoompanExpr`、`motionSegmentArgs`）、燒錄字幕（`tools/video/render/subtitles.mjs`）、配樂壓低、靜態鏡頭不買片段（`tools/video/media/clips.mjs`）。故事需要的佇列，長篇作品也已經有了：集數一集一集開始與完成（`apps/api/app/video_automation/series.py` 的 `next_job_for`、`tools/video/automation/series.mjs` 的 `seriesStep`）、免關卡（[`BINGE.md`](BINGE.md)）、全靜態圖等級 `stills`。

代價是故事與漫劇共用分頁、旁白聲音、預算與開關；作品列上有幾個對故事沒有意義的欄位（`genre`、`lead`、`tone`、`aspects`、`open_ended`）維持預設值、不讀。哪一天故事需要自己的設定頁或卡片版型，再升級成格式。

## 一支故事影片的規格

| 項目 | 規格 |
| --- | --- |
| 長度 | 12–15 分鐘；旁白約 3,000–3,750 字（每分鐘 250 字） |
| 畫面 | 每鏡 6–12 秒，一支 85–100 鏡，全部 `visual: "still"`；`MAX_SHOT_SECONDS = 12` 不變，品管的 `pace`（15 秒）因此必然成立 |
| 畫風 | 全部影片共用同一段風格提示詞與風格錨定圖（`look.style`、`look.style_frames`），存在作品的存檔裡 |
| 人物 | 一支最多 3 個反覆出現的主角，寫進 `characters`，設定圖由 judge 自動選；沒有主角的故事 `characters` 是空陣列，跳過設定圖階段 |
| 聲音 | 每一句的 `speaker` 都是 `narrator`；人物不說話 |
| 章節 | 六段：鉤子（30 秒內說完這支回答什麼）、起點與人物、關鍵點子、生意怎麼運作、代價或反轉、現況與一句觀察 |
| 片尾 | `outro` 卡：回到開場的問題給一句答案，只給一個下一步 |
| 字幕 | 燒錄繁中字幕＋五語 CC |
| 配樂 | 沿用漫劇的 `music`；設定關掉時沒有 |
| YouTube | 分類 27（教育）；合成內容揭露照漫劇的規則一律勾 |

## 企劃清單與集數列（合約）

企劃清單在 repo 的 `docs/videos/story-plans/brand-stories-100/stories.json`（票 `2026-09-28-video-story-backlog`）。工人的文件 volume 不會隨部署更新（票 `2026-09-25-the-video-worker-s-docs-volume`），所以清單**匯入資料庫**，工人從 API 拿，不讀檔案。

**作品列**（`video_drama_series`）：`kind: "story"`、`hands_off: true`、`visual_tier: "stills"`、`compilation: false`、`target_minutes: 13`、`style_preset: "custom"`，建立時就是 `active`，沒有任何文件（設定集、總綱、細綱、前情都不寫）。新增三個欄位：

| 欄位 | 內容 |
| --- | --- |
| `episodes_per_day` | 每天最多開始幾集，1–12，NULL 表示不限；以 Asia/Taipei 的日期計算 |
| `image_model` | 這部作品用的圖片模型，NULL 表示照設定分頁；故事填 `gemini-3.1-flash-image`，不動到漫劇預設的 Pro |
| `look` | 每個故事共用的畫風：`{style, negative, motion?}`。故事沒有設定集，畫風沒有別的地方可以放；其他類型的作品是 NULL |

**集數列**（`video_drama_episodes`）：一個故事一列，匯入時就是 `ready`。`number` 是製作順序（也就是排程順序），`chapter_number` 一律 1，`title` 是暫定標題，`logline` 是一句話說明，`slug` 是預先定好的影片代號，`beats` 是這個故事的企劃：

| `beats` 的鍵 | 內容 |
| --- | --- |
| `id` | 企劃代號，例如 `A01`、`B18`、`K04`、`T01`、`C20` |
| `category`、`region` | `everyday`／`asia-brand`／`tech`；`global`／`jp`／`kr`／`tw` |
| `subject` | 主題，例如「輪子行李箱」 |
| `question` | 開場要回答的那個問題 |
| `chapters` | 六段，各一個 `{key, point}`：`hook`、`origin`、`idea`、`engine`、`turn`、`now` |
| `takeaway` | 留給觀眾的一句觀察 |
| `must_verify` | 查核一定要對到來源的事實（年份、數字、引述），各是 `{claim, sources, core?, attributed?, reviewer_only?}`：`sources` 是 `sources` 的索引；`core` 是標題靠的那一條；`attributed` 表示旁白要說是誰的說法；`reviewer_only` 表示這一條只有工人讀不到的文件可以佐證，工人查核時以企劃為準 |
| `sources` | 至少 3 個 `{url, publisher, kind, supports, checked}`，https。企劃時照工人的方式讀過：每個都有回應，每個必查事實至少有一頁是工人讀得到文字的 |
| `names` | 這個故事的品牌名、產品名、真人姓名；圖像提示詞不得出現 |
| `cast` | 0–3 個 `{id, role, appearance}`；`appearance` 是英文、一般化的卡通人物，不像任何真人 |
| `image_notes` | 這個題目的圖像注意事項（例如不可畫出版權角色） |
| `sensitivity` | `none` 或 `care`（空難、抗爭、官司） |
| `related_guide` | 對應的 Mokaair 文章 slug，沒有就 null |
| `thumbnail` | `{headline, idea}`：縮圖上的字（最多 12 字）與畫面構想 |
| `caveats` | 查核的人留給撰稿的注意事項（查核紀錄的 `notes`，最多 800 字）：哪個軼事查不到出處不要講、哪個數字各來源說法不一、哪句話要說是誰的說法 |
| `publish` | `{day, slot}`：排程第幾天、`12:00` 或 `20:00` |

匯入指令（票 `2026-09-28-video-story-api-series-kind`）：`python -m app.cli video-story-import --series <slug> [--apply] [--limit N] [--episodes-per-day N]`，檔案從 stdin 讀，預設是試跑。同一個 `id` 再匯入一次只更新還沒開始的列，不會重複建立。作品不存在時照檔案裡的 `series` 建立；已經存在時不改作品列，因為站主可能在後台改過。`--limit` 只匯入排程的前 N 個（試作用 2），`--episodes-per-day` 是建立作品時的每日支數（從 1 開始）。

企劃清單的每個故事都有一份查核紀錄（`reviews/<代號>.json`），綁著故事內容的雜湊：另一個人或代理打開來源、逐條對過 `must_verify`。清單的檢查要求 100 個故事都有對得上內容的紀錄，所以匯入的每一列都是查核過的。

## 產線與關卡

步驟是漫劇的 `DRAMA_STEPS`，少掉不需要的：

| # | 階段 | 誰 | 關卡 |
| --- | --- | --- | --- |
| 1 | 開始：伺服器回下一集，工人寫 `brief.md` 與 `series.json` | 工人 | 大綱在本機直接核准，寫法同 `flow.mjs` 的 `draftEpisode`：題目是站主核准過的清單，不再問 Jev |
| 2 | 撰稿：逐章寫旁白與分鏡，合併成 `video.json` 與 `claims.md` | 撰稿模型 | `lint` 零錯誤 |
| 3 | 查核：逐章對來源網址 | 查核模型（新 session） | 查不到的說法拿掉；改超過 3 個事實再查一輪 |
| 4 | 聽眾審稿：逐章 | 聽眾審稿模型 | |
| 5 | `look`：只有在有主角時 | 工具 | judge 分數最高且過門檻的那張自動核准（免關卡作品本來就這樣） |
| 6 | `tts` → `check-audio` | 工具 | 旁白自動核准（Jev 全過） |
| 7 | `keyframes`：每鏡一張 | 工具 | 分鏡自動核准；送審只送聯絡表與待修的鏡頭 |
| 8 | `render`、`clips`（只寫 manifest，不花錢）、`music`、`assemble` | 工具 | 檢查全過 |
| 9 | 五語 CC、`qa` | 翻譯與審稿模型、工具 | 成片自動核准（品管全過） |
| 10 | `package` → 上架確認 | 工具 | 自動核准，進「可以上架」 |
| 11 | 上傳與上架時間 | 站主 | 站主在 Studio 上傳、在後台貼網址 |

長篇作品才有的三件事，故事都不做：劇本關卡（`script approved`）、前情（`recap`）、合集。

## 為什麼逐章寫稿

一次寫不完。網站轉送的上限是 295 秒（`apps/web/app/api/video/automation/run/route.ts` 的 `RUN_TIMEOUT_MS`），單次輸出上限是 32,000（`StageRunIn.max_output_tokens`）；一支 13 分鐘的稿子加 90 個鏡頭的提示詞，估計是 2 萬到 2 萬 7 千個輸出 token，寫到一半逾時就會被重試。撰稿、查核、聽眾審稿現在都是整份 `video.json` 來回。

故事改成一章一次：

- 撰稿（`writer:story`）一次只拿到這一章的要點、這一章用得到的來源頁面文字、前一章的最後幾句，只回這一章的場景。
- 查核（`verifier:story`）與聽眾審稿（`listener:story`）只回改動的句子（patch），不回整份稿。
- 工人負責合併、分配句子 id、跑 lint。
- 提示詞修正（keyframes 沒過）也是 patch：只回被點名的鏡頭。

## 查核與來源規則

這是故事與漫劇最大的差別：漫劇查的是連貫性，故事查的是事實，走投影片路線的做法（`claims.md`、`verify-*.md`、工人自己抓網址）。

- 每個數字、年份、引述都要對到一個**官方頁面**，或**兩個互相獨立的可靠來源**（大型媒體、百科、博物館、法院文件）。只有一個非官方來源的軼事，旁白要說是「據說」或交代是誰的說法。
- 查不到的說法（NOT FOUND）要從稿子拿掉；品管的 `facts` 項會擋。
- 查核過程不進旁白（不說「經查證」）。
- 負面事件（醜聞、官司、事故）以判決或官方文件為準；在世人物的負面說法要兩個來源。
- 傳說與事實分開講：大家愛講但查無實據的版本，可以講，要說它是傳說。
- 說明欄列出參考資料；`related_guide` 有值時放 Mokaair 文章連結。

**工人讀得到什麼。** 工人的讀取程式（`tools/video/automation/fetch.mjs`）只讀文字頁面：PDF 不讀，超過 3 MB 的頁面不讀，一頁只留前 40,000 個字，20 秒內抓不完就放棄。2026-09-28 把企劃清單的 965 個來源照這個方式讀了一遍：

| 結果 | 數量 |
| --- | --- |
| 工人讀得到文字 | 915 |
| 網頁在，但工人讀不到文字 | 50（38 個 PDF、10 個超過 3 MB、2 個時限內抓不完） |
| 讀得到的頁面裡，比 40,000 字長的 | 103 |
| 必查事實 | 939 條，其中 8 條只有查核的人讀得到證據（`reviewer_only`） |

粗略量過工人找得到多少：有數字、又有讀得到的頁面的事實有 773 條，其中 660 條的每個數字都出現在工人留下的文字裡，96 條只找到一部分，17 條一個都沒找到。沒找到的多半是寫法不同：日本與台灣的官方頁面用昭和、民國紀年，外文頁面寫 200 billion、企劃寫 2,000 億；少數是那句話在 40,000 字之後。所以：

- 企劃清單的規則是每個必查事實至少有一頁工人讀得到；PDF 與太大的文件留著當證據，人打得開，說明欄也會列。
- 企劃裡 `must_verify` 的事實是查核過的。工人的查核要確認的是**稿子說的跟企劃一樣**，以及撰稿模型自己加進去的數字、年份、人名在來源頁面裡找得到；找不到的拿掉。
- 很長的頁面，那句話可能在 40,000 字之後。工人要用事實裡的年份、數字、名字在整頁文字裡找到那一段，把那一段交給查核模型，不是只交頁面的開頭（票 `2026-09-28-video-story-worker`）。
- 工人讀不到的來源（PDF），交給查核模型的是企劃裡那個來源的 `supports`，並註明這是企劃查核時讀到的，不是這次讀到的。
- 官方頁面常用昭和、平成、民國紀年，外文頁面的數字單位也不同（billion 與億）。查核模型要自己換算，不能因為字面上找不到 1969 就說查不到。
- 找不到任何讀得到的頁面的事實，企劃會標 `reviewer_only`（查核的人讀過文件、也找過別的頁面）。工人對這幾條不去找來源，只確認稿子說的跟企劃一樣。

## 圖像規則

- 提示詞不出現品牌名、產品名、真人姓名、角色名（企劃的 `names`）；lint 擋。旁白可以講品牌名，圖裡不能有商標。
- 不畫文字、商標、浮水印（既有的 `no_text`）；judge 另加兩題：沒有商標、沒有可辨識的版權角色或真人長相。
- 真人（創辦人、工程師）畫成一般化的卡通人物：年代、服裝、職業對，長相不對應任何人。
- 會碰到版權角色的題目（迪士尼、吉卜力、Hello Kitty、環球影城）只畫場景與人群，不畫角色；排在排程最後兩週。
- 空難、抗爭這類題目（`sensitivity: "care"`）不畫事故畫面，畫制度與人怎麼改變。

## 伺服器

| 改動 | 位置 |
| --- | --- |
| 遷移：`ck_video_drama_series_kind` 加 `story`；`target_minutes` 放寬到 1–20；新增 `episodes_per_day`、`image_model`、`look` | 接在 main 目前的 head 之後（Shorts 的 PR #898 用了 `0109`） |
| `create_series`：故事作品一建立就是 `active`；`doc_problem` 拒絕故事作品的文件 | `apps/api/app/video_automation/series.py` |
| `next_job_for` 的故事分支：不看文件、不等前一集完成；看每日上限（台北日期）、`series_max_in_flight`、`series_episodes_per_month`，以及「可以上架」還沒上傳的集數是否已達 6 支 | 同上 |
| 匯入：`import_story_rows` 驗證每一列並寫進 `beats` | 同上，指令在 `story_cli.py` |
| 圖片模型：媒體工作依影片所屬作品的 `image_model` 決定模型 | `apps/api/app/video_media` |
| 立場檢查的故事版題組：照立場寫、留給觀眾一個觀察、沒有投資醫療法律政治建議、沒有業配、沒有貶損特定人；原本的「有示範」不問 | `apps/api/app/video_automation/judge.py` |
| 語系：PR #870 之後每支影片都等站主選語系；免關卡的故事由伺服器照設定自動決定 | `apps/api/app/video_reviews/admin_service.py` |
| 放棄影片時把那一集標成 `skipped`，名額才會釋放 | 同上 |
| 媒體每小時上限：送圖 60 → 240、judge 120 → 360 | `apps/api/app/video_media/admin_api.py` |
| Flash 的單價：目錄寫 US$0.045 是 0.5K 的價格，adapter 只送 `aspectRatio`、實際輸出 1K | `apps/api/app/video_media/catalog.py` |

工人不需要新的端點：`series/next`、`episodes/{n}/start`、`done` 就夠。故事的每一次模型呼叫都帶 `variant`，所以不算進 `max_drafts_per_month`（那是排程草稿的上限）。

## 每日配額與排程

- 上架時段每天 12:00 與 20:00（台北時間）。中午放全球題材（日常用品與科技以 2:1 穿插），晚上放日韓台題材（日、日、韓、日、台循環），每逢第 5 天晚上改放全球題材。100 個故事排 50 天，順序寫在企劃清單的 `publish`，集數的 `number` 就照這個順序。
- 製作比上架早：後台留著幾支「可以上架」當緩衝；緩衝滿 6 支就不開新的，站主幾天沒上傳也不會堆積。
- 不直接從每天兩支開始：試作兩支（A01 輪子行李箱、B18 迴轉壽司）→ 每天一支連續七天 → 每天兩支。

## 上限與成本

圖片單價是 Google 官方價目頁 2026-09-28 的數字；每支與每月是估計，試作後以帳本量到的為準。

| 模型與尺寸 | 每張 | 每支（約 120 張加 judge） | 每月 60 支 |
| --- | --- | --- | --- |
| **Flash 1K（選定）** | US$0.067 | 約 US$9 | 約 US$550 |
| Flash 2K | US$0.101 | 約 US$13 | 約 US$800 |
| Pro 1K–2K | US$0.134 | 約 US$17 | 約 US$1,040 |

旁白與配樂每支不到 US$1。寫稿用主機上的訂閱帳號，估計每天約 100 萬 token，至少兩個帳號輪替；額度用完時當天第二支順延，不自動改用付費 API。

每支估計 3–4.5 小時，瓶頸是圖片（送圖上限提高之前至少 2 小時）。兩支一天佔單一工人 6–9 小時，同時在做長篇漫劇時會互相排擠。

| 上限 | 現在 | 改成 | 在哪裡 |
| --- | --- | --- | --- |
| 每月圖片、judge 次數 | 1,500、3,000 | 各 9,000 | 設定分頁 |
| 作品每月集數 | 30 | 70 | 設定分頁 |
| 同時進行的影片（`max_waiting_drafts`） | 3 | 5 | 設定分頁 |
| 同時進行的集數（`series_max_in_flight`） | 1 | 2 | 設定分頁 |
| 旁白每月字數 | 30 萬 | 60 萬 | 主機 `.env` |
| Jev 每日次數 | 200 | 600 | 後台設定 |
| 審核單檔大小 | 400 MB | 1 GB | 主機 `.env` |
| 單支花費上限 | US$200 | 故事 US$25 | 工人端的帳本 |

旁白檢查現在一個場景呼叫一次 Jev；故事一支有 90 個場景，所以另外把呼叫跨場景合併（票 `2026-09-28-video-story-check-audio-batching`）。工作區沒有人清，上架後刪掉該支的工作檔（票 `2026-09-28-video-story-tidy-finished`）。

## 風險

| 風險 | 對策 |
| --- | --- |
| YouTube 的量產內容政策 | 每支有自己的來源、站主立場與觀察；說明欄列參考資料；從每天一支爬坡；前幾支成片站主親自看過才開自動核准 |
| 商標與版權角色 | 提示詞禁名、judge 兩題、版權角色的題目排最後 |
| 真人肖像與名譽 | 一般化的卡通人物；負面說法的來源規則 |
| 事實錯誤 | 逐章查核、`facts` 與 `links` 品管、企劃時就確認核心說法有來源 |
| 來源抓不到 | 企劃清單的驗證腳本逐一抓取；工人用固定的 User-Agent，每個網域間隔 1 秒 |
| 訂閱額度 | 兩個以上帳號；用完順延 |

## 站主要先做的事

1. 在後台「設定」打開「AI 漫劇」。故事借用漫劇的媒體服務；帳號要有 `settings.manage`。
2. 寫下頻道立場並存檔。空白時品管的 `policy` 一定不過。故事需要的三條，草稿：
   - 故事只講查得到出處的事，傳說與事實分開講。
   - 不業配、不推薦購買；負面事件以判決或官方文件為準。
   - 每個故事留給觀眾一個帶得走的觀察。
3. 每天在 YouTube Studio 上傳兩支並在後台貼網址。API 稽核通過之前，網站不能替站主上傳公開影片。

## 分期與票

| 票 | 內容 | scope | 依賴 |
| --- | --- | --- | --- |
| `video-story-design-docs` | 這份文件與 12 張票 | `docs/videos/STORY.md`、`tasks/open` | — |
| `video-story-backlog` | 100 個故事的完整企劃與驗證腳本 | `docs/videos/story-plans/brand-stories-100` | design-docs |
| `video-story-core-narrator-only` | 沒有角色時跳過設定圖、故事的 lint 規則、範例與煙霧測試 | `tools/video/core`、`tools/video/media/keyframes.mjs`、`tools/video/assemble/smoke.mjs` | design-docs |
| `video-story-storyboard-sheets` | 分鏡送審改送聯絡表 | `tools/video/review` | design-docs |
| `video-story-check-audio-batching` | 旁白檢查跨場景合併 Jev 呼叫 | `tools/video/tts` | design-docs |
| `video-story-api-series-kind` | 遷移、故事分支、上限、圖片模型覆寫、匯入指令 | `apps/api/app/video_automation`、`apps/api/app/cli.py`、遷移 | PR #870 |
| `video-story-api-policy-languages` | 故事版立場檢查、自動語系、釋放名額、每小時上限、Flash 單價 | `apps/api/app/video_automation/judge.py`、`apps/api/app/video_reviews`、`apps/api/app/video_media` | api-series-kind |
| `video-story-worker` | `automation/story.mjs`、故事提示詞、skill 文件與鏡像 | `tools/video/automation`、`.agents/skills/youtube-video`、`.claude/skills/youtube-video` | api-series-kind、core-narrator-only、storyboard-sheets |
| `video-story-tidy-finished` | 上架後清工作區 | `tools/video/automation` | worker |
| `video-story-admin` | 後台的故事清單、匯入表單、每日支數、「可以上架」預填時段，五語 | `apps/web/components`、`apps/web/messages` | api-series-kind |
| `video-story-pilot` | 試作兩支，數字寫回這份文件 | `docs/videos/STORY.md` | worker、backlog、部署 |
| `video-story-rollout` | 每天一支七天，再調成兩支 | `docs/videos/STORY.md` | pilot、tidy-finished |

順序：design-docs → backlog 與三張工具票平行 → PR #870 合併後 api-series-kind → api-policy-languages、worker、admin 平行 → tidy-finished → 部署（要站主同意）→ pilot → rollout。

第二期：直式精華（交給 Shorts 那條線，設計在 `SHORTS.md`）、多語配音、把題目清單的管理完全搬進後台。

## 試作紀錄

| 項目 | 數字 |
| --- | --- |
| 兩支試作的長度、鏡數、圖片張數、重做率 | （試作票做完補） |
| 每支花費（帳本）與各階段秒數 | （試作票做完補） |
| 1K 放大到 1080p 的清晰度 | （試作票做完補） |
| 訂閱帳號的 token 用量 | （試作票做完補） |
