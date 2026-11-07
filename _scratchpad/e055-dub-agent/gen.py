# usage: python3 gen.py <locale>  -> writes dub.<locale>.json from LINES[locale]
import json, sys
R='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e055'
v=json.load(open(R+'/video.json'))
ids=[l for s in v['scenes'] for l in s.get('lines',[])]
L={}
def add(loc, rows):
    L[loc]=[r.split(' || ') for r in rows.strip('\n').split('\n')]
add('en','''What I want is there.
A home.
A-Ling, affection: sixty-one.
What kind of answer is that… || Some answer…
All three wives' affection
has passed sixty.
Grand prize unlocked.
Grand prize: the gunpowder formula.
Gunpowder…
With this,
who'd dare take my family?
But it can also || But it can
kill a lot of people.
Seal it.
Not even I will open it. || Even I won't open it.
Seal confirmed.
What are you thinking?
Something that could kill a lot of people. || Something that kills many.
Locked, for now. || Locked for now.
Keep it locked. || Lock it.
What a welcome, || Look at this,
livelier than the prefecture city! || livelier than the city!
Our Liuxi
has produced a Jieyuan! || has a Jieyuan!
Brother!
Sister A-Ling said
you'd come back for sure! || you'd come back!
Sister A-Ling!
H-Honored Jieyuan…
Squire Qian,
that kowtow you promised— || that kowtow—
I-I…
Forget it.
A bow will do.
This account,
is finally settled.
Brother,
what's a Jieyuan?
It means from now on, || It means
no one will dare pick on you. || no one picks on you.
Miss Tang!
Urgent letter from the capital!
Wei Shaoqing…
took a portrait
into the chancellor's mansion. || to the chancellor's.''')
add('ja','''そこに、欲しいものがある。 || 欲しいものがある。
家族だ。
アーリン、好感度、六十一。
何よ、その答え…… || 何それ……
三人の妻の好感度、
全員、六十を突破。
大賞、解放。
大賞：火薬の調合法。
火薬……
これがあれば、 || これで、
誰も家族に手を出せない。 || 家族に手は出させない。
でもこれは、
大勢を殺せる。
封印。
俺自身も開けない。 || 俺も開けない。
封印を確認。
何を考えてるの？ || 何考えてるの？
大勢を殺せるもの。
しばらく、しまっとく。 || しまっとく。
固く封じて。 || 封じて。
この騒ぎ、
州城よりにぎやかね。 || 州城より派手ね。
わしらの柳渓から、
解元が出たぞ！
お兄ちゃん！
アーリンお姉ちゃんがね、
絶対帰ってくるって！
アーリンお姉ちゃん！
か、解元様……
チエン旦那、
約束の土下座は——
わ、わしは……
いいさ。
お辞儀で十分だ。 || 礼だけでいい。
この勘定、
やっと片付いた。
お兄ちゃん、
解元ってなに？
これからはね、
誰にもいじめさせないってこと。 || 誰にもいじめさせない。
タンお嬢様！
都から急ぎの手紙です！ || 都から急ぎの文！
ウェイ・シャオチンが……
一枚の肖像画を持って、 || 肖像画を持って、
相府に入った。''')
add('ko','''거기 내가 원하는 게 있어. || 원하는 게 있어.
가족.
아링 호감도, 육십일.
그게 무슨 대답이야…… || 무슨 대답이야……
세 부인의 호감도,
모두 육십 돌파.
대상 잠금 해제.
대상: 화약 제조법.
화약……
이게 있으면,
누가 감히 내 가족을 잡아가. || 누가 내 가족을 건드려.
하지만 이건,
많은 사람을 죽일 수 있어. || 많이 죽일 수 있어.
봉인.
나조차 열지 않아. || 나도 안 열어.
봉인 확인.
무슨 생각 해?
많은 사람을 죽일 수 있는 것. || 사람을 많이 죽일 물건.
일단 잠가 둘게. || 잠가 둘게.
잘 잠가.
이 난리,
주성보다 더 떠들썩하네. || 주성보다 요란하네.
우리 류시에서,
해원이 났다!
오빠!
아링 언니가 그랬어,
오빠 꼭 돌아온다고! || 꼭 돌아온다고!
아링 언니!
해, 해원 나리……
첸 나리,
약속한 절은——
저, 저는……
됐소.
읍이나 한 번 하쇼. || 읍만 하쇼.
이 장부,
드디어 다 맞췄네. || 드디어 끝났네.
오빠,
해원이 뭐야?
앞으로는,
아무도 널 못 괴롭힌다는 거야. || 아무도 널 못 괴롭혀.
탕 아가씨!
도성에서 급한 서신입니다! || 도성 급보입니다!
웨이사오칭이……
초상화 한 폭을 들고, || 초상화를 들고,
상부에 들어갔대.''')
add('es','''Ahí está lo que quiero.
Un hogar.
A-Ling, afecto: sesenta y uno.
Vaya respuesta…
Afecto de las tres esposas:
todas pasan de sesenta.
Gran premio desbloqueado.
Gran premio: la fórmula de la pólvora.
Pólvora…
Con esto,
¿quién se atreverá a llevarse a mi familia? || ¿quién toca a mi familia?
Pero también puede
matar a mucha gente.
Sellar.
Ni yo mismo lo abriré. || Ni yo lo abro.
Sellado confirmado.
¿En qué piensas?
En algo que puede matar a mucha gente. || Algo que mata a muchos.
Por ahora, bajo llave. || Bajo llave.
Ciérralo bien. || Ciérralo.
Este recibimiento, || Qué fiesta,
¡más animado que la ciudad de la prefectura! || ¡más que en la ciudad!
¡Nuestro Liuxi
tiene al primero del examen provincial! || tiene al primero del examen!
¡Hermano!
La hermana A-Ling dijo
¡que seguro volverías! || ¡que volverías!
¡Hermana A-Ling!
I-ilustre primero del examen… || E-excelencia…
Don Qian,
lo de arrodillarse que prometió… || ¿y lo de arrodillarse?
Y-yo…
Olvídelo.
Con una reverencia basta. || Basta una reverencia.
Esta cuenta,
por fin quedó saldada.
Hermano,
¿qué es el primero del examen provincial? || ¿qué es ser el primero?
Significa que, de ahora en adelante, || Que ahora
nadie se atreverá a molestarte. || nadie te molesta.
¡Señorita Tang!
¡Carta urgente de la capital!
Wei Shaoqing…
llevó un retrato
a la mansión del canciller.''')
add('pt','''Lá está o que eu quero.
Um lar.
A-Ling, afeição: sessenta e um. || A-Ling: sessenta e um.
Que resposta é essa… || Que resposta…
Afeição das três esposas:
todas acima de sessenta.
Grande prêmio desbloqueado.
Grande prêmio: a fórmula da pólvora.
Pólvora…
Com isso,
quem vai ousar levar minha família? || quem leva minha família?
Mas também pode
matar muita gente.
Lacrar.
Nem eu mesmo vou abrir. || Nem eu abro.
Lacre confirmado.
No que está pensando? || Pensando em quê?
Numa coisa que mata muita gente. || Algo que mata muitos.
Por ora, trancado. || Fica trancado.
Tranque bem.
Que recepção,
mais animada que a cidade da província! || mais que na cidade!
Nossa Liuxi
tem o primeiro do exame provincial! || tem o primeiro do exame!
Mano!
A A-Ling disse
que você ia voltar!
A-Ling!
Ex-Excelência…
Senhor Qian,
o ajoelhar que combinamos— || e o ajoelhar?—
E-eu…
Deixa pra lá.
Uma reverência basta.
Essa conta,
enfim fechou.
Mano,
o que é o primeiro do exame provincial? || o que é ser o primeiro?
Quer dizer que, daqui pra frente, || Que agora
ninguém vai ousar mexer com você. || ninguém mexe com você.
Senhorita Tang!
Carta urgente da capital!
Wei Shaoqing…
levou um retrato
à mansão do chanceler.''')
add('id','''Di sana ada yang kuinginkan.
Sebuah keluarga. || Keluarga.
Poin suka A-Ling, enam puluh satu. || A-Ling, enam puluh satu.
Jawaban macam apa itu… || Jawaban apa itu…
Poin suka ketiga istri
semuanya tembus enam puluh. || tembus enam puluh.
Hadiah utama terbuka.
Hadiah utama: resep mesiu.
Mesiu…
Dengan ini,
siapa berani menangkap keluargaku? || siapa berani tangkap keluargaku?
Tapi ini juga bisa
membunuh banyak orang.
Segel.
Aku sendiri pun tak akan membukanya. || Aku pun tak buka.
Segel dikonfirmasi.
Kau memikirkan apa? || Mikir apa?
Sesuatu yang bisa membunuh banyak orang. || Yang bisa bunuh banyak orang.
Kukunci dulu.
Kunci baik-baik. || Kunci rapat.
Meriah begini, || Wah,
lebih ramai dari kota prefektur. || lebih ramai dari kota.
Liuxi kita
punya juara pertama ujian provinsi! || punya juara pertama!
Kakak!
Kak A-Ling bilang,
Kakak pasti pulang!
Kak A-Ling!
Tu-Tuan Juara…
Tuan Qian,
sujud yang dijanjikan— || sujudnya—
Sa-saya…
Tak usah.
Membungkuk saja cukup. || Cukup membungkuk.
Hitungan ini,
akhirnya lunas juga. || akhirnya lunas.
Kakak,
juara pertama ujian provinsi itu apa? || juara pertama itu apa?
Artinya mulai sekarang, || Artinya,
tak ada yang berani menindasmu. || tak ada yang berani ganggu.
Nona Tang!
Surat kilat dari ibu kota!
Wei Shaoqing…
membawa sebuah potret,
masuk ke kediaman perdana menteri. || ke rumah perdana menteri.''')
add('vi','''Ở đó có thứ ta muốn.
Một mái nhà.
A Lệnh hảo cảm, sáu mươi mốt.
Trả lời gì kỳ vậy… || Đáp gì vậy…
Hảo cảm ba vị thê tử,
toàn bộ vượt sáu mươi.
Mở khóa đại thưởng.
Đại thưởng: công thức thuốc súng.
Thuốc súng…
Có nó rồi,
ai còn dám bắt người nhà ta.
Nhưng nó cũng có thể
khiến rất nhiều người chết.
Niêm phong.
Đến chính ta cũng không mở. || Ta cũng không mở.
Xác nhận niêm phong.
Ngươi đang nghĩ gì?
Thứ có thể giết rất nhiều người.
Tạm khóa lại đã.
Khóa kỹ vào.
Khí thế này,
còn náo nhiệt hơn châu thành.
Liễu Khê chúng ta,
có giải nguyên rồi!
Ca!
A Lệnh tỷ tỷ nói,
ca nhất định sẽ về!
A Lệnh tỷ tỷ!
Giải, giải nguyên lão gia…
Tiền lão gia,
cái dập đầu đã hứa——
Tôi, tôi…
Miễn đi.
Vái một cái là được.
Món nợ này,
cuối cùng cũng tính xong.
Ca,
giải nguyên là gì?
Là từ nay về sau,
không ai dám bắt nạt muội.
Đường tiểu thư!
Thư khẩn từ kinh thành!
Ngụy Thiếu Khanh…
mang theo một bức họa,
vào tướng phủ.''')
add('th','''ตรงนั้นมีสิ่งที่ข้าต้องการ
ครอบครัว
อาลิ่ง ค่าความชอบ หกสิบเอ็ด
นี่มันคำตอบอะไรกัน… || คำตอบอะไรกัน…
ค่าความชอบของภรรยาทั้งสาม
ทะลุหกสิบทั้งหมด
ปลดล็อกรางวัลใหญ่
รางวัลใหญ่: สูตรดินปืน
ดินปืน…
มีมันแล้ว
ใครจะกล้ามาจับครอบครัวข้า || ใครจะกล้าจับคนของข้า
แต่มันก็ทำให้
คนตายได้มากมาย
ผนึก
แม้แต่ข้าเองก็จะไม่เปิด || ข้าเองก็ไม่เปิด
ยืนยันการผนึก
คิดอะไรอยู่?
สิ่งที่ฆ่าคนได้มากมาย
ล็อกไว้ก่อน
ล็อกให้ดี
ขบวนแบบนี้
คึกคักกว่าในเมืองอีก
หลิ่วซีของพวกเรา
มีผู้สอบได้ที่หนึ่งแล้ว! || มีคนได้ที่หนึ่งแล้ว!
พี่!
พี่อาลิ่งบอกว่า
พี่ต้องกลับมาแน่!
พี่อาลิ่ง!
ท่าน ท่านผู้สอบได้ที่หนึ่ง… || ใ-ใต้เท้า…
เศรษฐีเฉียน
ที่สัญญาไว้ว่าจะโขกหัว—— || เรื่องโขกหัว——
ข้า ข้า…
ไม่ต้องแล้ว
คารวะสักทีก็พอ
บัญชีนี้
ในที่สุดก็คิดเสร็จ
พี่
ผู้สอบได้ที่หนึ่งคืออะไร? || ที่หนึ่งคืออะไร?
ก็คือต่อไปนี้
ไม่มีใครกล้ารังแกเจ้า
คุณหนูถัง!
จดหมายด่วนจากเมืองหลวง!
เว่ยเส้าชิง…
ถือภาพวาดหนึ่งภาพ || ถือภาพวาดไป
เข้าจวนอัครเสนาบดี''')
loc=sys.argv[1]
rows=L[loc]; assert len(rows)==len(ids),(loc,len(rows),len(ids))
out={}
for l,r in zip(ids,rows):
    e={'text':r[0].strip(),'emotion':l['emotion']}
    if len(r)>1 and r[1].strip()!=r[0].strip(): e['say']=r[1].strip()
    out[l['id']]=e
p=f'{R}/dub.{loc}.json'
import os
if os.path.exists(p) and '--force' not in sys.argv: print('exists, skip',p); sys.exit()
open(p,'w').write(json.dumps(out,ensure_ascii=False,indent=2)+'\n'); print('wrote',p)
