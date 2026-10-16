# B18 worker 輸入資料列：獨立離線審查

2026-10-17，Codex `/root/b18_row_independent_review`。**結論：PASS_OFFLINE_ROW_AND_SOURCE；HOLD_IMPORT_AND_FORMAL_WORKER。** 我獨立讀完六章的 85 景／88 句、65 筆逐景主張及本候選的十筆代表性必查主張，重開六個來源，並執行本機結構與讀取檢查。這不是正式 worker 查核、`reviews/B18.json`、主機匯入或付費製作核准。

## 凍結版本與差異

| 項目 | SHA-256／結果 |
| --- | --- |
| 最終父版 `B18-claim-granularity-candidate-20261017/sha256.json` | `1016d3de91236af487eec891e256f43214d71a06ba806409084831f47584e198` |
| 本候選 `sha256.json` | `56d6602b844a5daa055c7a176ad7db739d5ee29150c22eacb89110006071c05a`，14 個列舉檔案逐一相符 |
| 新 `B18.json` | `b927121fb7e693954679270ea3ecdfb64ad7ce8307751b4c3310e74d33511728` |
| 新 canonical story | `29993db8333f26ea5df68c09137f0b0cae924056602e7c1e49a1dfb2cbb9c059` |
| `claim-coverage.json` | `7038930605ba1db2adc3b5f2e04ed6fdd9f730a5c9283d56e15b7dc961f5e298` |

獨立 JSON 物件比較：`series-adoption.json` 只把父版 `series.plan` 換成候選資料列的企劃欄位；六個 `remapped-chapters` 的全部 `scenes`、88 句旁白、`loops` 與 65 筆 claim 的 ID、景號、文字、來源及 `UNCHECKED` 原狀保留。只改 19 個 `claim.fact` 指標：`h6` 1 筆、`e2/e3` 2 筆、`t1/t2/t4/t5/t6/t10/t11/t12/t13/t16/t17/t18` 12 筆、`n2–n5` 4 筆。42 筆逐景主張映到新 row fact 且仍直引原來源，23 筆只直引原來源；原十三筆 fact 中曾被逐景引用的索引恰為 `0–8,10,12`，未引用的 `9`（舊市場數字）與 `11`（給茶年份）沒有被偷偷算作已查。十筆新必查主張與六章內容相符。`composeStory` 前後一致是 `build.mjs --check` 的離線結果，不是實際成片相同的證據。

`node build.mjs --check`、`node manifest.mjs --check` 都退出 0；直接以 `plan.mjs` 重算 `storyProblems=[]`，舊 `episodes/reviews/B18.json` 對新 canonical SHA 明確回 `the story changed after this review`。用後端 `check_story_file` 在記憶體載入既有 A01 與此 B18，`problems=[]`、`refused=[]`、兩列順序為 1/2。既有 `episodes/B18.json`、`episodes/reviews/B18.json`、`stories.json` 均無工作樹差異；沒有編出可匯入檔。

## 來源與敘事邊界

- [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)支持 1947 立食店、一盤四貫 20 日圓、1948 吹田啤酒廠、撲克牌版本、1957 試作、1958 年 4 月首店、萬博與部分加盟店獨立；它把 1962 年的權利稱作特許、期滿寫 1978。候選把這當來源版本，沒有說啤酒公司已確定。20 日圓與首店 50 日圓分開。
- [發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)支持名片版本、首店約 20 坪與 50 日圓、1962 實用新案、萬博受表彰、後來約 240 家，以及後場製作、直線送盤的**後來其他業者**。其 1978 敘述不能覆蓋法院對特定第 579776 號的判讀。旁白中的全國知名度明確歸屬發明協會，未說法院也確認「元祿」標識全國著名。
- [日本法院判決理由](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)第 8 頁 466–474 行認定第 579776 號實用新案於 1962 年登錄，另認定原告道頓堀店在 1962 年 4 月開設；第 10 頁 574–578 行認定**該權利於 1972 年期滿**，其後有與原告無關的業者。候選沒有把 J-Net21 的 1960 道頓堀第二店版本混成法院認定，也沒有把其他店全歸因於一個到期日。
- [石野官方年表](https://www.ishino-group.com/history/)記 1980 年販售大型店旁通裝置、1986 年出現 ㄇ字型路線店；[集團介紹](https://www.ishino-group.com/group/)寫 1974 年給茶整合／開發，與年表所述 1971 年已販售整合設備衝突。給茶年份只留 caveat，沒有口播；後場直線、旁通與 ㄇ字也沒有說成同一店或同一台機器的改裝。
- [日本機械學會第 112 號](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)明確列一台 1985 年製、2021 年仍在元祿堺東店使用的輸送機，以及元祿產業**另外保存**的早期板片。候選沒有說成 1958 年首店原機。

本機以正式企劃讀取器 `fetchSources` 讀六頁：S0、S1、S2、S4、S5 各為 HTTP 200 且可讀文字；S3 法院 PDF 是 HTTP 200、`not a text page (application/pdf)`。`fetchProblems` 在此十筆 row 與 `reviewer_only=[]` 下回空陣列：F4/F5 同時引可讀的 S0／S2 及不可讀的 S3，依現有驗證規則**不可**把它們列為「全部來源不可讀」的 `reviewer_only`。正式工人只會從 S3 取得企劃 `supports`，而非判決正文；日後新審稿收據須明記我人工開啟 PDF 的上述行號，並讓正式查核保留 1972／1978 的歸屬。這項讀取限制是正式 worker 審核時要看的風險，不是 PDF 已被工人核讀的證據。

另有非口播的剩餘風險：候選 `names` 仍沿用舊企劃的「朝日啤酒／Asahi」，但查閱的來源未確定當年是哪一家啤酒工廠。`must_verify[1]` 與 `chapters.origin.point` 已禁止指名；若後續作者仍寫出該公司，必須刪去或另找可靠來源，不能因它在 `names` 就視作史實。

**下一關：**針對此 canonical story SHA 另產獨立 `reviews/B18.json`，在可用匯入編譯器中重編 A01/B18 同一 cohort、做唯讀／非寫入預檢，確認正式機既有 B18 狀態、作者六章採用路徑及成本閘門。所有 65 筆逐景主張仍為 `UNCHECKED`；正式逐章查核、聽眾審稿、十三題敘事、TTS 片長、圖像、CC、成片與站主觀看一項也未由此審查完成。
