"""Original, accessible vector covers and instructional diagrams for lessons 51–56."""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECS = {51: ('提示詞改寫', '用題庫比較', '一次只改一條規則', [('固定', '十題與量尺', '先寫預期判斷'), ('分開', 'A 與 B 新對話', '保存二十份回答'), ('評分', '四項各零至二分', '每次扣分附原因'), ('決定', '逐題看改善退步', '缺資料不算勝出')], '檢查程式已測；模型回答待驗'), 52: ('Gems 客服', '更新與回歸', '資料變更後，重跑相同問題', [('資料', '手冊有版本', '章節編號可追查'), ('回答', '已知附依據', '未知轉人工'), ('更新', '兩日 → 三日', '只改回覆目標'), ('回歸', '十二題再測一次', '版本標籤也核對')], '題庫與版本已查；Gems 回答待驗'), 53: ('Canvas 實作', '活動預算工具', '先核對公式，再檢查介面', [('需求', '人數・單價・場地', '備用金先取到分'), ('正常', '三組人工答案', '總額與每人核對'), ('錯誤', '空白・負值・文字', '清除上一筆結果'), ('交付', '完整 HTML 檔', '手機與鍵盤檢查')], '本機參考版已測；Canvas 生成待驗'), 54: ('會議信件', '交接有依據', '五封信件，保留更正與未知', [('來源', '先編 M1 到 M5', '日期時區要清楚'), ('更正', '十組 → 十二組', '保留兩封來源'), ('衝突', '兩個日期未定', '不能自行選一天'), ('交接', '文件 ＋ 待辦表', '未指派人員留空')], '合成信件已查；Workspace 操作待驗'), 55: ('手機筆記', '看見與推測', '照片、Live 與人工觀察分開', [('原圖', '保留來源與日期', '位置可回頭核對'), ('鏡頭', 'Android 與 iOS', '各自操作與紀錄'), ('未知', '遮擋與模糊', '指出需要補拍處'), ('交接', '原圖 ＋ 修正表', '電腦再次核對')], '照片與授權已查；手機實機待驗'), 56: ('Spark 摘要', '每週查核來源', '先手動查核，再觀察真實排程', [('範圍', '三個官方入口', '期間與時區固定'), ('查核', '可讀・取不到', '不把未知當沒更新'), ('排程', '核對下次時間', '等待一次真觸發'), ('停止', '暫停・恢復・刪除', '再看原定觸發時刻')], '期間程式已測；真實排程待驗')}
SOURCE_URLS = {51: [('Google 官方提示詞寫作建議', 'https://support.google.com/docs/answer/15013615?hl=en')], 52: [('建立與使用 Gems', 'https://support.google.com/gemini/answer/15235603?hl=en-GB'), ('Gems 基本說明', 'https://support.google.com/gemini/answer/15236405?hl=en-GB')], 53: [('Canvas 建立文件與程式', 'https://support.google.com/gemini/answer/16047321?hl=en')], 54: [('Gemini 連接應用程式', 'https://support.google.com/gemini/answer/13695044?hl=en'), ('Sheets 中的 Gemini', 'https://support.google.com/docs/answer/14356410?hl=en')], 55: [('Android Gemini Live', 'https://support.google.com/gemini/answer/15274899?hl=en'), ('iPhone 與 iPad Gemini Live', 'https://support.google.com/gemini/answer/15274899?co=GENIE.Platform%3DiOS&hl=en'), ('Commons 原始照片與 CC0 授權', 'https://commons.wikimedia.org/wiki/File:Parts_of_a_ballpoint_pen.jpg')], 56: [('Spark 可用性與操作', 'https://support.google.com/gemini/answer/17094507?hl=en-GA'), ('Spark 排程建立與管理', 'https://support.google.com/gemini/answer/17094710'), ('Gemini 官方消息入口', 'https://blog.google/products/gemini/'), ('Workspace 官方更新入口', 'https://workspaceupdates.googleblog.com/'), ('Gemini API 更新紀錄', 'https://ai.google.dev/gemini-api/docs/changelog')]}

def text(x: int, y: int, size: int, value: str, color="#263b38", weight=500) -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'


def wrap(title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<rect width="1600" height="900" fill="#f5f1e9"/>
<g font-family="Noto Sans TC, Microsoft JhengHei, sans-serif">{body}</g></svg>'''


def build() -> None:
    registry = {}
    for number, (line1, line2, heading, cards, footer) in SPECS.items():
        folder = HERE / str(number)
        folder.mkdir(parents=True, exist_ok=True)
        hero_title = f"{line1}：{line2}"
        hero = '<rect x="90" y="95" width="390" height="82" rx="41" fill="#dce9da"/>'
        hero += text(125, 153, 43, f"GEMINI 實驗 {number}", weight=700)
        hero += text(100, 345, 113, line1, weight=800) + text(100, 495, 113, line2, weight=800)
        hero += text(105, 640, 49, "限定範圍・保存證據・逐步驗證")
        hero += '<path d="M1150 295H1400V540H1150Z" fill="none" stroke="#afc9b8" stroke-width="16" stroke-linejoin="round"/>'
        for x, y, label in ((1150, 295, "1"), (1400, 295, "2"), (1400, 540, "3"), (1150, 540, "4")):
            hero += f'<circle cx="{x}" cy="{y}" r="59" fill="#316553"/>'
            hero += text(x - 16, y + 20, 58, label, color="#ffffff", weight=800)
        hero += '<path d="M100 750H1500" stroke="#b8ccd0" stroke-width="3"/>'
        hero += text(100, 817, 39, "MOKAAIR / GEMINI 深入教學", color="#4c685c")
        (folder / "hero.svg").write_text(wrap(hero_title, "以四個相連節點表示有順序且能查證的工作練習流程。", hero), encoding="utf-8", newline="\n")
        body = text(85, 108, 64, heading, weight=800)
        for index, (label, first, second) in enumerate(cards):
            x, y = 85 + index % 2 * 735, 160 + index // 2 * 290
            body += f'<rect x="{x}" y="{y}" width="695" height="257" rx="25" fill="#ffffff" stroke="#b9cfd1" stroke-width="3"/>'
            body += text(x + 35, y + 75, 57, label, color="#316553", weight=800)
            body += text(x + 35, y + 151, 54, first)
            body += text(x + 35, y + 219, 54, second)
        body += text(85, 818, 47, footer, color="#4c685c")
        description = "；".join("：".join(card) for card in cards)
        (folder / "diagram-1.svg").write_text(wrap(heading, description, body), encoding="utf-8", newline="\n")
        sources = [{"title": title, "url": url, "checked_on": "2026-09-14"} for title, url in SOURCE_URLS[number]]
        meta = {"hero_alt": hero_title + "教學封面", "diagram_alt": description,
                "diagram_caption": heading + "。" + footer + "。這是原創概念圖，不是介面截圖。", "sources": sources,
                "downloads": [{"source": f"examples/lesson-{number}.zip", "filename": f"lesson-{number}.zip", "text": f"下載第 {number} 篇完整練習包"},
                              {"source": "examples/work-verification.zip", "filename": "work-verification.zip", "text": "下載六組工作練習與本機檢查程式"}]}
        (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        registry[str(number)] = sources
    (HERE / "sources.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build()
