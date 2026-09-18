# 獨立查核：tech-news-apple-att-eu-20260916

查核代理：未參與撰稿。查核日 **2026-09-18**（文章與研究紀錄的 `checked_on` 本來就是 2026-09-18，
與我重抓的日期相同，未改）。批次 4.5 沒有前期修正清單，`corrections_applied` 維持 `[]`。

查核方式：`sources[]` 兩條當天以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
把文章拆成 **84 條主張**逐條回原文比對（正文 18 段約 46 句、summary 4 句、FAQ 6 題答句、
callout、表格 12 格與 caption、圖解 caption、title、description）。
研究紀錄的 `verbatim_quote` 以程式在該頁**原始 HTML** 全部重搜一次。
改了 **26 處**（歸納成下面 18 條），另有 4 件留給站主。

為了反駁而讀、但**沒有進 `sources[]`** 的官方網址：`developer.apple.com/news/rss/news.rss`、
`developer.apple.com/tw/news/?id=idsft9ai`、`developer.apple.com/tw/news/`、
`developer.apple.com/tw/app-store/user-privacy-and-data-use/`、`/jp/` 與 `/cn/` 的同一篇、
說明頁自己嵌的 `screen-att-eu-sheet-medium_2x.png`。沒有猜任何識別碼或網址。

## 重抓結果（兩條都還在、內容沒變）

| source | HTTP | bytes | body 是不是正文 |
| --- | --- | --- | --- |
| developer.apple.com/news/?id=idsft9ai | 200 | 106,682 | 是。`<h2 class="article-title">`＋`<p class="lighter article-date">September 16, 2026</p>`＋`<div class="article-text">` 裡**一個** `<p>`，後面只有一個 Learn more 連結 |
| developer.apple.com/app-store/user-privacy-and-data-use/ | 200 | 131,579 | 是。含 `ATT in the European Union` 一節（3 段＋1 張圖＋4 個文件連結）與 17 則常見問答 |

位元組數與研究紀錄**逐字相同**，可視為同一版本。兩頁的不斷行空格存法不同，逐字搜尋要分開處理：
`news.html` 有 **23 個 U+00A0 字元、1 個 `&nbsp;` 實體**，`privacy.html` 有 **0 個 U+00A0、18 個 `&nbsp;` 實體**。

**13 條 `verbatim_quote` 全部在該頁原始 HTML 命中（13/13）**，包含刻意保留 `iOS&nbsp;14.5` 的那一條與標題的 U+00A0。
本批科技 13 篇裡有 9 篇引文欄位靠不住，這一篇是例外，撰稿者的三個提醒（設定名、條號空格、`&nbsp;`）我逐條複驗，**全部成立、一個都沒有動**。

## 改掉的 18 條（共 26 處）

1. **「Apple 沒有附圖」不成立**（第 2 節、第 5 節、FAQ 第 3 題，三處）。說明頁在歐盟那一段**右邊就嵌著一張畫面圖**：
   `<img src="/app-store/user-privacy-and-data-use/images/screen-att-eu-sheet-medium_2x.png" width="100%" alt="" aria-label="">`，
   放在 `device-iphone-16-pro-titanium` 的手機外框裡；該網址單獨抓是 **200、66,000 bytes、image/png**。
   研究紀錄自己的 `unverified_or_excluded` 第 1 條也寫了這張圖，文章卻寫成沒有。
   三處都改成「Apple 沒有用文字寫出完整文案；說明頁在這一段旁邊嵌了一張畫面圖，本文不描述介面畫面」。
2. **「兩個頁面沒有看到能夠對應到特定機關或法規的文字」不成立**（第 5 節第 1 段）。說明頁的常見問答有一則專寫歐盟：
   `Can I provide additional information and consent controls with my app’s ATT prompt implementation, to comply with local privacy laws in the European Union, such as ePrivacy or GDPR?`
   `GDPR` 與 `ePrivacy` 在 `privacy.html` 各出現 1 次，都在這一則。已改成 Apple 沒有說**這次調整**依據哪一部法律，
   並寫出那則問答的脈絡（是開發者遵循當地隱私法的工具，不是調整的依據）。`summary` 第 4 句與 callout 同步改。
   （`DMA` 與 `Digital Markets` 兩頁仍是 **0 次**，`must_not_write` 的禁令沒有被踩到。）
3. **「頁面也沒有提到 macOS、tvOS、watchOS 或 visionOS」不成立**（第 1 節第 2 段）。這四個字在新聞頁的**全站導覽**裡全都有，
   `tvOS` 更直接出現在說明頁正文的 `In iOS&nbsp;14.5, iPadOS&nbsp;14.5, and tvOS&nbsp;14.5 or later`——
   而文章第 4 節自己就引了那一句，前後矛盾。已限縮成「這段調整也只寫這兩個系統，沒有說 macOS、tvOS、watchOS 或 visionOS 會不會比照」。
4. **「Apple 目前只發布英文版公告」「Apple 還沒有發布這則公告的繁體中文版本」刪掉**（第 3 節、第 5 節）。
   依據是 `/tw/news/?id=idsft9ai` 回 404——但那**不是軟性 404，是真的 404 狀態碼**，而且
   `developer.apple.com/tw/news/` **整個路徑就回 404**（81,978 bytes），`/jp/` 與 `/cn/` 的同一篇則是 200 但 302 落到
   英文的 `developer.apple.com/news/` 列表頁（504,440 bytes）。**Apple Developer News 根本沒有語系化的單篇網址**，
   這個 404 撐不起那個否定句（BRIEF 型態 6：從沒落地的網址取負面證據）。
   已改成只寫可驗證的部分：「本文讀到的兩個頁面都是英文，兩頁都沒有給這兩個名稱的中文寫法，所以中文說法是本站翻譯」。
   順帶把「不是 Apple 官方用語」也拿掉——iOS 介面有沒有官方中文字串不在這兩條來源的範圍內。
5. **「在大多數歐盟國家是開發者可以自行選擇」是自己數出來的**（第 2 節）。來源沒有印歐盟有幾個會員國，
   「大多數」是 27 減 5 的推論（BRIEF 型態 9，和 ENISA 那個「自己數的 27 國」同型）。
   已改成「在這五國以外的歐盟國家，要不要改用新版是開發者自己的選擇」，並補上「Apple 也沒有說為什麼是這五個國家」。
6. **Additional Information 按鈕的主詞錯了**（第 2 節）。原文是
   `provides **you** the option to use a text button ... This allows **you** to surface additional information about **your** request`——
   是開發者去說明，不是 Apple 顯示更多說明。原稿「按下之後可以看到更多說明」已改成「這個按鈕讓開發者進一步說明自己的請求」。
7. **補進兩條來源真的寫了、原稿漏掉的事**（第 2 節新增一段）。同一則歐盟問答還寫：按鈕可以
   `surface additional information **and more granular consent controls**`，內容 `are entirely your responsibility`；
   而且 `**you cannot access the device’s advertising identifier** ... until the user has granted your app permission in that prompt`。
   最後這句對讀者最有用（多一個按鈕不等於多一條繞過詢問框的路），原稿完全沒有。
8. **「歐盟多了一項既有規則沒有的彈性」是對舊規則的斷言**（第 3 節）。來源只寫
   `In addition, for users in the European Union, you can reprompt ...`，沒有寫歐盟以外的舊規則是什麼
   （`reprompt`／`re-prompt` 全頁各 1 次，都在歐盟那一段；`once` 唯一一次是講廣告識別碼何時回傳，與次數無關）。
   已改成「同一段還寫了一項只給歐盟的彈性」，並補一句「說明頁沒有寫歐盟以外能不能這樣再問一次」——這正是表格那一格的依據。
9. **表格「Additional Information 按鈕／歐盟以外：沒有」改成「不適用」**。那個按鈕是新版詢問框的一部分，
   而新版只存在於歐盟；頁面沒有寫「歐盟以外沒有這個按鈕」。
10. **表格「裝置設定名稱／歐盟以外：允許 App 要求追蹤」改成來源印的英文** `Allow Apps to Request to Track`，
    歐盟兩欄的「改名後名稱」改成「已改名，見內文」。原本的中文名沒有任何標示，讀起來像官方名稱。
    caption 同步改成「兩個頁面都是英文，設定名稱照英文原文列」。
11. **FAQ 第 2 題的方向反了**。原稿「App 不能因為使用者拒絕而關閉其他功能」，而 5.1.2(i) 那一則問的是
    `Can I gate functionality on agreeing to allow tracking`——禁止的是「以同意換功能」。已改回來源的方向。
12. **「能不能跳過詢問框」不是來源說的**（第 2 節）。來源是
    `The requirements for when you must seek permission to track users will remain the same`，已改成「什麼時候必須取得使用者許可」。
13. **「這個定義在歐盟與其他地區相同」改成可驗證的寫法**（FAQ 第 1 題）：「這個定義寫在說明頁一般性的段落，不在歐盟那一節裡」。
14. **「Apple 在頁面上重申」改成「說明頁的常見問答寫明」**（第 4 節第 3 段）。那兩條在常見問答裡本來就有，
    不是 Apple 因為這次調整而重申；段末「沿用既有的審查指南」也改成「9 月 16 日那則公告沒有提到這兩條」。
15. **「也沒有因為新版詢問框而改變」改成「公告也沒有說它改了」**（第 4 節第 2 段）。來源沒有對廣告識別碼歸零這條說它變或沒變。
16. **「標示新增等於在說……不是把舊版詢問框換個顏色而已」的後半刪掉**（第 3 節第 3 段）。那是沒有來源的畫面評論。
17. **`description` 與 `summary` 的「同時改名」改成「也改名」**。Apple 沒有寫改名的時點，「同時」會被讀成跟 27.2 綁在一起。
18. **研究紀錄**：新增 5 條 `verified_facts`（歐盟版問答的 ePrivacy／GDPR、按鈕可提供更細同意選項、未取得許可不得取得廣告識別碼、
    內嵌的畫面圖、四份文件清單——原稿引用了四份文件卻沒有對應的 fact）；改寫 `not_said` 第 1、5 條與
    `unverified_or_excluded` 第 3 條的 `seen_where`；`sourcing_notes` 記下 `/tw/` 404 的真正意義、兩頁 `&nbsp;` 存法的差異；
    新增 `factcheck` 欄位。

## 查過而且正確的部分（沒有動）

- **骨幹全部成立**：五國名單逐字正確（`Germany, France, Italy, Poland, and Romania`，就是五個）；
  `Beginning with iOS 27.2 and iPadOS 27.2`；設定改名的兩個名稱逐字正確；
  「一年後可再問」與「關掉設定就不會被再問」都照來源；「必須取得許可的情形不變」有引文。
- **`you can reprompt` 一律寫成給開發者的許可**，全文沒有一句寫成使用者一定會被再問（`must_not_write` 第 6 條）。
- **版本號沒有被換算成日期**，全文沒有任何推測的上市月份（`must_not_write` 第 3 條）。
- **條號的排版差異照來源保留**：`5.1.2(i)` 無空格、`5.1.1 (iv)` 有空格，兩種寫法在來源各自存在，**不是筆誤，沒有被統一**。
- **`iOS 14.5／iPadOS 14.5／tvOS 14.5` 的起點**與 `advertising identifier value will be all zeros` 兩條與來源一致。
- **台灣的寫法正確**：兩頁 grep「台灣」「Taiwan」各 **0 次**；文章只寫官方公告未提及台灣，沒有預測台灣會不會改。
- **一個數字都沒有被捏造**：兩頁只有 `img` 的 `width="100%"`，沒有任何同意率、拒絕率或廣告成效數字，文章也明寫比不了。
- **界線乾淨**：沒有購買建議、沒有推薦式比價、沒有機型或價格比較、沒有攻擊細節、**沒有投資免責 callout**（科技垂直不帶，只有一個 callout）；
  廠商說法一律「Apple 說明／表示／寫明」。
- **與既有文章不矛盾**：`tech-news-apple-eu-business-terms-20260818` 管的是歐盟商業條款與抽成、Apple 在那篇說的對象是歐盟執委會；
  這篇沒有把兩件事說成同一份和解，也沒有互相覆蓋的事實。第二個結尾連結的 text 與該包 zh-TW `title` 逐字相同。
- **事件日三處一致**：slug 尾碼、`news_date`、正文第一段都是 2026-09-16，依據是公告頁自己印的 `September 16, 2026`。

## 留給站主的 4 件事

1. **時區**：RSS 的 `pubDate` 是 `Wed, 16 Sep 2026 10:00:11 PDT`，換成台北時間是 **2026-09-17 凌晨 1 點**。
   文章採用 Apple 頁面印出的 9 月 16 日（與 slug、`news_date` 一致），換算只記在 `event_date_basis`。
   要不要在正文補一句「台北時間為 9 月 17 日凌晨」是編輯決定，查核代理不代決定。
2. **設定的中文名**：本文兩條來源都是英文，所以「允許 App 要求追蹤」寫成本站翻譯。
   iOS 繁體中文介面可能本來就有官方字串，但那要**另外加一條來源**才寫得了，本次沒有加。
3. **與 08-18 那篇的一處張力**：本文寫「Apple 沒有說明『在歐盟散布的 App』怎麼判定」，
   而 `tech-news-apple-eu-business-terms-20260818` 依它自己的來源寫商業條款是看商店前台。
   兩篇來源不同、主題不同，不衝突；若站主希望讀者不誤會，可在編輯階段加一句互相對照。
4. **`hero.alt` 與圖解 `alt` 未動**（依規格由協調者依實際畫面改寫）；圖解四格與 caption 內容未變，圖上沒有數字。

## 自檢

```
OK tech-news-apple-att-eu-20260916 zh-TW paragraphs 2817
```

沒有任何 FAIL：批次 4.5 的索引與第二個連結目標都已存在，規格允許保留的那兩條這次不適用。
段落字數 2,817（查核前 2,640），仍在 1,800–3,000 內；沒有為了湊字數刪掉任何但書或限定詞。

## 結論

`needs_second_round`。骨幹（五國、27.2、設定改名、一年再問、沒有改變的三件事）逐條成立、一字未動，
但事實面改了超過十處，而且**第 2 節有一段是我從來源新開出來的內容**（歐盟版常見問答：更細的同意選項、
內容由開發者負責、未取得許可不得取得廣告識別碼）——那一段沒有第二個人看過。
第二輪只要覆核第 2 節新增的那一段、第 5 節第 1 段的 ePrivacy／GDPR 說法，以及第 3、5 節關於「兩個頁面都是英文」的改寫即可，
其餘部分本輪已逐條比對過原文。

## 第二輪

第二輪查核代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-09-18**（與第一輪同日重抓，`checked_on` 未動）。

兩條來源自行以 `curl -sL -A "Mokaair-editorial"` 重抓：`news` **200／106,682 bytes**、
`user-privacy` **200／131,579 bytes**，與第一輪報告及研究紀錄的位元組數逐字相同，是同一版本。
從 `privacy.html` 原始 HTML 切出「ATT in the European&nbsp;Union」整節（`h2` 起至下一個 `h2` 止，3,467 bytes：
3 段正文＋1 張內嵌圖＋4 個文件連結）與常見問答整段，程式切出 **17 則問答**逐則讀過（第一輪說 17 則，複點相符）。
覆核第一輪改動過的每一段與新寫的每一句，共 **31 條主張**，另加指派訊息點名的 8 個疑點。
**20 條 `verbatim_quote`（第一輪 18 條＋本輪新增 2 條）全部以連續字串命中原始 HTML，20/20**，
每條的 `url` 都在 `sources[]` 內。又改了 **6 處**（4 處在內容包、2 處在研究紀錄）。

為了反駁而讀、**沒有進 `sources[]`** 的網址只有兩個，都是複驗第一輪的數字：內嵌的
`screen-att-eu-sheet-medium_2x.png`（200、66,000 bytes、`image/png`）與 `developer.apple.com/news/rss/news.rss`（200）。
沒有猜任何識別碼或網址；所有請求只帶 `Mokaair-editorial` 這一個 UA，沒有任何 email 或個人資料。

### 又改的 6 處

1. **第 1 節第 1 段：`As part of agreements` 被寫成時間先後。** 原文
   `As part of agreements with select European competition authorities, Apple is introducing changes to its App Tracking Transparency framework in the European Union.`
   寫的是這些調整**屬於協議的一部分**，不是「達成協議**之後**才做的調整」。
   已從「Apple 表示這是『與部分歐洲競爭主管機關達成協議』**後的調整**」改成
   「Apple 表示**這些調整是**『與部分歐洲競爭主管機關達成的協議』**的一部分**」。
2. **同一句的否定範圍沒有限縮。** `summary` 第 4 句、callout、第 5 節第 1 段在第一輪都已改成「沒有說**這次調整**依據哪一部法律」，
   只有第 1 節這一處還寫「也沒有**指出依據的是**哪一部法律」。已補上「這次調整」，四處寫法一致——
   這正是指派訊息疑點 (b) 要求的限縮，第一輪漏了一處。
3. **第 2 節第 1 段掉了 `collected from your app`。** 來源兩處都寫
   `link user or device data collected from your app with user or device data collected from other companies’ apps…`，
   原稿「把使用者或裝置資料，和其他公司…串連」沒有限定第一份資料的出處，讀起來比 Apple 寬。
   已改成「把**自家 App 蒐集到的**使用者或裝置資料」；FAQ 第 1 題本來就寫「把它蒐集到的」，改後兩處一致。
4. **第 2 節新增段（第一輪自己新開、沒有第二人看過的那一段）掉了兩個限定詞。** 第 17 則問答寫的是
   `to surface additional information and more granular consent controls **to comply with local privacy laws or other applicable legal requirements**`，
   以及 `…are **entirely** your responsibility`。原稿兩個限定都沒寫。
   已補成「**為了遵循當地隱私法等法律要求**提供更細的同意選項」（用「等法律要求」避免把
   `or other applicable legal requirements` 寫成封閉清單）與「**完全**由開發者自己負責」。
5. **同一段只引了 `cannot access` 那句的前半。** 來源是
   `you cannot access the device’s advertising identifier, **or otherwise collect and use device or user data from your app as described in the App Tracking Transparency system prompt**, until the user has granted your app permission in that prompt.`
   原稿只寫「不能取得裝置的廣告識別碼」，撐不起緊接著的結論句「多一個按鈕不等於多一條繞過詢問框的路」——
   那句結論講的是整個詢問框，不只是廣告識別碼。已補上「也不能依詢問框所述蒐集、使用 App 的使用者或裝置資料」，
   結論句因此完全落在同一則問答的引文範圍內。
6. **研究紀錄兩處自相矛盾／與原始 HTML 不符。**
   (i) `must_not_write` 第 9 條仍寫著「Apple 沒有發布這則公告的繁體中文版（`/tw/` 404）」，
   而同一份紀錄的 `not_said` 第 5 條在第一輪已認定這個 404 撐不起該否定句——理由已改寫成
   「兩個來源頁面都是英文、都沒有給中文寫法」，禁止自創譯名的規則本身不變。這是整份紀錄裡唯一殘留的那個錯誤前提。
   (ii) 第 13 條 fact 寫「`<div class="article-text">` 裡**一個** `<p>`」，實際上該 div 裡有**兩個** `<p>`，
   第二個只放 Learn more 連結。已照原始 HTML 改正；正文「公告正文只有一段」的說法不受影響，未動。

另在研究紀錄新增 2 條 `verified_facts`：`Tracking refers to the act of…`（FAQ 第 1 題「定義在一般性段落」那句在第一輪
改寫後沒有留下對應的 fact）與 `…are entirely your responsibility`。

### 指派訊息點名的 8 個疑點，逐條結果

- **(a) 第 2 節新增段逐句對 `ATT in the European Union` 節與 17 則問答**：三件事全部出自**第 17 則**問答同一則
  （更細的同意選項與用途限定、`entirely your responsibility`、`However, you cannot access…until the user has granted`），
  不是把不同段落拼在一起，主詞與方向都對。兩個限定詞已補（第 4、5 條）。
- **(b) ePrivacy／GDPR**：`privacy.html` 各 **1 次**、`news.html` 各 **0 次**，都在第 17 則問答的**題目**裡，
  寫法是 `such as ePrivacy or GDPR`；正文用「舉的是」呈現，沒有寫成完整清單。
  `DMA` 與 `Digital Markets` 兩頁仍是 **0 次**，文章全篇也是 **0 次**。正文四處都已限縮到「這次調整」。
- **(c) 「兩頁都是英文」的改寫**：全篇 grep `繁體中文`／`中文版`／`英文版`／`只發布`／`尚未`／`還沒` 皆 **0 次**，
  沒有任何一句仍靠 `/tw/news/?id=` 的 404 撐否定；第 3、5 節都只寫「本文讀到的兩個頁面都是英文」。
- **(d) 「沒有附圖」的三處**：第 2 節與 FAQ 第 3 題都寫「沒有用文字寫出完整文案／該段旁邊嵌了一張畫面圖／本文不描述介面畫面」；
  第 5 節第 2 段寫的是「沒有用**文字**寫出完整文案」，限定在文字，沒有再次否定圖的存在——三處互不矛盾。
  EU 那一節確實只有一張 `<img>`，FAQ 的「只…一張」成立。
- **(e) 三件複驗成立的事**：一個字都沒有動。`Allow Apps to Request to Track` 與
  `Allow Apps to Request to Link Your Activity Across Companies` 逐字相同；
  `5.1.2(i)` 無空格、`5.1.1 (iv)` 有空格照來源分開保留（程式複點：`5.1.2 (i)` 與 `5.1.1(iv)` 兩種相反排版在來源各 0 次）；
  `iOS&nbsp;14.5` 只以實體存在（`"iOS 14.5"` 一般空白版本 0 次），研究紀錄的引文原樣保留。
- **(f) 版本號／`reprompt`／台灣**：`27.2` 全文 10 次都只當版本號（`上市`、`月起` 各 0 次，沒有任何推測月份）；
  `you can reprompt` 在第 3 節與 FAQ 第 5 題都明寫成「給開發者的許可」；
  兩頁 `Taiwan`／`台灣` 各 **0 次**，文章只寫「官方公告沒有涵蓋台灣」並明說不能理解成台灣會或不會跟進。
- **(g) 日期**：slug 尾碼 `20260916`、`news_date` `2026-09-16`、正文第 1 段「2026 年 9 月 16 日」三者一致，
  依據是公告頁自己印的 `September 16, 2026`。RSS `pubDate` 複驗仍是 `Wed, 16 Sep 2026 10:00:11 PDT`（台北 9/17 01:00），
  只留在 `event_date_basis`；正文 grep「台北」**0 次**，沒有自行加上台北時間。
- **(h) 字數**：查核前 2,817 → **2,881**，仍在 1,800–3,000 內。本輪**只加字**，沒有為了字數刪掉任何但書、限定詞或歸因。

### 界線與連結（複掃）

`topics` 只有 `tech`／`tech-news`、不帶 `finance`；只有**一個** `info` callout、沒有投資免責段落；
沒有購買建議、沒有推薦式比價、沒有機型或價格比較、沒有規避追蹤的操作教學；
廠商說法一律「Apple 表示／說明／寫明」；`27.2` 一律寫成版本號，沒有把預告寫成已生效。
`summary` 四句、FAQ 六題答句、callout、表格四列與 caption、圖解四格與 caption 都能在正文找到對應，圖解四格沒有數字。

兩個結尾連結**都沒有動**：第一個逐字等於索引現行標題；第二個以程式比對逐字等於
`tech-news-apple-eu-business-terms-20260818` 內容包的 zh-TW `title`（`True`）。
**本篇 `title` 未改**，同批 `tech-news-app-store-bundles-multiseat-20260916` 指回本篇的第二個連結仍然逐字相符（`True`），
協調者不需要為本篇改動任何相關文章。

### 留給站主的事

第一輪那四件本輪全部複驗、結論不變（RSS 台北時間要不要進正文、設定中文名要不要另加來源、
與 08-18 那篇的張力要不要加一句對照、`hero.alt` 與圖解 `alt` 由協調者改寫）。本輪另加一件，純屬文字風格、不影響事實：
第 3 節寫「文中出現的中文說法（例如「允許 App 要求追蹤」）是本站翻譯」，
但第一輪把表格那一格改成英文之後，這個中文說法在全篇只剩這個括號裡出現一次；句子沒有錯，若讀起來繞可在編輯階段調整。

### 自檢

```
OK tech-news-apple-att-eu-20260916 zh-TW paragraphs 2881
```

沒有任何 FAIL。批次 4.5 的索引與第二個連結目標都已存在，規格允許保留的那兩條這次不適用。

### 結論

`ok`。第一輪新開的那一段經第二人逐句回原文，方向與主詞都對，但掉了兩個限定詞與半句話，已補回；
另外抓到第一輪自己漏掉的一處否定範圍、一處 `collected from your app`、一句 `as part of` 譯錯，
以及研究紀錄裡唯一殘留的錯誤前提。骨幹仍然一字未動，本篇可以出。
