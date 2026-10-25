---
name: curio-episode
description: 奇聞檔案局（slug 以 curio- 開頭的歷史與奇異解說長片）的做法：系列定案不能改的事、該走哪條路線（新集走主機可愛解說 cute-mystery；重製走本機 recut）、MiniMax image-01 可愛插圖怎麼寫提示詞、插圖怎麼驗收（內容相關的可愛插畫，不是證據重建）、整集一次報價、卡片的上限、跟品牌故事一樣每 45 秒一個鉤子與配樂、片頭片尾、配音與 Shorts。lint 對 curio- 的 slug 檢查系列畫風、插圖占比至少七成、連續卡片最多三張。要做、重做、續做或修任何一集奇聞檔案局（含 H01–H07、U、L 各題與它們的 v2），或改它的畫面、提示詞、卡片時，先讀這個 skill，再讀 youtube-video。Make or remake a 奇聞檔案局 (curio-*) episode in the series look.
metadata:
  short-description: 奇聞檔案局：系列畫風、路線、插圖驗收、檢查
---

# 奇聞檔案局（curio-episode）

奇聞檔案局是一個**可愛卡通插圖**配一個說書旁白的歷史與奇異系列：每一集講一個真實的怪事，像講故事
一樣講到底。畫面主體是 MiniMax `image-01` 畫的插圖，卡片只放數字、名字、出處。這份 skill 是系列的
固定做法；通用的步驟（旁白、合成、上架包、配音、Shorts）仍在 `youtube-video`。

2026-10-14 為什麼有這份 skill：H04–H06 重製時，負責的模型沒讀到系列的畫面規則（只寫在
`docs/videos/history-curiosity/look.md`），把插圖當證據重建、一張一張向站主要授權，試圖連續被自己退回，
最後整集變成 88 張文字卡、0 張插圖，跟 H01–H03 完全不像一個頻道。下面每一條都是為了不再發生。

## 先讀

1. 參考片 `docs/videos/curio-h01-v2/video.json`：動筆前讀前 30 景。116 張插圖、7 張卡片、連續卡片最多 1 張；
   每張提示詞的寫法照它。
2. `docs/videos/history-curiosity/README.md`（系列企劃與站主的決定）、`docs/videos/history-curiosity/look.md`
   （畫風怎麼來的、MiniMax 的限制、量過哪些寫法會漂）。
3. 稿子：`.agents/skills/youtube-video/references/script-writing.md` §故事主線與鉤子（一條故事線、`loops` 表、
   片尾不點名下一支）與 §奇聞檔案局與品牌故事的開場（2026-10-25：利害 → 場景 → 最多兩個預告 → 承諾句 → 問題）。

## 系列定案（改任何一條都要先問站主）

| 項目 | 定案 | 來源 |
| --- | --- | --- |
| 畫面 | MiniMax `image-01` 畫的可愛卡通插圖；**不由 Claude 或 Codex 手繪 SVG** | 站主 2026-10-10「用 minimax 產生圖不要用 claude 或 codex 產生」 |
| 畫風 | `look: { "preset": "cute-mystery" }`，一個字都不加：不寫 `style`、`negative` 留空 | 站主 2026-10-10 選第 3 版；`tools/video/core/drama.mjs` PRESETS |
| 照片 | 可放，限公有領域（CC BY 不用）；做成貼圖式照片卡，算卡片 | 站主 2026-10-10、L08 |
| 人物 | 過世 70 年以上可畫成卡通（用描述不用名字）；在世或未滿 70 年不畫本人 | README §內容守則 |
| 長度 | 目標 10 分鐘，旁白正文至少 8 分鐘。**2026-10-25 站主定 13 分鐘**（參考頻道中位 13–31 分）：後台建立單集時選 13 分鐘，正文約 3,500 字、4.5 字／秒（§跟高點閱頻道的差距） | `docs/videos/long-form/README.md`；`docs/videos/channel-review-20261025-story-series/README.md` |
| 片頭片尾 | 頻道片頭放在開場濃縮之後（`intro_at` = after_first_chapter）；片尾 v4-endscreen，旁白不提下一支 | `docs/videos/BRANDING.md` |
| 語言 | zh-TW 先做完，en／ja／ko 的標題說明、CC、配音由站主勾選 | `docs/videos/DUBS.md` |
| 鉤子 | 跟品牌故事一樣密：正文每 30–45 秒一個懸念，沒有超過 45 秒的空檔；`loops` 十分鐘至少 8 個；每章停在一個沒解的問題上 | 站主 2026-10-19「品牌故事比較順也有比較多鉤子」；lint 的 `TIGHT_CADENCE`（`tools/video/core/narrative.mjs`） |
| 開場與口吻 | 開場五步（利害 → 場景 → 最多兩個預告 → 一句承諾句 → 問題）；說給一個人聽：每章至少一句「你」、一句旁白自己的反應，lint 低於每千字 2 個「你」警告；標題公式見 §標題與縮圖 | 2026-10-25 對照黑猫研究院、馬臉姐、cheap 量到的差距（§跟高點閱頻道的差距）；`register.mjs` `STORY_OPENING_RULE`、`TOLD_TO_ONE_VIEWER` |
| 配樂 | 每一集都有：`"music": {"prompt": "light, curious, a little mysterious, no vocals", "gain_db": -20, "duck_db": -10}`，跟品牌故事同樣的音量；沒有配樂 lint 會警告 | 站主 2026-10-19「而且有音樂」；`tools/video/core/curio.mjs` 的 `CURIO_MUSIC` |

## 選路線

| 情況 | 路線 | 怎麼做 |
| --- | --- | --- |
| **新的一集** | 主機可愛解說路線（預設） | 後台「影片審核 → 漫劇 → 新的漫劇」，風格選奇聞檔案局（`cute-mystery`），圖片模型自動是 `image-01`，長度 10 分鐘。工人照 `tools/video/automation/explainer-series.mjs` 的 MYSTERY 系列檔案寫聖經與稿子；`settle()` 會丟掉撰稿模型加的 `style`／`negative`；每張圖九題是非題評審；畫面多樣性 lint 也管。設計在 `docs/videos/explainer-route/DESIGN.md` |
| **主機做的一集要用新規則重做**（站主在後台建立的 cute-mystery 單集，已可以上架或做到一半；2026-10-25 的開場五步、說給一個人聽等新規則） | 後台單集頁「重做」 | 伺服器放棄舊影片（工作區與已付費素材留著）、那一集回 `ready`、slug 加 `-redo1`，工人照核准的故事聖經、用現在的撰稿規則重寫劇本做一支新的（`docs/videos/BINGE.md` §重做一集）。要 13 分鐘先把單集的 `target_minutes` 改成 13。**本機做、`review-push` 推上站的集（S01–S40 這類有 `docs/videos/curio-*` 稿子的）沒有作品列，沒有這顆鈕**：用新規則整支重做走下一列（第一批是 PR #1844 的 `curio-h24` 與 `curio-s30-v2`） |
| **重製本機做的一集**（改稿、改開場、換片頭片尾；或照 2026-10-25 新規則整支重寫 `video.json` 再重跑旁白與插圖） | 本機 recut | `docs/videos/curio-five-recuts-20261012/README.md`；已付錢的插圖照舊用（提示詞逐字不動就吃快取），新景才畫新圖 |
| **主機不能用、要在本機從零做** | 本機漫劇格式 | `format: "drama"`、`look: { "preset": "cute-mystery" }`、`characters: []`；`node tools/video/cli.mjs keyframes --slug <SLUG> --takes 3` 一次畫整集（不是一次三張） |

不要用 `format: "slides"` 從零做新集：那是 H01–L08 第一版的試片路線，系列預設與評審都要手動接，
H04–H06 就是在這裡偏掉的。

## 稿子：跟品牌故事一樣順、一樣多鉤子

2026-10-19 站主比較兩個系列後說品牌故事「內容比較順也有比較多鉤子，而且有音樂」，要奇聞檔案局做到一樣好或更好。
量到的差距：H10、H11、H12、M09、U09、H01 v2 的最長空檔 69–81 秒，每集有 2–7 段超過 45 秒沒有任何懸念；
品牌故事的撰稿規則是 45 秒。所以：

- **每 30–45 秒（約 130–200 字）一個懸念**：一個問題、一個升級（「但這還不是最怪的」）、一份對不上的紀錄、
  先不講為什麼、或一個轉折。鉤子要站在這個檔案的事實上（日期、數字、某個人的決定、不該出現的東西），
  不寫空話（「接下來更精采」），不念目錄。
- **每章結尾停在一個具體、還沒解的問題或動作上，下一章第一句就接它**。結構裡的「流傳的版本、紀錄、
  最站得住的解釋」是**同一個故事照發生順序的段落**，不是旁白一段一段走過的區塊；章名照事件取。
- **`loops` 十分鐘至少 8 個**，開場濃縮種下至少 3 個，每一個都要回收。
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
| 長度 | 中位 13 分（11–21 分） | 馬臉姐 23–40 分、cheap 9–24 分 | 目標 10 分、正文 8 分（2,100–2,600 字） | **2026-10-25 站主定 13 分**：正文約 3,500 字（品牌故事 `series.json` 已改；奇聞檔案局後台建立時選 13） |
| 字幕 | 每格燒錄字幕、關鍵字黃色 | 同 | 不燒（站主 2026-10-08 定） | **2026-10-25 站主改試燒**：品牌故事（`story.mjs`）與主機 cute-mystery 單集（`flow.mjs settle()`）的 `subtitles.burn_in` 預設 true；其他語言仍 CC |
| 頻道 | 單一類型、每天一支、120 支在四個月內 | 單一類型 | 一個頻道混六個系列（AI 新聞、AI 名詞、教學、漫劇、奇聞、品牌） | 不是 skill 能改的；報告 §決定 |

把上面的變成稿子規則（撰稿提示、lint、盲評都已照這一節改）：

- **開場五步**：(1) 先講利害，對觀眾說，帶最大的數字（「一家公司差點把稱霸幾百年的瑞士錶業逼到關門」）；(2) 場景，照
  順序講到第一個說不通的事實就停；(3) 預告最多兩個後面的時刻（原本的「三到四個」在這兩個系列不用：觀眾還沒有脈絡，
  四個線索連著丟聽起來像清單）；(4) 一句承諾句，點名題目和規模（「這份檔案從頭翻一遍，九個空桶會回來」），不是目錄；
  (5) 最後一句是全片要回答的問題。
- **說給一個人聽**：每章至少一句轉向觀眾的「你」（他用的、有的、聽過的、會怎麼做）；每章一句旁白自己的反應（「這就很怪了」）；
  意見標成意見；一集一兩次拿共同經驗開玩笑。事實一個字都不改。
- **語速**：正文目標 4.5 字／秒（參考頻道約 5，我們 3.3）；句子用連接詞接著講，事實後面接它對某個人的意義。10 分鐘的集數
  正文約 2,700 字起算，不是 2,100。聲音指示 `STORY_VOICE_STYLE` 2026-10-25 已加「語速像平常聊天，一秒四到五個字，句與句之間不拖」（站主定）；
  主機用的是後台設定分頁貼的那一份，**站主要把這句貼上去**；它在 `speechHash` 裡，舊片不重錄。
- **結尾**也是對話：答案、「如果你…，留言告訴我」、訂閱的理由；可以說「好啦，這就是今天的故事」，仍然不講下一支。

## 標題與縮圖（2026-10-25）

- 標題：**大家認得的名字放前 6 字**（船、地方、人、事件、品牌）＋**一個利害或反常的詞**（消失、不敢、騙過、差點、全部、真相、
  憑什麼）＋一個數字或年份＋問號；後綴照舊「｜奇聞檔案局」或「｜品牌故事」；後綴前最多 30 字。
  例：「十個人全部消失，1872 年這艘船為什麼還在走？」「曹操自己放的火？赤壁真正燒船的人是誰」「賣輪胎的公司，憑什麼決定全世界最好吃的餐廳？」。
  不要平靜的閱讀題（「燈塔的故事改了哪裡？」「研究揭露了什麼？」）。
- 縮圖（版型重做前能做的）：`headline` 用最有利害的 6 字（「全部消失」「他自己燒的？」），`sub` 寫數字或年份，`shot` 選一張
  **有表情的臉**或**那件東西本身**（船、信、鞋），不選空景。版型 2026-10-25 已做（layout d，票 `2026-10-24-story-series-thumbnails-take-the-bold`）：`sub` 要寫，它是第二行白字大標（≤12 字），不是註腳。

## 配樂

每一集都有配樂，跟品牌故事一樣墊在整段旁白底下（片頭片尾的品牌音樂另外算）。`video.json` 寫上
`CURIO_MUSIC` 那一行（見上表），旁白之後跑 `node tools/video/cli.mjs music --slug <SLUG>`（一首約 US$0.15，
看 `status` 印出的報價），再 `assemble`。主機路線的撰稿提示詞也要求在設定開著配樂時一定寫 `music`。
2026-10-19 以前交付的集數都沒有配樂，**不補**（站主 2026-10-19「新的集數再開始就好」）：重製或重新合成舊集時也不要順手加。

## 插圖提示詞怎麼寫

畫風只在 `look` 裡；提示詞只寫**這一張畫什麼**。順序：景別 → 地點與時間 → **一個人做一件事** →
視線落點的物件 → 光從哪來。照 `docs/videos/curio-h01-v2/video.json` 的寫法，例如
「Medium shot of a ship's master on a wooden quarterdeck in grey daylight, a clean-shaven officer in a
peaked cap raising a brass telescope to one eye, rigging behind him, light from an overcast sky on the left」。

| 這樣寫 | 不要這樣寫（H04–H06 試圖被退的原因） |
| --- | --- |
| 一個人在做一件事，臉朝鏡頭，表情是主角（驚訝、害怕、困惑） | 從背後看的無名人物、兩三個人同框互動（MiniMax 聽不懂多人互動） |
| 沒有人的場景只在必要時用，寫成正向的「the only shapes are the tent, snow and trees」 | 大量空景（空帳篷、空運河、空櫃台）：模型會把臉畫到物件上，或自己補人 |
| 物件寫成卡通裡會有的樣子：a plain canvas tent、a blank manila folder | 在提示詞或 `look` 裡寫年代材質、地形學細節、「寫實」要求：會漂成照片或油畫 |
| 字一律不畫，寫 blank sign、blank page；字由卡片蓋上 | 要模型畫出可讀的文件、車票、招牌 |
| 白天、室內、夜景輪替（夜景最多一半）；景別遠、中、特寫輪替 | 懸疑題材全部寫成夜晚 |
| 光寫成柔和、陰天、檯燈這類不帶顏色的字：mild、overcast、soft grey sky、lamp | 寫 sunny、bright midday sun、green、leafy、summer：評審照系列色盤（夜空藍、牛皮紙黃、褪色青）判畫風，這些字畫出飽和的綠和藍，H04–H06 有五張因此不過 |
| 沒有人的畫面改成一個人在那個地方做事 | 只寫風景加「the only shapes are …」：H04–H06 重畫時仍有三張在樹梢、雪堆後面冒出小人頭 |

連續三張同一種運鏡是 lint 錯誤；提示詞裡出現 cartoon、chibi、navy 這類畫風字是警告（抄 `look`）。

## 插圖怎麼驗收

插圖是**內容相關的可愛插畫**，不是證據重建：觀眾知道這是卡通。驗收看三件事：

1. **評審過了就收**：九題是非題（文字、解剖、主體、畫框、畫風、細節……）全過的圖可以用。不要再加一層
   「每個細節都要有出處」的人工審核；H04–H06 judge 通過的 9 張被人工退到只剩 0–1 張，是標準錯了。
2. **只退會誤導的圖**：跟旁白或來源**矛盾**的事實才重畫（人數講九個畫成三個、旁白說白天畫成夜晚、
   旁白說他拿著劍畫成拿槍）。多一隻貓、一塊看不出是字的塗鴉、卡通化的道具，不是重畫的理由。
3. **畫風漂了就重畫**：照片質感、3D、油畫、黑邊——這些評審會抓；抓到就照上表改提示詞，不改 `look`。

一張圖重畫三次加兩輪改提示詞還不過，主機會停在 `prompt_fixes:keyframes` 等站主按重試；本機就把那一景
換成同一章已經過的另一張圖（提示詞逐字複製，吃快取不花錢），或換成一張卡片——前提是不破下面的上限。

## 卡片的上限（lint 錯誤，`tools/video/core/curio.mjs`）

- 正文（不算 title、chapter、outro）至少 **70%** 是插圖（`shot`）；已交付的集數是 73–95%。
- 兩張插圖之間最多 **3** 張卡片。
- 卡片只放插圖說不清的東西：一個數字、一個名字、一句引文、一個出處；出處卡（SVG 圖解、照片卡）也是卡片。
- 文字卡、SVG 圖解**不是**插圖失敗時的退路；退路是上一節的換圖或改提示詞。

## 預算：整集一次報、一次授權

一集約 75–120 張插圖，每張含評審約 US$0.0135，加上重畫，整集大約 **US$1.5–3**，再加一首配樂（約 US$0.15）（H01：136 次生成
US$2.04；L08：92 張 US$2.83）。開畫之前，把整集的張數與上限金額一次報給站主，核准後一次畫完；
**不要**一張、三張地分批要授權。試畫樣張只在換畫風時才需要，系列畫風已經定了。

## 每一集的順序與檢查

1. 大綱（站主選）→ 稿子（`loops`、開場一個場景加鉤子）→ 查核 → 盲評 `narrative` 每一題都過。
2. `node tools/video/cli.mjs lint --slug <SLUG>`：**0 錯誤**，包含這份 skill 的系列檢查。lint 紅了先修稿
   或分鏡，不要繞過。
3. 旁白（頻道聲音）→ `check-audio` → 站主聽。
4. 插圖整集一次畫 → 分鏡卡給站主看一次 → 配樂（`music`）→ 成片 → 品管 → 上架包。
5. 配音、Shorts：`docs/videos/DUBS.md`、`docs/videos/SHORTS.md`。Shorts 一律 `from-episode`（頻道聲音）；
   手動 `build --redo` 一定帶 `--speech server`，不帶會換成 Windows 的聲音。

## 在雲端環境做旁白與插圖（Claude Code 雲端、Codex 雲端）

2026-10-19 S01、S09、S18 三集的旁白和插圖全部在雲端容器裡做完，沒碰本機。容器裡沒有 Windows 的聲音，
所以旁白一律走網站的頻道聲音（伺服器 Gemini TTS），插圖走網站的 MiniMax；兩者都要網站權杖，錢記在網站上。

**準備（每個新容器一次）**

1. 網路：容器的對外連線要允許 `mokaair.com`（環境設定的網域白名單，站主開）。Node 的 `fetch` 預設不走
   代理，每個 `cli.mjs` 指令前面都要加 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1`；不加會報「cannot reach
   mokaair.com」。
2. 權杖：`node tools/video/cli.mjs login --name <名字>`（例如 `claude-cloud-curio`）。它印出後台連結和代碼，
   等站主在後台按「允許」才結束，權杖存在 `~/.mokaair/video-tool.json`，不進 repo。容器回收就要重配一次。
3. 長指令一律用工具的背景執行（Claude Code 的 `run_in_background`），不要在 shell 裡用 `&` 丟背景：
   回合結束時 `&` 的程序會被殺，`login` 等不到允許、代碼過期。輸出導到檔案，不要接 `grep` 管線（會卡緩衝）。
   背景執行最長 2 小時，到時間會被殺；整集插圖一集一個指令分開跑，不要三集串在一個指令裡。
4. 工作目錄在 `<VIDEO_WORKDIR>/<SLUG>/`（預設在容器家目錄下；音檔、`narration.wav`、`keyframes/manifest.json`、
   `review/check.json`）；容器回收就沒了，交接寫進票，不要只寫路徑。

**旁白**

1. `tts --slug <SLUG> --dry-run` 看句數與費用 → `tts --slug <SLUG>` → `check-audio --slug <SLUG>`。
2. `check-audio` 標出唸錯的句子寫在 `review/check-flags.json`，`tts --slug <SLUG> --redo <check-flags.json>`
   只重唸那幾句；speech journal 記著已付錢的句子，中斷後重跑不會重複收費。
3. 重唸還錯（中文多音字、年份、日文人名）就改那一句的字：`lexicon.json` 只收拉丁字母開頭的詞，中文讀音
   不能放進去。改的那句若是卡片上的原文（刀銘、題字），旁白跟卡片就不一樣了：卡片的 `sub` 補一句「意思是……」，
   讓觀眾知道旁白唸的是白話。改了旁白就要重新跑一次盲評 `narrative`（新讀者），再 `script --slug` 重產 `script.md`。
4. `review-push --slug <SLUG> --gate audio` 送審，站主在 `/admin/videos` 決定後 `review-pull --slug <SLUG>` 記下。
   站主在對話裡要先聽，就用 `ffmpeg -i narration.wav -codec:a libmp3lame -b:a 96k <SLUG>-narration.mp3`
   轉成 mp3 傳給站主；後台用不了、站主在對話裡說可以時，才 `approve --slug <SLUG> --gate audio --note "<站主原話>"`。
5. Gemini 回 429（`video_speech_upstream_busy`）可能是一時忙碌，也可能是網站那把金鑰的當日額度用完；工具會照
   `Retry-After` 自己重送。重送一小時以上還是 429，多半是當日額度：Gemini 的每日額度在太平洋時間午夜重置
   （夏令 07:00 UTC、冬令 08:00 UTC），S01 就是等到 07:05 UTC 才唸完。不要一直手動重跑。

**插圖**

1. `keyframes --slug <SLUG> --dry-run` 拿到張數與上限金額，三集一起報、一次授權（見上一節）。
2. 授權後一集一個背景指令：`keyframes --slug <SLUG> --takes 3`，約 30–60 分鐘。
3. 評審三次都不過的景，照〈插圖提示詞怎麼寫〉改成「一個人做一件事」再跑同一個指令：過了的圖吃快取，
   只畫改過的景。S01 八景、S09 六景、S18 十一景都是這樣一輪就過。
4. 網站回 HTTP 502 或背景到時被殺：直接重跑同一個指令，已經過的不會再收費；`ledgerTotals(workdir)`
   （`tools/video/media/ledger.mjs`）看這集花了多少。S01、S09、S18 每集 US$1.7–1.9，三集合計 US$5.32。
5. 畫完 `review-push --slug <SLUG> --gate storyboard` 把分鏡卡推給站主看。
6. 同一集的 `tts`、`check-audio` 與 `keyframes` 會互相鎖住（「the project is held by keyframes」，結束碼 3，什麼都沒送）：
   同一集一次只跑一個；不同集可以同時跑。排隊等前一個指令時，等待時間也算在背景的 2 小時裡，等太久會被殺，
   重跑即可（過的圖吃快取）。
7. 評審回「AI 拒絕回應（PROHIBITED_CONTENT）」時整個指令停下：是下一景的提示詞或畫面踩到安全規則
   （S34 是「偷渡的少年坐在淺水裡」）。改成成年人、穿著衣服、在乾地上，再重跑。

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

## 交接

做到一半要停，把狀態寫進看板的票：哪幾景的插圖過了、哪幾景卡在哪一題、花了多少、下一步。不要只寫
在對話或 PR 描述裡；下一個接手的模型（Claude 或 Codex）讀的是票和這份 skill。
