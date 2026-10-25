# ForTy 八語製作快照

截至 2026-10-25T21:02:27Z，八語各92句、metadata、獨立翻譯／縮圖審稿與預算提案完成，必要修正已正常native merge。已驗音訊為2／8：VI、EN各92／92句通過並已直接送達後臺下載角色；JA在bounded retake1流程，其餘五語待製作。八語CC／package未完成，`all_eight_ready=false`。

| 語言 | 文字／metadata及必要修正 | M4A／fit | 當前take音檢 | CC及後臺 |
| --- | --- | --- | --- | --- |
| en | 92句、已merge | 當前M4A、89／89窗fit | 92／92 PASS；0 flags／unchecked | M4A已送後臺；CC／package待八語完成後重產整批核對 |
| ja | 92句、已merge | 初次M4A生成／fit；retake1中 | 初檢92句／9 flags；當前take待重檢 | 尚未交付音軌 |
| ko | 92句、已merge | 待製作 | 未開始 | 初稿；待M4A對時及交付 |
| es | 92句、已merge | 待製作 | 未開始 | 初稿；待M4A對時及交付 |
| pt | 92句、已merge | 待製作 | 未開始 | 初稿；待M4A對時及交付 |
| id | 92句、已merge | 待製作 | 未開始 | 初稿；待M4A對時及交付 |
| vi | 92句、已merge | 當前M4A、89／89窗fit | 92／92 PASS；0 flags／unchecked | 已按dub重產CC；已附下載別名，速度advisory保留 |
| th | 92句、已merge | 待製作 | 未開始 | 初稿；待M4A對時及交付 |

## VI目前實測

初次92句合成後，ckag保義縮至21 chars，保留0,308與0,996，1句新合成／91句重用。音檢10→6→4 flags後，完成兩輪原文重錄及一輪四句等義改詞（jw6i、u5js、3p97、88pk）；最後4句新合成／253 billable chars、88句重用。正常原生重檢於19:21:17完成，exit0，92 checked／accepted、0 flags、0 unchecked，未手改轉寫或cache裁決。

- 目前M4A：512.805秒、12076524 bytes，AAC 48kHz stereo，−14 LUFS、TP −2.9 dBTP。
- SHA-256：`1f50cdfe5b5e6ff31ea562286d77ffd9c2df7dc00f75fea6e3f2b2036ce782f8`；translation `4b427c0fa1ee4bf8`，speech `c6d70ecaef91a15d`。
- 89窗全fit，0 over、0 skipped／kept；兩窗tempo，最高1.10。當前WAV、轉寫、完整目標文字及原生裁決已對帳；[VI驗證](vi-audio-verification.json)只宣稱VI ready，明列 `all_eight_ready:false`。
- 19:22的native captions已以目前dub時間軸重產VI CC；當時主片11／11 QA通過，VI等語字幕閱讀速度advisory仍保留。
- 正常final提交已附目前VI音軌，另以 `evidence_vi_m4a` 提供下載別名；原角色保留。驗證為server驗SHA的上傳及authenticated role metadata讀回，未做遠端二進位串流下載。遠端final仍pending，未提交八語language batch。

## EN目前實測與直接交付

EN經兩輪原文retake、兩輪保義縮句及兩輪等義改詞後，20:30:29原生音檢exit0，92／92句通過、0 flags／unchecked。獨立稽核逐句對帳當前WAV full SHA、native key、ASR clip16、完整intended／spoken form與有效原生裁決：54 exact、30 Jev、6 second exact、2 second Jev，未手改轉寫或裁決。

- 當前M4A SHA-256 `6ca5213241ac1f107141ebd4d2e410d4f6474efe39bb1374f2fd35abc0192c63`；512.805秒、13547232 bytes、AAC 48kHz stereo，−14 LUFS／TP −2.8 dBTP。
- 89窗全fit、0 over／skipped／kept，tempo最高1.21；translation `bfff4c39fe664d8e`，speech `c6d70ecaef91a15d`。
- 20:52:20正常單語交付完成：只上傳此已檢M4A，四個原生分段完成server SHA／大小驗證，追加 `dub_en`、`evidence_en_m4a`。authenticated GET讀回角色SHA／大小，原1080p、VI、所有舊files／payload及歷史QA保留，遠端final仍pending。
- 沒有native final重推、未夾帶未檢JA，沒有改標準dubs狀態或語言選擇、沒有正式語言批次。這是EN已驗音軌交付，未宣稱英語CC／metadata／整包ready；未進行遠端二進位串流下載驗SHA。
- [EN獨立稽核](en-audio-verification.json)（SHA `c02f9097a75b672f6965fd94a046fa649cfb523b85e81bef83cbeb0ff0552e10`）；[實際20:52交付收據](en-backend-delivery.json)（SHA `3211bb800cb6f2d7eddc434d938c23f4c1ead55c2fd209f1e98723d1fa2127cc`）。

## 接續工作

JA初次音檢已真實完成92 checked／9 flags（21:00:08、exit1），正進行bounded retake1流程，尚未ready；producer `ja_dub_running`（狀態 `2026-10-25T21:02:20.158Z`）。 其後依序KO、ES、PT、ID、TH。每語真PASS後獨立核對當前92句，才增量送該語M4A；不等全八語，也不擷取正在製作中的語系。目前已驗音訊只有VI、EN。

歷史主片QA有九份CC，不能作為後續配音及字幕的整包ready證據。VI曾於19:22依其音軌重產；其餘CC尚未完成本輪整批核對，八語音軌完成後均須按實際時間軸重產／核對，並保留閱讀速度advisory。不能為硬字數省略環境、類別、單位、否定或算步。八語預設及推薦修法的持續授權已存在。

## 審稿與原生套用證據

[localization/](localization/)保留四組獨立翻譯審稿與四組預算審稿；八語縮圖已由歷史主片核心QA檢查。必要修正的原生套用記錄：

- `/workspace/work/ai-tech-next/forty-en-ja-budget-application.json`
- `/workspace/work/ai-tech-next/forty-ko-es-pt-id-budget-application.json`
- `/workspace/work/ai-tech-next/forty-vi-th-budget-application.json`
- [VI初次fit修正](localization/forty-vi-fit1-application.json)及 `/workspace/work/ai-tech-next/forty-vi-reword1-application.json`。

舊application的「音訊尚未實測」是寫入當時狀態。以[VI目前驗證](vi-audio-verification.json)、[主片及VI交付讀回](main-delivery-verification.json)及實際producer紀錄為準；本快照讀到producer `2026-10-25T21:02:20.158Z`，不預告JA當前重錄／音檢的結果。
