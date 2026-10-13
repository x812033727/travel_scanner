# 首集關卡與預算檢查（2026-10-09）

**本文件保留 17:37 UTC（台北 01:37）的歷史檢查，後續採用由獨立決策收據接續。** 採樣當時使用者對預算問題只答「使用hailuoai」，所以當時只確認路線，未寫具體預算或 P7 採用。

檢查後，使用者已明確答覆「**採用素材與 v4，按此點數上限鎖定 plan**」。root 提問範圍是：採用 146 張素材與 v4、本期現有 Hailuo 額度最多 **26,980.8 點**含預留、三鏡小樣最多 **316.8 點**且已包含在本期上限、第二期有額度才繼續、**不購點／不續訂／不扣 API，look 保留待處理**。root 負責另存 adoption-decision 收據，綁實際問題／回答、素材 manifest、預算與實際寫出的 lock。本文件不宣稱後續 lock 已寫，也不把上述授權擴大到 API 或續費。

完整來源 SHA、命令、逐項 readiness 與 API 時點資料在 [JSON 收據](gate-preflight-20261009.json)。外部原始診斷保存在 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/adoption/20261009/`；沒有覆寫原 v4 檢查證據。

本次實跑 `plan_lock --ready --json`，讀 v4 `video.json`，工作目錄指向正常 `<VIDEO_WORKDIR>/ou-de-jianghu-e001`。2026-10-09 01:37 台北時間，**exit 1，通過 1 項、未通過 429 項**：

| 項目 | 未通過數 | 意義 |
| --- | ---: | --- |
| script／look／audio／storyboard | 4 | 尚無本次來源的有效關卡核准 |
| timeline 綁定 | 1 | 尚無錄音實測時長，買秒數仍為估算 |
| keyframes 綁定 | 1 | 尚無本次 look／畫面對應的關鍵影格 manifest |
| clip 首格 | 420 | 420 支待買素材尚缺合格首格 |
| 計畫末格 | 3 | 三鏡末格待製作 |

通過的是外部片段 profile 條件：目前沒有 production profile；這不等於片段已匯入或全部前提已通過。455 鏡中另有 30 still 和 5 source cuts，不能把 429 項誤讀為 429 個影片故障。這是開拍包階段的待製作清單；送出第一支付費片段前仍須把適用程式檢查全部通過。

此輪 root 同時授權另一代理離線匯入 9 張最新基底。**本次採樣時正常角色 manifest 尚不存在**，僅記該時點，不能推斷之後一直缺檔。離線匯入完成也只會新增 pending candidates；`choice`、judge、look approval 與正式模型使用證據仍是不同狀態。JSON 保存檢查前後檔案快照，`approvals.json`、`characters/choice.json`、`plan/lock.json` 均未被本檢查改動。

**P7 可以先於媒體完備，但不能先於具體開拍包確認。** [plan_lock 原碼](../../../../../../.agents/skills/animation-preproduction/scripts/plan_lock.mjs) 529–554 行的初次 `--write` 只拒絕「已有 lock 卻未給 force」或 `level=refuse` 的計畫，沒有要求 readiness 全綠；[前期 skill](../../../../../../.agents/skills/animation-preproduction/SKILL.md) 112–119 行明確把關卡、錄音與關鍵影格列為確認後製作的工作。`--write` 不會批准 look／audio／storyboard，也不會把 pending 圖變成採用圖。`--accept` 是既有 lock 的變更單接受，不是初次 P7。

本代理沒有執行 `--write`、`--accept`、`--judge`、choose 或 approve。後續具體授權已由 root 接收；root 可在相同來源／正常 episode 目錄，用相同規劃旗標加 `--write --assist off --note "採用素材與 v4，按此點數上限鎖定 plan"` 寫第一份 lock，再執行 `--check`。若已有別的 lock，先讀取並比較，不自動使用 `--force`。

v4 來源 SHA 為 `cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17`；v4 預算 SHA 為 `f62d04c4bbc99825d847a8818e1a0229e335f21f77f16598626e1d24741199a2`。以下是**原提案完整估算**；後續授權只涵蓋上面列明的現有 Hailuo 點數範圍，API／新訂閱金額未獲授權：

| 範圍 | 期望 | 上限 | 含 10% 預留的上限 |
| --- | ---: | ---: | ---: |
| 全集 H3 2K 點數 | 30,494.4 | 44,304 | 48,734.4 |
| 額度期 A：236 clips | 16,940.4 | 24,528 | 26,980.8 |
| 額度期 B：184 clips | 13,554 | 19,776 | 21,753.6 |
| 三鏡小樣 a02-s035～s037 | 240 | 288 | 316.8 |
| API 製作 USD | 98.7016 | 223.1652 | 245.4817 |

小樣一次全過為 144 點；每鏡最多 2 takes，不自動買第三次，先看小樣再放量。兩期配置各假設 27,000 點；A 期用滿 cap＋reserve 後只剩 19.2 點，不能承接未列追加。全集期望含預留為 33,543.84 點，超過單期 27,000 點；原生工具因此仍列額度 waste，不能稱單期足夠。

2026-10-08 預算調查以 Max 每月 USD 216 計算；若兩期都需新付，訂閱提案上限 USD 432，加 API cap＋reserve 的已知小計為 **USD 677.4817**。這不是結帳報價，也不包含內建 imagegen 未回傳的金額、稅費或已付訂閱成本判定。舊預算內 imagegen 103 項目標等數量保留為提案歷史，不能用來代替目前 146 張 unique 素材交付統計。

原生計畫這次重算的 clip 期望為 **30,304.8** 點，人工風險預算為 **30,494.4** 點；兩者 cap 都是 44,304。工具方案常數仍為 USD **199.99**（[episode_estimate](../../../../../../.agents/skills/animation-production/scripts/episode_estimate.mjs) 178 行），不得當作今日售價。原生 lock 只綁原生 totals，不會自動含人工風險、兩期 cap 或整套素材 receipt；未來正式採用需另綁這些原件 SHA，不能改寫 lock 數字假裝已由工具計算。

本次另在 **2026-10-08T17:37:27.681Z（台北 2026-10-09 01:37:27）** 成功只讀 GET `/api/video/media/status`：

| 伺服器狀態 | 實讀值 |
| --- | --- |
| drama media enabled | `false` |
| image provider / model | `gemini` / `gemini-3-pro-image`，configured=true |
| image 2K 計帳欄 | USD 0.134；狀態未宣告實際 output resolution |
| clip provider / model | `gemini` / `gemini-omni-1.1-flash`，1080p / 8s |
| 每集 API 上限 | USD 200 |
| judge 次數餘額 | 3,401（10,000 限額，已用 6,599） |

這些 API 配额不是 Hailuo 點數。[look import 原碼](../../../../../../tools/video/media/look.mjs) 240–245 行會在 `enabled=false` 時拒絕 judge，尚未進入 upload／付費 POST；因此目前能做離線候選匯入，無法誠實宣稱已過正常 judge／look。全片 API 提案 cap＋reserve USD 245.4817 又高於實際 USD 200 上限；本檢查未啟用路線、未提高上限，也未替使用者決定費用。

Hailuo 的新 UI 觀察由 root 持有獨立收據：2026-10-09 在 Chrome 看到 Max／27,000 點、H3 首尾幀／2K／16:9／4 秒／1 件，表單顯示 48 點；截圖在 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/final-art/20261009/qa/hailuo-preflight-20261009.jpg`。本 JSON 只標為 root 回報並綁截圖 hash，不冒稱本代理重新操作或曾扣點。上傳 API 有工具文件，尚未用實際首格測試；沒有送生成，沒有費用。餘額／表單報價不是預留點數，付費提交前仍要重查。

實跑命令如下；placeholder 由本機實際路徑展開，外部 execution 收據留有原始 argv、stdout、stderr、exit code 與時間：

```powershell
$node = '<BUNDLED_NODE>'
$videoWorkBase = '<VIDEO_WORKDIR>'
$normalEpisode = Join-Path $videoWorkBase 'ou-de-jianghu-e001'
$v4File = Join-Path $normalEpisode 'plan/preflight-20261009-v4/video.json'
$planFlags = @('--file', $v4File, '--workdir', $normalEpisode,
  '--route', 'hailuo', '--plan', 'hailuo:max', '--hailuo-model', 'h3',
  '--resolution', '2k', '--handle', '0.5', '--clip-takes', '2',
  '--expected-takes', '1.2,1.5,2', '--pilot', 'a02-s035,a02-s036,a02-s037')
& $node .agents/skills/animation-preproduction/scripts/plan_lock.mjs @planFlags --ready --json
```

`plan_lock --file` 的 `--workdir` 是 **episode 本身**，普通 media CLI 的 `--workdir` 是 **所有影片的父目錄**；[shot_plan](../../../../../../.agents/skills/animation-preproduction/scripts/shot_plan.mjs) 818–835 行與 [paths](../../../../../../tools/video/core/paths.mjs) 27–44 行可核對。不要把 lock 放在 v4 文件資料夾、媒體又放在正常 episode 後宣稱兩者自動接上。

`approve` CLI 只有 `--slug`，會讀 repo 正式來源，沒有 `--file`（[cli](../../../../../../tools/video/cli.mjs) 192–214 行）。v4 是外部工作提案，script.md 又綁來源目錄；需先完成來源持有人協調與 v4 screenplay 綁定。動畫 action／motion 會進 screenplay，所以「台詞、秒數未變」不等於可以借用原 script 核准。先前只讀 scope 稽核仍見 e001 與 production 各有 Claude 持票；時間久不等於已放棄，也未用票齡推斷 OS 工作停止。

後續最小順序是：完成當前授權的候選離線匯入並讀回 → root 保存已取得的具體 cap／來源包採用記錄 → 對齊 canonical／v4 關卡來源 → root 寫 P7 並 check。本次沒有 API 費用授權，所以正常 paid judge、look、錄音及 storyboard 仍保留待處理，不能因 P7 寫入便自動扣 API。首支付費片段前，仍須完成適用前提，再跑 ready 與人工上傳／表單／餘額檢查。正式素材採用、P7、look、音訊和 storyboard 各自保存真實狀態，不互相代填；原始 readiness stdout hash `074be56470476f03892c0b75d6c84d73cef41af91ac5d0bd1ffa0b337d5567a2` 保持不變。
