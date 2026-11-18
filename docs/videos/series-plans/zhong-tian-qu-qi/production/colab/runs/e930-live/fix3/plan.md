# 第 30 集真人版 fix3：重拍 s07（秦霜在院門攔下唐萬金）

2026-11-18 寫好，當天送出（兩支都出片），已選 **9301402**，換進成片（`review-picks.tsv`；結果見 `../review3-plan.md`〈s07 重拍〉）。送出腳本：scratchpad `e930f3.sh`（Colab G4、session `zt-live`，跑完執行 `colab-release.sh`）。

## 為什麼重拍

- 成片審查 1（`../cut-review.md` 中等 1）：s07（成片 31.46–36.92）秦霜的右手從第一格到最後一格都握著唐萬金的左手指，臉朝他，而且帶笑（32.4、34.0、36.85 秒嘴角上揚）。台詞是她攔門問「小棠，這位老爺是誰？一進門就東張西望」，畫面會讓人以為兩人很親，或是一起來的。這也是秦霜在本集第一次出場。稿子 c07 寫的是「秦霜撐著門板，擋在他半步前；嘴在說話，不笑」。
- 成片審查 2 說秦霜在 36.0–36.5 秒笑開，當時判為接受。
- REVIEW 3（`../review3-plan.md`）先把畫面放大 1.42 倍裁切，牽著的手全鏡出畫；但前 1 秒她伸過去的前臂與黑手套還留在下緣，帶笑也還在。
- 站主：「該修就修，品質比較重要」。

## d1 實際拍成什麼樣（2026-11-18 每秒抽一格看，scratchpad `e930f3/s07-930110{1,2}.jpg`）

- 9301101（現在用的那支，`../picks-merged.tsv`）：兩人並肩站在院門前、身體都朝鏡頭。她在畫左，左手握著他的左手腕或手指，六秒都沒放開。她開口時嘴角上揚，他頭往畫右看院子。
- 9301102：同樣並肩面向鏡頭，她挽著他的手臂，比 1101 更糟。
- 原因，對照 d1 提示詞：
  1. `her left arm already held out across his way`：這句寫的是「一隻伸向他的手臂」，模型讓這隻手落在他的手上。
  2. `blunt and wary, not smiling: brows level`：用否定句寫不笑，臉又只寫成中性。任務檔記錄第 11 集 fix2 的教訓：寫「不笑」擋不住，第 12 集起要寫具體的冷硬動作。
  3. 他寫的是 `facing us`，她寫的是 `half a step before him and a little to the side`：兩人肩並肩朝鏡頭站，看起來就是一對。

## 新提示詞的重點（只用正面描述，沒有任何 smile 字，也沒有否定名詞）

- **面對面，中間隔一步**：`they stand face to face across one full step of bare packed earth, a clear gap of low golden evening light between her shoulder and his from the first frame to the last`。她的臉朝畫右、轉四分之三看他，他的身體朝畫左、轉四分之三對著她。
- **她的兩隻手都放在離他遠的那一側**：左手掌平貼在左邊門柱上，高度到肩（對應稿子的「撐著門板」，也接 s08 的「one hand on the swung-back plank gate」）；右拳撐在腰帶旁的胯上。她 `standing square in his way`，正面擋住他的去路。說台詞時再寫一次「整句話手都在門柱和胯上」。
- **他兩臂垂在身側**：`both his arms straight down at his sides, his hands loose against his thighs`，動作句結尾再寫一次 `his arms still at his sides`。
- **兩人的手各在原處**：`her hands stay on the gatepost and on her hip, his hands stay at his sides`。
- **冷臉逐部位寫**：眉壓低、往中間皺，眼睛瞇起、目光冷硬、盯著他的臉，字與字之間嘴抿平，下顎繃住，下巴平；最後一個字說完，嘴收回一條緊抿的直線。
- **一鏡一個動作**：唯一的身體動作是 d1 原有的那個：唐萬金把頭從畫右慢慢轉到畫左看院子，最後視線停在她臉上（台詞「東張西望」說的就是這個）。他嘴閉著。秦霜站姿不動，只說話。
- **景別**：中景雙人，從大腿中段往上取景，頭頂留空。比 d1 的膝上景別近，臉比較大，表情才撐得住（第 1 集 fix6 的教訓）；她撐在胯上的拳頭和他垂在大腿邊的手仍在畫內。
- **鏡頭**：`The camera holds a static shot.`（取消 d1 的慢推：大腿以上的雙人鏡往前推會切到頭和手，固定鏡頭也讓兩人之間那一步的距離一直看得清楚）。
- **接前後鏡**：
  - s06：廣場，午後。他朝畫右的大車甩袖。
  - s07／s08：院子，傍晚，在院門邊。光與地點那句沿用 d1 原句：低斜陽從右上後方照來，影子往左下拉長；院門在後牆，屋角在左，禿樹在右。
  - s08 秦霜在畫左三分之一，所以這鏡她也在左、他在右，跟 d1 同一邊。
- **參考圖照 d1**：`qinshuang-portrait-l1`、`tangwanjin-portrait-l1`、`set-xujia-yuan-dong-men2-l1`。
- **規格**：6 秒、960×544 Ref2VA，跟 d1 一樣。台詞照稿子原句，只有她說，聲音用片中原聲。種子 9301401／9301402。

## 檔案與指令

| 檔案 | 內容 |
| --- | --- |
| `mkspec.py` | 從 st1 的 `ref-s07.txt` 改寫，寫出 `spec.json`。s07 在 d1 只換了場景圖、沒改提示詞，所以 st1 的提示詞＝d1 的提示詞，已用 cmp 確認逐位元相同 |
| `spec.json` | 種子、場景圖替換、四組 replace、6 秒 |
| `mkjobs.py` | retake.json → `colab-jobs.json`：圖片路徑絕對化並檢查檔案存在，再做以下掃描 |

`mkjobs.py` 的掃描項目：
- 否定名詞
- open 與會長出字的詞
- 掛起來、鎖、攤子類的詞
- 笑的詞
- 武器的詞
- 讓手伸向對方或讓兩人並肩的詞：hold his hand、clasp、grip、wrist、reach、held out、side by side、shoulder to shoulder、facing us
- 點名了不在畫面裡的人
- 分隔字串各出現一次
- fix3 的新句子各出現一次，而且不在 d1 裡
- d1 失敗的句子已經拿掉
- 台詞只出現一次
- 不動鏡頭
- 圖、秒數、畫布

```bash
cd docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e930-live/fix3
L=/root/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/runpod/live
python3 -I mkspec.py
python3 -I ../../_scripts/retake.py $L/st1 $L/fix3 spec.json
python3 -I mkjobs.py $L/fix3
python3 -I ../../_scripts/preflight-prompts.py $L/fix3/colab-jobs.json
cd /home/user/zt-work && bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest $L/fix3/colab-jobs.json
```

輸出：`$L/fix3/colab-jobs.json`（2 支）、`$L/fix3/prompts/ref-s07-930140{1,2}.txt`（868 字，sha256 `da2ab65b…aa8b7`），片子會出在 `$L/fix3/out/s07-930140{1,2}.mp4`。

## 檢查結果（2026-11-18）

- `mkjobs.py` 掃描：0
- `preflight-prompts.py`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest`：0 error(s)、0 warning(s)
- `minimax-h3-colab` 的 `h3.sh check`：0 error(s)、0 warning(s)

## 拍完之後

1. 每秒抽一格，再放大逐格看：
   - 兩人的手有沒有碰到（看 0–1 秒、每 0.5 秒一格）
   - 她嘴角有沒有上揚，看 32.4、34.0、36.85 秒對應的片段時間與句尾
   - 中間那一步的距離在不在
   - 她的手是否一直在門柱和胯上
   - 他是否看鏡頭
   - 片中原聲是不是稿子原句（用聽寫核對）
2. 挑片寫 `review-picks.tsv`，格式照 fix1：
   - choice 欄只能填種子、KEEP 或 RETAKE
   - 剪點寫在 reason 欄，只用 `start@`／`end-before@`
   - 理由裡提到舊剪點不要加 `@`
   - 不要寫 `crop=`
3. 兩支都不行：寫 **KEEP**（保留 REVIEW 3 的 1.42 倍裁切 9301101），不要寫 RETAKE，否則成片會少一鏡。
4. 換上新的那支以後，以下都要照新片段重新量：
   - `refine-prep.py 30` 的挑片檔順序：fix3 要排在 `review3-trims.tsv` 後面
   - REVIEW 3 加在剪接表的 s07 `vf` 裁切（`crop=1352:760:364:0,scale=1920:1080…`，在 scratchpad `e930c/overrides.json`，見 `../review3-plan.md` 第四節第 4 條）要拿掉
   - 剪點、`voice_skip`／`voice_until`、院門音效的 `off`
   - 秦霜 s07 對 s36 的音高（原本 214–224 對 242–260 Hz）
