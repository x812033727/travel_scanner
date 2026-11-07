# curio-s31-v2 重做：10 步對照表

這一版估計長 15:23：正文 3,139 字，用原片實測的語速（3,206 字合成 943.7 秒，每秒約 3.40 字）來算。lint 估 15.0 分鐘。「比例」欄是 `heimao/STRUCTURE.md` 共通模板建議的比例。

| 步 | 名稱 | 開始 | 秒數 | 占比 | 模板建議 | scene id |
|---|---|---|---|---|---|---|
| 1 | 鉤子 | 0:00 | 49 | 5.3% | 3–5% | open-poem、open-meaning、open-far、open-fresh、open-bai、open-death、open-twice |
| 2 | 承諾句 | 0:48 | 6 | 0.7% | 1–2% | open-promise |
| 3 | 時代與起源 | 0:55 | 106 | 11.4% | 8–20% | origin-dumu、origin-born、origin-lookback、origin-era、origin-tianbao、origin-fresh、origin-north-q、origin-zhang、origin-zhang-shrug、origin-bai-first、origin-bai-paint、origin-fruit-q、origin-lizhao、origin-bai-days、origin-bai-days2、origin-gradual、origin-looks、origin-deadline |
| 4 | 第一次起落 | 2:40 | 100 | 10.9% | 10–15% | relay-method、relay-you、relay-handoff、station、station-slow、pass-note、pass-cane、edict、edict-text、edict-300、edict-q、edict-tongjian、edict-ada、basket-wait、relay-close、crossroads |
| 5 | 升級關卡 | 4:20 | 268 | 29.0% | 25–35% | （唐人說南海）dufu、dufu-poem、dufu-route、dufu-route2、dufu-q、dufu-after、bao、bao-poem、bao-fast、bao-laugh、lingnan-li、lingnan-li2、shu-q、lizhao-again、guoshibu、shu-plant、shu-trap、ganze、ganze-scene、ganze-q、sima、sima-gap、arc-turn；（宋人說涪州）cai、cai-basket、cai-first、cai-quality、shu-returns、su、su-route、su-gai、fu-dist、fu-half、bai-zhongzhou、bai-tribute-q、bai-tribute、bai-limit、jian-q、jian、jian-ada、jian-close |
| 6 | 最大反轉 | 8:48 | 130 | 14.1% | 8–12% | wu、wu-you、wu-mingyi、wu-full、wu-turn、wu-listen、wu-fuzhou、wu-su、wu-local、wu-odd、orchard-witness、orchard-q、gaz、seven-days、seven-callback、gaz-poem、gaz-circle、gaz-copy、gaz-ada |
| 7 | 揭曉高潮 | 10:58 | 56 | 6.1% | 8–12% | rider-q、rider-edict、rider-same、rider-caveat、rider-receipt、fan-boat、gaz-admit、chen-wait |
| 8 | 尾聲：故事還沒結束 | 11:54 | 138 | 15.0% | 8–12% | chen、chen-quote、chen-season、chen-verdict、chen-scope、cheng、cheng-digs、cheng-date、cheng-more、cheng-poem、cheng-claim、cheng-q、cheng-key、winter、tianbao8-find、tianbao8、tianbao8-only、tianbao8-q、tianbao8-no、dumu-august、dumu-calendar、dumu-image |
| 9 | 主題收束 | 14:12 | 55 | 6.0% | 6–8% | baskets-a、baskets-b、close-fresh-q、close-xintang、close-notsame、verdict、verdict2、close-line |
| 10 | 提問與訂閱 | 15:07 | 15 | 1.6% | 1.5–2.5% | outro-q、outro-sub |

和模板差最多的是步 7。它只占 6%，因為這個故事最大的一次反轉就是吳曾改口（步 6），步 7 只負責揭曉「七天七夜」和那道詔書的速度一樣。步 8（華清宮季節之爭）比建議多 3%，原因是程大昌的辯護和夏四月那個例外都得講完，結論才站得住。

## 章節

章節照原檔的寫法，寫在每一章第一景的 `chapter` 欄位。時間是用每秒 3.40 字估的；lint 的估法略短，見 `changes.md`。

| 章 | 開始 | 對應步 |
|---|---|---|
| 一騎紅塵，送的是什麼？ | 0:00 | 1–2 |
| 寫詩的人，晚了將近五十年 | 0:55 | 3 |
| 一站一站接力，和一道催命的詔書 | 2:40 | 4 |
| 唐人說：南海來的使者 | 4:20 | 5 前半 |
| 宋人說：四川的涪州 | 6:54 | 5 後半 |
| 吳曾翻到後面，改了答案 | 8:48 | 6 |
| 七天七夜，跟那道詔書一樣快 | 10:58 | 7 |
| 收貨的人，當時在華清宮嗎？ | 11:54 | 8 |
| 散落的荔枝筐 | 14:12 | 9–10 |

## 原本的段落搬到哪裡

**開場：拿掉濃縮預告，鉤子先講懂**

| 原 scene | 新位置 | 說明 |
|---|---|---|
| poem（卡） | open-poem（步 1） | 第一句就是大家熟悉的那句詩，後面一句 open-meaning 說明它在講什麼 |
| consort-basket（人馬死傷） | open-death（步 1） | 留在鉤子當作利害，到步 6 的 seven-callback 才揭出處 |
| xin-tang（卡）、bai-branch | open-fresh、open-bai（步 1） | 「味未變」對上「三天變味」，就是這支片怪在哪裡 |
| tease-scholar | open-twice（步 1） | 預告第二個高潮：吳曾改口 |
| tease-edict | 拿掉 | 鉤子最多兩個預告。這道詔書放回步 4 它該出現的時候 |
| v2-add-001（「今天跟著一籃荔枝……」） | 拿掉 | 跟承諾句重複 |
| the-question | open-promise（步 2） | 改成固定句型「今天我們就來聊聊：……」，由 Ada 說 |
| dumu-writes | origin-dumu、origin-born、origin-lookback（步 3） | 這個故事是從杜牧的詩來的，所以起源先交代寫詩的人。用到 S31 第 2、49 列的「晚了將近五十年」 |

**原第 1 章「天寶五載，一道命令把人催上路」拆成兩步**

- **荔枝本身和長安人不認得荔枝，搬到步 3（時代與起源）**：lizhao、bai-desk、bai-days、v2-add-014、v2-add-015、bai-painter、zhang、zhang-shrug、bai-taste。
  - 先講貴妃要吃新鮮的（新唐書「必欲生致之」），再講這種果子多難保存。
  - 收在 origin-deadline 的「那要怎麼送？」。
- **驛站制度留在步 4（第一次起落）**：relay-handover、v2-add-002、v2-add-003、station、slow-rider、pass-note、v2-add-007、edict-sealed、ten-stations、v2-add-008、v2-add-009、300-li、exile、exile-road、v2-add-010、basket-wait、v2-add-012、crossroads。
  - 這一步的結構是：答案（置騎傳送）→ 規矩 → 更狠的詔書 → 果子不等人。
  - relay-close 收一句「這就是驛路的壓力」。
  - v2-add-004 和 v2-add-013 是過場句，拿掉了。

**原第 2 章（杜甫）、第 3 章（宋人說涪州）：步 5 升級關卡，順序幾乎不變**

- dufu-later 併進 dufu-route2。
- v2-add-027 併進 bao-fast。
- bao-laugh 拆成兩景：看法（bao-laugh），以及「多遠？」加答案（lingnan-li）。
- v2-add-028 改寫成 lingnan-li2 的「兩句詩，就把幾千里抹掉了」。
- v2-add-032、v2-add-033 併成 shu-trap。
- musician、emperor-lychee 改成 ganze、ganze-scene；v2-add-034、v2-add-035 併成 ganze-q。
- cai、cai-quote 併成 cai；cai-proud 拆成 cai-first 和 cai-quality。
- v2-add-037 的「路短一些，果子就一定新鮮嗎？」移到 fu-half，緊接在「一半」後面。
- v2-add-040、v2-add-041 併成 su-gai；v2-add-042、v2-add-043 併成 bai-limit。

**原第 4 章（吳曾）：步 6 最大反轉，加上步 7**

- 吳曾改口、妃子園、七天七夜、地方志拿杜牧的詩作證、「圖經相傳」都在步 6。
- seven-callback 是新加的點名回收：「開頭那句人馬死傷，就出自這裡」。
- 拿掉 v2-add-049、v2-add-055、v2-add-059 這三句過場。
- 「七天七夜一天要跑幾里」到范成大、地方志自己承認那一段，成了步 7。rider-same 是新加的 Ada 反應，用來兌現步 4 的「先記住這個速度」。

**原第 5 章（華清宮）：步 8 尾聲**

- 「故事還沒結束」放在步 7 最後一景 chen-wait。
- chen-quote 拆成兩景，問句後接答案「盛夏」（chen-season）。
- wang 併進 chen-verdict。
- v2-add-069、v2-add-070 併成 cheng-q；v2-add-071 和 arc-doubt 併成 cheng-key。
- v2-add-065 拿掉。

**收尾：步 9、步 10**

- v2-add-075 拆開：前半是 dumu-image（步 8 最後的問句），後半併進 baskets-a。
- v2-add-079 到 v2-add-082 改成 close-fresh-q、close-xintang、close-notsame。
- verdict（卡）拆成兩景，verdict 和 verdict2。
- close-line 是新加的金句，是旁白的看法，沒有新事實。
- outro（卡）改成兩張插圖：outro-q 和 outro-sub。

## 埋梗與回收（loops，共 28 條）

| 埋 | 收 | 內容 |
|---|---|---|
| t001（open-poem） | t009（origin-dumu） | 這句詩是誰寫的：晚唐的杜牧 |
| t001（open-poem） | t108（gaz-poem） | 杜牧那首詩：地方志拿它當妃子園的證據 |
| t001（open-poem） | t146（baskets-a） | 那一騎紅塵：荒廢的華清宮只剩荔枝筐 |
| t004（open-fresh） | t028（relay-method） | 《新唐書》說味未變：答案藏在「置騎傳送」 |
| t004（open-fresh） | t151（close-notsame） | 史書的「味未變」和白居易的變味觀察，不是同一批果子的互驗紀錄 |
| t005（open-bai） | t023（origin-bai-days） | 白居易的三天：一天變色、兩天變香 |
| t006（open-death） | t107（seven-callback） | 開頭人馬死傷的出處：宋代地方志，不是唐代運單 |
| t007（open-twice） | t097（wu-turn） | 同一本書寫了兩個答案的宋朝學者：改口了 |
| t008（open-promise） | t153（verdict2） | 楊貴妃的荔枝怎麼送到長安：結檔 |
| t012（origin-era） | t013（origin-tianbao） | 杜牧回頭看的年代：天寶年間 |
| t015（origin-north-q） | t016（origin-zhang） | 長安的大官見過荔枝嗎 |
| t018（origin-bai-first） | t085（bai-zhongzhou） | 忠州的白居易：那裡的荔枝不能進貢 |
| t022（origin-lizhao） | t064（lizhao-again） | 李肇「過一夜就壞」那條筆記的前半 |
| t027（origin-deadline） | t028（relay-method） | 要新鮮又會變味，那要怎麼送 |
| t033（station-slow） | t034（station-slow） | 騎馬的人一天能跑幾站 |
| t041（edict-300） | t115（rider-edict） | 十個驛站約三百里，七天七夜也要一天三百多里 |
| t049（crossroads） | t050（dufu） | 荔枝從哪裡出發 |
| t054（dufu-q） | t055（dufu-after） | 貴妃個人的口味能不能解釋驛路：杜甫寫她死後荔枝照樣進貢 |
| t060（lingnan-li） | t061（lingnan-li） | 嶺南到長安多遠 |
| t066（shu-plant） | t079（shu-returns） | 先記住的「蜀」字：涪州在四川 |
| t069（ganze-scene） | t129（cheng-digs） | 《甘澤謠》驪山那一幕：天寶十四載六月一日 |
| t074（arc-turn） | t075（cai） | 宋朝人說的另一個地方 |
| t092（jian-close） | t093（wu） | 涪州說法的依據：吳曾也找過 |
| t104（orchard-q） | t105（gaz） | 妃子園後來被寫成什麼樣子 |
| t114（rider-q） | t115（rider-edict） | 七天七夜，一天要跑幾里 |
| t122（chen-wait） | t123（chen） | 貴妃當時在華清宮嗎 |
| t136（cheng-key） | t137（winter） | 史書怎麼說 |
| t141（tianbao8-q） | t142（tianbao8-no） | 夏四月那一次，能不能證明荔枝也到了 |

鉤子預告的兩個高潮在正片兌現：
- 人馬死傷在 t107，句子點名「開頭那句」。
- 吳曾改口在 t097。

## 反覆出現的代表物

歷史人物一律不畫人像，每人固定一個物件，提示詞裡逐字用同一句：

| 人物 | 代表物（提示詞原文） | 用在 |
|---|---|---|
| 楊貴妃 | a gold flower hairpin | open-meaning、origin-born、origin-deadline、dufu-q、shu-trap、orchard-q、gaz-admit |
| 唐玄宗 | a pale yellow silk parasol | origin-tianbao、dufu-after、chen-quote、cheng-date |
| 杜牧 | a small pale celadon wine cup | origin-dumu、gaz-poem、gaz-circle、cheng-claim、dumu-august、dumu-calendar |
| 白居易 | a slate-blue round silk fan（摘荔枝那景只畫 slate-blue 袖子的手） | open-bai、origin-bai-paint、origin-bai-days2、bai-tribute、cheng-poem、close-xintang、origin-bai-first |
| 李肇 | a small sand-coloured bound notebook | origin-lizhao、lizhao-again、shu-returns（Ada 手上拿） |
| 張九齡 | a plain ivory court tablet with a crimson tassel | origin-zhang |
| 杜甫 | a worn brown walking staff | dufu、dufu-route2 |
| 鮑防 | an ochre wine gourd | bao |
| 蔡襄 | a dark red bound book with a plain cover | cai、cai-first |
| 蘇軾 | a tall square black scholar's hat | su、wu-su |
| 吳曾 | a thick tan bound book with two red ribbon bookmarks | open-twice、wu、wu-mingyi（翻到第一個書籤）、wu-turn（翻到第二個書籤）、wu-su |
| 地方志 | a thick gazetteer volume tied with brown string | gaz、seven-callback、gaz-poem、gaz-copy |
| 陳正敏 | a charcoal-grey wooden abacus | chen、chen-verdict |
| 程大昌 | a dark umber lacquered scroll case | cheng、cheng-digs、cheng-claim |
| 《甘澤謠》 | a bamboo flute | ganze、ganze-scene、ganze-q（Ada 手上拿）、cheng-digs |
| 史書 | a thick history volume with a plain cover | sima、sima-gap、tianbao8-find、tianbao8-only、close-xintang |

一般人照 RULES 第 6 條畫成普通卡通人：
- 驛使：`a young relay rider in a dusty brown riding robe and black headscarf`，10 景。
- 驛站文書：`a thin post-station clerk in a mustard robe and black headscarf`，3 景。
- 被貶官員：1 景。
- 其他各 1 景：長安的同僚、當地老農、「你」（查資料的讀者、在長安等荔枝的人）。

前後呼應的畫面：
- 長直路與一排驛站：edict-300 和 rider-edict。
- 吳曾的書：open-twice → wu → wu-mingyi → wu-turn。
- 荒廢的華清宮：origin-lookback 和 baskets-a。
- 兩位驛使交接竹籃：relay-method 和 verdict。
