# P15 salty sea: decisions on the dub lines the speech check flagged

Only `lines[<id>].text` was edited in `docs/videos/sothatswhy-p15-salty-sea/i18n/<locale>.json`. No new line is longer than the old one (counted in code points).

## en (1 flagged: 1 REWORD)
- p115 REWORD: "the sea keeps removing too?" -> "the sea takes it out too?". The recognizer heard "seat keeps moving". "removing" blurs into the word before it, and the new wording is plainer for a child.

## ja (4 flagged: all KEEP)
- p023 KEEP: 舌じゃわからないの。 The recognizer wrote 下 for 舌. Both are read した.
- p073 KEEP: 毎日煮られたら、 The recognizer wrote 煮 in kana (にられたら), so the reading was correct.
- p127 KEEP: …場所ごとに火と水が違うの。 The recognizer wrote 陽 for 火. Both are read ひ.
- p135 KEEP: よく煮つまって、紅海はしょっぱい。 The recognizer wrote 後悔 for 紅海. Both are read こうかい, and the Red Sea is on screen.

## ko (8 flagged: 5 REWORD, 3 KEEP)
- p051 KEEP: 붓는 건 맞아, The recognizer heard 붙는. Both are pronounced [분는].
- p077 KEEP: 머물다 끓어 나가. 끓어 and 끌어 sound the same, and the mismatch is tiny (Jev 0.03).
- p098 REWORD: "껍데기엔 소금이 안 쓰여서." -> "껍데기엔 소금이 안 들어가.". The recognizer heard 안 스며서 ("doesn't soak in"), which changes the meaning. 들어가 is clear.
- p111 REWORD: "한 길은 가장자리야. …" -> "하나는 가장자리야. …". The recognizer heard 한기는. 한 길은 runs together when spoken and is awkward. 하나는 is clear.
- p114 REWORD: "강이 보낸 소금을" -> "강이 넣은 소금을". The recognizer heard 보는 ("sees"). 넣은 matches p156 (강이 소금 조금 넣고).
- p135 REWORD: "세게 끓어 더 짜," -> "많이 졸아 더 짜,". The recognizer heard 세 개 ("three"). 졸아 ("boiled down") matches 졸아든 in p111.
- p151 REWORD: "해안은 좀 싱거워." -> "바닷가는 덜 짜.". The recognizer heard "해야는 좀 싱거", with the end of the line cut off. 바닷가 is the more familiar word for a child, and the new line is shorter.
- p156 KEEP: 강이 소금 조금 넣고, The recognizer heard 탕에, a slip on the first sound in a soup context (Jev 0.07).

## pt (4 flagged: 1 REWORD, 3 KEEP)
- p004 KEEP: "Já provei também," The recognizer heard "Já aproveitam bem", which sounds almost the same.
- p081 KEEP: "Nem o sal fica pra sempre." The recognizer heard "sol" and wrote "para". The next line ("E pra onde vai o sal?") makes the meaning clear.
- p147 KEEP: "Nem um, nem outro." The recognizer heard "Nenhum".
- p151 REWORD: "e a costa dilui." -> "e a costa adoça.". The recognizer produced nonsense ("colchetes, Louis"). "dilui" is an uncommon word for a child, while água doce ("fresh water") is a familiar idea.

## id (1 flagged: 1 REWORD)
- p088 REWORD: "Ya, sup ini pun berkerak." -> "Ya, sup ini ada keraknya.". The recognizer heard "bergerak" ("moves"). berkerak and bergerak differ by one sound.

## vi (7 flagged: 4 REWORD, 3 KEEP)
- p026 KEEP: "Mưa mà gặm được đá ạ?" The recognizer heard gắp and hả, a tone slip. gặm is set up in the line before.
- p045 REWORD: "đâu còn là chút xíu nữa." -> "thì thành rất nhiều.". The recognizer heard "còn lại chút xíu" ("a little is left"), which reverses the meaning. The new line says it plainly: it becomes a lot.
- p051 KEEP: "Sông cứ đổ nước, đúng," The recognizer heard xong for sông, a tone slip.
- p064 REWORD: "Đúng, mưa cháu dầm phải gần như là…" -> "Đúng, nước mưa gần như là…". The recognizer heard "nước dừa" ("coconut water"). The phrase "mưa cháu dầm phải" is awkward.
- p130 REWORD: "Kiểu ninh dữ ấy ạ?" -> "Kiểu lửa to ấy ạ?". The recognizer heard "ninh nhừ" ("simmered soft"), which changes the meaning. "lửa to" matches the kid's own words in p134.
- p135 REWORD: "Ninh dữ, Biển Đỏ mặn hơn" -> "Lửa to, Biển Đỏ mặn hơn". The recognizer heard "nhưng giữ". "Ninh dữ" is not idiomatic.
- p145 KEEP: "Con sông cháu thấy!" The recognizer heard Dâu for cháu. cháu is the kid's fixed pronoun, and other lines with it passed.

## th (9 flagged: 6 REWORD, 3 KEEP)
- p051 KEEP: ใช่ แม่น้ำเทตลอด The recognizer dropped แม่. แม่น้ำ is a common word.
- p061 REWORD: ไม่ แดดขนได้แค่น้ำ -> ไม่ แดดยกได้แค่น้ำ. The recognizer heard ดาดคน: ขน ("carry") was misheard as คน ("person"). ยก ("lift") is clear.
- p062 REWORD: ไม่ขนเกลือ -> ไม่ยกเกลือ. The recognizer heard ขึ้น. This keeps the same verb as p061.
- p073 KEEP: งั้นเคี่ยวทุกวัน The recognizer heard เที่ยว, a slip on the first consonant (Jev 0.04). The cooking context is clear.
- p088 REWORD: ใช่ ซุปหม้อนี้ก็มีคราบ -> ใช่ หม้อนี้ก็มีคราบนะ. The recognizer heard ค่ะ because คราบ was swallowed at the end of the line. A closing นะ protects it.
- p098 REWORD: เปลือกไม่ใช้เกลือในครัว -> หอยไม่ได้ใช้เกลือในครัว. The recognizer heard "เกลือ ไม่ใช่…", mixing up เปลือก/เกลือ and ใช้/ใช่, which flips the meaning.
- p115 REWORD: ทะเลก็เก็บไปตลอดเหรอ -> ทะเลเก็บไปตลอดเหรอ. The recognizer heard ทะเลาะ ("quarrel") because ทะเล+ก็ ran together.
- p117 REWORD: น้ำออกทางฟ้า … -> น้ำขึ้นฟ้า …. The recognizer heard ฝา ("lid"), which also makes sense for a pot. ขึ้นฟ้า ("goes up to the sky") can't be confused that way.
- p141 KEEP: เหนือสุด 1 กิโลมีเกลือไม่กี่กรัม The recognizer heard น้ำซุป, swayed by the soup context (Jev 0.05).
