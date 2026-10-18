# A01 r16 來源企劃 25 筆校正候選 — HOLD

這是**離線來源元資料候選**，從 `A01-r12-snapshot104-six-chapter-bridge-20261018/candidate/series.json` 的 25 筆企劃來源衍生。`candidate/series.json` **只更正零起算索引 23 的 `publisher`**：原欄位把 Plath 的署名自述當成出版者；出版者應為 West Seattle High School Alumni Association《Chinook》。索引 23 的來源 URL、`kind`、`supports`、`checked`，索引 24 的 Travelpro 來源，以及其他全部位元組均維持橋接提案原值。作者歸屬仍寫在索引 23 的 `supports` 與 r16 的 `t7b` 主張中。本包不改 r16 口播／畫面、r12 橋接、104→105 夾具或正式機。

## 來源與界線

| 來源 | 查證內容 | 使用界線 |
| --- | --- | --- |
| [West Seattle High School Alumni Association《Chinook》2024，第 17 頁](https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf)；[校友會期刊索引](https://wshsalumniassociation.org/chinook-archived-issues/) | Robert Plath 署名簡歷寫 1988 年發明直立 Travelpro Rollaboard。 | 屬多年後自述；[Travelpro 公司史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)記 1987 年，不能據此定讞唯一發明年份。SL8 PDF 與校友會鏡像的位元組同一性未在本包驗證。 |
| [Travelpro〈Duffel Bag vs. Rolling Suitcase〉](https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases)（2021-09-15） | 官方比較說部分旅客用輪箱走樓梯或顛簸人行道可能困難。 | 只支持 r16 `n14`／`now-06` 的有限陳述；不能推成所有旅客必須提箱或歷史實測。 |

## 精確集合與稽核

| 集合 | 筆數 | 證據與用途 |
| --- | ---: | --- |
| 正式機 104 快照 `story-rolling-suitcase-v2/series.json` | **13** | 2026-10-18 唯讀擷取；該檔 SHA-256 `68df2792fa98971eb805c8af773c8b3726801832cca03ed753a950bb56311cbc`。本包的重建檢查不從私人擷取資料重算此數，亦不宣稱此為 2026-10-19 即時狀態。 |
| r16 編輯企劃 `candidate/series.json` | **23** | 已凍結 r16 原值；零起算 0–22 的 URL 順序與橋接提案相同。 |
| 本包修正的來源企劃 | **25** | 0–22 保留橋接提案；索引 23 是《Chinook》，24 是 Travelpro 樓梯比較頁。 |
| r16 `video.json.sources` 公開引用 | **18** | 與 `source-map.json`、78 筆 `PENDING` 主張引用 URL 一一對齊；25 筆企劃中另有 7 筆研究／核對用來源不在公開引用內。 |

`source-alignment.json` 逐筆列出 **78** 個離線主張 ID、URL、25 筆企劃索引與 18 筆公開索引。`t7b` 是企劃 **23**／公開 **16**；`n14` 是企劃 **24**／公開 **17**。檢查程式會驗證來源順序、兩筆缺口、所有映射、研究用 7 筆集合，以及 `candidate/series.json` 除第 23 筆出版者外與已釘選橋接檔完全一致。正式工人的 `numberClaims` 仍會重編 `t7b`；此映射不能直接充作主機審稿收據。

## 重建與限制

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-r16-source-plan-25-candidate-20261019/build.mjs --check
```

`--check` 只讀已釘選的 r12 橋接、r16 候選及本包輸出，任何漂移即失敗；`--write` 只重建本資料夾的 `candidate/series.json`、`source-alignment.json`、`manifest.json`。**HOLD：不可直接安裝或公開 25 筆來源。**正式採用前仍需修正工人的 A01 公開引用過濾、核對 104→新版本主機狀態與六章、重編主張、獨立完成 verifier／listener／兩名敘事讀者及綁定正式雜湊的 `story/reviews/script-review.json`。本包不授權主機寫入、解除 STOP、付費媒體、配音、合成或上傳。
