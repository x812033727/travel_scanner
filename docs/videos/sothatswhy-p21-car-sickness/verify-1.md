# 查核報告 1（sothatswhy-p21-car-sickness）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-11
- 方法：逐句讀 `video.json` 的 193 句台詞（p001–p193），加上 YouTube 標題、說明與縮圖文字（headline「看漫畫／就暈車？」、sub「眼睛跟耳朵吵架了」）。對照 `claims.md` 的 C01–C25 當線索，但不採用它的引文，每個來源當天重新打開讀原文：
  - CDC Yellow Book〈Motion Sickness〉（作者 John F. Golding，頁面日期 2025-04-23）：curl 回 403（Akamai），改用 WebFetch 讀，要它逐字引出相關句子。
  - NHS〈Motion sickness〉（last reviewed 2023-06-19）、NIDCD〈Balance Disorders〉、Cleveland Clinic〈Motion Sickness〉（2024-04-08）：curl 抓 HTML 轉純文字逐段讀。
  - Lackner 2014（Exp Brain Res，PMC4112051）、Keshavarz et al. 2015（Front Psychol，PMC4403286）：Europe PMC `fullTextXML` 讀全文。
  - 只讀到 PubMed 摘要（NCBI efetch）：Golding 2006、Golding 2016、Griffin & Newman 2004、Turner & Griffin 1999、Kuiper et al. 2018、Kuiper et al. 2020、Rolnick & Lubow 1991、Dong et al. 2011、Reavley et al. 2006、Treisman 1977、Oman 2012、Oman & Cullen 2014、Stoffregen & Smart 1998。
  - 撰稿沒列、本次補讀的：Cullen & Roy 2004（J Neurophysiol 91:1919–1933，PubMed 摘要），用來確認 Oman & Cullen 說的「被動移動時反應較大的神經元」是在哪種動物身上記錄到的。
- 打不開／沒讀到原文的：CDC 頁面 curl 被擋，只經 WebFetch（引句由工具轉述，已要求逐字，但不是我親手讀的 HTML）；Oman & Cullen 2014 全文（Europe PMC PMC4130651 非開放取用，fullTextXML 只回 500 bytes），只用摘要；上列各篇只讀摘要，全文細節（例如 Griffin & Newman 的座位條件是前後排還是左右、Dong 2011 用的是不是賽車遊戲、Rolnick & Lubow 的旋轉裝置）沒有讀到。Mayo Clinic 沒有試，片中也沒有依賴。
- 結論統計（台詞 193 句）：正確 188、需改 5、錯誤 0。另外標題、說明、縮圖 3 項：正確 3、需改 0。另有 7 處選修建議（不影響結論，見文末）。
- 字數：下表建議句含標點計算，小問 ≤15、所長 ≤25。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p016（所長） | 剛好相反。研究暈車的人發現， | 需改（說過頭） | 小問猜「會暈車是內耳不好？」，「剛好相反」等於說內耳有毛病跟容易暈無關、甚至相反。CDC："People with a history of migraine, vertigo, or vestibular disorders are more prone to motion sickness." Golding 2016 摘要："Motion sickness susceptibility also varies dramatically between special groups of patients, including those with different types of vestibular disease"。內耳出問題的人有些反而**更**容易暈；只有平衡功能**完全**喪失的人才完全不暈（Lackner 2014："only those without a functioning vestibular system are fully immune"）。p017–p018 本身正確，只要開頭不說「剛好相反」 | 不一定。研究暈車的人發現，（13 字；p017、p018 照留） |
| F02 | p092（所長） | 還有實驗是先用聲音提醒，下一步要往哪動。 | 需改（少一半條件） | Kuiper et al. 2020："The auditory cues were either 1) informative on the timing and direction of the upcoming motion, or 2) non-informative." 提醒的是**什麼時候**和**往哪個方向**，兩樣一起 | 還有實驗用聲音先提醒：什麼時候、要往哪動。（21 字） |
| F03 | p093（所長） | 知道接下來會怎樣的人，也比較不暈。 | 需改（把同一批人的兩種情況說成兩種人） | Kuiper et al. 2020："Participants (N = 20) were exposed on a sled on a rail track to two 15-min conditions. Both were identical in terms of motion … average illness ratings were significantly lower for the condition that contained informative auditory cues"。是**同一批 20 人**各坐兩次，比的是「有提醒的那一次」，不是「某一種人」。原句讓人聽成有些人天生比較知道、比較不暈 | 有提醒的時候，同一群人也比較不暈。（17 字；p094–p096 照留） |
| F04 | p167（所長） | 另一派認為，暈車跟身體穩不穩有關： | 需改（放在「為什麼想吐」裡，層次會被聽錯） | 這句接在「為什麼偏偏是想吐」與毒物猜法之後，「另一派」會被聽成是「為什麼想吐」的另一個答案。其實姿勢不穩說是跟**感覺衝突**對打的「怎麼引起」理論：Keshavarz 2015："Another prominent theory highlights the potential role of postural stability … claiming that changes in postural stability are the crucial factor underlying VIMS. Following this approach, postural instability is not only a consequence of VIMS, but also precedes and causes it."；Stoffregen & Smart 1998："This confirms a key prediction of the postural instability theory of motion sickness." 它也沒有解釋為什麼是想吐。說出它是跟感覺衝突不同的一派，也補上 p063「最多人接受」之外確實有對手的交代 | 還有一派不同意感覺衝突，認為暈車跟身體穩不穩有關：（25 字；p168 照留） |
| F05 | p171（所長） | 研究的人找到一群腦細胞，被別人帶著動時，反應特別大； | 需改（沒說是猴子） | 小問 p169–p170 問的是「那大腦裡」，片中沒交代物種，會被聽成在人腦裡找到。Oman & Cullen 2014："Recent studies show a subclass of neurons in the vestibular nuclei and deep cerebellar nuclei that respond preferentially to passive head movements."——這些研究是 Cullen 實驗室的單細胞記錄。Cullen & Roy 2004："the results of recent single-unit studies in head-unrestrained monkeys … one class of neurons in vestibular nuclei … is substantially less responsive to active head movements than to passively applied head rotations." 現象本身寫對了，只是記錄的是猴子 | 猴子的腦裡有一群細胞，被別人帶著動時，反應特別大；（25 字；p172–p174 照留。若圖 `chief-neurons` 畫成人腦，可改畫成猴子或不指明的腦） |

## 二、逐段核對（正確的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p005 | 坐車看漫畫頭暈、肚子怪；開車的爸爸沒事 | 正確 | — | 小問的情境；司機少暈見 p084 |
| p006–p008 | 遮眼睛的乘客照樣暈；沙發上看賽車畫面也有人暈 | 正確 | Griffin & Newman 2004；Keshavarz 2015 | 預告句，在 p054–p057、p100–p111 回收 |
| p009–p013 | 不是只有我；眼睛跟身體在吵什麼 | 正確（附註） | Turner & Griffin 1999；Reavley 2006 | 遊覽車調查 "28.4% of passengers reported feeling ill"；雙胞胎調查 "Approximately 40% of respondents reported at least moderate susceptibility"。「絕對不是你一個人」成立 |
| p014–p015 | 小問錯猜：內耳不好 | 正確 | — | 錯猜，見 F01 |
| p016 | 剛好相反 | 見 F01 | — | — |
| p017 | 平衡功能完全不能用的人才完全不會暈 | 正確 | Lackner 2014 | "only those without a functioning vestibular system are fully immune" |
| p018 | 內耳好好的人幾乎每一個都可能暈 | 正確 | CDC；Golding 2006 | CDC "given a sufficient stimulus, almost all people with functional vestibular systems"；Golding "given a sufficiently provocative motion stimulus almost anyone with a functioning vestibular system can be made motion sick"。「可能」保住了「刺激夠強」這個條件 |
| p019–p021 | 會暈代表它一直在工作 | 正確（推論，已標「可以這麼說」） | 同上 | 會暈需要有功能的前庭，推論成立；改了 F01 之後不會被聽成「會暈＝耳朵健康的證明」 |
| p022–p025 | 耳朵深處有很細的小管子和小袋子，裡面裝液體 | 正確 | NIDCD | "three fluid-filled ducts"；"fluid-filled pouches called the utricle and the saccule" |
| p026–p028 | 一杯水的比喻：轉彎水晃到一邊，煞車加速也晃 | 正確（比喻） | NIDCD | "When you turn your head, fluid inside the semicircular canals moves"；限度在 p031–p032 交代 |
| p029 | 液體會晃，還有很小的顆粒被地球往下拉 | 正確（附註，簡化） | NIDCD | "the gel contains tiny, dense grains of calcium carbonate called otoconia. Whatever the position of your head, gravity pulls on these grains"。附註：顆粒在膠狀層裡，片中沒說顆粒浮在水裡，可留 |
| p030 | 大腦看它們怎麼晃，知道在轉、加速或煞車 | 正確 | NIDCD | 半規管 "tell your brain when your head rotates"；耳石器官 "any direction your head might be moving, such as side to side, up or down, forward or backward" |
| p031–p032 | 杯子只是比喻；內耳很小；管轉彎跟管加速分開 | 正確 | NIDCD | 半規管（轉動）與 utricle／saccule（重力與直線移動）是不同構造 |
| p033–p036 | 眼睛看外面怎麼跑也在報告；腳底跟肌肉也會報告 | 正確（簡化） | NIDCD；CDC | "your eyes, ears, and the muscles and touch sensors in your legs"；CDC 衝突在 "vestibular, visual, and kinesthetic" 之間 |
| p037–p039 | 走路時大家說的一樣，大腦就放心 | 正確（撰稿推論，成立） | Oman & Cullen 2014 | 主動移動的前庭輸入 "are canceled by a mechanism comparing the expected consequences of self-generated movement … with the actual sensory feedback"；"human immunity to normal self-generated movement" |
| p040–p050 | 看漫畫：漫畫跟著晃，眼睛報告沒動；內耳報告在轉；對不上 | 正確 | NHS；Cleveland Clinic；CDC | NHS "The inner ear sends different signals to your brain from those your eyes are seeing. These confusing messages cause you to feel unwell."、"do not read"；Cleveland "your eyes, inner ear and body send conflicting messages to your brain"；CDC "Avoiding reading or visual scanning" |
| p051–p053 | 閉上眼睛就不會吵了吧（錯猜） | 正確 | — | 錯猜 |
| p054–p056 | 英國研究：郊區坐車三十分鐘，遮眼的人跟看不到前面的人差不多一樣暈 | 正確 | Griffin & Newman 2004 | "a 30-min suburban car journey"；"Absence of a visual field (blindfolded) resulted in similar sickness to that with no external forward view (with or without a side view)." University of Southampton |
| p057 | 閉眼也不一定能讓大腦安靜 | 正確（措辭恰當） | Griffin & Newman 2004；NHS | 「不一定」很重要：NHS 把 "close your eyes and breathe slowly" 列為可以試的事；片中沒說閉眼沒用，也沒建議閉眼 |
| p058–p062 | 大腦會先猜；有一個預想；報告跟預想對不上就不舒服 | 正確（模型，下一句即標明） | CDC；Oman & Cullen 2014 | CDC 衝突與 "internal model" 有關；Oman & Cullen "expected consequences of self-generated movement (estimated with an internal model…)"。p063 立刻標成解釋 |
| p063–p064 | 叫感覺衝突，是目前最多人接受的解釋；不是全部的答案 | 正確 | CDC；Golding 2016；Lackner 2014 | CDC "The most widely accepted explanation for motion sickness is the sensory conflict or neural mismatch theory."；Lackner "A fully adequate theory of motion sickness is not presently available. … A sensory conflict theory can explain many but not all aspects" |
| p065–p066 | 看窗外會比較好嗎 | 正確 | — | 問句 |
| p067–p070 | 英國問了三千多位遊覽車乘客；完全看不到前面的人不舒服的大約是看得很清楚的人的三倍 | 正確 | Turner & Griffin 1999 | "A questionnaire survey of 3256 coach travellers"；"approximately three times higher for passengers with no view of the road ahead (mean, 34.6%) compared to passengers who could see the road ahead extremely well (mean, 12.7%)"。34.6÷12.7≈2.7，「大約三倍」是原文說法；「問了」符合問卷調查，沒說因果 |
| p071–p072 | 小客車實驗：只看得到旁邊的窗跟看不到前面差不多 | 正確 | Griffin & Newman 2004 | "no external forward view (with or without a side view)" 與蒙眼相似 |
| p073 | 看得到前面的路才比較不暈 | 正確（附註） | Griffin & Newman 2004 | "A wide or narrow forward view (with or without a side view) reduced sickness." 附註：講的是那個實驗，p132–p133 又交代螢幕播前路沒用，「才」可留；選修 S3 |
| p074–p076 | 重點是前面不是窗戶；那個實驗裡坐哪一排沒有明顯差別 | 正確（附註） | Griffin & Newman 2004 | "For the conditions of these experiments, seating position did not significantly affect sickness." 片中限定「那個實驗裡」。附註：摘要只說 seating position，沒說前後排，見選修 S4；NHS 建議 "sit in the front of a car"，片中沒有反駁，也沒有給建議，不打架 |
| p077–p078 | 所長的想法：路一彎眼睛先看到，大腦猜得到水要晃 | 正確（意見已標明） | Kuiper 2018；Kuiper 2020 | "Carsickness is associated with a mismatch between actual and anticipated sensory signals."；"Being able to anticipate upcoming motion is known to potentially mitigate sickness"。標成「我的想法」恰當 |
| p079–p080 | 荷蘭實驗：邊坐邊看螢幕找東西；螢幕在前窗高度、看得到外面，比低處比較不暈 | 正確 | Kuiper et al. 2018 | VU Amsterdam；"Seated in the front passenger seat 18 participants were driven a 15-min long slalom … while performing a continuous visual search-task"；"eye-height in front of the windscreen, allowing peripheral view on the outside world" vs "the height of the glove compartment"；"resulted in less carsickness" |
| p081–p084 | 看前面只是一部分；司機很少暈，研究者也注意到 | 正確 | Rolnick & Lubow 1991；CDC | 標題 "Why is the driver rarely motion sick?"；CDC "being the driver or the pilot; also, there is evidence that perception of "controllability" is important" |
| p085–p089 | 以色列實驗：22 對人坐會轉的機器；轉得一樣、只有一人能控制；能控制的明顯較不舒服少 | 正確（附註） | Rolnick & Lubow 1991 | Israeli Naval Hyperbaric Institute, Haifa；"Twenty-two pairs of yoked subjects were exposed to nauseogenic rotation. One subject of each pair had control over the rotation and head movements, while the other was exposed passively to the same motion stimulus. Subjects who had control reported significantly fewer motion sickness symptoms"。附註：摘要沒說是什麼裝置，「會轉的機器」恰當；圖畫旋轉椅是示意 |
| p090–p091 | 研究的人認為：自己要轉彎大腦早就知道，水一晃跟它猜的一樣 | 正確（已標「研究的人認為」） | Rolnick & Lubow 1991；Oman & Cullen 2014 | Rolnick "the concept of feed-forward mechanisms in motion perception"；Oman & Cullen "We discuss how such a mechanism is consistent with the notable difference in motion sickness susceptibility of drivers as opposed to passengers"。附註：Rolnick 刻意把兩組的「可預測性」拉平，所以效果歸給「控制」本身；片中說的是大腦預先知道自己的動作（feed-forward），不是「事先知道路況」，兩者不打架 |
| p092–p093 | 聲音提醒 | 見 F02、F03 | — | — |
| p094–p096 | 像爸爸喊一聲；有點像，但那是軌道上滑的車，不是山路 | 正確 | Kuiper et al. 2020 | "exposed on a sled on a rail track"；"9 m fore-aft displacements"。限度交代得好；研究由 Ford 贊助（摘要聲明），片中不必提 |
| p097–p106 | 反過來：沙發上看賽車畫面，眼睛說在動，茶几上的水不動、內耳說沒動 | 正確（情境示意） | Keshavarz 2015 | "physical movement is usually limited or absent during VIMS" |
| p107–p110 | 這樣也有人會暈，叫視覺引起的暈動症；「眼睛看出來的暈」 | 正確 | Keshavarz 2015；Cleveland Clinic | "VIMS is a sensation very similar to traditional motion sickness (MS)"；Cleveland "Some people get a kind of motion sickness while playing video games and virtual reality games" |
| p111 | 電影院大銀幕、虛擬實境、駕駛模擬器都有人遇過 | 正確 | Keshavarz 2015；CDC | "Cinerama sickness (VIMS in movie theaters), cybersickness (VIMS in VR users), simulator sickness (VIMS in driving or flight simulators), or gaming sickness"；CDC VR 與模擬器的症狀較多 |
| p112–p117 | 火車停在月台，旁邊那列開走，覺得自己在動；叫自己在動的錯覺 | 正確 | Keshavarz 2015 | "A typical real-life example of vection is the train illusion, whereby seeing the movement of a neighboring train creates the illusion that one's own stationary train is moving." |
| p118–p119 | 看出來的暈常跟錯覺一起出現；有錯覺不一定暈；怎麼連還在爭論 | 正確 | Keshavarz 2015 | "VIMS is typically accompanied by vection, but that vection can clearly be experienced in the absence of VIMS."；"it is still a matter of debate as to whether vection is a necessary prerequisite for visually induced motion sickness" |
| p120–p122 | 不管哪邊，對不上就可能暈；感覺衝突說得通 | 正確 | Keshavarz 2015 | "The sensory conflict theory … is arguably the most prominent theory used to explain VIMS" |
| p123–p128 | 兩人看一樣的賽車畫面，一個自己玩一個看錄影；自己開的比較少說會暈；螢幕裡的車也有差 | 正確（附註） | Dong et al. 2011 | "one member of each pair of participants played a driving video game … A recording of that performance was viewed … by the other member … exposed to identical visual motion stimuli"；"drivers … were less likely to report motion sickness than … passengers"；"extend this finding to the control of noninertial virtual vehicles"。附註：摘要只說 driving video game，沒確認是賽車，見選修 S5 |
| p129–p133 | 車上用螢幕即時播前面的路，並沒有比較不暈 | 正確 | Griffin & Newman 2004 | "The provision of a real-time video view of the road ahead did not reduce motion sickness." |
| p134–p136 | 研究的人說還要弄清楚哪些畫面讓人暈、哪些讓人不暈 | 正確 | Griffin & Newman 2004 | "The minimization of sickness by the provision of visual information requires improved understanding of those factors that combine to cause and suppress sickness." |
| p137–p138 | 解釋的界線：說得出哪裡對不上，還不能準準說誰會暈、暈多少 | 正確（所長轉述） | Lackner 2014 | "can explain many but not all aspects of motion sickness elicitation"；同篇也說個人差異由敏感度、適應、消退三個因素決定，理論本身不直接給出 |
| p139–p142 | 為什麼有人很會暈有人不會；第一件沒解開的事 | 正確 | Reavley 2006 | "the underlying determinants of individual susceptibility to motion sickness remain unclear" |
| p143–p144 | 有研究估計最容易和最不容易暈的人差大約一萬倍 | 正確（附註） | Lackner 2014 | "The range of vulnerability in the normal population varies about 10,000 to 1."。內文說明這是作者實驗室的估計：敏感度約 10:1、適應常數約 10:1、症狀消退時間常數約 100:1，"The import of these values is that susceptibility to motion sickness in the general population varies by about 10,000–1"。「有研究估計」「大約」恰當；附註：是三個參數範圍相乘的估計，範圍限「一般人」，見選修 S6 |
| p145–p146 | CDC：兩歲以下通常不太會暈；之後越來越容易，7–12 歲最容易，再慢慢變少 | 正確 | CDC | "Children under 2 years of age do not usually experience motion sickness."；"Susceptibility then rises, peaks between the ages of 7 and 12 years, and later declines through adulthood to old age" |
| p147–p149 | 我八歲，剛好在最會暈的年紀 | 正確 | CDC | 族群平均的說法，小問自己說「剛好在」不構成診斷 |
| p149–p150 | 女生比男生容易一點，差別比年紀小得多 | 正確 | CDC；Turner & Griffin 1999 | "women are more susceptible than men, but this is a much smaller effect than age"；遊覽車 "Females … by a ratio of four to three" |
| p151 | 常偏頭痛的人也比較容易暈 | 正確 | CDC | "People with a history of migraine, vertigo, or vestibular disorders are more prone"；見選修 S1 |
| p152 | 雙胞胎研究：誰比較會暈，很大一部分跟遺傳有關 | 正確（附註） | Reavley 2006；CDC | "heritability for a motion sickness factor score estimated as 57%"、兒童期 70%；CDC "heritability accounting for 55–70% of the variation"。附註：Reavley 的對象是 3,652 名成年女性雙胞胎；片中不給百分比、不說對象，「很大一部分」恰當 |
| p153–p155 | 是哪個地方讓我比較會暈；背後原因還不清楚 | 正確 | Reavley 2006 | "the underlying determinants of individual susceptibility to motion sickness remain unclear" |
| p156 | 遊覽車調查：年紀越大、越常坐車的人越少暈 | 正確 | Turner & Griffin 1999 | "Travel sickness decreased with increasing passenger age and greater travel experience."；只講觀察，沒說多坐就會好 |
| p157–p160 | 為什麼偏偏想吐，第二件沒解開；說得出怎麼引起，說不出為什麼是想吐 | 正確 | Golding 2006；Golding 2016 | "Current hypotheses of the 'Why?' of motion sickness are still under investigation … By contrast, the 'How?' of motion sickness is better understood"；Golding 2016 "what reason or purpose does motion sickness serve, if any?" |
| p161–p164 | 有人提過猜法：毒讓感覺亂掉，吐掉保險，暈車是不小心被晃動觸發 | 正確（已標猜法） | Treisman 1977 | "disturbances in sensory input or motor control produced by ingested toxins. The last would be the important cause in nature, the main function of the emesis being to rid the individual of ingested neurotoxins. Its occurrence in response to motion would be an accidental by product of this system." |
| p165–p166 | 只是猜法；有證據支持也有證據對不上；還沒定案 | 正確（附註） | Oman 2012；Golding 2006 | Oman "supporting evidence is equivocal, and contradictory evidence exists"；Golding 2006 把 "toxin detector" 列為仍在研究的假說之一。附註：原文是支持的證據「說不準」，片中「有證據支持它」略強，見選修 S7 |
| p167 | 另一派 | 見 F04 | — | — |
| p168 | 有實驗看到人在覺得不舒服以前身體就晃得比較厲害 | 正確（附註） | Stoffregen & Smart 1998；Dong 2011 | "Analysis of postural motion during exposure to the moving room revealed increases in postural sway before the onset of subjective motion sickness symptoms."；Dong 2011 也看到 "Before the onset of subjective symptoms of motion sickness movement differed"。附註：Stoffregen 的受試者是站在會動的房間裡，不是坐車，片中說「有實驗」沒擴大，可留 |
| p169–p170 | 大腦裡有負責吵架的地方嗎 | 正確 | — | 問句 |
| p171 | 一群腦細胞 | 見 F05 | — | — |
| p172 | 自己動的時候它們比較安靜 | 正確（簡化） | Oman & Cullen 2014；Cullen & Roy 2004 | "During active movement, the semicircular canal and otolith input … to these neurons are canceled"；"substantially less responsive to active head movements" |
| p173–p174 | 他們猜可能就是比對預想的地方；怎麼讓人想吐還沒找到 | 正確（已標猜） | Oman & Cullen 2014；Golding 2016 | "their existence and putative role in posture control and motion sickness have been long debated"；"stimulate nearby brainstem emetic centers-via an as yet unidentified mechanism"；Golding "putative "sensory conflict" neurons" |
| p175–p186 | 小問總結：漫畫跟著晃眼睛說沒動、耳朵裡的水說在轉、跟大腦猜的對不上就暈；爸爸自己轉彎猜得到 | 正確 | 同 p040–p064、p084–p091 | 與已核說法一致；「跟大腦猜的對不上」保留了感覺衝突是解釋的層次（p063 已標） |
| p187–p188 | 所長意見：你會暈是因為身體一直很認真在算你怎麼動 | 正確（意見已標明） | Lackner 2014 | 有「我覺得」；會暈需要有功能的前庭 |
| p189–p193 | 到阿嬤家；留言題；訂閱 | 正確 | — | 留言題問經驗，不給建議 |
| YouTube 標題 | 坐車看書，為什麼容易暈？ | 正確 | 同 p040–p050 | — |
| YouTube 說明 | 一杯水比喻；看書時哪邊報告變了；遮眼也暈；感覺衝突是「最多人接受的解釋」；沙發看賽車；還回答不了的事；非醫療建議、AI 插圖示意 | 正確 | 同前 | 與片中核過的說法一致；限度與「不是醫療建議」都有交代。若採 F04，「最多人接受的解釋」的說法仍成立 |
| 縮圖 | 看漫畫／就暈車？／眼睛跟耳朵吵架了 | 正確（附註） | NHS；Cleveland Clinic | NHS "The inner ear sends different signals to your brain from those your eyes are seeing."，「吵架」是小問 p013 用的比喻；片中 p042「沒有人說謊」與 p058–p062（閉眼也暈、大腦的預想）把它補完整，可留 |

## 三、撰稿者標出的疑點

| 項目 | 結論 |
| --- | --- |
| C05 走路時大家說的一樣（撰稿推論） | 正確。Oman & Cullen 摘要明說主動移動的輸入被預期抵銷、"human immunity to normal self-generated movement"，推論直接 |
| C11 所長的想法：路一彎眼睛先看到 | 正確。標成意見；Kuiper 2018／2020 的方向正是預期 |
| C13 以色列實驗、「會轉的機器」、旋轉椅插圖 | 正確。摘要只說 "nauseogenic rotation"，「會轉的機器」沒說錯；插圖是示意 |
| C24 衝突神經元（簡化） | 需改（F05）：被動／主動的差別寫對了，但記錄的是猴子，片中要說 |
| 其他：p016「剛好相反」 | 需改（F01）：CDC 明說前庭疾病的人更容易暈 |
| 其他：p092–p093 聲音提醒 | 需改（F02、F03）：提醒包含時機與方向；同一群人兩種情況 |
| 其他：p167「另一派」 | 需改（F04）：姿勢不穩說是跟感覺衝突對打的理論，不是「為什麼想吐」的答案 |
| 其他：一萬倍、三倍 | 都正確，見表二 p067–p070、p143 |
| 其他：醫療建議 | 沒有。片中不提藥物、坐前座或閉眼的建議；看前方、閉眼、座位都只講研究看到什麼（p057「不一定」、p076「那個實驗裡」措辭都恰當），說明欄寫明不是醫療建議 |

## 建議修改

必改：

- F01 p016：剛好相反。研究暈車的人發現， → 不一定。研究暈車的人發現，（13 字）
- F02 p092：還有實驗是先用聲音提醒，下一步要往哪動。 → 還有實驗用聲音先提醒：什麼時候、要往哪動。（21 字）
- F03 p093：知道接下來會怎樣的人，也比較不暈。 → 有提醒的時候，同一群人也比較不暈。（17 字）
- F04 p167：另一派認為，暈車跟身體穩不穩有關： → 還有一派不同意感覺衝突，認為暈車跟身體穩不穩有關：（25 字）
- F05 p171：研究的人找到一群腦細胞，被別人帶著動時，反應特別大； → 猴子的腦裡有一群細胞，被別人帶著動時，反應特別大；（25 字；插圖 `chief-neurons` 若畫人腦一併改）

選修（不影響本輪結論）：

- S1 p151：常偏頭痛的人，也比較容易暈。 → 常偏頭痛、或內耳平衡出過問題的人，也比較容易暈。（24 字；CDC "migraine, vertigo, or vestibular disorders"，跟 F01 前後呼應）
- S2 F01 若想更完整，可在 p018 後讓所長補「有些內耳的毛病，反而更容易暈」；不加也不錯。
- S3 p073：看得到前面的路，才比較不暈。 → 可照留；「才」限於那個實驗，p133 有轉折。
- S4 p076：坐哪一排 → 坐哪個位子（「對。那個實驗裡，坐哪個位子，反而沒有明顯差別。」23 字）。摘要只說 seating position，沒讀到全文，不能確認是前後排。
- S5 p101、p123：Dong 2011 摘要只說 "driving video game"，沒確認是賽車。p123 可改「還有一個實驗：兩個人看一模一樣的開車遊戲畫面，」（23 字）；p101 是情境示意，可留。
- S6 p143：有研究估計，最容易暈和最不容易暈的人，差了大約一萬倍。 → 有研究估計，一般人裡最會暈和最不會暈的，差了大約一萬倍。（28 字含標點，不含標點 25；原句也超過 25 含標點，依撰稿的計法決定）
- S7 p165：有證據支持它 → 支持的證據說不準（「這只是一個猜法。支持的證據說不準，反對的也有，」23 字；Oman 2012 "supporting evidence is equivocal, and contradictory evidence exists"）
