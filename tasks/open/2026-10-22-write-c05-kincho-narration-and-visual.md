---
id: 2026-10-22-write-c05-kincho-narration-and-visual
title: Write C05 Kincho narration and visual plan
status: review
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

- [x] 依採用的 Treatment 寫六章旁白（現為 88 句短稿）、每句固定 ID，附逐句來源對照與至少八個可回收的鉤子；來源不足就縮短，不用重述灌長。
- [x] 完成逐鏡畫面計畫，遵守奇聞檔案局的 MiniMax image-01／cute-mystery、插圖時間至少七成、卡片連續最多三張、片頭片尾及 CC 規則，不產生媒體。插圖時間占比仍須實測後核准。
- [x] 不同代理逐句獨立來源查核；兩位未參與撰稿的讀者各自盲讀敘事，收據綁稿件雜湊與未解限制。
- [x] 本次必要的非付費檢查與已知失敗都記入草稿 PR；等長度與敘事問題修正後，再交站主審劇本與逐鏡稿。

## Steps

- [x] 由 Treatment PR #1672 的核准版本開立獨立工作樹及 `codex/brand-story-kincho-c05-script`；查無另一人持有逐字稿路徑。
- [x] 讀規則及來源，寫六章旁白、逐句來源和視覺節拍。
- [x] 獨立逐句查核、兩位嚴格盲讀，按首輪具體意見修訂；把本輪未解的節奏意見留下，不冒稱定稿。
- [x] 跑本次適用的檢查、提交並推送草稿 PR #1675，記清下一道站主審核關卡。

## How to verify

核對 Treatment 與來源矩陣 SHA-256、逐句來源 ID、`script.md` 與 `visual-plan.md` 雜湊，以及獨立收據；跑 `npm run check:tasks`、`git diff --check` 和適用的影片 lint／`npm run test:docs-videos`。任何 lint 通過不等於站主劇本核准或已生成媒體。

## Notes

企劃與來源矩陣的核准雜湊分別為 `BBA52D1D55CE38560B8C7581EFCC7E739849468882C4FF91146F29F139A93C90`、`0939FD2ACEBF84FA8F84559F71C056BD8784E65BD4A875A03687F53B872CA1EA`；企劃 PR #1672 仍為草稿。這張票僅占逐字稿、畫面計畫及其審查收據的確切路徑，不改 Treatment／來源矩陣，也不動 C03、C04。專利原件、1889 年優先權與妻子構想的獨立同時期證據仍缺；旁白要按來源歸屬表述。

2026-10-22 草稿 PR #1675：88 句、65 個畫面狀態（50 shot／15 card）；每句恰有一個畫面對應，連續卡片最多 2 張。`script.md` SHA-256 `7D07A7A12478E4956B1DA110819F9C30514BA0C52DA007868F8644A401D78980`；`visual-plan.md` SHA-256 `7A7068BF5E38E0784EBA4A7DEA93A36FC0A3B988AC64F5B3750EA6FABBD117C3`。插圖 76.9% 只是狀態數，**不能**替代成片畫面時間至少 70% 的檢查。旁白 1,548 字元，照專案每分鐘約 250 字的規劃值僅約 6.19 分鐘，離純語音 8 分鐘至少差約 452 字元；目前材料不能合理補足，**劇本／逐鏡不具付費製作核准資格**。不靠停頓、重複或旁支史料補時；下一步由站主決定可否改為短片，或改題再寫，之後重新估價與審核。

獨立查核者已對此稿 88 句逐句 PASS，並查畫面物件；兩位嚴格盲讀者都認為主線與回收可追，但指出 T05–T08 揭曉重複、T12 提問到 N09–N11 答案間隔、N14–N16 收尾太像摘要／制式邀請，與 E18–E19 的工法年代轉場可再修。這些是下一版劇本問題，**不是**可付費的通過票。初輪曾有讀者誤看來源欄，另一份超讀鉤子表，均未列為兩份正式嚴格盲讀收據。來源矩陣 F08 尚有「兩條同時押出」的勘誤需求，應回 Treatment PR #1672 受控修正並重綁採用雜湊；本稿只採原件較窄的說法。

`npm run check:tasks` 通過，稿件 ID／畫面映射與連續卡片機械檢查通過，`git diff --check` 通過。`npm run test:docs-videos` 為 235/236 PASS；唯一失敗是 `docs/videos/imported-long-languages/runner.test.mjs:679` 的 Windows 子行程 3221226505／無 stderr，與本次純文件編輯無關，且在 Treatment 工作樹重現。沒有生成圖片、音訊、影片，也沒有任何付費請求。PR 保持草稿及 `no-auto-merge`；票留在 `review`，未併入不得 `done`。
