import json,sys
R='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e047/'
v=json.load(open(R+'video.json'))
ids=[l['id'] for s in v['scenes'] for l in s.get('lines',[])]
em={l['id']:l['emotion'] for s in v['scenes'] for l in s.get('lines',[])}
def P(s):
  out=[]
  for line in s.strip().split('\n'):
    parts=[p.strip() for p in line.split('|')]
    out.append((parts[0], parts[1] if len(parts)>1 and parts[1] else None))
  return out
D={}
D['en']=P('''
The waterwheel in part three,
you draw it.
D-Draw…|Draw…
Draw what?
Ahem,
Nonsense!
Beat him!
Wait.
Give them paper.
You memorized the words,|You know the words,
but the waterwheel?|And the wheel?
Twelve blades,
angled three degrees.
Correct,|Yes,
that's the one.
Wei Xun,
where's your waterwheel?|your waterwheel?
The blades,|Blades,
why mount them backward?|why backward?
I…
What I memorized…|I memorized…
Memorized?
Memorized from whom?|From whom?
The first time, I put them in backward,
and the wheel wouldn't turn.
My little sister held up a pinwheel,|My sister's pinwheel,
and then I flipped them around.|then I flipped them.
Before the exam,
in my study,
he drew this very wheel.|he drew this one.
Ahem,|Hm,
A scholar reciting his texts,
what's so odd about that!
My lord!
This humble woman has something to present!|I have something to present!
That man from the Wei family,|That Wei man,
came to see Examiner Feng again.
This is the second packet,
I took it off his hands.|I took it.
Five hundred taels,
paid in full when the results are posted.|paid when the list's posted.
I know this seal,
Wei Shaoqing's steward.
My lord,
I've been wronged…
Seize him!
Leave us.
Accuse the Wei family,|Accuse the Weis,
and the case goes to the capital.
Three years with no verdict,
and your exam year is lost.
Try only Examiner Feng,
and tomorrow,
you're Jieyuan, first in the province.|you're Jieyuan.
Choice: bring down the Wei clan,
or take Jieyuan first.
''')
D['ja']=P('''
第三段の水車を、
描いてみろ。
か、描く……|描く……
何を描けと？
ゴホン、
ふざけるな！
打ち据えろ！|打て！
待て。
紙を与えよ。
文は暗記できても、|字は覚えても、
水車は？
羽根板は十二枚、
三分傾けて。|斜め三分。
そうだ、
この水車だ。
ウェイ・シュン、
お前の水車は？
羽根板は、|羽根、
なぜ逆に付けた？
俺……
俺が覚えたのは……|覚えたのは……
覚えた？
誰のを？
最初は逆に付けて、
水車が回らなかった。
妹が風車で示してくれて、|妹の風車を見て、
やっと裏返した。
試験の前、
わしの書斎で
この水車を描いた。
ゴホン、
書生が書を覚えたとて、
何が珍しい！
閣下！
献上したい物がございます！|献上の品が！
あのウェイ家の者が、|ウェイ家の者が、
またフォン学正に会いに。
これが二つ目、
代わりに受け取りました。|預かりました。
五百両、
合格発表で全額支払い。|発表後に全額。
この印、存じております、|この印、存じます、
ウェイ・シャオチンの執事です。|ウェイ・シャオチンの執事。
閣下、
私は冤罪で……
捕らえよ！
下がれ。
ウェイ家を訴えれば、
この件は都へ送られる。
三年は片づかず、
お前の今回の受験は消える。|今回の受験は消える。
フォン学正だけ裁けば、
お前は明日、
解元だ。
選択：ウェイ家を倒す、
または先に解元を取る。
''')
D['ko']=P('''
셋째 단락의 수차,|셋째 단락 수차,
네가 그려 봐.|그려 봐.
그, 그려……|그려……
뭘 그려?
에헴,
터무니없다!|헛소리!
매우 쳐라!
잠깐.
종이를 줘라.
글은 외워도,
수차는?
날개판 열두 장,
삼 푼 기울여.
맞아,
바로 이 수차야.
웨이쉰,
네 수차는?
날개판,
왜 거꾸로 달았나?
나……
내가 외운 건……|외운 건……
외운 거라고?|외워?
누구 걸?
처음엔 거꾸로 달아서,
수차가 안 돌았죠.
여동생이 바람개비로 보여 줘서,|동생 바람개비 보고,
그제야 뒤집었죠.
시험 전에,
내 서재에서
이 수차를 그렸소.
에헴,
서생이 글을 외운 게,
뭐가 대수란 말이오!
나리!
바칠 물건이 있사옵니다!|바칠 것이 있습니다!
그 웨이 가 사람이,|웨이 가 사람이,
또 펑 학정을 찾아왔어요.
두 번째 꾸러미예요,
제가 대신 받았죠.|대신 받았죠.
오백 냥,
방이 붙으면 완납.
이 도장, 제가 알아요,|이 도장 알아요,
웨이사오칭의 집사예요.|웨이사오칭 집사.
나리,
소관은 억울……
잡아라!
다 물러가라.|물러가라.
웨이 가를 고발하면,|웨이 가 치면,
사건은 도성으로 가네.
삼 년은 안 끝나고,
자네 이번 시험은 끝일세.|이번 시험은 끝일세.
펑 학정만 처벌하면,
자네는 내일,|자넨 내일,
해원일세.
선택: 웨이 가를 무너뜨린다,
혹은 먼저 해원을 얻는다.
''')
D['es']=P('''
La noria del tercer párrafo:|La noria del párrafo tres,
dibújala tú.
Di-dibujar…|¿Dibujar…?
¿Dibujar qué?
Ejem,
¡Tonterías!|¡Absurdo!
¡Azótenlo!
Alto.
Denles papel.
El texto, se lo aprendió,|El texto, sí,
¿y la noria?
Doce paletas,
inclinadas tres grados.|tres grados.
Exacto,
esa es la noria.
Wei Xun,
¿y tu noria?
Las paletas,|Paletas:
¿por qué al revés?
Yo…
Lo que memoricé…|Yo memoricé…
¿Memorizaste?
¿De quién?
La primera vez las puse al revés,
y la noria no giró.
Mi hermanita lo comparó con un rehilete,|Mi hermana usó un rehilete,
y por fin las volteé.
Antes del examen,
en mi estudio
dibujó esta noria.
Ejem,
Un letrado que memoriza textos,
¡qué tiene de raro!
¡Señoría!|¡Señor!
¡Esta humilde mujer trae algo que presentar!|¡Traigo algo!
Ese hombre de los Wei|El de los Wei
volvió a buscar al examinador Feng.|volvió a ver a Feng.
Este es el segundo paquete,|Es el segundo paquete,
lo recibí por él.|lo recibí yo.
Quinientos taeles,
pagaderos al publicarse la lista.|a pagar con la lista.
Conozco este sello:
es del mayordomo de Wei Shaoqing.
Señoría,|Señor,
Este funcionario es inocente…
¡Arréstenlo!
Retírense.
Si acusas a los Wei,
el caso irá a la capital.
Tres años sin sentencia,
y pierdes este examen.
Juzga solo al examinador Feng,|Juzga solo a Feng,
y mañana
serás el primero del examen provincial.|serás el primero.
Elección: derribar a los Wei,
o ser el primero del examen provincial antes.|o quedar primero antes.
''')
D['pt']=P('''
A roda d'água da terceira parte,|A roda d'água, parte três,
desenha aí.
De-desenhar…|Desenhar…
Desenhar o quê?
Hum,
Absurdo!
Batam nele!
Espere.
Deem papel a eles.|Deem papel.
O texto ele decorou,|Texto, sim,
e a roda d'água?|e a roda?
Doze pás,
inclinadas três graus.|três graus.
Isso,
é essa mesma.
Wei Xun,
e a sua roda d'água?|e a sua roda?
As pás,
por que ao contrário?
Eu…
O que eu decorei…|Eu decorei…
Decorou?
De quem?
Na primeira vez, montei ao contrário,|Primeiro montei ao contrário,
e a roda não girou.
Minha irmãzinha mostrou com um cata-vento,|Minha irmã e um cata-vento,
e só então eu virei as pás.|aí eu virei.
Antes do exame,
no meu escritório
ele desenhou esta roda.
Hum,
Um letrado decorar textos,
o que tem de mais!
Excelência!|Senhor!
Tenho algo a entregar!
Aquele homem dos Wei|O homem dos Wei
veio de novo atrás do Examinador Feng.|voltou a ver o Feng.
Este é o segundo pacote,
eu recebi por ele.|recebi eu.
Quinhentos taéis,
pagos quando sair a lista.|pagos com a lista.
Conheço este selo,
é do mordomo de Wei Shaoqing.|mordomo de Wei Shaoqing.
Excelência,|Senhor,
Este servidor é inocente…
Prendam-no!
Saiam.
Se acusar os Wei,
o caso vai para a capital.
Três anos sem sentença,
e o seu exame deste ano já era.|e seu exame já era.
Puna só o Examinador Feng,|Puna só o Feng,
e amanhã
você é o primeiro do exame provincial.|você é o primeiro.
Escolha: derrubar os Wei,
ou ser o primeiro do exame provincial antes.|ou ser o primeiro antes.
''')
D['id']=P('''
Kincir air di bagian ketiga,|Kincir air bagian tiga,
coba kamu gambar.|gambar sana.
Gam-gambar…|Gambar…
Gambar apa?
Ehem,
Omong kosong!|Ngawur!
Pukul dia!
Tunggu.
Beri mereka kertas.|Beri kertas.
Tulisan bisa dihafal,|Hafal tulisan,
kincir airnya?|kincirnya?
Dua belas bilah,
miring tiga derajat.|tiga derajat.
Benar,
persis yang ini.
Wei Xun,
mana kincir airmu?|mana kincirmu?
Bilahnya,|Bilah,
kenapa dipasang terbalik?|kenapa terbalik?
Aku…
Yang kuhafal itu…|Kuhafal…
Hafalan?
Hafalan siapa?
Pertama kali kupasang terbalik,
kincirnya tidak berputar.|kincirnya diam.
Adikku menunjukkannya dengan kincir kertas,|Lihat kincir kertas adikku,
baru aku membaliknya.|baru kubalik.
Sebelum ujian,
di ruang bacaku
dia menggambar kincir ini.|dia menggambar ini.
Ehem,
Pelajar menghafal teks,
apa anehnya!
Tuan!
Hamba ingin menyerahkan sesuatu!|Hamba bawa sesuatu!
Orang keluarga Wei itu|Orang Wei itu
datang lagi menemui Penguji Feng.|datangi Penguji Feng lagi.
Ini bungkusan kedua,
aku yang menerimanya untuknya.|kuterima.
Lima ratus tael,
lunas saat pengumuman.
Aku kenal cap ini,
milik pengurus rumah Wei Shaoqing.|pengurus Wei Shaoqing.
Tuan,
Hamba difitnah…
Tangkap dia!
Keluar semua.|Keluar.
Kalau menyeret keluarga Wei,|Seret keluarga Wei,
kasusnya dibawa ke ibu kota.
Tiga tahun tak selesai,
ujian angkatanmu ini hangus.
Cukup adili Penguji Feng,|Adili Feng saja,
dan besok,
kamu juara pertama ujian provinsi.|kamu juara pertama.
Pilihan: jatuhkan keluarga Wei,
atau ambil juara pertama dulu.
''')
D['vi']=P('''
Guồng nước đoạn thứ ba,
ngươi vẽ ra đi.
V-vẽ…|Vẽ…
Vẽ cái gì?
E hèm,
Hồ đồ!
Đánh cho ta!
Khoan đã.
Đưa giấy cho họ.
Chữ thì thuộc được,
còn guồng nước?
Mười hai cánh guồng,
nghiêng ba phân.
Đúng vậy,
chính là cái này.
Ngụy Tuân,
guồng nước của ngươi đâu?|guồng của ngươi đâu?
Cánh guồng,
sao lại lắp ngược?
Ta…
Ta thuộc là…
Thuộc?
Thuộc của ai?
Lần đầu lắp ngược,
guồng không quay.
Muội muội ta lấy chong chóng ra so,|Muội ta lấy chong chóng so,
ta mới lật lại.
Trước kỳ thi,
ở thư phòng lão phu
hắn đã vẽ cái này.
E hèm,
Thư sinh học thuộc,
có gì lạ đâu!
Đại nhân!
Dân nữ có vật dâng lên!
Kẻ nhà họ Ngụy đó,
lại đến tìm Phùng đại nhân.
Đây là gói thứ hai,
ta nhận giùm hắn.|ta nhận giùm.
Năm trăm lượng,
có bảng thì trả đủ.
Con dấu này ta nhận ra,
là của quản gia Ngụy Thiếu Khanh.|quản gia Ngụy Thiếu Khanh.
Đại nhân,
Hạ quan oan…
Bắt lấy!
Lui hết đi.
Kiện đến nhà họ Ngụy,|Kiện nhà Ngụy,
vụ án phải đưa lên kinh thành.
Ba năm không xong,
khoa này của ngươi coi như mất.|khoa này ngươi mất.
Chỉ xử Phùng học chính,
ngươi ngày mai,
chính là giải nguyên.
Lựa chọn: lật đổ nhà họ Ngụy,
hoặc lấy giải nguyên trước.
''')
D['th']=P('''
กังหันน้ำในตอนที่สาม|กังหันน้ำตอนสาม
เจ้าวาดออกมา
ว-วาด…|วาด…
วาดอะไร?
อะแฮ่ม
เหลวไหล!
ตีมัน!
ช้าก่อน
ให้กระดาษพวกเขา|เอากระดาษมา
ตัวอักษรท่องได้
แล้วกังหันน้ำล่ะ?|กังหันล่ะ?
ใบพัดสิบสองใบ
เอียงสามส่วน
ถูกต้อง
ก็คือตัวนี้
เว่ยสวิน
กังหันน้ำของเจ้าล่ะ?|กังหันของเจ้าล่ะ?
ใบพัด
ทำไมติดกลับด้าน?
ข้า…
ที่ข้าท่องมา…|ข้าท่อง…
ท่อง?
ท่องของใคร?
ครั้งแรกติดกลับด้าน
กังหันไม่หมุน
น้องสาวข้าเอากังหันลมมาเทียบ|น้องสาวเอากังหันลมเทียบ
ข้าถึงพลิกกลับ
ก่อนสอบ
ที่ห้องหนังสือของข้า
เขาวาดตัวนี้ไว้
อะแฮ่ม
บัณฑิตท่องหนังสือ
มีอะไรแปลก!
ใต้เท้า!
ข้าน้อยมีของจะถวาย!
คนตระกูลเว่ยคนนั้น|คนตระกูลเว่ย
มาหาผู้คุมสอบเฝิงอีกแล้ว
นี่ห่อที่สอง
ข้ารับไว้แทนเขา|ข้ารับแทน
ห้าร้อยตำลึง
จ่ายครบเมื่อประกาศผล
ตรานี้ข้าจำได้
พ่อบ้านของเว่ยเส้าชิง|พ่อบ้านเว่ยเส้าชิง
ใต้เท้า
ข้าน้อยถูกใส่ร้าย…
จับไว้!
ออกไปให้หมด|ออกไป
ถ้าฟ้องถึงตระกูลเว่ย|ฟ้องตระกูลเว่ย
คดีต้องส่งเมืองหลวง
สามปีไม่จบ
รุ่นสอบของเจ้าก็หมดกัน
ลงโทษแค่ผู้คุมสอบเฝิง
พรุ่งนี้เจ้า
ก็คือผู้สอบได้ที่หนึ่งระดับมณฑล|ก็ได้ที่หนึ่ง
ทางเลือก: โค่นตระกูลเว่ย
หรือคว้าที่หนึ่งระดับมณฑลก่อน|หรือคว้าที่หนึ่งก่อน
''')
for loc in (sys.argv[1:] or D):
  rows=D[loc]; assert len(rows)==len(ids),(loc,len(rows))
  out={}
  for i,(t,s) in zip(ids,rows):
    e={'text':t,'emotion':em[i]}
    if s and s!=t: e['say']=s
    out[i]=e
  open(R+f'dub.{loc}.json','w').write(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
  print(loc,'written')
