# X11 FedEx｜v5 作者修訂與來源差異

**作者交審紀錄，不是來源或敘事 PASS。** v5 鎖定主片 `3d2a7d1d422105802fd1d755fa8f90f1ca5667057f76aa133d90db0f5efba0d8`、兩支 Shorts `7d352677b785667866b6ef09e7c4f4934d6659fb966f334c8d98c4ac063dcaa6`（SHA-256）。[v4 來源差異審查](reviews/source-audit-v4-independent.md)曾 PASS，但[盲讀 A](reviews/blind-a-v4-independent.md)與[盲讀 B](reviews/blind-b-v4-independent.md)都只通過 8／12 必答項；三份收據均只綁 v4 雜湊。

## 兩位讀者意見的逐句修訂

| v5 句 ID | 修訂與待核問題 |
| --- | --- |
| `x110109`、`x110227`→`x110301` | 主問題改成「公司合併後，地面路網為何仍逐地整合？」；第二章末改問三家公司進入哪項整合計畫，第三章首直接答 one FedEx。FY2022–26 申報不足以回答**歷史上為何等到 2024 才合併**，影片不再提出這個問題。 |
| `x110309`–`x110317`、`x110318`–`x110325` | 概念包裹沿分揀、取配、幹線往前走。只把 FY2023 的組織改造預期（隔年六月）和 Network 2.0 多年期分開；不再在同章重複念兩次「多年工程」，也不預告加拿大哪批先後無法證成的排序。 |
| `x110404`、`x110415`–`x110420` | 六月一日明說 **2024 年**；FY2024 管理層的空運／國際焦點與地面更整體安排，僅作當時的**目標**，不冒稱路線已驗收。服務承諾問題在相鄰句回收。 |
| `x110508`–`x110514` | 不再第三次口播司機配置；改用 FY2025 約 720 處舊 Ground、約 530 處舊 Express **美加地面設施**，及申報所說的營運整合中，回答「公司合併後還剩什麼要改」。設施數與約 290 **實施地點**不是同一分母。 |
| `x110606`–`x110615` | 刪除 v4 末章拖車 GPS、掃碼、排班、路線工具等與合併結果無直接證成關係的設備清單；用 FY2026 申報的**持續**分揀／取配／幹線工程接回 FY2023 計畫。最後一哩的雇員與服務商按市場並用，只保留 FY2026 一次現在式說法。 |
| 第三、六章標題、Short 1 | 章名寫可定位的事件；Short 1 加入主片 `x110303` 的「Network 2.0」口播與畫面標題，`x110404` 自帶 2024 年份，可單獨理解 50 多個美國實施地點量的是哪項計畫。 |

## 新增主張的 SEC 原文入口

- [FY2023 10-K，2023-07-17 申報](https://www.sec.gov/Archives/edgar/data/1048911/000095017023033201/fdx-20230531.htm)，`Item 1 > One FedEx and Network 2.0`：`The organizational redesign will be implemented in phases with full implementation expected in June 2024.` 請以 F32 核對 `x110318`、`x110320`–`x110322`：這是當年對**公司組織改造**的預期，與 Network 2.0 多年實體網路工程分開；事後法律合併日期由 FY2024 申報 F11 證明。
- [FY2024 10-K，2024-07-15 申報](https://www.sec.gov/Archives/edgar/data/1048911/000095017024083577/fdx-20240531.htm)，`Item 1`：`One FedEx and Network 2.0 will leverage the strength of our networks, people, and assets in more efficient ways, enabling a distinct focus on air and international volume while facilitating a more holistic approach to how we move packages on the ground.` 請以 F33 核對 `x110415`–`x110418` 的「希望／要」語氣；不可把未來營運方向當完成成果。
- [FY2025 10-K，2025-07-21 申報](https://www.sec.gov/Archives/edgar/data/1048911/000104891125000011/fdx-20250531.htm)，`Item 1 > Federal Express Segment > Operations`：`approximately 720 legacy FedEx Ground and 530 legacy FedEx Express facilities, as of May 31, 2025, that support its U.S. and Canada surface operations. Through Network 2.0 ... these operations are being consolidated.` 請以 F34 核對 `x110508`–`x110514`；兩個設施數**不能**與 F16 約 290 實施地點相除，也不能推斷每處舊設施都仍獨立。
- [FY2026 10-K，2026-07-20 申報](https://www.sec.gov/Archives/edgar/data/1048911/000104891126000105/fdx-20260531.htm)，`Item 1`：`In 2026, we continued our network transformation`，接 `modernizing and consolidating our sortation facilities and equipment, reducing pickup-and-delivery routes, and optimizing our enterprise linehaul network`；同件 `we utilize both employee couriers and service providers ... using a market-by-market approach`。請以 F28／F29 核對 `x110606`–`x110613`：工程仍在進行，司機安排是 FY2026 現在式，沒有宣稱全美完成。

**規格初查：**六章、122 句；扣除首章與三句片尾 CTA 的實質正文 2,426 個稿面字元、2,015 個程式正規化 spoken units。按正常每分鐘 250 spoken units，**語音本身**約 8.06 分鐘；估時計入逐句／換景停頓約 9.98 分鐘，正式 Sulafat 音訊仍須實測。15 組逐句 loop，106 景中的 99 插畫鏡頭／6 原生資料卡／1 片尾卡，lint 0 錯誤／0 警告。Short 1 204 字，約 40.8–49.0 秒；Short 2 188 字，約 37.6–45.1 秒（每分鐘 300–250 字估計）。尚無付費生成、成片或發布連結；US$25 是全片硬上限，未乾跑核價。
