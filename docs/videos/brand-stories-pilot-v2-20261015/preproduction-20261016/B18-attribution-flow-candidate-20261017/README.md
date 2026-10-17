# B18 來源承接口播隔離候選

**狀態：HOLD；未採用。** 本版針對[上一層來源歸屬候選](../B18-attributed-narration-candidate-20261017/README.md)的[獨立複核 P2](../B18-attributed-narration-candidate-20261017/INDEPENDENT-ATTRIBUTION-REVIEW.md)提出兩句最小改寫。上一版連續三景以 `J-Net21` 開頭，可追溯但像在讀書目。本版保留 `i5` 的明確「依 J-Net21 的記載」，讓相鄰 `i6` 以「同一篇報導」、`i7` 以「報導還記載」指回它。句子全文和父版雜湊見 [`flow-map.json`](flow-map.json)。

`i5/i6/i7` 是連續三景；這樣每句的來源都可從可聽見的前文定位，不再重複唸三次英數名稱。`i3` 前一景仍明講中小企業基盤整備機構，`i4` 本景仍明講發明協會；[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)的撲克牌說法與[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的名片說法仍分開。本版未更動來源卡、其餘四句、row、系列企劃或 65 筆主張的文字／來源／fact／判定。

`B18.json` 與父版**位元組相同**，canonical story SHA 仍是 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`；舊 active row review 對它仍然失效。完整逐字稿 I03/I04 必須依新兩句同步並獨立重審，不能因故事 hash 不變就沿用舊稿的聽眾或劇本收據。父版獨立審查也只對父版六句有效，仍是歷史 HOLD。

`build.mjs --write` 只在本目錄寫候選；`--check` 逐位元組重算。它釘住父版 manifest 與獨立複核，檢查唯一的 `idea` 兩句差異、明確來源承接、85 景／88 句／65 筆 `UNCHECKED`、全部 source/fact 路由與法院 PDF 專屬來源不變。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-attribution-flow-candidate-20261017/build.mjs --write
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-attribution-flow-candidate-20261017/build.mjs --check
```

**待驗收：** 獨立聽眾仍須從上一景一路朗讀這三句，確認「同一篇報導」及「報導還記載」沒有歧義，並在完整版查核中逐句核對。`J-Net21` 的台灣口音 TTS 發音尚未試聽；後續旁白／`check-audio` 不可略過。正式採用還需要以最後企劃版本重做 row review、保留法院 PDF `reviewer_only:[4]`、65 筆正式 worker verifier，以及 listener／敘事／畫面／CC／成片關卡。本包不改 active B18、主機、PR 或任務票；沒有付費、媒體或上傳。
