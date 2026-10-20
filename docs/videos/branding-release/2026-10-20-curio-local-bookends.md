# 奇聞檔案局本機片頭片尾候選（2026-10-20）

站主要求歷史長片有濃縮開場、片頭動畫、片尾動畫及連結，並授權代理採推薦方案繼續製作。先前核定的 v4 媒體在這個雲端工作區無法取得；這次製作原創本機候選供這批尚未上傳的影片重剪及檢視。這筆紀錄不代表站主親自看過新素材，也不代表已在 YouTube 安裝可點元素。

素材留在 Git 外：`/workspace/.video-work/curio-brand-candidate/`，已用 `branding --install` 安裝至本機 `/workspace/.video-work/_branding/1ffcf193d68dfface2d561c3362f69b8bfe8590a90b5d8fa257a8b783984a801/`。`manifest.json` 記錄程式生成的畫面、配樂和音效；沒有借用其他影片或外部音樂。

| 項目 | 值 |
| --- | --- |
| 素材包 ID | `curio-archive-original-candidate-20261020-v1` |
| 片頭 | 150 格／5 秒，`a5ae205fcf6fa7c92998ac4991225e54206fff482cf03493a60cfb2519e8fcef` |
| 片尾 | 630 格／21 秒，`275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee` |
| 安裝包 hash | `1ffcf193d68dfface2d561c3362f69b8bfe8590a90b5d8fa257a8b783984a801` |
| 濃縮後片頭的成片 pin hash | `d15370edfc0760da6e23f10a80f080ae4b8f6311b191ddc0a45a1f93beb23340` |

畫面為檔案櫃、卷宗與印章的動畫，1920×1080／30 fps，片頭無固定集數或標語；片尾依序停頓 1 秒、提示動畫 3 秒，再留 17 秒結束畫面。實際抽看新成片的片頭轉場與片尾框。兩個影片框和一個訂閱圓框依站主既有 Studio 範本 `oxEtlA8GWas` 的座標繪製；可點區由片尾第 5 秒起，因此在 Studio 把三個元素設於成片最後 16 秒。

可點影片卡及訂閱鈕只能在私人上傳後於 YouTube Studio 匯入、定位、儲存及點測；`final.mp4` 本身只有外框。上傳包 `UPLOAD.md` 寫入逐步操作與每支片的精確時碼。說明欄包含頻道 URL 和各集史料 URL。雲端代理對 `youtube.com` 返回 CONNECT 403，所以本機 QA 無法證明頻道 URL 可開啟；上傳時須在瀏覽器確認。片尾沒有第三方商品或付費服務，Jev 把本頻道訂閱呼籲算成業配的分數另記於各集 QA。

截至此筆紀錄，S34 已重剪為 17,874 格／09:55.8、片頭始於 37.6 秒，`final.mp4` SHA-256 `a14f5647283fa8a64b093eaf0e4c37158c1983d6c3cea180196ef205c183f512`；字幕重建，包檢查 4/4 通過，原版保存在 `review/prebrand-20261020/`。S02、S03、S28、S30 的同款重剪另依各集核准及包檢查進度記錄，不沿用舊成片 hash。
