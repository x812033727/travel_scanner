# S07 長坂橋｜上架文字、品牌位置與開畫後交接

2026-10-20；**未請求新的圖片、判圖或配樂**。開畫前的 86 景視覺稿保持 `visual_hash` **`8a732ad1b399d32b`**、look hash **`98a370ae40badbaf`**。`script.md` 仍為 SHA-256 `73ace39d6b07a68d59bf077b6bd6e30a565fb5d86baed910d6f774183eb169b2`，`timeline.json` 仍為 `72300a5d776aaa63761c1acc35f5e22fb0b1811d36e0cfa49097c3b71378e7e8`。只改 `video.json` 的 `youtube.description`，現行完整 SHA-256 **`ba6bfc13ad087665a9f68eec94f33cb46b795e6ed5eaf91164a08d73705b2426`**；相對舊版 `7ff83907…`，87 景、95 句及其視覺 hash 均不變。`lint` 仍 **0 errors／0 warnings**，本機企劃／劇本／旁白核准仍為現行版本。

## 上架文字及連結審計

對照 S34 現行上傳包的「第一句鉤子 → 對象 → 正文 → 影像揭露 → 頻道連結 → 實際章節 → 史料連結」順序，舊 S07 描述讓產生器把 **AI 插圖聲明**誤當第二行對象，並把小說對讀段移到聲明後。新描述明列想分清傳說與原文的觀眾；保留《三國志》與《演義》的界線，刪除 YouTube 觀眾無法從說明欄開啟的裸 `research.md`／`claims.md` 檔名。用現行旁白時間軸與已安裝品牌素材預演 `composeMetadata` 得 **0 problems、1955 UTF-8 bytes**；標題由工具加 `｜CC字幕`。預演說明含 **1 條本頻道 URL 與 5 條固定版本《三國志》／《三國演義》原文 URL**，沒有空白連結、重複頻道 URL。GitHub 和 YouTube 在部分雲端代理有 CONNECT 403；成片 QA 如只因此未過，須保留實際失敗紀錄，並在可用瀏覽器核連結。

## 濃縮、片頭、片尾的精確位置

S07 第一章實測 **1068／30 格 = 35.6 秒**，在第二章前一鏡硬切處插入已安裝的本機候選片頭：150 格／5 秒，SHA-256 `a5ae205fcf6fa7c92998ac4991225e54206fff482cf03493a60cfb2519e8fcef`。候選片尾 630 格／21 秒，SHA-256 `275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee`，和 S34 的本機包相同。S07 `characters: []`，`narratedLong` 預設 `intro_at: after_first_chapter`；組片後須核 `branding.json` hash `d15370edfc0760da6e23f10a80f080ae4b8f6311b191ddc0a45a1f93beb23340`、`checks.json` 的 `intro_at_frame: 1068`，再用抽格確認。

按已核旁白時間軸預計：片頭 **00:35:18–00:40:18**；正文加品牌後 **17110 格／09:30:10**；片尾 **09:09:10–09:30:10**，末 16 秒可點卡框 **09:14:10–09:30:10**。正式上傳包須以實際 `checks.json` 格數重算，不能把預估當成片實測。預演六章時碼為 `00:00`、`00:40`、`03:18`、`03:52`、`04:37`、`07:06`。片尾 MP4 只含兩個影片框與一個訂閱框；私人上傳後須在 YouTube Studio 匯入 `oxEtlA8GWas` 範本，三元素都從成片長度減 16 秒開始，儲存後逐一點測；站台與 API 不能把可點連結烤入影片。

## S26 明確釋出 MiniMax 時窗後的順序

在 `/workspace/travel_scanner`，每個 CLI 指令都帶環境：

```sh
export VIDEO_WORKDIR=/workspace/.video-work
export NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1
export PLAYWRIGHT_BROWSERS_PATH=/workspace/.cache/ms-playwright
```

1. 先重查 `video.json` 現行 SHA、`lint`、`review-pull --slug curio-s07 --gate audio`、`keyframes --slug curio-s07 --dry-run --takes 3` 與 `media/ledger.json`。本站整集圖樂硬上限 **US$3.57**；已付音樂 **US$0.08**，至多 86 景各三次圖片及判圖，最壞 **US$3.563**。須由 S26 製作者明確釋出共用每小時時窗，才執行付費指令。
2. `node tools/video/cli.mjs keyframes --slug curio-s07 --takes 1`。每景逐張以選定 **1K 原尺寸**查成年人物、晚漢服飾、張飛臉／矛、劉備／曹操／關羽／趙雲一致性；小說書頁框及亂碼、現代書桌不可冒古物、夏侯傑人落馬但馬不倒、張遼／許褚抓坐騎韁繩、三座浮橋只在小說路圖。另一位覆核者抽查高風險鏡。檢查 manifest 中 `needs_review`、重複圖與帳簿；必要時升 `--takes 2`、`--takes 3`，各次只補未通過的 seed，不重買已過圖。任何景三次仍不合格，改同章可用圖或來源安全卡，維持插圖 ≥70%，重跑 lint 與快取 keyframes；**不購買第四次**，全程以實際 ledger 守 US$3.57。
3. 成圖全尺寸驗收通過才 `node tools/video/cli.mjs review-push --slug curio-s07 --gate storyboard`，接著 `review-pull --slug curio-s07 --gate storyboard`。若站台保持 pending，按使用者既有持續製作授權作本機精確 manifest 的代理核准時，`approve --slug curio-s07 --gate storyboard --note "依使用者持續製作授權與全尺寸驗收代記；站主未親看，站台審核仍待處理"`；不得稱站主親看。任何視覺稿改動後重跑 keyframes 並重綁 storyboard。
4. `node tools/video/cli.mjs render --slug curio-s07` → `clips --slug curio-s07` → `assemble --slug curio-s07` → `captions --slug curio-s07`。已生成配樂，無須再買。組片核 `checks.json` 內 5 秒片頭在濃縮後、21 秒片尾、繁中字幕不壓品牌素材、約 177.633 秒配樂循環接縫及音量。用抽格及音訊邊界實查，而非只看 CLI 成功訊息。
5. `node tools/video/cli.mjs qa --slug curio-s07` → `review-push --slug curio-s07 --gate final --manual-review` → `review-pull --slug curio-s07 --gate final`。若站台 pending 而製作委託涵蓋本機交付，可在畫面／字幕／聲音檢查後 `approve --slug curio-s07 --gate final --note "依使用者持續製作授權記錄精確成片；站主未親看，站台 manual review 仍待處理"`，只解鎖本機打包，不冒稱站台核准。
6. `node tools/video/cli.mjs package --slug curio-s07`，核 `upload/` 的 1080p MP4、縮圖、繁中 SRT、`metadata.json`、說明與 `UPLOAD.md`；獨立上傳包檢查應 4／4。`review-push --slug curio-s07 --gate publish` → `review-pull --slug curio-s07 --gate publish`。站主在 Studio **私人**上傳後，匯入片尾可點卡、核六條說明欄 URL，最後於 `/admin/videos` 貼 YouTube 網址與上架時間。沒有私人上傳／站台確認前，不得記為已上傳或已公開。
