# 原來如此事務所 P07／P14 工作目錄備份（2026-11-07）

站主 2026-11-07：「如果都完成也都有推到後台就開分支備份，確認備份完就可以刪除」。兩集的成片、上架、語言關卡都已核准，配音已上到 YouTube Studio。

`workdirs/<slug>/` 是 `/root/mokaair-work/videos/<slug>/` 的副本，不含 `*.mp4`、`*.wav`、`audio/`、`dubs/`、超過 40 MB 的檔案與 `LEASE*`（成片與八語配音在 YouTube）。
還原：複製回 `/root/mokaair-work/videos/`，照需要重跑 `tts`、`render`、`assemble`、`dub`。集數原始檔在 main 的 `docs/videos/<slug>/`。
