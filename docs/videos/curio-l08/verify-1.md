# curio-l08 查核第 1 輪

2026-10-10，獨立查核代理（Claude Opus 5.5，不是撰稿者）。方法照 `.agents/skills/youtube-video/references/prompts/verifier-video.md`：先把 `video.json` 的主張列成清單，再逐一重開來源。抓取用 `curl`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1 秒以上；網頁搜尋用了 4 次（上限 5 次）。工具與抓回來的頁面在 `<home>/mokaair-work/videos/curio-l08/_tools/verify1/`（`fetch.sh`、`totext.py`、`dump.py`、`scan.py`、`apply.mjs`、`claims_patch.py`；改動前的備份是 `video.before.json`、`claims.before.md`）。沒有執行 git，沒有執行撰稿者的 `build.mjs`。

來源代號 S1–S19 同 [`research.md`](research.md)。這是歷史題材，「官方頁面」指主要或權威來源（當年與事後的大報報導、訃聞、Physics World、搞笑諾貝爾獎名單等）。

## 來源開啟結果

| 代號 | 網址 | HTTP | 備註 |
|---|---|---|---|
| S1 | https://www2.nau.edu/~gaud/bio372/class/readings/circ.htm | 200 | TIME 1991-09-23 全文轉載 |
| S2 | https://web.archive.org/web/20180613234536/https://www.nytimes.com/1991/09/10/world/2-jovial-con-men-demystify-those-crop-circles-in-britain.html | 200 | Wayback 存檔 |
| S3 | https://www.smithsonianmag.com/history/crop-circles-the-art-of-the-hoax-2524283/ | 200（curl） | 不在 `sources`；Wayback availability API 逾時、CDX 回空陣列，沒有可用的存檔 |
| S4 | https://physicsworld.com/a/coming-soon-to-a-field-near-you/ | 200 | |
| S5 | https://web.archive.org/web/20251111084343/https://www.britannica.com/biography/Doug-Bower | 200 | Wayback 存檔 |
| S6 | https://circlemakers.org/028_FT371.pdf | 200 | PDF，`pdftotext` 讀出 |
| S7 | https://improbable.com/ig/winners/ | 200 | 條目在「The 1992 Ig Nobel Prize Winners」標題下 |
| S8 | https://ufologie.patrickgross.org/press/independent4nov2000.htm | 200 | 剪報站轉載 |
| S9 | https://www.fwi.co.uk/news/crop-circle-maker-fined | 200 | 英鎊符號遺失（「fined 100 … pay 40 costs」） |
| S10 | https://www.fwi.co.uk/news/crime/farmers-tell-fw-of-stress-and-anguish-over-unwanted-crop-circle | 200 | |
| S11 | https://www.fwi.co.uk/arable/hidden-truths-of-crop-circles | 200 | datePublished 2010-06-01 |
| S12 | https://www.theguardian.com/environment/2022/sep/24/invasion-of-the-barley-snatchers-crop-circles-cost-farmers-thousands-in-lost-revenue | 200 | |
| S13 | https://circlemakers.org/cereal_entrepreneurs.html | 200 | The Independent 2004-07-06 轉載 |
| S14 | https://circlemakers.org/la.html 、 https://circlemakers.org/la2.html | 200／200 | |
| S15 | https://www.cicap.org/crops/en/jse_pr_en.pdf | 200 | |
| S16 | https://ufology.patrickgross.org/htm/cropbower01.htm | 200 | 次級來源 |
| S17 | https://hoaxes.org/weblog/comments/september_9 | 200 | |
| S18 | https://www.womensweekly.com.au/news/crop-circles-australia-tully/ | 200 | |
| S19 | https://circlemakers.org/new_documents.html | 200 | |
| 圖 1 | https://commons.wikimedia.org/wiki/File:Diablefaucheur.jpg | 200 | 公有領域；本機檔 SHA-1 與 Commons API 相同（`cc40df22…`，474×663） |
| 圖 2 | https://commons.wikimedia.org/wiki/File:CropCircleW.jpg | 200 | 作者 Jabberocky 釋出公有領域，2007-07-29 攝；本機檔 SHA-1 相同（`7d0bfa42…`，1334×857） |

## 主張表

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改動前 → 改動後 |
|---|---|---|---|---|---|---|
| 1 | 1991 年兩個英國老先生向報社承認 | `c8ck`、標題、說明、縮圖 | S1、S2、S17 | 200 | CONFIRMED | |
| 2 | 用一塊木板壓的 | `rr6y`、說明 | S1（「a 4-ft. long wooden plank」）；S2 引 Today 寫兩塊 | 200 | CONFIRMED（照 S1；差異已在 claims.md） | |
| 3 | 最早的只是一個圓 | `qnby` | S6、S19 | 200 | CONFIRMED | |
| 4 | 流傳的版本：飛碟降落的痕跡 | `njrb`、`legend-bullets` | S1：「Saucer enthusiasts argued that the cropland patterns marked the landing spots of UFOS」 | 200 | CONFIRMED（S1 有直接的句子，claims.md c6 已補） | |
| 5 | 帶電的旋風 | `wibu` | S1 | 200 | CONFIRMED | |
| 6 | 人類做不出來 | `ew5z` | S1、S2 | 200 | CONFIRMED | |
| 7 | 到 1991 年已登上時代雜誌 | `g48i` | S1（1991-09-23 那一篇就是報導自白） | 200 | CONFIRMED（見「懷疑但沒動」） | |
| 8 | 1678 年英國小冊，魔鬼一夜割光燕麥；是割掉不是壓倒 | `abr4`、`5p7h`、`legend-mowing-devil` | 圖 1 的 Commons 頁（小冊全文：「so neatly Mow'd by the Devil」）；年份 S4：「In 1678 a series of circles in Hertfordshire was attributed to the devil」 | 200 | CONFIRMED（Commons 這一頁與圖上都沒有印 1678，年份靠 S4 與同一木刻的另一個 Commons 檔） | |
| 9 | 兩個老朋友每週五喝一杯 | `mgp6`、`pub-chapter` | S6、S16 | 200 | CONFIRMED | |
| 10 | 兩人都是風景畫家 | `c9is` | S1 | 200 | CONFIRMED | |
| 11 | 住漢普郡；道格開畫框店 | `jkpy` | S17、S5、S6（「a gallery and picture-framing studio」） | 200 | CONFIRMED | |
| 12 | 道格移民澳洲，住了好幾年才回英國 | `zbdi` | S6（約 1958–1968）、S16 | 200 | CONFIRMED | |
| 13 | 在澳洲的報紙上讀到 | `2wsg` | S16、S6 | 200 | CONFIRMED | |
| 14 | 1966 年昆士蘭農夫說看到飛碟升空；蘆葦上一個圓，叫飛碟巢 | `f9m4`、`rqm4` | S18、S5、S4 | 200 | CONFIRMED | |
| 15 | 「道格對戴夫說，我們去做一個像飛碟降落過的」 | `nffc` | 對話原文只在 S3（不在 `sources`）；S6、S19、S13 有「make it look as if a flying saucer has landed」與「Doug told Dave about the … 'saucer nests'」 | 200 | CHANGED（引語的來源不在 `sources`，也沒有可開的存檔） | 道格對戴夫說，我們去做一個像飛碟降落過的。 → 道格跟戴夫講了這件事，想做得像飛碟降落過。 |
| 16 | 七〇年代後半，報導寫 1976 或 1978 | `97u4`、說明、`outro` | 1976：S3、S6、S19；1978：S1、S17 | 200 | CONFIRMED（當成分歧講） | |
| 17 | 最早用鐵棒，原本拴畫框店後門（圈內人的記述） | `u4nc`、`u8zr` | S19 | 200 | CONFIRMED（單源，已標明） | |
| 18 | 第一個圓直徑約九公尺 | `7mey` | S6（30ft／9m）、S19 | 200 | CONFIRMED | |
| 19 | 那是別人的田、別人的作物 | `4cqc` | S10 | 200 | CONFIRMED | |
| 20 | 做法四步；木板約 1.2 公尺 | `pub-steps`、`xm5r`–`zc29`、`sk9s` | S1 | 200 | CONFIRMED（4 呎＝1.22 公尺） | |
| 21 | 頭三年沒人注意 | `35mn` | S1 | 200 | CONFIRMED | |
| 22 | 太太先發現里程太多；剪報簿；再帶她去看一次（道格自己的說法） | `r3hc`、`9eku` | S16 | 200 | CONFIRMED（次級來源，已說成本人的說法；沒有「外遇」） | |
| 23 | 1980 年前後見報；標題「The Return of the Thing」 | `7kew`、`pub-headline` | S6（1980）；S1（1981） | 200 | CONFIRMED | |
| 24 | 氣象學者主張大氣現象；旋轉氣柱帶著帶電物質；電漿渦旋 | `fg56`、`prze`、`h763` | S1、S4（「a meteorologist and physicist」） | 200 | CONFIRMED | |
| 25 | 退休工程師合寫專書，賣了五萬多本 | `3njc` | S1 | 200 | CONFIRMED | |
| 26 | 兩人想證明跟天氣無關，把圓加成一組 | `2pze`、`9h95` | S4 | 200 | CONFIRMED（單源） | |
| 27 | 直線出現後氣象學者承認那些是人做的，但單純的圓仍可能是大氣現象 | `yru3`、`kqrd`、`xxc9` | S4 | 200 | CONFIRMED | |
| 28 | 1991 年霍金：不是惡作劇就是空氣渦旋 | `gyq3`、`ga8k` | S4 | 200 | CONFIRMED | |
| 29 | 數量：大英百科 200 多、Physics World 250 | `dq9t`、`zf26`、`expert-count-stats` | S5、S4 | 200 | CONFIRMED（旁白沒有給單一數字） | |
| 30 | TIME：每季 25–30 個 | `7mp5`、`expert-count-stats` | S1：「as many as 25 to 30 new circles each growing season」 | 200 | CHANGED（原文是上限） | 卡片「每季 25–30 個」→「每季最多 25–30 個」；旁白「每一季就有二三十個新的」→「每一季最多有二三十個新的」 |
| 31 | 模仿的人已經出現；愛好者向政府爭取經費 | `a755`、`wx2j`、`dj8u` | S1 | 200 | CONFIRMED | |
| 32 | 訃聞寫公開是戴夫的主意 | `zeib` | S6 | 200 | CONFIRMED | |
| 33 | 道格 67 歲、戴夫 62 歲 | `rh83` | S1 | 200 | CONFIRMED（戴夫的年齡單源） | |
| 34 | 最先登在小報 Today；9 月 9 日；標題 Men Who Conned the World | `v6zv`、`vrcc`、`confess-headline` | S2、S17 | 200 | CONFIRMED | |
| 35 | 肯特郡，當著記者的面做了一個圈；記者請來寫專書的研究者 | `2r37`、`vyy3`、說明 | S1（Sevenoaks） | 200 | CONFIRMED | |
| 36 | 「No human could have done this.」 | `confess-quote`、`9a4t`、說明 | S1 | 200 | CONFIRMED（逐字） | |
| 37 | 「I'm afraid we've been having you on.」「We have all been conned」 | `48iv`、`vnvf` | S1 | 200 | CONFIRMED | |
| 38 | 鑑定的結論 vs 現場的事實 | `confess-compare` | S1、S2 | 200 | CONFIRMED | |
| 39 | 之後在漢普郡對記者再做一次（另一件事） | `jfde` | S2：「Late today … in a field in Hampshire」 | 200 | CONFIRMED（與肯特的測試分開講，來源各自正確） | |
| 40 | 另一位研究者：沒什麼了不起，除了兩個身體很好的六十歲老人 | `xpcc`、`xx7q` | S2 | 200 | CONFIRMED | |
| 41 | 研究者後來改口；加拿大那一句 | `d5z5`、`5xuj` | S1、S2 | 200 | CONFIRMED | |
| 42 | 隔年拿到搞笑諾貝爾物理學獎 | `zf53` | S7（1992） | 200 | CONFIRMED（旁白沒有唸得獎理由） | |
| 43 | 1991 年夏天已有別人在做；超出兩人做得到的程度 | `ffic`、`ncp6`、`dauc` | S6、S13 | 200 | CONFIRMED | |
| 44 | 第二波創作者 | `h9vk` | S4 | 200 | CONFIRMED | |
| 45 | 藝術團體接案；客戶有麥片品牌、電信公司、電視節目 | `px5z`、`vxj4` | S13 | 200 | CONFIRMED | |
| 46 | 報社委託的圈：付農夫 £6,000，作物約值 £100 | `after-stats-fee` | S13（製作者 Dickinson 的回憶） | 200 | CONFIRMED（見「懷疑但沒動」） | |
| 47 | 最多兩千個獨立的形狀；1998 年電視台拍、一百個圓、約一分鐘一個 | `xeb8`、`vz6a`、`kxv8` | S4 | 200 | CONFIRMED | |
| 48 | 空拍照是 2007 年的瑞士（洛桑附近），不是英國 | `after-swiss`、`ccht` | 圖 2 的 Commons 頁（Le Chalet-à-Gobet, Lausanne，2007-07-29） | 200 | CONFIRMED | |
| 49 | 1996 年 7 月巨石陣旁；傍晚五點半醫生飛過，45 分鐘後才有 | `p2sw`、`fq9d`、`dmiu` | S14（1996-07-07） | 200 | CONFIRMED（當成流傳的說法講） | |
| 50 | 三個問題的卡片；圈內人：前一晚、三個人、2 小時 45 分；沒有自認；訪問沒錄音 | `after-three-steps`、`46n4`、`upfz` | S14 兩頁 | 200 | CONFIRMED | |
| 51 | 同一個月另一個圖形有 194 個圓 | `hx29` | S4（194）、S14（7 月 29 日） | 200 | CONFIRMED | |
| 52 | 有研究者說麥稈的節被電磁輻射拉長；批評者指出統計與取樣有問題；本來就會長得不一樣 | `ijkv`、`wtat`、`ikcn` | S4、S15 | 200 | CONFIRMED | |
| 53 | 物理學者：沒被證實也沒被推翻 | `zir6` | S4 | 200 | CONFIRMED | |
| 54 | 2017 年，60 公尺寬，兩英畝小麥；水桶募款 | `bih4`、`eirw` | S10 | 200 | CONFIRMED | |
| 55 | 2010 年另一座農場，進圈請投 £5 | `32xp` | S11 | 200 | CONFIRMED | |
| 56 | 衛報：2018–2022 年 92 個圈、£30,000、40 多個足球場 | `field-stats`、`sdxu`–`cff6` | S12 | 200 | CONFIRMED；範圍是英格蘭，卡片標題補上 | 2018–2022 年的損失（衛報的估算）→ 2018–2022 年英格蘭的損失（衛報的估算） |
| 57 | 2004 年埃夫伯里遊客中心：夏天八到九成生意與麥田圈有關 | `vsgd`、`md6j` | S13 | 200 | CONFIRMED（單源） | |
| 58 | 威爾特郡警方：這是刑事毀損 | `avsx`、說明 | S10 | 200 | CONFIRMED | |
| 59 | 2000 年一名男子認罪，被罰一百英鎊 | `vj4x` | S9（「fined 100 and ordered to pay 40 costs … after pleading guilty」） | 200 | CONFIRMED（英鎊符號遺失；英國治安法院，金額判為英鎊） | |
| 60 | 農民聯盟的人：跟闖進你家花園搞破壞一樣 | `ukvc` | S8 | 200 | CONFIRMED | |
| 61 | 戴夫在一九九〇年代過世 | `q5iu` | `sources` 沒有一條寫到他過世；找不到主要報紙的訃聞；只有次級資料寫 1996（另有 1997） | — | NOT FOUND（權威來源）→ 改成標明出處的說法 | 兩位老先生呢？戴夫在一九九〇年代過世。 → 兩位老先生呢？資料多寫戴夫九〇年代過世。 |
| 62 | 道格活到 2018 年，94 歲；晚年後悔公開 | `2jnb`、`u597` | S6 | 200 | CONFIRMED | |
| 63 | 圈內人記得他常說：那只是壓平的麥子 | `m657` | S19：「I'm sure his mischievous spirit will be … whispering to the audience "It's only flattened corn."」 | 200 | CHANGED（原文是圈內人想像他會說，沒有寫他常說） | 圈內人記得他常說：那只是壓平的麥子。 → 圈內人想像他會說：那只是壓平的麥子。 |
| 64 | 兩個人，十幾年 | `field-answer-big`、說明 | S1（13 年）；1976／1978–1991 | 200 | CONFIRMED | |
| 65 | 圖片說明與授權 | `assets`、兩個 `screenshot` | Commons 兩頁與 API | 200 | CONFIRMED | |

## 摘要

- 查了 65 項：確認 61、改動 3（#15、#30、#63）、找不到權威來源 1（#61，改成標明出處的說法）。另有 1 處補上範圍（#56，英格蘭），不算事實改動。
- 事實改動共 4 處，超過三處：**需要第二輪**（由另一個代理做）。
- 起始年份：旁白與說明都當成分歧講（1976 或 1978）。數量：旁白沒有單一數字，卡片各標出處。
- 肯特郡 Sevenoaks 的測試（S1）與漢普郡的公開示範（S2）分開講，來源各自正確。
- 引語：研究者的話、Bower 的回話、「We have all been conned」逐字對得上 S1；Andrews 的話對得上 S2；搞笑諾貝爾獎的得獎理由旁白沒有唸，claims.md 的引文與 S7 一致。`pub-idea` 的對話原文只在 Smithsonian，Wayback 沒有存檔，改用 `sources` 裡有的說法；說明欄沒有變動，長度不受影響。
- 太太與里程說成道格自己的說法；1678 年小冊說的是割掉；瑞士照片的說明寫明是瑞士；衛報的估算在卡片上有數字與出處。
- 2000 年的罰金只在旁白（`vj4x`，「罰一百英鎊」），`field-2000` 是插圖場景，沒有卡片；派工說明寫「罰金在卡片上」，與現況不符，沒有改版型（那是編排，不是事實）。£40 的訴訟費沒有出現在影片裡。
- 會過期的事實：沒有。影片沒有講「現在每年幾個」；衛報的數字標明 2018–2022。
- 意見：`sr6f`、`9wn4`、`pa32` 以「我的看法是」開頭，與 brief.md 的站主觀點一致。
- 內容守則：沒有評判任何真人；沒有編造的對話（`nffc` 改完之後也不是對話形式）；`4cqc`、`avsx`、`tiie` 與說明都講明在別人的田裡壓作物是刑事毀損。插圖 prompt 沒有任何真人姓名或長相描述；兩位老先生、研究者、氣象學者都是背影、手部或遠景；有臉的都是虛構的路人（農夫、遊客、小孩）。
- 聽感：沒有超過 40 字的句子；沒有查證口吻；旁白沒有拉丁字母、括號或網址；沒有先於介紹的 reveal。`97u4` 的「七八」可能聽不清楚（撰稿者已提）。
- lint：`node tools/video/cli.mjs lint --slug curio-l08` → 0 錯誤、1 條警告（outro 一句，撰稿者刻意的）；134 句、2,268 個單位、估 11.1 分鐘。每一句的 id 都保留，沒有增減場景或句子；改過的四句是 20、17、18、16 個單位。
- `shorts.json` 沒有用到改過的四句，不用跟著改（那個檔不在本輪可改的範圍）。

## 懷疑但沒動

- `g48i`「到一九九一年，這已經是登上時代雜誌的謎」：TIME 1991-09-23 那一篇報導的就是自白本身，不是自白之前把它當謎來報。句子字面上成立，但聽起來像是先成了謎才登上雜誌；站主可以考慮改寫。
- `after-stats-fee`：£6,000 與 £100 是製作者 Dickinson 在訪問裡的回憶（S13），卡片出處寫 The Independent，沒有標是製作者的說法。
- `vj4x`：S9 原頁英鎊符號遺失；The Times 2000-11-07 原文沒有取得。
- `q5iu`：改完仍然沒有權威來源說 Chorley 何時過世；如果站主想更穩，可以整句改成只講道格。
- `after-swiss` 的「洛桑附近」：Commons 寫的是 Le Chalet-à-Gobet, Lausanne（在洛桑市轄內）。
- `wtat`「統計和取樣都有問題」：S15 的原文是統計程序的誤用與任意捨棄不要的結果，「取樣」是意譯。
- S11 的年份：頁面日期 2010-06-01，文中寫「春季銀行假日後的星期二」發現、之後兩週人潮湧入；2010 年成立，但文章沒有直接寫年份。
- Smithsonian（S3）仍然不在 `sources`；claims.md 的 c2、c6 留著它的網址當背景。
