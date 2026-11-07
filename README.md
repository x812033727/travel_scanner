# 原來如此事務所 P02／P05 工作目錄備份（2026-11-07）

站主 2026-11-07：「如果都完成也都有推到後台就開分支備份，確認備份完就可以刪除」。

`workdirs/<slug>/` 是 `/root/mokaair-work/videos/<slug>/` 的副本，不含：
- `final.mp4`、`upload/final.mp4`（已上架 YouTube：P02 `rmQ9yD0I6tI`、P05 `BirHcIAlfz4`）
- `*.wav`、`audio/`、`dubs/`（旁白與八語配音，已上傳到 YouTube Studio；可用 `tts`／`dub` 從快取以外重錄）
- 超過 40 MB 的檔案、`LEASE*`

還原：把 `workdirs/<slug>` 複製回 `/root/mokaair-work/videos/`，再照需要重跑 `tts`、`render`、`assemble`、`dub`。
集數的原始檔（稿子、`video.json`、`i18n/`）在 main 的 `docs/videos/<slug>/`。
