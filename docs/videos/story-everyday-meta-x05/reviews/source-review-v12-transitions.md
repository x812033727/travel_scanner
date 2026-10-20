# X05 Meta v12｜獨立來源差異審查

- **判定：PASS（來源）**。只驗 v11→v12 的旁白、章名、數字卡、畫面提示及伏筆對位差異；敘事盲讀、實際語音及成片仍須另驗。
- 受審 `video.json` SHA-256：`ed510f5c7a57136dd9c21137fa3be9191181349d178b0c08caefec471a7c541d`。
- 2026-10-20 核對 Git 前版 diff，並讀取 [FY2023 Meta Form 10-K（M23）](https://www.sec.gov/Archives/edgar/data/1326801/000132680124000012/meta-20231231.htm) 原始 HTML SHA `d3b91050396da40656d06dadd75984cc9fcd5eeedde01f2d8a5ac6a8caff91f0` 與 [FY2025 Form 10-K（M25）](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm) 原始 HTML SHA `279019755c4435c94ab42d86c39b914f57c5ef3d63aafde5c4b0867ddccf4fa2`；雜湊與 [source-notes.md](../source-notes.md) 一致。其餘未改事實沿用前版同源審查，不能把此差異審查當成已聽音訊。

| v12 修訂 | 判定及原件邊界 |
| --- | --- |
| `m050314` 改問次年廣告送達數，`m050401` 立即答 FY2023 +28%；第四章卡另標公司合計「未揭曉」。 | **PASS**。M23 Revenue / Advertising 明載 FY2023 FoA ads delivered 比 FY2022 +28%，平均單價 −9%；這是廣告量變化，沒有冒充公司營業利益。公司合計留白是編輯遮蔽。 |
| `m050408` 刪除已由 `m050407` 說過的「虧損更深」，只保留人事費增加及 RL 收入減少。 | **PASS**。M23 的 FY2023 RL 段落把虧損擴大主要歸因於 increased personnel-related expenses 和 decreased RL revenue；兩個方向與來源相符。 |
| `m050601` 先答無法由眼鏡與 Quest 銷售方向算出單品損益，再說 AI 眼鏡銷售增、Quest 減；`m050609` 說分部表僅給 RL 整欄收入與營業虧損，沒有兩款產品各自營業損益。 | **PASS**。M25 只把 RL 年收入 +US$61m／3% 描述為眼鏡增、Quest 減的淨結果；同件分部表給 RL 合計收入及合計營業虧損，不能反推出兩款產品各自的營業損益。這是資訊不足的限定，不是宣稱任一產品在虧錢。 |
| 第一章章名改為 FY2025 RL 營業虧損近 US$19.2bn，第四章章名改為廣告量再增且 RL 結果蓋住，`x05-b06-s01` 的結果抽屜鎖住；兩筆 loops 指向新的開章回收。 | **PASS**。第一章章名只重述開場已給出的 M25 RL 營業虧損，第四章沒有提前報出 FY2023 RL 虧損方向；新增遮蔽／伏筆對位不構成新事實。M25 分部表 RL 虧損為 US$19,193m。 |

本次沒有改來源 URL、財年數字或 Shorts 的事實主張。製作仍停在審稿關卡，不能依此收據啟動付費畫面或宣稱成片合格。
