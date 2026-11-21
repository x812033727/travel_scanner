# 第 4 集真人版 fix-polish：上架前精修重拍（s16、s14、s19、s23、s40）

2026-11-21 寫好，**還沒送出**。來源：`review-zt/consolidated/retakes.json` 裡 e004 的 tier B 五鏡（本集沒有 A；s25、s31、s22 是 C，不在這次範圍）。
種子 9049101／9049102，960×544 Ref2VA，每鏡兩支，共 10 支、72 秒草稿（s14 12 秒，其餘 6 秒）。

審片報告 `review-zt/reports/e004.md` 是精簡版，**沒有英文改寫句**（retakes.json 的 `prompt` 全空，報告說要回問代理 a3a3fcaf74f7f51b6，沒有去問）。
這版的寫法是照報告的中文修法、畫格條（`ep/e004/review/shots/`）、證據格（`ep/e004/review/x/` 的 s16-xuface、s14-wide、s19-box、s17-gold、
s23-motion、s38-full、s40-full）與 `e904-live/` 前四輪挑片表（`review-picks-*.tsv`、`fix1`–`fix4/review-picks.tsv`）自己判斷寫的。

**本集沒有 `_live-e904/.../picks.json`**（其他集都有）。現在用哪一支是從 `_live-e904/zhong-tian-qu-qi-e904-dh/cut/final.log`
（`s16-t1.mp4`、`s23 still`、`s40 still`）對 `e904-live/fix*/review-picks.tsv` 與 `cut-review-2.md` 推回來的，見下表 base 欄。

| 鏡 | 審片問題 | base（現在用的那支） | 改了哪些句子（舊→新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| **s16**（最優先） | 唐小棠背對鏡頭講話（錄音 `zq904a20`），許硯正面整鏡半張著嘴（證據 s16-xuface：0–3.5 秒一直張著一條縫），看起來像他在對嘴女聲 | `fix3/prompts/ref-s16-9041401.txt`（fix3 挑 9041401，成片 start@1.0 end-before@5.0） | 構圖：from behind Tang Xiaotang（她的背在右前景）→ **桌前全景、胸口高度，三人都離視線約 70 度；她站桌右端、正側臉朝畫左對許硯**；許硯臉：`surprised: brows raised, eyes wide, lips closed`（張嘴的來源）→ **brows lifted a little、eyes on the casket and then on her、lips pressed together in one straight line the whole shot、jaw still**；小禾：`eyes wide, lips closed` → **eyes wide on the casket, lips pressed together**；她的臉：新增 **brows level and firm、chin up、mouth corners level、lips pressed flat between words、brisk and businesslike**；動作：「背對走到桌前放匣、抬下巴」→ **開場已在桌邊，只做放匣一個動作，喘一口氣後說原句（台詞句照稿 「許硯，二十兩是吧？你看看這些夠不夠」，改回原聲）**，加 `Xu Yan and Xiaohe watch her with their lips pressed together the whole shot, only her lips moving`；木匣：book 大小那句加 **domed lid、brass corner pieces、one square brass hasp on its front**（照 s17、s20）；`no smile at any moment…` 那句拿掉，改成 **after her last word her lips settle into one flat closed line** | 無（照 base 八張） | 唐小棠露臉講話：本集前四輪她每次露臉講話都笑（d1 1101 已被選用時也有 4.5–5.25 秒一下側臉笑）。這次全景、她人小，逐部位寫冷臉、沒有任何 smile 字，但仍可能笑；**兩支都笑的話，退路是留現在的 fix3 1401（背影）**，只把許硯半張嘴那段剪掉。審片說「從右門進來」，這版開場已在桌邊（走進來那一段 d1 兩支都轉正臉對鏡頭笑），進門靠 s15→s16 剪接帶過 |
| s14 | 唐小棠本集第一次出場只有扶門框的一隻手，台詞全在畫外，到 s21 才露臉 | `fix2/prompts/ref-s14-9041302.txt`（fix2 挑 9041302，成片剪成 10.58 秒） | 構圖：Xu Yan alone（門框上只有一隻手）→ **側面雙人鏡，鏡頭垂直兩人連線：畫左門口她探身進來（頭肩與上身在門框內、一手扶門框、兩個髮髻都在畫內），正側臉朝畫右；畫右三大步外許硯正側臉朝畫左，捧著翻過來的裂鍋**；鍋寫死 **round-bellied black iron pot the size of a man's head, one long crack across its bottom facing up**（照 s13、s14 選定片段的鍋）；她的臉 **brows knotted and drawn down、eyes narrowed and fixed on the cracked pot and then on his face、mouth corners pulled down、jaw set、lips pressed flat between words、urgent and blunt**（拿掉 d1 的 shrewd、eyes darting：模型演成俏皮的笑）；他：lips closed → **lips pressed together in one straight line the whole shot**；動作：前半許硯轉鍋看裂縫（心裡話，錄音）、後半她說原句 「鍋裂了，米也見底，說到底就是缺錢。等著別走！」（原聲），他抬眼看她、嘴閉；`no one in the frame speaks` 與 `no smile…` 拿掉 | **加** `tangxiaotang-portrait-l1`、`angles/tangxiaotang-angle-a-l1`、`angles/tangxiaotang-angle-b-l1`（排在前 1–3，許硯改 4–6、屋內 7） | 同 s16：d1、fix1 四支她講這句都在笑，fix2 才改成只拍手。這次是第五、六次讓她露臉講這句，風險最高；**兩支都笑就留現在的 fix2 1302**。她在門「外」：場景圖是屋內，模型可能把她放在屋裡門邊（fix1 1201 就是）。12 秒照 base |
| s19 | 木匣是平蓋長匣、金錠一列五錠，跟 s16/s17/s20 的圓頂匣不同（證據 s19-box 對 s17-gold）；又是她的背 | `fix4/prompts/ref-s19-9041502.txt`（fix4 挑 9041502） | 構圖：over-the-shoulder from behind Tang Xiaotang's right shoulder → **稿子原本的過肩：從許硯左肩後拍，他的肩與後腦在左前景、臉朝她；她在畫右胸口以上、四分之三臉朝畫左看他，髮髻上方留空**；她的臉：**one eyebrow raised、eyelids half lowered、chin lifted、looking down her nose at him、mouth corners level、lips pressed flat between words、bored and indifferent**（照 fix0 挑片表建議，不寫 offhand）；木匣：`one small dark brown lacquered wooden casket with one brass clasp … five … in one row` → **book 大小那句加 domed lid、brass corner pieces、square brass hasp，蓋子開在她那一側，五錠「three in a back row and two in a front row」**（照 s17-gold 的後三前二）；動作：推過桌面直到他面前＋抬下巴 → **只把開著的匣子推過一手寬，手平放桌上說原句 「這點不過是零頭，拿去還，省得錢員外再上門」（原聲）**；許硯 keeps still、後腦朝鏡頭；`no smile…` 拿掉 | 無（照 base 七張） | 錠數：前三輪 fix 有四錠、三錠、一排的；這次寫後三前二，數目可能又不對（挑片要逐格數）。她露臉講話笑的風險同上，fix1 兩支是開口那一下笑；**兩支都不行就留 fix4 1502**。聲音從錄音 `zq904a22` 改成原聲，s19→s21 的音高差（審片第二節 4）可能變小也可能變大，要重聽 |
| s23 | 唐小棠 4.5 秒靜圖（fix1 1202 的一格慢推）不眨眼，好感 +10 前的關鍵反應是死的 | `fix1/prompts/ref-s23-9041202.txt`（靜圖的來源片段；成片 `s23 still s23-t1.png`） | 錨句：`dazzling sweet glamorous … rosy cheeks with dimples` → **拿掉 sweet、with dimples**（跟 s16、s19 的 base 一致）；臉：`brows drawn together, eyes glistening wet, lower lip pressed up…, mouth corners level, her throat moving once as she swallows` → **brows pinched upward in the middle、eyes wet and glistening、lower lip pressed up against the upper and trembling a little、mouth corners pulled slightly down、chin tight、moved and holding it in**（拿掉吞嚥）；動作：手指收緊＋吞嚥＋慢慢低頭（三個）→ **只做一個：手指慢慢收緊、指節泛白，濕的眼睛從他往下看到手、慢眨一次，下巴只低一指寬**；木匣改圓頂、包銅、方銅扣；`no smile…` 拿掉，改成嘴整鏡保持顫抖的直線、嘴角往下 | 無（照 base 四張） | 審片寫「慢慢低頭」，前三輪六支一低頭就變溫柔的抿嘴笑（fix1、fix2 挑片表），所以只讓眼睛往下、下巴低一指寬，低頭的量比審片要的小。**兩支都笑就留現在的靜圖**，或從新片段截嘴平的一段 |
| s40 | 黑影沒回頭：現在是 s38 9041202 同一張靜圖推近；水聲聽不到（水聲是剪接的事，不在這裡） | `fix1/prompts/ref-s38-9041202.txt`（現在的靜圖出自這支；s40 自己最後一輪 `fix2/prompts/ref-s40-9041301.txt` 也對照過） | 從 s38 的「屋裡門縫往外看的全景」改成 s40：**從他背後偏左、低角度中景，第一格就是他小腿到頭巾上方、板凳頂在下緣，背對鏡頭兩腳站在凳上、兩手平舉水桶在鍋口上方；灶火與白氣在他身體前方，把背、頭巾、頭勾成橘邊黑剪影；屋牆與門在畫右**；新增分隔句 **His whole figure stays a black silhouette with his face turned away from the camera the whole shot; the picture fixes the place only, never the mood.**（base 沒有 `never the mood. `，polish-build 與 refine-prep 要一次）；動作：踩凳＋舉桶 → **只做一個：往右肩猛回頭望畫外右邊的屋門，鏡頭只看到頭巾後側與下巴暗邊，桶微傾、水晃到桶口不出桶，定住**；光：`cold moonlight` → **cold blue night sky above the fence、灶火是畫面最亮的光**（fix1、fix2 四支的臉都被月光或灶火照亮）；鏡頭照 s40 舊版慢推 | 無（照 base 一張院子圖） | 幾何：屋門在他背後偏右，鏡頭放在他左後方，他往右轉頭時臉轉向遠側。但前兩輪四支都把臉轉亮、轉向鏡頭；**兩支都亮臉就留現在的靜圖**（cut-review-2 第 12 項已接受推近＋抖動＋切黑）。院子圖是白天的 `set-xujia-yuan-l2`，夜靠文字（s38 也是這樣出的） |

## 寫法的決定

- 五鏡都從 base 複製（`scratchpad e904p/mk.py` 組字串）：header、`[Shot 1] Photorealistic …` 開場、角色錨句、`never the mood. `、`One continuous shot.` 以後的乾淨畫面句與尾段照 base；改的是 `Initial composition:` 到 `The camera …` 之間。
- 露嘴的三鏡（s14、s16、s19）台詞照稿子原句，用系列的說話句（turned toward … never looking at the camera），**改回原聲**；s14 許硯的心裡話、s23 許硯的畫外仍用錄音，畫面上他嘴閉／不在畫內。
- 沒有任何 smile 字；`no smile at any moment …` 這句全拿掉，改成逐部位寫臉與「最後一個字後嘴收回一條線」（照 e930 fix3）。保留 base 的 `no second copy of anyone appears` 與 `no subtitles, captions or text` 兩句系列固定句。
- 一鏡一個動作，寫成 `her one movement:`／`his one movement:`；s14 是稿子的兩拍（他看鍋、她說話），分前半後半。
- 手伸向對方的寫法都避開：s16 她的兩手放在匣蓋上，s19 推過一手寬後手平放桌上、許硯不動，s14 她的手在門框上、兩人隔三大步。
- 換圖只有 s14：加唐小棠三張。其他照 base。

## 檢查（2026-11-21）

- `polish-build.py 4`：e904 5 shots, 10 drafts, 72 s，0 錯（腳本的 `REPO` 已是 `parents[7]`，不用像第 3 集那樣在記憶體裡改）。
  第一次跑 preflight 有 `unpictured Xu Yan`（s23 寫了「eyes lower from Xu Yan」，名字後面沒有 off screen）→ 改成 `from him`；
  重跑前先刪了 `fixp/prompts/ref-s*-904910{1,2}.txt`，否則 polish-build 會把自己上一次寫的檔當成「種子已用過」。
- `preflight-prompts.py fixp/colab-jobs.json`：0 error(s)、0 warning(s)。
- `h3r.sh check --manifest fixp/colab-jobs.json`：0 error(s)、0 warning(s)。

輸出：`~/mokaair-work/videos/zhong-tian-qu-qi-e904-dh/runpod/live/fixp/`（`retake.json`、`colab-jobs.json`、`prompts/ref-sNN-904910{1,2}.txt`），片子會出在 `fixp/out/`。

## 拍完要看

- s16：她整鏡是側臉、嘴角平（4.5 秒前後特別看）；許硯與小禾的嘴每 0.25 秒放大看是不是一直閉著；木匣是圓頂、闔著。
- s14：她在門口（不是屋裡）、露臉、講話時嘴角往下不往上；許硯嘴閉；鍋翻著、裂縫朝上。
- s19：數錠（每 0.5 秒），要五錠；匣子是圓頂包銅；她不看鏡頭、開口那一下沒笑；許硯後腦朝鏡頭。
- s23：有眨眼、手指收緊；嘴一直平或往下；頭頂留空。
- s40：臉一格都沒亮；兩腳在凳上；回頭的方向是畫右；水沒出桶。
- 任何一鏡兩支都不行：挑片表寫 **KEEP**（留現在那支或靜圖），不要寫 RETAKE。
