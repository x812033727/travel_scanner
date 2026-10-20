# Beats X04｜手工詞庫啟動前獨立來源複核

審查者：`beats-bootstrap-source-final`。審查對象是 `video.json` SHA-256 `53483afc8fbc219ee6b10a356f29f8a5202319888a2f7e47a3e048de8a544ae5`，六章、67 句及 13 張資料卡。**來源判定：PASS**，限此版文字與資料卡；不核准語音、插畫、片頭片尾或成片。

我將現稿和前一版 `77bd76e62f280b16e5dd5f33f72cc0723ddba5176fad76373c3c3335c08c9a39` 逐欄比較：只變更 `x040104`、`x040311` 的旁白文字，其餘場景、資料卡、提示詞、五份來源 URL 和 65 句文字均未變。現行[逐句矩陣](../source-matrix.md) 67／67 個 ID 唯一、逐字對應現稿，13 張卡與上一版相同；未變部分沿用[前版獨立來源審查](verify-1.md)的逐來源判定，沒有把舊收據冒充現稿核准。

| 修訂句 | 原始申報的可核對文字 | 本輪判定 |
| --- | --- | --- |
| `x040104`：「偏偏**同年第三季**的報表，數位音樂銷售往下走；它和這筆收購有沒有關係？」 | [Apple 2014 Q3 Form 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/d740164d10q.htm) Item 2 明寫 “third quarter and first nine months of **2014**” 的 iTunes Store 淨銷售增長受 App 銷售帶動，並稱 “partially offset by a decline in sales of digital music”。本機原件快取 `/tmp/apple-2014-q3.html` SHA-256 `b29836df9752e3edb1f149c6679406093dadf1b3790c10a251b82467b7447b70`，文字約在第 10155 行。 | PASS。「同年」承接開場 `x040101` 的 2014 年，不再把報表誤聽成 2015 年；下降只指數位音樂銷售，沒有說整個商店營收下降。因果是提問，`x040212` 隨後明答申報沒有把它寫成收購直接原因。 |
| `x040311`：「交易在**七月三十一日完成**；**下一份年報**把兩家公司一起寫成已完成的收購。」 | [Apple FY2014 Form 10-K](https://www.sec.gov/Archives/edgar/data/320193/000119312514383437/d783162d10k.htm) Note 4 原文：“On July 31, 2014, the Company completed the acquisitions of Beats Music, LLC ... and Beats Electronics, LLC ... (collectively, ‘Beats’).” 本機原件快取 `/tmp/apple-2014-10k.html` SHA-256 `9ffd3710a0428a7a7589c0f7c131dca05f6d6c69319b2f5a72f962a5fb84a98e`，文字約在第 11372 行；2014 Q3 10-Q 截至 6 月底仍把完成交易寫成待監管同意的預期。 | PASS。分號分開交易日期與其後年報的記載，不會把年報發布誤放在 7 月 31 日；同句只說兩家公司合計完成，沒有虛構分項價格。 |

現稿仍把 **US$2.6 billion** 限於兩家公司合計會計收購對價，2014 數位音樂銷售下降限於同期背景，2015／2016 的 Apple Music 與 Beats 產品分類限於公司描述；未由此推算單品收入、交易唯一動機、服務程式碼或訂戶移轉。此複核使用保留在本機的原始 SEC HTML 快取與前版審查記錄，**未重新宣稱本輪 HTTP 連線成功**。資料卡和未變的 65 句原件對照維持前版判定；若現稿再變更，須重新綁定來源證據。
