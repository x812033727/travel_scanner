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
- **長開 pod 接力**（2026-11-02 起，站主把後台 pod 最長時數改 24、閒置回收改 60 分鐘）：`production/colab/runs/_scripts/chain.sh st23:46 st1:47 …` 在同一台 pod 上依序跑，每一步自己重試沒貨、自帶速度看門狗，跑完不停機（閒置 60 分鐘才回收），審完草稿的重抽也用同一台（`KEEP=1 retake-run.sh`）。審草稿和剪接時 GPU 跑別集，不必每段重開、也少碰 EU-RO-1 沒貨。
- **八語配音一集一個代理，可以三集同時跑**（e045–e047，各約 20 分鐘，每集 US$0.10–0.25）：`dub.sh` 的鎖是每集一個，不同集不會互卡。但代理之間共用 scratchpad，同名的輔助腳本會互相覆蓋（e045 的代理跑到 e047 的 `mk.py`），每個代理要一開始就給它自己的資料夾。
- **長開的 pod 也會壞**（e049，第 21 小時）：GPU 掉了，SeedVR2 先卡 3600 秒，之後每支都 `[Errno 6] No such device or address`。`speed-guard.sh` 現在連續三支 `ComfyUI failed`／`no result after` 就停 pod 換一台；之前只看慢，抓不到這種死法。
- **volume 上的模型檔壞了**（2026-11-03）：換新 pod 也一樣失敗、但第一段（只用 H3 的檔）正常，就是 volume 上那個檔壞了；開機的 `fetch_models.py` 只看 `.verified` 標記和大小，不重驗內容，所以新 pod 修不好。站主在後台 RunPod 卡「空間」刪掉 volume（要先停 pod），下一台 pod 會在有貨的地方自動開新 volume、重下約 112 GiB（e049 在 EU-CZ-1，開機到第一支約 40 分鐘）。
- **台詞會被畫成字幕**（e053 s05）：正文寫 `speaks a short Mandarin line, 「衝——！」`，草稿在畫面中間燒進一行「衝——！」。只有一兩個字的喊叫最容易出事；改寫成 `shouts out loud, his mouth wide open in a shout` 並補「The picture is clean: no subtitles, no captions, no text」，重抽一次就乾淨。
- **24 小時上限也會到**（2026-11-04）：長開的 pod 在第 24 小時被站台停掉（`max_hours`），`st23-retry.sh` 照常接手，但當時 EU-CZ-1 沒貨 90 分鐘。一台 pod 大約跑 4.5 集就會碰到上限；接力時不必提前換，讓重試迴圈處理即可。

## 雲端 session 的磁碟（2026-11-05，第 55 集）

- 每集的工作資料夾約 1.5–2 GB；最大的是 `segments-v4`（約 800 MB），是 `asm.sh` 的中間片段，重剪時會重建。整集上架後就可以刪。
- 幫別的 session 推備份分支時，**不要用一般的 `git worktree add`**：一份完整 checkout 就要 1.5 GB，兩份幾乎把配額用完，升 1080p 寫檔會失敗。改用
  `git worktree add --no-checkout -b <branch> <dir> origin/main && git -C <dir> read-tree origin/main`，只放要加的檔，`git add -f`、commit，推完 `git worktree remove --force`。
- 開工前看 `df -h .`（在 repo 裡跑）的 Avail；低於 3 GB 就先清已上架集數的 `segments-v4`。

## r2 第 1–3 集學到的（2026-11-06）

**跑長批次（雲端 session）**
- **雲端容器會自己重啟**（這兩天三次），背景工作全部被砍；`run_in_background` 的工作兩小時也會被砍。一集的草稿要 3.5–4 小時，一律用
  `setsid nohup bash … > log 2>&1 < /dev/null & disown` 跑，並接成一支「等上一步結束 → 下一步 → 最後 `h3r.sh stop`」的 chain 腳本。
- 容器重啟後 pod 還開著、沒人送工作，會空轉到站台 60 分鐘閒置停機，每次約 US$2.6（第 1 集 r2、第 3 集 r2 各一次）。重啟後第一件事：
  `h3r.sh usage` 看有沒有 pod 在跑，有就馬上把 chain 接回去（已完成的片段會跳過）。
- **`h3r.sh batch` 只停自己開的 pod**：重用別人（或上一個被砍的批次）開的 pod 時，結束會寫「left running: it is billing until stop」。chain 的最後一步一定要 `h3r.sh stop`。
- `retake-run.sh` 沒貨放棄時以前是 exit 0（2026-11-06 改成 exit 1）；外層迴圈仍以「輸出檔數夠了沒」判斷，不要只看結束碼。
- 用 `grep error` 等批次失敗會誤中「0 error(s)」，要寫 `Traceback|gave up|failed` 這類只在失敗時出現的字。
- `h3r.sh images` 不會借用正在跑 batch 的 pod，而是另開一個（同一個帳號一次只能一個，沒貨時直接 409）；要畫圖就排在 batch 之後、同一個 chain 裡，並加 `--keep`，否則畫完會把 pod 停掉。

**挑片**
- 每鏡兩個種子，82 支裡約一成會**鏡中跳鏡**（特寫一兩秒就跳成全景或別的場、夜景），第 2 集 s13、s35，第 3 集 s14、s19、s21、s25、s29 都有一支。
  挑片時看片段最後一兩格，不只看第一格和動量。
- 動量低的鏡（插鏡、坐著說話）兩支都低就照用，整集剪完看總數；r2 第 2 集整集動量 8.3、靜止 4%，沒有因為幾鏡低而不過。

**買秒數**
- **先錄配音，再決定買幾秒**：錢員外說得慢（約 2.4 字／秒），三句各 7.4–7.8 秒，照稿子估的 6 秒會停格。每鏡需要的秒數 = Σ(該鏡每句錄音長 + 0.5 秒)，
  超過「買的秒數 − 0.3」0.5 秒以上就加買（8、10、12）。r2 第 2–4 集各有 6–8 鏡因此加買。
- 該在鏡尾發生的事（第 2 集 c40 柴刀飛出）抽出來常常在片段後段：`stage-clips.sh 902 s40@2.0` 從 2 秒起，剪進 3 秒裡剛好收在半空。

**參考圖**
- 稿子寫「要補○○的定妝照」之前先看現有的圖：阿令「沒戴鐵鐐」的定妝照不用畫，因為她的定妝照是胸像、本來就沒有鐵鐐（第 1 集的鐵鐐是正文寫的）。
- 別的 session 改過的 `cast.json` 先比對再合併：審片分支的版本是舊底稿，直接合會把系統聲音、二牛的扁擔、錢員外的家丁、許硯的西裝 look 改回去；只套真正新改的欄位。

**磁碟（r2 第 3 集，2026-11-06）**
- 雲端磁碟滿了（0 MB）：推備份用的暫存 git 庫寫不進去，第 3 集備份失敗；同時寫入中的草稿也可能壞掉（這次檢查過沒壞）。
- 舊版集數的工作資料夾推上 `transfer/zt-eNNN-media` 之後，先用 `--filter=blob:none` 只抓檔案清單，逐檔比對 blob 雜湊（不可重建的檔案全部在、內容一樣）才刪本機；
  第 43–57 集比對全部一致後刪掉，清出 17 GB。各集發布包資料夾（`zhong-tian-qu-qi-eNNN/review/`，匯入工具的預覽與匯入紀錄）沒備份，留在本機。
- 每集開工前看一次 `df -h ~`：一集的工作資料夾約 1.3–1.5 GB，推備份時暫存再要約一樣大。
- **自己定時檢查，不要等站主問**（站主 2026-11-06）：容器一天重啟五次，每次都砍掉背景排程。用 `create_trigger` 開兩個每小時的排程（:05、:35）喚醒同一個對話，
  每次看 `uptime`、chain 還在不在、pod 有沒有空轉，斷了就接回去，批次做完就接下一步；不用了就 `delete_trigger`。chain 腳本放在 scratchpad，容器重啟後還在。

**送審前的連戲審查（站主 2026-11-07：「這些在審片時應該要看到吧？」）**
- 第 4 集 r2 的三個錯（木匣忽大忽小、門與鍋的距離、許硯出門看不到黑影）每一鏡單看都沒問題，挑片時一鏡比兩支、剪完每鏡只看中間一格，所以都沒抓到。
- 剪完、`cut-qa.py` 過了以後，一定要跑
  `python3 docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/continuity-sheets.py <cut 資料夾> <video.json> <輸出資料夾>`：
  一場一張圖，每鏡頭、中、尾三格照剪接順序排。對著 `script.md` 那一場逐張看：
  - 同一個道具每一鏡大小、樣子一樣嗎（木匣、柴刀、借據、鍋）？
  - 地點的相對位置一樣嗎（門、灶、桌、院門、井的左右與距離）？
  - 誰在看什麼：被看的人或東西在他看的方向、在前後鏡裡看得清楚嗎？
  - 同一場的時間、光、衣服、手上的東西一樣嗎？
- 有一項不對就重抽那幾鏡，修好再送後台；看過的結果寫進該集工作單。
- **鏡頭開頭閃一下別的畫面**：連戲表一排出來才看到，Ref2VA 片段有時開頭 0.1–0.8 秒是另一個畫面（全景、場景圖）再跳成這一鏡；每鏡只看中間一格看不到，播出來是閃一下。
  r2 第 1–4 集共 11 處（e901 s08、s16；e902 s13、s35；e903 s01、s05、s14、s19、s24、s25；e904 s13）。剪完一定跑
  `python3 docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/cut-jumps.py <cut 資料夾>`（逐格找鏡頭內的硬切），
  開頭的用 `stage-clips.sh NN sNN@秒數` 從跳完之後起剪（寫進 `colab/runs/eNNN/stage-clips-args.txt`），再剪一次、`cut-jumps` 要 0。
- **送審前另外兩關（站主 2026-11-07 同意加）**：
  - 聲音：`python3 docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/audio-qa.py <cut 資料夾> <video.json>`，
    讀 `assemble-v4.mjs` 寫的 `<stem>.lines.json`，查台詞跨到下一鏡（說話的人在畫面裡時）、兩句重疊、被片尾切掉、被配樂蓋過、超過 4 秒沒有台詞。
    它不會判斷嘴型與聲音合不合臉，那仍要站主聽。
  - 獨立審片：另開一個沒參與製作的子代理，照 `colab/runs/_scripts/independent-review.md` 給它稿子、連戲表與三個檢查的結果，逐場挑錯；
    照它的清單修完才送後台，清單與處理結果寫進該集工作單。
- 每集送後台前的順序：`cut-qa.py` → `cut-jumps.py` → `audio-qa.py` → `continuity-sheets.py` 自己看一遍 → 獨立審片 → 修 → 送審。

**挑片要對著稿子看動作有沒有發生（2026-11-07，獨立審片的教訓）**
- 第 2、3 集送審後，獨立審片各挑出十幾處「稿子的動作沒演出來」：鐵鐐沒打開、木頭沒劈開、柴刀是被手拿著不是飛、該撲空的手抓住了水桶、
  許硯走出灶房而不是走進來、唐小棠一鏡開襟低胸、家丁露臉、同一把刀與燈每鏡不同。挑片時我只比兩支哪支好看、有沒有跳鏡，沒有逐鏡讀稿子的「動作」欄。
- 挑片時每一鏡都要問：稿子這一列寫的動作（誰做了什麼、東西最後在哪裡）在片段裡有沒有發生？兩支都沒有，就是重抽，不是挑比較好的那支。
- 站主 2026-11-07 定的流程：**挑完片、精修前**先跑連戲表（`continuity-sheets.py runpod/a/st1/out <video.json> <out>`，草稿模式）與獨立審片，
  該重抽的重抽、再一起精修；**剪完**再跑一次全部檢查與獨立審片。修正範圍：嚴重與中等都修，輕微的接受。
- 第 6 集起，挑片直接交給獨立審片代理：每鏡兩個種子的整段格子（`fps=0.7` 一條）與稿子一起給它，逐鏡判斷「稿子的動作有沒有發生」並選種子，
  兩支都不行就標 RETAKE、附英文改寫句；製作端照它的清單重抽，再一起精修。製作端不再自己挑完才給人審。

**寫規格的小陷阱（r2 第 2–6 集重寫時踩到的）**
- 提示詞裡出現 `modern` 這個字（例如「不要現代手銬」），`gen-dh.mjs` 會把那一鏡當成現代場景、拿掉場景圖；改寫成「old Chinese iron shackles」這種正面描述。
- 寫「red paper flower」會被 preflight 的紙張檢查擋（以為是有字的紙），改寫「red papercut flower」。
- 場景圖本身有的東西會被畫進去（第 3 集灶房的場景圖右邊有一盞玻璃燈，所以燈常變成玻璃煤油燈）；道具與場景圖衝突時，在每鏡寫清楚道具的樣子，或換一張場景圖。
- 一鏡的提示詞上限 1000 字：多個常數一起用時很容易超過；近景改用一句短的場景句（`*_cu`），全景用 `*_m`，不要拿掉道具與表情。
- 稿子裡的雷電、閃白這種「整個畫面一下子發白」，模型常常不畫；剪接用 `edit-dh-eNNN.json` 的 `"flash": {"sNN": 0.4}` 加白閃（`assemble-v4.mjs`），再配一個雷聲音效。


## Colab 版第 1 集（《恁祖媽今年18》，2026-11-07）學到的

真人短劇第 1 集照同一條路線 A（Ref2VA 960×544 `hero` → σ0.5 refine 到 1312×736，不跑 SeedVR2）在 Colab G4 做完；28 鏡草稿 9 CU、精修約 10 CU。
跟 RunPod 共通、或寫稿時就能避開的事：

**一鏡最多三個有名字的人**
- Ref2VA 一支最多放四張參考圖：最多三張角色定妝照，再加一張場景圖。第四個角色只能靠文字，模型會自己編一個人：
  - c12 寫四個人，第一次草稿多出一個穿米色套裝的女人。
  - 把林美鳳的外貌寫進正文重抽，又多出三個穿制服的女生。
- 站主同意的改法：那兩個人移到畫面外，他們的反應交給下一鏡。
- 寫稿時就把多人鏡控制在三個有名字的人以內；第四個人只拍背影，或放到別鏡。

**模型會跳過開頭的動作**
- c21 寫「照老習慣撐扶手站起來，才發現不用撐」，兩次小樣她一開頭都已經站著。
- 改法：起身寫進前一鏡 c20 的結尾。c20 從約 6 秒變約 7 秒，標長鏡、買 8 秒；c21 從站著開始。
- 一鏡的開頭要和前一鏡的結尾同一個狀態（坐著、站著、手上拿什麼），要轉換的動作放在前一鏡的尾巴。

**鏡中跳鏡要在精修前剪掉，而且剪完要停在 17k+5 格**
- 跳鏡分兩種，要用不同的方法抓：
  - c19 的 5 秒眼睛大特寫，第 3.2 秒硬切成一個全景（同一個 seed 每次都一樣）。
  - c26 是鏡頭慢慢轉去拍燈，掃描抓不到，要看格子圖。
- 剪完的草稿格數必須是 17k+5（39、56、73、90…），refine 的 notebook 才收。手剪成 77 格送出去才失敗，白開了一個 session；`refine.py --check` 現在會先擋。
- `.agents/skills/minimax-h3-colab/scripts/h3.sh cuts --input-dir st1/out --output-dir trimmed --manifest st1.json` 在草稿階段（本機、免費）做這兩件事：
  - 找出鏡中的硬切。分數要過 0.15，而且是前後六格中位數的 8 倍以上才算：c19 是 0.31 對 0.002；c13 書包上的鈴一彈就到 0.16，但周圍有 0.02–0.06，那是動作不是切點。
  - 剪回切點前的 17k+5 格；剪完短於該鏡的 `min_seconds`，就以結束碼 3 要求重買。
- 跟剪完才跑的 `cut-jumps.py` 互補：一個在精修前，一個在成品上。

**剪接表要跟著剪過的片段改**
- `assemble-v4.mjs` 對無聲鏡用 `min(action_seconds, 2.4)` 秒，再跟 `min.<鏡>` 取大的那個。
- 片段剪到 1.6 秒時，會被撐成 2.4 秒、停格 0.6 秒。
- 那一鏡的 `action_seconds` 要寫成不超過片段長度，`min` 寫片段長度。

**道具大小只寫在場景圖不夠**
- 場景圖的提示詞寫了「約三十公分」，片段裡的燈加燈罩仍比人頭還高。
- 每一鏡的正文都帶同一句用身體比的尺寸，大小就穩了，c18 是小的：「about thirty centimetres tall … about as tall as a forearm is long … never looks bigger than a person's head」。這跟本章「同一個道具忽大忽小」的教訓一致。

**Colab 的批次與容器重啟**
- runner 的 `prompt_file` 是相對於「執行時所在的資料夾」，不是 manifest 所在的資料夾。在上層資料夾送出子資料夾的 manifest，會讀到上層同名的舊提示詞（報錯「references Picture [4]; it has 3 images」）。一律 `cd` 到 manifest 所在的資料夾再跑 `h3.sh batch`。
- 容器重啟時 Colab 的 session 照樣開著，每小時約 10 CU。重啟後第一件事是看 `h3.sh usage` 的 `active_assignments`；有就馬上接上同一個 session（`--session` 沿用、`refine.py --only` 跳過已完成的鏡）。不要重開，冷開機一次約 2 CU。
- 重抽與精修排在同一個 session 裡跑：草稿重抽、產生精修 manifest，再 `h3.sh refine`，省一次冷開機。

**種田（RunPod）也用得到的兩件事**（2026-11-07 對照上面一節）
- RunPod 一支放得下九張參考圖，第四個人不會像 Colab 那樣被模型自己編出來，但人多一樣會出事：r2 第 6 集 c01 五人同框，兩稿都多畫一個秦霜。`preflight-prompts.py` 的 `four` 對一鏡四個以上有名字的人發出警告，寫稿時就壓到三人。
- 挑完片、精修之前，在本機（免費）跑一次 `python3 -I .agents/skills/minimax-h3-colab/scripts/cuts.py --input-dir runpod/a/st1/out --output-dir <暫存> --json <報告>`，只看報告、不用它剪出來的檔案。報告裡的切點換成 `stage-clips.sh NN sNN@SECS` 的剪點。e905 試跑 35 支，只抓到 s36 的 0.42 秒，和人工挑片排好的 `s36@0.5` 一致。
