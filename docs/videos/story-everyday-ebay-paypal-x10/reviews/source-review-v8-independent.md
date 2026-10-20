# eBay／PayPal X10 v8｜獨立來源差異審查

**PASS，限 v7→v8 的來源差異。** 2026-10-20；v7 的完整來源審查見 [v7](source-review-v7-independent.md)，此收據不代替兩位 v8 敘事盲讀或實際音訊驗收。v8 主片 `video.json` SHA-256 `3f20fbcf4fa8143b21b227ea12a629c39d6ec2929999c95bffde67a57392a73d`，`shorts.json` SHA-256 `dde413de5eac00fd74c6ab6b200a60f92e05bc454ce29de7ce6453552ea17ff1`。

| 判定 | 差異 | 原件與界線 |
| --- | --- | --- |
| PASS | `x100413` 新問 eBay 在合作條款下能否自己接手部分付款；`x100414` 說 merchant-of-record 角色受限，`x100415` 說合約允許小範圍測試。 | [2015 Operating Agreement, Article XIV §14.1](https://www.sec.gov/Archives/edgar/data/1065088/000119312515257121/d93601dex101.htm) 有限制及條件式例外：生效第三週年後，eBay 在至多兩個測試法域且受 GMV 上限約束，可作 merchant-of-record 測試。下載 HTML SHA-256 `3d409931d8b78bb017d31ff8e6dd4db6b36ae0b33062c6f8a7257117c9433841`。旁白沒有說五年完全禁止開發、也沒有推定 2018 上線實際依哪個例外運作。剪接時須保留 `x100414`–`x100415` 的限定，不可單取問句。 |
| PASS | `x100512` 將上句 US$2bn 定為累計處理的交易額，沒有第二次唸數字，也未當作 eBay 收入。 | [eBay FY2019 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508820000006/ebay201910-k.htm) `Our Marketplace` 說自 2018 年起為近 25,000 賣家累計處理超過 US$2bn 付款；下載 HTML SHA-256 `21ee7cbf2c49eacf58253d5c631915c3ec924f538b5fa6f59e12612d45fe029d`。這是付款流量，不是收入。 |
| PASS | Short 1 現取 `x100407`–`x100408`，分拆後仍合作，合約也有鼓勵 eBay 支援 PayPal 的條款。 | [PayPal 2015 Form 10 information statement](https://www.sec.gov/Archives/edgar/data/1633917/000119312515237232/d877527dex991.htm) 的 Commercial Agreements 與 Operating Agreement 段落，以及上列 2015 合約，支持「合作延續／有誘因」；沒有推成付款方式市占或實際使用量。分股而非現金出售的主題已由 v7 來源審查覆核。 |
| PASS | Short 2 把 why-hook 換成「誰管付款」，先交代 2015 合作，再以 FY2019／FY2020 遷移與 `x100703` 的 2021 年底平台交易付款管理直接回答。 | [eBay FY2022 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508823000006/ebay-20221231.htm) `Our Marketplace` 明寫 `Since late 2021, eBay has managed payments for all transactions on our Marketplace platforms`；下載 HTML SHA-256 `e6e819f329c187299f25b4d983be60866341495ff276591260c955fd8abf897b`。此句說 eBay 管理平台交易的付款，沒有說 PayPal 不再可作付款方式。2020 經營好處仍保留公司主張及非實測限定。 |
| PASS | 三筆 loop metadata payoff IDs 改到實際有答案的行；主片時間估算與鏡頭數變動。 | metadata 未新增歷史事實；來源綁定的逐句實質主張沒有因此改變。實際時間仍須 TTS 驗收。 |

來源差異無待修事實錯誤；敘事是否重述、Shorts 是否獨立成立由 v8 兩位盲讀另審。
