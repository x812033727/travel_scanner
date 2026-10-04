# 原創人工向量：離線執行紀錄

2026-10-04。本檔記錄作者標準函式庫程式的實際輸出，不是模型embedding、模型評測、tokenization、ANN或真實活動。完整六筆DATA在demo.py；查詢向量與全部資料向量是作者直接指定。

Python 3.14.6。程式SHA-256：`75950a028e51828f1b3338f5074fd29a0af523bd745976c7a005542506263a0c`。

Fixture canonical SHA-256：`1104f77855003f038eccf08640ebc728cf8f8e3d7b389af6260846fe40c9e75c`（query、query_toy_vector、top_k、records，UTF-8、排序keys、無多餘空白）。

同一份source與fixture，完整JSON與五種畫面摘錄模式各實跑兩次，所有輸出一致。只用既有Python與標準函式庫，無安裝、模型下載、網路或付費。

以下stdout SHA-256採文字擷取後的UTF-8、LF換行（保留結尾換行）。Windows原始pipe輸出可為CRLF；最後再用Node原始pipe覆跑兩次，完整JSON的CRLF SHA-256均為 `87ed17beb6a02f919cd5974a17e1229e6604ea6e70a6b759e8fd64065e94dd40`，LF正規化後與以下紀錄相同。只正規化換行，沒有改數字、字句或輸出順序。

## 原始JSON輸出，第一次與第二次相同

指令：`python -X utf8 demo.py`，工作目錄為本集source資料夾。

```json
{
  "disclosure": "六筆活動與全部座標均為作者原創的人工玩具示意；不是模型embedding、模型評測、真實活動或真實營業資料。程式只計算已填向量的cosine與明確欄位，不tokenize、不訓練、不聯網、不呼叫模型。",
  "query": "今天想找可直接參加、不用預約的室內手作活動",
  "rank_all": [
    {
      "id": "N001",
      "cosine": 1.0,
      "note": "室內拼貼教室今天休館",
      "condition": "REJECT:closed_today"
    },
    {
      "id": "N002",
      "cosine": 0.9949,
      "note": "陶藝室今天開放，但僅接受已預約者",
      "condition": "REJECT:requires_reservation"
    },
    {
      "id": "N004",
      "cosine": 0.9878,
      "note": "室內木作室免預約，尚無今日開放資料",
      "condition": "UNKNOWN:missing_condition"
    },
    {
      "id": "N003",
      "cosine": 0.9762,
      "note": "社區紙藝桌今天開放，無需預約",
      "condition": "MATCH:explicit_conditions"
    },
    {
      "id": "N005",
      "cosine": 0.3011,
      "note": "河邊寫生活動今天舉行，無需預約",
      "condition": "REJECT:not_indoor"
    },
    {
      "id": "N006",
      "cosine": -0.0995,
      "note": "社區器材維修公告，未記活動開放條件",
      "condition": "UNKNOWN:missing_condition"
    }
  ],
  "top_k_ids": [
    "N001",
    "N002"
  ],
  "eligible_within_top_k": [],
  "eligible_after_checking_all_records": [
    "N003"
  ],
  "metadata_change_same_vector": {
    "cosine_before": 1.0,
    "cosine_after": 1.0,
    "condition_before": "MATCH:explicit_conditions",
    "condition_after": "REJECT:closed_today"
  }
}
```

第一次stdout SHA-256：`5ec2bc9a97b24aacb96a843db6901975d6d5a8af764a8130c07bd4601fc292bd`。第二次：`5ec2bc9a97b24aacb96a843db6901975d6d5a8af764a8130c07bd4601fc292bd`。兩次exit均0，內容逐字相同。

## 正式terminal卡的實際摘錄指令

以下模式只改顯示的摘錄範圍，仍對同一份完整DATA執行run_demo；並非只對其中三筆重新排序。畫面命令沒有使用者名稱、host或私有路徑。

### rank-first

實際指令：`python demo.py rank-first`；兩次exit均0。

```text
TOY: manual vectors; no model
N001 1.0000 REJECT:closed_today
N002 0.9949 REJECT:requires_reservation
N004 0.9878 UNKNOWN:missing_condition
```

第一／二次stdout SHA-256均為 `b422085852633a4310c239c8ef905860f2648085c123960e8b562542c7343a16`；逐字相同。

### rank-last

實際指令：`python demo.py rank-last`；兩次exit均0。

```text
TOY: manual vectors; no model
N003 0.9762 MATCH:explicit_conditions
N005 0.3011 REJECT:not_indoor
N006 -0.0995 UNKNOWN:missing_condition
```

第一／二次stdout SHA-256均為 `329d6ddabba77bac51e405b4d95946df8891603b80c17f683778c8c5acc44cf4`；逐字相同。

### top

實際指令：`python demo.py top`；兩次exit均0。

```text
TOP_K: 2
CANDIDATES: N001 N002
ELIGIBLE: []
```

第一／二次stdout SHA-256均為 `925ad54b70521cf41f79ee9a8b7a719c36e8caedfaa7e2271986314485810d12`；逐字相同。

### all

實際指令：`python demo.py all`；兩次exit均0。

```text
CHECK_SCOPE: ALL_6
ELIGIBLE: ['N003']
UNKNOWN: ['N004', 'N006']
```

第一／二次stdout SHA-256均為 `95847ff605d02368f74671719012b43a875d7965431649b4c30ad24461a3a4a2`；逐字相同。

### control

實際指令：`python demo.py control`；兩次exit均0。

```text
COSINE: 1.0000 -> 1.0000
CONDITION: MATCH -> REJECT
```

第一／二次stdout SHA-256均為 `799a75d37d0f76b2a2a81fc5edbd6a571206f5bbf4739e8dcba9d103865df561`；逐字相同。

## 能證明的事與不能延伸的事

- 精確全量餘弦排序如保存輸出。作者指定只取前兩筆，篩後空；對全六筆檢查條件，保留N003。沒有近似查詢、向量庫或reranker。
- N004、N006的必要資訊不足，保留UNKNOWN；明示排除條件可以拒絕。MATCH只符合虛構欄位，不是現實今天開門的證據。
- 控制對照固定作者向量[1,0]，只改open_today；餘弦相同而條件判定不同。沒有改文字、重新編碼或測模型否定句。
- 餘弦值不是這個程式的正確機率。不能推成所有產品未校準，或所有嵌入模型不能表示條件。
- first disclosure在video.json第一個數字之前；terminal只抄上述實際輸出，資料表每卡最多三列。此紀錄不是影音、音訊或獨立查核關卡。

## Source-only PR whitespace checkpoint

程式只移除檔尾一個空白行；原審稿程式SHA-256是 `71adf5fc12ba94f14ae03adbc17872630023e26f3fc604148c2fcd733b729216`，目前SHA-256是 `75950a028e51828f1b3338f5074fd29a0af523bd745976c7a005542506263a0c`。JSON及五種終端模式各覆跑兩次，12次stdout均與獨立審稿保存輸出逐字相符；沒有改fixture、計算、卡片或旁白。原檔與覆跑收據留在private `<home>/mokaair-work/ai-series-continuation-20261004/`。
