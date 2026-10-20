# X19 Uber｜SEC 原件與口徑邊界

2026-10-20 逐份 HTTP GET 讀取 Uber 自行提交 SEC 的 HTML 附件。位元組與 SHA-256 對下載原件計算，不是文字轉檔的雜湊。下列每份均小於 3 MiB，主片要用的事實均位於抽出文字的前約 16,000 字內；作者查核尚待另一位審稿者對定稿獨立重做。

| 代碼 | SEC 原件 | HTTP bytes | 原始 bytes SHA-256 | 成片可支持的範圍 |
| --- | --- | ---: | --- | --- |
| S1 | [2020 Q1 財報公告，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000154315120000020/uberq120earningspressr.htm) | 548,307 | `62ae39afd36f2ae05259806367d6f2501791dba93239d674ae82ff8f03611a9c` | 2020 Q1 Rides 訂單額 US$10.874bn、Eats US$4.683bn，對上年同季分別 −5%／+52%（報告幣別）；載客司機 App 的跨接功能在 **Q1 季內**改進，四月美加近 40% 當月活躍載客司機亦接 Eats 工作，兩時點不能合一。推出 Direct／Connect 等配送服務；在一些市場免新餐廳啟用費並加快加入流程。5 月初公告又稱退出八個虧損 Eats 市場，此項屬 Recent Developments，非 Q1 季內決策。不是疫情時才發明 Eats。 |
| S2 | [2020 Q2 財報公告，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000154315120000027/uberq220earningspressr.htm) | 829,739 | `56a2a1a93d26227b18c8cd66f3beab747322f745806821ea493c1a30b8427a7a` | 2019 Q2 Mobility／Delivery 訂單額 US$12.188bn／US$3.386bn；2020 Q2 換成 US$3.046bn／US$6.961bn，按報告幣別同比 −75%／+106%，2020 Q2 外送已反超；2020 Q2 起 Rides 改名 Mobility、Eats 改名 Delivery，分類變更註腳不可忽略。總訂單額 US$10.224bn、營收 US$2.241bn、GAAP 淨損 US$1.775bn、Mobility 調整後 EBITDA +US$50m、Delivery −US$232m、集團調整後 EBITDA −US$837m。六月 Eats 合作餐廳逾 50 萬；七月宣布擬以約 US$2.65bn 全股票交易收購 Postmates，當時尚未完成。 |
| S3 | [2020-07-06 Postmates 收購說明會逐字稿，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000412/e20423_ex99-1.htm) | 53,755 | `09dce79d280c8487d15f21143e7ef6831718dd633b159bdbe8a59d3e937a5c44` | 執行長說已簽約以約 US$2.65bn 全股票交易收購 Postmates；公司期待結合餐飲、商家與配送網，屬交易當時的預期，不是後來獲利的證明。這個宣布發生在六月季度結束後，不能倒因為六月反超的原因。 |
| S3a | [2020-07-06 Postmates 收購 8-K 封面／附註](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000412/e20423_uber-8k.htm) | 37,477 | `6a039db45bf31d666d2223c1a5d31324110639b9f89413ffcb788463321fdc74` | Date of Report 明列 2020-07-06，並連結收購說明會附件。供逐句口播「七月六日」作工人可讀日期原件。 |
| S4 | [2020 Q3 財報公告，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000162828020015770/uberq320earningspressr.htm) | 512,044 | `fe864c5d4a2776e3346ca9b17334e03b41f35ebcb4bd3f382fe5f555640d933e` | Q3 Mobility／Delivery 訂單額 US$5.905bn／US$8.550bn；Mobility 對 Q2 恢復約 94%，但仍同比 −53%（按報告幣別）；Delivery 同比 +134%，在 Postmates 完成交割之前仍較大。Delivery 調整後 EBITDA −US$183m、Mobility +US$245m。活躍合作餐廳同比增加逾 70%，公司新推出店家自家網站接單、交由 Uber Eats 配送的選項；九月雜貨配送已進入十多個國家，包含台灣。iOS 版 Uber App 當時陸續把 Eats 服務入口放在叫車旁。上述動作與交易額同時發生，不能量化其個別貢獻。 |
| S5 | [2020-12-01 完成 Postmates 收購公告，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_ex99-1.htm) | 8,683 | `11f3911af6a22458d48c478cb704d53369c524d454a557f7308e232111788ab4` | 全股票交易完成，美國業務開始整合；公告當時說兩個消費者 App 繼續分開運作，但背後商家與配送網會結合。只能說整合開始，不能說已在 2020 年 12 月完成或造成之前的訂單額反超。 |
| S5a | [2020-12-01 完成交割 8-K 封面／附註](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_uber-8k.htm) | 33,735 | `4b58ef2b356ae9c39f2fd2cac21a39a6c02ead8a0b1e5e378a4753dd236f2170` | Date of Report 明列 2020-12-01，內文寫當日發布完成收購公告；供逐句口播「十二月一日」作工人可讀日期原件。 |
| S6 | [2021 Q2 財報公告，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000154315121000035/uberq221earningspressrelea.htm) | 499,870 | `79a8914e82146c35228fa643b152219ff263b7e942e7725e9513c5ecd039d975` | Mobility／Delivery 訂單額 US$8.6bn／US$12.9bn；Mobility 同比大幅回升，但外送仍高。公司說 Postmates App 大致整合、近 500 萬消費者、16 萬配送員、逾 2.5 萬商家轉移；這是公司聲明，不能等同完成每個用戶遷移。Delivery 調整後 EBITDA −US$161m，仍為負。活躍商家逾 75 萬；美國活躍餐廳逾六成提供自取。美國雜貨、便利品、酒類等非餐廳配送的**六月 Gross Bookings**較 2020 年 12 月近三倍；這是新配送類別的月度比較，不是全部 Delivery 同比或收購效果。公司稱同時用 Mobility 和 Delivery 的消費者貢獻全平台近半 Gross Bookings；此非收購單獨效果。 |
| S7 | [2021 Q4／全年財報公告，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000154315122000004/uberq421earningspressrelea.htm) | 520,384 | `afba881d480d8d8ab8a3974c1887cf87d471f5cfc489f24c1dfa2ba5f20b3f06` | Q4 Mobility／Delivery 訂單額 US$11.340bn／US$13.444bn，報告幣別同比 +67%／+34%；Delivery 調整後 EBITDA +US$25m，是**單季部門非 GAAP 指標**，不能推定全年或公司 GAAP 都已由外送盈利。 |
| S8 | [2022 Q4／全年財報公告，8-K exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1543151/000154315123000004/uberq422earningspressrelea.htm) | 583,069 | `0deb0103252070de3283d03b1f76659794d9f6de824984bdce70c76467321579` | Q4 Mobility 訂單額 US$14.894bn，Delivery US$14.315bn；報告幣別同比 +31%／+6%，兩者都成長，這一季載客再次高過外送。**同一季度的 Segment Adjusted EBITDA**，Mobility +US$1.012bn，Delivery +US$241m，分別為十點一二億與二點四一億美元，均為正數；這不等於全公司 GAAP 正式淨利。不可宣稱這是重新超越的第一個季度，除非另查 Q1–Q3。 |

## 說法限制

- 主問句的「超過」專指 **Gross Bookings／平台訂單額**，不是 Uber 確認的營收，更不是利潤。S2 同季總訂單額 US$10.224bn 與 GAAP 營收 US$2.241bn 已顯示兩者不是同一欄。
- 比較都用來源表格的報告幣別數字；「固定匯率」同比另列，不能把 −75%／+106% 和 −73%／+113% 拼成同一組。
- 2020 Q2 季報把 Rides／Eats 改名 Mobility／Delivery；2019 對照值已按報告相同欄位呈現。不要寫成兩個全新的業務。
- 疫情與居家令是 Uber 同期描述的需求背景；訂單額分岔不能證明單一政策、司機轉派或 Postmates 收購各自貢獻多少。Postmates 七月簽約、十二月完成，均晚於六月季度。
- Segment Adjusted EBITDA 是公司定義的非 GAAP 部門尺度；Delivery 訂單額領先時仍可能在這個尺度虧損。GAAP 公司淨利又可能含股權重估。片中需每次點出尺度及季度，不把營運結果寫成收購效果。
- 開場路邊司機停車接餐袋是匿名概念示意，並非來源記載的特定人物或某趟真實派單；它只引入 S1 已記載的司機端轉接功能與四月跨接統計。2022 Q4 兩部門指標同為正，也只能說那一季的部門非 GAAP 尺度，不推成全年或公司正式淨利。
- 只用概念插畫呈現匿名司機、無標誌車、餐袋、手機與空白報表；不重建某個真實司機的一天，也不畫 Uber、Eats、Postmates 標誌、真人長相、可讀畫面或特定 App 介面。精確數字由後製排字。
