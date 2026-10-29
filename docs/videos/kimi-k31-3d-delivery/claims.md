# Kimi K3.1 Pro 3D交付｜逐項主張

錄製／查核日期：2026-10-26（Asia/Taipei）。本表是草稿事實對照，尚非換人查核或模型／列印驗證。官方事實、原創可重現示範、編輯判斷分列。所有實檔示範都發生於本地編輯教具；沒有Kimi模型呼叫。

## 官方事實

| ID | 主張與母體／限定 | 官方來源與確認日期 | 對應場景 |
|---|---|---|---|
| c01 | 官方論壇首帖2026-10-23T20:12:59.921Z，換算台北10/24 04:12:59.921；新聞為Kimi K3.1 Pro與3D能力。本片錄製10/26。Blog dateModified不能充當首發日期。 | [官方論壇JSON](https://forum.moonshot.ai/t/kimi-k3-1-pro-has-launched-start-exploring-now/629.json)，2026-10-26；`kimi-official-audit.sources.json::release_dates` | download-moment、news-reaches-desk |
| c02 | 官方將3D Make描述為可在線預覽、編輯、下載三維資產並供列印／分享用途。是官方功能主張；本片未用帳號實測其產物、品質、可用性或匯出。 | [Kimi技術文章](https://www.kimi.com/en/blog/kimi-k3-1-pro)，2026-10-26 | news-reaches-desk、download-is-not-weights、export-not-assumed |
| c03 | 完整模型權重承諾2026-11-04前釋出。這是未來承諾；未驗新權重、授權或自行部署。資產下載與權重下載不是同一項交付。 | 同上，2026-10-26 | download-is-not-weights |
| c04 | BenchCAD的92.7為供應商with-tools VoxelIoU；衡量從多視角圖重建形狀的重疊。官方open-model組隨機1000／17900檔案子集、max effort／Claude Code harness。不是92.7%列印成功率、不是獨立重跑，也不是全題／全用途模型排名。 | 同上BenchCAD圖與註腳，2026-10-26；ROOT固定brief保留完整母體與harness | one-benchmark、overlap-is-not-hole、source-and-model-separated |
| c05 | 本次已讀官方頁僅說可下載列印資產，沒有指定STL匯出；本片未親測帳號、按鈕、匯出副檔名或權限。不從「未寫STL」推定功能不存在。 | 同上；[Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart)，2026-10-26。Quickstart有xx.x/xxx未填段落，不取其作數據。 | export-not-assumed |

## 原創實檔與幾何結果

原始研究檔案在 `/workspace/work/ai-tech-next/new-popular-topic-20261026/`；正式同源副本已由唯一demo作者建立於本片demo/；其中ring.stl、filled.stl、spec.json逐bytes相同。下載網址與後台附件仍待正常交付，不宣稱已上傳。

| ID | 實際觀察／推論界線 | 可重跑證據 | 場景 |
|---|---|---|---|
| d01 | 同一教學墊圈外徑40、名義孔徑16、厚5，外部規格宣告mm。兩個確定性ASCII STL皆編輯製作；填孔反例刻意設計，絕非Kimi輸出或模型失敗樣本。 | `kimi-official-audit.geometry-spec.json` SHA9bfbca42e2b99b065d3c74bf20181cb3a795d4f4acb2d2adbd5247e94eaf3ac8；原始ring SHA58efbfb030273dafb948da5c57596244f8099736401644e19149db5535c372c5／95879B；filled SHAf5f6278b84bd07b5a5e7b31980b5ce4b2fc13227758da7de694127e5de90c22a／44805B。 | 開場、spec-arrives、spec-not-prompt、editorial-counterexample |
| d02 | 兩實檔bounding box各為X[-20,20]、Y[-20,20]、Z[0,5]，所以三軸外部範圍40×40×5相同；此項不讀中央內部材料。並非宣稱多邊形所有角度的外徑都精準40。 | 作者`geometry-results.json`；獨立`independent-geometry-result.json`同原始mesh重算。 | three-unresolved、outer-size-question、outer-bounds-pass |
| d03 | 兩實檔都是封閉連通有向網格：boundary edges0、每邊2相鄰面、vertex-link通過。墊圈可有內壁且材料表面仍封閉；封閉不保證需求的指定通孔。不是以任意一個edge-only測試證明所有3D網格可製造。 | 獨立結果`topology`：ring256vertices／768edges／512triangles／genus1；filled130／384／256／genus0。 | closed-mesh-check、hole-has-walls |
| d04 | 這兩份ASCII STL由三角形頂點與法向組成，未嵌單位標籤；本次mm來自外部規格。匯入單位需對照外部需求。 | 原始ASCII檔與規格；未主張STL只支援ASCII或所有3D格式都無單位。通用格式有ROOT當日實讀的主要來源：[Autodesk Fusion STL匯出](https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/SLD-3D-PRINT.htm)明列unitless triangulated surface；[LOC ASCII STL](https://www.loc.gov/preservation/digital/formats/fdd/fdd000506.shtml)說明頂點與法向。 | spec-not-prompt、unit-is-outside、same-files-opened |
| d05 | ring512三角形、signed volume5269.401464119024mm³；filled256、6273.096981094106mm³。畫面保留三位小數，口播約5269與6273；面數不當品質分數。 | 作者geometry-results，獨立體積分別5269.401464119025／6273.096981094107。 | triangles-not-meaning、volume-crosscheck |
| d06 | 同一spec／同一檢查器對要求的Z軸孔內33條取樣線：ring受阻0、filled受阻33；作者有限檢查的孔與1%體積條件使filled不合。33為有限取樣，不證明任意曲孔或每個位置。 | 原始checker `kimi-official-audit.geometry.py` 的兩條完整CLI；`geometry-results.json`保存結果。 | axis-not-anywhere、run-package、run-ring-command、run-filled-command、rays-cross-center、ray-results、volume-crosscheck |
| d07 | 有限檢查不涵蓋任意孔、自交、每處最小壁厚、材料、切片、承重、實際列印；通過不能稱製造認證或安全保證。 | 作者limits與獨立proof limitations。未執行列印／切片。 | limits-with-purpose、washer-decision |
| d08 | 獨立程式直接剖切相同mesh，在Z0.5／1.25／2.5／3.75／4.5各高度，ring兩封閉輪廓、中心非材料；filled一輪廓、中心為材料。另獨立射線spotpeer佐證。不是人工看圖推定。 | 獨立proof SHA3faf79eddb4716de8959081afcf036624eab52db980af23c465af0e0f2b8d0a3；`independent-second-spotpeer-receipt.json`。 | section-reveals |
| d09 | 64段直邊近似名義圓。名義孔頂點直徑16；獨立剖面邊界最小淨空直徑15.98072729845233。字卡15.980727，口播約15.98；不把16名義值當所有方向最小值。 | 獨立proof `smallest_clear_diameter_from_section_edges`，來自實際triangle-plane sections；約等於16cos(π/64)。未用近似公式替代實檔計算。 | polygon-not-circle、clearance-number、tolerance-is-purpose |
| d10 | 若另要求「最小淨空≥16mm」，由實測15.980727<16可直接判此教具不滿足該新增條件。這是同一mesh對更嚴用途的推論，不冒稱原checker已有minimum-clearance gate或改spec後重跑過。允差需依真用途與製程另定。 | d09實際量值＋數值比較；差約0.019273mm。 | new-use-new-spec、tolerance-is-purpose、washer-decision |
| d11 | 編輯建議：交付實際檔、版本相同規格、對應結果；需要修改方式時另要保留該方式的來源。STL三角網格不自動保存當初畫圓的參數或CAD建模歷史。此建議不冒稱Kimi產品保證。修訂另明說本check.py僅讀文字版ASCII STL，不直接讀圖片；其他網格需相符工具，改副檔名不是格式轉換。這是檢查器讀取範圍與格式原理，不宣稱實際轉換或Kimi新增匯出支援。 | 頻道brief站主觀點；實檔內容。[LOC STL家族](https://www.loc.gov/preservation/digital/formats/fdd/fdd000504.shtml)說明triangle-mesh surface，而非CAD參數歷史；與實際ASCII檔一致。 | format-question、handoff-three-files、answer-in-file |

## 核心示範：輸入、動作、預期與實際結果

- 輸入：上述兩份真實STL與同一份JSON規格，原始SHA皆見d01。
- 動作：在教材demo資料夾依序執行下列兩條完整命令。短檔名alias與原始檔逐bytes相同；check.py SHA f930e4c88b2f147a28d5304cb4a4691e42b2df8e8388c8b23327ce678e9f2be7。使用python3，不改演算法。

```bash
python3 check.py --stl ring.stl --spec spec.json
python3 check.py --stl filled.stl --spec spec.json
```

- 預期：有孔教具在作者限定條件通過，刻意填孔的對照在孔與體積條件失敗。這個反例是設計的，不能寫成模型意外失誤。
- 實際：作者有限檢查得到上述差別；獨立parser／完整topology／五平面剖切／不同射線spotpeer也支持孔與填孔差別。外部尺寸與封閉性是簡單做法，兩份實檔都通過，無法替代指定孔檢查。
- 加嚴需求：新用途最小淨空至少16mm，實測不合；這是由實檔新增量得的最小淨空帶來的新判斷，不是檔案換名或重播同一個pass。
- 證據限制：未親測Kimi、未下載新權重、未實際列印；模型benchmark與教具驗收不是同一個母體。

## 與企劃不同的地方

維持briefA、六章、同一墊圈與三個開場未揭結果。口播省略API價格／token／Highspeed延伸，避免改成成本或來源查核片。待真實PNG完成才引用圖檔；目前已綁四張實際viewer PNG（作者20項檢查與本作者逐4檢視、SHA核對），不偽造產品UI。因全頁圖均帶結果，僅在最小淨空揭曉之後使用，避免提前回答開場。官方5秒片頭放第一章後、21秒片尾放正文後，兩者是後續組片設定，不寫進口播充片長。

## 我懷疑但沒動的事

1. 本題尚未證明news-flow「同則新聞三頻道各20萬、七天內」群門檻，ROOT明確保留為推薦題而非門檻PASS。
2. 官方頁未明說STL，留未親測；不教虛構的匯出按鈕。
3. 原checker通過有限孔／體積條件，不能自動保證嚴格最小孔徑，後段以獨立實檔量值指出差別。
4. 新main writer prompt與schema對voice.performance不同步；作者以實際schema允許的voice.style承載表演方向，不添加unknown欄位。全域lexicon未修改，必要讀音用綁當前text hash的say。

## 進度

完整首稿111個ID保留，新增3個用途疑問共114句／42景／6章。三輪自審與所有delta、依賴啟動失敗、1error／8warnings及中間0error／1warning都保存在draft-notes。最後修改後正常原生lint真exit0、0errors／0warnings，估11.844444分鐘；這不是實際語音／成片長度。尚無換人全文查核／盲評、TTS、ASR、字幕、影片、外語媒體或後台成品聲稱。


## 實際製作狀態差異

ROOT已於2026-10-26T11:08:39Z完成該新slug的正常report-only主題資料寫入與讀回（PUT1／GET1；reviews0，非核准）。這是題目卡，不是本片成片／語言媒體交付；本source作者未碰auth或後台。


## R1全文查核與盲讀修訂（保留失敗，不作R2核准）

- 原源稿0223dc6d…與原script／claims／draft-notes／verify均逐bytes保留於研究scratch的source-before-R1-revision；本作者修改前逐一比對相等。
- verify-1.md仍為原版REVISE，三項必修是開場純音教具來源、台北發布時區、a2bm不能說每個判斷只來自STL。R1正式敘事false也保留，未改答案或門檻。
- 修訂2g58首句明說2026-10-26、這台電腦、我打開兩份自製墊圈教具；2sc4很快帶入Kimi問題。新聞首發移於lqfp明說台北時間10/24，相關say／say_for同步。
- 4ran／pfy0／5jr1停在量尺寸、封閉標記、孔剖面結果展開前；不先說兩份尺寸相同、兩份封閉或誰被退回。q0p1把第二章接到收到什麼檔案，資產／權重與11/4未來承諾只作這個下載問題的背景。
- a2bm改為「檢查器把檔案的座標與三角形，對照同一份外部規格」，保留單位與條件來自spec的關係。
- qhwk保留一次孔軸要求，rk1x改講實際兩檔的底面原點；s8d7／lxiq／usyf用明確回呼承接且增加檢查位置、第二條件或交回原始結果的新動作。3w3j／kwmv／cezr改為本檢查器的文字STL輸入限制與工具選擇，不再重講展示可幫人選工作方式。
- 5m5q縮小成「新增最小淨空要求如何寫成一句話」，33ye在交付說明明寫「成品最小淨空至少十六毫米」，edz9／f106明說未實作此欄位且原checker通過不作答。只對理想幾何新增條件作數值比較，未制定實物棒、材料或製程的容差建議。
- 新中性側視圖00-neutral-side-intro.png SHA569b6bd06455d340de64ad07c7bcea90a94ce5b51494f9ac2f63d90f6e5162ff，已實際view＋核hash。開場引用它，只標原創教具與未展開結果；舊四張結果PNG仍在其結果揭曉後，hash未變。
- 當前114句／42景，原114 IDs全保留；正常離線lint真exit0、0errors／0warnings，估12.065556分鐘。此正常lint不是敘事／事實R2通過，也不是實際音檔或成片長度。
- 詳細逐句before/after與完整檔案binding見revision-R1.md；仍待ROOT派全新R2兩盲讀者與事實復核。


## 最新有界編輯修訂2（待R3，非事實PASS延用）

目前source為650298cd725c9dfea16059a1b3bc8f0e28210e5c6204712ca0f258456950ff04。verify-2的PASS只綁舊c068與其文字；原verify-1 REVISE、verify-2、revision-R1及R1/R2原生false全數保留，沒有改答案、清旗、重設次數或宣稱R3已通過。

只改五句與一個事件章名：q0p1改為實際打開教具旁的規格，對照要交付的尺寸與模型資料（d01/d04/d11），不再宣布解說從哪裡開始；zzay先給更嚴最小淨空要求導致退件的新後果，c8hn明確以剛剛量測作因果回呼（d09/d10），條件仍非原checker實作。dra2保留新體積結果並點名回呼原外框（d02/d05）；0gjn改問原檔改版後舊結果能否同行，移至fxx4正前，由下一句既有事實直接回答（d11）。章五改為「兩份實檔送進了同一個檢查器」，沒有新增結果、測試或Kimi操作。

114原ID及所有數字、否定、日期與限定保留。正常離線lint真exit0、0errors／0warnings，估12.081667分鐘；仍不是音檔、成片或敘事R3通過。詳細逐句差異與移動記錄見revision-R2.md。這是初稿之後第2次編輯改寫；下一次實際原生敘事紀錄應是第3輪，由ROOT按正常流程執行，本作者未執行或修改counter。


## ROOT三句讀稿校正後的版本

目前source 9686969c66cfd9329c28e0f75d62c22830930b609479560d896e3e087829958b。前文650298與verify-3是先前版本歷史綁定，保留原文。此次只把改孔問題收窄到下一句實際回答的來源檔選擇，並標明兩處回呼；沒有新增事實、數字或模型測試。新版本尚待獨立delta／全文一致性核對及真實讀稿驗收，不把舊PASS自動套上。
