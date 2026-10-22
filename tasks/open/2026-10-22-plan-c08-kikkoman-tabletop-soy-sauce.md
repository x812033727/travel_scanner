---
id: 2026-10-22-plan-c08-kikkoman-tabletop-soy-sauce
title: Plan C08 Kikkoman tabletop soy sauce story
status: review
priority: P2
area: docs
owner: codex-gpt6-c08-treatment
claimed_at: 2026-10-22T04:33:12Z
created_at: 2026-10-22T04:33:08Z
completed_at:
branch: codex/brand-story-kikkoman-c08-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/treatment.md
  - docs/videos/story-everyday-kikkoman-c08/source-matrix.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/source-review.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/owner-treatment-approval.md
---

# Plan C08 Kikkoman tabletop soy sauce story

## Why

C08 在「日用品的意外轉身」排定為龜甲萬桌上醬油瓶，但目前只有題目和待查入口。要先證明大瓶、倒入桌上容器、1955 年小瓶與 1961 年新設計的先後關係，再判斷「從儲存容器到餐桌用品」是否有足夠的一手與獨立來源支撐長片；不能把設計成功直接寫成銷量原因。

## Definition of done

- [x] 六章 Treatment 有一條可追的設計問題、試作、推出、後來識別的主線，含濃縮開場、約十分鐘容量、章末問題與奇聞檔案局畫面規則。
- [x] 來源矩陣逐項區分公司、設計團隊、獨立館藏與獎項資料，列出可直接核對的事實、未找到的原件及不得推論的銷售因果。
- [x] 由另一代理獨立覆核並產生綁定 Treatment 與來源矩陣 SHA256 的收據；實質錯誤修正後再請站主審方向。
- [x] [草稿 PR #1678](https://github.com/x812033727/travel_scanner/pull/1678) 僅供站主審企劃；在本集企劃核准前不寫逐字稿、不付費生成、不上傳或發布。

## Steps

- [x] 確認 C08 題目與既有任務、分支、PR、工作樹沒有同題權屬衝突；建立獨立工作樹並認領窄範圍任務。
- [x] 撰寫 Treatment 與來源矩陣，核對公司沿革、GK 設計紀錄、MoMA 1961 館藏物件及 2018 年立體商標文件。
- [x] 派另一代理獨立逐來源查核，依查核結果修正並重新綁定雜湊。
- [x] 執行文件和任務檢查，提交草稿 PR 並貼 `no-auto-merge`，維持 review 待站主審企劃。

## How to verify

`npm run check:tasks`、`git diff --check`，加上來源頁逐項對 Treatment 與來源矩陣、審查收據 SHA256 與目前文件一致。Treatment、企劃核准、逐句稿、付費生成與上架各是不同關卡；規劃時長不等於 TTS 或成片實長。

## Notes

2026-10-22：C08 在新系列清單中的題目是「龜甲萬：醬油瓶怎麼走上餐桌？」；舊 `brand-stories-100/stories/C08.json` 是 emoji，僅代號相同。龜甲萬題也曾在未核准備選 `reserve.json`，不是另一支已開工影片。查無同題活躍任務、遠端分支與開啟 PR。核心可讀資料是 [龜甲萬 2020 年回顧](https://www.kikkoman.com/en/culture/foodforum/today/20200327.html)、[GK 設計團隊檔案](https://www.gk-design.co.jp/en/archives/history/2242/)、[MoMA 1961 年館藏物件](https://www.moma.org/collection/works/90106)及[龜甲萬 2018 年新聞稿](https://cdn.kyodonewsprwire.jp/prwfile/release/M103831/201804162969/_prw_PR1fl_58lMXR0V.pdf)。公司 2020 年資料的五億瓶是截至 2018 年 3 月的累計**出貨**，不是淨銷售或瓶形帶動成長的因果；MoMA 的「近百個模型」是策展回顧，不是完整試作台帳。C03–C07 的任何核准或 US$25 額度都不移轉到 C08。

2026-10-22：已寫六章 [Treatment](../../docs/videos/story-everyday-kikkoman-c08/treatment.md) 與[來源矩陣](../../docs/videos/story-everyday-kikkoman-c08/source-matrix.md)，兩檔仍待獨立逐來源審查和站主企劃核准。日本特許廳商標原始登錄、當年顧客調查與完整試作台帳未找到；正式逐字稿不可把 2018 年公司累計出貨稱作銷量因果。

2026-10-22：獨立來源審查先判 REVISE，指出龜甲萬 2020 年 HTML 與年表 HTML 直接抓取 timeout／503；已以同篇可讀官方 PDF 支持 1955 年、一公升與三年多試作，另以可讀官方環境 PDF 支持 1961 年 150ml，1991 年 100ml 的年表條目降為 reviewer-only。瓶口用語改成「少滴」，不保證絕不滴漏。第二輪企劃來源審查 PASS，收據在 [reviews/source-review.md](../../docs/videos/story-everyday-kikkoman-c08/reviews/source-review.md)，只適用本版企劃；正式逐字稿仍須逐句查核。站主尚未核准 C08 方向。

2026-10-22：已建立草稿 [PR #1678](https://github.com/x812033727/travel_scanner/pull/1678)，以新系列分支為 base，貼 `no-auto-merge`，等待站主採用或修訂方向。`npm run check:tasks` 與 `git diff --cached --check` 通過；沒有 C08 付費媒體、上傳或發布。
