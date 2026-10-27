# 第 6 輪事實查核（2026-10-26，獨立新工作階段）

製作路線：教學卡片。本輪是新的獨立工作階段，沒有沿用前幾輪的結論。官方頁兩份今日重讀，皆為 ok=true、status 200。所有算式都重新獨立計算。金額、稅率與供應商是原創練習資料（fixture），以內部一致性和算術核對；它們不是外部事實，不需要官網佐證。第三方頁（kevinstratvert.com、fableguide.com）沒有任何數字進入 video.json，本輪也不拿它們佐證任何事。

| # ｜ claim ｜ where ｜ URL ｜ verdict ｜ before → after |
|---|---|---|---|---|
| 1 ｜ 三家單價：甲 180 未稅、乙 205 含稅、丙 175 未稅 ｜ opening-unit、cost-unit-baseline、extract-birch、missing-known、revision-diff ｜ 原創 fixture（materials） ｜ CONFIRMED（各卡一致） ｜ — |
| 2 ｜ 需求為 10 張 A6 105×148 mm、350 gsm 霧面、雙面全彩、同址、7 個工作天；兩張需求卡的第 8 行重疊且一致 ｜ need-spec、need-delivery、ddpd ｜ 原創 fixture ｜ CONFIRMED ｜ — |
| 3 ｜ 原檔清單：aster.pdf、birch.pdf、cedar.pdf ｜ need-labels ｜ 原創 fixture ｜ CONFIRMED ｜ — |
| 4 ｜ 供應商與稅率是虛構練習設定 ｜ need-fiction、description ｜ brief ｜ CONFIRMED ｜ — |
| 5 ｜ 工作分成抽文 → AI 欄位 → 精確小數計算 ｜ need-route、extract-start、description ｜ brief ｜ CONFIRMED ｜ — |
| 6 ｜ 甲的運費 200 未稅在第 2 頁，單價與 5% 在第 1 頁 ｜ need-proof、extract-aster、extract-aster-quote ｜ 原創 fixture ｜ CONFIRMED（與算式一致） ｜ — |
| 7 ｜ viewer-prompt.txt 全文 7 行，caption 寫第 1–7 行 ｜ extract-core ｜ materials ｜ CONFIRMED（實數 7 行） ｜ — |
| 8 ｜ 乙運費 0、送達免運、交期 5 個工作天 ｜ extract-birch ｜ 原創 fixture ｜ CONFIRMED ｜ — |
| 9 ｜ 丙寫 "Shipping: not quoted"，值為 null，頁碼 2 ｜ extract-missing-quote、extract-null、missing-known ｜ 原創 fixture ｜ CONFIRMED ｜ — |
| 10 ｜ 單價排序為丙 < 甲 < 乙 ｜ cost-start、cost-unit-baseline ｜ 算術 ｜ CONFIRMED（175 < 180 < 205） ｜ — |
| 11 ｜ 甲 10 張：1,800 + 90 + 210 = 2,100 ｜ cost-aster-formula、cost-initial-result ｜ 算術 ｜ CONFIRMED ｜ — |
| 12 ｜ 乙 10 張：10 × 205 = 2,050 ｜ cost-birch-formula、cost-initial-result ｜ 算術 ｜ CONFIRMED ｜ — |
| 13 ｜ 丙原版總價待確認，乙 2,050 低於甲 2,100 ｜ cost-initial-result、bcr5 ｜ 算術 ｜ CONFIRMED ｜ — |
| 14 ｜ 小數交給計算工具，原文值與計算值分欄 ｜ cost-rounding、cost-workbook ｜ brief ｜ CONFIRMED ｜ — |
| 15 ｜ 試算表不會自己重算 ｜ ehby、description ｜ https://openpyxl.readthedocs.io/en/stable/simple_formulae.html ｜ CONFIRMED（"openpyxl never evaluates formula"） ｜ — |
| 16 ｜ 丙商品含稅比乙低，運費不高就會翻盤 ｜ e86a ｜ 算術 ｜ CONFIRMED（2,050 − 1,837.50 = 212.50） ｜ — |
| 17 ｜ 詢問草稿由使用者確認 ｜ missing-question、missing-no-send ｜ — ｜ OUT OF SCOPE ｜ — |
| 18 ｜ 狀態欄使用規則 ｜ missing-status ｜ — ｜ OUT OF SCOPE（教學建議） ｜ — |
| 19 ｜ 修訂版取代 CED-1026-v1，供應商仍是三家 ｜ revision-start、revision-identity、revision-links ｜ 原創 fixture ｜ CONFIRMED ｜ — |
| 20 ｜ 丙修訂 10 張：1,837.50 + 262.50 = 2,100.00 ｜ revision-diff、revision-total ｜ 算術 ｜ CONFIRMED ｜ — |
| 21 ｜ 修訂後乙 2,050 最低，甲與丙同價 ｜ revision-ranking、dyun ｜ 算術 ｜ CONFIRMED ｜ — |
| 22 ｜ 來源欄要改成對應修訂版 ｜ revision-links ｜ — ｜ CONFIRMED（流程描述） ｜ — |
| 23 ｜ request-20.json 全文 4 行、quantity 20；命令參數 ｜ quantity-edit、quantity-run、quantity-output ｜ materials；實跑紀錄（不在 payload） ｜ CONFIRMED（行數）；實跑輸出見下方「懷疑但未改」 ｜ — |
| 24 ｜ 三家單價適用 10–20 張，運費在範圍內固定 ｜ quantity-ranges、sxtz ｜ 原創 fixture 第 2 頁 ｜ CONFIRMED（與 brief 一致） ｜ — |
| 25 ｜ 甲 20 張：3,780 + 210 = 3,990 ｜ quantity-aster ｜ 算術 ｜ CONFIRMED ｜ — |
| 26 ｜ 乙 20 張：20 × 205 = 4,100 ｜ quantity-birch ｜ 算術 ｜ CONFIRMED ｜ — |
| 27 ｜ 丙修訂 20 張：3,675 + 262.50 = 3,937.50，最低 ｜ quantity-cedar、quantity-ranking ｜ 算術 ｜ CONFIRMED ｜ — |
| 27a ｜ 甲與乙的名次相對 10 張時反轉 ｜ pruf ｜ 算術 ｜ CONFIRMED（10 張甲 2,100 > 乙 2,050；20 張甲 3,990 < 乙 4,100） ｜ — |
| 28 ｜ 交付內容為可編輯表、待問清單與變動清單 ｜ handoff-output ｜ brief ｜ CONFIRMED ｜ — |
| 29 ｜ 掃描圖片的抽文結果可能是空的，要改用有辨識能力的流程 ｜ handoff-scan、description ｜ https://pypdf.readthedocs.io/en/stable/user/extract-text.html ｜ CONFIRMED（"the extracted text may be minimal or visually empty"；"pypdf is not OCR software."） ｜ — |
| 30 ｜ 表格排版可能把數字接錯 ｜ handoff-table ｜ 同上 ｜ CONFIRMED（"Typically, tables are just absolutely positioned text… hard to tell where columns / rows are."） ｜ — |
| 31 ｜ 實跑日期 2026-10-26 ｜ quantity-run、quantity-output 的 caption 與 source ｜ brief、claims（lab receipts） ｜ CONFIRMED（日期與 brief 相符） ｜ — |
| T ｜ 縮圖、youtube.title、tags ｜ thumbnail、youtube ｜ — ｜ CONFIRMED / OUT OF SCOPE ｜ — |
| D ｜ description：Codex 分析、pypdf、openpyxl 不算公式、不做 OCR、日期 2026-10-26、5% 為練習設定 ｜ description ｜ 上列兩份官方頁與 brief ｜ CONFIRMED ｜ — |

## 計數

- CONFIRMED 30
- CHANGED 0
- NOT FOUND 0
- OUT OF SCOPE 3（c17、c18、outro CTA 與 tags 的風格部分）
- changed_facts = 0，video.json 不修改。

## 規則檢查

- **免責語家族**：旁白與 description 都沒有出現以官網為準、公告沒寫、我不唸、不在這裡唸、不替你填，也沒有「不代表／不等於」用在描述某事沒寫的句子。
- **查證用語**：旁白沒有出現經查證、根據官方文件、截至查證、本影片。
- **敘事者**：沒有站主常設指示，旁白沒有使用名字、口頭禪或固定結尾句。
- **建議類內容**：沒有財務、稅務、法律或健康建議；稅率明說是計算假設。
- **個人資料**：沒有。

## 即將過期

- 所有金額都是原創 fixture，沒有會過期的價格。
- pypdf 6.21.2 與 openpyxl 3.1.3 的行為描述以 2026-10-26 讀取為準，套件改版後要重讀。

## 意見不符

- 旁白沒有標記為站主個人的意見。
- 教學建議（先寫需求、回原文核對、只用明示條件計算）與站主觀點立場 1、3、4、6、7 一致。
- 沒有發現不符之處。

## 懷疑但未改

1. quantity-output 表的內容（需求數量 20、採用修訂版、供應商名單）和 quantity-run 的實跑標示，依據是 lab receipts 裡的 selected-comparison.json 與 stdout。本輪 payload 沒有附這些原始輸出，所以這裡無法直接核對執行證據。這兩張卡的旁白是要觀眾自行打開輸出確認，沒有把預期結果說成已觀察到的成功。成片前必須對照 receipts 做視覺核對；對不上就要把這兩張卡改成「預期輸出」。
2. aster.pdf、cedar-revised.pdf 第 2 頁的逐字全文，以及 requirements.txt 全文，仍未摘入 claims。quantity-ranges、sxtz 與兩張需求卡依賴這些原文。
3. 原版 cedar.pdf 的「數量適用 10–20」（missing-known）在本 payload 中只能和 brief 對照，看不到原頁。
