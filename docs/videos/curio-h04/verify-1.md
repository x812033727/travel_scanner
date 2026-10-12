# H04 第一輪獨立事實查核

日期：2026-10-12。查核者：`h03_verify`，未撰寫正式稿。

**狀態：PASS，未解 must-fix＝0。** 已核讀最終 100 景／119 句、46 組主張、全部 `scene.data`（含圖像提示）、縮圖、YouTube 標題／說明／tags；三組事實修正及後續文書素材整合均已回讀。這是腳本事實與素材文字／局部像素查核，不是旁白、生成圖、完整成片或站主驗收通過。

- 最終 `video.json` SHA-256：`98b2fe192185644dd7a36a3deac8c4f8c9314a54486cedf1ff23cdd85dfae2f8`。
- 最終 `claims.md` SHA-256：`3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`；46 組定義、來源與素材段已讀。
- 全文先行核讀快照：`c4d8f146…`；作者交接：`ef0f52d8…`；root 文書整合及三句口語調整後為上述最終 SHA。所有旁白、卡片、metadata 與 prompt 已逐路徑抽出，見外部 `_audit/verify1-extractions/98b2fe192185644d.json`、同名 `.txt`／`.video.json`／`.claims.md`。
- 差異逐項讀取存於同目錄 `handoff-delta-ef0f52d8.json`（初稿至作者交接）與 `handoff-delta-ef0f52d8-98b2fe19.json`（作者交接至最終）。抽取工具保守標記 in_progress，實際交接與最終通過狀態以本報告為準。
- 本查核者只寫此報告；`video.json`／`claims.md` 的修正由作者／root 統一套用，未改 brief。

## 本輪修正項目

| # | 位置 | 原文／問題 | 建議修正與理由 | 狀態 |
|---|---|---|---|---|
| F1 | `euwn` | 「內側刀切是事後鑑定，不是當場一眼看穿。」 | 改為「內側刀切的判斷，來自對留下布料的鑑定。」四月鑑定可證實判斷依據，不能證明早先無人看出或猜到。 | 已套用及回讀通過 |
| F2 | `7tq6` | 「後來這些雪板比較軟，坡也更陡。」 | 加比較基準「比起模型假設，後來的雪板更軟，坡也更陡。」2022 Comment 的比較承接 1959 模型情境，不能使觀眾以為當年雪板硬度已被實測。 | 已套用及回讀通過 |
| F3 | `hook-footprints`、`trail-varied`、`broken-trail` 等現場足跡 prompt | 初稿把當年足跡概念寫成 shallow depressions／felt-boot depression／footprint depressions。 | 依 Slobtsov 證詞改凸起壓實足跡與較低的風蝕雪面；7 張相關 prompt 全部同步，保留短段、不完整、不同鞋襪。新增 c46 記錄同一圖像證據。 | 已套用及回讀通過；7 鏡為同一事實問題 |

實質事實修正共 **3 組**，不以同一項的多處相依修改累加。交接後其他改動是 reveal 對齊、開場示意揭露、CTA、三句同義口語改寫、來源名稱及三份掃描整合，未新增第 4 組事實修正。依「>3」規則本輪不強制第二輪；root 仍可另行要求。

## 每個來源的實際讀取狀態

所有以下直接 GET 均使用指定 editorial User-Agent、跟隨轉址，同 host 間至少隔 1 秒；HTML 註解先剔除再讀。逐次狀態、有效 URL、擷取時間、回應 SHA-256 在外部 `_audit/verify1-sources/access.json`。HTTP 200 不單獨當作已讀證據，本表列出實際正文範圍。

| ID | URL | HTTP／本輪實讀範圍 | 限制 |
|---|---|---|---|
| H1 | https://dyatlovpass.com/case-files-384-387-ru | 200；1959-05-28 結案決定全文俄文轉錄，384–387 頁。此前本查核者已實看 385、386 原掃描。 | 一手文件的民間轉載，不是官方檔案館直接取件。387 新像素讀取由 listener 另存收據，本輪不冒稱自己已看。 |
| H2 | https://dyatlovpass.com/case-files-303-304-ru | 200；1959-04-16 帳篷鑑定俄文轉錄，含檢驗方法與結論。此前已實看 304 背面原掃描。 | 刀切與其他撕裂須區別；不把鑑定擴成離帳人員順序。 |
| H3 | https://dyatlovpass.com/case-files-309-312-ru | 200；1959-04-18 Tempalov 證詞俄文正文。此前已實看 312 原掃描。 | 觀察與證人自己的原因推測分開，不採他對死亡過程的推測。 |
| H4 | https://dyatlovpass.com/case-files-298-300 | 200；1959-04-15 Slobtsov 證詞英譯正文，26 日下午找到帳篷、清雪查看空帳篷、凸起足跡等段落。 | 沒有本輪實看 298–300 掃描，編者括號補語不當原證詞。 |
| N21 | https://www.nature.com/articles/s43247-020-00081-8 | 200；直接 HTML 含真正正文。已讀摘要、導言、Results 地形／風搬雪／延遲機制、Discussion、Methods 個案參數段。 | Web open 登入轉址失敗，但 curl 取得正文成功。未逐式驗算完整推導、未讀補充材料／同行審查／補充影片，未重跑模型。 |
| N22 | https://www.nature.com/articles/s43247-022-00393-x | 200；直接 HTML，已讀完整 Comment 敘事正文，包括 Into the mountains、The avalanches、No final word。 | 未另讀其引用的全部俄羅斯微氣候、雪科學、危險地圖研究；未看補充影片。作者後續報告不能當多組獨立研究。 |
| NC | https://www.nature.com/articles/s43247-022-00425-6 | 200；更正本文直接讀取，只改 reference 1 DOI。 | 不支持「模型結果被更正」的說法，稿中也沒有這樣說。 |
| E21 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/ | 200；2021-01-28 校方解說全文。 | 同一作者研究，非獨立重複試驗；其刑案 reopened 字眼不採。 |
| T21 | https://ethz.ch/en/news-and-events/eth-news/news/2021/01/ein-neuer-blick-auf-ein-altes-raetsel.html | 200；2021-01-28 校方解說全文，作同源性對照。 | 未列入當前 video.sources，僅查核輔助，不作新增影片主張。 |
| E22 | https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/ | 200；2022-03-24 作者訪談全文，含未能執行測試及作者不宣稱完全破案的限制。 | 2022 敘事中的「數日後找到九人」不採；歷史時間以 H1／H3／H4 為準。 |
| T22 | https://ethz.ch/en/news-and-events/eth-news/news/2022/03/the-dyatlov-pass-mystery-and-what-a-research-article-can-trigger.html | 200；2022-03-24 校方解說全文。 | confirmed／proving 不能擴成 1959 當夜重建已確證。 |
| I19 | https://www.interfax.ru/russia/649229 | 200；2019-02-05 新聞正文，明確否認刑案重新偵辦，稱一般監督性複查於 2018-09 開始。 | 新聞引述檢方，不是完整官方報告；稿件「2019 年對外說明複查」可用。 |
| I20 | https://www.interfax.ru/russia/716956 | 200；2020-07-11 記者會報導全文。 | 僅支持「檢方於記者會提出雪崩解釋」。不背書其中每項事故重建或精確氣象數字。 |

Nature 的成功擷取發生於本輪 05:27 UTC；先前 `research-science.md` 記載受阻，是當時狀態，不應抹除。也不把現在取得正文改寫成所有 PDF、補充資料都已看過。2019／2020 官方完整技術報告本輪未取得，不宣稱它不存在。

## 完整主張表

判定針對影片實際表述；方法論界線採 CONFIRMED 表示與已讀原件／模型範圍一致，不表示已證明某個未記錄事件從未發生。`CHANGED` 表示本輪曾修正，最終版本已套用並回讀通過。

| # | 主張 | 位置（句 ID／scene.data） | URL | HTTP | 判定 | 前 → 後／核對結果 |
|---|---|---|---|---|---|---|
| c01 | 鞋子與用品留帳，九人離開；從帳篷追線索 | nvja、86sh、eyqe | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 385 頁記近乎全部鞋、外衣、物品留下；稿說多數屬保守轉述，問句不替離營編原因。 |
| c02 | 1959 年事件，旅程在二月初中斷 | u9ci、2fix | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 不宣稱精確死亡時刻。 |
| c03 | 不同鞋襪印，不能說全員裸腳 | q82x、e4jx、9pkr、3hs8、b8fk、z6at、88ft、nueh；hook-records、document-footprints-slot.data | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 386 頁列近乎赤腳／棉襪／氈靴等；「你以為」在下一句即修正。另見 F3 畫面凹凸修正。 |
| c04 | 足跡向山下谷地森林，不能讀出心情 | e4jx、9pkr、34gm；hook-records.data | https://dyatlovpass.com/case-files-309-312-ru | 200 | CONFIRMED | H1／H3 共同支持方向；沒有宣稱知道每個人的心理。 |
| c05 | 北烏拉冬季滑雪行程，原十人、一人因病折返、九人繼續 | mvpk、2dku、5kgy；journey-numbers.data | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 384 頁名單與折返記錄支持，10−1＝9。 |
| c06 | 成員有學生及已工作者，非九名大學生 | k6p3、cwig | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 384 頁另列旅遊基地教練及工程師。 |
| c07 | 山坡帳篷為最後營地與調查起點 | qvru、s24k；camp-platform-context.data.prompt | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | H1／H3 描述山坡搭帳平台，插圖不能當精確原貌。 |
| c08 | 1959-02-26 白天下午發現帳篷 | 2fqy、rdfd；search-date.data | https://dyatlovpass.com/case-files-298-300 | 200 | CONFIRMED | H4 直接記當日下午，H1 也列 26 日；沒有混成首批五人的同日發現。 |
| c09 | 清雪查看帳篷時內部無人 | 9rjv | https://dyatlovpass.com/case-files-298-300 | 200 | CONFIRMED | H4 明述 26 日除雪後確認無人。 |
| c10 | 搜救者見到的是事後現場 | yqn7、9msp | https://dyatlovpass.com/case-files-298-300 | 200 | CONFIRMED | 事發與搜救有時間差；問句不額外宣稱痕跡怎樣消失。 |
| c11 | 1959-04-16 鑑定認為切口由內側刀切，依布料微痕 | fyrp、9ihg、haem、euwn；tent-examination.data | https://dyatlovpass.com/case-files-303-304-ru | 200 | CHANGED | 日期與檢驗結果支持；euwn 刪去不能證明的「不是當場一眼看穿」，見 F1。 |
| c12 | 切口方向不等於九人離帳次序 | fmgf、xcze；cut-inference.data | https://dyatlovpass.com/case-files-303-304-ru | 200 | CONFIRMED | 鑑定未識別誰先割、每個人從何處離開；未混用切口計數。 |
| c13 | 調查以用品留帳推論突然離營，非逐人目擊 | 4jq6、8kqa、jhkz、8xtt；document-shoes-slot.data | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 385 頁明確以物品配置作推論；結尾「顯得急迫」維持判讀而非全知事實。 |
| c14 | 結案書 8–9 組，Tempalov 8 組、未確認第 9 | kb6v、h63r、43t2；footprint-count.data | https://dyatlovpass.com/case-files-309-312-ru | 200 | CONFIRMED | 對 H1／H3；不把不同觀察範圍併成九條完整線。broken-trail 的 F3 同步修。 |
| c15 | 一位勘驗者判讀普通步伐，不能推出全程不跑不怕 | y9t5、ngnu、6wja、nueh；stride-inference.data | https://dyatlovpass.com/case-files-309-312-ru | 200 | CONFIRMED | 312 頁是 Tempalov 觀察及判讀，稿保留範圍界線。 |
| c16 | 二月底發現帳篷，隨後陸續找到五人，五月最後四人；無當夜倖存口述 | up4g、nd7v、zhkv、46sm、5nwz；discovery-sequence.data | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 合讀 H1／H3／H4，沒有沿用不同首批日期的單一版本。 |
| c17 | 1959 年五月結案，自然力量使其無力克服 | peqt、wjny、qeyq；natural-force-slot.data | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 1959-05-28，387 頁原句；旁白為繁中轉述，最終圖片僅原文關鍵詞，非偽造直譯全文。 |
| c18 | 自然力量沒有神祕／超自然含義，也未提供雪板機制 | ca3c、78gf、n8qm；natural-not-supernatural.data | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 原詞 стихийная сила；不追認是哪一家媒體加字。 |
| c19 | 結案書多頁，內有物品足跡，不能只讀一句 | f8ug、jqdj | https://dyatlovpass.com/case-files-384-387-ru | 200 | CONFIRMED | 384–387 共四頁；稿未把全文縮成一句。 |
| c20 | 2019 對外說明複查，2020 記者會提出雪崩說法 | ek8t、dpfd、2ebc；review-timeline.data | https://www.interfax.ru/russia/649229 、 https://www.interfax.ru/russia/716956 | 200／200 | CONFIRMED | 明標新聞來源，不說重啟刑案，不以新聞中的詳細重建當確證。 |
| c21 | 低表觀坡度與延遲是模型欲回應的問題 | xzmn、m3z2 | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 論文導言列此疑問；問句不預先認定當夜發生。 |
| c22 | 2021 年 Gaume、Puzrin 兩人研究小型雪板可行機制 | vtj7、6x68；model-paper-card.data | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 年份／作者正確；明標可行性模型、非當晚實測。 |
| c23 | 連結雪層能以雪板形式失穩 | kf77；cohesive-snow.data.prompt | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 模型 cohesive slab 簡化解說，非特殊材質鑑定。 |
| c24 | 埋藏弱層可能先破壞 | 4q3w；buried-layer-close.data.prompt | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 用條件句，未宣稱已挖到 1959 真實雪剖面。 |
| c25 | 平均表面與局部階梯坡度不同 | advd、zr5j、53be、wetp；surface-and-ground.data | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | Results 地形與坡度段；無安全角度規則。 |
| c26 | 模型假設弱層跟隨局部傾斜地形 | h5qj、rajs、vrd2；model-first-two.data | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 已明說「假設」，沒有把該幾何當史料實測。 |
| c27 | 切出搭帳平台改變支撐與受力 | 8tk6、3ywy、rajs、vrd2；model-first-two.data | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 對應切坡邊界條件，不承諾任何切坡必然雪崩。 |
| c28 | 切坡後可能延遲，非立刻滑落 | be3v、m574 | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 在既述模型條件下；沒有設定固定倒數時間。 |
| c29 | 風可搬既有積雪，堆積後增重 | azmm、p4m5、a5xc；wind-moves-snow 等 prompt | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 對應 wind-driven deposition，畫面沿地搬雪，不以新降雪替代。 |
| c30 | 慢慢加重量的布吊帶比喻 | 76ai；weight-analogy.data.prompt | —（類比） | — | OUT OF SCOPE | 未宣稱是雪板實驗或同一破壞材料；保留「像」。 |
| c31 | 逐漸載重、弱層裂縫擴展後雪板可能滑動 | zj3d、92m4、m574；model-later-two.data | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 對 Results delayed-release；不是聲稱單靠重力定律重建當晚。 |
| c32 | 檢驗延遲數小時，推定時距參與回算，非獨立確切時刻預測 | pxkt、6n95、c5xt；model-hours、model-not-timer.data | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | Results 及 Methods 明列回算 Q；稿未搬回各處不同用途的小數區間。 |
| c33 | 厚度、強度、風載雪量影響模型；當夜參數非完整現場實測 | e9q7、xchu | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | 參數與 Discussion 假設／不確定性支持，不說所有參數全無任何估計。 |
| c34 | 小範圍雪板與大崩塌不同；風吹雪可能改變痕跡但非證明當年如此 | h6hn、rhik、iry6；small-slab-remains 等 prompt | https://www.nature.com/articles/s43247-020-00081-8 、 https://www.nature.com/articles/s43247-022-00393-x | 200／200 | CONFIRMED | 未普遍化為雪崩必然不留痕，也未用後來個案證明 1959 痕跡消失。 |
| c35 | 2021 年 9 月無人機測量可能帳篷位置附近 | swkf、24gt、mhqb；survey-date.data | https://www.nature.com/articles/s43247-022-00393-x | 200 | CONFIRMED | Into the mountains 直接載明 March 與 September 分次考察。 |
| c36 | 測地形發現局部較陡階梯 | mpms、ay45 | https://www.nature.com/articles/s43247-022-00393-x | 200 | CONFIRMED | Fig.2／DEM 說明支持；不把具體角度當現場安全門檻。 |
| c37 | 地形測量不能還原當年雪層厚度和強度 | v2ar、nf2q | https://www.nature.com/articles/s43247-022-00393-x | 200 | CONFIRMED | 地形 DEM 與雪材力學參數不同；稿的證據邊界正確。 |
| c38 | 作者報告 2022-01-29 鄰近坡面兩處近期雪板痕跡 | j3ju、z9pi；avalanche-date.data | https://www.nature.com/articles/s43247-022-00393-x | 200 | CONFIRMED | Fig.3d/e 日期及正文數量相符，明說作者報告，未稱當晚影片。 |
| c39 | 後來照片在鄰近坡面，不能搬成帳篷上方當夜過程 | r7wf、hrcj | https://www.nature.com/articles/s43247-022-00393-x | 200 | CONFIRMED | 原文距帳篷附近幾公里、年份不同；稿未精確化坡向或距離。 |
| c40 | 測坡和雪崩照片來自不同時間，各補不同支持 | 2cqd、x8az；two-dates-not-one.data | https://www.nature.com/articles/s43247-022-00393-x | 200 | CONFIRMED | 2021-09 與 2022-01 分列，未假稱同次測量。 |
| c41 | 後來雪板更軟、坡更陡、無切坡、觸發可不同 | 7tq6、6yky、khhj；model-field-difference.data | https://www.nature.com/articles/s43247-022-00393-x | 200 | CHANGED | No final word 直接支持差異；7tq6 補「比起模型假設」，見 F2。 |
| c42 | 2022 考察原定雪層測試受天氣阻礙 | wh89 | https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/ | 200 | CONFIRMED | 直接作者訪談說未能執行規劃測試，不誤說已量齊參數。 |
| c43 | 作者跟進與校方新聞同源，網頁多不代表獨立試驗多 | r295、apqe、hve7；shared-source.data | https://www.nature.com/articles/s43247-022-00393-x 、 https://ethz.ch/en/news-and-events/eth-news/news/2022/03/the-dyatlov-pass-mystery-and-what-a-research-article-can-trigger.html | 200／200 | CONFIRMED | 作者、引用及考察內容一致；不否定後續確有新增現地資料。 |
| c44 | 模型支持可能觸發，未重建九人當夜完整行動 | vee2、a6qq、u6ta、u3tt、kum7、tnsj、bi2x；case-status、unclosed-case、outro.data | https://www.nature.com/articles/s43247-020-00081-8 | 200 | CONFIRMED | Discussion 明說離帳後行為與位置等超出論文範圍；「未結」為系列知識狀態，非宣稱刑案仍偵辦。 |
| c45 | 未知不表示每種傳說都有相同證據 | uqzu | —（站主觀點） | — | OUT OF SCOPE | 與 brief 站主立場一致；不作可量化科學結論。 |
| c46 | 當年足跡示意為凸起壓實雪形、周圍風蝕低面 | hook-footprints、trail-varied、boot-print-evidence、broken-trail、trail-downhill、stride-evidence、return-to-trail.data.prompt | https://dyatlovpass.com/case-files-298-300 | 200 | CHANGED | 初稿凹洞 → 7 景均改 raised compacted-snow forms；H4 299 頁支持，未新增口播數字或宣稱真實足形復原。 |

## 縮圖、metadata 與圖像涵義

| 範圍 | 結果 |
|---|---|
| `youtube.title` | 問「為何離開帳篷」，不宣稱已破案；人物／地名與正文一致。 |
| `youtube.description` | 多數鞋留帳、反問是否全員赤腳、2021 模型／2021 測坡／2022 鄰近痕跡均有對應。明說情境圖、繁中 CC 與非安全教學；沒有新數字。 |
| `youtube.tags` | 題材索引，無額外事實主張。 |
| `thumbnail.data` | 最終「鞋子還在／雪夜裡的空帳篷」有 H1 留鞋記錄支持；情境插圖不冒充事故實攝，也未寫雪崩定案。 |
| 全部 shot prompts | F3 已解。主要為匿名背影、用品、空景、generic 雪層與模型示意；未要求重製九名死者、作者或搜救者肖像。開場 title 新增「情境插圖與科學示意｜非當晚攝影」。畫面生成後仍須像素審查。 |
| `assets` | 最終含 385／386／387 三份原件局部，已讀 exact Commons URL、作者、PD-RU-exempt、日期及裁切／透明留邊說明，並親自實看三張 stock PNG。結果見下表；不再沿用空 assets 的較早狀態。 |
| 來源名稱 | 最終已統一為「Interfax（2019）：檢方對外說明一般監督性複查」，與正文一致。 |

### 三份素材與 caption 回讀

Commons 授權頁與 API 資訊由本輪受派的 listener 逐頁核對，原件 URL／SHA／裁切矩形見 `asset-register.md` 及外部 `_audit/source-assets.json`；本查核者另外開啟實際成片用 PNG 核對內容。這裡不將 listener 的全頁像素讀取算為自己完成。

| scene | 檔案 SHA-256（即 stock 檔名） | caption／實看結論 | Commons URL |
|---|---|---|---|
| document-shoes-slot | `bf338fb136401d2bb9358a7bceeb46abe20a9ee55b7bdcf263d483eb67d1963f` | 385 局部確有鞋子、外衣、用品、突然離營推論及內側切口；caption 相符。沒有遺體圖片或傷勢文字。 | https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_385.jpg |
| document-footprints-slot | `1c31a7da3de0851b0645f7636df4a6bc07a8252447a8ad74f98e2f9dca709b40` | 386 足跡段確有 8–9 組及鞋襪差異；caption 相符，下面傷勢段已排除。原件內 500 公尺未被口播誤用為另一證人的 50 公尺。 | https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_386.jpg |
| natural-force-slot | `f90b4c557783827cfde143fb4ddfd59ae08e93b9b97a05026a9cb3e288ddf25d` | 387 只呈 стихийная сила 關鍵詞，caption 正確稱關鍵詞而非完整結論；頂邊少量鄰行墨跡無新增可讀傷勢敘述。 | https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_387.jpg |

三筆 assets 的作者均為 Lev Nikitich Ivanov、日期 1959-05-28、PD-RU-exempt，source 已含署名及修改說明；字幕圖說沒有把民間託管掃描說成官方檔案館直接提供。輸出檔已核 SHA 與檔名一致。

## 摘要與待完成項

- 已核：46 組 scene claims；41 組 CONFIRMED、3 組 CHANGED 並已回讀通過、2 組 OUT OF SCOPE（類比／站主觀點）。NOT FOUND：0，未解 must-fix：0。
- 會變的事實：不把 2021／2022 描述成最新或唯一模型；本輪來源讀取日 2026-10-12。沒有價格、版本、在任職稱或「此後無新報告」等易過期新斷言。
- 站主觀點不符：0；保留未知、區分模型與事件、原文優先均符合 brief。
- Listener 報告範圍：最終 119 句，超過 40 字的句子 0；旁白 URL／拉丁詞／括號 0，say 欄 0。兩組 reveal 對齊改句及 qvru／4jq6／z6at 口語修訂已讀，沒有新事實差異。CTA 是互動用語而非查核主張。
- 原生 lint：本查核者於最終 `98b2fe19…` 執行，**exit 0，0 errors／4 warnings**。提醒為 daylight、snow、central 詞頻及開場章約 29 秒；第一句即提出鉤子，這些不是未解事實錯誤。估長 10.1 分鐘／2063 spoken units，不等於實際 TTS 長度。
- SECOND ROUND：**規則不強制**；本輪實質事實修正 3 組，未超過 3。
- 腳本事實查核完成。後續仍須原生製作關卡、生成圖／版型／字幕與實際影音審查；本報告不代替那些檢查或站主核准。

## 2026-10-12 停頓調整回讀

在保留上方完整覆核的前提下，逐欄比對外部 `_audit/outro-pause-correction/video-before.json` 與目前 `video.json`。前檔 SHA-256 為 `98b2fe192185644dd7a36a3deac8c4f8c9314a54486cedf1ff23cdd85dfae2f8`；目前為 **`f4291c340eef12bac0ba08980f9cbe7f39bba6309131a8fb50e379e8f31755c8`**。

JSON 全樹只有兩處差異：`scenes[99].lines[0]`（`bi2x`）與 `scenes[99].lines[1]`（`x53t`）各新增 `pause_after_ms: 100`。原欄位未設定；`tools/video/core/timeline.mjs` 的 `DEFAULT_PAUSE_MS = 300`，所以兩句預設停頓各由 300 毫秒改成 100 毫秒。旁白文字、emotion／voice、全部字卡、提示詞、場景主張、metadata 與 assets 均完全相同。

`claims.md` SHA-256 仍為 `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`，與完整覆核版本一致。**0 新增事實修正、0 新增 must-fix；事實查核 PASS 延伸綁定目前來源。** 本次只核來源差異，未讀寫音訊或其他媒體，也未重跑製作／音訊品管；先前 lint 紀錄仍明確屬於 `98b2fe19…` 版本。

## 2026-10-12 已套用視覺提示詞修正回讀

獨立比對外部 `_audit/pilot-before-prompt-fix/video.json`（SHA-256 `f4291c340eef12bac0ba08980f9cbe7f39bba6309131a8fb50e379e8f31755c8`）與現行來源（**`ae85b2c4f5c1b95ca782603725b4a162140ece65c32b7cccafd6df82f695cb35`**）。將已通過的 `_audit/pilot-prompt-fixes.json`（SHA-256 `597e2219be8e8b5b92848c5c474ee20cbcb17bb2e297eac17fca44f17d4641e7`）21 個 after 逐一套入記憶體中的前版，結果與現行 JSON 完全相同；再做全樹 diff，恰為 **21 處 `scene.data.prompt` 差異**。

修正範圍是 14 個高坡／營地外景的圓鈍、開闊地形，以及 7 個既有現場足跡的鞋形、隆起頂面與周圍較低雪面。提案已逐項對應旁白及主張，詳見外部 `_audit/pilot-prompt-fixes-review.md`；沒有新增 1959 實測數值，沒有把後來鄰坡雪崩或現代考察搬成當晚實錄。這是讓生成圖遵守原有主張的描述修正，**0 新增事實修正、0 新增 must-fix**。

所有旁白文字、emotion／voice、兩句結尾停頓、camera、look、字卡、場景主張、metadata 與 assets 保持完全相同；`claims.md` SHA-256 仍為 `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。套用收據記錄 speech hash 仍為 `d9e4eeb59801eac3`，pictures hash 由 `2e0fd759eda41446` 變為 `628de277f9a81782`；本次獨立證據為來源全樹比對，未重算媒體或執行製作程序。

原完整腳本覆核與前項停頓回讀保留，**事實查核 PASS 延伸綁定 `ae85b2c4…`**。此結論不代表重畫結果已通過；新 selected 圖仍待逐張像素覆核。本次只修改本查核報告，未讀寫音訊／圖像媒體或干預正在執行的音訊品管。

## 2026-10-12 五處鏡位前綴回讀

依 `_audit/framing-prefix-backup/receipt.json` 與實際檔案 SHA 核對，前版 `ae85b2c4f5c1b95ca782603725b4a162140ece65c32b7cccafd6df82f695cb35` 到現行 **`169d607735c155abb988c62643db72567f9d947498d479e1d691ba98bd24a6a0`**，恰等於 `_audit/framing-prefix-fixes.json`（SHA-256 `82a4dd50b12f92fe2bbba09bf41a8c000b0210361a1c587feedd47bd609539ff`）五案的精確套用。

只有 `hook-footprints`、`trail-varied`、`broken-trail`、`trail-downhill`、`return-to-trail` 的 prompt 開頭改用可辨識的 Close-up／Medium shot／Wide shot，保留低斜視角；各前綴之後的內容逐位元相同。完整 JSON 其餘欄位未變，`claims.md` SHA 仍為 `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。**0 新增事實修正、0 must-fix；事實查核 PASS 延伸綁定現行 `169d6077…`。** 僅追加本報告，未動凍結來源、媒體或執行中的生成程序；新圖仍待像素覆核。

## 2026-10-12 七張原創圖解整合回讀

以 `_audit/footprint-vector-integration/video-before.json`（`169d607735c155abb988c62643db72567f9d947498d479e1d691ba98bd24a6a0`）重建核准提案，確認現行 **`4979754cb76c36e8301ec6bab8d12b414a15f876b92459954440e95d8b6fce21`** 只有七個足跡場景的 `template`／`data` 精確改成所審 diagram，並在保留原 assets 的末尾增加七筆對應 SVG 的 Mokaair 原創署名／示意揭露；其他全部欄位完全相同。旁白、voice、場景主張與時序未變，`claims.md` SHA 仍為 `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。

所套用提案 SHA-256 為 `23e44df5b1b5a4c701496f7e0be48e51010c487db896a1eb49a4f6f1ba45ff3b`。本查核者已獨立實看全部七張原生 PNG、核對七 SVG／七 PNG 的 SHA，結果 PASS_WITH_NOTE、0 material；完整綁定與逐圖觀察在外部 `_audit/footprint-vector-independent-review.md`（`beca585de31dd369880fb85cba56914025b5c7e0d3e084564f646b49a822e24a`）。圖形標明非現場照片、未按比例，沒有九條完整路線、實測步距或全程情緒推論。**0 新增事實修正、0 must-fix；事實查核 PASS 延伸綁定 `4979754c…`。** 此次僅追加本報告；65 張其餘生成圖、成片節奏與音畫同步仍是後續關卡。

## 2026-10-12 四句口語修訂及帳內用品提示詞回讀

由 `_audit/audio-rewrite-1/video-before.json` 的 `4979754cb76c36e8301ec6bab8d12b414a15f876b92459954440e95d8b6fce21` 出發，在記憶體只套收據中的四句修訂，再套 `_audit/search-objects-correction.json` 的一個提示詞，結果與現行 **`30eb4fa95a6a3737d2d3e328ae409a86158550ea40c917829762a256049634c4`** 完整 JSON 精確相等。全樹 diff 恰為四個 `lines[].text` 與一個 `data.prompt`，沒有其餘差異；未採用備案 `88ft` 亦完全未動。

四句為 `xzmn`「山坡看起來不夠陡，為什麼雪板還可能滑落？」、`c5xt`「所以不能拿算出的時間，回頭推算九人何時出事。」、`a6qq`「雪板滑動的研究，提供了可能迫使人離開營地的一種機制。」與 `u3tt`「特定條件下，雪板可能滑動，這是能夠檢驗的解釋。」已核對獨立文字審稿 `_audit/audio-rewrite-independent-review.md`（SHA-256 `fc775cd275739145a01f11ddba532a2f10586093c8bc9b62175bf61a6ec0350b`）的核准文字；可能性、條件限制及不能替九人當晚計時的意思保留，沒有新數字或新事實。

`search-objects` 精確採用已審的帳內冬靴、外套及布袋提示詞，與「仍留在帳內」旁白一致；其審查 `_audit/search-objects-prompt-review.md` SHA-256 為 `908870861c1f681696c4900fea32b19c4291943a5fb0dc80b69db0ad1c51c1e5`。它不宣稱精確物品清單或原始擺放位置。其他旁白、voice／emotion、停頓、字卡、diagram／SVG 參照、claims、assets 及運鏡均未變；`claims.md` SHA-256 仍為 `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。

**0 新增事實修正、0 must-fix；事實查核 PASS 延伸綁定 `30eb4fa9…`。** 四句文字修訂會改變 speech hash，不把舊音訊驗收當作新句已通過；本次沒有聽讀新 TTS、改寫媒體或干預執行中的 producer。後續仍須對新音訊及生成圖分別實際覆核。

## 2026-10-12 八鏡材料性畫面修正回讀

獨立逐欄比對 `_audit/keyframes-before-bulk-fixes/video-before.json`（`30eb4fa95a6a3737d2d3e328ae409a86158550ea40c917829762a256049634c4`）與現行 **`a7c23cd82f138834c85c1d41eaf4ba50725d20cb320924ae842c63246bb0dc33`**，全樹恰有八個 `data.prompt` 差異：`hook-slope`、`journey-pack`、`search-empty-interior`、`tent-cut-detail`、`remaining-boots`、`tent-opening-empty`、`spring-empty-ravine`、`archive-reader-back`。

將已審 `_audit/bulk-prompt-fixes-round1.json`（SHA `d6407cdc3a33dbffb038b541aa85d7509266f52f24b73904b70daa219416d3df`）及 `_audit/middle-material-prompt-proposal.json`（SHA `2066f42e4c57c9fd4579348cb36d9acb67e19e396fe67c39027905554edd5632`）的八個 after 精確套入記憶體前版，可重建現行完整 JSON。它們修正營地與林緣關係、用品或人物造形、冬季帳內背景、切口、毛氈靴，以及誤生聚落／峭峰；不新增歷史實測值、人物身分或當夜動作。門口雪面提案已刪除未受擾動的過度限定字。

全部 **119 個 line 物件**逐項相同，包含旁白、emotion 與停頓；voice、look、camera、字卡／圖說、主張、assets、metadata 及所有其他欄位完全未變。`claims.md` SHA 仍為 `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。備份與目前外部 `timeline.json` 逐位元相同，SHA 均為 `f4ab52a1e7ccceccd88576b8bbc8f273cb35f204730ec3d4bb825c251305dc82`；收據所記 speech hash 仍為 `296feca213cf8271`，pictures hash 改為 `1b4cf094f12e9b3c`。

**0 新增事實修正、0 腳本 must-fix；事實查核 PASS 延伸綁定 `a7c23cd8…`。** 這是來源與時間軸的增量回讀，八張重繪仍須另行 actual selected 像素覆核；本次未改來源／媒體／manifest、未接受候選或呼叫付費程序。

## 2026-10-12 位置向量整合與帳內鞋子提示詞回讀

本段由 `h03_research` 追加，只核本次來源差異；此代理是新 SVG 作者，圖像另有 `h04_audio_wording` 的獨立實看報告，不冒稱作者自查為獨立像素覆核。

由 `_audit/slope-and-boots-integration/video-before.json`（`a7c23cd82f138834c85c1d41eaf4ba50725d20cb320924ae842c63246bb0dc33`）出發，在記憶體只套已審提案的 `hook-slope.template/data`、收據的 `remaining-boots.data.prompt`，並追加一筆 `Mokaair original` 的位置 SVG asset，重建結果與現行 **`250e1d192dd7463cb3f73236a9eadcba52ceb0cb01b9ddb135d4428744eee5f9`** 完整 JSON 精確相同。機讀證據為外部 `_audit/slope-and-boots-factual-readback.json`。

`hook-slope` 保留 c01 及 `86sh` 問句，改以高處帳篷、低處林緣、中間開闊雪坡的通用位置關係示意承接原主張；caption 明列非現場影像、未按比例。沒有新增實測位置、距離、坡角、九人路線、離營動作或原因結論。`remaining-boots` 只將背景限定為封閉帆布帳壁與地布，避免生成海面；仍是用品情境，不宣稱復原原帳篷當時開閉狀態或精確物品配置。

最終向量提案 SHA 為 `6ea4aae1bda99a279d1468c8307c9809e5f094747d5770270fa24a2f9836a7a0`；SVG／原生提案 PNG 已實算 SHA 與提案吻合。獨立像素覆核 `_audit/slope-vector-independent-review.md` SHA 為 `0019b806756656bb1c6a0b40339db2462d95e46194f4b3d567c6620a8c1009c1`，判定 PASS、0 material；素材署名與揭露已登錄 `asset-register.md`。

全部 **119 個 line 物件**（含 emotion、停頓）、voice、look、主張及其他未列欄位完全相同。`claims.md` SHA 仍為 `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。回讀時備份與當前 `timeline.json` 逐位元相同，SHA 均為 `f4ab52a1e7ccceccd88576b8bbc8f273cb35f204730ec3d4bb825c251305dc82`；此處不把未變旁白時間視為新 diagram 已完成正式 render。結構為 100 景、64 張 AI shot、36 個非 shot 場景，含八張原創 SVG。

**0 新增事實修正、0 腳本 must-fix；事實查核 PASS 延伸綁定 `250e1d19…`。** 這次只追加本報告與素材登錄，沒有修改 canonical source／媒體／manifest 或呼叫 provider。新的鞋子 selected、正式字卡／成片、字幕與聲音，仍由各自像素及播放覆核證據判定，不由這份來源回讀代替。
