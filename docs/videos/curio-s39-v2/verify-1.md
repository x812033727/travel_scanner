# curio-s39-v2 查核第一輪（沿用第一版的查核）

- **第二版沒有新增查核。** 這一集第一版（站上的 `curio-s39`）的查核由 Codex 在雲端做，檔案不在 repo 工作樹：`research.md`（六份固定全文，各附 commit 與 SHA-256，
  2026-10-20 逐段重開原文）、`claims.md`（89 句旁白逐句對到來源代號）、`verify-1.md`～`verify-11.md`（R1–R4a 的作者自查與獨立覆核交接）。
  獨立覆核的結果：R3 來源與畫面稽核 89/89 主張通過；R4 六句聽辨改寫後，新讀者重開五份固定原文，六句改寫與 89/89 主張對齊通過（`verify-10.md`）。
  第一版沒有 `topic-checks/S39.md`，所以這份檔案把第一版 `research.md` 的來源表、R3 補核的界線、故事界線，與第一版 `claims.md` 的逐句表照抄過來，
  讓成片品管（`tools/video/qa/facts.mjs`）讀得到判定；判定欄是這份檔案加的，依上面兩次獨立覆核：89 句全部 CONFIRMED，沒有 NOT FOUND。
- 第二版的旁白每一句對到哪一列，見 [`claims.md`](claims.md)；新加的事實句只用下表已有的列（`SU-L` 80.4 的卡西烏斯、`SU-L` 83.2 的遺囑、`SHA` L1694–1711 的高喊自由與安撫旁人、
  `SU-T` L1689–1709 的英譯正文 some authors relate），標「第二版新加」。
- 第一版沒有用、第二版也不用的：遺體由三名僕人搬回、醫師認為第二處胸口傷致命（`SU-L` 82.2–3；第一版 R1 判成岔題，畫面也不畫傷與遺體）；章 81 的夢與預兆只說「傳記裡的故事」。

## 來源與段落（抄自第一版 research.md，查核日 2026-10-20）

| 代號 | 固定全文與雜湊 | 已讀段落與能支持的事 | 限制 |
| --- | --- | --- | --- |
| `SU-L` | [PerseusDL, Suetonius, *Divus Iulius* 80–85, Rolfe 拉丁文本](https://github.com/PerseusDL/canonical-latinLit/blob/128a05afa9cc7179ab18f8d05f78a9f1dd50e415/data/phi1348/abo011/phi1348.abo011.rolfe-lat1.xml#L587-L638)。commit `128a05afa9cc7179ab18f8d05f78a9f1dd50e415`，XML SHA-256 `cd81ab500674c637e204b17e14a58b8bccd24a3087d96171d04d7d5ecb8ee0fc`。 | [80.4, L594–595](https://github.com/PerseusDL/canonical-latinLit/blob/128a05afa9cc7179ab18f8d05f78a9f1dd50e415/data/phi1348/abo011/phi1348.abo011.rolfe-lat1.xml#L594-L595)：六十餘同謀，領導者含 Gaius Cassius、**Marcus Brutus 和 Decimus Brutus**；計畫選在三月十五日龐培會議廳。 [81.4, L604–605](https://github.com/PerseusDL/canonical-latinLit/blob/128a05afa9cc7179ab18f8d05f78a9f1dd50e415/data/phi1348/abo011/phi1348.abo011.rolfe-lat1.xml#L604-L605)：Decimus 勸他赴會，路人遞陰謀警告，他和其他紙張混放，說會稍後讀。 [82.1–4, L607–615](https://github.com/PerseusDL/canonical-latinLit/blob/128a05afa9cc7179ab18f8d05f78a9f1dd50e415/data/phi1348/abo011/phi1348.abo011.rolfe-lat1.xml#L607-L615)：Cimber 扯袍，凱撒先喊 `Ista quidem vis est!`；受第一刀時僅呻吟，後有 `etsi tradiderunt quidam`（但有些人傳說）他對迎上來的 Marcus Brutus 說 `καὶ σὺ τέκνον`；共二十三傷，遺體後由三名僕人搬回；醫師認為第二處胸口傷致命。 [83.2, L620–621](https://github.com/PerseusDL/canonical-latinLit/blob/128a05afa9cc7179ab18f8d05f78a9f1dd50e415/data/phi1348/abo011/phi1348.abo011.rolfe-lat1.xml#L620-L621)：遺囑把 Decimus 列為後順位繼承人，把部分刺殺者列為可能出生兒子的監護人。 | 原文的 `καὶ σὺ τέκνον` 是**希臘語**，可直譯「你也，孩子？」；既沒有拉丁語 `Et tu, Brute?`，引語本身也沒有喊出 Brutus 的名字。`etsi tradiderunt quidam` 保留「有些人傳說」這一層；不能說 Suetonius 作了目擊證言，也不能把其「只有呻吟」說成凱撒整天都沒說過話。章 81 的夢與預兆是作者轉載的敘事，不把神諭講成實證。醫師認為第二傷致命，是他在作者筆下的判斷，非今日驗屍。 |
| `SU-E` | [同一 PerseusDL 版本的 Rolfe 英譯](https://github.com/PerseusDL/canonical-latinLit/blob/128a05afa9cc7179ab18f8d05f78a9f1dd50e415/data/phi1348/abo011/phi1348.abo011.rolfe-eng1.xml#L1948-L2044)，XML SHA-256 `64e8e818ac27e67f7b4700c6dc954c7b693f20d9071725743a84ab5f08835305`。 | [82.2, L2027–2037](https://github.com/PerseusDL/canonical-latinLit/blob/128a05afa9cc7179ab18f8d05f78a9f1dd50e415/data/phi1348/abo011/phi1348.abo011.rolfe-eng1.xml#L2027-L2037)：「uttered not a word, but merely a groan at the first stroke, though some have written ... said in Greek ... You too, my child?」英譯協助核對希臘語的稱呼與拉丁語的保留語氣。 | 英譯是譯者的語句，不代替原文；本集不把「my child」拿去斷言 Marcus Brutus 是凱撒親生兒子。 |
| `SU-T` | [GITenberg, Thomson/Forester《十二凱撒傳》全文](https://github.com/GITenberg/The-Lives-of-the-Twelve-Caesars-Complete_6400/blob/bb5afc956095e248b2287cce2a4d3ebe394e5d31/6400.txt#L1637-L1755)。commit `bb5afc956095e248b2287cce2a4d3ebe394e5d31`，SHA-256 `082eee2d55230c1f75f9476dae537fc37851487bc1cce5dfaef1ef2a67558b15`。 | [正文 L1689–1709](https://github.com/GITenberg/The-Lives-of-the-Twelve-Caesars-Complete_6400/blob/bb5afc956095e248b2287cce2a4d3ebe394e5d31/6400.txt#L1689-L1709)同樣保留「some authors relate」。**該版本的譯者／編者腳註** [L18375–18392](https://github.com/GITenberg/The-Lives-of-the-Twelve-Caesars-Complete_6400/blob/bb5afc956095e248b2287cce2a4d3ebe394e5d31/6400.txt#L18375-L18392)自稱更可能是拉丁語 `Et tu Brute!`。 | 腳註是後來**編者的推測**，不能倒灌為 Suetonius 原文或公元前一世紀的現場證詞。腳註還補了不同手稿讀法，這也限制了對古代措辭的過度自信。 |
| `PL-C` | [GITenberg, Plutarch, *Caesar*](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L46780-L46975)。commit `6aea7c6d83ee3596f9106d2d832d705aa4ed4620`，全文 SHA-256 `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`。 | [L46821–46883](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L46821-L46883) Calpurnia 勸留下、Decimus 勸去、有人遞警告；[L46897–46946](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L46897-L46946) Antony 被門外拖住，Cimber 扯衣，Casca 先刺；凱撒對 Casca 先用**拉丁語**發話，Casca 用希臘語向兄弟求救；有些說法是凱撒見 Brutus 拔刀便蒙面倒在龐培像腳邊；馬爾庫斯欲解釋，元老們卻逃散。這一段**沒有** `Et tu, Brute` 或希臘語 `καὶ σὺ τέκνον`。 | Plutarch 是事後傳記，亦在多處標「有人說」；對見 Brutus 後的反應，**不應**硬套為在場攝影。劇本只說該記述沒有那句台詞，不從「未寫」推成絕不曾說。 |
| `PL-B` | [同全文，Plutarch, *Brutus*](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L63906-L64177)。 | [L63906–63920](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L63906-L63920)馬爾庫斯的聲望使其他人想借重他；[L64042–64141](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L64042-L64141)佈置於龐培廊廳、Brutus 參與、等候時誤疑走漏、元老與凱撒談話；[L64144–64180](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L64144-L64180)凱撒看見 Brutus 持刀、放開 Casca 手、蒙袍受擊；馬爾庫斯試圖向元老說明而眾人逃散，未給凱撒對 Brutus 的最後一句。 | 同一作者的兩篇傳記不是兩名獨立現場目擊者；只當互相核對場景與作者的敘述選擇。 |
| `SHA` | [GITenberg, Shakespeare, *Julius Caesar* III.i](https://github.com/GITenberg/Julius-Caesar_1120/blob/61f9979ce377707e385fdd4e0b48b0383b857524/1120.txt#L1648-L1711)。commit `61f9979ce377707e385fdd4e0b48b0383b857524`，SHA-256 `0df49e211e16bc5ec1dabaf4b031bb60806a110754f3c0bf511e19594d590ce4`。 | [L1684–1694](https://github.com/GITenberg/Julius-Caesar_1120/blob/61f9979ce377707e385fdd4e0b48b0383b857524/1120.txt#L1684-L1694)：劇場指示明寫 Brutus 與其他人刺殺；凱撒接著說 `Et tu, Brute?—Then fall, Caesar!`，再有 `Dies` 舞台指示。**只有前半是拉丁語；最後一句口頭台詞是英文 `Then fall, Caesar!`。** [L1670–1689](https://github.com/GITenberg/Julius-Caesar_1120/blob/61f9979ce377707e385fdd4e0b48b0383b857524/1120.txt#L1670-L1689)安排他在襲擊前宣稱自己如北極星堅定。[L1694–1711](https://github.com/GITenberg/Julius-Caesar_1120/blob/61f9979ce377707e385fdd4e0b48b0383b857524/1120.txt#L1694-L1711)密謀者高喊自由，Brutus 安撫旁人並稱 Caesar 的野心受了罰。 | 莎劇是戲劇台詞的一手文本，並非古羅馬的現場紀錄；不能說莎士比亞**首創**該拉丁短語，只能說這個劇本確實把它寫成確定台詞。 |

### R3 補核的原文界線（抄自第一版 research.md）

- 普魯塔克《凱撒傳》[L46927–46933](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L46927-L46933)以英譯 `Some say` 引出見 Brutus 拔刀、蒙面與倒在龐培像座旁的場面。R3 `cs059` 口頭說「轉述一說」，插圖也以單一玩具劇場人物示意；不把那一說演成已證實的現場影像。
- Thomson/Forester 英譯的[正文 L1698–1704](https://github.com/GITenberg/The-Lives-of-the-Twelve-Caesars-Complete_6400/blob/bb5afc956095e248b2287cce2a4d3ebe394e5d31/6400.txt#L1698-L1704)把稱呼寫成 `my son`，在引句後標註號 97。集中列在[全文後段 L18375–18392](https://github.com/GITenberg/The-Lives-of-the-Twelve-Caesars-Complete_6400/blob/bb5afc956095e248b2287cce2a4d3ebe394e5d31/6400.txt#L18375-L18392)的腳註嫌呼語太長、質疑緊急時改說希臘語，又列出希臘文字樣的手稿異文；它沒有提出載有拉丁舞台名句的古代抄本。R3 只稱「腳註」，不把這份數位轉錄排版說成「頁底」。這些推理都歸屬後來的編者。

### 故事界線（抄自第一版 research.md）

1. 開場讓莎劇舞台**停在扮演凱撒的人開口之前**，到事件與傳記交代完才揭開劇本台詞。實際史實問題靠原文層級回答：Suetonius 的主記述在二十三刀間未留成句的話，只記第一刀時呻吟；**同一段**用「有些作者說」提出希臘語變體；Plutarch《Caesar》《Brutus》講 Brutus 持刀時的動作，沒有給該台詞。據此只能判斷**沒有足夠證據確認那句拉丁語就是歷史上的最後一句**，不能斷言他絕對沒有說過類似的話。
2. 「凱撒完全沒有說話」錯。Suetonius 82.1 在**襲擊開始、第一刀之前**寫他喊「這是暴力」；Plutarch《Caesar》寫他**受第一刀後**對 Casca 發問。把「臨死時沒有可確定的話」限於最後時刻。
3. Marcus Brutus 是 Suetonius 那段「有些作者」話語所指的 Brutus；Decimus Brutus 則是勸他赴會的人。莎劇兩人也分配不同角色，卡通造型及分鏡不可把二人混成同一張臉或把 Decimus 當作最後台詞的對象。
4. 保留原文希臘語 `καὶ σὺ τέκνον` 和戲劇拉丁語 `Et tu, Brute?` 作為後製卡／說明欄可讀字；MiniMax 提示詞只能畫空白紙。圖像不畫血、傷口、屍體，也不假裝場景、古籍手稿或服飾是精確重建。
5. 引用早期英譯腳註作「後來讀者如何推測」的實例時，必須口頭明說它是**編者腳註**。腳註的拉丁文猜測不可當成古文正文，手稿異文未做全譜系校勘，不聲稱解決了真正臨終語。

## 第一版逐句主張（抄自第一版 claims.md，R4a 定稿）

`EDIT` 為觀眾提問或由相鄰引文導出的比較，不冒充古代直接引語。判定欄依 R3 來源稽核（89/89）與 R4 聚焦覆核（六句改寫通過）。

| ID | 旁白 | 依據 | 判定 |
| --- | --- | --- | --- |
| cs001 | 木造舞台上，扮演凱撒的人剛坐下，身旁的演員突然靠近。 | SHA | CONFIRMED |
| cs002 | 扮演布魯圖斯的人舉起道具刀，畫面就在凱撒開口前停住。 | SHA,EDIT | CONFIRMED |
| cs003 | 這份劇本會給他一句話；古代傳記記下的聲音，卻會一樣嗎？ | SHA,SU-L:82.2 | CONFIRMED |
| cs004 | 到了那場會議之前，有人把警告遞到他手裡；他有讀嗎？ | SU-L:81.4,PL-C | CONFIRMED |
| cs005 | 同一天有兩位布魯圖斯，一位勸他出門；另一位會站在哪裡？ | SU-L:80.4,SU-L:81.4,SU-L:82.2 | CONFIRMED |
| cs006 | 先讓舞台停在這裡：歷史上的凱撒，最後說了什麼？ | SHA,SU-L:82.2,EDIT | CONFIRMED |
| cs007 | 蘇埃托尼烏斯的密謀者名單裡，馬爾庫斯和德奇姆斯都姓布魯圖斯。 | SU-L:80.4 | CONFIRMED |
| cs008 | 這份傳記說，參與密謀的人超過六十位。 | SU-L:80.4 | CONFIRMED |
| cs009 | 他們曾考慮選舉場、街道和劇場入口，最後挑了元老院會議。 | SU-L:80.4 | CONFIRMED |
| cs010 | 三月十五日，元老們要在龐培的會議廳聚集。 | SU-L:80.4,PL-C | CONFIRMED |
| cs011 | 這個位置靠著龐培的劇場，普魯塔克也記下了；凱撒會走到座位嗎？ | PL-C,PL-B | CONFIRMED |
| cs012 | 另一邊，凱撒雕像下面出現諷刺他像國王的字句。 | SU-L:80.3 | CONFIRMED |
| cs013 | 馬爾庫斯自己的審判席，也被放上催他行動的匿名字條。 | PL-B | CONFIRMED |
| cs014 | 普魯塔克說，其他密謀者想借馬爾庫斯的聲望，讓行動更有分量。 | PL-B | CONFIRMED |
| cs015 | 德奇姆斯也加入了密謀，凱撒對他卻仍有信任。 | PL-C | CONFIRMED |
| cs016 | 在這兩個人中，哪個會親自把凱撒帶出家門？ | SU-L:81.4,PL-C | CONFIRMED |
| cs017 | 在那位布魯圖斯勸他之前，三月十五日早晨的凱撒一度考慮留在家裡。 | SU-L:81.4,PL-C | CONFIRMED |
| cs018 | 蘇埃托尼烏斯提到他身體不適，也提到不利的祭兆。 | SU-L:81.4 | CONFIRMED |
| cs019 | 普魯塔克寫，卡爾普尼亞還勸丈夫把會議改天。 | PL-C | CONFIRMED |
| cs020 | 夢與預兆只是傳記裡的故事；它們最後攔得住凱撒嗎？ | SU-L:81,PL-C,EDIT | CONFIRMED |
| cs021 | 這時，另一位布魯圖斯來勸他：元老們已在等，不該讓整場會議落空。 | SU-L:81.4,PL-C | CONFIRMED |
| cs022 | 凱撒聽了他的話，走出家門。 | SU-L:81.4,PL-C | CONFIRMED |
| cs023 | 開場那位勸他出門的布魯圖斯，就是德奇姆斯。 | SU-L:81.4 | CONFIRMED |
| cs024 | 路上有人把一份陰謀警告交給凱撒。 | SU-L:81.4,PL-C | CONFIRMED |
| cs025 | 他把紙放進手裡其他文件之間，打算稍後再讀。 | SU-L:81.4 | CONFIRMED |
| cs026 | 普魯塔克也寫那張警告，但說擁擠的人群讓他無法讀完。 | PL-C | CONFIRMED |
| cs027 | 警告到了手上，卻沒把他攔下；會議廳外還有誰在等？ | SU-L:81.4,PL-C | CONFIRMED |
| cs028 | 密謀者已等在龐培廊廳；凱撒遲遲沒來，使他們緊張。 | PL-B | CONFIRMED |
| cs029 | 一位元老悄悄對馬爾庫斯與卡西烏斯說，希望他們快些辦完。 | PL-B | CONFIRMED |
| cs030 | 他們一度以為事情洩了底；那人轉去與凱撒說話，緊張又加深。 | PL-B | CONFIRMED |
| cs031 | 馬爾庫斯看那人的神色，才判斷他只是在向凱撒陳情。 | PL-B | CONFIRMED |
| cs032 | 安東尼又被另一名同謀留在門外談話。 | PL-C,PL-B | CONFIRMED |
| cs033 | 凱撒進門坐下；有人立刻帶著請願走近。他會先說什麼？ | SU-L:82.1,PL-C | CONFIRMED |
| cs034 | 請願的是提利烏斯辛伯，要替被放逐的兄弟求情。 | SU-L:82.1,PL-C | CONFIRMED |
| cs035 | 凱撒沒有答應，辛伯便抓住他的袍子。 | SU-L:82.1,PL-C | CONFIRMED |
| cs036 | 蘇埃托尼烏斯記下凱撒先喊：這是暴力。 | SU-L:82.1 | CONFIRMED |
| cs037 | 這聲發在第一刀之前，並不是那句有名的臨終問話。 | SU-L:82.1,SHA | CONFIRMED |
| cs038 | 接著一名卡斯卡出手；凱撒還來得及還擊嗎？ | SU-L:82.1 | CONFIRMED |
| cs039 | 凱撒抓住對方的手，蘇埃托尼烏斯說他還用寫字筆反擊。 | SU-L:82.2 | CONFIRMED |
| cs040 | 普魯塔克的《凱撒傳》讓他在受第一刀後，又用拉丁語質問卡斯卡。 | PL-C | CONFIRMED |
| cs041 | 兩份傳記各給凱撒一句不同的話，時間也一前一後。 | SU-L:82.1,PL-C | CONFIRMED |
| cs042 | 卡斯卡隨即向兄弟求助，普魯塔克記他改用希臘語。 | PL-C | CONFIRMED |
| cs043 | 那段希臘話的主人是卡斯卡；凱撒自己後來有說希臘語嗎？ | PL-C,SU-L:82.2 | CONFIRMED |
| cs044 | 附近的元老一時嚇得動不了，既不逃，也沒上前幫忙。 | PL-C | CONFIRMED |
| cs045 | 凱撒試著向外移動，周圍卻都是拔出的短刀。 | SU-L:82.2,PL-C | CONFIRMED |
| cs046 | 普魯塔克《布魯圖斯傳》寫，馬爾庫斯拿刀站到他眼前。 | PL-B | CONFIRMED |
| cs047 | 凱撒於是鬆開卡斯卡的手，用袍子遮住頭。 | PL-B | CONFIRMED |
| cs048 | 眼前這人已是馬爾庫斯；古代作者有替他寫下最後一句嗎？ | SU-L:82.2,PL-B | CONFIRMED |
| cs049 | 蘇埃托尼烏斯先寫，二十三次刺擊之間，凱撒沒有說出完整的話。 | SU-L:82.2 | CONFIRMED |
| cs050 | 他只記凱撒在第一刀時，發出一聲呻吟。 | SU-L:82.2 | CONFIRMED |
| cs051 | 可是，這段拉丁文沒有在呻吟那裡結束。 | SU-L:82.2 | CONFIRMED |
| cs052 | 作者接著寫：雖然有些人傳下另一種話。 | SU-L:82.2 | CONFIRMED |
| cs053 | 他沒列出那些作者是誰，也沒說自己在場聽見。 | SU-L:82.2 | CONFIRMED |
| cs054 | 在那條傳說裡，馬爾庫斯布魯圖斯衝上來，凱撒對他開口。 | SU-L:82.2 | CONFIRMED |
| cs055 | 三個希臘詞，大致是：連你也嗎，孩子？ | SU-L:82.2,SU-E | CONFIRMED |
| cs056 | 原句沒有布魯圖斯的名字；名字在作者引介這條傳聞的句子裡。 | SU-L:82.2 | CONFIRMED |
| cs057 | 「孩子」也不能當成兩人血緣的證明。 | SU-L:82.2,EDIT | CONFIRMED |
| cs058 | 另一位傳記作者普魯塔克，會替那三個希臘詞補上證據嗎？ | SU-L:82.2,PL-C | CONFIRMED |
| cs059 | 普魯塔克《凱撒傳》轉述一說：凱撒倒在龐培像腳邊。 | PL-C | CONFIRMED |
| cs060 | 那一段也沒有給他一句對馬爾庫斯的遺言。 | PL-C | CONFIRMED |
| cs061 | 換到《布魯圖斯傳》，凱撒倒下後，馬爾庫斯想解釋卻沒人聽。 | PL-B | CONFIRMED |
| cs062 | 兩篇是同一位作者的作品，不能算兩名獨立現場證人。 | PL-C,PL-B | CONFIRMED |
| cs063 | 沒寫也不等於絕不曾發生；那句拉丁名言又是誰明確寫進劇本？ | PL-C,PL-B,SHA,EDIT | CONFIRMED |
| cs064 | 開場停住的舞台，現在讓扮凱撒的演員繼續說話。 | SHA,EDIT | CONFIRMED |
| cs065 | 莎士比亞先讓請願圍上來，凱撒宣稱自己像北極星一樣堅定。 | SHA | CONFIRMED |
| cs066 | 卡斯卡喊：讓雙手說話；舞台指示讓他和其他人動刀。 | SHA | CONFIRMED |
| cs067 | 劇本特別寫出馬爾庫斯布魯圖斯也參與刺殺。 | SHA | CONFIRMED |
| cs068 | 接下來的名句，只有「連你也，布魯圖斯？」這半句是拉丁語。 | SHA | CONFIRMED |
| cs069 | 他隨後說的「那就倒下吧，凱撒！」在這個版本是英文。 | SHA | CONFIRMED |
| cs070 | 那才是劇本給凱撒的最後一句口頭台詞；接著才有「死」的舞台指示。 | SHA | CONFIRMED |
| cs071 | 演員有了清楚的句子與動作；古代原文也給出這句確定的拉丁問話嗎？ | SHA,SU-L:82.2,EDIT | CONFIRMED |
| cs072 | 可古代作者並沒有以同樣肯定的語氣留下那句拉丁問句。 | SU-L:82.2,PL-C,SHA | CONFIRMED |
| cs073 | 這份戲證明莎士比亞寫了它，沒有證明凱撒真的說了它。 | SHA,SU-L:82.2,EDIT | CONFIRMED |
| cs074 | 也不能因為戲裡有這句，就說莎士比亞一定是第一個寫它的人。 | SHA,EDIT | CONFIRMED |
| cs075 | 後來一份《十二凱撒傳》英譯，還把拉丁猜測放進腳註；讀者會看錯哪一層？ | SU-T:F97 | CONFIRMED |
| cs076 | 這份英譯把稱呼寫成「我的兒子」，而非莎劇的「布魯圖斯」。 | SU-T,SHA | CONFIRMED |
| cs077 | 這句英譯後面掛著第九十七號註記；一翻到註腳，就會看見另一種語言。 | SU-T,SU-T:F97 | CONFIRMED |
| cs078 | 到了腳註，後來的編者才猜：凱撒大概會用拉丁語說那句。 | SU-T:F97 | CONFIRMED |
| cs079 | 註腳裡沒有現場逐字紀錄；「很可能」幾個字，說明這是編者的推測。 | SU-T:F97 | CONFIRMED |
| cs080 | 編者還嫌英譯那串呼語太長，不像緊急時刻會說的話。 | SU-T:F97 | CONFIRMED |
| cs081 | 編者自己的理由是：在這種緊急時刻，凱撒何必改用希臘語？ | SU-T:F97 | CONFIRMED |
| cs082 | 腳註也提到希臘文字樣的手稿異文，卻沒提出寫著拉丁名句的古抄本。 | SU-T:F97 | CONFIRMED |
| cs083 | 這是編者的推理，卻不能放回蘇埃托尼烏斯的嘴裡；拉丁原文究竟寫什麼？ | SU-T:F97,SU-L:82.2,EDIT | CONFIRMED |
| cs084 | 回頭看這份傳記的拉丁原文，找不到編者猜的那句拉丁問話。 | SU-L:82.2,SU-T:F97 | CONFIRMED |
| cs085 | 回到開場的問題：我們能確定劇本怎麼寫，仍不能確定凱撒真說了那句拉丁語。 | SU-L:82.2,PL-C,SHA | CONFIRMED |
| cs086 | 再遇到歷史名言，你可以先看它在古文正文、譯本腳註，還是舞台上。 | SU-L:82.2,SU-T:F97,SHA,EDIT | CONFIRMED |
| cs999a | 歷史有時留不下清楚的遺言，戲劇卻能留下一句人人記得的話。 | SHA,SU-L:82.2,PL-C | CONFIRMED |
| cs999b | 你第一次聽到這句話，是在課本、電影，還是戲劇裡？ | EDIT | CONFIRMED |
| cs999c | 想繼續從原文找歷史名場面的來源，歡迎訂閱奇聞檔案局。 | EDIT | CONFIRMED |
