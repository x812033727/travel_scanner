"""Original vector reference assets and planning fixtures, never purported model outputs."""
import csv
import html
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX = HERE / "examples"


def put(name, value):
    p = EX / name
    p.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    p.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def table(name, fields, values):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(values)
    put(name, out.getvalue())


def text(x, y, value, size=36, color="#34403c"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(value)}</text>'


def cup(x=640, y=290, color="#71aaa0", second_handle=False):
    body = f'<g transform="translate({x} {y})"><ellipse cx="150" cy="325" rx="225" ry="27" fill="#d3dcd5"/>'
    body += '<path d="M275 65 H320 C420 65 420 250 305 250 H280" fill="none" stroke="#46786e" stroke-width="34"/>'
    if second_handle:
        body += '<path d="M25 65 H-20 C-120 65 -120 250 -5 250 H20" fill="none" stroke="#46786e" stroke-width="34"/>'
    body += f'<path d="M0 20 H300 L275 290 Q270 320 240 320 H60 Q30 320 25 290Z" fill="{color}"/>'
    body += '<ellipse cx="150" cy="20" rx="150" ry="28" fill="#a9d0c8"/><ellipse cx="150" cy="20" rx="128" ry="16" fill="#3f7067"/>'
    body += '<path d="M30 280 H270 L267 300 Q265 315 242 315 H58 Q35 315 33 300Z" fill="#d97b4e"/><circle cx="150" cy="166" r="29" fill="#eaa86f"/></g>'
    return body


def scene(name, title, body, caption="作者繪製參考素材；非 Gemini 或 Flow 生成結果"):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">原創虛構青禾杯設計及教學比較素材。</desc><rect width="1600" height="900" fill="#f7f3e9"/><g font-family="Microsoft JhengHei, sans-serif">{text(85,115,title,58)}{body}{text(85,825,caption,32)}</g></svg>'
    put(name, svg)


def build():
    put("63/style-guide.md", "# 青禾杯 v1｜原創虛構商品\n\n只有一個杯子；薄荷綠杯身 #71aaa0、橘色底圈 #d97b4e、正面單一橘色圓點；一個右側弧形把手；無品牌字樣。杯身正面寬高約300:320，把手不計入杯身寬。平面插畫，不要求擬真材質。\n\n三種用途：白底商品介紹、桌面情境、保留文字區的活動橫幅。每次只改用途與位置，保留主體特徵。參考SVG/PNG為作者繪製，不是模型成品。\n\n評分：數量、外形比例、把手、配色、圓點各0–2分；0不符、1有偏差、2符合。任一核心特徵0分即退回；總分只是作者量尺，不是模型保證。")
    scene("63/references/product.svg", "青禾杯：商品參考", cup())
    scene("63/references/desk.svg", "青禾杯：桌面構圖參考", '<rect x="170" y="610" width="1250" height="70" rx="15" fill="#dfc4a4"/>'+cup(650,270)+'<rect x="270" y="440" width="220" height="155" rx="15" fill="#d8dece"/>')
    scene("63/references/banner.svg", "青禾杯：活動橫幅構圖", cup(1030,290)+text(125,400,"左側保留文案區",56)+text(125,470,"日期與文字後製排版",36))
    scene("63/failure-fixtures/two-handles.svg", "故障練習：多出把手", cup(second_handle=True), "作者刻意製作的故障圖，不是實際模型失敗紀錄")
    scene("63/failure-fixtures/wrong-color.svg", "故障練習：杯身變色", cup(color="#9376aa"), "作者刻意製作的故障圖，不是實際模型失敗紀錄")
    scene("63/failure-fixtures/two-cups.svg", "故障練習：主體數量改變", cup(310,290)+cup(920,290), "作者刻意製作的故障圖，不是實際模型失敗紀錄")
    for name, purpose in [("product", "白底商品介紹"), ("desk", "木桌上的情境圖"), ("banner", "主體放右側、左側保留文案空間的橫幅")]:
        put(f"63/prompts/{name}.txt", f"依上傳的青禾杯原創參考圖製作{purpose}。維持一個杯子、一個右側把手、薄荷綠杯身、橘色底圈和正面一個橘色圓點，無新增字樣。平面插畫，光線由左上。橫向16:9；若模型輸出尺寸不同，保存原檔並記錄，勿把裁切當生成設定。")
    table("63/image-scorecard.csv", ["output_id", "purpose", "file", "count", "shape", "handle", "color", "dot", "reason", "status"], [{"output_id": f"I{i}", "purpose": purpose, "status": "not_run"} for i, purpose in enumerate(["商品圖", "桌面情境", "活動橫幅"], 1)])
    put("63/actual-outputs-needed.md", "# 待完成\n\n三張實際Gemini合格成品、三張實際生成失敗案例、完整提示詞、模型標籤、原始副檔名尺寸與評分。作者參考圖及刻意故障圖不能填補這六張實測要求。")

    baseline = cup()+text(100,700,"青禾杯體驗日 2026-12-03",32)
    scene("64/reference-original.svg", "局部修改原創基準圖", baseline)
    scene("64/manual-text-correction.svg", "作者向量文字補正示範", cup()+text(100,700,"青禾杯體驗日 2026-10-03",32), "直接修改 SVG 文字節點的作者示例；非 Gemini 修圖結果")
    put("64/edit-request.txt", "只把左下角日期2026-12-03改成2026-10-03。保留一個杯子、右側把手、薄荷綠杯身、橘色底圈與正面圓點；背景、杯子位置和比例不變。先做這一項修改，不同時加人物或改光線。")
    table("64/edit-log.csv", ["round", "input", "request", "output", "target_changed", "preserved_regions", "decision", "status"], [{"round": i, "input": "reference-original.png" if i == 1 else "待記錄實際前輪輸入", "request": "日期補正" if i == 1 else "依上一輪結果決定", "status": "not_run"} for i in range(1, 4)])
    put("64/region-check.md", "# 檢查區域\n\n目標區：1600×900畫面左下日期文字，約x=100–620、y=660–720。保留區：杯子外形、右側把手、底圈、圓點、背景。位置是說明需求，不代表Gemini提供像素級遮罩或保證區域外不變。\n\n先看日期全部字元，再比較杯口、輪廓與背景。退化時回原始圖重做。作者向量補正檔示範在可編輯文字圖層處理日期，不宣稱生成模型已成功。")

    shots = [("S1", "開場", "固定鏡頭看見桌上的一個青禾杯", "杯身、右側把手與圓點可辨識"), ("S2", "過程", "鏡頭緩慢向左平移，杯子仍靜止在原處", "沒有多出第二個杯子，動作方向明確"), ("S3", "收尾", "鏡頭停止，杯子在右側，左側留空白給後製字卡", "主體保留，字卡區不被物件遮住")]
    table("65/storyboard.csv", ["shot_id", "role", "action", "acceptance", "desired_seconds", "status"], [{"shot_id": sid, "role": role, "action": action, "acceptance": condition, "desired_seconds": 4, "status": "not_run"} for sid, role, action, condition in shots])
    for sid, role, action, _ in shots:
        scene(f"65/storyboard/{sid}.svg", f"{sid} {role}｜靜態分鏡參考", cup(1030 if sid == "S3" else 640,290)+text(100,720,action,35), "作者分鏡圖；不是影片、擷取影格或模型輸出")
        put(f"65/prompts/{sid}.txt", f"{action}。平面插畫，暖白背景和木桌，左上柔光。單一薄荷綠青禾杯，一個右側把手、橘色底圈和正面圓點。禁止新增人物、文字或第二個杯子。橫向16:9，期望4秒；依所選模型實際支援設定。保留完整實際輸出供核對。")
    capabilities = {"checked_on": "2026-09-14", "source": "https://support.google.com/flow/answer/16352836?hl=en", "models": {"Veo 3.1 Lite": {"frames_first_last": True, "ingredients": True, "ingredients_seconds": [8], "extend": True, "video_edit": False}, "Veo 3.1 Fast": {"frames_first_last": True, "ingredients": True, "ingredients_seconds": [8], "extend": False, "video_edit": False}, "Veo 3.1 Quality": {"frames_first_last": True, "ingredients": False, "ingredients_seconds": [], "extend": False, "video_edit": False}, "Gemini Omni Flash 1.1": {"frames_first_last": True, "ingredients": True, "ingredients_seconds": [4,6,8,10], "extend": False, "video_edit": True}}, "note": "只摘錄本練習需用能力，非完整規格。Omni Extend列coming soon，不能當已提供。Veo Lite延伸限相容Veo 3.1八秒片段。選功能後重查實際模型、比例、秒數、解析度、點數與地區條件。"}
    put("65/model-capabilities.json", capabilities)
    table("65/generation-log.csv", ["shot_id", "attempt", "model", "mode", "resolution", "quoted_credits", "actual_credit_change", "actual_seconds", "output_file", "failure_reason", "status"], [{"shot_id": sid, "attempt": 1, "status": "not_run"} for sid, *_ in shots])
    put("65/editing-handoff.md", "# 合片要求\n\n先檢查三個實際片段，再依開場／過程／收尾排列。Flow有可用場景編輯時使用其畫面操作；若缺該功能，下載原片段，用自己已具備的剪輯工具明示接合。記錄實際工具版本、素材順序、裁切秒數、輸出解析度與格式。\n\n三張分鏡圖不等於三段影片，不把圖片串成動畫冒充Flow實測。只預設無人物、無對白的原創商品練習；仍須聽實際音軌，不能保證沒有多餘音效。")

    scene("66/reference-a-end.svg", "A 結尾：主體在中央", cup(640,290), "作者接點示意圖；不是實際影片擷取影格")
    scene("66/reference-b-bad.svg", "B 開場故障：位置與顏色跳變", cup(970,250,color="#9376aa"), "作者刻意接點故障；非模型失敗案例")
    scene("66/reference-b-target.svg", "B 開場目標：接回相同主體", cup(640,290), "作者接點目標圖；非模型修訂影片")
    put("66/continuity-checklist.md", "# 接點查核\n\n逐項核對A結尾前一秒、最後影格、B第一影格、B開場後一秒，保存實際時間碼。\n\n- 主體數量、把手、配色、圓點與比例\n- 位置、鏡位、光線方向、運動方向\n- 片段長度、聲音突然中斷或音量改變\n\n基準與修訂版本各做一次。分數0不符、1仍有偏差、2符合；每項附位置與理由，不能只挑接點一格。\n\n先核對模型支援，起點影格用真正A片段截圖；若無终點影格能力，就用起點與文字指示，記錄少了何種控制。不把本篇作者示意PNG標為真實A末幀。".replace("终", "終"))
    table("66/continuity-log.csv", ["version", "criterion", "a_time", "b_time", "score", "reason", "status"], [{"version": version, "criterion": criterion, "status": "not_run"} for version in ["baseline", "revised"] for criterion in ["subject", "position", "light", "direction", "sound"]])
    put("66/revision-prompt.txt", "以所附真正A片段的最後影格作為B的起點。保持杯子位置、比例、把手、圓點與左上柔光。B鏡頭緩慢向左平移，杯子不移動、不換色。不要把參考圖中的註解或字卡變成場景文字。記錄實際所用模型與支援的影格模式。")

    brief = {"version": "v1", "fictional": True, "facts": {"F01": "青禾杯體驗日", "F02": "2026-10-03", "F03": "14:00", "F04": "虛構青禾教室", "F05": "僅作教學，不開放真實報名"}}
    put("68/brief-v1.json", brief)
    put("68/brief-v2.json", {**brief, "version": "v2", "facts": {**brief["facts"], "F02": "2026-10-10"}, "change": "僅日期改變，其他事實不變"})
    put("68/brief.md", "# 原創虛構活動交付規格\n\n依brief-v1.json，為青禾杯體驗日製作一篇短文、三張圖片與一支三鏡頭短片。商品圖可不含日期；活動橫幅與邀請圖有日期；影片收尾字卡有日期。精確字卡後製排版，保留可編輯來源。\n\nv2只將日期由2026-10-03改為2026-10-10，找出每個使用F02的成品。原活動是假想情境，不新增真實報名連結。")
    put("68/article-reference.md", "# 青禾杯體驗日｜作者參考短文\n\n2026-10-03 14:00，在虛構青禾教室一起觀察商品影像與素材交付。青禾杯是本系列原創的薄荷綠插畫杯，右側有一個把手，杯底有橘色圈，正面有一個圓點。\n\n活動練習先看原始參考圖，再檢查商品圖、情境圖與影片是否保留相同特徵。看到日期、色彩或物件數量不一致時，回到來源與版本表核對，留下修正紀錄。\n\n這是虛構教學素材，沒有真實報名或付款入口。文章是作者參考版，尚未執行Gemini改寫與完整影音交付。")
    assets = [("A1", "article", "F01|F02|F03|F04|F05"), ("I1", "banner", "F01|F02|F03"), ("I2", "product", "F01"), ("I3", "invitation", "F01|F02|F03|F04|F05"), ("V1", "video", "F01|F02|F03|F05")]
    table("68/asset-register.csv", ["asset_id", "kind", "fact_ids", "brief_version", "file", "sha256", "prompt", "source_asset", "license", "reviewer", "status"], [{"asset_id": sid, "kind": kind, "fact_ids": facts, "brief_version": "v1", "status": "not_run"} for sid, kind, facts in assets])
    put("68/handoff.md", "# 交付狀態\n\n作者簡報、參考短文與素材清單已備妥。尚缺本篇三張實際圖片、三鏡頭實際影片、生成提示詞紀錄、尺寸／副檔名／時間碼與審閱結果；不是可直接發布的完整成果包。\n\nv2日期變更應影響A1、I1、I3、V1；I2未引用F02，仍需抽查是否意外寫入日期。更新文字原稿、可編輯字卡、圖像輸出、影片輸出與素材表；不能只改文章。\n\n每個成品存在且來源、授權、版本、核對紀錄齊全才可填完成；缺檔或待生成保留not_run。不在本練習執行對外發布。")
    license_text = (HERE.parent / "work/examples/51/LICENSE.txt").read_text(encoding="utf-8")
    for n in range(63, 69):
        put(f"{n}/LICENSE.txt", license_text)
        put(f"{n}/README.md", f"# 第 {n} 篇作者練習材料\n\n原創虛構教材、向量參考素材與程式依MIT授權。參考圖、刻意故障圖、分鏡及腳本皆非Gemini／Flow實際生成輸出。\n\n本次瀏覽器User unavailable，實際模型生成、影音、Google Sheets匯入和雲端操作尚未驗證；保留not_run。第67篇XLSX是本機公式模板，下載後可按教學自行匯入。\n")


if __name__ == "__main__":
    build()
