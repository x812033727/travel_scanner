---
name: youtube-video
description: 製作 YouTube 教學與解說影片的完整流程，分兩條路線。全自動：AI 撰稿與查核、伺服器用 Gemini（或 Azure）合成台灣口音旁白、深色投影片版型、ffmpeg 合成、五語 CC，工具在 tools/video。人工錄製：口播稿、分鏡、字卡、螢幕錄影、剪輯交接。兩條都涵蓋選題與格式、查核、畫面與縮圖、章節、字幕、上架包與上架前檢查。要做一支 YouTube 影片、把 Mokaair 文章改成影片、寫口播稿或分鏡、合成旁白、做縮圖、排章節、寫影片說明或上字幕時，先讀這個 skill。Produce Mokaair YouTube videos, fully automated through tools/video or recorded by the owner, from topic to upload.
metadata:
  short-description: YouTube 影片：全自動或人工錄製，從選題到上架
---

# YouTube 影片製作（youtube-video）

目標是像「AI 模型這麼多，到底該怎麼挑？」（觀點解說）和「Claude Code 近期更新彙整」（更新彙整＋示範）那樣的中文科技影片：畫面是字卡、截圖、螢幕錄影交錯，每一段都回答一個觀眾真的會問的問題。代理負責**企劃、查核、稿子、畫面素材、上架文字**；按下「發布」永遠是站主的事。

路徑都相對於 repo 根目錄 `<ROOT>`；一支影片一個工作目錄，開在 repo 外（影片與音檔絕不進 git，repo 是公開的）。

## 什麼時候用、什麼時候不用

- 用：從零做一支影片；把站上的 AI／科技文章（`docs/claude-code-series`、`docs/ai-workflow-series`、各期 AI 新聞）改成影片；只要口播稿、分鏡、縮圖或上架文字其中一項。
- 不用：寫或發布網站文章（content-pipeline）；影片裡要提到的事實還沒查過又趕著要稿子——先查，不然就不做。

## 先選路線

| 路線 | 成品 | 誰做什麼 | 從哪裡開始 |
| --- | --- | --- | --- |
| **全自動** | 深色投影片＋台灣口音合成旁白＋五語 CC，8–12 分鐘 | 代理企劃、撰稿、查核，工具合成旁白、畫面與成片；站主選大綱、聽旁白、看成片、自己上傳 | 下面「全自動路線」與 `.agents/skills/youtube-video/references/automated.md` |
| **AI 漫劇** | AI 生成的鏡頭片段＋旁白與角色配音＋燒錄繁中字幕＋配樂＋五語 CC，2–4 分鐘一集 | 代理寫故事聖經、劇本與分鏡，工具生成設定圖、關鍵影格、片段、音樂並合成；站主選大綱、選角色設定圖、聽旁白、看分鏡、看成片、自己上傳 | `.agents/skills/youtube-video/references/drama.md`（設計在 `docs/videos/DRAMA.md`） |
| **人工錄製** | 站主出鏡或配音、螢幕錄影、剪輯 | 代理交稿子、分鏡、字卡、上架文字；站主錄音、錄影、剪輯 | 下面「人工錄製路線」 |

站主沒指定時：AI／科技資訊、工具介紹、概念解說走全自動；故事（神話、民間傳說、原創玄幻、站上文章改成的故事）走 AI 漫劇；要真人示範操作、或站主想自己出鏡的走人工錄製。全自動的螢幕錄影手把手還在做（票 `2026-09-24-video-screencast-steps`、`2026-09-24-video-terminal-template`、`2026-09-24-video-obs-import`），做好之前這類影片走人工錄製。

## 再讀對應的 reference

| 你要做的 | 讀 |
| --- | --- |
| 決定是哪一種影片、每段多長 | `.agents/skills/youtube-video/references/formats.md` |
| 寫口播稿（口語、節奏、開場 30 秒；給 TTS 唸的寫法在最後一節） | `.agents/skills/youtube-video/references/script-writing.md` |
| 字卡、截圖、螢幕錄影、縮圖 | `.agents/skills/youtube-video/references/visuals.md` |
| 標題、說明、章節、字幕、揭露、上架檢查；全自動的上架包 | `.agents/skills/youtube-video/references/publish.md` |
| 人工錄製的稿子格式（`video_kit.py` 讀得懂的寫法） | `.agents/skills/youtube-video/references/script-format.md` |
| 全自動：一次性設定、主幹、指令、結束碼、發音、成本、坑、主機自動產線 | `.agents/skills/youtube-video/references/automated.md` |
| 全自動的代理提示 | `.agents/skills/youtube-video/references/prompts/`（`planner.md`、`writer-video.md`、`verifier-video.md`、`caption-translate.md`、`caption-review.md`） |
| AI 漫劇：一次性設定、主幹與關卡、指令、`video.json` 的角色與鏡頭、品檢與重做、成本、坑 | `.agents/skills/youtube-video/references/drama.md` |
| AI 漫劇的代理提示（故事聖經、劇本與分鏡、連貫性查核、修鏡頭） | `.agents/skills/youtube-video/references/prompts/planner-drama.md`、`writer-drama.md`、`verifier-drama.md` |
| 頻道規格：版型、配色、聲音、片頭片尾、說明欄範本 | `docs/videos/README.md` |
| 全自動的設計理由、YouTube、Azure 與 Gemini 語音的官方規則 | `docs/videos/DESIGN.md` |

## 不變的規矩

1. **一支影片只回答一個問題。** 標題問什麼，影片就在前 30 秒承諾答案、在最後一章給出答案。講不完就拆成兩支。
2. **每個版本號、價格、上限、日期、功能名稱都在當天的官方頁確認**，寫進稿子最後的 `## 來源`，附確認日期。更新彙整類的影片最容易過期：稿子第一行寫「錄製日期」，說明欄也寫。找不到官方說法的東西，影片裡就說「以官方公告為準」，不講數字。
3. **意見要標成意見。** 「我覺得」「我的用法是」可以講；排行榜、跑分、別人的評測要說出處。沒有實測過的東西不能講成「我測過」。
4. **錄影畫面不能露出任何秘密或個資**：API key、token、email、帳單、客戶名稱、瀏覽器分頁與書籤、終端機的提示字元裡的使用者名稱與主機名。錄之前開乾淨的 profile 與示範用的目錄；剪輯後逐格檢查一次。這一條出事就是撤片。
5. **對外請求**（查核時抓官方頁）的 User-Agent 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不帶任何人的 email 或姓名。
6. **只用有授權的素材**：音樂用 YouTube 音效庫或已購授權；別人的影片、截圖、Logo 只在評論必要時短暫引用並標出處；縮圖不用別人的照片。
7. **上架是站主的動作。** 代理不登入 YouTube、不按發布、不改公開狀態；交出上架包，列出需要站主決定的欄位（付費宣傳、合成內容揭露、兒童設定）。
8. **檔案先落地**：每完成一段稿子就存檔，session 被切斷時留下的是檔案，不是對話。
9. **金鑰與權杖不經過代理。** 旁白的金鑰（Gemini 用網站既有的金鑰，Azure 由站主填）只在正式站後台；本機工具的影片工具權杖靠 `login` 配對取得：代理把印出的連結交給站主，站主在後台按「允許」，權杖直接寫進本機檔案。權杖不能出現在對話、檔案或指令參數裡。

## 全自動路線

工具是 `node <ROOT>/tools/video/cli.mjs <子指令>`，每個子指令都讀 `docs/videos/` 底下這支影片的 `video.json`，產物寫到 `<VIDEO_WORKDIR>/<SLUG>/`（`<VIDEO_WORKDIR>` 預設在使用者家目錄下，用 `--workdir` 或環境變數 `VIDEO_WORKDIR` 改）。完整步驟、一次性設定與坑都在 `automated.md`，這裡只列骨架。

| # | 階段 | 誰 | 關卡 |
| --- | --- | --- | --- |
| 1 | 企劃：`brief.md`，含「站主觀點」「觀眾看完能做到的事」與 2–3 個大綱 | 企劃代理（`prompts/planner.md`） | `review-push` → **站主在 `/admin/videos` 選大綱** → `review-pull` |
| 2 | 撰稿：`video.json`＋`claims.md`，新英文詞補進發音字典 | 撰稿代理（`prompts/writer-video.md`） | `lint` 零錯誤 |
| 3 | 查核：換人；改超過 3 個事實就第二輪再換人 | 查核代理（`prompts/verifier-video.md`） | `verify-1.md` 完成 |
| 4 | 聽眾優先審稿：口語、句長、術語唸法、開場鉤子 | 審稿代理 | 協調者套用修正、`lint` 再過 |
| 5 | `tts`：先 `--dry-run` 看字數與額度，再實際合成 | 工具 | 時間軸寫出、章節時間檢查過 |
| 6 | `check-audio`（Jev 判斷）→ 被標的句子 `tts --redo` → `review-push` | 工具、站主 | **站主在 `/admin/videos` 核准旁白** → `review-pull` |
| 7 | `render` → `assemble` → CC 翻譯與 `captions` | 工具、翻譯代理 | 聯絡表看過；`checks.json` 全過；沒有過期翻譯 |
| 8 | `review-push` 送 720p 成片 | 站主 | **站主在 `/admin/videos` 看完全片** → `review-pull` |
| 9 | `package` → `review-push` 送上架確認 → 站主照 `UPLOAD.md` 在 Studio 上傳成「私人」，檢查後自己按公開 | 站主 | 站主按「確認可以上架」；影片 ID 寫回 `video.json` |

`status --slug <SLUG>` 隨時印出做到哪一步、下一個指令是什麼。核准綁檔案雜湊：稿子或旁白改了，舊的核准自動失效，後面的指令會以結束碼 3 拒絕，要重新 `review-push`。後台頁用不了時，才用有選項的提問問站主，再 `approve --gate …` 記下。

## 人工錄製路線

一支影片一個工作目錄 `<WORKDIR>`，開在 repo 外。`<KIT>` 是 `python3 <ROOT>/.agents/skills/youtube-video/scripts/video_kit.py`，只用標準函式庫，任何 python 3.10+ 都能跑。

### 主幹

| # | 階段 | 產出（都在 `<WORKDIR>`） | 關卡 |
| --- | --- | --- | --- |
| 0 | 選題：觀眾會怎麼搜尋、這支回答哪個問題、選格式、目標長度 | `brief.md`（一句話問題、目標觀眾、格式、長度、參考影片） | 站主同意題目與格式 |
| 1 | 查核：列出影片裡會出現的每個事實，逐一在官方頁確認 | `facts.md`（事實、來源 URL、確認日期） | 沒有「待查」的事實 |
| 2 | 口播稿：從文章起稿用 `<KIT> from-article`，否則照 script-format 手寫 | `script.md` | `<KIT> check` 零 FAIL；開場 ≤ 30 秒；站主讀過一遍 |
| 3 | 畫面：每段的字卡、截圖、錄影清單；字卡與縮圖用 HTML 渲染 | `shots.csv`、`slides/*.png`、`thumbnail.png` | 每張 PNG 打開看過：字不超框、手機縮小也讀得到 |
| 4 | 錄製（站主）：讀稿機文字、錄音、螢幕錄影 | `teleprompter.txt`；站主的音檔與錄影 | 錄影逐段對過規矩 4 |
| 5 | 剪輯交接：把分鏡表與素材交給剪輯（站主或剪輯師） | `handover.md` | 剪輯知道每段要用哪個素材 |
| 6 | 上架包：標題 3 案、說明、實際章節時間、標籤、字幕稿、置頂留言 | `upload.md`、`transcript.txt` | `<KIT> metadata --chapters` 用剪完的時間重產；publish.md 的清單全打勾 |
| 7 | 上架後：確認章節有出現、字幕有同步、連結可點；有錯就更正並記在 `ERRATA.md` | — | 站主確認 |

### 指令

```bash
# 從站上的文章起一份稿子骨架（標題變章節、段落變素材註解、表格變字卡建議、來源帶過來）
<KIT> from-article <SLUG> --out <WORKDIR>/script.md [--locale zh-TW]
# 檢查稿子：每章估計長度、總長、開場長度、章節 ≥ 10 秒、長句、書面語、沒有畫面指示的長段
<KIT> check <WORKDIR>/script.md [--cpm 250]
# 讀稿機文字（一句一行），也是上傳 YouTube 自動對時字幕用的逐字稿
<KIT> teleprompter <WORKDIR>/script.md --out <WORKDIR>/teleprompter.txt
# 分鏡表：每個畫面指示一列，含估計開始時間
<KIT> shots <WORKDIR>/script.md --out <WORKDIR>/shots.csv
# 字卡與縮圖：slides/ 下每個 .html 渲染成 1920x1080 PNG，thumbnail*.html 渲染成 1280x720
<KIT> render <WORKDIR>/slides
# 上架文字：先用估計時間出草稿；剪完後把實際章節時間寫進 chapters.txt 再產一次
<KIT> metadata <WORKDIR>/script.md [--chapters <WORKDIR>/chapters.txt] --out <WORKDIR>/upload.md
```

`render` 找瀏覽器的順序：`--chromium`、環境變數 `CHROMIUM_BIN`、`PLAYWRIGHT_BROWSERS_PATH` 底下的 Chromium、PATH 上的 `chromium`／`google-chrome`。字卡與縮圖的起手範本在 `.agents/skills/youtube-video/references/templates/`，複製到 `<WORKDIR>/slides/` 再改字。

## 交接

- 全自動：狀態由 `status --slug <SLUG>` 從檔案算出來，不必另外記。停手前在票的 Notes 寫下目前階段、等站主的是哪一個關卡、有沒有沒解決的查核項目。**不要改 `brief.md`**：大綱的核准綁它的雜湊，改一個字就要重新核准。
- 人工錄製：停手前把 `brief.md` 最上面的狀態行改成目前階段（例如「階段 3：字卡做了 5／8 張，縮圖未做」），並列出下一步。站主要的只有三樣東西：讀稿機文字、分鏡表與素材、上架包。
