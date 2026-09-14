"""Build original research exercises without calling a model or changing source snapshots."""
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX = HERE / "examples"


def put(name, value):
    p = EX / name
    p.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    p.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def table(name, fields, rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    put(name, out.getvalue())


def build():
    docs = [
        ("S01", "v1", "2026-09-01", "sources/S01-v1.md", "# S01 活動規格 v1\n生效日：2026-09-01。虛構活動。\n## CAP\n參與名額為 24 人。\n## TIME\n活動在 2026-10-03 上午 09:30 開始。"),
        ("S01", "v2", "2026-09-14", "sources/S01-v2.md", "# S01 活動規格 v2\n生效日：2026-09-14；替代 v1。虛構活動。\n## CAP\n參與名額修訂為 30 人，不與舊版相加。\n## TIME\n活動在 2026-10-03 上午 09:30 開始。"),
        ("S02", "v1", "2026-09-01", "sources/S02-v1.md", "# S02 場地\n虛構海風教室，練習用名稱，沒有真實地址。\n## ROOM\n使用 A 教室，椅子可移動。"),
        ("S03", "v1", "2026-09-02", "sources/S03-v1.md", "# S03 人員\n## OWNER\n阿晴負責場地確認；小安負責教材。名額依有效規格，不由本文件另訂。"),
        ("S04", "v1", "2026-09-03", "sources/S04-v1.md", "# S04 設備\n## KIT\n帶自己的筆電；現場提供投影設備。不收集個人帳密。"),
        ("S05", "v1", "2026-09-04", "sources/S05-v1.md", "# S05 報名\n## CONFIRM\n填表後仍需收到確認信才算報名成功。費用與退款資訊未提供。"),
        ("S06", "v1", "2026-09-05", "sources/S06-v1.md", "# S06 編輯紀錄\n## POLICY\n保存每次問題、選用来源與原始回答；來源更新後要另查既有講義是否需重做。".replace("来源", "來源")),
    ]
    registry = []
    for sid, version, date, path, content in docs:
        put("57/" + path, content)
        registry.append({"source_id": sid, "version": version, "effective_on": date, "path": path, "phase1": "yes" if version == "v1" else "no", "phase2": "no" if sid == "S01" and version == "v1" else "yes", "sha256": hashlib.sha256((EX / "57" / path).read_bytes()).hexdigest()})
    table("57/sources-v1-v2.csv", list(registry[0]), registry)
    put("57/update-checklist.md", "# 更新驗收\n\n先以六份 v1 文件建立筆記本。S01 使用 Drive 文件與本機上傳各作一次獨立練習。\n\n- 記錄匯入方式、版本、來源勾選及觀察時間。\n- 問同一題：有效規格有多少名額？來源與章節是什麼？\n- 改 S01 為 v2 後檢查來源檢視器；Drive 依畫面同步，本機檔重新上傳。\n- 預期有效名額為 30，不能把 24 與 30 相加。\n- 保留原回答及既有講義，不推定舊產出已更新；重做後另存版本。\n- 真實操作未完成時標 not_run。\n")
    table("57/update-log.csv", ["mode", "phase", "expected_capacity", "observed", "source_version", "checked_at", "status"], [{"mode": mode, "phase": phase, "expected_capacity": capacity, "status": "not_run"} for mode in ["Drive", "upload"] for phase, capacity in [("v1", 24), ("v2", 30)]])

    evidence_sources = {
        "E1": "# E1 報名公告\n2026-09-01，虛構工作坊。\n## DATE\n預定活動日期為 2026-10-03。\n## CAP\n名額為 24 人。\n## CONFIRM\n收到確認信才算報名成功。\n",
        "E2": "# E2 修訂通知\n2026-09-14，名額正式修訂。\n## CAP\n名額改為 30 人，替代 E1 的 24 人。\n## DATE\n討論也許改到 2026-10-04，尚未決定是否替代原日期。\n",
        "E3": "# E3 工作分工\n2026-09-15，虛構紀錄。\n## OWNER\n小安負責教材；報名表負責人尚未指派。\n## COST\n本紀錄未提供費用或退款資訊。\n",
    }
    for sid, content in evidence_sources.items():
        put(f"58/sources/{sid}.md", content)
    matrix = [
        {"id": "C1", "claim": "有效名額30人", "status": "supported", "source_ids": "E1|E2", "quotes": {"E1": "名額為 24 人。", "E2": "名額改為 30 人，替代 E1 的 24 人。"}, "judgment": "E2 明確替代，只採新值"},
        {"id": "C2", "claim": "活動日期已改10月4日", "status": "conflict", "source_ids": "E1|E2", "quotes": {"E1": "預定活動日期為 2026-10-03。", "E2": "討論也許改到 2026-10-04，尚未決定是否替代原日期。"}, "judgment": "保留10月3日原訂及10月4日提案，需人工確認"},
        {"id": "C3", "claim": "報名表由誰負責", "status": "unknown", "source_ids": "E3", "quotes": {"E3": "報名表負責人尚未指派。"}, "judgment": "不能因小安負責教材就替他指派報名表"},
        {"id": "C4", "claim": "填表是否已完成報名", "status": "supported", "source_ids": "E1", "quotes": {"E1": "收到確認信才算報名成功。"}, "judgment": "需收到確認信，不把填表等於成功"},
        {"id": "C5", "claim": "退款金額", "status": "unknown", "source_ids": "E3", "quotes": {"E3": "本紀錄未提供費用或退款資訊。"}, "judgment": "缺少資料，不生成金額或政策"},
    ]
    table("58/evidence-matrix.csv", list(matrix[0]), [{**row, "quotes": json.dumps(row["quotes"], ensure_ascii=False)} for row in matrix])
    put("58/unknown-questions.md", "# 缺證據問題\n\n- 退款可拿回多少錢？\n- 報名表一定由小安負責嗎？\n- 有沒有餐點與停車位？\n\n最後一題三份文件均未提及。標 unknown，寫已查 E1/E2/E3，引用留空，不能編造不存在的原文。矩陣中的原文是作者參考，不是模型已產生的引用。")
    put("58/prompt.txt", "只用選取的 E1、E2、E3 回答五個問題：有效名額、活動日期、報名表負責人、報名成功條件、退款金額。每項分成主張、來源、原文位置與判斷。明確修訂與未確認提案分開，找不到就寫未知；不要用提问句替代證據。".replace("提问", "提問"))

    chapters = {
        "chapter-1.md": "# 第一章：資料來源與版本\n作者原創短教材，2026-09-14。\n\n## K01\n來源 ID 是用來追蹤同一份資料的固定代號，版本不同仍保留同一 ID。\n\n## K02\n擷取時間是保存資料的時間，發布時間是原作者公布內容的時間，兩者不能互換。\n\n## K03\n明確寫出取代舊值的修訂，才可採新值；較晚出現的提案不必然是定案。\n\n## K04\n日期沒有時刻就保留日期，不自行補上下午五點。\n\n## K05\n相同資料的 v1 與 v2 是不同版本，不是兩筆可相加的觀測。\n\n## K06\n来源更新後，既有摘要需要另行檢查；不要假設它已重新生成。\n".replace("来源", "來源"),
        "chapter-2.md": "# 第二章：主張與證據\n作者原創短教材，2026-09-14。\n\n## K07\n引用存在只證明出處可找，仍需檢查引文是否支持主張。\n\n## K08\n兩份資料尚無法判定哪份生效，保留衝突；沒有足夠資料則標未知。\n\n## K09\n題目的答案要能由指定教材支持，不能加入教材外的規則。\n\n## K10\n若兩個選項都符合題目條件，先修題目再計分，不把疑義算成學習者答錯。\n\n## K11\n完成選擇題不等於能解釋概念，重測時加一句理由並回到來源核對。\n\n## K12\n間隔複習表記錄實際作答日期與結果；預定日期不代表已複習。\n",
    }
    for name, value in chapters.items():
        put("59/" + name, value)
    questions = [
        ("K01", "規格由v1改v2，來源ID要如何處理？", ["保留同一ID並記版本", "完全不記ID", "把版本當兩份活動"], "A"),
        ("K02", "今天下載去年文章，哪個說法正確？", ["文章今天發布", "擷取與發布日期分開", "兩個日期取平均"], "B"),
        ("K03", "新信寫『可能改期，未決定』應怎麼處理？", ["直接採新日期", "刪除舊信", "保留原訂與提案待確認"], "C"),
        ("K04", "來源只有10月3日，期限欄應填？", ["10月3日，不加時刻", "10月3日17時", "10月3日中午"], "A"),
        ("K05", "同一場活動v1名額24、v2改30，應採？", ["54人", "30人，保留更正來源", "27人"], "B"),
        ("K06", "來源更新後，昨天的摘要應？", ["視為自動更新", "刪掉來源", "另外核對是否需重做"], "C"),
        ("K07", "回答附來源連結後，下一步是？", ["檢查引文是否支持主張", "直接認定正確", "只看連結數量"], "A"),
        ("K08", "來源沒有任何餐點資料，應標？", ["免費供餐", "未知", "一定不供餐"], "B"),
        ("K09", "出題時加入教材沒說的規則，應？", ["視為加分題", "讓讀者猜", "剔除或補充核准來源後重出"], "C"),
        ("K10", "單選題兩個選項都合理，應？", ["修题後再計分", "任選一個當標準", "全部算錯"], "A"),
        ("K11", "想確認理解，而不只記答案，重測可加？", ["固定同一選項位置", "一句理由並核對來源", "更大字體"], "B"),
        ("K12", "排在明天複習，現在能記已完成嗎？", ["可以", "按預估分數記錄", "不行，等實際作答後記錄"], "C"),
    ]
    quiz = []
    for i, (concept, question, options, answer) in enumerate(questions, 1):
        chapter = "chapter-1.md" if i <= 6 else "chapter-2.md"
        quote = chapters[chapter].split("## " + concept + "\n", 1)[1].split("\n", 1)[0]
        quiz.append({"id": f"Q{i:02}", "concept": concept, "question": question.replace("修题", "修題"), "A": options[0].replace("修题", "修題"), "B": options[1], "C": options[2], "answer": answer, "source": chapter, "quote": quote})
    table("59/questions.csv", list(quiz[0]), quiz)
    put("59/answer-key.md", "# 作者參考答案，不是 NotebookLM 生成結果\n\n" + "\n\n".join(f"## {q['id']} {q['answer']}｜{q['concept']}\n{q['quote']}\n來源：{q['source']} 的 {q['concept']}。" for q in quiz))
    table("59/study-plan.csv", ["round", "planned_date", "actual_date", "status"], [{"round": str(i), "planned_date": date, "status": "not_run"} for i, date in enumerate(["2026-09-14", "2026-09-16", "2026-09-21"], 1)])
    table("59/error-log.csv", ["question_id", "round", "answer", "reason", "next_date", "status"], [{"question_id": q["id"], "round": "1", "status": "not_run"} for q in quiz])
    put("59/bad-questions.md", "# 三個作者故障題\n\n1.『如何追查來源？A保留ID B保留原文』：兩選項都可能正確，單選條件不足。\n2.『每天複習幾分鐘保證考滿分？』：教材沒有這個保證，超出範圍。\n3.『有引用一定正確，對嗎？答案：對，引用K07』：來源否定此結論。\n\n先剔除或改寫，再由人工核對，不計入十二題的學習分數。")

    paper_rows = [
        {"id": "P1", "title": "Dense Passage Retrieval for Open-Domain Question Answering", "authors": "Vladimir Karpukhin; Barlas Oguz; Sewon Min; Patrick Lewis; Ledell Wu; Sergey Edunov; Danqi Chen; Wen-tau Yih", "year": 2020, "file": "papers/dpr-2020.pdf", "url": "https://aclanthology.org/2020.emnlp-main.550/", "doi": "10.18653/v1/2020.emnlp-main.550", "pages": "6769-6781", "question": "學習雙編碼器能否改善开放領域問答的段落檢索？", "sample": "五個問答資料集；NQ test 3610題（表1）", "method": "以問答資料監督訓練檢索器，對比BM25", "metric": "top-20 retrieval accuracy", "example_result": "NQ：Single DPR 78.4，BM25 59.1（表2）", "locators": "問題與方法：摘要、§2-3；資料：§4表1；結果：§5表2", "limit": "只是指定資料集、語料及訓練設定；檢索命中不等於完整回答正確", "fulltext": "yes"},
        {"id": "P2", "title": "Precise Zero-Shot Dense Retrieval without Relevance Labels", "authors": "Luyu Gao; Xueguang Ma; Jimmy Lin; Jamie Callan", "year": 2023, "file": "papers/hyde-2023.pdf", "url": "https://aclanthology.org/2023.acl-long.99/", "doi": "10.18653/v1/2023.acl-long.99", "pages": "1762-1777", "question": "沒有目標任務相關性標籤時如何改善稠密檢索？", "sample": "TREC DL19/20、BEIR等任务；此教學不彙成一個總樣本數", "method": "HyDE先生成假想文件，再編碼檢索真實語料", "metric": "nDCG@10", "example_result": "DL19：HyDE 61.3，Contriever 44.5（表1）", "locators": "方法：§3.2、PDF第2頁圖1；資料與評估：§4；結果：PDF第6頁表1", "limit": "結果隨任務、生成模型與指標不同；假想文件不是可信引用", "fulltext": "yes"},
        {"id": "P3", "title": "Lost in the Middle: How Language Models Use Long Contexts", "authors": "Nelson F. Liu; Kevin Lin; John Hewitt; Ashwin Paranjape; Michele Bevilacqua; Fabio Petroni; Percy Liang", "year": 2024, "file": "papers/lost-middle-2024.pdf", "url": "https://aclanthology.org/2024.tacl-1.9/", "doi": "10.1162/tacl_a_00638", "pages": "157-173", "question": "相關資訊在長上下文中的位置是否影響作答？", "sample": "多文件問答採2655題NQ-Open子集；另有鍵值檢索任务", "method": "控制相关文件位置與上下文長度，測問答與鍵值查找", "metric": "answer accuracy by position", "example_result": "多個受測模型在中段資訊位置表現下降（圖1與§2-3）", "locators": "研究問題：§1；2655題：PDF第3頁§2.1；位置結果：圖1及§2-3", "limit": "2024論文中的受測模型與資料；不是對2026所有模型的測量", "fulltext": "yes"},
    ]
    for row in paper_rows:
        for k, value in row.items():
            if isinstance(value, str):
                row[k] = value.replace("开放", "開放").replace("任务", "任務").replace("相关", "相關")
        row["sha256"] = hashlib.sha256((EX / "60" / row["file"]).read_bytes()).hexdigest()
        row["license"] = "CC BY 4.0"
        row["license_url"] = "https://creativecommons.org/licenses/by/4.0/"
    table("60/paper-matrix.csv", list(paper_rows[0]), paper_rows)
    put("60/paper-licenses.json", {"checked_on": "2026-09-14", "license_evidence": "https://aclanthology.org/faq/copyright/", "note": "三份均為ACL材料，2016年後依CC BY 4.0；P3首頁亦明載。原PDF未修改；paper-matrix為作者中文摘要及解讀，無作者背書意涵。", "papers": paper_rows})
    put("60/reading-questions.md", "# 逐欄讀文\n\n先確認全文與PDF頁碼，再查研究問題、樣本定義、資料切分、監督訊號、評估指標、基準線及適用限制。表1、表2等是各自論文的編號，不可跨文件共用。\n\n故障：把P1的78.4與P2的61.3直接排序。這兩個數字來自不同任務與量尺，拒絕比較。P3的2655題也不能直接視為所有實驗的總樣本數。\n\n作者矩陣已按原文查閱，NotebookLM生成與逐欄點擊引用尚未操作。")

    facts = [
        ("F01", "活動名", "資料查核入門工作坊"), ("F02", "日期", "2026-10-03"),
        ("F03", "開始", "上午09:30"), ("F04", "長度", "90分鐘"), ("F05", "名額", "12人"),
        ("F06", "講師", "林沐"), ("F07", "準備", "帶自己的筆電"),
        ("F08", "報名條件", "僅於收到確認信後視為報名成功"),
        ("F09", "數字限制", "範例數字不得用於真實採購"),
        ("F10", "練習資料", "只使用合成資料，不輸入個人帳密"),
    ]
    table("61/lesson-facts.csv", ["id", "topic", "fact"], [dict(zip(["id", "topic", "fact"], row, strict=True)) for row in facts])
    put("61/source-lesson.md", "# 原創虛構工作坊教材\n\n2026-09-14 v1。與57、58的活動資料是獨立練習，不能合併人數。\n\n" + "\n\n".join(f"## {sid}\n{topic}：{fact}。" for sid, topic, fact in facts))
    put("61/handout.md", "# 作者參考講義｜非模型輸出\n\n" + "\n\n".join(f"{sid} {topic}：{fact}。" for sid, topic, fact in facts) + "\n\n進行順序：先看原始資料，再寫主張與依據，最後討論未知與修正。")
    put("61/narration-script.md", "# 作者語音／影片參考腳本，不是已生成媒體\n\n" + "\n\n".join(f"{sid}：{fact}。" for sid, _, fact in facts) + "\n\n生成後逐句核對條件，不把此腳本當成實際逐字稿；實際語音與影片檔尚未產生。")
    table("61/consistency-log.csv", ["fact_id", "format", "location", "actual", "judgment", "status"], [{"fact_id": sid, "format": fmt, "status": "not_run"} for sid, _, _ in facts for fmt in ["handout", "audio", "video"]])
    put("61/generation-brief.md", "# 生成前的共同要求\n\n僅使用source-lesson.md；受眾為繁體中文初學者。保留F01–F10，尤其名額、日期、講師與確認信條件。先產生講義，再於Studio分別生成Audio Overview和Video Overview。影片先選可用的Explainer與繁體中文；Cinematic英語限制不可套用到所有格式。\n\n逐項記錄實際格式、語言、生成日期、是否可下載與副檔名；不预填MP3或MP4。沒有模型媒體就保留not_run。\n".replace("预填", "預填"))

    downloaded = json.loads((HERE / "source-downloads.json").read_text(encoding="utf-8"))
    snapshot = next(x for x in downloaded if x["file"].startswith("62/"))
    put("62/snapshot-provenance.json", {**snapshot, "provider": "臺北市政府交通局", "dataset_url": "https://data.nat.gov.tw/dataset/147580", "license": "政府資料開放授權條款-第1版", "license_url": "https://data.gov.tw/license", "purpose": "單次歷史快照的研究練習；不是目前站點可借還保證"})
    put("62/ATTRIBUTION.md", "# 公開資料顯名\n\n臺北市政府交通局，2026，YouBike2.0臺北市公共自行車即時資訊，2026-09-14擷取快照。\n此開放資料依政府資料開放授權條款（Open Government Data License）第1版進行公眾釋出，使用者於遵守條款各項規定之前提下得利用之。\n條款：https://data.gov.tw/license\n資料集：https://data.nat.gov.tw/dataset/147580\n\n原始JSON未修改，程式產生的彙總與報告為Mokaair分析；不代表原機關背書。")
    put("62/metadata-fields.json", {"checked_on": "2026-09-14", "source": "https://data.nat.gov.tw/dataset/147580", "declared": ["sno", "sna", "tot", "sbi", "sarea", "mday", "lat", "lng", "ar", "sareaen", "snaen", "aren", "bemp", "act", "srcUpdateTime", "updateTime", "infoTime", "infoDate"], "metadata_updated": "2025-05-12 22:28"})
    put("62/research-brief.md", "# 研究問題\n\n2026-09-14擷取的臺北YouBike即時資料，能支持哪些站點與資料品質描述？哪些內容不能由單次快照回答？\n\n只用公開來源；區分擷取時間、各站infoTime與詮釋資料更新時間。不查個人行程、不推論年度使用量、不排名行政區服務優劣。\n\n先用Deep Research檢視問題與研究計畫，再逐一核對原始資料；必要快照與官方欄位清單加入Notebook。保留實際模型報告與作者參考報告兩套版本。\n\n交付：來源清單、快照、程式彙總、主張依據、至少三個未解問題與更新待辦。")
    table("62/source-register.csv", ["id", "title", "url", "local_file", "checked_on", "kind"], [
        {"id": "T1", "title": "官方資料集詮釋資料", "url": "https://data.nat.gov.tw/dataset/147580", "local_file": "metadata-fields.json", "checked_on": "2026-09-14", "kind": "作者摘錄欄位清單"},
        {"id": "T2", "title": "即時站點JSON的一次快照", "url": snapshot["url"], "local_file": "youbike-snapshot.json", "checked_on": "2026-09-14", "kind": "官方原始位元組"},
        {"id": "T3", "title": "政府資料開放授權條款", "url": "https://data.gov.tw/license", "local_file": "ATTRIBUTION.md", "checked_on": "2026-09-14", "kind": "顯名與授權連結"},
    ])
    license_text = (HERE.parent / "work/examples/51/LICENSE.txt").read_text(encoding="utf-8")
    for n in range(57, 63):
        put(f"{n}/LICENSE.txt", license_text)
        put(f"{n}/README.md", f"# 第 {n} 篇練習\n\n作者原創教材與程式依MIT；60/papers下三篇PDF另依CC BY 4.0及paper-licenses.json；62公開資料另依ATTRIBUTION.md。\n\n模型回答、真實引用點擊、Drive同步及媒體生成尚未執行；not_run是待填的實測表，不是成功結果。解壓後按文章操作，Python檢查器位於壓縮包根目錄research_checks.py。\n")


def package():
    checker = EX / "research_checks.py"
    groups = [(f"lesson-{n}.zip", [p for p in (EX / str(n)).rglob("*") if p.is_file()] + [checker], EX) for n in range(57, 63)]
    groups.append(("research-verification.zip", [p for n in range(57, 63) for p in (EX / str(n)).rglob("*") if p.is_file()] + [checker, HERE / "verification/test_materials.py", HERE / "verification/README.md"], HERE))
    for name, files, base in groups:
        with zipfile.ZipFile(EX / name, "w", zipfile.ZIP_DEFLATED) as archive:
            for p in sorted(files):
                if "__pycache__" in p.parts:
                    continue
                info = zipfile.ZipInfo(p.relative_to(base).as_posix(), (2026, 9, 14, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, p.read_bytes())


if __name__ == "__main__":
    build()
    package()
