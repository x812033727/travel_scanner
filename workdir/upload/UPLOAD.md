# 上傳步驟：山上滾水煮得慢，玉米為什麼又會爆開？｜原來如此事務所｜CC字幕

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

   - `captions/zh-TW.srt`

在「字幕」分頁新增語言並上傳對應的檔案；其他語系的標題與說明在 `description.<語系>.txt`。

## 3. 配音音軌（多語言音訊）

這支沒有配音音軌。要加，在 `/admin/videos` 這支影片的頁面勾那個語言的「配音」，工人做好會再送一張「語言」卡片。

## 4. 各語言的縮圖

沒有自己縮圖的語言（用 `thumbnail.jpg`，不用等）：
- en：i18n/en.json has no thumbnail words (i18n-sheet --locale en --parts metadata, then i18n-merge)
- ja：i18n/ja.json has no thumbnail words (i18n-sheet --locale ja --parts metadata, then i18n-merge)
- ko：i18n/ko.json has no thumbnail words (i18n-sheet --locale ko --parts metadata, then i18n-merge)

## 5. 上傳之後

回到 /admin/videos 這支影片的「可以上架」卡片貼上 YouTube 網址，並選上架時間；影片 ID 會寫進 `video.json`，影片就算完成。不要自己按公開：公開由站主選的時間決定。
