# X08 Target Canada v8｜視覺與章標獨立來源查核

**總判定：FAIL。** 五句旁白及其歸因維持 v7 已通過的內容；v8 的第六章章標卻把 FY2014 Q4 已入帳的退出費用，讀起來放在加拿大門店停止營運／全數關閉之後。此時間暗示與 SEC 原件及影片自己的敘事次序衝突。其餘 v8 視覺修訂及來源對應通過。

## 版本鎖定與範圍

| 檔案 | 實算完整 SHA-256 |
| --- | --- |
| `video.json` v8 | `2d72b7357bd72d84033037bb4b8aadb382e06371f9d5f4a529a6c31f4e8b6ffe` |
| `shorts.json` | `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543` |

將 v8 `video.json` 的兩張數字卡標籤、三個章標及一個鏡頭提示這**六個非旁白欄位**暫時還原，所得完整 SHA-256 精確等於 v7 的 `ab4d99818ee51bfe9e81893c813caac56f33af68be5de5002844506a97bd7764`。因此旁白文字、語音欄位、其餘場景與數字均未變。`drafts/narration.md` 與 `line-source-matrix.md` 已把 `x0803a08` 的面積依據補列 **TC29**。

對照 [T13／Target FY2013 Form 10-K](https://www.sec.gov/Archives/edgar/data/27419/000002741914000014/tgt-20140201x10k.htm)、[T14Q1](https://www.sec.gov/Archives/edgar/data/27419/000002741914000018/a2014q1ex-99.htm)、[T14Q2](https://www.sec.gov/Archives/edgar/data/27419/000002741914000025/a2014q2ex-99.htm)、[T14Q3](https://www.sec.gov/Archives/edgar/data/27419/000002741914000033/a2014q3ex-99.htm)、[T14／Target FY2014 Form 10-K](https://www.sec.gov/Archives/edgar/data/27419/000002741915000012/tgt-20150131x10k.htm) 及 [T15Q1／FY2015 Q1 Form 10-Q](https://www.sec.gov/Archives/edgar/data/27419/000002741915000018/tgt-20150502x10xq.htm) 原件。讀取的原始 HTML SHA-256 依序為 `dbbdbee947bf108d0b4026a0ca4923a0df7a655cfbb27ee57b074e84f6b36225`、`cda825d969174a631e9eb9f66585574ff711989d20ddf68b0ab73de5817b5568`、`3428247c9bb33651ec70cbbf483872bb64af06bc003a56f498ef037765e98ff4`、`045ad1e81177229c378790af8ec5240a2776277c987caf0f8062d911214dca77`、`bcba1e1012631dcfd52c8ffec17805d9f316f3b214cee166111479c872049005`、`5916ab69c69940ee20cddd0fc43e7cf2aac187d80294242c0dce038299610a85`，與 `source-notes.md` 一致。

## v8 改動逐項判定

| 改動 | Yes/No | 依據及界線 |
| --- | --- | --- |
| `x080305` 數字卡標籤改為「毛利率；原因待揭曉」 | **Yes** | T13 MD&A 報加拿大部門 FY2013 毛利率 14.9%，隨後將其歸於 `clear excess inventory following lower than anticipated sales and supply chain start-up challenges`。卡片保留正確部門、財年、比率；暫緩透露原因是敘事提示，讓下一句及 `x080307` 說明兩項原因。 |
| 第四章章標改為「二〇一四年，Target 再調整加拿大營運」 | **Yes** | T14Q1 管理層稱調整團隊、投入資源；T14Q2 稱調整加拿大營運和商品組合；T14Q3 稱節慶前改營運、價格與品項。章標沒有預告後段同店銷售或虧損結果，也沒有把「調整」說成成功。 |
| 第五章章標改為「董事會批准停止加拿大營運」 | **Yes** | T14 Note 6 原文是 `our Board of Directors approved a plan to discontinue operating stores in Canada`，時間為 2015-01-14。應按「批准停止營運方案」理解，**不表示當天全部關店**；下一句及其後的清算／關店過程維持此界線。章標只先點出該章第一句的決議，未提前揭露後段會計答案。 |
| `x080512` 前的鏡頭改為封閉帳冊與關閉的店模型 | **Yes** | 封面遮住帳冊內容，不會提前把後章退出費用全說成現金或非現金。模型位於片中已交代「截至五月二日全店關閉」之後，也不暗示公告當日立即鎖門。這是象徵畫面，不能視為某家實際門店的紀錄。 |
| `x080601` 數字卡標籤改為「稅前退出費用；性質待揭曉」 | **Yes** | T14 Note 6 列 FY2014 Q4 加拿大 `pretax exit costs` US$5,105m，其中 US$4,766m 是 `Investment impairment on deconsolidation`；年報風險章明稱非現金減損。卡片數字、財年、稅前口徑正確，且在 `x080602`／`x080603` 前不揭露非現金答案。 |
| 第六章章標改為「停止營運後，退出費用入帳」 | **No** | T14 Note 6 明載董事會 **2015-01-14 批准停止營運方案**、2015-01-15 申請保護，`stores will remain open during the liquidation`；同份年報把 US$5,105m 列為截至 **2015-01-31 的 FY2014 第四季**退出費用。T15Q1 只說 `As of May 2, 2015, all stores have been closed.` 章五已敘述到全店關閉，再接「停止營運後，退出費用入帳」，自然讀法把記帳排在實際停業／全店關閉之後，錯置時間。建議章標改成「**退出決定後，費用如何入帳**」等指向 **決定** 而非門店已停業的中性說法；仍可保留非現金性質給後段揭曉。 |

修正第六章章標後，只需重新核對產生檔及其 SHA；本次 FAIL 不涉及五句旁白或 Shorts。
