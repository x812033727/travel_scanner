---
id: 2026-10-22-write-and-review-c08-kikkoman-script
title: Write and review C08 Kikkoman script and visual plan
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-c08-script
claimed_at: 2026-10-22T05:29:04Z
created_at: 2026-10-22T05:28:57Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/script.md
  - docs/videos/story-everyday-kikkoman-c08/visual-plan.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/blind-reader-a.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/blind-reader-b.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/visual-preflight.md
---

# Write and review C08 Kikkoman script and visual plan

## Why

站主已採用 C08 龜甲萬桌上瓶企劃，核准收據綁定 Treatment 與來源矩陣的 SHA。下一關是把同一條設計問題寫成約十分鐘的六章旁白，逐句對可讀來源，再給兩位只看旁白的獨立讀者盲讀。畫面採奇聞檔案局的可愛示意插畫規則；所有本階段產物均不付費。

## Definition of done

- [ ] 六章逐句稿有 ID、來源代號和每 30–45 秒的具體鉤子，開場濃縮、章末接力、結尾三句完整；時長只以文字估算，TTS 尚未實測。
- [ ] 逐鏡表與每一句對應，含插圖／單焦點卡、匿名提示詞、運鏡、證據界線；插圖占比至少 70%，連續卡最多三張。
- [ ] 另一名代理逐句對可直接讀的來源查核，判定與 script／visual SHA 綁定；錯誤修後重新審。
- [ ] 兩名不同代理各自只看旁白盲讀，留下獨立且綁定稿件 SHA 的收據；視覺預檢另有收據。
- [ ] 檔案與任務檢查通過，草稿 PR 貼 no-auto-merge，供站主審劇本和逐鏡方向；不把企劃核准當劇本或付費核准。

## Steps

- [x] 核對 C08 Treatment 原 PR、現有任務與分支；從含站主企劃核准收據的提交建立獨立工作樹並認領窄票。
- [x] 依企劃與來源矩陣撰寫六章逐句旁白及逐鏡表。
- [ ] 獨立逐句來源查核、兩位盲讀、視覺預檢；需要修稿就重新綁定 SHA。
- [ ] 執行 check:tasks、diff check 與本集結構檢查，提交草稿 PR；保留站主劇本審核關卡。

## How to verify

讀 script.md 的每一行 ID 與「依」欄，逐項打開來源矩陣列出的直接可讀文件；計算 script.md、visual-plan.md SHA256，與三份獨立收據相對；機械檢查句 ID／鏡 ID 完整、插圖占比與連續卡上限。執行 npm run check:tasks 與 git diff --check。純文字字數估算不算實測 480 秒，正式旁白仍需另關卡。

## Notes

2026-10-22：Treatment 分支 codex/brand-story-kikkoman-c08-treatment 的 dd019ccf3 含站主企劃核准收據；本票工作樹從該提交切出。原企劃 PR #1678 維持草稿與 no-auto-merge。未找到 1955 原始調查、GK 委託書、完整原型台帳或 JPO 原始登錄；公司回顧、設計團隊與 MoMA 後來策展要分清。2018 年逾五億瓶是截至三月底的全球累計出貨，不能推成設計帶動銷量。

2026-10-22：初稿 92 句、92 鏡（79 shot／13 卡，按鏡數 85.9%，最多連續 2 卡）；ID 全對齊，提示詞未含品牌、人名與館藏禁字，沒有 3 連同運鏡。純文字約 2,700 字元，尚無 TTS 實長。已派與作者獨立的逐句來源查核代理；兩位真正盲讀與最終視覺預檢仍待完成。

2026-10-22：草稿 PR #1681 已開、維持 `no-auto-merge`。獨立來源查核者曾對 92／92 句及 13／13 卡判 PASS；作者其後把 `c080511` 卡改為單一 2005 年入藏焦點，`visual-plan.md` SHA 改變，原查核收據因此暫時失效，**HOLD 至同一獨立審查者核對並重綁 SHA**。作者技術預檢已寫；兩名只看旁白的盲讀代理尚未完成，不能稱劇本審查通過。結構檢查 92／92 ID 對齊、79／13、最長 2 連卡。`test:docs-videos` 在安裝缺少的依賴後有 235／236 PASS；唯一失敗在其他影片語言流程的 `package-runtime.mjs` Windows 子程序（status 3221226505）。低磁碟下停止後續大型測試；工作樹 `node_modules` 清理命令遭自動審查 `blocked by policy`，未刪除。
