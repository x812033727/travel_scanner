# B18 Route B：全文到逐景輸入的分階段對位

**狀態：設計候選，HOLD；沒有可匯入的新版企劃列或章稿。** 本包固定已獨立審查的第三版完整口播稿，提出讓工人實際六章與 85 景輸入忠實承接它的變更清單。`route-b-plan.json` 是差異設計，不是已套用的 patch；`check.mjs` 只讀既有候選並驗證清單覆蓋率、來源雜湊及收據，不會更動 active、主機或媒體。

父版企劃及 85 景章稿在 `../B18-attribution-flow-candidate-20261017/`，第三版逐字稿與離線全文審稿在 `../B18-spoken-source-cadence-candidate-20261017/`。正式工人從資料庫 `beats` 自己撰寫六章，不讀這裡的 Markdown 或離線逐景稿；不能把候選資料視為真實工人輸出。

第三版 `B18.md` 內「尚無獨立審稿」是當時寫稿的歷史狀態；同資料夾後出的 `review-candidate.md` 已對該稿固定 SHA 給出離線全文 PASS。正文不因這個狀態說明而改動。

本路線保留第三版全文的文字與審稿 SHA。第三版第三個開場問題是「後場到客席」，父版企劃與 `hook-s006/h7` 卻是「權利期滿」；全文 T01 多了法院 PDF 記錄的 1967 年仙台／東京展店，而父版 row 與 65 筆逐景主張尚未收這項事實。前者要改企劃、對應場景、畫面與伏筆；後者須把法院 PDF P8 L476–495 編入企劃來源及專供獨立審查的事實，然後改 T01 場景與主張。不能只修改五個已知的 i1／i5／i6／i7／n7 來源句。

## 分階段實作次序

1. **新企劃列，隔離審查。** 保留原第 579776 號權利在正文的 `must_verify[4]`；只把第三個開場預告改為後場直線送盤，在 `turn.point` 加入萬博之前的 1967 年展店；來源 `[3]` 的 `supports` 明列法院 PDF P8 L476–495；增列法院 reviewer-only 事實（索引 10），新審查收據須列 `[4,10]`。盤色與裝飾區分價格另列可讀來源 `[2]` 的事實（索引 11）。舊 `episodes/reviews/B18.json` 只對舊 story SHA 有效。
2. **章稿與 85 景對位。** 依 `route-b-plan.json` 的 25 段→場景區間重分 88 句；保留每個既有 scene 與 claim ID，對每個變更的來源、事實索引和畫面做明示映射。針對已不口播的舊 `h4/e9/t3/t18` 明確改寫與搬移，不能孤立留下舊主張或私下刪掉。片頭第三景需從權利資料夾畫面改為後場送盤；I03 的 `ウロコ` 日文原詞與中文解釋須分開；E05 的人工備料、T01 的法院史料、T04 的後場直線、N02 的片尾回收都要按全稿重排。
3. **獨立逐項覆核。** 新 row 自己重跑來源審稿與企劃驗證；全 65 筆舊 claim ID 仍先列 `UNCHECKED`，逐章正式 verifier 才能給判定。重算 loop setup/payoff、圖片／字卡比例、連續卡片、逐鏡時長、`say_for`、lexicon 及完整稿的 `script.md`／`video.json` 一致性。若 85 景無法容納全稿，先在隔離候選增景並記錄成本，不讓長句靠停格硬撐。
4. **正式工人收據。** 工人重新產生六章後，以實際檔案與第三版全文做獨立 reference、facts、narrative 審查；`tools/video/automation/story.mjs` 目前凍結的 B18 舊稿 SHA 仍須另案審查更新。逐章 verifier／listener、整片敘事、TTS 長度與發音、畫面、CC、成片及站主看片全是後續關卡。

此包不授權 B18 付費製作；未取得 B18 費用上限核准，也沒有主機匯入、TTS、MiniMax 圖片、上傳或發布。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-fullscript-route-b-plan-20261017/check.mjs --check
```
