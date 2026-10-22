---
id: 2026-10-22-correct-c10-oxo-source-hold-and
title: Correct C10 OXO source HOLD and image prompts
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-22T14:38:35Z
completed_at:
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/script.md
  - docs/videos/story-everyday-oxo-c10/visual-plan.json
  - docs/videos/story-everyday-oxo-c10/visual-plan.md
  - docs/videos/story-everyday-oxo-c10/script-source-notes.md
---

# Correct C10 OXO source HOLD and image prompts

## Why

草稿 PR #1689 的獨立逐句查核收據綁定舊版 script SHA `1A05017A9C6DF2A60365655975E00AC954AF799D2264C9E006F89B21449C2CB3` 與 visual JSON SHA `4241FC748B5FA81927EC81B3FAAF4BEC8AC332AA5893F7B2DC3C6CD240AE1CF9`，判 c100308 旁白及畫面、另八條圖片提示詞為 HOLD。這張修訂票只處理該收據的定點，讓新 bytes 可交同一獨立審查者做 delta review。

## Definition of done

- [x] c100308 不再暗示有紀錄的多位受訪者反覆試握泡棉模型；對應畫面不演成可考測試場面。
- [x] 全部 `shot.prompt` 沒有被禁的人名、品牌名、產品名或館名；八條 HOLD 及共通畫面契約都修正，閱讀版逐鏡同步。
- [x] 80／80 ID、來源歸屬、畫風與書擋等機械檢查通過，新版本雜湊及修訂差異推到同一草稿 PR，交獨立 delta review。

## Steps

- [x] 讀 [獨立收據](../../docs/videos/story-everyday-oxo-c10/reviews/independent-script-source-review.md) 的逐 ID 判定與來源界線，保留未點名的 79 句及分鏡。
- [x] 定點修改旁白、圖片 JSON、閱讀版逐鏡與來源說明；把原審查 PASS 與新 bytes 明確分開。
- [x] 驗 ID、prompt 名稱禁令、JSON 格式、任務板與差異；記 SHA，commit/push 同一 PR，轉 review。

## How to verify

PowerShell 解析 `visual-plan.json`，以正則檢查每一條 `shot.prompt`、80 個 ID 順序／唯一性、71 圖 9 卡和最長連卡 2；讀回 `script.md` 的 c100308，確認不指定測試參與者；比對 `visual-plan.md` 逐鏡文字；`npm run check:tasks`、`git diff --check`；最後用 `Get-FileHash -Algorithm SHA256` 綁定新稿。

## Notes

已把先前 `2026-10-22-write-c10-oxo-script-and-visual` 從 review 釋出為 open，解除重疊 scope 後認領本票；舊任務代表原稿交付歷史，不能把它的核對結果當新稿來源 PASS。修訂不涉及付費、TTS、站主核准、上架或發布。

上一輪 `npm run check:tasks` PASS。專屬機械檢查驗 80／80／80 ID 同序且無重號、71 `shot`、9 `stats`、最長連卡 2、`look`／書擋、逐鏡閱讀版與 JSON 文案一對一、全部圖片提示詞中禁用名稱 0 筆。這些舊 bytes 後來由獨立來源 delta 審查綁 SHA 判 PASS；不延伸到後續修訂。

## 2026-10-22 口播盲讀 HOLD 後續修訂

同一已認領的 C10 文件 scope 續處理 [Reader A 收據](../../docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v2-a.md)，而不是覆寫其判定。上一輪[獨立來源 delta](../../docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v2.md)在舊 SHA 上 PASS，本輪修改後須再獨立查核，兩位口播盲讀也須綁新 SHA。

- [x] c100508–513 讓胡蘿蔔展示有可聽的結果：按 2017 年品牌回顧，店家後來看見讓顧客現場試用的價值；不推試用造成銷售。
- [x] c100601–612 回收開場馬鈴薯與商店問題，減少館方清單；c100313、402、407、501 換成可口述的說法。
- [x] 80 句／80 鏡 IDs 對齊，逐鏡 JSON 與閱讀版同步，圖片提示詞保留無名稱規則；不改已採用企劃及來源矩陣。
- [x] 專屬機械檢查與 `git diff --check` 通過，記錄新 SHA，推回草稿 PR #1689；將舊收據列為歷史版本，交獨立 delta 與新盲讀。

本段仍只屬文字製作；未做 TTS、付費圖片／配樂或影片，也沒有站主稿件核准。

本輪專屬檢查：80／80／80 ID 同序無重號；71 `shot`、9 `stats`、最長連卡 2；閱讀版逐鏡與 JSON 逐條相同；全部 `shot.prompt` 及共通契約禁用名稱 0 筆；`look` 與 5／21 秒書擋正確。`git diff --check` 通過。`npm run check:tasks` 這次 exit 1，原因是此工作樹已有其他兩張審查任務的未追蹤 `tasks/open` 孤檔，和已追蹤的 `tasks/done` 同 ID；本票沒有動那些檔案，也不將此記作本票結構 PASS。廣泛的過期認領／scope 重疊只見 warning。

## 2026-10-22 v3 口播盲讀 HOLD 的窄化修訂

[v3 來源與逐鏡差異收據](../../docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v3.md)對舊 script SHA `67AC2AB3D054CC0023EC09A0EBC6124CE9DAC48E27B66D8E28CE649A3CE77980` 判 PASS；同 SHA 的[v3 口播盲讀 A](../../docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v3-a.md)判 HOLD。前者不能移植到本次新 bytes，後者指出開場承諾超過可證範圍及章尾問第二雙手卻由館方代答。

- [x] c100108 收窄為「如何讓人有機會親手試」，與 S4 的店內展示可直接對答。
- [x] c100507–514 保留胡蘿蔔試用，明講品牌回顧中的店家看見試用價值及後來示範延伸，不虛構買賣、銷量、特定顧客或另一雙手的實測；章末改問產品延伸。
- [x] c100601–612 用刀具與開罐器立即回答新章末問題，片尾回收握不住與貨架看不懂兩道阻力，對應卡片及鏡頭同步。
- [x] 完成 80 ID、提示詞禁名、閱讀版一致及差異檢查，記錄 SHA，推回草稿 PR 並轉 review；交另一代理重新綁 SHA 覆核來源及盲讀。Task board 的工作樹孤檔失敗另記，不算通過。

本次仍無 TTS、付費生成、站主稿件核准、匯入、上傳或發布。

本輪檢查：80／80／80 唯一 ID 同序；71 `shot`、9 `stats`、最長連卡 2；閱讀版與 JSON 0 列不符；全部 `shot.prompt` 和 `visual_contract` 禁用名稱 0 筆；`look` 及 5／21 秒書擋正確；`git diff --check` 通過。`npm run check:tasks` 仍 exit 1，這次是四張其他審查任務的未追蹤 `tasks/open` 孤檔與已追蹤 `tasks/done` 同 ID；沒有改動或清除那些檔案。舊 v3 來源 PASS 和盲讀 HOLD 都只對舊 script SHA `67AC2AB3D054CC0023EC09A0EBC6124CE9DAC48E27B66D8E28CE649A3CE77980` 生效，不能把新版自判通過。
