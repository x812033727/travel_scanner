# S38 R8an PF038 木箱提示獨立紙面核對

**PASS（僅提示／史料相容性；新原生圖仍須另行驗收）。**

審閱者：`/root/s38_pf021_last_paper`，與 verify133 作者不同。以凍結檔案實際內容及 Git HEAD 為基準。

## 綁定雜湊

- `video.json` SHA-256：`b3c013a87c7af580f7e905bd855e25a28c7138f4a551d048174604f716870b8b`。
- `script.md` SHA-256：`2be40fda932ec6881f9f9cc1cb504bbe3705157f0c0e8a15cf74f1044c8e0314`。
- `claims.md` SHA-256：`65d2d3c70735495fb4c9e42806a414fc5dba90a67c4aa3eaaae4a9f12c30e464`。

## 差異與史料

實際遞迴比對 Git HEAD 與目前 video.json，僅一個 JSON 葉節點改變：`/scenes/37/data/prompt`，對應 PF038；其前後值逐字符合 verify133。所有其他場景完整物件、camera、look、文字卡及台詞均不變。112 個 spoken line 物件（含文字、id、emotion）與 HEAD 完全相同；script.md 及 claims.md 也與 HEAD 無差異。

固定 Pepys 原文 D2c，L65888–65893 記飯後街道滿是人、馬、載貨車，並把早晨收進的物品搬往更遠街道。新提示仍是1666年飯後搬運家當往馬車；改為近景、可見橡木板與鐵箍的小箱子，是避免現代紙箱的時代相容插圖安排，不聲稱日記指定木材、箱型或搬運者身分。沒有新結果、見證、對白或時間轉移。街石、白麻袖口與灰午後光亦是插圖安排，不作史料證據。

## 已選圖與額度邊界

目前 manifest 恰有27筆：原25筆加 PF036、PF037。原25筆完整記錄 canonical SHA-256 仍為 `6be60e778ca9a312fcbfab79e74f9090b0cb3c0a9b9580836c7496f3c73debfc`，與 verify132 起始基線相同；PF036、PF037 入選雜湊與 verify132 相同。PF038 不在 active selected entries 中，既有27筆不得重畫或修改。

目前27筆完整記錄 canonical SHA-256：`3d999f8ab58f3b8395f9f6e54acdb5fc57d9e14da60c231725afef2c2a592806`。

PF038 已有2次實際原生圖，只容許剩餘1次，提示修改不重設次數；若最後原生圖失敗，不得有第四次。PF039 已有1張 ready、尚未評審的 cached 原生圖 `/workspace/.video-work/curio-s38/keyframes/pf039-1.jpg`，249000 bytes，SHA-256 `4282ee6bc682b740349a11eb00110a6baad2ef72a53f91592e64badcbbb98c43`；保留檔案及已付次數，應先利用現有圖，最多另2次實際原生圖，不得當作零次重啟。

本次只寫驗收票，沒有修改媒體、創作檔、manifest、ledger、STOP 或 git。此 PASS 不代替新原生圖審核，也不新增預算。
