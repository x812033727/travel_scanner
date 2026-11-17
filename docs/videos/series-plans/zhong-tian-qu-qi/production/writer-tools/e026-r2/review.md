# 第 26 集重製版 r2（e926）真人版：開拍前獨立審稿

- 審稿日期 2026-11-17。審稿者沒參與寫稿，也沒用 Colab、RunPod 或任何付費服務；只寫了這一份檔，沒改別的檔，沒 git commit。看圖用的小 jpg、試做的調色圖、變調試聽檔都放在 scratchpad，用完已刪。
- 審的對象：`docs/videos/zhong-tian-qu-qi-e026-r2/{script.md,storyboard.md,video.json,overlays.json}`、`writer-tools/e026-r2/r2.py`、`colab/runs/e926/extras.json`、`colab/runs/e926-live/{mkspec.py,spec.json}`、`hailuo/clips-dh-e926.json`（精修文字），以及實際要送的 `~/mokaair-work/videos/zhong-tian-qu-qi-e926-dh/runpod/live/d1/colab-jobs.json`（82 支＝41 鏡 × 2 種子）與 `prompts/`；錄音 `audio/`（`README-retakes.txt`、`fw926.txt`、`fw926-retake.txt`、36 個 wav、`take1/`、`take2/`）。
- 對照了這些：`r2-bible-e021-e030.md`（拍法 1–30、接點 25→26 與 26→27、帳、道具表、小角色、場景盤點）、`season-01.md` 第 26 集、`writer-tools/e025-r2/review.md`、`colab/runs/e924-live/picks-merged.tsv`（與 e921–e923 的挑片）、任務檔 `2026-11-07-zhong-tian-live-action-remake.md` 第 13–23 集的教訓。
- 參考圖都放大看過：`set-tangfang-l1`、`set-tangfang-jia-l1`、新裁的 `set-tangfang-lu-l1`、`set-xuji-pu-l1`、`set-xuji-pu-cabinet-l1`、`set-xuji-pu-houjian-l1`（另試了免費提亮）、`set-xuji-pu-eve-l1`、`set-xuji-pu-ye-l1`（試了櫃檯油燈的裁切，不建議）、`set-xianjie-l1`（石板路放大）、`set-xianjie-{weiji,xuji,shi}-l1`、`xiaohe-portrait-l1` 與 `angles/xiaohe-angle-{a,b}-l1`、`laisan-portrait-l1`、`laisan-sleeve-l1`、`weishaoqing-portrait-l1`。
- 錄音：36 句用 silencedetect（−35 dB）重量長度；a01、a07、a12、a19、a22、a23、a25、a26（重錄與 take1）用 YIN 重算音高；a26 試做降 3 個半音（ffmpeg `rubberband`），faster-whisper medium 聽寫一支（numpy 陣列、兩條執行緒、無提示與帶上下文各一次，跑完就結束）。

## 先確認的事

| 項目 | 結果 |
| --- | --- |
| 分隔句 | 82 支 d1 提示詞，每支 `never the mood. ` 與 `One continuous shot.` 都剛好一次；`prompt_sha256` 都跟檔案相符；兩個種子的提示詞與參考圖逐位元相同。clips-dh 41 鏡每鏡 `the set layout stays as it is. ` 剛好一次；沒有 `Tang Xiaotang`、`stand-up collar`、`abacus`、`lantern` |
| 參考圖路徑 | 全部是絕對路徑、檔案都在；每鏡送的場景圖跟 `mkspec.py` 的 SWAP 一致（s01 是 `set-tangfang-jia-l1`；`retake.json` 裡的 `set-tangfang-l1` 是換圖前的版本，不影響） |
| 帳本 | s18、s21 都寫 `one thick stack of plain blank paper sheets stitched along one edge with cord`；沒有 book、ledger、brush、ink、pen。**但 `open` 有出現**：七支插鏡（s06、s18、s22、s31、s33、s36、s39）的固定句 `the shot opens directly on`，見必改 1 |
| 扇子 | s26、s29 `one closed folding fan held upright ... like a short slim stick, its dark bamboo ribs pressed tight together`，s28 插在腰帶；沒有打開的字 |
| 魏記夥計 | s25–s28 一律 `one thin young man of about twenty in a dark red cloth short jacket and a black cloth head wrap`、side-on 或 profile；沒有 shop boy、沒有 gong；不送圖 |
| 唐小棠 | 五支說話背影（s01、s07、s12、s21、s24）拿掉她的三張圖與身分句；s23 不點名不送圖；s18、s22 只有手（`thick opaque peach-pink silk sleeve cuff`）；其他鏡沒有她 |
| 人數句 | s02、s12、s14、s17、s19、s21、s23 兩人；s25 七人；s35、s40 八人；s37、s38 三人；跟構圖一致。沒有 e925 s28 那種「exactly two」配「only person」的矛盾 |
| 說與不說 | 背影或畫外說話的鏡（s01、s07、s08、s12、s13、s15、s20、s21、s24、s25、s30、s40），每張朝鏡頭的臉都寫 `says nothing ... lips pressed together ... no mouthing words` 或 `their lips closed` |
| 秒數 | 照 r2.py 的算法（(買的秒數 − 0.3) × 1.1）全部裝得下。最緊：s05（a05 人聲 5.96／6.27）、s18（a19 約 5.73／6.27）、s29（a29 5.23）、s19（a20 5.08）、s37（a35 5.04）。s15、s40 買 8 秒合理 |
| 面板 | `overlays.json` 只有 s20 兩塊 task，跟系統句、聖經〈系統〉第 26 集一字不差 |
| 軸線 | 糖坊：灶與許硯在左、欄杆與路在右；許硯一律看畫右，賴三在欄杆外看畫左，s10／s11 過肩互為反打、沒越軸。鋪子：她在右前景背對、許硯隔櫃檯朝畫右（照第 24 集 fix1 的方向）。大街：許記在左、魏記在右，魏少卿一律朝畫左看許記 |
| 時間與光 | 糖坊清晨、斜陽從右（圖上太陽在右上，對）；鋪子早上、光從門口（對）；後間黃昏、油燈（對）；大街見建議 3 |

## 寫稿者沒把握的地方：逐一判斷

| 寫稿者問的 | 判斷 | 改法在哪 |
| --- | --- | --- |
| s01 只拍她、許硯不在畫面，接點寫「許硯在她左邊」 | **可以照拍**。25→26 是隔了一夜、換了地點，不是同一刻接戲；聖經接點只要求「把字條收進錢箱、轉身指揮」。s01 提示詞寫了 `the white steam rising from the iron pan on the left`，灶（許硯的位置）就在畫左外，s02 全景許硯在左前灶邊，「他在她左邊」由 s02 交代 | 不用改 |
| s05 錄音 5.96 秒放 6 秒片 | **放得下，但不留尾巴**。第 24 集 s05 一模一樣（a04 5.96 秒、6 秒片、人聲從第一格起）挑片照用了。要防的是提示詞結尾的 `after the last word he holds it there`：模型會把話說短、留一段不動，嘴就比錄音早停 | 建議 8 |
| a26 唐小棠比同場高約 6 個半音 | **重算確認**：a26 中位 351 Hz，同場 a19 251、a22 239、a23 253、a25 260（中位約 252），高 5.7 個半音；take1 366 Hz 更高。畫外高興地喊可以高，但 5.7 個半音聽起來像換了一個人。**免費修法試過**：`rubberband=pitch=0.8409:formant=preserved`（降 3 個半音）後 YIN 中位 304 Hz、長度不變；聽寫無提示「二牛,你看,隊伍排到結尾了!」、帶上下文「二牛你看，隊伍排到街尾了！」，跟原檔一樣（街尾／結尾同音） | 建議 9 |
| a36「糖裡有毒」聽成「藏裡」、a21 系統句 | a36：**要耳朵聽，必要時再錄一次**。cáng／táng 差在聲母，尖叫最容易把送氣的 t 喊糊；它是全集的鉤子，字幕雖然寫對，觀眾聽到「藏」會出戲。a21：**接受**，系統聲變速濾波過，無提示 r0.59 跟第 25 集系統句一樣；要緊的兩句（白糖量產，達成；許記是魏記兩倍）都有面板逐字疊上 | 建議 10 |
| s20 近景木箱在下緣、手插糖裡 | **要改**。胸以上的近景，「箱子在下緣」沒說放在哪裡：箱子放地上，手就要伸到畫外；模型多半會把箱子畫成浮在胸前，或讓他彎腰出畫。要寫明箱子立在櫃檯上、開口在胸下 | 必改 6 |
| s25 高角度搖鏡、七個小人 | **搖鏡其實沒送出去**：s25 的提示詞與 clips-dh 都沒有運鏡句（產生器丟掉了 pan），片子會是定鏡，這反而好；七個小人定鏡比搖鏡穩。要改的是兩件：(1) `high-angle` 跟送的 `set-xianjie-l1`（人眼高、略仰、天空占四成）打架，第 24 集 s02 寫俯拍、挑片接受的是「平視不是俯拍」；(2) 隊伍從許記門口往街裡排，六個客人會朝鏡頭方向站，臉都對著我們（客人不給臉） | 必改 2 |
| 後間圖幾乎全暗、桌與竹匾全靠文字 | **文字可以照用，圖建議免費提亮**。`set-xuji-pu-houjian-l1` 平均亮度 16／255（中位 10），只有一面空格架；第 23 集的教訓是「只送單色或全暗的圖會自己長出室內」——這裡提示詞把房間寫完整了（後牆空架、中間長桌、三只竹匾、桌角竹籃、油燈、左門洞、右後門門閂），長出來的就是我們寫的，s30、s30b、s34 用的是同一句，s31–s33 是同一句的短版，接戲沒問題。真正的風險是整支片偏黑、臉糊。`eq=gamma=1.9:contrast=1.15:saturation=1.1` 試過：空格架與牆面讀得出來、仍是暖橘夜色。`set-xuji-pu-ye-l1` 右邊櫃檯兩盞油燈的裁切也試過：燈像燈泡、是前堂的櫃檯，不建議 | 建議 1 |
| s38「慢慢倒地」6 秒 | **6 秒夠，但動作太多**：彎腰、踉蹌、側身倒、蜷著、糖糕與紙掉出手，一鏡五件事；倒地翻身時臉最容易轉向鏡頭。第一格就讓他彎著腰、糖糕與黃紙已經掉在腳邊，整支只做「慢慢側倒、背對我們、蜷著不動」一件事 | 必改 5 |
| s16 二牛兩指點自己眼睛 | **要改**。第 16 集教訓「單根手指的手勢會被讀成比中指」；兩指湊到眼下，第一格手還擋著臉（`his right hand already raised to his face`），又是一鏡兩個動作（點眼睛、說完放手抱胸）。「這雙眼睛」由台詞說，畫面用瞇眼、下巴一指就夠 | 必改 4 |
| s04 許小禾只送定妝照 | **免費就能補**：`angles/xiaohe-angle-a-l1` 已經有，正是臉朝畫左 3/4、同一件補丁淡紫短襖、紅繩小辮，跟 s04「仰頭朝畫左」同方向（照 e925 審稿補秦霜 angle-a 的做法）。s17 她是背景小人，送定妝照就夠 | 必改 8 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 26 | s18（同句也在 s06、s22、s31、s33、s36、s39） | 插鏡的固定句 `the shot opens directly on` 帶著 `open`。s18 接的是 `one thick stack of plain blank paper sheets stitched along one edge with cord`，「opens ... stitched sheets」最容易被讀成一本攤開的書（攤開就有字）；s22 接的是要包的白紙 | 任務要求「不出現 open」；拍法 7、27（紙只見空白、不攤開）；第 21 集挑片「平攤的白婚書」 | spec 對七鏡加 `replace`：`the shot opens directly on` → `the very first frame is already a close view of`。clips-dh 沒有這一句，不用動 |
| 26 | s25 | (1) `high-angle wide shot from under the eaves of the Xu shop` 跟送的街景圖（人眼高、略仰）打架；(2) 隊伍 `standing one behind another` 沿許記門前往街裡排，排頭在近處的門口，六張臉都朝鏡頭；(3) 同一句重複 `a long low dark table before it, the long low dark table before it`；(4) 分鏡表寫搖鏡、提示詞沒有運鏡句，兩邊不一致 | 拍法 25（客人不給臉）、29（場景圖說了算）；第 24 集 s02「平視不是俯拍」；第 24 集 s12 女客抬頭看鏡頭落選 | 構圖改成 `wide shot down the street at standing eye height, like the picture: along the paving before the Xu shop on the left, a line of six customers in plain Song-dynasty cotton robes and cloth head wraps, small, each one turned toward the Xu shop's doorway on the left, seen side-on and from behind, their faces hidden by their cloth head wraps;`；`a long low dark table before it, the long low dark table before it piled with` 改 `a long low dark table before it piled with`；動作段後面補 `The camera stays still.`（或照其他鏡 `The camera pushes in with small amplitude at slow speed.`）。分鏡表與 `video.json` 的 camera 改成 `Wide shot, static`；要「左到右」的感覺由剪接在成片上做數位慢搖（裁切移動，免費） |
| 26 | s40 | 鏡位寫 `high-angle wide shot from just inside the Xu shop's doorway, its dark door frame soft at the left edge`，但送的 `set-xianjie-l1` 是站在街上看、許記門面在左；同一張提示詞前面又寫 `on the left the front of the Xu shop`——人在許記門裡就看不到許記門面。許硯「在左邊門口、全身」也跟「鏡頭在門裡」矛盾（他會變成前景大半身）。六個客人「往四面退開」，圍成一圈就有一半臉朝鏡頭 | 拍法 25、29；接點 26→27（許硯在門口；第 27 集照 `set-xianjie-xuji-l1` 的方向接）；第 24 集 s02 | `high-angle wide shot from just inside the Xu shop's doorway, its dark door frame soft at the left edge:` 換成 `wide shot down the street at standing eye height, like the picture:`；客人那句換成 `around him six customers in plain Song-dynasty cotton robes and cloth head wraps backing away toward both sides of the street, small, side-on and from behind, their faces turned down toward the man on the ground, a widening ring of bare paving around him;`。分鏡表 s40 的「前景虛焦許記的門框、高角度」一併拿掉 |
| 26 | s16（clips-dh 同鏡） | 兩指點自己眼下：手勢易被讀錯、手擋臉；第一格 `his right hand already raised to his face`；說完又 `lowers the hand and folds his arms`，一鏡兩個動作 | 第 16 集「單根手指的手勢會被讀成比中指」；一鏡一個動作；第 15 集「手與道具位置寫在第一格」 | 構圖的 `his right hand already raised to his face,` 換成 `his thick arms already folded across his chest from the first frame,`；動作段 `Wang Erniu taps two fingers just under his own eyes twice as he speaks; after the last word he lowers the hand and folds his arms` 換成 `Wang Erniu narrows his eyes at the path and jerks his chin toward it once as he speaks; after the last word he keeps glaring at the path, his arms still folded`。clips-dh 的 a926-s16 同樣替換 |
| 26 | s38（clips-dh 同鏡） | 彎腰、踉蹌、側倒、蜷著、糖糕與紙掉出手，一鏡五件事；側倒時臉會轉向鏡頭；糖糕在空中掉落是另一件難畫的事 | 一鏡一個動作；拍法 25（灰衣客人背影與側背）；第 18 集「求情正面臉」的教訓 | 構圖的 `both hands already pressed to his stomach from the first frame, the bitten cake and its scrap of rough blank yellowish paper in one hand;` 換成 `already doubled over from the first frame, both hands pressed to his stomach, his knees bent, the bitten cake and its crumpled scrap of rough blank yellowish paper already lying on the paving at his feet;`；動作段換成 `the man in grey slowly sinks down onto his side on the paving, his back toward us and his face toward the shop, and lies curled up and still for the rest of the shot; the two customers step back;` |
| 26 | s20 | 木箱只寫 `before him at the lower edge of the frame`，沒說放在什麼上面；胸以上的近景，箱子要立在櫃檯上，手才在畫裡 | 寫稿者問題；任務檔第 13、15 集「手與道具位置寫在第一格構圖」 | `one plain wooden crate before him at the lower edge of the frame, its lid already lifted off and leaning against it from the first frame, heaped with fine white sugar like fresh snow, his right hand already buried in the sugar;` 換成 `one plain wooden crate standing on the counter top right in front of his chest, its open top at the lower edge of the frame, its lid already lifted off and leaning against its side from the first frame, heaped with fine white sugar like fresh snow, his right hand already buried to the wrist in the sugar;`；`his face three-quarter to screen right, eyes on the sugar` 改 `his face three-quarter to screen right, his eyes lowered to the sugar` |
| 26 | s28 | `low-angle medium shot ... framed from the knees up so the whole table stays in the frame`：桌子是 `long low dark table`（膝高），從膝蓋以上取景，桌子正好在畫框下緣外，掀桌的整個動作出畫 | 分鏡表「整個動作留在畫面裡」；一鏡一個動作要看得見 | `low-angle medium shot of Wei Shaoqing` 改 `low wide shot of Wei Shaoqing, the camera at knee height`；`framed from the knees up so the whole table stays in the frame` 改 `framed full figure, the whole long low table across the lower part of the frame in front of him` |
| 26 | s04 | 許小禾只送定妝照，本集她唯一的中景、會說話；`angles/xiaohe-angle-a-l1` 已有，方向正好（臉朝畫左 3/4） | 寫稿者問題；拍法 19；e925 審稿必改 6 的做法 | spec 的 s04 加 `"add_pictures": ["angles/xiaohe-angle-a-l1.png"]`（絕對路徑，排在 portrait 後、場景圖前），`replace`：`little Xiaohe shown in <Picture 1> keeps` → `little Xiaohe shown in <Picture 1> and <Picture 2> (the same girl from several angles) keeps`、`the location shown in <Picture 2>` → `the location shown in <Picture 3>`、開頭 `<Picture 1> and <Picture 2> are referenced throughout` → `<Picture 1>, <Picture 2> and <Picture 3> are referenced throughout` |
| 26 | s36、s37、s38、s40 | 灰衣客人寫成 `a plain grey cotton cross-collared short jacket`，聖經〈小角色〉是「灰布長衫」；第 27 集第一鏡就是同一刻（接點 26→27），下一集照聖經寫長衫就跳衣服 | 聖經〈小角色〉灰衣客人；接點 26→27 | s37、s38、s40 的 `one man in a plain grey cotton cross-collared short jacket` 換成 `one man in a long plain grey cotton robe`；s36 的 `a plain grey cotton sleeve cuff` 換成 `a long plain grey cotton sleeve`（後面的 `grey-sleeved` 不動）。若寫稿者認為短衣較好，就改聖經同一行，二選一，不要兩邊不同 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 26 | s30–s34（後間圖，免費調色） | `set-xuji-pu-houjian-l1` 平均亮度 16／255，片子會整支偏黑、賴三的臉糊；文字已把房間寫完整，圖只需要讀得出「暖的油燈夜、深色空木架」 | 第 23 集「全暗或單色的圖」；拍法 8、19 | 做一張免費提亮圖，**新 id、自帶 l1**：`ffmpeg -i set-xuji-pu-houjian-l1.png -vf "eq=gamma=1.9:contrast=1.15:saturation=1.1" set-xuji-houjian-deng-l1.png`（試過：空格架與牆面讀得出、仍是暖橘夜色、沒有字），`refs-live/README.md` 補一行，spec 的 s30–s34 SWAP 改指它。不要用 `set-xuji-pu-ye-l1` 的櫃檯油燈裁切（燈像燈泡、是前堂櫃檯） |
| 26 | s30 | `one grey rag already under his right hand ... Lai San's hand with the rag stops still`：第一格手已經不動，「停住」沒有可看的變化 | 一鏡一個動作要看得見 | 構圖改 `his right hand already wiping the table top with one grey rag from the first frame`；動作段改 `Lai San's hand with the rag slows and stops still on the table top, and he listens toward the doorway` |
| 26 | s25、s35–s40（大街的光） | 都寫 `low morning sun from the right`；`set-xianjie-l1` 石板路放大看：左半（許記那側）在陰影裡、右半與魏記門面整片陽光，光是從左邊屋頂後面來的；s26–s29 寫的是 `bright morning sunlight`（不寫方向） | 光源與參考圖一致；拍法 29 | 大街各鏡的 `low morning sun from the right, long shadows on the paving` 與 `in low morning sunlight` 一律改成 `in clear morning sunlight, the shop fronts across the street in full sun, the paving before the Xu shop in soft shade`（或至少拿掉 `from the right`） |
| 26 | s20、s21、s23 | 同一個位置（許硯隔櫃檯、面朝櫃檯），s20 寫 `behind him the dark shelves`，s21、s23 寫 `behind him the bright doorway`。照圖：櫃檯在右牆、鏡頭在她背後往左看，他身後應是左牆的空架，門在後牆 | 接戲；拍法 29 | 三鏡統一寫 `behind him the dark shelves along the far wall, the bright doorway at the edge of the frame, soft` |
| 26 | s19 | 推車上 `six plain wooden crates`，賴三懷裡再 `one plain wooden crate`，畫面上七箱，台詞「又出了六箱」 | 數字照台詞 | 推車改 `stacked with five plain wooden crates`，賴三抱的那一箱是第六箱 |
| 26 | s35、s40 | s35 隊伍六人（s37 灰衣客人就站在隊伍裡），s40 寫灰衣客人加「六個客人」，客人變七個 | 拍法 25（寫實際人數）；接戲 | s40 改 `around him five customers ...`，人數句 `exactly eight people` 改 `exactly seven people`、`the six customers backing away` 改 `the five customers backing away`；s35 客人那句補 `side-on and small, their faces turned toward him under their cloth head wraps` |
| 26 | s27 | 夥計在畫面上說話（側面中景、嘴照錄音動），提示詞卻沒有台詞，只寫 `lips moving between mumbled words`；側面中景看得到嘴，嘴形會跟錄音對不上。另外「攤掌」加「縮半步」兩個動作。分鏡表台詞標「魏記夥計（畫外）」也不對 | 拍法 14；一鏡一個動作 | 動作段改 `the young man in dark red speaks a short Mandarin line, 「少爺，全去對面買糖霜糕了」, his voice dropping, his face in profile to screen left, his lips moving with every syllable; he turns one flat palm toward the far side of the street as he speaks`，拿掉 `and shrinks back half a step`；分鏡表把「（畫外）」拿掉 |
| 26 | s10 | 送的 `set-tangfang-jia-l1` 是從棚裡往棚尾看、欄杆在右緣；這一鏡鏡頭在欄杆外往棚裡看，`across the wooden railing` 沒說欄杆在畫面哪裡，模型可能把賴三放進棚裡 | 拍法 29 | 構圖補 `the top rail of the wooden railing running across the lower foreground between them`；`behind him the stone basin and the steam, soft` 改 `behind him the plaster wall with the brown clay funnels on their rack and the steam over the iron pan, soft` |
| 26 | s05 | 人聲 5.96 秒剛好裝滿；結尾 `after the last word he holds it there` 會讓模型把話說短、留一段靜止 | 第 24 集 s05 同長度照用（人聲從第一格起） | 拿掉 `after the last word he holds it there,`，改成 `he keeps talking softly to her to the end of the shot,`；剪接時從第 0 格鋪上 |
| 26 | a26（s25 畫外） | 比同場高 5.7 個半音（見上） | 第 17 集變調要人耳聽；第 23 集 a29 偏高交站主 | 免費：`ffmpeg -i zq926a26.wav -af "rubberband=pitch=0.8409:formant=preserved" zq926a26-m3.wav`（降 3 個半音，約 304 Hz，聽寫兩遍都對），剪接時兩版用耳朵比，留不像換了人的那一版 |
| 26 | a36（s40 畫外） | 重錄後無提示仍聽成「藏裡有毒」 | 第 14 集「重錄要聽寫確認」；第 21 集「帶上下文的聽寫證明不了念對」 | 剪接前用耳朵聽第一個字；若聽得出 cáng，用 `lines.mjs` 重錄一次，只在給 TTS 的暫存稿把「糖」寫成「táng」（照 a01 的做法，字幕不動），聽寫照舊兩遍 |
| 26 | s33 | 第 27 集阿令要「看見賴三指甲縫的粉」，聖經〈人物〉賴三寫「第 26 集指甲縫的白粉只在插鏡」；本集唯一的插鏡沒埋 | 伏筆（第 27 集）；拍法 12 的寫法例外 | 構圖補 `a faint trace of the greyish white powder along the edges of his fingernails`（只寫在指甲縫邊緣，不寫皮膚上的點） |
| 26 | s31、s33、s36 | 賴三的手插鏡不要加送 `laisan-sleeve-l1`：放大看它是胸口交領的裁切、不是袖口，送了會長出胸口 | 拍法 19（參考圖壓過文字） | 維持現狀（文字 `checked grey-brown sleeve cuff`），在 `refs-live/README.md` 該圖那一行補「是胸口交領，不當手插鏡用」 |
| 26 | s38 | 兩邊的客人 `side-on`：中景裡側臉夠大 | 拍法 25 | 改 `on either side of him two customers in plain Song-dynasty cotton robes and cloth head wraps, half turned away from us, soft` |
| 26 | 分鏡表 | 表上 s25 寫「搖鏡（左到右）」、s40 寫「前景虛焦許記的門框」，跟必改 2、3 之後的提示詞不一致；s27 台詞標畫外 | 製作端照抄分鏡表 | 必改 2、3 與建議 s27 改完後，`r2.py` 重產 `storyboard.md` 與 `video.json`，再跑 `mkspec.py`、`prep926.sh` 重建 `colab-jobs.json`；clips-dh 跟著 d1 的動作段改（s16、s38、s20、s27） |

## 回報摘要

- **必改 9 條**，都是改文字或送一張已有的角度圖，不花錢、不用新畫圖。
- 最重要的五條：
  1. **s40 鏡位自相矛盾**：寫「鏡頭在許記門裡、門框在左緣」，送的卻是站在街上看、許記門面在左的街景，許硯又要全身在門口。改成 `wide shot down the street at standing eye height, like the picture:`，客人寫成往兩邊退、側背、臉朝地上的人。
  2. **s25 客人正臉＋高角度**：隊伍從許記門口往街裡排，六張臉都朝鏡頭；高角度跟人眼高的街景圖打架（第 24 集 s02 拍出來就是平視）。改成人眼高的定鏡、客人側背朝許記門口；搖鏡本來就沒送出去，改由剪接做數位慢搖。
  3. **s38 一鏡五件事**：改成第一格已經彎腰、糖糕與黃紙已經掉在腳邊，整支只做「慢慢側倒、背對我們、蜷著不動」。
  4. **s16 兩指點眼睛**：手勢易讀錯又擋臉，還多一個抱胸動作。改成第一格已經抱胸、瞇眼、下巴朝路上一指。
  5. **`open` 出現在七支插鏡的 `the shot opens directly on`**，s18 正好接在縫邊紙疊前面（易畫成攤開的書）：spec 一律換成 `the very first frame is already a close view of`。
  其餘必改：s20 木箱寫明立在櫃檯上、s28 從膝蓋以上改全身（低矮桌才在畫裡）、s04 加送已有的 `angles/xiaohe-angle-a-l1`、灰衣客人照聖經改「灰布長衫」（第 27 集同一刻接）。
- 參考圖：**不需要重裁或新畫就能開拍**。建議做一張免費提亮圖 `set-xuji-houjian-deng-l1`（`set-xuji-pu-houjian-l1` 加 `eq=gamma=1.9:contrast=1.15:saturation=1.1`，試過讀得出空格架、仍是暖橘夜色）給後間 s30–s34；`laisan-sleeve-l1` 其實是胸口裁切，手插鏡不要送。
- 錄音：a26 確認高 5.7 個半音，免費降 3 個半音試過、聽寫不變，交剪接用耳朵比；a36 要用耳朵聽「糖」，聽得出「藏」就照 a01 的拼音做法重錄一次；a21 接受（面板逐字疊上）；s05 的 5.96 秒放得下（第 24 集同長度用過），只要拿掉結尾的「說完停住」。
