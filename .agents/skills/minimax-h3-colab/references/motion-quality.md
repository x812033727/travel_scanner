# H3 的動作流暢度與低錯誤率：貼圖感從哪裡來、怎麼寫、怎麼設定

站主 2026-10-28 看《種田娶妻打天下》仍有「貼圖感、不流暢」。這份把量到的原因、外面實測過的寫法與開源版的取樣設定放在一起；對 Hailuo 網頁的 H3、MiniMax API 的 H3 與 Colab 跑的開源 H3 都適用，只有第四節是 Colab 專屬。所有外部說法都標來源與讀取日（2026-10-28），本 repo 沒實拍過的就寫「未驗」。

## 一、貼圖感的三個來源（在《種田》量到的）

| 來源 | 量到什麼 | 對策 |
| --- | --- | --- |
| **秒數太短** | 每支買 4 秒＝107 幀（24 fps、對齊 17k+5），低於 H3 訓練範圍 **124–362 幀（約 5–15 秒）**（ComfyUI 官方 H3 教學；上游 notebook 對 <124 幀也印「低於已訓練下限」）。短於訓練範圍的片動作沒展開就結束，台詞一長只能慢放、停格 | **買 ≥5 秒**（124 幀＝5.17 秒）；畫面上有人說話或動作有兩拍買 6 秒（158 幀＝6.58 秒）。多的在剪接切掉，比停格便宜 |
| **剪接用複製幀慢放、再停格** | `assemble-v4.mjs` 原本 `setpts` 慢放最多 1.35 倍不插幀、`fps=24` 直接複製幀、不夠再 `tpad` 停格；第 1 集靜圖緩推 19%、第 2 集 27%，停格 7–8% | 慢放改 **光流補幀**（ffmpeg `minterpolate`，`mi_mode=mci`），上限 1.25 倍；靜圖 ≤10%；停格是最後手段 |
| **正文寫法** | 固定尾句「the camera keeps moving slowly the whole time」跟鏡頭自己的運鏡（fast pan right、tracking）打架；所有 locked 鏡被改成 push in，整集同一種推；`[Shot 1]` 沒有官方要的風格詞與 `<Picture 1>` 錨句；motion 寫的是狀態不是軌跡，沒有預備動作與重量 | 第二節的寫法 |

社群實測把僵硬、漂浮、「剪紙感」歸到同三件事：動作寫成狀態而不是物理事件、運鏡模糊或疊兩個、沒有力與重量的字（fuser.studio 的 H3 實測、digitalzoomstudio 2026-09、kapwing 的 H3 指南，2026-10-28 讀）。

## 二、正文怎麼寫（I2VA／FL2VA 三欄；Hailuo 網頁、API、Colab 同一套）

外框照官方（`.agents/skills/animation-preproduction/references/route-decisions.md` 第六節）：固定第一行、空一行、`integrated_multimodal_description`、`overall_soundscape: N/A`、`non_diegetic_music: N/A`。`[Shot 1]` 裡面依序：

1. **風格詞＋錨句**（官方 base 指南：「At the beginning of [Shot 1], state the overall style and initial composition」）。風格詞從官方表挑：`3D CG`、`2D-animated`、`live-action`、`claymation`、`watercolor`、`vintage film`；錨句引用 `<Picture 1>`、說人在哪、保留什麼：`3D CG. Xu Yan shown in <Picture 1> stays on screen left before the sealed doors, preserving his appearance, costume, props and the set layout.` 不重述畫面裡已經有的東西（有首格時正文只花在動作與運鏡；kapwing、fuser 同說）。
2. **說話句**（照 `docs/videos/series-plans/zhong-tian-qu-qi/production/storyboard-rules.md`）：`X speaks a short Mandarin line, 「…」, his lips, jaw and cheeks moving clearly with every syllable`。嘴要閉的鏡頭寫正向句 `lips remain closed`。
3. **動作寫成軌跡，一鏡一事**：`起點 → 預備動作 → 主動作＋物理 → 收勢`。預備動作是避免「突然就動了」的關鍵（digitalzoomstudio：a breath before speaking、a weight shift before stepping）；主動作要有力與重量的字：`weighted footfalls`、`shifts his weight onto the back foot`、`the sleeve catches the air`、`momentum carries the arm through`、`decelerates and settles`。寫哪隻手、握在哪、多快、停在哪（kapwing）。很快的動作留給模型的空間少，幾何容易壞：寫成中速或拆鏡。
4. **運鏡只一個**，照官方「種類＋幅度＋速度」句（`The camera pushes in with small amplitude at slow speed`；速度詞只有 `at slow speed`／`at fast speed`，中等就不寫）。鎖定要明講 **`The camera holds a static shot`**：H3 預設會漂（fuser）。推近寫起訖景別（from a medium shot to a medium close-up），不然會推過頭裁掉主體。**不要用 `then` 串第二個運鏡**：三個 `then` 在實測變成三個鏡頭、兩個切點（fuser）；`[Shot 2]` 同樣會切（`error-catalogue.md` #54）。
5. **收尾**：`One continuous shot.`（正向）。否定句常被畫成正向（試拍把 already closed 畫成開著的門），能不寫就不寫；真的要排除的東西用短句，不要堆清單。

長度：有首格時 60–150 個英文字；描述的動作要填滿買的秒數（官方 skill：描述時長對齊 4–15 秒）。身份細節在臉小的全景會掉（kapwing）：身份與顏值的重點放 MCU／CU。計畫有末格的鏡頭用 FL2VA 的對齊句（`model-misreads.md` §6 第一列），寫兩格之間的路徑，不寫兩個靜態描述。

改寫前後（《種田》e027 s06，許硯特寫、locked）：

```text
舊：[Shot 1] Xu Yan speaks 2 short Mandarin lines, 「那位客人，」 then 「還好嗎？」, his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, then he brushes the fan off his shoulder and holds Zhao Butou's gaze. The camera pushes in slowly. 3D Chinese donghua CG animation with smooth, weighty, expressive character animation; the camera keeps moving slowly the whole time; faces, hair and costumes stay the same; no morphing, no cuts. Keep the supplied first frame's composition, art style, character identities, costumes and props; one continuous shot with no cuts and no on-screen text.

新：[Shot 1] 3D CG. Xu Yan shown in <Picture 1> stays on screen left before the sealed doors, preserving his appearance, costume, props and the set layout. Xu Yan speaks 2 short Mandarin lines, 「那位客人，」 then 「還好嗎？」, his lips, jaw and cheeks moving clearly with every syllable; his eyes stay on Zhao Butou off screen right. After the last word his shoulder drops a little, then his hand sweeps the fan off his shoulder in one weighted motion and settles at his side, his gaze never leaving Zhao Butou. The camera holds a static shot. One continuous shot. Smooth, weighty 3D CG character animation; face, hair and costume stay as in the first frame.
```

Ref2VA（只有設定圖、沒有首格）用六段格式（`subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music`）；每鏡重述角色的完整外觀，不能只寫 `<Subject 1>`（ai-muninn 雙角色實測：只給標籤就會換人）；參照圖給正面臉、膝上、全身各一張就夠，轉身或背面要穩再加三視圖（note.com sepiablue 的三張參照實測）；兩個角色要長得夠不一樣。

## 三、秒數、幀數與畫布

| 買 | 幀數 | 實際秒 | 用在 |
| --- | --- | --- | --- |
| 4 | 107 | 4.46 | **不要**（低於訓練下限） |
| 5 | 124 | 5.17 | 一拍動作、沒人說話 |
| 6 | 158 | 6.58 | 畫面上有人說話；兩拍動作 |
| 8 | 192 | 8.00 | 長句或走位 |

Colab 的畫布：`width`／`height` 要 32 的倍數、面積 ≤ 1344×768。**16:9 的首格用 `1312×736`**（1.783，離 16:9 不到 0.005；0.97 MP 就是訓練尺寸；過 `qc.mjs` 的 1280×720 下限）。1344×768 是 7:4，`MiniMaxH3ImageToVideo` 會把首格**拉伸**到畫布（ComfyUI 官方：first_frame 比例不同就 stretch）；1280×720 不是 32 的倍數（720/32＝22.5），runner 會拒絕。`scripts/fit_first_frame.sh` 把關鍵影格裁到畫布比例；只有設定圖的 reference 模式才用 1344×768。解析度低於訓練尺寸會整片變軟（ComfyUI 官方：soft frames 多半是解析度不是步數）。

## 四、Colab 取樣設定（`scripts/patch_notebook.py` 的三個 profile）

上游 notebook（killkli，釘 `0a0d3b9`）的設定與問題：Ref2VA 用 **4 步** `ref2v_turbo_4step_v0.1`（544p 訓練；ComfyUI 官方：4 步 turbo 幾乎吃不進參照、臉與姿勢漂移）；FL2VA 用社群 drbaph v4 8 步；兩種都 `euler`／`beta`；沒有 shift 節點（官方 ComfyUI 範本也沒有，2026-10-28 讀 `Comfy-Org/workflow_templates` 的 i2v／r2v，所以不加）。`bootstrap.sh` 抓完上游就套 profile（`H3_PROFILE`，預設 `smooth`；`H3_NOTEBOOK_PATCH=off` 不套）：

| profile | Ref2VA | FL2VA（首格） | 取樣 | 用在 |
| --- | --- | --- | --- | --- |
| `smooth`（預設） | lightx2v `minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16`，8 步 | 官方 Comfy-Org `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16`，8 步 | `euler`／`simple`（lightx2v 卡片的建議） | 一般鏡頭；時間約上游 Ref2VA 的兩倍 |
| `hero` | 同上但 LoRA 強度 0（等於不掛）、**20 步** | 同 | `res_multistep`／`simple`（官方範本的 base 設定） | 顏值鏡、身份鏡、參照一定要吃進去的鏡；約三倍時間 |
| `draft` | 上游原樣（4 步 v0.1） | drbaph v4 8 步 | `euler`／`beta` | 只是看構圖 |

單項可用環境變數覆寫（`H3_REF_STEPS`、`H3_SCHEDULER`、`H3_REF_LORA_FILE`…，見腳本開頭）。釘 Ref2V **v1.0** 不是 v1.1：lightx2v 討論 #57 有使用者回報 v1.1 的 8 步「提示跟隨變差、說話不連貫」而 v1.0 在同設定下好；FL2V 的 4 步 v1.3 也有人回報跟其他 LoRA 疊用時嚴重退步（維護者承認）。turbo 的代價是「動作與聲音偏軟」（ComfyUI 官方）；步數 12–16 之後動作幾乎不再變，細節到 50 步還在長。

四個 LoRA 檔 2026-10-28 都在 Hugging Face（HEAD 200）；本 repo **沒有用這些設定實拍過**，第一批小樣要看：臉同設定圖、動作做完、嘴有動、第 0 格 PSNR。

續接（一鏡超過 15 秒、或要「上一支的最後一格接下一支」）：ComfyUI 官方建議 I2V continuation 從上一支末格接、每支之後掛 `H3-Anti-Burn-LoRA` 強度 0.5（臉在續接中越來越糙，comfyui-wiki 2026-10-14 實測 10 支鏈 +44% → 0%）；`NikoDemon80/ComfyUI-H3-Motion-Context` 把上一支的尾幀與聲音釘進下一支（要 ComfyUI ≥0.34、同解析度）。兩樣都不在這份 notebook 裡，產線本來就一鏡一支，列為選項。

## 五、錯誤目錄（症狀 → 原因 → 怎麼辦）

| 症狀 | 原因 | 怎麼辦 |
| --- | --- | --- |
| 動作小、像剪紙滑動、第 3 秒就停 | 4 秒（107 幀）低於訓練範圖；motion 是狀態不是軌跡；沒有預備動作 | 買 5／6 秒；第二節的軌跡寫法 |
| 畫面抖、一格一格 | 剪接複製幀慢放 | `minterpolate`，慢放 ≤1.25；多買秒數 |
| 鎖定鏡慢慢漂 | 沒寫 `holds a static shot` | 寫 |
| 一支裡自己切鏡（`qc.mjs` 退） | `[Shot 2]`、`then the camera …`、兩個動作 | 一鏡一事一運鏡 |
| 推近推過頭、主體被裁 | 沒寫起訖景別 | `from a medium shot to a medium close-up` |
| 臉、姿勢跟參照不像（Ref2VA） | 4 步 turbo；全景臉太小；只寫 `<Subject N>` 沒重述外觀 | `smooth`／`hero`；身份鏡用 MCU；每鏡重述外觀 |
| 三角形網格雜訊 | 步數太低、蒸餾版 shift 不對（ComfyUI 官方） | 提高步數（`hero`）；不要自己加 shift |
| 整片軟、糊 | 解析度低於 1312×736／1344×768 | 用訓練尺寸，不是加步數 |
| 首格被壓扁或拉長 | 16:9 首格對 1344×768 畫布 | 首格鏡用 1312×736，或 `fit_first_frame.sh` |
| 第 0 格 PSNR < 22 | 首格不是這一鏡通過 judge 的關鍵影格；被拉伸 | 首格＝關鍵影格；比例對 |
| 續接幾支後臉變糙 | 每支繼承上一支的誤差 | anti-burn LoRA 0.5（第四節） |
| 片尾變形、字亂 | Sage Attention 的 INT8（ComfyUI 官方；本 notebook 不用） | 不開 Sage |
| 冷啟動逾時 | 第一支要裝 ComfyUI、抓 40 GiB 模型 | `--timeout 10800`；一批同一個 manifest 共用 session |
| `exec` 逾時後重跑被重扣 | 遠端 kernel 還在跑 | 看 `progress.json`，只重跑沒完成的；`--session NAME` 重用 |
| GPU 配不到 | 方案、餘額、A100 沒貨 | 如實回報；`--no-high-mem` 或換 GPU 前先問站主 |
| 重做同一鏡結果每次都不同 | seed 隨機 | manifest 給 `seed`，寫進 `clips import --note` |
| 上傳前就該擋的錯（32 的倍數、`<Picture 3>` 超過、sha 不符） | — | `h3.sh check --manifest`（`batch` 會先跑） |

## 六、收工看什麼

照 `clips import` 的 verdict（凍格、切鏡、第 0 格 PSNR；`.agents/skills/animation-production/references/stage-preconditions.md` 最後一節）之外：開聲音實速看整支，說話的人嘴有沒有動；數近停格的時間占比（參考片《萬妖圖錄傳》1.4%）；比對首格與末格的身份；把 profile、seed、秒數、CU 寫進收據。

## 七、來源（2026-10-28 讀）

- MiniMax 官方：`github.com/MiniMax-AI/MiniMax-H3`（`skills/h3-prompt-writing/references/base-en.txt`、`ref-en.txt`）；`github.com/MiniMax-AI/awesome-minimax-h3-integration`（Turbo 6–8 步減少動作拖影、PDD 在 4 NFE 會抹平插畫質感）。
- ComfyUI 官方：`docs.comfy.org/tutorials/video/minimax/minimax-h3`（步數、解析度、124–362 幀、turbo 強度、失敗模式）與 `…/minimax-h3-native`（I2V 首格拉伸、R2V 參照、turbo 偏軟）；`Comfy-Org/workflow_templates` 的 `video_minimax_h3_i2v.json`／`video_minimax_h3_r2v.json`（res_multistep／simple、20 步、LoRA 預設關）。
- LoRA：`huggingface.co/lightx2v/Minimax-h3-Turbo` 討論 #48、#51、#57；`huggingface.co/drbaph/MiniMax-H3-Turbo-Lora-ComfyUI`；`comfyui-wiki.com/en/news/2026-09-04-minimax-h3-turbo-ref2v-8step`、`…/2026-10-14-h3-anti-burn`。
- 續接：`github.com/NikoDemon80/ComfyUI-H3-Motion-Context`。
- 上游與分支：`github.com/killkli/minimax-h3-colab-skill`（釘 `0a0d3b9`，最新）；`github.com/wonghanz/minimax-h3-colab-skill` v0.2.0-hardened 的 17 項修正（冷啟動 timeout、seed、single 的 progress、先下載再驗音軌、HTTP 退避）——沒合回上游、也沒 LICENSE，本 repo 不換，能在自己這層做的（送出前檢查、seed、逾時原則）做了。
- 寫法實測：`fuser.studio/articles/minimax-h3-prompt-guide`、`kapwing.com/resources/how-to-prompt-minimax-h3-hailuo-3-0-…`、`digitalzoomstudio.net/2026/09/unrealistic-movement-in-ai-video-models-like-minimax-hailuo-h3-fix/`、`zenn.dev/acntechjp/articles/zenn-minimax-h3-character-consistency`（FL2VA vs REF2VA：關鍵影格要是動作的起點不是終點；REF2VA 糙是 4 步與低解析度造成，不是模式）、`note.com/sepiablue/n/nc752c844266c`（三張參照怎麼配）、`ai-muninn.com/en/blog/minimax-h3-ref2va-two-characters`（雙角色、每鏡重述外觀）、`atlascloud.ai/blog/tips/minimax-h3-prompt-guide`（45 支官方提示：有參照時正文短、運鏡明講含「不推不切」）。
