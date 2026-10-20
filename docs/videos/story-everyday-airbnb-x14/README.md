# X14｜Airbnb：預訂少四成後，平台怎麼走到首個全年獲利？

狀態：**離線前製 v4 逐句稿，待同版獨立逐句來源覆核及兩位新讀者盲評；尚無成片或 PR。** v1–v3 的獨立來源審查和盲評收據都未放行，舊收據僅保留歷史記錄。本集與 X01–X13 分開製作，不改原先核准的 100 題及它們的 SHA 綁定審稿。那份題庫 100 個 `stories` 中沒有 Airbnb；已在做的獨立 X01–X13 分別是 Adobe、Domino's、Netflix、Beats、Meta、WD-40、GoPro、Target、BlackBerry、eBay/PayPal、FedEx、Peloton、Spotify，沒有同一主角。

主問題：2020 年 3–4 月期間合計，Airbnb 平台上取消的夜晚與體驗席位，比同期新預訂的總量還多。訂單全年比 2019 年少 41%。到了 2022 年，平台卻公布首個按 GAAP 計算的全年淨利。這兩年間，房東、產品呈現、旅行需求和公司成本各發生了什麼？答案不能寫成「長住救了 Airbnb」或「砍人就帶來獲利」；原件只支持多個同時變化的事實，不能把其中一個算成獨立因果。

本階段交付：`source-matrix.md` 記錄 SEC 原始 HTML 的網址、取得位元組數、SHA-256、主張與限制；`treatment.md` 是一條事件線與六章節拍；`drafts/narration.md`、`drafts/shorts.md` 是逐句稿。`compose-video.mjs`、`compose-shorts.mjs` 可重建 `video.json` 與 `shorts.json`；目前 v4 影片 JSON SHA-256 為 `23f057225c826b5687559fb7a47ea58c5b00eeb342f460a9c8a5484de1b84a62`，Shorts JSON SHA-256 為 `545a0844636cbc769afb9254824a6a68bbaf0006ebcbbe37b58344ae5a04252c`。Shorts 稿文字未改，但所引用的長片插畫鏡頭已按 v4 更新，仍須同版重審。這兩個雜湊是本輪**待審**鎖版，審查後如有改稿必須重新生成和重審。四份核心來源皆小於工人 3 MB 讀取上限。2022 10-K 另作審稿者交叉核對，超出工人上限，不讓它承擔工人稿的唯一證據。

目前編譯結果：135 句旁白、27 張後製數字卡、105 個待生圖插畫鏡頭和 19 個掛鉤；濃縮開場 228 字、扣除開場與最後三句的正文 2,696 字，按每分鐘 300 字**紙面估計** 8:59，正式音訊仍須實測。兩支獨立 Short 分別 169／189 字，須實測 25–55 秒。`node tools/video/cli.mjs lint --slug story-everyday-airbnb-x14` 回 0 error／0 warning；v4 文件測試 236/236，task check exit 0。下一關由未參與撰稿的代理重新下載原件、逐句查核，兩名不看 Treatment 的讀者作獨立盲評；審過再按[整片預算](production-quote.md)與[製作交接](publishing-handoff.md)進媒體。站主既定規格：`MiniMax image-01` 加精確 `look: {"preset":"cute-mystery"}`、故事正文至少 8 分鐘且目標約 10 分鐘、每 30–45 秒有實質新鉤子、開場濃縮後接正式 5 秒片頭、正文後接 21 秒片尾、繁中可關閉 CC、左上大字橘色 `Airbnb` 縮圖品牌名、整支付費成本不超過 US$25。正式片頭片尾資產與 YouTube URL 只在實際產出後填入。

選題邊界：2020–2022 是旅行重開、產品調整、成本管理與會計基期共同作用的時段。2020 年的 GAAP 虧損含上市相關非現金費用，不能拿 2022 與 2020 淨利差額當「疫情損失被賺回」；2021/2022 的長住比例是第四季 **gross nights booked**，不是全年客數；平台 GBV 包含房東收入等，與 Airbnb 收取的服務費收入不同。2019／2020／2022 年底的 active listings 計入住宿或體驗刊登項目，不是純住宿房源，更不能從兩個總數推論同批提供者或實際進出。
