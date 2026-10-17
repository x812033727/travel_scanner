# A01 round10 候選：獨立唯讀事實、敘事與畫面審查

Reviewer：codex-a01-repair-editor；日期：2026-10-16。審查者未撰寫本次兩句＋claim 候選。

**總判定：HOLD，不能直接進入媒體製作。** 兩句的史實範圍有來源支持，局部銜接確有改善；四處聲畫錯位仍在現有 prompt，尚未修復。用途演進主線可以跟上，但這不等於已解決正式 `one_thread` 對「同一具體主角」的規則張力。round9 的三項真實 FAIL 全部保留。

本報告的 PASS 只表示下列限定項目經人工讀稿／來源核對成立。不是 worker checker、listener、narrative、script-review、pilot 或媒體 PASS，也不授權安裝、生成、上傳或發布。

## 1. 審查來源與實際執行

- Repo HEAD：`c0cce5e523c4f5d2f47d8deed5e1c7a45ee93afe`。
- 套件：`docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round10-candidate/`。
- 候選 manifest SHA256：`839ea9093b259450c7fd3469d78eb404206e77a524d16bd8323e21227c427ee1`。
- 比對快照：`actual-20261016-035053`，archive SHA256 `b988ed8af18e650985f85d6085d243c71032b0885172405645a40c86dc1a341a`。
- 本次重算並確認 frozen 六章、series、narrative 與該 actual 的對應檔逐 bytes 相同。未重新重演 80 筆 audit；完整重演結論讀自既有 `script-review-20261016/round9-diagnosis.md`，不冒稱本次又跑過。
- 本次完整讀六章、series、round9 原 FAIL／診斷、兩句與 claim 差異、四處問題 prompt，以及 `turn-15 → now-01 → now-02b → now-03`。
- 審過只讀 `verify.mjs` 後實跑，exit 0：29 檔、25 JSON、六章、exact reverse；官方 compose/lint **0 errors、37 warnings**，cute 0 errors；63 鏡、92 句、520.333 秒估算。沒有 TTS 或成片計時。
- 獨立 structural diff 只有三欄：`origin/scenes/0/lines/0/text`、`now/scenes/0/lines/0/text`、`now/claims/0/claim`。92 個 line IDs／順序不變；其他四章逐 bytes 不變；所有 prompt、camera、loops 不變。
- 來源與候選 pins、實際三欄前後值、來源快取、執行摘要另存 [evidence.json](evidence.json)。目前公開版僅遮蔽本機絕對路徑，SHA256 `f4adbdc98897b4f438b5897859101e8f7f7658d99d5b26077cbf8fe89e701018`；審查時原位元組 SHA256 `ed24f1fad05ed561a9758491e5eab2a3bcef22b4ccf9cef0caf6ad57342136f5` 仍在先前 Git 提交。

round9 narrative 原檔 SHA256：`dd458ee2b6eee90a3b358408c605620c108ca4387afb94249fd555abc01babab`；`round=9`、`passed=false`、failed=`chapters_link,payoffs,one_thread`。本次沒有改寫這些值。

## 2. 一手來源核對及邊界

| 來源 | 本次讀取證據 | 可支持／不可擴張的範圍 |
| --- | --- | --- |
| [Winnetka Historical Society：Anita 的輪子箱](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/) | 官方索引全文實讀；直接 open 兩次失敗，沒有把它記成新 HTTP 200。另完整讀 actual 頁面快取 `98a451f4018ca9a9.json`，該歷史紀錄為 200/readable、read_at `2026-10-15T07:39:02.967Z`，hash 見 evidence。 | 該館保管箱子，記事明列第二次旅程 1928–1930、兒子製作、舊嬰兒車輪與木柄、家人自行使用。因此支持「1928 出發」「兒子做」「一家人的自製品」。不證明 1928 才製作，也不證明當時全世界沒有商售輪子箱。文章關於後世專利優先性的簡化說法，不採為本次結論。 |
| [Travelpro：Our History](https://travelpro.com/pages/our-history) | 本次官方頁成功讀取，The Origin, 1987 段。 | 支持 Plath 的直立兩輪、伸縮柄拉行這個前段用途。沒有證明他傳授技術給 Samsonite；候選也沒有這樣說。 |
| [Samsonite 2011 招股書](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf) | 本次官方 PDF 抽文成功，印刷頁 72（PDF index 80）年份表；印刷頁 40（index 48）Spinners 定義。另嘗試 screenshot 失敗，未宣稱 PDF 像素驗收。 | 1997 用字為 `presented`，平衡四輪直立箱可推／拉；2000 列出四輪 Spinners，詞彙表說明其直立多向移動。因此「發表」準確，兩個年份的機制須分清。沒有以這份紀錄證明 1997 零售店已上架、全球第一或與 Travelpro 的技術承繼。 |

## 3. 文字與敘事逐項判定

| 項目 | 判定 | 精確 ID／理由 |
| --- | --- | --- |
| 1928 日期、母子與自製箱 | **PASS（限定史實）** | `origin-01 / zc7k` 新句：「1928 年，母親拉著兒子做的箱子出發；輪子有了，這卻還是一家人的自製品。」日期修飾出發；自製限定眼前這只家用箱，來源足夠。不能在後續改成「還沒有人販售」或「只有這一家有」。 |
| 開場問題接正文起點 | **PASS（局部改善）** | `x7r4 → zc7k → 6b28`：開場問會滾之後還缺什麼，新句直接放出「會滾／仍是自製」的差距，再介紹一家六口。比舊句「開場那一家人，其實早就…」更快進入主問題。沒有虛構 Burnham 家庭造成 Sadow 創業。 |
| 1997 用語與 n1 同步 | **PASS（限定史實）** | `now-01 / 7asx`：「從往後拉，到站著推，1997 年 Samsonite 發表了平衡四輪直立箱。」`n1` 同改為「發表」，`source=11/fact=9` 未動。比「推出」更精確對應官方年份表的發表動作，不把發表偷換成上架。 |
| 章際用途承接 | **PASS（局部改善）** | `turn-15 / arxr,4e5m → now-01 / 7asx,kfiw`：問題是直立之後四輪是否仍有位置；新章首先講拉→推，再點品牌年份，確比「有。1997…」更容易沿使用方式理解。 |
| 兩步回答是否混年 | **PASS（文字）** | `4e5m` 同時問站著推及轉向；1997 的 `7asx/kfiw` 回答直立推拉，`now-02b / 5tik` 明點 2000，`now-03 / fmd7` 才說多向／側移。答案跨相鄰兩步完成，沒有明說 1997 已有萬向側移。`同一家公司` 指相鄰已點名 Samsonite，指涉清楚。 |
| 顧客問句是否沒有答案 | **PASS（人工確認答案存在）** | `idea-10 / eghq → ys5y → quhs`：問買不買帳，下一句用 Sadow 日後回憶回答接受，再說沒有確切銷量。這是即問即答，沒有缺一個 payoff。`大家` 在此承接顧客可以理解；改「顧客」可選，並非事實必修。這項判斷不覆蓋 round9 raw `payoffs=no`。 |
| 近問答是否要硬加回呼 | **PASS（現況可保留）** | 上述相鄰問答，以及 `4e5m → 7asx`，不需加「還記得」。`script-writing.md:104` 要求遠距離才點名，近處直接續答；強加回呼會製造重述。 |
| 用途主線是否較順 | **PASS（依 frozen 品類史讀法）** | 同一問題從能滾、自製、上架、航站搬運，走到直立推行與轉向；1997/2000 段有回答前章的作用，不只是念品牌清單。兩句有改善，沒有新未證因果。 |
| 是否已滿足正式 one_thread 全條件 | **HOLD** | 文字仍跨 Burnham、Kelly、Sadow、Plath、Samsonite。若規則要求同一具體人／團隊／專案全程行動，改兩句無法使它成立；frozen 又明許日用品演進。此適用問題尚未由本次真 panel 解決，不能將上列人工可讀性 PASS 當正式 yes。也不能為求 yes 捏造同一只箱子或技術傳承。 |
| 改稿後的事實／全片關卡 | **HOLD** | 目前 `o22`、`n1` 仍是原 `PLAN/note`；n1 只改 claim 文。作為明示 UNREVIEWED 的離線候選可以保留歷史，但若正式採用，受改句／claim 必須失效化並真正重查，不能沿用舊判作新稿通過。o22 的舊 claim 仍可支持日期與製箱，但未明記新句「自製」的範圍，重查時應一併確認；不需換 source/fact 索引。 |

## 4. 四處必修聲畫錯位：目前全部仍存在

| Scene／旁白 ID | 判定 | 現有問題與最小修正邊界 |
| --- | --- | --- |
| `origin-01 / zc7k` | **FAIL（聲畫對位）** | 旁白母親拉箱出發；prompt 是 young adult man 在門口放箱、準備提走，木柄縮著。人物與動作均沒有承接改句。應讓匿名母親使用伸出的木柄拉兩輪箱；仍為示意，不能冒充真實照片或精確肖像。 |
| `idea-01 / j9sw,ugak` | **FAIL（角色／動作歧義）** | 旁白推銷者被拒；prompt 的 salesman 指著出口、面帶拒絕，看起來反而在趕人。應把拒絕者明確為匿名採購，單一退回／搖頭動作；不能只換英文標籤而保留角色方向不明。 |
| `idea-05 / s7me` | **FAIL（錯誤提前揭曉）** | 話才問另一個人會否不同，圖已讓 buyer 堅決搖頭並用腳踢回箱子；下一鏡卻是副總裁試用、後續翻案。應只呈現未表態的檢視樣品／拿拉帶，與 `idea-06` 道具空間一致；不要先畫拒絕或成功。 |
| `now-01 / 7asx,kfiw` | **FAIL（超出來源的場景暗示）** | prompt 仍是 late 1990s luggage shop、shopper、貨架。和明點 1997 發表的旁白並置，容易被讀作當年已在店售，而來源未證明。改為中性產品示意／展示環境、匿名示範者向前推直立四輪箱；不帶貨架／價格／零售身分，不先畫 2000 的萬向側滑。 |

上表是對既有 prompt 的具體判斷；不是已看過生成影格，也不是報告中「建議」已完成。這四個 prompt 在本候選和 round9 完全相同。

## 5. 相鄰三鏡與其他限定事項

| 項目 | 判定 | 說明 |
| --- | --- | --- |
| `turn-15` 構圖可讀性 | **HOLD（畫面驗證前）** | 目前同格有一排兩輪直箱、角落四輪橫箱、人物。與旁白不是確定的史實衝突，但輪數／姿態可能混淆，宜將提問焦點收在一只直立兩輪箱。這項與上表四處「已確認錯位」分開；原 audit 也稱它必修，本次不把推測的生成失敗寫成已發生。 |
| `now-02b / 5tik` | **HOLD（動作辨識）** | 現 prompt 已有 upright、four swivel casters、sideways，文字方向符合多向輪；問題在相鄰 now-01 外形近似，靜圖是否真的看出轉向尚未驗證。應與前鏡向前推作清楚視覺區別，不把年份全壓在觀眾猜同一款箱上。 |
| 片長／節奏 | **HOLD（實測未做）** | 官方估算 8:40.333，低於原約 10 分／9–11 分目標。37 warnings 不能當零風險，其中 14 個靜圖逾 10 秒值得後續分鏡處理；但角色漫劇的數值警告不能全部移植成旁白品牌故事硬門檻。不得靠停頓、慢播或灌字補足。沒有理由在本次窄審擴寫整片。 |
| 設定／來源保全 | **PASS（本次機械範圍）** | 六章 source/fact 索引、series、畫風、原 source evidence 未改；候選本身不含媒體、沒有寫正式 receipt。verify 的 0 error 只證明結構與既有 lint，不證明畫面或敘事已合格。 |

## 6. 有限下一步

文字兩句可作為下一版待查候選保留，無需回滾成 round9。先修四個確定聲畫錯位，並把 `turn-15/now-01/now-02b` 的觀看任務分清；改動另建 manifest 和重新綁 hash。之後若依既有正式流程採用，需真正查核受改句／claim、全片敘事與後續媒體品質。此報告不代替任一關卡，不要求盲重跑相同 panel，也沒有授權付費三鏡試作。

本次只寫 Temp 審查報告、只讀核對程式及證據 JSON。未改 repo／快照／正式機，未呼叫模型、TTS、圖像或媒體生成，未修改 round9 FAIL 或任何 counters。
