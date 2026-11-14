# 主張與來源（sothatswhy-p21-car-sickness）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說（附行號，第一版 2026-11-11）、來源原文與注意事項，並標出它是
**公認的解釋（模型）**、**研究看到的現象**、**假說**，還是**未知**。撰稿只能用「可用說法」裡的數字與說法；等另一個代理逐行查核（`verify-1.md`）。

**行號 2026-11-13 重編**：小問的捧場句刪減後（站主 2026-11-13 規則，小問字數 ≤ 20%），以下行號改對到目前 `video.json` 的 p001–p172；「可用說法」裡引的句子仍是第一版原文，現行措辭以 `video.json` 為準（查核改字見 `verify-1.md`）。

2026-11-11 撰稿時當天重讀每一個來源（引文是原句）：
- NHS、NIDCD、Cleveland Clinic：curl 讀 HTML 轉純文字。
- CDC Yellow Book：curl 被 Akamai 擋（403 Access Denied），改用 WebFetch 讀到全文（頁面標示作者 John F. Golding、更新日 2025-04-23）。
- PubMed 摘要：NCBI E-utilities `efetch` 讀。PMC 全文（Lackner 2014、Keshavarz 2015）：PMC 網站要過 reCAPTCHA，改用 Europe PMC 的 `fullTextXML` API 讀全文。
- **讀不到、沒有用的**：Mayo Clinic（curl 與 WebFetch 都 403），改用 Cleveland Clinic；Oman & Cullen 2014 的 Europe PMC 全文回 500，只用 PubMed 摘要（舊查核 `week11/S20.md` 讀過全文）。
- 舊查核包 `so-thats-why/week11/S20.md`（2026-09-29）只當線索；這裡每一條都重開來源。方括號數字對應文末〈來源〉。

**本集不做的事**：不提任何藥物、貼片、薑、穴位手環或治療；看前方、閉眼、坐哪一排只講「研究看到什麼」，不寫成「你應該怎麼做」。NHS [2] 的建議清單（坐前座、看地平線、閉眼慢慢呼吸、不要閱讀）只用來核對片中的觀察，片中不轉述成指示。

## C01 會暈車不是內耳不好；平衡功能完全不能用的人才完全不會暈；內耳正常的人幾乎都可能暈【研究看到的現象】

- **可用說法**：小問「我聽說會暈車，是內耳不好？」所長「剛好相反。研究暈車的人發現，內耳的平衡功能完全不能用的人，才完全不會暈。內耳好好的人，幾乎每一個都可能暈。」（p014–p018）「可以這麼說：會暈，代表它一直在工作。」（p020，口語收尾）開場「你會暈，絕對不是你一個人。」（p010）
- **來源**：[5]、[1]、[6]
- **可信度／注意**：高。Lackner [5]：「Motion sickness can occur during exposure to physical motion, visual motion, and virtual motion, and only those without a functioning vestibular system are fully immune.」CDC [1]：「almost all people with functional vestibular systems」can develop motion sickness。Golding 2006 [6]：「given a sufficiently provocative motion stimulus almost anyone with a functioning vestibular system can be made motion sick」。
  「代表它一直在工作」是口語化的推論（會暈需要有功能的前庭），**撰稿推論**。

## C02 耳朵很深的地方有很細的小管子和小袋子，裡面裝著液體，還有很小的顆粒被地球往下拉；大腦看它們怎麼動，知道你在轉、在加速或煞車；管轉彎和管加速的是不同地方【公認的構造】

- **可用說法**：p022–p023、p027–p028、p029–p030（「真的內耳很小很小，而且管轉彎的地方，跟管加速的地方，是分開的」）
- **來源**：[4]
- **可信度／注意**：高。NIDCD [4]：「The semicircular canals contain three fluid-filled ducts … They tell your brain when your head rotates.」「When you turn your head, fluid inside the semicircular canals moves…」「two otolithic organs: fluid-filled pouches called the utricle and the saccule. These organs tell your brain the position of your head with respect to gravity … as well as any direction your head might be moving, such as side to side, up or down, forward or backward.」「the gel contains tiny, dense grains of calcium carbonate called otoconia. Whatever the position of your head, gravity pulls on these grains」。
  **簡化**：耳石在膠狀層裡，不是在水裡漂；片中「裡面還有很小的顆粒，被地球往下拉」不說顆粒浮在水裡。「加速、煞車」是直線移動的口語說法。

## C03 一杯水的比喻【比喻，撰稿自己的】

- **可用說法**：「我們借一杯水來想。車子一轉彎，杯子裡的水就晃到一邊；一煞車、一加速，水也跟著晃。」（p024–p026）比喻的限度（p029–p030）。
- **來源**：日常可見；對應 [4] 的「fluid … moves」。
- **可信度／注意**：比喻本身不是主張。限度片中有講（內耳很小、轉動與直線移動分開管）。

## C04 眼睛、腳底與肌肉也會報告你在動【公認】

- **可用說法**：「會。眼睛看外面的東西怎麼跑，也在告訴大腦你在動。腳底跟肌肉，也會報告。」（p032–p033）
- **來源**：[4]、[1]
- **可信度／注意**：高。NIDCD [4]：「Your sense of balance relies on a series of signals to your brain from several organs and structures in your body, specifically your eyes, ears, and the muscles and touch sensors in your legs.」CDC [1] 的衝突是「vestibular, visual, and kinesthetic inputs」。「腳底」＝腿部的觸覺感受器，**簡化**。

## C05 走路時，眼睛看到路往後退，杯子裡的水也在晃，大家說的都一樣，大腦就放心【撰稿推論】

- **可用說法**：p035–p036
- **來源**：[1]、[18]
- **可信度／注意**：中。CDC [1] 說症狀來自輸入與預測對不上；Oman & Cullen [18]：主動移動時的前庭輸入會被「expected consequences of self-generated movement」抵銷，並說明「human immunity to normal self-generated movement」。走路時訊號一致、不會暈，是由此推得的日常例子，**撰稿推論**。

## C06 看漫畫時：漫畫跟著你晃，眼睛報告沒動；車子轉彎，內耳報告在轉；兩邊的報告對不上【公認解釋的典型例子】

- **可用說法**：p039–p047
- **來源**：[2]、[3]、[1]
- **可信度／注意**：高。NHS [2]：「The inner ear sends different signals to your brain from those your eyes are seeing. These confusing messages cause you to feel unwell.」並列「do not read, watch films or use electronic devices」。Cleveland Clinic [3]：「It happens when your eyes, inner ear and body send conflicting messages to your brain.」CDC [1]：避免閱讀「Shown to reduce motion sickness in a variety of transport or simulator environments」。

## C07 遮住眼睛的乘客照樣會暈：英國實驗，郊區坐車三十分鐘，蒙眼的人跟看不到前面的人差不多一樣暈；所以閉上眼睛不一定能讓大腦安靜【研究看到的現象】

- **可用說法**：開場預告 p007；回收 p050–p053
- **來源**：[7]
- **可信度／注意**：高。Griffin & Newman [7]（Southampton）：「a 30-min suburban car journey」「4 experiments using 15 different conditions, with 20 subjects in each condition」「Absence of a visual field (blindfolded) resulted in similar sickness to that with no external forward view (with or without a side view).」
  「照樣會暈」＝蒙眼並沒有比看不到前方的人好，**簡化**。「閉上眼睛不一定能讓大腦安靜」故意說「不一定」：NHS [2] 把閉眼慢慢呼吸列為可以試的事，其他實驗結果不一（舊查核 S20 記 Wada & Yoshida 2016、Bos 2005），片中不說閉眼沒用，也不說閉眼有用。

## C08 大腦會先猜；報告跟預想對不上就會不舒服；這叫感覺衝突，是目前最多人接受的解釋，不是全部的答案【公認的模型，標成解釋】

- **可用說法**：p055–p059；第三章「這是感覺衝突說得通的地方」（p112）、「這就是這個解釋的界線」（p126–p127）
- **來源**：[1]、[16]、[5]、[6]
- **可信度／注意**：高。CDC [1]：「The most widely accepted explanation for motion sickness is the sensory conflict or neural mismatch theory.」衝突是輸入與「the expected patterns as predicted by an 'internal model'」之間（舊查核引的原句，WebFetch 摘要同義）。Golding 2016 [16]：「The "how" of motion sickness (i.e., the mechanism) is generally accepted to involve sensory conflict」。Lackner [5]：「A fully adequate theory of motion sickness is not presently available. A sensory conflict theory can explain many but not all aspects of motion sickness elicitation.」——片中「還不是全部的答案」的依據。

## C09 英國三千多位遊覽車乘客：完全看不到前面路的人，不舒服的比例大約是看得很清楚的人的三倍【研究看到的現象（相關性調查）】

- **可用說法**：p061–p063
- **來源**：[8]
- **可信度／注意**：高。Turner & Griffin [8]：「A questionnaire survey of 3256 coach travellers」「Passenger illness occurrence was approximately three times higher for passengers with no view of the road ahead (mean, 34.6%) compared to passengers who could see the road ahead extremely well (mean, 12.7%).」片中說「問過」，因為是問卷調查；不說因果。

## C10 只看得到側窗跟看不到前面差不多；看得到前面的路才比較不暈；那個實驗裡坐哪一排沒有明顯差別【研究看到的現象】

- **可用說法**：p064–p068
- **來源**：[7]
- **可信度／注意**：高。[7]：「no external forward view (with or without a side view)」與蒙眼相似；「A wide or narrow forward view (with or without a side view) reduced sickness.」「For the conditions of these experiments, seating position did not significantly affect sickness.」片中說「那個實驗裡」，不擴大成所有車。

## C11 所長的想法：前面的路一彎，眼睛先看到，大腦就猜得到水等一下要晃【所長的想法（標成意見）】

- **可用說法**：「我的想法是：前面的路一彎，眼睛先看到，大腦就猜得到，杯子裡的水等一下要晃。」（p069–p070）
- **來源**：[9]、[11]
- **可信度／注意**：意見。Kuiper 2018 [9]：「Carsickness is associated with a mismatch between actual and anticipated sensory signals.」Kuiper 2020 [11]：「Being able to anticipate upcoming motion is known to potentially mitigate sickness」。看到前方路有助預期，是作者群的方向，片中標成所長的想法。

## C12 荷蘭實驗：乘客在車上看螢幕找東西，螢幕擺在前窗高度、看得到外面，比擺在低處比較不暈【研究看到的現象】

- **可用說法**：p071–p072
- **來源**：[9]
- **可信度／注意**：高。Kuiper, Bos & Diels [9]（VU Amsterdam）：「Seated in the front passenger seat 18 participants were driven a 15-min long slalom … while performing a continuous visual search-task. The display was positioned either at 1) eye-height in front of the windscreen, allowing peripheral view on the outside world, and 2) the height of the glove compartment … Using a display at windscreen height resulted in less carsickness compared to a display at glove compartment height.」

## C13 司機很少暈；以色列實驗：二十二對人接受會讓人暈的旋轉，每一對一模一樣，只有一個人能控制；能控制的那一個不舒服明顯比較少【研究看到的現象】

- **可用說法**：p075–p080
- **來源**：[10]、[1]
- **可信度／注意**：高。Rolnick & Lubow [10]（Israeli Naval Hyperbaric Institute, Haifa），標題「Why is the driver rarely motion sick?」；「Twenty-two pairs of yoked subjects were exposed to nauseogenic rotation. One subject of each pair had control over the rotation and head movements, while the other was exposed passively to the same motion stimulus. Subjects who had control reported significantly fewer motion sickness symptoms」。CDC [1]：「there is evidence that perception of "controllability" is important」（以司機為例，並註明乘客做不到）。
  **示意**：摘要沒說旋轉裝置的樣子，片中說「會轉的機器」，圖 `swivel-chair` 畫一張旋轉椅是示意。

## C14 研究者的解釋：自己要轉彎，大腦早就知道，水一晃剛好跟它猜的一樣【研究者提出的解釋】

- **可用說法**：「研究的人認為：自己要轉彎，大腦早就知道，杯子裡的水一晃，剛好跟它猜的一樣。」（p081–p082）
- **來源**：[18]、[10]
- **可信度／注意**：中高，標成「研究的人認為」。Oman & Cullen [18]：主動移動時的輸入「are canceled by a mechanism comparing the expected consequences of self-generated movement … with the actual sensory feedback」，並說這與「the notable difference in motion sickness susceptibility of drivers as opposed to passengers」一致（「We propose」）。Rolnick & Lubow [10] 以「feed-forward mechanisms」討論。

## C15 用聲音先提醒下一步往哪動，知道接下來會怎樣的人也比較不暈；那個實驗是軌道上的滑車，不是山路【研究看到的現象＋限度】

- **可用說法**：p083–p087
- **來源**：[11]
- **可信度／注意**：高。Kuiper et al. [11]：「Participants (N = 20) were exposed on a sled on a rail track … The auditory cues were either 1) informative on the timing and direction of the upcoming motion, or 2) non-informative … average illness ratings were significantly lower for the condition that contained informative auditory cues」。研究由 Ford 贊助（摘要的利益聲明）；小問「就像爸爸先喊一聲要轉彎囉？」所長只說「有點像」並交代限度。

## C16 反過來：坐在沙發上看賽車畫面，眼睛說在動、身體沒動，也有人會暈，叫視覺引起的暈動症；電影院大銀幕、虛擬實境、駕駛模擬器都有人遇過【研究看到的現象】

- **可用說法**：開場預告 p008；p090–p101
- **來源**：[12]、[1]、[3]、[16]
- **可信度／注意**：高。Keshavarz et al. 2015 [12]：「VIMS is a sensation very similar to traditional motion sickness (MS), with the difference being that physical movement is usually limited or absent during VIMS」「Depending on the application, VIMS has also been labeled as Cinerama sickness (VIMS in movie theaters), cybersickness (VIMS in VR users), simulator sickness (VIMS in driving or flight simulators), or gaming sickness (VIMS during video game playing).」Cleveland Clinic [3]：「Some people get a kind of motion sickness while playing video games and virtual reality games」。CDC [1]：VR 與模擬器的眼睛疲勞、頭痛比真實環境多。Golding 2016 [16]：「The recent introduction of new visual technologies may expose more of the population to visually induced motion sickness.」
  「也有人會暈」「都有人遇過」故意說得保守，不給比例。素材審視（`material-20261111`）說缺的就是這一類來源。

## C17 火車錯覺：停在月台時旁邊那列開走，會覺得是自己這列在動，叫自己在動的錯覺；看出來的暈常跟它一起出現，可是有錯覺的人不一定會暈，兩者怎麼連還在爭論【現象＋未定】

- **可用說法**：p104–p109
- **來源**：[12]
- **可信度／注意**：高。[12]：「A typical real-life example of vection is the train illusion, whereby seeing the movement of a neighboring train creates the illusion that one's own stationary train is moving.」「it is clear that VIMS is typically accompanied by vection, but that vection can clearly be experienced in the absence of VIMS.」「To date, it is still a matter of debate as to whether vection is a necessary prerequisite for visually induced motion sickness」。

## C18 自己玩賽車遊戲的人，比看同一段錄影的人少說會暈【研究看到的現象】

- **可用說法**：p113–p118
- **來源**：[13]
- **可信度／注意**：高。Dong, Yoshida & Stoffregen [13]：「one member of each pair of participants played a driving video game … A recording of that performance was viewed … by the other member of the pair. Thus, the two members of each pair were exposed to identical visual motion stimuli … Participants who drove the virtual vehicle (drivers) were less likely to report motion sickness than participants who viewed game recordings (passengers).」片中「比較少說會暈」照原文 report。

## C19 車上用螢幕即時播前面的路，沒有比較不暈；研究者說還要弄清楚哪些畫面會讓人暈、哪些能讓人不暈【研究看到的現象＋未知】

- **可用說法**：p119–p127
- **來源**：[7]
- **可信度／注意**：高。[7]：「The provision of a real-time video view of the road ahead did not reduce motion sickness.」「It is concluded that sickness in cars is dependent on the visual scene. The minimization of sickness by the provision of visual information requires improved understanding of those factors that combine to cause and suppress sickness.」
  「這就是這個解釋的界線：它說得出哪裡對不上，卻還不能每次準準地說，誰會暈、暈多少」是所長對 [5]「can explain many but not all aspects」的口語轉述。

## C20 最容易暈和最不容易暈的人，差了大約一萬倍【研究者的估計】

- **可用說法**：「有研究估計，最容易暈和最不容易暈的人，差了大約一萬倍。」（p132–p133）
- **來源**：[5]
- **可信度／注意**：高。Lackner [5]：「The range of vulnerability in the normal population varies about 10,000 to 1.」片中說「有研究估計」「大約」。

## C21 兩歲以下通常不太會暈，之後越來越容易，七到十二歲最容易，再慢慢變少；女生比男生容易一點，但這個差別比年紀小得多；常偏頭痛的人比較容易暈；雙胞胎研究發現很大一部分跟遺傳有關【整理過的現象】

- **可用說法**：p135–p139
- **來源**：[1]、[14]
- **可信度／注意**：高。CDC [1]：「Children under 2 years of age do not usually experience motion sickness.」「peaks between the ages of 7 and 12 years」，之後隨年齡下降；「women are more susceptible than men, but this is a much smaller effect than age」；「People with a history of migraine, vertigo, or vestibular disorders are more prone to motion sickness」；「a large proportion of individual variation in susceptibility is due to genetic factors」。Reavley et al. [14]：3,652 名成年女性雙胞胎，「heritability for a motion sickness factor score estimated as 57%」，兒童期 70%。片中不給百分比，只說「很大一部分」。

## C22 背後真正的原因還不清楚；遊覽車調查也看到年紀越大、越常坐車的人越少暈【未知＋現象】

- **可用說法**：p141–p142
- **來源**：[14]、[8]
- **可信度／注意**：Reavley [14]：「the underlying determinants of individual susceptibility to motion sickness remain unclear」。Turner & Griffin [8]：「Travel sickness decreased with increasing passenger age and greater travel experience.」只講觀察，不說「多坐幾次就會好」。**未知**：為什麼個人差這麼多。

## C23 為什麼對不上會想吐，還沒解開；有人猜是身體把它當成中毒（毒物的猜法），有證據支持也有證據對不上，還沒定案；另一派認為跟身體穩不穩有關，有實驗看到不舒服之前身體就晃得比較厲害【假說，兩派都未定】

- **可用說法**：p143–p150
- **來源**：[6]、[15]、[16]、[17]、[19]、[5]
- **可信度／注意**：
  - 「說得出怎麼引起、說不出為什麼是想吐」：Golding 2006 [6]：「Current hypotheses of the 'Why?' of motion sickness are still under investigation … By contrast, the 'How?' of motion sickness is better understood in terms of mechanisms (e.g., 'sensory conflict' or similar)」。**未知**。
  - 毒物的猜法：Treisman 1977 [15]（Science）提出：神經毒素會擾亂感覺與動作控制，「the main function of the emesis being to rid the individual of ingested neurotoxins. Its occurrence in response to motion would be an accidental by product of this system.」**假說**。Oman 2012 [17]：「Treisman's "poison" theory is plausible, and frequently cited as the accepted scientific explanation … supporting evidence is equivocal, and contradictory evidence exists」。片中只說「有人提過一個猜法」「還沒定案」，不說它是答案。
  - 另一派：Stoffregen & Smart 1998 [19]：站在「moving room」裡，「increases in postural sway before the onset of subjective motion sickness symptoms. This confirms a key prediction of the postural instability theory」。**假說（對手理論）**。Keshavarz 2015 [12] 也把 postural instability theory 列為另一種解釋。片中「有實驗看到」，不說這一派是對的。

## C24 研究的人找到一群腦細胞，被別人帶著動時反應特別大、自己動時比較安靜；他們猜這可能就是比對預想的地方；怎麼讓人想吐還沒找到【候選，未確認】

- **可用說法**：p151–p156
- **來源**：[18]、[16]
- **可信度／注意**：中高。Oman & Cullen [18]：「a subclass of neurons in the vestibular nuclei and deep cerebellar nuclei that respond preferentially to passive head movements. During active movement, the semicircular canal and otolith input … are canceled by a mechanism comparing the expected consequences of self-generated movement … with the actual sensory feedback.」「We propose that conditions producing persistent activity of these neurons, or their targets, stimulate nearby brainstem emetic centers-via an as yet unidentified mechanism.」Golding 2016 [16]：「putative "sensory conflict" neurons」。
  「被別人帶著動」＝passive；「比較安靜」＝輸入被抵銷，**簡化**。片中說「他們猜」「可能」。

## C25 收尾：小問的答案、所長的意見、留言題

- **可用說法**：小問 p160–p165（C06、C08、C14 的總結）；所長「我覺得最好玩的是：你會暈，是因為你的身體一直很認真，在算你怎麼動。」（p166–p167，標成意見，對應 C01）；留言題 p170。
- **來源**：同上各條。

## 不講、找不到來源的

- 藥物、貼片、薑、穴位手環：NHS [2] 有列，本集依企劃刪減條件不講、不查療效。
- 坐前座：NHS [2] 列「sit in the front of a car」，但 [7] 的小客車實驗座位沒有顯著差別，而且片子的主角八歲，不在片中提，只講「坐哪一排沒有明顯差別」。
- Wada 2012 的歪頭實驗、Bos 2005 船艙模擬器：有來源（舊查核），但方向畫不出來、不推進主線，不講。
- 「nausea 來自希臘文的船」（Golding 2016 [16]）：有來源，不推進主線，不講。
- 暈車的確切比例：只有 Turner & Griffin 的單一遊覽車調查（28.4%），片中不給「幾成人會暈」。
- 為什麼個人差這麼多、為什麼是想吐、衝突神經元怎麼接到嘔吐中樞：來源都說還不知道，片中照實說「還不清楚」「還沒找到」。
- Mayo Clinic 讀不到（403），沒有引用。

## 來源

1. CDC Yellow Book 2026, Motion Sickness (chapter author John F. Golding, updated 2025-04-23). https://www.cdc.gov/yellow-book/hcp/travel-air-sea/motion-sickness.html（2026-11-11 WebFetch 讀全文；curl 被 Akamai 擋）
2. NHS, Motion sickness (page last reviewed 2023-06-19, next review due 2026-06-19). https://www.nhs.uk/conditions/motion-sickness/（2026-11-11 curl 讀全文；頁面標的下次審閱日已過，內容仍是現行版本）
3. Cleveland Clinic, Motion Sickness (medically reviewed, last updated 2024-04-08). https://my.clevelandclinic.org/health/diseases/12782-motion-sickness（2026-11-11 curl 讀全文）
4. NIDCD (NIH), Balance Disorders (last updated 2018-03-06). https://www.nidcd.nih.gov/health/balance-disorders（2026-11-11 curl 讀全文）
5. Lackner JR (2014), Motion sickness: more than nausea and vomiting. Exp Brain Res 232:2493–2510. https://pmc.ncbi.nlm.nih.gov/articles/PMC4112051/（2026-11-11 Europe PMC fullTextXML 讀全文）
6. Golding JF (2006), Motion sickness susceptibility. Auton Neurosci 129:67–76. https://pubmed.ncbi.nlm.nih.gov/16931173/（摘要）
7. Griffin MJ, Newman MM (2004), Visual field effects on motion sickness in cars. Aviat Space Environ Med 75:739–748. https://pubmed.ncbi.nlm.nih.gov/15460624/（摘要）
8. Turner M, Griffin MJ (1999), Motion sickness in public road transport: passenger behavior and susceptibility. Ergonomics 42:444–461. https://pubmed.ncbi.nlm.nih.gov/10048305/（摘要）
9. Kuiper OX, Bos JE, Diels C (2018), Looking forward: In-vehicle auxiliary display positioning affects carsickness. Appl Ergon 68:169–175. https://pubmed.ncbi.nlm.nih.gov/29409631/（摘要）
10. Rolnick A, Lubow RE (1991), Why is the driver rarely motion sick? The role of controllability in motion sickness. Ergonomics 34:867–879. https://pubmed.ncbi.nlm.nih.gov/1915252/（摘要）
11. Kuiper OX, Bos JE, Diels C, Schmidt EA (2020), Knowing what's coming: Anticipatory audio cues can mitigate motion sickness. Appl Ergon 85:103068. https://pubmed.ncbi.nlm.nih.gov/32174356/（摘要）
12. Keshavarz B, Riecke BE, Hettinger LJ, Campos JL (2015), Vection and visually induced motion sickness: how are they related? Front Psychol 6:472. https://pmc.ncbi.nlm.nih.gov/articles/PMC4403286/（2026-11-11 Europe PMC fullTextXML 讀全文）
13. Dong X, Yoshida K, Stoffregen TA (2011), Control of a virtual vehicle influences postural activity and motion sickness. J Exp Psychol Appl 17:128–138. https://pubmed.ncbi.nlm.nih.gov/21604911/（摘要）
14. Reavley CM et al. (2006), Genetic influences on motion sickness susceptibility in adult women: a classical twin study. Aviat Space Environ Med 77:1148–1152. https://pubmed.ncbi.nlm.nih.gov/17086768/（摘要）
15. Treisman M (1977), Motion sickness: an evolutionary hypothesis. Science 197:493–495. https://pubmed.ncbi.nlm.nih.gov/301659/（摘要）
16. Golding JF (2016), Motion sickness. Handb Clin Neurol 137:371–390. https://pubmed.ncbi.nlm.nih.gov/27638085/（摘要）
17. Oman CM (2012), Are evolutionary hypotheses for motion sickness "just-so" stories? J Vestib Res 22:117–127. https://pubmed.ncbi.nlm.nih.gov/23000611/（摘要）
18. Oman CM, Cullen KE (2014), Brainstem processing of vestibular sensory exafference: implications for motion sickness etiology. Exp Brain Res 232:2483–2492. https://pubmed.ncbi.nlm.nih.gov/24838552/（摘要；Europe PMC 全文回 500）
19. Stoffregen TA, Smart LJ Jr (1998), Postural instability precedes motion sickness. Brain Res Bull 47:437–448. https://pubmed.ncbi.nlm.nih.gov/10052572/（摘要）
