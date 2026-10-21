# X19｜Uber 外送交易額反超載客：離線前製交接

**狀態：v7 事實通過、敘事 HOLD。** [v7 獨立 SEC 查核](reviews/script-source-audit-v7-independent.md)重新抓取十份原件並通過事實界線；兩名新首讀者 [A](reviews/blind-a-v7-independent.md)／[B](reviews/blind-b-v7-independent.md)都對必答 Q8／Q13 判 No，B 另對 Q7 判 No。反覆講部門與公司帳的差別、App／雜貨／台灣旁枝和司機問題未獲實際結果，是下一版需要修的地方；改稿須重凍結並再做來源與雙盲審核。本包沒有實際配音、官方動畫素材、已生成插畫、MP4、上傳或真實影片網址。

[六章 Treatment](treatment.md)、[brief](brief.md)、[110 句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 JSON](video.json)。十份 Uber 向 SEC 提交的工人可讀原件、2026-10-20 原始 bytes／SHA 和動態 script tag 的後續比對界線見 [source-matrix.md](source-matrix.md)；[逐句來源](line-source-matrix.md) 是作者標記，尚不是 v7 獨立審核 PASS。兩支**不同題目**的 8 拍 [Shorts JSON](shorts.json)、[短片稿](shorts-script.md)、[短片來源](shorts-source-matrix.md)、[9:16 裁切方案](shorts-portrait-plan.md) 同包。[逐鏡方案](visual-plan.md)、[全片 US$25 試算](production-quote.md) 與 [正式製作／動畫／連結交接](publishing-handoff.md) 說明後續門檻；沒有宣稱本機持有官方素材。

主片六章 **95 張** `image-01`、`look: {"preset":"cute-mystery"}` 的無品牌靜態插畫，**12 張**原生數字卡和 1 個結尾槽，插畫占正文 107 槽的 **88.8%**，生成影片 clip 為 0。第 1 章濃縮 187 字，本機 lint 估約 **45 秒**，其後交接頻道既有 v4 **5 秒動畫片頭**。第 2–6 章紙面 **2496 字**，按每分鐘 300 字約 8:19；主片 lint 粗估總長 **11.3 分鐘**。兩支 Short 各 163／171 字，約 33／34 秒。這些都不是實際成音長度；正式機必須以 TTS timeline 驗正文**至少 8:00**、短片各 **25–55 秒**，按成音剪輯。最後恰三句答題、留言、訂閱，其後接官方 v4 **21 秒動畫片尾**；最後 16 秒在 Studio 設定並測三個可點結束畫面目標，真實主片／Short／播放清單 URL 待上傳後回填。

讀財報時需分清四欄：2020 Q2 Mobility／Delivery Gross Bookings **US$3.046bn／US$6.961bn**，全公司 Revenue **US$2.241bn**，Delivery 部門非 GAAP Adjusted EBITDA **−US$232m**，全公司 GAAP 淨損 **US$1.775bn**。2021 Q2 Delivery 部門同尺度仍虧 **US$161m**，與一年前同季比收窄 **US$71m**，但部門合計帳**不能拆出 Postmates 的單獨損益影響**。後段仍沿兩條交易額追蹤；2022 Q4 載客金額大於外送只證明那一季，不能宣稱首次重超。片尾的新答案是同一季 Mobility／Delivery **部門調整後 EBITDA +US$1.012bn／+US$241m**，不能推成全公司 GAAP 淨利。Postmates 的 **7 月 6 日簽約**及 **12 月 1 日完成**均在六月季度之後，日期另有同期 8-K 封面 S3a／S5a 支持。

離線重建與驗證（repo 根目錄）：

```bash
node docs/videos/story-everyday-uber-x19/compose-video.mjs
node docs/videos/story-everyday-uber-x19/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-uber-x19
npm run test:docs-videos
npm run check:tasks
git diff --check
```

將 `shorts.json` 陣列分成兩個暫存單檔後，逐支用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-uber-x19` 驗 schema 和主片 shot SHA；composer 也直接執行 `episodeShortsProblems`。本版主片 lint **0 errors／0 warnings**，`episodeShortsProblems` **[]**，兩支 Short schema／shot hash 均通過；`test:docs-videos` **236／236**、`check:tasks` exit 0（只有倉庫既有任務警告）、`git diff --check` 通過。修改原因與剩餘審核門檻見 [v7 作者修訂對照](reviews/v7-author-response.md)。下表為本次候選稿**實際檔案** SHA-256；審稿、重編或修字後都須重算，不沿用舊審核結論。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `f4e373a53a3424f29f9c3e511f13c2489ac9c7e93c4500413038060d8d08a385` |
| `shorts.json` | `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95` |
| `series.json` | `6c4944e5db4cccd4e8cee3adc286e9afb630118eb7f9e4e513cee5bbb9bf7c9d` |
| `drafts/narration.md` | `959b8da99002f86239897d52fbc2559b22bf040f179bc8d3e91178fccf965d6f` |
| `source-matrix.md` | `5e949609bf8163b28cfeea3ca3592c52855e6ece34f52f3da37549efe3d31043` |
| `visual-plan.md` | `137cd29316b1ec634d299f23b543974a865d77415916ea2d83ae8afad0c668ee` |
