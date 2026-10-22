---
id: 2026-10-22-write-and-review-c08-kikkoman-script
title: Write and review C08 Kikkoman script and visual plan
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T05:28:57Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/script.md
  - docs/videos/story-everyday-kikkoman-c08/visual-plan.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-pre-rewrite.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-pre-blind-fix.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-pre-final-pass.md
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

2026-10-22：C: 回升至 19.34 GiB 後接續原工作樹，**未重裝依賴**。92 句定向修訂：第 2／3 章改以放穩、握取接力，瓶口解法留到第 4 章揭曉；第 5 章改問設計界後來如何注意，不再用設計評價回答購買成因；第 6 章先解釋累計出貨口徑，再回到無字外形與最後一滴。逐鏡同步更新，仍是 92／92 ID、79 插圖方向／13 卡、最長 2 連卡。現版 `script.md` SHA-256 `3EEB08795352580764527B9211C65C511A5D5705931335C0757857835FB145F4`，`visual-plan.md` SHA-256 `DB0122E5036F20FBD3A8D9543C545D877D477254937B8B9461A8C0F28BDFAA50`；**本機未提交的舊版來源 PASS 收據綁的是舊 SHA，不能當現版通過**。下一關仍需獨立代理對修訂句、卡片與畫面重查，之後兩位只看旁白欄位的真正盲讀。

2026-10-22：舊版來源審查已保存為 `reviews/line-source-review-20261022-pre-rewrite.md`，頁首明確標失效。`npm run check:tasks` 通過（2076 張票，既有持有者／範圍警告）；`git diff --check` 通過。完整 `test:docs-videos` 因工作交接提前中止，沒有本輪完整結果；前輪 235／236 PASS 與其他影片語言流程的 Windows 子程序退出碼 3221226505 只作歷史背景，不當本輪綠燈。

2026-10-22：另一代理 `codex-c08-independent-source-review` 重新直接核對 K1、K2a、K3、D1、M1、G1 的原發行者文件，對**現版** 92／92 句旁白、92／92 列畫面及 13／13 張資料卡判 **PASS（來源與畫面事實界線）**。新收據 `docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review.md` 綁 `script.md` SHA-256 `3EEB08795352580764527B9211C65C511A5D5705931335C0757857835FB145F4` 與 `visual-plan.md` SHA-256 `DB0122E5036F20FBD3A8D9543C545D877D477254937B8B9461A8C0F28BDFAA50`。空白問卷／帳冊／出貨圖僅能作資訊缺口示意，後製不可當已找到的原件。這一關不包含兩名旁白盲讀、獨立美術預檢、TTS 時長、付費或站主劇本核准；任一稿件改動即須重新綁定審查。

2026-10-22：一位**只看旁白**的獨立讀者退回 `c080310–317`／`c080401–409` 的反覆倒取說明、`c080503–506` 的包裝轉工具重述、`c080605–611` 的出貨數字鋪墊，以及 `c080612–614` 可能暗示瓶嘴造成商標註冊的相鄰敘述。作者依此重寫，仍保留 92／92 ID、79 shot／13 卡、最多 2 連卡；K2a 的可再填充與 K3 的約百國均由原發行者文件直接支持，仍須獨立複核。現版 `script.md` SHA-256 `08539F264C5B228805AE9EF3E219E1DF81C10FE9853301A8441B5B25F510BF78`，`visual-plan.md` SHA-256 `04C554C4BDDEE9E37D7D76EA226CF0BA592E41D5365225D68F529F89F514F571`。先前 PASS 收據已存為 `reviews/line-source-review-20261022-pre-blind-fix.md` 並標失效；`line-source-review.md` 預留給新 SHA 的獨立查核。這位盲讀者的 HOLD 不是新稿的通過收據；需先重查來源，再找兩位新讀者只看旁白欄位重讀。

2026-10-22：獨立代理 `codex-c08-delta-source-review` 重新打開 K1、K2a、K3、D1、M1、G1 原發行者資料，逐句與同 ID 畫面核對現版 92／92 列，**來源和事實界線 PASS**。新 `reviews/line-source-review.md` 綁上段兩個現版 SHA；重點確認可再填充、約百國餐桌及全球累計出貨的原文，並把抽象倒取示意與尚未取得的問卷、模型、帳冊、JPO 原件分開。兩名新讀者盲讀、美術預檢、TTS 與站主稿件核准仍待完成，沒有付費生成。

2026-10-22：真正只看旁白的新盲讀者指出 `c080515` 問「觀眾能否認出無字瓶形」，但 `c080602–604` 只能回答公司所述的日本立體商標註冊；`c080509/514/610` 又重複提醒購買因果。作者將章末問題收窄到**無字樣與圖案的容器外形可否註冊**，保留公司公告與未查 JPO 原件界線；`c080514` 改接瓶形，`c080610` 只說全球累計出貨與零售成交的口徑差。僅修 `c080514–516`、`c080601–602`、`c080610` 旁白和 `c080514` 畫面，保留 92 ID、79 shot／13 card。現版 `script.md` SHA-256 `E2AA781EBB041CBB5A844271540ABB479858E5477FFA51802E8D723E6CAD4474`，`visual-plan.md` SHA-256 `1AA2AF927AD3C2FEBCEECF32A90316539913A242C277F760B03F0EB47323A2CA`。前版獨立 PASS 只綁舊 SHA，已保存為 `reviews/line-source-review-20261022-pre-final-pass.md` 並在原收據標失效；須重新獨立查核，另待兩名新盲讀與獨立美術預檢，不能宣稱稿件已通過。
