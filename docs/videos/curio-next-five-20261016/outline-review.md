# 五集大綱交叉覆核

日期：2026-10-16（Asia/Taipei）。範圍僅為研究、claims 與 A/B 企劃；正式劇本、逐句查核、十三題盲評、音訊及成片仍未開始。

## 分工與修訂

| 集數 | 作者 | 獨立覆核者 | 本輪已修訂的具體問題 |
| --- | --- | --- | --- |
| H10 | curio_five_inventory | curio_h12_m09_planning | 4/25 紙條所記的是翌日 26 日南行計畫；開場由物件清單改成取紙、標圖、查看岸上零件的未揭曉事件。 |
| H11 | curio_five_inventory | curio_h12_m09_planning | 開場不先透露 2019 校方撤下消息的處置；2009 稱定年工作，取樣插畫不擅加日期；Naibbe 示意不宣稱本片實測。 |
| H12 | curio_h12_m09_planning | curio_u09_planning | 分開 ARCHTOR 15 日午夜過船通報與岸上 Return Book 觀測；110 英尺是器材位置；1912 詩中餐桌與當年現場分開。 |
| M09 | curio_h12_m09_planning | curio_u09_planning | 2021 明寫電腦重建模型，未主張實體製作已驗證；30 殘存齒輪與69模型齒輪分開；各盤以同一次操作依序揭示用途。 |
| U09 | curio_u09_planning | curio_five_inventory | 最後一章保留60秒解釋機制；LGM玩笑、2月振盪候選與5月自轉解釋分開；A/B開場補至170/163字元並同步時間表。 |

覆核者重新開啟各自負責集數的主要來源；作者負責套用意見，覆核者讀回修訂。五集的大綱層級均無剩餘阻擋項。U09 覆核者另取得並視讀 Gold 1968 原論文的 UBC 學術鏡像兩頁，已歸屬記入研究表；後續只更新完成狀態元資料。這些結論不代表後續正式稿十三題已通過。

主協調另重開 Parks Canada 航程頁與 NRS 2026 展覽公告，核對 H10 人數／年份及 H12 展期邊界；成本提案由 U09 覆核者另核算。所有來源取用成功與受限處保留在各集 research.md，不把摘要當作已讀全文。

## 成本與製作狀態

- 每次圖片加圖像評審 US$0.0135；120張、含首輪最多3次為US$4.86，加US$1.14旁白與QA預留，得每集US$6／五集US$30。
- 審稿已修「含首輪共最多三次」及「建議停手上限」，避免誤讀為額外三輪或已獲授權。
- 本批未產生付費呼叫，沒有主機開拍請求。既有 H09 額度未挪用。
- 章節與開場秒數為估計；正式稿仍須 lint、配音實測及必要調整。

## 本機驗證紀錄

- 既有 outlineOptions 解析器可讀五集的完整 A/B 標題、摘要與鉤子。
- 五份 brief 均為 UTF-8、無 BOM、LF，避免送審後 Git 換行改變雜湊。
- npm ci 完成；系統 Node v24.13.0 的 test:docs-videos 為214通過、1失敗。失敗為既有 imported-long-languages runtime freezing 子行程 native exit3221226505，無 stdout/stderr，單項重跑相同。
- 受測 package-runtime.mjs／runner.test.mjs 與 origin/main 相同。以既有 bundled Node v24.19.0 重跑該單項為1通過、0失敗、exit0；沒有修改程式或全域Node。既有調查見 tasks/done/2026-09-28-investigate-windows-native-crash-in-video.md。未宣稱整套在bundled Node重跑通過。
- 送審後 check:tasks 通過（1895份任務檔）；既有過期／重疊認領僅為警告，本批沒有新增衝突。repo-hygiene 為3通過、0失敗；git diff --cached --check 通過。
- 最後由 curio_five_inventory 唯讀重算五份 brief 雜湊，全部與 submission.json 相符；README、製作計畫、覆核紀錄與送審收據的 pending／未授權狀態及金額一致。
