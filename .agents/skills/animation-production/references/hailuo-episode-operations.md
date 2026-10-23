# Hailuo 網頁整集製作：數百鏡的守衛、每包迴圈、瀏覽器實務與收工

用內建瀏覽器、以**站主的登入**在 hailuoai.video 把**一整集**（數百鏡）從鎖定包做到每鏡都有交付時讀。`.agents/skills/animation-production/references/browser-production.md` 管第一次：本次工具能力、三鏡 pilot、每 take 收據；這篇管 pilot 之後，照鎖定包一包一包做完整集。前提不變：開拍鎖定包（`.agents/skills/animation-preproduction/SKILL.md`）站主已確認，授權範圍內不逐鏡再問。

經驗來自《偶的江湖》第一集：17 輪、2026-10-09 → 10-15、31 包；鎖定包 455 鏡（clip 420、still 30、cut 5）；帳本 978 筆動作（含 Codex 時期 374 筆基準）；全域花用 36,721／38,000 點（帳本 `totals()`，10-15 讀）。來源縮寫：「R n」＝交接檔的第 n 輪、「補 n」＝第十七輪的第 n 段補記（分支 `codex/ou-de-jianghu-visual-preproduction-20261008` 的 `…/ou-de-jianghu/visual-development/handoff/CLAUDE-PROGRESS-20261009.md`；票 `2026-10-08-ou-de-jianghu-visual-handoff` 的 Notes 是它的摘要）；「工具」＝操作腳本原文（10-15 讀）；「量到的」＝ffprobe 實測。沒標的就當沒驗。海螺的頁面會改版（R12、補十九都碰到），每次開工先用當天的頁面核對。

**頁面注入是這一集站主的裁定，不是預設。** 首格與參考圖用頁面 JS 從海螺自己的 CDN 抓副本、頁內驗 SHA-256 後塞進 file input；取檔抓「無水印下載」實際 fetch 的網址、本機 curl 存。站主 2026-10-10 把這兩條定為本製作的正式規則：每次記 SHA 或網址；繞過付費、額度、浮水印仍禁止（R5）。它和 browser-production.md 第 1 節「不用頁面注入繞過檔案限制」有張力：新的製作或新的操作者先問站主一次，沒有裁定就照第 1 節。

工作目錄（repo 外，名稱照這一集）：

```text
<VIDEO_WORKDIR>/<episode>/                      E：STOP（有就全停）、LEASE（製作租約）
  browser-production/<date>/continuation-plan/  video.json、plan/lock.json、plan/changes.jsonl、shot-plan.stdout.json
  browser-production/<date>/finish-episode/     F：authorization-resume.json、action-ledger-resume.mjs、actions/<id>.json
    throughput-resume-<date>/                   O：<id>-official.png|mp4、qa/、claude-next-batch-<N>-<date>/、next-D-claude-<date>/
      claude-recover-<date>/                    H：操作腳本（claude-submit.mjs、gen-*-js.mjs、file-*.mjs、各包的 ffNN／vstepNN）
```

## 一、角色與守衛

| 誰 | 做什麼 | 不做什麼 |
| --- | --- | --- |
| 站主 | 在窗格登入；定上限、額度期、操作額度、變更單、修圖路線、放行與吸收；跑改授權檔／鎖定包／帳本的腳本；需要時在窗格的原生選檔框選檔；實聽 | — |
| 操作者（主對話） | 開瀏覽器、記意向與結算、取檔建檔、寫 QA 收據、交接 | 買點數、改 `buy_s`、改授權檔、上架、合併、部署 |
| 建包子代理（這一集用 opus） | 從鎖定包建一包（第二節第 2 步），只寫自己的包資料夾 | 動帳本、授權檔、別包的檔 |
| D 軌子代理（opus） | 每個 take 一個新資料夾建台詞軌（第 11 步），影片收據寫好之後才做 | 改收據、改畫面 |

**授權檔 `authorization-resume.json`（schema 2）是唯一的「可以花什麼」。** 每次改動都備份前一版（`authorization-before-<tag>.json`），並在對應的歷史陣列加一筆：時間、誰、站主原話、前一版 SHA。10-15 讀到的值：

| 欄位 | 管什麼 | 10-15 的值 |
| --- | --- | --- |
| `period_a_cap`／`period_b_cap` | 站主在鎖定包核定的兩個額度期上限 | 26,980.8／21,753.6，全程沒改 |
| `active_batch`、`active_batch_period` | 在批次裡、且期別等於現行期的鏡才能記意向 | 445 鏡；期別切換 8 次（`active_period_changes`） |
| `active_batch_new_credit_ceiling` | 操作額度：全域內部上限，不是加預算 | Claude 接手時 7,600，放寬 7 次到 38,000（R2–補十一） |
| `repair_shots`、`repair_credit_ceiling`、`repair_total_image_take_cap` | 修圖路線：哪幾鏡可多畫首格、修圖花費上限、首格 take 上限 | 15 鏡、1,803 點、4（只給 a02-s028；平常 3） |
| `total_video_take_cap` | 每鏡影片 take 上限（一般首格上限 2 寫在 guard） | 2 |
| `blocked_shots`、`material_dependencies` | 結果不明、或依賴未定素材的鏡不能再送 | 0 鏡 |
| `lock_sha256`、`shot_plan_sha256`、`source_sha256` | 鎖定包、shot-plan、`video.json` 的雜湊；變更單改了就重記 | `lock_changes` 9 筆 |
| `lease_owner`、`lease_pid` | 誰持有製作租約 | `lease_resumes` 3 筆 |
| `credit_readback_max_age_ms` | 餘額讀回最多多舊 | 300,000（5 分鐘） |
| `reconciliations`、`repair_adjudication_changes`、`operating_ceiling_changes` | 事後關帳、修圖放寬、額度放寬 | 6、6、7 筆 |

**帳本只增不改**（工具 `action-ledger-resume.mjs`）。每筆動作是 `F/actions/<id>.json`，`<id>`＝`<shot>-start-t<N>`／`-end-t<N>`／`-video-t<N>`。`guard()` 每次查：沒有 `STOP`；`LEASE` 的 owner／pid 等於授權檔；`video.json`、`lock.json`、shot-plan 的 SHA 等於授權檔；Codex 時期基準動作的財務欄沒動。`intent` 再查：在 `active_batch`（或修圖路線）且期別相符（否則 `SCOPE`）；這鏡沒有未結動作、不在 `blocked_shots`、不依賴被扣住的素材（`SHOT_HOLD`）；兩期上限、操作額度、修圖額度（`BUDGET`）；累計 take（`TAKE_CAP`）；影片正文逐字等於 shot-plan、秒數等於 `buy_s`（`CANONICAL`）；附一份**新的**餘額讀回（`observed_at`、截圖、頁面摘錄；5 分鐘內、晚於上一筆財務事件、不能重用），讀回數字要等於「基準餘額減所有已記扣款」（`BALANCE`），扣掉未結保留還夠付報價。`update` 不准改輸入欄；扣款與 `balance_after` 要對得上新讀回；扣 0 點必須是終態（failed／refunded）且附不扣點的證據；`unknown` 不能記 0；`downloaded` 前要先結算。

流程固定三步：`intent`（按創建之前）→ `settle`（狀態 generating、`provider_group_id`、扣款＝報價、`balance_after`、讀回）→ `downloaded`（`file-*.mjs` 記路徑、SHA-256、`provider_asset_id`、`download_method`、抓到的網址）。帳本表達不了的事（排隊中取消後才退點、送出就被擋的 0 扣款、卡死的工作）由**站主跑**的 `reconcile-*.mjs` 關：先用帳本自己的算術證明（基準減已記扣款＝頁面餘額），再改那幾個動作檔、授權檔 `reconciliations[]` 記一筆、整夾備份（R7、補五、補十四、補十六）。10-15 讀 `actions/`：圖 downloaded 511、failed 4；影片 downloaded 451、refunded 8、failed 3、provider_rejected_refunded 1。

**收據綁 SHA，一路串下去**：動作檔 → `qa/first-frame-review-<shot>-t<N>.json`（綁圖檔、動作檔快照、包）→ 影片意向的 `first_frame_review` → `qa/video-review-<shot>-t<N>.json`（綁影片、動作檔快照）→ D 軌的 `timeline-and-sources.json`（綁影片收據）。寫收據的腳本用 `flag: 'wx'`，檔在就拒寫。改了上游任何一份，下游的綁定就斷（錯誤目錄 #76）。

**製作租約**：`claude-lease-<date>.mjs` 是背景程序，把 `{owner, pid}` 寫進 `E/LEASE`，帳本拿它比對授權檔的 `lease_pid`。session 一結束程序就死，下一個 session 的第一筆 intent 以 `Unexpected lease owner/PID` 失敗（10-12、10-13、10-15 三次，`lease_resumes[0..2]`）。接手：重跑 lease 腳本拿新 pid → 站主跑 `claude-lease-resume-<date>.mjs`（只改 `lease_pid`、備份、`lease_resumes[]` 記前一版 SHA、租約 token、站主原話）→ `guard()` 過了才送。失敗的 intent 留下 `<id>-before.json/.png`（讀回檔是 `wx`），重跑前改名 `*.orphan-*`，不刪（補十九）。換操作者（Codex → Claude，10-09）時：前一位放 `STOP` 並釋放租約；接手者把 `STOP` 改名歸檔、起新租約、授權檔只換租約持有人並備份（R1）。

**誰跑哪支腳本**：

| 腳本 | 改什麼 | 誰跑 |
| --- | --- | --- |
| `claude-submit.mjs intent｜image-intent｜settle｜evidence`、`file-image.mjs`、`file-video-url.mjs`、收據與聯絡表腳本、頁面 JS | 帳本的正常三步、操作者自己的檔 | 操作者 |
| 建包腳本（`build-packet.mjs` 等）、D 軌 builder | 只寫自己的資料夾 | 子代理 |
| `set-active-period.mjs`、`raise-ceiling.mjs`、`extend-active-batch.mjs`、`extend-repair-*.mjs`、`apply-buy-change-*.mjs`、`reconcile-*.mjs`、`claude-lease-resume-*.mjs`、合併腳本 `apply-recommendations-*.mjs` | 授權檔、鎖定包、已記帳的動作 | **站主**（在 cmd） |

最後一列自 10-14 起一律站主跑：自動模式的分類器把操作者執行它們判成交易或修改共用資源（10-10 擋 `set-active-period`／`raise-ceiling` 三次，R6；10-14 連 Write 與 heredoc 寫進 `H/` 都擋，補十三、補十四）。更早幾輪操作者憑站主原話跑過 `extend-active-batch`，分類器時擋時放，不要依賴。操作者把這類腳本寫在自己的 scratchpad：先全部檢查再寫、一個備份夾、歷史陣列記站主原話、重跑會被自己擋下（補二十）；給站主的是 cmd 指令（cmd 不吃 `S=...` 這種 bash 寫法，補十四）。

站主在這一集的常設規則（新製作要重問）：「建好包就直接跑，不用問我」（10-12）；「D 軌做完直接推，不用再問」：每輪的素材、收據、D 軌、交接檔直接推到製作分支（10-13）。買點數、改 `buy_s`、上架、合併、部署仍要站主。

## 二、每包的操作迴圈

一包最多 24 鏡（建包上限 `pick_limit_24`）。24 鏡約 1,800 點（第 7 包首格 553＋影片 1,308＝1,861，R8；第 14 包 1,816，與估計相同，R15）。供應商一次生成一支、每支約 4–5 分鐘，一包前後 2.5–4 小時（R9、R11–R13）。

1. **開工與對帳**（每個 session 開頭）：`guard()`、`totals()`；租約（上節）；窗格登入：登入跟著窗格的 profile，窗格關掉再開、或登入分頁被站主開 mp4 換掉，都要站主重登（R7、補十）；佇列裡跑完的卡先取回。
2. **建包**（建包子代理，照上一包的建包腳本）：照鎖定包的買入順序（A1–A236、B1–B184），選參考圖都有提供者端副本的鏡；第 13 包起先量台詞（10-12），裝不下鎖定秒數的放進 `dialogue_overrun_hold`；`skipped` 逐鏡寫原因（already_done、missing_references、owner_hold、end_frame_route、dialogue_overrun_hold、pick_limit_24）。每鏡給：參考圖順序與 CDN 副本（網址、SHA、對本機 PNG 的 PSNR）、首格提示詞（鏡頭句＋原文＋實作段＋每角色左右規則＋`look.style`＋參考順序＋「One moment only; no panels, text or labels.」）、鎖定包的 H3 正文與 SHA、送出前旗標（起始狀態、冠頂留白、左右、道具數、手）、首格 QA 清單、連戲參考格；另給 `packet.md`、`verify-packet-shot.mjs`、`next_operator_step`、`operator-copies.json`（各包編號腳本的 sed 指令與預期 SHA）。建包時斷言變更單鏈、授權檔每一步與 `protected_fingerprint`，全部通過才一次寫檔（R15）。之後由站主跑 `extend-active-batch.mjs` 把鏡加進批次。
3. **種子檔**：`packet<N>-image-inputs.json`（refs 是 `[url, sha, name.jpeg]` 陣列；包裡寫成物件時要轉，R10）、`packet<N>-video-inputs.json`（首格、乾淨網址、SHA、正文、`buy_s`）、`-ff-takes.json`（用哪一張首格）、`-clean-urls.json`。變更單之後，`buy_s` 要改成鎖定包的新值、重產步驟檔（補十七）。
4. **首格步驟**（圖像頁 `…/create/image-generation`；直接導網址會被轉回影片頁，要點頁首「圖像」，R16）：每次載入先設 GPT Image 2.5 Sunburst／16:9／High／2K／張數 1，因為比例會退回「自動」或 21:9、張數退回 4（R7、R12、補十四、補十九）。拆三步，每步都遠低於 45 秒（工具 `fstep15-js.mjs`）：A 移除舊參考、抓 CDN 副本並在頁內驗 SHA、塞進多檔 input、用 Slate 編輯器 API 逐行寫提示詞；B 輪詢最多 38 秒等參考數與報價（上傳有時 30 秒以上才反映，R9）；C 預檢（提示詞、報價＝20＋參考張數、底欄籤的順序 model／16:9／High／2K、縮圖數與 CDN 來源）→ 創建 → 輪詢最多 20 秒等新卡。報價是 20＋每張參考 1 點（工具 `gen-prep-js.mjs`；第 7 包平均每張 23 點，R8）。
5. **記帳與送出**：按創建前先 `intent`（`image-step.sh`、`ffNN.sh`、`vstepNN.sh` 把上一張的 `settle` 與下一張的 `intent` 串在一起）；只按一次，**沒重掃就不准再按**（錯誤目錄 #69）；讀新的 `media-group-<id>` 與頁首餘額（餘額有時慢半拍，結算前再讀一次，R17）→ `settle`。
6. **取檔**：到作品詳情頁 `…/my-work-detail/ai-image/<id>` 或 `…/ai-video/<id>`，等約 7 秒水合（R14）；先裝 `window.fetch` 鉤子，從 `button.ant-dropdown-trigger` 的 React fiber 找 `memoizedProps.menu.items` 裡 key 為 `downloadWithoutMark` 的項目，直接呼叫它的 `onClick`（隱藏窗格不渲染 antd 下拉，R7）；抓 `content-type` 為 `image/png`／`video/mp4` 的 `multi_chat_file/…` 網址，本機 curl。選單沒出現就再導一次頁（R9）。**永遠不用畫廊的 `<img>`／`<video>` 網址**：烙了 MINIMAX／Hailuo AI 浮水印；去掉 `?x-oss-process` 的裸 `.png` 仍是浮水印版、檔案 id 不同（R7）；畫廊與詳情頁顯示的 2560 寬 PNG 也不是無水印檔（R9）。圖片詳情頁在隱藏窗格會卡死分頁：一張開一個新分頁，抓完就關；影片詳情頁同一分頁連續導頁沒問題（R6）。
7. **建檔**：`file-image.mjs`／`file-video-url.mjs` 存成 `O/<id>-official.png|mp4`（檔在就拒寫）、驗檔頭（PNG 簽名／`ftyp`）、記 SHA-256 與 `download_method: official-no-watermark-ui`；影片另算首格 PSNR（對本鏡首格，量到 30.8–31.9 dB，R17、補十九、補二十），並出聯絡表與末格。尺寸一律 ffprobe 量，不抄模板（R12：45 張收據抄成 2560×1440，實際 1672×941）。
8. **首格 QA 收據**（`write-ff-receipts-*.mjs`）：1280 px 看全圖、原解析度裁冠頂與手；`verdict` 寫 candidate／limited_candidate／HOLD（附 `hard_blockers`）／退回，限制寫 `limits_zh`。這一集收斂出的規則：冠整頂在畫內、最高飾物上方留一條背景（冠被上緣切掉是 blocker，a05-s084 立的規則，補九、補十一；量法：PNG 頂端 4 列有沒有金色像素，R6）；每角色左右規則照包裡的 `laterality_rules_per_character`（遠側眼角的霜花、袈裟披哪一肩）；起始狀態不能已經做完動作（a03-s006 首格已看著沈、a03-s034 左掌已張開，影片沒戲可演，R8、R9）；道具數與材質（匣、三枚銅錢、一壺一杯，R15）；**動作需要的東西要在畫內**（a02-s028，第四節）；跟鄰鏡連戲（a05-s020 草帽戴在頭上還是掛背後，R16）；16:9、2560×1440。首格 take 上限一般 2，修圖路線 3–4。
9. **影片步驟**（`…/create/image-to-video`；分頁要 `tabs_select` 到前景才渲染，補十九；先 `resize_window` 1400×900，因為窗格寬度一變或回合結束，模擬就被清掉、退回手機版面，`#video-create-textarea` 與時長籤都不見，R15、補十三）。拆四步（工具 `vstep15-js.mjs`）：A 模式籤「全能參考」→ 浮層裡的「起始/結束幀」、移除舊圖、抓乾淨首格驗 SHA、塞進 file input 就回傳；B 輪詢最多 38 秒等上傳到 CDN（一般 30 秒以上，10-14／15 夜裡 50 秒以上，補十八、補十九）；C Slate 寫正文、開時長抽屜（滑桿圖示的 React `onClick`）選秒數、對編輯器派發一串 pointer／mouse 事件關抽屜、讀回；D 預檢（沒有開著的 popover，停在 `ant-zoom-big-leave` 的不算；模式；報價＝12×秒；時長籤＝`buy_s`；正文片段；恰好一張圖）→ 創建 → 4 秒後讀群組數、生成中的 id、餘額。H3 2K 報價 12 點／秒（實測 2026-10-04：5 秒扣 60；工具 `gen-video-js.mjs` 的 4–10 秒表）。實際片長（量到的，24 fps；R17、補一）：

   | 買 | 4 s | 5 s | 6 s | 7 s | 8 s | 9 s | 10 s |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | 實長 | 4.458（107 格） | 5.167（124） | 6.583（158） | 7.292（175） | 8.000 | 9.417（226） | 10.125（243） |

   輸出 2560×1440、24 fps、帶 AAC（不用）。佇列上限 12（toast「視頻隊列限制: 12」，按創建沒反應、不扣點，R7）；卡死的工作也佔一格（錯誤目錄 #70）。
10. **影片 QA 收據**（`write-qa-receipts-*.mjs`）：完整影音解碼（`ffmpeg -xerror -err_detect explode`）、尺寸格數秒數、首格 PSNR；看 12 格聯絡表（每 10 格一張、640 px、4×3，`make-sheets-take.sh`）＋末格 1280 px＋冠與手的放大裁圖。抽格只證明那幾格：`animation_verified` 可以寫 true，`real_speed_listened`、`lip_sync_verified` 寫 false。這一集常見的有限與 HOLD：動作給錯人（a02-s075 t2、a02-s020 t1、a03-s067、a05-s048）、動作太小或沒有（a03-s069、a05-s040）、憑空長東西（a02-s028 匣、a04-s016 繩樁、a03-s074 t2 第二把扇）、方向反（a01-s012 旗往左展）（R1–補十八）。10-10 時 41 份影片收據是 32 候選、7 有限、2 HOLD（交接檔的額度估算節）。影片 take 上限 2。
11. **D 軌**（D 軌子代理）：每個 take 一個**新**資料夾 `next-D-claude-<date>/<shot>-video-t<N>/`（still 是 `-still-t<N>`）；把最新的 `build-candidate.py` 複製進去、只加這鏡的列（`SHOTS`、`PREV_D`／`NO_PREV_D`、`OWNER_ABSORB`）、用 `PYTHONUTF8=1` 跑；README 記 builder 的 SHA 譜系（例：`429566d1→d6de1bc5`，插 7 行，補二十）。固定規則（R14 交出的 builder 說明）：台詞 PCM 逐位元等於來源、不變速不剪；句間 `pause_after_ms`（預設 300 ms），一場最後一句再加 700 ms、全集最後一句加 1,500 ms（`tools/video/core/timeline.mjs` 的 `SCENE_GAP_MS`、`TAIL_MS`）；前導延伸到第一個 ASR 字前 80 ms；上一鏡的溢出（carry-in）佔用這一鏡的前導；台詞本身超出畫面時前導 0、只出 D、不合成畫面；網頁錄音切片、或前一鏡還沒有 D 時標 provisional，後台錄音且帶入已知才是 candidate；無台詞的鏡只寫 README＋timeline（`no_dialogue_lines_no_D_built`）；still 的停留＝帶入＋台詞＋間隔＋場尾，進位到整格（補四）。資料夾裡不放 `*.before-*`（builder 的 take 排序會壞），被取代的整夾搬到 `next-D-claude-<date>-superseded/`（補八）。離線 ASR 的旗標（差很多、句首被截、同音字）只記錄，不是實聽。
12. **交接**（每包、每張變更單都做）：交接檔補一段（卡片與群組 id、每鏡判定、點數、全域／期別／修圖／餘額、D 軌數）、票的 Notes 一行、記憶一條；用暫存索引 commit 推到製作分支（不切分支）；session 結束前把窗格 viewport 重設回 desktop（R16）。

## 三、瀏覽器實務

| 現象 | 做法 | 來源 |
| --- | --- | --- |
| 登入跟著窗格的 profile：別的瀏覽器登入了不代表這裡登入；窗格關掉再開、登入分頁被換掉就登出 | 請站主登入（Ctrl+Shift+B 顯示窗格）；不代輸密碼 | R1、R7、補十、補十九 |
| `javascript_tool` 一次上限 45 秒，逾時後頁面裡的腳本還在跑；隱藏窗格的計時器被節流、CSS 離場動畫跑不完、antd 下拉不渲染 | 每步拆到 38 秒內；逾時先用便宜的 JS 讀狀態再決定；等待用 `browser_batch` 的 `computer wait` 串起來，不在頁內 sleep；取檔用 fetch 鉤子的 Promise，不輪詢 | R9、R15、補十一 |
| 圖片詳情頁在隱藏窗格會把分頁卡死（連 `location.href` 都逾時）；平行開多個 `preview_start` 會搶同一個分頁 | 一張一個新分頁、抓完關掉；要多個分頁用 `tabs_create`＋`navigate` | R6、R7、補十九 |
| 影片頁網址是 `create/image-to-video`；分頁不在前景時 SPA 不渲染 | `tabs_select`；`resize_window` 1400×900 | 補十三、補十九 |
| 創作頁不會自己更新生成狀態；列表偶爾空白；卡片多時 `innerText` 掃描 45 秒逾時 | 掃之前重新導頁；完成與否改到作品詳情頁試取檔判斷 | R9、R12、補十七、補十八 |
| 兩個分頁同時下 navigate／JS 會互撞逾時 | 一個分頁送、另一個分頁取，但不同時下指令 | R15 |
| 首格上傳到 CDN 要 30 秒以上，慢夜 50 秒以上；偶爾第一次沒進 CDN | B 步輪詢；沒進就清掉已注入的圖、重跑 A、B | R12、R15、R16、補十九 |
| 標籤會搬家：10-15 起「參考圖片 N」是歷史卡片的標籤、不是作曲區的；設定抽屜關著時「16:9」字樣仍在 DOM | 預檢讀縮圖數＋CDN 來源＋報價；比例讀底欄籤的順序 | R12、補十九 |
| 內建瀏覽器對 `127.0.0.1`／`localhost` 的 fetch 一律 `ERR_BLOCKED_BY_CLIENT`；沒有本機選檔工具；幾 MB 的 base64 塞不進頁面 | 本機檔請站主在窗格用原生選檔框親手選，或用 Claude in Chrome 的 `file_upload`（已連線、先問站主）；再用提供者副本對本機檔算 PSNR 證明選對檔 | 補二十；2026-10-04 首見 |
| 提供者把上傳存成降尺寸的 JPEG 副本（`multi_chat_file/<ts>-<uuid>.jpeg`；修圖版的副本是 1920×1080），不會和本機 PNG 位元相同 | 參考圖就用副本，記副本網址與 SHA；對回本機 PNG 先用 16×16 平均雜湊預篩（`match-refs.py` 收 Hamming ≤ 40；10-13 掃描時真副本 ≤ 5、無關圖 51 以上），再以 PSNR 確認（量到 44–51.6 dB） | R2、補八、工具 |
| 參考圖不在帳號裡（10-10 估算時約 42 鏡卡在這裡） | 站主在圖像頁的「參考」選檔一次（一次最多 16 張，頁面的「参考图 (n/16)」）；查有沒有進來用頁內的上傳清單（`POST /v2/api/upload/files`，同源、唯讀、最新在前），不翻虛擬捲動的 /mine；10-13 站主說傳好了的三張其實沒送出 | 估算節、補八 |
| 排隊中的卡有「取消」→「確認」，立即退點；進入生成之後沒有取消（伺服器旗標 canCancel／canRetry／canAppeal 全 false） | 送之前查清楚；卡死的處理見錯誤目錄 #70 | R7、補六 |
| 「Policy check temporarily unavailable; retry.」 | 暫時的，重跑就過 | R16 |
| 窗格隱藏時截不了圖，但餘額讀回需要截圖檔 | 這一集附較早的截圖並在摘錄寫明（`image-step.sh`）；能讓窗格顯示著就取真截圖 | 工具 |

## 四、重做、修圖路線與變更單

**什麼時候複審舊首格**：別的操作者或更早時期買了、還沒拍影片的首格，拍影片前免費複審一次，收據綁新的包，舊的 HOLD 收據搬到 `qa-superseded/`（10-14 複審 Codex 時期五張都收，補十三；第 29 包複審八張收五張、三張重畫，補十七）。宣告「沒畫過」之前先查 `F/` 與 `O/`：「暫緩九鏡」裡有四鏡 10-09 早已各畫兩張（補十七）。

**修圖路線**：授權檔的 `repair_shots`＋`repair_credit_ceiling`＋`repair_total_image_take_cap`。每次放寬是站主跑一支腳本、`repair_adjudication_changes[]` 記一筆，額度用算式給：新額度＝舊額度＋這鏡已花＋首格張數×25＋影片秒數×12（a04-s043：1,469＋48＋25＋48＝1,590，補十九）。這一集修圖額度 182→687→1,352→1,469→1,590→1,778→1,803（補十四–補二十）。首格提示詞改了就是「有紀錄的修圖變更」：`prompt_change` 記舊／新 SHA、每一句改動與理由，把改動還原要得回舊文字（第 31 包，補二十）。影片正文不改（帳本 `CANONICAL` 擋）；若為修圖改了打進頁面的句子，帳本照記正典句，實際打的句子與 SHA 記在 `operator_note`／`prompt_as_typed_sha256`（R16）。

**台詞先量，再買秒數**：需求＝台詞（後台 WAV 的樣本數，或網頁錄音切段的 window）＋句間 300 ms＋場尾 1,000 ms（300＋700）＋前導（含上一鏡帶入）。拿需求對**實際片長表**（第二節第 9 步），不是對名目秒數：5.34 s 的需求買 5 s（5.167）會溢出，買 6 s（6.583）才裝得下。長老的後台錄音每句 2.4–4.2 秒（R13，10-12），照 `action_seconds` 定的 `buy_s` 普遍裝不下。寫「買 N 秒」前先看 `lock.json` 的 `visual_kind`：cut 與 still 不買影片（a04-s067 是 cut、a04-s071 是 still，站主差點為它們付點數，補三；錯誤目錄 #66）。

**溢出有四條路**，每條都由站主選，選了就寫成紀錄：（1）變更單買長；（2）下一鏡的前導吸收（`owner-absorb-<shot>-<date>.json`，下一鏡開頭至少留那麼多靜音；a05-s081 的 0.733 s 由 a05-s082 吸收，a05-s082 因此要 6 s，補十、補十一）；（3）剪接時縮停頓（a03-s030→s031 縮 0.168 s，記在變更單那行的 `editorial_decisions`，補二）；（4）保留不拍，等裁定。

**變更單**（`shot_plan.mjs` 沒有單鏡覆寫，10-12）：一支一次性腳本（站主跑）改 `plan/lock.json` 與 `shot-plan.stdout.json` 的 `buy_s`、`promise.buy_s`、`cost`（12 點×秒、期望×風險 take、上限×take 上限）與 totals，改前各留 `*.before-<tag>.json`；`plan/changes.jsonl` 追加一行（`plan_lock.mjs` 的格式、站主原話）；同步建包時比對用的鎖定秒數表；把新的 lock／shot-plan 雜湊記進授權檔 `lock_changes[]`。帳本比對這兩個雜湊，之後的 intent 才讀到新秒數。這一集共 9 張（10-12 → 10-14）：第一張 15 鏡加 21 秒、單 take +252 點；第二張 14 支已出片的鏡重買、加 22 秒（重買實花 1,116 點，R17）；9 秒以上先買一支量實長（9.417 s）再開第三張（補一）。

**起始／結束幀**：結束幀要拿起始幀當參考 1（pilot a02-s037 的做法），否則尺度會漂。a04-s043 結束幀 t1 只用四張板，比起始幀緊約兩成、冠被切；t2 把參考 1 換成起始幀的乾淨 CDN 副本，與起始幀逐一對上（補十九）。影片意向兩張幀都綁，起始、結束兩格各注一張。

**首格要有動作需要的東西**：a02-s028 第 29 包的首格提示詞寫「只到上胸、手和匣在畫外」，鎖定的動作卻是「雙手按平在匣蓋上」，影片 t1 憑空長出一個棕色木匣（limited，補十七）；t3 改成從冠到膝入畫、拿上一鏡首格裡的匣當參考 3 才對（補二十）。寫首格提示詞時把 motion 的受詞逐一對過：手、道具、對象都要在畫內，而且是起始狀態。

**GPT Image 的左右偏誤**：近側臉朝下時，遠側眼角的霜花 2／2 被畫到近側臉頰；t4 把左右規則整句移到提示詞最前面也沒用（a02-s028，補二十）。早先 a03-s044／046 霜花落在頰側（R5）、a02-s056／074 念珠手臂相反（R7）。明寫一句有時有用（a05-s063 袈裟寫「LEFT shoulder ONLY…」，t2 一次對，R17）。規劃時，有遠近側標記的鏡頭先排正面或另一側的角度，不然預留一次本機修圖。

**本機修圖是一個有紀錄的步驟**：站主先同意（「本機修圖再拍」，10-15）；腳本（PIL）＋紀錄 JSON＋收據（標明不是海螺產出）；上傳靠站主在窗格的原生選檔框；用提供者副本（1920×1080 JPEG）分別對修圖版與未修圖版算 PSNR（41.7 對 40.3 dB；差這麼小要再加區域檢查：舊印區沒有紫）證明選對檔；影片意向綁修圖紀錄。站主看了有疑慮就另做一版給他比，不覆蓋（補二十）。意向時寫錯的欄位（`upload_method` 寫成頁內 fetch）在結算摘要與收據更正，動作檔不原地改（D 軌已綁）。

**給站主的決定用選項表**：一項一列、A 案是建議，寫明多少點、影響哪個接點；站主回「依建議」就整表照做（10-14 十一項，補十七）。

## 五、收工與交接

**五個數字**（SKILL.md「收工」那節）在網頁路線的對應，10-15：

| 數字 | 網頁路線怎麼算 | 《偶的江湖》第一集，10-15 |
| --- | --- | --- |
| job ready | 帳本 `downloaded` | 影片 451、圖 511 筆（含 Codex 時期的基準動作） |
| QC ok | QA 收據的 verdict（candidate／limited／HOLD） | `O/qa` 影片收據 418 份、首格收據 458 份、結束幀 2 份（含退回與 HOLD）；每鏡至少一份候選或有限候選 |
| judge passed | 沒跑 `clips import --judge` | not_checked |
| needs_review | HOLD 或等站主的鏡 | 0（補二十：沒有等站主的事） |
| 站主 accepted | 收據的 `owner_accepted` | 0：全部 false，`normal_pipeline_approved` 也是 false |

**「全部交付」的意思**（10-15）：鎖定包每一鏡都有一支取回的 take（clip）或一張首格（still），一份 QA 收據，一個 D 軌資料夾（418 個）。它**不**代表：實聽（ASR 旗標沒人聽過，`words_listened: false`）、口型（`lip_sync_verified: false`）、音樂／環境／擬音（M·A·F；D 軌只有台詞）、產線匯入（`clips import` 沒跑）、站主接受。回報時這幾項分開寫。

**審看粗剪**：交付之後的下一步，是照故事順序把 `picture-D-candidate` 與 provisional 接成一支實速審看版：同一鏡有 t1、t2 照索引的判定挑，站主裁定的優先（a02-s028 用 t2、a03-s074 用 t1）；still 照 D 軌的停留；cut 從來源切；標明候選、不是成片。站主實速看過之後，實聽、口型與 M·A·F 才開始。到 10-15 交接時本集還沒做這一步。

**整理資料夾**：站主要「整理起來」時，在 `<VIDEO_WORKDIR>/` 下建一個以集名命名的資料夾，用 NTFS 硬連結（不多占空間、在那裡刪檔不影響原檔，但**原地編輯會連原檔一起改**），分「首格與still」「影片」「D軌候選-含台詞」「舊素材」，附 `索引.csv`（鏡號、類型、take、判定、秒數、收據、原路徑）與 README。帳本、收據、D 軌都綁原路徑，所以整理只能是連結。這一集 1,311 個檔（454＋435＋342＋80），重跑同一支腳本即可更新（補十九）。

**最後的帳**（帳本 `totals()`，10-15 讀）：全域 36,721／38,000；A 期 19,973／26,980.8（含 Codex 試拍的 475）；B 期 17,223／21,753.6；修圖 1,734／1,803；未結 0；供應商餘額 24,804（補二十）。收工回報這幾個數字、上面「不代表」的那幾項，以及每一筆 unknown 是怎麼關的。
