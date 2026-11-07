import json
v=json.load(open('zhong-tian-qu-qi-e043/video.json'))
emo={l['id']:l['emotion'] for s in v['scenes'] for l in s.get('lines',[])}
T=[
("Kertas ini,",None),
("dia yang buat.",None),
("Kertas putih Liuxi?","Kertas Liuxi?"),
("Murid Xu Yan,",None),
("mohon Guru Besar menjamin saya.","mohon jaminan Guru."),
("Jaminan dicabut menjelang ujian,","Dicabut jelang ujian,"),
("pasti ada sebabnya.",None),
("Tintanya nggak merembes,",None),
("pembuatnya tak menipu orang.","pembuatnya tak menipu."),
("Baik.",None),
("Saya uji kau satu soal.",None),
("Kemarau tanpa hujan,",None),
("dari mana sawah dapat air?",None),
("Sungai di bawah,",None),
("sawah di atas.",None),
("Maka biarkan airnya",None),
("naik sendiri.",None),
("Liuxi membongkar balok rumah abu leluhur,","Liuxi bongkar balok rumah abu,"),
("untuk membuat kincir air ini.","jadi kincir air ini."),
("Liuxi dapat air,",None),
("ternyata karena kau.",None),
("Jaminan ini,",None),
("saya yang tanggung.",None),
("Gu-Guru Besar Cheng?","Gu-Guru Cheng?"),
("Cabut jaminan tanpa tanya alasan,","Cabut tanpa tanya alasan,"),
("begini caramu bekerja?",None),
("Hamba salah!",None),
("Segera hamba isi lagi!","Segera hamba isi!"),
("Orang Kabupaten Qingshui,","Orang Qingshui,"),
("pantas dijamin Guru Besar?","pantas dijamin Guru?"),
("Sampai jumpa di ujian.",None),
("Pakaian itu…",None),
("orang keluarga Wei.",None),
("Aku ingat kau.",None),
("Tuan,",None),
("di sini bocor.",None),
("Bilik tak bisa ditukar,",None),
("urus sendiri.",None),
("Bocor, bagus.",None),
("Aku boleh basah,",None),
("lembar ujian jangan.",None),
("Kumpulkan!",None),
("Tiga tahap ujian provinsi,","Tiga ujian provinsi,"),
("semuanya selesai.",None),
("Kabupaten Qingshui,",None),
("Xu Yan.",None),
("Karangan bagus.",None),
("Sayang sekali.",None),
("Mulai hari ini,",None),
("namamu Wei Xun.",None),
]
out={}
for i,(t,s) in enumerate(T,1):
    k=f"zq43a{i:02d}"; e={"text":t,"emotion":emo[k]}
    if s: e["say"]=s
    out[k]=e
assert set(out)==set(emo)
open('zhong-tian-qu-qi-e043/dub.id.json','w').write(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
p='series-plans/zhong-tian-qu-qi/production/hailuo/youtube-locales/id.json'
d=json.load(open(p))
d['episodes']['43']={"title":"Bertani, Beristri, Berkuasa Episode 43 | Sub Indo","description":"Ujian tinggal dua hari, dan jaminan Xu Yan dicabut seseorang. Tang Xiaotang meletakkan setumpuk kertas putih Liuxi ke meja Guru Besar Cheng, kepala akademi di kota provinsi: \"Kertas ini, dia yang buat.\" Guru Besar Cheng mengujinya soal mengatasi kemarau, dan Xu Yan mengambil kuas lalu menggambar kincir air: sungai di bawah, sawah di atas, maka biarkan airnya naik sendiri. Liuxi membongkar balok rumah abu leluhur untuk membuat kincir air ini. Guru Besar Cheng langsung menjadi penjaminnya, bahkan memarahi juru tulis yang mencabut jaminan itu di depan meja pendaftaran. Di hari ujian, di depan gerbang balai ujian, Tang Xiaotang melihat Penguji Feng menerima selembar kertas terlipat dari seorang pelayan berpakaian keluarga Wei, lalu menyelipkannya ke dalam lengan bajunya. Bilik ujian bocor, dan Xu Yan melindungi lembar ujiannya dengan tubuhnya sampai tiga tahap ujian selesai. Larut malam di ruang segel, Penguji Feng menarik keluar lembar ujian Xu Yan. \"Bertani, Beristri, Berkuasa\" — Episode 43."}
open(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
