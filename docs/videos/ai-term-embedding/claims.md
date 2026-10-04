# 嵌入向量：逐項主張與證據

撰稿日：2026-10-04。本文是作者證據清單，尚未獨立查核或影音驗收。所有社區活動、人物與向量為作者原創示意；實際執行的僅是標準函式庫數學與顯式欄位程式，沒有任何模型、tokenizer、網路、ANN或產品評測。

官方來源今日重新開啟與閱讀；editorial-UA HTTP／正文與快照收據在claims-source-notes.md與私有研究JSON。本集原創DATA與實算只引用demo.py／demo-log.md，不將數字冒充官網產品性能。

格式：主張ID｜主張｜官方URL或原創證據｜查核／實算日期｜scene IDs。一般機制、編輯推論、原創資料與意見各明示範圍。

c1｜社區活動、人物與畫面是原創虛構故事，不是營業資訊。｜原創企劃 brief.md／demo.py／demo-log.md；原創或站主立場，無外部官方數據｜2026-10-04｜closed-door-hook、closed-workshop、toy-disclosure、neighbors-compare、empty-seat、expectation-first、latch-reveal、material-but-no-class、reservation-seat、return-to-note、no-confidence-meter、clear-role-first、market-materials、cloth-relationships、basket-sorting、same-items-other-uses、metaphor-boundary、courtyard-dowels、dowel-direction、angle-not-venue、not-a-longer-is-truer、lower-score-can-match、community-hall-review、one-clay-bowl、paper-table-lower-rank、candidate-setting、same-vector-control、tailor-patterns、different-origins、length-is-not-map、garden-next-step、do-not-fill-empty、toy-match-not-real-place、answer-locked-door
c2｜嵌入將內容表示成一組可比較的數值；此集聚焦文字句段。｜https://developers.google.com/machine-learning/crash-course/embeddings；https://developers.google.com/machine-learning/crash-course/embeddings/obtaining-embeddings；https://arxiv.org/html/1908.10084v1；P1、P3、P6｜2026-10-04｜first-chapter-question、embedding-representation、market-materials、different-wording、task-shaped-materials、one-bundle-focus、not-characters-count、not-a-word-count、architecture-scope、representation-workflow、query-also-represented、representation-not-answer
c3｜真實表示可由訓練等方法形成；句子嵌入為代表應用，不是全部嵌入通用架構。｜https://developers.google.com/machine-learning/crash-course/embeddings/obtaining-embeddings；https://arxiv.org/html/1908.10084v1；P3、P6｜2026-10-04｜one-bundle-focus、learned-not-labels、not-fixed-glossary、sentence-method-example、architecture-scope、task-changes-organizing、real-versus-toy、axis-careful
c4｜表示、比較、使用結果是不同步驟；嵌入不是直接生成回答。｜https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html；https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html；P4、P5；機制區分與既有文章｜2026-10-04｜not-characters-count、not-a-word-count、representation-workflow、compare-is-separate、use-result-separate、representation-not-answer、no-answer-from-vector
c5｜單一維度通常不易直接命名，不能自行指定為可信度；不是所有軸永遠不可解釋。｜https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space；https://developers.google.com/machine-learning/crash-course/embeddings/obtaining-embeddings；P2、P3｜2026-10-04｜task-changes-organizing、same-items-other-uses、not-a-longer-is-truer、direction-versus-origin、axes-interpretation、not-confidence-axis、axis-careful、no-dimensions-buying-rule
c6｜相似度方式需要配合表示；此玩具使用餘弦方向比較。｜https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html；P4／原創demo.py｜2026-10-04｜clear-role-first、compare-is-separate、second-chapter-question、similarity-not-conditions、courtyard-dowels、dowel-direction、cosine-chosen、equal-direction、cosine-formula、metric-varies、compatible-metric、score-context、metric-normalization
c7｜查詢與文件須在相容表示空間；同維度本身不足以保證相容。｜https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html；P5／既有文章；相容性編輯推論｜2026-10-04｜representation-workflow、query-also-represented、representation-not-answer、fourth-chapter-question、compatible-space、tailor-patterns、different-origins、length-is-not-map、same-dimension-not-space、new-map-old-data、number-still-computable、check-pairing、check-compatible-parts、entry-point-nuance、keep-original-evidence、scope-not-deploy
c8｜某些檢索模型區分query/document入口，並非所有模型都要求同API或固定兩API。｜https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html；P5｜2026-10-04｜check-compatible-parts、query-document-not-identical、compatible-can-differ、entry-point-nuance
c9｜分數、門檻依表示與比較方式而變；不給通用門檻或維度推薦。｜https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html；https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html；P4、P5；由配套設定作編輯推論｜2026-10-04｜compatible-metric、score-context、fourth-chapter-question、compatible-space、new-map-old-data、check-pairing、check-compatible-parts、metric-normalization、no-universal-cutoff、no-dimensions-buying-rule
c10｜作者手填全部六筆向量，無模型、切詞、訓練或聯網；兩維不命名。｜原創demo.py／demo-log.md／brief.md；原創或站主立場，無外部官方數據｜2026-10-04｜closed-door-hook、toy-disclosure、wet-shoe-pause、not-fixed-glossary、metaphor-boundary、toy-skips-encoding、real-versus-toy、do-not-overclaim、angle-not-venue、cosine-chosen、cosine-formula、direction-versus-origin、score-does-not-prove、same-toy-score-different-condition、rerun-same-records、one-paper-object、rank-first-half、separate-rank-from-condition、rank-last-half、expand-check-scope、no-model-benchmark
c11｜原創六筆的活動描述及室內、今日開放、預約欄位如保存資料；缺欄位明示null。｜原創demo.py DATA／demo-log.md；原創或站主立場，無外部官方數據｜2026-10-04｜neighbors-compare、empty-seat、need-three-conditions、latch-reveal、highest-but-closed、reservation-seat、missing-opening、three-known-statuses、lower-score-can-match、rerun-same-records、community-hall-review、one-paper-object、fixture-first-half、one-clay-bowl、fixture-second-half、wood-block-wait、read-before-run、paper-table-lower-rank、rank-last-half、read-the-necessary-bit、answer-locked-door
c12｜精確排序N001、N002、N004、N003、N005、N006；四位分數1.0000、0.9949、0.9878、0.9762、0.3011、-0.0995。｜原創demo.py實跑／demo-log.md；原創或站主立場，無外部官方數據｜2026-10-04｜latch-reveal、highest-but-closed、do-not-overclaim、near-one-not-probability、lower-score-can-match、read-before-run、rank-first-half、separate-rank-from-condition、paper-table-lower-rank、rank-last-half
c13｜作者指定k=2，只檢查前兩筆為空；查全六筆得到N003。未執行ANN、向量庫或reranker。｜原創demo.py實跑／demo-log.md；原創或站主立場，無外部官方數據｜2026-10-04｜lower-score-can-match、third-chapter-question、paper-table-lower-rank、candidate-setting、top-two-check、empty-result-explained、expand-check-scope、all-records-check、exact-ranking-boundary、no-universal-fix
c14｜N004、N006保留UNKNOWN；MATCH只符合虛構欄位，不是真實營業證據。｜原創demo.py condition／demo-log.md；原創或站主立場，無外部官方數據｜2026-10-04｜missing-opening、three-known-statuses、fixture-second-half、wood-block-wait、rank-first-half、separate-rank-from-condition、rank-last-half、not-inferred-truth、all-records-check、do-not-fill-empty、toy-match-not-real-place
c15｜固定作者向量[1,0]，只改open_today，餘弦同為1.0而MATCH變REJECT；未改文字重新編碼。｜原創demo.py metadata_change_same_vector／demo-log.md；原創或站主立場，無外部官方數據｜2026-10-04｜same-toy-score-different-condition、same-vector-control、metadata-only-control、not-text-reencoding
c16｜本toy的餘弦值不是正確機率；1.0000不代表100%正確。不能推成全部產品未校準。｜原創公式與demo-log.md；數學邊界；原創或站主立場，無外部官方數據｜2026-10-04｜highest-but-closed、not-a-longer-is-truer、near-one-not-probability、score-does-not-prove、metadata-only-control
c17｜相近是所選表示與比較下的相對關係；單靠分數不完成現實時效與條件查證。｜https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space；https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html；P2、P4／原創反例；明示編輯推論，非所有模型否定句能力結論｜2026-10-04｜closed-workshop、expectation-first、material-but-no-class、return-to-note、no-confidence-meter、use-result-separate、representation-not-answer、no-answer-from-vector、angle-not-venue、cosine-formula、score-does-not-prove、same-toy-score-different-condition、do-not-throw-away-score、one-clay-bowl、keep-original-evidence、remember-the-locked-door、source-can-be-stale、answer-locked-door
c18｜站主採回讀來源、不把未測說成實測、給一個觀眾動作的觀點。｜核准brief.md stance4、6、7；協調者今日GET設定一致；原創或站主立場，無外部官方數據｜2026-10-04｜no-real-product-test、fifth-chapter-question、viewer-original-conditions、garden-next-step、one-viewer-action、do-not-fill-empty、what-the-score-did、answer-and-article
c19｜此toy排序不證明實際模型相同排序、忽略否定的頻率或資料庫漏候選。｜demo程式範圍；無模型評測或產品性能主張；原創或站主立場，無外部官方數據｜2026-10-04｜toy-disclosure、no-confidence-meter、real-versus-toy、do-not-overclaim、no-real-product-test、top-two-check、exact-ranking-boundary、no-universal-fix、no-model-benchmark、not-text-reencoding、no-dimensions-buying-rule、scope-not-deploy、toy-match-not-real-place
c20｜同義說法能否對應，受所選表示與任務影響；示例是語言改寫，不是模型實跑。｜https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space；https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html；P2、P5；原創中文改寫示意｜2026-10-04｜cloth-relationships、basket-sorting、different-wording、task-shaped-materials
c21｜相對最高分仍不等於符合需求或充分證據；是否採用要回讀原文必要條件。｜https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html；原創toy／P5；編輯推論與觀眾方法｜2026-10-04｜need-three-conditions、return-to-note、do-not-throw-away-score、empty-result-explained、no-universal-fix、keep-original-evidence、remember-the-locked-door、fifth-chapter-question、viewer-original-conditions、garden-next-step、read-the-necessary-bit、one-viewer-action、source-can-be-stale、what-the-score-did、answer-and-article
c22｜Mokaair既有嵌入文章與自有圖解已讀，公開頁今日200且標題正文成立。｜https://mokaair.com/zh-TW/life/ai-term-embedding；M1；來源取證在claims-source-notes.md｜2026-10-04｜representation-workflow、article-at-example、answer-and-article

## 每個scene的主張對照

| scene | claims |
| --- | --- |
| closed-door-hook | c1、c10 |
| closed-workshop | c1、c17 |
| toy-disclosure | c1、c10、c19 |
| wet-shoe-pause | c10 |
| neighbors-compare | c1、c11 |
| empty-seat | c1、c11 |
| need-three-conditions | c11、c21 |
| expectation-first | c1、c17 |
| latch-reveal | c1、c11、c12 |
| highest-but-closed | c11、c12、c16 |
| material-but-no-class | c1、c17 |
| reservation-seat | c1、c11 |
| missing-opening | c11、c14 |
| three-known-statuses | c11、c14 |
| return-to-note | c1、c17、c21 |
| no-confidence-meter | c1、c17、c19 |
| clear-role-first | c1、c6 |
| first-chapter-question | c2 |
| embedding-representation | c2 |
| market-materials | c1、c2 |
| cloth-relationships | c1、c20 |
| basket-sorting | c1、c20 |
| different-wording | c2、c20 |
| task-shaped-materials | c2、c20 |
| one-bundle-focus | c2、c3 |
| not-characters-count | c2、c4 |
| not-a-word-count | c2、c4 |
| learned-not-labels | c3 |
| not-fixed-glossary | c3、c10 |
| sentence-method-example | c3 |
| architecture-scope | c2、c3 |
| task-changes-organizing | c3、c5 |
| same-items-other-uses | c1、c5 |
| metaphor-boundary | c1、c10 |
| representation-workflow | c2、c4、c7、c22 |
| query-also-represented | c2、c7 |
| compare-is-separate | c4、c6 |
| use-result-separate | c4、c17 |
| representation-not-answer | c2、c4、c7、c17 |
| no-answer-from-vector | c4、c17 |
| toy-skips-encoding | c10 |
| real-versus-toy | c3、c10、c19 |
| do-not-overclaim | c10、c12、c19 |
| second-chapter-question | c6 |
| similarity-not-conditions | c6 |
| courtyard-dowels | c1、c6 |
| dowel-direction | c1、c6 |
| angle-not-venue | c1、c10、c17 |
| cosine-chosen | c6、c10 |
| equal-direction | c6 |
| not-a-longer-is-truer | c1、c5、c16 |
| cosine-formula | c6、c10、c17 |
| direction-versus-origin | c5、c10 |
| axes-interpretation | c5 |
| not-confidence-axis | c5 |
| axis-careful | c3、c5 |
| metric-varies | c6 |
| compatible-metric | c6、c9 |
| score-context | c6、c9 |
| near-one-not-probability | c12、c16 |
| score-does-not-prove | c10、c16、c17 |
| no-real-product-test | c18、c19 |
| same-toy-score-different-condition | c10、c15、c17 |
| lower-score-can-match | c1、c11、c12、c13 |
| do-not-throw-away-score | c17、c21 |
| third-chapter-question | c13 |
| rerun-same-records | c10、c11 |
| community-hall-review | c1、c11 |
| one-paper-object | c10、c11 |
| fixture-first-half | c11 |
| one-clay-bowl | c1、c11、c17 |
| fixture-second-half | c11、c14 |
| wood-block-wait | c11、c14 |
| read-before-run | c11、c12 |
| rank-first-half | c10、c12、c14 |
| separate-rank-from-condition | c10、c12、c14 |
| paper-table-lower-rank | c1、c11、c12、c13 |
| rank-last-half | c10、c11、c12、c14 |
| not-inferred-truth | c14 |
| candidate-setting | c1、c13 |
| top-two-check | c13、c19 |
| empty-result-explained | c13、c21 |
| expand-check-scope | c10、c13 |
| all-records-check | c13、c14 |
| exact-ranking-boundary | c13、c19 |
| no-universal-fix | c13、c19、c21 |
| no-model-benchmark | c10、c19 |
| same-vector-control | c1、c15 |
| metadata-only-control | c15、c16 |
| not-text-reencoding | c15、c19 |
| article-at-example | c22 |
| fourth-chapter-question | c7、c9 |
| compatible-space | c7、c9 |
| tailor-patterns | c1、c7 |
| different-origins | c1、c7 |
| length-is-not-map | c1、c7 |
| same-dimension-not-space | c7 |
| new-map-old-data | c7、c9 |
| number-still-computable | c7 |
| check-pairing | c7、c9 |
| check-compatible-parts | c7、c8、c9 |
| query-document-not-identical | c8 |
| compatible-can-differ | c8 |
| entry-point-nuance | c7、c8 |
| metric-normalization | c6、c9 |
| no-universal-cutoff | c9 |
| no-dimensions-buying-rule | c5、c9、c19 |
| keep-original-evidence | c7、c17、c21 |
| scope-not-deploy | c7、c19 |
| remember-the-locked-door | c17、c21 |
| fifth-chapter-question | c18、c21 |
| viewer-original-conditions | c18、c21 |
| garden-next-step | c1、c18、c21 |
| read-the-necessary-bit | c11、c21 |
| one-viewer-action | c18、c21 |
| do-not-fill-empty | c1、c14、c18 |
| source-can-be-stale | c17、c21 |
| toy-match-not-real-place | c1、c14、c19 |
| what-the-score-did | c18、c21 |
| answer-locked-door | c1、c11、c17 |
| answer-and-article | c18、c21、c22 |

## 與企劃不同的地方

保留核准A的六章與順序，沒有增加冷開場章節。原企劃600秒是估算；本稿補足表示方法的範圍、六筆條件、完整精確排序、前兩筆／全清單與固定向量控制，達3109中文口播單位，估14.76分鐘。較短句補了必要條件與計算範圍，估state皆5–7秒。這是必要說明的初稿估時，不是成片14.76分鐘，也不以停頓、重複或慢播補時。標題沒有承諾十分鐘整。

CTA在完整例子後指向同一篇文章，outro也只給這個文章下一步；沒有另外加留言或訂閱。句子用中文術語與活動名稱，英文原始字與代號只在正式卡片／來源出現，未修改共享字典。共80個短shot，六章使用不同場所與光源；沒有要求一張圖畫六件精確物件、步驟或公式。

## 我懷疑但沒動的事

- 沒測真實嵌入的繁中、同義改寫、否定句、精確名稱與數字表現；保留為未知，不寫成效能結論。
- 不推論所有模型軸不能表示可信度；稿子只說不能未分析就自行替單一維度命名，通常難以直接解釋。
- lint以整個第一章長度警告hook，本章約131秒但第一句已落鉤，第二景給承諾；估hook／promise結束在20秒內，詳draft-metrics。保留六章，不加靜音或另造過短章節來壓警告。
- 估狀態min5秒、max7秒、平均5.7秒、插圖50.75%只是初稿預估。真實TTS可能不同，後續須重新量actual chapters/cadence/body和成片，沒有宣稱關卡通過。
- no-text與中央構圖提示不保證真實圖合格，特別要看偽字、手、動作和直式裁切。沒有生成圖片或TTS，不能用schema／judge替代實看。

## 進度

六章全部寫完；156句、121scene、80shot。demo.py完整JSON與五個摘錄模式各本機執行兩次，輸出一致。兩支cut Shorts已草擬，圖只引用本集shot，未合成。source-only：待另一位代理獨立fact/listener review、真實音訊、圖片、字幕與成片流程；沒有verify文件、fact_checked旗標、音訊或媒體核准，未上傳／發布。
