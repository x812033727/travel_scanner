# 第 31 集真人版 fix2：重拍 s20、s40、s22（從 fix1 選定那支改寫）

2026-11-18 寫好，**還沒送出**（要花 Colab 點數）。送出腳本是 scratchpad 的 `e931f2.sh`，用 Colab G4、session `zt-live2`。第 30 集 fix3（`e930f3.sh`，session `zt-live`）可能同時在跑，所以這支腳本用自己的 session。跑完以 `ONLY_SELF=1` 執行 `colab-release.sh zt-live2`，只停掉、釋放 zt-live2 自己那台，不動 zt-live，也不動沒有登記名字的 `[?]` 機器。
站主：「該修就修，品質比較重要」。

## 重拍清單

種子 9311301／9311302，每鏡兩支，長度照 d1／fix1：s20 買 6 秒、s40 買 6 秒、s22 買 8 秒，6 支共 40 秒。
底稿是 fix1 選定那支的提示詞（`../fix1/review-picks.tsv`：三鏡都選 9311202）。做法跟 fix1 一樣：`retake.py` 從 `live/st1` 開始，先套 d1 與 fix1 的修改（原樣取自 `../fix1/spec.json`），再套下面 fix2 的修改。`mkjobs.py` 會把 fix2 的修改倒回去，確認得到的就是 fix1 的 `ref-sNN-9311202.txt`，逐位元相同。

| 鏡 | fix1 選定那支還剩的問題（2026-11-18 抽格看，scratchpad `e931f2/*.jpg`） | fix2 改什麼 |
|---|---|---|
| s20 | 許硯 1.5–3.0 秒、5.5–6.0 秒露齒笑，兩支都是，NOSMILE 句擋不住。唐小棠偏右，約在畫面六成五到七成的位置，5.5 秒後頭頂碰到右緣。緞帶綁成交叉結，兩條尾巴垂著。 | 見下方〈s20〉 |
| s40 | 二牛從頭到尾站著，把鋤頭橫在胸前（分鏡要他第一格就已經在衝）。許硯面向畫右，伸出去的卻是往畫左的手，跟二牛方向相反。 | 見下方〈s40〉 |
| s22 | 碗中央長出一株帶兩片綠葉的芽，越拍越高，5 秒後最明顯；s21 是貼在穀粒上的白芽尖，兩鏡接不上。唐小棠偏右，約在畫面六成的位置。 | 見下方〈s22〉 |

（s06 唐小棠偏右，但可以接受，這次不重拍。s30、s31 用 fix1 的那支。）

### s20：許硯不笑；唐小棠在正中

- **不寫任何笑字**，連本季的 NOSMILE 句也拿掉。第 1 集 fix6 那次能擋住笑，是因為同時改成中近景、拿掉其他動作。這鏡是雙人腰上景，又在說一句有盼頭的話，兩支都笑了。第 12 集 fix2、第 18 集 fix2、第 30 集 fix3 的經驗都是：改寫成具體、冷硬或專注的臉部動作，嘴的空檔用動作填滿。
- **改成側臉，眼睛看手上的碗**：`his face in right profile, turned toward screen right, his eyes lowered to the covered bowl in his hands`。他說的「三天前我把稻種包進濕布，今天該醒了」講的就是這碗，所以看碗是自然的。正臉看鏡頭方向，正是 fix1 笑出來的角度。
- **逐部位寫專注的臉**：`intent and serious, a farmer checking his seed`；眉頭微皺、壓低；眼睛定在碗上；嘴角平、往兩側拉平；下顎繃住；嘴只張到發每個字需要的程度，字與字之間抿回一條直線。說完最後一個字，`his lips close into one straight flat line, his jaw firm, his eyes still on the bowl to the last frame`。用這個動作補住片尾容易笑的空檔。
- 拿掉 d1／fix1 的 `quietly hopeful`、`eyes bright`（「亮」的眼睛會帶出笑）。說話句原本是 `turned toward the person he is speaking to … eyes on that person`，改成側臉看碗。
- **唐小棠在正中**：髮型句、`dead centre of the frame from the first frame to the last` 跟 s30 fix1 選定那支（9311201）一字不差（兩顆丸子、緞帶纏緊、尾端收進去、後頸露到粉色內領）。比對 s30 9311201 的畫面，它能在正中，是因為右三分之一站著二牛，左右平衡。s20／s22 只有許硯在左三分之一，模型就把她往右推來平衡。所以這次補上：
  - 右三分之一寫進場景圖本來就有的東西：一堆劈柴，加上亮著的院門口與門外龜裂的田（`so that she stands exactly between Xu Yan in the left third and the firewood and gateway in the right third`）。
  - 她的頭和肩膀占中間三分之一，左右露出的院子一樣寬。
  - 丸子頂上離畫面上緣留一個手掌寬。
  - 「兩大顆」丸子：`two big round buns`。
  - 緞帶寫成「平貼的一條窄粉帶、緊緊纏兩圈、兩端都塞進圈下」，對付這次的交叉結和兩條垂尾。
- **鏡頭改固定**（`The camera holds a static shot.`）：fix1 是慢推把她推到右緣。第 30 集 fix3 也是改成固定鏡頭。
- 動作照 fix1：許硯把蓋著布的碗往她那邊遞一點（一個動作）。台詞照劇本原句，用片中原聲。

### s40：二牛第一格就在衝；許硯的手伸向畫右

- **第一格**：`already in a full sprint toward screen right in the first frame: caught mid-stride with both feet off the path, his body pitched far forward, his front knee driving up and his rear foot kicked up behind him`。站在畫面中間，雙腳離地，身體前傾。
- **一鏡一個動作，就是衝**：`charges on toward the bank of sacks at the right in long, heavy strides, his feet pounding the path and kicking up dust`，到片尾衝到麻袋坡腳下（motion-quality 第二節：主動作要寫出力量與重量，也要寫停在哪裡）。喊一次台詞，喊完咬著牙、嘴閉上，照 fix1。
- **鋤頭**：部位句照 fix1 9311202 一字不差：`a long straight wooden handle with one flat, broad, square iron blade set at a right angle across its top end, the same hoe he carries on his shoulder`。持法照 1202 實際拍出來的樣子，也是 s39 扛的樣子：`gripped in both hands across his chest`，刃那一頭拖在他身後的畫左，刃朝下。fix1 原本寫的是 `raised above his head`，拍出來他站著擺姿勢、沒有舉，這次拿掉。道具在第一格的構圖句裡就寫到。
- **許硯**：站在左三分之一，身體與臉都朝畫右、朝二牛，`his right arm already stretched straight out toward screen right, his right hand reaching palm out toward Wang Erniu's back`，左手垂在身側。表情寫成驚急：眉毛往上、往中間擠，眼睛睜大盯著二牛的背，嘴閉著，等到他喊那一句。說話句改成 `his face in right profile toward Wang Erniu's back`。片尾 `stays planted where he is, his right arm still stretched toward screen right after Wang Erniu`。
- 拿掉兩處 `not smiling`。二牛的臉逐部位寫 `fierce`：咬緊下顎、眉頭擠著、眼睛盯著麻袋坡。
- **鏡頭改固定**：人往右緣衝的時候再慢推，會把他裁掉。
- 圖照 fix1：二牛定妝照、許硯定妝照、`set-shangyou-ba-fx-lu-l1`（翻轉過的壩，麻袋在右）。兩句台詞都用片中原聲。錄音 a42／a43 是退路。

### s22：碗裡照 s21 實際拍出來的樣子；唐小棠在正中

- 先看 s21 選定那支（d1 9311101），在 3.5 秒抽一格放大：紅陶碗裝滿金褐色帶殼稻種，表面平；表面散著約十根細白芽，每根大約一兩粒米長，平躺在穀粒上。
- 碗改寫成：`one red clay bowl filled level to just below its rim with plump golden-brown unhusked rice seeds … about ten short thin pure-white sprouts scattered evenly over the seeds, each sprout as long as one rice grain and as thin as a thread, lying flat on the seeds against its own grain, the surface of the seeds flat and level from rim to rim`。
- 動作句後面加上 `the golden seeds and their short white sprouts lie still and flat in the bowl, each sprout keeping its one-grain length from the first frame to the last`，對付「越拍越高」。
- 只寫碗裡有什麼，不寫否定名詞。`mkjobs.py` 會擋 leaf、seedling、shoot、stem、plant、green、grow 這幾類字。原本的 `no longer than the seed itself` 也拿掉。
- 唐小棠的正中、丸子、緞帶、右三分之一、頭頂留空、固定鏡頭，都跟 s20 一樣。
- 她交握的手從腰抬到胸前，只有前臂動，照 fix1。許硯閉著嘴、帶暖意，照 fix1（挑片時判定這鏡可以接受）。片中沒有人說話，錄音 a21 或 a21-p88 鋪在畫外。

## 檔案與指令

```bash
cd docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e931-live/fix2
L=/root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live
python3 -I mkspec.py                                   # spec.json; checks st1 + fix1 edits rebuild fix1's 9311202 prompts
python3 -I ../../_scripts/retake.py $L/st1 $L/fix2 spec.json
python3 -I mkjobs.py $L/fix2                           # colab-jobs.json + the scans
python3 -I ../../_scripts/preflight-prompts.py $L/fix2/colab-jobs.json
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest $L/fix2/colab-jobs.json   # from the repo root
bash /tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/e931f2.sh                    # SENDS (paid): only when the owner says so
```

`mkjobs.py` 的掃描（2026-11-18 全部 0）：

- 底稿＝fix1 選定那支，逐位元相同。
- 否定名詞。
- 任何笑字：smil、grin、laugh、beam，NOSMILE 與 `not smiling` 也算。
- 舊的失敗句已拿掉：NOSMILE、`not smiling`、`quietly hopeful`、`eyes bright,`、s22 的芽尖句、`raised above his head`、`stretched out after him`、`the hoe held high`、慢推。
- fix2 的新句子各出現一次，而且 d1、fix1 都沒有。
- s22 沒有葉、苗、莖、綠、長高這類字。
- s40 許硯的描述裡沒有 `screen left`。
- 每支都寫了人數（`exactly two people`）。
- 道具寫在第一格的構圖句裡。
- 動作句與台詞照原樣。
- 三鏡都是固定鏡頭。
- 武器、鎬、會長出字的詞（含 open）、掛起來的東西、辮子、尾巴、垂下來的詞。
- 不在畫面裡的人被點名。
- 圖、秒數、`<Picture N>` 與檔頭。

檢查結果：

- preflight：0 錯誤。2 個警告都是 s40「還我們水！」的 shout 規則，fix1 同樣有，片子沒有長出字幕。
- `h3r.sh check`：0 錯誤、0 警告。

## 挑片時要看的

- s20：放大許硯的嘴，每 0.5 秒看一次，尤其 1.5–3.0 秒與片尾。看唐小棠是不是在正中、頭頂有沒有碰到上緣或右緣、緞帶有沒有尾巴。側臉之後，嘴形對不對得上原聲。
- s40：第一格雙腳是不是離地；有沒有一路衝到坡腳；鋤頭是不是平刃、刃朝下（跟 s39 一樣），不能是鎬或斧；許硯的手是不是朝畫右；「二牛！」是不是許硯的嘴在喊。
- s22：碗裡是不是金黃稻種加貼著穀粒的短白芽，芽有沒有站起來、變綠、長高；唐小棠是不是在正中、沒露出頰邊。
- 兩個種子都不行時：照 `../fix1/review-picks.tsv` 留 fix1 那支（寫 KEEP，不寫 RETAKE）。
