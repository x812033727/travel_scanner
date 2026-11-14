# S38 R8n｜`pf003` 同章已過插圖重用候選

2026-10-21 01:05 UTC。**作者候選，`STOP` 在位，未畫新圖或送評審。**`pf003` 原圖付款請求在私有 ledger 留有 **US$0.0035 reserved**，沒有收到圖片，也沒有可追認的 `job_id`。為避免重送不明付款，依 [Curio 三圖兩修以外的同章重圖選項](../../../.agents/skills/curio-episode/SKILL.md)讓 `pf003` 重用已收的 `pf001` 兩人挖土坑插圖；中間隔著 `pf002` 起司放進坑的近景，且 `pf003` 的問題「火追到什麼程度，才讓他選擇院子裡的泥土？」可由坑的畫面承接。旁白、來源、序列不改。

只把 `pf003.data.prompt` 和 `pf003.data.camera` 改成 **逐字等於 `pf001`**；後者現有原生 JPEG `pf001-1.jpg` 及九題 PASS、`needs_review=false`，實際沿用仍須工具核其 request key 和 judge stamp。`Stage.imageKey` 由合成 prompt、negative、尺寸、seed、參照等組成，**不以 scene ID 為鍵**；同一 look／camera／prompt 與 seed1 預計命中已付費圖片快取，卻不能先假定 `pf003` 新情境的 judge 免費或已通過，也不把舊 `pf003` reservation 抹掉。[結構化差分](verify-35-r8n-structured-diff.json)只兩葉；我定位 `pf003` 區塊逆向代回兩個舊值，原始位元組 SHA 精確回到 R8m **`980c371a793bfe3f4d2772d6d002309026a8cbd8874187ab8cd1d8fdeba82065`**。R8n SHA **`df05f4a886abfe18018a85db948623cfe96537940c5ed7cf1f71461752bb1e35`**、`visualHash` **`721f73508d3d3870`**。`pf007` 日記卡與 `pf005` 1,600ms 停頓保持 R8m 已獨立覆核內容；劇本、主張、音檔也未改。`lint --slug curio-s38 --json` **0 errors／0 warnings**。

目前 S38 ledger **US$0.3300**（20 image、18 judge、1 music，含舊 reservation）；整集原硬上限 **US$4.58**。`STOP` 仍在，R8n 尚無有效完整 storyboard manifest；`pf003` 缺已收圖，`pf007` 舊原生圖已判退。請非作者先獨立比對 `pf001` 原生圖與 `pf003` 問句、精確差分、cache key 條件、額度與源頭；紙上 PASS 後才可在工具下指名 `pf003` 重新判定，僅預期 image cache、不可預宣 image/judge 全免費。第一章新停頓 30.20 秒尚需成片聽感確認，其餘景、網站音訊／分鏡審核及成片仍 HOLD。
