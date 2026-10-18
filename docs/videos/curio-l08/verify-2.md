# curio-l08 查核第 2 輪

2026-10-10，獨立查核代理（Claude Opus 5.5；不是撰稿者，也不是第 1 輪的查核代理）。方法照 `.agents/skills/youtube-video/references/prompts/verifier-video.md` 的第 2 輪：重查第 1 輪改過的每一項、協調者在第 1 輪之後改的三處，再加第 1 輪確認項目的隨機三分之一，來源全部自己重開。抓取用 `curl`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1 秒以上；網頁搜尋用了 2 次（上限 5 次），搜尋結果的摘要不當證據，只用來找網址。工具與抓回來的頁面在 `<home>/mokaair-work/videos/curio-l08/_tools/verify2/`（`fetch.sh`、`totext.py`、`dump.py`、`sample.py`、`apply.mjs`、`claims_patch.py`、`nf.mjs`；改動前的備份是 `video.before.json`、`claims.before.md`；lint 輸出在 `lint-after.txt`）。沒有執行 git，沒有執行撰稿者的 `build.mjs`。

來源代號 S1–S19 同 [`research.md`](research.md)；主張編號同 [`verify-1.md`](verify-1.md)。

## 抽樣

第 1 輪 65 項裡確認的 61 項（#15、#30、#61、#63 以外），用 `sample.py` 抽 ⌈61÷3⌉ = 21 項：`random.Random(20261010082).sample(confirmed, 21)`，種子 `20261010082`。抽到 #1、#7、#9、#12、#14、#19、#20、#23、#28、#33、#35、#37、#38、#44、#47、#48、#50、#51、#53、#57、#59。#7、#59 剛好也是指定要查的項目；#46 與 #56 不在抽樣裡，因為協調者改過或第 1 輪補過，另外查。合計查 27 項。

## 來源開啟結果

| 代號 | 網址 | HTTP | 備註 |
|---|---|---|---|
| S1 | https://www2.nau.edu/~gaud/bio372/class/readings/circ.htm | 200 | TIME 1991-09-23 全文轉載，整篇讀過 |
| S2 | https://web.archive.org/web/20180613234536/https://www.nytimes.com/1991/09/10/world/2-jovial-con-men-demystify-those-crop-circles-in-britain.html | 200 | Wayback 存檔 |
| S4 | https://physicsworld.com/a/coming-soon-to-a-field-near-you/ | 200 | |
| S5 | https://web.archive.org/web/20251111084343/https://www.britannica.com/biography/Doug-Bower | 200 | Wayback 存檔 |
| S6 | https://circlemakers.org/028_FT371.pdf | 200 | PDF，`pdftotext` 讀出 |
| S7 | https://improbable.com/ig/winners/ | 200 | |
| S8 | https://ufologie.patrickgross.org/press/independent4nov2000.htm | 200 | The Independent 2000-11-04 轉載（逮捕的報導，沒有罰金） |
| S9 | https://www.fwi.co.uk/news/crop-circle-maker-fined | 200 | 原始 HTML 的位元組就是「fined 100 and ordered to pay 40 costs」，英鎊符號確實不在頁面裡 |
| S10 | https://www.fwi.co.uk/news/crime/farmers-tell-fw-of-stress-and-anguish-over-unwanted-crop-circle | 200 | |
| S12 | https://www.theguardian.com/environment/2022/sep/24/invasion-of-the-barley-snatchers-crop-circles-cost-farmers-thousands-in-lost-revenue | 200 | |
| S13 | https://circlemakers.org/cereal_entrepreneurs.html | 200 | The Independent 2004-07-06 轉載 |
| S14 | https://circlemakers.org/la.html 、 https://circlemakers.org/la2.html | 200／200 | |
| S16 | https://ufology.patrickgross.org/htm/cropbower01.htm | 200 | 次級來源 |
| S17 | https://hoaxes.org/weblog/comments/september_9 | 200 | |
| S18 | https://www.womensweekly.com.au/news/crop-circles-australia-tully/ | 200 | |
| S19 | https://circlemakers.org/new_documents.html | 200 | |
| 新 | https://web.archive.org/web/20140515090322/http://www.thisiswiltshire.co.uk/archive/2000/11/07/7393897.Man_fined___100_for_making_crop_circle/ | 200（curl 與 Node `fetch` 都是） | This Is Wiltshire（當地報紙）2000-11-07，Wayback 存檔；原始位元組有 `C2 A3`（£）。網址是從維基百科 Crop circle 條目的註腳找到的，維基百科只當索引 |
| — | https://www.thisiswiltshire.co.uk/archive/2000/11/07/7393897.Man_fined___100_for_making_crop_circle/ | 200 | 現站回 200 但頁面沒有內文，所以 `sources` 用存檔網址 |
| 圖 1 | https://commons.wikimedia.org/wiki/File:Diablefaucheur.jpg | 200 | 公有領域；Commons API 的 SHA-1 `cc40df22…` 與本機檔相同（474×663） |
| 圖 2 | https://commons.wikimedia.org/wiki/File:CropCircleW.jpg | 200 | Le Chalet-à-Gobet, Lausanne，2007-07-29，作者 Jabberocky 釋出公有領域；SHA-1 `7d0bfa42…` 與本機檔相同（1334×857） |

S3、S11、S15 也抓了（都是 200），這一輪要查的項目沒有用到。

## 主張表

### 第 1 輪改過的項目

| # | 主張（現在的說法） | 位置 | 來源 | HTTP | 判定 | 改動前 → 改動後 |
|---|---|---|---|---|---|---|
| 15 | 道格跟戴夫講了這件事，想做得像飛碟降落過 | `nffc` | S6：「Doug told Dave about the mysterious 'saucer nests' he'd read about in a newspaper」「make it look as if a flying saucer has landed」；S19：「making it look as if a flying saucer had landed」；S13：「it was purely about making it look as if a UFO had landed」；S4：「Bower recounted a story to his friend David Chorley」 | 200 | CONFIRMED（不是對話形式，三個來源都在 `sources`） | |
| 30 | 每季最多 25–30 個；「每一季最多有二三十個新的」 | `expert-count-stats`、`7mp5` | S1：「fashioning as many as 25 to 30 new circles each growing season」「for the past 13 years」 | 200 | CONFIRMED | |
| 56 | 2018–2022 年英格蘭的損失：92 個圈、£30,000、40 多個足球場 | `field-stats`、`sdxu`、`jrkx`、`cff6` | S12：「More than 40 football pitches’ worth of arable land has been affected by crop circles in England since 2018 … Farmers lost £30,000 in income between 2018 and 2022 as a result of 92 crop circles」 | 200 | CONFIRMED | |
| 61 | 兩位老先生後來怎麼樣了？（戴夫的過世年份不講） | `q5iu` | —（協調者改成問句，沒有事實主張） | — | CONFIRMED（沒有可查的事實；見「懷疑但沒動」） | |
| 63 | 圈內人想像他會說：那只是壓平的麥子 | `m657` | S19：「I'm sure his mischievous spirit will be looking down, chuckling to himself and whispering to the audience "It's only flattened corn."」 | 200 | CONFIRMED | |

### 協調者在第 1 輪之後改的三處

| # | 主張（現在的說法） | 位置 | 來源 | HTTP | 判定 | 改動前 → 改動後 |
|---|---|---|---|---|---|---|
| 61 | 見上 | `q5iu` | | | CONFIRMED | |
| 7 | 一九九一年，時代雜誌也寫了麥田圈 | `g48i` | S1 文末：「From Time Magazine, September 23, 1991, pg 59」 | 200 | CONFIRMED（新句不再暗示雜誌先把它當謎來報） | |
| 46 | 製作者說，一家報社委託，付了農夫六千英鎊；作物約值 £100；出處標「製作者自述」 | `after-stats-fee`、`zkst`、`ytin` | S13：「"We did a formation for the Daily Mail in a wheat field in Avebury," recalls Dickinson, "and the paper paid the farmer £6,000 for the equivalent of around £100 worth of crops"」；頁面日期 06 July 2004 | 200 | CONFIRMED（`zkst` 18 個單位） | |

### 隨機抽的 21 項

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改動前 → 改動後 |
|---|---|---|---|---|---|---|
| 1 | 1991 年兩個英國老先生向報社承認 | `c8ck`、標題、說明、縮圖 | S2：「Newspapers in London today published the claims of two local men」；S17：1991-09-09 Today | 200 | CONFIRMED | |
| 7 | 見上 | `g48i` | S1 | 200 | CONFIRMED | |
| 9 | 兩個老朋友每週五喝一杯 | `mgp6`、`pub-chapter` | S6：「They used to meet for a beer every Friday evening」；S16：「we used to go out on Friday evenings, to have a drink in the pub」 | 200 | CONFIRMED | |
| 12 | 道格移民澳洲，住了好幾年才回英國 | `zbdi` | S6：「18 years earlier … set sail on a £10 assisted passage to Victoria」（1976 往回 18 年）、「returned to Hampshire in 1968」；S16：「eight and a half years」 | 200 | CONFIRMED | |
| 14 | 1966 年昆士蘭農夫說看到飛碟升空；蘆葦上一個圓，叫飛碟巢 | `f9m4`、`rqm4` | S18：1966 年 1 月，香蕉農，「tall reeds were now woven into a 30-foot diameter circle」「flying saucer nest」；S4：「a UFO rising into the sky and leaving behind a circular "saucer nest"」；S5：Tully, Queensland | 200 | CONFIRMED | |
| 19 | 那是別人的田、別人的作物 | `4cqc` | S10：「creating a crop circle is criminal damage and an offence」「a loss in revenue to the farmer and landowner」 | 200 | CONFIRMED | |
| 20 | 做法四步；木板約 1.2 公尺；工具三樣 | `pub-steps`、`xm5r`–`zc29`、`sk9s` | S1：「a 4-ft. long wooden plank, a ball of string and a baseball cap with wire threaded through the visor as a sighting device」「Bower held one end of the string … the plank, held horizontally at knee level by Chorley as he circled around Bower」 | 200 | CONFIRMED（4 呎＝1.22 公尺） | |
| 23 | 1980 年前後見報；標題「The Return of the Thing」 | `7kew`、`pub-headline` | S6：「in 1980, in a field near Westbury, someone noticed … "The Return of the Thing", ran the headline」；S1：「spotted in 1981」 | 200 | CONFIRMED | |
| 28 | 1991 年霍金：不是惡作劇就是空氣渦旋 | `gyq3`、`ga8k` | S4：「in 1991, Hawking told a local newspaper that "crop circles are either hoaxes or formed by vortex movement of air"」 | 200 | CONFIRMED | |
| 33 | 道格 67 歲、戴夫 62 歲 | `rh83` | S1：「David Chorley, 62, and Douglas Bower, 67」 | 200 | CONFIRMED | |
| 35 | 肯特郡，當著記者的面做了一個圈；記者請來寫專書的研究者 | `2r37`、`vyy3`、說明 | S1：「near Sevenoaks, in the British county of Kent」「created the Sevenoaks circle while Brough looked on」「who had alerted Delgado」 | 200 | CONFIRMED | |
| 37 | 「I'm afraid we've been having you on.」「We have all been conned」 | `48iv`、`vnvf` | S1 | 200 | CONFIRMED（逐字） | |
| 38 | 鑑定的結論 vs 現場的事實 | `confess-compare`、`gffu`、`s5u9` | S2：「the genuine article, of the sort no human could have made」；S1 | 200 | CONFIRMED | |
| 44 | 第二波創作者 | `h9vk` | S4：「the pictographs they created inspired a second wave of crop artists」 | 200 | CONFIRMED | |
| 47 | 最多兩千個獨立的形狀；1998 年電視台拍、一百個圓、約一分鐘一個 | `xeb8`、`vz6a`、`kxv8` | S4：「up to 2000 individual shapes」「BBC filmmakers … a 100-circle roulette pattern in 1998 … at the remarkable rate of one every minute」 | 200 | CONFIRMED | |
| 48 | 空拍照是 2007 年的瑞士（洛桑附近），不是英國 | `after-swiss`、`ccht`、`assets` | 圖 2 的 Commons 頁與 API | 200 | CONFIRMED | |
| 50 | 三個問題的卡片；圈內人：前一晚、三個人、2 小時 45 分；沒有自認；訪問沒錄音 | `after-three-steps`、`6cv6`、`46n4`、`upfz` | S14：「The interview wasn't taped」「if they don't have to claim the Stonehenge formation」；la2：「It was made the previous night, by three people, in about two and three-quarters hours … he just didn't see it the first time」；訪問日 10 月 27 日 | 200 | CONFIRMED | |
| 51 | 同一個月另一個圖形有 194 個圓 | `hx29` | S14：「on July 29 … totalling 194 individual circles」；S4：「194 "crop circles"」 | 200 | CONFIRMED | |
| 53 | 物理學者：沒被證實也沒被推翻 | `zir6` | S4：「has ever been reconfirmed or disproved by subsequent studies」 | 200 | CONFIRMED | |
| 57 | 2004 年埃夫伯里遊客中心：夏天八到九成生意與麥田圈有關 | `vsgd`、`md6j` | S13：「Around 85 to 90 per cent of our custom during the summer months is connected to crop circles」 | 200 | CONFIRMED（單源） | |
| 59 | 2000 年一名男子認罪，被罰一百英鎊 | `vj4x` | This Is Wiltshire 2000-11-07（Wayback）：「A man was fined £100 after admitting damaging farmland while creating crop circles in Wiltshire」「Williams pleaded guilty」「also ordered to pay £40 costs by Devizes magistrates」；S9（引 The Times）同樣的數字，沒有符號 | 200 | CONFIRMED（金額與幣別都看到了；旁白不改） | `sources` 加一條（不是事實改動） |

## 2000 年的罰金怎麼定的

- S9（Farmers Weekly，轉述 The Times）的原始 HTML 就是「fined 100 and ordered to pay 40 costs」，符號不是抓取時掉的。
- S8（The Independent 2000-11-04）是逮捕當週的報導，在開庭之前，沒有罰金。
- 當地報紙 This Is Wiltshire 在 2000-11-07 的報導（Wayback 2014-05-15 的存檔）標題與內文都寫「£100」，另寫「£40 costs」與檢方說的「£200 damage」，原始位元組有英鎊符號。這是當年的報紙報導，數字與 S9 一致，幣別看得到，所以 `vj4x`「罰一百英鎊」維持原樣。
- 這一條加進 `video.json` 的 `sources`（放在 Farmers Weekly 2000-11-07 那一條後面，`sources` 現在 19 條），`claims.md` 的 c37 與〈我懷疑但沒動的事〉也補上。Node `fetch` 用編輯部的 User-Agent 開這個存檔網址回 200。

## 摘要

- 查了 27 項（第 1 輪改過的 5 項含 #56 的範圍、協調者改的 3 處、隨機 21 項，扣掉重複）：確認 27、改動 0、找不到 0。
- 事實改動 0 處，**不需要再一輪**；沒有未解決的項目。
- 這一輪對檔案的改動：`video.json` 只多了一條 `sources`；`claims.md` 的 c37、〈我懷疑但沒動的事〉的罰金那一條與〈進度〉各補一句。旁白、卡片、縮圖、標題、說明都沒有動；每一句的 id 都在，沒有增減場景或句子。
- 2000 年的罰金：定案，£100（另有 £40 訴訟費，影片沒有講）。
- 會過期的事實：沒有。衛報的數字標明 2018–2022；影片沒有講「現在每年幾個」。
- 意見：`sr6f`、`9wn4`、`pa32` 以「我的看法是」起頭，重讀 brief.md 的〈站主觀點〉比對過（答案公布之後大家為什麼不信；不嘲笑相信的人；兩位老先生自己說那是玩笑），沒有不一致。
- 內容守則：改過的句子沒有評判任何人；`nffc` 不是對話形式；`zkst` 標明是製作者的說法；被罰的男子旁白不說名字。
- 圖片：兩張照片的 SHA-1 與 Commons API 相同，說明、作者與授權和 Commons 頁一致。
- 聽感（只回報）：這一輪看過的句子沒有超過 40 字的，沒有查證口吻，沒有拉丁字母、括號或網址。
- lint：`node tools/video/cli.mjs lint --slug curio-l08` → 0 錯誤、1 條警告（outro 只有一句，撰稿者刻意的）；134 句、2,259 個單位、估 11.1 分鐘。

## 懷疑但沒動

- `q5iu`「兩位老先生後來怎麼樣了？」問的是兩個人，接下來三句只回答道格（`2jnb`、`u597`、`m657`），戴夫沒有下文。這是編排，不是事實；站主如果在意，可以把問句改成只問道格。
- `g48i` 放在「流傳的版本」那一章，講的是 1991-09-23 那篇報導自白的文章；句子本身成立，位置由站主決定。
- This Is Wiltshire 的報導寫 Williams 做的是 West Overton 的七角星（8 月）；S8 寫的罪名是 Marlborough 附近、7 月。兩個來源的月份不同，影片沒有講月份也沒有講地點，不受影響。
- This Is Wiltshire 與 S9 都寫這是第一件這類起訴／罰金；影片沒有講「第一個」或「唯一」，維持不講。
- `claims.md`〈連結檢查〉那一節寫的「`sources` 的 18 條」是撰稿當時的紀錄，沒有改；現在是 19 條，新加的那一條這一輪用 Node `fetch` 開過。
- 第 1 輪留下的其他幾點（`wtat` 的「取樣」是意譯、S11 的年份靠頁面日期、Smithsonian 不在 `sources`）這一輪沒有抽到，狀態不變。
