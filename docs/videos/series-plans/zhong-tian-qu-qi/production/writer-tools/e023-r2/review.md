# 第 23 集重製版 r2（e923）真人版：開拍前獨立審稿

- 審稿日期 2026-11-16。審稿者沒參與寫稿，也沒用 Colab、RunPod 或任何付費服務。只寫了這一份檔，沒改別的檔；試做的調色與裁切圖只放在 scratchpad，看完就刪了。
- 審的對象：`docs/videos/zhong-tian-qu-qi-e023-r2/{script.md,storyboard.md,video.json,overlays.json}`、`writer-tools/e023-r2/r2.py`、`colab/runs/e923/extras.json`、`colab/runs/e923-live/{mkspec.py,spec.json}`、`hailuo/clips-dh-e923.json`（精修用的文字），以及實際要送的 `~/mokaair-work/videos/zhong-tian-qu-qi-e923-dh/runpod/live/d1/colab-jobs.json`（82 支）與 `prompts/`。
- 對照了這些：`r2-bible-e021-e030.md`（拍法 1–30，第 20 條已更正成長金算盤；接點 22→23、23→24；道具表；場景盤點）、`r2-bible-e011-e060.md`、season-01 第 23 集、`writer-tools/e022-r2/review.md`、`colab/runs/e921-live/` 與 `e922-live/` 的兩份挑片表、任務檔第 15–20 集的教訓、第 22 集 r2 的 s39–s41。
- 參考圖都放大看過：`set-chuan-ye-l1`、`set-chuan-ye-wu-l1`、`set-chuan-chen-l1`、`set-chuan-chen-wu-l1`、`set-dukou-ye-l1`、`set-dukou-ye-shui-l1`、`set-kezhan-pm-l1`、`set-kezhan-pm-table-l1`、`prop-jinsuanpan-l1`，人物圖 `xuyan-portrait-l1`、`tangxiaotang-portrait-l1`、`weishaoqing-portrait-l1`。四張霧色或桌面圖另外量了平均 RGB，跟母圖比過。
- 錄音：faster-whisper medium 重聽了 a37（現在用的版本，也聽了加速以前的 raw-tts）、a32、a29（整句一次，再切出有問題的那幾個字聽一次）。一次只跑一支，跑完就結束；先用 ffmpeg 轉成 16 kHz f32le raw，再用 numpy 讀成陣列餵進去；兩條執行緒。另外用 silencedetect（-35 dB）與每 50 毫秒的 volumedetect 量了 a09、a10、a14、a18、a19、a23、a26、a28、a29、a31、a32、a34、a35、a36。
- 也跑了 `storyboard-check.py script.md`（40 鏡、199.5 秒，沒有錯誤）與 `preflight-prompts.py colab-jobs.json`（0 錯 0 警告）。

## 先確認的事（都對）

| 項目 | 結果 |
| --- | --- |
| d1 提示詞的分隔句 | 82 支裡，每支的 `never the mood. ` 與 `One continuous shot.` 都剛好一次 |
| clips-dh 的分隔句 | 41 鏡，每鏡的 `the set layout stays as it is. ` 都剛好一次；三支算盤插鏡 s11、s15、s25 沒有這一句，改用 `keeps the first frame's set layout and props. `，也剛好一次。不送人的 s02、s06、s21、s35、s39 兩句都有，這跟第 22 集一樣，`refine-prep.py` 會優先用標準那句，沒問題 |
| 兩個種子 | 每鏡 9231101 與 9231102 兩支的提示詞逐位元相同；`prompt_sha256` 跟檔案相符 |
| 參考圖路徑 | 全部是絕對路徑，檔案都在；`swap_pictures` 已經套上（retake.json 裡的 `set-dukou-l2` 在 colab-jobs.json 已換成 `set-dukou-ye-l1`） |
| 唐小棠不露嘴（拍法 3） | 她的 14 句台詞所在的鏡都沒送她的圖、也沒有身分句；臉只在 s19、s37、s40，送 l1 與 angle-a，三鏡都寫了不說話 |
| 一鏡送幾張圖 | 最多是 s37 的 6 張，在 Ref2VA 九張的上限內 |
| 一鏡最多三張臉 | 沒有超過的。s37 是魏、唐、許三張臉，三老在後面虛焦、側面；s40 是唐、許兩張臉加魏少卿的手 |
| 摺扇 | 15 個出現扇子的地方都是合著的（寫成 `its dark bamboo ribs pressed tight together`），沒有開扇的寫法 |
| 算盤 | 只在 s11、s15、s25 三支插鏡出現，送 `prop-jinsuanpan-l1`，寫前臂長的長金算盤，平放在桃粉百褶裙上（第 22 集 s19 用同樣寫法，挑片時畫對了）；中景以上的唐小棠都沒寫算盤 |
| 夜戲的光 | 只有稿子寫的光：岸邊插著的一盞燈籠、船頭竹竿上一盞燈，s12 半邊臉被船頭燈照亮；沒寫月光；天亮以後燈都沒點 |
| 否定名詞、會長字的東西 | 除了固定的「不說話」句與片尾的乾淨畫面句，沒有否定名詞；沒有 book、ledger、letter、scroll、sign、calligraphy、curtain、candle、moon 這類字 |
| 秒數 | 照 r2.py 的算法（一支片能裝 (買的秒數 − 0.3) × 1.1 秒的人聲），只有 s20 不夠，見必改 7；其他鏡都裝得下。s16 a14 的人聲 5.66 秒、s28 a26 的人聲 5.02 秒（檔案 6.00 秒，後面 0.7 秒是靜音）、s37 a35 的人聲 5.58 秒，都在 6.27 秒以內；s13 是 a09 的 2.13 秒加 a10 的 2.74 秒再加 0.5 秒，共 5.37 秒，6 秒裝得下 |
| 軸線 | 渡口：棧橋在左、船在右，許硯往畫右追，跟第 22 集 s39–s41 一樣。船上：許硯在左、唐小棠在右，許硯的說話鏡都看畫右，過肩鏡她在右前景。客棧：魏少卿在左（窗下長凳）、唐小棠在右，許硯在她畫右肩後（s29、s34、s37、s40 都一樣）。沒有越軸 |
| 接點 | s01 接 22→23（燈籠插在泥裡、他已在水裡，跳下水交給音效）；s40 交給 23→24（拇指按在賭約上、三老在旁、唐許在桌對面，紅框由剪接疊上） |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 23 | 參考圖 `set-chuan-ye-wu-l1`（s03、s05、s06、s08–s10、s12–s14、s16–s18，共 13 鏡 26 支） | 這張霧色底圖比母圖亮很多，也青很多。平均 RGB 是 44/109/143，母圖 `set-chuan-ye-l1` 是 35/71/93。看起來是偏藍的黃昏或水底，不像子夜濃霧。夜裡的近鏡會跟 s04、s07 兩個全景接不上；s05 他泡在水裡，背景又是整片亮青色，很容易畫成水下 | 第 22 集挑片 s39、s40「天色偏藍黃昏，不是深夜」；拍法 8（夜就是夜）；送的場景圖會壓過文字（拍法 19、29） | 免費重做同一個 id（還沒拍過任何一支，換掉不影響重建）：`ffmpeg -i set-chuan-ye-l1.png -vf "crop=384:216:0:0,scale=1312:736:flags=lanczos,eq=saturation=0.55:gamma=0.75" set-chuan-ye-wu-l1.png`。試算後平均 RGB 是 34/73/88，跟母圖一樣暗、一樣灰藍。README 第 3 篇章那一行的命令也要跟著改。提示詞不用動 |
| 23 | s03（也套用到 s04） | 他「水到大腿」，畫面卻是「胸口以上」，還寫「兩手往上伸到船舷」。照比例，小船的船舷在他腰的高度，要往上伸手搆船舷，水就得淹到胸口，模型會畫成泡到胸口或在游泳。另外，她跪在船舷邊往外探、要往下看他，提示詞卻寫她 `facing left toward the stern`，等於臉朝船尾，跟往下看水裡的他對不上 | 拍法 23（每鏡同一個水位，不游泳）；分鏡表 s03 | s03 把他那一句換成：`below her on the left, facing us, Xu Yan, ... standing in the river beside the boat, framed from the waist up, the boat's low wooden edge at the height of his waist and both his hands flat on it, the flat dark water around his thighs just below the edge, his face tilted up to her, three-quarter to screen right, never the lens`；她那一句的 `facing left toward the stern` 改成 `kneeling at the boat's side, leaning out over the edge and looking down at him`。s04 的 `framed from the chest up, both hands gripping the wooden edge` 改成 `framed from the waist up, standing in the river with the boat's low wooden edge at his waist and both hands gripping it, the dark water around his thighs` |
| 23 | s05 | 地點句一開頭就寫 `On a small boat ... under its arched canopy`，可是畫面上只有他一個人，而且人在水裡。只送一張全是霧色的底圖，又是胸口以上，最可能拍出來的是他坐在篷下，或者水淹到下巴、像在游泳。這是寫稿者最擔心的那一鏡 | 拍法 23；分鏡表 s05「泡在船邊水裡」 | 地點句改成 `In the dark river water beside one small boat off the ferry landing of Liuxi at midnight, thick cold grey-blue fog all around:`；構圖改成從她的高度往下拍的中景，這樣看得到水位：`high-angle medium shot looking down from the boat's edge at Xu Yan, framed from his thighs up, standing in the river with the flat dark water around his thighs, the boat's low dark wooden edge across the lower right corner at the height of his waist, his left hand on it, his right hand already reaching up toward the upper right edge from the first frame, his face tilted up three-quarter to screen right toward Tang Xiaotang off screen above the right edge, never the lens`。後面那句 `the warm glow of the one bow lantern stay unchanged` 改成 `the thick cold grey fog and the one far warm glow on the shore stay unchanged`（見建議 9） |
| 23 | s07 | 構圖寫 `wide shot from the stern end of the boat`，送的 `set-chuan-ye-l1` 卻是從側面拍、船頭在右，兩者矛盾；模型多半照圖拍側面。從側面拍時，她 `facing away toward the bow` 等於臉朝畫右，觀眾會看到她的側臉，而她的台詞 a04 正在這一鏡播出 | 拍法 3；拍法 29（照場景圖改站位）；第 21、22 集挑片「背影露出側頰，落選」 | `wide side-on shot of the boat as in the set picture, its bow and lantern on the right, a dark wet stretch of the near side of the boat in the soft foreground`；她那一段改成 `on the right under the canopy, an arm's length from him, one young woman seen only from behind, ..., sitting with her arms around her drawn-up knees, turned away from us toward the far side of the boat and the fog beyond it`；`she sits stiffly facing the bow the whole shot` 改成 `she sits stiffly turned away from us the whole shot` |
| 23 | s17、s22、s27 | 三支都是「從背後拍」的唐小棠說話鏡，提示詞卻寫她面朝右邊：s17 是 `facing out over the side toward the dark water on the right`，s22 是 `facing ahead downstream toward the right`。從背後拍又面朝右，就是側背，會露出耳朵與臉頰。s27 的船夫寫成 `seen only from behind, standing side-on`，前後矛盾 | 拍法 3；第 21、22 集挑片的落選原因大多是「露側頰」 | s17：`facing straight away from us toward the dark water beyond the far edge of the boat`。s22：`facing straight away from us, downstream, the bright glittering water ahead of her filling the frame`。s27：`beyond her at the very prow one boatman ..., standing with his back to us, his wide hat brim hiding his face, both hands on one long bamboo pole` |
| 23 | s18 | 構圖寫許硯 `stunned: eyes wide, lips parted and still`，動作段又寫 `his lips stay pressed together from the first frame to the last`，兩句互相矛盾。嘴是張開的，模型就容易讓他對嘴，而這一鏡是她從背後說的台詞 a16 | 第 22 集 s09 重拍：她背後的台詞被畫成對面的人在說；拍法 14 | `stunned: eyes wide, brows up, lips pressed together and still` |
| 23 | s20 | a18 檔長 6.12 秒、人聲 5.62 秒，要整支 6 秒、而且放慢 1.1 倍才勉強裝得下（6.27 秒）。可是背影鏡在挑片時幾乎都要剪掉開頭 0.5–1.25 秒（她轉頭露臉、或從畫外擠進來），剪掉之後就放不下了；下一鏡 s21 也是 5.92 秒的畫外句，沒有空間讓這句延到 s21 | `r2.py` 的 BUY 算法；第 21、22 集挑片的剪點（s01 1.25、s04 0.5、s34 0.75–1.0 秒） | `BUY = {"s20": 8, "s40": 8}`（多 2 支 × 2 秒）。分鏡表與 storyboard 的長鏡說明一起改 |
| 23 | s28 | 許硯不送圖、背對鏡頭，可是只有他沒有「頭不動」那一句（只在動作段跟大家一起寫了 `all with their backs to us`）。他一回頭就是一張陌生的臉。另外，三老在跟拍的鏡頭裡一個接一個走進門，畫面上有六個人在動，加上魏少卿一共六個人，模型很容易多長一個人或讓人分身 | 拍法 2、25；第 22 集挑片「兩個唐小棠」；第 15 集「四隻手＝兩個許硯」 | 他那一段改成 `one step behind her and half hidden by her, his back to us, one young man ...; the young man keeps his head still, the back of his head toward us the whole shot`；三老改成已經站在門內：`behind them, just inside the door at the right edge, three thin old men ..., standing together, soft and out of focus, their backs to us`；動作段改成 `the young woman and the young man walk on toward the table, and the three old men stay by the door, all with their backs to us` |
| 23 | s29 | 三老只寫了 `soft and out of focus`，沒寫面朝哪邊。他們站在屏風邊，位置在魏少卿後面、正對著唐小棠，最自然的拍法就是正臉朝鏡頭；這樣畫面上會變成許、魏加三老共五張臉 | 拍法 1、25（三老不給正臉）；s37、s40 都有寫 `seen side-on` | `far behind by the folding screen three thin old men in long silk robes, standing side-on to us and turned toward Wei Shaoqing, their faces in profile, soft and out of focus` |
| 23 | s31、s36 | s29 是同一個過肩機位，許硯站在畫右邊緣、她的右肩後；到了 s31、s36，同一個機位卻寫 `exactly two people`，許硯不見了。s34、s37、s40 他又在原位，等於中間消失兩鏡 | 接戲；分鏡表〈客棧〉「許硯在她右肩後」 | 兩鏡都照 s29 加上他，也送 `xuyan-portrait-l1` 與 `angles/xuyan-angle-a-l1`（臉是許、魏兩張，加她的背影）：`standing close at her right shoulder, on the right edge of the frame, Xu Yan, in an old plain grey cloth outer coat worn open over his faded blue-grey scholar's robe, his robe dry and creased, framed from the waist up, his face three-quarter to screen left toward Wei Shaoqing, never the lens; tense: jaw set, lips pressed shut`。人數句改成 `exactly three people: the young woman seen only from behind, Xu Yan at her shoulder and Wei Shaoqing beyond the table`，動作段加上 `Xu Yan says nothing in this shot: his lips stay pressed together from the first frame to the last` |
| 23 | s29、s31、s36、s37、s40（賭約） | 賭約只寫了 `one sheet of plain paper folded in half`，沒寫哪一面朝上，也沒寫紙的質地。第 22 集 s30–s32 寫成 plain 的紙仍然長出一行行假字或透出字影，其中 s32 必須重拍。s37 的紙還放在前景最靠近鏡頭的桌緣，面積最大 | 拍法 7、17、27；第 22 集 s30、s31、s32 挑片 | 每一處都統一寫成：`one sheet of thick smooth cream paper folded in half, its blank outside facing up, smooth and empty`。s37 另外加 `lying soft and out of focus at the very bottom edge of the frame`。s40 寫 `its thumb pressed down on one sheet of thick smooth cream paper, its blank outside facing up`。s39 原本的 `with its plain blank side up` 可以保留 |

必改一共 11 條，牽涉 15 鏡、1 張參考圖。

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 23 | 參考圖 `set-chuan-chen-wu-l1`（s20、s22–s24、s26、s27） | 這張是中性灰（平均 156/158/162），提示詞卻每鏡都寫 `lit warm gold from the right`；s19、s21 用的母圖是金色日出（上方平均 172/156/144），近鏡會比全景冷，看起來像陰天 | 拍法 29；光源跟參考圖一致 | 免費調暖、同一個 id 重做：`crop=352:198:0:0,scale=1312:736:flags=lanczos,colorbalance=rm=0.10:bm=-0.10:rh=0.10:bh=-0.12`，試算後平均是 174/158/141，跟母圖上方一致（看過，左灰褐、右淡金）。README 那一行一起改 |
| 23 | 霧色底圖的近鏡（s08、s09、s12、s13、s13b、s16、s23、s26） | 寫稿者問：底圖幾乎是單色，近鏡會不會太空、竹篷會不會畫錯。我的判斷：夜霧裡淺景深的近鏡，背景本來就是一片霧，單色反而對；危險在文字一直提竹篷。地點句寫 `under its arched canopy of dark woven bamboo`，s09、s10、s14、s18 又寫 `behind him the dark woven canopy`，圖上沒有竹篷，模型只能自己編，可能編成傘或帳篷，也可能把畫面拉回全景 | 送的圖是霧（第 21 集教訓：夜戲不送場景圖會長出夜市攤子，所以底圖要送）；參考圖壓過文字 | 近鏡與過肩鏡的背景一律只寫霧：`behind him only the thick grey fog, soft`。地點句換成 `On a small boat out on the water off the ferry landing of Liuxi at midnight, thick cold grey-blue fog all around:`（拿掉 `under its arched canopy...`）；要交代他在篷下，就只寫頭上一根竹骨：`one curved rib of dark bamboo just above his head at the top edge of the frame` |
| 23 | 船上 10 支背影與過肩鏡（s03、s07、s10、s14、s17、s18、s20、s22、s24、s27） | 寫稿者問：會不會單調、轉頭露臉的風險多大。單調：s10、s14、s18、s24 是同一個腰以上的過肩構圖，連著出現 4 次。露臉：每一支都寫她 `facing left toward the stern`，她的頭得往左轉才看得到他，耳朵與臉頰的風險就在這裡。第 21、22 集的經驗是每支都可能要剪掉開頭 0.5–1 秒 | 第 21、22 集挑片；拍法 3 | 只改景別，不加動作：s14 改成過肩近景（`over-the-shoulder close shot, the back of her head and her right shoulder filling the right third of the frame`）；s24 改成從船板高度往上的低角度過肩；s10、s18、s20 維持原樣。過肩鏡的許硯位置改成 `facing us beyond her, a little left of the middle`（客棧過肩鏡就是這樣寫，她不必轉頭），她那句改成 `facing into the frame toward him` |
| 23 | s21 | 寫稿者問：兩個小人加一個船夫，會不會長出第二個桃粉色的人。全景裡人很小，提示詞也寫了 `exactly three people, all small in the frame`，風險不大；分身多半發生在近一點的過肩鏡（第 22 集 s09）。可以再加一句保險 | 第 22 集 s41 的同類全景（三個小人）沒有分身 | 加：`her small peach-pink figure is the only spot of pink anywhere in the picture, sitting close at his right side under the canopy` |
| 23 | s28 等客棧鏡 | 寫稿者問：圖上窗外是灰白的陰天，稿子卻寫晴天斜陽。現在的寫法 `a bright pale sky beyond it` 加 `warm afternoon light from the bright window` 跟圖一致，也不會長出光束，這樣就對了。`clear winter afternoon` 這幾個字可能會讓模型畫出藍天，跟圖打架 | `refs-live/README.md`：`set-kezhan-pm-l1` 窗外仍是陰天；拍法 29 | 保留，只把 `on a clear winter afternoon` 改成 `on a bright winter afternoon`。要晴天的感覺，剪接時把整場調暖一點；不要寫光束或太陽 |
| 23 | s30、s32、s38（魏少卿近鏡，不送場景圖） | 背景只靠一句 `behind him the bright window`。第 22 集不送圖的近鏡曾經長出雜物牆或灶間 | 第 22 集 s30 挑片 | 可選、免費：從 `set-kezhan-pm-l1` 裁出窗與屋瓦 `crop=544:306:0:40,scale=1312:736:flags=lanczos`，新 id 叫 `set-kezhan-pm-chuang-l1`（看過：簷口、灰瓦屋頂、木格窗扇，沒有字），用 swap_pictures 加給這三鏡。不做也可以，第 22 集的魏少卿近鏡大多過了 |
| 23 | s36 | a34 檔長 5.48 秒、人聲 5.20 秒，6 秒裝得下。可是這是背影鏡，開頭剪掉 0.75 秒以上就不夠了 | 同必改 7 | 挑片時如果每支都要剪頭超過 0.6 秒，就把 s36 改成買 8 秒重拍；不必先買 |
| 23 | s01 | 船寫成 `already ten metres out`。第 22 集 s41 最後挑定的那支，船離棧橋只有兩三公尺；模型本來就傾向把船畫近 | 第 22 集 s41 挑片（「船太近」） | 寫 `already a few boat lengths out` 比較接得上，也比較畫得出來 |
| 23 | 近鏡與插鏡的光句（s03、s05、s06、s08–s10、s12–s14、s16–s18） | 船頭燈不在畫面裡的鏡，每支片尾都寫 `the warm glow of the one bow lantern stay unchanged`。寫了燈，模型就容易把燈畫進近鏡的背景；第 22 集夜裡沒送圖的近鏡長出過串燈與蠟燭。s05 還同時寫了岸邊燈籠與船頭燈兩個光源 | 第 22 集 s16、s21、s23 挑片；拍法 18 | 畫面裡看不到燈的鏡，改成 `the thick cold grey fog and the faint warm light on one side of his face stay unchanged`；畫面裡有燈的 s04、s07 照舊 |
| 23 | 近鏡的濕衣句（s09、s12、s13、s16、s23、s26 等胸口以上的鏡） | `his robe and coat soaked dark from the thighs down and clinging to his legs` 寫的是畫面外的腿；寫了腿，模型可能把畫面拉遠去畫它 | 只寫畫面裡看得到的東西 | 胸口以上的鏡改成 `his coat sleeves dark and damp, his wet black hair stuck to his forehead`（s19 以後寫 `his coat sleeves dry, his hair still a little damp`） |
| 23 | s08 | 他看畫右外的船頭，船夫卻在畫面右後方虛焦，視線落點有兩個 | 視線要明確 | `his face three-quarter to screen right toward the boatman soft in the background on the right` |
| 23 | s19 | 構圖寫 `from the stern end of the boat`，送的天亮船圖卻是側面拍的，跟 s07 同樣的矛盾（這一鏡她可以露臉，所以只算建議） | 拍法 29 | `medium wide side-on shot under the canopy, as in the set picture, the bow on the right` |
| 23 | s30 | 胸口以上的近鏡，卻寫他用扇子在膝上敲兩下，膝蓋在畫面外 | 道具與手寫在畫面內 | `tapping the closed fan twice against his open left palm at chest height` |
| 23 | s34 | 他臉朝畫左，伸的卻是右手，要越過身體才搆得到她，容易畫成手臂交叉 | 手的位置寫清楚 | `reaches his left hand out toward her arm` |
| 23 | 唐小棠的緞帶（s19、s37、s40 對其他背影鏡） | 定妝照 l1 與 angle-a 的緞帶都長長垂到胸前，背影鏡寫短緞帶纏在髻上，露臉的三鏡會照圖畫成長的 | 第 20–22 集都接受過 | 接受，挑片時看就好，不要為這個去花錢改圖 |

## 錄音（寫稿者問的三句）

| 句 | 鏡 | 聽到什麼 | 判斷 |
| --- | --- | --- | --- |
| a37「叮。強制任務：鬥商三十日，勝出。」 | s40 | 加速以前的 raw-tts：「鬥傷 30 日」（鬥 0.93，傷跟商同音），念對了。加速 1.3 倍、加電子音以後：「右上 30 日」，「鬥商」兩個字擠在 2.04–2.32 秒，只有 0.28 秒，「鬥」的聲母被吃掉 | 留用。面板在同一刻疊出「強制任務：鬥商三十日，勝出」，觀眾看得到字。想更清楚的話，可以免費把 raw-tts 這一句單獨用 1.2 倍重做後製再聽寫一次比較，但系統聲音的速度要跟全季一致，不必強求 |
| a32「小棠，三十天，魏記背後是整個宰相府。」 | s34 | 整句與只切出「三十天」那段，聽寫都多出一個「內」（機率 0.38–0.46）。逐 50 毫秒量音量：「天」在 1.70 秒還有 -19 dB，1.75 秒降到 -30 dB，1.80–2.26 秒都在 -44 dB 以下 | 沒有多一個字。那段只是「天」的鼻音尾巴加上停頓，聽寫是被「三十天內」這個常見說法帶出來的幻覺。留用 |
| a29「…鬥商三十日，比營收。」 | s31 | 兩次錄音不給提示都聽成「鼻音收」（比→鼻、營→音，-ng 收成 -n、第三聲聽成第二聲），給上下文就聽對 | 留用。台灣口音的 -ng 與聲調本來就這樣，前文是「鬥商三十日」，聽得懂；這是背影鏡，不用對嘴，字幕也會打出「比營收」。重錄也很難改掉這個口音 |

## 參考圖要不要動（都是免費做法）

- **要做（必改 1）**：`set-chuan-ye-wu-l1` 同一個 id 重做，加 `eq=saturation=0.55:gamma=0.75`。
- **建議做**：`set-chuan-chen-wu-l1` 同一個 id 重做，加 `colorbalance=rm=0.10:bm=-0.10:rh=0.10:bh=-0.12`。
- **可選**：新 id `set-kezhan-pm-chuang-l1`（窗與屋瓦的裁切），給 s30、s32、s38。
- 不用動：`set-dukou-ye-l1`（沒有船、沒有岸，岸與泥寫在鏡頭裡就好）、`set-dukou-ye-shui-l1`（棧橋底下、蘆葦、黑水，偏軟但只用在 2 秒的腳）、`set-kezhan-pm-table-l1`（茶壺在正中，插鏡寫的是桌緣與手，可以接受）、`prop-jinsuanpan-l1`（底下的深色櫃子已經用 `the pleated peach-pink silk skirt fills the rest of the frame` 壓住，第 22 集 s19 證明有效）、三張人物圖。
- 不需要新的試鏡，也不需要付費的編輯。

## 最重要的五條

1. **夜霧底圖太亮太青**（必改 1）：一張圖影響 26 支片，免費調色就能修，修完跟夜裡的全景接得上，也不會被拍成偏藍黃昏或水底。
2. **水位與構圖**（必改 2、3）：s03、s04、s05 的水是到大腿，取景卻是胸口以上，s05 的地點句還寫他在船上。改成腰或大腿以上取景，讓船舷在他腰的高度、看得到水位；s05 改成從她的位置往下拍。
3. **背影鏡的方向**（必改 4、5）：s07、s17、s22、s27 寫她面朝右、朝船頭，或寫船夫側身，從背後拍就會露出側臉或臉頰。一律改成 `turned away from us` 或 `facing straight away from us`。
4. **客棧的人**（必改 8、9、10）：s28 的許硯要寫頭不動，三老改成已經站在門口；s29 的三老改成側面；s31、s36 把許硯加回她的右肩後。
5. **賭約與 s20 的秒數**（必改 11、7）：所有賭約統一寫 `thick smooth cream paper folded in half, its blank outside facing up, smooth and empty`；s20 改買 8 秒，留出剪掉開頭的空間。
