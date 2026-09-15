"""Original vector lesson artwork; short labels remain readable on a phone."""
from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECS = {
    69: ("GEMINI.md", "載入範圍實驗", "分開核對三種載入證據", [
        ("常駐記憶", "全域 ＋ 專案", "先看 memory show"),
        ("工具新增", "讀取子目錄檔案", "再看 JIT 與清單"),
        ("重新載入", "清除舊載入清單", "再讀才重新探索"),
        ("驗證結果", "載入 ≠ 遵循", "最後仍須查成果"),
    ], "實測：CLI 0.59.0 載入模組"),
    70: ("團隊規則", "拆分與維護", "主檔短，責任與測試要清楚", [
        ("主檔", "說清適用範圍", "匯入三份共用規則"),
        ("分工", "風格・測試・責任", "每條都有維護理由"),
        ("測試", "檔案存在不夠", "命令也必須跑通"),
        ("交接", "保留變更原因", "新成員能重做一次"),
    ], "反例：缺檔與衝突命令，都應被發現"),
    71: ("設定為何", "沒有生效？", "八組實驗，先找來源再改值", [
        ("來源", "使用者 → 專案", "再看系統強制設定"),
        ("格式", "JSON 與資料型別", "是不同的檢查"),
        ("使用", "未知鍵可能保留", "不代表功能存在"),
        ("環境", "信任・版本・引數", "每次只變一項"),
    ], "實測：CLI 0.59.0；其他版本需重做"),
    72: ("三個指令", "一組可測契約", "先驗提示詞，再驗模型成果", [
        ("REVIEW", "範圍・證據・問題", "找不到就說待確認"),
        ("TEST PLAN", "正常 ＋ 邊界案例", "未執行就標建議"),
        ("DOCS SYNC", "程式與文件比對", "不直接覆寫內容"),
        ("參數", "空白・中文・引號", "十八組本機展開"),
    ], "提示詞展開已測；模型回答品質未測"),
    73: ("技能打包", "安裝與回退", "版本、啟用狀態與執行結果", [
        ("腳本", "成功 0・缺欄位 1", "讀取失敗 2"),
        ("安裝", "核對名稱與版本", "模型觸發另驗"),
        ("更新", "來源與安裝是副本", "更新後重新核對"),
        ("回退", "保留完整舊版本", "重裝後再跑案例"),
    ], "模組已測；Windows 終端異常待複驗"),
    74: ("只改這裡", "保留原有工作", "從範圍到恢復，每步都有證據", [
        ("先記錄", "範圍 ＋ 原有差異", "別漏掉未追蹤檔案"),
        ("小修改", "只改指定模組", "用同一測試核對"),
        ("保留", "使用者草稿不覆寫", "比較前後差異"),
        ("恢復", "對話 ≠ 檔案回復", "先讀磁碟現況"),
    ], "本機修正已測；登入會話恢復未測"),
}
SOURCE_URLS = {
    69: [("GEMINI.md 與 JIT", "https://geminicli.com/docs/cli/gemini-md/"), ("CLI 原始碼：0.59.0", "https://github.com/google-gemini/gemini-cli/tree/v0.59.0")],
    70: [("GEMINI.md 匯入", "https://geminicli.com/docs/cli/gemini-md/"), ("Memory Import Processor", "https://geminicli.com/docs/reference/memport/")],
    71: [("CLI 設定參考", "https://geminicli.com/docs/reference/configuration/"), ("互動設定", "https://geminicli.com/docs/cli/settings/")],
    72: [("自訂指令", "https://geminicli.com/docs/cli/custom-commands/"), ("CLI 原始碼：0.59.0", "https://github.com/google-gemini/gemini-cli/tree/v0.59.0")],
    73: [("建立 Agent Skills", "https://geminicli.com/docs/cli/creating-skills/"), ("Extension 參考", "https://geminicli.com/docs/extensions/reference/")],
    74: [("會話恢復", "https://geminicli.com/docs/cli/tutorials/session-management/"), ("忽略檔案", "https://geminicli.com/docs/cli/gemini-ignore/")],
}


def text(x: int, y: int, size: int, value: str, color="#122e39", weight=500) -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'


def wrap(title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<rect width="1600" height="900" fill="#f7f3e8"/>
<g font-family="Noto Sans TC, Microsoft JhengHei, sans-serif">{body}</g></svg>'''


def build() -> None:
    registry = {}
    for number, (line1, line2, heading, cards, footer) in SPECS.items():
        folder = HERE / str(number)
        folder.mkdir(parents=True, exist_ok=True)
        hero_title = f"{line1}：{line2}"
        hero = '<rect x="90" y="95" width="380" height="82" rx="41" fill="#d2e8d4"/>'
        hero += text(128, 153, 43, f"GEMINI 實驗 {number}", weight=700)
        hero += text(100, 345, 120, line1, weight=800) + text(100, 495, 120, line2, weight=800)
        hero += text(105, 640, 49, "讀懂規則・親手驗證・留下紀錄")
        hero += '<path d="M1150 240V640M1250 200V670M1350 300V600" stroke="#abcaba" stroke-width="18" stroke-linecap="round"/>'
        for index, y in enumerate([310, 490, 410]):
            x = 1150 + index * 100
            hero += f'<circle cx="{x}" cy="{y}" r="48" fill="#286657"/><circle cx="{x}" cy="{y}" r="17" fill="#f7f3e8"/>'
        hero += '<path d="M100 750H1500" stroke="#b7c6bd" stroke-width="3"/>'
        hero += text(100, 817, 39, "MOKAAIR / GEMINI 深入教學", color="#48615c")
        (folder / "hero.svg").write_text(wrap(hero_title, "用三條可調軌道表示設定需要分項驗證。", hero), encoding="utf-8", newline="\n")
        body = text(85, 108, 64, heading, weight=800)
        for index, (label, first, second) in enumerate(cards):
            x, y = 85 + (index % 2) * 735, 160 + (index // 2) * 290
            body += f'<rect x="{x}" y="{y}" width="695" height="257" rx="25" fill="#ffffff" stroke="#c3d5ca" stroke-width="3"/>'
            body += text(x + 35, y + 75, 57, label, color="#286657", weight=800)
            body += text(x + 35, y + 151, 54, first)
            body += text(x + 35, y + 219, 54, second)
        body += text(85, 818, 47, footer, color="#48615c")
        description = "；".join("：".join(card) for card in cards)
        (folder / "diagram-1.svg").write_text(wrap(heading, description, body), encoding="utf-8", newline="\n")
        sources = [{"title": title, "url": url, "checked_on": "2026-09-14"} for title, url in SOURCE_URLS[number]]
        meta = {"hero_alt": hero_title + "教學封面", "diagram_alt": description,
            "diagram_caption": heading + "。" + footer + "。本圖是概念整理，不是操作介面截圖。", "sources": sources,
            "downloads": [{"source": f"examples/lesson-{number}.zip", "filename": f"lesson-{number}.zip", "text": f"下載第 {number} 篇完整練習包"},
                {"source": "examples/md-verification.zip", "filename": "md-verification.zip", "text": "下載本批本機驗證程式與六組練習（CLI 0.59.0）"}]}
        (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        registry[str(number)] = sources
    (HERE / "sources.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build()
