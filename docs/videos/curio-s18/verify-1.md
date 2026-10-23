# curio-s18 查核第一輪

- 這一集的查核寫在 [`../history-curiosity/topic-checks/S18.md`](../history-curiosity/topic-checks/S18.md)（S18　拿破崙其實不矮？），
  逐列對過原文，另外經過一位獨立覆核者；旁白怎麼依查核改過、覆核推翻或加但書的列，都寫在那份檔案。
  每一句旁白對到哪一列，見 [`claims.md`](claims.md)。
- 這份檔案只是把那份查核的〈逐項查核〉表照抄過來，讓成片品管（`tools/video/qa/facts.mjs`）讀得到判定；
  兩份不一致時以 `topic-checks/S18.md` 為準。
- 判定沒有任何一列是 NOT FOUND：旁白不再使用的事實寫成「不用」，有爭議的寫成 DISPUTED 並在旁白裡說成有爭議。

## 逐項查核（抄自 `topic-checks/S18.md`，2026-10-19）

| # | 主張 | 判定 | 原文（引文） | 位置 | 來源 | 備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1821 年 5 月 5 日死在聖赫勒拿島，隔天驗屍 | CONFIRMED | 「Il est six heures moins onze minutes. Napoléon touche à sa fin … il n'est plus」；「Le cadavre était gisant depuis vingt heures et demie. Je procédai à l'autopsie」；英方報告「Longwood, St. Helena, May 6th, 1821」 | ANT pp. 149–160；ARN pp. 24–26 | ANT、ARN | |
| 2 | 驗屍的是他的私人醫生安托馬爾基，寫下五呎二吋四分 | CONFIRMED | 「4°. La hauteur totale, du sommet de la tête aux talons, était de cinq pieds deux pouces et quatre lignes.」；「J'étais médecin de Napoléon ; j'avais fait l'autopsie」 | ANT p. 158、p. 170 | ANT | 覆核：身高是解剖前核對的「remarques」，印在 1825 年的回憶錄裡，**沒有證據顯示 1821 年的報告裡就有**；旁白不再說「報告」，改「記下的身高」。「au nombre de huit」可能是連安托馬爾基共八名。英方報告沒有身高；Henry 寫「the stature was short and thick」（HEN p. 15），還記了門上的身高記號（他比拿破崙高兩吋） |
| 3 | 法制 pied ≈ 32.48 公分、pouce ≈ 2.707、ligne ≈ 0.226；換算約 168–169 公分 | CONFIRMED | 「Le pied de roi … se divisait en 12 pouces = 144 lignes … sa valeur légale est de 324.83958497 millimètres」 | DOU p. 408 | DOU；DUN「1m.686」 | 748 lignes × 2.2558 mm ≈ 168.7 公分 |
| 4 | 英制 foot 30.48、inch 2.54；照英制讀「5 呎 2 吋」約 157 公分 | CONFIRMED（算術） | — | — | WP | 157.5 公分（加四分作十二分之一吋則約 158.3）。**沒有史料說當時有人這樣讀**；NG 只說混淆「seems to stem」部分來自兩種尺 |
| 5 | 當時法國成年男性平均約 164–165 公分 | CONFIRMED | 「The average height of recruits of this age bracket born at the end of the century was 1636 mm」「about 1646 mm」 | KOM pp. 9–10 | KOM（引 Weir 1997） | 卡片改寫出處 |
| 6 | 其他當時的紀錄也差不多（貼身男僕康斯坦） | CONFIRMED | 「Sa taille était de cinq pieds deux pouces trois lignes」 | CON p. 53 | CON | 約 168.5 公分；馬爾尚回憶錄也寫五呎二吋四分（DUN 轉引） |
| 7 | 吉爾雷把他畫成矮小、愛發脾氣的「小波尼」 | CONFIRMED | 〈Maniac-Raving's – or – Little Boney in a Strong Fit〉，1803-05-24：「Napoleon Bonaparte stamps in fury, right arm outstretched with clenched fist … huge plumed cocked hat lies on the floor」 | LOC 94509079；雪菲爾 38419 | LOC | 1803 年至少五張標題有「Little Boney」，最早是 1803-01-01 的〈German-nonchalence〉。圖裡是**揮拳**，劍是斷的：旁白「揮著劍」改「揮著拳頭」 |
| 8 | 吉爾雷死於 1815 年 | CONFIRMED（二手） | 1756-08-13 – 1815-06-01 | — | WP | 滑鐵盧在 6 月 18 日，「同一年」成立 |
| 9 | 英國漫畫在戰爭期間一直把他畫小 | CONFIRMED（二手） | 「La légende du petit grand-homme est la mine qu'à partir de la rupture de la paix d'Amiens, ont exploitée la propagande britannique et ses caricaturistes contre « le petit Boney »」 | DUN | DUN；LOC 各張版畫 | 覆核：DUN 說英國「ont exploitée」（利用）這個傳說，不是發明；法文裡也有「le Nabot」。旁白「在海峽對面誕生」改「把他畫成矮子的，主要在海峽對面」 |
| 10 | 近衛擲彈兵有身高下限 | CONFIRMED（**數字改**） | 「Avoir la taille d'un mètre 8 décimètres (5 pieds 6 pouces) au moins pour les grenadiers」 | PER p. 53（共和十年風月十七日／1802-03-08 執政令第 33 條） | PER；Peuchet「un mètre 786 millimètres」 | 下限是五呎六吋（約 178 公分），不是清單寫的五呎十吋。覆核：PER 也收了 1804-07-29 的敕令（近衛軍步兵 1.760 m＝5 呎 5 吋）與 1815-04-08 敕令第 47 條（擲彈兵 5 呎 5 吋），下限約 176–178 公分，「比一般人高出一大截」成立。「全國最高」說過頭，改「特別高」；「永遠」改「常常」 |
| 11 | 「小下士」源自 1796 年洛迪之後，是親暱的稱呼 | CONFIRMED（但書） | 「après chaque bataille, les plus vieux soldats se réunissaient en conseil, et donnaient un nouveau grade à leur jeune général … Il fut fait caporal à Lody … de là ce surnom de petit caporal」 | LAS pp. 181–182 | LAS | **覆核推翻歸屬**：這段沒有引號，是拉斯卡斯自己的敘述，不是拿破崙說的話（前一段拿破崙的話在「…mon Musée de Paris, etc., etc.」結束）；他給的理由是「Sa jeunesse … ou toute autre cause」。WP 引 Dwyer 2004：沒有當時的證據。Las Cases 沒有把外號跟身高連在一起。旁白改成「陪他到島上的拉斯卡斯在書裡寫」 |
| 12 | 樸素的灰大衣與不插羽毛的帽子 | CONFIRMED | 「la redingote grise si fameuse」；帽子「Il n'y portait ni glands, ni torsades, ni plumes」 | CON pp. 90、95–96 | CON；napoleon.org（二手）「On le reconnaissait ainsi plus aisément au milieu de son brillant état-major」 | 二手說的是**更好認**，跟稿子原本「越不起眼」相反，旁白照改 |
| 13 | 「拿破崙情結」二十世紀才出現，跟阿德勒的「自卑」有關 | **DISPUTED** | 1923-04-07《Washington Daily News》：「Porter has a Napoleon Complex [delusion] of grandeur」；MW「First Known Use: 1924」 | LOC 報紙掃描；MW | LOC、MW | 1923 年的用法是「自大狂」，不是「矮個子補償」；MW 1924 是現在這個意思。覆核補：《Red Book Magazine》1923 年 4 月號也有「It's all very well to get the Napoleon complex and think you own the earth」，所以是「報刊」；阿德勒 1912 年的書提到 Napoleon 是在講英雄崇拜。**沒有找到是阿德勒或他的學生取名的證據**。旁白改成「目前查得到最早的，在一九二三年的美國報刊上；那時候它說的是自以為了不起，還跟個子無關」「後來這個詞才專門拿來說矮個子」 |
| 14 | 2007 年中央蘭開夏大學：矮個子沒有比較易怒；2018 年另有研究結論不同 | CONFIRMED（但書） | KNA 摘要：「shorter men keep more resources to themselves … shorter men are not more likely to show direct, physical aggression toward a taller opponent」 | KNA；WP〈Napoleon complex〉（引 BBC 2007） | KNA；WP | 2007 年的只有二手（BBC 頁面連不上、沒有找到論文）。兩個研究不是「互相矛盾」：2018 年也發現矮個子不會比較愛動手，差在分資源。旁白改成各說各的發現 |
| 15 | 拿破崙生於 1769 年 | CONFIRMED（二手） | 1769-08-15 | — | WP | 洛迪時二十六歲 |
| 16 | 聖赫勒拿島在南大西洋 | CONFIRMED | — | — | 一般知識 | 距離旁白沒用 |
| 17 | 1840 年遺體運回巴黎 | 不用 | — | — | — | 旁白已拿掉 |
| 18 | 1821 年法國已有公尺 | CONFIRMED | 共和八年霜月十九日法（1799-12-10）把公尺定為「3 pieds, 11.296 lignes」 | Hallock & Wade 1906, p. 63 | 二手引法條 | |
| 19 | 1812 年允許「常用單位」沿用呎、吋等舊名稱 | CONFIRMED（**旁白拿掉**） | 「un pied usuel de 12 pouces ou 144 lignes, égal au tiers du mètre」 | DOU p. 601 注、p. 408 | DOU | 名稱沿用但**長度改成三分之一公尺**。驗屍用哪一種沒有史料說明；照日常用呎是約 173 公分。康斯坦（第 6 列）與達林、梅特蘭（第 21 列）都跟舊制對得上；覆核補：PER 收的 1804–05 年敕令把「5 pieds 2 pouces」寫成「un mètre 678 millimètres」，可見拿破崙政府的公文用舊制（只證明 1812 年以前）。稿子原本那一句暗示單位沒變，拿掉；覆核後旁白加一句「照一八一二年以後的日常用呎，他還會再高四公分」，並把「法國的一呎」改「法國舊制的一呎」 |
| 20 | 一吋十二分，四分是三分之一吋 | CONFIRMED | 「12 pouces = 144 lignes」 | DOU p. 408 | DOU | |
| 21 | 島上的英國人用英制記下五呎七吋 | CONFIRMED（二手引一手） | 「le Journal d'Andrew Darling, tapissier anglais qui fut chargé de prendre des mesures exactes … taille 5 pieds, 7 inches », soit (mesures anglaises) … =1m.70」 | DUN 轉引 1963 年《Bulletin … de Sainte-Hélène》 | DUN | 記的是**英國工匠（室內裝潢工）達林**，不是醫生；覆核：Chaplin《St. Helena Who's Who》1914「On the death of the Emperor, Darling was the undertaker」，量的是遺體。旁白改「替他辦後事的英國工匠」。另一個英制數字：梅特蘭「a remarkably strong, well-built man, about five feet seven inches high」（MAI，1815 年，他還活著），旁白 np322 改用這一句 |
| 22 | 今天台灣成年男性平均約 172 公分 | 不用數字 | — | — | — | 旁白只說「他確實不算高」 |
| 23 | 洛迪橋約兩百公尺，對岸有奧地利砲兵 | CONFIRMED | 「trente pièces de canon de position défendaient le passage du pont … l'on se présenta sur le pont, qui a cent toises de longueur」 | CORR no 382, pp. 260–261 | CORR | 一百 toise ≈ 195 公尺：「兩百多公尺」改「將近兩百公尺」 |
| 24 | 老兵「投票」把他升為下士 | CONFIRMED（傳說） | 見第 11 列 | LAS | LAS | |
| 25 | 吉爾雷作品上千張，從未見過拿破崙 | CONFIRMED（二手） | 「nearly 1000 prints」；「Gillray never saw Napoleon in person」 | james-gillray.org；NG 2023 | 二手 | 「上千張」改「將近一千張」 |
| 26 | 1805 年〈The Plumb-pudding in Danger〉 | CONFIRMED | 「Pitt, very tall and thin … Napoleon, sturdier and much shorter, has to stand up from out of his chair to reach the pudding」；1805-02-26 | 雪菲爾 38497；LOC 2001695072 | LOC | 覆核：原文「sturdier and much shorter」，「又矮又小」改「又矮又壯」 |
| 27 | 〈The King of Brobdingnag and Gulliver〉 | CONFIRMED | 「King George III … holding a tiny Napoleon on the palm of his right hand and inspecting him through a spy-glass」；1803-06-26，「after Lieutenant Colonel Thomas Braddyll」 | 雪菲爾 38425；LOC 95501581 | LOC | 是 1803 年，比布丁那張早；旁白只說「另一張」 |
| 28 | 英國報紙稱他「科西嘉的小個子」 | CONFIRMED（**改成版畫**） | 〈Pidcock's grand menagerie … Buonaparte, the little Corsican monkey〉1803-08-27；吉爾雷〈The new dynasty … the little Corsican gardiner〉1807 | LOC 2006681988、2006684697 | LOC | 沒有找到英國報紙的例子：旁白「報紙也跟著叫他」改「別的版畫也叫他」（覆核：1807 年那張是吉爾雷自己的，1803 年那張是別人的） |
| 29 | 法國政府曾就英國報紙與漫畫正式抗議 | CONFIRMED（**只有報紙**） | Otto 1802-08-17：「That His Majesty's Government will adopt the most effectual Measures to put a Stop to the unbecoming and seditious Publications with which the Newspapers and other Writings printed in England are filled」 | PAP | PAP | 這批文件裡沒有「caricature」。旁白改成「法國政府曾經正式要求英國，管一管那些罵他的報紙」 |
| 30 | 1815 年夏天柏勒洛豐號，大批小船出來看他 | CONFIRMED | 「upwards of a thousand were collected round the ship, in each of which, on an average, there were not fewer than eight people」 | MAI pp. 138–139（1815-07-30，普利茅斯灣） | MAI | 「幾千個英國人」改「上千艘小船、好幾千個英國人」 |
| 31 | 克魯克香克繼續畫「小波尼」 | CONFIRMED | 〈Little Boney gone to pot〉1814-05-12；〈Complements & congées or little Boney's surrender〉1815-07-24 | LOC 2006687894、2006688719 | LOC | |
| 32 | 傷兵院的石棺 | 不用 | — | — | — | 旁白已拿掉 |
| 33 | 阿德勒二十世紀初在維也納提出「自卑」 | CONFIRMED（但書） | 《Studie über Minderwertigkeit von Organen》1907；《Über den nervösen Charakter》1912（「Minderwertigkeitsgefühl」） | archive.org 兩書 | 一手書目 | 「自卑情結」這個詞較晚才通行；旁白改說「阿德勒的理論」 |
| 34 | 「Napoleon complex」收在英文字典裡 | CONFIRMED（**只有韋氏**） | 「a domineering or aggressive attitude perceived as a form of overcompensation for being physically small or short —not used technically」 | MW | MW | 牛津學習辭典、劍橋查無此條：旁白「連英文的字典裡都查得到」改「美國的韋氏字典裡就查得到」 |
