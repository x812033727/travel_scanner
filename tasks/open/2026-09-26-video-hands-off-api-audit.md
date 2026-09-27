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
branch: claude/video-hands-off-api-audit
depends_on: []
scope:
  - docs/videos/YOUTUBE-API-AUDIT.md
---

# 影片交給 AI 決定：YouTube API 稽核申請書草稿與隱私權政策段落

## Why

YouTube 會把未通過稽核的 API 專案用 `videos.insert` 上傳的影片鎖成私人。要做到「站主在後台選時間，網站自己上傳」，就要通過「YouTube API Services - Audit and Quota Extension Form」。表單由站主用自己的 Google 帳號送出；這張準備送出前需要的所有內容（`docs/videos/HANDS-OFF.md` §YouTube API）。

## Definition of done

- [x] `docs/videos/YOUTUBE-API-AUDIT.md`：
  - 表單每一欄的建議答案（中英對照）；以個人還是組織身分申請，由站主選；
  - 要附的文件與截圖清單，標出哪些要等 T8 完成才截得到。
- [x] 隱私權政策要加的 YouTube API 段落，五種語言的草稿，內容包括：
  - 使用了 YouTube API Services，並連到 YouTube 服務條款與 Google 隱私權政策；
  - 存取與保存了哪些資料；
  - 怎麼撤銷授權；
  - 刪除資料的方式。
- [x] OAuth 同意畫面的設定清單：
  - 應用程式名稱不含「YouTube」；
  - 首頁與隱私權政策的網址；
  - 發布狀態設成「正式版」（留在「測試中」的話，refresh token 7 天就會過期）。
- [ ] 站主送出表單之後，送出日期與之後的往來記在這張票。

## Steps

- [x] 讀表單與 YouTube API Services 的 Developer Policies，依這個站的情況寫出答案。
- [x] 隱私權政策段落的草稿，交給站主在後台的法律頁面貼上，或交給內容線處理。
- [ ] 站主在後台 `/zh-TW/admin/site-pages` 貼上並發布五個語系的隱私權政策段落與服務條款那一句（`YOUTUBE-API-AUDIT.md` §三），再截附件 1、3。
- [ ] T8 完成後補上截圖（附件 4、5、7、8）。
- [ ] 站主送出表單，把日期與往來記進 `YOUTUBE-API-AUDIT.md` §六 與這張票的 Notes。

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
- 2026-09-27 草稿寫好（`docs/videos/YOUTUBE-API-AUDIT.md`，分支 `claude/video-hands-off-api-audit`）。事實來源是當天讀到的 19 個頁面，列在文件第一節；表單本身讀到的是五段式的版本（申請類型／申請人／業務模式／API 用戶端／用途與配額），比上面的摘要多了目標受眾、營利模式、示範帳號、衍生指標確認、端點勾選等欄位，都已寫進去。
- 標「待核對」的地方（頁面沒寫、要實際填表才看得到）：選個人身分後「Organization's Legal Name」還在不在；端點勾選清單上的名稱寫法；`videos.insert` 的配額欄能不能留空；首頁截圖說明提到的「看得到 YouTube 品牌」；`youtube.force-ssl` 算不算敏感 scope。
- 站主要決定的：個人或組織身分（法律頁寫的是個人營運，建議個人）；Category 選 Media and Entertainment 還是別的；「Is your API Client publicly accessible?」選 No 靠截圖，還是選 Yes 並開示範帳號；API 用戶端名稱用 Mokaair Studio Sync 或備選。
- 讀到的兩件會影響 T8 的事：`videos.insert` 現在是自己的桶（每天 100 次、每次 1 單位），不在 10,000 單位裡；Required Minimum Functionality 要求上傳用戶端讓使用者設定標題、說明與瀏覽權限，「可以上架」卡片在做 `videos.insert` 時要補這三個欄位。另外 Developer Policies III.E.4：授權取得的資料最多存 30 天、每 30 天確認授權還在，寫在文件 §五。
- 之後的順序：貼法律頁段落並發布（五語系）→ T8 → 截圖 → 站主送表單 → 紀錄。稽核有結果之前這張票不 done。
