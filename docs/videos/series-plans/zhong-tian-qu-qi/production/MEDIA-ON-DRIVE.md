# 種田娶妻打天下（真人版）的圖片與音檔在 Google Drive

2026-11-25 起主幹改成路線 B（#2224）：影片的二進位媒體不進 GitHub，`tools/video-drive-boundary.test.mjs`
限制 `docs/videos/` 追蹤的二進位檔只能少不能多。這個系列在 PR #2149（第 31–39 集真人版）累積的 467 個圖片與音檔
（參考圖 `assets/refs-live/`、`refs-dh/`、`angles/`、Qwen 挑選圖、試鏡表、配樂）已移到 Drive，路徑跟 repo 一模一樣：

`videobackup:AI劇/種田娶妻打天下（真人版）/_共用/製作檔/repo-media/<repo 裡的路徑>`

搬移時 `rclone check --one-way` 467 個相符、0 差異；清單在 `MEDIA-ON-DRIVE.list`。`.gitignore` 擋住本系列 `production/` 底下的
png／jpg／jpeg／webp／wav／mp3／mp4，製作腳本照舊讀本機路徑。

## 新的 session 開工前先拉回來

```bash
rclone copy "videobackup:AI劇/種田娶妻打天下（真人版）/_共用/製作檔/repo-media/docs" docs --checksum
```

（只拉不刪；rclone 的 videobackup 遠端設定見 `docs/videos/AI-DRAMA-DRIVE.md`。）

## 新做的參考圖

畫好或裁好的新圖照舊放在 `production/assets/refs-live/` 等原位（git 會忽略），README 照舊記種子與 md5，
然後馬上補進 Drive：

```bash
rclone copy docs/videos/series-plans/zhong-tian-qu-qi/production "videobackup:AI劇/種田娶妻打天下（真人版）/_共用/製作檔/repo-media/docs/videos/series-plans/zhong-tian-qu-qi/production" --checksum --include "*.{png,jpg,jpeg,webp,wav,mp3,mp4}"
```
