# Shorts 零台詞短劇的多引擎製作路線手冊（Colab H3 × Google Flow × 後端 Veo API）

這份是共用區：說明一支通過**階段一盲評**、**階段二技術審稿與 `preflight.mjs` 前檢**的零台詞 Shorts，如何依需求選擇最合適的影片生成引擎（或在同一集內混搭），並安全接回統一的剪接（`edit.py`）、成片品管（[`REVIEW.md`](REVIEW.md)）與雲端備份流程。

無論走哪一條路線，**成片技術規格永遠一致**：`1080×1920`（9:16 直式）、`30 fps`、`48 kHz` 雙聲道、`-14 ± 1 LUFS`（真峰值 `≤ -0.8 dBTP`）、零台詞零字卡、9:16 介面安全區構圖。

---

## 一、三條路線一覽與選用決策

| 項目 | 路線 A：Colab Qwen ＋ MiniMax H3 | 路線 B：Google Flow（代理在瀏覽器操作；2026-11 預設 Omni 1.2 Flash） | 路線 C：網站後端 Veo 3.1 API |
| --- | --- | --- | --- |
| **定位** | **批次主力**（已實戰量產 4 系列 20 集） | **高表現力／新系列試片／難演微表情**；2026-11-21 起可整季量產（社畜地獄 e01–e06） | **全自動 API 路線**（適合接回後台媒體管線） |
| **原生畫幅與時長** | `736×1312`（放大至 `1080×1920`）、**5 秒** | Portrait `9:16`；Omni 1.2 Flash **4 秒**、下載 720×1280（Veo 3.1 Fast／Quality 標示 2026-12-05 停用） | `720p`／`1080p`、4／6／8 秒（`veo-3.1-lite` 1080p 固定 **8 秒**） |
| **角色一致性做法** | 系列定妝照 → Qwen 首格 → H3 圖生影片（`<Picture 1>`） | 上傳系列定妝照 → Flow 內 Nano Banana 2.1 畫首格（同機位用前一張編輯）→ 以首格為第一格生影片 | `veo-3.1-lite` 僅首尾幀（無 `referenceImages`）；`fast`/`standard` 最多 3 張參考圖 |
| **原生音訊處理** | 無原生音訊（純影像） | **原生音訊必開** → 提示詞加靜音防護，剪接時預設 `-an` 靜音再由 `edit.py` 統一配 BGM＋SFX | **原生音訊必開**（`catalog.py`：`native_audio=True`）→ 同左處理 |
| **單支費用參考** | Colab CU（批次最低，詳見 `minimax-h3-colab`） | Flow 點數：Omni 1.2 Flash **12 點／支**、生圖不扣點；一集 6–7 鏡約 72–84 點（不額外走 API 帳單） | `apps/api/app/video_media/catalog.py`：`lite` US\$0.08/s（720p \$0.05/s）、`fast` \$0.12/s、`standard` \$0.40/s |
| **最適合的鏡頭** | 固定機位靜態造型、日常節奏鏡、大批量續集 | 精細臉部微表情（慢轉頭、憋噴嚏、挑眉）、複雜物理互動（倒水、翻書、毛髮飄動） | 未來交給主機工人全自動跑的系列 |

### 混搭原則（一集內可混用）
- **靜態唯美照／成品照鏡**（如《網美小豬》第 1 鏡）：**兩條路線都不進影片生成**，直接拿首格（`still: true`）做 `push` 慢推靜圖片段，最省點數且零變形。
- **一般動作鏡**走路線 A（Colab H3）；**重頭戲特寫鏡**（例如怎麼抽 H3 都表情僵硬的第 2 拍慢轉頭或第 5 拍收尾反應）可單獨改走路線 B（Google Flow Veo 3.1），再一起放進同一個 `edit/plan.json` 剪接。

---

## 二、路線 A：Colab Qwen 首格 ＋ MiniMax H3（批次主力）

完整操作與排錯見 `.agents/skills/minimax-h3-colab/SKILL.md`；零台詞 Shorts 只需牢記四條實戰紀律：
1. **先跑前檢**：送 Colab 前必先跑：
   ```bash
   node docs/videos/shorts-drama/preflight.mjs check <slug>.json --engine h3
   ```
   確認 **0 錯誤**（含 `thumb` 有效、單人框、SFX 落在 `dur` 內、無 `magazine cover`／人手陷阱）與所有必要警告都已處理。
2. **首格先過目再進 H3**：Qwen 畫完 `colab/ff/*.png` 後，逐張檢查四件事（誇張結果造型有畫出來、動物毛爪沒變人手、無路人與亂碼文字、關鍵元素在 9:16 安全區內），首格不對當場重畫，絕不把錯的首格送去跑 H3。
3. **只取前段最穩的 0.6–3.0 秒**：H3 生成 5 秒片段，剪接表預設 `in: 0.2~0.3`、`dur: 0.6~3.0`；`edit.py` 會在偵測到片段中途硬切（`scene > 0.4`）前自動截斷。
4. **同機位換姿勢必用圖編**：同一場地連換多個姿勢（如《闖禍小浣熊》電視換台），後面的鏡一律拿第一張首格當底圖給 Qwen Image Edit，背景才 100% 鎖死不跳動。

---

## 三、路線 B：Google Flow

### 2026-11-21 起：代理直接在瀏覽器操作 Flow（社畜地獄 e01–e06 的做法）
1. **帳號與瀏覽器**：Flow 專案屬於登入的 Google 帳號，換帳號就看不到。優先用 **Claude in Chrome**（站主的 Chrome、可自動存檔）；內建瀏覽器每次下載都會要站主按。Chrome 視窗被最小化或分頁在背景時，Flow 頁面常卡死（`innerWidth` 變 0、指令逾時），請站主讓視窗留在畫面上。**不要用 `/u/N/` 網址試帳號**：其中一個被導到 Google 登出頁，把 Chrome 裡所有帳號都登出了。
2. **一集一個專案**；代理設定（專案層級）把圖像與影片都改成 9:16、各 1 張。
3. **上傳定妝照**：Flow 的上傳鈕會開系統檔案視窗，代理操作不了。把圖片轉成 File 後對媒體區送出拖放事件即可；第一次上傳會跳使用權同意框，要站主同意才能按。
4. **首格**：一則訊息可要求 Flow 一次畫 4–5 張（附兩張定妝照、每張編號 `E0N-S0M`），同機位鏡再寫「edit E0N-S0M」。逐張檢查五項＋**重點道具在畫面中段**（生圖時寫 `at the vertical centre of the image` 最有效）＋**沒有隔間背景**＋**道具連戲**（同一個公事包顏色、風衣還在）。生圖不扣點，不對就重畫，同一鏡最多重畫兩次。
5. **片段**：一則訊息列出全部鏡頭與「用哪張圖當第一格」，Flow 會問「要開始生成這 N 部影片嗎？這會消耗 12×N 點」，按「核准」。等太久沒按會逾時取消（不扣點，按「再試一次」）。每支提示詞結尾都加無台詞防護句。同名圖有多個版本時，用文字指定是哪一版並請 Flow 先說它會用哪張。
6. **下載**：格子上按右鍵 →「下載」→ 720p，比點進編輯畫面穩（有一支片在編輯畫面讓分頁卡死）。Chrome 會擋同一網站連續下載；我們的做法是在頁面上攔下 Flow 的下載動作，把檔案直接 POST 給本機的接收程式（127.0.0.1），站主在 Chrome 允許一次「存取本機網路」後就全自動。內建瀏覽器同一檔名會互相覆蓋，記得每次換檔名。
7. **剪接前先抽格**：Omni 的動作常在 1–2 秒後才發生，結尾又可能自己加戲（貓整隻撲出畫面、筆電翻面露出像商標的圖案），每支先抽 4 格再決定 `in`／`dur`。片段是 **24 fps**，格數換秒數要除以 24。水花、撲擊這類大動作要加 `"keep_cuts": true`，不然 `edit.py` 會當成換景截掉。

### 舊做法：站主在 Flow 手動生片（Veo 3.1，2026-11-20 寫）



因本環境的雲端 VM 無法直接登入並操作站主的 Google Flow 網頁帳號，路線 B 採**「AI 備齊首格＋可貼提示詞 → 雲端硬碟交接 → 站主在 Flow 生片 → AI 下載組裝與四關品管」**的半自動協作模式，把站主的手動操作壓到最低（一集約 5–10 分鐘）：

#### 步驟 1：AI 產出分鏡、過前檢並一鍵轉出 Flow 提示詞單
1. 分鏡過完階段一盲評與階段二獨立審稿後，跑：
   ```bash
   node docs/videos/shorts-drama/preflight.mjs check <slug>.json --engine h3
   node docs/videos/shorts-drama/preflight.mjs export-flow <slug>.json --out flow-prompts.md
   ```
2. `export-flow` 會自動完成三件專為 Veo 3.1 調整的轉寫：
   - **移除 H3 專用標記**：把 `shown in <Picture 1>` 轉為自然英文 `from the starting frame`，避免 Veo 誤讀角括號；
   - **自動附加無台詞音訊防護句**：每鏡尾端強制加上：
     > `Silent film visual comedy: zero spoken dialogue, no voices, no gibberish speech, no background music; only subtle natural foley sounds.`
   - **標出免進 Flow 的靜圖鏡（`still: true`）與雲端交接路徑**。

#### 步驟 2：AI 畫好 9:16 首格（Frames）並放進雲端硬碟
- AI 用內建生圖工具（`generate_image`，`AspectRatio: "9:16"`，以系列鎖定定妝照為 `ImagePaths` 參考）畫好每一鏡首格，檢查完 9:16 安全區、無人類手指、無文字 Logo 後，連同 `flow-prompts.md` 上傳至：
  ```text
  AI/備份/Shorts/<系列名>/<slug>/
  ├── flow-prompts.md          # 逐鏡可直接複製貼上的 Flow 提示詞與設定
  ├── flow-inputs/             # 9:16 首格圖（s01-xxx.png, s02-xxx.png...）
  └── flow-clips/              # 站主在 Flow 生成完丟回來的 mp4（s01-xxx.mp4...）
  ```

#### 步驟 3：站主在 Google Flow 網頁生片（逐鏡 3 步）
1. 在 Flow 開專案，模式選 **Frames to Video**（若需要同時參考角色定妝照與道具，改選 **Ingredients to Video**），畫幅選 **Portrait (9:16)**。
2. 依序上傳 `flow-inputs/<鏡號>.png` 當開頭影格，貼上 `flow-prompts.md` 對應的動態提示詞，先用 **Veo 3.1 Fast** 生成（關鍵微表情鏡若不滿意再切 **Veo 3.1 Quality**）。
3. **8 秒片段省額度技巧（同機位雙拍合併）**：若同一場景有連續兩拍、同一個鎖定機位（例如「看到東西掉下去 → 僵住 1 秒 → 慢慢轉頭看鏡頭」），可以在 Flow 用一支 8 秒片段演完，下載後在 `edit/plan.json` 切成兩段（或中間插切別鏡），一鏡當兩鏡用。
4. 下載成片命名為 `<鏡號>.mp4`（與 `flow-prompts.md` 寫的檔名一致）丟進雲端 `flow-clips/`，通知 AI 接手。

#### 步驟 4：AI 下載、靜音軌重混、四關品管
1. **音訊處理鐵律**：Veo 3.1 內建原生音訊，容易混入背景雜音、自動生成的怪配樂或細碎含糊人聲。
   - **預設做法（最穩）**：直接進 `edit.py`（預設帶 `-an` 抽離原片音軌），改由 `edit.py` 統一鋪系列 BGM、`music_off: True` 瞬間靜音與精準物理 SFX，確保全集 `-14 ± 1 LUFS` 與統一系列聽感。
   - **保留原生物理音效的例外**：只有當 Flow 生成了極自然的物理聲（如玻璃碎裂、水花潑灑、貓推馬克杯）且**人工聽過 100% 沒有任何怪人聲與雜音配樂**時，才用 `ffmpeg` 單獨擷取該段音軌當該鏡 SFX 混入。
2. 照 [`REVIEW.md`](REVIEW.md) 跑 `qa_check.py`（疊上 9:16 安全區紅框）、獨立畫面審核與雙人成片笑點審核，通過後備份與匯入後台。

---

## 四、路線 C：網站後端 Veo 3.1 API

網站後端媒體目錄（`apps/api/app/video_media/catalog.py`）已登記三款 Veo 3.1 模型：
- **`veo-3.1-lite-generate-preview`**：720p（US\$0.05/s）與 1080p（US\$0.08/s，固定 8 秒）；支援首尾幀、**不支援角色參考圖（`reference_images=0`）**、原生音訊必開。
- **`veo-3.1-fast-generate-001`**：4／6／8 秒，1080p US\$0.12/s，最多 3 張角色參考圖、原生音訊必開。
- **`veo-3.1-generate-001`**：主鏡頭用，4／6／8 秒（1080p 固定 8 秒），US\$0.40/s，最多 3 張角色參考圖、原生音訊必開。

使用路線 C 的注意事項：
1. 任何 API 付費生片前，必須先經站主核准該集預算，並先跑 `node docs/videos/shorts-drama/preflight.mjs check <slug>.json --engine veo`。
2. 因為 `veo-3.1-lite` 1080p 固定計費 8 秒（單鏡 US\$0.64），若 1 集 5 鏡全跑 `lite` 1080p 約 US\$3.20；靜態鏡頭務必設 `still: true` 省去生片費，並視需要把同機位連續動作合併在同一個 8 秒片段內再切鏡。
3. 與路線 B 相同，Prompt 必加無台詞防護句，且進 `edit.py` 預設 `-an` 靜音軌統一混音。
