"""Create initial production trackers without overwriting measurements on reruns."""
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
episodes=[json.loads(f.read_text('utf-8')) for f in sorted((ROOT/'episodes').glob('*.json'))]

def csv_new(name,fields,rows):
    target=ROOT/name
    if target.exists():
        print(f'Preserved existing tracker: {name}'); return
    with target.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)

schedule=[];analytics=[];budget=[];claims=[];qa=[]
first=datetime.fromisoformat('2026-10-11T20:00:00+08:00')
for i,ep in enumerate(episodes):
    when=first+timedelta(days=14*i)
    schedule.append({'episode':ep['id'],'title':ep['title_a'],'proposed_publish_at':when.isoformat(),'status':'PROPOSED_NOT_SCHEDULED','actual_video_id':'','actual_published_at':'','short_1_proposed_at':(when+timedelta(days=2)).isoformat(),'short_2_proposed_at':(when+timedelta(days=5)).isoformat()})
    for window,days in [('48h',2),('7d',7),('28d',28)]:
        analytics.append({'episode':ep['id'],'checkpoint':window,'proposed_check_at':(when+timedelta(days=days)).isoformat(),'status':'NOT_PUBLISHED_NO_DATA'})
    for name,limit in [('AI 視覺',3000),('配音',1000),('音樂與授權',1000),('剪輯字幕工具',1000),('縮圖補生成',1000),('修改預備金',3000)]:
        budget.append({'episode':ep['id'],'category':name,'cap_twd':limit,'actual_twd':'','receipt':'','note':'規劃上限；沒有帳單資料不得填 0'})
    for n,s in enumerate(ep['scenes'],1):
        claims.append({'episode':ep['id'],'scene':n,'heading':s['heading'],'type':s['kind'],'source_ids':';'.join(s['refs']),'scope_note':'限定為來源實際支持範圍；虛構示例不作產品實測','checked_on':'2026-09-28'})
    for item in ['完整人耳配音審查','最終節奏與場景剪輯','手機畫面與字幕','公開素材與授權複核','頻道與發布時間確認','非公開上傳播放檢查','正式公開發布']:
        qa.append({'episode':ep['id'],'check':item,'status':'PENDING','checked_by':'','checked_at':'','evidence':''})
csv_new('schedule.csv',list(schedule[0]),schedule)
fields=['episode','checkpoint','proposed_check_at','status','video_id','published_at','observation_at','views','impressions','impressions_ctr_pct','retention_30s_pct','avg_percentage_viewed','subscribers_gained','returning_viewers','browse_impressions','browse_ctr_pct','suggested_impressions','suggested_ctr_pct','title_variant','thumbnail_variant','notes']
csv_new('analytics.csv',fields,analytics)
csv_new('budget.csv',list(budget[0]),budget)
csv_new('claim-ledger.csv',list(claims[0]),claims)
csv_new('release-checklist.csv',list(qa[0]),qa)
print('Trackers ready; no schedule or external publication was created.')
