# 影片上傳後的雲端硬碟備份

影片上 YouTube 之後，把上傳包依系列複製到站主的 Google 雲端硬碟，確認雲端的檔案
與主機一致後，才允許 worker 刪掉主機上的檔案。本文是設計；實作拆成
`tasks/open/2026-10-15-video-backup-*.md` 幾張票。

## 為什麼要做

- 成片只存在 VPS。`video_work/<slug>/` 由 [`tidy.mjs`](../../tools/video/automation/tidy.mjs)
  在上傳 7 天後清掉 `final.mp4`、配音、clips、keyframes；審核區的 mp4 也由
  `prune_published_previews` 在 7 天後刪除。YouTube 上的版本是轉碼過的，不能當原檔。
- 漫劇與動畫（偶的江湖等）的 clips 是付費買的，重拍要再花點數，而且不一定拍得回同一個畫面。
- 加密的系統備份（[`2026-10-07-backup-google-drive-offsite`](../../tasks/open/2026-10-07-backup-google-drive-offsite.md)）
  是給災難還原用的，檔名也加密，站主在 G: 看不懂。影片備份要讓站主直接打開，所以是
  另一條不加密的路線。兩條路線用不同的 rclone remote，互不影響。

## 站主的決定（2026-10-15）

1. **備份位置**：站主電腦上是 `G:\我的雲端硬碟\AI\備份\`，雲端路徑是 `AI/備份`。
2. **授權用 A 案**：rclone 使用完整的 `drive` 權限，但 remote 設 `root_folder_id`
   鎖在 `AI/備份` 這個資料夾。只用 `drive.file` 的話，rclone 看不到站主自己建的
   「AI」資料夾，會另建一個同名的，造成 G: 出現兩個「AI」。
3. **備份層級**：漫劇與動畫（`category` 為 `drama`、`long-drama`、`anime`）用「完整」，
   其他用「基本」。後台可以依系列覆寫。
4. **還沒決定**：雲端硬碟的方案與容量。在決定之前，worker 只會在剩餘空間足夠時備份，
   不夠就停下並在後台提示（見「空間」）。

## 架構

```
後台「備份位置」卡 ──存──▶ ProviderConfig「video_backup」（路徑、層級、開關）
                                     │ worker 透過 automation API 讀取
                                     ▼
video-worker 每一輪：記下 YouTube ID → 排進備份 → rclone 複製 → 檢查 → 回報網站
                                     │                              │
                                     ▼                              ▼
              Google Drive：AI/備份/<系列>/<集>/        video_projects.backup（後台顯示）
                                     │                tidy：沒備份完不准刪檔
                                     ▼
              Google 雲端硬碟電腦版 → G:\我的雲端硬碟\AI\備份\
```

- **在哪裡執行**：只有 `video-worker` 容器能寫 `video_work`，而且 `auto.json` 和 tidy
  都是它在管，所以備份放在它的每一輪裡跑，順序是 tidy 之前。API 容器只把 `video_work`
  掛成唯讀，也不放 Drive 的權杖。
- **權杖**：放在主機的 `/etc/travel-scanner/rclone-videos.conf`（root、0600），
  唯讀掛進 worker。不存進資料庫，也不重用 YouTube OAuth：重用的話要加 scope、
  重新同意授權，還會影響 YouTube API 稽核。這個檔和加密備份的 `rclone.conf` 分開放，
  `ops/backup/manifest-paths.txt` 也要加上它，讓它進入每晚的設定包。
- **鎖定範圍**：worker 的環境變數 `VIDEO_BACKUP_LOCK_PATH=AI/備份` 記錄
  `root_folder_id` 對應到的雲端路徑。後台填的路徑必須是它本身或它底下的資料夾，
  超出範圍就拒絕儲存，並說明要在主機改 rclone 設定。

## 設定（後台：影片 → 設定 → 備份位置）

寫法比照 [`vps_settings.py`](../../apps/api/app/video_youtube/vps_settings.py)：
是一筆私人的 ProviderConfig；存檔時檢查 `expected_updated_at`，避免覆寫別人的修改；
會寫稽核紀錄；儲存需要 `settings.manage` 權限，查看需要 `content.read`。

| 欄位 | 說明 |
| --- | --- |
| 開關 | 關閉時 worker 不備份，tidy 也不會因為備份而保留檔案（回到現在的行為） |
| 路徑 | 可以貼 `G:\我的雲端硬碟\AI\備份\`、`G:\My Drive\AI\備份`、`AI/備份` 或 `/AI/備份/`；存檔時統一成 `AI/備份` |
| 預設層級 | 依 `category` 決定：`drama`／`long-drama`／`anime` 用完整，其他用基本 |
| 系列覆寫 | `{系列鍵: basic \| full \| off}` |
| 資料夾名稱 | `{系列鍵: 顯示名稱}`，預設見下表 |
| 測試 | 送出測試請求，worker 下一輪寫入再刪除 `_probe-<時間>.txt`，回報結果與剩餘空間 |

路徑的統一規則：去掉開頭的磁碟代號，再去掉 `我的雲端硬碟` 或 `My Drive`，
反斜線換成 `/`，去掉頭尾的 `/`。路徑中不能有 `..`，也不能是空字串。

## 資料夾排法

```
AI/備份/
  <系列資料夾>/
    _共用/characters/…              （僅完整層級：_series/<系列>/characters）
    <集數三位數>-<slug>/  或  <slug>/
      final.mp4
      thumbnail.jpg
      metadata.json
      captions/<語言>.srt
      descriptions/<語言>.txt
      dubs/<語言>.m4a
      backup.json
      （完整層級另外有）clips/ keyframes/ characters/ timeline.json narration.wav
  Shorts/<shorts_series 或 shorts_line>/<slug>/…
  其他/<slug>/…
```

**系列鍵**依序取第一個有值的：`series_slug` → Shorts 的 `shorts_series`（放在
`Shorts/` 底下）→ slug 開頭（`curio-`、`ai-term-`、`sothatswhy-`）→ `category`。
都沒有就放「其他」。

| 系列鍵 | 預設資料夾名稱 |
| --- | --- |
| `curio` | 奇聞檔案局 |
| `ou-de-jianghu` | 偶的江湖 |
| `sothatswhy` | 原來如此事務所 |
| `ai-terms` | AI 名詞十分鐘 |
| `story` | 品牌故事 |
| 其他 | 系列鍵本身 |

**資料夾名稱只決定一次。** 第一次備份時，實際用到的資料夾寫進
`video_projects.backup.folder`，之後補備份都沿用它。之後改系列顯示名稱，不會讓同一支
影片被分到兩個資料夾。

## 每一層備份哪些檔

來源都是 `video_work/<slug>/`。

- **基本**：`upload/` 裡的 `final.mp4`、`metadata.json`、`description.<l>.txt`
  （放進 `descriptions/`）、`captions/<l>.srt`、`dubs/<l>.m4a`，再加上根目錄的
  `thumbnail.jpg`。
- **完整**：基本的全部，加上 `clips/`、`keyframes/`、`characters/`、`timeline.json`、
  `narration.wav`；系列共用的 `_series/<系列>/characters/` 每個系列只備份一份，放在
  `_共用/`。
- **任何層級都不備份**：`segments/`、`build/`、`frames/`、`review/`、`media/` 快取、
  `audio/` 中間檔。這些可以重算，或只是審核用的預覽。

## 流程

1. **排入**：`recordVideoId`（[flow.mjs](../../tools/video/automation/flow.mjs)）記下
   YouTube ID 時，在 `auto.json` 寫 `backup: {state: "pending"}`。三種上傳方式
   （手動貼網址、API、VPS 上傳器）最後都會經過這裡；Shorts 由認領流程記下 ID 後，
   下一輪掃描也會排入。
2. **列清單**：依層級列出要備份的檔案，計算 sha256 與大小，產生 `backup.json` 的草稿：
   `{slug, youtube_video_id, series, folder, tier, files: [{path, sha256, size}], backed_up_at}`。
3. **檢查空間**：用 `rclone about` 讀剩餘空間。剩餘空間少於「這次要傳的量 + 2 GB」就不傳，
   狀態記為 `blocked_quota`，回報網站。
4. **複製**：執行 `rclone copy --checksum --drive-chunk-size 64M --tpslimit 5 --retries 5`。
   遠端已經有同名但內容不同的檔案（例如上傳後重剪），舊版用 `--backup-dir` 移到
   `<集>/_舊版/<時間>/`，不會覆蓋掉。**永遠不刪雲端上的檔案**：只用 `copy`，不用 `sync`。
5. **檢查**：執行 `rclone check --one-way --download=false`，以 Drive 的 md5 和大小比對。
   全部一致之後才上傳 `backup.json`，最後才在 `auto.json` 寫
   `backup: {state: "done", at, bytes, files_hash}`。
6. **回報**：呼叫 automation API，寫入 `video_projects.backup`（JSON：
   `state`、`folder`、`tier`、`bytes`、`at`、`error`、`attempts`）。後台影片卡顯示
   「已備份 ✓ 時間／大小」，失敗時顯示原因。
7. **補備份**：配音和翻譯字幕常常晚幾天才核准。每一輪都重新計算清單的 hash（`files_hash`），
   跟上次備份的不一樣就排回 `pending`，只傳新增或變動的檔案。
8. **失敗**：每輪最多處理 `VIDEO_BACKUP_PER_ROUND`（預設 2）支影片，最舊的先做。
   失敗的下一輪重試；連續失敗 3 次標記為 `failed`，後台出現紅燈並寫入稽核紀錄，之後
   每 6 小時再試一次。worker 目錄裡的 `STOP` 檔也會停止備份。

## 跟 tidy 的關係

[`tidy.mjs`](../../tools/video/automation/tidy.mjs) 的 `judge` 加一個保留條件：
**備份開啟時，`auto.json.backup.state` 不是 `done`，或目前清單的 hash 跟
`files_hash` 不一樣，就保留，不刪。** 備份壞掉時，影片只是延後刪除，不會不見。
保留的原因會顯示在 tidy 的紀錄裡（`backup pending` / `backup failed` / `backup quota`）。

`prune_published_previews` 刪的是審核區的副本，原檔還在 `video_work`，所以這裡不用改。

## 空間

站主還沒決定方案，以下用文件裡的實測值估算：

| 種類 | 基本層級／支 |
| --- | --- |
| 純投影片 | 約 10 MB/分鐘 |
| 插畫版 | 約 40 MB/分鐘，最多約 70 MB/分鐘（13:22 的片是 535 MB） |
| 配音 | 每種語言約 1 MB/分鐘 |

完整層級要多算 clips 與 keyframes，第一次實際備份後把量到的數字補進這裡。
免費的 15 GB 大約只放得下二、三十支插畫版。

## 已經上傳的舊影片

上線時，每部已有 YouTube ID 而且還沒被 tidy 清掉的影片，都會排一次 `pending`，
照一般流程備份。已經清掉的影片只備份還在的檔案（縮圖、字幕、說明），`backup.json`
記 `partial: true`，並列出缺了哪些檔。

## 本機製作的影片

站主電腦上做的影片（例如本機的海螺製作）用同一套排法：本機工具以
`VIDEO_BACKUP_LOCAL_ROOT`（預設 `G:\我的雲端硬碟`）加上設定的雲端路徑，直接把檔案
複製進去，由 Google 雲端硬碟電腦版上傳。`backup.json` 格式相同。Drive 電腦版
上傳完成以前，本機不能刪原檔：要確認 DriveFS 沒有待上傳的工作、雲端大小也一致。

## 還原

找到 `AI/備份/<系列>/<集>/backup.json`，按 `files` 清單下載，比對 sha256。
要重新上架時，`final.mp4`、`captions/`、`descriptions/`、`dubs/` 就是一份完整的手動上傳包
（對應 [MANUAL-UPLOAD.md](MANUAL-UPLOAD.md)）。
