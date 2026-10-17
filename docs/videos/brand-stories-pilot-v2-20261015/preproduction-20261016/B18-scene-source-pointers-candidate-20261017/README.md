# B18 四筆逐景來源指標修正候選

**狀態：離線候選，HOLD。** 只修正 `e1`、`h5`、`i1`、`i5` 的逐景 `source`，均改指向既有 `sources[0]` J-Net21。這四筆的 `fact` 指標已允許來源 0；其餘 61 筆逐景主張、全部 85 景／88 句、10 筆企劃事實、企劃資料列與審稿收據均不變。65 筆逐景判定仍全是 `UNCHECKED`。

父版是 [`B18-readable-registration-candidate-20261017`](../B18-readable-registration-candidate-20261017/README.md)，其 `sha256.json` SHA-256 為 `1838bc925f6647776803129c177c286ac0493f8a0aaeee8ecc1aae8d02364044`。建置器會逐檔核對父版 manifest、既有本機企劃資料列與收據，並驗證只有這四個來源指標有變；不修改父版或本機正式輸入。

| 主張／場景 | 父版來源 1 或 2 的缺口 | 來源 0 的直接支持 |
| --- | --- | --- |
| `e1`／`engine-s041` | [日本機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)記 1958 年 4 月布施市首店，未記「近鐵布施站附近」。 | [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)「町工場の経営者が協力」段明記首店在近鐵布施站附近。 |
| `h5`／`hook-s004` | [發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)只記轉角順暢通過是難題，未直接記盤子「卡住」。 | J-Net21 同段記轉角輸送帶壅塞、盤子掉落。 |
| `i1`／`idea-s024` | 同上，發明協會沒有「帶子擠在一起、盤子可能掉下來」的機械細節。 | J-Net21 同段直接描述該細節。 |
| `i5`／`idea-s031` | 發明協會記扇形靈感及實現，但未直接描述「一片片扇形板子」的構造。 | J-Net21 同段記組合扇形部件，形成後稱「ウロコ」的輸送帶板。 |

法院專屬的 `sources[3]`／`must_verify[4]`／`h7`、`t7`、`t8` 完全不變；可讀的 1962 年登記 `e6`、`e7` 仍指發明協會 `sources[2]`，沒有把法院 PDF 的 `reviewer_only` 判斷擴大。企劃資料列和其既有獨立審稿收據逐位元組相同，因此**只就同一企劃資料列**仍可核對既有 row review；先前對逐景來源映射的獨立審讀不自動核准這四筆新指標，正式工人 verifier 仍須逐景查核。

在儲存庫根目錄執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-scene-source-pointers-candidate-20261017/build.mjs --write
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-scene-source-pointers-candidate-20261017/build.mjs --check
```

`delta.json` 記四筆前後來源與受影響檔案的確切雜湊；`verification.json` 記結構與 row review 檢查結果；`sha256.json` 綁定完整候選。`--check` 是離線、唯讀重算，不能替代獨立史料審查、正式 worker 的查核、匯入核准、費用授權或站主成片驗收。本候選不呼叫主機或付費供應商，也沒有配音、插圖、CC、MP4 或 YouTube 上傳。

採用前須由另一位審稿者重開上列官方來源並覆核四筆精確差異；再以核准的章稿 manifest 更新相應工人輸入、重跑逐章 verifier／listener／narrative 與後續媒體關卡。不可把舊逐景 PASS 或此機械檢查寫成新的審稿收據。
