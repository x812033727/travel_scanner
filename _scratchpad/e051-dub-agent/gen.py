import json,sys
V='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e051/'
v=json.load(open(V+'video.json',encoding='utf-8'))
lines=[l for s in v['scenes'] for l in s.get('lines',[])]
T={}
T['en']="""Resisting arrest?|Resisting?
Kill her on the spot!
Go with them.
What did you say?
Fight them here,|Fight here,
and you really become a fugitive.|and you're a real fugitive.
I'll come for you.
I'll walk on my own.|I'll walk.
Mandatory mission: rescue Qin Shuang within three days.
Failure: Qin Shuang's affection resets to zero.
Xu Yan.
Keep your word.
I will.
Officer, sir,|Officer,
make me a copy of the warrant.|copy me the warrant.
And one more ingot.|One more.
Before dawn,
you never saw me.
A copy of the arrest warrant,|The warrant copy,
bought with Tang family money.|bought with Tang money.
It's on your tab,|On your tab,
pay me back slowly.
Okay,
I'll pay.
A-Ling?
Where is she?|Where?
The prefecture jail.|The jail.
We have to get her out within three days.|Three days to get her out.
From Liuxi to here,
you rode all night?
The escort agency knocked at midnight.|The escorts knocked at midnight.
I left Xiaohe with Elder Han.
One more thing,|Also,
Dad's people in the capital sent a letter.|Dad's man in the capital wrote.
A month ago, Wei Shaoqing
went back to the capital with a painter.|took a painter back to the capital.
A painter?
Who's he going to paint?|Paint who?
Here's the copy of the arrest warrant.|Here's the warrant copy.
This seal,
is fake."""
T['ja']="""逮捕に逆らう気か？|逆らうか？
その場で斬り捨てる！|斬り捨てろ！
あいつらと行け。|行け。
何ですって？
ここでやり合えば、|ここで戦えば、
本当に逃亡者になる。|逃亡者になる。
迎えに行く。
自分で歩く。
強制任務：三日以内にチン・シュアンを救出せよ。
失敗時：チン・シュアンの好感度はゼロに。
シュー・イェン。
約束は守って。
守る。
お役人さん、
逮捕状の写しを一部ちょうだい。|写しをちょうだい。
銀をもう一つ。|もう一つ。
夜が明けるまで、|夜明けまで、
私とは会っていません。|会ってませんよ。
逮捕状の写しよ、
タン家のお金で買ったの。|タン家のお金よ。
ツケにしとくね、|ツケね、
ゆっくり返して。
ああ、
返す。
アーリン？
彼女は？|どこ？
州の牢。
三日以内に救い出す。|三日で救う。
柳渓からここまで、
一晩中馬で？
鏢局が夜中に戸を叩いた。|夜中に鏢局が来た。
シャオホーはハン爺さんに預けた。|シャオホーはハン爺さんに。
それと、
都にいる父さんの人から手紙が来た。|父さんの都の人から手紙。
ウェイ・シャオチンが一か月前、|ウェイ・シャオチンが先月、
画師を連れて都に戻ったって。|画師を連れて都へ。
画師？
誰を描く気だ？|誰を描く？
これが逮捕状の写し。
この印、
偽物。"""
T['ko']="""체포에 저항하겠다?|반항해?
그 자리에서 베어라!|베어 버려!
따라가.
뭐라고?
여기서 싸우면,
진짜 도망자가 돼.
데리러 갈게.
내 발로 갈 거야.|내 발로 가.
강제 미션: 사흘 안에 친솽을 구출하라.
실패 시: 친솽 호감도 초기화.
쉬옌.
약속 지켜.
지킬게.
나리,
공문 한 부만 베껴 줘요.|공문 사본 줘요.
한 덩이 더요.|하나 더요.
날이 밝기 전까지,|날 밝기 전까지,
저를 못 보신 겁니다.|전 못 보신 겁니다.
체포 공문 사본이야,|공문 사본이야,
탕가 돈으로 샀어.
장부에 달아 둘게,|외상이야,
천천히 갚아.
그래,
갚을게.
아링?
그 사람은?|어딨어?
주 감옥.
사흘 안에 꺼내야 해.|사흘 안에 꺼내.
류시에서 여기까지,
밤새 달려온 거야?|밤새 달려왔어?
표국이 한밤중에 문을 두드렸어.|한밤에 표국이 왔어.
샤오허는 한 어르신께 맡겼어.|샤오허는 한 어르신께.
그리고,
도성에 있는 아빠 사람한테서 편지가 왔어.|도성에서 편지 왔어.
웨이사오칭이 한 달 전에,|웨이사오칭이 지난달,
화공을 데리고 도성에 돌아갔대.|화공을 데리고 갔대.
화공?
누굴 그리려고?|누굴 그려?
이게 체포 공문 사본이야.|이게 공문 사본이야.
이 도장,
가짜야."""
T['es']="""¿Te resistes al arresto?|¿Te resistes?
¡La matamos aquí mismo!|¡Mátenla aquí!
Ve con ellos.
¿Qué dijiste?
Si peleas aquí,
serás una fugitiva de verdad.|serás fugitiva.
Iré por ti.
Iré por mi cuenta.|Voy sola.
Misión obligatoria: rescatar a Qin Shuang en tres días.
Si fallas: el afecto de Qin Shuang vuelve a cero.
Xu Yan.
Cumple tu palabra.
La cumpliré.|Cumpliré.
Oficial,
hágame una copia de la orden.|una copia de la orden.
Y otro lingote.|Y otro.
Hasta que amanezca,|Hasta el alba,
usted no me ha visto.|no me vio.
La copia de la orden de arresto,|La copia de la orden,
pagada con dinero de los Tang.|con dinero Tang.
Te lo anoto en la cuenta,|Anotado,
me lo pagas con calma.|págame despacio.
Bueno,|Va,
te lo pago.|te pago.
¿A-Ling?
¿Y ella?
En la cárcel de la prefectura.|En la cárcel.
Hay que sacarla en tres días.|Tres días para sacarla.
¿De Liuxi hasta aquí,|¿Desde Liuxi,
cabalgaste toda la noche?|toda la noche?
La agencia de escoltas tocó a medianoche.|Los escoltas tocaron de noche.
Xiaohe se quedó con el anciano Han.|Xiaohe está con el anciano Han.
Y otra cosa,|Además,
llegó carta de la gente de papá en la capital.|escribió la gente de papá.
Hace un mes, Wei Shaoqing|Hace un mes, Wei Shaoqing
volvió a la capital con un pintor.
¿Un pintor?
¿A quién va a pintar?|¿Pintar a quién?
Esta es la copia de la orden de arresto.|La copia de la orden.
Este sello,
es falso."""
T['pt']="""Resistindo à prisão?|Vai resistir?
Matamos aqui mesmo!|Matem ela!
Vá com eles.|Vai com eles.
O que você disse?
Se lutar aqui,
vira fugitiva de verdade.
Eu vou te buscar.|Vou te buscar.
Eu vou sozinha.|Vou sozinha.
Missão obrigatória: resgatar Qin Shuang em três dias.
Falha: a afeição de Qin Shuang volta a zero.
Xu Yan.
Cumpra sua palavra.
Cumpro.
Seu guarda,
me faz uma cópia do mandado.|uma cópia do mandado.
E mais um lingote.|Mais um.
Até o dia nascer,|Até amanhecer,
o senhor nunca me viu.|nunca me viu.
A cópia do mandado de prisão,|A cópia do mandado,
comprada com o dinheiro dos Tang.|com dinheiro dos Tang.
Fica na conta,|Na conta,
vai pagando devagar.
Tá bom,|Tá,
eu pago.
A-Ling?
Cadê ela?|Cadê?
Na cadeia da prefeitura.|Na cadeia.
Temos três dias pra tirar ela de lá.|Três dias pra tirá-la.
Da Vila Liuxi até aqui,|De Liuxi até aqui,
você cavalgou a noite toda?|a noite toda?
A agência de escolta bateu à meia-noite.|A escolta bateu de madrugada.
Deixei Xiaohe com o Ancião Han.
E mais,
o pessoal do papai na capital mandou carta.|o pessoal do papai escreveu.
Há um mês, Wei Shaoqing
voltou à capital com um pintor.
Um pintor?
Pra pintar quem?
Esta é a cópia do mandado de prisão.|A cópia do mandado.
Este selo,
é falso."""
T['id']="""Berani melawan?
Bunuh di tempat!
Ikut mereka.
Kamu bilang apa?
Kalau bertarung di sini,|Melawan di sini,
kamu benar-benar jadi buronan.|kamu jadi buronan.
Aku akan menjemputmu.|Kujemput.
Aku jalan sendiri.
Misi wajib: selamatkan Qin Shuang dalam tiga hari.
Gagal: poin suka Qin Shuang jadi nol.
Xu Yan.
Tepati janjimu.
Kutepati.
Bang petugas,|Bang,
salinkan satu surat perintahnya untukku.|salinkan suratnya buatku.
Tambah satu keping.|Tambah satu.
Sebelum fajar,
Nona tak pernah melihat saya.|Nona tak lihat saya.
Salinan surat perintah penangkapan,|Salinan surat penangkapan,
dibeli pakai uang keluarga Tang.|dibeli uang keluarga Tang.
Kucatat di buku,|Kucatat,
bayarnya pelan-pelan.
Oke,
kubayar.
A-Ling?
Mana dia?
Penjara prefektur.|Penjara.
Dalam tiga hari harus diselamatkan.|Tiga hari harus keluar.
Dari Liuxi ke sini,
kamu berkuda semalaman?|berkuda semalaman?
Biro pengawal mengetuk pintu tengah malam.|Pengawal mengetuk tengah malam.
Xiaohe kutitipkan ke Kakek Han.
Satu lagi,|Lalu,
orang Ayah di ibu kota mengirim surat.|orang Ayah di ibu kota kirim surat.
Wei Shaoqing sebulan lalu
pulang ke ibu kota membawa seorang pelukis.|pulang ke ibu kota bawa pelukis.
Pelukis?
Dia mau melukis siapa?|Melukis siapa?
Ini salinan surat perintah penangkapan.|Ini salinan surat penangkapan.
Cap ini,
palsu."""
T['vi']="""Dám kháng cự à?
Giết tại chỗ!
Đi với họ.
Chàng nói gì?
Động thủ ở đây,
là thành kẻ trốn tội thật.|là thành tội phạm thật.
Ta sẽ đón nàng.|Ta đón nàng.
Ta tự đi.
Nhiệm vụ bắt buộc: trong ba ngày cứu Tần Sương về.
Thất bại: độ hảo cảm của Tần Sương về không.
Hứa Nghiên.
Nói phải giữ lời.
Giữ lời.
Đại ca nha dịch,|Đại ca,
chép cho ta một bản công văn.|chép cho ta công văn.
Thêm một thỏi nữa.|Thêm một thỏi.
Trước khi trời sáng,
cô nương chưa từng gặp tôi.|cô chưa gặp tôi.
Bản chép lệnh bắt,
mua bằng tiền nhà họ Đường.
Ghi sổ nhé,
chàng cứ từ từ trả.|từ từ trả.
Được,
ta trả.
A Lệnh?
Người đâu?
Ngục châu.
Trong ba ngày phải cứu ra.
Từ Liễu Khê tới đây,
cưỡi ngựa suốt một đêm sao?|cưỡi cả đêm sao?
Tiêu cục nửa đêm gõ cửa.
Tiểu Hòa giao cho Hàn bá rồi.
Còn nữa,
người của cha ở kinh thành gửi thư tới.|người của cha ở kinh gửi thư.
Ngụy Thiếu Khanh một tháng trước,
dẫn theo một họa sư về kinh rồi.
Họa sư?
Hắn định vẽ ai?
Đây là bản chép lệnh bắt.
Con ấn này,
là giả."""
T['th']="""กล้าขัดขืนหรือ?
ฆ่าทิ้งตรงนี้!
ไปกับพวกเขา|ไปกับเขา
ท่านว่าอะไรนะ?
ถ้าลงมือตรงนี้
ก็กลายเป็นผู้หลบหนีจริงๆ|ก็เป็นผู้หลบหนีจริง
ข้าจะไปรับเจ้า|ข้าจะรับเจ้า
ข้าเดินเอง
ภารกิจบังคับ: ช่วยฉินซวงกลับมาภายในสามวัน
ล้มเหลว: ค่าความชอบของฉินซวงเป็นศูนย์
สวี่เยี่ยน
พูดแล้วต้องทำ
ทำแน่
พี่เจ้าหน้าที่|พี่ชาย
คัดสำเนาหนังสือให้ข้าสักฉบับ|คัดสำเนาให้ข้าฉบับหนึ่ง
เพิ่มอีกหนึ่งก้อน|อีกก้อน
ก่อนฟ้าสาง
ท่านไม่เคยเห็นข้า
สำเนาหมายจับ
ซื้อด้วยเงินตระกูลถัง
ลงบัญชีไว้
ค่อยๆ ใช้คืนนะ
ได้
ข้าจะคืน
อาลิ่ง?
คนล่ะ?
คุกเมือง
ต้องช่วยออกมาในสามวัน
จากหลิ่วซีมาถึงนี่
ขี่ม้ามาทั้งคืนเลยหรือ?|ขี่ม้าทั้งคืนหรือ?
สำนักคุ้มภัยมาเคาะประตูตอนดึก|คุ้มภัยมาเคาะประตูตอนดึก
ฝากเสี่ยวเหอไว้กับลุงหานแล้ว
แล้วก็
คนของท่านพ่อในเมืองหลวงส่งจดหมายมา|คนของพ่อในเมืองหลวงส่งจดหมาย
เว่ยเส้าชิงเมื่อเดือนก่อน
พาจิตรกรคนหนึ่งกลับเมืองหลวง|พาจิตรกรกลับเมืองหลวง
จิตรกร?
เขาจะวาดใคร?
นี่คือสำเนาหมายจับ
ตรานี้
ของปลอม"""
for loc in (sys.argv[1:] or T):
  rows=T[loc].split('\n'); assert len(rows)==len(lines),(loc,len(rows))
  out={}
  for l,r in zip(lines,rows):
    p=r.split('|'); e={'text':p[0],'emotion':l['emotion']}
    if len(p)>1 and p[1]!=p[0]: e['say']=p[1]
    out[l['id']]=e
  open(V+'dub.%s.json'%loc,'w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
  print(loc,'written')
