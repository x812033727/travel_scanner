# S61 R2｜作者針對軍種歸屬的修正交接

2026-10-22 UTC。**R2 作者修正，待其他人重覆核；R1 的獨立史料／書面畫面 HOLD 未由作者自行解除。** 依 [R1 獨立覆核](r1-independent-source-visual.md)，Prince 固定全文 L1832–1834 說火藥庫位於 *naval yard*，且 *an entire battery volunteered* 灌水；沒有說這支砲兵隊屬海軍。

## 精確改動

- `s61058` 改為「一整支砲兵隊」，YouTube 說明、企劃一句答案、`research.md` P08 同步收窄；`s61035` 及企劃中的「海軍火藥庫」改成位置明確的「海軍造船廠的火藥庫」。保留 Prince 對未再爆炸的歸因，沒有增加命令、值勤時刻、供水機制或實際火距。
- `s61009`、`s61054`、`s61058`、`s61063`、`s61098`、`s61102` 六個提示詞不再把志願者畫成海軍人員；其中可見的水管也移除，避免把未記載的灌水方式畫成史實。消防員救火鏡頭及海軍造船廠位置未改。
- `claims.md` 與 `script.md` 隨上述兩句旁白和六個鏡頭同步，任務票的錯誤英文軍種記述已修正。其餘章節、來源錨點及影像數未改。完整逐行 before／after、行號、前後 SHA-256 與正反向重放結果見 [r2-author-delta.json](r2-author-delta.json)：六檔共 25 個精確行替換；其中 `script.md` 另有自動更新的 narrative／speech hash 兩行。

## R2 固定值與驗證

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `91ff577923a5cac28728b3c67b86ab52e9d9b628afe435f5be7d43b74c57426d` |
| `research.md` | `a012983fabf32d076941412c791f650e84a8c5f9b96b8554aa3fdce913799c9c` |
| `video.json` | `800a8c7476bee77fad9b97e8a23e5b7e26007cfcf32e5ee471db371257fec134` |
| `script.md` | `1f55c9182b1aac974cecea31d7755b1c310da29db651a6993aa310da9bb63fc9` |
| `claims.md` | `5087fd10009f997c135f420c2c09ba0ebd3a59ea996296f0ac31aa15006c681f` |
| `r2-author-delta.json` | `6999476f46e99f09ee51a572f958ab3c5f5235a96610a706ab16590592982b1c` |

Prince 固定原文 commit `befb706982ba1be631a52d4f686be301c2de7f34`、raw SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52` 未變。重新生成 `script.md` 得 narrative hash `946c1c8bbc7a0f5f`。影片 lint **0 errors、0 warnings**：107 句、七章、14 組設問、95 個插圖鏡頭與 9 張資訊卡，第一章約 57 秒，全段工具估約 10.293 分鐘。作者機械核對 107／107 句與證據表及生成劇本一致、95／95 個提示詞逐字一致且不重複；逐行 delta 能由 R1 正向重放至 R2，並由 R2 逆向重放至 R1。`npm run check:tasks` 通過 2,416 件任務檔驗證，仍有與 S61 無關的既有逾時／範圍警告。

**下一步：**由未參與作者修稿者以 R2 雜湊重覆核史料與畫面，再走兩位盲讀及系列媒體關卡。本輪沒有 TTS、圖片、音樂、品牌動畫實作、成片、YouTube Studio 連結或付費製作。
