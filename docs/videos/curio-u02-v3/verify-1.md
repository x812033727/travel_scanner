# curio-u02-v3 查核第一輪

- 範圍：`video.json` 全部 167 句旁白、10 張卡片、章名、`youtube.title`、`youtube.description`、`thumbnail.data`、與真實人物或旁白有關的畫面提示詞。日期 2026-10-31。
- 做法：獨立查核，沒有參與撰稿。來源當天用 curl 重開（User-Agent 只用 `Mokaair-editorial/1.0`），掃描頁轉成圖片用眼睛讀。`claims.md` 只當線索。信心欄寫高、中、低；單一來源會標明。
- 第一列的 `行` 寫對應的行 id 或場景 id。CHANGED 與 NOT FOUND 的改法在表後的〈備註〉，用同一個編號對。
- 三項最重要的新發現：(1) 能源部內華達辦公室的制式回信證實名字不在它的地圖上，**也寫了原因**，a084 的「查不到」不成立，片尾的「三十五年」也不能當成藏了三十五年；(2) 1995 年收地的公報原文是 **3,972.04 英畝**，不是五千，而且空軍 **1993 年就申請了**，早於訴訟，a112 的「結果」不成立；(3) 1958 年土地命令原文（這次開到了）**沒有任何編號**，a056 講強了。

## 逐項查核

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | `youtube.title`、`thumbnail.sub`：「1965 年的壘球新聞就印過它的名字」 | CHANGED | 刊頭 "An Information Bulletin for employees of the Atomic Energy Commission's Nevada Test Site"；名字確實印過，可是不是對外新聞 | Bulletin Board 影本（親眼看） | https://dreamlandresort.com/pete/no_secret_03.jpg | 高 |
| 2 | a001–a002、`open-58` 卡片：流傳的版本是連名字都藏了 58 年 | CHANGED | "Not all of these details have been secret for the last 58 years."；"For the first time, the CIA acknowledged"；沒有找到「連名字藏 58 年」這個說法本身 | Las Vegas Sun 2013；Reuters 經 CSMonitor | https://lasvegassun.com/news/2013/aug/15/government-acknowledges-area-51-declassified-spy-p/ | 中 |
| 3 | a003：有人為了這個名字告上法院 | CHANGED | 訴訟為的是焚燒廢料："alleged toxic waste burning"；名字是訴訟中的程序問題："without the officially recognized name ... the suit cannot proceed" | Las Vegas Sun 1998；Begley | https://www.sharonlbegley.com/it-dares-not-speak-its-name | 高 |
| 4 | a004–a005：1995 年拉斯維加斯法院，工人要政府講名字 | CONFIRMED | "A Las Vegas federal judge"；"which Turley filed a motion last week to get"；"disputing the name" | Las Vegas Sun 1996-10-14、1996-03-07；Begley | https://lasvegassun.com/news/1996/mar/07/judge-throws-out-groom-lake-suit/ | 高 |
| 5 | a006、`no-name` 卡片：政府律師回答法官「沒有名字」，標成工人律師引述 | CONFIRMED | "in 1995, the government's lead counsel, Col. Richard Sarver, told Judge Philip Pro: 'Your honor, there is no name.'"。逐字只有 Turley 一人；逐字稿已在 2000 年以塗黑版釋出但沒開到（"released ... with all classified information blacked out"）。政府拒講名字這件事有多個獨立來源 | Turley 2013；Las Vegas Sun 2000-02-25 | https://jonathanturley.org/2013/08/21/the-truth-is-out-there-the-real-cover-up-at-area-51/ | 中：逐字單方；要旨高 |
| 6 | a007：這些工人就在那裡上班 | CONFIRMED | "five current and former workers at the base"；"My (clients) worked at Area 51" | Las Vegas Sun 1998 | https://lasvegassun.com/news/1998/jan/08/toxic-data-at-area-51-ruled-confidential/ | 中：沒有政府承認的文字 |
| 7 | a008：三十年前名字印在標題上 | CONFIRMED | 1965→1995＝30；"AREA 51 WINS SLOW-PITCH TOURNAMENT" | Bulletin Board 影本 | https://dreamlandresort.com/pete/no_secret_03.jpg | 高 |
| 8 | a012–a015：1955-04-12 小飛機四人、看似鋪過的跑道、討論後降湖床 | CONFIRMED | "On 12 April 1955"；"After debating about landing on the old airstrip, LeVier set the plane down on the lakebed, and all four walked over"；"appeared to be paved" | CIA 史 2013 版 p.56（看圖），1998 版同頁也可讀 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf | 高 |
| 9 | a016–a018：壓實的土、荒十幾年、灰到腳踝、降在跑道上多半會翻 | CONFIRMED | "compacted earth that had turned into ankle-deep dust after more than a decade of disuse"；"would probably have nosed over ... killing or injuring all of the key figures" | CIA 史 p.56 | 同上 | 高 |
| 10 | a020–a021：下個月官方宣布蓋新設施、十八家媒體 | CONFIRMED | 新聞稿影本 LAV-55-16，May 18, 1955；分發表我數了是 18 家。稿內沒有寫 Groom 或 Area 51 | AEC 新聞稿影本（Merlin 網站，**claims 列為沒開到，其實有掃描**） | https://dreamlandresort.com/pete/no_secret_01.jpg | 高 |
| 11 | a023–a024：工程師取名天堂牧場；後來承認是騙工人 | CONFIRMED | "To make the new facility ... sound more attractive to his workers, Kelly Johnson called it the Paradise Ranch"；"a dirty trick to lure workers"（後句只有 Merlin） | CIA 史 p.57；Merlin | https://dreamlandresort.com/pete/no_secret.html | 高／單一來源（後句） |
| 12 | a025：CIA 史書說當時地圖編號就是它 | CONFIRMED | "known by its map designation as Area 51" | CIA 史；Las Vegas Sun 2013 照引；CIA 2015 | https://www.cia.gov/stories/story/area-51-and-the-accidental-test-flight/ | 高 |
| 13 | a026：航空史家說五〇年代官方文件都寫沃特敦 | CONFIRMED | "During the 1950s, the site appeared in all official documents as Watertown."；1955 年墜機也有佐證 "secret 'Watertown' airstrip"。CIA 2015 另說 "both the names Watertown and Area 51 were used as official names" | Merlin；Review-Journal 2015；CIA 2015 | https://dreamlandresort.com/pete/no_secret.html | 中：「都」是他的說法，旁白有標 |
| 14 | a028–a030：七月搬入、八月一日滑行時離地、沒打算飛 | CONFIRMED | "By July 1955 the base was ready"；"had no intentions whatsoever of flying"；"during a high-speed-taxi test" | CIA 史 p.57、69；CIA 2015 | https://www.cia.gov/stories/story/area-51-and-the-accidental-test-flight/ | 高 |
| 15 | a031–a032：十月開班機、週一進週五回、不到七週後 11-17 暴風雪撞山 | CONFIRMED | "began on 3 October 1955"；"Less than seven weeks after it started"；"during a blizzard"。10/3→11/17＝45 天 | CIA 史 p.72；Review-Journal 2015 | https://www.reviewjournal.com/?p=959585 | 高 |
| 16 | a033–a034、`fourteen` 卡片：差約 15 公尺、14 人、死最多的一次 | CONFIRMED | "just 50 feet below the ridgeline"；"clipped it 50 feet below the crest"；"greatest single loss of life in the entire U-2 program"。50 英尺＝15.2 公尺 | Las Vegas Sun 2001；Roadrunners；CIA 史 p.72 | https://lasvegassun.com/news/2001/mar/16/plane-crash-site-urged-as-monument/ | 高 |
| 17 | a036：對外說法是出差；家屬幾十年不清楚細節 | CONFIRMED | "The media was told the plane was on a business trip"；"found the victims were no ordinary businessmen"；"For decades, families ... never knew the details" | Las Vegas Sun 2001；Roadrunners；Review-Journal 2015 | https://www.reviewjournal.com/?p=959585 | 中：另有官方稱飛往 Indian Springs（Merlin） |
| 18 | 章名「十四個人撞上山，家屬聽到的是出差」 | NOT FOUND | 來源只寫媒體被告知 "The media was told"；家屬那邊只查到 "her family got a phone call that her brother had been killed in a plane crash"。沒有來源說家屬被告知出差 | Las Vegas Sun 2001；Review-Journal 2015 | https://lasvegassun.com/news/2001/mar/16/plane-crash-site-urged-as-monument/ | 高 |
| 19 | a037：工程師女兒那年八歲 | CONFIRMED | "She was 8 years old when her dad, Richard Hruda" | Review-Journal 2015 | https://www.reviewjournal.com/?p=959585 | 高 |
| 20 | a039：當地報紙兩天後就寫去超機密基地，只是官方不講 | CHANGED | "Another article, two days later"（是前一篇報導的兩天後，不一定是失事兩天後）；"Officials told reporters that the plane was destined for the airfield at Indian Springs"（官方不是不講，是講了別的地方） | Merlin；第二來源沒找到 | https://dreamlandresort.com/pete/no_secret.html | 中／單一來源 |
| 21 | a040、a133：四十幾年 | CONFIRMED | 1955→1998＝43 | 算術 | （無） | 高 |
| 22 | a042、`altitudes` 卡片：客機 1–2 萬、軍機 4 萬以下、它 6 萬以上 | CONFIRMED | "between 10,000 and 20,000 feet"；"below 40,000 feet"；"above 60,000 feet"。卡片標了 CIA 計畫史 | CIA 史 p.72（1998 版與 2013 版都看了） | https://www.cia.gov/resources/csi/static/CIA-and-U2-Program.pdf | 高 |
| 23 | a043：那時候沒有人相信人能飛到那麼高 | CHANGED | CIA 史 "no one believed manned flight was possible above 60,000 feet"；可是 1953 年 D-558-2 已飛到 83,235 英尺，1954 年 X-1A 飛到 90,440 英尺 | CIA 史 p.72；NASA | https://www.nasa.gov/aeronautics/d-558-ii-transonic-aircraft/ | 高 |
| 24 | a044–a047：傍晚往西的客機、機翼反光、一團火、他們沒有看錯 | CHANGED | "if a U-2 was airborne in the vicinity"；"fiery objects"。原文是 CIA 史書的解釋機制，旁白直述成發生過的事，a047 再判定「沒有看錯」，而 a052–a053 又質疑同一本書的根據 | CIA 史 p.72 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf | 高 |
| 25 | a048–a050：寫信、請華盛頓核對、不能告訴寫信的人、自然現象 | CONFIRMED | "wrote letters to the Air Force unit"；"check reported UFO sightings against U-2 flight logs"；"could not reveal to the letter writers"；"natural phenomena" | CIA 史 p.73（看圖） | 同上 | 高，CIA 單方 |
| 26 | a051、a134：飛碟通報一半以上；1998 版那句沒有黑條 | CONFIRMED | "more than one-half of all UFO reports during the late 1950s and most of the 1960s"；1998 版 p.73 該段完整，同頁下方另有整塊黑 | CIA 史 p.73 兩版都看了 | https://www.cia.gov/resources/csi/static/CIA-and-U2-Program.pdf | 高 |
| 27 | a053：腳註是行政主管提供給作者的資訊 | CONFIRMED | **2013 版 p.73 我親眼看了（用 PyMuPDF 解得開）**，與 1998 版相同："Information supplied by James Cunningham to Donald E. Welzenbach (U)."；"added an administrative officer, James A. Cunningham, Jr." | CIA 史 2013 版 p.73；同章 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf | 高 |
| 28 | a054–a055、`bluebook` 卡片：12,618 件、701 件、沒有證據指向外星飛行器 | CONFIRMED | "a total of 12, 618 sightings ... 701 remain 'Unidentified.'"；結論段含 "no evidence" | 美國國家檔案館 | https://www.archives.gov/research/military/air-force/ufos | 高 |
| 29 | a056：那時候這塊地早就有編號了：1958-06-20 | CHANGED | **命令原文開到了**：Public Land Order 1662，June 20, 1958，filed June 25，全文沒有編號，只寫 "for use of Atomic Energy Commission in connection with the Nevada Test Site"。編號是 Merlin 的說法，能源部說 "at some point" | Federal Register 1958-06-26 p.4700 | https://www.govinfo.gov/content/pkg/FR-1958-06-26/pdf/FR-1958-06-26.pdf | 高 |
| 30 | a057：三萬八千多英畝劃給原子能委員會 | CONFIRMED | "The area described contains approximately 38,400 acres." | 同上（一手） | 同上 | 高 |
| 31 | a058：能源部說之後某個時候開始叫 Area 51 | CONFIRMED | "was then referred to as 'Area 51' at some point during its usage by AEC" | 勞工部 Circular 08-06 | https://www.dol.gov/owcp/energy/regs/compliance/PolicyandProcedures/finalcircularhtml/EEOICPACircular08-06.htm | 高 |
| 32 | a060：起算點往後挪三年 | CHANGED | 能源部只說 1958 之後的某個時候；最早有影本的是 1960-01-15。所以是「至少三年」 | 勞工部通告；N.T.S. Bulletin | https://dreamlandresort.com/pete/no_secret_02.jpg | 高 |
| 33 | a061–a062：1960-01-15 頭版電話欄，號碼塗黑 | CONFIRMED | "AREA 51 TELEPHONE NUMBERS"；三個號碼是黑條。同頁另一個無關的電話也是黑條，影本也有 UNCLASSIFIED 字樣 | N.T.S. Bulletin 影本（親眼看） | https://dreamlandresort.com/pete/no_secret_02.jpg | 高 |
| 34 | a064–a066、`score` 卡片：1965-09-17、14 比 4、八號球、全明星兩人、外野手名字 | CONFIRMED | "14-4 victory over the Area 12 Mets"；"The championship game"；Left Field Al King Area 51；Short Field Lippy Lipscomb Area 51 | Bulletin Board 影本；Las Vegas Sun 2008 | https://lasvegassun.com/news/2008/jan/21/secrets-out-about-field-we-cant-talk-about/ | 高 |
| 35 | a067：1961 道路圖，10.3 英里 | CONFIRMED | "10.3 MILES TO AREA 51"；第二來源與掃描都沒找到 | Merlin | https://dreamlandresort.com/pete/no_secret.html | 中／單一來源 |
| 36 | a069：1967 年 CIA 文件，三架要部署到嘉手納 | CONFIRMED | "Three OXCART aircraft ... will be deployed from Area 51 to Kadena." | CIA BYE 2369-67 p.17（Commons 轉載） | https://commons.wikimedia.org/wiki/File:CIA_BYE2369-67_page17.gif | 高 |
| 37 | a070–a072：1971 空軍官員反對內部文章；六年 | CONFIRMED | "In May 1971 ... 'the article exposes the existence of Area 51'"；第二來源沒找到。1965→1971＝6 | Merlin | https://dreamlandresort.com/pete/no_secret.html | 中／單一來源 |
| 38 | a073–a074：太空人拍到；只有這裡被交代不准拍；原因說不清 | CONFIRMED | "inadvertently photographed"；"was the only location which had such an instruction"；"disobeyed ... unknown" | The Space Review 2023 | https://thespacereview.com/article/4518/1 | 高 |
| 39 | a075：軍方要壓、NASA 主張公開、國務院大致同意 | CONFIRMED | "DoD elements ... all believe it should be withheld ... NASA, and to a large degree State" | 同上 | 同上 | 高 |
| 40 | a076–a077、`three-questions` 卡片：局長的三個問題 | CONFIRMED | "1-USSR has it from own sats. 2-What really does it reveal? 3-If exposed don't we just say classified USAF work is done there?" | 同上 | 同上 | 高 |
| 41 | a079–a080：沒有文件寫怎麼決定；進檔案庫沒人注意；1959、1968 航照 | CONFIRMED | "no declassified documents indicating how this dilemma was resolved"；"went unnoticed for several more decades"；"1959 and 1968"；"higher-resolution" | 同上 | 同上 | 高 |
| 42 | a082、章名「一九七八年，它從地圖上不見了」、`description`「一九七八年它從地圖上消失」 | CHANGED | 只有能源部的試驗場地圖："from maps of the NTS produced by the Department of Energy"；同年土地管理局的地圖 "showing more detail than any previous map"，邊界還在 | Merlin | https://dreamlandresort.com/pete/no_secret.html | 高 |
| 43 | a083：到 1978 年 9 月能源部地圖上的邊界和編號不見了 | CONFIRMED | "By September 1978 ... the boundary of Area 51 and its number had been removed"。**第二來源：能源部自己的制式回信** "Area 51 no longer appears on maps of DOE's Nevada Test Site"。回信證實不在地圖上，**但沒有寫 1978**；年月仍只有 Merlin | Merlin；DOE Nevada Operations Office 回信（隨 2001-07-09 FOIA 回函） | http://www.theblackvault.com/documents/ufos/area51/area51.pdf | 事實高；年月中／單一來源 |
| 44 | a084：為什麼？我查不到文件說明 | CHANGED | "Because DOE is not now active there, Area 51 no longer appears on maps of DOE's Nevada Test Site (NTS)."；回信附在回函裡，寫明 "sent in response to all such requests" | DOE FOIA 回函與附件（影本親眼看） | http://www.theblackvault.com/documents/ufos/area51/area51.pdf | 高 |
| 45 | a085：隔年空軍接手、第三分遣隊、1984 路管制 | CONFIRMED | "Since the Air Force had taken control of the facility in 1979"；"Detachment 3"；"By March 1984"。Merlin 另一處寫 "in the 1970s"，Sun 2013 寫 1957 空軍進駐 U-2 訓練，是不同的事 | Merlin | https://dreamlandresort.com/pete/no_secret.html | 中／單一來源 |
| 46 | a086：名字真正開始被藏是從這裡 | CHANGED | 標了意見，可是與本片事實衝突：a070 的 1971 年反對信早七年；能源部給的是行政理由；Merlin 全文主張 "Area 51 was never secret" | Merlin；DOE 回信 | http://www.theblackvault.com/documents/ufos/area51/area51.pdf | 高 |
| 47 | a088–a090、`nine` 卡片：1989 年五月、遮臉化名、S-4、九艘、元素 115，都標他說 | CONFIRMED | "May 13, 1989"；"face was hidden and he used a pseudonym"；"S-4 south of Groom Lake"；"nine alien flying saucers"；115 另見 Skeptic。a090 引的 KLAS 第二篇 claims 沒給網址，我沒開到 | KLAS 回顧（Wayback）；NBC；Skeptic | https://web.archive.org/web/20210117151518/https://www.8newsnow.com/news/i-team-25-years-later-man-who-exposed-area-51/ | 高 |
| 48 | a092–a095：相信與懷疑兩邊、紀錄被改的說法、115 國際承認、沒有人證實 | CONFIRMED | "no record of him at either institution"；"altered or removed"；"has not been proved"；"later recognition by IUPAC does not validate" | Skeptic 2026 | https://www.skeptic.com/article/the-strange-case-of-bob-lazar/ | 高 |
| 49 | a098：1994 年五工人兩遺孀，聲稱 | CONFIRMED | "Five workers and the widows of two former employees ... since 1994" | Las Vegas Sun 2003 | https://lasvegassun.com/news/2003/apr/15/judge-keeps-lid-on-area-51-secrets/ | 高 |
| 50 | a099–a101：大桶、足球場大的溝、飛機燃料、魚鱗皮膚，都標聲稱 | CONFIRMED | "55-gallon drums"；"trenches the size of football fields"；"doused with jet fuel"；"fish-like scale and continually cracks and bleeds" | Las Vegas Sun 1996 | https://lasvegassun.com/news/1996/oct/14/ex-workers-judge-ignored-area-51-evidence/ | 高 |
| 51 | a103：不要賠償，要答案給醫生 | CONFIRMED | "The workers sought no damages"（獨立報導）；"never sued seeking damages"；Wood 法官轉述 Turley "not big money judgments" | Las Vegas Sun 1998、2003；Village Voice | https://lasvegassun.com/news/1998/jan/08/toxic-data-at-area-51-ruled-confidential/ | 高 |
| 52 | a104：連工作地點都不能告訴醫生，標律師說 | CONFIRMED | "barred from telling doctors where they worked" | Turley 2013 | https://jonathanturley.org/2013/08/21/the-truth-is-out-there-the-real-cover-up-at-area-51/ | 中：單方，有標 |
| 53 | a105：提告後四個月不承認存在 | CONFIRMED | "For four months after the suit was filed, the government denied the very existence of the facility"；Merlin 也這樣寫 | Begley；Merlin | https://www.sharonlbegley.com/it-dares-not-speak-its-name | 高 |
| 54 | a107：書狀說要求含糊、範圍太廣、負擔太重 | CONFIRMED | "vague, overbroad, and unreasonably burdensome" | Begley | 同上 | 高 |
| 55 | a109–a110：空軍部長說沒有正式運作名稱；開頭那句講的就是這個 | CONFIRMED | "has no actual operating name per se"；第二來源沒找到（查到的 Widnall 文字是講化學物質）。「講的就是這個」是撰稿的連結，兩句都指 operating location，合理。另注意 Sun 2000 把 1995 年那場聽證稱作 teleconference，「法庭上」未必字面成立 | Merlin；Sun 1998、2000 | https://dreamlandresort.com/pete/no_secret.html | 中／單一來源 |
| 56 | a111：律師提議載法官上山 | CONFIRMED | "I offered to drive the judge personally to the base and point at it from a mountaintop." | Turley 2013 | https://jonathanturley.org/2013/08/21/the-truth-is-out-there-the-real-cover-up-at-area-51/ | 中：單方，有標 |
| 57 | a112：結果 1995 年 4 月空軍收了五千英畝 | CHANGED | **Public Land Order 7131："withdraws 3,972.04 acres ... to provide a safety and security buffer"，effective April 7, 1995**。Salt Lake Tribune 1993-10-17 轉載："On Oct. 6, the Air Force filed a petition ... 3,972 acres"，早於 1994 年的訴訟。Turley 寫 "then acquired the mountaintop" 是他的順序，Merlin 的 5,000 是錯的或約數 | Federal Register 60 FR 18030（一手）；報導轉載 | https://www.federalregister.gov/documents/1995/04/10/95-8756/withdrawal-of-public-land-to-the-united-states-air-force-nevada | 數字高；1993 日期中（轉載） |
| 58 | a113：俄國衛星照片、信用卡，標律師 | CONFIRMED | "Russian satellite pictures"；"You just needed a credit card."；Begley 也提俄國照片 | Turley 2013；Begley | https://jonathanturley.org/2013/08/21/the-truth-is-out-there-the-real-cover-up-at-area-51/ | 中：單方，有標 |
| 59 | a114：9-29 總統簽，稱呼是空軍在格魯姆湖附近的作業地點 | CONFIRMED | "Presidential Determination No. 95-45 of September 29, 1995"；"operating location near Groom Lake, Nevada" | Federal Register 1995-10-10 | https://www.govinfo.gov/content/pkg/FR-1995-10-10/html/95-25244.htm | 高 |
| 60 | a115：公報上查得到九份，最後 2003 | CONFIRMED | 我重跑：1995、96、97、98、99、2000、01、02、03 共九件；同檢索另兩筆不相干 | Federal Register API | https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22Groom+Lake%22&per_page=60&order=oldest | 高 |
| 61 | a117–a118：電影；照製片說法軍方撤協助 | CONFIRMED | "according to the film's producer and co-writer Dean Devlin, the military withdrew its support"；只有轉述的轉述 | Mental Floss | https://www.mentalfloss.com/article/76231/16-earth-shattering-facts-about-independence-day | 中，有標 |
| 62 | a119–a122：外星公路、3,300 美元、朝天的牌子、50 輛、州長上電視 | CONFIRMED | "signs costing $3,300 ... including at least one pointing skyward"；"about 50 vehicles a day"；"Miller appeared on national television" | Las Vegas Sun 1996-03-08 | https://lasvegassun.com/news/1996/mar/08/area-51-highway-serious-business/ | 高 |
| 63 | a123–a125：1998-01、3-0、無權知道、甚至名字、馬賽克 | CONFIRMED | "The 3-0 ruling"；"or even the name of the base"；"'mosaic'"。判決全文 justia 403，沒開到。報導另寫政府 "denied it was Area 51"，法院未質疑，旁白沒用 | Las Vegas Sun 1998 | https://lasvegassun.com/news/1998/jan/08/toxic-data-at-area-51-ruled-confidential/ | 高 |
| 64 | a126：1998 年 CIA 出版 U-2 史書，272 頁 | CONFIRMED | PDF 272 頁；"published, in 1998, by the agency's Center for the Study of Intelligence" | CIA PDF；EBB 434 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/ | 高 |
| 65 | a127、`black-58` 卡片：p.56 黑條、p.57 上半、p.58 全黑 | CONFIRMED | 三頁我都轉圖親眼看，與旁白一致 | CIA 史 1998 版 | https://www.cia.gov/resources/csi/static/CIA-and-U2-Program.pdf | 高 |
| 66 | a129–a130：p.72 目的地與安全主管姓名黑條 | CONFIRMED | "MATS aircraft bound for ▇ crashed"；"CIA's ▇ four members of his staff"，親眼看 | 同上 | 同上 | 高 |
| 67 | a131–a132：1998 童軍團長上山、找家屬、多數第一次聽到 | CONFIRMED | "In 1998, Ririe hiked up the mountain"；"shared them with the families he tracked down"；"most of them heard for the first time" | Roadrunners；Review-Journal 2015 | https://m.roadrunnersinternationale.com/authors/pardew6.html | 高 |
| 68 | a137–a139：里切爾森、2002 全黑、2005 再申請 | CONFIRMED | "prolific Freedom of Information Act requester"；"all mentions of Area 51 had been redacted"；"requested the history again in 2005" | National Security Archive 2017；AP | https://www.mprnews.org/story/2013/08/16/news/cia-area-51-declassified-documents | 高 |
| 69 | a140–a142：2008 記者、衛星圖、發言人、上網查到 | CONFIRMED | "We can't talk about anything that goes on out there"；"A quick search of the Internet" | Las Vegas Sun 2008 | https://lasvegassun.com/news/2008/jan/21/secrets-out-about-field-we-cant-talk-about/ | 高 |
| 70 | a143–a144：2008-08-05 勞工部通告標題、職業病補償 | CONFIRMED | "SUBJECT: Expansion of Nevada Test Site to include Area 51" | 勞工部 | https://www.dol.gov/owcp/energy/regs/compliance/PolicyandProcedures/finalcircularhtml/EEOICPACircular08-06.htm | 高 |
| 71 | a145：比 CIA 早五年 | CHANGED | 2008→2013 算術對。可是 CIA 網站 2010 年前就公開了 a069 那一頁（Commons 2010-04-05 上傳，來源 foia.cia.gov）；NRO 2004 年也在回函寫 "Aerial Observation, Area 51"。要比的是那本史書 | Commons 檔案歷史；NRO 回函 | http://www.theblackvault.com/documents/nro/Area51AerialObservation.pdf | 高 |
| 72 | a146–a147：6-25 核准、8-15 上網、地圖爆紅、流量紀錄 | CONFIRMED | "approved for release 25 June 2013"；"went viral, bringing a record spike in traffic" | EBB 434；National Security Archive 2017 | https://nsarchive.gwu.edu/news/cybervault/2017-11-14/memoriam-jeffrey-t-richelson-1949-2017 | 高 |
| 73 | a148–a149：第 58 頁地圖、頂端 Area 51、小框裡的長方形 | CONFIRMED | 親眼看：頁首框 "Area 51"，右上小框內長方形緊貼 "AEC Nevada Test Site"，頁角手寫 58 | EBB 434 圖檔 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/images/Area-51-map.jpg | 高 |
| 74 | a150：p.72 回來了；William Marr | CONFIRMED | 2013 版 p.72 "bound for Area 51"；"CIA's William H. Marr" | CIA 史 2013 版 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf | 高 |
| 75 | a151：里切爾森說有意識的決定 | CONFIRMED | "clearly a conscious decision to acknowledge the name, the location rather than play pretend about the secrecy"。同一人同篇也說之前的官方提及 "rare and 'probably inadvertent'" | Review-Journal 2013 | https://develop.reviewjournal.com/?p=472448 | 高 |
| 76 | a153：CIA 發言人說找不到外星人 | CONFIRMED | "What readers won't find are any references to aliens" | Reuters 經 CSMonitor | https://www.csmonitor.com/USA/Latest-News-Wires/2013/0817/Area-51-is-real-say-CIA-documents | 高 |
| 77 | a154：只寫到 1974 | CONFIRMED | 書名 1954-1974 | EBB 434 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/ | 高 |
| 78 | a155：2022 CIA 回讀者 | CONFIRMED | "I'm sad to say there are no aliens in the basements"；July 1, 2022 | CIA Ask Molly | https://www.cia.gov/stories/story/ask-molly-what-really-went-on-at-area-51/ | 高 |
| 79 | a157：2003 上訴法官另外寫 | CONFIRMED | "to strongly consider releasing any information possible which might aid plaintiffs"；原句後面還有但書 | Las Vegas Sun 2003 | https://lasvegassun.com/news/2003/apr/15/judge-keeps-lid-on-area-51-secrets/ | 高 |
| 80 | a159：律師 2013 寫政府沒解密 | CONFIRMED | "the government refused to declassify information about what it had burned in the trenches" | Turley 2013 | https://jonathanturley.org/2013/08/21/the-truth-is-out-there-the-real-cover-up-at-area-51/ | 中：單方，有標 |
| 81 | a160–a161：2015 年五月紀念碑、家屬、螺旋槳、刻意抹掉 | CONFIRMED | "A throng of surviving family members"；"a memorial that features a propeller"；"purposely erased" | Review-Journal 2015 | https://www.reviewjournal.com/?p=959585 | 高 |
| 82 | a162：現在官方叫內華達試驗訓練場；不會告訴你 | CONFIRMED | "commonly preferred official name for the facility today"；"remain classified and cannot be discussed" | CIA 2015；Sun 2008 | https://www.cia.gov/stories/story/area-51-and-the-accidental-test-flight/ | 高 |
| 83 | a165：從地圖上拿掉到 CIA 印回去，三十五年，名字藏的是這段 | CHANGED | 1978→2013＝35 算術對，也標了「照我的算法」。可是那段時間官方寫過這個名字：能源部回信寫了 "once known as 'Area 51'"（文內 "more than 35 years ago" 自 1958 起算，所以寫於 1993 年以後，隨 2001 回函）；NRO 2004；勞工部 2008；CIA 網站 2010 前；里切爾森本人 "rare and 'probably inadvertent'"；AP "acknowledged in passing"；片子自己 a143 就講 2008 | DOE 回信；NRO；勞工部；Review-Journal 2013；AP | http://www.theblackvault.com/documents/ufos/area51/area51.pdf | 高 |
| 84 | `description` 其他事實句（1965、1998 第 58 頁、法院因國家機密駁回沒有認定事實、流傳的版本標明） | CONFIRMED | 見上；"on grounds that the issue was a national secret" | Las Vegas Sun 1996 | https://lasvegassun.com/news/1996/oct/14/ex-workers-judge-ignored-area-51-evidence/ | 高 |
| 85 | `scout`、`scout-2` 提示詞：童軍團長本人 | CHANGED | Steve Ririe，2015 年仍在世，沒有查到過世。提示詞畫他跪在螺旋槳旁、站在家屬門口，對著旁白 a131–a132 | Review-Journal 2015；說明欄承諾「不入畫」 | https://www.reviewjournal.com/?p=959585 | 高 |
| 86 | `researcher`、`conscious` 提示詞：里切爾森本人 | CHANGED | 他 2017 年過世，未滿七十年。a137「這個人叫里切爾森」時畫面是面對觀眾的讀者，等於畫成本人 | National Security Archive 2017 | https://nsarchive.gwu.edu/news/cybervault/2017-11-14/memoriam-jeffrey-t-richelson-1949-2017 | 高 |
| 87 | `softball-2008`、`cant-talk`、`found` 提示詞：記者本人 | CHANGED | 文章作者 Brian Hilderbrand，生死未查到，應視為在世。提示詞連畫三張他的動作 | Las Vegas Sun 2008 | https://lasvegassun.com/news/2008/jan/21/secrets-out-about-field-we-cant-talk-about/ | 中 |
| 88 | `footnote-2` 提示詞：退休的 program manager 在廚房講話 | CHANGED | 職稱是 administrative officer，與旁白「行政主管」不符；這場景沒有來源（1983 年訪談），又畫真實人物。生卒未查到 | CIA 史第 2 章 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf | 中 |
| 89 | 其他真實人物：Lazar（`tv` 空椅）、LeVier（`taxi`、`no-intention` 無飛行員）、Kelly Johnson（`ranch-sign` 畫工）、Colby（`you-director` 只有手）、總統（`order` 只有手）、Turley（`credit-card` 法學生代替）、Widnall、Wood 法官（只有手）、Marr（`marr` 1955 過世，滿 71 年，規則允許；37 歲有來源） | CONFIRMED | 都沒有畫成本人；"William H. Marr, 37" | 提示詞逐一對過；Review-Journal 2015 | https://www.reviewjournal.com/?p=959585 | 高 |
| 90 | 外星與 UFO 說法是否標成流傳：a001、a087–a096、`nine` 卡片、a152–a155、a167 | CONFIRMED | 都帶流傳、他說、相信的人說或官方引述；沒有當事實講 | 逐句對過 | （無） | 高 |
| 91 | 人物內心與對話：a019「互看一眼的表情」、a068「大概常常聽到」、a096「很可能」 | OUT OF SCOPE | 都帶「你可以想像」「大概」「很可能」，標得出是想像，沒有假裝紀錄 | 逐句對過 | （無） | 高 |

## 備註：CHANGED 與 NOT FOUND 的行 id 與建議改法

1. **`youtube.title`、`thumbnail.sub`。** 標題是問句，沒有強過事實，也不靠片尾的三十五年，**可以保留方向**。可是「新聞」會讓人以為是對外報紙。建議：「51 區藏了 58 年？1965 年的員工通訊就登過它的壘球冠軍」；縮圖 sub 改「1965 卻上員工通訊」。
2. **a002、`open-58`。** 旁白改「政府藏了五十八年，二〇一三年才第一次承認。」卡片 kicker 從「流傳的數字」改「報導算出來的數字」。
3. **a003。** 改「可是真的有人在法院裡，為了這個名字跟政府吵。」
18. **章名。** 改「十四個人撞上山，對外說的是出差」。
20. **a039。** 改「官方跟記者說飛機要去印第安泉，當地報紙沒幾天就寫：它要去超機密基地。」
23. **a043。** 改「CIA 的史書還說，那時候沒有人想到，人能飛到那麼高。」只能歸給史書；如果嫌弱就刪，這句直述是錯的。
24. **a045、a047。** a045 開頭加「照 CIA 史書的解釋，」；a047 改「如果史書說得對，他們沒有看錯，天上真的有東西。」這樣和 a052 的質疑才不矛盾。
29. **a056。** 改「那時候，這塊地也正式劃出來了：一九五八年六月二十日，」不要講「早就有編號」。a058 接得上。
32. **a060。** 改「起算點至少要往後挪三年。」
42. **a082、章名、`description`。** a082 改「可是四年後，它從能源部的地圖上不見了。」章名改「一九七八年，能源部的地圖上沒有它了」；說明欄改「一九七八年它從能源部的地圖上消失」。
44. **a084。** 不能再說查不到。改「為什麼？能源部後來的制式回信只有一句：能源部已經不在那裡活動了。」要新增 claims 來源列（DOE 回信）。回信沒有寫 1978，所以 a083 的年月仍然標史家。
46. **a086。** 改「我的看法是，這個名字變得很難從官方嘴裡聽到，是從這裡，不是一九五五年。」不要用「真正開始被藏」。`map-erased` 的橡皮擦畫面帶有刻意抹除的暗示，配上能源部的理由時可以考慮換。
57. **a112。** 改「律師說，政府接著把那座山也收了。不過空軍一九九三年就申請了，一九九五年四月公報上是三千九百七十二英畝，寫的用途是安全緩衝。」拿掉「結果」與「五千」。NOTES 寫「Turley 也提到」，他只提到收山，沒有數字。這一條也證明 Merlin 的數字不能單獨依賴。
71. **a145。** 改「還比 CIA 那本史書早五年。」
83. **a165。** 算術保留，「藏了三十五年」不能保留。建議：「照我的算法，五十八年算不過去。從能源部的地圖拿掉，到 CIA 決定承認，是三十五年；就連這三十五年，它也沒藏好。」能源部回信的日期只知道不晚於 2001，所以不要講具體年。如果要照 NOTES 的備案改回「三件事沒有答案」也可以，但不必，1978 這一條沒有被推翻。
85–88. **提示詞。** `scout`：只畫戴手套的手和雪裡的螺旋槳。`scout-2`：只畫門口遞資料夾的手，或收件的家屬。`researcher`、`conscious`：只畫桌上的書和黑條，沒有人。`softball-2008`、`cant-talk`、`found`：只畫螢幕、話機與手。`footnote-2`：畫腳註與放大鏡，不畫人。這幾條是說明欄「在世或過世未滿七十年的人物不入畫」這句承諾的落差。

## 撰稿者標的疑點

- **a006**：沒有找到第二個逐字來源。旁白標「工人律師後來引述」、卡片標「工人律師事後的引述」都準確，可以用。逐字稿有塗黑版（Sun 2000），但沒找到線上全文。
- **a083、a165**：見 #43、#44、#83。事實有第二來源，年月沒有，原因有官方說法，「藏」的講法要改。
- **a053**：2013 版我看到了，和 1998 版相同。`claims.md` 說本機解不開，用 PyMuPDF 可以。舊 claims 講 OSA History 確實是前一條（p.72 注）。
- **Merlin 六條的第二來源**：1955 新聞稿有掃描（#10）；1978 有能源部回信佐證事實（#43）；5,000 英畝被公報推翻（#57）；1961 路圖、1971 信、Widnall 沒找到第二來源（#35、#37、#55）；a039 的報紙也沒有（#20）；PLO 1662 原文開到了（#29、#30）。

## 開不到

- 1995 年聽證逐字稿（塗黑版）：沒找到線上檔。
- Kasza v. Browner、Kasza v. Whitman、Frost v. Perry 判決全文：law.justia.com 回 403。
- a090 依據的 KLAS 第二篇：`claims.md` 沒給網址。元素 115 另見 Skeptic，但 Skeptic 沒有說是在 1989 年那場訪談講的。
- 1993 年空軍申請的公報原文：API 用案號 NV-57922 只回 1995 年那份；1993 年日期來自 Salt Lake Tribune 的網路轉載（https://sacred-texts.com/ufo/hillgrab.htm）。
- Steve Ririe、Brian Hilderbrand、James Cunningham 的生卒：沒有查到。
- CIA Studies 1997 的 Haines 文章舊網址 404，這次沒有用。
- Black Vault 是私人 FOIA 檔案站，它對這些信的評論不當事實；我讀的是它放出的政府回函影本。
