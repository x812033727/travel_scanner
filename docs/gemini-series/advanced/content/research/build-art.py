"""Original SVG covers and teaching diagrams for research lessons 57–62."""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECS = {57: ('來源版本', '更新有紀錄', '同一份規格，分清來源與產出', [('清單', '六個固定 ID', 'S01 保存兩版'), ('更新', '24 人 → 30 人', '只採有效規格'), ('觀察', 'Drive 與上傳', '兩種方式分開測'), ('交付', '來源 ＋ 舊產出', '逐份查是否重做')], '文件已查；真實同步與回答待驗'), 58: ('引用查核', '支持或未知', '先找原文，再判斷是否支持', [('支持', '明確取代舊值', '名額修訂為 30'), ('未決', '日期只是提案', '不能當成定案'), ('未知', '沒有餐點資料', '引用可保留空白'), ('修正', '保存原始回答', '主張與引文同查')], '五列矩陣已查；模型引用待驗'), 59: ('十二道題', '複習有依據', '題目先審閱，作答才有意義', [('範圍', '兩章・十二概念', '每題對回章節'), ('審題', '單一正確選項', '刪除教材外題'), ('作答', '答案 ＋ 一句理由', '先分辨是否懂'), ('重測', '預定不等於完成', '填實際日期結果')], '題庫與程式已查；真實重測待驗'), 60: ('論文比較', '數字有條件', '不同資料與量尺，不能直接排名', [('識別', '三份原始全文', '作者・版本・授權'), ('方法', '問題・資料切分', '監督訊號分清楚'), ('結果', '78.4 與 61.3', '不是同一項測量'), ('限制', '歷史模型實驗', '不能推成現況')], '原文與 PDF 已查；模型矩陣待驗'), 61: ('多格式教材', '逐項核對', '十項事實，三種格式各自查', [('來源', '固定 F01 到 F10', '只用本篇教材'), ('產出', '講義・語音・影片', '保存實際生成檔'), ('核對', '十項 × 三格式', '時間與句子對照'), ('修正', '條件不可省略', '重做後再次檢查')], '作者教材已備；語音影片尚未生成'), 62: ('研究報告', '保存與重算', '一次快照能回答哪些問題？', [('範圍', '官方歷史快照', '不是全年使用量'), ('計算', '1800 個站點 ID', '十三種地區標籤'), ('查核', '校區不是行政區', '欄位對應待確認'), ('更新', '至少三項待查', '新舊版本分開存')], '公開資料已重算；模型研究待驗')}
SOURCE_URLS = {57: [('加入與更新來源', 'https://support.google.com/gemininotebook/answer/16215270?hl=en'), ('Notebook 與 Gemini 整合差異', 'https://support.google.com/gemininotebook/answer/17003757')], 58: [('Notebook 聊天與引用', 'https://support.google.com/gemininotebook/answer/16179559'), ('來源範圍與匯入', 'https://support.google.com/gemininotebook/answer/16215270?hl=en')], 59: [('學習卡與測驗', 'https://support.google.com/gemininotebook/answer/16958963?hl=en'), ('來源與引用', 'https://support.google.com/gemininotebook/answer/16179559')], 60: [('Notebook 來源操作', 'https://support.google.com/gemininotebook/answer/16215270?hl=en'), ('DPR 原始論文', 'https://aclanthology.org/2020.emnlp-main.550/'), ('HyDE 原始論文', 'https://aclanthology.org/2023.acl-long.99/'), ('Lost in the Middle 原始論文', 'https://aclanthology.org/2024.tacl-1.9/'), ('ACL 材料授權', 'https://aclanthology.org/faq/copyright/')], 61: [('語音摘要', 'https://support.google.com/gemininotebook/answer/16212820?hl=en'), ('影片摘要', 'https://support.google.com/gemininotebook/answer/16454555?hl=en'), ('Studio 與 Gemini 入口差異', 'https://support.google.com/gemininotebook/answer/17003757')], 62: [('Deep Research 操作', 'https://support.google.com/gemini/answer/15719111?hl=en'), ('Notebook 來源', 'https://support.google.com/gemininotebook/answer/16215270?hl=en'), ('臺北 YouBike 資料集', 'https://data.nat.gov.tw/dataset/147580'), ('官方即時 JSON', 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'), ('政府資料開放授權條款', 'https://data.gov.tw/license')]}

def text(x: int, y: int, size: int, value: str, color="#263b38", weight=500) -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'


def wrap(title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<rect width="1600" height="900" fill="#eef3f8"/>
<g font-family="Noto Sans TC, Microsoft JhengHei, sans-serif">{body}</g></svg>'''


def build() -> None:
    registry = {}
    for number, (line1, line2, heading, cards, footer) in SPECS.items():
        folder = HERE / str(number)
        folder.mkdir(parents=True, exist_ok=True)
        hero_title = f"{line1}：{line2}"
        hero = '<rect x="90" y="95" width="390" height="82" rx="41" fill="#dce6f3"/>'
        hero += text(125, 153, 43, f"GEMINI 實驗 {number}", weight=700)
        hero += text(100, 345, 113, line1, weight=800) + text(100, 495, 113, line2, weight=800)
        hero += text(105, 640, 49, "來源與主張・逐項核對・留下未知")
        hero += '<path d="M1150 295H1400V540H1150Z" fill="none" stroke="#a6bedb" stroke-width="16" stroke-linejoin="round"/>'
        for x, y, label in ((1150, 295, "1"), (1400, 295, "2"), (1400, 540, "3"), (1150, 540, "4")):
            hero += f'<circle cx="{x}" cy="{y}" r="59" fill="#365477"/>'
            hero += text(x - 16, y + 20, 58, label, color="#ffffff", weight=800)
        hero += '<path d="M100 750H1500" stroke="#b8ccd0" stroke-width="3"/>'
        hero += text(100, 817, 39, "MOKAAIR / GEMINI 深入教學", color="#475f7d")
        (folder / "hero.svg").write_text(wrap(hero_title, "以四個相連節點表示有順序且能查證的工作練習流程。", hero), encoding="utf-8", newline="\n")
        body = text(85, 108, 64, heading, weight=800)
        for index, (label, first, second) in enumerate(cards):
            x, y = 85 + index % 2 * 735, 160 + index // 2 * 290
            body += f'<rect x="{x}" y="{y}" width="695" height="257" rx="25" fill="#ffffff" stroke="#b9cfd1" stroke-width="3"/>'
            body += text(x + 35, y + 75, 57, label, color="#365477", weight=800)
            body += text(x + 35, y + 151, 54, first)
            body += text(x + 35, y + 219, 54, second)
        body += text(85, 818, 47, footer, color="#475f7d")
        description = "；".join("：".join(card) for card in cards)
        (folder / "diagram-1.svg").write_text(wrap(heading, description, body), encoding="utf-8", newline="\n")
        sources = [{"title": title, "url": url, "checked_on": "2026-09-14"} for title, url in SOURCE_URLS[number]]
        meta = {"hero_alt": hero_title + "教學封面", "diagram_alt": description,
                "diagram_caption": heading + "。" + footer + "。這是原創概念圖，不是介面截圖。", "sources": sources,
                "downloads": [{"source": f"examples/lesson-{number}.zip", "filename": f"lesson-{number}.zip", "text": f"下載第 {number} 篇完整練習包"},
                              {"source": "examples/research-verification.zip", "filename": "research-verification.zip", "text": "下載六組研究練習與本機檢查程式"}]}
        (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        registry[str(number)] = sources
    (HERE / "sources.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build()
