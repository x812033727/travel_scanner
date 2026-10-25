# ForTy 八語製作快照

截至 2026-10-25T18:42:32Z，八語各92句字幕文字、metadata、獨立審稿與預算提案均完成；必要語義修正已由root以正常native流程merge。這是文字階段完成，外語可交付音軌目前為0。

| 語言 | 文字／metadata及必要修正 | M4A | 實際fit | 音檢 | CC及後臺交付 |
| --- | --- | --- | --- | --- | --- |
| en | 92句、已merge | 未製作 | 未開始 | 未開始 | 初稿；待M4A重對時／未交付 |
| ja | 92句、已merge | 未製作 | 未開始 | 未開始 | 初稿；待M4A重對時／未交付 |
| ko | 92句、已merge | 未製作 | 未開始 | 未開始 | 初稿；待M4A重對時／未交付 |
| es | 92句、已merge | 未製作 | 未開始 | 未開始 | 初稿；待M4A重對時／未交付 |
| pt | 92句、已merge | 未製作 | 未開始 | 未開始 | 初稿；待M4A重對時／未交付 |
| id | 92句、已merge | 未製作 | 未開始 | 未開始 | 初稿；待M4A重對時／未交付 |
| vi | 92句、已merge | 已生成 | 89／89窗 | 初檢92句、10 flags，待retake1 | 待按M4A重對時／未交付 |
| th | 92句、已merge | 未製作 | 未開始 | 未開始 | 初稿；待M4A重對時／未交付 |

## VI實際結果

- 初次真實合成92句、5822 billable chars，只有ckag一窗超長。round1保義縮至21 chars，保留0,308與0,996；正常重新合成1句／21 chars，91句重用。
- 原生fit目前89窗全過、0 over；兩窗使用tempo，最高1.10。fit通過不代表音檢通過。
- `/workspace/work/videos/forty-forest-map/dubs/vi.m4a`：512.805秒、AAC 48kHz stereo、11987551 bytes，−14 LUFS、TP −2.9 dBTP。
- M4A SHA-256：`297cd4d7666f926ad479ed5e593db904815191ee241e52e6c83eae730860be4a`。
- session37621初次音檢已真實完成：exit1、92 checked、10 flags，均有二轉寫。flags為 `jw6i/erqz/jkby/u5js/3p97/dkq3/beg8/88pk/bu6j/hr4b`。接手代理依root核心快照commit後進行bounded retake1；本檔未聲稱後續重錄或重檢已完成。

## 保留的限制與下一步

核心11／11 QA中的九份CC是當時初稿，不能當成八語dub ready。每語M4A生成／fit／音檢後，仍須重新產生或對齊自己的CC並檢查速度；目前advisory保留，單句字數指引不等於共享音窗的實測。不得為硬字數刪環境問句、類別、單位、否定或算步。

先完成VI flags的正常重錄／重檢，再製作並檢查其餘七語M4A。全部語言需有實體音軌、實際fit及當前take音檢結果；完成各自CC與package後，才能記錄真正後臺交付／下載及讀回。主片final目前也尚未送，避免自動夾帶未通過音檢的VI。八語預設與推薦修法的授權已存在，不另詢問。

## 審稿與原生套用證據

[localization/](localization/)保存四組獨立審稿與四組預算審稿，必要修正的原生套用記錄為：

- `/workspace/work/ai-tech-next/forty-en-ja-budget-application.json`
- `/workspace/work/ai-tech-next/forty-ko-es-pt-id-budget-application.json`
- `/workspace/work/ai-tech-next/forty-vi-th-budget-application.json`
- `/workspace/work/ai-tech-next/forty-vi-fit1-application.json`；另存 [VI fit修正紀錄](localization/forty-vi-fit1-application.json)。

舊application的「音訊尚未實測」描述其寫入當時；目前只有VI已做真實fit及第一次音檢。最新原生fit為 `/workspace/work/videos/forty-forest-map/dubs/vi/fit.json`，初檢為 `review/check.vi.json`／`review/check-flags.vi.json`。無未完成音軌或未完成後臺交付被標成ready。
