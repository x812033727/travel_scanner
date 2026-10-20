# S26 本機長片與上傳包驗收（2026-10-20）

## 定稿差分與審核狀態

前一輪 `verify-21.md` 的 82 句史料敘事、72 張正常機評通過的插圖與九張來源卡仍在。實際渲染發現 `ma020` 的法文引句在大卡上太寬，因此只把同一批法文字分成三行；沒有增減原字、史料來源或語音。新版畫格通過字形與邊界檢查，72 張插圖全由原快取重用。現行插圖 manifest SHA-256 `5d2ef215180433525b523e6d82a7622e95b92febee3179ac48d050c818c53490`，影格 manifest SHA-256 `f115830ae0be3726ff05870b11e245c61425a1b204a44b98b3c3568c6bc4ce69`。站台曾核准**舊版**分鏡；新版精確 manifest 已重新 `review-push`，目前 `hand_pushed` 待站主審核。本機依站主持續「用推薦的決定」委託，另記精確 manifest 的**本機代理分鏡核准**，沒有冒稱新版獲站台批准。

第一次合成後，現行故事旁白在 Jev 政策 QA 的「業配」為 0.34／0.36，超過 0.30 門檻。逐句檢查沒有商品或合作廣告；只移除最後一句口播中的頻道訂閱呼籲做診斷時，分數降至 0.02 且通過。因此只把 `ma093` 口播改為「這份檔案先收到這裡；下一頁原文，我們繼續追。」；片尾動畫中的訂閱位置、兩個推薦影片框以及畫面上的訂閱字樣均保留。其餘 81 句口播、來源判斷與可見歷史內容未變。`script --slug` 同步更新腳本尾部校驗與 big 字卡標記。現行 `video.json` SHA-256 `bb524cc7846a17a102d8b8c50322061977cdc897b097b7473c5b22e9edd77996`，`script.md` SHA-256 `406f5e9cb9008bece78ac2415092b0a519ae27d42aa5eee11a208ddf9369d05e`；兩者的站台 script／audio 審核仍 `hand_pushed` 待站主，本機代理決定另有明註。

新句只重新合成一條語音，另外 81 條快取重用；`check-audio` 對 **82/82** 句覆核，零未解旗標。現行 `timeline.json` SHA-256 `08c88cb2da2874e7b2fdd9c0895f541b082f4c0d71cf14ede17e67b9d567ab6c`。在重合成前對**現行完整腳本**做政策預檢，業配為 0.01 且通過；重合成後的正式 QA 仍通過政策檢查。插圖／配樂帳簿 US$2.1455／已核准 US$3.37，補作過程零新付費圖或片段；`clips` 清單是 72 張動畫靜圖、零付費影片秒數。

## 成片與上傳包

現行 `final.mp4` 與 `upload/final.mp4` SHA-256 同為 `582b208a0a821c9f1eefff6e26d7d9a9713428ab73e725c698efea2035354e54`。H.264 1920×1080、30 fps、15,919 格、約 8:50.7；音訊 −14.1 LUFS、真峰值 −1.9 dBTP。`checks.json` SHA-256 `3e7f2b5e96f2c53fbb8e1047c03054c224e19f7410f7fa6962bbb64ea4e7b2fc`，`ok=true` 且零問題。33.133 秒濃縮開場後接 5 秒原創動畫片頭；故事在 509.633 秒結束，接 21 秒動畫片尾，末 16 秒保留兩個影片框與訂閱圓框。

獨立唯讀讀者對**現行 MP4** 的 12 個原尺寸 1080p 畫格、片頭／片尾接點、末句波形及繁中字幕作抽驗，結論 PASS；完整收據 `/tmp/s26-final-native-qa-current.md` SHA-256 `731658f9b3159c94934c79bf9458da05d3bacb60b2e60215ab2ec577d50ef6ec`。92 條 `zh-TW.srt` SHA-256 `f098a4dcaab6aa38eb6c17006b532a6ab84ecc1a7920afeb12cde4c8e2cf0463`；字幕未覆蓋片頭及片尾卡。原尺寸抽驗是抽樣，並非聲稱逐格人工審視。

正式 `qa` 是 **10/11**：政策門檻通過（重送 final 審片時 Jev 業配 0.01），僅頻道網址 `https://www.youtube.com/channel/UCR0rRWT4blMDUwEMx-TZ57Q` 在這個雲端的代理遭 CONNECT 403，無法網路開啟。說明欄有四筆固定版本史料網址、頻道網址、六章時間碼及 AI 畫面揭露。`package` 的精確檔案檢查 **4/4**；`upload/metadata.json` SHA-256 `4d69ff14ade73e36422034fe4644ff5a4c212013e68ad04d017aabde46221e96`。`upload/UPLOAD.md` 記私人上傳後在 YouTube Studio 匯入範本 `oxEtlA8GWas`，把兩個可點影片元素及訂閱元素放在 **08:34:19–08:50:19**；目前畫面外框尚不是可點連結。

現行 MP4 已 `review-push --gate final`，站台回覆 **pending**；本機在上述 QA 和獨立抽驗後另記**精確 MP4 的代理 final 核准**，才製作上傳包。`review-push --gate publish` 已提交，站台亦回覆 **pending**。這不表示站主親自看過、網站 final／publish 已核准、影片已私人上傳、取得真實 YouTube 影片 ID，或 Studio 可點片尾已安裝。現行 storytelling panel 因片尾口播變動顯示 stale；先前 13/13 屬舊的精確腳本，不冒稱是本版盲讀。

文件驗證：`npm run test:docs-videos` **236/236** 通過；`npm run check:tasks` 驗證 **2112** 張任務票通過，僅既存的跨票認領範圍／時長警告；S26 `lint` 零錯誤，六個提示詞／片尾口播風格警告如實保留。
