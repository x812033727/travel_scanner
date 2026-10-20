# Meta X05｜SEC 年報原文獨立查核

查核日期：2026-10-20。以 `lxml` 抽出本機 SEC 年報 HTML 可見文字，逐項比對年度、表頭、列名、單位及正負號；FY2022 文件另重新下載 SEC 原檔並比對位元組。沒有依據影片稿判定。以下是**財報原文查核**，不是劇本、畫面或成片核准。

| 本機原文 | SHA-256 | 文件明示的財年 |
| --- | --- | --- |
| `/tmp/meta-2021.html` | `c4e4ed1556c890ece859432b8dd6cfa00c6c555cb87ac975b1838b4033edf62c` | 截至 2021-12-31 的財年 |
| `/tmp/x03-meta-2022-10k.htm` | `09c65f4c5cc2cf6b9b9c799c8f4c04045556a9567d508a0c2e8112d15a8aafb8` | 截至 2022-12-31 的財年 |
| `/tmp/meta-2023.html` | `d3b91050396da40656d06dadd75984cc9fcd5eeedde01f2d8a5ac6a8caff91f0` | 截至 2023-12-31 的財年 |
| `/tmp/meta-2025.html` | `279019755c4435c94ab42d86c39b914f57c5ef3d63aafde5c4b0867ddccf4fa2` | 截至 2025-12-31 的財年 |

FY2022 原始文件的 SEC submissions [older index](https://data.sec.gov/submissions/CIK0001326801-submissions-001.json) 列出 accession `0001326801-23-000013`、form `10-K`、reportDate `2022-12-31`、filingDate `2023-02-02`、primaryDocument `meta-20221231.htm`。2026-10-20 重新下載 [SEC 原始頁](https://www.sec.gov/Archives/edgar/data/1326801/000132680123000013/meta-20221231.htm)，所得 2,881,101 位元組與本機 FY2022 HTML 的 SHA-256 完全相同。因此下面 M22 引文有可追溯的 SEC 原檔；**2023-02-02 是 index metadata 查得，並非 HTML 本文直接證實**。

四份文件的 **Segment profitability** 段落均以 *income (loss) from operations by segment* 命名表格。2021 年表頭是 `(dollars in millions)`；2022、2023 和 2025 年是 `(in millions, except percentages)`。括號代表負數，`Total income from operations` 是全公司的**營業利益**，不是收入、稅後淨利、現金支出或自由現金流。

| 財年與原文列 | Family of Apps | Reality Labs | Total income from operations | 同年算式，單位均百萬美元 |
| --- | ---: | ---: | ---: | --- |
| FY2021 | 56,946 | (10,193) | 46,753 | 56,946 − 10,193 = 46,753 |
| FY2022（FY2022 原檔及 FY2023 比較欄一致） | 42,661 | (13,717) | 28,944 | 42,661 − 13,717 = 28,944 |
| FY2023 | 62,871 | (16,120) | 46,751 | 62,871 − 16,120 = 46,751 |
| FY2025 | 102,469 | (19,193) | 83,276 | 102,469 − 19,193 = 83,276 |

FY2025 換算為中文「億美元」時，FoA 為 **+1,024.69 億**、RL 為 **−191.93 億**、全公司為 **+832.76 億**。若標題取約數，仍須保留「營業損益」指標與 FY2025 年份；不能把 `83,276` 百萬美元直接寫成 `83,276` 億美元。

跨年端點的獨立算術核對，單位仍為**百萬美元營業損益**：FY2021→FY2023，FoA 正項增加 `62,871 − 56,946 = 5,925`，RL 虧損幅度增加 `16,120 − 10,193 = 5,927`，全公司營業利益變化 `46,751 − 46,753 = −2`。兩項變化近乎抵銷，是**兩個端點**的算術觀察，不能由此推測中間每年的走勢或背後因果。FY2023→FY2025，FoA 正項增加 `102,469 − 62,871 = 39,598`，RL 虧損幅度增加 `19,193 − 16,120 = 3,073`，全公司營業利益增加 `83,276 − 46,751 = 36,525`；這也只比較兩個年末財年的整年結果，不推導逐年趨勢。

FY2023 文件**同一張分部表**亦列 FY2022 比較欄，所以可直接看見 FY2021→FY2022 公司營業利益 `28,944 − 46,753 = −17,809` 百萬美元，FY2022→FY2023 `46,751 − 28,944 = +17,807` 百萬美元。首尾只差 `−2` 百萬，**中間曾大幅下降再回升**；不能說三年每年都停在同一水位。FY2023 **Segment profitability** 表後原文說 FoA 2023 營業利益較 2022 增 `$20.21 billion, or 47%`，主要來自較高廣告收入及行銷、銷售費用下降；RL 2023 營業虧損較 2022 增 `$2.40 billion, or 18%`，主要因人事相關費增加及 RL 收入下降。這些公司原因陳述只比較 **FY2023 對 FY2022**，不能冒充 FY2021→FY2023 全段的單一原因。

FY2022 **Segment profitability / Family of Apps** 原文稱 `FoA income from operations in 2022 decreased $14.29 billion, or 25%, compared to 2021.`，並解釋為 FoA 總成本與費用增加，主因較高員工數帶動薪資及相關費用、重組費用，以及資料中心與技術基礎設施費用上升。同節 **Reality Labs** 原文稱 `RL loss from operations in 2022 increased $3.52 billion, or 35%, compared to 2021.`；主要原因是薪資及相關費用與研發費增加，但 RL 庫存成本下降（包括採購承諾損失較低）部分抵銷。兩句的比較分母都是 **FY2021**；14.29/3.52 十億美元是公司四捨五入後的文句，精確表格差額分別是 `56,946 − 42,661 = 14,285` 和 `13,717 − 10,193 = 3,524` 百萬美元。

FY2022 **Consolidated and Segment Results** 同表將 FoA 收入列為 2022 `114,450`、2021 `115,655` 百萬美元（約 −1%），FoA 成本與費用列為 `71,789`、`58,709` 百萬美元（+22%）。因此收入變化 `−1,205`、費用變化 `+13,080`，共同對應營業利益變化 `−14,285` 百萬美元；這是同口徑算術，不代表收入下降是唯一原因。該節另列 FY2022 重組費用總額 `4,611` 百萬美元；原文 `Total restructuring charges recorded under our FoA segment were $4.10 billion and RL segment were $515 million.`。`4.10`／`0.515` 十億是四捨五入敘述，不能把全部公司重組費用指給 FoA，亦不能當成 FoA 營業利益下降額本身。

同節 **Headcount / Restructuring** 原文稱 `Headcount was 86,482 as of December 31, 2022, an increase of 20% year-over-year.`，並緊接 `Our reported headcount includes a substantial majority of the approximately 11,000 employees impacted by the layoff we announced in November 2022`。這是**全公司 2022 年末人數**，不是 FoA 專屬人數；2022-11 是**宣布裁員**時間，不能說一萬一千人在當月已全數離職。重組描述另列辦公室設施整併及取消多個資料中心專案。財年成本陳述與年末人數可並置，但不能由年末 +20% 推導特定部門人數或每名員工薪資變化。

FY2022 **Revenue / Family of Apps** 原文另稱 FoA 收入較 2021 下降 `$1.21 billion, or 1%`，主要是廣告收入；**Advertising** 原文稱廣告收入下降 `$1.29 billion, or 1%`，每則廣告平均價格下降 `16%`、廣告送達數增加 `18%`（均較 FY2021），後者部分抵銷前者。這些是**收入、價格與量**，不能說成 FoA 營業利益下降全因廣告或把價格變化當營業利益百分比。

FY2023 **Revenue / Advertising** 原文稱 `Advertising revenue in 2023 increased $18.31 billion, or 16%, compared to 2022 due to an increase in the number of ads delivered, partially offset by a decrease in the average price per ad.`；同段列廣告送達數較 FY2022 增 `28%`、每則廣告平均價格較 FY2022 降 `9%`。這是 **FY2023 對 FY2022 的廣告收入及價量**，與同年 FoA 營業利益 +47% 不可混成同一指標，也不保證每則或每類廣告的價格都下降。

其他可直接確認的原文及口徑：

- FY2021 文件前言明寫：`In October 2021, we changed our corporate name from Facebook, Inc. to Meta Platforms, Inc.`。同份文件的 **Consolidated and segment results** 與 **Note 15. Segment and Geographical Information** 均寫 `Beginning in the fourth quarter of 2021, we report our financial results based on two reportable segments: Family of Apps (FoA) and Reality Labs (RL).`。這是更名與**開始分部揭露**的證據，不能推論 Reality Labs 在 2021 年才成立。
- FY2021 業務概述文字稱 `For FoA, we generate substantially all of our revenue from selling advertising placements to marketers.`；FY2023 業務概述及 FY2025 **Revenue and Investments** 稱公司 `generate substantially all of our revenue from selling advertising placements on our family of apps to marketers, which is reflected in FoA.`。`substantially all` 修飾的是**收入**來源，沒有說所有收入、FoA 營業利益或現金流都來自廣告。
- FY2021 **Consolidated and segment results** 將 RL 描述為擴增與虛擬實境相關的消費性硬體、軟體及內容。FY2025 **Reality Labs (RL)** 收入說明明列 `Meta Quest and AI glasses, and related software and content`；因此不能把 FY2025 RL 全稱為 VR 頭盔或單一「元宇宙」產品。
- FY2023 **Reality Labs** 收入段落明寫 `RL revenue in 2023 decreased $263 million, or 12%, compared to 2022.`，並稱這段收入下降 `was mostly driven by a net decrease in the volume of Meta Quest sales`。所以「相較 FY2022，FY2023 Meta Quest **銷量淨減少**」有原文支持，**未提供減少的裝置件數**；RL 收入下降 2.63 億美元屬收入指標，不可當成 FY2021→FY2023 分部營業虧損擴大的唯一原因。
- FY2025 **Reality Labs Products** 原文說許多投資指向尚未上市產品的長期研發，`may only be fully realized in the next decade`。這是公司的前瞻描述，不能當成投資將會成功的獨立證明。
- FY2025 **Reality Labs** 收入段落寫 `RL revenue in 2025 increased $61 million, or 3%, compared to 2024.`，並說 AI 眼鏡銷售增加，部分被 Meta Quest 銷售下降抵銷。這是**收入**相較 FY2024 的變動，不是 RL 營業損益、公司營業利益或某單品的營業利益。
- FY2025 **Segment profitability** 表後說 `FoA income from operations in 2025 increased $15.36 billion, or 18%, compared to 2024.`，較高廣告收入為推動因素，部分被較高成本費用抵銷；列出的成本包括員工薪酬、基礎設施、夥伴安排和法律相關費用。這段公司說明只比較 **FY2025 與 FY2024**；不可當作 FY2023→FY2025 端點差額 `+39,598` 百萬美元的完整因果解釋。
- FY2025 **Revenue and Investments** 原文稱 `In 2025, 82% of our total costs and expenses were recognized in FoA and 18% were recognized in RL.`；這是**當年全公司成本費用的分部認列占比**，不是收入、營業利益、營業虧損、投資回報或現金流占比。同段另寫 `our ability to support our efforts to build the next computing platform is dependent on generating sufficient profits from other areas of our business.`。可如實歸因為 Meta 的公司陳述：支撐 RL 相關長期努力仰賴其他業務產生足夠利潤；仍無法由此推論逐筆 FoA 現金轉帳、專款用途或投資最終成果。
- FY2025 **Segment profitability** 表後說 RL 營業虧損較 2024 年增加 14.6 億美元，原因是成本費用提高；列舉員工薪酬等人事費、不能取消的 RL 庫存採購承諾估計損失、技術開發費。FY2023 表後則提員工相關費增加及 RL 收入下降。不能只用頭盔銷量或消費者評價解釋任一年度的虧損。

限制：HTML 本文明示**財年截止日**，但原文可見文字沒有能獨立確認 SEC **提交日期**的欄位。FY2022 提交日已另用 SEC submissions index 核實；候選筆記所列 FY2021、FY2023、FY2025 提交日仍應另用 EDGAR 文件索引或帶提交日期的 SEC 原始紀錄核實，本報告不據 HTML 本文簽認。分部表只顯示會計加總，不能據此宣稱 FoA 現金被指定轉帳給 RL，或判定 RL 投資報酬與未來產品成敗。
