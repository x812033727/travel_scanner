import pathlib,json
out=pathlib.Path('/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/dyson');r=json.loads((out/'author-rows.json').read_text())
def change(old,new):
 x=next(x for x in r if x['text']==old);x['text']=new
change('換成你要讓生產繼續，我也會問：把粉末抽走，為什麼反而添一個堵塞？','換成你要讓生產繼續，我也會問：要把粉末收住，該換哪一種裝置？')
a=next(i for i,x in enumerate(r) if x['text'].startswith('戴森回憶，問到工業氣旋'));b=next(i for i,x in enumerate(r) if x['text'].startswith('官網還記下，他去看過'));v=r.pop(b);r.insert(a,v)
change('兩人都做過製造，這次想讓授權方接下後面的生產。','兩人都做過製造，這次希望由取得授權的廠商接下生產。')
change('後來確實有英國授權商接手，做出Cyclon。','後來，英國一家取得授權的廠商，確實做出Cyclon。')
change('後來他決定自己製造，模具、場地和組裝，又得由自己安排。','要走到開場那批零件圖，還差自家製造需要的資金和場地。')
change('有資金做模具以後，誰把零件圖交給製造的人，誰又把零件接回來組好？','錢能買模具，開場卻還缺組裝的人；這件事，要先找到哪一個落腳處？')
change('戴森在訪談裡說，那家做成型零件的供應商，工廠有半邊閒著。','開場那四個人，從成型供應商那裡找到一個機會：對方的工廠，有半邊閒著。')
change('接著還得聘一個管理組裝線的人，再聘實際負責組裝的工人。','開場問的組裝，最後還得另外聘線長，再聘真正上線組裝的工人。')
change('他回憶，雙方是按這種條件達成交易，沒有在那段話給出確切日期。','戴森說，雙方是按這個條件達成交易。')
remove=[
'倒空能移走袋裡的垃圾，卻沒有把那層堵塞一起移走。',
'我喜歡這裡能指認的工作：有一個加進去的部件，也有要拿來試的形狀。',
'開場那四個人找不到的組裝工作，最後從成型供應商那裡，找到一個空間的辦法。',
'這裡補上的，是場地和人，不是把完成的圖面直接算成能交的貨。',
'我覺得租半座現成空間這一步很具體，你可以省掉先買整廠，卻不能省掉組裝能力。',
'這個工作，是把解說留在售點，讓產品旁邊有能供顧客理解的內容。',
'這不是替前一家郵購買手補一份訂單，而是初期英國通路裡，另一段交涉的記錄。'
]
r=[x for x in r if x['text'] not in remove]
(out/'author-rows.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
