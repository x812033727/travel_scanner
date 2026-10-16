# 四集 title 字卡的手機尺寸檢查

2026-10-16。此紀錄只驗 A16、A37、B14、A21 的 49 張來源字卡，使用 [來源文字候選](../readable-source-qa-20261016.md)的原樣章檔。尚未把候選接入正式工作者，也不是完整影片或手機播放器的驗收。

## 模板修改

共用 title 模板的來源徽章由 36px 增至 64px，副標由 46px 增至 64px 並提高對比；縮小卡片間距，來源標示允許換行並優先避免拆開詞語。主標大小、字卡文字、數字、限定範圍、來源映射與旁白均未修改。1920×1080 縮到 320×180 時，來源與副標的指定字級約為 10.7px；實際長行仍由 renderer 的文字適配處理，以畫面檢查為準。

## 實際結果

正式 `slideHtml`／`openRenderer.capture` 對 49 張逐張重畫 1920×1080 PNG，renderer 版面、字型及資源問題 **0**。另外重畫非品牌的 `showcase/video.json#opening` 對照卡，問題 **0**。逐張檢視六張原尺寸聯絡表及六張每卡實際 **320×180** 的聯絡表；49 張的來源、主標與副標均可辨識，沒有裁切或互蓋。A16 `now-072` 的完整來源在兩行呈現，「印刷」沒有拆字；A16 `turn-062` 的兩行算式、B14 `turn-075` 的長副標及 A21 的雙行標題也完整。非品牌對照卡在兩種尺寸都正常。這是靜態字卡的視覺檢查，**沒有驗證影片播放或裝置上的實際觀看**。

[逐卡雜湊與檢查收據](render-evidence.json)記錄 24 個輸入章檔、49 張 PNG、六對聯絡表、對照卡和 CSS 的 SHA-256。24 個候選章檔 SHA 全部符合原來源候選證據，原 24 個章檔也逐一符合原始 SHA，失配 **0**。本機正式 render 索引 SHA-256 `ea19061985552373d9bf39ea13fb31bf2288b9f868897f53b264d76c29efbb50`；本目錄收據 SHA-256 `de97df68d4e5210231c9e821c91eb53b4dfd71a1a762e3ab10e3ce802ab39240`。PNG 與聯絡表保留在 `<local-temp>/brand-mobile-title-qa-20261016-candidate2/`，未納入 Git。

本機檢查：`node --test tools/video/templates/templates.test.mjs` **27/27**、`node --test tools/repo-hygiene.test.mjs` **3/3**。`npm run test:docs-videos` **214/215**；唯一失敗是 `imported-long-languages/runner.test.mjs` 啟動系統 Node 的 `package-runtime.mjs` 時以 Windows 狀態碼 `3221226505` 結束，未指出字卡樣式或上述 49 張渲染的錯誤。未因這個環境失敗重跑整套測試。

本次的靜態字卡可讀性已通過；來源主張查核、敘事與配音、整片手機觀看、可關閉 CC、正式採用與站主看片仍是各自獨立的關卡。
