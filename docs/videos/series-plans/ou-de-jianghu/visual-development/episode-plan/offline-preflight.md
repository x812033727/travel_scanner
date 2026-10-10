# 第 1 集離線前置檢查收據

> **歷史基線，非目前製作提案。** 本頁保存2026-10-08首次對未改原稿的離線結果；下列451 clip、447 setup、10個程式C、歷史費率及「播放／冷看待執行」均屬當時狀態。現行可審交付請讀 [P0–P7 審閱包 v3](preproduction-package-v3.md)、[提案摘要與SHA](proposal-summary.json)及[獨立觀看紀錄](cold-review-independent.md)：v3已完成全長1倍速播放，v3.1另完成23卡停格複看。保留本頁原始數據與收據，不用後來結果覆寫舊證據。本說明於2026-10-09（Asia/Taipei）補訂。

2026-10-08。這份交付把現有第 1 集做成可審閱的分鏡表與文字卡 animatic，**尚未核准；本離線檢查未製作正常 look、配音、關鍵影格或動畫**。同輪內建 imagegen 已生成九人概念候選，見 [美術定調](../art-direction/README.md) 與 [第一集畫像](../episode1-portraits/README.md)，尚未匯入正常 look。本離線檢查使用既有來源，未改劇本、production policy 或 profile；付費請求 0，未寫 `plan/lock.json` 或 `--accept` 紀錄。

機器可讀的命令、退出碼、來源及產物 SHA-256 在 [offline-preflight.json](offline-preflight.json)。分場與人工小樣判斷見 [scene-and-pilot.md](scene-and-pilot.md)。此收據不能代替站主核准或冷看驗收。

## 本輪實際交付

完整大檔保存於 repo 外的 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261008/`；公共文件不記私人機器絕對路徑。

| 檔案 | 內容 | native exit code |
| --- | --- | --- |
| `shot-plan.json` | 455 鏡完整規格、H3 正文、雜湊、風險與歷史常數預算 | 1（strict：10 review、1 waste） |
| `shot-plan.md` | 同一計畫的可讀分鏡表 | 1（同上） |
| `ready.json` | 真實關卡、配音與首格缺口 | 1（未備妥） |
| `animatic.html` | 455 張文字卡、播放器與逐鏡表 | 0（HTML 成功產生） |
| `receipt.json` | 本機實際命令、來源雜湊與產物雜湊 | 寫入完成 |
| `verification.json` | HTML 結構、資產引用與雜湊核對 | 核對完成 |

HTML 成功產生不等於實速看過：本輪結構核對為 455 個唯一鏡號、0 圖片、0 影片、無音訊、無遠端資產 URL、0 非正鏡長；來源和產物 SHA 均一致。**瀏覽器播放與獨立冷看尚待執行**。未要求 `--mp4`，因目前沒有各鏡圖片。

## 可重現命令與工作目錄規則

本機初跑因缺 `pinyin-pro` 而失敗。依 `dev-and-ci` 在本 worktree 執行 `npm ci`，以 bundled Node **24.19.0 ARM64** 直接呼叫 npm CLI；exit 0，547 packages。安裝前後 `package.json`、`package-lock.json` SHA 未變，未執行 audit fix。後續四次命令均使用同一 Node。

以下 PowerShell 的 `$verifiedNode` 指已核對版本的 Node，`$videoBase` 是 repo 外所有影片的根目錄；不要指向本集目錄，因 `--slug` 會再加一層 slug。`shot_plan` 的檔案入口是 positional path，不是 `--file`；其餘兩支才接受 `--file`。

```powershell
$outDir = Join-Path $videoBase 'ou-de-jianghu-e001/plan/preflight-20261008'
$planArgs = @(
  '--slug', 'ou-de-jianghu-e001', '--workdir', $videoBase,
  '--route', 'hailuo', '--plan', 'hailuo:max',
  '--hailuo-model', 'h3', '--resolution', '2k',
  '--handle', '0.5', '--clip-takes', '2',
  '--expected-takes', '1.2,1.5,2',
  '--pilot', 'a02-s035,a02-s036,a02-s037'
)
& $verifiedNode .agents/skills/animation-preproduction/scripts/shot_plan.mjs @planArgs --json --strict
& $verifiedNode .agents/skills/animation-preproduction/scripts/shot_plan.mjs @planArgs --markdown --strict
& $verifiedNode .agents/skills/animation-preproduction/scripts/plan_lock.mjs @planArgs --ready --json
& $verifiedNode .agents/skills/animation-preproduction/scripts/animatic.mjs @planArgs --out (Join-Path $outDir 'animatic.html')
```

JSON／Markdown 命令的 stdout 保存為上表檔案；每次執行後立即記 `$LASTEXITCODE`。三支不呼叫付費服務；`shot_plan` 僅輸出，`plan_lock --ready` 只讀，`animatic` 寫指定 HTML。`--write`、`--accept` 未執行。

## 數量與路線：這一集沒有 production profile

| 項目 | 本次來源／工具結果 |
| --- | --- |
| 全部 scenes | 459 |
| shot | 455：clip 451、still 3、source cut 1 |
| 角色 | 9；現有 `look.candidates=3` 是來源設定，不是付款授權 |
| clip 的程式風險分級 | A 207、B 234、C 10；不是人工逐鏡簽核 |
| shot 所需秒數加總 | 1,385.62 秒（逐鏡欄位四捨五入後加總） |
| animatic 時間軸尾端 | 1,403.533 秒，畫面摘要顯示 1,403.5 秒 |
| 擬購素材總秒數 | 1,973 秒／每鏡一 take |
| 時長依據 | `estimateTimeline`，沒有錄好的 `timeline.json` |

兩個時長口徑不同：`shot_plan` 只加 shot 的 `need_s`；animatic 保留原 timeline 的起訖位置，包含非 shot 場景占用的時間。兩者都不是實際配音或成片時長。

e001 `video.json`、`series.json` 都宣告 `production_policy: long-anime-v1`，但 `series.json` 沒有頂層 `production.profile`。`clips import` 依目前 `tools/video/media/clips.mjs` 只在該 profile 存在時拒收外部片段；本集的 `import.profile` 檢查因此通過。**不要為了標示「製作版」加 `--production`**：規劃腳本會因此套用 profile 規則，誤將 Hailuo 路線及既有 still 判為不允許。未移除或修改任何 profile。

這只通過路線相容性的單項檢查；`clips import` 還需要目前來源綁定的配音 timeline、首格、keyframes manifest、storyboard 核准及媒體 QC，現在均未滿足。

## 歷史常數預算，尚未核准

費率來源為 `.agents/skills/animation-production/scripts/episode_estimate.mjs` 的 `PRICES`／`PLANS` 及 `shot_plan.mjs` 的 `HAILUO_MODELS`：catalog 標 2026-09-26、方案標 2026-10-03、H3 2K 12 credits/s 的帳號實測標 2026-10-04。**未在本輪查當日生成頁、帳號方案或剩餘餘額；不是 2026-10-08 的正式報價。**

規劃假設：Hailuo H3 2K，尾把手 0.5 秒，每鏡 take 上限 2，A/B/C 預期 take 1.2/1.5/2；風險乘數及 10% 預留是編輯判斷。`hailuo:max` 只用作歷史 27,000 credits／月及月費 US$199.99 的換算基準，不代表目前帳號是此方案或允許購買方案。

| 片段部分 | 一次 take | 工具期望 | take 上限 |
| --- | ---: | ---: | ---: |
| 全集 credits | 23,676 | 32,563.2 | 47,352 |
| 加 10% 預留的規劃數 | 26,043.6 | 35,819.52 | 52,087.2 |
| 歷史 27,000 月額占比（未加預留） | 87.69% | 120.60% | 175.38% |

期望已超過歷史一個月額度，所以 strict 回 `waste`。不能將單次 take 的 87.69% 當整集一定做得完；分批、降風險、跨月或額外成本都尚未形成核准方案。

工具另列伺服器端一次 **US$69.344**、上限 **US$203.984**，其程式只包含基底設定圖、關鍵影格及其 judge、音樂。**不包含 TTS、外部 clip judge、額外角色畫像／多視圖／表情／姿態／道具參照或稅費**，也不是全包預算。這些仍須另列數量、單價與預留；目前不可宣稱 P0 預算已鎖定。

## 小樣與風險不能只信正則

本次明列的候選是 `a02-s035` → `a02-s036` → `a02-s037`，三鏡連續 6.733 秒；按歷史 H3 最短 4 秒各買一支，共 12 秒。一次 144 credits；程式風險 B/A/A 算出期望 187.2、上限 288，10% 預留後分別 205.92／316.8。**這是未核准的候選，不是可立刻送出的清單。**

人工分鏡稽核已指出：`a02-s036` 掌與冠的接觸被程式漏判，應按 C 級處理；`a02-s037` 首格已分髮露印、動作卻再分髮，需要先釐清。若僅將 s036 的預期 take 從 1.2 改成 2，其他不變，小樣期望為 225.6 credits、含 10% 為 248.16；這仍只是人工修正試算，未改原始輸出或來源。小樣所需殷無聲已有概念候選，正式參照仍待備妥。詳見人工分場文件。

程式列出的 10 個 C 級 review 全在此小樣外：`a01-s083`、`a02-s030`、`a03-s037`、`a03-s039`、`a03-s050`、`a04-s015`、`a04-s053`、`a04-s090`、`a05-s032`、`a05-s072`。前三個已被人工標為可能的文字誤報，不能直接當作全部真 C；其餘也需逐鏡裁定、重設計或補適切小樣。原始 strict 結果完整保留，沒有為了 exit 0 改掉它。

## 開拍缺口與完成邊界

`plan_lock --ready` 共 458 項，通過 1 項（沒有 profile 阻擋）、未過 457 項：script `missing`、look/audio/storyboard `absent`、timeline 缺、keyframes manifest 缺，以及 451 個 clip 首格缺。另有提示指出沒有正常 plan lock。

後續順序是：人工裁定風險及小樣起始狀態 → 補齊美術與配音成本 → 播放與獨立冷看文字 animatic → 將具體包及目前有效授權集中交接。正常關卡、實際帳號／即時費率／餘額、瀏覽器上傳、H3 圖生影片及真實匯入均未在本輪驗證；未核准前不將本收據當作開拍鎖定。

本離線查核前，預設本集工作目錄不存在；本離線檢查僅在 `plan/preflight-20261008` 寫入產物，平行美術工作已在本集 `art-direction` 目錄保存概念圖。這不是對其他主機或其他私人工作目錄的全盤媒體搜尋，不能推論那些地方也沒有舊資產。
