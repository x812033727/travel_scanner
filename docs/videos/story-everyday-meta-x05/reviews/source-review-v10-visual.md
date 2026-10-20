# X05 Meta｜v10 視覺修訂獨立來源差異審查

結果：**PASS（文字／卡片所據來源與畫面寓意）**，僅限 `video.json` SHA-256 `e230d6b7e8f28f90e88792b8900f84e994d2f957ce37fba04dbe32ed948ab32b`。這不是插畫評審、聽審或成片核准。審查者為 Codex root，與改稿／生成代理不同，日期 2026-10-20。

比較已獨立逐來源 PASS 的 [v9 審查](source-review-v9.md) 所綁主稿 SHA `9ec57716a952185ef4ba17b50493b851c8b60223145a0606a40d07deaabab85c` 與 v10 JSON：**84 景的所有旁白 `lines`、句 ID 與順序、來源 URL、音樂、固定 `look` 均逐欄相同**；speech hash 仍為 `7a735f4f4a395882`。差異僅是 b01-s02/s03 兩景由失敗插畫改為原生 stats 卡、其餘 64 個 `shot` 的英語插畫提示詞及 thumbnail 景 ID 改為 b01-s07。未加新旁白或新的營收推論。

兩張新增卡均重新對 SEC 原始 HTML：FY2025 [Meta Form 10-K](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm)（本機內容 SHA `279019755c4435c94ab42d86c39b914f57c5ef3d63aafde5c4b0867ddccf4fa2`）列全公司 operating income **US$83,276m，為正數**，同表 Reality Labs operating loss **US$19,193m**。b01-s02 卡只說「FY2025｜公司營業損益／正數／全公司口徑」，不把部門虧損誤作全公司虧損，也未先揭示正數尾數。FY2022 [Meta Form 10-K](https://www.sec.gov/Archives/edgar/data/1326801/000132680123000013/meta-20221231.htm)（本機內容 SHA `09c65f4c5cc2cf6b9b9c799c8f4c04045556a9567d508a0c2e8112d15a8aafb8`）記錄 ad impressions delivered **+18%**、average price per ad **−16%**；b01-s03 卡只說二者「不同方向」，未提前揭方向與營收，與 `m050103` 及後續揭示相符。

我逐讀 64 景新版提示詞並與相鄰旁白及 `source-matrix.md` 對照。木塊、封套、座椅代幣、陶片及原型道具是抽象示意：保留分部與公司總額、收入與營業損益、實際結果與未來計畫的界線；沒有把 QNX 等其他企業史、Meta 特定產品獲利或資金流動杜撰進畫面。FY2021／FY2023 近等端點仍留中間 FY2022 跌幅；FY2025 產品走勢以中性灰藍道具呈現，沒有借 FoA／RL 色碼把兩項產品硬分到不同部門。b01-s07 作 thumbnail 來源是一個抽象天平，不畫品牌商標或未公開數值。畫面生成後仍須逐張確保無可辨文字、錯誤圖表、真人外觀或與旁白矛盾的結果；只要一張評審未過，不得藉本來源審查直接入片。

結構檢查顯示 64 個 MiniMax 插畫景加 20 張原生卡，規劃比例 **64/84 = 76.2%**；前三景恰為三卡，下一景必須是真正通過審查的插畫。這是**規劃比例**，最終比例及 `image-01`／`cute-mystery`、每張檔案與 paid receipt 須由媒體 QA 再證明。原 v9 故事敘事盲讀因整個 JSON SHA 改變而不直接冒充 v10 盲讀；等兩位讀者的 v10 精確收據。
