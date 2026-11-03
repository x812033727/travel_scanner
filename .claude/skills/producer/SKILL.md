---
name: producer
description: 製片：決定 Mokaair 頻道接下來做什麼、改什麼，再把製作交給既有的影片 skill。四種工作：趨勢掃描（最近很夯的議題、短片與影片，包括站主貼來的 Instagram、TikTok、YouTube 連結，拆成可以學的結構）、系列診斷（用站台的 YouTube 報表、Studio 宣傳數字與縮圖標題評分，判斷每個系列該加碼、改包裝、改內容還是停）、新主題（從需求證據、頻道定位與製作成本挑題，先做三支試片）、新影片（不一定有主題的單支創作，例如 15–30 秒的 AI 寵物短劇）。產出是一份有數字、有出處、有下一步的製片單，花錢與上架永遠等站主。要看最近什麼紅、分析某個系列為什麼沒人看、想新系列或新短劇、拆解別人的爆紅短片、或用後台數據決定下一批做什麼時，先讀這個 skill。Producer for the Mokaair channel — trend scans, series diagnosis from the site's YouTube reports, new themes and one-off videos such as AI pet micro-dramas, handing production to the existing video skills.
metadata:
  short-description: 製片：看趨勢、診斷系列、發展新主題與新短劇
---

# 製片（producer）

這個 skill 只回答兩件事：**下一批做什麼**、**現有的哪裡要改**。怎麼做出來交給製作的 skill：

| 要做的東西 | 交給 |
| --- | --- |
| 投影片長片、AI 漫劇、一鍵合集、Shorts、人工錄製 | `.agents/skills/youtube-video/SKILL.md` |
| 奇聞檔案局（`curio-`） | `.agents/skills/curio-episode/SKILL.md` |
| 品牌故事（`story-`） | `.agents/skills/brand-story/SKILL.md` |
| 要付點數的 AI 片段（Hailuo、Kling、RunPod H3） | 先過 `.agents/skills/animation-preproduction/SKILL.md` 鎖企劃，再照 `.agents/skills/minimax-h3-runpod/SKILL.md` |
| 讀頻道數據 | `.agents/skills/youtube-channel-reports/SKILL.md` |

## 不能讓步的事

1. **數字先於意見。** 每個「這個系列不好」「這個題目會紅」都要附一個數字和它的出處（站台報表、Studio 宣傳表、公開的觀看與讚數）。拿不到數字就寫「沒有資料」，不要用印象補。
2. **付費流量和自然流量分開看。** 2026-11-03 的判讀：28 天 3.1 萬觀看裡，抽查的兩支 98–99% 來自 YouTube 廣告，自然點閱率只有 0.7–0.8%。把兩種混在一起，會把「買得到觀看」誤判成「觀眾喜歡」。報表的流量來源 `ADVERTISING` 一律單獨列。
3. **花錢、上架、改公開影片都是站主的事。** 這個 skill 產出建議與企劃；Studio 宣傳、生成點數、上傳、改標題縮圖，都要站主在對話裡點頭（宣傳要寫明金額、天數、地區、目標）。
4. **參考別人的片，學結構，不搬內容。** 拆節奏、鏡長、梗的位置、包裝；不複製角色、台詞、畫面或配樂，也不做「換個名字的同一支」。
5. **AI 生成要標示。** 照 YouTube 的合成內容揭露，`contains_synthetic_media` 照實填；短劇片角的「AI 生成」標示保留。

## 先選工作

| 站主說的 | 工作 | 產出 |
| --- | --- | --- |
| 「最近什麼很夯」「幫我看這幾支短片」 | **趨勢掃描**（§1） | 趨勢卡，每張一個可以學的結構 |
| 「某系列為什麼沒人看」「後台數據怎麼改」 | **系列診斷**（§2） | 系列診斷表：加碼／改包裝／改內容／停 |
| 「發展新主題」「開一個新系列」 | **新主題**（§3） | 三個候選與三支試片企劃 |
| 「做一支新的」「像這樣的短劇」 | **新影片**（§4） | 一份可以交給製作 skill 的製片單 |

站主一次問好幾件時照 §2 → §1 → §3 → §4 的順序：先知道現在哪裡壞了，再看外面，最後才開新的。

## §1 趨勢掃描

細節與來源清單在 `.agents/skills/producer/references/trend-scan.md`。

1. **蒐集。** 站主貼的連結優先；自己找時用 YouTube 搜尋（台灣、近 7 天、依觀看次數）、Shorts 與 Instagram／TikTok 的熱門短片、站上已查證的新聞。每支記：平台、帳號、日期、長度、比例、觀看／讚／留言（公開數字）。
2. **讀資料，不登入。** `yt-dlp --skip-download --dump-json <網址>` 讀公開數字；要看畫面時把影片抓到 scratchpad 的獨立資料夾，`ffmpeg -vf "fps=1,scale=320:-1,tile=4x4"` 做每秒一格的聯絡表。Instagram 網頁要登入才放影片，yt-dlp 通常讀得到公開 reel。
3. **量節奏。** 長片用 `node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file <影片> --out <json>`（鏡頭切點、鏡長、靜音），比較時對照 `docs/videos/drama-craft/` 的既有紀錄。
4. **拆結構，寫趨勢卡。** 每支一張：鉤子（前 2 秒發生什麼）、節拍（每拍幾秒）、反轉在哪一秒、收尾、包裝（標題、封面、字幕語言）、為什麼會被分享或留言、我們能做的版本、需要的製作路線與大約成本。
5. **判斷適不適合我們。** 對照頻道現有系列（§2 的表）與「不能讓步的事」；適合的才進 §3 或 §4。

## §2 系列診斷

細節、門檻與出處在 `.agents/skills/producer/references/series-diagnosis.md`；縮圖與標題的評分表在 `.agents/skills/producer/references/scorecards.md`。

1. **讀數據。** `node tools/video/youtube-reports/cli.mjs overview` 先看頻道是不是 Mokaair、報表有沒有進來；再 `videos --window 7`、`videos --window 28 --long`、`traffic --slug <slug>`。報表晚 48–72 小時；站台還沒有報表時，退回 Studio 每支影片的「觸及」分頁讀流量來源。
2. **讀花費。** Studio「內容 → 宣傳活動」逐筆抄：費用、曝光、觀看、訂閱、後續觀看、地區、最佳化目標。算每位訂閱成本與**每 NT$100 換到的後續觀看**（後續觀看才代表觀眾回來看別的片）。
3. **每個系列一行。** 系列、支數、自然觀看中位數、自然點閱率、平均觀看百分比、前 30 秒留存、付費占比、留言數、每 NT$100 後續觀看。
4. **下判斷。** 照 `series-diagnosis.md` 的決策表：點閱率低→改包裝（縮圖、標題），留存低→改內容（開場、節奏），兩者都還可以但沒曝光→加碼（Shorts 導流、宣傳只投中文地區、最佳化選後續觀看），三支試片都在門檻下→停或換形式。
5. **改包裝時給成品，不只給意見。** 新標題（大家認得的名字放前面、後綴照 `CAPTION_TAGS`）、新縮圖（用 `tools/video/templates/templates.mjs` 的 `thumbnailHtml` 畫，五項評分新舊並列），交站主在 Studio 用「測試與比較」上傳。

## §3 新主題

1. **需求證據。** 至少兩項：同題材在 YouTube／短影音近 30 天有多支高互動的片、站上同題文章的流量、我們自己的片在報表裡的搜尋字詞或推薦來源指向它、留言有人問。
2. **頻道適合度。** 能不能放進現有系列（奇聞檔案局、品牌故事、AI 科技資訊、AI 名詞、實作教學、漫劇、Shorts）；開新系列要說明為什麼現有的放不下。
3. **製作成本。** 走哪條路線、每支約花多少（點數、伺服器、人工），對照 `.agents/skills/youtube-video/SKILL.md` 的路線表；要付點數的先估價。
4. **三支試片。** 新主題不一次排滿：寫三支的企劃（標題、縮圖構想、開場 5 秒、長度），做完看 7 天報表再決定，門檻寫在企劃裡。

## §4 新影片（單支創作與短劇）

短劇的格式、節拍與兩支參考片的拆解在 `.agents/skills/producer/references/micro-drama.md`。

1. **一句話企劃。** 誰、在哪、想要什麼、哪裡出錯、最後一秒的反轉。說不成一句就還沒好。
2. **選長度與比例。** 現有 Shorts 工具只收 25–55 秒（`tools/video/shorts/core.mjs` 的 `PROFILE`）；15 秒的短劇目前要嘛寫成兩個反轉的 25–30 秒，要嘛等工具開新的長度（另開票，見 `micro-drama.md`）。
3. **分鏡與生成。** 一場戲 3–6 鏡，每鏡 2–5 秒；要付點數就照 `animation-preproduction` 先鎖分鏡、估價、等站主核准。
4. **包裝。** 標題寫情境不寫結局；封面是反轉前那一格最強的表情；雙語字幕（繁中＋英文）讓國外也看得懂。
5. **交製作。** 成片用 `node tools/video/shorts/cli.mjs import` 進 Shorts 流程（`.agents/skills/youtube-video/references/shorts.md`），之後照那邊的品管與上架。

## 產出：製片單

每次工作結束都交一份，放在對話裡或站主指定的檔案，不進 repo（數據屬於頻道）：

- **現況**：三到五個數字，每個附出處與日期。
- **建議**：最多五條，依影響排序；每條寫要誰做（代理／站主）、要不要花錢、怎麼量成效、幾天後回來看。
- **成品**：已經做好的標題、縮圖、企劃或分鏡，附檔案位置。
- **沒查到的**：資料缺口與原因（報表還沒進來、平台要登入、數字是推估）。

## 已知的坑

- **重新連結頻道會選錯帳號。** 2026-11-03 站主第一次重新連結選到個人帳號，站台改連到個人頻道；Mokaair 是另一個 Google 帳號。重新連結後一定先跑 `overview` 看 `channel` 那行是 Mokaair。
- **Reporting API 要啟用在 OAuth 用戶端所屬的專案。** 啟用到別的 Google Cloud 專案時，站台會一直說「還沒有啟用」；專案編號就是後台 OAuth 用戶端 ID 開頭那串數字。
- **Studio 分析頁在背景窗格常畫不出來。** 頻道層級的分頁會是黑畫面；單支影片的 `/video/<id>/analytics/tab-reach_viewers` 等 20 秒、往下捲後用 `document.body.innerText` 讀得到。
- **進行中的 Studio 宣傳改不了地區與最佳化目標。** 只能暫停再新開；「再次宣傳」會沿用舊設定，要用「新增宣傳活動」。存檔可能要站主重新驗證 Google 密碼。
- **審核區的成片會被清掉。** 要從成片截畫面做縮圖時，用 `tools/video/review/files.mjs` 的審核區 API 抓 `publish/final.mp4`；已經清掉的回 404，只能用舊縮圖或分鏡圖。
