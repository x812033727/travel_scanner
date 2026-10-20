# X15｜Garmin：導航機被手機擠壓後，另一張營收表怎麼長出來？

狀態：**一手來源企劃及 v3 逐句 SEC 審查 PASS；v3 兩份敘事盲讀均 HOLD。v4 已針對開場、章節銜接與後段清單感改寫，待新的獨立逐句 SEC 審查與兩份同版敘事盲讀。沒有媒體、成片、YouTube 連結或 PR。** 本集取材自已查核的 100 題清單 C15，但作為 X15 獨立製作，不改 C15 的企劃或其 SHA 綁定審稿。現有 X01–X14 沒有 Garmin 主角。

主問題：2008 年 Garmin 的車用／行動事業占營收逾七成，單是 nüvi 產品系列就占約 64%。2008 年報說手機導航**可能**拖慢成長；2011 年報已改說手機 GPS 和導航軟體的普及**已**使其成長停滯。當這門高度依賴的生意遇到手機與新車內建導航，Garmin 後來靠哪些業務形成了不同的營收結構？

`source-matrix.md` 記錄 2026-10-20 實際 HTTP 下載的 SEC 原始 HTML、逐檔位元組與 SHA-256、可支持主張及禁區；[獨立來源企劃收據](reviews/source-audit-independent.md)重新下載 G1–G7 並逐項核對，結果 PASS。`treatment.md` 給一條事件線、六章節拍；`script.md` 與 `video.json` 是 v4 已編譯的 144 句主片；`shorts-script.md` 與 `shorts.json` 是兩支各 9 節拍的獨立短片，[直式構圖交接](shorts-portrait-plan.md)指定重用鏡頭的首次裁切及文字安全區。作者逐句來源標記見 `line-source-matrix.md`、`shorts-source-matrix.md`，**不能當成另一人的逐句來源審查 PASS**。六份核心 SEC 原件均低於工人 3 MiB 讀取門檻；2023 10-K 僅供編輯者交叉核對。

目前 v4 凍結 `video.json` SHA-256：`4ada054a0a6e3c1e396e1ecc8cf8550d6ff9c0a72bab0062e29ef02c5b582e00`；`shorts.json` SHA-256：`9dc9be2a237ea6aabbd60d3268351ee16ea72daa54f0f6822e5c5990788b9d2e`。主片有 97 個匿名插畫 shot、15 張精確後製數字卡、18 個有句 ID 的掛問／回收；兩支 Shorts 用主片 shot 做來源，直式字卡仍需正式製作。主片 lint 0 errors／0 warnings，兩支 Shorts schema／來源驗證均通過，18／18 重用鏡頭有獨立直式構圖指示；詳見 [視覺規劃](visual-plan.md)與 [US$25 護欄](production-quote.md)。[v3 逐句來源 PASS](reviews/script-source-audit-v3-independent.md) 只綁定舊版 SHA；[盲讀 A](reviews/blind-a-v3-independent.md)與 [盲讀 B](reviews/blind-b-v3-independent.md) 均 HOLD，指出場景開場、重複但書、後段目錄感及估時過長。更早 v1、v2 的 HOLD 收據也保留。下一關由**沒有撰寫 v4 逐句稿的代理**按同版 JSON SHA 重新讀 SEC 原件，核對所有口播，再交兩名新讀者做同版敘事盲評。

既定規格是 MiniMax `image-01`、精確 `look: {"preset":"cute-mystery"}`、實質正文至少 8 分鐘且總片目標約 10 分鐘、每 30–45 秒一個實質鉤子、濃縮開場後正式 5 秒片頭、結尾三句後 21 秒 v4 片尾、可關閉繁中 CC、橘色大字 `Garmin` 縮圖、整支不超過 US$25。v4 實質正文 2,415 個稿文字元按 300 字元／分鐘約 8:03；lint 的 250 口播單位／分鐘估開場 0:48、正文 9:37、末三句 0:19，另加 5 秒片頭與 21 秒片尾約 11:10。這些是紙面估值，不是實際 TTS 或成片時長。正式成片前必須測量與調整；動畫資產與真實影片網址只在取得後填入。

核心界線：2008 年的 automotive/mobile **不等於只有車用導航機**；手機不是 2008–2010 收入下滑唯一可證原因，年報還指出市場滲透、售價、新車內建導航和景氣。2011 年「has halted our growth」是公司風險揭露的判斷，不是本片獨立估計的因果效果。2025 年的 `Auto OEM` 是另一個現行部門，不能拿它的 9.2% 直接當舊部門從逾七成跌到一成的證據。2025 總營收是 2008 的約 2.07 倍；這是不同年份的名目美元比較，不是同範圍產品的成長率，也不證明單一手錶型號救了公司。
