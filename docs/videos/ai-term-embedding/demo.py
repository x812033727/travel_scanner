"""Original manual-vector toy: no embedding model, tokenizer, training, or network."""
import json
import sys
import math

def cosine(a, b):
    if len(a) != len(b): raise ValueError("dimension mismatch")
    aa=math.sqrt(sum(x*x for x in a))
    bb=math.sqrt(sum(x*x for x in b))
    if not aa or not bb: raise ValueError("zero vector")
    return sum(x*y for x,y in zip(a,b))/(aa*bb)

def condition(row):
    fields=("indoor","open_today","needs_reservation")
    if row.get("indoor") is False: return "REJECT:not_indoor"
    if row.get("open_today") is False: return "REJECT:closed_today"
    if row.get("needs_reservation") is True: return "REJECT:requires_reservation"
    if any(row.get(f) is None for f in fields): return "UNKNOWN:missing_condition"
    if row["indoor"] is True and row["open_today"] is True and row["needs_reservation"] is False:
        return "MATCH:explicit_conditions"
    return "UNKNOWN:unsupported_combination"

def run_demo(data):
    query=data["query_toy_vector"]
    ranked=sorted(data["records"],key=lambda r:(-cosine(query,r["toy_vector"]),r["id"]))
    top=ranked[:data["top_k"]]
    checked=[{"id":r["id"],"cosine":round(cosine(query,r["toy_vector"]),4),"note":r["note"],"condition":condition(r)} for r in ranked]
    top_matches=[r["id"] for r in top if condition(r).startswith("MATCH:")]
    all_matches=[r["id"] for r in ranked if condition(r).startswith("MATCH:")]
    positive={"indoor":True,"open_today":True,"needs_reservation":False}
    negative={**positive,"open_today":False}
    return {"disclosure":data["disclosure"],"query":data["query"],"rank_all":checked,"top_k_ids":[r["id"] for r in top],"eligible_within_top_k":top_matches,"eligible_after_checking_all_records":all_matches,"metadata_change_same_vector":{"cosine_before":cosine(query,[1.0,0.0]),"cosine_after":cosine(query,[1.0,0.0]),"condition_before":condition(positive),"condition_after":condition(negative)}}

DATA = json.loads(r'''{
  "name": "社區手作日：先找候選，再看今天能否直接參加",
  "disclosure": "六筆活動與全部座標均為作者原創的人工玩具示意；不是模型embedding、模型評測、真實活動或真實營業資料。程式只計算已填向量的cosine與明確欄位，不tokenize、不訓練、不聯網、不呼叫模型。",
  "query": "今天想找可直接參加、不用預約的室內手作活動",
  "query_toy_vector": [
    1,
    0
  ],
  "top_k": 2,
  "records": [
    {
      "id": "N001",
      "note": "室內拼貼教室今天休館",
      "toy_vector": [
        1,
        0
      ],
      "indoor": true,
      "open_today": false,
      "needs_reservation": false
    },
    {
      "id": "N002",
      "note": "陶藝室今天開放，但僅接受已預約者",
      "toy_vector": [
        0.99,
        0.1
      ],
      "indoor": true,
      "open_today": true,
      "needs_reservation": true
    },
    {
      "id": "N003",
      "note": "社區紙藝桌今天開放，無需預約",
      "toy_vector": [
        0.9,
        0.2
      ],
      "indoor": true,
      "open_today": true,
      "needs_reservation": false
    },
    {
      "id": "N004",
      "note": "室內木作室免預約，尚無今日開放資料",
      "toy_vector": [
        0.95,
        0.15
      ],
      "indoor": true,
      "open_today": null,
      "needs_reservation": false
    },
    {
      "id": "N005",
      "note": "河邊寫生活動今天舉行，無需預約",
      "toy_vector": [
        0.3,
        0.95
      ],
      "indoor": false,
      "open_today": true,
      "needs_reservation": false
    },
    {
      "id": "N006",
      "note": "社區器材維修公告，未記活動開放條件",
      "toy_vector": [
        -0.1,
        1
      ],
      "indoor": null,
      "open_today": null,
      "needs_reservation": null
    }
  ]
}''')

def lines_for(mode, result):
    badge = "TOY: manual vectors; no model"
    ranked = result["rank_all"]
    if mode in ("rank-first", "rank-last"):
        selected = ranked[:3] if mode == "rank-first" else ranked[3:]
        return [badge] + [
            f'{row["id"]} {row["cosine"]:.4f} {row["condition"]}'
            for row in selected
        ]
    if mode == "top":
        return [
            f'TOP_K: {DATA["top_k"]}',
            "CANDIDATES: " + " ".join(result["top_k_ids"]),
            "ELIGIBLE: " + repr(result["eligible_within_top_k"]),
        ]
    if mode == "all":
        unknown = [row["id"] for row in ranked if row["condition"].startswith("UNKNOWN")]
        return [
            "CHECK_SCOPE: ALL_6",
            "ELIGIBLE: " + repr(result["eligible_after_checking_all_records"]),
            "UNKNOWN: " + repr(unknown),
        ]
    if mode == "control":
        control = result["metadata_change_same_vector"]
        before = control["condition_before"].split(":")[0]
        after = control["condition_after"].split(":")[0]
        return [
            f'COSINE: {control["cosine_before"]:.4f} -> {control["cosine_after"]:.4f}',
            f"CONDITION: {before} -> {after}",
        ]
    raise ValueError("Use rank-first, rank-last, top, all, control, or no argument")

if __name__ == "__main__":
    actual = run_demo(DATA)
    if len(sys.argv) == 1:
        print(json.dumps(actual, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines_for(sys.argv[1], actual)))
