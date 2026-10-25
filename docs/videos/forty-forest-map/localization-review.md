# ForTy 八語製作快照

截至 2026-10-25T19:34:15Z，八語各92句、metadata、獨立翻譯／縮圖審稿與預算提案完成，必要語義及預算修正已正常native merge。VI目前音軌92／92句通過且有後臺下載別名；EN正在原生製作。八語整體仍未完成，`all_eight_ready=false`。

| 語言 | 文字／metadata及必要修正 | M4A／fit | 當前take音檢 | CC及後臺 |
| --- | --- | --- | --- | --- |
| en | 92句、已merge | 19:28:17開始native dub | 未完成 | 初稿；待實際M4A對時及交付 |
| ja | 92句、已merge | 待製作 | 未開始 | 初稿；待M4A對時及交付 |
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
- 19:22的native captions已以目前dub時間軸重產VI CC；最新11／11 QA通過，VI等語字幕閱讀速度advisory仍保留。
- 正常final提交已附目前VI音軌，另以 `evidence_vi_m4a` 提供下載別名；原角色保留。驗證為server驗SHA的上傳及authenticated role metadata讀回，未做遠端二進位串流下載。遠端final仍pending，未提交八語language batch。

## 接續工作

主片1080p與已檢VI讀回完成後，root於19:28釋出其餘七語；目前producer `/root/forty_r1_listener` 的 `en_dub_running` 正在運行。依序完成EN、JA、KO、ES、PT、ID、TH的實體M4A、實際fit、當前take音檢與CC對時，再做package及正常後臺語言交付讀回。其餘七語沒有被標成ready。

核心QA有九份CC並不代表八語dub ready；尚無M4A的七語CC仍是主片時間軸初稿。各語音軌完成後須使用自己的實際時間軸並檢視閱讀速度。不能為硬字數省略環境、類別、單位、否定或算步。八語預設及推薦修法的持續授權已存在。

## 審稿與原生套用證據

[localization/](localization/)保留四組獨立翻譯審稿與四組預算審稿；八語縮圖已由最新核心QA檢查。必要修正的原生套用記錄：

- `/workspace/work/ai-tech-next/forty-en-ja-budget-application.json`
- `/workspace/work/ai-tech-next/forty-ko-es-pt-id-budget-application.json`
- `/workspace/work/ai-tech-next/forty-vi-th-budget-application.json`
- [VI初次fit修正](localization/forty-vi-fit1-application.json)及 `/workspace/work/ai-tech-next/forty-vi-reword1-application.json`。

舊application的「音訊尚未實測」是寫入當時狀態。以[VI目前驗證](vi-audio-verification.json)、[主片及VI交付讀回](main-delivery-verification.json)及實際producer紀錄為準；本快照讀到producer `2026-10-25T19:28:17.308Z`，不預告運行中的EN結果。
