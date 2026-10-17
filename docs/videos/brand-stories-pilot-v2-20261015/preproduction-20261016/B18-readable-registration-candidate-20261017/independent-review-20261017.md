# B18 可讀登記事實分源：獨立審查

- 審查人：Codex `/root/b18_e6_independent`；日期：2026-10-17。
- 結論：**PASS，僅限隔離候選的企劃資料列**。沒有發現此精確修正仍需處理的 P1／P2。這不核准正式匯入、逐景查核、媒體製作或上架。
- 候選 `B18.json` SHA-256：`21122b7db5f97957ca89399b249a02e47e0b4465003e3653efbbf422b6043e9d`；canonical story SHA-256：`da692f3833f3d5448e3ec7603f0549a4f9b1afe2828c00aa8ee657618584a5e1`。收據 `reviews/B18.json` 只對後者有效。
- 父候選 `sha256.json` SHA-256：`87d9ee2fafe2b579dad9dd496391e31d5db585054abf89da380edfd345b959f4`。作者本版 `sha256.json` 的十個產物、`README.md`、`build.mjs` 雜湊均與實檔相符；本審查收據與報告另存，不屬作者 manifest。

## 史料與修正

1. [發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)第 34 行明記 **1962 年以白石名義登記實用新案「コンベヤ附調理食台」**，直接支持 `engine-s049/e6` 及 `engine-s050/e7`。同頁第 43 行的 **1978 年**期滿版本與特定權利的法院認定不一致；完整權利鏈尚未釐清，本片不口播該年。
2. [日本法院官方判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)的**判決理由**第 8 頁第 466–469 行認定第 **579776** 號於昭和 37 年 12 月 6 日（1962 年）登錄；第 10 頁第 574–578 行認定**該項**權利於昭和 47 年（1972 年）期滿，之後有多家企業「原告とは無関係に」經營使用輸送帶餐台的壽司店。新 `must_verify[4]` 只收後兩項判決結論、只引 `sources[3]`，未推論所有權利同時到期或其他店只因期滿而開。
3. [J-Net21 訪談](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)第 1232–1234 行用「特許」記述另一個 **1978 年**版本及警告、加盟店獨立；不能代替法院對第 579776 號的認定。[日本機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)第 14–20 行仍區分 1985 年機器與另存早期板片。我也打開了石野集團介紹頁；石野年表本次讀取失敗，因此未計入 `sources_opened`，但其企劃內容與先前六源獨立審查版本逐欄相同。本次成功打開五個來源：S0、S1、S2、S3、S5。

## 精確範圍

- `must_verify` 仍是格式允許的 **10 條**；只有第 4 條從混合「1962 年登記／1972 年期滿」縮成法院的特定權利期滿與後續經營認定。十條來源索引、各來源網址／出版社／種類／檢查日與 caveat 均未改。
- `e6` 為 `source:2, fact:null`，`e7` 從 `source:3, fact:4` 改為 `source:2, fact:null`。`h7`、`t7`、`t8` 保持 `source:3, fact:4`；`claim-coverage.json` 的第 4 條 scene 清單及兩筆直讀來源映射同步更新。所有 **65 筆場景主張仍為 `UNCHECKED`**，不能因本企劃審查視為通過。
- 六章仍為 85 景、88 句，旁白與畫面內容逐欄未改。舊 `episodes/reviews/B18.json` 綁前版 canonical SHA，對本版失效；正式來源讀取器把 PDF 判為非文字頁，因此僅 `must_verify[4]` 留在 `reviewer_only:[4]`。正式工人還須逐章核對可讀 S2 的 e6／e7、完成其他關卡並由獨立編輯審實稿。
