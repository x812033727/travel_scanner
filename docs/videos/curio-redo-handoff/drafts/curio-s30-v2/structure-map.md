# S30 v2 重做：10 步對照表

lint 估總長 12.2 分鐘（731 秒，正文 2,518 字）。秒數照字數比例估，比例欄是 `heimao/STRUCTURE.md` 共通模板的建議。

| 步 | 名稱 | 開始 | 秒數 | 占比 | 模板建議 | scene id |
|---|---|---|---|---|---|---|
| 1 | 鉤子 | 0:00 | 44 | 6.0% | 3–5% | open-novel、open-permit、open-real、open-twist、open-warrant、open-arrow、open-emperor |
| 2 | 承諾句 | 0:43 | 7 | 1.0% | 1–2% | open-promise |
| 3 | 時代與起源 | 0:50 | 92 | 12.5% | 8–20% | src-where、src-cien、src-daoxuan、era-border、era-petition、cien-no、cien-alone、cien-q、xu-no、xu-desk、xu-how、frost、frost-west、two-ways、first-gate |
| 4 | 第一次起落 | 2:22 | 106 | 14.5% | 10–15% | liang-li、liang-order、lecture、lecture-q、report、report-ask、report-back、secret、hide-day、yumen、beacons、warrant-arrives、warrant-text、lichang、lichang-q、truth、tear-say、tear、tear-next |
| 5 | 升級關卡 | 4:08 | 158 | 21.6% | 25–35% | shi、shi-vow、old-man、old-horse、old-horse-b、river、bridge、bridge-cross、law-q、law、law-lost、law-later、knife、quit、promise、alone、beacon-water、beacon-skin、arrow、arrow-2、wang、wang-no、wang-gift、bolong、two-only |
| 6 | 最大危機 | 6:46 | 49 | 6.7% | 8–12% | moheyan、lost、spill、spill-b、turn-east、ning、ning-west、thirst、collapse |
| 7 | 翻身與揭曉 | 7:35 | 78 | 10.6% | 8–12% | wind、horse-up、grass、yiwu、gaochang、gaochang-keep、gaochang-q、brothers、brothers-ada、novel、novel-c、gifts、three-years |
| 8 | 尾聲：故事還沒結束 | 8:53 | 143 | 19.5% | 8–12% | gaochang-fall、khotan、khotan-eight、confess、confess-b、tianwei、tianwei-q、reply、return、luoyang、luoyang-meet、first-words、answer、answer-b、praise、praise-ada、which-year、which-year-b、yuannian、old-history、scholars、scholars-b |
| 9 | 主題收束 | 11:16 | 43 | 5.8% | 6–8% | close-q、close-a、close-history、close-help、close-help-b、close-line、close-file |
| 10 | 提問與訂閱 | 11:58 | 13 | 1.7% | 1.5–2.5% | close-you、close-subscribe |

**比例說明**
- 步 5 偏低（21.6%）、步 8 偏高（19.5%）。
- 步 8 偏高，是因為原片最後兩章（洛陽宮的赦免、哪一年出關）都留在「故事還沒結束」。
- 如果把烽火台那一段（beacon-water 到 two-only）算進步 6，步 5 約 14%、步 6 約 15%。
- 這一稿把烽火台算步 5：箭是「升級關卡」的最後一關，真正的谷底是水袋打翻。

## 章節

| 章 | 第一景 |
|---|---|
| 御弟、文牒，和一份通緝公文 | open-novel |
| 兩本傳記，兩種說法 | src-where |
| 涼州都督逼他回去，瓜州州吏撕了公文 | liang-li |
| 三更天，他在玉門關上游十里過了河 | shi |
| 烽火台下，一支箭差點射中他的膝蓋 | beacon-water |
| 水袋打翻，四夜五天沒喝一滴水 | moheyan |
| 高昌王跟他結拜，不是唐太宗 | wind |
| 于闐的奏章：他自己寫下「私往天竺」 | gaochang-fall |
| 洛陽宮：皇帝的第一句話 | luoyang |
| 他是哪一年出關的？ | which-year |
| 被撕掉的公文，和一匹老馬 | close-q |

## 原段落搬到哪裡

| 原章（原 id） | 新位置 | 怎麼處理 |
|---|---|---|
| 瓜州的州吏，拿出一張通緝公文（x001–x010） | 步 1、2；瓜州那一幕搬到步 4 | 原開場直接跳進瓜州的場景，接著才倒回長安，時間是跳的。現在的鉤子先講觀眾知道的版本（《西遊記》的御弟、通關文牒），再點出這是真人玄奘，然後翻出反差：史書裡他沒有文牒，反倒被公文追著跑。鉤子只留兩個預告：烽火台的箭、皇帝的第一句話。承諾句改成「今天我們就來聊聊」，由 Ada 說。「十七個年頭翻一遍」那句拿掉。 |
| 長安的奏章（x011–x022） | 步 3 | 前面新加兩段。一段介紹兩本傳記從哪裡來：慧立的《慈恩傳》〔#41〕、道宣的《續高僧傳》〔#2 #41〕。一段講時代：唐朝剛建國，邊境禁止百姓出境〔#5，原本在涼州章〕。接著才是奏章的兩種說法和霜災。「先回到瓜州之前」這類倒敘句都拿掉了。 |
| 涼州都督逼他回長安（x023–x038） | 步 4 | 照時間順序講：涼州講經被告發，被逼回長安（危機），法師暗中送他往西（翻身），晝伏夜行到瓜州。之後是玉門關和五烽，通緝公文追到，李昌撕掉公文。李昌第一次出場就在這裡，不用再說「還記得開場那個州吏嗎」。刺史獨孤達那句刪了。「換成你是李昌」只留在結尾的 CTA。 |
| 三更天過河（x039–x050） | 步 5 前半 | 照舊。唐律那張卡改成兩景：Ada 問、一個天平畫面。「傳記寫，玄奘看不出他的意思」併掉了。 |
| 烽火台下的箭（x051–x062） | 步 5 後半 | 箭點名回收鉤子。王伯隴兩句併成一句。「你有沒有想過，一個人要怎麼走那麼遠」刪了，莫賀延磧移到步 6 開頭。 |
| 水袋打翻（x063–x072） | 步 6，涼風之後進步 7 | 谷底停在「這一次，誰來救他？」。步 7 從涼風開始，老紅馬點名回收，接青草水池、伊吾。 |
| 高昌王跟他結拜（x073–x083） | 步 7；高昌亡國移到步 8 開頭 | 結拜由 Ada 點名回收鉤子的「御弟」。路費統計卡改成一句旁白，黃金和銀錢的數目拿掉，因為數字不入畫。「這個約，他守得住嗎？」跨進步 8 才回答。 |
| 于闐的奏章（x084–x091） | 步 8 | 「我們覺得」改成 Ada 說「我覺得」。「天威」那句後面加一句 Ada 的小結：「一邊認罪，一邊歸功給皇帝」〔#47 備註〕，再問皇帝會怎麼回。 |
| 洛陽宮：皇帝的第一句話（x092–x097） | 步 8 | 第一句話回收鉤子，「玉門關那筆帳」回收步 5。 |
| 哪一年出關（x098–x103） | 步 8 尾 | 照舊，學者那句拆成兩景，都是 Ada。 |
| 結尾（x104–x107） | 步 9、10 | 新加倒帶：小說給他文牒，史書裡追著他的是公文和箭；幫他走過去的是州吏、胡人、軍官和老馬。這些都是前面講過的事。再收一句 Ada 的看法：讓他走出去的，是「絕不往東走一步」。最後是「存檔／未結」和原本的 CTA。 |

## 埋梗與回收（loops，共 23 條，已寫進 video.json）

| 埋 | 收 | 內容 |
|---|---|---|
| x001（open-novel） | x095（brothers-ada） | 結拜的御弟：其實是高昌王 |
| x004（open-twist） | x097（novel-c） | 史書裡，他出發時連文牒都沒有 |
| x005（open-warrant） | x038（warrant-arrives） | 追著他跑的那份公文 |
| x006（open-arrow） | x066（arrow） | 烽火台下的那支箭 |
| x007（open-emperor） | x114（first-words） | 皇帝的第一句話 |
| x008（open-promise） | x127（close-a） | 他真的是偷渡出國的嗎 |
| x017（cien-q） | x018（xu-no） | 奏章送到皇帝面前了嗎 |
| x021（xu-how） | x022（frost） | 那他是怎麼走的 |
| x029（lecture-q） | x030（report） | 消息會傳到誰耳朵裡 |
| x033（report-back） | x034（secret） | 他回去了嗎 |
| x041（lichang-q） | x042（truth） | 這說的不就是你嗎 |
| x046（tear-next） | x053（bridge） | 玉門關要怎麼過 |
| x051（old-horse-b） | x086（horse-up） | 認得路的老紅馬 |
| x058（law-later） | x118（praise-ada） | 出關這筆帳，後來有人算嗎 |
| x063（alone） | x089（yiwu） | 一個人走得出去嗎 |
| x069（wang-no） | x070（wang-no） | 他會跟著回敦煌嗎 |
| x074（two-only） | x075（moheyan） | 最難的一段 |
| x084（collapse） | x085（wind） | 這一次誰來救他 |
| x092（gaochang-q） | x093（gaochang-q） | 國王會不會放人 |
| x100（three-years） | x101（gaochang-fall） | 三年之約守住了嗎 |
| x103（khotan-eight） | x104（confess） | 最重要的八個字 |
| x108（tianwei-q） | x109（reply） | 皇帝會怎麼回 |
| x119（which-year） | x121（yuannian） | 哪一年出關 |

## 人物代表物（歷史人物不入畫）

| 人物 | 固定代表物 |
|---|---|
| 玄奘 | 竹編行李架 `a tall woven bamboo backpack frame` |
| 唐太宗 | 鋪黃絲的空寶座 `a tall empty throne draped in bright yellow silk` |
| 李大亮 | 紅纓鐵盔 `a dark iron helmet with a red plume` |
| 李昌 | 只畫手（遞出、撕掉公文） |
| 石槃陀 | 尖頂氈帽 `a tall pointed felt hat` |
| 胡老翁 | 老紅馬加一根拐杖 |
| 王祥 | 獵弓 `a hunting bow`；王伯隴是兩把並掛的弓 |
| 麴文泰 | 鑲寶石金冠 `a jewelled gold crown` |
| 《慈恩傳》（慧立） | 紅色素面厚書 |
| 《續高僧傳》（道宣） | 藍色素面厚書 |
| 《西遊記》 | 橘色素面厚書 |
| 《廣弘明集》那篇表 | 綠繩細卷軸 |
| 《舊唐書》 | 一疊黑皮厚書 |
| 通緝公文 | 綁紅繩的空白摺紙 `a folded blank paper order tied with red cord` |
| 老紅馬 | `an old thin red horse`（動物，不算人） |

一般人可以入畫：涼州聽講的人、告密的人、兩個送行的弟子、結尾的「你」。另有幾景只畫手，例如裝水、打翻水袋、合掌、遞乾糧。
