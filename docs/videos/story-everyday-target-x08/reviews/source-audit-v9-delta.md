# X08 Target Canada v9｜章標差異來源複核

**PASS。** `video.json` v9 的完整 SHA-256 為 `0cc79a86deeed1831fea40ebc26bf5266d55c74d927ab1af1ae663331db8dc94`；`shorts.json` 仍為 `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543`。

v9 唯一 `video.json` 差異是第六章 `chapter` 由「停止營運後，退出費用入帳」改成「**退出決定後，費用如何入帳**」。只把此欄位還原，整份檔案的 SHA-256 精確回到 v8 的 `2d72b7357bd72d84033037bb4b8aadb382e06371f9d5f4a529a6c31f4e8b6ffe`；因此旁白、數字卡、鏡頭與其他章標皆未變。`drafts/narration.md`、`script.md` 顯示相同新章標，`line-source-matrix.md` 與 `script.md` 亦載正確 v9 雜湊。

[T14 FY2014 Form 10-K，Note 6](https://www.sec.gov/Archives/edgar/data/27419/000002741915000012/tgt-20150131x10k.htm) 原文稱董事會於 **2015-01-14** `approved a plan to discontinue operating stores in Canada`；加拿大子公司翌日申請保護，門店在清算中仍開放。該年報列截至 **2015-01-31** 的 FY2014 第四季退出費用 US$5,105m。[T15Q1 Form 10-Q，Note 2](https://www.sec.gov/Archives/edgar/data/27419/000002741915000018/tgt-20150502x10xq.htm) 才說 `As of May 2, 2015, all stores have been closed.` 兩份原始 HTML 的 SHA-256 分別是 `bcba1e1012631dcfd52c8ffec17805d9f316f3b214cee166111479c872049005`、`5916ab69c69940ee20cddd0fc43e7cf2aac187d80294242c0dce038299610a85`，與 `source-notes.md` 相符。

新章標把「後」明確接到**退出決定**，符合上述先決定、後於 FY2014 Q4 列帳的順序；「如何入帳」是問句，未暗示 US$5,105m 全是現金，也沒有把入帳時間放在全店關閉之後。v8 唯一來源時間問題已解決；其餘 v8 逐項判定維持通過。
