# S38 R8t｜PF015–022 付費測試三張即停，原圖三張 REJECT

2026-10-22 UTC。依 [八景書面預檢](verify-62-r8t-pf015-022-independent.md)，在私有 STOP 邊界中**逐景只試 PF015、PF016、PF017 各一次**，每次打開完整 1280×720 原生 JPEG 和裁邊版，再決定是否購買下一景。**三張原圖人工全數 REJECT；成年人物／1666 年代與場景失準已在三張連續出現，立即停止。** PF018、PF020、PF021、PF022 雖書面 PASS，未生成、未付費、未有原圖 KEEP；PF019 書面 HOLD，始終未列入付費清單。下一章沒有啟動。

## 逐張未裁切原圖

| 景 | 原圖 SHA-256；裁邊版 SHA-256 | 機器／人工判斷 |
| --- | --- | --- |
| PF015 | `ba0314616dab1887ee7b532c87dbe42a6888c0745baa09e223c8d590b69dd7f7`；`512f142b79eb770f2f23fa709fe4d1c502cc31f29d6b670cc3298d2d1f268823` | 機器 **8.71/10 FAIL**；人工 **REJECT**。塔上人物下方是現代筆直柏油路、近代多層樓與一輛在火／煙下的汽車，不是 1666 年倫敦；原圖又有上下黑色寬帶、背景偏寫實，裁邊不能修年代或風格。 |
| PF016 | `3b7ca7dba4d930c428ddd07dae234b4b9730eeb17a43601daa1eb9f2209253c0`；`4b321b92b440d9de9de9bcd0532dbb768a574496ec63f83c52e8b6f6c1cbabe3` | 機器 **9.29/10 PASS**；人工 **REJECT**。兩個童貌人物穿東亞式制服／帽飾，背景地圖有偽漢字與現代展示感的光源。它既不是 1666 年倫敦塔官與成年佩皮斯的可信畫面，還把 prompt 的無字概念圖變成有字道具；不能拿來表現**口頭**消息。裁邊版保留全部問題。 |
| PF017 | `bb9a237e8d951cf5be36f9d45ad5dacf5052db913bca7755780ba10d576fe673`；`9a1c12559d15656eb658dfcc2053cf744d13c82f2cebd4532b81d6399ec71d97` | 機器 **9.29/10 PASS**；人工 **REJECT**。原 prompt 只有一名沉思的成年 diarist 望塔窗外煙，原圖卻有多個近似少年面容的人擠在窗邊，衣著看不出 1666 年英國身分；主角不可辨。石窗和煙不足以抵銷成年人／角色／年代失準，裁邊後也一樣。 |

PF015 的近代街／車、PF016 的童貌東亞制服、PF017 的童貌多人均屬**成人與年代錯置**的重複類型；已達三張停止門檻。PF016、PF017 的 `needs_review=false` 只反映自動評審，絕不等同人工 KEEP。三景的書面史料主張仍可追溯佩皮斯 1666-09-02 日記，失敗發生在生成畫面。PF019 的 `near city Bridge` 風險仍獨立 HOLD。

## 執行邊界與私有收據

批前 STOP、ledger、manifest 與九張 KEEP entry 基線私存 `/workspace/.video-work/curio-s38/review/r8t-pf015-022-pre/`。每張都只用 `NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work PLAYWRIGHT_BROWSERS_PATH=/workspace/.video-work/playwright-system node tools/video/cli.mjs keyframes --slug curio-s38 --shot <單一 ID> --takes 1`；命令在 EXIT trap 中暫解並恢復 STOP，執行前拒絕重複原圖／日誌，無 `--force`、seed offset 或第二 take。各 ID 的完整 log／exit 存私有 `review/r8t-first-chapter-pf015.*`、`pf016.*`、`pf017.*`；退出碼皆 `1`，PF016／PF017 是**既有 PF015 內容關卡未過**使整個圖單仍失敗，不代表它們沒有生成或機器未 PASS。批後 STOP、ledger、manifest、三張原圖／裁圖及日誌備份在 `review/r8t-pf015-017-post/`。

私有 ledger 由 **US$0.5830／38 image／37 judge／1 music** 增至 **US$0.6235／41 image／40 judge／1 music**，恰有 PF015–017 各 US$0.0035 圖與 US$0.01 評審，追加 US$0.0405，仍低於整集 **US$4.58** 硬上限；舊 PF003 US$0.0035 reservation 未動。新 ledger SHA-256 `86bf09c92238cfc7ff44001955c19bf6cd5e580e64bc52e342ea91f0c1bca6c4`。新 manifest SHA-256 `121fa94cb357ee891b1c8c4b01df909753a536f9b58bc6b69d1decd39c81fcfa`，只含九張先前 KEEP 和三張本輪退件圖；九張 KEEP 的 manifest entries 與各所選檔案 SHA 對批前逐項不變。R8t 的 PF009／013／014 是卡片，其舊退件圖片不在新 manifest 內。STOP 已恢復在位。

`video.json`／`script.md`／`claims.md` SHA-256 仍是 `35a23a36a8503988bdb70ff2dc2c6e3bd2f02c226891a5119f3b9756b86d2532`／`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`／`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。後續只依 [停止後任務](verify-64-r8t-pf015-022-next-task.md)重新做窄範圍候選與獨立書面覆核；**本次不再付款**。
