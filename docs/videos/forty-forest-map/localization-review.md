# ForTy 八語製作快照

截至 2026-10-25T22:35:44Z，八語各92句、metadata、獨立翻譯／縮圖審稿與預算提案完成，必要修正已正常native merge。已驗並交付音訊為3／8：VI、EN、JA各92／92句通過；KO第二輪重錄及fit／量測完成，等待ASR槽重檢，ES／PT／ID／TH待製作。八語CC／package及正式品牌bookend未完成，overall及all_eight_ready均為false。

| 語言 | 文字／metadata及必要修正 | M4A／fit | 當前take音檢 | CC及後臺 |
| --- | --- | --- | --- | --- |
| en | 92句、已merge | 當前M4A、89／89窗fit | 92／92 PASS；0 flags／unchecked | M4A已送後臺；CC／package待八語完成後重產整批核對 |
| ja | 92句、已merge | 當前M4A、89／89窗fit | 92／92 PASS；獨審完成，0 flags／unchecked | 已送dub_ja／evidence_ja_m4a；CC／package待整批核對 |
| ko | 92句、已merge | 第二輪retake及fit／量測完成 | 上次92 checked／10 flags；新take待ASR槽重檢 | 未ready／未交付 |
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

## JA目前實測與直接交付

JA經兩輪原文retake、兩輪保義縮句及兩輪等義改詞後，21:50:50原生音檢exit0，92／92句通過，0 flags／unchecked。獨立稽核逐句對帳當前WAV full SHA、完整intended／spoken form及有效原生裁決：62 exact、20 Jev、7 second exact、3 second Jev，0 skipped／kept，未手改轉寫或裁決。

- 當前M4A SHA-256 `a4af09e0a4e5be06f1469c66caa43fb7b7380296103d7159e0b73acb2a53972e`；14775477 bytes、512.805秒、AAC 48kHz stereo，−14 LUFS／TP −2.9 dBTP。
- 89窗全fit、0 over、tempo最高1.19；translation `4c1e48d66bcd3684`，speech `c6d70ecaef91a15d`。
- 21:54:49正常單語增量交付完成：四部分上傳經server組裝SHA／大小驗證，只追加同blob的 `dub_ja`、`evidence_ja_m4a`；authenticated role metadata讀回SHA／大小。原1080p、EN、VI、全部舊files／payload／歷史QA、遠端pending及語言選擇保留。
- 未做遠端二進位串流下載；沒有正式語言批次，未改標準dubs payload或approval。這是已驗JA音訊交付，不代表JA CC／metadata／完整package或全八語ready。
- 獨立稽核 [JA獨立核驗](ja-audio-verification.json)，SHA `1de81cac0e64939a322b0963a9a651093d8c5c88eb29dbe3fbaf5794576fd8e8`；實際增量交付 [JA後臺交付收據](ja-backend-delivery.json)，SHA `ba21ef011b4dab323777485bb85d265e31ca96a1129e62e80f7cd1e78d70ff04`。

## 接續工作

KO上一輪原生check於22:29:17完成，exit1、92 checked／82 accepted／10 flags／0 unchecked；第二輪原文重錄及fit／量測已完成，新take尚未音檢。producer於 `2026-10-25T22:34:59.053831Z` 為 `ko_waiting_shared_asr_slot_after_retake2`，依root指示等待共享Whisper槽釋放。ES／PT／ID／TH仍pending。每語真PASS後獨立核對當前92句，才增量送該語M4A；不擷取正在製作中的語系。目前已驗並交付為VI、EN、JA共3／8。

歷史主片QA有九份CC，不能作為後續配音及字幕的整包ready證據。VI曾於19:22依其音軌重產；其餘CC尚未完成本輪整批核對，八語音軌完成後均須按實際時間軸重產／核對，並保留閱讀速度advisory。不能為硬字數省略環境、類別、單位、否定或算步。八語預設及推薦修法的持續授權已存在。

## 審稿與原生套用證據

[localization/](localization/)保留四組獨立翻譯審稿與四組預算審稿；八語縮圖已由歷史主片核心QA檢查。必要修正的原生套用記錄：

- `/workspace/work/ai-tech-next/forty-en-ja-budget-application.json`
- `/workspace/work/ai-tech-next/forty-ko-es-pt-id-budget-application.json`
- `/workspace/work/ai-tech-next/forty-vi-th-budget-application.json`
- [VI初次fit修正](localization/forty-vi-fit1-application.json)及 `/workspace/work/ai-tech-next/forty-vi-reword1-application.json`。

舊application的「音訊尚未實測」是寫入當時狀態。以[VI目前驗證](vi-audio-verification.json)、[主片及VI交付讀回](main-delivery-verification.json)、EN／JA實際獨審及增量交付收據為準；本快照讀到producer `2026-10-25T22:34:59.053831Z`，不預告KO新take音檢結果。

## 品牌與整體交付限制

本producer沒有正式品牌bookend package／default，ForTy在repo及media workdir都沒有branding.json。已交付b293…d18為主體版；歷史QA11／11及靜態outro不能當成正式品牌bookend或全部新規則已完成。待合法官方素材齊備後依guard另處理；此快照不改source／media／approval。追蹤ID `2026-10-25-local-first-build-without-branding`記在第三片分支，此處不建立不存在的相對連結。八語整包DOD仍未勾，overall false。
