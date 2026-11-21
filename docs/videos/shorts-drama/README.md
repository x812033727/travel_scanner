# Shorts 零台詞短劇的共用區

每一部無語音（零台詞）Shorts 短劇都適用的共用規則、分鏡與審劇本規範、成片品管流程與教訓。各系列自己的角色設定、固定笑點公式與集數規劃放在 [`series/`](series/) 底下的個別區；做過的集數學到的跨系列與單系列教訓統一放在 [`../lessons/shorts.md`](../lessons/shorts.md)。

這整個資料夾與 [`../lessons/shorts.md`](../lessons/shorts.md) 會由 [`../rules-sync/`](../rules-sync/README.md) 每小時自動同步到雲端硬碟 `AI/備份/AI劇/_共用規則/`、`AI劇/Shorts/_規則與教訓/` 與各系列的 `_規則與教訓/`。**正本只有這份 repo**，改規則或補教訓一律改在 repo。

| 檔案 | 內容 |
| --- | --- |
| [`WRITING.md`](WRITING.md) | **分鏡怎麼寫＆審劇本規範**：黃金五拍分鏡公式（11–16 秒、5–6 鏡）、單人框與 80% 鎖定機位、**9:16 介面安全區（Safe Zone）**與**無縫重播迴圈（Loop >100%）**、聲音三層設計（BGM、`music_off` 留白、物理音效打點）、第 0 關 AI 6 大系統性陷阱避險寫法，以及花錢前的**審劇本／審分鏡技術三道檢查**（含 `preflight.mjs` 與獨立審稿交辦範本） |
| [`PRODUCTION-ROUTES.md`](PRODUCTION-ROUTES.md) | **多引擎製作路線手冊**：Colab Qwen＋MiniMax H3（批次主力）、**Google Flow（Veo 3.1 網頁半自動，含雲端交接與無台詞音訊防護）**、網站後端 Veo 3.1 API 三條路線規格、混搭與省點數指南 |
| [`REVIEW.md`](REVIEW.md) | **四階段評分與審核機制**：**階段一** 企劃與分鏡 100 分三位獨立評審盲評（`preflight.mjs score-blind` 自動彙整、70 分門檻與滑走陷阱攔截）→ **階段二** 自動前檢＋技術審稿＋首格五項（含安全區）檢查 → **階段三** 成片 `qa_check.py`（疊安全區紅框）＋獨立畫面審核＋雙人成片笑點審核（平均 `≥ 3/5` 門檻）＋五級由便宜到貴修法與原審片人複審 → **階段四** 八語包裝、雲端備份、上架後 7／28 天數據覆盤與三點評分校準 |
| [`preflight.mjs`](preflight.mjs) | **自動化前檢／Flow 轉寫／盲評彙整 CLI**（零外部套件，隨 `npm run test:docs-videos` 跑單元測試）：`check` 檢查 `<slug>.json` 與 `edit/plan.json`、`export-flow` 一鍵產出 Google Flow 提示詞單、`score-blind` 自動彙整三位盲評 JSON |
| [`series/_template.md`](series/_template.md) | **新系列快速啟動範本**：開新無語音系列時複製填寫，5 分鐘套用全部共用規格、角色定妝錨點與前三支試片表 |
| [`../lessons/shorts.md`](../lessons/shorts.md) | **教訓**：2026-11-04 四系列 20 集五輪品管、35 鏡重畫與笑點重剪學到的實戰教訓，以及後續新增的教訓 |
| [`../SHORTS.md`](../SHORTS.md) | 後台 `/admin/videos?tab=shorts` 的三條內容線（AI 實測 `lab`、長片精華 `cut`、漫劇直式短篇 `drama`）、自動品管 13 項與月曆排程架構 |

## 系列個別區

| 系列 | 代號（`slug` 前綴） | 核心角色與關係 | 固定笑點機制 | 個別規則檔 |
| --- | --- | --- | --- | --- |
| **《汪家夫妻》** | `wangjia-couple` | 柯基老公阿福 × 柴犬老婆珍珠 | 家事日常反差：老公敷衍或偷懶 → 老婆慢轉頭（定格＋靜音）→ **跳過過程直接給誇張造型結果** → 結尾反轉 | [`series/wangjia-couple.md`](series/wangjia-couple.md) |
| **《闖禍小浣熊》** | `raccoon-mischief` | 小浣熊豆豆 × 浣熊媽媽、浣熊爸爸 | 弄壞家裡東西 → 門外鑰匙聲（0.6–0.8s）→ **跳過過程把自己假扮成那樣東西** → 媽媽當真使用／爸爸也在假扮 | [`series/raccoon-mischief.md`](series/raccoon-mischief.md) |
| **《網美小豬》** | `influencer-piglet` | 粉紅小豬粉粉 × 水豚男友 | 1.2 秒唯美網美照 → **拉遠揭曉超陽春假景＋苦力水豚男友** → 成品照破綻或男友失誤反轉 | [`series/influencer-piglet.md`](series/influencer-piglet.md) |
| **《社畜地獄》** | `shechu-hell` | 黃金獵犬員工阿金 × 胖橘貓老闆喵總 | 狗員工想做正常上班事 → **貓老闆用貓的天性搗亂**（推東西下桌、追紅點、躲紙箱、睡鍵盤）→ 無奈定格 | [`series/shechu-hell.md`](series/shechu-hell.md) |

新增一個零台詞 Shorts 系列時：複製 [`series/_template.md`](series/_template.md) 為 `series/<series-slug>.md`，寫明角色定妝錨點、固定五拍公式、專屬 AI 避險與前三支試片分鏡，並登記進上表、[`preflight.mjs`](preflight.mjs) 與 [`../rules-sync/manifest.tsv`](../rules-sync/manifest.tsv)。

---

## 所有零台詞 Shorts 統一的規格（站主定案）

四個系列與未來新增的無語音 Shorts 系列，一律遵守以下統一規格。個別系列有特殊例外時，寫在該系列的 `series/<slug>.md`。

| 項目 | 統一規格 | 為什麼（實戰依據） |
| --- | --- | --- |
| **零台詞、零字卡** | 整集沒有任何角色對白、旁白、內心獨白或畫面文字卡；只有背景配樂與物理音效，**關靜音也 100% 看得懂** | 2026-11-03 試做有內心獨白的職場短劇時，評審與站主都覺得靠台詞撐笑點太慢且有語言門檻；改成純視覺因果＋物理音效後，1 支成片可直接配 8 語系標題說明吃全球流量 |
| **片長與鏡數** | 成片 **11–16 秒**（硬範圍 **9–20 秒**），每集 **5–7 鏡**；單鏡動態段 **`≤ 3.5 秒`**（取 5 秒 H3 或 8 秒 Veo 片段最穩的 **0.6–3.0 秒**） | 2025–2026 Shorts 完播與重播數據顯示 11–16 秒最容易在觀眾看懂結尾反轉時自動重播回第 1 格（衝出 >100% 留存）；超過 20 秒單一視覺梗會疲乏 |
| **畫幅與音畫技術** | `1080×1920`（9:16 直式，Colab H3 `736×1312` 放大或 Flow／Veo Portrait）、`30 fps`、`48 kHz` 雙聲道、整體響度 **`-14 ± 1 LUFS`**（真峰值 `≤ -0.8 dBTP`） | 對齊 `qa_check.py` 與後台 Shorts 品管 `profile`／`loudness` 標準 |
| **9:16 介面安全區** | 核心臉部、毛爪道具與破綻線索一律放在 **`x: 78–902`、`y: 180–1380`**（比例 `x: 0.07–0.84`、`y: 0.09–0.72`）內 | 對齊 [`../SHORTS.md`](../SHORTS.md) 與 `tools/video/shorts/build.mjs`：避開右側 16.5% 按讚留言分享欄與底部 28% 標題進度條 |
| **畫風與世界觀** | 寫實 AI（真實毛髮與動物外觀），動物像人一樣雙足站立、穿固定服裝過日子；**世界裡完全沒有人類**（包含背景路人、人類手指與手臂） | 角色一旦混入人手或背景人影，一般觀眾第一眼就會覺得怪異出戲（2026-11-04 第一輪審片抓出最多的高嚴重度問題） |
| **鏡位鐵律** | **一鏡一主角（單人框）**、**80% 鎖定機位（`locked`）**。對手戲一律拆正反打；需要交代同場時，另一人只露畫面邊緣的一隻毛爪、一角衣服或背影 | 9:16 橫向窄，雙人同框或「畫外一隻手伸進來」極易讓模型畫出多一隻手或角色分身；固定機位最能凸顯前後狀態的喜劇反差 |
| **五拍節奏與迴圈** | ① 鉤子 `≤ 1.2s` → ② 停頓反應 `0.6–1.5s` → ③ **跳過過程硬切給誇張結果** `2.2–3.0s` → ④ 升級／破綻 `1.5–2.2s` → ⑤ 結尾反轉＋定格 `hold: 0.5–0.9s`（禁無意義黑畫面收尾，自然重播 Loop） | 2026-11-04 第一版有 10 集笑點盲審沒過，全是因為開頭鋪陳太長（4.6 秒）、反應呆滯（3 秒）、揭曉後沒停頓；按五拍重剪後 20 集全數過關 |
| **聲音與留白** | 轉折與結尾打點處必設 **`music_off: True`（瞬間抽掉背景音樂）**，搭配具體物理音效；**收尾音效必須排在最後一鏡結束前 ≥ 0.45s**（Veo／Flow 原片預設 `-an` 抽離音軌再重混） | 第一版有 4 支片的收尾音效排在最後一鏡結束後，成片直接被切掉沒播出；抽掉 BGM 加定格能讓笑點力道翻倍 |
| **八語上架** | 零台詞無需配音與翻譯字幕；`youtube-meta` 一次產出繁中＋8 語系（`en,ja,ko,es,pt,id,vi,th`）標題與說明欄；皆標示 AI 生成（`synthetic_media: true`） | 標題寫「情境鉤子」不寫「結局答案」；封面選反轉前或誇張結果最強的那一格 |

---

## 一集零台詞 Shorts 從頭到尾：每一關看哪份文件

| 階段 | 做什麼 | 看哪裡 | 過關條件 |
| --- | --- | --- | --- |
| **1. 企劃與三位盲評** | 寫一句話前提與五拍節拍表，送三位獨立評審做 100 分盲評，跑 `preflight.mjs score-blind` 排序；新系列先做 3 支試片 | [`WRITING.md` §一](WRITING.md)、[`REVIEW.md` §1](REVIEW.md)、[`series/_template.md`](series/_template.md) | 盲評中位數 `≥ 70 分`、無 `≥ 2` 位同鏡滑走、關靜音秒懂因果 |
| **2. 自動前檢與審劇本** | 寫 5–7 鏡分鏡表與 `<slug>.json`；跑 **`preflight.mjs check`** → 寫稿者十項自檢 → **獨立審稿代理七大關卡** | [`WRITING.md` §二～§六](WRITING.md)、[`preflight.mjs`](preflight.mjs) | `preflight.mjs` 0 錯誤、獨立審稿零高／中風險項 |
| **3. 角色定妝照與首格** | 沿用系列鎖定的定妝照（平靜、閉嘴、無道具）當參考圖，畫每一鏡首格（`colab/ff/` 或 `flow-inputs/`） | 各系列 [`series/<slug>.md`](series/)、[`REVIEW.md` §2](REVIEW.md) | 首格過五項（結果造型、毛爪、無路人無字、9:16 安全區、同機位連戲）；不對當場重畫 |
| **4. 片段生成與剪接** | 依 [`PRODUCTION-ROUTES.md`](PRODUCTION-ROUTES.md) 走 Colab H3、Google Flow（`preflight.mjs export-flow`）或後端 Veo API，用 `edit.py`／`recut.py` 剪取精華段、加音效、`hold` 與 `music_off` | [`PRODUCTION-ROUTES.md`](PRODUCTION-ROUTES.md)、[`WRITING.md` §三](WRITING.md) | 避開後半硬切與變臉；Veo 原片靜音重混；收尾音效落在鏡內 |
| **5. 成片四道品管與笑點審核** | 跑 `qa_check.py`（疊安全區紅框）→ 獨立審片人查畫面破綻 → **兩位不同觀眾角色盲審笑點** → 沒過走五級修法並送原審片人複審 | [`REVIEW.md` §3～§5](REVIEW.md) | 規格全過、無高／必修改中度畫面瑕疵、兩位審片人都判「笑點有畫出來」且好笑平均 `≥ 3/5` |
| **6. 雲端備份、匯入與覆盤** | 完整製作檔備份到雲端硬碟 `AI/備份/Shorts/<系列名>/`，再用 `node tools/video/shorts/cli.mjs import`（`meta.json` 寫 `"line": "drama"`、`"silent": true`，不放字幕檔）送後台；上架 7／28 天做數據覆盤與三點評分校準 | [`REVIEW.md` §6](REVIEW.md) | 雲端備份完整；後台匯入成功；7／28 天對比系列中位數與三點校準 |
