# 獨立查核：tech-news-apple-eu-business-terms-20260818

查核代理：未參與撰稿。查核日 **2026-09-17**（跨到 09-18 凌晨；文章的 `checked_on` 維持 **2026-09-17**，沒有改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；Newsroom 那頁另外重抓四次
比對 JSON-LD 與位元組數；研究紀錄的 verbatim_quote 以程式對原始 HTML 做四種正規化比對
（保留標籤內文／不斷行空格轉空白／標籤轉空白／壓縮空白）。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，也沒有猜任何識別碼。

檢查的主張：96 條（正文 15 段、摘要 4 句、FAQ 6 題的答句、callout、表格 4 列與 caption、
圖解 caption、title 與 description）。**改了 14 處**，另有 5 件留給站主。

## 重抓結果（四條都活著，都是正文）

| source | HTTP | bytes | body 是正文？ | 驗到的東西 |
| --- | --- | --- | --- | --- |
| developer.apple.com/news/?id=gmws0jgp | 200 | 111,532 | 是 | `August 18, 2026`；四項重點；`Some key updates, which go into effect October 1, 2026, include:`；CTF→CTC 那一句 |
| apple.com/newsroom/…/apple-announces-changes…/ | 200 | **162,779** | 是 | `datePublished": "2026-08-18Z"`、`dateModified": "2026-08-27T14:00:09Z"`；26/20/15/5 percent 四句；兒少保護**四**個項目；資格五項 |
| developer.apple.com/support/apps-in-the-eu/ | 200 | 142,113 | 是 | 三張費率表；CTC 三類交易；資格**七**項；兒少保護四段；`Digital Markets Act` 1 次、`DMA` 2 次 |
| developer.apple.com/support/payment-options-…-in-the-eu/ | 200 | 141,539 | 是 | 29 個國家代碼；iOS 26.2／26.6；揭露畫面；`audit rights` 1 次；`store services commission` 表 |

**Newsroom 那頁今天拿到的是另一個 edge 版本**：撰稿紀錄寫 162,927 bytes／`13:59:42Z`，
我四次重抓全部是 162,779 bytes／`14:00:09Z`。日期 `2026-08-27` 兩邊一致、秒不一致——
撰稿者「只寫日期不寫秒」的處置**正確**，文章也確實沒有印任何時刻，所以沒有時區換算問題。
但紀錄裡「四個位元組數與前次完全相同，代表頁面未變動」這個推論不成立，已改寫。

## 改掉的 14 處

1. **推翻：「Newsroom 只寫『未滿 18 歲』」**（第 3 節第 3 段）。Newsroom 的兒少保護有**四個**項目，
   其中就有 `For users under 13 years old, apps from the App Store cannot link out to websites for transactions…`
   與 `In EU member states that require parental consent for digital actions for children older than 13 years old,
   these protections will scale accordingly.`。撰稿紀錄只抄了第二項，據以寫成「支援頁較嚴格」。
   已改寫成「兩邊寫法不完全一致」，並把 Newsroom 的未滿 13 歲那條寫進去。
2. **刪除歐盟執委會新聞頻道那兩句**（第 1 節第 3 段、FAQ 第 1 題）。原稿寫「查到 9 月 17 日為止，
   最新一則與這次異動無關」——那個頻道**不在 `sources[]`**，撰稿紀錄自承當天沒抓，而且它是滾動視窗
   （修正清單第 45 行已經寫過「回溯不到 8 月」）。改成「本文四條來源都是 Apple 自己的頁面，
   沒有取得執委會的一手說明」。
3. **刪除「Apple 目前沒有繁體中文版的支援頁，中國大陸、日本與韓國語系頁面也仍沿用英文原文」**（第 5 節第 2 段）。
   四個語系網址不在 `sources[]`，紀錄也寫明當天沒抓、是沿用前一輪。改成「本文四條來源都是英文頁面」——
   這句話光靠 `sources[]` 就撐得住，中文名詞仍註明是編輯部自行翻譯。
4. **商店服務抽成掉了「附可點擊連結」這個要件，7 天限制又掛錯格**（第 2 節第 1 段、表格第 3 列、FAQ 2／3、摘要第 2 句）。
   原文：`The store services commission applies when your app uses an out-of-app offer **with an actionable link**…
   Only sales made within 7 days of the link tap are subject to this commission.`——7 天掛在整段（15% 與 10% 都適用），
   原表格只寫在 10% 那一格。**不帶可點擊連結的店外提案不在這筆抽成內**，原稿寫成「連到 App 外完成交易」會多收。
   另補上 apps-in-the-eu 對 15% 那列的排除語（`excluding transactions from program participants or
   auto-renewable subscriptions after their first year`），該排除語在 payment-options 頁沒有——表格建在前者就引前者。
5. **核心技術抽成漏一類、多一個目的地、免收範圍放大**（第 2 節第 2 段）。原文列三類，原稿只寫了第二、三類，
   漏掉最核心的 `Sales of digital goods and services **within** alternative app marketplaces…`；
   第三類原文是 `actionable links that open in a web browser **to a website**`，原稿寫成「網站或其他 App」。
   免收那一條原文是 `you qualify to have the CTC waived **on fees your EU marketplace app charges to download
   your alternative app marketplace, or subscription fees to access apps distributed by your…marketplace**`，
   原稿寫成「可申請免收這筆抽成」——既放大了範圍（不是整筆 CTC），又多了原文沒有的「申請」。
6. **替代市集與網站發布只做 iOS 與 iPadOS，原稿把六平台清單掛在這一節**（第 4 節第 2 段）。
   支援頁的段落標題是 `Core Technology Commission for **iOS and iPadOS** apps distributed outside of the App Store`，
   替代發布那節也是 `Alternative distribution on iOS and iPadOS`；六平台那一句
   （`specific business terms for iOS, iPadOS, macOS, tvOS, visionOS, and watchOS apps distributed in EU storefronts`）
   講的是**商店前台上架 App 的商業條款**。原稿寫成「這些安排只適用於…涵蓋 iOS…watchOS」，
   會讓讀者以為 macOS／watchOS 也能用替代市集。已拆成兩句寫。
7. **核心技術抽成的主體誤讀**（第 1 段、摘要第 1 句）。原文 `a simple 5% commission on digital transactions
   in apps **distributed** outside the App Store`——條件是「App 在哪裡發布」，不是「交易在哪裡完成」。
   原稿寫「App 在 App Store 以外完成數位交易的 5%」，已改成「在 App Store 以外通路發布的 App，其數位交易抽 5%」。
8. **刪掉「歐盟（歐洲經濟區）」四處**（摘要、第 5 節、FAQ 4、callout）。Apple 這四頁只有在 HCE 非接觸式交易
   那一段用 EEA（`Users based in the European Economic Area (EEA)`），商業條款一律寫 EU／EU storefronts。
   而且那份 29 個商店前台是歐盟 27 國加冰島、挪威，**列支敦斯登不在裡面**——所以既不等於歐盟，也不等於歐洲經濟區。
   冰島、挪威那句改成「兩國不是歐盟會員國」，不再宣稱清單等同某個法律區域。
9. **「多數重點／多數條款於 10 月 1 日生效」**（description、摘要、callout）。三頁的引導句是
   `Some key updates…include:`／`The primary updates…include:`，沒有「多數」；Newsroom 則寫
   `changes will go into effect on October 1`。已一律改成「主要更新」，並把「Apple 列出四項重點」
   改成「Apple 以『主要更新包括』帶出四項」，保住 `include` 的舉例性質。
10. **資格條件的結構錯了**（第 4 節第 1 段）。支援頁列的是**七項**、而且繫在
    `Starting October 1, 2026`；Newsroom 只列五項。原稿寫「Apple 列出五種情形，符合其一即可…支援頁另列兩項」，
    讀起來像五選一。已改成一份七項清單加「Newsroom 少了後兩項」。另外
    `venture funding from an **established** investment firm` 不是「知名創投機構」，改成「具規模投資機構的創投資金」；
    `have a legal entity **or be established** in the EU` 漏掉的後半段補回成「法律實體或據點」。
11. **兒少保護的範圍被收窄**（第 3 節第 3 段、FAQ 6、摘要第 3 句）。未滿 13 歲原文是
    `out-of-app offers are **not permitted**`（整類店外提案），不是「不能連到 App 外網站」；
    兒童類別 App 補回「替代付款流程須放在家長閘門後」那半句。摘要原本寫「13 至 17 歲**不論用哪一種付款方式**
    都要先通過家長閘門」——Apple 應用程式內購買不在其中，已改。
12. **「部分前台把門檻拉高…但未說明是哪些前台」講得太死**（第 3 節第 3 段、FAQ 6）。
    Apple 其實說明了觸發規則：`In cases where an EU storefront sets an age for parental consent above 13 years old,
    the same protections apply at the higher age instead of 13.`，並要開發者去查
    `Region-specific rules for managing an Apple Account`。已補上規則與指引，只保留「這一頁沒有列出是哪些前台」。
13. **揭露畫面的觸發條件與介面字串**（第 3 節第 1 段）。原文的條件是「App 內替代付款處理」**或**
    「用可點擊連結帶到店外提案」，不是「同時提供替代付款的 App」；顯示時機是使用者點下替代付款按鈕時
    （`showNotice when the user taps any alternative payment button`）。`External Purchases` 原稿翻成
    「外部購買」——四條來源都沒有中文對照，已改回英文原字串。12 個月鎖定補上原文的「在所有歐盟商店前台」。
14. **研究紀錄的 9 條 `verbatim_quote` 在來源頁搜尋不到，全部改掉**：
    `dateModified` 的秒級時間戳（今天四次都不是那個值，改用穩定的 `datePublished`）；
    四處把直引號 `'` 打成來源的彎引號 `’`（`DMA's`、`app's`×2、`they'll`）；
    四處用刪節號把**不相鄰**的段落接成一句（Report a Problem／Kids category／Web distribution／audit rights）。
    另外兩條把多個項目符號串成一句的引文（Developer News 四項、Newsroom 資格五項）已改成單一項目，
    其餘寫進 `fact`。`audit rights` 那句在原始 HTML 的 `Apple&nbsp;Developer`、`App&nbsp;Store` 是不斷行空格，
    已在 `fact` 寫明，免得下一個代理照抄後搜不到。

## 查過而且正確的部分（沒有動）

- **撰稿者自己標的三個疑點，兩個成立、一個是它想多了**：
  (1) `dateModified` 確實有兩個 edge 變體，日期穩、秒不穩，文章沒印時刻——處置正確；
  (2) 稽核權／抵扣／下架那一句**確實只在 payment-options 頁**（`audit rights`、`offset of proceeds`
  在該頁各 1 次、在 apps-in-the-eu 頁各 **0** 次），`must_fix 4` 的掛址修正成立，而且這段沒有寫進正文；
  (3) 「未滿 16 歲／16 至 17 歲」那句是**在來源頁原樣搜尋得到的連續字串**，而且兩份支援頁都有，
  掛在 apps-in-the-eu 正確。
- **抽成數字逐一核對無誤**：26%／15%、20%／10%、15%／10%、5%；12 個月、7 天、次月起 15 日內申報、
  1000 萬歐元／100 萬歐元、100 萬美元備用信用狀、首年 100 萬次安裝、
  iOS 26.2／iPadOS 26.2／macOS 26.6／tvOS 26.6／visionOS 26.6／watchOS 26.6。29 個國家代碼我自己重數也是 29。
- **日期沒有混用**：公告日 2026-08-18（三處來源一致）、頁面修改日 2026-08-27、生效日 2026-10-01，
  三個日期在文章裡分開寫；`news_date` 與 slug 尾碼都是事件日 2026-08-18；沒有任何自行推算的日期。
- **界線（tech.md）**：全文沒有購買或升級建議、沒有推薦式比價、沒有「該不該改用替代付款」的結論；
  Apple 的自述（與執委會化解歧見、公證、網站發布沒有持續監督、替代付款的取捨）全部歸因給 Apple；
  只有一個 callout，**沒有**投資免責段落。`must_not_write` 十三條逐條沒踩到，包括沒有寫舊比率、
  沒有寫 DMA「要求／迫使」、沒有把台灣寫成會跟進。
- **`sources[]` 之外的事實沒有外溢**（改掉第 2、3 點之後）：授權合約頁的 Attachment 14／Section 3.5、
  執委會新聞頻道、四個語系支援頁，一句都沒有進文章。四條 sources 全是 Apple 一手頁，沒有超過 4 條上限。
- **否定句都有範圍**：「這兩篇公告的全文都沒有出現…」「這四個頁面都沒有提到台灣或其他地區」
  「Apple 沒有在這一頁列出是哪些前台」——都限縮到具體文件。`Taiwan`／`Asia` 在四頁都是 0 次，我自己重查過。
- **摘要沒有多說**：四句的每個數字都在正文出現；FAQ 六題都是純文字、沒有連結；圖解四格與 hero_label
  的數字（5、2026、10、1）都在正文；全文沒有簡體字、沒有 Markdown 或條列。

## 留給站主的 5 件事

1. **`check_article.py` 仍是 FAIL，只剩索引那一條**（見下）。tech 垂直的索引內容包還不存在
   （`corrections-tech.md` 第 15 條說留給索引階段），查核代理只能動內容包與研究紀錄，所以沒有建立它。
   索引落地後，第一個 link 的 text 必須逐字換成索引自己的 zh-TW title。這條失敗在查核前後完全相同。
2. **15% 那一階有兩個官方版本**：Newsroom 寫 `For the vast majority of developers, **including** those in the
   …Program`（三個計畫是舉例），支援頁的費率表寫 `from participants in the …Program`（較窄）。
   正文與表格採支援頁並在 caption 標明依據哪一頁，但**沒有**用一句話寫出兩版差異——
   段落字數已經是 **2,995／3,000**，補一句就得從別處刪等量的字。這是編輯取捨，查核代理不代決定。
3. **統一條款的生效時點還有一個分支沒寫進正文**：舊的 Alternative Terms Addendum 與
   StoreKit External Purchase Link Entitlement (EU) Addendum 自 2026-10-01 起被 Attachment 14 取代；
   同意更新條款的開發者，帳號適用的時點是 `October 1, 2026, or the date they agree, **whichever is later**`。
   已寫進研究紀錄的 `verified_facts`，同樣因為字數沒有進正文。
4. **撰稿者問的兩條 must_add，我判定「不是非寫不可」**：
   - `Guideline 3.1.3(b) Multiplatform Services` 那條只對一小類 App 生效，一般讀者價值低；
   - reader app 那條**修正清單自己寫錯了**。原文是 `reader apps distributed in the EU **may** promote
     out-of-app offers…**without an actionable link**`——那是一項**許可**（可以不帶連結地宣傳），
     不是修正清單所寫的「不得放可點擊的連結」。照修正清單的字面寫反而會寫錯。要補請用原文那個讀法。
   兩條都記進研究紀錄的 `factcheck.left_for_the_owner`。
5. **Apple 對「公證」有兩種官方描述**：Newsroom 是「聚焦基本功能與防範重大威脅」，
   支援頁是 `focused on platform policies for security and privacy and to maintain device integrity`。
   正文採 Newsroom 版並歸因給 Apple，兩版差異只記在研究紀錄。

## 自檢

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
```

## 結論

`needs_owner`：文章經 96 條主張逐條核對後可刊，14 處已改（其中 6 處是事實層面的推翻或範圍錯誤，
其餘是限定詞、掛址與引文）。擋住 gate 的只有 tech 索引內容包還不存在，那不在查核代理可動的兩個檔案裡。
骨幹論述（誰被涵蓋、哪幾檔比率、何時生效、台灣不適用）沒有動，所以不需要第二輪。

---

## 第二輪

查核日 **2026-09-18**。第一輪改了 14 處、且多半改在費率的適用條件上，所以做第二輪。
**範圍不是整篇重做**：(a) 第一輪改動過的每一段與新寫進去的每一句，逐句回 `sources[]` 原文；
(b) 每一種費用連著它自己的全部要件，正文／表格／摘要／FAQ／標題／description／圖解 nodes 逐處比對是否一致；
(c) 適用平台、29 個商店前台、生效日、要不要主動同意；(d) 兒少保護四項兩邊各寫什麼；
(e) 執委會與 DMA 的歸因與範圍；(f) 40 條 `verbatim_quote` 全數重驗；(g) 回掃有沒有為了字數刪掉但書。

**覆核 71 條主張 ＋ 40 條引文，又改了 14 處。** 文章的 `checked_on` 仍維持 2026-09-17，沒有動。

### 重抓結果（四條全部重抓，與第一輪逐位元組相同）

| source | HTTP | bytes | 與第一輪 | body 是正文？ |
| --- | --- | --- | --- | --- |
| developer.apple.com/news/?id=gmws0jgp | 200 | 111,532 | 相同 | 是（`August 18, 2026`、四個項目符號、`Some key updates…include:`） |
| apple.com/newsroom/…/apple-announces-changes…/ | 200 | 162,779 | 相同 | 是（`datePublished "2026-08-18Z"`、`dateModified "2026-08-27T14:00:09Z"`，仍是第一輪那個 edge 版本） |
| developer.apple.com/support/apps-in-the-eu/ | 200 | 142,113 | 相同 | 是（三張費率表、CTC 三類交易、資格七項、兒少四段） |
| developer.apple.com/support/payment-options-…-in-the-eu/ | 200 | 141,539 | 相同 | 是（29 個國碼、揭露畫面、`Out-of-app offers.` 沒有排除語） |

字串普查：`Taiwan`／`Asia`／`gatekeeper`／`antitrust`／`fine` 在四頁都是 **0** 次；
`Digital Markets Act` 只在 apps-in-the-eu 出現（兩個段落）；`European Economic Area` 只在該頁的 HCE 段落。
正文所有否定句的範圍都對得上。

### 引文重驗：40 條，0 條搜尋不到

40 條 `verbatim_quote` 以五種正規化（原始 HTML／實體解碼／不斷行空格轉空白／標籤轉空白／標籤直接去除）
比對今天抓到的頁面，**全部命中**，`url` 也全在 `sources[]` 內——第一輪那 9 條修正經得起重驗。
六條（26%／20%／15% 三句、未滿 13 歲那句、國碼清單、揭露畫面）只在「標籤直接去除」那一版命中，
原因是原頁用行內粗體把 `Apple In-App Purchase`、`(at)` 這類字串包起來，去掉標籤後才是讀者看到的連續字串——
這是正確的比對法，不是瑕疵。第 31 條原本把兩個項目符號用 `; or ` 接成一句，已改成單一項目（見下 13）。

### 又改掉的 14 處

1. **第一輪自己把引導句掛錯了**（第 1 節第 1 段）。第一輪把「Apple 列出四項重點」改成
   **「Apple 以「主要更新包括」帶出四項」**——但文中列的四項是 **Developer News** 的四個項目符號，
   那一頁的引導句是 `Some key updates, which go into effect October 1, 2026, include:`。
   `The primary updates … include:` 是**支援頁**的引導句，而支援頁底下的四項是另一組
   （Unified business terms／Alternative payments／Child safety／Eligibility），第一項就不一樣。
   已改成「Apple 寫「部分重點更新」包括四項」，`Some` 與 `include` 兩個限定詞都保住。
2. **核心技術費掉了它自己的要件**（第 1 段、摘要第 1 句）。原文是
   `a per-install fee for developers who achieve **extraordinary scale**`，原稿只寫「原本按安裝次數計費的核心技術費」，
   讀起來像對所有開發者收。改成「原本**只對特殊規模開發者**按安裝次數計費的核心技術費」（不寫門檻數字，`must_not_write` 第三條）。
3. **核心技術抽成漏掉一種適用主體**（第 2 節第 2 段、FAQ 2）。5% 那一列的原文是
   `**Alternative app marketplaces**, apps distributed through them, or apps distributed via Web Distribution`——
   **替代市集本身也在內**。原稿只寫「透過替代市集或網站發布的 App」。已改成
   「替代市集本身與透過替代市集或網站發布的 iOS 與 iPadOS App」。
4. **核心技術抽成第三類交易掉了「在瀏覽器開啟」**（第 2 節第 2 段）。原文是
   `actionable links that **open in a web browser** to a website`。已補回。
5. **商店服務抽成的目的地被寫成「站外」**（第 2 節第 1 段、FAQ 3）。原文是
   `at a destination of your choice — **a website, an alternative app marketplace, or another app**`，
   三種目的地。「站外」會讓讀者以為只有網站——而核心技術抽成那一類**才真的只有 website**，兩者剛好被混成同一個字。
   正文改成「把使用者帶出 App」，完整三種目的地寫進**表格第三列與 FAQ 第三題**（這兩處不計入段落字數）。
6. **商店服務抽成 15% 的排除語掉了「自動」**（第 2 節第 1 段）。原文
   `excluding transactions from program participants or **auto-renewable** subscriptions after their first year`。
   「續訂超過第一年的訂閱」改成「滿一年後的自動續訂訂閱」。
7. **「新條款把 App Store 抽成依付款方式拆成三檔」把商店服務抽成算進 App Store 抽成**（第 2 節第 1 段、description）。
   支援頁把它列成獨立的 `Store services commission`，與兩張 `App Store commission` 表分開；
   文章自己的表格也是分開標的，只有這一句不一致。改成「新條款依付款方式訂出三檔比率」；
   description 的「App Store 抽成依付款方式分為…」同步改成「抽成依付款方式分為…」。
8. **表格第三欄的欄名套不住第四列**。原欄名是「小型企業／Mini Apps／影片夥伴計畫」，
   但第四列的免收要件是**小型市集業者**的兩項營收門檻，和那三個計畫完全無關，並排會讀成「計畫參與者可以免核心技術抽成」。
   欄名改成「較低比率或免收」，三個計畫名稱移進第一列的儲存格，第四列寫明
   「免收：小型市集業者的市集下載費與訂閱費，須同時符合兩項營收門檻」。
   第三列的項目也從「附連結」補回「附**可點擊**連結」。
9. **Newsroom 的未滿 18 歲那一項被放大**（第 3 節第 3 段）。原文是
   `use alternative payment processing or **link out to a website** for transactions`，
   正文寫成「連到 **App 外**」。研究紀錄第 24 條本來就寫對，是正文抄錯。已改回「連到網站」。
10. **`first annual installs` 被譯成「首年」**（第 4 節第 1 段）。原文
    `Have one million **first annual installs** worldwide.`——這是 Apple 自己的計量名詞，
    **不等於「第一年之內的累計安裝次數」**，而四條來源都沒有定義它。原稿寫「首年全球累計安裝次數達 100 萬次」，
    等於替 Apple 定義了一個它沒定義的詞。改成「全球「首次年度安裝」達 100 萬次」並加引號，研究紀錄同步。
11. **「這類名詞沒有 Apple 自己的中文譯名」是四條英文來源撐不起的否定命題**（第 5 節第 2 段）。
    那四頁只能證明**它們自己**沒有中文對照，證明不了 Apple 別處沒有譯名。
    第一輪把前半句改成「本文四條來源都是英文頁面」，這個否定命題卻留著。已改成「這類名詞**也**沒有中文對照」，
    範圍收回到前一句。
12. **研究紀錄 `verified_facts` 第 3 條仍留著第一輪已在正文推翻的誤讀**：
    「比率是 App 在 App Store 以外通路**完成**數位交易的 5%」。正文第一輪已改成「發布」，研究紀錄沒改。
    已改成「在 App Store 以外通路**發布**的 App，其數位交易的 5%」並附原文——
    否則下一個代理照抄研究紀錄就會把錯的版本寫回去。
13. **研究紀錄第 31 條的 `verbatim_quote` 把兩個項目符號接成一句**（`…local currency); or Have one million…`）。
    雖然壓縮空白後搜得到，它在頁面上仍是兩個元素。已改成只取第二個項目
    `Have one million first annual installs worldwide.`，第一項的原文移進 `fact`。**現在 40 條引文每一條都是單一頁面元素。**
14. **摘要與 callout 的範圍字**。摘要第 4 句與 callout 的「Apple 的公告沒有提到《數位市場法》」
    改成「Apple 的**兩篇**公告…」，與正文第 1 節第 3 段一致（apps-in-the-eu 確實提了兩個段落）；
    摘要第 2 句補上商店服務抽成的 **7 天**限制，FAQ 第 2 題同步。

### 標題站不站得住：**站得住**

- **「核心技術抽成 5%」**：Developer News `a simple 5% commission`、Newsroom `a simple 5 percent commission`、
  支援頁費率表 `5%`，三處一致，而且 CTC **沒有第二檔比率**。唯一的但書是小型市集業者的免收，
  那是免收、不是另一個比率，內文與表格都寫了。
- **「可同時用替代付款」**：Newsroom `developers can now offer Apple In-App Purchase alongside alternative
  payment options, which had not previously been permitted in the EU`、支援頁
  `Apps distributed in EU storefronts can now offer alternative payment methods and offers alongside Apple
  In-App Purchase`。兩處都撐得住，範圍（歐盟）由標題前半的「歐盟新版 App 商業條款」帶住。
- 建議**不要改**。唯一可挑的是「可同時用」讀起來像已經生效，而這一項其實是 10 月 1 日才生效的四項之一——
  但標題開頭是「Apple **公布**」，框在公告層次；摘要、callout、description 三處都寫了生效日。
  （標題被別篇的連結逐字引用，我也沒有動它。）

### 查過而且正確的部分（沒有動）

- **第一輪最重的三處改寫今天再核一次都成立**：商店服務抽成需要「附可點擊連結」、且 7 天限制掛在整段
  （兩份支援頁的引導句逐字相同）；15% 那一列的排除語**只在** apps-in-the-eu，payment-options 的同一列今天仍只寫
  `Out-of-app offers.`；核心技術抽成的條件是「App 在哪裡發布」不是「交易在哪裡完成」。
- **四種費用的要件逐處一致**（正文／表格／摘要／FAQ／description 五個地方比對）：26%／15%、20%／10% 的
  「計畫參與者＋滿一年後自動續訂」；15%／10% 的「附可點擊連結＋7 天」；5% 的三類交易與免收的兩項門檻。
- **資格條件**：支援頁七項、Newsroom 五項的落差，`nonprofit approved for a fee waiver`、
  `or be established in the EU`、繫在 `Starting October 1, 2026`，以及替代市集與 Web Distribution
  兩節的七項條件逐字相同——全部重核無誤。
- **適用平台的兩層**仍然正確：六平台那一句在 `Payment options on the App Store` 段落下（歐盟商店前台的商業條款），
  替代市集與網站發布的兩個段落標題都限定 iOS 與 iPadOS。
- **29 個商店前台**今天重數仍是 29（歐盟 27 國加冰島、挪威），列支敦斯登不在其中；
  全文沒有出現「歐洲經濟區」。**全文沒有一句讓台灣的開發者或使用者變成適用對象**：
  第 5 節與 FAQ 4 都把判斷依據寫成「App 在哪個商店前台販售」。
- **兒少保護**：支援頁三項與較高年齡的觸發規則，兩份支援頁逐字相同。Newsroom 的第四項
  （`In EU member states that require parental consent for digital actions for children older than 13 years old`）
  與支援頁的「商店前台」版本是**兩種不同的觸發寫法**；正文只採支援頁那一版並歸因為「Apple 另說明」，
  沒有把兩者混成一句，也沒有宣稱 Newsroom 只有三項——判定**不是錯**，只是沒寫進去（見留給站主第 2 條）。
- **執委會與 DMA 的歸因**：`Apple’s disagreements with the Commission` 歸給 Apple；
  「本文四條來源都是 Apple 自己的頁面，沒有取得執委會對這次異動的一手說明」出現在第 1 節第 3 段**段尾**與 FAQ 1 **答尾**，
  兩處都緊接在 DMA 那段之後，範圍清楚。
- **沒有為了字數刪掉但書**：第二輪淨減 3 個字（2,995 → **2,992**）。刪掉的三處都是冗詞
  （「把 App Store 抽成」「原本獨立計費的」「沒有 Apple 自己的中文譯名」），每一處刪減都同時補進更精確的條件。
- **`summary` ⊆ 正文、FAQ ⊆ 正文**：四句與六題的每個說法都能在正文、表格或 callout 找到對應，
  數字全部出現在正文；FAQ 仍是純文字；圖解四格與 `hero_label` 的數字（5、2026、10、1）都在正文。
- **界線（tech.md）再掃一次**：沒有購買或升級建議、沒有推薦式比價、沒有「該不該改用替代付款」的結論；
  Apple 的自述全部歸因；只有一個 callout，沒有免責段落。

### 留給站主的事（第一輪那 5 條全部仍然成立，另加 2 條）

第一輪的 5 條（索引尚未建立、15% 有兩個官方版本、「與同意日取其晚」沒進正文、兩條 `must_add` 判定不是非寫不可、
公證有兩種官方描述）第二輪全部複查過，結論不變。新增：

6. **`Members of the Apple Developer Program can review and agree…`**——原文限定的是**計畫會員**，
   正文第 1 節寫的是「開發者」。改成「Apple Developer Program 會員」要 +23 字，而段落只剩 8 個字的空間；
   同一句已經點名《Apple Developer Program 授權合約》，判定不至於誤導，但站主若要精確可自行擴寫。
7. **Newsroom 兒少保護的第四項沒有寫進正文**（會員國版的家長同意年齡調整）。正文採的是支援頁的「商店前台」版本，
   兩者是不同的觸發條件。要並列兩版約需 +26 字，同樣卡在字數。這是編輯取捨，不是錯誤。

### 自檢

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
```

（第二個結尾連結的目標 `tech-news-eu-cra-reporting-20260911.json` 現在已經存在，link text 也與該篇的 zh-TW title
逐字相同，所以第一輪報告裡的第二條 FAIL 已經自己消失；只剩索引那一條，兩個結尾連結我沒有動。）

### 結論

`needs_owner`：又覆核 71 條主張與 40 條引文，改了 14 處，**全部是限定詞、適用主體、掛址與引文**——
沒有一處動到骨幹論述（誰被涵蓋、哪幾檔比率、何時生效、台灣不適用），標題的兩個說法也都站得住，
所以**不需要第三輪**。擋住 gate 的仍然只有 tech 索引內容包尚未建立，那不在查核代理可動的兩個檔案裡。
