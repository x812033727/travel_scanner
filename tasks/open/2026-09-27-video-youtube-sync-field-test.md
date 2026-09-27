---
id: 2026-09-27-video-youtube-sync-field-test
title: YouTube 同步實測：連結頻道、用一支私人影片跑一次、把結果寫進 publish.md
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-27T10:13:21Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-youtube-sync
scope:
  - .agents/skills/youtube-video/references/publish.md
---

# YouTube 同步實測：連結頻道、用一支私人影片跑一次、把結果寫進 publish.md

## Why

T8（`2026-09-24-video-youtube-sync`）讓網站用站主授權的 OAuth 權杖，把核准的上傳包送到頻道：標題與說明、五語系、標籤、字幕、縮圖、排程時間，也可以由網站自己上傳 mp4。程式是照 2026-09-27 讀到的官方文件寫的，也用假的 Google 跑過測試，但有兩件事只有真的頻道回答得了：

- 沒有稽核的專案，對站主在 Studio 上傳的影片呼叫 `captions.insert` 與設定 `publishAt`，是不是都會成功；
- 中文字幕用 `zh-TW`／`zh-CN` 送出後，`captions.list` 讀回來是同一個碼，還是 `zh-Hant`／`zh-Hans`。程式兩種都當成同一個語系，但 `publish.md` 應該寫實際看到的。

另外，字幕軌名稱送的是空字串（播放器選單只顯示語言名）；文件寫 `snippet.name` 是必填，要確認空字串被接受。

## Definition of done

- [ ] 站主已經照設定分頁「YouTube 頻道」卡片的五步建好 OAuth 用戶端（網頁應用程式、同意畫面正式版、只有 `youtube.force-ssl`），並按允許連結了頻道。
- [ ] 用一支私人影片跑過一次「我已經在 Studio 上傳」：details、captions、thumbnail 三步的結果記下來。
- [ ] 用一支測試影片跑過一次「由網站上傳 mp4」（稽核前會被鎖成私人）：上傳、續傳與影片狀態記下來；這一次的畫面順便截給稽核附件 4、5、7、8（`docs/videos/YOUTUBE-API-AUDIT.md` §二）。
- [ ] 上面兩個問題與字幕名稱的結果寫進 `.agents/skills/youtube-video/references/publish.md`「網站送到 YouTube」一節，取代「還沒實測的兩件事」。

## Steps

- [ ] 站主：Google Cloud 專案、OAuth 用戶端、同意畫面（密鑰由站主自己貼，不經過代理或對話）。
- [ ] 站主：在卡片貼 ID 與密鑰、按「連結 YouTube 頻道」、在 Google 選擁有頻道的帳號按允許。
- [ ] 選一支已核准上傳包的影片，在 Studio 上傳成私人，從「可以上架」送出，排一個幾天後的時間。
- [ ] 在 Studio 核對：標題、說明、五語系、字幕語言與名稱、縮圖、排程時間、「變造或合成內容」。
- [ ] 寫回 `publish.md`；有不符的地方另開票修程式。

## How to verify

- `/admin/videos` 的影片頁「YouTube 同步」面板：每一步都是「完成」或寫出原因。
- YouTube Studio 那支影片的詳細資料、字幕分頁與「瀏覽權限」顯示排程時間。

## Notes

- 面板上失敗的原因與處理方式在 `publish.md`「網站送到 YouTube」：配額（太平洋時間午夜重置）、縮圖 403（頻道要電話驗證）、影片不是私人或不在連結的頻道、授權失效（重新連結）。
- 同步在 API 容器裡跑，日誌看 `docker compose logs api`，關鍵字 `YouTube sync`。
