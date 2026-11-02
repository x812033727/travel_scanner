# 路線 A 在 RunPod 上（2026-10-31 實測）

站主的標準：**除了 GPU 伺服器，品質和流程都要和 Colab 一樣；一樣就繼續，不一樣就找原因。** 寫法、審片與重抽的規則不在這裡重寫，照 `.agents/skills/minimax-h3-colab/references/lessons.md` 第 2、6 節與 `.agents/skills/minimax-h3-colab/references/three-stage.md`。

## 一、和 Colab 的對照

《種田》e033 s08、s21，同 seed 330000、同參考圖，第一段與第二段正文的 SHA-256 都與 Colab 當時送出的相同，Colab 原始檔在分支 `transfer/zt-e033-parity`。

| 階段 | 構圖、動作、臉 | SSIM（s08／s21） |
| --- | --- | --- |
| 第一段 960×544 hero | 一致 | 0.835／0.910 |
| 第二段 1312×736 | 一致 | 0.830／0.903 |
| 第三段 1920×1080 | 一致 | 0.802／0.880 |

位元不會相同：Colab 是 Server 版 G4、PyTorch 2.11（第三段記錄）、當時最新的 ComfyUI、SeedVR2 命令列；這裡是 WK、PyTorch 2.9.1、釘住的 ComfyUI、SeedVR2 節點。背景細節與表情有些微差異，判斷只看過兩鏡的抽格。

## 二、實測時間與費用（WK，US$2.59／小時）

| 項目 | 時間 |
| --- | --- |
| 第一次下載全部模型（112.4 GiB） | 約 19 分鐘（FP8 那組）；之後開機不重下 |
| 開機到可送工作 | 約 1–5 分鐘 |
| 第一段，第一支（含載入） | 238–284 秒 |
| 第一段，暖機 | e040 前 14 支平均 124 秒；7 張參考圖 160 秒 |
| 第二段（含載入／之後） | 223–255 秒／s21 192 秒 |
| 第三段 7B（含載入／之後） | 198–225 秒；暖機未單獨量 |

三段一支約 US$0.3–0.4（估算）。兩鏡三段一個 Pod 實付 US$0.99。同一張卡 Colab 約 US$0.8／小時（換算，未查帳單），RunPod 約貴 3 倍；好處是模型留在 volume、站台代開代停。

## 三、踩過的坑

| 症狀 | 原因 | 怎麼辦 |
| --- | --- | --- |
| 每步 31.65 秒、一支 11 分鐘、GPU 滿載 | 映像用 CUDA 12.8＋FP8；Colab 是 CUDA 13＋INT8 | 已改成相同的組合，**不要自行換權重**；要換先和 Colab 對照 |
| Pod 回報就緒，下一個上傳卻 404 且無內容 | 新 Pod 的 RunPod 代理還不穩（由症狀推斷） | runner 已要求連續三次就緒並重試 |
| 覺得風格和舊集不同 | 拿第一次抽的原始片段比調色、挑片後的成片；那鏡又是清晨群戲 | **同鏡同 seed 比原始檔**再下結論；原始片段未經 `assemble-v4.mjs` 的調色與暗角 |
| 人物赤腳 | 定妝照看不到腳，或別人的定妝照是赤腳 | 第一段重抽，後兩段救不回來 |
| Windows 上 `ref2manifest.mjs` 沒有輸出 | 它的 main 判斷只在 Linux 成立 | 從 Linux 跑 |
| 同時開第二個 Pod 被拒 | 站台一次只准一個 | 等前一批結束 |
| Pod 終止後讀不到記錄 | 記錄隨 Pod 消失 | 每步秒數要趁跑的時候從 RunPod 主控台看 |

## 四、整集做法

```bash
bash .agents/skills/minimax-h3-runpod/scripts/route_a_st1.sh 40 400000   # 草稿；先給站主估價
# 審草稿、重抽有問題的鏡；不做的鏡寫進 st2/skip.txt
bash .agents/skills/minimax-h3-runpod/scripts/route_a_st23.sh 40 400000 s08:400001   # 第二、三段，重抽過的鏡寫它的 seed
```

輸出在 `VIDEO_WORKDIR` 底下的 `zhong-tian-qu-qi-eNNN-dh/runpod/a/`；第三段的檔名是 `<id>_1080.mp4`。這兩支都會花錢，先請站主點頭。

**雲端 session 從這條路跑還沒驗過**：要有 `MOKAAIR_VIDEO_TOKEN`，環境要連得到 `mokaair.com` 與 `*.proxy.runpod.net`，整集要用 `setsid nohup` 脫離（背景指令上限 2 小時，`lessons.md` 第 4 節）。兩支腳本也還沒照原樣跑完過整集，本機是用相同步驟的工作目錄腳本跑的。片段匯入產線是票 `2026-10-30-runpod-canvas-and-import`。

## 五、第 40–42 集學到的（2026-11-01）

三集共 125 支走完三段。第 41 集 US$18.31，第 42 集 US$18.05（含 US$0.93 畫圖、US$4.84 重抽）。一集約 9 小時是 54 鏡的量。

**速度**

- 同型 WK 也會差很多：第 42 集重抽那台每支 180–300 秒，第一段那台同鏡 130 秒，下一台第二段又回到正常的 167 秒。原因沒查出來。第一支含載入模型，不算；跑到第三支以後再比，慢一倍就換一台比等著划算。
- 「done in」接近 300 秒的那幾支參照圖並不多（s02 只有 4 張），參照圖張數解釋不了。

**Qwen 在 RunPod 上**

- `h3r.sh images` 驗過能用：第一張約 110 秒（含載入），之後一張 9–20 秒，四張約 US$0.24。
- 沒有定妝照的角色（掌櫃、書吏）會變卡通，衣服顏色每鏡都變。從草稿裁臉當參照也不行，卡通感會帶過去；要先畫定妝照，提示詞寫 `realistic human proportions and a normal-sized nose and eyes`。
- 寫 `wine jars` 會多畫現代酒瓶，場景圖畫好要放大看櫃檯和角落，瓶子會跟著進每一鏡。發現時已經用它拍片的話，代價就是整組重抽。
- **不要用 Qwen 修已有的場景圖。** 「其他不變，只換這一處」三個 seed 都失敗：要換的東西還在、多出一個大甕蓋住帳本、木頭變成花紋。ffmpeg `delogo` 留下糊塊，貼圖裡的物件又像飄著。要改就趁拍片前整張重畫。

**審草稿**

- 只看 4 格縮圖會漏。酒瓶就是縮圖上沒認出來、看成片才發現，別在縮圖上下「沒問題」的結論。
- 同一個人出現兩次（s32、s35）：拿掉場景圖，再寫 `behind him is only a blurred ... wall, with no other figure`。
- 只有手的插鏡開頭常是場景空景。`headtrim.sh` 只抓硬切，手慢慢滑進來的抓不到（第 40 集 s20、s49、s54 都是 `no cut`），要自己看格數再用 `stage-clips.sh` 的 `sNN@秒數`。
- 扣手腕容易畫成握手：寫 `wraps from above around the wrist, four fingers over the top and the thumb under it; the two palms never meet`，還是只有最後幾格對，這鏡短的話用最後一段。
- 寫 `a scrawny young thief` 會畫成小孩，要寫年紀和 `a grown man`。
- 配角沒有固定場景方向時，兩個 seed 常常一個看錯邊；挑片時先看視線合不合分鏡的軸線。

**環境**

- Windows 上放在 scratchpad 的 worktree 路徑太長，`shutil.copy2` 會在較長的檔名報「找不到路徑」，已經跑完的部分還是會被 `git add`。多步驟指令要 `set -e`，worktree 開在短路徑。新 worktree 沒有 `node_modules`，`tools/video` 會缺 `pinyin-pro`。

**分工**

- 動手畫圖或做集數前先看 `npm run tasks -- list` 和 `origin/claude/*`：第 42 集四張圖就是和別的 session 各畫了一份。先做完拍片的那份為準，因為換圖要重拍。

## 六、第 43 集學到的（2026-11-01，第一次從雲端 session 跑整集）

**雲端 session**

- 雲端 session 走得通：`login --runpod` 配對、開 pod、上傳參照圖、下載草稿、停機都正常；`mokaair.com` 與 `*.proxy.runpod.net` 經代理都連得到。新 pod 回報 ready 前會先回幾次 `pod: 404`，約 3 分鐘，正常。
- 同型 WK 速度差很多，跟在哪裡跑無關：第一段兩台都是每支 175–260 秒，重抽那台 106–132 秒、第二段那台 165–187 秒。照第五節，跑到第三支還慢就換。
- `HTTP 409 … EU-RO-1 目前沒貨`：模型 volume 在那一區，只能等。寫一個每 3 分鐘重試的迴圈（第 43 集等了 12 分鐘、5 次）。
- 等待條件別用 `grep -q error`：檢查器那行「0 error(s)」也會中。
- 換機要殺 runner 時先記 pid（`echo $! > x.pid`），不要 `pgrep -f <腳本路徑>`：會比對到自己那條 shell，exit 144（colab `lessons.md` §7 同一個坑）。

**配角定妝照（Qwen，`h3r.sh images`）**

- image 1 用既有的胸像（書吏）畫新配角，三種提示詞都抄了書吏的臉和山羊鬍。**image 1 改用一張場景圖**（`set-haoshe-t1.png`），提示詞寫「in exactly the 3D render quality, materials and lighting of image 1, but not its place: a plain dark smoky blue-grey studio backdrop …」，臉才各自不同，一輪就成。一張 38 秒。
- 不寫領口就會畫成立領盤扣（清代、民國）：寫「a crossed collar or a round collar, no buttons and no frog closures on the chest」。
- `gen-dh` 只認得主要角色；`video.json` 的 `characters` 裡其他 id（書吏 `shuli`、巡考 `xunkao` …）拿不到定妝照。`production/colab/runs/_scripts/extras_patch.py` 依每集的 `colab/runs/eNNN/extras.json` 把定妝照接進去（`st1-ep.sh NN` 會自動跑）。

**草稿的通病（第 43 集 37 鏡重抽 15 鏡）**

- **紙上的假字最多**（8 鏡）：場景圖書案上有字的紙、考卷、摺紙、門上的匾額都畫成一大片亂碼。救法：摺紙寫「folded into a tight square, its outside plain and blank」；考卷寫寬袖蓋住大半張、只露出貼彌封的紙角，或焦點放在袖上的雨珠、紙在陰影裡虛焦；門楣寫「the beam above the gate plain bare red-lacquered wood」。
- **場景圖是長巷，就拍不出小號舍**：拿掉場景圖、把小空間寫清楚（磚牆三面、矮瓦頂的裂縫正在頭上）後兩個 seed 都在號舍裡，漏水也看得到。
- **台詞全在畫外的特寫，嘴還是會動**：寫「does not speak at all: his lips stay closed for the whole shot except for one long slow exhale」。
- **唐小棠的角度臉是舊版低領**：她的嚴肅特寫一個 seed 露出胸口。重抽時拿掉兩張角度臉、只留 `tangxiaotang-portrait-t2`，再寫「collar stays buttoned up to her chin」，兩個 seed 都對。
- **遠景裡的人會站到參考圖其他人旁邊**：s20 唐小棠該在廣場遠處，兩個 seed 都站在馮學正旁邊；拿掉她的參考圖（她下一鏡才出場）就好。
- 只給場景圖的插鏡有 5 鏡開頭是空景：`headtrim.sh` 抓到 4 鏡的硬切；s01 是手慢慢伸進來，逐格看後用 `s01@0.7`。看起來像硬切的不一定是：e043 s11 的「跳」是人從書案直起身。

**花費（第 43 集，37 鏡）**：定妝照 2 張 US$0.64；第一段 US$5.0（兩台慢機）；重抽 34 支 約 US$3.1；第二、三段見票。

**第 44–45 集補充**

- 唐小棠的高領：定妝照 t2 是整件蓋住的，但在州城客棧客房的中近景，模型常畫成「立領扣著、下面開襟外罩＋抹胸」，重抽壓不住（e045 s33、s36）。**站主 2026-11-02 看過這種畫法：「這種露胸程度還好，也蠻不錯的」**，所以立領扣著、外罩下露出抹胸上緣這個程度不必重抽、不必裁。仍要重抽的是：衣料透明、低領露出乳溝、抹胸滑落這類更露的。
- 插鏡的場景空景不一定在開頭一閃：e044 s31、s36 長達 4.0／2.5 秒，`headtrim.sh` 只看前 1.5 秒。整支跑 `select='gt(scene,0.30)'` 找切點，再 `stage-clips.sh NN sNN@秒`。
- 只要寫到紙上有「brush columns」「columns of small neat brush strokes」，就會畫出一片清楚的假字，「no readable writing」沒用。焦點寫在燭火或指尖、紙寫成 `far out of focus, only soft pale grey blur and shadow`，兩個 seed 至少一個乾淨（e045 s26、s27、s30）。
- 第二段第一台 pod 中途 `Connection reset by peer`，那份清單其餘的都沒做；`route_a_st23.sh` 重跑一次會跳過已有的，只補缺的。
- **慢機很常見，而且越來越多**（2026-11-02）：e045 第三段一台每支 830–900 秒（正常約 200），e046 第一段一台 845／1383 秒（正常約 120）；同一區 EU-RO-1 也常整個沒貨（409）。`production/colab/runs/_scripts/` 有 `st1-retry.sh`、`st23-retry.sh`（沒貨每 3 分鐘重試、被回收就接著做）和 `speed-guard.sh LOG 秒數 "樣式"`（第 2 支以後超過門檻就殺掉內層驅動，trap 停 pod，重試迴圈開新的一台）。整集交給它們跑，不用人盯。
