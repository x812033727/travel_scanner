# H10 四語上傳包與後台送審收據

日期：2026-10-17（Asia/Taipei）。本收據更新 [交付預檢](delivery-preflight-1.md) 的日語停點；先前收據保留當時狀態，不回寫歷史結果。

## 授權及日語定向重錄

站主核准 H10 多語新增 US$0.20，將 H10 多語估算停手上限由 US$2.00 提高至 US$2.20、H10 全集上限至 US$8.20、五集總上限至 US$41.70。共用帳本在付費呼叫前預留這 US$0.20；供應商實際帳單不可見，保守估算仍計入停手額度。

`dub --slug curio-h10 --locale ja` 只重錄 `he2b2172`，實際 1 次 Gemini 合成、37 計費字元，其他 79 個請求沿用快取。新版逐句音檔 SHA-256 為 `D2090338789D01CFAF7671366DEB615A300B784736014BF03DE38DAE1236B3A4`，整條日語 M4A SHA-256 為 `D2076C411A0046442B1FB7D3EABA58562B721FBAF3B1997A478DCC0195B1A86A`。`check-audio --slug curio-h10 --locale ja` 只新增 1 次 Gemini 轉寫、0 次 Jev 呼叫；`he2b2172` 轉寫為 exact，整體 45 exact、14 Jev accepted、23 flagged。這 23 句是站主先前已試聽接受的舊句；站主也在本次試聽後回覆「新句旁白可以」。機械 QA 的非零結束碼代表保留舊旗標，不能解讀為這句重錄失敗。共用帳本的 `h10-dub-ja-one-line-20261017-01` 已核對為 `reconciled_estimate`，沒有把 US$0.20 重複加入估算支出。

## 上傳包核對

重新執行 `captions --slug curio-h10`：繁中 102、英文 122、日文 123、韓文 124 段，四語 `problems: []`；英文、日文、韓文均採各自配音時間軸。日文 SRT SHA-256 為 `2A0AD74694C333AB801A86B86101F91A1970FCA63C586B346F623F7754A19B8B`。

`package --slug curio-h10` 通過 4／4：已核准繁中成片 `final.mp4`、主縮圖與英／日／韓三語縮圖、四語字幕與標題說明、三語配音齊備。成片 SHA-256 仍為 `912F39E5DF15E0FEC7AADE44FE6872B28E8C6E5E9EDA63F60EEECB7E4949017C`；`upload/metadata.json` SHA-256 為 `38974F680B2425D2A2CEBDA76DEFDFDE3CFB445AF9BDEEF18C21F64A745DB96E`。

## 後台審核狀態

已依序送出最新版 `publish` 卡 `c6384662-a373-432f-a948-8469514fa9e1`（綁上述 metadata SHA）與 `languages` 卡 `bbbf9132-7b42-4903-85a8-70d3c00add49`（`review/languages.json` SHA-256 `1072CB291D615C8EC59AF2689686C281C86E632F513C6C8816B1B83E9A8C8F9E`）。`review-pull` 分別讀回「waiting for the owner」，後台持久狀態也顯示兩張 pending，九個英／日／韓語言項目為 ready。站主已收到核准請求；未讀回核准前不能稱為可上架。

本輪未向 YouTube 上傳。後台 `youtube_video_id` 仍為空；上傳由站主在 Studio 操作，完成後須記錄影片 ID 並試播四語，才能把 H10 標為已交付。

## 站主核准後的讀回

站主在對話中確認兩張最新版卡。初次 `review-pull` 仍讀到兩張 pending；進一步查看後台才確認，語言卡目前的按鈕是「我已經在 Studio 傳好這些配音」，不能在影片與音軌尚未上傳時按。依站主已給的上傳包核准，在後台按「確認可以上架」後，畫面顯示「可以上架」，`review-pull --gate publish` 也讀回 `upload package approved (metadata.json 38974f680b24)`。語言卡保持 pending，等三語音軌在 Studio 實際上傳後由站主確認；這不是語言素材未完成。

H10 目前仍沒有 YouTube 影片 ID，也沒有四語 Studio 播放驗證。已交付 `upload/UPLOAD.md` 給站主，請其由 Studio 上傳為私人影片、加入三語配音及縮圖、回填新網址並切換四語試播；不得把後台「可以上架」誤記成已上架。`npm run check:tasks` 通過。`npm run test:docs-videos` 為 214 pass／1 fail；唯一失敗是已由任務 `2026-10-16-fix-windows-unicode-path-crash-in` 追蹤的 Windows Node 24.13.0 `package-runtime.mjs` 子行程退出 `3221226505`，單測重跑仍同樣失敗，與這次 H10 媒體／文件變動無關。
