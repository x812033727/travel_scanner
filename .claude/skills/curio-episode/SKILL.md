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
   開場一個場景加三到四個鉤子、片尾不點名下一支）。

## 系列定案（改任何一條都要先問站主）

| 項目 | 定案 | 來源 |
| --- | --- | --- |
| 畫面 | MiniMax `image-01` 畫的可愛卡通插圖；**不由 Claude 或 Codex 手繪 SVG** | 站主 2026-10-10「用 minimax 產生圖不要用 claude 或 codex 產生」 |
| 畫風 | `look: { "preset": "cute-mystery" }`，一個字都不加：不寫 `style`、`negative` 留空 | 站主 2026-10-10 選第 3 版；`tools/video/core/drama.mjs` PRESETS |
| 照片 | 可放，限公有領域（CC BY 不用）；做成貼圖式照片卡，算卡片 | 站主 2026-10-10、L08 |
| 人物 | 過世 70 年以上可畫成卡通（用描述不用名字）；在世或未滿 70 年不畫本人 | README §內容守則 |
| 長度 | 目標 10 分鐘，旁白正文至少 8 分鐘 | `docs/videos/long-form/README.md` |
| 片頭片尾 | 頻道片頭放在開場濃縮之後（`intro_at` = after_first_chapter）；片尾 v4-endscreen，旁白不提下一支 | `docs/videos/BRANDING.md` |
| 語言 | zh-TW 先做完，en／ja／ko 的標題說明、CC、配音由站主勾選 | `docs/videos/DUBS.md` |
| 鉤子 | 跟品牌故事一樣密：正文每 30–45 秒一個懸念，沒有超過 45 秒的空檔；`loops` 十分鐘至少 8 個；每章停在一個沒解的問題上 | 站主 2026-10-19「品牌故事比較順也有比較多鉤子」；lint 的 `TIGHT_CADENCE`（`tools/video/core/narrative.mjs`） |
| 配樂 | 每一集都有：`"music": {"prompt": "light, curious, a little mysterious, no vocals", "gain_db": -20, "duck_db": -10}`，跟品牌故事同樣的音量；沒有配樂 lint 會警告 | 站主 2026-10-19「而且有音樂」；`tools/video/core/curio.mjs` 的 `CURIO_MUSIC` |

## 選路線

| 情況 | 路線 | 怎麼做 |
| --- | --- | --- |
| **新的一集** | 主機可愛解說路線（預設） | 後台「影片審核 → 漫劇 → 新的漫劇」，風格選奇聞檔案局（`cute-mystery`），圖片模型自動是 `image-01`，長度 10 分鐘。工人照 `tools/video/automation/explainer-series.mjs` 的 MYSTERY 系列檔案寫聖經與稿子；`settle()` 會丟掉撰稿模型加的 `style`／`negative`；每張圖九題是非題評審；畫面多樣性 lint 也管。設計在 `docs/videos/explainer-route/DESIGN.md` |
| **重製已交付的一集**（改稿、改開場、換片頭片尾） | 本機 recut | `docs/videos/curio-five-recuts-20261012/README.md`；已付錢的插圖照舊用（提示詞逐字不動就吃快取），新景才畫新圖 |
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

## 配樂

每一集都有配樂，跟品牌故事一樣墊在整段旁白底下（片頭片尾的品牌音樂另外算）。`video.json` 寫上
`CURIO_MUSIC` 那一行（見上表），旁白之後跑 `node tools/video/cli.mjs music --slug <SLUG>`（一首約 US$0.15，
看 `status` 印出的報價），再 `assemble`。主機路線的撰稿提示詞也要求在設定開著配樂時一定寫 `music`。
2026-10-19 以前交付的集數都沒有配樂；要不要補（一首配樂＋重新合成，旁白與插圖不動）由站主決定。

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

## 交接

做到一半要停，把狀態寫進看板的票：哪幾景的插圖過了、哪幾景卡在哪一題、花了多少、下一步。不要只寫
在對話或 PR 描述裡；下一個接手的模型（Claude 或 Codex）讀的是票和這份 skill。
