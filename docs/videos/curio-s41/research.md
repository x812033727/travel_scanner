# S41｜焚書令下，《書》怎麼留下來？來源可行性（2026-10-20）

## 問題與暫定答案

**問題：**《史記》所記禁書議把《書》列入焚毀條款後，傳世史書怎麼解釋它在漢代仍有人教、有人校？

**暫定答案：**《史記·秦始皇本紀》記李斯要求焚燒非秦的史官記錄，以及不在博士官職掌中的民間《詩》《書》與百家語，並有三十日期限與重刑；《儒林列傳》又追記秦廷博士伏生壁藏《書》，兵亂後只找回二十九篇，轉而教學生。《漢書》補記解除挾書律、孔子舊宅另一面牆的古文書與漢代互校時的缺簡。這只能回答**傳世故事中部分篇章如何存續及哪裡仍缺**，不能把後出記載當秦令原件、把每處亡佚歸給書禁，或由二十九篇推出所有書的倖存率。

## 固定、已開啟的文本

以下 `raw` 於 2026-10-20 用 HTTPS 開啟並存入工作區外的 `/tmp/s41-*.txt` 後核 SHA-256。Kanripo 是傳世文本的電子轉錄；《史記》的這份檔帶現代編輯標記，《前漢書》是四庫全書文淵閣底本且混有後來注文。**它們不是出土秦令或未經傳抄的同時代影像。** 任何引文要按 `#L` 錨開回當前固定 commit，不用搜尋摘要或現代百科代替原文。

第二位審查者另外下載初期四份固定檔案，覆核 15 條候選主張與 48 個錨點；修訂後結果與保留界線見 [verify-sources.md](verify-sources.md)。第五份 H23 是劇本新增的**後世刑名白話註解**。初期四份的來源可行性 PASS 不等於新版逐句劇本或畫面核准。完整 R5b 稽核另發現同部《漢書》內部的魯王餘年代衝突，故加入 H6、H53 交叉核對。R5c 獨立逐景覆核見 `/tmp/s41-source-visual-r5c.md`，它要求收窄「百篇」與刪除一處未受史料支持的校書因果，並修分鏡。R5d 稽核見 `/tmp/s41-source-visual-r5d.md`，其來源已過，但地方官署畫面的一個郡／縣層級仍錯；R5e 來源與畫面規劃已過，然而兩位獨立盲讀者都判定孔騰／孔鮒旁白離題。R5f 把此異說留在研究註記，旁白直接回答第二面牆的篇數，並用 H30 L101–103 說明異字缺簡的理解後果；獨立逐景覆核在武帝時 `書缺簡脫` 的旁白發現過度說成缺篇。R5g 收窄該句與畫面，也把法令教學縮成與《書》交燒範圍相關的兩句；來源與畫面規劃已獨立覆核通過，但兩位盲讀者都要求改善章首回答。R5h 讓例外條款的四字短引直接回答章前問題，並把惠帝廢令的日期移到新章首句；仍待 exact-version 重新覆核。

| 代號 | 固定檔案與來源層級 | SHA-256 | 本題錨點 |
| --- | --- | --- | --- |
| J6 | [《史記》卷六〈秦始皇本紀〉轉錄](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt)；[raw](https://raw.githubusercontent.com/kanripo/KR2a0001/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt)。司馬遷漢代敘事，不是秦令實物。 | `b2c951b0613186eca4026c0f91d1dc913046313e778a2af368fd32fd63545991` | [三十四年宮宴、淳于越與李斯 L8827–8978](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8827-L8978)；[三十五年年標 L8979–8983](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8979-L8983)；[諸生案 L9144–9198](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L9144-L9198)。 |
| J87/J121 | [《史記》列傳總檔](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt)；[raw](https://raw.githubusercontent.com/kanripo/KR2a0001/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt)。同一部《史記》的複述及儒林回顧，**不算獨立秦代見證**。 | `02ebd6e50938cf3ab8c4df6bfa8d880a6c434f51518d38eba2183829dcebb07e` | [李斯列傳 L19386–19461](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt#L19386-L19461)；[儒林開篇 L48272–48348](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt#L48272-L48348)；[伏生記 L48655–48708](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt#L48655-L48708)。 |
| H2 | [《前漢書》卷二〈惠帝紀〉四庫轉錄](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_002.txt)；[raw](https://raw.githubusercontent.com/kanripo/KR2a0007/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_002.txt)。班固後出編纂，夾漢唐注釋。 | `26e42470c1a7351fcceca967ea35514ca9567a9fe3de47e5697c63ff4bb4af20` | [惠帝四年三月「除挾書律」 L88–96](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_002.txt#L88-L96)。 |
| H30 | [《前漢書》卷三十〈藝文志〉四庫轉錄](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt)；[raw](https://raw.githubusercontent.com/kanripo/KR2a0007/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt)。班固對秦以後書籍散亡、搜訪與分類的回顧；伏生藏書也見此篇，但比《史記》更晚。 | `58fd3be80541ddd20bf86f2523aae54e3d9256f96320a698d93e210404d06f8e` | [前言與漢代搜書 L12–33](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt#L12-L33)；[《易》以卜筮傳續 L59–68](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt#L59-L68)；[《書》傳續、缺簡與古文解讀 L75–103](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt#L75-L103)。 |
| H23 | [《前漢書》卷二十三〈刑法志〉四庫轉錄](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_023.txt)；[raw](https://raw.githubusercontent.com/kanripo/KR2a0007/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_023.txt)。**後出的漢代刑制整理及注文，只作刑名白話解說，不能當秦令原文。** | `32e04f44fff262aaafdc4cda774804098feaa3f88752787c002a4ec7e33e1624` | [黥／墨 L202–204](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_023.txt#L202-L204)；[城旦、棄市 L303–324](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_023.txt#L303-L324)；[三族與親屬連坐 L392–400](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_023.txt#L392-L400)。 |
| H6 | [《前漢書》卷六〈武帝紀〉固定轉錄](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_006.txt)；[raw](https://raw.githubusercontent.com/kanripo/KR2a0007/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_006.txt)。同部《漢書》的武帝年序，供**內部年代交叉核對**，不是秦令證人。 | `6bc57b8fcec6e96ca6d130d40522f7f4512d96af0023ec4d1a37262fdc55ce64` | [元朔元年與魯王餘薨 L159–207](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_006.txt#L159-L207)。 |
| H53 | [《前漢書》卷五十三〈景十三王傳〉固定轉錄](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_053.txt)；[raw](https://raw.githubusercontent.com/kanripo/KR2a0007/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_053.txt)。同部王傳追記魯王餘與舊宅，仍非牆中實物。 | `4249d9a4aa157ce5e1a841a7cf6da3524e6082ada3fac4334a03aac6a7ab76d2` | [魯王餘在位、舊宅壁書 L67–78](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_053.txt#L67-L78)。 |

## 《漢書》內部的魯王餘年代衝突

[H30 L92](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt#L90-L96) 將魯共王拆孔子舊宅寫成「武帝末」；但同書 [H6 L159–207](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_006.txt#L159-L207) 明記「魯王餘」在元朔元年薨，並非武帝末年。 [H53 L67–78](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_053.txt#L67-L78) 把拆舊宅、得古文經傳放在同一位王在世時，又記其在位二十八年。這是**傳世《漢書》內部互相牴觸的定年**，不取〈藝文志〉的「武帝末」作片中確年；旁白只說該志追記魯共王得書。此交叉核對不能證明牆中物件仍存或傳說每一細節都為真。

同段 [H30 L90–92](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt#L90-L92) 還夾**後來顏師古注**：它引《家語》稱孔騰藏書，又引《漢記》尹敏傳稱孔鮒藏書，最後明說「二說不同，未知孰是」。這只作為第二面牆傳述本身也有分歧的研究註記；兩名任何一個都不是〈藝文志〉主文確定的藏書者，也不與主文記的孔安國比對、獻書角色混同。兩位 R5e 盲讀者都認為把名字放進旁白會推遲十六篇的回答，所以 R5f 不說此支線。

## 可核的主張和要守的界線

| # | 文本所能說 | 固定錨點 | 不可偷換成 |
| --- | --- | --- | --- |
| 1 | 《史記》把議禁書放在始皇**三十四年**，開頭是咸陽宮宴；博士淳于越請參照殷周封子弟、功臣。 | [J6 L8827–8897](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8827-L8897) | 秦代當場錄影、保留下來的宮廷逐字筆記，或未查曆法就說某月某日。 |
| 2 | 李斯回應的核心理由，是「士」以古論今、私學議論現行法教，君權與法令要出於一。 | [J6 L8908–8950](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8908-L8950)；[J87 L19414–19445](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt#L19414-L19445) | 為防火、保存或單純節省書庫空間的行政命令。 |
| 3 | 李斯先說「史官非秦記皆燒之」：在史官記錄中，**非秦史記**被列入焚燒。 | [J6 L8950–8958](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8950-L8958) | 所有官署藏書都免燒；也不能據此算出每一諸侯國史書實際亡佚多少。 |
| 4 | 「非博士官所職，天下敢有藏《詩》《書》百家語者」須送郡守、郡尉雜燒：文字針對**不在博士官職掌中的藏書**。 | [J6 L8952–8961](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8952-L8961) | 每一份博士官文書均實際存活；或說《詩》《書》在秦代民間完全消失。 |
| 5 | 命令把民間私藏送交地方官與三十日期限、黥為城旦的懲罰連在一起。 | [J6 L8955–8977](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8955-L8977) | 只是一句文化口號、無強制力，或每個違令者實際都受同樣處分。 |
| 6 | 「所不去者，醫藥卜筮種樹之書」明列三類實用文本；欲學法令則「以吏為師」。 | [J6 L8967–8979](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8967-L8979) | 這三類是全部可能倖存的書；或書全可自由閱讀。 |
| 7 | 李斯是提出者，始皇在《史記》文本中答「可」。 | [J6 L8930–8979](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8930-L8979) | 有傳世的秦代原令，或有史料能證明各郡實際完成程度。 |
| 8 | 《李斯列傳》複述這段倡議，但比本紀簡略，沒有另給可驗的地方執行數字。 | [J87 L19389–19465](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt#L19389-L19465) | 和本紀算成兩件彼此獨立的秦時證據。 |
| 9 | 次年《史記》另敘侯生、盧生離去後的案問，記御史訊問咸陽「諸生」、牽連四百六十餘人；扶蘇進諫說諸生誦法孔子。 | [J6 三十五年 L8979–8983](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L8979-L8983)、[侯生、盧生 L9109–9115](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L9109-L9115)、[諸生案 L9148–9199](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt#L9148-L9199) | 這是三十四年的焚書同一道命令；也不說四百六十餘人全是方士、全是儒生。畫面不得重現處刑。 |
| 10 | 《儒林列傳》回顧此時說「焚《詩書》，阬術士」並指出六藝有缺；與本紀的人群字眼不同。 | [J121 L48278–48315](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt#L48278-L48315) | 看到「術士」就抹去本紀「諸生」與扶蘇的話；或把這句視為秦時官方統計。 |
| 11 | 伏生故事是《史記》回看：傳稱他壁藏《尚書》，戰亂後只尋回二十九篇；另記文帝遣朝錯問學、伏生教張生與歐陽生、歐陽生再教兒寬，兒寬貧而仍攜經誦讀。這顯示**部分傳續與部分缺失同在**。 | [J121 L48655–48691](https://github.com/kanripo/KR2a0001/blob/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt#L48655-L48691) | 對所有書籍的存亡比例抽樣、獨立考古證明，或把戰亂所失一律算在焚書令上；兒寬攜帶的「經」不指定為伏生壁藏的原卷。 |
| 12 | 《前漢書·惠帝紀》記惠帝四年三月「除挾書律」，說明後來有明記解除藏書禁令的節點。 | [H2 L88–95](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_002.txt#L88-L95) | 解除當日每份書立即恢復；此書比秦事晚，不能假稱秦律原件已存。 |
| 13 | 《前漢書·藝文志》說漢興後開放獻書，武帝、成帝時仍整理、求遺書；劉向去世後由劉歆承接編目；《易》傳本有字句差異，《書》則有缺篇記載。同段又說《書》是古代號令：言語不完整，受命者難以施行；古文讀應《爾雅》，須解通古今用語。 | [H30 L16–33](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt#L16-L33)、[L59–103](https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt#L59-L103) | 書籍全數回來、所有損失皆由一場大火造成；班固是後世整理者。不要把古文讀法說成劉向個人使用《爾雅》的具體流程。 |

## 敘事順序與視覺守則

用一個具體場景開頭：**咸陽宮宴**上淳于越主張仿古封建，李斯被要求答覆。《書》如何因這場爭論被點名？先看本紀的史官條款，再看博士官與持書人條款、期限與刑罰，才走到伏生的壁藏、兵亂、**未定年**尋找先前藏的書。伏生找到的二十九篇經師生傳授，接到文帝遣朝錯的記載；惠帝除挾書律作獨立法律節點，**不作伏生尋書的原因或先後錨點**。最後依〈藝文志〉追記孔子舊宅的另一面牆、孔安國與伏生版本互校，以及劉向對《書》的具體缺簡。兒寬受教於孔安國見 J121；不可說他讀過孔子舊宅的牆中本。**次年諸生案留在 B 案，A 案正文不提四百六十人的數字。**

插圖只示意人物與空白竹簡；原文短引（`史官非秦記`、`非博士官所職`、`醫藥卜筮種樹`、`除挾書律`、`古文尚書`）只能在有來源的卡上出字。不可讓 MiniMax 畫出可讀且未驗證的竹簡字、虛構秦詔書原件、現代裝訂古書、醫藥種植的時代錯置道具，或火燒人／屍體。畫面要避免「皇帝親手點燃每座書庫」及「博士官庫裡每卷完整保存」之類超過史料的行為。系列 5 秒片頭放濃縮開場後、21 秒片尾；本階段沒有成片或付費媒體。

## 審核前的未決事項

1. 由不同審查者從四個固定原檔重新讀 `史官非秦記` 與 `非博士官所職`，確認研究中的句法邊界和年代敘事，不用搜索結果摘要。
2. 若劇本要把三十四年換成西元前 213 年，另找可存取的可靠紀年換算來源；此稿暫只寫史書的年號。
3. 若劇本要討論「坑儒」一詞何時形成、460 人身份或戰國百家實際存亡，需額外獨立來源。現有兩部傳世史書只夠標示用字差異和事件先後。
4. 若想把伏生、孔子壁中書做成戲劇化重建，先核版本與出土證據；本集目前只可說《史記》／《漢書》**如此追記**。
