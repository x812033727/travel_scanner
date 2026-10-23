---
id: 2026-10-23-c16-bialetti-script-independent-review
title: Independently review C16 script sources and paired visuals
status: review
priority: P1
area: docs
owner: codex-c16-independent-script-review
claimed_at: 2026-10-23T03:35:30Z
created_at: 2026-10-23T03:35:24Z
completed_at:
branch: codex/brand-story-bialetti-c16-script
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/independent-script-source-visual-review.md
---

# Independently review C16 script sources and paired visuals

## Why

草稿 PR #1704 的 C16《Bialetti》已有 85 句旁白、85 筆配鏡與作者自查；上線前仍需要非作者對精確 Git blob 版本獨立逐句核讀，尤其要避免洗衣鍋傳說、1950／1951 年登記、鬍子角色身分和未定發明權屬被畫面或旁白說成確定歷史。

## Definition of done

- [x] 在本 task 的窄 scope 寫出以 head、SHA-256 和一手來源定位的獨立 PASS 或精確 HOLD 收據，列出所有 85 句及 85 鏡覆蓋。
- [x] 將需要作者修訂的句／鏡逐 ID 定位，保留其他核讀結論及 M16／M17 未決界線。

## Steps

- [x] 直接閱讀 Treatment、來源矩陣、逐字稿、逐句來源註記、JSON 與 Markdown 逐鏡，以及可讀的一手館藏、公司、圖錄和原論文。
- [x] 從 PR head 的 Git blob bytes 重算四份輸入雜湊，逐 ID 比對旁白、JSON 與 Markdown，出具獨立收據。

## How to verify

收據：`docs/videos/story-everyday-bialetti-c16/reviews/independent-script-source-visual-review.md`。核讀 head：`883359dbaaf8e76ed84dcb63521b048e760d616e`。原始 bytes 用 `git show HEAD:<path>` 輸入 Python `hashlib.sha256`；85 個 ID 順序及兩種逐鏡列內容用 Python 讀檔比對。七鏡 HOLD 為 `c160106`、`c160508`、`c160510`、`c160511`、`c160602`、`c160604`、`c160605`。`npm run check:tasks` 應通過。

## Notes

語音 85/85 來源及企劃邊界 PASS；視覺 78/85 PASS、7/85 HOLD。1957 年原件是雜誌第 16 頁印刷廣告，畫面不能讓觀眾以為是有據的展場直立海報；MoMA 2008 和 Museo Omero 1956 是兩館各自的館藏紀錄，不能畫成同場展櫃。MoMA 目前頁面標 `Not on view`。作者修訂視覺 JSON／Markdown 後需新雜湊和另一輪覆核。沒有編輯作者四份檔案、購買媒體、合併或發布。

2026-10-23 差異覆核：作者新 head `4501a630481d7399c598103c5310f14451f41b84` 的原七鏡均修至 PASS；逐鏡檢查相鄰 `c160606–609` 時另找到 `c160607` 仍用空白海報代表唯一已定位的 1957 雜誌廣告，故整體改為 85/85 句 PASS、84/85 鏡 PASS、1/85 鏡 HOLD。詳見同一收據的差異覆核段。等待作者只修 `c160607` 並提供新 head／視覺雜湊。

2026-10-23 最終差異覆核：作者 head `3d569b59133241f764263897c36fc1a0084db557` 僅改 `c160607` 兩份視覺檔，海報已改為無字雜誌頁；旁白／逐句註記 blob 不變、85/85 Markdown／JSON 鏡頭同序同內容。收據已加精確 blob hashes，最終裁決 85/85 句來源 PASS、85/85 鏡文案 PASS。此 task 維持 `review`，待 PR 後續流程；站主核稿與付費生成是其他關卡。
