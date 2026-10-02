# 原來如此事務所（So That's Why）：系列規格

2026-09-28 起草。一集回答一個「為什麼」、畫面幾乎全是插圖的長期解說系列，長片與 Shorts 同步發佈，五語 CC 加四語配音。目標是 100 萬訂閱，這是挑戰目標，不是保證。

- 100 集題目、鉤子、答案、Shorts 角度、必備畫面、待查核事實：[`episodes.json`](episodes.json)
- 100 天發布表：[`schedule.csv`](schedule.csv)（日期是提案，首集公開當天才定 D1）
- 每日工作流：[`operations.md`](operations.md)

## 站主的決定（2026-09-28）

| 項目 | 決定 |
| --- | --- |
| 名稱 | 原來如此事務所。不用「十萬個為什麼」 |
| 參考 | 黑貓研究院〈HTC 曾掌握 Beats 過半股份，為什麼最後卻讓 Apple 花 30 億美元買走？〉（YouTube `vjAM8T_92Rs`）：一個問題、說故事的旁白、畫面一直換插圖。只參考形式；題目、稿子、畫面、角色全部原創 |
| 題材 | 四軸各 25 集：商業與品牌（B）、生活與科學（S）、旅遊與各國文化（T）、科技與 AI（A） |
| 畫面 | AI 插圖＋運鏡：漫劇路線的 `visual: "still"` 鏡頭 |
| 節奏 | 每天 1 支長片，搭配 Shorts |
| 吉祥物 | 不用。沒有固定角色，辨識度靠畫風、色盤與蓋章動作（[`look.md`](look.md)） |

## 各語系名稱

| 語系 | 系列名 | 片尾口號 |
| --- | --- | --- |
| zh-TW | 原來如此事務所 | 原來如此！ |
| en | So That's Why | So that's why! |
| ja | なるほど事務所 | なるほど！ |
| ko | 그래서그랬구나 사무소 | 그래서 그랬구나! |
| zh-CN | 原来如此事务所 | 原来如此！ |

標題格式：`為什麼……？｜原來如此事務所`；其他語系用 `localizations` 填翻譯後的標題與說明。

## 一集長什麼樣

| 段落 | 長度 | 內容 |
| --- | --- | --- |
| 鉤子 | 0:00–0:20 | 題目用反常識的說法丟出來（`hook`），先給一張最有衝擊的畫面，承諾「看完就知道為什麼」 |
| 片頭 | 3 秒 | 事務所的門打開、紅色印章在問題信上蓋「受理」。每集一樣 |
| 背景 | 1.5–2 分鐘 | 大家以為的答案、事情的起點 |
| 拆解 | 5–6 分鐘 | 3–4 個章節，每章一個原因；時間軸、地圖、數字對比用卡片場景 |
| 答案 | 1 分鐘 | 一句話的答案（`answer`），答案卡被蓋上「原來如此」 |
| 片尾 | 20 秒 | 下一集預告（照 `schedule.csv` 的順序）、訂閱 |

- 16:9、8–10 分鐘（至少 8 分鐘，站主 2026-10-01 定：除了漫劇，每集都要 8 分鐘以上；後台可設 8–12），章節 4–6 段。
- 每 4–6 秒換一張圖，一集約 90–120 張插圖；全部 `visual: "still"`（關鍵影格＋`zoompan` 運鏡，`tools/video/assemble/drama.mjs` 的 `motionMove`），不買影片片段。畫面等級上限見 [`../BINGE.md`](../BINGE.md)。
- 單一旁白：頻道聲音 Gemini `Sulafat`、台灣腔 style（[`../README.md`](../README.md)）。不做角色對白。
- 名詞發音用 [`../lexicon.json`](../lexicon.json)，新品牌名第一次出現就補。

## 畫面風格

- 扁平、明亮的編輯插畫（flat editorial illustration），粗描邊、有限色盤、乾淨背景；和漫劇的 3D 寫實分開，觀眾一眼認得出是這個系列。
- **沒有吉祥物**：不做跨集重複的角色，也就不需要設定圖。辨識度靠固定畫風、色盤（印章紅只給答案）、片頭與結尾的蓋章；完整規格、`look` JSON、片頭分鏡在 [`look.md`](look.md)。
- 真實人物、公司 logo、產品外觀：不用 AI 生成相似照片或 logo，改用剪影、泛稱物件與文字卡；需要引用真實圖片時走 `screenshot` 模板並標出處。
- 數字、年份、地圖、比例：用投影片卡片場景（`stats`、`compare`、`diagram`），字要大，手機看得清楚。

## Shorts

每集 2 支，9:16、35–55 秒（`tools/video/shorts/` 的 1080×1920 規格）：

1. **濃縮版**：鉤子＋答案，最後一格「完整故事在長片」。
2. **一個驚人事實**：`episodes.json` 的 `shorts[1]`，只講一件事。

- 重用長片的關鍵影格重新構圖成直式，不另外生圖。
- 發佈時間：長片隔天 12:00 發 Shorts 1、第三天 18:00 發 Shorts 2，所以每天都有兩支 Shorts 導回前兩天的長片（`schedule.csv`）。Shorts 說明欄第一行放長片連結，並設定「相關影片」。
- 腳本：解說版撰稿寫長片時順手寫 `docs/videos/<slug>/shorts.json`：兩支長片精華（Shorts 腳本第 2 版，`line: "cut"`、`series: "sothatswhy"`、`source.slug` 是長片，[`../SHORTS.md`](../SHORTS.md)）；場景用 `shot` 指長片的鏡頭，圖直接沿用那張關鍵影格並綁雜湊。寫壞了只記在工人 notes，不擋長片，可以之後手寫。
- 做法：長片的關鍵影格畫好（最好是成片核准）後，在有 ffmpeg 與 Chromium 的機器跑：

  ```bash
  node tools/video/shorts/cli.mjs from-episode --slug <slug> --check                    # 只檢查腳本與關鍵影格雜湊
  node tools/video/shorts/cli.mjs from-episode --slug <slug> --workdir <repo 外的目錄>    # 兩支都做；--short 1 只做一支
  ```

  `from-episode` 把每支的 `shot` 換成關鍵影格、寫成腳本檔，再交給一般的 `build`（旁白預設 `--speech server`：頻道聲音經網站合成，按字數計費；也可以 `--speech windows` 或 `--audio-dir`）。之後每個 build 目錄照 Shorts 的一般順序走 `check-audio` → `qa` → `package` → `push`：`package` 從網站讀長片的網址，把 Short 導回長片。卡片用 `cut:sothatswhy` 主題（`tools/video/shorts/layouts.mjs`）：系列色盤、左上「原來如此事務所」、每張卡片底下「完整版在長片 ▶」。

## 多語

| 項目 | 長片 | Shorts |
| --- | --- | --- |
| CC | zh-TW、en、ja、ko、zh-CN（現有 `i18n-sheet` → `i18n-merge` → `captions`） | 先只有繁中 CC；長片數據穩定後再加四語 |
| 配音 | en、ja、ko、zh-CN 四條，同一個 Sulafat 聲音（[`../DUBS.md`](../DUBS.md) 的 `dub` 指令，塞回時間軸規則照原文） | 不做 |
| 標題與說明 | 五語 `localizations` | 五語 `localizations` |

- 配音要頻道先有 YouTube「進階功能」權限；音軌由站主在 Studio 逐語上傳（Data API 沒有音軌上傳）。每支長片先出繁中，站主在 `/admin/videos` 勾要配的語言。
- 翻譯工作表的字元預算照 DUBS.md，旁白寫短句，配音塞不下的機率才低。
- 這個系列的標題問題大多是跨文化的；翻譯審稿時檢查「對該語系觀眾是否仍然反常識」，不成立的題目在該語系的標題改問法，不硬翻。

## 查核規則

- 標題、稿子、卡片上的每個數字、年份、金額、名稱，都在製作當天找一手或官方來源確認，寫進該集的 `## 來源`，附確認日期（`youtube-video` skill 的不變規矩第 2 條）。
- `episodes.json` 的 `facts_to_verify` 是已知最容易錯的點；查不到就改題目、拿掉數字，不講「據說」。
- 科學題（S 軸）若科學界沒有定論（例：S05 打哈欠、S10 做夢），影片要說「目前主流假說」，不能講成已證實。
- 商業題只講公開的事實與報導，意見要標成意見；不評論在世個人的私德。

## 成本與產能（估計，試片三集後改成實測）

| 項目 | 每集 | 100 集 |
| --- | --- | --- |
| 關鍵影格（Gemini 3 Pro Image 約 US$0.134／張 × 約 110 張，含重做） | 約 US$15 | 約 US$1,500 |
| 旁白＋四語配音（Gemini TTS） | 不到 US$1 | 不到 US$100 |
| 撰稿、查核、翻譯（模型 token） | 未知，試片量 | 未知 |

單價來源是 [`../DRAMA.md`](../DRAMA.md) 的供應商表，實作時照 `apps/api/app/video_media/catalog.py` 再核對。

**每天一集的瓶頸是站主**：每天要審 1 支長片＋2 支 Shorts、上傳四條配音、決定上架時間。要撐住每日節奏，D1 開播前至少要有 **14 集做完**的庫存（兩週緩衝），並讓 [`../HANDS-OFF.md`](../HANDS-OFF.md) 的自動關卡（旁白、分鏡、成片品管）都上線。庫存低於 7 集就降成隔日更，不降品質。

## 100 萬訂閱的路線圖

| 階段 | 目標 | 主要看的數字 | 決策 |
| --- | --- | --- | --- |
| 第 1–20 集 | 找出有效的主軸與標題寫法 | 各主軸的 CTR、平均觀看百分比、前 30 秒留存 | 第 20 集後檢討：表現最差的主軸比例砍半，換成最好的主軸 |
| 第 21–60 集 | 1 萬訂閱 | Shorts → 長片的導流（Shorts 觀看頁的相關影片點擊）、每千次觀看新增訂閱 | 找出能連看的題組，做成播放清單（例：商業「失敗的巨頭」、旅遊「日本為什麼」） |
| 第 61–100 集 | 10 萬訂閱 | 各語系觀看占比、配音音軌的觀看時間 | 占比高的語系優先做 Shorts 配音與在地化題目 |
| 第 2 季起 | 100 萬訂閱 | 回訪觀眾比例、播放清單連看數 | 依數據擴充題庫，開觀眾提問單元（留言點題） |

每 20 集寫一次檢討到這份文件（數字從 Studio 匯出，檔案留在 repo 外；缺的數字寫「未取得」，不填 0）。

## 製作怎麼接現有產線

1. 在 `/admin/videos` 發起一支漫劇：故事前提填 `episodes.json` 那一列的題目（可附 `hook`、`answer` 當備註），風格選**扁平插畫解說**（`flat-explainer`，migration 0113）。這會建一部單集作品（one-off，`docs/videos/DRAMA-FLOW.md`）：工人先寫一份解說版的「故事聖經」（問題、一句答案、原因、大綱、來源網址，沒有角色）給你核准，核准後用解說版的撰稿、查核提示詞，產出 `format: "drama"`、`look.preset: "flat-explainer"`、`characters: []`、全部 `visual: "still"` 的 `video.json`；沒有角色就沒有設定圖關卡，直接畫關鍵影格。規格見 `youtube-video` skill 的 `references/drama.md`，範例 `tools/video/core/fixtures/explainer/`。
2. 之後照漫劇路線：選大綱 → 劇本 → 查核 → 旁白 → 關鍵影格 → 合成 → 五語字幕 → 配音 → 上架包。
3. Shorts：`shorts/cli.mjs from-episode`（見上面 Shorts 一節），用同一集的關鍵影格與 `shorts.json`。

要先補的產線工作是 `tasks/open/` 裡 `sothatswhy-*` 的四張票：解說版型預設、從長片切 Shorts、畫面識別與片頭、前三集試片。
