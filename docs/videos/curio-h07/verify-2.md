# H07 第二輪定稿史實覆核

查核日：2026-10-14（台北）。本輪只覆核改稿後的 narration-first.md、narration-second.md、video.json、visual-prompts.json、script.md，並對照 brief.md、research.md、claims.md、history-curiosity/topic-checks/H07.md 和 verify-1.md。這是文字與預定畫面查核；沒有把旁白音檔、生成圖、成片、上傳或播放判為通過。

## 判定

**PASS（本輪七句的史實強度、來源年代與編排對應）**。1703 年死亡補記寫黑絲絨；1698 年入獄登記未寫材質；兩筆仍分開標示。伏爾泰 1738 年信使用「鐵面人」，但信未交代材質如何查驗；後來書中明寫的是下巴部位的鋼製彈簧，不能由此推定整副面具是鐵的。身分及其他年份的面具材質仍未確定。

| 位置與目前精確句子 | 來源與限制 | 當前綁定 |
| --- | --- | --- |
| first:6「他記下死亡時刻，也記下面具，卻沒留下能確認死者身世的名字。」 | [F99] 轉錄 Du Junca 的 1703 年死亡補記，記死亡時刻、黑絲絨及「未知」；後來下葬簿有不同拼名，不能把本句讀成「從未留下任何名字」。 | scene[1] h07-780680cf；副官與**已合上的**死亡簿是插畫，不充當原稿照片。 |
| first:18「死亡補記還寫著：面具是黑絲絨。」 | [F99] 的 1899 年英譯轉錄支持的是 **1703 年補記**，並非 1698 年入獄照；本輪未逐字核對 1703 手稿原件。 | scene[10] h07-bced8458：kicker 明寫「1703 年 11 月 19 日死亡補記」，sub 明寫「Du Junca 登記｜Funck-Brentano 1899 年轉錄」。 |
| first:56「入獄登記沒寫姓名與材質；黑絲絨出自死亡補記。」 | [J98] 是 1698 年入獄登記的照片；[F99] 的入獄轉錄未寫姓名、材質，死亡補記另寫黑絲絨。照片未在本輪逐字校讀，文字依後來轉錄。 | scene[42] h07-300c617e：左右欄分列「1698 入獄」與「1703 死亡」，各有本名、材質欄；下方分標照片 BnF／Commons 和 1899 年轉錄。scene h07-7355e817 的 1698 照片仍只作入獄證據。 |
| second:5「一七三八年，伏爾泰叫他『鐵面人』，卻沒交代材質的查驗依據。」 | [V38] 的 Garnier 1880 年轉錄顯示 1738-10-30 信使用 homme au masque de fer，並稱曾與服侍過囚犯的人交談；信沒有該問答逐字稿或材質查驗方法。本句限於**信沒有交代**，沒有斷言伏爾泰個人從未查驗。 | scene[48] h07-4d151adf：書信插畫；不畫可讀的原信或把「鐵」當實物證據。 |
| second:13「伏爾泰寫的是面具下巴有鋼製彈簧，讓囚犯戴著也能吃飯。」 | [V51] 的 Garnier 1878 年第 25 章轉錄有 mentonnière 與 ressorts d'acier；本輪未核對 1751 年首版該頁，因此不稱「已見首版原文」。 | scene[56] h07-a0b99b19：排練桌上的布面罩示意，下緣小鋼彈簧；不是存世面具。 |
| second:14「鋼製的是他描述的彈簧，不能憑這句話認定整副面具是鐵的。」 | 同 [V51]。這是從句子內容作的有限推論；不主張已證明整副面具從未有金屬。 | scene[57] h07-a1d34f98：製道具者只檢視小彈簧，戲劇頭盔關在戲服箱，和史料段分開。 |
| second:60「面具沒留下；副官記下黑絲絨，死者是誰仍未定。」 | [C26] 坎城館方稱死後個人物品及傳說中的面具被焚毀、真實身分仍不明；黑絲絨見 [F99] 的 1703 年補記。此句只回答可用證據，不否定其他年份曾有別種面具的可能。 | scene[97] h07-answer-card：標「1703 年死亡登記／黑絲絨／身分未定／其他年份的面具材質無從確定」。 |

[J98]: https://commons.wikimedia.org/wiki/File:L%27homme_au_masque_de_fer,_acte_d%27%C3%A9crou,_1698.jpg
[F99]: https://www.gutenberg.org/cache/epub/43231/pg43231-images.html
[V38]: https://fr.wikisource.org/wiki/Correspondance_de_Voltaire/1738/Lettre_952
[V51]: https://fr.wikisource.org/wiki/Le_Si%C3%A8cle_de_Louis_XIV/%C3%89dition_Garnier/Chapitre_25
[C26]: https://www.cannes.com/fr/culture/musees-et-expositions/musee-du-masque-de-fer-et-du-fort-royal/a-voir-au-musee.html

## 與第一輪查核的關係

verify-1.md 第 23、47、49、51 行所載 first:18、first:56、second:14、second:60 的**精確舊引句**已不是現稿；例如 first:18 舊文為「一七零三年十一月十九日的死亡補記，寫出面具的材質：黑絲絨。」、first:56 舊文為「入獄登記只說蒙面、不寫姓名；對照死亡補記，才看見『黑絲絨』。」。舊的 h07-e312f95e、h07-c1fd8138、h07-f607238e 等文字衍生 scene ID 也不能用來指認本稿。verify-1.md 第 63、79 行的 SHA-256 是當時快照，**不是本輪檔案的驗證值**。

第一輪 C01–C18 中未改的史料判定及其「原件未見／版次限制／單一學者假說」界線仍可作來源背景；本輪只把上表七句及其卡片重新判為 PASS，不把第一輪的整份精確逐字核對移植到新雜湊。

本輪 SHA-256：
- narration-first.md：92C3DED8739F968C33E19CA37E623A6D9D4C337DAF2C6FBBF8B33AEA92C10A85
- narration-second.md：4F42B7151DA9A7E9D0B9B0BC3399C4559A23BB136F67B996A8E3646DC5C8DA54
- video.json：8421383E55C8B444C8F692BA6389E8C4E448C826DF2E5C3F7DC4AF0A15473756
- visual-prompts.json：0E99979E4073E3F98D62B6D647FE56741B65946D98F30B8CFAF69DEAAEEB22EA
- script.md：BAEFF7349F82C805DCA2731DFBED3A23A82DB888B1627A2EAA528800AC5874D2

## 編排與剩餘門檻

本輪機械核對：兩份旁白共有 100 句，逐句等於 video.json 的 100 個 scene line；95 個 visual-prompts 項目皆對應同索引的 shot line；上表七句也都出現在 script.md。執行 node tools/video/cli.mjs lint --slug curio-h07：**0 errors、1 warning**，估時 9.4 分鐘。唯一警告是 scene[99] h07-outro 只有一句；回答、留言問題與訂閱邀請實際分在 scene[97]–[99]，此警告屬結尾版型檢查，未消除。估時不等於旁白正文或成片的實際時長。

仍須依最新句子核對或重錄相應音檔，聽音與對時；生成畫面須逐張看，特別是插畫不可冒充史料、1703 來源卡不可套用 1698 照片。音訊、圖像、成片、字幕、上傳、播放與發布各有後續關卡；本報告不替代任何一關。

## 2026-10-14 定稿畫面增補

原判定及上方雜湊保留為歷史快照。本增補另核現版 100 句旁白與 `video.json` 的 100 場逐字相符；獨立覆核者重查 C01–C18、兩輪查核與新增資料卡，**現版文稿及資料卡的史實界線 PASS**，未見新的無來源實質史實斷言。此判定只涵蓋文字和來源歸屬；音檔核准、生成圖、成片和站主播放各依自己的收據。

生成圖容易畫成假原稿、錯誤歷史現場或已確定的線索後，scene 61、74、75、77、82、84、87、88、89、91、96 及留言問題 scene 98 改為程式資料卡。卡片明標：1669 多熱公文不能直接替 1703 死者填姓名；四站及約 34 年只在多熱身分推定下成立；桑尼諾財務與外交說是學者推論；原簿已毀而十九世紀刊本仍可比對；面具無留存實物可檢驗各年份材質。scene 74 統一使用「馬提歐里」，scene 96 同列坎城博物館與 Funck-Brentano 的相應來源。其餘現用 59 張插畫逐張核對分鏡聯絡表，明顯誤導的生成圖已退件或換成資料卡。

現版 Git 內容的 SHA-256（LF 換行）：
- narration-first.md：ED0741A45DB5C0F70B50120917A25F657116EF2FC2EE38714ED51734B77A1278
- narration-second.md：4F42B7151DA9A7E9D0B9B0BC3399C4559A23BB136F67B996A8E3646DC5C8DA54
- video.json：50BBFFE0E9D1D4EC4DE7CB8A875D0D01D61E12015E71BD3ACC46EB72CC792874
- visual-prompts.json：AFCB1329AB1745B09F2BA12300162E904D686440F5B4314495C6A45BEC4C39B9
- script.md：566FA8CAF23BBE5942F421E2CA16789895A9695A39F3BD0AD514935B2DDF2EC4

第一段旁白在 Windows 製作與覆核時使用 CRLF 換行，其 SHA-256 為 `965608B0B831D76D999FD73932F4CBFFADC4FE8589AEB8B374C1EC1BA15945B9`。Git 提交把換行正規化為 LF；上述 `ED0741…` 是提交後內容的精確雜湊。兩者只差換行位元組，旁白文字相同，不能拿製作時的 CRLF 雜湊來驗證 Git blob。

重建後 `lint` 為 0 errors、6 warnings；警告是鏡頭描述用字重複及 `h07-outro` 單句模板檢查，未新增史實錯誤。已核准的 9 分 26 秒旁白時間軸對應現版分鏡：59 張插畫占 57.5% 畫面時間，最長單畫面 7.93 秒。成片 `qa` 實測節奏及其餘 10 項均通過；交付與核准紀錄見 [`delivery.md`](delivery.md)。
