# W03 每句配音錄音（八語）

`<locale>/<line>.flac` 是工作資料夾 `dubs/<locale>/audio/<line>.wav` 的無損 FLAC（`<line>.x<tempo>` 是加速過的那一句），`cache.json` 原樣保留。
重製時還原：`ffmpeg -i <line>.flac <line>.wav`，放回 `dubs/<locale>/audio/`，dub 工具就會沿用，不重錄。
中文旁白的逐句錄音在第一次刪除工作資料夾時已遺失，整軌 `narration.wav` 在上一層。
