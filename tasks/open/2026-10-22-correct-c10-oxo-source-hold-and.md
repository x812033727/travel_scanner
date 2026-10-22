---
id: 2026-10-22-correct-c10-oxo-source-hold-and
title: Correct C10 OXO source HOLD and image prompts
status: review
priority: P1
area: docs
owner: codex-c10-oxo-script
claimed_at: 2026-10-22T14:38:54Z
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

`npm run check:tasks` PASS。專屬機械檢查驗 80／80／80 ID 同序且無重號、71 `shot`、9 `stats`、最長連卡 2、`look`／書擋、逐鏡閱讀版與 JSON 文案一對一、全部圖片提示詞中禁用名稱 0 筆。獨立來源 delta 審查仍待新稿推送後重新綁 SHA，不由作者自判 PASS。
