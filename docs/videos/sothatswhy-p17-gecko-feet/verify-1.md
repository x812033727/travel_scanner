# 查核報告 1（sothatswhy-p17-gecko-feet）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-09
- 方法：逐句讀 `video.json` 的 224 句台詞（p001–p224，與 `script.md` 的 130 個場景一一對應），加上 YouTube 標題、說明與縮圖文字。對照 `claims.md` 的 C01–C21，但不採用它的引文，每個來源都重新打開讀原文：
  - PMC 全文（WebFetch 讀 pmc.ncbi.nlm.nih.gov）：Autumn 2002（PMC129431）、Hansen & Autumn 2005（PMC544316）、Hu 2012（PMC3479896）、Tian 2006（PMC1748224）、Hsu 2012（PMC3284128）、Stark 2013（PMC3631644）、Stark 2015（PMC4528608）。
  - 摘要（Europe PMC REST API，以 DOI 查）：Autumn 2000（Nature）、Autumn & Peattie 2002、Autumn 2006 Frictional adhesion、Autumn 2006 Dynamics、Stark 2012、Huber 2007、Gillies 2014、Zimin 2025；Huber 2005 由 NCBI efetch 取得摘要；SICB 會議摘要（Autumn 團隊，倒掛時的相對剪力）。
  - 其他：OpenStax Chemistry 2e 10.1、Wikipedia（Tokay gecko、Common house gecko、Gekko hokouensis、Gecko、Non-stick surface，raw wikitext）、Phys.org 2014-08 報導、亞里斯多德《動物志》D'A. W. Thompson 英譯（ellopos.net）。
- 打不開／只讀到摘要的：Autumn 2006（J. Exp. Biol.）全文要訂閱，第三方 PDF 抓回來是空的，只讀摘要與同團隊 SICB 摘要；Autumn 2000、Autumn & Peattie、Stark 2012、Huber 2007、Gillies 2014 只讀摘要。用到這幾篇的台詞，摘要都足以支撐，或在下面標出只能支撐到哪裡。
- 結論統計（台詞 224 句）：正確 213、需改 11、錯誤 0。另外標題、說明、縮圖 3 項：正確 3。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 |
| --- | --- | --- | --- | --- |
| F01 | p021（所長） | 兩千多年前，亞里斯多德就記下過壁虎爬牆的本事。 | 需改（細節走樣） | 《動物志》第九卷講啄木鳥時拿壁虎來比："It can run up and down a tree in any way, even with the head downwards, like the gecko-lizard." 他寫的是壁虎頭朝下爬**樹**，不是爬牆。Autumn & Peattie 摘要只說 "since Aristotle first recorded his observations"。改成照原文的樹，順便讓「頭朝下」呼應開場的倒掛。這個鏡頭若畫的是牆，插圖提示詞要一起改 |
| F02 | p038（所長） | 結果不差，代表主要不是靠一層水。 | 需改（小朋友會聽錯） | Autumn 2002："adhered equally well to strongly hydrophobic and strongly hydrophilic, polarizable surfaces"；全文 "was not significantly different"。原文是「兩種沒有差別」，口語「結果不差」最常被聽成「結果還不錯」。改成「差不多」 |
| F03 | p046（所長） | 不是。它少到要用很精密的儀器才找得到。 | 需改（與來源不完全一致） | Hsu 2012："Although not visible to the naked eye, we find that the geckos also leave behind footprints on glass"；腳印是把玻璃放進 98% 濕度的房間，靠水氣凝結（"differential condensation"）用數位相機拍出來的；殘留厚度 "1–2 nm"；**鑑定成分**才用到 NALDI 質譜與 SFG 光譜。所以「找到」不一定要精密儀器，「認出是什麼」才要。改成「眼睛看不到，要精密儀器才查得出是什麼」 |
| F04 | p069（所長） | 可是那麼多小扁片，就能鑽進每個小山谷， | 需改（說得太滿，與 p195–p196 打架） | Autumn & Peattie："permitting intimate contact with rough and smooth surfaces alike"，是「能貼合」，沒說每一處。Huber 2007："the effective adhesion shows a minimum for a root mean square roughness ranging from 100 to 300nm"，片中 p195–p196 也說有一種很細的粗糙最難黏。「每個小山谷」會讓小朋友記成什麼牆都貼得滿，後面又聽到「鑽不進去」。改成「許多」 |
| F05 | p070（所長） | 幾乎每個地方，都貼得上。 | 需改（同 F04） | 改成「大部分地方」，正好跟 p068「大部分地方，都差了一點點」對成一組 |
| F06 | p091（所長） | 牠的身體，比你家牆上那隻長好幾倍。 | 需改（倍數偏寬） | Wikipedia Tokay gecko："reaching a total length (including tail) of 10–12 in (25–30 cm) on average"；Common house gecko："between 7.5–15 cm"；台灣家屋常見的鉛山壁虎 *Gekko hokouensis* "snout-vent length of roughly 60 mm"（全長約十二公分）。約兩到四倍，多數情況是兩三倍；「好幾倍」常被聽成五倍、十倍。照站主觀點說成大約 |
| F07 | p158（所長） | 一開始是不太黏。可是牠只走了幾步， | 需改（實驗方式說錯） | Hansen & Autumn 全文：研究者 "manually isolating a single toe"，在光滑玻璃上 "simulated steps"，並寫 "Full strides were not used"。壁虎沒有自己走，是研究的人把牠的腳趾在玻璃上按、拉。兩次模擬踩步後力量仍少 "92.99%"；之後回復的力量 "well over the force required for an animal to support its body mass (43 g) by a single digit"，所以 p159「差不多又能撐住自己」可以留。摘要寫 "after only a few steps"，但這句接在「研究的人把粉末撒在大守宮的腳上」之後，指的就是這個實驗，要照實驗說「腳趾踩了幾下」（讓壁虎真的走的是 Hu 2012，見 p164–p165） |
| F08 | p164（所長） | 另一個研究發現，腳趾往上一捲， | 需改（跟著 F09） | 見 F09 |
| F09 | p165（所長） | 會順便把灰塵甩掉，大約四步，就回到八成左右。 | 需改（推測說成定論，說法也不對） | Hu 2012 摘要："When walking naturally with hyperextension, geckos shed dirt from their toes twice as fast as they would"；"returning their feet to nearly 80 per cent of their original stickiness in only four steps"；對照組是穿了「鞋子」、腳趾不能往上捲的壁虎，"stall[ed] at approximately 40–50% even after taking eight steps"。量到的是「腳趾能捲時，灰塵掉得快一倍」；灰塵怎麼掉，作者是用模型推測小毛突然放開的加速度把灰塵震掉（"we hypothesize that it contributes to the higher cleaning rate"），原文沒有「捲一下把灰塵甩掉」。改成只說量到的結果。「四步、八成」照留（10 隻大守宮、5–50 µm 矽砂、在乾淨玻璃上自然行走） |
| F10 | p173（所長） | 研究的人讓壁虎去爬乾的鐵氟龍， | 需改（實驗方式說錯） | Stark 2013 方法：壁虎穿兩條背帶，接在水平軌道的力量感測器上，"Maximum shear adhesive force was defined as the point at which all four feet began to slip along the surface"；Stark 2015 同法。沒有讓壁虎爬牆，是在平放的表面上往後拉、量牠何時開始滑。改成「去抓」；p174「連壁虎都會滑」照留（Stark 2015 "even geckos … slip on PTFE"） |
| F11 | p196（所長） | 最難黏：小扁片鑽不進去，又貼不滿。 | 需改（原因是撰稿推論） | Huber 2007 摘要只有結果："Both experiments consistently show that the effective adhesion shows a minimum for a root mean square roughness ranging from 100 to 300nm"，沒有寫原因（claims.md C19 也標了這是撰稿解釋）；「鑽不進去」又跟 p069 打架。改成只說結果：是一個最低點，比更平、更粗的都差 |

## 二、逐段核對（正確的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p011 | 天花板倒掛的壁虎；四隻腳貼著、背朝下；全片問題 | 正確 | Wikipedia Common house gecko | 開場情境。"cling to vertical or even inverted surfaces when at rest" |
| p012–p015 | 膠水（錯猜）；在灰塵裡爬，有膠早沾成一團 | 正確 | — | 錯猜與反問，答案在 p152–p168 |
| p016–p019 | 有沒有牠爬不上去的地方；家裡找得到；跟著一隻腳看到放開 | 正確（附註） | Stark 2013、2015 | 回收在 p171–p174。Stark 2013 稱 PTFE 是 "a synthetic substrate to which geckos cannot adhere in dry conditions"，Stark 2015 "slip on PTFE"。附註：乾 PTFE 量到 1.6 ± 0.66 N，壁虎平均 99.3 g（體重約 1 N），而且是平放表面上的拉力，沒測過能不能爬直立的鐵氟龍。作者自己的用詞是黏不住、會滑，小問的問句可留；p017／p169 選修改「黏不太住」（見文末） |
| p020 | 你猜的膠水很多人都猜過 | 正確 | Hsu 2012；Autumn & Peattie | Hsu 特地澄清 "without the use of glue or suction devices"；"challenged explanation for millennia" |
| p021 | 亞里斯多德記下爬牆的本事 | 見 F01 | — | — |
| p022–p023 | 他沒有答案，後來的人也猜了很久 | 正確 | Autumn & Peattie；Autumn 2002 | "challenged explanation for millennia"；"the focus of scientific study for over a century"。原文只是拿壁虎比啄木鳥，沒有解釋 |
| p024–p029 | 靠膠水就得一直冒膠；腳底沒有會分泌的腺體；腺體＝做汗、口水的小工廠 | 正確 | Autumn 2002 全文；Hansen & Autumn 全文 | "Unlike many insects, geckos lack glands on the surfaces of their feet"；Hansen "nor secrete fluids that could remove adhering particles"。小工廠是兒童說法 |
| p030–p032 | 腳趾很怕水，水滴縮成圓圓一顆；腳是乾的 | 正確 | Autumn 2002 全文；Hsu 2012 | "The toes of live Tokay geckos were highly hydrophobic"；"The water contact angle (θ) of gecko setae was 160.9°"，160° 的水滴就是近乎正圓的水珠。Hsu "the complete absence of water at the contact interface" |
| p033–p035 | 很愛沾水、很怕水兩種表面黏得一樣好 | 正確 | Autumn 2002 | "adhered equally well …"（GaAs 對 SiO₂，活大守宮腳趾） |
| p036–p037 | 如果靠一層水，愛沾水的應該黏得好很多 | 正確 | Autumn 2002 | "reject the use of mechanisms relying on high surface polarity, including capillary adhesion"。論文推理的簡化 |
| p038 | 結果不差 | 見 F02 | — | — |
| p039–p042 | 吸盤（錯猜）；沒有用膠也沒有用吸盤 | 正確 | Hsu 2012 | "geckos are 'sticky' without the use of glue or suction devices" |
| p043–p045 | 腳印裡找到非常薄的一層油油的東西；那不就是膠水 | 正確 | Hsu 2012 全文 | "a residue is transferred on surfaces as they walk—geckos leave footprints"；鑑定為磷脂；厚 "1–2 nm"。「油油的」是脂質的兒童說法 |
| p046 | 少到要精密儀器才找得到 | 見 F03 | — | — |
| p047 | 還在查它有沒有幫忙；腳底沒有一灘膠 | 正確 | Hsu 2012 | "The presence of lipids has never been considered in current models"；作者只說可能是 "sacrificial layer"、"may be important"，來源與作用 "still unclear" |
| p048–p052 | 不用膠的貼紙；畫大來看 | 正確 | — | 站主觀點指定的唯一比喻 |
| p053–p055 | 腳趾底下一排排的皮，像疊起來的小毯子；每排長滿很細的毛 | 正確 | Hansen & Autumn 全文 | "Setae occur in uniform arrays on overlapping lamellar pads"；圖說 "adhesive lamellae (scansors) visible as overlapping pads"。claims.md C06 請查核者確認的「毛長在皮瓣上」已確認 |
| p056 | 一根大約頭髮的十分之一粗 | 正確 | Autumn 2000 摘要 | "Each 30-130 microm long seta is only one-tenth the diameter of a human hair" |
| p057–p059 | 一隻腳大約五十萬根 | 正確（附註） | Autumn 2000 摘要 | "a gecko's foot has nearly five hundred thousand keratinous hairs or setae"。附註：(1) 這是大守宮的數字，p090 與 p202 有交代；(2) Autumn & Peattie 寫全身 650 萬根，兩來源對不齊；片中 p100 不提剛毛數，不會相乘出矛盾，可留 |
| p060–p061 | 毛毛不黏 | 正確 | — | 小問的直覺 |
| p062–p063 | 尖端分成好幾百個更小的尖；最前面扁片像小湯匙 | 正確 | Autumn 2000；Hansen & Autumn | "hundreds of projections terminating in 0.2-0.5 microm spatula-shaped structures"；"branches at the tip into 100–1,000 spatulae" |
| p064–p068 | 牆畫大像小山丘；手指只碰到幾個山頂 | 正確 | Autumn & Peattie | 比喻；沒有說數字，不構成錯誤 |
| p069–p070 | 鑽進每個小山谷；幾乎每處都貼得上 | 見 F04、F05 | — | — |
| p071–p072 | 分得越細能貼的點越多；算過，分細就黏更牢 | 正確 | Autumn 2002 | "Theory predicts greater adhesive forces simply from subdividing setae to increase surface density" |
| p073–p075 | 兩種材料做的假小尖都黏得住；重點是形狀和大小 | 正確 | Autumn 2002 | "nanofabricated from two different materials. Both artificial setal tips stuck as predicted"；"merely a result of the size and shape of the tips" |
| p076–p083 | 任何兩樣東西靠得非常近就互相輕輕拉；很弱、只在極近處；手只碰到幾點 | 正確 | OpenStax 10.1 | 分散力 "present in all condensed phases"；"relatively weak … significant only when the molecules are very close"。「東西」代替「分子」是簡化 |
| p084–p085 | 叫凡得瓦力 | 正確 | Autumn 2002 | "dry adhesion of gecko setae by van der Waals forces"。先講是什麼再命名，符合站主觀點 |
| p086 | 濕氣會幫上一點忙 | 正確（附註） | Huber 2005 摘要 | "humidity contributes significantly to gecko adhesion on a nanoscopic level"，並明說與 Autumn 2002 相反。「一點忙」比 "significantly" 保守，但這是站主觀點指定的說法、且要求不判兩派誰對；不改 |
| p087–p088 | 一個扁片很弱，很多個一起拉 | 正確 | OpenStax 壁虎專欄 | "Although dispersion forces are very weak … the total attraction over millions of spatulae is large enough to support many times the gecko's weight" |
| p089–p090 | 研究大多用大守宮 | 正確 | 各論文方法 | Autumn 2002、Hansen、Hu、Stark 三篇、Gillies、Hsu 都用 *Gekko gecko*；爬牆速度是 *Hemidactylus garnotii*（p131 另說「一種小壁虎」） |
| p091 | 長好幾倍 | 見 F06 | — | — |
| p092–p094 | 我家那隻也這樣嗎 | 正確 | — | 回收在 p199–p207 |
| p095–p096 | 大守宮腳趾上大約十億個小扁片 | 正確 | Huber 2005 摘要 | "consisting of one billion spatulae in the case of Gekko gecko [Ruibal & Ernst 1965]"（二手引用；量級與「每腳約五十萬根 × 好幾百個尖」相符） |
| p097–p101 | 先量一根再估算；理論上能吊起大約一百三十公斤，約兩個大人 | 正確（附註） | Autumn 2000；Autumn & Peattie | "the first direct measurements of single setal force"；"200 microNewton … 6.5 million setae of a single tokay gecko attached maximally could generate 130 kg force"。附註：200 µN 是沿表面的拉力，「吊起」是把力換成重量的口語；兩個大人以每人約 65 公斤計 |
| p102 | 平常只用到一小部分 | 正確 | Autumn 2000；Wikipedia Gecko | "a seta is ten times more effective at adhesion than predicted from maximal estimates on whole animals"；"Gecko toes operate well below their full attractive capabilities most of the time" |
| p103–p105 | 一根腳趾撐得住整隻壁虎 | 正確 | Hansen & Autumn | "support its body mass with a single toe"；單趾力量 "well over the force required … (43 g) by a single digit" |
| p106–p112 | 貼得夠近夠多；用力一拔（錯猜）；不用硬拔，用角度的小把戲 | 正確 | Autumn 2000；Autumn 2006 | "reduced the forces necessary to peel the toe by simply detaching above a critical angle"；"very low detachment forces observed in climbing geckos" |
| p113–p114 | 腳趾從最前面往上、往後捲 | 正確 | Tian 2006；Autumn 2006；Hu 2012 | "rolling the toes upward and backward"；"geckos hyperextend their toes"；"scrolling … from a distal to a proximal direction" |
| p115–p118 | 像撕貼紙？看起來很像，但開關在每根小毛 | 正確 | Autumn 2006 摘要 | "apparently peeling like tape"；"adhesion depended directly on shear force, and was independent of detachment angle. Therefore we reject the hypothesis that gecko toes peel like tape"；"consistent with a critical angle of release" |
| p119–p121 | 小毛斜躺；角度翻到大約三十度以上自己鬆開 | 正確 | Autumn & Peattie；Tian 2006 | "simply increasing the angle that the setal shaft makes with the substrate to 30° causes detachment"；Tian "characteristic angle θs of ≈30°" |
| p122–p126 | 幾乎不用力；一排排小毛跟著翻起、照順序放手；把角度一翻 | 正確 | Autumn 2006；Hu 2012 | 低脫離力見上；「照順序」由趾尖往趾根的捲法推得，合理 |
| p127–p128 | 量過，放開一隻腳大約百分之一秒多一點 | 正確（附註） | Autumn & Peattie；Autumn 2006 Dynamics | "detach their feet in just 15 ms"。綜述沒寫物種；Dynamics 中 *H. garnotii* 步頻 15 Hz、"detachment of feet occupied … 37% of stance time"，量級吻合 |
| p129–p132 | 一種小壁虎往牆上衝，每隻腳一秒大約貼放十五次 | 正確 | Autumn 2006 Dynamics | "Hemidactylus garnotii … climbed vertically at up to 77 cm s(-1) with a stride frequency of 15 Hz using a trotting gait"。步頻＝每隻腳每秒循環數 |
| p133–p138 | 放平貼上，往身體這邊拖一下；小毛斜躺貼平；拖越大黏越牢 | 正確 | Autumn & Peattie；Autumn 2000；Autumn 2006；Tian 2006 | "a small normal preload, combined with a 5 μm displacement yielded a very large adhesive force"；"increased attachment force 600-fold"；"adhesion depended directly on shear force"；Tian "small pulling angles … gripping the toes inward" |
| p139–p144 | 只拍不拖黏得很少；平常不太黏，拖一下像打開開關；往裡拖就黏、翻起來就放 | 正確 | Autumn & Peattie；Autumn 2006；Phys.org 2014 | "Initial efforts to attach a seta failed because of improper 3D orientation"；Phys.org 報導的模型 "by default, non-sticky, but the stickiness can be activated by a small shear force"。「不太黏」保守恰當 |
| p145–p151 | 倒掛時前腳後腳互相往裡拉；可能是讓小毛保持拖著 | 正確（附註） | Autumn 2006 摘要；SICB 摘要；Dynamics | "Geckos use opposing feet and toes while inverted, possibly to maintain shear forces that prevent detachment"；"Inverted locomotion of geckos requires opposing shear forces at the level of toes or feet"；直立時 "Fore- and hindlegs both pulled toward the midline"。「可能」對上 possibly。附註：原文是「相對的腳**和腳趾**」，沒限定前對後；每隻腳往身體拖時前後腳自然互相往裡拉，不算錯；選修見文末 |
| p152–p157 | 回收灰塵；很細的粉末撒在大守宮腳上 | 正確 | Hansen & Autumn | "silica-alumina ceramic microspheres (2.5-μm mean radius"；三隻大守宮 |
| p158 | 只走了幾步 | 見 F07 | — | — |
| p159 | 差不多又能撐住自己 | 正確 | Hansen & Autumn | 見 F07 |
| p160–p163 | 灰塵留在玻璃上；推測牆拉灰塵的力比扁片大 | 正確 | Hansen & Autumn | "Contact mechanical models suggest …"；"particles tend to remain attached to the wall rather than to the spatulae"。「推測」對上 suggest |
| p164–p165 | 腳趾一捲甩掉灰塵；四步回到八成 | 見 F08、F09 | — | — |
| p166–p168 | 一般貼紙沾灰就不黏；贏過貼紙 | 正確 | — | 常識 |
| p169–p172 | 在廚房；不沾鍋的塗層常是鐵氟龍 | 正確 | Wikipedia Non-stick surface | "Non-stick is often used to refer to surfaces coated with polytetrafluoroethylene (PTFE), a well-known brand of which is Teflon"；同頁 "Not all non-stick pans use Teflon"（陶瓷塗層等），「常是」恰當 |
| p173 | 讓壁虎去爬 | 見 F10 | — | — |
| p174–p175 | 連壁虎都會滑 | 正確 | Stark 2015；Stark 2013 | "even geckos … slip on PTFE"；乾 PTFE 1.6 N 對乾玻璃 17.1 N。說「會滑」不說「完全黏不住」 |
| p176 | 小扁片很難拉出小拉力 | 正確（附註） | Stark 2015 | "the level of fluorination was most important for shear adhesion, particularly in air"；作者也說乾光滑含氟表面低得 "unusually"、"not captured by surface energy calculations"。台詞只描述結果方向，可留 |
| p177–p180 | 沾水一定更滑（錯猜）；泡水反而好上好幾倍 | 正確 | Stark 2013 | "wet PTFE (8.0 ± 1.09 N) than dry PTFE (1.6 ± 0.66 N)"，約五倍 |
| p181–p183 | 算得出大方向，還沒完全弄懂 | 正確 | Stark 2013 全文；Stark 2015 | "our model does not predict the whole-animal experimental results"、"further work is needed"；"our predictions show a qualitative trend" |
| p184–p186 | 普通玻璃泡水抓力少一大半 | 正確 | Stark 2013 | 濕玻璃 5.4 N 對乾玻璃 17.1 N（少約七成）；玻璃接觸角 50° |
| p187–p188 | 腳趾濕透只剩一點點 | 正確 | Stark 2012 | "Wetted toe pads … (0.86 ± 0.09 N) than the control (17.96 ± 3.42 N)"，約二十分之一 |
| p189–p192 | 下雨天？作者提醒，對又熱又濕地方的壁虎水可能是大麻煩 | 正確 | Stark 2012 | "may have significant consequences for the ecology and behavior of geckos living in tropical environments"。所長只轉述「可能」；Stark 2012 也發現只有水滴的玻璃與乾玻璃沒有顯著差別，台詞沒說有一點水就爬不動，恰當 |
| p193–p195 | 粗牆更好抓（錯猜）；不一定，有一種很細很細的粗糙 | 正確 | Huber 2007 | 見 F11 |
| p196 | 鑽不進去又貼不滿 | 見 F11 | — | — |
| p197–p198 | 跟一排排的皮差不多大的凸起，抓力剩很少很少 | 正確 | Gillies 2014 | "approaching the lamella length and inter-lamella spacing, losing 95% of shear adhesion over the range tested"。台詞沒說越粗越難（同篇 3 mm 起伏仍保有 60%） |
| p199–p202 | 家裡多半是另外幾種比較小的壁虎；也有一排排的皮；實驗大多用大守宮 | 正確 | Wikipedia Common house gecko、Gekko hokouensis、Tokay gecko | "adhesive lamellae under the feet"；種名不念，符合站主觀點 |
| p203–p205 | 換一種數字不一定一樣 | 正確 | Zimin 2025；Stark 2012 | "the difficulty to infer … from one taxon to another"。這段把前面大守宮的數字收回成「不一定」，處理了以單一物種推到全部壁虎的問題 |
| p206–p207 | 不是每種都有；有些腳趾細細的、沒有墊子 | 正確（附註） | Zimin 2025；Wikipedia Gecko | "pad-bearing species" 對 "padless geckos"；"About 60% of gecko species have adhesive toepads"；豹紋守宮 "does not have adhesive toe pads and cannot climb the glass"。「細細的」來源沒逐字寫，但無趾墊種的腳趾沒有擴大、細長帶爪是一般描述，可留；選修見文末 |
| p208–p214 | 小問總結 | 正確 | 同前 | 與已核說法一致 |
| p215–p216 | 我覺得最厲害是說放就放；一秒貼放好多次 | 正確 | Autumn 2006 Dynamics | 意見句；「好多次」對上 15 Hz，沒說成定值 |
| p217–p220 | 看就好別抓；看腳趾是不是先往上捲 | 正確 | Hu 2012 | 安全提醒（C21，不當查核主張）；"walking naturally with hyperextension"，觀察邀請可行 |
| p221–p224 | 片尾 | 正確 | — | — |
| YouTube 標題 | 壁虎黏得住，怎麼又能走得動？ | 正確 | — | 問題句 |
| YouTube 說明 | 膠水或吸盤、皮與小毛與扁片、翻角度、走幾步就乾淨、不沾鍋濕玻璃粗牆；插圖示意；數字多來自大守宮、是大約；不要抓 | 正確 | 同前 | 物種與「大約」都交代了；「走幾步就乾淨」對上 Hansen 摘要與 Hu 2012 自然行走 |
| 縮圖 | 黏得住／怎麼走？／腳底沒有膠 | 正確 | Hsu 2012 | "without the use of glue"；磷脂殘留片中已交代 |

## 三、撰稿者標出的疑點

| 項目 | 結論 |
| --- | --- |
| 「比你家那隻長好幾倍」 | 需改成「兩三倍」（F06） |
| 不沾鍋「常是」鐵氟龍 | 正確，「常是」恰當 |
| 「有些壁虎的腳趾細細的、沒有墊子」 | 正確（附註），可留；選修刪「細細的」 |
| 一百三十公斤 | 正確，有「理論上」「大約」 |
| 剛毛數（五十萬根／腳） | 正確；兩來源不一致，但片中只用一個、不相乘 |
| 三十度脫離角 | 正確（Autumn & Peattie、Tian 2006） |
| 腳趾往上往後捲 | 正確（Tian 2006、Hu 2012、Autumn 2006） |
| 倒掛時相對的腳 | 正確（附註），「可能」對上 possibly |
| 預設不黏 | 正確，「不太黏」保守 |
| 一秒十五次 | 正確，*H. garnotii* 步頻，片中說「一種小壁虎」 |
| 鐵氟龍與濕表面 | 數字與方向正確；只改 p173 的「爬」（F10） |
| 粗糙表面 | 結果正確；p196 原因是推論（F11） |
| 磷脂殘留 | p044、p047 正確；p046 要分清「看不到」與「查成分要精密儀器」（F03） |
| 亞里斯多德 | 原文是壁虎頭朝下爬樹（F01） |
| 以大守宮推到所有壁虎 | p090、p199–p207 與說明欄已交代 |
| 與站主觀點衝突 | 沒有。F04／F05／F11 讓「貼得夠近」前後一致；F09 讓灰塵機制不被說成定論 |

## 建議修改

必改（F01–F11）：

- p021：兩千多年前，亞里斯多德就記下過壁虎爬牆的本事。 → 兩千多年前，亞里斯多德就記下過，壁虎能頭朝下爬樹。（插圖若畫牆，提示詞一起改成樹）
- p038：結果不差，代表主要不是靠一層水。 → 結果兩種差不多，代表主要不是靠一層水。
- p046：不是。它少到要用很精密的儀器才找得到。 → 不是。它少到眼睛看不到，要用很精密的儀器，才查得出是什麼。
- p069：可是那麼多小扁片，就能鑽進每個小山谷， → 可是那麼多小扁片，就能鑽進許多小山谷，
- p070：幾乎每個地方，都貼得上。 → 大部分地方，都貼得上。
- p091：牠的身體，比你家牆上那隻長好幾倍。 → 牠的身體，大約是你家牆上那隻的兩三倍長。
- p158：一開始是不太黏。可是牠只走了幾步， → 一開始是不太黏。可是腳趾才踩了幾下，
- p164：另一個研究發現，腳趾往上一捲， → 另一個研究發現，腳趾能往上捲的時候，
- p165：會順便把灰塵甩掉，大約四步，就回到八成左右。 → 灰塵掉得快一倍，大約四步，就回到八成左右。
- p173：研究的人讓壁虎去爬乾的鐵氟龍， → 研究的人讓壁虎去抓乾的鐵氟龍，
- p196：最難黏：小扁片鑽不進去，又貼不滿。 → 黏起來反而最差，比更平、更粗的都差。

選修（不影響本輪結論）：

- p017：那有沒有牠爬不上去的地方？ → 那有沒有牠黏不太住的地方？；p169：那牠爬不上去的地方， → 那牠黏不太住的地方，（同步改 `video.json` loops 的 what 與 `build_scenes.py`；實驗只量平放表面上的拉力）
- p149：前腳和後腳會互相往裡拉。 → 腳和腳趾會朝相反方向，互相往裡拉。
- p207：有些壁虎的腳趾細細的，根本沒有這片墊子。 → 有些壁虎，根本沒有這片墊子。
- （給 claims.md 的維護者）C01 補記原文是拿壁虎頭朝下爬樹比啄木鳥；C05 補記 "not visible to the naked eye"、靠濕氣凝結顯影、厚 1–2 nm；C06 的「毛長在皮瓣上」已由 Hansen 全文確認；C16 補記 Hansen 是 "simulated steps"、"Full strides were not used"，Hu 2012 的灰塵機制是模型假說；C17 補記 Stark 2013 是平放表面上拉背帶。

## 來源

只列查核者這次實際打開並讀到原文的頁面。

```json
[
  {"title": "Autumn et al. (2000), Adhesive force of a single gecko foot-hair, Nature 405: 681–685（Europe PMC 摘要）", "url": "https://doi.org/10.1038/35015073", "checked_on": "2026-11-09"},
  {"title": "Autumn et al. (2002), Evidence for van der Waals adhesion in gecko setae, PNAS 99: 12252–12256（PMC 全文）", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC129431/", "checked_on": "2026-11-09"},
  {"title": "Autumn & Peattie (2002), Mechanisms of adhesion in geckos, Integr. Comp. Biol. 42: 1081–1090（摘要）", "url": "https://doi.org/10.1093/icb/42.6.1081", "checked_on": "2026-11-09"},
  {"title": "Hansen & Autumn (2005), Evidence for self-cleaning in gecko setae, PNAS 102: 385–389（PMC 全文）", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC544316/", "checked_on": "2026-11-09"},
  {"title": "Huber et al. (2005), Evidence for capillarity contributions to gecko adhesion, PNAS 102: 16293–16296（摘要）", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1283435/", "checked_on": "2026-11-09"},
  {"title": "Autumn et al. (2006), Frictional adhesion: a new angle on gecko attachment, J. Exp. Biol. 209: 3569–3579（摘要）", "url": "https://doi.org/10.1242/jeb.02486", "checked_on": "2026-11-09"},
  {"title": "SICB abstract: Why geckos don't fall off ceilings（Autumn 團隊）", "url": "https://sicb.org/?p=31725", "checked_on": "2026-11-09"},
  {"title": "Autumn et al. (2006), Dynamics of geckos running vertically, J. Exp. Biol. 209: 260–272（摘要）", "url": "https://doi.org/10.1242/jeb.01980", "checked_on": "2026-11-09"},
  {"title": "Tian et al. (2006), Adhesion and friction in gecko toe attachment and detachment, PNAS 103: 19320–19325", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1748224/", "checked_on": "2026-11-09"},
  {"title": "Hsu et al. (2012), Direct evidence of phospholipids in gecko footprints, J. R. Soc. Interface 9: 657–664（PMC 全文）", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3284128/", "checked_on": "2026-11-09"},
  {"title": "Hu et al. (2012), Dynamic self-cleaning in gecko setae via digital hyperextension, J. R. Soc. Interface 9: 2781–2790（PMC 全文）", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3479896/", "checked_on": "2026-11-09"},
  {"title": "Stark et al. (2012), The effect of surface water and wetting on gecko adhesion, J. Exp. Biol. 215: 3080–3086（摘要）", "url": "https://doi.org/10.1242/jeb.070912", "checked_on": "2026-11-09"},
  {"title": "Stark et al. (2013), Surface wettability plays a significant role in gecko adhesion underwater, PNAS 110: 6340–6345（PMC 全文）", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3631644/", "checked_on": "2026-11-09"},
  {"title": "Stark et al. (2015), Adhesive interactions of geckos with wet and dry fluoropolymer substrates, J. R. Soc. Interface 12: 20150464", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4528608/", "checked_on": "2026-11-09"},
  {"title": "Huber et al. (2007), Influence of surface roughness on gecko adhesion, Acta Biomaterialia 3: 607–610（摘要）", "url": "https://doi.org/10.1016/j.actbio.2007.01.007", "checked_on": "2026-11-09"},
  {"title": "Gillies et al. (2014), Gecko toe and lamellar shear adhesion on macroscopic, engineered rough surfaces, J. Exp. Biol. 217: 283–289（摘要）", "url": "https://doi.org/10.1242/jeb.092015", "checked_on": "2026-11-09"},
  {"title": "Zimin et al. (2025), Microhabitat and adhesive toepads shape gecko limb morphology, Integrative Zoology（摘要）", "url": "https://doi.org/10.1111/1749-4877.12880", "checked_on": "2026-11-09"},
  {"title": "Phys.org (2014-08-12), Scientists discover how geckos defy gravity", "url": "https://phys.org/news/2014-08-scientists-miracle-geckos-ceilings.html", "checked_on": "2026-11-09"},
  {"title": "OpenStax Chemistry 2e, 10.1 Intermolecular Forces", "url": "https://openstax.org/books/chemistry-2e/pages/10-1-intermolecular-forces", "checked_on": "2026-11-09"},
  {"title": "Wikipedia: Tokay gecko", "url": "https://en.wikipedia.org/wiki/Tokay_gecko", "checked_on": "2026-11-09"},
  {"title": "Wikipedia: Common house gecko", "url": "https://en.wikipedia.org/wiki/Common_house_gecko", "checked_on": "2026-11-09"},
  {"title": "Wikipedia: Gekko hokouensis", "url": "https://en.wikipedia.org/wiki/Gekko_hokouensis", "checked_on": "2026-11-09"},
  {"title": "Wikipedia: Gecko", "url": "https://en.wikipedia.org/wiki/Gecko", "checked_on": "2026-11-09"},
  {"title": "Wikipedia: Non-stick surface", "url": "https://en.wikipedia.org/wiki/Non-stick_surface", "checked_on": "2026-11-09"},
  {"title": "Aristotle, History of Animals, Book IX（D'Arcy W. Thompson 英譯）", "url": "https://www.ellopos.net/elpenor/greek-texts/ancient-greece/aristotle/history-animals-c.asp?pg=23", "checked_on": "2026-11-09"}
]
```
