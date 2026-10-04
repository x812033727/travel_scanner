# 無歸箭｜長篇漫劇企劃包（期一，2 季 24 集）

幽皇死後一年，他的女兒帶著幽都的老弱跪在三宗盟門前求收容，懷裡藏著一支能毀人元神的詛咒之箭。白衣謀士沈歸鶴明知是局仍把她留下，怒目佛寂聞為此與他決裂；一個求死的書生、一個自罰的匠師、一個不知道母親是誰的海外少年，將決定這支箭最後射向誰。

本包分類為 **`anime`（動漫）**，畫風預設 **`anime-2d`**，題材 `custom`、群像 `ensemble`。共 **2 季、每季 12 集、期一 24 集**，**開放結局**（三條謎團保留給續期）。它的形狀照 [`borrowed-dawn`](../borrowed-dawn/README.md) 的企劃包，但集數、季數與結局政策不同。

## 原創聲明

本劇取材經典布袋戲「魔女入盟—詛咒之箭—鑄劍—智星軍師—機龍」的三段式故事結構，**人名、門派、地名、神兵、經書、招式、造型與台詞全部原創**，不借用任何既有作品的名稱、角色或台詞；原型裡拖戲的支線不排進 24 集。這份包不列任何與既有作品的對照表，外觀提示詞只描述原創的偶戲式華麗古裝。

## 閱讀順序

1. [設定集](setting.md)：九洲四地、五條核心規則與代價、三宗盟／幽都三派／赤淵宮／扶瀾國、20 位人物、12 條長線謎團、時間總帳、敘事約束與畫面基調。
2. [兩季總綱](outline.md)：賭注從個人到門派到天下，再回到個人的升級曲線。
3. 分季細綱：每集冷開場鉤子、兩段高張力、懸念、五段張力、埋回與連貫狀態。
4. [連貫性與伏筆帳](continuity.md)、[逐集狀態 CSV](continuity.csv)。
5. [自審紀錄](review.md)：張力曲線、懸念類型交錯、每 4 集回收、砍掉的支線。

| 季 | 集數 | 細綱 | 主題 |
| --- | --- | --- | --- |
| 1 | 1–12 | [無歸箭](season-01.md) | 用謊言保護人，和用真話害死人，哪個是善 |
| 2 | 13–24 | [智星](season-02.md) | 兩個最聰明的人對弈，棋子是朋友 |

## 來源與格式

[plan.json](plan.json) 保存分類、時長、影片預設與製作支援差距；[authoring-contract.json](authoring-contract.json) 定義 20 個人物 ID、12 條謎團 ID 與排程、每集欄位、懸念類型、結局政策與八條不得改寫的規則；[setting.json](setting.json)、[season-01.json](season-01.json)、[season-02.json](season-02.json) 是細綱來源。Markdown、`outline.json`、`documents.json`、`continuity.*` 與 `manifest.json` 全由 `build.mjs` 產生，不手改。

每集 `high_tension` 有前、後半兩段具體事件、賭注與延續後果；`setups`／`payoffs` 引用長線謎團，`general_payoffs` 記錄當集已完成的具體成果，讓每 4 集至少收一個東西而不必提早揭長線；`state` 分開時間、已知資訊、人物狀態、證據與接續。五段 `tension` 是企劃評分，不是觀眾反應或實測時間。

## 單集長度與集數的理由

| 問題 | 決定 | 依據 |
| --- | --- | --- |
| 一集多長 | 正文 22 分鐘，播出時段 30 分鐘（OP/ED 3 分鐘、保留 5 分鐘） | 站主要 20–30 分鐘；`long-anime-v1` 的企劃匯入路線只驗 22 分鐘這組數字，沿用省掉改程式 |
| 一季幾集 | 12 集一季，期一兩季 24 集 | 原型兩部各約二十餘集、每集近一小時，砍掉拖戲後約壓成五到六分之一；12 集一季是 repo 唯一長篇範例的形狀 |
| 效果 | `anime-2d`，人物設計走偶戲式華麗古裝：高冠、長髮、繡袍、詩號出場字卡、武戲用氣勁與定格 | 對應布袋戲動漫化的質感，但不用任何既有角色造型 |
| 語音 | 國語；每角色固定一個聲音，說書人另一個 | repo 的 TTS 只有國語路線 |

每集節奏：冷開場鉤子不超過 20 秒、四幕各約 5.5 分鐘、前半與後半各一段高張力、最後一句是懸念、相鄰兩集懸念類型不同、每 4 集至少收一個伏筆。

## 成本估算（企劃階段，不是帳本）

依 `animation-production` skill 的 3 分鐘 60 鏡估價按 22 分鐘約 440 鏡等比放大，Veo 3.1 Lite：

| 畫面等級 | 一集一次過 | 一集到重拍上限 | 24 集一次過 |
| --- | ---: | ---: | ---: |
| clips（全片段） | 約 US$360 | 約 US$780 | 約 US$8,600 |
| hybrid（四成片段） | 約 US$190 | 約 US$440 | 約 US$4,500 |
| stills（一成片段） | 約 US$100 | 約 US$270 | 約 US$2,400 |

全片段一集約 3,500 片段秒，超過預設月配額 3,000 與單片上限 US$200。建議先以 **hybrid** 做第 1 集試播測成本與畫風，再決定等級。

## 製作差距

- **單集長度**：`SeriesIn` 普通漫劇只接受 1–8 分鐘；22 分鐘要走 `long-anime-v1`（`anime` 分類、`anime-2d`、`custom`、`ensemble`、`runtime_spec`），不得改用 `story` 或 `flat-explainer` 繞過，也不得縮成 3 分鐘短漫劇。
- **群像節奏**：`custom` 題材的工人節奏規格要求每集 `hook_type`、`lead_arc` 與至少兩個爽點；本劇以兩段高張力與季末翻轉代替，未假填爽點欄位。
- **開放結局**：`long-anime-v1` 的企劃匯入路線綁定 22 分鐘正文與封閉結局的契約；本包是開放結局的期一，匯入前要確認政策是否接受 `open_ended: true`，否則只能當唯讀企劃。
- **預算與配額**：見上表；hybrid 等級與月配額要在試播後定案。

`production_support` 的四個狀態（`ready_for_import`、`admin_series_created`、`media_generated`、`published`）全部維持 `false`。本包沒有建立後台作品、沒有 POST series-request、沒有生成設定圖或片段、不動 `apps/`。

## 本機重建與驗證

在 repository 根目錄執行；指令只讀寫這個企劃目錄，不呼叫模型、正式站、匯入 API 或媒體供應商：

```bash
node docs/videos/series-plans/no-return-arrow/build.mjs
node docs/videos/series-plans/no-return-arrow/validate.mjs
node --test docs/videos/series-plans/no-return-arrow/validate.test.mjs
node docs/videos/series-plans/no-return-arrow/build.mjs --check
npm run check:tasks
```

`build` 從 JSON 來源產生設定集、總綱、分季 Markdown、文件包、連貫 CSV 與 SHA256 manifest；修改來源、README 或 review 後都要重建，`--check` 會在衍生檔與來源不符時失敗。`validate` 檢查集數、引用、兩段高張力、懸念類型交錯、埋回排程、保留謎團與開放結局政策；它不能證明 22 分鐘劇本完整、觀眾張力、媒體品質或法律上的原創。

交付後站主要決定的：先做第 1 集試播用哪個畫面等級；要不要把 24 集改成 20 集（每季 10）。
