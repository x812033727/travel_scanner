from pathlib import Path
import copy, hashlib, json, re, datetime, subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
CACHE = Path("/workspace/work/brand-story-20261025/c09-audit/source-cache")
EXPECTED_BASE_SHA = "875eaca7ba51de28a9e2a198dfd8070325aabec91b58bb7cb903731415fb233a"
REVISION = "length-extension-r3"
R1 = OUT / "history" / "r1"
R2 = OUT / "history" / "r2"
REPO = BASE.parents[3]
CANONICAL_ROOT = Path("/workspace/work/brand-story-20261025/submission-root")
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
      "text": "反彈不只來自年輕人。書評還引述一份在東岸廣為流傳、由年長攀岩者寫的文字。",
      "source": "S3",
      "paras": [
        "007"
      ],
      "quote": "On the east coast a widely-circulated notice written by an older climber",
      "gain": "保留書評引述、年長作者與東岸流傳地；本句只交代批評的歸屬，下一句承接原有批評，不增加作者地緣或絕對量詞。",
      "prompt": "Medium shot at a reading desk, one anonymous older adult frowning at a blank equipment booklet, soft window light from the left.",
      "camera": "push in",
      "id": "c09le015",
      "scene": "c09le-shot-015"
    },
    {
      "after": "c09r074",
      "text": "那位作者嫌型錄裡有「買不起的器材」和「不需要的說教」。",
      "source": "S3",
      "paras": [
        "007"
      ],
      "quote": "equipment you can’t afford and sermons you don’t need",
      "gain": "承接c09le015已交代的年長作者，保留原批評內容與書評歸屬；由r2單景拆出以符合12秒分鏡上限，沒有新增史實。",
      "prompt": "Close-up at a reading desk, one anonymous older adult pointing at a blank equipment booklet beside a closed coin purse, gentle window light from the right.",
      "camera": "pull back",
      "id": "c09le022",
      "scene": "c09le-shot-022",
      "split_from": "c09le015"
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
      "c09le022",
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
  "brief": "# C09 長度增補候選 r3｜一枚岩釘的角色\n\n狀態：r3作者候選，待新來源差分審查與兩位全新隔離讀者；不是新核准。原 current、canonical、舊核准與全部譯文保留。\n\n## 本次建議\n\n### 選項 A：一枚岩釘的角色\n\n主角是一枚示意岩釘：從鍛造、裝進器材袋、放入與取回岩縫，走到型錄中的使用選擇，再走進記者所見的工廠。它是敘事視點，不宣稱同一件歷史實物曾經跨越全部年代。\n\n## 問題\n\n賣岩釘的人為什麼在1972年的型錄勸你少敲，而後來工廠裡仍有新岩釘做出來？\n\n## 一句答案\n\n前言改的是使用的優先次序，在適合路線先選可拆楔塊、必要情況仍留例外；後來報導所見，岩釘並未只剩展品，仍在製造。\n\n## 站主觀點\n\n品牌的反常勸告，要和工具怎麼做、怎麼用、給下一位攀登者留下什麼一起看，讓觀眾自己判斷賣家的勸告。\n\n## 增補如何推進同一條線\n\n新料依序增加：軟鐵貼合與鉻鉬鋼手工、扣環銼修與手鑽、英國楔塊前史、單手取掛與敲入/回收取捨、金屬疲勞、十四頁教學及組合支點、年長者的社群反彈、工廠工作與不同楔塊的展示。具體製造和使用動作帶出選擇，沒有加新的預告問句。\n\n保留原95 IDs，僅001為第一秒具體場景微調，079把『同年』澄清為S4:009明寫的1973；新增內容使用c09le前綴。每個改字與新增行的來源、段落、摘句和有效信息列在claims.json與author-notes.json。\n\n## r1 → r2 的唯一內容差分\n\n採用來源審查者對c09le015的完整建議句：東岸只限定文字流傳地，移除「盡是」，保留年長作者與書評引述。刪除c09le017及其鏡頭，讓舊岩釘展品直接接回存貨或新製造的疑問；不以另一份商品清單補字數。其餘114句及保留鏡頭資料保持原樣，原95 IDs及兩處基底微調不變。14個回收端點不變，按新文本重新計算位置。\n\nr1兩位讀者共同的必題否定只指向le017離題；Reader B另對one_line單獨作否定，這不是共同HOLD條件。本次不為追求一致答案另改主線；新讀者仍可獨立判斷。r1原始報告保留在history/r1，任何舊結果都不作r2批准。\n\n## r2 → r3 機械修訂\n\n本版只把問題、一句答案、站主觀點改為原生解析器讀取的獨立二級標題，並保留唯一的選項A。c09le015保留書評、年長作者與東岸流傳的歸屬；新增c09le022接續同一批評，兩個短句配兩景，沒有加快語速、加入停頓或新增史實。r2其餘114句、全部原鏡頭資料與14個回收端點保持不變；批評的實質鉤子定位改綁c09le022。各版讀者的單獨保留意見均不作這次改故事的理由。\n\n原生lint載入已初始化字典的canonical context，再僅以候選doc、brief與series替代；完整結果綁在author-notes.json。lint只處理機械條件，不代替來源、讀者或owner批准。\n\n## 視聽製作規劃\n\nlook精確為cute-mystery；新增景均匿名英文概念prompt，一人一動作，still配緩慢運鏡，不用品牌、人名、logo、可讀文字或額外style。舊景不當史料重建。正文插圖規劃時間遠高於70%，本候選沒有新增文字卡；卡片總量不超過三張。\n\n繁中燒錄字幕及可關閉CC並存。開場濃縮後才放5秒頻道片頭；敘事結束後接21秒v4片尾。兩者不補正文units。縮圖沿用bold layout d。這些只是規劃，沒有製作SRT、TTS、圖片或媒體。\n\n## 來源界線\n\n1972是型錄原前言，重刊頁的現代編按不混入當年原話；1973書評的指責、評論者觀察及判斷都保留歸屬。1977只表示文章刊出，不表示已確認的到訪日。服裝補貼器材及模具回本只沿用受訪者說法，不作獨立財報，也不推導繼續製釘的財務動機。1973那次攀登只是不帶岩釘，仍非不帶繩索或其他裝備，更不替所有路線作保。\n\n## 後續\n\n本候選等待獨立來源核對及兩位新隔離讀者後，才由根代理決定是否採用；任何舊批准都不自動覆蓋這份增補。沒有付費呼叫、後台寫入或媒體長度宣稱。\n"
}
''')
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]")
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]")

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def units(text):
    return sum(1 if CJK.fullmatch(t) else 2 for t in TOKEN.findall(text))

def spoken(line):
    return line.get("say", line["text"])

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

total_units = sum(units(spoken(l)) for s, l in flat)
first_chapter_start = next(i for i, s in enumerate(scenes[1:], 1) if s.get("chapter"))
opening_units = sum(units(spoken(l)) for s in scenes[:first_chapter_start] for l in s.get("lines", []))
closing_units = sum(units(spoken(l)) for s in scenes if s["template"] == "outro" for l in s.get("lines", []))
shot_units = sum(units(spoken(l)) for s in scenes if s["template"] == "shot" for l in s.get("lines", []))
added_units = sum(units(r["text"]) for r in DATA["additions"])
body_units = total_units - opening_units
strict_body_units = body_units - closing_units
if not 3300 <= body_units <= 3550:
    raise ValueError("Author target units outside requested window: " + str(body_units))
# The assigned target uses body_after_opening. The stricter count is disclosed;
# r2 removed a detour; r3 only splits a shot and does not add filler.
cumulative = 0
ends = {}
chapter_inventory = []
for scene in scenes:
    if scene.get("chapter"):
        chapter_inventory.append({"scene": scene["id"], "chapter": scene["chapter"], "units": 0, "you": 0, "i": 0})
    for line in scene.get("lines", []):
        cumulative += units(spoken(line))
        ends[line["id"]] = cumulative
        chapter_inventory[-1]["units"] += units(spoken(line))
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
script = ["# C09 Patagonia｜長度增補作者候選 r3", "", "狀態：未採用，待新來源差分核對與兩位全新隔離讀者；舊報告不作本版批准。", ""]
for scene in scenes:
    if scene.get("chapter"):
        script += ["## " + scene["chapter"], ""]
    for line in scene.get("lines", []):
        row = next(x for x in claims if x["id"] == line["id"])
        script.append("- " + line["id"] + " ｜ " + line["text"] + " ｜ " + row["source"])
(OUT / "script.md").write_text("\n".join(script) + "\n")
claim_md = ["# C09 長度增補候選 r3 來源映射", "", "全部待獨立核對；舊版只作修訂證據，本文不延用舊收據為本版作判定。英文短錨點僅存claims.json，本表不重複引文。", "",
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
# Author scope guards compare the frozen r2 with this mechanical revision.
# These are not independent review or a native verify invocation.
r2_video = json.loads((R2 / "video.json").read_text())
r2_scene_map = {s["id"]: s for s in r2_video["scenes"]}
r3_scene_map = {s["id"]: s for s in doc["scenes"]}
r2_lines = {l["id"]: l["text"] for s in r2_video["scenes"] for l in s.get("lines", [])}
r3_lines = {l["id"]: l["text"] for s in doc["scenes"] for l in s.get("lines", [])}
r2_changed = [k for k in r2_lines if k in r3_lines and r2_lines[k] != r3_lines[k]]
r2_deleted = [k for k in r2_lines if k not in r3_lines]
r3_added = [k for k in r3_lines if k not in r2_lines]
if r2_changed != ["c09le015"] or r2_deleted or r3_added != ["c09le022"]:
    raise ValueError("r3 content changes exceeded the assigned split")
if [k for k in r3_scene_map if k not in r2_scene_map] != ["c09le-shot-022"]:
    raise ValueError("r3 added an unlisted scene")
if any(k not in r3_scene_map for k in r2_scene_map):
    raise ValueError("r3 removed a retained scene")
for ident, scene in r2_scene_map.items():
    prior = copy.deepcopy(scene)
    if ident == "c09le-shot-015":
        prior["lines"][0]["text"] = r3_lines["c09le015"]
    if prior != r3_scene_map[ident]:
        raise ValueError("r3 changed an unlisted scene field: " + ident)
if {k:v for k,v in r2_video.items() if k != "scenes"} != {k:v for k,v in doc.items() if k != "scenes"}:
    raise ValueError("r3 changed an unlisted video field")
for loop in DATA["loops"]:
    if loop["setup"] not in r3_lines or loop["payoff"] not in r3_lines:
        raise ValueError("A loop endpoint no longer exists")
r2_note = json.loads((R2 / "author-notes.json").read_text())
r1_primary = r2_note["r1_inputs"]
r1_receipts = r2_note["r1_review_evidence"]
revision_delta = r2_note["r1_to_r2_delta"]
r2_primary = {name: {"path":str(R2/name), "sha256":sha(R2/name)} for name in [
    "video.json", "script.md", "narration-only.json", "claims.json", "claims.md",
    "brief.md", "series.json", "author-notes.json", "build-candidate.py"]}
r2_receipt_paths = ["reviews/source-r2-independent.json", "reviews/narrative-r2-a.raw.json",
                    "reviews/narrative-r2-b.raw.json", "reviews/narrative-r2.json",
                    "reviews/narrative-r2-input.json", "reviews/narrative-r2-binding.json",
                    "reviews/canonical-lint-r2.json"]
r2_receipts = [{"path":str(R2/name), "sha256":sha(R2/name)} for name in r2_receipt_paths]
r2_source_receipt = json.loads((R2 / "reviews/source-r2-independent.json").read_text())
for name, expected in r2_source_receipt["input_sha256"].items():
    if sha(R2/name) != expected:
        raise ValueError("Frozen r2 does not match its source receipt: " + name)
r3_delta = {
    "previous_revision":"length-extension-r2", "scope":"four mechanical errors only",
    "changed_retained_line_ids":r2_changed, "deleted_line_ids":r2_deleted,
    "added_line_ids":r3_added, "added_scene_ids":["c09le-shot-022"],
    "deleted_scene_ids":[], "retained_line_texts_unchanged":len(r2_lines)-len(r2_changed),
    "retained_scene_data_unchanged":True, "other_video_fields_unchanged":True,
    "line_split":{"before_id":"c09le015","before_text":r2_lines["c09le015"],
                  "after":[{"id":ident,"text":r3_lines[ident]} for ident in ["c09le015","c09le022"]],
                  "source":"S3", "evidence":cache_evidence("S3", ["007"], "On the east coast a widely-circulated notice"),
                  "reason":"Split the already sourced attribution and complaint into two natural sentences and two still shots; no speed or pause changes.",
                  "new_prompt":r3_scene_map["c09le-shot-022"]["data"]["prompt"]},
    "brief_structure_changes":["## 本次建議 with exactly one ### 選項 A",
                               "non-empty standalone ## 問題", "non-empty standalone ## 一句答案",
                               "non-empty standalone ## 站主觀點"],
    "loop_plan_unchanged_from_r2":doc["loops"]==r2_video["loops"],
    "loop_endpoints_rebound_to_current_text":True,
    "substantive_hook_rebound":{"before":"c09le015","after":"c09le022","reason":"The original criticism now finishes in the split second sentence."},
    "reader_single_no_not_a_story_rewrite_request":True,
    "old_receipts_are_revision_evidence_only":True, "no_new_approval_claimed":True}

# Native, read-only mechanical lint in the actual initialized canonical context.
# Only doc/brief/series are substituted in memory; no source or canonical file is written.
native_code = r"""
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {loadProject, lintProject} from './tools/video/core/state.mjs';
import {spokenText} from './tools/video/core/schema.mjs';
import {spokenUnits, estimateTimeline, FPS, DEFAULT_CPM} from './tools/video/core/timeline.mjs';
const candidate=process.argv[1], root=process.argv[2], slug='story-everyday-patagonia-c09-remake-20261025';
const bytesSha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const valueSha=value=>crypto.createHash('sha256').update(JSON.stringify(value)).digest('hex');
const project=loadProject({root,slug});
const context={root,slug,canonical_file:project.file,canonical_video_sha256:bytesSha(project.file),
  lexicon_initialized_terms:Object.keys(project.lexicon.terms??{}).length,
  initialized_lexicon_sha256:valueSha(project.lexicon),shelf_lexicon_sha256:valueSha(project.shelfLexicon),
  canonical_brief_sha256:bytesSha(path.join(project.dir,'brief.md')),
  canonical_series_sha256:bytesSha(path.join(project.dir,'series.json')),
  preserved_context_fields:['lexicon','shelfLexicon','translations','others','pack','file','dir']};
project.doc=JSON.parse(fs.readFileSync(path.join(candidate,'video.json'),'utf8'));
project.brief=fs.readFileSync(path.join(candidate,'brief.md'),'utf8');
project.series=JSON.parse(fs.readFileSync(path.join(candidate,'series.json'),'utf8'));
const result=lintProject(project),doc=project.doc,flat=doc.scenes.flatMap(s=>s.lines??[]);
const sum=lines=>lines.reduce((n,l)=>n+spokenUnits(spokenText(l)),0);
const firstChapter=doc.scenes.findIndex((s,i)=>i>0&&s.chapter);
const total=sum(flat),opening=sum(doc.scenes.slice(0,firstChapter).flatMap(s=>s.lines??[]));
const closing=sum(doc.scenes.filter(s=>s.template==='outro').flatMap(s=>s.lines??[]));
const timeline=estimateTimeline(doc);
const scene_estimates=timeline.scenes.filter(s=>['c09le-shot-015','c09le-shot-022'].includes(s.id)).map(s=>({
  id:s.id,seconds:(s.end_frame-s.start_frame)/FPS,basis:'native estimated timeline, not actual TTS'}));
const inputs=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','brief.md','series.json'].map(f=>[f,bytesSha(path.join(candidate,f))]));
console.log(JSON.stringify({scope:'local read-only native mechanical lint; not verify or independent approval',
  context_binding:context,candidate_input_sha256:inputs,result,
  native_units:{total,opening,body_after_opening:total-opening,closing_narration:closing,
    body_excluding_opening_and_closing_narration:total-opening-closing,
    added_lines:sum(flat.filter(l=>l.id.startsWith('c09le'))),rule:'spokenUnits(spokenText(line)); existing say overrides included'},
  split_scene_estimates:scene_estimates,default_cpm:DEFAULT_CPM,actual_timing_verified:false}));
"""
native_run = subprocess.run(["node", "--input-type=module", "-e", native_code, str(OUT), str(CANONICAL_ROOT)],
                            cwd=REPO, capture_output=True, text=True, check=True)
native_record = json.loads(native_run.stdout)
if native_record["result"]["errors"]:
    raise ValueError("Native initialized-context lint has errors: " + json.dumps(native_record["result"]["errors"], ensure_ascii=False))
if native_record["native_units"]["total"] != total_units or native_record["native_units"]["body_after_opening"] != body_units:
    raise ValueError("Author units differ from native spokenText units")
notes = {"status": "HOLD_PENDING_INDEPENDENT_SOURCE_AND_TWO_NEW_ISOLATED_READERS",
         "revision": REVISION,
         "r1_inputs": r1_primary, "r1_review_evidence": r1_receipts, "r1_to_r2_delta": revision_delta,
         "r2_inputs": r2_primary, "r2_review_evidence": r2_receipts, "r2_to_r3_delta": r3_delta,
         "native_initialized_context_lint": native_record,
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
                          "baseline_total": sum(units(spoken(l)) for s in base["scenes"] for l in s.get("lines", [])), "baseline_after_opening": 2603,
                          "spoken_text_rule": "existing say overrides included, matching native spokenText",
                          "text_projection_total": sum(units(l["text"]) for s,l in flat),
                          "new_lines_units": added_units, "total": total_units, "opening": opening_units,
                          "body_after_opening": body_units, "closing_narration": closing_units,
                          "body_excluding_opening_and_closing_narration": strict_body_units,
                          "target_definition": "body_after_opening, consistent with assigned baseline2603",
                          "r2_detour_removed_and_no_padding_for_stricter_count": True,
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
         "actual_timing_verified":False,"actual_media_reviewed":False,"source_review_status":"PENDING_NEW_DELTA",
         "isolated_readers_required":2,"candidate_files":{}}
for name in ["video.json","script.md","narration-only.json","claims.json","claims.md","brief.md","series.json","build-candidate.py"]:
    notes["candidate_files"][name] = sha(OUT/name)
save_json("author-notes.json", notes)
print(json.dumps({"candidate":str(OUT),"lines":len(flat),"scenes":len(scenes),"added_units":added_units,
                  "body_after_opening":body_units,"body_excluding_both":strict_body_units,
                  "max_author_hook_gap_seconds":notes["max_planned_hook_gap_seconds_at_4_5"],
                  "unique_loop_payoffs":notes["unique_loop_payoffs"],
                  "native_lint_errors":len(native_record["result"]["errors"]),
                  "native_lint_warnings":len(native_record["result"]["warnings"]),
                  "native_units":native_record["native_units"],
                  "split_scene_estimates":native_record["split_scene_estimates"]},ensure_ascii=False))
