# 第 31 集真人版 fix3：重拍 s23（碗裡變成白飯插芽）

2026-11-18 寫好，**還沒送出**（要花 Colab 點數）。送出腳本是 scratchpad 的 `e931f3.sh`，用 Colab G4、session `zt-live2`，跑完以 `ONLY_SELF=1` 執行 `colab-release.sh zt-live2`，只停掉、釋放 zt-live2 自己那台。拍完、挑好之後只精修 s23 的腳本是 scratchpad 的 `e931f3refine.sh`（同樣要花錢，也還沒跑）。
站主：「品質比較重要」，重拍 s23。

## 為什麼重拍

- 成片審查 1（`../cut-review.md` 輕微 3）：s23（成片 112.37–117.54）碗裡是「一碗雪白、像煮熟的米飯，上面插幾根長芽」，s21、s22 是金黃帶殼稻種冒白芽，s22→s23 硬切相鄰，看得出顏色變了。
- 成片審查 2（`../cut-review-2.md` 中等 2）：碗裡是一堆隆起的白色東西，上面直直插著三根白芽，從 112.4 到 117.5 秒都看得到，觀眾會讀成白飯插香，跟「出芽」的喜事接不上。
- 挑片時（`../picks-merged.tsv`）只記了「芽偏長」，沒看出顏色。

## d1 實際拍成什麼樣（2026-11-18 抽格，scratchpad `e931f3/*.jpg`、`e931f3/bowls.jpg`）

- 9311102（現在用的那支）與它的精修片：許硯一個人中近景，左手把紅陶碗托在畫面右下。碗裡是隆起的雪白一堆，三根白芽直直插著，芽頭帶一點黃綠。兩支種子都一樣。
- 前後鏡碗的實際樣子：
  - s21（d1 9311101）：從上往下看，手掀起濕白布，碗裡鋪滿金褐帶殼稻種，表面平，幾根細白芽平躺在穀上。
  - s22（fix2 9311301）：許硯雙手把碗捧在胸前，碗口下是金褐稻種，表面平，中間一小撮細白芽，濕布沒蓋在碗上。
  - s24（d1 9311102）：碗又蓋著白布，許硯雙手拿著。
- 原因：d1 把碗寫成 `one red clay bowl holding a layer of rice grains, each grain with one tiny white sprout`。
  - `rice grains` 沒寫帶殼、也沒寫顏色，模型就畫成煮好的白米。
  - `each grain with one sprout` 讓芽一根根插著、站起來。

## 新提示詞的重點

底稿是 d1 選定那支（9311102）的提示詞。`retake.py` 從 `live/st1` 開始，先套 d1 的修改（原樣取自 `../spec.json` 的 s23：拿掉 angle-b、換 `-han-wu-l1`、兩句 replace），再套 fix3 的三處修改。`mkspec.py` 確認 st1 加上 d1 修改後，就是 d1 的 `ref-s23-9311102.txt`。`mkjobs.py` 把 fix3 的修改倒回去，確認得到的也是這個檔，逐位元相同。

1. **碗照 fix2 s22 那句寫**。這句已由 9311301 驗證過，`mkjobs.py` 也會確認這幾段字確實出現在 fix2 的 `ref-s22-9311301.txt` 裡：
   - `one red clay bowl filled level to just below its rim with plump golden-brown unhusked rice seeds`
   - `about ten short thin pure-white sprouts scattered evenly over the seeds, each sprout as long as one rice grain and as thin as a thread, lying flat on the seeds against its own grain, the surface of the seeds flat and level from rim to rim`
   - 持法照原 s23：`held in his left hand at the bottom of the frame`。另加一句 `tilted a little toward us so that the flat golden top of the seeds shows`：中近景裡碗在下緣，從側面看只看得到碗口那一圈，讓碗朝鏡頭斜一點，才看得見金黃的平面。
2. **芽靜躺、到最後一格都是一粒米長**：動作句後面加上 `the bowl stays in his left hand at the bottom of the frame, its golden seeds and their short white sprouts lying still and flat, each sprout keeping its one-grain length from the first frame to the last`。最後半句跟 s22 一字不差。
3. **濕布**：s22 的提示詞寫 `the wet cloth over his left wrist`，碗沒蓋。s23 緊接在 s22 後面，用同一句、碗不蓋，跟 s22 接得上。s24 碗又蓋上布，這是兩份審查都判為接受的時有時無（審查 1 第 2 條、審查 2 第 7 條）。不在 s23 加「把布蓋回去」：一鏡一個動作，稿子 c30 才蓋回去。
4. **臉不寫笑字**：d1 寫 `sobering, not smiling`，兩位挑片的人都說沒笑。照 fix2 的做法連 `not smiling` 也拿掉，改成 `sobering and grave`，再補上 `the corners of his mouth level`。d1 原有的幾個部位（眼裡的暖意收掉、眉頭收起、嘴隨字動）照留。
5. **其他照 d1**：
   - 一個人的中近景，`he is the only person in the frame`。
   - 唯一的動作是眼睛從碗抬到畫右外乾裂的地（分鏡 c23「只拍抬眼」）。
   - 台詞照劇本原句「芽是醒了，可田裡沒水，插下去也活不了」，看得到嘴，用新片的片中原聲；錄音 a22（3.77 秒）是退路。
   - 慢推：d1 推到最後碗仍在畫內，不改。
   - 圖：許硯定妝照、angle-a、`set-xujia-yuan-han-wu-l1`。6 秒，960×544。種子 9311401／9311402。
- 只寫碗裡有什麼，沒有否定名詞。不寫葉、苗、莖、綠、長高，也不寫堆、隆起、煮熟、白米。

## 檔案與指令

```bash
cd docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e931-live/fix3
L=/root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live
python3 -I mkspec.py                                   # spec.json; checks st1 + d1 edits rebuild d1's 9311102 prompt
python3 -I ../../_scripts/retake.py $L/st1 $L/fix3 spec.json
python3 -I mkjobs.py $L/fix3                           # colab-jobs.json + the scans
python3 -I ../../_scripts/preflight-prompts.py $L/fix3/colab-jobs.json
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest $L/fix3/colab-jobs.json   # from the repo root
bash /tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/e931f3.sh        # SENDS (paid): only when the owner says so
```

輸出：`$L/fix3/colab-jobs.json`（2 支），提示詞在 `$L/fix3/prompts/ref-s23-931140{1,2}.txt`，片子會出在 `$L/fix3/out/s23-931140{1,2}.mp4`。

`mkjobs.py` 的掃描（2026-11-18 全部 0）：

- 底稿就是 d1 選定那支，逐位元相同。
- 否定名詞。
- 任何笑字（smil、grin、laugh、beam），`not smiling` 也算。
- 舊的失敗句已拿掉：`holding a layer of rice grains`、`each grain with one tiny white sprout`、`not smiling`，以及 d1 s22 的芽尖句。
- 碗裡不得出現：葉、苗、shoot、莖、梗、plant、綠、長高、子葉，也不得出現 heap、mound、pile、cooked、steam、white rice、rice grains。
- 不得出現武器、鎬、incense（香）這類字。
- s22 的碗句各出現一次，而且確實是 fix2 9311301 自己的字。fix3 自己的新句各出現一次，而且 d1、fix1、fix2 都沒有。
- 寫了人數（`he is the only person in the frame`）。
- 碗寫在第一格的構圖句裡。
- 動作句、台詞照 d1，各出現一次。
- 鏡頭照 d1 慢推，只出現一次。
- 會長出字的詞（含 open）、掛起來的東西、辮子、尾巴、垂下來的詞。
- 不在畫面裡的人被點名（只能有許硯）。
- 圖、秒數、`<Picture N>` 與檔頭。

檢查結果（2026-11-18）：

- `mkjobs.py` 掃描：0。
- `preflight-prompts.py`：0 error(s)、0 warning(s)。
- `h3r.sh check --manifest`：0 error(s)、0 warning(s)。
- `minimax-h3-colab` 的 `h3.sh check`：0 error(s)、0 warning(s)。

## 挑片時要看的

- 碗裡是不是金褐帶殼稻種、表面平，白芽有沒有平躺、一粒米長。每 0.5 秒放大看一次，看芽有沒有站起來、變長、變綠，碗裡有沒有變成白的一堆。要跟 s22 fix2 9311301 並排比顏色。
- 碗有沒有一直在畫內、在左手上；濕布是不是在左手腕、沒蓋到碗上。
- 許硯不笑：嘴角平、眉頭收起；眼睛有沒有從碗抬到畫右外。
- 原聲是不是完整一句、沒有多出來的人聲，用 20 ms RMS 與聽寫確認，跟 d1 挑片一樣。
- 寫進 `review-picks.tsv`：剪點只寫 `start@`、`end-before@`，而且只寫給選定的那支。兩支都不行時寫 `KEEP`（留 d1 9311102），不寫 RETAKE。

## 挑好之後

1. 跑 scratchpad 的 `e931f3refine.sh`（要花錢）。要先免費檢查一次，就用 `PRECHECK_ONLY=1`。這支腳本會：
   - 確認 2026-11-18 做的備份在。備份在 scratchpad `e931f3r/bak`，內容是 picks.json、live-clips-e931.json、st2-*.json、43 個 st2 提示詞，以及 d1 精修 `refined-s23-9311102.mp4`（md5 `fe68252e…`）。
   - 以 `picks-merged.tsv fix1/ fix2/ [review3-trims.tsv] fix3/review-picks.tsv` 的順序重跑 `refine-prep.py 31`。
   - 把 `e931refine.sh` 對 s04、s24 開頭的改寫放回去。
   - 確認除了 s23 以外，42 個挑片與 st2 提示詞都跟備份一樣，s23 的精修提示詞帶著 fix3 的碗句。
   - 只精修 s23，再用 `ONLY_SELF=1` 釋放 zt-live2。
2. 精修完，在 `../e931cut.sh` 的 want 與 seed 表把 s23 改成新的種子與剪點，然後重剪（`stage.py 31` 會因為 picks.json 比較新而自動重跑）。
