# A01 輪子行李箱 r20：史料措辭限縮候選 — HOLD

這是從已釘選 r19 離線稿、[r19 獨立主張稽核](../A01-editorial-candidate-20261019-r19/independent-fact-audit-20261019.md)與修正後的 25 筆來源企劃提案衍生的**另一份候選**。建置器先驗證前版輸出與審查收據，再只在本資料夾產生檔案。r19 及更早版本、正式機、媒體與付費素材均不改動；舊審查不自動核准 r20。

## 稿件變更

- `t5`、`t46` 都改為 [2012 年 USA TODAY／ABC 受訪報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)所能支持的「旅客**費力想**把以彈力繩固定的箱子從金屬推車卸下」；報導沒說是否成功，也沒有 Plath 對那位旅客動作的逐字引言。`turn-05`／`turn-06` 旁白仍描述困境與所需步驟；`turn-06` 插圖明確停在嘗試階段。
- `hook-04` 移除對百貨拜訪的精確 **1970 年**斷言，改為「後來」；[Sadow 2010 年受訪](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)記樣品推銷、遭拒及 Macy 展示的順序，沒有給逐店拜訪日期。插圖也不標特定年代。
- `origin-r12-01`、`origin-01b` 與 `o1`、`o32` 改稱 **1928–1930 年第二趟長途旅行**。[Winnetka 歷史學會家族史](https://www.winnetkahistory.org/who-were-the-burnhams/)具體記 1921 年先行歐洲、非洲，1928 年再展開路線更廣的第二趟旅程；不暗示首旅已完成環球。
- 片尾將「三人沒有直接傳承」限縮為**本集查到的資料還不能證明三人一棒接一棒直接啟發**。`n16`、`n61`、`n63` 各自只陳述相應材料能證實或尚未記載的範圍。[Travelpro 公司史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)把 Plath 的設計寫成對 Sadow 輪箱的改良；本稿不否認這項公司說法，也不把它擴大成有文件證明三人直接傳遞原型。

鏡頭 ID、鉤子的 setup／payoff ID、65 鏡、77 句、74 筆仍為 `PENDING` 的主張、18 個公開引用來源、畫風與配音規格不變。`candidate/series.json` 的 23 個編輯來源與新增的 `proposed-25-source-series.json` 只修正旅行措辭，來源 URL／順序／數量不變；後者仍是**擬採用**企劃，未裝入正式機。`plan-source-addition.json` 沿用 r19 的未採用提案。

## 使用界線

`validation.json` 的秒數只由文字代理估算，沒有實際 TTS、剪輯或盲聽。r20 仍需獨立查核改動後的主張與節奏；1939 年原報紙掃描尚未直接逐頁視讀。正式機還須核對 104→新版本、六章、重新編號的主張、verifier、listener、兩名獨立敘事讀者、正式 `story/reviews/script-review.json`、圖片聯絡表及 US$25 帳本。保持 **HOLD**，不授權主機寫入、解除 STOP、付費呼叫、合成或上傳。

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r20/build.mjs --check
```
