# curio-h18-flight-19 獨立查核（第二輪）

- 查核者：Antigravity 查核子代理（沒有寫過 video.json 或 brief.md），2026-11-14。
- 範圍：第三版 video.json（t001–t099，對照重新產生的 `/tmp/h18panel/panel.txt`）與章名。只讀不改 video.json。
- 當天親自打開的來源：
  - M https://www.nasflmuseum.com/flight-19 （全頁，含 14 人小傳）
  - S https://www.smithsonianmag.com/history/how-the-disappearance-of-flight-19-a-navy-squadron-lost-in-1945-fueled-the-legend-of-the-bermuda-triangle-180987759/ （全文）
  - K https://skeptoid.com/episodes/337 （全文）
  - J https://www.data.jma.go.jp/vois/data/tokyo/323_BeyonesuRocks/323_history.html （1952–53 條）
  - H https://jha.or.jp/jp/shop/products/suiro/pdf/suiro165.pdf （pp.2–3，第 2 節，`pdftotext`）
  - W https://en.wikipedia.org/wiki/Flight_19 （引 McDonell 1973 Naval Aviation News 與海軍調查委員會紀錄）
  - WD https://en.wikipedia.org/wiki/Devil%27s_Sea 與 https://ja.wikipedia.org/wiki/ドラゴントライアングル （引 Berlitz 1974 pp.91–92、Berlitz 1989、Kusche 1975 pp.252–260、讀賣新聞 1955-01-14、NYT 1955-01-16 p.8）
  - N（NOAA）、C（國會紀錄）沿用第一輪 verify-1.md 的逐字核對，這一輪的 NOAA 句子與第一輪相同。
- 沒開：Berlitz 兩本原書、Kusche 原書與 Skeptical Inquirer 原文、NYT 1955 原報（只看到標題與 WD 的轉述）。

## 必須改（REQUIRED）

### 1. t081 與章名「一九八九年，三角被搬到了日本」

- 問題：Berlitz 不是 1989 年才把三角「搬到」日本。他 1974 年那本《The Bermuda Triangle》就已經寫了魔鬼海（K：“his book's 1974 appearance, which did discuss the Devil's Sea in addition to the Bermuda Triangle”；WD：“In 1974 … Berlitz introduced the Devil's Sea in his book The Bermuda Triangle”，引 Berlitz 1974 pp.91–92）。1989 年的《The Dragon's Triangle》是第一本專寫它的書，並把它叫做 Dragon's Triangle。
- t081 原：「這次他把三角搬到東京南方的魔鬼海，列了一長串失蹤的船。真的那麼多嗎？」
- t081 改：「這次整本書都在寫東京南方的魔鬼海，列了一長串失蹤的船。真的那麼多嗎？」
- 章名原：「一九八九年，三角被搬到了日本」
- 章名改：「一九八九年，一整本書寫日本的魔鬼海」
- t080 不必改（1989、《The Dragon's Triangle》成立：K、WD）。

### （已隨第三版刪除，留紀錄）舊稿「魔鬼海這個說法最早只追到一九七〇年代初的美國超自然作家」

- 這句第三版已經刪掉，不用再改；但**不要再加回來**。Skeptoid 的說法被更早的報紙推翻：Kusche 1975 找到 NYT 1955-01-16（路透電）用 “Devil's Sea” 報導第十伸洋丸失聯（後來平安），讀賣新聞 1955-01-14 已寫漁民稱那片海「魔の海」（WD 兩語版）。若之後要講名稱來源，只能寫「一九五五年日本報紙寫一艘失聯的船，外電把它譯成魔鬼海」。

## 建議微調（optional）

- **t086**　原：「調查委員會寫得很清楚：船被海底火山的爆發直接擊中，當場翻覆。」
  - 建議：「調查委員會的結論是：船被海底火山的爆發直接擊中，當場翻覆。」
  - 理由：H「…直撃を受け、直ちに転覆沈没したと結論づけた」是委員會依撈到的碎片推定的結論（ja 維基：「推定された」），「寫得很清楚」語氣比來源確定。
- **章名「一九六四年，一本雜誌替這片海取了名字」**
  - 建議：「一九六四年，一本雜誌讓這個名字紅了」
  - 理由：S 只說 Gaddis “the first to popularize this term”；K 後加更正，聽眾找到更早的零星用例。t073 已寫「開始流行」是對的，章名說「取了名字」略超出。
- **video.json sources**：Skeptoid #337 把第五海洋丸寫成 1953 年、把魔鬼海名稱來源寫成 1970 年代，兩點都錯；本片現在只用它支持「最有名」與 Kusche 的漁船結論（t082、t088），可以留。若想補一條較穩的出處，可加 en.wikipedia.org/wiki/Devil%27s_Sea（Berlitz 1974 已寫魔鬼海、Kusche 1975 的漁船與 31 人）。

## 逐行結果

| 行 | 結論 | 來源與說明 |
| --- | --- | --- |
| t001 | ok | N；M：Fort Lauderdale／Miami–Bermuda–Puerto Rico |
| t002 | ok | 傳說描述，非事實主張 |
| t003 | ok | S：Spielberg《Close Encounters》（電影）、Fleetwood Mac 與 Barry Manilow（歌）、Scooby-Doo（卡通）；W：*Scooby-Doo! Pirates Ahoy!* |
| t004 | ok | 詮釋句 |
| t005 | ok | M；S：1945-12-05，五架 Avenger 訓練飛行 |
| t006 | ok | S；M：PBM Mariner 13 人也失蹤 |
| t007 | ok | S：“Don't come after me”，後來 “assume mythical significance” |
| t008–t009 | ok | 承諾句與提問 |
| t010 | ok | S：“World War II, which had ended just three months earlier” |
| t011 | ok | M；S：NAS Fort Lauderdale 訓練基地 |
| t012 | ok | M：當天有 Flight 17、18 等批次；“last practice before graduation”；W：Navigation Problem No. 1 |
| t013 | ok | 比喻 |
| t014 | ok | M；S：5 架 TBM Avenger、14 人 |
| t015 | ok | M 小傳：Devlin 17 歲；Parpart、Gruebel 18；Devlin（Enterprise）、Thompson（Franklin）、Gallivan（Guadalcanal、Tarawa）等打過太平洋戰爭 |
| t016 | ok | M：28 歲、2,509.3 小時；S：28 歲、2,500 多小時；USNR Lieutenant＝上尉 |
| t017 | ok | M：1945-11-21 調到 NAS Fort Lauderdale（到 12-05 為 14 天）；S（Bloom）：從邁阿密調來、不熟這一帶 |
| t018 | ok | M：14:10 起飛；S、W：先往東到 Bimini 附近 Hens and Chickens 練投彈，再往北越過 Grand Bahama，再轉回 |
| t019 | ok | M：東 141 哩、北 73 哩、回程 140 哩；C：“triangular route” |
| t020 | ok | S：約 2 小時 40 分 |
| t021 | ok | S：Cox “shortly before 3:45 p.m.” 收到；W：15:40 左右；Cox 是另一隊的教官（FT-74）；W（McDonell 1973）：說「我不知道我們在哪裡」的是學員 Powers，「一個學員」成立 |
| t022 | ok | S；W：“I don't know where we are. We must have got lost after that last turn.” |
| t023 | ok | S；W：“both my compasses are out … I'm sure I'm in the Keys”（節錄） |
| t024 | ok | 常識 |
| t025 | ok | S：“impossible for the group to be over the Keys so soon after taking off”；M：起飛約 90 分鐘後報告迷路 |
| t026 | ok | S：館長 John Bloom：Taylor 上個月才從邁阿密調來，“This may explain the pilot's belief that he was over the Keys instead of the Bahamas”；W：調查報告也認為他把小島誤認為 Keys |
| t027 | ok | S：Cox 提議飛過去；Taylor 說已知道在哪，“Don't come after me” |
| t028 | ok | S：Berlitz 1974 年加了半句；距 1945 為 29 年，「快三十年」成立 |
| t029 | ok | S：事後報告強調曾要他們往西 “into the sun”，調查員認為照做 “certain this flight would have returned” |
| t030 | ok | 轉場 |
| t031 | ok | S：訊號越來越弱，離海岸越來越遠 |
| t032 | ok | S；W：16:45 “fly north to make sure we are not over the Gulf of Mexico” |
| t033 | ok | S：半小時後往西 “until we hit the beach or run out of gas” |
| t034 | ok | S：保持編隊、油少時一起迫降 |
| t035 | ok | S；W：18:04 “didn't go far enough east … go east again” |
| t036 | ok | S：沿岸機場與船點燈，他們卻往反方向飛 |
| t037 | ok | S：約 18:00 算出 fix，“well north of the Bahamas and roughly east of Daytona Beach”；W：17:50 |
| t038 | ok | 提問 |
| t039 | ok | S：ready plane；Cox 回站後要求開它去找；M：同 |
| t040 | ok | S：Lt Cdr Donald J. Poole，“the officer in charge of training flights”；“confident and certain that they would hit the coast before their gas supply ran out” |
| t041 | ok | M：天氣與海況入夜變壞；16:00 記錄地面颮線、1,000 呎 40 哩風 |
| t042 | ok | S；M：19:04 Ensign Joseph Bossi 呼叫 Taylor（W 另記 Taylor 最後訊息 18:20，兩說並存，照 S 與 M 可） |
| t043 | ok | S：“No response was heard.”；最後已知訊息 |
| t044 | ok | 轉場 |
| t045 | ok | S；W：兩架 PBM-5 Mariner 19:27 從 NAS Banana River（基地以北約 150 哩）起飛 |
| t046 | ok | S：13 人；“Within half an hour, the Mariner suddenly fell off radio contact” |
| t047 | ok | M：S.S. Gaines Mills 19:50 看到海上爆炸；S：約 100 英尺（≈30 公尺）的火 |
| t048 | ok | M：“widespread oil slick” |
| t049 | ok | S：“flying gas tanks” due to high fuel capacity and propensity to onboard fires |
| t050 | ok | S：搜救五天；M：“the biggest rescue effort of peacetime” |
| t051 | ok | M：“The Navy alone ordered 248 planes into the air, while 18 surface craft” |
| t052 | ok | M：超過 20 萬平方英里；≈518,000 km² ÷ 台灣約 36,000 km² ≈ 14.4 |
| t053 | ok | S：12-09 United Press 報六艘救生筏，官方隨即說是誤認 |
| t054 | ok | S：“No confirmed trace”；6 架、27 人 |
| t055 | ok | 提問 |
| t056 | ok | S：1946 年 1 月內部報告承認協調等可改進 |
| t057 | ok | S：“something akin to a mental aberration”，寫的人是 “the chief of naval air training” |
| t058 | ok | S：收到電報時在 Corpus Christi（德州）教室前 |
| t059 | ok | S：“walked out, never to return” |
| t060 | ok | S：她認為報告缺實物證據與飛行員本人說法 |
| t061 | ok | S：1946 年 3 月前到佛州訪談參與搜救的人 |
| t062 | ok | S；M：寫信給同機 18 歲無線電員 Walter Reed Parpart Jr. 的母親 |
| t063 | ok | S：“emotionally unstable” |
| t064 | ok | 轉場 |
| t065 | ok | S；M：1947 年 Board for Correction of Naval Records |
| t066 | ok | S：“reasons or causes unknown” |
| t067 | ok | M：Taylor 被除去 “responsibility for loss of lives and naval aircraft”（詮釋合理） |
| t068 | ok | 提問 |
| t069 | ok | S：1950 AP 文章 |
| t070 | ok | S：“erroneously suggested had disappeared under complete radio silence” |
| t071 | ok | 15:45–19:04，三個多小時 |
| t072 | ok | S；K：Argosy 1964 年 2 月號，Gaddis〈The Deadly Bermuda Triangle〉；S：“men's magazine” |
| t073 | ok | S：“the first to popularize this term” |
| t074 | ok | S：Gaddis “the lost patrol”；M：“not a patrol flight, it was a training flight” |
| t075 | ok | S：“his best-selling 1974 book, The Bermuda Triangle” |
| t076 | ok | S：“don't come after me … they look like they are from outer space” |
| t077 | ok | S：“falsely relayed”；K（轉引 Kusche）：調查報告未提 Berlitz 引的通訊 |
| t078 | ok | S：Mariner 在同一帶失蹤被當成超自然，“ignoring the fact that a rescue plane would naturally be sent to its target's presumed location” |
| t079 | ok | 詮釋句，事實基礎同 t065、t075 |
| 章名（07:29） | **fix** | 見〈必須改〉1 |
| t080 | ok | K；WD：Berlitz 1989《The Dragon's Triangle》 |
| t081 | **fix** | 見〈必須改〉1；「東京南方」成立（WD：“a region of the Pacific, south of Tokyo”；K：台灣到三宅島、硫磺島一帶）；「列了一長串失蹤的船」成立（K：“listed numerous Japanese ships and sailors lost”） |
| t082 | ok | K：“Its most famous casualty was the No. 5 Kaiyo-Maru”；ja 維基所列《The Dragon's Triangle》名單含 1952-09-24 第五海洋丸（書中誤作「第五海王丸」）；年份 1952 以 J、H 為準（K 寫 1953 是錯的） |
| t083 | ok | H：明神礁 1952 年 9 月噴發，為確定噴火位置派遣第五海洋丸；J：「調査中の水路部所属第5海洋丸」 |
| t084 | ok | H：9 月 23 日從東京出發，預定 24 日到，「その日から定時連絡が絶えた」 |
| t085 | ok | H：明神礁南方、南南西方陸續找到船體一部；J：31 名殉職 |
| t086 | ok（建議微調） | H：第五海洋丸遭難調查委員會結論：24 日 12:20 左右右舷斜下方受爆發直擊，「直ちに転覆沈没」；見〈建議微調〉 |
| t087 | ok | 詮釋句；H 的結論早在 1952–53 年就寫好，Berlitz 1974 卻把它寫成 1955 年的謎（WD） |
| t088 | ok | K：Kusche（Skeptical Inquirer）：Berlitz 說的軍艦其實是漁船，損失率與日本周邊漁船一向相同；WD：Kusche 1975：九艘船大多是小漁船 |
| t089 | ok | N：U.S. Board on Geographic Names 不承認；“no official maps exist that delineate the boundaries” |
| t090 | ok | N：“no evidence that mysterious disappearances occur with any greater frequency … than in any other large, well-traveled area of the ocean” |
| t091 | ok | N：“The majority of Atlantic tropical storms and hurricanes pass through the Bermuda Triangle” |
| t092 | ok | N：Gulf Stream、天氣驟變、加勒比海淺水 |
| t093 | ok | 標「我覺得」的看法 |
| t094 | ok | S：結論是 “reasons or causes unknown”，不是超自然 |
| t095 | ok | S：真正解不開的是 Taylor 一開始為何偏航，以及 19:04 之後發生什麼 |
| t096 | ok | 感想 |
| t097 | ok | S：Cox 要求開待命飛機被拒（t039–t040） |
| t098–t099 | ok | 互動與片尾 |

## 無法確認

- 沒有無法確認的旁白。NYT 1955-01-16 與讀賣 1955-01-14 原報我沒有親眼看到，只看到 NYT 檔案標題與英、日維基的轉述；它們只影響已刪掉的舊句，不影響第三版。

## Round 5（2026-11-14，第五版 t001–t090）

- 日本章（Berlitz 1989《The Dragon's Triangle》、第五海洋丸、漁船名單）整章刪除。上面〈必須改〉1（t081 與 07:29 章名）與 t086 的建議因此不再適用；日本章各行的查核留作紀錄，不必再處理。章名已改成「一九六四年，一本雜誌讓這個名字紅了」，與上面的建議一致。
- 回呼改寫，沒有新的事實主張：
  - t014「開頭說的那五架，是 Avenger 魚雷轟炸機，一共十四個人」：M；S，5 架 TBM Avenger、14 人。ok。
  - t027「Taylor 的回答，就是開頭那句：不用，我知道我在哪裡了，不要來找我」：S。ok。
  - t045「七點二十七分，開頭說的救援機出發了：兩架 PBM Mariner 水上飛機」：S、W：兩架 PBM-5 Mariner 19:27 從 NAS Banana River 起飛。拿掉「從北邊的基地」只是少了細節，不影響正確。t006 說救援機沒回來、t046 說其中一架（13 人）失聯，兩句合起來與來源一致。ok。
  - t080「回到開頭的問題，NOAA 說得很直接：它不是官方地名，也沒有官方地圖畫範圍」：N。ok。
  - t082「那為什麼還是一直有船出事？大西洋的熱帶風暴和颶風，大多會經過這一帶」：N。ok。t084 是標「我覺得」的看法。
- 第五版沒有需要改的地方，也沒有查不到出處的旁白。`claims.md` 已照 t001–t090 重寫，日本章的列已刪除。
