# seoul-ganjang-gejang-food-guide：第一輪獨立事實查核

查核日期：2026-09-20。此檔依本輪實際重新開啟的官方可見頁與 Commons 檔案頁重建；沒有採用另一份查核報告的結論。

## 分店官方來源重開

| 分店 | 本輪重開的官方頁 | 可重現的可見文字 | 與正文的處理 |
|---|---|---|---|
| 양반댁 | VISITKOREA 英文 `vcontsId=99515`，HTTP 200 | 頁面含 Ganjang、11:30、21:00 與 27 等店家欄位文字。 | 保留它是仁寺洞店、主項為醬蟹定食的寫法；不把定食配菜推成每間店都有。 |
| 함초간장게장 | VISITKOREA 英文 `vcontsId=59525`，HTTP 200 | 頁面含 Ganjang、11:30 與 27 等店家欄位文字。 | 保留明洞分店、醬蟹與醬油蝦分列的說法；沒有把其他店的時段挪用到這家。 |
| 진미식당 | VISITKOREA 英文 `vcontsId=192629`，HTTP 200 | 頁面含 Ganjang、`186-6` 與店家資訊。 | 正文採用麻浦대로 186-6 作為辨識，不以其他城市同名店替代；菜單仍限於官方頁列出的 gejang 相關項。 |
| 게방식당 | VISITKOREA 英文 `vcontsId=59972`，HTTP 200 | 頁面含 Ganjang、11:30、21、`131-gil` 與 27 等店家欄位文字。 | 保留醬油／辣味醃蟹與蟹湯、醬蟹拌飯是此店頁所列項目；沒有將它們推給其餘三店。 |

四個 URL 均為內容包 `sources` 中的分店官方頁，請求時均回 HTTP 200。頁面可能隨店家更新而改變，本文的營業時間與門牌在出發前仍需以店家當日公告確認。

## 圖片、授權與圖解

- 已實看隔離 repo 的 hero 與 photo-1：hero 為白盤中的醬油醃蟹、辣椒和芝麻；photo-1 是蟹肉與蟹黃近拍。兩張是料理示意，沒有標成四間店中任何一間的實拍。
- Commons 檔案頁的可追溯資料已寫入 `write/seoul-ganjang-gejang-food-guide/images.json`：`Gejang.jpg` 為 kimsco、CC0；`Ganjang-gejang 1.jpg` 為 lazy fri13th、CC BY 2.0。來源 URL 分別為 `https://commons.wikimedia.org/wiki/File:Gejang.jpg` 與 `https://commons.wikimedia.org/wiki/File:Ganjang-gejang_1.jpg`。
- `diagram-1.svg` 可作 XML 解析；title／desc 與 간장게장、양념게장、간장게장 정식、꽃게탕、게장비빔밥、새우장標示存在。圖解把品項寫成各店供應，不把醬蟹拌飯誤稱所有店都提供。

## 結論與未完成項

本輪完成四個分店官方頁、兩張圖片對 alt 的實看，以及 Commons 作者與授權的重新核對。此工具環境沒有在本輪輸出 SVG 的瀏覽器像素 render，也沒有執行 dry-run、ingest 或定向 lint；因此不把這份來源覆核說成收件或發布完成。
