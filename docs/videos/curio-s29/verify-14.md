# S29 曹沖稱象｜上架文字及品牌預檢

2026-10-20，**未新增付費媒體請求**。只改 `video.json` 的 `youtube.description`：在《三國志》原句鉤子後加觀眾對象行，讓《雜寶藏經》對讀先於 AI 插圖聲明，固定來源與 SHA 註記保留在正文後。原全檔 SHA-256 `15afba6dbe466b175f2a9e2b5a8f367361d90712eb647cddbeab40f4aef12412`，現為 **`b56b39c71371e7680d7dc895994eda4b13c0f2c7f8dfb40882451115e8c09eb4`**。結構化比對只有 `youtube.description` 不同，92 張 still 與場景未動；`visual_hash` 前後皆 **`01ec569eadd4bc9e`**、look hash 皆 `98a370ae40badbaf`。`lint` **0 errors／0 warnings**。

`review-pull --gate audio` 回 **already recorded**；現行 `timeline.json` SHA-256 `aae42c240e51f6ca0e17e8a0ab1de2971ee70cccdaf18c2232fcfdfb54136a8d` 與本機音訊核准完全相同。用現行時間軸及已安裝品牌素材預演 `composeMetadata`：**0 problems、1648 UTF-8 bytes**；繁中說明第二行是觀眾對象，後段保留 AI 示意揭露，結尾自動加入本頻道 URL **1 條**、固定版《三國志》與 CBETA URL **2 條**（source title 仍含各自 SHA-256）。兩條原文 URL 本次 Node GET 各得 HTTP 200；頻道 YouTube URL 在本雲端代理無法 fetch，正式 QA 與上傳後仍需在瀏覽器核對。

第一章濃縮實長 **1380 格／46 秒**；無角色敘事預設接上 150 格／5 秒片頭（**00:46:00–00:51:00**），結尾再放 630 格／21 秒片尾。預估 18,038 格／**10:01:08**，片尾 **09:40:08–10:01:08**，YouTube Studio 三個可點元件設最後 16 秒 **09:45:08–10:01:08**。品牌候選的預計 pin hash `d15370edfc0760da6e23f10a80f080ae4b8f6311b191ddc0a45a1f93beb23340`；成片以實際 `checks.json` 重核。說明章節預演為 `00:00`、`00:51`、`02:57`、`04:14`、`05:30`、`08:07`。片尾可點卡須私人上傳後在 Studio 匯入 `oxEtlA8GWas`，不能由 MP4 自帶連結。
