# 品牌故事兩支試作與 VPS 私人上傳驗收方案

日期：2026-09-29。此次授權為「依賴就緒後準備試作／上傳驗收方案」。本文件完成可在本機與 GitHub 唯讀確認的準備，沒有登入正式主機、Google 或 Studio，沒有製作媒體、修改正式設定、建立上傳工作或發布影片。原兩張執行票仍保留。

## 依賴現況

以下 GitHub 狀態於 2026-09-29 02:24–02:29 UTC 初查，故事依賴於 **02:33 UTC** 再查並更新。狀態會變；真正執行前須重查當次 SHA。CI 成功、合併、部署、真人驗收分別記錄。

| 原任務與依賴 | 今日可確認的證據 | 是否可進入下一階段 |
| --- | --- | --- |
| `2026-09-28-video-story-pilot`：worker | [PR #933](https://github.com/x812033727/travel_scanner/pull/933) OPEN、非草稿、BLOCKED；更新後 head `345d8e9926d79b107e23db560b4fdf8cc96db2e0`，containers SUCCESS，api/web/full-stack-smoke IN_PROGRESS | **未就緒**。等新 head 的必要檢查通過並實際合併，才可算依賴完成；舊 head 的四綠不能帶到新 head，本方案不接管該分支 |
| 同上：policy/languages | [PR #938](https://github.com/x812033727/travel_scanner/pull/938) 已於 **2026-09-29 02:29:18 UTC MERGED**，merge `0cfcfdc126db3a6f4ed3f3fc2136816ba8045761`；final head `5e0a06329942d6bb155db5a1842810d09d1a9039` 四必要檢查全 SUCCESS | 程式依賴已完成，取代初查時的 OPEN 狀態；仍不代表部署及真人試作完成 |
| 同上：100 篇故事 backlog | [PR #909](https://github.com/x812033727/travel_scanner/pull/909) MERGED，merge `be6f584cb51f4ddb2a541588cb9374451a0e65ad`；四必要檢查成功；本機 done 票及計畫清單存在 | 程式庫資料依賴已完成；不代表已匯入主機或已出片 |
| `2026-09-28-vps-youtube-studio-deployment-and-live`：uploader | [PR #893](https://github.com/x812033727/travel_scanner/pull/893) MERGED，2026-09-28 06:55:22 UTC 合入當時母分支；final head `6ccac4841d7217784a11a1390b1e045e795f398c` 的四必要檢查與專用 uploader 檢查成功 | 已可準備具體驗收方案；不代表部署或 Google 登入完成 |
| 同上：母 PR 與 main 整合 | [PR #890](https://github.com/x812033727/travel_scanner/pull/890) 於 2026-09-28 07:58:26 UTC 合入 main，merge `55e75518e147adcf54dcdda7055be1e79fef4262`；final head `8e4110e4e85488fa41e23bd0b100ab25ff2568c4` 的四必要檢查與 uploader 成功 | 原堆疊已落到 main；以下證據比單看 #893 的 MERGED 更完整 |

#893 合併 SHA `1857a71282728cfd5b94a4b65cca088be5de9936` 位於原母分支，父 PR 後來 squash，因此不是目前 main 的直接祖先。GitHub compare 確認 #890 的 merge `55e75518…` 是 main 的祖先（behind_by 0）。另外比對 #893 final head、#890 merge，以及查詢時的 main `a14d45f8a4caa975b94b8d21cd0e1edc5522055f`，以下四個檔案的 blob 完全一致：

| 檔案 | blob SHA |
| --- | --- |
| `.github/workflows/youtube-uploader.yml` | `0b232d783b1c4187df1850539a1e0fe171bbb303` |
| `apps/api/app/video_youtube/vps.py` | `52ae471986581fe8b32137daa54f1fad7dd110a9` |
| `ops/youtube-uploader/compose.mokaair.yml` | `cc10608e0b7941396107d55331befe7428c02b7f` |
| `services/youtube-uploader/src/studio.mjs` | `a7e3dd5a360eca65b46de2cbee4b3a3eed24bdac` |

專用 [#893 uploader run](https://github.com/x812033727/travel_scanner/actions/runs/36388630493) 及 [母 PR uploader run](https://github.com/x812033727/travel_scanner/actions/runs/36392852878) 都成功。它們涵蓋 synthetic DOM、Docker/headful/noVNC 與同機 RPC；不涵蓋登入後的 Studio。

VPS 現有交接狀態保留為「既有批准紀錄存在、未部署／未真人驗收」。原票及 VPS-UPLOADER.md 仍記錄未部署；本輪沒有連主機刷新此狀態，不能聲稱今天重新證實主機未運行。2026-09-28 的主機預檢已是歷史資料，不能當今天的容量、鎖或埠狀態。執行前應先核對是否有其他 session 已完成其中步驟，避免重部署、覆寫密鑰或重傳影片。

## 品牌故事：等待條件，先不啟動試作

直接依賴 #938 已合併，**#933 仍未就緒**，所以本次不準備可直接執行的主機匯入或生片批次。等 #933 實際合併後，再針對同時包含它與 #938 的精確部署 SHA 完成試作方案與預檢。

原驗收範圍繼續保留為 A01 輪子行李箱、B18 迴轉壽司，各一支；不延伸成每天兩支的 rollout。依賴就緒後，方案仍須納入原票的站主立場、字幕語系、AI 漫劇設定、帳號權限、常設指示、預算與配額確認。`video-story-image-model-pricing` 仍是 open follow-up：它影響工人的估價、快取與模型記錄，試作前要確認它是否已修復，或明列如何避免錯誤估價提前觸發花費上限；量測一律以伺服器帳本為準。

待後續方案納入的既有接受條件：

- 只匯入排程前兩筆，先 dry-run；作品每日支數先 1，不直接啟動 100 篇或每日兩支。
- 原票要求 1920×1080、30 fps、720–900 秒；review/qa.json 全過、每鏡 checks.json 為 motion，單支帳本花費不超過 US$25。這些是接受上限，不是本輪已量測結果或當日供應商報價。
- 每支記長度、鏡數、圖片數／重做率、逐階段時間、帳本金額、訂閱 token、final.mp4 大小與素材雜湊。站主看完兩支；1K 放大品質用實際畫面判斷，改 2K 及額外成本由站主決定。
- 旁白修兩輪仍超長／過短、來源讀不到、額度耗盡時保留工作與原因；不自動換付費 API、不用「放棄」掩蓋失敗。不得在試作完成前宣告工人負載或每日兩支產能已驗收。

詳細原始標準見 [story pilot 票](../tasks/open/2026-09-28-video-story-pilot.md) 與 [STORY.md](videos/STORY.md)。原票與本次看板主報告由稽核協調者更新；本文件不取代它們。

## VPS：待執行的私人驗收方案

### 指定測試件與開始前必填欄位

本方案指定驗收件代號 **`vps-private-acceptance-20260929`**。這是測試件的識別，不代表已有這個影片 slug、媒體檔或上傳工作。開始前由站主把它綁定到一份已核准上傳包；不能臨時拿公開影片或未核准草稿替代。為避免本輪擅自製作媒體，以下欄位保留為執行前必填：

| 欄位 | 需留下的非敏感紀錄 |
| --- | --- |
| 精確版本 | 當次選定的完整部署 SHA、CI run、主機 live SHA、uploader image digest；目前 main 僅為查核基準，不自動成為已核准部署版本 |
| 測試件 | 實際 `/admin/videos` slug、publish gate 已核准版本、metadata SHA-256、MP4 大小／SHA-256、thumbnail 與每份 caption 的 SHA-256 |
| 頻道與影片 | 站主當次確認的 channel ID；第一次新傳後回填私人 video ID；若採既有私人影片路線，事前指定既有 ID，禁止再傳 MP4 |
| 語言及內容欄位 | 建議最小組合為 zh-TW 加 en，實際依此片核准清單；標題、含章節說明、標籤、類別、縮圖、字幕及標題／說明翻譯逐項列出。Made for kids、合成內容與付費宣傳由站主決定 |
| 授權與時段 | 對此版本、設定／密鑰準備、啟動、API 啟用、指定私人上傳及中斷測試的授權紀錄；站主可親自處理 Google 登入與驗證的時段 |

已有明確批准的項目沿用批准紀錄，不重複要求同意；若舊批准尚未綁定現在的版本、實際素材或中斷測試，就補齊缺少的部分。此次「準備方案」不自行變成新一輪部署、登入或上傳授權。測試件未選定或站主無法登入時，停在本節，不建立 job。

### 執行順序與每階段證據

命令及同機配置以 [VPS-UPLOADER.md 的同機部署說明](videos/VPS-UPLOADER.md) 為準；下面界定何時可以進入下一步，不複製一份容易過期的密鑰初始化腳本。

| 階段 | 執行內容 | 通過證據／停止條件 |
| --- | --- | --- |
| 0：版本與既有狀態 | 重新核對原票、PR、部署 SHA 與當次 CI；先確認是否已由別人部署、已有 uploader job 或相同 MP4 | 版本與狀態記錄完整；不把 #893 的合併時間當 live revision |
| 1：主機預檢及備份 | 在已授權的正式操作流程檢查 hold、staged release、部署鎖、磁碟／記憶體、埠與容量；按部署流程驗證備份及回退版本 | 未發生 release 衝突；備份收據與必要時 pg_restore --list 通過。不得自動清掉別人的 hold 或使用 --ignore-hold |
| 2：網站與獨立服務 | 如仍需部署，先保持 VPS URL 未啟用；按已核准 SHA 部署網站及獨立 uploader。只在不存在時建立秘密檔；已有檔案就核對流程，不能覆寫或輪換 | 兩個 Compose project、獨立 profile/data volume、API-only internal RPC network；loopback 8789/6080；健康及服務啟動驗證 |
| 3：網站接線 | 經核准設定 URL、secret file 路徑與 channel ID，保留 .env 權限；僅依核准步驟重建 API | API UID 10001 可讀唯讀密鑰；authenticated status、DNS、頻道一致。只記錄通過與否，不能輸出密鑰或完整環境 |
| 4：站主登入 | 站主經 SSH 隧道進專用 Chromium，親自處理 Google 帳密、2FA、同意與警告，確認精確頻道及 English Studio UI | 重新讀取已登入畫面確認頻道；拒絕登入或出現帳號警告即停止。不搬 cookie、不降低帳號保護；不代替站主處理登入決策 |
| 5：單件私人驗收 | 以指定、雜湊綁定的核准上傳包建立一個 job，依下面矩陣驗 MP4 與各欄位 | 保存 job ID、manifest hash、唯一 private video ID 及逐項結果；不公開、不排程 |
| 6：復原與回寫 | 在站主已核准的時段按矩陣做中斷／重開驗證，確認沒有其他工作受影響 | 同一 ID、同一 package hash、傳送位移／已完成步驟保存，網站 receipt 記錄可重讀 |
| 7：完成或停止 | 站主看完私人影片、核對素材與語言；記錄結果及未解缺陷 | 只有矩陣全過才可把真人驗收標完成。失敗先停 uploader／保留現場，不能將健康檢查或 synthetic CI 當補證 |

如果實際採多段 release driver，須依 [ops/release/README.md](../ops/release/README.md) 由 driver 管理自己的 hold、每段驗證；失敗保留，不能由本方案暗示可清除他人的 hold。

### 驗收矩陣

| 情境 | 操作與預期結果 | 保存證據 |
| --- | --- | --- |
| 首次私人影片 | 只傳指定 MP4 一次，處理完成後仍是 Private、沒有 publishAt；影片可由站主播放且音畫正確 | 唯一 ID、處理狀態、私密狀態與站主播放結果 |
| 欄位與素材持久化 | 標題、完整說明、章節、標籤、類別、觀眾／合成內容、thumbnail、每份字幕及翻譯依核准包保存；離開頁面後重新打開核對 | package hash、每個欄位／asset 的期望值與重讀結果。只看按鈕成功或 HTTP 200 不算 |
| 後台顯示／回寫 | 桌機及手機寬度看 staging、queued、needs_action、completed；關閉後台後重開，若服務已完成可記錄影片連結 | 狀態、同一 ID、receipt 與 persisted site record；截圖遮除個資 |
| 素材傳送中斷 | 同一 job 在 staging 中斷傳送，回到原進度繼續；若需 API 重建，另依核准時段執行 | server offset 接續、最終大小／SHA-256 相同，不建立第二筆工作 |
| 已進 Studio 的中斷 | 已知 video ID 時才做受控 uploader restart；重開後 needs_action，人工核對再續跑已完成步驟 | SQLite job／step 狀態、同一 video ID，無第二次 MP4 upload |
| 未知上傳結果 | 上傳可能開始卻尚未取得 ID 的情況，先在 Studio 核對並填回既有影片網址 | 停在 video_id_required；禁止盲目新傳。不能靠「看不到完成訊息」判定不存在 |
| 既有私人影片更新 | 在同一支核准私人影片上更新測試字幕／metadata 後重讀；若更新包改 hash，先確認舊 job 不 active | 保留同一影片 ID、只更新核准素材；不能刪其他語系或代換公開影片 |
| 登入與頻道守門 | login_required、verification_required、channel_unconfirmed 應停給站主；兩筆工作只允許一個 channel worker | 在真實自然出現的阻擋核對；額外排隊或負向 live 測試需另指定批准素材，不任意動其他影片 |
| 公開影片拒絕／DOM 變動 | synthetic regression 先證明 private_required、歧義 selector 停止；真人遇到 studio_changed 時先記錄並修 sanitized fixture | 不把公開影片改私人以求測試通過；不使用私有 API、不連續盲按重試 |

VPS 上傳本輪驗的是包內 MP4、字幕、縮圖與 metadata 翻譯；沒有把「翻譯」擴張成多語音軌上傳能力。既有影片重試應沿用 ID；不能從取消工作推論影片已刪除。

### 失敗處置及收據

發現 Studio selector 或流程差異時，保留 job、已知 ID、素材雜湊與去重狀態，記 sanitized observation，另開最窄的修正票並重跑對應回歸後重驗。停止獨立 uploader 時同機配置仍需帶兩份 Compose 檔；保留 volume。先確認遠端 job 停住，才可移除網站 URL、重建 API 並恢復原上傳路徑。單純移除網站 URL 不會停止已排入 VPS 的工作。不得 down -v，不刪 Google profile 或素材來「重試」。

正式收據放在原 VPS 驗收票或其獨立接受紀錄，至少含：UTC 時間、部署 SHA/image digest、核准包雜湊、job ID、private video ID、頻道核對結果、每列 PASS/FAIL/BLOCKED、重讀與播放證據、重啟前後狀態、未解缺陷。MP4、Cookie、瀏覽器 profile、密鑰與個資不進公開 repo；敏感素材只保留在指定的私人 evidence 位置。

## 本次交付與驗證

本次只完成方案與依賴清單：VPS 的程式依賴已具備，故事試作仍等 #933；#938 已在本輪完成合併。沒有把兩張原執行票結案，也沒有填造正式驗收結果。

驗證方式：唯讀 gh pr view / gh api 核對狀態、四必要檢查與 uploader checks、stacked merge 路徑、四個相關 blob；閱讀原票、STORY.md、VPS-UPLOADER.md、youtube-video／deploy／task-board 技能與 release hold 規則。文件變更執行 npm run check:tasks；沒有為純方案重跑媒體生成、容器或真實上傳測試。
