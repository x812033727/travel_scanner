# 第 36 集真人版 fix4：s22 三雙新鞋、s23 虎口的繭

第三輪修片代理 2026-11-21 寫（REVIEW 3，品質優先）。依據：`../cut-review.md`（審 1：中等 7、輕微 8、中等 2）、`../cut-review-2.md`（審 2：中等 4、輕微 4）、`../review3-plan.md`、
範本第 35 集 `../../e935-live/fix4/`、本集 `../fix3/`。沒用 RunPod、付費圖、站台 TTS；沒 commit。

## 兩鏡 4 支、24 秒（英文全文在 `mkjobs.py`）

| 鏡 | 種子 | 秒 | 圖 | 寫法 |
|---|---|---|---|---|
| s22 | 9361241、9361242 | 6（= BUY） | 只送 `set-shanjiao-qu-di-l1`（乾裂渠底，照 d1） | d1 只有**兩雙**新布鞋（另一支 9361102 一雙），台詞、s30、s32、s34 都說三個人。改成「**一排正好六雙**，由左到右：草鞋、草鞋、新布鞋、新布鞋、新布鞋、草鞋」，數字在構圖與 only 句各寫一次；景別放寬一點、六雙兩邊都留土；**大家站在原位**（d1 的「新鞋一起往前一步、草鞋跟上」會走出框），只讓三雙新鞋原地小小挪一下重心、揚一點土；**固定鏡** |
| s23 | 9361241、9361242 | 6（= BUY） | 只送 `set-shanjiao-qu-an-l1`（照 d1） | d1：兩次 5–6 格內換握（cut-jumps 三處）、虎口被柄擋住看不到繭、四個指節都長出「十」字刻紋（d1 的 `one long pale old scar across two knuckles`）。改成**從下面握柄、手心與虎口朝鏡頭**、拇指與食指張開繞著柄，虎口與指根一大片厚而粗、發黃的硬皮「plainly seen」；**疤那句拿掉**（不寫 scar／callous／cross）；寫「one thumb and four fingers」；**整鏡同一個握法**：慢慢握緊、再一個慢而穩的動作把鋤頭往下壓進土裡停住（拿掉 d1 的「鬆開再握回」）；**固定鏡** |

**s06／s12b 不重拍**：剪接表左錨放大 1.40 把前景的蝴蝶結髻整個裁出畫面（`../review3-plan.md` A2），只在幾格右緣留一點虛的髮與頰邊，讀成過肩近景。站主若要更清楚的畫面（放大後是 1312 寬的 0.71 倍再放大，偏軟），
可以照下面的寫法再抽（約 0.6 CU，四支）：d1 s06／s12b 提示詞裡前景唐小棠後腦那句換成 s07 的雙丸子寫法（`two round buns, a pink ribbon wrapped round each`），不送任何有蝴蝶結的圖，其餘照 d1、加 NOSMILE。

## 免費檢查（全 0）

```
python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/fix4                     # 4 jobs, 24 s, scan 0
python3 -I ../../_scripts/preflight-prompts.py <live>/fix4/colab-jobs.json                                      # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix4/colab-jobs.json                 # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix4/colab-jobs.json               # 0／0
```

`mkjobs.py` 的掃描：d1 提示詞 sha256 對 d1 的 `colab-jobs.json`；每個要換的句子在 d1 裡正好一次；推鏡、cinema camera、reverse grip、loosens、step forward 都不在；
scar／callous／tattoo／cross、笑字、會長字或掛著的東西、blood、open、否定名詞都 0；分隔句各一次；必含句在；圖與秒數照 d1；種子沒在 d1／fix1–fix3 用過。

## 送出

`bash <scratchpad>/e936f4.sh`（照 `e936f3.sh`：查別的 driver 與 session → `check_manifest`＋`preflight` → zt-live3 G4 → 兩輪補缺 → `ONLY_SELF=1 colab-release.sh zt-live3` → sessions／usage）。

## 跑完之後（挑片與精修）

1. 一人挑（寫明），兩支並排每 0.25 秒抽格，跟目前的 d1 9361101 比：
   - s22：數得出三雙新黑布鞋、三雙草鞋，整鏡六雙都在框裡、沒有多出或走出去的腳；沒有字。
   - s23：手心與虎口朝鏡頭、虎口一片發黃硬皮讀得出；五指、沒有「十」字刻紋或疤；整鏡沒有 5–6 格內的大位移（cut-jumps 0）。
   寫 `review-picks.tsv`（`shot	choice	reason`，choice 是種子或 `KEEP`，剪點 start@／end-before@，台詞 a22 c0.60–4.45、a23 c0.60–5.32 要放得下）。
2. 比 d1 好才換：`SESSION=zt-live3 PREP=1 PRECHECK_ONLY=1 ONLY=s22,s23 bash <scratchpad>/e936refine.sh`（讀檔順序已含 `fix3..fix9/review-picks.tsv`，`SRC` 表 `124` = fix4），
   再 `SESSION=zt-live3 ONLY=s22,s23 bash <scratchpad>/e936refine.sh`；核 `.seed`、1312×736、格數等於草稿。跑完 `ONLY_SELF=1` 釋放、核 assignments 0、未記名 VM 手動釋放。
3. 換了 s23 就拿掉剪接表 `vf` 的 s23 凍格（scratchpad `e936c/mkov936.py`），重跑 `bash ../e936cut.sh`。

## 結果（2026-11-21）

- **跑**：送前 `colab sessions` 沒有 session、沒有別的 driver、assignments 0、餘額 **222.25 CU**；`e936f4.sh` 一輪 4/4（s23-9361242 第一次 launch 逾時 180 秒，自動第二次成功），
  `ONLY_SELF=1 colab-release.sh zt-live3` 之後 sessions 空、assignments 0、rate 0；餘額 **220.57 CU（fix4 草稿 1.68 CU）**。片在 `<live>/fix4/out/`，log `colab-run-1.log`。
- **挑片**（`review-picks.tsv`；**只有第三輪修片代理一人挑**，scratchpad `e936r3/look/f4-*.jpg`、`s22ab.jpg`、`s23c.jpg`）：
  - **s22 → 9361242**：前排四雙（草鞋、新黑布鞋、新黑布鞋、草鞋）＋兩雙新鞋中間的後排一雙新黑布鞋＝**新鞋三雙**（五雙腳，不是寫的六雙）；新鞋的人纏白綁腿、草鞋的人光腳，整鏡站著、固定鏡。
    比 d1 的兩雙好；第三雙半遮在後排，要細看。9361241 新鞋又只有兩雙、腳下多一張草蓆。
  - **s23 → 9361241（要人眼決定換不換）**：沒有 5–6 格換握、沒有十字紋、五指正常，c0–1.0 手心朝鏡頭、c0.5–1.5 慢慢握住；但掌心那塊「繭」像沾了一塊黃粉、手比 d1 嫩。
    9361242 掌心一塊像貼上去的方形砂紙、c2.0–2.5 拇指翻轉怪，不用。
- **還沒做**：精修（`e936refine.sh`，s22＋s23 約 1–2 CU）與換進成片——等協調者決定；s23 換的話記得拿掉剪接表 vf 的凍格。
