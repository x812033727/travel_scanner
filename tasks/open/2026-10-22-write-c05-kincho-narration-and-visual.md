---
id: 2026-10-22-write-c05-kincho-narration-and-visual
title: Write C05 Kincho narration and visual plan
status: in-progress
priority: P2
area: docs
owner: codex-c05-kincho-script
claimed_at: 2026-10-22T03:39:41Z
created_at: 2026-10-22T03:39:36Z
completed_at:
branch: codex/brand-story-kincho-c05-script
depends_on: []
scope:
  - docs/videos/story-everyday-kincho-c05/script.md
  - docs/videos/story-everyday-kincho-c05/visual-plan.md
  - docs/videos/story-everyday-kincho-c05/video.json
  - docs/videos/story-everyday-kincho-c05/reviews/line-review.md
  - docs/videos/story-everyday-kincho-c05/reviews/narrative-reader-1.md
  - docs/videos/story-everyday-kincho-c05/reviews/narrative-reader-2.md
---

# Write C05 Kincho narration and visual plan

## Why

站主已採用 C05 金鳥螺旋蚊香的企劃方向，但 Treatment 不是可錄音的逐句稿。要把 1890 直條、1895 試作、1900 公司記載的專利申請、1902 上市、後來雙卷運送與現行產品串成一條可查核的故事，並在任何付費製作前交站主審劇本與畫面。

## Definition of done

- [x] 依採用的 Treatment 寫約 94 句六章旁白、每句固定 ID，附逐句來源對照與至少八個可回收的鉤子；來源不足就縮短，不用重述灌長。
- [x] 完成逐鏡畫面計畫，遵守奇聞檔案局的 MiniMax image-01／cute-mystery、插圖時間至少七成、卡片連續最多三張、片頭片尾及 CC 規則，不產生媒體。插圖時間占比仍須實測後核准。
- [ ] 不同代理逐句獨立來源查核；兩位未參與撰稿的讀者各自盲讀敘事，收據綁稿件雜湊與未解限制。
- [ ] 本次必要的非付費檢查通過，草稿 PR 報告結果，等站主另外核准劇本與逐鏡稿。

## Steps

- [x] 由 Treatment PR #1672 的核准版本開立獨立工作樹及 `codex/brand-story-kincho-c05-script`；查無另一人持有逐字稿路徑。
- [x] 讀規則及來源，寫六章旁白、逐句來源和視覺節拍。
- [ ] 獨立逐句查核、兩位盲讀後按具體意見修訂，再固定最終雜湊。
- [ ] 跑本次適用的檢查、提交並推送草稿 PR，記清下一道站主審核關卡。

## How to verify

核對 Treatment 與來源矩陣 SHA-256、逐句來源 ID、`script.md` 與 `visual-plan.md` 雜湊，以及獨立收據；跑 `npm run check:tasks`、`git diff --check` 和適用的影片 lint／`npm run test:docs-videos`。任何 lint 通過不等於站主劇本核准或已生成媒體。

## Notes

企劃與來源矩陣的核准雜湊分別為 `BBA52D1D55CE38560B8C7581EFCC7E739849468882C4FF91146F29F139A93C90`、`0939FD2ACEBF84FA8F84559F71C056BD8784E65BD4A875A03687F53B872CA1EA`；企劃 PR #1672 仍為草稿。這張票僅占逐字稿、畫面計畫及其審查收據的確切路徑，不改 Treatment／來源矩陣，也不動 C03、C04。專利原件、1889 年優先權與妻子構想的獨立同時期證據仍缺；旁白要按來源歸屬表述。

2026-10-22 草稿進度：94 句、69 個畫面狀態，52 shot／17 card；每句恰有一個畫面對應，連續卡片最多 2 張。這只是狀態數，**不能**替代成片插圖時間至少 70% 的檢查。旁白 1,649 字元，照專案每分鐘約 250 字的規劃值僅約 6.6 分鐘，離純語音 8 分鐘門檻有實質落差；目前材料不能合理補足，**劇本／逐鏡不具付費製作核准資格**。不靠停頓、重複或旁支史料補時；下一步由站主審短片方向或改題，再重做長度與成本評估。

兩位初讀者都讀完整六章、認為主線可追，但指出 E18–E19 的 1940／1957 年跳到 T06–T11 的 1919–1940 年，以及展品／海報段拖慢動作主線；一位誤讀來源欄，該份不能作嚴格盲讀收據。正式來源逐句覆核與最終敘事收據仍在進行。`npm run test:docs-videos` 為 235/236 PASS；唯一失敗是 `docs/videos/imported-long-languages/runner.test.mjs:679` 的 Windows 子行程 3221226505／無 stderr，與本次純文件編輯無關；`npm run check:tasks` 通過。
