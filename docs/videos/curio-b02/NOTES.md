# curio-b02 筆記

## 人物設定（2026-11-04）

獨立評審 2026-11-04 給 37/60（`score.md`，沒過：總分 < 42，「沒有假字」4 分）。主要問題：#21、#56 的假字在畫面主位，#62、#63、#126 的招牌與玻璃字也是假字；真實人物幾乎沒畫，被路人、小孩、手代替；開頭與結尾的「你」換了人；委員會官員、Shimano 發言人、律師是同一款黑髮西裝小人。下面每個角色一句固定外型，畫到那個角色的景都原樣貼進 `video.json` 的提示詞（取代 a young man、an official 這類泛稱），再接上該年代的限制句。提示詞裡不寫真名，名字只記在這裡。

**跟評審建議不同的地方（系列守則優先）**：評審建議把創辦人畫成一個看得到臉的年輕人。創辦人島野庄三郎 1958 年過世，到今年未滿 70 年；系列守則（`../history-curiosity/README.md` §內容守則：過世未滿 70 年不畫本人，可用剪影）和這集 `brief.md` 的畫面規則都不准畫本人，改這條要先問站主。所以創辦人、會長，以及後來查到約 1989 年過世的保羅朗格、2008 年過世的美國老技師，都畫成**固定外型的剪影**：人在畫面裡、出現在旁白講到他的那幾景，但沒有臉。站主若同意破例畫臉，只要把下表的剪影句換成有臉的描述，再重畫這幾景。

| 角色 | 固定英文描述 | 出現的景 |
| --- | --- | --- |
| 創辦人 島野庄三郎 Shozaburo Shimano（1921，剪影） | the founder, a slim young Japanese man in his late twenties shown only as a dark silhouette with no facial details, his outline made by a flat cap, short hair, a long canvas work apron over a collarless shirt with rolled sleeves | #4 open-sakai、#6 open-gear、#13 rule-finger、#128 close-answer（回呼同一間工坊） |
| 會長 島野容三 Yozo Shimano（2024，在世，剪影） | an older Japanese executive in his seventies shown only as a dark silhouette with no facial details, his outline made by swept-back hair and a dark suit | #102 bust-why（#101 是卡片，沒動） |
| 「你」：騎車的觀眾（串場，現代） | a young rider of about 25 with short black hair, a round friendly face, a green cycling cap and a mustard-yellow cycling jersey with dark shorts | #1 open-you、#35 index-you、#97 recall-you、#127 close-question |
| 美國消費品安全委員會官員 the commission（代表這個機關，1997–2026 同一張臉） | a US safety-commission official, a woman in her fifties with short silver-grey hair, rectangular black-framed glasses and a dark blue suit over a white blouse | #9 open-fine、#45 index-cut、#54 crank-fine、#56 crank-crime、#91 recall-notice、#110 late-fine |
| Shimano 發言人 the spokesman（代表公司的說法，1999–2026） | the company spokesman, a Japanese man in his forties with neat short black hair, round silver-rimmed glasses, a light grey suit, a white shirt and a dark-red tie | #58 crank-deny、#72 boom-pr、#114 late-claim、#115 late-deny、#118 late-cut |
| 德國總代理 保羅朗格 Paul Lange（創辦人本人，剪影；約 1989 年過世） | the German distributor, a tall German man shown only as a dark silhouette with no facial details, his outline made by swept-back hair, a long work coat and a tie | #22 abroad-stuttgart、#23 abroad-remember、#120 lange-reveal、#121 lange-name、#122 lange-buy、#126 lange-europe、#130 close-answer-c |
| 日經專欄作者 the Nikkei columnist | a Japanese newspaper columnist, a woman in her forties with a low black ponytail, thin gold-rimmed glasses and a grey turtleneck sweater | #106 late-nikkei、#107 late-nikkei-b |

### 不入畫（不畫臉；2026-11-04 協調者確認可用無臉剪影）

系列規則：在世或 1956 年以後過世的人不畫本人。下列的人不寫有臉的外型，只用上表的無臉剪影，或畫手、物件、場景：

| 人 | 原因 | 處理 |
| --- | --- | --- |
| 島野庄三郎（創辦人） | 1958 年過世 | 剪影：#4 #6 #13 #128 |
| 島野容三（會長） | 在世 | 剪影：#102 |
| 保羅朗格 Paul Lange（Paul Lange & Co. 創辦人，1949 年與妻子 Fernanda 在斯圖加特創業） | 約 1989 年過世：兒子 Bernhard Lange「在父親早逝後」於 1989 年接手（[bike-magazin.de 75 週年訪談](https://www.bike-magazin.de/magazin/hintergruende/shimano-xt-kannst-wieder-einpacken-interview-zum-75-geburtstag-der-paul-lange-and-co-ohg/)）；確切年份查不到，但一定晚於 1956 | 剪影：#22 #23 #120 #121 #122 #126 #130（原本有臉，已改） |
| 引述的美國老技師 | 2008 年過世 | 剪影：#31 |
| 島野家其他人、現任社長 | 在世 | 不畫：#17 只畫六個空畫框，#76 沒動 |

委員會官員、Shimano 發言人、日經專欄作者、#41 律師都是**不具名的綜合角色**，不對應任何具名的人，所以可以畫臉（協調者 2026-11-04 確認）。「你」是虛構的觀眾。

只出場一次、但要跟上面分得開的人：#41 index-court 告 Shimano 那家小公司的律師固定成 `a young American lawyer in his thirties with curly red hair and freckles, a tan corduroy jacket and a brown knit tie`（#42 握手的一隻袖子也是 tan corduroy）；#31 abroad-topgroup 引述的美國老技師（過世未滿 70 年）畫成剪影。島野家其他人（#17 六任社長）、新社長（#76）不畫；工人、店員、會計等無名人物沒有固定外型。

**年代限制**（貼在提示詞尾端）。全集通用句型：

`set in <year> <place>; period-accurate clothes, tools and vehicles; no hard hats, no high-visibility vests, no smartphones, no flat screens, no modern cars`

各段實際用的：

- 1921 堺：`set in 1921 Sakai, Japan; period-accurate clothes, tools and vehicles; no electric machines, no plastic, no modern bicycles, no hard hats, no high-visibility vests, no cars`
- 1950 年代日本（#15）：`set in the 1950s in Japan; …; no hard hats, no high-visibility vests, no computers, no plastic, no modern cars`
- 1949 斯圖加特（#121）：`set in 1949 Stuttgart, Germany; …; no plastic, no shipping containers, no forklifts, no hard hats, no high-visibility vests, no modern cars`
- 1965 紐約、1967 斯圖加特、1972 杜塞道夫、1973 美國、1987 美國、1991 加州、1997 華盛頓、1999 美國：同一句型，後半列該年代不能有的東西（貨櫃、塑膠箱、電腦、螢幕、手機、現代車、工地帽）
- 2020 年以後的景寫 `present day`，不加年代限制
- 畫到紙、文件、招牌、螢幕、店面的景另加 `no readable text, no letters, no signs with writing`

**改了 45 景的提示詞**（只動 `data.prompt`；旁白、順序、秒數、運鏡、卡片都沒動，其他 86 景一字未改，吃快取）：

- 人物固定：上表各角色的景。
- 假字：#21 改仰角、只留天空與樓牆、店面沒有招牌；#56 拿掉月曆，改成官員指著過了午夜的時鐘；#62 改成拉下鐵捲門的空街、沒有招牌；#63 推近到人和車、店面虛化；#126 改成德國總代理（剪影）站在一高一矮兩堆箱子之間（德國多四成、中國少三分之一），不畫招牌、國旗、地圖。
- 畫面對不上旁白：#3 只剩零件、沒有整車；#4 老婦改成創辦人掛木牌；#23 郵差改成德國總代理（剪影）拍著空白銅牌；#27 只畫一人改成兩個職員各接一支電話；#105 三張空椅改成書記官舉著兩份案卷（兩家大車廠）；#121 現代物流碼頭與反光背心改成 1949 年斯圖加特的石造零件店，創辦人保羅朗格以剪影站在門口。
- 一人一事、壞圖：#6、#18 只有手改成看得到的人；#11 臉被紙擋住；#13、#128 只有物件改成創辦人剪影；#17、#49、#54、#118 人太小；#31 三個人改成一人；#42 背後的流淚怪臉改成素面牆；#74 前景糊掉的大臉；#102 兩人搶畫面改成會長剪影。
- 錯時代：#15 1950 年代西裝配工地帽、#40 1987 年工作室裡的工地帽。

lint：只剩 9 個既有錯誤，全是「Shimano 不在 docs/videos/lexicon.json」；這個詞在提交 42b0585d1（分支 `claude/eloquent-hypatia-fxsz7j`）加進字典，這個 worktree 還沒有，跟提示詞無關。新增的兩個 warning（writing、sign 出現在三分之一以上的圖）是 `no readable text …` 那句重複造成的，不用處理。還沒有重畫；下一次 `keyframes --takes 3` 只會畫這 45 景（要先經站主授權）。

## 正向改寫（2026-11-04）

規則：MiniMax image-01 沒有反向提示詞，寫 no／not／without 反而會把那個東西畫出來，所以提示詞只寫要畫的東西（空白物件、素面牆、該年代的物件、剪影寫成「shown only as a dark flat silhouette against a bright window, the outline of …」）。

改了 50 景（只動 `data.prompt`，每句 350 字元以內；旁白、順序、秒數、卡片、camera 沒動，其他 73 景一字未改）：

open-you、open-nobike、open-sakai、open-gear、open-wait、open-fine、rule-unknown、rule-finger、rule-you、rule-family、abroad-ny、abroad-stuttgart、abroad-remember、abroad-dusseldorf、abroad-two、abroad-topgroup、index-you、index-rival、index-court、index-settle、index-cut、crank-whose、crank-giant、crank-fine、crank-crime、crank-deny、crank-small、crank-turn、boom-surge、boom-pr、boom-order、boom-cool、bust-freeze-b、recall-notice、recall-price、bust-why、late-class-b、late-nikkei、late-nikkei-b、late-fine、late-claim、late-deny、late-cut、lange-reveal、lange-name、lange-buy、lange-europe、close-question、close-answer、close-answer-c

- 剪影保留：創辦人（open-sakai、open-gear、rule-finger、close-answer）、會長（bust-why）、保羅朗格（abroad-stuttgart、abroad-remember、lange-reveal、lange-name、lange-buy、lange-europe、close-answer-c）、美國老技師（abroad-topgroup），全部改成正向的剪影句，不再寫 no facial details。
- 年代限制改成 `set in <year> <place>` 加該年代該有的東西（木推車、煤爐、轉盤電話、紙本檔案、手推車），上面「年代限制」一節的 no … 句型已不再使用。
- `no readable text …` 改成 blank／plain 物件與 plain bare wall；index-settle 改成雙手握手填滿畫面的特寫。
