# A01 round14／15 逐條來源表獨立複核 — SOURCE ONLY／HOLD

日期：2026-10-17（台北）。範圍是 round14 `source-map.json` 的 **25 條 `lines`**，以及仍在 `inherited_claim_reconciliation`、但有實際旁白的 `now-06/tszs`。round15 的來源表逐位元組相同，SHA-256 均為 `373e79cb1372bfd1bc722ad3251288ea357efe78547bc5996f83d88f75726b74`。round14 manifest 的 SHA-256 為 `9c2b6a69360c0f701fb28043e2e1179b6cda83c6e90a91253e14224b66245162`；round15 manifest 記錄 `narration_or_claim_changes: 0`。本表沒有修改任何候選章稿、來源表、判定或正式機資料。

**判定的意思**：「可支撐」只表示列出的來源足以支撐目前這句的限定說法；「限縮」表示來源有相關材料，但句子或來源綁定仍需修；「推論」表示是說書者基於原件的合理情境，而非有文件記載的事件。這些都不是完整影片的事實、聽感或敘事 PASS。原來源表 25 條仍全部是 `PENDING_INDEPENDENT_REVIEW`；六章共有 24 筆 `PENDING` claim，其中 23 筆在 `lines`，另 1 筆是下表的 `n14`。另兩條 hook 問句沒有 claim ID。舊輪次的 `PLAN`／`CONFIRMED` 也沒有在此重新審核。

來源索引（均為原始專利、當事人訪談或當事機構的紀錄）：

- **WHS**：[溫尼特卡歷史學會館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)；**WHS 2010**：[館方藏品整理紀錄](https://www.winnetkahistory.org/gazette/from-the-curator-fall-2010/)。館藏文章本次直接開啟逾時，官方搜尋索引可讀完整正文；round12 候選另記錄獨立擷取的官方 HTTP 200、123873 bytes、SHA-256 `0219df34bcd52f93ff9346883ad865af9e9a0c65e2efba87079d62dcaefb1fb4`。未直接核對 Anita 的 1933 年原書。
- **ABC 2010**：[Sadow 本人及空服員 Poole 的訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)；**ABC 2012**：[Plath 與早期 Rollaboard 的採訪](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)。兩頁可直接讀取；訪談中的個人回憶按歸屬處理。
- **Sadow patent**：[US3653474A 原申請書](https://patents.google.com/patent/US3653474A/en)；**Plath patent**：[US4995487A 原申請書](https://patents.google.com/patent/US4995487A/en)。兩件專利可直接讀取；設計示例不可轉成已上市實物的證據。
- **Travelpro**：[品牌自述歷史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)。該頁可直接讀取；只用來核對其自家 1991 年敘述，不採用它把 Sadow 說成第一人的廣泛說法。

## 25 條來源表紀錄

| 章／旁白／claim | 來源與逐句判讀 | 應採動作 |
| --- | --- | --- |
| `origin/r12o01`／`claim-r12o01` | **WHS，可支撐歸屬**：館方引述 Anita 於 1928 年旅前對搬運行李的發問；1933 原書尚未逐頁核。 | 保留「歷史學會引述」歸屬；勿寫成已親讀原書。 |
| `origin/r12o02`／`claim-r12o02` | **WHS，可支撐歸屬**：館方轉述丈夫寧提重箱並取笑妻兒輪子箱。 | 保留「館方轉述」，不泛稱當時所有男性。 |
| `origin/r12o03`／`claim-r12o03` | **WHS，需限縮**：館方說第二次旅程後她帶著輪子行李巡迴講述；沒有逐件核實口播「那只」與旅程、館藏實物是同一物。 | 新候選改「她巡迴講旅行故事時，仍帶著輪子行李箱」；claim 與 source map 同步，重新審。 |
| `engine/r12e01`／`claim-r12e01` | **Sadow patent，可支撐歸屬**：背景段有航空、鐵路、巴士航站，自行搬行李且步行甚遠的發明人陳述。 | 保留「申請書」歸屬；不可當獨立市場統計。 |
| `engine/r12e02`／`claim-r12e02` | **Sadow patent，可支撐**：設計目標是保留普通箱形、大小、式樣並能拖行。 | 保留申請書設計語態，勿稱每款上市箱皆如此。 |
| `engine/r12e03`／`claim-r12e03` | **Sadow patent，可支撐問句**：箱底由蓋與身的底段構成，示例有四組輪件。 | 問句可留；下一句須標明是專利示例。 |
| `engine/r12e04`／`claim-r12e04` | **Sadow patent，可支撐示例**：輪件 23／24 位於窄蓋底段 111，25／26 位於較寬箱身底段 121。 | 保留「專利的示例」；產圖需核對 2＋2 位置。 |
| `engine/r12e06`／`claim-r12e06` | **Sadow patent，可支撐設計用途**：端環與可拆拖帶見示例，權利要求可提可滾；「平地不用提」是設計用途。 | 保留設計歸屬，不描寫未證實的顧客使用實測。 |
| `engine/r12e07`／`claim-r12e07` | **Sadow patent，情境推論**：原提把、可拆帶有據；「遇到台階」是例子，不是專利記錄的事故或實測。 | 宜改「需要提起時，還有原本的提把；拖帶也能拆」或於審稿明確視作假設情境。 |
| `turn/r12t01`／`claim-r12t01` | **Plath patent＋ABC 2012，可支撐邊界**：專利 1989-08-08 申請；2012 採訪向前 25 年指 1987 原型。 | 保留「不能倒推 1987 原型細節」；同年事件不要補先後。 |
| `turn/r12t04`／`claim-r12t04` | **Plath patent，可支撐敘事問句**：說明書有支腳站立與傾斜後兩輪承重的設計。 | 保留問句，作為專利設計問題而非實測現場。 |
| `turn/r12t05`／`claim-r12t05` | **Plath patent，可支撐**：凹入式兩輪只有小部分外露，專利稱不致顯著增加內外尺寸。 | 保留「專利讓」語態；勿投射到 1987 初版。 |
| `turn/r12t06`／`claim-r12t06` | **Plath patent，可支撐**：抽起拉桿並傾箱，支腳離地而由輪子走。 | 保留專利示範語態。 |
| `turn/r12t07`／`claim-r12t07` | **Plath patent，可支撐**：說明書區分直立支腳與傾斜滾行姿態。 | 保留專利示範語態。 |
| `turn/r12t08`／`claim-r12t08` | **Plath patent，可支撐**：桿 18、套筒 28、偏心導件 47 與襯套 27 的摩擦夾持見詳細說明與圖 4。 | 保留；畫面不可畫成無來源的按鈕／卡榫。 |
| `turn/r12t11`／`claim-r12t11` | **Plath patent，可支撐**：核准日 1991-02-26。 | 保留，不指定它與同年離職的先後。 |
| `origin/csdd`／`o2` | **WHS，可支撐**：兒子 Bud 以舊嬰兒車兩輪與伸縮木把手造箱。該 claim 跨 `csdd` 與同鏡 `9ij6`，來源表目前僅列第一句。 | 全稿來源矩陣應將 `9ij6` 也綁到 `o2`／WHS，或標示 claim 覆蓋同鏡兩句；勿臆造固定工法。 |
| `origin/zc7k`／`o22` | **WHS，可支撐歸屬**：館方記錄 1928–1930 第二次旅行時家族使用自製輪子箱，Anita 的箱子由兒子製作。 | 日期只修飾出發，不宣稱 1928 製作；館藏圖說的 1927 不口播為製作年。 |
| `origin/6b28`／`o1` | **WHS，可支撐歸屬**：Anita 是畫家，帶六口之家兩次旅行，第二次為 1928–1930。 | 保留。 |
| `origin/4prs`／`o17` | **WHS，需限縮**：文章說在多個港口、車站與住處之間搬行李，沒有「每到一站」的全稱頻率。 | 新候選改「在港口、車站和住處之間，行李得跟著搬」；claim/map 同步重審。 |
| `origin/83ew`／`o20` | **WHS＋WHS 2010，可支撐有限說法**：館方圖說標 `2005.26.576` 為 Anita 的 1927 箱，2010 藏品紀錄也列她的輪子箱；**未證明它是 1928 旅途插畫指的同一件**。 | round14「館藏保存安妮塔的一只自製輪子箱」可保留；`must_verify` 與來源 8 `supports` 應另列這件物件及非同一性界線；不改判正式 PASS。 |
| `turn/6jx3`／`t13` | **Travelpro，可支撐自家紀年**：品牌年表記 1991 年 Plath 離職全職經營。 | 保留「照 Travelpro 的說法」；不採品牌頁的廣泛第一人宣稱。 |
| `hook/6h2q`／無 claim ID | **ABC 2010，可支撐問句**：Sadow 回憶機場輪板，以及四腳輪加繩子的初樣。 | 回收應落在輪與繩都說完的 `origin/idiy`；現 round14 loop 已如此。 |
| `idea/76ur`／`i17` | **ABC 2010，可支撐回憶＋有限推論**：Sadow 回憶副總裁 Jerry Levy 親自試走、命採購進貨；同報導記 1970 年 10 月陳列。 | 保留已寫的歸屬；「有機會走到顧客面前」是後續合理銜接，不說副總裁親見購買成效。 |
| `hook/y9b6`／無 claim ID | **WHS＋WHS 2010，可支撐有限問句**：館方有一件 Anita 輪子箱；沒有指認是片頭旅程示意的同一件。 | round14「還有一只留到今天嗎」可留；所有畫面與 payoff 都保持「一只」範圍。 |

## 來源表外但仍待審的 active claim

| 旁白／claim | 來源與判讀 | 應採動作 |
| --- | --- | --- |
| `now-06/tszs`／`n14` | **一般物理推論；ABC 2010 只能作旅客裝太滿的受訪者例子**。輪子降低移動所需的搬運動作，但不會改變箱子與內容物的重量；這句沒有再歸屬 Poole。 | 在新候選來源矩陣補 active `tszs` 行，`support_type` 記為一般物理敘述，別以 ABC 的個人觀察當物理證明。保留 round11 已刪的 Poole 歸屬與引語為歷史，不自動恢復。 |

## 進入整片審核前的精確修補

1. **另建新版候選，不覆寫 round14／15**：把 `r12o03` 的「那只」與 `4prs` 的「每到一站」縮到來源能證明的範圍；若保留 `r12e07` 台階例子，審稿標為推論。逐條同步章稿 `claims`、source map、series 企劃與 manifest 雜湊。
2. series 的來源 8 `supports` 現只列出旅行與演講，沒有明寫館藏物件；`must_verify` 也沒有獨立的 `o20` 物件項，source map 的 `o20.fact_index` 因而是 `null`。增列「WHS 收藏安妮塔一只輪子箱，物件 2005.26.576；不推定與 1928 旅程示意同一件」作獨立待核 claim，再把 `o20` 綁到它。圖說的 1927 只作館方標籤，不當製作年。
3. series `origin.point` 寫「片頭動畫後明確從 1928 年出發開始」，實際 `origin-r12-01 → origin-03 → origin-01` 是旅前發問、造箱、再出發。改企劃或改敘事順序，使 plan 與最終旁白一致；不要把這個差異留給 verifier 猜。
4. 新候選的完整來源矩陣應包含 `origin-03/9ij6` 與 `now-06/tszs`，清楚區分專利**設計**、當事人**回憶**、館方**轉述**與作者**推論**。保留舊 `NOT FOUND` 的原判作歷史，別把後來找到來源錯寫成舊輪次已通過。
5. 以上只是受限來源複核。仍需對最後一個精確版本的 **108 句全稿**跑獨立事實與聽感覆核、正式 verifier／listener／整片 narrative panel，再量真實 TTS 與畫面；現在不得建立 `script-review.json` 或啟動付費媒體。
