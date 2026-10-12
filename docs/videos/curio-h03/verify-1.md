# H03 第一輪獨立事實查核

查核者：h03_verify，未參與撰稿。日期：2026-10-12（Asia/Taipei）。實讀原始論文、官方研究機構資料、學會／研究者歷史敘述及素材原件；claims.md 與研究摘要僅作索引。

**結果：最新文字版本通過本輪事實查核。** 35組主張全部覆核，其中33組 CONFIRMED、2組 CHANGED（root修訂後已回讀）；另1組來源書目 CHANGED。NOT FOUND 未解決項為0。這不等於插圖、音訊、字幕、成片、站主或正式站審核通過。

## 輸入與修訂軌跡

- 初稿 video SHA-256：4ebbd2769b4a8a006657e30b88e1942820fa310cb30b780cb4d20a2023b1479f。
- 本報告最終 video SHA-256：40b1d0d2de9d11f20b5182634be46bdadeb5f753004be0c3377d8d989cfe36c0。
- 本報告最終 claims SHA-256：2706ab3877f712a916920d22dcb4ffafe2e84826cd7807295a411dd7c088f4a6。
- brief SHA-256：98e2a3a28c529714bef64d4c42bd76aca5e08ab1cb9318df5c897d7f8cb0bdfc，未改。
- 115景、139句、82個shot、2個photo；33景為非shot（含2個photo）。無say／say_for覆寫。
- 初稿1265欄提取留在外部 _audit/verify-input-inventory.json；最終1270欄留在 _audit/verify-final-input-inventory.json。沒有覆蓋初稿證據。
- 已逐句回讀修訂後的139句及卡片、metadata、受影響prompt。最終8cii emotion與voice.performance只調表演，亦讀回；不把舊SHA的判定冒充新SHA。這兩項及claims末段技術敘述不作歷史／科学事實主張。
- root整合收據：_audit/editorial-revision.json；其後refinement、情緒、performance更新依上列最終SHA為準。查核者沒有修改video.json、claims.md或brief.md。

## 必修問題及最後回讀

| # | where | 原問題 | before → after | 最終 verdict |
| --- | --- | --- | --- | --- |
| F01 | denser-air/fdqr；c13 | 增密與增壓被說成無條件單調關係，忽略減速 | 天體愈往低處走，空氣愈來愈密，承受的壓力也愈大。 → 往更密的空氣移動，天體可能承受更大壓力。c13保留速度條件。 | CHANGED，已解決 |
| F02 | sampling-location/vvez；different-lake-depths/vpzm；c25 | 所引2023文未支持特定「岸邊對湖心採樣位置」爭點 | 改為「爭論包括泥層的定年方法，能不能支持那個年代。」與「沉積物的層次如何判讀，兩邊也沒有相同答案。」sampling prompt改泥芯。 | CHANGED，已解決 |
| F03 | sources[10].title | 書目標題不符合URL原刊／作者稿 | A search for surviving fragments of the Tunguska Event of 1908 → Computation of a possible Tunguska’s strewn field (Icarus 2024; author manuscript) | CHANGED，已解決 |

F01、F02為兩組內容修正；F02兩句及配圖為同一命題相依修改。F03書目從嚴另計第三組。四倍措辭、爆高比較詞、口播與卡片同步沒有替換數值；39句編輯修訂不等於39項事實變更。

## 全部主張表

where列出每次使用的scene、line ID與data。CONFIRMED表示措辭與限制符合已讀證據，並非所有問題都已在科學上定案。

| # | claim | where | URL | HTTP／實讀 | verdict | before → after／限制 |
| --- | --- | --- | --- | --- | --- | --- |
| c01 | 1908年6月30日早上，西伯利亞通古斯地區發生強光、巨響與森林破壞。時刻不精確到分鐘；日期為新曆。 | hook-standing-trunk (3wt8); date-of-flash (wbq3; data); morning-trading-post (huyj); new-forest (3wh5) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ | 直接 GET 200，正文實讀 | CONFIRMED | NASA 日期與地域相符；旁白只說早晨，沒有把新舊曆或分鐘混用。 |
| c02 | 沒有找到公認的主撞擊坑。這不否認存在切科湖等撞擊候選，也不把「未確認」誤寫成地面沒有任何凹地或任何微粒。 | hook-no-crater (m93v; data); search-empty-ground (j9da); specimen-tray-empty (yt7z); negative-evidence-limit (68q7, qivj; data) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ ; https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ | 直接 GET 200，正文實讀 | CONFIRMED | 有候選湖泊與顆粒不等於找到公認主坑；否定句保留「公認」。 |
| c03 | 外圍樹幹大致呈放射狀向外倒伏，接近中心有部分樹幹仍立著，但枝條、樹皮受損；不是所有中央樹都直立，也不是樹木完好無傷。 | hook-standing-trunk (3wt8); kulik-follows-timber (j96k); nineteen-years (fxdt; data); outer-felled-trunk (nn83); central-stripped-trunk (c5u4); two-tree-patterns (6afz, 8cii; data); branch-stubs (vw49); trunk-to-sky (f6zq); standing-trunk-side (za3v); evidence-layers (7tip, 4tzv, uhkz; data); tree-witness-ending (mvq7) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | NASA 描述中央仍立樹幹、樹枝／樹皮破壞；Longo 倒樹方向與 Sandia 動畫說明相符。部分直立，不是全部完好。 |
| c04 | 主流解釋為天體在大氣中解體並快速釋能，衝擊波造成地面破壞；以此回答無公認主坑與倒樹現象。不能把主要能量在空中釋放說成所有碎片完全氣化。 | hook-kulik-puzzled (vu7c); hook-sky-above (nys5); negative-evidence-limit (68q7, qivj; data); generic-rock-above (msxv); relocate-explosion (j3mj; data); airburst-ground (fh3w); evidence-question (zxin); new-forest (3wh5); evidence-layers (7tip, 4tzv, uhkz; data); outro (wg93, 248y, njit; data) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html ; https://arxiv.org/abs/2302.13620 | 直接 GET 200，正文實讀；直接 GET 200，作者摘要及原刊摘要實讀 | CONFIRMED | NASA 與 Sandia 支持大氣中解體釋能；不聲稱所有物質必然氣化。 |
| c05 | 居民記述包括強光、熱感、聲響、被震倒，以及帳篷、財物受影響。另以Andy Bruno於OSU Origins的2018歷史文章核對帳篷敘述（https://origins.osu.edu/milestones/june-2018-1908-tunguska-event-and-threats-tomorrow）。人物畫面是泛化歷史重建，不描畫特定卒年未確認目擊者的臉，不引用未核對的直接對話。 | morning-trading-post (huyj); witness-back (yy5f); tent-cloth (hy4f); measurement-layers (w2u4, 5w6w; data); inhabited-camp (qvai) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ ; https://www.aps.org/apsnews/2018/06/tunguska-event ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | 帳篷敘述另讀 Andy Bruno 2018 OSU Origins 正文；已補 sources[11] 及 c05。原始俄文訪談本次未讀，不冒稱直接見證。 |
| c06 | 倒樹區約2000平方公里；NASA 2023寫830平方英里，Longo記2150±50平方公里。整體近蝴蝶形，局部呈放射狀，兩種尺度不可混成完美圓圈。地景插圖非測繪。 | damage-area (xs6g; data); fallen-corridor (saq5); uneven-hills (k8ac); butterfly-shape (musr; data); areas-not-counts (pceg, bb4w; data); outro (wg93, 248y, njit; data) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | NASA 830 平方英里與 Longo 2150±50 平方公里可口語約兩千；近蝴蝶形與局部放射狀分屬尺度。 |
| c07 | 1908年地方報紙已有報導，不可說1927年以前無人知道。使用已驗明原件的《Сибирская жизнь》135號剪報，正文刊日為1908-07-12，不照檔名07-29讀日期。只展示報導存在，不念未另核對的內文翻譯。 | contemporary-newspaper (pbf7; data); not-forgotten (zrku, xgep; data) | https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | Longo 印刷頁309及1908剪報支持當時已有報導；caption 已標當時報導／傳聞。剪報不是精確爆心觀察；檔名日期不可當正文日期。 |
| c08 | 庫利克1921年調查未抵現場，1927年成功抵達，與1908相差19年；偏遠交通及地形造成困難，其後繼續考察。不要稱1927是第一次出發，不把具體補給畫面當作某日原貌。 | remote-river (hyd4); kulik-expeditions (6qay, wkui; data); kulik-trekking (uqmj); supply-sack (myc5); marsh-route (6w54); not-forgotten (zrku, xgep; data); kulik-follows-timber (j96k); nineteen-years (fxdt; data); repeat-expeditions (f2mk); survey-tripod (2uat) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://www.aps.org/apsnews/2018/06/tunguska-event ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | NASA 原文 geologist Leonid A. Kulik 支持 6qay 地質學家；1921未能抵達、1927抵達、相隔19年。職稱也早已用於原版概念 prompt，不是改換人物身份。 |
| c09 | 庫利克以大型鐵質隕石為搜尋預期，試圖在地面及沼澤中尋找殘骸；這是他當年的假設，不能拿來當已鑑定出的天體成分。 | kulik-first-view (3np7); expected-iron (cvt5); search-empty-ground (j9da); kulik-examines (bikj); repeat-expeditions (f2mk) | https://www.aps.org/apsnews/2018/06/tunguska-event ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | APS 與 Longo 支持庫利克尋鐵隕石的假设；不能拿他的假設當天體成分結論。 |
| c10 | 若有大塊完整天體高速撞入地面，研究者會尋找撞擊坑及殘骸。這是搜尋預期的物理概念，不聲稱每種小碎片落地必形成可辨大坑。 | expected-iron (cvt5) | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html ; https://www.aps.org/apsnews/2018/06/tunguska-event | 直接 GET 200，正文實讀 | CONFIRMED | 是大塊天體高速抵地的搜尋預期，非每顆小碎片都必成大坑。 |
| c11 | 庫利克抽乾一個懷疑的沼澤坑，發現老樹樁，沒有交出期待的隕石。具體坑底老樹樁故事僅採APS 2018歷史專欄，原始日記未重開，標單一歷史敘述來源；沒有杜撰人物反應或對話。 | round-marsh-pool (c48q); drainage-ditch (2pwk); old-stump-bottom (44d4); stump-not-meteorite (qvf5; data); silent-excavation (vf7r) | https://www.aps.org/apsnews/2018/06/tunguska-event | 直接 GET 200，正文實讀 | CONFIRMED | APS 2018 正文確有抽乾 Suslov 沼澤坑、老樁；原始考察日記未讀。維持單一後世歷史敘述來源的限制。 |
| c12 | 編輯判讀：一次沒有找到殘骸不能排除全部落點，觀察到樹木受力痕跡也不是拍到天體本身。分辨搜尋結果與因果推論，不主張新科學發現。 | silent-excavation (vf7r); trunk-to-sky (f6zq) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://www.aps.org/apsnews/2018/06/tunguska-event | 直接 GET 200，正文實讀 | CONFIRMED | 明示由搜尋限制所作編輯判讀，與來源的未確認殘骸狀態一致，非新實驗。 |
| c13 | 高速天體壓縮前方空氣；氣動壓力超過其強度可導致碎裂；更多表面暴露後急速減速，把動能傳給大氣。較低高度空氣一般更稠密；在仍保持高速的條件下，氣動壓力隨密度增大。物體的承受能力取決於結構。科學示意採JPL對車里雅賓斯克的機制解釋，不把通古斯畫成炸彈引爆，也不只歸因於摩擦燃燒。 | generic-rock-above (msxv); forest-question (54sv); incoming-small-body (derk); compressed-air-glow (ih6d); denser-air (fdqr); pressure-not-bomb (vfvs; data); first-breakup (asif); fragment-cloud (jm4w); airburst-chain (uew5, jm2y, 6s9v; data); airburst-ground (fh3w); strong-stone (x7bs) | https://www.jpl.nasa.gov/news/additional-details-on-the-large-feb-15-fireball-over-russia/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html ; https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ | 直接 GET 403，web 正文實讀；直接 GET 200，正文實讀 | CHANGED（已解決） | F01 已解決：fdqr「天體愈往低處走，空氣愈來愈密，承受的壓力也愈大。」→「往更密的空氣移動，天體可能承受更大壓力。」c13 保留速度條件。JPL 原文同時談壓缩、減速與強度，不支持無條件單調增壓。 |
| c14 | 爆心附近，波主要從上方到達；外側具有更大的側向作用，能解釋中央部分直立樹與外圍倒樹。卡片是機制簡化，實際情況包含天體移動、地形、氣流與樹木差異；不以單棵樹直接算高度。 | relocate-explosion (j3mj; data); forest-question (54sv); airburst-chain (uew5, jm2y, 6s9v; data); trunk-overhead (8x3s); standing-trunk-side (za3v); forces-two-positions (fyt5, hbj5; data); root-snap (a7yq); tree-witness-ending (mvq7) | https://newsreleases.sandia.gov/releases/2007/asteroid.html ; https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ | 直接 GET 200，正文實讀 | CONFIRMED | Sandia Movie2 說明爆心正下方衝擊从上方到達；外圍側向分量為概念簡化。不是用單棵樹測定高度。 |
| c15 | 地形、林況與入射條件使實際破壞不必完全對稱。正文不是宣布蝴蝶形只由樹種或山坡造成；精確倒樹幾何仍須測繪和模型。 | uneven-hills (k8ac) | https://newsreleases.sandia.gov/releases/2007/asteroid.html ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | Sandia 說地形與林況影響損害；Longo 討論飛行與倒樹幾何。沒有把蝴蝶形僅歸樹種或地形。 |
| c16 | 能量、大小、高度等由模型回推，取決於天體強度、密度、速度、入射角、碎裂與放能方式。Sandia 2007為3–5百萬噸TNT當量；NASA 2019介紹的模型為10–30百萬噸。分列各模型，不能把3–30當一份研究的統計信賴區間。 | laboratory-body (ew6f); porous-stone (rz3q); strong-stone (x7bs); spreading-fragments (e4kb); oblique-approach (gb8q); energy-models (r359, wfff; data); energy-unit (kcfm); height-matters (7uyu, tfp3; data); parameters-together (pefz); model-puzzle (7wqj); model-height (cti2, q8h7, 2etw; data); evidence-layers (7tip, 4tzv, uhkz; data) | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html | 直接 GET 200，正文實讀 | CONFIRMED | Sandia 2007 3–5 Mt；NASA 2019 10–30 Mt，分列模型與假設。口播百萬／千萬及卡片TNT當量相符；不是單篇3–30信賴區間。 |
| c17 | 2013-02-15車里雅賓斯克有日間火球、尾跡、高空碎裂及地面衝擊破壞；現代影片、儀器與碎片可交叉核對。使用原創概念插圖，不使用未授權行車紀錄器或第三方照片。刻意不混用最亮點、碎裂帶、主要釋能高度。 | modern-comparison-date (69ir; data); modern-white-trail (t3f2); delayed-wave (dcje); window-impact (k386); modern-fragment (35as); different-events (wxdt, 34vg; data) | https://www.jpl.nasa.gov/news/additional-details-on-the-large-feb-15-fireball-over-russia/ ; https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ | 直接 GET 403，web 正文實讀；直接 GET 200，正文實讀 | CONFIRMED | JPL 2013 官方更新確認火球、感測、碎片；沒有把最亮點高度等同全部碎裂高度。 |
| c18 | 2013事件與1908事件在天體大小及入射等條件不同；現代事件支持空中解體可危及地面，不能把其參數或觀測直接當作通古斯的實測。 | different-events (wxdt, 34vg; data) | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://www.jpl.nasa.gov/news/additional-details-on-the-large-feb-15-fireball-over-russia/ | 直接 GET 200，正文實讀；直接 GET 403，web 正文實讀 | CONFIRMED | NASA 2019 談以現代事件驗模型；通古斯參數仍回推。不能直接把2013實測套為1908實測。 |
| c19 | Boslough與Bruno 2025評論追出「八千萬棵」源自1933年估能量時使用約8000平方公里的面積假設；約為後來約2000平方公里測繪範圍的四倍。引用鏈轉述漸省掉前提，不能當逐棵統計。1933及1934原文此次未重開，旁白明說「一篇研究評論，把它追到…」，不用引號假裝原文。 | counting-question (52jj); eighty-million (vabr; data); forest-impossible-count (jbd7); old-calculation-table (6cjz); measuring-assumption (rkmd); areas-not-counts (pceg, bb4w; data); wide-assumption (8yu4); density-question (5cus); assumption-propagates (h5rn, phjq, mkxr; data); measurement-layers (w2u4, 5w6w; data) | https://pmc.ncbi.nlm.nih.gov/articles/PMC12015480/ ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | 2025 Boslough／Bruno 原刊全文追查1933、8000平方公里、面積約四倍、引用流傳。1933原文未讀，旁白清楚歸屬於研究評論。8yu4已改「約為四倍」，不再有多出四倍的歧義。 |
| c20 | 編輯判讀：把流傳棵數除以面積倍率不會得到經驗證的正確棵數，仍需密度、樹種與損傷等資料。稿件不產生新的棵數。 | no-new-count (undx); different-density (76tt) | https://pmc.ncbi.nlm.nih.gov/articles/PMC12015480/ | 直接 GET 200，正文實讀 | CONFIRMED | 編輯判讀成立：面積、密度等前提仍需資料；本稿沒有直接把八千萬除四冒充新測量。 |
| c21 | 偏遠不等於無人生活；有居民遭遇和受傷報告，但死亡人數記載存在差異。旁白只講不確定，不採零人或確定死亡數字。 | measurement-layers (w2u4, 5w6w; data); inhabited-camp (qvai); empty-stool (8dmz) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ | 直接 GET 200，正文實讀 | CONFIRMED | NASA 2023 與2025對居民傷亡表述有差異；本稿只說記錄不一致，不採確定死傷數或零人。 |
| c22 | 後來找到的微粒不能公認地與爆炸主體相連。樣本的出土脈絡及成分需要檢驗；沒有公認樣本不等於沒有任何人提出候選。 | scattered-small-stone (e4ma); core-awaiting (i6te); microscopic-candidate (5ig5); older-ground-stone (dqeb); identity-testing (fbje); sample-identity (9zvs); no-identity-sample (ap9b) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ ; https://arxiv.org/abs/2302.13620 | 直接 GET 200，正文實讀；直接 GET 200，作者摘要及原刊摘要實讀 | CONFIRMED | NASA 表述粒子尚未確證歸屬，作者稿仍談找不到獲確認的宏觀殘骸；保持「公認」限制。 |
| c23 | 切科湖被提出為碎片撞擊的候選，支持者考察湖盆形狀與沉積；此說仍有爭議，不能直接稱隕石坑或已解案。 | lake-introduction (hh9k); cheko-name (g4cw; data); cheko-shore (dd4q); lake-basin-model (6ru7); shape-not-age (i48k, huin; data); cheko-evidence-table (addm, 8a76, znur; data) | https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ ; https://link.springer.com/article/10.1134/S1028334X17100269 ; https://link.springer.com/article/10.1134/S1028334X23601359 | 直接 GET 200，正文實讀；直接 GET 200 challenge，web 原刊實讀 | CONFIRMED | NASA2025及雙方原刊支持候選／有爭議，沒有把切科湖直接命名已確認撞擊坑。 |
| c24 | Rogozin等2017沉積研究主張湖比1908事件更早形成；本次讀摘要。若湖確實早已存在，就難以由1908碎片形成，這是有條件的推論，不把對方論證當確定年代。 | shape-not-age (i48k, huin; data); sediment-layers (gnpc); older-deposit (r9ig); age-implication (ze2w; data); cheko-evidence-table (addm, 8a76, znur; data) | https://link.springer.com/article/10.1134/S1028334X17100269 ; https://link.springer.com/article/10.1134/S1028334X23601359 | 直接 GET 200 challenge，web 原刊實讀 | CONFIRMED | 2017原刊摘要確以放射性核種及年紋推較古老；此為作者結論。旁白使用「有團隊認為」及若湖先存在的條件句。 |
| c25 | Gasperini等2023正式回應仍支持撞擊假說，爭論泥層的定年方法、沉積層次的解讀等，主張湖心鑽探可作關鍵檢驗。不可沿用舊底稿「反方較新」或「2017已證偽」。本次讀公開全文。 | response-evidence (cjcr); sampling-location (vvez); different-lake-depths (vpzm); cheko-evidence-table (addm, 8a76, znur; data); core-awaiting (i6te) | https://link.springer.com/article/10.1134/S1028334X23601359 | 直接 GET 200 challenge，web 原刊實讀 | CHANGED（已解決） | F02 已解決：vvez／vpzm 原稿岸邊對湖心採樣說法→泥層定年及層次判讀，c25及取樣概念圖同步。2023全文爭的是資料、年紋及定年；結論仍主張湖心鑽探。授權勘誤沒有撤回科學結論。 |
| c26 | Carbognani等作者稿對應Icarus 408（2024-01-15）115845，DOI含2023，提出某些條件下大碎片可能存活與可搜尋落區；沒有藉此找到隕石。讀作者摘要及正式書目，未聲稱讀付費全文。不能說全部物質必然氣化或絕無可存活碎片。 | possible-survival (e5xj); possible-not-found (hdg9, 43pz; data); sample-identity (9zvs) | https://arxiv.org/abs/2302.13620 | 直接 GET 200，作者摘要及原刊摘要實讀 | CONFIRMED | arXiv v8與原刊Icarus408刊期2024-01-15相符；DOI含2023不造成稿件年份錯。可存活與落區是模型，非已發現碎片。正式全文付費段未讀。 |
| c27 | 主要研究偏向小行星，石質天體為重要模型；彗星碎片曾為候選。成分、精確能量與殘骸仍有待檢驗，機制可信與細節未定可同時成立；不做假說票選或自創機率。 | evidence-question (zxin); evidence-layers (7tip, 4tzv, uhkz; data); comet-alternative (uu24); no-identity-sample (ap9b); case-status (bavy; data) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://arxiv.org/abs/2302.13620 | 直接 GET 200，正文實讀；直接 GET 200，作者摘要及原刊摘要實讀 | CONFIRMED | uhkz 可保留作有保留的質性綜述：NASA2023偏小行星；NASA2019四模型石質最有希望；2024作者摘要亦 most likely stony。不是系統性文獻票數、機率或成分鑑定。後半句明保留成分與能量未定。 |
| c28 | 系列立場的編輯推論：沒有主坑不使無證據說法自動獲得支持；保留未解細節不等於抹除空爆的證據。不是新研究結論或對研究者個人的批評。 | no-saucer-needed (c4kc); case-status (bavy; data) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html | 直接 GET 200，正文實讀 | CONFIRMED | 系列立場／編輯推論與brief一致，不把無證據陰謀和空爆等權。 |
| c29 | 衛星圖為2024-07-06 Landsat 8資料製作，NASA EO Michala Garrison／USGS；不是1908災後原貌。實際原圖無爆心標籤與軌跡箭頭，旁白不聲稱畫面中有這些標示。 | modern-satellite (3umw; data) | https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ | 直接 GET 200，正文實讀 | CONFIRMED | NASA原頁及本地原圖均已讀／看：2024-07-06 Landsat8，Garrison／USGS；本地原圖無爆心標籤。不是1908災後照片。 |
| c30 | 庫利克及後續考察留下倒樹的照片和測繪等資料，使後人可以重新研究破壞；片中只畫時代相符的泛化測繪器具，沒有取用有權利疑點的老倒樹照片。 | survey-tripod (2uat) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | Longo 相關頁談1927倒向、1938航拍、1958起測繪及後來重分析；NASA談後續考察。沒有冒稱所有测绘都在1927完成。 |
| c31 | TNT當量用來比較能量，不表示事件是核爆。此為能量單位的概念說明；不把通古斯換算成幾顆廣島原子彈。 | energy-unit (kcfm) | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html | 直接 GET 200，正文實讀 | CONFIRMED | TNT當量為能量比較，NASA與Sandia的模型值不表示核反應。未換成原子彈顆數。 |
| c32 | NASA 2019介紹的模型爆高6–9英里，約10–14公里；1英里精確為1.609344公里，顯示約1.61。較早研究另有不同高度，不能將英里誤當公里，也不能將不同模型視為同一次現場儀器測量。 | model-height (cti2, q8h7, 2etw; data) | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，正文實讀；直接 GET 200，PDF 相關完整頁實讀 | CONFIRMED | NASA原文6–9miles；NIST 1mi=1.609344km，9.656064–14.484096km→約10–14km。cti2已去掉無比較基準的「更高處」，Longo保留其他高度史。 |
| c33 | 光傳播遠快於聲波，車里雅賓斯克先見閃光後受到聲波影響，兩者不是同時到達；不額外給未核對的秒數或距離。 | delayed-wave (dcje) | https://www.jpl.nasa.gov/news/additional-details-on-the-large-feb-15-fireball-over-russia/ | 直接 GET 403，web 正文實讀 | CONFIRMED | 光聲到達不同時支持；另讀 NASA podcast 2019 0:47 段先閃光後窗戶受衝擊。未補未核對秒數。 |
| c34 | 一般石頭可能早已在現地；若要連回特定爆炸，必須結合出土脈絡與物質成分等證據。這是從候選碎片尚難確認歸屬所作的科學判讀，不聲稱本片鑑定過實物。 | older-ground-stone (dqeb); identity-testing (fbje) | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ ; https://arxiv.org/abs/2302.13620 | 直接 GET 200，正文實讀；直接 GET 200，作者摘要及原刊摘要實讀 | CONFIRMED | 候選物證需要脈絡與成分為合理明示科學判讀，未宣稱本片鑑定過實物。 |
| c35 | 釋能高度會影響地面的衝擊與破壞；相同總能量不能忽略高度而只以倒樹面積直接認出天體大小。較高釋能有較大的傳播距離和擴散空間，是概念說明，未自跑模擬或宣稱單一比例公式。 | height-matters (7uyu, tfp3; data); parameters-together (pefz) | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ ; https://newsreleases.sandia.gov/releases/2007/asteroid.html | 直接 GET 200，正文實讀 | CONFIRMED | Sandia與NASA模擬高度影響地面破壞；概念句不給公式，不聲稱單凭樹倒範圍即可定天體大小。 |

## 逐句覆核覆蓋表

139句逐句讀過；提問、比喻、CTA及編輯意見另標OUT OF SCOPE，不以外部事實方式判定。含實際主張的修辭仍依主張查核。

| # | scene／line | text | 主張 | verdict |
| --- | --- | --- | --- | --- |
| 1 | hook-standing-trunk/3wt8 | 通古斯的森林倒了，中央卻有樹還站著。 | c01, c03 | CONFIRMED |
| 2 | hook-no-crater/m93v | 你以為這麼大的爆炸，正中央一定有個大坑。 | c02 | OUT OF SCOPE（提問／修辭／意見） |
| 3 | hook-kulik-puzzled/vu7c | 其實空中爆炸，才比較能解釋這片森林。 | c04 | CONFIRMED |
| 4 | hook-sky-above/nys5 | 天上的東西，怎麼把地面的樹壓倒？ | c04 | OUT OF SCOPE（提問／修辭／意見） |
| 5 | date-of-flash/wbq3 | 一九〇八年六月三十日，西伯利亞的早晨。 | c01 | CONFIRMED |
| 6 | morning-trading-post/huyj | 通古斯地區出現強光，接著傳來巨響。 | c01, c05 | CONFIRMED |
| 7 | witness-back/yy5f | 附近居民感到熱浪，還有人被震得跌倒。 | c05 | CONFIRMED |
| 8 | tent-cloth/hy4f | 住在森林裡的人，也留下了帳篷搖晃的回憶。 | c05 | CONFIRMED |
| 9 | damage-area/xs6g | 倒下的森林，範圍大約兩千平方公里。 | c06 | CONFIRMED |
| 10 | fallen-corridor/saq5 | 樹幹大致向外躺倒，留下放射狀的痕跡。 | c06 | CONFIRMED |
| 11 | contemporary-newspaper/pbf7 | 當年的地方報紙，很快就記下了這件怪事。 | c07 | CONFIRMED |
| 12 | remote-river/hyd4 | 消息傳得出去，人要走進現場卻很困難。 | c08 | CONFIRMED |
| 13 | kulik-expeditions/6qay | 地質學家庫利克，在一九二一年出發調查。 | c08 | CONFIRMED |
| 14 | kulik-expeditions/wkui | 那次沒能抵達，直到一九二七年才走進現場。 | c08 | CONFIRMED |
| 15 | kulik-trekking/uqmj | 這時距離爆炸，已經過了十九年。 | c08 | CONFIRMED |
| 16 | supply-sack/myc5 | 研究者帶著補給，穿過河道和難走的沼地。 | c08 | CONFIRMED |
| 17 | marsh-route/6w54 | 濕軟的地面，讓尋找落點變成長期工作。 | c08 | CONFIRMED |
| 18 | not-forgotten/zrku | 當地居民早就知道，報紙也已經報導。 | c07, c08 | CONFIRMED |
| 19 | not-forgotten/xgep | 只是研究者隔了很久，才走到倒樹的現場。 | c07, c08 | CONFIRMED |
| 20 | kulik-first-view/3np7 | 庫利克原本相信，森林底下藏著鐵隕石。 | c09 | CONFIRMED |
| 21 | expected-iron/cvt5 | 如果大塊天體撞到地面，應該留下坑和殘骸。 | c09, c10 | CONFIRMED |
| 22 | kulik-follows-timber/j96k | 他沿著樹木倒下的方向，尋找破壞的中心。 | c03, c08 | CONFIRMED |
| 23 | nineteen-years/fxdt | 時間沖淡了很多痕跡，倒木卻還留在原地。 | c03, c08 | CONFIRMED |
| 24 | search-empty-ground/j9da | 他終於走到了，那塊隕石到底藏在哪裡？ | c02, c09 | OUT OF SCOPE（提問／修辭／意見） |
| 25 | outer-felled-trunk/nn83 | 外圍的樹躺倒了，中央卻出現另一種模樣。 | c03 | CONFIRMED |
| 26 | central-stripped-trunk/c5u4 | 有些樹幹直直站著，樹枝和樹皮卻受了損。 | c03 | CONFIRMED |
| 27 | two-tree-patterns/6afz | 外圍的樹朝外倒下，留下受力的方向。 | c03 | CONFIRMED |
| 28 | two-tree-patterns/8cii | 中央有些樹卻還站著，只剩光禿的樹幹。 | c03 | CONFIRMED |
| 29 | branch-stubs/vw49 | 光禿的樹幹，看起來像一根根電線桿。 | c03 | OUT OF SCOPE（提問／修辭／意見） |
| 30 | kulik-examines/bikj | 庫利克仍想找到坑，證明大隕石埋在地下。 | c09 | CONFIRMED |
| 31 | round-marsh-pool/c48q | 沼澤裡的圓形凹地，成了他追查的目標。 | c11 | CONFIRMED |
| 32 | drainage-ditch/2pwk | 研究者抽乾其中一個坑，想看看底下有沒有鐵塊。 | c11 | CONFIRMED |
| 33 | old-stump-bottom/44d4 | 結果露出來的，竟然是一個老樹樁。 | c11 | CONFIRMED |
| 34 | stump-not-meteorite/qvf5 | 這個坑沒有交出他期待的隕石。 | c11 | CONFIRMED |
| 35 | silent-excavation/vf7r | 一次挖錯地方，當然還不能排除所有落點。 | c11, c12 | CONFIRMED |
| 36 | repeat-expeditions/f2mk | 接下來幾年，庫利克反覆回到這裡，繼續搜尋鐵質殘骸。 | c08, c09 | CONFIRMED |
| 37 | survey-tripod/2uat | 搜尋留下了照片和測繪資料，後人才能重新檢查森林。 | c08, c30 | CONFIRMED |
| 38 | specimen-tray-empty/yt7z | 可是後續搜尋，也沒有找到公認的主撞擊坑。 | c02 | CONFIRMED |
| 39 | negative-evidence-limit/68q7 | 找不到期待的東西，要檢查的也包括原先的假設。 | c02, c04 | OUT OF SCOPE（提問／修辭／意見） |
| 40 | negative-evidence-limit/qivj | 會不會從一開始，就把爆炸的位置想錯了？ | c02, c04 | OUT OF SCOPE（提問／修辭／意見） |
| 41 | trunk-to-sky/f6zq | 樹幹留下的是受力痕跡，不是天體的照片。 | c03, c12 | CONFIRMED |
| 42 | generic-rock-above/msxv | 真正砸向地面的，可能先是空氣的衝擊。 | c04, c13 | CONFIRMED |
| 43 | relocate-explosion/j3mj | 把爆炸移到天空，中央的直立樹就有了線索。 | c04, c14 | CONFIRMED |
| 44 | forest-question/54sv | 如果是空爆，衝擊波究竟怎麼抵達地面？ | c13, c14 | OUT OF SCOPE（提問／修辭／意見） |
| 45 | incoming-small-body/derk | 高速天體進入大氣，前面的空氣來不及讓開。 | c13 | CONFIRMED |
| 46 | compressed-air-glow/ih6d | 空氣被猛烈壓縮，天體承受的壓力跟著升高。 | c13 | CONFIRMED |
| 47 | denser-air/fdqr | 往更密的空氣移動，天體可能承受更大壓力。 | c13 | CHANGED（已解決） |
| 48 | pressure-not-bomb/vfvs | 當壓力超過它承受得住的強度，石塊開始碎裂。 | c13 | CONFIRMED |
| 49 | first-breakup/asif | 它一碎開，更多表面就暴露在空氣裡。 | c13 | CONFIRMED |
| 50 | fragment-cloud/jm4w | 碎片急速減慢，把原本的動能交給周圍空氣。 | c13 | CONFIRMED |
| 51 | airburst-chain/uew5 | 天體高速進入大氣，前方空氣受到強烈壓縮。 | c13, c14 | CONFIRMED |
| 52 | airburst-chain/jm2y | 石塊破碎又減速，把能量快速傳給空氣。 | c13, c14 | CONFIRMED |
| 53 | airburst-chain/6s9v | 衝擊波傳到地面，森林就受到破壞。 | c13, c14 | CONFIRMED |
| 54 | airburst-ground/fh3w | 這不是一顆炸彈，而是天體在大氣裡解體。 | c04, c13 | CONFIRMED |
| 55 | trunk-overhead/8x3s | 在爆心正下方，衝擊主要從上方壓過來。 | c14 | CONFIRMED |
| 56 | standing-trunk-side/za3v | 樹枝可能被剝掉，樹幹卻仍維持直立。 | c03, c14 | CONFIRMED |
| 57 | forces-two-positions/fyt5 | 接近爆心正下方，樹幹主要承受上方的衝擊。 | c14 | CONFIRMED |
| 58 | forces-two-positions/hbj5 | 外圍受到較大的側向推力，樹就朝外倒下。 | c14 | CONFIRMED |
| 59 | root-snap/a7yq | 同一個空爆，就能留下站著和躺著的樹。 | c14 | CONFIRMED |
| 60 | uneven-hills/k8ac | 真實森林有山坡和不同樹種，形狀不會完美對稱。 | c06, c15 | CONFIRMED |
| 61 | butterfly-shape/musr | 整個倒樹區近似蝴蝶形，並不是整齊的一個圓。 | c06 | CONFIRMED |
| 62 | laboratory-body/ew6f | 科學家把這些破壞，拿來回推天體的條件。 | c16 | CONFIRMED |
| 63 | porous-stone/rz3q | 但石頭有多鬆、速度多快，都會改變碎裂時機。 | c16 | CONFIRMED |
| 64 | strong-stone/x7bs | 鬆散的石塊可能較早破碎，結實的天體則可能撐得更久。 | c13, c16 | CONFIRMED |
| 65 | spreading-fragments/e4kb | 碎片沿著路徑散開多少，又會改變能量釋放在哪個位置。 | c16 | CONFIRMED |
| 66 | oblique-approach/gb8q | 進來的角度不同，能量落在哪裡也會不同。 | c16 | CONFIRMED |
| 67 | energy-models/r359 | 較低的一組估計，相當於三到五百萬噸炸藥。 | c16 | CONFIRMED |
| 68 | energy-models/wfff | 另一組估成一千到三千萬噸，兩組的假設不同。 | c16 | CONFIRMED |
| 69 | energy-unit/kcfm | 炸藥當量只是比較能量的單位，並不是說這裡發生核爆。 | c16, c31 | CONFIRMED |
| 70 | height-matters/7uyu | 同樣的能量，若在不同高度釋放，地面破壞也會不同。 | c16, c35 | CONFIRMED |
| 71 | height-matters/tfp3 | 爆得較高，衝擊抵達地面以前，就有更多空間向外擴散。 | c16, c35 | CONFIRMED |
| 72 | parameters-together/pefz | 因此只拿倒樹範圍，就想認出天體大小，會漏掉關鍵條件。 | c16, c35 | CONFIRMED |
| 73 | model-puzzle/7wqj | 所以空爆說得通，不等於每個參數都已算定。 | c16 | CONFIRMED |
| 74 | model-height/cti2 | 二〇一九年的一組模型，把主要爆炸放在高空。 | c16, c32 | CONFIRMED |
| 75 | model-height/q8h7 | 它估計離地大約十到十四公里，那是模型回推的答案。 | c16, c32 | CONFIRMED |
| 76 | model-height/2etw | 較早研究給過別的高度，不能當成同一次的直接測量。 | c16, c32 | CONFIRMED |
| 77 | modern-comparison-date/69ir | 二〇一三年，車里雅賓斯克給了我們現代對照。 | c17 | CONFIRMED |
| 78 | modern-white-trail/t3f2 | 白天的天空出現火球，後面拖著長長的尾跡。 | c17 | CONFIRMED |
| 79 | delayed-wave/dcje | 天空的閃光先被看見，聲波傳到地面，還需要一段時間。 | c17, c33 | CONFIRMED |
| 80 | window-impact/k386 | 它在高空碎裂，地面仍被衝擊波波及。 | c17 | CONFIRMED |
| 81 | modern-fragment/35as | 這一次，有錄影、感測資料和落地碎片可互相核對。 | c17 | CONFIRMED |
| 82 | different-events/wxdt | 這一次有現代觀測，還能拿碎片互相核對。 | c17, c18 | CONFIRMED |
| 83 | different-events/34vg | 通古斯主要靠留下的痕跡，不能直接套用答案。 | c17, c18 | CONFIRMED |
| 84 | counting-question/52jj | 至於人人都會背的八千萬棵，又是怎麼算出來的？ | c19 | OUT OF SCOPE（提問／修辭／意見） |
| 85 | eighty-million/vabr | 八千萬這個數字，出現在很多通古斯的介紹裡。 | c19 | CONFIRMED |
| 86 | forest-impossible-count/jbd7 | 聽起來很精確，卻不是有人拿名冊一棵棵清點。 | c19 | CONFIRMED |
| 87 | old-calculation-table/6cjz | 一篇研究評論，把它追到一九三三年的估算。 | c19 | CONFIRMED |
| 88 | measuring-assumption/rkmd | 當時是為了估爆炸能量，先假設一個倒樹面積。 | c19 | CONFIRMED |
| 89 | areas-not-counts/pceg | 那個假設用了大約八千平方公里。 | c06, c19 | CONFIRMED |
| 90 | areas-not-counts/bb4w | 後來測繪的倒樹範圍，卻只有大約兩千。 | c06, c19 | CONFIRMED |
| 91 | wide-assumption/8yu4 | 原先假設的面積，大約是後來測繪的四倍。 | c19 | CONFIRMED |
| 92 | density-question/5cus | 再配上樹木密度，才能換成估計的棵數。 | c19 | CONFIRMED |
| 93 | assumption-propagates/h5rn | 原本的棵數，建立在面積和樹木密度的假設上。 | c19 | CONFIRMED |
| 94 | assumption-propagates/phjq | 後來被一次次引用，當初的前提慢慢不見了。 | c19 | CONFIRMED |
| 95 | assumption-propagates/mkxr | 最後只剩八千萬，聽起來就像真的逐棵數過。 | c19 | OUT OF SCOPE（提問／修辭／意見） |
| 96 | no-new-count/undx | 那也不能把八千萬除以四，就宣布新的正確答案。 | c20 | CONFIRMED |
| 97 | different-density/76tt | 森林的密度、樹種和受損程度，都還需要資料。 | c20 | CONFIRMED |
| 98 | measurement-layers/w2u4 | 約兩千平方公里，有後來的測繪支持。 | c05, c19, c21 | CONFIRMED |
| 99 | measurement-layers/5w6w | 棵數和傷亡，卻沒有同樣完整的統計。 | c05, c19, c21 | CONFIRMED |
| 100 | inhabited-camp/qvai | 偏遠不代表沒人，居民留下了受熱和受損的經驗。 | c05, c21 | CONFIRMED |
| 101 | empty-stool/8dmz | 死亡人數的資料不一致，不能順口說無人傷亡。 | c21 | CONFIRMED |
| 102 | scattered-small-stone/e4ma | 天體的碎片，有沒有留在地上？ | c22 | OUT OF SCOPE（提問／修辭／意見） |
| 103 | lake-introduction/hh9k | 如果有碎片落下，附近一座湖會不會就是線索？ | c23 | OUT OF SCOPE（提問／修辭／意見） |
| 104 | cheko-name/g4cw | 這座常被提起的湖，叫做切科湖。 | c23 | CONFIRMED |
| 105 | cheko-shore/dd4q | 有研究團隊認為，湖可能是碎片撞出來的。 | c23 | CONFIRMED |
| 106 | lake-basin-model/6ru7 | 他們研究湖盆的形狀，也檢查湖底的沉積。 | c23 | CONFIRMED |
| 107 | shape-not-age/i48k | 可是湖的形狀，只是問題的一部分。 | c23, c24 | CONFIRMED |
| 108 | shape-not-age/huin | 還得回答它什麼時候形成，以及底下有什麼。 | c23, c24 | CONFIRMED |
| 109 | sediment-layers/gnpc | 沉積物像一層層留下的紀錄，可以用來估年代。 | c24 | CONFIRMED |
| 110 | older-deposit/r9ig | 有團隊認為，湖底的沉積比一九〇八年古老。 | c24 | CONFIRMED |
| 111 | age-implication/ze2w | 如果湖早就存在，就很難說它是那次撞出來的。 | c24 | CONFIRMED |
| 112 | response-evidence/cjcr | 支持撞擊說的研究者，後來又提出不同解讀。 | c25 | CONFIRMED |
| 113 | sampling-location/vvez | 爭論包括泥層的定年方法，能不能支持那個年代。 | c25 | CHANGED（已解決） |
| 114 | different-lake-depths/vpzm | 沉積物的層次如何判讀，兩邊也沒有相同答案。 | c25 | CHANGED（已解決） |
| 115 | cheko-evidence-table/addm | 湖的外形，能不能只用撞擊來解釋？ | c23, c24, c25 | OUT OF SCOPE（提問／修辭／意見） |
| 116 | cheko-evidence-table/8a76 | 這座湖，真的形成於一九〇八年嗎？ | c23, c24, c25 | OUT OF SCOPE（提問／修辭／意見） |
| 117 | cheko-evidence-table/znur | 就算挖到石頭，也得確認是否來自當年的天體。 | c23, c24, c25 | CONFIRMED |
| 118 | core-awaiting/i6te | 更深的鑽探，才可能檢查湖心下面藏著什麼。 | c25, c22 | CONFIRMED |
| 119 | microscopic-candidate/5ig5 | 過去有人找到微小顆粒，卻難以確定屬於這次爆炸。 | c22 | CONFIRMED |
| 120 | older-ground-stone/dqeb | 一顆落在泥地裡的普通石頭，可能在爆炸以前就已經存在。 | c22, c34 | CONFIRMED |
| 121 | identity-testing/fbje | 要把它連回一九〇八年，還得檢查出土位置和物質成分。 | c22, c34 | CONFIRMED |
| 122 | possible-survival/e5xj | 也有模型認為，某些條件下碎片可以存活落地。 | c26 | CONFIRMED |
| 123 | possible-not-found/hdg9 | 但算出可能的落點，和真的找到隕石，相差很遠。 | c26 | CONFIRMED |
| 124 | possible-not-found/43pz | 沒找到，也不能反過來說每一塊都一定化成了氣。 | c26 | CONFIRMED |
| 125 | sample-identity/9zvs | 一顆石頭必須帶著可檢驗的來歷，才有機會結案。 | c22, c26 | CONFIRMED |
| 126 | evidence-question/zxin | 那麼，在找到最後那塊石頭前，我們能確定多少？ | c04, c27 | OUT OF SCOPE（提問／修辭／意見） |
| 127 | new-forest/3wh5 | 爆炸發生在空中，證據留在地面的森林。 | c01, c04 | CONFIRMED |
| 128 | modern-satellite/3umw | 現在的衛星看見的是森林，當年的細節還得靠證據重建。 | c29 | CONFIRMED |
| 129 | evidence-layers/7tip | 樹倒下的方向、中央的樹幹，讓空爆有了根據。 | c03, c04, c16, c27 | CONFIRMED |
| 130 | evidence-layers/4tzv | 天體在空中解體放能，是最有力的解釋。 | c03, c04, c16, c27 | CONFIRMED |
| 131 | evidence-layers/uhkz | 研究多偏向石質小行星，但成分和能量還沒定案。 | c03, c04, c16, c27 | CONFIRMED |
| 132 | comet-alternative/uu24 | 彗星碎片也曾是候選之一，和石質小行星的條件不同。 | c27 | CONFIRMED |
| 133 | no-identity-sample/ap9b | 要驗明天體身分，仍缺一份公認的實物樣本。 | c22, c27 | CONFIRMED |
| 134 | no-saucer-needed/c4kc | 沒有找到主坑，不會讓沒有證據的說法突然變強。 | c28 | OUT OF SCOPE（提問／修辭／意見） |
| 135 | tree-witness-ending/mvq7 | 最奇怪的直立樹，反而幫我們把爆炸移回天空。 | c03, c14 | CONFIRMED |
| 136 | case-status/bavy | 這份檔案的未結，是細節未結，不是什麼都不知道。 | c27, c28 | OUT OF SCOPE（提問／修辭／意見） |
| 137 | outro/wg93 | 森林倒了，空爆能解釋。 | c06, c04 | CONFIRMED |
| 138 | outro/248y | 哪個線索最意外？ | c06, c04 | OUT OF SCOPE（提問／修辭／意見） |
| 139 | outro/njit | 訂閱，一起查案。 | c06, c04 | OUT OF SCOPE（提問／修辭／意見） |

## 卡片、照片及包裝覆核

以下33個非shot場景的全部data已讀。82個shot prompt均讀過，屬明示概念／歷史重建；精確地形、樹木數量與容貌不當史實。修改後泥芯prompt與定年爭點一致，實際生成圖仍待目視審核。

| # | where | 全部data | verdict |
| --- | --- | --- | --- |
| V1 | scenes.hook-no-crater.data | {"text":"你以為中央有**大坑**","kicker":"1908｜通古斯","sub":"現場沒有找到公認的主撞擊坑"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V2 | scenes.date-of-flash.data | {"stats":[{"value":"1908.06.30","label":"西伯利亞的早晨"}],"source":"NASA 歷史整理｜2023"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V3 | scenes.damage-area.data | {"stats":[{"value":"約 2,000 km²","label":"倒樹區面積","note":"整體輪廓近蝴蝶形"}],"source":"NASA 2023｜Longo 2007"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V4 | scenes.contemporary-newspaper.data | {"image":"stock/4021615ee82ef55923ceb551b05d1a1e3cfb4cba3859a13cb1383adb7dd12792.jpg","caption":"1908年地方報紙：當時的報導與傳聞","credit":"Alexander Adrianov｜PD-RusEmpire","tilt":-1.5} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V5 | scenes.kulik-expeditions.data | {"steps":[{"title":"1921 年","detail":"出發調查，未抵現場"},{"title":"1927 年","detail":"終於抵達倒樹區"}],"source":"NASA 歷史整理｜2023"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V6 | scenes.not-forgotten.data | {"left":{"heading":"當地早已知道","points":["親歷者留下回憶","地方報紙已有報導"]},"right":{"heading":"調查晚到現場","points":["交通與地形困難","1927年抵達倒樹區"]},"source":"Longo 2007｜NASA 2023"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V7 | scenes.nineteen-years.data | {"text":"森林是**現場紀錄**","sub":"留下方向，也留下不完整的細節"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V8 | scenes.two-tree-patterns.data | {"left":{"heading":"外圍","points":["樹木大致朝外倒伏"]},"right":{"heading":"靠近中心","points":["部分樹幹仍直立","枝條與樹皮受損"]},"source":"NASA 歷史整理｜2023"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V9 | scenes.stump-not-meteorite.data | {"text":"坑底是**老樹樁**","kicker":"庫利克尋找的沼澤坑","sub":"APS 2018 歷史專欄"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V10 | scenes.negative-evidence-limit.data | {"left":{"heading":"搜尋得到的結果","points":["主坑未確認","主體殘骸未確認"]},"right":{"heading":"不能直接推成","points":["天上什麼都沒來","地面破壞憑空發生"]},"source":"NASA 2023｜NASA EO"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V11 | scenes.relocate-explosion.data | {"text":"把爆炸的位置\n移到**天空**","sub":"空爆：主要能量在大氣中釋放"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V12 | scenes.pressure-not-bomb.data | {"text":"壓力超過**強度**","sub":"高速穿越大氣的力學過程｜JPL 2013"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V13 | scenes.airburst-chain.data | {"steps":[{"title":"高速進入","detail":"前方空氣受到壓縮"},{"title":"破碎與減速","detail":"動能快速傳給大氣"},{"title":"衝擊波抵達地面","detail":"樹木承受壓力與氣流"}],"source":"JPL 2013｜Sandia 2007"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V14 | scenes.forces-two-positions.data | {"left":{"heading":"接近正下方","points":["衝擊主要來自上方","部分樹幹仍直立"]},"right":{"heading":"外圍","points":["較大的側向推力","樹木朝外倒下"]},"source":"Sandia 2007｜概念簡化，非比例圖"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V15 | scenes.butterfly-shape.data | {"text":"整體倒樹區\n近似**蝴蝶形**","sub":"並非完美圓圈｜NASA 2023／Longo 2007"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V16 | scenes.energy-models.data | {"title":"兩組研究的模型估值","stats":[{"value":"3–5 百萬噸","label":"2007 Sandia 模型"},{"value":"10–30 百萬噸","label":"NASA 2019介紹的模型"}],"source":"TNT 等效能量｜不是同一組誤差範圍"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V17 | scenes.height-matters.data | {"left":{"heading":"能量相同","points":["在不同高度釋放"]},"right":{"heading":"地面結果","points":["衝擊的強弱與範圍不同"]},"source":"Sandia 2007｜NASA 2019"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V18 | scenes.model-height.data | {"steps":[{"title":"NASA 2019介紹的模型","detail":"約6–9英里高空釋能"},{"title":"換算約10–14公里","detail":"原始單位是英里"},{"title":"模型各有條件","detail":"不是1908年的直接測量"}],"source":"NASA Ames 2019｜1英里約1.61公里"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V19 | scenes.modern-comparison-date.data | {"stats":[{"value":"2013.02.15","label":"車里雅賓斯克火球"}],"source":"JPL 2013"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V20 | scenes.different-events.data | {"left":{"heading":"2013 車里雅賓斯克","points":["有現代觀測與碎片"]},"right":{"heading":"1908 通古斯","points":["主要依歷史痕跡回推","天體大小、入射條件不同"]},"source":"JPL 2013｜NASA 2019"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V21 | scenes.eighty-million.data | {"text":"**8,000 萬棵**","kicker":"常見的通古斯敘述","sub":"流傳估值，不是逐棵清點"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V22 | scenes.areas-not-counts.data | {"title":"數字背後的面積","stats":[{"value":"約 8,000 km²","label":"1933年估算採用的假設"},{"value":"約 2,000 km²","label":"後來現場測繪的範圍"}],"source":"Boslough／Bruno 2025｜Longo 2007"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V23 | scenes.assumption-propagates.data | {"steps":[{"title":"面積與密度的假設","detail":"用來估算能量與棵數"},{"title":"後續不斷被引用","detail":"前提逐漸被省略"},{"title":"看起來像確定統計","detail":"其實沒有逐棵清點"}],"source":"Boslough／Bruno 2025 的引用鏈追查"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V24 | scenes.measurement-layers.data | {"left":{"heading":"比較穩妥","points":["約兩千平方公里受災"]},"right":{"heading":"不冒充精確統計","points":["八千萬棵","確切死亡人數"]},"source":"Boslough／Bruno 2025｜NASA 2023"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V25 | scenes.cheko-name.data | {"text":"**切科湖**","sub":"撞擊坑候選｜成因仍有爭議"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V26 | scenes.shape-not-age.data | {"left":{"heading":"湖盆形狀","points":["可能提示形成機制"]},"right":{"heading":"沉積年代","points":["檢查是否早於1908"]},"source":"Cheko 研究爭論｜2017／2023"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V27 | scenes.age-implication.data | {"text":"如果湖早已存在","sub":"就難以直接歸因於1908年的碎片"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V28 | scenes.cheko-evidence-table.data | {"columns":["線索","需要回答的問題"],"rows":[["湖形","是否只能由撞擊造成？"],["年代","是否真的形成於1908？"],["物證","能否連回通古斯天體？"]],"source":"Rogozin 2017｜Gasperini等2023回應"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V29 | scenes.possible-not-found.data | {"left":{"heading":"模型計算","points":["某些碎片可能落地","提出可以搜尋的區域"]},"right":{"heading":"現場發現","points":["尚未認出當年天體","未找到，不等於全部氣化"]},"source":"Carbognani等｜Icarus 2024 作者稿"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V30 | scenes.modern-satellite.data | {"image":"stock/d99767162754c9cafc1cea2049ba95b613ac8d4df210cd6392fc7fcda170a68b.jpg","caption":"2024年7月6日，通古斯地區衛星圖","credit":"NASA EO／Michala Garrison、USGS（公有領域）","tilt":1.5} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V31 | scenes.evidence-layers.data | {"items":["現場：大範圍倒樹與中央直立樹","解釋：天體在空中解體放能","未定：成分、能量與碎片歸屬"],"source":"NASA 2023／2019｜研究爭論綜合"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V32 | scenes.case-status.data | {"text":"空爆**站得住**\n細節仍**未結**","kicker":"奇聞檔案局 H03","sub":"天體身分、精確能量、碎片與切科湖"} | CONFIRMED（提問／CTA為OUT OF SCOPE） |
| V33 | scenes.outro.data | {"title":"森林倒了，答案在天空","cta":"訂閱奇聞檔案局","lines":["讓證據說到它能說的地方"]} | CONFIRMED（提問／CTA為OUT OF SCOPE） |

| # | where | claim／完整文字 | URL／依據 | verdict | before → after |
| --- | --- | --- | --- | --- | --- |
| M01 | youtube.title | 通古斯大爆炸：森林倒了，坑在哪裡？｜奇聞檔案局 | c02–c04 | CONFIRMED | 維持 |
| M02 | youtube.description | 約兩千平方公里的森林倒下，靠近爆炸中心的樹幹卻還站著。通古斯沒有找到公認的主撞擊坑，留下的森林反而指向天空。<br>奇聞檔案局 H03：跟著庫利克走進西伯利亞，從十九年後的考察、沼澤坑底的老樹樁，看高速天體如何在空中解體，讓衝擊波抵達地面。<br>八千萬棵樹是誰數的？不同模型為什麼算出不同能量？切科湖能不能算隕石坑？把現場觀察、估算前提與候選物證分開，才能看出哪些答案站得住，哪些細節還沒結案。<br><br>資料截至2026-10-12。情境畫面由AI生成，是歷史與科學概念的重建，不是1908年現場攝影；空爆示意不按比例。能量與高度均為研究模型估計，八千萬棵是流傳的粗估；切科湖成因與碎片歸屬仍有爭議。本集只提供繁體中文旁白、說明與可關閉CC。 | c02–c08、c11、c13、c16、c19、c23–c26；user繁中決策 | CONFIRMED（製作揭露為規格） | 未把問題寫成已解；尚非成品驗收 |
| M03 | thumbnail.data | {"headline":"**坑在哪裡**","tag":"歷史懸案","sub":"倒下的森林，站著的樹幹","shot":"hook-kulik-puzzled"} | c02、c03 | CONFIRMED | 非實物鑑定或已解案承諾 |
| M04 | youtube.tags | 通古斯大爆炸；通古斯；奇聞檔案局；Tunguska；空爆；庫利克；切科湖；隕石坑；西伯利亞；歷史懸案 | 來源人地名及主題 | CONFIRMED | 無無據數字 |
| M05 | sources[10].title | Carbognani et al.: Computation of a possible Tunguska’s strewn field (Icarus 2024; author manuscript) | https://arxiv.org/abs/2302.13620 | CHANGED | F03已解決 |
| M06 | assets[0]／contemporary-newspaper | 1908原剪報、Adrianov、PD-scan/PD-RusEmpire | https://commons.wikimedia.org/wiki/File:1908-07-29-SibirskayaZshizn-135.jpg | CONFIRMED | 正文1908-07-12新曆；filename不是刊期。caption標報導／傳聞 |
| M07 | assets[1]／modern-satellite | 2024-07-06、Landsat8、Garrison／USGS | https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ | CONFIRMED | 本地原圖無路徑、爆心標籤；保持非1908說明 |

## 每個來源的實讀状态

外部_audit/verify-sources/保存指定UA的GET收據與去HTML註解正文。指定User-Agent為Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)，同主機GET間隔至少1.1秒。HTTP200 challenge不算正文；有時直接GET失敗而web可讀，明確分列。使用3次web搜尋（上限5次），其餘為開啟已知來源。

| URL | HTTP／實讀状态 | 所讀範圍 |
| --- | --- | --- |
| https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ | 直接 GET 200，正文實讀 | 正文 |
| https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ | 直接 GET 200，正文實讀 | 正文 |
| https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ | 直接 GET 200，正文實讀 | 正文 |
| https://newsreleases.sandia.gov/releases/2007/asteroid.html | 直接 GET 200，正文實讀 | 正文 |
| https://www.aps.org/apsnews/2018/06/tunguska-event | 直接 GET 200，正文實讀 | 正文 |
| https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 直接 GET 200，PDF 相關完整頁實讀 | HTTP200，一次下載19,348,345bytes。28頁PDF中相關完整頁1、4、7、10、12、17、18、20（印刷頁303、306、309、312、314、319、320、322）實讀；未聲稱逐頁读完全部28頁。SHA256 77f2285ca2deeaf774f1ad3708f6f554d61a0b2d2fb8e45322d7638bb1473ce8。 |
| https://www.jpl.nasa.gov/news/additional-details-on-the-large-feb-15-fireball-over-russia/ | 直接 GET 403，web 正文實讀 | 正文 |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC12015480/ | 直接 GET 200，正文實讀 | 指定UA GET200全文；web初次recaptcha。亦讀Nature原刊正文；裸Nature GET200只是ClientChallenge。 |
| https://link.springer.com/article/10.1134/S1028334X17100269 | 直接 GET 200 challenge，web 原刊實讀 | web原刊摘要；付費全文未讀。 |
| https://link.springer.com/article/10.1134/S1028334X23601359 | 直接 GET 200 challenge，web 原刊實讀 | web公開全文，包括結論；另讀授權勘誤。 |
| https://arxiv.org/abs/2302.13620 | 直接 GET 200，作者摘要及原刊摘要實讀 | 作者摘要v8；另讀DOI原刊摘要、導言與刊期，付費全文未讀。 |
| https://origins.osu.edu/milestones/june-2018-1908-tunguska-event-and-threats-tomorrow | 直接 GET 200，正文實讀 | Andy Bruno歷史研究敘述，帳篷震動、居民遭遇。原訪談連結未能開，不冒稱讀到俄文第一手訪談。 |
| https://www.nature.com/articles/s41598-025-98362-9 | 直接GET200為challenge；web帶cookies_not_supported查詢參數開啟正文 | 與PMC同篇2025原刊評論。1933原文未讀。 |
| https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8 | 直接GET200、web正文 | mile→km 1.609344，核c32算術；較短錯誤路徑先前404，不混作此成功頁。 |
| https://www.nasa.gov/podcasts/on-a-mission/season-two-episode-1-the-sky-is-falling/ | web逐字稿可讀，直接GET未執行 | 0:47段閃光先到、後續窗戶受衝擊；不用其舊八千萬或原子彈倍率。 |
| https://link.springer.com/article/10.1134/S1028334X23600044 | web原刊摘要；直接GET未執行 | 2023反方湖形比較；未讀付費全文。 |
| https://link.springer.com/article/10.1134/S1028334X23060119 | web公開全文；直接GET未執行 | 勘誤改CC BY，無撤回科學結論。 |
| https://doi.org/10.1016/j.icarus.2023.115845 | web重定向原刊摘要／導言；直接GET未執行 | Icarus408，2024-01-15；標題Computation of a possible Tunguska’s strewn field。 |
| https://pubmed.ncbi.nlm.nih.gov/24196713/ | 直接GET203 challenge；web最後成功讀摘要 | Brown2013，現代事件背景，未把其500±100kt另塞進旁白。 |
| https://www.nature.com/articles/nature12741 | web開啟失敗，原刊搜尋摘要及PubMed可讀；未另GET | 不冒稱已讀Nature付費全文。此稿未使用其新數字。 |
| https://commons.wikimedia.org/wiki/File:1908-07-29-SibirskayaZshizn-135.jpg | web檔頁與本地原件可讀；本代理未另GET檔頁 | 1908-07-12新曆、135號p4、作者、PD-scan/PD-RusEmpire；不按檔名讀7/29。 |
| https://commons.wikimedia.org/wiki/File:A_Cosmic_Explosion_Over_Siberia_(154488_-_russia_tunguskablast_oli_20240706_lrg).jpg | web工具未能開；獨立讀NASA原頁與本地像素 | root另保留Commons API授權收據，不能把此頁失敗當NASA原頁失敗。 |

## 疑點、意見、易變事實與聽眾檢查

- 切科湖形成、碎片歸屬與模型研究狀態可能新增證據。本次讀到2023雙方論文、2024碎片模型、2025 NASA／研究評論；不是宣稱系統性讀遍所有2026论文。隔很久才出版應重新查核。
- Longo來源已在2026-10-12下載並讀相關完整頁，最終sources及claims日期已一致更新。
- 系列立場與brief一致；沒有意見衝突。來源未與brief主線衝突，沒有私自改brief。
- 6qay「地質學家」明確有NASA原文支持。uhkz「研究多偏向石質小行星」作有保留的質性綜述可接受；不能解讀為系統性投票比例，不能刪去後半句未定限制。
- 8yu4「高估四倍」已改「大約是…四倍」；cti2「更高處」改為一般高空並接約10–14公里，沒有產生新測量。
- 139句皆≤40字；旁白沒有拉丁術語、括號或URL，未用未核對的直接引語，沒有「經查證／根據官方文件／本影片」核稿語气。
- listener負責reveals與語音卡片節奏；此報告核其最後文字的來源，不等於已驗每個揭示時間。兩張photo本地原始像素已看；82張圖生成後仍需目視品管。
- 老樹樁由APS後世歷史敘述支持；1933數值源自2025評論追查；2017切科湖僅讀摘要；付費原刊未讀區、原訪談未開者都已揭露，不冒充第一手全文。

## Lint及第二輪

最新SHA原生lint為0 errors、3 warnings（face/daylight/writing提示詞頻率，多為否定句），139句、2442 spoken units、估11.8分鐘。這不是TTS實測時長，也不證明8分鐘正文、全片、CC或上架包已通過；相關製作檢查後續另做。

本輪查核者實際改稿0項，root依查核與listener整合。實質事實／書目修正3組，其中內容2組、書目1組；未達技能「超過3個FACT changes」強制第二輪門檻。root另安排不同代理作獨立第二輪，屬額外覆核；本報告不代其宣告通過。第二輪應核F01–F03及其相依項，並記錄所抽查的已確認主張。

## 來源補充後的版本回讀（2026-10-12）

本次僅追加metadata回讀，不重審已查核全文。video.sources新增Icarus 2019來源，claims c21僅補同一引用URL；主張文字未改。

- 當前video SHA-256：08b8fc80c9b9720ee30cf1ccf73f8f0d540a03e8b3ec6ef77166dde43237dca2。
- 當前claims SHA-256：8872f4f0db0ddad05367b8c8c8597ece64c83f556983fd620dbbbd301a9e39dc。
- 新增來源：[Tunguska eyewitness accounts, injuries, and casualties](https://doi.org/10.1016/j.icarus.2019.01.001)，checked_on為2026-10-12。
- 新來源實讀者為第二輪h03_research：原刊搜尋回傳的摘要、導言及結論；DOI／出版社直接GET為403，未讀付費全文。本代理只回讀來源metadata及引用，不冒稱本代理已實讀該原刊。
- _audit/casualties-source-revision.json記錄sources以外JSON未變；本代理另以40b1d0d2…版的逐欄inventory比對當前所有非sources欄位，完全一致。139句旁白、卡片及包裝內容沒有改動。
- 本報告上方完整查核仍對應40b1d0d2…／2706ab38…；此追加將「文字內容通過本輪」結論延伸到僅補引用的當前版本，不計新增事實修正。第二輪對該來源的獨立判定另見verify-2.md。
