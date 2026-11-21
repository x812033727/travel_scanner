# 第 19 集真人版 fix-polish：上架前精修重拍（2026-11-21）

照 `/root/mokaair-work/review-zt/RETAKE-BRIEF.md`。重拍清單是 `consolidated/retakes.json` 裡 e019 的 A、B 兩級，共 5 鏡，全部是 B：s21、s20、s01、s26、s31（s16、s29 是 C，不在這批）。
種子 9199101、9199102，960×544 Ref2VA，5 鏡 10 支，共 64 秒草稿。只寫了提示詞與 spec，沒有送出任何工作。

- 產出：`spec.json`、`prompts/sNN.txt`；`python3 -I ../../_scripts/polish-build.py 19` 寫出
  `~/mokaair-work/videos/zhong-tian-qu-qi-e919-dh/runpod/live/fixp/{prompts/,retake.json,colab-jobs.json}`。
- base 是現在剪進成片的那支（`_live-e919/.../picks.json`：5 鏡都是 `motion_from: d1`，提示詞 `d1/prompts/ref-sNN-SEED.txt`）。
  d1 的兩個種子提示詞逐位元相同（cmp 確認過）。
- **參考圖照 base 實際送的圖，但在 spec 裡寫死清單**：`d1/retake.json` 記的是換圖前的 `set-xianya-l1`，第 19 集的場景圖是 `e919-live/spec.json` 的 `swap_pictures` 換進
  `d1/colab-jobs.json` 的（側廳 `set-xianya-ceting-l1`、公堂 `set-xianya-gongtang-floor-l1`、門口 `set-xianya-steps-l2`）。`polish-build.py` 先讀 `retake.json`，
  `pictures: null` 會拿到錯的整張縣衙圖，所以 5 鏡都把 `d1/colab-jobs.json` 的清單抄進 `pictures`，沒有換、加、拿掉任何一張。
- 改法照 `e930-live/fix3/plan.md` 的寫法：只用正面描述、一鏡一個動作、說話面向對方、道具寫死樣子與大小；每鏡用腳本對 base 做「整句換整句」，舊句必須剛好出現一次。

## 公堂的方位（s20、s21 沒照審片改寫句的地方）

審片改寫句把高台放在「畫左上」。這場戲已拍好的鏡是另一邊：s18 唐小棠把帳頁舉向**畫右外**的高台（`script.md` 真人版改動）、s14 許硯臉朝畫右、s22 胡縣令看向畫左、現用 s21 許硯看畫右上。
所以 s20、s21 都寫「身體與臉四分之三朝畫右、下巴抬向畫右上外的高台」。s20 唐小棠仍在畫右（跟 s06、s07、s27 同一邊），許硯朝畫右時靠她那邊的是左手，攤手的是左手（審片改寫句也是左手）。

## 每鏡

| 鏡 | 級 | 審片問題（看畫格條） | base | 改了哪些句子（舊 → 新） | 圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- | --- |
| s21 | B | 「拍一下露出暗紅綢一角」沒拍到：右手平貼在平的衣襟上一直不放，什麼都沒露；許硯臉朝畫右上、方位對 | `d1/prompts/ref-s21-9191101.txt` | 胸口 `a small rounded bulge … where a pouch is tucked inside`（第 20 集米色外掛小袋的來源）→ `a palm-sized flat fold of dark red silk tucked inside the left breast … one corner of the dark red silk, two fingers wide, peeking out of the collar fold … from the first frame to the last`；動作「拍一下、綢角露出、手停在胸口」→ 說完前兩字指尖在綢角旁點兩下、手放出畫面、綢角留在畫面上，說完嘴抿成薄線；視線句改成 `three-quarter to screen right … the high dais off screen to the upper right` | 照 base | 綢角改成從第一格就露著（WRITING 第 218 行「改字只改一次，第二輪還錯就改設計」：把關鍵的東西寫成狀態，不靠拍一下才出現）；分鏡原意是拍了才露一下，這版是整鏡露一角。綢角可能長成整個紅袋掛在外面，或被畫成紅色內衣領 |
| s20 | B | 兩人正面看鏡頭；許硯右手攤向畫左前方（不是朝唐小棠）；胸口釘著米色小袋；唐小棠 119.4 起微笑看鏡頭 | `d1/prompts/ref-s20-9191101.txt` | 胸口小袋句 → `the front of his robe plain blue-grey cloth lying smooth and flat from the collar down to the sash`（中景不需要鼓包；跟剪接遮掉 s32 小袋後一致）；`face tipped up toward the high dais above the top of the frame`（正上方 → 對鏡頭）→ 身體與臉四分之三朝畫右上的高台；「右手攤向身旁的她」→ 第二秒左手（靠她那邊）腰高往畫右攤開、掌心朝上、停在離她袖子一前臂處；唐小棠站到他後方一步、`face three-quarter to screen left toward him … shy and stirred … flushing pink` → 側臉朝畫右的高台、眼睛垂看摺紙、冷臉逐部位（眉平、眼瞼垂、嘴抿成平線、臉頰不動、只有耳尖淡粉），說完下巴微低 | 照 base | 審片改寫句要她「四分之三臉、垂眼」；改成側臉，少露嘴角（她愛笑，REVIEW.md）。攤手仍可能被畫成牽手，所以寫停在一前臂外 |
| s01 | B | 錢員外的手整鏡搭著沒動、許硯沒抽手也沒轉身；背景是棚拍素灰牆（接不上 s02 有窗有椅的側廳） | `d1/prompts/ref-s01-9191102.txt` | 場景句 `a plain grey wall` 與 `behind them only the plain grey wall`（棚拍感的來源）→ 灰泥牆、右緣一扇深色格窗、窗光；胸口 pouch 句 → `the cloth over his left breast lying a little fuller and flat`；搭臂 `left arm rests along Xu Yan's right upper arm` → 前臂橫壓在他右上臂上；抽手「one sharp tug」→ 第一秒先低頭看那截金袖、右肩往畫左猛一抽、上臂從金綢下滑出、金袖直直垂出下緣不再回來、兩人肩間露出一道灰牆，再抬眼冷冷一字一字說（眉壓、咬牙），說完嘴抿成平線、轉頭轉肩向畫左；錢員外加「嘴角往下」 | 照 base | 抽手與說完轉肩仍是兩拍（轉肩是收勢，s02 要他背對錢員外）；若兩支都沒抽手，下一步是改設計：第一格就已經抽開、只拍他轉身。錢員外帽子照定妝照（高圓頂），第 18 集 s40 的交叉帶子不追 |
| s26 | B | 錢員外兩肘外張像叉腰坐著回嘴，沒有手抓他、沒往外移；右下一截膚色的手 | `d1/prompts/ref-s26-9191102.txt` | 景別 `medium close-up … framed from the chest up`（兩臂出畫 → 叉腰）→ `medium shot … standing on his feet, framed from the belly up`、身體側面、胸口朝畫左；兩隻從左右緣伸進來的黑袖手（都沒畫出來）→ 一隻從左緣伸進來抓他靠鏡頭那條上臂；他的兩臂貼身垂下、兩手收在金袖裡出畫面下緣；`drag him step by step` → 從第一格到最後一格踉蹌小步被拖往畫左、每拉一下肩膀一頓、柱子窗格從後面滑過；回頭、哼一聲、慢慢說照 base；「Besides him」句改成一隻手 | 照 base | 只剩一隻黑袖手，可能讀不出「被押」；手可能長成膚色或不見。8 秒照 base（台詞前有一聲哼） |
| s31 | B | 審片：阿令高馬尾、長髮垂背、橫插一簪，跟 s08 高髻、s32 前景盤髻不接 | `d1/prompts/ref-s31-9191102.txt` | 只改一句：構圖句 `her black hair in a high bun with one plain wooden hairpin`（跟外貌錨句與參考圖都不一致）→ `worn half up exactly as in the pictures: one small round knot on the crown with one plain wooden hairpin through it, the rest … falling straight and loose down behind her shoulders` | 照 base | **審片的要求跟系列定案相反**：`REVIEW.md` 阿令一列與 `lessons/zhong-tian-qu-qi.md`「她的頭髮是半披髮加髮簪，跟定妝照一樣，不是髮髻」；三張參考圖（定妝照、角度 a、b）都是頭頂小髻、其餘長髮垂到背，現片 s31 其實照定妝照。不接的是 s32 前景那顆全盤起的髻（s32 不在這批）。這支只是讓提示詞不自相矛盾，**建議站主不拍 s31**；若要整集看起來一致，該重拍的是 s32 前景背影（寫半披髮）。參考圖會壓過文字，照審片改寫句寫全盤髮也會畫成半披髮 |

## 檢查（2026-11-21）

- `polish-build.py 19`：5 鏡、10 支、64 秒，0 錯。
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error、0 warning。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error、0 warning。
- 自己掃新句子：沒有 smile／grin／laugh、sword／blade、pouch；`nothing` 只出現在 base 原有的「says nothing in this shot」。字數 559–864 字，在 1000 字內。

## 拍完要看

- s21：綢角是不是一小角（兩指寬）在交領縫裡，不是整個袋子掛在外面；手點完有沒有放下；臉朝畫右上。
- s20：許硯臉朝畫右上、不對鏡頭；攤的是左手、朝她、沒碰到她；胸口沒有外掛小袋；唐小棠嘴角。
- s01：第一秒有沒有抽手、金袖有沒有垂出畫面；背景有沒有窗（接 s02）；說完有沒有轉向畫左。
- s26：他是不是站著被拖著走、黑袖手在不在、有沒有膚色的手。
- s31（若拍）：頭髮跟定妝照一樣。

- s31 不拍（站主規則：阿令半披髮加髮簪，審片要的全盤髻跟規則相反）；s19 送出前已拿掉 prompts/s31.txt。
