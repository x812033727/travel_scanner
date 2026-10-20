# X10｜從前製到可點影片的交接

本包已有企劃、來源、主片逐句稿／分鏡、兩支 Shorts 腳本與 105 句本機 TTS；[實測時長](reviews/tts-timing-v9.md)達標，逐句音訊複查仍在進行。它沒有插畫、音樂、MP4、縮圖、字幕檔、正式片頭片尾、YouTube 影片 ID 或本集可點影片連結；不可把本 PR 描述成成片。影片工具在此雲端已配對可用；新付費媒體須重新核對全包預算與共享配額。

1. 鎖定 `video.json`、`shorts.json` 的 SHA-256。由另一位代理逐句對 [SEC 原件](source-notes.md)、[B 主張矩陣](source-matrix.md)、原生卡與 Shorts 標題；兩位未先看來源矩陣的獨立讀者只看 [逐句稿](script.md) 做敘事盲評。所有收據必須綁同一版主片／Shorts SHA。修稿後重驗受影響的項目。`lint` 維持 **0 錯誤、0 警告**。
2. 媒體前先讀 [成本總帳](production-quote.md) 的當期價格；全片連同失敗重試、TTS、圖、音樂、複查、字幕、Shorts 和稅費不得超過 **US$25**。MiniMax 用 `image-01` 與精確 `look: {"preset":"cute-mystery"}`；首輪圖畫風與視覺連續性通過後才批量生成。插畫不得帶品牌 logo、可讀文字、真實 eBay UI 或假裝 SEC 原件。
3. Gemini Sulafat 的 105 句單人旁白已合成；`timeline.json` 量得**濃縮開場 00:50.433、六章實質正文 08:40.567、最後三句 00:20.233**，詳見[時長收據](reviews/tts-timing-v9.md)。逐句音訊複查未通過前不可做成片驗收。正式時間軸應在濃縮開場之後插入站主選定 **5 秒片頭**，在原生三句尾聲後插入站主選定 **21 秒 v4 片尾動畫**；固定片頭片尾不算正文。官方品牌包在本集仍未選定，不能把示意卡冒稱官方素材。
4. 完成字幕轉錄與語音查核，輸出可關閉的繁中 CC；不把字幕燒進畫面。圖像、資訊卡、原生結尾與兩段固定動畫進時間軸後，做聲音、字卡、視覺、事實和最終畫面 QA。縮圖左上橘色大字 `eBay`；其餘視覺不放商標。片尾留兩個影片／訂閱圖框的安全位置。
5. 長片成片核准後，兩支 Shorts 使用 [shorts.json](shorts.json) 的主片原句與 shot，9:16 各實測 25–55 秒；檢查聲音、繁中字幕安全區、字卡分母和來源敘述。若新增素材或重配音，成本同樣計入本集總帳。
6. 上架後在 YouTube Studio 加長片與 Shorts 的真實影片連結及片尾可點元素，逐個實點檢查。只有驗過真實 `video_id`／URL 才把它們寫回交付記錄；目前欄位 `null` 是正確狀態。

本機免費重建／檢查指令：

```bash
node docs/videos/story-everyday-ebay-paypal-x10/compose-video.mjs
node docs/videos/story-everyday-ebay-paypal-x10/compose-shorts.mjs
node tools/video/cli.mjs lint --file docs/videos/story-everyday-ebay-paypal-x10/video.json --json
npm run check:tasks
```

這些指令只建稿、驗結構，不呼叫媒體生成。已合成的 WAV 與時間軸在本機媒體工作區，不在 Git；後續須先解決音訊旗標，才可製作圖片、配樂、字幕與正式上架包。
