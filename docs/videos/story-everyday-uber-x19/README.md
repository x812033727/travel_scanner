# X19｜Uber 外送交易額反超載客：離線前製交接

**狀態：v3 凍結候選稿，待新 SHA 的獨立來源審核與兩位敘事盲讀。** v2 的[獨立來源票](reviews/script-source-audit-v2-independent.md)是 PASS，但[盲讀 A](reviews/blind-a-v2-independent.md)與[盲讀 B](reviews/blind-b-v2-independent.md)都判 Q8／Q13 不通過，B 另判 Q1／Q7 不通過；這些票只綁 v2 SHA，不能沿用到本版。這是品牌故事額外系列第 19 支的可重建離線稿，尚未正式生成、配音、合成、上傳或開 PR。2020 年第二季外送平台交易額反超載客，故事沿著同一支**匿名示意派單手機**走過第一季 App 調整、四月司機跨接、六月兩欄交叉、七月 Postmates 簽約、十二月交割、次年整合與後來載客交易額再次較大。對比的是 Gross Bookings 美元金額，**不是**交易件數、Uber 營收或利潤。

[六章 Treatment](treatment.md)、[brief](brief.md)、[119 句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 JSON](video.json)。十份 Uber 向 SEC 提交的工人可讀原件、原始 bytes／SHA 和說法界線見 [source-matrix.md](source-matrix.md)；[逐句來源](line-source-matrix.md) 是作者標記，尚不是 v3 審核 PASS。兩支**不同題目**的 8 拍 [Shorts JSON](shorts.json)、[短片稿](shorts-script.md)、[短片來源](shorts-source-matrix.md)、[9:16 裁切方案](shorts-portrait-plan.md) 同包。[逐鏡方案](visual-plan.md)、[全片 US$25 試算](production-quote.md) 與 [正式製作／動畫／連結交接](publishing-handoff.md) 說明後續門檻；沒有宣稱本機持有官方素材。

主片六章 **102 張** `image-01`、`look: {"preset":"cute-mystery"}` 的無品牌靜態插畫，**12 張**原生數字卡和 1 個結尾槽，插畫占正文 114 槽的 **89.5%**，生成影片 clip 為 0。第 1 章濃縮 195 字，本機 lint 估約 **47 秒**，其後交接頻道既有 v4 **5 秒動畫片頭**。第 2–6 章紙面 **2469 字**，按每分鐘 300 字約 8:14；主片 lint 粗估總長 **11.3 分鐘**。兩支 Short 各 163／171 字，約 33／34 秒。這些都不是實際成音長度；正式機必須以 TTS timeline 驗正文**至少 8:00**、短片各 **25–55 秒**，按成音剪輯。最後恰三句答題、留言、訂閱，其後接官方 v4 **21 秒動畫片尾**；最後 16 秒在 Studio 設定並測三個可點結束畫面目標，真實主片／Short／播放清單 URL 待上傳後回填。

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

將 `shorts.json` 陣列分成兩個暫存單檔後，逐支用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-uber-x19` 驗 schema 和主片 shot SHA；composer 也直接執行 `episodeShortsProblems`。本版主片 lint **0 errors／0 warnings**，`episodeShortsProblems` **[]**，兩支 Short schema／shot hash 均通過，`test:docs-videos` **236／236 通過**，`check:tasks` exit 0（只有倉庫既有的過期任務與範圍重疊警告），`git diff --check` 通過。下表為本次候選稿**實際檔案** SHA-256；審稿、重編或修字後都須重算，不沿用舊審核結論。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `377d045d160e46ddd2ed3eaa08d30b5ecfd45f02e6a20dd7f6f6e1526604ca48` |
| `shorts.json` | `bc2c17924498699adc6f8267ae820589ec7321c2e0f2e63e9931e10357f44c64` |
| `series.json` | `6c4944e5db4cccd4e8cee3adc286e9afb630118eb7f9e4e513cee5bbb9bf7c9d` |
| `drafts/narration.md` | `19975257b2780bd39d825bfbf1103beca8b98de03b5d92fd21bd833d18f45cd1` |
| `source-matrix.md` | `8859bbef63c8d44a8de48ae42f6e01202e65115b81d23736775392fe7ce6c1db` |
| `visual-plan.md` | `0544ece63a49b47ad5c87f85a9c3500b560a241821eca2a269db5234a9b58ec2` |
