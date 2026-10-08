# 機場英文 60 集：獨立旅運事實查核

查核日期：2026-10-08。查核者：`airport_claims_review`，與逐集撰稿代理不同。

**此輪完成文字事實查核；不是語音、成片或發布核准。** 全 60 集分成 23 組可查核主張，使用 24 份實際取得的官方頁面。找出的 3 處安全表述已由作者修改，查核者已重讀英文及四語譯文，沒有待套用的事實修正。

## 覆核範圍與版本

- 已讀 Day02–60 全部原稿的對話與 177 題測驗，以及 Day01 的 36 筆英文對話／複習列與 UI（包含 3 題測驗）；原稿共 744 筆英文列。
- 已讀重製 Day01 的取句、全 60 集共 300 句新增英文引導，以及 Day28／30／31 的 3 句安全修訂和繁中、簡中、日文、韓文譯文。
- [claims-review.json](claims-review.json) 保存 60 份原稿 SHA-256、60 份重製 lesson SHA-256，以及只含本次覆核英文內容的獨立摘要。作者後續改動文字必須再核；純狀態欄位修改可另比對英文內容摘要，不能直接假定全文 hash 不變。
- 未宣稱完整母語人工審稿、逐句音訊轉寫、影片實看、CC 對時、測驗重播的最終媒體驗證或任何 YouTube 核准。測驗句 ID 與選播正確性由課程覆核另行驗收。

## 已完成的三項文字修正

| Day／句 ID | 問題與已採用英文 | 依據 |
| --- | --- | --- |
| 28／B02 | 原稿只請旅客詢問規則；已明確要求托運前取出行動電源：`Remove it before the bag is checked. Ask the agent how to carry it safely in the cabin.` | [FAA：Lithium Batteries](https://www.faa.gov/hazmat/packsafe/lithium-batteries) |
| 30／A06 | 原稿只以大小與走道是否暢通判斷；已補上機組／座位許可：`Yes, if the crew permits it and it fits fully under the seat without blocking the aisle.` | [UK CAA：Stowage of baggage and cargo](https://regulatorylibrary.caa.co.uk/965-2012/Content/Document%20Structure/04%20CAT/3%20AMC/AMC1%20CAT%20OP%20MPA%20160%20Stowage.htm)、[IATA：Passenger Baggage Rules](https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/) |
| 31／B02 | 原稿把解開與調整連成同一動作；已分清示範安全帶的解開與調緊：`Lift the metal buckle to release it. To tighten it, fasten it and pull the loose end of the strap.` | [Air Cambodia：Travel advise](https://www.aircambodia.com/en/travel-advise) |

以上各句四語譯文已同步，語意保留「先取出」「須獲允許」「先扣好再調緊」。這些改動不表示所有機型的安全帶相同；Day31 引導已要求依當班飛機的安全示範操作。

## 情境數字與真實規則分開處理

所有航班號碼、登機門、櫃檯、步行分鐘數、超重公斤數、飯店與個人行程，是虛構聽力練習。對話中的免費接駁車、餐點、座位可用性等，也是該例子的設定；不能拿來當成真實機場保證，也不應替虛構 B32 登機門捏造班表來源。

每集 metadata／系列 profile 應有清楚的情境說明，例如：

> These are fictional listening scenarios. Check your airline, airport and destination's current requirements for your own journey.

國家／機場／航空公司的官方頁用來確認保留條件的實用建議，不能擴張成全球一體適用的規則。這套稿子沒有新增通用 100 ml 限制、免費行李重量、免簽資格、補償金額、最短轉機時間或保證送達期限。

## 逐項覆核

| Claim ID | 範圍 | 判定及官方依據 |
| --- | --- | --- |
| AE-C01 全系列虛構情境 | Day01–60 | 虛構情境，不偽裝成外部事實 |
| AE-C02 行李額度與登機門托運 | 08、09、28 | 原條件式表述有據；[iata-bags](https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/) |
| AE-C03 行李收據與舊條碼 | 08 | 原條件式表述有據；[gatwick-bags](https://www.gatwickairport.com/passenger-guides/preparing-hold-baggage.html)、[lufthansa-bags](https://www.lufthansa.com/au/en/prepare-for-your-trip/baggage/baggage-irregularities/faq-baggage-delay) |
| AE-C04 安檢依當地與通道程序 | 11、12、13、14、15、16、44 | 原條件式表述有據；[uk-liquids-detail](https://www.gov.uk/hand-luggage-restrictions/liquids)、[heathrow-connect](https://www.heathrow.com/connecting-flights) |
| AE-C05 液體藥物與必要藥物 | 14、28 | 原條件式表述有據；[uk-liquid-medicine](https://www.gov.uk/hand-luggage-restrictions/essential-medicines-and-medical-equipment)、[ba-allergies](https://www.britishairways.com/content/information/travel-assistance/medical-conditions-and-pregnancy) |
| AE-C06 登機組別、協助與嬰兒車 | 10、21、22、23、59 | 原條件式表述有據；[ba-boarding](https://www.britishairways.com/content/information/checking-in-and-boarding/boarding)、[aa-boarding](https://www.aa.com/web/i18n/travel-info/boarding-process.html) |
| AE-C07 登機截止早於起飛 | 10、26 | 原條件式表述有據；[aa-boarding](https://www.aa.com/web/i18n/travel-info/boarding-process.html) |
| AE-C08 托運前移除行動電源 | 28 | 已修正並覆核；[faa-batteries](https://www.faa.gov/hazmat/packsafe/lithium-batteries) |
| AE-C09 座位下方收納須獲允許 | 30 | 已修正並覆核；[caa-stowage](https://regulatorylibrary.caa.co.uk/965-2012/Content/Document%20Structure/04%20CAT/3%20AMC/AMC1%20CAT%20OP%20MPA%20160%20Stowage.htm)、[iata-bags](https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/) |
| AE-C10 安全示範與最近出口 | 31 | 原條件式表述有據；[caa-cabin](https://www.caa.co.uk/air-passengers/about-your-trip/cabin-safety/) |
| AE-C11 安全帶解開與調緊 | 31 | 已修正並覆核；[cambodia-belt](https://www.aircambodia.com/en/travel-advise) |
| AE-C12 安全帶、亂流與行李櫃 | 30、32、35、38、40 | 原條件式表述有據；[faa-turbulence](https://www.faa.gov/travelers/fly_safe/turbulence)、[caa-cabin](https://www.caa.co.uk/air-passengers/about-your-trip/cabin-safety/)、[jal-turbulence](https://www.jal.co.jp/jp/en/dom/boarding_attention/sudden-shake/) |
| AE-C13 電子裝置收納／過熱 | 32、40 | 原條件式表述有據；[caa-cabin](https://www.caa.co.uk/air-passengers/about-your-trip/cabin-safety/)、[faa-devices](https://www.faa.gov/hazmat/packsafe/portable-electronic-devices-with-batteries)、[cambodia-belt](https://www.aircambodia.com/en/travel-advise) |
| AE-C14 手機掉入座椅 | 32 | 原條件式表述有據；[ttcaa-safety](https://caa.gov.tt/safety-security-2/cabin-safety/passenger-information/) |
| AE-C15 食物過敏與交叉接觸 | 20、34、36 | 原條件式表述有據；[ba-allergies](https://www.britishairways.com/content/information/travel-assistance/medical-conditions-and-pregnancy) |
| AE-C16 身體不適時向機組求助 | 39 | 原條件式表述有據；[ttcaa-safety](https://caa.gov.tt/safety-security-2/cabin-safety/passenger-information/)、[ba-allergies](https://www.britishairways.com/content/information/travel-assistance/medical-conditions-and-pregnancy) |
| AE-C17 轉機動線與重新托運 | 08、41、43 | 原條件式表述有據；[heathrow-connect](https://www.heathrow.com/connecting-flights)、[dot-baggage](https://www.transportation.gov/lost-delayed-or-damaged-baggage) |
| AE-C18 轉機免稅液體封袋 | 44 | 原條件式表述有據；[uk-liquids-detail](https://www.gov.uk/hand-luggage-restrictions/liquids) |
| AE-C19 延誤、錯過轉機與取消 | 25、45、46、58 | 原條件式表述有據；[canada-disruption](https://protection-passager-passenger.otc-cta.gc.ca/en/when-an-issue-happens/flight-delays-and-cancellations) |
| AE-C20 入境問答與真實旅程 | 38、47、48、49、50、60 | 原條件式表述有據；[uk-visit](https://www.gov.uk/standard-visitor)、[uk-border](https://www.gov.uk/uk-border-control) |
| AE-C21 行李延誤、損壞與配送 | 08、28、43、51、52、53、54、55、60 | 原條件式表述有據；[dot-baggage](https://www.transportation.gov/lost-delayed-or-damaged-baggage)、[iata-bags](https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/)、[ba-report-bags](https://www.britishairways.com/content/en/ca/information/baggage-essentials/lost-and-damaged-baggage/reporting-baggage-problems)、[lufthansa-bags](https://www.lufthansa.com/au/en/prepare-for-your-trip/baggage/baggage-irregularities/faq-baggage-delay) |
| AE-C22 海關申報 | 56 | 原條件式表述有據；[uk-goods](https://www.gov.uk/bringing-goods-into-uk-personal-use/when-to-declare-goods)、[uk-border](https://www.gov.uk/uk-border-control) |
| AE-C23 機場正式計程車排班處 | 57 | 原條件式表述有據；[heathrow-taxi](https://www.heathrow.com/transport-and-directions/by-taxi-or-mini-cab) |

各項確切句 ID、英文主張、短引文或支持摘要、適用限制，以及修訂前後用語，均在 JSON 中逐筆保存。沒有用單一的「全部通過」取代個別證據。

幾項容易誤讀的界線：

- Day14／44：英國各機場的液體程序已有差異；保留「詢問此通道／此機場」正確。密封免稅袋與收據不能保證所有轉機安檢皆接受。
- Day32／40：繫好安全帶與依機組指示有官方支持。Day40 是機長預告亂流的情境；不是教觀眾在已劇烈搖晃時穿越客艙。JAL 的官方說明另外區分突然亂流且人已離座時應立即穩住身體。
- Day36／39：提供求助與溝通用語，沒有診斷、劑量或自行治療步驟。配方標籤不等於保證沒有交叉接觸。
- Day41／43：直掛行李不必然免領；也不是所有轉機都一定要領。Heathrow 與美國入境案例支持先看行程／當地流程的寫法。
- Day46／58：請航空公司確認方案不等於放棄法定權利；不能把「航空公司政策」解讀成可以取代適用法律。
- Day47–50／60：練習如實回答自己的旅遊目的與行程，虛構答案不保證獲准入境。
- Day52–55：行李延誤不等於永久遺失；原行李收據與問題通報編號也不同。已核對官方追蹤、保留單據、更新聯絡地址與保留損壞行李的說明。

## 官方來源取得紀錄

下列頁面於查核日以指定 User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 實際 GET，HTTP 200。JSON 保存實際回應 SHA-256；HTML 可含動態欄位，摘要僅表示取得的版本，不保證下一次請求相同。

- `faa-turbulence`：[Turbulence: Staying Safe | Federal Aviation Administration](https://www.faa.gov/travelers/fly_safe/turbulence)，確認日期 2026-10-08。
- `faa-devices`：[PackSafe - Portable Electronic Devices Containing Batteries | Federal Aviation Administration](https://www.faa.gov/hazmat/packsafe/portable-electronic-devices-with-batteries)，確認日期 2026-10-08。
- `faa-batteries`：[PackSafe - Lithium Batteries | Federal Aviation Administration](https://www.faa.gov/hazmat/packsafe/lithium-batteries)，確認日期 2026-10-08。
- `uk-liquid-medicine`：[Hand luggage restrictions at UK airports: Medicines, medical equipment and dietary requirements - GOV.UK](https://www.gov.uk/hand-luggage-restrictions/essential-medicines-and-medical-equipment)，確認日期 2026-10-08。
- `uk-liquids-detail`：[Hand luggage restrictions at UK airports: Liquids - GOV.UK](https://www.gov.uk/hand-luggage-restrictions/liquids)，確認日期 2026-10-08。
- `caa-cabin`：[Cabin safety | UK Civil Aviation Authority](https://www.caa.co.uk/air-passengers/about-your-trip/cabin-safety/)，確認日期 2026-10-08。
- `ttcaa-safety`：[Passenger Information – Trinidad and Tobago Civil Aviation Authority](https://caa.gov.tt/safety-security-2/cabin-safety/passenger-information/)，確認日期 2026-10-08。
- `cambodia-belt`：[Travel advise - Air Cambodia - Proudly The National Flag Carrier](https://www.aircambodia.com/en/travel-advise)，確認日期 2026-10-08。
- `ba-allergies`：[Medical conditions and pregnancy | Information | British Airways](https://www.britishairways.com/content/information/travel-assistance/medical-conditions-and-pregnancy)，確認日期 2026-10-08。
- `heathrow-connect`：[Connecting flights | Heathrow](https://www.heathrow.com/connecting-flights)，確認日期 2026-10-08。
- `dot-baggage`：[Lost, Delayed, or Damaged Baggage | US Department of Transportation](https://www.transportation.gov/lost-delayed-or-damaged-baggage)，確認日期 2026-10-08。
- `uk-visit`：[Visit the UK as a Standard Visitor: Overview - GOV.UK](https://www.gov.uk/standard-visitor)，確認日期 2026-10-08。
- `uk-border`：[Entering the UK: Overview - GOV.UK](https://www.gov.uk/uk-border-control)，確認日期 2026-10-08。
- `uk-goods`：[Bringing goods into the UK for personal use: When to declare goods to UK customs - GOV.UK](https://www.gov.uk/bringing-goods-into-uk-personal-use/when-to-declare-goods)，確認日期 2026-10-08。
- `caa-stowage`：[AMC1 CAT.OP.MPA.160 Stowage of baggage and cargo](https://regulatorylibrary.caa.co.uk/965-2012/Content/Document%20Structure/04%20CAT/3%20AMC/AMC1%20CAT%20OP%20MPA%20160%20Stowage.htm)，確認日期 2026-10-08。
- `jal-turbulence`：[JAL | In case of Sudden Turbulence](https://www.jal.co.jp/jp/en/dom/boarding_attention/sudden-shake/)，確認日期 2026-10-08。
- `iata-bags`：[IATA - Passenger Baggage Rules](https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/)，確認日期 2026-10-08。
- `heathrow-taxi`：[By taxi or mini cab | Heathrow](https://www.heathrow.com/transport-and-directions/by-taxi-or-mini-cab)，確認日期 2026-10-08。
- `ba-boarding`：[Boarding | Information | British Airways](https://www.britishairways.com/content/information/checking-in-and-boarding/boarding)，確認日期 2026-10-08。
- `gatwick-bags`：[Preparing Hold Baggage | London Gatwick Airport](https://www.gatwickairport.com/passenger-guides/preparing-hold-baggage.html)，確認日期 2026-10-08。
- `canada-disruption`：[Flight delays and cancellations - Air Passenger Protection](https://protection-passager-passenger.otc-cta.gc.ca/en/when-an-issue-happens/flight-delays-and-cancellations)，確認日期 2026-10-08。
- `aa-boarding`：[Boarding groups and boarding process | American Airlines](https://www.aa.com/web/i18n/travel-info/boarding-process.html)，確認日期 2026-10-08。
- `ba-report-bags`：[Reporting and tracking baggage | Information | British Airways](https://www.britishairways.com/content/en/ca/information/baggage-essentials/lost-and-damaged-baggage/reporting-baggage-problems)，確認日期 2026-10-08。
- `lufthansa-bags`：[Frequently asked questions about delayed baggage | Lufthansa](https://www.lufthansa.com/au/en/prepare-for-your-trip/baggage/baggage-irregularities/faq-baggage-delay)，確認日期 2026-10-08。

TSA／CBP 指定頁被拒絕（403），CASA 直連失敗（503），部分猜測的 EASA／DOT 舊網址是 404，CAA 舊路徑轉到總覽。這些失敗或無關頁沒有作為已取得的支持證據；改用可取得的相應官方來源。搜尋服務僅用來找官方網址，沒有把搜尋摘要冒充已讀全文。

## 後續使用

可依此資料生成各集 `claims.md`／`verify-1.md`，但生成器應保留原 Claim ID、來源與情境限制，並綁定當前稿件內容。若新稿增加數字、權利、醫療／安全指令，須重新查核新增主張。正式音訊、成片、字幕與發布關卡仍須各自完成。

## Day01 四句擴充：獨立補充查核（2026-10-08T16:31:27.528832+00:00）

本查核者 `airport_claims_review` 實際讀過新增 A07／A08／B09／B10 的英文及 16 段四語譯文，並逐物件比對先前 14 段對話、三題測驗與 evidence_ids、五組 guides、標題、claims 和 sources；上述既有內容都未改動。修正後 adaptation note 準確記載 A 八段、B 十段。已接受的 canonical 與實際覆核提案僅差狀態欄位，沒有以其他審稿者身分補簽。

**新增文字的事實覆核通過，仍適用 AE-C01。** A 段在虛構 C 區確認 Sunrise Airlines 標示及排隊隊伍；B 段延續既有樓梯旁的位置，確認 Maple Airlines 隊伍。向這個情境的現場人員確認航空公司，是角色對話中的指示，並未宣稱所有機場都適用的排隊規定、權利或安全程序。四語保留上述事實意義，沒有需要新增外部來源的主張；此輪沒有重新抓取網頁，也沒有待修正事實。

| 版本紀錄 | SHA-256 |
| --- | --- |
| 目前 canonical Day01 全檔 | `14ecdeed1cd17bb0f4f9ad1097813c150954b1462177dd4259c92a42e929ec05` |
| 目前 Day01 已核英文內容 | `4206a5c57022f7a268ee5557e40efa2b15261a4125b0678b35397377de7e985b` |
| 目前 Day01 完整教學內容 | `aa66c6a01286e22a32606f5ad3381fc3fe7dc11356a48a111745920888ca463e` |
| 本次實際覆核的最終提案全檔 | `8b902b0dfbaf438eee7bf324a437effa9676dc37c3b1877683d20b425ecc49ab` |
| 保留的先前 Day01 全檔歷史值 | `137ef7a19096c7b3d4afd762426be7e3cf5eb5fdd53bfaf301444d753e3f1c40` |
| 保留的先前 Day01 英文歷史值 | `e5a2cb7dae964fbbefe536e80a9761d395b0cd4f08284395fedd6fb30686d2f9` |

JSON 僅更新 `production_source_hashes` 的 Day01 目前摘要，先前紀錄原樣放入 `production_source_history`；其他 59 份目前摘要、原稿摘要、23 組主張與 24 份來源紀錄全部保持不變。擴充事實與目前版本比對另記於 `supplemental_reviews`。

### 目前 brief 的窄範圍補充覆核

重新讀過 A／B 大綱選項及第一題可跟做示例：A 描述目前逐段聽懂後跟讀的順序；B 明說是替代順序，選用後須調整劇本及對應計畫。示例的問題、Zone B／D／C 三選項、B01／B02 原對話、選答提示與四秒 line pause、B／Zone D 正解及逐字答案說明，均與當前生成順序一致。目前 brief SHA-256 為 `9c37f1c466b7e8ea830985198f6d66272ff10441d68c85fbed95b54e55ed1748`，純記憶體生成結果與目前磁碟 brief 相同。

[較早的共用指示覆核](verify-shared-instructions.md) 中 95 個條目、545.6 秒文字估算及 68 秒固定練習停頓，是擴充前十四段對話版本的歷史快照。擴充後純記憶體生成為 111 個條目、691.6 秒文字估算及 84 秒固定練習停頓；五語共用指示本身沒有改變。本查核沒有重跑落地 prepare 或綁定工具，也未量測新語音／品牌素材或宣稱最終 600 秒已達標。root 將在目前獨立紀錄整合後重新 prepare、綁定與 staging。
