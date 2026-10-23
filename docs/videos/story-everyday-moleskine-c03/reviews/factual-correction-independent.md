# C03 Moleskine｜2016 年底直營店數獨立複核

複核日：2026-10-22（臺北）。複核者：Codex `brand_audit` 子代理，未撰寫本次主稿或媒體。結論：**「2016 年底 79 家直營店」的來源與文字改動通過獨立複核；音訊、字卡渲染與成片尚未驗收。** 本收據不核准新增付費嘗試、上傳或發布。

## 受審版本與來源

| 項目 | 核對結果 |
| --- | --- |
| 現行 `video.json` SHA-256 | `2DCFE691C05C5A041B16BCDBB77ACC8FDAE2955D0247CC41F951C5C9097F7833` |
| 修正前 `video.json` SHA-256 | `5729039524FA9F0F915002C96D7CD6F8BAD8BA6C8C2C042EA5DE6DBB6B7FD792` |
| 現行 `narration-draft.md` SHA-256 | `4C23F1DB6F45F9BD9220FCAB74257600F7CC17B8236AEF0B914CCFC9426E8314` |

- [D’Ieteren《2016 Activity Report》](https://dieterengroup.imgix.net/annual-reports/3_moleskine.pdf)印刷頁 35 明說 **79 家直接營運門市**，頁 37 的 2016 年比較表列 `Number of stores = 79`。[集團《2017 Annual Report》](https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf)財務與董事報告印刷頁 7 明說門市由 **2016 年底 79 家**增至 2017 年底 87 家。合看三處原文，現行 `c03-p12-s02` 旁白「到 2016 年底，已有七十九家直營店」及同景字卡 `79 家／2016 年底直營店` 有直接來源支持。
- [D’Ieteren 2017 年投資人簡報](https://dieterengroup.imgix.net/documents/presentations/moleskine_lorenzo_viglione.pdf)投影片 15 把 2016 年直接營運門市標為 **78**，未在圖上明標年底日期。此數字與年報相衝；現行稿採兩份年報支持的 79，`source-matrix.md` S6 已保留分歧及各頁定位。批發 `doors` 與直營店沒有混算。

## 改動範圍與媒體保留

- 與 Git 基線及修正前版本對照：原有 **14 個 `shot`→`stats`** 的畫面改版仍在；另兩張舊字卡只補來源頁。此次事實修正只動 `c03-p12-s02`／句 `c031202` 的 **78→79** 與來源，`script.md`、`narration-draft.md` 同步改同一數字。94 個場景 ID／順序、其餘 93 句旁白、`look`、來源清單及 21 條 `loops` 均未變。舊 `verify-3.md`、`verify-4.md` 的 78 是其舊版簽收，不套用到現行雜湊。
- `build-local-video.mjs` 現標為歷史產生器，已移除寫入 `video.json` 的路徑；其舊 78 及 83／11 配置不得重建現行影片。現行配置是 **67／94 插畫（71.3%）與 27 張字卡**，最長連續字卡 **2 張**；`node tools/video/cli.mjs lint --slug story-everyday-moleskine-c03` 為 **0 errors、0 warnings**。
- 唯讀核對工作區：67 個現行插畫景均有原選圖、通過的圖片評審，檔案 SHA-256 與 manifest 相符；媒體帳本為 116 次圖片、116 次圖片評審及 1 首配樂，共 **US$1.646**、保留額 0。逐 ID 圖片嘗試最多 3 次，沒有超額景。這些是已付費產物的保留證據，不等於現行整片成本已完整核銷或畫面已驗收。

## 尚未完成的關卡

複核時，修正一個口播數字已使現行語音雜湊 `0fcff03acf93ed47` 與既有時間軸 `a23505d0a1da1c09` 不同。先按既有預算停線乾跑並必要時只重錄 `c031202`，再重測時間軸、正文純語音時長、人耳念法與字幕。現行畫面雜湊 `35f8abdf564d872a` 也與關鍵影格 manifest 的 `2cef3031b6ac1da4` 不同；須重綁既有合格圖片、產生本機字卡，檢查 `c03-p19-s04` 的 2.8 秒字卡可讀性，並重新做完整 1080p 解碼、音畫與 CC 驗收。站主看片、上傳和發布仍須各自留下收據。本次獨立複核沒有編輯主稿、媒體或呼叫付費工具。
