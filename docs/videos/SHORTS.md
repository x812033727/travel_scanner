# Shorts 區：後台分頁、三條內容線、全自動上架（設計）

2026-09-28 定案。前提是 [`DESIGN.md`](DESIGN.md) 的產線、[`AUTOMATION.md`](AUTOMATION.md) 的主機工人、[`HANDS-OFF.md`](HANDS-OFF.md) 的分工與 YouTube API 兩步、[`DRAMA.md`](DRAMA.md) 的漫劇路線，以及 PR #871 的本機 Shorts 試片產線（[`ai-shorts/README.md`](ai-shorts/README.md)、`tools/video/shorts`）。這份寫：`/admin/videos` 多一個 **Shorts 分頁**之後，一支直式短片從題目到公開、再到成效回報，每一步在哪裡發生、由誰決定、出錯時怎麼辦。工作分成 15 張票，id 都是 `2026-09-28-video-shorts-*`。

## 站主的決定（2026-09-28）

| 項目 | 決定 |
| --- | --- |
| 「Shorts 區」在哪裡 | 後台 `/admin/videos` 的 Shorts 分頁。前台（mokaair.com 給訪客看的頁面）這次不做 |
| 放哪些內容 | 三條內容線：**「AI 真的可以？」實測**、**長片精華**、**漫劇直式短篇**。旅遊短片不做 |
| 站主參與多少 | **全自動**：製作、品管、排時段、上架都不等站主。站主看每週報告，隨時可以喊停 |
| 誰製作 | 兩條都留、分期做：第一期把本機（或 Codex）做好的 Shorts 接進後台；第二期由主機工人自動做 |

## 現況與缺口

PR #871（2026-09-28 合併）交付的是本機產線：`node tools/video/shorts/cli.mjs validate|build|track-init|report`、15 題企劃、三支試片、90 天 120 個時段的排程表。它刻意不碰伺服器，所以：

| 要做的事 | 現在 | 這份之後 |
| --- | --- | --- |
| 看試片 | 到這台電腦的 `mokaair-work/shorts/<slug>/…/upload/final.mp4` 找檔案 | Shorts 分頁直接播 9:16 預覽，疊上 Shorts 介面的遮擋範圍 |
| 決定能不能上 | 票上寫「站主聽審」，沒有紀錄的地方 | 自動品管的報告、伺服器的核准紀錄、每一筆都進 audit log |
| 排哪一天上 | repo 外的 `calendar.csv` | 伺服器的時段表，Shorts 做好自動排進去 |
| 上架 | 站主在 Studio 填全部欄位、自己設時間 | 稽核前：站主只把檔案拖進 Studio，其餘網站做；稽核後：網站自己上傳 |
| 成效 | 站主從 Studio 匯出、手動對欄位填 `metrics.csv`、跑 `report` | 網站在第 1、3、7 天自己讀 YouTube 的數字 |
| 花費 | 手填 `costs.csv` | 旁白、圖片、片段的花費自動記帳，其餘在分頁補一筆 |
| 旁白 | Windows 的 Hanhan 本機語音（試片用） | 頻道聲音（Gemini Sulafat，經伺服器），跟長片同一個人 |
| 誰做下一支 | 開一個 session 照企劃做 | 主機工人照每週排片自己做 |

另外有兩批本機做好的 Shorts 等著接進來：#871 的三支試片，以及開著的 PR #880 的 12 支（六集長片各切兩支）。

三件卡住「全自動」的事，都是既有的票、都在等站主（2026-09-28 查證）：

1. **頻道還沒通過 YouTube API 稽核**：未稽核的專案用 API 上傳的影片一律鎖成私人。申請書草稿在 [`YOUTUBE-API-AUDIT.md`](YOUTUBE-API-AUDIT.md)，送件前要先在法律頁貼上 YouTube API 段落；`https://mokaair.com/en/privacy` 今天還沒有那一段。
2. **頻道立場還是空白**：自動品管的 `policy` 項要對照頻道立場（`HANDS-OFF.md` §頻道立場），空白就永遠不過。
3. **頻道連結**（設定分頁的「YouTube 頻道」卡片）要站主自己在 Google Cloud 建用戶端、按允許；實測票 `2026-09-27-video-youtube-sync-field-test` 還開著。

## 名稱

| 站主看到的 | 內部 | 內容 |
| --- | --- | --- |
| Shorts | `video_projects.shorts_line` 不是空的影片 | 1080×1920、30 fps、25–55 秒的直式短片。用哪條產線做的另外記在 `format`（字卡式是 `shorts`，漫劇直式是 `drama`） |
| 內容線 | `shorts_line`：`lab`、`cut`、`drama` | 實測、長片精華、漫劇直式短篇 |
| 系列 | `shorts_series` | 實測線是 `daily`（台灣日常）、`blind`（成品盲選）、`prompts`（提示驗證）；另外兩條線是來源的長片或作品代號 |
| 題庫 | `video_shorts_topics` | 還沒做的題目：15 題企劃、企劃模型每週補的新題、每支長片與每集漫劇自動生出的題目、站主自己丟的想法 |
| 時段 | `video_shorts_slots` | 月曆上的一格：幾月幾日幾點公開一支。預設照 #871 的節奏：前 30 天每天 19:30 一支，之後 60 天單雙日輪流一支與兩支（加 12:30），共 120 格 |
| 片庫 | 已核准、還沒排進時段的 Shorts | 庫存。少於 `stock_days` 天的量，工人就優先做 Shorts |
| 上傳包 | `publish` 審核的檔案 | `final.mp4`、`zh-TW.srt`、`cover.png`、`metadata.json`、說明欄文字；實測線另有原始證據 |
| 自動上架授權 | `video_shorts_settings.consent_*` | 站主明確同意「網站照月曆替我上傳與排程」的那一次按鈕，連同當時看到的條文雜湊 |
| 成效快照 | `video_shorts_metrics` | 公開後第 1、3、7 天，以及最新一次讀到的 YouTube 數字，原樣存下 |
| 花費帳 | `video_shorts_costs` | 每一筆花費：已確認、已預留、未知 |
| 每週報告 | `video_shorts_reports` | 每週一由企劃模型寫：上週發了什麼、數字、花費、卡住的事、下週排片 |

## 一支 Shorts 的一生

```
題庫
  → 每週排片（企劃模型把題目排進下週的時段；各內容線有配額）
  → 製作（依內容線，見下一節）
  → 自動品管 12 項 → 伺服器規則
        全過：核准 → 上傳包 → 進片庫
        沒過：先自動修（每種最多 2 輪）；修不好就放進「需要你」，時段改用片庫裡的下一支
  → 排進時段（公開前 lock_hours 小時鎖定那一格用哪一支）
  → 上架
        稽核通過前：站主把一批 mp4 拖進 Studio（私人）→ 網站依檔名認領 → 補標題、說明、字幕、揭露、publishAt
        稽核通過後：網站在鎖定時自己上傳，同時帶上 publishAt
  → YouTube 在時段到的那一刻公開
  → 成效快照（第 1、3、7 天）→ 每週報告 → 下週排片
```

站上看到的狀態（伺服器算，`shorts_state`；判斷的順序是已放棄、已公開、需要你、已排程、已排時段、片庫，所以等站主處理的影片不會被它的時段蓋住）：

| 狀態 | `shorts_state` | 條件 | 在分頁的哪裡 |
| --- | --- | --- | --- |
| 製作中 | `making` | 有影片、上傳包還沒核准 | 製作中 |
| 需要你 | `needs_you` | 有審核在等站主（品管沒過且自動修完仍不過）、卡住（同一步連續失敗、預算、缺金鑰、缺素材） | 需要你 |
| 在片庫 | `library` | 上傳包已核准、沒有時段 | 片庫 |
| 已排時段 | `slotted` | 佔著一格（`assigned` 或 `locked`）、還沒排上 YouTube | 月曆；稽核前同時列在「等你上傳」 |
| 已排程 | `scheduled` | 有影片 id、`publishAt` 在未來、同步完成 | 月曆 |
| 已公開 | `published` | `publishAt` 已過（Y1 確認 YouTube 回報公開之後，時段也標成 `published`） | 成效 |
| 錯過時段 | `missed` | 錯過了一格、現在沒有佔任何一格；它人在片庫，下一個空格會輪到它 | 片庫（標「錯過」）、每週報告 |
| 已放棄 | `dropped` | 站主或規則放棄 | 已放棄 |

全自動之下仍然會找站主的情況只有這些：頻道連結或自動上架授權失效、稽核前要上傳的那一批、品管自動修不好的那一支、卡住的影片、題目缺站主才有的素材（自己拍的照片）、預算到頂、片庫連續幾天是空的。

## 三條內容線

| | 實測（`lab`） | 長片精華（`cut`） | 漫劇直式短篇（`drama`） |
| --- | --- | --- | --- |
| 來源 | 題庫的企劃：固定輸入、先寫好的答案、評分方式、失敗時怎麼辦 | 已經公開的教學長片（有 YouTube 影片 id） | 成片已核准的漫劇集數或合集 |
| 觀眾拿到什麼 | 一次真的測試的結果，連限制一起說 | 長片裡最值得記住的一段，結尾導回完整影片與文章 | 一個鉤子加一個懸念，導回完整的一集 |
| 怎麼做 | 凍結題目 → 受測模型在全新對話各跑一次 → 對答案 → 撰稿照實寫（平手就說平手）→ 查核對證據 → 旁白 → 字卡 → 成片 | 企劃模型從長片挑 1–2 段（鉤子到結論在 55 秒內）→ 撰稿改寫成直式字卡與 38 字內的短句 → 旁白 → 成片 | **原生路線**：從該集挑鏡頭與台詞 → 每鏡用原關鍵影格當參考重畫一張 9:16 → 靜圖加運鏡，最多兩鏡買片段 → 燒錄字幕 → 成片。**後製路線**（2026-10-05，`from-drama`）：站主選已核准成片的一段（`--from`／`--to`，不切到句子）→ 每鏡問一次 `locate` 找主角的方框 → 9:16 視窗置中在方框上、換鏡前 15 格線性移到下一鏡 → 字幕走 Shorts 的字幕層 → 成片；不生任何圖 |
| 產線 | `tools/video/shorts`（`format: "shorts"`） | 同左 | 原生：漫劇產線加 9:16（`format: "drama"`、`aspect: "9:16"`）。後製：`tools/video/shorts/from-drama.mjs`（`line: "drama"`，送審時 `format: "drama"`） |
| 旁白 | 頻道聲音 | 頻道聲音；句子跟長片一字不差時旁白快取直接命中 | 沿用該作品的旁白與角色聲音；後製路線直接剪該集的混音（人聲、配樂、音效一起）再正規化 |
| 一支的花費（估） | 旁白不到 NT$1；模型走訂閱帳號；要生圖的題目每張約 NT$4 | 同左，沒有生圖 | 原生：約 7 張圖加 0–2 個片段，約 NT$30–90。後製：每鏡一次 `locate`（US$0.01 一次，記在 judge 的額度），一支不到 NT$5 |
| 揭露 | 字卡加一般 TTS 不用勾；有擬真生成圖的那幾題要勾 | 不用勾 | 一律勾「變造或合成內容」 |
| 分類 | 28（科學與技術） | 28 | 24（娛樂） |
| 第一期（本機做好的） | #871 三支試片、之後本機做的 | PR #880 的 12 支 | 後製路線本機就能做（`from-drama`，2026-10-05）；原生路線沒有 |
| 第二期（主機自動） | 先做：15 題裡有 8 題只用文字（01、03、06、07、09、13、14、15），1 題產出不含程式的 HTML（02） | 第二個做 | 最後做：要等漫劇試作（`2026-09-26-video-drama-pilot`）先跑出第一集 |

實測線其餘六題暫時排不進自動產線，題庫會標出原因：

- 04 景點照片、08 修圖、10 菜單、11 手繪草圖要站主自己拍的照片或手繪：標成「缺素材」，站主在分頁的素材箱上傳並填拍攝者與授權之後才會排進去。受測模型要看圖，得接一個有金鑰的視覺模型（訂閱帳號的執行環境只收文字）。
- 12 生圖要花錢（一張約 NT$4），受預算管。
- 05 珍奶小遊戲與 11 的網頁成品要真的執行模型寫的程式、在手機尺寸上操作錄影；現在的渲染環境刻意關掉 JavaScript、擋掉所有網路請求，要另外做隔離的執行環境才行。

沒有素材或工具時用已備料的題目遞補，不做假的操作畫面（#871 的規則）。

漫劇直式短篇的來源不只原本的漫劇：同一天（2026-09-28）另一條線在規劃「品牌故事影片」（票 `2026-09-28-video-story-*`，設計文件 `STORY.md` 在那條線的分支上，還沒合併）——100 支 16:9、12–15 分鐘、全靜態圖的商業故事，每天 12:00 與 20:00 各一支，用的也是漫劇產線。它們上架之後一樣可以切直式短篇（`shorts_line: "drama"`、`source_slug` 是那一集）。這份只定短篇進 Shorts 區之後怎麼排程、品管、上架；故事內容由各自的線決定。不是從某一集切出來的獨立直式小故事，`source_slug` 留空。

兩條線會在同一個頻道上同時發片。Shorts 預設的時段（12:30、19:30）跟品牌故事的時段錯開半小時；稽核通過前站主每天要為品牌故事上傳兩支長片，Shorts 的「依檔名認領」做好之後，長片也可以改用同一個做法（不在這份的範圍）。

## Shorts 分頁

分頁順序是「影片｜漫劇｜**Shorts**｜設定」，網址 `?tab=shorts`；`?tab=shorts&view=calendar|library|metrics|costs|topics|report|settings`；`video=<slug>` 仍然優先開單支影片的頁面。「影片」分頁的清單改成只列 `format` 是 `slides` 而且 `shorts_line` 是空的影片，Shorts 不會混進去。

| 區塊 | 內容 |
| --- | --- |
| 頂列 | 自動上架（開、暫停、沒有授權）；今天與明天的時段；片庫還夠幾天；本期花費與上限；頻道連結狀態；「需要你」的數量；90 天目標旁邊放 YouTube 回報的 Shorts 觀看數 |
| 需要你 | 每一項寫清楚要站主做什麼：重新授權、上傳這一批、看這支沒過的品管（核准、退回並寫原因、放棄）、補素材、調預算 |
| 等你上傳（只在稽核通過前） | 接下來 `upload_ahead_days` 天要上的 Shorts：「下載這一批」（一個 zip）、三行步驟、「我上傳好了」按鈕。按了之後網站去頻道找這些檔案 |
| 月曆 | 一天一列，每個時段顯示題目、內容線、狀態。可以換時段、抽掉、指定某一支、標「這格不發」 |
| 片庫與製作中 | 每支一張卡：封面、長度、內容線、品管結果、排在哪一格 |
| 花費 | 這 30 天對上限的狀況、三個 30 天區間各自的合計、每一筆帳；補一筆、替「不知道金額」的那一筆補上金額、刪掉自己補錯的 |
| 成效 | 已公開的每一支：公開時間、第 1／3／7 天與最新的觀看、喜歡、留言；連結了 Analytics 之後多 engaged views、平均觀看百分比、分享、新增訂閱。數字旁邊寫來源與讀取時間 |
| 題庫 | 依內容線列出題目與狀態；「新增想法」一格；缺素材的題目旁邊是素材箱 |
| 每週報告 | 每週一份，最新的在最上面 |
| Shorts 設定 | 時段與節奏、各內容線的每週配額、庫存天數、聲音、預算、語言、自動上架授權。要 `settings.manage`；其他操作只要 `content.manage` |

單支 Shorts 的頁面：

- **9:16 預覽**：直式播放器，寬度固定、不裁切。一個開關疊上 Shorts 介面會蓋住的範圍（右側按鈕欄與底部標題區），對照 `tools/video/shorts/build.mjs` 的安全區：內容在 x 78–902、下緣 1380 以內，字幕條下緣 1600 以內。
- 兩個標題（使用中的與備案）、說明欄、標籤、揭露的答案。第一期只能看與複製；標題與說明要改的話，用「送到 YouTube」的表單改，它會重新送。
- 實測線：原始證據（題目、每一組的原始回答、評分）與查核報告，每個檔案附 SHA-256。
- 長片精華與漫劇：來源影片的連結與切出來的範圍。
- 品管 12 項的結果、審核紀錄、YouTube 同步面板（沿用 `YoutubeSyncPanel`）、放棄這支影片。

## 自動品管（成片）

`node tools/video/shorts/cli.mjs qa --dir <成片目錄>` 寫出 `qa.json`：`{ ok, final_sha256, kind: "shorts", line, items: [{ id, ok, detail }], inputs: { version: 1, files: { 檔案路徑: SHA256或null } } }`，`push` 把它放進成片審核的 `payload.qa`。

`check-audio` 的 `check.json` 同時綁定依序排列的 WAV（`audio_sha256`）和逐句原文（`phrases_sha256`）；`qa` 還核對 `results` 的順序、文字與每句結果。只改文字、句數不變，也要重查，不能沿用原音檔的舊通過結果。

`qa.inputs` 記錄本機的 `script.json`、`timeline.json`、`timing.json`（卡拉 OK 字幕的時間，沒有就記 `null`）、`check.json`、`verify.json`、`checks.json`、成片、逐句 WAV、五種支援語系的字幕與腳本列出的證據檔；缺檔記成 `null`，之後補檔也要重跑 QA。`qa` 在非同步檢查前後比對快照，途中改檔就拒絕寫入新結果。`push` 在任何後台寫入前及送出審核前重核；沒有綁定或任一輸入改變時，回報 `waits` 並停止。`package` 產出的 metadata、說明及 manifest 不列入 QA 輸入，仍走原有的上傳包檢查。

舊成片升級順序：先對目前版本重新查核並更新 `verify.json`，再跑 `check-audio --dir <成片目錄>` → `qa --dir <成片目錄>` → `package --dir <成片目錄>` → `push --dir <成片目錄>`（各指令前加 `node tools/video/shorts/cli.mjs`）。若旁白、字卡或時間軸改了，先依修改內容重建成片；只改說明也會使 QA 與事實查核失效。不可只補 hash、改 `ok`，或把舊收據重新包裝成通過；新跑出的失敗項仍照下方規則交站主處理。這份綁定記錄本機檔案的一致性，不替代重新查詢網站狀態或站主驗收。

後台的 Shorts 成片審核同時辨識 MP4 與完整 QA。更新 QA 後重新 `push`，即使 MP4 沒變，也會建立新審核 ID／版本；完全相同的重送仍回傳目前同一筆決定，包含站主對該版失敗 QA 的人工核准。待審 QA 改變也建立新 ID，舊頁面的核准操作會被拒絕。舊成片與上傳包審核標成 `superseded`，決定者、時間、備註與原收據保留，另寫入取代前狀態的稽核紀錄；已決定審核的附件也會保留。原本尚未上傳的指派／鎖定時段釋放，通過新成片審核後才重新送上傳包。

`push` 會比對後台回傳的完整 QA，再把該筆成片的 `final_review_id` 放進上傳包審核。後台拒絕缺少 ID、舊 ID 或尚未核准的 ID；上傳包的 metadata 雜湊相同，也不能沿用另一版成片的核准。升級時需同時更新 API 與 Shorts 工具；舊工具遇到 `video_shorts_final_review_stale` 時，更新工具並重新 `push`。遷移 `0115_video_review_revision` 讓舊紀錄成為版本 0；若已產生同檔案的多版審核，資料庫降版會拒絕刪去版本欄位，保護歷史紀錄。

重新送審支援尚未開始上傳的 Shorts。已有 YouTube 影片 ID、續傳工作、排隊或執行中的 API 同步，以及尚未結束或已取得影片 ID 的 VPS 工作，都會擋下更新；VPS 狀態無法確認也先停止。遇到 `video_shorts_review_upload_started` 或 VPS 錯誤，先到後台與 Studio 核對原工作；不可清掉上傳紀錄或刪除失敗項來冒用舊核准。這個流程不會撤回已上傳影片或 YouTube 上的公開排程。

| id | 檢查 | 來源 |
| --- | --- | --- |
| `profile` | 1080×1920、30 fps、H.264／AAC 48 kHz、長度在設定的範圍內、格數等於時間軸、影音差距不到一格 | `build` 的 `checks.json`，由 `qa` 用 ffprobe 重新量一次，不信任舊收據 |
| `loudness` | −14 ± 1 LUFS、真峰值 ≤ −0.8 dBTP | 同上 |
| `layout` | 內容與字幕都在安全區內、沒有超框、素材圖有載入 | `checks.json.layout` |
| `narration` | 每一句唸出來的跟稿子一樣 | 伺服器逐句轉寫加 Jev（`/video/speech/transcribe`、`/video/speech/judge`），跟長片同一套 |
| `evidence` | 實測線：每個證據檔都在、雜湊都對、字卡用到的素材都在證據清單裡。精華與漫劇：來源影片存在而且已公開（或已核准） | 腳本與伺服器的影片清單 |
| `facts` | 查核模型在新對話對照證據：字卡與旁白的每個數字和結論都對得上；沒有超出這次測試範圍的說法 | `verify.json` |
| `policy` | Jev：照頻道立場、有觀眾能照著做的東西、沒有投資醫療法律政治建議、沒有業配。精華（`cut`）不問「有觀眾能照著做的東西」：二、三十秒的片段放不下示範，示範留在它連回去的長片（站主 2026-09-30 決定） | 既有的 `POST /video/automation/judge/policy`；伺服器依影片的內容線選題組 |
| `metadata` | 標題 ≤ 100 字元、沒有角括號；說明 ≤ 5,000 位元組；標籤合計 ≤ 500 字元；話題標籤最多 3 個 | `package` |
| `captions` | `zh-TW.srt` 讀得懂、每段時間跟時間軸一致；有勾其他語言時每個語系都在而且沒過期。卡拉 OK 字幕的亮字時間還是估算的（`checks.json.captions.source` 是 `estimated`）時照樣過，但帶一條 `warnings`，後台卡片會列出；每一句都是伺服器量到的（`aligned`，`speech/align`）就沒有警告 | `package`、`checks.json.captions` |
| `links` | 說明欄每個網址都回 200；精華的完整影片連結是公開的 | 工人用固定的 User-Agent 抓 |
| `variety` | 開場那一句跟最近 30 支不重複；字卡結構跟同系列前一支不是一模一樣 | 伺服器的影片清單 |
| `disclosure` | 依內容線與素材決定要不要勾「變造或合成內容」，寫進 `metadata.json`；這一項只記答案，不會讓品管失敗 | 規則見「三條內容線」 |

**過關規則**（伺服器端，`shorts_qa_passed`，跟 `final_qa_passed` 同一個信任模型）：`qa.ok` 為真、`qa.final_sha256` 等於這份審核的雜湊、`kind` 是 `shorts`，而且伺服器自己列的必要項目（`SHORTS_QA_ITEMS`）每一項都在、都過。Shorts 設定的「品管全過就核准」開著時，審核在送達的當下核准，備註寫「Shorts 自動品管 12 項全過，依設定自動核准」，寫一筆 `video_review_auto_approved`。

**沒過的時候**：工人先自己修——`narration` 重錄或改寫被聽錯的句子、`layout` 交撰稿模型縮短那張字卡、`facts` 交撰稿模型照查核的意見改、`metadata` 重寫；每種最多 2 輪。還是不過才送審，摘要寫「Shorts 自動品管 2 項沒過：facts、layout」，進「需要你」。**這支 Shorts 不會擋住月曆**：它原本的時段改用片庫裡的下一支。

**上傳包**（`publish` 審核）沿用既有規則，項目換成 Shorts 的四項 `SHORTS_PACKAGE_ITEMS`：`files`（mp4、字幕、封面、`metadata.json`）、`descriptions`、`captions`、`disclosure`。

外部請求失敗（Jev、轉寫、抓網址）一律當作沒過，下一輪再試；不會因為判斷不了就核准。

## 排片與時段

- **開跑**：站主在 Shorts 設定選「第一支公開的日期」並按開跑，伺服器照節奏（`daily_pattern`）建出 90 天的時段。日期之後可以延後，已公開的時段不動。沒有開跑之前，做好的 Shorts 只進片庫。
- **每週排片**：每週一（或片庫低於 `stock_days` 時）工人拿到 `plan` 工作。企劃模型看題庫、各內容線的每週配額（預設實測 5、精華 2、漫劇 0）、上週已公開的每一支與 YouTube 回報的數字、預算狀態，把題目排進下一週的時段，並補新題目讓題庫至少夠兩週。伺服器檢查每個題目存在而且可以做、一格一題、配額沒超過，才寫進時段。某條線沒有來源（這週沒有新長片），它的配額讓給實測線。
- **選題比例**：沿用 #871 的滾動配額，每十支 6 支已驗證的題型、3 支新角度、1 支當週話題；沒有查得到來源的當週話題時，那一格改做有明確答案的觀眾挑戰。
- **製作順序**：片庫低於 `stock_days`（預設 5 天的量）時，工人每一輪先做 Shorts，再做漫劇與教學長片；庫存夠了就排在它們後面。一支 Shorts 的機器時間約 5–10 分鐘。
- **鎖定**：時段前 `lock_hours`（預設 24）小時鎖定那一格用哪一支。那一格排的題目還沒做好，就從片庫拿最早核准的一支（盡量同一條內容線）；片庫是空的，那一格記成「錯過」，寫進每週報告。連續 3 天錯過會進「需要你」。
- **一天最多幾支**：`max_per_day`（預設 2）。YouTube 官方說沒有最低發片頻率，這個節奏是製作管理的決定，四週後依數字調整（#871 的說法不變）。

## 上架

### 自動上架授權

YouTube 的開發人員政策對「代替使用者寫入」有三條要求（原文見「政策與依據」）：自動上傳必須有使用者**事前、具體、明示的同意**；寫入之前要講清楚會做什麼、會怎麼改瀏覽權限；使用者對發布出去的內容有**最後決定權**。全自動上架照這三條做成一個授權步驟：

- Shorts 設定有一張「自動上架授權」卡，列出網站會替站主做的每一件事：連結的是哪一個頻道、哪幾條內容線、一天最多幾支、時段、每支會設定的欄位（標題、說明、標籤、分類、字幕、兒童設定、合成內容揭露）、瀏覽權限會怎麼變（私人，到時段由 YouTube 公開）。站主按「我同意，開始自動上架」。
- 伺服器記下同意的人、時間、當時那段條文的 SHA-256，寫一筆 `video_shorts_autopublish_granted`。之後每一次自動送出的 audit log 都帶這筆授權的 id。
- 授權的範圍變了就失效、要重新同意：換頻道、加內容線、調高每天上限、改時段。授權 90 天到期（跟一輪排程一樣長），到期前 7 天進「需要你」。
- 設定存檔時檢查一次範圍，每一支送出之前再檢查一次：這一支的內容線、這一格在授權時區的時刻、這一天已經送出的支數，三樣都要在授權裡。月曆上的一格可以被拖到任何時間，一支 Shorts 也可能比授權早做好，所以只看設定不夠。範圍外的那一支網站不送，原因寫在那一格上，由站主自己從「可以上架」送。
- 別人給的時間網站不改：站主自己從卡片或在 Studio 排好的影片，就算時間跟那一格不一樣，網站也不會改成那一格的時間。
- 站主的最後決定權：排進時段的每一支在公開之前都能改標題與說明、換時段、抽掉；頂列的「暫停」立刻停止新的上傳與排程；「撤回已排程的」把還沒公開的影片在 YouTube 上取消排程（保持私人）。撤回會連同暫停一起做（不然下一輪又會排回去），按「繼續」之後那幾支重新送出；已經公開的不會動，每一支撤回了沒有都列出來。
- 網站永遠不會自己把影片設成公開：它只設私人加 `publishAt`，公開由 YouTube 在那個時間做（`HANDS-OFF.md` 的規則不變）；已經公開的影片網站不改。

沒有授權時，Shorts 照樣製作、品管、進片庫、排時段，只是不會送 YouTube；每一支在「可以上架」等站主自己按「送到 YouTube」，跟長片一樣。

### 稽核通過前：站主只拖檔案

1. 「等你上傳」列出接下來 `upload_ahead_days`（預設 10）天要上的 Shorts。站主按「下載這一批」拿到一個 zip，檔名是 `mokaair-short-<slug>.mp4`。
2. 在 YouTube Studio 把這些 mp4 一次拖進上傳視窗（官方說明：一次最多選 15 個，之後每支各自在草稿編輯器裡完成），瀏覽權限選私人，其他欄位都不用填，也不用改檔名帶出來的標題。
3. 回到分頁按「我上傳好了」。網站讀頻道最近上傳的影片，用上傳檔名（`fileDetails.fileName`，只有頻道擁有者讀得到；讀不到時用 Studio 從檔名帶出的標題）對回每一支 Shorts，再核對長度與尺寸。對到的寫下影片 id，送出 `videos.update`（標題、說明、標籤、分類、揭露、私人加 `publishAt`）與 `captions.insert`。
4. 對不到的、長度不符的、已經公開的，列在「需要你」，可以改用貼網址（既有的表單）。
5. 時段到了還沒上傳的那一支回到片庫，時段記成錯過。

站主每週大約做一次。要花多久取決於一件還沒實測的事：停在草稿、沒有按完精靈的影片，API 讀不讀得到。讀得到的話就是拖檔案加按一個鈕；讀不到的話每支要在 Studio 多按幾下存成私人，一批十支大約五分鐘。試作票會測出來。

### 稽核通過後：網站自己上傳

設定分頁的「YouTube API 稽核已通過」勾起來之後，鎖定時段的那一刻網站用 `videos.insert`（續傳上傳）上傳 mp4，同時帶私人與 `publishAt`，接著送字幕。站主不用做任何事。上傳用的是自己的配額桶（每天 100 次），其餘呼叫一支約 500 單位（`videos.update` 50、一條字幕 400、讀取數次），一天兩支遠低於每日 10,000 單位。

### 誰在什麼時候動手

審核檔案區只掛在 API 容器，OAuth 權杖也只在那裡，所以送 YouTube 的工作跑在 API 行程（沿用 `app/video_youtube/sync.py` 的 `run_sync`，連同它的租約、續傳與重試）。影片這一塊在 API 沒有背景排程（媒體工作靠輪詢推進、預覽清理掛在讀清單的請求上），時間到了由工人來敲門：工人的迴圈腳本（`ops/video/worker.sh`）在 `auto` 旁邊另開一個背景迴圈，照自己的計時每 5 分鐘（`VIDEO_SHORTS_KNOCK_SECONDS`，預設 300 秒）跑一次 `shorts/cli.mjs tick`，也就是呼叫 `POST /video/automation/shorts/tick`。它不等 `auto` 的一輪跑完（一輪可能跑上快一小時），也不看「自動產線有沒有開」，所以教學影片的自動草稿關著時 Shorts 的排程照走；工作區裡有 `STOP` 檔時它就暫停敲門，刪掉後下一次恢復（見 [AUTOMATION.md](AUTOMATION.md)）。伺服器在這個請求裡照順序做到期的事——把已經排上 YouTube 的那幾格標成已排程、鎖定時段、啟動該送的同步、讀該讀的成效、檢查授權——並記下這次敲門的時間（先標記再鎖定：工人停了一陣子再回來時，已經排上去的那一格不會被當成錯過）；頂列顯示「工人上次回報」，超過 15 分鐘沒有回報就進「需要你」。`tick` 只回做了幾件事，不回任何權杖或影片內容；工人的權杖本來就能送審，這裡沒有擴大它能做的事。

站主按的「送到 YouTube」記在 audit log 的是站主本人；自動送出的那幾筆，操作者記成授權的那一位，metadata 帶 `auto: true` 與授權的 id（欄位名稱不要含 `token`、`secret`，audit 面板會把那些鍵濾掉）。

### Shorts 和長片送出去的東西不一樣

| 欄位 | 長片 | Shorts |
| --- | --- | --- |
| 標題與說明 | 五語系 | 先只有 zh-TW；Shorts 設定的「語言」勾了才加其他語系的標題、說明與 CC（畫面上的字與旁白仍是繁中） |
| 章節 | 有 | 沒有 |
| 字幕 | 五條 CC，不燒錄 | 字卡式的字幕本來就在畫面上，另外上傳一條 zh-TW CC 給關掉聲音與需要輔助的觀眾 |
| 縮圖 | `thumbnails.set` | 不送。第一格就是封面（開場的鉤子）。Shorts 的自訂縮圖 2026-07 才開放，只能在電腦版 Studio 設，而且先開放給營利計畫的頻道；`thumbnails.set` 對 Shorts 有沒有用，官方沒寫 |
| 相關影片 | — | 精華與漫劇要連回完整影片。Shorts 的「相關影片」只能在 Studio 設（要進階功能），影片資源沒有這個欄位，API 寫不了。所以連結一律放說明欄第一行；要不要另外在 Studio 補相關影片，由站主決定，每週報告會列出還沒補的 |
| 標題測試 | 可以在 Studio 做 A/B | 官方明說 Shorts 不能做 A/B 測試；兩個標題只是備案 |
| 分類 | 28 | 依內容線：28 或 24 |
| 話題標籤 | 三個 | 最多三個，不強制 `#Shorts` |

## 成效與每週報告

**數字照 YouTube 給的顯示，判斷用文字寫，不算分數。** YouTube 的開發人員政策原則上不准 API 用戶端拿 API 的數字去算新的或衍生的指標（政策舉的例子就是「把喜歡數、觀看數合成一個分數」）。2026-06-01 起有一個例外：稽核時把用途選成「Analytics & Reporting」並接受政策的增修條款的開發者，可以算特定的衍生指標（平均、加總、比率、自訂分數、排行），條件是跟 YouTube 的原值分開標示；統計數字也可以存到 36 個月。在拿到這個例外之前：

- 成效區顯示的每個數字都是 YouTube 回傳的原值，旁邊寫來源（Data API 或 Analytics API）與讀取時間。不顯示自己算的分數、排名、中位數或達成率。
- 每週報告由企劃模型寫：它讀到的是這張原值的表，寫出來的是編輯決定（下週哪個系列多做、哪個換開場、哪個先停）與理由，理由引用原值。提示詞明寫不要輸出任何自己算的指標。
- #871 的判定規則（同系列至少五支、各滿七天、觀看超過同期中位數兩倍就擴大……）保留成企劃模型的**判斷準則**，寫在提示詞裡；伺服器不拿 API 的數字去跑這套算式。
- 想要照 #871 的算式出一份數字報告時，站主從 Studio 匯出（那是站主自己的資料，不是 API 資料），照舊用本機的 `report`；或之後在分頁上傳匯出檔（第三期）。「選擇觀看、還是滑走」這個數字 API 沒有提供，只有 Studio 有。

稽核申請書（O1）會把「Analytics & Reporting」一起選進用途。通過之後，伺服器才可以拿 API 的數字跑 #871 的算式，畫面上標明「本站自己算的，不是 YouTube 的數字」。

**兩種觀看數不要混著看**：公開的觀看數（`viewCount`）從 2025-03-31 起對 Shorts 是每一次開始播放與重播都算，2026-08-24 起所有格式都從第一格開始算；營利資格與 Shorts 分潤看的是另一個比較小的數字，官方現在叫「合格的 Shorts 觀看」（qualified Shorts views，也就是 engaged views）。第一期讀得到的只有前者。

**讀什麼、什麼時候讀**：

| 期 | 來源 | 數字 | 要站主做什麼 |
| --- | --- | --- | --- |
| 第一期 | Data API `videos.list` 的 `statistics`（一次最多 50 支、1 單位；2026-06 新增的 `videos.batchGetStats` 有自己的配額桶，實作時擇一） | 公開的觀看、喜歡、留言 | 不用：現有的授權就讀得到 |
| 第三期 | YouTube Analytics API：`filters=video==<id>` 加日期區間；分辨 Shorts 用維度 `creatorContentType`（官方只把它列為維度，沒有列為篩選條件，所以取回來再留 `SHORTS` 那幾列） | 加上 engaged views、平均觀看百分比、平均觀看時間、分享、新增訂閱 | 重新按一次允許（多一個唯讀的 scope `yt-analytics.readonly`；既有的權杖不會自己多出這個 scope），稽核申請書要寫到 |

快照的時間窗沿用 #871：公開後滿 24 小時未滿 48 小時讀到的第一筆是「第 1 天」，滿 72 未滿 96 是「第 3 天」，滿 7 天到 9 天是「第 7 天」。每個時間窗只存第一筆、之後不覆寫；沒有在時間窗內讀到就留白，不用後來的累積數字回填。Analytics API 的資料以太平洋時間的「日」為單位、約晚兩到三天，所以它的三個時間窗是「公開日起算第 1、1–3、1–7 天」的區間報表，資料齊了才讀。

政策允許經授權取得的統計數字長期保存，但每 30 天要確認授權還在、影片沒有被刪。`tick` 每天做一次：授權失效就停止讀取並進「需要你」；影片被刪或改成私人，那一支標成「已下架」，不再算進任何清單（已經讀到的數字留著；它排的那一格如果還沒公開過，記成錯過）。「最新」那一筆在公開後的四個月每天更新，之後每 25 天一次，所以舊的 Shorts 也在 30 天內被確認過。站主在 Studio 把公開時間往後改的影片不算下架：以 YouTube 上的時間為準，等它公開再開始讀。

第一期用 `videos.list`（一次最多 50 支、1 單位）：同一次呼叫連 `status` 一起讀，才知道公開了沒有、下架了沒有；120 支一天三次呼叫。一天的配額用到八成（8,000 單位）時先停的是讀數字，送 Shorts 不停；被 YouTube 以配額拒絕之後，當天（太平洋時間）不再呼叫。

**90 天目標**：#871 的挑戰目標（首支公開起 90 天、累積 1,000 萬公開觀看）放在頂列，旁邊是 YouTube 回報的頻道 Shorts 觀看數。它是實驗目標，不是營利資格的核算，也不是保證。

這個數字跟營利計畫的門檻長得很像，但不是同一件事，站主排時程時要知道（2026-09-28 讀官方說明）：

| | 現在 | 2027-02-01 起 |
| --- | --- | --- |
| 新頻道加入營利計畫（廣告分潤） | 1,000 位訂閱，加上過去 90 天 1,000 萬次**合格的** Shorts 觀看（或過去 12 個月 4,000 小時合格的觀看時數） | 1,000 位訂閱，加上過去 90 天 **2,000 萬次**合格的 Shorts 觀看（或過去 365 天 8,000 小時）。已經在計畫裡的頻道不受影響 |
| 每個月從 Shorts 分潤池領錢 | 在計畫裡就有 | 過去 90 天要維持 1,000 萬次合格的 Shorts 觀看；沒達到不會被移出計畫，也不影響長片的收益 |
| 粉絲贊助那一級（會員、超級留言、購物） | 500 位訂閱、90 天內 3 支公開影片，加上 90 天 300 萬次合格的 Shorts 觀看（或 12 個月 3,000 小時） | 不變 |

合格的 Shorts 觀看只算公開的 Shorts 在 Shorts 動態裡的 engaged views，比公開的觀看數小。也就是說：想用現行的 1,000 萬門檻申請，要在 2027-01-31 之前達標並送出申請；10 月初開跑的話，90 天剛好落在 1 月初。

## 花費與預算

- 自動記帳：伺服器今天只有漫劇的媒體工作記得到每支影片的花費（`video_media_jobs.usd_estimate`）；旁白字數、轉寫、Jev 都是不分影片的月計數或日計數，`/video/speech` 連影片代號都不收。所以旁白與模型呼叫的用量由工具在送審時自己回報（`payload.usage`：旁白秒數與字數、各階段的呼叫次數與 token），伺服器照回報寫進 `video_shorts_costs`；圖片、片段、音樂則從媒體工作的紀錄抄過來。送出生成請求時先記一筆 `reserved`，成功改 `confirmed`，失敗刪掉。
- 旁白的金額是照廠商價目估的：Gemini 的語音每秒 25 個輸出 token，`gemini-3.8-flash-tts` 每百萬 token US$9（2027-01-01 起 US$18），`gemini-3.8-flash-lite-tts` US$6（之後 US$12）；40 秒的旁白約 US$0.009。價目是 2026-09-28 讀 ai.google.dev/gemini-api/docs/pricing 的，寫在 `app/video_shorts/costs.py`；價目裡沒有的聲音記成 `unknown`。本機語音（試片用的 Windows 語音）記 0。
- 模型呼叫走訂閱帳號的記 0、附次數；走計費 API 的記成 `unknown`，等站主補金額。
- 手動補帳：新訂閱、工具費。廠商沒回報金額的填 `unknown`，不能填 0。
- 幣別：原幣與當天匯率一起存，報表用新台幣。匯率服務沒有回應時用帳上最近一次的匯率，再沒有就用備用匯率（美元 32），並在那一筆的備註寫明。
- 上限（預設沿用 #871，站主可改）：每 30 天 NT$3,000；到 NT$2,400 停止開新的付費工作，保留 NT$600 做完手上的；90 天 NT$9,000。有 `unknown` 的帳時，付費工作一律先停。預留的金額算在已花的裡面。
- 「每 30 天」從開跑日起算，一輪三期；還沒開跑時看的是到今天為止的 30 天與 90 天。
- 走訂閱帳號的模型呼叫不算新增花費，但每週報告會列用了幾次。
- 超過上限時工人停在目前的步驟，分頁寫原因；不會悄悄換成較便宜的模型。不用錢的工作（文字題的實測、長片精華）照常做。

## 資料模型

第一期的表在遷移 `0109_video_shorts`（A1）；題庫、素材、每週報告的表在 A3 自己的遷移。一律「不存在才建」，CHECK 的重建照 `0101`、`0106` 的做法。

`video_projects` 的新欄位：

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| `format` 的 CHECK | 重建成 `format IN ('slides', 'drama', 'shorts')` | `shorts` 是字卡式 Shorts 的產線；用這個格式回報的影片一定要帶 `shorts_line` |
| `shorts_line` | String(8)，可空；CHECK `lab`、`cut`、`drama` | 不是空的就是一支 Shorts |
| `shorts_series` | String(40)，可空 | 系列 |
| `source_slug` | String(80)，可空 | 精華與漫劇短篇的來源影片 |
| `youtube_removed_at` | 時間，可空 | 每 30 天的驗證發現影片被刪或改回私人的時間（Y1 寫入）；之後不再讀它的數字 |

新表：

| 表 | 欄位 |
| --- | --- |
| `video_shorts_settings`（一列，id 1） | `enabled`、`lines`、`weekly_quota`、`campaign_start`、`daily_pattern`、`slot_times`、`timezone`、`stock_days`、`lock_hours`、`upload_ahead_days`、`max_per_day`、`seconds_min`／`seconds_max`、`voice`、`stage_models`、`subject_models`、`stage_instructions`、`locales`、`auto_approve`、`autopublish`、`paused_at`、`consent_id`／`consent_at`／`consent_by_user_id`／`consent_text_sha256`／`consent_expires_at`／`consent_scope`、`budget_ntd_30d`、`budget_soft_ntd`、`budget_total_ntd`、`made_for_kids`、`last_tick_at`／`last_tick`（工人上次敲門的時間與那一輪做了什麼）。獨立一張表，不加進 `video_automation_settings`：各格式的設定各自儲存是站主 2026-09-27 的要求 |
| `video_shorts_slots` | `id`、`starts_at`（唯一）、`phase`、`line`、`series`、`topic_slug`、`project_slug`（可空）、`status`（`open`、`planned`、`assigned`、`locked`、`scheduled`、`published`、`missed`、`skipped`）、`locked_at`、`note`。一支 Shorts 同時只佔一格：`project_slug` 的唯一索引只算狀態不是 `missed`、`skipped` 的列，錯過的那一格留著當時排的代號當紀錄 |
| `video_shorts_topics` | `slug`（唯一）、`line`、`series`、`title`、`hook`、`status`（`idea`、`ready`、`needs_assets`、`making`、`made`、`dropped`）、`brief`（JSON：測試規格、真值核對、完成條件、旁白大綱、標題備案、來源）、`source_slug`、`origin`（`campaign`、`planner`、`owner`、`auto`）、`release_order`、`assets_needed` |
| `video_shorts_assets` | 站主上傳的素材：`topic_slug`、`sha256`、`filename`、`content_type`、`size`、`author`、`taken_on`、`rights_note`、`uploaded_by_user_id`。檔案放媒體庫 |
| `video_shorts_metrics` | `project_slug`、`youtube_video_id`、`period`（時間窗：`d1`、`d3`、`d7`、`now`；`window` 是 PostgreSQL 的保留字，所以欄位不叫那個名字）、`source`（`data_api`、`analytics_api`、`studio_export`）、`captured_at`、`range_start`／`range_end`、`views`、`engaged_views`、`likes`、`comments`、`shares`、`subscribers_gained`、`avg_view_seconds`、`avg_view_percent`、`stayed_percent`、`raw`。`(youtube_video_id, source, period)` 唯一；`d1`、`d3`、`d7` 寫了就不改，`now` 原地更新 |
| `video_shorts_costs` | `occurred_at`、`project_slug`、`category`、`amount`、`currency`、`fx_rate`、`amount_ntd`、`status`（`confirmed`、`reserved`、`unknown`）、`source`（`auto`、`manual`）、`units`（工具回報的用量：秒數、字數、次數）、`note`、`dedupe_key`（唯一、可空：自動記的帳用它認出同一筆，例如 `usage:<slug>:<成片雜湊前 16 碼>:narration`）。`unknown` 的列沒有金額，其他狀態一定有，由 CHECK 保證 |
| `video_shorts_reports` | `week_start`（唯一）、`body_md`、`rows`（報告引用的原值）、`plan`（下週排片）、`model`、`generated_at` |

審核關卡不加新的：Shorts 用既有的 `final` 與 `publish`。`ProjectIn`、`ProjectSummary` 多 `shorts_line`、`shorts_series`、`source_slug`、`shorts_state`、`slot_at`。

兩個一定要一起處理的地方：

- **格式寫在四個地方**：`ck_video_project_format`、`VideoFormat`（`video_reviews/schemas.py`）、`PromptFormat`（`video_automation/schemas.py`）與 `ck_video_stage_prompt_format`，外加清單的 `format` 查詢參數。前兩個與查詢參數在 A1 放寬；提示詞那兩個在 A3（工人開始替 Shorts 跑模型階段時）。
- **清單上限 200 支**：`list_projects` 只回最新的 200 支，後台清單與工人讀的 `GET /video/automation/videos` 都是它。90 天 120 支 Shorts 加進來，教學影片與漫劇會被擠出清單。A1 加篩選 `shorts=only|exclude`（後台與工人兩個端點都收），「影片」與漫劇分頁、工人原本的迴圈一律帶 `exclude`，Shorts 分頁與 `shortsStep()` 帶 `only`；Shorts 自己的清單另外依狀態分頁讀取，已公開的只回最近 60 支，更早的從成效區看。

## 端點

後台路徑不需要四語錯誤；`AppError` 只出現在檔名帶 `admin` 的路由檔（`admin_api.py`、`admin_publish_api.py`、`admin_automation_api.py`，`tests/test_error_localization.py` 靠檔名分辨），模組丟 `ShortsRefused`。三個路由檔都已經掛進 `main.py`：A1 的端點在 `admin_api.py`，Y1 加在 `admin_publish_api.py`，A3 加在 `admin_automation_api.py`。

| 誰 | 端點 | 做什麼 |
| --- | --- | --- |
| 後台（content.read） | `GET /admin/video-shorts/overview` | 頂列：授權與暫停、今明兩天的時段、庫存天數、本期花費、頻道連結、工人上次回報、需要你的每一項 |
| 後台（content.read） | `GET /admin/video-shorts/slots?from=&to=` | 月曆（兩個日期是設定時區的當地日期，都含；不帶就是整輪） |
| 後台（content.manage） | `PATCH /admin/video-shorts/slots/{id}` | 一次一個動作（`action`）：`move` 換時段、`assign` 指定影片、`clear` 抽掉、`skip` 標成不發、`reopen` 重新開啟、`note` 寫備註 |
| 後台（content.read） | `GET /admin/video-shorts/metrics`、`…/costs`、`…/reports`、`…/topics` | 成效、花費帳、每週報告、題庫 |
| 後台（content.manage） | `POST /admin/video-shorts/costs`、`PATCH`／`DELETE …/costs/{id}` | 補一筆、改一筆（替 `unknown` 補上金額）、刪掉自己補錯的；自動記的帳不能刪，預留的不能改 |
| 後台（content.manage） | `POST …/topics`、`PATCH …/topics/{slug}`、`POST …/topics/{slug}/assets`、`POST …/topics/{slug}/assets/finish` | 新增想法、改題目、上傳素材：每一段 4 MiB 的原始位元組，網址只帶 `sha256`、`part`、`parts`、`size`、`need`；傳完再用 `finish` 的 JSON 送檔名、拍攝者、拍攝日期、授權說明（人名不進網址，所以不進 access log 和瀏覽器歷史） |
| 後台（content.read） | `GET /admin/video-shorts/uploads` | 等你上傳：接下來 `upload_ahead_days` 天排了時段、YouTube 上還沒有影片的 Shorts，每一支的檔名、大小、長度、時段 |
| 後台（content.manage） | `GET /admin/video-shorts/uploads/batch.zip`、`POST …/uploads/claim` | 下載這一批、我上傳好了（回每一支的結果：`matched`、`duplicate`、`not_found`、`not_private`、`length_differs`） |
| 後台（settings.manage） | `GET`／`PUT /admin/video-shorts/settings`、`POST …/campaign/start` | 設定、開跑 |
| 後台（settings.manage） | `POST`／`DELETE /admin/video-shorts/autopublish` | 授權、撤銷 |
| 後台（content.manage） | `POST /admin/video-shorts/pause`、`…/resume`、`…/recall` | 暫停、繼續、撤回已排程的 |
| 工具與工人（VideoTool） | `GET /video/automation/shorts/settings` | Shorts 的聲音、長度範圍、語言、有沒有暫停；不含授權 |
| 工具與工人 | `GET /video/automation/videos?shorts=only\|exclude` | 影片清單。原本的迴圈帶 `exclude`，Shorts 的那一輪帶 `only`（可再帶 `state=`、`limit=`、`before=`）；後台的 `GET /admin/videos` 收同樣的參數 |
| 工人 | `POST /video/automation/shorts/tick` | 做到期的事，回做了幾件 |
| 工人 | `GET /video/automation/shorts/next` | 下一件工作：`plan`、`brief`、`make`（帶題目、內容線、脈絡）、`report`，或沒有 |
| 工人 | `POST …/shorts/plan`、`…/shorts/topics`、`…/shorts/{slug}/start`、`…/shorts/{slug}/done`、`…/shorts/report` | 寫回排片、新題目、開始、完成、每週報告 |
| 工人 | 既有的 `/video/reviews/*`、`/video/speech/*`、`/video/automation/run`、`/video/automation/judge/policy` | 送審、旁白與檢查、模型階段、政策判斷 |
| 工具與工人（VideoTool） | `POST /video/speech/align` | 一句旁白每個字什麼時候唸到（`app/video_speech/align_api.py`）：送 `speech`（跟 `/video/speech` 一樣的合成請求，Azure 聲音）就在**同一次**合成裡拿回音檔（base64）與 Azure 的 WordBoundary，預算、allowlist、錯誤碼與計費字數都跟語音路由一樣，不會付兩次；送 `audio`＋`text`（任何音檔）交伺服器的 CPU 對齊器——目前沒有裝（量過的數字見 §工具端），回 503 `video_align_unavailable`，工具保留估算。Gemini 聲音沒有字時，送 `speech` 會回 422 `video_align_voice_unsupported`。每個權杖每小時 1,200 次 |

`/video/automation/run` 的階段名稱不加新的，Shorts 的提示詞送在 `planner`、`writer`、`verifier` 底下，用 `variant` 分開（`shorts-plan`、`shorts-brief`、`shorts-lab`、`shorts-cut`、`shorts-drama`、`shorts-report`）。實測線的受測模型是唯一的新階段 `subject`，`variant` 是 `a` 或 `b`：哪一個模型由 Shorts 設定的 `subject_models` 決定，工人不能指定；伺服器回傳實際用的模型名稱，工人原樣寫進證據。

## 工具端

`tools/video/shorts` 留著自己的腳本格式（一支 Shorts 一份 JSON、一句一張字卡），不併進 `video.json`：它小、已經過審查、不碰共用的核心檔。主產線的規則也套不上 25–55 秒的影片：少於 3 個章節是 lint 錯誤、每章至少 10 秒、長度以分鐘計、縮圖要 1280×720、畫面寫死 1920×1080。

今天它是一支獨立的指令：不在主指令 `tools/video/cli.mjs` 的清單裡、不發任何網路請求、旁白只能在 Windows 上合成（工人的映像是 Linux，`build` 沒有 `--audio-dir` 會直接失敗）。要加的東西：

| 指令或模組 | 做什麼 |
| --- | --- |
| 腳本格式第 2 版 | 多 `line`、`source`（精華與漫劇的來源與範圍）、`hashtags`、`links`；`evidence` 只有實測線必填；`series` 不再寫死三個值，改成依 `line` 檢查。第 1 版的三支試片照舊讀得懂 |
| `build --speech server` | 旁白經伺服器合成（既有的 `/video/speech`，頻道聲音與 style 來自 Shorts 設定），逐句快取；`windows` 與 `--audio-dir` 兩種來源保留 |
| `check-audio` | 每一句送轉寫與 Jev，被標的句子重錄，最多照設定的輪數 |
| `qa` | 上面的 12 項，寫 `qa.json` |
| `package` | 寫 `metadata.json`（標題、兩個備案、說明、標籤、分類、兒童設定、揭露、`final_sha256`、`line`、`series`、`source`）與上傳包檢查 |
| `push` | 在站上建立或更新這支影片（`format: "shorts"`、`shorts_line`），分段上傳檔案，送 `final` 與 `publish` 兩筆審核。本機與工人用同一個指令；本機用配對好的工具權杖 |
| `import --from <目錄>` | 把別的工具做好的 Shorts（mp4、srt、一份最小的 `meta.json`）包成同一種上傳包再 `push`。品管一樣要重跑，不信任外來的檢查結果 |
| `motion.mjs`（2026-09-29，票 `video-shorts-motion-music`） | 畫面不再是每句一張不透明字卡硬切：**一個場景一段**，底層是這個場景的圖（長片的關鍵影格，16:9 裁成 9:16 只留中間約 32%，依 `camera` 運鏡：push in／pull out／pan left／pan right／tilt up／tilt down／drift）或主題的底色與光暈（純字卡場景，慢慢漂移），上層是每句的**透明字卡**（`sceneHtml` 的 `transparent`：有圖時內容放在半透明面板上、上下加漸層遮罩；`.content`、字幕條、計數與進度條的幾何不變，`measurePage` 與 qa 的 layout 項照舊）；場景之間從上一段的最後一格溶接 15 格，第一個場景硬切。運鏡表達式與溶接長度直接 import `assemble/drama.mjs`，跟長片一致。`checks.json` 多 `motion`（每景的 camera、背景種類、有沒有溶接）。實測線的證據圖（`asset` 沒有 `camera`）仍放在卡片裡，清楚可讀，底下是漂移的底色 |
| 腳本格式第 2 版的 `camera`、`music`、`sfx` | 場景可寫 `camera`（上面七個詞）；文件層可寫 `music {track, sha256?, gain_db?, duck_db?}` 與 `sfx {set, gain_db?}`，都是站主放在工人主機 `<VIDEO_WORKDIR>/_music/`、`_sfx/<set>/` 的授權檔（跟長片同一份，`docs/videos/ILLUSTRATED.md` §配樂與音效），Shorts 不生成音樂。有配樂或音效時 `build` 走長片的 `measureMixArgs`／`mixArgs`（床壓在旁白下、側鏈壓低、成片 −14 LUFS、床 ≤ −24 LUFS 否則失敗），音效依 `shortSfxPlan` 放：每個場景開頭一個 stamp（第一景除外）、有 `big` 的句子一個 pop、1.5 秒內不重複。`buildId` 加配樂 sha 與音效組雜湊；`checks.json` 多 `music {track, sha256, bed_lufs}`、`sfx {set, events}`。第 1 版腳本一個位元組都不用改 |
| `karaoke.mjs`（2026-10-05，票 `2026-10-05-shorts-karaoke-captions-estimated-timing`） | 字幕條可以**逐組亮字**（`build --captions karaoke`，沒給旗標就讀 `VIDEO_SHORTS_CAPTIONS`，再沒有就是 `plain`，舊行為一個位元組不變）：每句先切成最多兩行、一行 ≤ 15 個全形字（820 px 盒的真正上限，38 字只是格式上限），每行再切成 5–10 個顯示單位一組（拉丁字與數字不拆、標點黏前一個字、偏好在句讀收尾）；字幕層是獨立的透明 PNG（`captionHtml`，只畫字幕條、裁到 `CAPTION_BOX` 80,1430,820×165），一個亮字狀態一張，疊在卡片上（`segmentArgs` 的最後一個輸入，`overlay=80:1430`），卡片本身把字隱藏但保留盒與底色，所以 `measurePage` 的量法不變；亮組只換顏色（主題的 `highlight`，或 `colors.karaoke`）與光暈，不換版面。時間是**估算**的：伺服器只回音檔，`speechSpan` 先用每句音檔的 RMS 找到頭尾靜音，再依 `spokenUnits` 加標點的權重分攤；寫在成品的 `timing.json`（`source: "estimated"`，每句的 lines、groups、start／end、states），`checks.json.captions = {style, source, groups, states, version}`。CC 的 `zh-TW.srt` 仍一句一段（YouTube CC 沒有逐字）。`MOTION_VERSION` 升到 v2、`karaoke.mjs` 進 `codeHash`、`captions` 進 `buildId`。伺服器的字幕樣式設定延後（要 migration、schemas、後台表單與五個 admin.json）；站主先看一支樣片，滿意再在工人主機設 `VIDEO_SHORTS_CAPTIONS=karaoke`。真實字時由下一列的 `speech/align` 補（同一個 `timing.json` 形狀，`source: "aligned"`） |
| `speech/align`（2026-10-05，票 `2026-10-05-speech-align-character-timing`） | 伺服器量字時，工具照量到的亮字。**API**：`app/video_speech/align.py`＋`align_api.py`（自己的 router，掛在 `video_speech_router` 旁邊；端點表見 §端點）。Azure 聲音走 Speech SDK（`azure-cognitiveservices-speech`，裝起來 9 MB、import 後 36 MB RSS，核心函式庫只連 libstdc++ 與 libuuid，slim 映像不用加套件；只有裝置音訊的擴充才連 ALSA，記憶體內合成從不載入），在同一次合成裡收 `WordBoundary`／`PunctuationBoundary` 事件：Azure 一個「詞」常是兩三個中文字，時間平均分給每個字（一字一音節）；詞典的詞（`<sub alias>`）整個詞取它被唸成的那幾個字的時間；Azure 沒給的字（例如沒報的標點）取左右鄰居之間的空檔。**工具端**：`tts/client.mjs` 的 `synthesizeAligned`（Azure 聲音，付費，跟 `synthesize` 一樣的 SPEECH_UNCERTAIN 規則）與 `alignClip`（任何音檔，不付費；伺服器回 `video_align_unavailable`／`video_align_voice_unsupported` 或舊站的 404 時回 `null`，一次就停）；`shorts/speech.mjs` 把字時存在 `.speech-server/<key>.timing.json`，跟 WAV 同一把 key；沒拿到的只有 `--captions karaoke` 的 build 會再問一次（不付費），`plain` 的 build 不問，只用快取裡已有的；`karaoke.mjs` 的 `alignedGroupTimes` 讓每一組從它第一個字被唸到的時刻亮起（第一組仍從語音段開頭、最後一組仍到語音段結尾，組不會倒退），字時拼不出這句（別的斷詞、別的文字）就保留那句的估算。`timing.json` 的 `source` 只有**每一句**都量到才是 `"aligned"`，否則仍是 `"estimated"`；量到的句子各帶 `aligned: {source: "azure"|"aligned", model}`，`checks.json.captions` 多 `aligned`（量到幾句；零句時不寫，估算的輸出一個位元組不變）。`qa` 的 `captions` 警告只在 `estimated` 時出現。**Gemini 聲音目前仍是估算**：量過的 CPU 對齊器（4 核機器、2026-10-05）——Qwen3-ForcedAligner 與 WhisperX 的 wav2vec2 都要 torch，API 映像裝不下；`sherpa-onnx` 1.13.8 的 wheel 4.4 MB（裝起來 38 MB、import 27 MB RSS），中文 zipformer-14M int8 模型 25 MB、載入 0.6 s、126 MB RSS、一段 3 秒音檔單執行緒 55 ms，小 Paraformer-zh 78 MB、完整 Paraformer-zh int8 約 230 MB；但這裡沒有語音可對、沒有 Azure 可比，transducer 的 token 時間是發射時間（晚於起音），而且 Dockerfile 不在票的範圍，模型得在容器啟動後下載，所以沒有上線：`align.load_aligner()` 回 `None`，端點回 503，接手的票在那個 hook 後面裝模型即可，合約與工具端都不用再動 |
| `from-drama.mjs`（2026-10-05，票 `2026-10-05-shorts-from-drama-reframe`） | 漫劇直式短篇的**後製路線**：`from-drama --slug <集> --from <秒> --to <秒>` 讀該集已核准的 `final.mp4`（`approvals.json` 的 `final` 要對得上目前的雜湊，否則拒絕）、`timeline.json`（成片有片頭片尾時依 `checks.json.branding` 位移，跟字幕同一個時鐘）與 `captions/zh-TW.srt`，把 1920×1080 的畫面**按格數**（`trim=start_frame`，不 seek）切出這一段；每個 shot 問一次 `POST /video/media/locate`（工作目錄有 `keyframes/manifest.json` 就用該鏡的關鍵影格，沒有就從成片抽鏡頭中段那一格，都先 `putFile` 進該集的媒體庫；標籤是 `video.json` 裡該鏡的角色名，主角在前），取第一個對上的角色、否則分數最高的方框、都沒有就置中；`crop=608:1080:x='…'` 的視窗置中在方框上、整鏡不動、換鏡前 `MOVE_FRAMES`（15 格，等於溶接長度）線性移到下一鏡的位置，讓剪接點落在已經對好的構圖上；卡片場景（片頭、章節、片尾）置中，不問；再 `scale=1080:1920`。聲音是該集混音剪下來的這一段，兩段式 loudnorm 到 −14 LUFS，不合成旁白。字幕不用 libass：每句用 `core.mjs` 的 `captionHtml`（多加一條主題字幕條底色的規則，版面不動）畫成字幕層 PNG，`--captions karaoke` 時依 `karaoke.mjs` 估的時間逐組亮字、`plain` 時整句不亮，連同沒人說話時的空白圖用 ffconcat 清單疊在 `CAPTION_BOX`（跟 `motion.mjs` 疊卡片的做法相同）；每句都量過安全區（字幕條下緣 ≤ 1600、字在 x 78–902），超過兩行 15 字的句子會停下來說是哪一句。產物跟 `build` 一樣：`script.json`（`line: "drama"`、`source.slug` 與起訖秒數、標題說明預設抄 `video.json` 的 `youtube`，`--meta` 可改標題、說明、系列、標籤、連結、每景標題）、`audio/`（每句一個 WAV，給 `check-audio`）、`timeline.json`、`timing.json`、`checks.json`（`layout` 有量，另有 `reframe`：每鏡的圖片來源、方框、視窗、`pieces` 與 locate 次數）、`upload/`；之後 `check-audio`、`qa`（`layout` 能過）、`package`、`push` 照常。`usage.json` 不報 locate：站上已經記在 judge 的額度，而 `costs.py` 會把計費供應商的階段呼叫記成未知金額。`--from`／`--to` 切到句子一半、長度不在 Shorts 範圍、來源沒核准，都在任何呼叫之前拒絕並說怎麼改。原生 9:16 路線（T4）仍是另一條；這條不生圖、不重畫 |
| `from-episode` 接任何有 shot 的長片 | 原來如此事務所的漫劇與插圖投影片影片都行：`episodeShort` 把每個 shot 換成長片的關鍵影格（雜湊綁定，不另外生圖），並帶上長片那個 shot 的 `camera`（Short 自己寫了就用自己的）；系列依長片決定（`episodeSeries`）：explainer → `sothatswhy`、插圖投影片 → `illustrated`（主題 `cut:illustrated`，深青、奶油白、琥珀，每張卡指回長片）；沒有 shot 的長片直接拒絕 |
| `tools/video/automation/shorts.mjs` | 工人的 `shortsStep()`：依 `next` 做 `plan`、`brief`、`make`、`report`。`make` 依內容線走 `lab.mjs`、`cut.mjs`、`vertical.mjs`（漫劇）。`auto` 現在一讀到自動產線沒開就結束；`shortsStep()` 要排在那個檢查之前，由 Shorts 自己的開關決定做不做。`tick` 不在這裡：工人的迴圈腳本另外每 5 分鐘敲一次（見「誰在什麼時候動手」） |
| `track-init`、`report` | 留著給離線使用；伺服器是正本 |
| CI | `video-tooling.yml` 的煙霧測試加一支 Shorts：用程式產生的正弦波當旁白（`--audio-dir`），從腳本做到上傳包，檢查尺寸、格數、響度 |

工人讀不到 repo 裡的 Shorts 文件：`video_docs` 這個 volume 只在第一次建立時從映像填一次（票 `2026-09-25-the-video-worker-s-docs-volume`），`docs/videos/ai-shorts` 與這份文件都不在工人那裡。所以題目、測試規格與脈絡一律由伺服器在 `shorts/next` 給，工人做出來的腳本與證據放工作區、隨審核送上站；不要讓任何步驟依賴工人去讀 `docs/videos/ai-shorts`。

實測線的製作步驟（`lab.mjs`）：凍結題目（把企劃的輸入、答案、評分寫成 `protocol.json` 並算雜湊）→ 受測模型各跑一次（`subject`；原始回答、模型名稱、時間、重試次數寫成證據）→ 評分（數字題用程式對答案，其餘交查核模型，結果寫 `scores.json`）→ 撰稿（只准照證據寫；兩組都對就說都對）→ 查核（新對話）→ lint → 旁白 → `build` → `qa` → `push`。技術失敗可以重試一次，兩次的紀錄都留；模型答錯不是失敗，是結果。

漫劇直式短篇的原生路線要動到漫劇產線：`tools/video` 目前把畫面寫死 1920×1080，伺服器的 `drama_aspect` 設定（`16:9`、`9:16`）工具沒有讀。那張票（T4）要讓關鍵影格、運鏡、片段、字幕條與合成都依 `aspect` 走，並且跟漫劇那條線協調。在那之前，`from-drama` 是後製路線：不生圖、不重畫，直接從已核准的 16:9 成片裁出跟著主角的 9:16（上表）。

## 政策與依據（2026-09-28 讀官方頁）

| 規則 | 內容 | 來源 |
| --- | --- | --- |
| 自動上傳要事前同意 | 不得在沒有使用者「事前、具體、明示的同意」下自動化或觸發上傳等動作 | developers.google.com/youtube/terms/developer-policies（濫用行為一節） |
| 寫入要講清楚、要先同意 | API 用戶端要清楚指出它代替使用者新增、更新、刪除了什麼，使用者要在執行前明示同意；會設定或修改的瀏覽權限也要講清楚，沒有使用者明確指示不得修改 | 同上（使用者同意一節） |
| 最後決定權 | 用戶端可以建議欄位的值，但使用者對要發布到 YouTube 的資料有最後決定權 | 同上 |
| 不得算衍生指標 | 不得用 API 資料建立新的或衍生的資料與指標；例子是用喜歡數、觀看數算出一個分數。非 API 的數字若和 API 數字並列，要清楚標示不是來自 YouTube | 同上（資料顯示一節） |
| 衍生指標的例外 | 稽核表單第 5 段把用途選成「Analytics & Reporting」並接受增修條款的開發者，可以算自訂的分數與比率、排行等指標，要跟 API 的原值分開標示；統計數字可以存到 36 個月，標題與說明這類資料仍然是 30 天 | developers.google.com/youtube/terms/derived-metrics-policy（2026-09-14 更新） |
| 統計數字可以久存 | 經授權取得的 Analytics、Reporting 資料與統計數字可以存到不需要為止，但每 30 天要確認授權還在、影片沒有被刪 | 同上（III.E.4） |
| 未稽核的上傳鎖私人 | 2020-07-28 之後建立、沒有通過稽核的專案，用 `videos.insert` 上傳的影片限制為私人 | developers.google.com/youtube/v3/docs/videos/insert |
| 配額 | `videos.insert` 自己一桶，每天 100 次；其餘合計每天 10,000 單位：`videos.update` 50、`captions.insert` 400、`videos.list` 1、`playlistItems.list` 1 | developers.google.com/youtube/v3/determine_quota_cost |
| 排程 | `status.publishAt` 只能設在私人、而且從來沒有公開過的影片上；用 `videos.update` 設的時候要同時送 `privacyStatus: private`；時間在過去會立刻公開 | developers.google.com/youtube/v3/docs/videos |
| 上傳檔名 | `fileDetails.fileName` 是上傳時的檔名，只有影片擁有者讀得到 | 同上 |
| 揭露 | `status.containsSyntheticMedia` 可以在 `videos.insert`、`videos.update` 寫入 | 同上 |
| 觀看數的算法 | 2026-08-24 起所有格式的 `viewCount` 都從影片開始播放的那一刻算（含自動播放） | 同上 |
| Analytics 有的數字 | `views`、`engagedViews`、`averageViewDuration`、`averageViewPercentage`、`shares`、`subscribersGained`、`likes`、`comments`；沒有「選擇觀看或滑走」。限定單一影片時，`subscribersGained` 只算從那支影片的頁面訂閱的 | developers.google.com/youtube/analytics/metrics |
| 只看 Shorts | 維度 `creatorContentType` 的值有 `SHORTS`；`video` 篩選一次最多 500 個 id；資料通常晚 48–72 小時，以太平洋時間的日為單位 | developers.google.com/youtube/analytics/dimensions、/data_model |
| 什麼是 Shorts | 2024-10-15 之後上傳、正方形或直式、3 分鐘以內的影片自動歸為 Shorts；Studio 與 API 都沒有開關可以指定 | support.google.com/youtube/answer/15424877 |
| Shorts 的縮圖 | 自訂縮圖只能在電腦版 Studio 設（2026-07-24 起，先開放給營利計畫的頻道）；手機只能挑影格 | support.google.com/youtube/answer/72431、blog.youtube（2026-07-24） |
| 相關影片 | 只能在 Studio 設、要進階功能、目標要是公開或不公開的影片；影片資源沒有這個欄位 | support.google.com/youtube/answer/14075157 |
| A/B 測試 | Shorts 不能做標題與縮圖的 A/B 測試 | support.google.com/youtube/answer/16391400 |
| 字幕 | 自動字幕涵蓋 Shorts；上傳的字幕軌在手機的 Shorts 播放器會不會顯示，官方沒寫。要讓人看到的字就做進畫面 | support.google.com/youtube/answer/6373554 |
| 推薦看什麼 | 觀眾選擇觀看還是滑走、平均觀看時間、平均觀看百分比、喜歡、看完後的問卷；沒有最低發片頻率；Shorts 的表現不會拖累長片的推薦 | support.google.com/youtube/answer/11914225 |
| 上傳上限 | 每個頻道每 24 小時有上限，依地區與頻道紀錄而定，官方不公布數字；Studio 一次最多選 15 個檔案 | support.google.com/youtube/answer/10383400、/answer/12779649 |
| 營利門檻 | 見「成效與每週報告」的表；2027-02-01 起改制，新的條款要在 2027-01-31 前於 Studio 接受 | support.google.com/youtube/answer/72851、/answer/12843009 |
| 不能營利的內容 | 2026-07 起分成三條：制式或重複的內容、重複使用的內容、令人不適的內容；另有一條是假扮真人專家談健康、法律、財務、政治的 AI 角色。點名的例子包含「只有表面差異的旁白故事」「共用同一段旁白的投影片」「看起來像量產、沒有創作者觀點的 AI 模板內容」。可以接受的例子包含「片頭片尾一樣、主要內容每支不同」「每支有自己的主題與觀點的系列」 | support.google.com/youtube/answer/1311392 |
| 揭露什麼 | 擬真的生成或變造內容要揭露，AI 生成的音樂也要；明顯不真實的內容、AI 協助寫大綱與腳本、做資訊圖不用。一般的合成旁白兩邊的清單都沒列 | support.google.com/youtube/answer/14328491 |

官方頁面之間互相矛盾、或查不到明確答案的地方（做之前不要當成事實）：`thumbnails.set` 對 Shorts 有沒有用；沒有通過稽核的專案能不能對 Studio 上傳的影片設 `publishAt`（文件列的條件都符合，但沒有任何一頁明說）；翻譯的標題說明與自動配音適不適用於 Shorts；一般的合成旁白要不要揭露。

## 風險與對策

| 風險 | 對策 |
| --- | --- |
| 全自動、套版型、合成旁白，正是 YouTube 營利政策點名的樣子：「看起來像用模板做的，或連看同一個頻道幾支之後覺得重複」的內容不能營利 | 政策同時寫了什麼可以：形式相近沒關係，每一支的實質內容要明顯不同、而且有創作、教育或其他價值。所以：每支實測測的是不同的事、有真的跑過的測試與留存的證據；頻道立場是站主自己寫的；`variety` 擋掉重複的開場與結構；三個系列各有自己的版面（現在只有一種版面，T1 要補）；每週報告讓站主每週至少看一次。營利審查看的是整個頻道（主題、最多人看的、最新的、占最多觀看時間的影片），這些降低風險，不保證通過 |
| 長片精華被當成「重複使用的內容」 | 精華不是把長片裁一段重新上傳，是用同一份查核過的內容重寫成直式字卡、重新配音；一支長片最多兩支精華；兩支不能講同一件事 |
| 稽核申請書寫的是「站主看過每一支才上架」 | 全自動上架之後這句話不成立。送件前照這份把申請書改成實際的做法：站主事前授權、月曆排程、隨時可以撤回（票 `video-shorts-audit-update`）。申請書不能寫跟實際不一樣的事 |
| 品管誤放行 | 門檻是常數，寫在 `judge.py` 與這份文件；試作後對照站主自己會不會過來調。站主隨時可以關掉「品管全過就核准」回到逐支審，或按暫停 |
| 實測的結果對模型不利，或兩組一樣 | 照實寫是這個系列的賣點，也是規則：撰稿只能照證據寫，查核會擋沒有證據的說法 |
| 受測模型的名稱與版本 | 只寫伺服器回報的名稱；沒有回報就寫「未回傳」，不用代理名稱猜 |
| 稽核前站主忘了上傳 | 時段記成錯過、影片回片庫、報告寫出來；不會補發在奇怪的時間 |
| 授權、權杖失效 | `tick` 每天驗一次（同時滿足政策的 30 天規定）；失效就停止送出並進「需要你」 |
| 預算失控 | 付費工作在送出前由伺服器擋；有未知金額的帳就先停；漫劇直式短篇另外受既有的片段秒數與單支上限限制 |
| 主機磁碟 | 一支 Shorts 約 5–15 MB；公開滿 7 天後 mp4 從審核檔案區刪除（既有規則）；120 支同時在的最壞情況約 2 GB |
| 跟 PR #870 撞檔 | #870 大改 `admin-video-reviews.tsx`、設定與 `video_reviews`。Shorts 的後台票排在它合併之後；伺服器票用自己的模組與自己的設定表 |

## 站主要做的事

一次性（依順序）：

| # | 事 | 為什麼 | 大約多久 |
| --- | --- | --- | --- |
| 1 | 寫頻道立場（設定分頁；草稿在 `HANDS-OFF.md`） | 沒有它，品管的 `policy` 永遠不過，每一支都會落回「需要你」 | 15 分鐘 |
| 2 | 連結 YouTube 頻道（設定分頁的卡片，Google Cloud 五步） | 網站才能補資料、排程、讀數字 | 20 分鐘 |
| 3 | 確認登入的帳號有 `settings.manage` | 才存得了 Shorts 設定與授權 | 5 分鐘 |
| 4 | Shorts 設定：看過預設值、按「自動上架授權」、選第一支公開的日期、開跑 | 全自動的起點 | 10 分鐘 |
| 5 | 法律頁貼上 YouTube API 段落（五語）→ 送稽核申請 | 通過之後才能連上傳都自動 | 1 小時，加上等 YouTube 回覆 |

每週（只在稽核通過前）：下載這一批、拖進 Studio、按「我上傳好了」，幾分鐘。

稽核通過後：看每週報告。

另外兩件有期限的事，跟 Shorts 區的程式無關，但會影響 Shorts 的目標：2027-01-31 之前要在 Studio 接受營利計畫的新條款（已經在計畫裡的頻道才需要）；想用現行的 1,000 萬門檻申請營利，要在 2027-02-01 之前達標並申請。

## 分期與票

| 期 | 票 | 做什麼 | scope | 依賴 |
| --- | --- | --- | --- | --- |
| 一 | `video-shorts-api`（A1） | 遷移（`video_projects` 三欄與 `format`、設定、時段、成效、花費）、`shorts_qa_passed` 與自動核准、時段指派的規則、後台端點（總覽、月曆、花費、設定、授權、暫停）、清單篩選與上限 | `apps/api/app/video_shorts`（models、schemas、settings、slots、costs、rules、overview、errors、admin_api，以及兩個空的路由檔 admin_publish_api、admin_automation_api）、`apps/api/app/models.py`、`apps/api/app/video_reviews`、`apps/api/app/video_automation`（judge、admin_api）、`apps/api/app/main.py`、`apps/api/app/admin/operations_service.py`、遷移、測試 | — |
| 一 | `video-shorts-tools-push`（T1） | 腳本格式第 2 版、三個系列各自的版面、伺服器旁白、`check-audio`、`qa`、`package`、`push`、`import`、CI 的煙霧測試；工人的迴圈腳本在 `auto` 旁邊每 5 分鐘敲一次門（`shorts/cli.mjs tick`，有 `STOP` 檔時暫停） | `tools/video/shorts`、`ops/video/worker.sh`、`.github/workflows/video-tooling.yml` | A1 |
| 一 | `video-shorts-web-routes`（A2） | 工人與工具端點的網站轉送；影片清單的轉送把篩選參數帶過去（原本的轉送不帶查詢字串） | `apps/web/app/api/video/automation/shorts`、`apps/web/app/api/video/automation/videos` | — |
| 一 | `video-shorts-admin-tab`（W1） | Shorts 分頁：頂列、需要你、等你上傳、月曆、片庫、成效、花費、設定與授權；9:16 預覽與遮擋範圍；五語字串 | `apps/web/components/admin-video-shorts*`、`admin-video-reviews.tsx`、`admin-video-review-card.tsx`、`apps/web/app/api/admin-video-shorts`、`apps/web/messages` | A1；PR #870 合併之後 |
| 一 | `video-shorts-youtube-auto`（Y1） | `tick`、照授權自動送出、依檔名認領、Shorts 的欄位、撤回、Data API 的成效快照、每 30 天驗證 | `apps/api/app/video_shorts`（publish、claim、stats、tick、admin_publish_api）、`apps/api/app/video_youtube`、測試 | A1 |
| 一 | `video-shorts-pilot-launch`（P1） | 三支試片改用頻道聲音重做並 `push`；站主做完一次性的第 1–4 項；第一批上傳與公開；把實測的數字與 YouTube 的實測結果寫回這份文件 | `docs/videos/SHORTS.md` | T1、W1、Y1、部署 |
| 二 | `video-shorts-automation-api`（A3） | 題庫與素材、匯入 15 題、`shorts/next` 的規則、每週排片與報告的寫回、`subject` 階段與 `variant`、每月上限 | `apps/api/app/video_shorts`（topics、assets、jobs、plan、reports、admin_automation_api）、`apps/api/app/video_automation`（ai、schemas）、遷移、測試 | A1 |
| 二 | `video-shorts-worker-lab`（T2） | `shortsStep()`、每週排片、實測線的製作與自動修、每週報告、提示詞 | `tools/video/automation`（shorts、flow）、`tools/video/shorts/lab*`、skill 的 `references/prompts` | A3、T1 |
| 二 | `video-shorts-worker-cut`（T3） | 長片精華：挑段落、改寫、連回完整影片 | `tools/video/shorts/cut*`、skill 的 `references/prompts` | T2 |
| 二 | `video-shorts-worker-drama`（T4） | 漫劇直式短篇：產線依 `aspect` 走、直式關鍵影格與運鏡、燒錄字幕的安全區 | `tools/video/core/drama.mjs`、`tools/video/media`、`tools/video/render`、`tools/video/assemble`、`tools/video/shorts/vertical*` | T2、`2026-09-26-video-drama-pilot` |
| 二 | `video-shorts-admin-automation`（W2） | 題庫、素材箱、每週報告、各內容線配額與受測模型的設定 | `apps/web/components/admin-video-shorts-topics*`、`admin-video-shorts-report*`、`apps/web/messages` | A3、W1 |
| 二 | `video-shorts-skill-docs`（D1） | skill 的 `references/shorts.md`、`formats.md` 的 Shorts 一節、`README.md` 的規格表、`AUTOMATION.md` 的 Shorts 一節 | `.agents/skills/youtube-video`、`.claude/skills/youtube-video`、`docs/videos/README.md`、`docs/videos/AUTOMATION.md` | T2 |
| 三 | `video-shorts-audit-update`（O1） | 稽核申請書照全自動的做法改寫：用量、事前授權、用途加選「Analytics & Reporting」；隱私權政策段落補上統計數字 | `docs/videos/YOUTUBE-API-AUDIT.md` | —（截圖要等 W1、Y1 上線） |
| 三 | `video-shorts-auto-upload`（Y2） | 稽核通過後鎖定時自己上傳、每天上限、失敗時的處理 | `apps/api/app/video_shorts`（upload）、`apps/api/app/video_youtube/sync.py`、測試 | Y1、稽核通過 |
| 三 | `video-shorts-analytics`（M2） | Analytics API 的授權與三個時間窗、Studio 匯出檔的上傳與 #871 的算式、成效區的新欄位 | `apps/api/app/video_shorts`（analytics、exports）、`apps/api/app/video_youtube`（connection、client）、`apps/web/components/admin-video-shorts-metrics*` | Y1 |

順序：A1（A2 平行）→ T1、W1、Y1 平行 → 部署 → P1；A3 → T2 → T3、W2、D1 平行 → T4；O1 隨時可以寫，Y2 等稽核，M2 在 P1 之後。部署走 skill `deploy`，是合併後另一步。

規劃時順手發現、另外開的兩張小票：`2026-09-28-video-planner-counts-the-ai-shorts-folder`（企劃模型把 `docs/videos/ai-shorts` 當成一支做過的影片）、`2026-09-28-ai-shorts-docs-carry-one-machine-s-paths`（#871 的文件裡寫著這台開發機的路徑）。

## 還要站主決定的事

| # | 事 | 預設（不回答就照這個做） |
| --- | --- | --- |
| 1 | Shorts 的旁白聲音 | 頻道聲音 Sulafat。三支試片用 Hanhan 做的那一版不上架，改用頻道聲音重做 |
| 2 | 節奏 | 照 #871：90 天 120 支（30／45／45）。三條內容線每週配額 5／2／0，漫劇有第一集之後改成 5／2／1 |
| 3 | 預算 | 照 #871：每 30 天 NT$3,000。漫劇直式短篇一支約 NT$30–90，一個月做 8 支約 NT$500，包含在內 |
| 4 | 稽核申請書 | 送件前改成全自動的實際做法，用途加選「Analytics & Reporting」（O1）。站主也可以選擇先照原稿送（每支都看過才上），通過之後再依政策申報用途變更；那樣在變更之前 Shorts 不能自動上傳，也不能拿 API 的數字算指標 |
| 5 | 要不要連 Analytics | 第三期再連。第一期只用現有授權讀觀看、喜歡、留言 |
| 6 | 什麼時候開跑 | 由站主在 Shorts 設定選。第一期的四張票合併、部署之後才能開跑；想趕現行的營利門檻（見「成效與每週報告」），開跑日越早越好，但不要為了趕日期跳過試作 |
| 7 | 通知訂閱者 | 網站自己上傳時可以選擇要不要通知訂閱者（`notifySubscribers`）。預設通知；一天兩支覺得太吵的話，第二支不通知 |
