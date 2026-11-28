# C07 Dr. Martens｜來源預備（2026-10-25）

研究已完成，可用材料足以規劃約 **3,500 spokenUnits 正文**的單線重寫：沿著氣墊／彈性鞋底與鞋邊接縫，從接合難題、英國靴款的可辨識部位，走到穿法和換底。這是素材容量判斷，**沒有新敘事稿、SOURCE PASS、verify、實測語音、媒體 QA 或站主核准**。早期僅有 Google 轉錄的專利不是補長目標的必要支柱；原始 US 專利掃描、現行原廠工法、正式揭露及授權維修程序已能提供實物動作。

## 舊稿原生計數與來源鏈

原生匯入 `timeline.spokenUnits()` 與 `schema.eachLine()`，逐句計 `line.text`；第二章起算正文。現行 **78句／78景，總2057，開場123，正文1934**，距約3500差1566；最後觀眾問題與訂閱48 units仍包含在1934內，扣掉則1886。六章 units：123／446／299／276／431／482。這不是 TTS 或 runtime 測量，不能由舊紙上575秒估時推定達標。

`script.md` 是73列，`video.json` 五列在標點切段而成78列；本次逐組還原73列全數逐字相等。v12回執的script SHA與現件相符；2026-10-24前製收據也明記只是機器轉換。舊來源回執保留為歷史鏈，不是本研究對新稿或新增來源發PASS。

| 原件 | SHA-256 |
|---|---|
| `video.json` | `ddcf3cb5bfe8fb2124afdc27d6e422fe53012aa05a13892728596d3d543712e0` |
| `script.md` | `624af568ec2f85c2df2536a307433a4eadf301eeaa095d8cd676a5418c2ab47b` |
| `claims.md` | `1b2b1c178857c79147e5ac508c858033bda05220858d10eb50f9112f2a5664a0` |
| `source-matrix.md` | `7eecf40d1683da46f73b0722d63f3d7e4fc729ebbb10233caae469e33aa0993a` |
| `script-source-notes.md` | `3d14723d60eaf0e12657dc97e75c9b720d339c301925b4b2019b622a27d69fc2` |
| `reviews/script-source-review-v12.md` | `4a01424f213b915c91299d990dc4ead9bd96a8d48fa0134320951a8004c52be9` |
| `reviews/canonical-video-preflight-20261024.md` | `80039798ab87358b843b6d0645dd813a00ec9d071f72f951da7ea0cd78efd20f` |

## 可用來源：證據層級和日期

所有下列 SHA 均重讀實際快取 bytes 計算。完整 URL、bytes、取得時間、短原文與限制在 `claims.json`；HTTP Last-Modified 不冒充出版日。同公司沿革、招股書及產品頁不算多個獨立歷史證人。

| ID／來源 | 日期、層級、用途 | bytes／SHA-256 |
|---|---|---|
| [B1：Our brand — Dr. Martens plc](https://www.drmartensplc.com/about-us/our-brand/) | undated；corporate_retrospective。Heritage：1945/1947/1959及英國改款；同一利益方回顧，非當期契約。 | 67800／`45a495b56d5ffd3934afb330d52f7727349aa9f1e7be3a1de95f7dd49f31834d` |
| [B2JP：History — Dr. Martens Japan](https://jp.drmartens.com/brand/history.html) | undated；corporate_retrospective。可保全的日文公司History；舊加拿大入口404；非獨立第二證人。 | 179867／`ae6eebd27b59fbaa7c6b1f9b043a3bdc1232da54fb39c1ea61bea17defd8b6de` |
| [B3：Creating an icon: The 1460 boot](https://www.drmartens.com/us/en/archive/1460) | undated；brand_product_archive_retrospective。1960-04-01首雙下線；下一週展會準備夏季生產訂單；不是首筆零售。 | 280332／`719804439f01d55dc47c7c70ef02a59ddace8fa9659c1e4189a1167bbd535c76` |
| [P1：Dr. Martens plc Prospectus](https://www.drmartensplc.com/application/files/9116/1191/9428/Dr._Martens_plc_-_Prospectus.pdf) | 2021-01-29；issuer_formal_disclosure。歷史章仍為回顧；IP與供應鏈為2021揭露當時機制。 | 11561404／`d2fd7561aa111f43459dc9f5a371e69c552d738fd460f3a79f3664e33176c521` |
| [M1：Boot; ankle boot — London Museum 95.525/6a-b](https://www.londonmuseum.org.uk/collections/v/object-91428/boot-ankle-boot/) | undated; object production date 1995；museum_collection_catalogue。館方對實物與歷史的後來說明；1995不是入藏/網頁刊年。 | 164999／`d4d87740a5a377102144ca71e2ef445a820f4418ee972b0f8ddf6e6006d0f517` |
| [A1：Double ‘Class’. On the Popularization of Dr. Martens — Arthur Crucq, Widok 31](https://www.pismowidok.org/en/archive/2021/31-visuality-of-social-classes/double-class-on-the-popularization-of-dr.-martens) | 2021; exact day not established；scholarly_analysis_and_author_memoir。研究者分析加個人荷蘭龐克圈回憶；不是六〇年代採購/動機原件。 | 123316／`fdd197ea939becd3a022cb9a5bcda7c6cb10998447382156654434a97b47dd0a` |
| [US3046679A_SCAN：US3046679A original patent facsimile](https://patentimages.storage.googleapis.com/95/9f/77/edb0fa9dffd8d7/US3046679.pdf) | 1962-07-31；contemporaneous_patent_original_facsimile。US original PDF p3 visually checked by researcher and parent subagent for dates/names/failure mode/proposed groove. Patent proposal is not adoption or independent test. | 703751／`5631ac56504e99edc14f71c675dd1c361845a38a28b0d0f6dbc4630f67012b72` |
| [DE808095C_HTML：DE808095C patent transcription and bibliographic record](https://patents.google.com/patent/DE808095C/en) | 1951-07-09；patent_text_mirror_not_facsimile_verified。Google text and metadata only; early original scan not obtained. No proof this patent was in 1959 licence; legal status not independently checked. | 74078／`838287fabec2d1cea2062177af76ed2954cc2cb4879f50cb6039b69567f65ab9` |
| [AT217902B_HTML：AT217902B patent transcription and bibliographic record](https://patents.google.com/patent/AT217902B/en) | 1961-10-25；patent_text_mirror_not_facsimile_verified。Google text and metadata only; early original scan not obtained. No proof this patent was in 1959 licence; legal status not independently checked. | 49904／`f228a55e5b120481716557abf26b33302d3acd24e9777846207456ea0e67b5bb` |
| [AT209762B_HTML：AT209762B patent transcription and bibliographic record](https://patents.google.com/patent/AT209762B/en) | 1960-06-25；patent_text_mirror_not_facsimile_verified。Google text and metadata only; early original scan not obtained. No proof this patent was in 1959 licence; legal status not independently checked. | 43788／`8db23db479b17371e16129e7affa2a44056bfc983eedd5ac84ae0ecf51926afc` |
| [T3_plc_product：Product - Dr. Martens plc](https://www.drmartensplc.com/sustainability/product/) | undated；corporate_current_technical_account。Contemporary company account. Temperature describes current welding operation; not the temperature experienced by a worn boot and not proof of 1945/1960 process. Durability, shock absorption, waste and environmental claims are company claims, not independent tests. Most footwear/Original products scopes must be preserved. | 82566／`42cf77198a9d4f84e767d84591fbc15e4e97c3adff134ec44237c271c61bea07` |
| [T2_sole_guide：Dr. Martens Sole Guide | Dr. Martens™](https://www.drmartens.com/eu/en_eu/dms-world/article/sole-guide) | undated；corporate_current_technical_account。Current product-family guide. Marketing descriptions; no independent durability/weight test. Does not prove 1945 or 1960 materials, machinery, or technique. | 415710／`ca10784a2f8279e175ad190fc1cad3810e7f3de7265e33bef92b373a98d75b1e` |
| [TEACH_T：Dr. Martens Product teach-in webcast transcript](https://www.drmartensplc.com/application/files/8716/9520/5561/Dr._Martens_plc__Product_teach-in_transcript.pdf) | 2023-09-14 event; PDF Last-Modified 2023-09-20；first_party_named_management_statement。具名原話：Adam Meek產品識別/材料；Tuze Mekik材料/修復；當時計畫不可當已完成。 | 638581／`e1b2da48e5c699f7c3b8a8d53310ec939f831b9f6e84235362c4df9aff279189` |
| [AR26：Dr. Martens plc Annual Report 2026](https://www.drmartensplc.com/application/files/5417/8038/8372/DOCs-AR26-web2.pdf) | 2026; board reports signed 2026-05-19; exact public-release day not established；issuer_annual_report。封面52週截至2026-03-29；HTTP Last-Modified 2026-06-02不是自動出版日。p63修復、p67材料試驗。 | 21630186／`d4d494022fa39959df66353d0bbf0a03508a0fc9f365fef09f713f70ab74d373` |
| [T7_repairs_resole：Resole and Welt - Classic DMS Sole (Per Pair) – Dr. Martens Repairs](https://drmartensrepairs.com/collections/welted-footwear-repairs/products/resole-and-welt-classic-dms-sole-per-pair) | undated; no datePublished/dateModified metadata found；authorised_service_partner_current_account。Authorised partner service description; current offering, no lifetime guarantee or universal repair claim. No historical technique evidence. | 650634／`96bf02e38a6214615de13b38a3dd6b0c0fa8ffa234286e8787274df44803a8ec` |
| [T6_repairs_faq：FREQUENTLY ASKED QUESTIONS | Dr. Martens Repairs](https://drmartensrepairs.com/pages/faqs) | undated; no datePublished/dateModified metadata found；authorised_service_partner_current_account。Current service terms may change; no historical evidence. | 194307／`b3fa94767a663d418b10a25a1c641592e00cb2c68b9b5b040ad9e97ec5d5a48c` |

## 同一物件可以增加的動作與取捨

以下是研究模組，不是章節定稿，也不是可直接配音的新文案。每項都有逐主張 source IDs／短摘錄／禁止推論。可按敘事需求取捨，不需全部塞入。

| 材料模組 | 原件能支持的具體推進 | 不可越界 |
|---|---|---|
| 腳下的問題與權利跨海 | B1/P1/B2JP：公司回顧腳傷、原型、1947生產與年長女性市場；B1稱1959英國製造權，B3給1960首雙下線及下一週準備接單。 | 1945/1947仍無同期原件；不把製造權、專利、首賣、首單合成一日。 |
| 有彈性，接縫反而承受反覆拉扯 | US3046679原始p3：柔軟外底在邊緣受力可從鞋面剝離；提出接合面附近平行槽，讓應力分布改變。可見動作是受力、剝離、改槽，並非只說更舒服。 | 1957申請、1962核准的方案，沒有證據這正是Griggs採用技術；也不可把現代外側刻槽直接說成該專利。 |
| 把接縫做成靴子的辨識處 | B1/B3/P1回顧圓鞋面、黃welt線、刻槽邊、拉環；T3現行說明先縫PVC welt，再把welt與底熱接。縫線和熱接各負不同工作。 | 歷史外觀可與現行解說分時對照，不重建1960設備；不說一條縫線穿透整個外底。 |
| 工作物件被刻意露出 | M1列工作場合與晚六〇年代採用；A1描述裁褲腳、熨褲、吊帶、擦亮靴。讓動作推符號，不再增加音樂團體清單。 | A1是研究者分析；不是每人的職業、心理、購買動機或鞋廠策劃。 |
| 換工廠後仍要做出認得出的接縫 | P1 p63：新製造夥伴導入可達一年，涉及專用設備、製程、IP；p203–204披露Airwair與家族授權方權利分工及樣品/工廠年檢。 | 限定2021機制；一年不是單雙靴工時；商標、專利、股權分開，不開財報支線。 |
| 底磨掉，上半部還能留下嗎 | 2023逐字稿p13–14為具名管理層對舊靴的描述；AR26 p63說專門結構需專門設備；授權DMS換底頁明說拆舊底、welt、縫線再重建。這能回扣先前接合難題。 | 不是每雙靴可修、20年壽命保證或全球服務；當前授權服務限英國，需依款式/鞋況。 |
| 可選的窄結尾限制 | T3承認多材料鞋履難回收；AR26 p67替代PVC仍有供量/成本問題，可用一兩句讓材料選擇保留代價。 | 不是已完整閉環或已完成2035/2040目標；10,000雙試驗不是全面替換。 |

容量建議只作作者的材料配額：起源/權利約300–450、具號專利接合問題450–700、英國靴的外觀與結構450–650、穿用與可見動作600–750、當代複製/權利約350–500、磨耗與專用換底600–800，另可用150–250說材料代價。區間約2,900–4,100；新作者可選約3,500有效正文。這些尚未寫成句子，不能把配額當實算或時間驗收。


## 舊句處理

`claims.json.existing_line_inventory` 列全部78句、現文、units、原主張ID、來源、可用/需修/可壓縮分流。重寫時可保留：1945/1947/1959的企業回顧歸因、B3下線與展會順序、M1晚六〇年代概述、A1裁褲腳與擦亮等實物穿法，以及M1的1995製造年。

- **c070207需精確化**：「鞋底裡那層會回彈的空氣」把結構簡成一層空氣。早期專利列彈性材料、空間、肋及不同實施例；AT217902B更明說某實施例不需密封，另有封閉實施例。應依具號專利或現行原廠說明，區分彈性底、空腔與接合；不畫成密封氣球。
- **c070309／309a可壓縮**：首賣與型號界線須保留，但不必用完整查核警語占正文；靠精確用字與一次歸因處理。
- **c070603–605可縮**：鞋帶只到作者八〇年代末荷蘭龐克圈回憶；不能變全球政治色碼，也不需要擴成一章。
- **c070607／607a、608／608a、609不能串新因果**：花卉客製、媒體、荷蘭店面及1995館藏分開；沒有手繪工法、同店同人或前者造成後者。B2JP把花卉段列八〇年代；B1/P1段落銜接較粗，不能拼出精確日期。
- **c070515保留「可能」**：相對省錢是研究者解釋，不是同期代表性購買調查。


## 數字、原件缺口和取捨

原始US掃描p3已由兩個研究者目視核對：1957-05-23申請／1962-07-31核准，三位發明人Klaus Maertens、Herbert Funck、Heinrich Götz。DE808095C、AT209762B、AT217902B只有Google轉錄及metadata，未取得可目視原掃描；其優先權、各國申請、公開/授權日期在JSON分欄。沒有證據把任何一件指定為1959授權標的，沒有建立1945專利註冊，也沒有核到世界第一氣墊鞋優先權。

1945樣鞋/醫療、1947生產帳、1959廣告與利用契約/專利清單、1960實物剖面和機器工法、首筆零售/訂單均未補到。查不到只是本次取得限制，不等於不存在。早期專利scan在DPMA遇CAPTCHA即停止；快取HTML不當PDF。

現行工廠頁的reader版本有clicking/closing/lasting與「trapping air」字句，但實際HTTP已導購物分類，沒有同正文bytes，因此本包**不使用**那些詳細動作或密封結論。可保全的PLC Product只支持PVC成型、air pockets與welt熱接等正文。其超過650°C是接合操作溫度，不是靴子耐熱標示；「不用黏著劑」只限接底程序。

後代財報不用來補正文：P1的1460占FY20營收42%不是雙數占比；2023產品教學約80%是特定DTC產品毛利，不是集團淨利率；11百萬雙產能與11.1百萬雙FY20銷售不同。AR26的4,287是FY26英國修復雙數；10,000雙是材料市場試驗。年報封面為截至2026-03-29的52週，不用3/31或網站更新日代換。


## 交付及未做項目

只寫本work資料夾的 `research.md`、`claims.json` 及raw來源/衍生摘錄快取；原repo各檔仍唯讀。paid/provider/backend/git呼叫均0，沒有新敘事、verify、翻譯、圖片/聲音生成、TTS或owner核准。後續新稿須自行實算並由另一位來源審查者覆核。

