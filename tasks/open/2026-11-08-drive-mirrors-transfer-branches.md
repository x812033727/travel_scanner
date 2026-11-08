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
  - tools/video/automation
  - docs/videos/BACKUP.md
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

- [ ] 一條 `transfer/<代號>-*` 分支推上新的一版之後，站主的雲端硬碟 `AI/備份/drama/<劇>/_分支/<分支名>/` 會出現跟分支最新一版
      逐檔相同的內容（切塊的 `.partNN` 已接回原檔），`rclone check` 為 0 差異。
- [ ] 被新一版蓋掉或刪掉的檔不會消失，移到 `_舊版/<時間>/`。
- [ ] 後台 `/admin/videos?tab=settings#video-backup-settings` 的備份卡看得到每條分支最後鏡像的 commit、時間與核對結果。
- [ ] 審核區那條路線照舊（上傳包、`--publish` 的片段與組片資料），不受影響。
- [ ] `docs/videos/BACKUP.md` 有一節〈AI 劇的分支鏡像〉，`docs/videos/drama/BACKUP-BRANCHES.md`〈雲端硬碟〉改成「已做」。

## Steps

- [ ] 站主同意走這條路（花費是主機磁碟與 Drive 空間，不花 API 錢），並決定 Drive 上的資料夾名稱（`_分支/` 或別的）。
- [ ] 主機放一把只讀的 deploy key（compose 掛載，不進 repo）；決定要鏡像哪些前綴（`transfer/zt-*`、`transfer/tn-*`）。
- [ ] `tools/video/automation/branch-mirror.mjs`：`git fetch` → 比對上次鏡像的 commit → 稀疏 checkout 或 `git archive` 解到暫存 →
      接回 `.partNN` → `rclone copy --checksum --backup-dir _舊版/<時間>` → `rclone check` → 回報網站。在 `cli.mjs` 每一輪備份之後呼叫。
- [ ] 後台備份卡加一列「分支」（這一步會動到 `apps/api` 與 `apps/web`，開工前把 scope 補上或另開票）。
- [ ] 測試：用一個假的本機 bare repo 與 rclone 的 local 後端，涵蓋切塊接回、增量（同一 commit 不重做）、被刪的檔進 `_舊版`。
- [ ] 文件：`BACKUP.md` 一節、`BACKUP-BRANCHES.md`〈雲端硬碟〉與〈怎麼確認備份完整〉加「推完分支後，等後台顯示這條分支已鏡像」。

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
