# S38 `pf009`–`pf022` 首輪：六張即停，全數原生退件

2026-10-22 UTC。依 [第一章批次開畫前檢查](verify-47-first-chapter-art-batch-preflight.md)以一次抽樣執行 `pf009`–`pf022`。**在 `pf009`–`pf014` 六張裡，成人年齡／時代錯誤重複出現，立即送出私有 `STOP`；CLI 在下一個安全檢查點停止，`pf015`–`pf022` 沒有生成。六張原圖人工均 REJECT；五張機器 PASS 不能進成片。**本頁不放行整集分鏡。

## 有界執行與帳本

開畫前 `video.json` SHA-256 `8db80e07bffff8863f949e4a458b9fed0a891e36ed93063bce59c3915fc6e142`、manifest SHA-256 `39dd823c0763f599bdeb5a76af6a3d5ad9f8eedda1e87b1d8b9e415f4a946b6c`；兩者及帳本、STOP 已私有備份於 `review/pf009-022-pre/`。`--dry-run` 回報 14 張各一次約 US$0.1890、MiniMax `image-01` ready、提示詞都在長度內。執行時只使用 `--shot pf009,pf010,pf011,pf012,pf013,pf014,pf015,pf016,pf017,pf018,pf019,pf020,pf021,pf022 --takes 1`，沒有 `--force` 或 seed offset；外層 `EXIT` trap 恢復 STOP。設了 `PLAYWRIGHT_BROWSERS_PATH=/workspace/.video-work/playwright-system`，但批次因 STOP 提早結束，尚未進到產聯絡表的步驟；本輪直接看了六張未裁切原生 JPEG 及裁邊版。

私有 ledger 從 **US$0.3805／23 images／22 judges／1 music** 增至 **US$0.4615／29 images／28 judges／1 music**，恰為六張圖加六次評審 US$0.0810；舊 `pf003` US$0.0035 reservation 仍在，遠低於整集 **US$4.58** 上限。新 manifest SHA-256 `ce54cc81f12c12c92bd8dbf1824bf17f2fbdffb5de4171fce53a820d5bd42c61`；已收 `pf001`–`pf005`、`pf008` 的完整 manifest entries 與檔案 SHA 均與批前一致。六張新圖、裁邊圖與此 manifest 已保存在私有 `review/pf009-014-rejected/`，供下一輪差分及原圖對照。

## 逐張原圖判定

| 景 | 未裁切原圖 SHA-256 | 機器 | 人工 REJECT 的實質原因 |
| --- | --- | --- | --- |
| `pf009` | `6658cb529cbf3e039b7e4edbf1f3ed7935b825f319a28cf39c3c130159c82c91` | 10/10 PASS | 小孩坐在床外地板、披毯，沒有成年佩皮斯**回床睡去**的動作；窗外還像明亮清晨。 |
| `pf010` | `115539c63f786194edf4606a767de1520f51d55fbad30e92e097c5bd618db93f` | 9.29/10 PASS | 窗邊是兩名童貌、東亞服飾人物，街景似現代樓房；不是 1666 年早上成年佩皮斯再看遠火。 |
| `pf011` | `9eef1312644d159396a76670026b3eb2429e93f6108d9615883aed7c6cb7f825` | 9.29/10 PASS | 只見一名童貌女僕拿著紙張、沒有被告知的佩皮斯；日記是 Jane **口頭**轉述聽來的三百餘屋，畫面易暗示書面消息。 |
| `pf012` | `31afc253b164065d1d96684fec2fb0c89431ac378952bb31b3425c3d72dfab74` | 10/10 PASS | 兩名童貌女性和手冊／紙本，沒有佩皮斯，與「他聽說後得自己去看」的角色與口頭層級不符。 |
| `pf013` | `ff37b4867c2dcb1cd8b963367cd800da309d110710fa87cedff2e9f17555c730` | 9.29/10 PASS | 塔上主角明顯是小孩；雖有石拱橋及遠火，不能當成年佩皮斯的目擊畫面。 |
| `pf014` | `2408d3250410abbe27f2257e1c874eacc03387215b3357ca880189310e2b5bdd` | 9/10 FAIL（frame=0、details=7） | 又是小孩，且後景把 1666 年 London Bridge 畫成吊索／懸吊結構，原圖有黑色上下寬帶；這不是來源中佩皮斯在塔上掛念熟人家的時代畫面。 |

機器給前五張 `needs_review=false` 只表示其自動題目通過，**不代表人類 KEEP**；六張都不得用於成片或站主分鏡審核。這次不是挑剔卡通頭身比例：PF009、PF011、PF012 的主動作／角色／消息媒介明顯錯，PF010、PF013、PF014 的童貌與年代建築錯會誤導史料。PF014 的裁邊版去掉黑帶，也無法修正孩童與橋型。

## 接續限制

這是系列畫風下的**系統性成年人物與時代失準**，同批六張全退，超過 [開畫前策略](verify-47-first-chapter-art-batch-preflight.md)對下一批的停止門檻。先對 `pf009`–`pf014` 依具體錯因窄修 `data.prompt`，保留日記的時間、人物、口頭／親見界線與 `look.preset`；另人核精確差分後才可定點重試。`pf015`–`pf022` 尚未花錢，宜在看過修訂後的成年／年代小批原圖之前先暫停，避免同類錯誤擴散。不要直接對五張機器 PASS、人工 REJECT 的原 prompt 再跑 `--takes 2`，工具會沿用其「已通過」判定，未必生成新圖。私有 `STOP` 現在存在；站台音訊／分鏡核准、完整插圖、片頭片尾、字幕、Shorts 與 Studio 可點連結仍未完成。
