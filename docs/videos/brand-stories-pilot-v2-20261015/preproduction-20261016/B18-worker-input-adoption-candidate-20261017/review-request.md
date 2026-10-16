# B18 新資料列的獨立覆核請求

此稿是**待審候選**，不可把舊 `episodes/reviews/B18.json` 或上一版完整分鏡的離線審讀當成新 row 的收據。審查者請重新從確切父版和本候選比對：

1. 先驗 `verification.json` 的父版 manifest SHA、`B18.json` 和 `claim-coverage.json` SHA，再執行 `node build.mjs --check`；比對目前 `episodes/B18.json`，確認舊來源／敘事確實已過期，且本候選沒有改動既有 row／review／`stories.json`。
2. 逐章讀最終父版的 85 景、88 句，核對新 row 的六章 point、logline、takeaway、十筆 `must_verify` 是否準確代表實際口播。不可只因 schema 通過就給史料 PASS。全部 65 筆 `UNCHECKED` 原景／原來源及 42／23 的對位數字應可從父版重算；索引 9／11 是未口播背景，不得默默視為已查核。另對比 `remapped-chapters/` 與父版六章：只有 19 個 `claim.fact` 索引改動，`series-adoption.json` 只把 `plan` 換成本候選 row 的 beats，場景、旁白、來源和 `composeStory` 結果都不可改。
3. 特別重新打開[法院 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)理由第 8 頁 466–474 行、第 10 頁 574–578 行，將第 579776 號的登錄和 1972 年期滿與 [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的 1978 年寫法分開；不要把後者重新包裝成法院同一項權利的年份，也不要把法院與發明協會不同的「全國知名度」判斷混成定論。法院文件是 PDF，正式工人的頁面讀取器可能只交回 `supports` 而非 PDF 正文；請獨立判定法院日期主張是否需在新 review 標 `reviewer_only`，並核對 checker 實際看見的段落或 PLAN 標記。此候選沒有自作該判定。
4. 核對[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的撲克牌／名片來源界線、後場直線送盤與元祿首店的分離；[石野年表](https://www.ishino-group.com/history/)的 1980 旁通、1986 ㄇ字型與[石野集團介紹](https://www.ishino-group.com/group/)的 1971／1974 給茶年份差異；[機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)的 1985 年機器和另外保存的板片。
5. 若新 row 真的通過獨立來源與全文覆核，另製**只綁此 canonical story SHA** 的正式 `reviews/B18.json`；在可用的匯入編譯器上以同一個 A01/B18 cohort 重編譯，做非寫入 dry-run。那一階段仍需核對既有 B18 episode 是否已 started、工人是否會使用已審六章，以及成本與主機鎖。這份請求本身不是批准匯入、模型查核或媒體生成。

需要 HOLD 時，請指明 `B18.json` 的欄位、對應的 `claim-coverage.json` 行及來源段落，勿直接修改父版分鏡或舊審稿收據。
