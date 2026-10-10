# 影片產線：站主只決定上架時間（設計）

2026-09-27 定案。前提是 [`AUTOMATION.md`](AUTOMATION.md) 的主機自動產線與 [`DRAMA.md`](DRAMA.md) 的漫劇路線。站主的要求是：現在等站主的每一個決定，都改由 AI 或 Jev 做，**站主只決定什麼時候上架**。這份寫為什麼這樣分工、每個決定改由誰做、做錯時怎麼退回；工作分成幾張票，id 都是 `2026-09-26-video-hands-off-*`。

## 站主的決定（2026-09-27）

| 原本等站主的事 | 改成 |
| --- | --- |
| 站主觀點 | 站主在設定分頁寫一次「頻道立場」，企劃模型每一支都依這份立場寫站主觀點 |
| 選大綱 | Jev 挑；每個選項在各項標準的得分記在審核頁，當作挑選的理由 |
| 看成片 | 自動品管全部通過就核准；沒通過的才交給站主，審核頁列出沒過的項目 |
| 上架 | 先維持站主在 Studio 手動上傳；同時準備 YouTube API 稽核的申請 |

## 每個決定之後由誰做

| 決定 | 現在 | 之後 |
| --- | --- | --- |
| 題目 | 企劃模型（已自動） | 不變 |
| 站主觀點 | 企劃模型寫草稿，站主選大綱時一併看 | 企劃模型依「頻道立場」寫；Jev 檢查有沒有照立場寫 |
| 選大綱 | 站主 | Jev；沒有一個選項過關時退回企劃模型重寫，重寫兩次仍不過才交給站主 |
| 旁白 | Jev 全部句子都過就自動核准，否則等站主 | 另外加上「改寫一直被聽錯的句子」：重錄之後仍被標記的句子交給聽眾審稿模型改寫措辭 |
| 成片 | 站主 | 自動品管（下面列出的 11 項） |
| 上架確認（`UPLOAD.md` 的自我檢查） | 站主 | 併進自動品管；上傳包備好就自動核准，影片進「可以上架」清單 |
| 上傳與上架時間 | 站主在 Studio 做全部 | 第一步：站主在 Studio 只上傳 mp4（私人），到後台貼上影片網址、選上架時間，其餘由網站用 API 補齊並排程。第二步（稽核通過後）：站主在後台選時間就好 |
| 漫劇的角色設定圖 | 站主每個角色挑一張 | judge 分數最高、且達到門檻的那張 |
| 長篇作品的設定集、總綱、每篇細綱 | 站主逐份核准 | **免關卡作品**（2026-09-27，[`BINGE.md`](BINGE.md)）：查核模型出裁決，伺服器依規則核准或退回重寫；其他作品照舊 |
| 長篇作品的每集劇本 | 站主 | 免關卡作品：查核的節拍覆蓋與量測節奏過就核准；不過先由撰稿模型修，修不好才交給站主 |
| 卡住的影片 | 站主 | 仍然是站主：那是故障，不是決定 |

之後仍然會找站主的情況只有四種：影片卡住（同一階段連續失敗、預算、缺金鑰）、自動品管有項目沒過、Jev 找不到過關的大綱而且已經重寫兩次，以及上架時間。`/admin/videos` 把「需要你」的項目排在最上面，「可以上架」排第二。

## 頻道立場

**為什麼**：YouTube 的「非原創內容」政策點名的，就是沒有創作者觀點、套模板量產的 AI 內容。站主觀點是這條產線對這條政策最主要的回答。要讓 AI 替站主寫觀點，觀點的來源就必須是站主自己寫下的東西，而不是模型自己編出來的。

- 設定分頁新增一格「頻道立場」（最多 4000 字）。它和 #814 的「各階段常設指示」分開：常設指示寫的是**怎麼寫**（格式、用詞），頻道立場寫的是**這個頻道相信什麼**。企劃、撰稿兩個階段，以及 Jev 的兩次檢查都會讀它。
- 企劃模型在 `brief.md` 的「站主觀點」段落，第一行要寫出這支影片套用的是立場的哪幾條（例如「套用立場：2、4」），接著寫出對這個題目的具體看法。lint 會檢查這一行存在，而且引用的條號都存在。
- **立場還是空白時，Jev 不挑大綱**，大綱照舊等站主。這樣在站主寫下立場之前，不會有任何一支影片由 AI 自己決定觀點。
- 站主改了立場之後，只會影響之後才寫企劃的影片；已經寫好的不回頭重寫。

**草稿**（從已經做好的四支影片的站主觀點整理出來，要站主改過、存進設定才會生效）：

1. 先把帳算清楚再花錢：付費是為了真的用得到的額度與能力，不是為了拿掉廣告、追排行榜，或因為「新的比較好」。
2. 官方原文優先：價格、條款、限制以官方頁面當天的寫法為準；查不到或只有登入才看得到的，就直說「以官網為準」，不猜。
3. AI 的整理要點開來源核對：AI 寫的摘要、字卡、新聞稿都可能抄錯，要拿去用之前先看引用。
4. 安全靠技術上的界線，不靠寫在指示裡的「不要」：權限、沙箱、金鑰隔離先做好，再談提示詞。
5. 每支影片都給觀眾一個看完就能做的動作，例如設提醒、改一個設定、把帳分開算一次。
6. 不追每週的熱度：新功能、新排行不是換工具的理由，先回到自己的需求（成本、品質、速度）。
7. 只做資訊與工具教學：不給投資、醫療、法律或選舉政治建議；幣圈只談工具與風險，不談買賣。

## Jev 挑大綱

**時機**：工人寫好企劃之後、送審「選大綱」之前（本機的 `review-push --gate outline` 也走同一條）。條件是設定開著「Jev 挑大綱」，而且頻道立場不是空白。

**怎麼問**：工具呼叫新的端點 `POST /video/automation/judge/outline`，送出 `brief.md` 全文與選項。伺服器讀設定裡的頻道立場，組成一次 Jev 呼叫：

- `pick`：`choice` 題，每個選項一個條件（選項標題、一行說明、開場鉤子）。指示是：挑出最能服務企劃寫的目標觀眾、最符合頻道立場、而且有具體示範或實算的大綱。
- 每個選項各兩題 `noul`：`stance_<key>`（這個選項照頻道立場寫，沒有和立場相反的主張）、`demo_<key>`（這個選項有觀眾能照著做的示範或實算）。
- 整份企劃一題 `noul`：`advice`（這份企劃提供投資、醫療、法律或選舉政治建議）。

一次呼叫最多 3 個選項，也就是最多 8 題，計入既有的 Jev 每日次數。Jev 擅長判斷文字，但不會算數、也讀不準日期（`apps/api/app/ai/jev.py` 開頭的說明），所以這裡只問文字判斷，不問金額或日期對不對，那些是查核階段的工作。

**過關規則**（伺服器端，`outline_pick_passed`）：

- Jev 選的選項 `stance` ≥ 0.6 且 `demo` ≥ 0.6；
- `advice` ≤ 0.3。

過關的話，工人把答案放進審核的 `payload.pick`，連同選擇一起送審；伺服器收到時照規則核准，`choice` 就是 Jev 選的選項。審核頁顯示一張表，列出每個選項的 `pick` 機率、`stance`、`demo`，這就是挑選的理由。

沒過關的話，工人不送審，而是把沒過的原因當成退回意見，交給企劃模型重寫（和站主退回大綱走同一條路，最多重寫 `MAX_REPLANS` 次），之後才卡住、交給站主。

Jev 或網站暫時不行時大綱等一下，之後再問：API 說 Jev 這次判斷失敗（502 `video_judge_upstream_failed`）、網站的路由沒連到 API（502 `upstream_unavailable`）、限流器暫時不能計數（503 `rate_limit_unavailable`）、限流或每日次數用完（429），或連線根本沒送出去。Jev 沒設金鑰（503 `provider_unavailable`）是站主要處理的事。其他的 5xx（包括 API 的 502 `video_judge_outcome_uncertain`、路由的 504 `video_judge_answer_lost`、閘道的錯誤頁），以及送出後連線斷掉或回答讀不出來，都算回答在途中遺失（`judgeOutline` 回 `lost`），不再自己問：Jev 可能已經判斷並用掉當天一次，工人把影片卡住（`uncertain:judge`），站主按重試才對同一份企劃再問一次；本機的 `review-push --gate outline` 則把大綱直接送給站主、不附選擇，並在 `review/outline-lost.json` 記住這份企劃，不會再問（[`AUTOMATION.md`](AUTOMATION.md) §回答在途中遺失）。

門檻先訂成常數，寫在程式與這份文件裡。第一批五支影片做完之後，對照站主自己會怎麼選，再決定要不要調整。

## 自動品管（成片）

新指令 `node tools/video/cli.mjs qa --slug <slug>` 會寫出 `<工作區>/<slug>/review/qa.json`：`{ ok, final_sha256, items: [{ id, ok, detail }] }`。`review-push --gate final` 會先跑它，再把結果放進 `payload.qa`。

| id | 檢查 | 來源 |
| --- | --- | --- |
| `assemble` | 畫格數、影音差距 ≤ 1 格、響度、每章第一格的 PSNR | 既有的 `checks.json` |
| `render` | 超框、缺字、每種字型、程式碼框切行 | 既有的 render 檢查（#782） |
| `narration` | 核准過的旁白時間軸，就是現在這一份 | `approvals.json` |
| `pace` | 沒有一個畫面停超過 15 秒 | 時間軸加上畫面計畫；把 2026-09-26 重排第二批時用的檢查做成正式工具 |
| `captions` | 設定裡每個語系都有字幕檔；翻譯沒有過期，包含章節、標題、說明、標籤。每秒字數超標只列成警告 | `i18n/<locale>.json` 與 lint 既有的過期警告（章節與說明欄的雜湊來自已完成的票 `2026-09-26-video-i18n-sheet-flags-stale-chapters`），這裡把警告升級成品管失敗 |
| `metadata` | 每個語系的 YouTube 上限：標題、說明欄位元組、標籤、章節規則 | 既有的 lint |
| `facts` | 最後一輪查核標成 NOT FOUND 的說法，已經不在稿子裡 | `verify-*.md` 對 `video.json` |
| `links` | 說明欄的每個網址都回 200，文章連結是已發布的文章 | 工人用固定的 User-Agent 抓，每個網域間隔 1 秒 |
| `thumbnail` | 1280×720、< 2 MB、縮到手機寬度時標題字高仍然夠大 | render 的縮圖檢查 |
| `policy` | Jev：旁白照頻道立場寫、有示範或實算（只問教學類的影片，見下面）、沒有投資醫療法律政治建議、沒有業配 | 新端點 `POST /video/automation/judge/policy`，門檻同上 |
| `disclosure` | 依規則決定要不要勾「變造或合成內容」：投影片加一般 TTS 不需要；漫劇一律要勾 | 寫進上傳包的 `metadata.json`，不會讓品管失敗 |

**誰會被問「有示範」**：這一題是教學影片的規矩，伺服器依自己資料庫裡這支影片的那一列決定（`judge.policy_questions_for`），工人的請求不能指定。分類（`category`，見 §影片分類）是 `explainer` 觀念解說或 `story` 品牌故事的影片，以及格式（`format`）是 `drama` 的影片，不問這一題：回應的 `demo` 是 `null`、`questions` 是 `explainer`，備註寫「有示範：不適用（解說）」，`passed` 只看其餘三題。其他分類（`tutorial`、`ai-terms`、`ai-news`、`comparison`、`travel`、`other`……）照舊四題都問；伺服器查不到這支影片、或影片還沒分類時，也照舊問。品牌故事作品的集另有自己的五題（`STORY.md`），長片精華 Shorts 也不問示範（`SHORTS.md`）。奇聞檔案局、原來如此這類用史料或道理講一件事的影片，分類填 `explainer` 就不會卡在這一題。

**過關規則**（伺服器端，`final_qa_passed`）：`qa.ok` 為真、`qa.final_sha256` 等於這份審核的雜湊，而且伺服器自己列的必要項目每一項都在、都過。最後這一條是為了避免少跑了某一項的舊版工具被當成全部通過。設定「自動品管全過就核准成片」開著時，審核在送達的當下就核准，備註寫「自動品管 11 項全過，依設定自動核准」。

沒過的話，審核照舊等站主。摘要寫「自動品管 2 項沒過：pace、links」，審核卡片的最上面列出沒過的項目與細節。站主可以照舊核准或退回。

`policy` 的回答在途中遺失時（Jev 可能已經判斷並用掉當天一次），`qa` 在 `qa.json` 記下 `policy_lost`（請求的雜湊、成片雜湊、時間、原因），同一段旁白不再問，項目寫「outcome unknown」，以結束碼 3 收尾；`review-push --gate final` 不送審。工人把影片卡住（`uncertain:policy`），站主按重試時清掉這筆紀錄，Jev 再被問一次，過了照樣自動核准。Shorts 的品管也一樣：Short 卡住，重試時再問一次。

**同一份成片再送一次時重新判斷**：現在同一個雜湊再送審，伺服器會直接回傳既有的那一筆。改成：既有那筆還在等站主時，換上新送來的 payload，再跑一次自動規則。字幕、連結、說明欄這類不會改變 `final.mp4` 的修正，修好之後再送一次就會重新判斷。第二批三支已經送審的成片，也能用這個方式補上品管結果。

## 上傳包與「可以上架」

- 成片核准之後，工人照舊跑 `package`，再多跑一次品管的上傳包部分：檔案齊全、四個語系的說明欄與字幕都在、揭露的答案已經寫好。通過就送審「確認上架」，而且自動核准。
- 「確認上架」這筆審核會附上完整的上傳包：1080p 的 `final.mp4`、`thumbnail.jpg`、四條字幕、四個語系的說明欄。站主不用碰主機，直接從後台下載。成片照既有的分段上傳送進審核檔案區；影片標成已上架滿 7 天後，mp4 就從檔案區刪除，以節省主機磁碟。
  - **成片多大**（2026-10-04 實測，細節在 `ILLUSTRATED.md` §成片大小）：純投影片約 10 MB／分鐘（十分鐘約 90–100 MB）；插圖投影片約 40 MB／分鐘（13:22 的一支 535 MB），最壞情況約 70 MB／分鐘（運鏡段的位元率上限是 8 Mbit/s）。成片關卡送的 720p 預覽另外約 7 MB／分鐘。
  - **單檔上限**：`VIDEO_REVIEW_MAX_FILE_BYTES`，預設 1.5 GB（原本 400 MB 是照純投影片訂的，2026-10-04 一支 895 MB 的插圖投影片在這一關被 413 `video_review_file_too_large` 擋下）。合集的 720p 預覽要 2.5 GB，見 `BINGE.md`。
  - **磁碟成本**：檔案區總量上限 `VIDEO_REVIEW_MAX_TOTAL_BYTES` 預設 20 GB，滿了回 507 `video_review_store_full`。一支 13 分鐘的插圖投影片從送出上架確認到上架後 7 天，佔預覽加成片約 0.63 GB；20 GB 大約同時放得下 30 支：每天兩支、上架後留 7 天是 14 支約 9 GB，另外還有其他影片的預覽（2026-10-04 時檔案區已用 6.5 GB）。成片在「可以上架」放著沒上架就一直佔著，檔案區會滿多半是這個原因，不是單檔上限。
- `UPLOAD.md` 只留操作步驟。原本「上架前自我檢查」的項目都已經併進自動品管。
- `/admin/videos` 最上面新增「可以上架」：每支列出標題、長度、章節數、下載連結、中文標題、說明欄與標籤的複製鈕，以及揭露要怎麼勾。站主上傳之後，在同一張卡片貼上 YouTube 網址（第一步之後，也在這裡選上架時間）。伺服器記下 `youtube_video_id`，工人下一輪把它寫進工作區的 `video.json`，這支影片就算完成。

## 影片分類（2026-09-30 加）

- 每支影片有一個 `category`，十一選一：`ai-terms` AI 名詞解釋、`ai-news` AI／科技時事、`tutorial` 教學實作、`comparison` 比較評測、`explainer` 觀念解說、`story` 品牌故事、`drama` 漫劇（`DRAMA.md`、`SERIES.md` 的三分鐘一集）、`long-drama` 長篇劇（接下來規劃的一集 40–60 分鐘、40–50 集的作品）、`anime` 動漫、`travel` 旅遊、`other` 其他；沒有就是「未分類」。清單定義在 `apps/api/app/models.py` 的 `VIDEO_CATEGORIES`，工具端同一份在 `tools/video/core/schema.mjs`，資料庫用 `ck_video_project_category` 擋（遷移 0116 建立、0118 加上 `anime`）。
- **誰填**：`video.json` 頂層可以寫 `category`，工具回報時帶上；伺服器只在這支影片還沒分類時採用，之後的回報不會覆寫，因為工人每個階段都會重送一次回報，若每次覆寫，站主在後台改的會被洗掉。站主在 `/admin/videos` 的影片詳情頁隨時可以改（`PUT /admin/videos/{slug}/category`，寫 `video_category_set` 稽核），改成「未分類」也可以。品牌故事一律 `story`；`import` 的 `meta.json` 可帶 `category`。遷移用四條規則回填既有影片（只填未分類的、依序）：品牌故事作品（`video_drama_series.kind = story`）的集是 `story`、其餘 `format = drama` 的非 Shorts 影片是 `drama`、`source_guide` 以 `ai-news-` 開頭的是時事、slug 以 `ai-term-` 開頭的是名詞解釋，其餘留給站主。
- **清單**：「等你決定」與「可以上架」兩組維持在最上面；底下是全部影片的目錄（`GET /admin/videos/browse`，教學與戲劇都在，只有 Shorts 不在、留在 Shorts 分頁）：分類與狀態（進行中／已上架／已放棄）兩排篩選膠囊帶數量、標題或代號搜尋、每頁 30 支的分頁，條件都在網址（`category`、`state`、`q`、`page`）；戲劇集在標題下標明作品與集數，戲劇分頁照舊。舊的 `GET /admin/videos` 清單形狀不變，工人與其他分頁照舊讀它。

## YouTube API：分兩步

**第一步：不需要稽核。** YouTube 鎖成私人的，只有「未通過稽核的 API 專案用 `videos.insert` 上傳」的影片。站主在 Studio 上傳的私人影片，可以用 `videos.update` 設定 `status.publishAt`（官方規則：影片必須是私人、而且從來沒有公開過；更新時也要把 `privacyStatus` 設成 `private`）。流程是：

1. 站主在 Studio 只上傳 `final.mp4`，瀏覽權限選私人，其他欄位都不用填。
2. 在後台「可以上架」的卡片貼上網址、選上架時間。
3. API 容器用站主授權過的 OAuth 權杖送出以下請求，約 2,100 配額單位，每日預設額度是 10,000：
   - `videos.update`：四語系的 `localizations`、標籤、分類、`containsSyntheticMedia`、`publishAt`。先讀現值、合併後整段送出，並帶上 `snippet.defaultLanguage`。
   - `captions.insert` 五次。
   - `thumbnails.set`。
4. 送出結果記在審核頁。到了排定的時間，YouTube 自己公開影片。

OAuth 的做法：

- 在站主的 Google Cloud 專案建立 OAuth 用戶端，授權流程在網站上跑。站主在瀏覽器按同意，refresh token 存在 API 那一側，和其他廠商金鑰一樣不會再顯示出來。工人、代理與這個對話都碰不到權杖。
- 同意畫面要設成「正式版」（In production）。留在「測試中」的話，refresh token 7 天就會過期。沒有驗證的正式版應用程式會顯示警告畫面，而且最多 100 個使用者，但只有站主一個人用，不受影響。
- scope 是 `youtube.force-ssl`。

有兩件事要實測後才寫進 skill 的 `publish.md`：

- 沒有稽核的專案，能不能對 Studio 上傳的影片呼叫 `captions.insert` 與 `publishAt`；
- 中文字幕的語言碼要用 `zh-TW`，還是 `zh-Hant`。

這一步取代原本 T8（`2026-09-24-video-youtube-sync`）「在站主電腦上用桌面 OAuth」的做法，因為工人已經搬到主機，金鑰只能放在 API 容器。

**T8 做好的樣子（2026-09-27）**：連結在設定分頁的「YouTube 頻道」卡片（重新導向 URI 是 `https://mokaair.com/api/admin-video-youtube/callback`，卡片上可以複製）；送出在「可以上架」卡片的「送到 YouTube」表單，兩種來源都做了：站主在 Studio 上傳後貼網址（第一步），或由網站自己用 `videos.insert` 續傳上傳（第二步，稽核通過前要站主勾「會被鎖成私人」，用來實測與截稽核附件）。卡片也有「YouTube API 稽核已通過」的勾選，勾了之後上傳不再多問，預設來源改成由網站上傳。步驟、重試與失敗原因在 skill `youtube-video` 的 `references/publish.md`。

**第二步：稽核通過之後。** 網站自己用 `videos.insert`（續傳上傳）上傳 mp4，同時帶上 `publishAt`。站主只在後台選時間。

稽核走「YouTube API Services - Audit and Quota Extension Form」，由站主用自己的 Google 帳號送出。要準備的東西：

- 用途選「Video Uploading & Account Management」與「Internal Company Tool」，預估每日請求數選「少於 1,000」。
- 隱私權政策要加一段 YouTube API 的說明：
  - 使用了 YouTube API Services，並連到 YouTube 服務條款與 Google 隱私權政策；
  - 存取與保存了哪些資料（只有這個頻道自己的影片與字幕）；
  - 怎麼從 Google 帳戶的安全性設定撤銷授權；
  - 刪除資料的方式。
  
  隱私權政策在後台的法律頁面維護，五種語言都要改，由站主或內容線處理。
- 首頁找得到隱私權政策連結的截圖，以及服務條款。
- OAuth 流程的截圖（同意畫面、scope、撤銷方式），以及上傳介面（「可以上架」卡片）的截圖。這些要等第一步做完才截得到。
- API 用戶端名稱不能含「YouTube」。

申請書的草稿寫在 `docs/videos/YOUTUBE-API-AUDIT.md`（票 `2026-09-26-video-hands-off-api-audit`）。

## 旁白：改寫一直被聽錯的句子

2026-09-26 第二批的旁白，最後是靠人工改措辭才收斂：「和」改成「跟」、句尾的「答」改成「回答」、「旗艦」改成「旗艦模型」。這一步可以交給模型做：

- 重錄到上限之後仍被標記的句子，連同 Gemini 聽到的內容，交給聽眾審稿模型，只改這幾句的措辭；
- 數字、專有名詞與說法不能改，lint 會比對改寫前後出現的數字與拉丁字詞；
- 改完用 `tts --redo` 重錄這幾句，再檢查一次，最多兩輪；
- 還是不過，才等站主。

## 漫劇的設定圖

`look` 階段已經幫每個角色標出分數最高的 `suggested`。設定分頁加一個開關「設定圖自動選」：分數最高的那張達到 `judge_min_score`、而且沒有列出問題時，伺服器就用它核准這個角色的 `look` 審核。預設關閉，理由和 `auto_approve_storyboard` 一樣：第一支漫劇要由站主看過。這張票在漫劇那條線（`2026-09-26-video-hands-off-drama-look`），要先和那條線的 session 協調。

## 免關卡的作品：文件與劇本由查核決定（2026-09-27 加，設計在 [`BINGE.md`](BINGE.md)）

長篇作品（`SERIES.md`）多了每部作品自己的旗標 `hands_off`；後台的「一鍵開拍」預設開著。開著時，原本等站主的四份文件與每集劇本都由查核模型的答案加伺服器規則決定（`apps/api/app/video_automation/judge.py`），跟 Jev 挑大綱、自動品管同一個信任模型：工人的 payload 帶判斷，伺服器套門檻，每筆寫進 `admin_audit_logs`。

| 決定 | 規則 | 常數 |
| --- | --- | --- |
| 設定集、總綱、篇章細綱 | `series_doc_passed(judge, kind)`：查核在新 session 對文件出裁決 `{verdicts: {項目: 有／弱／無}, problems, similar_works, notes}`；該 kind 的必要項目都在、沒有「無」、「弱」最多一個、`problems` 與 `similar_works` 都空才過。過→核准；不過→退回重寫（`series_doc_rewrites` 輪）；重寫用完→停在待審，卡片附查核的問題 | `REQUIRED_VERDICTS`（setting 4 項、outline 5 項、chapter 6 項）、`MAX_WEAK_VERDICTS = 1` |
| 每集劇本 | `script_check_passed(payload, retention_required)`：`coverage` 的 hook／conflict／turn／cliffhanger 沒有「無」、「弱」≤ 1；`continuity_problems` 與 `similar_works` 空；有節奏規格的題材再看 `coverage.satisfaction`、`retention.hook_seconds`、`retention.satisfaction.count`／`first_seconds`、`retention.cliffhanger_last`。秒數由工人在估計時間軸上量，不是模型估的 | `COVERAGE_BEATS`、`HOOK_MAX_SECONDS = 8.0`、`FIRST_SATISFACTION_MAX_SECONDS = 30.0`、`MIN_SATISFACTION = 2`、`RETENTION_GENRES` |
| 設定圖、分鏡 | 影片屬於免關卡作品時，`auto_pick_look`／`auto_approve_storyboard` 視為開著，門檻仍是 `judge_min_score` | — |
| 合集成片 | `final_qa_passed` 對合集影片改用六項 `COMPILATION_QA_ITEMS`（報告要有 `kind: "compilation"`）；每集自己已過完 11 項 | `COMPILATION_QA_ITEMS` |

沉默不算通過：少一個鍵、多一句問題、舊工人沒帶的欄位，都留給站主。站主把作品的「免關卡」關掉，就回到逐份核准。門檻先訂成常數，試作（票 `2026-09-27-video-binge-pilot`）後對照站主自己會怎麼判再調。

## 設定（新增到 `video_automation_settings`）

| 欄位 | 預設 | 說明 |
| --- | --- | --- |
| `channel_stance` | 空 | 頻道立場，最多 4000 字 |
| `auto_pick_outline` | 開 | 立場空白時，這個開關沒有作用 |
| `auto_approve_final` | 開 | 自動品管全過就核准成片；上傳包備好就核准「確認上架」 |
| `auto_pick_look` | 關 | 漫劇的設定圖 |

遷移接在 #814 的 `0098_video_stage_instructions` 之後。開票時 main 最新的是 `0097`，實作前要再查一次 main。

## 安全與失敗

- 自動核准都在伺服器端判斷，依據是工具送來的 payload，和旁白、分鏡的自動核准同一個信任模型。工人的權杖本來就能送審，這裡沒有擴大它能做的事。每一筆自動核准都寫進 `admin_audit_logs`（`video_review_auto_approved`）。
- Jev 或品管的外部請求失敗時，視為「沒過」：審核留給站主，或下一輪再試。不會因為判斷不了就直接核准。
- 站主隨時可以在設定分頁關掉任何一個自動開關，或放置 `STOP` 檔，讓整條產線停下來。

## 票

| 票 | 內容 | scope | 依賴 |
| --- | --- | --- | --- |
| `video-hands-off-settings` | 遷移（立場與三個開關）、設定 API、設定分頁、工具讀取端點帶出立場 | `apps/api/app/video_automation`（models、schemas、settings）、遷移、`apps/web/components/admin-video-settings*`、`admin.json` | #814 已合併 |
| `video-hands-off-judge` | `judge.py` 與兩個 judge 端點、`outline_pick_passed`／`final_qa_passed` 規則、送審時自動核准與同雜湊重新判斷 | `apps/api/app/video_automation/judge.py`、`admin_api.py`、`apps/api/app/video_reviews/admin_service.py` | settings |
| `video-hands-off-qa` | `qa` 指令、`pace` 檢查、連結與縮圖檢查 | `tools/video/qa`、`tools/video/cli.mjs` | — |
| `video-hands-off-worker` | 企劃提示帶立場、Jev 挑大綱與不過時重寫、`review-push` 帶 pick 與 qa、上傳包附完整檔案、讀回 `youtube_video_id`、skill 文件 | `tools/video/automation`、`tools/video/review`、`tools/video/package`、`.agents/skills/youtube-video`、`.claude/skills/youtube-video` | judge、qa |
| `video-hands-off-web` | 審核卡片顯示 Jev 的理由與品管項目、「可以上架」清單、貼網址與時間的表單、`POST /admin/videos/{slug}/youtube` | `apps/web/components/admin-video-reviews*`、`apps/web/app/api/admin/videos`、`apps/api/app/video_reviews`（schemas、admin_api） | judge |
| `video-hands-off-narration-rewrite` | 改寫一直被聽錯的句子 | `tools/video/automation/narration*` | worker |
| `video-youtube-sync`（改寫 T8） | 第一步：網站上的 OAuth、`videos.update`＋`publishAt`、字幕、縮圖 | `apps/api/app/video_youtube`、遷移 | web |
| `video-hands-off-api-audit` | 稽核申請書草稿、隱私權政策要加的段落、截圖清單 | `docs/videos/YOUTUBE-API-AUDIT.md` | 截圖要等 T8 |
| `video-hands-off-drama-look` | 設定圖自動選 | 漫劇那條線協調後決定 | settings |

順序：settings → judge → web、worker（qa 可以最先平行做）→ narration-rewrite；T8 接在 web 後面；稽核草稿隨時可以寫。
