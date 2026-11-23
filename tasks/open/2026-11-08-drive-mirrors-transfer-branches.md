---
id: 2026-11-08-drive-mirrors-transfer-branches
title: 雲端硬碟備份跟 transfer 分支一樣
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-08T07:15:12Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/branch-mirror.mjs
  - tools/video/automation/branch-mirror.test.mjs
  - tools/video/automation/cli.mjs
  - docs/videos/BACKUP.md
  - ops/video/Dockerfile
  - docker-compose.prod.yml
---

# 雲端硬碟備份跟 transfer 分支一樣

## Why

站主 2026-11-08：「備份到雲端的內容應該也要跟備份到分支的一樣」。

雲端 session 做的 AI 劇（種田 `zt`、祖媽 `tn`）每集推到 GitHub 的 `transfer/*` 分支：分集分支放重剪需要的加上可能還會用到的
（全部草稿、精修新舊版、提示詞、log、挑片檔、錄音、剪接表、該集配樂），共用分支放參考圖各輪、音效、系列配樂、小樣、scratchpad。
規則在 `docs/videos/drama/BACKUP-BRANCHES.md`。

主機的雲端硬碟備份（`tools/video/automation/backup.mjs`，`docs/videos/BACKUP.md`）只從後台**審核區**取檔，所以雲端硬碟只拿得到
上傳包，加上 `import --publish --clips … --edit …` 帶上去的片段、錄音、`cut/*.log`、配樂、剪接表、首格。差異逐項列在
`docs/videos/drama/GAPS-20261108.md` 的 C 節（C1–C19）與 `BACKUP-BRANCHES.md`〈雲端硬碟〉。

## Definition of done

- [x] （程式與測試，待部署後在主機上確認）一條 `transfer/<代號>-*` 分支推上新的一版之後，站主的雲端硬碟 `AI/備份/drama/<劇>/_分支/<分支名>/` 會出現跟分支最新一版
      逐檔相同的內容（切塊的 `.partNN` 已接回原檔），`rclone check` 為 0 差異。
- [x] 被新一版蓋掉或刪掉的檔不會消失，移到 `_舊版/<時間>/`。
- [ ] （另開票 `2026-11-08-backup-card-shows-branch-mirror`；這張只寫進 state JSON 與 log）後台 `/admin/videos?tab=settings#video-backup-settings` 的備份卡看得到每條分支最後鏡像的 commit、時間與核對結果。
- [x] 審核區那條路線照舊（上傳包、`--publish` 的片段與組片資料），不受影響。
- [ ] `docs/videos/BACKUP.md` 有一節〈AI 劇的分支鏡像〉（已做）；`docs/videos/drama/BACKUP-BRANCHES.md`〈雲端硬碟〉改成「已做」。

## Steps

- [x] 站主同意走這條路（2026-11-08「好，照你的建議做雲端備份」；資料夾用 `_分支/`）（花費是主機磁碟與 Drive 空間，不花 API 錢），並決定 Drive 上的資料夾名稱（`_分支/` 或別的）。
- [x] ~~主機放一把只讀的 deploy key~~ 不需要：repo 是公開的，worker 用 HTTPS 匿名抓；token 只是備案。前綴預設 `transfer/zt-`、`transfer/tn-`（`VIDEO_BRANCH_MIRROR_PREFIXES` 可改）。
- [x] `tools/video/automation/branch-mirror.mjs`：`git fetch` → 比對上次鏡像的 commit → 稀疏 checkout 或 `git archive` 解到暫存 →
      接回 `.partNN` → `rclone copy --checksum --backup-dir _舊版/<時間>` → `rclone check` → 回報網站。在 `cli.mjs` 每一輪備份之後呼叫。
- [ ] 後台備份卡加一列「分支」（這一步會動到 `apps/api` 與 `apps/web`，開工前把 scope 補上或另開票）。
- [x] 測試：用一個假的本機 bare repo 與 rclone 的 local 後端，涵蓋切塊接回、增量（同一 commit 不重做）、被刪的檔進 `_舊版`。
- [ ] 文件：`BACKUP.md` 一節（已做）、`BACKUP-BRANCHES.md`〈雲端硬碟〉與〈怎麼確認備份完整〉加「推完分支後，等後台顯示這條分支已鏡像」。

## How to verify

1. 在主機上對一條小分支（例如 `transfer/zt-live-pilot-20261107`）手動跑一次鏡像。
2. `rclone check <暫存> <drive>:AI/備份/drama/zhong-tian-qu-qi/_分支/zt-live-pilot-20261107` 為 0 差異。
3. 在分支上加一個 commit（改一個檔、刪一個檔），再跑：改的檔更新、舊版在 `_舊版/`，同一 commit 再跑一次不重複複製。
4. 後台備份卡顯示這條分支的 commit 與「已核對」。

## Notes

已知的限制（2026-11-08 缺口檢查查到的）：

- 審核區那條路改不出「一樣」：`clip_` 最多 120 支、組片資料（`build_`）最多 40 個且名稱最多 28 字、不能有子路徑、只收文字 json mp3 wav；
  每個檔 1.5 GB、審核區總共 20 GB；worker 每輪下載 40 個檔。種田真人第 1 集分支就有 768 個檔、976 MB，CG 版 1,014 個檔、1,585 MB；
  要放寬這些（缺口檢查的方案二）改動大，而且還是送不了系列共用檔與已被蓋掉的舊版整集，所以建議方案一。
- 系列共用的檔（參考圖各輪、音效、配樂）今天只能在掛著雲端硬碟（G:）的電腦跑 `tools/video/import/series-backup.mjs`，雲端 session 沒有這條路。
- 主機磁碟要有一條分支大小的暫存空間（目前最大約 1.8 GB），用完就清。
- 舊分支（帶日期、分批的 `zt-e0NN-media`、`zt-series-media-*` 等）要不要也鏡像，請站主決定；建議只鏡像 `BACKUP-BRANCHES.md` 統一後的名字。
- 這張票不改刪本機檔案的條件；鏡像做好後，要不要把「雲端硬碟核對完成」加進條件由站主決定。
- 順手統一 `docs/videos/BACKUP.md` 裡系列共用檔的雲端資料夾名：第 297 行附近寫 `drama/<劇>/_series`，〈資料夾排法〉寫 `_共用/`（缺口檢查 X10）。

### 2026-11-08 實作（claude-opus-zt-session，分支 `claude/drive-mirror-transfer`）

- 認領：`npm run tasks -- claim` 被拒，因為 scope 跟五張早已過期（> 24 小時）的 in-progress 票重疊
  （`2026-10-23-video-backup-when-ready-to-upload`、`2026-10-24-bug-1-4`、`2026-10-29-daily-brief-on-the-host-worker`、
  `2026-11-02-video-backup-shorts-sent-by-hand`、`2026-11-03-admin-upload-zip-fails-to-download`，都是整個資料夾或 `BACKUP.md`）。
  `--force` 這次 session 不能用，所以 owner 欄沒填；要正式認領請有權限的人跑 `claim --force`。scope 已縮到實際改的檔，
  沒有改 `backup.mjs`。
- 做法：`git ls-remote` 比對 → 只抓那一個 commit（`--depth 1`）到暫存 bare repo → `read-tree` + `checkout-index`
  （`core.symlinks=false`）寫出檔案 → 刪 repo → 接回切塊（有 `X.SPLIT` 就驗 sha256）→ `rclone sync --checksum --backup-dir _舊版/<時間>`
  （排除 `_舊版`，所以不碰舊版；分支刪掉的檔也是「移」不是刪）→ `rclone check` 雙向 → 0 差異才記錄。
- 用 `sync` 而不是 `copy`：只有 `sync --backup-dir` 能把分支刪掉的檔從資料夾移到 `_舊版`；分支一個檔都沒有時不 sync。
- 開關：程式預設關，`docker-compose.prod.yml` 給 video-worker 設 `VIDEO_BRANCH_MIRROR: "on"`，所以部署後就開；改成 `"off"` 就關。
  不在程式裡預設開，是因為現有的 cli／backup 測試沒有設這個變數，預設開會讓它們去連 GitHub。
- 每輪上限：1 條分支、2 GB、工作磁碟至少剩 5 GB；第一次要傳完現有的幾十條分支，會分散在很多輪。
- 目的地的根跟影片備份一樣，用網站 config 的 `remote_prefix`；影片備份關著時鏡像不跑。
- 映像加了 `git`（`ops/video/Dockerfile`）。
- 一輪走錯誤路徑結束（例如每月草稿上限的結束碼 3）時不跑鏡像：`host-verify.sh` 的 `video_log_classify` 把原因與結束碼之間不在白名單的行算成錯誤，
  鏡像的行會讓自動部署的檢查 FAIL。正常結束的輪與兩個單位之間照跑。若之後想在那條路也跑，要先把 `branch mirror:` 的成功行加進
  `host-verify.sh` 的 `benign`（自動部署用的是 `/opt/travel-scanner-autodeploy/` 安裝的那一份，要重跑 `ops/autodeploy/install.sh`）。
- 還沒做：`docs/videos/drama/BACKUP-BRANCHES.md`（在分支 `claude/drama-branch-backup`，還沒進 main）〈雲端硬碟〉改成「已做」
  與〈怎麼確認備份完整〉加一句；那份合併後補。舊分支（帶日期的 `zt-e0NN-media` 等）也在預設前綴裡，站主若只要統一後的名字，
  把前綴改成 `transfer/zt-live-,transfer/zt-cg-,transfer/zt-shared,transfer/tn-`。

