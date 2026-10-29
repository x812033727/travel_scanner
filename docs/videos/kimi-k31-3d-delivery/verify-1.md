# 全文事實查核1：REVISE

查核日：2026-10-26 UTC。這是全文事實與證據對照，不是盲聽、敘事答案、音檢、QA、核准或整片完成宣告。

**身分／獨立性**：查核人未撰寫本片114句稿，與source作者分開；但曾供應本題官方研究，並撰寫原始兩個STL教具及有限檢查器。因此不是官方研究／教具方法的全新盲態獨立研究者。本輪重讀完整source、114句口播、畫面字卡、claims、brief、task／progress、實際檔案與不同作者的獨立幾何proof，並實跑公開兩條檢查命令；沒有冒稱自己產生第三方獨立幾何結果。

## 精確版本

| 已讀文件 | SHA-256 |
|---|---|
| `video.json` | `0223dc6d45d9e22b4f772a627ac76dba5bf80fc298a081e0422cca14b4d8198a` |
| `script.md` | `44c1f965e164a7875f64e7e2dbd9514c63d60579a39844fdb7a0e83a06efa8b9` |
| `claims.md` | `5f599d3d55c0e8e56e8a49170aa39d60d0875bda73fc95121cf483f44e8b9290` |
| `brief.md` | `1ebb7aaa2cd7809f0228de108dd8932b0df48396d546fb88fdab2b466f3d167b` |

上述source為42景、6章、114個唯一ID。全部114筆ID／text與script對應，未發現句子遺漏或順序差異。原始版本副本與逐檔初始hash在研究scratch `new-popular-topic-20261026/factreview-1/initial-*`；本輪結束前確認上述三個source文件仍未漂移。**新增素材引用或文字改動後須另核對新hash，本報告不自動適用新版本。**

## 必須修正的三處

| 編號／位置 | 發現 | 建議最小修正；由source作者處理 |
|---|---|---|
| R1 `download-moment / 2sc4` | 開場先說Kimi推出新版本，第二句立即指向「這枚墊圈」；口播直到`fv1i`才說教學模型，較後才明確說不是Kimi輸出。第一張subtitle已標教具，但M4A／純聽眾拿不到字卡，仍可能把目前墊圈誤認為Kimi生成證據。 | 在前兩句口播內說清「自製／原創墊圈教具」。例如第二句加入「這枚自製的墊圈教具」。保留後面反例及未親測聲明。不要只依賴新PNG上的文字。 |
| R2 `download-moment / 2g58`，含對應`say` | 「十月二十四日，Kimi推出……」未在口播標時區。證據是論壇UTC10/23，換算台北才是10/24；後面字卡雖有台北，開場純音仍將地方日期說成無條件的發表日。 | 明講「台北時間十月二十四日」，同步更新say／say_for與script；不改UTC原始時間、不拿blog修改日當首發。 |
| R3 `ring-read-triangles / a2bm` | 「輸出的**每一個判斷，都來自這個檔案的座標與三角形**」過度概括。實際`check.py`的`explicit_unit_declaration`來自外部spec，尺寸與體積條件也把mesh數值和spec相比，並非全從STL自身取得。 | 改為明示比較關係，例如「檢查器把檔案的座標與三角形，對照同一份外部規格。」不改演算法或把單位說成存在STL內。 |

三處都是交付語意／事實限定的修正，與目前數字結果是否正確分開。其餘全文未發現需推翻的官方數字或示範數值；仍不能因此先標全文PASS。

## 全部主張與實檔對照

| 主張 | 本輪判斷 | 實際核對與限定 |
|---|---|---|
| c01 日期 | REVISE／R2 | 官方JSON首帖`2026-10-23T20:12:59.921Z`＝台北2026-10-24 04:12:59.921。Blog只有`dateModified=2026-10-24`，未當成首發。 |
| c02 3D功能 | PASS，保留官方主張身分／R1開場修正 | 正式blog列文字／參考圖、3D Make線上預覽編輯及下載用途。稿中沒有假稱已登入試用或展示Kimi實際輸出；前兩句仍需提早說教具。 |
| c03 權重 | PASS | 完整權重是2026-11-04前的未來承諾；稿保留「承諾」，沒有說已取得權重／授權或自架成功。雲端資產下載與權重分清。 |
| c04 BenchCAD | PASS，有條件的官方自報 | 92.7為with-tools Voxel IoU；open模型組1,000／17,900隨機子集、max effort、Claude Code harness保留。沒有改成列印成功率／全面排名／本片重跑。Quickstart佔位未被用來填數字。 |
| c05 匯出副檔名 | PASS | 「本次已讀官方頁未指定STL」和「本片未親測」保留；沒有從缺字推論功能不存在，也沒有虛構操作按鈕。 |
| d01 教具來源 | REVISE開場／R1，其餘PASS | 原創確定性有孔墊圈及刻意填孔反例，名義40／16／5mm；實檔／說明均非Kimi產物。填孔反例實際是同外部尺寸的實心圓柱，不冒稱真模型失誤。 |
| d02 外部範圍 | PASS | 兩份均X[-20,20]、Y[-20,20]、Z[0,5]；尺寸40×40×5。限定外框，沒有將中央材料或所有角度的多邊形寬度混成同一概念。 |
| d03 封閉與孔 | PASS，特定兩實檔 | 獨立proof確認每邊2面、邊方向、vertex-link、連通性；ring genus1、filled genus0。只是這兩份網格，未擴成任意封閉網格都能製造。 |
| d04 STL／單位 | PASS；R3需修整體判斷來源 | 實際ASCII檔為頂點與法向。當日正常公開GET的Autodesk明列unitless triangulated surface，LOC補足ASCII結構／三角表面；mm由外部規格宣告。沒有說所有3D格式都無單位。 |
| d05 面數／體積 | PASS | 實跑ring512面、5269.401464119024；filled256面、6273.096981094106。獨立體積只差浮點末位。畫面三位小數正確，未把面數當品質分數。 |
| d06 命令／33射線 | PASS | 本輪從實際demo cwd執行兩條`python3 check.py --stl … --spec spec.json`，均真exit0；ring受阻0、有限accepted=true；filled受阻33、孔／體積failed且accepted=false。exit0沒有被洗成幾何通過。 |
| d07 限制 | PASS | 指定軸向、有限取樣／尺寸／邊／體積，未保證任意孔、自交、最小壁厚、材料、切片、承重或實際列印。全文否定與限制保持一致。 |
| d08 獨立剖面 | PASS／一致性查核 | 不同作者proof在Z0.5、1.25、2.5、3.75、4.5均得ring兩圈中心空、filled一圈中心有材料；不同射線spotpeer支持。這不是本查核人本輪新獨立實驗或看圖猜測。 |
| d09 最小淨空 | PASS／本實檔限定 | 獨立剖面量得中心淨空直徑15.98072729845233；六位顯示、口播約15.98與差小於0.02都成立。64段近似圓不被寫成精確圓孔。 |
| d10 新用途 | PASS／推論分清 | 對新增「最小淨空≥16mm」條件，15.980727<16所以不滿足。原checker沒有此gate；稿沒有假稱改完spec重跑或實際拿棒子／列印件試配。 |
| d11 交付建議 | PASS／編輯判斷 | 檔案＋同版spec＋結果及需要時的可編輯來源，標為建議。STL三角表面不自動保存建模參數歷史；不冒充Kimi產品保證。 |

已讀原獨立proof SHA `3faf79eddb4716de8959081afcf036624eab52db980af23c465af0e0f2b8d0a3`、freeze `7d53e4fc84c49113451a4e76f72cf516dc07a8ed61c58d0c3daf0d23163d17e6`及射線spotpeer `610ec89f0891ebfdbe8d46915c8b22392f8d80e2318159714a093cc49162ee55`。原檔、短alias、規格與checker全部逐bytes／SHA對上provenance；`check.py` SHA `f930e4c88b2f147a28d5304cb4a4691e42b2df8e8388c8b23327ce678e9f2be7`。

## 指令、來源與素材狀態

本輪真正重跑命令：

```sh
cd docs/videos/kimi-k31-3d-delivery/demo
python3 check.py --stl ring.stl --spec spec.json
python3 check.py --stl filled.stl --spec spec.json
```

stdout SHA分別 `7acd4c1f2f9ee051d7f0ac1b8972668db0849e5c67186c3a60ec7cb1d8a99a6f`、`d1d6e50c9363369487e47225f5ec533a8f8305698f91541bb4f23e5f81af8b6d`，stderr皆0；原結果與demo作者收據一致。只執行讀取式幾何CLI，沒有`--make-fixtures`、原生影片關卡、TTS、ASR或付費請求。記錄與詳細結果僅存自己的factreview-1 scratch。

已重讀本題八官方來源的當日查核快照／URL與hash記錄（`kimi-official-audit.sources.json` SHA `4e83f75ee6c61639597a8370b578f5a9c82fce1161dece1a6475359f8811ca73`），官方blog／論壇／model docs的本題相關內容與先前公開讀取一致。API價格／cache附錄不是本稿口播主線，未把API與Code方案混入3D模型成效。新補正常公開GET：

- [Autodesk STL匯出](https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/SLD-3D-PRINT.htm)：HTTP200，SHA `95ee3b68abac050b3025593a199556e83a55fda12c0dc1a876613ba25017c6af`。
- [LOC ASCII STL](https://www.loc.gov/preservation/digital/formats/fdd/fdd000506.shtml)：HTTP200，SHA `c2767fc6c313632b51b449eadabe37459167edfa73548efa3d5a68a3a8d1ef7d`。
- [LOC STL家族](https://www.loc.gov/preservation/digital/formats/fdd/fdd000504.shtml)：HTTP200，SHA `b91a832dadfe444799c135deb2bf9ee9205389d404a7f93e98fd41d6241f4d0a`。

四張目前已引用PNG的實際SHA均對上source assets。新中性開場圖`00-neutral-side-intro.png`已存在，收據聲明教具身分與結果未展開，但本source版本還未引用它；**本查核未以收據代替實際看圖，視覺驗收由root另做**。其將來引用不會取消R1的純音歧義。

非口播交接缺項：brief指向`reference-study.md`，目前該episode內尚無此檔；詳細研究在scratch `youtube-research.md/.json`。請正式交接時補入真實研究或修正相對路徑；不要先宣稱該文件已存在。幾何示範與公開命令的檔案目前均存在。

## 門檻與完成狀態

三個頻道各20萬、七日內的新聞群門檻仍未證明；brief／progress明示ROOT依站主委派採推薦題，不是假PASS。本查核沒有將採題授權改成已過流量門檻。僅有題目卡不代表成片或八語媒體交付；本輪沒有接觸auth、後台、審核、merge、部署或YouTube。

請修R1–R3並同步script／相關say後交回精確新source hash。即使只新增視覺引用，也需報新hash及差異。本報告保留原版REVISE紀錄，不直接改成PASS或替新版本核准。
