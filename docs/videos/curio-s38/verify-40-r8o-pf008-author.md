# S38 R8o｜`pf008` 成人與時代提示詞定點修正，作者凍結

2026-10-21 UTC. [R8n 原生圖](verify-39-pf008-010-native.md)把 1666 年倫敦佩皮斯窗邊遠火畫成多名兒童、東亞服裝和紙格窗，雖然機器評審報 PASS，人工已退件。**R8o 只改 `pf008` 的 `data.prompt`，不重畫、不改系列 `look` 或旁白。**

新提示詞把「one fully grown English man in his thirties with mature facial features」、倫敦與 1666 年日期、羊毛上衣／亞麻領布、木框上窗放在句首；唯一動作是探向窗口判斷遠處紅光。它保留日記的**遠處**感與黎明前時序，不畫已確定的火源或某戶被燒。木窗與衣貌是可愛卡通的年代示意，不稱日記記錄了窗形或服裝。相較 R8n，刪掉尾端否定式「no Asian court costume or modern fixtures」，改用正向、具體的英國成年人物與窗形；`look.preset` 仍為 `cute-mystery`。

[逐字結構化差分](verify-40-r8o-pf008-structured-diff.json)記下舊／新 prompt 與 `scenes[7].data.prompt`。目前 `video.json` SHA-256 **`183534e814a5142613ff2d5db56cfe0a3e5424af4aa622bd7667d3080b36684d`**；將這**唯一**字串替回舊值，原始位元組 SHA-256 精確回到 R8n **`df05f4a886abfe18018a85db948623cfe96537940c5ed7cf1f71461752bb1e35`**。其他 111 景、所有口播、鏡頭運動、章節、開場 `pf005` 1.6 秒停頓、`pf006`／`pf007` 文字卡、已收 `pf001`–`pf005` 各 prompt 均未改。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json`：**0 errors／0 warnings**。

這是作者書面候選，仍須另一位工作者核精確差分、日記 [9 月 2 日 L65795–65803](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L65803)與書面畫面界線後，才能**單張**定點重試 `pf008`。私有 `STOP` 仍在；ledger **US$0.3535、21 image／20 judge／1 music、舊 `pf003` 預約 US$0.0035**，整集上限 US$4.58。R8n 的 `pf008` 圖即使保留在舊 manifest 也仍是人類 REJECT，不得當成 R8o 圖。舊圖原生檔已私有備份。聲畫、網站音訊／分鏡及交付關卡仍 HOLD。
