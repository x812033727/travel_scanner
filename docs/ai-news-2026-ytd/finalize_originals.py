"""Final editor changes after complete read, before translation input is frozen."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
for file in (HERE/'renders/drafts').glob('*.json'):
    r=json.loads(file.read_text(encoding='utf8'));d=r['document'];slug=r['slug']
    if 'fable-5-access' in slug:
        d['sections'][2]['paragraphs'].append('可以挑一份已完成的研究筆記，請另一位同事只用匯出的檔案接手，看看是否找得到引用來源與尚未確認的問題。若仍須回到原平台才能理解附件或上下文，就表示備份方式還需要補強。這種小型交接演練，比只確認下載按鈕能用，更能反映資料是否真的可攜。')
    if 'gemini-36' in slug:
        d['sections'][2]['paragraphs'].append('抽樣時可同時選一般紀錄與已標記的例外，避免只檢查看起來最整齊的輸出。若簡單分類先把重要疑點刪掉，後面的強模型也無從核對。保留原始資料與處理紀錄，才能發現分工流程究竟是在省事，還是把錯誤藏得更深。')
    if 'nvidia-rubin' in slug:
        d['sections'][2]['paragraphs'][2]='將員工挑錯、修正提示和重新整理資料的時間計入後，才能算出每筆合格商品的完整成本。人力費用可能是重要部分，但占比需要從實際記錄取得，不能預設為雲端費用的固定倍數。若新的硬體或服務只改善一小段運算，整體效益也要放回這份工作紀錄比較，才知道改變是否值得。'
    if 'gpt-54' in slug:
        d['sections'][4]['paragraphs'][0]=d['sections'][4]['paragraphs'][0].replace('為行政人員省下數小時的純手工整理時間','協助行政人員處理部分手工整理工作，省下多少時間則需自行比較')
    r['paragraph_characters']=sum(map(len,d['introduction']))+sum(len(p) for s in d['sections'] for p in s['paragraphs'])
    assert 1800<=r['paragraph_characters']<=3000,(slug,r['paragraph_characters'])
    file.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('All 22 originals meet the requested paragraph length')
