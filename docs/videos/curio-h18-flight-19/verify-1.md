# curio-h18-flight-19 獨立查核（第一輪）

- 查核者：Antigravity 查核子代理（不是撰稿者，沒有寫過 video.json 或 brief.md），2026-11-14。
- 範圍：video.json 的 t001–t107 全部旁白、youtube.title／description、sources 標題。只讀不改 video.json 與 brief.md。
- 當天親自打開的來源：
  - https://www.nasflmuseum.com/flight-19 （全頁，含 14 人小傳）
  - https://www.smithsonianmag.com/history/how-the-disappearance-of-flight-19-a-navy-squadron-lost-in-1945-fueled-the-legend-of-the-bermuda-triangle-180987759/ （全文）
  - https://www.govinfo.gov/content/pkg/CRECB-2005-pt19/html/CRECB-2005-pt19-Pg26365.htm （決議文與全部院會發言）
  - https://oceanservice.noaa.gov/facts/bermudatri.html （全頁）
  - https://www.data.jma.go.jp/vois/data/tokyo/323_BeyonesuRocks/323_history.html （1946、1952–53 條）
  - /tmp/suiro165.pdf（https://jha.or.jp/jp/shop/products/suiro/pdf/suiro165.pdf ，`pdftotext -f 1 -l 4`，第 2 節）
  - https://skeptoid.com/episodes/337 （全集逐字稿）
- 沒開、沒用：海軍 Board of Investigation 原始紀錄（約 400 頁微縮膠片）、1950 AP 原文、1964 Argosy 原文、Berlitz 原書、Sanderson《Pursuit》1971 原刊、Kusche 的 Skeptical Inquirer 原文。這些都只透過 S、K 的轉述。
- 篩選筆記 wave2-legacy-20261101.json 的 H18 與 L5-S004..S011 只當線索。

來源代號：M＝NAS Fort Lauderdale Museum〈Flight 19 the Lost Avengers〉；S＝Smithsonian Magazine（Francine Uenuma，2025-12-05）；C＝Congressional Record 2005 Vol. 151 Pt 19 pp. 26365–26367（H. Res. 500）；N＝NOAA National Ocean Service〈What is the Bermuda Triangle?〉；J＝氣象廳〈ベヨネース列岩 有史以降の火山活動〉；H＝日本水路協會《水路》165 號 伊藤弘志 pp.1–3；K＝Skeptoid #337（Brian Dunning，2012-11-20）。

## 改了什麼

### 必須改（與來源不符或超出來源）

- **t040**　原：「值勤的長官說不行。他認為這些人只是一時迷路，油用完前一定會自己飛回來。」
  - 改成：「負責訓練飛行的長官說不行。他後來作證：他確信這些人在油用完以前，一定會飛回海岸。」
  - 理由：拒絕的是 Lt Cdr Donald J. Poole，“the officer in charge of training flights there”，不是值勤官。Poole：“didn't think there was any use”、等 fix、怕干擾通訊、“confident and certain that they would hit the coast before their gas supply ran out”。「一時迷路」（temporarily confused）是作戰官 Kenyon 的證詞
- **t081**　原：「美國海洋暨大氣總署 NOAA 說得很直接：百慕達三角不是官方地名，也沒有地圖畫出範圍。」
  - 改成：「美國海洋暨大氣總署 NOAA 說得很直接：百慕達三角不是官方地名，也沒有官方地圖畫範圍。」
  - 理由：NOAA：“no official maps exist that delineate the boundaries”（NOAA 轉述海軍與海岸防衛隊）；NOAA 自己的頁面就放了一張示意地圖，所以「沒有地圖畫出範圍」與來源相反，要加「官方」
- **t099**　原：「那魔鬼海這個名字哪裡來的？目前找得到最早的，是一九七一年美國一本超自然刊物。」
  - 改成：「那魔鬼海這個說法哪裡來的？有研究者追查，最早只追到一九七〇年代初，美國的超自然作家。」
  - 理由：Skeptoid：Sanderson 1971 年 4 月在其研究會會刊 Pursuit 寫 “vile vortices”（12 個漩渦），1972 年 Saga 轉載為 “The Twelve Devil's Graveyards”；Skeptoid 說 Berlitz 從 vile vortices 得到 Devil's Sea 的靈感，並說找不到 Berlitz 與 Sanderson 之前的用例。沒有寫明 1971 年那篇用了「魔鬼海」這個名字，而且只有 Skeptoid 一家；寫成「這個名字最早是一九七一年」超出來源
- **t103**　原：「我們真正不知道的，只有剛剛那個七點零四分之後，那些年輕人在海上經歷了什麼。」
  - 改成：「我們真正不知道的，是他當初怎麼迷的路，和七點零四分之後，那些年輕人在海上經歷了什麼。」
  - 理由：Smithsonian 結尾列出兩個真正解不開的謎：Taylor 一開始為什麼偏離航線，以及 19:04 之後發生什麼。旁白說「只有」七點零四分之後，漏了第一個

### 建議微調（不改不算錯，改了更準）

- **t057**　原：「可是負責飛行訓練的長官寫得更直接：領隊糊塗到，近似某種精神錯亂。」
  - 建議：「可是海軍航空訓練的最高長官寫得更直接：領隊糊塗到，近似某種精神錯亂。」
  - 理由：“something akin to a mental aberration”，寫的人是 “the chief of naval air training”（海軍航空訓練的首長），不是基地裡負責訓練飛行的人；t040 改成 Poole 的職稱後兩句會混淆
- **t016**　原：「有的才十八、九歲，有的剛從太平洋打完仗回來。」
  - 建議：「有的才十七、八歲，有的剛從太平洋打完仗回來。」
  - 理由：博物館各人小傳：最小的是 Devlin 17 歲（Parpart、Gruebel 18；Baluk、Lightfoot、Thelander 19）；Devlin（Enterprise）、Thompson（Franklin）等打過太平洋戰爭。原句不算錯，但漏了 17 歲
- **t028**　原：「記住這句話。三十年後，會有人在它後面，多加半句。」
  - 建議：「記住這句話。快三十年後，會有人在它後面，多加半句。」
  - 理由：Berlitz 1974 年，距 1945 是 29 年；「三十年後」是約數
- **t100**　原：「後來有研究者去翻失蹤名單，發現大多是小漁船，比例跟日本周邊其他海域差不多。」
  - 建議：「後來有研究者去翻失蹤名單，發現大多是漁船，損失的比例跟日本周邊一向差不多。」
  - 理由：Kusche（Skeptical Inquirer）：Berlitz 說是軍艦的其實是漁船，損失率跟日本周邊漁船一向的損失率相同。來源沒寫「小」，也沒寫「大多」以外的比例細節

### 說明與附帶發現

- 指定要特別看的點，除上列外全部成立：Taylor 11-21 調來（14 天）、2 小時 40 分、約 15:45 Cox 收到的第一句、羅盤與 Keys 引句、16:45／17:15／18:04、fix 的位置、7:04 Bossi、7:27 Banana River（在基地以北約 150 哩）、13 人、7:50 Gaines Mills 100 英尺火光與油跡、flying gas tanks、5 天／248 架／18 艘／20 萬平方英里（14.4 個台灣）、12-09 UP 六艘救生筏、1946-01 報告與 chief of naval air training 的引句、德州教室、佛州訪談、寫給 Parpart 母親、emotionally unstable、1947 更正委員會 reasons or causes unknown、1950 AP、1964 Argosy／Gaddis／lost patrol、1974 Berlitz 暢銷與外星半句、NOAA 各句、明神礁各數字、31 人、12:20 右舷斜下方直擊。
- t045 的 7:27：Smithsonian 寫起飛時間，博物館寫的是起飛後的無線電回報，國會紀錄寫約 7:30 起飛。兩說並存，照 Smithsonian 可以，不必改。
- t094「海上保安廳派出」：第五海洋丸屬海上保安庁水路部（氣象廳原文「水路部所属」），1952 年水路部是海上保安庁的內部單位，寫「海上保安廳」可接受；若要更精確可寫「海上保安廳水路部」。
- Skeptoid 把第五海洋丸寫成 1953 年，與氣象廳、水路協會相反；旁白用 1952 年是對的，Skeptoid 這一點不能引。
- 國會紀錄裡 Spratt 議員把 “They look like they're from outer space” 當成 Taylor 7:04 說的話，正是 Berlitz 版本的流傳，不可當作證據；本片沒有用。
- youtube.title、description：成立（6 架、27 人、同一晚、1947 更正、1964／1974、日本調查委員會）。
- sources 標題：成立。氣象廳頁的實際標題是「ベヨネース列岩 有史以降の火山活動」，video.json 多加了「（明神礁）」當說明，不算錯。
- 無法確認：無（t099 改寫後只說到 Skeptoid 能支持的程度）。

## 逐行對照

| 行 | 旁白（節錄） | 來源 | 狀態（確認／需改／無法確認） |
| --- | --- | --- | --- |
| t001 | 你一定聽過百慕達三角：佛羅里達、百慕達和波多黎各之間那片海。 | N；K；M：Skeptoid：Miami–Bermuda–Puerto Rico；博物館：Fort Lauderdale–Bermuda–Puerto Rico | 確認 |
| t003 | 可是你去翻美國政府的地名資料，找不到這個地名，它連正式的邊界都沒有。 | N：U.S. Board of Geographic Names 不承認為正式名稱、不設檔；沒有官方地圖畫出邊界 | 確認 |
| t005 | 一九四五年冬天，五架海軍訓練機起飛，再也沒有回來。 | M；S；C：1945-12-05，五架 TBM Avenger 訓練飛行 | 確認 |
| t006 | 連去找他們的救援機，也沒有回來。一共二十七個人。 | S；C；M：6 架、27 人（14＋13） | 確認 |
| t007 | 一句無線電裡的「不要來找我」，後來被人補上半句：他們看起來像外星來的… | S：Berlitz 把 “don't come after me” 寫成 “… they look like they are from outer space” | 確認 |
| t008 | 而海軍最後的結論，只有四個字：原因不明。 | S；M：1947 年更正委員會：“reasons or causes unknown” | 確認 |
| t011 | 時間回到那一年，第二次世界大戰才結束三個月。 | S：“World War II, which had ended just three months earlier” | 確認 |
| t012 | 佛羅里達的 Fort Lauderdale 海軍航空站，每天都有學員… | M；S：NAS Fort Lauderdale | 確認 |
| t013 | 那天下午排到第十九批，所以叫 Flight 19。它不是巡邏隊，是一… | M；C：博物館：當天有 Flight 17、18 等批次；“not a patrol flight, it was a training flight”；“last practice before graduation”；國會紀錄：Navigation Problem Number 1 | 確認 |
| t015 | 五架 Avenger 魚雷轟炸機，一共十四個人。 | M；S；C：5 架 TBM Avenger、14 人 | 確認 |
| t016 | 有的才十八、九歲，有的剛從太平洋打完仗回來。 | M：博物館各人小傳：最小的是 Devlin 17 歲（Parpart、Gruebel 18；Baluk、Lightfoot、Thelander 19）；Devlin（Enterprise）、Thompson（Franklin）等打過太平洋戰爭。原句不算錯，但漏了 17 歲 | 確認（建議微調） |
| t017 | 帶隊的是二十八歲的教官 Charles Taylor 上尉，飛了兩千… | M；S：28 歲；2,509.3 飛行小時；USNR Lieutenant（O-3＝上尉） | 確認 |
| t018 | 先記住一個細節：他兩個禮拜前才從邁阿密調過來，這一帶他還不熟。 | M；S：博物館：“recently transferred to NAS Fort Lauderdale (November 21, 1945)”，到 12-05 為 14 天；Smithsonian（Bloom）：“transferred up from Miami the previous month”，不熟這一帶 | 確認 |
| t019 | 下午兩點十分起飛。往東飛到巴哈馬附近練投彈，再往北，最後轉回基地。 | M；S；C：14:10 起飛；先往東到 Bimini／Hen and Chickens 一帶練投彈，再往北，最後回基地 | 確認 |
| t020 | 我第一次看到這條航線還愣了一下：他們要飛的，本身就是一個三角形。 | C：國會紀錄：“on a triangular route”（「我第一次看到」是旁白感想） | 確認 |
| t021 | 預定不到三個小時就回來。到底是在哪一個轉彎出錯的？ | S：“intended to last around 2 hours and 40 minutes” | 確認 |
| t022 | 三點四十五分左右，另一位教官 Robert Cox 在附近飛，耳機裡… | S：Cox “picked up that first concerning transmission shortly before 3:45 p.m.”；Cox 是另一個飛行的教官（博物館：Senior Flight Instructor） | 確認 |
| t023 | 我不知道我們在哪裡。 | S：“I don't know where we are … We must have got lost after that last turn.” Smithsonian 把它寫成第一則訊息；說話者未具名，旁白也沒說是誰 | 確認 |
| t024 | 回話的是 Taylor：「我的兩個羅盤都壞了。我確定我在 Flori… | S；M：“both my compasses are out. … I'm sure I'm in the [Florida] Keys”（中間省略 “I am over land, but it's broken”，屬節錄，不改義） | 確認 |
| t025 | Florida Keys，就是佛羅里達最南端那串小島。 | 常識：Florida Keys 為佛州最南端島鏈 | 確認 |
| t026 | 奇怪的是，起飛才一個多小時，照航線，他們根本不可能飛到那麼南邊。 | S；M：14:10→約 15:40 為一個多小時；博物館：約起飛 90 分鐘後報告迷路；Smithsonian：“impossible for the group to be over the Keys so soon after taking off” | 確認 |
| t027 | Cox 說要飛過去帶路。Taylor 回答：不用，我知道我在哪裡了，… | S：Cox 提議飛過去；Taylor 說他現在知道在哪裡，“Don't come after me” | 確認 |
| t028 | 記住這句話。三十年後，會有人在它後面，多加半句。 | S：Berlitz 1974 年，距 1945 是 29 年；「三十年後」是約數 | 確認（建議微調） |
| t029 | 地面告訴他們：往西飛，朝著太陽飛，一定會碰到佛羅里達的海岸。 | S：事後報告強調曾要他們往西 “into the sun”；調查員：若聽到並照做 “certain this flight would have returned to base safely”。註：Cox 本人先建議的是往北、太陽在左翼 | 確認 |
| t031 | 沒想到，Taylor 的聲音越來越小。他們離岸越來越遠，不是越來越近… | S：“transmissions were growing weaker”；離海岸越來越遠 | 確認 |
| t032 | 四點四十五分，Taylor 說要往北飛，先確定自己不在墨西哥灣上空。 | S：約 16:45 “fly north to make sure we are not over the Gulf of Mexico” | 確認 |
| t033 | 五點十五分，他好像想通了：往西飛，飛到碰到海灘，或是油用完為止。 | S：半小時後（≈17:15）往西 “until we hit the beach or run out of gas” | 確認 |
| t034 | 他還交代大家不要散開，油不夠了就一起迫降。 | S：保持編隊、油少時一起迫降 | 確認 |
| t035 | 問題來了。六點剛過，他說了最關鍵的一句：我們往東飛得不夠遠，轉回去，… | S：18:04 “didn't go far enough east — turn around again … go east again” | 確認 |
| t036 | 這時候，沿岸的機場和船正把燈點亮，等他們回家；他們卻往反方向飛。 | S：“lights were being lit at air stations and on ships … they were unknowingly flying in the opposite direction” | 確認 |
| t037 | 差不多同時，地面終於算出大概位置：巴哈馬北方，Daytona Bea… | S：約 18:00 算出 fix：29°N 79°W 方圓 100 哩，“well north of the Bahamas and roughly east of Daytona Beach” | 確認 |
| t039 | 其實有。基地有一架待命的飛機，Cox 落地後主動說要開它出去找。 | S；M：ready plane；Cox 回站後向 Poole 要求開它往東北找 | 確認 |
| t040 | 值勤的長官說不行。他認為這些人只是一時迷路，油用完前一定會自己飛回來… | S：拒絕的是 Lt Cdr Donald J. Poole，“the officer in charge of training flights there”，不是值勤官。Poole：“didn't think there was any use”、等 fix、怕干擾通訊、“confident and certain that they would hit the coast before their gas supply ran out”。「一時迷路」（temporarily confused）是作戰官 Kenyon 的證詞 | 需改 |
| t041 | 天黑了，海上起風，浪越來越大。 | M；S：博物館：天氣與海況入夜變壞；國會紀錄：rain squalls、terrific winds、sea ran rough | 確認 |
| t042 | 七點零四分，有人聽到其中一架的駕駛員 Joseph Bossi，在呼… | S；M：19:04 Ensign Joseph Bossi 呼叫 Taylor | 確認 |
| t043 | 沒有人回答。那是這支飛行隊，留下的最後一句話。 | S；M：“No response was heard.”；最後一則已知訊息 | 確認 |
| t045 | 七點二十七分，兩架 PBM Mariner 水上飛機從北邊的基地起飛… | S；M；C：Smithsonian：兩架 PBM-5 Mariner 19:27 從 NAS Banana River（基地以北約 150 哩）起飛。博物館把 19:27 寫成起飛後不到半小時的無線電回報、國會紀錄寫約 19:30 起飛：時間有兩說，旁白照 Smithsonian 可接受 | 確認 |
| t046 | 其中一架載著十三個人。起飛不到半小時，它也從無線電裡消失了。它去哪了… | S；M；C：13 人；“Within half an hour, the Mariner suddenly fell off radio contact” | 確認 |
| t047 | 七點五十分，附近一艘商船 Gaines Mills，看到海面竄起一團… | M；S；C：博物館：S.S. Gaines Mills 19:50 看到海上爆炸；Smithsonian：“burst of flames” 約 100 英尺（≈30 公尺）；國會紀錄：merchant ship | 確認 |
| t048 | 之後，海上漂著一大片油。 | M：“observed a widespread oil slick” | 確認 |
| t049 | 怎麼會燒起來？這種飛機有個外號，叫「會飛的油箱」：油載得多，又容易起… | S：“flying gas tanks” due to high fuel capacity and propensity to onboard fires | 確認 |
| t050 | 那人呢？接下來五天，是當時和平時期最大的搜救。 | S；M：搜救五天；博物館：“the biggest rescue effort of peacetime” | 確認 |
| t051 | 光是海軍，就派出兩百四十八架飛機，還有十八艘船。 | M：“The Navy alone ordered 248 planes into the air, while 18 surface craft …” | 確認 |
| t052 | 搜過的範圍超過二十萬平方英里。我換算了一下，差不多是十四個台灣。 | M；C；自算：>200,000 平方英里 ≈ 518,000 km²；台灣約 36,000 km² → 約 14.4 個；旁白已標「我換算」 | 確認 |
| t053 | 結果，四天後新聞說找到六艘救生筏；官方很快又說，是看錯了。 | S：12-09（四天後）United Press 報六艘救生筏，官方隨即說是誤認 | 確認 |
| t054 | 最後，一塊確定的殘骸都沒有找到。 | C；S：“failed to recover any aircraft, debris, or remains”；“No confirmed trace” | 確認 |
| t056 | 隔年一月，海軍的調查報告出來了。報告承認，搜救的協調有可以改進的地方… | S：1946 年 1 月內部報告；承認搜救協調等可改進 | 確認 |
| t057 | 可是負責飛行訓練的長官寫得更直接：領隊糊塗到，近似某種精神錯亂。 | S：“something akin to a mental aberration”，寫的人是 “the chief of naval air training”（海軍航空訓練的首長），不是基地裡負責訓練飛行的人；t040 改成 Poole 的職稱後兩句會混淆 | 確認（建議微調） |
| t058 | Taylor 的母親 Katherine 收到電報時，正在德州的教室… | S：收到電報時在 Corpus Christi（德州）教室前 | 確認 |
| t059 | 她走出教室，從此沒有再回去教書。 | S：“walked out, never to return” | 確認 |
| t060 | 她不相信。飛機一架都沒找到，飛行員也沒辦法替自己說話，憑什麼全算在他… | S：她認為報告倚重搜救者證詞，缺實物證據與飛行員本人說法 | 確認 |
| t061 | 她自己跑到佛羅里達，找參加搜救的人一個一個問。 | S：1946 年 3 月前到佛州訪談參與搜救的人 | 確認 |
| t062 | 還寫信給同機那位年輕無線電員的媽媽。 | S；M：寫信給 Taylor 同機 18 歲無線電員 Walter Reed Parpart Jr. 的母親；博物館藏有兩家通信 | 確認 |
| t063 | 海軍的紀錄怎麼寫她？情緒不穩定。 | S：“It is believed that Mrs. Taylor is emotionally unstable as a result of this disaster” | 確認 |
| t065 | 一九四七年，在她不停申訴之後，海軍的紀錄更正委員會改了結論： | S；M：1947 年，在她持續陳情後；博物館：Board for Correction of Naval Records | 確認 |
| t066 | 這支飛行隊，是因為原因不明而失蹤。 | S：“that the flight disappeared for reasons or causes unknown” | 確認 |
| t067 | 這幾個字原本很單純：沒有證據，就不能把錯算在 Taylor 頭上。 | M：博物館：Taylor 1947 年被除去 “responsibility for loss of lives and naval aircraft” 的責任（「很單純」為旁白詮釋） | 確認 |
| t069 | 一九五〇年，美聯社把美國東南外海幾次飛機和船的失蹤寫在一起。 | S：1950 AP 文章，美國東南外海飛機與船的失蹤 | 確認 |
| t070 | 文章還寫錯，說這支飛行隊是在完全沒有無線電的狀態下消失的。 | S：“erroneously suggested had disappeared under complete radio silence” | 確認 |
| t071 | 我們剛剛才聽完它三個多小時的無線電耶。 | S；自算：約 15:45 至 19:04，三個多小時 | 確認 |
| t072 | 一九六四年，男性雜誌《Argosy》刊出 Vincent Gaddi… | S；K：Argosy（men's magazine）1964 年 2 月號，Vincent Gaddis〈The Deadly Bermuda Triangle〉 | 確認 |
| t073 | 致命的百慕達三角。這個名字，就是從 Gaddis 這一篇開始流行的。 | S；K：Smithsonian：“the first to popularize this term”；Skeptoid 原寫 “first time the name is known”，後加更正說有更早的零星用例 → 旁白說「開始流行」正確 | 確認 |
| t074 | 更怪的是，文章把他們叫做失蹤的巡邏隊。可那根本不是巡邏，是一堂導航課… | S；M：Gaddis：“the lost patrol”；實為訓練飛行（博物館、國會紀錄：Navigation Problem No. 1） | 確認 |
| t075 | 一九七四年，Charles Berlitz 寫的《The Bermu… | S；K：“his best-selling 1974 book, The Bermuda Triangle” | 確認 |
| t076 | 那句「不要來找我」，在他的書裡多了半句：他們看起來像外星來的。 | S：“don't come after me … they look like they are from outer space” | 確認 |
| t077 | 可是紀錄裡，沒有這半句。 | S：“falsely relayed”；調查紀錄無此句（Skeptoid 轉引 Kusche：委員會報告未提 Berlitz 引的通訊） | 確認 |
| t078 | 救援機在同一片海上失蹤，也被當成怪事；可是它本來就是被派去那裡找人的… | S：“ignoring the fact that a rescue plane would naturally be sent to its target's presumed location” | 確認 |
| t079 | 而原因不明，從一個母親替兒子討回的清白，變成了神秘力量的證據。 | S：詮釋句，事實基礎同 t065、t075 | 確認 |
| t081 | 美國海洋暨大氣總署 NOAA 說得很直接：百慕達三角不是官方地名，也… | N：NOAA：“no official maps exist that delineate the boundaries”（NOAA 轉述海軍與海岸防衛隊）；NOAA 自己的頁面就放了一張示意地圖，所以「沒有地圖畫出範圍」與來源相反，要加「官方」 | 需改 |
| t082 | 而且，沒有證據顯示，那裡神秘失蹤的次數，比其他又大、船又多的海域更頻… | N：“no evidence that mysterious disappearances occur with any greater frequency … than in any other large, well-traveled area of the ocean” | 確認 |
| t083 | 那為什麼常出事？大西洋的熱帶風暴和颶風，大多會經過這一帶。 | N：“The majority of Atlantic tropical storms and hurricanes pass through the Bermuda Triangle” | 確認 |
| t084 | 再加上流得很快的灣流、說變就變的天氣，和很多淺灘。 | N：Gulf Stream 造成 “rapid, sometimes violent, changes in weather”；加勒比海島多、淺水多 | 確認 |
| t085 | 我覺得這比較像交通量，不是詛咒。 | —：標「我覺得」的看法 | 確認 |
| t086 | 那天下午也一樣：一個不熟這片海的領隊、一次轉錯的方向、越來越壞的天氣… | M；S：不熟這片海（t018）、18:04 轉回往東、天候變壞、油料減少 | 確認 |
| t089 | 東京南方的海上，也有一片魔鬼海，據說船開進去也會消失。 | K：Devil's Sea 大致從台灣到東京南方三宅島、硫磺島一帶；“legends … go back for centuries” 屬流傳 | 確認 |
| t090 | 最有名的例子在一九五二年九月：漁船第十一明神丸回報，海底火山在噴發。 | H；J：水路 165：1952 年 9 月漁船「第11明神丸」無線電報告海底火山活動；氣象廳：9 月 17 日海底噴火。註：Skeptoid 寫 1953 年是錯的 | 確認 |
| t091 | 那座海底火山，後來就用這艘漁船的名字，叫做明神礁。 | H；J：「明神礁の名称も、この「第11明神丸」に由来」；氣象廳：噴火した浅瀬を明神礁と命名 | 確認 |
| t092 | 巡視船趕到，看到海面冒出一座新島，大約一百五十公尺長、三十公尺高。 | H：巡視船「しきね」9 月 18 日：東西 100m、南北 150m、高 30m 的新島 | 確認 |
| t093 | 怪就怪在，位置跟漁船回報的差了十海里以上。 | H：「報告の位置と10海里以上のかい離」 | 確認 |
| t094 | 為了確定火山在哪裡，海上保安廳派出測量船第五海洋丸，從東京出發。 | H；J：「噴火位置を確定させるため「第五海洋丸」が派遣」；9 月 23 日東京出發。所屬是海上保安庁水路部（氣象廳：水路部所属），1952 年水路部隸屬海上保安庁，寫「海上保安廳派出」可接受 | 確認 |
| t095 | 隔天，它的定時聯絡，斷了。船上的人怎麼了？ | H：預定 24 日到達，「その日から定時連絡が絶えた」 | 確認 |
| t096 | 搜救的人在明神礁南方，陸續撈到船體碎片。船上三十一個人，全部殉職。 | H；J：明神礁南方、南南西方陸續找到船體一部；31 名殉職 | 確認 |
| t097 | 調查委員會的結論是：九月二十四日中午十二點二十分左右，船的右下方被爆… | H：第五海洋丸遭難調查委員會：「９月24日12時20分ごろ右舷斜め下方向から爆発の直撃を受け」 | 確認 |
| t098 | 當場翻覆沉沒。這不是神秘消失，是一群人為了量一座火山，被它吞了下去。 | H；K：「直ちに転覆沈没」；Skeptoid：9 名科學家＋22 名船員為觀測火山 | 確認 |
| t099 | 那魔鬼海這個名字哪裡來的？目前找得到最早的，是一九七一年美國一本超自… | K：Skeptoid：Sanderson 1971 年 4 月在其研究會會刊 Pursuit 寫 “vile vortices”（12 個漩渦），1972 年 Saga 轉載為 “The Twelve Devil's Graveyards”；Skeptoid 說 Berlitz 從 vile vortices 得到 Devil's Sea 的靈感，並說找不到 Berlitz 與 Sanderson 之前的用例。沒有寫明 1971 年那篇用了「魔鬼海」這個名字，而且只有 Skeptoid 一家；寫成「這個名字最早是一九七一年」超出來源 | 需改 |
| t100 | 後來有研究者去翻失蹤名單，發現大多是小漁船，比例跟日本周邊其他海域差… | K：Kusche（Skeptical Inquirer）：Berlitz 說是軍艦的其實是漁船，損失率跟日本周邊漁船一向的損失率相同。來源沒寫「小」，也沒寫「大多」以外的比例細節 | 確認（建議微調） |
| t102 | 原因不明，只是說證據不夠下結論；它從來沒有說，是海把人帶走的。 | S：詮釋句；“reasons or causes unknown” | 確認 |
| t103 | 我們真正不知道的，只有剛剛那個七點零四分之後，那些年輕人在海上經歷了… | S：Smithsonian 結尾列出兩個真正解不開的謎：Taylor 一開始為什麼偏離航線，以及 19:04 之後發生什麼。旁白說「只有」七點零四分之後，漏了第一個 | 需改 |
| t105 | 問你一題：如果你是那天的 Cox，長官說不准飛，你會照命令留在地上，… | S：Cox 要求開待命飛機被拒（t039–t040） | 確認 |

沒列進表的行（t002、t004、t009、t010、t014、t030、t038、t044、t055、t064、t068、t080、t087、t088、t101、t104、t106、t107）是提問、轉場或旁白感想，沒有可查的事實主張。
