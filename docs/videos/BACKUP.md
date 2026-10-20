# 影片上傳後的雲端硬碟備份

影片上 YouTube 之後，把它的檔案依系列複製到站主的 Google 雲端硬碟。雲端的檔案經過核對、
網站也確認沒有缺檔之後，worker 才可以刪掉主機上的檔案。程式在
`apps/api/app/video_backup/`（設定與狀態）、`tools/video/automation/backup.mjs`（複製）、
`apps/web/components/admin-video-backup.tsx`（後台卡片），2026-10-19 隨 #1595 合併。
要真的開始備份，還要做完下面的〈主機設定〉。

## 為什麼要做

- 成片只存在 VPS。`video_work/<slug>/` 由 [`tidy.mjs`](../../tools/video/automation/tidy.mjs)
  在上傳 7 天後清掉 `final.mp4`、配音、clips、keyframes；審核區的 mp4 也由
  `prune_published_previews` 在 7 天後刪除。YouTube 上的版本是轉碼過的，不能當原檔。
- 漫劇與動畫（偶的江湖等）的 clips 是付費買的，重拍要再花點數，而且不一定拍得回同一個畫面。
- 加密的系統備份（[`2026-10-07-backup-google-drive-offsite`](../../tasks/open/2026-10-07-backup-google-drive-offsite.md)）
  是給災難還原用的，檔名也加密，站主在 G: 看不懂。影片備份要讓站主直接打開，所以是
  另一條不加密的路線。兩條路線用不同的 rclone remote 和設定檔，互不影響。

## 站主的決定（2026-10-15）

1. **備份位置**：站主電腦上是 `G:\我的雲端硬碟\AI\備份\`，雲端路徑是 `AI/備份`。
2. **授權用 A 案**：rclone 使用完整的 `drive` 權限，但 remote 設 `root_folder_id`
   鎖在 `AI/備份` 這個資料夾。只用 `drive.file` 的話，rclone 看不到站主自己建的
   「AI」資料夾，會另建一個同名的，造成 G: 出現兩個「AI」。
3. **備份層級**：漫劇與動畫（`category` 為 `drama`、`long-drama`、`anime`）用「完整」，
   其他用「基本」。後台可以依系列覆寫。
4. **還沒決定**：雲端硬碟的方案與容量。在決定之前，worker 只會在剩餘空間足夠時備份，
   不夠就停下並在後台提示（見〈空間〉）。

## 架構

```
後台「備份位置」卡 ──存──▶ ProviderConfig「video_backup」（路徑、開關、層級、資料夾名稱）
                                     │ worker 讀 GET /api/video/automation/backup/config
                                     ▼
video-worker 每一輪：排入 → rclone 複製 → rclone check → 上傳 backup.json → 回報網站
                                     │                                      │
                                     ▼                                      ▼
              Google Drive：AI/備份/<系列>/<集>/              video_projects.backup
                                     │                    網站依語言選擇再數一次有沒有缺檔
                                     ▼                                      │
              Google 雲端硬碟電腦版 → G:\我的雲端硬碟\AI\備份\               ▼
                                                     tidy：網站確認 done 之前不刪檔
```

- **在哪裡執行**：只有 `video-worker` 容器能寫 `video_work`，tidy 也在它那裡，所以備份在
  它每一輪的最後、tidy 之前跑。自動產生草稿關掉時也照樣備份。API 容器不放 Drive 的權杖。
- **權杖**：主機的 `/etc/travel-scanner/rclone-videos/rclone.conf`（擁有者 uid 1001，0600），
  compose 把這個**資料夾**唯讀掛到 worker 的 `/etc/mokaair/rclone-videos/`。掛資料夾而不是
  檔案：檔案還不存在時，Docker 會在那個位置建一個同名資料夾，之後就放不進設定檔。worker
  每輪把它複製到 `/tmp` 再交給 rclone，rclone 更新 access token 時不會去寫主機的檔案。
  權杖不進資料庫，也不重用 YouTube 的 OAuth（重用要加 scope、重新同意，還會影響 YouTube
  API 稽核）。`/etc/travel-scanner` 整個資料夾已經在每晚加密的設定包裡
  （`ops/backup/manifest-paths.txt`）。
- **鎖定範圍**：worker 的環境變數 `VIDEO_BACKUP_LOCK_PATH=AI/備份`（compose 設定）記錄
  `root_folder_id` 對應到的雲端路徑，worker 啟動時回報給網站。後台填的路徑必須是它本身或
  它底下的資料夾，超出範圍就拒絕儲存，並說明要在主機改 rclone 設定。

## 設定（後台：影片 → 設定 → 備份位置）

卡片在 `/admin/videos?tab=settings#video-backup-settings`。查看需要 `content.read`，儲存與
測試需要 `settings.manage`。存檔只送改過的欄位，並比對 `expected_updated_at`，避免覆寫別人的
修改；每次儲存都寫稽核紀錄。

| 欄位 | 說明 |
| --- | --- |
| 開關 | 關閉時 worker 不備份，tidy 也不會因為備份而保留檔案（回到原本的行為） |
| 路徑 | 可以貼 `G:\我的雲端硬碟\AI\備份\`、`G:\My Drive\AI\備份`、`AI/備份` 或 `/AI/備份/`；卡片會即時顯示「儲存為：AI/備份」 |
| 預設層級 | 依 `category` 決定：`drama`／`long-drama`／`anime` 用完整，其他用基本 |
| 系列覆寫 | 每個系列選預設、基本、完整或關閉 |
| 資料夾名稱 | 每個系列的雲端資料夾名稱，預設見下表 |
| 測試連線 | worker 下一輪（約 5 分鐘內）寫入再刪除 `_probe-<時間>.txt`，回報結果與剩餘空間；按「重新讀取」看結果 |

路徑的統一規則：去掉開頭的磁碟代號，去掉 `我的雲端硬碟` 或 `My Drive`，反斜線換成 `/`，
去掉頭尾的 `/`。路徑中不能有 `..`、不能是空字串，也不能有 Windows 不接受的字元
（`< > : " | ? *`）或以句點、空白結尾的資料夾，否則雲端硬碟電腦版同步不到 G:。

卡片最上面直接回答「上傳的影片都備份到雲端了嗎」：全部完成，或還有幾支沒完成。下面列出
沒完成的每一支（按「顯示全部影片」可以看全部）：狀態、資料夾、缺哪些檔案、失敗原因、是否
已等待超過 24 小時，完成的顯示時間和大小。

## 資料夾排法

```
AI/備份/
  <系列資料夾>/
    _共用/characters/…              （僅完整層級：_series/<系列>/characters）
    <集數三位數>-<slug>/  或  <slug>/
      final.mp4
      thumbnail.jpg、thumbnail-b.jpg…、thumbnails/<語言>.jpg
      metadata.json
      captions/<語言>.srt
      descriptions/<語言>.txt
      dubs/<語言>.m4a
      backup.json
      _舊版/<時間>/…                 （之後被覆蓋的舊檔）
      （完整層級另外有）clips/ keyframes/ characters/ timeline.json narration.wav
  Shorts/<shorts_series 或 shorts_line>/<slug>/…
  其他/<slug>/…
```

**系列鍵**依序取第一個有值的：Shorts 一律放在 `Shorts/<shorts_series 或 shorts_line>/` →
`series_slug` → slug 開頭（`curio-`、`ai-term-`、`sothatswhy-`、`story-`）→ `category`。
都沒有就放「其他」。

| 系列鍵 | 預設資料夾名稱 |
| --- | --- |
| `curio` | 奇聞檔案局 |
| `ou-de-jianghu` | 偶的江湖 |
| `sothatswhy` | 原來如此事務所 |
| `ai-terms` | AI 名詞十分鐘 |
| `story` | 品牌故事 |
| `other` | 其他 |
| 其他 | 系列鍵本身 |

**資料夾名稱只決定一次。** 第一次備份時，實際用到的資料夾寫進
`video_projects.backup.folder`，之後補備份都沿用它。之後改系列顯示名稱，不會讓同一支
影片被分到兩個資料夾。

## 每一層備份哪些檔

來源都是 `video_work/<slug>/`。

- **基本**：整個 `upload/` 上傳包：`final.mp4`、`metadata.json`、`captions/<語言>.srt`、
  `dubs/<語言>.m4a`、`thumbnail.jpg`、測試縮圖 `thumbnail-b.jpg` 等、各語言縮圖
  `thumbnails/<語言>.jpg`；`description.<語言>.txt` 放進 `descriptions/<語言>.txt`。上傳包
  裡沒有縮圖時，用工作資料夾根目錄的 `thumbnail.jpg`。Shorts 的上傳包是 `final.mp4`、
  `zh-TW.srt`、`cover.png`、`titles.json`。
- **完整**：基本的全部，加上 `clips/`、`keyframes/`、`characters/`、`timeline.json`、
  `narration.wav`；系列共用的 `_series/<系列>/characters/` 放在系列資料夾的 `_共用/`。
- **任何層級都不備份**：`segments/`、`build/`、`frames/`、`review/`、`media/` 快取、
  `audio/` 中間檔。這些可以重算，或只是審核用的預覽。

## 流程

1. **排入**：每一輪掃描網站列出的、有 YouTube ID 的影片。還沒有備份紀錄的就排入
   （`pending`），所以剛上傳的影片、Shorts 和上線前已經上傳的舊影片都會被排進來。
   每支影片的備份狀態存在工作資料夾的 `backup-state.json`，不放進 `auto.json`，避免產線
   存檔時蓋掉它。
2. **列清單**：依層級列出檔案，計算 sha256 與大小。上一次 `backup.json` 裡大小與修改時間
   相同的檔案沿用舊的雜湊，不用每輪重讀幾 GB 的成片。
3. **檢查空間**：`rclone about`。剩餘空間少於「這次要傳的量 + 2 GB」就不傳，狀態記為
   `blocked_quota`，把剩餘空間回報網站。
4. **複製**：先把要傳的檔案用硬連結排成雲端的目錄結構（`<工作根目錄>/_backup-stage/<slug>/`，
   做完就刪），再 `rclone copy --checksum --drive-chunk-size 64M --tpslimit 5 --retries 5`。
   雲端已經有同名但內容不同的檔案時，舊版用 `--backup-dir` 移到 `<集>/_舊版/<時間>/`，
   不會被覆蓋掉。**永遠不刪雲端上的檔案**：只用 `copy`，不用 `sync`。
5. **核對**：`rclone check --one-way`，用雲端硬碟記錄的 md5 比對，不必下載。全部一致之後
   才上傳 `backup.json`，然後才回報 `done`。
6. **網站再數一次**：回報要附上雲端實際有哪些檔案。網站拿它跟 `final.mp4`、
   `metadata.json`（Shorts 只要 `final.mp4`）和站主選的每一種語言（說明、字幕、配音）比對；
   上傳包有寫明原因而跳過的部分不算缺。少了任何一個，網站就把它記成 `partial`
   並列出缺什麼，tidy 不會刪這支影片的檔案。之後站主又加選語言或改成完整層級，原本完成的
   備份會顯示「需要補備份」（`stale`）。
7. **補備份**：配音和翻譯字幕常常晚幾天才核准。每一輪都比對目前的檔案和 `backup.json`，
   有新增或改過的檔案就重新排入，只傳新增或改過的。tidy 已經清掉的檔案不算改變，
   雲端那份還在。
8. **失敗**：每輪最多備份 `VIDEO_BACKUP_PER_ROUND`（預設 2）支影片，最舊的先做；每輪最多
   送 10 筆「排入」或補送的回報。失敗的下一輪重試；連續失敗 3 次標記為 `failed`，寫入
   稽核紀錄，之後每 6 小時再試一次。工作根目錄的 `STOP` 檔也會停止備份。

## 跟 tidy 的關係

[`tidy.mjs`](../../tools/video/automation/tidy.mjs) 對每支已上傳的影片多一道保留條件：
**備份開啟時，只有 worker 這邊是 `done`、網站也回答 `done`、而且沒有新增或改過的檔案，
才可以清。** 其他情況都保留：還沒備份、失敗、空間不足、缺檔、網站沒收到回報、網站連不上、
主機還沒設定 rclone。保留的原因寫在 tidy 的紀錄裡（`not in Google Drive yet: …`），
每輪也會印出有幾支因此保留。

備份關閉時，或網站還沒有這些 API（回 404）時，tidy 照原本的方式運作。

`prune_published_previews` 刪的是審核區的副本，原檔還在 `video_work`，所以這裡不用改。

## 主機設定

部署之後還要做一次。前四步要站主本人在自己的電腦上做，權杖不要貼到任何對話裡。

1. **Google Cloud**：到 Google Cloud Console，用現有的專案或新建一個：
   - 啟用「Google Drive API」。
   - OAuth 同意畫面：使用者類型選「外部」，發布狀態要按「發布應用程式」改成「正式版」。
     留在「測試」狀態的話，Google 發的 refresh token 7 天就失效，備份每週都會斷。只有站主
     自己使用，不必送審；授權時會看到「Google 尚未驗證這個應用程式」，按「進階」繼續即可。
   - 「憑證」→「建立憑證」→「OAuth 用戶端 ID」→ 類型選「電腦版應用程式」，記下用戶端 ID
     和用戶端密鑰。不要用 YouTube 那組用戶端。
2. **授權**：在電腦上安裝 rclone（<https://rclone.org/downloads/>），執行
   `rclone authorize "drive" "<用戶端 ID>" "<用戶端密鑰>"`。瀏覽器會開啟，用放
   `AI/備份` 的那個 Google 帳號登入並允許。終端機會印出一段 `{"access_token":...}` 的 JSON，
   那就是 token。
3. **資料夾 ID**：在 drive.google.com 打開 `AI/備份`，網址
   `https://drive.google.com/drive/folders/<這一段>` 的最後一段就是 `root_folder_id`。
4. **寫設定檔**：照 [`ops/video/rclone-videos.conf.example`](../../ops/video/rclone-videos.conf.example)
   填好 `client_id`、`client_secret`、`root_folder_id`、`token`。
5. **放到主機**：把設定檔傳到主機（例如 `scp rclone.conf root@<主機>:`），再以 root 執行：

   ```bash
   install -d -m 0750 -o 1001 -g 1001 /etc/travel-scanner/rclone-videos
   install -m 0600 -o 1001 -g 1001 rclone.conf /etc/travel-scanner/rclone-videos/rclone.conf
   rm rclone.conf   # 主機上別留第二份
   ```

   uid 1001 是 video-worker 容器裡的 pwuser。資料夾是掛進容器的，放好檔案不必重啟容器。
6. **確認 rclone 只看得到 `AI/備份`**：

   ```bash
   cd /root/travel_scanner
   docker compose -f docker-compose.prod.yml exec -T video-worker sh -c \
     'cp /etc/mokaair/rclone-videos/rclone.conf /tmp/rv.conf && export RCLONE_CONFIG=/tmp/rv.conf && rclone lsd videobackup: && rclone about videobackup:; rm -f /tmp/rv.conf'
   ```

   `lsd` 應該只列出 `AI/備份` 裡面的資料夾（一開始是空的）；看到雲端硬碟最上層的資料夾，
   就是 `root_folder_id` 填錯了。
7. **開啟**：後台「備份位置」卡確認「主機的 rclone 可以寫入 AI/備份」，勾選開關、儲存，
   按「測試連線」，等 5 分鐘按「重新讀取」，看到「上次測試成功」和剩餘空間。
8. **第一支**：之後每一輪會備份最舊的兩支。第一支完成後在電腦的
   `G:\我的雲端硬碟\AI\備份\<系列>\` 裡看得到檔案，卡片上那支顯示「已備份」。
   想在主機上再核對一次：

   ```bash
   docker compose -f docker-compose.prod.yml exec -T video-worker sh -c \
     'cp /etc/mokaair/rclone-videos/rclone.conf /tmp/rv.conf && RCLONE_CONFIG=/tmp/rv.conf rclone check /var/lib/mokaair/video-work/<slug>/upload "videobackup:<資料夾>" --one-way --exclude "/description.*" ; rm -f /tmp/rv.conf'
   ```

   `<資料夾>` 是卡片「資料夾」欄 `AI/備份/` 後面那一段（例如 `奇聞檔案局/curio-h01`）。
   說明檔在雲端改名成 `descriptions/`，所以這裡略過；完整的核對每一輪都做過。

### 出問題時

| 卡片或 log 上看到 | 原因與處理 |
| --- | --- |
| 「主機沒有影片備份用的 rclone 設定」 | 第 5 步的檔案不在，或路徑打錯 |
| 「讀不到 …；檔案要讓容器的 pwuser 讀得到」 | 檔案或資料夾不是 uid 1001，重做第 5 步的 `install` |
| 「路徑 … 不在主機鎖定的 AI/備份 之內」 | 後台路徑填到 `AI/備份` 外面了；要備份到別處，改 `root_folder_id` 和 compose 的 `VIDEO_BACKUP_LOCK_PATH` 再部署 |
| 測試失敗，`invalid_grant` | token 失效：多半是 OAuth 同意畫面還在「測試」，或站主撤銷了授權。改成正式版後重做第 2、4、5 步 |
| 「雲端空間不足」 | 剩餘空間少於這次要傳的量加 2 GB；清空間或升級方案，下一輪會自動再試 |
| 「缺少檔案」 | 網站列出缺哪些；多半是配音或字幕還沒做完，做完後下一輪會補 |

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

開啟之後，每支已有 YouTube ID 的影片都會排入，照一般流程備份，每輪兩支。已經被 tidy
清掉成片的影片，只會備份還在的檔案（縮圖、字幕、說明）；網站會把它記成「缺少檔案」並列出
缺 `final.mp4`，讓站主知道這幾支只能從別處找原檔。

## 本機製作的影片

站主電腦上做的影片（例如本機的海螺製作）用同一套排法：本機工具以
`VIDEO_BACKUP_LOCAL_ROOT`（預設 `G:\我的雲端硬碟`）加上設定的雲端路徑，直接把檔案
複製進去，由 Google 雲端硬碟電腦版上傳。`backup.json` 格式相同。Drive 電腦版
上傳完成以前，本機不能刪原檔：要確認 DriveFS 沒有待上傳的工作、雲端大小也一致。
這部分還沒做（`tasks/open/2026-10-15-video-backup-local.md`）。

## 還原

找到 `AI/備份/<系列>/<集>/backup.json`，按 `files` 清單下載，比對 sha256。
要重新上架時，`final.mp4`、`captions/`、`descriptions/`、`dubs/` 就是一份完整的手動上傳包
（對應 [MANUAL-UPLOAD.md](MANUAL-UPLOAD.md)）。
