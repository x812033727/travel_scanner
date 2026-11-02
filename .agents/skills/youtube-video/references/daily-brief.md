# Tech Signal｜科技訊號：每日 AI／科技 Podcast（daily-ai-YYYYMMDD）

站主 2026-11-02 定：每日 AI／科技快報改成由 Claude 主持的每日 Podcast《Tech Signal｜科技訊號》，**平日每天一集，20–25 分鐘（上限 30）**，取代 10 分鐘的快報。主持人叫 **Sola**（頻道聲音 Gemini Sulafat），**只有一個主持人**。**台灣國語主持、字卡全英文**：主市場還是台灣，但要國際化，歐美觀眾聽英文配音、看英文 CC，另外七種語言照舊（八語標題說明、CC、配音、縮圖都在上 YouTube 前做完）。先只上 YouTube（清單 `PLMSBVkAy71z0` 設成 Podcast，`docs/videos/PLAYLISTS.md`）。slug 沿用 `daily-ai-YYYYMMDD`：說故事關卡的快報措辭（`tools/video/core/narrative.mjs` 的 `DAILY_BRIEF_PANEL_QUESTIONS`）、品管不問「有示範」（`apps/api/app/video_automation/judge.py` 的 `is_daily_brief`）、縮圖的節目標籤（`tools/video/templates/templates.mjs` 的 `AI_THUMB_SERIES.brief`，現在是 Tech Signal）都掛在這個前綴上。

2026-11-02 起由排程的 Claude Code 雲端工作階段在台北時間平日 9:00 開工做（主機工人的「每日快報」站主已關，第四節是它的舊做法）。這是 SKILL.md 規矩 11「一支影片一個故事」的例外：一集是一個節目，每段一個章節。把整集串起來的是**一個觀點**：每一則都回答「這對你改變了什麼」，主題段再把它放進更大的產業、錢與台灣／亞洲的脈絡。其餘規矩照舊：一個畫面狀態不超過 15 秒、出處放卡片與說明欄。

參考的節目（2026-11-02）：The AI Daily Brief（先快訊、再一個主題接到更大的脈絡，20–25 分鐘）、Techmeme Ride Home（平日 15–20 分鐘，摘錄各方對新聞的說法）、《敏迪選讀》（先補背景再講事情，台灣聽眾熟悉的講法）。

## 一、每集結構（章節＝段落，字卡上的段落名用英文）

| 段落 | 長度 | 寫什麼 |
| --- | --- | --- |
| Cold Open | 約 30 秒 | 今天主題那則最意外的一句：日期＋誰＋做了什麼，停在影響之前。不放音樂 |
| Intro | 約 20 秒 | 固定句「這裡是 Tech Signal 科技訊號，從一堆雜訊裡，挑出今天真正重要的訊號。我是 Sola。」＋日期＋今天主題一句話。主題曲片段放這張卡 |
| Headlines | 6–7 分 | 5–6 則快訊，每則約 1 分鐘：第一句日期＋誰＋做了什麼，再一句對你的影響（台灣能不能用、要不要錢、要不要小心）。照影響大小排，每則一張帶 `source` 的卡；每則之間用一句串場，不寫「下一則」 |
| Signal of the Day | 9–11 分 | 主題一則講透，五拍：① 背景（為什麼是現在）② 事情本身 ③ 誰贏誰輸、錢從哪裡來 ④ 對台灣與亞洲的意義（晶片、供應鏈、在地服務與法規；找不到真的關聯就說沒有，不硬湊）⑤ 接下來看什麼。每拍至少一張卡 |
| What People Are Saying | 2–3 分 | 官方、分析師或媒體各一句說法，**只引用站上文章與它列的來源**，每句唸出是誰說的，卡片用 `quote` 寫原文與出處 |
| Try This | 1–2 分 | 聽眾今天就能做的一件事（打開哪個設定、去哪裡申請、先不要做什麼）；沒有就講要觀察什麼 |
| Sola's Take | 約 1 分 | 今天最重要的是哪一則、為什麼；一句承認不確定；一個留言題。站主貼來的觀眾留言，在這段挑一則回應。**不提下一集** |

- 題材：一天 6–8 則站上 `ai-news`、`tech-news` 文章（依 `news_date`）。主題挑影響最大、背景最值得講的那則；同一件事的幾篇合成一則。當天不到 5 則就跳過那天，寫原因。候選照舊用 `node .agents/skills/youtube-video/scripts/daily_news_pick.mjs --date YYYY-MM-DD`。不選：沒有官方來源也沒有具名媒體報導的傳聞、跟觀眾無關的純財報數字、站上還沒發布的文章；加密貨幣不談價格。只有具名媒體報導、官方沒證實的，可以選，但旁白與卡片都標明「據報導」，不放在 Cold Open。
- 排序本身是編輯判斷（YouTube 的「不真實內容」政策看的就是這個）：`brief.md` 的〈選題〉表每則寫排在這個位置的理由，主題寫為什麼是它。
- 標題：英文關鍵字加中文，例如 `Nvidia's new chip, explained｜Tech Signal EP12`（`youtube.title`），集數 EP 從 1 累加（看前一集的標題）。說明欄開頭揭露：旁白為 AI 合成語音、配樂為 AI 生成、內容依官方來源整理。
- 每天從 Signal of the Day 剪一支直式 Shorts（英文字卡，`tools/video/shorts`）導流。

## 二、英文字卡

- 字卡（`data` 裡畫在畫面上的字、`key`／`keys`、章節卡）全部英文；產品名照官方寫法。旁白與 zh-TW CC 照舊是台灣國語。翻譯只翻旁白、章節名、標題說明與縮圖字，**不翻字卡**，所以八語影片看到的是同一套英文字卡。
- 長度照 `docs/videos/PAPER.md` 的英文上限：有 `icon` 的 `big` ≤16 字、沒有 `icon` 的 `big` ≤2 行×22 字、`quote` 約 85 字、`key`／`keys` ≤24 字（`KEY_MAX_CHARS`）、有關鍵句帶時 `steps`／`compare` 不寫 `title`。lint 不檢查字卡語言、`render` 不一定擋英文超框，聯絡表一定要看。
- 縮圖的大標也用英文（兩到四個字），縮圖標籤由程式寫「Tech Signal」。

## 三、旁白與配音的規矩（2026-11-02 第一集試跑學到的）

- **不寫雙關、同音字的文字遊戲**（英文 brake／break 被兩個轉寫器都聽成另一個字）；型號結尾是數字的（Gemma 4）要讓數字唸得清楚，必要時換個說法。
- **每個畫面狀態不超過 15 秒**：`big`、`quote`、`outro` 不能用 `reveal` 分段（lint 會過、`render` 會擋），太長就拆成兩張卡；片尾 `outro` 正好三句（答案、留言題、訂閱邀請）。
- **大綱寫成工具讀得到的樣子**：`### 選項 A：標題`，下面接「一行說明：」與「開場鉤子：」兩行。
- **Whisper 第二意見**：雲端工作階段沒有主機的 `VIDEO_SECOND_OPINION`，先 `python3 -m venv ~/whisper && ~/whisper/bin/pip install faster-whisper`，每次 `check-audio` 帶 `VIDEO_SECOND_OPINION="$HOME/whisper/bin/python tools/video/tts/whisper_second_opinion.py"`、`WHISPER_MODEL=medium`。少了它，Gemini 聽錯的每一句都會被標（第一集第一輪 57 句，大多是同音字）。
- **日、韓翻譯每句瞄準 `max_chars` 的 85% 左右**：第一集日文 72 個視窗有 40 個要加速到最多 1.21×。
- `dubs/<語系>/fit.json` 的 `over` 若是某句錄得特別長（印尼文一句 72 秒），是語音模型錄壞，`dub --redo` 那句就好，不要縮翻譯。
- `dub` 與 `check-audio` 有專案鎖，一次只能跑一個；在背景等的時候不要用 `pgrep -f`（會比對到自己），等背景工作完成的通知。

## 三之一、節目音樂（站主 2026-11-02：AI 生成；整集一首很輕的底樂＋章節轉場音效）

- 底樂：`music.track`（`<VIDEO_WORKDIR>/_music/` 的檔，`sha256` 綁住），`assemble` 把它壓在旁白下（底樂 ≤ −24 LUFS、成片 −14 LUFS），比成片短就循環（`music --loop`）。
- 轉場與主題曲片段：音效組 `techsignal`（`<VIDEO_WORKDIR>/_sfx/techsignal/`，manifest 寫來源「AI 生成，Mokaair」，`assemble sfx-measure` 量過），章節卡自動放；主題曲片段放 Intro 卡。
- 整套音樂只生成一次（網站的配樂生成，`music.prompt`），存在站主的 Google 雲端硬碟「Tech Signal 音樂」資料夾，每天開工下載回來，節目的聲音固定。

## 四、主機工人怎麼做（2026-10-29 起；2026-11-02 站主關掉主機的每日快報，留作參考）

全自動，跟其他教學影片走同一條產線（`automated.md`、`docs/videos/AUTOMATION.md` §每日 AI 快報），差別如下：

1. **每天的請求**：設定分頁的「每日快報」開著時（`daily_brief_enabled`），到了台北時間 `daily_brief_hour`（預設 9 點），工人下一輪來問，伺服器就用前一天的文章開一筆請求；那天的文章少於 `daily_brief_min_stories`（預設 5）就記成跳過、寫原因，那天不出片。工人每一輪問一次，排在所有影片、請求與排程草稿之前；不受「等站主的草稿」上限擋，也不算進排程草稿的間隔與每月草稿數（企劃呼叫帶 variant `daily`）。
2. **企劃**：工人讀當天每一篇文章，企劃模型照第一到三節挑 5–8 則、排序、寫 `brief.md`（多一節〈選題〉表），出兩個大綱（開場用哪一則、怎麼排各不同，附排序理由）。slug 固定是請求的 `daily-ai-YYYYMMDD`；影片記 `category: ai-news`，**不記 `source_guide`**：快報不算重講哪一篇文章，之後站主還可以把其中任何一篇排成教學影片。規劃完用 slug 認領請求。
3. **關卡都是 Jev 與自動品管**：Jev 依頻道立場挑大綱（快報不問「有示範」）、聽旁白全對就核准、成片自動品管全過就核准、上傳包齊全就進「可以上架」。撰稿、查核、聽眾審稿都用 variant `daily` 的提示詞（`tools/video/automation/register.mjs` 的 `DAILY_BRIEF_RULES`），說故事關卡用快報措辭。退回大綱時重寫用同一天的文章、同一個 slug。
4. **語言分兩步，由伺服器決定**（`docs/videos/LANGUAGES.md`）：成片核准時伺服器照 `daily_brief_locales` 勾好八種語言（en、ja、ko、es、pt、id、vi、th）的標題說明與 CC，配音先不勾；這一批不用站主，自己核准，影片很快就進「可以上架」。網站把影片送上 YouTube 之後，伺服器才把設定裡勾的配音打開，工人照「上架後再加語言」的做法補做。
5. **站主每天兩件事**：
   - 上午：在「可以上架」卡片按上傳，排在當天 12:00 公開。
   - 下午：配音做好後，在 YouTube Studio 傳那 8 條配音音軌，回後台按「已上傳」。
6. **Gemini 語音額度用完（429）就等**：旁白、配音或聽檢遇到 Gemini 忙碌或當天額度用完（`video_speech_upstream_busy`），工人把影片延後，不算進它自己被卡住前的次數（跟本月語音字數用完一樣，是大家的事），額度台灣時間下午 3 點左右重置後自己接著做。代價是那天公開時間往後延，站主接受（「沒額度就晚點發」）。
7. 媒體檔放 repo 外（`<VIDEO_WORKDIR>/<slug>/`），工人只寫 `docs/videos/<slug>/` 的文字檔。

在工作階段裡手做一集（補做、重做或試新規矩）時照 `automated.md` 的指令，`brief.md` 同樣只出〈選題〉表與兩個大綱，撰稿後 `lint` 0 錯誤，另派一個代理照 `prompts/verifier-video.md` 把每則的事實對回站上文章與它的 `sources`；手動推送的片子每一關都等站主（`docs/videos/HANDS-OFF.md`）。成片品管的 policy 項不問「有示範」（站主 2026-10-29 定；`apps/api/app/video_automation/judge.py` 的 `is_daily_brief`）：快報只報新聞，第一集得 0.17。立場、建議、業配三項照常。

第一集（`daily-ai-20261028`）學到的：

- 盲讀一位讀者一次的結果不穩，同一題每次挑不同的句子；改稿後一定換新讀者重讀，`no_detour` 的快報措辭已放寬到單句帶出處的說法不算岔題。
- 兩行的 `big` 卡不要放 `icon`，小字（`sub`）一行內講完，`steps` 的 `detail` 十個字左右；第二行被切掉、看起來壓在白條下，`render` 從 2026-10-31 起會自己縮字，縮不下就擋，主機工人再交撰稿模型只縮短那幾張卡的字（2026-10-31 起，`fixLayout`；10/30 那集第一次就被擋了 6 張）（`docs/videos/PAPER.md`；10/29 那集就是被這個切到，站主「字被底部白條蓋住」），聯絡表還是要看。
- 縮圖右框放頭條的官方圖（2026-10-31 起，`flow.mjs` `leadPicture`、`lead-picture.mjs`）：畫面之前，工人讀 `video.json` 第一個不是本站的來源頁的 `og:image`，整張放進框裡、四周補模糊底（`PAD_FILTER`），存成 `docs/videos/<slug>/lead.jpg`，在 `assets[]` 寫出處與授權，版型用 `a`（卡片）免得字標被標題壓住。每集只試一次；找不到圖就維持原樣。縮圖大標從同一天起跟卡片一樣嚴格：最後一行不會再被切掉下半（10/29 印尼文「keliru」、葡文「errada」），日文改成照詞組斷行。
- 縮圖改成 AI 版型（站主 2026-11-01，`visuals.md` §縮圖）：圖鋪滿整張，左上「AI 科技快報｜日期」由範本寫，底部一行「主角＋**鉤子**」加一行副標。圖的順序：先由網站的生圖模型照這集的版畫風格畫一張不帶字、不畫 logo 的圖（`flow.mjs` `briefPicture`、`lead-picture.mjs` `briefPicturePrompt`，約 US$0.1 一張，站主同意），存成 `brief.jpg`、在 `assets[]` 記出處；畫不出來（設定分頁的「投影片影片的插畫」沒開、沒額度、工作失敗）才改抓頭條官方頁的 og:image，改成鋪滿 16:9；兩者都沒有就是深色底。各試一次。八種語言的縮圖照舊由 `render` 依 `i18n/<locale>.json` 各出一張，用同一張圖。官方分享圖常是印著字的通用卡（10/29 那張只寫「OpenAI Deployment Safety Hub」），所以生圖排在前面。
- 刪掉一句有 `reveal` 的旁白時，同場景 `keys` 的數量要跟著減，否則 `render` 擋下。
- Gemini 語音當天額度用完會回 429，台灣時間下午 3 點後重置；配音排在那之後最穩。
- 主機做的第一支（`daily-ai-20261029`）是深色舊版型、沒有關鍵句帶：快報的撰稿規矩換掉了教學規矩，紙底與 `key`／`keys` 那段也一起掉了（站主 2026-10-30「怎麼感覺是舊式的」）。現在 `settle()` 對 `daily-ai-` 一律寫 `theme: "paper"`，`DAILY_BRIEF_RULES` 要每景寫關鍵句；還沒上架、沒有紙底的快報，工人在畫之前請撰稿模型只補關鍵句，只收 `key`／`keys`，旁白一字不動，接著重畫、重組、重送成片卡（`flow.mjs` `restyleDailyBrief`）。
- 雲端工作階段 render 前要讓 Playwright 找得到容器的 Chromium（版本對不上時，把 `PLAYWRIGHT_BROWSERS_PATH` 指到一個把期望版本名連到既有瀏覽器的目錄）；片頭片尾用 `branding --pull` 從站上拿。

## 五、試做後要量的

上架七天後，把每集的平均觀看時長、CTR、留存曲線在第幾分鐘掉最多，寫回票的〈Notes〉；比較各集排第一則的類型（新模型、資安、價格）跟留存的關係，決定排序理由要不要改權重、開場要不要換寫法。公開時間被 429 往後延的那幾天另外標出來，別跟內容的影響混在一起。
