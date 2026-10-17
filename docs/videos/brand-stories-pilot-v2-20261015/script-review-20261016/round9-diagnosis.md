# A01 narrative round 9：真實退件與最小處置診斷

Reviewer: codex-story-cc-review（獨立唯讀覆核）  
Scope: actual-20261016-035053；只讀本機快照與正式 producer 程式，未呼叫主機、模型、媒體工具，未更改任何既有結果或候選。  
Decision: 保留真實 FAIL；本文件不是候選安裝資格、script-review 收據或 pilot PASS。

## 1. 可重演的實際結果

- 下載 archive 實算 SHA256：`b988ed8af18e650985f85d6085d243c71032b0885172405645a40c86dc1a341a`。
- 全部 80 個 audit 的 before/after composite 與相鄰連結均符合；最新 7 筆從已知安裝後 source `abe9742685874795acef7a572ef02ed5e0d8fc52001c805448fdeacac67445a0` 開始，到 `cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b`。
- 最新 7 筆依序為 origin verifier round 7、turn verifier round 5、now verifier round 7、origin/turn/now listener、narrative round 9。
- 用正式 `parseAnswer`、`applyPatch`、`checkedRows`、`rewriteProblems`、`composeStory`、`panelPayload`、`panelVerdict`、`narrativeRecord` 重演。每一步的六章 bytes 雜湊均與 audit after 相同；最後六章與 video.json 完全相同，最終 script/claims/series/auto/narrative/verify/lexicon 雜湊符合 source composite。
- 所有 journal 都是真實 succeeded、已 adopted；request 經正式 normalizeRun/sourceHash 後符合 receipt。三筆 listener 的舊 instructions、callback appendix 與當時六章解析出的 story_callbacks/context SHA 均符合。panel 的 questions/narration 等於當前全文，instructions 是原文加既有格式提醒，13 個引用 ID/逐字引文均對得上，raw yes/no 與儲存結果完全相同。
- origin verifier 的 raw 最後多了一個 `}`，一般 JSON.parse 會拒絕；正式 producer 的 parseAnswer（prompts.mjs:832、856–876）取第一個完整物件。使用同一正式解析器後能精確重演。這沒有造成 panel 的三個 no，也沒有修改 raw。
- 真實結果：`chapters_link`、`payoffs`、`one_thread` 為 no；其餘 10 項 yes，無 advisory。不是格式誤判或過期 hash。
- auto 仍 blocked / prompt_fixes:narrative；六章 checked/listened true，verified/listener_done true，verify_rounds 1、narrative_fixes 2、narrative round 9。pending journal 為空。沒有媒體授權。
- 正式 lint/cute 均 0 errors。63 鏡、92 句；估正文 520.833 秒（8:41）、hook 60 秒。只是文字時間估算，未做實際配音或播放驗收。

重演證據：`A01-NARRATIVE-ROUND9-INDEPENDENT-REPLAY.json`；程式：`review-round9-replay.mjs`。最後追加的 80-link／已知安裝 anchor assert 另在同一輪本機執行通過；未重新請任何模型判讀。

## 2. 三句修補實際如何被改寫

| 行 ID | 安裝的 round8-continuity 候選 | 真正送到本輪 panel 的文字 | 判讀 |
| --- | --- | --- | --- |
| zc7k | 開場那個家庭已經不必一路提著那只箱子：1928 年，母親拉著兒子做的箱子出發。 | 開場那一家人，其實早就不必一路提箱子：1928 年出發時，母親拉著兒子做的箱子。 | origin listener 改；保留家庭回呼，但加回「其實早就」的回頭語氣，弱化原本以搬運動作承接主問題的意圖。 |
| jm3w | 開場那位機師 Plath，1987 年在車庫做出 Rollaboard。 | 1987 年，Plath 就在開場那間車庫裡，做出了 Rollaboard。 | turn listener 改；有效車庫遠回呼保住，沒有復活先前未點名問題。這輪不應再為此行重寫。 |
| 7asx | 從往後拉，到站著推，1997 年 Samsonite 推出了平衡四輪直立箱。 | 有。1997 年，Samsonite 推出平衡四輪直立箱，箱子能站著推了。 | now listener 改；把明確的用途轉變前綴換成短答，重新以年份／另一品牌開句。它仍回答上一章四輪問題，但較容易被讀成下一個產品例子。 |

三筆 verifier 都保留這三個安裝版本。now verifier 還明文認定「從往後拉，到站著推」是動作承接、沒有虛構 Plath→Samsonite 傳承。因此不能說本輪 panel 已實讀並拒絕原三句候選；它讀的是 listener 改後全文。

其他真實改動：turn verifier 只在 `6i8x` 加「照這篇報導的說法」，保留 USA TODAY 軼事的來源界線；listener 改 origin 的 `3zkh`、`3s8v`、turn 的 `iu9y`、`bxv2`、now 的 `kfiw`，均為相同事實範圍的措辭。turn listener 刪 `cbw4`「一趟又一趟地走，箱子怎麼帶，成了每天的難題」，它重述上一句且不含數字／名稱，正式可刪規則接受。`edtc` 擬新增 Travelpro 被原 rewrite guard 拒絕，實稿仍是「這家公司也說…」。未發現需恢復刪句的敘事或事實理由。

## 3. 三項 no 必須分開看

### chapters_link：真有可聽見的接縫，也有冷開場規則的解讀張力

panel 引用 `zc7k`。hook 最後問的是「箱子早就能滾著走，還缺什麼，才能走進旅客的日常？」；origin 開句先重述開場預告過的 1928 家庭，而非直接回答還缺什麼。listener 加「其實早就」使回頭感更明顯。這是具體可改善的接縫，不能只稱模型誤讀。

但 frozen 原案本來允許機場冷開＋多個預告後進入 1928→1940 年代→1970→1987→1997/2000 的正文。冷開預告後回到故事起點，不等於倒敘本身有錯。本輪 one_line=yes 也沒有提供年代錯亂的指控。不能為求 chapters_link 而編出 1928 家庭直接導致 Sadow 的歷史因果，或默改 frozen 原案。

### payoffs：即問即答 eghq→ys5y，並非沒有答案

真實同鏡 idea-10：

1. `eghq`：那麼，顧客買不買帳？
2. `ys5y`：據他多年後回憶，大家一看懂怎麼用，很快就接受了。
3. `quhs`：不過他沒有說出確切賣了多少。

前兩句就是問與答，且 canonical loops 明列 eghq→ys5y。idea 本輪完全未改，與上一輪相同。這輪 payoffs 改引 eghq；上一輪引用的是 jm3w。**不能把上一輪沒引用 eghq 說成模型已逐項核准這個 loop**；單一負例不揭示其他缺陷。不過「沒有回答」在此與可見全文不符，最合理的問題是：payoffs 要求點名，卻沒把即問即答與隔數分鐘的掛鉤分清。

script-writing.md:104 明說剛講完的事直接接著說，隔數分鐘才需要點名；core/narrative.mjs:259 的 payoffs 則一律問「而且回答時點名了它」。不應在相鄰兩句硬加「還記得顧客買不買帳嗎」，那會製造冗餘。仍保留 raw no；這是規則適用的歧義，不能私自把它改 yes。

### one_thread：用途演進是否算一個主角，與即問即答是不同問題

panel 引用 `7asx`。全文可以沿同一個用途問題理解：讓重箱子跟人走→自製能用→能買到→航站帶得順手→直立推行與轉向；Samsonite 是最後一步使用方式的例子。這符合 frozen「輪子行李箱」的品類演進，不需要宣稱同一只實物箱子傳下去。

另一方面，文字跨了家庭、Kelly、Sadow、Plath、Samsonite；若 one_thread 按「同一個具體人／團隊／專案持續行動」嚴格讀，這份原企劃本來就不符合。換三句同義詞無法把數個歷史參與者變成一個具體主角。本輪 one_line/no_detour=yes 只能說沒有被其餘題挑出問題，不能邏輯上強迫 one_thread=yes。原 panel 不給解釋段，以上是獨立判讀，不冒充模型的內心理由。

因此這裡應釐清「產品用途演進」與規則的相容性，不能把生產線上的真 FAIL 覆蓋成通過，也不能編造技術承繼或因果來湊單一主角。

## 4. 最小文字建議；不自動建立第 10 輪

如後續仍維持 frozen 品類演進方案，可保留以下**最多三行**作 owner 讀稿的對照；本輪沒有修改候選或實稿：

- `zc7k`：恢復已審過的「開場那個家庭已經不必一路提著那只箱子：1928 年，母親拉著兒子做的箱子出發。」這去掉 listener 重新加的回頭語氣，仍僅指 1928 出發時已有自製箱，不新增製作年份。前輪正式估此鏡 8.933 秒。
- `7asx`：恢復已審過的「從往後拉，到站著推，1997 年 Samsonite 推出了平衡四輪直立箱。」把用途演進先說出來，不聲稱技術血緣或全球第一；和當前 kfiw 相接仍須在真正候選正式 compose 時核對，前輪搭配較長 kfiw 估 10.433 秒。
- `ys5y`：若 owner 覺得「大家」指涉不夠明白，最小只換成「據他多年後回憶，顧客一看懂怎麼用，很快就接受了。」這是可讀性選擇，不是補一個原本不存在的答案；不加「還記得」，不刪來源歸屬，不改成可證實的銷量。此提議尚未形成候選／重查。

`jm3w` 保留現稿。hook、其他鏡頭與全文長度不需為這三項重新填充。新稿若採用，必須誠實失效化受影響的文字與事實／敘事綁定，再依真正流程重查，不能沿用原 PASS；本診斷不授權執行。

## 5. 為何應保留現稿供 owner 讀／聽稿

建議先把**這份真實 92 句全文**和上述三行對照留給 owner 做一次內容聽讀，而非再對相同關卡盲抽。理由：

1. 這次資料鏈可精確重演，已排除「舊稿、錯誤套用、parser」；不需要再靠跑同稿判讀來找答案。
2. 正文已有約 8:41 的有據內容，事實取捨和遠回呼大多穩定；原來機師車庫的問題有實際改善。重做全片會破壞已完成的來源／圖文對位，沒有本輪證據支持。
3. 目前尚存的是一個可改善的章首接縫、局部 listener 將用途承接改弱，以及「品類史是否被視為同一主角／短問答是否必須點名」的審稿適用問題。人的一次完整聽讀能對是否真的困惑給出具體段落，不必以同義詞無限迭代。
4. 聽讀是內容回饋，不是要求 owner 代替真正 panel 簽核，不是媒體製作／上傳授權。仍保留 blocked、round9 FAIL、所有歷史 raw 和 counters。

## 6. 生產流程觀察與限制

v6 沒漏送遠回呼 context。origin 的 story_callbacks 含 y9b6→83ew、6h2q→3zkh、dkkz→76ur，沒有把 zc7k 當作某個 payoff；now context 有 4e5m→7asx。appendix 只要求保留有效回呼、允許自然改句，沒有要求保留用途對比句。因此 listener 的行為可由現有 request 解釋；不能稱 harness 沒有照送或偷偷移除了保護。檢查器事實關卡也不負責驗證這類敘事語意。

若日後改 listener 約束，應另審新 request 與真 hash，讓它保留章際因果／用途承接且仍可修正常句；不能事後重寫已回傳的結果或假裝舊 listener 通過新稿。這輪不實作。

本次沒有重新查外部史料。三次 verifier 的 PLAN 表示依既有 must_verify 計畫；尤其來源 11 仍是 read=plan，不應宣稱本輪重新打開官方招股書。未發現本輪新增需要再寫史實的問題；這不是整部影片的最終事實／畫面／音訊驗收。
