# 第 1 集〈我重生了，面板卻是二手的〉開拍鎖定包（P7，等站主確認）

照 `animation-preproduction` 的規矩，這是花任何錢之前唯一一次整體確認。站主點頭之後鎖定檔生效（代理已先用 `plan_lock.mjs --write` 寫出 [e001-plan-lock.json](e001-plan-lock.json)，站主要改任何一項就改完重寫），之後設定圖、配音、關鍵影格、小樣、批量照包做，改動一律走變更單。

數字的來源：**工具規定**（`shot_plan.mjs`、`plan_lock.mjs`，2026-10-28 跑）、**實測**（《種田娶妻打天下》第 1 集 3D 國漫版與《修仙獎勵》鎖定包引的收據）、**推算**、**編輯判斷**。沒標的就當沒驗。

## 0. 站主的決定（2026-10-28，本 session）

1 題材：都市重生系統（避開古裝修仙，換一個觀眾群）；故事核心 A「二手重生系統」。2 畫風與路線：3D 國漫 CG，片段在 Colab 的 GPU 跑開源 H3（跟《修仙獎勵》同一條），設定圖與關鍵影格走產線 `look`／`keyframes`。3 規模：第一季 6 篇 × 12 集，這一輪交企劃包加第 1 集製作檔。

這一包裡還要站主點頭的：

| # | 事 | 建議 | 為什麼 |
| --- | --- | --- | --- |
| 1 | 片名 | 《我的重生系統是二手的》 | 把梗寫在名字上，跟《我的修仙獎勵是不是發錯了？》同一種「系統有問題」的片名味；備選《重生系統請勿二手轉讓》《前任重生者沒刪乾淨》 |
| 2 | 第 1 集集長 | 約 89 秒（lint 估法；真人語速約 98 秒），不是細綱寫的 100 秒 | 《修仙》第 1 集 92 秒、《種田》80–140 秒；小樣看過留存再決定要不要拉長 |
| 3 | 聲音 | 周野 Orus、周岸 Achird、林晚秋 Autonoe、老柯 Rasalgethi、王經理 Algenib、趙強 Zubenelgenubi、面板 Umbriel；旁白 Sulafat | 代理的建議，試片前照 `voice-audition.md` 試聽再定 |
| 4 | 小樣 | s29–s31（林晚秋從車底滑出、滑走合約夾、抬眼的特寫） | 一次驗女主身份、三人同框的全景、道具位移、說話鏡與顏值鏡；不過就改設計不花整集 |
| 5 | 三十二歲的周野 | 另一個角色 id `zhouye32`（同一張臉老十年），只在前 6 鏡 | 兩張設定圖比一張便宜太多；judge 的 identity 題也才答得了 |

## 1. 製作條件卡（P0）

| 格 | 值 |
| --- | --- |
| 作品 | 《我的重生系統是二手的》第 1 集，`docs/videos/ershou-chongsheng-e001/` |
| 路線 | 片段：Colab GPU 開源 H3（Turbo LoRA 版，1344×768、4 秒）；設定圖與關鍵影格：站上產線 `look`／`keyframes`；鎖定檔的正文用 `--route hailuo --hailuo-model h3` 的 H3 格式（跟《修仙》一樣，Colab 的 H3 讀同一種正文） |
| production profile | 沒有：外部片段 `clips import` 收得進來（`plan_lock --ready` 的 `import.profile` ok） |
| 交片規格 | 1920×1080（Colab 輸出 1344×768，`assemble` 放大，畫質沒驗）、CC 軟字幕、面板剪接時疊（`overlays.json`） |
| 預算上限 | Colab compute units（見第 6 節）；伺服器端 look／keyframes／音樂上限 US$22.83（工具規定）；若站主改走海螺網頁，上限 3,768 點加一成預留 |
| take 上限 | 首格 3、片段 2（工具規定） |
| AI 潤飾 | 關（`--assist off`，跟《種田》《修仙》一致；Colab 路線沒有這個選項，寫著是為了鎖定檔） |
| 期限 | 無 |

## 2. 分鏡表與製作規格（P4）

- H3 正文與點數：[e001-shot-plan-hailuo.md](e001-shot-plan-hailuo.md)（`shot_plan.mjs --route hailuo --plan hailuo:pro --hailuo-model h3 --resolution 2k --pilot s29,s30,s31 --strict`，結束碼 0）
- 伺服器路線對照：[e001-shot-plan-server.md](e001-shot-plan-server.md)
- 給人讀的中文分鏡表：`docs/videos/ershou-chongsheng-e001/storyboard.md`；英文提示詞在 `video.json`；面板文字在 `overlays.json`

42 鏡：片段 39、靜圖 3（s12 圖紙、s18 樓梯、s25 合約第三頁三個插鏡）、切素材 0。四段：雨夜 6 鏡（5 個鏡位）、醒來 12 鏡（9 個鏡位）、車行 18 鏡（9 個鏡位）、二手 6 鏡（5 個鏡位）。

離線檢查（2026-10-28，都不花錢）：

| 檢查 | 結果 |
| --- | --- |
| `node tools/video/cli.mjs lint --slug ershou-chongsheng-e001` | 0 錯誤、1 警告（claims.md 沒有來源：虛構劇集，照《種田》《修仙》不寫） |
| `drama_craft_check.mjs` | 30 列全過：中位數 2.0 秒、前 10 秒 5 鏡、前 30 秒 15 鏡、臉 57%、插鏡 12%、全景 19%、第一句台詞 0 秒 |
| `shot_reading.mjs --route hailuo --strict` | 42 鏡、0 陷阱 |
| `shot_plan.mjs --strict`（H3） | 風險 A 19、B 20、C 0；沒有「會白花」 |
| `plan_lock.mjs --check` | 和鎖定一樣 |

## 3. 風險分級與重設計（P5）

- **C 級 0**。改掉的：s06「吞掉」改成「填滿」（eat-drink 誤讀）、s39「筆跡」改成「一道模糊的光」（text.readable）、s26「抬眼離開紙頁」改成「抬起目光」（hands.small-prop）；合約的「翻頁」做成靜圖插鏡 s25（已翻到第三頁、手指按著），「抽走合約」寫成一手平推滑過櫃檯（s30）。
- **B 級 20 鏡裡 9 鏡是 speech.visible-mouth**：說話的人在臉的景別裡。這是站主 10-16 的規矩（說話鏡頭一定要動嘴），不照 shot-risk 改成聽者鏡；《種田》第 1–30 集都這樣拍。
- s02 雨水「流下」、s03 水窪漣漪、s15 眼裡的反光（physics.fluid B）：首格就畫好雨與反光，片段只做一點變化。
- s11、s24 微小反應（B）：寫了幅度與結束狀態（下顎慢慢收緊、笑容一角抽動）。
- 畫面裡的字：手機螢幕只寫 glowing、合約與圖紙寫 blank；面板全部在 `overlays.json`。

## 4. 動態分鏡（P6）

文字卡版要 `animatic.mjs --file video.json`，這個 session 沒有跑（沒有 workdir 與 timeline）；配音錄完再出關鍵影格版給站主看 storyboard 關卡。

## 5. 小樣計畫

- **三鏡**：s29（全景：林晚秋從車底滑出坐起，三人同框，B cast.three）、s30（中景：她一手把合約夾滑過櫃檯、說「這合約，我留著」，說話加道具位移）、s31（特寫慢推：抬眼看周野、一邊嘴角先笑，顏值鏡，王經理畫外）。同一場連續三鏡，一條路線一個模型一個檔位。
- **點數**：Colab 三支約 1–2 CU（推算：xiuxian 的 colab README 寫一支 12 秒約 1 CU，本 repo 沒量過）；若走海螺網頁一次 144 點、上限 288。
- **目的**：身份（林晚秋、老柯、王經理跟設定圖同一張臉）、主動作（滑出坐起、滑夾子、抬眼笑三件事各做完）、兩鏡之間剪得起來（s29 → s30 她站起來的位置連得上）、首格 PSNR ≥ 35 與匯入。
- **失敗條件**：任一鏡兩個 take 都壞在手與道具（多一隻手、夾子變兩本）、s30 嘴不動、s31 的笑變成鬼臉；或三人同框的全景裡任何一張臉走樣。失敗就改設計重鎖，不放量。
- 另一家比較：不做。

## 6. 預算

| 項 | Colab＋產線（站主定的路線） | 海螺網頁（對照，鎖定檔的點數基準） | 伺服器片段（對照） |
| --- | --- | --- | --- |
| 設定圖 8 張（zhouye、zhouye32、zhouan、linwanqiu、laoke、wangjingli 各 2 候選…） | look 約 US$1.1（最壞 2.1） | 約 120 點（《種田》12 張 241 點，實測換算） | 同左欄 |
| 首格 42 張＋judge | keyframes 約 US$5.6（最壞 16.9） | 約 990 點（《種田》第 1 集 35 張 780 點，實測換算） | 同左欄 |
| 片段 39 支 | 約 15–20 CU（推算：157 秒，一支 12 秒約 1 CU）；Colab Pro+ 月額另算 | 一次 1,884、期望 2,552、上限 3,768 點（工具規定） | 一次 US$23.40、期望 31.68、上限 46.80 |
| judge、音樂 | 約 US$1（最壞 2.4） | — | 同左欄 |
| **合計** | **伺服器端一次 US$8.43、上限 US$22.83（工具規定）＋約 15–20 CU** | **期望約 3,700 點，上限約 4,900 點，加一成預留約 5,400** | **一次 US$31.8、最壞 US$69.6** |

《修仙》第 1 集 45 鏡的鎖定包期望 3,900 點；本集 42 鏡 3,700 點，對得上。

## 7. 批次順序與停損

1. 設定圖 → look 關卡（站主看臉；zhouye 與 zhouye32 要像同一個人）。
2. 配音 `tts` → `check-audio` → audio 關卡；用錄好的 `timeline.json` 重跑 `shot_plan --timeline` 看買的秒數有沒有變（s15 現在買 5 秒，其餘 4 秒）。
3. 首格 42 張 → 關鍵影格版動態分鏡 → storyboard 關卡。
4. 小樣 s29–s31 → 站主看過才往下。
5. 其餘依場：車行（鏡位最多）→ 二手 → 醒來 → 雨夜；每場先母鏡頭、再 B、A；第一場做完用 animatic 換進素材實速看一次。
6. 停：同一鏡同一缺陷兩次、到 take 上限、結果不明（先查 Colab 的 progress.json 與餘額，不重按）、花到期望值。停的是那一鏡。

## 8. `plan_lock.mjs --ready` 的結果（2026-10-28）

程式查得到、現在還沒做到的（製作中要完成）：script 關卡 missing、look／audio／storyboard 關卡 absent、timeline 還沒錄（買幾秒是估的）、42 張關鍵影格還沒畫。`import.profile` ok。

人工打勾（送第一支之前）：Colab 帳號已配對（`minimax-h3-colab` 的 bootstrap）、compute units 餘額、`h3/first-frames/<id>.png` 放的是通過 judge 的關鍵影格、正文 SHA-256 等於鎖定檔、收據檔與停損規則、`drama_preflight.mjs --stage clips` 沒有 refuse。

## 9. 還沒驗的事

- 3D 國漫 look 的 `look.style` 原句沿用《修仙》，場景字（雨夜、車行、玻璃帷幕）寫在每鏡 prompt；現代都市的設定圖還沒出過圖，站主要看臉。
- 面板的青綠色框只在 overlays.json 寫了文字，剪接樣式（像舊手機系統更新畫面、右下角「使用者：2／2」的小字）還沒做，要在 `assemble` 時照《種田》的 panel 樣式改色。
- 聲音七個都沒試聽。
- Colab 開源 H3 的畫質與一致性、一支扣幾 CU，本 repo 沒有實測；小樣就是在量這件事（跟《修仙》第 1 集同一個未知）。
- 預期 take A 1.2、B 1.5 是編輯判斷；第一集做完用收據回填。
- 鏡頭中位數 2.0 秒，在目標下緣；小樣後覺得太碎就把 s03／s04、s38／s39 合併。
