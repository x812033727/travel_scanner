# curio-s34-v2 重排：10 步對照表

依據 `scratchpad/heimao/STRUCTURE.md` 的共通模板與 `scratchpad/redo/RULES.md`。lint 估總長 13.7 分鐘（原片 13.2 分鐘）；
下表的秒數用 250 字／分加句間、換景停頓自估（全長約 13:00），比 lint 略短，比例照看即可。

| 步 | 名稱 | 開始 | 秒數 | 占比 | scene id |
|---|---|---|---|---|---|
| 1 | 鉤子 | 0:00 | 44 | 5.7% | open-ad、open-who、open-stakes、open-versions、open-book、open-boat、open-deep |
| 2 | 承諾句 | 0:44 | 11 | 1.4% | open-promise、open-question |
| 3 | 時代與起源 | 0:55 | 114 | 14.6% | origin-london、origin-letters、origin-pick-you、origin-teams、origin-worsley、origin-dream、origin-dream-ada、origin-door、origin-engaged、origin-no-ad、origin-quay、origin-refused、origin-stowaway、origin-plead、origin-plead-ada、origin-youngest、origin-anchor、origin-last-link、origin-horizon |
| 4 | 第一次起落 | 2:49 | 124 | 15.9% | ice-close、ice-dream-true、ice-beset、ice-281、ice-crushed、ice-abandon、ice-crank、camp-film、camp-mast、camp-two-pounds、camp-bottle-you、camp-coins、camp-coins-ada、camp-bible、camp-plates、camp-ocean、camp-tent、camp-shout、camp-sinks、camp-records、camp-records-ada |
| 5 | 升級關卡 | 4:53 | 131 | 16.8% | floe-where、floe-hut、floe-640、floe-patience、floe-never、floe-launch、floe-caird、floe-island、land-callback、land-answer、land-who、land-jump、land-sat、land-pebbles、land-pebbles-ada、land-empty、land-you、land-upturned、land-decides、land-800、land-crazy-ada |
| 6 | 最大危機 | 7:05 | 91 | 11.7% | caird-depart、caird-left、caird-clock、caird-sun、caird-kneel、caird-clouds、caird-four-ada、caird-you、caird-white、caird-wave、caird-hold、caird-breath-ada、caird-cliffs、caird-storm、caird-landing |
| 7 | 翻身與揭曉 | 8:36 | 152 | 19.4% | cross-other、cross-31、cross-nobody、cross-q-ada、cross-set-off、cross-36、cross-first、cross-station、cross-voice、cross-name、cross-war、cross-war-ada、cross-waiting、rescue-first、rescue-trawler、rescue-worry-ada、rescue-yelcho、rescue-promise、rescue-spots、rescue-call、rescue-well、rescue-aboard、rescue-all-ada、rescue-634 |
| 8 | 尾聲：故事還沒結束 | 11:07 | 56 | 7.1% | epi-other-ada、epi-ross、epi-wreck-q、deep-icebreaker、deep-found、deep-centenary、deep-position-ada、deep-dart、deep-stern、deep-star |
| 9 | 主題收束 | 12:03 | 41 | 5.3% | close-ad-ada、close-legend、close-records-ada、close-shelf、close-line、close-you |
| 10 | 提問與訂閱 | 12:44 | 14 | 1.8% | close-outro、close-subscribe |

模板建議比例：鉤子 3–5%、承諾 1–2%、起源 8–20%、第一次起落 10–15%、升級關卡 25–35%、最大危機 8–12%、翻身 8–12%、尾聲 8–12%、收束 6–8%、CTA 1.5–2.5%。
步 4、5 加起來 33%，等於模板的「第一次起落＋升級關卡」上緣；步 7 偏長（19%），因為翻山和救援兩段都在這裡，見 changes.md〈要站主決定的事〉。

## 章節

| 章 | 步 | lint 估的開始 |
|---|---|---|
| 一則人人會背的廣告 | 1–2 | 00:00 |
| 一九一四年，倫敦一扇門上的牌子 | 3 | 00:58 |
| 冰在一夜之間把船圍住 | 4 | 02:57 |
| 金幣丟掉，照片留下 | 4 | 03:40 |
| 浮冰上的五個半月，象島上沒有別人 | 5 | 05:08 |
| 凱爾德號的十六天，只量到四次太陽 | 6 | 07:26 |
| 三十六小時翻過山，站長只認得他的聲音 | 7 | 09:02 |
| 試了三次，第四次耶爾喬號開到了象島 | 7 | 10:25 |
| 二〇二二年，三千零八公尺深的海底 | 8 | 11:56 |
| 廣告找不到，紀錄都在 | 9–10 | 12:40 |

## 原本每一段搬到哪裡

| 原段落（原 scene id） | 新位置 | 怎麼改 |
|---|---|---|
| 開場 open-you、open-stakes | 步 1 open-ad、open-who、open-stakes | 保留「你一定聽過這則廣告」；新加 open-who 一句說清楚這是誰、為了什麼登的（探險家薛克頓招人去南極），沒聽過的人才知道在講什麼 |
| 開場 open-dream、open-sign（一九一四年倫敦、夢、門上的牌子、「你錄取了」） | 步 3 origin-worsley、origin-dream、origin-door、origin-engaged | 這是原片開場的濃縮劇情：從鉤子拿掉，搬回它的年代，先介紹沃斯利是誰再講夢 |
| 開場 open-no-ad（書裡廣告在哪一頁） | 步 1 open-book ＋ 步 3 origin-no-ad | 鉤子只說「書裡根本沒提到這則廣告」當怪點；沃斯利怎麼來的放到起源再收 |
| 開場 tease-boat、tease-deep | 步 1 open-boat、open-deep | 留作兩個高潮標籤（小木船只靠太陽、一個世紀後有人回去找），不講中間怎麼走到那裡 |
| 開場 open-promise（big 卡，634 天） | 步 2 open-promise、open-question | 改成承諾句「今天我們就來聊聊」加兩個全片問題；「634 天」挪到 rescue-634 才揭曉 |
| 第 2 章 letters、letters-card、pick-you | 步 3 origin-letters、origin-pick-you、origin-teams | 卡片改插圖；「一頁都沒有」的回答已在鉤子用掉，所以從「他自己寫：收到將近五千封」開始 |
| 第 2 章 buenos-aires … youngest | 步 3 origin-quay … origin-youngest | 照原順序；「我讀到這裡忍不住笑」縮成 Ada 一句 |
| 第 2 章 anchor、last-link、horizon | 步 3 origin-anchor、origin-last-link、origin-horizon | 「下一次踩到陸地」加「先記住這個問題」，在象島收 |
| 第 2 章 closing-ice … abandon、tease-crank | 步 4 ice-close … ice-crank | 新加 ice-dream-true：沃斯利夢裡的冰塊真的圍上來（收起源的夢） |
| 第 3 章 photographer … records | 步 4 camp-film … camp-records-ada | 卡片改插圖；「兩磅」改成問觀眾會帶什麼 |
| 第 3 章 calculates … open-water | 步 5 floe-where … floe-island | paulet-card 改成插圖加問句 |
| 第 4 章 nights-on-floe … voyage-card | 步 5 land-callback … land-crazy-ada | 「開頭問過」改成「還記得起錨那天的問題嗎？」（埋梗改在起錨，不在開場） |
| 第 5 章 departure … no-one-went | 步 6 caird-depart … caird-landing ＋ 步 7 cross-other … cross-q-ada | four-card、landing-card 改插圖 |
| 第 6 章 set-off … still-waiting | 步 7 cross-set-off … cross-waiting | crossing-card 改插圖 |
| 第 7 章 attempts-card … all-card | 步 7 rescue-first … rescue-634 | 二、三次救援併一句 |
| 第 7 章 other-party、logbook-shelf | 步 8 epi-other-ada、epi-ross、epi-wreck-q | 「故事還沒結束」：另一隊、沉船 |
| 第 8 章 icebreaker … star | 步 8 deep-icebreaker … deep-star | depth-card 改插圖；「發現團隊說」併進 deep-dart |
| 第 8 章 ad-again、answer、file-stamped | 步 9 close-ad-ada … close-you | 新加 close-shelf（夢、牌子、底片、位置倒帶串回）與 close-line（一句金句） |
| outro 卡 | 步 10 close-outro、close-subscribe | 改成兩張 Ada 插圖；「這份檔案，存檔」移到這裡 |

刪掉的景見 changes.md〈為了長度刪掉的〉。

## 鉤子、起源、轉折、收尾怎麼排

- **鉤子（步 1）**：情境「你一定聽過這則廣告」→ 說清楚是誰、去哪（探險家薛克頓招人去南極）→ 利害（二十八個人困冰快兩年）→ 「可是你想不到」翻反差（流傳的文字不只一個版本、他自己的書裡沒提到）→ 兩個高潮標籤（小木船只靠太陽、一個世紀後回去找船）。不先講招募、困冰、象島、救援的順序。
- **承諾（步 2）**：「今天我們就來聊聊」，給全片的兩個問題：廣告在哪裡、回來了幾個。
- **起源（步 3）**：「故事要回到一九一四年初的倫敦」→ 五千封信 → 五十六人兩隊 → 沃斯利的夢與門牌（不是廣告）→ 偷渡少年 → 起錨。一路照時間走，不跳主角：主角是這一船人，薛克頓、沃斯利、布雷克伯勒在需要時才各用一句話介紹。
- **轉折**：每 40–60 秒一個問句或「但這還不是最危險的」「問題來了」；大起落是困冰→沉船（步 4）、寶萊島走不到→象島（步 5）、只量到四次太陽與巨浪（步 6）、翻山與三次救援失敗→耶爾喬號（步 7）。
- **收尾（步 8–10）**：「全部」只算堅忍號（另一隊）→ 二〇二二年找到沉船 → 回到開場的廣告 → 倒帶串回四個代表物 → 一句金句 → 問觀眾要上小艇還是留在島上、訂閱。

## 埋梗與回收（loops）

| 埋 | 收 | 內容 |
|---|---|---|
| e001（open-ad） | e125（close-legend） | 人人會背的那則廣告 |
| e003（open-stakes） | e113（rescue-634） | 困在冰裡的快兩年到底多久 |
| e004（open-versions） | e125（close-legend） | 流傳的文字不只一個版本：原件在哪裡 |
| e005（open-book） | e019（origin-no-ad） | 薛克頓的書裡沒有廣告，那人是怎麼來的 |
| e006（open-boat） | e080（caird-four-ada） | 只靠太陽指路 |
| e007（open-deep） | e117（deep-icebreaker） | 開破冰船回去找它 |
| e008（open-promise） | e125（close-legend） | 那則廣告到底在哪裡 |
| e009（open-question） | e112（rescue-all-ada） | 這一船人回來了幾個 |
| e012（origin-pick-you） | e013（origin-teams） | 從五千封信裡挑誰 |
| e016（origin-dream-ada） | e030（ice-dream-true） | 塞滿冰塊的夢有多準 |
| e020（origin-quay） | e021（origin-refused） | 求工作的年輕人會不會被收 |
| e024（origin-plead-ada） | e025（origin-youngest） | 薛克頓收不收偷渡的少年 |
| e028（origin-horizon） | e061（land-answer） | 下一次踩到陸地是什麼時候 |
| e031（ice-beset） | e032（ice-281） | 船會被卡多久 |
| e036（ice-crank） | e037（camp-film） | 冰上轉把手的人在做什麼 |
| e046（camp-ocean） | e049（camp-sinks） | 船還會撐多久 |
| e051（camp-records-ada） | e121（deep-dart） | 沃斯利記下的沉船位置 |
| e054（floe-640） | e056（floe-never） | 走得到寶萊島嗎 |
| e062（land-who） | e064（land-jump） | 誰先上象島 |
| e069（land-you） | e071（land-decides） | 下一步怎麼做 |
| e085（caird-breath-ada） | e086（caird-cliffs） | 巨浪撐得過去嗎 |
| e092（cross-q-ada） | e095（cross-first） | 沒人走過的山翻得過去嗎 |
| e105（rescue-worry-ada） | e110（rescue-well） | 島上的人撐得到嗎 |
| e107（rescue-promise） | e108（rescue-spots） | 冰會讓開嗎 |
| e114（epi-other-ada） | e115（epi-ross） | 另一隊呢 |
| e116（epi-wreck-q） | e117（deep-icebreaker） | 沉船還找得到嗎 |
| e120（deep-position-ada） | e121（deep-dart） | 位置準不準 |

## 人物與代表物（歷史人物不入畫）

| 人物 | 畫面上用什麼代表 | 第一次出現 |
|---|---|---|
| 薛克頓 | 灰色毛線帽（grey knitted wool hat） | open-who |
| 沃斯利 | 黃銅六分儀 | origin-worsley |
| 布雷克伯勒 | 一雙小小的舊皮靴 | origin-quay |
| 赫利 | 三腳架上的木頭手搖攝影機 | ice-crank（只畫手）、camp-film |
| 懷爾德、克林、站長、其他隊員 | 不入畫；用倒扣的小艇、靴印、手套、半開的門 | — |
| 堅忍號 | 木造三桅帆船（沒有名字、沒有字） | open-stakes |

解說員 Ada（`researcher`）24 景，只用在「我」的反應、轉折、承諾與提問；她不演任何歷史人物。「你」的 6 景畫一般卡通人（年輕男女）。手的 7 景只畫戴手套的手。
