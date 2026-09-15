"""Original SVG artwork for creative lessons 63–68."""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECS = {63: ('圖片系列', '主體要一致', '同一原創商品，三種使用情境', [('固定', '外形・色彩・把手', '一個杯子一個圓點'), ('改變', '商品・桌面・橫幅', '每次只換一種用途'), ('評分', '五項各零至二分', '每次扣分附原因'), ('保留', '原圖與失敗輸出', '不把漂亮當合格')], '參考圖已備；真實模型輸出待驗'), 64: ('修圖除錯', '每輪查全圖', '修好日期，也要保留商品外觀', [('目標', '十二月改成十月', '每輪只改一件事'), ('保留', '杯身・把手・背景', '未要求區域也查'), ('退化', '回原始圖重做', '不覆蓋前輪結果'), ('文字', '保留可編輯圖層', '人工補正另記錄')], '作者補正示例；Gemini 修圖待驗'), 65: ('三鏡頭短片', '逐鏡生成', '先查模型支援，再記錄真實結果', [('分鏡', '開場・過程・收尾', '每鏡一個主要動作'), ('模式', '影格與參考素材', '模型支援不同'), ('生成', '保存提示詞與輸入', '秒數點數填實際'), ('合片', '順序與聲音同查', '下載後完整播放')], '靜態分鏡已備；Flow 影片待生成'), 66: ('轉場連貫', '接點前後查', '不只一格，檢查前後一秒', [('主體', '外形・位置・光線', '兩段都要對照'), ('影格', '使用真正影片末幀', '不能用示意圖充當'), ('重做', '先核對模式支援', '一次修正一個問題'), ('比較', '基準與修訂並存', '整段與聲音也查')], '接點示例已備；實際片段待驗'), 67: ('資料報表', '清理有依據', '保留原表，分幣別核對金額', [('原始', '五十列合成交易', '來源列號可追查'), ('採用', '四十三列可計算', '退款與大額保留'), ('隔離', '七列待查或重複', '空白金額不補零'), ('總數', 'TWD 45340', 'USD 50 分開列')], '本機公式已測；Sheets 匯入待驗'), 68: ('內容交付', '版本可追查', '日期變更，要找出所有成品', [('來源', '固定五項活動事實', '同一資料表出發'), ('製作', '文章・三圖・短片', '記錄版本與輸入'), ('變更', '日期 F02 更新', '四份成品受影響'), ('交付', '原稿・成品・限制', '缺檔不能標完成')], '交付練習已備；實際影音仍待補')}
SOURCE_URLS = {63: [('Gemini 圖片生成與編輯', 'https://support.google.com/gemini/answer/14286560?hl=en')], 64: [('Gemini 圖片生成與編輯', 'https://support.google.com/gemini/answer/14286560?hl=en')], 65: [('Flow 建立影片', 'https://support.google.com/flow/answer/16353334?hl=en'), ('Flow 模型與支援功能', 'https://support.google.com/flow/answer/16352836?hl=en'), ('Flow 使用條件', 'https://support.google.com/flow/answer/16353333?hl=en'), ('AI 點數與用量紀錄', 'https://support.google.com/googleone/answer/16287445'), ('Flow 編輯與建立場景', 'https://support.google.com/flow/answer/16935718')], 66: [('Flow 建立影片', 'https://support.google.com/flow/answer/16353334?hl=en'), ('Flow 模型與支援功能', 'https://support.google.com/flow/answer/16352836?hl=en'), ('Flow 編輯與建立場景', 'https://support.google.com/flow/answer/16935718')], 67: [('Gemini in Sheets', 'https://support.google.com/docs/answer/14356410?hl=en')], 68: [('Gemini 圖片生成與編輯', 'https://support.google.com/gemini/answer/14286560?hl=en'), ('Flow 建立影片', 'https://support.google.com/flow/answer/16353334?hl=en'), ('Google 提示詞建議', 'https://support.google.com/docs/answer/15013615?hl=en')]}

def text(x: int, y: int, size: int, value: str, color="#263b38", weight=500) -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'


def wrap(title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<rect width="1600" height="900" fill="#fbf1e8"/>
<g font-family="Noto Sans TC, Microsoft JhengHei, sans-serif">{body}</g></svg>'''


def build() -> None:
    registry = {}
    for number, (line1, line2, heading, cards, footer) in SPECS.items():
        folder = HERE / str(number)
        folder.mkdir(parents=True, exist_ok=True)
        hero_title = f"{line1}：{line2}"
        hero = '<rect x="90" y="95" width="390" height="82" rx="41" fill="#f3dcc5"/>'
        hero += text(125, 153, 43, f"GEMINI 實驗 {number}", weight=700)
        hero += text(100, 345, 113, line1, weight=800) + text(100, 495, 113, line2, weight=800)
        hero += text(105, 640, 49, "原創素材・逐輪核對・保留版本")
        hero += '<path d="M1150 295H1400V540H1150Z" fill="none" stroke="#d7b898" stroke-width="16" stroke-linejoin="round"/>'
        for x, y, label in ((1150, 295, "1"), (1400, 295, "2"), (1400, 540, "3"), (1150, 540, "4")):
            hero += f'<circle cx="{x}" cy="{y}" r="59" fill="#875b3e"/>'
            hero += text(x - 16, y + 20, 58, label, color="#ffffff", weight=800)
        hero += '<path d="M100 750H1500" stroke="#b8ccd0" stroke-width="3"/>'
        hero += text(100, 817, 39, "MOKAAIR / GEMINI 深入教學", color="#775b45")
        (folder / "hero.svg").write_text(wrap(hero_title, "以四個相連節點表示有順序且能查證的工作練習流程。", hero), encoding="utf-8", newline="\n")
        body = text(85, 108, 64, heading, weight=800)
        for index, (label, first, second) in enumerate(cards):
            x, y = 85 + index % 2 * 735, 160 + index // 2 * 290
            body += f'<rect x="{x}" y="{y}" width="695" height="257" rx="25" fill="#ffffff" stroke="#b9cfd1" stroke-width="3"/>'
            body += text(x + 35, y + 75, 57, label, color="#875b3e", weight=800)
            body += text(x + 35, y + 151, 54, first)
            body += text(x + 35, y + 219, 54, second)
        body += text(85, 818, 47, footer, color="#775b45")
        description = "；".join("：".join(card) for card in cards)
        (folder / "diagram-1.svg").write_text(wrap(heading, description, body), encoding="utf-8", newline="\n")
        sources = [{"title": title, "url": url, "checked_on": "2026-09-14"} for title, url in SOURCE_URLS[number]]
        meta = {"hero_alt": hero_title + "教學封面", "diagram_alt": description,
                "diagram_caption": heading + "。" + footer + ("。合計 TWD 45340、USD 50，分幣別列示" if number == 67 else "") + "。這是原創概念圖，不是介面截圖。", "sources": sources,
                "downloads": [{"source": f"examples/lesson-{number}.zip", "filename": f"lesson-{number}.zip", "text": f"下載第 {number} 篇完整練習包"},
                              {"source": "examples/creative-verification.zip", "filename": "creative-verification.zip", "text": "下載六組創作練習與本機檢查程式"}]}
        (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        registry[str(number)] = sources
    (HERE / "sources.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build()
