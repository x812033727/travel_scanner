---
id: 2026-10-25-brand-stories-new-rules-remakes
title: 依 1844 與 10-25 規則重製後台未完成品牌故事
status: blocked
priority: P1
area: docs
owner: codex-brand-remakes
claimed_at: 2026-10-25T10:29:13Z
created_at: 2026-10-25T10:29:13Z
completed_at:
branch: codex/brand-remakes-20261025
depends_on: []
scope:
  - docs/videos/brand-story-remakes-20261025
---

# 依 1844 與 10-25 規則重製後台未完成品牌故事

## Why

站主要求接續完成後台未完成品牌故事並依新規則重製，隨後指定參考 PR #1844。舊工作區停在 10 月 22 日，不能作現行規則；本次在一份新的稀疏 worktree 以已合併 #1844（2b20c30d3）為基準，保存新候選而不覆寫既有核准稿及付費素材。

## Definition of done

- [x] 用工具權杖完整列出後台品牌故事並區分已上傳、未完成及同題舊版。
- [ ] 未完成影片依 #1844 的來源、雙讀者、聲音、插圖、字幕、片頭片尾、縮圖與成片 QA 流程完成新版本。
- [ ] 每支實測正文 12–14 分鐘，字幕燒錄、繁中 CC、5 秒片頭與 21 秒 v4 片尾通過媒體檢查。
- [ ] 付費前有相符的逐片全片帳戶、歷史費用讀回與可審閱報價；不繞過現有 C 系列 hold。
- [ ] 上傳包與後台新審核卡可讀回；站主看片及上傳沿既定關卡。

## Steps

- [x] 依追加指示優先完成 C03 Moleskine 的新規則劇本／文字分鏡、獨立來源、雙讀者合併、免費預檢及企劃／劇本送審；成片仍待正式製片入場。
- [x] 讀取 #1844、10/25 頻道報告與現行品牌故事規則，保留正式清單快照。
- [x] 確認 22 筆品牌故事，19 筆未有 YouTube ID 且未放棄；其中龜甲萬原版與 short-v8 是同題兩版，保留舊版避免重複製作。
- [x] 完成先前首批 C04 泡泡紙、C05 金鳥、C09 Patagonia 的新規則劇本／書面分鏡；加上優先 C03 共四題備稿，其餘14題仍待來源／媒體核對。
- [x] 四份精確稿 lint 均 0 errors，tts／keyframes dry-run 完成並綁輸入雜湊；music dry-run 因缺真實 timeline 正常停下。
- [ ] 實際 TTS 後重估分鏡及配樂，補齊含歷史費用、轉寫、Jev 與重試的全片最壞預留。
- [x] 四份新稿以新 slug 送後台；C03企劃／劇本待審，C04、C05 劇本核准已讀回並匯入，C09 r12 待審。未重綁原 episode。
- [ ] 取得可操作正式後台／主機的管理連線，核對並建立符合既有硬停線的 remake 預算帳戶。
- [ ] 實際合成、逐句聽檢、插圖、render、配樂、assemble、字幕、qa、package 與後台 readback。

## How to verify

`batch.json` 保存 19 筆唯讀進度、舊稿 SHA 和新版規格；新候選各自保存輸入與輸出雜湊、逐行來源、隔離旁白投影及獨立讀者判定。以 #1844 的官方 CLI 逐關執行並保存真實結果，不用紙上估秒替代 TTS、圖片或成片。純文字候選不代表成片完成。

## Notes

- C03 r3已通過獨立來源／書面配鏡（143句、110景）及雙讀者原生合併（讀者一13 yes、讀者二12 yes，個別保留意見未刪）。真實r1／r2 HOLD及來源鏈在`c03/history/`；`c03/verify-1.md`由獨立查核代理撰寫，已綁SHA複製至canonical，並非owner核准。
- C03新版`story-everyday-moleskine-c03-remake-20261025`：outline review `3b0480b5-0ca4-4337-b743-0db04dfb4106`、script review `c90d3492-7efe-4385-bdcc-ccd6664205d1`，均讀回pending。新稿video SHA `65ca1b602a5048e4f6af7c721bf1bd15abf152616c07d179f6ff5b6350c02005`；後台canonical script SHA `4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`。未復用舊核准或新建auto.json。
- C03從零預檢：120個TTS請求／4194計費字元，100個插畫景、每景含首次最多3次，圖像與評審目錄估價約US$4.05；不是全片報價。原生保守語音／轉寫預留、價格可見性與未完成全片入場核對見`c03/pricing-and-entry.json`。付費請求／新媒體仍為0，正文12–14分鐘未量測。
- C03獨立執行根目錄`/workspace/work/brand-story-20261025/c03-submission-root`，媒體根目錄仍為`/workspace/work/brand-story-20261025/media`。續做請先讀`c03/production-entry.md`：精確新版預算帳戶與受保護啟用、正式v4素材仍需有正式連線的操作方處理；從零製作不再等舊C03插圖／音訊。原集帳本與既有US$25停線未變。
- 站主追加順序指示後已復工，當前優先 C03；`execution-order.json` 記錄 C03 起的既有未完成集數，不為缺號新增題目。C04／C05／C09 已完成的新稿與審核紀錄保留。
- 站主後續回覆「如果不行你就重新來吧」，因此 C03 改採全新製作／從零估價，舊素材取回改為可選的歷史保全，不再擋住新稿或新製作準備。新生成仍須使用精確新版帳戶與現行付費入場保護，不借原集帳戶放行繞路。
- C03 舊版雖有 10/25 本機上架包收據，正文約 481.02 秒、總長約 633.6 秒、未燒字幕，仍是 9–11 分鐘舊規格，不能當作新規則版本。舊 73 張付費插圖、配樂與 v4 素材在原 Windows 工作機，本環境無原件；已詢問可讀共享路徑／工作機連線，先做新稿、來源與可沿用圖片對照。
- C03 原 slug 的付費放行針對 10/24 完成舊片的一句重錄等工作；新的 `story-everyday-moleskine-c03-remake-20261025` 仍受完整前綴 hold。歷史剩餘額不是即時讀值，不借原 slug 的放行替新版繞過帳戶啟用。最小化後台讀回、媒體可用性與 admission 差異保存在 `c03/existing-evidence/`。
- Worktree：`/workspace/work/brand-remakes-source`，分支 `codex/brand-remakes-20261025`，根代理負責。一次共享 checkout，讀者只拿隔離文字，未為每位讀者複製 repo。
- 2026-10-25 正式唯讀盤點：104 筆漫劇中品牌故事 22 筆；19 筆未上 YouTube，含 14 筆 everyday、4 筆 blocked 及 Dyson 1 筆。已上傳的 A4／米其林／杜比保留。everyday 劇本多已獲舊規格核准，新改寫須重新審。
- 10/25 media/status 可連通；MiniMax image-01、Gemini 頻道旁白與 Lyria 設定可用。音樂月額度只剩 8 首，不能不查額度就同時為 18 題購買配樂。
- 現行 `pending-pilot-budget.mjs` 與 API 對 everyday 除 C03 外均有 preproduction hold；新 remake slug 也在 hold。工具權杖不含 admin drop/redo/series patch 權限；不得把新 slug 改到其他前綴避開帳本。
- 先前存於 `.video-work/_branding` 的 5 秒/21 秒素材為 `curio-archive-original-candidate-20261020-v1`，只確認檔案與時長；未確認它是站主選定的 v4，不得當作正式 v4。
- 本批三支候選、逐句來源、真實雙讀者紀錄、失敗版本、正式後台送審收據與續做方式已存 `docs/videos/brand-story-remakes-20261025/README.md`；最新逐片狀態在 `status.json`。盤點的 22／19 筆是送審前三支新卡的快照，不能當作目前後台總數。
- 後台新版：`story-everyday-bubble-wrap-c04-remake-20261025`、`story-everyday-kincho-c05-remake-20261025` 的精確劇本已核准，官方 `review-pull` 已匯入；`story-everyday-patagonia-c09-remake-20261025` 的 r12 已送 pending。保留原始 pending 送審收據，另以 `backend-status.json` 記新讀回結果。不建立 `auto.json`、不自行恢復 worker、不改舊集。
- 正式製片仍被既有 C 系列 preproduction hold 與尚未建立的 remake 預算啟用流程擋住；現有權杖無法做受保護的帳本／歷史費用讀回與啟用。已向站主說明仍缺可操作管理員／正式主機連線。不得把站點顯示的 USD200 當全片授權、不得換 slug 前綴繞過 USD25 既有硬停線。
- 本批送出的是免費劇本審核，不是音訊或影片。付費請求 0；新音訊、插圖、配樂、成片均 0；無實測 12–14 分鐘、無媒體 QA、無成片核准、無 YouTube 上傳。正式 v4 來源身分尚待主機核對，候選秒數相符不能代替身分驗收。
- 隔離執行根目錄 `/workspace/work/brand-story-20261025/submission-root`，素材根目錄 `/workspace/work/brand-story-20261025/media`。三支的 canonical `script.md` 由官方 `writeScreenplay` 產生，與作者附來源稿分開。C04、C05 已有 `approvals.json`，不可再以準備程式覆寫核准輸入；既有 source／runtime／字典及研究快取保留待續。
- 驗證：236 項 `test:docs-videos` 全過，0 skipped；文件測試收集契約另 2 項全過；2178 份任務檢查通過（其他既有任務警告未改）；兩 helper 語法通過。53 份舊稿雜湊複核未變。三支 lint 0 errors，C04／C05／C09 各 6／0／18 個警告仍留原紀錄，須待真實聲音與圖像處理。
- 交接已推送至草稿 PR https://github.com/x812033727/travel_scanner/pull/1849 ，已讀回 open／draft／未合併及 `no-auto-merge` 標籤。純文字成果先保留待正式製片入場，任務維持 blocked。
