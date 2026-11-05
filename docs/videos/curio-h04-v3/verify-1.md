# curio-h04-v3 查核第一輪

- 範圍：`video.json` 全部 `lines[].text`（t001–t144）、卡片 `data`、`youtube.title`、`youtube.description`、`thumbnail.data`、132 個景的插圖提示詞，對照 `claims.md`。查核者沒有參與撰稿。`t090`、`t091` 協調者已決定刪除，不查。
- 日期：2026-10-31。來源都是當天重開（User-Agent 只用編輯用的那一個）。1959 年文件逐字引（俄文，資料站的轉錄，掃描沒有逐頁比對）；CC 授權的論文與校方稿短引；《紐約客》《國家地理》《生意人報》《國際文傳電訊》、BBC、《自由新聞》一律轉述。
- 判定只有 CONFIRMED、CHANGED、NOT FOUND、OUT OF SCOPE；CHANGED 與 NOT FOUND 在判定欄寫行 id 與建議改法，「低」表示可改可不改。信心：✅ 一手或多來源；△ 單一來源或轉述；⚠ 來源本身可疑或互相矛盾。
- **撰稿者的疑點，結論先講**：
  - 帳篷去向（t132–t138）：撰稿者只找到兩個出處，我多找到第三個，而且早於《紐約客》：《自由新聞》（Свободная Пресса）2019-03-01 訪問 1978 年進那間實驗室工作的鑑定人安庫季諾夫。他說的時間跟資料站不同：主任過世後、1980 年代前半地下室淹水，帳篷才發霉被丟。他自己沒說親眼看到丟棄，也主張火箭說，所以「據說」要留；但 `t134` 的「七〇年代末」與 `t137` 的「只查到這兩個出處」都要改。三者是否同源查不到：《紐約客》與資料站都沒有引註。
  - `t004`「他一按，它亮了」：確實是斯洛布佐夫的證詞，但旁白沒有點名是誰說的（`claims.md` 寫有點名，不對），另兩份證詞不同。要加歸屬。
  - 標題「9 人從裡面割開帳篷」強過紀錄：鑑定書只說切口從裡面割，沒說是誰、幾個人，`t058` 自己也這樣講。要改。
  - 2019 檢方與 2021 模型：歸屬與反對意見都有標（t075–t089、t102–t119），唯一例外是 `t106` 的因果寫成確定，片尾 `t142` 與結尾卡的「雪崩說得通」沒有寫是誰說的。
  - 真實人物與遺體：沒有提示詞寫名字、長相或遺體傷勢；但有 `frozen-b`、`temp-8`、`open-lit`、`items-out`、`turn` 幾景其實是在畫旁白正在講的那個人或那九人之一，見下方提示詞列。
- `claims.md` 要順手更正的一處：#15 與〈記錄互相對不上〉寫 2-28 筆錄是「9 雙氈靴」，原文是 `9 пар ботинок`（靴子）與 `валенки три пары`（氈靴 3 雙）。

## 逐項查核

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | `youtube.title`：「9 人從裡面割開帳篷，真的是雪崩嗎？」 | CHANGED：鑑定書只回答切口方向，沒有回答誰割、幾人動手（t058 自己這樣說）。建議「佳特洛夫事件：9 人離開的帳篷，切口從裡面割開，真的是雪崩嗎？」或「…帳篷從裡面被割開，真的是雪崩嗎？」 | 「Все указанные разрезы нанесены с внутренней стороны из палатки」；結案書也只寫 `оказалась разрезана изнутри` | 第 199 號鑑定書；結案書 | https://dyatlovpass.com/case-files-303-304-ru ；https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 2 | `youtube.description`：「他後來受到懲戒的報導」 | CHANGED：t090–t091 已刪，說明欄這句要一起刪，只留「以及家屬的反對」。景 `reprimand`、`resign` 一併刪；`sources` 裡只為這段而列的 Коммерсантъ-Урал 2020-08-16、Коммерсантъ 2020-11-02 可拿掉 | 協調者決定，不查內容 | — | — | ✅ |
| 3 | `youtube.description`：「九個人赤腳狂奔」是流傳的版本，案卷不是這樣寫的 | CHANGED：旁白根本沒講這個說法，而且案卷有一半是這樣：索格林作證寫「逃跑」，結案書寫有人近乎赤腳。建議刪掉這五個字，只留「未知的力量」 | 「группа бежала из палатки」；「почти босой ногой оставлены」 | 索格林證詞；結案書 | https://dyatlovpass.com/case-files-330-339-ru ；https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 4 | `youtube.description`：帳篷被丟棄「只查到《紐約客》與一個愛好者資料站兩個出處」 | CHANGED：現在有第三個，見 #99。建議「帳篷被丟棄一事只有《紐約客》、一個愛好者資料站與一位前實驗室人員的受訪說法，沒有公文，時間也對不上」 | 見 #99 | 《自由新聞》2019-03-01 | https://web.archive.org/web/2021/https://svpressa.ru/politic/article/226183/ | △ |
| 5 | `youtube.description`：「二月二十六日下午」 | CHANGED（低）：案卷只寫白天（днем），列別傑夫的證詞甚至把發現寫在前一天傍晚之前。建議「二月二十六日」或「白天」 | 「днем 26 февраля 1959 года」 | 斯洛布佐夫證詞 | https://dyatlovpass.com/case-files-298-300-ru | ✅ |
| 6 | `thumbnail`：「從裡面 割開」「1959，9 人走進雪夜」 | CONFIRMED：割開方向有鑑定書；「雪夜」是推定：鑑定命令寫傍晚、論文寫午夜之後，當晚沒有任何紀錄 | 「Вечером 1 февраля 1959 года」；「after midnight」 | 指派鑑定的決定；Gaume & Puzrin 2021 | https://dyatlovpass.com/case-files-301-302-ru ；https://www.nature.com/articles/s43247-020-00081-8 | △ |
| 7 | t001 零下二十五度以下 | CONFIRMED | 「below −25 °C」；結案書「порядка 25-30°С」 | Gaume & Puzrin 2021；結案書 | https://www.nature.com/articles/s43247-020-00081-8 ；https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 8 | t002 九人沒有回來；檢方數出七十五種說法 | CONFIRMED | 發言人說從 75 種版本裡查 3 種（轉述） | 《國際文傳電訊》2019-02-05 | https://www.interfax.ru/russia/649229 | ✅ |
| 9 | t003 二月二十六日，學生領隊看見帳篷 | CONFIRMED：另有異文：列別傑夫的證詞把這件事放在 25 日，BBC 訪問的沙拉文說是他先看到；結案書與斯洛布佐夫都寫 26 日，旁白可不改 | 「Палатка группы Дятлова была обнаружена нашей группой днем 26 февраля」；「вход палатки выступал из под снега」 | 斯洛布佐夫證詞；結案書；列別傑夫證詞 | https://dyatlovpass.com/case-files-298-300-ru ；https://dyatlovpass.com/case-files-313-315-ru | ✅ |
| 10 | t004 手電筒底下有雪、上面沒有；他一按，它亮了 | CHANGED：內容是斯洛布佐夫的證詞，但旁白寫成事實，沒有點名（`claims.md` 標「旁白點名」不符）；馬斯連尼科夫寫開著卻不亮，坦帕洛夫寫沒點亮。建議 `t004`：「帳篷上躺著一支手電筒，底下有雪，上面沒有；他作證說，他一按，它亮了。」 | 「обнаружил, что он не был включен. Когда включил я, то зажегся」；另見「в зажженном состоянии (но не горел)」「в незажженном состоянии」 | 斯洛布佐夫、馬斯連尼科夫、坦帕洛夫證詞 | https://dyatlovpass.com/case-files-298-300-ru ；https://dyatlovpass.com/case-files-62-75-ru ；https://dyatlovpass.com/case-files-309-312-ru | ⚠ |
| 11 | t005 挖開沒有人，鞋幾乎都在 | CONFIRMED | 「убедились, что людей нет」；「почти вся обувь」 | 斯洛布佐夫證詞；結案書 | https://dyatlovpass.com/case-files-298-300-ru ；https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 12 | t006 四月，一位鑑定人把它重新搭起來，只問兩個問題 | CHANGED（低）：問題是調查員出的，鑑定人是回答的人。建議「只要回答兩個問題」 | 「На разрешение экспертизы поставлены вопросы」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 13 | t008、卡片 `open-promise` 帳篷長 4.33 公尺 | CONFIRMED | 「по конку/ равна 4м.33см」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 14 | t009 九個訓練有素的人 | CONFIRMED | 「имели хорошую туристскую подготовку」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 15 | t010 帶隊學生斯洛布佐夫；帳篷在山上二十五天 | CONFIRMED：2 月 1 日到 26 日，25 天無誤 | 「Я руководил поисковой группой」 | 斯洛布佐夫證詞 | https://dyatlovpass.com/case-files-298-300-ru | ✅ |
| 16 | t011 隔天起拿出九個背包、八雙靴子、七隻氈靴 | CONFIRMED：兩份證詞一致；但 2-28 現場筆錄是靴子 9 雙、氈靴 3 雙（`claims.md` 誤記，見開頭）。旁白可不改 | 「9 рюкзаков…8 пар ботинок, 3,5 пары валенок (7 шт.)」；筆錄「9 пар ботинок…валенки три пары」 | 馬斯連尼科夫、坦帕洛夫證詞；營地發現筆錄 | https://dyatlovpass.com/case-files-62-75-ru ；https://dyatlovpass.com/case-files-309-312-ru ；https://dyatlovpass.com/case-files-2-ru | ✅ |
| 17 | t012 口袋約八百盧布，所以不像搶劫 | CONFIRMED：推論跟結案書一致 | 「деньги примерно 800 руб.」；「наличие всех ценностей группы」 | 斯洛布佐夫證詞；結案書 | https://dyatlovpass.com/case-files-298-300-ru ；https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 18 | t013 切好的肥肉；爐子在袋子裡，管子沒拿出來 | CONFIRMED | 「нарезанного сала」；「в чехле лежала печка. Трубы последней находились внутри печки」 | 坦帕洛夫、列別傑夫證詞 | https://dyatlovpass.com/case-files-309-312-ru ；https://dyatlovpass.com/case-files-313-315-ru | ✅ |
| 19 | t015–t017 最後一張是挖雪；1/25 秒、光圈 5.6；約傍晚五點 | CONFIRMED | 「с выдержкой I/25 сек., при диафрагме 5,6」；「около 5 часов вечера」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 20 | t018 五點之後沒有紀錄和照片 | CONFIRMED | 「ни одной записи и ни одного фотоснимка не было обнаружено」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 21 | t019–t021 案卷抄著傳單，2 月 1 日；爐子紀錄 1:02:27.4；雪人 | CONFIRMED：只有日期，沒有時刻；緊接 t018 不要讓人以為它寫於五點之後，現在的字句沒有這樣說 | 「1 час 02 мин. 27, 4 сек」；「снежные человеки обитают на Северном Урале」 | 傳單抄本 | https://dyatlovpass.com/case-files-31-ru | ✅ |
| 22 | t022 十人出發，尤丁一月二十八日生病折返 | CONFIRMED | 「в количестве 10 человек」；「не смог из-за болезни продолжать」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 23 | t023 三月初認東西；毛背心是他的，折返那天交給隊友 | CONFIRMED：筆錄日期 3 月 5–7 日 | 「этот жилет принадлежит ему и 28/I-59 г. передан им」 | 物品指認筆錄 | https://dyatlovpass.com/case-files-11-20-ru | ✅ |
| 24 | t025 八到九組腳印，往山谷和森林 | CONFIRMED | 「их насчитывалось 8-9 пар」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 25 | t026–t027 腳印凸起，旁邊的雪被風吹走 | CONFIRMED：「小雪柱」是旁白的比喻，我開的文件只寫凸出雪面 | 「Следы выступали над окружающей поверхностью снега, ибо около следов снег ветром был выдут」 | 斯洛布佐夫證詞 | https://dyatlovpass.com/case-files-298-300-ru | ✅ |
| 26 | t028 近乎赤腳、一隻棉襪；氈靴印 | CONFIRMED | 「почти босой ногой оставлены (например, в одном х/б. носке)」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 27 | t029 坦帕洛夫只認到八組，寫正常步伐 | CONFIRMED：譯名提醒：俄文 Темпалов，「坦」偏離發音，聽檢可考慮「田帕洛夫」 | 「Девятого следа установить мне не удалось」；「люди шли нормальным шагом」 | 坦帕洛夫證詞 | https://dyatlovpass.com/case-files-309-312-ru | ✅ |
| 28 | t031 同一批搜救者裡的「登山老手」說他們是逃跑的 | CHANGED：說「逃跑」的是索格林，1937 年生、作證時還是大四學生，當時帶自己的一隊。建議 `t031`：「可是同一批搜救者裡，另一隊的學生領隊看了腳印說，他們是逃跑的。」 | 「Год рождеия 1937」；「Учится на 4 курсе」；「группа бежала из палатки」 | 索格林證詞 | https://dyatlovpass.com/case-files-330-339-ru | ✅ |
| 29 | t033 一公里半，林線邊的火 | CONFIRMED | 「в 1500 метрах от палатки, у границы леса, обнаружены остатки костра」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 30 | t034 接下來一週多找到五個人 | CHANGED（低）：來源是隔天四人、一週後第五人，共約一週，`claims.md` 自己也寫「約一週」。建議「接下來大約一週」 | 第五人在一週後（轉述） | 《生意人報》2024-02-03 | https://www.kommersant.ru/doc/6480697 | △ |
| 31 | t035 檢察官的猜測，標明個人意見 | CONFIRMED | 「Это мое личное мнение」 | 坦帕洛夫證詞 | https://dyatlovpass.com/case-files-309-312-ru | ✅ |
| 32 | t036 有人被風颳走喊了一聲，其他人衝出去「救」 | CHANGED：原文是其他人嚇到衝出去，也被風颳走，沒有「救」。`claims.md` #37 也要改。建議 `t036`：「有人出帳篷被風颳走，喊了一聲，其他人嚇得衝出去，也被風颳走，全回不去了。」 | 「этот человек поднял крик. Студенты испугались, бросились из палатки и так же ветром были унесены」 | 坦帕洛夫證詞 | https://dyatlovpass.com/case-files-309-312-ru | ✅ |
| 33 | t037 條件：另外四人也是凍死才成立 | CONFIRMED | 「Если и у этих 4 студентов причиной смерти будет замерзание, то вышеуказанная версия будет правильная」 | 坦帕洛夫證詞 | https://dyatlovpass.com/case-files-309-312-ru | ✅ |
| 34 | t038 帶過隊長的老手猜：有人出去方便，嚇得手電筒掉了 | CONFIRMED：阿克塞爾羅德 1958 年帶過佳特洛夫的三級隊。原文是「驚訝」，譯成「嚇得」可接受 | 「один из вышедших помочиться товарищей, от удивления выронивший фонарик」 | 阿克塞爾羅德證詞 | https://dyatlovpass.com/case-files-316-329-ru | ✅ |
| 35 | t040–t041 三月十六日命令：有理由相信帳篷被某人割過 | CONFIRMED | 「есть основания полагать, что палатка была кем-то разрезана」 | 指派鑑定的決定 | https://dyatlovpass.com/case-files-301-302-ru | ✅ |
| 36 | t042 一開始追謀殺；曼西獵人被問話、被拘留 | CONFIRMED：旁白點名《生意人報》 | 他立刻提出謀殺版本；幾位曼西人受懷疑、被問話甚至被拘留（轉述） | 《生意人報》2024-02-03 | https://www.kommersant.ru/doc/6480697 | △ |
| 37 | t044 學生用冰斧挖；破口可能是自己人弄的 | CONFIRMED | 「может быть её порвали наши ребята」 | 列別傑夫證詞 | https://dyatlovpass.com/case-files-313-315-ru | ✅ |
| 38 | t045 拖六七百公尺，裝上直升機 | CONFIRMED | 「волоком перетащили к вертолетной площадке на расстояние метров 600-700」；直升機運走（轉述） | 馬斯連尼科夫證詞；《紐約客》 | https://dyatlovpass.com/case-files-62-75-ru ；https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | ✅ |
| 39 | t046 四月三日送到，皺成一團 | CONFIRMED | 「3 апреля 1959г.」；「в беспорядочно-скомканном виде」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 40 | t047–t048 丘爾金娜先把它搭起來，尤丁幫忙 | CONFIRMED | 「при помощи и консултации туриста Юдина Ю. была натянута」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 41 | t049 帳篷相當舊 | CONFIRMED | 「Палатка доволно поношена」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 42 | t050、卡片 `two-q` 兩個問題 | CONFIRMED | 「Имеются ли разрезы…сделанные ли они с внутренней стороны или с наружной?」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 43 | t051–t052 撕順著線，割斜斷兩種線 | CONFIRMED | 「рвутся либо нити утка, либо нити основы」；「нарушает как те, так и другие нити под различными углами」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 44 | t053、卡片 `three` 三道約 32、89、42 公分，其他撕裂 | CONFIRMED：「大約」用對了，第 2、3 道邊緣布片缺失，鑑定書說可能更長 | 「примерно 32, 89, и 42 см」；「Все же остальные повреждения являются разрывами」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 45 | t054 最高五十六倍 | CONFIRMED | 「увеличение с 0,6 до 56Х」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 46 | t055 內面刺孔角上有細刮痕，外面沒有 | CONFIRMED | 「В углах проколов с внутренней стороны палатки /в отличие от наружной/」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 47 | t056、卡片 `verdict` 全部從裡面割的 | CONFIRMED | 「Все указанные разрезы нанесены с внутренней стороны из палатки」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 48 | t057 「紀錄對不上」：《紐約客》寫裁縫 | CHANGED：裁縫的版本查到了，但這句說「對不上」卻只講一邊，另一邊被砍了；而且兩邊都是事後報導，不是紀錄。建議 `t057`：「偏偏是誰先看出來的，說法對不上：《紐約客》寫一位去警局量制服的裁縫，BBC 訪問的搜救學生則說，他當場就看出來了。」 | 《紐約客》：來試制服的女裁縫碰巧看出；BBC：沙拉文 80 多歲受訪，說當時就注意到（皆轉述） | 《紐約客》；BBC 2019 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved ；https://www.bbc.co.uk/news/extra/SoLiOdJyCK/mystery_of_dyatlov_pass | △ |
| 49 | t058 鑑定書只回答方向，不回答誰與為什麼 | CONFIRMED | 結論只有兩句，沒有提人 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 50 | t059 帳篷一頭有門 | CONFIRMED | 「имеется отверстие, служащее дверью」 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 51 | t060 五月四日，四公尺多深的雪底下 | CONFIRMED | 「4 мая 1959 г.…под слоем снега в 4-4,5 метрах」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 52 | t061 法醫：其中三人不是凍死的 | CONFIRMED：第四人科列瓦托夫是凍死，三個人數字正確 | 「Смерть Дубининой, Тибо-Бриньоль и Золотарева наступила в результате множественных телесных повреждений」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 53 | t062 五月二十八日伊凡諾夫簽四頁結案書 | CONFIRMED | 第 384–387 頁，頁碼 1–4 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 54 | t063 兩個錯：下午三點才爬；偏五六百公尺 | CONFIRMED | 「только в 15-00」；「на 500-600 м. левее」；「Это была вторая ошибка」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 55 | t064–t065、卡片 `force` 一股自然的力量 | CONFIRMED | 「причиной гибели туристов явилась стихийная сила, преодолеть которую туристы были не в состоянии」 | 結案書 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 56 | t066–t067 俄文沒有「未知」，有些英文轉述多出來 | CONFIRMED：俄文確實沒有；《國家地理》寫 unknown；校方稿另譯 compelling | 《國家地理》用 unknown natural force（轉述） | 結案書；《國家地理》 | https://dyatlovpass.com/case-files-384-387-ru ；https://www.nationalgeographic.com/science/article/has-science-solved-history-greatest-adventure-mystery-dyatlov | ✅ |
| 57 | t069 帳篷據說留在鑑識實驗室 | CONFIRMED：現在有兩個人講（資料站、《自由新聞》受訪者），「據說」要留。另有一處對不上：鑑定書送回檢方的公文附件列了物證，受訪者卻說檢方沒取回；旁白不必講，記入 `claims.md` | 「Приложение: акт экспертизы, 2 фототаблиц, вещ док.」 | 案卷第 302 頁；資料站；《自由新聞》 | https://dyatlovpass.com/case-files-301-302-ru ；https://dyatlovpass.com/controversy ；https://web.archive.org/web/2021/https://svpressa.ru/politic/article/226183/ | ⚠ |
| 58 | t070 一九九〇年退休的伊凡諾夫發表文章，說受壓，「他的新說法」是火球 | CHANGED（低）：他自己的說法是當年被壓著不准寫自己的看法，所以「新說法」跟他的主張相反。建議「…說當年有人施壓，不讓他寫自己的看法；他講的是火球。」 | 1990 年文章〈火球之謎〉；被施壓不寫自己的看法（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 59 | t071 簽自然力量與講火球的是同一人 | CONFIRMED | 見 #55、#58 | 結案書；《紐約客》 | https://dyatlovpass.com/case-files-384-387-ru | ✅ |
| 60 | t072 雪人變成一種說法，電視拍了整個節目 | CONFIRMED | 探索頻道節目 Russian Yeti: The Killer Lives（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 61 | t073 家屬和基金會認定武器試驗 | CONFIRMED | 《紐約客》：基金會主席堅持此說、家屬傾向；《生意人報》：家屬認定與軍方有關的人為災難（轉述） | 《紐約客》；《生意人報》2020-07-12 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved ；https://www.kommersant.ru/doc/4415422 | ✅ |
| 62 | t074 尤丁到 2013 年過世前都不信是自然 | CONFIRMED | 主張不是自然死亡，2013 年過世（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 63 | t075 二〇一九年二月：七十五種只查三種 | CONFIRMED | 2 月 1 日發言人：75 種裡查最可能的 3 種（轉述） | 《國際文傳電訊》2019-02-05 | https://www.interfax.ru/russia/649229 | ✅ |
| 64 | t076 三種全跟天氣有關：雪崩、雪板、颶風 | CHANGED（低）：三種名稱對；檢方的字眼是自然現象、自然因素，不是天氣，雪崩也不算天氣。建議「三種全是自然因素」 | 三個版本都與自然因素有關（轉述） | 《國際文傳電訊》2020-07-11 | https://www.interfax.ru/russia/716956 | ✅ |
| 65 | t077 發言人隔幾天澄清：不是重啟偵查 | CONFIRMED：另有異文：校方稿寫 reopened，旁白採檢方自己的說法，正確 | 2 月 5 日；一般監督檢查（轉述） | 《國際文傳電訊》2019-02-05 | https://www.interfax.ru/russia/649229 | ✅ |
| 66 | t078 三月上山定帳篷位置 | CONFIRMED | 計畫三月派檢察官上山定位置、坡度、雪深（轉述） | 《國際文傳電訊》2019-02-05 | https://www.interfax.ru/russia/649229 | ✅ |
| 67 | t079、卡片 `slope-card`：三十度；「老手」十五到十八度、沒有危險 | CHANGED：數字都對；「老手」與 #28 同一個人。建議 `t079`：「當年的現場筆錄寫三十度，三月上去看的學生領隊卻寫十五到十八度，還說這坡沒有危險。」卡片 `1959-03-04 登山老手` 改 `1959-03-04 搜救隊員證詞` | 「под уклоном горы 30°」；「Крутизна склона 15-18°」；「не представляет никакой опасности」 | 營地發現筆錄；索格林證詞 | https://dyatlovpass.com/case-files-2-ru ；https://dyatlovpass.com/case-files-330-339-ru | ✅ |
| 68 | t080 檢方算出二十三到二十六度 | CONFIRMED：這是檢方**重新定位後**那個點的坡度，離舊位置數百英尺；t078 已交代要重定位置，卡片「同一片坡」可接受 | 新位置坡度 23 到 26 度（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 69 | t082 二〇二〇年七月十一日，副主管庫里亞科夫說是雪崩 | CONFIRMED | 檢察總署烏拉爾聯邦區局副局長，向記者宣布（轉述） | 《國際文傳電訊》2020-07-11 | https://www.interfax.ru/russia/716956 | ✅ |
| 70 | t083–t084 照他的說法：沒有驚慌、五十公尺石脊、能見度最多十六公尺 | CONFIRMED：有標「照他的說法」 | 一起、不慌、50 公尺、石脊；能見度 6 到 16 公尺（轉述） | 《國際文傳電訊》2020-07-11 | https://www.interfax.ru/russia/716956 | ✅ |
| 71 | t086–t087 蒙眼一男一女，三十公尺，很快走偏 | CONFIRMED：《紐約客》寫 90 英尺，相同 | 他的話見《國際文傳電訊》；走偏見《紐約客》（轉述） | 《國際文傳電訊》2020-07-11；《紐約客》 | https://www.interfax.ru/russia/716956 ；https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | ✅ |
| 72 | t089 宣布到此為止；家屬的律師不接受，主張人為災難 | CONFIRMED：《生意人報》稱基金會的律師，RIA 稱他代表家屬，兩說都通 | 律師說不同意；親屬堅持人為災難（轉述） | 《生意人報》2020-07-12；RIA 2024-02-02 | https://www.kommersant.ru/doc/4415422 ；https://ria.ru/20240202/gruppa_dyatlova-1924548349.html | ✅ |
| 73 | t092 到《紐約客》刊出時檢方沒有正式報告 | CONFIRMED：有點名出處 | 總檢察署沒有發布正式報告（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 74 | t092 「之後有沒有，我查不到」 | NOT FOUND：我也沒查到 2021 年 5 月之後的正式報告；偵查委員會 2025 年會刊一篇（pressa.sledcom.ru）回 403，封存也沒有，UNOPENED。t092 照寫，不用改 | — | 網站搜尋 | https://pressa.sledcom.ru/ZHurnal/Magazine-1-2025/item/1962590/ | ⚠ |
| 75 | t094–t095 官方沒解釋怎麼發生：沒有痕跡；隔幾小時 | CONFIRMED | 「the authorities have not provided an explanation of how it happened」；「at least nine hours after the cut」 | EPFL 2021 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans | ✅ |
| 76 | t096–t097 電話打到洛桑，接的是高姆 | CHANGED（低）：2019 年 10 月初沒錯，但打的是他的手機，來源沒寫他人在哪裡。建議 `t097`：「那通電話其實更早：二〇一九年十月，打給洛桑聯邦理工的雪崩研究者高姆。」提示詞見 #111 | 「rang EPFL professor Johan Gaume’s cell phone」 | EPFL 2021 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans | ✅ |
| 77 | t098 沒聽過；黑板算式；找蘇黎世、俄國出生的普茲林 | CONFIRMED | 「had never heard of the case」；「equations and figures on my blackboard」；「Russian-born Puzrin」 | EPFL 2021 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans | ✅ |
| 78 | t099–t100 《國家地理》：幾年前跑過好萊塢，改《冰雪奇緣》程式 | CONFIRMED：有點名出處 | 幾年前；找做雪效的專家；改用該片的動畫程式（轉述） | 《國家地理》 | https://www.nationalgeographic.com/science/article/has-science-solved-history-greatest-adventure-mystery-dyatlov | △ |
| 79 | t102–t103 二〇二一年一月發表；搭帳切出平台 | CONFIRMED | 「the cut in the snow slab made by the group to install the tent」 | Gaume & Puzrin 2021 | https://www.nature.com/articles/s43247-020-00081-8 | ✅ |
| 80 | t104 無人機量到平均約二十度，階梯超過三十度 | CONFIRMED：這是作者自己的報告，t127 才講；論文 2021 另寫平均 23 度。可不改 | 「although the average slope angle is around 20°, locally steeper steps have indeed an inclination exceeding 30°」 | Puzrin & Gaume 2022 | https://www.nature.com/articles/s43247-022-00393-x | ✅ |
| 81 | t106 「那晚沒有新雪，可是強風一直把雪搬到帳篷上方」 | CHANGED：前半「他們假設」只罩到弱雪層，後面讀成確定；校方稿裡普茲林說的是 probably、could。而批評者也主張當晚沒有風（2022 Comment 自己列的反對意見）。建議 `t106`：「他們假設雪底下有一層弱雪；照他們的推算，那晚沒有新雪，強風可能一直把雪搬到帳篷上方，」 | 「The katabatic wind probably drifted the snow」；「there was no wind that night」（反對意見） | EPFL 2021；Puzrin & Gaume 2022 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans ；https://www.nature.com/articles/s43247-022-00393-x | ✅ |
| 82 | t107 約五公尺雪板 | CONFIRMED | 「The predicted length of 5.0 m」 | Gaume & Puzrin 2021 | https://www.nature.com/articles/s43247-020-00081-8 | ✅ |
| 83 | t108、卡片 `hours` 七個半到十三個半小時 | CONFIRMED | 「a delay of 7.5 to 13.5 h」，前提 realistic wind deposition flux；卡片已寫「模型算出」 | Gaume & Puzrin 2021 | https://www.nature.com/articles/s43247-020-00081-8 | ✅ |
| 84 | t109 照模型，雪板壓上，裡面的人割開帆布 | CONFIRMED：有標「照這個模型」與「我的比喻」 | 「cut the tent suddenly from the inside」；「impacted the hikers lying on the tent floor」 | Gaume & Puzrin 2021 | https://www.nature.com/articles/s43247-020-00081-8 | ✅ |
| 85 | t110–t111 美國雪崩專家推論只能往下坡側割 | CONFIRMED：有點名出處並寫「推論」，原文是條件句 | 科羅拉多雪崩資訊中心主任：如果雪板滑上帳篷（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 86 | t112 普茲林：沒有切那一刀就什麼事都沒有 | CONFIRMED：他下一句說單靠這個還不夠，引句未誤導 | 「If they hadn’t made a cut in the slope, nothing would have happened」 | EPFL 2021 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans | ✅ |
| 87 | t113 高姆：當時看不出危險 | CONFIRMED | 「the possibility of an avalanche was impossible to discern」 | EPFL 2022 | https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/ | ✅ |
| 88 | t114 論文用詞「說得通」；不處理離開帳篷之後 | CONFIRMED | 「shows the plausibility」；「we do not explain nor address…the behavior of the hikers after leaving the tent」 | Gaume & Puzrin 2021 | https://www.nature.com/articles/s43247-020-00081-8 | ✅ |
| 89 | t116 莫斯科記者：當地人沒見過這面坡雪崩 | CONFIRMED | 曼西人、遊客、雪車團主辦者都沒見過（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 90 | t117 《生意人報》：滑雪板還站著，爐子沒壓壞 | CONFIRMED | 照片裡帳篷兩端的滑雪板；容易變形的爐子沒壞（轉述） | 《生意人報》2024-02-03 | https://www.kommersant.ru/doc/6480697 | △ |
| 91 | t118 杜倫大學學者有點意外 | CONFIRMED | 小雪崩造成這種傷有點出人意料（轉述） | 《國家地理》 | https://www.nationalgeographic.com/science/article/has-science-solved-history-greatest-adventure-mystery-dyatlov | △ |
| 92 | t119 未參與的專家認為算式站得住 | CONFIRMED | 認為算式看來很穩健（轉述） | 《國家地理》 | https://www.nationalgeographic.com/science/article/has-science-solved-history-greatest-adventure-mystery-dyatlov | △ |
| 93 | t121 批評：這裡從沒有雪崩 | CONFIRMED：「最硬」是旁白的評價 | 「snow avalanches never happen in this area」 | Puzrin & Gaume 2022 | https://www.nature.com/articles/s43247-022-00393-x | ✅ |
| 94 | t122–t123 二〇二二年一月兩位職業嚮導；三百公斤的車連人翻倒好幾次 | CONFIRMED | 「two professional mountain guides」；「Several times, the 300 kg snowmobiles and their drivers were overturned」 | Puzrin & Gaume 2022 | https://www.nature.com/articles/s43247-022-00393-x | ✅ |
| 95 | t124 隔天，不到三公里，兩道雪板痕跡 | CONFIRMED：1 月 28 日出發、1 月 29 日觀察到 | 「the visibility briefly improved」；「<3 km away」；「traces of two new snow slab avalanches」 | Puzrin & Gaume 2022 | https://www.nature.com/articles/s43247-022-00393-x | ✅ |
| 96 | t125–t126 其中一道不到一小時幾乎看不見；作者說這就是搜救隊沒看到的原因 | CONFIRMED：有標「他們說」「作者說」 | 「practically invisible after less than an hour」；「could not find signs of an avalanche」 | Puzrin & Gaume 2022 | https://www.nature.com/articles/s43247-022-00393-x | ✅ |
| 97 | t127、卡片 `diff` 雪較軟、坡較陡、沒被切開、不同坡 | CONFIRMED | 「the slab was softer, the slope was steeper, it was not undercut from below」 | Puzrin & Gaume 2022 | https://www.nature.com/articles/s43247-022-00393-x | ✅ |
| 98 | t007、t132、t133、t138 據說被丟掉；《紐約客》發霉丟棄；大概沒有地方可以看 | CONFIRMED：都有「據說」「大概」或點名；《紐約客》這句沒有引註 | 存放後發霉，只好丟掉（轉述） | 《紐約客》 | https://www.newyorker.com/magazine/2021/05/17/has-an-old-soviet-mystery-at-last-been-solved | △ |
| 99 | t134–t135 資料站：主任留著，七〇年代末水管爆裂發霉；八〇年代他過世後進垃圾箱 | CHANGED：資料站確實這樣寫（用 apparently，無引註），但有第三個來源時間不同。前實驗室人員 2019 年受訪：主任過世後、1980 年代前半因公共管線事故地下室淹水，帳篷泡水發霉，跟其他損壞物品一起丟掉；他 1978 年入職，說自己沒去看過帳篷，只說有同事看過；他也主張火箭說。建議 `t134`：「專門整理案卷的網站寫：實驗室主任留著它，七〇年代末水管爆裂，帆布發霉，八〇年代他過世後進了垃圾箱。」`t135` 改：「可是一位七八年進那間實驗室的人受訪時說，是主任過世後地下室淹水，帳篷才發霉被丟。」 | 《自由新聞》受訪者安庫季諾夫（轉述）；資料站（轉述） | 《自由新聞》2019-03-01（現場回 403，用 Wayback 封存開）；dyatlovpass.com〈Controversy〉 | https://web.archive.org/web/2021/https://svpressa.ru/politic/article/226183/ ；https://dyatlovpass.com/controversy | ⚠ |
| 100 | t137 「我只查到這兩個出處，沒看到公文」 | CHANGED：出處是三個，時間對不上；同源與否查不到（可能共同來源是基金會主席，他也是《紐約客》的受訪者，這是我的推測；有部落客提到他講過類似的話並質疑他）。建議 `t137`：「我查到三個出處，時間對不上，也沒看到公文，請當成據說來聽。」 | 部落格：基金會主席說過帳篷因管線事故損毀（轉述，低可信） | foto-trip LiveJournal；同 #99 | https://foto-trip.livejournal.com/8202758.html | ⚠ |
| 101 | t137 丟棄的公文或一手紀錄 | NOT FOUND：俄文、英文各搜兩輪都沒有。旁白已說「沒看到公文」，照留 | — | 網站搜尋 | — | ⚠ |
| 102 | t139 「那三道切口，現在只剩鑑定書上的數字和幾張照片」 | CHANGED：前一句才說「大概」，這句又寫成確定，建立在「據說被丟」之上。建議 `t139`：「如果真是這樣，那三道切口就只剩鑑定書上的數字和幾張照片，我覺得這是最可惜的地方。」 | 照片編號 №1–13 附在鑑定書 | 第 199 號鑑定書 | https://dyatlovpass.com/case-files-303-304-ru | ✅ |
| 103 | t140 普茲林：沒有人真的知道 | CONFIRMED | 「no one really knows what happened that night」 | EPFL 2021 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans | ✅ |
| 104 | t142、卡片 `close-outro` 「雪崩說得通，還沒有定案」 | CHANGED：片尾把論文的用詞寫成旁白的結論，t116–t118 才列完反對意見。建議 `t142`：「論文說雪崩說得通，還沒有定案；紀錄留下的，是從裡面割開的帳篷和一路往下的腳印。」卡片 `title` 改「雪崩是一種說法，還沒有定案」 | 「shows the plausibility」；腳印與切口見 #24、#47 | Gaume & Puzrin 2021 | https://www.nature.com/articles/s43247-020-00081-8 | ✅ |
| 105 | t014、t024、t030、t032、t039、t043、t068、t081、t085、t088、t093、t101、t105、t115、t120、t128–t131、t136、t141、t143、t144 | OUT OF SCOPE：意見、問句與玩笑，都標得出是旁白自己的；t014 與 BBC 訪問沙拉文的印象相近 | — | — | — | — |
| 106 | t090、t091 | OUT OF SCOPE：協調者已決定刪除 | — | — | — | — |

## 插圖提示詞（132 景逐一看過）

規則：九位登山者不畫；在世或過世未滿 70 年的真實人物不畫本人；遺體與傷勢不畫。**沒有任何提示詞寫名字、描述長相，也沒有遺體或傷勢**（`five`、`may4`、`fire`、`cond-pay` 都只有搜救隊、火堆灰、筆）。名字出現的景多半只畫手或物件，例如 `yudin-vest`、`lab-yudin`、丘爾金娜的白袖口（`open-lab`、`lab-pitch`、`lab-worn`、`thread`、`scope`、`limit`）、伊凡諾夫（`order`、`sign`、`1990`）、高姆（`blackboard`），這些我判定可以。下面是例外。

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 107 | 景 `frozen-b`（t100）：背包訪客在片廠門口問路 | CHANGED：旁白正講高姆跑好萊塢，高姆在世，全身入畫就是畫他本人。建議改物件或無名檔案員：「Close-up of the archivist at her desk holding up a small snow globe, one eyebrow raised, desk lamp from the left」 | 見 #78 | 《國家地理》 | https://www.nationalgeographic.com/science/article/has-science-solved-history-greatest-adventure-mystery-dyatlov | ✅ |
| 108 | 景 `temp-8`（t029）、`open-lit`（t004）、`items-out`（t010） | CHANGED：旁白同時點名或用「他」指人，畫面是那個人的那個動作，遮了嘴也還是本人（坦帕洛夫、斯洛布佐夫都過世未滿 70 年）。建議只留手與物件：`temp-8` 改「a mitten counting small snow pillars with one raised finger」；`open-lit` 改「a gloved hand holding up a small lit flashlight」；`items-out` 改無名書記員，或只畫背包從帳篷被拿出來的手 | 坦帕洛夫 1921 年生；斯洛布佐夫 1939 年生 | 兩人證詞 | https://dyatlovpass.com/case-files-309-312-ru ；https://dyatlovpass.com/case-files-298-300-ru | △ |
| 109 | 景 `turn`（t084）：手套舉燈站在暴風雪裡；景 `rock`（t083）：石脊上有一盞燈 | CHANGED：這是庫里亞科夫重建的那一夜，那隻手就是九人之一，不能畫；燈是提示詞自己加的，我開的文件與他的說法都沒有提到。建議 `turn` 去人去燈：「Wide shot of driving snow at night in a thick blizzard, nothing visible beyond a few meters, a low dark ridge of rocks at the edge of frame, cold blue light, the only shapes are the snow and the rocks」；`rock` 刪 lantern | 外衣與鞋幾乎都留在帳篷：「почти вся обувь, вся верхняя одежда」 | 結案書；《國際文傳電訊》 | https://dyatlovpass.com/case-files-384-387-ru ；https://www.interfax.ru/russia/716956 | ✅ |
| 110 | 景 `open-you`、`flash-you`：睡袋裡的年輕女性 | CONFIRMED：旁白是對「你」說，算觀眾替身，不是登山者；但第一景就接 t002「九個人這樣走了」，容易被讀成隊員。建議加現代裝備（例如 modern down sleeping bag、headlamp）讓人分得出 | t001、t039 都是對觀眾的問句 | — | — | △ |
| 111 | 景 `ch6-end`（舊桌機響）、`call`（秘書遞話筒） | CHANGED：來源是打到他的手機，沒有秘書。建議 `ch6-end` 改「a smartphone starting to buzz on a cluttered desk」；`call` 改「a young researcher in a university corridor holding a smartphone to his ear with one eyebrow raised」，不要點名 | 「rang EPFL professor Johan Gaume’s cell phone」 | EPFL 2021 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans | ✅ |
| 112 | 景 `temp-flee`：an older mountaineer | CHANGED：t031 指的人當年 21、22 歲（1937 年生）。建議 `older` 改 `young` | 「Год рождеия 1937」 | 索格林證詞 | https://dyatlovpass.com/case-files-330-339-ru | ✅ |
| 113 | 景 `guess-note`、`guess-cond`：速記員打字、打字稿 | CHANGED（低）：坦帕洛夫的證詞是他親筆寫的。建議改成手寫（a clerk reading a handwritten page） | 「Записано верно, собственноручно」 | 坦帕洛夫證詞 | https://dyatlovpass.com/case-files-309-312-ru | ✅ |
| 114 | 景 `ch7-end`、`flip`、`see`、`hour`：連帽戴護目鏡的嚮導 | CONFIRMED：兩位嚮導在世，但旁白不點名、畫面無臉，照規則是無名角色，可留 | Comment 有寫他們的名字，旁白沒有用 | Puzrin & Gaume 2022 | https://www.nature.com/articles/s43247-022-00393-x | △ |
| 115 | 景 `reprimand`、`resign` | OUT OF SCOPE：隨 t090、t091 刪除 | — | — | — | — |

## 開不到的來源

- UNOPENED：`pressa.sledcom.ru`（偵查委員會會刊 2025 年一篇）回 403，Wayback 也沒有。
- `svpressa.ru/politic/article/226183/` 現場回 403，用 Wayback 封存開（Wayback 另有 2025-10-07 版本），內容已讀。
- 1959 年文件我讀的也是資料站轉錄，掃描沒有比對；坦帕洛夫、斯洛布佐夫、索格林等人是否過世未滿 70 年，我以 1921–1939 年生推定，沒有逐一查歿年。
