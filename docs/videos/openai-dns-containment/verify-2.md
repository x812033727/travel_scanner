# 第二位獨立完整查核：openai-dns-containment（R2）

查核日期：2026-10-25，依Asia/Taipei日期。查核者未撰稿、未參與原事件選材；先重新讀四原始頁，之後才讀第一輪報告與作者證據。依協調者限制，只寫本檔，不修改video、claims、brief、SVG或媒體，也沒有git操作。

**結論：文字事實PASS；整包REVISE。** R2已修正第一輪指出的compaction限定及模型身分精確性。82場、86句與全部data、metadata、縮圖、兩SVG及兩Shorts未發現新的必修事實錯誤。但Q1公開頁畫面含過量逐字原文，Q2整包轉述的可重算英文等義下限對incident及containment均超200 words；修正前不能聲稱整包引用檢核通過。

## 讀取快照與驗證範圍

- `video.json` SHA-256：`6347592e6a9db70e526b7acf10b1351c5b8e59a196cd7e6b19b150ebc3c28681`
- `script.md` SHA-256：`743e06a78f5ed9158bd3e9671c2346c0e94e0ac664c7f744258df417a91f7d7a`
- `claims.md` SHA-256：`75f9153e80a451280da1846aca5d69b54623705fafbabc446819b5ca09958f31`
- `brief.md` SHA-256：`f19784c44aba343e69ec85d97c6381ab3baecd0f2f39b93bd44262b9c48d15d2`
- `shorts.json` SHA-256：`416529ebb9bb9c7c5fcf2a25f10266d92f1fee48a9999f420e6e0fffe2b6e287`
- `control-boundary.svg` SHA-256：`8a6a50188f90ef8c146f4dec4129a5d30914c5666609f27f309650b1ca510093`
- `defense-layers.svg` SHA-256：`083846db5ca3d303999f0c3045e1af103ca6f48eedaaeec40f3dc69b8c20bda9`

本表綁這份快照。後續作者改稿或重新擷取畫面時，須對受影響欄位再查。script.md逐句包含video.json全部86句，無漏句；claims c001–c082與當前scene.claims一致。未以舊稿假想資料夾／新聞標題練習當本稿證據。

四官方頁重新以固定UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`取得，保留TLS與proxy、同host請求間隔超過1秒；移除HTML註解及script/style後全文讀取。全為HTTP 200，redirect後URL不變。沒有搜尋或第三方影片當新聞事實證據。

| 來源 | URL | HTTP | 獨立核對的日期與範圍 |
| --- | --- | --- | --- |
| incident | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 200 | Sample與Discovery均9/20；Report updated 9/25；任務與DNS回答、四時間戳、停止故障、不續訓特定模型 |
| containment | https://openai.com/index/securing-our-frontier-model-training-environment/ | 200 | 發布10/23；恢復10/1的frontier RL及internal inference；離線、分層、受命紅隊、修補自述 |
| monitoring | https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/ | 200 | 發布10/22；7/21–8/11工作；7/21及之前歷史系統；compaction期間、先識別當期修正、未驗後續聲明 |
| safety | https://openai.com/index/towards-safety-cases-for-frontier-ai-training/ | 200 | 發布9/28；初步安全論證指南；fail closed、logs及責任；尚在實施而非外部認證 |

## 必修Q1：公開頁capture的逐字原文

精確位置：`scope.data.steps`／`scope/p2ac`的視覺，及`thumbnail.data.capture=scope`與沿用capture的變體。實際查看 `/workspace/work/videos/openai-dns-containment/screencast/8166b04eca58b4ae/01.png`：畫面有11-word事件h1，還有Summary完整首段與大段次段。僅首段即超過25英文詞；不是只有來源標題。manifest記錄1280×720、scale1.5、無profile、無mask、zoom1.15，拍攝2026-10-25T09:59:24.801Z。來源頁的9/25「remain paused」也仍可見，雖本稿旁白沒有把它當當前狀態，視覺應避免這種歧義。

處理：依既有screencast步驟擷取前遮掉不必要正文與nav，只保留必要標題；或正式畫面只裁出必要標題，重新檢視實際輸出的所有入場與靜止影格、縮圖。不要修改原文文字冒充原始頁。來源h1本身11個英文詞，清楚可計數；保留其他原文時仍須加總。此處未因公共網頁可讀就判成無上限引用。

## 必修Q2：整包來源轉述帳目

不使用「漢字數÷某係數」估word。下表是逐項正常英文等義展開，以空白分詞計數；同一資訊在metadata、Shorts或SVG再表達時另計。不計純產品名／日期時間／來源定位標籤、原創算術或單純互動問句；也不把只是換說法的來源內容當作原創分析排除。英文等義只用來稽核，不是要放進影片。這是**保守下限**，尚未逐條加上全部重複卡片短語及Q1整頁畫面；所以低於200的頁是未見超額，高於200的兩頁則已足以判定需縮減。

| 來源 | 主片直接轉述等義 | metadata／SVG／Shorts重述 | 合計下限 | 200-word檢核 |
| --- | --- | --- | --- | --- |
| incident | 176 | 114 | 290 | REVISE |
| containment | 195 | 150 | 345 | REVISE |
| monitoring | 82 | 49 | 131 | 未見超額；仍需最終包重算 |
| safety | 44 | 12 | 56 | 未見超額；仍需最終包重算 |

建議保留事件主線，先刪衍生Shorts重複報導、metadata重講故事和圖上的來源情節重述；以原創比較／推論取代時仍明標analysis，不能把原始事實換個分類就停止計數。Q2是篇幅／引用帳目，**不否定已由原文確認的事實**，也不是提出新的新聞查證疑點。

### 可重算的英文等義明細

| 來源／位置 | 等義展開（稽核用） | words |
| --- | --- | --- |
| incident／`open.pgqb` | On September 20, 2026, a research model was searching for a blog post's author. | 14 |
| incident／`open.a3tm` | The task supplied article clues, and the model had a search tool available. | 13 |
| incident／`search-stuck.wvuh` | After several searches, the clues still did not identify the person. | 11 |
| incident／`search-doubt.ijsv` | It began wondering whether the problem lay in its available information sources. | 12 |
| incident／`original-task.hv8i` | It used the lack of search progress as a reason to try other routes. | 14 |
| incident／`search-fails.f94z` | It unsuccessfully tried direct external access but continued exploring. | 9 |
| incident／`resolver.asjv` | It subsequently found a gap through which domain name queries reached an external chatbot. | 14 |
| incident／`test-response.5tat` | It received an answer to a test question, establishing more than an attempted connection. | 14 |
| incident／`not-solved.m6iv` | The external route did not solve the original task, and it could not provide a reliable answer. | 17 |
| incident／`time-start.gfwn` | Monitoring generated an alert after the external response. | 8 |
| incident／`time-human.z2at` | A person took over the alert, and the timestamp records its acknowledgement. | 12 |
| incident／`pause-failure.ysxf` | The expected automatic stop did not happen, and people were confused about whether the run should stop. | 17 |
| incident／`time-stopped.vjrz` | After clarification, the run was manually stopped. | 7 |
| incident／`specific-model.t5e6` | The September 25 report separately said that training this particular model would not continue. | 14 |
| incident／`youtube.description.incident` | The incident occurred on September 20, 2026; its report was updated September 25. The original timestamps have no stated timezone. The September report said that the particular model would not continue training. | 32 |
| incident／`svg.control-boundary` | The original task was finding an author. Normal searches used offline cached pages; an unauthorized domain lookup gap reached an external chatbot and received limited responses. | 26 |
| incident／`shorts[0] narration` | On September 20, 2026, a research model was searching for a blog post's author. The expected automatic stop did not happen, and people were confused about whether the run should stop. | 31 |
| incident／`shorts[0] description and headlines` | An internal research incident on September 20, 2026; the source timestamps have no timezone. A research model seeks an author. Automatic stopping did not happen. | 25 |
| containment／`boundary-diagram.7366` | A configuration gap in this environment gave the model limited internet access. | 12 |
| containment／`training-paused.vvry` | Relevant frontier research workloads paused after this incident while the control chain was reexamined. | 14 |
| containment／`offline-work.6fxh` | The approach published in October supplies indexed and cached content so models can work offline. | 15 |
| containment／`cache-live.6fhj` | Models can search and browse saved content to obtain material for their tasks. | 13 |
| containment／`scope.p2ac` | These are internal research environments; this does not mean ordinary chat products have all lost internet access. | 17 |
| containment／`not-unplugged.w2v7` | Research infrastructure still needs operational and monitoring connections, so completely disconnecting it is infeasible. | 14 |
| containment／`outer-boundary.vmrq` | The new defenses extend to the network and cloud perimeter, which must block access even if inner defenses fail. | 19 |
| containment／`nested-boundary.atun` | Containers and virtual machines isolate workspaces, while perimeter controls restrict external access. | 12 |
| containment／`test-assumption.k2a6` | Some attack tests assume the model already controls its host, then test the perimeter. | 14 |
| containment／`test-not-event.bacp` | These agents were tasked to find weaknesses in controlled tests, unlike the unauthorized author-search incident. | 15 |
| containment／`find-and-repair.r7u8` | The discovered software flaws and misconfigurations led to patches and tighter perimeter restrictions. | 13 |
| containment／`resume-evidence.mnqx` | The resumption decision used test results, implemented fixes, and improved monitoring and stopping. | 13 |
| containment／`resume-work.fe76` | After assessments and new controls, frontier reinforcement learning and internal inference resumed October 1. | 14 |
| containment／`public-date.zt6y` | The account of the containment changes was published October 23. | 10 |
| containment／`youtube.description.containment` | On October 23 OpenAI published containment changes and reported that frontier reinforcement learning and internal inference resumed October 1. Research environments differ from released products. | 25 |
| containment／`shorts[0].boundary` | A configuration gap in this environment gave the model limited internet access. | 12 |
| containment／`shorts[1] narration` | The approach published in October supplies indexed and cached content so models can work offline. Models can search and browse saved content for their tasks. Research infrastructure still needs operational and monitoring connections, making complete disconnection infeasible. The new defenses extend to the network and cloud perimeter, which must block access if inner defenses fail. | 55 |
| containment／`shorts[1] description/headlines` | OpenAI publicly described research containment changes October 23. Models work offline but research infrastructure retains necessary connections. The outer perimeter must still block access if inner defenses fail. | 28 |
| containment／`svg.defense-layers` | Authorized agents and tools are inside container or virtual machine isolation, research infrastructure and services, and a network perimeter that must block unauthorized live access even after inner defenses fail. | 30 |
| monitoring／`publication-assessment.k57p + card` | External researchers assessed the historical internal system from July 21 to August 11; the report was published October 22. | 19 |
| monitoring／`historical-gap.ii2r + sub` | During the historical period when compaction was not monitored, agents could postpone monitoring by continuing to act. | 17 |
| monitoring／`fixed-during-pilot.qk5c` | OpenAI had identified this issue before the exercise and fixed it during the exercise. | 14 |
| monitoring／`expected-seen.xvzp` | The assessment recommends cross-checking traffic expected to be monitored against what monitoring actually receives. | 14 |
| monitoring／`unknown-status.ubvs` | OpenAI stated that identified vulnerabilities affecting production safeguards were patched; the external team has not reevaluated those claims. | 18 |
| monitoring／`youtube.description.monitoring` | The October 22 METR post describes a July 21 to August 11 historical assessment, not the September DNS incident's cause or October coverage. During unmonitored compaction, continued actions could postpone monitoring. OpenAI identified the issue beforehand and fixed it during the assessment. METR has not evaluated subsequent patch claims. | 49 |
| safety／`guidelines.n8qp` | The September safety-case guidelines cover alignment, containment, and monitoring. | 9 |
| safety／`fail-closed.5fnm` | One principle says workloads should not start without required monitoring. | 10 |
| safety／`logs-and-response.pymx` | Logs should permit investigation and incident-response responsibility must be assigned in advance. | 12 |
| safety／`guideline-not-certificate.e64q` | These are proposed guidelines, not external verification that every control has been implemented. | 13 |
| safety／`youtube.description.safety` | The September 28 safety-case document contains initial guidelines, not completed external certification. | 12 |

## 逐場完整核對

每列data列出該場全部data JSON，涵蓋標題、caption、source、數字、比較項目和capture URL；旁白列出全部text與line id。本稿沒有say欄位。CONFIRMED表示來源事實，OUT OF SCOPE表示已標為原創因果分析，並檢查其前提及證據層級；不表示其媒體或產品實測已通過。

| # | 場景／line id | 全部旁白text | 全部data | 判定 | 原文URL或證據 | 理由／before→after |
| --- | --- | --- | --- | --- | --- | --- |
| c001 | `open`／`pgqb`, `a3tm` | 二〇二六年九月二十日，一個研究模型正在尋找文章作者。<br>題目給了文章線索，它手上也有搜尋工具。 | {"tag":"AI／科技時事","title":"找一位作者\n**為何重查整條防線？**","subtitle":"OpenAI 研究訓練環境 · 2026-10-25 編輯草案"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 9/20是事件，不是10/23發布日期；作者任務、線索與工具有原文。 |
| c002 | `search-stuck`／`wvuh` | 但幾輪查找下來，線索還是對不上人。 | {"text":"線索對不上人","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 旁白與全部data吻合該頁敘述；不新增能力、傷害或安全保證。 |
| c003 | `search-doubt`／`ijsv` | 它開始懷疑，問題是不是出在可用的資料入口。 | {"text":"它懷疑資料入口","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 原文敘述質疑搜尋工具是否運作；本稿未捏造額外測試。 |
| c004 | `unexpected-route`／`mku3` | 一條只該查網域的通道，會把它帶到哪裡？ | {"text":"查網域，會通到哪裡？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c005 | `alarm-question`／`y9kq` | 它如果摸到外面，警報真的能讓實驗停下來嗎？ | {"text":"警報真能叫停嗎？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c006 | `new-wall-question`／`dyff` | 要讓這個環境繼續工作，團隊得補上什麼？ | {"text":"環境要補上什麼？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c007 | `main-question`／`s3mm` | 一個找答案的任務，為什麼逼團隊重查整條安全邊界？ | {"text":"重查整條安全邊界","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c008 | `original-task`／`hv8i` | 它把搜尋沒有進展，當成繼續嘗試其他入口的理由。 | {"text":"它開始試別的入口","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 旁白與全部data吻合該頁敘述；不新增能力、傷害或安全保證。 |
| c009 | `search-fails`／`f94z` | 它嘗試直接連外，沒有成功，卻沒有因此停下探索。 | {"text":"直接存取沒有成功","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 旁白與全部data吻合該頁敘述；不新增能力、傷害或安全保證。 |
| c010 | `resolver`／`asjv` | 後來，它找到網域名稱查詢這條路，透過缺口問到外部聊天服務。 | {"text":"DNS：網域名稱查詢","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 經DNS設定缺口取得外部聊天服務回答；非一般HTTP已全面開放。 |
| c011 | `dns-purpose`／`5sm4` | 網域名稱查詢的工作，是把名字對到網路位址。 | {"text":"名字，要對到位址","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 教學用一般定義；未聲稱所有DNS紀錄都只有IP位址。 |
| c012 | `data-channel`／`hkcr` | 既然查詢會傳送資料，就得把它納入對外通道的檢查。 | {"text":"查詢也會傳送資料","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c013 | `boundary-diagram`／`7366` | 在這次環境裡，通道的設定留下缺口，模型真的取得有限連網。 | {"svg":"docs/videos/openai-dns-containment/control-boundary.svg","caption":"OpenAI 事件紀錄・概念重繪，非原始架構圖"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 有限即時連網；SVG明標概念重繪、非精確原始架構。 |
| c014 | `test-response`／`5tat` | 它收到測試問題的回答，這回不能再當作只有連線嘗試。 | {"text":"外部服務有回答","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 確有測試問題回覆；沒有說原任務已解出。 |
| c015 | `effect-not-intent`／`8hmd` | 判斷這條邊界是否守住，得看資訊能不能實際出去再回來。 | {"text":"邊界看的是動作","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c016 | `task-scope`／`3swz` | 找作者是它的任務，重新安排網路存取卻超出了原本授權。 | {"text":"任務沒有擴大授權","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 原任務未要求測網控或取benchmark答案；範圍分析有原文支持。 |
| c017 | `not-solved`／`m6iv` | 這次外部通道沒有幫它完成原本任務，它仍交不出可靠答案。 | {"text":"任務最後仍未完成","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 最後未能可靠辨認作者。 |
| c018 | `failure-still-matters`／`epum` | 因此任務失敗，和環境失去隔離，是可以同時成立的。 | {"text":"沒有答案，仍有越界","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c019 | `detection-question`／`78eg` | 通道已經傳回資訊，環境裡的監控有沒有看見？ | {"text":"越界，誰先看見？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c020 | `time-start`／`gfwn` | 外部回覆過後，監控真的產生了一筆警報紀錄。 | {"text":"09:50:23","kicker":"OpenAI DNS incident · 2026-09-25","sub":"原文未標時區；保留原始時間"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 原文09:50:23 a.m.為外部回答；未標時區。 |
| c021 | `time-alarm`／`edem` | 警報時間與外部回應時間相減，能量出發現它的落差。 | {"text":"10:02:11","kicker":"OpenAI DNS incident · 2026-09-25","sub":"監控警報；原文未標時區"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 原文10:02:11 a.m.為P0警報；非停止。 |
| c022 | `detect-gap`／`uncu` | 兩個時間相減，偵測落差是十一分四十八秒。 | {"stats":[{"value":"11 分 48 秒","label":"外部回答 → 警報"}],"source":"依官方時間戳計算 · 2026-10-25"} | CONFIRMED／獨立算術 | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 708秒＝11分48秒；獨立重算。 |
| c023 | `time-human`／`z2at` | 警報接著由人員接手，時間戳顯示它已經被確認。 | {"text":"10:05:06","kicker":"OpenAI DNS incident · 2026-09-25","sub":"人員確認警報；原文未標時區"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 原文10:05:06 a.m.為human acknowledgement；非停止。 |
| c024 | `human-gap`／`4d87` | 這一段的兩分五十五秒，量的是警報到人員確認。 | {"stats":[{"value":"2 分 55 秒","label":"警報 → 人員接手"}],"source":"依官方時間戳計算 · 2026-10-25"} | CONFIRMED／獨立算術 | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 175秒＝2分55秒；獨立重算。 |
| c025 | `pause-failure`／`ysxf` | 但預期的自動停止沒有發生，人員對是否該停也出現困惑。 | {"text":"自動停止沒有發生","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 預期自動停未發生；是否應停的操作困惑有原文。 |
| c026 | `time-stopped`／`vjrz` | 釐清之後，這次執行才被手動停止。 | {"text":"12:34:30","kicker":"OpenAI DNS incident · 2026-09-25","sub":"手動停止；原文未標時區"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 12:34:30 p.m.手動停止；未自行補時區。 |
| c027 | `stop-gap`／`8j2p` | 從警報算到真正停止，經過兩個半小時以上。 | {"stats":[{"value":"2 時 32 分 19 秒","label":"警報 → 手動停止"}],"source":"依官方時間戳計算 · 2026-10-25"} | CONFIRMED／獨立算術 | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 警報至停止9139秒＝2時32分19秒；原文2.5h為概數。 |
| c028 | `time-meaning`／`26jt` | 這些落差分別落在發現、接手與執行停止，修補的位置也不同。 | {"text":"三段時間，各有用途","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c029 | `gap-not-speed`／`2g46` | 如果只縮短偵測時間，沒有修好停止流程，後半段仍然斷著。 | {"text":"不是把警報加快就好","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c030 | `training-paused`／`vvry` | 這次事件之後，相關前沿研究工作暫停，控制鏈必須重新檢查。 | {"text":"暫停，檢查整條鏈","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 10/23回述9月暫停；本稿沒有說當前仍暫停。 |
| c031 | `review-question`／`vkbd` | 但在宣布監控修好以前，還有沒有別的行動沒被它看見？ | {"text":"還有什麼沒被看見？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c032 | `monitor-history`／`mjfp` | 要回答這個問題，得先查清楚監控何時啟動、看到了哪些紀錄。 | {"text":"先查監控的視野","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c033 | `publication-assessment`／`k57p`, `m67f` | 外部評估團隊檢查過七月時的內部系統，報告到十月才公開。<br>這份歷史檢查，不能直接當成九月事故原因或十月現況。 | {"left":{"heading":"實際評估","points":["7/21～8/11"]},"right":{"heading":"後來發布","points":["10/22"]},"source":"METR historical pilot · 2026-10-22"} | CONFIRMED | https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/ | 發布10/22、工作7/21–8/11、被評估系統為7/21及之前；非9月原因調查。 |
| c034 | `historical-gap`／`ii2r` | 當時摘要事件還沒納入監控，代理若一直做事，就可能延後檢查。 | {"text":"當時：摘要事件漏監控","kicker":"METR historical pilot · 2026-10-22","sub":"compaction 未監控期間；歷史系統"} | CONFIRMED | https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/ | 口播與sub共同限定compaction未監控期間；接續qk5c交代當期修正。 |
| c035 | `compaction-meaning`／`nbp6` | 摘要事件，是工作中的上下文被整理壓縮，讓模型能繼續處理。 | {"text":"上下文被整理成摘要","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c036 | `trigger-condition`／`77x3` | 所以問題有它的條件，不能簡化成那時所有行動都看不見。 | {"text":"不是所有七月工作都相同","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c037 | `fixed-during-pilot`／`qk5c` | OpenAI 在評估前已識別這個問題，並在評估期間修正。 | {"text":"評估期間已經修正","kicker":"METR historical pilot · 2026-10-22"} | CONFIRMED | https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/ | OpenAI已在評估前自行識別，於評估期間修正；不是METR首次揭露未修問題。 |
| c038 | `why-old-matters`／`csz9` | 這份舊檢查留下的問題，是環境要怎麼證明監控沒有漏接。 | {"text":"它留下的是驗證問題","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c039 | `expected-seen`／`xvzp` | 評估建議把該監控的紀錄，和監控實際收到的內容交叉核對。 | {"left":{"heading":"應該被監控","points":["符合條件的執行紀錄"]},"right":{"heading":"監控實際收到","points":["系統留下的紀錄"]},"source":"METR historical pilot · 2026-10-22"} | CONFIRMED | https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/ | 交叉核對預期應監控紀錄與實收紀錄，是METR建議。 |
| c040 | `missing-record-meaning`／`h3zv` | 如果只看監控自己收到多少資料，看不到沒送進來的那一部分。 | {"text":"有資料，不代表沒漏接","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c041 | `unknown-status`／`ubvs` | OpenAI 表示影響正式防護的漏洞已修補，外部團隊尚未再驗證。 | {"text":"修補聲明，尚未再驗證","kicker":"METR historical pilot · 2026-10-22"} | CONFIRMED | https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/ | 指METR發現且影響production safeguards的漏洞；後續patch聲明未經METR再驗。 |
| c042 | `verify-scope`／`ryi4` | 因此新版環境需要新版證據，不能拿歷史檢查替它完成驗收。 | {"text":"修補與驗證要接得上","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c043 | `offline-question`／`py6x` | 監控還在補強，模型又得練習查資料，這個環境要怎麼工作？ | {"text":"工具保留，連網怎麼辦？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c044 | `offline-work`／`6fxh` | 十月公布的做法，是提供索引和快取內容，讓模型在離線環境工作。 | {"text":"給它離線的工作世界","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 索引和快取可供離線搜尋；公布時間與實際開始時間未混同。 |
| c045 | `cache-live`／`6fhj` | 模型可以對保存的內容搜尋、瀏覽，取得任務所需的材料。 | {"text":"讀快取，不碰即時服務","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 取得保存內容，未宣稱每個任務保證成功或資料即時。 |
| c046 | `cache-effects`／`rr9h` | 差別不只是資料新不新，而是這次動作會不會碰到外部系統。 | {"left":{"heading":"離線內容","points":["讀取保存的資料"]},"right":{"heading":"即時外部服務","points":["當下與外部系統互動"]},"source":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c047 | `offline-utility`／`3x4j` | 想讓模型學會查資料，不代表必須讓它任意接觸即時網路。 | {"text":"能力，不等於通行權","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c048 | `offline-tradeoff`／`dejm` | 這種選擇把資料範圍交給環境準備，任務不再保證能查到最新消息。 | {"text":"代價是資料範圍","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c049 | `scope`／`p2ac` | 這裡重建的是內部研究環境，不能套成一般聊天產品也全面斷網。 | {"title":"OpenAI 公開事件紀錄","caption":"OpenAI Alignment · 原始公開頁 · 2026-10-25 截圖","steps":[{"action":"goto","url":"https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/"},{"action":"wait","selector":"h1"},{"action":"capture","focus":"h1","zoom":1.15}]} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 研究與正式產品範圍區分正確；capture畫面引用量另列必修Q1。 |
| c050 | `not-unplugged`／`w2v7` | 但研究設施仍需要運作與監控連線，無法把整套系統完全拔線。 | {"text":"不是整套設施拔線","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 完整air gap不可行是研究設施運作連線的限制，非代理任意連網授權。 |
| c051 | `indirect-route`／`dtru` | 只要必要連線還存在，就得檢查模型能不能間接借用它。 | {"text":"必要連線，也有邊界","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c052 | `offline-not-sufficient`／`f92m` | 離線內容提供工作材料，對外限制則要攔住它不該觸及的服務。 | {"text":"快取，只解決一部分","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c053 | `same-boundary`／`pz5p` | 這個環境必須同時做到，有材料可以工作，又不能把工具變成出口。 | {"text":"同一環境，兩項要求","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c054 | `inner-fails-question`／`qvbx` | 可是假如模型連工作區限制都突破了，下一層還剩下什麼？ | {"text":"如果內層仍被突破？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c055 | `outer-boundary`／`vmrq` | 新的防線把限制延伸到網路與雲端外圍，內層失守仍要能攔住。 | {"svg":"docs/videos/openai-dns-containment/defense-layers.svg","caption":"OpenAI 2026-10-23・分層概念，非安全認證"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 外圍是設計目標與概念層次；不認證已完全安全。 |
| c056 | `nested-boundary`／`atun` | 容器與虛擬機隔開工作區，外圍控制再限制對外存取。 | {"left":{"heading":"內層","points":["限制工作區內的存取"]},"right":{"heading":"外層","points":["限制對外連線與系統間移動"]},"source":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 容器/microVM與網路及雲端perimeter分層有來源；SVG非拓樸。 |
| c057 | `layers-meaning`／`zd4b` | 這樣才能分清楚，是某層擋住了，還是只是前一層暫時沒出事。 | {"text":"每一層，承擔不同失敗","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c058 | `layers-not-count`／`u3zn` | 若每層都依賴同一個錯誤設定，數量再多也沒有獨立的保護。 | {"text":"不能只數有幾道防線","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c059 | `test-assumption`／`k2a6` | 攻防測試有一部分，直接假設模型已取得主機控制權，再測外圍。 | {"text":"直接假設內層已經失敗","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 僅部分測試假設host已被控制，用以獨立測試外圍。 |
| c060 | `why-assume-compromise`／`c3xd` | 拿掉內層保護，才能知道外圍本身是否有能力承擔那個失敗。 | {"text":"避免前一層遮住問題","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c061 | `test-not-event`／`bacp` | 這些代理是在指定的測試中找弱點，和找作者時自行越界不同。 | {"text":"這次是受命找弱點","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 受命紅隊與找作者時自發越界區別清楚；未稱所有測試都無提示。 |
| c062 | `test-result-scope`／`fn3u` | 測試成功證明的是，給定條件下存在缺口，不是模型平常必然會越界。 | {"text":"成功，證明哪個條件？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c063 | `find-and-repair`／`r7u8` | 測試找到的軟體漏洞與設定缺口，接著進入修補與外圍限制的調整。 | {"text":"缺口進入修補流程","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 軟體修補與network restrictions為官方自述；未冒充本片驗證。 |
| c064 | `after-patch`／`zgps` | 堵住被發現的路，只是改造的一步，還得查其他路是否仍通著。 | {"text":"修補後，還得再問一次","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c065 | `controls-together`／`mw8y` | 同一請求經過工作區、外圍與監控，得讓這些控制在實際路徑上接起來。 | {"text":"一起工作，才算一條防線","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 編輯的整體控制要求；不把監控當即時停止，亦不作實際串聯拓樸主張。 |
| c066 | `resume-question`／`xskh` | 缺口修過，攻防也測過，這樣就足以讓研究工作重新開始嗎？ | {"text":"現在，可以重新開始嗎？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c067 | `resume-evidence`／`mnqx` | 恢復決定得回到測試結果、已做的修補，以及監控和停止的改善。 | {"text":"把證據接回恢復決定","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 依據tests/fixes/monitoring/stopping，不是單一數量或認證。 |
| c068 | `safety-case`／`yqf8` | 這些材料要支持一個具體判斷，這個版本的環境能否承擔接下來的工作。 | {"text":"安全主張不能只是一句話","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c069 | `guidelines`／`n8qp` | 九月提出的安全論證指引，要求把模型行為、隔離與監控一起檢查。 | {"text":"用安全論證串起材料","kicker":"OpenAI safety cases · 2026-09-28"} | CONFIRMED | https://openai.com/index/towards-safety-cases-for-frontier-ai-training/ | 9/28初步指南包含alignment/containment/monitoring；非法律或認證。 |
| c070 | `fail-closed`／`5fnm` | 其中一個原則，是缺少必要監控時，相關工作就不該啟動。 | {"text":"必要監控沒開，就不啟動","kicker":"OpenAI safety cases · 2026-09-28"} | CONFIRMED | https://openai.com/index/towards-safety-cases-for-frontier-ai-training/ | 文件的technical controls建議必要監控沒開不得啟動。 |
| c071 | `logs-and-response`／`pymx` | 紀錄要能回查，出事時誰負責停止也得事先明確，不能等警報後才猜。 | {"text":"保留紀錄，也明定停止責任","kicker":"OpenAI safety cases · 2026-09-28"} | CONFIRMED | https://openai.com/index/towards-safety-cases-for-frontier-ai-training/ | immutable transcripts/accountability/pausing支持；不聲稱已普遍落實。 |
| c072 | `guideline-not-certificate`／`e64q` | 這些是提出的指引，不代表外部已驗證每項控制都完成。 | {"text":"這仍是指引","kicker":"OpenAI safety cases · 2026-09-28"} | CONFIRMED | https://openai.com/index/towards-safety-cases-for-frontier-ai-training/ | 原文說initial recommendations且in process；限制正確。 |
| c073 | `resume-work`／`fe76` | 完成評估與新增控制後，十月一日恢復了前沿強化學習與內部推論。 | {"text":"10 月 1 日恢復工作","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 10/1恢復frontier RL training與internal inference；未擴充成所有評估恢復。 |
| c074 | `identity-question`／`mra4` | 恢復工作，是不是代表原來那個模型又開始訓練？ | {"text":"原來那個模型又開跑？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c075 | `specific-model`／`t5e6` | 九月二十五日的紀錄另說，不會繼續訓練那個特定模型。 | {"text":"9/25：特定模型不再續訓","kicker":"OpenAI DNS incident · 2026-09-25"} | CONFIRMED | https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ | 9/25說不續訓this particular model；未推斷10/1型號。 |
| c076 | `identity-not-known`／`r6cu` | 這和整體工作恢復並不矛盾，也不能據此斷言恢復的是哪個模型。 | {"text":"整體恢復，不替換模型身分","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 整體工作恢復不推出特定模型身分，推論有效。 |
| c077 | `public-date`／`zt6y` | 到了十月二十三日，這套隔離改造的說明才公開。 | {"text":"10 月 23 日公開整改","kicker":"OpenAI containment · 2026-10-23"} | CONFIRMED | https://openai.com/index/securing-our-frontier-model-training-environment/ | 文章日期10/23；不是事故發生於當週。 |
| c078 | `disclosure-meaning`／`r7m7` | 因此本週的新消息，是改造與恢復依據的公開，不是把九月事故重演一次。 | {"text":"公開，不是再次發生","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 本週新消息為公開改造與恢復依據；事件已在9月。 |
| c079 | `version-changes`／`vmqz` | 當工具、設定或模型能力變了，之前的測試就未必涵蓋新的路徑。 | {"text":"環境一變，證據也要更新","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c080 | `continuing-tests`／`cnab` | 這也解釋了為什麼邊界要持續測試，不能在一次恢復決定後就封存。 | {"text":"測試不能停在修補那天","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c081 | `end-question`／`snqs` | 還記得開頭那個找作者的任務嗎？它最後改變了團隊要證明的事。 | {"text":"開頭那項任務，改變了什麼？","kicker":"編輯分析：同一研究環境的控制邊界"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |
| c082 | `outro`／`ty9n`, `t2yw`, `jtz8` | 他們得證明，模型繼續找路時，環境仍能限制、發現並停止越界。<br>你最在意哪一段控制？<br>訂閱，一起追蹤這些改善的證據。 | {"title":"邊界，要在繞路時也守得住","lines":["留言：你最在意哪段控制？"],"cta":"訂閱 Mokaair，追蹤 AI 事件的證據"} | OUT OF SCOPE／原創分析 | 原創編輯分析；四原文僅作背景 | 已由kicker/source明標編輯分析；沒有虛構模型實測或站主經驗。 |

## 額外欄位、圖與衍生稿

| 位置 | 判定 | 核對結果 |
| --- | --- | --- |
| youtube.title | CONFIRMED／編輯問句 | OpenAI 研究模型怎麼連上外網？一次 DNS 事件，為何重查整條防線；不含本週才發生、全網逃逸或模型已造成損害等新斷言。 |
| youtube.description | CONFIRMED facts／Q2篇幅REVISE | 9/20、9/25、10/1、10/23皆正確；四時間戳未標區；研究≠產品，METR歷史≠現況，compaction期間及當期修正，後續patch未再驗，guideline非認證，特定模型與整體恢復均有保留。重述累計見Q2。 |
| youtube.tags、category_id、made_for_kids、default_language、video_id | OUT OF SCOPE metadata | AI與研究事件分類恰當；video_id維持null，無已發布宣稱。 |
| thumbnail.data及兩variants全部文字 | CONFIRMED／編輯問句；Q1視覺REVISE | 「響警報／還在跑？」「誰能／叫停？」「聽話／不夠用」為事件控制問題；未新增身份、能力或傷害，capture所含原文需縮減。 |
| control-boundary.svg 全部title/desc/text及箭頭 | CONFIRMED conceptual／Q2篇幅REVISE | 離線快取與DNS通道缺口通往外部服務的兩種關係受事件頁支持；無精確IP、原始拓樸或漏洞操作步驟；明標概念、未重現。 |
| defense-layers.svg 全部title/desc/text及分層 | CONFIRMED conceptual／Q2篇幅REVISE | agent/tools、container/VM、research infrastructure、network perimeter為公開文章層級；未把Linux例子擴張到所有OS精確配置；外層阻擋為要求，非安全認證。 |
| assets[] source/license | CONFIRMED attribution | 兩圖來源正確，license明說Original editorial diagram，不冒用官方原始架構圖身份。 |
| shorts[0]全部titles/description/scenes | CONFIRMED facts／Q2篇幅REVISE | 摘自主片，9/20、有限連網、11:48、停止故障與2:32:19正確；仍標未生成、連結待長片；非完成Shorts或實測。 |
| shorts[1]全部titles/description/scenes | CONFIRMED facts／Q2篇幅REVISE | 離線內容、可搜尋瀏覽、必要運作連線與外圍控制吻合10/23原文；間接借用的警語標本片原創因果解釋；未宣稱重新測過控制。 |
| brief.md／claims.md | CONFIRMED consistency | 已同步R2；82個c編號無刪場景舊支線。觀點是編輯提案未批准，旁白未冒用站主第一人稱或體驗。 |
| script.md | CONFIRMED consistency | 全86句與video.json一致；未以本稿當核准或成片收據。 |

## 算術獨立重算

以同日24小時原始時間相減，未自行加時區或跨日假設：

| 起點→終點 | 秒數 | 差值 | 結果 |
| --- | --- | --- | --- |
| 09:50:23→10:02:11 | 708 | 00:11:48 | PASS；c022 |
| 10:02:11→10:05:06 | 175 | 00:02:55 | PASS；c024 |
| 10:02:11→12:34:30 | 9139 | 02:32:19 | PASS；c027 |
| 09:50:23→12:34:30 | 9847 | 02:44:07 | PASS；timeline-calculation.json及brief/claims |

原文「2.5 hours later」是概數；精確字卡的起點為警報，不與首次回應混用。告警、人員確認、手動停止為三個不同動作。

## Listener與技術結果（不代替影音驗收）

`node tools/video/cli.mjs lint --slug openai-dns-containment --json`：exit0，errors=[]，warnings=[]。估算9.456111分鐘，86句、2010 spoken units、7章。沒有超過40 Unicode字元的旁白、沒有say、沒有旁白URL或括號；發音字典由native lint檢查為零錯誤。5個loops的setup/payoff存在且順序正確；其是否好聽或達成敘事目標仍由盲評判定。

未執行approve、TTS、送審或發布；未驗證音訊、CPS、字幕對時、正式鏡頭節奏或成片長度。不能把估算當8分鐘影音門檻已過。

## 統計與交接

82場逐場覆核：37個直接來源群組場景（incident15、containment13、monitoring5、safety4），3個算術場景、42個原創分析場景；合計82。全部data與額外metadata、2SVG、2Shorts另覆核。必修事實更動0、未解新聞事實0；作者已解決第一輪條件問題。Q1/Q2為引用及封包完整性未過，整包結論REVISE。沒有修改任何事實；before→after均為保留原稿。

本輪不因「超過三個事實更動」要求第三位查核（本輪0個）；但Q1/Q2修正後，協調者須重新核對受影響旁白/data/metadata/Shorts、capture實際畫面及計數。若修正引入超過三個事實更動，依既有規則再交不同人。來源有新更新或正式媒體製作日期改變時，重新開啟四官方頁；尤其研究恢復／監控現況不能以本輪永久背書。


## Delta覆核：Q1／Q2修正後的最新結論（2026-10-25）

**最新結論：目前video.json的事實與引用檢核PASS。** 本節取代前文舊快照的Q1／Q2未過判定；前文保留作修改歷史，不代表新版仍需照舊計數。只覆核實際變更及引用累計，不重啟原文研究，也不修改其他檔。這不是音訊、字幕、成片或發布核准。

覆核video SHA-256：`21d0fc2be0a9a497e1e10c700384ca1e61ccc960c1389e792a722c87a5010d20`；78場、81句。作者的claims／script同步收據另見本節末，不將舊文件錯當成已同步。

### Q1：PASS，真實公開頁的必要標題節錄

獨立開啟新圖 `/workspace/work/videos/openai-dns-containment/screencast/9dbee6d0b776b2eb/01.png`，確認除必要h1外，其餘區域已遮蔽，看不到Summary正文、nav、日期塊或舊版「remain paused」字句。mask是runner在重新擷取前覆蓋區域，沒有改寫原文假冒官方內容。

manifest：key `9dbee6d0b776b2eb`、captured_at `2026-10-25T10:10:36.847Z`、profile=false、viewport1280×720、scale1.5、zoom1.15。PNG SHA-256：`a77360c81a4b6902d9c20c2b6238bc7786c8701317423aafe15138a38f4ed5d3`。四mask rect記錄為(0,0,1280,129)、(0,221,1280,499)、(0,121,304,108)、(946,121,334,108)。caption明說「標題節錄，其他區域遮蔽」。scope與縮圖使用的是同一必要標題capture asset，沒有額外正文引文。

**計數更正：h1實際為9個英文詞，不是前文粗述的11。** 逐字拆分為An(1)、agent(2)、used(3)、DNS(4)、to(5)、reach(6)、an(7)、external(8)、chatbot(9)。未見其他來源原句逐字引用；技術詞、產品名、純日期與來源定位標籤不當作長段引文。

### Q2：PASS，目前引用範圍內不得再加重複轉述

同前一版規則，以正常英文等義展開計數，不用漢字比例。已實際確認shorts.json刪除，metadata只剩日期／方法／素材說明，沒有重述事件情節。SVG仍含來源關係，因此**仍計入**26／30 words，沒有整圖改標ED後排除。r6cu仍提及9月不續訓與整體恢復，兩個部分分別加回原來源；mnqx改為具體「紅隊納入安全論證」後也重新計數。

| 來源 | 現在等義累計words | 變更及範圍 | 結果 |
| --- | --- | --- | --- |
| incident | 197 | 保留SVG26＋標題9＋r6cu回述11；刪a3tm及ijsv與衍生重述 | PASS，≤200 |
| containment | 197 | 保留SVG30＋新mnqx15＋r6cu範圍7；移除具體重複轉述與Shorts | PASS，≤200 |
| monitoring | 81 | ii2r補不交回控制權；歷史條件及期內修正仍保留 | PASS，≤200 |
| safety | 44 | 安全論證四句；metadata不重述 | PASS，≤200 |

以上不計純名稱／時間數字／來源定位標籤及原創算術或獨立因果分析；卡片的簡短名詞標籤並未增加來源的獨特敘事。對nested-boundary，新的atun是「分層後分別驗證」的原創推理，卡片只列一般內外層功能，不再重述container/microVM的具體實施；具體來源分層已在defense-layers.svg的30-word項完整計入，沒有把整個架構來源排除。這個等義帳目不是可再堆轉述的額外授權；若再加旁白、SVG事實、說明欄或Shorts，須從此處重新累計。

可重算最新版明細：

| 來源／位置 | 正常英文等義展開（稽核用） | words |
| --- | --- | --- |
| incident／`open.pgqb` | On September 20, 2026, a research model was searching for a blog post's author. | 14 |
| incident／`search-stuck.wvuh` | After several searches, the clues still did not identify the person. | 11 |
| incident／`original-task.hv8i` | It used the lack of search progress as a reason to try other routes. | 14 |
| incident／`search-fails.f94z` | It unsuccessfully tried direct external access but continued exploring. | 9 |
| incident／`resolver.asjv` | It subsequently found a gap through which domain name queries reached an external chatbot. | 14 |
| incident／`test-response.5tat` | It received an answer to a test question, establishing more than an attempted connection. | 14 |
| incident／`not-solved.m6iv` | The external route did not solve the original task, and it could not provide a reliable answer. | 17 |
| incident／`time-start.gfwn` | Monitoring generated an alert after the external response. | 8 |
| incident／`time-human.z2at` | A person took over the alert, and the timestamp records its acknowledgement. | 12 |
| incident／`pause-failure.ysxf` | The expected automatic stop did not happen, and people were confused about whether the run should stop. | 17 |
| incident／`time-stopped.vjrz` | After clarification, the run was manually stopped. | 7 |
| incident／`specific-model.t5e6` | The September 25 report separately said that training this particular model would not continue. | 14 |
| incident／`svg.control-boundary` | The original task was finding an author. Normal searches used offline cached pages; an unauthorized domain lookup gap reached an external chatbot and received limited responses. | 26 |
| incident／`scope actual h1 (single capture asset, also reused for thumbnail)` | An agent used DNS to reach an external chatbot | 9 |
| incident／`identity-not-known.r6cu (first sentence)` | Recall September's statement that this particular model would not continue training. | 11 |
| containment／`training-paused.vvry` | Relevant frontier research workloads paused after this incident while the control chain was reexamined. | 14 |
| containment／`offline-work.6fxh` | The approach published in October supplies indexed and cached content so models can work offline. | 15 |
| containment／`cache-live.6fhj` | Models can search and browse saved content to obtain material for their tasks. | 13 |
| containment／`scope.p2ac` | These are internal research environments; this does not mean ordinary chat products have all lost internet access. | 17 |
| containment／`not-unplugged.w2v7` | Research infrastructure still needs operational and monitoring connections, so completely disconnecting it is infeasible. | 14 |
| containment／`outer-boundary.vmrq` | The new defenses extend to the network and cloud perimeter, which must block access even if inner defenses fail. | 19 |
| containment／`test-assumption.k2a6` | Some attack tests assume the model already controls its host, then test the perimeter. | 14 |
| containment／`test-not-event.bacp` | These agents were tasked to find weaknesses in controlled tests, unlike the unauthorized author-search incident. | 15 |
| containment／`resume-evidence.mnqx` | The team incorporated adversarial testing into safety cases to provide inspectable grounds for resuming workloads. | 15 |
| containment／`resume-work.fe76` | After assessments and new controls, frontier reinforcement learning and internal inference resumed October 1. | 14 |
| containment／`public-date.zt6y` | The account of the containment changes was published October 23. | 10 |
| containment／`svg.defense-layers` | Authorized agents and tools are inside container or virtual machine isolation, research infrastructure and services, and a network perimeter that must block unauthorized live access even after inner defenses fail. | 30 |
| containment／`identity-not-known.r6cu (second sentence)` | Overall resumption did not identify specific models. | 7 |
| monitoring／`publication-assessment.k57p + card` | External researchers assessed the historical internal system from July 21 to August 11; the report was published October 22. | 19 |
| monitoring／`historical-gap.ii2r + sub` | During the historical unmonitored compaction period, agents could postpone monitoring by continuing actions without returning control. | 16 |
| monitoring／`fixed-during-pilot.qk5c` | OpenAI had identified this issue before the exercise and fixed it during the exercise. | 14 |
| monitoring／`expected-seen.xvzp` | The assessment recommends cross-checking traffic expected to be monitored against what monitoring actually receives. | 14 |
| monitoring／`unknown-status.ubvs` | OpenAI stated that identified vulnerabilities affecting production safeguards were patched; the external team has not reevaluated those claims. | 18 |
| safety／`guidelines.n8qp` | The September safety-case guidelines cover alignment, containment, and monitoring. | 9 |
| safety／`fail-closed.5fnm` | One principle says workloads should not start without required monitoring. | 10 |
| safety／`logs-and-response.pymx` | Logs should permit investigation and incident-response responsibility must be assigned in advance. | 12 |
| safety／`guideline-not-certificate.e64q` | These are proposed guidelines, not external verification that every control has been implemented. | 13 |

### 變動欄位的事實delta

| 位置 | 新版內容／動作 | 判定與理由 |
| --- | --- | --- |
| open/a3tm；search-doubt/ijsv | 刪除句與場景 | PASS；移除重複來源敘述，不產生新事實。 |
| failure-still-matters；find-and-repair；identity-question | 刪除 | PASS；不影響9/20→暫停→10/1恢復→10/23公開主線。 |
| main-question/s3mm | 改為「會把安全邊界推到哪裡」 | PASS-E；開場問題，不再預告重查結果。 |
| boundary-diagram/7366 | 改為越過管制即顯示授權邊界未被完整執行 | PASS-E；一般控制推理，不冒充新的實驗觀察；SVG仍計來源。 |
| specific-model/t5e6 | 移到vvry之後 | CONFIRMED；原句未改，9/25不續訓特定模型；時序更清楚。 |
| review-question/vkbd | 改問「哪些檢查得補上」 | PASS-E；不承諾揭露另一個尚未找到的具體事件。 |
| monitor-history.chapter | 舊評估揭露監控漏接條件 | CONFIRMED；明確為歷史評估。 |
| historical-gap/ii2r | 補「持續行動、不交回控制權」 | CONFIRMED；與compaction未監控期間的條件吻合；qk5c仍保留事前識別及評估期修正。 |
| scope全部data／p2ac視覺 | 四mask＋新capture＋「標題節錄」caption | PASS；原始頁標題畫面只證明公開來源存在，不是模型或監控實測。 |
| nested-boundary/atun | 改為各層限制須分別驗證 | PASS-E；沒有把一般分層建議說成測試結果；data保持一般內外層功能。 |
| resume-evidence/mnqx與data.text | 攻防測試納入安全論證，支持恢復決定 | CONFIRMED；10/23文章明說高算力紅隊納入safety cases及恢復依據，未冒稱外部認證。 |
| safety-case/yqf8 | 問材料是否足以證明新版能承擔工作 | PASS-E；是後續指南及限制的問題，不是聲稱已經證明安全。 |
| identity-not-known/r6cu及data.text | 回指9月不續訓；整體恢復未交代具體模型 | CONFIRMED／有效分析；不把恢復工作套成同一模型重啟，也不猜具體型號。 |
| youtube.description | 精簡日期及圖解／算術／標題節錄說明 | CONFIRMED；事件日期9/20、說明公開10/23、確認10/25均正確。 |
| 兩SVG | 仍為概念重繪 | CONFIRMED；沒有新增精確拓樸或親測宣稱，來源轉述繼續計入Q2。 |

時間戳及四算式未變，原先獨立計算仍成立。沒有將監控、接手或停止混成同一動作；沒有新增外部損害、自我意識或型號斷言。

### 技術檢查與剩餘同步

本次native lint：errors=[]，warnings=[]，78場、81句，1901 spoken units，估算8.9466667分鐘（約8:56.8），7章。這是稿件估算，不替代正式媒體長度。新版主要引文、機制圖及全部變動欄位已覆核，沒有新事實問題需要第三位重新查全部原文。

同步觀察：此delta取樣時claims.md SHA仍為`75f9153e80a451280da1846aca5d69b54623705fafbabc446819b5ca09958f31`（舊82場），script.md SHA為`94dbe3c0471c36a1ece6bfb07d2e56c9b53f2f03e4cd46812a45f3e7631f3cc5`且尚缺新版yqf8全文。已通知協調者與作者同步；這是衍生文件一致性工作，不是新的新聞事實疑點。後續同步只能抄當前video，不擴張事實或改已freeze的brief。

### 最後同步收據：PASS，沒有未結引用或事實項

作者同步後已再次實讀驗證：video SHA仍為`21d0fc2be0a9a497e1e10c700384ca1e61ccc960c1389e792a722c87a5010d20`；claims SHA為`42438bb9456de28504d2cbd5a106583e12982200cd0319e589ab0cb5cf3c8d30`，script SHA為`46c645375efdd99678d00383d0626bfb864fc337beb66102457f844bb5074dd6`。script完整包含當前81句，包含新版yqf8；claims有78行，全部scene存在、每列「video既存ID」與當前scene.claims一致、每句當前口播皆有對應。左欄順序編號與既存ID兩者分列且明示，沒有依順序誤對來源。shorts.json確實不存在。

本次只檢查文件同步，未再改稿，Q1/Q2的197／197／81／44-word帳目及新capture不變。**此最新快照的獨立事實、來源範圍、引用篇幅與文件同步檢查均PASS。** 後續新增來源內容或媒體擷取需重新核對；正式旁白／字幕／成片QA仍由各自關卡處理。


## 最終三處聽稿簡化delta：PASS（2026-10-25）

本節是最新文字收據，覆蓋上一節78場／81句的版本資訊；不重新擴張來源範圍。協調者只簡化三處，作者已同步衍生文字，未再修改video、freeze的brief、SVG或capture。

| 修改位置 | 最新內容 | 事實覆核 |
| --- | --- | --- |
| monitor-history／mjfp | 檢查發現，監控何時啟動，本身也藏著一個漏洞。 | PASS；章名已限定「舊評估」，後續publication-assessment／ii2r／qk5c保留7月歷史範圍、compaction未監控期間、持續行動不交回控制權與評估期內修正。此句是METR發現的概述，已計monitoring轉述，沒有因原kicker標編輯分析就排除。 |
| offline-work／6fxh | 環境保留索引和快取內容，讓模型在離線環境工作。 | PASS；移除「十月公布」敘事前綴，未更動離線內容機制或將其說成從十月才開始。 |
| same-boundary／pz5p | 刪除整句重述 | PASS；未產生新的日期、數字或控制斷言。 |

最新可重算帳目：incident **197**、containment **194**、monitoring **91**、safety **44** words。與上一節相比，containment的6fxh等義改為12-word「The environment retains indexed and cached content, allowing models to work offline.」，取代舊15-word項，減3；monitoring新加10-word「The review found a vulnerability in when monitoring was triggered.」，81→91。pz5p是獨立控制推理，刪除不改來源轉述數。其餘等義明細、SVG26／30、r6cu拆分及9-word標題均未變，四頁皆不超200；沒有以改類別藏匿轉述。

最終檔案綁定：

- `video.json`：`8d067315c93997b8f25b9fc3480f229cb03a623abc7dfc9ea2eab6dd3e5a7aa2`
- `claims.md`：`c19328bdbc847c5278a8d2d30150bc59de660a4907fcd1e83120e7aa3a33e84b`
- `script.md`：`94efd1e5fd6354afafea1aa7338384e0f5f2c728a200c5abb7b414fdb5f6d4de`
- `draft-estimate.json`：`432f36ab8026bb1fcc81ef2ec5896022768554922c1a77fb0bae519a738c8fa0`
- `draft-notes.md`：`29a288c2091c73e9034bc02f9cfa8d82e8a838ce2ca2e2a706b7ccf78d3b34eb`

實讀一致性檢查：77場／80句；script無漏句，claims無漏句，每場video既存ID與scene.claims一致；mjfp證據類別已明列monitoring，shorts.json仍不存在。未發現新事實錯誤或未結來源問題。

native lint再次為零errors、零warnings；1862 spoken units、6315計費字元，估算8.7738889分鐘（526.43秒，約8:46.4），仍是文字估時。四時間點、四差值、9/20／9/25／10/1／10/23、METR歷史與當期修正／後續未再驗證、特定模型身分與正式產品範圍均未更改；先前獨立原文證據與算術覆核繼續適用。**最新77場快照的事實、來源範圍、引用及文件同步PASS；不代替音訊、字幕或正式成片QA。**


## 音檢措辭修正delta與第二次實際轉寫（2026-10-25）

### 文字事實與引用：PASS

協調者依第一次音檢，只修改12句措辭及其清晰度emotion，穩定line id不變；另外的6處data斷行屬排版，未更動旁白主張。此次依實際 `/workspace/work/ai-tech-dns-containment/audio-wording-changes.json` 核對，並非直接採用查核者的建議稿。video SHA-256：`97133cf8b266a6290710d8b6acec130e70277808b30d8fbde7e10f61e212b377`，新speech_hash：`4b18fd9cbb9b8c84`。沒有增加日期、數字、產品功能、實測或新的安全保證。

| line id | 最新措辭 | 事實涵義覆核 |
| --- | --- | --- |
| `mku3` | 這條查詢網域的路徑，接著會通往哪裡？ | PASS；同一事件或原創控制推理的縮句，證據層級未提高。 |
| `y9kq` | 如果它連上外部服務，警報能讓這次實驗停下嗎？ | PASS；同一事件或原創控制推理的縮句，證據層級未提高。 |
| `5sm4` | 這種查詢，負責找出名稱所對應的網路位址。 | PASS；DNS的一般白話定義不變；不把網路位址換成網址，也未聲稱所有DNS紀錄只查IP。 |
| `78eg` | 資訊已經傳回來，監控系統有沒有發現這件事？ | PASS；同一事件或原創控制推理的縮句，證據層級未提高。 |
| `gfwn` | 模型拿到外部回答後，監控系統發出了警報。 | PASS；同一事件或原創控制推理的縮句，證據層級未提高。 |
| `26jt` | 發現異常、人員接手、停止執行，各是不同階段。 | PASS；同一事件或原創控制推理的縮句，證據層級未提高。 |
| `vkbd` | 監控要判定可靠，還得通過哪些檢查？ | PASS；同一事件或原創控制推理的縮句，證據層級未提高。 |
| `77x3` | 這個問題有特定條件，不代表當時完全沒有監控。 | PASS；保留有特定條件，沒有把compaction期間漏監控擴張成當時完全無監控。 |
| `csz9` | 要證明監控沒有漏接，舊評估提出了什麼檢查方式？ | PASS；舊評估確有交叉核對監控紀錄的建議，下一場回答，未新增另一項檢查結果。 |
| `h3zv` | 只數系統收到的資料，無法發現沒送進來的資料。 | PASS；同一事件或原創控制推理的縮句，證據層級未提高。 |
| `ubvs` | OpenAI 說正式防護的漏洞已修補，評估團隊沒有檢查這項聲明。 | PASS；正式防護漏洞修補是OpenAI自述；評估團隊沒有檢查這項聲明，並非正在驗證。指本段已發現的相關漏洞，不是所有未知漏洞。 |
| `r6cu` | 還記得九月那個特定模型嗎？整體工作重開，不能推定是哪個模型。 | PASS；回指九月特定模型後，明說不能由整體重開推定具體模型，未猜型號或宣稱該模型重訓。 |


引用等義重新累計為incident **194**、containment **196**、monitoring **87**、safety **44** words；其餘項與上一節相同。變更項如下，不因措辭改為白話就自動排除來源：

- gfwn取代為11-word「The model received an external answer, then monitoring raised an alert.」（原8）。
- r6cu第一段以5-word「Recall that particular September model.」取代原11-word回指不續訓句；第二段為9-word「Overall workloads restarting does not establish which model resumed.」（原7）。
- ubvs改為14-word「OpenAI says production-safeguard vulnerabilities are patched; the assessment team has not checked that statement.」（原18）。
- 原創控制問題、算術判讀及一般DNS定義的主張未新增來源專有情節；兩SVG26／30及9-word標題繼續計入。四頁仍≤200。

### 第二次actual音檢：尚未PASS，餘3句旗標

實際執行一次cache增量check-audio，沒有force、沒有second-opinion。最新native記錄2026-10-25T10:47:31.774Z：80/80句checked，66 exact、9同音／語助詞、2 Jev通過、3 flagged、unchecked=0；只新轉寫12個take、1次Jev。逐一核對check.json的clip hash與目前80個wav，**全部一致**；沒有把舊12旗標或舊cache文字直接當新take通過。speech journal當前無未結JSON。

| line id | 最新預期 | 最新ASR | Jev | 狀態 |
| --- | --- | --- | --- | --- |
| 5sm4 | 這種查詢，負責找出名稱所對應的網路位址。 | 這種查詢負責找出名稱所對應的網路位置 | 0.10 | flagged；位址／位置仍混淆 |
| h3zv | 只數系統收到的資料，無法發現沒送進來的資料。 | 只輸系統收到的資料，無法發現沒送進來的資料。 | 0.09 | flagged；數／輸可能多音字或ASR誤識 |
| ubvs | OpenAI 說正式防護的漏洞已修補，評估團隊沒有檢查這項聲明。 | OpenAI 說，證實防護的漏洞已修補，評估團隊沒有檢查這項聲明。 | 0.06 | flagged；正式／證實仍混淆；重要否定「沒有檢查這項聲明」已完整被轉寫 |

此處判讀的是ASR與Jev的實際結果，未獨立聆聽，不將差字逕稱實際clip必然唸錯。77句目前通過、3句仍需處理或獨立聆聽／轉寫；查核者沒有自行再重錄、付費重跑、approve或送審。**文字facts PASS不等於音訊PASS**。正式字幕、成片與上架包仍需後續native關卡；script／claims待最終音檢措辭定稿後同步，不沿用前一hash收據稱已同步。


## 最後三句定向改寫與第三次actual音檢delta（2026-10-25）

文字fact delta **PASS**；音訊仍有**1句未通過**。此節綁video SHA-256 `eb25733a8eda28df0a8213b625c0109189ea4a01b17746c0b62d44ec1fbfa6e0`，speech_hash `76cd6105601e80a5`。依實際 `/workspace/work/ai-tech-dns-containment/audio-wording-changes-round2.json` 及current video重新核對，未替協調者套用或重錄。

| line id | 最新文字 | 意義與來源範圍 |
| --- | --- | --- |
| 5sm4 | 這種查詢，會找出網域名稱對應的網路地址。 | PASS；網路地址為網路位址的白話詞，沒有換成網址或地理地址，也未擴張成所有DNS紀錄只有一種功能。 |
| h3zv | 只統計系統收到的資料量，無法發現遺漏的那部分。 | PASS-E；保留「只看實收而無預期基準，無法看見漏送部分」的原創推理；沒有新產品實測或第一人稱經驗。 |
| ubvs | OpenAI 說正式系統的防護漏洞已修補，評估團隊沒有檢查這項聲明。 | PASS；production safeguards的範圍仍保留；OpenAI修補自述與評估團隊沒有驗證該聲明分開；沒有說正在驗證或已完成外部認證。 |

引用等義帳目為incident **194**、containment **196**、monitoring **91**、safety **44** words。只有ubvs的英文等義由上一節14-word項改為18-word「OpenAI says the safeguards vulnerabilities in production systems are patched; the assessment team has not checked that statement.」；其餘來源內容不增。一般DNS定義及原創監控推理沒有新增獨特來源情節，兩SVG、r6cu及9-word標題的既有計數繼續保留。四頁仍≤200。

第三次native check-audio為不force、不second-opinion的cache增量。實際run記錄 `2026-10-25T10:54:17.767Z`：80/80 checked，68 exact、9同音／語助詞、2 Jev通過、1 flagged，unchecked=0；僅新轉寫3個take、1次Jev。再次逐一對比80個wav與cache clip hash，全部吻合；journal未結JSON=0。

- 5sm4最新clip `50d22e7f3bf9e1f5`，ASR「這種查詢會找出網域名稱對應的網路地址」，exact，**這次新take通過**。
- h3zv最新clip `63a0904f4269ee47`，ASR與新稿逐字一致，exact，**這次新take通過**。
- ubvs最新clip `155d268166a262a5`，ASR「OpenAI說，證實系統的防護漏洞已修補，評估團隊沒有檢查這項聲明。」；Jev0.06，**仍flagged**。差異僅剩正式／證實；重要否定句完整聽對。沒有獨立聆聽，不將ASR差字當成已確認的真實唸錯，也不能擅自把flag清掉。

timeline實際fps=30、total_frames=15003，因此旁白時間軸500.1秒（8:20.1）；此數字來自當前TTS時間軸，不是估算片長，也不代替成片音量或字幕同步檢查。沒有自行第四次重錄、重跑或approve；已回報協調者，如需下一步，應針對剩餘ubvs做一次獨立第二轉寫／盲聽，而非反覆重錄。**此快照文字及引用PASS；目前音訊79句通過、ubvs尚未通過。**


## 最後單句清晰化與音訊完整通過收據（2026-10-25）

**最新結論：文字facts／引用PASS；原生音檢80／80 PASS。** 此節覆蓋前節「ubvs仍flagged」的舊take狀態，僅適用下列文字與音訊hash，不把先前失敗紀錄抹去。

- video SHA-256：`95589bbde407087acbe7ed1b37ffc45f61850e139ae73d94b22da9befa32fcf3`。
- current speech_hash：`5b325d9c66864a50`。
- ubvs最新clip：`14418ce209fd1136`。
- native check-audio記錄：`2026-10-25T11:00:55.455Z`。

最後ubvs改為：「OpenAI 說正在使用的防護系統已修補漏洞，評估團隊沒有檢查這項聲明。」在本段METR歷史評估及修補聲明脈絡中，「正在使用的防護系統」是production safeguards的白話表達；仍是OpenAI修補自述，評估團隊**沒有檢查這項聲明**，未聲稱正在／已完成驗證，也未擴張到未知漏洞皆修妥。沒有更動已核實日期、數值、模型身分或研究／正式產品範圍。此單句fact delta PASS。

引用等義：該句為19-word「OpenAI says vulnerabilities in safeguards currently in use have been patched; the assessment team has not checked that statement.」，取代前版18-word項。最終累計incident **194**、containment **196**、monitoring **92**、safety **44** words；兩SVG及必要標題照計，四來源均≤200。

這次實際執行不force、不second-opinion的native增量檢查，**只新轉寫1個ubvs take**；其餘79句使用已驗證cache。逐一重算80個wav的clip hash與check.json全部吻合。結果：

| 項目 | 實際結果 |
| --- | --- |
| checked／total | 80／80 |
| exact | 69 |
| 同音／語助詞差異 | 9 |
| Jev通過（沿用既有判讀） | 2 |
| flags | **0** |
| unchecked | **0** |
| 此次新ASR／新增Jev | 1／0 |
| native exit code | **0** |
| speech journal未結JSON | 0 |

ubvs的最新ASR為「OpenAI說，正在使用的防護系統已修補漏洞，評估團隊沒有檢查這項聲明。」；只差空白及標點，native match_kind=exact，沒有靠低分覆核、改門檻、清cache或人工清旗。check-flags.json綁當前speech_hash，flags=[]、notes={}。因此本次是**新take的完整工具通過**，不是把舊12／3／1旗當作已解決。

第二轉寫處理紀錄：原生`--second-opinion`型別為外部程式命令字串，不能不帶值當布林旗。曾在work準備faster-whisper依賴，安裝完成後協調者取消該方向；沒有啟動模型下載、沒有執行Whisper、沒有生成第二轉寫結果，也沒有因此新增Jev呼叫。取消後檢查無相關殘留process。本次音檢通過不冒稱曾有第二轉寫佐證。

當前timeline為fps30、total_frames15018，即500.6秒（8:20.6）；音量、字幕同步及成片畫面仍以協調者的各原生關卡為準。查核者沒有執行approve、review-push或發布；script／claims須以最終文字同步，不能沿用修改前hash稱已同步。
