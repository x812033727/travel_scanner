# 種田娶妻 第 31 集起：首格與片段都在 Colab 做

站主 2026-10-28 定的路線 B（票 `2026-10-28-31-60-colab-qwen-image-edit`）：第 31–60 集不再用海螺。首格在 Colab 用
**Qwen-Image-Edit-2509**（吃定妝照與場景圖）畫，片段在同一個 Colab session 用 **MiniMax H3** 的 `first_frame`
模式跑；兩者都走 skill `minimax-h3-colab`（`.agents/skills/minimax-h3-colab/SKILL.md`）。分鏡、`video.json`、
錄音、剪接、合集與配音照 `../hailuo/README.md` 與 `hailuo-batch-driver.md` 的既有流程，只有「畫首格」和「買片段」
這兩步換掉；素材位置、檔名（`first-frames/sNN-tK.png`、`clips/sNN-tK.mp4`）與 `assemble-v4.mjs` 都不變。

## 這個資料夾

- `ff2manifest.mjs`：`gen-dh.mjs` 的首格清單（`ff-dh-eNNN.json`）→ `h3.sh images` 的 manifest。每鏡最多三張參照
  （Qwen-Image-Edit 只收 image1–image3）：場景圖一定在，再放鏡頭順序的前兩張定妝照，被擠掉的會印出來，那個角色只剩
  提示詞裡的 `Characters:` 文字描述。海螺那句 `Reference images: …` 改寫成 `image 1 is the character sheet of …`。
- `clips2manifest.mjs`：`clips-dh-eNNN.json` → `h3.sh batch` 的 manifest，每 20 鏡一份（上游 runner 的上限）。每鏡用
  `first-frames/` 裡最新的 take 當首格，正文原封不動寫進 `prompts/clip-sNN.txt`、`prompt_sha256` 是全文雜湊；
  沒首格的鏡列出來並以 1 停下（`--skip-missing` 才跳過）。

兩支都讀 `VIDEO_WORKDIR`（沒設時 `~/mokaair-work/videos`），take 號碼自動接在工作區已有的檔案後面，`--take K`
可以指定；`--only s01,s02` 只做幾鏡。

## 2026-10-28 小樣之後：片段走 Ref2VA，不畫首格

e031 三鏡小樣（票 `2026-10-28-31-colab-h3`）量到：Qwen-Image-Edit 畫的首格臉與皮膚質感到不了海螺那種寫實 CG（三輪提示詞、20 步 base、
單人特寫都一樣），而 H3 **reference 模式**直接吃 3D 定妝照畫出來的片段就是海螺的畫風；1920×1088 比 1344×768 更能守住低頭、轉頭時的臉。
所以第 31 集起的片段用 `ref2manifest.mjs`：每鏡的參考圖 = 鏡內角色的定妝照（`refs-dh/<id>-portrait-tK.png`）＋每人最多兩張角度臉
（`refs-dh/angles/<id>-angle-*.png`，從第 1–30 集的海螺首格裁的；唐小棠的要裁到臉、不帶舊版低領）＋場景圖，最多九張；正文是 gen-dh 的鎖定稿，
把首格的對齊句與錨句改成逐張點名，並把 `cast.json` 的外貌段逐字放進錨句（動作之前、每鏡同一段字）。首格那兩步（`ff2manifest.mjs`、`h3.sh images`）
留給需要靜圖或要先審構圖的鏡。

```bash
node $C/ref2manifest.mjs $H/clips-dh-e031.json $H/ff-dh-e031.json 31 $M/ref        # 預設 1920×1088、每人兩張角度臉、20 鏡一份
for m in $M/ref/ref-e031-part*.json; do
  bash $K/h3.sh batch --manifest $m --output-dir $W/clips --progress ${m%.json}.progress.json --session zt31 --timeout 10800
done
```

實測：1920×1088 一支 6 秒約 12 分鐘、約 1.5–2 CU（A100 高 RAM 6.77 CU/hr）；同一個 seed 換解析度構圖會變。`output_path` 直接寫
`clips/sNN-tK.mp4`（上游 runner 會把 `output_name` 的點換成底線，所以不用它）。

## 一集的流程（首格路線，保留）

```bash
H=docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo
C=docs/videos/series-plans/zhong-tian-qu-qi/production/colab
K=.agents/skills/minimax-h3-colab/scripts
W=${VIDEO_WORKDIR:-~/mokaair-work/videos}/zhong-tian-qu-qi-e031-dh
M=$W/colab   # manifest、prompts、progress 都放工作區，不進 repo

# 0. 開機（每個新 session；要先配對，見 skill）；餘額抄下來
bash $K/bootstrap.sh && bash $K/h3.sh usage

# 1. 工作清單（跟海螺時期一樣）
node $H/gen-dh.mjs docs/videos/zhong-tian-qu-qi-e031/video.json $H/local/empty-lock.json 31 $H/ff-dh-e031.json $H/clips-dh-e031.json

# 2. 首格：manifest → 檢查 → 同一個 session 畫完（第一次會裝 ComfyUI、抓約 29 GiB 模型）
node $C/ff2manifest.mjs $H/ff-dh-e031.json 31 $M
bash $K/h3.sh start --session zt31                       # A100 高 RAM；之後片段共用這個 session
for m in $M/ff-e031-part*.json; do
  bash $K/h3.sh images --manifest $m --output-dir $W/first-frames --progress ${m%.json}.progress.json --session zt31
done

# 3. 審首格（照第 1–24 集掃描的規則：女角不露、不血腥、畫面無字、唐小棠高領）；退的重畫
node $C/ff2manifest.mjs $H/ff-dh-e031.json 31 $M --only s08,s21     # 自動變成 t2
bash $K/h3.sh images --manifest $M/ff-e031-part1.json --output-dir $W/first-frames --session zt31

# 4. 片段：manifest（每 20 鏡一份）→ 檢查 → 同一個 session 跑
node $C/clips2manifest.mjs $H/clips-dh-e031.json 31 $M
for m in $M/clips-e031-part*.json; do
  bash $K/h3.sh batch --manifest $m --output-dir $W/clips --progress ${m%.json}.progress.json --session zt31 --timeout 10800
done
bash $K/h3.sh stop --session zt31 && bash $K/h3.sh usage          # 餘額差額寫進收據與票

# 5. 之後照舊：rec.sh 31 → asm.sh 31 → audit.mjs → prep-import.mjs
```

顏值鏡（細綱的 `glamour_shot`）的片段用 `H3_PROFILE=hero bash $K/bootstrap.sh patch` 換 profile 後另跑一份只含那一鏡的
manifest，跑完 `bash $K/bootstrap.sh patch` 換回 `smooth`。

## 第一批要量的

e031 先做三鏡（含一個雙人鏡、一個顏值鏡）當小樣：冷啟動幾分鐘、一張首格與一支片各扣幾 CU、磁碟放不放得下兩組模型、
Qwen-Image-Edit 畫的臉跟定妝照像不像、空白 latent（`QIE_LATENT=empty`）的構圖對不對提示詞、1312×736 放大到 1080p
的畫質。數字寫進 `.agents/skills/minimax-h3-colab/references/cloud-pairing.md` §4 與票。規劃時的預估：每集約 60 CU
（首格 4、片段 48、冷啟動 6、hero 2），30 集約 1,800 CU；都還沒實測。

## 已知的限制

- 首格最多三張參照：三個以上角色同框時第三個人只靠文字，臉可能不像；可以先畫兩人、第三人靠 `image1` latent 重畫，
  或把那鏡拆開。
- `h3.sh images` 的檢查器會對 `<Picture N>` 警告：那是 H3 的標記，Qwen-Image-Edit 讀的是「image N」。
- `exec` 逾時後遠端可能還在跑；看 `*.progress.json`，用 `--only` 只重跑沒 `completed` 的鏡，不然會重扣。
- 一批首格最多 40 張、片段最多 20 支；轉檔會自動分 part。
