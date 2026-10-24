# S38 R8j｜`pf006` 退圖後無新圖卡片方案

2026-10-21 00:36 UTC。**作者凍結，待獨立書面審核；原生新圖、整體分鏡、網站審核及成片仍 HOLD。**R8i `pf006` 經三張原生圖與兩輪修詞仍失敗，依 [系列處理規則](../../../.agents/skills/curio-episode/SKILL.md)改成一張日期／人名卡，不再為這一景購圖。旁白及來源未更動。

`pf006` 保留原 ID、原句「先回到兩天前。九月二日凌晨，女僕珍妮發現城裡有火。」及章節「九月二日凌晨，佩皮斯看過火又睡回去」，只將 `template: shot` 改為 `big`，卡片文字是 **`1666．09．02`**、標籤 **`女僕珍妮`**、輔文 **`凌晨，倫敦城裡有火`**。卡片只給日期／人物／事件定位，不重現未被日記證實的 Jane 年齡、窗口、衣物或她目擊的具體起火點。相鄰 `pf007` 的未畫鏡頭 camera 從 `drift right` 改 `pan left`，因移除 `pf006` 的運鏡後原三張仍圖連續同類運鏡觸發 lint；其提示詞、台詞及其他資料未改。已通過 `pf004/005` 的畫面與 camera **完全未改**，但新版本仍須工具逐景驗證 request key／judge stamp 才可宣稱沿用。

[結構化差分](verify-24-r8j-structured-diff.json) SHA-256 **`50bae1d7cc5659a26714bcf849d964cc0cceb0f2965ce6c010e14e718718ba5c`**。我把 R8j 卡片與 `pf007` camera 原始位元組還原，整檔 SHA 正好回到 R8i **`de27c08f77dd91e66703fcf5c875ee1ea787d34246b93bc6237af8c7fcd03861`**；解析 JSON 只有卡片模板／資料七個葉節點及 `pf007.data.camera` 一處變動。R8j `video.json` SHA-256 **`cd28ba2255917a5040c8c84c3275959ca94b29934b5a892595b82e304e8eeb42`**、`visualHash` **`3a63356704b7dedb`**；`brief.md`、`research.md`、`claims.md`、`script.md` 仍分別為 `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。Lint 0 error／0 warning；全片為 110 張插圖、1 張 `big`、1 個 outro，正文插圖占比 **110／111＝99.1%**，不會連續出卡。

私有 `STOP` 仍在，ledger 累計 **US$0.2895**（17 image、15 judge、1 music），含舊 `pf003` **US$0.0035 reserved**，整集硬上限仍 US$4.58。`pf003` 仍是未畫景，不把預約當免費圖；不可擅清或重送同一付款請求。獨立審查應核 D2a 日期與 Jane 角色、卡片語意、系列卡片限制、逐景快取、聲畫時序及兩張 KEEP；通過後再設新範圍的限額續畫方案。原第一章 28.90 秒，尚少 1.10 秒才達 30–60 秒濃縮開場；這張卡片在第一章後，不能拿 5 秒品牌片頭湊數，組片前另處理節奏。
