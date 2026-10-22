# C13 Victorinox｜作者定向修訂收據（待獨立重審）

**狀態：作者 v2 交稿，不授予逐句來源、逐鏡、盲讀、站主或付費 PASS。** 2026-10-23（Asia/Taipei）；作者 `codex-c13-script`；同一個 [draft PR #1693](https://github.com/x812033727/travel_scanner/pull/1693)。

## 已採用輸入與本版輸出

| 檔案 | SHA-256 |
| --- | --- |
| `treatment.md`（站主已採用，未改） | `A4A47F06F52490B4044267405445F31AC31EF7FB2C19575D59511D5BE0C57F20` |
| `source-matrix.md`（站主已採用，未改） | `295A7793DE618FEF714FA530F78592527EF77E82BAA38EE5594745B8386641D1` |
| `script.md` | `FC538ED72ED024CF3F832D9CD1232C674C9C26F31039E06A3C762EADDEB25E10` |
| `script-source-notes.md` | `DE87D4F65F50B608C977A1B25A3321FA7D2C9CE8861CC78AD8987492DB5CF043` |
| `visual-plan.md` | `E6AEEDE4D4CC5573E9C6C6C74684378BC10E84FAD7F387960C3AFB0D6112A303` |
| `visual-plan.json` | `9BFE558EFCCFD7C37357A00973EE9D42007897990E861CEE65C510F73D84DA86` |

站主 Treatment 採用憑據為 `reviews/owner-treatment-adoption.md`；本次沒有改它、Treatment 或矩陣。以上四個作者檔案是新的獨立審查對象，舊審查雜湊不轉簽。

## 對獨立 HOLD 的定向回應

獨立 [script/visual 審查](independent-script-visual-review.md) 在舊作者稿上判 HOLD；本輪只修它指出的 T03 來源鏈、61 個插圖 prompt 和 E03／T03 字卡。

- T03 原稿聲稱不同訪談的人數有差異，但其行末只有 S6，無法支持跨訪談比較。現在 T02–T03 只轉述 [Elsener 本人多年後訪談](https://www.swissmadebusiness.com/brands/victorinox) 說的**部分員工暫借附近企業、約四到八個月、避免裁員**；不在旁白報精確員工人數，也不主張不同訪談衝突。T04 不把借調說成獲利量化證明；來源筆記另說明它不是當年人事名冊。
- E03 卡只顯示 [Swissinfo 2002/1/29 綜合報導](https://www.swissinfo.ch/eng/archive-banking-fintech/sales-blunted-at-victorinox/2511740) 所述的 2001 年第四季刀具跌幅；E02 口播仍另歸屬 1/25 訪談的十月幅度，兩個時間窗保持未定論。T03 卡只顯示「CEO 多年後回憶｜曾短期借調員工」。兩卡不再露 `S5`／`S10` 等內部代號或「不鎖定人數」這類編輯指令。
- 61 個插圖 prompt 均移除 `cute-mystery` 字樣，系列畫風只保留精確 `look: {"preset":"cute-mystery"}`；H01 也移除額外 `papercut` 風格詞。鏡頭仍是泛用概念插畫，沒有商標、真人肖像、品牌商品複製或 9/11／機場現場重建。

1989 北美手錶、1999 授權旅行用品均早於 2001；七月 30 日合營宣布早於事件、十一月營運在事件後。瑞士 Victorinox AG 與美國 SABI 分帳，2001 十月訪談與 Q4 綜合報導不合成一個數字，2002 年產品狀態分清；2005／2014／2017 後續事件不歸為同一個 9/11 因果。此輪未改這些來源邊界。

## 作者機械檢查與環境限制

- 六章 **75 句／75 鏡**，口播 **2,705 字元**（含標點與空格，不含來源碼）。暫排正文 **599 秒**、插圖 **490 秒＝81.8%**、14 張後製字卡、最長連卡 2、最長單鏡 12 秒；開場後 5 秒片頭，正文後 21 秒 v4 片尾，紙上全長 625 秒。最大標記鉤子間隔沿用原排程約 43 秒。**未配音；正文實際是否 ≥480 秒仍待 TTS。**
- 本輪本機結構核對 PASS：75 個唯一行 ID 與 JSON 同序，逐行有 S 來源標籤，61 幅插圖 prompt 無 `cute-mystery`，精確系列 `look.preset` 保留，兩張改動字卡不含內部代號／編輯指令。 `git diff --check` exit 0；提交前再核對暫存差異。
- `npm run check:tasks` **exit 1**，只因兩個已存在、未追蹤的 `tasks/open/2026-10-22-...treatment...md` ghost 檔與 `tasks/done` ID 重複；本任務不刪、不改、不暫存它們。此前 `npm run test:docs-videos` exit 1（131 pass、6 fail），工作樹缺 `node_modules`／`pinyin-pro`；本輪未重試或安裝，不宣稱全量測試通過。

請另一位代理針對**本版四個作者 SHA**重做 T02–T04 來源與 E03／T03 字卡、61 個 prompt 的獨立審查。兩位純旁白盲讀、念法／TTS 實測、圖片驗收、站主逐字稿／分鏡採用與整集付費報價仍是後續關卡；作者不自判 PASS。沒有付費生成、匯入、上傳、合併、發布或部署。
