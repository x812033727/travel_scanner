# S38 R8aa｜PF018 第二張實際原圖退件停線

2026-10-22 UTC。PF018 [單景窄修獨立紙審](verify-89-r8aa-pf018-independent-paper.md) PASS、[離線圖單重綁](verify-90-r8aa-pf018-offline-rebind.md)保全 11 張 KEEP 後，只付費試 PF018 **一張新原圖與一次正式 judge**。CLI exit 1：judge 9.71／10 但 `detached=0`、`passed=false`，認為船上方有無依附線段。沒有試 PF020–022，也沒有推分鏡。

主代理直接看未裁切 1280×720 原圖 SHA-256 `3e1589f827837bd1196a6ebfeca11082e680b3db50944b65868147584ca6a073`：上下有顯著黑寬帶；貨箱已在船板、人物的手扶著箱子，沒有畫出從岸上跨船舷搬入的動作；人物服裝與整排制式磚門窗顯得較近代。裁邊圖 SHA `9522f0b0a466399a2d671191d7266153a768f4954bb52b5cd05c8c17fdb6f478` 雖去掉黑帶，動作與年代疑慮仍在，且正式 judge 未通過。**原圖人工 REJECT**；這是 PF018 第二張實際付費原圖，新 prompt 的 seed 1 不代表首次嘗試。

在 STOP 在位、jobs 空時，先把 CLI 後 12 筆 manifest SHA `82ddc94e6c44bc0a79ad420852dde8257317adcaa1721489e3515d5381975991` 與新原圖／裁圖逐位元備份於私人 `review/r8aa-pf018-seed1-judge-fail/`，再只從 active manifest 移去退件 PF018、清空過期聯絡表。現行 manifest SHA `eca0cddcec00a26be05be63d6d62e6ce71f57e775595dbd74a02ba1cd5f0e507`，仍綁 R8aa visual hash `819c6ff2d7c16ad0`；11 張 KEEP 完整條目 canonical SHA `59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301` 與每張選圖 JPEG SHA 未變。[隔離清冊](verify-91-r8aa-pf018-seed1-fail-inventory.json)逐項列出前後雜湊。

ledger SHA `c40120e6801716b79f867d873c4d2068ca2afd51ebdf379387f9b659a011594a`，**US$0.7955／53 image／53 judge／1 music**，另有舊 US$0.0035 reservation，低於全片 US$4.58；STOP 恢復且 jobs 空。若繼續 PF018，僅允許再做一次有來源的提示詞窄修、另一位獨立書面核對及最多**第三張／最後一張**原圖；再退就改同章合格圖或來源卡，不購第四張。
