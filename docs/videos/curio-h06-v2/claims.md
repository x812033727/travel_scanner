# H06 v2｜主張、來源與不可越過的界線

**2026-10-14 視覺路線後續變更：**站主在聽審 101 句旁白後，因 MiniMax 小樣反覆出現虛構細節或風格錯誤，指定改為來源圖卡主導的投影片，撤下原先至少 50% 插畫的配置。現行 `video.json` 的 48 個未驗收 `shot` 已逐景改成附來源或標明編輯提問的原生圖卡，保留三張經權利記錄的 `photo` 與四張原創 `diagram`；沒有採用舊 manifest 的生圖。以下第一段是這次轉換前的史料／語音修訂快照，其 `video.json` 雜湊、付費預估及「尚待 TTS／音訊核准」不再描述目前語音狀態。新圖卡須重建時間軸並重新綁定音訊核准；完整來源、圖卡及字幕風險見 [圖卡路線收據](source-card-route-receipt-20261014.md)。

**2026-10-14 最後一行免費窄修：**最新獨立盲審對上一稿的 `no_recap` 判 FAIL：`[v226]` 已直說排除公主身分，片尾 `[d7um]` 又直說她不是安娜塔西亞。站主指定只將 `[v226]` 改為「回到開場那兩份檢體：它們提供母系線索，卻不能獨自鎖定另一個本名。」；`[fa8j]` 與皇后已知母系參照未對上的句文及片尾答案均保留，`v226.pause_after_ms=0` 亦不變。現行 `video.json` SHA-256 `c0e4c948b9f1fd3cb628992ab325700eae9dff716ff65c7163ab5de194e9e21b`、敘事 hash `12dccbe87d74918d`；82 景、101 句，其中 99 句沿用已核樣本數的原 WAV，`fa8j`／`v226` 尚待站主核准的各一次 TTS。以 99 句原 WAV 與兩句文字語速混合投影，正文 **14,670 格／489 秒（8:09.00）**、planned shot **7,464／14,670 格＝50.8793%**；`v226` 畫面預估 7.7 秒，`cadenceProblems=[]`，但新 TTS 後必須按實際 WAV 重算。前次 FAIL 原件、新純盲審輸入與前後收據見[最後一行修稿補記](dna-payoff-last-line-20261014.md)及 `<home>/mokaair-work/videos/curio-h06-v2/review/dna-payoff-last-line-20261014T054614Z/`。新版獨立盲審、TTS、正式時間軸重綁與站主音訊核准仍待後續；來源及成片畫面關卡不因這次改文而放寬。

本表對應 `video.json` 的 `claims` 代號。v2 改寫了敘事順序與旁白，**不能沿用舊版 H06 的逐句查核或站主核准**。舊版的 [第一輪](../curio-h06/verify-1.md)與[第二輪](../curio-h06/verify-2.md)查核可作前案線索；v2 原有獨立覆核見本集 [verify-1.md](verify-1.md)。先前的盲評、時間軸與音訊核准均為歷史紀錄，不代表現行稿已通過。原先 104 句配音有 8 句經本地 Whisper medium 第二意見留下旗標；現行保留的原 WAV 仍須獨立聽審。來源抽查不代替成圖與成片稽核。逐檔收據與視覺計畫另見 [visual-pilot-01.md](visual-pilot-01.md)、[verification-notes.md](verification-notes.md)及 [運河圖卡交接](native-canal-cards-20261014.md)。

| ID | 影片使用的主張 | 可核來源與界線 |
| --- | --- | --- |
| c01 | 尼古拉二世夫婦及五名子女一九一八年遭處決；片中只用來說明後來的倖存傳聞。 | [PLOS ONE 2009 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) 摘要及導論；不重演處決。 |
| c02 | 一九二〇年女子從柏林運河獲救、拒報身分，警方未查出本名。 | [法院判決第三方掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) PDF 第 5–6 頁；[CSUEB 博物館解說](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html)。影片只報年、月，不報爭議中的救援細節。 |
| c03 | 一九二二年病院裡有人把她與安娜塔西亞連在一起；誰先說出名字，判決保存兩種記述。 | [法院掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) PDF 第 6 頁。開場 `[dszz]` 不指訪客或安德森為第一個說出名字的人；CSUEB 頁使用單一起點敘述，不能蓋過判決的分歧記載。 |
| c04 | 皇室遠親一九二八年接待她，另有親近皇室的人否認她的公主身分；接待和辨識都不是身分鑑定。 | [TIME 1928 同期報導](https://time.com/archive/6662258/russia-whose-body/)；[法院掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) PDF 第 7 頁和證詞部分。不把個人看法說成整個家族共識。 |
| c05 | 安德森提起的是民事財產及繼承權請求，公主身分是前提；請求包括給付、確認繼承權及舊繼承證書有誤。 | [法院掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) PDF **第 13 頁**三項訴請。不是刑事詐欺判決；不報未核金額。 |
| c06 | 一九六七年前審對她的公主主張作不利證據評價；安德森提起法律審後，一九七〇年德國聯邦最高法院駁回，維持公主身分未獲證明。 | [法院掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) PDF 第 3、143–144 頁。正文先講前審，再講法律審；法律審檢查前審的法律及程序，不重問每位證人。 |
| c07 | 被告提出失蹤女工 Franziska Schanzkowska 身分說法；法院未在該案裁定安德森是不是她，也未裁定安德森主觀動機。 | [法院掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) PDF 第 138–139 頁。不能把未裁定事項寫成肯定身分或詐欺意圖。 |
| c08 | 安德森一九八四年過世，DNA 身分研究一九九五年一月發表。 | [Nature Genetics 書目](https://www.nature.com/articles/ng0195-9)、[PubMed 書目](https://pubmed.ncbi.nlm.nih.gov/7704032/)、[CSUEB 解說](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html)。論文正文付費；不要把一九九四年當發表年。 |
| c09 | 頭髮與醫院保存組織由不同團隊分析，先比較兩份檢體的母系序列，結果彼此相符，但不符皇后已知母系參照，強力排除她是安娜塔西亞。開場 `[v203]` 只問檢體能否說出身分，正文 `[bp4e]` 才交代比較方法，`[4yw7]` 才給兩份檢體彼此相符的結果；`[fa8j]` 指明兩份檢體都不符**皇后已知母系參照**，`[v226]` 點名回扣開場兩份檢體，只說它們提供母系線索而不能獨自確證另一個本名；片尾 `[d7um]` 才明說人物結論「她不是安娜塔西亞」。 | [共同研究者 Stoneking 第一手訪談](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)、[CSUEB 解說](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html)。訪談不是 Nature Genetics 原文，不報未核機率。 |
| c10 | 排除公主身分，與支持另一個候選身分，是不同層級的主張。 | c07、c09、c19–c20 的**編輯界線**；不能把法院沒有裁定的事說成法院結論，也不能省略毛赫爾的陽性母系線索。 |
| c11 | 第一座墓七〇年代末被找到但一九九一年才正式發掘；九具遺骸包括父母、三名女兒及四名隨行人員，仍少一男一女。 | [PLOS ONE 導論](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)。發現與官方發掘不可合併成年份一九九一年。 |
| c12 | 第一墓發現後幾次尋找附近第二墓都未果；二〇〇七年業餘考古者先在俄國林地發現碎片，正式調查隨後進場；該批碎片來自第一墓約七十公尺外的第二墓，正式整理出四十四件骨及牙碎片。 | [PLOS ONE 摘要與導論](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)。`[dm7x]` 是原研究導論記載的搜尋過程；開場 `[pxbi]` 停在碎片，正文 `[v2jq]` 先以業餘發現者的畫面點名第二墓；`[v219]` 才畫正式測繪。不畫真實遺骸的假照片。 |
| c13 | 第二墓 DNA 以母系、常染色體及 Y-STR 比對家族關係，辨出阿列克謝與一名姊妹。 | [PLOS ONE 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)。影片用白話描述各比對回答的親緣問題。 |
| c14 | 俄方與美方人類學者對第一墓缺的是瑪麗亞或安娜塔西亞有不同判讀；PLOS ONE 明說該篇所報 DNA 結果無法單獨區分第二墓姊妹的個別姓名。 | [PLOS ONE Introduction 與 Discussion](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)。表格的人骨暫定標籤不可蓋過正文限制；不能把早年的形態判讀寫成 DNA 已證實的墓位。 |
| c15 | 另一篇二〇〇九年家族研究認定尼古拉二世夫婦五名子女均在兩座墓中，無人於一九一八年處決中生還。 | [Rogaev 等 PNAS 原文](https://www.pnas.org/doi/10.1073/pnas.0811190106)；[PubMed 索引](https://pubmed.ncbi.nlm.nih.gov/19251637/)。只說家族五人到齊，不用它替 PLOS 的個別姊妹墓位作確證。 |
| c16 | 一九七〇年法院、一九九五年檢體、二〇〇九年家族研究回答不同問題；這是把原始材料並列後的敘事判讀。 | c05–c06、c09、c14–c15；標為**編輯推論**，不得當作法官或研究者逐字結論。 |
| c17 | 安德森當年主觀上怎麼理解或接受公主名字，現有本集證據不足以判定。 | [法院掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)判決範圍及上述實驗的回答範圍；**證據界線**，不做心理診斷。 |
| c18 | 地質學家 Alexander Avdonin 在七〇年代末找到第一墓；他和少數朋友保密地點直到一九九一年。 | [PLOS ONE 2009 原文導論](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)。v2 新增主張，見 `grave-map-table`；正式發掘的年份仍屬 c11。 |
| c19 | 安德森的母系序列與 Carl Maucher 的樣本相符；Maucher 是 Franziska Schanzkowska 的母系旁系親屬，結果支持安德森可能就是那名失蹤女工。 | [Cold Spring Harbor DNA Learning Center 教師指南原件第 24–25 頁](https://www.dnai.org/romanovs/romanov_guide.pdf)明載與 Maucher 有母系關係；[同機構工作簿第 11 頁](https://dnalc.cshl.edu/assets/files/dnalc-live/17207.the_mystery_of_anastsia_workbook.pdf)註明 Maucher 是 Schanzkowska 的母系姪孫。1995 年[原研究書目](https://www.nature.com/articles/ng0195-9)可確認作者與刊期，但正文付費，不能說已直接從原研究逐字核到結果。 |
| c20 | 母系 DNA 由同一母系的親屬共享，相符可支持家族線索，但單憑它不能唯一鎖定一人的本名。 | [美國司法部 NIJ 法醫 DNA 教材](https://nij.ojp.gov/nij-hosted-online-training-courses/principles-forensic-dna-officers-court/08-mitochondrial-dna-y-str-analysis/introduction-mtdna/maternal-inheritance-0)說明 mtDNA 不是唯一個人識別碼。此界線也適用於 c19；`[v226]` 只把兩份檢體接回母系線索與個人識別限制，不能把相符說成身分的單一終局證明；排除公主身分的人物答案留給片尾 `[d7um]`。 |

## 製作與畫面界線

照片的作者、項目、授權及原圖位元組雜湊列在 [assets-provenance.md](assets-provenance.md)。五張已核候選照中，現行腳本安排三張 `photo` 卡，只有這三張列在 `video.json.assets[]`；未使用的兩張仍保留外部原圖與來源記錄，避免上架包誤列未入片圖片。照片卡明示歷史照片與劇情事件的關係，不把舊照當成二〇年代救起、庭審、檢體或墓地現場。現行視覺用有來源的原生卡與原創圖解，不重建可辨安德森臉部、遺骸或法院原件；`berlin-staff-corridor.data.sub` 和影片說明已改成圖卡來源及編輯圖解揭露。`dna-two-results` 顯示兩份檢體先彼此相符；`dna-mismatch` 比的是**皇后已知母系參照**，而 `dna-maucher-match` 對上的是**尚茨科夫斯卡的母系親屬毛赫爾**，後者支持線索卻不能單獨確定本名。旁白、畫面、成片與上架仍需各自的關卡，不能以本次預檢代替。
