# 上傳步驟：羽絨衣一點熱都不會產生，為什麼穿上就暖？｜原來如此事務所｜CC字幕

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

- `dubs/en.m4a`（en，最快處 1.15 倍速）
- `dubs/ja.m4a`（ja，最快處 1.15 倍速）
- `dubs/ko.m4a`（ko）
- `dubs/es.m4a`（es，最快處 1.03 倍速）
- `dubs/pt.m4a`（pt）
- `dubs/id.m4a`（id，最快處 1.05 倍速）
- `dubs/vi.m4a`（vi）
- `dubs/th.m4a`（th，最快處 1.01 倍速）

每個語系做一次：Studio 左選單「語言」→ 這支影片 →「新增語言」→ 選語言 →「配音」旁的「新增」→「選取檔案」→ 選對應的檔案 →「發布」。上架前或上架後都可以加。

- 頻道要有「進階功能」（設定 → 頻道 → 功能使用資格）。
- YouTube 已經替這個語言自動配音的話，要先在同一頁刪掉自動配音，才傳得上去；建議在設定 → 頻道 → 進階設定取消「允許自動配音」。
- 傳完到影片頁的「語言」卡片按「已在 Studio 上傳配音」；標題說明與字幕由網站的 API 送上，不用手動。

## 4. 各語言的縮圖

要上傳的縮圖（每個語言一張，字換成該語言，畫面與版型同 `thumbnail.jpg`）：

- `thumbnails/en.jpg`（en）
- `thumbnails/ja.jpg`（ja）
- `thumbnails/ko.jpg`（ko）
- `thumbnails/es.jpg`（es）
- `thumbnails/pt.jpg`（pt）
- `thumbnails/id.jpg`（id）
- `thumbnails/vi.jpg`（vi）
- `thumbnails/th.jpg`（th）

先照第 1 節傳好 `thumbnail.jpg`。每個語言做一次：Studio 左選單「語言」→ 這支影片 → 點那個語言的名稱 →「縮圖」旁的「新增」→ 選對應的檔案 →「更新」。要點的是語言名稱，所以那個語言要先列在這支影片的「語言」頁：第 2、3 節的字幕、配音或標題說明傳上去後就會列出。

- YouTube 說明頁寫的條件：只適用長片（不含 Shorts），頻道要能使用「進階功能」。
- 觀眾看到的是符合他語言設定的縮圖；沒有自己縮圖的語言看到 `thumbnail.jpg`。
- 說明頁只寫了 Studio 的做法、沒提到 API，網站也不送它：只能在 Studio 手動傳。

## 5. 上傳之後

回到 /admin/videos 這支影片的「可以上架」卡片貼上 YouTube 網址，並選上架時間；影片 ID 會寫進 `video.json`，影片就算完成。不要自己按公開：公開由站主選的時間決定。
