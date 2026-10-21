# X19 Uber｜正式製作與連結交接

這份工作包是**v5 離線候選稿**。v4 的[獨立 SEC 來源票](reviews/script-source-audit-v4-independent.md)對舊 SHA 判事實 PASS；兩位首次[盲讀 A](reviews/blind-a-v4-independent.md)／[B](reviews/blind-b-v4-independent.md)均判 Q8 重複與 Q13 旁支 HOLD。v5 刪掉服務／客群清單與重複排名，讓縮減虧損市場、餐廳進站和交割後未公開的配送成本沿同一手機主線發展。**舊票不能轉移到 v5 新 SHA**。目前沒有真實 TTS、插畫、正式動畫、合成 MP4、影片 ID 或上架網址。不能把 schema 通過或作者來源矩陣寫成 v5 已通過事實審、已開工或已發布。

**審稿先核時間線與尺度。** 另一位審稿者重抓 [`source-matrix.md`](source-matrix.md) 的 SEC URL，核原始 byte／SHA，逐句查 [`line-source-matrix.md`](line-source-matrix.md) 和 [`shorts-source-matrix.md`](shorts-source-matrix.md)。重點是 2019／2020 Q2 對照的 **Gross Bookings 美元交易額**；Rides／Eats 改名 Mobility／Delivery；2020 Q2 US$6.961bn＞US$3.046bn 的口徑及 −75%／+106% 的報告幣別；同季營收、部門 Adjusted EBITDA、GAAP 淨損分開；2020 Q1 司機跨接、五月初退出八個虧損 Eats 市場、免新餐廳啟用費的**不同時點**；Postmates **7 月 6 日簽約、12 月 1 日才完成**，日期另由 S3a／S5a 8-K 封面支持；2020 Q3 合作餐廳同比逾七成、新增自家網站接單入口，十多國含台灣只屬 **11 月 5 日公告時**狀態；2021 Q2 遷移數不當留存或新增訂單、美國非餐廳配送六月交易額與 2020 年 12 月之比；2021 Q4 外送部門單季調整後轉正；2022 Q4 載客交易額重新較大及兩部門調整後 EBITDA **+US$1.012bn／+US$241m**，不能當作公司 GAAP 淨利，也未查每季何時首次重超。兩位新讀者先盲讀**相同 v5 JSON hash**，再依正式規則投票；需要改字就重編並重審。

**正式機接手。** 審核過後先按 [`production-quote.md`](production-quote.md) 讀回所有付費路由和 US$25 全片停損，再生成並審核 95 張 `image-01`、精確 `look: {"preset":"cute-mystery"}` 的概念靜態插畫；至多 30 次有理由重畫、每鏡至多 3 次嘗試，0 支生成影片 clip。日期、品牌字、精確金額只在原生後製模板排。台灣自然國語單人 TTS 按 `video.json` `say` 試讀 **Uber Eats／Postmates／EBITDA／App**；若需修音改 `say` 和 `say_for` 後再凍結。按實際聲音 timeline 驗**實質正文 ≥8:00**、濃縮開場 30–60 秒、兩支 Short 各 25–55 秒，字幕生成可關閉的 zh-TW CC 並逐字對齊，不燒在圖上。正文若不足，只能有來源的新資訊補充，不用慢速或長空白卡。

**官方動畫與真連結。** 第 1 章濃縮後放頻道既有 v4 **5 秒片頭動畫**；末三句後放既有 v4 **21 秒片尾動畫**。在正式機確認媒體來源、時長、比例、音量與授權；本包沒有動畫檔，不生成替代品。片尾末 16 秒在 YouTube Studio 放「最符合觀眾喜好」影片、訂閱、「最新上傳」影片三個結束畫面目標。先私人上傳，於桌機和手機播放器逐一點擊測可用，再確認公開版。`youtube.video_id` 目前 `null`；主片、兩支 Short、系列播放清單的實際 URL 要在正式上傳後才回填描述、置頂留言及互相導流位置，逐項點擊驗收。MP4 畫面本身不是可點連結。

**離線重建。** 從 repo 根目錄依序執行 `node docs/videos/story-everyday-uber-x19/compose-video.mjs`、`node docs/videos/story-everyday-uber-x19/compose-shorts.mjs`；再跑主片 lint、Shorts 各自 schema／來源 shot hash 驗證、`npm run test:docs-videos`、`npm run check:tasks` 和 `git diff --check`。composer 僅寫本包內的 JSON／可讀稿／矩陣，不連接媒體供應商或發布平台。獨立審稿必須使用 README 凍結 hash；任何重編都使舊版結論失效。
