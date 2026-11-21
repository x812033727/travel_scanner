# 第 5 集真人版 fix-polish：上架前精修重拍（2026-11-21）

照 `/root/mokaair-work/review-zt/RETAKE-BRIEF.md`。重拍清單：`consolidated/retakes.json` 裡 e005 的 A、B 兩級 8 鏡（s26 是 C，不在這批）。
種子 9059101、9059102，960×544 Ref2VA，8 鏡 16 支、共 96 秒草稿。只寫了提示詞與 spec，沒有送出任何工作。

- 產出：`spec.json`、`prompts/sNN.txt`；`python3 -I ../../_scripts/polish-build.py 5` 寫出
  `~/mokaair-work/videos/zhong-tian-qu-qi-e905-dh/runpod/live/fixp/{prompts/,retake.json,colab-jobs.json}`。
- base = 現在剪進成片那支（`_live-e905/.../picks.json` 的 `draft` 路徑：fix1／fix2／fix4／d1 的 `prompts/ref-sNN-SEED.txt`；picks.json 沒有 `motion_from` 欄，從 draft 的資料夾判斷）。
- 參考圖全部沿用 base（`pictures: null`）。小金算盤的道具圖 `prop-jinsuanpan-l1` 底是室內深色木櫃，放進晨光院子怕把背景拉成室內，沒加。
- 分鏡以 `zhong-tian-qu-qi-e005-r2/storyboard.md` 的 live prep 規則為準，審片改寫句有兩處沒照抄（見表內「拿不準」）：
  唐小棠不准笑的鏡仍從她背後拍、嘴不入鏡（s31、s33、s39）；s40 仍只放三個有名字的人（一鏡最多三人）。

| 鏡 | 級 | 審片問題（看畫格條） | base | 改了哪些句子（舊 → 新） | 圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- | --- |
| s08 | A（嚴重） | 開頭刀不在柱上、是秦霜橫握一把長刀抵在賴三胸前；拔出後變一公尺直劍、往下拖到腳邊再收到背後；賴三兩袖一格內變短袖 | `fix1/prompts/ref-s08-9051201.txt` | 柴刀 `a long narrow iron blade with a slightly hooked tip`（劍的來源）→ `a short, broad, single-edged iron chopping blade about as long as a forearm and as wide as a palm, thick straight back, squared-off tip, handle as long as a fist`；賴三右臂沿柱舉高、袖子在手肘下被刀從側面釘進柱子、只露刀柄與後半刀身、右手張開在刀上方一前臂遠；秦霜第一格手已握柄；動作改成拔出 → 袖子沿前臂裂一道口、手臂垂下但長袖仍蓋到手腕 → 刀在身前刃朝下插進右腰、刀柄立在右胯、右手停在柄上、兩手都在身前腰高；錨句與動作句各寫一次「兩袖長到手腕」；拿掉「許硯轉身」（他本來就朝她） | 照 base | 柴刀的說法跟全季其他鏡（`long narrow … hooked tip`）不一樣了，s02–s07 的現用片段刀也偏長；本集上下鏡會差一點。這句系列固定描述可能就是會變劍的原因，建議另開票掃全季 |
| s06 | A | 刀身橫在賴三頭上、賴三右手握著刀身、看不出釘在柱上 | `fix1/prompts/ref-s06-9051201.txt` | 同一把短寬柴刀、同一個釘法（手肘下、側面吃進柱子）；賴三站板凳、右手張開在刀上方；秦霜右手握柄、左手揪領；動作一個：揪領往下一拽、賴三半蹲、舉著的右手仍在刀上方、刀留在柱上到最後一格；兩袖長到手腕 | 照 base | 賴三半蹲後手臂被拉直，模型可能讓手滑到刀上；s08 寫的是靠柱站著，接點差一個姿勢（s07 低角度近景隔開） |
| s39 | B | 唐小棠沒抓袖子；算盤一開始已經在板上 | `d1/prompts/ref-s39-9051101.txt` | 她站近半步、右手先垂在身側、算盤夾在左腋；動作：右手抓住他左袖手肘上方抓到最後一格，身體一衝算盤從腋下掉到板上彈一下；許硯右手拿扁皂在胸前、左臂垂下 | 照 base | 審片改寫句要露她四分之三的臉；沒照做，仍從她右肩後拍（第 4 集、r2 第 5 集多次重抽仍笑，storyboard live prep 規則）。抓袖子可能被畫成牽手 |
| s40 | B | 許硯沒抬頭看日頭、對著鏡頭方向講，鏡尾嘴角有點上揚 | `fix4/prompts/ref-s40-9051502.txt` | 「先看日頭再轉向唐小棠」兩拍 → 一拍：第一格起臉朝畫左低日到最後一格、眼睛瞇著；冷臉逐部位寫（眉壓、瞇眼、鼻翼張、咬牙、字間嘴抿成線、嘴角往下、說完收成直線）；拿掉 `no blade, no knife and no weapon` 否定名詞句；修 base 的筆誤 `one a flat square` | 照 base | 審片改寫句要五人（加阿令、小禾）；沒照做，一鏡最多三個有名字的人。說話對著日頭不是對著人，`gaze` 檢查用 `eyes on the low rising sun` 過，但跟「說話面向對方」通則不同；這句是對自己下決心，稿子也寫看太陽 |
| s33 | B | 許硯坐著（s32 他是走過來站著）；皂是厚塊 | `d1/prompts/ref-s33-9051101.txt` | 許硯 `standing upright on his feet behind the long board, the board at the height of his hips`、動作句再寫一次站著；板上一排扁方皂、近端留一個空位；第一格她右手拿一塊懸在空位上方，放下用兩指對齊，才抬頭看他 | 照 base | 審片改寫句是反打拍她的臉；沒照做（同 s39） |
| s31 | B | 只拍到腰身、沒有頭，沒有聞皂；算盤吊在手上；皂是厚塊 | `fix2/prompts/ref-s31-9051301.txt` | 手部插鏡（no face, no head）→ 從她左肩後中近景、胸口以上、兩個髮髻在畫內、臉轉向畫右（許硯在畫外右）只露臉頰邊與睫毛；一個動作：右手從板上拿起扁皂湊到鼻下聞一口、頭微前傾；算盤夾在左腋下、指尖搭在算珠上不動 | 照 base | 稿子的「左手撥三顆算珠」沒寫成動作（一鏡一個動作，上次兩個都沒做到），由音效 abacus 帶；從左肩後拍與 s32、s33 的右肩後不同邊，但沒越軸（她仍在許硯左邊、看畫右） |
| s38 | B | 背景是井與花田、沒有木板與皂；從箱子拿出長條皂 | `d1/prompts/ref-s38-9051102.txt` | 站在木板後、臀部以上、頭上留大空間；板上兩排扁皂、一塊分開放在最近處；背景改「柿子樹幹與竹籬」；動作：慢慢彎腰撿起那塊分開的、慢慢直起身、平拿在胸前 | 照 base | 場景圖 `set-xujia-yuan-l2` 這一側是石牆與井，竹籬是文字補的，可能還是拍到井 |
| s29 | B | 皂黏在模子格子裡一路往下掉、提起後板邊多一堆皂 | `d1/prompts/ref-s29-9051101.txt` | 「倒扣的模子、皂滑出來」→ 無底的淺格框（四邊厚、裡面三排十格細隔板、皂在格裡直接放在板上）；兩手往上一提、空格框一路提出畫面上緣、每格透光；三十塊扁方皂原地留在板上、間隔一指；其餘板面空著到邊 | 照 base | 格框跟稿子「倒扣的長木模」做法不同（s27 抬的是外觀一樣的長框，看不出差別）；模型可能仍讓幾塊黏著往上帶 |

## 檢查（2026-11-21）

- `polish-build.py 5`：8 鏡、16 支、96 秒，0 錯。
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error、0 warning。第一次有 s31 `unpictured Xu Yan` 兩條（寫成「where Xu Yan stands out of the frame」被當成在畫面裡），改成 `toward Xu Yan off screen right` 後消掉。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error、0 warning。
- 自己掃：新句子沒有笑字、沒有 sword／hooked／long narrow、沒有新增的否定名詞（剩下的 `no smile at any moment`、`no marks or writing`、`no second copy` 是 base 原有的固定句）。

## 拍完要看

- s08：0–1 秒刀在不在柱上、刀長（不超過前臂）、拔出後是否插右腰（不往背後）、賴三右袖全程長到手腕。
- s06：賴三右手有沒有碰到刀；鏡尾狀態接 s08 第一格。
- s39、s33、s31：唐小棠嘴角（雖然嘴不入鏡，臉頰邊鼓起也算）；s39 抓的是袖子不是手。
- s40：許硯整鏡朝日頭、鏡尾嘴角。s29：提框時有沒有皂掉落或黏著。
