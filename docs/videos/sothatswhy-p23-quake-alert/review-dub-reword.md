# P23 quake-alert dub review: KEEP / REWORD

Files edited: `docs/videos/sothatswhy-p23-quake-alert/i18n/{en,ja,ko,es,pt,id,vi,th}.json` (only `lines[id].text` of REWORD lines; each rewrite has the same number of characters or fewer than the old text; all files pass json.tool).
Safety lines (p178–p183) were not changed in any locale. th p182 「หมอบ ป้อง เกาะ!」 matches p179/p180/p181.

| locale | flagged | KEEP | REWORD |
|---|---|---|---|
| en | 7 | 5 | 2 |
| ja | 20 | 14 | 6 |
| ko | 9 | 8 | 1 |
| es | 3 | 2 | 1 |
| pt | 8 | 7 | 1 |
| id | 7 | 5 | 2 |
| vi | 13 | 11 | 2 |
| th | 16 | 14 | 2 |
| **total** | **83** | **66** | **17** |

## en
- p059 KEEP: "Feeling the messenger at home is often too late." The recognizer heard "Killing", a near-homophone at the start of the clip. The sentence itself is fine.
- p068 KEEP: "Do the stations yell…" was heard as "To the stations yelled". This is a slip on correct speech.
- p093 REWORD: "It rides on electricity and wins!" → "It rides electricity to win!" "and wins" was heard as "and winds", which is ambiguous after "electricity". "to win" cannot be heard that way.
- p137 KEEP: "There" was heard as "They're", a homophone.
- p147 KEEP: "9 seconds! Hualien" was heard as "Nine seconds? Wow!". These are digits and a proper name.
- p148 KEEP: "folks all hid" was heard as "Foxhole head". This is a sound-alike word split across two clips.
- p189 REWORD: "electricity and wins!" → "electricity to win!" Same reason as p093. It also stays consistent with p093.

## ja
- p003 KEEP: パパのも鳴って was heard as パパのものって. The recognizer split the words differently.
- p025 REWORD: 始まった地震は競走なの。→ 始まったら、かけっこ。 競走 was heard as 表層, and 競走 is easily confused with 競争. かけっこ is clearer for children.
- p042 KEEP: S波 was written as S派. This is a kanji homophone.
- p045 KEEP: 大男なの？ was heard as オーナーの. 大男 is the recurring term and is recognized correctly in about ten other lines, so this is a slip on a short clip.
- p048 KEEP: ちび伝令 was heard as チビでも礼. The term is recognized correctly in p038/p041/p187.
- p059 KEEP: 伝令 was heard as 電波. This is a slip on the recurring term.
- p070 KEEP: 伝令 was heard as 電報, and 気象署 was normalized to 気象庁 (the Japanese agency name). Both are slips.
- p090 KEEP: 警報 was heard as 京王, a homophone.
- p109 KEEP: 一緒に鳴った was heard as 一緒になった. This is a slip on the n sound.
- p112 REWORD: かせいだのは → 稼いだのは. Written in kana, かせいだ was heard as 火星. The kanji form fixes the reading and the pitch accent.
- p117 KEEP: 震央 was heard as 震源. The recognizer swapped in the more common word. 震央 is the established term.
- p118 KEEP: 大男 was heard as 王 at the start of the clip. The term is fine elsewhere.
- p121 REWORD: 大男は約1秒遅れて着く。→ 約1秒ずつ遅れて着く。 It was heard as 第2音は. The subject is clear from p120, so dropping it loses nothing.
- p134 REWORD: 間に合わないこの輪が、警報の死角。→ 間に合わない場所が、警報の死角。 The single-mora 輪 was heard as 幅.
- p147 KEEP: 9秒/花蓮 was heard as 急病/春奈. These are digits and a name, and 花蓮 is recognized correctly in p145/p149/p155.
- p163 KEEP: 台北 was heard as 大抵, a near-homophone.
- p167 KEEP: 地震を…推定 was heard as 重心を…振って. Jev is 0.04, so the transcript is close to the script. The wording is fine.
- p188 REWORD: 計算し、電気に乗り → 計算して電気に乗り. The clipped 計算し、 was drawn out as 軽さーん、しーっ. 計算して reads more naturally.
- p190 REWORD: 震央そばは間に合わないかも、→ 震央近くは間に合わないかも、 震央そば is unnatural and was heard as おそば.
- p193 KEEP: 大男は was heard as 応答は, a near-homophone at the start of the clip.

Note: 大男 and ちび伝令 are recognized correctly in most lines. Renaming either term would be a series-wide decision and has not been made here.

## ko
- p021 KEEP: 많은 was heard as 만약. This is a slip.
- p059 KEEP: 전령 was heard as 정황. 전령 is the established term.
- p079 KEEP: 갈지 was heard as 닿을지. This is a slip and does not change the meaning.
- p108 REWORD: 수신도 못 꺼. → 끌 수도 없어. The old line was short and awkward and was heard as 소신도 없고. The new line is natural: "you can't turn it off".
- p147 KEEP: 9초/화롄 was heard as 구초/화낸. These are digits and a name.
- p149 KEEP: 화롄/진앙 was heard as 화려/진한. These are a name and an established term.
- p158 KEEP: 늦지 was heard as 눕지. This is a slip.
- p161 KEEP: 타이베이/울렸 was heard as 타입A4/올렸. These are a name and a slip.
- p190 KEEP: 진앙 옆 was heard as 침낭 안. This is a slip on the established term.

## es
- p077 REWORD: ¿Qué se sabe al ver al mensajerito? → ¿Qué nos dice el mensajerito? The old line was stiff and was heard as "Quise saber". The new line is simpler and natural for a child.
- p093 KEEP: "La alerta" was heard as "La letra". This is a slip.
- p189 KEEP: "gana al" was heard as "Gana el". This is a slip on a short article. The current text is already the shortest wording, and none of the alternatives fits the length budget.

## pt
- p038 REWORD: Lidera um mensageiro veloz. → Um mensageiro veloz lidera. Starting with the verb sounded odd and was heard as "E deram". Normal word order fixes it.
- p048 KEEP: "era o Mensageiro" was heard as "Era um exagero". This is a slip.
- p057 KEEP: "Mal chega antes" was heard as "Malas gigantes". This is a sound-alike slip.
- p067 KEEP: "ouvem o" was heard as "Ó, vem o". This is a slip.
- p078 KEEP: "largada" was heard as "largura". largada is the established word for the start point (p026–p034).
- p153 KEEP: "E Taipei" was heard as "Itaipu". This is a proper name.
- p158 KEEP: "Taipei" was heard as "Tampei". This is a proper name.
- p187 KEEP: "estações ouvem" was heard as "cê tá me ouvindo". This is a sound-alike slip in the recap.

## id
- p029 KEEP: "start" was heard as "star". "start" is the established term (p026–p034, p078).
- p030 KEEP: "start" was heard as "krater". Jev is 0.05. Same term as p029.
- p079 KEEP: "Si Besar" was heard as "sebesar". This is a slip on the character name.
- p096 KEEP: "Si Besar" was heard as "sebesar". Same slip as p079.
- p106 REWORD: Agar dalam detik, semua terbangun. → Agar semua bangun dalam sekejap. "dalam detik" is unidiomatic, and "Agar" was heard as "Apa".
- p118 REWORD: Si Besar sedetik berapa? → Ingat laju Si Besar? The old line was terse, dropped the "remember" from the Chinese, and was heard as "sebesar". The new line matches the Chinese.
- p147 KEEP: "Hualien" was heard as "Wah, lihat". This is a proper name.

## vi
- p068 KEEP: Jev is 0.02, so the transcript is close to the script, and the line is correct.
- p073 KEEP: "đợi đủ trạm" was heard as "đội chụp chạm". These are tone slips. Jev is 0.06.
- p090 KEEP: "cảnh báo" was heard as "cảnh sát". This is a slip.
- p093 KEEP: "cưỡi điện" was heard as "cười điên". This is a tone slip. The same phrase is the established metaphor in p091 and p188.
- p108 REWORD: và không tắt nhận được. → và không tắt được. The old line was ungrammatical and was heard as "không chấp nhận được".
- p112 KEEP: "chính" was heard as "chín". This is a slip.
- p121 KEEP: "trễ" was heard as "sẽ". This is a slip.
- p126 KEEP: "càng gần" was heard as "Kangen". This is a slip.
- p139 REWORD: Ừ, anh to con có thể ngay sau. → Ừ, anh to con có thể theo sau. The old line had no verb and was heard as "ngáy sao". The new line means "the big guy may follow".
- p147 KEEP: "Dân Hoa Liên" was heard as "dâng hoa liền". This is a proper name.
- p153 KEEP: "Đài Bắc" was heard as "đại bác". This is a proper name.
- p187 KEEP: "trạm" was heard as "Chạm". This is a slip.
- p188 KEEP: "cưỡi điện" was heard as "cưới Điệp". Same tone slip as p093.

## th
- p023 KEEP: ไหว was heard as โอย. Jev is 0.09. The line is short but correct together with p024.
- p032 KEEP: ไหว was heard as หวย. This is a tone slip.
- p038 REWORD: ตัวหน้าสุดคือเจ้าส่งข่าวขาไว → ตัวแรกคือเจ้าส่งข่าวสุดไว. The run ข่าวขาไว is a tongue-twister and was heard as ขาวขาวไว. สุดไว ("super fast") keeps the meaning.
- p046 KEEP: ส่งข่าว was heard as ทรงเขา. This is a slip on the established term.
- p051 KEEP: ส่งข่าว was heard as สองขาว. This is a slip on the established term.
- p063 KEEP: ทั่ว was heard as ทัวร์. This is a homophone.
- p070 REWORD: ส่งท่าทางเจ้าส่งข่าว → ส่งหน้าตาเจ้าส่งข่าว. ท่าทาง ("posture") is the wrong word for the wave's 樣子 (shape), and that part was heard as a garbled repetition (ส่งท่าทางจะส่งเขา). หน้าตา ("what it looks like") is correct.
- p073 KEEP: คอม was heard as เขา. This is a slip.
- p093 KEEP: แจ้งเตือนขี่ไฟฟ้า was heard as จรวดสีฟ้า. Jev is 0.05. แจ้งเตือน is recognized correctly elsewhere.
- p098 KEEP: แจ้งเตือน was heard as เชตตัง. This is a slip at the start of the clip.
- p119 KEEP: ราววิละ was heard as เราว่า Villa. This is a slip. There is no clearer wording that fits the length budget.
- p147 KEEP: 9 วิ/ฮัวเหลียน was heard as เก้าอี้/หัวเหลียน. These are digits and a name.
- p160 KEEP: ไทเป was heard as HiPay. This is a proper name.
- p165 KEEP: แก้ was heard as เกม. This is a slip.
- p182 KEEP: the safety slogan หมอบ ป้อง เกาะ matches p179/p180/p181. It was heard as โกร่งป้องไก, a recognizer slip.
- p188 KEEP: ขี่ไฟฟ้า was heard as เครื่องบินไฟฟ้า. This is a slip.
