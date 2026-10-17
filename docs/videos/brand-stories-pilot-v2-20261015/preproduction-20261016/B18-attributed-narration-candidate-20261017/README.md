# B18 來源歸屬旁白隔離候選

**狀態：HOLD。** 本候選從 [`B18-corner-and-source-card-candidate-20261017`](../B18-corner-and-source-card-candidate-20261017/README.md) 的固定 manifest `03bcf39d…6543a9a` 衍生。父版的[獨立審查](../B18-corner-and-source-card-candidate-20261017/INDEPENDENT-ROW-SOURCE-REVIEW.md)指出 P2：`must_verify[3].attributed: true` 對應的六處工程旁白沒有說出來源。保留父版和審查作歷史 HOLD，不在原地覆寫。

本版不拆事實、不更動 65 筆 `UNCHECKED` 的來源或 fact 映射，也不碰法院 PDF 專屬的 `h7/t7/t8`。只將整筆 row 必查事實表明「據 J-Net21」；在 `h5/i1/i5/i6/i7/n7` 六處旁白直接點名 J-Net21。`i3` 前一景已完整說出中小企業基盤整備機構，`i4` 本景已說出發明協會，保留兩種互不合併的扇形靈感版本。新句與舊句逐一列在 [`attribution-map.json`](attribution-map.json)。

[J-Net21 原文](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)〈町工場の経営者が協力〉明寫轉角輸送帶壅塞與盤子掉落、約十年開發、孩子攤開撲克牌的記述、組合扇形部件做出稱作「ウロコ」的板片與 1957 年試作。[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)記名片扇形的另一說。這些是來源歸屬的口播草案，不是工人逐章 verifier 已確認。

**待聽感與發音審查：** `i5/i6/i7` 連續三景都直接唸 `J-Net21`，可追溯但可能聽起來重複；TTS 也可能把連字號與英數念錯。正式逐字稿審查須朗讀這三句並試音。若改為 `i5` 點名 J-Net21、`i6/i7` 稱「同一篇報導」等較順的寫法，審稿者必須確認每句的指向仍清楚，再同步修改逐景稿、完整逐字稿與 hash；本候選沒有先套用這種尚未驗收的簡稱。

`build.mjs --write` 僅在本目錄產出 row、系列投影、六章與查核資料；`--check` 重算並逐位元組比對。建置器先核父版 manifest、檔案與審查雜湊，反推檢查改動只落在指定一筆 row 事實與六句旁白，並核對 85 景、88 句、65 筆均為 `UNCHECKED`、全部來源路由不變。它也證明舊 row review 對新 canonical story hash 無效。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-attributed-narration-candidate-20261017/build.mjs --write
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-attributed-narration-candidate-20261017/build.mjs --check
```

新版完整逐字稿必須與這六句及新 row hash 對齊並獨立重審；舊版逐字稿、審稿和父版來源審查都不是此候選的通過收據。正式採用還要新 row 來源審核、65 筆正式逐景查核、listener／敘事／旁白／畫面／字幕／成片關卡。本候選不修改現用 B18、主機或 PR；沒有匯入、付費模型呼叫、成片或上傳。
