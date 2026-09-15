"""Original, accessible vector covers and instructional diagrams for lessons 75–80."""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECS = {
    75: ("本機 MCP", "查詢與除錯", "固定資料來源，逐項驗證連線", [
        ("輸入", "只接受商品編號", "拒絕路徑與錯誤型別"),
        ("查詢", "唯讀合成 CSV", "不開放任意檔案"),
        ("結果", "找到・查無資料", "資料文字不是指令"),
        ("連線", "啟動・握手・中斷", "分開記錄錯誤"),
    ], "本機 stdio 已測；模型選工具待驗"),
    76: ("Hooks", "品質檢查關卡", "非零退出，不一定代表阻擋", [
        ("JSON 決策", "allow 或 deny", "核對 BeforeTool"),
        ("退出碼 2", "阻擋這次操作", "錯誤原因要可讀"),
        ("退出碼 1", "可能繼續執行", "不是通用阻擋碼"),
        ("逾時", "不等於已阻擋", "仍須核對實際決策"),
    ], "CLI 0.59.0 Hook 模組實測"),
    77: ("兩個代理", "一份審查報告", "引用有依據，衝突交給人判斷", [
        ("契約", "檔名・行號・原文", "缺證據就不接受"),
        ("重複", "同項同建議", "合併並保留來源"),
        ("衝突", "同項不同建議", "列出兩邊理由"),
        ("交付", "待人工審閱", "不自動套用修正"),
    ], "定義與合併已測；模型回答待驗"),
    78: ("二十份文件", "中斷後接著跑", "核對輸入與成品，再使用檢查點", [
        ("第一次", "完成 5 份後停止", "保留結果與雜湊"),
        ("接續", "跳過 5・完成 15", "避免重複產出"),
        ("更動", "只改 1 份來源", "只重做那 1 份"),
        ("失敗", "記錄後停止", "不自動重試模型"),
    ], "固定資料實測；真實模型用量待驗"),
    79: ("GitHub", "保存審查報告", "先跑固定資料，再核對遠端產物", [
        ("觸發", "手動・預設分支", "固定事件提交"),
        ("環境", "核對帳號條件", "需要的審核另設"),
        ("模式", "fixture → live", "一份資料先驗證"),
        ("交付", "下載 artifact", "核對模式與結果"),
    ], "本機執行器已測；遠端工作流待驗"),
    80: ("文件維護", "交付可讀差異", "先核對候選，再決定是否套用", [
        ("原稿", "十份互連文件", "保留初始內容"),
        ("候選", "只改允許範圍", "沒有來源就停下"),
        ("檢查", "檔案・定位點", "拒絕不存在的目標"),
        ("差異", "報告 ＋ patch", "交給人工審閱"),
    ], "參考修正已測；尚未套用或發布"),
}
SOURCE_URLS = {
    75: [("Gemini CLI MCP server", "https://geminicli.com/docs/tools/mcp-server/"),
         ("MCP Python SDK 2.2.0", "https://pypi.org/project/mcp/2.2.0/"),
         ("MCP Python SDK 官方原始碼", "https://github.com/modelcontextprotocol/python-sdk")],
    76: [("Hooks 概念與設定", "https://geminicli.com/docs/hooks/"),
         ("Hook 事件及退出碼", "https://geminicli.com/docs/hooks/reference/")],
    77: [("CLI Subagents", "https://geminicli.com/docs/core/subagents/"),
         ("CLI 0.59.0 原始碼", "https://github.com/google-gemini/gemini-cli/tree/v0.59.0")],
    78: [("CLI Headless 模式", "https://geminicli.com/docs/cli/headless/"),
         ("CLI Policy Engine", "https://geminicli.com/docs/reference/policy-engine/")],
    79: [("GitHub Actions 工作流語法", "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax"),
         ("GitHub Actions 安全使用", "https://docs.github.com/en/actions/reference/security/secure-use"),
         ("Artifact 官方 Action", "https://github.com/actions/upload-artifact")],
    80: [("CLI 自訂指令", "https://geminicli.com/docs/cli/custom-commands/"),
         ("CLI Headless 模式", "https://geminicli.com/docs/cli/headless/"),
         ("Git apply 官方參考", "https://git-scm.com/docs/git-apply")],
}


def text(x: int, y: int, size: int, value: str, color="#173445", weight=500) -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'


def wrap(title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<rect width="1600" height="900" fill="#f3f5ee"/>
<g font-family="Noto Sans TC, Microsoft JhengHei, sans-serif">{body}</g></svg>'''


def build() -> None:
    registry = {}
    for number, (line1, line2, heading, cards, footer) in SPECS.items():
        folder = HERE / str(number)
        folder.mkdir(parents=True, exist_ok=True)
        hero_title = f"{line1}：{line2}"
        hero = '<rect x="90" y="95" width="390" height="82" rx="41" fill="#d8e6ed"/>'
        hero += text(125, 153, 43, f"GEMINI 實驗 {number}", weight=700)
        hero += text(100, 345, 113, line1, weight=800) + text(100, 495, 113, line2, weight=800)
        hero += text(105, 640, 49, "限定範圍・保存證據・逐步驗證")
        hero += '<path d="M1150 295H1400V540H1150Z" fill="none" stroke="#b1c9ce" stroke-width="16" stroke-linejoin="round"/>'
        for x, y, label in ((1150, 295, "1"), (1400, 295, "2"), (1400, 540, "3"), (1150, 540, "4")):
            hero += f'<circle cx="{x}" cy="{y}" r="59" fill="#2b6577"/>'
            hero += text(x - 16, y + 20, 58, label, color="#ffffff", weight=800)
        hero += '<path d="M100 750H1500" stroke="#b8ccd0" stroke-width="3"/>'
        hero += text(100, 817, 39, "MOKAAIR / GEMINI 深入教學", color="#476574")
        (folder / "hero.svg").write_text(wrap(hero_title, "以四個相連節點表示有順序且能查證的自動化流程。", hero), encoding="utf-8", newline="\n")
        body = text(85, 108, 64, heading, weight=800)
        for index, (label, first, second) in enumerate(cards):
            x, y = 85 + index % 2 * 735, 160 + index // 2 * 290
            body += f'<rect x="{x}" y="{y}" width="695" height="257" rx="25" fill="#ffffff" stroke="#b9cfd1" stroke-width="3"/>'
            body += text(x + 35, y + 75, 57, label, color="#2b6577", weight=800)
            body += text(x + 35, y + 151, 54, first)
            body += text(x + 35, y + 219, 54, second)
        body += text(85, 818, 47, footer, color="#476574")
        description = "；".join("：".join(card) for card in cards)
        (folder / "diagram-1.svg").write_text(wrap(heading, description, body), encoding="utf-8", newline="\n")
        sources = [{"title": title, "url": url, "checked_on": "2026-09-14"} for title, url in SOURCE_URLS[number]]
        meta = {"hero_alt": hero_title + "教學封面", "diagram_alt": description,
                "diagram_caption": heading + "。" + footer + "。這是原創概念圖，不是介面截圖。", "sources": sources,
                "downloads": [{"source": f"examples/lesson-{number}.zip", "filename": f"lesson-{number}.zip", "text": f"下載第 {number} 篇完整練習包"},
                              {"source": "examples/automation-verification.zip", "filename": "automation-verification.zip", "text": "下載六組練習與本機驗證程式（CLI 0.59.0）"}]}
        (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        registry[str(number)] = sources
    (HERE / "sources.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build()
