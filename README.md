# sothatswhy-p15-salty-sea 備份

站主 2026-11-07：每過一關就把整個工作目錄（重製要用的所有檔案）加上 upload/ 裡全部上傳的檔案推到這個分支，超過 90 MB 切塊，逐檔核對雜湊。

- `workdir/` 是 `/root/mokaair-work/videos/sothatswhy-p15-salty-sea/` 的副本（不含 LEASE）。
- `music/` 是系列配樂床與它的付費原檔。
- `MANIFEST.tsv`：每個檔案的原始大小、sha256 與切塊數；切塊的檔案是 `<name>.part00`、`.part01`…，還原時依序 `cat` 接回再核對 sha256。
- 稿子與 `build_scenes.py` 在工作分支的 `docs/videos/sothatswhy-p15-salty-sea/`。

## 紀錄

- 2026-11-07 16:56 UTC：開工：系列配樂床（從 P02 付費原檔重做）與原檔（2 個檔案）
