# 向量嵌入：企劃來源與示範邊界

日期：2026-10-04。對應同目錄 brief.md 的A、B、C三個選項。這是企劃作者的來源備忘；不是獨立 verify-1、劇本核准、模型評測或影音驗收。只有 brief.md、claims-source-notes.md 寫入本集已認領的 source scope。

## 原始文章與今日取證

完整閱讀的站內來源：apps/api/app/guides/content/ai-term-embedding.json；文章是概念與查核入口，沒有逐段拼成新稿。其舊 checked_on 不作為今日官方查核。鄰近語意搜尋與向量資料庫文章僅用於控制不重複的概念範圍。

官方文件／原作者論文已於今日用 web 工具重新開啟與閱讀，另用固定 UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 的唯讀 curl GET 留HTTP、正文內容標記與hash。相同host請求至少間隔1.1秒，檢查前移除HTML註解；沒有付費端點、模型生成或遠端mutation。

| ID | 官方頁／原始研究 | 今日取證UTC | HTTP／exit／正文 | 本集使用範圍 |
| --- | --- | --- | --- | --- |
| P1 | [Embeddings  ／  Machine Learning  ／  Google for Developers](https://developers.google.com/machine-learning/crash-course/embeddings) | 2026-10-04T12:36:50.871887+00:00 | 200／0／成立 | embedding表示、encoding與embedding區別 |
| P2 | [Embeddings: Embedding space and static embeddings  ／  Machine Learning  ／  Google for Developers](https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space) | 2026-10-04T12:36:52.792378+00:00 | 200／0／成立 | 距離是表示中的相對相似；單維通常不易命名；任務不同表示會不同 |
| P3 | [Embeddings: Obtaining embeddings  ／  Machine Learning  ／  Google for Developers](https://developers.google.com/machine-learning/crash-course/embeddings/obtaining-embeddings) | 2026-10-04T12:36:55.659127+00:00 | 200／0／成立 | 嵌入可由訓練或其他方法取得；static/contextual不是固定字詞永遠同坐標 |
| P4 | [Semantic Textual Similarity — Sentence Transformers  documentation](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) | 2026-10-04T12:36:56.568306+00:00 | 200／0／成立 | 嵌入與相似度計算分開；cosine/dot/distance配合設定 |
| P5 | [Semantic Search — Sentence Transformers  documentation](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) | 2026-10-04T12:36:58.680923+00:00 | 200／0／成立 | 查詢/文件使用同一相容空間；某些模型query/document需不同入口；最近鄰先回候選 |
| P6 | [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/html/1908.10084v1) | 2026-10-04T12:36:59.081102+00:00 | 200／0／成立 | 句子嵌入與cosine一種代表方法，非全部架構 |
| M1 | [嵌入向量（Embedding）是什麼：把內容放進可比較的空間](https://mokaair.com/zh-TW/life/ai-term-embedding) | 2026-10-04T12:37:00.185369+00:00 | 200／0／成立 | 既有文章與自有圖解；雨天活動例與讀回條件 |

M1的web工具open回Internal Error；固定UA實際GET回200，文章標題和正文成立。只據此確認公開頁內容，不聲稱瀏覽器、播放器或owner驗收。其餘六個primary頁已由web工具重新閱讀；HTML、effective URL、bytes與SHA在私有JSON。

來源快照收據：`<home>/mokaair-work/ai-series-continuation-20261004/embedding-research-2030.json`；可讀企劃研究為同名 `.md`。兩者是2026-10-04研究，檔名2030不是未來查核年份。完整圖片／影片來源尚未製作，不能列為已有授權付費素材。

## 可用主張

| ID | 可用說法 | 支持與必要界線 |
| --- | --- | --- |
| E01 | 嵌入是可比較的向量表示；此集聚焦文字句段。 | P1、P3、P6。內容編成表示與程式比較分開；不是字數或直接生成答案，不展示假切詞。 |
| E02 | 真實表示可由訓練等方法取得；句子嵌入是其中一類。 | P3、P6。Sentence-BERT作代表研究，不推成全部embedding通用架構，也不說所有表示只靠訓練。 |
| E03 | 單一維度通常不容易直接命名；表示與任務有關。 | P2、P3。本集兩維是人工數值、完全不命名；不能把圖解軸當真實模型內部或可信度維。 |
| E04 | 查詢與資料的表示要在相容空間；同維度本身不足以證明相容。 | P5及既有文章。一些檢索方法使用不同query/document入口，但仍需相容；不一概說同API，也不一概說一定兩API。 |
| E05 | 相似度可用餘弦、內積等方法，需配合所選表示與設定。 | P4。toy只用餘弦，不引用產品預設、通用維度、門檻或正確率。 |
| E06 | 相近描述所選表示與比較的關係，單靠該分數不能完成今日開放查證。 | P2、P4介紹比較；後半為編輯推論與明示toy反例。未找到來源證明『所有模型忽略否定』，不得那樣寫。嵌入可表示條件，這仍不等於向外查證現實。 |
| E07 | 玩具餘弦1.0000不是100%正確機率。 | 公式與本地實算；沒有機率校準步驟。不能從此推成任何產品都未校準，沒有做真實產品評測。 |
| E08 | 本例只查前兩筆沒有匹配；全六筆條件檢查匹配N003。 | 原創toy兩次實跑一致。本例全量精確排序，不是近似查詢、資料庫漏候選或推薦通用k。 |
| E09 | N004、N006缺資訊保持未知，匹配僅指虛構紀錄欄位。 | 原創資料與條件函式；不能把缺欄位當否定或肯定，更不能當真實活動開放證據。 |

## 原創demo的可追查收據

六筆社區手作活動與全部數值由作者原創指定，與既有文章的雨天旅行例或上一集失物記錄分開。原始資料在研究JSON的demo.records，程式在demo.python_source，輸出在demo.execution.output。程式使用標準函式庫；沒有帳號、網路、embedding模型、tokenizer或訓練。

既有Python 3.14.6，2026-10-04本機執行兩次，輸出一致。執行UTC 2026-10-04T12:41:00.254363+00:00。原始碼SHA-256：`9e64621b8b32eb3bdb3c38d6df88911392ae0ca7ea5d36536f5aa0eb9f71a3b3`。Fixture SHA-256：`1104f77855003f038eccf08640ebc728cf8f8e3d7b389af6260846fe40c9e75c`，對query、query_toy_vector、top_k、records作canonical JSON。

| 精確排名 | 四位玩具餘弦 | 條件結果 |
| --- | --- | --- |
| N001 | 1.0000 | REJECT:closed_today |
| N002 | 0.9949 | REJECT:requires_reservation |
| N004 | 0.9878 | UNKNOWN:missing_condition |
| N003 | 0.9762 | MATCH:explicit_conditions |
| N005 | 0.3011 | REJECT:not_indoor |
| N006 | -0.0995 | UNKNOWN:missing_condition |

前兩筆代號 `[N001,N002]`，檢查後 `[]`；全清單檢查 `[N003]`。未知為N004、N006。作者選k=2，不是實際模型／索引設定；所有數字是人工fixture或其實際計算，不冒充官方產品數據。

控制對照固定作者手填 `[1,0]`，僅改open_today欄。before和after餘弦均1.0，條件判定從MATCH變REJECT。沒有變更文字後重新編碼；不證明模型忽略否定句。比較公式只讀向量，條件函式另讀欄位，這個明確程式結構才是反例的範圍。

完整資料與六行排序不是一次顯示的字卡。正式table／terminal分成每卡最多三筆；第一個數字之前先以big與旁白標『人工座標示意，非模型實測』，實算仍保留。中文旁白唸活動名稱與中文術語，不唸代號、指令、英文欄位或網址；共享lexicon不需修改。

## 寫稿前與後續確認

- 三選項鍵A/B/C；各估600秒、約2500口播單位，來自planner策劃估算。不是模型數字或TTS時長。八分鐘正文與成片門檻、十秒章節、五至八秒狀態、插圖至少一半，均須後續媒體實測，不以預估代替。
- 站主立場4／6／7由協調者指定，brief第一行已綁號，第一人稱意見只由來源核對、明示實測／示意、一個觀眾動作形成；協調者於企劃日唯讀GET已核實現行頻道設定相同，沒有編造經驗。
- 尚未實測任何真實embedding模型在繁中、否定句、精確名稱、型號或數字的排序。若要增加，必須先提出新的可審review方案與取得授權，不把本toy當現成性能證據。
- 不報模型、產品的價格、版本、輸入上限、推薦維度或門檻；新增時須查當日primary內容，否則不寫或明示以官網為準。
- 現有diagram為自有©Mokaair素材，官方資料只作事實參照，沒有引用第三方圖片或未明授權的截圖。新插圖與聲音尚未產製。
- 後續選案與來源包由正常outline judge/pull決定；本次沒有寫video.json、metadata、task、共享字典或其他集來源。後續獨立查核仍須另人完成。
