# T27 獨立事實與聽眾審稿

判定：`PASS_TEXT_FACTS_AND_LISTENER`。本判定只覆蓋下表位元組版本的旁白、主張、投影片文字資料、縮圖文案、標題、說明、標籤及來源；尚未驗收 SVG 圖形、聲音、時間軸、CC、成片、後台或發布。

審稿者 `facts_t27`，未撰寫本集稿件；作者 `write_t27`。查核日 2026-10-02，完整讀取六章、137 景、137 句、13 個主張 ID 及全部 metadata。不是沿用季企劃的文字收據。逐句與逐卡摘錄另保存在 repo 外的 `t27-facts-extracted.txt/json`；來源獨立取得、頁碼、HTTP 狀態及快照雜湊在 `fact-source-audit.json`。

| 受審檔案 | 實際 byte SHA256 |
| --- | --- |
| `video.json`，一次聽眾改寫後的目前 master | `89d7d0fb16acfb196d5f19f6f9cc96a776b69b08234a492f1d3e8fd7078d494c` |
| `claims.md` | `2b29857d6720932ac286992e0467f63700624249634a251541aa6a102afc0518` |
| `brief.md` | `25afc729f4c2243d98eedac3e1e2134b411da10a3b178e225e1734bb5201e62b` |
| 137 句 ordered id/text/say/say_for 序列的 byte SHA | `4ff9e7a0005e915f58199825e2b04cf04f0289471b4395ad2f85507a27b0840c` |
| 旁白、章節、主張、非 SVG 文字資料與 metadata 的語義序列 SHA | `b5216546e839ec897a8e9ef67f1325b2f803026fe44620d0255ab64152ba57f0` |

## 一手來源與取得界線

S1 為 [觀光廳結果公告](https://www.mlit.go.jp/kankocho/news08_00039.html)，S2 為 [原始調查附件](https://www.mlit.go.jp/kankocho/content/001998584.pdf)，S3 為 [有日期的報道發表 PDF](https://www.mlit.go.jp/kankocho/content/001998583.pdf)。三份來源均由本審稿者當日獨立讀取，另使用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 公開 GET 留存完整快照，HTTP 200；同站直接 GET 間隔超過一秒，未讀取任何私密資料。

S2 實際渲染、打開並閱讀 PDF 實體第 2、5 頁，即印刷第 1、4 頁；已看清面訪方法、逐機場表、複選題意、當年度與前年度圖例，以及 17.2%／43.7% 的歸屬，不用文字解析的碎片自行猜圖。S3 首行的 2026-04-28 是發表日期，與 S1 的最後更新欄分開核對；不是只把網頁更新欄當成發布證據。

另以 S4 [東京航空局的機場頁](https://www.cab.mlit.go.jp/tcab/airport/list/haneda/) 本日正文及指定 UA HTTP 200 核對「東京國際機場」與「羽田」是同一機場。它只補機場名稱對照，不增加交通、政策或設施主張。

## 完整主張審查

「位置」列包含主要 scene／line，並覆蓋同 ID 所有 `scenes[].claims` 關聯及全部文字重述；旁白與 `scene.data` 的數字、日期、題意均已逐一讀過。沒有使用搜尋摘要、作者索引或模型自述當作官方證據。

| ID | 主張及主要位置 | URL／狀態 | 判定；修正前 → 後 |
| --- | --- | --- | --- |
| c1 | 2026-04-28 公布；c3-s10/qi3w、c3-s11/nejc、c6-s15/m25k 及日期 caption | S1、S3／200 | CONFIRMED。發表日已由 S3 明列；nejc 的「大家何時看見結果」→「公開結果的時間」，不把公布日當每個人的實際觀看日。 |
| c2 | 2025-11-18 至 2026-01-13 收集；c3-s02–s08、s12、s16、s18–s19及 c6-s15 | S1、S2 印刷 p1／200 | CONFIRMED。期間跨年不等於每位旅客跨年旅行，也沒有聲稱每座機場每天訪問；日期數據未改。 |
| c3 | 五座機場、4,110 位準備出境的外國旅客；c2-s02–s05、s07、s09、s11、s16–s17、c6-s04、s16、s23 | S1、S2 印刷 p1、S4 名稱對照／200 | CONFIRMED。成田、東京國際機場即羽田、關西、福岡、新千歲；1014+1015+1012+537+532=4110。受訪地點沒有被換成困擾發生地點；未稱所有住民或全體旅客。 |
| c4 | 面對面問卷；4,110 不是網路留言票數；c2-s10/mkgu、s11/cht5，claims c4 | S2 印刷 p1／200 | CONFIRMED。另外的 2,000 則網路分析與面訪樣本分開，影片沒有把兩者合併，也沒有新增該分析的結果主張。 |
| c5 | 詢問這次訪日旅行困擾，可複選；c2-s08/85z3、c4-s09/5pqn、s10/257h及相關重述 | S2 印刷 p4／200 | CONFIRMED。當年度 n=4110、複選。訪談在機場不代表受訪者只答機場困擾。 |
| c6 | 垃圾桶少 17.2% 是最多人選的困擾項目；c1-s01–s04、c4-s02–s03、c5-s21、c6-s03–s06、s22–s24，caption與尾卡 | S1、S2 印刷 p4／200 | CONFIRMED。限於困擾項目的排名，不把「沒有困擾」排除後稱全部答案第一名；17.2% 未過半。所有反問、標題、說明及結論均把多數疑問限定到垃圾桶困擾。 |
| c7 | 沒有困擾回答 43.7%；c4-s04–s08、c6-s08–s10與數字卡 | S1、S2 印刷 p4／200 | CONFIRMED。未當作垃圾桶項目的互補比例，未說多數受訪者沒有任何困擾。 |
| c8 | 旅程經驗不是全國街道普查或唯一歷史起因；c5-s15、s17–s21、c6-s16、s18 | S2 方法與題意／200；編輯範圍解讀 | CONFIRMED AS SCOPE INTERPRETATION。ch29「今天的旅客回答」→「這份旅客回答」，避免錄製日被誤解為收集日。沒有加入配置起源、恐攻單因或店家代收承諾。 |
| m1 | 排名與過半不同；十人中的三人可排第一，過半至少六人；c1-s08–s17及結論 | 基本算術，對照 c6；非新增人口資料 | CONFIRMED AS MATHEMATICS。3<6，17.2<50；不把示例三人換算成官方受訪人數。 |
| m2 | 複選時人數與勾數不同，同一人在每項只算一人；c4-s06–s10、s16–s27、s29、c6-s10–s12 | S2 複選題及 e1 原創設定 | CONFIRMED AS INTERPRETATION。每項比例不能拼成互斥圓餅；沒有推各項獨立機率或讓其強制合計百分之百。 |
| m4 | 受訪人數不自行擴張對象範圍；不同問題需要相應資料；c2-s17–s21、c5-s05–s22、c6-s16–s20 | S2 方法；編輯方法解讀 | CONFIRMED AS SCOPE INTERPRETATION。密度示意限定同一街道範圍的數量與長度，沒有說已執行實測盤點。 |
| e1 | 十人、十一勾的原創例子；c1-s10–s16、c4-s11–s23、s28–s29、c6-s11 | 原創設定，逐人算術 | CONFIRMED AS ORIGINAL EXAMPLE。一二三號垃圾桶；三四號連線；五號指標；六號溝通；七至十號沒有困擾。六人有困擾、七個困擾勾，加四個沒有困擾共十一個勾；三號在兩項出現。相關圖的固定示意標籤須在實際 SVG 查核中確認。 |
| e2 | 分享卡、旅客、日曆、相簿、三本筆記與盤點問題皆原創比喻；c1-s05–s07、c2-s12–s15、c3-s06–s15、c5及c6 | 原創教學內容 | CONFIRMED AS ORIGINAL EXAMPLE。rf86「一位旅客說不好找」→「假設一位旅客說不好找」，明示沒有實際訪談原句；未編造站主親身經驗。 |

整體覆蓋：13 個 claim ID 全數閉合，0 NOT FOUND／UNRESOLVED，0 新增或更換的數字、日期、對象、方法及官方資料結論。三項句意釐清已由作者按原 line ID 套用，再直接讀取確認；不是本審稿者代寫全稿。初輪完整稿 SHA `0f55147f50b4fae28fd4619ab99ceb4ad15a0b91701ac226833792b69e46c66d` 已被上表最終版本取代。

早期 skeleton 的 metadata 原本把「多數旅客都有困擾」問得太廣，已在受審全文保存前限定為垃圾桶困擾。這是問題範圍釐清，不更改官方資料；不能把 43.7% 沒有困擾當成「過半沒有困擾」。發布日額外加入 S3 是補足直接發表證據，不是換日期。

第二輪：不需。官方事實數據修正 0；全文內的句意釐清 3，沒有超過三項 FACT 修正。若後續變更數字、旁白或主張，應重新查核並依變更量判斷是否另派第三人。

## 聽眾與敘事

`PASS_TEXT_LISTENER`。開場先問垃圾桶特定困擾是否過半，第三句就給 17.2%，第四句將排名與多數拆開；六章依序用十人例子、機場問卷、日曆與相簿、複選連線、三本筆記、分享文字改寫推進。最後一句直接回答開場。概念與教學示意有具體作用，沒有無關清單、假對白、站主經驗、重複口號或手寫長停頓補時。

目前一次聽眾改寫後，137 句共 2,201 口語漢字（初審 2,200），含標點最長 22 字元；無超過 40 字、Latin、口播網址、括號、人工 `pause_after_ms` 或查核過程旁白。日期寫成中文唸法；精確阿拉伯數字留在圖卡。沒有來源流程塞進耳朵，也沒有比喻冒充實際樣本。

正常 CLI `node tools/video/cli.mjs lint --slug sothatswhy-t27` 實際 exit 0：0 errors、1 warning。warning 是第一整章估算約 87 秒，不是鉤子長度；以正常 `estimateTimeline` 獨立計算，第一句結束於 5.100 秒，第三句的 17.2% 答案於 15.067 秒，第四句的排名／多數區別於 20.400 秒。這些都是預設估算，實際前四句的聲音時間仍須以當前 WAV 核對。工具未改、warning 沒刪。先前加了不適用的 `--workdir` 選項曾被 CLI 拒絕，已改為這個正常指令，未把拒絕當成 lint PASS。

## 長度與媒體界線

預設估算 11.1 分鐘是含正常工具間隔的估算；目前 2,201 口語單位在每分鐘 250／300 單位時，純內容估算分別 528.24／440.20 秒。此處不把估算當作正文已滿八分鐘，也不降低至少 480 秒的門檻。TTS 後必須由當前逐句 WAV 重建時間軸，核對正常語音正文及成片各至少 480 秒；不得靠慢播、重複、片頭片尾或人工停頓補足。

目前 SVG 路徑與 caption 只作文字分鏡；尚未把實際圖形、手機辨讀或每景停留時長判 PASS。原創十人示例所有相關畫面須維持「原創示意，非本調查數據」，百分比圖不能誤畫互補圓餅，官方比例與教學例子不可混為同一組資料。之後加入 assets 或變更 SVG 時，需比較原口語與語義、補做畫面審查，再將本收據綁到最終 full master SHA；此文字 PASS 不自動轉移到改過的檔案。

`AUDIO / BODY / SVG / CC / MP4 / PLATFORM / OWNER_FULL_PLAY / PUBLISHED = PENDING`。本報告未聽過 Sulafat 實際音檔，未冒充站主接受成片；正常語音、成片十一項 QA、上架包、後台附件與發布各有各的當前證據。

## 素材登記後的文字收據重新綁定

2026-10-02T13:18:54.959Z 獨立讀取目前 master，與保存在 repo 外的完整受審 `7e698…` source 逐欄位比較：**唯一改動是 `assets` 登記 130 項**。137 句的順序、ID、text、say／say_for 全部一致；six chapter／scene ID／template／claims／非 SVG data、來源、縮圖文案及 YouTube metadata 語義序列完全一致；`claims.md` 與 `brief.md` byte SHA 也未變。沒有用排除所有 scene 的粗略比較掩蓋未審文字。

已讀目前 manifest 的檔案 SHA `4713d4455e5d2c14ca2f5d8e6a62247e888da903e3f661c4efb05e9f78349af1` 作這次資產登記 snapshot 標識，**不是 SVG 圖形或幾何 PASS**；後續 SVG 修圖仍由畫面 reviewer 及當前 runtime 資產綁定另查。此處只將已完整審過、逐字未改的文本判定重新綁到 `d506…` master。

完整素材登記比較收據：repo 外已凍結的 `t27-facts-assets-only-comparison.json`，SHA256 `378c628d6bce06509242af4a68b0eefd695bb2701f38a106ba61419f4928124d`；保存了 top-level changed keys、每景語義差異（空陣列）、原與當時 master、raw script／semantic／claims／brief 雜湊。前 `7e698…` 僅保留為完整文字初審 snapshot，`d506…` 則為素材登記後、聽眾改寫前的版本。

## 音訊阻擋後的一句聽眾改寫

2026-10-02T14:19:36.815Z 已獨立讀取 root 套用後的實際 `89d7…` master，沒有僅憑作者 JSON 建議宣稱新稿通過。137 句中只有 c1-s17／`63kr` 的 text 改變：

| 改寫前 | 目前改寫後 | 判定 |
| --- | --- | --- |
| 把兩個問題分開，第一名才不會越講越大。 | 把兩個問題分開，就不會把第一名當成多數。 | PASS_EQUIVALENT_LISTENER_REWRITE。仍比較排名與過半，保留「兩個」「第一」，讓隱喻改成直接說明；沒有新數字或調查結論。 |

其餘 136 句、全部 line ID、say／say_for、章節、template、scene claims、caption／其他非 SVG 文字資料、來源及 metadata 均逐欄位一致；claims 與 brief byte SHA 未變。相對初審 `7e698…` 的 top-level 改動只有 assets 登記及上述 scene 一句；直接讀取比較的語義差異也只有 c1-s17。不把這次 raw-script hash 的改變寫成「全部口語未改」。原 raw-script `fba8c240ce1ee225411e286a4fcd79f16a5bb0d4fc6ea1da5d685abc2b7f5ec8` 與 semantic `4d5e4c594a71c55a4c9db54c4405eeeaebb9a23ca2c5188ae20e51ff46adcc9c` 保留為上輪來源。

目前 137 句仍無 >40 字、Latin、口播網址、括號或手寫 pause；基本數值與方法仍為原 13 個已查核主張。這次為第 1 輪 listener rewrite，官方 FACT 數據變更仍 0，不需要另起 FACT 第二輪。新的實際 WAV、ASR、speech hash、時間軸與音訊 gate 必須重新走正常程序；本等價文字 PASS 未清除任何聲音 flags。

root 的正常改寫收據 `t27-listener-rewrite1.json`，實際 SHA256 `5d50dff7039f9fae48fa9080f2e77842e99cb2a151eabfd5dcac2e209c776334`，已由本審稿者讀取；其中紀錄正常 rewriteProblems 為空、一次只改一個 line text。聲音校正原因及原 WAV／checks 另由 root 保存，本審稿沒有抹除前次音訊失敗。

本審稿又在目前 source 重新執行正常 lint：exit 0、0 errors／1 opening-chapter warning，仍是 137 句。比對收據 `t27-facts-listener-rewrite1-comparison.json` 的實際 SHA256 `974c71487d5c0ef377fc5a77b760e0d9fdf847f722a628b411c784390319218c` 保存了唯一 c1-s17 的 before／after 語義差異。130 個 manifest entry 的 spoken_text／caption／路徑與目前 source 逐項核對，並將 manifest 現在的 `260ed6f4a37ce2199e8ef563fc0de0b4d92bd3368b67b89d5d4809927b538bda` 綁到本次文字 metadata snapshot；原 `4713…`／`fabc…` 的來源階段另有歷史收據，不冒充目前版本。

130 個使用中 SVG 位元組與目前 manifest 的 SHA 相符；這是 asset binding，不是全套 SVG 圖形語義 PASS。root 提出的 c2-s06 底部改為「每位受訪者算一人，不按五座重算」，符合不將人數乘以機場數的原教學題意，也避免暗示收集身分資料；這項特定文字釐清不增加人口調查方法。整套實際圖形與成片仍由對應畫面 reviewer 完成。
