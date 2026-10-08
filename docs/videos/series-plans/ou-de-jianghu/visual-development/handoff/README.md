# 第一集資產與開拍交接

2026-10-09。範圍為《偶的江湖》第1集〈幽皇之女〉。站主已正式回覆「採用素材與 v4，按此點數上限鎖定 plan」。**146 張素材按既有用途限制正式採用，v4 的 455 鏡 Hailuo plan 已寫入正常工作目錄並通過原生比對。** 本期含預留上限 26,980.8 點，三鏡小樣上限 316.8 點包含在內；第二期須實際有額度才續做，不購點、不續訂、API 支出授權為 0。look 按本次決定保留待判圖，尚未開始配音。站主其後要求內建瀏覽器製作，已交付[三鏡 Hailuo 外部視覺小樣](hailuo-browser-pilot-20261009.md)：13.375秒無聲完整take預覽，本輪總實扣300點；s036懸停變更另經站主核准並建立獨立來源及鎖，正常v4未覆蓋。抬手跳接、正式時窗與使用者成片接受仍待解決，未擴量。

最新狀態以[剪接、聲音與剩餘預算](episode-continuation-20261009.md)為準：站主已採用原三片重剪的10.75秒無聲小樣並續A期，自行儲值後頁面61,700點；036／038首格懸停連戲另建一致來源及獨立鎖。已續製4張首格（91點），053七秒片另實扣84點；A期累計475點、頁面61,525點。062仍有右臉小紫痕，未購片。Google配音後置，597句備料完成；站主已同意聲音分軌，取得130個CC0音效並製成9段試聽，尚未採用／混音。上段13.375秒與未放量敘述保留作先前pilot狀態，不作最新待辦。

053新片已下載，實際7.291667秒／175格／24fps／2K，全decode及首格相似度過；末段裁冠，母片與059／065切用保持hold。062臉上小紫痕亦待修。兩分支保留原件及收據，未自動第三次生圖或重買同缺陷影片；不能把4支下載原片當4支通過。

素材採用以 [正式採用與鎖定紀錄](adoption-decision-20261009.md)／[逐圖決策 JSON](adoption-decision-20261009.json) 為準；後續付費生成與懸停变更見 [瀏覽器製作紀錄](hailuo-browser-pilot-20261009.md)。原清冊、v3 staging 及決策前快照保留歷史值；不能只讀其中的舊 pending 欄位判斷當前採用狀態。

本交接與原 e001、production 檔分開保存；未改既有試播票或第8集工作。下游仍接 [原第1集Hailuo試播票](../../../../../../tasks/open/2026-10-04-clip-route-pilot-comparison.md)，沒有另開重複付費試播。

## 先讀什麼

1. [本次收尾與連戲](finalization-20261009.md)、[455 鏡參照分派](finalization-20261009.json)、[v4 唯二修正與實看](../episode-plan/finalization-v4.md)：尺寸用途、逐鏡 base/head/detail/mouth 與場景道具、接觸／棋盤／空間首尾。
2. [P0–P7 基礎包 v3](../episode-plan/preproduction-package-v3.md)、[分項批次JSON](../episode-plan/budget-and-batches.json)：9 場空間、455 鏡、預算、三鏡小樣及停止規則。v4 只修兩個 prompt 字串，台詞、時間、motion、camera、風險與預算不變。
3. [v4 差異與工具證據](../episode-plan/finalization-v4-verification.json)、[獨立文字分鏡觀看紀錄](../episode-plan/cold-review-independent.md)：v3 全程觀看、v3.1 23 卡覆核、v4 修改者六卡覆核分開保存。
4. [最新畫像與概念](../episode1-portraits/finalized-views-receipt.json)、[最新角色參照與嘴形](../animation-reference/finalized-media-receipt.json)、[場景道具收據](../scene-prop-design/media-receipt.json)、[匯入合約](../import-contract/README.md)：個別 key、原生尺寸、來源／媒體 SHA 與狀態。

最新清冊 [asset-manifest.json](asset-manifest.json) 綁 12 份來源、**146 張唯一 latest 素材**、9 張正面沿用、16 種 shot_looks 獨立雜湊與 455 鏡 v4。採用決策另以清冊 SHA 綁定，保留其原歷史欄位。舊 9 筆隔離 pending 匯入只作 **v3 歷史證據**；本輪已把含沈全身 v3 的 [最新九張基底圖接入正常 runtime](runtime-look-preparation-20261009.md)，仍未 judge、choice 或 look 核准。清冊也沒有讓模型自動使用所有多角度或口型圖。

## 已形成的具體交付

| 項目 | 可交接內容 | 狀態界線 |
| --- | --- | --- |
| 美術方向 | 華麗古裝、細緻人物；9 概念與27 獨立視圖按 finalized receipt 取最新修版 | 畫風與146張素材的限定參照用途已接受；正常look待判圖 |
| 新參照範圍 | 82 張新角色用途含 8 嘴形，另沿用 9 正面＝91 用途；28 張場景／道具；加9概念27畫像共146唯一圖 | 舊版本與失敗修訂原件均保留；不能把 91 用途當91張新生成圖 |
| 正式 plan | v4，455鏡＝420clip＋30still＋5來源切，9空間 | 正常 plan/lock.json 已寫入且 check 無差異；597句台詞、鏡序、action_seconds與原預算算術不變；實際支付受本次較窄授權限制 |
| 鏡位及風險 | 原447組setup收斂343；原10個程式C逐鏡裁定；接觸s036保留人工C | 不把機器C0解讀為動畫零風險；343也不等於343支可直接共用影片 |
| 文字動態分鏡 | 459列，包含4原稿字卡，23:23.533；可本機播放與重建 | 沒有TTS／关键影格／動畫；獨立觀看結論依專人紀錄，不等於成片QA |
| 工程接點 | 最新9張全身已正常接入；27次dry-run／import／exact-rerun全過，0次fetch | 每人1張pending候選；尚無judge、choice或look核准，舊staging保持不動 |
| 預算及採購次序 | 420支逐一歸入兩個27000點額度期；首末格、聲音、judge、音樂及內建美術分開記帳 | 原始費率、畫面餘額快照與未來可用額度分開；沒有購點或續費授權 |

原稿video SHA `82d221350032c02b3b2f8943e72e63795be36e221c45067acf5bd9a751d20443` 不變；目前 v4 SHA `cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17`。父版 v3 SHA `7f7676d1ce39a6f9dbbdc4cacc5bc8cb39b9979e66e4a906213d2ea4235014df` 保留。後續原稿持有人改 e001，先核對合併，不把工作提案直接覆蓋原檔。

舊角色圖冊的 83 圖檢查保留在 [歷史紀錄](../animation-reference/gallery-verification.json)。[本輪最新圖冊驗證](../animation-reference/gallery-verification-20261009.json) 另核實 146 圖解碼／SHA、60 組篩選、放大／Escape、390px 手機無溢出及 v4／棋局跨頁連結；三張截圖的實看結論依該覆核者紀錄。本 manifest 負責逐圖原件 SHA／原生尺寸及版本接線，不把圖冊正常顯示當美術採用。

## 素材用途與連戲定稿提案

- 白扇形制唯一依據為 **shen-guihe-construction-details-v3＋personal-prop-states-v3**：白玉骨、白紙、沒有扇穗／鏈／小珠掛件。最新人物姿態、概念、配色或群像仍可能有微小手邊短線／小珠，只供臉、服裝、姿態、配色，不能用那些像素推導扇拓撲；不宣稱所有圖幾何已全面一致。逐鏡 mapping 對沈／明示扇鏡分配這兩母圖的用途，持物手／腰間位置仍依 v4，不加物件。舊失敗修訂保留，舊 staging 不自動變新图。
- **取消獨立冷室母圖**：所有 `chess-guestroom-cold-v*` 都不選用、不送模型。a05-s031／035／042 改用 clean `chess-guestroom-master-v4` 的幾何與不透景紙窗，加 [冷光／霜／翻盤状態 spec](../scene-prop-design/cold-state-spec.json)；`rendered=false`，不能宣稱三張冷場首格已完成。s023 在翻盤前，不能預先帶地面灑茶。
- AI 棋盤不是格數／落子權威。[六個精確狀態](../scene-prop-design/go-layout-decision.json) 以同一 19×19 坐標保留原16點的子集：12→13→14→15→16，最後唯一白子 [1,17] 才成17；不加棋子、不鏡像。
- **1600／2048 是編輯長邊目標**。27 張原生 PNG 都符合現行 look 匯入條件；18 張半／全身仍保留 `native_below_target`，不硬放大。用途是身分／服裝參照，不是已交付的最終 2K 首格。實際首格另選支援路線並讀回 native pixels；當前 drama keyframes 預設1K，H3 I2V 的首格與 `reference_images` 互斥。
- 新 8 嘴形板只供靜態嘴部畫法；部分冠帽裁切時仍用原頭像／冠部母圖，沒有精確 phoneme 或 lip-sync 證據；殷無聲沒有嘴形板。九人多角度仍是2D參照，不是正交工程轉台或骨架。
- 場景10地點對應9空間族；道具索引保留原稿，逐鏡實際做法以 v4 提案為準。接匣、四箭入囊、拔釘接弦及最後白子維持結果插鏡，不把複雜接觸加回去。送茶舊包鏡號誤索引已另更正，原稿與 v3/v4 此處一致。

上述差異保留在既有畫像、動畫參照、場景道具與交接待辦票；沒有以候選張數冒稱全部已通過最終製作驗收。

其中 `shen-guihe-concept-v5`、`shen-guihe-right-profile-v3`、`shen-guihe-left-three-quarter-v3` 明確列為「僅身分／服裝用途」的限制素材。最新逐圖範圍與限制由 [白扇獨立檢查](../animation-reference/fan-independent-final-review.json)、[嘴形獨立檢查](../animation-reference/mouth-independent-review.json) 留證；機械圖冊檢查另見 [20261009 圖冊驗證](../animation-reference/gallery-verification-20261009.json)。本次站主採用保留這些限制，不轉成動畫品質核准。

## 工作產物與播放器證據

**目前工作目錄**：`<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/`。包含 video、分鏡JSON/CSV/Markdown、camera/risk ledger、預算、可讀文字animatic、工具原始診斷及六卡截圖。v4 HTML SHA `cee2fc9cbe89b879e8c899bccd3888a63ddfb9f6534e09163e27c6f2872324d1`；本機服務入口 [v4 文字animatic](http://127.0.0.1:8774/animatic.html)，服務只綁 localhost。重建器限定父版 hash，拒絕覆寫非空目錄：

```text
node docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/verify-finalization-v4.mjs <V3_DIR> <V31_DIR> <EMPTY_V4_OUTPUT>
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/build-finalization-20261009.mjs <VIDEO_WORKDIR> <V4_DIR>
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/build-finalization-20261009.mjs <VIDEO_WORKDIR> <V4_DIR> --check
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/build-manifest.mjs <VIDEO_WORKDIR>
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/build-manifest.mjs <VIDEO_WORKDIR> --check
```

先更新 finalized receipts，再重建 mapping，最後重建 manifest；mapping 的候選來源 hash 失效時 manifest 會拒絕繼續。兩份產物都只寫 handoff metadata，不寫 runtime。下列是**保留的 v3 歷史重建與播放器證據**：

v3 repo 外目錄 `.../plan/preflight-20261008-v3/` 可用原命令重建到另一空目錄：

```powershell
node docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/verify-proposal.mjs <OUTPUT_DIR>
node docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/budget-and-batches.mjs <OUTPUT_DIR>
node docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/serve-proposal.mjs <OUTPUT_DIR> 8767
```

服務只綁本機；運行時入口為 [文字animatic](http://127.0.0.1:8767/animatic.html)。已在獨立 `preflight-20261008-v3-rebuild-check/` 重建，video、HTML、shot-plan、camera-ledger、risk-ledger、proposal-edits六份SHA全部與v3相同。HTML SHA為 `2d8d5457f4056a3b99f46cf34d580b41791dd172aec0d60119b22a406b96353c`。

舊v2曾在15.7秒真的崩潰：共用generator省略字卡但保留時間洞，字幕索引變負；另有終點回第一格的邊界缺陷。v3在 [scope renderer](../episode-plan/render-proposal.mjs)補回4字卡及字幕／終點邊界，459段連續、2295邊界probe通過。舊v2目錄、未修的 `animatic-upstream.html`、錯誤時間與console證據均保留。

**共用generator兩份來源尚未修。** [追蹤票](../../../../../../tasks/open/2026-10-08-animatic-title-gap-subtitle-boundary.md)已明列 `.agents`／`.claude`同步及相關回歸測試；本次修的是可重建wrapper，不稱共用工程已完成。冷看者的實播時間與觀察限制，另見獨立紀錄。

v3後續已完成全長1倍速播放；373張卡即時觀察、86張補看，459張全覆蓋，但有工具觀察間隙及最初AX暴露全表，不稱完全盲看。冷看指出still卡缺首格線索，故另做 [v3.1卡面版](http://127.0.0.1:8768/animatic.html)：顯示原首格／靜態結果與3末格，video、台詞、時間及預算不改。其23卡獨立停格複看已完成，證據在 [呈現覆核收據](../episode-plan/presentation-review.json)；沒有把v3全長證據冒稱v3.1第二次全長。原版及修訂版各自保留SHA，重建補充器見v3包。

v4 修正後只複看 a03-s085／086／087、a04-s037／038／039 六張停格卡。CUA timeout 與後續成功的本機 Playwright/Edge 選卡／截圖均保存；六張真實截圖再以 view_image 實看，無 pageerror。這是修改者定點複核，沒有新的全長、獨立冷看、美術／聲音／動畫 QA 主張。

工具真實結果：lint與shot_reading strict過；craft strict保留a03-s052～s054三反應警告與人工理由；shot_plan strict保留整集期望超單月的警告。正式鎖定後原生readiness為 **2過／429尚未到位**：plan與當前劇本／路線相符，但仍缺script、look、audio、storyboard關卡、錄音時間線及首末格；這是製作送出前檢查，不能反過來說前期規劃尚未鎖定。

## 正式採用之後的執行順序

| 次序 | 具體行動／證據 | 開始條件 |
| --- | --- | --- |
| 1 已完成 | 站主採用146張限定用途素材、v4及本期Hailuo點數上限；原話及對應SHA已保存 | 第二期須有實際額度；不購點、不續訂、不扣API |
| 2 | 將採用版本接回正常劇本與look流程；外部圖正式judge／choice／review，核對series-store和參照SHA | 原生來源仍一致，實際判圖與owner決定可追查 |
| 3 已完成 | 正常 `plan_lock --write --note "站主原話" --assist off`，附兩期逐鏡分配；`--check` exit0 | 原生鎖允許在媒體未齊時寫入；look保留待處理；送片前仍須ready全過 |
| 4 | 製作TTS、ASR／聽審及audio；依真實時間重算秒數／剪點／價檔 | 當次成本範圍、有效runtime與餘額已核對；原估23:23.533超原驗收上緣23.533秒，需實測處理 |
| 5 | 製作450張獨立首格及3末格，核對实际reference SHA與當鏡造型；關鍵影格animatic及storyboard審閱 | look與audio當前；不能以單人概念圖充當場景首格 |
| 6 | 原生ready全部適用項通過；先做下面三鏡連續動畫小樣 | 送出前帳號／頁面模型／秒數／2K／參照上傳／AI潤飾off確認；留請求與實扣收據 |
| 7 | 小樣實速觀看、逐格及匯入QA，站主接受才依場景批次放量 | 不用三張靜圖或不連續抽樣宣稱小樣完成 |

原生plan_lock只拒`refuse`；本版月配額問題為`waste`，正常寫鎖會保留警告。兩期配額不由原生鎖自動管理，執行者須按JSON每期shot清單及即時可用餘額檢查。已見27000的頁面快照不是可無限支用的預約。

## 唯一首批動畫小樣

| 順序 | 鏡號／剪入秒 | 具體起終與主要風險 |
| --- | --- | --- |
| 1 | a02-s035／3秒 | 寂聞從右側最後三級階下來停在跪於左側的姬前；殷留上階。固定全身鏡，驗階梯、腿袍與站跪高度 |
| 2 | a02-s036／1.733秒 | 右掌首格離實體冠脊1cm→落到冠脊即停，說「你不躲？」；人工C，驗指頭、穿透、冠鏈及接觸 |
| 3 | a02-s037／2秒 | 後頸銀髮首格完全遮印→一次風分髮→末格一個月牙；驗左右、胎記及與s038落髮銜接 |

同場連續6.733秒，每支買4秒。一次144點、人工期望240點、最多2takes合計288點；含10%管理預留264／316.8點。它們已在420支整集預算內，不重複計費。第二次同缺陷仍在即停止，改提接觸局部／前後狀態的具體變更；不能悄悄第三次重買、改still或循環補秒。

成功標準包含實速連看、身份和道具、动作可读、首格匹配／PSNR、ffprobe原生尺寸與音軌、下載／匯入可用性、request ID、首末格及正文SHA、實扣、採用區間與站主接受。H3歷史原生2K／24fps需首支再測，不以1080p／30fps交片轉碼冒稱生成原生規格。小樣沒有沈的動畫，沈的臉／冠／扇仍在其第一批逐項驗。

## 預算與未決欄

v4 沿用 v3 的逐鏡算術：片段人工期望30494.4點、2takes上限44304點；含10%為33543.84／48734.4點。兩期分配分別236／184支，上限加預留26980.8／21753.6點。本次授權採用現有點數及這些上限，第二期須實際有額度才續做。頁面已核對Max餘額27000、H3 2K 4秒48點；每次送出仍核對當時模型、費率、餘額與實扣。沒有新購或續費授權。

新增API分項期望US$98.7016、上限223.1652，含10%為108.5718／245.4817；若兩期Max均需新付款，另外2×216＝432，已知項上限合計677.4817。內建imagegen實際美元、稅額、已付訂閱及未來額度未知，不能把677.4817當已支付總額或完整最終帳單。完整當日官方來源、費率假設及逐项算式見v3包。

本次 API 支出授權為0，前段美元方案沒有獲准。已唯讀查到實際 Mokaair `drama_enabled=false`、單集API上限200美元，未修改設定。送出前仍需當期其他保留額、正常look核准SHA、真實TTS時間、首末格SHA與storyboard；已完成的圖像採用與plan lock指紋見決策收據。

任何request回覆不明先查job、餘額和收據；不把timeout當作免費失敗重送。達單鏡／批次／額度期上限、同缺陷兩次、左右／身份或道具連戲不明，就停該鏡及依賴鏡，保留已有合格素材。

## 所有權及後續接線

[本交接票](../../../../../../tasks/open/2026-10-08-ou-de-jianghu-visual-handoff.md)目前只持有handoff範圍。production README過期角色數、正式工作檔採用與原試播票依賴接線，取得原持有人交接後再改；本README不是對另一持有者的機械鎖。第8集劇情與後續14人／16造型仍由各自票推進，不阻塞首集規劃包交審。

文件與工程透過既有草稿PR #1388保存。媒體原件及正常plan lock存repo外，repo內保存來源、提示、版本、原生尺寸、SHA與正式採用決策；已有4支Hailuo付費外部原片，其中新053因裁冠hold，前三支的10.75秒無聲重剪已採用。尚無TTS、正式整集輸出或上架。沒有填寫不存在的judge、choice、look、audio或storyboard核准。
