"""Editor correction of speed terminology in all five languages, after assembly."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
slug='ai-news-gemini-36-flash-20260721'
paragraphs={
'zh-TW':'速度是評估快速模型的一個項目，每秒處理字數描述的是處理速率，與一次請求需要等待多久並不完全相同。以市集名冊為例，若電話號碼少抓一位、把電壓 110V 誤寫成 220V，或漏掉地址的樓層，都可能造成聯絡或現場配置錯誤。團隊應核對關鍵欄位的完整性，並記錄重試與補救所花的時間。用同一批資料比較，才能看出速度改善是否也帶來合格成果，而不是只增加輸出量。',
'en':'Speed is one factor in evaluating fast models. Characters processed per second describe throughput, which is not the same as how long one request takes. In a market vendor roster, dropping a phone digit, recording 110V as 220V, or omitting an address floor could cause contact or setup errors. Teams should check that key fields are complete and record the time spent on retries and corrections. Comparing the same dataset helps reveal whether higher speed also produces usable results, rather than simply more output.',
'ja':'高速モデルを評価するうえで、速度は一つの項目です。1秒あたりの処理文字数は処理量を示し、1回のリクエストにかかる待ち時間とは同じではありません。マーケットの出店者名簿で電話番号が1桁欠けたり、電圧の110Vが220Vと記載されたり、住所の階数が抜けたりすると、連絡や現場の配置に支障が出る可能性があります。重要な欄が揃っているか確認し、再試行や修正にかかった時間も記録しましょう。同じデータで比較することで、速度の向上が単なる出力量の増加ではなく、使える成果につながっているかを判断しやすくなります。',
'ko':'속도는 빠른 모델을 평가하는 요소 중 하나입니다. 초당 처리 문자 수는 처리량을 나타내며, 한 번의 요청을 기다리는 시간과는 같은 개념이 아닙니다. 바자회 참가 업체 명단에서 전화번호 한 자리가 빠지거나 전압 110V가 220V로 기록되거나 주소의 층수가 누락되면 연락이나 현장 배치에 문제가 생길 수 있습니다. 중요한 항목이 빠짐없이 담겼는지 확인하고 재시도와 수정에 쓴 시간도 기록해야 합니다. 같은 데이터로 비교하면 속도 향상이 단순히 출력량을 늘리는 데 그치지 않고 실제로 쓸 수 있는 결과로 이어지는지 판단하기 쉽습니다.',
'zh-CN':'速度是评估快速模型的一个项目，每秒处理字数描述的是处理速率，与一次请求需要等待多久并不完全相同。以市集名册为例，若电话号码少抓一位、把电压 110V 误写成 220V，或漏掉地址的楼层，都可能造成联系或现场配置错误。团队应核对关键字段的完整性，并记录重试与补救所花的时间。用同一批数据比较，才能看出速度改善是否也带来合格成果，而不是只增加输出量。',
}
path=ROOT/'apps/api/app/guides/content'/f'{slug}.json';pack=json.loads(path.read_text(encoding='utf8'))
assert set(pack['locales'])==set(paragraphs)
for locale,text in paragraphs.items():
    assert pack['locales'][locale]['blocks'][10]['type']=='paragraph'
    pack['locales'][locale]['blocks'][10]['text']=text
path.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
draft_path=HERE/'renders/drafts'/f'{slug}.json';draft=json.loads(draft_path.read_text(encoding='utf8'))
draft['document']['sections'][2]['paragraphs'][0]=paragraphs['zh-TW']
draft['paragraph_characters']=sum(map(len,draft['document']['introduction']))+sum(len(p) for s in draft['document']['sections'] for p in s['paragraphs'])
assert 1800<=draft['paragraph_characters']<=3000
draft_path.write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
review_path=HERE/'original-review.json';review=json.loads(review_path.read_text(encoding='utf8'))
entry=next(i for i in review['originals'] if i['slug']==slug)
entry['paragraph_characters']=draft['paragraph_characters'];entry['sha256']=hashlib.sha256(json.dumps(draft['document'],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
entry['additional_edit']='Distinguished processing rate from request waiting time; editor updated and compared the corresponding paragraph in all five languages.'
review_path.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'localized-editorial-correction.json').write_text(json.dumps({'slug':slug,'id':'/document/blocks/10/text','reason':entry['additional_edit'],'paragraphs':paragraphs},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Corrected speed terminology consistently in all five locales')
