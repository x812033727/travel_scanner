# YouTube 播放清單：標題與說明（九語）

2026-10-22 在 Studio 手動設定。播放清單跟影片一樣可以設多語言標題與說明：Studio 的「播放清單 → 語言」頁先設預設語言（中文（台灣）），再用「新增語言」逐一填翻譯；Data API 對應 `playlists.update` 的 `localizations`（每次 50 單位），repo 目前沒有寫入播放清單的程式（`apps/api/app/video_youtube/client.py` 只有 `playlistItems.list`）。

語言跟影片的 `TARGET_LOCALES` 一致（`tools/video/core/schema.mjs`）：zh-TW 預設，另加 en、ja、ko、es（拉丁美洲）、pt（巴西）、id、vi、th；zh-CN 在 2026-10-09 拿掉，所以沒填。

## 清單

| 清單 id | 標題（zh-TW） | 瀏覽權限 | 備註 |
| --- | --- | --- | --- |
| `PLTcDQ82htNKM` | AI 名詞十分鐘 | 公開 | 原標題「AI名詞教學」，改成系列定案名稱（`docs/videos/ai-terms/README.md`） |
| `PLM3u7nG09RcI` | AI科技資訊 | 公開 | AI 新聞影片 |
| `PLa-mCBTn-dSw` | 奇聞檔案局 | 公開 |  |
| `PLXNxidbAJ8cY` | 品牌故事 | 私人 | 私人；三支裡一支（A4 紙）沒有品牌故事後綴 |
| `PLEGyTVvrsIag` | 種田娶妻打天下 | 公開 | 存說明時 Studio 把預設語言自動設成日文，已改回中文（台灣） |
| `PLQMXuxTH5Pkc` | 歷史系列 | 私人 | 私人、0 支影片；站主 10-19 建立，用途未定 |
| `PLMSBVkAy71z0` | AI 科技快報 | 公開 | 每日 AI／科技快報；2026-10-29 加 |

## AI 名詞十分鐘（`PLTcDQ82htNKM`）

| 語言 | 標題 | 說明 |
| --- | --- | --- |
| 中文（台灣） | AI 名詞十分鐘 | 一集講清楚一個 AI 名詞：它是什麼、怎麼運作、什麼時候該在意、跟誰容易搞混。每集約 10 分鐘，不編集數，每一集都能單獨看；說明欄連回 mokaair.com 的完整文章。<br>繁中旁白、可關閉的 CC 字幕。 |
| 英文 | AI Terms in 10 Minutes | One AI term per episode, explained properly: what it is, how it works, when it matters and what it gets confused with. About 10 minutes each, no episode numbers, so start anywhere; the description links to the full article on mokaair.com.<br>Mandarin narration with English CC subtitles. |
| 日文 | 10分でわかるAI用語 | 1話にAI用語をひとつ。それは何か、どう動くのか、いつ気にすべきか、何と混同しやすいのかを約10分で解説します。話数はなく、どの回からでも見られます。概要欄から mokaair.com の記事全文へ。<br>中国語ナレーション、日本語字幕付き。 |
| 韓文 | 10분 AI 용어 | 한 편에 AI 용어 하나: 무엇인지, 어떻게 작동하는지, 언제 신경 써야 하는지, 무엇과 헷갈리기 쉬운지. 한 편 약 10분, 회차 번호가 없어 어디서든 시작할 수 있습니다. 설명란에서 mokaair.com의 전체 글로 이어집니다.<br>중국어 내레이션, 한국어 CC 자막 제공. |
| 西班牙文（拉丁美洲） | Términos de IA en 10 minutos | Un término de IA por episodio, bien explicado: qué es, cómo funciona, cuándo importa y con qué se confunde. Unos 10 minutos cada uno, sin numeración, así que empieza por donde quieras; la descripción enlaza al artículo completo en mokaair.com.<br>Narración en mandarín con subtítulos en español. |
| 葡萄牙文（巴西） | Termos de IA em 10 minutos | Um termo de IA por episódio, bem explicado: o que é, como funciona, quando importa e com o que se confunde. Cerca de 10 minutos cada, sem numeração, então comece por onde quiser; a descrição leva ao artigo completo em mokaair.com.<br>Narração em mandarim com legendas em português. |
| 印尼文 | Istilah AI dalam 10 Menit | Satu istilah AI per episode, dijelaskan tuntas: apa itu, cara kerjanya, kapan perlu diperhatikan, dan dengan apa sering tertukar. Sekitar 10 menit per episode, tanpa nomor urut, jadi mulai dari mana saja; deskripsi menautkan ke artikel lengkap di mokaair.com.<br>Narasi Mandarin dengan subtitle Indonesia. |
| 越南文 | Thuật ngữ AI trong 10 phút | Mỗi tập một thuật ngữ AI, giải thích rõ ràng: nó là gì, hoạt động thế nào, khi nào cần để ý và dễ nhầm với gì. Mỗi tập khoảng 10 phút, không đánh số tập nên xem từ đâu cũng được; phần mô tả dẫn tới bài viết đầy đủ trên mokaair.com.<br>Thuyết minh tiếng Trung, có phụ đề tiếng Việt. |
| 泰文 | ศัพท์ AI ใน 10 นาที | ตอนละหนึ่งศัพท์ AI อธิบายให้เข้าใจ: มันคืออะไร ทำงานอย่างไร เมื่อไรที่ต้องใส่ใจ และมักสับสนกับอะไร ตอนละประมาณ 10 นาที ไม่มีลำดับตอน เริ่มดูจากตอนไหนก็ได้ คำอธิบายมีลิงก์ไปบทความฉบับเต็มที่ mokaair.com<br>บรรยายภาษาจีนกลาง มีซับไทย |

## AI科技資訊（`PLM3u7nG09RcI`）

| 語言 | 標題 | 說明 |
| --- | --- | --- |
| 中文（台灣） | AI科技資訊 | AI 與科技新聞的整理：這個數字是誰說的、在哪裡說的、該怎麼讀，還有看完今天就能做的一件事。每支 8–10 分鐘，來源列在說明欄；媒體轉述與官方說法分開標明。只做資訊整理，不是投資、法律或採購建議。<br>繁中旁白、可關閉的 CC 字幕。 |
| 英文 | AI & Tech News, Explained | AI and tech news, sorted out: who said that number, where they said it, how to read it, and one thing you can do today. 8–10 minutes each, sources in the description; media reports and official statements are labelled separately. Information only, not investment, legal or purchasing advice.<br>Mandarin narration with English CC subtitles. |
| 日文 | AI・テックニュース解説 | AIとテックのニュースを整理します。その数字は誰が、どこで言ったのか、どう読むべきか、そして見終わったら今日できることをひとつ。1本8〜10分、出典は概要欄に。メディアの報道と公式発表は分けて示します。情報整理のみで、投資・法律・購入の助言ではありません。<br>中国語ナレーション、日本語字幕付き。 |
| 韓文 | AI·테크 뉴스 정리 | AI와 테크 뉴스를 정리합니다: 그 숫자는 누가, 어디서 말했는지, 어떻게 읽어야 하는지, 그리고 보고 나서 오늘 바로 할 수 있는 한 가지. 한 편 8–10분, 출처는 설명란에; 언론 보도와 공식 발표는 따로 표시합니다. 정보 정리일 뿐 투자·법률·구매 조언이 아닙니다.<br>중국어 내레이션, 한국어 CC 자막 제공. |
| 西班牙文（拉丁美洲） | Noticias de IA y tecnología, explicadas | Noticias de IA y tecnología puestas en orden: quién dijo esa cifra, dónde la dijo, cómo leerla y una cosa que puedes hacer hoy. 8–10 minutos cada una, fuentes en la descripción; las notas de prensa y las declaraciones oficiales se marcan por separado. Solo información, no es asesoría de inversión, legal ni de compra.<br>Narración en mandarín con subtítulos en español. |
| 葡萄牙文（巴西） | Notícias de IA e tecnologia, explicadas | Notícias de IA e tecnologia postas em ordem: quem disse aquele número, onde disse, como ler e uma coisa que você pode fazer hoje. 8–10 minutos cada, fontes na descrição; relatos da imprensa e declarações oficiais são marcados separadamente. Só informação, não é aconselhamento de investimento, jurídico ou de compra.<br>Narração em mandarim com legendas em português. |
| 印尼文 | Berita AI & Teknologi, Dijelaskan | Berita AI dan teknologi yang dirapikan: siapa yang menyebut angka itu, di mana, bagaimana membacanya, dan satu hal yang bisa kamu lakukan hari ini. 8–10 menit per video, sumber di deskripsi; laporan media dan pernyataan resmi ditandai terpisah. Hanya rangkuman informasi, bukan saran investasi, hukum, atau pembelian.<br>Narasi Mandarin dengan subtitle Indonesia. |
| 越南文 | Tin AI & công nghệ, giải thích rõ | Tin AI và công nghệ được sắp xếp lại: con số đó ai nói, nói ở đâu, nên đọc thế nào, và một việc bạn có thể làm ngay hôm nay. Mỗi video 8–10 phút, nguồn trong phần mô tả; tin báo chí và phát biểu chính thức được ghi riêng. Chỉ tổng hợp thông tin, không phải lời khuyên đầu tư, pháp lý hay mua sắm.<br>Thuyết minh tiếng Trung, có phụ đề tiếng Việt. |
| 泰文 | ข่าว AI และเทคโนโลยี อธิบายให้เข้าใจ | เรียบเรียงข่าว AI และเทคโนโลยี: ตัวเลขนั้นใครพูด พูดที่ไหน ควรอ่านอย่างไร และสิ่งหนึ่งที่ทำได้ทันทีวันนี้ คลิปละ 8–10 นาที แหล่งที่มาอยู่ในคำอธิบาย แยกชัดระหว่างรายงานของสื่อกับคำแถลงอย่างเป็นทางการ เป็นการสรุปข้อมูลเท่านั้น ไม่ใช่คำแนะนำด้านการลงทุน กฎหมาย หรือการซื้อ<br>บรรยายภาษาจีนกลาง มีซับไทย |

## 奇聞檔案局（`PLa-mCBTn-dSw`）

| 語言 | 標題 | 說明 |
| --- | --- | --- |
| 中文（台灣） | 奇聞檔案局 | 歷史懸案、奇異現象、預言、外星與都市傳說：一集打開一份檔案，把流傳的說法、留下的證據與目前最站得住的解釋分開講清楚。沒有定論就說沒有定論，每個數字、年份與引言的出處列在說明欄。每集約 10 分鐘。<br>繁中旁白、可關閉的 CC 字幕。 |
| 英文 | Curio Files: History's Unsolved Cases | Historical mysteries, strange phenomena, prophecies, aliens and urban legends: each episode opens one case file and separates what people say from what the evidence shows and what the best current explanation is. When there is no verdict, we say so; every figure, year and quote is sourced in the description. About 10 minutes per episode.<br>Mandarin narration with English CC subtitles. |
| 日文 | 奇聞ファイル：歴史の未解決事件 | 歴史の未解決事件、不思議な現象、予言、宇宙人、都市伝説。1話につき1件のファイルを開き、語り継がれてきた説、残された証拠、現時点で最も確かな説明を分けて語ります。結論が出ていないことは「出ていない」と言う。数字・年代・引用の出典は概要欄に。1話約10分。<br>中国語ナレーション、日本語字幕付き。 |
| 韓文 | 기이한 사건 파일: 역사 속 미스터리 | 역사 미제 사건, 기이한 현상, 예언, 외계인과 도시 전설: 한 편에 파일 하나를 열어, 떠도는 이야기와 남아 있는 증거, 지금 가장 설득력 있는 설명을 나누어 이야기합니다. 결론이 없으면 없다고 말하고, 모든 숫자·연도·인용의 출처는 설명란에 있습니다. 한 편 약 10분.<br>중국어 내레이션, 한국어 CC 자막 제공. |
| 西班牙文（拉丁美洲） | Archivo de curiosidades: casos sin resolver | Misterios históricos, fenómenos extraños, profecías, extraterrestres y leyendas urbanas: cada episodio abre un expediente y separa lo que se cuenta, lo que muestran las pruebas y la explicación más sólida hasta hoy. Cuando no hay veredicto, lo decimos; cada cifra, año y cita tiene su fuente en la descripción. Unos 10 minutos por episodio.<br>Narración en mandarín con subtítulos en español. |
| 葡萄牙文（巴西） | Arquivo de curiosidades: casos sem solução | Mistérios históricos, fenômenos estranhos, profecias, extraterrestres e lendas urbanas: cada episódio abre um dossiê e separa o que se conta, o que as provas mostram e a explicação mais sólida até hoje. Quando não há veredito, dizemos isso; cada número, ano e citação tem fonte na descrição. Cerca de 10 minutos por episódio.<br>Narração em mandarim com legendas em português. |
| 印尼文 | Arsip Kisah Aneh: kasus yang belum terpecahkan | Misteri sejarah, fenomena aneh, ramalan, alien, dan legenda urban: setiap episode membuka satu berkas dan memisahkan apa yang beredar, apa yang ditunjukkan bukti, dan penjelasan paling kuat sampai hari ini. Kalau belum ada kesimpulan, kami bilang belum ada; setiap angka, tahun, dan kutipan ada sumbernya di deskripsi. Sekitar 10 menit per episode.<br>Narasi Mandarin dengan subtitle Indonesia. |
| 越南文 | Hồ sơ kỳ văn: những vụ án chưa có lời giải | Bí ẩn lịch sử, hiện tượng kỳ lạ, lời tiên tri, người ngoài hành tinh và truyền thuyết đô thị: mỗi tập mở một hồ sơ, tách bạch lời đồn, bằng chứng còn lại và lời giải thích vững nhất hiện nay. Chưa có kết luận thì nói là chưa có; mọi con số, năm và trích dẫn đều có nguồn trong phần mô tả. Mỗi tập khoảng 10 phút.<br>Thuyết minh tiếng Trung, có phụ đề tiếng Việt. |
| 泰文 | แฟ้มเรื่องแปลก: คดีปริศนาในประวัติศาสตร์ | คดีปริศนาในประวัติศาสตร์ ปรากฏการณ์ประหลาด คำทำนาย มนุษย์ต่างดาว และตำนานเมือง: แต่ละตอนเปิดหนึ่งแฟ้ม แยกให้ชัดระหว่างเรื่องที่เล่าต่อกันมา หลักฐานที่เหลืออยู่ และคำอธิบายที่หนักแน่นที่สุดในปัจจุบัน ถ้ายังไม่มีข้อสรุปก็บอกว่ายังไม่มี ตัวเลข ปี และคำพูดอ้างอิงทุกรายการมีแหล่งที่มาในคำอธิบาย ตอนละประมาณ 10 นาที<br>บรรยายภาษาจีนกลาง มีซับไทย |

## 品牌故事（`PLXNxidbAJ8cY`）

| 語言 | 標題 | 說明 |
| --- | --- | --- |
| 中文（台灣） | 品牌故事 | 查核過的非虛構故事：一個品牌、一件日用品或一個大家天天用卻沒想過的標準，背後的生意怎麼運作。每集約 10 分鐘，每個數字、年份與引言的出處都列在說明欄。<br>繁中旁白、可關閉的 CC 字幕。 |
| 英文 | Brand Stories | Fact-checked, non-fiction stories: how the business behind a brand, an everyday object or a standard you use without thinking actually works. About 10 minutes per episode; every figure, year and quote is sourced in the description.<br>Mandarin narration with English CC subtitles. |
| 日文 | ブランドストーリー | 事実確認済みのノンフィクション。ひとつのブランド、ひとつの日用品、あるいは誰もが毎日使いながら考えたことのない規格の裏で、ビジネスがどう動いているのかを語ります。1話約10分。数字・年代・引用の出典はすべて概要欄に記載。<br>中国語ナレーション、日本語字幕付き。 |
| 韓文 | 브랜드 스토리 | 사실 확인을 거친 논픽션 이야기: 브랜드 하나, 생활용품 하나, 또는 매일 쓰면서도 생각해 본 적 없는 표준 하나의 뒤에서 비즈니스가 어떻게 돌아가는지. 한 편 약 10분, 모든 숫자·연도·인용의 출처는 설명란에 있습니다.<br>중국어 내레이션, 한국어 CC 자막 제공. |
| 西班牙文（拉丁美洲） | Historias de marca | Historias reales y verificadas: cómo funciona el negocio detrás de una marca, un objeto cotidiano o una norma que usas sin pensarlo. Unos 10 minutos por episodio; cada cifra, año y cita tiene su fuente en la descripción.<br>Narración en mandarín con subtítulos en español. |
| 葡萄牙文（巴西） | Histórias de marca | Histórias reais e verificadas: como funciona o negócio por trás de uma marca, de um objeto do dia a dia ou de um padrão que você usa sem perceber. Cerca de 10 minutos por episódio; cada número, ano e citação tem fonte na descrição.<br>Narração em mandarim com legendas em português. |
| 印尼文 | Kisah Merek | Kisah nyata yang sudah diverifikasi: bagaimana bisnis di balik sebuah merek, benda sehari-hari, atau standar yang kita pakai tanpa berpikir sebenarnya bekerja. Sekitar 10 menit per episode; setiap angka, tahun, dan kutipan ada sumbernya di deskripsi.<br>Narasi Mandarin dengan subtitle Indonesia. |
| 越南文 | Câu chuyện thương hiệu | Những câu chuyện có thật đã được kiểm chứng: cách vận hành của việc kinh doanh đằng sau một thương hiệu, một món đồ dùng hằng ngày hay một tiêu chuẩn ai cũng dùng mà chưa từng nghĩ tới. Mỗi tập khoảng 10 phút; mọi con số, năm và trích dẫn đều có nguồn trong phần mô tả.<br>Thuyết minh tiếng Trung, có phụ đề tiếng Việt. |
| 泰文 | เรื่องราวแบรนด์ | เรื่องจริงที่ผ่านการตรวจสอบ: ธุรกิจเบื้องหลังแบรนด์หนึ่ง ของใช้ประจำวันชิ้นหนึ่ง หรือมาตรฐานที่ทุกคนใช้ทุกวันโดยไม่เคยคิดถึง ทำงานอย่างไร ตอนละประมาณ 10 นาที ตัวเลข ปี และคำพูดอ้างอิงทุกรายการมีแหล่งที่มาในคำอธิบาย<br>บรรยายภาษาจีนกลาง มีซับไทย |

## 種田娶妻打天下（`PLEGyTVvrsIag`）

| 語言 | 標題 | 說明 |
| --- | --- | --- |
| 中文（台灣） | 種田娶妻打天下 | 農學碩士許硯面試被刷，雨夜醒來成了柳溪村的窮秀才：欠員外二十兩、腦中多了一個「良緣系統」，官差還帶著配婚令和三個新娘敲門。穿越種田短劇，每集 2–4 分鐘，照集數順序看。<br>繁中旁白；提供英、日、韓、西、葡、印尼、越、泰文的 CC 字幕與配音。 |
| 英文 | Farm, Marry, Conquer | Agriculture grad Xu Yan bombs a job interview and wakes up in a thunderstorm as a penniless scholar in Liuxi Village: 20 taels in debt, a Matchmaker System in his head, and an officer at the door with a marriage decree and three brides. A time-travel farming drama, 2–4 minutes per episode. Watch in order.<br>Mandarin audio with English dub and CC subtitles. |
| 日文 | 畑を耕し嫁を娶り天下を取る | 農学修士の許硯は面接に落ち、雷雨の夜に目を覚ますと柳渓村の貧乏書生になっていた。借金二十両、頭の中には「良縁システム」、そして役人が婚配令と三人の花嫁を連れて戸を叩く。タイムスリップ農村ドラマ、1話2〜4分。話数順にどうぞ。<br>中国語音声、日本語吹き替えと字幕付き。 |
| 韓文 | 농사짓고 장가가서 천하를 얻다 | 농학 석사 허연은 면접에서 떨어지고, 비 오는 밤 눈을 떠 보니 류시 마을의 가난한 서생이 되어 있었다. 빚 스무 냥, 머릿속의 '좋은 인연 시스템', 그리고 혼배령과 신부 셋을 데리고 문을 두드리는 관리. 시간 여행 농사 드라마, 한 편 2–4분. 순서대로 보세요.<br>중국어 음성, 한국어 더빙과 CC 자막 제공. |
| 西班牙文（拉丁美洲） | Siembra, cásate y conquista | Xu Yan, maestro en agronomía, fracasa en una entrevista de trabajo y despierta en una noche de tormenta convertido en un letrado pobre de la aldea Liuxi: 20 taeles de deuda, un «Sistema Casamentero» en la cabeza y un oficial en la puerta con un decreto de matrimonio y tres novias. Drama rural de viaje en el tiempo, 2–4 minutos por episodio. Míralo en orden.<br>Audio en mandarín con doblaje y subtítulos en español. |
| 葡萄牙文（巴西） | Plantar, Casar e Conquistar | Xu Yan, mestre em agronomia, vai mal numa entrevista de emprego e acorda numa noite de tempestade como um letrado pobre da aldeia Liuxi: 20 taéis de dívida, um «Sistema Casamenteiro» na cabeça e um oficial à porta com um decreto de casamento e três noivas. Drama rural de viagem no tempo, 2–4 minutos por episódio. Assista em ordem.<br>Áudio em mandarim com dublagem e legendas em português. |
| 印尼文 | Bertani, Beristri, Berkuasa | Xu Yan, magister pertanian, gagal wawancara kerja dan terbangun di malam badai sebagai sarjana miskin di Desa Liuxi: utang 20 tael, sebuah «Sistem Perjodohan» di kepalanya, dan seorang petugas di depan pintu membawa titah perkawinan beserta tiga mempelai. Drama bertani lintas waktu, 2–4 menit per episode. Tonton berurutan.<br>Audio Mandarin dengan sulih suara dan subtitle Indonesia. |
| 越南文 | Làm Ruộng Cưới Vợ Đoạt Thiên Hạ | Hứa Nghiên, thạc sĩ nông học, trượt phỏng vấn rồi tỉnh dậy trong đêm mưa bão, hóa thành thư sinh nghèo ở thôn Liễu Khê: nợ hai mươi lượng, trong đầu có «Hệ thống Lương Duyên», còn quan sai gõ cửa mang theo lệnh phối hôn và ba cô dâu. Phim ngắn xuyên không làm ruộng, mỗi tập 2–4 phút. Xem theo thứ tự.<br>Tiếng Trung, có lồng tiếng và phụ đề tiếng Việt. |
| 泰文 | ทะลุมิติไปทำนา ได้เมีย ครองแผ่นดิน | สวี่เยี่ยน มหาบัณฑิตเกษตร สัมภาษณ์งานตก แล้วตื่นขึ้นในคืนพายุฝนกลายเป็นบัณฑิตยากจนแห่งหมู่บ้านหลิ่วซี: ติดหนี้ยี่สิบตำลึง มี «ระบบคู่บุญ» อยู่ในหัว และนายอำเภอมาเคาะประตูพร้อมคำสั่งแต่งงานกับเจ้าสาวสามคน ละครสั้นทะลุมิติทำนา ตอนละ 2–4 นาที ดูตามลำดับตอน<br>เสียงจีนกลาง มีพากย์ไทยและซับไทย |

## 歷史系列（`PLQMXuxTH5Pkc`）

| 語言 | 標題 | 說明 |
| --- | --- | --- |
| 中文（台灣） | 歷史系列 | 歷史人物與名場面：一集一份檔案，照可查的來源講清楚當時發生了什麼、留下了哪些證據、後人又加了哪些說法。每集約 10 分鐘，參考資料列在說明欄。<br>繁中旁白、可關閉的 CC 字幕。 |
| 英文 | History Series | Historical figures and famous moments: one case file per episode, told from verifiable sources — what happened, what evidence survives, and what later retellings added. About 10 minutes per episode; sources are listed in the description.<br>Mandarin narration with English CC subtitles. |
| 日文 | 歴史シリーズ | 歴史上の人物と名場面。1話につき1件のファイルを、確認できる資料に沿って語ります。何が起きたのか、どんな証拠が残っているのか、後世に何が付け加えられたのか。1話約10分、参考資料は概要欄に。<br>中国語ナレーション、日本語字幕付き。 |
| 韓文 | 역사 시리즈 | 역사 속 인물과 명장면: 한 편에 파일 하나, 확인 가능한 자료를 따라 당시 무슨 일이 있었고 어떤 증거가 남았으며 후대에 무엇이 덧붙여졌는지 이야기합니다. 한 편 약 10분, 참고 자료는 설명란에 있습니다.<br>중국어 내레이션, 한국어 CC 자막 제공. |
| 西班牙文（拉丁美洲） | Serie de historia | Personajes y escenas célebres de la historia: un expediente por episodio, contado a partir de fuentes verificables: qué pasó, qué pruebas quedan y qué añadieron los relatos posteriores. Unos 10 minutos por episodio; las fuentes están en la descripción.<br>Narración en mandarín con subtítulos en español. |
| 葡萄牙文（巴西） | Série de história | Personagens e cenas famosas da história: um dossiê por episódio, contado a partir de fontes verificáveis: o que aconteceu, que provas restaram e o que os relatos posteriores acrescentaram. Cerca de 10 minutos por episódio; as fontes estão na descrição.<br>Narração em mandarim com legendas em português. |
| 印尼文 | Seri Sejarah | Tokoh dan momen terkenal dalam sejarah: satu berkas per episode, diceritakan dari sumber yang bisa diperiksa: apa yang terjadi, bukti apa yang tersisa, dan apa yang ditambahkan oleh cerita-cerita kemudian. Sekitar 10 menit per episode; sumber ada di deskripsi.<br>Narasi Mandarin dengan subtitle Indonesia. |
| 越南文 | Loạt phim lịch sử | Nhân vật và khoảnh khắc nổi tiếng trong lịch sử: mỗi tập một hồ sơ, kể theo những nguồn có thể kiểm chứng: chuyện gì đã xảy ra, bằng chứng nào còn lại, và đời sau đã thêm thắt những gì. Mỗi tập khoảng 10 phút; nguồn tham khảo nằm trong phần mô tả.<br>Thuyết minh tiếng Trung, có phụ đề tiếng Việt. |
| 泰文 | ซีรีส์ประวัติศาสตร์ | บุคคลและฉากสำคัญในประวัติศาสตร์: ตอนละหนึ่งแฟ้ม เล่าตามแหล่งข้อมูลที่ตรวจสอบได้ว่าเกิดอะไรขึ้น เหลือหลักฐานอะไร และคนรุ่นหลังเติมอะไรเข้าไป ตอนละประมาณ 10 นาที แหล่งอ้างอิงอยู่ในคำอธิบาย<br>บรรยายภาษาจีนกลาง มีซับไทย |

## AI 科技快報（`PLMSBVkAy71z0`）

2026-10-29 加，放每日 AI／科技快報（`daily-ai-YYYYMMDD`，[`AUTOMATION.md`](AUTOMATION.md) §每日 AI 快報）。快報每支都傳八條配音，所以說明寫「配音」而不是只有字幕。中文說明在詳細資訊頁可以換行；語言頁的翻譯對話框按 Enter／Shift+Enter 都不會換行，所以八語說明實際存的是一段，表中 `<br>` 的位置是一個空格。

| 語言 | 標題 | 說明 |
| --- | --- | --- |
| 中文（台灣） | AI 科技快報 | 每天十分鐘，跟上昨天的 AI 與科技新聞：挑 5–8 則，一則一章，講清楚這跟你有什麼關係、現在能不能用、要不要擔心。每則的出處列在說明欄，連回 mokaair.com 的完整文章；媒體轉述與官方說法分開標明。只做資訊整理，不是投資、法律或採購建議。<br>繁中旁白，另有八種語言配音與 CC 字幕。 |
| 英文 | Daily AI & Tech Brief | Ten minutes a day to catch up on yesterday's AI and tech news: 5–8 stories, one chapter each, covering what it means for you, whether you can use it yet, and whether to worry. Sources for every story are in the description, linking to the full articles on mokaair.com; media reports and official statements are labelled separately. Information only, not investment, legal or purchasing advice.<br>Mandarin narration, with dubbed audio and CC subtitles in eight languages. |
| 日文 | 毎日AI・テック速報 | 1日10分で、前日のAIとテックのニュースに追いつく。5〜8本を1本1章で、自分に何の関係があるのか、今すぐ使えるのか、心配すべきかを解説します。各ニュースの出典は概要欄に、mokaair.com の記事全文へリンク。メディアの報道と公式発表は分けて示します。情報整理のみで、投資・法律・購入の助言ではありません。<br>中国語ナレーション、日本語吹き替えと字幕付き。 |
| 韓文 | 매일 AI·테크 브리핑 | 하루 10분으로 어제의 AI·테크 뉴스 따라잡기: 5–8개 뉴스를 한 챕터씩, 나와 무슨 상관인지, 지금 쓸 수 있는지, 걱정해야 하는지 짚어 드립니다. 뉴스마다 출처는 설명란에 있고 mokaair.com의 전체 기사로 이어집니다. 언론 보도와 공식 발표는 따로 표시합니다. 정보 정리일 뿐 투자·법률·구매 조언이 아닙니다.<br>중국어 내레이션, 한국어 더빙과 CC 자막 제공. |
| 西班牙文（拉丁美洲） | Resumen diario de IA y tecnología | Diez minutos al día para ponerte al corriente de las noticias de IA y tecnología de ayer: 5–8 historias, un capítulo cada una, sobre qué significa para ti, si ya puedes usarlo y si debes preocuparte. Las fuentes de cada historia están en la descripción, con enlace al artículo completo en mokaair.com; las notas de prensa y las declaraciones oficiales se marcan por separado. Solo información, no es asesoría de inversión, legal ni de compra.<br>Narración en mandarín, con doblaje y subtítulos en español. |
| 葡萄牙文（巴西） | Resumo diário de IA e tecnologia | Dez minutos por dia para acompanhar as notícias de IA e tecnologia de ontem: 5–8 histórias, um capítulo cada, sobre o que muda para você, se já dá para usar e se é preciso se preocupar. As fontes de cada história estão na descrição, com link para o artigo completo em mokaair.com; relatos da imprensa e declarações oficiais são marcados separadamente. Só informação, não é aconselhamento de investimento, jurídico ou de compra.<br>Narração em mandarim, com dublagem e legendas em português. |
| 印尼文 | Ringkasan Harian AI & Teknologi | Sepuluh menit sehari untuk mengikuti berita AI dan teknologi kemarin: 5–8 berita, satu bab per berita, tentang apa artinya bagimu, apakah sudah bisa dipakai, dan perlu khawatir atau tidak. Sumber setiap berita ada di deskripsi, menautkan ke artikel lengkap di mokaair.com; laporan media dan pernyataan resmi ditandai terpisah. Hanya rangkuman informasi, bukan saran investasi, hukum, atau pembelian.<br>Narasi Mandarin, dengan sulih suara dan subtitle Indonesia. |
| 越南文 | Bản tin AI & công nghệ mỗi ngày | Mười phút mỗi ngày để cập nhật tin AI và công nghệ hôm qua: 5–8 tin, mỗi tin một chương, nói rõ nó liên quan gì đến bạn, đã dùng được chưa và có cần lo không. Nguồn của từng tin nằm trong phần mô tả, dẫn tới bài viết đầy đủ trên mokaair.com; tin báo chí và phát biểu chính thức được ghi riêng. Chỉ tổng hợp thông tin, không phải lời khuyên đầu tư, pháp lý hay mua sắm.<br>Thuyết minh tiếng Trung, có lồng tiếng và phụ đề tiếng Việt. |
| 泰文 | สรุปข่าว AI และเทคโนโลยีรายวัน | วันละสิบนาที ตามทันข่าว AI และเทคโนโลยีของเมื่อวาน: 5–8 ข่าว ข่าวละหนึ่งบท บอกว่าเกี่ยวกับคุณอย่างไร ใช้ได้แล้วหรือยัง และต้องกังวลไหม แหล่งที่มาของแต่ละข่าวอยู่ในคำอธิบาย พร้อมลิงก์ไปบทความฉบับเต็มที่ mokaair.com แยกชัดระหว่างรายงานของสื่อกับคำแถลงอย่างเป็นทางการ เป็นการสรุปข้อมูลเท่านั้น ไม่ใช่คำแนะนำด้านการลงทุน กฎหมาย หรือการซื้อ<br>บรรยายภาษาจีนกลาง มีพากย์ไทยและซับไทย |
