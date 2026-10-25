# ForTy ko / es 獨立翻譯審稿

結論：ko ready；es ready after 1 個小幅語義明確化修正（ecb8），另有 1 個低優先語法修飾（yiya）。沒有數字、座標、年份、否定、算步或核心分數語義的錯誤。afyy 新問句已補讀通過，不是整體失敗。

審稿者沒有翻譯 ko / es，沒有讀取或引用作者的 self-critique 作為審查依據。逐句比對實際 source 與合併後譯文，另讀 caption-review.md、claims.md、lexicon 對應詞、worksheet glossary / boundaries 及 source metadata。只寫本報告，未改 repo / todo / 音訊。

## 綁定實際檔案

以下均為檔案原始 bytes 的 SHA-256，不是 Git commit：

| 檔案 | SHA-256 |
| --- | --- |
| /workspace/work/travel-scanner-forty/docs/videos/forty-forest-map/video.json | a62a48382272fb4b9171f2c261b8f736c7516afca35417ccaa842757b04f8a6f |
| /workspace/work/travel-scanner-forty/docs/videos/forty-forest-map/i18n/ko.json | 97ca7ad938f97579badc6694deb11134da1218b616ae4a5c7381caef00a2c84a |
| /workspace/work/travel-scanner-forty/docs/videos/forty-forest-map/i18n/es.json | ceb4c1d128a8e68d8ce4c7c7f7906173235c070f40de933fe9c61590eab7d1d3 |

首讀時兩語各 91 條，afyy 因 source 更新而被 stale guard 排除。root 原生合併新問句後，只補讀新 afyy；其餘 91 句沿用已逐句完成的審查。最終實際檔案兩語皆為 92 / 92，沒有缺 ID；逐條 source_hash 均等於當前 source 的 SHA-256 前 12 字元。afyy 的 source_hash 為 9902ddfcb5ec。

## 修正清單

| locale / ID | 種類與問題 | current | suggested |
| --- | --- | --- | --- |
| es / ecb8 | meaning，小幅明確化：原句「類別名稱仍要逐項對回」要求每個值與其類別對應；目前只說核對每個類名，沒有明說與值對回。這個差異會削弱「總和正確仍不能代替欄位對齊」的操作提醒。 | Si no suma bien, revisa omisiones y decimales; coteja cada nombre de clase. | Si no cuadra, revisa omisiones y decimales; coteja cada valor con su clase. |
| es / yiya | readability，低優先語法：第一個名詞的複數冠詞 Los 不宜直接帶到單數抽象名詞 agroforestería；第二項補 la 更自然。所有實體、否定及數字不變。 | Los cultivos arbóreos y agroforestería incluyen palma aceitera, caucho y huertos; dan productos agrícolas no madereros. | Los cultivos arbóreos y la agroforestería incluyen palma aceitera, caucho y huertos; dan productos agrícolas no madereros. |

ecb8 建議為 75 字元，比在原句後再加長解釋更適合後續預算；保留總和不對、漏項、小數位、逐值對類別四個要素。yiya 只增加 3 字元，屬語法修飾，沒有視作事實或核心語義失敗。

ko 沒有需修改的現存譯句；不為湊修正數量另造風格要求。

## afyy 單句差異覆核

source：把第二格填進紀錄前，這六個分數也能加回一嗎？

- ko current：2번째 격자를 기록하기 전, 이 6개 점수도 더하면 1이 됩니까?
- es current：Antes de registrar la segunda celda, ¿estas 6 puntuaciones también suman 1?

兩句皆自然且保義：第二格、記錄前、6 分數、也、加總 1 與問句均保留。ko 使用 합니다체 的問句；es 使用自然的中性拉美語序。這兩句就是本次建議，可維持。接續 f2ze / ckag / n37p 的三步加法能直接回答它。

## 全部字幕的實際覆蓋

下面按當前 source 的章節順序列出全部 92 個 ID；每個 ID 的 ko / es 都已對照 source。除上表 es ecb8、yiya 外，其餘沒有需改問題；afyy 是後補讀的唯一差異。

| 章節 | 句數 | 已對照的全部 ID |
| --- | --- | --- |
| 讀出一個台灣綠格 | 5 | 8aw6, gngj, ep85, jw6i, 5ur9 |
| 把綠色對回六種類型 | 16 | m2p6, erqz, t4w3, 66nz, 3pse, v9fh, 7id9, 2vcb, yiya, rrgq, fbc5, gsa7, 9wmz, jkby, 5nt9, m8cb |
| 找到指定格的五個值 | 10 | p2ry, u5js, 7732, yi97, 2k27, vk36, gfes, e826, svhy, 3gwz |
| 補出第六類，選出最高 | 18 | 7iv8, bxdi, anxa, up9r, 3p97, 4av2, 8hpb, ywu9, u362, eym7, k3i2, p9sg, dkq3, w86h, wh49, 6ybg, xxju, endc |
| 換一格，再算六類分數 | 26 | appe, beg8, fe8z, ymf8, 54sx, mfsh, 578j, 97h6, 8mtz, 4amm, ux8j, y64h, afyy, f2ze, ckag, n37p, ecb8, 8k4a, z33x, wnrz, ywz8, ww8v, mx7g, 7qfx, hbci, sbkg |
| 把分數和年份寫進紀錄 | 14 | upmh, vb62, 8m2e, bs4s, ci5j, 6ss6, rume, pvkj, ncx4, j5kv, nqyj, wfb2, 88pk, bu6j |
| 完成一列像素紀錄 | 3 | hr4b, 4w7g, 39nc |

### 重點事實與語義核對

- 六類沒有混併：ko 的 원시림 / 자연갱신림 / 식재림 / 집약 조림지 / 수목 작물·혼농임업 / 기타 토지 可辨識；es 的 bosque primario / bosque de regeneración natural / bosque plantado / plantación forestal / cultivos arbóreos y agroforestería / otras tierras 可辨識。OtherLand 沒有被誤譯成沒有樹的裸地。
- 人工建立類別的兩側條件保留：超過 40 年，以及 40 年或以下；輪伐期沒有改成現在樹齡。原始林的原生樹種及無可見干擾、自然更新中的次生林、非木材農產品、其他土地也可有樹等條件均有保留。
- A 輸入完整為 [0, 248, 0, 0, 0]；加總 248、250−248=2、有效範圍 0–250、除以 250、0.992 / 0.008 / 其餘 4 類為 0、六項和 1、唯一最高皆完整。
- B 輸入完整為 [0, 86, 0, 1, 77]；86+1+77=164、250−164=86、兩項 86 並列、0.344 / 0.004 / 0.308 / 另外兩類 0 均完整。刻意挑最低最大分數，不是隨機精度抽樣，沒有被改成代表全圖。
- 新增 B 驗算完整：0.344+0.344=0.688；再加 0.308=0.996；最後加 0.004=1；另外兩類的 0 不改變總和。ko / es 都沒有省掉中間值或把此驗算說成校準或精度證據。
- 250 總量與 255 無資料角色沒有互換；排除無資料、零為有效值的操作含義保留。248 沒有變成棵數或平方米。
- A 的請求位置 121.4°E / 24.7°N、B 的指定像素中心 121.42234°E / 24.69528°N 保留正確方向與所有小數位；未改為窗口幾何中心或地面真值。10×10 窗口及名目 10m 輸出也保留。
- argmax 選類別並省略完整分數、並列不會自行消失、此衍生圖按類別順序取第一個最高者、記錄須保留全部最高者等機制完整；沒有把本片規則泛稱官方硬分類層規則。
- 分數和實際正確率分開：尚未事後機率校準、需要獨立參考、不能直接說 99.2% 判對、土地歷史 / 經營用途仍需參考資料均保留。沒有把 0.992 改成已知正確率。
- 2020 是基準資料年；五月公開、正式論文 10 月 21 日、早期年度序列 2017–2025 均無數字變動。metadata 明寫 2026 年 10 月的介紹及早期序列另行區分；沒有捏造這兩格的年度變化量測。
- ForTy / DeepMind / AlphaEarth / Google、AI / CC、Forest Typology 2020 (v1) 拼字或縮寫符合 glossary；沒有把產品名音譯。第一句保留作者第一人稱。

## Metadata 全項覆蓋

兩語皆已逐項對照 title、整篇 description、完整 tags、7 個 chapter 名及 thumbnail 的 tag / headline / sub。不是只查字幕或只查 metadata 的字元數。

| 檢查 | ko | es |
| --- | --- | --- |
| title | 38 字元，主題 / Taiwan 2 pixels / 6 類計算一致 | 68 字元，主題 / Taiwán 2 píxeles / 6 類計算一致 |
| chapters | 7 / 7，最長 17 字元 | 7 / 7，最長 28 字元 |
| tags | 50 字元；無頻道名 | 103 字元；無頻道名 |
| thumbnail | 3 欄齊全；**녹색** 強調及 2 行；5 值 / 6 類正確 | 3 欄齊全；**VERDE** 強調及 2 行；5 值 / 6 類正確 |
| description | 本文全部條件、來源、授權與改作說明保留 | 本文全部條件、來源、授權與改作說明保留 |
| 外連 | DOI、CC BY 4.0、GitHub 三個完整 URL 與 source 一致 | DOI、CC BY 4.0、GitHub 三個完整 URL 與 source 一致 |

description 的 Neumann 等 (2026)、資料版本、B 刻意選樣、2020 / early annual 界線、裁切 / 補數 / 取首 / 重繪、無衛星底圖皆核對，沒有漏掉授權或資料包連結。

## Cue、語域與預算

worksheet 指定的 4av2、z33x、8m2e 三個多 cue 邊界，ko / es 均維持 source 子句順序：先範圍再總和、先壓成標籤再說並列、先獨立參考再對比真實結果。沒有提前或延後一個 cue 才讀出數字的重排。

當時 /workspace/work/videos/forty-forest-map/captions/zh-TW.srt 尚不存在，所以沒有宣稱逐個實際 SRT 時碼或 dub fit 已通過；cue 次序以實際 worksheet boundaries 檢查。worksheet 的 92 句皆未提供 max_chars，硬 budget 問題目前為 0 / 不適用，仍需以 root 後續實測預算檢查。

ko 的 합니다체 一致，es 的 tú 語域一致，沒有 vosotros / voseo 或其他文字系統混入。軟性字數建議以上：ko 20 句超過約 40 字元，最長 53；es 28 句超過約 80 字元，最長 125。這是完整複句的字數，工具仍會拆 cue，且未有 max_chars，因此不把它們一律當作不合播放長度；本輪沒有為縮字而建議省略算步或否定。

最終分類計數：ko meaning 0 / facts 0 / glossary 0 / cue order 0 / readability 0 / budget 0（未提供）/ metadata 0 / thumbnail 0；es meaning 1（小幅對回關係明確化）/ facts 0 / glossary 0 / cue order 0 / readability 1（低優先語法）/ budget 0（未提供）/ metadata 0 / thumbnail 0。afyy 兩語均已完成單句差異覆核，不再列待修。
