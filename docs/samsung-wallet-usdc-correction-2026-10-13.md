# Samsung Wallet／USDC 已刊五語更正對照（2026-10-13）

## 對象與狀態

- Guide ID：`9e38d360-a0f7-4d5b-81c4-15af1224fcf2`
- Slug：`crypto-news-samsung-wallet-solana-usdc-20261008`
- 2026-10-13 以正式站 `/zh-TW/admin/guides` 逐語讀取後，zh-TW、en、zh-CN、ja、ko 原本都是草稿 v2／已發布 v2。
- 五語均已於 2026-10-13 由 Guide 編輯器逐語發布，後台重新切換語系讀回**草稿 v6／已發布 v6／修訂紀錄 `v6 · published`**；五語公開頁也逐頁讀回更正內容。v3 修正費用、託管、資格與裝置數；獨立初審指出另一處把 2025 年 Coinbase One 優惠的可觸及人數寫成實際服務人數，v4 逐語修正；v5 補存新來源查證日期；獨立覆核內容 PASS 後以 `expected_version=5` 發布成 v6。每語保留 Decrypt 來源，另增 Samsung 2026、Coinbase 2026、Solana 2026、Samsung 2025 四個一手來源；新增一手來源的查證日期均已讀回 2026-10-13。
- Guide 後台沒有適用已刊修訂的 AI judge；依既有 Guide 人工確認、發布原因與管理稽核流程發布，沒有使用新聞候選重試或付費重跑。管理稽核逐語有 `guide_article_published` 成功紀錄與此 Guide 的 locale 目標。

## 一手依據

1. [Samsung 美國新聞稿，2026-10-07](https://news.samsung.com/us/samsung-wallet-bring-stablecoin-access-eligible-galaxy-users-us/)：預計十月最後一週向合資格美國用戶推出；18 歲以上、Samsung 帳號、Android 13 以上相容 Galaxy 裝置，註冊、身分與生物辨識設定。8,200 萬指美國與 Samsung Wallet 相容的裝置，非已啟用人數。Samsung 不收轉至相容第三方 USDC 錢包的費用，收款錢包／交易所可能收費；轉至 60 多國合資格銀行帳戶另有依目的地和金額浮動的費用，確認前顯示。Bastion 提供託管與轉帳架構、Coinbase Prime Vault 擔任次級託管；用戶不用自行管理私鑰。
2. [Coinbase 公告，2026-10-08](https://www.coinbase.com/blog/coinbase-and-samsung-bring-usdc-to-samsung-wallet)：Coinbase 透過 Prime 提供 subcustody，Bastion 是合作的持牌託管與基礎設施方。
3. [Solana 基金會公告，2026-10-07](https://solana.com/news/samsung-wallet)：Solana 支援 Samsung Wallet／Samsung Pay 內的 USDC 跨境轉帳，預計十月最後一週開始；8,200 萬台是美國裝置規模。
4. [Decrypt 原報導，2026-10-08](https://decrypt.co/380377/samsung-wallet-taps-solana-for-usdc-transfers-on-82m-us-galaxy-devices)：原有報導來源，保留其事件與引言脈絡。轉帳費用及託管細節以 Samsung／Coinbase 的更具體一手公告更新。
5. [Samsung Coinbase One 優惠公告，2025-10-03](https://news.samsung.com/us/samsung-wallet-offers-users-special-access-coinbase-one)：美國 Samsung Wallet 用戶可申領 Coinbase One Standard 三個月免費訂閱；只限新訂戶。公告所說超過 7,500 萬美國 Galaxy 用戶是合作可觸及的規模，不能寫成實際申領、訂閱或使用服務的人數。

## 五語錯句與 v6 已刊修正

五個語系均修正搜尋摘要、重點摘要、事件段落、8,200 萬裝置段落、用戶影響段落、費用／託管表格、上線／資格／費用 FAQ，以及背景段落 6。簡中另修段落 8 的標點空格；日文、韓文另修標題與主圖替代文字的推出時態。表格從籠統「尚未說明」改為已公布資訊與仍待確認事項。

| 語系 | v2 公開版錯句（節錄） | v6 已刊版的關鍵修正 |
| --- | --- | --- |
| zh-TW |「費用與私鑰管理方式尚未說明」「用戶是否自行持有私鑰、轉帳費用」|「相容外部錢包轉帳 Samsung 不收費（收款端可能收費）；銀行轉帳費依目的地與金額變動；Bastion 託管、Coinbase 次級託管，用戶無須自行管理私鑰」|
| zh-CN |「费用与私钥管理方式尚未说明」「用户是否自行持有私钥、转账费用」|「向兼容外部钱包转账三星不收费（收款方可能收费）；银行转账费用随目的地和金额变化；Bastion 托管、Coinbase 次级托管，用户无需自行管理私钥」|
| en |“Fees and how private keys are handled have not been explained.” / “Whether users hold their own private keys; transfer fees”|“Samsung charges no fee for compatible external-wallet transfers, though recipients may; bank fees vary; Bastion provides custody and Coinbase sub-custody, so users need not manage private keys.”|
| ja |「手数料と秘密鍵の管理方法は明らかにされていない」「ユーザーが秘密鍵を自己保有するか、送金手数料」|「対応する外部ウォレットへの送金にSamsungの手数料はかからないが受取側は課金の可能性。銀行送金の手数料は送金先・金額で変動。Bastionが保管しCoinbaseが再委託先となり、秘密鍵の自己管理は不要」|
| ko |「수수료와 개인키 관리 방식은 아직 공개되지 않았다」「개인키 직접 보유 여부, 송금 수수료」|「호환되는 외부 지갑 송금에 삼성 수수료는 없으나 수취 측은 부과 가능. 은행 송금 수수료는 국가·금액별로 다름. Bastion이 수탁하고 Coinbase가 재수탁하며 개인키 직접 관리는 불필요」|

資格 FAQ 也從「上線時涵蓋 8,200 萬台」補成合資格美國居民的具體條件，並明確指出 8,200 萬是**與 Samsung Wallet 相容的美國裝置數**，不是已註冊、已開通或合資格用戶數。原本「目前的細節都來自 Solana 基金會」已改為援引 Samsung 10 月 7 日公告。所有上線時間仍寫「預計」，避免把尚未上線的功能寫成已開放。

獨立初審另找到五語背景段落 6 都把 2025 年的 Coinbase One 優惠寫成「服務 7,500 萬用戶」一類實際使用量。v5 保留 v4 依 Samsung 2025 年公告所做的修正：**美國 Samsung Wallet 用戶可申領三個月 Coinbase One Standard 優惠，僅限新訂戶**；不再宣稱實際服務或申領人數。簡中引言後的 `.”Decrypt` 補空格；日、韓標題與主圖替代文字改為「預定」語氣。

### v5 精確欄位稿：zh-TW

下列列出 v5 草稿經人工發布為 v6 的全部改動欄位完整新值；舊值留在該語系的 v2 revision，可逐欄比對。段落以編輯器位置編號，未列欄位沿用 v2。重點摘要中的「／」只標示後台文字框內的換行，不是稿件字元。五語來源清單另外新增 Samsung 2025 公告，查證日期為 2026-10-13。

1. 搜尋摘要：Samsung 與 Solana 宣布，合資格美國 Galaxy 用戶預計從 10 月最後一週起，可透過 Samsung Wallet 使用 USDC 跨境轉帳。約 8,200 萬是與 Samsung Wallet 相容的美國裝置數；Samsung 不收相容外部錢包轉帳費，銀行入帳另有可變費用。Bastion 託管、Coinbase 提供次級託管。
2. 重點摘要：Samsung 宣布，合資格美國 Galaxy 用戶預計自 10 月最後一週起，可在 Samsung Wallet 使用 Solana 上的 USDC 跨境轉帳。／約 8,200 萬是與 Samsung Wallet 相容的美國裝置數；相容外部錢包轉帳 Samsung 不收費，銀行轉帳另有可變費用，USDC 由 Bastion 與 Coinbase 分工託管。
3. 「發生了什麼事」第一段：Decrypt 於 2026 年 10 月 8 日報導，Solana 基金會宣布 Samsung Wallet 將支援美國用戶在 Solana 上傳送 Circle 發行的 USDC；Samsung 於 10 月 7 日公告，功能預計從 10 月最後一週起向合資格美國用戶推出。穩定幣是一種設計成價值與法定貨幣（例如美元）掛鉤的加密貨幣，USDC 是以美元計價的穩定幣。Solana 是記錄與處理轉帳的區塊鏈網路。
4. 「發生了什麼事」第二段：此功能也涵蓋 Samsung Pay，Solana 的基礎設施在幕後運作。Samsung 表示，美國約 8,200 萬台 Galaxy 裝置與 Samsung Wallet 相容；這是相容裝置數，不是已開通服務或符合資格的用戶數。錢包規劃內建法幣出入金，可將當地貨幣換成 USDC，或將 USDC 換回當地貨幣。
5. 「對一般用戶的實際影響」：依 Samsung 10 月 7 日公告，功能預計在 10 月最後一週向符合條件的美國用戶推出，目前尚未上線。轉至支援 USDC 的相容外部錢包或交易所帳戶，Samsung 不收轉帳費，但收款服務商可能收費；轉至 60 多國合資格銀行帳戶會有依目的地與金額而異的費用，送出前會顯示。用戶不必自行管理私鑰；Bastion 提供託管與跨境支付服務，Coinbase 透過 Prime Vault 擔任次級託管。實際可用國家、費用及到帳時間以 Samsung Wallet 內的提示為準。
6. 表格（`|` 分欄）：

   ```text
   項目|已公布|仍待確認
   上線時間|合資格美國用戶預計從 10 月最後一週起|其他市場的具體時程
   支援平台|Samsung Wallet 與 Samsung Pay；約 8,200 萬台美國 Galaxy 裝置與 Samsung Wallet 相容|實際註冊與使用人數
   技術|Solana 上的 USDC，內建法幣出入金|Circle 是否為此服務合作夥伴
   用戶層面|相容外部錢包轉帳 Samsung 不收費（收款端可能收費）；銀行轉帳費依目的地與金額變動；Bastion 託管、Coinbase 次級託管，用戶無須自行管理私鑰|各目的地具體費率與到帳時間
   ```

7. 上線 FAQ：Samsung 表示，功能預計自 2026 年 10 月最後一週起向合資格美國用戶推出；其他市場的時程尚未公布，將視當地法規而定。
8. 資格 FAQ：Samsung 公告限定合資格的美國居民：年滿 18 歲，持 Samsung 帳號，使用執行 Android 13 以上版本且與 Samsung Wallet 相容的 Galaxy 裝置，並完成帳戶註冊、身分驗證及生物辨識設定。約 8,200 萬是相容裝置數，並非已開通服務的人數。
9. 費用 FAQ：Samsung 不收轉至相容外部 USDC 錢包的手續費，但收款錢包或交易所可能收費。轉至 60 多國合資格銀行帳戶則有費用，依目的地和金額浮動；費用與預估到帳時間會在確認轉帳前顯示。用戶不必自行管理私鑰，Bastion 提供託管，Coinbase 透過 Prime Vault 擔任次級託管。
10. 背景段落 6：Decrypt 指出，Samsung 7 月在倫敦的 Galaxy Unpacked 活動上曾表示 Samsung Wallet 將加入原生穩定幣支援，並展示持有 USDC 的示意畫面，但當時未公布上線日期、發行方或區塊鏈。Decrypt 另指出，Samsung 於 2019 年推出 Galaxy 手機區塊鏈錢包。依 Samsung 2025 年 10 月 3 日公告，美國 Samsung Wallet 用戶可申領 Coinbase One Standard 三個月免費訂閱優惠，但僅限新訂戶。

### v5 精確欄位稿：en

1. Description: Samsung and Solana say eligible US Galaxy users are expected to send USDC across borders through Samsung Wallet from the last week of October. The 82 million figure counts US Galaxy devices compatible with Samsung Wallet, not active users. Samsung charges no fee for transfers to compatible external wallets; bank transfers carry variable fees. Bastion provides custody, with Coinbase Prime as sub-custodian.
2. Key points: Samsung says eligible US Galaxy users are expected to use Samsung Wallet for cross-border USDC transfers on Solana from the last week of October. / About 82 million US Galaxy devices are compatible with Samsung Wallet, but that is not the number of active users. Samsung charges no fee for compatible external-wallet transfers; bank transfers have variable fees, and Bastion and Coinbase provide custody.
3. What happened, first paragraph: Decrypt reported on October 8, 2026 that the Solana Foundation announced USDC transfers on Solana through Samsung Wallet. Samsung's October 7 announcement says the feature is expected to launch for eligible US users in the last week of October. A stablecoin is a cryptocurrency designed to track a fiat currency such as the US dollar; USDC is a dollar-denominated stablecoin issued by Circle. Solana is a blockchain network that records and processes transfers.
4. What happened, second paragraph: The feature also extends to Samsung Pay, with Solana infrastructure operating behind the scenes. Samsung says about 82 million US Galaxy devices are compatible with Samsung Wallet; that is a device count, not a count of registered or eligible users. Built-in fiat on- and off-ramps are intended to convert between USDC and local currency.
5. What it means for everyday users: Samsung's October 7 announcement says the feature is expected to launch for eligible US users in the last week of October; it is not live yet. Samsung does not charge for USDC transfers to compatible third-party wallets or exchange accounts, although the recipient provider may charge a fee. Transfers to eligible bank accounts in more than 60 countries carry fees that vary by destination and amount and are shown before confirmation. Users do not manage private keys themselves: Bastion provides custody and cross-border payment services, while Coinbase Prime Vault acts as sub-custodian. The app will show actual availability, fees and estimated delivery times.
6. Table:

   ```text
   Item|Announced|Still to confirm
   Launch timing|Expected for eligible US users in the last week of October|Specific timelines for other markets
   Supported platforms|Samsung Wallet and Samsung Pay; about 82 million US Galaxy devices are compatible with Samsung Wallet|Actual enrollment and usage
   Technology|USDC on Solana with built-in fiat on- and off-ramps|Whether Circle is a partner in this service
   User terms|Samsung charges no fee for compatible external-wallet transfers, though recipients may; bank fees vary; Bastion provides custody and Coinbase sub-custody, so users need not manage private keys|Specific fees and delivery times for each destination
   ```

7. Launch FAQ: Samsung expects to launch the feature for eligible US users in the last week of October 2026. It has not announced dates for other markets, which depend on local regulatory requirements.
8. Eligibility FAQ: Samsung says users must be eligible US residents aged 18 or older with a Samsung account, a Galaxy device compatible with Samsung Wallet running Android 13 or later, and completed registration, identity verification and biometric setup. About 82 million counts compatible US devices, not activated users.
9. Fee FAQ: Samsung does not charge for USDC transfers to compatible external wallets, though the recipient wallet or exchange may charge a fee. Transfers to eligible bank accounts in more than 60 countries carry fees that vary by destination and amount; fees and estimated delivery times are shown before confirmation. Users do not manage private keys themselves: Bastion provides custody and Coinbase Prime Vault is the sub-custodian.
10. Background paragraph 6: Decrypt noted that at the Galaxy Unpacked event in London in July, Samsung said Samsung Wallet would add native stablecoin support and showed a mock-up screen holding USDC, but it did not announce a launch date, issuer or blockchain at the time. Decrypt also noted that Samsung launched a blockchain wallet on Galaxy phones in 2019. Samsung's October 3, 2025 announcement said US Samsung Wallet users could claim a free three-month subscription to the Standard tier of Coinbase One, limited to new subscribers.

### v5 精確欄位稿：zh-CN

1. 搜索摘要：三星与 Solana 宣布，符合条件的美国 Galaxy 用户预计从 10 月最后一周起，可通过三星钱包（Samsung Wallet）使用 USDC 跨境转账。约 8,200 万是与 Samsung Wallet 兼容的美国设备数量，并非已开通用户数。三星不收向兼容外部钱包转账的费用，银行转账另有浮动费用；Bastion 提供托管，Coinbase 提供次级托管。
2. 重点摘要：三星宣布，符合条件的美国 Galaxy 用户预计从 10 月最后一周起，可在 Samsung Wallet 使用 Solana 上的 USDC 跨境转账。／约 8,200 万是与 Samsung Wallet 兼容的美国设备数量；向兼容外部钱包转账三星不收费，银行转账另有浮动费用，USDC 由 Bastion 与 Coinbase 分工托管。
3. 事件第一段：Decrypt 于 2026 年 10 月 8 日报道，Solana 基金会宣布 Samsung Wallet 将支持美国用户在 Solana 上发送 Circle 发行的 USDC；三星 10 月 7 日公告称，功能预计从 10 月最后一周起向符合条件的美国用户推出。稳定币是一种设计成价值与法定货币（例如美元）挂钩的加密货币，USDC 是以美元计价的稳定币。Solana 是记录和处理转账的区块链网络。
4. 事件第二段：该功能也涵盖 Samsung Pay，Solana 基础设施在幕后运行。三星表示，美国约 8,200 万台 Galaxy 设备与 Samsung Wallet 兼容；这是兼容设备数量，不是已注册或符合使用条件的用户数量。钱包计划内置法币出入金渠道，可将当地货币兑换成 USDC，或将 USDC 换回当地货币。
5. 用户影响段：根据三星 10 月 7 日的公告，该功能预计在 10 月最后一周向符合条件的美国用户推出，目前尚未上线。向支持 USDC 的兼容外部钱包或交易所账户转账，三星不收取转账费，但收款服务商可能收费；转入 60 多个国家的合资格银行账户则会收取因目的地和金额而异的费用，确认前会显示。用户无需自行管理私钥；Bastion 提供托管和跨境支付服务，Coinbase 通过 Prime Vault 担任次级托管。实际可用国家、费用和预计到账时间以 Samsung Wallet 内显示的信息为准。
6. 表格：

   ```text
   项目|已公布|仍待确认
   上线时间|符合条件的美国用户预计从 10 月最后一周起|其他市场的具体时间
   支持平台|Samsung Wallet 与 Samsung Pay；约 8,200 万台美国 Galaxy 设备与 Samsung Wallet 兼容|实际注册与使用人数
   技术|Solana 上的 USDC，内置法币出入金|Circle 是否为此服务的合作伙伴
   用户层面|向兼容外部钱包转账三星不收费（收款方可能收费）；银行转账费用随目的地和金额变化；Bastion 托管、Coinbase 次级托管，用户无需自行管理私钥|各目的地的具体费用和到账时间
   ```

7. 上线 FAQ：三星表示，该功能预计从 2026 年 10 月最后一周起向符合条件的美国用户推出；其他市场的时间尚未公布，并取决于当地监管要求。
8. 资格 FAQ：三星公告限定符合条件的美国居民：年满 18 岁，持有三星账户，使用运行 Android 13 或以上版本且与 Samsung Wallet 兼容的 Galaxy 设备，并完成账户注册、身份验证及生物识别设置。约 8,200 万是兼容设备数，并非已开通服务的人数。
9. 费用 FAQ：向兼容外部 USDC 钱包转账时，三星不收取手续费，但收款钱包或交易所可能收费。转入 60 多个国家的合资格银行账户则会收费，费用随目的地和金额变化；费用和预计到账时间会在确认转账前显示。用户无需自行管理私钥，Bastion 提供托管，Coinbase 通过 Prime Vault 担任次级托管。
10. 背景段落 6：Decrypt 指出，三星 7 月在伦敦的 Galaxy Unpacked 活动上曾表示 Samsung Wallet 将加入原生稳定币支持，并展示了持有 USDC 的示意画面，但当时未公布上线日期、发行方或区块链。Decrypt 另指出，三星于 2019 年推出 Galaxy 手机区块链钱包。三星 2025 年 10 月 3 日公告显示，美国 Samsung Wallet 用户可申领 Coinbase One Standard 三个月免费订阅优惠，但仅限新订户。
11. 引言段落 8：Solana 基金会总裁 Lily Liu 则表示：“Samsung's decision to work with Solana puts digital dollars into everyday life through one of the world's most trusted technology brands.” Decrypt 还指出，该基金会点名 PayPal 与 Western Union 为已使用 Solana 处理稳定币的企业。

### v5 精確欄位稿：ja

1. Description: SamsungとSolana財団によると、条件を満たす米国のGalaxyユーザーは、10月最終週からSamsung WalletでUSDCの国際送金を利用できる見込み。約8,200万台はSamsung Walletに対応する米国内の端末数で、利用者数ではない。対応する外部ウォレットへの送金にSamsungの手数料はかからないが、銀行口座への送金には変動手数料がある。資産はBastionとCoinbaseが保管を分担する。
2. Key points: Samsungは、条件を満たす米国のGalaxyユーザー向けに、10月最終週からSamsung WalletでSolana上のUSDC国際送金を提供する見込みだ。／約8,200万台はSamsung Walletに対応する米国内の端末数。対応する外部ウォレットへの送金にSamsungは手数料を課さず、銀行送金には変動手数料がある。保管はBastionとCoinbaseが分担する。
3. 事件第一段：Decryptは2026年10月8日、Solana財団がSamsung WalletでSolana上のUSDC送金を提供すると発表したと報じた。Samsungの10月7日の発表によると、機能は10月最終週から条件を満たす米国のユーザーに提供される予定。ステーブルコインは米ドルなどの法定通貨に価値が連動するよう設計された暗号資産で、USDCはCircleが発行するドル建てのステーブルコイン。Solanaは送金を記録・処理するブロックチェーンネットワークだ。
4. 事件第二段：この機能はSamsung Payにも対応し、Solanaの基盤は裏側で動作する。Samsungによると、米国内でSamsung Walletに対応するGalaxy端末は約8,200万台。これは対応端末数であり、登録済みまたは利用資格のあるユーザー数ではない。法定通貨の入出金手段によって、現地通貨とUSDCの交換も可能になる予定だ。
5. 利用者への影響：Samsungの10月7日の発表によると、機能は10月最終週から条件を満たす米国のユーザー向けに提供される予定で、現時点ではまだ始まっていない。対応する外部ウォレットや取引所口座へのUSDC送金についてSamsungは手数料を課さないが、受取側の事業者が課金する場合がある。60カ国超の対象銀行口座への送金には、送金先と金額に応じた手数料がかかり、確定前に表示される。利用者が秘密鍵を自分で管理する必要はない。Bastionが保管と国際送金の基盤を担い、CoinbaseはPrime Vaultを通じてサブカストディアンを務める。対象国、手数料、着金見込みはSamsung Wallet内の表示で確認する必要がある。
6. 表格：

   ```text
   項目|公表済み|なお確認が必要
   開始時期|条件を満たす米国ユーザー向けに10月最終週から提供予定|他の市場での具体的な開始時期
   対応環境|Samsung WalletとSamsung Pay。米国内の約8,200万台のGalaxy端末がSamsung Walletに対応|実際の登録・利用者数
   技術|Solana上のUSDC、法定通貨の入出金を内蔵|Circleがこのサービスの提携先かどうか
   利用者に関する条件|対応する外部ウォレットへの送金にSamsungの手数料はかからないが受取側は課金の可能性。銀行送金の手数料は送金先・金額で変動。Bastionが保管しCoinbaseが再委託先となり、秘密鍵の自己管理は不要|送金先ごとの具体的な手数料と着金時間
   ```

7. 上線 FAQ：Samsungによると、条件を満たす米国ユーザー向けに2026年10月最終週から提供される予定です。他の市場での開始時期は未発表で、各地の規制状況によります。
8. 資格 FAQ：Samsungによると、対象は18歳以上の条件を満たす米国居住者です。Samsungアカウントを持ち、Android 13以降を搭載したSamsung Wallet対応のGalaxy端末を使い、登録・本人確認・生体認証の設定を完了する必要があります。約8,200万台は対応端末数で、利用開始済みの人数ではありません。
9. 費用 FAQ：対応する外部ウォレットへのUSDC送金についてSamsungは手数料を課しませんが、受取側のウォレットや取引所が課金する場合があります。60カ国超の対象銀行口座への送金には、送金先と金額に応じた手数料がかかり、手数料と着金見込みは確定前に表示されます。利用者による秘密鍵の自己管理は不要で、Bastionが保管を担い、Coinbase Prime Vaultがサブカストディアンとなります。
10. 標題：Samsung Wallet、SolanaのUSDCによる国際送金に対応予定 対象の米国Galaxyユーザーは10月最終週から利用開始予定
11. 主圖替代文字：Samsung Wallet、SolanaのUSDCによる国際送金に対応予定 対象の米国Galaxyユーザーは10月最終週から利用開始予定
12. 背景段落 6：Decryptによると、Samsungは7月にロンドンで開いたGalaxy Unpackedで、Samsung Walletにネイティブのステーブルコイン対応を加えると述べ、USDCを保有するイメージ画面を披露した。ただし当時は、開始日、発行体、ブロックチェーンは公表されなかった。Decryptはまた、Samsungが2019年にGalaxyスマートフォン向けのブロックチェーンウォレットを投入したと指摘している。Samsungの2025年10月3日の発表によると、米国のSamsung WalletユーザーにはCoinbase One Standardを3カ月間無料で利用できる特典が案内され、対象は新規加入者に限られた。

### v5 精確欄位稿：ko

1. Description: 삼성과 솔라나 재단에 따르면 자격을 갖춘 미국 갤럭시 사용자는 10월 마지막 주부터 삼성 월렛에서 USDC로 해외 송금을 이용할 수 있을 전망이다. 8,200만 대는 삼성 월렛과 호환되는 미국 내 기기 수이지 실제 이용자 수가 아니다. 호환되는 외부 지갑으로 보낼 때 삼성은 수수료를 부과하지 않지만 은행 계좌 송금에는 변동 수수료가 있다. 자산은 Bastion과 Coinbase가 나눠 수탁한다.
2. Key points: 삼성은 자격을 갖춘 미국 갤럭시 사용자를 대상으로 10월 마지막 주부터 삼성 월렛에서 솔라나 기반 USDC 해외 송금을 제공할 예정이다.／8,200만 대는 삼성 월렛과 호환되는 미국 내 기기 수다. 호환되는 외부 지갑 송금에 삼성 수수료는 없지만 은행 송금에는 변동 수수료가 있으며, Bastion과 Coinbase가 자산 수탁을 맡는다.
3. 事件第一段：디크립트는 2026년 10월 8일 솔라나 재단이 삼성 월렛에서 솔라나 기반 USDC 송금을 지원한다고 발표했다고 보도했다. 삼성의 10월 7일 발표에 따르면 이 기능은 10월 마지막 주부터 자격을 갖춘 미국 사용자에게 제공될 예정이다. 스테이블코인은 미국 달러 같은 법정화폐에 가치가 연동되도록 설계된 암호화폐이며, USDC는 서클이 발행하는 달러 기준 스테이블코인이다. 솔라나는 송금을 기록하고 처리하는 블록체인 네트워크다.
4. 事件第二段：이 기능은 삼성페이에도 적용되며 솔라나 인프라는 배후에서 작동한다. 삼성에 따르면 미국에서 삼성 월렛과 호환되는 갤럭시 기기는 약 8,200만 대다. 이는 호환 기기 수이지 등록을 마쳤거나 이용 자격을 충족한 사람의 수가 아니다. 지갑에는 현지 통화와 USDC를 서로 바꿀 수 있는 법정화폐 입출금 경로가 내장될 예정이다.
5. 用戶影響段：삼성의 10월 7일 발표에 따르면 이 기능은 10월 마지막 주부터 자격을 갖춘 미국 사용자에게 제공될 예정이며 아직 출시되지 않았다. 호환되는 외부 지갑이나 거래소 계정으로 USDC를 보낼 때 삼성은 송금 수수료를 부과하지 않지만 수취 측 사업자는 수수료를 부과할 수 있다. 60개국이 넘는 국가의 대상 은행 계좌로 보내는 경우에는 국가와 금액에 따라 달라지는 수수료가 있으며 송금 확정 전에 표시된다. 사용자는 개인키를 직접 관리할 필요가 없다. Bastion이 수탁과 해외 송금 체계를 제공하고 Coinbase는 Prime Vault를 통해 재수탁을 맡는다. 실제 지원 국가, 수수료, 예상 도착 시간은 삼성 월렛 앱에서 확인해야 한다.
6. 表格：

   ```text
   항목|발표된 내용|추가 확인 필요
   출시 시기|자격을 갖춘 미국 사용자에게 10월 마지막 주부터 제공 예정|다른 시장의 구체적인 일정
   지원 환경|삼성 월렛과 삼성페이. 미국 내 약 8,200만 대의 갤럭시 기기가 삼성 월렛과 호환|실제 등록 및 이용자 수
   기술|솔라나 기반 USDC, 법정화폐 입출금 내장|서클이 이 서비스의 제휴사인지 여부
   이용자 조건|호환되는 외부 지갑 송금에 삼성 수수료는 없으나 수취 측은 부과 가능. 은행 송금 수수료는 국가·금액별로 다름. Bastion이 수탁하고 Coinbase가 재수탁하며 개인키 직접 관리는 불필요|국가별 구체적인 수수료와 도착 시간
   ```

7. 上線 FAQ：삼성은 자격을 갖춘 미국 사용자에게 2026년 10월 마지막 주부터 제공할 예정이라고 밝혔습니다. 다른 시장의 출시 일정은 공개되지 않았으며 현지 규제에 따라 달라집니다.
8. 資格 FAQ：삼성에 따르면 대상은 만 18세 이상의 자격을 갖춘 미국 거주자입니다. 삼성 계정과 Android 13 이상을 실행하는 삼성 월렛 호환 갤럭시 기기가 필요하며, 계정 등록·신원 확인·생체인증 설정을 완료해야 합니다. 약 8,200만 대는 호환 기기 수이지 서비스를 개통한 사람의 수가 아닙니다.
9. 費用 FAQ：호환되는 외부 지갑으로 USDC를 보낼 때 삼성은 수수료를 부과하지 않지만 수취 지갑이나 거래소는 수수료를 부과할 수 있습니다. 60개국이 넘는 국가의 대상 은행 계좌로 송금할 때는 국가와 금액에 따라 달라지는 수수료가 있으며, 수수료와 예상 도착 시간은 확정 전에 표시됩니다. 사용자는 개인키를 직접 관리할 필요가 없고 Bastion이 수탁, Coinbase Prime Vault가 재수탁을 맡습니다.
10. 標題：삼성 월렛, 솔라나 기반 USDC 해외 송금 지원 예정…대상 미국 갤럭시 사용자 10월 마지막 주부터 이용 예정
11. 主圖替代文字：삼성 월렛, 솔라나 기반 USDC 해외 송금 지원 예정…대상 미국 갤럭시 사용자 10월 마지막 주부터 이용 예정
12. 背景段落 6：디크립트는 삼성이 7월 런던에서 열린 갤럭시 언팩 행사에서 삼성 월렛 자체에 스테이블코인 기능을 기본으로 넣겠다고 밝히고 USDC를 보유한 예시 화면을 공개했지만, 당시에는 출시일, 발행사, 블록체인을 발표하지 않았다고 전했다. 디크립트는 삼성이 2019년 갤럭시 스마트폰용 블록체인 지갑을 선보였다고도 전했다. 삼성의 2025년 10월 3일 발표에 따르면 미국 삼성 월렛 사용자는 Coinbase One Standard 3개월 무료 구독 혜택을 신청할 수 있었으며, 신규 구독자에게만 적용됐다.

## 發布與讀回核對

1. 獨立審核者逐語檢查更正欄位、一手公告與原始 v2 revision；v4 正文 PASS。v5 只補存新來源查證日期，正文未變。
2. 後台沒有適用**已刊 Guide 修訂**的 AI judge；使用 Guide 既有人工發布與稽核流程。每語確認 `expected_version=5`，填寫更正原因、勾選人工確認，然後讀回 v6 已刊修訂。
3. 管理稽核於 2026-10-13 逐語顯示 `guide_article_published`、此 Guide ID 加語系及成功：zh-TW 16:59:19、en 17:01:15、zh-CN 17:02:16、ja 17:03:14、ko 17:04:01（台灣時間）。稽核詳情讀回更正原因：「更正既刊 Samsung Wallet／USDC 新聞：依 Samsung 2026-10-07 與 2025-10-03、Coinbase、Solana 官方公告修正費用、託管、資格、裝置數及 Coinbase One 優惠；五語獨立覆核通過。」
4. 五語公開頁逐頁讀回：描述／正文／表格的相容外部錢包轉帳由 Samsung 不收費、收款端可能收費、銀行入帳有可變費用；Bastion 託管、Coinbase 次級託管、用戶不自行管理私鑰；8,200 萬是相容裝置，18 歲以上合資格美國居民與註冊身分驗證條件；2025 Coinbase One 僅描述三個月 Standard 優惠且限新訂戶；日韓標題為預計推出。五語資格及費用 FAQ 均展開讀回；公開頁新增 Samsung 2025 來源與 2026-10-13 查證日期。

| 語系 | 已讀回公開頁 |
| --- | --- |
| zh-TW | https://mokaair.com/zh-TW/life/crypto-news-samsung-wallet-solana-usdc-20261008 |
| en | https://mokaair.com/en/life/crypto-news-samsung-wallet-solana-usdc-20261008 |
| zh-CN | https://mokaair.com/zh-CN/life/crypto-news-samsung-wallet-solana-usdc-20261008 |
| ja | https://mokaair.com/ja/life/crypto-news-samsung-wallet-solana-usdc-20261008 |
| ko | https://mokaair.com/ko/life/crypto-news-samsung-wallet-solana-usdc-20261008 |
