# X19｜Uber 外送交易額反超載客：離線前製交接

**狀態：v4 凍結候選稿，待同一 SHA 的獨立來源審核與兩位全新敘事盲讀。** v3 的[獨立來源票](reviews/script-source-audit-v3-independent.md)發現一處雜貨配送國家數的日期錯置；[盲讀 A](reviews/blind-a-v3-independent.md)與[盲讀 B](reviews/blind-b-v3-independent.md)共同否決重複說明與自取餐數字旁支。本版修正了來源時點、兩個敘事阻塞點和開場過密的提問；舊票不能沿用。這是品牌故事額外系列第 19 支的可重建離線稿，尚未正式生成、配音、合成、上傳或開 PR。2020 年第二季外送平台交易額反超載客，故事沿著同一支**匿名示意派單手機**走過第一季 App 調整、四月司機跨接、六月兩欄交叉、七月 Postmates 簽約、十二月交割、次年整合與後來載客交易額再次較大。對比的是 Gross Bookings 美元金額，**不是**交易件數、Uber 營收或利潤。

[六章 Treatment](treatment.md)、[brief](brief.md)、[114 句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 JSON](video.json)。十份 Uber 向 SEC 提交的工人可讀原件、原始 bytes／SHA 和說法界線見 [source-matrix.md](source-matrix.md)；[逐句來源](line-source-matrix.md) 是作者標記，尚不是 v4 審核 PASS。兩支**不同題目**的 8 拍 [Shorts JSON](shorts.json)、[短片稿](shorts-script.md)、[短片來源](shorts-source-matrix.md)、[9:16 裁切方案](shorts-portrait-plan.md) 同包。[逐鏡方案](visual-plan.md)、[全片 US$25 試算](production-quote.md) 與 [正式製作／動畫／連結交接](publishing-handoff.md) 說明後續門檻；沒有宣稱本機持有官方素材。

主片六章 **98 張** `image-01`、`look: {"preset":"cute-mystery"}` 的無品牌靜態插畫，**12 張**原生數字卡和 1 個結尾槽，插畫占正文 110 槽的 **89.1%**，生成影片 clip 為 0。第 1 章濃縮 187 字，本機 lint 估約 **45 秒**，其後交接頻道既有 v4 **5 秒動畫片頭**。第 2–6 章紙面 **2581 字**，按每分鐘 300 字約 8:36；主片 lint 粗估總長 **11.7 分鐘**。兩支 Short 各 163／171 字，約 33／34 秒。這些都不是實際成音長度；正式機必須以 TTS timeline 驗正文**至少 8:00**、短片各 **25–55 秒**，按成音剪輯。最後恰三句答題、留言、訂閱，其後接官方 v4 **21 秒動畫片尾**；最後 16 秒在 Studio 設定並測三個可點結束畫面目標，真實主片／Short／播放清單 URL 待上傳後回填。

讀財報時需分清四欄：2020 Q2 Mobility／Delivery Gross Bookings **US$3.046bn／US$6.961bn**，全公司 Revenue **US$2.241bn**，Delivery 部門非 GAAP Adjusted EBITDA **−US$232m**，全公司 GAAP 淨損 **US$1.775bn**。後段以司機、餐廳與兩條交易額繼續故事，不把公司淨利重估利益混成外送獲利；Q4 2022 載客金額大於外送只證明那一季，不能宣稱首次重超。片尾的新答案是同一季 Mobility／Delivery **部門調整後 EBITDA +US$1.012bn／+US$241m**，不能推成全公司 GAAP 淨利。Postmates 的 **7 月 6 日簽約**及 **12 月 1 日完成**均在六月季度之後，日期另有同期 8-K 封面 S3a／S5a 支持。

離線重建與驗證（repo 根目錄）：

```bash
node docs/videos/story-everyday-uber-x19/compose-video.mjs
node docs/videos/story-everyday-uber-x19/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-uber-x19
npm run test:docs-videos
npm run check:tasks
git diff --check
```

將 `shorts.json` 陣列分成兩個暫存單檔後，逐支用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-uber-x19` 驗 schema 和主片 shot SHA；composer 也直接執行 `episodeShortsProblems`。本版主片 lint **0 errors／0 warnings**，`episodeShortsProblems` **[]**，兩支 Short schema／shot hash 均通過；`test:docs-videos` **236／236**、`check:tasks` exit 0（只有倉庫既有任務警告）、`git diff --check` 通過。修改原因與剩餘審核門檻見 [v4 作者修訂對照](reviews/v4-author-response.md)。下表為本次候選稿**實際檔案** SHA-256；審稿、重編或修字後都須重算，不沿用舊審核結論。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `5feac02ca62feb4625959c1bd8a48266d185e84ac3776783fdc3b3eddb628988` |
| `shorts.json` | `bc2c17924498699adc6f8267ae820589ec7321c2e0f2e63e9931e10357f44c64` |
| `series.json` | `6c4944e5db4cccd4e8cee3adc286e9afb630118eb7f9e4e513cee5bbb9bf7c9d` |
| `drafts/narration.md` | `f46736ea42ea147745a12b561480baa8454af530a36c0a38bd00572b1b1ab888` |
| `source-matrix.md` | `16a660e71ea51f1a9a288aee8c6598550a0c96f45e271888cf9130a6d8f4ce70` |
| `visual-plan.md` | `f26f758f7872013eb9ec76e5b2e11b3ec6eee511db5dfad68ff1bff6ca944b40` |
