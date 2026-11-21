# 第 9 集真人版 fix-polish：上架前精修重拍（2026-11-21）

依 `/root/mokaair-work/review-zt/RETAKE-BRIEF.md`。審片：`review-zt/reports/e009.txt`、`consolidated/retakes.json`（e009 的 A、B 三鏡）。
種子 9099101、9099102，960×544 Ref2VA。只寫了提示詞與 spec，沒有送出任何工作。

base：`picks.json` 沒有 `motion_from` 欄，三鏡的 `draft` 都在 `d1/out/`，所以 base 是 `d1/prompts/ref-sNN-<選中的種子>.txt`
（d1 兩個種子的提示詞逐位元相同）。參考圖三鏡都照 base，`pictures` 留 null。

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊→新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- | --- |
| s30 | A（嚴重） | 阿令手上的匕首變成 50–60 公分有護手的直劍、劍尖朝上；她的臉瘦長偏老，跟 s28、s32 不像同一人 | `d1/prompts/ref-s30-9091102.txt`，6 秒 | ① 景別句補 `both faces large and sharply lit by the candle`（臉大一點，長相才撐得住）。② 阿令：拿掉 `no shackles`；補 `the same young woman of twenty as in <Picture 1>, her youthful face smooth and fresh with the same phoenix eyes`；冷臉逐部位寫成眉間一小道皺、眼瞇盯著他的臉、嘴抿平、下顎繃住（原本 `brows drawn together … no smile`）。③ 刀：`one dagger … about a palm long … raised in her left hand` → 左手正握、**腰的高度、刀尖平指他**的小匕首：直的單刃鐵刃一掌長、刀尖只比拳頭多一掌寬、黑布纏的木柄握在拳裡、整把比前臂短、刃朝他背朝外；右手空著垂在身側。④ 拿掉 `no other blade and no other weapon anywhere in the frame`（否定名詞）。⑤ 動作：`takes one step back …, the dagger … still raised toward him, and her brows knit tighter` → 只做一件事：小退一步、重心落到後腳，刀維持腰高平指他（拿掉第二個動作「眉再皺緊」）。⑥ 許硯：`the bedding bundle in both arms` → 抱著灰藍粗布、麻繩綁的鋪蓋 | 無 | 改成腰高平指，是因為 d1「raised」被畫成豎著朝上的長劍；稿子寫「刀沒放下」，腰高平指仍是舉著對他，審片建議的是胸口高。臉漂的原因不確定：參考圖跟 s24、s28（臉對）同一組（定妝照＋角度 a、b），所以沒拿掉角度 b（正側面那張木簪不見）；兩支都還像別人的話，下一輪考慮拿掉 `aling-angle-b-l1` |
| s02 | B（中等） | 全集第一句模型原聲多「寧親」兩字，像口吃 | `d1/prompts/ref-s02-9091101.txt`，8 秒 | 主要是換種子重抽（審片：動作不用改）。提示詞只補：台詞後 `saying the whole line once at an even, unhurried child's pace, each word clear and said a single time`；動作 `throws her left arm out wide …` 後補 `then plants her feet and holds that pose while she talks`；認真臉補 `chin lifted, lips pressed firm` | 無 | 聲音口吃是模型隨機的，提示詞的幫助有限；挑片要用聽寫逐字對「哥，昨天成親你躲去睡柴房，今晚不准再躲」 |
| s07 | B（中等） | 進門全景的鋪蓋是紫紅外皮、米白內捲（前後鏡是灰藍粗布、麻繩綁） | `d1/prompts/ref-s07-9091101.txt`，8 秒 | ① `the bedding bundle under his left arm and the brass candlestick in his right hand` → 鋪蓋寫死：暗灰藍粗棉布、捲緊、兩端捲層也只看得到灰藍、兩道褐色麻繩、前臂長、夾在左臂；燭台補一根點著的白蠟燭。② 動作 `shoulders the door open and steps into the room` 後補 `the grey-blue bedding roll still tucked under his left arm`。審片句裡的 `not pink, not cream` 沒用（否定名詞） | 無 | 房裡的粉被、唐小棠的粉色衣服可能把顏色帶到鋪蓋上；場景圖沿用 `set-xujia-tangfang-l1`（跟 s08–s18 同一張），沒換 l2 |

## 檢查（2026-11-21）

- `polish-build.py 9`：`e909: 3 shots, 6 drafts, 44 s`，0 錯誤。
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)。

總草稿秒數 44 秒（(6＋8＋8)×2）。

## `polish-build.py` 的兩個毛病（沒改原檔，回報協調者）

1. `REPO = HERE.parents[6]` 算到 `/home/user/zt-work/docs`，參考圖路徑變成 `docs/docs/...`，每張圖都報 `no picture`。應是 `parents[7]`。
   這次用 scratchpad 的副本跑（只改這一行，並把 `HERE` 釘在原本的 `_scripts`），其餘一字不改。
2. 它在檢查錯誤之前就把 `fixp/prompts/ref-sNN-SEED.txt` 寫出去，而 `used` 又掃 `*/prompts/ref-*`（含 `fixp/` 自己），所以失敗一次或重跑一次，
   就會報「seed already used for this shot」。重跑前要先刪 `fixp/prompts/ref-s*-909910*.txt`（這次就是這樣做的）。
