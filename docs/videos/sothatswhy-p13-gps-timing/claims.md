# 主張與來源（sothatswhy-p13-gps-timing）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說（附行號，第一版 2026-11-11）、來源原文與注意事項，並標出它是
**官方規格／官方說明**、**教材**、**研究回顧**、**撰稿推論**，還是**示意**。另外每條標明它講的是**理想示意**（畫圓圈、交點、哨子遊戲）
還是**接收機實際做法**（把位置與鐘差一起估算、超過四顆用最小平方）。撰稿只能用「可用說法」裡的數字與說法；等另一個代理逐行查核（`verify-1.md`）。

2026-11-11 撰稿時當天重讀每一個來源（引文是原句）：
- GPS.gov 現行頁（node/70、faq、space-segment、augmentation-systems）、archive.gps.gov 典藏頁、FAA、ESA Navipedia、NWS、NIST、ION 摘要頁：curl GET 200，HTML 轉純文字。
- SPS 性能標準 2020 年第五版：curl GET 200（2,166,466 bytes），`pdftotext -layout` 讀。
- Blay et al. 2021：navi.ion.org 期刊 HTML 全文（CC BY），curl GET 200（226,281 bytes）。
- Ashby 2003：Europe PMC `fullTextXML`（PMC5253894），curl GET 200（289,549 bytes）。PMC 網站本身要過 reCAPTCHA，沒有用。
- **讀不到、沒有用的**：IS-GPS-200N（navcen.uscg.gov 的 PDF，curl 回 403、118 bytes），舊查核包 A38 用它支持「相對論頻率偏移」，這次只用 Ashby 原 review 的同一個數字；
  ION GNSS+ 2015 論文全文要付費，只讀到摘要（摘要已寫出 4.9 公尺的來歷與「誤差跟大樓高度相關」）。
- 舊查核包 `so-thats-why/season2/A38.md`（2026-10-01）與素材審視 `material-20261111-round3`（T53-012～019）只當線索；這裡每一條都重開來源。方括號數字對應文末〈來源〉。

**四捨五入與換算**（片中都說「大約」）：光速 299,792,458 m/s → 「一秒大約三十萬公里」；百萬分之一秒 × 光速 = 299.8 m → 「三百公尺」；
雷聲 5 秒一英里（1,609 m）→ 每秒約 322 m、每公里約 3.1 秒 → 「三秒一公里」「三百多公尺」；20,200 km → 「兩萬公里」；
0.643 m → 「還不到六十五公分」；4.9 m → 「大約五公尺」；−4.4647 × 10⁻¹⁰ × 86,400 秒 = 38.58 微秒 → 「三十八微秒」；38.58 微秒 × 光速 = 11.56 km → 「十一公里多」；
「九成九以上」是 Navipedia「more than 99.9%」的保守說法。

**本集不做的事**：不講選擇性可用性的歷史細節（只用 GPS.gov 一句「2000 年停了」）；不講相對論的歷史與公式，只講要修的那一點（約 50 秒）；
不給手機首次定位的秒數（廠商數字不一，Navipedia [13] 也這麼說）；不念 URE、DOP、SUPL、TTFF 這些縮寫；不放 A58。

## C01 衛星不知道你在哪，只往下廣播；手機只聽【官方說明】【接收機實際做法】

- **可用說法**：p016–p022（「剛好相反，衛星根本不知道你在哪。美國政府的 GPS 網站說，衛星就像燈塔，只負責一直往下廣播。手機只聽、不說話，它要自己從聽到的東西，算出你在哪。」）
- **來源**：[3]、[7]
- **原文**：GPS.gov FAQ [3]：「the GPS satellites themselves do not track anything on the ground. They are simply beacons, like lighthouses, broadcasting one-way reference signals.」
  FAA [7]：「The receiver uses the time difference between the time of signal reception and the broadcast time to compute the distance」。
- **注意**：「手機只聽、不說話」指的是 GPS 這部分；手機的行動網路當然會發訊號（C16 輔助 GPS 才講網路）。

## C02 雷聲大約五秒走一英里，約三秒一公里；數到六秒約兩公里【官方說明＋換算】【比喻的入口】

- **可用說法**：p025–p029
- **來源**：[16]
- **原文**：NWS [16]：「it takes the sound of thunder about 5 seconds to travel a mile … count the number of seconds between the flash of lightning and the sound of thunder, and then divide by 5, you'll get the distance in miles」。
- **注意**：公里是換算（5 秒 ÷ 1.609 km ≈ 3.1 秒／公里），**四捨五入**。只借來說「聽聲音晚多久＝多遠」；NWS 原頁還說聽得到雷就在雷擊範圍內，片中沒有教避雷。

## C03 哨子遊戲【示意，撰稿自己的比喻】【理想示意】

- **可用說法**：p030–p032、p057（「哨子報的時間」）、p077–p084、p129–p130、p138、p143–p145、p154、p169
- **來源**：比喻本身不是主張；對應 [7] 的「時間差算距離」。
- **限度**：真的 GPS 訊號是無線電，跑得跟光一樣快（C05）；高低兩支哨子（p138、p143）只借來想像「兩個頻率被拖慢的程度不同」，空氣裡的聲音並不會這樣（C12）。
  公園是平面，三個朋友就夠算「東西、南北＋錶差」；所以第四顆衛星那段明說「換回衛星：東西、南北、高低，再加上錶差多少」（p085–p086），不說四個朋友。

## C04 衛星帶原子鐘，訊號裡寫著發射時刻；大約兩萬公里高；訊號通常走 60–90 毫秒【官方說明＋研究文獻】

- **可用說法**：p033–p038。p038「一毫秒是千分之一秒」是「毫秒」第一次出現時的說明。p033「原子鐘，就是非常非常準的鐘」是給八歲小孩的定義，對應 FAA「atomic clocks that provide extremely accurate time」。
- **來源**：[7]、[4]、[14]
- **原文**：FAA [7]：「GPS satellites carry atomic clocks that provide extremely accurate time. The time information is placed in the codes broadcast by the satellite so that a receiver can continuously determine the time the signal was broadcast.」
  GPS.gov Space Segment [4]：「at an altitude of approximately 20,200 km (12,550 miles)」。
  Blay et al. [14] §2.3：「the travel time from satellite to receiver is typically 60 to 90 milliseconds」。
- **注意**：20,200 km ÷ 光速 ≈ 67 ms（正上方），斜向的衛星更遠，與 60–90 ms 一致。「兩萬公里」**四捨五入**。

## C05 訊號跟光一樣快，一秒約三十萬公里；差百萬分之一秒，距離差三百公尺【物理常數＋換算】

- **可用說法**：p009–p011（開場只問「時間只差百萬分之一秒，你猜，距離會差多少？」，小問錯猜「差一兩公尺吧？」）、p040–p042（第一次說出三百公尺，就在算出來的地方：「所以剛剛那百萬分之一秒，光就跑了大約三百公尺，不是一兩公尺。」）
- **來源**：[17]；[7]（距離由時間差算出）
- **原文**：NIST [17]：speed of light in vacuum「299 792 458 m s⁻¹」（exact）。
- **注意**：299,792,458 × 10⁻⁶ = 299.8 m → 「三百公尺」**四捨五入**。大氣會讓訊號稍慢（C11），所以 FAA 說接收機要扣電離層與對流層延遲；片中「跟光一樣快」是在真空裡的說法。
  第三輪（盲評 no_spoiler）把開場的結果拿掉，只留問題。p042 說的是「光跑了」三百公尺＝距離（偽距）誤差，不說「位置」：位置最後偏多少還要乘上幾何的放大倍數（C09）。片名「位置怎麼差那麼遠」是定性的說法（第二輪刪掉了 p045 的「這就是今天的題目」）。

## C06 只聽一顆只知道距離，可能在一整圈（太空裡是一整顆球面）上；兩三顆疊起來縮小範圍；畫圓圈只是示意【理想示意】

- **可用說法**：p060–p068（p068「先說清楚，畫圓圈只是幫你想像的示意。」）
- **來源**：[7]、[9]
- **原文**：FAA [7]：「With information about the ranges to three satellites and the location of the satellite when the signal was sent, the receiver can compute its own three-dimensional position.」
  Navipedia [9]：「The positioning principle is based on solving a geometric problem from the measured ranges to the satellites, with known coordinates.」
- **注意**：球面交會是教學上的**理想示意**，不是接收機的演算法（見 C08）。

## C07 三顆要靠一顆跟 GPS 同步的原子鐘；手機沒有；多量第四顆就不用；四個未知數：東西、南北、高低、鐘差【官方說明＋教材】【接收機實際做法】

- **可用說法**：p069–p088
- **來源**：[7]、[9]
- **原文**：FAA [7]：「An atomic clock synchronized to GPS is required in order to compute ranges from these three signals. However, by taking a measurement from a fourth satellite, the receiver avoids the need for an atomic clock. Thus, the receiver uses four satellites to compute latitude, longitude, altitude, and time.」
  Navipedia [9]：「The right side contains the four unknown parameters: The receiver coordinates (x,y,z) and the receiver clock offset δt.」
- **注意**：「手機裡沒有那麼準的鐘」（p076）是由 FAA「avoids the need for an atomic clock」推得：一般接收機沒有原子鐘，**撰稿推論**，沒有給手機鐘的誤差數字。
  p077–p079 的「哨子是聲音，錶慢一秒；聲音一秒跑三百多公尺，每個朋友都像近了這麼多」是哨子遊戲裡的算術（聲音每秒約 322 m，C02），不是 GPS 數字。

## C08 真的手機不是在畫圓圈，是把四個答案一起算；衛星超過四顆就找一個跟大家最合得來的答案【教材】【接收機實際做法】

- **可用說法**：p089–p091（p089 用「還記得剛剛那些圓圈嗎？」回呼 p068，不再重講示意）
- **來源**：[9]
- **原文**：Navipedia [9]：方程「defines a non linear system, which a usual resolution technique consists of linearising the geometric range … in the neighbourhood of a point … corresponding to an approximate receiver position」；
  「In general, an over-dimensioned system is obtained (for n > 4), which can be solved using the Least Squares adjustment.」
- **注意**：「最合得來的答案」是最小平方的口語說法，**簡化**；不教矩陣、不講線性化。Navipedia 是 ESA 主辦、大學研究者撰寫的教材級維基，不是同儕審查期刊。

## C09 基本排法 24 個位置，幾乎任何地方看得到至少四顆；位置誤差約＝量距離的誤差×放大倍數；倍數看相對位置；太差算不出；五顆以上不比四顆差【官方規格】

- **可用說法**：p092–p102
- **來源**：[4]、[6]
- **原文**：GPS.gov Space Segment [4]：「This 24-slot arrangement ensures users can view at least four satellites from virtually any point on the planet.」
  SPS PS [6] B.2.1：「Accuracy = UERE x DOP (B-1) … a simple approximation」；Glossary：「Dilution of Precision (DOP). The magnifying effect on GPS position error induced by mapping URE into a position solution … through the relative satellite-to-receiver geometry.」
  A.8.2：「Without 'good geometry', it can sometimes be impossible for users to even determine a PVT solution.」
  B.2.4.3.4：「Using five or more SISs for the PVT solution or time transfer solution always results in DOP values that are at least as good as the 4-SIS DOP values.」
- **注意**：照素材審視的要求，**刪掉**來源沒有的「衛星擠在一角放大得多、散開放大得少」機制句；片中只說「看衛星和你的相對位置好不好」。公式是**近似**（標準自己說的）。
  「二十四個位置」是基本排法的 slot 數，不是衛星總數（衛星數會變，片中不用）。PDOP ≤ 6 的 98% 承諾沒有放進片裡（觀眾聽不出意義）。

## C10 大樓擋住一部分衛星，能用的變少，放大倍數可能變大【撰稿推論，連接兩個官方說法】

- **可用說法**：p103–p106
- **來源**：[1]、[6]
- **原文**：GPS.gov [1]：常見原因「Satellite signal blockage due to buildings, bridges, trees, etc.」；SPS PS [6] B.2.4.3.4（五顆以上不比四顆差）。
- **注意**：「被擋 → 能用的少 → 倍數可能變大」是由這兩句推得，**撰稿推論**，所以說「可能」。沒有說衛星會擠到哪一邊。

## C11 訊號本身的誤差：承諾 95% 在 2 公尺內；2021-04-20 實際不到 65 公分；訊號誤差不等於使用者精度【官方說明】

- **可用說法**：p107–p112、p118–p121。p121「手上的誤差，還要加上路上的事：擋住、反彈，跟大氣」只列這一章接著講的三件事（擋住在 C10、反彈在 C13、大氣在 C14），衛星幾何已在第二章講過
- **來源**：[1]
- **原文**：GPS.gov [1]：「the government commits to broadcasting the GPS signal in space with a daily global average user range error (URE) of ≤2.0 m (6.6 ft.), with 95% probability … On April 20, 2021, the global average URE across all satellites was ≤0.643 m (2.1 ft.), 95% of the time.」
  「To be clear, URE is not user accuracy. User accuracy depends on a combination of satellite geometry, URE, and local factors such as signal blockage, atmospheric conditions, and receiver design features/quality.」
- **注意**：「每日全球平均」與「所有健康衛星」的限定片中省略，**簡化**；2021 年的數字是頁面上的舊日期，片中照念日期。原文沒有「乘上」，乘法是 C09 SPS 的近似式，兩段分開講。

## C12 手機開闊天空平均約 5 公尺；城市裡誤差跟大樓高度很相關【研究摘要，經 GPS.gov 引用】

- **可用說法**：p122–p124
- **來源**：[8]、[1]
- **原文**：ION 摘要 [8]（van Diggelen & Enge, ION GNSS+ 2015）：MOOC「created by the authors for Stanford University」；「In this lab, with over one thousand participants in one hundred countries, the measured mean accuracy, remarkably, came to 4.9 meters. Even more interesting, the accuracy in urban areas showed a remarkable correlation with building height.」
  GPS.gov [1]：「GPS-enabled smartphones are typically accurate to within a 4.9 m (16 ft.) radius under open sky … However, their accuracy worsens near buildings, bridges, and trees.」
- **注意**：素材審視時 4.9 m 的 ION 原文還沒讀；這次讀到 ION 的**摘要**（全文付費，沒讀）。4.9 → 「大約五公尺」**四捨五入**。2014 年課程、當年的手機，片中說「一門線上課」，沒說是現在的手機。
  沒有說藍點會偏多少公尺：小問的「跳到對街」是她自己看到的事，片中沒有用數字支持它。

## C13 多路徑：訊號撞到牆反彈才進手機；主要是天線太靠近反射物；低仰角的衛星影響最大【官方說明＋教材】

- **可用說法**：p125–p133。p131 把「教材」說清楚是誰的：「歐洲太空總署的導航教材說」（ESA Navipedia，ESA 主辦、大學研究者撰寫）。
- **來源**：[1]、[10]
- **原文**：GPS.gov [1]：「Signals reflected off buildings or walls ("multipath")」列為常見原因。
  Navipedia [10]：「The interference by multipath is generated when a signal arrives, by different ways, at the antenna … Its principal cause is the antenna closeness to the reflecting structures, and it is important when the signal comes from the satellite with low elevation.」
- **注意**：Navipedia 說碼量測的多路徑「Typically, it is less than 2 or 3 meters」、超過 15 公尺很難觀察；片中**沒有**念這兩個數字，也沒有說多路徑單獨就會把人放到對街（收尾 p183–p184 小問只說「訊號撞牆晚到一點點，手機就把我算到對街了」，是她自己的經驗；舊版收尾把遮擋、反彈與時間合在一起說）。
  「繞了遠路才到 → 以為比較遠」對應 [10] 的「arrives, by different ways」。

## C14 電離層延遲；單頻只能用模型、效應可達幾十公尺；廣播模型約修一半；延遲與頻率有關，雙頻可去掉 99.9% 以上【教材】

- **可用說法**：p134–p145。p138「衛星用不同的頻率送訊號，就像哨子有高音和低音」是「頻率」第一次出現時的說明：GPS.gov [1]「two GPS radio frequencies: L1 and L2」「a third civil signal at the L5 frequency」；高音低音是**比喻**。片中不再說「接收機」，改說「只聽一個頻率的話」（p139）
- **來源**：[11]、[12]
- **原文**：Navipedia [11]：「As the ionosphere is a dispersive media, the GNSS signals refraction depends on its frequencies (as the squared inverse). This dependence on the signal frequency allows us to remove its effect up to more than 99.9% using two frequency measurements … But, single frequency receivers have to apply an ionospheric prediction model to remove (as much as possible) this effect, that can reach up to several teens of meters」。
  Navipedia [12]：「GPS satellites broadcast the parameters of the Klobuchar ionospheric model for single frequency users … estimated to reduce about the 50% RMS ionospheric range error worldwide.」
- **注意**：照素材審視：「可達數十公尺」是**效應本身**，不是修正後的殘差（p139–p140 這樣說）；p141 的「估計」照查核 F 系列附註。「全世界平均大約修掉一半」＝50% RMS 的估計，**簡化**。高低兩支哨子是**示意**（C03）。
  片中**沒有**說「多數手機只收一個頻率」：那句只在典藏頁，而且現在已有雙頻手機。

## C15 政府沒有故意讓民用的變差，2000 年停了；訊號本身變差的話會到處都偏，不會專挑大樓中間【官方說明（現行頁）＋撰稿推論】

- **可用說法**：p113–p117（第二輪移到第三章「衛星送得很準」之後，當作小問的錯猜「會不會給我們的，故意弄不準？」）
- **來源**：[1]
- **原文**：GPS.gov [1]：「Doesn't the Government Degrade Civilian GPS Accuracy? No. During the 1990s, GPS employed a feature called Selective Availability that intentionally degraded civilian accuracy on a global basis. In May 2000 … the U.S. government ended its use of Selective Availability」。
- **注意**：p115 照查核 F02 的改法「美國政府的 GPS 網站說：沒有故意把民用的弄差。」（不回答「軍用是不是比較準」）。
  p117「而且訊號本身變差，到處都會偏，不會專挑大樓中間」是**撰稿推論**：GPS.gov 說選擇性可用性是「on a global basis」降低民用精度，而藍點只在大樓中間跳，所以這不是她看到的原因。
  第二輪**刪掉**了增強系統兩句（p129–p130 舊版）：跟藍點為什麼跳無關。來源 [5] 仍列在文末，但片中已不用。
  素材審視提到的「軍民 URE 相同、多數民用單頻、軍用雙頻」**只在** archive.gps.gov 典藏頁 [2]（頁首寫 2025 年 2 月後沒有更新），現行 node/70 已刪；片中不用。

## C16 衛星的鐘因相對論要修：重力弱→走快，速度快→走慢，合起來還是快；每天約 38 微秒；光在這段時間跑 11 公里多；有些鐘發射前在地面調慢，有些入軌後量了把修正寫進廣播【研究回顧＋換算】

- **可用說法**：p043–p059。p054「一微秒，就是百萬分之一秒」是「微秒」第一次出現時的說明（10⁻⁶ 秒，與開場 p010 的「百萬分之一秒」接上）（約 55 秒，企劃上限約 90 秒）。第二輪移到第一章「三百公尺」之後，當作「衛星報的時間能不能信」：小問「差一點點都不行！那衛星的錶，真的那麼準嗎？」→ 修正 → 「時間能信了，那聽一顆衛星…」
- **來源**：[15]
- **原文**：Ashby [15]：「+2.5046 × 10⁻¹⁰ − 6.9693 × 10⁻¹⁰ = −4.4647 × 10⁻¹⁰. The negative sign in this result means that the standard clock in orbit is beating too fast, primarily because its frequency is gravitationally blueshifted.」
  「for a GPS satellite clock, the gravitational blueshift is greater」（低軌道則是速度的時間膨脹較大）。
  「This adjustment is accomplished on the ground before the clock is placed in orbit.」
  「It has become common practice not to apply such offsets to Rubidium clocks … Instead, after such clocks are placed in orbit their frequencies are measured and the actual frequency corrections needed are incorporated in the clock correction polynomial」。
- **注意**：「一天約 38 微秒」是 4.4647 × 10⁻¹⁰ × 86,400 秒 = 38.58 微秒的**換算**（原文沒寫這個數，可重算）；「十一公里多」是 38.58 微秒 × 光速 = 11.56 km 的換算。
  **不說**「不修的話每天定位會飄 11 公里」（舊查核包 A38 明令不報；接收機的鐘差未知數會吸收共同的偏差，實際影響不是這麼簡單）。片中只說「光在這段時間可以跑十一公里多」與「不修的話，哨子報的時間，一天就錯這麼多」（p057）：錯的是衛星報的**時間**（換成距離十一公里多），不是定位結果。
  「地球拉得比較沒那麼用力」是重力位較高的口語說法，**簡化**。Ashby 是 2003 年的 review，不宣稱是現行規格。

## C17 位置還需要衛星在哪、鐘差多少，寫在廣播電文裡；每秒 50 位元；一整框 30 秒重複；收齊前三段最久約 36 秒【官方規格＋研究文獻】

- **可用說法**：p146–p159。p156「鐘差跟衛星在哪，放在每一輪最前面的三段」交代了「三段」是什麼（Subframe 1 鐘差、2–3 星曆），p157 才說「傳統的做法要聽完這三段」；片中不說「接收機」
- **來源**：[6]、[14]、[7]
- **原文**：SPS PS [6] §2.2：「the LNAV data also clocked at 50 bps」；Fig. 2.2-1：Subframe 1「Satellite Clock Correction Terms」、Subframe 2–3「Ephemeris Parameters」、「Frame (30 sec repeat)」。
  Blay et al. [14] §2：「Conventional GNSS receivers need to receive the data from the first three subframes of the 30 second navigation frame to solve for time and position. For the GPS L1 C/A signal, it can take as long as 36 seconds」。
  FAA [7]：「The signal contains data that a receiver uses to compute the locations of the satellites」。
- **注意**：「位元＝資料裡最小的一格，只能是或不是」是一般定義（p154），不另外引用。「一個字一個字慢慢念」是**比喻**。只講 GPS L1 C/A 的舊電文，不講其他系統。

## C18 冷開機要找遍天空；已有精確衛星位置（熱開機）不用再等；都市峽谷訊號斷續，等更久【教材】

- **可用說法**：p160–p163
- **來源**：[13]
- **原文**：Navipedia [13]：「in case the receiver already has a valid navigation message, it does not need to decode it」；「Cold start: … no information is available at the receiver and therefore the receiver entails a full search of the sky」；
  「Hot start: … the receiver has both accurate ephemeris and information on frequency offset as well as an accurate initial solution」；「in harsh environments, such as urban canyons, the signals may suffer interruptions or even obstruction blocking the TTFF process」。
- **注意**：暖開機（有曆書）沒講，**簡化**。不給秒數。

## C19 輔助 GPS：手機透過行動網路先拿到衛星位置與鐘差；只要幾毫秒的訊號就能定位【研究文獻】【接收機實際做法】

- **可用說法**：p164–p169
- **來源**：[14]
- **原文**：Blay et al. [14] §2：「With the A-GNSS technique, receivers can solve for position with only milliseconds of IF data, receiving the navigation data message via an alternate source … the precise orbital and clock parameters, also known as the assistance data … For the mobile phone, this data is typically provided through the cellular network using the Secure User Plane Location (SUPL) protocol」。
- **注意**：「typically」→ 片中說「手機透過行動網路」，沒說每支手機都這樣；SUPL 不念。p169「有人先把每個朋友站在哪傳訊息給你」是**比喻**。

## C20 代價：沒有從電文讀到精確時間；衛星在動，時間錯 → 算出的衛星位置錯；每差一秒距離錯約 800 公尺；把時間當第五個未知數，要至少五顆衛星【研究回顧】

- **可用說法**：p170–p178
- **來源**：[14]
- **原文**：Blay et al. [14] §2.1：「the problem is that the time is in error, so the normal four-state least squares algorithm can not solve for the receiver position and common bias … For each one second of error, the pseudoranges would be incorrect on the order of 800 m (Van Diggelen, 2009). There is hope though, as we know the velocities of the satellites, and thus the pseudorange rate.」
  「Since there are now five columns of the H matrix, there now must be at least five satellites to solve for δx.」
  §1：「van Diggelen's technique … is the one that is representative and is being widely used」。
- **注意**：800 m 是 Blay 等 2021 引述 van Diggelen 2009，不是 Blay 自己的實驗；片中說「一篇導航期刊的論文回顧一個常用的方法」，把歸屬講出來。van Diggelen 2009 原書沒讀。
  「量出的距離就錯」＝偽距（pseudorange）錯，**簡化**。

## C21 （第三輪刪除）藍點對了導航還帶錯路

盲評 no_detour：跟「藍點為什麼跳」無關，整段（舊 p177–p180）與 loop `map` 一起刪掉。GPS.gov [1] 的地圖錯誤一段片中已不用。

## C22 收尾：小問的答案、所長的意見【回收，意見標成意見】

- **可用說法**：p181–p186。p185–p186「說得好。還記得那支慢一秒的錶嗎？我覺得最神奇的是：手機每次定位，都在幫自己對錶。」是所長的**意見**，內容對應 C07（每次解算都把鐘差當未知數）。
  p183–p184「訊號撞牆晚到一點點，手機就把我算到對街了」是小問把多路徑（繞遠路＝量到的時間變長，C13）說成自己的話；第二輪拿掉了逐條回顧（哨子、第四顆、被擋）。

## 來源

1. GPS.gov〈GPS Accuracy〉FAQ（現行頁），https://www.gps.gov/node/70 （2026-11-11 讀）
2. GPS.gov 典藏頁〈GPS Accuracy〉，https://archive.gps.gov/systems/gps/performance/accuracy/ （頁首：2025 年 2 月後未更新；只用來確認哪一句**不用**）
3. GPS.gov〈Frequently Asked Questions〉，https://www.gps.gov/faq
4. GPS.gov〈Space Segment〉，https://www.gps.gov/space-segment
5. GPS.gov〈Augmentation Systems〉，https://www.gps.gov/augmentation-systems
6. U.S. DoD, *GPS Standard Positioning Service Performance Standard*, 5th ed., April 2020（§2.2、Fig. 2.2-1、§3.8 Table 3.8-1、A.8.2、B.2.1、B.2.4.3.4、Glossary），https://archive.gps.gov/technical/ps/2020-SPS-performance-standard.pdf （現行版入口 https://www.gps.gov/node/205 ）
7. FAA〈Satellite Navigation - GPS - How It Works〉，https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/gps/howitworks
8. van Diggelen, F. & Enge, P. (2015). The World's first GPS MOOC and Worldwide Laboratory using Smartphones. *Proc. ION GNSS+ 2015*, 361–369（摘要），https://www.ion.org/publications/abstract.cfm?articleID=13079
9. ESA Navipedia〈Code Based Positioning (SPS)〉oldid=12251，https://gssc.esa.int/navipedia/index.php/Code_Based_Positioning_(SPS)
10. ESA Navipedia〈Multipath〉oldid=11617，https://gssc.esa.int/navipedia/index.php/Multipath
11. ESA Navipedia〈Ionospheric Delay〉oldid=13741，https://gssc.esa.int/navipedia/index.php/Ionospheric_Delay
12. ESA Navipedia〈Klobuchar Ionospheric Model〉oldid=16790，https://gssc.esa.int/navipedia/index.php/Klobuchar_Ionospheric_Model
13. ESA Navipedia〈TTFF〉oldid=13355，https://gssc.esa.int/navipedia/index.php/TTFF
14. Blay, R., Wang, B. & Akos, D. M. (2021). Deriving Accurate Time from Assisted GNSS Using Extended Ambiguity Resolution. *NAVIGATION* 68(1):217–229, doi:10.1002/navi.412，https://navi.ion.org/content/68/1/217
15. Ashby, N. (2003). Relativity in the Global Positioning System. *Living Reviews in Relativity* 6:1（Europe PMC 全文 XML），https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5253894/fullTextXML
16. NOAA National Weather Service〈Understanding Lightning: Thunder〉，https://www.weather.gov/safety/lightning-science-thunder
17. NIST CODATA〈speed of light in vacuum〉，https://physics.nist.gov/cgi-bin/cuu/Value?c
