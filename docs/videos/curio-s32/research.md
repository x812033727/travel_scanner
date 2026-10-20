# S32｜馬可波羅的紙幣記載能證明他到過元朝嗎？來源可行性

查核日：2026-10-20（UTC）。這是**來源先行的前製候選**，不是已核准劇本或影片。題庫原題「馬可波羅，真的到過中國嗎？」可改成可由原文回答的較窄問題：**遊記寫的元代紙幣制度，有哪些能和《元史》互證？這種相符能證明到訪嗎？**

## 固定、可重開的底本

| 簡稱 | 固定版本、定位與本次讀取 | 使用界線 |
| --- | --- | --- |
| P1 | Marco Polo／Rustichello, *The Travels of Marco Polo*, Yule–Cordier 英譯校注本，卷一，[GITenberg 固定 commit `813d6dffb6c2968664c573ed0f24242b919dfcbf`](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt)，[raw](https://raw.githubusercontent.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt)。HTTP 200，2,023,404 bytes，下載檔 SHA-256 `db5fe3122057a37615ccda2813d1edee2525046177b9ce885072a2c669a893e0`。 | **1903 年 Cordier 修訂第三版**，承接已故尤爾的十九世紀譯註，不是 1298 年單一法文手稿。尤爾[二版序署 1874](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L663-L674)，Cordier [第三版序](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L232-L260) 明說尤爾生前未及完成第三版。[尤爾自述](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L11770-L11794) 主文以 Pauthier 本為底，擇入 G 本材料，再把他認為可信的 **Ramusio 版特有內容放在方括號**；Cordier 的新增註解也可能用括號，須逐處分辨。不能把括號段當所有早本共有。 |
| P2 | 同書卷二，[固定 commit `95709397a514799b8bb9262bd918f19be61b009c`](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-2_12410/blob/95709397a514799b8bb9262bd918f19be61b009c/12410.txt)，[raw](https://raw.githubusercontent.com/GITenberg/The-Travels-of-Marco-Polo---Volume-2_12410/95709397a514799b8bb9262bd918f19be61b009c/12410.txt)。HTTP 200，2,214,378 bytes，SHA-256 `4dcfd52725f9d6ab671c18edacb43fbbb8f206075fe2be24b6617ec271067104`。 | 杭州鹽稅一章的「馬可替可汗查稅」只見一個版本；編者緊接指出另一較早的法文 G 本僅說「多次聽到帳目」。不能把單一版本當獨立履歷證據。 |
| Y93 | 宋濂等修《元史》卷九十三〈食貨一·鈔法〉，Kanripo 四庫全書底本，[固定 commit `e2cf641b7f57ad9847edca32c2b851c0e875ee4c`](https://github.com/kanripo/KR2a0036/blob/e2cf641b7f57ad9847edca32c2b851c0e875ee4c/KR2a0036_093.txt)，[raw](https://raw.githubusercontent.com/kanripo/KR2a0036/e2cf641b7f57ad9847edca32c2b851c0e875ee4c/KR2a0036_093.txt)。HTTP 200 via clone，SHA-256 `ad3da9fd1a80ca80add2f5536135fc0729cc6a1d85cda1ce3847dba57c68ba6f`。 | 早明編修、四庫傳本的官史文字，並非十三世紀即時記錄，也不是馬可波羅旅行的個人證明。其 `<pb:…>` 標籤可作頁面錨。 |
| Y94 | 同書卷九十四〈食貨二·鹽法〉，[固定同 commit](https://github.com/kanripo/KR2a0036/blob/e2cf641b7f57ad9847edca32c2b851c0e875ee4c/KR2a0036_094.txt)。本次 Git clone 完整讀取。 | 可核元代有鹽課與兩浙運司；**不能**直接把遊記的金幣 `toman/saggio` 換成官史的引／鈔／錠，宣稱收入數字一致。 |

本雲端直接訪問 Gutenberg、Brill、Crossref、OpenAlex、Cambridge、JSTOR、Wikisource 均遭代理 CONNECT 403；上面固定的 GitHub 原文可讀。Hans Ulrich Vogel 的 *Marco Polo Was in China: New Evidence from Currencies, Salts and Revenues* 是後續查找線索，**未取得全文或可信摘要，不採其結論**。

## 已能逐段核的事實

| 影片可用說法 | 精確原文位置 | 界線 |
| --- | --- | --- |
| 遊記的序言把 1298 年熱那亞囚居和魯斯蒂謙記錄旅行見聞連在一起，且明說書中有「親見」與「聽來」兩種材料。 | [P1 序言 L11950–11977](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L11950-L11977)。 | 這是書自己的說法，不等於我們獨立證明每一段由誰目擊；[英譯本所收傳記重述 L7031–7045](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L7031-L7045) 也只是另一層文本。 |
| 卷一第二冊第 24 章稱大汗把紙做成不同面額的貨幣，強制通行，舊鈔可到官署換新。 | [P1 第 24 章 L32843–32922](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L32843-L32922)。 | 金額寫作威尼斯貨幣比擬，不能直接說成元朝鈔面額；**蓋朱印與偽造者處死**在 L32873–32882 的 Ramusio 特有括號段，後續稿須明示版本，不可當所有早本共有。「全境無人敢拒」是遊記的廣泛說法，官史片段不足以驗證覆蓋率。樹皮材料沒有由下列官史段證實。 |
| 《元史》記中統元年造中統元寶鈔、至元二十四年改造至元鈔，列面額、偽造者處死、昏爛鈔換新及工墨費。 | [Y93〈鈔法〉L446–479](https://github.com/kanripo/KR2a0036/blob/e2cf641b7f57ad9847edca32c2b851c0e875ee4c/KR2a0036_093.txt#L446-L479)，頁標 25b–27a。 | 是對**制度存在與幾個運作環節**的跨文本對照；遊記說換鈔按 3%，《元史》記工墨三十文、後減二十文、再增回原額，兩者不能直接等同，也不能擅自把《元史》費額說成「每張」固定費。制度相符無法排除透過別人得知。 |
| 尤爾的十九世紀導論指出：其所校的遊記正文未說長城、飲茶、纏足；他認為這些沉默難解，也推測作者在元朝主要接觸外國人。 | [P1 尤爾導論 §71 L10124–10152](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L10124-L10152)。 | **尤爾觀察與假說**，收錄於 1903 年 Cordier 修訂版；不是 Cordier 在 1903 年提出的新觀察，也不等於「沒去過」。整份電子書其他地方多次出現 `Great Wall`／`tea`，那些主要屬編者文字，不能用對整檔搜尋單詞的方法證明遊記正文有提。 |
| 編者註說紙鈔並非此書唯一的歐洲記錄，亦列其他遊記作者。 | [P1 第 24 章編者註 L32928–32946](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-1_10636/blob/813d6dffb6c2968664c573ed0f24242b919dfcbf/10636.txt#L32928-L32946)。 | 相符的紙幣知識是值得查的正證，但不是只有親臨才能知道的「指紋」。 |
| 卷二杭州段有海鹽帶來收入的描述；《元史》也列元代鹽法與兩浙鹽運司。 | [P2 第 78 章 L11166–11221](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-2_12410/blob/95709397a514799b8bb9262bd918f19be61b009c/12410.txt#L11166-L11221)；[Y94 L177–192](https://github.com/kanripo/KR2a0036/blob/e2cf641b7f57ad9847edca32c2b851c0e875ee4c/KR2a0036_094.txt#L177-L192)、[L310–329](https://github.com/kanripo/KR2a0036/blob/e2cf641b7f57ad9847edca32c2b851c0e875ee4c/KR2a0036_094.txt#L310-L329)。 | 僅能對照有鹽政，不能說數額吻合。P2 [編者註 L11223–11226](https://github.com/GITenberg/The-Travels-of-Marco-Polo---Volume-2_12410/blob/95709397a514799b8bb9262bd918f19be61b009c/12410.txt#L11223-L11226) 指出「馬可受命查稅」似只見 Pauthier 版本；G 本是「聽過帳目」。 |

## 題庫說法的處置

- **保留作疑問：**為何不寫長城、茶、纏足？先講「十九世紀英譯者尤爾在其導論裡的觀察」，並把文本選材和不同抄本當成解釋候選；不能從缺席推出本人沒到過。
- **保留作可核的對讀：**元代紙鈔制度、杭州／兩浙鹽政，須分清官史與遊記是哪一層來源；若之後提具體收入、面額、百分比，先完成貨幣和版本研究。
- **暫不採：**「中文史料找不到馬可波羅的名字」、其與忽必烈的職位、「學界多數認為他到過」，因未完成中文史料全量檢索與現代學術來源查核。也不說「元史證明他親眼看到紙鈔」。
- **畫面界線：**可愛卡通人物與紙鈔只作示意；不把 1903 版所載的明代鈔票插圖、現代復原鈔或某一本抄本畫成「馬可親手持有的元代原物」。

## 候選敘事與下一步

**A（推薦）｜「一張紙幣，能證明馬可波羅到過中國嗎？」** 開在 1298 年熱那亞：一本自稱混合親見和聽聞的遊記成書。由卷一一張紙幣切入，讓觀眾先看到材質／面額／換鈔的具體說法，再打開《元史》的鈔法，對上制度、看清不一致的換鈔費；之後處理「漏掉長城」的沉默，最後用「紙鈔也見其他旅人記載」及杭州查稅句的版本差異，回答：**制度細節可信度提高，但不能單獨判定作者親身走到哪裡。** 可形成一條「從書中一個細節到它究竟能證明什麼」的故事線。下一位撰稿者仍要逐句核源、安排 8 分鐘以上正文與 45 秒內懸念節奏、獨立盲讀，再考慮語音／插圖費用。

**B（候補）｜「他真的替忽必烈查過杭州的稅嗎？」** 由卷二兩個版本的「受派／聽到」差異帶進鹽政。若取這案，須先取得更早法文 G 本與 Pauthier 版的可讀固定正文、釐清其年代與編校關係，還須有可靠貨幣換算，否則不能把此句拍成馬可的確定差事。

**可行性判定：**A 的核心問題已有兩套可固定文本及跨文本對照，值得進下一輪企劃與來源獨審；它不能回答題庫原本的二選一真偽判決。B 在抄本和數字查核之前暫不開稿。這輪沒有劇本、音訊、插圖、上站 gate 或花費。
