# B18 未證實啤酒公司名稱：獨立差異審查

2026-10-17，Codex `/root/b18_name_delta_review`。**結論：PASS_OFFLINE_EXACT_NAME_DELTA；HOLD_IMPORT_AND_FORMAL_WORKER。** 本審查只承接父版的獨立離線審查，核對這次名稱刪除與其產物；不產生新的正式 `reviews/B18.json`，也不代表主機、付費媒體或成片關卡通過。

## 版本與檢查

| 項目 | SHA-256／結果 |
| --- | --- |
| 父版 `sha256.json` | `56d6602b844a5daa055c7a176ad7db739d5ee29150c22eacb89110006071c05a`，與請求相符 |
| 父版 `independent-review-20261017.md` | `bbb3782c57ec05c4ba0c58dfb766343e67f4ef4f890c051ed93c8552dd1508a1`，與請求相符 |
| 本版 `sha256.json` | `da3820bd403c4a9fb33d2b904cbf3f2b112579a060ee9ab6709c3ab07d7137c3`；列舉 15 檔，`manifest.mjs --check` 通過 |
| 本版 `B18.json` | `209fb773139e96afd5a56f373b6f0843eca902f81b374c19bcd9bc8a4d78e3dd` |
| 本版 canonical story | `3c43dc0c0eccdb063cc1e62d756c48ce2a476c5bfe1a70b74799c8f3cfc475f1`；直接由 `plan.mjs` 另算相同，`storyProblems=[]` |
| `claim-coverage.json` | `7038930605ba1db2adc3b5f2e04ed6fdd9f730a5c9283d56e15b7dc961f5e298`，與父版逐位元組相同 |

逐檔 `git diff --no-index` 顯示 `B18.json:/names` 只刪「朝日啤酒、アサヒビール、Asahi」三筆；`series-adoption.json:/names` 與 `/plan/names` 同樣只刪這三筆。其餘 row／series 欄位，包括六章 point、十筆 `must_verify`、六個來源及其 `supports`、`caveats`、`image_notes`、縮圖與出版序位沒有差異。六個 `remapped-chapters/*.json` 和 `claim-coverage.json` 與父版逐位元組相同；獨立計數仍為 **85 景、88 句、65 筆逐景主張且全部 `UNCHECKED`**。因此旁白、分鏡提示、loops、逐景來源與 fact 指標沒有漂移。

在本版執行 `build.mjs --check` 與 `manifest.mjs --check` 均退出 0。離線 `composeStory` 物件與父版相同、可愛風格視覺問題清單為空；這只說明本機規劃資料的結果，不證明圖片、配音或影片一致。舊 `episodes/reviews/B18.json` 對本版 canonical SHA 回報 `the story changed after this review`，所以舊收據不可轉用。建置自身回報零外部呼叫；本審查未連主機、未呼叫媒體供應商、未匯入或寫入正式站。

## 內容與來源界線

我另搜尋本版 row、series、六章和 coverage 的三種公司名稱：除 `build.mjs`、`delta.json`、`verification.json`、`review-request.md`、`README.md` 作為**移除紀錄**外，沒有在故事、旁白、圖片提示、來源 `supports`、必查主張或 caveat 看到公司名稱。`image_notes` 仍要求啤酒瓶與壽司盤不畫標籤、商標、文字，店招留白；縮圖也指定無標籤酒瓶。[J-Net21 的白石訪談報導](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)記載他在 1948 年參觀吹田的啤酒工廠及輸送帶，沒有在該段指認公司；[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)同樣不提供足以把這次故事中的工廠命名為 Asahi 的證據。本版的泛稱與來源相符。

父版的其他查核界線保留：row 的 caveat 仍分開 [法院判決理由](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)對第 579776 號權利 **1972 年**期滿的認定，與 J-Net21／發明協會 **1978 年**的歷史版本；萬博知名度、道頓堀年份、1971／1974 給茶裝置也沒有被本次改寫。法院 PDF 雖可人工閱讀，父審查記錄正式企劃讀取器把它視為 `application/pdf` 非文字頁，故不能宣稱 worker 已讀判決正文。此版仍須重新取得與新 canonical SHA 綁定的正式審稿收據，且須在 worker 查核時明確保留來源歸屬與 PDF 限制。

**後續閘門：**先準備新 SHA 的獨立正式 review 和 A01／B18 同一 cohort 的可匯入包，再做現場唯讀前檢及授權的匯入流程。六章正式逐景查核、聽眾審稿、十三題敘事、實測 TTS 片長、MiniMax 圖像、可關閉繁中 CC、成片品管與站主觀看均未由這份差異審查完成。
