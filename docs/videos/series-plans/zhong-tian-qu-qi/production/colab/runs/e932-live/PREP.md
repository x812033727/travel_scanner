# 第 32 集重製版 r2（e032-r2，內部 932）真人版開拍前置

- 2026-11-18，開拍前置代理。**沒送任何生成**（Colab、RunPod 都沒開）、**沒用站台 TTS**、沒 commit。只跑免費檢查。
- 依據：`writer-tools/e032-r2/r2.py`（照獨立審稿 `writer-tools/e032-r2/review.md` 改過的 39 鏡）、第 31 集的做法（`colab/runs/e931/extras.json`、`colab/runs/e931-live/{mkspec.py,spec.json}`、scratchpad `tools/prep931.sh`、`tools/e931d1.sh`、`tools/e930d1.sh`）、第 30 集審稿的〈機械檢查〉表、`r2-bible-e031-e040.md`（拍法 1–43、〈人物〉音高表）。
- scratchpad = `/tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad`（舊路徑 `/tmp/claude-0/-home-user/e6a64eea-98ea-5986-b96b-5cdbc5d1572e/scratchpad` 是它的 symlink；腳本裡沿用舊路徑）。

## 1. s01 照第 31 集 s41 實拍重核

看的是挑定的 s41（`colab/runs/e931-live/picks-merged.tsv`：9311101，0–3.833 秒）精修片 `/root/mokaair-work/videos/_live-e931/zhong-tian-qu-qi-e931-dh/runpod/a/st2/refined/s41.mp4`（1312×736、8 秒），抽 0、1.5、3.0、3.8 秒四格，並把家丁那一排放大三倍數人頭。

| 項目 | 原本 s01 寫的（照聖經 31→32 與 e031 r2.py 的 s41 文字） | 實拍 | s01 改成 |
| --- | --- | --- | --- |
| 二牛背影 | 左下前景、切在腰 | 佔左下約四分之一（x≈100–350／1280，頭頂約在畫面一半高），切在臀部，身子略朝右轉離鏡頭 | `filling the lower left quarter of the frame and cut at the hips`、`turned a little away from us toward the right` |
| 鋤頭 | 兩手舉在頭上 | 兩手高舉過頭，柄往左上斜，鐵刃在畫面左緣上方（3.8 秒時刃已出左緣，只剩柄） | `its handle slanting up to the upper left and its iron blade high at the left edge of the frame`；秦霜的扁擔頭頂在**鋤頭柄**下 |
| 家丁位置 | 土埂遠段的**頂上**，從畫面中間往左後 | **不在土埂頂上**：站在土埂右後方水塘的淺泥水裡、沿土埂排一排，最近的在畫面中間偏右（最高）、往左後越來越小 | `beyond the bank of sacks on the right, standing in one row in the shallow muddy water of the pond along the far side of the bank, from just right of the middle of the frame away to the left` |
| 家丁朝向 | 正面朝我們 | 三分之二朝畫左（看二牛） | `their faces three-quarter to screen left toward the young man` |
| 棍子 | 舉著 | 0–1.5 秒往前傾，剪點 3.833 時已豎直 | `their staffs held upright` |
| 人數與衣著 | 十二人，黑短打、黑頭巾、布鞋 | 約 13–15 人（放大數到 14–15）；黑短打、黑頭巾、黑褲、膝下白綁腿 | 新常數 `RETAINERS_S01`：**十四人**、白綁腿；`exactly sixteen people`（14＋二牛背影＋秦霜）。稿子的十二人改掉，免得 s41→s01 少兩三個人；家丁仍只在這個遠景（拍法 34） |
| 動作 | 扁擔往上一 `flicks` | — | 改 `jerks`（`flick` 在第 31 集起的「會長字」掃描裡；`prep932.sh` 一樣掃）；鋤頭往左飛、刃朝下插在**畫左緣**的土路上；「十二個家丁」改「水塘裡的十四人不動」 |

`r2.py` 同時改了：docstring 的〈TO RECHECK〉換成〈RECHECKED〉一段（實拍紀錄）、〈THE AXES〉第一場那句、HEAD 第二條、s01 的 zh（把「要重核」換成實拍的站位）。

前置時順手修的三處（不改台詞、不改鏡頭設計，都是機械檢查擋下的）：

1. s01、s20 的 motion 前面原本有 `NOBODY`（「Throughout the shot the set layout stays as it is. The pictures fix the place … never the mood.」）。有人物的鏡已有 extras 的「… never the mood.」，會變成 d1 分隔句出現兩次、精修文字的 `the set layout stays as it is. ` 也兩次 → 拿掉（第 31 集也只有沒人的鏡才用 `NOBODY`）。
2. 反過來，插鏡 s16、s25b 原本沒有 `NOBODY`，d1 一次分隔句都沒有 → 補上（第 30 集審稿：插鏡標準句）。
3. s20 `All four says` → `All four say`、motion 開頭大寫；祠堂地面 `grey stone flags` → `grey flagstones`（`flags` 在「掛著的東西」掃描裡，模型也可能讀成旗子）。

重 build（scratchpad `build932.sh`）：39 鏡（6 × 5 秒、20 × 6 秒、13 × 8 秒），`storyboard-check.py` 通過（script.md 37 鏡 210.5 秒、面板「秦霜 +12 → 41」），`shot_reading` 39 鏡、4 個陷阱全是 `cast.speaker`（s25、s26 系統、s25b 心裡話、s32 主觀畫外；拍法 15 `OFFSCREEN_SPEECH = False` 的預期結果，不是錯）。

## 2. d1 前置

做出的檔：

| 檔 | 內容 |
| --- | --- |
| `colab/runs/e932/extras.json` | 第一段的措辭修正：乾淨畫面句；二牛 `an honest, guileless face`、拿掉 `empty-handed`（他扛鋤頭）；石木匠短衣改 `faded light tan`（定妝照，審稿建議 10）、拿掉 `covered in wood shavings, calloused hands`（preflight `skin`：會畫成小點，拍法 12）。韓伯、石木匠 gen-dh 已送定妝照，不用補 portrait |
| `colab/runs/e932-live/mkspec.py` → `spec.json` | 種子 9321101／9321102；39 鏡全部有改。詳見 docstring |
| scratchpad `tools/prep932.sh` | 照 `prep931.sh` 的順序：免費圖逐位元重建比對 → 第一段吃錨點形式、精修文字放回 → st1 DRY（ref2manifest、extras_patch、`h3r.sh check`、preflight）→ pilot → retake → colab-jobs（絕對路徑）→ 逐鏡檢查 → preflight → `check_manifest.py` → `h3r.sh check` → 掃描。log：`tools/prep932.log` |
| scratchpad `tools/e932d1.sh` | 78 支 d1，G4、session `zt-live2`、跑兩輪補缺、跑完釋放 VM。**沒有執行**（只跑過 `DRY=1`：只查 manifest，0 錯） |

每鏡送的圖（`prep932.sh` 逐支比對）：

| 場景圖 | 鏡 |
| --- | --- |
| `set-shangyou-ba-fx-l1` | s01 |
| `-fx-lu-l1` | s02 s04 s07 s08 s10 |
| `-fx-shan-l1` | s03 s06 |
| `-fx-jiao-l1`／`-fx-ding-l1` | s05／s09 |
| `set-jingkeng-chen-l1`（清晨） | s11 |
| `-kou-chen-l1`／`-dui-chen-l1`（清晨） | s12 s14 s15／s13 |
| `set-jingkeng-l1`（傍晚，整張） | s20 |
| `-kou-l1` | s17 s18 s19 s22 |
| `-dui-l1` | s23 s25 |
| `-tian-l1` | s24 s26 s26b |
| `-di-l1` | s21；**插鏡 s16、s25b**（見下） |
| `set-citang-huang-l1` | s36 |
| `-huang-men-l1` | s27 s28 s30 s31 s37 |
| `-huang-qiang`／`-liang`／`-tang`／`-zuo`／`-zuo2` | s29／s32／s33／s34／s35 |

`set-liuxi-he-l1`、`set-citang-l1`、`set-shangyou-ba-l1`（沒翻的）、`set-citang-huang-zhuo-l1` 一支都沒送；清晨五鏡沒有任何金黃圖。

人物圖：許硯 angle-b 整集不送；全景 s10、s11、s36 只送定妝照；s26、s26b（gen-dh 只給兩張角度圖）換成先定妝照、後 angle-a。二牛近景 s03、s06、s18（gen-dh 只給 angle-a）換成定妝照；全景 s10、s20、s23、s25 只送定妝照。秦霜每鏡只送定妝照（`refs-dh` 沒有她的角度圖，gen-dh 不送；`r2.py` FOOT 原本寫「l1、angle-a」，已改成實際送的）。韓伯、石木匠只有定妝照。s01 二牛背影、過肩背影、肩上的人、插鏡的手、s36 門裡兩人、村民、家丁都不送圖、不點名。

### 插鏡 s16、s25b：「不送任何圖」做不到

`r2.py` 與任務要 s16、s25b「spec 不送任何圖」。但 H3 參考模式**一定要 1–9 張圖**：`check_manifest.py` 與 `h3r.sh check` 都報 `reference_images must list 1-9 images`，`retake.py` 的 `drop_set` 拿掉最後一張也會在改圖頭時出錯。所以每鏡只送**一張中性的圖**：乾裂土地的免費近裁 `set-jingkeng-di-l1`（俯看的乾田壟，沒有坑口、沒有坑邊、沒有人；審稿必改 2 擔心的是 `-kou` 從高處斜看磚坑，會長出「地上一顆人頭」），並把 d1 裡會讓它變成地點的兩句改掉：

- 場景句 `the location shown in <Picture 1> is the set, keeping its layout and props.` → `The dry earth shown in <Picture 1> gives only the colour and grain of the soil.`
- 插鏡標準句 → `Throughout the shot the framing stays as it is. The picture gives the colour of the earth only, never the mood.`（分隔句仍只出現一次）
- d1 的地點句拿掉（同第 31 集 s18、s21）：s16 從 `High-angle close shot looking straight down` 開頭，s25b 從 `Low orange evening light from the left` 開頭。

`prep932.sh` 掃這兩鏡：`well pit(s)`、`field`、`village`，再加 `pit`、`furrow`、`heap`、`willow`、`rim`、`row`、`Liuxi`、`the set`、`set layout`、`place`，都是 0。**風險**：s16 要的是暗的井底，`-di` 是亮橘色的乾田壟，草稿可能長出田壟；兩個種子都不像井底就請協調者決定：接受、改送別的圖，或照 `r2.py` s26 的備案改拍法。這是本集唯一跟 `r2.py` 原意不同的地方，**要協調者點頭**。

### 檢查結果（`tools/prep932.log`，最後一次 2026-11-18，連跑三次結果相同）

| 項目 | 結果 |
| --- | --- |
| 免費圖 | 22 張（壩 6、井坑 4＋清晨 3、祠堂 8＋整張）照 `shangyou_fx.sh`、`jingkeng_crops.sh`、`jingkeng_chen.sh`、`citang_huang.sh` 重建，跟 `refs-live` **逐位元相同**（這個容器原本沒有 scipy，`pip install scipy` 1.18.1 後才跑得動 `jingkeng_chen.py`、`citang_huang.py`；重建仍逐位元一樣） |
| 第一段 st1 DRY | 吃錨點形式；`check_manifest` 兩份 0 錯 0 警告；preflight 0 錯（8＋6 警告：扁擔、圖卷的紙、s36 的鋤頭、s07／s31 送了許硯帶笑的 angle-b——d1 已拿掉；石木匠的 skin 警告已由 extras 修掉）；精修文字放回且相符（`clips-dh-e932.json` sha256 開頭 `87c306f43af025e4`） |
| 支數秒數 | **78 支**＝39 鏡 × 2 種子；5 秒 12 支、6 秒 40 支、8 秒 26 支，共 **508 秒**；每支秒數＝`clips-dh` 的 BUY |
| 分隔句 | 78 支每支 `never the mood. ` 與 `One continuous shot.` 各剛好一次、順序對；`clips-dh` 39 鏡 `the set layout stays as it is. ` 各一次，三支沒人的鏡（s16、s25b、s32）`keeps the first frame's set layout and props.` 各一次 |
| d1 漏進精修句 | 0（沒有 `shown in <Picture N> keep(s) the same …`、沒有 `back to us; the set layout`） |
| `prompt_sha256` | 78 支全部跟檔案相符 |
| 兩個種子 | 39 鏡每鏡兩支提示詞逐位元相同 |
| 參考圖 | 全部絕對路徑、檔案都在、每支 1–9 張；圖頭的 `<Picture N>` 數跟送的張數一致 |
| 人與名字 | 每鏡送的人＝提示詞點的名字＝計畫；唐小棠、阿令、小禾等不在本集的名字 0 |
| 畫外的人 | 對畫外說話都寫 `toward someone out of sight beyond the left/right edge`（s03、s06、s09、s18、s30），GAZE_REFINE 的鏡沒有通用的 `person he/she is speaking to`；描述畫外的人 0；`<名字> off screen` 0 |
| 插鏡地點字 | 0（見上） |
| 光與場景 | 壩 s01–s10 霧白午後；清晨 s11–s15 沒有 `evening`、`orange`、`golden`、太陽方向；傍晚 s17–s26b 低斜橘光、沒有 `morning`；祠堂 s27–s37 燭光與門口暮色、沒有 `sky`（審稿建議）；蠟燭只在祠堂；牌位只在 s32–s36 且都寫素面 |
| 原版必修 | 二牛有出場的鏡都 `not smiling`；鋤頭每支最多一把、井坑場一把都沒有；`flushed` 只在 s24 秦霜的耳朵；沒有 `waterwheel`、`chopper`、`knife`；村民沒有 `grey-blue`；s33、s36 的八人有深梅紫與芥黃、沒有紅繩小辮 |
| 其他 | 沒有 `open`、單指、藍光／發光眼、`pan`／`track`／`crane`；秦霜的全景 s01、s10、s20、s23、s25 鞋句改成她穿皮靴；韓伯 s34–s36 的人物句沒有竹杖；石木匠淺褐、沒有木屑與老繭 |
| 掃描 | 否定名詞 0、會長字的名詞 0、掛著的東西 0（祠堂的牌位、扛在肩上垂下的手臂與垂柳枝不算） |
| `preflight-prompts.py`（d1） | **0 錯**、16 警告（`carrying pole` 7 鏡 × 2、s36 `a hoe` × 2：道具不在參考圖裡，第 30、31 集同樣接受） |
| `check_manifest.py`、`h3r.sh check`（d1） | 各 0 錯 0 警告 |
| `e932d1.sh` `DRY=1` | 0 錯（沒送） |

## 3. d1 要送的與估價

- **78 支、508 秒**（39 鏡 × 種子 9321101／9321102；5 秒 12 支、6 秒 40 支、8 秒 26 支）。Colab G4、session `zt-live2`（跑之前確認沒有別集在用）。
- 第 31 集實測：86 支、556 秒，21:16:38 開 session 到 23:51:53 跑完＝**2.59 小時**（含冷啟動與五次 launch 逾時重試），單支 1.1–1.4 分鐘，約 **26 CU**（G4 10.05 CU/小時；`e931d1.sh` 事前估 21–24 CU，實際偏高）。
- 第 32 集照支數與秒數比例（78/86、508/556）：約 **2.2–2.6 小時、22–26 CU，約 US$2.2–2.6**。餘額接近 400 CU 要先問站主（聖經〈還沒解決的〉1）。

## 4. 錄音待辦（沒錄：要站台 TTS）

36 句、6 個聲音（`video.json` 的 `voice`；音高範圍是聖經〈人物〉表的 YIN 中位數，第 43 條）：

| 聲音 | 角色 | 句數 | 音高範圍 |
| --- | --- | --- | --- |
| Umbriel | 許硯 | 11（含心裡話 a24、a26，主觀畫外 a32） | 88–145 Hz，心裡話同範圍 |
| Autonoe | 秦霜 | 8 | 195–240 Hz |
| Sadachbia | 王二牛 | 5 | 170–230 Hz（喊聲到 260） |
| Enceladus | 韓伯 | 6 | **還沒量**（聖經第 43 條、〈還沒解決的〉10）：第一次錄時量，要跟同場的石木匠差至少 3 個半音，量完補進〈人物〉表 |
| Schedar | 石木匠 | 3 | 110–175 Hz |
| Callirrhoe | 系統 | 3 | 照 `hailuo/local/voice-post.json` 後製 |

| 鏡 | id | 角色 | 句子 | 字 | 語氣 | BUY |
| --- | --- | --- | --- | --- | --- | --- |
| s02 | zq932a01 | 秦霜 | 打了，就是給錢家藉口。你想讓全村吃官司？ | 17 | 冷，不回頭 | 6 |
| s03 | zq932a02 | 王二牛 | 可水都被截了！不打，難道看著田乾死？ | 15 | 急，不笑 | 6 |
| s04 | zq932a03 | 許硯 | 秦霜說得對。錢員外就等我們先動手。 | 15 | 喘，很穩 | 6 |
| s05 | zq932a04 | 許硯 | 水，我們自己找。不靠他的壩，也要讓田見水。 | 17 | 穩 | 8 |
| s06 | zq932a05 | 王二牛 | 下游還有一口深潭，潭裡的水沒乾！ | 14 | 想到了 | 6 |
| s07 | zq932a06 | 許硯 | 潭在溝底，田在坡上，一擔擔挑，挑不活三畝田。 | 18 | 搖頭 | 8 |
| s08 | zq932a07 | 秦霜 | 別繞了，說人話。到底要怎麼做？ | 12 | 不耐煩 | 6 |
| s09 | zq932a08 | 許硯 | 挖井。就在田邊挖，挖到見水為止。 | 13 | 很穩 | 6 |
| s10 | zq932a09 | 秦霜 | 好，聽你的。都走，別在這裡讓人看笑話。 | 15 | 乾脆 | 8 |
| s11 | zq932a10 | 韓伯 | 第三天了，挖了十幾口，一口都沒見水。 | 15 | 蒼老，慢 | 8 |
| s12 | zq932a11 | 許硯 | 韓伯，待會日頭就毒了，您回樹蔭下歇著。 | 16 | 溫和 | 6 |
| s13 | zq932a12 | 韓伯 | 你一個秀才都要下去，老頭子哪坐得住。 | 16 | 篤定 | 8 |
| s14 | zq932a13 | 王二牛 | 許大哥，你沒挖過井，讓我下去！ | 12 | 急，不笑 | 6 |
| s15 | zq932a14 | 許硯 | 你挖了兩天了。這口換我，上面拉繩靠你。 | 16 | 累，穩 | 6 |
| s17 | zq932a15 | 秦霜 | 他下去多久了？上頭的人都沒換他？ | 14 | 皺眉 | 6 |
| s18 | zq932a16 | 王二牛 | 一整天了，叫他也不上來，剛才就沒聲了。 | 16 | 喘，擔心 | 6 |
| s19 | zq932a17 | 秦霜 | 沒聲了還等什麼？二牛，一起拉！ | 12 | 命令 | 6 |
| s21 | zq932a18 | 許硯 | 沒……沒水。再往下一丈，也許就有…… | 12 | 虛弱，眼睛半閉 | 8 |
| s22 | zq932a19 | 秦霜 | 都讓開。曬昏了，得馬上送回屋裡。 | 13 | 低聲，不耐煩 | 6 |
| s23 | zq932a20 | 秦霜 | 文弱書生，逞什麼能，挖什麼井！ | 12 | 罵，嫌棄 | 6 |
| s24 | zq932a21 | 秦霜 | 在樹蔭下指一指就好，偏要自己下去。 | 15 | 小聲，耳根紅 | 6 |
| s25 | zq932a22 | 系統 | 叮。秦霜，好感加十二。 | 8 | 冷，宣布 | 8 |
| s25 | zq932a23 | 系統 | 加十二。宿主差點死在井裡，才換到這些。 | 16 | 冷 | （同鏡） |
| s25b | zq932a24 | 許硯 | 死不了……換得到一口水，就值得。 | 12 | 心裡話，錄得近、輕，迷迷糊糊 | 5 |
| s26 | zq932a25 | 系統 | 秦霜好感，突破四十。獎勵箱開啟：水車圖紙。 | 17 | 冷，宣布 | 8 |
| s26b | zq932a26 | 許硯 | 水車……有了水車，深潭的水就上得來。 | 14 | 心裡話，錄得近、輕 | 6 |
| s27 | zq932a27 | 石木匠 | 圖是好圖。可這輪子，要三百斤好木頭。 | 15 | 粗啞 | 6 |
| s28 | zq932a28 | 許硯 | 我醒來就把它畫出來了。石師傅，這車做得出來嗎？ | 20 | 啞 | 8 |
| s29 | zq932a29 | 石木匠 | 做得出。料呢？三百斤的整木，村裡上哪找？ | 16 | 皺眉 | 6 |
| s30 | zq932a30 | 王二牛 | 村裡的大樹，去年秋天就砍光了。 | 13 | 悶，不笑 | 6 |
| s31 | zq932a31 | 石木匠 | 這麼大的料，村裡只剩一根，就在頭頂上。 | 16 | 壓低 | 6 |
| s32 | zq932a32 | 許硯 | 祠堂的梁……這是全村祖宗的屋頂。 | 13 | 畫外，愣住 | 5 |
| s33 | zq932a33 | 韓伯 | 許秀才，你們在門口說的，我都聽見了。 | 15 | 蒼老，慢 | 8 |
| s34 | zq932a34 | 韓伯 | 祖宗在上。求了三個月的雨，一滴都沒下。 | 16 | 篤定 | 8 |
| s35 | zq932a35 | 韓伯 | 柳溪全村，願拆祠堂的梁，給孩子換一口水。 | 17 | 一字一字 | 8 |
| s36 | zq932a36 | 韓伯 | 許秀才，祖宗的梁拆不拆，由你來說。 | 14 | 回頭 | 8 |

沒有台詞的鏡：s01、s16、s20、s37（各 5 秒）。

錄音那天照第 31 集的順序（`tools/rec931.sh` 的寫法，跑之前先跟協調者說）：

1. 寫 `tools/rec932.sh`：`hailuo/local/lines.mjs` 從 `video.json` 的暫存副本錄 `zq932a01`–`zq932a36`，一句一次呼叫，輸出 `/root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/audio`。
2. 讀音提示檔 `e932-tts-hints.json`（只給 TTS，`video.json` 與字幕照原字）。要先聽寫確認的多音字：a06「一擔擔」（dàn）、a19「得馬上」（děi）、a11「待會」（dāi）、a08「為止」（wéi）、a24「換得到」、a26「上得來」、a29「做得出」（de）、a18「一丈」。聽寫對了就不加提示。
3. faster-whisper 回聽（照 `fw931.py`：一次一支、單句與帶上下文都聽）、YIN 音高（照 `f0y931.py`）：超出範圍半個範圍以上就 `rubberband=pitch=…:formant=preserved` 調回，變調後帶上下文再聽一次（第 43 條）。**韓伯 6 句先量**，跟石木匠（Schedar 110–175 Hz）差不到 3 個半音就調其中一個，量好的範圍補進聖經〈人物〉表。
4. 人聲長度照 `tools/span931.sh`（`silencedetect -35 dB、0.15 秒`）量每句，跟上表 BUY 比：6 秒的鏡實際出片約 6.58 秒、5.9 秒以內放得下（第 43 條）；s25（兩句系統，25 字）、s28（20 字，啞）、s21（兩個長停頓）、s35（一字一字）最可能超。超的改 `r2.py` 的 `BUY`、重 build、**重跑 `prep932.sh`**（秒數與 `prompt_sha256` 都會變），再跑 `e932d1.sh`。也可以先開拍 d1（草稿不需要錄音），錄音後只重買放不下的鏡。

## 5. 還擋著開拍的事

1. **協調者要點頭插鏡 s16、s25b 的做法**：送一張 `-di` 乾土圖當「土的顏色」，不是 `r2.py` 寫的「不送任何圖」（H3 做不到）。
2. **花錢的決定**：`e932d1.sh` 約 22–26 CU（約 US$2.2–2.6），要站主或協調者同意，並確認 Colab 餘額與 `zt-live2` 沒有別集在跑（第 31 集正在剪：工作樹裡有別人的 `e931cut.sh`、`edit-dh-e931-live.json`、`assemble-v4.mjs` 改動，跟本集無關，我沒碰）。
3. **錄音沒錄**（站台 TTS）：不擋 d1 草稿，但擋挑片的對嘴與剪接；韓伯的音高還沒量。BUY 錄音後要照 `span931.sh` 重核，放不下就改 BUY 重跑 prep。
4. s01 的家丁人數照實拍寫十四人（稿子十二人）：如果協調者要守稿子的十二人，改回 `RETAINERS` 並把 `exactly sixteen people` 改 fourteen，重 build、重跑 prep。
5. 備註：`colab/runs/e932/extras.json` 在別人的 WIP commit `0483945fa` 裡是第一次試跑時產生的佔位 `{}`；現在工作樹裡是真的版本，還沒 commit。
