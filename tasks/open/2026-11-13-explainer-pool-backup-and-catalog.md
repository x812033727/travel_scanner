---
id: 2026-11-13-explainer-pool-backup-and-catalog
title: 奇聞與原來如此：題庫備份雲端、備份紀錄與各集總表
status: in-progress
priority: P2
area: docs
owner: claude-opus-stw-round27
claimed_at: 2026-11-13T00:46:30Z
created_at: 2026-11-13T00:45:44Z
completed_at:
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/AI-DRAMA-DRIVE.md
---

# 奇聞與原來如此：題庫備份雲端、備份紀錄與各集總表

## Why

站主 2026-11-13：「將這些題庫備份到雲端」「應該要有一個記錄將這些都記錄在上面」「應該要有一個總表記錄目前製作的集數
放的位置、上架的 id、是否用新版做的、語音用哪一種 minimax 還是 Gemini 等等的資訊，之後如果要重置也比較知道要怎麼查以前的資訊」。
題庫的研究原稿只在做研究的 session 的 scratchpad，session 收掉就沒了；各集的位置、YouTube ID、版本與聲音分散在雲端的
backup.json、metadata.json 與 repo 的 video.json，沒有一張表。

## Definition of done

- [x] 兩個題庫的快照在雲端硬碟，逐檔核對 0 差異。
- [ ] 這個 session 的題庫研究原稿在雲端硬碟，逐檔核對 0 差異。
- [x] `docs/videos/ai-drama-drive/BACKUP-LOG.md` 記下每一次傳了什麼、在哪裡、核對結果。
- [x] `docs/videos/explainer-series/CATALOG.md`／`catalog.json`：每集的雲端位置、slug、YouTube ID、版本、畫風、縮圖版型、旁白與外語配音聲音、片頭片尾、repo 文件，可用 `catalog.py` 重產。
- [ ] 總表與紀錄的唯讀副本在雲端 `AI劇/<系列>/_總表/`。

## How to verify

`python3 docs/videos/ai-drama-drive/catalog.py`（需要 rclone 與 RCLONE_CONFIG_VIDEOBACKUP_*）重產後 diff 只差產生時間；
`docs/videos/ai-drama-drive/todrive.sh --check <來源> <雲端位置>` 對 BACKUP-LOG 每一列都是 0。

## Notes

- 外語配音的聲音雲端沒有直接記：用 dubs/ 檔案日期推，2026-11-12 起標「MiniMax（推定）」。要確定得看主機配音 timeline.json 的 voice_provider，可另開票讓 backup.json 記上聲音。
- 2026-11 主機開始寫 backup.json 之前上傳的舊版（H01、H02、H03、U02、L08、H12、M09 與 10-12 重剪版），YouTube ID 只在 repo 交付紀錄，catalog.py 的 IDS_FROM_DOCS 列了出處。後台才是正本。
- 原來如此同一集可能有兩個雲端資料夾（第007集/ 上架包、P07/ 製作檔），總表合成一列。
- 奇聞 S23–S40 的 -v2 有上架包但 backup.json 沒有 YouTube ID（metadata 是 private），可能還沒上傳或後台沒回寫。
