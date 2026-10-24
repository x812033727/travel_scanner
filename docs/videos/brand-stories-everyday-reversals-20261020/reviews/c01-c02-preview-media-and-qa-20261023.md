# C01／C02 試片素材與品管讀回（2026-10-24）

**狀態：素材未找回；兩集均不可上架。** 本輪只讀檢查沒有取得影片、字幕、縮圖或逐句音檔的實際位元組。下列雜湊與時長來自 2026-10-20 的製作紀錄，**不是本輪重新驗證**；原始雲端 `/workspace` 是否還存在、是否另有備份，仍未確認。

| 項目 | 舊製作紀錄 | 本輪結果 |
| --- | --- | --- |
| C01 `preview.mp4` | SHA-256 `5ba761f9cb0b68cdaa96da4855b6c66e35cb0414f57c26a49a15bb1f1b432322`；約 189 MiB、19,553 格、651.77 秒 | 已查路徑均未找到；無法重算雜湊或完整解碼 |
| C01 `preview.zh-TW.srt`／`.vtt` 與已付費來源素材 | 舊目錄 `/workspace/.brand-video-workdir/story-everyday-crocs-c01/review/local-preview/`；交接未列字幕雜湊 | 未取得位元組或可驗證備份 |
| C02 `preview.mp4` | SHA-256 `f146606206290086cec6215f46250bf0cbaf6ec3e3795950deac1e82eaa1f9da`；163,204,884 bytes、19,169 格、639.00 秒 | 已查路徑均未找到；無法重算雜湊或完整解碼 |
| C02 `thumbnail.jpg`、SRT、VTT | 舊 SHA-256 依序為 `f63c6de3797e381ec8e7235261c8ea685e01ef463975e61177160e14f63655d4`、`90c91afa9e983bb954f1e547150b1965b529acf764ba23747590e3db528fdb34`、`4207c52d32f9141d7480f95bd4767dff1c462751e579e24a4284d6175ca4ed0a` | 未取得位元組或可驗證備份 |
| C02 92 句 WAV、`review/check.json`、`review/check-flags.json` | 舊目錄 `/workspace/.brand-video-workdir/story-everyday-tupperware-c02/` | 未取得位元組；十句旗標無法人耳覆核 |

## 本輪查找範圍

- 2026-10-24 `Test-Path -LiteralPath` 確認 `<home>\mokaair-work\videos\story-everyday-crocs-c01`、`<home>\mokaair-work\videos\story-everyday-tupperware-c02`、`C:\workspace`、使用者目錄下的 `.brand-video-workdir`／`brand-story-preview` 均不存在。
- G: 已掛載；指定候選 `G:\我的雲端硬碟\AI\videos\<slug>` 與 `G:\我的雲端硬碟\AI\mokaair-work\videos\<slug>` 兩集目錄均不存在。淺層備份專案清單沒有這兩集；對現有備份收據與交接文字的定點搜尋，也沒有兩集 slug 或上述試片雜湊。
- 唯讀連線正式主機 `hostinger2` 時，舊文件所列 `/workspace/.brand-video-workdir/story-everyday-crocs-c01/`、`/workspace/.brand-video-workdir/story-everyday-tupperware-c02/`、`/workspace/brand-story-preview/tupperware-c02/` 及 `/var/lib/mokaair/video-work/<slug>` 未找到。**正式主機不等於原始雲端工作區**；這些陰性結果不能證明原始工作區已被刪除，也不能證明沒有其他備份。

## 未通過的成片關卡

- C01 舊 97 句自動音訊檢查曾通過，仍缺正式 worker 品管、站主指定的 5 秒片頭與 21 秒 v4 片尾、品牌驗收、站主實際看片及正式 `final.mp4`。
- C02 舊檢查尚有十句音訊旗標，優先人耳聽 `c020901`、`c021504`、`c021904`，再聽其餘七句。自動辨識文字與原稿不一致，不能直接判成 TTS 口誤；沒有 WAV 時也不能宣稱清除旗標。
- 兩集的 `local-preview.mjs` 都只產概念試片，不寫正式 `checks.json` 或 `final.mp4`。後台企劃／劇本匯入、試片、正式成片、上傳和發布是不同關卡；C01／C02 目前不列入已核准劇本匯入或可上架影片。

**下一步：**取得原雲端工作區快照或具名備份位置，按舊雜湊比對試片及可得素材，再做 `ffprobe`、完整解碼和 C02 逐句人耳覆核。任何搬移都先複製、讀回、記錄雜湊；保留已付費音檔與影格。這份收據不授權重錄、重新生圖、上傳或發布。

來源：[C01 試片紀錄](../../story-everyday-crocs-c01/local-preview.md)、[C01 交接](../../story-everyday-crocs-c01/publishing-handoff.md)、[C02 試片紀錄](../../story-everyday-tupperware-c02/local-preview.md)、[C02 音訊審查](../../story-everyday-tupperware-c02/reviews/audio-check.md)、[C02 交接](../../story-everyday-tupperware-c02/publishing-handoff.md)。
