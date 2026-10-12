# H03 第二輪獨立事實查核

查核者：h03_research。日期：2026-10-12（Asia/Taipei）。本代理做過製作前來源刷新及兩張公有領域素材收據，沒有撰寫本片旁白，亦非第一輪查核者。這一輪由主代理額外指定；只寫本報告，未修改 video.json、claims.md 或 brief.md。

**結果：本輪覆核範圍通過，沒有未解決的事實問題。** 第一輪 F01–F03 均已解決。另依主代理指定，固定抽查 c01、c04、c07、c10、c13、c16、c19、c22、c25、c28、c31、c34，再擴查編輯修訂涉及的命題。這是系統抽樣，不冒稱隨機抽樣；亦不把本報告稱為重新查完全部 35 組。

**最終適用版本：video `08b8fc80c9b9720ee30cf1ccf73f8f0d540a03e8b3ec6ef77166dde43237dca2`；claims `8872f4f0db0ddad05367b8c8c8597ece64c83f556983fd620dbbbd301a9e39dc`。** 下列文字覆核先綁 40b1d0d2 版本，其後只追加 c21 的直接來源；最後差異回讀證據見尾註。

## 綁定輸入與方法

- 主要文字覆核 video SHA-256：`40b1d0d2de9d11f20b5182634be46bdadeb5f753004be0c3377d8d989cfe36c0`。
- 同版 claims SHA-256：`2706ab3877f712a916920d22dcb4ffafe2e84826cd7807295a411dd7c088f4a6`。
- brief SHA-256：`98e2a3a28c529714bef64d4c42bd76aca5e08ab1cb9318df5c897d7f8cb0bdfc`。
- 對照第一輪 verify-1 SHA-256：`2b982153473e1e87e18c5defd5356d02a524f8a8da6f16e3e373aa2cb002cfe5`；已讀其 F01–F03、35 組表及完整修訂說明。
- 實際稿件是 115 景、139 句、82 個 shot、2 個 photo；無 say/say_for 覆寫。已回讀文字、非 shot data、sources 與包裝資訊，不把 claims.md 當證據。
- 主代理限定本輪只寫 verify-2，故未重建或覆寫第一輪提取檔；唯讀參照外部 `_audit/verify-final-input-inventory.json`，並直接從當前 video.json 提取核對。39 句整合修订依 `_audit/editorial-revision.json` 及後續 refinement、emotion 收據逐句回讀。
- 本輪直接請求使用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同主機相鄰請求至少間隔 1.1 秒；HTML 註解剔除後讀正文。對 HTTP 200 的 challenge 不作成功正文。直接讀取失敗而 web 可讀者，下面明確區別。

## 第一輪三組修正的獨立回讀

| # | where | before → after | 獨立核對 | verdict |
| --- | --- | --- | --- | --- |
| F01 | denser-air/fdqr；c13 | 無條件「越低、密度越大、壓力也越大」→「往更密的空氣移動，天體可能承受更大壓力。」 | [JPL13] 同時描述氣動壓力、物體強度與減速。現在「可能」不再暗示壓力必然隨下降單調增加；claims 保留仍高速的條件。 | CONFIRMED：前輪問題已解決，本輪未再改稿 |
| F02 | sampling-location/vvez；different-lake-depths/vpzm；c25 | 無據的岸邊／湖心採樣位置爭點→泥層定年與沉積層次判讀 | [C23] 公開全文直接討論上部放射性定年、下部年紋計數解讀及地震地層判讀；最後要求湖心鑽探。兩句及泥芯 prompt 均對得上，沒有宣判任何一方勝出。 | CONFIRMED：前輪問題已解決 |
| F03 | sources[10].title | 錯誤書目名→`Computation of a possible Tunguska’s strewn field` | [A24] 作者摘要標題相符；Icarus 408、2024-01-15、115845 與 DOI 中 2023 可並存，不是出版年矛盾。 | CONFIRMED：前輪問題已解決 |

## 抽查與修訂相依主張表

「固定」是每三組取一的指定樣本；「擴查」是本輪為涵蓋所有具事實內容的修訂加入。CONFIRMED 表示措辭與限制能由所讀來源支持，不表示研究爭議已消失。所有「維持」均指本輪沒有改稿。

| # | claim | where | URL | HTTP／實读 | verdict | before → after／判定界線 |
| --- | --- | --- | --- | --- | --- | --- |
| c01 固定 | 1908-06-30 早晨、西伯利亞 | date-of-flash/wbq3、data；new-forest/3wh5 | [N23]、[EO25] | N23 GET 200 正文；EO web 正文 | CONFIRMED | 維持；無未核對的分鐘精度。 |
| c03 擴查 | 外圍朝外倒、中央部分樹幹仍立且受損 | two-tree-patterns/6afz、8cii、data；evidence-layers/data | [N23]、[S07] | GET 200 正文 | CONFIRMED | 改後兩句仍是既有觀察；「有些」保留部分性，沒有說中央全完好。 |
| c04 固定 | 大氣中解體釋能能解釋地面破壞，非所有碎片必氣化 | airburst-ground/fh3w；evidence-layers/4tzv；new-forest/3wh5；outro/wg93 | [N23]、[N19]、[S07]、[A24] | GET 200 正文／作者摘要 | CONFIRMED | 維持；「最有力的解釋」是多來源綜合，沒有聲稱本片實驗證明。 |
| c06 擴查 | 約 2,000 km² 有測繪支持，整體近蝴蝶形 | damage-area/data；measurement-layers/w2u4；areas-not-counts/data | [N23]、[L07] | N23 GET 200；Longo 本輪 HEAD 200，實讀當日下載原 PDF 相關段落 | CONFIRMED | NASA 830 平方英里與 Longo 2,150±50 km² 支持口語約兩千；地景概念圖不當測繪。 |
| c07 固定 | 1908 年已有地方報導，研究者後來才抵現場 | contemporary-newspaper/pbf7、caption；not-forgotten/zrku、xgep | [L07]、[NP] | Longo 原 PDF 相關段落；當日檔頁及原圖實讀 | CONFIRMED | 改後不把 1927 當事件首次被知道。剪報只展示報導存在；未翻譯未核對內文，未念檔名日期。 |
| c08 擴查 | 地質學家庫利克 1921 出發未抵、1927 抵達 | kulik-expeditions/6qay、wkui、data | [N23] | GET 200 正文 | CONFIRMED | NASA 明確稱 geologist；1927−1908＝19。沒有把 1927 說成首次出發。 |
| c10 固定 | 大塊完整天體高速抵地的搜尋預期是坑及殘骸 | expected-iron/cvt5 | [N19]、[S07]、[APS] | GET 200 正文 | CONFIRMED | 維持；限大塊高速撞地，不延伸成每顆小碎片必製造大坑。 |
| c11 擴查 | 抽乾懷疑的沼澤坑，底下有老樹樁 | drainage-ditch/2pwk；old-stump-bottom/44d4；stump-not-meteorite/data | [APS] | GET 200 正文 | CONFIRMED | 2pwk 改後仍是當時尋找鐵塊的目的，非已認定天體成分。老樁細節是 APS 後世歷史敘述，原考察日記本輪未讀。 |
| c13 固定／F01 | 壓缩、強度、碎裂、減速與能量傳給大氣 | denser-air/fdqr；airburst-chain/uew5、jm2y、6s9v、data | [JPL13]、[S07] | JPL GET 403、web 正文；Sandia GET 200 | CONFIRMED | 前輪 F01 已解決；三個改寫步驟與卡片一致，沒有變成炸藥自行引爆。 |
| c14 擴查 | 近正下方受上方衝擊，外側有側向推力 | forces-two-positions/fyt5、hbj5、data | [S07]、[N23] | GET 200 正文 | CONFIRMED | Sandia Movie 2 文字支持上方衝擊。比較是幾何簡化；來源欄已明示非比例圖，無單棵樹算高度。 |
| c16 固定 | 不同模型是 3–5 與 10–30 百萬噸 TNT 當量 | energy-models/r359、wfff、data；energy-unit/kcfm | [S07]、[N19] | GET 200 正文 | CONFIRMED | 口播「三到五百萬」「一千到三千萬」分別匹配 3–5 Mt、10–30 Mt。未合成同篇 3–30 區間。 |
| c17 擴查 | 2013-02-15 事件有現代觀測及碎片 | modern-comparison-date/data；different-events/wxdt、data | [JPL13]、[N19] | JPL GET 403、web 正文；NASA GET 200 | CONFIRMED | 維持；不把亮點高度、碎裂高度或別篇能量塞進比較。 |
| c18 擴查 | 2013 可支持機制，但其條件非 1908 的直接實測 | different-events/34vg、data | [N19]、[JPL13] | 同上 | CONFIRMED | 改後保留事件大小與入射條件不同；「不能直接套用答案」是合理限制。 |
| c19 固定 | 八千萬的估算前提與 8,000／約 2,000 km² 約四倍 | wide-assumption/8yu4；assumption-propagates/h5rn、phjq、mkxr、data；areas-not-counts/data | [B25]、[L07] | PMC GET 200 全文；Longo 原 PDF 相關段落 | CONFIRMED | 8yu4 現為「大約是…四倍」，不再有增加四倍＝五倍的歧義。2025 評論追查 1933 估算；本輪未读 1933 原文。 |
| c21 擴查 | 有居民經歷且傷亡記錄不完整，不說無人傷亡 | measurement-layers/5w6w；inhabited-camp/qvai；empty-stool/8dmz | [N23]、[EO25]、[J19]、[J18] | NASA GET／web 正文；J19 原刊搜尋回傳摘要，直接 GET 403；J18 公開原始摘要 PDF | CONFIRMED | 新增更直接的證據支持：J19 摘要明言保存不足、記載有矛盾。沒有把其研究下限改為確切總死亡數。NASA 兩頁措辭不同本身不能證明死亡數爭議；本輪以 J19 補強該點。 |
| c22 固定 | 候選微粒尚不等於公認來自事件主體 | scattered-small-stone/e4ma；no-identity-sample/ap9b；sample-identity/9zvs | [N23]、[EO25]、[A24] | NASA／arXiv GET 200；EO web 正文 | CONFIRMED | 維持；「公認」保留候選存在，不把未確認說成沒有任何石頭。e4ma 是提問，未新增發現。 |
| c23 擴查 | 切科湖是有爭議的候選，湖形非充分證明 | cheko-evidence-table/addm、data；cheko-name/data | [C17]、[C23]、[EO25] | Springer web 摘要／公開全文；EO web 正文 | CONFIRMED | 改後仍是待回答問題，未宣稱唯一成因。 |
| c24 擴查 | 年代是否早於 1908 是關鍵，2017 主張仍有反駁 | cheko-evidence-table/8a76、data；age-implication/data | [C17]、[C23] | 2017 web 摘要；2023 web 公開全文 | CONFIRMED | 問句對應已有爭論；不把 2017 摘要當定案，也不冒稱讀付費全文。 |
| c25 固定／F02 | 爭論定年、沉積層次，進一步鑽探有檢验價值 | sampling-location/vvez、prompt；different-lake-depths/vpzm；core-awaiting/i6te | [C23] | GET 200 但為 challenge；web 公開全文實讀 | CONFIRMED | 前輪 F02 已解決。文中上部定年／下部年紋批評與地層解讀支持現有概括；i6te 的「可能」沒有把鑽探成果當已發生。 |
| c26 擴查 | 2024 落區模型談可能存活，非已找到隕石 | possible-not-found/data；sources[10]；c26 | [A24]、[I24] | arXiv GET 200 摘要；原刊書目／摘要實讀 | CONFIRMED | 正確題名及刊期，沒有把 DOI 中 2023 當錯誤；未聲稱讀付費全文或模型已有實物驗證。 |
| c27 擴查 | 石質小行星受主要研究支持，細節仍未定 | evidence-layers/uhkz、data；no-identity-sample/ap9b | [N23]、[N19]、[A24] | GET 200 正文／作者摘要 | CONFIRMED | NASA 2023 偏向小行星、NASA 2019 模型偏石質，足以支持有保留的質性綜述；「多」不是研究票數或系統綜述比例。不得刪掉未定限制。 |
| c28 固定 | 無坑不自動替無證據說法加分 | no-saucer-needed/c4kc；case-status/bavy、data | [N23]、[N19]；brief 站主觀點 | GET 200 正文；brief 實讀 | OUT OF SCOPE（編輯立場） | 與 brief 一致，沒有冒充實驗結論；本輪未改。 |
| c31 固定 | TNT 當量是能量比較，不表示核爆 | energy-unit/kcfm；energy-models/data | [S07]、[N19]、[B25] | GET 200 正文 | CONFIRMED | 維持；來源談自然天體動能及 TNT 等價，未引入廣島倍率或放射性論斷。 |
| c32 擴查 | NASA 2019 為 6–9 英里，換約 10–14 公里 | model-height/cti2、q8h7、2etw、data | [N19]、[NIST] | GET 200 正文 | CONFIRMED | cti2 去掉無比較基準的「更高處」。6×1.609344＝9.656064；9×1.609344＝14.484096，四捨五入整公里為 10–14。是模型估值而非現場儀器讀數。 |
| c34 固定 | 普通石頭可能早已存在，須脈絡與成分才可歸屬 | older-ground-stone/dqeb；identity-testing/fbje；cheko-evidence-table/znur | [N23]、[EO25]、[A24] | NASA／arXiv GET 200；EO web 正文 | CONFIRMED | 從候選難以確認歸屬所作的科學判讀，非本片鑑定結果；未說只做一項檢測即可定案。 |

合計核對 25 組主張：24 CONFIRMED、1 OUT OF SCOPE、0 本輪 CHANGED、0 NOT FOUND；另核對 F03 書目為 CONFIRMED。這 25 組包含固定樣本 12 組及相依擴查 13 組。

## 39 句編輯修訂覆蓋與 16 句 reveal 回讀

已對照第一輪 changed 清單。真正需改正的歷史／科學命題只有 F01、F02 與書目 F03；其餘重整也逐句核其改後語義，不能僅因第一輪稱「風格」就略過。

| 修訂 line IDs | 回讀結果／對應 |
| --- | --- |
| 6afz、8cii | c03；外圍與中央分列，仍說部分中央樹幹。 |
| uew5、jm2y、6s9v、fdqr | c13；機制順序及「可能」限制正確。 |
| fyt5、hbj5 | c14；簡化受力方向，未量化成單一精確模型。 |
| r359、wfff | c16；兩組既有數字及 TNT 等價未變。 |
| h5rn、phjq、mkxr、8yu4 | c19；假設、轉述、表面確定性、約四倍，未生新棵數。 |
| addm、8a76、znur、i6te、vvez、vpzm | c23–c25、c34；湖形／年代／物證分開，定年與層次用真正爭點替代無據採樣位置。 |
| 4tzv、3wh5、wg93 | c04；空爆回答主線，無全氣化斷言。 |
| uhkz、ap9b | c27、c22；質性偏向與公認樣本未定。 |
| cti2 | c32；取消跨模型「更高」比較，保留高空與既有高度。 |
| 6qay、wkui | c08；地質學家職稱及兩個年份正確。 |
| zrku、xgep | c07、c08；居民早知道與研究晚到場分開。 |
| 2pwk | c11；仍是當時搜索鐵塊的預期。 |
| wxdt、34vg | c17、c18；現代證據與歷史回推不混用。 |
| w2u4、5w6w、qvai | c06、c19、c21；面積有測繪，棵數／傷亡記錄不冒充精確統計。 |
| e4ma、248y、njit | 提問與 CTA，OUT OF SCOPE；沒有增添實質事實主張。 |

指定 16 句 reveal 重整另逐句與 data 對拍：`6afz, 8cii` 對應 compare 左右；`uew5, jm2y, 6s9v` 對應三步；`fyt5, hbj5` 對應左右受力；`r359, wfff` 對應兩组模型；`h5rn, phjq, mkxr` 對應三步引用鏈；`addm, 8a76, znur` 對應湖形、年代、物證三列；`4tzv` 對應 evidence-layers 第二項。16 句均沒有偷換既有數字。原生 timeline 將 `reveal: 1` 解讀為每句前增加一項，並非每句都揭示第一項；依此讀法沒有發現文字先揭示未介紹項目的問題。這只核靜態文本與揭示順序，實際旁白起點與播放器仍待媒體生成後檢查。

## 來源讀取狀態與限制

以下為本代理本日實讀，非直接抄第一輪狀態。主要直接 GET 重開時間為 2026-10-11 23:58:58–23:59:07 UTC，即台灣 2026-10-12；其後在同一查核時段補讀 NASA EO、NIST、Longo、傷亡研究。此輪只作兩次額外搜尋（c21 專用），其餘均開已知 URL。

| source | HTTP／可讀內容 | 限制 |
| --- | --- | --- |
| [N23] NASA 2023 | 本輪 GET 200，正文 | 倒樹、庫利克、微粒與小行星傾向；不是原始考察日記。 |
| [N19] NASA Ames 2019 | 本輪 GET 200，正文 | 此頁介紹的研究模型，不把所有歷史估值視為同一模型。 |
| [S07] Sandia 2007 | 本輪 GET 200，正文與 Movie 2 說明 | 機制示意，非本片重跑計算。 |
| [APS] APS 2018 | 本輪 GET 200，正文 | 老樹樁故事為此學會歷史專欄；原日記未讀。 |
| [B25] Boslough／Bruno 2025 | 本輪 PMC GET 200，全文 | 1933、1934 原件未重開；稿件歸屬為評論的引用鏈追查。 |
| [C17] Rogozin 等 2017 | 本輪 web 原刊摘要可讀；本輪未另 GET | 付費全文未讀，不擴大摘要支持範圍。 |
| [C23] Gasperini 等 2023 | 本輪直接 GET 200 為 Client Challenge；web 公開全文可讀 | 正文含定年、泥芯層次、地層與結論。本報告不把 challenge 計入正文成功。 |
| [A24] Carbognani 等作者稿 | 本輪 GET 200，摘要及書目 | 沒有假稱已讀 Icarus 付費全文。 |
| [I24] Icarus 正式卷期／摘要 | 本代理當日 web 原刊書目、摘要可讀 | 2024-01-15 卷408，DOI內2023；未讀付費全文。 |
| [JPL13] JPL 2013 | 本輪 GET 403；web 正文可讀 | 明示兩種路徑不同；不把403改記200。 |
| [EO25] NASA EO | 本輪 web 正文可讀；素材任務同日已讀原頁 | 地景圖是 2024-07-06，頁面故事是2025-06-30；不可混日期。 |
| [L07] Longo 2007 | 本輪 HEAD 200 application/pdf；讀當日已下載原 PDF 對應文字段落 | 原 PDF SHA `77f2285ca2deeaf774f1ad3708f6f554d61a0b2d2fb8e45322d7638bb1473ce8`，未冒称本輪重新 GET 或逐頁讀完28頁。 |
| [NIST] mile 換算 | 本輪 GET 200，正文 | 精確1.609344 km，卡片約1.61。 |
| [J19] Jenniskens 等 2019 | web 原刊搜尋完整回傳摘要、導言與結論文字；再次 open／指定 UA GET 為403 | 只聲稱讀到原刊索引內容；未讀付費全文。SciX再次開啟為驗證頁／GET202空內容，不作成功證據。 |
| [J18] 同作者2018會議摘要 | 本輪 web 公開1頁PDF全文 | 原研究者摘要直接說記錄晚採集、二手轉述及位置僅約略；不把此版所有數字導入旁白。 |
| [NP] 剪報檔頁及原件 | 本代理素材任務同日已開檔頁、下載原始位元組並 view_image | PD-scan／PD-RusEmpire；只展示當時報導存在。 |

## 素材、包裝、意見與聽眾检查

- 兩張 photo 的本日素材查核與 `_audit/assets-receipt.json` 對得上：剪報 SHA `4021615ee82ef55923ceb551b05d1a1e3cfb4cba3859a13cb1383adb7dd12792`；Landsat SHA `d99767162754c9cafc1cea2049ba95b613ac8d4df210cd6392fc7fcda170a68b`。本代理先前已逐一 view_image 原件。前者 PD-scan／PD-RusEmpire；後者 NASA EO 製圖與 USGS Landsat，PD-USGov-NASA／PD-USGov-USGS。不是因為頁面在 NASA 就把所有照片當公有領域。
- 衛星原圖實際沒有爆心與軌跡標籤，稿件沒有聲稱有；caption 明示 2024-07-06。1929 倒樹照片沒有使用。照片授權完成不等於82張尚未生成插圖已驗收。
- 標題、縮圖與說明維持「森林倒了，坑在哪裡」的提問及空爆主線；說明明示情境重建、模型估計、切科湖與碎片未定。未引入額外數字、確切死傷數或解案承諾。
- c28 的編輯判讀及其他提問與 brief 站主觀點相符；沒有發現來源與 brief 衝突，也沒有需要站主重新決定立場的事項。
- 139 句程序檢查：超過40字0句、拉丁字母0句、括號／URL／「經查證」「根據官方文件」「本影片」0句。無 say 覆寫，無未核對直引。人地名仍要在實際音訊檢查。
- 本輪原生 lint：`node tools/video/cli.mjs lint --slug curio-h03`，exit 0，0 errors／3 warnings（face、writing、daylight 提示詞重複率，主要包含否定限制）。139句、2442 spoken units、估11.8分鐘。這是估算，不能充作 TTS 時長或8分鐘正文實測。

## 結論與後續邊界

本輪事實改稿0項、未解決0項；不需要因本輪結果再啟動第三輪。第一輪實質三組修正及全部相關文本已回讀，固定抽樣亦完成。後續如果改動數字、成因、來源所支持的範圍或旁白意義，應針對差異重核，不把本報告綁到未讀的新稿。

仍可能隨新研究改變的部分是天體成分、精確能量、碎片歸屬及切科湖；本次核對至2026-10-12可取得內容，並未聲稱系統性讀遍所有2026研究。老樹樁、1933引用鏈、付費全文與原始俄文訪談的讀取限制如上。這份文字查核不代表付費生成、配音、畫面、字幕、全片播放、站主審核或上架通過。

## 最後來源 metadata 追加回讀

主代理在2026-10-12 00:04:06 UTC追加 [J19] 至 video.sources，並在 claims.c21 加上同一 DOI；來源標題為 `Tunguska eyewitness accounts, injuries, and casualties (Icarus 2019)`，checked_on 為2026-10-12。本代理重新讀到該標題、URL、日期及 c21，與上文實讀內容相符。這次沒有改動任何旁白、分鏡、數字、表演或揭示順序。

本代理不只採信 `_audit/casualties-source-revision.json`：另從最終 video 刪去最後一筆來源，在記憶體還原相同 JSON 格式，得到原版 SHA `40b1d0d2de9d11f20b5182634be46bdadeb5f753004be0c3377d8d989cfe36c0`；從最終 claims 移去新增 DOI 文字，同樣還原原版 SHA `2706ab3877f712a916920d22dcb4ffafe2e84826cd7807295a411dd7c088f4a6`。去除所有 sources 的 JSON SHA 為 `e90edb1920e9a7a6302eecbf250905183851521350bfb25ff9e14ff312e043c0`，與修訂收據相同。以上僅作記憶體讀取及比對，沒有寫回稿件。

最終 video SHA 為 `08b8fc80c9b9720ee30cf1ccf73f8f0d540a03e8b3ec6ef77166dde43237dca2`，claims SHA 為 `8872f4f0db0ddad05367b8c8c8597ece64c83f556983fd620dbbbd301a9e39dc`。已對最終版本再跑原生 lint，仍為 exit 0、0 errors／3 warnings、139句／2442 spoken units／估11.8分鐘。因此本報告通過判定適用此最終版；新增僅為來源補強，本輪事實改稿仍為0項。J19 的直接403、原刊搜尋摘要可讀、付費全文未讀的限制保留，不因列入 sources 就宣稱 HTTP 或全文驗證成功。

[N23]: https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/
[N19]: https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/
[S07]: https://newsreleases.sandia.gov/releases/2007/asteroid.html
[APS]: https://www.aps.org/apsnews/2018/06/tunguska-event
[B25]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12015480/
[C17]: https://link.springer.com/article/10.1134/S1028334X17100269
[C23]: https://link.springer.com/article/10.1134/S1028334X23601359
[A24]: https://arxiv.org/abs/2302.13620
[I24]: https://doi.org/10.1016/j.icarus.2023.115845
[JPL13]: https://www.jpl.nasa.gov/news/additional-details-on-the-large-feb-15-fireball-over-russia/
[EO25]: https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/
[L07]: https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf
[NIST]: https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8
[J19]: https://doi.org/10.1016/j.icarus.2019.01.001
[J18]: https://www.hou.usra.edu/meetings/metsoc2018/pdf/6234.pdf
[NP]: https://commons.wikimedia.org/wiki/File:1908-07-29-SibirskayaZshizn-135.jpg
