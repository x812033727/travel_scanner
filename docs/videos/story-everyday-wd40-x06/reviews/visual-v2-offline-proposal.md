# X06 WD-40｜第二輪視覺策略（離線提案，未送圖）

本提案沒有改動 `video.json`，也沒有授權新的 MiniMax 或 judge 呼叫。
目前受獨立審查綁定的腳本 SHA-256 仍是
`907f8e3ff45f3edf0bbed64a54216c761696e8e954d51c315a8a228069e204d1`；
主工作區 `STOP` 仍在。隔離三鏡小試的機器評審 3/3 PASS，人工僅
`x06-b02-s06` 暫可用，說明刪除字面載體可降低假字／商標風險，
但「smooth metal cylinder」與「hinge」仍不夠限定尺度與形狀。

| 鏡頭 | 待覆核的下一版 prompt | 解決的失真 |
| --- | --- | --- |
| `x06-b02-s01` | `Close shot at a clear shipping doorway, one adult clerk places a palm-sized steel aerosol can with a tiny spray nozzle onto a shallow wooden tray, its smooth metal back facing the viewer, morning light` | 以手掌尺度、小噴嘴、罐背朝向鏡頭約束「噴罐」，移除紙箱與倉庫牌；一個放下動作。 |
| `x06-b02-s02` | `Close shot at a clear wooden workbench against an empty wall, one adult mechanic pivots the two leaves of a palm-sized door hinge around its central pin with one hand, soft daylight` | 以兩片鉸鏈葉片與軸銷限定鉸鏈形狀，只畫一隻手轉動，移除背景機具。 |

後續畫面提示詞依同一組檢查條件逐鏡重看，再決定是否把相似物件一併
改寫：

1. **尺寸與辨識點同時出現。** 只寫「cylinder」可能生成貨桶；
   出現噴劑時用「palm-sized aerosol can」與「tiny spray nozzle」，
   滴油瓶寫小玻璃瓶與細滴嘴，鉸鏈寫兩片葉片和中心軸銷。容器正面
   不朝鏡頭，精確品牌與數字仍由原生卡和字幕承載。
2. **動作壓到一幀看得懂。** 「設定路線／檢查貨物」等抽象動詞會被畫
   成站著或推著已裝貨的車。明確指定手碰到物件的瞬間，例如把罐
   放上托盤、轉動鉸鏈的一片葉、推開空貨架的門。若動作本身複雜，
   改取具體成果，不要求模型同時畫動作與前後因果。
3. **背景不給可印字的表面。** 要店面、物流或帳務情境時，選空門口、
   櫃位輪廓、簡單桌面或遠處貨輪；不要紙箱、簿頁、牆牌、刻度與
   面板。`x06-b02-s06` 的空白貨櫃與遠景貨輪是目前較好的實際例子。
4. **輪流取樣不同畫面家族。** 新稿的木珠／木塊、繩線路線、光滑
   噴罐、清潔海綿與修理工具，仍可能各自失真或重複。兩個 HOLD
   鏡頭如果在新的獨立 SHA 審查與有界試畫後過關，下一個付費關卡
   應從路線象徵、財務對比、家清貨架各抽一鏡，逐張人工核對後
   再考慮章節批次。評審 pass 不能蓋過人工 HOLD。

下一輪若實際改動 `drafts/visual-safety.mjs` 並重跑 compose，必須生成
新的 `video.json` SHA、重算 visual hash，另請獨立審查者確認只是
視覺變動。先前四張舊圖和 `x06-b02-s06` 的原 prompt／take 應保持不動。
每次付費前先讀 live ledger、配額與 US$25 全包餘額；用隔離 allowlist
測指定鏡頭，主工作區 STOP 保持。未通過者不得進本機預覽，
也不得用 SVG 替代真 MiniMax 來湊 70% 比例。
