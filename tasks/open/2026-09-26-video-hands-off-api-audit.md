---
id: 2026-09-26-video-hands-off-api-audit
title: 影片交給 AI 決定：YouTube API 稽核申請書草稿與隱私權政策段落
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-26T16:18:31Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/YOUTUBE-API-AUDIT.md
---

# 影片交給 AI 決定：YouTube API 稽核申請書草稿與隱私權政策段落

## Why

YouTube 會把未通過稽核的 API 專案用 `videos.insert` 上傳的影片鎖成私人。要做到「站主在後台選時間，網站自己上傳」，就要通過「YouTube API Services - Audit and Quota Extension Form」。表單由站主用自己的 Google 帳號送出；這張準備送出前需要的所有內容（`docs/videos/HANDS-OFF.md` §YouTube API）。

## Definition of done

- [ ] `docs/videos/YOUTUBE-API-AUDIT.md`：
  - 表單每一欄的建議答案（中英對照）；以個人還是組織身分申請，由站主選；
  - 要附的文件與截圖清單，標出哪些要等 T8 完成才截得到。
- [ ] 隱私權政策要加的 YouTube API 段落，五種語言的草稿，內容包括：
  - 使用了 YouTube API Services，並連到 YouTube 服務條款與 Google 隱私權政策；
  - 存取與保存了哪些資料；
  - 怎麼撤銷授權；
  - 刪除資料的方式。
- [ ] OAuth 同意畫面的設定清單：
  - 應用程式名稱不含「YouTube」；
  - 首頁與隱私權政策的網址；
  - 發布狀態設成「正式版」（留在「測試中」的話，refresh token 7 天就會過期）。
- [ ] 站主送出表單之後，送出日期與之後的往來記在這張票。

## Steps

- [ ] 讀表單與 YouTube API Services 的 Developer Policies，依這個站的情況寫出答案。
- [ ] 隱私權政策段落的草稿，交給站主在後台的法律頁面貼上，或交給內容線處理。
- [ ] T8 完成後補上截圖。

## How to verify

站主讀過申請書草稿，確認每一欄都填得出來。

## Notes

- 2026-09-27 讀到的表單內容：
  - 申請類型；
  - 申請人是個人或組織，網站、地址、類別與規模；
  - 聯絡人；
  - 組織說明（100–5000 字）；
  - 目標受眾與營利模式；
  - API 用戶端名稱（不能含 YouTube）、主要網址、隱私權政策網址、服務條款網址；
  - Cloud 專案編號、用途類別、是否使用 OAuth、預估每日請求數；
  - 必附：隱私權政策截圖（要有 YouTube 段落、Google 隱私權政策連結、刪除方式）、首頁截圖（看得到隱私權政策連結）、服務條款；
  - 使用 OAuth 時要附 OAuth 流程截圖；用途是上傳時要附上傳介面截圖；
  - 需要的配額，`videos.insert` 要另外說明理由。
- repo 是公開的：申請書草稿裡不能出現個人姓名、個人 email 或地址，那些由站主在表單上自己填。
