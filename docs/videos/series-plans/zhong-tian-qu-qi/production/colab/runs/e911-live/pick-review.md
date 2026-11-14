# e911-live 挑片後、精修前的獨立審查（第 11 集真人版）

- 審查者：沒有參與製作的獨立代理，2026-11-14。只寫這份檔，沒有改任何專案檔，沒有用 Colab、RunPod 或任何付費服務。
- 這是 `_scripts/independent-review.md` 的第一次審查（挑片後、精修前）。還沒有成片，所以 cut-qa、cut-jumps、audio-qa 與音效量測都跳過；遞婚書（s06、s07）、攤紙（s18、s19）、搭肩（s24）、揪袖（s16）、拍手臂（s31）的鏡仍然逐格看過。
- 對照：
  - 稿子：`docs/videos/zhong-tian-qu-qi-e011-r2/script.md`（以〈真人版的改動（2026-11-14）〉與〈2026-11-14 獨立審稿後的修改〉為準）、`storyboard.md`（真人版每鏡的畫面）；`writer-tools/e011-r2/review.md`；`r2-bible-e011-e020.md`。真人版要點：唐小棠台詞鏡（s06、s14）只拍背後、頭不轉；兵器都不拍（秦霜不帶柴刀、阿令不露匕首、趙捕頭腰間只有黑布帶、衙役只拿火把）；紙上沒有字（s18、s19 是空白紅紙加一方空的朱紅印框）；畫外句（s04、s12、s23、s24、s28、s29）畫面上的人整鏡閉嘴；過肩前景不點名、頭整個轉開；交領角色不翻轉。
  - 選定的草稿：`/root/mokaair-work/videos/_live-e911/zhong-tian-qu-qi-e911-dh/runpod/a/st1/out/sNN.mp4`，960×544，24 fps。35 支逐支比對過 md5，跟 `picks.json` 的 `draft` 都是同一支（s02 s09 s13 s14 s16 s18 是 fix1，其餘 d1）。
  - 剪點：`/root/mokaair-work/videos/_live-e911/zhong-tian-qu-qi-e911-dh/picks.json`。
  - 挑片表：`picks-merged.tsv`、`fix1/review-picks.tsv`、`review-picks-a.tsv`、`review-picks-b.tsv`；重拍規格 `fix1/spec.json`（s02 s09 s13 s14 s16 s18）。
  - 備用草稿：`/root/mokaair-work/videos/zhong-tian-qu-qi-e911-dh/runpod/live/{d1,fix1}/out/`。
  - 參考圖：`production/assets/refs-live/`（`huxianling-portrait-l1`、`zhaobutou-portrait-l1`、`aling-portrait-l1`、`qinshuang-portrait-l1`、`tangxiaotang-portrait-l1`、`xuyan-portrait-l1`、`set-xujia-yuan-ye-l1`）。
  - 第 10 集最後一鏡：`/root/mokaair-work/videos/_live-e910/zhong-tian-qu-qi-e910-dh/clips/s40-t1.mp4`（1312×736，5.8 秒）。
- 做法：
  - 每鏡整支每 0.5 秒抽一格做總表（`sheet-sNN.jpg`）。
  - 嘴與笑的逐 0.25 秒放大：`mouth-s06.jpg`、`mouth-s13.jpg`、`mouth-s14.jpg`、`mouth-s16.jpg`、`mouth-s21.jpg`、`mouth-s25.jpg`、`mouth-s27.jpg`、`mouth-s30.jpg`。
  - 全格放大：s05（`z-s05-6.5.jpg`、`z-s05-face.jpg`、`z-s05-torch.jpg`）、s08、s09（`z-s09-2.0.jpg`、`z-s09-6.5.jpg`、`z-s09-7.5.jpg`）、s13（`z-s13-4.0.jpg`、`z-s13-belt.jpg`）、s14（`z-s14-1.0.jpg`、`z-s14-5.0.jpg`、`z-s14-wall.jpg`、`z-s14-spears-l.jpg`）、s16（`z-s16-0.5.jpg`、`z-s16-2.0.jpg`）、s19（`z-s19-4.5.jpg`、`track-s19.jpg`）、s22（`z-s22-1.0.jpg`、`z-s22-3.5.jpg`、`z-s22-plaque.jpg`）、s30、s31、s32、s35、s01、s03、s07（`z-s07-red.jpg`）、s10（`z-s10-plaque.jpg`）、`z-quad1.jpg`（s15、s23、s26、s25）。
  - 接第 10 集：`join-e910s40-s01.jpg`、`sheet-e910-s40.jpg`；參考圖並排 `refs-people.jpg`、`refs-set.jpg`。
  - 試做局部處理：`try-spears.jpg`（s16、s13、s14 的槍架壓暗，採用）、`try-more.jpg`（s31 槍、s22 匾、s32 槍，s22 採用、s31 可選、s32 不建議）。
  - 抽格與放大圖都在 `/tmp/claude-0/-home-user/e6a64eea-98ea-5986-b96b-5cdbc5d1572e/scratchpad/e911/pick-review/`。
- 秒數一律是草稿原片的秒數（有 `start@` 的鏡沒有扣掉）。座標用 960×544 草稿像素，寫成 `寬:高:x:y`。
- 挑片表已經寫過、這裡確認還在的問題標「已知」。

## 先講結論

- **嚴重**：
  1. **s21、s25：`picks.json` 的剪點抄成了另一支種子的退路剪點**（新）。挑片表定的是 s21 用 1101 `end-before@4.2`、s25 用 1102 `start@4.6 end-before@9.5`；`picks.json` 的種子對，剪點卻是落選那支的（s21 寫了 1102 的 `start@2.6 end-before@4.8`，s25 寫了 1101 的 `start@0.4 end-before@5.6`）。結果：
     - s21：4.25–4.75 秒胡縣令咧嘴露齒笑進了片（`mouth-s21.jpg`），台詞是結巴推卸，笑場。
     - s25：0.4–5.6 秒這段 2.0–3.25 秒他仰頭大笑、張大嘴，甩袖到 5.0 秒才來；挑片表選的 4.6–9.5 才有甩袖接拖長音說話。
     - **修法（不花錢）**：改剪點（見文末 TSV）：s21 `end-before@4.0`（4.25 秒起就笑，比挑片表的 4.2 再收 0.2）；s25 `start@4.6 end-before@9.5`。s27 同一個毛病（寫了 1101 的 2.0），但 2.0 比 2.4 更好（2.0 秒起畫右冒出一支插地的火把架），維持 2.0。
  2. **s13、s14、s16：背景紅纓長槍架**（已知，判斷能處理）。s13 畫左上、s14 畫左上加畫右屋牆、s16 畫左上整排（另畫中一支、畫右門邊一支），刃與紅纓都清楚，農家院子裡出現槍架也說不通。三支都試做過羽化框局部壓暗加模糊（`try-spears.jpg`），刃和紅纓消失、只剩看不清的暗杆，框邊看不出來。**不用重拍**，剪接時照下面的 vf 套。s09 選中的 fix1 1202 我沒找到槍架（只有斜靠的竹竿），不用處理。
- **中等**：
  3. **s13：0–2.4 秒胡縣令笑著張嘴**（新）。台詞是惱羞成怒的「胡說八道！本官就是王法」，前 2.4 秒是笑臉，2.5 秒起才變驚怒、3.5 秒往畫左戳手指。**修法**：`start@2.6`（剩 5.4 秒，這句約 4.6 秒）。
  4. **s14：5.5 秒起胡縣令嘴角上揚**（已知 5.7，放大後提早）。`picks.json` 的 `end-before@5.8` 包進了 5.5–5.75 的笑意。**修法**：`end-before@5.4`，唐小棠這句約 5.8 秒，剪接時本鏡放慢約 1.07 倍（`slow_max` 1.1 以內）或讓句尾 0.4 秒蓋到 s15 開頭。唐小棠 4.0–5.4 秒臉頰與耳朵側面出來一點（頭微轉），看不到嘴，接受。
  5. **s30：7.25 秒起許硯嘴角上揚**（新）。`picks.json` 取 B 的 7.5，挑片表定的是 A 的 6.6。**修法**：`end-before@7.0`（0.8–7.0 共 6.2 秒，這句約 5.6 秒）；2.5–3.0 秒還有一點笑意，輕微，接受。
  6. **s17：剪點太短**（新）。`picks.json` 寫 5.6，挑片表 5.8；0.4–5.6 只有 5.2 秒，趙捕頭這句約 5.3 秒，「有……」後還要停半拍。6.5 秒前沒有笑（`mouth-s17.jpg` 的眼神）。**修法**：`end-before@5.8`。
  7. **s18 與 s19：印對不上**（新）。fix1 為了擋閃粒把 s18 寫成「只拍紙背、不畫印框」，結果插鏡是一張全素的紅紙；s19 緊接著高舉的那份右下角卻有一方朱紅印（裡面有細小類字筆畫，約 30×35 像素，已知）。稿子 c18 的戲就是讓觀眾看到「前天蓋的印」（← c17），現在插鏡看不到印、下一鏡才冒出來。**處理**：接受（s19 的印讀得出來，故事不斷）；若站主要 s18 有印，**可選重拍**（英文改寫見中等 7）。s19 的印跟著紙大幅移動（x 約 570→730，`track-s19.jpg`），局部模糊要逐格追，不建議。
  8. **s32、s35：許硯直視鏡頭**（已知）。稿子是「眼睛盯著畫右鏡外一點」，兩支都正對鏡頭看。耳語戲裡直視觀眾有點破第四面牆，但讀得成「定住不動、不看縣令」，下一集接「直起身、正眼看胡縣令」也不衝突。另一支 1102 都更糟（s32 縣令站錯位、s35 許硯轉眼看縣令）。**接受**；若站主在意本集最後一格，**可選重拍 s35**（英文改寫見中等 8）。
  9. **s05：鏡頭沒朝院門、縣令官帽不明顯**（已知加新）。房子在畫右、看不到院門（已知）；胡縣令的帽子在 6.5 秒看起來是沒有展角的褐黑高帽（`z-s05-face.jpg`，兩側只有很淡的暗影），臉跟定妝照像同一人。火把十一、二支、人數比稿子多（已知）。火把頭纏一圈白布，上面有一道深色橫紋（`z-s05-torch.jpg`，像第 10 集 s32 的白塊，這裡看不出字形），輕微。**接受**；`end-before@7.5` 保留 6.7 秒往畫左一甩（挑片表寫可以）。
  10. **s22：屋牆上的匾有類字筆畫**（新）。窗左那塊深色匾（夜院參考圖本來就有）在 s22 裡三行亮點像字（`z-s22-plaque.jpg`，約 35×50 像素）。**修法**：局部模糊（vf 見下，`try-more.jpg` 已試做）。s10 那塊在虛焦裡、看不出字，接受。
  11. **s26、s15：笑**（已知）。s26 胡縣令整段笑著說「冒名頂替騙婚」（稿子是陰陰地說），兩支種子都一樣；s15 秦霜 2.0–3.5 秒笑開露齒（稿子只准嘴角一勾）。接受。
  12. **s08、s30：過肩前景的胡縣令露出耳朵與臉頰**，帽子是黑色幞頭加兩條長垂帶，背影像披髮（已知）。讀得出是縣令（藍綠袍），接受。
- **建議重拍**：
  - 沒有非重拍不可的鏡（嚴重的都能用剪點與局部處理解決）。
  - 可選 **s18**（中等 7）：補一方空的朱紅印框。
  - 可選 **s35**（中等 8）：眼神改看畫右鏡外。
- **每場的結尾**：
  - 第一場（s23）讀得懂：屋門前左秦霜（木棍）、中唐小棠（抱算盤、臉色緊）、右阿令走過來站定，三人嘴閉著、不笑；許硯這句畫外放錄音。秦霜沒有明顯「拉唐小棠」、阿令沒揉手臂（已知），接受。
  - 第二場（s35）讀得懂：許硯胸以上、右拳握三份紅紙，胡縣令在他左肩後（畫右）湊近說完；許硯嘴閉著、眉頭壓下。直視鏡頭見中等 8。
- **接第 10 集**：第 10 集 s40 末格是許硯張臂擋在院門、左後屋門口站著白衣阿令、衙役舉火把湧來；本集 s01（3.4 秒起）切到阿令站在暗屋格柵前、半邊臉被畫左一支火把照亮，3.6 秒黑袖手抓住她右臂（`join-e910s40-s01.jpg`）。同一刻、夜、同一套白衣，接得上。她嘴角有一點點上揚（輕微），被扯的幅度小（已知）。s02 接著從院子裡朝院門拍許硯背影，跟第 10 集 s40 他擋在院門一致。

## 一、嚴重

1. **s21、s25 剪點抄錯**（新）
   - 挑片表（`picks-merged.tsv`）：
     - s21：「取 1101 end-before@4.2；退路 1102 start@2.6 end-before@4.8」。
     - s25：「取 1102，剪點用 B 建議的 4.6–9.5；退路 1101 start@0.4 end-before@5.6」。
   - `picks.json`：s21 `seed 9111101`＋`start 2.6 end-before 4.8`；s25 `seed 9111102`＋`start 0.4 end-before 5.6`。種子是選定的那支，剪點是落選那支的退路。
   - 畫面：
     - s21（1101，`mouth-s21.jpg`）：0–4.0 秒眼睛撐圓、嘴半張結巴（對）；4.25 秒起咧嘴露齒笑，到片尾一直笑。抄錯的 2.6–4.8 包進了 4.25–4.75。
     - s25（1102，`mouth-s25.jpg`）：2.0–3.25 秒仰頭張大嘴大笑；5.0–5.75 甩袖、說話；7.25–7.75、9.0–9.75 說話。0.4–5.6 這段以大笑為主，甩袖剛出來就切掉。
   - **修法**：改剪點（文末 TSV）。s21 `end-before@4.0`（4.0 秒，這句約 4.1 秒；放慢 1.03 倍或句尾蓋到 s22）。s25 `start@4.6 end-before@9.5`。兩鏡都沒有扶正官帽（已知）。
   - 背景（s25）：左右兩個衙役腰間斜掛帶鞘的刀（已知，小、在背景），接受；要處理可局部壓暗，但兩人會走動，不建議。

2. **s13、s14、s16 的槍架**（已知；判斷：可以接受到「看不出是槍」，用局部處理）
   - 稿子：兵器都不拍；衙役只拿火把。許家院子不會有槍架。
   - 畫面：
     - s13（fix1 1202，`z-s13-4.0.jpg`）：畫左上三支紅纓長槍，刃在 x 0–110、y 50–170，杆斜到 y 420；整支都在。
     - s14（fix1 1202，`z-s14-1.0.jpg`）：畫左上三支（x 0–140、y 90–330，5.0 秒後被唐小棠擋住）；畫右屋牆三支（1.0 秒 x 820–900、y 130–300，推鏡後 5.0 秒移到 x 860–950，`z-s14-wall.jpg`）。
     - s16（fix1 1202，`z-s16-0.5.jpg`）：畫左上一整排六、七支（x 30–200、y 50–170 是刃與紅纓）；畫中兩人頭之間一支（x 485–530、y 155–235）；畫右門邊一支（x 840–860、y 175–250）。
   - 裁切不行：s13 胡縣令 3.5–5.5 秒往畫左戳的手指到 x 約 150；s16 胡縣令的帽翅在 x 145 起；s14 畫右的槍緊貼縣令的帽翅。
   - **修法（不花錢，已試做 `try-spears.jpg`）**：羽化 25 像素的框，壓暗、去飽和、模糊。框邊看不出來，紅纓與刃都消失，只剩幾條暗杆（讀成竹竿）。帽翅本來就是黑的，壓到也看不出。
     ```
     s13：split[a][b];[b]crop=190:180:0:30,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=0:30
     s14：split[a][b];[b]crop=150:250:0:85,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=0:85,split[a2][b2];[b2]crop=150:175:810:115,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c2];[a2][c2]overlay=810:115
     s16：split[a][b];[b]crop=210:150:0:35,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=0:35
     ```
     - s14 畫右框會壓到 5.0 秒縣令右側帽翅（黑的，看不出），框下緣停在 y 290，不壓到火盆的火。
     - s16 畫中那支緊貼趙捕頭的鼻樑、畫右那支很細，框會壓到臉，**接受**不處理。
     - 精修放大（SeedVR2）若在這之後做，座標乘上放大倍數；建議先精修、再在剪接時套。
   - s13 另有一點（**不確定**）：趙捕頭鑲金屬片的腰帶上吊一個金環，下面一根暗色斜杆往畫右下出畫（`z-s13-belt.jpg`），像刀鞘的掛環；黑對黑、在腰以下，觀眾多半看不到。接受。

## 二、中等

3. **s13 笑**：見結論。`start@2.6`。

4. **s14 笑**：見結論。`end-before@5.4`，本鏡放慢約 1.07 倍。

5. **s30 笑**：見結論。`end-before@7.0`。

6. **s17 剪點**：見結論。`end-before@5.8`。

7. **s18 與 s19 的印**（新，**可選重拍 s18**）
   - 稿子：c18 插鏡，兩手攤開一份紅紙、右下角一方空的朱紅印框；c19 舉高，印框朝畫右。
   - 畫面：
     - s18（fix1 1202）：整張素紅紙，另兩份夾在右邊，沒有印、沒有字、沒有閃粒（fix1 修好的部分都對）。
     - s19（d1 1101，`z-s19-4.5.jpg`）：右下一方朱紅印，框裡有類字的細筆畫（已知），紙面朝鏡頭。
   - 接受的理由：s19 的印很小、讀成蓋過的印，台詞「縣衙蓋印配的婚」跟得上。
   - **重拍 s18**（送不送圖照 fix1：不送人物圖、不送 `set-xujia-yuan-ye-l1`；不寫透光、不寫印框反光）：
     > Insert close-up, slow push in. From the very first frame two hands in faded blue-grey cuffs under old grey cloth sleeves hold open one sheet of plain matte red paper toward the camera; the other two folded red papers are pinched against its back by the left thumb. The sheet is blank: no characters, no writing, no pattern anywhere. Near its lower right corner there is one small square outline printed in flat dull vermilion ink, the square completely empty inside, just a thin plain frame, flat ink with no shine, no gold, no glow and no sparkle. Soft warm light falls on the front of the paper; no light shines through it. The background is dark and softly out of focus, no fire bowls, no flames, no braziers in the frame. Only the hands, the cuffs and the red paper are in the frame, no face. The two hands smooth the sheet flat and lift it a little; the paper stays flat matte red with no specks. No strings of beads, no hanging beads and no glitch effects anywhere.
   - 不重拍的話，s18 照 `picks.json` 整支用。

8. **s32、s35 直視鏡頭**（已知，**可選重拍 s35**）
   - 畫面：s32（2.8–7.5）、s35（1.8–6.2）許硯臉正對鏡頭、眼珠也正對（`z-s32-5.0.jpg`、`z-s35-4.0.jpg`）。站位對：胡縣令在畫右、他左肩後、手攏嘴邊。
   - 背景：s35 畫右兩個衙役腰間帶鞘的刀（已知）；s32 畫左遠處衙役手上一支紅纓長槍、畫右門邊一支、腰間有刀（已知）。都虛焦，接受。s32 試過壓暗畫左（`try-more.jpg`），推鏡時會把一個衙役壓成一團黑影，不建議。
   - **重拍 s35**（送 `xuyan-portrait-l1`、`huxianling-portrait-l1`、`set-xujia-yuan-ye-l1`；照 r2.py 不送許硯側面角度圖）：
     > Medium close-up on the night yard of the Xu farmhouse, deep night, the sky black, slow push in. Xu Yan, a young man in an old plain grey cloth outer coat over a faded blue-grey scholar's robe, black topknot tied with a cloth band, framed from the chest up, his body almost facing us but his head turned slightly to screen RIGHT and his eyes fixed on a point just off the right edge of the frame, never looking into the lens and never at the man beside him; his own right fist in the lower left of the frame grips three folded red papers, only their plain blank backs toward us, his knuckles whitening; his brows press down, his lips stay closed, no smile. Magistrate Hu, plump, in a black futou hat with two long flat wings and a blue-green robe, stands half a step behind Xu Yan's left shoulder on screen right, leans in with his face in profile to screen left, one hand cupped by his mouth, and slowly whispers into Xu Yan's left ear, his lips moving. Behind them, soft and out of focus, the dark yard and a few torches each held up in a person's hand; nobody in the background carries a spear, a sword or a scabbard. No smile at any moment.

9. **s05**：見結論。接受。

10. **s22 匾上的類字筆畫**（新）
    - 位置：1.0 秒 x 95–130、y 140–195；3.5 秒 x 78–112、y 138–190。
    - **修法**（已試做，`try-more.jpg`）：
      ```
      split[a][b];[b]crop=80:85:65:122,boxblur=6,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/15)'[c];[a][c]overlay=65:122
      ```
    - s22 其他（已知）：胡縣令的高帽沒有展角；兩個衙役沒鬆開阿令、沒退到右邊；火把九、十支；許硯手上的紅紙在全景裡像一朵紅花。接受。

11. **s26、s15 笑**：見結論。接受。

12. **s08、s30 過肩前景**：見結論。接受。

## 三、兵器、紙、道具（逐鏡）

| 鏡 | 人 | 看到的 | 處理 |
| --- | --- | --- | --- |
| s01 | 阿令 | 兩手空、袖蓋腕，沒有刃光 | 對 |
| s04 | 阿令 | 左手抬到右袖口再放下（0.5–2.0 秒），沒有匕首 | 對 |
| s13 | 趙捕頭 | 鑲金屬片腰帶、吊金環，下面一根暗杆（**不確定**是否刀鞘）；背景槍架 | 槍架壓暗（嚴重 2）；腰間接受 |
| s14 | 背景 | 畫左、畫右槍架 | 壓暗（嚴重 2） |
| s16 | 趙捕頭、背景 | 腰帶白片，沒看到刀；畫左槍架、畫中一支、畫右一支 | 畫左壓暗（嚴重 2）；另兩支接受 |
| s17 | 趙捕頭 | 腰不入鏡，手在胸前比劃，沒按布帶（已知） | 接受 |
| s15、s23、s27、s29、s34 | 秦霜 | 右手木棍、黑護腕，腰帶沒刀 | 對 |
| s25 | 衙役 | 左右兩人腰間帶鞘的刀 | 接受 |
| s26 | 衙役 | 灰藍短衣、腰間刀，籬笆邊兩三支紅纓槍 | 接受（小、虛焦） |
| s31 | 衙役、背景 | 畫左衙役腰間刀柄；畫右門邊一支紅纓槍（2.0 秒起，x 810–835、y 130–500） | 可選壓暗：`crop=80:420:785:100` 同上式（`try-more.jpg`，會變成一根暗柱，讀成木柱）；不做就接受 |
| s32 | 衙役、背景 | 畫左遠處一支紅纓槍、腰刀；畫右門邊一支 | 接受 |
| s35 | 衙役 | 畫右兩人腰間帶鞘的刀 | 接受 |
| s05、s22 | 衙役 | 只看到火把；s05 有一根斜靠的竹竿 | 對 |

- 判斷：衙役腰間帶鞘的刀全集零星（s25、s26、s31、s32、s35），都在背景、沒有人拔刀，同第 10 集的處理接受。槍架只有 s13、s14、s16 是清楚的前中景，用局部壓暗處理；不建議為了槍架重拍（fix1 已經重拍過一次，兩個種子都有槍架，再拍很可能還在）。
- 紙：s07 三份摺起、無字；s09 fix1 紅紙無字（fix1 修好）；s10、s20、s30、s32、s35 都是紙背或摺著、無字；s18 素紅紙無印（中等 7）；s19 有印與細筆畫（中等 7）。
- 算盤：s02、s06（夾在左肘）、s23、s27、s29、s34 都是素木算盤，沒有雕花。
- 錢員外（s24）：胖手、金戒指、深金團花袖口、一般膚色，臉不入鏡，對；1.4–6.8 秒胡縣令嘴閉著，對。
- 錢袋：s12 0–3.5 秒右手按左袖，對；s21 沒有抓袖（已知）。

## 四、人、字、閃粒、故障特效、嘴

- **分身、多出來的人**：選中的 35 支都沒有分身。s07 的「畫右多一隻空手」在 3.7 秒（`end-before@3.4` 已剪掉）。s02 4.3 秒左緣多一個人（`end-before@2.8` 已剪掉）。s24 背景一個紫紅衣、拿火把的人（已知），接受。
- **字**：s22 匾（中等 10，局部模糊）；s10 同一塊匾在虛焦裡，接受；s19 印框筆畫（中等 7）；s07 背景一排暗紅條狀物（`z-s07-red.jpg`），虛焦、沒有字，接受。燈籠都空白。
- **閃粒、印框發光**：s18 fix1 沒有，對。
- **故障特效（紅珠串、霓虹線、光環）**：選中的 35 支都沒有。落選的 s01 1101、s04 1102、s09 1201、s13 1201、s14 1201、s28 1102、s34 1101 才有。
- **火把頭白布**：s05 每支火把頭纏一圈白布、上有深色橫紋（`z-s05-torch.jpg`），看不出字形，輕微；精修後再看一次。
- **插地的火把、火盆**：s02、s03、s04、s06（已剪）、s10、s12、s15、s17、s20、s28 背景有三腳火把架或火盆，規格寫每支火把在人手上（已知）。都在背景，接受。
- **畫外句時的嘴**：
  - s04 阿令整段閉嘴（0–5.4），對。
  - s06 許硯 3.4–7.5 閉嘴（`mouth-s06.jpg`），對。
  - s12 胡縣令 0–6.0 閉嘴，對（6.5 秒起笑，已剪）。
  - s14 胡縣令 0–5.4 閉嘴（中等 4）。
  - s23 三人閉嘴，對。
  - s24 胡縣令 1.4–6.8 閉嘴，對（7.0 張嘴，已剪）。
  - s28 許硯 10 秒閉嘴，9.0–9.5 咬牙，對。
  - s29 三人閉嘴，對。
- **唐小棠背影不轉頭**：
  - s06（3.4–7.5）：只有後腦、丸子頭、粉緞帶、衣肩，對（1.3–1.8 秒轉頭露耳在剪點外）。
  - s14（0–5.4）：0–4.0 對；4.0 秒起頭微轉，臉頰與耳朵側面出來、看不到眼睛和嘴，接受。
  - s02（0–2.8）：2.0–2.75 秒轉頭露出側臉（看屋門方向），稿子准她這鏡露不說話的臉，嘴閉著，對。
- **笑場**：s21、s25（嚴重 1，改剪點）；s13（中等 3）；s14（中等 4）；s30（中等 5）；s15、s26（中等 11，接受）；s09、s31 縣令笑（稿子准冷笑、陪笑）；s33 7.0 秒後嘴角微笑——`picks.json` 剪在 7.2，建議收到 `end-before@7.0`（6.0 秒，這句約 4.4 秒），輕微。s01 阿令嘴角一點點上揚，輕微。
- **攝影機入鏡**：35 支 0.5 秒總表都沒有看到。

## 五、各場檢查結果

- **第一場（s01–s23，院子夜）**：
  - 天全黑、火把與燈籠，沒有像白天的窗或天。s03 0–0.8 秒右上角月亮（`start@0.8` 已避開大半，已知）。
  - 軸線：稿子屋門在左後、院門在右。s03、s19、s22、s23 屋門在左後，對。s05 房子在畫右、看不到院門（已知）；s08、s09、s11 過肩與全景的背景房角都在畫右，反打沒有換邊，夜裡背景不顯，接受。s10 身後是屋門暗處，對。
  - 人物左右：許硯在左、官府在右，s08 → s09（前景縣令在右 → 前景許硯在左）、s11、s19、s22 都一致；s12、s13、s21 胡縣令朝畫左，對；s16 縣令在左揪住畫右的趙捕頭（稿子寫側身朝畫右），對。
  - s02 → s03：s02 剪在 2.8 秒，許硯還背對我們張臂，沒有轉身跑（fix1 前 2.8 秒只有這些，已知）；「住手！」放在他背影上，s03 從 0.8 秒他從畫右跑進來接，動作接得上。接受。
  - s06 → s07：s06 唐小棠從左往右遞、s07 紙從畫右的手放進畫左的掌心，方向相反（已知）；插鏡，接受。s06 是一張薄紙、s07 是三份一疊，接受。
  - 阿令被架著（s08、s11、s19）：都是兩個衙役站在她兩邊，沒架住（已知），接受。
  - 人數與火把：s05 衙役十來個加後排家丁、火把十一、二支；s11 約七支；s22 九、十支（稿子不超過八支），接受。
  - 結尾 s23 讀得懂（見結論）。
- **第二場（s24–s35，院子夜）**：
  - 屋門前並排秦霜左、唐小棠中、阿令右：s23、s27、s29、s34 都一致，對。s27 畫右緣是灰白袖肩（阿令），對。
  - 胡縣令在許硯畫右：s30、s31、s32、s33、s35 一致；s33 前景左是許硯虛焦的耳朵、臉頰與鼻樑側面，沒有嘴，接受。
  - 衙役衣色：第一場是黑公服；s26、s31、s32、s35 背景衙役是灰藍短衣（已知，兩支種子都一樣），接受。
  - s34 三人往前走了不只半步（已知），接受。
  - 結尾 s35 讀得懂（見結論）。

## 六、建議與修法總表

| 鏡 | 等級 | 做法 |
| --- | --- | --- |
| s21 | 嚴重 | 剪點改 `end-before@4.0`（picks.json 抄成 1102 的退路，包進 4.25–4.75 的笑） |
| s25 | 嚴重 | 剪點改 `start@4.6 end-before@9.5`（picks.json 抄成 1101 的退路，包進大笑、甩袖被切） |
| s13 | 嚴重（槍架）＋中等（笑） | `start@2.6`；剪接時局部壓暗畫左上槍架（vf 見嚴重 2） |
| s14 | 嚴重（槍架）＋中等（笑） | `end-before@5.4`，放慢約 1.07 倍；局部壓暗畫左、畫右槍架 |
| s16 | 嚴重（槍架） | 局部壓暗畫左上槍架；畫中、畫右兩支接受 |
| s30 | 中等 | `end-before@7.0`（7.25 秒起笑） |
| s17 | 中等 | `end-before@5.8`（5.6 放不下這句） |
| s18 | 中等 | 接受；**可選重拍**補空印框（英文改寫在中等 7） |
| s35（s32） | 中等 | 接受；**可選重拍 s35** 改眼神（英文改寫在中等 8） |
| s22 | 中等 | 匾局部模糊（vf 見中等 10） |
| s31 | 輕微 | 可選：門邊紅纓槍局部壓暗 `crop=80:420:785:100`；不做就接受 |
| s33 | 輕微 | `end-before@7.0`（7.0 秒後嘴角微笑） |
| s05 | 中等 | 接受（鏡頭朝向、官帽、火把白布） |
| s15、s26 | 中等 | 接受（笑，兩支種子都一樣） |
| s08、s30 | 輕微 | 過肩前景露耳朵臉頰，接受 |
| s25、s26、s31、s32、s35 | 輕微 | 背景衙役腰刀，接受 |
| s27 | — | 維持 `end-before@2.0`（picks.json 的 2.0 比挑片表 2.4 好，2.0 秒起畫右冒出火把架） |
| 換種子 | — | 沒有一鏡換備用種子更好（看過的落選片都有珠串、兵器更多或站位更錯） |
| 水平翻轉 | — | 沒有建議。每一鏡都有交領或圓領內交領的人 |

## 給 refine-prep.py 的 review2-trims.tsv（建議）

只列要改的；其餘照 `picks.json`。局部處理不是剪點，不放進表，剪接時照下面的 vf 套。

```
shot	choice	reason
s13	9111202	start@2.6 pick-review：0–2.4 秒胡縣令笑著張嘴，2.5 秒起才驚怒；剩 5.4 秒，這句約 4.6 秒
s14	9111202	end-before@5.4 pick-review：5.5 秒起胡縣令嘴角上揚；這句約 5.8 秒，剪接時本鏡放慢約 1.07 倍
s17	9111102	start@0.4 end-before@5.8 pick-review：picks.json 的 5.6 只剩 5.2 秒放不下 5.3 秒的句子，6.5 秒前沒有笑
s21	9111101	end-before@4.0 pick-review：picks.json 抄成 1102 的退路 start@2.6 end-before@4.8，1101 在 4.25 秒起咧嘴笑
s25	9111102	start@4.6 end-before@9.5 pick-review：picks.json 抄成 1101 的退路 0.4–5.6，1102 這段 2.0–3.25 秒大笑、甩袖被切；挑片表定 4.6–9.5
s30	9111101	start@0.8 end-before@7.0 pick-review：7.25 秒起許硯嘴角上揚（picks.json 7.5）
s33	9111101	start@1.0 end-before@7.0 pick-review：7.0 秒後嘴角微笑（picks.json 7.2）
```

剪接時另外套（不放進 TSV）：
- s13（9111202）：`split[a][b];[b]crop=190:180:0:30,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=0:30`
- s14（9111202）：`split[a][b];[b]crop=150:250:0:85,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=0:85,split[a2][b2];[b2]crop=150:175:810:115,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c2];[a2][c2]overlay=810:115`
- s16（9111202）：`split[a][b];[b]crop=210:150:0:35,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=0:35`
- s22（9111101）：`split[a][b];[b]crop=80:85:65:122,boxblur=6,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/15)'[c];[a][c]overlay=65:122`
- s31（9111101，可選）：`split[a][b];[b]crop=80:420:785:100,eq=brightness=-0.4:saturation=0,boxblur=4,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=785:100`
- 座標是 960×544 草稿；精修放大後再套要乘上倍數。
- s18、s35：若重拍，用新片取代 9111202／9111101，剪點另定。
