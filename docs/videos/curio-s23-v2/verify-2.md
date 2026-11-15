# curio-s23-v2 查核第二輪（2026-11 重做稿）

- **查核日期**：2026-11-11。查核者沒有參與撰稿。
- **範圍**：`video.json` 的 `scenes[].lines[].text`，共 121 句（t001–t121）、117 景（`say` 只管讀音，沒有查）。另外查了 `curio-redo-handoff/drafts/curio-s23-v2/changes.md`：裡面寫【待查】0 條，但列了 12 句「意思不變、但說法改了」要查核方重新綁定（t004、t005、t006、t008、t015、t016、t027、t051、t086、t089、t113、t119），這 12 句逐條判定如下。
- **方法**：逐句把人名、年份、金額、數字、引號裡的話、誰說的、事件順序、「算不出來」「整筆」「從此」這類強詞，對照 `claims.md`、`verify-1.md`（第一版獨立覆核）與 `brief.md` 的史料界線。這次沒有只照抄前兩份，而是把 `video.json` 的 `sources` 列的五份固定文本**重新抓下來逐字核對**：
  - A65-39／40／41＝《5 Geo. III c.20》（1765）OCR 第 39–41 頁：https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Ruffhead-separate-pages/Ruffhead-10-separate-pages/Ruffhead-10-0089.txt （0090、0091 同目錄）
  - A73＝《13 Geo. III c.77》（1773）第 882 頁 §XXIX：https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Ruffhead-separate-pages/Ruffhead-11-separate-pages/Ruffhead-11-0882.txt （下稱「A73 第 n 行」）
  - H67＝John Harrison《Remarks on a Pamphlet Lately published by the Rev. Mr. Maskelyne》（1767，第二版）：https://github.com/GITenberg/Remarks-on-a-Pamphlet-Lately-published-by-the-Rev.-Mr.-Maskelyne-Under-the-Authority-of-the-B__37321/blob/24326a3040d42d57765f01b864279f1705aad4d4/37321-0.txt （下稱「H67 第 n 行」，行號是這個固定檔的行號）
  - 另外上網查了兩處：Royal Museums Greenwich〈How did astronomers including Nevil Maskelyne … help solve the longitude problem?〉https://www.rmg.co.uk/stories/topics/longitude-found-nevil-maskelyne-lunar-method （航位推算的誤差），以及 incoherency.co.uk 引 Jonathan Betts《Harrison》的拆錶開始日 https://incoherency.co.uk/blog/stories/principles-harrison-timekeeper.html （二手，只當旁證）。
- **結論摘要**：主幹沒有問題。三級賞金（60／40／30 地理英里對一萬／一萬五千／兩萬）、£2,500 與「相當的用處」、樸茨茅斯到布里奇敦「不逾十地理英里」、兩半的條件、六個月期限、五個月、德普特福德號與梅林號、三年後才看到計算、1766 年 5 月、海軍部存六個月、借錶被拒、四十八年、最多 £8,750、海軍財務官、「進一步的獎勵」都逐字對得上。**要改 5 句**：
  - open-sea「連往東西走了多遠都**算不出來**」太強：當時船上用航位推算估經度，只是估不準。
  - open-route、lab-pamphlet「他**自己印**的小冊子」：H67 書名頁寫的是 Printed for W. SANDBY，不是他自己印。
  - trial-petition「**為了這只錶**，來來回回好多年」：H67 說的「好多年」是從 1726 年起整個發明，不是這只錶（H4）。
  - half-open「一七六五年八月二十二日，他把錶拆開」：H67 說 8 月 22 日是講解**結束**的日子，不是拆開那天。
- changes.md 那 12 句重新綁定的句子：**全部通過**（t089 通過但記一筆）。

## 判定表

| 景 id | 句子（原文） | 判定 | 依據 | 建議改法 |
| --- | --- | --- | --- | --- |
| open-sea（t002） | 可是三百多年前的船，在海上連往東西走了多遠都算不出來。 | 要改 | 當時船上用航位推算（dead reckoning）估經度，不是「算不出來」，是誤差很大。RMG 上面那頁：Maskelyne 用月距法「only 1½° in error compared to errors of up to 10° from dead reckoning」。H67 第 83–85 行也只說要的是「a Method of finding out at Sea, how far we are got to the Eastward or Westward」。「三百多年」＝1714 到 2026，沒問題 | 可是三百多年前的船，在海上連往東西走了多遠都算不準。 |
| open-route（t010） | 我是檔案局的研究員，照兩部法案和他自己印的一本小冊子，從頭翻起。 | 要改 | H67 書名頁（第 45–53 行）：「By JOHN HARRISON. THE SECOND EDITION. LONDON: Printed for W. SANDBY in Fleetstreet. MDCCLXVII.」作者是他，印的是書商 Sandby。「自己印」查不到依據；「自己寫」查得到 | 我是檔案局的研究員，照兩部法案和他自己寫的一本小冊子，從頭翻起。 |
| trial-petition（t032） | 為了這只錶，他跟經度委員會來來回回好多年，終於申請到正式的海上試驗。 | 要改 | H67 第 398–406 行：「Having from the Year 1726, employed myself in adapting those Principles … and having made a Voyage to Lisbon and done sundry other Things during a Course of Years, mostly under the Direction of the Commissioners of Longitude … I thought the Invention sufficiently perfect about the latter End of the Year 1760, to go upon the ultimate Trial, which I accordingly applied for.」「好多年」說的是整個發明（含前三件），不是第四件這只錶 | 為了這一題，他跟經度委員會來來回回好多年，終於申請到正式的海上試驗。 |
| half-open（t079） | 可是他照做了：一七六五年八月二十二日，他把錶拆開。 | 要改 | H67 第 170–175 行：「When I made the Discovery … to six Gentlemen appointed by the Board of Longitude and to Mr. Maskelyne … which Discovery was finished on the 22d Day of August, 1765 … the Watch then remained in my Hands, all taken to pieces」。8 月 22 日是講解「完成」的日子。旁證：incoherency.co.uk 引 Betts《Harrison》：「It began on Wednesday 14 August 1765」。拆錶不是 22 日那天才開始，拿掉日子最安全 | 可是他照做了：一七六五年八月，他把錶拆開。 |
| lab-pamphlet（t091） | 隔年，他自己印了一本小冊子，專門反駁這套測法和計算。 | 要改 | 同 open-route：H67 第 51–53 行「Printed for W. SANDBY」「MDCCLXVII」。「隔年」（1767 對 1766）與「反駁測法和計算」（H67 第 330 行批評他拿「mean Time, instead of the corrected Time」比、第 361 行說比對的時刻前後差半小時到四小時四十八分）都對 | 隔年，他出了一本小冊子，專門反駁這套測法和計算。 |
| open-watch（t004，重新綁定） | 後來，一個做鐘的人，交出了一只帶得走的航海錶。 | 通過 | H67 第 407 行「the fourth or Watch」；A65-40「one other Watch Machine or Time Keeper」 | — |
| open-third（t005，重新綁定） | 錶帶上船橫過大西洋，誤差最多只有最高獎門檻的三分之一。 | 通過 | A65-40「from Portsmouth in Great Britain, to Bridgetown in the Island of Barbadoes」「did not lose its Longitude beyond ten Geographical Miles」；最高級是「one Half the same Distance」＝30（A65-39／40）。10/30＝1/3；「最多」保留「不逾」 | — |
| open-split（t006，重新綁定） | 但你想不到，議會沒有把錢整筆給他，而是把獎金拆成了兩半。 | 通過 | A65-40「one Moiety of the greatest Reward」「the other Moiety」 | — |
| open-gears（t007） | 他還得當著別人的面，把那只錶一件一件拆開。 | 通過 | H67 第 170–175 行：在六位受派者與 Maskelyne 面前講解，錶「all taken to pieces」；A65-40 要求講解原理到委員會滿意 | — |
| open-observatory（t008，重新綁定） | 錶後來還被送進天文台，有人一天一天記它走快還是走慢。 | 通過 | H67 第 118–127 行引 Maskelyne：1766 年 5 月 5 日收錶，「I most Days wound up and compared the Watch with the transit Clock」；第 161 行「the Watch's going from Day to Day」。原文是「most Days」，「一天一天」可以接受 | — |
| era-orange（t015，重新綁定） | 地球轉一圈是二十四小時，人們把這一圈分成三百六十度。 | 通過 | H67 第 87–95 行「The Earth's Surface is divided into 360 equal Parts … daily Revolution … in 24 Hours」 | — |
| era-four（t016，重新綁定） | 算法很直白：兩個地方差一度，正午就差大約四分鐘。 | 通過 | H67 第 94–98 行「must be just four Minutes, for 24 Hours being divided by 360 … for every Degree of Longitude we sail Westward, it will be Noon with us four Minutes the later」。原文是「just」，「大約」偏保守，不算錯 | — |
| era-compare、era-answer（t018–t019） | 錶說港口已經正午，頭頂的太陽卻還沒到……／代表船往西走了多遠 | 通過 | 同上第 96–98 行：往西每一度，本地正午晚四分鐘；方向對 | — |
| era-anymethod、era-tiers、era-top（t022–t024） | 賞金分成三級／六十個以內一萬；四十個以內一萬五千／最高那一級，要在三十個以內 | 通過 | A65-39：「ten thousand Pounds, if it determines the said Longitude to one Degree of a Great Circle, or sixty Geographical Miles; fifteen thousand Pounds … Two Thirds of that Distance」；A65-40「twenty thousand Pounds … one Half the same Distance」。40＝60 的三分之二 | — |
| era-miles（t025） | 地理英里，大約可以當成今天的海里。 | 通過 | A65-39 自己寫「one Degree of a Great Circle, or sixty Geographical Miles」，一地理英里＝大圓一角分，就是海里的定義；「大約」保留 | — |
| era-judged（t026） | 而且不是做出一只好錶就能領：得真的上船去試，再由委員會裁定。 | 通過 | H67 第 395–397 行引 1714 年法案：「when a Ship, under the Appointment of the said Commissioners, shall thereby actually sail from Great Britain to the West Indies …」；A65-40「in the Judgement of the said Commissioners」 | — |
| era-who（t027，重新綁定） | 那麼，後來接下這一題、跟它纏了大半輩子的，是誰？ | 通過 | A73 第 97–99 行「unremitting Industry for the Space of Forty-eight Years」；H67 第 398 行「from the Year 1726」、第 468–469 行「near forty Years of my Life」 | — |
| era-four-pieces、era-not-pendulum、era-three-kept（t029–t031） | 三件計時機器，第四件……帶得走的錶／不是把牆上的擺鐘搬上船／前三件機器還在他手上 | 通過 | H67 第 398–401 行（把擺鐘的原理改成「endure the Motion of a Ship」）、第 407 行；A65-40 三件機器照約交出；H67 第 517–518 行前三件「soon after demanded of me」。t030 沒說前三件是擺鐘，可以 | — |
| trial-who、trial-wait（t034–t035） | 是他的兒子威廉……／等正式命令，一等就是五個月 | 通過 | H67 第 406–408 行「My Son, after being sent to Portsmouth … was kept there five Months, waiting for Orders」 | — |
| trial-sail、trial-back（t037、t039） | 皇家海軍的德普特福德號，往牙買加去／回程，威廉改搭梅林號 | 通過 | H67 第 409–410 行「he went to Jamaica in the Deptford Man of War, and returned in the Merlin Sloop of War」 | — |
| trial-compare、trial-differ（t040–t041） | 兩地的觀測……／算出來的看法不一樣 | 通過 | H67 第 411–420 行：Portsmouth、Jamaica 的天文觀測；委員會派三人計算後宣布沒在限內；「I had the same Materials they had to calculate from」 | — |
| trial-refuse、trial-years（t043–t045） | 想指派自己信任的人去核對……照他自己的說法，沒有／過了幾年才看到 | 通過 | H67 第 415–416 行「I should name some Person to check the Computations, which was refused」；第 422–423 行「’till three Years afterwards」。都已歸給他 | — |
| trial-useful-b、trial-2500、trial-eighth（t048–t050） | 委員會多數認為……相當的用處／先給兩千五百英鎊……算進獎金／八分之一，還沒有判給他 | 通過 | A65-40「the major Part of the said Commissioners did adjudge the same to be of considerable Use to the Publick … two thousand five hundred Pound … to be deemed and taken as Part of such of the Rewards … as he might become intitled to」。2,500/20,000＝1/8 | — |
| trial-start（t051，重新綁定） | 這就是這場獎金拉鋸的起點：錶過了一趟海，錢只先給了一小袋。 | 通過 | 小結，沒有新事實（同上） | — |
| bb-sail、bb-route、bb-ten、bb-third（t053–t057） | 再請求一次海試……樸茨茅斯……布里奇敦……沒有差出十個地理英里……三分之一 | 通過 | H67 第 443–444 行第二趟於 1762 年底議定；A65-40 原文見 t005 | — |
| bb-doubt（t060） | 可是一七六五年的法案寫著：照舊法，這筆錢到底該怎麼付，有疑義。 | 通過（記一筆） | A65-40「Doubts may arise whether, by the Words of the said Act of the twelfth of Queen Anne, the said Commissioners can direct the Payment of the said Reward of twenty thousand Pounds … upon a Discovery of the Principles … and upon other Watches … being made」。原文的疑義是「照舊法的字面能不能照這些條件付」，旁白的「該怎麼付」是寬一點的說法，不算錯 | — |
| bb-reason（t061） | 理由是：方法要完整解釋、同樣的錶還做得出來，才可能普遍拿來用。 | 通過 | A65-40「may be made generally practicable … if the Principles … are fully discovered and explained, and other Watches or Time Keepers of the same Kind can be made」 | — |
| bb-harrison（t063） | 但哈里森不這麼看，他覺得海上測試，已經回答了最關鍵的問題。 | 通過 | H67 第 390–397 行：1714 年法案定的是「the last grand Test of the Merit of any such Invention」 | — |
| bb-moon（t065） | 同一部法案裡，議會也替算月亮位置的表，發了獎勵。 | 通過 | A65-41 §III Euler 不逾 £300；§IV Mayer 遺孀不逾 £3,000（交出月表產權後）；§V 改進月表不逾 £5,000 | — |
| half-first、half-four、half-deduct（t069、t071、t073） | 前半筆……六個月／前三件加這只錶產權轉給委員會／從這前半扣掉 | 通過 | A65-40「assigned to the said Commissioners, for the Use of the Publick, the Property of the three several Time Keepers … and also the Property of the said last mentioned Watch … deducting … two thousand five hundred Pounds」；A65-41 §II「within six Months after the passing of this Act」 | — |
| half-second、half-unclear（t075–t076） | 同類的錶要做出來，測到半度之內／還要委員會滿意……要做幾只、怎麼測，法案沒有直接寫 | 通過 | A65-40／41「other Time Keepers of the same Kind shall be made, and upon Trial … within half a Degree of a Great Circle, or thirty Geographical Miles, to the Satisfaction of the said Commissioners」；條文沒定數量與試法，H67 第 488–490 行「without determining how many … without defining the Mode of Trial」 | — |
| half-his（t078） | 哈里森的說法是：航程都跑完了，領獎的辦法卻換了一套。 | 通過 | H67 第 483–484 行「totally changing the Terms on which the Reward was to be given me」 | — |
| half-show、half-william、half-paid（t080、t082、t083） | 在委員會派來的人面前……講解構造／交錶那天，是威廉帶著錶到場／前半筆獎金，他拿到了 | 通過 | H67 第 171 行（six Gentlemen appointed by the Board）；第 183–184 行「upon receiving the Certificate for the Remainder of the first Moiety … I was ordered to deliver it to the Board. My Son, attending with it」；第 493 行「The first Moiety I obtained」。都歸給他 | — |
| lab-admiralty、lab-maskelyne（t085–t086，t086 重新綁定） | 錶先放在海軍部，後來送進格林威治／一七六六年五月，收下這只錶的，是皇家天文學家馬斯基林 | 通過 | H67 第 515–516 行「it remained six Months locked up at the Admiralty, and was then removed to Greenwich」；第 63–64 行「Mr. Maskelyne Astronomer Royal」；第 118–121 行「received it on the 5th of May, 1766」 | — |
| lab-doubt（t089，重新綁定） | 一天一天記下來，他對這只錶每天的快慢，提出了質疑。 | 通過（記一筆） | H67 第 161–167 行引 Maskelyne：「the Watch was getting from the very first near 20 seconds per day … seems to shew that the Watch cannot be taken to pieces and put together again without altering its Rate」；第 365–366 行他的結論「the Watch is not to be depended upon to determine the Longitude in a Voyage of six Weeks」。Maskelyne 的結論比「提出質疑」強，但旁白往弱的方向講，不算錯 | — |
| lab-fixed（t092） | 錶不必每天分秒不差，只要快慢固定、知道快多少，就能扣回來。 | 通過 | H67 第 105–113 行「it is only required that it should invariably perform it in some known Time … the Rate of its going … added to or deducted from the Time shewn」 | — |
| lab-adjust（t095） | 哈里森說，他交錶之前特地改過走速，所以不能拿航試時的速度判它。 | 通過 | H67 第 180–181 行「went on making some experiments, and alter’d the Rate of its going」；第 322–325 行 Maskelyne 知道它在巴貝多航程不是照平均時走、「its Rate of going had been since altered」 | — |
| lab-unread（t097） | 可惜對方的報告全文，我們這次沒有讀到。 | 通過 | 交代資料界線（claims.md lg712、brief B 案），不是史實主張 | — |
| lab-borrow（t098） | 他還請委員會把錶借回來，讓別的工匠照著做；他說，這個請求被拒絕了。 | 通過 | H67 第 529–534 行「praying that the Watch might be lent to me … for the Sake of employing other Workmen to make the different Parts by Model … Still have my Requests been refused」 | — |
| act-1773、act-48、act-public（t100–t101、t103） | 一七七三年……把哈里森的名字寫了進去／不間斷地做了四十八年／把構造原理公開了 | 通過 | A73 第 93–101 行「John Harrison of Red Lion Square … with unremitting Industry for the Space of Forty-eight Years … discovered the Principles of constructing the same」 | — |
| act-answer、act-unknown（t105–t106） | 同類的錶已經做出來了，而且走得相當準／沒寫是誰做的，也沒列出每一只在海上各差多少 | 通過 | A73 第 103 行「by which other Time-keepers have been already made, and found to answer with great Exactness」。原文是「great Exactness」，「相當準」偏保守；條文沒有製作者與各只誤差 | — |
| act-trade、act-8750（t107–t108） | 對航運和貿易有好處，於是授權一筆新的獎勵／最多八千七百五十英鎊，由海軍財務官支付 | 通過 | A73 第 105–113 行「great Benefit will arise to the Trade and Navigation … the Treasurer of His Majesty’s Navy … a Sum not exceeding Eight thousand seven hundred and fifty Pounds」 | — |
| tail-further（t111） | 條文寫的是「進一步的獎勵」，加在他之前已經拿到的錢之外。 | 通過 | A73 第 115 行「as a further Reward and Encouragement, over and above the Sums already received by him」 | — |
| tail-prize（t113，重新綁定） | 還記得開頭那兩萬英鎊嗎？兩半各實付了多少，條文沒有列出來。 | 通過 | A73 §XXIX 只寫「the Sums already received」，沒有列數目 | — |
| close-two、close-sea、close-more（t116–t118） | 那筆懸賞被拆成兩半，拆開的，其實是兩個問題……海上準不準……同樣的錶，做不做得出來 | 通過（記一筆） | A65-40 的理由（見 t061）。嚴格說前半的條件是公開構造、交出產權，不是「海上準不準」；這三句是旁白的詮釋，沒有說前半＝海上測試，可以照用 | — |
| close-line（t119，重新綁定） | 一只好錶，是一個人的本事；做得出第二只，才是所有船都能用的辦法。 | 通過 | 觀點句，換句話說 A65-40「generally practicable … other Watches … of the same Kind can be made」，沒有新事實 | — |

**其餘全部通過**（逐句看過，都是問句、轉場、「你」的旁白、比喻或旁白自己的反應，沒有暗含新事實）：t001、t003、t009、t011–t014、t017、t020–t021、t028、t033、t036、t038、t042、t046–t047、t052、t058–t059、t062、t064、t066–t068、t070、t072、t074、t077、t081、t084、t087–t088、t090、t093–t094、t096、t099、t102、t104、t109–t110、t112、t114–t115、t120–t121。

幾句通過但記下的地方（不用改）：

- t003、t011「英國」「一七一四年」：A65-39 稱它是「the twelfth Year of the Reign of Queen Anne」的法案；H67 第 390–391 行「an Act of Parliament passed so long ago as the Year 1714」。1714 年已是聯合後的大不列顛，說「英國」可以。
- t066「鐘跟天文不是只能贏一邊」是旁白的觀點；A65-41 同一部法案同時給錶與月表獎勵撐得住。H67 第 301 行說 Maskelyne「deeply interested in the Lunar Tables」，那是哈里森的指控，旁白沒採用，對。
- t072「四件東西，從此不歸他了」：A65-40 產權轉給委員會「for the Use of the Publick」；H67 第 517–518 行前三件被 Maskelyne 取走。成立。

## 要改的句子清單

- open-sea｜可是三百多年前的船，在海上連往東西走了多遠都算不出來。｜可是三百多年前的船，在海上連往東西走了多遠都算不準。
- open-route｜我是檔案局的研究員，照兩部法案和他自己印的一本小冊子，從頭翻起。｜我是檔案局的研究員，照兩部法案和他自己寫的一本小冊子，從頭翻起。
- trial-petition｜為了這只錶，他跟經度委員會來來回回好多年，終於申請到正式的海上試驗。｜為了這一題，他跟經度委員會來來回回好多年，終於申請到正式的海上試驗。
- half-open｜可是他照做了：一七六五年八月二十二日，他把錶拆開。｜可是他照做了：一七六五年八月，他把錶拆開。
- lab-pamphlet｜隔年，他自己印了一本小冊子，專門反駁這套測法和計算。｜隔年，他出了一本小冊子，專門反駁這套測法和計算。

旁白以外、同一個問題也要跟著改（本輪沒有改）：`youtube.description` 第二段「1765 年 8 月 22 日當著委員會派來的人拆錶」建議改「1765 年 8 月當著委員會派來的人拆錶（8 月 22 日講解完畢）」，「哈里森 1767 年印小冊子反駁」建議改「哈里森 1767 年出小冊子反駁」。`claims.md` 的 lg611（8 月 22 日）、lg706（自己印）兩列的依據也要照上面更正。open-sea 的新依據（RMG 航位推算誤差）要補進 `claims.md` 與 `video.json` 的 `sources`。
