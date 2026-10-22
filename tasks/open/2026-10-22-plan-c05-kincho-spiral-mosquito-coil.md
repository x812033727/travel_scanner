---
id: 2026-10-22-plan-c05-kincho-spiral-mosquito-coil
title: Plan C05 Kincho spiral mosquito coil story
status: review
priority: P2
area: docs
owner: codex-c05-kincho
claimed_at: 2026-10-22T03:23:51Z
created_at: 2026-10-22T03:23:46Z
completed_at:
branch: codex/brand-story-kincho-c05-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-kincho-c05/treatment.md
  - docs/videos/story-everyday-kincho-c05/source-matrix.md
  - docs/videos/story-everyday-kincho-c05/reviews/source-review.md
  - docs/videos/story-everyday-kincho-c05/reviews/owner-treatment-approval.md
---

# Plan C05 Kincho spiral mosquito coil story

## Why

「日用品的意外轉身」第 1 批的 C05 題目已列金鳥螺旋蚊香，但原清單只是取證入口。前兩集已有本機試片、C04 已進逐字稿；C05 需要自己的非付費企劃與來源查核，才能讓站主審方向。舊的品牌故事 100 題庫另有同代號 C05（Ctrl+Alt+Del），不得共用 slug、收據或核准。

## Definition of done

- [x] C05 有獨立的六章 Treatment、一條因果主線、開場與鉤子草圖、標題與縮圖假設，並明列奇聞檔案局畫面規則。
- [x] 一手來源矩陣逐項區分 1895 試作、1900 年公司記載申請、1902 年上市及現行產品，標示企業回顧與缺口。
- [x] 另一代理對固定雜湊的企劃與來源矩陣獨立覆核；審查結果已寫入 reviews/source-review.md。站主已採用企劃方向，核准範圍見 reviews/owner-treatment-approval.md；本票沒有劇本、付費生成、匯入或發布。

## Steps

- [x] 從新系列分支開立獨立工作樹和 codex/brand-story-kincho-c05-treatment 分支；本票只占 docs/videos/story-everyday-kincho-c05。
- [x] 讀 brand-story、youtube-video/story、curio-episode 與一手資料，起草 Treatment、來源矩陣。
- [x] 獨立代理核對 Treatment 與矩陣，保存內容雜湊、判定與未解風險。
- [x] 執行本次涉及的非付費檢查，提交草稿 PR #1672 等站主審方向。

## How to verify

在本工作樹執行 npm run check:tasks 及 npm run test:docs-videos；以 Get-FileHash -Algorithm SHA256 固定 treatment.md、source-matrix.md 版本，核對另一代理的獨立審查。這次沒有 episodes/C05.json 或 video.json，影片 lint、付費估價、TTS 與成片 QA 不適用。

## Notes

2026-10-22：基底是 origin/codex/brand-stories-new-series-20261020 的 f80204ff5；origin/main 尚無 20 集企劃，C04 PR #1668 也以新系列分支為 base。專屬工作樹是 C:\Users\x8120\.codex\worktrees\brand-story-kincho-c05-treatment\travel_scanㄐ；未碰 C03/C04 的文件或媒體。

已查金鳥年表、技術遺產頁、產品 Q&A、2017 年公告及署名文章、國立科學博物館的 1895 年木模登錄、國立公文書館的 1943 年授勳卷宗介紹。年表分列 1895 構想、1900 申請、1902 上市；原始 1900 申請件未取得。2017 年公司資料稱早期螺旋約六小時，現行一般規格 Q&A 稱約七小時；不得混為同一產品或推成效力倍數。

獨立來源調查代理提醒：兩名日本專利師指出可能有更早的 1889 年「蚊遣香」特許第 825 號，但本輪未讀到日本特許廳原件。暫不說上山「發明世界第一支蚊香」，也不把該線索寫成已證實的反駁。妻子ゆき的構想依金鳥回顧歸屬；公文書館摘要歸功於上山英一郎，沒有當年逐字證詞。六章可否承載至少八分鐘仍是下階段逐字稿前的證據容量關卡，不靠重述灌長。

獨立代理先判 REVISE，要求移除當下無正文的 Good Design 來源、將僅見 PDF 的早期「六小時」標為 reviewer_only 或刪除、拆開螺旋的長度效果與後來雙卷的運送效果。修訂後對 treatment.md SHA-256 BBA52D1D55CE38560B8C7581EFCC7E739849468882C4FF91146F29F139A93C90、source-matrix.md SHA-256 0939FD2ACEBF84FA8F84559F71C056BD8784E65BD4A875A03687F53B872CA1EA 回報 PASS；收據在 docs/videos/story-everyday-kincho-c05/reviews/source-review.md。這只核准企劃來源界線，不是站主決定。

2026-10-22：草稿 PR #1672（https://github.com/x812033727/travel_scanner/pull/1672）堆疊在新系列草稿 PR #1610，等待站主審本集企劃方向。npm run check:tasks 通過（僅有其他任務的既存 stale／scope 重疊警告）；git diff --cached --check 通過。首次 npm run test:docs-videos 因新工作樹缺少 pinyin-pro 失敗；npm ci 後重跑為 236 測試中 235 通過、1 失敗，失敗在未修改的 docs/videos/imported-long-languages/runner.test.mjs 第 679 行，子程序 package-runtime.mjs 在 Windows 以狀態 3221226505 無 stdout/stderr 結束。本次只有 C05 Markdown 與票；沒有動那組程式或付費媒體。後續若要追全套測試紅燈，依原組件另案處理，不混進 C05 來源審核。

2026-10-22：站主採用本集企劃方向，精確綁定 treatment.md `BBA52D1D55CE38560B8C7581EFCC7E739849468882C4FF91146F29F139A93C90` 與 source-matrix.md `0939FD2ACEBF84FA8F84559F71C056BD8784E65BD4A875A03687F53B872CA1EA`。正式收據在 docs/videos/story-everyday-kincho-c05/reviews/owner-treatment-approval.md。下一張獨立票只做非付費逐句旁白、畫面規劃及獨立審稿；劇本與付費生成仍待分別審批。

本票維持 `review`，因草稿 PR #1672 尚未合併；範圍收窄為本票實際修改的四個檔案，好讓新票獨立持有劇本檔。一次錯誤的 `tasks done` 在本機先寫出未追蹤的 `tasks/done/2026-10-22-plan-c05-kincho-spiral-mosquito-coil.md`，卻因 Windows 檔案占用未能移除 `tasks/open/` 原件；精確刪除又遭工具政策拒絕。未追蹤的本機重複票不會提交，直到政策允許安全清理；乾淨工作樹另行驗證看板。
