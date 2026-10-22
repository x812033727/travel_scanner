---
id: 2026-10-22-write-and-review-c08-kikkoman-script
title: Write and review C08 Kikkoman script and visual plan
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-c08-final-revision
claimed_at: 2026-10-22T12:24:20Z
created_at: 2026-10-22T05:28:57Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/script.md
  - docs/videos/story-everyday-kikkoman-c08/script-source-addendum.md
  - docs/videos/story-everyday-kikkoman-c08/visual-plan.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-pre-rewrite.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-pre-blind-fix.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-pre-final-pass.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-pre-flow-fix.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-shortened.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-expanded.md
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-c080419-delta.md
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

讀 script.md 的每一行 ID 與「依」欄，逐項打開來源矩陣和 script-source-addendum.md 列出的原發行者文件；計算 script.md、visual-plan.md、R1 補充 SHA256，與新一輪獨立收據相對。機械檢查句 ID／鏡 ID 完整、插圖占比與連續卡上限。執行 npm run check:tasks 與 git diff --check。純文字字數估算不算實測 480 秒，正式旁白仍需另關卡。

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

2026-10-22：獨立代理 `codex-c08-delta-source-review` 比對最後一輪差異，重開 K3 原新聞稿、MoMA 館藏頁與 G1 主辦展品清單，對改動的六句旁白及一列畫面判 **PASS（來源／畫面事實界線）**；未改的 86 句與 91 列沿用前版逐句來源審查。新 `reviews/line-source-review.md` 綁本版兩檔 SHA。92／92 ID 對齊、79 shot／13 card、最多兩連卡與提示詞禁字檢查通過。兩位最終盲讀、獨立美術評審、實際旁白時長及站主劇本核准仍待處理，不涉及付費。

2026-10-22：新盲讀指出第 3 章末承諾「控制流量與少滴」兩邊都解釋，第 4 章的來源與旁白卻只說明瓶嘴內收切面如何減少積液和滴落；同處的事後回顧界線又重複。作者逐一核對 92 句的提問與回收：`c080101/105` → `c080310–312/410–416`；`c080107` → `c080515/601–604`；`c080108` → `c080501–506/614`；`c080214` → `215`、`c080216` → `c080301–313`；`c080304` → `306–309`、`c080317` → `c080410–412`；`c080401` → `402`、`c080408` → `409–411`、`c080417/419` → `c080501–503`；`c080507` → `508–513`、`c080515` → `c080601–604`；`c080607` → `608–610`、`c080611` → `612–614`。`c080615` 是開放留言題。現稿將瓶嘴承諾收窄到 MoMA M1 與設計團隊 D1 能說明的**少積液、少滴**；`c080404` 集中說明館方多年後敘述與缺少逐件原型，`c080413` 只限定效果而不重述資料缺口。第 1 章形狀伏筆也改指可查的公司商標公告。現版 `script.md` SHA-256 `ED7CDBFAB7588F6D3B69A4FC6E4740EAAB349567CE9ADB80493EA0FB5FF14868`；`visual-plan.md` SHA-256 `D696E6A3633E1C8C79FE3AF2B727FF51961E0B2A5ADC9E3EA90002875D3817F2`。前版 PASS 存為 `reviews/line-source-review-20261022-pre-flow-fix.md`，並於原收據標失效；本版需新獨立來源查核、視覺預檢、兩位新盲讀與站主核准，均尚未付費。

2026-10-22：獨立代理 `codex-c08-delta-source-review` 直接重開 MoMA M1、GK D1、龜甲萬 K1/K3，逐句核對這輪 15 句瓶嘴／開場修訂及 3 鏡倒取畫面，判 **PASS（來源與畫面事實界線）**；77 句與 89 鏡未改內容沿前版獨立來源收據。新 `reviews/line-source-review.md` 綁上段現版兩檔 SHA，明確不聲稱已證實最終流量控制、零滴漏、銷售效果或逐件實驗次序。92／92 ID 對齊、79 shot／13 card、最多兩連卡、生成 prompt 禁字檢查通過。最終兩名盲讀、獨立美術預檢、TTS 實長和站主稿件核准仍未完成；無付費製作。

2026-10-22：第二位嚴格盲讀對上述版本判 **HOLD**：`c080410–411` 的嘴尖內斜和積液作用難以在腦中成像；`c080405–408` 重述 `c080311–317`；`c080508–613` 的獎項、館藏、商標、出貨堆疊拖慢結尾，`c080612–614` 又重說功能解答。作者重新打開 MoMA M1、GK D1、龜甲萬 K1/K3 與 Treatment，只用來源可支持的「嘴尖向內斜／較少積液和滴桌」重寫第 3–4 章；畫面 `c080410` 改成僅標角度的泛用側面示意，移除液體回流路徑。結尾保留 2005 館藏與 2018 公司商標公告，1993 設計選定及全球累計出貨留在來源矩陣，不進旁白；以一次拿起、倒出、放回回答開場。現版 79／79 句與鏡 ID 對齊、68 shot／11 card（86.1%）、最多兩連卡、無缺號與生成 prompt 禁字；純文字 2,065 字元，**TTS 尚未實測**。`script.md` SHA-256 `36BC6272BBFF8FC82FF3E9EB68901D5140AF23332AA2FEBD420763A2C6E2CE85`，`visual-plan.md` SHA-256 `B56CA7071222E0CDC2A35C7ED3F0231B6C5615299F34ADFBF39F58F1D97F27C8`。前版來源 PASS 已標為歷史失效。作者只完成自檢；**須由不同代理重新做來源查核、兩位只看旁白的新盲讀及獨立視覺預檢**，站主劇本核准另待處理。未付費、未上傳。

2026-10-22：79 句縮稿的獨立來源審查判 **HOLD**，指出當時 `c080405` 把近百模型的雙重難題過度縮成收手一瞬間；同一收據另指出第 2–6 章 1,857 字元可能不足 480 秒，已標為歷史失效。作者重新核對 MoMA M1、GK D1、Kikkoman K1/K2a 及 Treatment，改寫為**防滴與控制流量並列要求**，僅把嘴尖內收角度連到 MoMA 明說的少積液、少滴；沒有最終流量量測或零滴漏保證。新增的因果資訊包含 1918 年 1.8 L 回收再用大瓶與 1961 年可再填充桌上小瓶之區別、MoMA 描述的瓶頸外展／透明玻璃／紅蓋，以及醬油易流動的葡萄酒比喻；結尾不補回獎項或出貨。旁白與逐鏡現版 **96／96 ID**、第 2–6 章 **2,324 字元**（較 HOLD 版 +467）、**81 shot／15 card**（84.4%）、最長 **2** 連卡；`git diff --check`、ID／卡片／prompt 禁字結構自檢、`npm run check:tasks` PASS（2077 張票，其他票既有警告）。`script.md` SHA-256 `31438408B20ED60C4AEF2F552720C0DB8DA20D1E05FA69CB40C65262EA378026`；`visual-plan.md` SHA-256 `F6CA5C5C120BB92C5AD414D576ECE1F6372B67C4D8D15F0685E478948C5EC003`。這只是作者自檢；須由不同代理重新做逐句來源查核、兩位只看旁白的新盲讀與獨立視覺預檢，另須正式 TTS 時長及站主稿件核准。未付費、未上傳。

2026-10-22：另一代理對擴稿 96 句與 96 鏡完成獨立來源審查，僅 `c080419` **HOLD**：原句「只支持少滴」把 MoMA M1 同時描述的防滴／控流脈絡說得過窄。作者只改該句為「兩份後來的說明都談到滴液；但都未提供逐次量測，不能保證每次倒取都乾乾淨淨。」相鄰 `c080403`、`405–420`、`606` 與 `c080419` 畫面核對後不改；擴稿審查收據標為歷史失效。新 `script.md` SHA-256 `8443CBD82DDCC75C6BD8603A403D2BDBE8BB9317BCD701AA9A868C568492FA2C`，`visual-plan.md` SHA-256 仍為 `F6CA5C5C120BB92C5AD414D576ECE1F6372B67C4D8D15F0685E478948C5EC003`。現版 **96／96 ID**、正文第 2–6 章 **2,336 字元**、81 shot／15 card、最多兩連卡；`git diff --check`、結構／prompt 禁字自檢及 `npm run check:tasks` PASS（2078 張票，其他票既有警告）。這是作者自檢；新 SHA 的獨立來源差異覆核與兩位新盲讀、視覺預檢、TTS、站主稿件核准仍待完成。未付費、未上傳。

2026-10-22：前輪 `c080419` 差異獨立來源 PASS 只綁 96 句舊稿 `8443CBD8…`／`F6CA5C5C…`，現已標**歷史失效**。第一位新敘事讀者對該稿提出結構 HOLD（旁白欄外意外露出前八格來源，因此不列為正式盲讀收據）：第 2 章反覆容量／上桌、第 3 章繞著握／滴不揭瓶嘴、第 4 章重述滴液與查核界線、第 5 章把上市／補充／入館塞成尾聲、第 6 章重播答案。作者由此重排完整 2–6 章，並新增**不與 Treatment 票重疊**的 `script-source-addendum.md` 窄 scope；原 `source-matrix.md` 仍由 Treatment 票持有，未修改。GK Report No.34 官方 PDF 印刷頁 23–24 由作者下載掃描頁目視核對：設計者後來回憶的大瓶轉注陶壺、可量產且預裝醬油、握法、紅蓋取下後補充開口比大瓶稍寬，均只以 R1 後來回顧歸屬；不採其 60 度／第 101 模型，與 MoMA M1 的近百模型、防滴及控流並列界線分開。全段與逐鏡目前 **82／82 ID**、正文 **2,196 字元**、69 shot／13 card（84.1%）、最多 1 連卡；作者結構和 prompt 禁字自檢 PASS，並更新 `reviews/visual-preflight.md` 為明確的作者技術預檢。`script.md` SHA-256 `A9D45943B0544018EA08B6605120B56CE067D7D1AEA0F0C71A471C4AAAF1507A`；`visual-plan.md` SHA-256 `39C2382CF111AA73C8785CE60E864974BE3C204861C182445565947B38BA24E3`；R1 補充 SHA-256 `942D1FB6A9AF3BF87D2E8E63A69BBE3E4735872B7C4983CDD7C3045219B5F74A`。**新稿未有獨立來源 PASS、兩位新盲讀、獨立視覺預檢或實測 TTS 480 秒**；字數只近似 C05 的實測稿，不能推本集已達標。PR #1681 保留草稿與 `no-auto-merge`；未付費、未上傳。
