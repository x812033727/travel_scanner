# 第 10 集真人版 fix-polish：上架前精修重拍（2026-11-21）

審片來源：`/root/mokaair-work/review-zt/consolidated/retakes.json`（e010，tier A/B 共 5 鏡，全是 B）與 `reports/e010.md`。
種子 9109101／9109102，960×544 Ref2VA，每鏡 8 秒（照 base），5 鏡 10 支、共 80 秒。只寫提示詞與 spec，沒有送出。
base 一律是 `picks.json` 現在用的那支的提示詞（兩個種子的 d1 提示詞逐字相同）。

| 鏡 | 審片問題 | base | 改了哪些句子（舊→新） | 換圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- |
| s13 | 許硯笑著說全場最重的一句（24.9–31.6 秒嘴角上揚） | `d1/prompts/ref-s13-9101102.txt` | 表情「brows level… no smile」→ 冷臉逐部位：眉低微皺、眼不眨、臉頰不動、嘴角平、句與句之間抿平；包袱結寫死在構圖裡（灰藍粗布、拳頭大、肩高、畫右緣）；動作「伸手放在結上」+「no smile…」→ 開口時右手按住結、一直按到最後一格，說完嘴收成一直線，嚴肅臉維持到最後 | 照 base（angle-a、angle-b、set-xujia-yuan-l2） | 定妝照本身不笑，d1 的笑是模型自己加的；若兩支仍笑，下一步考慮只送 angle-a |
| s29 | 八個村民像複製人、二牛站著沒蹲 | `d1/prompts/ref-s29-9101102.txt` | 「二牛和八人蹲成一排」→ 貼近二牛的中景：二牛蹲在左前景、頭剛過籬笆頂、兩手握棍；八人在後方較小虛焦、高矮遠近不齊，逐一寫四個不同長相（灰鬍瘦、圓胖、瘦高少年、粗壯塌鼻），其餘被肩與籬笆柱擋住，衣色與包頭各不同；「no blade, no knife, no sword and no spear」→「手上只有木棍」；動作「蹲下再一根根舉棍」→ 棍子一根根豎過籬笆頂、二牛全程蹲著點一下頭 | 照 base | 八個沒參考圖的人仍可能長得像二牛；靠虛焦與遮擋降低可見度。稿子寫「蹲下」的動作改成一開始就蹲好（一鏡一個動作） |
| s30 | 唐小棠 7.7 秒都是後腦勺 | `fix1/prompts/ref-s30-9101201.txt` | 整段構圖改寫：背後拍 → 她胸上近景在畫左、臉四分之三朝畫左（許硯在畫外左）、燈籠光、算盤框在下緣、擔心發白（眉心上提、眼睜大泛淚、嘴抿小）；秦霜（不點名）在畫右後方虛焦蹲在棍子旁；動作改成她原聲低聲說「半刻鐘就排好了……她到底是什麼人？」，說完抿嘴聽畫外男聲 | 加 `tangxiaotang-portrait-l1`、`tangxiaotang-angle-a-l1`，留 `set-xujia-yuan-ye-l1`（3 張） | **聲音**：分鏡原本刻意讓她整集都錄音（s23 仍是背後拍＋錄音），本鏡改原聲後同集兩種聲音，請站主聽 s23 對 s30；許硯畫外那句仍放錄音 |
| s33 | 錢員外戴黑帽像縣令、馬上多坐一人 | `d1/prompts/ref-s33-9101102.txt` | 外貌錨句「a small black cap」→ 光頭、頭髮梳成小髻插一支金簪；構圖加「光頭、金簪映火光、獨自下馬」；家丁「接韁繩」→ 步行站在馬頭前的路上兩手牽韁、他下馬後鞍上空著；轎簾「no writing and no emblem」→ plain unmarked；動作拿掉「整袍子」，只剩落地、小跑到轎旁、彎腰對簾說話 | 拿掉 `qianyuanwai-angle-b-l1`（側面、帽子最大），留 portrait、angle-a、set-xujia-menwai-l1 | **三張定妝照都戴黑帽**，文字可能壓不過圖；兩支都還戴帽的話，接受帽子（跟定妝照一致）、只取「馬上沒人」的修正，或另做一張去帽的定妝照（不在本次範圍） |
| s36 | 三人排排站對鏡頭、院門自己打開 | `d1/prompts/ref-s36-9101102.txt` | 鏡位「從路上透過院門往裡看」→ 從路上斜拍、左前景門柱，兩扇門第一格就已推開貼牆；許硯身體與臉四分之三朝畫右的官差、左手一開始就搭在唐小棠肩上；表情「brows level, eyes hard… no smile」→ 眉低皺、眼瞇、咬牙；唐小棠移到他左肩後、身體朝畫右；「no blade, no knife and no sword」→ 手上只有秦霜的木棍與唐小棠的算盤；動作三段（按肩、拉門、跨出張臂）→ 一個：放手、跨一步進門口、張開雙臂，說完嘴抿成一線 | 照 base（許硯三張、秦霜、唐小棠三張、set-xujia-menwai-l1） | 稿子的「按肩讓她退到身後、再拉開院門」改成開場狀態（手已搭肩、門已開），拉門的動作沒了；院門音效（c36 院門拉開）剪接時可拿掉或放在上一鏡尾 |

## 檢查（2026-11-21）

- `python3 -I _scripts/polish-build.py 10`：5 鏡、10 支、80 秒，0 錯誤
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)

輸出在 `~/mokaair-work/videos/zhong-tian-qu-qi-e910-dh/runpod/live/fixp/`（`colab-jobs.json`、`retake.json`、`prompts/ref-sNN-910910{1,2}.txt`）。
