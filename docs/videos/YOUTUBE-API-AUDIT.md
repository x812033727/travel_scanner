# YouTube API 稽核申請書：逐欄草稿、附件清單與隱私權政策段落

2026-09-27 起草。這是 [`HANDS-OFF.md`](HANDS-OFF.md) §YouTube API 第二步要用的申請書：站主用自己的 Google 帳號送出「YouTube API Services - Audit and Quota Extension Form」，通過之後網站才能自己用 `videos.insert` 上傳而不被鎖成私人。這份把表單每一欄的建議答案、要附的截圖、隱私權政策與服務條款要加的段落、OAuth 同意畫面的設定，以及送出後的紀錄放在一起。票是 `2026-09-26-video-hands-off-api-audit`。

三個規矩：

- repo 是公開的。站主的姓名、地址、聯絡信箱、Cloud 專案編號一律寫成【站主填】，只在表單上填，不寫進這份、票或 PR。
- 表單是英文的。「填什麼」欄是照抄進表單的英文；旁邊的中文只是給站主看的對照，不用翻回去。
- 事實只來自 2026-09-27 讀到的頁面（下一節）。頁面沒寫、或要實際填到表單才看得到的，標「待核對」。

## 讀過的頁面（2026-09-27）

| # | 頁面 | 網址 | 用在哪裡 |
| --- | --- | --- | --- |
| 1 | 稽核表單 | https://support.google.com/youtube/contact/yt_api_form | §一 的欄位、選項、必附附件 |
| 2 | Developer Policies | https://developers.google.com/youtube/terms/developer-policies | 隱私權政策與服務條款要寫什麼（III.A）、寫入操作要由使用者發起（III.C.3）、一個用戶端一個專案（III.D）、資料保存 30 天（III.E.4）、稽核（III.H） |
| 3 | API Services Terms of Service | https://developers.google.com/youtube/terms/api-services-terms-of-service | 監看與稽核、配額、終止 |
| 4 | Quota and compliance audits | https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits | 預設配額、什麼時候要稽核、12 個月內可再申請 |
| 5 | Quota costs | https://developers.google.com/youtube/v3/determine_quota_cost | 每個方法的配額；`videos.insert` 自己的桶 |
| 6 | `videos.insert` | https://developers.google.com/youtube/v3/docs/videos/insert | 未稽核專案的上傳鎖成私人；256 GB 上限 |
| 7 | Videos resource | https://developers.google.com/youtube/v3/docs/videos | `publishAt`、`containsSyntheticMedia`、`localizations`、`selfDeclaredMadeForKids` |
| 8 | Required Minimum Functionality | https://developers.google.com/youtube/terms/required-minimum-functionality | 上傳用戶端要讓使用者填標題、說明、瀏覽權限 |
| 9 | Branding Guidelines | https://developers.google.com/youtube/terms/branding-guidelines | 名稱、網域、圖像不能用 YouTube、YT |
| 10 | OAuth 2.0 總覽 | https://developers.google.com/identity/protocols/oauth2 | refresh token 什麼時候過期 |
| 11 | Manage App Audience | https://support.google.com/cloud/answer/15549945 | 測試中／正式版、100 個使用者的上限 |
| 12 | Manage OAuth App Branding | https://support.google.com/cloud/answer/15549049 | 名稱規則、首頁與隱私權政策網址的條件、標誌要驗證、已授權網域 |
| 13 | Unverified apps | https://support.google.com/cloud/answer/7454865 | 未驗證警告畫面、100 個新使用者 |
| 14 | OAuth app verification | https://support.google.com/cloud/answer/10311615 | 正式版要填首頁與隱私權政策；名稱不能含 Google 產品名 |
| 15 | Verification requirements | https://support.google.com/cloud/answer/13464321 | 只讀到品牌驗證的通則與「不回通知會失去存取」；豁免清單在它連出去的頁面，沒讀 |
| 16 | YouTube 服務條款 | https://www.youtube.com/t/terms | 連結有效（2022-01-05 版） |
| 17 | Google 隱私權政策 | https://policies.google.com/privacy | 連結有效（2026-05-26 版） |
| 18 | 撤銷頁 | https://security.google.com/settings/security/permissions | Developer Policies 寫的網址；301 轉到 https://myaccount.google.com/permissions |
| 19 | 本站 | https://mokaair.com/zh-TW 、 /zh-TW/privacy 、 /en/terms | 首頁頁尾有隱私權政策與服務條款連結；隱私權政策現有的章節；兩頁生效日 2026-09-13 |

沒讀到的：Google Cloud「設定 OAuth 同意畫面」的舊說明頁（answer/6158849）現在放的是「管理 OAuth 用戶端」，同意畫面的規則改用第 11、12 頁。Developer Policies 沒有專講「代使用者上傳」的章節，上傳相關只找到 III.C.3（寫入操作要由使用者清楚發起，使用者對發布到 YouTube 的內容有最後決定權）。

## 先弄清楚：稽核到底在管什麼

- 預設配額：每天 `search.list` 100 次、`videos.insert` 100 次，其他端點合計 10,000 單位。`search.list` 與 `videos.insert` 各有自己的桶，每次 1 單位（頁 5）。
- 鎖私人的規則：2020-07-28 之後建立、沒有通過稽核的專案，用 `videos.insert` 上傳的影片一律限制為私人（頁 6）。這是第二步非過稽核不可的原因，不是配額不夠。
- 第一步不需要稽核：`videos.update`（50）、`captions.insert`（400，五次）、`thumbnails.set`（50）都在預設配額內，一支影片約 2,100 單位，再加上讀回用的 `videos.list`（1）、`captions.list`（50）、`channels.list`（1）（頁 5）。
- 稽核通過後 12 個月內可以用同一張表單再申請更多配額；用途改變要重送；被退可以申訴；連續 90 天沒用 API 可能被收回憑證或降配額（頁 2、4）。
- YouTube 隨時可以要求提供帳號讓他們檢查用戶端，要在他們指定的期限內給（頁 2 III.H）。頁 4 只寫「會盡快聯絡」，沒有審查時程。

## 一、表單逐欄建議答案

表單分五段，順序照 2026-09-27 讀到的版本；票的 Notes 記的是同一張表單較早看到的欄位摘要，兩者對得上。可複選的題目列出要勾的每一項。

### 第 1 段：申請類型

| 欄位 | 填什麼 | 說明 |
| --- | --- | --- |
| Select the reason for your request | Complete a compliance audit to request for additional quota | 兩個選項只有這個是新申請；另一個是被要求重審時用。名稱雖然寫 additional quota，第 5 段可以選維持預設配額 |

### 第 2 段：申請人與聯絡人

先決定：個人還是組織。本站法律頁寫的營運者是個人營運、不是公司法人；用組織身分申請會跟隱私權政策上的營運者說明對不上，也會被要求填組織的法定名稱與母公司。建議選個人；站主之後若成立公司，先改法律頁再改這裡。

| 欄位 | 填什麼 | 說明 |
| --- | --- | --- |
| Application Type | As an individual user | 見上；站主決定 |
| Your Full Legal Name | 【站主填】 | 與 Google 帳號、之後可能被要求的證件一致 |
| Your Organization's Legal Name | 【站主填】（待核對） | 表單列為必填；選個人之後這欄還在不在，要實際填到才知道。還在的話填站主的名字，或 Mokaair |
| Parent Company Name | 空白 | |
| Your Organization's Primary Website | https://mokaair.com | 必須 https:// 開頭 |
| Country、Street Address、City、State/Province、Postal Code | 【站主填】 | 法律地址 |
| Category | Media and Entertainment | 本站是內容站；「Creator Tools and Services」描述的是工具，不是申請人。站主決定 |
| Organization Size / Type | Independent Developer/Sole Proprietor | 與個人身分一致 |
| Primary Contact：Name、Email | 【站主填】 | 用會看的信箱：稽核往來、之後 III.H 的稽核要求、Cloud 的通知都寄到這裡 |
| Primary Technical Contact | 勾 Same as Primary Contact | |
| Primary Business Contact | 勾 Same as Primary Contact | |

### 第 3 段：業務模式與 Google 窗口

| 欄位 | 填什麼 | 說明 |
| --- | --- | --- |
| Describe your organization's work as it relates to YouTube | 下面的英文全文 | 100–5,000 字元；草稿約 2,800 字元 |
| Who is your target audience? | Internal Users | 這題問的是 API 用戶端的使用者：只有站主一個人。頻道的觀眾是一般大眾，寫在說明裡即可 |
| How does your API Client monetize or generate revenue? | Free service (we do not charge users)；再勾 Other (please specify)，填：The API Client itself earns nothing. The website carries affiliate links on travel pages; they are unrelated to YouTube content. | |
| Do you sell advertisements or sponsorships ON or WITHIN YouTube video content or the embedded YouTube player itself? | Not applicable | 本站目前沒有展示型廣告（AdSense 2026-09-23 退件；文章頁廣告的後台開關預設關閉）。之後若打開文章頁廣告，改選「No, ads only appear elsewhere on the page」：文章頁不嵌 YouTube 播放器，有嵌播放器的只有社群探索頁（`apps/web/components/discovery/video.tsx`，youtube-nocookie），那裡沒有廣告版位 |
| If you answered yes, have you obtained prior written approval | 不填 | |
| Do you currently have a designated Google Partner Manager or YouTube Partner Manager? | No, I do not have a Google representative | |
| How did you first learn about the YouTube Data API? | Google Developer Documentation | |
| Content Owner ID(s) | 空白；「associated YouTube Channel URL」填頻道網址【站主填】 | Content Owner ID 是內容管理系統合作夥伴才有的，本站沒有 |
| Google Ads Customer ID(s) | 空白 | |

**Describe your organization's work as it relates to YouTube**（照抄）：

```text
Mokaair (https://mokaair.com) is an independently operated website for travel planning and for practical explainers about AI tools, published in five languages: Traditional Chinese, Simplified Chinese, English, Japanese and Korean. It runs its own YouTube channel, where it publishes tutorial and explainer videos on the same topics.

The videos are made by an automated pipeline that runs on the site's own server. A script is drafted with an AI model and checked by a separate fact-checking step against cited sources; the narration is synthesized speech; the visuals are slide-style graphics; captions are produced in the five languages. The site operator reviews the finished video and decides when it goes live. Nothing reaches the channel without that decision.

The API Client, "Mokaair Studio Sync", is an internal tool inside the site's administration area. It is used by exactly one person, the site operator, and only on the operator's own channel. It never accesses, reads or stores data about any other YouTube user or channel. It uses the YouTube Data API for these steps:

1. videos.update: set the default language, the localized titles and descriptions for the five languages, tags, the category, the synthetic-media disclosure (status.containsSyntheticMedia) and the scheduled publish time (status.publishAt) chosen by the operator. The video stays private until YouTube publishes it at that time.
2. captions.insert: upload the five caption tracks. captions.list is called first so that a retry never uploads a track twice.
3. thumbnails.set: set the thumbnail.
4. videos.insert (resumable upload): upload the finished MP4 as a private video together with the publish time, so that the operator only has to choose the time in the administration area. This is why we are asking for the audit: the reference documentation says that uploads through videos.insert from projects that have not completed an audit are restricted to private viewing.
5. videos.list and channels.list: read back the operator's own videos and channel to show their state in the administration area.

The expected volume is a few videos per week, at most a handful in one day, far below the default quota: about 2,100 units per video for the metadata, caption and thumbnail calls, and one videos.insert call per upload. We are not asking for quota above the default.

Authorization uses OAuth 2.0 with the single scope https://www.googleapis.com/auth/youtube.force-ssl. The operator grants access once in the browser; the refresh token is stored on the server in the same way as the site's other provider credentials and is never displayed or sent to the browser. Access can be revoked at any time from the Google Account permissions page or with the revoke button in the administration area. The privacy policy (https://mokaair.com/en/privacy) and the terms of service (https://mokaair.com/en/terms) state that the site uses YouTube API Services, link to the YouTube Terms of Service and the Google Privacy Policy, list the data that is accessed and stored, and explain how to revoke access and how stored data is deleted.
```

中文對照（不用填）：

> Mokaair（https://mokaair.com）是個人營運的網站，做旅行規劃與 AI 工具的實用解說，五種語言（繁中、簡中、英、日、韓）。它有自己的 YouTube 頻道，發布同樣題目的教學與解說影片。
>
> 影片由網站自己伺服器上的自動產線製作：AI 模型撰稿，另一個查核步驟對照引用來源檢查；旁白是合成語音；畫面是投影片式圖像；字幕五種語言。站主看過成片、決定上架時間，沒有這個決定，影片不會進頻道。
>
> API 用戶端「Mokaair Studio Sync」是網站後台裡的內部工具，只有站主一個人用、只對站主自己的頻道。它不存取、不讀取、不保存任何其他 YouTube 使用者或頻道的資料。用到的步驟：（1）`videos.update` 設定預設語言、五語系標題與說明、標籤、分類、合成媒體揭露與站主選的上架時間，影片在那之前一直是私人；（2）`captions.insert` 上傳五條字幕，先用 `captions.list` 確認不重複；（3）`thumbnails.set` 設縮圖；（4）`videos.insert` 續傳上傳成品 mp4，帶上上架時間，站主只要在後台選時間——這就是申請稽核的原因：文件寫明未稽核專案用 `videos.insert` 上傳的影片會被限制為私人；（5）`videos.list`、`channels.list` 讀回自己的影片與頻道狀態顯示在後台。
>
> 預估用量是每週幾支、一天最多幾支，遠低於預設配額：一支約 2,100 單位，加上一次 `videos.insert`。不申請高於預設的配額。
>
> 授權用 OAuth 2.0，只有 `youtube.force-ssl` 一個 scope。站主在瀏覽器授權一次，refresh token 和本站其他供應商金鑰一樣存在伺服器，不顯示、不回傳瀏覽器；隨時可以在 Google 帳戶的權限頁或後台的撤銷鈕撤銷。隱私權政策與服務條款寫明本站使用 YouTube API Services、連到 YouTube 服務條款與 Google 隱私權政策、列出存取與保存的資料、說明怎麼撤銷與怎麼刪除。

### 第 4 段：API 用戶端

| 欄位 | 填什麼 | 說明 |
| --- | --- | --- |
| API Client Name | Mokaair Studio Sync | 名稱、網域、圖像都不能用 YouTube、YT 或變體（頁 9）；同一個名字用在 OAuth 同意畫面（§四）。備選：Mokaair Channel Sync、Mokaair Video Publisher |
| Does this API Client name contain the word "YouTube"? | No, the name does not contain "YouTube" | |
| Primary Access URL | https://mokaair.com | |
| Privacy Policy URL | https://mokaair.com/en/privacy | 給審查者看英文版；五個語系是同一份。要和 OAuth 同意畫面填的一樣（頁 12） |
| Terms of Service URL | https://mokaair.com/en/terms | 選填，但反正要附服務條款文件，所以填 |
| Is your API Client publicly accessible? | No | 用戶端在需要登入的後台，只有站主用；網站本身是公開的。選 No 之後靠截圖與說明。站主決定：另一個做法是選 Yes 並提供示範帳號（下一列） |
| Demo Account Username、Password、Login URL | 空白 | 後台只有站主的帳號，不建議為了審查開一個。若審查者事後依 III.H 要求帳號，再由站主決定要不要開一個只看得到 `/admin/videos` 的帳號 |
| Special Instructions for Access | 下面的英文 | |
| Acknowledgment（提供示範帳號時 Google 不受本站條款約束） | 勾 | 必填；沒給帳號也要勾 |

**Special Instructions for Access**（照抄）：

```text
The API Client is an internal tool inside the administration area of https://mokaair.com. The only account that can reach it belongs to the site operator, and it is linked to the operator's own YouTube channel, so no demo account is provided. The attached screenshots show the whole flow: the settings tab where the operator links the channel (consent screen, scope, revoke button), the "ready to publish" card where the operator picks the publish time, and the result log. If you need to see it live, write to the primary contact e-mail and we will arrange a screen share or a temporary reviewer account.
```

> 中文對照：用戶端是 mokaair.com 後台裡的內部工具，唯一能進去的帳號是站主的，而且綁的是站主自己的頻道，所以沒有示範帳號。附件截圖涵蓋整個流程：設定分頁的連結頻道（同意畫面、scope、撤銷鈕）、「可以上架」卡片選時間、送出結果。需要實際看的話，寫信到主要聯絡信箱，我們安排分享畫面或臨時的審查帳號。

### 第 5 段：用途、專案與配額

| 欄位 | 填什麼 | 說明 |
| --- | --- | --- |
| How many project numbers are you adding? | 1 | 一個用戶端一個專案，憑證不能分享（頁 2 III.D） |
| Google Cloud Project Number | 【站主填】 | 只能是數字；在 Cloud Console 首頁的專案資訊卡上，不是 project ID |
| Use Case Category | Video Uploading & Account Management；Internal Company Tool | 可複選；就這兩個 |
| Does this API Client require users to sign in with their Google Account (OAuth 2.0)? | Yes | |
| Derived Metrics and Data Storage 的兩個確認框 | 勾 | 必填。本站不做衍生指標；資料保存規則見 §五 |
| Expected API Usage Volume | Fewer than 1,000 requests per day | 一支影片約 10 次請求 |
| REQUIRED EVIDENCE（隱私權政策截圖、首頁截圖、服務條款） | 見 §二 | |
| CONDITIONAL EVIDENCE（OAuth Flow、Upload Interface、Dashboard / Feature） | 見 §二 | 選了 OAuth＝Yes、Video Uploading 與 Internal Company Tool，三組都要 |
| Select the endpoints you plan to use | youtube.videos.insert、youtube.videos.update、youtube.videos.list、youtube.captions.insert、youtube.captions.list、youtube.captions.update、youtube.captions.delete、youtube.thumbnails.set、youtube.channels.list | 清單有 60 幾項；勾的名稱以表單上的寫法為準（待核對）。`captions.update`／`delete` 是重試時替換舊字幕用的 |
| Quota Request Options | No change / Default quota (10k quota points) | |
| Total Per Day Quota、Detailed Justification | 10000；理由見下 | 表單可能只在選 Above Default 時才問；問了就填 |
| youtube.search.list：Total Per Day Quota、Detailed Justification | 不填 | 不用這個端點 |
| youtube.videos.insert：Total Per Day Quota、Detailed Justification | 100；理由見下 | 稽核的目的是解除私人鎖，不是要更多。表單允許留空的話，理由仍然要寫在說明欄或這裡（待核對） |

**Detailed Justification（total quota）**（照抄）：

```text
We are not requesting an increase. One video needs about 2,100 units: videos.update (50), five captions.insert calls (400 each), thumbnails.set (50), plus a few small reads (videos.list, captions.list, channels.list). Even five videos in one day stay well under the 10,000-unit default.
```

> 中文對照：不申請增加。一支影片約 2,100 單位：`videos.update` 50、五次 `captions.insert` 各 400、`thumbnails.set` 50，加上幾次很小的讀取。一天五支也遠低於 10,000 的預設。

**Detailed Justification（youtube.videos.insert）**（照抄）：

```text
One call per finished video. We expect one to three uploads on a busy day and never more than ten, so the default allocation of 100 calls per day is sufficient. We are asking for the audit so that videos uploaded from this project are no longer restricted to private viewing: each upload is private with a publish time chosen by the operator, and YouTube publishes it at that time.
```

> 中文對照：一支成片一次呼叫。忙的日子一到三次、絕不超過十次，預設的每天 100 次夠用。申請稽核是為了讓這個專案上傳的影片不再被限制為私人：每支上傳時都是私人，帶站主選的上架時間，由 YouTube 到時公開。

## 二、附件與截圖清單

| # | 附件 | 內容 | 從哪裡截 | 什麼時候截得到 |
| --- | --- | --- | --- | --- |
| 1 | 隱私權政策截圖（必附） | 看得到 YouTube 段落、Google 隱私權政策連結、撤銷與刪除的說明 | https://mokaair.com/en/privacy 全頁 | §三 的段落發布之後 |
| 2 | 首頁截圖（必附） | 看得到頁尾的 Privacy policy 連結 | https://mokaair.com/en 全頁，頁尾要入鏡 | 現在。表單說明還提到畫面上「看得到 YouTube 品牌」；本站首頁沒有 YouTube 元素，先截頁尾連結；若之後頁尾加了頻道連結，一起截（待核對） |
| 3 | 服務條款（必附） | 加了 YouTube 服務條款那一句 | https://mokaair.com/en/terms 全頁，或印成 PDF | §三 的段落發布之後 |
| 4 | OAuth：同意畫面 | Google 的同意畫面，看得到應用程式（未驗證時顯示的是網域 mokaair.com）與權限那一行 | 站主在設定分頁按「連結 YouTube 頻道」時 | T8 之後 |
| 5 | OAuth：未驗證警告 | 有出現就截，沒有就略過 | 同上 | T8 之後 |
| 6 | OAuth：scope | Cloud Console「資料存取」頁只列 youtube.force-ssl | Cloud Console | 現在 |
| 7 | OAuth：撤銷 | 設定分頁的撤銷鈕；Google 帳戶 https://myaccount.google.com/permissions 列出本站 | 設定分頁、Google 帳戶 | T8 之後 |
| 8 | 上傳介面 | `/admin/videos` 的「可以上架」卡片：影片資訊、上架時間欄、送出結果 | 後台 | T8 之後（卡片本身在票 `video-hands-off-web`；時間欄與送出結果在 T8） |
| 9 | 儀表板／功能 | `/admin/videos` 整頁：需要你、可以上架的排序，審核紀錄 | 後台 | `video-hands-off-web` 之後 |
| 10 | 配額理由 | §一 第 5 段的文字，不是檔案 | — | 現在 |

截圖的做法：用英文語系；瀏覽器寬 1280 以上；全頁 PNG 或印成 PDF；不要把 token、用戶端密鑰或任何信箱截進去（設定分頁顯示 client ID 沒關係，密鑰欄本來就不回顯）。

附件 8 的兩個選項：T8 可以先把 `videos.insert` 的上傳鈕做出來、用一支測試影片實測（未稽核專案上傳會被鎖成私人，正好不會外流），這樣就截得到真正的上傳畫面；或者只截第一步的卡片，在說明裡寫稽核通過後同一張卡片會多一個上傳鈕。

## 三、隱私權政策與服務條款要加的段落（五種語言）

怎麼上：法律頁是資料庫文件，在後台 `/zh-TW/admin/site-pages` 編（元件 `apps/web/components/admin-site-pages-panel.tsx`，API `apps/api/app/site_pages/`），每個語系一份草稿、各自「發布」（要勾確認、寫理由），五個語系做五次。編輯器的區塊型別是標題（level 2）、段落（4,000 字內）、清單、連結（文字＋網址）。`apps/api/app/site_pages/drafts/*.json` 只是初始化用的種子，改它不會改正式站；要不要同步更新種子由內容線決定，不在這張票的 scope。發布後用瀏覽器看五個網址各一次，再截附件 1、3。

隱私權政策放的位置：「文章頁的廣告」之後、「保存、刪除與資料請求」之前。每個語系都是 1 個標題、4 個段落、3 個連結區塊。網址三個語系都一樣：

| 連結文字（依語系） | 網址 |
| --- | --- |
| YouTube 服務條款 | https://www.youtube.com/t/terms |
| Google 隱私權政策 | https://policies.google.com/privacy |
| Google 帳戶的第三方應用程式權限 | https://myaccount.google.com/permissions |

服務條款放的位置：「旅行資訊、外部服務與 AI」那一節最後加 1 個段落（Developer Policies III.A.1 要求服務條款寫明使用者同意受 YouTube 服務條款約束，並提供連結；連結用 1 個連結區塊或直接寫在段落裡）。

### zh-TW

隱私權政策：

- 標題：YouTube API 服務
- 段落 1：本站使用 YouTube API 服務（YouTube API Services），讓營運者把本站製作的影片、字幕、縮圖與影片資訊送到本站自己的 YouTube 頻道，並排定上架時間。使用這項功能即受 YouTube 服務條款約束；YouTube 與 Google 對資料的處理方式，請見 Google 隱私權政策。
- 段落 2：這項功能只存取營運者自己頻道的影片、字幕與影片資訊（標題、說明、標籤、縮圖、上架時間），不讀取、不保存任何其他 YouTube 使用者或頻道的資料。本站的伺服器會保存營運者授權時取得的 OAuth 授權權杖（refresh token）、每支影片的 YouTube 影片編號，以及每次 API 請求的結果；權杖只存在伺服器端，不會顯示在任何頁面，也不會提供給第三方。
- 段落 3：營運者可以隨時在 Google 帳戶的「安全性」→「第三方應用程式與服務」頁面（https://myaccount.google.com/permissions）撤銷本站的存取權；撤銷後，本站保存的權杖立即失效。
- 段落 4：影片在本站的紀錄被刪除時，對應的 YouTube 影片編號與 API 請求紀錄會一併刪除。要刪除保存的權杖、或對這項功能有任何疑問，請用本頁所列的聯絡方式提出，我們會在確認後刪除。
- 連結：YouTube 服務條款、Google 隱私權政策、Google 帳戶的第三方應用程式權限

服務條款（段落）：營運者可以透過 YouTube API 服務，把本站製作的影片發布到本站自己的 YouTube 頻道。使用這項功能時，除了本條款之外，也同意受 YouTube 服務條款（https://www.youtube.com/t/terms）約束。

### zh-CN

隐私权政策：

- 标题：YouTube API 服务
- 段落 1：本站使用 YouTube API 服务（YouTube API Services），让运营者把本站制作的视频、字幕、缩略图与视频信息发送到本站自己的 YouTube 频道，并预约发布时间。使用这项功能即受 YouTube 服务条款约束；YouTube 与 Google 对数据的处理方式，请参阅 Google 隐私权政策。
- 段落 2：这项功能只访问运营者自己频道的视频、字幕与视频信息（标题、说明、标签、缩略图、发布时间），不读取、不保存任何其他 YouTube 用户或频道的数据。本站的服务器会保存运营者授权时获得的 OAuth 授权令牌（refresh token）、每个视频的 YouTube 视频 ID，以及每次 API 请求的结果；令牌只保存在服务器端，不会显示在任何页面，也不会提供给第三方。
- 段落 3：运营者可以随时在 Google 账号的「安全性」→「第三方应用和服务」页面（https://myaccount.google.com/permissions）撤销本站的访问权限；撤销后，本站保存的令牌立即失效。
- 段落 4：视频在本站的记录被删除时，对应的 YouTube 视频 ID 与 API 请求记录会一并删除。要删除保存的令牌、或对这项功能有任何疑问，请通过本页所列的联系方式提出，我们会在确认后删除。
- 链接：YouTube 服务条款、Google 隐私权政策、Google 账号的第三方应用权限

服务条款（段落）：运营者可以通过 YouTube API 服务，把本站制作的视频发布到本站自己的 YouTube 频道。使用这项功能时，除本条款外，也同意受 YouTube 服务条款（https://www.youtube.com/t/terms）约束。

### en

Privacy policy:

- Heading: YouTube API Services
- Paragraph 1: This site uses YouTube API Services so that the site operator can send videos produced on this site, together with their captions, thumbnails and video details, to the site's own YouTube channel and schedule when they are published. Use of this feature is subject to the YouTube Terms of Service; how YouTube and Google handle data is described in the Google Privacy Policy.
- Paragraph 2: The feature only accesses the videos, captions and video details (title, description, tags, thumbnail, publish time) of the operator's own channel. It does not read or store data about any other YouTube user or channel. The site's server stores the OAuth refresh token obtained when the operator grants access, the YouTube video ID of each video and the result of each API request. The token is kept on the server only; it is never shown on any page and never passed to third parties.
- Paragraph 3: The operator can revoke this site's access at any time on the Google Account page Security → Third-party apps & services (https://myaccount.google.com/permissions). After revocation, the token stored by this site stops working immediately.
- Paragraph 4: When a video's record on this site is deleted, its YouTube video ID and API request records are deleted with it. To have the stored token deleted, or to ask anything about this feature, use the contact details given on this page; we delete the data after confirming the request.
- Links: YouTube Terms of Service; Google Privacy Policy; Third-party app permissions in your Google Account

Terms of service (paragraph): The operator may publish videos produced on this site to the site's own YouTube channel through YouTube API Services. By using this feature you also agree to be bound by the YouTube Terms of Service (https://www.youtube.com/t/terms).

### ja

プライバシーポリシー：

- 見出し：YouTube API サービス
- 段落 1：当サイトは YouTube API サービス（YouTube API Services）を利用しています。これにより、運営者は当サイトで制作した動画、字幕、サムネイル、動画情報を当サイト自身の YouTube チャンネルへ送り、公開日時を予約できます。この機能の利用には YouTube 利用規約が適用されます。YouTube と Google によるデータの取り扱いについては、Google プライバシーポリシーをご覧ください。
- 段落 2：この機能がアクセスするのは、運営者自身のチャンネルの動画、字幕、動画情報（タイトル、説明、タグ、サムネイル、公開日時）のみです。他の YouTube ユーザーやチャンネルのデータを読み取ったり保存したりすることはありません。当サイトのサーバーには、運営者がアクセスを許可した際に取得した OAuth リフレッシュトークン、各動画の YouTube 動画 ID、各 API リクエストの結果が保存されます。トークンはサーバー側にのみ保存され、どのページにも表示されず、第三者に提供されることもありません。
- 段落 3：運営者は、Google アカウントの「セキュリティ」→「サードパーティ製のアプリとサービス」（https://myaccount.google.com/permissions）から、いつでも当サイトのアクセス権を取り消せます。取り消し後、当サイトに保存されたトークンは直ちに無効になります。
- 段落 4：当サイト上の動画の記録が削除されると、対応する YouTube 動画 ID と API リクエストの記録も一緒に削除されます。保存されたトークンの削除や、この機能に関するお問い合わせは、本ページに記載の連絡方法でご連絡ください。確認のうえ削除します。
- リンク：YouTube 利用規約、Google プライバシーポリシー、Google アカウントのサードパーティ製アプリの権限

利用規約（段落）：運営者は YouTube API サービスを通じて、当サイトで制作した動画を当サイト自身の YouTube チャンネルに公開できます。この機能を利用する場合、本規約に加えて YouTube 利用規約（https://www.youtube.com/t/terms）にも同意したものとみなされます。

### ko

개인정보처리방침:

- 제목: YouTube API 서비스
- 단락 1: 이 사이트는 YouTube API 서비스(YouTube API Services)를 사용합니다. 이를 통해 운영자는 이 사이트에서 제작한 동영상과 자막, 미리보기 이미지, 동영상 정보를 이 사이트의 자체 YouTube 채널로 보내고 게시 시간을 예약할 수 있습니다. 이 기능의 이용에는 YouTube 서비스 약관이 적용되며, YouTube와 Google의 데이터 처리 방식은 Google 개인정보처리방침을 참고하시기 바랍니다.
- 단락 2: 이 기능은 운영자 자신의 채널에 있는 동영상, 자막, 동영상 정보(제목, 설명, 태그, 미리보기 이미지, 게시 시간)에만 접근합니다. 다른 YouTube 사용자나 채널의 데이터를 읽거나 저장하지 않습니다. 이 사이트의 서버에는 운영자가 접근을 허용할 때 발급된 OAuth 리프레시 토큰, 각 동영상의 YouTube 동영상 ID, 각 API 요청의 결과가 저장됩니다. 토큰은 서버에만 보관되며 어떤 페이지에도 표시되지 않고 제3자에게 제공되지 않습니다.
- 단락 3: 운영자는 언제든지 Google 계정의 「보안」 → 「타사 앱 및 서비스」 페이지(https://myaccount.google.com/permissions)에서 이 사이트의 접근 권한을 취소할 수 있습니다. 취소하면 이 사이트에 저장된 토큰은 즉시 무효가 됩니다.
- 단락 4: 이 사이트에서 동영상 기록이 삭제되면 해당 YouTube 동영상 ID와 API 요청 기록도 함께 삭제됩니다. 저장된 토큰의 삭제나 이 기능에 관한 문의는 이 페이지에 안내된 연락 방법으로 요청해 주십시오. 확인 후 삭제합니다.
- 링크: YouTube 서비스 약관, Google 개인정보처리방침, Google 계정의 타사 앱 권한

서비스 약관(단락): 운영자는 YouTube API 서비스를 통해 이 사이트에서 제작한 동영상을 이 사이트의 자체 YouTube 채널에 게시할 수 있습니다. 이 기능을 이용하면 본 약관 외에 YouTube 서비스 약관(https://www.youtube.com/t/terms)에도 동의하는 것으로 간주됩니다.

## 四、OAuth 同意畫面設定清單

在站主的 Google Cloud 專案做，密鑰不經代理或對話。

| 項目 | 設定 | 依據 |
| --- | --- | --- |
| 要啟用的 API | YouTube Data API v3 | T8 票 |
| 專案 | 一個用戶端一個專案；專案編號填進表單第 5 段 | 頁 2 III.D |
| 使用者類型 | External（沒有 Cloud 組織的個人帳號只有這個選項；Internal 要有組織） | 頁 11 |
| 應用程式名稱 | Mokaair Studio Sync，與表單第 4 段相同 | 頁 9、12：不能用 YouTube、YT，不能把 Google 產品名和通用字組合，不能暗示與 Google 有關係 |
| 應用程式標誌 | 不上傳 | 頁 12：名稱與標誌要經品牌驗證才會顯示，沒驗證的同意畫面只顯示網域；上傳標誌只會多一道驗證 |
| 使用者支援信箱 | 【站主填】 | |
| 應用程式首頁 | https://mokaair.com | 頁 12：首頁要在自己驗證過的網域、要說明產品、要連到隱私權政策 |
| 隱私權政策連結 | https://mokaair.com/en/privacy | 頁 12：要與首頁連到的、與稽核表單填的一致；首頁頁尾在英文語系連到的正是這個網址（`apps/web/components/site-footer.tsx`） |
| 服務條款連結 | https://mokaair.com/en/terms | |
| 已授權網域 | mokaair.com | 頁 12：專案擁有者或編輯者在 Search Console 驗證過的網域；本站已有 Search Console |
| 開發人員聯絡資訊 | 【站主填】 | 頁 15：不回 Google 的通知會失去 API 存取 |
| Scope | 只有 https://www.googleapis.com/auth/youtube.force-ssl | HANDS-OFF §YouTube API |
| 發布狀態 | In production（正式版） | 頁 10、11：測試中的授權 7 天過期、refresh token 跟著過期，而且只能給列出的測試使用者；正式版的 token 不會這樣過期（撤銷、6 個月沒用、超過每個用戶端的 token 數上限除外） |
| 驗證 | 不送 | 頁 11、13：未驗證的正式版會先顯示警告畫面，總共只能有 100 個新使用者，功能照常；本站只有站主一人 |
| youtube.force-ssl 算不算敏感 scope | 待核對 | 讀到的頁面都沒點名；算的話就是上面那個警告畫面，不影響使用 |
| OAuth 用戶端 | 類型「網頁應用程式」；已授權的重新導向 URI 由 T8 決定，形式像 https://mokaair.com/api/…/callback | T8 票 |
| 用戶端密鑰 | 站主自己貼進後台的設定分頁，不進 repo、不進對話 | T8 票 |

## 五、送出之後要一直守的規則（給 T8 與之後的維護）

- **資料保存（頁 2 III.E.4）**：授權權杖可以存到不需要為止；其他透過授權取得的資料最多存 30 天，之後要重新讀取或刪除；每 30 天要確認授權還沒被撤銷。T8 的做法：每月跑一次 `channels.list`（1 單位）確認權杖有效；後台顯示影片狀態時重新讀 `videos.list`，不用超過 30 天的舊副本；伺服器只存影片編號、上架時間與每一步的結果。
- **寫入要由使用者發起（頁 2 III.C.3）**：上架時間由站主選，網站永遠不會自己把影片設成公開，公開由 YouTube 在那個時間做。
- **上傳用戶端的最低功能（頁 8）**：讓使用者上傳的用戶端要能讓使用者設定標題、說明與瀏覽權限。「可以上架」卡片目前只有複製鈕與時間欄；T8 做 `videos.insert` 時，卡片要能改標題與說明、選瀏覽權限（至少 private／unlisted），否則審查者對照這頁會問。
- **一個用戶端一個專案、憑證不外流（頁 2 III.D）**：用戶端密鑰只在後台設定分頁。
- **用途改變要重送；連續 90 天沒用可能被降配額或收回憑證（頁 2、4）**：產線停工超過兩個月時記得跑一次 `channels.list`。
- **稽核要求（頁 2 III.H）**：YouTube 可能要求帳號或資料，要在他們給的期限內回；主要聯絡信箱要有人看。
- **12 個月內可以再申請配額（頁 4）**：若之後一天要上超過 100 支，或字幕改成更多語系，用同一張表單。

## 六、送出紀錄

| 日期 | 事件 | 備註 |
| --- | --- | --- |
| | 送出表單 | 案件編號或自動回覆的主旨 |
| | | |

站主送出之後，同一筆紀錄也寫進票 `tasks/open/2026-09-26-video-hands-off-api-audit.md` 的 Notes；往來的信只記日期與結論，不貼全文。票在稽核有結果之前不要 `done`。
