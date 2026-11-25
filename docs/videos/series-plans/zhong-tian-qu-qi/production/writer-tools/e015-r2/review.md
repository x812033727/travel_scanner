# 第 15 集重製版（e015-r2，內部編號 915，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-15，只讀（只寫本檔）；沒用 Colab、RunPod 或任何付費服務，沒有 git commit。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e015-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e015-r2/r2.py`、
  `colab/runs/e915/extras.json`、`colab/runs/e915-live/{mkspec.py, spec.json}`，以及完整試跑**實際要送出的**
  `…/scratchpad/dry915/zhong-tian-qu-qi-e915-dh/runpod/live/d1/colab-jobs.json`（84 支，s01–s42 × 種子 9151101／9151102）與 `prompts/ref-sNN-915110{1,2}.txt`
  （兩個種子的提示詞逐位元相同；extras 的替換都已套進去）。錄音：`/root/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/audio/zq915a01–a40.wav`，
  用 wave 讀長度、20 ms 能量包絡量開頭／結尾靜音與句中停頓。
- 對照：`r2-bible-e011-e020.md`（拍法 1–18、道具表、接點 14→15、15→16、場景表與格局）、`r2-bible-e011-e060.md`、`season-01.md` 第 15 集、
  `writer-tools/e01{2,3,4}-r2/review.md`、`colab/runs/e913-live/pick-review.md` 與 fix1／fix2、第 14 集 r2 s40–s42、
  `assets/refs-live/`（逐張看過 `set-gongpeng-ye-l1`、`set-gongpeng-l2`、`set-dagu-chang-l1`、`set-qiutian-l1`、`set-zhulin-fen-l3`、`set-shiqiao-l1`、
  `laisan-portrait-l1`、`hanbo-portrait-l1`；README 的第 2 篇章與第 13、14 集段落）。

## 總評

台詞與 script.md 一字不差；第 18 條（背景正面描述、不列否定名詞）、第 15 條（畫外句不補、不說話的人寫硬）、唐小棠八句全背影或插鏡、
spec.json 拿掉她的臉部圖與身分句、過肩前景不點名不送圖、長棍固定寫成素木長棍、紙空白正面打光，都照前三集審稿後的寫法做了。
軸線大致清楚（打穀場許硯左、秦霜右；田埂在右、犁往左；橋上許硯左、賴三右）。

問題集中在四處：
1. **三張場景圖跟文字打架**：夜工棚 l2 還沒畫，試跑 s01–s08 送的是舊 l1（地上格柵、左邊兩架長竿、桶裡交叉的攪棒），跟每鏡「地面空、什麼都沒靠」正面衝突；
   秋田圖整片已是一壟壟的犁溝，「還沒翻的稻茬」與「秦霜翻出泥浪」的對比拍不出來，而且是大白天藍天，拿去拍 s27–s30 的夕陽；
   石橋圖右前景的木板便橋（一根長板架在短樁上）跟要寫的「橫木架在兩個木架上」幾乎是同一個東西，而且就在賴三站的畫右。
2. **幾個軸線破口**：s24 秦霜跟 s23 的二牛同朝畫右；s41 唐小棠在右前景、賴三朝畫右看她，跟 s38、s40、s42 賴三一律朝畫左相反。
3. **句子自相矛盾**：工棚「柱子光禿、什麼都沒釘」緊接著「中間柱上釘一張紙」；竹簾「直立」又「濕紙平躺在上面」；s05 燭光「從左來」但蠟燭在右邊桌上；
   s09、s25、s31「每個人穿深色布鞋」但秦霜穿皮靴；九支沒有棍子的鏡也寫「大家手上唯一的長東西是素木長棍」；s16 寫了紙背後的炭筆線。
4. **第一格少了手與道具**：s18 許硯手上沒有圖、s40 賴三身前沒有橫木、s42 許硯在車把後面卻要接隔著橫木和整台車遞過來的紙。

必改 **19** 條、建議 **20** 條。
**參考圖：`set-gongpeng-ye-l2` 必須先畫好才開拍**（已有 `screen-test-e015.py`）；**`set-shiqiao-l1` 必須重畫成 l2**（拿掉木板便橋；石橋第一次用在本集，沒有舊鏡要對）；
**`set-qiutian-l1` 必須重畫成 l2**（平的、沒翻的稻茬田）。`set-zhulin-fen-l3` **不重畫**，用文字把右下那塊平放木板正面寫出來（必改第 18 條）。

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| 竹林的餘燼 | **可以留**。圖上墳前有火，照第 18 條寫成「一小片灰、幾點將熄的紅燼」是讓文字跟圖一致的最穩寫法；第 13 集秦霜在這座墳燒過紙，觀眾會讀成她之前來祭過。不要寫成火盆或火堆。真正的問題是右下那塊**平放木板沒寫**、而直立木牌又寫在同一位置（右前） | 必改 18、建議 15 |
| l3 右下平放木板 | 正面寫出來：「一塊平放在落葉上的舊木板」，木牌改寫在墳前正中、直立。近景 s33、s34 已不送圖，照舊 | 必改 18 |
| 夜工棚 l2 還沒畫 | **擋開拍**。pilot.py 拿最新 l 版，現在最新是 l1，試跑 8 鏡全送了 l1 | 必改 1 |
| 秋田圖已是一壟壟的田 | **重畫 l2**（平的稻茬田）。s27–s30 是翻完後的夕陽，用 drop_set 不送圖 | 必改 2 |
| 石橋右前景木板便橋 | **重畫 l2**。s40 近景不送圖 | 必改 3、建議 19 |
| 韓伯錄音偏慢 | a16 6.44 秒（18 字，約 3.1 字／秒）放 s15 的 8 秒沒問題，老人慢說合角色；a28 6.19 秒放 s29 的 6 秒**放不下**，說完沒有時間給「抿嘴、點頭」那一拍（笑多半出在那裡） | 必改 12、建議 1 |
| c03 只買 8 秒 | **可以**。兩句都是畫外（系統＋心裡話），a03 3.91＋a04 3.68，句頭句尾靜音剪掉約 0.4 秒、句間 0.3 秒，約 7.5 秒，面板疊在上面，尾巴必要時可蓋進 s04 開頭。10 秒的沉默臉只會漂 | 建議 2 |
| s18 二牛拋長棍 | 稿子要拋接，但「把比人高的棍子丟向一個人」最容易被畫成揮棍、刺擊，而秦霜右手已有一根、左手再接一根，兩根棍子要一路帶到 s24。改成**很短的一下遞拋**，秦霜兩手空著站在一步外接 | 必改 10 |
| s24 只露二牛的肩 | 肩可以，三張臉的規則守住了；但(1)軸線反了，(2)交棍要他的手在第一格裡 | 必改 11 |
| 賴三頭巾歪 | 定妝照是一條寬布帶纏得**很正**，頭頂一個髮髻、左耳後垂一截布頭。「pushed crooked」跟「keeps exactly the same hair and costume」打架，七鏡會時正時歪。照定妝照寫，油滑改用身體姿勢與表情 | 建議 18 |
| s02、s05 插鏡把唐小棠列進人物 | **不會長出臉**：她只在 chars 裡讓錄音不標畫外，提示詞沒有她的名字、沒有她的圖（只送工棚圖）。剩下的風險是尾巴兩句通用句「Facial expressions follow…」「every visible face acts…」在只有手的鏡叫模型去找臉，用 spec 換掉 | 建議 3 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 15 | s01–s08（參考圖） | **夜工棚 l2 沒畫，試跑送的是舊 `set-gongpeng-ye-l1`**（`colab-jobs.json` 8 支都是）。l1 地上一大片木格柵（本集主題正是竹簾，地上又一張）、最左兩架斜靠的長竿 A 字架、兩個桶裡插著交叉的攪棒；提示詞每鏡寫「floor plain packed earth, smooth and empty」「nothing leaning against them」，圖文正面衝突，長竿是 e911 長槍架的來源。 | `set-gongpeng-ye-l1.png`；`screen-test-e015.py` 說明；README 第 2 篇章重畫段（「地上還留一點格子影」）；pick-review（e913 s06 兩座兵器架）；bible 第 18 條。 | 開拍前跑 `screen-test-e015.py`（種子 37011／37012），挑一張存成 `refs-live/set-gongpeng-ye-l2.png` 再重跑 prep915；挑片時逐項確認：蠟燭在**右邊**舊木桌上（各鏡寫的光源方向依這張）、左牆光禿、兩桶紙漿面光滑、地面是素土。重跑後檢查 `colab-jobs.json` 的 s01–s08 都是 `set-gongpeng-ye-l2.png` 才送。 |
| 15 | s19–s30（參考圖 `set-qiutian-l1`） | **秋田圖整片已經是一壟壟隆起的犁溝**（稻茬長在壟頂），s19「犁頭只刮了一小條」、s20「只翻了一小條」、s25「泥浪一路翻過去」的前後對比拍不出來，本集奇觀全靠這個對比。另外圖是正午藍天，s27–s30 是夕陽，照圖會亮成白天（bible 第 8 條同理）。 | `set-qiutian-l1.png`；script.md c19–c30「收割完、還沒翻的稻茬田」；season-01 第 15 集奇觀；bible 第 8 條。 | 用 Qwen-Image-Edit 從 l1 改一張 `set-qiutian-l2`（s19–s26 用；石橋與秋田同一支 screen-test 跑）：`Same autumn field, same camera, same big willow with yellow leaves on the raised grass ridge along the right side, same low tiled farmhouses and blue hills far off, same warm slanting afternoon sunlight from the left. The whole field is flat and level: hard, dry, dark earth that has never been ploughed, short cut rice stubble standing in straight even rows on the flat ground, the soil between the rows flat, firm and finely cracked. Photorealistic photograph shot on a cinema camera.` s27、s29、s30 在 spec.json 加 `"drop_set": true`（背景已寫「only the long dark furrows and the gold sky」）；s28 也 drop_set，場景句保留全文。 |
| 15 | s36–s42（參考圖 `set-shiqiao-l1`） | **石橋圖右前景一座木板便橋**（長板架在短樁上、橫過水面），每鏡又照圖寫進「a low plank footbridge on short posts across the water at the right」，緊接著寫「one thick rough log … each end resting on a low wooden trestle」：兩樣都是「長木架在矮腳上」，又都在賴三站的畫右，模型很可能把便橋當成橫木、把賴三放到水上，或畫出兩道攔路木。圖上也沒有 bible 寫的「橋頭在右、橫木架在兩個木架上」；石板路沿左岸往遠處走，接不到拱橋的近端。石橋本集第一次用，重畫沒有舊鏡要對（l2 也會給第 16 集 s01）。 | `set-shiqiao-l1.png`；bible 場景表第 15 集「橋頭一根粗橫木架在兩個木架上；橋頭在右」；e913 院子井邊斜板長出槍架的教訓。 | 重畫 `set-shiqiao-l2`：`Same old grey stone arch bridge over the misty stream in the early morning, same bamboo on both banks, same tiled houses on the far bank, the low cold golden sun at the upper right. The camera stands on the near bank: the stone-paved path runs from the left foreground straight to the near foot of the arch bridge on the right of the middle, ending on a small flat stone landing at the foot of the bridge; one thick rough log lies across that landing, each end on a low wooden trestle. On the right beyond the landing only open misty water with round stones and green reeds along the bank. Photorealistic photograph shot on a cinema camera.` 各鏡場景句把「a low plank footbridge on short posts across the water at the right」換成 `open misty water with round stones and reeds along the bank at the right`。 |
| 15 | s01–s08（場景句） | 每鏡場景句都寫「the posts and the earthen walls bare, nothing mounted on them」，s01、s05 接著寫「one sheet of plain paper pinned flat to the middle timber post」：同一段裡說柱上什麼都沒有又說柱上釘一張紙，模型二選一，s05 的插鏡主體可能沒了。 | s01、s05 提示詞；接點 14→15「告示釘在棚柱上」；bible 道具表「行會告示」。 | 八鏡的場景句統一換成：`the posts and the earthen walls bare, the middle timber post carrying only one sheet of plain paper pinned flat with one wooden peg, thick and opaque, completely blank; nothing leaning against the walls`（s02、s08 看不到柱子也可照用，不衝突）。 |
| 15 | s01 | 竹簾寫成「standing upright in both his hands with one wet sheet … lying on it」：直立的簾子上「平躺」一張濕紙，物理上不成立；動作又要他把紙「揭下、平端著轉身」。e913 fix1：手與道具在第一格寫錯，動作句救不回來。 | s01 提示詞；r2.py docstring（第一格寫手與道具）。 | 構圖句改：`one papermaking mould … held level at waist height in both his hands, flat like a tray, with one wet sheet of fresh plain white paper the size of a book page, matte, thick and completely blank lying flat on it`；動作句改：`Xu Yan lifts one corner of the wet sheet with his fingertips and peels it off the flat mould, then turns toward the stack holding the sheet flat on both palms`。 |
| 15 | s05 | (1) 寫「warm candlelight from the left」，蠟燭在畫右的舊木桌上（l1／l2 都是），s01–s04 也寫燭在右，光向反了。(2) 插鏡的主體（柱上的紙）寫成「soft and out of focus」，是從 s01 背景搬來的；主體失焦，拍手這一下沒有對象。 | s05 提示詞；`set-gongpeng-ye-l1.png` 蠟燭位置；bible 第 10 條（插鏡第一格就是主體）。 | `warm candlelight from the right, from the candle stub on the table at the right`；那張紙改 `in sharp focus, filling the middle of the frame, thick and opaque, lit from the front by the candle, completely blank`。 |
| 15 | s09、s25、s31 | 尾巴的「Every person in the frame wears dark cloth shoes on both feet」跟同一段裡秦霜的「leather boots」衝突（s09、s25、s31 都有她）。模型要嘛把她的靴子改成布鞋，要嘛不信整句。 | 三支提示詞；cast／extras 秦霜造型句。 | 三鏡在 spec.json 用 replace 換成：`Qin Shuang wears her black leather boots and everyone else wears dark cloth shoes, on both feet.`（s25 只有她和遠處村民，同句可用）。 |
| 15 | s17、s19、s20、s21、s22、s23、s25、s26、s28 | 這九鏡**沒有人拿棍子**，卻都寫「the only long things anyone holds are plain wooden staffs, smooth and round to both ends」：等於告訴模型「有人拿著棍子」。s19、s20、s26、s28 的村民、s21 的二牛會長出棍子；s21、s22、s25 的曲轅犁（彎轅、犁把）也是「長東西」，跟句子矛盾。第 18 條：寫在場的東西，不寫會引出東西的句子。 | 九支提示詞；bible 第 18 條；e913 pick-review。 | 這九鏡拿掉 STICKS 句，改寫每雙手：s19、s20 `the three men's hands on the ropes across their chests, the onlookers' hands empty at their sides`；s21 `their hands on the plough on their shoulders, nothing else in their hands`；s22、s25 `only the plough in the frame, nothing else in anyone's hands`；s23 `in his hands only the hemp rope harness`；s26 `the villagers' hands empty at their sides`；s28 `the villagers' hands empty`；s17 `Elder Han's right hand on his bamboo walking staff, Erniu's left arm holding his staff in its crook`（見建議 9）。 |
| 15 | s16 | 「its blank back toward us, lit from the front, the charcoal strokes on its far side」：寫了背面的線條，紙會透出筆畫（bible 第 17 條：不寫透出、不寫背後的字或圖）。 | s16 提示詞；bible 第 17 條紙的寫法；storyboard s16「不寫透出線條」。 | 換成：`its back toward us, plain and blank, thick and opaque, lit from the front, nothing showing through it`。 |
| 15 | s18 | (1) **第一格許硯手上沒有圖**（構圖句只寫他的臉與站位），動作卻是「把捲好的圖塞進二牛左手」——e913 fix1：只寫在動作句常被忽略。(2) 二牛把比人高的棍子「underhand」拋給幾步外的秦霜，最容易被畫成揮擊或刺向她；(3) 秦霜右手已有一根自己的棍子又用左手接一根，兩根要帶到 s24，s24 只交一根給二牛、s25 又要兩手空空。 | s18 提示詞；script c18「棍子往秦霜那邊一丟、秦霜伸手接住」；bible 第 5、17 條；e913 fix1。 | 構圖句加 `the rolled sheet in Xu Yan's right hand, held out toward Erniu at chest height`；秦霜改 `one step behind Erniu on screen right, her hands empty, her right hand open at her side`；動作句改 `Erniu nods once, swings his staff upright and gives it a short easy toss across the one step to Qin Shuang, who catches it upright in both hands, and he turns and runs off toward screen left`。這樣她到 s24 只拿二牛那一根，交還後兩手空。 |
| 15 | s24 | **軸線反了**：s23 二牛朝畫右對畫外的秦霜說；s24 秦霜也朝畫右對畫右緣的二牛說——兩人同朝一邊。照 s23，秦霜在二牛的右邊，s24 她要朝畫左看、二牛的肩在畫左緣；她接著「越過他往畫左的犁走」也才通。另外交棍要他的手，構圖句只有肩；棍子在胸以上的中近景「held out toward screen right」對著一個人，像刺。 | s23、s24 提示詞；animation-camera 軸線；e014 審稿 s20–s25 同類必改；e913 fix1。 | 構圖句改：`… one plain wooden staff, smooth and round to both ends, held upright in her right hand, her face three-quarter to screen left toward the young man there, never the lens; … at the left edge of the frame, soft and out of focus, only the broad shoulder of one young man in a coarse brown jacket and his open right hand reaching in at chest height, his face out of the frame`；動作句改 `Qin Shuang sets the upright staff into the young man's open hand at the left edge, rolls her sleeves up to the elbows with two quick tugs and steps past him toward the plough off screen left`。mkspec 的 s24 replace 把 "right edge" 改 "left edge"。 |
| 15 | s29（錄音） | a28 6.19 秒（開頭 0.22、結尾 0.36 秒靜音，句中 0.42、0.58 秒停頓）放買 6 秒的鏡：照 storyboard 自己的「錄音＋0.5 秒」要 6.7 秒，放不下；r2.py 的「(6−0.3)×1.1＝6.27」只差 0.08 秒，說完之後的「抿嘴、慢慢點頭」完全沒有時間——第 18 條要說完最後一個字也寫一個動作佔住，因為笑多半在句尾冒出來，這鏡偏偏是「眼眶發亮」的韓伯。 | 錄音量測；bible 第 18 條；storyboard「剪接以錄音長度＋0.5 秒為準」。 | 擇一，建議第一種：(a) a28 開頭與結尾靜音各剪到 0.1 秒（約 5.75 秒），竹杖第一格已放在地上，構圖句改 `his polished old bamboo walking staff lying on the earth beside him`、動作句刪「lays his bamboo walking staff down beside him」，台詞從第一秒內開口，6 秒剛好容下說完後約 0.5 秒的點頭；(b) 改買 8 秒，動作句寫 `after the last word he presses his lips together, his eyes still on the sky, and nods slowly twice to the last frame`。 |
| 15 | s36 | 「the servants take one step forward; Lai San lifts one hand to stop them」：「them」接在家丁後面，變成賴三攔**自己的家丁**；稿子是他抬手攔許硯與推車。 | s36 提示詞；script c36「賴三抬手攔」。 | 換成：`the four servants behind him take one step forward; Lai San lifts his right hand, palm out toward the cart, and shouts`。 |
| 15 | s39 | 構圖句寫許硯「just let go of the cart's handles」，動作句又寫「sets the cart's handles down, steps up to the log」：第一格已經放開了，後面再放一次。script c39 第一格是兩手還搭在車把上。 | s39 提示詞；script c39。 | 構圖句改 `both his hands still on the cart's two handles`，背景改 `behind him only the stone-paved path and the mist`（推車在他身前，不在身後）；動作句保留 `sets the handles down, steps round the cart up to the log and stops in front of it`。 |
| 15 | s40 | 動作「pats the log twice with his palm」，但構圖句裡**沒有橫木**（低角度近景只寫胸以上與霧）；第一格沒有的東西動作句叫不出來。 | s40 提示詞；e913 fix1。 | 構圖句加 `his left forearm resting on the top of the thick rough log barrier across the bottom of the frame`；動作句改 `pats the log twice with his left palm`。 |
| 15 | s41 | **軸線破口**：唐小棠在**右**前景、賴三朝**畫右**看她；s38、s40、s42 賴三一律朝畫左（許硯、唐小棠、推車在左），s39 從賴三背後拍也是他在右、許硯在左。s41 照現在寫等於跳到線的另一邊，剪起來賴三忽左忽右。 | s38–s42 提示詞；animation-camera 軸線；bible 第 9 條。 | 構圖句改：`… her face turned fully away, the small gold abacus hanging at her waist, standing in the left foreground, her right hand (on screen right) at the small gold abacus at her waist; facing us a few steps away, a little right of the middle, behind the thick log barrier, Lai San …, his face three-quarter to screen left toward her, his eyes on her face just left of the lens, never the lens`；動作不變。 |
| 15 | s42 | 許硯寫在「behind the cart … both hands on the cart's handles」，賴三卻要把紙「across the log … stops in front of him」：獨輪車從車把到車頭一公尺多，中間還隔著橫木，手伸不到；模型會把推車縮小或讓賴三越過橫木，或乾脆讓許硯接下（第 15→16 接點要他還沒接）。 | s42 提示詞；script c42；接點 15→16（下一集第一鏡許硯才把紙塞回去）。 | 改站位（台詞不動）：`on screen left at the front of the cart, close to the log, Xu Yan, …, his left hand resting on the oilcloth bundle on the cart, his right hand at his side, framed from the waist up …`；動作句改 `… holds it out across the log and stops it a hand's width in front of Xu Yan's chest; Xu Yan keeps his left hand on the bundle and his right hand at his side, his eyes lift from the slip to Lai San's face and narrow`（不用「does not take it」）。 |
| 15 | s31、s32、s35（竹林圖） | 圖上墳的右前方地上**平放一塊舊木板**，提示詞完全沒寫（第 18 條要正面寫出圖上的東西）；反而在**同一個位置**（at its right front）寫一塊直立木牌——模型要把那塊平木板立起來，或平的、立的各一塊。s32 秦霜要跪在木牌前、手搭在牌頂，牌的位置不穩，整鏡構圖跟著漂。 | `set-zhulin-fen-l3.png`；README 第 14 集段「右下仍有一塊平放木板」；bible 場景表「墳前一塊空白木牌」；bible 第 18 條。 | 三鏡的場景句改成：`a small low earthen grave mound, one short weathered blank plank standing upright in the earth at the front of the mound in its middle, its face bare grey wood; one old flat wooden board lying on the fallen leaves to the right of the mound; and a small patch of grey ash on the bare earth in front of the upright plank with a few last dull red embers in it …`；s32 構圖句的「in front of the small blank plank at the grave mound」不變。 |
| 15 | s01–s08、s19–s30、s36–s42（重跑） | 以上三張圖（工棚 l2、秋田 l2、石橋 l2）都換好之後，現在的 dry915 試跑全部作廢，要用新圖重跑 prep915 與 preflight，再逐支看 `colab-jobs.json` 送的場景圖。 | pilot.py `live_picture` 取最新 l 版。 | 重跑後確認：s01–s08 → `set-gongpeng-ye-l2.png`；s19–s26 → `set-qiutian-l2.png`；s27–s30 沒有場景圖；s36–s39、s41、s42 → `set-shiqiao-l2.png`。 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 15 | s15（錄音） | a16 句中「冬麥再種不下去，」後停 0.62 秒，8 秒放得下，但韓伯臉上要靜止撐過這段。 | 錄音量測；e014 a06／a10 的做法。 | 跟 a22、a28 一樣剪到 0.4 秒（約 6.2 秒）；不必重錄，老人慢說合角色。 |
| 15 | s03（錄音） | 8 秒放 a03＋a04（7.59 秒）偏緊。 | 錄音量測。 | 剪 a04 開頭 0.26 秒靜音、兩句間留 0.3 秒；兩句都是畫外，尾巴可蓋進 s04。不要改回 10 秒。 |
| 15 | s02、s05、s08 | 只有手的插鏡仍帶通用句「Facial expressions follow the action and lines … the pictures fix the face …」與「each person keeps the identity … every visible face acts the emotion …」，叫模型去找一張臉。唐小棠本身不會長臉（沒有名字、沒有圖）。 | s02、s05 提示詞；mkspec.py。 | spec.json 把這兩句換成：`Only hands move in this shot; the frame stays on the paper and the hands from the first frame to the last.` |
| 15 | s04 | 廢紙堆寫在「beside his right hand」，動作卻用左手撿紙、右手拿炭條；他朝畫右站，右手在身體遠側。 | s04 提示詞。 | `on the vat's rim in front of him a small loose heap of torn scrap paper, every piece blank, and beside it one short black stick of charcoal`。 |
| 15 | s07 | 「lays her head sideways on top of the stack … her cheek resting on it with her face turned … toward the stack」：側躺一定露出半張臉或側面，從背後稍高處拍正好看到。 | s07 提示詞；bible 第 3 條（第 8 集背影鏡）。 | `folds both arms on top of the stack and lays her forehead down on her arms, her face hidden in her peach-pink sleeves, the back of her head and her two buns toward us`；a09 句中 0.78 秒（哈欠）可剪到 0.5 秒，5.6 秒。 |
| 15 | s13 | 主觀看「場外的稻茬田」，送的是打穀場圖（前景一大片磚地與稻草垛，遠處田是黃、橘條紋），稻茬近看長不對。 | s13 提示詞；`set-dagu-chang-l1.png`。 | 秋田 l2 畫好後，s13 改送 `set-qiutian-l2`（spec 無法換圖時，在 r2.py 的 loc 改成秋田那一套場景句、留「the foreground only the edge of the threshing ground」）。 |
| 15 | s14 | 構圖句「staff … lowered with its end on the ground」，動作句又「Erniu lowers his staff」。 | s14 提示詞。 | 構圖句改 `one plain wooden staff … held upright in his right hand`。 |
| 15 | s15 | 構圖句已把韓伯放在二牛身邊（「coming to a stop beside the young man」），動作又要他走進來、跟拍；第一格與動作打架，常變成原地踏步。 | s15 提示詞；e913 fix1。 | 構圖句改 `Elder Han a few steps behind and to the right of Wang Erniu, walking toward him, his bamboo walking staff in his right hand`；動作句 `walks up beside Erniu, stops and taps the staff twice`。 |
| 15 | s17 | 紙「held up by hands off screen」從畫左伸進來，沒手的紙常浮在空中；二牛的長棍不知去向（s14、s15 在手上、s18 又在右手）。 | s17 提示詞；道具連戲。 | `one sheet of paper held up into the frame from the left edge by one hand in a blue-grey sleeve tied back with a cloth strip`；二牛 `his staff held in the crook of his left arm`。 |
| 15 | s18 | 8 秒裡五拍（交圖、點頭、拋、接、轉身跑），剪在轉身跑一半。 | r2.py BUY 註解。 | 照必改第 10 條簡化後不變；挑片時優先看拋接那一下有沒有變成揮棍。 |
| 15 | s22 | a22 5.57 秒放 6 秒鏡，動作卻有敲兩下、繞犁走半圈、說完哼一聲三拍，走半圈時臉轉開、嘴型對不上，哼那一拍也擠不下。 | s22 提示詞；錄音量測；bible 第 18 條。 | 刪「walks half a circle round the plough」，改 `knocks his fist twice on the curved beam and leans in to squint along it`；a22 開頭 0.24、結尾 0.36 秒靜音剪到 0.1 秒（約 5.1 秒）。 |
| 15 | s26 | 唐小棠身邊抓袖子的村民寫成「standing small and soft」，他就在前景、不可能小。 | s26 提示詞。 | `her left hand gripping the sleeve of the village man just left of her, only his shoulder and arm in the frame, his head cut off by the top of the frame`；其餘村民 `further along the ridge, small and soft`。 |
| 15 | s27 | 光從左來、她臉朝畫右，卻寫「the low sun on her face」。 | s27 提示詞；光向一致。 | `the low sun from the left rimming her cheek and ponytail in gold`。 |
| 15 | s30 | 夕陽從左來，秦霜在左、臉朝右，兩人都逆光；可以，但要寫明，否則模型補正面光。 | s30 提示詞。 | 加 `the low sun behind Qin Shuang on the left, a gold rim on her hair and shoulders, Xu Yan's face warm in its light`。 |
| 15 | s31、s35 | s31 秦霜在左、許硯在右後一步「走進空地」＝兩人往畫左走；s35 兩人「往畫左的出路」離開，等於繼續往深處走，不是原路回家。 | s31、s35 提示詞。 | s31 改成從深處往鏡頭走：`walking toward us along the narrow earth path from the back of the clearing, Qin Shuang a step ahead on screen left`；s35 的出路寫 `the path out of the clearing on screen left`（不變）。或 s35 改往畫右離開。餘燼照現在寫，不寫火、不寫盆。 |
| 15 | s33 | 構圖句已「crouched down low」，動作又「crouches down beside her」。 | s33 提示詞。 | 構圖句改 `bending down, about to crouch`。 |
| 15 | s36 | 四個家丁的臉沒寫大小，畫面裡已有三張有名字的臉，家丁臉清楚會像多出四個人搶戲，也會被當成同一張臉的分身。 | s36 提示詞；bible 第 1 條。 | `four servants … standing in a row behind him, small and soft, their faces shadowed under their head-wraps`。 |
| 15 | s36–s42 | 賴三「old cloth head wrap pushed crooked to one side」跟定妝照（寬布帶纏得很正、頂上髮髻、左耳後垂一截布頭）衝突，七鏡會時正時歪。 | `laisan-portrait-l1.png`；每鏡「keeps exactly the same face, hair and costume」。 | 各鏡換成 `his wide grey-brown cloth band wound round his forehead below his small topknot, its tied end hanging behind his left ear`；s39 背影 `the back of his head with a small topknot above a wide grey-brown cloth band`。油滑交給 `slouching, one shoulder dropped, eyes sliding sideways`。 |
| 15 | s40 | 低角度近景，背景只要霧與橋石，卻送石橋圖（現在的圖會帶進木板便橋）。 | e913 院子圖教訓；s33、s34 同做法。 | spec.json 的 s40 加 `"drop_set": true`。 |
| 15 | s09 | 十二個年輕人都看得到臉、二牛在其中一排，三張參考圖臉之外又一群同齡男子，第 8 集有過二牛分身。 | bible 第 1 條、e908 分身。 | 年輕人加 `faces small and soft in the low sun, shadowed under their head-wraps`，二牛那句加 `the only one in the front row facing the lens side`。 |

## 逐鏡核過、沒有問題的部分

- 劇情：照 script.md c01–c42；跟 season-01 細綱的差異（秋耕冬麥取代春耕、賴三代錢員外出面、唐小棠不拍告示改成第 14 集已帶來的釘柱告示）都是 r2 稿已定的改動，接點 14→15、15→16 對得上（除必改第 17 條 s42 的站位）。
- 一鏡最多三張有名字的臉：s09、s18、s36、s42 各三張；s19 田埂上的人移走；s24、s39 前景不點名不送圖。
- 說話與不說話：s01、s03、s04、s15、s17、s18、s21、s25、s30、s31、s35、s36、s37、s41、s42 不說話的人都寫了「says nothing … no mouthing words」；畫外句沒有補。
- 紙：s01、s02、s04、s06、s08、s09、s10、s42 都寫空白、正面打光（s16 見必改第 9 條）；s08 犁圖只有幾筆線、其餘空白。
- 光向：打穀場低光從左（圖上影子往右前，對）、竹林星光加墳前低暖光（對）、石橋冷金光從右（圖上太陽在右上，對）；工棚除 s05 外都對。
- 兵器：整集沒有刀；秦霜腰帶每鏡寫空；長棍與竹杖寫成素木。
- 秒數：除 s29（必改第 12 條）、s22（建議）外，其餘錄音＋0.5 秒都放得下買的秒數；s13 買 5 秒放 a14 3.64 秒可以。
