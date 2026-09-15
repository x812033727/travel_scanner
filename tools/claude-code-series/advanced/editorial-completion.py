"""Close small editorial gaps and mark authored content without claiming live validation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
notes={
65:'交接單最後加上更新時間，並註明目前哪些檔案尚未提交。若後續又修改檔案，先更新交接內容再結束階段，避免讀者照著過期狀態接手。',
68:'錯誤訊息可以示範正確參數格式，但不要自動猜選另一個檔案。讓讀者修正明確輸入後重新執行，才能保留本次審查範圍的可追蹤性。',
84:'若草稿描述中的測試名稱與實際命令不一致，先修正描述。審查者應能直接複製命令重現結果，不需要從聊天紀錄尋找漏掉的參數。',
85:'另外測試連續點同一筆兩次，完成狀態應回到起點，其他項目保持原樣。這個案例檢查的是翻轉操作的連續使用，不是只確認第一次點擊。若資料函式通過而畫面不變，查看是否仍使用舊狀態渲染；若畫面正確但重新整理後錯誤，則轉向儲存與載入流程，不再反覆修改已通過的比較式。',
86:'保存重構前的基準提交，讓讀者可以重新執行相同測試比較行為。若沒有基準，事後很難分辨變更是整理程式還是改變既有需求。',
88:'解決衝突時在紀錄寫出保留兩方需求的理由，不只記錄 Git 命令成功。命令成功代表提交完成，功能是否正確仍以最後檔案的行為為準。',
}
for number,paragraph in notes.items():
    path=ROOT/f'docs/claude-code-series/lessons/{number}.md'
    text=path.read_text(encoding='utf-8')
    if paragraph not in text:
        index=text.rfind('\n## ');text=text[:index]+'\n\n'+paragraph+'\n'+text[index:]
        path.write_text(text,encoding='utf-8')
plan_path=ROOT/'docs/claude-code-series/advanced/curriculum.json'
plan=json.loads(plan_path.read_text(encoding='utf-8'))
plan['status']='authored-local-preview'
for entry in plan['entries']:
    entry['status']='authored-local-preview'
    if entry['number']==96:entry['reading_minutes']=30
    additions={79:['list_tasks','get_task'],80:['list_tasks','get_task'],91:['--json-schema','--output-format','structured_output']}
    entry['aliases']=list(dict.fromkeys(entry['aliases']+additions.get(entry['number'],[])))
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in (ROOT/'tools/claude-code-series/advanced/lab').rglob('*.md'):
    if 'node_modules' in path.parts:continue
    text=path.read_text(encoding='utf-8').replace('證据','證據')
    path.write_text(text,encoding='utf-8')
