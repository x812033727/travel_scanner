# daily-ai-20261109 查核第 2 輪

查核日 2026-11-09。查核代理不是撰稿人，也不是第 1 輪的查核代理。範圍：第 1 輪（commit `6a678de65`「fact and joke check round 1」）之後改過的一切，即 `git diff 6a678de65..HEAD -- docs/videos/daily-ai-20261109/video.json`：claims.md 的 c62–c76、〈笑點〉最後的「盲聽修改第 2 輪」一節，以及每一張改過的卡片（`kicker`、`text`、`key`）。另外照 `prompts/verifier-video.md` 的第 2 輪規則，把第 1 輪改過的主張（verify-1 #8、#10、#11、#14、#15、#17、#18、#25、#30、#32、#35、#48、#53、#60）對回原文再看一次。
來源：站上 4 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.2 秒，全部 HTTP 200、`status: published`，news_date 與 claims.md 相同），加上 `sources` 的 5 個原始來源，用 `Mokaair-editorial/1.0` UA 以 curl 重開（去掉 `<!-- -->` 後讀全文，全部 200、沒有轉址）。web search 0 次。另有〈笑點檢查〉、〈清楚度檢查〉與〈畫面狀態〉三節。

## 來源代號

站上文章（全部 200，published）：

| 代號 | slug | news_date |
| --- | --- | --- |
| TSLA | tech-news-tesla-cybertruck-wind-down-20261106 | 2026-11-06 |
| ART | ai-news-artex-exposed-tools-20261106 | 2026-11-06 |
| NYT | ai-news-nyt-cooking-assistant-20261107 | 2026-11-07 |
| SUNO | ai-news-suno-elvis-eminem-lawsuits-20261108 | 2026-11-08 |

原始來源（2026-11-09 全部 HTTP 200，沒有轉址）：

| 代號 | URL |
| --- | --- |
| DC7 | https://decrypt.co/382703/tesla-to-wind-down-cybertruck-production-as-elon-musk-pivots-to-robotaxis-and-ai |
| VNY | https://www.theverge.com/tech/1029489/nyt-cooking-ai-assistant-review |
| SUV | https://www.theverge.com/ai-artificial-intelligence/1029533/elvis-eminem-suno-ai-music-clone-lawsuit |
| TC6 | https://techcrunch.com/2026/11/06/hundreds-of-artex-ai-hacking-tools-found-publicly-exposed-to-the-web/ |
| MS1 | https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/ |

## 主張表（本輪改過的句子與卡片）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 開場鉤子：今天的主菜是一場官司，兩組握有音樂權利的原告告了 AI 音樂公司 Suno；卡片「Music rights holders vs. Suno」、key「Today: Suno is sued」 | hk01；mo-hi | SUV、SUNO | 200 | CONFIRMED（「Suno is facing yet another pair of lawsuits. A group of rights holders of Elvis Presley's music and the publisher of some of Eminem's biggest records are suing」；出版商握有的是唱片的權利，「音樂權利」涵蓋得到） | |
| 2 | Kai 的問題搬到開場；「這題，主菜時吵給你聽」；「先補上週五到週末的另外兩則新聞」 | su05、su06、hi03；mo-q | 站上 4 篇 | 200 | CONFIRMED（另外兩則是 Cybertruck 11/6 週五與 NYT Cooking 11/7 週六；AI Fail 的 Artex 是固定單元，不算在「兩則」裡） | |
| 3 | 據 The Verge 週日 11 月 8 日的報導，Suno 又被告了 | su01；su-lead | SUV | 200 | CONFIRMED（「yet another pair of lawsuits」；datePublished 2026-11-08。日期掛在「報導」上，不會讀成 11/8 起訴，第 1 輪 #17 的問題沒有回來） | |
| 4 | 告 Suno 的，一組是握有貓王 Elvis Presley 音樂權利的權利人，一組是 Eminem 幾張招牌唱片的出版商 | su03；su-who | SUV、SUNO | 200 | CONFIRMED（「rights holders of Elvis Presley's music」「the publisher of some of Eminem's biggest records」；SUNO 標題「Elvis 與 Eminem 權利人起訴 Suno」。原文的出版商是單數，「一組」在這裡是「一方」的意思，可以接受） | |
| 5 | 他們都說，Suno 違法生成模仿這些歌手的音樂和歌詞；所以出面告人的，不一定是歌手本人 | su04、mc04；su-claim | SUV | 200 | CONFIRMED（「claiming it illegally generates music and lyrics that mimic those artists」；mc04 是解釋，「不一定」比來源保守，不會錯） | |
| 6 | 使用者輸入給 AI 的那段文字，叫提示詞（移到 mc39 前面） | mc03；mc-guard | SUNO | 200 | CONFIRMED（解釋；mc-guard 的 keys 3 個，畫面狀態 3 個） | |
| 7 | 這部法律的英文全名，意思是確保肖像、聲音與影像安全，縮寫起來就是 ELVIS | mc11；mc-acr | SUV | 200 | CONFIRMED（「Ensuring Likeness Voice and Image Security (ELVIS) Act」：確保＝Ensuring、肖像＝Likeness、聲音＝Voice、影像＝Image、安全＝Security，逐字對得上，順序照中文語序；E-L-V-I-S 的拼法成立。沒有說命名是照貓王取的，mc13 照舊說報導沒這樣說） | |
| 8 | 好，這點算你一分，至少 Suno 說得出它怎麼擋；卡片「At least it says how it blocks」、key「Point to Kai: guardrails」 | mc43；mc-kai2b | SUV | 200 | CONFIRMED（發言人「we do not allow prompts for specific artists' names and songs and work with third-party providers to screen uploaded audio files and lyrics」：說了兩種擋法；「說得出」不等於「擋得住」，跟 mc42 一致） | |
| 9 | 誰會吃虧？訴狀的原話是，Suno 想讓人類的創意變得過時 | mc73、mc51；mc-lose | SUV、SUNO | 200 | **CHANGED**（原文「Suno's ravenous race to the bottom aims to make human creativity obsolete」：主詞是 Suno「搶著壓低的競賽」，旁白是中譯又只取半句，不是「原話」；SUNO 自己也標「大意是：Suno 意在讓人類創意變得過時」。「原話」會讓人以為這是逐字引句。卡片 quote 片段「Human creativity obsolete」是原文的字，沒問題） | mc51 →「照訴狀的說法，Suno 想讓人類的創意變得過時。」（第 1 輪 #40 確認過的說法） |
| 10 | 而且 Presley 那一案用的，是美國田納西州的法律（改由 Kai 說） | mc57；mc-tw2 | SUV | 200 | CONFIRMED（「violated Tennessee's … (ELVIS) Act」；換人說不改內容） | |
| 11 | 一種叫 trifle 的分層甜點，記者問能不能把手指餅乾換成牛絞肉 | ny08；ny-beef | VNY、NYT | 200 | CONFIRMED（「Could I swap ladyfingers for minced beef in this trifle」「anywhere in this sweet dessert trifle」；NYT「trifle（一種分層甜點）」。`docs/videos/lexicon.json` 已有 `"trifle": null`，lint 沒有警告） | |
| 12 | Kai：我覺得它比一般聊天 AI 好用，至少不會把原食譜蓋掉；卡片 kicker「Kai's verdict」、text「Useful, but check it」 | ny16；ny-check | VNY | 200 | **CHANGED**（「比一般聊天 AI 好用」是 VNY 沒做的比較：記者說 AI 一向是她的「sous chef」，沒有拿這個助理跟一般聊天 AI 比好壞；後半還暗示一般聊天 AI 會把原食譜蓋掉，等於用意見帶出來源沒有的事。VNY 有的是「genuinely helpful」與「it doesn't change the existing recipe」。卡片 kicker 寫「Kai's verdict」，但「but check it」是 Sola 在 ny17 補的、記者的話，卡片把它算到 Kai 頭上） | ny16 →「我覺得它真的好用，至少不會把原食譜蓋掉。」；kicker →「The verdict」 |
| 13 | 同意一半，記者也說用量和時間，還是要自己跟原食譜對一次 | ny17；ny-check | VNY | 200 | CONFIRMED（「I still felt the need to double-check amounts and cooking times and cross-reference them with the original」） | |
| 14 | AI Fail 的主角是一套叫 Artex 的 AI 工具，它會自己去找電腦系統的弱點；研究人員發現好幾百套 Artex 露在公開網路上；Artex 是開源的工具 | af01、af02、af03；af-intro、af-news、af-what | TC6 | 200 | CONFIRMED（「open source autonomous penetration testing tool, meaning software that automatically probes computer systems for weaknesses」「hundreds of copies … publicly exposed to the internet」） | |
| 15 | Censys 找到超過 800 套 Artex，從網路就連得進去，登入還不用密碼 | af08；af-open | TC6 | 200 | CONFIRMED（「more than 800 distinct deployments of Artex that were accessible from the web without needing a password to log in」） | |
| 16 | TechCrunch 還說，連攻擊用的工具也一起露出來了；其中一種，是藏在受害者網路裡的惡意程式 | af15、af31；af-kit | TC6、ART | 200 | CONFIRMED（「also expose attack tools, such as implants (hidden malicious software) used to compromise and maintain persistent access to a victim's network」；ART「植入程式（隱藏的惡意軟體）」；沒有講用法）／**改措辭（清楚度）**：af31「其中一種」單獨聽不知道指什麼；改完 af-kit 變 13.9 秒，所以 af15 一起縮短 | af15 →「TechCrunch 還說，攻擊用的工具也露出來了。」；af31 →「這些工具裡，有藏在受害者網路裡的惡意程式。」（af-kit 12.9 → 12.4 秒） |
| 17 | 部分原因是，這個駭客把放 Artex 的資料夾，設成誰都能打開 | af19；af-kr2 | TC6、ART | 200 | **CHANGED**（原文「in part because the hacker had left an "open directory" hosting the system」，ART「留下了託管該系統的開放目錄」：left 是「留著沒關」，「設成」說成刻意去設定，比來源多一層意思。卡片「The hacker left it public」本來就對） | →「部分原因是，這個駭客放 Artex 的資料夾，留在網路上誰都能打開。」（af-kr2 12.4 → 12.9 秒） |
| 18 | Cybertruck 的銷量，大約只有產線規劃的十分之一 | ct12；ct-sales | DC7 | 200 | CONFIRMED（「roughly a tenth of the 250,000 units a year that Tesla built its production line to make, according to the outlet」；拿掉「賣不好」沒有改意思） | |
| 19 | outro：原告說，AI 跟人學歌，差在授權和速度；用歌手的聲音，AI 該先問嗎？留言告訴我們；訂閱 Tech Signal。訊號收到 | ou01–ou03；outro | SUV | 200 | ou01 CONFIRMED（「without a license in seconds what takes years」）；ou02 不含事實；**改（時間）**：ou02 的「留言說」→「留言告訴我們」讓 outro 從 12.3 變 13.0 秒 | ou02 →「AI 該先問歌手嗎？留言告訴我們。」（outro 13.0 → 12.0 秒，仍是三句：答案、留言題、訂閱與收尾；跟卡片「Should AI ask first? Tell us」一致） |

## 主張表（第 1 輪改過的主張，再對一次）

| # | 主張（第 1 輪改後） | 位置 | URL | HTTP | 判定 |
| --- | --- | --- | --- | --- | --- |
| 20 | NYT Cooking 最近加了 AI 助理（不說 11/7 上線） | ny01 | VNY | 200 | CONFIRMED（文末更新註記：功能在說明頁上非正式宣布；11/7 是 The Verge 的發布日） |
| 21 | 上線時只給 iOS 上的訂閱用戶用 | ny05 | VNY | 200 | CONFIRMED（「available to subscribers on iOS only at launch」） |
| 22 | The Verge 的記者 11 月 7 日週六發了實測；幾秒鐘生出新食譜 | ny06、ny07 | VNY | 200 | CONFIRMED（「Within seconds, it created a new version of the recipe, with a new title」） |
| 23 | 照原版烤蛋糕，問奶油，它給了改版的量；卡片「almost a dry cake」 | ny13；ny-butter | VNY | 200 | CONFIRMED（「gave me the modified recipe's 6 tablespoons rather than the original's three-quarter cup, without telling me which version」「would have made for a dry cake」） |
| 24 | 標題、縮圖副標、su-lead「Elvis, Eminem rights holders vs. Suno」 | youtube.title、thumbnail、su-lead | SUV | 200 | CONFIRMED（SUV 標題「Elvis and Eminem rights holders are suing Suno」） |
| 25 | 據 The Verge，這部法律讓 AI 公司未經同意複製歌手的聲音成為違法的事；卡片「without consent」 | mc10；mc-law2 | SUV | 200 | CONFIRMED（「which makes it illegal for an AI company to clone a singer's voice」；「未經同意」是第 1 輪對法案原文補的，本輪沒有重開 TNL） |
| 26 | 卡片 mc-turn「Not just learning.」 | mc-turn | SUV | 200 | CONFIRMED（「mechanically encoded itself with artists' identities」） |
| 27 | 發言人也說了 Suno 怎麼防（不用「她」） | mc38 | SUV | 200 | CONFIRMED |
| 28 | Microsoft：跟中國國家立場一致的駭客組織，最早從 9 月起，用它自動攻擊全球數百個組織；卡片「targeted」 | af07；af-ms | MS1 | 200 | CONFIRMED（「As early as September 2026, Storm-0940, a China-state aligned actor, used … ARTEX to automate attacks targeting hundreds of organizations globally」「the majority of the targeting wasn't successful」） |
| 29 | CrowdStrike 把 9 月針對韓國金融業的攻擊算到一個用 Artex 的駭客頭上 | af18 | TC6 | 200 | CONFIRMED（「attributed the attacks to a Chinese-speaking hacker who used an Artex instance」） |
| 30 | Isbell 案與著作權的解釋（第 1 輪 #30、#31） | 已刪 | — | — | OUT OF SCOPE（盲聽修改把 mc28–mc31 與 mc-isb、mc-isb2 刪掉；全片已沒有 Isbell 的旁白或卡片，claims.md c31、c32 有註記） |

## 笑點檢查

逐句看 claims.md〈笑點〉最後「盲聽修改第 2 輪」的每一句，加上改過的卡片。五條標準：暗示錯誤或來源沒有的事實、新的數字、替真人編話、打一般人、雙關或諧音。

| # | 笑點 | 位置 | 判定 | 理由 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- |
| 1 | 「對車主來說，這總比一句『沒了』好。」 | ct07；ct-ex | **留** | Kai 的意見，接 ct04 的馬斯克回覆；「沒了」是假設的說法，沒有掛在任何真人嘴上；沒有說售後怎樣（ct05 剛說報導沒提）。 | |
| 2 | 「換句話說，Cybertruck 被裁員了，接替它的同事，連方向盤都沒有。」；key「Laid off by a robotaxi」；卡片「Replaced by a car with no steering wheel」 | ct10；ct-joke | **留** | 「被裁員」的主詞是車，「同事」是另一台車，一聽就是擬人；事實照 ct08、ct09（騰產能給 Cybercab；「no steering wheel or pedals」）。旁白與卡片只說沒有方向盤，沒有加任何來源沒有的操控方式（沒有搖桿之類的說法）。沒有說特斯拉裁了員工。 | |
| 3 | 「十分之一？那條產線要是員工，早就在偷投履歷了。」 | ct13 | **留** | 同一組擬人比喻，「要是」標明是假設；「十分之一」是 ct12 剛說的數字，沒有新數字；不說產線停工、不說工人要走，笑的是產品賣不動。 | |
| 4 | 「老規矩，先問我的老問題：所以我要不要換手機？」／「老問題又來了，所以我要不要換手機？」 | ct14、af25 | **留** | 固定梗（daily-brief §一 的例子，11/6 起每集都有）；ct15、af26 的答案不變。 | |
| 5 | 「而且它守住的戰場，是甜點。」 | ny18；ny-joke | **留** | 接 ny10 的誇張，事實是 ny09（VNY「Good call」）；沒有數字、不是雙關。 | |
| 6 | 「可是模仿秀也是靠模仿別人賺錢，我不覺得差那麼多。」；「差在模仿秀的人會累。」；卡片「Impersonators get paid too」 | mc23、mc70；mc-joke1b | **留** | mc23 是 Kai 的意見，「模仿秀靠模仿賺錢」是一般常識，沒有法律主張；mc70 對比人與 AI，替模仿藝人說話（他們要花力氣），不是笑他們；沒有說模仿秀合法或 Suno 違法。不是雙關。 | |
| 7 | 「終於有一分是我的！」；「記好，今天可能就這一分。」 | mc44、mc71；mc-kai2b | **留** | 計分梗；「可能」是主持人的嘴，不預測判決。 | |
| 8 | 「我覺得那就少學一點吧，人類歌手也沒聽完全世界的唱片才出道。」 | mc69；mc-kai3 | **留** | 標明是 Sola 的看法；誇張的對比，沒有數字。 | |
| 9 | 「我還是站 AI 這邊，學本身沒有錯；要不要先問，等法院說。」；卡片 kicker「Kai's last word」、「Learning is fine. Let the court decide」、key「Kai: still on AI's side」 | mc67；mc-view2 | **留** | 「我還是站」標明是意見；「等法院說」跟 mc35、mc66 一致，沒有預測結果。Kai 從頭到尾沒改立場，跟 `callbacks` 的 mc05→mc67 一致；Sola 的看法（mc64、mc65）仍標「我的看法是」，跟 brief.md〈站主觀點〉一致。 | |
| 10 | 「好，AI 跟人學唱歌差在哪，現在可以吵了。」 | su07；su-lead | **留** | 串場，把開場的問題重說一次。 | |
| 11 | 「連密碼都不用？這是駭客工具，還是公共圖書館？」；卡片「No password? A public library?」 | af09；af-open2 | **留** | 誇張的反應，接 af08（c49）；圖書館是公共場所，不是在笑一般人；「駭客工具」照 TC6 標題「AI hacking tools」；不是雙關。 | |
| 12 | 「我覺得研究人員太客氣了，工具放在網上還不鎖，本身就是問題。」；卡片「Unlocked tools: the problem itself」 | af32；af-kai | **改** | 「研究人員太客氣了」暗示研究人員沒把外露當一回事，可是 TC6 明寫外露「increasing the chance that someone will find and misuse them」，研究人員說的「不是每一套都拿去做壞事」是在講使用者，不是替外露開脫。等於用意見帶出跟來源相反的事；後半「本身就是問題」是 Kai 可以有的看法。 | →「我覺得不管是誰在用，工具放在網上還不鎖，本身就是問題。」（接 af12 的「很多是有授權的測試人員」，不評論研究人員；卡片不動） |
| 13 | 「打個比方，就像小偷把作案行程表貼上網，還設成公開。」 | af20；af-kr2 | **留** | 開頭標明是比方；「小偷」指 CrowdStrike 歸因的那一個駭客，不是一般人；「設成公開」在比方裡是笑點，旁白的事實句 af19 已改成「留在網路上」（主張表 #17），兩句不會打架。 | |
| 14 | 卡片 kicker「Kai, stunned」「Kai holds out」「Kai's side」（mc-lose2）「Sola's reply」（mc-lose3） | 各卡片 | **留** | 標明誰的立場，跟說話的人一致；mc-lose3「No license, per the suit」照 mc54 的「照原告的說法」。 | |

笑點總計：14 項，留 13 項，改 1 項（#12），刪 0 項。全片沒有雙關或諧音、沒有新的數字、沒有替真人編的引句、沒有打一般人。主張表 #12 的 ny16 也是意見句帶出來源沒有的比較，算在事實修改裡。

## 清楚度檢查

照 daily-brief.md §一之〇。

- 句子完整性檢查（任務給的 node 指令，含 key 長度與 keys 數量）：修改前 0 行，修改後 0 行。`big`、`quote`、`outro` 都沒有 `reveal`；所有 `key`／`keys` ≤24 字；有 `keys` 的場景（mc-sides、mc-guard、mc-next）數量都等於畫面狀態數。
- 改過的每一句都有主詞、以 。？！ 結尾，單獨聽得懂：
  - hk01 一開口就說今天的主菜是官司、誰告誰；「權利人」這個詞留到 su03，在同一句裡用「握有……音樂權利的」解釋，第 1 輪〈懷疑但沒改〉的「權利人比解釋早一句」解決了。
  - su01「Suno 又被告了」、su03「告 Suno 的，一組是……一組是……」：主菜前兩句就是誰告了誰。
  - mc03 搬到 mc39 前一句，「提示詞」第一次出現就有解釋。
  - mc11 補上全名的意思，聽眾知道 ELVIS 是哪幾個字的縮寫。
  - mc51 原本的「訴狀的原話是」跟在 Kai 的問句後面聽得懂；改成「照訴狀的說法」一樣是完整的句子。
  - af01 把 Artex 是什麼搬到第一句；af03「Artex 是開源的工具」重說名字。
  - af31 原「其中一種，是……」單獨聽不知道是哪一種，改「這些工具裡，有……」重說「工具」。
  - af19 重說「Artex」，不寫「那套」。
  - ct14、af25 先交代「老規矩」「老問題」，第一次看的人也知道是固定梗。
  - outro 的 ou02「AI 該先問歌手嗎？」自己是完整的問句，離 su05 十分鐘也聽得懂。
- 不往回指：改過的句子裡沒有「剛剛那篇」「跟那個一樣」「這也是」。mc57「Presley 那一案」重說名字。
- 出處短講：su01 一次「據 The Verge」，af02 一次「據 TechCrunch」，ct12 一次「據 Decrypt」。

## 畫面狀態

用 lint 的估計時間軸（`tools/video/core/timeline.mjs` 的 `estimateTimeline` 加 `cadence.mjs` 的 `slideStates`）重算：

- outro 13.0 → **12.0 秒**（三句：ou01 答案、ou02 留言題、ou03 訂閱與「訊號收到」）。
- 本輪改動造成的變化：ny-check 12.8 → 11.6、mc-lose 8.0（沒變）、af-kai 7.3 → 6.8、af-kit 12.9 → 12.4（af31 第一版改完是 13.9 秒，所以 af15 一起縮短）、af-kr2 12.4 → 12.9。
- 全片最長 **12.9 秒**（ny-why、ny-beef、su-lead、mc-scene、af-kr2、so-take、so-call），沒有一個畫面狀態超過 13 秒。

## 摘要

- 本輪查了 30 項：本輪改過的句子與卡片 19 項、第 1 輪改過的主張 11 項（其中 1 項已刪，OUT OF SCOPE）。CONFIRMED 25 項；CHANGED 4 項事實（#9 mc51、#12 ny16 與 ny-check kicker、#17 af19），另有 1 項清楚度（#16 af15／af31）與 1 項時間（#19 ou02）；NOT FOUND 0 項。
- 事實修改：(1) mc51「訴狀的原話是」→「照訴狀的說法」：旁白是中譯的半句，原文主詞是「Suno's ravenous race to the bottom」，SUNO 自己標「大意是」；(2) ny16「比一般聊天 AI 好用」→「真的好用」：VNY 沒做這個比較，「genuinely helpful」撐得住後者；(3) 卡片 ny-check kicker「Kai's verdict」→「The verdict」：「but check it」是 Sola 和記者的話；(4) af19「設成誰都能打開」→「留在網路上誰都能打開」：原文是 left，不是刻意設定。
- 笑點：14 項，改 1 項（af32「研究人員太客氣了」暗示研究人員沒把外露當問題，跟 TC6 相反 →「不管是誰在用」），刪 0 項。任務點名的幾句：ELVIS 全名的意思（mc11）逐字對得上；trifle 照原文、字典有；ct10、ct13 只說沒有方向盤，沒有加任何來源沒有的操控方式，擬人比喻一聽就是玩笑；Kai 的三句意見 ny16（改）、af09（留）、af32（改）；mc23、mc67 標明是意見、不暗示法律結論；su01、su03、su04 的歸屬都掛在 The Verge 與原告。
- 訴訟：仍然每一句都標成「他們都說」「律師說」「照原告的說法」「照訴狀的說法」；mc35、mc66 明說要法院決定、現在都是指控；mc67 Kai 也說「等法院說」。
- 會過期的事實：同第 1 輪（Cybertruck 停產時程，DC7 2026-11-06；NYT Cooking 的 iOS 範圍「at launch」，VNY 2026-11-07；Suno 兩案的進度與 Eminem 案的法律依據，SUV 2026-11-08；Censys 的 800 多套，TC6 2026-11-06）。`sources` 的 `checked_on` 留在 2026-11-08：本輪 2026-11-09 重開全部 200、沒有數字改變。
- 觀點：Sola 的看法（mc64、mc65、mc66、mc69、so01、so02）都有標明，跟 brief.md〈站主觀點〉一致；Kai 的意見（ct07、ny16、mc23、mc67、af32）都以「我覺得」「我還是站」「我不覺得」標明，不在 brief 的站主觀點裡，是角色的立場，沒有不一致。
- 聽眾檢查（只報告）：全片超過 40 字（不算標點、引號與空白）的有 11 句：su03 52、af07 46、af08 46、af23 44、ct01 43、af02 43、af18 43、mc09 42、ct12 41、mc25 41、af01 41；本輪改過的是 su03、af08、af02、af01、ct12。su03 仍最長，一句裡有兩組原告，可以考慮拆成兩句（只報告，沒動）。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後；沒有新的字典外拉丁詞（trifle 已在 `docs/videos/lexicon.json`）。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261109` → `daily-ai-20261109: 0 errors, 3 warnings`（同前三條：開場章節長度、「11」說了 5 次、投影片順序跟 daily-ai-20261106 有 86% 相同）；估 14.0 分鐘，154 句。
- 懷疑但沒改：
  - mc04「不一定是歌手本人」：在這兩案裡原告確實都不是歌手本人，「不一定」比較保守，不會錯，沒改。
  - su03「一組是……出版商」：原文出版商是單數，「一組」當「一方」用，沒改。
  - ct10 的「被裁員」：擬人很清楚，但八語翻譯時要確認不會讀成特斯拉裁了員工；交給翻譯代理留意。
  - mc67「要不要先問，等法院說」：法院判的是這兩案有沒有違法，不是一般的「要不要先問」；是 Kai 的意見而且有標明，沒改。
  - af20 比方裡的「設成公開」跟 af19 改後的「留在網路上」不完全同一個動作；比方本來就是誇張，沒改。
- 需要再一輪：照規則（本輪事實修改超過 3 個）**是**，但只需要對本輪改過的 7 句與 1 張卡片（mc51、ny16、af19、af15、af31、af32、ou02 與 ny-check 的 kicker）。這些改動都是把措辭收回到來源，沒有新的事實或數字。所有主張都已判定，沒有懸而未決的。
