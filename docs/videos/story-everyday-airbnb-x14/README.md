# X14｜Airbnb：預訂少四成後，平台怎麼走到首個全年獲利？

狀態：**離線前製 V5，等待同版獨立 SEC 逐句來源覆核與兩名新讀者盲評；尚無成片或 PR。** V4 來源審查在 `reviews/script-source-audit-v4-independent.md` 通過，但兩份獨立盲評在 `reviews/blind-a-v4-independent.md`、`reviews/blind-b-v4-independent.md` 均 HOLD；舊版收據不適用 V5。Airbnb 不在原核准的 100 題或另行製作的 X01–X13 主角中，本集獨立交付。

主問題：2020 年三、四月**合計**，Airbnb 取消的夜晚與體驗席位超過同期新預訂；2022 年卻公布首個 GAAP 全年盈利。故事跟著一張**抽象的**住宿日曆，從取消通知、旅客退款與有限房東支援，走過貸款、縮編、附近住宿呈現、長住與遠行的回歸。SEC 原件不能把任何單一措施算成獨立獲利原因，也不能從活躍刊登項目總量推知同一批房東是否留下。

`source-matrix.md` 保存 SEC 原始 HTML 的網址、位元組數、SHA-256 和口徑限制；`treatment.md`、`drafts/narration.md`、`drafts/shorts.md`、`visual-plan.md` 是可審的製作稿。用 `node docs/videos/story-everyday-airbnb-x14/compose-video.mjs` 再執行 `compose-shorts.mjs` 可重建 JSON、逐句稿與來源表。**V5 凍結 SHA-256**：`video.json` `e38a12eef5f51da9eb13b8a1cab3bb7b7fdc867889e7580ae1c11cd1b961c199`；`shorts.json` `b581e9f717769bace170833d8ef48c36b7b499fcf306baaa40542dffbf31ac2e`。任何改稿都須重新生成並讓新審查綁定新 SHA。

目前編譯為 119 句旁白、26 張原生數字卡、90 個待生圖插畫鏡頭、19 個問題與回應掛鉤。濃縮開場 158 字；扣除開場與最後三句的實質正文 2,429 字，按每分鐘 300 字**紙面估計** 8.10 分鐘。按工具每分鐘 250 spoken units 及場景停頓估計，主片約 11:31，加預留正式 5 秒片頭與 21 秒片尾約 11:57；真正 TTS 和片尾檔仍未測量。兩支獨立 Short 各 169／192 字，須由 TTS 實測 25–55 秒。影片 lint 為 0 error／0 warning；文件測試 236／236 通過，task check exit 0。

[整片 US$25 預算](production-quote.md)與[動畫、字幕、連結交接](publishing-handoff.md)定義後續工作。既定規格為 MiniMax `image-01`、精確 `look: {"preset":"cute-mystery"}`、約 10 分鐘的故事片且正文 ≥8:00、濃縮開場後正式 5 秒片頭、三句結尾後正式 21 秒片尾、可關閉繁中 CC、左上橘色 `Airbnb` 縮圖品牌名與整片 US$25 硬上限。**目前沒有音檔、插畫、正式動畫工作檔、MP4 或可驗證的 YouTube URL。**

口徑防線：取消與新訂只比較 2020 年三、四月合計，不能說兩個月各自成立；旅客退款資格與房東支援的入住日期門檻分開；2019／2020／2022 年末活躍刊登項目含住宿或體驗；2021／2022 長住與跨境比例只限相應第四季 gross nights booked；平台 GBV 不是服務費收入；2020 GAAP 虧損含上市觸發的非現金費用，不能說成全部退訂成本。四份工人可讀核心來源均低於 3 MB；2022 10-K 僅供審稿者交叉核對。
