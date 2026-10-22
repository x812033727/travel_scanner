# S38 R8ad｜PF021 原圖退件後單景提示詞窄修

2026-10-22 UTC。**作者提案；待非作者固定史料與書面畫面紙審。本輪修訂後沒有付費媒體呼叫。**PF021 首張[機器 FAIL、原圖人工 REJECT](verify-103-r8ad-pf021-seed1-machine-human-reject.md)：兩名童貌人物跑離左後方的船，右側為不合 1666 年倫敦的東亞式翹瓦簷。退件已從 active 圖單隔離；13 張舊 KEEP 完整條目和所選實檔 SHA 不變。

只改 `scenes[20].data.prompt`（PF021）。新提示詞把畫面定為倫敦泰晤士河登船處，**一名灰髮、中年、有成人面部線條與寬肩的居民**穿羊毛 doublet 和及膝褲，自畫面左側冒煙的樸素磚屋跑向畫面右側靠岸的低木船；前腳已踏上登船板，一手伸向船舷。用左屋→右船、腳上板和手伸船三個畫面錨點糾正先前方向顛倒；只要一個主角，避免模型另畫童貌群像。樸素磚牆與陰天也縮小翹瓦簷風險。年齡、衣服、船型及登船板均是年代合理的插畫示意，沒有當成日記對個別住戶的識別細節。

固定 [1666-09-02 Pepys 日記 L65818–65823](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65818-L65823)寫人們一直等到火碰屋才 `running into boats`；旁白「佩皮斯見有些住戶等火貼近門口，才往船上跑。」與 `claims.md` D2a 未改。提示詞把奔向船、快登船畫得明確，但沒有指認此人，也不新增到達安全處的結局。

[單葉可逆差分](verify-104-r8ad-pf021-prompt-structured-diff.json)僅 `scenes[20].data.prompt`；`video.json` SHA-256 `d8d169a010a7ffce93b3aec580e7c9580dc3a5393ffbe0bbc5909b72e8559688` → `c531301285fd9cbc3730f40c9c4a1d37936f00f2c7a0bfb98bf0c1ba97a7e121`，反填舊 prompt 可逐位元復原。`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 均不變。新視覺雜湊為 `03d5ee8d1b78b924`；修訂後 `lint --json` **0 errors／0 warnings**，單景 live dry-run 在 `NODE_USE_ENV_PROXY=1` 下通過，prompt **366／1068 字**、MiniMax `image-01` ready，但這不是付費圖驗收。

私人 active manifest SHA `c8c9c4042fd7568a222bb26056e48d3775b66b18dd55af24dbae00a2ffc1a0da` 仍綁**舊** R8ac `visual_hash=799a46f1c5720fec`、13 張 KEEP；不能直接用於新影片稿付費呼叫。ledger SHA `d64076ef7a4ee30f98e242e28102139fdff756c722c94d18a4d15bd639808722`，US$0.8495／57 image／57 judge／1 music，加舊 US$0.0035 reservation，整集硬上限 US$4.58；STOP 在位、jobs 空。非作者紙審 PASS 後，先把 13 KEEP 安全離線重綁到新視覺雜湊，查實檔 SHA、live status 和整集預算，再一次只畫 PF021 一張，逐張看原始 1280×720；任何機器 FAIL 或人工 REJECT 即停。PF022 仍在範圍外。
