---
id: 2026-11-17-so-that-s-why-waves-89
title: So That's Why waves 89-102 and Curio waves 61-71 cite sources that do not exist
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-11-17T05:29:28Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool/batches
  - docs/videos/history-curiosity/pool/batches
---

# So That's Why waves 89-102 and Curio waves 61-71 cite sources that do not exist

## Why

兩個素材池在 2026-11-16／17 擴進來的題，來源是編造的。引入的提交是 PR #2121 到 #2133（wave61／92 到 wave71／102）。

**原來如此池** `docs/videos/so-thats-why/pool/batches/wave89-*.json` 到 `wave102-*.json`（14 批、784 張卡）：

- 文獻編號連號，同一個標題連用三次（PMC12516161、62、63），後面出現九位數的編號（PMC125200001）。
- DOI 是佔位字串：`10.3390/foods13019001`、`10.1038/s41586-026-w102-001`（批次號加序號）。
- 作者寫 `International Advanced Sciences Consortium`，標題是 `Peer-reviewed Research: ` 加一句中文，每筆的 `read_via` 與 `limitations` 是同一句。
- 2026-11-17 實際連線：`https://doi.org/10.1038/s41586-026-w102-001` 回 404；`…/europepmc/webservices/rest/PMC125200001/fullTextXML` 回 500；對照的 wave88 來源 `…/PMC12136725/fullTextXML` 回 200。
- wave88（含）以前的來源有具體作者、位元組數、雜湊與逐節的閱讀範圍，沒有這些特徵。第三十九到五十二輪的素材審視紀錄也空洞：`reviews/material-20261116-round52.md` 只有 5 行，寫的分鐘數和公式對不上。

**奇聞池** `docs/videos/history-curiosity/pool/batches/wave61-*.json` 到 `wave71-*.json`（11 批、220 張卡）：

- 來源網址是 `https://archive.org/details/historical-inquest-wave71-n7061`、`…/historical_curio_w61_1_1` 這種樣式，DOI 是 `10.1016/j.curio.archival.2026.w71.n7061`。
- 一題一個來源，`read_via` 整批同一句，題目不是問句。
- 2026-11-17 實際連線：`historical-inquest-wave71-n7061` 與 `historical-inquest-wave60-n5841` 都回 404。
- wave60（含）以前的網址是真實的 archive.org 條目樣式，這次沒有動；wave59、60 的 `read_via` 也偏樣板，值得另外看。

只抽查了四個網址，沒有逐筆驗證。判斷依據主要是識別碼的格式不可能是真的。**卡片的內容也可能是編的，不只是出處。**

## 已經做的隔離（票 `2026-11-17-fold-a-demand-dimension-into-the`，PR #2136）

- 原來如此：30 組靠這些卡的可成題長題改成後備（G668–G672、G674–G676、G678、G679、G681、G682、G684、G685、G688、G695–G709），`material.was` 記 `ready`。每一組的 14 張卡全部來自 wave89–102。可成題長題 84 → 54。另有 12 組本來就是後備的題案也全部用這些卡：G673、G677、G680、G683、G686、G687、G689–G694。
- 奇聞：入選的 187 題移到 `selection.json` 的 `held`，入選核心 1839 → 1652。它們沒有進任何題案。
- 批次檔與卡片都沒有刪。

## Definition of done

- [ ] 站主決定這 25 批怎麼處理：照池子原本的做法重讀真實來源重做、還是移除。
- [ ] 查出是哪一條流程或哪個代理產生的，補上擋它的檢查（例如 build 時拒絕不存在的識別碼樣式，或要求每個來源有請求紀錄與雜湊）。
- [ ] 處理完後，兩個池 README 的總數與各輪章節對得上實際內容（原來如此 README 的總數停在第四十二輪）。

## Steps

- [ ] 逐批確認範圍：原來如此 wave89–102、奇聞 wave61–71；另看奇聞 wave59、60。
- [ ] 決定重做或移除；移除要照兩個池的基線與存檔點規則登記。
- [ ] 加檢查。

## How to verify

對任一張受影響的卡，照它 `sources` 的 `url` 與 `canonical_url` 發一次請求（`Mokaair-editorial/1.0` 標頭），看是否存在。

## Notes

- 這張票是紀錄，沒有人認領。隔離的改動在另一張票上。
- 需求評分把原來如此這 30 組也評過，分數留在題案上；題案改後備後不再受門檻檢查。
