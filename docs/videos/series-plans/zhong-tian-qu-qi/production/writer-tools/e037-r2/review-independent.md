# 第 37 集重製版 r2（e037-r2，內部 937）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-23，開拍前（d1 還沒跑；錄音 39／39 已錄齊、核對完）。只寫這一個檔；沒改 `r2.py` 或別的檔、沒開 Colab／RunPod（沒碰 `zt-live2`、`zt-live3`）、
  沒用站台 TTS、沒付費圖、沒 commit。沒讀前置代理的自審 `writer-tools/e037-r2/review.md` 與 scratchpad 的 `e937prep/PROGRESS.md`。
- 審的對象：`writer-tools/e037-r2/r2.py`、`docs/videos/zhong-tian-qu-qi-e037-r2/{script.md,storyboard.md,video.json,overlays.json}`、
  d1 提示詞 `~/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/runpod/live/d1/prompts/*.txt`（84 支）與 `colab-jobs.json`（逐鏡送圖，含 `append_pictures`）、
  `colab/runs/e937-live/{mkspec.py,spec.json,PREP.md}`、`colab/runs/e937/extras.json`、`hailuo/clips-dh-e937.json`、
  `live-action/free-e031-e040/{shanjiao_qu_ye_clean.py,shanjiao_qu_ye_e937.sh,xujia_houmen_e937.sh,xujia_yuan_ye_e937.sh}`。
- 對照：`r2-bible-e031-e040.md`（拍法 1–43、〈接點〉36→37、〈道具〉〈人物〉〈小角色〉〈場景〉〈原版必修〉第 37 集）、任務檔最後幾條教訓、`OWNER-CHECK-20261122.md`、
  `tasks/open/2026-11-21-1-30-a-b-140.md` Notes（柴刀句會畫成劍、人群聲倒放）、第 36 集 `review-independent.md`、`colab/runs/e936-live/{PREP.md,cut-review.md,cut-review-2.md,final-check.md}`。
- 參考圖全尺寸打開看過：院子 `set-xujia-yuan-ye-dong2-l1`、`-zhong`、`-shu`、`-qiang`、`-chai`、`-wu`、`-di`；渠 `set-shanjiao-qu-ye2-l1`、`-geng`、`-zhuo`、`-tian`、`-cao`、`-kong`、
  `set-shanjiao-qu-chen-l1`、`-chen-geng`、`-chen-zhuo`、`-chen-tian`（與母圖 `set-shanjiao-qu-ye-l1`、白天 `set-shanjiao-qu-l1` 比）；後門 `set-xujia-houmen-ye-l1`、`-men`、`-xiang`；
  `tangxiaotang-back-shuangji-e929-w3`、`prop-changqiang-l1`、`diaoqi-portrait-l1`。自己放大看的在 scratchpad `e937rev/`（`gate.png` 院門、`ye2-left.png` 護欄清理、`ye2-plank.png` 木板、`houmen-roof.png`）。
- 接點：自己從第 36 集定版成片 `e936-live.mp4`（200.84 秒）抽 165–200 秒每 2 秒一格（scratchpad `e937rev/tail/sheet.jpg`、`end.jpg`、`gate170.jpg`）。
- 語速：用錄好的 39 句實測（`tools/span937-buy.txt`、`span937-retake.txt`、`audio/README-retakes.txt`），不再估。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| d1 清單 | 84 支、每種子 261 秒（5 秒 5、6 秒 30、8 秒 7），合計 522 秒，跟 `r2.py` 的 `BUY` 與 `colab-jobs.json` 逐鏡相符 |
| 唐小棠的名字與圖 | 84 支提示詞 0 個 `Tang Xiaotang`；`colab-jobs.json` 每支送圖都沒有她的三張臉部圖；`stand-up collar`、`apricot` 0；`clips-dh-e937.json` 42 筆也沒有她的名字與立領句 |
| 雙丸子背影圖（站主 11-22） | s07、s09、s32、s34、s35 五支都在最後一張加送 `tangxiaotang-back-shuangji-e929-w3`，句子「that picture fixes the hairstyle only, never the place or the light」在場景句後；s08 插鏡只有手，不送，合理 |
| 跪姿拍到膝蓋（站主 11-22） | s28 刁七 `framed full figure with both knees on the ground`、s39 許硯 `framed full figure with his knee on the ground`；s40 寫成蹲；**s10 跪著埋袋的壯丁沒寫**（必改 5） |
| 柴刀（站主 11-21） | 0 個 `chopper`、`sword`、`hooked`、`slightly hooked tip`；秦霜身分句的柴刀 extras 已拿掉；c05、c13 的柴刀不拍。刁七的長刀見建議 2 |
| 人群聲倒放（站主 11-21） | PREP §0 與 r2.py 配樂段已寫 s35 歡呼、s17–s21 喊殺、s31 巷子用 `crowd-murmur.py 37`；39 句已齊，可以做 |
| 會長字、會畫錯的字 | 0 個 `open`、` mud`、`crowd`、`hundreds`、`villager`、` pool`、`deep pool`、`causeway`、`fog`、`lantern`、`candle`、`dagger`、`blade`、`armour`、`tassel`、`stubble`、`cinema camera`、`crescent`、`sign`、`plaque`、`banner` |
| 月亮 | 渠的夜景塗掉細月、提示詞不寫月亮（只寫冷月光）；後門 `full moon high above`（圖上滿月，接第 36 集 s36 滿月） |
| 光線句 | 36 個夜鏡 `the cool moonlight stays unchanged`、6 個天快亮鏡 `the cold grey-blue dawn light stays unchanged`；clear-and-still 逐鏡換成夜氣、油燈、火把、石灰粉、蒸氣、天快亮 |
| 人數 | s01 五、s09b 七、s10 五、s13 七、s18 四、s20 四、s31 九、s34 七、s35 六、s39 四：`exactly N` 都跟描述對得上；`only` 句每支再寫一次 |
| 笑 | 寫笑的只有 s37（稿子准「淡淡一笑」）；s12「a faint easy look in his eyes」不寫笑字；其他有臉的鏡都逐部位寫 `not smiling`；二牛每鏡（s01 s02 s11 s12 s24 s28）都寫 |
| 精修文字 | 通用說話視線留著的 s04 s06 s07 s09 s12 s13 s25 s27 s31 s36 s40，聽的人都在畫裡；畫外與看地方的 s01 s02 s05 s10 s11 s14 s15 s18 s19 s22 s24 s28 s29 s30 s37 都換成 `GAZE_REFINE` 方向句 |
| 錄音對 BUY | 39 句全部放得下（最緊 s01 5.08／6、s05 重錄 5.44／8、s37 兩句 5.20／8、s24 重錄 5.04／8、s14 4.06／6、s36 4.13／6）；a20「扔！」要人耳聽（PREP 已記） |

## 寫稿者的決定：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| 接點 36→37：站位 | 成片最後一鏡 s38（196–200.8 秒）：許硯在畫左、側臉朝右上、手上一盞燈；唐小棠雙丸子背影在他右前、正中；背景院門口、樹、後牆、木桶、**滿月**。s31（170–172 秒）草蓆在樹與井之間的院子中段、睡的人頭朝畫左；s35 秦霜在後牆右段牆頭、s37 阿令在屋門口。本集 s01 從院子朝院門拍、許硯與唐小棠在鏡頭這一側（不入鏡），二牛從院門朝鏡頭跑、樹旁四個流民坐起；s03–s09 許硯在畫左朝右、唐小棠背影在正中、秦霜從後牆右段井旁跳下：**接得上** | 接受 |
| 接點 36→37：院門 | 圖上（`-ye-dong2-l1`、`-zhong`、`-chai`）**門扇是掛在右門柱上、往內半開**，門洞左半是空的（看得到牆外的田），不是 r2.py 寫的「swung back inward against the left post」（scratchpad `e937rev/gate.png`）。成片 s38 背景的門洞也是開的。照圖寫就好，但左右要寫對 | 必改 1 |
| 接點 36→37：滿月、草蓆 | 渠的細月已塗掉、後門滿月，合理。院子圖本身**沒有草蓆**，s01 的四個人與蓆子是文字加的（樹旁右邊那塊空地夠坐四人），s09b 全景的 `YARD` 也寫了蓆子；第 36 集 s31 就是這樣生出來的，接受 | 接受 |
| 阿令在第一場不見了 | 第 36 集 s37 她在屋門口；本集 s07 背景正是屋的黑門洞，空的；稿子 c07「回頭看一眼屋門口的阿令」不拍。觀眾不太會追，s07 台詞點了她 | 接受 |
| 渠頭的格局 | 圖上確實沒有橫過渠的土埂、沒有閘板、沒有山。左岸新土堆當土埂、守的人面向左、淺坑挖在土埂前的乾地、流寇從左邊遠處松樹過乾地來：**跟圖一致、軸線自洽**（s14／s15／s19 面向左、s18／s22／s25 刁七朝右、s26／s27 秦霜在右流寇在左）。但「只有一條路」讀不出來：土埂外是一整片平坦的空地，流寇哪裡都能走，土埂也很長，沒有窄口；目前只能靠 s04 台詞 | 建議 5 |
| `-ye2` 的清理 | 細月、地平線方塊、直立平木板都清乾淨了；木板改成細樁合理（圖上其實有兩三根支撐，文字寫一根，接受）。**護欄那一帶留下一道比上下都亮的直條**（約 x 310–500、y 337–348，右端在 x≈500 一刀切齊），`-zhuo` 放大 2 倍後就在人物後面，s14 s18 s22 s25 都會看到；`-kong` 左下、`-cao` 左上、`-chen`／`-chen-zhuo` 同樣有。木板後方塗掉直立板的地方是一塊橫向拉絲的矩形（`ye2-plank.png`），平常亮度不明顯 | 必改 6、建議 7 |
| 左邊的分層擋土坡與修剪的灌木 | 白天母圖就有（像水泥分層護坡），第 36 集成片沒被點名，接受；但清理留下的亮條會讓它更像公路邊坡 | 必改 6 |
| `-chen` 像不像天快亮 | 整張提亮成灰藍、松樹上方一條灰白，讀得出黎明前的冷光；但**天空上半還是滿天星**，地面卻像陰天白天一樣均勻亮，兩者有點打架；左邊乾地提亮後像一片灰白的鋪面或霜 | 必改 7（星星）、建議 6 |
| `-chen-zhuo` 給 s37 | 文字寫「behind him, soft, only the pale grey-white sky low over the far pines」，圖是三分之二的乾地加分層擋土坡、右上角一點天：**圖文不一致** | 必改 7 |
| 唐小棠（拍法 3、4、40） | s32、s34、s35 從背後說話、s08 兩手抓袖插鏡、s07、s09 不點名背影，五鏡都 `HEADSTILL`、正中、剛好兩顆丸子；全集沒有臉部圖與名字；不寫淡杏外衣與高立領：**合理**。s32 兩手往前甩桶、s34 右手抓門框肩膀一抖，都只動手臂 | 接受 |
| 雙丸子背影圖帶白天進夜景 | 圖是藍天白天、背後兩棟瓦屋，佔畫面約四成。s32、s34 只送兩張圖（巷子＋這張），它佔一半份量；「只定髮型、不定地方與光」的句子有寫，但白天天空與屋子仍可能滲進來。站主指定的是這個檔，改圖要協調者決定 | 建議 1 |
| 動作戲：一鏡一個動作 | s20 扔（劈手＋三人砸袋，同一拍，接受）、s23 踩火（第一格火把已在草上，好）、s26 奪槍（一個連續動作）、s32 潑水、s33 刀鞘敲手腕（拍法 22，好）都在畫面裡。**s21 把「兩個人踩破乾草掉進坑」寫在構圖（第一格）裡當進行中的動作**，又跟煙吞火把、火光熄、黑影踉蹌疊在 5 秒裡；**s27 槍頭先往上挑飛舉過頭頂的刀、再回到喉嚨前停住**，是一上一下兩段；**s28 刁七兩手舉在肩旁、繩子卻要繞肩、在背後打結** | 必改 3、建議 3、4 |
| 長東西第一格分開 | 鋤頭（s09b、s35 寫 well apart）、竹竿（s13）、刀與槍（s27 第一格槍低平、刀舉頭頂）有寫；**s26 流寇的槍第一格就「挺著刺過來」、s27 槍「低平端著指向他」，都沒寫槍頭離人還有一段**，模型常把槍頭直接畫進身體 | 必改 4 |
| 兵器只有劇情要的 | 刀只有刁七一把（s18–s28）、槍只有一桿（s26 流寇的→秦霜，s28 只露槍頭、s35 s36 她拿著）、阿令刀不出鞘、流寇素木棍：**合理**。s28 槍頭從畫左伸進來，但秦霜在 s26／s27 都站在畫右 | 必改 2 |
| 拆鏡 s09b、s16b | s09b 合理（交燈與出門是兩個動作，2026-11-06 審稿補的那句）。s16b：實測系統 2.84＋心裡話 3.01＝5.85 秒，其實塞得進一支 8 秒；但拆開換景別、各一個動作，剪起來節奏更好，多花約 0.4 CU，接受 | 接受 |
| 再拆 s21、s27？ | s21 用必改 3 的免費改法（掉坑在第一格已完成）就不用拆；s27 見建議 3 | 必改 3、建議 3 |
| 刁七第一次出場 | 破布短褐、繩腰帶、黑綁腿、不穿皮甲、疤在左（extras）：合理。定妝照上的疤只是左顴骨上一小段淡痕，文字寫「從左眉骨斜到左顴骨的長疤」；而他每鏡都是臉朝畫右的四分之三側，左頰在遠側，疤幾乎都看不到 | 建議 9 |
| 二牛、小禾、許硯 | 二牛六鏡都逐部位寫不笑；小禾 s40 整張臉燒紅、不寫細點；許硯 s40 眉頭擠緊、眼睛睜大（原版必修），s37 唯一的笑：**合理** | 接受 |
| 人數與群眾（拍法 34、37） | 流寇只有背影、剪影、遠處黑影；四百人＝松樹流出的一長串小火光＋六個黑影；六十壯丁＝三到七個衣色年紀不同的人；婦孺＝s39 兩個婦人：**合理** | 接受 |
| 對畫外的人說話（拍法 31） | s02、s05、s24、s37 寫「toward someone out of sight beyond the … edge」加那一側只有什麼景、只有一人；s01 是全景有五人，只寫視線，可以；看地方的 s03 s15 s16 s19 s28 s38 寫成遠山、乾地、火光、土埂 | 接受 |
| 過肩邊緣的肩 | s06 秦霜在右緣（接 s04 她在右、s05 她朝左看）、s14 許硯在右緣（她朝左看乾地，接 s15 他朝左）、s25 許硯在右緣（刁七從左衝來，接 s26 秦霜在右）、s36 許硯在左緣（接 s35 秦霜在他右邊、s37 他朝右看她）：**都接得上** | 接受 |
| BUY 照實測 | 39 句都放得下；s04（4.39）、s06（4.28）、s09（3.72）買 8 秒偏寬，可省約 0.6 CU，但都有動作，站主規則品質優先，不改 | 建議 11 |
| 後門 | 圖上門在右、往內半開、門左柴堆、巷子往左、滿月：文字照圖。整張圖（只給 s31）右上屋簷下有一塊平的空白木板（`houmen-roof.png`） | 建議 10 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 37 | `YARD`（s09b）、s01 構圖 | **院門的門扇寫錯邊**：圖上門扇掛在**右**門柱、往內半開，門洞左半是空的；r2.py 寫「its plank leaf swung back inward against the left post」（PREP、`zh` 也寫靠左柱）。照字畫，模型會把門扇搬到左邊或在片中自己動門（第 35 集 fix1 s34、fix3 s32） | 拍法 29（圖說了算）、36；任務檔「門要明寫關著或推開」 | `YARD`：`with its plank leaf swung back inward against the left post` → `with its slatted plank leaf hung on the right gate post and standing half open inward, the left half of the gateway clear`；s01：`the plank gate leaf swung back inward against the left gate post from the first frame to the last, the gateway clear in the middle of the back wall` → `the slatted plank gate leaf hung on the right gate post standing half open inward from the first frame to the last, unmoving, the left half of the gateway clear`，`already through the gateway` → `already through the clear left half of the gateway`。`zh`、PREP §1／§2、聖經〈接點〉36→37 的「靠左柱」一起改成「掛在右柱、往內半開」 |
| 37 | s28 | **槍頭從畫左伸進來**：s26、s27 秦霜都在畫右、刁七在畫左；s28 同一場、刁七跪在中間，秦霜的槍應該從**右**邊來 | 軸線（秦霜右、流寇左）；拍法 31 | `the small iron head of a long spear reaching in from the left edge` → `… from the right edge`；`only the head of a spear at the left edge`（mkspec 的 only 句）→ `at the right edge`；`zh`「從畫左伸進來」→「從畫右伸進來」 |
| 37 | s21 | **掉坑寫成第一格的進行中動作**：構圖寫「two of them dropping waist-deep into hidden pits as the straw over the pits gives way, their torches falling to the ground」，動作句又寫煙翻滾、火光熄、黑影踉蹌：5 秒裡三四件事，模型多半只做一件或亂做 | 拍法 32（前置動作在第一格完成、一鏡一個動作） | 構圖改 `two of them already sunk waist-deep in hidden pits from the first frame, the broken straw around their waists, their torches lying on the ground`；動作只留煙吞火把：`the thick white powdery smoke rolls higher and wider across the field and one torch after another dims and goes out inside it`（掉坑由 s24「全掉進坑裡了」交代） |
| 37 | s26、s27 | **長桿第一格沒分開**：s26 流寇「already lunging at her with {RAID_SPEAR} thrust forward」、s27 秦霜「{SPEAR} held low and level … toward him」，都沒寫槍頭離對方的距離，第一格常直接畫成槍頭插進身體或碰到刀 | 任務檔教訓「長桿第一格分開」；拍法 32 | s26 加 `, its spearhead still an arm's length short of her in the first frame`；s27 加 `, its spearhead pointing low at the ground a step short of him, well apart from his saber` |
| 37 | s10 | **跪著的壯丁沒寫拍到膝蓋**：`a lean young man in a rust-red jacket already kneeling from the first frame over a shallow hole`，全景但沒寫全身 | 站主 2026-11-22（跪姿要拍到膝蓋） | 加 `, framed full figure with both knees on the earth`；或改成蹲：`already crouching low on his heels` |
| 37 | `shanjiao_qu_ye_clean.py` 第 1 步（`-ye2`、`-zhuo`、`-kong`、`-cao`、`-chen`、`-chen-zhuo`） | **護欄清理留下一道亮直條**：每欄用下面 13 px 的坡面蓋掉護欄，那段坡面正好是亮的一階，結果 x 0–500 一道比上下都亮的平直條、右端在 x≈500 一刀切齊；`-zhuo` 放大後在 s14 s18 s22 s25 人物身後（s11 s17 s21 也有），會被讀成欄杆或路緣石再長回來 | 拍法 29、33（塗掉要用旁邊同材質接過去、柔邊、不能留方塊）；第 36 集成片審查（地平線方塊長成高樓） | **免費**：第 1 步改成上下內插：每欄 `out[top:top+13, x] = 由 a[top-2, x] 線性過渡到 a[top+15, x]`，處理範圍延到 x 0–520、在 x 480–520 跟原圖柔邊混合；新 id（`-ye3` 一族，拍法 19），重裁 `-zhuo`、`-kong`、`-cao`、`-chen`、`-chen-zhuo`（`-geng`、`-tian` 不含這一帶，可沿用），README 記一行 |
| 37 | s37（`-chen-zhuo`）；`-chen` | **s37 圖文不一致**：文字只要灰白天與遠處松樹，送的是三分之二乾地加分層擋土坡；而 `-chen` 的天空上半仍是滿天星，跟「天快亮的灰白天」打架，s37 若改送天空的裁切星星會更顯眼 | 拍法 29、35 | **免費**：`-chen` 先去星（只在 y < 330 的天空：亮度比 9×9 中位數高 25 以上的點換成中位數，外擴 1 px），新 id；再裁 `c "$C" set-shanjiao-qu-chen-kong-l1 640:360:240:0`（同 `-ye2-kong` 的取景：松樹頂上的天），s37 改送它，背景句照舊（`only the pale grey-white sky low over the far pines`）。s35 全景改送去星後的 `-chen` |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 37 | s07 s09 s32 s34 s35 | 雙丸子背影圖是**藍天白天**、背後兩棟屋，s32、s34 只送兩張圖，它佔一半份量，白天的天色或屋子可能滲進夜裡的巷子 | 拍法 8（夜就是夜）；站主 11-22 指定這個檔 | 先照站主規則跑 d1，看 s32、s34 有沒有變亮或長出瓦屋；有的話（要協調者同意改站主指定的圖）做一張免費的夜版：藍天（b > r+60）換成夜藍、屋子壓暗模糊，新 id，句子不變 |
| 37 | s18–s28（`SABER`） | 「one long single-edged broad-backed saber」只寫長與單刃，沒寫刀身形狀，可能畫成直的雙刃劍——站主 11-21 記的正是「刀變劍」 | 站主 11-21 柴刀句的教訓；拍法 5 | `SABER` 改 `one long single-edged saber with a broad, gently curved back and a blade that widens toward the tip, a plain round guard`（不寫 sword 這個字）；或先看 d1 s18 |
| 37 | s27 | 槍頭往上挑飛舉過頭頂的刀、再回到喉嚨前停住，是一上一下兩段；8 秒裡模型常只做一半（挑了沒停，或停了沒挑） | 拍法 32 | 免費：第一格改成刁七的刀**舉到肩膀高、往下劈到一半**，挑刀的路徑就短；或拆成 s27（5 秒無台詞：挑飛，剪接在刀出畫）＋s27b（6 秒：槍尖停在喉前說話），兩種子多約 6 秒、約 **0.3 CU** |
| 37 | s28 | 刁七「兩手舉在肩旁」，繩子卻「已經在他肩上繞兩圈」、二牛「在他背後打結」：手舉著被繞肩、背後打結，畫面難成立，模型可能讓他放手或繩子穿過手臂 | 拍法 32 | `both his hands raised empty at his shoulders` → `both his hands already pulled behind his back from the first frame`，繩子 `looped twice round his chest and upper arms`；投降的感覺交給低頭與跪 |
| 37 | s04、s17（格局） | 「下山的路，最後都得走渠頭那道土埂」讀不出來：土埂外是一整片平地，沒有窄口 | 原版劇情要的「一條路」 | 免費：s17 六個黑影寫成 `running one behind another in a single file along one narrow beaten track across the field toward the ridge`（圖上沒有小路，文字加，風險低）。付費：Qwen 在 `-ye`（或 `-ye3`）只改一件事「一條窄土路從松樹那頭直通到土埂」，約 **1.5–2 CU**，再免費重裁 |
| 37 | s35–s40（`-chen`） | 地面亮得像陰天白天、左邊乾地像灰白鋪面或霜 | 拍法 8；任務檔「天快亮前寫 last dark hour」 | 免費：`eq` 的 gamma 1.55 → 1.35、灰白帶只留在 y 0.35–0.50h，地面暗一點；跟必改 7 的去星一起做 |
| 37 | s15 s16 s16b s19 s36 s38（`-tian`）、s10 s13（`-ye2`） | 塗掉直立板的地方，木板上下各一塊橫向拉絲的矩形，左右邊緣直 | 拍法 33（第 27 集暗方塊長回來） | 先看 d1；長出板子或箱子再把那塊改成用左右 40 px 的裂土貼過去（新 id） |
| 37 | s35 | 秦霜拿長槍入鏡，但沒加送 `prop-changqiang-l1`（s36 有），全景小、風險低 | 〈道具〉長槍同一桿 | 可加在最後一張（第 5 張圖）；或接受 |
| 37 | s18 s22 s25 s27 s28（刁七） | 定妝照的疤是左顴骨一小段淡痕，文字寫「從左眉骨斜到左顴骨的長疤」；他每鏡都臉朝畫右，左頰在遠側，疤幾乎看不到 | 拍法 6、29 | 文字照圖改 `a short pale old scar on his left cheekbone`；第一次出場要讓疤被看見的話，s28（低頭跪）寫 `his face lowered and turned a little to screen left`；或接受（第 39、40 集還會出場） |
| 37 | s31（`set-xujia-houmen-ye-l1`） | 右上屋簷下一塊平的空白木板，掛著的平板會長字 | 拍法 33 | 先看 d1 s31；長字就免費用旁邊瓦簷與梁接過去（新 id） |
| 37 | BUY | 實測都放得下；s04、s06、s09 改 6 秒可省約 0.6 CU、s16b 併回 s16（8 秒）可省約 0.4 CU | 聖經〈每集鏡數〉 | 品質優先，不改；若點數吃緊再考慮 |

## 接受（看過、不用改）

| 項目 | 為什麼 |
| --- | --- |
| s01 二牛已經進門 | 第一格已衝進門、跑三步停、平掌往後一揮，一個動作；不笑逐部位寫；四個流民第一格已坐起、嘴閉著 |
| 唐小棠 s08 插鏡 | 第一格就是兩手抓袖口、背景只寫暗地（拍法 10、35），送 `-di` 只當地面；錄音是她的話 |
| 秦霜 | 柴刀全集不寫；s04 跳下在第一格完成；s14 改成許硯肩後拍她、她的嘴在畫面上；s19 極輕、s20 張嘴喊 `nospeak`；s36 槍頭朝上頓地 |
| 阿令（拍法 22） | 刀鞘與刀柄一整塊深色木頭、一掌長、在右手；s33 刀鞘一端敲手腕、不見刃；不寫紅唇 |
| 刁七 | 不穿皮甲、破布短褐、繩腰帶、黑綁腿；s22、s25、s27 臉上白粉一大片；眼睛瞇著流淚不寫紅眼 |
| 火把與煙（拍法 37） | 遠處寫一長串小火光、六個黑影各一支、後門三支；「火把全滅了」之後渠頭不再有亮的火把；煙只寫 `thick white powdery smoke` |
| 天快亮的站位 | s35 唐小棠背影正中、許硯與秦霜面向她（秦霜在他右）、三個壯丁舉鋤頭；s36 許硯肩在左、s37 他朝右看她、s38 回頭看左邊的土埂：方向一致 |
| 錄音 | 39 句逐字照稿、全部放得下 BUY；重錄 4 句、變調 7 句、相鄰說話者 ≥ 3 半音；刁七（Fenrir）第一次量已補進聖經 |
| `POOLMARK` | d1 已拿乾淨（0 個 `pool`）；PREP §6 寫明 fix／retake 都要帶替換 |

## 小結

- **必改 7 項**，全部是改字或免費清理、重裁，不花錢：(1) 院門的門扇在圖上掛在**右**門柱、往內半開，不是靠左柱（`YARD`、s01、PREP、聖經一起改）；(2) s28 秦霜的槍頭要從**右**邊伸進來；
  (3) s21 掉坑改成第一格已經掉進去，動作只留煙吞火把；(4) s26、s27 長槍第一格寫明槍頭離人還有一段；(5) s10 跪著的壯丁要拍到膝蓋（或改蹲）；
  (6) `-ye2` 的護欄清理留下一道亮直條，免費改成上下內插、新 id 重裁 `-zhuo` 一族；(7) s37 圖是乾地與擋土坡、文字只要天空——`-chen` 去星後裁一張 `-chen-kong` 給它。
- **建議 11 項**；要花錢的只有兩項：s27 拆成挑刀與停槍兩鏡（約 0.3 CU）、渠頭加一條窄土路讓「只有一條路」讀得出來（約 1.5–2 CU）。其他是免費或先看 d1：雙丸子背影圖的白天天空、刁七的刀寫成彎背刀免得變劍、s28 繩子與舉手、`-chen` 地面偏亮、木板後的拉絲矩形、s35 長槍道具圖、刁七的疤、後門屋簷木板、BUY 可省的秒數。
- **站主 11-21～23 規則**：唐小棠五個背影鏡都加送髮型圖（白天天空見建議 1）；跪姿 s28、s39 拍到膝蓋，s10 漏了（必改 5）；柴刀不寫、0 個 sword（刁七的刀見建議 2）；人群聲倒放已排進剪接。
- **接點 36→37** 接得上（站位、滿月、草蓆）；只有院門的門扇左右寫反（必改 1）。
- **BUY** 照實測 39 句全部放得下，不用改。
- 改完 `r2.py`、`mkspec.py`、`shanjiao_qu_ye_clean.py`／`shanjiao_qu_ye_e937.sh`（新 id）後重跑 `build937.sh`、`prep937.sh`、`DRY=1 e937d1.sh`。
