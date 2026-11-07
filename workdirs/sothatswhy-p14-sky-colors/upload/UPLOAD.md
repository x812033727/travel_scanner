# 上傳步驟：同一道陽光，天空為什麼是藍的、夕陽卻是紅的？｜原來如此事務所｜CC字幕

這個資料夾就是要上傳的全部內容。自動品管與上傳包檢查已經做過；這裡只剩站主自己在 YouTube Studio 的操作，公開的時間也由站主決定。

## 1. 上傳（Studio → 建立 → 上傳影片）

1. 上傳 `final.mp4`。**瀏覽權限先選「私人」**。
2. 標題：`description.zh-TW.txt` 的第一行。
3. 說明：`description.zh-TW.txt` 第三行以後的全部內容（章節時間戳已經在裡面）。
4. 縮圖：上傳 `thumbnail.jpg`（帳號需完成手機驗證）。
5. 目標觀眾：選「否，這不是為兒童打造的內容」。
6. 標籤：貼上 `metadata.json` 的 `tags`。類別：科學與技術（27）。影片語言：中文（台灣）。
7. 「變造或合成內容」：勾「是」。`metadata.json` 的 `contains_synthetic_media` 是 `true`（a drama: AI-generated shots and music are always disclosed）。

## 2. 字幕

   - `captions/en.srt`
   - `captions/es.srt`
   - `captions/id.srt`
   - `captions/ja.srt`
   - `captions/ko.srt`
   - `captions/pt.srt`
   - `captions/th.srt`
   - `captions/vi.srt`
   - `captions/zh-TW.srt`

在「字幕」分頁新增語言並上傳對應的檔案；其他語系的標題與說明在 `description.<語系>.txt`。

## 3. 配音音軌（多語言音訊）

要上傳的音軌：

- `dubs/en.m4a`（en，最快處 1.07 倍速）
- `dubs/ja.m4a`（ja，最快處 1.15 倍速）
- `dubs/ko.m4a`（ko）
- `dubs/es.m4a`（es）
- `dubs/pt.m4a`（pt，最快處 1.14 倍速）
- `dubs/id.m4a`（id，最快處 1.04 倍速）
- `dubs/vi.m4a`（vi）
- `dubs/th.m4a`（th，最快處 1.02 倍速）

每個語系做一次：Studio 左選單「語言」→ 這支影片 →「新增語言」→ 選語言 →「配音」旁的「新增」→「選取檔案」→ 選對應的檔案 →「發布」。上架前或上架後都可以加。

- 頻道要有「進階功能」（設定 → 頻道 → 功能使用資格）。
- YouTube 已經替這個語言自動配音的話，要先在同一頁刪掉自動配音，才傳得上去；建議在設定 → 頻道 → 進階設定取消「允許自動配音」。
- 傳完到影片頁的「語言」卡片按「已在 Studio 上傳配音」；標題說明與字幕由網站的 API 送上，不用手動。

## 4. 各語言的縮圖

沒有自己縮圖的語言（用 `thumbnail.jpg`，不用等）：
- en：i18n/en.json has no thumbnail words (i18n-sheet --locale en --parts metadata, then i18n-merge)
- ja：i18n/ja.json has no thumbnail words (i18n-sheet --locale ja --parts metadata, then i18n-merge)
- ko：i18n/ko.json has no thumbnail words (i18n-sheet --locale ko --parts metadata, then i18n-merge)
- es：not drawn yet; run render
- pt：not drawn yet; run render
- id：not drawn yet; run render
- vi：not drawn yet; run render
- th：not drawn yet; run render

## 5. 上傳之後

回到 /admin/videos 這支影片的「可以上架」卡片貼上 YouTube 網址，並選上架時間；影片 ID 會寫進 `video.json`，影片就算完成。不要自己按公開：公開由站主選的時間決定。
