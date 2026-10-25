from pathlib import Path
import copy, hashlib, json, re, datetime

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
CACHE = Path("/workspace/work/brand-story-20261025/c09-audit/source-cache")
EXPECTED_BASE_SHA = "875eaca7ba51de28a9e2a198dfd8070325aabec91b58bb7cb903731415fb233a"
REVISION = "length-extension-r2"
R1 = OUT / "history" / "r1"
DATA = json.loads(r'''
{
  "additions": [
    {
      "after": "c09r009",
      "text": "報導解釋，軟鐵能順著不規則的裂縫變形；當時追求的是讓釘子貼進岩縫，不是讓它用完還保持原樣。",
      "source": "S4",
      "paras": [
        "028"
      ],
      "quote": "malleable iron",
      "gain": "補明早期材料的變形用途，區分貼合裂縫與可重用的價值。",
      "prompt": "Close-up at a workbench, one anonymous adult bending a plain soft metal spike beside a narrow gap between two blocks, soft window light from the left.",
      "camera": "pan left",
      "id": "c09le001",
      "scene": "c09le-shot-001"
    },
    {
      "after": "c09r013",
      "text": "他說，自己的釘子用鉻鉬鋼製作；爐旁還有鐵鎚和鉗子，金屬得在手上一步步加工。",
      "source": "S4",
      "paras": [
        "033"
      ],
      "quote": "chrome-molybdenum steel",
      "gain": "增加當事人所說的合金材料與手工工具，不以材料名稱推價格或利潤。",
      "prompt": "Medium shot at a forge bench, one anonymous adult holding a plain metal blank with tongs, mild side light from the right.",
      "camera": "tilt down",
      "id": "c09le002",
      "scene": "c09le-shot-002"
    },
    {
      "after": "c09r013",
      "text": "同一段回憶裡，連扣環也幾乎是手工：夾在便攜虎鉗上銼修，或用手鑽加工，工具跟著車子搬動。",
      "source": "S4",
      "paras": [
        "033"
      ],
      "quote": "hand-drill them",
      "gain": "補手工扣環的銼修與手鑽工序，與後段工人調整扣環形成製造動作的回收。",
      "prompt": "Close-up at a portable workbench, one anonymous adult filing a plain metal carabiner held in a small vise, soft overcast light from the left.",
      "camera": "pull back",
      "id": "c09le003",
      "scene": "c09le-shot-003"
    },
    {
      "after": "c09r040",
      "text": "報導追溯，英國攀岩者早先會用小石塊卡進岩縫，再把短繩套在石頭上；後來，有孔的金屬螺帽也進了器材袋。",
      "source": "S4",
      "paras": [
        "007"
      ],
      "quote": "the hole",
      "gain": "補充楔塊從天然石塊到有孔金屬的具體動作，支持替代工具並非品牌首創。",
      "prompt": "Close-up at a rocky practice wall, one anonymous adult holding a short rope loop beside a small stone in a gap, soft overcast light from the left.",
      "camera": "push in",
      "id": "c09le004",
      "scene": "c09le-shot-004"
    },
    {
      "after": "c09r040",
      "text": "到了六〇年代初，英國鐵匠開始加工不同尺寸的金屬楔塊；修納德最初用的，則是鋁製飛機螺帽。",
      "source": "S4",
      "paras": [
        "007",
        "008"
      ],
      "quote": "aluminum aircraft nuts",
      "gain": "補英國加工楔塊與當事人最初使用航空鋁螺帽的區別，讓後接1959/1960的回憶不被誤讀為更早使用六〇年代英國成形楔塊。",
      "prompt": "Medium shot at a metalworking bench, one anonymous adult measuring a plain wedge-shaped metal blank, soft lamp light from the left.",
      "camera": "pan right",
      "id": "c09le005",
      "scene": "c09le-shot-005"
    },
    {
      "after": "c09r027",
      "text": "那枚釘子不只接繩。文章還寫，人把腳梯接上扣環，靠器材向上移動，睡覺的吊床也能懸掛在釘子上。",
      "source": "S1",
      "paras": [
        "004",
        "009"
      ],
      "quote": "sleeping in hammocks",
      "gain": "補岩釘在人工攀登中連腳梯及吊床的實際角色，讓後續克制使用的取捨有具體負擔。",
      "prompt": "Medium shot at a plain climbing practice wall, one anonymous adult examining a carabiner connected to a short webbing ladder, mild side light from the right.",
      "camera": "pan right",
      "id": "c09le006",
      "scene": "c09le-shot-006"
    },
    {
      "after": "c09r029",
      "text": "尺寸還連著攜帶動作：薄片釘和較厚的釘分組掛在扣環，扣環開口的方向也得安排。",
      "source": "S1",
      "paras": [
        "013",
        "014"
      ],
      "quote": "one hand",
      "gain": "將分類落到分組懸掛及扣環方向的具體器材動作。",
      "prompt": "Close-up at an equipment table, one anonymous adult hanging a plain metal piton on an open carabiner, mild window light from the right.",
      "camera": "tilt up",
      "id": "c09le007",
      "scene": "c09le-shot-007"
    },
    {
      "after": "c09r029",
      "text": "文章還要人一隻手就能取下、掛回；回收一段路線的釘子時先排好，免得到末尾才停下分類。",
      "source": "S1",
      "paras": [
        "014",
        "016"
      ],
      "quote": "sorting",
      "gain": "補單手取掛與回收時預先排序的效率取捨，限定為1967文中主張。",
      "prompt": "Medium shot at a packing bench, one anonymous adult sorting plain metal pitons into separate groups, soft overhead light.",
      "camera": "pull back",
      "id": "c09le008",
      "scene": "c09le-shot-008"
    },
    {
      "after": "c09r029",
      "text": "同一篇文章提醒，最常見的錯誤是把合金釘敲得太深；在垂直裂縫裡，固定力也靠它抵抗轉動，不是只靠猛敲。",
      "source": "S1",
      "paras": [
        "018"
      ],
      "quote": "overdrive",
      "gain": "補明固定與抗轉動的機制，將多敲不一定更好推進到使用取捨。",
      "prompt": "Close-up at a plain practice block, one anonymous adult examining the contact between a metal piton and a narrow gap, soft side light from the left.",
      "camera": "pan left",
      "id": "c09le009",
      "scene": "c09le-shot-009"
    },
    {
      "after": "c09r029",
      "text": "原文把放入與取出的時間一起算，還特別提醒忍住多補那一錘：它可能讓回收更難。",
      "source": "S1",
      "paras": [
        "019",
        "021"
      ],
      "quote": "placement time and removal time",
      "gain": "補放入與取回的總時間及額外一錘的代價，連回可重用商品的實際工作。",
      "prompt": "Medium shot beside a plain practice wall, one anonymous adult pausing with a hammer above a metal piton, mild overcast light.",
      "camera": "push in",
      "id": "c09le010",
      "scene": "c09le-shot-010"
    },
    {
      "after": "c09r037",
      "text": "而且能回收也有期限。那份器材文章說，合金釘會長時間保持形狀，但出現疲勞裂紋就該退役。",
      "source": "S1",
      "paras": [
        "049"
      ],
      "quote": "fatigue cracks",
      "gain": "補金屬疲勞而外形可仍保留的生命週期，不把可重用寫成永久不需更換。",
      "prompt": "Close-up at an equipment desk, one anonymous adult inspecting a fine crack in a plain metal piton, soft lamp light from the right.",
      "camera": "tilt down",
      "id": "c09le011",
      "scene": "c09le-shot-011"
    },
    {
      "after": "c09r061",
      "text": "後來的採訪把這段教學寫得更具體：它有十四頁，談楔塊怎麼搭配，不只列商品和價格。",
      "source": "S4",
      "paras": [
        "010"
      ],
      "quote": "fourteen-page",
      "gain": "補教學篇幅及其功能，具體回答只看前言是否足夠。",
      "prompt": "Medium shot at a reading table, one anonymous adult opening a thick blank booklet beside a plain metal wedge, mild window light.",
      "camera": "pan right",
      "id": "c09le012",
      "scene": "c09le-shot-012"
    },
    {
      "after": "c09r061",
      "text": "報導提到，有時要組合不只一個楔塊，還要把幾個支點連起來；讀者得重新理解器材和岩縫的配合。",
      "source": "S4",
      "paras": [
        "010"
      ],
      "quote": "two or more",
      "gain": "補教學內容涉及組合楔塊與相連支點，而非把換工具化約為換購物清單。",
      "prompt": "Close-up at a plain demonstration board, one anonymous adult arranging two small metal wedges beside connected rope loops, soft overhead light.",
      "camera": "pull back",
      "id": "c09le013",
      "scene": "c09le-shot-013"
    },
    {
      "after": "c09r061",
      "text": "同篇採訪裡，他估計，投入攀岩的人在普通人工攀登約帶二十個不同尺寸、形狀的楔塊；大岩壁可能要六十個。",
      "source": "S4",
      "paras": [
        "009"
      ],
      "quote": "twenty chocks",
      "gain": "補當事人對普通人工攀登與大岩壁攜帶量的估計，限定歷史受訪說法而非現代裝備清單。",
      "prompt": "Medium shot at an equipment table, one anonymous adult choosing among several plain metal wedges beside an open unmarked bag, soft window light from the left.",
      "camera": "tilt up",
      "id": "c09le014",
      "scene": "c09le-shot-014"
    },
    {
      "after": "c09r074",
      "text": "反彈不只來自年輕人。書評還引述一份在東岸廣為流傳、由年長攀岩者寫的文字，嫌型錄裡有「買不起的器材」和「不需要的說教」。",
      "source": "S3",
      "paras": [
        "007"
      ],
      "quote": "equipment you can’t afford and sermons you don’t need",
      "gain": "補年長攀岩者的具體批評；東岸只限定文字廣為流傳的地點，不指定作者出身；嫌型錄有該器材與說教，不擴為全部。批評仍經書評引述，不作公司自白。",
      "prompt": "Medium shot at a reading desk, one anonymous older adult frowning at a blank equipment booklet, soft window light from the left.",
      "camera": "push in",
      "id": "c09le015",
      "scene": "c09le-shot-015"
    },
    {
      "after": "c09r074",
      "text": "書評也說，有些不滿者仍承認這種倫理在道德上是對的；只是他們覺得，自己的登山自由也被押上了。",
      "source": "S3",
      "paras": [
        "005"
      ],
      "quote": "their freedom as an individual",
      "gain": "補反對者也承認倫理方向但擔心個人自由的矛盾，避免把反彈寫成只想破壞岩石。",
      "prompt": "Close-up at a quiet equipment table, one anonymous adult looking thoughtfully between a plain hammer and a metal wedge, mild side light.",
      "camera": "pan left",
      "id": "c09le016",
      "scene": "c09le-shot-016"
    },
    {
      "after": "c09r089",
      "text": "工廠裡，工人還在調整扣環的活動門和冰斧柄；同一篇報導，讓這枚釘子回到一座處理多種器材的工廠。",
      "source": "S4",
      "paras": [
        "053"
      ],
      "quote": "ice-axe handles",
      "gain": "補工廠可見的活動門與冰斧柄調整，不擅自指定工人在壓床旁，也不從生產推財務動機。",
      "prompt": "Close-up at a factory workbench, one anonymous adult adjusting the gate of a plain metal carabiner, soft lamp light from the left.",
      "camera": "pan right",
      "id": "c09le018",
      "scene": "c09le-shot-018"
    },
    {
      "after": "c09r090",
      "text": "那塊木板裝著不規則木塊，留出不同的縫，讓楔塊能試各種組合；展示的不只是貨品，也是它怎麼工作。",
      "source": "S4",
      "paras": [
        "053"
      ],
      "quote": "wooden blocks",
      "gain": "補示範板製造裂縫與試不同組合的具體設計，使新用法可見。",
      "prompt": "Medium shot beside a plain wooden demonstration board, one anonymous adult fitting a metal wedge between irregular wooden blocks, mild window light.",
      "camera": "pull back",
      "id": "c09le019",
      "scene": "c09le-shot-019"
    },
    {
      "after": "c09r091",
      "text": "報導列出的當時型錄中，不規則六角形楔塊有十四種尺寸，可以換角度卡進岩縫。",
      "source": "S4",
      "paras": [
        "009"
      ],
      "quote": "fourteen sizes",
      "gain": "補報導當時六角楔塊的形狀、角度與尺寸供應，不當成現行規格。",
      "prompt": "Close-up at an equipment counter, one anonymous adult turning a plain irregular hexagonal metal wedge in one hand, soft side light from the right.",
      "camera": "tilt down",
      "id": "c09le020",
      "scene": "c09le-shot-020"
    },
    {
      "after": "c09r091",
      "text": "另一種末端像角錐的楔塊，則列十六種尺寸；少用岩釘的選擇，在後來這份型錄裡，已有不同形狀和大小可買。",
      "source": "S4",
      "paras": [
        "009"
      ],
      "quote": "sixteen sizes",
      "gain": "補另一種楔塊的角錐外形及尺寸供應，把勸告落到顧客面前的替代商品。",
      "prompt": "Medium shot at an equipment counter, one anonymous adult comparing two plain pyramid-ended metal wedges, soft lamp light from the left.",
      "camera": "push in",
      "id": "c09le021",
      "scene": "c09le-shot-021"
    }
  ],
  "changes": {
    "c09r001": {
      "text": "把一枚岩釘放在你手邊。器材文章舉例，一組結繩熟手，一天能放入、取回多達一百枚。",
      "source": "S1",
      "paras": [
        "004"
      ],
      "quote": "100 pitons a day",
      "reason": "第一秒落在觀眾手邊的匿名示意場景，保留一組熟手/一天/多達100枚例示；不指同一枚或同一孔敲100次。"
    },
    "c09r079": {
      "text": "開場那次不帶岩釘的攀登，說的就是這裡：一九七三年，修納德和夥伴帶著楔塊，去爬酋長岩一條著名長路線。",
      "source": "S4",
      "paras": [
        "009"
      ],
      "quote": "in 1973",
      "reason": "親讀S4:009後把相對『同年』澄清為明文1973；其餘伙伴/長路線與未帶岩釘範圍不補未說細節。"
    }
  },
  "loops": [
    {
      "setup": "c09r002",
      "payoff": "c09r034",
      "what": "下一位攀登者會接到什麼岩縫，揭露合金鋼與岩片的機制"
    },
    {
      "setup": "c09r005",
      "payoff": "c09r080",
      "what": "不帶岩釘的一次大岩壁攀登是否完成"
    },
    {
      "setup": "c09r005",
      "payoff": "c09r089",
      "what": "工廠仍在動的機器究竟製什麼"
    },
    {
      "setup": "c09r011",
      "payoff": "c09r012",
      "what": "可重用硬鋼釘從哪裡買到，揭露供應缺口"
    },
    {
      "setup": "c09r016",
      "payoff": "c09r017",
      "what": "手工打出的釘子售價與買家的反應"
    },
    {
      "setup": "c09r025",
      "payoff": "c09r033",
      "what": "工具更順手，為何反而留下岩壁問題"
    },
    {
      "setup": "c09r035",
      "payoff": "c09r037",
      "what": "可重用釘子面對變寬裂縫會怎樣"
    },
    {
      "setup": "c09r052",
      "payoff": "c09le012",
      "what": "讀克制口號後如何選，十四頁教學把用法落實"
    },
    {
      "setup": "c09r064",
      "payoff": "c09r065",
      "what": "器材選擇有差別的具體舊路線對照"
    },
    {
      "setup": "c09r070",
      "payoff": "c09r077",
      "what": "賣器材者的勸告在書評裡如何被回應"
    },
    {
      "setup": "c09r092",
      "payoff": "c09r095",
      "what": "服裝與器材關係的當事人說法，不推持續生產的財務動機"
    },
    {
      "setup": "c09r095",
      "payoff": "c09r097",
      "what": "模具成本的當事人回本估算"
    },
    {
      "setup": "c09le003",
      "payoff": "c09le018",
      "what": "扣環從便攜手工銼修走到工廠調整開門的具體製作"
    },
    {
      "setup": "c09r007",
      "payoff": "c09r102",
      "what": "少敲的建議改了什麼，與仍在供應的商品如何並存"
    }
  ],
  "hooks": [
    [
      "c09r001",
      "利害",
      "熟手一天可處理多達100枚岩釘"
    ],
    [
      "c09r004",
      "反常",
      "在自家型錄勸少用"
    ],
    [
      "c09r007",
      "問題",
      "勸少用的商品後來怎麼了"
    ],
    [
      "c09r010",
      "揭露",
      "硬鋼可重用先例不屬修納德"
    ],
    [
      "c09r012",
      "缺口",
      "想買的釘子已不可得"
    ],
    [
      "c09r015",
      "數字",
      "手工一小時只有兩枚"
    ],
    [
      "c09r017",
      "差距",
      "30美分與1.5美元及顧客接受"
    ],
    [
      "c09le004",
      "轉折",
      "不敲入的楔塊從石塊到有孔金屬"
    ],
    [
      "c09r020",
      "反常",
      "價目表警告攀岩季交貨慢"
    ],
    [
      "c09r023",
      "改法",
      "機器和模具回應手工供應不足"
    ],
    [
      "c09r025",
      "未解",
      "更多更順手的工具如何長出代價"
    ],
    [
      "c09le006",
      "角色揭露",
      "岩釘在人工攀登還承接腳梯及吊床"
    ],
    [
      "c09le009",
      "反轉",
      "固定力不只靠猛敲，敲深反而出問題"
    ],
    [
      "c09r030",
      "轉向",
      "人熟練了，岩石承受什麼"
    ],
    [
      "c09r045",
      "矛盾",
      "當事人曾說楔塊平常不能取代岩釘"
    ],
    [
      "c09r033",
      "後果",
      "熱門路線出現成排釘孔"
    ],
    [
      "c09r037",
      "升級",
      "裂縫變寬需要更大釘子"
    ],
    [
      "c09r046",
      "轉念",
      "當事人曾以為攀岩不傷岩，發現後把選擇寫在哪裡"
    ],
    [
      "c09r048",
      "選擇",
      "合適路線優先可拆楔塊"
    ],
    [
      "c09r051",
      "反常",
      "賣家請顧客想這一下要不要敲"
    ],
    [
      "c09r056",
      "例外",
      "必要固定岩釘後資訊怎麼留給後人"
    ],
    [
      "c09le012",
      "落地",
      "勸告旁還有十四頁具體用法"
    ],
    [
      "c09r064",
      "證據問題",
      "改器材是否真有差別，作者用什麼讓顧客相信"
    ],
    [
      "c09r065",
      "對照",
      "踩亮的落腳處與仍完整的保護縫"
    ],
    [
      "c09r071",
      "衝突",
      "書評記下說一套做一套的指責"
    ],
    [
      "c09le015",
      "擴大",
      "年長攀岩者也嫌器材價格與說教"
    ],
    [
      "c09r076",
      "反證",
      "書評作者遇到更多不帶錘子的攀登者"
    ],
    [
      "c09r080",
      "結果",
      "一次不帶岩釘的攀登完成"
    ],
    [
      "c09r085",
      "場景",
      "刊出報導記下店裡舊釘子展示"
    ],
    [
      "c09r089",
      "揭曉",
      "壓床繼續製出新岩釘"
    ],
    [
      "c09le020",
      "具體商品",
      "替代楔塊有不同形狀角度與尺寸"
    ],
    [
      "c09r097",
      "數字",
      "當事人估模具五到十年回本"
    ],
    [
      "c09r102",
      "答案",
      "改優先次序，商品仍在"
    ]
  ],
  "source_reads": {
    "S1": [
      "004",
      "009",
      "013",
      "014",
      "016",
      "018",
      "019",
      "021",
      "049"
    ],
    "S2": [
      "025",
      "026",
      "027",
      "028",
      "029",
      "030",
      "031",
      "032",
      "033",
      "034",
      "035",
      "036"
    ],
    "S3": [
      "001",
      "002",
      "003",
      "004",
      "005",
      "006",
      "007",
      "008",
      "009"
    ],
    "S4": [
      "002",
      "003",
      "006",
      "007",
      "008",
      "009",
      "010",
      "028",
      "031",
      "033",
      "035",
      "037",
      "045",
      "046",
      "050",
      "051",
      "053",
      "054",
      "055"
    ],
    "S7": [
      "072"
    ]
  },
  "source_labels": {
    "S1": "1967當事人器材文章",
    "S2": "1972前言全文重刊，現代編按與原前言分開",
    "S3": "1973同期型錄書評",
    "S4": "1977刊出採訪；到訪日期未確認",
    "S7": "2012品牌回顧，僅沿用1973服裝標籤時序"
  },
  "brief": "# C09 長度增補候選 r2｜一枚岩釘的角色\n\n狀態：r2作者候選，待來源差分審查與兩位全新隔離讀者；不是新核准。原 current、canonical、舊核准與全部譯文保留。\n\n## 唯一方案 A\n\n主角是一枚示意岩釘：從鍛造、裝進器材袋、放入與取回岩縫，走到型錄中的使用選擇，再走進記者所見的工廠。它是敘事視點，不宣稱同一件歷史實物曾經跨越全部年代。\n\n問題：賣岩釘的人為什麼在1972年的型錄勸你少敲，而後來工廠裡仍有新岩釘做出來？\n\n一句答案：前言改的是使用的優先次序，在適合路線先選可拆楔塊、必要情況仍留例外；後來報導所見，岩釘並未只剩展品，仍在製造。\n\n站主觀點：品牌的反常勸告，要和工具怎麼做、怎麼用、給下一位攀登者留下什麼一起看，讓觀眾自己判斷賣家的勸告。\n\n## 增補如何推進同一條線\n\n新料依序增加：軟鐵貼合與鉻鉬鋼手工、扣環銼修與手鑽、英國楔塊前史、單手取掛與敲入/回收取捨、金屬疲勞、十四頁教學及組合支點、年長者的社群反彈、工廠工作與不同楔塊的展示。具體製造和使用動作帶出選擇，沒有加新的預告問句。\n\n保留原95 IDs，僅001為第一秒具體場景微調，079把『同年』澄清為S4:009明寫的1973；新增內容使用c09le前綴。每個改字與新增行的來源、段落、摘句和有效信息列在claims.json與author-notes.json。\n\n## r1 → r2 的唯一內容差分\n\n採用來源審查者對c09le015的完整建議句：東岸只限定文字流傳地，移除「盡是」，保留年長作者與書評引述。刪除c09le017及其鏡頭，讓舊岩釘展品直接接回存貨或新製造的疑問；不以另一份商品清單補字數。其餘114句及保留鏡頭資料保持原樣，原95 IDs及兩處基底微調不變。14個回收端點不變，按新文本重新計算位置。\n\nr1兩位讀者共同的必題否定只指向le017離題；Reader B另對one_line單獨作否定，這不是共同HOLD條件。本次不為追求一致答案另改主線；新讀者仍可獨立判斷。r1原始報告保留在history/r1，任何舊結果都不作r2批准。\n\n## 視聽製作規劃\n\nlook精確為cute-mystery；新增景均匿名英文概念prompt，一人一動作，still配緩慢運鏡，不用品牌、人名、logo、可讀文字或額外style。舊景不當史料重建。正文插圖規劃時間遠高於70%，本候選沒有新增文字卡；卡片總量不超過三張。\n\n繁中燒錄字幕及可關閉CC並存。開場濃縮後才放5秒頻道片頭；敘事結束後接21秒v4片尾。兩者不補正文units。縮圖沿用bold layout d。這些只是規劃，沒有製作SRT、TTS、圖片或媒體。\n\n## 來源界線\n\n1972是型錄原前言，重刊頁的現代編按不混入當年原話；1973書評的指責、評論者觀察及判斷都保留歸屬。1977只表示文章刊出，不表示已確認的到訪日。服裝補貼器材及模具回本只沿用受訪者說法，不作獨立財報，也不推導繼續製釘的財務動機。1973那次攀登只是不帶岩釘，仍非不帶繩索或其他裝備，更不替所有路線作保。\n\n## 後續\n\n本候選等待獨立來源核對及兩位新隔離讀者後，才由根代理決定是否採用；任何舊批准都不自動覆蓋這份增補。沒有付費呼叫、後台寫入或媒體長度宣稱。\n"
}
''')
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]")
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]")

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def units(text):
    return sum(1 if CJK.fullmatch(t) else 2 for t in TOKEN.findall(text))

def save_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def cache_evidence(source, numbers, phrase=None):
    path = CACHE / (source + ".paragraphs.txt")
    paragraphs = {line[:3]: line[4:] for line in path.read_text().splitlines() if line[:3].isdigit()}
    evidence = []
    for number in numbers:
        text = paragraphs[number]
        evidence.append({"source": source, "cache_path": str(path), "cache_sha256": sha(path), "paragraph": number,
                         "paragraph_sha256": hashlib.sha256(text.encode()).hexdigest()})
    if phrase and not any(phrase in paragraphs[number] for number in numbers):
        raise ValueError("Source anchor phrase absent: " + source + ":" + repr(phrase))
    return evidence

if sha(BASE / "video.json") != EXPECTED_BASE_SHA:
    raise ValueError("Base changed; stop without adopting another current")
base = json.loads((BASE / "video.json").read_text())
base_claims = json.loads((BASE / "claims.json").read_text())
doc = copy.deepcopy(base)
doc["look"] = {"preset": "cute-mystery"}
doc["subtitles"]["burn_in"] = True
doc["thumbnail"]["data"]["layout"] = "d"
doc["loops"] = DATA["loops"]
original_lines = {l["id"]: l["text"] for s in base["scenes"] for l in s.get("lines", [])}
base_claim_map = {r["id"]: r for r in base_claims}
addition_map = {}
for row in DATA["additions"]:
    addition_map.setdefault(row["after"], []).append(row)
scenes = []
for old_scene in doc["scenes"]:
    for line in old_scene.get("lines", []):
        if line["id"] in DATA["changes"]:
            line["text"] = DATA["changes"][line["id"]]["text"]
    scenes.append(old_scene)
    for line in old_scene.get("lines", []):
        for row in addition_map.get(line["id"], []):
            scenes.append({"id": row["scene"], "template": "shot",
                           "data": {"prompt": row["prompt"], "visual": "still", "camera": row["camera"]},
                           "lines": [{"id": row["id"], "text": row["text"]}]})
doc["scenes"] = scenes
flat = [(s, l) for s in scenes for l in s.get("lines", [])]
line_map = {l["id"]: l for s, l in flat}
if not all(k in line_map for k in original_lines):
    raise ValueError("An original line ID was lost")
if len(line_map) != len(flat):
    raise ValueError("Duplicate line ID")
changed = [k for k in original_lines if line_map[k]["text"] != original_lines[k]]
if set(changed) != set(DATA["changes"]):
    raise ValueError("Unlisted retained narration edit")
camera_adjustments = []
cameras = ["push in", "pan left", "pull back", "pan right", "tilt up", "tilt down", "hold"]
for i in range(2, len(scenes)):
    triplet = scenes[i-2:i+1]
    if all(s["template"] == "shot" for s in triplet) and len({s["data"].get("camera") for s in triplet}) == 1:
        selected = next((s for s in reversed(triplet) if s["id"].startswith("c09le-")), None)
        if selected is not None:
            before = selected["data"]["camera"]
            selected["data"]["camera"] = next(c for c in cameras if c != before)
            camera_adjustments.append({"scene": selected["id"], "before": before, "after": selected["data"]["camera"]})

chapter_label = ""
chapter_key = "hook"
projection = []
claims = []
addition_by_id = {r["id"]: r for r in DATA["additions"]}
for scene, line in flat:
    if scene.get("chapter"):
        chapter_label = scene["chapter"]
    projection.append({"chapter": chapter_label, "id": line["id"], "text": line["text"]})
    if line["id"] in base_claim_map:
        row = copy.deepcopy(base_claim_map[line["id"]])
        chapter_key = row["chapter"]
        row["text"] = line["text"]
        row["status"] = "PENDING_INDEPENDENT_REVIEW"
        row["candidate_basis"] = "retained_base_text" if line["id"] not in DATA["changes"] else "declared_retained_text_delta"
        if line["id"] in DATA["changes"]:
            change = DATA["changes"][line["id"]]
            row["source"] = change["source"]
            row["anchor"] = change["reason"]
            row["candidate_evidence"] = cache_evidence(change["source"], change["paras"], change["quote"])
            row["short_anchor_phrase"] = change["quote"]
        claims.append(row)
    else:
        added = addition_by_id[line["id"]]
        claims.append({"id": line["id"], "chapter": chapter_key, "text": line["text"], "source": added["source"],
                       "anchor": added["gain"], "status": "PENDING_INDEPENDENT_REVIEW",
                       "candidate_basis": "sourced_expansion_with_narrative_connection",
                       "short_anchor_phrase": added["quote"],
                       "candidate_evidence": cache_evidence(added["source"], added["paras"], added["quote"])})

total_units = sum(units(l["text"]) for s, l in flat)
first_chapter_start = next(i for i, s in enumerate(scenes[1:], 1) if s.get("chapter"))
opening_units = sum(units(l["text"]) for s in scenes[:first_chapter_start] for l in s.get("lines", []))
closing_units = sum(units(l["text"]) for s in scenes if s["template"] == "outro" for l in s.get("lines", []))
shot_units = sum(units(l["text"]) for s in scenes if s["template"] == "shot" for l in s.get("lines", []))
added_units = sum(units(r["text"]) for r in DATA["additions"])
body_units = total_units - opening_units
strict_body_units = body_units - closing_units
if not 3300 <= body_units <= 3550:
    raise ValueError("Author target units outside requested window: " + str(body_units))
# The assigned target uses body_after_opening. The stricter count is disclosed;
# r2 removes a detour without adding filler for its small gap below 3300.
cumulative = 0
ends = {}
chapter_inventory = []
for scene in scenes:
    if scene.get("chapter"):
        chapter_inventory.append({"scene": scene["id"], "chapter": scene["chapter"], "units": 0, "you": 0, "i": 0})
    for line in scene.get("lines", []):
        cumulative += units(line["text"])
        ends[line["id"]] = cumulative
        chapter_inventory[-1]["units"] += units(line["text"])
        chapter_inventory[-1]["you"] += line["text"].count("你")
        chapter_inventory[-1]["i"] += line["text"].count("我")
hooks = []
previous = 0
for ident, kind, content in DATA["hooks"]:
    end = ends[ident]
    hooks.append({"id": ident, "kind": kind, "substance": content, "end_spoken_units": end,
                  "gap_from_previous_spoken_units": end-previous, "planned_gap_seconds_at_4_5": round((end-previous)/4.5, 2)})
    previous = end

save_json("video.json", doc)
save_json("narration-only.json", projection)
save_json("claims.json", claims)
script = ["# C09 Patagonia｜長度增補作者候選 r2", "", "狀態：未採用，待來源差分核對與兩位全新隔離讀者；r1報告不作本版批准。", ""]
for scene in scenes:
    if scene.get("chapter"):
        script += ["## " + scene["chapter"], ""]
    for line in scene.get("lines", []):
        row = next(x for x in claims if x["id"] == line["id"])
        script.append("- " + line["id"] + " ｜ " + line["text"] + " ｜ " + row["source"])
(OUT / "script.md").write_text("\n".join(script) + "\n")
claim_md = ["# C09 長度增補候選 r2 來源映射", "", "全部待獨立核對；r1只作修訂證據，本文不延用舊收據為本版作判定。英文短錨點僅存claims.json，本表不重複引文。", "",
            "| ID | 旁白 | 來源／定位 | 作者信息增量或界線 |", "| --- | --- | --- | --- |"]
for row in claims:
    locators = ", ".join(e["source"] + ":" + e["paragraph"] for e in row.get("candidate_evidence", []))
    claim_md.append("| " + row["id"] + " | " + row["text"] + " | " + row["source"] + (" / " + locators if locators else " / 原current映射與source-r12-delta鏈") + " | " + row["anchor"].replace("|", "／") + " |")
(OUT / "claims.md").write_text("\n".join(claim_md) + "\n")
(OUT / "brief.md").write_text(DATA["brief"] + "\n## 作者計數（不是媒體實測）\n\n" + "按spokenUnits公式：新增行 " + str(added_units) + " units；開場 " + str(opening_units) + "；開場後正文 " + str(body_units) + "；再扣敘事收尾為 " + str(strict_body_units) + "。沒有新增停頓或調慢語速。\n")
series = json.loads((BASE / "series.json").read_text())
series["production_status"] = "length_extension_candidate_unapproved"
series["target_minutes"] = 13
save_json("series.json", series)
base_bindings = {name: {"path": str(BASE / name), "sha256": sha(BASE / name)} for name in ["video.json", "script.md", "narration-only.json", "claims.json", "brief.md", "series.json"]}
source_bindings = {}
for source, paragraphs in DATA["source_reads"].items():
    source_bindings[source] = {"label": DATA["source_labels"][source],
                              "paragraph_cache": {"path": str(CACHE/(source+".paragraphs.txt")), "sha256": sha(CACHE/(source+".paragraphs.txt"))},
                              "html_cache": {"path": str(CACHE/(source+".html")), "sha256": sha(CACHE/(source+".html"))},
                              "author_read_paragraphs": paragraphs}
delta = []
for ident, change in DATA["changes"].items():
    delta.append({"id": ident, "before": original_lines[ident], "after": change["text"], "reason": change["reason"],
                  "source": change["source"], "evidence": cache_evidence(change["source"], change["paras"], change["quote"])})
# Author scope guards compare the frozen r1 with this revision; these are not
# independent review or native verify results.
r1_video = json.loads((R1 / "video.json").read_text())
r1_scene_map = {s["id"]: s for s in r1_video["scenes"]}
r2_scene_map = {s["id"]: s for s in doc["scenes"]}
r1_lines = {l["id"]: l["text"] for s in r1_video["scenes"] for l in s.get("lines", [])}
r2_lines = {l["id"]: l["text"] for s in doc["scenes"] for l in s.get("lines", [])}
r1_changed = [k for k in r1_lines if k in r2_lines and r1_lines[k] != r2_lines[k]]
r1_deleted = [k for k in r1_lines if k not in r2_lines]
if r1_changed != ["c09le015"] or r1_deleted != ["c09le017"]:
    raise ValueError("r2 content changes exceeded the two assigned targets")
if [k for k in r1_scene_map if k not in r2_scene_map] != ["c09le-shot-017"]:
    raise ValueError("r2 removed an unlisted scene")
for ident, scene in r2_scene_map.items():
    if ident not in r1_scene_map:
        raise ValueError("r2 added an unlisted scene")
    prior = copy.deepcopy(r1_scene_map[ident])
    if ident == "c09le-shot-015":
        prior["lines"][0]["text"] = r2_lines["c09le015"]
    if prior != scene:
        raise ValueError("r2 changed an unlisted scene field: " + ident)
if {k:v for k,v in r1_video.items() if k != "scenes"} != {k:v for k,v in doc.items() if k != "scenes"}:
    raise ValueError("r2 changed an unlisted video field")
for loop in DATA["loops"]:
    if loop["setup"] not in r2_lines or loop["payoff"] not in r2_lines:
        raise ValueError("A loop endpoint no longer exists")
r1_receipt_paths = ["reviews/source-r1-independent.json", "reviews/narrative-r1-a.raw.json",
                    "reviews/narrative-r1-b.raw.json", "reviews/narrative-r1.json",
                    "reviews/narrative-r1-input.json", "reviews/narrative-r1-binding.json"]
r1_primary = {name: {"path":str(R1/name), "sha256":sha(R1/name)} for name in [
    "video.json", "script.md", "narration-only.json", "claims.json", "claims.md",
    "brief.md", "series.json", "author-notes.json", "build-candidate.py"]}
r1_receipts = [{"path":str(R1/name), "sha256":sha(R1/name)} for name in r1_receipt_paths]
r1_source_receipt = json.loads((R1 / "reviews/source-r1-independent.json").read_text())
for name, expected in r1_source_receipt["input_sha256"].items():
    if sha(R1/name) != expected:
        raise ValueError("Frozen r1 does not match its source receipt: " + name)
revision_delta = {
    "previous_revision": "length-extension-r1",
    "changed_retained_line_ids": r1_changed,
    "deleted_line_ids": r1_deleted,
    "deleted_scene_ids": ["c09le-shot-017"],
    "added_line_ids": [],
    "added_scene_ids": [],
    "retained_line_count": len(r2_lines),
    "retained_line_texts_unchanged": len(r2_lines) - len(r1_changed),
    "retained_scene_data_unchanged": True,
    "other_video_fields_unchanged": True,
    "line_changes": [{"id":"c09le015", "before":r1_lines["c09le015"], "after":r2_lines["c09le015"],
                     "reason":"Exact source-r1 recommendation: circulation location, not writer origin; remove absolute quantifier.",
                     "source":"S3", "evidence":cache_evidence("S3", ["007"], "On the east coast a widely-circulated notice")}],
    "deletions": [{"id":"c09le017", "scene":"c09le-shot-017", "text":r1_lines["c09le017"],
                   "reason":"Both r1 native readers identified this shop merchandise list as the no_detour failure. Delete rather than replace with filler.",
                   "removed_prompt":r1_scene_map["c09le-shot-017"]["data"]["prompt"]}],
    "loop_plan_unchanged_from_r1": doc["loops"] == r1_video["loops"],
    "loop_endpoints_rebound_to_current_text": True,
    "reader_b_one_line_no":"Preserved as a single-reader observation, not rewritten into a shared failure or approval requirement.",
    "r1_receipts_are_revision_evidence_only": True,
    "no_new_approval_claimed": True}
notes = {"status": "HOLD_PENDING_INDEPENDENT_SOURCE_AND_TWO_NEW_ISOLATED_READERS",
         "revision": REVISION,
         "r1_inputs": r1_primary, "r1_review_evidence": r1_receipts, "r1_to_r2_delta": revision_delta,
         "role": "candidate_author_not_reviewer", "created_on_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "base_inputs": base_bindings, "base_source_chain": [{"path":str(BASE/rel),"sha256":sha(BASE/rel)} for rel in [
             "reviews/source-r12-delta.json","history-r11/source-r11-delta.json","history-r10/source-r10-delta.json",
             "history-r9/source-r9-delta.json","history-r8/source-r8-delta.json","history-r7a/source-r7a-delta.json",
             "history-r7/source-r7-delta.json","reviews/source-r6-delta.json","reviews/source-r5-delta.json","reviews/source-r4-delta.json"]],
         "prior_approvals_not_inherited": True, "approved": False, "independent_reviews": [],
         "top_level_delta": {"loops":{"before_count":len(base["loops"]),"after_count":len(doc["loops"]),"basis":"author-curated distinct information payoffs, pending new readers"},
                             "thumbnail.data.layout":{"before":base["thumbnail"]["data"].get("layout"),"after":"d"},
                             "look_and_burn_in":"explicit required values retained"},
         "source_read_log": source_bindings, "narration_line_count": len(flat), "scene_count": len(scenes), "original_line_ids_retained": len(original_lines),
         "unchanged_original_line_texts": len(original_lines)-len(changed), "changed_original_line_texts": delta,
         "added_line_count": len(DATA["additions"]), "added_line_information": [{k:v for k,v in r.items() if k not in ["prompt","camera","quote"]} for r in DATA["additions"]],
         "author_units": {"native_formula_reference": "tools/video/core/timeline.mjs:spokenUnits",
                          "baseline_total": 2802, "baseline_after_opening": 2603,
                          "new_lines_units": added_units, "total": total_units, "opening": opening_units,
                          "body_after_opening": body_units, "closing_narration": closing_units,
                          "body_excluding_opening_and_closing_narration": strict_body_units,
                          "target_definition": "body_after_opening, consistent with assigned baseline2603",
                          "r2_no_padding_for_stricter_count": True,
                          "planned_speech_seconds_at_4_5": round(total_units/4.5,2), "not_measured_media": True},
         "chapter_inventory": chapter_inventory, "substantive_hook_plan": hooks,
         "max_planned_hook_gap_seconds_at_4_5": max(h["planned_gap_seconds_at_4_5"] for h in hooks),
         "tail_after_last_hook_seconds_at_4_5": round((total_units-previous)/4.5,2),
         "loop_plan": DATA["loops"], "unique_loop_payoffs": len(set(x["payoff"] for x in DATA["loops"])),
         "opening_forward_previews": [{"setup":"c09r005","topic":"不帶岩釘的一次攀登","payoff":"c09r080"},
                                      {"setup":"c09r005","topic":"仍在動的工廠機器","payoff":"c09r089"}],
         "visual_plan": {"look": {"preset":"cute-mystery"}, "new_scenes": len(DATA["additions"]), "all_new_scenes_still": True,
                         "illustrated_speech_units": shot_units, "all_narration_units": total_units,
                         "planned_illustration_share_by_speech_time": round(shot_units/total_units,4),
                         "new_cards":0,"total_non_shot_scenes":sum(s["template"]!="shot" for s in scenes),
                         "new_scene_camera_adjustments":camera_adjustments,"thumbnail_layout":"d",
                         "prompts":"anonymous English conceptual still scenes; no brand/person names, logos, readable text or extra style"},
         "planned_bookends": {"intro_at":"after_first_chapter","intro_seconds":5,"intro_after_line":"c09r007",
                              "outro_version":"v4","outro_seconds":21,"not_counted_as_body_units":True},
         "subtitles_plan":{"zh_TW_burn_in":True,"zh_TW_CC":True,"media_not_created":True},
         "source_scope_limits": ["1977 is publication year; visit date remains unconfirmed.",
                                "1973 in c09r079 is directly anchored to S4 paragraph009; no new route or participant detail added.",
                                "S2 modern introduction is separate from the original 1972 foreword.",
                                "S3 criticism and its author's observations remain attributed.",
                                "S3:007 locates circulation on the East Coast, not the older writer; r2 removes the unsupported absolute quantifier.",
                                "Apparel subsidy and die payback remain participant claims, not a motive inferred from factory observations.",
                                "New S4 catalogue sizes and carrying estimates describe that historical account, not current products or a modern equipment checklist."],
         "unused_conflicting_detail":"S3 lists a fifty-cent catalogue while S4 calls it a dollar; no new catalogue-price claim or comparison is used.",
         "paid_calls":0,"backend_writes":0,"provider_calls":0,"verification_pipeline_run":False,
         "actual_timing_verified":False,"actual_media_reviewed":False,"source_review_status":"PENDING",
         "isolated_readers_required":2,"candidate_files":{}}
for name in ["video.json","script.md","narration-only.json","claims.json","claims.md","brief.md","series.json","build-candidate.py"]:
    notes["candidate_files"][name] = sha(OUT/name)
save_json("author-notes.json", notes)
print(json.dumps({"candidate":str(OUT),"lines":len(flat),"scenes":len(scenes),"added_units":added_units,
                  "body_after_opening":body_units,"body_excluding_both":strict_body_units,
                  "max_author_hook_gap_seconds":notes["max_planned_hook_gap_seconds_at_4_5"],
                  "unique_loop_payoffs":notes["unique_loop_payoffs"]},ensure_ascii=False))
