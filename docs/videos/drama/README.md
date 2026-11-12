# AI 劇的共用區

每一部 AI 劇都適用的規則、教訓、審片與備份。系列自己的決定放在系列資料夾的 `production/RULES.md`、`REVIEW.md`；教訓統一放 `docs/videos/lessons/<劇>.md`。

| 檔案 | 內容 |
| --- | --- |
| [`WRITING.md`](WRITING.md) | 分鏡怎麼寫，讓模型照我們的意思畫 |
| [`REVIEW.md`](REVIEW.md) | 審片：付錢前的預檢、挑片、剪完的檢查、獨立審片、表情審查、交站主、送後台；語言、標題封面、上 YouTube |
| [`lessons/shared.md`](../lessons/shared.md) | 做過的集數學到的教訓，依主題分 |
| [`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md) | 備份分支：分集與共用各放什麼、怎麼確認完整；雲端硬碟今天有什麼 |

系列區：
- 種田娶妻打天下：[`RULES.md`](../series-plans/zhong-tian-qu-qi/production/RULES.md)、[`lessons/zhong-tian-qu-qi.md`](../lessons/zhong-tian-qu-qi.md)、[`REVIEW.md`](../series-plans/zhong-tian-qu-qi/production/REVIEW.md)
- 恁祖媽今年18：[`RULES.md`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/RULES.md)、[`lessons/tai-nainai.md`](../lessons/tai-nainai.md)、[`REVIEW.md`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/REVIEW.md)

## 兩個系列統一的做法（站主 2026-11-08：「照你的建議統一」）

種田與祖媽原本做法不同的地方，統一如下。系列的 bible 或舊文件跟這裡衝突時，以這裡為準。

| 項目 | 統一後 | 為什麼 |
| --- | --- | --- |
| 表情 | 每個露臉的人每一鏡都寫表情，寫成臉怎麼動。只有劇情要冷臉的才寫平靜。舊規則「沒寫就是嚴肅、不笑」不再用 | 真人定妝照是平臉，沒寫表情就是一張平臉（種田真人版第 1 集，34 張臉有 18 張偏平、沒表情或演錯） |
| 畫面上說話的台詞 | 用模型自己的聲音（同一鏡草稿的音軌）；系統聲、心裡話、畫外、背影的台詞用錄好的聲音 | 錄好的聲音對不上模型的嘴形（種田真人小樣）。祖媽站主 2026-11-07 也已改成模型原聲（第 1–3 集是原聲版） |
| 預算 | 每一集都有上限，接近上限先停下來問站主。種田每集 US$28；祖媽每集 25 CU（整季 1,300–1,500 CU ÷ 60 集，從第 4 集起） | 兩個系列都不會一集超支才發現 |
| 剪接 | 預設不推近、不裁切放大；慢放上限 1.1 倍，台詞放不下時單一鏡可以到 1.2 倍，要寫在剪接表的備註。**用模型原聲的鏡完全不放慢、也不加空白尾巴**，片段不夠長就停在最後一格（祖媽第 2 集：放慢 3% 嘴就慢 5 格；`assemble-v4.mjs` 已照做） | 放大會糊，慢放太多動作不自然；秒數買夠才是正解 |
| 開場 | 開場 10 秒至少四鏡 | 抓住觀眾的通用做法。種田第 2 集已經在拍，從第 3 集起照做 |
| 挑片 | 草稿交給獨立代理挑，製作端不先自己挑 | 做的人容易看成自己希望的樣子 |
| 每一集的流程 | 照種田站主 2026-11-07 定的五步：自己審自己改（挑片後、剪完後各一次獨立審片，嚴重與中等自己修好）→ 教訓寫進規則 → 推分集與共用分支、核對 → 送上後台確認成片字幕封面都在、另一個代理到 GitHub 核對後才刪本機那一集 → 前一集還在跑時先做下一集的前置 | 兩個系列同一套 |
| 精修解析度 | 精修到 1312×736，剪接時放到 1920×1080，不跑 SeedVR2 | 兩個系列的真人版本來就這樣做 |
| 劇本的來源 | 每個系列只有一份來源檔，其他檔由它產生（種田是 `r2.py` → `video.json`、`script.md`；祖媽是 `script.md` → `compile.py`），產生出來的檔不手改 | 工具不同，原則一樣 |

**不統一、各系列自己定的**：
- 服裝與露膚：種田允許低胸；祖媽因為廣告安全，不露胸不露背。這是各系列自己的服裝與廣告決定。
- 角色、場景、道具、聲音的選擇。
- 外語：兩部都是中文原聲加多語字幕（CC），不做外語配音（種田站主 2026-11-07；祖媽站主 2026-11-07）。

## 一集從頭到尾：每一關看哪份文件

| 關卡 | 看哪裡 |
| --- | --- |
| 開拍前的企劃與鎖定 | 下面〈開拍前的鎖定與變更單〉 |
| 角色與參考圖、試鏡 | 下面〈角色與參考圖〉；試鏡的教訓在 [`lessons/shared.md`](../lessons/shared.md) 第二節 |
| 寫分鏡 | [`WRITING.md`](WRITING.md) |
| 付錢前的預檢、估價 | [`REVIEW.md`](REVIEW.md) 第 1 節；上限照系列 `RULES.md` 第四節 |
| 跑草稿、精修 | 種田走 RunPod 路線 A（[`minimax-h3-runpod`](../../../.agents/skills/minimax-h3-runpod/SKILL.md)）；祖媽走 Colab G4（[`minimax-h3-colab`](../../../.agents/skills/minimax-h3-colab/SKILL.md)）。兩部都精修到 1312×736 |
| 挑片、重抽、連戲審 | [`REVIEW.md`](REVIEW.md) 第 2、3 節 |
| 配音與錄音 | 下面〈聲音〉 |
| 配樂與音效 | 下面〈配樂與音效〉 |
| 剪接 | 上面的統一規則；工具是種田的 `assemble-v4.mjs`，兩部都用（種田 [`storyboard-rules.md`](../series-plans/zhong-tian-qu-qi/production/storyboard-rules.md)〈剪接〉、祖媽 [`REVIEW.md`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/REVIEW.md) 第八節） |
| 剪完的檢查、獨立審片、表情審查 | [`REVIEW.md`](REVIEW.md) 第 4–6 節 |
| 交站主、送上後台、核准上架包 | [`REVIEW.md`](REVIEW.md) 第 7、8 節 |
| 語言與多語 CC、標題說明封面、上 YouTube | [`REVIEW.md`](REVIEW.md) 第 9–11 節 |
| 備份分支、雲端硬碟、刪本機 | [`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md) |
| 交接給下一個 session | 下面〈交接〉 |
| 下一集的前置 | 下面〈下一集的前置〉 |

容器重啟後的第一件事兩部一樣：先查還有沒有 GPU 機器在計費，有就接回同一台。種田看 `h3r.sh usage`，祖媽看 `h3.sh usage` 的 `active_assignments`（教訓在 [`lessons/shared.md`](../lessons/shared.md) 第十二、十四節）。

### 開拍前的鎖定與變更單

開拍前的分鏡表、動態分鏡、小樣計畫、預算上限與鎖定，照 [`animation-preproduction`](../../../.agents/skills/animation-preproduction/SKILL.md) 的〈開拍鎖定包〉：整集在花錢之前給站主確認一次，之後照包做。
鎖定以後要改分鏡、路線、秒數或參考圖，照它的〈變更控制〉開變更單：改動先攢齊、站主點頭、一次改完再重鎖；同時照 [`WRITING.md`](WRITING.md) 第十三節告訴製作端。
祖媽試鏡用過變更單（[`screen-test/decisions.md`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/screen-test/decisions.md)）。

### 角色與參考圖

1. 列清單：本集的角色、造型、場景、道具（分鏡最後的〈本集需要的造型〉〈本集需要的參考圖〉，`WRITING.md` 第十四節）。稿子寫「要補○○」之前，先看現有的圖是不是已經夠用。
2. 先試 2–4 張，跟原圖或候選並排、每張標好名字給站主挑。調「程度」只畫一輪兩個種子，挑不到就停。
3. 選中的放進 repo 系列資料夾的 `production/assets/refs/`，重算 `SHA256SUMS`，在那裡的 README 寫來源與還原指令（照種田 [`assets/README.md`](../series-plans/zhong-tian-qu-qi/production/assets/README.md) 與祖媽 [`screen-test/README.md`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/screen-test/README.md)〈收工〉的做法）。
   種田真人版目前只有 [`assets/refs-live/README.md`](../series-plans/zhong-tian-qu-qi/production/assets/refs-live/README.md) 進了 repo，圖還在備份分支。
4. 登記進 `cast.json` 的 look。
5. 每一輪的圖，包括沒選中的，都進系列的共用備份分支（[`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md)）。

### 聲音

- 錄音用站台的 Gemini 聲音，聲音與 style 寫在系列的 `cast.json`；style 開頭照頻道寫法「標準國語，咬字清楚…」，不寫台灣腔；Sulafat 留給旁白（祖媽 bible〈聲音〉）。
- **撞聲檢查**：同一集裡不能有兩個說話的角色用同一個聲音。換聲音或加一個有台詞的路人就重跑。祖媽 2026-11-06 跑過全季；種田還沒有寫下來的結果。
- 畫面上露嘴說話的台詞用模型原聲（上面的統一規則），其他用錄音。原聲的開口時間由剪接工具量（`assemble-v4.mjs` 對草稿音軌跑 `silencedetect`，-35 dB、0.25 秒），字幕照它放；工具細節在 [`route-a.md`](../../../.agents/skills/minimax-h3-runpod/references/route-a.md)〈嘴形跟配音對不上〉那一條。
- 錄音放在每集工作資料夾的 `audio/`（外語在 `audio-<語言>/`），跟著分集分支備份；聲音樣本（試鏡的 `_audition/`）進共用分支。

### 配樂與音效

- 配樂：每場一首，揭曉的那一鏡一個重音（`WRITING.md` 第二節）。種田用 Lyria 依情緒生成（`hailuo/music-zt.mjs`），祖媽照 bible〈配樂、音效、剪接〉。
- **只給一集用的配樂放在那一集的 `music/`，跟著分集分支**；系列共用的配樂與音效庫放 `_series/<系列>/`，跟著共用分支（[`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md)）。
- 招牌音效（例如祖媽的報信鈴、種田系統句前的「叮」）列在系列的 `REVIEW.md`，剪完要量得到（`REVIEW.md` 第 4 節）。

### 交接

容器隨時會被收掉，每天收工或換 session 前寫一份交接。放在這一集分集分支的 `RESUME.md`（跟著備份走）；做法或規則的改變另外寫進 repo 的系列文件。要寫的：

- 現在做到哪一關、下一步是什麼；
- 正在跑的 GPU 機器（RunPod pod 或 Colab session 的 id）、排程的 id、串接腳本與 log 的位置；
- 花了多少、還剩多少上限；
- 等站主決定的事（照 `REVIEW.md` 第 7 節的寫法，有選項與花費）；
- 備份推到哪一版、三道檢查的結果（`BACKUP-BRANCHES.md`〈怎麼確認備份完整〉）；
- 本機還沒進分支的檔案。

### 下一集的前置

前一集還在跑時先做：上一集最後一場的連戲表與接點（下一集第一鏡接同一刻）、轉提示詞與預檢、要補的參考圖、估價。
