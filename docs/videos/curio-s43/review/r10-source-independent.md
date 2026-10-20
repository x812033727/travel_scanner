# S43 R10｜改稿的固定史料與文字畫面核對

**結論：PASS（限 R10 文字史料／文字畫面）。** 2026-10-20 UTC；精確 `script.md` SHA-256 `152623a7c93c1dbeeef4c1db25ae760f7ad66d0ac5b7e6cae84f73b0929b0cbf`、`video.json` `eb26b1c742280f597e78eba2f7445aa2492c341c810a32827b7128f3dfc0739e`、`claims.md` `ea167a1c92c50402860b49da3608aa211146509646be6a043b37158d1689e518`。未改動的 `research.md` 為 `35e0e14636349fc149edc716df72be659a361e01e7aae567d4a13fc6c49e3bd2`，`brief.md` 為 `f4a24cae62e5c1e92a83df61b29285ed2305888f3001d8520ba01d435d6739b4`。前後雜湊均再次核對一致。

## 方法與範圍

我直接從 `research.md` 指定的三個固定 Git commit 下載原始全文至 `/tmp`，逐檔算出與研究表一致的 SHA-256：1831 年選編書信 L `c795bf75dde25565205b8d3ec696e92cebc9019da7dd28d01936fa15bc334dec`、達爾文後來的自傳 A `eb2c4e03f7eff1ac5c6fdaa865099e8238df712d04e820c24d7768f6961cde96`、後出的航海記 V `24b8d915eb5f61c091ee66403096bb3a950e3c0cb310caf086b6be0cc86781f1`。下表的 R10 **16 個異動句**逐一回查這些固定全文所引原始行，並看該景英文畫面提示。其餘口播沿用 R9，這一輪**未重做其餘 83 句的逐條史料核對**。

本審核者繼承了前一工作者的任務背景，知道改稿是為音檢而來；因此這份是**重新打開原文的來源核對**，不是隔離背景的盲讀、獨立聽寫或已生成圖片的檢驗。任何「書信沒有記載」只限本集明示所引的選編 1831 年段落；不能推斷世上不存在別的文件。L 為兒子事後選編，不是手稿照片；A 是達爾文多年後回憶；V 是事後出版的航海記。

## 16 句異動的直接來源核對

| 景 | 原文支持及畫面界線 | 判讀 |
| --- | --- | --- |
| `dn015` | [L5620–5657](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5620-L5657)：亨斯洛轉述船長要能作伴且被推薦為紳士的人。教授折空白信、兩空椅只是示意。 | PASS |
| `dn019` | [L5661–5706](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5661-L5706)：皮科克來信說職位可交達爾文，後文回答薪水；前置問句沒有把答案改成已付薪。寫信畫面不顯可讀原文。 | PASS |
| `dn032` | [L5708–5742](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5708-L5742)：達爾文因父親反對而不能接受，並明說另致皮科克；沒替那封未收錄信編內容。示意封信無字。 | PASS |
| `dn033` | [L5746–5783](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5746-L5783)：8 月 31 日又寫信求父親明答是或否；畫面只示意動筆。 | PASS |
| `dn050` | [L5868–5882](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5868-L5882)當年信說父親改意且希望位置尚未給人；[A871–889](https://github.com/GITenberg/The-Autobiography-of-Charles-Darwin_2010/blob/906f72376c2153899e7482609fb915eda282e661/2010.txt#L871-L889)回憶舅舅勸說。空椅為船上名額意象。 | PASS |
| `dn051` | [L5884–5928](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5884-L5928)：達爾文致姊姊說 Jenyns 先被問；「家書／另外一個人」保留來源及順序，旅行箱不冒充候選名冊。 | PASS |
| `dn057`、`dn059`、`dn060` | [L5932–5958](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5932-L5958)：達爾文**自己在家書轉述**伍德收到船長信，說自己當時又放棄；亨斯洛亦以為機會沒了，批評皮科克過度誇大；船長原想帶的朋友因任職不能去。新句的「太樂觀」比原信批評輕，未添新主張。畫面只有示意信、教授、空艙位，沒有冒充船長原信或正式名冊。 | PASS |
| `dn071a` | [L5975–5981](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L5975-L5981)：達爾文當時轉述船長說可搭其他船返英；地圖留白，不畫承諾過的固定航線。 | PASS |
| `dn074b` | [L6121–6129](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L6121-L6129)：達爾文致姊姊信說只要還有勇氣便不在馬德拉回頭；問句保留是否已答應的懸念，畫面無假造馬德拉到港。 | PASS |
| `dn074f` | [L6137–6153](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L6137-L6153)：9 月 9 日信說**達爾文本人缺乏南太平洋群島行程的確定消息**，這阻住他最後決定。新版明說「達爾文還不確定船是否會去」，不宣稱海軍部已拒絕或正式核定航線；空白地球儀無定案航路。 | PASS |
| `dn077b` | [L6220–6231](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L6220-L6231)：同封信後段，與船長再見並採購後，自稱「可把我要去看作已定」，仍留意外可能；「決定登船」是**本人意向**，沒有說正式航路獲核定。畫面僅示意達爾文續寫。 | PASS |
| `dn087` | [V147–153](https://github.com/GITenberg/The-Voyage-of-the-Beagle_944/blob/a26cbdcdc1449627d1594dac877ad11396167791/944.txt#L147-L153)：兩次因風返港後 1831 年 12 月 27 日從 Devonport 啟航；新句的「英國港口」較寬但真實，成人在船上示意無矛盾。 | PASS |
| `dn087b` | [V15164–15175](https://github.com/GITenberg/The-Voyage-of-the-Beagle_944/blob/a26cbdcdc1449627d1594dac877ad11396167791/944.txt#L15164-L15175)：11 月 15 日晨塔希提在視野內，隨後停泊 Matavai Bay；[V16212–16225](https://github.com/GITenberg/The-Voyage-of-the-Beagle_944/blob/a26cbdcdc1449627d1594dac877ad11396167791/944.txt#L16212-L16225)緊接 1836 年 1 月、[L7928–7947](https://github.com/GITenberg/Life-and-Letters-of-Charles-Darwin---Volume-1_2087/blob/1314d6b4dd6353f610004423a6cb93749080ff00/2087.txt#L7928-L7947)回顧前一年訪塔希提，合起來定位 1835 年。島景說明非當日海岸復原。 | PASS |
| `dn999a` | [A891–899](https://github.com/GITenberg/The-Autobiography-of-Charles-Darwin_2010/blob/906f72376c2153899e7482609fb915eda282e661/2010.txt#L891-L899)：鼻子險些使他被拒，是後來熟識船長後聽到、晚年才記下的回憶；[V147–153](https://github.com/GITenberg/The-Voyage-of-the-Beagle_944/blob/a26cbdcdc1449627d1594dac877ad11396167791/944.txt#L147-L153)證明確實啟航。固定 L 的本集所引 1831 年信段 L5620–6255 未記載鼻形作為拒絕理由；新版明限「本集引用」的信，不假稱普世檔案皆無。片尾是品牌卡，無假造面相審查。 | PASS |

## 對照與尚待的關卡

以封存 R9 `video.json` 對比，R10 **僅 16 個 `lines[0].text` 異動**；景數、畫面資料、運鏡、迴圈與中繼資料無差。R10 `video.json` 有 **96 個正文句**，`claims.md` 有 **96 個相同 ID 的口播列，逐字 96/96 相同**；`script.md` 含 99/99 個場景／片尾口播，無缺漏。`claims.md` 的 115 個 GitHub 引文 URL 都落在上述三個固定 commit。這些是文字一致性檢查，**未驗任何實際生成圖片**。原有 `dn087b` 的 `green` 提示詞可能讓系列色盤偏綠，須以原尺寸原生試圖觀察；它沒有與來源描述相反，不能視為史實重建。

R10 的兩名全新敘事盲讀、精確稿審核、合成後重跑完整音檢與實際片長仍屬後續關卡；本報告不能替它們放行，尤其 R9 音檢還有 16 個旗標。同版 Jev 政策回條另見 [r10-jev-policy.json](r10-jev-policy.json)；那是政策判讀，不是本來源審核的一部分。
