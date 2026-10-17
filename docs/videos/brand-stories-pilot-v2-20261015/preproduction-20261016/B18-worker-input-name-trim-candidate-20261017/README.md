# B18 未證實啤酒公司名稱移除候選

**狀態：離線極小修訂，待獨立差異審查；匯入與正式製作仍 HOLD。**

本目錄接續 [B18 worker 輸入候選](../B18-worker-input-adoption-candidate-20261017/README.md)，以其 `sha256.json` SHA-256 `56d6602b844a5daa055c7a176ad7db739d5ee29150c22eacb89110006071c05a` 和[獨立離線審查](../B18-worker-input-adoption-candidate-20261017/independent-review-20261017.md) SHA-256 `bbb3782c57ec05c4ba0c58dfb766343e67f4ef4f890c051ed93c8552dd1508a1` 為父證據。獨立審查通過父版本的離線 row 與來源，但指出 `names` 尚含來源未證實的「朝日啤酒／アサヒビール／Asahi」。[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)與[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)支持參觀啤酒工廠的故事，未核定是哪家公司。

## 精確變更

- `B18.json:/names` 刪除上述三個名稱；`series-adoption.json:/names` 與 `/plan/names` 同步刪除。其他欄位，包括六章 point、十筆 `must_verify`、六筆來源及來源確認日期、caveat、縮圖與出版序位，完全不變。
- `claim-coverage.json` 和 `remapped-chapters/` 六章均與父候選逐位元組相同：85 景、88 句旁白與 65 筆 `UNCHECKED` 逐景主張、來源和 fact 指標不變。`composeStory` 的本機輸出亦完全相同；這不是媒體或正式 worker 收據。
- `image_notes` 仍規定酒瓶、壽司盤、店招不畫標籤、商標或文字。未證實的公司名稱不再進入後續作者的 `names` 欄，也不會藉企劃被當作史實。

新 `B18.json` 原始檔 SHA-256 為 `209fb773139e96afd5a56f373b6f0843eca902f81b374c19bcd9bc8a4d78e3dd`；canonical story SHA-256 為 `3c43dc0c0eccdb063cc1e62d756c48ce2a476c5bfe1a70b74799c8f3cfc475f1`。`build.mjs --check` 證明上述差異、官方 `storyProblems=[]`、舊 `episodes/reviews/B18.json` 因 hash 不合失效；`manifest.mjs --check` 驗證包內檔案。後端 `check_story_file` 只以記憶體中的 A01 舊列加本 B18 新列檢查結構，不寫匯入檔。

先前獨立審查的 **法院 PDF 讀取界線**仍在：工人讀來源時可能只取得 `supports`，不能把它寫成已讀判決正文；1972 年與 1978 年的權利版本、萬博知名度的來源歸屬、1971／1974 年給茶裝置分歧，仍依父審查及新 [review-request.md](review-request.md) 處理。前一版本的文字審查不自動轉成此 canonical SHA 的 `reviews/B18.json`。正式逐景查核、聽稿、十三題敘事、實測 TTS、圖片／CC／成片、主機及站主觀看均未完成；本候選未呼叫模型、未花費、未匯入或上傳。
