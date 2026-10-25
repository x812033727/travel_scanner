---
id: 2026-10-25-brand-stories-new-rules-remakes
title: 依 1844 與 10-25 規則重製後台未完成品牌故事
status: in-progress
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
- [x] 四份新稿以新 slug 送後台；C03企劃／劇本均核准並以官方 review-pull 匯入，C04、C05 劇本核准已讀回並匯入，C09 r12 也已重新讀回核准並匯入。未重綁原 episode。
- [ ] 取得可操作正式後台／主機的管理連線，核對並建立符合既有硬停線的 remake 預算帳戶。
- [ ] 實際合成、逐句聽檢、插圖、render、配樂、assemble、字幕、qa、package 與後台 readback。

## How to verify

`batch.json` 保存 19 筆唯讀進度、舊稿 SHA 和新版規格；新候選各自保存輸入與輸出雜湊、逐行來源、隔離旁白投影及獨立讀者判定。以 #1844 的官方 CLI 逐關執行並保存真實結果，不用紙上估秒替代 TTS、圖片或成片。純文字候選不代表成片完成。

## Notes

- C03 r3已通過獨立來源／書面配鏡（143句、110景）及雙讀者原生合併（讀者一13 yes、讀者二12 yes，個別保留意見未刪）。真實r1／r2 HOLD及來源鏈在`c03/history/`；`c03/verify-1.md`由獨立查核代理撰寫，已綁SHA複製至canonical，並非owner核准。
- C03新版`story-everyday-moleskine-c03-remake-20261025`：outline review `3b0480b5-0ca4-4337-b743-0db04dfb4106`、script review `c90d3492-7efe-4385-bdcc-ccd6664205d1`，均已讀回正式 approved 並匯入精確雜湊。新稿video SHA `65ca1b602a5048e4f6af7c721bf1bd15abf152616c07d179f6ff5b6350c02005`；後台canonical script SHA `4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`。未復用舊核准或新建auto.json。
- C03從零預檢：120個TTS請求／4194計費字元，100個插畫景、每景含首次最多3次，圖像與評審目錄估價約US$4.05；不是全片報價。原生保守語音／轉寫預留、價格可見性與未完成全片入場核對見`c03/pricing-and-entry.json`。付費請求／新媒體仍為0，正文12–14分鐘未量測。
- C03獨立執行根目錄`/workspace/work/brand-story-20261025/c03-submission-root`，媒體根目錄仍為`/workspace/work/brand-story-20261025/media`。續做請先讀`c03/production-entry.md`：精確新版預算帳戶與受保護啟用、正式v4素材仍需有正式連線的操作方處理；從零製作不再等舊C03插圖／音訊。原集帳本與既有US$25停線未變。
- 站主再指示「做完後你繼續下一個不用停」，已接續C04八語文字與製片準備，並查C06原始資料。C03媒體仍優先；沒有宣稱跳過其預算入場。C04後台既有八語三部分全選已讀回，時間`2026-10-25T11:30:25.950439Z`；單一選項A企劃已免費送審，首卡`57a05583-f61e-4a74-88c9-274d00b163ee`已superseded；補齊原生三必填段落後重送，現行review `b82ea00f-85da-4cc9-92d8-a654e08ea09b`為pending，原劇本核准不變。C05/C09基底八語文字亦已完成獨立校對與原生合併；增補候選譯文尚未採用。
- 站主已授權本集做完按集數繼續、採建議選項且預設八語，不再為例行製片選項提問。C03正式後台讀回英／日／韓／西／葡／印尼／越南／泰全部 metadata、CC、dub=true，原始決定時間為 `2026-10-25T14:09:36.202531Z`；後續各新集依此預設走正常身分驗證設定，未宣稱已替其他集套用。
- C03八語共1,144句文字、48章及標題說明完成原生合併與非譯者獨立校對，修正後重查全部 TEXT_PASS；初次 FIXES_REQUIRED、原檔與撤回意見保留。隔離 runtime 搬入演練0 lint errors、無缺漏或過期翻譯警告。沒有實際時間軸／SRT／配音或語言輪啟動。
- C03原繁中燒錄稿不變，另備 clean-master 衍生配方，只有字幕旗標不同，官方劇本／旁白／圖像／混音輸入hash相同，獨立判定 METADATA_DERIVATION_PASS。須用真實已驗主素材分別輸出、clean成片重作QA及final審核後才符合原生配音關卡，不是已有乾淨影片或可以沿用另一輸出的成片核准。
- 正式核准匯入後已真實執行TTS，exit 3 `video_budget_preproduction_hold`於請求規劃及供應商派送前拒絕；0付費請求、0新音訊。現有影片工具權杖已有效，不需站主重貼。正式主機的精確新slug註冊、獨立帳戶及API／本機受審啟用、全片價格／帳本與正式v4素材讀回仍缺。`c03/host-admission-readback.sh`已通過bash與Node語法、三項本機拒絕測試及獨立檢查；未在正式主機執行；它只讀且不啟用帳戶。
- 站主追加順序指示後已復工，當前優先 C03；`execution-order.json` 記錄 C03 起的既有未完成集數，不為缺號新增題目。C04／C05／C09 已完成的新稿與審核紀錄保留。
- 站主後續回覆「如果不行你就重新來吧」，因此 C03 改採全新製作／從零估價，舊素材取回改為可選的歷史保全，不再擋住新稿或新製作準備。新生成仍須使用精確新版帳戶與現行付費入場保護，不借原集帳戶放行繞路。
- C03 舊版雖有 10/25 本機上架包收據，正文約 481.02 秒、總長約 633.6 秒、未燒字幕，仍是 9–11 分鐘舊規格，不能當作新規則版本。舊 73 張付費插圖、配樂與 v4 素材在原 Windows 工作機，本環境無原件；已詢問可讀共享路徑／工作機連線，先做新稿、來源與可沿用圖片對照。
- C03 原 slug 的付費放行針對 10/24 完成舊片的一句重錄等工作；新的 `story-everyday-moleskine-c03-remake-20261025` 仍受完整前綴 hold。歷史剩餘額不是即時讀值，不借原 slug 的放行替新版繞過帳戶啟用。最小化後台讀回、媒體可用性與 admission 差異保存在 `c03/existing-evidence/`。
- Worktree：`/workspace/work/brand-remakes-source`，分支 `codex/brand-remakes-20261025`，根代理負責。一次共享 checkout，讀者只拿隔離文字，未為每位讀者複製 repo。
- 2026-10-25 正式唯讀盤點：104 筆漫劇中品牌故事 22 筆；19 筆未上 YouTube，含 14 筆 everyday、4 筆 blocked 及 Dyson 1 筆。已上傳的 A4／米其林／杜比保留。everyday 劇本多已獲舊規格核准，新改寫須重新審。
- 10/25 media/status 可連通；MiniMax image-01、Gemini 頻道旁白與 Lyria 設定可用。音樂月額度只剩 8 首，不能不查額度就同時為 18 題購買配樂。
- 現行 `pending-pilot-budget.mjs` 與 API 對 everyday 除 C03 外均有 preproduction hold；新 remake slug 也在 hold。工具權杖不含 admin drop/redo/series patch 權限；不得把新 slug 改到其他前綴避開帳本。
- 先前存於 `.video-work/_branding` 的 5 秒/21 秒素材為 `curio-archive-original-candidate-20261020-v1`，只確認檔案與時長；未確認它是站主選定的 v4，不得當作正式 v4。
- 本批四支候選、逐句來源、真實雙讀者紀錄、失敗版本、正式後台送審收據與續做方式已存 `docs/videos/brand-story-remakes-20261025/README.md`；最新逐片狀態在 `status.json`。盤點的 22／19 筆是新增 remake 卡之前的原始快照，不能當作目前後台總數。
- 後台新版：`story-everyday-bubble-wrap-c04-remake-20261025`、`story-everyday-kincho-c05-remake-20261025` 的精確劇本已核准，官方 `review-pull` 已匯入；`story-everyday-patagonia-c09-remake-20261025` 的 r12 亦已讀回核准，於2026-10-25T15:31Z確認精確SHA並匯入。保留原始 pending 送審收據，另以 `backend-status.json` 記新讀回結果。不建立 `auto.json`、不自行恢復 worker、不改舊集。
- 正式製片仍被既有 C 系列 preproduction hold 與尚未建立的 remake 預算啟用流程擋住；現有權杖無法做受保護的帳本／歷史費用讀回與啟用。已向站主說明仍缺可操作管理員／正式主機連線。不得把站點顯示的 USD200 當全片授權、不得換 slug 前綴繞過 USD25 既有硬停線。
- 本批送出的是免費劇本審核，不是音訊或影片。付費請求 0；新音訊、插圖、配樂、成片均 0；無實測 12–14 分鐘、無媒體 QA、無成片核准、無 YouTube 上傳。正式 v4 來源身分尚待主機核對，候選秒數相符不能代替身分驗收。
- 隔離執行根目錄 `/workspace/work/brand-story-20261025/submission-root`，素材根目錄 `/workspace/work/brand-story-20261025/media`。三支的 canonical `script.md` 由官方 `writeScreenplay` 產生，與作者附來源稿分開。C03、C04、C05 已有 `approvals.json`，不可再以準備程式覆寫核准輸入；既有 source／runtime／字典及研究快取保留待續。
- 驗證：236 項 `test:docs-videos` 全過，0 skipped；文件測試收集契約另 2 項全過；2178 份任務檢查通過（其他既有任務警告未改）；兩 helper 與主機唯讀腳本語法通過；12項原生i18n測試全過，八語runtime搬入演練0錯誤／無缺漏過期。53 份舊稿雜湊複核未變。三支 lint 0 errors，C04／C05／C09 各 6／0／18 個警告仍留原紀錄，須待真實聲音與圖像處理。
- 交接已推送至草稿 PR https://github.com/x812033727/travel_scanner/pull/1849 ，已讀回 open／draft／未合併及 `no-auto-merge` 標籤。當時先保存純文字成果；本輪已接續後續集數，任務維持 in-progress，製片仍另有入場阻擋。

- 接續C04已完成八語880句／48章及metadata原生合併、完整獨立文字校對與14處精確修正後重查，全數TEXT_PASS；歷史與譯者自校保留。另重開原件獨立來源／書面配鏡PASS，verify-1已綁精確SHA進canonical並以原生report-only同步後台。新runtime搬入演練0errors／無缺漏過期翻譯，沒有造SRT／配音或語言輪。C04／C05／C09 clean配方均獨立METADATA_DERIVATION_PASS，尚無實際輸出。
- C05／C09基底八語作者／交叉覆核已完成；C06完成11份官方或原始來源研究，r3新稿已通過來源／書面配鏡及原生兩讀者合併，正在八語文字準備。沒有將C06來源研究當新稿PASS或舊核准沿用。任務本輪持續in-progress，成片DoD仍未完成。

- 補查native spokenUnits：C03 3406／正文3222、C04 3166／正文2981、C05 2792／正文2609、C09 2802／正文2603；這些不是實際TTS秒數。C05／C09正文偏短風險明顯，已另派作者在各candidates/length-extension增補有來源有效資訊，保留current/核准/譯文、不靠停頓慢播或警語填長；新候選須新的來源核對、兩隔離讀者及精確新審核後才採用。
- C05 current基底八語776句已全獨立TEXT_PASS（KO2/PT1/ID2精確修正後重查），preparation-status明確排除length候選。r6來源重開9原件PASS但readiness為HOLD_FOR_LENGTH_EXTENSION，未寫verify-1 marker。C09原始S4報導已釐清c09r079同年為1973，增補候選將親讀原件澄清，舊95句翻譯仍按原source保留。最新main76cc8aa1a的三份budget檔與分支一致，guard未變，沒有重送付費TTS。

- 本輪C06 r3 163句／137插畫景、全片3428／正文3229 units，原生0errors15warnings；來源與書面配鏡PASS、雙讀者合併PASS（個別scene_first/no_recap保留）。精確企劃cf42c3a1-f54b-4295-934e-f4d6fa0ee163、劇本3d8ed292-ea12-4bfd-98b8-097acda4a828已讀回pending，canonical e00fd07d54ef284a5577327f999f4e46222aef455417f3fc878c1a91f11b124e，沒有新批准。八語文字開始；新卡分類/正式八語選擇須有content.manage連線，具體資料已存c06/protected-admin-settings.json。C07改寫及C08來源查核同步接續。
- C05／C09 r4增補候選原生均0errors；C05刪除煙燻/花期/時數警語支線後正文2785，仍有規劃容量風險；C09刪除型錄尺寸清單後正文3325，來源差分與新讀者正在做。兩者未採用，原BASE/核准/基底八語保留。C09 r2本機fullcontext預檢4errors後已於任何外部呼叫前rollback，失敗與修正鏈存history。

- C08研究包已凍結38主張／120舊句盤點，取得2011後期200mL產品對應的JP5727888B2完整原專利，1961原專利仍列缺口，沒有新旁白或SOURCE PASS。C09r4來源／書面配鏡PASS但兩讀者共同HOLD one_line/no_recap/no_detour，保留history/r4並開始R5實質重編；原已核准BASE仍未換稿。

- C06八語1304句／48章及metadata已全量交叉校對，19處必修後獨立重查全TEXT_PASS；8語原生縮圖均真正合併，runtime0errors／無過期缺漏譯文，17個其餘soft warnings保留。五份current基底共4864句，不含C05/C09未採候選或C07/C08新改寫。clean配方獨立METADATA_DERIVATION_PASS，實際媒體仍0。
- C07r1來源與書面配鏡PASS（15原件／144句／141插圖+outro）但native兩讀者共同HOLD chapters_link/payoffs/no_recap/no_detour，完整history/r1後重編r2，不假裝sourcePASS就是敘事批准。C05r5來源PASS但native只共享no_recap，保留history/r5再做r6；C09r5補當事人1974AAJ原刊中的1973攀登場景實質重編；C08新稿接續中。

- 當前更新：C09 R7已通過獨立來源／書面配鏡、兩全新讀者各13yes及0error實際canonical預檢後採用。新video aed95981…／官方劇本02f091ca…；新script 6a441762-8d88-45b7-adff-78b5c3ef1260、outline 5199b233-c1ee-4970-ae11-af9115cbbde9真實讀回pending。舊BASE／批准／760句完整封存，新稿不沿用其批准。新版八語824句全部TEXT_PASS，3處必修後獨立重查；五份current共4928句。clean新配方另獨立METADATA_DERIVATION_PASS，仍無實際媒體。
- C05材料旅程R9已凍結待來源差分／actualpanel8，BASE與776句未變；C07R3修窄來源並刪物流教程待新查；C08R4兩讀者仍共享no_recap；C10R1來源／書面配鏡PASS但兩讀者共享scene_first/no_recap。完整各輪history與真正投票保留，不抽取未改稿重投。原53檔本輪再次核對未變。持續下一題準備，不將任一文字PASS宣稱影片完成。
