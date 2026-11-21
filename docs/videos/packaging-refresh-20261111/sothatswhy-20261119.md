# 原來如此事務所舊集改標題（2026-11-19）

- 日期：2026-11-19。規則：本資料夾 [README.md](README.md)（§二、§四、§五、〈標題檢查〉、〈譯名〉）、[`docs/videos/so-thats-why/refresh-20261101/SPEC.md`](../so-thats-why/refresh-20261101/SPEC.md)〈標題〉；公式照黑猫研究院：大家認得的名字放前 6 字、一個利害或意外的字、數字只在有用且有出處時加、只有一個問號、後綴前最多 30 字、利害字或數字落在前 18 字、不寫平靜的閱讀題、不破梗、不重用縮圖大字。
- 每個 zh-TW 新標題都跑過 `tools/video/core/narrative.mjs` `titleProblems`，結果都是 `[]`；標題裡的每個數字、年份、名字都出自該集 `video.json` 的旁白或 claims／verify／source 檔（「為什麼」欄註明出處）。
- 八語標題照同一套公式另寫，不逐字翻，結尾是〈譯名〉的定版系列後綴；每一條加上 `CAPTION_TAGS` 的完整字幕標記後都在 YouTube 100 字元內（`captionedTitle` 實測，沒有一條要退到短標記 `｜CC`）。
- **怎麼換**：站主在 Studio 換，或在站主於對話裡明確同意後，在主機跑 `python -m app.cli video-youtube-caption-titles --set-title <VIDEO_ID> <LANGUAGE> <TITLE> --apply`（每支 50 配額單位；不加 `--apply` 只報告）。同一支影片兩次改動之間隔 14 天；Studio 的「測試與比較」A/B 測試還在跑時不要改標題。
- 這份只列標題；縮圖不動（`thumbnail` 文字在 `visualHash` 裡，見 README §三）。`video.json`、i18n 檔都沒有改。
- 範圍：`sothatswhy-t27`、repo 裡其他 8 個 `sothatswhy-*` 資料夾（只有公式明顯沒做到才改，否則 keep），以及不在 repo 的 QR Code 那一集。
- 結果：改 2 支（T27、QR Code），保留 8 支。QR Code 那支在 repo 裡找不到劇本或 claims，新標題只用舊標題已有的事實，**上架前要查核**。
- 保留的 6 支 P 系列（P02、P05、P07、P08、P14、P25）中文標題沒問題，但 i18n 檔裡 ko、es、pt、id、vi、th 的系列後綴還是 2026-11-13 定版前的舊名（例如 es「La Oficina del Por Eso」、ko「그래서그랬구나 사무소」）。README §四要求八語一律用〈譯名〉的定版後綴；下面另列「只換後綴」的版本給站主決定要不要一起換。只換後綴也算一次標題改動，同樣受 14 天間隔限制。

| slug | YouTube ID | 舊標題 → 新標題（zh-TW） | 為什麼（缺哪一項、事實出處） | 換之前 28 天 | 換上去的日期 | 換之後 14 天 |
| --- | --- | --- | --- | --- | --- | --- |
| `sothatswhy-t27` |  | 日本垃圾桶少？旅客調查說了什麼｜原來如此事務所 → **日本垃圾桶少是困擾第一名，4,110 位旅客有幾成選它？｜原來如此事務所** | claims.md c3／c6（觀光廳 2026-04-28 公布、001998584.pdf）：五座機場面訪 4,110 位出境外國旅客，「缺少垃圾桶」是最多人選的困擾項目；片中答案 17.2%（未過半）不寫進標題，留給影片回答。舊標題沒有利害或意外字，「說了什麼」是平靜的閱讀題。數字 4,110 有出處、讓「第一名」有分母，所以加。縮圖「最多≠多數」不重用。 | | | |
| `QR Code（不在 repo）` |  | QR Code 沾到咖啡還能嗶，旁邊新碼…（舊標題在手機上被截斷，全文要從 Studio 補） → **QR Code 沾到咖啡，竟然照樣掃得出來？｜原來如此事務所** | repo 裡找不到這集的資料夾、劇本或 claims（grep docs/videos、tasks、git log -S「沾到咖啡」都沒有）；最接近的是 docs/videos/so-thats-why/season2/A36.md（〈QR Code 髒了為什麼還能讀？30%到底在算什麼？〉，當時註明媒體未製作），不能確定是同一份稿。新標題只用舊標題已有的事實（沾到咖啡、仍能讀），不加數字。舊標題的「還能嗶」和縮圖「缺一塊還能嗶？」重複，舊標題後半「旁邊新碼…」在手機上被截掉，利害點落在 18 字之後。上架前要查核：要對照實際上架的劇本，若片中講到 A36 的「約 30%（總碼字）」，可改成「QR Code 沾到咖啡竟然照樣能掃？30% 指的是什麼」之類，但要先確認片中真的有說。 | | | |
| `sothatswhy-b26` |  | 為什麼超市常把牛奶放在最裡面？｜原來如此事務所 → **keep** | 後綴前 15 字；「超市」在前 6 字；只有一個問號；titleProblems 通過（「為什麼」算利害字）。縮圖「兩條路線」不重複。邊緣案例：除了「為什麼」沒有更強的意外字，是公式最弱的一支；這次照「明顯不符才改」保留，可以列為下一輪候選。沒有 i18n 資料夾，八語標題不在 repo。 | | | |
| `sothatswhy-p02-cloud-rain` | rmQ9yD0I6tI | 一朵雲裡約有 500 公噸的水，為什麼不會掉下來？｜原來如此事務所 → **keep** | 一朵雲、500 公噸（claims 有出處）都在前 18 字；一個問號；titleProblems 通過。 | | | |
| `sothatswhy-p05-down-jacket` | BirHcIAlfz4 | 羽絨衣一點熱都不會產生，為什麼穿上就暖？｜原來如此事務所 → **keep** | 羽絨衣在前、「一點熱都不會產生」是意外；titleProblems 通過。 | | | |
| `sothatswhy-p07-fridge-door` |  | 冰箱門打開，房間為什麼不會變涼？｜原來如此事務所 → **keep** | 冰箱門在前、「不會變涼」是反差；titleProblems 通過。 | | | |
| `sothatswhy-p08-popcorn-pressure` |  | 山上滾水煮得慢，玉米為什麼又會爆開？｜原來如此事務所 → **keep** | 山上滾水／玉米兩件事對比；titleProblems 通過。 | | | |
| `sothatswhy-p14-sky-colors` |  | 同一道陽光，天空為什麼是藍的、夕陽卻是紅的？｜原來如此事務所 → **keep** | 同一道陽光、藍與紅的反差；titleProblems 通過。 | | | |
| `sothatswhy-p25-train-tunnel` |  | 高鐵車頭拉那麼長，居然不是為了防風？｜原來如此事務所 → **keep** | 高鐵車頭在前、「居然」在 18 字內；titleProblems 通過。 | | | |
| `sothatswhy-t26` |  | 為什麼日本常端飯碗，韓國卻常放桌上？｜原來如此事務所 → **keep** | 日本／韓國的反差（「卻」）；titleProblems 通過。沒有 i18n 資料夾，八語標題不在 repo。 | | | |

## 八語標題（改標題的兩支）

字幕標記由工具加在最後，括號裡是加上之後的總長。

### `sothatswhy-t27`

| 語言 | 標題 |
| --- | --- |
| en | Japan's missing bins top the complaints. How many of 4,110 chose it? \| So That's Why（97） |
| ja | 日本のゴミ箱不足は困りごと1位、旅行者4110人の何割が選んだ？｜なるほど事務所（45） |
| ko | 일본 쓰레기통 부족이 불편 1위, 여행자 4,110명 중 몇 %가 골랐을까?｜그래서 그랬구나 연구소（61） |
| es | Pocas papeleras en Japón, la queja n.º 1: ¿cuántos de 4.110 viajeros la eligieron? \| Así Funciona（100） |
| pt | Poucas lixeiras no Japão lideram as queixas. Quantos de 4.110 marcaram? \| Agora Entendi（97） |
| id | Jepang minim tempat sampah jadi keluhan no. 1, berapa dari 4.110 turis? \| Oh Begitu Toh（96） |
| vi | Nhật thiếu thùng rác là phiền toái số 1, bao nhiêu trong 4.110 khách chọn? \| Hóa Ra Là Vậy（98） |
| th | ญี่ปุ่นถังขยะน้อยคือปัญหาอันดับ 1 นักท่องเที่ยว 4,110 คนเลือกข้อนี้กี่คน? \| อ๋ออย่างนี้นี่เอง（100） |

### QR Code（不在 repo）

| 語言 | 標題 |
| --- | --- |
| en | A QR code covered in coffee still scans? \| So That's Why（69） |
| ja | QRコード、コーヒーで汚れても読み取れる？｜なるほど事務所（34） |
| ko | QR코드에 커피가 묻어도 그대로 찍힌다고?｜그래서 그랬구나 연구소（42） |
| es | ¿Un código QR manchado de café todavía se escanea? \| Así Funciona（68） |
| pt | QR Code sujo de café ainda funciona? \| Agora Entendi（62） |
| id | QR code kena tumpahan kopi masih bisa dipindai? \| Oh Begitu Toh（72） |
| vi | Mã QR dính cà phê mà vẫn quét được? \| Hóa Ra Là Vậy（59） |
| th | QR Code เปื้อนกาแฟ ยังสแกนได้อยู่อีก? \| อ๋ออย่างนี้นี่เอง（64） |

## 保留的集數：八語後綴只換成定版譯名（給站主決定）

標題本文一字不改，只把結尾的舊系列名換成〈譯名〉的定版名。en、ja 本來就對，不列。

### `sothatswhy-p02-cloud-rain`

| 語言 | 現在 | 只換後綴 |
| --- | --- | --- |
| ko | 구름 하나에 물이 약 500톤, 왜 떨어지지 않을까?｜그래서그랬구나 사무소 | 구름 하나에 물이 약 500톤, 왜 떨어지지 않을까?｜그래서 그랬구나 연구소（48） |
| es | Una nube tiene unas 500 toneladas de agua. ¿Por qué no se cae? \| La Oficina del Por Eso | Una nube tiene unas 500 toneladas de agua. ¿Por qué no se cae? \| Así Funciona（80） |
| pt | Uma nuvem tem umas 500 toneladas de água. Por que não cai? \| Escritório do Ah, É Por Isso | Uma nuvem tem umas 500 toneladas de água. Por que não cai? \| Agora Entendi（84） |
| id | Satu awan berisi sekitar 500 ton air. Kenapa tidak jatuh? \| Kantor Oh Begitu | Satu awan berisi sekitar 500 ton air. Kenapa tidak jatuh? \| Oh Begitu Toh（82） |
| vi | Một đám mây chứa khoảng 500 tấn nước, sao không rơi xuống? \| Văn phòng À ra thế | Một đám mây chứa khoảng 500 tấn nước, sao không rơi xuống? \| Hóa Ra Là Vậy（82） |
| th | เมฆก้อนเดียวมีน้ำราว 500 ตัน ทำไมไม่ร่วงลงมา? \| สำนักงานอ๋อเป็นอย่างนี้ | เมฆก้อนเดียวมีน้ำราว 500 ตัน ทำไมไม่ร่วงลงมา? \| อ๋ออย่างนี้นี่เอง（72） |

### `sothatswhy-p05-down-jacket`

| 語言 | 現在 | 只換後綴 |
| --- | --- | --- |
| ko | 패딩은 열을 전혀 안 내는데, 왜 입으면 따뜻할까?｜그래서그랬구나 사무소 | 패딩은 열을 전혀 안 내는데, 왜 입으면 따뜻할까?｜그래서 그랬구나 연구소（47） |
| es | Una chaqueta de plumas no produce nada de calor. ¿Por qué te abriga? \| La Oficina del Por Eso | Una chaqueta de plumas no produce nada de calor. ¿Por qué te abriga? \| Así Funciona（86） |
| pt | Jaqueta de plumas não gera calor. Por que ela esquenta? \| Escritório do Ah, É Por Isso | Jaqueta de plumas não gera calor. Por que ela esquenta? \| Agora Entendi（81） |
| id | Jaket bulu angsa tak menghasilkan panas. Kenapa bisa hangat? \| Kantor Oh Begitu | Jaket bulu angsa tak menghasilkan panas. Kenapa bisa hangat? \| Oh Begitu Toh（85） |
| vi | Áo lông vũ không tự sinh chút nhiệt nào, sao mặc vào lại ấm? \| Văn phòng À ra thế | Áo lông vũ không tự sinh chút nhiệt nào, sao mặc vào lại ấm? \| Hóa Ra Là Vậy（84） |
| th | เสื้อขนเป็ดไม่สร้างความร้อนเองเลย ทำไมใส่แล้วอุ่น? \| สำนักงานอ๋อเป็นอย่างนี้ | เสื้อขนเป็ดไม่สร้างความร้อนเองเลย ทำไมใส่แล้วอุ่น? \| อ๋ออย่างนี้นี่เอง（77） |

### `sothatswhy-p07-fridge-door`

| 語言 | 現在 | 只換後綴 |
| --- | --- | --- |
| ko | 냉장고 문을 열어 두면, 왜 방이 시원해지지 않을까?｜그래서그랬구나 사무소 | 냉장고 문을 열어 두면, 왜 방이 시원해지지 않을까?｜그래서 그랬구나 연구소（48） |
| es | Abres la puerta del refri y el cuarto no se enfría. ¿Por qué? \| La Oficina del Por Eso | Abres la puerta del refri y el cuarto no se enfría. ¿Por qué? \| Así Funciona（79） |
| pt | Geladeira aberta não esfria a cozinha. Por quê? \| Escritório do Ah, É Por Isso | Geladeira aberta não esfria a cozinha. Por quê? \| Agora Entendi（73） |
| id | Pintu kulkas dibuka, kenapa ruangan tak jadi sejuk? \| Kantor Oh Begitu | Pintu kulkas dibuka, kenapa ruangan tak jadi sejuk? \| Oh Begitu Toh（76） |
| vi | Mở cửa tủ lạnh, sao căn phòng không mát hơn? \| Văn phòng À ra thế | Mở cửa tủ lạnh, sao căn phòng không mát hơn? \| Hóa Ra Là Vậy（68） |
| th | เปิดประตูตู้เย็นไว้ ทำไมห้องไม่เย็นลง? \| สำนักงานอ๋อเป็นอย่างนี้ | เปิดประตูตู้เย็นไว้ ทำไมห้องไม่เย็นลง? \| อ๋ออย่างนี้นี่เอง（65） |

### `sothatswhy-p08-popcorn-pressure`

| 語言 | 現在 | 只換後綴 |
| --- | --- | --- |
| ko | 산에서 끓인 물은 면이 늦게 익는데, 옥수수는 왜 터질까?｜그래서그랬구나 사무소 | 산에서 끓인 물은 면이 늦게 익는데, 옥수수는 왜 터질까?｜그래서 그랬구나 연구소（51） |
| es | En la montaña, el agua hirviendo cuece lento. ¿Por qué revienta el maíz? \| La Oficina del Por Eso | En la montaña, el agua hirviendo cuece lento. ¿Por qué revienta el maíz? \| Así Funciona（90） |
| pt | Na serra o macarrão demora. Por que a pipoca estoura? \| Escritório do Ah, É Por Isso | Na serra o macarrão demora. Por que a pipoca estoura? \| Agora Entendi（79） |
| id | Di gunung mi lama matang, kenapa jagung malah meletup? \| Kantor Oh Begitu | Di gunung mi lama matang, kenapa jagung malah meletup? \| Oh Begitu Toh（79） |
| vi | Trên núi nước sôi mà nấu mì chậm, sao hạt ngô lại nổ bung? \| Văn phòng À ra thế | Trên núi nước sôi mà nấu mì chậm, sao hạt ngô lại nổ bung? \| Hóa Ra Là Vậy（82） |
| th | บนเขาน้ำเดือดแต่ต้มบะหมี่ช้า แล้วทำไมข้าวโพดถึงแตกเป็นป๊อปคอร์น? \| สำนักงานอ๋อเป็นอย่างนี้ | บนเขาน้ำเดือดแต่ต้มบะหมี่ช้า แล้วทำไมข้าวโพดถึงแตกเป็นป๊อปคอร์น? \| อ๋ออย่างนี้นี่เอง（91） |

### `sothatswhy-p14-sky-colors`

| 語言 | 現在 | 只換後綴 |
| --- | --- | --- |
| ko | 같은 햇빛인데, 왜 하늘은 파랗고 노을은 빨갈까?｜그래서그랬구나 사무소 | 같은 햇빛인데, 왜 하늘은 파랗고 노을은 빨갈까?｜그래서 그랬구나 연구소（46） |
| es | La misma luz del sol: ¿por qué el cielo es azul y el atardecer rojo? \| La Oficina del Por Eso | La misma luz del sol: ¿por qué el cielo es azul y el atardecer rojo? \| Así Funciona（86） |
| pt | Mesma luz: por que o céu é azul e o pôr do sol, vermelho? \| Escritório do Ah, É Por Isso | Mesma luz: por que o céu é azul e o pôr do sol, vermelho? \| Agora Entendi（83） |
| id | Sinar matahari yang sama, kenapa langit biru tapi senja merah? \| Kantor Oh Begitu | Sinar matahari yang sama, kenapa langit biru tapi senja merah? \| Oh Begitu Toh（87） |
| vi | Cùng một tia nắng, sao bầu trời màu xanh mà hoàng hôn lại đỏ? \| Văn phòng À ra thế | Cùng một tia nắng, sao bầu trời màu xanh mà hoàng hôn lại đỏ? \| Hóa Ra Là Vậy（85） |
| th | แสงแดดเดียวกัน ทำไมท้องฟ้าสีฟ้า แต่พระอาทิตย์ตกสีแดง? \| สำนักงานอ๋อเป็นอย่างนี้ | แสงแดดเดียวกัน ทำไมท้องฟ้าสีฟ้า แต่พระอาทิตย์ตกสีแดง? \| อ๋ออย่างนี้นี่เอง（80） |

### `sothatswhy-p25-train-tunnel`

| 語言 | 現在 | 只換後綴 |
| --- | --- | --- |
| ko | 고속열차의 긴 코, 사실 공기 저항 때문이 아니라고?｜그래서그랬구나 사무소 | 고속열차의 긴 코, 사실 공기 저항 때문이 아니라고?｜그래서 그랬구나 연구소（48） |
| es | ¿La nariz del tren bala no es por el viento? \| La Oficina del Por Eso | ¿La nariz del tren bala no es por el viento? \| Así Funciona（62） |
| pt | Nariz do trem-bala não é contra o vento? \| Escritório do Ah, É Por Isso | Nariz do trem-bala não é contra o vento? \| Agora Entendi（66） |
| id | Moncong panjang kereta cepat bukan soal angin? \| Kantor Oh Begitu | Moncong panjang kereta cepat bukan soal angin? \| Oh Begitu Toh（71） |
| vi | Mũi tàu cao tốc dài đâu phải để cản gió? \| Văn phòng À ra thế | Mũi tàu cao tốc dài đâu phải để cản gió? \| Hóa Ra Là Vậy（64） |
| th | หัวรถไฟความเร็วสูงยาว ไม่ได้ลดแรงลมเหรอ? \| สำนักงานอ๋อเป็นอย่างนี้ | หัวรถไฟความเร็วสูงยาว ไม่ได้ลดแรงลมเหรอ? \| อ๋ออย่างนี้นี่เอง（67） |
