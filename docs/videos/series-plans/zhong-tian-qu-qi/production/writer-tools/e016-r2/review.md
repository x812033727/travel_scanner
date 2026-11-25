# 第 16 集重製版（e016-r2，內部編號 916，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-15，只讀（只寫本檔）；沒用 Colab、RunPod 或任何付費服務，沒有 git commit。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e016-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e016-r2/r2.py`、
  `colab/runs/e916/extras.json`、`colab/runs/e916-live/{mkspec.py, spec.json}`，以及**實際要送出的**
  `/root/mokaair-work/videos/zhong-tian-qu-qi-e916-dh/runpod/live/d1/colab-jobs.json`（84 支，s01–s42 × 種子 9161101／9161102）與 `prompts/ref-sNN-916110{1,2}.txt`
  （兩個種子的提示詞逐位元相同，42 鏡逐鏡讀完；送圖清單逐鏡核過）。錄音 `audio/zq916a01–a39.wav` 用 wave 讀長度。
- 對照：`r2-bible-e011-e020.md`（拍法 2、3、5、7–10、15–18，時間線第 16 集）、`season-01.md` 第 16 集、`writer-tools/e015-r2/review.md`、
  `colab/runs/e91{3,4,5}-live/{review-picks-a,review-picks-b,picks-merged}.tsv` 與 `e915-live/fix1/review-picks.tsv`、第 15 集 r2 s39–s42、
  `assets/refs-live/README.md`；**放大看過**本集要送的 `set-shiqiao-l2`、`set-gongpeng-l2`、`set-zhufa-ye-l1`、`set-shuyuan-l1`（木匾、兩側白板、門內院子各裁切放大）、`set-dukou-l1`。
- 台詞：storyboard 的 39 句逐句對過 script.md，一字不差。否定名詞：42 支提示詞只剩允許的「no subtitles, captions or text」與「no talking / no mouthing words」，乾淨。
  OFFSCREEN_SPEECH 沒補畫外句；唐小棠 11 個背影鏡都有「only one with buns and pink ribbons」與固定側；賴三兩鏡都拿掉圖與身分句。這些都照前幾集審稿做到了。

## 總評

問題集中在五處：

1. **參考圖狀態壓過文字**（第 15 集 s25 秋田、s08 工棚的教訓）在本集最後一場最嚴重：`set-dukou-l1` 上沒有煙，又有一條篷船繫在棧橋，
   s41 的煙柱是本集結尾的鉤子，照現在的圖很可能拍不出來；s40、s42 人站在竹筏上卻送渡口圖，篷船會被當成他們的船。
   `set-shuyuan-l1` 兩側屋簷下掛滿大塊空白白板、木匾中央木紋打旋像淡墨字，是「紙長字」的溫床，而且超廣角變形、門內院子有一個紅色塑膠感的桶。**這兩張要重畫**。
2. **插鏡 s12、s27、s38 還送場景圖**——第 15 集 s08 兩支都先開在空工棚全景再硬切，fix1 拿掉場景圖後就好了；本集只有 s31 照做。
3. **代名詞歧義**：s01、s07、s10 的「he keeps his head still and never turns it, the back of his head toward us」緊接在許硯的動作後面；
   s21、s42 的「she keeps her head still」緊接在秦霜的動作後面。模型照字面會把說話的人凍住，或把他／她畫成背影（同一人出現兩次的來源）。
4. **書院一場的軸線**：場景句（從街這邊看：街往左、馬車在左）原封不動放進從門這邊往街上拍的反打鏡（s29、s32、s33、s34、s37）。s36 許硯朝畫左看馬車、
   s37 反打到唐小棠背後馬車仍在畫左，是本集中段鉤子那一刀的跳軸。
5. **道具與光**：唐小棠的錢袋與小金算盤都寫在「腰間右側」（s33、s34、s37、s38），兩樣會合成一樣或互換；s28 燈籠在許硯身後、紙背朝鏡頭，是逆光透紙；
   s29 紙背朝鏡頭但沒寫太陽在哪；s39 同一句裡「燈籠竿在筏尾畫右」又「筏頭在畫右」。

寫稿者最沒把握的十件事，結論：

| 問題 | 判斷 |
| --- | --- |
| 插鏡會不會先開在空場景再跳（s12 s27 s38 s31） | **會**（s12、s27、s38），s31 已照第 15 集 fix1 做對。見必改 5。 |
| 竹筏圖偏 CG、s39 筏頭方向與圖相反 | CG 感明顯（竹子是黑色粗管、像塑膠管），工棚 l2 也偏 CG 而第 14–15 集可用，**不擋開拍、建議重畫真人質感 l2**；s39 方向**必改**（必改 16）。 |
| 柳溪口煙柱畫不出、空篷船被當竹筏 | **兩件都成立**。重畫 `set-dukou-l2`（同構圖、村後一柱黑煙、棧橋空著），s40、s42 不送渡口圖。見必改 17、18。 |
| s24–s26、s32–s33 連續背影鏡單調 | 成立。s25 改許硯乾淨近景、s33 換景別。見建議 1、2。 |
| s01 手的交接 | 四拍（接、摺、塞回、按攏）跨過橫木兩隻手互碰，手指最容易糊。改成一拍。見必改 1。 |
| s33 唐小棠兩手兩樣道具 | 成立，又跟算盤同側。改成一隻手依序做、錢袋改位置。見必改 10、11。 |
| s34 一鏡太多拍 | 成立（四個動作、三人加三十人）。刪成兩拍。見必改 12。 |
| 書院圖白板與木匾長假字、s30 前景書生背影撞成許硯的臉 | 圖**重畫**（必改 8）；s30 前景改成側面中景（必改 9）。 |
| 工棚圖桶裡攪棒與斜靠竹竿架 | 圖上是兩架光禿的 A 字竹竿架（沒掛紙）與近桶裡交叉的兩根攪棒、遠桶上一根；文字寫成「掛著濕紙的晾紙架」「一根攪棒」，s13 還寫「唯一的長東西是她的竹篙」。照圖正面寫（必改 4），有空再畫 l3（建議 18）。 |

**必改 18 條、建議 18 條。**

**參考圖：`set-dukou-l1` 必須重畫成 `set-dukou-l2`**（同構圖與黎明光；村子屋後一柱濃黑煙往上翻；棧橋邊不繫船）；
**`set-shuyuan-l1` 必須重畫成 `set-shuyuan-l2`**（一般焦距、人眼高度；木匾深色漆面素平無紋；街邊店面改深色木門與深灰布簷，不掛白板；門內院子只有石板地）。
建議：`set-zhufa-ye-l1` 重畫真人質感 l2（青黃竹、紙捆壓低到能坐），並做一張水平鏡像給 s39 用（空景沒有交領，第 9 條不適用）；`set-gongpeng-l2` 有空畫 l3 拿掉攪棒與 A 字架。

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 16 | s01 | 手的交接四拍（許硯接紙、再摺一次、塞回對方攤開的右掌、按攏手指），兩人的手隔著橫木疊在一起，是手指糊掉與紙換錯手的高風險；第一格對方右手正捏著紙伸出來，又要在同一鏡變成「攤開的掌」。 | 第 15 集 s41 算盤跑到賴三手上、s42 紙正面長字；拍法 9「每樣道具寫在主人的那隻手」；e015 s42 接點：紙停在許硯胸前一掌寬、他右手垂著。 | 改成一拍、紙始終在賴三手裡：「Xu Yan lifts his right hand and closes the man's fingers over the folded slip with his own fingers, then pushes the man's closed hand back across the log toward the man's chest; the slip stays folded inside the man's fist, only a corner of its blank back showing.」刪掉 takes / folds it once more / presses back into palm。s02 第一格照接：「the man's right fist still closed around the folded slip」。 |
| 16 | s01 s07 s10 | 「he keeps his head still and never turns it, the back of his head toward us the whole shot」緊接在許硯的動作之後，he 讀成許硯：說話的人被凍住或被畫成背影（同一人兩次）。 | 第 15 集 s26、s41 背影鏡冒出第二個人；拍法 2。 | 一律點名主詞：「the thin young man in the right foreground keeps his head still, the back of his head toward us the whole shot」（s01、s07）；「the old man in the right foreground keeps his head still, the back of his grey topknot toward us the whole shot」（s10），並把這句移到許硯動作句的**前面**。 |
| 16 | s21 s42 | 「she keeps her head still and never turns it」緊接在秦霜的動作之後；畫面上有兩個女人，she 會套到秦霜身上（她本來要回頭說話／撐篙）。 | 同上。 | 「the young woman with the two buns and pink ribbons in the right foreground keeps her head still, the back of her head toward us the whole shot」（s21 寫 right、s42 寫 left foreground），放在秦霜動作句之前。 |
| 16 | s09–s17 | 工棚圖與文字打架：圖左是兩架**光禿**的 A 字竹竿架、近桶裡兩根**交叉**的攪棒、遠桶上一根；文字寫「two drying frames … hung with rows of wet blank white sheets」「one plain wooden stirring stick lying across them」；s13 還寫「the only long thing in the frame is her one green bamboo pole」——跟圖上至少五根長竿正面矛盾，模型會把竹篙跟 A 字架或攪棒混在一起。許硯在 s10、s13、s14 正站在有交叉攪棒的近桶邊、兩手拿竹簾。 | 拍法 18「背景寫在場的東西」；第 15 集 s25、s08（參考圖狀態壓過文字）；第 14 集 s15 畫左長竿是 l2 原有的 A 字架、s30／s32 竹簾畫成長竿、耙子；README 更正：l2「仍有左邊捆起的長竿三腳架與桶裡交叉木棍」。 | 場景句照圖寫：「against the left wall two tall bare bamboo A-frame drying stands leaning on the stones; across the near vat two plain wooden stirring sticks crossed in an X, resting on its rim, and one more lying across the far vat」。s09 前景改成「wide shot past the bare bamboo A-frame drying stand in the left foreground」，不寫掛紙。s13 刪掉「the only long thing」句，改「Qin Shuang's green bamboo pole is the only thing anyone carries; the stirring sticks stay resting on the vats」。s10、s13、s14 加「the crossed stirring sticks stay on the rim of the near vat beside his hip, his two hands only on the bamboo mat」。 |
| 16 | s12 s27 s38 | 三支手的插鏡都送場景圖（工棚、竹筏夜景、書院）；s31 已照第 15 集 fix1 不送。 | 第 15 集 s08：兩支都先開在空工棚全景再硬切，fix1 拿掉工棚圖改送 xuyan-angle-a 只當手的主人，抽格「沒有硬切」；第 13 集 s09、s14、s30 插鏡前也有全景硬切／疊化。 | s12：不送 `set-gongpeng-l2`，改送 `xuyan-angle-a-l1`，開頭照 s31 寫「The hands and sleeves belong to Xu Yan shown in <Picture 1>, whose face stays out of the frame.」。s27：不送 `set-zhufa-ye-l1` 全圖；送一張從它裁出的燈籠特寫（燈籠與竿頭、黑夜，裁切免費），寫「the lantern shown in <Picture 1> glows beside the sheet」。s38：不送 `set-shuyuan-l1`，送 `tangxiaotang-portrait-l1` 只當手、袖與腰帶的主人：「The hands, sleeves and sash belong to Tang Xiaotang shown in <Picture 1>, whose face stays out of the frame; the frame shows only her waist, her hands and the table edge.」 |
| 16 | s28 | 燈籠在許硯右後方，紙由左邊伸進來、「its plain blank back toward us, lit from the front by the lantern」：燈籠照到的是朝許硯那面，朝鏡頭那面是背光——就是逆光透紙。 | 拍法 17「紙一律正面打光、不透光」；第 11 集紙長金色閃粒；第 15 集 s17 紙背淡框線與字痕。 | 「the sheet is held low at the left edge, below the lantern's height, its blank back toward us lit softly from the side by the lantern glow on his right, thick and opaque, plain matte white, the lantern light falling on its edge」；許硯接過後立刻摺起（已寫），不要舉高對著燈。 |
| 16 | s29 s32 | s29 從唐小棠背後拍，兩張紙朝街、紙背朝鏡頭，只寫「lit from the front by the sun」——沒說太陽在哪；書院圖太陽在左前方，反打過來很容易在紙後面，紙背朝鏡頭會透光。s32「held up into the sunlight」同樣是逆光字眼。 | 拍法 17；storyboard「正面受光」。 | s29：「the morning sun is behind the camera on the left, lighting the backs of both sheets toward us flat and even, both sheets thick and opaque, plain matte white」。s32：「her right hand holds the sheet up at shoulder height, the sun from the left grazing its edge, thick and opaque, plain matte white」，刪 into the sunlight。 |
| 16 | s29–s38 | `set-shuyuan-l1` 放大看：街兩側屋簷下掛著十幾塊大塊空白白板（模型最愛往上面長字）、木匾中央木紋打旋像兩三筆淡墨字、門內院子一個紅色塑膠感的桶與現代感長凳、整張是超廣角變形。十支鏡都送這張。 | 拍法 7「紙上的字一律不拍：招牌、匾額寫成空白」；第 7 集 `set-chouduan-l1` 37001 招牌有假字被淘汰；第 13 集帳冊白籤條長假字、木牌似字要後製糊。 | **重畫 `set-shuyuan-l2`**：一般焦距、人眼高度，大門與三級石階在右、街往左；木匾深色漆面素平、沒有木紋花樣；街邊店面寫深色木板門與深灰布簷，不掛白板；門內只有石板地。提示詞場景句同步改：「dark wooden shop fronts with plain dark grey cloth awnings under their eaves」「one dark lacquered wooden plaque above the doors, smooth and plain」。重畫前不開拍書院這十鏡。 |
| 16 | s30 | 前景三個書生的肩與方巾（背影、虛焦）加上送許硯三張圖：前景背影最容易長成許硯的臉或側臉（寫稿者自己也擔心）。 | 第 13 集 s20、s41 前景許硯轉成側臉露臉頰；第 9 集「一送就多一個分身」；拍法 2。 | 前景拿掉，書生改成中景側面：「medium shot of Xu Yan behind the long table; at the left edge of the frame, across the table, two young scholars in pale blue-green robes and black square caps stand side-on in profile facing screen right, small and soft, round young faces different from his, their caps covering their hair」。末句「Xu Yan appears only once, behind the table」。 |
| 16 | s33 | 一鏡兩隻手各做一件事（右手收錢入袋、左手推紙），又是背影過肩；收錢要伸過桌子再縮回腰間，兩隻手交錯時錢或紙最容易跑到書生手上。 | 第 15 集 s41 算盤到賴三手上；拍法 9。 | 改成一隻手依序做、另一隻手定住：「her left hand stays flat on the stack of blank paper the whole shot; her right hand takes the coins from the nearest scholar's open palm and drops them into the blue pouch at the front of her sash, then the same right hand slides one small stack of paper across the table to him」。 |
| 16 | s33 s34 s37 s38 | 藍布錢袋與小金算盤都寫在「at her own waist on her right side」：s33、s34、s38 寫錢袋、s37 寫算盤，兩樣同位置會合成一樣，或錢袋在 s37 變算盤、算盤在 s33 消失。 | 拍法 4（定妝照腰間那把小金算盤）；第 15 集 s41。 | 固定兩個位置，四鏡都兩樣一起寫：「one small plain blue cloth pouch tied at the front of her sash, and the small gold abacus hanging at her right hip」。s37 撥算盤的手寫「her right hand on the small gold abacus at her right hip」。 |
| 16 | s34 | 高角度全景、三十個書生加三張臉，要做四件事（秦霜遞紙給許硯、許硯遞給書生、秦霜捲油布夾腋下、唐小棠把小包拉近），第一格就有兩人之間傳遞；6 秒、人小，傳遞的手一定糊、紙會跑到別人手上。 | 寫稿者自己的疑慮；拍法 9；第 13 集 s15「台詞與動作順序顛倒」、多拍時模型只做一半。 | 刪成兩拍、第一格已就位：「Xu Yan already holds the last small stack of blank paper and hands it across the table to the scholar in front of him; Qin Shuang, at the right end, rolls up the empty oilcloth and tucks it under her left arm; Tang Xiaotang, at the left end, keeps her left hand resting on the small oilcloth packet the whole shot」。刪掉「handing a small stack of plain white paper to Xu Yan」。 |
| 16 | s35 | 孫掌櫃要先「看街一會兒、放下簾子、轉頭」才開口，a33 錄音 5.48 秒；6 秒片段可用約 6.58 秒，加 0.5 秒餘裕要 5.98 秒，前面的動作只剩半秒，嘴型會被擠掉或句子剪在動作中間。 | storyboard「剪接以錄音長度＋0.5 秒為準」；第 14 集 s10、s21 起點離第一個字只剩 0.06–0.08 秒；第 15 集 s15 順序顛倒要重寫。 | 二選一：（a）買 8 秒（本鏡允許薄笑，不必為不笑壓短）；（b）留 6 秒、把話跟動作疊在一起：「From the first frame he is already speaking low toward the front of the carriage on screen left, his eyes still on the street through the gap; on his last word his right hand lets the indigo curtain fall half shut.」 |
| 16 | s29 s33 s34 s37 | 書院的場景句是從街這邊看的（街往左、馬車在街左遠處），但 s29、s32、s33、s34、s37 是從門這邊（唐小棠背後、門樓瓦頂）往街上拍的反打，場景句沒改：s36 許硯朝畫左看馬車，s37 反打到她背後馬車仍在畫左——中段鉤子這一刀跳軸；s29「scholars walking toward the gate at the right」在門這邊拍時門在鏡頭後面。s34 唐小棠已正確地放在桌子左端（門這邊看的鏡像），隊伍卻仍往左拐。 | 拍法 9「每鏡用畫左畫右寫死位置」；animation-camera 軸線；第 15 集 s41 跳軸被列必改。 | 門這邊的五鏡另寫一個場景句：「seen from the gate steps looking out over the long table: the stone-paved street running away to the right between white walls and dark shop fronts; far down the street on the right, small, the closed black-canopied carriage」。s29「scholars walking up the street toward the table and the camera」；s33「queueing from the table away down the street to the right」；s34「winding along the street and round the corner at the right」；s37 唐小棠改到左前景：「in the left foreground … beyond her far down the sunlit street on the right, small, the closed carriage」。 |
| 16 | s39 | 同一句場景句寫「one tall bamboo pole standing at its stern on the right … lantern」，構圖句又寫「the raft heading toward screen right: at the bow on screen right Qin Shuang」——筏頭筏尾同在畫右；送的 `set-zhufa-ye-l1` 燈籠竿在畫右、筏頭朝左下。參考圖會贏，竹筏會倒退著走或秦霜站在燈籠竿旁。 | 寫稿者疑慮；第 15 集 s25「參考圖狀態壓過文字」；逆水往畫右是對的（s18 順流往畫左）。 | 不送原圖；送 `set-zhufa-ye-l1` 的水平鏡像（空景可翻，第 9 條只管交領人物；本機 PIL 一行），場景句改：「one tall bamboo pole standing at its stern on screen left with one plain blank paper lantern burning low; the bow on screen right」，兩捆油布改成「only one rolled-up empty oilcloth in its middle」與構圖句一致。 |
| 16 | s40 s42 | 人站在竹筏上，卻只送 `set-dukou-l1`（渡口、棧橋、繫著一條空篷船）；模型最自然的做法是把他們放進那條篷船，或竹筏消失。s40 中景背景只是天，用不到渡口。 | 寫稿者疑慮；拍法 2 的「送一張圖就照它畫」；第 15 集 s26 秋田圖換成定妝照後前景才乾淨。 | s40：不送場景圖（只送秦霜一張），寫「she stands on the green bamboo poles of the raft, the open water and the red dawn sky behind her on screen left」。s42：不送 `set-dukou-l1`，改送 `set-dukou-l2`（見下一條）或不送場景圖，寫「they are on the open bamboo raft of eight lashed green bamboo poles, the far bank and the smoke beyond them」，場景句刪掉 covered boat。 |
| 16 | s41 | 結尾鉤子的煙柱只在文字裡；`set-dukou-l1` 沒有煙，天空乾淨。s41 是只靠一張場景圖的主觀鏡，參考圖狀態會壓過「one thick column of dark grey smoke」。 | 第 15 集 s25（圖上已是犁溝，文字的「還沒翻的稻茬」拍不出）；`season-01.md` 第 16 集結尾危機就是這柱煙。 | **重畫 `set-dukou-l2`**：同 l1 構圖與黎明光，村子屋後一柱濃黑煙翻上去，棧橋邊不繫船。s41 送 l2，場景句刪 covered boat，改「the low wooden jetty standing empty」。重畫前不開拍 s41。 |
| 16 | s37 | 「the young woman's fingers stop dead on the abacus beads」：第一格沒寫手指在撥，只有「停」沒有「動」，模型會整鏡不動，「臉一白」的反應就沒了。 | storyboard「撥算盤的手指停住、肩膀僵住」；拍法 10「第一格就是主體」；第 13 集 s15 只寫結果、動作沒做。 | 「From the first frame her right forefinger flicks the beads of the small gold abacus at her right hip, two quick flicks; then the finger stops dead on a bead and her shoulders go stiff and still to the last frame.」 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 16 | s24–s26 | 三鏡同一個過肩機位（她左前景、許硯畫面中偏右），只差景別一級，三句對話看起來像同一支片。 | 寫稿者疑慮；animation-camera 同一機位連剪。 | s25 改許硯乾淨近景（他自己的台詞，不必有她的背）：「close-up of Xu Yan at the stern, the lantern just behind him on the right, his face three-quarter to screen left toward the middle of the raft」，送他三張圖，刪前景背影。s24 維持中景過肩、s26 維持中近景過肩。 |
| 16 | s32–s33 | 兩鏡同機位過肩，接著 s34 又是全景。 | 同上。 | s32 推成中近景過肩（她舉紙的手與肩、書生頭虛焦）；s33 改高一點的中全景：「a slightly high medium-wide shot from behind her right shoulder, the whole queue running away down the street on the right」。s33 運鏡把 tracking 改成 slow push in（沒有人走動可跟）。 |
| 16 | s20 | 鏡頭在唐小棠背後往筏頭方向拍，「beyond her only the dark river ahead」，但秦霜就站在筏頭撐篙，照理應該在她前面；s19、s21 都有秦霜，s20 她不見了。 | 接戲。 | 機位轉成側後方往岸看，讓筏頭出畫：「from behind and a little to her right, looking across the raft toward the dark left bank; the bow is out of the frame」。 |
| 16 | s20 | a18 剪尾後 6.23 秒，6 秒片段可用約 6.58 秒，＋0.5 秒是 6.73 秒，放不下。 | storyboard 剪接規則；e915 的 6 秒片段終點 6.584。 | 她背對、下一鏡 s21 也是她的背影在前景：剪接時讓句尾 0.2 秒延到 s21 開頭（J-cut），不用多買；在剪接表註明。 |
| 16 | s23 | 系統 2.88＋心裡話 4.40＋句間 0.5＝7.78 秒，8 秒片段可用到 8.0，前後都沒有餘裕。 | 同上。 | 系統那句往前疊到 s22 尾巴（s22 a20 4.68 秒、片段約有 1.4 秒空），s23 只放心裡話；或句間縮到 0.3 秒。剪接表註明。 |
| 16 | s01 | 第 15 集 s42 有兩個家丁各扶橫木一端，本鏡家丁全沒了；s07 才又出現一隻灰袖的手。 | 接戲；script「這集接在哪」四個家丁。 | 加「at the left end of the log, one hand in a plain grey sleeve resting on it, the rest of that man out of the frame」，與 s07 同一句。 |
| 16 | s01 s05 s10 等 | 尾句樣板「after the last word … the brows stay drawn」套在眉頭本來是平的（s01 calm brows level）、驚訝揚眉（s05）、挑眉（s10）的臉上，前後矛盾；s01 唐小棠寫 tense brows drawn，storyboard 是中性臉。 | 拍法 14「每鏡寫表情」要一致；拍法 3 中性臉。 | 尾句照每鏡的臉寫：s01「after the last word his lips press flat and his brows stay level, eyes steady on the man」；s05「his brows stay lifted, lips pressed」；s10「his brows stay up, lips pressed, eyes on the old man」。s01 唐小棠改「composed: brows level, lips closed」。 |
| 16 | s11 | 唐小棠那張竹簾的尺寸句沿用「as wide as his shoulders」。 | 代名詞錯指（同第 2 條必改的道理）。 | 她那張改「as wide as her shoulders」。 |
| 16 | s31 | 俯拍插鏡沒說從桌子哪一邊看；s30 從書生那邊拍，黃紙在畫左；若模型從許硯這邊俯拍（他的右手拿筆最自然），黃白會左右對調。 | 接戲、拍法 9。 | 「seen from the street side of the table, his right hand reaching in from the top edge of the frame; the yellowish sheet on screen left and the white sheet on screen right」。 |
| 16 | s36 | 許硯臉朝畫左看馬車，同時樣板句說「turned toward the person he is speaking to」（她在畫右），兩個方向互相拉。 | 樣板句與構圖衝突。 | 說話句改「he speaks low out of the side of his mouth toward her on his right, his eyes staying on the carriage down the street at the left」。 |
| 16 | s41 | 「smoke rising and spreading into the red dawn sky」：渡口圖的紅霞在畫左地平線，村子與煙在畫右，煙上方是淡色天。 | 光源與參考圖一致。 | 「into the pale dawn sky above the village, the red glow low on the far left horizon」（重畫 l2 時也照這樣畫）。 |
| 16 | s34 | 三十個淡青長衫書生加送許硯兩張圖，人小時書生最容易借到他的臉。 | 第 9 集分身；同一人兩次。 | 「Xu Yan appears only once, behind the table in his grey outer coat; the scholars are other young men with round faces and black square caps」。 |
| 16 | s02 | 第一格許硯「standing at the front of the wheelbarrow」，要退回車把得繞過整台車，動作會很長或直接瞬移。 | 拍法 10、接戲。 | 「Xu Yan steps back along the side of the cart to its two handles and takes them in both hands」，並把他第一格寫在推車側邊靠前（s01 他也在車頭旁）。 |
| 16 | s13 | 秦霜「stops just behind Xu Yan」：接下來 s14 是從她背後過肩、許硯在畫左面對她；「behind him」會讓他背對她說話。 | 接戲、軸線。 | 「walks over and stops a step to his right, facing him」。 |
| 16 | s16 | 紙堆「lit from the front」同時夕陽「from the open right side across the stack」，兩個光向。 | 光源一致、拍法 17。 | 「the low sunset light from the open right side falls across the top of the stack, every sheet blank, thick and matte」。 |
| 16 | 竹筏 s18–s28、s39 | `set-zhufa-ye-l1` 是 CG 渲染（黑色粗管似的竹子、塑膠感），紙捆疊了四五層、比坐著的人還高；第 14–15 集工棚 l2 也偏 CG 而可用，所以不擋開拍。 | README 試鏡挑法；真人版質感。 | 有空時重畫 `set-zhufa-ye-l2`：真人質感、青黃色粗竹八根、紙捆兩捆壓低到膝高能坐、筏尾燈籠竿；同時存一張鏡像給 s39。 |
| 16 | 工棚 s09–s17 | 必改 4 是照圖改字；圖本身的攪棒與 A 字架仍會在 s10、s13、s14 跟竹簾、竹篙搶「長東西」。 | 第 14 集 s15、s30、s32。 | 有空畫 `set-gongpeng-l3`：拿掉桶裡交叉攪棒（留一根平放在遠桶沿）、左牆兩架改成掛著一排空白濕紙的低矮晾紙架。畫了就把必改 4 的場景句改回「drying frames hung with wet blank sheets」。 |
| 16 | s29 s32 s33 s37 | 第 15 集 fix1 的 s26、s41 兩支裡各有一支仍冒出第二個唐小棠背影；本集 11 支背影鏡，每鏡兩個種子，預期仍會有一半要挑掉。 | `e915-live/fix1/review-picks.tsv`。 | 書院這幾鏡人多，把書生寫成「every scholar wears pale blue-green and a black cap; nobody else wears pink」；預算上保留每鏡兩個種子，不要為省錢只跑一個。 |
