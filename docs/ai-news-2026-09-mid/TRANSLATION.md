# 翻譯規格：第三批 AI 新聞的 en、ja、ko、zh-CN

繁中原稿已經過獨立查核，是唯一依據。翻譯不再查新資料、不增刪事實；發現原稿疑似錯誤時不要自己改，寫進回報。

## 每個語言交一份 GuideDocument

寫到 scratchpad：`C:\Users\x8120\AppData\Local\Temp\claude\C--Users-x8120-mokaair--claude-worktrees-recent-ai-news-4fadd1\dcb1f5ce-dad2-44d0-8d44-f86d22d333b3\scratchpad\tr\<slug>.<locale>.json`，
內容是 `{"title","description","hero","blocks","sources"}`，形狀和內容包裡的 zh-TW 完全相同：

- blocks 型別、順序、heading level、table 的 header 欄數與 rows 列數都照原稿。
- `hero.src` → `/guides/<slug>/hero-<en|ja|ko|zh-cn>.jpg`；diagram 的 `src` → `/guides/<slug>/diagram-1-<en|ja|ko|zh-cn>.svg`；
  width、height、credit 不變；alt 與 caption 要翻譯。
- `sources`：title 翻譯（廠商名與頁面原名保留），url 與 checked_on 不變。
- 兩個 link：url 換成 `https://mokaair.com/<locale>/life/<slug>`，text 必須逐字等於目標內容包在該 locale 的 `title`
  （第一個是 `ai-news-2026-january-september-index`，第二個見 BRIEF 表格；打開 `apps/api/app/guides/content/<target>.json` 複製）。

合併：在 `apps/api` 目錄執行
`PYTHONIOENCODING=utf-8 /c/Users/x8120/mokaair/apps/api/.venv/Scripts/python.exe ../../docs/ai-news-2026-09-mid/merge_locale.py <slug> <locale> <檔案>`。
印出 REFUSED 就修檔案再合併。**不要直接編輯內容包 JSON，也不要改 zh-TW。**

## 寫法

- 讀起來要像該語言的原生科技新聞解析，不是逐字直譯；但每個日期、數字、價格、方案名、地區、條件、歸因（「官方表示」「本站沒有實測」「編輯設計的例子」）都要保留，不可變強或變弱。
- 保留台灣讀者視角（例如「台灣帳號」「台灣時間」照譯，不改成讀者所在地）。
- 日期依語言習慣：en `September 10, 2026`；ja `2026年9月10日`；ko `2026년 9월 10일`；zh-CN `2026 年 9 月 10 日`。
- 產品介面字樣：官方有該語言的介面名稱就用官方的（例如 Apple、Google、OpenAI 各語言說明頁的設定名稱）；不確定時保留英文原名。
- zh-CN 用簡體字與大陸常用詞（账号、视频、软件、设置），不可混入繁體字。ja 用です・ます體。ko 用 합니다體。
- en 允許比中文長，lint 的 `text_length` 超過 6,000 字元只是警告，不要為此刪內容。
- 不要 Markdown、不要 emoji、不要加原稿沒有的句子。

## 研究紀錄

在 `docs/ai-news-2026-09-mid/research/<slug>.json` 加上
`"translations": {"en": {...}, "ja": {...}, "ko": {...}, "zh-CN": {...}}`，每個是
`{"hero_label": "…", "diagram": {"title": "…", "caption": "（逐字等於該語言內容包裡 diagram 的 caption）", "nodes": [[小標, 說明] ×4]}}`。
圖上字要短（會畫在 640px 寬的卡片裡）：en 小標 ≤ 18 字元、說明 ≤ 30 字元、hero_label ≤ 24 字元；ja／ko／zh-CN 小標 ≤ 10 字、說明 ≤ 17 字、hero_label ≤ 15 字。
圖上的數字必須出現在該語言正文。用 Edit 工具只加 `translations` 這個鍵，其他欄位不動。

## 自檢

全部四個語言合併、研究紀錄補好後，在 `apps/api` 執行
`PYTHONIOENCODING=utf-8 /c/Users/x8120/mokaair/apps/api/.venv/Scripts/python.exe ../../docs/ai-news-2026-09-mid/check_article.py <slug> --full`
直到 OK。
