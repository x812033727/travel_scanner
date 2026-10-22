---
id: 2026-10-22-plan-c07-dr-martens-work-boot
title: Plan C07 Dr. Martens work-boot reversal
status: review
priority: P2
area: docs
owner: codex-gpt6-c07-treatment
claimed_at: 2026-10-22T04:20:28Z
created_at: 2026-10-22T04:20:24Z
completed_at:
branch: codex/brand-story-dr-martens-c07-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/treatment.md
  - docs/videos/story-everyday-dr-martens-c07/source-matrix.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/source-review.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/owner-treatment-approval.md
---

# Plan C07 Dr. Martens work-boot reversal

## Why

C07 已在「日用品的意外轉身」20 集順序中排為 Dr. Martens，但還沒有可核准的 Treatment。要先查清工作靴如何被不同青年文化採用，再決定是否有足夠證據與故事容量寫成約十分鐘長片；不能把品牌回顧當成獨立的同時期紀錄，也不能把不同年代的次文化混成一群。

## Definition of done

- [x] 六章 Treatment 提出一條可追的因果主線、濃縮開場、每章剪點、縮圖方向與時長容量；品牌字及真人／版權角色不進圖片提示詞。
- [x] 來源矩陣逐項列出可讀的一手入口、獨立文化史來源、未找到的原件及不能推論的因果；招股書 PDF 若超過工人直接讀取限額須標審稿人專用。
- [x] 另一位代理逐來源核對，留下綁定 Treatment 和來源矩陣雜湊的審查收據，修掉實質錯誤。
- [ ] 草稿 PR 供站主審企劃；在企劃核准前不寫逐字稿、不買圖片／配音／配樂、不上傳或發布。

## Steps

- [x] 確認 20 集名單中的 C07 題目、同題檔案／任務／遠端分支／PR 無權屬衝突，建立獨立工作樹並認領窄範圍任務。
- [x] 撰寫六章 Treatment 與來源矩陣，核實官方可讀沿革、1460 品牌檔案及獨立博物館論述；招股書 PDF 標 reviewer-only，未讀內文不當證據。
- [x] 派另一代理獨立逐來源查核；依查核結果修訂與重綁雜湊。
- [ ] 執行文件與任務檢查、提交草稿 PR 並貼 `no-auto-merge`；維持 review 等站主審企劃。

## How to verify

`npm run check:tasks`、`git diff --check`；來源網址可讀性與內容逐項對 Treatment 和來源矩陣；查核收據的 SHA256 與目前檔案一致。草稿 PR、付費媒體、上傳、發布及站主採用方向各自是不同狀態。

## Notes

2026-10-22：主線暫定「德國緩震鞋底 → Griggs 取得英國授權並改成 1960 年 1460 工作靴 → 青年自行賦予階級與文化意義 → 公司後來把文化記憶寫進品牌」。官方 [IPO 招股書](https://www.drmartensplc.com/application/files/9116/1191/9428/Dr._Martens_plc_-_Prospectus.pdf)、[1460 檔案](https://www.drmartens.com/uk/en_gb/archive/1460)及獨立 [V&A 文章](https://www.vam.ac.uk/blog/museum-of-childhood/dr-martens-dips-toe-into-new-market)是待逐頁核實的入口；先別把「第一款」「所有青年都穿」「某場表演帶動銷量」寫成定論。1960 年代多族裔 ska／早期 skinhead 與後來極右挪用必須分期，不拿後者替代前者。C03–C06 的稿件與額度核准均不移轉到 C07。
