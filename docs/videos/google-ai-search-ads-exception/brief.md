# 把 Gmail 連上 Google 的 AI 搜尋，廣告就能看你的信？10 月 16 日改的那一句話

企劃日期 2026-10-24。AI／科技時事，**教學卡片短片**（`format: "slides"`、`category: "ai-news"`、`theme: "paper"`，
teaching-flow §十「一個概念」＋§十二 畫面規格，範本是 `claude-md-house-rules` 與 `claude-duet-proactive-agent` 的紙底版）。
站內文章 `ai-news-google-personal-intelligence-ads-20261023`（每小時自動新聞，只在站上資料庫，不能當 `source_guide`，放進 `sources`）。
事實來源全部是 Google 自己的頁面，2026-10-24 開過：隱私權政策現行版（Effective October 16, 2026）、2026-10-01 的存檔版、
Google 搜尋說明中心的四頁（Personal Intelligence、Connected Content Apps、Personalized Recommendations、Search Services History）。
The Verge 2026-10-23 的報導與它引用的 Android Authority 只當「誰先發現」的時間鉤子，數字與條文一律以 Google 頁面為準。

**畫面文字一律英文**（站主 2026-10-24：影片要做多語言，畫面盡量不出現繁體中文，用英文取代；旁白仍是台灣國語、繁中走 CC）。
卡片的 `title`、`text`、`items`、`kicker`、`sub`、`keys`／`key`、章名 `chapter` 都寫英文；條文引用照原文；
`KEY_MAX_CHARS` 24 個字元在英文大約四到五個字，每句關鍵句寫短。zh-TW 的縮圖照頻道規則（中文大字 ≤ 6 字），其他八語（en、ja、ko、es、pt、id、vi、th）各自的縮圖、標題說明、CC 與配音照 i18n（站主 2026-10-24：「不只三語了，現在是八語」）。

## 觀眾

在台灣用 Google 搜尋、有 Gmail，看到「Google 要拿 Gmail 和相簿投廣告」這類標題，想知道「是我嗎？要不要關？關了會失去什麼？」的人。
他們搜尋的是「Google 隱私政策 Gmail 廣告」「Personal Intelligence 關閉」「AI Mode 個人化 廣告」。
他們知道 Google 靠廣告賺錢、知道搜尋紀錄會變成廣告，不知道這次改的只是一句話、只對「自己按了連接」的人生效、
也不知道那個開關在帳戶的哪一層。

## 觀眾看完能做到的事

- 打開 Google 隱私權政策，找到 10 月 16 日改掉的那一句（「We don’t show you personalized ads based on your content from Drive, Gmail, or Google Photos, unless you choose to make data from these services available to other Google services that support personalized ads.」），
  對照 10 月 1 日版只到「…or Photos.」就結束，說得出「例外」指的是哪個動作（第 2 章，`compare` 卡＋政策頁 `screencast`；CITED：policies.google.com/privacy 現行版與 /privacy/archive/20261001，2026-10-24 開過）。
- 在自己的 Google 帳戶裡走到 Search Services Personalization 的 Connected Content Apps，看見 Google Workspace（Gmail、Calendar）與 Google Photos 是「Connect」還是已連接，決定要不要按 Disconnect，
  並知道 Disconnect 不會刪掉 Search Services History（第 5 章，`steps` 卡；CITED：support.google.com/websearch/answer/16859283 的「On your computer」四步）。
- 在 Google 帳戶 → Data & privacy → Personalization settings 把「Personalized Recommendations in Search services」整個關掉，並說得出代價：AI Mode 的個人化（Personal Intelligence）要這個開著才有，
  Search Services History 是另一個開關（第 6 章，`steps`＋`compare` 卡；CITED：answer/17025248、17026260、17212611）。
- 跟朋友講清楚連接之後廣告拿到的是什麼、拿不到什麼：Search 可能用信件與照片的「摘要、片段與推論」選廣告；廣告商拿不到信箱與相簿、拿不到姓名與 email；
  種族、宗教、性傾向、健康這些敏感類別不投（第 4 章，`bullets`／`table` 卡；CITED：answer/16859283「Ads」段與隱私權政策「Provide personalized services」段）。

## 站主觀點

（頻道立場的文字沒有隨這次的啟動訊息帶進來，所以這一段是提案；站主 2026-10-23、10-24 都說過大綱照推薦直接做。）
我的看法是：這次不是 Google 偷改規則，是把一個早就存在的開關寫進了政策——你按下「Connect」那一刻，Gmail 和相簿就從「不碰」變成「可以拿摘要和推論去選廣告」。
我在意的不是那句英文，是三件事：這是你自己按的、它藏在帳戶第三層、關掉連接不會失去搜尋紀錄，但關掉 Personalized Recommendations 會連 AI Mode 的個人化一起沒了。
所以我的用法是：想要 AI Mode 記得我的口味就留著 Personalized Recommendations，但 Connected Content Apps 一個都不連；
真的要連 Gmail 來問行程，就先接受廣告會跟著變。台灣這一步大多數人還沒按過，所以看完先去確認那一頁，不用急著關掉整個個人化。

## 示範或實算

製作路線：教學卡片短片，`theme: "paper"`，畫面文字英文；一個生活對照撐全片：**會員卡**——你把會員卡交給店員刷，是為了折扣與推薦，
但從那一刻起你的購買紀錄就能變成下次的優惠券；不刷卡，店不知道你買了什麼。Connect 就是把會員卡交出去。

- 主例（CITED，Google 隱私權政策，2026-10-24 開過）：同一條 bullet 兩個版本並排。
  2026-10-01 版：「We don’t show you personalized ads based on your content from Drive, Gmail, or Photos.」
  2026-10-16 版：「We don’t show you personalized ads based on your content from Drive, Gmail, or Google Photos, unless you choose to make data from these services available to other Google services that support personalized ads.」
  同一版還多了一句：「For example, Search may process some of the data that you allow Search to access to personalize content, including ads.」
  以及把「based on your interests and activity across Google services」改成「based on your interests, activity, or personalized content from Google services」。登山車的例子兩版都有：
  「if you search for “mountain bikes,” in Search you may see ads for sports equipment on YouTube.」
- 開關的路（CITED，support.google.com/websearch/answer/16859283「On your computer」，2026-10-24 開過）：
  1. In your Google Account, go to **Search Services Personalization**（google.com/search-personalization）
  2. Turn on **Personalized Recommendations**
  3. Go to **Additional Personal Intelligence** → **Connected Content Apps**
  4. Select **Connect** next to Google Workspace / Google Photos
  影片把同一條路倒過來走：看自己有沒有連、按 Disconnect。說明頁原句：「You can choose to connect or disconnect your Google content apps at any time」「Disconnecting doesn't delete any data from your Search Services History」。
- 整個關掉（CITED，answer/17025248、17026260）：Google Account → **Data & privacy** → **Personalization settings** → 「Personalized Recommendations in Search services」on／off；
  Search Services History 是另一頁 myactivity.google.com/search-services/settings。answer/17212611：「AI Mode personalization is available if you're 18 or older and have history and personalized recommendations enabled.」
- 廣告拿到什麼（CITED，answer/16859283「Ads」段）：「Ads will not be based directly on your Gmail inbox or your Google Photos library.」
  「Search may reference summaries, excerpts and inferences from these sources to personalize your experience and do things for you. That same info may be used to show you ads.」
  「advertisers will not have access to your Gmail inbox or Google Photos.」「Google doesn't show you personalized ads based on sensitive categories, such as race, religion, sexual orientation, or health.」
- 不用這個方法：觀眾今天就能做的最簡單一步是打開 google.com/search-personalization 看一眼——這支影片比那一眼多的，是告訴他那一頁上每個開關各管什麼、關了丟什麼、以及政策那句話為什麼在 10 月 16 日才出現。
- 要先實作：沒有。本頻道沒有登入任何 Google 帳戶（規矩 4、9），所以帳戶設定頁的畫面不截圖，用 `steps` 卡照說明頁的字寫；
  `screencast` 只截公開頁：policies.google.com/privacy（那一句）、support.google.com/websearch/answer/16859283（四步）。
- 示範在第 2 章（兩版條文並排）、第 5 章（四步）、第 6 章（整個關掉的代價）。

## 大綱

### 選項 A（推薦）：一句話的例外——照觀眾會問的順序走

角度：整支只講一個概念「Connect ＝ 同意廣告用摘要」，章名是觀眾的問題；跟 B 差在不編人物、跟 C 差在不以兩句話的矛盾開場。

開場（五句，20 秒內）：「10 月 16 日，Google 的隱私權政策多了一句話。」／「你可能會問：我把 Gmail 連到 Google 的 AI 搜尋，廣告就會看我的信嗎？」／
「它會讀摘要、做推論、拿去選廣告；不會把信交給廣告商。」／「這一句只管一種人：自己按過 Connect 的人。」／
「看完這八分鐘，你會找到那一句、找到那個開關，知道關哪一個不會丟掉 AI 搜尋的個人化。」

案例與結果：「10 月 1 日版與 10 月 16 日版同一條 bullet 並排，多出來的 unless 子句就是整支影片；成果是觀眾走到 Connected Content Apps 那一頁並決定連或不連；證據 CITED（Google 政策頁與說明頁）。」

1. What changed on October 16?（70 秒）`title` → `big`（numeral 16, icon document）→ `compare`（Oct 1 / Oct 16 同一句）→ `screencast` 政策頁那一段。收尾問題：「那句 unless 後面講的『你選擇』，到底是哪個動作？」
2. What does “you choose” mean?（90 秒）`big`（icon arrow：Connect）→ `bullets`（Google Workspace: Gmail, Calendar；Google Photos；18+；opt-in）→ 會員卡對照一張 `big`（icon person）。收尾問題：「連了之後，廣告商真的看得到我的信嗎？」
3. Does an advertiser see my inbox?（90 秒）`table`（What Search may use / What advertisers get：summaries, excerpts, inferences ↔ no inbox, no name or email）→ `bullets` 敏感類別 → `big` mountain bikes 例子。收尾問題：「所以我現在到底有沒有連？」
4. Am I connected right now?（100 秒）`steps` 四步（Search Services Personalization → Personalized Recommendations → Additional Personal Intelligence → Connected Content Apps）→ `screencast` 說明頁四步 → `big`（Disconnect keeps your history）。收尾問題：「那乾脆全部關掉？」
5. What do I lose if I turn it all off?（80 秒）`steps`（Data & privacy → Personalization settings → Personalized Recommendations in Search services）→ `compare`（Off: no Personal Intelligence in AI Mode ／ On, apps disconnected: AI Mode still learns from your searches）→ `big`（Search Services History is a separate switch）。收尾問題：「那我會怎麼選？」
6. My call（50 秒）「我」三句：留 Personalized Recommendations、一個 app 都不連；要連 Gmail 問行程就接受廣告跟著變；台灣多數人沒按過 Connect，先去看那一頁。
7. 結尾（30 秒）一句答案：「Connect 是你自己按的，廣告跟著那一下」＋留言題「你會為了 AI 搜尋記得你的行程，讓它也拿去選廣告嗎？」＋訂閱句。

### 選項 B：小美的星期一——從一個人連接 Gmail 的早上講起

角度：用一位虛構使用者（小美）把 Gmail 連到 AI Mode 問「我這週有哪些要付的帳單」，接著在 YouTube 看到相關廣告，再回頭讀政策；
章節照她的疑問走。跟 A 差在有人物與時間線，跟 C 差在不談兩句話的矛盾。
開場：「小美星期一早上把 Gmail 連上 Google 的 AI 搜尋，問它這週要付哪些帳單——那一下，她也同意了另一件事。」
案例與結果：同 A 的條文對照，加小美的三個時刻（連接、問、看到廣告）；證據 CITED，小美是說明用的虛構人物（旁白要說清楚）。
章節：1. 她按了什麼（60 秒）2. 政策那一句（70 秒）3. 廣告商拿到什麼（90 秒）4. 她怎麼找到開關（100 秒）5. 她關了哪一個、留了哪一個（80 秒）6. 我會怎麼做（40 秒）7. 結尾（30 秒）。
風險：虛構人物的「看到廣告」沒有證據，說故事關卡與含金量都可能扣；只能講成「可能」。

### 選項 C：兩句話怎麼同時成立——政策說「unless」、說明頁說「not directly」

角度：以 Google 自己的兩句話開場：政策說連接後可能用來投廣告，說明頁又說「Ads will not be based directly on your Gmail inbox」，
全片解釋「directly」與「summaries, excerpts and inferences」的差別，最後才給開關。
開場：「Google 同一天寫了兩句話：一句說可能拿你的 Gmail 投廣告，一句說廣告不會直接根據你的信箱。兩句都是真的。」
案例與結果：同 A 的條文對照，重點卡是 `table`「directly ↔ summaries / excerpts / inferences」；證據 CITED。
章節：1. 兩句話（60 秒）2. directly 是什麼意思（90 秒）3. 誰會進到這個例外（80 秒）4. 開關在哪（100 秒）5. 關哪一個（80 秒）6. 我的選法（40 秒）7. 結尾（30 秒）。
風險：開場像在挑語病，對只想知道「要不要關」的觀眾慢了一章。

## 會過期的事實

- 政策條文與生效日：https://policies.google.com/privacy?hl=en（現行 Effective October 16, 2026）、存檔 https://policies.google.com/privacy/archive/20261001?hl=en
- 可連接的 app、地區與年齡：https://support.google.com/websearch/answer/16859283（Gmail、Calendar、Photos；Calendar 只有美國英文；Photos 不是所有地區；18+）
- Personal Intelligence 的前提：https://support.google.com/websearch/answer/17212611
- 開關的路徑與頁面名稱：https://support.google.com/websearch/answer/17025248、https://support.google.com/websearch/answer/17026260（兩頁都寫設定「rolling out gradually over the next few months」，撰稿當天再開一次）
- 直達頁：https://www.google.com/search-personalization、https://myactivity.google.com/search-services/settings
- The Verge 2026-10-23 報導日期與「Android Authority 先發現」：站內文章 ai-news-google-personal-intelligence-ads-20261023（The Verge 本身本機抓不到）

## 素材

- 站內文章 `ai-news-google-personal-intelligence-ads-20261023`（放 `sources`）
- `screencast`：https://policies.google.com/privacy?hl=en（公開頁，截「Provide personalized services, including content and ads」那段）；https://support.google.com/websearch/answer/16859283?hl=en（截「On your computer」四步）；兩頁也是縮圖主體候選（`thumbnail.data.capture`）
- 條文與說明頁的原文存在 `<home>/mokaair-work/videos/google-ai-search-ads-exception/_tools/sources/`（privacy-current.html、privacy-20261001.html、help-16859283.html）
- 不用任何人的帳戶畫面；不畫 AI 插圖

## 不做的事

- 不教怎麼開 Personal Intelligence 或 AI Mode（這支只講那一句話與那兩層開關）
- 不講 Gemini app、Workspace 企業帳戶、Ask Maps 的連接（說明頁有，但不是這句話影響的人）
- 不下「Google 偷改規則」的結論，不講法律責任，不比較其他公司的廣告政策
- 不猜廣告實際怎麼跑、不做「連了之後看到什麼廣告」的實測（本頻道不登入 Google 帳戶）
