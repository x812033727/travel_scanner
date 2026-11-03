# 影片的雲端硬碟備份

影片可以上架（或已經上 YouTube）時，把它的檔案依系列複製到站主的 Google 雲端硬碟。雲端的檔案經過核對、
網站也確認沒有缺檔之後，worker 才可以刪掉主機上的檔案。程式在
`apps/api/app/video_backup/`（設定與狀態）、`tools/video/automation/backup.mjs`（複製）、
`apps/web/components/admin-video-backup.tsx`（後台卡片），2026-10-19 隨 #1595 合併。
要真的開始備份，還要做完下面的〈主機設定〉。

## 為什麼要做

- 成片只存在 VPS。`video_work/<slug>/` 由 [`tidy.mjs`](../../tools/video/automation/tidy.mjs)
  在上傳 7 天後清掉 `final.mp4`、配音、clips、keyframes；審核區的 mp4 也由
  `prune_published_previews` 在 7 天後刪除（2026-11-03 起要等備份完成，見〈跟 tidy 的關係〉）。
  YouTube 上的版本是轉碼過的，不能當原檔。

站主 2026-11-03 定的三條規則（之前沒備份的不追；票 `2026-11-03-*` 六張）：
1. 上架前，每支影片在 VPS 上都要有一份完整的檔案，不論在哪裡做的，除非站主放棄並刪除它。
2. 站主刪除影片時，VPS 上那支的檔案整支刪掉。
3. 上架後先備份到雲端硬碟、確認完整，才把 VPS 上那支整支刪掉：上架、備份核對完整、所有勾選的
   語言都已核准或略過，三樣齊了才刪；之後要補做就從雲端還原。
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
  每一輪都在跑到備份之前就結束了。一輪跑超過 10 分鐘（`BACKUP_EVERY_MS`，`tools/video/automation/cli.mjs`）時，
  第一條 lane 在兩個單位之間也會跑一次備份（含匯入影片的上架包下載），tidy 仍只在整輪結束時跑：
  每日快報的八種語言一輪可以跑好幾個小時，2026-11-01 四集匯入的種田因此等了一整個早上。
  API 容器不放 Drive 的權杖。
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
      （完整層級另外有）clips/ keyframes/ characters/ recordings/ timeline.json narration.wav
                       （匯入的影片：clips/ 是 import --publish 送的每鏡片段，recordings/ 是逐句原始錄音）
                       dubs/未進上傳包/<語言>.m4a、captions/未進上傳包/<語言>.srt、
                       上傳包缺的 thumbnails/<語言>.jpg
  Shorts/<shorts_series 或 shorts_line>/<slug>/…
  其他/<slug>/…
```

**系列鍵**依序取第一個有值的：Shorts 一律放在 `Shorts/<shorts_series 或 shorts_line>/` →
`series_slug` → 匯入的劇（分類 `drama`、沒有 `series_slug`、slug 是 `<劇>-e033`、`<劇>-e001-005`、`-v2` 這種）的 `<劇>` →
slug 開頭（`curio-`、`ai-term-`、`sothatswhy-`、`story-`）→ `category`。都沒有就放「其他」。

匯入的劇放在分類資料夾底下自己的資料夾：`drama/<劇>/<集>/`，例如 `drama/zhong-tian-qu-qi/zhong-tian-qu-qi-e033/`
（站主 2026-11-01：不同劇要有不同資料夾）。在那之前備份在 `drama/<集>/` 的，網站在 worker 設定裡多給一個
`moved_from`，worker 在 Drive 裡把舊資料夾整個搬過去（`rclone moveto`，伺服器端搬移、不重傳），再回報新資料夾；
網站之後就記新資料夾。搬不動的那一輪不備份那支影片，免得在新位置再傳一份。

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
影片被分到兩個資料夾。唯一的例外是上面匯入的劇從 `drama/<集>/` 搬到 `drama/<劇>/<集>/` 那一次。

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
   續作或重剪，2026-10-23 起），或是從審核區取回的匯入上傳包（`review-package.json`，見
   〈匯入的影片〉）；都沒有的資料夾不排入。
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

## 匯入的影片與手動推送的影片

雲端 session 做的影片（例如第 31 集起在 Colab 做的種田娶妻打天下）用
`node tools/video/cli.mjs import --from DIR` 送上站台：成片、字幕、配音、縮圖和 `metadata.json`
進的是 API 的**審核區**（`video_reviews` volume），不是 worker 的 `video_work`。2026-10-31 之前
備份只看 `video_work/<slug>/`，所以匯入的影片從來沒有被備份過（主機上沒有它的工作資料夾，
第 1 步直接略過），只在審核區裡，而審核區的 mp4 在上 YouTube 7 天後就刪掉。

審核區連整包都不留的舊片（2026-10-31 的種田娶妻 e001-005、e006-010），主機上沒有檔案可以備份：
只回報網站一次（後台顯示失敗與原因），不再每六小時重試；之後重送上架包才會再排入備份。

現在的做法（`tasks/open/2026-10-31-zhong-tian-clip-backup.md`）：

1. **片段跟著上傳包走**：`import --publish` 除了上傳包，也把每鏡的 1080p 片段送進審核區：
   `<from>/clips/` 或 `--clips DIR` 裡每一個 `<鏡>.mp4`，角色叫 `clip_<鏡>`（例如
   `clip_s01-t1`）。網站只在上架確認（publish）這一關收 `clip_` 檔，一關最多 120 個，不算在
   原本每關 48 個檔案的上限裡（`apps/api/app/video_reviews/schemas.py` `MAX_CLIP_FILES`）；
   每個檔照常分段上傳、在最後一段核對 sha256，大小上限也照常（`video_review_max_file_bytes`）。
   片段不寫進 `metadata.json`，所以上架確認還在等站主時重送一次 `--publish`，就把片段補進同一筆
   審核；**已經核准**的那一份不會再收檔，工具會說片段沒送。YouTube 上傳、手動上傳包和後台頁面
   都不讀 `clip_` 檔。
2. **worker 先取回來**：網站列給 worker 的影片裡，匯入的長片（核准的上架確認帶 `imported`）、
   手動送上來的 Shorts（帶 `hand_pushed`，2026-11-02 起），以及在別處做好、用 `review-push` 送上來的長片
   （工作資料夾沒有 `auto.json` 時 `review-push` 每一關都帶 `hand_pushed`，2026-11-03 起：雲端 session 做的
   奇聞檔案局在這之前都沒備份到）多一個 `review_package`（審核 id 與 `metadata.json` 的 sha256），
   有核准的語言批次時再加上最新那一批（`languages_review_id`、`languages_sha256`）。worker 自己做的影片
   兩個標記都沒有，檔案本來就在 video_work。worker 每一輪在備份之前用
   影片工具權杖從審核區下載這一包（跟 `review-files` 同一條路由），逐檔比對 sha256 與大小，排成
   `package` 的樣子：`upload/final.mp4`、`upload/metadata.json`、`upload/thumbnail.<副檔名>`、
   `upload/captions/<語言>.srt`、`upload/dubs/<語言>.<副檔名>`、從 `metadata.json` 寫出
   `upload/description.<語言>.txt`，片段放 `clips/<鏡>.mp4`。語言批次（上架後才核准的配音、字幕、說明、
   各語縮圖）接在上傳包後面排，同一個位置以批次的為準；檢查沒過、站主可以手動上傳的配音
   （`dub_unchecked_<語言>`）放 `dubs/<語言>.<副檔名>`，完整層級照 `dubs/未進上傳包/` 備份。網站核准新的
   一批時，下一輪只抓新的檔，上一批單獨放的檔從主機移走（雲端留著）。`review-push` 的字幕是
   `text/plain`，一樣當 `.srt` 放。紀錄寫在
   `video_work/<slug>/review-package.json`；取到一半的不備份，下一輪接著取。每輪最多下載 40 個
   檔（審核區每個權杖每小時 600 個）。程式在
   [`review-package.mjs`](../../tools/video/automation/review-package.mjs)。
3. **然後照一般流程備份**：完整層級把 `clips/` 一起複製到 `AI/備份/<系列>/<集>/clips/`，
   `rclone check` 核對，網站的回報會數到片段的數量（`contents.clips`）。
4. **逐句原始錄音也跟著走**（2026-11-01，票 `2026-11-01-zhong-tian-the-line-recordings-travel`）：`import --publish` 把那一集工作資料夾的
   `audio/`（zh-TW）與 `audio-<語言>/`（各配音，連同每句的 `.json`）打包成每種語言一個 wav（每句的取樣接在一起，可以直接播放）加
   `manifest.json`（每句的位置、檔頭、雜湊與 `.json`），角色 `recording_<語言>` 與 `recordings_manifest`，都是網站本來就收的類型。
   來源是 `--recordings DIR`，沒給就用 `--clips` 那個資料夾的上一層。metadata.json 記下 manifest 的雜湊（`recordings_sha256`），
   所以補送錄音是一筆新的上架確認，要站主再核准一次。worker 放到 `recordings/`，完整層級複製到 `AI/備份/<系列>/<集>/recordings/`。
   要改某一句時，把那個資料夾抓回來，`node tools/video/import/recordings.mjs unpack <recordings 資料夾> <那集的工作資料夾>`
   就還原成原本的每一句檔，一個位元組都不差。

5. **`review-push` 也帶完整層級**（2026-11-03，票 `2026-11-03-review-push-sends-the-full-backup`）：在別處做的影片
   （工作資料夾沒有 `auto.json`）`review-push --gate publish` 除了上傳包，也送完整層級的其他檔
   （[`full-tier.mjs`](../../tools/video/review/full-tier.mjs)）：每張分鏡圖 `kf_<名稱>`（一集奇聞檔案局約 230–320 張）、
   `keyframes_manifest`、`full_narration`（narration.wav）、`full_timeline`（timeline.json）、`clips/` 的 `clip_<鏡>`，
   以及照 `import` 的方式打包的逐句錄音（`recording_<語言>`、`recordings_manifest`，工作資料夾的 `audio/`、`audio-<語言>/`）。
   網站把這些另外計數：`kf_` 最多 400 個、`clip_` 120 個、其他 24 個，都不占每關 48 個的上限；`kf_` 與 `clip_` 只收在
   上架確認這一關（`apps/api/app/video_reviews/clips.py`）。名稱放不進角色（字母、數字、`-`、`_`，最多 37 個字）的檔不送，
   原因寫在 payload 的 `full_tier.problems`。worker 取回時放回原位：`keyframes/<名稱>.<副檔名>`、`keyframes/manifest.json`、
   `narration.wav`、`timeline.json`。一集三百多個檔，worker 每輪抓 40 個，約八、九輪抓完；抓完之前不備份。
   worker 自己做的影片不送這些（檔案本來就在 video_work）。審核區只在備份完成後刪 mp4，這些圖與音檔目前會一直留在審核區
   （一集約 180 MB），整支清除是 `2026-11-03-purge-a-video-from-the-host` 的事。

只動自己放的東西：有 `auto.json` 的（worker 做的）和沒有 `review-package.json` 卻已經存在的
資料夾（手動做的）一律不碰；換版後新的上架確認核准時，只替換上一包放的檔案，舊檔照第 4 步留在
雲端 `_舊版/`。審核區已經刪掉的檔案（上 YouTube 7 天後的 mp4）記成取不到，其他照備份，網站列出
缺什麼。tidy 只清有 `auto.json` 的影片，所以這些資料夾不會被清，留在主機上（每集約成片加 300 MB
片段）。

## worker 自己做的 Shorts

worker 的實測與精華 Shorts（`lab`、`cut` 兩條線，[`automation/shorts.mjs`](../../tools/video/automation/shorts.mjs)）不在
`video_work/<slug>/`，而在 `video_work/_shorts/<slug>/`：`lab.json` 記著目前那一版的 build 資料夾（`build`），每次重建都是旁邊的
新資料夾。2026-11-03 之前備份只讀 `video_work/<slug>/`，這些 Shorts 從來沒備份過，網站一直顯示「還沒排入」。
現在 `backup.mjs` 的 `videoDir` 在 `video_work/<slug>/` 不存在時改看 `_shorts/<slug>/lab.json` 的 `build`：那個資料夾必須在
`_shorts/<slug>/` 裡面、而且有 `upload/final.mp4`，才拿它當這支 Short 的工作資料夾，照一般流程備份它的上傳包
（`final.mp4`、`zh-TW.srt`、`cover.png`、`titles.json`）。`backup-state.json`、`backup.json` 也寫在那個 build 裡：重建出新的一版
就是新的成片，會再備份一次，舊版照第 4 步留在雲端 `_舊版/`。tidy 跳過 `_` 開頭的資料夾，這些 Shorts 的清除由
`2026-11-03-purge-a-video-from-the-host` 處理（票 `2026-11-03-back-up-the-worker-s-own`）。

## 跟 tidy 的關係

[`tidy.mjs`](../../tools/video/automation/tidy.mjs) 對每支已上傳的影片多一道保留條件：
**備份開啟時，只有 worker 這邊是 `done`、網站也回答 `done`、而且沒有新增或改過的檔案，
才可以清。** tidy 只清已上傳的影片，可以上架但還沒上傳的不受影響。 其他情況都保留：還沒備份、失敗、空間不足、缺檔、網站沒收到回報、網站連不上、
主機還沒設定 rclone。保留的原因寫在 tidy 的紀錄裡（`not in Google Drive yet: …`），
每輪也會印出有幾支因此保留。

**2026-11-03 起（站主的規則，票 `2026-11-03-purge-a-video-from-the-host`）**：已上 YouTube 的影片，三樣齊了就整支離開主機，
不再等 7 天：(1) 有 YouTube ID；(2) 備份 worker 與網站都是 `done`、沒有新增或改過的檔案；(3) 語言已決定、沒有等站主的審核、
沒有再做一次的配音請求，每個勾選的語言部分都做好或略過，配音要「已上傳」（站主核准語言批次＝已放上 Studio）或略過。
這時 tidy 把 `video_work/<slug>/` 裡**全部**刪掉，只留 `auto.json`、`backup-state.json`、`backup.json`
（匯入或手動資料夾另有 `review-package.json`、`tidied.json`），幾 KB，讓 worker 與備份知道這支已經做完、已經在雲端，
不會當成新影片或重新排備份；`auto.json` 記下 `tidied.purged: true`。沒有 `auto.json` 的資料夾（`import`、`review-push`
取回的、手動做的）同樣處理，條件看網站那一列。
- **一律不刪**：備份關閉、系列層級設成「關閉」、這一輪讀不到備份狀態、配額不足、缺檔。以前備份關閉時
  tidy 照舊刪，現在主機保留。
- **完整層級多備份這些**（刪了就只剩雲端）：逐句旁白 `audio/`、各語配音的逐句檔（雲端在 `dub-lines/<語言>/`）、翻譯工作表
  `i18n/`、`approvals.json`、`languages.json`。`segments/`、`build/`、`frames/`、審核預覽可以重算，不備份。
- **審核區同一條規則**：`prune_published_previews` 對符合上面三樣的影片把審核區裡這支的**所有**檔案刪掉（`_done_with`），
  不只 mp4，也不等 7 天；資料庫的審核紀錄保留。
- 之後要補語言、重試配音、剪 Shorts：先從雲端還原（票 `2026-11-03-restore-a-purged-video-from-drive`）。
- 放棄的影片照舊：放棄後 7 天刪大檔。
- **刪除影片（站主在 /admin/videos 放棄後再刪除）**：網站刪掉資料庫列、審核區與素材區；worker 每輪讀備份設定時多拿到
  `deleted`（近 60 天刪除、而且這個 slug 沒有被新影片用回去的），tidy 把 `video_work/<slug>/` 與 `video_work/_shorts/<slug>/`
  **整個**刪掉，不管備份開關、不等雲端（站主的規則：刪除就整支刪）。只刪工作根目錄底下真的資料夾，連結不跟、不刪工作根目錄或
  repo。雲端硬碟上已備份的那份不動。從它剪出的 Shorts 是另外的影片，要各自刪除（票 `2026-11-03-deleting-a-dropped-video-removes-its`）。
- `_shorts/` 底下 worker 自己做的 Shorts 還不在這條規則裡（tidy 跳過 `_` 開頭的資料夾），之後另開票。
- 沒有傳備份狀態給 tidy 的呼叫（只有測試），或網站還沒有備份的 API（回 404，正式站不會）時照舊：上架 7 天後刪大檔。

`prune_published_previews` 刪審核區的 mp4 也要等備份：2026-11-03 起，除了原本的「上架確認核准滿 7 天、
有 YouTube ID、設了公開時間的話也過了 7 天」，還要網站上這支的備份紀錄是 `done`；備份關閉、還沒備份、
`partial`、`failed` 都不刪。在別處做的影片，審核區的 mp4 在 worker 取回之前是主機上唯一的一份，
以前核准後拖過 7 天才上架的片，一上架 mp4 就被刪，worker 只能記成取不到。代價是備份關著時審核區的
mp4 不會自己清，檔案區（預設 20 GB）要靠備份開著才會回收。

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
| 匯入的影片一直「還沒排入」，`video_work/<slug>/` 也還不存在 | 上架包只在跑備份時下載。看 `docker compose logs video-worker` 最近有沒有 `backup:` 開頭的行，和 `ps` 裡那一輪 `cli.mjs auto` 跑了多久；一輪在兩個單位之間每 10 分鐘會備份一次，但一個單位本身（例如一種語言的配音，約 20 分鐘）跑完之前不會插進去 |
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

**從主機還原（2026-11-03，票 `2026-11-03-restore-a-purged-video-from-drive`）**：上架、備份完整、語言做完之後主機會把影片整支清掉
（〈跟 tidy 的關係〉）。之後要補語言、重做配音、從長片剪 Shorts，先在 video-worker 容器裡把它拉回來：

```bash
docker compose -f docker-compose.prod.yml exec -T video-worker node tools/video/cli.mjs restore --slug <slug> --dry-run
docker compose -f docker-compose.prod.yml exec -T video-worker node tools/video/cli.mjs restore --slug <slug>
```

[`restore.mjs`](../../tools/video/automation/restore.mjs) 讀雲端那一集的 `backup.json`（雲端沒有就用主機留下的那份），
`rclone copy` 到 `video_work/_restore-stage/<slug>/`（不含 `_舊版/`），逐檔比對 sha256 與大小，對得上的才放回原位
（`workPathOf`，planFiles 的反向：上傳包回 `upload/`、`descriptions/<l>.txt` 回 `upload/description.<l>.txt`、`dub-lines/<l>/`
回 `dubs/<l>/audio/`、`dubs/未進上傳包/` 回 `dubs/`、`captions/未進上傳包/` 回 `captions/`，其餘照原路徑）。worker 自己的影片也把
`upload/final.mp4` 連回根目錄的 `final.mp4`。對不上的檔不放，列出來、結束碼非 0。完成後 `auto.json` 拿掉 `tidied_at`、寫上
`restored_at`（手動資料夾寫在 `tidied.json`），tidy 保留 14 天（`RESTORE_HOLD_DAYS`）讓後續工作做完，之後照一般規則再清。
雲端上的檔案不會被改動。目前要手動下這個指令：worker 遇到已清掉的影片時，新勾的語言仍會回報「工作檔已清」，不會自己還原。

**手動還原**（不在主機上）：找到 `AI/備份/<系列>/<集>/backup.json`，按 `files` 清單下載，比對 sha256。
要重新上架時，`final.mp4`、`captions/`、`descriptions/`、`dubs/` 就是一份完整的手動上傳包
（對應 [MANUAL-UPLOAD.md](MANUAL-UPLOAD.md)）。
