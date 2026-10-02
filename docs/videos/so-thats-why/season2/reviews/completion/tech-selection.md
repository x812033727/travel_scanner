# 第二季剩餘科技16題全面裁決

日期：2026-10-01。執行：write_t26。範圍僅選題；此報告存在repo外。未改企劃清單、任務、Git、PR或媒體。13題採用／換角度，3題不採用同核心，0題以「困難」全面延後。選題可行性不是製作完成或獨立審稿通過；正式author仍逐claim直接讀來源。

## 比對方法與實際讀取範圍

逐題完整讀 season2-topics.json 的16個record及原 topic-checks/s2-A26-A38.md、s2-A39-A50.md 對應節。整份JSON跨欄搜尋第一季episodes.json100、season3-topics.json100、品牌stories.json100、AI terms.json81，再讀完整相關record的核心、鉤子、答案、Short、圖像例子與備註。不是只比標題。

第一季完整相關records：A01/A03/A06/A08/A09/A13/A16/A21/A24/S17/B10；並讀week3/A03.md完整長片／兩Short。第三季完整相關records：A51/A52/A53/A54/A55/A58/A61/A64/A70/A71/A72；A58原check全文另讀。品牌完整相關question/logline/六章point/takeaway：C05/C18/A13/C15/C10/C01/C19/C20。AI完整相關records：token、tokenization、context-window、context-compaction、context-rot、agent-memory、large-language-model、transformer、pretraining、rlhf、direct-preference-optimization、prompt-caching、multimodal-ai、ai-agent；另讀catalogue對應AI/agent/pretraining/multimodal來源與claim。AI token/context-window兩現有video.json全部旁白、description和兩Short全文再次抽取讀；首次直接print整個巨型JSON遭截斷，未以截斷輸出當全文。A48在terms81、catalogue及三相關staging包搜尋自駕／autonomous／飛機／車輛，無匹配。額外發現既有AI第一季06-digital-yesman完整稿，讀全文判A27實質撞核心。

## 逐題裁決

### A26 — 不採用同核心

原題：為什麼AI聊太久會忘記前面說過的話？容量、截斷、摘要與長文漏看，全部已由上下文試片覆盖。明確existingpath：docs/videos/ai-term-context-window/video.json及shorts.json；terms.json context-window/context-compaction/context-rot/agent-memory。完整稿已分「沒送進去／摘要漏掉／看了卻答錯」，用三份會議紀錄、「尚未核准」交接、桌面與倉庫例子。改比喻或換對話仍是同核心，不另author A26。

一手來源原線索：Anthropic context windows https://platform.claude.com/docs/en/build-with-claude/context-windows ；Liu研究 https://arxiv.org/abs/2307.03172 。不必因来源可讀就重複生產。當日此裁決依完整現有包，不宣稱本輪重新核所有研究主張。

### A27 — 不採用同核心

原題：為什麼AI常常順著你說？AI81的RLHF/DPO僅訓練概念尚可區隔，但額外existingpath docs/ai-video-season-01/episodes/06-digital-yesman.json已完整講迎合、2023年五助手四任務、人類偏好與正確性的張力、支持感受vs替判斷背書、無心機假設、虛構工作提案例子及两Short。同研究換說法仍重複。

原一手研究 https://arxiv.org/abs/2310.13548 。2025服務回滾若獨立做更新事故是另一題，但本輪不把品牌歷史附帶改成新A27強湊支數。此record作不採用同核心裁決，不能記為新媒體完成。

### A28 — 換角度，採用「知道今天日期，為什麼不等於知道今天新聞？」

AI81 pretraining、large-language-model、system-prompt與第一A01只相鄰原理；第一A01是假書目／評分鼓勵猜，AI pretraining是如何形成基礎能力。本題以日期由產品提供vs事件資料需另取得作故事，避百科／訓練教程。與A26聊天歷史、A70串流不相同。

今日直讀Anthropic system prompts overview https://platform.claude.com/docs/en/release-notes/system-prompts/overview ：web及UA正文可讀，产品在對話開始透過system prompt提供目前日期，該產品prompt更新不套API。研究Dated Data https://arxiv.org/abs/2403.12958 今日web摘要可讀，只談測試模型的有效截止與公布值不一致，不給全模型精確截止日。原check「訓練完知識固定」過絕對，刪；不說不上網一定不能得知（使用者可貼新資料、工具可取資料）。不列2026所有產品功能與型號。

### A29 — 換角度，採用「不抽籤，AI回答為什麼也可能不同？」

原本下一token機率條／抽樣骰子與第三A70完整record的候選機率／逐token生成及第一A01接龍重疊；換到可重現性，先區分抽樣，再以2025研究團隊的batch invariance故事談特定推論系統即使greedy亦可能因批次運算順序／有限精度不同。AI81 transformer/LLM只相鄰，不讲整個架構。例子是排隊批次與四捨五入示意，避A70一排積木逐字流。

今日web與UA actual body直接讀 https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ （Horace He等，2025-09-10）。限定該分析／實驗配置，不把同時用戶說成資料混入，不說所有GPU每次都不確定或temp0所有產品都不保證，亦不教平台參數設定。未自行跑研究程式／API或實測。

### A30 — 不採用同核心

existingpath docs/videos/ai-term-token/video.json及shorts.json。完整稿已包括中文兩種編碼、社團公告精簡、用量不是字數、整份請求與歷史重送、輸入／輸出分開、快取／推理／工具依服務欄位、用量不等於帳單。AI81 token/tokenization/prompt-caching；第一A08用strawberry分詞、第三A70逐token。原题若刪未核「廠商成本所以這样訂價」動機，只剩既有稿已做的內容，不另author。

Anthropic pricing及官方分詞工具只是計費規則／計數，不能證明所有供應商定價動機。可用 https://platform.claude.com/docs/en/about-claude/pricing 作原線索，但本輪不报價／不宣稱重新核當日价表。

### A32 — 選入，boot／bootstrap的啟動悖論故事

品牌C05是Bradley的重開機鍵到Windows安全登入鍵，六章未解靴環字源／每階段載入下一階段。第一/第三/AI81無同核心；不挪用C05五分鐘發明／比爾／安全鍵。

今日UA讀Caltech CS124原教學30頁 https://courses.cms.caltech.edu/cs124/lectures-wi2017/CS124Lec05.pdf ，Bootstrapping節可讀：多階段載入下一階段，並說靴環俗語來源；web初次失敗，不能寫成web成功。詞源專家原線索 https://listserv.linguistlist.org/pipermail/ads-l/2005-August/052756.html 可補原用例但本輪未重取。正式稿不需要最早1953/1975年份、1834第一用例、吹牛男爵或海因萊因動機，避免歷史查無原件卡住整題。靴環不是綁鞋帶；教授教學來源不是發明當事人口述史。

### A34 — 換角度，保留「硬體不用了，為什麼仍認得儲存圖示？」

品牌C18完整六章核心是日本磁碟片法規撤除，原A34 Short2「日本2024才廢」完全拿掉。品牌C20是接龍的滑鼠教學目的，不是磁碟圖示辨識。第一/第三/AI81無samecore。本题用物件辨識vs學來的操作符號，不講法規／全球停產。

今日web+UA直讀NN/g作者第一手研究 https://www.nngroup.com/articles/floppy-disk-icon-understandability/ 2025-07-04。83%聯想到儲存、另13%字面物件，中位41歲、美國英語受試；不能推全球所有年輕人都會、也不把辨識當「永遠最好」或所有軟體保留的已證因果。Short2可換自動儲存／同步／匯出對圖示動作的差別，來源同篇，無教程與產品推薦。

### A35 — 換角度，採用法院通知的80GB/74.4GB爭議

第一A03完整包已讲1TB/931GB、IEC與容量換算的兩Short；原A35的容量差百分比主線不採。保留具体Safier官司文件：標示被指控的內容、備份軟體與加註提案、不認責條款，80GB/74.4GB只是原告主張示例。品牌C10是員工發明報酬，不是容量標示消費者案，避免挪和解金戲劇。

新取得一手政府保存22頁PDF https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_05-cv-03353/pdf/USCOURTS-cand-3_05-cv-03353-4.pdf ，web與UA actualbody可讀：Doc31 2006-03-17初步核准＋通知，第4–5頁不認責、第6頁80GB/74.4GB屬原告指控、第7頁開始救濟提案。這不是最終核准原件！正式author先嘗試補最終order；未取到則稿中明说「初步核准的和解提案／通知」，不報NBC的最終核准日期、百万买家、30美元或已履行结果。核不出最终亦不需延期整題，初步文件本身可以成為窄故事。0/5/6 suffix猜測URL本輪web不可讀，不宣稱成功。

### A38 — 選入，窄GPS衛星相對論頻率補償

更正先前以第三A58為同題的粗判。A58全文record+原check只有手機石英／NTP／NITZ／GNSS來源與原子鐘，無相對論頻率。品牌A13完整六章是1983民航政治承諾、2000關選擇性可用性、公共免費廣播；C15是Garmin轉型。三者沒有本題的速度／重力對衛星鐘的方向不同及預設頻率偏移。可選入但不用手機自動對時／免費政策敘事。

今日UA全PDF248頁文字讀取定位到IS-GPS-200N印刷14頁§3.3.1.1與時鐘校正章 https://www.navcen.uscg.gov/sites/default/files/pdf/gps/IS-GPS-200N.pdf ，offset −4.4647E-10補償relativistic effects可讀。只稱2022N文件，不稱current；理論解释原線索Ashby https://pmc.ncbi.nlm.nih.gov/articles/PMC5253894/ 待正式当日重读。可用約38.6微秒粗算，刪「每日必差10公里」／真機失效實測／出廠設定；如要談發射前需Ashby原文，不把規格無此字當證明。

### A42 — 換角度，採用電影觀看vs互動操作的幀率感受

第一A21是多張夜景對齊降噪，第三A64是串流分段選碼率／緩衝，A61是加减色，不是fps、曝光與操作需求。品牌C01/C19六章是播放器經營／收購，无24fps機理。以曝光模糊與2007射擊／移動任務研究，避「電影24就夠」「遊戲必60」排序。

今日web+UA RED https://www.reddigitalcinema.com/red-101/shutter-angle-tutorial Appearance節读到近180°条件24fps約1/48秒；是常見例子不是所有电影曝光。今日web讀作者WPI https://web.cs.wpi.edu/~claypool/papers/fr/ ，两研究近100人、快而準射擊受fps下降影響較大，移動較可忍；正式稿可補原PDF。1927SMPE原件未取得，刪聲音定標最早折衷／Hobbit媒體意見／人眼上限，毋須因历史來源缺口延後原理。

### A43 — 選入，離譜故事篩選是模型推論

第一A09密碼组合、第三A54驗證碼SIMswap與A55鎖頭可信度，仅安全領域相鄰；AI81 deepfake/red-teaming是生成痕跡／系統測試，無Herley低基率筛选模型。用虛構空白訊息卡／回覆漏斗，不演示诈骗脚本或嘲笑被害者。

今日UA实body重新讀Microsoft研究Herley2012 PDF https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/WhyFromNigeria.pdf ，552946bytes，self-identify／低基率模型可讀。第一次取得后stdout遇字形编码錯，第二次UTF8讀取正常；不能把第一次當完整log。不是实证「故意写错字」，不说都如此。补今日FBI https://www.ic3.gov/PSA/2024/PSA241203 与FTC https://consumer.ftc.gov/articles/how-avoid-scam 当日正式稿需再次直接讀，避免文字正確=安全。

### A45 — 換角度，採用「無線充電為什麼也要對準？」

第一S17电池SEI老化／高温，第三A51充電后段CC-CV／80%暂停；已產A37電源轉換頻率／體積。原A45熱伤电池／80%多讲会撞；改双线圈磁耦合、摆歪与磁吸对准，速度熱只一句带条件，不做充電后段课或通用效率百分比。

今日Apple web/UA108377 https://support.apple.com/en-us/108377 正文可讀：位置移動可能停止供電、会稍暖、过暖可能限制80%以上。今日WPCweb https://www.wirelesspowerconsortium.com/knowledge-base/magnetic-induction/ 为目录，可再click原Principle/Coupling；https://www.wirelesspowerconsortium.com/knowledge-base/ 官方FAQ实际可讀磁吸對準／效率，但版本與瓦數全删就不用做最新規格排名。iFixit單一測試36%不採，沒有自己的手機溫度／電費／充電實測。

### A47 — 選入，名稱與後補標語的故事

第一A06是Wi-Fi穿牆衰減，第三A55是HTTPS安全，不是命名；第一A13藍牙古王代號轉正式與此不同命名物件／例子／因果，避免logo字源支線。品牌100完整索引無Wi-Fi命名同题，C04是国家網域收費。

今日web與UA实际body https://boingboing.net/2005/11/08/wifi-isnt-short-for.html 讀Phil Belanger當事人来信：Interbrand命名與之后tagline。宿主是媒體，證據範圍是公開刊出的當事人說法，不冒称聯盟正式聲明；作者Doctorow前言Hi-Fi推論不能當命名者動機。首UA剝除script后僅151字看不到內容，第二次保留嵌入內容取得引文，两次皆200但只有后者支持；記錄限制不填造读到。Interbrand目前官网案例未取得，刪10候選名字列表／具体年份不必要細節。

### A48 — 換角度，採用自動化任務與監看邊界

AI81 artificial-intelligence自治定义、multimodal圖像问答、ai-agent工具循环与权限，是相邻词，完整records與相关staging未出现飞机／自駕案例；不把LLM agent自动化直接類比機師。品牌GarminC15飞航只是业务，占比故事，無autopilot。

改題「同叫自動駕駛，飛機和汽車包辦了哪些事？」用航空選定航路/模式仍需机师监看、ATTOL研究测试非商业採用、道路限定运行条件的区分，刪谁更困难一概排名／机师全按按钮／高空绝无障碍／2026城市数。

今日Airbus ATTOL官方 https://www.airbus.com/en/newsroom/press-releases/2020-06-airbus-concludes-attol-with-fully-autonomous-flight-tests web與UA可讀，测试性质而非无人商业飞机。FAA-host Airbus14页 https://www.faa.gov/sites/faa.gov/files/2022-11/AirbusSafetyLib_-FLT_OPS-SOP-SEQ02%20-%20Automation.pdf web可讀，UA403，须如实分開取得方式；NASM馆藏web403，不講1914則可删。正式稿要补NHTSA或SAE原ODD责任範圍，而非用Waymo城市数证明所有道路复杂度；有限功能≠同一自治等级，源規範年次不稱最新。

### A49 — 換角度，採用「吹完能玩，為什麼不能證明吹氣有效？」

第一B10是任天堂花札转型、品牌C20滑鼠教学／遊戲，与卡帶接點及因果缺口不同。以同时拔出、吹、重插的记忆不能隔离因素，属于明确编者推论；不宣称研究已证明重插才关键。

今日UA任天堂原支援全文200136441bytes https://en-americas-support.nintendo.com/app/answers/detail/a_id/54157/~/health-%26-safety-precautions%3A-cartridge-based-consoles-%28nes%2C-super-nes%2C-and Game Pak precaution可读：不要吹、弄濕或弄髒，可能损坏。删72针（不套红白机）、非正式两不同卡帶劣化测試、唾液腐蚀明确成分因果没原文则删，不教清洁／拆修／用液体。只带官方保养警语和区分同时动作不能推出单一因果，不假裝知道每次成功原因。

### A50 — 選入，螢幕／感光陣列造成摩爾紋

第一A21多帧夜景降噪，第三A61 RGB/CMYK混色、A53材料老化、A64串流碼率，都没網格取样與干涉形成低频图案。可保留兩格重疊／角距變化，避免换角度保证消失。

今日web原作者摘要 https://arxiv.org/abs/1805.02996 可讀pixel grids interference；UA PDF https://arxiv.org/pdf/1805.02996 回IncompleteRead只收到6291456byte，本轮没当完整原文成功。正式稿再取作者HTML／PDF导论来核undersampling与角距细节；只读摘要时只保留摘要支持的格纹核心。原论文数据集／算法成果与本片无关；摩爾名称历史可删。与滚动快门时间条带分开。之后示意网格要计算或拍摄验证，不用AI伪造pattern当实测；此处尚无图像生成或验证。

## 可追溯UA实际取得摘要

User-Agent统一 Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)。本轮不同host批量请求，同host重复均间隔>1秒。下面是UTCstart/end，不是本機時區；所有证据确认日期2026-10-01。

| 题 | UTC起→止 | 实体／讀取結果 |
| --- | --- | --- |
| A32 | 12:14:02.942602→12:14:40.279096 | 200/1432157bytes/30頁；Bootstrapping正文 |
| A34 | 12:14:40.279289→12:14:43.311771 | 200/129707；83%／美國英語／median41正文 |
| A35 | 12:14:43.311983→12:14:45.287594 | 200/136585/22頁；Doc31初步核准＋通知 |
| A38 | 12:14:45.287734→12:15:02.626762 | 200/3338120/248頁；频率offset章 |
| A42 | 12:15:02.626930→12:15:04.307782 | 200/41688；Appearance正文 |
| A45 | 12:15:06.988355→12:15:07.863147 | 200/164276；Apple位置與发热条件正文 |
| A49 | 12:15:11.969318→12:15:14.411735 | 200/136441；Game Pak precautions正文 |
| A28 | 12:16:11.131941→12:16:12.529291 | 200/360213；当前日期／API限定正文 |
| A29 | 12:16:12.529493→12:16:12.952388 | 200/97253；temperature0／batch-invariance正文 |
| A43 | 12:16:12.952591→12:16:22.116009 | 200/552946；PDF模型正文UTF8可讀 |
| A47 | 12:16:22.116316→12:16:22.508066 | 200/90542；當事人来信嵌入正文可讀（不採首次剝除后的空内容） |
| A48 | 12:16:22.508352→12:16:24.541254 | 200/228837；ATTOL官方研究测试正文可讀；元数据日期不同不可拿来改原press date |

A48 FAA UA403；A50 UA PDF不完整；对应web取得与失败已分别列。未把HTTP200、标题、检索摘要或仓库旧check当作本轮读到全文。A26/A27/A30裁决以现有完整稿重复为由，不需重演一轮source事实核准。来源可行性只是author准备，后续13包需逐claim当日核与另一非作者独立review。
