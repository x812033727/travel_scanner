# S38 R8z｜PF018 首張原圖人工退件

2026-10-22 UTC。**PF018 HUMAN REJECT，本次批次停在 PF018，未購 PF020–022。**正式 MiniMax `image-01` 和九題 judge 只生成一張 PF018 原圖；judge 為 9.29／10、`passed=true`，但其 `details` 問題已指出前景船上多名孩童而非一名成年觀察者，背景人物沒有把木箱裝上船。主代理另直接查看未裁切 1280×720 [私有原圖](/workspace/.video-work/curio-s38/keyframes/pf018-1.jpg) SHA-256 `5076c875dfeb2f2372ce070da28a417572e2e5f0823449897abb42420c6d8615`：前景船上三個卡通人物的兩個明顯是小孩，後方載箱船無人搬箱，不能承接旁白「他搭船沿河看，人們正把家當搬上平底貨船。」原圖雖有當代質感的木船、背景貨物與系列畫風，核心動作與成年觀察者均未呈現；機器 PASS 不取代這項內容驗收。所選裁邊圖 SHA `7053751d221e7bf1e64b14ae7dffdb78a6ba409f76481696f599434f43df2fbd` 留在私人工作區作證據，未列為 KEEP。

來源為固定 1666-09-02 Pepys 日記 L65816–65834：先從塔下來坐船，隨後沿河看居民往 `lighters` 搬財物。現行 prompt 寫 `family load crates`，容易補出未記載親屬與孩童，也沒有在這張圖畫出裝箱動作；後續若要修，只能定點把觀察者與搬箱者明定為成年人並聚焦裝箱動作，重新做可逆差分和非作者書面紙審，再單景試一張，不能直接重跑同 prompt。

付費前的[PF019 卡重綁](verify-86-r8z-pf019-card-rebind.md)有 11 張 KEEP。PF018 正式 CLI 後 manifest SHA `f1c9fad1104321424da55a6a7b0e169d2dff3f1f96dc05f06e8b21a781dc0616` 有 12 筆，先逐位元備份於私人 `review/r8z-pf018-seed1-human-reject/manifest-post-cli.json`；在 STOP 在位、jobs 空時只刪去退件 PF018 並清空過期聯絡表。現行圖單 SHA `a7c5920fd1e4c96b66bb7d9331541c36683987999617279bca9a75c21197c48d`，原 11 張 KEEP 完整條目的 canonical SHA 仍為 `59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301`，各選圖檔 SHA 仍相符。詳[隔離清冊](verify-87-r8z-pf018-seed1-reject-inventory.json)。

ledger SHA `a753f6ef1831579858e439305677e3c4a8599b35141b9136e37099fe84d772c0`，**US$0.7820／52 image／52 judge／1 music**，另有舊 US$0.0035 reservation，低於整集 US$4.58 上限。STOP 已恢復、jobs 為空。PF020–022 舊紙審仍有效，但這一批在 PF018 退件處停住；完整 storyboard 與成片尚未完成。
