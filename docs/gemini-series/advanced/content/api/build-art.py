"""Original code-native SVG art for API lessons; no external images or model calls."""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECS = {
81: ("工具呼叫", "驗證再執行", "模型提出要求，程式決定能做什麼", [("宣告","只讀合成訂單","名稱與參數白名單"),("檢查","查無與非法分開","不動態執行字串"),("回傳","保留呼叫識別碼","完整步驟交回模型"),("停止","次數與時間有界","不把逾時當重送")],"本機協定已測；真實模型待驗"),
82: ("搜尋引用", "對照來源", "答案、引用與搜尋建議分別核對", [("搜尋","確認搜尋步驟","沒有搜尋就不冒稱"),("定位","中文用位元組查","錯誤邊界停止連結"),("呈現","保留來源與建議","不改寫搜尋元件"),("保存","真實回應僅記憶體","作者測試資料可下載")],"合成引用已測；真實搜尋待驗"),
83: ("檔案索引", "版本可追查", "原始檔案、索引文件、操作各有身分", [("匯入","保存原檔與操作","完成不代表答對"),("查詢","只讀目前版本","引文須能對到原文"),("更新","新版入庫後查核","刪除舊版再提問"),("清理","索引與原檔分開","只處理自己的帳本")],"十份合成文件已備；雲端待驗"),
84: ("快取實驗", "用量與帳單", "不同 API 家族，分開記錄成本", [("隱含","Interactions","命中沒有保證"),("手動","generateContent","保存名稱與到期"),("比較","同文件與問題","缺值不改填為零"),("清理","到期與刪除各查","命中不等於省錢")],"本機序列化已測；實際費用待驗"),
85: ("批次評測", "每題可追蹤", "工作完成後，仍要逐題核對", [("送件","固定題目識別碼","逾時先核對原工作"),("分類","缺項與故障分開","已成功題目不重送"),("重試","引用父工作紀錄","驗雜湊與次數上限"),("採用","每題只採用一次","保留未解決項目")],"二十題合成故障已測；Batch 待驗"),
86: ("文件助手", "答案能追查", "從本機介面一路查到來源原文", [("啟動","預設作者模式","金鑰留在伺服器"),("回答","查詢與引用一起","缺證據就明示"),("評測","固定二十題","來源存在仍需閱讀"),("交接","版本與限制明列","停止服務另清索引")],"本機服務已測；真實問答待驗")}
BASE = "https://ai.google.dev/gemini-api/"
SOURCE_URLS = {
81:[("Function calling 官方教學",BASE+"docs/function-calling"),("Interactions 官方說明",BASE+"docs/interactions-overview")],
82:[("Google Search Grounding 官方教學",BASE+"docs/google-search"),("Gemini API 使用條款",BASE+"terms"),("官方 Python SDK", "https://googleapis.github.io/python-genai/")],
83:[("File Search 官方教學",BASE+"docs/file-search"),("官方 Python SDK","https://googleapis.github.io/python-genai/")],
84:[("Interactions 隱含快取",BASE+"docs/caching"),("generateContent 手動快取",BASE+"docs/generate-content/caching")],
85:[("Batch API 官方教學",BASE+"docs/batch-api"),("官方 Python SDK","https://googleapis.github.io/python-genai/")],
86:[("File Search 官方教學",BASE+"docs/file-search"),("Function calling 官方教學",BASE+"docs/function-calling"),("Interactions 官方說明",BASE+"docs/interactions-overview")]}
def text(x,y,size,value,color="#263b38",weight=500):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'
def wrap(title,description,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc><rect width="1600" height="900" fill="#edf3f6"/><g font-family="Noto Sans TC, Microsoft JhengHei, sans-serif">{body}</g></svg>'
def build():
    registry={}
    for number,(line1,line2,heading,cards,footer) in SPECS.items():
        folder=HERE/str(number)
        folder.mkdir(parents=True,exist_ok=True)
        title=f"{line1}：{line2}"
        hero='<rect x="90" y="95" width="390" height="82" rx="41" fill="#d5e5ef"/>'
        hero+=text(125,153,43,f"GEMINI 實驗 {number}",weight=700)
        hero+=text(100,345,113,line1,weight=800)+text(100,495,113,line2,weight=800)
        hero+=text(105,640,49,"固定資料・保留結果・核對限制")
        hero+='<path d="M1150 295H1400V540H1150Z" fill="none" stroke="#adc6d8" stroke-width="16"/>'
        for x,y,label in ((1150,295,"1"),(1400,295,"2"),(1400,540,"3"),(1150,540,"4")):
            hero+=f'<circle cx="{x}" cy="{y}" r="59" fill="#365477"/>'
            hero+=text(x-16,y+20,58,label,color="#ffffff",weight=800)
        hero+=text(100,817,39,"MOKAAIR / GEMINI 深入教學",color="#365477")
        (folder/"hero.svg").write_text(wrap(title,"四個節點表示四階段教學流程。",hero),encoding="utf-8")
        body=text(85,108,61,heading,weight=800)
        for i,(label,first,second) in enumerate(cards):
            x,y=85+i%2*735,160+i//2*290
            body+=f'<rect x="{x}" y="{y}" width="695" height="257" rx="25" fill="#ffffff" stroke="#adc6d8" stroke-width="3"/>'
            body+=text(x+35,y+75,57,label,color="#365477",weight=800)+text(x+35,y+151,52,first)+text(x+35,y+219,52,second)
        body+=text(85,818,47,footer,color="#365477")
        desc="；".join("：".join(c) for c in cards)
        (folder/"diagram-1.svg").write_text(wrap(heading,desc,body),encoding="utf-8")
        sources=[{"title":t,"url":u,"checked_on":"2026-09-14"} for t,u in SOURCE_URLS[number]]
        meta={"hero_alt":title+"教學封面","diagram_alt":desc,"diagram_caption":heading+"。"+footer+"。原創概念圖，不是操作截圖。","sources":sources,"downloads":[{"source":f"examples/lesson-{number}.zip","filename":f"lesson-{number}.zip","text":f"下載第 {number} 篇完整練習包"},{"source":"examples/api-verification.zip","filename":"api-verification.zip","text":"下載六組 API 練習與本機檢查程式"}]}
        (folder/"meta.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        registry[str(number)]=sources
    (HERE/"sources.json").write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":
    build()

