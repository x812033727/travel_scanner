# Till the Verdict Do Us Part｜第一季人物參考圖計畫（定妝照與全身照）

2026-11-12 寫。第一季（第 1–60 集）每一個要露臉的人、每一套要參考圖的造型，排成一張表，照「第一次需要這張臉的集」排；
後面是兩個種子的估價與每輪 ≤ 12 張的批次。**還沒花錢，也還沒建 manifest**：開跑前要站主點頭報價，manifest 照下面的提示詞擴充
`screen-test/build.py`（另開一張票做）。

依據：`cast.json`（`characters`、`shot_looks`、`extras`）、`assets/refs/README.md`（已有的 7 張人物圖）、`screen-test/README.md`（r1–r3 的做法與教訓）、
`docs/videos/drama/WRITING.md` 第十一節、六份 `s1-bible-e0*.md` 的〈人物與參考圖〉、`s1-decisions-e021-e060.md`（站主 2026-11-12「照你建議」），
以及 `docs/videos/till-the-verdict-e001`…`e040/script.md` 的〈五張清單〉「本集需要的參考圖」（第 41–60 集還沒有劇本，照 bible）。

## 怎麼畫（照試鏡 r1–r3）

- **工具**：Qwen-Image-Edit（`h3.sh images --detached`，`lora: false`、20 步、CFG 4），一個人或一套造型畫兩個種子，跟原圖並排標名字讓站主挑。
- **新的人（胸像）**：image 1 是一張空白的中灰畫布、`latent: empty`、1248×1664（照 `build.py r1`）。**不要拿別人的定妝照當 image 1**：臉、衣服、疤都會被抄（`minimax-h3-colab/references/lessons.md` 第 9 節）。
- **同一個人換造型（胸像）**：image 1 是鎖定的那張、`latent: image1`、只寫「Change only …」（照 `build.py r2`），臉才會是同一個人。
- **全身照**：bible 寫「從定妝照 `latent: image1`，只換衣服」，但 `latent: image1` 會守住原圖的構圖（r2 三張換裝都還是胸像），從胸像畫不出全身。所以：
  每個人的**第一張全身照**用鎖定的胸像當 image 1、`latent: empty`、1088×1920（像素數跟 1248×1664 一樣，一張的時間相同）；
  **之後的造型**用那張選定的全身照當 image 1、`latent: image1`、只換衣服（Nora 以 `discharge` 全身為基準）；只改一處的（頭髮放下、拿掉圍裙）寫 exactly one change。
  第一輪的 `night-coat` 就是這個做法的試驗：臉跑掉就改用 lessons 第 9 節的兩張圖做法（先畫對人、裁胸口以上當 image 1、原胸像當 image 2）。
- **參考圖會蓋過文字**（r3、WRITING 第十一節）：每張都是平靜、嘴閉著、嘴角平、不帶道具、灰底。r3 修的兩件事每張驗收都要看：**有沒有笑**（Grant 閉嘴微笑）、**皮膚上有沒有紅點紅痕**（Nora 頰與頸）。
  有的那張不選；兩張都有，就照 r3 在比較好的那張上寫 exactly one change 修，不重寫提示詞。
- **胸像只寫頭肩看得到的東西**：`build.py` 的 `bust()` 會拿掉 shoes、boots、trousers、hands、pocket、gloves 等字（會把鏡頭拉成全身）；
  `bust()` 漏掉的 pants、khakis、forearms、fingers、wrist、tool belt 這張表另外拿掉了（備註寫「外貌句刪」），整段被 `bust()` 吃掉的制服（副警長、急救員、藥師、店員、Gus）改寫成只剩上衣。
- **全身照寫鞋**；外貌句沒寫鞋的（Nora `gown`、Elias 三套）補上。全身照只給中景、全景用：**特寫不給全身照**，否則畫面旁邊會多站一個全身的同一人（lessons 第 6 節，種田第 33 集）。

### 提示詞裡的縮寫

表裡的英文提示詞用下面這幾段，送出前展開成原文（前三段一字不差照 `build.py`）。

- 〔BLANK〕 = `image 1 is only a blank mid-grey canvas: take nothing from it but the plain grey backdrop.`
- 〔BUST〕 = `A tight head-and-shoulders casting portrait: the frame ends just below the collarbones and the face fills the upper half of the frame, large and sharp. Front view, looking at the camera, calm neutral expression, mouth closed, not smiling. Plain mid-grey studio backdrop. Only the head, neck and shoulders are in the frame: no hands, no legs, no feet.`
- 〔REAL〕 = `Style: a photorealistic live-action photograph for a modern American prestige TV drama, shot on a cinema camera with an 85mm lens, natural soft key light, realistic skin with fine pores and natural texture, realistic hair and fabric, shallow depth of field. Not a painting, not 3D CG, not anime, not a cartoon. The picture fills the whole frame edge to edge: no black bars, no letterbox, no border. Clean image with nothing written anywhere, no watermark, no logo, no signature.`
- 〔LOOK〕 = `Edit image 1: keep the face, skin, hairstyle unless this look changes it, the framing, the plain grey backdrop and the lighting exactly the same. Change only what differs in this look:`（`build.py r2` 原句）；句末接外貌句，再接 `Calm neutral expression, mouth closed, not smiling; nothing in the hands.`
- 〔KEEP〕 = `Keep everything else exactly as in image 1: the same face and identity, eyes, hairstyle, clothes, framing, plain grey backdrop and lighting.`（`build.py r3` 原句）
- 〔KEEPFULL〕 = `Keep everything else exactly as in image 1: the same face and identity, eyes, clothes, shoes, pose, full-length framing, plain grey backdrop and lighting.`
- 〔FULL〕 = `A full-length casting photograph in a vertical frame: the whole figure from the top of the head to the soles of the shoes is in the frame, standing straight on a plain mid-grey studio floor, front view, looking at the camera, calm neutral expression, mouth closed, not smiling. Plain mid-grey seamless studio backdrop. Arms relaxed at the sides, both hands open and empty, holding nothing: no bag, no props. The face is clearly lit and sharp.`
- 〔FACE1〕 = `Take only the face, identity, eyes, skin and age from image 1: exactly the same person. The hair, clothes and shoes are only as written here; take nothing else from image 1.`

## 人物與造型總表

優先：**已有** = `assets/refs/` 已經有、不用畫；**P0** = 第 1–10 集開拍前一定要有；**P1** = 第 11–20 集；**P2** = 第 21–40 集；**P3** = 第 41–60 集（還沒有劇本，照 bible）；**選** = 建議但可省。
「第一次露臉說話的集」：用模型原聲，開口前一定要有臉；先露臉、晚一點才開口的寫兩個數字，表照早的那個排。備註裡的 R1–R10 是下面〈批次〉的輪次。

| 優先 | id／look | 第一次露臉說話的集 | 要畫什麼（胸像／全身） | 英文提示詞（照 cast.json 外貌句，加 build.py 的畫風、灰底、平臉、嘴閉著、不帶道具；全身照寫鞋） | 跟誰不能撞臉 | 備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 已有 | `nora`（基本款）`nora-portrait.jpg` | 1 | 胸像 | 已有（r3 `nora-portrait-fix-b`，紅痕已去掉） | Fiona（第 57 集，見 `henley-down`） | 全季每一鏡的臉；Nora 所有全身照與 `hospital`、`nineteen` 都從它出。 |
| 已有 | `peg`（基本款＝`visit`）`peg-portrait.jpg` | 1 | 胸像 | 已有（r1 `peg-a`） | Bev、Dr. Brandt、Gus、Rosa | 眼鏡戴在臉上；直的短灰髮往一邊梳。 |
| 已有 | `grant`（基本款）`grant-portrait.jpg` | 1 露臉（電視廣告）／3 開口 | 胸像 | 已有（r3 `grant-portrait-fix-b`，平臉） | Elias、Fisk、Crane、Lyle | 第 1 集電話與電視是 Gemini Algieba；第 3 集起原聲。 |
| P0 | `cole` | 1 | 胸像 | 〔BLANK〕〔BUST〕He is: a 30-year-old Black American man, close-cropped hair, a black suit. He is the only person in the frame. 〔REAL〕 | 值班醫生（不同集）、發表會保全（都是黑西裝，不同集） | R1。第 1 集 c20、c21、c23 露臉說話。白手套是 `bust()` 拿掉的，寫在鏡上。 |
| 選 | `nora:pregnant` | 1 | 全身 | 〔FULL〕〔FACE1〕She is: a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, five months pregnant with a visible rounded belly, long dark chestnut hair loose past her shoulders, a loose cream cable-knit sweater dress, soft cream slippers on her feet. She is the only person in the frame. 〔REAL〕 | — | R1 第六位（加了 R1 變 12 張）。image 1 `nora-portrait.jpg`、`latent: empty`、1088×1920。bible 沒列；直式小樣只給定妝照，臉與懷孕的身形都守住了，所以可省。 |
| P0 | `nora:night-coat` | 2 | 全身 | 〔FULL〕〔FACE1〕She is: a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, five months pregnant, long dark chestnut hair loose and wet from rain, a loose cream cable-knit sweater dress under an open camel wool coat, soft cream slippers on her feet, her clothes clean and dry under the coat. She is the only person in the frame. 〔REAL〕 | — | R1，bible 第 1–3 集先畫第一位。image 1 `nora-portrait.jpg`、`latent: empty`、1088×1920；也是「從胸像畫全身」的試驗。外貌句的 "pain only in her face and posture" 不寫（定妝照是平臉）。 |
| P0 | `nora:hospital` | 2 | 胸像 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face, pale and tired, long dark chestnut hair loose and slightly tangled, a faded white hospital patient gown with a small pale blue diamond print, a round snap neckline and short sleeves, under a cream cardigan, no makeup. She is the only person in the frame. 〔REAL〕 | — | R1。image 1 `nora-portrait.jpg`、`latent: image1`、1248×1664。第 2–5 集（第 3 集清單：從修好的圖出）。在床上多半是胸上，所以畫胸像；病人服不露腿。 |
| P0 | `dr-brandt` | 2 | 胸像 | 〔BLANK〕〔BUST〕She is: a 48-year-old white German-American woman, short silver-blond bob, rectangular glasses, a white doctor's coat over navy scrubs. She is the only person in the frame. 〔REAL〕 | Peg（戴眼鏡的短髮白人女性；第 11–12 集不同框）、書記官（不同集） | R1。第 2、11、12、33 集原聲。方框眼鏡。 |
| P0 | `nurse-kim` | 2 | 胸像 | 〔BLANK〕〔BUST〕She is: a Korean-American woman around 30, pale blue scrubs, short black hair tucked behind her ears, a round kind face, gentle eyes. She is the only person in the frame. 〔REAL〕 | Theo（都是韓裔，不同集） | R1。第 2–3 集原聲。 |
| P0 | `grant:rain` | 3 | 胸像 | 〔LOOK〕 a 37-year-old white American man, good-looking in a polished way, sandy-blond hair side-parted and damp, clean-shaven, thin round metal-rim glasses with drops on the lenses, a light stone-colored suit with a wet collar. He is the only person in the frame. 〔REAL〕 | Elias（細金屬框眼鏡、灰西裝） | R2。image 1 `grant-portrait.jpg`、`latent: image1`（第 3、4 集清單：只換頭髮與鏡片）。第 3–5、18–19 集。驗收：嘴角平，不能回到 r1 的微笑。 |
| P0 | `on-call-doctor` | 4 | 胸像 | 〔BLANK〕〔BUST〕He is: a 45-year-old Black American man, a shaved head, a short greying beard, no glasses, a white doctor's coat over light grey scrubs. He is the only person in the frame. 〔REAL〕 | Cole（不同集）、警探（都是光頭，不同集） | R2。第 4 集四鏡原聲。夾板不畫。 |
| 已有 | `peg:coat` `peg-coat.jpg` | 5 | 胸像 | 已有（r2 `peg-coat-a`） | Bev | 第 5、8、9、11–19 集出門。 |
| P0 | `nora:discharge` | 6 | 全身 | 〔FULL〕〔FACE1〕She is: a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face, pale and tired, no makeup, long dark chestnut hair loose and slightly tangled, a loose cream cable-knit sweater dress hanging straight to below the knee, grey soft slippers on her feet. She is the only person in the frame. 〔REAL〕 | — | R2。image 1 `nora-portrait.jpg`、`latent: empty`、1088×1920。**Nora 不懷孕的全身基準**：之後的造型都在選定的這張上換衣服。大衣是道具句，不畫進圖。 |
| P0 | `fisk` | 6 | 胸像 | 〔BLANK〕〔BUST〕He is: a 52-year-old white American man, slicked-back grey-brown hair, a sharp grey suit, gold-rimmed glasses. He is the only person in the frame. 〔REAL〕 | Grant、Elias、主持離婚的法官、Wexler | R2。第 6–7、20、42–43 集原聲。金框眼鏡；鋼筆與錶是道具句。 |
| P0 | `sienna` | 6 | 胸像 | 〔BLANK〕〔BUST〕She is: a 27-year-old Indian-American woman, striking, warm brown skin, a sharp jet-black chin-length bob, bold red lipstick, a bright red tailored pantsuit with a modest neckline. She is the only person in the frame. 〔REAL〕 | 副警長（都是深膚色深髮）、Dana、旗艦店店員 | R2。第 6–7、22、26、28 集原聲。外貌句刪：左腕的錶（胸像看不到，全身照才畫）。 |
| P0 | `deputy` | 6 | 胸像 | 〔BLANK〕〔BUST〕She is: a 40-year-old Latina woman, dark hair in a tight low bun, a tan shirt of a plain sheriff's deputy uniform, a plain star-shaped badge and shoulder patches with no readable text. She is the only person in the frame. 〔REAL〕 | Sienna（第 6 集台階那場不拍 Sienna 的臉） | R2。第 6 集原聲。`bust()` 會把整段制服吃掉（同一段有 trousers），改寫成只剩上衣；不入鏡武器。 |
| P0 | `sienna`（全身） | 6 | 全身 | 〔FULL〕〔FACE1〕She is: a 27-year-old Indian-American woman, striking, warm brown skin, a sharp jet-black chin-length bob, bold red lipstick, a slim gold watch on her LEFT wrist, clearly visible, a bright red tailored pantsuit with a modest neckline, pointed heels. She is the only person in the frame. 〔REAL〕 | 同上 | R3。image 1 選定的 Sienna 胸像、`latent: empty`、1088×1920。bible 要「看得到左腕的錶」：胸像看不到手，所以另畫全身。 |
| P0 | `installer-lead` | 6 露臉（不說話） | 胸像 | 〔BLANK〕〔BUST〕He is: a white American man in his forties, a short red beard, a grey knit cap, plain grey work overalls with no lettering. He is the only person in the frame. 〔REAL〕 | — | R3。第 6–9、50 集唯一露臉的工人。另一個工人（`installers`）不畫。 |
| P0 | `bev` | 9 | 胸像 | 〔BLANK〕〔BUST〕She is: a 55-year-old white American woman, a round soft face with rosy cheeks, short curly auburn-grey hair, a bright floral blouse, reading glasses hanging on a beaded chain against her chest. She is the only person in the frame. 〔REAL〕 | **Peg**（六十歲上下的白人女性；不並排正臉） | R3。第 9、12、14–16、19–20 集原聲。眼鏡掛胸前、圓臉、赤褐髮，跟 Peg 分開。 |
| P1 | `dale` | 11 | 胸像 | 〔BLANK〕〔BUST〕He is: a 40-year-old white American man, thick black-framed glasses, a white pharmacist's coat. He is the only person in the frame. 〔REAL〕 | Theo、Grant、Elias、Fisk（都戴眼鏡） | R3。第 11–13 集原聲（`cast.json` 寫 12–13，以 bible 與第 11 集劇本為準）。`bust()` 會因 pocket 吃掉藥師袍，改寫；兩支筆是道具。 |
| P1 | `nora:motel` | 11 | 全身 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, long dark chestnut hair in a loose low knot, a cream knit sweater, blue jeans, flat tan ankle boots. She is the only person in the frame. 〔REAL〕 | — | R3。image 1 選定的 `discharge` 全身、`latent: image1`。第 11–19 集（剪髮前）。 |
| P1 | `detective` | 14 | 胸像 | 〔BLANK〕〔BUST〕He is: a 50-year-old Samoan-American man, broad build, a shaved head, a neat black goatee, a grey sport coat over a navy polo shirt. He is the only person in the frame. 〔REAL〕 | Reyes（電話兩頭，不同框）、值班醫生（都是光頭，不同集） | R3。第 14 集原聲。沒有徽章、沒有槍套。 |
| P1 | `reyes` | 14 | 胸像 | 〔BLANK〕〔BUST〕He is: a 45-year-old Mexican-American man, close-cropped black hair greying at the temples, a dark navy suit, white shirt. He is the only person in the frame. 〔REAL〕 | 警探、急救員、Ashford 的技師（不同集） | R4。第 14、53 集原聲。 |
| P1 | `pawnbroker` | 15 | 胸像 | 〔BLANK〕〔BUST〕He is: a 60-year-old Vietnamese-American man, thinning grey hair combed back, a lined face, a grey cardigan over a checked flannel shirt. He is the only person in the frame. 〔REAL〕 | — | R4。第 15、35 集原聲。放大鏡是道具。 |
| P1 | `bank-teller` | 15 | 胸像 | 〔BLANK〕〔BUST〕She is: a 26-year-old Black American woman, natural hair in a short rounded puff, small gold stud earrings, a plain navy blazer over a white blouse. She is the only person in the frame. 〔REAL〕 | Dana（不同集） | R4。第 15 集原聲。 |
| 已有 | `elias`（基本款）`elias-portrait.jpg` | 15 露臉／16 開口 | 胸像 | 已有（r1 `elias-a`） | Grant、Fisk、Sparks | 頭髮往後梳。第 2、10 集不露臉。 |
| P1 | `elias`（全身，基本款） | 15 | 全身 | 〔FULL〕〔FACE1〕He is: a 34-year-old Italian-American man, handsome, about 188 cm tall, lean with straight shoulders, olive skin, dark brown hair combed straight back from the forehead, short at the sides, dark brown eyes, a defined jaw, thin silver wire-framed glasses, a charcoal three-piece suit with a faint windowpane check, a white shirt open at the collar, no tie, a white pocket square, black leather shoes. Exception to the frame above: his left hand is in his left trouser pocket; his right hand hangs empty at his side. He is the only person in the frame. 〔REAL〕 | Grant（同框只在中景以上）、Fisk | R4。image 1 `elias-portrait.jpg`、`latent: empty`、1088×1920。**跟 bible 不同**：第 11–20 集 bible 寫「穿大衣」，但 2026-11-12 對齊後大衣是道具句（`elias-overcoat`），圖裡有大衣會蓋過「沒有大衣」的鏡（第 20、26–30 集），所以不畫大衣。左手插口袋：第 60 集前左手一律不露。 |
| P1 | `theo` | 15 虛焦／16 開口 | 胸像 | 〔BLANK〕〔BUST〕He is: a 29-year-old Korean-American man, neat black hair, round tortoiseshell glasses, a light blue button-down shirt under a grey knit sweater vest. He is the only person in the frame. 〔REAL〕 | Ray（三十歲上下的亞裔男性，不同框）、Nurse Kim | R4。第 16 集起原聲、面無表情。外貌句刪：khakis。平板是道具。 |
| P1 | `dana` | 17 | 胸像 | 〔BLANK〕〔BUST〕She is: a 35-year-old Black Nigerian-American woman, deep brown skin, dark brown eyes, hair in a neat high bun, a fitted black blazer over a white T-shirt. She is the only person in the frame. 〔REAL〕 | Sienna、銀行行員、Fiona、發表會保全 | R4。第 17 集起原聲。卷宗是道具。 |
| P1 | `clerk` | 19 | 胸像 | 〔BLANK〕〔BUST〕She is: a 45-year-old white American woman, short sandy-brown hair, small silver earrings, a navy cardigan over a pale blue blouse. She is the only person in the frame. 〔REAL〕 | Dr. Brandt（不同集） | R5。只說 "Filed."（第 19 集；`cast.json` 寫 20，以 bible 為準）。 |
| P1 | `nora:motel-down` | 19 | 全身 | Edit image 1. Exactly one change: her hair is out of the low knot, long dark chestnut hair loose past her shoulders. 〔KEEPFULL〕 She is the only person in the frame. 〔REAL〕 | — | R5。image 1 選定的 `motel` 全身、`latent: image1`。第 19 集新開。 |
| P1 | `nora:shoulder` | 19 | 全身 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, dark chestnut hair cut to a clean shoulder-length bob, a cream knit sweater, dark trousers, flat tan ankle boots. She is the only person in the frame. 〔REAL〕 | — | R5。image 1 `discharge` 全身、`latent: image1`。第 19 集剪髮後起，到第 49 集。 |
| P1 | `nora:decree` | 20 | 全身 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, dark chestnut hair cut to a clean shoulder-length bob, an ivory fine-knit sweater with a modest round neckline, pale grey tailored trousers, low nude flat shoes. She is the only person in the frame. 〔REAL〕 | — | R5。image 1 `discharge` 全身、`latent: image1`。第 20–21 集。 |
| P1 | `judge` | 20 | 胸像 | 〔BLANK〕〔BUST〕He is: a 64-year-old white American man, short white hair, a trimmed white beard, no glasses, a black judicial robe over a white shirt and dark tie. He is the only person in the frame. 〔REAL〕 | Fisk（法官的鏡不帶 Fisk）、Wexler | R5。第 20、42 集原聲。 |
| P1 | `wedding-judge` | 20 | 胸像 | 〔BLANK〕〔BUST〕She is: a 52-year-old Filipino-American woman, black hair in a low chignon, small pearl earrings, a black judicial robe. She is the only person in the frame. 〔REAL〕 | 主持離婚的法官（同一集，要一看就是不同人） | R5。第 20 集原聲。 |
| P2 | `elias:turtleneck` | 21 | 全身 | 〔LOOK〕 a 34-year-old Italian-American man, handsome, about 188 cm tall, lean with straight shoulders, olive skin, dark brown hair combed straight back from the forehead, short at the sides, dark brown eyes, a defined jaw, thin silver wire-framed glasses, a black merino turtleneck and charcoal trousers, black leather shoes. He is the only person in the frame. 〔REAL〕 | Grant | R6。image 1 選定的 Elias 全身、`latent: image1`（左手留在口袋）。第 21 集最後、22、24–25、49 集。 |
| P2 | `store-clerk` | 23 | 胸像 | 〔BLANK〕〔BUST〕She is: a 23-year-old white American woman, platinum-blonde hair in a sleek low ponytail, light grey eyes, a fitted black shirt. She is the only person in the frame. 〔REAL〕 | Sienna（不同集） | R6。第 23 集原聲。`bust()` 會吃掉整段上衣（同一段有 trousers），改寫；名牌不畫。定妝照不笑，招呼時的閉嘴笑寫在鏡上。 |
| P2 | `nora:gown` | 24 | 全身 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, dark chestnut shoulder-length hair smoothed back behind her ears, a misty-grey floor-length gown with a modest high boat neckline and long sleeves, plain grey closed low-heeled shoes just visible under the hem. She is the only person in the frame. 〔REAL〕 | — | R6。image 1 `discharge` 全身、`latent: image1`。第 24 集鏡前、25–30 集。外貌句沒寫鞋，補上。手拿包、白棉手套、Elias 的戒指寫在鏡上。 |
| P2 | `crane` | 26 | 胸像 | 〔BLANK〕〔BUST〕He is: a 61-year-old white American man, short and stocky, a ruddy face, a dark band-collar jacket. He is the only person in the frame. 〔REAL〕 | Grant、Lyle（白人男性；臉的鏡一鏡一人） | R6。第 26、28–29 集原聲；大笑寫在鏡上，定妝照不笑。籌碼是道具。 |
| P2 | `lyle` | 26 露臉／29 開口 | 胸像 | 〔BLANK〕〔BUST〕He is: a 30-year-old white American man, a plaid shirt, a backwards plain baseball cap. He is the only person in the frame. 〔REAL〕 | Crane、Grant、Sparks | R6。第 29、46–47、57 集原聲。相機、手機、口香糖不進圖。 |
| P2 | `launch-guard` | 27 | 胸像 | 〔BLANK〕〔BUST〕He is: a 45-year-old Native American man, broad-shouldered, long black hair tied low at the nape, a plain black suit and white shirt, a clear coiled earpiece. He is the only person in the frame. 〔REAL〕 | Cole（都是黑西裝，不同集）、Dana（不同集） | R6。第 27 集 "Mr. Ashford."（原聲）。沒有徽章字、沒有武器。 |
| P2 | `ray` | 27 露臉（第一季不說話） | 胸像 | 〔BLANK〕〔BUST〕He is: a 30-year-old Filipino-American man, a black T-shirt, a headset microphone. He is the only person in the frame. 〔REAL〕 | Theo（不同框） | R7。第 27–28 集只在燈控室。外貌句刪：cargo pants、手腕的膠帶（寫在鏡上）。 |
| P2 | `walter` | 28 | 胸像 | 〔BLANK〕〔BUST〕He is: a 55-year-old Italian-American man, grey stubble, fine lines around his eyes from furnace heat, a heavy leather apron over a work shirt. He is the only person in the frame. 〔REAL〕 | Elias（**不要**刻意畫得像他）、Gus | R7。第 28 集回憶，原聲兩句。外貌句刪 "(flashback only)"；粗手是 `bust()` 拿掉的。 |
| P2 | `nora:nineteen` | 28 | 胸像 | 〔LOOK〕 she is twelve years younger: a 19-year-old white Irish-American girl, slender, fair skin with faint freckles, soft grey-green eyes, long dark chestnut hair in a high ponytail, a faded misty-grey T-shirt and a too-big leather apron, safety goggles on her forehead. She is the only person in the frame. 〔REAL〕 | Walter（回憶只有這兩人） | R7。image 1 `nora-portrait.jpg`、`latent: image1`（第 21–30 集 bible：先試 image1 加「十九歲」，不像再從灰底單獨畫）。第 28、31、34 集回憶；站主 2026-11-12 定：畫，T 恤霧灰色。 |
| P2 | `gus` | 31（只露下巴與嘴）／32 露臉 | 胸像 | 〔BLANK〕〔BUST〕He is: a 70-year-old Italian-American man, stooped, a bald crown with white hair at the sides, small steel reading glasses low on his nose, a sleeveless white undershirt. He is the only person in the frame. 〔REAL〕 | Peg（第 37 集同框，寫清楚分得開的地方）、Walter | R7。bible 第 31–40 集「必須最先畫」；第 31 集 c40 "Who's there?" 就用到。`bust()` 會連 undershirt 一起刪（同一段有 trousers），補回；不寫疤（細疤會畫成紅點）。爐邊的圍裙、手套、面罩是道具。 |
| P2 | `grant:young` | 31 | 胸像 | 〔LOOK〕 he is twelve years younger: a 25-year-old white American man, sandy-blond side-parted hair, clean-shaven, thin round metal-rim glasses, the same pair as in image 1, a cheap grey suit with a plain dark lanyard whose card is tucked inside the jacket, out of sight. He is the only person in the frame. 〔REAL〕 | 現在的 Grant（要認得出是同一人）、十九歲的 Nora（同框一鏡就好） | R7。image 1 `grant-portrait.jpg`、`latent: image1`。第 31 集回憶，以後幾季也用。識別證寫成收進外套，免得畫出字。 |
| P2 | `nora:work`（全身） | 33 | 全身 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, dark chestnut shoulder-length hair tied in a low ponytail, clear safety goggles pushed up on her head, a dark canvas work apron over a grey henley with long sleeves, dark work trousers, sturdy boots. She is the only person in the frame. 〔REAL〕 | Fiona（都綁低馬尾；不同框） | R7。image 1 `discharge` 全身、`latent: image1`；選的時候跟 `nora-work.jpg` 並排看臉與頰（r3 a 兩頰帶一點紅，這張不能更紅）。第 33–60 集在 Remelt 裡。 |
| 已有 | `nora:work` `nora-work.jpg` | 33 | 胸像 | 已有（r3 `nora-work-fix-a`） | Fiona | 近景與特寫用這張，不用全身照。 |
| P2 | `sparks` | 33 | 胸像 | 〔BLANK〕〔BUST〕He is: a 20-year-old Italian-American young man, buzz cut, a small silver stud earring, a black T-shirt. He is the only person in the frame. 〔REAL〕 | Hank（都是平頭，不同框）、Lyle、Elias、Cole | R8。第 33 集起原聲；可以露齒笑的只有他（寫在鏡上）。外貌句刪：grey work pants、前臂的隔熱護套（寫在鏡上）。 |
| P2 | `nora:henley` | 33 | 全身 | Edit image 1. Exactly one change: the dark canvas work apron and the clear safety goggles are gone; she wears only the grey henley with long sleeves over dark work trousers and sturdy boots, her hair still in the low ponytail. 〔KEEPFULL〕 She is the only person in the frame. 〔REAL〕 | — | R8。image 1 選定的 `work` 全身、`latent: image1`（bible 寫從 `nora-work.jpg`，那是胸像，改從全身照）。第 33–40 集出門。 |
| P2 | `ashford-tech` | 37 | 胸像 | 〔BLANK〕〔BUST〕He is: a 38-year-old Mexican-American man, short black hair, a neatly trimmed moustache, a plain navy work jacket with no lettering. He is the only person in the frame. 〔REAL〕 | Reyes（不同集） | R8。第 37 集原聲。外貌句刪：tool belt（寫在鏡上）。 |
| P2 | `fiona` | 38 | 胸像 | 〔BLANK〕〔BUST〕She is: a 40-year-old Chinese-American woman, sleek black hair in a low ponytail, a white shirt under a navy blazer. She is the only person in the frame. 〔REAL〕 | Nora（第 57 集）、Dana | R8。第 38、40、46、54、56–57 集原聲。識別證、規格夾、錶是道具。 |
| P2 | `hank` | 38 | 胸像 | 〔BLANK〕〔BUST〕He is: a 50-year-old white American man, buzz cut, a grey work jacket. He is the only person in the frame. 〔REAL〕 | Sparks（不同框） | R8。第 38–39 集原聲。外貌句刪：指縫的白沙（寫在鏡上）；「不看人」寫在每鏡，定妝照照樣看鏡頭。 |
| P3 | `wexler` | 43 | 胸像 | 〔BLANK〕〔BUST〕He is: a 58-year-old Black American man, close-cropped grey hair, a neat short grey moustache, thin black half-rim reading glasses, a brown herringbone tweed waistcoat over a white shirt with a dark green knit tie. He is the only person in the frame. 〔REAL〕 | Fisk、主持離婚的法官（原本的白人灰髮會撞，已改） | R8。第 43 集原聲。外貌句站主 2026-11-12 照建議定案。 |
| P3 | `nora:home` | 44 | 全身 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, dark chestnut shoulder-length hair tied in a low ponytail, a soft heather-grey long-sleeve cotton top, loose charcoal lounge trousers, grey wool socks on her feet, no shoes. She is the only person in the frame. 〔REAL〕 | — | R9。image 1 `discharge` 全身、`latent: image1`。第 44–45 集 Ashford 家的夜裡。 |
| P3 | `talk-host` | 45 | 胸像 | 〔BLANK〕〔BUST〕She is: a 46-year-old white American woman, glossy honey-blonde shoulder-length blowout, a cobalt-blue sleeveless sheath dress with a modest neckline, small gold hoop earrings. She is the only person in the frame. 〔REAL〕 | — | R9。第 45 集原聲加電視濾波（站主 2026-11-12 照建議：拍攝影棚）。 |
| P3 | `rosa` | 46（最後一鏡）／47 | 胸像 | 〔BLANK〕〔BUST〕She is: a 63-year-old Italian-American woman, sturdy and broad-shouldered, olive skin, very short cropped salt-and-pepper hair, more black than grey, close to her head, thick dark eyebrows, dark brown eyes, deep lines at the corners of her eyes, no glasses, a deep wine-red cotton shirt with the sleeves rolled up under a stained white apron. She is the only person in the frame. 〔REAL〕 | **Peg**（不同場；不戴眼鏡、橄欖膚色、短到貼頭的頭髮是分得開的地方）；Elias（母子，像是好事） | R9。第 46–47、49、59 集原聲。外貌句刪：右腕的銀鐲（寫在鏡上）；湯勺是道具。 |
| P3 | `process-server` | 50 | 胸像 | 〔BLANK〕〔BUST〕He is: a 38-year-old Middle Eastern-American man, short dark hair, a neatly trimmed dark beard, a plain navy windbreaker over a grey polo shirt. He is the only person in the frame. 〔REAL〕 | — | R9。第 50 集一句原聲。 |
| P3 | `nora:blazer` | 53 | 全身 | 〔LOOK〕 a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face with natural light makeup, dark chestnut hair cut to a clean shoulder-length bob, a dark navy linen blazer over a cream knit top, dark trousers, flat tan ankle boots. She is the only person in the frame. 〔REAL〕 | — | R9。image 1 `discharge` 全身、`latent: image1`。第 53 集。 |
| P3 | `emt` | 54 | 胸像 | 〔BLANK〕〔BUST〕He is: a 35-year-old Latino man, close-cropped black hair, a short trimmed beard, a plain navy blue EMT uniform shirt with shoulder patches that carry no readable text. He is the only person in the frame. 〔REAL〕 | Reyes（都是拉丁裔男性，不同集） | R9。第 54 集 "Back spasm. Rest."。`bust()` 會吃掉整段制服（同一段有 trousers），改寫成只剩上衣。 |
| 已有 | `elias:furnace` `elias-furnace.jpg` | 55 | 胸像 | 已有（r2 `elias-furnace-a`） | Sparks、Grant | 近景用；第 58 集脫右手套、第 60 集脫左手套的鏡用這張，不用戴手套的全身照。 |
| P3 | `elias:furnace`（全身，戴手套） | 55 | 全身 | 〔LOOK〕 a 34-year-old Italian-American man, handsome, about 188 cm tall, lean with straight shoulders, olive skin, dark brown hair combed straight back from the forehead, short at the sides, dark brown eyes, a defined jaw, thin silver wire-framed glasses, a plain black short-sleeved T-shirt, a brown leather work apron, dark work trousers, sturdy boots, a pair of thick grey heat-resistant work gloves reaching halfway up his forearms, on both his hands; his left hand comes out of the pocket and both gloved hands hang relaxed at his sides, empty. He is the only person in the frame. 〔REAL〕 | Grant（第 60 集只用深的雙人鏡）、Sparks | R10。image 1 選定的 Elias 全身、`latent: image1`（bible 寫從 `elias-furnace.jpg`，那是胸像，改從全身照；衣服對照 `elias-furnace.jpg`）。手套是 bible 指定的（`heat-gloves` 道具句）；疤**不**進任何參考圖（第 60 集的插鏡另驗靜圖）。 |
| P3 | `nora:henley-down` | 57 | 全身 | Edit image 1. Exactly one change: her hair is out of the ponytail, dark chestnut hair cut to a clean shoulder-length bob, worn loose. 〔KEEPFULL〕 She is the only person in the frame. 〔REAL〕 | Fiona（頭髮放下就跟她的低馬尾分開） | R10。image 1 選定的 `henley` 全身、`latent: image1`。第 57 集；橄欖色工作外套是道具句。 |

**數量**：表上 63 列，其中已有 7 張（Nora、Nora `work`、Elias、Elias `furnace`、Grant、Peg、Peg `coat`）；**要畫 55 個**（新的人胸像 35、同一人換造型的胸像 4、全身 16），另有可省的 1 個（Nora `pregnant` 全身）。
P0 有 14 個（第 1–10 集），P1 15 個，P2 17 個，P3 9 個（Wexler 起）。

### 不畫的人

- 只拍背影、手、虛焦或剪影：Elias 的 `soot`（第一季不露清楚的臉）、`installers`（另一個工人）、`police-officer`、`clinic-assistant`、`gift-shop-owner`、`court-gallery`、`shoppers`、
  `launch-host`、`launch-usher`、`launch-guests`、`reporters`、`press-pack`、`stagehands`、`waiting-mother`、`emt-partner`、`pr-man`、`ferry-crowd`；第 2–5 集的護理師群眾。
- 只有聲音：`dispatcher`、`phone-recording`、`supplier-phone`。
- 第一季不入鏡：Claire Quinn（第 40 集照建議不拍，Nora 自己念那句）；Judith Hale、Douglas Penrose（第二季以後，用到時再畫）。
- 第一季沒用到的造型：Sienna `yellow`（六份 bible 與四十集劇本都沒有排到）。
- 沒排全身照：Grant、Peg 與所有配角（bible 沒要；全景照外貌句寫鞋）。要是第一批草稿出現光腳或鞋子亂換，再補該人的全身照。
- 不是人：第 60 集疤的插鏡靜圖（`s1-decisions` 第 6 章第 9 條，約 0.5 CU）、道具與場景圖，各自另列。

### 戴眼鏡的人（每張圖、每一鏡都寫是哪一副）

Grant 細圓金屬框、Elias 細銀絲框、Fisk 金框、Theo 圓玳瑁框、Dale 粗黑框、Dr. Brandt 方框、Peg 玳瑁框老花（戴在臉上）、Bev 老花掛胸前珠鍊、Gus 小鋼框老花低在鼻樑、Wexler 黑色細半框。
其他人都不戴；驗收時多一副或換了框都不選。

## 批次（每輪 ≤ 12 張，兩個種子）

照第一次需要的集排；後一輪要用前一輪選定的圖（全身基準、換造型）時，那一輪要等站主挑完才建 manifest。種子接著 r3 從 714000 起，每張加一。

| 輪 | 內容（每個兩張） | 張數 | 依賴 | 約 CU |
| --- | --- | --- | --- | --- |
| R1 | Cole、Nora `night-coat` 全身、Nora `hospital`、Dr. Brandt、Nurse Kim（＋選：Nora `pregnant` 全身） | 10（12） | 無 | 2.7（3.2） |
| R2 | Grant `rain`、值班醫生、Nora `discharge` 全身、Fisk、Sienna、副警長 | 12 | 無 | 3.2 |
| R3 | Sienna 全身、工頭、Bev、Dale、Nora `motel` 全身、警探 | 12 | R2 的 Sienna、`discharge` | 3.2 |
| R4 | Reyes、當鋪老闆、銀行行員、Elias 全身、Theo、Dana | 12 | 無 | 3.2 |
| R5 | 書記官、Nora `motel-down`、`shoulder`、`decree`（全身）、主持離婚的法官、證婚的法官 | 12 | R3 的 `motel`、R2 的 `discharge` | 3.2 |
| R6 | Elias `turtleneck` 全身、旗艦店店員、Nora `gown` 全身、Crane、Lyle、發表會保全 | 12 | R4 的 Elias 全身 | 3.2 |
| R7 | Ray、Walter、Nora `nineteen`、Gus、Grant `young`、Nora `work` 全身 | 12 | R2 的 `discharge` | 3.2 |
| R8 | Sparks、Nora `henley` 全身、Ashford 的技師、Fiona、Hank、Wexler | 12 | R7 的 `work` 全身 | 3.2 |
| R9 | Nora `home` 全身、脫口秀主持人、Rosa、送達人員、Nora `blazer` 全身、急救員 | 12 | R2 的 `discharge` | 3.2 |
| R10 | Elias `furnace` 全身（戴手套）、Nora `henley-down` 全身 | 4 | R4 的 Elias 全身、R8 的 `henley` | 1.1 |
| 合計 | 55 個（＋選 1） | **110**（112） | | **約 29.3**（29.9） |

- R1–R3 的 34 張含全部 P0（14 個，第 1–10 集開拍前一定要有）與第 11–14 集的 Dale、Nora `motel`、警探；R4–R5 是第 14–20 集其餘的人；R1 也是「從胸像畫全身」的試驗，`night-coat` 的臉不對就先停，改做法再往下。
- 每輪開一個 session、跑完就停（`h3.sh images --detached … --new-session --stop-on-complete`，或先 `h3.sh start` 再 `stop`）。等站主挑圖的時候不要讓 runtime 開著：r3 那台 A100 一小時約 10 CU。
- 不必等前一輪的輪（R2、R4）可以跟前一輪排在同一天；需要選圖的輪（R3、R5–R10）先把站主的選擇記進 `assets/refs/README.md` 再建 manifest。
- 選定的圖照 `assets/refs/README.md` 的做法存成 JPEG、記種子與原 PNG 雜湊、重算 `SHA256SUMS`；原圖與兩個種子都照 `docs/videos/AI-DRAMA-DRIVE.md` 用 `todrive.sh` 傳到
  `AI/備份/AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/`，不進 repo。

## 估價

- **算法**：照 r3 實測，A100 級的 runtime 六張約 1.6 CU（含冷啟動），一張約 0.27 CU。110 張 × 1.6 ÷ 6 ≈ **29.3 CU**；加可省的 Nora `pregnant` 是 112 張、約 29.9 CU。
  全身照 1088×1920 跟胸像 1248×1664 的像素數一樣，一張的時間不變。
- **可能更少**：r3 的 1.6 CU 裡有一次冷啟動（約 9–10 分鐘）；一輪 12 張只冷啟動一次，攤下來約 21–23 CU。分到 G4 也比 A100 便宜。
- **要留的餘裕**：r3 是「挑出來仍要修一處」才定案的；照它估五個裡有一個要再修一輪（約 11 個 × 2 張），約 +6 CU。
- **建議向站主報**：約 30 CU，上限 36 CU（含修圖）。超過上限先停下來報告，不往下一輪。

## 驗收（每輪挑圖時對著表看）

1. 臉照外貌句：年齡、膚色、髮型、眼鏡是哪一副；跟「跟誰不能撞臉」那一欄的人並排看，一眼分得出來。
2. 平臉：嘴閉著、嘴角平、沒有閉嘴微笑（Grant r1 的錯）；眼睛看鏡頭。
3. 皮膚乾淨：臉頰、脖子、手腕沒有紅點、紅痕、疤（Nora r1、Elias 疤的錯）。
4. 沒有字、沒有道具：徽章、臂章、識別證、制服、衣服上都沒有字；手上沒東西（胸像看不到手）。
5. 胸像真的是胸像（臉占上半），全身照從頭到鞋都在畫面裡、鞋對；換造型的那張跟它的 image 1 是同一個人。
6. 兩張都不合格：在比較好的那張上照 r3 寫 exactly one change 修一次（兩個種子）；還不行就改做法（WRITING 第十一節「改字只改一次」），不要第三次改字。

## 跟 bible 或劇本不一樣的地方（建 manifest 的人要知道）

- **全身照的做法**：bible 寫「從定妝照 `latent: image1`」，這份改成第一張全身照 `latent: empty`、之後在全身照上 `latent: image1`（理由見〈怎麼畫〉）；`henley` 從 `work` 全身、Elias `furnace` 全身從 Elias 全身出，不是從胸像。
- **Elias 全身不畫大衣**：第 11–20 集 bible 要「穿大衣」，對齊後大衣是道具句；第 15–19 集的鏡照樣寫 `a dark charcoal wool overcoat, worn open`。
- **Nora `hospital` 畫胸像**、**Sienna 另畫一張全身**（看得到左腕的錶）：bible 沒寫，前者是場景多半在床上，後者是胸像看不到手。
- **Nora `pregnant` 全身**列為可省：bible 沒列，直式小樣證明只給定妝照也守得住。
- **出場集數以 bible 與劇本為準**：Dale 第 11 集（`cast.json` 寫 12–13）、書記官第 19 集（`cast.json` 寫 20）。`cast.json` 的這兩處要另開票改，這份不動它。
