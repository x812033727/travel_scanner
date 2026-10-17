# B18 精準修正版：全稿與來源獨立審讀（離線）

2026-10-17，Codex `/root/b18_full_story_sources`。**結論：PASS_OFFLINE_EDITORIAL_AND_SOURCE_RECONCILIATION；HOLD_FORMAL_PRODUCTION_GATES。** 我獨立讀完這一版六章 85 景、88 行旁白，逐筆檢視 65 個仍為 `UNCHECKED` 的來源主張及其景號；核對它相對前版的實際差異、十三題說故事關卡和可讀官方原文。這是編輯／史料審讀結果，**不是**正式 worker 的 `narrative`、`fact`、`script-review.json` 收據，也沒有製作音訊、圖、CC 或影片。

## 凍結版本與機械核對

| 檔案 | SHA-256 |
| --- | --- |
| `sha256.json` | `CB28AE7BB6AED7A30C639318504E8E11386AEE8DE1404E9B71B1C372C1E40953` |
| `series.json` | `218d1bb500701380f505f5c3da37638de7cbffce95db23f8c06aa45b6546c807` |
| `chapters/hook.json` | `eb502bc4436ecf5b82edd49f6fd0f31502565d54b61145fb2e5a8465665691a2` |
| `chapters/origin.json` | `8d464a318133bf04ca804e3e4576fa6705ba483803277dc1c1664aae7bc32328` |
| `chapters/idea.json` | `9afd40486ba804e38e8aa12b11a298275eb96cc4a651671baf46925516c15301` |
| `chapters/engine.json` | `37610084a186c8d0774e63ea5f182a46952ce6104320baaa7afee1227ab8ed1d` |
| `chapters/turn.json` | `6c2ac8deec71807b5065af8784f8395336cefc29836801ec7cab984c17ff9d49` |
| `chapters/now.json` | `b9bda31ee48f9cee19a5ffe8815170dd1a33b23c3d24d818c282c16f003577fe` |

本包 `sha256.json` 的所有列舉檔案現值均與清單吻合，0 hash mismatch；它的前版清單雜湊指向 `039131fdaba3107668062722af6e126b06aa6acc9d46a5b8481a9402e287997a`。`node build.mjs --check` 退出碼 0：85 景、88 行、66 插圖、19 卡、65 筆 `UNCHECKED`、0 lint error、0 cute error、24 warnings、0 外部呼叫。另逐筆查 65 筆的景號、來源索引和非空 fact 索引：**0 錯位**；旁白 **0 純標點行**。靜態正文估時 **560.97 秒**（約 9:21）；若片頭片尾共假設 26 秒，合計約 9:47。`measured_body_seconds=null`，因此真正 TTS 及成片長度仍未知。66／85 景為插畫，字卡 19 景；此為離線結構數量，不是生成圖品質驗收。

## 與前版的實際差異

獨立比較 `chapters/*.json` 的 scene 與 claim 物件後，`hook`、`origin`、`idea`、`engine` 完全未動。`turn` 只改 `turn-s081`、`turn-s086` 兩景及 `t10`、`t12`、`t18` 三筆 claim；`now` 只改 `now-s093`、`now-s095`、`now-s096`，刪掉 `now-s097`，並改 `n2`–`n5`、刪 `n6`／`n8`。`series.json` 同步收窄 F10 的 1980 旁通表述並更新 S2 的重讀日期；`loops` 把 `turn-s092/f996e543` 的年份問題回收點改為 `now-s093/233e1a3a`。沒有發現 `delta.json` 之外的章節場景或 claim 內容改動。

上一版的六個必修點均已解開：`turn-s081/d8ecd870`、`t10` 共同說其他新店重新設計路線；`turn-s086/ed0c5c6c`、`t12` 準確說**販售供大型店使用**的旁通裝置；`t18` 僅綁 `turn-s092` 的元祿舊機懸念；`now-s093/233e1a3a` 立即回答「1985 年製、不是 1958 年首店原機」；`now-s095/bb7022f4`、`8b88e002` 清楚說 2021 堺東店仍使用的**這台**輸送機列入第 112 號；`now-s096/1585ea8b` 說另存早期板片同列此號。重述的 `now-s097` 已刪，`n6`／`n8` 兩筆舊綁定也已刪；沒有多台機器的暗示或年份提前洩漏。

## 65 筆來源主張的逐項歸屬

S0＝[J-Net21／中小企業基盤整備機構](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、S1＝[日本機械學會第 112 號](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)、S2＝[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?age=high-growth&eid=00026&page=keii)、S3＝[日本法院判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)、S4＝[石野集團官方年表](https://www.ishino-group.com/history/)、S5＝[同集團介紹](https://www.ishino-group.com/group/)；F 是 `series.json.plan.must_verify` 的零起算索引，`—` 為沒有 fact 索引。下表 PASS 是**來源與旁白語義在本輪離線核讀中可成立**，並不把 `UNCHECKED` 改成正式查核通過。

| 章／筆數 | 每筆 ID → S／F | 本輪判讀 |
| --- | --- | --- |
| hook／7 | `h1` S0/F1、`h2` S0/F1、`h3` S0/F2、`h4` S0/F0、`h5` S2/F3、`h6` S2/F7、`h7` S3/F4 | **PASS**。1948 工廠／遞盤瓶頸、1958 首店、1970 萬博、特定餐台權利均作未揭結果的預告。 |
| origin／11 | `o1` S0/—、`o2` S0/—、`o3` S0/F2、`o4` S0/—、`o5` S0/—、`o6` S0/—、`o7` S0/—、`o8` S2/—、`o9` S0/F2、`o10` S0/F1、`o11` S0/— | **PASS**。1947 遷居、20 圓四貫立食、人手瓶頸與 1948 工廠點子，來源歸屬一致。 |
| idea／11 | `i1` S2/F3、`i2` S0/—、`i3` S0/F3、`i4` S2/F3、`i5` S2/F3、`i6` S0/F3、`i7` S0/F3、`i8` S0/—、`i9` S0/—、`i10` S0/—、`i11` S0/— | **PASS**。撲克牌／名片兩版本各有歸屬；扇形板、約十年及 1957 試作沒有混寫成一名目擊者的說法。 |
| engine／13 | `e1` S1/F0、`e2` S2/F6、`e3` S2/F6、`e4` S0/—、`e5` S0/—、`e6` S2/F4、`e7` S3/F4、`e8` S0/F5、`e9` S2/—、`e10` S0/—、`e11` S0/—、`e12` S0/—、`e13` S0/— | **PASS**。1958 首店、1962 特定實用新案、萬博出店都有來源；道頓堀不指定相衝的 1960／1962 年。 |
| turn／18 | `t1` S2/F7、`t2` S2/F7、`t3` S0/—、`t4` S2/F7、`t5` S2/F12、`t6` S2/F12、`t7` S3/F4、`t8` S3/F5、`t9` S0/F5、`t10` S2/F12、`t11` S2/F12、`t12` S4/F10、`t13` S4/F10、`t14` S2/—、`t15` S2/—、`t16` S2/F12、`t17` S2/F12、`t18` S1/F8 | **PASS**。萬博／加盟、特定 1972 期滿與元祿外業者、一些新業者的後場直線路線、1980 旁通和 1986 ㄇ字店各自有出處；未說成同店一次改造。`t18` 現只綁懸念。 |
| now／5 | `n2` S1/F8、`n3` S1/F8、`n4` S1/F8、`n5` S1/F8、`n7` S0/F3 | **PASS**。`n2` 接住 1985 與非 1958 原機；`n3`–`n5` 區分一台 1985 整機與另外保存的早期板片；`n7` 回到轉角解法。 |

### 核對過的史料邊界

- **特定權利是 1972，不把 1978 混作同一案。** 法院理由 P8 L466–473 記第 **579776** 號實用新案 1962-12-06 登錄及道頓堀店 1962-04；P10 L574–578 認定**這項**權利 1972 年期滿，之後已有與原告無關業者。J-Net21 與發明協會回顧另說 1978，但權利鏈未釐清；現稿 `engine-s049`、`turn-s077–080` 只說這項實用新案，不給一切權利單一到期年，也不把其他店的出現歸於單一事件。[法院 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)、[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)。
- **道頓堀有 1960／1962 版本。** J-Net21 記 1960 第二店，法院 P8 L470–473 記原告道頓堀店 1962-04，是否同一法人／店序未解；`engine-s048` 只說「後來也開進」，沒有強行選版本。[法院 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)、[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)。
- **1971／1974 給茶仍不作口播。** 石野同一集團的年表說 1970 開發給茶裝置、1971 已販售附給茶裝置的壽司輸送機；集團介紹說 1974 整合／開發。這兩頁不是獨立佐證，沒有證實哪年是「首次」。`series.json` 留 caveat，本版旁白未引入首次整合年份。[官方年表](https://www.ishino-group.com/history/)、[集團介紹](https://www.ishino-group.com/group/)。
- **後場直線、1980 旁通、1986 ㄇ字是不同證據層。** 發明協會記載一些新業者在後場做壽司、用直線輸送帶供應；石野年表記 1980 販售**供大型店使用**的旁通裝置、1986 出現 ㄇ字型輸送帶店。現稿有來源歸屬，不說石野發明所有路線或同一家店從直線、旁通一路改到 ㄇ字；`t10`／`t12` 已隨口播收窄。[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?age=high-growth&eid=00026&page=keii)、[石野年表](https://www.ishino-group.com/history/)。
- **機械遺產 #112 的實物為一台後來的整機加另存早期板片。** JSME 明載 2021 認定，一台 1985 年製造、當時在堺東店使用的壽司輸送機，加上元祿產業保存的早期「ウロコ／三日月」板片；這不是 1958 首店原機連續運轉。`now-s093–096` 現逐句清楚表達。[JSME 第 112 號](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)。

`t6` 的 claim 已含「直線」，旁白在同章下一景 `turn-s073` 才說出直線；`t11` 也綁該下一景，故連續口播與來源本身相合。若正式工人逐**景**嚴格要求 claim 完全不先帶下景資訊，可以把 `t6` 收窄為「後場做好的盤子放上輸送帶」；這是低風險的粒度建議，**不構成新的史實 HOLD**。同樣，`turn-s063` 有明確「發明協會說」的全國知名度歸屬；法院 P9 L543–553 認為單憑萬博不足以證成「元祿」商業標識全國著名，對象不同，不應把這句宣傳為法院也確認商標全國知名。

## 十三題說故事關卡：本次人工離線判讀

依 `.agents/skills/youtube-video/references/script-writing.md` 第十三題逐行讀稿。第 9 題是參考題；下列 YES 只是本讀者對這個**凍結版本**的判讀，不能替代正式獨立 `narrative` worker。

| 題 | 判讀 | 依據 |
| --- | --- | --- |
| 1 前四句在具體時刻 | YES | 1948 吹田工廠的瓶子、白石參觀、店裡遞盤問題立刻進場。 |
| 2 開場不洩漏後段結果 | YES | 轉角、萬博、權利與小店方案各留結果。 |
| 3 一條故事線 | YES | 缺人手 → 借輸送帶 → 轉彎 → 首店 → 別店重畫盤路 → 兩種年代實物。 |
| 4 不唸目錄或清單 | YES | 開場未報章節；後半段仍跟一盤壽司如何走向客人。 |
| 5 每章第一句承接 | YES | 尤其 `turn-s092` 問舊機年份，`now-s093` 第一行立刻回答 1985 並排除首店原機；其餘章界也接住上章事件。 |
| 6 90 秒內有懸念 | 暫定 YES | 靜態 `loops` 與章段有轉角、開店、萬博、權利、後場路線及舊機年份；正式秒數待 TTS。 |
| 7 掛著問題回收且點名 | YES | `turn-s092/f996e543` → `now-s093/233e1a3a` 已在 `loops` 修正，問題於章首直接答；舊機不再新增無回答的「是否第一台」。 |
| 8 不重講同一事實 | YES | 刪除舊 `now-s097`；1985 年只在 now 首句口播一次，其後談 2021 認定與另存板片。1962 權利在 turn 是必要的點名回呼。 |
| 9 章名（參考） | YES | 六章指向可辨的事件節拍。 |
| 10 片尾不預告下一支 | YES | 留給觀眾的拿盤習慣問題及訂閱句沒有下一集預告。 |
| 11 開場至少三個後段時刻 | YES | 轉角、萬博及權利到期均停在答案前。 |
| 12 一個主角從頭帶到尾 | YES | 主線可一路跟白石小店出發的**送盤路**；後段新業者各自重畫同一條功能性路線，片尾回到客人伸手拿盤。 |
| 13 無岔段／清單 | YES | 未口播給茶、採購、盤價、辭書、市場數字；1980／1986 是同一送餐路線問題的後續例子。 |

**後續界線：**這版可作正式獨立查核／聽稿的候選，尚不能說已取得正式全稿、史實或音訊 PASS。作者資料中 65 項 `verdict` 仍全是 `UNCHECKED`，`worker_pass=false`、`full_story_pass=false`、`full_source_pass=false`、`tts_generated=false`；尚缺正式逐章來源查核、worker narrative、TTS 聽檢、實際片長、圖像與成片驗收。不得以本離線報告替代付費匯入或上傳的關卡。
