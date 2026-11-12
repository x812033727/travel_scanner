# Till the Verdict Do Us Part 第一季：道具參考圖企劃

2026-11-12 寫。對象是第一季 60 集（英文、直式 9:16、真人 AI 劇）。這份只決定**哪些道具要先畫一張參考圖、怎麼畫、花多少、分幾輪**，
並列出 `cast.json` 裡會跟 bible 打架或會畫出字的道具句。還沒有花任何點數；開跑要站主點頭。

讀過的：`cast.json` 的 `props`（讀取時 263 條，另有代理在加條目）、七份 `s1-bible-e0*.md` 的〈道具的樣子〉與〈先畫順序〉、
`s1-decisions-e021-e060.md`、第 1–40 集 `docs/videos/till-the-verdict-e0*/script.md` 的〈五張清單〉第 2 張（參考圖）與正文、
`docs/videos/drama/WRITING.md` 第九、十一節、`screen-test/README.md` 與 `screen-test/build.py`、`assets/refs/README.md`。

## 怎麼決定要不要畫

要畫的，至少符合一條：

1. **重複出現、每一鏡都要長得一樣**：跨很多集的主道具（帽子、玻璃磚、帳本、兩只行李箱、兩輛車、Elias 給的戒指、Remelt 的玻璃管與證據架、燈箱、藍面板）。
2. **模型已經畫錯過，或這一類東西模型常畫錯**：藥（直式小樣把 tablet 畫成平板電腦、把藥畫成中間帶黃的小花，`screen-test/README.md`）、
   小的疤（畫成紅色縫線，第 60 集）、歪的東西（瓶口微歪的 No. 1、歪杯子）、該是奶油色卻會變色的帽子、灰藍窄條毛線（會畫成嬰兒帽）。
3. **很容易畫出字**：要拍到正面的紙與玻璃（背光的三條、瓶底的光點、刻好的面板、燈箱上的紙、海報、鐘面）。這類先出一張圖**驗不出字**，就算之後不當參考圖用也值得。
4. **bible〈先畫順序〉或劇本〈五張清單〉已經點名建議先畫的**（第 4–10、11–20、21–30、31–40、41–50、51–60 集各章都有一行「道具若要參考圖」）。

照文字就好的：只拍背面或紙邊的紙、螢幕永遠背對鏡頭的手機與平板、穿在身上的衣物與配件（跟角色的全身照走）、吃的、光與效果、只在一兩集背景裡的工具。
理由：參考圖會蓋過文字（WRITING 第十一節），多給一張圖就多一個模型照抄的東西；紙背與手機背面本來就沒有可以「畫錯」的樣子。

## 共用的寫法

出圖路線照試鏡：Colab G4、Qwen-Image-Edit（`screen-test/build.py` 的 `job()`：20 步、cfg 4、兩個種子），image 1 是空白畫布。
每一張的英文由三段組成：**共用的頭** + 表裡的那一段 + **共用的尾**。

- 共用的頭：
  `Style: a photorealistic live-action photograph for a modern American prestige TV drama, a prop reference still shot on a cinema camera with a 50mm lens, soft even light, realistic materials and texture, the whole prop sharp. Not a painting, not 3D CG, not a cartoon. The picture fills the whole frame edge to edge: no black bars, no border. image 1 is only a blank canvas: take nothing from it but the plain backdrop.`
- 共用的尾：
  `The prop and the body parts named above are the only things in the frame. Clean image with nothing written anywhere, no watermark, no logo, no signature.`
  （場景中的那幾張把第一句換成 `Nobody is in the frame.`，照 `build.py` 的 `NO_TEXT_SET`。）
- **道具句一字不差照 `cast.json`**（下面〈要改的道具句〉建議先改的，用改好的那句）；後面才接擺法、比大小的身體部位與光。
  身體比大小沿用道具句自己的比法（指甲、手掌、前臂、膝、腰），參考圖把那個身體部位真的放進畫面，眼睛就能驗。
- **手的寫法**（不露臉；只到手腕或手肘）：
  - Nora 第 1–19 集：`a young woman's slender hand, fair skin with faint freckles, short unpainted nails, bare fingers`。
  - Nora 第 20 集起：同上，`bare fingers` 換成 `a plain narrow white-gold band with no stone on her left ring finger`（`elias-band` 每一鏡都在）。
  - Peg：`an older woman's weathered hand` 加 `only her fingertips` 或只拍右手（她的婚戒第 15 集當掉、第 57 集才回來，參考圖不要替她決定戒指在不在）。
  - 手只是比大小用：**用到片段裡時，若模型把手也抄進鏡頭，就在本機把參考圖裁到只剩道具**（不花點數），不要重畫。
- **尺寸**：手上的小道具用直式 `PORTRAIT` 1248×1664；長的、寬的（車、玻璃管、吹管、一排面板）用 `SET` 1920×1088；
  爐子、疤的插鏡、影本對燈這種「其實是一個鏡頭」的用直式 1088×1920。
- **背景**：白的、奶油色的東西放在淺灰或深色上（白藥放黑色桌墊，第 11 集本來就是這樣），不放在純白上，否則看不出輪廓。
- **依賴**：表裡寫「image 1 = ○○ 的選定圖」的，用 `latent: image1` 加 `Exactly one change: …`（WRITING 第十一節），保證同一頂帽子、同一支花瓶、同一座爐。那一張要排在被依賴的那一輪之後；共用的頭最後一句（空白畫布）這時拿掉。

## 主表

優先：**P1** 錯了會讓很多鏡或整集重拍，開拍前一定要有；**P2** 用幾集、或模型常畫錯，建議畫；**P3** 一兩集，有餘裕再畫。
「用幾集」第 1–40 集是從劇本正文數的，第 41–60 集照 bible 與 `cast.json` 的備註估。

| 優先 | id | 為什麼要畫 | 第一次用的集 | 用幾集 | 英文提示詞（照 cast.json 句，白底或場景中，用身體比大小，nothing written） | 要不要人手入鏡比大小 |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | `half-pill` | 全季的起點；小樣畫成平板電腦、畫成帶黃的小花；一定要「比指甲小」 | 1 | 3（1、10、11；2–4 在大衣口袋不入鏡） | `a tiny half of a white pill, smaller than a fingernail, plain white with one faint shallow line across it, no colour, no markings (a medicine pill, not a device), lying on a black desk mat; a young woman's index finger rests flat beside it, the pill smaller than her fingernail. Close macro view from slightly above, the pill sharp in the middle of the frame, soft white desk-lamp light. Only her fingertip and first knuckle are in the frame, short unpainted nail.` | 要（食指指尖，驗「小於指甲」） |
| P1 | `real-pill`（兼 `two-pills` 的鏡） | 第 11 集兩顆並排是證據鏡；半顆在左、整顆在右（bible 第 11–20 集） | 11 | 1 | `on a black desk mat, side by side in hard white desk-lamp light: on the left, a tiny half of a white pill, smaller than a fingernail, plain white with one faint shallow line across it, no colour, no markings (a medicine pill, not a device); on the right, a tiny whole round white pill, smaller than a fingernail, plain white with one clean line across it, no colour, no markings (a medicine pill, not a device). A young woman's index fingertip rests just below the two pills. Close macro view from slightly above, both pills sharp.` | 要（指尖） |
| P1 | `knit-hat` | 第 1 集到第 44 集的情感主線；要守住奶油色、手掌大、還在兩根前臂長的棒針上；之後三張圖都從它改 | 1 | 10（1–5、10、21–23、44） | `a cream baby hat about the size of her palm, half-knitted, still on two wooden knitting needles as long as her forearm, lying across a young woman's two open hands, her forearms along the needles so the needles read as long as her forearm; soft cream wool, even stitches. Plain light-grey backdrop, seen from above at a slight angle. Only her hands and forearms are in the frame, cut off below the elbows, bare fingers, short unpainted nails.` | 要（雙手與前臂） |
| P1 | `keepsake` | 第 6–23 集幾乎每集抱著或擺著，之後在她房間窗台；「裡面的影子」不能長成看得出的東西 | 6 | 12 以上（6–10、13、14、19–23，之後她房間的鏡） | `a heavy block of thick clear cast glass the size of a brick, about as long as her hand, faintly green, with a faint shadow of something folded inside, standing on a plain pale-grey tabletop; a young woman's right hand lies flat on the table beside it, the block exactly as long as her hand. Soft side light shows the thick glass edges; the shadow inside stays soft and shapeless. Only her hand is in the frame, cut off at the wrist.` | 要（手平放，驗「跟手一樣長」） |
| P1 | `nora-suitcase` | bible 第 4–10 集點名先畫；連續八集，要跟 Peg 那只一眼分得開 | 7 | 8（7–10、13、14、20、21） | `a mid-size navy soft-sided rolling suitcase, reaching just above her knee, no logo, standing upright on a plain light-grey floor, handle down, zipper closed; a slender young woman stands beside it, seen from the waist down in plain dark trousers and flat shoes, the top of the suitcase just above her knee. Only her legs and one hand resting on the suitcase are in the frame.` | 要（腰以下，驗「過膝一點」） |
| P1 | `peg-suitcase` | 同上；大、舊、棕褐硬殼，要跟深藍軟殼分開 | 5 | 7（5、8–10、13、14、20） | `a large old tan hard-shell rolling suitcase, reaching her hip, scuffed corners, no logo, standing upright on a plain light-grey floor, handle down; an older woman stands beside it, seen from the waist down in dark slacks and sensible shoes, the top of the suitcase level with her hip. Only her legs and one hand resting on the suitcase are in the frame.` | 要（腰以下，驗「到髖」） |
| P1 | `grant-car` | 十集出現；要一直是珍珠白、後窗有色、沒有廠徽，才不會跟黑車混（`s1-decisions` 4-2） | 5 | 10（5、7–9、18、19、36、43、57、59） | `Nobody is in the frame. a pearl-white full-size four-door luxury sedan (not a limousine) with tinted rear windows, no badge, number plate out of frame, parked at a wet grey curb on an overcast Pacific Northwest street, seen straight from the side, the whole car in the frame, grey-blue overcast daylight, wet asphalt, the windows dark.` | 不要（正側面本來就看不到車牌；車不用身體比） |
| P1 | `black-car`（兼 `watching-car`） | 第 10 集起在對街守著，第 15 集起是 Elias 的車；跟白車同一個角度畫，兩張並排驗分得開 | 10 | 約 14（10–21、26、30–32、49） | `Nobody is in the frame. a black full-size four-door luxury sedan (not a limousine) with no badge, number plate out of frame, parked at a wet grey curb on an overcast Pacific Northwest street, seen straight from the side, the whole car in the frame, grey-blue overcast daylight, wet asphalt, the windows dark.` | 不要（夜裡的 `watching-car` 照文字，用這張當車的樣子） |
| P1 | `ledger` | Peg 的帳本是喜劇與帳目的主道具，十六集；封面最容易被畫上字或格線 | 5 | 16（5、9–13、15、20、23、24、34、37、39、40、48、51） | `a small worn brown pocket ledger about the size of her palm, a pencil tucked in its spine, closed, lying in an older woman's open right palm, the ledger covering her palm; the soft brown cover scuffed at the corners, plain and unmarked. Plain light-grey backdrop, seen from above. Only her right hand is in the frame, cut off at the wrist.` | 要（右手掌，驗「手掌大」） |
| P1 | `clauses` | bible 第 11–20 集點名先畫；背光的三段淡影最容易長成假字（`cast.json` 的舊句還會畫字，見下） | 15 | 5（15–19） | `a single sheet of heavy white paper about the size of a magazine page, held so only its back shows, a faint shadow of three short paragraphs through it, held up by a young woman's two hands at its top corners against a bright overcast window, the light behind the paper; the shadows are three soft grey bands with blurred edges. Only her hands are in the frame, cut off at the wrists, bare fingers.` | 要（兩手捏著上角，驗雜誌大小） |
| P1 | `elias-band`（兼 `ring-box`） | 第 20–60 集每一鏡拍到她左手都要有；細、白金、沒有鑽，最容易被畫成鑽戒；戒盒同一張比大小 | 20 | 41（20–60） | `a plain narrow white-gold band with no stone, on her left ring finger: a young woman's slender left hand, fair skin with faint freckles, short unpainted nails, resting on a dark walnut table; beside her fingers, a small dark blue velvet ring box about the size of a walnut, open and empty. Close view of the hand, cut off at the wrist.` | 要（左手） |
| P1 | `forever-no1` | 第 21–30 集的核心證物；瓶口「微微歪」模型會畫正或畫成另一支花瓶（bible 第 21–30 集） | 26 | 4–5（26–29，28 回憶） | `a tall cream-white hand-blown glass vase about as tall as a forearm, its body gently swelling, its lip tilted very slightly to one side, standing alone on a plain white tabletop; a young woman's forearm rests flat on the table beside it, elbow to fingertips, the vase as tall as the forearm is long. Seen from the front at the height of the vase, plain light-grey backdrop, soft light glowing through the cream glass. Only her forearm and hand are in the frame.` | 要（前臂平放，驗「前臂高」） |
| P1 | `forever-vase` | 工廠版要跟 No. 1 是同一支、只差瓶口是正的；兩張在本機拼成並排給站主看 | 1（電視廣告） | 5（1、23、26、27、35） | image 1 = `forever-no1` 的選定圖，`latent: image1`：`Keep the photograph of image 1 exactly. Exactly one change: the vase's lip is perfectly level. It stays a tall cream-white hand-blown glass vase about as tall as a forearm, its body gently swelling; the same glass, colour, size, forearm, table, backdrop and light as image 1.` | 要（沿用 No. 1 那張的前臂） |
| P1 | `light-box-plinth`（兼 `glass-dome`、`glove-tray`、`cotton-gloves`） | bible 點名「展示台加玻璃罩加燈箱」一張；四集的舞台中心 | 26 | 4（26–29） | image 1 = `forever-no1` 的選定圖：`on a dark black stage, a waist-high white plinth whose flat top is a glowing white light box; on it the vase from image 1, a tall cream-white hand-blown glass vase about as tall as a forearm, its body gently swelling, its lip tilted very slightly to one side, under a clear glass display dome a hand taller than the vase, as wide as her two hands spread side by side; beside the plinth a small plain white tray on a slim stand holding a pair of white cotton handling gloves. Light rises from the light box through the vase; the stage around it is dark. A woman in a misty-grey floor-length gown stands beside the plinth, seen from the waist down, the top of the plinth level with her waist.` | 要（穿禮服的人腰以下，驗「齊腰」） |
| P1 | `vase-base-lit` | 第 28 集的高潮插鏡；光點最容易排成字母（"N.Q." 只在後製的鎖定靜圖） | 28 | 1 | `the thick round glass base of a cream-white vase seen from above, light rising through it from below, a short curved line of tiny air bubbles inside the glass glowing like pinpoints, nothing readable; the vase stands upside down on a glowing white light box, the base about as wide as a woman's palm; the fingertips of a hand in a white cotton handling glove rest on the rim. Dark surroundings, only the light from below.` | 要（戴白棉手套的指尖） |
| P1 | `furnace-no3`（冷） | 第 28–60 集的主景；`set-remelt.jpg` 是圓鋼殼、爐上有字、橫式，不能用（`s1-decisions` 4-10）；三種狀態都從這張改 | 28（回憶）、31 | 約 28（28、31–60） | `Nobody is in the frame. Inside an old glass studio of red brick, a huge round furnace of dark red firebrick bound with rusted steel bands, about twice as tall as a man, a steel flue rising from its dome, a round mouth at chest height behind a hinged steel door, no lettering, cold and grey with dust; a worn yellow safety line painted across the concrete floor in front of it, a black steel plate on the floor in front of the furnace mouth, a round steel shop stool about knee height beside it. Cold grey light from high windows. Seen from the front, the whole furnace from floor to flue.` | 不要（場景圖；人會被抄進鏡頭，用膝高的鋼凳比） |
| P1 | `furnace-no3`（點著） | 第 37 集起每一場 Remelt 戲；爐門縫的橘光要一致 | 28（回憶）、37 | 約 24（28、37–60） | image 1 = 冷爐的選定圖：`Keep the photograph of image 1 exactly. Exactly these changes: the furnace is lit, an orange glow pouring from the gap of its half-open door, warm orange light spilling across the black steel plate and the yellow line, the dust gone from the brick. Everything else stays as in image 1.` | 不要 |
| P1 | `blowpipe` | 熱料一定是橘的、冷了才是藍；一根人那麼長的管子，模型常畫短或畫成棍子 | 28 | 約 10（28、33、34、40、55–60） | `a long steel glassblowing pipe about as long as a person is tall, a glowing orange gather of molten glass at the far end, held level across the frame by two hands in a pair of long grey heat-resistant gloves reaching to the elbow, in a dark brick glass studio, the orange glow of a furnace mouth far behind and out of focus; the gather glows orange with heat shimmer, the steel pipe dull grey. Only the gloved hands and forearms are in the frame; the whole pipe from end to end fits across the frame.` | 要（Sparks 的灰色長手套） |
| P1 | `case-tracker`（兼 `tracker-bead`、空的 `evidence-rack`） | bible 第 31–40、41–50 集都點名「玻璃管加珠子加十二格架一張」；第 36–60 集的背景主角 | 36 | 約 22（36–60 的 Remelt 戲） | `Nobody is in the frame. On the red brick wall of an old glass studio, under one warm hanging work lamp: a long clear glass tube about as long as her outstretched arms and as thick as her wrist, mounted level on the red brick wall on two plain steel brackets, a row of small plain brass bands clamped around it at even spacing, no letters; one small amber glass bead about the size of a fingertip, resting inside the tube against the first brass band; below it an old steel sample rack bolted to the red brick wall below the tube, a long row of empty upright slots, each slot about the size of a hardcover book, no labels. Seen straight on from across the room, the whole tube and rack in the frame; a paint-spattered wooden stepladder taller than a woman leans on the wall at the left end.` | 不要（場景圖；用梯子比） |
| P1 | `blue-panel` | 全季唯一的「海港清晨藍」：第 40 集樣品、第 48–57 集吊燈每一片、第 57 集吊燈都要同一個藍 | 40 | 約 11（40、48–57） | `a flat panel of clear deep blue glass like the harbor at dawn, about the size of a large hardcover book, as thick as her little finger, a few tiny seed bubbles inside, held up in both hands to the low morning sun; a young woman's two hands hold it by its side edges, a plain narrow white-gold band with no stone on her left ring finger; a patch of deep blue light sliding across the red brick behind. Only her hands and wrists are in the frame.` | 要（兩手捏邊，驗書本大、小指厚） |
| P1 | `light-box` | 第 41–60 集的工作檯中心，照臉的冷白光也從它來；先要一張沒有紙的 | 41 | 約 15（41、43、48、50–60） | `a flat white drafting light box about the size of a large serving tray, its glass top glowing evenly from below, on the long wooden workbench, in a dim brick glass studio at night under one hanging work lamp; a young woman's two hands rest flat on its glowing top, a plain narrow white-gold band with no stone on her left ring finger. Seen from a low angle at the edge of the workbench. Only her hands and wrists are in the frame.` | 要（兩手平放，驗托盤大） |
| P1 | `engraved-panel`（兼第 51 集起的 `evidence-rack`） | bible 第 51–60 集點名「刻好的面板（字要糊）」；刻痕最容易長成看得懂的字；第 60 集疤的插鏡背景也是它 | 51 | 10（51–60） | `Nobody is in the frame. an old steel sample rack bolted to the red brick wall below the tube, a long row of upright slots, each slot about the size of a hardcover book, no labels, two clear engraved glass panels standing in the first two slots on the left, the other slots empty; each a clear glass panel about the size of a hardcover book, carrying a few soft frosted engraved strokes too small and blurred to read; warm orange firelight from the left, soft blurred strokes of orange firelight thrown through the engraved glass onto the red brick. Seen straight on, the two panels sharp, the empty slots fading out of focus.` | 不要 |
| P1 | `elias-scar-insert` | `s1-decisions` 6-9：開拍前先出一張直式靜圖給站主看（試鏡兩次都帶紅、手太大）；還帶紅就改成靜圖慢推 | 60 | 1 | 直式 1088×1920：`a man's bare left hand resting on the cold steel rim of a stool, small in the lower third of the frame, on the back of the hand a pale, flat, smooth silvery patch of old burn scar, healed decades ago, only slightly paler than the skin around it, no redness, no stitches, no open wound, lit by cold white streetlight from the open door, the furnace glow kept off the hand; behind it, far out of focus, two clear engraved glass panels on a steel rack against red brick.` | 要（道具本身就是手；驗手只占下三分之一） |
| P1 | `knit-hat-finished` | 第 48 集一眼要認出「就是醫院那頂」；bible 第 41–50 集要確認是奶油色、不是嬰兒鞋 | 48 | 約 13（48–60，49 起在鋼架最下層） | image 1 = `knit-hat` 的選定圖，`latent: image1`：`Keep the photograph of image 1 exactly. Exactly one change: the hat is finished and off the needles, a cream baby hat about the size of her palm, finished, off the needles, resting in her open palms; the needles are gone. The same cream yarn, the same stitch, the same hands, backdrop and light as image 1.` | 要（沿用同一雙手） |
| P2 | `canvas-tote` | Peg 每集背著；托特包最容易被印上字或標誌 | 1 | 17 以上（1、5、8–15、19、21、34–40） | `a plain beige canvas tote bag with no print, hanging from her left shoulder, soft and half full: on an older woman's left shoulder over a washed-out oatmeal cardigan, seen from the side from her shoulder to her knees, her head out of the frame; the bottom of the tote reaches her hip.` | 要（肩到膝，驗掛在肩上到髖） |
| P2 | `camel-coat` | 第 1–20 集每集都在（穿、披、掛）；它是道具句不在造型裡，顏色與長度要一致 | 1 | 20（1–20） | `a camel wool coat with deep pockets, worn open by a slender young woman over a loose cream cable-knit sweater dress, seen from the front from the collarbones to the knees, her head out of the frame; the coat reaches her knees, the deep front pockets at her hips.` | 要（鎖骨到膝） |
| P2 | `peg-ring` | 第 15 集當掉、第 57 集贖回，要跟 Nora 的鑽戒、Elias 的素圈三個分得開 | 5 | 13（5、8–15、57–60） | `a thin worn gold wedding band with one tiny old diamond, on her left ring finger: an older woman's weathered left hand resting on a plain wooden table, soft lined skin, short plain nails; the band thin and worn, the diamond barely bigger than a grain of rice. Close view of the hand, cut off at the wrist.` | 要（左手） |
| P2 | `peg-knitting` | bible 第 11–20 集點名：灰藍窄條會被畫成嬰兒帽；長度每集變，要先有基準 | 11 | 5（11、12、15、19、20 織完） | `a long narrow strip of slate-blue knitting on two wooden knitting needles as long as her forearm, about as long as her forearm, held up by an older woman's two hands, the strip hanging straight down between the needles; plain light-grey backdrop. Only her hands and forearms are in the frame.` | 要（手與前臂，驗「前臂長」） |
| P2 | `nora-ring` | bible 第 11–20 集點名；鉑金圓鑽「像鉛筆那麼寬」，要跟 Peg 的小舊鑽分開 | 15 | 2（15、35） | `a polished platinum wedding ring set with one round diamond as wide as a pencil, in her open palm: a young woman's open right palm, fair skin, the ring lying in the middle of it, the diamond bright and clean. Close view of the palm, cut off at the wrist.` | 要（掌心） |
| P2 | `window-poster` | 海報最容易被排上廣告字；臉要像 Grant（bible 第 21–30 集） | 23 | 1 | image 1 = `assets/refs/grant-portrait.jpg`，`latent: empty`：`a tall window poster of Grant in his light stone suit cradling a cream-white vase, no lettering anywhere: on the inside of a tall shop window, a photograph of the man in image 1 from the waist up in a light stone-colored suit, holding a tall cream-white glass vase in both arms, plain pale-grey studio background, the photograph filling the whole poster edge to edge; seen from the sidewalk through the glass, soft grey daylight reflections on the window. The poster is as tall as a man.` | 不要（海報上的人就是比例） |
| P2 | `gown`（Nora 的 `gown` 造型，不是 props；兼 `gown-folded`） | bible 第 21–30 集點名「霧灰禮服與手拿包」；七集的顏色要一致，也給 Nora `gown` 全身照當第二張圖 | 24 | 7（24–30） | `a misty-grey floor-length gown with a modest high boat neckline and long sleeves, on a plain headless dress form of a slender woman's size, the whole gown in the frame from neckline to hem, the hem resting on the floor; soft matte fabric, plain light-grey backdrop, soft even light.` | 要（用人台當身體） |
| P2 | `grey-clutch` | 第 24–30 集一直在手上，裝律師函；要跟禮服同一個霧灰 | 24 | 6（24、26–30） | `a small misty-grey satin clutch about the size of her hand, closed, held in a young woman's left hand against the skirt of a misty-grey gown, a plain narrow white-gold band with no stone on her left ring finger. Only her hand, wrist and a strip of the gown are in the frame.` | 要（左手，驗「手那麼大」） |
| P2 | `waiting-hat` | 淡黃、比較小，故意跟 Nora 的奶油色分開（`s1-decisions` 4-11）；從同一張改最能驗出差別 | 33 | 1 | image 1 = `knit-hat` 的選定圖，`latent: image1`：`Keep the photograph of image 1 exactly. Exactly one change: the hat is a tiny pale yellow baby hat, half-knitted on two wooden knitting needles as long as her forearm, pale yellow yarn instead of cream. Everything else stays as in image 1: the hands, the needles, the backdrop and the light.` | 要（沿用同一雙手） |
| P2 | `copies-to-light`（鏡頭靜圖，不當參考圖） | 第 30 集 mid hook；劇本〈五張清單〉建議先出一張直式靜圖給站主看；驗墨跡不成字 | 30 | 1 | 直式 1088×1920：`two thin photocopied white pages held flat together up to a bare bulb, the light shining through both, one small soft dark smudge of ink showing through where two marks sit exactly on top of each other, nothing readable; the bare bulb in a black wire cage on a white corridor wall behind the pages; a young woman's two hands hold the pages by their corners, a plain narrow white-gold band with no stone on her left ring finger; focus on the smudge and her fingertips, the rest of the pages soft pale grey.` | 要（兩手） |
| P2 | `furnace-no3`（蓋帆布） | 第 31–32 集的揭幕；從冷爐改才是同一座 | 31 | 2（31、32） | image 1 = 冷爐的選定圖：`Keep the photograph of image 1 exactly. Exactly one change: the furnace stands under a huge dusty grey canvas tarp that hangs to the floor, only the steel flue showing above it. Everything else stays as in image 1.` | 不要 |
| P2 | `crooked-cup` | 「每一隻歪的方向都不一樣」模型會畫成整齊的一排；架子是第 33–60 集的背景 | 33 | 3（33、34、40）＋背景 | `a row of small clear lopsided hand-blown cups on a steel shelf, each a small clear hand-blown cup about the size of her fist, leaning to one side, its rim lopsided, every cup leaning a different way; a young woman's loose fist rests on the shelf beside the first cup. Red brick wall behind, warm work-lamp light. Only her fist and wrist are in the frame.` | 要（拳頭，驗「拳頭大」） |
| P2 | `wall-clock` | 鐘面最容易被畫上數字；第 39 集十二點、第 54 集十點都要插鏡 | 39 | 約 10（39、40、46、54＋Remelt 背景） | `Nobody is in the frame. an old round wall clock with a white face and plain black bar markers, no numerals, about as wide as a man's shoulders, hung high on a red brick wall above one leaf of a pair of tall rusted double steel doors, both hands pointing straight up; cold grey daylight.` | 不要 |
| P2 | `heat-gloves` | bible 第 51–60 集點名「灰色隔熱手套」；第 55–60 集每一鏡 Elias 兩手都戴，第 58、60 集各脫一隻 | 55 | 6（55–60） | `a pair of thick grey heat-resistant work gloves reaching halfway up his forearms, on both his hands: a man's two hands resting on his knees, olive skin above the cuffs, the sleeves of a plain black T-shirt above; warm orange furnace light from one side. Only his hands and forearms are in the frame.` | 要（男人的兩手，驗「到前臂一半」） |
| P2 | `blue-panel-row` | 第 48–56 集的進度就是這排面板；藍要跟樣品片一樣 | 48 | 9（48–56） | image 1 = `blue-panel` 的選定圖：`Nobody is in the frame. a long row of flat panels of clear deep blue glass like the harbor at dawn, each about the size of a large hardcover book, standing upright on a plain wooden rack, along the red brick wall of an old glass studio, the same deep blue as the glass in image 1, glowing blue where the first daylight comes through them.` | 不要 |
| P2 | `chandelier-sketch` | 可以拍正面的水彩；紙邊最容易被畫上註記；藍要跟樣品片一致（bible 第 31–40 集） | 38 | 2（38、40） | image 1 = `blue-panel` 的選定圖：`a large watercolor drawing on heavy white paper about the size of a newspaper page, many deep blue glass panels hanging in overlapping rows like falling waves, no writing, painted in the same deep blue as the glass in image 1, lying flat on a long wooden workbench, seen from above; a young woman's two hands rest on its top corners, a plain narrow white-gold band with no stone on her left ring finger; clean white margins.` | 要（兩手按角，驗報紙大小） |
| P2 | `light-box-papers`（驗字，不當參考圖） | bible 第 41–50 集：「先畫燈箱與上面的紙（確認畫不出字）」 | 41 | 3（41、43、48） | image 1 = `light-box` 的選定圖：`two sheets of white paper laid one over the other on the glowing light box, only two soft overlapping grey shapes far out of focus, seen from a low angle at the edge of the workbench, the focus on the near edge of the light box.` | 不要 |
| P2 | `left-hand-sketch` | 第 51–60 集一直貼在證物架右邊；手描的紙最容易被加上簽名或日期 | 51 | 10（51–60） | `Nobody is in the frame. a sheet of white drawing paper about the size of a magazine with a plain pencil outline of a left hand traced around spread fingers, no writing, taped to the red brick by one strip of masking tape; warm work-lamp light, seen straight on.` | 不要（描的就是手，大小自明） |
| P2 | `receipt` | 第 52 集攤在燈箱上、正面朝上發白，是全季最危險的一張紙；第 5、9 集摺著照文字 | 5 | 4（5、9、52、53） | image 1 = `light-box` 的選定圖：`a small thermal receipt about as long as her finger, its faded print far too faint to make out, pressed flat on the glowing light box, the paper shining white; a young woman's index finger rests beside it, the receipt as long as her finger, a plain narrow white-gold band with no stone on her left ring finger.` | 要（食指，驗「手指長」） |
| P3 | `blue-cup` | 從歪杯子改成深藍，兩隻（Wexler、Rosa）同一個樣子 | 43 | 2（43、49） | image 1 = `crooked-cup` 的選定圖：`Keep the photograph of image 1 exactly. Exactly one change: the first cup is a small deep blue hand-blown cup about the size of her fist, leaning to one side, its rim lopsided, the same deep blue as harbor glass at dawn. Everything else stays as in image 1.` | 要（沿用拳頭） |
| P3 | `gown-box` | 掀開時要看到摺好的霧灰布料；第 24–25 集 | 24 | 2（24、25） | `a long flat pale grey box tied with a grey satin ribbon, about as long as her arm, its lid lifted, misty-grey fabric folded inside, lying on a dark walnut table; a young woman's arm lies along the box from shoulder to fingertips, the box as long as her arm. Only her arm and hand are in the frame.` | 要（手臂） |
| P3 | `gold-envelope` | bible 第 21–30 集點名；燙金面最容易被壓上字 | 22 | 1 | `a stiff gold-foil envelope about as long as her hand, its face blank, catching the light, held in a young woman's right hand; the gold face smooth and empty. Only her hand is in the frame, cut off at the wrist.` | 要（右手） |
| P3 | `glass-bird` | 「一邊翅膀比較低」模型會畫對稱；只在第 1 集夢裡 | 1 | 1 | `a clear hand-blown glass bird about the size of a fist, one wing lower than the other, sitting in a young woman's open palm; dreamy soft light, plain dark backdrop. Only her hand is in the frame, cut off at the wrist.` | 要（掌心） |
| P3 | `vase-base-blank` | 第 23 集要跟第 28 集的光點瓶底對照（乾淨、沒有氣泡） | 23 | 1 | `the thick round glass base of a cream-white vase seen from below, clear and smooth, no bubbles inside, the vase held upside down in a young woman's two hands, a plain narrow white-gold band with no stone on her left ring finger; bright white shelf light behind. Only her hands are in the frame.` | 要（兩手） |
| P3 | `practice-furnace` | 第 33–34 集；有餘裕再畫，否則文字 | 33 | 2（33、34） | `Nobody is in the frame. a small round practice furnace on steel legs, about waist high, its mouth the size of a dinner plate glowing orange, against the right red brick wall of an old glass studio, a black steel plate on the floor in front of the furnace mouth, a round steel shop stool about knee height beside it.` | 不要 |
| P3 | `gas-valve` | 壓力錶最容易被畫上刻度數字；第 36–37、55–60 集 | 36 | 8（36、37、55–60） | `Nobody is in the frame. a gas valve with a red lever handle and a round dial gauge on a black pipe at knee height beside the furnace, the dial a pale blur, the red lever pointing along the pipe; dark red firebrick to the left, warm orange furnace light.` | 不要 |

合計 **50 張**（P1 24、P2 19、P3 7）。

## 不畫、照文字的

下面這些照 `cast.json` 的道具句（或 bible 的句子）寫進每一鏡就好；有「要改」標記的見下一節。

- **已經包在上表某一張裡**：`ring-box`、`glass-dome`、`glove-tray`、`cotton-gloves`、`tracker-bead`、`evidence-rack`（空的與第 51 集起兩種）、`safety-line`、`steel-plate`、`furnace-tarp`（蓋帆布那張）、`watching-car`、`gown-folded`（照 `gown` 那張）、`steel-stool`。
- **交給場景企劃**：`chandelier`（第 57 集渡輪站大廳首航夜的場景圖，image 1 給 `blue-panel` 的選定圖）、`forever-wall`、`launch-screen`、`steel-doors`、`blowpipe-rack`、`work-lamp`、`long-bench`、`sand-bins`、`annealer`、`ferry`、`lectern`、`sponsor-backdrop`。
- **只拍背面、紙邊或虛焦的紙**：`property-agreement`、`divorce-papers`、`delivery-slip`、`sketch-folder`、`grant-check`、`custody-copy`、`lab-report`、`pickup-log`、`manila-envelope`、`pawn-ticket`、`ashford-card`、`house-rules-card`、`invitation-card`、`seat-card`、`certified-envelope`、`cease-and-desist`、`photocopy`、`young-grant-card`、`cashiers-check`、`lease`、`burner-estimate`、`ferry-notice`、`entry-form`、`date-stamp`、`hank-receipt`、`blank-sheet`、`sketch-sheets`、`court-papers`、`ten-sheets`、`signature-strips`、`examiner-file`、`examiner-notebook`、`sticky-note`、`bank-card-copy`、`certificate-copy`、`examiner-report`、`charge-letter`、`receipt-copy`、`competition-envelope`、`harbor-drawing`、`lab-pouch`、`evidence-bag`、`doctor-clipboard`、`emt-clipboard`；`lyle-photo` 照第 35 集〈五張清單〉從 c13 截一格，不另畫。
- **手機、平板與螢幕**（背面、側面或一團白光）：`nora-phone`、`grant-phone`、`elias-phone`、`new-phone`、`phone-box`、`peg-phone`、`sienna-phone`、`lyle-phone`、`guest-phones`、`nora-own-phone`、`hank-phone`、`gus-phone`、`dana-phone`、`rosa-phone`、`fiona-phone`、`theo-tablet`、`ashford-tv`、`card-reader`、`desk-phone`、`sim-card`、`sim-packet`。
- **穿戴、拿在手上的小東西**（跟角色全身照走，或一兩鏡）：`elias-glove`、`navy-raincoat`、`white-handkerchief`、`elias-overcoat`、`peg-apron`、`nora-jacket`、`sparks-glasses`、`gus-apron`、`gus-gloves`、`gus-face-shield`、`sparks-helmet`、`dust-respirator`、`sparks-jacket`、`sparks-gloves`、`fiona-badge`、`fiona-watch`、`fiona-binder`、`sleeve-protectors`、`peg-glasses-folded`、`grant-cufflink`、`grant-shoes`、`card-wallet`、`bank-cards`、`cash`、`peg-wallet`、`motel-key`、`house-key`、`ashford-key`、`fisk-pen`、`ballpoint`、`grant-pen`、`examiner-pen`、`engraving-pen`、`poker-chip`、`cue-cards`、`handheld-mic`、`lyle-camera`、`press-cameras`、`examiner-loupe`、`examiner-ruler`、`fisk-folder`、`dana-files`、`scissors`、`knitting-needle`、`peg-yarn`、`paper-clip`、`zip-bag`、`tv-remote`、`glass-rod`、`chalk-stub`、`gus-flashlight`、`claire-padlock`。
- **吃的與廚房**：`plastic-cup`、`drinking-glass`、`soup-pot`、`peg-thermos`、`peppermint-bowl`、`ashford-fridge`、`peg-dinner`、`clean-plate`、`pasta-bowl`、`pasta-bowl-washed`、`pasta-pot`、`soup-ladle`、`stockpot`、`chowder-bowl`、`chowder-splash`、`oyster-crackers`、`stew-pot`、`takeout-boxes`、`grant-coffee`、`wooden-spoon`、`cast-iron-pot`。
- **醫院、旅館、Ashford 家的陳設**：`umbrella`、`paper-bag`、`hospital-blanket`、`belongings-bag`、`nurse-call`、`curtain-panel`、`curtain-rod`、`red-curtain`、`ladder`、`guest-lamp`、`builder-plaque`、`reyes-lamp`、`photocopier`。
- **車**：`rideshare-car`、`gus-pickup`、`sparks-motorbike`、`cole-hand`（遠、虛，車照 `grant-car` 那張）。
- **光與效果**（寫在鏡上的光，不是東西）：`camera-flash`、`follow-spot`、`spotlight`、`green-light-box`、`caged-bulb`、`smoke`、`firelight-strokes`、`hot-glob`、`tripod-work-light`。
- **Remelt 的工具與雜物**（一兩集或背景）：`pell-batch-sacks`、`beam-balance`、`cobalt-jar`、`measuring-spoon`、`steel-bucket`、`charging-shovel`、`casting-mould`、`moving-blanket`、`drawing-tube`、`blackboard`、`chalk-tally`、`stepladder`、`gas-fitting`、`pipe-wrench`、`tech-toolbox`、`fire-extinguisher`、`sand-pallets`、`blank-panel`、`cullet-sack`、`cullet-spill`、`army-cot`、`stretcher`、`crates`。
- **建議刪掉的舊條目**：`two-pills`、`invitation`、`peg-pot`；`marriage-application` 換句（見下一節）。

## 估價與分輪

- 每張約 **0.27 CU**（試鏡 r3：6 張約 15 分鐘、約 −1.6 CU，含開機），每項兩個種子。
- 全部 50 項 × 2 = 100 張 ≈ **27.0 CU**。只畫 P1：24 項 48 張 ≈ **13.0 CU**；P1＋P2：43 項 86 張 ≈ **23.2 CU**。
- 預留重畫：約五項裡一項要再畫一輪（10 項 20 張）≈ **5.4 CU**。**建議上限 33 CU**（全部）或 **18 CU**（只畫 P1）。
- 每輪 **≤ 12 張**（6 項 × 2 個種子，約 3.2 CU、G4 約 15–20 分鐘）：Colab 斷線時最多損失一輪（`minimax-h3-colab` lessons：第 12 張斷線空轉約 15 CU，所以一輪不放多）。
  沒有依賴的第 1、2、4、9 輪可以排在同一個 session 連跑，省冷開機；有依賴的（第 3、5、6、7、8 輪）要等前一輪選定。
- 每輪跑完：兩個種子並排標好名字給站主挑（WRITING 第十一節），選定的轉 JPEG 放進 `assets/refs/`、更新 `SHA256SUMS` 與 `assets/refs/README.md`；原圖照 `docs/videos/AI-DRAMA-DRIVE.md` 用 `todrive.sh` 傳到 `_共用/製作檔/`。

| 輪 | 內容（尺寸） | 依賴 | 為哪幾集 | 約 CU |
| --- | --- | --- | --- | --- |
| 1 | `half-pill`、`real-pill`、`knit-hat`、`keepsake`、`nora-suitcase`、`peg-suitcase`（都 1248×1664） | — | 1–14 | 3.2 |
| 2 | `grant-car`、`black-car`（1920×1088）；`ledger`、`peg-ring`、`canvas-tote`、`camel-coat`（1248×1664） | — | 1–20 | 3.2 |
| 3 | `clauses`、`peg-knitting`、`nora-ring`、`elias-band`（1248×1664）；`waiting-hat`、`knit-hat-finished`（image 1 = `knit-hat`） | 第 1 輪 | 11–24，48 | 3.2 |
| 4 | `forever-no1`、`vase-base-lit`、`window-poster`、`gown`、`grey-clutch`（1248×1664）；`copies-to-light`（1088×1920） | — | 23–30 | 3.2 |
| 5 | `forever-vase`、`light-box-plinth`（image 1 = `forever-no1`）；`furnace-no3` 冷（1088×1920）；`blowpipe`、`case-tracker`（1920×1088）；`blue-panel`（1248×1664） | 第 4 輪 | 23–40 | 3.2 |
| 6 | `furnace-no3` 點著、蓋帆布（image 1 = 冷爐）；`crooked-cup`、`wall-clock`、`light-box`（1248×1664）；`engraved-panel`（1920×1088） | 第 5 輪 | 31–60 | 3.2 |
| 7 | `elias-scar-insert`（1088×1920）、`heat-gloves`；`blue-panel-row`（1920×1088）、`chandelier-sketch`（image 1 = `blue-panel`）；`light-box-papers`、`receipt`（image 1 = `light-box`） | 第 5、6 輪 | 41–60 | 3.2 |
| 8 | `left-hand-sketch`、`blue-cup`（image 1 = `crooked-cup`）、`gown-box`、`gold-envelope`、`glass-bird`、`vase-base-blank` | 第 6 輪 | 1、22–25、43–60 | 3.2 |
| 9 | `practice-furnace`、`gas-valve`（1088×1920） | — | 33–37、55–60 | 1.1 |

合計約 27 CU（不含重畫）。`elias-scar-insert` 若想早點知道第 60 集要不要改成靜圖慢推，可以換到第 1 輪（只差先後，不加錢）。
三號爐三張若場景企劃已經排了 Remelt 直式圖（`s1-decisions` 4-10），就用那張當 image 1、這裡只畫點著與蓋帆布，省 0.5 CU。

**每一張的驗收**（不過就照 WRITING 第十一節「改字只改一次」：第二輪還錯就改擺法或拿掉那張圖）：

1. 整張沒有字、數字、刻度、標誌、車牌（放大看紙邊、瓶底、鐘面、玻璃刻痕、帳本封面、托特包）。
2. 大小對得上身體：藥比指甲小、玻璃磚跟手一樣長、帽子手掌大、行李箱到膝上／到髖、展示台齊腰。
3. 顏色：帽子是奶油色（不是淡黃），候診區那頂是淡黃；藍面板、草圖、整排面板是同一個藍；禮服與手拿包同一個霧灰；熱料是橘的。
4. 形狀：No. 1 瓶口微歪、工廠版是正的；歪杯子每隻歪向不同；藥是藥（不是平板、不是花）；Elias 的戒指沒有鑽。
5. 皮膚上沒有紅點、紅痕（試鏡學到：小的痕會變紅），疤是銀白、不帶紅。

## 要改的道具句

### 跟 bible 打架的

| id | `cast.json` 現在 | 打架的地方 | 建議 |
| --- | --- | --- | --- |
| `two-pills` | `two tiny round white pills, … the left one's single line slightly shallower …` | 第 11 集是**半顆**在左、**整顆**在右（bible 第 11–20 集）；這句寫成兩顆整的；`real-pill` 的備註已說取代它 | 刪掉；第 11 集兩句（`half-pill`、`real-pill`）都抄 |
| `half-pill` | 句尾 `, resting in a crumpled white tissue` | bible 的句子到 `(a medicine pill, not a device)` 為止，面紙、夾鏈袋、桌墊都是接在後面的狀態；照抄 `cast.json` 會讓第 10–11 集也有面紙 | 句子停在 `(a medicine pill, not a device)`；面紙寫進備註當接法 |
| `knit-hat` | 句尾 `, a loose tail of yarn`；備註 `Peg's tote 3–20` | bible 的句子沒有 loose tail（每鏡一字不差）；bible 第 4–10 集：第 5–10 集在醫院袋、第 10 集才進 Peg 的帆布袋 | 拿掉 `, a loose tail of yarn`；備註改 `hospital belongings bag 5–10; Peg's tote 10–20` |
| `clauses` | `a single sheet of heavy white paper with three short numbered paragraphs and a signature line, text not readable`；備註 `Add any readable text in post` | bible 第 11–20 集換成背光的紙背；`numbered paragraphs`、`signature line` 會畫出數字與假字；`s1-decisions` 3-2 建議全部念出來、後製也不上 | 換成 `a single sheet of heavy white paper about the size of a magazine page, held so only its back shows, a faint shadow of three short paragraphs through it`；備註改「念出來，不後製」 |
| `marriage-application` | `a folded government form, not readable, folded twice into a man's breast pocket` | bible 第 11–20 集已換句；`government form` 會畫出抬頭、印章 | 換成 `a single white form, held so only its back shows`；摺起接 `…, folded twice` 與 `, sliding into his inside breast pocket` |
| `grant-phone` | 句尾 `; when lit, the screen is blurred (any text added in post)` | 提示詞裡出現 `text`；bible 說螢幕一律背面、側邊或虛焦，亮起寫 `its screen a soft white glow, seen from the side`；後製上字也跟 3-2 衝突 | 句子停在 `about the size of his palm`；亮起的寫法放備註 |
| `nora-phone` | 句尾 `, screen dark or blurred, no logo` | bible 句子到 `about the size of her palm` 為止；`or` 讓模型自己選，`blurred` 的螢幕會正對鏡頭 | 改成 `a phone in a pale pink case, about the size of her palm, no logo` |
| `peg-pot` | `a white enamel soup pot with a lid, nothing written on it` | 跟 `soup-pot` 是同一個鍋；沒有大小；`nothing written` 是點名「寫字」的否定句（WRITING 第九節） | 刪掉，用 `soup-pot` |
| `paper-bag` | 句尾 `, on a chair` | 第 3 集他拎進門、之後才放椅上；位置寫死在道具句裡 | 拿掉 `, on a chair`，放備註當接法 |
| `gown-folded` | `the mist-grey gown …`（2026-11-12 新加） | Nora `gown` 造型、`gown-box` 備註與 bible 都寫 `misty-grey` | 改 `misty-grey`；建議寫成 `a misty-grey floor-length gown folded over her forearms against her chest` |
| `blue-panel-row` | 備註 `Along Remelt's right wall from 46` | bible 第 41–50 集的帳：吊燈合約第 142 天才簽（第 46–47 集是第 141 天），第三片第 144 天（第 48 集）出爐；`blue-panel` 備註寫 48–57 | 改 `from 48`；bible 第 31–40 集 `blue-panel` 那格的「第 46–57 集」也一起改成 48–57（請寫稿的人核對） |
| `evidence-rack` | 備註 `From 48 the finished hat rests on its bottom ledge` | `knit-hat-finished` 寫 49–60；bible 第 41–50 集一處寫第 48 集起、一處寫第 49 集起留在 Remelt | 統一成「第 48 集最後放上，第 49–60 集在架上」 |
| `invitation` | 跟 `invitation-card` 同一句 | 備註已說被取代 | 刪掉 |

### 會畫出字的（bible 同句的一起改）

| id | 問題字 | 建議 |
| --- | --- | --- |
| `certified-envelope` | `certified-mail sticker` 會印出 CERTIFIED MAIL | `a long white envelope with a small plain green sticker in one corner` |
| `lab-pouch` | `tamper-evident specimen pouch` 真的這種袋子滿是印字 | `a clear plastic pouch about the size of her hand, a red seal strip across the top, plain and unprinted` |
| `evidence-bag` | `evidence bag`、`blank white label` 會印出 EVIDENCE 與表格 | `a clear plastic bag about the size of his hand, a red seal strip across the top, a small plain white sticker` |
| `crates` | `no stencilled letters`：否定句點名了字 | `plain unmarked pale wooden crates about the size of a suitcase, packed with pale wood wool` |
| `poker-chip` | `casino-style` 會帶面額與字 | `a plain solid red poker chip with a thin white edge stripe, about as wide as his thumb is long` |
| `builder-plaque` | 牌子本身就招字；`no engraving visible` 是否定句 | `a small smooth brass plate beside the door, about the size of her hand, seen at a steep angle, only a bright reflection on its face` |
| `window-poster` | `poster` 會排上廣告標語 | 改成照片：`a tall photograph of Grant in his light stone suit cradling a cream-white vase, printed edge to edge on the inside of the shop window` |
| `ashford-card`、`young-grant-card`、`house-rules-card` | 正面 `print not readable` 仍會畫出一排假字 | 句尾改 `, held so only its blank back shows`（拍在桌上那一鏡本來就是背面朝上） |
| `custody-copy`、`pawn-ticket`、`hank-receipt`、`receipt-copy` | 同上 | 改成摺起或背面：`…, folded so only its blank back shows` |
| `delivery-slip` | 第 7 集要拍到簽字，正面一定入鏡 | 句尾加 `, the slip far out of focus, the focus on the pen tip`（照 WRITING 第九節：焦點放在筆尖） |
| `seat-card` | `print not readable` | bible 說只拍金邊：改 `…, seen edge-on, only its gold edge catching the light` |
| `beam-balance` | `its markings too fine to read` 等於叫它畫刻度 | `…, its scale a soft pale blur` |
| `ferry` | `no name or numbers visible` 是否定句 | `a large white car ferry with its deck lights on, docking beyond the glass wall, seen far off, its plain white hull soft in the evening haze` |
| `wall-clock` | 沒有大小（不會畫字，但鐘面一大就容易長數字） | 加 `about as wide as a man's shoulders`（上表已用） |

### bible 有、`cast.json` 還沒有的道具句

不影響上面的參考圖，但寫分鏡的人會找不到 id：`blue nitrile gloves`、`flat white plastic tweezers as long as her finger`、`a small black pocket magnifier about the size of his thumb`、
`a small black desk lamp casting hard white light`、`a plain silver ballpoint pen as long as her hand`、`a plain black rollerball pen as long as her hand`（Dana、Nora）、`a slim gold pen`、`a plain blue motel ballpoint pen`、
`a plain silver wristwatch on his left wrist, its face turned toward him`（Fisk）、`a bouquet of pale pink roses …`、`a flat white gift box …`、`two plain white paper cups with lids, no logo`、
`a small wooden desk drawer with a brass keyhole`、`a pale blue cotton shirt, half folded`、`a grey office desk phone on speaker`、`a thick plain buff case file`（Reyes）、`worn beige house slippers`、
`a faint pale band of skin on her left ring finger where a ring used to be`、`a short yellow pencil as long as her finger`、`long dark chestnut locks of hair lying in a white porcelain sink`、
`a long glass display counter of old wristwatches, silver lockets and rings under warm light`、`a computer monitor on the counter, its screen turned toward Nora and away from the camera`、
`a brand-new brushed-steel deadbolt and lever handle on the black steel door frame, bright and unscratched`、`a small motel bedside lamp with a pale yellow shade, warm light`、`a dark wooden gavel`、
`a single sheet of heavy cream paper lying flat on a small wooden table, seen edge-on, print not readable`（結婚證書）、`a thin stack of white papers, held so only the backs or edges show`（離婚申請）。
第 36、37 集劇本另有「螺絲起子」「點火鈕」兩句標「待加進 `cast.json`」。

## 2026-11-12 稽核後補（`../review/2026-11-12-ref-audit-e001-e020.md`）

- **道具圖帶手**（定案 12）：手對不上的鏡不傳道具圖，只寫道具句。
  - `half-pill` 畫著一根光指尖，第 11 集 c01、c21 是 Brandt 戴藍手套的手，不傳。
  - `knit-hat` 畫著 Peg 拿針的兩隻手，只給她在織的鏡。
  - `nora-suitcase` 旁邊站著一雙穿黑長褲的腿，拍到 Nora 腿腳的鏡不傳。
- **`camel-coat` 重畫**（第二批）：`a camel wool coat with deep pockets, worn open by a slender young woman over a cream knit sweater and blue jeans, seen from the front from the collarbones to the knees, her head out of the frame; the coat reaches her knees, the deep front pockets at her hips.`（第 11–19 集是毛衣配牛仔褲。）
- **`peg-knitting`**：第 11 集的長度是 `about as long as her hand`，跟本表「前臂長」那張不同，第 11 集不傳。
- **`canvas-tote`**：圖裡背在開襟衫上，穿 `coat` 的鏡不傳。
- **`grant-phone`**：螢幕上沒有字；第 3 集的訊息是後製浮在手機旁的泡泡，不在螢幕上（`cast.json` 已改）。
- **`fisk-watch`**：已加進 `cast.json`，句子是 `a plain silver wristwatch on his left wrist, its face turned toward him`。
- **`half-pill` 沒有參考圖**（2026-11-12）：試了四次都畫成整顆、兩半連著或兩顆，前後是 p1、p3、p6、p7 剪半修圖。所以不傳道具圖，每鏡只寫道具句；藥的大小與「a medicine pill, not a device」已經寫在句子裡。
