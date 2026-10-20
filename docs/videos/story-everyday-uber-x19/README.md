# X19｜Uber 外送交易額反超載客：離線前製交接

**狀態：等獨立來源審核與兩位敘事盲讀。** 這是品牌故事額外系列第 19 支的可重建候選稿，尚未正式生成、配音、合成、上傳或開 PR。2020 年第二季外送平台交易額反超載客，故事沿著同一支**匿名示意派單手機**走過四月轉派、六月兩欄交叉、七月 Postmates 簽約、十二月交割、次年整合與後來載客交易額再次較大。對比的是 Gross Bookings 美元金額，**不是**交易件數、Uber 營收或利潤。

[六章 Treatment](treatment.md)、[brief](brief.md)、[125 句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 JSON](video.json)。十份 Uber 向 SEC 提交的工人可讀原件、原始 bytes／SHA 和說法界線見 [source-matrix.md](source-matrix.md)；[逐句來源](line-source-matrix.md) 是作者標記，尚不是審核 PASS。兩支**不同題目**的 8 拍 [Shorts JSON](shorts.json)、[短片稿](shorts-script.md)、[短片來源](shorts-source-matrix.md)、[9:16 裁切方案](shorts-portrait-plan.md) 同包。[逐鏡方案](visual-plan.md)、[全片 US$25 試算](production-quote.md) 與 [正式製作／動畫／連結交接](publishing-handoff.md) 說明後續門檻；沒有宣稱本機持有官方素材。

主片六章 **107 張** `image-01`、`look: {"preset":"cute-mystery"}` 的無品牌靜態插畫，**12 張**原生數字卡和 1 個結尾槽，插畫占正文 119 槽的 **89.9%**，生成影片 clip 為 0。第 1 章濃縮 200 字，本機估約 **48 秒**，其後交接頻道既有 v4 **5 秒動畫片頭**。第 2–6 章紙面 **2474 字**，按每分鐘 300 字約 8:15；主片 lint 粗估總長 **11.4 分鐘**。兩支 Short 各 157／162 字，約 31／32 秒。這些都不是實際成音長度；正式機必須以 TTS timeline 驗正文**至少 8:00**、短片各 **25–55 秒**，按成音剪輯。最後恰三句答題、留言、訂閱，其後接官方 v4 **21 秒動畫片尾**；最後 16 秒在 Studio 設定並測三個可點結束畫面目標，真實主片／Short／播放清單 URL 待上傳後回填。

讀財報時需分清四欄：2020 Q2 Mobility／Delivery Gross Bookings **US$3.046bn／US$6.961bn**，全公司 Revenue **US$2.241bn**，Delivery 部門非 GAAP Adjusted EBITDA **−US$232m**，全公司 GAAP 淨損 **US$1.775bn**。Q2 2021、Q4 2021 的公司 GAAP 正數含股權重估利益，不可歸給外送；Q4 2022 載客金額大於外送只證明那一季，不能宣稱首次重超。Postmates 的 **7 月 6 日簽約**及 **12 月 1 日完成**均在六月季度之後，日期另有同期 8-K 封面 S3a／S5a 支持。

離線重建與驗證（repo 根目錄）：

```bash
node docs/videos/story-everyday-uber-x19/compose-video.mjs
node docs/videos/story-everyday-uber-x19/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-uber-x19
npm run test:docs-videos
npm run check:tasks
git diff --check
```

將 `shorts.json` 陣列分成兩個暫存單檔後，逐支用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-uber-x19` 驗 schema 和主片 shot SHA；composer 也直接執行 `episodeShortsProblems`。本版主片 lint **0 errors／0 warnings**，兩支 Short 驗證通過，`test:docs-videos` **236／236 通過**，`check:tasks` exit 0（只有倉庫既有過期任務與範圍重疊警告），`git diff --check` 通過。下表為本次候選稿**實際檔案** SHA-256；審稿、重編或修字後都須重算，不沿用舊審核結論。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `0f1a2b9902b36fd9a050f96aa5321a1ddba67928cae6bf2bbff2aed63c9cf2c8` |
| `shorts.json` | `5b53405aa140922ccf8e0543733133e9d11e4472ae33ce701d93b6ac7cefee2e` |
| `series.json` | `6c4944e5db4cccd4e8cee3adc286e9afb630118eb7f9e4e513cee5bbb9bf7c9d` |
| `drafts/narration.md` | `62e964be887d328bd1cf5519826620922c3a1cf1228f586e81b23567a6ae1336` |
| `source-matrix.md` | `3aec8274dceee908e4b3fca1598b814d2d97f285f0bd65fc96d414720c698bf0` |
| `visual-plan.md` | `8190e47ccc52e468119875b8279682858bdd99e89a61ea320095bc4705494925` |
