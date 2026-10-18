# H07-v2 獨立史實與分鏡覆核

查核日：2026-10-15（台北）。範圍是 `video.json` 的繁中台詞、資料卡、插畫提示詞與 `script.md`；本輪自行重讀下列公開轉錄與館方說明。原版 H07 的 `verify-1.md`／`verify-2.md` 只供尋找待核主張，不把原版核准搬到新版。**這不是音檔、生成圖、字幕、成片、後台或上傳的驗收。**

## 判定與綁定快照

**PASS：四句新旁白的史實強度及本版資料卡／插畫計畫未見阻擋性史實矛盾。** 本輪所讀 `video.json` SHA-256 為 `80772F6204204F42F8A0B4905766EAE1A72635C6BDA73BFEA36F618D3A02771A`。獨立史實覆核當時的 `lint` 為 0 errors、3 個多語舊譯 warnings；其後 en／ja／ko 譯文已更新，2026-10-15 重跑 `lint` 為 **0 errors、0 warnings**，不改變此處史實判定的來源快照。

| 新行 ID／現行台詞 | 獨立來源核對與判定 |
| --- | --- |
| `45164df0`「他記下囚犯當晚約十點去世。」 | **PASS。** Du Junca 的 1703-11-19 死亡補記在 [Funck-Brentano 1899 英譯轉錄](https://www.gutenberg.org/cache/epub/43231/pg43231-images.html)中明載約十點；不把 1899 年轉錄說成這次親閱原稿。scene[11] 的副官闔簿屬卡通示意。 |
| `baeadea2`「兩份文書一對照，關鍵的落差就從名字裡冒出來。」 | **PASS。** 前一張 scene[72] 資料卡將 [1669 年多熱公文轉錄](https://earlymodernfrance.org/journal/2016-volume-xvii/valet-marquis-louvois%E2%80%99s-invited-guest-mystery-man-iron-mask)與 1703 年下葬名的 [Marchialy 摹本](https://www.gutenberg.org/cache/epub/70207/pg70207-images.html)／[Marchioly 轉錄](https://www.gutenberg.org/cache/epub/43231/pg43231-images.html)分開；本句引向下一章的拼法對比，scene[73] 以現代研究者分開兩張抽象人形片示意。這是線索落差，沒有斷言兩人已證不同。`143be677` 已恢復原版句子，不列為本輪改寫。 |
| `029cafbf`「下葬摹本上的拼法，和密令裡的多熱並不相同。」 | **PASS。** `Dauger／d'Auger` 與下葬刊本 `Marchialy／Marchioly` 的字面不同；這句只比記載，後續明說若多熱就是蒙面囚犯，四站路線才成立。不能把下葬名當成確定本名，也不能把讀法衝突當作兩人已證。來源同上。 |
| `926246b2`「面具實物沒有留下，誰也不能替伏爾泰的『鐵』做材質鑑定；剩下的，是互相競爭的身分推論。」 | **PASS，限於實物查驗。** [坎城鐵面人博物館](https://www.cannes.com/fr/culture/musees-et-expositions/musee-du-masque-de-fer-et-du-fort-royal/a-voir-au-musee.html)稱面具與私人物品死後被燒毀、身份仍未知；[伏爾泰 1738 年信](https://fr.wikisource.org/wiki/Correspondance_de_Voltaire/1738/Lettre_952)已有「鐵面人」稱呼，[後來刊本的《路易十四時代》](https://fr.wikisource.org/wiki/Le_Si%C3%A8cle_de_Louis_XIV/%C3%89dition_Garnier/Chapitre_25)描述的是下巴鋼彈簧。不能藉無實物否定 Du Junca 1703 年補記的「黑絲絨」文字紀錄。 |

## 分鏡與資料卡

- **已修再核** scene[4] `h07-dfc7a42b` 現明畫囚犯的素面遮臉罩，沒有把「蒙面」誤畫成只靠帽影藏臉；材質不由此插畫下斷言。`look` 仍僅用 `cute-mystery`。
- **已修再核** scene[5] `h07-db81d592` 的 1698 入獄簿與 scene[13] `h07-30d6e64a`、scene[88] `h07-13f0cb04` 的下葬簿摹本均改為**闔上**；scene[55] `h07-1778513e` 的伏爾泰書也闔上。這避免把有文字但姓名未確證的簿冊畫成空白頁。具體文字只由來源卡排版。
- **已修再核** scene[97] `h07-answer-card` 現寫「無實物可驗『鐵』；身分仍未確定」，限於無實物做鑑定；scene[10]、[42] 的 1703 年「黑絲絨」文字證據仍在。
- **已核界線** scene[10]／[40]／[42] 將 1703 年黑絲絨補記與 1698 年入獄紀錄分開；[BnF 原件的 1927 年攝影館藏頁](https://commons.wikimedia.org/wiki/File:L%27homme_au_masque_de_fer,_acte_d%27%C3%A9crou,_1698.jpg)只對應後者，這次沒有逐字校讀手寫圖像。scene[76]–[78] 的四站與約 34 年均明寫**若蒙面囚犯就是多熱**，且是監禁而非戴面具的年數。scene[57]、[67]–[71] 把金屬面罩與雙胞胎放在劇場／小說／研究區，沒有畫成獄方已確認的實物與身份；[1771 年編者增補](https://fr.wikisource.org/wiki/Dictionnaire_philosophique/Garnier_%281878%29/Ana,_Anecdotes)的兄長說也只作傳說。[桑尼諾訪談](https://news.ucsb.edu/2016/016743/mystery-unmasked)的財務與外交動機仍在 scene[84] 明標為學者推論。

## 來源限制與重核點

Du Junca 的兩筆登記在此以 1899 年英譯轉錄查讀；Topin 的公文、下葬簿資料是十九世紀刊本，且 Topin 與 Funck-Brentano 對身份各有自己的解釋，不把其結論當原件。伏爾泰信與書使用後來編輯版，未核 1738 年手稿、1751 年首版或 1771 年原印本。坎城網頁是當代館方整理，不是獄方當年紀錄。動畫角色、書信、簿冊與道具都是插畫，不得在片中標成親閱原稿或存世面具。若此快照再改，須重算雜湊、重跑 lint 並重核相應句子與畫面；本報告不替代付費產圖後的逐張事實矛盾檢查。
