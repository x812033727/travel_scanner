# curio-s19 查核第二輪（獨立查核，新稿）

- 查核日：2026-10-31。查核者沒有參與撰稿，只讀不改稿。
- 對象：`<repo>/docs/videos/curio-s19/video.json` 新稿 144 句與卡片、標題、縮圖、`youtube.description`、`loops`、`claims.md`；舊稿用 `e78c725cf` 比對，新句與改過的句子先查。
- 對照表：`<repo>/docs/videos/history-curiosity/topic-checks/S19.md` 第 1–45 列與〈獨立覆核〉。

## 結論：有條件通過

主幹站得住：合約沒有期滿拆除條款、1903 年詢問與 1906 年書面報告、1906／1908／戰爭條款／1946 年的四段延長、1909 年沒有拆塔的紀錄，抽查的引文都對得上原文。查核表標「不入旁白」或被覆核推翻的列（第 2、12、32、40 列）沒有被用到；第 23 列只以「後來流傳說」出現並當場點破，符合該列備註。

**必須改的是一條新加的線：「那場賭」（ef206、ef414、ef823–ef825）。**旁白說遊客掉了、賭看起來要輸了，可是同一本書、同一個第五部寫著股本在 1889 年一年內就全額還清。這條線不改不算通過。其餘是過強兩處與措辭六處。

統計：錯誤 1 組、過強 3 條（ef206 算進過強，與錯誤那組同一條線）、措辭 6 條。

## 問題表

| 行 id | 旁白原文 | 問題 | 依據 | 建議改法 | 嚴重度 |
| --- | --- | --- | --- | --- | --- |
| ef414（連帶 ef823、ef824–ef825 的回收，與 `loops` 裡 ef206→ef824、ef414→ef825 兩條） | 你要是那個賣票的，看到這數字大概也會慌；那場賭，看起來要輸了。 | 這句沒有標「我覺得」，而且跟來源相反。到 1898 年這場賭早就贏了：股本 510 萬法郎在 1889 年全額還清，之後的利潤才對半分。1898 年全年收入仍有約 36 萬法郎。`claims.md` 掛第 21 列「同上」，第 21 列只有人次，撐不住「要輸了」。 | EIFFEL1900 第五部（看了頁面圖）p. 227「le capital primitif ayant été intégralement remboursé dès la première année」；p. 232「Les bénéfices nets de l'exercice 1889 s'élèvent donc à 5.551.036,47 fr」「il a été prélevé 5.100.000 fr pour le remboursement intégral du capital social」；同頁表 1898 年合計 361.700,35。另 MORICE1936 p. 87（與 ef103 同一段報告）寫 1889–1905 年的淨利約 300 萬法郎、三分之一多分給股東 | ef414 改：「你要是那個賣票的，看到這數字大概也會慌；可是公司的本錢，五百一十萬法郎，一八八九年那一年就全還清了。」ef415 接得上。ef823 改：「還記得一年只剩十八萬人嗎？」ef824–ef825 內容不動。兩條 `loops` 的 `what` 與 `bet` 那一景的文字要一起改。S19.md 新增一列（見下〈建議新增的列〉） | 錯誤 |
| ef206 | 我覺得這比較像一場賭：要把錢賺回來，這座塔就得一直有人爬。 | 「我覺得」只蓋得住「像一場賭」，後半「得一直有人爬」是事實前提，與上一列相反：只爬了 1889 年 5 月到 11 月就回本。`claims.md` 把它列為「不帶新事實」，也不對。 | 同上；EIFFEL1900 p. 227「ce n'est que le 15 mai que la Tour fut ouverte au public」 | 改：「我覺得這比較像一場賭：錢回不回得來，全看有沒有人肯爬。」把這句移出「不帶新事實」清單 | 過強 |
| ef610、ef611 | 到了十二月，艾菲爾把塔借給陸軍做實驗，帶頭的是費里耶上尉，底下只有幾個人。 | 撰稿者提醒的那列。查到的分兩半：「1903 年、艾菲爾、把塔交給軍方做第一批試驗」有當年的書（Rothé 1913，表中第 27 列沒引這句），不再只有二手；「十二月」「費里耶帶頭」「幾個人」仍只有 UFF2011（無註腳）。旁白把這三點講成確定。「借」也跟 ef208「塔歸巴黎市」小有衝突；Rothé 的字是「mise à la disposition」。 | ROTHE1913 p. 7「Ce n'est, en effet, qu'en 1903 que la Tour fut mise à la disposition de l'autorité militaire par M. Eiffel, pour les premiers essais.」下句「cabanes de planches」；UFF2011 p. 33「In December 1903, Eiffel offered the use of his Tower … A handful of military engineers, under the direction of Captain (later General) Gustave Ferrié」。Boulanger、Ferrié《La télégraphie sans fil et les ondes électriques》第 5 版 archive.org OCR 檢索「Eiffel」0 筆，沒有幫助（可能是 OCR 問題，沒有逐頁看） | ef610 改：「同一年，艾菲爾讓陸軍上塔，做第一批無線電試驗，器材就放在木板小屋裡。」ef611 改：「一篇軍史專文說，那是十二月，帶頭的是費里耶上尉，底下只有幾個人。」第 27 列補 ROTHE1913；說明欄界線改成「1903 年有 Rothé 1913；十二月與費里耶上尉只見於二手專文」 | 過強 |
| ef712 | 一篇法學論文說：到這一步，留或拆，再也沒有人提了。 | 「再也沒有人」比原文強。原句是第五章開頭，講 1908 年這次談判的議題已經不是留或拆，不是說此後沒有人再提；而且下面 ef718 自己就引了 1909 年還有報紙在傳要拆。 | MORICE1936 p. 93：「Avant même que les modifications de l'année 1906 fussent entrées en vigueur, des pourparlers étaient engagés … Il n'est plus question ni de l'harmonie du jardin du Champ-de-Mars, ni de la conservation ou de la démolition de la tour Eiffel.」 | 改：「一篇法學論文說：談到這次延期，已經不再談留或拆了。」 | 過強 |
| ef824 | 內政部後來說，那五十年，平均每年五十萬人； | 「那五十年」前面沒有交代是哪五十年，改掉 ef823 後更懸空。原文也只說「過去」的五十年，沒寫起訖年。卡片 sub「前五十年」同樣是推定。 | COUR1956 內政部答覆：「des résultats d'exploitation du passé. Pendant cinquante ans, la Tour Eiffel avait reçu en moyenne, chaque année, 500.000 visiteurs」 | 改：「內政部後來說，一九四六年以前的五十年，平均每年五十萬人；」卡片 sub 同步寫「1946 年以前的五十年」 | 措辭 |
| ef703 | 一九〇八年，陸軍部要把天線，直接掛上塔頂； | 1908 年要把永久電台的天線固定到塔頂，有 MORICE 撐；但「直接掛上」聽起來像第一次。1903 年起的臨時電台，天線已經拉到塔的第三層。 | MORICE1936 pp. 94–96「6 fils réunis au sommet de la Tour」「il était indispensable … que les fils d'antennes soient reliés au sommet de la Tour」；UFF2011「the antenna consisted of a wire that stretched through the air to the third and highest floor」 | 改：「一九〇八年，陸軍部要蓋永久的電台，六條天線全拉到塔頂；」 | 措辭 |
| ef312 | 記者提醒他：他們反對的，是博覽會之後，塔還要一直立著。 | 原文是「立二十年」。「一直」把期限講沒了，而這正是本集的主線。 | TEMPS1887「son maintien pendant vingt ans après l'Exposition」 | 改：「…是博覽會之後，塔還要再立二十年。」 | 措辭 |
| ef607 | 軍事上，陸軍正在塔上試光學通訊，聯絡盧昂和楓丹白露； | 原文是完成式，且試的是「可不可能」，不是已在聯絡。 | MORICE1936 p. 90「a fait procéder à des expériences sur la possibilité d'établir des communications optiques … jusqu'à Rouen et Fontainebleau」 | 改：「軍事上，陸軍試過光學通訊，看能不能聯絡到盧昂和楓丹白露；」 | 措辭 |
| ef409、ef410 | 可是他一八九〇年自己寫的，是朋友老約他上塔吃飯，他乾脆離開巴黎：因為艾菲爾鐵塔讓我煩透了。 | 引文都對，但把「約吃飯」接成離開的原因，是旁白接的。他第一段緊接著就說不只是塔，還有塔周圍的一切。「朋友約吃飯」在原文相隔好幾段。不必改事實，只是不要讓它聽成因果。 | MAUP1890 第一章「Ce n'est pas elle uniquement d'ailleurs qui m'a donné une irrésistible envie de vivre seul」「tout ce qu'on a fait autour d'elle」 | 可留；若要更穩，ef410 改：「他還是離開了巴黎，書的第一句就寫：因為艾菲爾鐵塔讓我煩透了。」 | 措辭 |
| ef105 | 更怪的是，這座塔的合約裡有一條，只有打仗才會用上； | 第 13 條是「戰爭或宣布戒嚴」，「只有打仗」少了戒嚴。art13 卡片寫對了，所以很輕。 | CONV1887 第 13 條「En cas de guerre ou de déclaration d'état de siège」 | 可留（開場鉤子）；不改也可以 | 措辭 |

## 查過、沒問題的

新句抽查，都開了原文（不只看查核表引文）：

- **合約**（Wikisource 七頁轉寫）：ef204 分三次付（第 7 條）、ef205、ef208–ef210（第 11 條；同條另有「sans qu'il puisse être exigé … de réfections spéciales」，不影響「保養好再交回」）、ef212、ef213–ef215（第 2 條 1886 年 11 月 6 日）、ef815（第 13 條）。
- **《Le Temps》艾菲爾訪談**（Wikisource 轉寫 pp. 4–8）：ef203「entre cinq et six millions」、ef311（「si tard」「tous nos contrats sont passés」「les fondations sont posées」）、ef314、ef315、ef316。
- **EIFFEL1900**（OCR；pp. 227、231、232 看了頁面圖）：ef216–ef217（註腳「L'un des riverains」「perdu en première instance … ne fut pas suivi en appel」）、ef308–ef309（Lockroy 信）、ef401–ef402（一點半到兩點半）、ef405–ef406（「banquet de Scientia」、1889 年 4 月 13 日；他接著說要「en appeler de ma propre sentence」，所以 ef404 的回答站得住）、ef412–ef413、ef502（第六部第 IV 章 Hénocque 的表有登塔前後的脈搏欄，受測者還有艾菲爾本人；`claims.md` 可補這個出處）、ef503–ef508。
- **MORICE1936**（archive.org OCR）：ef103–ef104、ef604–ef606、ef608、ef612、ef614–ef616、ef618（「redevance annuelle fixe de 5.000 francs」，自 1910 年起）、ef619（「remplacement des balustres cassés au pourtour du premier étage」）、ef706–ef708（p. 95「dix-huit ans」）、ef710（5 月 15 日）、ef713（「à 200 mètres environ」）、ef813、ef816–ef817（p. 112）、ef819（「peut-être」保留了）。
- **TURPAIN1908**：ef702。**ROTHE1913**：ef804、ef805、ef809、ef811。**BDL1915**：ef714、ef716。
- **COUR1956**（JO 1956-02-29 archive.org OCR）：ef820、ef822、ef825。
- **MAUP1890**：ef409、ef410。

其他：

- 標題、縮圖 `headline`／`sub`、片尾 ef901、卡片都沒有比紀錄強；標題是問句，ef901 掛「紀錄裡」。`youtube.description` 只需要改費里耶那半句（見上表）。
- 開場承諾都兌現：ef105–ef106→ef812、ef107→ef806–ef809、ef104→ef826、ef108（翻到 1980）→ef822、ef109→ef802。
- 算術都對：1887＋27＝1914；1887→1980＝93 年；1 月 8 日到 2 月 14 日是 37 天；3 月 31 日到 4 月 13 日是 13 天；九成：1 − 183,391／1,968,287＝90.7%；1908＋18＝1926，比 1915 多 11；十九季又三十天＝20 段＝20 年。
- `claims.md`：程式比對 144 句全部出現在表內（116 句）或「不帶新事實」清單（28 句），沒有漏列、沒有多列；列號抽查（ef101、ef204、ef401、ef607、ef708、ef712）都對。例外只有上表的 ef206、ef414。
- `verify-1.md` 寫「DISPUTED 的第 23 列不講」，新稿 ef408 講了（掛「後來流傳說」，合第 23 列備註）。`verify-1.md` 這句已過時，但照指示不動。

## 建議新增的列（給 S19.md）

**46　股本第一年就還清（本輪新增）**：EIFFEL1900 第五部 p. 226–227「Le fonds social est fixé à 5.100.000 fr」「le capital primitif ayant été intégralement remboursé dès la première année」；p. 232「Les bénéfices nets de l'exercice 1889 s'élèvent donc à 5.551.036,47 fr」「il a été prélevé 5.100.000 fr pour le remboursement intégral du capital social」。CONFIRMED（看了 pp. 227、232 頁面圖；6,523,847.40 − 972,810.93 ＝ 5,551,036.47）。注意：還清的是公司股本 510 萬法郎，不等於整座塔的造價。

第 27 列補：ROTHE1913 p. 7（原文見上表），1903 年與艾菲爾不再只有二手；十二月、費里耶、人數維持二手。

## 開了哪些來源

fr.wikisource（合約七頁、艾菲爾訪談 8 頁，`action=raw`）；archive.org：`n-0106381-pdf-1-400`（EIFFEL1900 全文與 pp. 227、231、232 頁面圖）、`IA41551407_0021`（MORICE1936）、`latlgraphiesans00turpgoog`、`latlgraphiesans00boutgoog`、`lesapplicationsd00roth`、`WirelessTimeSignals`、`MI201104275.`、`sim_journal-officiel-de-la-republique-francaise_1956-02-29_50`、`la-telegraphie-sans-fil-et-les-ondes-electriques`；Project Gutenberg #14793。

**這輪沒開的**：LOC 兩份報紙（*Rawlins Republican* 1909-08-28、*New-York Tribune* 1910-01-23；loc.gov 與 chroniclingamerica 都回 Cloudflare 驗證頁，沒有繞過），所以 ef107、ef718、ef806–ef807 只對到查核表與 10-20 覆核重抓的引文，「美聯社」這個掛名這輪沒有親眼看到；〈Les artistes contre la tour Eiffel〉抗議書本文（ef302–ef305）與 EIFFEL-AIR（ef510）沒有重開，沿用查核表看過掃描的引文。Gallica 與《Rapports et Documents》原件沒試，仍是 MORICE1936 轉引，說明欄已寫明。
