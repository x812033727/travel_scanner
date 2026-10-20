# X19 Uber v1｜獨立 SEC 來源查核

**來源票：HOLD（兩處日期錯置、結句因果需收窄）。** 本票只綁 `video.json` SHA-256 `0f1a2b9902b36fd9a050f96aa5321a1ddba67928cae6bf2bbff2aed63c9cf2c8` 與 `shorts.json` SHA-256 `5b53405aa140922ccf8e0543733133e9d11e4472ae33ce701d93b6ac7cefee2e`；不沿用作者的事實判定，也不評成片敘事。

2026-10-20 審稿者另外按發行人 SEC 網址 HTTP GET S1–S8 與日期封面 S3a／S5a，十份全回 200、全小於 3 MiB；下載原始位元組長度與 SHA-256 均與作者 `source-matrix.md` 一致。必要數字、公告與日期均在各原件抽出文字前 40,000 字內。

| 原件 | Bytes／原始 SHA-256 | 重核關鍵 |
| --- | --- | --- |
| [S1 Q1 2020 公告](https://www.sec.gov/Archives/edgar/data/1543151/000154315120000020/uberq120earningspressr.htm) | 548,307／`62ae39afd36f2ae05259806367d6f2501791dba93239d674ae82ff8f03611a9c` | Q1 改進司機 App；**四月**美加近四成活躍載客司機跨接 Eats；8 個市場退出在公告的 **Recent Developments／五月初**，非 Q1 決定。 |
| [S2 Q2 2020 公告](https://www.sec.gov/Archives/edgar/data/1543151/000154315120000027/uberq220earningspressr.htm) | 829,739／`56a2a1a93d26227b18c8cd66f3beab747322f745806821ea493c1a30b8427a7a` | Q2 Mobility/Delivery Gross Bookings US$3.046bn／US$6.961bn，2019 同季 US$12.188bn／US$3.386bn；報告幣別同比 −75%／+106%。全公司 Gross Bookings US$10.224bn、GAAP revenue US$2.241bn、GAAP net loss US$1.775bn；部門調整後 EBITDA +US$50m／−US$232m。 |
| [S3 七月收購說明會](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000412/e20423_ex99-1.htm) 與 [S3a 8-K 封面](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000412/e20423_uber-8k.htm) | 53,755／`09dce79d280c8487d15f21143e7ef6831718dd633b159bdbe8a59d3e937a5c44`；37,477／`6a039db45bf31d666d2223c1a5d31324110639b9f89413ffcb788463321fdc74` | 約 US$2.65bn 全股票**簽約**，封面日期 2020-07-06，晚於 Q2 結束。 |
| [S4 Q3 2020 公告](https://www.sec.gov/Archives/edgar/data/1543151/000162828020015770/uberq320earningspressr.htm) | 512,044／`fe864c5d4a2776e3346ca9b17334e03b41f35ebcb4bd3f382fe5f555640d933e` | Q3 Mobility/Delivery Gross Bookings US$5.905bn／US$8.550bn；部門調整後 EBITDA +US$245m／−US$183m；全公司 GAAP 淨損 US$1.089bn。 |
| [S5 交割公告](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_ex99-1.htm) 與 [S5a 8-K 封面](https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_uber-8k.htm) | 8,683／`11f3911af6a22458d48c478cb704d53369c524d454a557f7308e232111788ab4`；33,735／`4b58ef2b356ae9c39f2fd2cac21a39a6c02ead8a0b1e5e378a4753dd236f2170` | 全股票交易**完成**、美國業務**開始**整合，消費者 App 仍分開；封面日期 2020-12-01。 |
| [S6 Q2 2021 公告](https://www.sec.gov/Archives/edgar/data/1543151/000154315121000035/uberq221earningspressrelea.htm) | 499,870／`79a8914e82146c35228fa643b152219ff263b7e942e7725e9513c5ecd039d975` | Mobility/Delivery Gross Bookings US$8.6bn／US$12.9bn；Postmates App **大致**整合及遷移近 500 萬消費者、16 萬配送員、逾 2.5 萬商家是公司說法；Delivery adjusted EBITDA −US$161m，GAAP 公司淨利含大額股權重估。 |
| [S7 Q4 2021 公告](https://www.sec.gov/Archives/edgar/data/1543151/000154315122000004/uberq421earningspressrelea.htm) | 520,384／`afba881d480d8d8ab8a3974c1887cf87d471f5cfc489f24c1dfa2ba5f20b3f06` | Delivery/Mobility Gross Bookings US$13.444bn／US$11.340bn；Delivery adjusted EBITDA +US$25m 為**當季**，集團同尺度 +US$86m；GAAP 公司淨利 US$892m 含約 US$1.4bn 股權淨收益。 |
| [S8 Q4 2022 公告](https://www.sec.gov/Archives/edgar/data/1543151/000154315123000004/uberq422earningspressrelea.htm) | 583,069／`0deb0103252070de3283d03b1f76659794d9f6de824984bdce70c76467321579` | Mobility/Delivery Gross Bookings US$14.894bn／US$14.315bn；這一季載客再高於外送，未主張首次翻回。GAAP 公司淨利 US$595m 含約 US$756m 稅前股權重估淨利益。 |

必修三處：

1. `x190101`「二〇二〇年四月，優步**改了**載客司機的手機派單方式」把 S1 的兩個時間合成一日：文件說 App 改進在 **Q1 季內**，近四成跨接統計在**四月**。可改「二〇二〇年春，優步調整載客司機手機上的接單功能」，下句再明說四月跨接比例。
2. `x190215`「**第一季**公司還決定撤出八個虧損的外送市場」錯把 S1 的 **Recent Developments**（5 月 7 日公告稱本週一宣布）寫入 1–3 月。可改「五月初，公司還宣布撤出八個虧損的外送市場」；`x190217` 客服／招募縮編也只宜說「當時」，不要指定 Q1。
3. `x190625`「外送先超過載客，**是**乘客急縮、既有外送擴張與派單轉向相遇」把同時發生的因素寫成已拆算的因果。S1/S2 證實需求與派單同時變化，**未量化**派單改動對反超的獨立貢獻。可改「當時乘客訂單急縮、既有外送擴張，司機也開始跨接餐袋；各自推了多少無法拆算」。最後三句仍須先回答比較的是 Gross Bookings。

其餘抽核的比較與口徑有證據支持：`x190301–321` 反超指**訂單額**，沒有稱單量、公司營收或利潤反超；`x190401–503` 保持七月簽約與十二月完成兩個時間；`x190507–519` 把部門 adjusted EBITDA、公司 GAAP 淨利及股權重估分開；`x190601–616` Q4 2021 的部門正數只說該季，Q4 2022 的再次載客領先不冒稱首次。Short 1 沒把 Gross Bookings 等同收入／獲利；Short 2 依日期排清六月先反超、七月簽約、十二月交割，沒有倒置因果。

這是**完整原件**的事實票，不代替敘事雙盲、正式來源工人攝取、官方動畫、實際 TTS、插畫、CC、MP4、Shorts 成片或 YouTube 連結驗收。上述三處修正後須以新 JSON SHA 重審。
