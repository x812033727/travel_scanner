# X11 FedEx｜來源可行性與故事主線（前製）

2026-10-20。**狀態：一手來源初查，尚非逐句查核、獨立審稿或影片稿。**這是既定 C01–C20 之外的新增題，保留 C03 Moleskine 的編輯順位；C03 所需的 Moleskine／D’Ieteren 官方網域在本雲端被網路白名單擋下。本題所用 `www.sec.gov` 與 `data.sec.gov` 則實測可讀。未產生付費媒體或成片。下方六章／Shorts 是最初可行性骨架；目前 v5 稿的事件流以 [Treatment](treatment.md) 和 [逐句來源矩陣](source-matrix.md) 為準，Freight 區分已移到說明欄。

## 可拍的反常問題

以下工作標題與末段 Treatment 是**最初可行性假說**；五份近年 SEC 申報不能證明為何歷史上延至 2024 才合併。現行 v5 主片已改問「公司合併後，地面路網為何仍逐地整合？」，以 [Treatment](treatment.md) 與 [逐句稿](script.md) 為準。

**工作標題：同樣叫 FedEx，快遞與地面包裹為何到 2024 年才併成一家？**觀眾看到一個品牌，FY2022 Form 10-K 卻列 FedEx Express、FedEx Ground 為不同公司／營運部門；FY2026 申報更直說兩套業務和網路在歷史上「分開、獨立」運作。公司的反轉是先在 2023 財年宣布 `one FedEx` 與 `Network 2.0`，2024-06-01 完成 Ground／Services 法律合併，再逐市場改分揀、取件、配送與幹線。**法律合併不等於所有實體路線完成整合**；2026 年報說加拿大已全部實施，美國預計 2027 年底完成，並警告整合可能延誤、費用或節省幅度偏離預期。

觀眾能看見「一箱包裹、兩種服務承諾、兩張路線圖，最後才調成一張」；主線是**怎樣重畫配送網路**，不是臆測「兩台車到同一門口」或聲稱某項確定節省額。公司把改善效率／長期獲利與電商成長、服務組合轉向較慢服務連在一起，旁白必須說成公司當時的理由，不得把它寫成唯一或已證明的成因。

## 已讀的 SEC 原件與可追的原文錨點

SEC HTML 原件均於 2026-10-20 以 GET 成功讀取；財年截至各年 **5 月 31 日**。日期是申報日期，不是事件日期。括號內為下載 HTML 的 SHA-256，供後續獨立審核比對；原文可在各頁 `Item 1. Business`／`Item 1A. Risk Factors` 內搜尋短句。

| 原件（申報日） | 原文錨點／支持的有限說法 |
| --- | --- |
| [FY2022 Form 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017022012762/fdx-20220531.htm)（2022-07-18；`27ea3122e13dc3adb37c379f8b055ba850125ed636d1063c5b83a45d8314cfcc`） | `Item 1` 的 `FedEx Express:` 是 Federal Express Corporation 的限時配送；`FedEx Ground:` 是 FedEx Ground Package System, Inc. 的北美小包裹地面配送，描述為 `low-cost, day-certain service`。兩者服務及組織分開，但不能因此推論每筆訂單走兩套線。 |
| [FY2023 Form 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017023033201/fdx-20230531.htm)（2023-07-17；`630ceceb23295ffae3ba52509394758a378d8f8f934899111ae66244c6286eed`） | `Item 1` 的 `One FedEx and Network 2.0`：在 FY2023 第四季宣布整併 Express、Ground、Services 等；`We plan to consolidate our sortation facilities and equipment, reduce pickup-and-delivery routes, and optimize our enterprise linehaul network`。這是當年的計畫，不能當完成成果。 |
| [FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017024083577/fdx-20240531.htm)（2024-07-15；`8f21468ed36509a9ba715479ee766fbf0b98615dd0cd436be1eab4309a9e1141`） | `Item 1` 的 `On June 1, 2024, FedEx Ground and FedEx Services were merged into Federal Express` 是 **FY2024 結束後**的法律事件；同頁稱 `more than 50 locations in the U.S.` 已實施 Network 2.0，並從 2024 年 4 月起分階段轉換加拿大舊 Ground 業務。地點數只指當時的實施範圍。 |
| [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000104891125000011/fdx-20250531.htm)（2025-07-21；`f65d13a0b23d5687a5fcd7681eae63f60f538ef0bc254c654c63365a1958cb35`） | `Item 1`：截至 **2025-05-31**，Network 2.0 已在美加 `approximately 290 locations` 做最佳化；另一段稱加拿大已完成、美國約 `130 locations`。`Using a market-by-market approach, service providers will handle ... while employee couriers will handle others` 是**未來配置說法**。290 是美加地點數，不是完成百分比，且不能和 FY2024 美國 50 多處直接算增長率（地理範圍不同）。 |
| [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000104891126000105/fdx-20260531.htm)（2026-07-20；`b24489462a93674730fd19432953fba9c9bc544a1bbc2b7e50a45fb1f360fff2`） | `Item 1`：美國截至 2026-05-31 約 `360 locations` 實施；公司重述 `Network 2.0 has been fully implemented in Canada`，美國 `we expect to complete ... by the end of calendar year 2027`，後者只是展望。該申報亦描述部分既有場站的拖車定位、條碼掃描、動態排班與服務商路線資料，不代表每站都已改成相同流程。`Item 1A`：Express／舊 Ground 網路 `historically operated separately and independently`，且 `There can be no assurance` 能如計畫完全整合；費用、節省、客戶流失與延宕都是風險，不能說改善已由整併單獨證成。 |

**Freight 邊界（不能省）：**Ground 是小包裹地面配送，Freight 是 less-than-truckload 大宗零擔貨運；兩者不是同一條線。FY2024 申報說 Freight 當時維持另一子公司。FY2026 申報 `Item 1` 的後續事件記載 2026-06-01 分拆生效：FedEx 配發 FedEx Freight Holding 80.1% 股權予股東、保留 19.9%，此後不再把 Freight 併入財報。這不能被敘述為「FedEx 又把剛合併的 Ground 拆出去」。

## 六章事件流（Treatment 方向，待逐句驗證）

1. **濃縮開場（30–60 秒）**：一箱要隔日送達、一箱可等幾天；外箱都寫 FedEx，但 2022 年報把兩條服務線分開列。到 2024 年才合併公司，到底要合的是什麼？停在這個問題後接 5 秒片頭。
2. **原來是兩條承諾**：用 FY2022 申報對照 Express 的限時承諾與 Ground 的按日、低成本地面服務，拆清包裹、車、分揀站與時間表；章尾問同品牌下的分線何時成為公司想改的問題。
3. **轉折不是改名字**：FY2023 宣布 `one FedEx` 與 `Network 2.0`；公司提出合併分揀設備、減少取配路線、優化幹線。說明這是想做什麼，不先說做成了多少。
4. **日期陷阱**：2024-06-01 Ground／Services 併入 Federal Express，實體網路卻是分市場推進；截至 FY2024 已在美國 50 多處實施，加拿大分階段轉換。章尾問「公司合在一起以後，路線是不是就合好了？」
5. **進度與取捨**：FY2025 美加約 290 個實施地點，公司按市場決定雇員或承包商配送；不是所有地方同一方案。用 2026 年報的風險揭示回答：歷史上分開運作的網路，整合仍有成本、服務、勞務與時間風險。
6. **目前能回答多少**：FY2026 加拿大已完成 Network 2.0 實施，美國預計 2027 年底完成（**預測**）；「同牌不同網」到「逐市場合網」是過程。明確區分 Freight 的 2026 分拆，最後以「若是你，隔日件與可等件要在哪一段共用路線？」作留言題，訂閱邀請扣回「熟悉品牌背後的運作」。

正文需先寫足至少 8 分鐘實質資訊、30–45 秒可回收鉤子及至少 8 組伏筆；以上六章只是骨架，不能把風險揭示重複灌成長度。視覺可用匿名箱子、兩色路線、分揀帶、夜間樞紐、地面車和後製地點數字卡；AI 插圖不得含商標或可讀字，品牌名留後製字卡／縮圖。正式片頭 5 秒、片尾 21 秒、繁中可關閉 CC 與兩支 Shorts 仍須依奇聞檔案局規則製作。

## 兩支可單獨看的 Shorts（25–55 秒構想）

- **「FedEx 不是一直只有一套配送網」**：先講 FedEx Express／FedEx Ground 兩類服務，再揭 FY2023 才宣布整併、2024-06-01 才完成公司合併；結句說實體路線仍逐市場改。年份與「公司」對「網路」的差別要放在這支內，不能靠長片補。
- **「合併公司後，地面網路還在改」**：先交代 FedEx `Network 2.0` 是改美加包裹取件、分揀、幹線、配送；FY2025 美加約 290 地點，FY2026 加拿大完成，美國年底 2027 只是預計。結句問「整合會不會真的省下想省的？」並以年報的風險語氣作答。

## 去重與下一關

已在此倉庫 `docs/videos`、核准 100 題／備選題、兩份新增候選及保存的參考頻道研究標題搜尋 `FedEx`／`聯邦快遞`：只找到原[新增候選表](../brand-stories-everyday-reversals-20261020/additional-brand-candidates-20261020.md)及 README，沒有同主線既有集；無法連到參考頻道即時頁，**不宣稱當前 YouTube 沒有同題**。原候選的「隔夜包裹為何先集中夜間樞紐」需要早期同期來源，這五份年報不足以證明起源細節，因此建議採本次 SEC 可證的近年整合角度。

下一關：另一位代理逐條覆核上表與六章限制，然後才定 Treatment、逐句稿、兩位盲讀、畫面與成本上限。這份初查不能作來源 PASS 收據，也沒有支付媒體費用。
