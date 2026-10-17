# B18＋後五集：每片 US$5 執行限額的唯讀交接

## 結論

截至本次 fresh `origin/main = ebcba1caaa8db3e7be082afad62ba970962b3f10`，共用帳本已由 PR #1508 合併，但 **六片各 US$5 尚未實作**。目前 B18-v2 是 US$25 帳戶；五個 follow-on slug 不在預算保護集合。單改故事企劃、全域媒體 cap 或 `models.py` 清單，都不能形成這次要求的 US$5 all-in 限額。

本報告不是新報價或付費核准。**六片合計 US$30 的核准仍待使用者回覆**；每片不能借用另一片餘額，既有成本也不能歸零。本次只有本機/Git/GitHub 唯讀調查，沒有執行測試、主機操作或付費請求。

| 本次精確影片 | main 現況 | 待核准後的目標 |
|---|---|---|
| B18 `story-conveyor-belt-sushi-v2` | 固定 US$25 | US$5 all-in，保留既有操作與費用 |
| A29 `story-five-lego-legoland` | 不受此帳本保護 | US$5 all-in |
| A16 `story-five-costco-hot-dog` | 不受此帳本保護 | US$5 all-in |
| A37 `story-five-adidas-puma-brothers` | 不受此帳本保護 | US$5 all-in |
| B14 `story-five-ajinomoto-chip-film` | 不受此帳本保護 | US$5 all-in |
| A21 `story-five-pringles-vat-case` | 不受此帳本保護 | US$5 all-in |

原 `story-conveyor-belt-sushi`、A01 原版及 A01-v2 應維持原 US$25 保護；本方案不把舊 B18 原版當成第七片，也不更動 A01 已核准範圍。

## 已有實作與真正缺口

1. **共用帳本已完成基礎。** `video_budget/service.py` 鎖住每片帳戶列後預留；`reserved`、`uncertain` 都按完整上限占用；settle、冪等 operation ID、超額停送及具證據 reconciliation 已存在。延伸此機制即可，不需要另造批次帳本。六個獨立 US$5 帳戶自然令此批帳本合計最多 US$30，仍須逐片核對既有成本與保留額。
2. **金額不能只改清單。** `models.py:33–51` 的 default 和 DB constraint 都是 25；`service.py:92`、`:333` 又要求實存帳戶必須正好等於 `PILOT_LIMIT_USD`。直接寫 5 會被 DB 或 service 拒絕。`service.py:210` 的超額文案也固定寫 25。
3. **五集的 API routes 尚未進入保護。** `is_pilot` 只認四個舊 pilot，所有現有 speech/media/Jev/model gate 都經這個共用判斷。加入五集後可沿用現有路由保護；不需要為每個 handler 再造一組帳本。
4. **三個 Node client 都有自己的四片清單。**
   - `tools/video/tts/client.mjs:15,186`：只有四片會附 `video_slug` 與一次邏輯請求的 UUID。未延伸時五集 TTS、transcribe、speech judge 的請求沒有此歸屬。
   - `tools/video/media/client.mjs:115–157`：只有四片 judge/locate 帶 operation ID，且 generation/judge/locate 採一次送出、未知結果停住的路徑。
   - `tools/video/automation/client.mjs:34,337–346`：只有四片的 story writer/checker/listener 一律走 durable jobs；只擴 API 集合會令五集仍走同步路徑並被 `video_pilot_durable_required` 拒絕。
5. **audition 若包含在 all-in，需同步。** `tts/cli.mjs:251–285` 只從四個 pilot slug、A01/B18 名稱及 pilot-v2 路徑強制歸屬。擴集合後精確 slug 路徑可自然受保護，但 `A29` 等人類編號路徑仍需對應本片或明確拒絕缺少 `--slug` 的六片 audition。不能將其當一般頻道免費樣本。
6. **讀值介面可重用。** `video_media/admin_api.py:208` 遍歷集合並輸出實存 limit/reserved/settled/remaining；`reconcile_cli` 亦經共用 service。無需新 API、BFF 或管理介面。將固定「四個試作／25美元」提示與操作文件改成實際受保護片及限額，避免錯誤交接即可。

## 最小建議變更範圍（尚未認領或編輯）

| 類別 | 必要檔案/內容 |
|---|---|
| 帳戶契約 | `apps/api/app/video_budget/models.py`：明確 slug→Decimal cap 對照；保留既有命名 alias 亦可。DB constraint 容許新限額但不得以任意 DB 值放寬授權；service 必須驗對照值。 |
| 共用服務 | `apps/api/app/video_budget/service.py`：`_locked_account`、`summary` 對每片期望值檢驗，超額文案用實際 cap；reserve/settle/uncertain/鎖和冪等語意保留。 |
| 新 migration | main 現在 head 為 `0132_video_pilot_budget`。新增接此 head 的 migration（編號先依當時 fresh main 重查），**不改歷史 0132**；變更 constraint、seed 五片各 5、只把 B18-v2 改 5。原操作表、reserved/uncertain/settled、舊 pilot 帳戶不刪不重建。 |
| Node 傳輸 | `tools/video/{automation,media,tts}/client.mjs` 精確延伸五個 slug；可維持三清單並以集合一致性測試約束，或經審查提取共用常數。 |
| audition | `tools/video/tts/cli.mjs` 補五集編號／路徑歸屬與有界錯誤提示；若本批明確不做 audition，可先把它排除於執行 allowlist，但不能聲稱未修改的 generic audition 會自動入帳。 |
| 一致文案 | `video_budget/recovery.py`、`video_budget/RECONCILE.md`、`video_media/admin_api.py` 的「四個／25」文字需同步。這不是新增昂貴路由或重新定價工作。 |
| 測試 | `test_video_pilot_budget.py` 加逐片 5／舊片 25／migration；三個 client `.test.mjs` 加新 slug 的 paid attribution/durable/未知結果；tts client 測試已有 audition 測例可擴。對現有 API route tests 做有限參數化，證明六片 media/speech/Jev/model 都走現有 gate。 |

**B18 降額的必要處理：**部署前唯讀讀出 B18-v2 的實際 settled＋reserved＋uncertain 與是否有在途工作；已花的錢照算，舊 hold 不釋放。若總暴露已超過 5，或未知結果仍未釐清，就不能宣稱符合 US$5 或重啟付費；先保留停用狀態交 root 處理。不能藉 migration 歸零、另造 slug 或把限額當「新增 US$5」。本次未碰主機，沒有對 B18 現有餘額作任何判斷。

不需要修改故事正文、row sources/claims、renderer、paid price 表、既有保護的所有 handler，也不需要開新通用預算 UI。現有 `PRICE_VALID_THROUGH=2026-12-31` 尚在本次日期內；未知模型/未定價路由仍應 fail closed，訂閱文字路線仍沿既有選擇，不另要求帳戶餘額。

## 最小驗證清單

- 六個精確 slug 各 limit=5；A01 原版/v2 與 B18 原版保持 25；未列 slug 保留既有行為；API/Node 保護集合一致。
- settled＋reserved＋uncertain 累計正好 5 可成立，再多 0.000001 必須送出前拒絕；一片額度不能補另一片；已知費用超過 hold 照記並停後續。
- 相同 operation ID 不重買；未知價格、價格失效、timeout/遺失回應、尚未解決 hold 都維持既有拒絕/保留語意。
- 六片的 TTS/transcribe/judge 都帶 slug＋固定單次 UUID；media judge/locate 同理；story verifier/listener 走 durable jobs。未取得可確定結果時不能改新 UUID 重送。
- 新 migration 的 offline SQL 及真 PostgreSQL upgrade：既有 0132 資料、操作及其他帳戶全保留；重複執行有界且不擴額；不得把 downgrade 變成不經授權擴回 25。
- 真 PostgreSQL 兩 session 同時向一片 5 元帳戶各 reserve 3，只能一個成功；六片各自獨立。原測試 `test_postgres_row_lock_prevents_concurrent_over_reservation` 已具模式，標記 `RUN_INTEGRATION_TESTS=1` 才會執行，普通 SQLite 通過不能冒稱並發驗證。
- 根據實際變更跑 scoped pytest、Node test、Ruff/mypy 與 migration CI。合併/部署後再以既有唯讀 ledger 每片讀回 5 與真 exposure，完成授權和稿件關卡後才開始付費。

## 任務／分支／PR 持有人

| 工作 | 本次查到的狀態 | 對下一步的影響 |
|---|---|---|
| `2026-10-14-enforce-usd-25-all-in-cap` | main 仍 `in-progress`；owner `codex-story-budget-cap`；local `+ codex/story-pilot-usd25-cap-20261015` 位於 `worktrees/story-budget-cap/travel_scanㄐ`，HEAD `2b4591064...`，乾淨；remote head 已不存在；#1508 已於 2026-10-15T04:37:20Z 合併成 `42fbfb40d...` | 共同預算目錄及主要 clients 的正式 claim 還在，且 worktree 實存。已合併不等於可以代釋放。root 應先協調該持有人/處理現有票的剩餘 live 驗收，再對後續票正式擴 scope/接手。 |
| `2026-10-15-extend-all-in-video-budget-to` | 目前工作分支有檔，`open`、無 owner，僅 scope models.py＋test_video_pilot_budget.py；屬 open #1510 分支，**尚不在 origin/main** | 已有後續票，不需重開。需在其整合時把 B18-v2 5 元、六片總 30 的待核准範圍與上述真正必要檔案寫清楚；舊「正常5、可能25」提案文字已不符本次硬上限目標。 |
| `2026-10-12-play-the-channel-intro-bumper-after` | 票仍 review、owner `claude-opus-5-5-bumper`，涵蓋 tts/cli；branch 本機/remote 均不存在，對應 #1481 已合併 | 這是殘留 claim 證據，不能當正在開發的新功能；此唯讀調查未釋放。若要改 audition，仍由 root 依看板協調。 |
| #1387、#1379 | 仍 open draft，分別碰 `tts/check.mjs`／`tts/speech-journal.mjs` | 現有 clients 傳識別路徑已可用，不需改這兩個並行 PR 持有檔。 |
| 目前全部 42 個 open PR | 核對 budget 目錄、budget 主測試、migration 目錄、三個 client 與 tts/cli：**無 core overlap** | 沒有另一個已開 PR 正在交付六片 5 元實作。#1502 是 monthly-draft-cap 驗證票，不是本片 all-in cap。 |

## 建議交接順序

1. 保留既有五集 prepared 成果；本報告放在其外，不重建/變動 frozen 作品。
2. root 協調仍持有範圍的 cap owner，確認後續票具體 scope；不要因本報告而自行釋放別人 claim。
3. 在現有後續票實作上述最小差異及測試，可先免費完成可審查 PR；不由本報告授權合併/部署/付費。
4. 使用者回覆精確 US$30 批次／各 US$5 後，依正式部署規則、現有內容與 pilot 驗收順序，做逐片 ledger readback 及有界啟動。核准未回覆時維持免費備料。

## 證據與限制

- 結構化證據：`B18-five-usd5-enforcement-audit-20261016.json`，SHA256 `79867796ec5a9e2d283c2829d124e53610566651a163cbe5a05bfd258079cdb9`。含 12 個 code/task blobs 的 main/local pins、main ref、migration 清單、worktrees、42 PR 篩查與 #1508 merge receipt。
- 原生 task-board 唯讀 survey：`B18-five-usd5-ownership-survey-20261016.json`。所有相關 code 本機與 main 除 CRLF 外相同；沒有依未合併本機 runtime 差異推論。
- 本輪沒有測試執行結果，也沒有 live DB/worker 檢查。建議驗證項不是已完成清單。看板 claim 與分支存在證明範圍佔用，不能證明持有人此刻正在執行。
