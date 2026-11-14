---
name: curio-episode
description: 奇聞檔案局（slug 以 curio- 開頭的歷史與奇異解說長片）的做法：系列定案不能改的事、照黑猫研究院十步的架構（鉤子＋承諾句，不先濃縮劇情）、2026-11-14 定案升級版「劇場級動畫光影 × 厚塗水粉質感」內建 generate_image 生圖與 keyframes import 匯入（停用 MiniMax 生圖、角色設定圖 ImagePaths 鎖定、四格 2x 放大獨立審圖）、不用卡片也不放文字、在世或 1956 年後過世的人不入畫、英文名照原文念、中文 Gemini Sulafat（≥4.4 字／秒）＋八語 MiniMax 配音、每 30–45 秒一個鉤子與配樂、片頭片尾與 Shorts。lint 對 curio- 的 slug 檢查系列畫風、插圖占比至少七成、連續卡片最多三張（舊集的上限；新集一張卡都不寫）。要做、重做、續做或修任何一集奇聞檔案局（含 H01–H07、M、P、S、U、L、F、G 各題與它們的 v2），或改它的畫面、提示詞、卡片時，先讀這個 skill，再讀 youtube-video。Make or remake a 奇聞檔案局 (curio-*) episode in the series look.
metadata:
  short-description: 奇聞檔案局：劇場厚塗水粉畫風、內建生圖匯入、插圖驗收、檢查
---

# 奇聞檔案局（curio-episode）

奇聞檔案局是一個**劇場級動畫光影 × 厚塗水粉插畫**配一個說書旁白的歷史與奇異系列：每一集講一個真實的怪事，像講故事一樣講到底。**2026-11-14 起全系列停用 MiniMax 生圖**：關鍵影格一律用代理內建 `generate_image`（`AspectRatio: "16:9"`）套用五大質感配方生成，經獨立子代理四格 2 倍放大審圖後以 `keyframes import --provider external --usd 0` 匯入；2026-11-05 起不用卡片、畫面不放任何文字（§不用卡片）。這份 skill 是系列的固定做法；通用的步驟（旁白、合成、上架包、配音、Shorts）仍在 `youtube-video`。

2026-10-14 為什麼有這份 skill：H04–H06 重製時，負責的模型沒讀到系列的畫面規則（只寫在 `docs/videos/history-curiosity/look.md`），把插圖當證據重建、一張一張向站主要授權，試圖連續被自己退回，最後整集變成 88 張文字卡、0 張插圖，跟 H01–H03 完全不像一個頻道。下面每一條都是為了不再發生。

## 先讀

1. 參考片 `docs/videos/curio-h01-v2/video.json`：動筆前讀前 30 景，看一張圖配一兩句的節奏（現改為同節拍 2–3 句併一景）。它有 7 張卡片；2026-11-05 起不用卡片，2026-11-14 起插圖生圖與提示詞照 §插圖生圖與提示詞怎麼寫（2026-11-14 定案）。
2. `docs/videos/history-curiosity/README.md`（系列企劃與站主的決定）、`docs/videos/history-curiosity/look.md`（2026-11-14 劇場級動畫光影×厚塗水粉質感定案與英文基底句）。
3. 稿子：`.agents/skills/youtube-video/references/script-writing.md` §故事主線與鉤子（一條故事線、`loops` 表、片尾不點名下一支）與 §奇聞檔案局與品牌故事的架構（2026-11-05：黑猫研究院的十步，鉤子＋承諾句，不先濃縮劇情；顯性「還記得開頭…嗎？」留頭尾最多 2 次，最後一章章名寫總結收束句）。

## 系列定案（改任何一條都要先問站主）

| 項目 | 定案 | 來源 |
| --- | --- | --- |
| 畫面與生圖 | **2026-11-14 起全面改用代理內建 `generate_image`（`AspectRatio: "16:9"`）生成「劇場級動畫光影 × 厚塗水粉質感」插圖，再用 `keyframes import --provider external --usd 0` 匯入；嚴禁用 MiniMax 生圖，亦不由手寫 SVG 充數**。遇到 `gemini-3.1-flash-image` 配額冷卻時，先跑八語翻譯、配音與 `check-audio`，分批等待配額恢復，絕不退回 MiniMax | 站主 2026-11-14「畫圖用你生成的不要用 minimax」「以後用這樣的風格」 |
| 畫風設定 | `video.json` 頂層仍寫 `look: { "preset": "cute-mystery" }`（不寫 `style`、`negative` 留空）以通過系列 lint（`tools/video/core/curio.mjs`）；實際 `generate_image` 的每鏡 Prompt 必帶「劇場級動畫光影 × 厚塗水粉質感」英文基底句（見 §插圖生圖與提示詞怎麼寫） | 站主 2026-10-10、2026-11-14；`tools/video/core/curio.mjs` |
| 照片 | 2026-11-05 起新集不用：照片卡也是卡片（§不用卡片）。之前可放，限公有領域（CC BY 不用），做成貼圖式照片卡 | 站主 2026-10-10、L08、2026-11-05 |
| 人物與設定卡 | 1956 年以前過世（70 年以上）可入畫（Prompt 用年代／身分／服裝描述，不寫真名）。**單一可入畫歷史人物或串場研究員只要跨 ≥ 4 鏡出場，開畫前必先用 `generate_image` 產一張角色設定圖（鎖死五官、髮色、髮型與主色服裝），每鏡出場時 `ImagePaths` 必傳該設定圖**（重繪既有鏡頭時一併傳前一版圖檔）。**在世或 1956 年後過世的人不入畫**，連「代表他的路人」也不畫：講到他們時畫串場角色、物件，或明顯是一般人的匿名角色（§誰可以入畫） | README §內容守則；站主 2026-11-05、2026-11-14 |
| 長度 | **2026-11-01 站主改為看內容決定：至少 8 分鐘、最多 13 分鐘**（「≥8 分鐘都可以」）。片長跟著素材走：撐不住就剪短，或跟同一個核心問題的兄弟題排成一集，不用重述、停頓或慢唸補時間。後台建立單集時照題案的 `target_minutes` 選（`docs/videos/history-curiosity/pool/THEMES.md`；沒有題案的單題照題卡素材估，至少 8 分鐘），正文約 4.5 字／秒：8 分鐘約 2,100 字、13 分鐘約 3,500 字。2026-10-25 曾定一律 13 分鐘（參考頻道中位 13–31 分，§跟高點閱頻道的差距），已被這條取代；已製作與製作中的集照原本的長度 | `docs/videos/long-form/README.md`；`docs/videos/channel-review-20261025-story-series/README.md` |
| 片頭片尾 | 頻道片頭放在第一章（鉤子＋承諾句）之後（`intro_at` = after_first_chapter）；片尾 v4-endscreen，旁白不提下一支 | `docs/videos/BRANDING.md` |
| 語速與停頓 | **2026-11-13 站主：實測語速至少 4.4 字／秒**（字數不含標點，除以每句錄音長度加總，不算句間空白）；停頓照 PR #2069：`"pauses": {"line_ms": 0, "scene_ms": 150}`、`"still_motion": "beat"`。**不符合的集數一律重做**，連已核准、待上傳的也重做；重錄旁白時八語配音一起改用 MiniMax（PR #2085），中文旁白維持 Gemini `Sulafat`。聲音指示寫「一秒四到五個字」只念到約 4.1–4.3（Gemini 會打折扣），要寫得比目標快（見 §稿子 的語速） | 站主 2026-11-13「不符合的都要重製」「重錄的話八語就用 minimax」 |
| 八語 | **2026-11-13 起每集預設八語都做**（en、ja、ko、es、pt、id、vi、th：標題說明、CC、配音）。工具的 `DEFAULT_LOCALES` 仍只有 zh-TW、en、ja、ko，所以每集要明確選這八個語言（站台的語言勾選／`languages.json`，`i18n-sheet --locale en,ja,ko,es,pt,id,vi,th`、`dub --locale <loc> --provider minimax` 逐一跑），不能靠預設；外語配音固定用 MiniMax；外語標題要在手機清單寬度內（lint `at most 36`），外語縮圖標題手機寬度 ≥ 24 px；外語（尤其泰文，每字 3 bytes）組完說明欄壓在 `< 4,500` UTF-8 bytes 安全區間 | 站主 2026-11-13、2026-11-14 |
| 語言 | zh-TW 先做完（Gemini `Sulafat`）；外語照上一列「八語」全做（MiniMax） | `docs/videos/DUBS.md` |
| 鉤子 | 跟品牌故事一樣密：正文每 30–45 秒一個懸念，沒有超過 45 秒的空檔；`loops` 十分鐘至少 8 個；每章停在一個沒解的問題上 | 站主 2026-10-19「品牌故事比較順也有比較多鉤子」；lint 的 `TIGHT_CADENCE`（`tools/video/core/narrative.mjs`） |
| 架構與口吻 | **2026-11-05 起照黑猫研究院十步**：鉤子（問句或情境＋終點多大×起點多小，最多 1–2 個高潮標籤，不講過程、不先濃縮劇情）→ 承諾句「今天我們就來聊聊…」（約 0:40–1:05）→ 時代與起源 → 第一次起落 → 升級關卡 2–4 個 → 最大危機或反轉 → 翻身與揭曉（「還記得…嗎？」顯性提示全片留頭尾最多 2 次，中段直接講事實）→ 尾聲「故事還沒結束」→ 主題收束（最後一章章名寫總結收束句，不拿花絮當最後章名）→ 提問＋訂閱；大方向照時間順序，倒敘只做小段且有時間提示；全片不能沒頭沒尾。說給一個人聽：每章至少一句「你」、一句旁白自己的反應，lint 低於每千字 2 個「你」警告；標題公式見 §標題與縮圖 | 站主 2026-11-05；`script-writing.md` §奇聞檔案局與品牌故事的架構；`register.mjs` `STORY_OPENING_RULE`、`TOLD_TO_ONE_VIEWER` |
| 畫面上的字 | **不用卡片、畫面不放任何文字**（走全球市場）：數字講出來、畫成圖；章名只放在 YouTube 說明欄的章節（工具從 `chapter` 欄位寫）；縮圖保留文字，每個語言各做一張 | 站主 2026-11-05；`register.mjs` `STORY_SERIES_SCREEN_RULE` |
| 英文名稱 | 人名、公司、作品、地名只要是英文（或其他拉丁字母）就**寫英文、念英文**，不硬翻成中文音譯（Pigafetta 不寫「皮加費塔」）；中英之間空一格；不寫中文音譯的 `say`；台灣慣用的正式中文名例外（三星、華為、維基百科、麥哲倫）；新的英文詞在 `docs/videos/lexicon.json` 記 `null` | 站主 2026-11-05；2026-11-08「如果是英文就用英文不要硬翻譯 不然會怪怪的」 |
| 配樂 | 每一集都有：`"music": {"prompt": "light, curious, a little mysterious, no vocals", "gain_db": -20, "duck_db": -10}`，跟品牌故事同樣的音量；沒有配樂 lint 會警告 | 站主 2026-10-19「而且有音樂」；`tools/video/core/curio.mjs` 的 `CURIO_MUSIC` |

## 選路線（2026-11-14 更新）

| 情況 | 路線 | 怎麼做 |
| --- | --- | --- |
| **新的一集（現行預設）** | 本機／雲端對話漫劇格式＋內建 `generate_image` 匯入 | `format: "drama"`、`look: { "preset": "cute-mystery" }`、`characters: []`、`"pauses": { "line_ms": 0, "scene_ms": 150 }`、`"still_motion": "beat"`；全部關鍵影格由代理內建 `generate_image`（`AspectRatio: "16:9"`）套用劇場級動畫光影×厚塗水粉基底句生成（角色跨 ≥ 4 鏡時先產角色設定圖並傳入 `ImagePaths`），經獨立子代理四格 2 倍放大審過後，逐鏡以 `node tools/video/cli.mjs keyframes import --slug <SLUG> --shot <ID> --file <PNG> --provider external --usd 0` 匯入，**不跑 MiniMax `keyframes` 生圖** |
| **重製已交付的一集**（改稿、改開場、換片頭片尾） | 本機 recut | `docs/videos/curio-five-recuts-20261012/README.md`；既有已核准插圖可保留，新景或重繪鏡頭一律改用內建 `generate_image`＋`keyframes import --provider external --usd 0`（重繪時將原圖一併傳入 `ImagePaths` 鎖定構圖） |
| **主機自動解說路線（歷史參考）** | 主機 `explainer-series.mjs` | 早期主機工人綁定 `image-01` 的自動化路線（`docs/videos/explainer-route/DESIGN.md`）；2026-11-14 站主定案停用 MiniMax 生圖後，新集一律走第一列內建生圖匯入路線 |

**同一位歷史人物要在很多張圖裡長得一樣時**（2026-11-14 更新）：單靠提示詞文字鎖不住臉與穿搭（`curio-m17` 瑪麗・雪萊未傳設定圖，6 鏡換了 6 套髮色與洋裝）。只要單一可入畫人物（過世滿 70 年的歷史人物，或虛構的檔案局串場研究員）在單集出場 ≥ 4 鏡，開畫前先用 `generate_image` 產一張 16:9 角色設定圖（鎖死五官、髮色、髮型、主色年代服裝），之後該人物出場的每一鏡都在 `generate_image` 的 `ImagePaths` 傳入該設定圖；`video.json` 的 `characters` 維持 `[]` 即可（奇聞檔案局只有旁白：任何一句的 `speaker` 寫成角色 id，`lint` 就報錯，`core/drama.mjs` `isNarratedExplainer`）。在世或 1956 年後過世的人照舊不入畫，不要為他們建角色設定圖。

**句間停頓**（站主 2026-11-05）：預設每句後停 0.3 秒、換場再停 0.7 秒，加上配音本身的尾音，成片靜音佔 7–10%，評分卡的目標是 3% 以下。奇聞的 video.json 加 `"pauses": { "line_ms": 0, "scene_ms": 150 }`（只能比預設短）；改了之後時間軸會變，旁白與分鏡都要站主重新核准，配音不必重錄。
**插圖的動法**（同日，參考黑貓研究院）：預設整張圖慢慢飄、而且多半往裡推，站主嫌「只會一直放大」。video.json 加 `"still_motion": "beat"`：插圖輪流用推近、右移、拉遠、左移、上搖（camera 寫了方向就照寫的），整段都在動、幅度比預設大；圖與圖之間淡入淡出，章節開頭硬切。只動合成，不必重畫、不必重新核准分鏡。
**2026-11-11 起這兩項是系列預設**（站主「改成系列預設」；奇聞檔案局與原來如此事務所都是，`core/curio.mjs` `SERIES_PACING`）：主機路線的 `settle()` 在撰稿沒寫時自動補上；**用 Claude 對話／雲端配對影音權杖做片走的是本機路線（不經主機 `settle()`），`video.json` 必須自己明寫 `"pauses": { "line_ms": 0, "scene_ms": 150 }` 與 `"still_motion": "beat"`**（S42、B01 漏寫就退回 300／700 毫秒舊停頓與單向慢推）。`lint` 缺哪一項就警告哪一項，照警告補上。
**同節拍多句併一景（禁止全集一句一景）**：講同一個動作、因果或畫面的連續 **2–3 句短句放進同一個 `scene.lines[]`**（一張插圖停留約 4–8 秒），畫面主體換了才開新 `scene`。若寫成 100% 一句一景（S42 92 句拆 73 景、B01 137 句拆 137 景），每一句結尾都變成換景的 `scene_ms`，`line_ms: 0` 完全失效，插圖張數與費用也白白翻倍。
停頓拿掉後同一份稿子估出來的片長會變短：奇聞每句少 0.3 秒（句子原本用預設的 300 毫秒）、每景少 0.55 秒；原來如此每句只少 0.1 秒（它的台詞原本每句寫 `pause_after_ms: 100`，新一集照 [`docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`](../../../docs/videos/so-thats-why/dialogue-pilot-20261103/README.md) §10.6 不再每句寫，只在答案前留一拍）、每景同樣少 0.55 秒。接近片長下限的稿子要多寫內容，不要拉長停頓補時間。

不要用 `format: "slides"` 從零做新集：那是 H01–L08 第一版的試片路線，系列預設與評審都要手動接，H04–H06 就是在這裡偏掉的。

## 稿子：跟品牌故事一樣順、一樣多鉤子

2026-10-19 站主比較兩個系列後說品牌故事「內容比較順也有比較多鉤子，而且有音樂」，要奇聞檔案局做到一樣好或更好。
量到的差距：H10、H11、H12、M09、U09、H01 v2 的最長空檔 69–81 秒，每集有 2–7 段超過 45 秒沒有任何懸念；
品牌故事的撰稿規則是 45 秒。所以：

- **每 30–45 秒（約 130–200 字）一個懸念**：一個問題、一個升級（「但這還不是最怪的」）、一份對不上的紀錄、
  先不講為什麼、或一個轉折。鉤子要站在這個檔案的事實上（日期、數字、某個人的決定、不該出現的東西），
  不寫空話（「接下來更精采」），不念目錄。
- **每章結尾停在一個具體、還沒解的問題或動作上，下一章第一句就接它**。結構裡的「流傳的版本、紀錄、
  最站得住的解釋」是**同一個故事照發生順序的段落**，不是旁白一段一段走過的區塊；章名照事件取。
- **`loops` 十分鐘至少 8 個**，第一章（鉤子＋承諾句）種下至少 3 個（反差、一兩個高潮標籤、承諾句的問題），每一個都要回收。
- 寫完跑 `node tools/video/cli.mjs lint --slug <SLUG>`：curio- 的 slug 用 45 秒、8 個伏筆檢查（警告），
  每一段「no open loop between …」都要讀那一段稿子補上懸念，不是加一個問號湊數。
- 盲評：本機 `node tools/video/cli.mjs narrative --slug <SLUG>` 每一題都過；品牌故事在主機上問兩位讀者、
  兩位都答「否」才算沒過，本機重評時也比照，不要為一位讀者的「否」一直改稿。

## 跟高點閱頻道的差距（2026-10-25 量的）

站主 2026-10-25 問「奇聞檔案局跟品牌故事跟別人點閱率高的影片差異在哪」。用 yt-dlp 抓三個參考頻道最近 120 支的
觀看與片長、Seiko 那支的字幕時間軸，對照我們已上架的集數（完整報告與數字在
`docs/videos/channel-review-20261025-story-series/README.md`）。只寫量得到的差距，依影響排序：

| 項目 | 黑猫研究院（品牌故事的參考） | 馬臉姐／cheap（奇聞檔案局的參考） | 我們（H01 v2、S01、H12、C01） | 這份 skill 改了什麼 |
| --- | --- | --- | --- | --- |
| 觀看 | 近 120 支中位 3.75 萬，最高 78.5 萬（Seiko，20:32） | 馬臉姐中位 53.7 萬（片長中位 31 分）；cheap 中位 58.7 萬（15 分） | 奇聞檔案局 14 支 0–7 次；品牌故事 0 支公開（清單還是私人） | — |
| 語速 | 5.1 字／秒，全片沒有 1.5 秒以上的空檔 | — | 3.3 字／秒（講話中 3.7） | §稿子 的語速目標 4.5 字／秒；聲音指示的寫法等站主試聽（`voice-audition.md`） |
| 開場 | 前 26 秒講這件事差點改變什麼（對觀眾說），40 秒給數字，66 秒一句「今天我們就來聊聊 Seiko 當年到底有多瘋狂」；**不預告任何時刻** | 老高 22 秒進場景 | 一個場景之後連丟 4–5 個沒有脈絡的線索（劍、酒精、小說、礁石） | 開場改成利害 → 場景 → 最多兩個預告 → 一句承諾句 → 問題（`register.mjs` `STORY_OPENING_RULE`；盲評題目換成系列版 `STORY_SERIES_PANEL_QUESTIONS`） |
| 對觀眾說話 | 20 分鐘「你」26 次、「我」18 次、「大家」5 次；有反應（「這聽起來像科幻小說」）、有觀點、結尾問觀眾戴什麼錶 | 本人出鏡，全程對鏡頭講 | H01「你」1 次、「我」2 次；C01 兩個都是 0；像在唸檔案 | 每章至少一句「你」、一句自己的反應；lint 低於每千字 2 個「你」會警告（`narrative.mjs` `viewerAddressProblems`） |
| 標題 | 名字在前 6 字＋利害動詞（摧毀、統治、死活不用）＋問號；10 支前 10 名 9 支問句、7 支有強詞 | 馬臉姐全是斷言＋數字＋驚嘆號；cheap 用【】框問題 | 平靜的閱讀題：「燈塔的故事改了哪裡？」「三個人失蹤後…」 | 標題公式寫進 §標題與縮圖；主機 `titleGuide` 同步 |
| 縮圖 | 亮底、黃字黑邊兩行大字（6–8 字＋8–12 字副標）、看得出的東西本身（手錶、米其林寶寶、A4 紙、Dolby 標誌）、一張有表情的臉 | 同上，加本人；cheap 全是誇張表情的角色 | 深青底、6 字小標、標籤膠囊、暗色插圖、沒有表情特寫 | **2026-10-25 做了 bold 版型**（`templates.mjs` `THUMB_BOLD_LAYOUT`，curio-／story- slug 預設 layout d：圖滿版、黃字黑邊大標、白字副標、無膠囊）；`headline` 選最有利害的 6 字、`sub` 寫一句利害、`shot` 選表情特寫 |
| 長度 | 中位 13 分（11–21 分） | 馬臉姐 23–40 分、cheap 9–24 分 | 目標 10 分、正文 8 分（2,100–2,600 字） | **2026-10-25 站主定 13 分**：正文約 3,500 字（品牌故事 `series.json` 已改）；**奇聞檔案局 2026-11-01 改為 8–13 分看內容**（見上表〈長度〉） |
| 字幕 | 每格燒錄字幕、關鍵字黃色 | 同 | 不燒（站主 2026-10-08 定） | 2026-10-25 站主改試燒；**2026-10-31 定案：奇聞檔案局燒繁中字幕，品牌故事不燒**。主機 cute-mystery 單集由 `flow.mjs settle()` 設 true，本機路線的 `video.json` 要明寫 `"subtitles": {"burn_in": true}`（預設是 false，lint 會警告）；品牌故事 `story.mjs` 是 false；其他語言都是 CC |
| 頻道 | 單一類型、每天一支、120 支在四個月內 | 單一類型 | 一個頻道混六個系列（AI 新聞、AI 名詞、教學、漫劇、奇聞、品牌） | 不是 skill 能改的；報告 §決定 |

把上面的變成稿子規則（撰稿提示、lint、盲評都已照這一節改）：

- **開場**：這裡 2026-10-25 定的「開場五步」已由 2026-11-05 的十步架構取代（§系列定案〈架構與口吻〉、
  `script-writing.md` §奇聞檔案局與品牌故事的架構）。留下來的是同一個觀察：觀眾還沒有脈絡時，連丟線索聽起來像清單。
- **說給一個人聽**：每章至少一句轉向觀眾的「你」（他用的、有的、聽過的、會怎麼做）；每章一句旁白自己的反應（「這就很怪了」）；
  意見標成意見；一集一兩次拿共同經驗開玩笑。事實一個字都不改。
- **語速**：正文目標 4.5 字／秒（參考頻道約 5，我們 3.3）；句子用連接詞接著講，事實後面接它對某個人的意義。10 分鐘的集數
  正文約 2,700 字起算，不是 2,100。聲音指示 `STORY_VOICE_STYLE` 2026-10-25 已加「語速像平常聊天，一秒四到五個字，句與句之間不拖」（站主定）；
  主機用的是後台設定分頁貼的那一份，**站主要把這句貼上去**；它在 `speechHash` 裡，舊片不重錄。
  **2026-11-13 改**：實測只有 4.1–4.3 字／秒，站主定「至少 4.4、不符合的重做」（§系列定案〈語速與停頓〉）。原來如此實測過的寫法是「語速像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音」（`docs/videos/lessons/sothatswhy.md` 2026-11-11），奇聞照用；錄完看 `tts` 印出的實測語速（或量 `timeline.json` 的 `audio_samples`），若 Gemini 仍把語速打折在 4.1–4.3 字／秒，可在 `voice` 加 `"tempo": 1.08`–`1.15`（`ffmpeg atempo` 不變調微加速，`1 <= tempo <= 1.5`）再跑 `tts`，確保實測 ≥ 4.4 字／秒才送審。
- **結尾**也是對話：答案、「如果你…，留言告訴我」、訂閱的理由；可以說「好啦，這就是今天的故事」，仍然不講下一支。

## 標題與縮圖（2026-10-25；2026-11-13 審片補齊）

- 標題：**大家認得的名字放前 6 字**（船、地方、人、事件、品牌）＋**一個利害或反常的詞**（消失、不敢、騙過、差點、全部、真相、
  憑什麼）＋一個數字或年份＋問號；後綴照舊「｜奇聞檔案局」或「｜品牌故事」；後綴前最多 30 字。
  例：「十個人全部消失，1872 年這艘船為什麼還在走？」「曹操自己放的火？赤壁真正燒船的人是誰」「賣輪胎的公司，憑什麼決定全世界最好吃的餐廳？」。
  不要平靜的閱讀題（「燈塔的故事改了哪裡？」「研究揭露了什麼？」）。
- 縮圖文字（layout e 預設）：
  - `headline`（≤ 6 字，兩行）：**第一行優先寫大家認得的名字／主體**（人、品牌、國家、船；S42 只寫「為了一頭豬」沒點名，不如「英美差點開戰\n**為一頭豬？**」），**第二行用 `**…？**` 寫反常識衝突或反轉**。
  - `sub`（≤ 12 字）：補標題與 `headline` 沒說的硬事實（數字、年份、懸殊對比），是第二行白字大標，不是註腳。
  - **嚴禁在縮圖破梗答案**：`headline` 與 `sub` 只能拉高懸念與利害，**絕不直接寫出片中才要揭曉的因果答案或結局**。
- 縮圖畫面（`shot`）：選**誇張清楚的表情特寫**（驚恐、困惑、震驚的大臉）或**強烈視覺反差**（例如軍艦對一頭豬）；**禁止選闔上的空白書本、空房間、單一靜態死物**（W02 選闔上的紅皮書在手機列表毫無吸睛力；書頁不能畫字時改選角色看到結果的驚訝表情）。
- **字不擋主體**（站主 2026-11-08）：重做的集數在 `thumbnail.data` 寫 `"layout": "e"`（左邊深藍字區、右邊放圖，字不疊在圖上，長的外語標題在字區內自動縮字），
  `"focus": 0–100` 調圖在右框裡的左右位置，讓主體在框中間；做上架包時八語縮圖逐張看。**2026-11-10 起 curio- 的預設就是 layout e**（站主「應該用新版縮圖」：W02、S10-v2 因為沒寫 layout 畫成舊版）；不寫也會是新版，`focus` 照樣要調。要保留舊版的集數寫 `"layout": "d"`。

## 說明欄、八語系列後綴與置頂留言（2026-11-13）

- **前兩行鉤子不破梗**：`youtube.description` 第一行是鉤子問題或反差，第二行是「給…的人」（搜尋結果與展開前只看得到這兩行）；**不在前兩行直接講完謎底**。
- **內部查核與作畫備註不進說明欄**：史料算式核對、版本出入、誰能不能入畫（「皮加費塔過世超過四百年」「不畫創辦人的臉」）一律留在 `claims.md`／`verify-1.md`，**禁止寫進給觀眾看的 `youtube.description`**（S42、W02、B01 把內部查核備忘錄寫進說明欄，讀起來像工程紀錄）。AI 揭露若要寫，只留最後一行乾淨短句（Studio 照勾「變造或合成內容」）。
- **參考資料標題寫給觀眾看**：`sources[].title` 用清楚的書名、章名或機構頁面名稱；引用同一份公有領域長文時，只挑最核心的 1–2 段（`#L...` 行號錨點只用來區分確實不同的關鍵段落，不要把同一本書拆成五六條洗版）。說明欄最末由工具自動帶上 `#奇聞檔案局` 系列 hashtag（`core/metadata.mjs` `SERIES_HASHTAGS`）。
- **八語標題保留系列後綴**：`i18n/<locale>.json` 的外語標題一律帶定版系列譯名後綴（例如英文 `｜Curio Archive`、日文 `｜奇聞ファイル局`，完整八語對照表在 [`docs/videos/packaging-refresh-20261111/README.md`](../../../docs/videos/packaging-refresh-20261111/README.md) §譯名），最末的 `｜CC Subtitles` 等字幕標記由工具自動補上。
- **播放清單與二選一置頂留言**：交付上架包時，一併擬好一則**低門檻二選一置頂留言**（例如「換作是你會選 1 還是 2？留言打數字！」），提醒站主公開後置頂並把影片歸入「奇聞檔案局」播放清單。

## 配樂

每一集都有配樂，跟品牌故事一樣墊在整段旁白底下（片頭片尾的品牌音樂另外算）。`video.json` 寫上
`CURIO_MUSIC` 那一行（見上表），旁白之後跑 `node tools/video/cli.mjs music --slug <SLUG>`（一首約 US$0.15，
看 `status` 印出的報價），再 `assemble`。主機路線的撰稿提示詞也要求在設定開著配樂時一定寫 `music`。
2026-10-19 以前交付的集數都沒有配樂，**不補**（站主 2026-10-19「新的集數再開始就好」）：重製或重新合成舊集時也不要順手加。

## 插圖生圖與提示詞怎麼寫（2026-11-14 定案升級）

**兩層提示詞分工（必須同時滿足 lint 與畫質）**：
1. **`video.json` 裡的 `scene.data.prompt`（供 `lint` 與分鏡紀錄讀）**：保持精簡（約 100–200 字元），只寫「景別 → 地點與光線 → 一個主體做一個動作 → 關鍵道具」；**不寫 `no`、`not`、`without`、`text`、`blank`，也不寫 `cartoon`、`chibi`、`navy` 等畫風字**（`tools/video/core/curio.mjs` 會對禁用負面詞與抄 `look` 字詞報錯／警告）。連續三張同一種運鏡仍是 lint 錯誤。
2. **呼叫代理內建 `generate_image`（`AspectRatio: "16:9"`）的完整英文 Prompt（實際生圖用）**：每鏡必帶站主 2026-11-14 定案的**「劇場級動畫光影 × 厚塗水粉質感」**基底句，再接該鏡主體、光影、材質與零文字正向描述：
   ```text
   High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background.
   ```
   - **角色一致性（`ImagePaths` 必傳）**：單集內跨 ≥ 4 鏡出場的可入畫歷史人物或串場研究員，先用 `generate_image` 生一張固定角色設定圖（鎖定髮色、髮型、五官與主色服裝），之後每鏡出場必把設定圖路徑放進 `ImagePaths`；重繪修正既有鏡頭時，把前一版圖檔也放進 `ImagePaths` 鎖定構圖與道具位置。
   - **防畫紙白邊與防招牌亂碼（實戰必加）**：桌面物件／書本／食物特寫容易被水粉筆觸留出四周白紙邊，Prompt 尾端必加 `100% full-bleed edge-to-edge composition where rich background pigment reaches every single outer pixel on all four sides`；街道與建築外景必加 `plain unadorned timber and stone walls with clean blank surfaces and zero hanging shop signs`。
   - **會冒字的道具與螢幕**：書頁、文件、木牌一律寫成 `clean blank parchment surface` 或改拍闔上的書脊與人物表情；現代題材螢幕只畫一條藍色路線、一個白色轉彎箭頭或紅色定位釘；數字與比例畫成具體視覺對比（鼓或扁的錢包、滿載的小船），不上文字卡。
   - **純物件／空景鏡頭**：`video.json` 標 `"nobody": true`，生圖 Prompt 明確寫出純環境與物件結構，嚴禁出現路人、背景人影或殘肢。

（註：2026-11-05 以前針對 MiniMax `image-01`「夜晚會變 3D 公仔、不吃厚塗水粉」的舊限制隨停用 MiniMax 生圖解除；歷史火災、燭光書房、月夜航行可正常表現暖金火光／窗光與深藍夜色冷暖對比，但仍須維持 2D 手繪暖褐墨線與厚塗水粉筆觸，不可漂成寫實照片或 3D CGI。）

## 誰可以入畫（2026-11-05）

- **在世或 1956 年後過世的人不入畫**，連「代表他的路人」也不畫。講到他們時三選一：
  1. **串場角色**：例如虛構的檔案局研究員，用角色設定圖（`ImagePaths`）固定長相，**只畫不說話**；第一次入畫前旁白先介紹她（W03：「我們檔案局的研究員，把那一年的帳攤開來」）。
  2. **物件**：他做的東西、他寫的那份文件（`clean blank surfaces`，不畫字）、他坐過的位子。
  3. **明顯是一般人的匿名角色**：做觀眾也會做的事的店員、客人、路人，不是他本人的替身。
- 1956 年以前過世的人照舊可以入畫，Prompt 用年代、身分、服裝描述，不寫真名；跨 ≥ 4 鏡出場時必先產角色設定圖並在每鏡傳入 `ImagePaths`。

## 插圖怎麼驗收（2026-11-14 四格 2x 放大硬門檻）

所有關鍵影格轉成 `1920×1080` PNG 後、鎖定 `storyboard` 關卡之前，必須通過**程式邊緣檢測＋獨立子代理四格 2 倍放大審查**：

1. **100% 滿版無邊框**：先檢查四邊外框像素，零白邊、零黑邊、零相框線。
2. **零文字與零亂碼**：把每張圖切成左上、右上、左下、右下四張 2 倍放大圖（2x zoom quadrants），派**沒參與生圖的獨立子代理**逐張檢查，嚴禁任何中英文字母、數字、街道招牌字、印章字或黑板粉筆亂碼。
3. **解剖、人數與 `nobody` 精準**：手指數（5 指）、眼神對焦正常；`nobody: true` 鏡頭零路人與殘肢；跨鏡角色五官髮色服裝與設定圖一致。
4. **圖文相符、時代道具與地理考證**：畫面必須精準接住旁白當下講的主體與數量；**嚴禁時代穿幫**（例如 1816 年或 1666 年室內出現現代插電檯燈、電線開關）；若畫面出現地圖或地球儀，標記位置必須 100% 符合真實地理（例如印尼松巴哇島不可插在巴布亞紐幾內亞、菲律賓不可插在北太平洋公海；若無把握精準對位，改畫局部火山島或無標記古地球儀）。

任何一鏡被獨立審圖代理抓到上述瑕疵，立即把原圖與角色設定圖傳入 `ImagePaths` 重繪修正，直到全集 100% 通過後才逐鏡執行 `keyframes import --provider external --usd 0` 並送審分鏡。

## 不用卡片（2026-11-05）

站主 2026-11-05 定：**不用卡片、畫面不放任何文字**，因為影片要走全球市場（配音與字幕有好幾種語言，畫面上的中文字
在別的語言裡是雜訊）。

- 正文、片尾都是 `shot`：沒有 title、chapter、big、stats、compare、steps、table、quote、outro 卡。
- 數字講出來、畫成圖（上一節）；出處寫在說明欄。
- 章名只放在 `chapter` 欄位，工具把它寫進 YouTube 說明欄的章節，畫面上看不到。
- 縮圖保留文字，**每個語言各做一張**（`render` 會依字幕語言出各自的縮圖）。
- 主機撰稿提示已經不給撰稿模型任何卡片（`explainer-series.mjs` 的 `NO_CARDS`）。lint 不要求卡片，也不加分；
  它對 curio- 的檢查（`tools/video/core/curio.mjs`：正文至少 70% 是插圖、兩張插圖之間最多 3 張卡）是 2026-11-05
  以前的集數的上限，新集一張卡都沒有，自然是 100%。
- 2026-11-05 以前交付的集數不補拆卡片；重製時順手改成插圖。

## 費用結構（2026-11-14 更新）

- 關鍵影格：由代理內建 `generate_image` 生成並以 `keyframes import --provider external --usd 0` 匯入，站台帳本生圖費用為 **US\$0.00**（嚴禁改調用 MiniMax `image-01` 或站台付費生圖 API 充數）。
- 語音與配樂：中文旁白走站台 Gemini `Sulafat`（約 US\$0.35–0.50／集），一首配樂 `music` 約 US\$0.08，八語 MiniMax 配音合計約 US\$2–3／集。

## 每一集的順序與檢查

1. 大綱 → 稿子（十步架構、`loops`、同節拍 2–3 句併一景、沒有卡片）→ 獨立代理逐主張查核（`claims.md`＋`verify-1.md`）→ 盲評兩位獨立讀者 `narrative` 14/14 通過 → 逐景核對圖文相符與接梗。
2. `node tools/video/cli.mjs lint --slug <SLUG>`：**0 錯誤、0 警告**。
3. 中文旁白（Gemini `Sulafat`，實測語速 ≥ 4.4 字／秒）→ `check-audio` → 送 `audio` 關卡；`music`（不足片長時 `--loop`）。
4. 八語翻譯（`en,ja,ko,es,pt,id,vi,th`，獨立審校，泰文說明欄壓在 `< 4,500` UTF-8 bytes）→ `i18n-merge` → `dub --provider minimax`（0 fit overflow）→ 逐語 `check-audio` 並修正誤讀（若遇 `generate_image` 配額冷卻，優先把第 3–4 步全部跑完）。
5. 角色設定圖＋全集關鍵影格以內建 `generate_image`（`16:9`）生成 → 四格 2x 放大獨立子代理逐張審過 → `keyframes import --provider external --usd 0` → `render`（逐張檢查 9 語縮圖）→ `clips` → `assemble` → `captions` → `qa`（11/11）→ `package`（4/4）→ 雲端硬碟備份與獨立位元組核對。
6. Shorts：`docs/videos/SHORTS.md`。Shorts 一律 `from-episode`（頻道聲音）；手動 `build --redo` 一定帶 `--speech server`。

## 在雲端環境做旁白、配音與插圖匯入

容器裡沒有本機語音引擎，中文旁白走網站 Gemini TTS（`Sulafat`），八語配音走網站 MiniMax TTS（`--provider minimax`），關鍵影格則由代理內建 `generate_image` 產出後 `keyframes import --provider external --usd 0` 匯入。

**準備（每個新容器一次）**

1. 網路：容器的對外連線要允許 `mokaair.com`（環境設定的網域白名單，站主開）。Node 的 `fetch` 預設不走
   代理，每個 `cli.mjs` 指令前面都要加 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1`；不加會報「cannot reach
   mokaair.com」。
2. 權杖：`node tools/video/cli.mjs login --name <名字>`（例如 `claude-cloud-curio`）。它印出後台連結和代碼，
   等站主在後台按「允許」才結束，權杖存在 `~/.mokaair/video-tool.json`，不進 repo。容器回收就要重配一次。
3. 長指令一律用工具的背景執行，不要在 shell 裡用 `&` 丟背景：回合結束時 `&` 的程序會被殺。輸出導到檔案，不要接 `grep` 管線（會卡緩衝）。
4. 工作目錄在 `<VIDEO_WORKDIR>/<SLUG>/`（音檔、`narration.wav`、`keyframes/manifest.json`、`review/check.json`）；容器回收就沒了，完片必傳雲端硬碟備份，交接寫進票。
5. 片頭片尾：拿到權杖後跑 `branding --pull`，把正式站工人用的素材包裝進這個容器（`docs/videos/BRANDING.md`
   §從正式站取得目前的素材包）。容器裡本來沒有 `_branding`，不裝就合成，成片沒有片頭片尾。

**旁白與八語配音**

1. `tts --slug <SLUG> --dry-run` 看句數與費用 → `tts --slug <SLUG>`（確認實測語速 ≥ 4.4 字／秒，不足加 `voice.tempo`）→ `check-audio --slug <SLUG>`。
2. `check-audio` 標出唸錯的句子寫在 `review/check-flags.json`，`tts --slug <SLUG> --redo <check-flags.json>` 只重唸那幾句；speech journal 記著已付錢的句子，中斷後重跑不會重複收費。
3. 重唸還錯（中文多音字、年份、外文數字或縮寫如 `St. Paul's`、西文千分位 `13,200`、日文逗號數字 `68,596`、印尼文 `666`）就改那一句的字，合併後重錄該句並重跑 `check-audio` 確認。改了中文旁白就要重新跑盲評 `narrative` 與 `script --slug`。
4. 同一集的 `tts`、`dub` 與 `check-audio` 會共用 speech lock（「the project is held by …」，結束碼 3）：**同一集一次只跑一個語音指令**（外語 `check-audio` 一次跑一個 `--locale`，每個約 2.5 分鐘）。

**插圖生成、2x 放大審圖與匯入（2026-11-14 現行流程）**

1. 嚴禁呼叫 `node tools/video/cli.mjs keyframes` 讓站台調用 MiniMax 生圖。
2. 先用內建 `generate_image`（`AspectRatio: "16:9"`）畫出單集跨 ≥ 4 鏡出場的角色設定圖，再逐批生成全集關鍵影格（有角色出場必傳 `ImagePaths`）。若遇 `gemini-3.1-flash-image` 配額冷卻，先跑完八語翻譯、配音與 `check-audio`，等配額恢復再繼續生圖，**絕不退回 MiniMax**。
3. 將所有關鍵影格轉為 `1920×1080` PNG 並切出四格 2x 放大圖，交由獨立子代理逐張審過（零文字、零白邊、角色一致、五指與地理／時代道具無誤），不合格鏡頭帶原圖進 `ImagePaths` 重繪。
4. 全數審過後，逐鏡執行 `node tools/video/cli.mjs keyframes import --slug <SLUG> --shot <ID> --file <PNG> --provider external --usd 0` 寫入 `keyframes/manifest.json`，再鎖定並推送 `storyboard` 關卡。注意：之後只要改動 `video.json` 某景的 `prompt`，該景的外部匯入紀錄就會失效，務必先定稿 `video.json` 再匯入。

**配樂與成片**

1. `music --slug <SLUG>`（`--dry-run` 先看價，一首約 US$0.08）→ `render` → `clips`（全是靜圖加運鏡，不花錢，
   但 `assemble` 一定要它的 manifest）→ `assemble`（一集約 15 分鐘，4 核心一次跑一集）→ `captions` → `qa`
   → `review-push --gate final`。
2. `render` 用 Playwright 開瀏覽器。容器預裝的 Chromium 版本可能比 repo 的 Playwright 舊，報「Executable doesn't
   exist」時不要 `playwright install`：在暫存目錄建一個 `PLAYWRIGHT_BROWSERS_PATH`，把預裝的 headless shell
   接成 Playwright 要的版本號資料夾（`chrome-headless-shell-linux64/chrome-headless-shell` 指到預裝的
   `headless_shell`），再帶這個環境變數跑。
3. `qa` 讀 `video.json` 旁邊的 `verify-<n>.md`：查核寫在 `topic-checks/` 的集數，要放一份 `verify-1.md` 把那份表抄過來。
   卡片一個狀態超過 15 秒是 `pace` 失敗：把卡上第二句移到一張新插圖，不重唸；但旁白與分鏡的核准會失效，要站主再核准。
4. `links` 在容器裡常是 403：github.com 被網路政策擋，loc.gov 的圖片頁和 doi.org 擋程式請求。瀏覽器打得開就不是壞連結，
   回報給站主時寫清楚。
5. 改了 `video.json` 的任何一景（連卡片的 `sub`），插圖清單就要重建：重跑 `keyframes`（全吃快取，0 張新圖），
   分鏡核准也會失效。

## W03 重做的教訓（2026-11-06／07）

W03（Garmin）重畫十二輪分鏡、花了約 US$28 才過，量到的做法（Ada 設定圖全系列固定一張、放大檢查、`nobody`、
方向靠不住、年報畫成闔上的書、刪工作資料夾前先備份媒體、片頭在前、長度依內容）在
`.agents/skills/curio-episode/references/w03-lessons.md`，**每一集開畫前先讀**。

## 交接

備份（2026-11-10 起）：整個工作資料夾用 `docs/videos/ai-drama-drive/todrive.sh` 傳到雲端硬碟
`AI劇/奇聞檔案局/<代碼>/製作檔/`，規則在 `docs/videos/AI-DRAMA-DRIVE.md`；**不要再推 `transfer/*` 分支**
（`tobranch.sh` 會拒絕）。跟原來如此事務所統一的其他規則仍在 `docs/videos/explainer-series/README.md`。

做到一半要停，把狀態寫進看板的票：哪幾景的插圖過了、哪幾景卡在哪一題、花了多少、下一步。不要只寫
在對話或 PR 描述裡；下一個接手的模型（Claude 或 Codex）讀的是票和這份 skill。
