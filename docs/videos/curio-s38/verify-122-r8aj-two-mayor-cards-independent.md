# S38 R8aj PF028／PF029 終局字卡獨立來源覆核

2026-10-22 UTC。審者 `/root/s38_pf021_last_paper`，未撰寫此次兩張字卡或claims附註；曾是R8ag剩餘88prompt的作者，故對剩餘79景只做**機械沿用性確認**，不冒稱重新獨立審核自己的提示詞。兩張字卡的來源、中文譯文與改動範圍結論：**PAPER PASS**。沒有媒體、creative檔案修改、manifest重綁或Git提交。

| 精確現稿 | SHA-256 |
| --- | --- |
| `video.json` | **`8d4b427f8587ef20fb5a12bf983444766ad68bb527ce4b9acd767ae3df87a172`** |
| `script.md` | `52a65118f58dae3378006d68524a07b41ecd0763e66ac5c931d2798f5560913e` |
| `claims.md` | `154e17297a27a6589868908efaab6a0cdef905fd802fb4cc79120aa4d6e7966f` |
| `verify-121-r8aj-two-mayor-cards-author-diff.json` | `d0ac1c2fa2df28020487953d285beb34db1bb81519e1463f14b2c7ebaff3db3e` |

## 來源與中文卡片

重開固定Pepys日記1666年9月2日L65860–65866，全文SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。L65863為 `I am spent: people will not obey me. I have been pulling down`，L65864接 `houses; but the fire overtakes us faster than we can do it.`。這是佩皮斯記錄市長對自己的回話，不能作錄音、逐字現場筆錄或存世手稿外觀的證明。

- **PF028「我已精疲力竭」：PASS。** 對應 `I am spent`，只呈現疲憊，不再在相鄰卡重複「人不聽命令」。與本句旁白的疲倦市長及其問句相符。
- **PF029「人不聽命令，火又追得太快」：PASS。** 是同一回話中不被服從與拆屋趕不上火的**濃縮中文譯意**。雖省去句間「我一直在拆屋」的細節，仍保留原有抱怨，不增加群眾動機、全城結果或新因果。claims附註列出兩段英文對應；本句旁白原本已明確把兩項抱怨歸於日記記下的市長回話。它不應被宣傳成逐字逐句完整譯文。

兩卡皆標 `佩皮斯日記・中文譯文` 與 `市長對佩皮斯說・1666．09．02`，說話人、轉述層次與日期清楚；不畫假手稿字形。PF028疲憊與PF029抱怨分開，沒有增加一段重複的視覺引句。PF029三張實際原生圖已耗盡且第三張因黑邊FAIL；改卡不授權第四張。

## 精確差分、口播與沿用性

我逐項確認verify121的old／new完整場景物件與稿件相同；把兩個new完整場景反填old、以原有JSON格式序列化，逐位元組復原verify120所審video SHA `2b435f0ee955ffa798f3c44e01c504e47e5fae1eb7d4bbfcdc2a0c4aa904bc6b`。PF028只縮短卡片文字，PF029由shot改big；其他JSON值未變。

全片112個 `(line.id,line.text)` 與Git HEAD `f2bc35e8f`逐項相同；script的112行旁白也與HEAD逐字相等，並逐句等於video.json。script新SHA源於官方工具補PF029的`（big）`標示及刷新雜湊頁腳，並非口播、讀音或句子次序改稿。先前七張big標示已在verify118證明只是重新產稿後補齊。

**PF033–PF111共79個完整場景物件與Git HEAD逐欄相同**；其79個prompt亦逐字等於verify115的最終after值，接續協調者verify116的獨立來源／畫面覆核及既有verify110來源鏈。本票對這79景只證明沒有新增差異。PF031最後原圖由協調者按verify120及實圖KEEP，入選圖不因鄰卡修改而重買。正式lint exit0，**0 errors／0 warnings**；正文仍102shot／111非outro景（91.9%），最長連卡3，新增相鄰PF028／029兩卡未破系列門檻。

## 私人守衛快照與剩餘整集範圍

只讀active manifest SHA `3c8ed03d023163fabbf561ca25789661a1b920d0a5bba78c78db52f87c9423d3`，**23張KEEP**，每張所選實檔SHA符合條目、judge PASS且無needs_review；PF029退件不在active入選。STOP在位、jobs空。Ledger SHA `5519662cbcfa4b0d7b412d8bb46219b6d53fdf8086de2f89214dbe886425ea35`：US$1.1600／80image／80judge／1music，舊US$0.0035 reservation保留，PF029三張ready原生image紀錄均在。

若即時價目仍為每試image US$0.0035＋judge US$0.01，剩餘79景各最多三試為US$3.1995；加現有實付及reservation上界為 **US$4.3630 < US$4.58**。本票支持協調者在STOP下保留23個KEEP完整條目／實檔，隔離所有失效shot條目並安全重綁現稿visual hash，再核live模型、餘額、dry-run、request key／judge stamp及整集上限後，續做**PF033–PF111一次有界的整集最多三試流程**。PF028／029與更早耗盡來源卡不重開；已選23張只吃快取、不新購；原圖與入選圖仍在產後按judge、材料性來源矛盾及畫風驗收。紙審不自行移除STOP，也不是整集成片完成。
