# C14 R4 source / written visual verification

Status: PASS — source and written prompts only.

Reviewer: /root/c14_r4_source (independent; no authorship of this episode, its research or R4 revision).

本輪實際核對：刪o03／t09／t10；改t11／m02／r02；刪成績表loop，將t11回收改接m02。親讀供應商原PDF p3及現行產品raw HTML，原件支持三維列印模具製出實體矽膠咬閥、單手關閉飲水管。新問法由製作動作直接回答，不補真人實咬結果、耐久分數、同SKU／同批次或歷史研發因果。

| File | SHA256 |
| --- | --- |
| video.json | ab3d5ae2987e1f6c753dd49d5df67624325dee12255001c981fe53ef9430417f |
| script.md | 873dd9e51e4d663bac06c4cc2b47f2dc32eb48f93d9bf104b60e613a304c18cf |
| narration-only.json | ad996deb9779c1e0bf3a856a4903ff4789ef24acae15fafb2212556005687304 |
| claims.json | ab0123d806a9f04ba69548f7868323a61f4f8d41acad3690df9776255c2c2991 |

R4 independent report: `reviews/source-r4-independent.json`, SHA256 `9535c2fb0ab330160dc8144e1f004127fe7ea390aa43bcc77a1a4856aef9d18b`.
R3 report: `history/r3/reviews/source-r3-independent.json`, SHA256 `3415016205e2450bfe9983ef2d2a70f77c1c2e467752f400a54208cd75103f43`.
R3 verify: `history/r3/verify-1.md`, SHA256 `63038e57eb6e5026705f4de283d1ce85f060c36f23398330cc4d3d1fa606b322`.

現存87句／85景／84插圖prompt、26loops、32anchors與145bindings全部驗證；四個口播投影完全一致。84完整line與82完整scene逐物件不變；所有現存英文prompt／camera逐字不變，兩項loop調整的語意與端點有效。15研究原件重新抽文與快取逐byte吻合；121保護檔及舊35原檔／35唯讀snapshots的SHA與bytes全部吻合。完整來源rawSHA、逐行locator／line mapping與保全SHA在R4 report。

35–45mL/s仍是專利申請人、特定口器及口含咬開後吸吮的條件自述；飲水管盤緊只說水「可能」積在低處。正文插圖比例100%，非結構卡連續0；image-01、唯一cute-mystery look與繁中／burn_in=true旗標保留。

CONFIRMED指原件支持記載；ATTRIBUTED指有歸屬的來源主張，非本片重現試驗；PLAN是提問、作者反應、假設或解讀。未變內容依固定R3來源PASS與全物件proof繼承，本輪不讀native／blind投票。

| ID | Claim | Verdict | Sources / anchors |
| --- | --- | --- | --- |
| c14r1h01 | 你背著三公升水，若管口一直滴，喝到以前就先漏掉；多裝水，能解決這件事嗎？ | PLAN | SWISS_CRUX / A28, A_CRUX_3L |
| c14r1h02 | 八〇年代末，德州一場單車賽裡，品牌回顧中的艾德森，把一袋水放到車衣背後。 | ATTRIBUTED | NZ_HISTORY, HH_HISTORY, COURT_MIRROR / A02, A05, A06, A07 |
| c14r1h03 | 袋子外面套著襪子，管子越過肩膀；我注意到的，卻是管口那枚衣夾。 | PLAN | NZ_HISTORY / A02, A03 |
| c14r1h04 | 後來，出口被送進模具，也被夾在模擬牙齒的金屬之間。 | PLAN | SW_PDF, SONOMA2015 / A18, A21 |
| c14r1h05 | 今天跟著CamelBak的一袋水，從背上身，走到下一次還能再喝。 | PLAN | NZ_HISTORY, PAT_MOUTH_PDF, TRADE2006, SW_PDF, CLEAN / A02, A10, A14, A19, A27 |
| c14r1h06 | 把水背上身之後，怎麼讓它在你要喝時出來，其他時候留在該在的地方？ | PLAN | NZ_HISTORY, PAT_MOUTH_PDF, CARE, CLEAN / A03, A10, A22, A27 |
| c14r1o01 | 那枚衣夾先替管端守住出口；紐西蘭品牌回顧說，艾德森就是用它夾住管子。 | ATTRIBUTED | NZ_HISTORY / A03 |
| c14r1o02 | 他是急救醫療技術員，回顧裡那袋水，用的原是點滴袋；襪子套在袋外，水仍裝在袋裡。 | ATTRIBUTED | NZ_HISTORY / A02 |
| c14r1o04 | 但把出口移到嘴邊，和讓出口自己關上，是同一件事嗎？ | PLAN | NZ_HISTORY / A02, A03 |
| c14r1o05 | 這套拼裝留下的，是手動夾閉：衣夾還要有人照顧，並不會因為你喝完，就自己回到管口。 | CONFIRMED | NZ_HISTORY / A03 |
| c14r1o06 | 我覺得，管子越過肩膀的意義，也在這裡：水已經來到嘴邊，控制水的機會也到了嘴邊。 | PLAN | NZ_HISTORY / A02, A03 |
| c14r1o07 | 如果放開嘴，出口就能關回去，你的手是不是能少管一件事？ | PLAN | NZ_HISTORY, PAT_MOUTH_PDF / A03, A10 |
| c14r1v01 | 後來的咬閥，把這個開關問題交給了嘴；其中一份口器專利，記下可變形的出口。 | CONFIRMED | PAT_MOUTH_PDF / A10 |
| c14r1v02 | 這份申請在一九九八年提出，二〇〇〇年獲准；它描述的出口，不是一個始終敞開的圓孔。 | CONFIRMED | PAT_MOUTH_PDF / A10 |
| c14r1v03 | 前端兩片相貼的部分，合起一條平常閉著的狹縫；水路已經接上，縫卻還沒打開。 | CONFIRMED | PAT_MOUTH_PDF / A10, A_MOUTH_P7 |
| c14r1v04 | 你若只想到把孔挖大，就漏掉了這個問題：不喝的時候，那個孔由誰補回去？ | PLAN | PAT_MOUTH_PDF / A10, A11 |
| c14r1v05 | 專利裡，牙齒壓住可咬的區域，口器變形，貼在一起的兩片才分開，形成出水口。 | CONFIRMED | PAT_MOUTH_PDF / A10, A_MOUTH_P8 |
| c14r1v06 | 力氣撤掉以後，彈性讓它回到閉合狀態；開和關，靠的是同一個零件的形變。 | CONFIRMED | PAT_MOUTH_PDF / A11, A_MOUTH_P8 |
| c14r1v07 | 我喜歡這個轉換：原先掛在外面的衣夾，換成出口本身會回復的形狀。 | PLAN | NZ_HISTORY, PAT_MOUTH_PDF / A03, A10, A11 |
| c14r1v08 | 可是，材料軟到能咬，為什麼不會放開以後，就一直扁在那裡？ | PLAN | PAT_MOUTH_PDF / A11 |
| c14r1v09 | 文件選材看的是能不能回到閉合狀態，並舉一種硬度的矽膠作例子；軟，還得能回彈。 | CONFIRMED | PAT_MOUTH_PDF / A11 |
| c14r1v10 | 口器的脖子接著管端，頭部留給嘴含住；那個整天碰到嘴的地方，怎麼清理？ | CONFIRMED | PAT_MOUTH_PDF / A_MOUTH_P7 |
| c14r1v11 | 專利說，口器能從管子上滑下來，再裝回去，方便清潔與維護。 | CONFIRMED | PAT_MOUTH_PDF / A_MOUTH_P7 |
| c14r1v13 | 文件裡還記了一組出水測試；咬開這條縫，水究竟能怎樣通過？ | PLAN | PAT_MOUTH_PDF / A_MOUTH_P8 |
| c14r1v14 | 用的是圖一到圖十那種口器，放進嘴裡、咬到出水狀態，再像吸管那樣吸水。 | ATTRIBUTED | PAT_MOUTH_PDF / A_MOUTH_P8 |
| c14r1v15 | 專利申請人自報的流量，是每秒約三十五到四十五毫升；數字裡，也包含人在吸的動作。 | ATTRIBUTED | PAT_MOUTH_PDF / A_MOUTH_P8 |
| c14r1v16 | 我讀這段時，最在意的是水路終於有了可觀察的結果：嘴一邊開口，一邊把水吸過來。 | PLAN | PAT_MOUTH_PDF / A_MOUTH_P8 |
| c14r1v17 | 這是那個設計記載的測試，還不是每一款袋子、每一個嘴，都會流出同樣的量。 | CONFIRMED | PAT_MOUTH_PDF / A_MOUTH_P8 |
| c14r1v18 | 可既然控制已經在嘴邊，水還非得背在背後嗎？ | PLAN | TRADE2006 / A14 |
| c14r1b01 | 二〇〇六年的展場報導裡，那個咬著喝的出口，已經搬到透明水瓶上。 | ATTRIBUTED | TRADE2006 / A14 |
| c14r1b02 | 記者寫的是七百五十毫升瓶，咬口可以翻起，下面接著瓶內一小段吸管。 | ATTRIBUTED | TRADE2006 / A14 |
| c14r1b03 | 你手裡換回瓶子，嘴邊卻不用換回一個敞開的瓶口；這才是讓我停下來看的地方。 | PLAN | TRADE2006 / A14 |
| c14r1b04 | 原先是管子越肩來找嘴，現在瓶子被手拿起，短管把瓶裡的水接到上面的咬口。 | PLAN | NZ_HISTORY, TRADE2006 / A02, A14 |
| c14r1b05 | 容器變了，讓出口在喝的時候打開，這個工作能一起搬過去嗎？ | PLAN | PAT_BOTTLE_PDF, TRADE2006 / A13, A14 |
| c14r1b06 | 同年公開的一份水瓶申請文件，描述了受壓變形的咬口，也引用先前那份口器專利。 | CONFIRMED | PAT_BOTTLE_PDF / A12, A13 |
| c14r1b07 | 裡面的構想仍是壓開、撤力回閉；換容器，不必連開關的原理都從頭換掉。 | CONFIRMED | PAT_BOTTLE_PDF / A13 |
| c14r1b08 | 可是，報導說它防漏，是記者測過，還是公司這樣說？ | PLAN | TRADE2006 / A14 |
| c14r1b09 | 防漏，是公司在報導裡的說法；這個展品，讓出口和容器的分工，出現在日常水瓶裡。 | ATTRIBUTED | TRADE2006 / A14 |
| c14r1b10 | 我覺得，這次不是背水的點子被丟掉，而是把能帶走的控制，留在另一種容器上。 | PLAN | TRADE2006 / A14 |
| c14r1b11 | 不過，瓶子拿起一次能喝，和袋子在身上反覆擠、反覆咬，能算同一場考驗嗎？ | PLAN | SONOMA2015 / A20, A21 |
| c14r1t01 | 背袋會受擠壓，水路也分成不同部件；二〇一四年年報，寫下當時的組合。 | CONFIRMED | CODI2014 / A17 |
| c14r1t02 | 那是聚氨酯袋體、管子，再接自封口器；同份年報的採購段，也列出聚氨酯膜。 | CONFIRMED | CODI2014 / A17, A30 |
| c14r1t03 | 你背著它走時，會彎動的是袋子，嘴邊一再受壓的，卻是另一個小部件。 | PLAN | CODI2014, SONOMA2015 / A17, A20, A21 |
| c14r1t04 | 所以，要看反覆使用，該把力氣加在哪裡？ | PLAN | SONOMA2015 / A20, A21 |
| c14r1t05 | 二〇一五年，記者走進加州佩塔盧馬的實驗室，看見水袋正在被壓、被扭。 | ATTRIBUTED | SONOMA2015 / A20 |
| c14r1t06 | 同時，十二個咬閥夾在兩片金屬之間，模擬大人和孩子的牙齒反覆咬壓。 | ATTRIBUTED | SONOMA2015 / A21 |
| c14r1t07 | 開場那副金屬牙齒，到這裡有了工作：不只碰一下出口，而是反覆讓它受力。 | PLAN | SONOMA2015 / A21 |
| c14r1t08 | 我覺得這個畫面比一句耐用有用得多；袋子和咬口，承受的動作根本不同。 | PLAN | SONOMA2015 / A20, A21 |
| c14r1t11 | 而螢幕上的咬口形狀，還不是你能碰到的軟零件；工程師先怎麼把它做出來？ | PLAN | SW_PDF / A18, A19 |
| c14r1m01 | 二〇一六年的供應商個案，訪問了設計工程師麥克里迪；他做的是一體、自封的矽膠咬閥樣件。 | ATTRIBUTED | SW_PDF / A18 |
| c14r1m02 | 螢幕上的形狀先變成三維列印模具；麥克里迪再用模具做出矽膠咬閥，手裡才有了能變形的實體。 | ATTRIBUTED | SW_PDF / A18, A19 |
| c14r1m03 | 如果要知道放開會不會回閉，你拿一塊硬的外形模型，能替軟零件回答嗎？ | PLAN | SW_PDF, PAT_MOUTH_PDF / A18, A19, A11 |
| c14r1m04 | 這次交到手裡的是可拿去測的矽膠件，形狀與材料，才有機會一起接受人的測試。 | ATTRIBUTED | SW_PDF / A18, A19 |
| c14r1m05 | 工程師回述，這樣兩天就拿到了測試零件；那個數字買到的是能試，不是已經證明不壞。 | ATTRIBUTED | SW_PDF / A19 |
| c14r1m06 | 我喜歡這個結果，因為下一個判斷不用只對著螢幕做；手裡已經有東西，能交給真的人。 | PLAN | SW_PDF / A18, A19 |
| c14r1m07 | 拿到軟樣件以後，工程師最想再取得什麼？ | PLAN | SW_PDF / A18, A19, A_SW_CONTEXT |
| c14r1m08 | 他說，越能從真人測試取得回饋越好；能被人試的出口，才有機會把感受帶回設計。 | ATTRIBUTED | SW_PDF / A18, A19, A_SW_CONTEXT |
| c14r1m09 | 可是，就算嘴邊會自封，補水時還有另一個開口必須打開；那裡也能守住水嗎？ | PLAN | CARE, SWISS_CRUX / A22, A28 |
| c14r1r01 | 補水口把你帶回袋子上；開場那款水袋的現行介紹，特別列了方便握住、重新灌水的把手。 | ATTRIBUTED | SWISS_CRUX / A28 |
| c14r1r02 | 這一款另有單手開關，讓你用一隻手關住飲水管。 | ATTRIBUTED | SWISS_CRUX / A28 |
| c14r1r03 | 我原先容易把不漏水，全想成嘴邊那一小塊；可是補水蓋，也是一個得關好的接面。 | PLAN | CARE, SWISS_CRUX / A22, A28 |
| c14r1r04 | 如果出口沒有滴，水卻從蓋邊跑出來，你會先看哪裡？ | PLAN | CARE / A22 |
| c14r1r05 | 原廠現行問答列出兩個可能原因：蓋子螺紋有砂粒，或者蓋內的密封圈扭了。 | ATTRIBUTED | CARE / A22 |
| c14r1r06 | 砂粒讓蓋子不能完整密合；那個黑色環若扭曲變形，也會破壞蓋口的密封。 | ATTRIBUTED | CARE / A22, A_CARE_CONTEXT, A_CARE_GRIT |
| c14r1r07 | 所以你手上看似已經轉緊的蓋子，裡面仍可能有一個地方，沒有貼好。 | PLAN | CARE / A22, A_CARE_CONTEXT |
| c14r1r08 | 能不能在背出去以前，讓這條縫先露出來？ | PLAN | CARE / A23 |
| c14r1r09 | 原廠的季前檢查，把水裝回袋子，蓋好後轉動、擠壓，觀察有沒有漏水。 | ATTRIBUTED | CARE / A23 |
| c14r1r10 | 這個動作讓蓋口也承受水與擠壓；觀察的位置，從嘴邊移到了整個裝水的袋子。 | PLAN | CARE / A23 |
| c14r1r11 | 我覺得，它沒有離開一開始的問題：讓水跟你走，還得知道它有沒有從別的地方先走掉。 | PLAN | CARE / A22, A23 |
| c14r1r12 | 可喝完、洗完之後，水反而不該再留在袋裡；這次要怎麼讓它出去？ | PLAN | CARE, CLEAN / A24, A25 |
| c14r1d01 | 洗後殘水，把水路反過來考了一次；原廠清潔頁說，角落、飲水管和咬口都可能留水。 | ATTRIBUTED | CLEAN / A25 |
| c14r1d02 | 你看到外面已經乾了，不表示管內和接縫，也一起乾了。 | PLAN | CLEAN / A25, A27 |
| c14r1d03 | 我覺得這是整段水路最刁鑽的反面：喝的時候要留住水，收起來以前，卻要把殘水送走。 | PLAN | CARE, CLEAN / A24, A25, A27 |
| c14r1d04 | 原廠的清洗範圍，因此不只是一個大袋子；水走過的管與咬口，也得接到清水。 | ATTRIBUTED | CLEAN / A25, A_CLEAN_CONTEXT, A_CLEAN_RINSE |
| c14r1d05 | 但洗掉殘留物以後，內壁還貼在一起，空氣要從哪裡進去？ | PLAN | CLEAN / A26 |
| c14r1d06 | 清潔頁給的動作，是把袋體撐開，讓內部通風；乾燥架把兩邊內壁分開，也讓水能排出。 | ATTRIBUTED | CLEAN / A26 |
| c14r1d07 | 出口能回閉，這時卻不能替內部乾燥；袋口得打開，貼合的內壁得分開。 | CONFIRMED | PAT_MOUTH_PDF, CLEAN / A10, A26 |
| c14r1d08 | 飲水管若緊緊盤起來，原廠說水可能積在低處；怎麼讓管內也有乾燥的路？ | PLAN | CLEAN / A_CLEAN_TUBE |
| c14r1d09 | 它排掉管裡的水，垂直掛起，並讓兩端敞開；乾燥不只留給袋子的內部。 | ATTRIBUTED | CLEAN / A_CLEAN_TUBE |
| c14r1d10 | 分件晾乾用到的是可拆零件；管與咬口各自留出的空間，也讓你能查看裡面是不是還有水。 | PLAN | CLEAN / A_CLEAN_CONTEXT |
| c14r1d11 | 再看一眼，才知道能不能收回去；原廠要你看的是什麼？ | PLAN | CLEAN / A27 |
| c14r1d12 | 原廠要求收存前再看接縫、角落、管子和接口，有沒有水滴或凝結；還有水，就繼續晾乾。 | ATTRIBUTED | CLEAN / A27 |
| c14r1d13 | 開場問水能不能留在該在的地方，到這裡，答案多了一個時間點：收起來時，它得離開。 | PLAN | CARE, CLEAN / A24, A27 |
| c14r1d14 | 我想，讓你下一次還能拿起這袋水的方便，就藏在這個沒有水的結尾裡。 | PLAN | CARE, CLEAN / A24, A27 |
| c14r1ct1 | 一袋水的方便，是把開、關與重新使用接成水路；容量留在背上，出口和接縫，卻都得被照顧。 | PLAN | NZ_HISTORY, PAT_MOUTH_PDF, CARE, CLEAN / A02, A03, A10, A22, A27 |
| c14r1ct2 | 你最常把水帶去騎車、走路，還是放在桌邊？留言告訴我，哪個小地方最讓你在意。 | PLAN |  /  |
| c14r1ct3 | 想知道熟悉的物品，怎麼把方便送到你手裡，歡迎訂閱，和我一起看那些真正起作用的小動作。 | PLAN |  /  |

Full body: 2571 spoken units, including cold open and voiced CTA (2465 + 106). Actual audio unmeasured; duration PASS/FAIL not issued. This source / written visual PASS is not a 13-minute, 720–840-second, TTS, generated-image or owner/media approval. Native/blind votes not read.
