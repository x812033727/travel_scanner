# sothatswhy-b26 查核第一輪

- 查核 2026-10-10（UTC），Claude Opus 5.5（查核代理，不是撰稿的那一個）。
- 方法：先把 `video.json` 的每句旁白、每張卡片、縮圖、標題、說明欄、標籤、`sources[]`，以及 `shorts.json` 兩支的標題、說明、字卡與旁白抽成 304 條清單（`<home>\mokaair-work\videos\sothatswhy-b26\_tools\verify-1\claims-extracted.txt`，改完後重抽一份 `claims-extracted-after.txt`），再把查核包 [`../so-thats-why/season2/B26.md`](../so-thats-why/season2/B26.md) 與 `claims.md` 列的每個網址當天用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔一秒以上）重開，去掉註解後讀全文：S1 逐字稿整篇、S2 節目頁整頁、S3 與 S4 的摘要、作者摘要、介入方法段、限制與 Discussion 開頭。網路搜尋 0 次（上限 5 次）。
- 這一集沒有「官方頁」意義下的數字；一手來源是 NPR 的逐字稿（會員電台刊載，頁尾標明逐字稿由 NPR 提供）與兩篇 PLOS Medicine 論文的原文頁。`claims.md` 是撰稿者的證據，本表每一列都對回今天讀到的原文。
- 「來源」欄寫的是原文在哪裡、說了什麼（中文轉述）；原文是有著作權的逐字稿與論文，這裡不整句照抄，只在要對用詞時留下個別英文詞。要看原句，開上面的網址，或看 `_tools\verify-1\text\` 裡當天存下的純文字。
- 改動原則：只改事實與連帶的地方；行 id 不變、沒有加場景或句子；每句 22 單位以內（帶 `emotion` 的 20 以內）。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| S1 | https://www.nprillinois.org/2014-08-01/everyone-goes-to-the-store-to-get-milk-so-whys-it-way-in-the-back （NPR Illinois 刊載的 NPR 逐字稿；頁面資料的節目欄是 Morning Edition，發布 2014-08-01，署名 David Kestenbaum） | 200 |
| S1-NCPR | https://www.northcountrypublicradio.org/news/npr/337034378/ （查核包原本的入口） | 403：NOT OPENED |
| NPR 主站 | https://www.npr.org/2014/08/01/337034378/… 與 https://www.npr.org/transcripts/337034378 | 逾時（30 秒沒有回應）：NOT OPENED |
| S2 | https://www.kedm.org/2016-09-21/episode-555-why-is-the-milk-in-the-back-of-the-store （發布 2016-09-21） | 200 |
| S3 | https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1003729 （發表 2021-09-07） | 200 |
| S4 | https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004575 （發表 2026-03-31） | 200 |
| DOI | https://doi.org/10.1371/journal.pmed.1003729 、https://doi.org/10.1371/journal.pmed.1004575 | 200，各自轉到 S3、S4 |

S1 的主張都靠 NPR Illinois 這一份逐字稿判定；NCPR 與 NPR 主站今天沒讀到，沒有拿來當依據。S3、S4 兩頁除了選單連結，沒有更正、撤稿或關注聲明的標記（只代表這兩頁今天的狀態）。

## 主張對照表

| # | 主張 | 位置 | 來源（今天讀到的內容） | HTTP | 判定 | 修改前 → 修改後 |
|---|---|---|---|---|---|---|
| 1 | 標題的「常」是那份報導的描述，不是統計出來的比例 | `youtube.title`、`hook.data.title`、`hook-often/nus6`、`hook-not-stat/6az8`、說明欄第 4 段 | S1 主持人開場說牛奶 often 放在店的最後面；S2 節目介紹第一句也用 often。兩處都是描述，沒有比例 | 200 | CONFIRMED | — |
| 2 | 2014 年，美國公共廣播（NPR）一位記者去問過 | `hook-reporter/jd8n`、說明欄第 2 段 | S1：2014-08-01、Morning Edition、記者 David Kestenbaum；他在稿中說自己去訪問了幾家超市與顧問 | 200 | CONFIRMED | — |
| 3 | 「超市要你多逛、多買」是你大概聽過的一種說法 | `hook-common/eqj3`、說明欄第 1 段 | S1 主持人開場把它列為一種理論；S2 稱它是常見的解釋 | 200 | CONFIRMED | — |
| 4 | 那位記者問到的人給了兩種理由；兩種考量都有人提到 | `hook-two-answers/c523`、`measure-both-said/mdh2`、說明欄第 2 段 | S1：記者在公關那一句之後說，兩種想法都確實有人講 | 200 | CONFIRMED | — |
| 5 | 範圍：美國一次採訪裡的個案，不是全球普查；講的是要冷藏的鮮奶，不含常溫保久乳 | `hook-one-case/66xe`、`hook-fresh-milk/5dpf`、`hook-shelf-milk/xt4d`、說明欄第 4 段 | S1：受訪者都在美國，談的是要一路冷藏的桶裝牛奶；查核包開頭的界定 | 200 | CONFIRMED | — （範圍聲明） |
| 6 | 開場鋪陳、片頭卡副標、縮圖三行（你以為／其實、兩條路線、要分開來看、章末問句） | `hook/wxac`、`tamr`、`6297`、`hjar`、`m3wc`、`hook.data.subtitle`、`thumbnail.data` | — | — | OUT OF SCOPE | — （沒有可查的事實） |
| 7 | 報導裡有一位受訪的經濟學者；研究經濟、不在超市工作 | `route-economist/8sd7`、`route-scholar/j5xn` | S1：記者介紹 Russ Roberts 是 Hoover Institution 的經濟學者；他自稱學界的人 | 200 | CONFIRMED | — |
| 8 | 他的解釋：卡車把牛奶送到超市後方，後方有冷藏室，留在後面是因為方便 | `hook-backdoor`（c5）、`route-from-back/8bht`、`route-truck/2eze`、`route-coldroom/cpay`、`route-handy/wgi8`、說明欄第 2 段 | S1：由記者轉述他的想法，三點依序是放後面比較省事（easier）、卡車把牛奶送到後方、那裡有一間大冷藏室 | 200 | CONFIRMED | — （原文只說後方，「後門」是旁白的說法，見懷疑項 2） |
| 9 | 概念示意：跟著一箱鮮奶走（冷藏卡車、後門、後方的冷藏室、賣場的冷藏櫃）；兩條路線在冷藏櫃碰頭；不是每家超市的構造，也不是每個冷藏櫃後面都有冷藏室 | `route-chapter`（卡片與 `ke2y`）、`v2vz`、`nkcn`、`q8bx`、`dnk4`、`ymj3`、`5q6u`、`route-compare`（卡片、`e4a6`、`bnyd`）、`vp2w`、`answer-meet/epea` | S1 只有第 8、12 列那幾句；其餘是節目自己的示意 | — | OUT OF SCOPE | — （旁白說「畫成示意圖」，卡片結語與來源欄都標「概念示意」） |
| 10 | 同一份報導裡有一位乳品採購，任職於一家會員制的量販店 | `route-buyer/gucw`、`route-club/ufp3`、說明欄第 2 段 | S1：記者介紹 Rob Olsen 是 BJ's Wholesale Club 的乳品採購，並說這家公司是另外兩家會員制量販店的主要對手；他自己用「會員」稱顧客 | 200 | CONFIRMED | — |
| 11 | 這位採購提到「冷鏈」；白話是運送和存放全程維持冷藏；冷鏈是他自己提出來的 | `route-cold-chain/97s7`、`route-meaning/hz6p`、`route-never-warm/r57j`、`basket-also-cold/9236` | S1：記者說採購接著提到另一個詞 cold chain，並解釋牛奶裝瓶之後每一步都要保持低溫 | 200 | CONFIRMED | — |
| 12 | 採購描述的五站：冷藏室 → 冷藏卡車 → 冷藏的配送中心 → 再上冷藏卡車 → 賣場 | `route-chain-steps`（卡片五格、來源欄、`kbe9`、`ursr`、`tbqr`） | S1：採購本人的話，依序是冷藏室、冷藏卡車、冷藏的配送中心、再回到冷藏卡車、賣場 | 200 | CONFIRMED | — （順序與用詞都對） |
| 13 | 購物籃理由：記者問牛奶為什麼放在後面；採購說希望顧客走到賣場後方、看到他們賣的各式商品；記者追問是不是看到就覺得也需要，他說沒錯；這一行叫它 building the basket | `route-question/4hkb`、`basket-chapter`（卡片、`7d7i`）、`y85c`、`t85d`、`m4t8`、`x4yj`、`kner`、`8ieg`、`xhx6`、`answer-see-more/xagr`、說明欄第 2 段 | S1：一問一答四句都在，順序與旁白一致；採購說的是希望會員走到賣場後方、看到店裡賣的各種品項，記者把它轉述成看到別的東西就覺得也需要，採購答對，並說業界稱為 building the basket | 200 | CONFIRMED | — （「沿路」「更多」是意譯，見懷疑項 3） |
| 14 | 示意：顧客走得越遠、經過的貨架越多，購物籃裡多了一樣東西 | `basket-sketch/ycw3`、`6vam`、`jk4h`、`xm3s` | — | — | OUT OF SCOPE | — （旁白說「畫成示意圖」「不是測量到的結果」） |
| 15 | 這是一位採購自己的說明，不代表所有美國超市 | `basket-one-buyer/772x`、`basket-not-all/x3mw` | S1（一位受訪者的話）；查核包第 2 列的限制 | 200 | CONFIRMED | — |
| 16 | 事後，這家公司的公關向記者保證：冷鏈才是最主要的原因；這仍是公司的說明 | `basket-pr/sxg5`、`basket-primary/3gc9`、`basket-still-statement/3svm`、說明欄第 2 段 | S1：記者說 BJ's 的公關人員事後向他保證，冷鏈是最主要的原因（primary reason） | 200 | CONFIRMED | 措辭（不是事實修改）：`3gc9`「全程冷藏的冷鏈，才是最主要的原因。」→「公關說，全程冷藏的冷鏈才是最主要的原因。」 |
| 17 | 卡片「同一份報導，兩種考量」：左欄購物籃理由（乳品採購）；右欄經濟學者的後方收貨與冷藏室、採購的冷鏈、公關說冷鏈才是主因；結語「都是受訪者的說明，不是測量結果」 | `basket-compare.data`、`c3p4` | S1（第 8、11、13、16 列） | 200 | CONFIRMED | — |
| 18 | 「卡片右邊是冷藏的理由，有三個人提到」 | `basket-compare/s5ua` | S1：除了卡片上這三位，報導還說另一家連鎖超市的發言人兩種理由都提了（本集沒有用他） | 200 | CHANGED | 「有三個人提到。」→「列出三個人的說法。」 |
| 19 | 卡片來源欄：採購與公關「任職於」BJ's | `basket-compare.data.source` | S1 只稱這個人是 BJ's 的公關人員（PR person），沒有說雇用關係 | 200 | CHANGED | 「NPR 2014 年採訪｜採購與公關任職於 BJ's」→「NPR 2014 年採訪｜BJ's 的乳品採購與公關」（查核者原判 NOT FOUND：公關的雇用關係在逐字稿查不到，這個細節已從來源欄拿掉。協調者 2026-10-10 把這一欄改標 CHANGED：本表的列號 19 與 claims.md 的主張編號 c19 是兩回事，成片品管的 facts 項目卻把兩者對在一起，誤報蔬果研究那幾景還在引用查不到的主張。） |
| 20 | 意見：兩種考量可以同時出現；只看位置沒辦法斷定超市怎麼想；「要你多買」很順口，但是解釋不是測量 | `basket-both/79qe`、`ybgz`、`cuhv`、`eug8`、`5xim` | `brief.md` 站主觀點 | — | OUT OF SCOPE | — （標成「我的看法是」，與站主觀點一致） |
| 21 | 記者在報導結尾說，這次訪問到的人沒有誰拿得出一份測量過牛奶位置的實證研究 | `measure-chapter/yk2s`、`measure-nobody/pudc`、`measure-binder/8h8j`、說明欄第 2 段 | S1 記者倒數第二次發言：他說談過的人裡，沒有誰桌上有一本題為「牛奶最佳位置的實證研究」的資料夾 | 200 | CONFIRMED | — |
| 22 | 所以那次採訪分不出兩種考量各占多少；這句話只限那次採訪，不是說全世界沒有人研究過，也不能說各占一半 | `measure-no-ratio/p9td`、`pt5j`、`v94b`、`xp4w`、`answer-no-ratio/9pdr`、`answer-big.data.sub`、`outro.data.lines[0]`、說明欄第 2、4 段 | S1：整篇沒有任何比例；記者的結語是兩個理由都答「是」最保險 | 200 | CONFIRMED | — （沒有延伸成「沒有研究」） |
| 23 | 解釋和測量是兩件事；三步的研究設計示意；一批放後面、一批放前面的比較；「在看到那種研究以前，我只說到這裡」 | `measure-chapter.data`、`r8dn`、`spyh`、`47g3`、`hggc`、`ctpi`、`measure-steps`（卡片與三句）、`mkqp`、`sg4q`、`82bq`、`xm2x`、`jbas` | `brief.md` 站主觀點 | — | OUT OF SCOPE | — （意見與示意；卡片來源欄寫「不是已完成的研究」） |
| 24 | 2016 年這個題目又播出一次；節目頁面註明是 2014 年節目的重播，不算第二次調查 | `measure-rerun/mkpx`、`b6gz`、`2ngx`、說明欄第 2 段 | S2：頁面發布日 2016-09-21；正文第一行是註記，說這一集原於 2014 年 7 月播出 | 200 | CONFIRMED | — |
| 25 | 其他商品的配置有研究測量過；測量的是蔬果，不是牛奶 | `measure-question/m778`、`produce-chapter`（卡片、`gn8a`） | S3、S4：兩頁全文都沒有 milk 一詞 | 200 | CONFIRMED | — |
| 26 | 2021 年，一份醫學期刊刊出一項研究；地點在英格蘭，是小規模的試辦研究 | `produce-journal/t67m`、`produce-england/s4g8`、`produce-pilot-stats.data.title`、`.source` | S3：PLOS Medicine，2021-09-07 發表；摘要自稱 pilot study，在英格蘭的折扣超市做 | 200 | CONFIRMED | — |
| 27 | 3 家調整、3 家拿來比較；不是隨機分組，不是抽籤決定；兩組原本就可能不一樣，結論要保守 | `produce-pilot-stats`（兩格、`nqjd`、`hk4w`）、`yx7q`、`w7x8`、`jyfi`、說明欄第 3 段 | S3 摘要：3 家介入店、3 家配對的比較店，超市無法隨機分派；方法段說介入店是公司原本就排定要改裝的店；作者摘要要讀者對結果保持謹慎 | 200 | CONFIRMED | — |
| 28 | 「調整的地方，一共有三件事」 | `produce-bigger/jbrq`；`shorts.json` 第二支第 2 景字卡 | S3 摘要與方法段都寫「兩個」同時執行的介入項目；方法段另外列了冷凍蔬菜移到第一條走道、糖果區移到最後一條走道、店面同時清潔粉刷與換標示 | 200 | CHANGED | `jbrq`「調整的地方，一共有三件事。」→「調整的地方，我分成三件事來說。」；Shorts 字卡「英格蘭的試辦研究：同時調整三件事」→「英格蘭的試辦研究：同時調整好幾件事」 |
| 29 | 蔬果區擴大；整個移到入口附近；結帳區的糖果類商品撤掉；結帳區對面走道盡頭貨架上的糖果也撤掉 | `produce-bigger/6j72`、`produce-entrance/dvti`、`produce-checkout/e3de`、`produce-aisle-end/awdr` | S3 摘要與方法段：擴大蔬果區並擺到入口附近（取代原本在後方的小陳列）；撤掉結帳區與其對面走道盡頭的糖果類商品 | 200 | CONFIRMED | — |
| 30 | 結果是整間超市的蔬果銷售增加；看的是整間店的銷售；幾件事同時調整，功勞不能全算在搬到入口 | `produce-result/uby5`、`hbg7`、`eegw`、`pepc` | S3 摘要：介入店的店級蔬果銷售增幅高於模型預測；同一段說這是試辦研究，檢定力不足 | 200 | CONFIRMED | — （只用方向，沒有用數字） |
| 31 | 2026 年又有一項更大的研究發表；是後續的補充，不是更正前一項 | `produce-bigger-study/fikq`、`produce-supplement/5i4f`、`produce-big-stats.data.title`、`.source` | S4：2026-03-31 發表；內文兩處把 S3 稱為同一項研究的 pilot phase；S3 頁沒有更正標記 | 200 | CONFIRMED | — |
| 32 | 一共 36 家，18 家調整、18 家比較；追蹤到第六個月；一樣不是隨機分組 | `produce-big-stats`（三格、`ftes`、`3xu9`、`d7ee`）、`tvk9`、說明欄第 3 段 | S4 摘要：36 家店（18 介入、18 比較）；介入實施六個月，在第 3 與第 6 個月各看一次；限制段說無法隨機分派超市 | 200 | CONFIRMED | — |
| 33 | 除了位置，蔬果的品項也一起增加 | `produce-range/h2mg` | S4 方法段：兩個同時執行的項目，一是把新鮮蔬果擺到入口附近，二是增加新鮮蔬果的品項數 | 200 | CONFIRMED | — |
| 34 | 調整後的初期，整間超市的蔬果銷售增加；到第六個月效果變小、也沒那麼穩固；不能說效果一直都在 | `produce-early/n9by`、`produce-fade/sa7x`、`produce-not-lasting/vt5e`、說明欄第 3 段 | S4 Discussion 第一句：介入實施當下店級銷售增加，但效果的大小與穩健性在六個月追蹤期間減弱；摘要的三個時間點也是一路變小、後兩個的信賴區間跨過零 | 200 | CONFIRMED | — |
| 35 | 每個家庭有沒有多買，結果不確定；店賣得多不等於每家多買；不能說每個家庭吃得更健康 | `produce-household/3trh`、`6kx4`、`produce-not-health/itq8`、說明欄第 3 段 | S4 摘要：主要結果是家庭購買，第 3 與第 6 個月兩組的差距都沒有統計上的顯著差異；作者摘要說家庭層級的發現統計上不穩健 | 200 | CONFIRMED | — |
| 36 | 卡片「受訪者的說法 vs 研究測量到的事」：左欄牛奶、美國一次採訪、說的是理由；右欄蔬果區配置、英格蘭 3＋3 家與 36 家、整間超市的蔬果銷售 | `produce-compare-said`（卡片、`iad8`、`kgx6`） | S1、S3、S4（第 21、27、32 列） | 200 | CONFIRMED | — |
| 37 | 卡片「能說 vs 不能說」；兩項研究提供一條線索：配置和供應可能影響銷售 | `produce-compare-can`（卡片、`ju49`、`fnsn`）、`produce-clue/etb4` | S3、S4 的結論都用「可以／可能」的語氣；兩篇都是非隨機、多項同時調整 | 200 | CONFIRMED | — （「初期」對 S3 是保守的說法，見懷疑項 6） |
| 38 | 這兩項都是蔬果研究，不能拿來證明牛奶放後面是要你多買 | `produce-is-produce/um5j`、`produce-not-milk/vdqq`、`produce-question/rup6`、說明欄第 3 段 | S3、S4：沒有任何關於牛奶位置的內容 | 200 | CONFIRMED | — |
| 39 | 回答：在這幾個美國的採訪個案裡考量有兩種（看到更多商品；運送和存放要冷藏）；沒有分出比例；沒有能套用到全世界超市的單一原因；不推論台灣或日本 | `answer-chapter`（卡片、`8ajh`）、`4xrp`、`6nii`、`6q6p`、`tfat`、`e9mg`、`answer-big`（卡片、`higw`）、說明欄第 4 段 | S1（第 4、13、16、22 列）；查核包故事前提 | 200 | CONFIRMED | — （`tfat` 的語氣見懷疑項 5） |
| 40 | 意見與收尾：冷藏櫃在哪裡是看得到的事；要有人說明也要有人測量；先問三件事；去附近的超市當成觀察；留言題；訂閱 | `answer-opinion/th7p`、`8dbd`、`xnp8`、`sm9y`、`zif7`、`w6js`、`bsfc`、`outro` | `brief.md` 站主觀點與觀眾能做到的事 | — | OUT OF SCOPE | — （意見都有標，與站主觀點一致） |
| 41 | 說明欄第 3 段的數字：2021、3＋3、2026、36、18＋18、第六個月 | `youtube.description` | S3、S4（第 26、27、31、32、34 列） | 200 | CONFIRMED | — |
| 42 | 說明欄：第二季 B26；來源查核 2026-10-01、2026-10-10 重開來源頁面；插圖由 AI 生成、人物是泛稱角色 | `youtube.description`、`hook.data.tag` | 查核包（製作查核日期 2026-10-01）；今天各網址的結果 | 200 | CONFIRMED | — |
| 43 | 十個標籤與六個章名 | `youtube.tags`、各 `chapter` | 與內文一致 | — | CONFIRMED | — （`route-chapter` 的章名見懷疑項 1） |
| 44 | `sources[]` 四筆的標題、網址與 `checked_on` | `sources[0..3]` | 四個網址今天都是 200；頁面標題、節目名、日期與論文題目相符 | 200 | CONFIRMED | — （`checked_on` 已是 2026-10-10） |
| 45 | 查核包排除的東西沒有出現：1.71 個標準差、6,170 份、其他效果量與百分比、Wansink、Wegmans 店長引句、入口小冷藏櫃、台灣或日本的配置 | 全部 304 條（腳本列出每個數字） | 出現的數字只有 2014、2016、2021、2026、3、18、36、六個月、查核日期與卡片章號 | — | CONFIRMED | — |
| 46 | Shorts 第一支：兩個標題、說明欄、五景（採購的兩種說法、公關說冷鏈才是主因、沒有分出比例、位置不等於動機） | `shorts.json[0]` | S1（第 10、11、13、16、22 列） | 200 | CONFIRMED | — （歸屬都在句子裡；沒有排除的數字） |
| 47 | Shorts 第二支：兩個標題、說明欄、六景（試辦研究的調整、店級銷售增加、非隨機、較大型研究第六個月效果變小、不是牛奶、不能說更健康） | `shorts.json[1]` | S3、S4（第 26–35、38 列） | 200 | CONFIRMED | 第 2 景字卡隨第 28 列修改，其餘沒動 |

合計：47 列（涵蓋清單 304 條）。CONFIRMED 38、CHANGED 2（#18、#28）、NOT FOUND 1（#19，拿掉查不到的細節）、OUT OF SCOPE 6（#6、#9、#14、#20、#23、#40）。

## 摘要

- 查了 47 列（304 條抽出的字串）：確認 38、改了 2、查不到而拿掉的細節 1、不在範圍 6。沒有任何主張懸著：S1 的主張都落在今天讀到的 NPR Illinois 逐字稿上。
- 事實修改 3 處：`jbrq`（「一共有三件事」不是論文的計數，論文寫兩個介入項目、內文還列了別的改動，改成旁白自己的分法；Shorts 第二支的字卡跟著改）、`s5ua`（「有三個人提到」只算卡片上的三位，報導裡還有別人提到）、`basket-compare` 來源欄（逐字稿沒說公關受雇於 BJ's）。另有 1 處措辭：`3gc9` 把「公關說」寫進句子裡，事實沒變。
- 重點逐項：每個解釋都留著歸屬（經濟學者「他的解釋／照他的說法」、採購「他的回答／這位採購說」、公關「公關說／這也還是公司的說明」）；「記者沒有拿到研究」沒有被說成「沒有研究」（`v94b` 還明講了）；2016 年是重播；兩項研究都說了非隨機、多項同時調整、看的是店級銷售、較大型研究追蹤時變弱、不能證明牛奶位置或健康；沒有推論台灣、日本或所有超市；排除的數字在卡片、說明欄與兩支 Shorts 都沒有出現；標題的「常」在 `nus6`、`6az8` 與說明欄交代是報導的描述。
- 來源與企劃衝突：`brief.md` 選項 A 第 5 章寫「同時改了三件事」，S3 自己的計數是兩個介入項目（蔬果擺到更顯眼的位置；撤掉結帳區與對面端架的不健康食品），照來源處理成旁白的分法。大綱不受影響。
- 會過期的事實：沒有。S1 原入口（NCPR）仍是 403、NPR 主站逾時；兩篇論文頁今天沒有更正標記，上架前若隔了很久可以再看一次。
- 意見：`cuhv`、`ctpi`、`th7p` 以「我的看法是」開頭，`jbas`、`e9mg` 用第一人稱交代立場，都與 `brief.md` 站主觀點一致，沒有不符。
- 聽感（只報告）：沒有超過 40 字的句子（最長 21 單位）；沒有拉丁字母、括號或網址；沒有「經查證」類字眼。`b6gz`「節目頁面寫明」是在旁白裡引頁面；`nus6`「標題說」與 `c3p4`、`s5ua`、`iad8`、`kgx6`「卡片左邊／右邊是」要看著畫面才聽得懂。`produce-compare-can` 右欄四點在 `fnsn` 一次全亮，後三點（效果一直都在、每個家庭吃得更健康、牛奶放後面的動機）到後面三個鏡頭才唸到。
- lint：`node tools/video/cli.mjs lint --slug sothatswhy-b26` 0 錯誤、2 警告（開場章約 64 秒、outro 只有一句，都是原本就有的）；估 11.2 分鐘、144 句、2,215 個口語單位（改前 11.1 分鐘、2,208）。`shorts.json` 用 `tools/video/shorts/episode.mjs` 的 `episodeShortsProblems` 檢查，0 個問題。
- 懷疑但沒動：
  1. `route-chapter` 的章名「牛奶怎麼進超市：冷藏卡車、後門、冷藏室」與開場句 `ke2y`「你從前門進來，牛奶走的是另一邊」是沒有歸屬的直述，下一句才接「報導裡，有一位受訪的經濟學者」；後面有「這是他的解釋，不是每家超市的實際構造」收住。
  2. 原文只說後方（the back），旁白與卡片用了「後門」；「冷藏卡車」出自採購的話，經濟學者只說卡車。都落在標了「概念示意」的段落裡。
  3. 「沿路看到更多商品」（卡片、`xagr`、說明欄、Shorts 第一支）是意譯：採購說的是看到店裡賣的各種品項，記者的轉述是看到別的東西，都沒有「沿路」與「更多」這兩個詞；「把購物籃裝滿」是 building the basket 的意譯。
  4. 卡片把經濟學者的說法歸在「冷藏的理由」：他的重點是省事（easier），冷藏室是其中一環；記者自己在結語的二分是「比較省事」對「讓你走過整間店」。說明欄與答案卡的「銷售與冷藏」照查核包的寫法。
  5. `tfat`「也沒有一個原因，可以套用到全世界的超市」聽起來像對全世界下結論；來源能撐的是「這些來源沒有給出這樣的原因」。這是查核包故事前提的原句，沒有動。
  6. 「初期增加」用在兩項研究上是保守的講法：試辦研究在第 3 與第 6 個月都高於預測，變弱的是較大型的那一項。
  7. 試辦研究的調整是超市公司做的，研究團隊只是評估（摘要說介入的實施不在研究團隊的掌控內）；Shorts 第二支「英格蘭一項試辦研究，把蔬果區擴大、移到入口」主詞是研究，中文讀得通，沒有動。
  8. `produce-compare-said` 左欄「說的是理由，沒有測量」指受訪者的話，不是說世上沒有測量；與另一張卡的「不是測量結果」寫法不同。
  9. 說明欄沒有來源網址（查核包的草稿有）；`sources[]` 四筆都在，上架包若不會自動帶入要補。
  10. `basket-pr` 的畫面是發言人拿著電話，逐字稿沒說公關是怎麼聯絡記者的；屬插圖示意。
- 第二輪：依規則不需要（事實修改 3 處，沒有超過三處）。若仍要跑，請重查 #18、#19、#28 三處與 `3gc9` 的措辭，加上確認列的隨機三分之一。
