# A01 r21 獨立史實與企劃全文審查（HOLD）

- 審查對象：`story-rolling-suitcase-v2` 的 r21 離線候選；**不是**正式機稿件、正式 worker 審稿通過、付費製作或上架許可。
- 綁定 `manifest.json` SHA-256：`5131D53CEF6F20184C1D5043CF63428602DEB1551FFB9808CA42E940F190E900`。其中 `candidate/claims.md` 為 `eaa249f5499cde9cd4a9453f6b78adc862c004d68cf4b408c898e26a31ba0987`、`candidate/script.md` 為 `4d78999a42e4a485937d0c7b2e4a5cde7e7e1401e4c1684e5ef0e0580f16bc43`、`candidate/series.json` 為 `650471512080d92f0444e16fcf198e1c0fc554bdceb8dd422d3bcf797e782289`、`proposed-25-source-series.json` 為 `04245f1bb3ab5ebda8cdb3334dc962d2adc7ea5b10d8a83ee8f99686d6facdb7`、`candidate/video.json` 為 `a9bdaa89d82c7d2a7e0d718ad02f41533d0412ac75841a9520ca7abe8a7f2eae`。
- 審查範圍：74 個 `PENDING` claim ID、65 鏡／77 行旁白與視覺提示、18 筆公開來源、source map／alignment、23 來源的 `candidate/series.json` 和 25 來源提案的全部文字欄位（含 logline、角色、章節點、待查聲明、來源 supports、caveats、圖像提示、縮圖文字與註記）。兩份企劃的既有 23 個 URL 相同，除 5 筆 `checked` 日期和新增 2 筆來源外，企劃敘述相同；下列企劃問題同時存在於兩份。
- r20→r21：74 個 ID 與順序維持，只有 `h6`、`e37` 兩個 claim 文字變動，其餘 72 個逐項相同。65 鏡／77 行不變；`origin-01b`、`engine-porter` 兩段旁白變動，`turn-09b` 與 `turn-09` 調序並改視覺提示。所有 claim ID 均可在 scene refs 與 alignment 對上，沒有孤兒 ID。`h6` 已把旅客「費力解開」而非「已解下」校準到 2012 報導；`e37` 已把搬運工說法歸屬於 Shiller 2008 年課堂轉述。
- 結論：**P0 0；P1 2；P2 6；仍 HOLD。** P1 會使觀眾把不同設計／不同事件和 1987 年車庫情節接成一件事，須在 r22 消除。P2 應同版修正來源精度。沒有任何 `PASS` 被前版繼承。

## P1：發行前須修

1. **兩份企劃把「1987 車庫 Rollaboard」寫成已證實的同一事件。** `candidate/series.json` 與 25 來源提案的 `chapters[turn].point`（約第 78 行）說「Travelpro 記述 1987 車庫 Rollaboard」；`must_verify[4].claim`（約第 122 行）說「Travelpro 回顧 1987 年車庫 Rollaboard」。[Travelpro 官方歷史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage) 將兩輪直立伸縮把手設計定在 1987 年、車庫作業搬入倉庫定在 1989 年；[ABC／USA TODAY 2012 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603) 的「回車庫把推車鎖在硬殼箱上」沒有標事件年，也沒有證明這只安檢原型就是後來定型的兩輪 Rollaboard。1989 專利描述後來的結構與問題，不能補成 1987 車庫實物構造。建議分開寫：「2012 訪談記述未標年份的推車鎖箱安檢故事；Travelpro 回顧 1987 年完成直立兩輪伸縮把手設計，1989 年搬離車庫。」不要替安檢故事指定 1987 年或直接等同量產型。
2. **r21 調序使旁白把安檢臨時箱和直立兩輪箱接成同一物。** `candidate/script.md` 的 `turn-07c`（約第 220 行）說安檢員答「好」，下一鏡 `turn-09b`（約第 224 行）立即說「箱身直立，底下兩個輪子，上面接一根能收回去的伸縮拉桿」；至 `turn-09` 才作 1987／1988 年份比較。新視覺提示有區隔，**可聽見的故事沒有**。ABC 2012 僅說推車鎖在硬殼箱上，[Travelpro 官方歷史](https://travelpro.com/pages/our-history) 才說 1987 年的兩輪直立伸縮把手設計。建議在 `turn-09b` 加明確口語橋接，例如「後來定型的 Rollaboard，外形已經不同：……」，並保留年分比較；勿讓這句成為安檢那只箱的形貌描述。

## P2：同版修正的來源精度

1. **`1921 車站候宿` 地點超出館方文字。** 兩份企劃 `must_verify[8].claim`（約第 156 行）說「1921 年首旅車站候宿經驗」。[Winnetka 館方的 Anita 生涯文章](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/) 只說搭火車到新地方後，父親去找廉價住處，Anita 與孩子守著行李，沒有指明候宿地點在車站。`o30` 和相應畫面已避免指認車站。改為「搭火車抵達新地方後的候宿／守行李經驗」。
2. **開場把改箱年份鎖在 1928。** `candidate/script.md` 的 `hook-anita`（約第 24 行）及 `video.json` 對應 text 說「1928 年，安妮塔的兒子把舊嬰兒車輪裝上箱子」。[Winnetka 館方藏品文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/) 僅確立 1928 年第二趟旅行**之前**已改好；「1927 suitcase」圖說不能證明是片中同一只或確切製作年。改「準備 1928 年旅行前，安妮塔的兒子……」。
3. **`三十多年後` 以未證實年份算事件距離。** `candidate/script.md` 的 `idea-memory`（約第 80 行）把 1939 巡講後的 Sadow 機場靈感說成「三十多年後」。[ABC 2010 Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469) 沒有給阿魯巴返程確切年份；[Sadow 專利](https://patents.google.com/patent/US3653474A/en) 僅給 1970-02-16 申請日。`i35` 也未支持精確間隔。改「多年後」。
4. **`i35` 使用跨來源的無證據結論。** `candidate/claims.md` 約第 28 行以 ABC 2010 Sadow 訪談為唯一來源，末尾說「與 Anita 的故事也無可證實的直接交接」。該文不提 Anita，因此僅能說「這篇訪談沒有記述兩者的直接交接」，不能由一篇未提及的文章證明整體不存在交接；或刪此尾句。前版 `n61` 與企劃已改用「本集所查來源未證實」限縮，`i35` 應一致。
5. **企劃把記者敘述當成 Plath 本人回憶。** 兩份企劃 `chapters[turn].point`（約第 78 行）寫「Plath 自述安檢推車故事」，`must_verify[3].claim`（約第 113 行）寫「Plath 的安檢經歷是其受訪回憶」。[ABC／USA TODAY 2012 報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603) 的旅客「費力解開」是記者敘述，安檢員答話才放在 Plath 的直接引語中。`h6/t5/t46` 現已正確修成「費力解開」，企劃也應改「2012 年 Plath 受訪報導所記安檢故事；安檢員對話由 Plath 直接引述」。
6. **兩份企劃的 `1970 年 10 月開賣` 超出所引 ABC 2010 的日期。** 來源 `supports` 在約第 222、236 行寫 Macy's 1970 年 10 月開賣。[ABC 2010 Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469) 確認 Levy 下單和 **1970 年 10 月店內人偶展示**，但沒有直接給首次開賣日期。這不是斷言十月未開賣；是此來源對這個精確說法不足。`engine-08` 旁白已用展示，企劃可同步改「Macy's 決定進貨；1970 年 10 月展示人偶」。

## 已核對且仍需保留的界線

- [Winnetka 館方文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/) 分開 1921–22 第一趟旅程與 1928–30 第二趟；`o30/o32/n16/n63` 及旅後巡講的敘述目前未把兩趟混作同一次，也未把 1939 Midland 所見箱認作館藏同一箱。
- [Yale 2008 課堂紀錄](https://oyc.yale.edu/economics/econ-252-08/lecture-3) 中搬運工反對是 Shiller 轉述其助理致電 Sadow 的回話。r21 的 `e37` 已作此歸屬，不能再升格為同期百貨檔案。[ABC 2010 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469) 說的是當時「男人不碰輪子箱」的觀念。
- [Plath 專利](https://patents.google.com/patent/US4995487A/en) 1989-08-08 申請、1991-02-26 核准，說明外置推車在安檢、登機、落地反覆拆裝與其後結構目標；不提供 1987 安檢故事的精確日期或那只原型的逐項零件。[Travelpro 官方歷史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage) 說更新 Sadow 設計，不足以證明 Plath 親眼看過 Sadow 的原型。
- [Quirks 1992 Samsonite 一手研究稿](https://www.quirks.com/articles/research-with-travelers-helps-samsonite-develop-a-convenient-new-line-of-luggage/) 的 1986 概念、1987 停車場、1988 空服員調查、1990 上市有分開；[Samsonite 官方歷史](https://corporate.samsonite.com/en/about-us.html) 的 1997 Ultra Transporter 與 2000 spinner 已分開，不採其他文獻的 2004 起點。
- [LA Times 1993 採訪](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html) 支持機艙尺寸測試與另帶衣物／平裝書造成不合，不是所有輪箱普遍不能上機。[Travelpro 樓梯文章](https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases) 把樓梯困難限於部分旅客與地形；稿件未擴成無條件定律。

## 查核限制與機械結果

- Winnetka 兩篇官方站原文瀏覽連線逾時，依官方搜尋索引全文核對；1939 Midland 的 48 MB 原報紙 PDF 未完成逐頁目視，只核到官方庫的索引 OCR，故不能把報紙版面或每字視為已直接確認。RNPA 2016 PDF 本輪直開逾時，先前獨立 r19 審查直接核過 pp. 46–48；本輪僅與該收據和來源表比對，未重作 PDF 逐頁檢視。Chinook 的官方 PDF 與 sl8 鏡像都過大未直接位元組比對；僅讀官方來源搜尋索引。Briggs & Riley 新聞稿本輪亦以 PRNewswire 的原站索引核其原文要點。上述未直接讀到的材料維持 `PENDING`，沒有冒稱一手重驗。
- 兩份企劃的流程性句子（如 B18 或正式機狀態）不屬此歷史來源審查，沒有代替正式機讀回。18 筆公開資料的 claim 對位與 23／25 筆企劃索引均檢查；因上述原件取得限制，這是**有界的全文審查**，不是所有原始影像的完全覆核。
- `node A01-editorial-candidate-20261019-r21/build.mjs --check` 退出碼 0：65 scenes、77 lines、74 claims、18 public sources、1858 spoken units；估時 250／275／300 cpm 分別 516.4／476／441 秒；lint/cute 機械錯誤皆 0。這不代表史實問題已消除或正式 worker 可通過。

本收據只寫在 r21 目錄，並綁定上述 manifest 與候選輸出 SHA-256；未改動候選、舊收據、任務票、PR、正式主機或付費資產。待作者出 r22，須重新對 r22 的實際檔案與 manifest 做獨立審查；本收據不得當作 r22 PASS。
