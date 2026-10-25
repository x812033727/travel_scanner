# 影片的雲端硬碟備份

影片可以上架（或已經上 YouTube）時，把它的檔案依系列複製到站主的 Google 雲端硬碟。雲端的檔案經過核對、
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
3. **備份層級**：有備份的影片一律用「完整」（站主 2026-10-23）；後台可以把某個系列改成
   基本或關閉。之前只有漫劇與動畫預設完整，沒設定過的新系列（例如 `brand-stories-adapt`）
   就落到基本。
4. **容量**：站主的方案是 5 TiB（2026-10-22 量到剩 4.77 TiB）。worker 仍然只在剩餘空間
   足夠時備份，不夠就停下並在後台提示（見〈空間〉）。
5. **層級（2026-10-20 後台）**：站主把所有系列都改成「完整」。
6. **什麼時候備份（2026-10-23）**：影片做完、可以上架時就備份，不必等上 YouTube；之後改版，
   等再次可以上架時再覆蓋。之前只備份已上 YouTube 的影片，卡在每月草稿上限或要手動上架的
   成片，在上傳之前只存在主機上。

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
  它每一輪的最後、tidy 之前跑。自動產生草稿關掉時也照樣備份。一輪中途出錯結束時也照樣
  備份，只是不跑 tidy：2026-10-21 網站每輪都拒絕一個太長的提示詞，在這個修正之前，
  每一輪都在跑到備份之前就結束了。API 容器不放 Drive 的權杖。
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
| 預設層級 | 完整（系列沒有覆寫時） |
| 系列覆寫 | 每個系列選預設、基本、完整或關閉 |
| 資料夾名稱 | 每個系列的雲端資料夾名稱，預設見下表 |
| 測試連線 | worker 下一輪（約 5 分鐘內）寫入再刪除 `_probe-<時間>.txt`，回報結果與剩餘空間；按「重新讀取」看結果 |

路徑的統一規則：去掉開頭的磁碟代號，去掉 `我的雲端硬碟` 或 `My Drive`，反斜線換成 `/`，
去掉頭尾的 `/`。路徑中不能有 `..`、不能是空字串，也不能有 Windows 不接受的字元
（`< > : " | ? *`）或以句點、空白結尾的資料夾，否則雲端硬碟電腦版同步不到 G:。

卡片最上面直接回答「完成的影片都備份到雲端了嗎」（已上傳和可以上架的都算）：全部完成，或還有幾支沒完成。下面列出
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
                       dubs/未進上傳包/<語言>.m4a、captions/未進上傳包/<語言>.srt、
                       上傳包缺的 thumbnails/<語言>.jpg
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
  另外照站主勾的語言（`languages.json`）補上傳包沒有的東西：勾了配音、工人錄出音軌
  （`dubs/<語言>.m4a`／`.mp3`／`.wav`）卻沒進上傳包的（被放棄的，或還沒核准的），放進
  `dubs/未進上傳包/<語言>.m4a`；勾了字幕（或配音，配音一定帶字幕）、工作資料夾有
  `captions/<語言>.srt` 卻沒進上傳包的，放進 `captions/未進上傳包/<語言>.srt`；勾了任何一項
  的語言，上傳包缺它的縮圖時，用工作資料夾 `thumbnails/<語言>.jpg` 補進 `thumbnails/`。
  沒進上傳包的音軌與字幕沒過工人的檢查，要上架前先聽過、看過；它們放在自己的資料夾，網站
  不會把它們算成已打包的配音或字幕。沒有 `languages.json` 時，工作資料夾有的音軌、字幕和
  縮圖都備份。站主 2026-10-23：「所有選的語系語音、縮圖跟 CC 都要」。tidy 會清掉工作資料夾的音軌，所以已備份完成的完整層級影片
  有這些新檔時會再排一次，傳完才清。
- **任何層級都不備份**：`segments/`、`build/`、`frames/`、`review/`、`media/` 快取、
  `audio/` 中間檔。這些可以重算，或只是審核用的預覽。

## 流程

1. **排入**：每一輪掃描網站列出的影片：有 YouTube ID 的，加上**可以上架**的
   （和審核頁的 `ready_to_upload` 同一條規則：上架確認已核准、語言已決定、選的每一項都已做好
   或略過、沒有放棄；Shorts 只要上架確認已核准）。還沒有備份紀錄的就排入（`pending`），
   所以可以上架還沒上傳的、剛上傳的、Shorts 和上線前已經上傳的舊影片都會被排進來。
   工作資料夾要有 `auto.json`（工人做的），或至少有 `upload/final.mp4`（手動做的，例如
   續作或重剪，2026-10-23 起）；兩樣都沒有的資料夾不排入。
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
   雲端那份還在。可以上架時備份的影片，上傳後 `backup.json` 的 `youtube_video_id` 還是
   `null`，所以也重新排入一次：沒有檔案要傳，只把帶 YouTube ID 的 `backup.json` 再送一次。
8. **改版**：還沒上傳的影片換版（`renew_final`）時，上架確認會被取代，網站就不再把它列給
   worker，改到一半的檔案不會被傳上去。站主再次核准上架確認、它又可以上架時，回到清單，
   上一步的比對發現檔案改過，就把新檔傳上去覆蓋；被覆蓋的舊檔照第 4 步移到
   `_舊版/<時間>/`。網站也拒絕不在清單上的影片的回報（`video_backup_not_ready`）。
9. **失敗**：每輪最多備份 `VIDEO_BACKUP_PER_ROUND`（預設 2）支影片，最舊的先做；每輪最多
   送 10 筆「排入」或補送的回報。失敗的下一輪重試；連續失敗 3 次標記為 `failed`，寫入
   稽核紀錄，之後每 6 小時再試一次。工作根目錄的 `STOP` 檔也會停止備份。

## 跟 tidy 的關係

[`tidy.mjs`](../../tools/video/automation/tidy.mjs) 對每支已上傳的影片多一道保留條件：
**備份開啟時，只有 worker 這邊是 `done`、網站也回答 `done`、而且沒有新增或改過的檔案，
才可以清。** tidy 只清已上傳的影片，可以上架但還沒上傳的不受影響。 其他情況都保留：還沒備份、失敗、空間不足、缺檔、網站沒收到回報、網站連不上、
主機還沒設定 rclone。保留的原因寫在 tidy 的紀錄裡（`not in Google Drive yet: …`），
每輪也會印出有幾支因此保留。

備份關閉時，或網站還沒有這些 API（回 404）時，tidy 照原本的方式運作。

`prune_published_previews` 刪的是審核區的副本，原檔還在 `video_work`，所以這裡不用改。

## 主機設定

部署之後還要做一次（2026-10-22 已做完，以下是重做時的步驟，例如 token 失效或換帳號）。
前三步要站主本人在自己的電腦上做：主機沒有瀏覽器，Google 的同意只能在電腦上按。之後
影片由主機直接傳到雲端硬碟，不經過這台電腦。用戶端密鑰和 token 不要貼到任何對話裡，
也不要在 Claude app 的 Terminal 面板裡跑第 3 步（那裡的畫面代理讀得到），開一個獨立的
終端機視窗。

1. **Google Cloud**：用 YouTube 那個專案（`mokaair-studio-sync`）就好。它的同意畫面已經
   是正式版，Google Drive API 也已經啟用；換專案的話，這兩項要重做：
   - 啟用「Google Drive API」。
   - 「Google Auth Platform」→「目標對象」：使用者類型「外部」，發布狀態「實際運作中」
     （舊介面叫「OAuth 同意畫面」→「發布應用程式」）。留在「測試」的話，Google 發的
     refresh token 7 天就失效，備份每週都會斷。只有站主自己使用，不必送審。
   - 「用戶端」→「建立用戶端」→ 類型選「電腦版應用程式」，把用戶端 ID 和密鑰存在電腦上
     （關掉彈窗後密鑰不會再完整顯示）。不要用 YouTube 那組網頁應用程式用戶端。
     密鑰不小心外流了，就在同一個用戶端「新增密鑰」，再停用、刪除舊的。
2. **資料夾 ID**：在 drive.google.com 打開 `AI/備份`，網址
   `https://drive.google.com/drive/u/0/folders/<這一段>` 的最後一段就是 `root_folder_id`
   （目前是 `15Qgf5hiXpmOWR3hfgVnGWO5OESYSZAFH`）。它不是機密。
3. **授權並寫設定檔**：在電腦上安裝 rclone（`winget install Rclone.Rclone`，或
   <https://rclone.org/downloads/>；裝完要開新的終端機視窗才找得到 `rclone`），執行下面
   **一條**指令。它會開瀏覽器：用放 `AI/備份` 的那個帳號登入，「尚未驗證」按「進階」→
   「前往」，權限頁勾雲端硬碟，看到 Success! 即可；問到 Shared Drive 按 Enter（n）。
   token 直接寫進檔案，不必複製。

   ```bat
   rem cmd（提示字元是 C:\Users\...>）
   rclone config create videobackup drive client_id=<用戶端 ID> client_secret=<用戶端密鑰> scope=drive root_folder_id=<資料夾 ID> --config "%USERPROFILE%\rclone-videos.conf"
   ```

   PowerShell 把最後的 `"%USERPROFILE%\…"` 換成 `"$env:USERPROFILE\rclone-videos.conf"`。
   跑完先在電腦上確認 `rclone lsd videobackup: --config <那個檔>` 只列出 `AI/備份` 裡的
   資料夾。檔案的格式見
   [`ops/video/rclone-videos.conf.example`](../../ops/video/rclone-videos.conf.example)。
4. **放到主機**：把設定檔傳到主機（例如 `pscp -P 7788 rclone-videos.conf root@<主機>:/root/rclone.conf`），
   再以 root 執行。主機的 `install` 不接受數字 uid（`install: invalid user: '1001'`，容器的
   pwuser 在主機上沒有名字），所以用 `chown`：

   ```bash
   umask 077
   mkdir -p /etc/travel-scanner/rclone-videos
   chown 1001:1001 /etc/travel-scanner/rclone-videos && chmod 0750 /etc/travel-scanner/rclone-videos
   cp /root/rclone.conf /etc/travel-scanner/rclone-videos/rclone.conf
   chown 1001:1001 /etc/travel-scanner/rclone-videos/rclone.conf && chmod 0600 /etc/travel-scanner/rclone-videos/rclone.conf
   shred -u /root/rclone.conf   # 主機上別留第二份
   ```

   uid 1001 是 video-worker 容器裡的 pwuser。資料夾是掛進容器的，放好檔案不必重啟容器。
   放好之後刪掉電腦上的 `rclone-videos.conf`。
5. **確認 rclone 只看得到 `AI/備份`**：

   ```bash
   cd /root/travel_scanner
   docker compose -f docker-compose.prod.yml exec -T video-worker sh -c \
     'cp /etc/mokaair/rclone-videos/rclone.conf /tmp/rv.conf && export RCLONE_CONFIG=/tmp/rv.conf && rclone lsd videobackup: && rclone about videobackup:; rm -f /tmp/rv.conf'
   ```

   `lsd` 應該只列出 `AI/備份` 裡面的資料夾（一開始是空的）；看到雲端硬碟最上層的資料夾，
   就是 `root_folder_id` 填錯了。
6. **開啟**：後台「備份位置」卡確認「主機的 rclone 可以寫入 AI/備份」，勾選開關、儲存，
   按「測試連線」，等 5 分鐘按「重新讀取」，看到「上次測試成功」和剩餘空間。
7. **第一支**：之後每一輪會備份最舊的兩支。第一支完成後在電腦的
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
| 「主機沒有影片備份用的 rclone 設定」 | 第 4 步的檔案不在，或路徑打錯 |
| 「讀不到 …；檔案要讓容器的 pwuser 讀得到」 | 檔案或資料夾不是 uid 1001，重做第 4 步的 `chown`／`chmod` |
| `install: invalid user: '1001'` | 主機的 `install` 不認數字 uid；照第 4 步改用 `chown 1001:1001` |
| 設定檔放好了，卡片還是說沒有設定，測試也一直沒結果 | worker 的一輪沒跑到備份。看 `docker compose logs video-worker`：沒有任何 `backup:` 開頭的行，就是每一輪都在中途結束；2026-10-22 起一輪出錯也會備份，在那之前的版本要先修好讓那一輪出錯的原因 |
| 「路徑 … 不在主機鎖定的 AI/備份 之內」 | 後台路徑填到 `AI/備份` 外面了；要備份到別處，改 `root_folder_id` 和 compose 的 `VIDEO_BACKUP_LOCK_PATH` 再部署 |
| 測試失敗，`invalid_grant` | token 失效：多半是 OAuth 同意畫面還在「測試」，或站主撤銷了授權。改成正式版後重做第 3、4 步 |
| 「雲端空間不足」 | 剩餘空間少於這次要傳的量加 2 GB；清空間或升級方案，下一輪會自動再試 |
| 「缺少檔案」 | 網站列出缺哪些；多半是配音或字幕還沒做完，做完後下一輪會補 |

## 空間

站主的方案是 5 TiB：2026-10-22 第一次接上時用了 223 GiB（其中 14 GiB 是其他 Google
服務），剩 4.77 TiB。以下用文件裡的實測值估算每支的量：

| 種類 | 基本層級／支 |
| --- | --- |
| 純投影片 | 約 10 MB/分鐘 |
| 插畫版 | 約 40 MB/分鐘，最多約 70 MB/分鐘（13:22 的片是 535 MB） |
| 配音 | 每種語言約 1 MB/分鐘 |

完整層級要多算 clips 與 keyframes，第一次實際備份後把量到的數字補進這裡。
所有系列都設成完整、一支以 1 GB 算，5 TiB 也放得下四千多支，空間不是限制。

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
