---
id: 2026-10-20-curio-s52-tahiti-venus-transit
title: Curio S52 Tahiti Venus transit sourced preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T16:38:13Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s52
---

# Curio S52 Tahiti Venus transit sourced preproduction

## Why

站主要求依推薦方案繼續製作更多**不重複**的奇聞檔案局歷史長片。S52 選 1769 年奮進號在大溪地觀測金星凌日：六月三日無雲，庫克仍寫下三位觀測者對「接觸太陽邊緣」的時刻差異。題庫 S01–S36、現有 `curio-s01`–`curio-s51` 的 brief 與任務票未見相同事件；S43 的 1835 年達爾文大溪地航段另是不同年代及事件。以可直接重新下載的庫克日誌轉錄與 Kippis 近時代傳記先做題材可行性，兩者不是兩次獨立觀測證據。

## Definition of done

- [x] A／B 企劃、推薦 A 的一條故事主線、30–60 秒濃縮開場及 5 秒片頭／21 秒片尾與連結規格已寫成 `docs/videos/curio-s52/brief.md`。
- [x] 兩份直接可取用的固定 Git 文字與 SHA、行段、當日與後出編輯的界線寫在 `docs/videos/curio-s52/research.md`。
- [x] R2 題材／大綱由另一人按當時 hash 獨立覆核通過；作者完成逐句主張表、至少八分鐘估時正文劇本與書面畫面，R3 精確 hash 見 `review/r3-author-freeze.md`。
- [x] R3–R6 作者、獨立來源／畫面及雙人敘事審核紀錄已保存；R6 來源／畫面 PASS、敘事 FAIL。R7 來源／畫面公開資料三處 HOLD，正式敘事四項 FAIL。R8 獨立史料／書面畫面因 4 月 17 日誤寫成 5 月 17 日而 HOLD／HOLD，雙人敘事合併三題 FAIL。R9 史料／書面畫面 PASS，但兩位新盲讀共同否決章界、重述與旁枝；R10 作者已修稿但正文按 300／325 CPM 只約 7:14／6:49。R11 找到固定 1771 年皇家學會觀測原報 OCR，新增校鐘、三人分列觀測與 Cook 對微光和暗影幾秒不確定的敘述；正文 300／325 CPM 估 8:53／8:23。R11 仍待獨立來源／畫面、全新雙盲與真實語音時長。
- [ ] 依精確稿完成政策、網站、TTS／音檢、MiniMax 原生畫面、動畫片頭片尾、成片／上架包及 Studio 連結檢查；未經各關卡前不稱影片完成。

## Steps

- [x] 查題庫與既有 S 軸劇本，排除題目重複。
- [x] 從 GITenberg 固定 commit 直接下載庫克日誌、Kippis 傳記全文，計本地 SHA 並抽查 1769-06-03 段落。
- [x] 編推薦 A「晴天仍有讀秒分歧」及備案 B「失而復得的象限儀」；將殖民敘述和二手轉述界線寫入企劃與研究。
- [x] 依 R1 獨立覆核 HOLD，在 R02 與 A 線補 C 5404–5425 的 4 月 15 日觀測處開槍死亡事件，凍結 R2 作者版。
- [x] 另一位工作者獨立核 R2 的 C 行段、來源層次與 brief／research 差分。
- [x] 依站主推薦 A 寫完 R3 作者逐句劇本、主張表與分鏡；lint 0 錯誤／0 警告。
- [x] 對 R3 精確五檔完成新一輪獨立史料／畫面與雙人敘事，並按共同 FAIL／HOLD 指出修成 R4 作者候選；結果不放行後續關卡。
- [x] 對 R4 精確五檔重做獨立來源／畫面與兩位新讀者盲評；來源／畫面 PASS，合併敘事 FAIL，結果見 `review/r4-source-independent.md`、`review/r4-official-panel.md`。
- [x] 對 R5 精確五檔重做獨立來源／畫面：三處限縮 HOLD，見 `review/r5-source-independent.md`；作者在 R6 定點修補。
- [x] 對 R6 精確五檔重做獨立來源／畫面：**PASS／PASS**，見 `review/r6-source-independent.md`。
- [x] 兩位新讀者對 R6 精確 `script.md` 盲評；共同四項必答 No，正式合併 **敘事 FAIL**，見 `review/r6-official-panel.md`。
- [x] 對 R7 精確五檔重做獨立來源／畫面覆核及兩位全新隔離讀者盲讀：公開資料三處使來源關 HOLD，正式敘事四項 FAIL，見 `review/r7-source-independent.md`、`review/r7-merged-narrative.md`。
- [x] 對 R8 精確五檔重做獨立來源／書面畫面：日期與兩個提示詞錯月，HOLD，見 `review/r8-source-independent.md`。
- [x] 兩位 R8 新隔離讀者正式合併：`payoffs`、`no_recap`、`no_detour` 三項 FAIL，見 `review/r8-merged-narrative.md`。
- [x] R9 作者修正 4 月 17 日及兩個插圖提示詞、修三項敘事失敗，重生稿並凍結五檔，見 `review/r9-author-freeze.md`。
- [x] R9 獨立史料／書面畫面 PASS，兩位新讀者正式合併 `chapters_link`、`no_recap`、`no_detour` FAIL。
- [x] R10 作者按共同失敗點修稿並重生逐句主張與分鏡，凍結五檔與時長風險。
- [x] R11 找到直接相關固定原報轉錄，增加鐘的校時和接觸判讀細節，凍結五檔、主張、畫面與保守估時；作者檢查不等於獨立 PASS。
- [x] 對現行 R15 精確五檔由另人獨立查核來源／書面畫面 **PASS／PASS**，兩名全新隔離讀者各 13／13 並正式合併 **13／13 PASS**；實際 TTS 正文 **10:23.30**。證據見 `docs/videos/curio-s52/verify-15.md`。
- [ ] R15 兩輪定點重配後正式音檢仍有 18 旗標；先按 `review/r15-audio-final-flag-review.json` 獨立聽辨現有 WAV，網站音訊卡待站主審。音訊未放行前不做付費插圖或後續成片。
- [x] R16 作者依 18 旗標定點改 18 句口播與主張，重生劇本並凍結五檔；最快估算正文 8:25.43、lint 0／0，見 `review/r16-author-audio-clarity.md`。未作新音檔或付費插圖。
- [x] R16 獨立史料／書面畫面 PASS、全新隔離雙讀者正式合併 13／13 PASS；只合成 18 句，其餘 101 句沿用，實際正文 10:43.17。正式音檢三輪均 119／119、僅 `s52127` 旗標；同文定點重配已達兩次上限。見 `review/r16-source-independent.md`、`r16-isolated-merge.md`、`r17-author-single-line-fix.md`。
- [ ] R17 只改 `s52127` 一句與對應主張、重生劇本；須另一人核精確來源／書面畫面差分及兩名全新隔離讀者盲評，之後才重配新句與正式音檢。R16 舊 WAV／政策／網站劇本卡均不可冒作 R17 核准；網站音訊卡仍待站主。

## How to verify

在 repo 根執行 `sha256sum /tmp/curio-s52-sources/{cook-8106,kippis-7777,rsc-106113}.txt`，前兩份應得 `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`、`c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`，第三份應得 `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`；若容器換掉，照 [`research.md`](../../docs/videos/curio-s52/research.md) 的固定 URL 重下再核。直接讀 C L5049／L5439–5457／L5592 的四月與五月邊界、L5371–5425、L5942–5984 與 K L1133–1182，確認開槍事件、庫克未在場、日期、分遣、晴天、暗影及讀時層級。`npm run check:tasks` 驗證本票；這不是音訊或媒體測試。

## Notes

- 2026-10-20：題材可行性已完成；直接下載 C（Cook 1769 日誌、1893 Wharton 編輯轉錄）21,861 行與 K（Kippis 1788 左右近時代傳記）15,413 行。Kippis 沿用既刊航海／觀測材料，不當第二次獨立實驗；只印格林一人四個接觸時間，不能倒推三人確切秒差。
- C 的**1893 編者前言** L1069–1073 誤寫凌日 `June 1st`，但庫克**當日日誌** C L5963 起寫 6 月 3 日，K L1151 也記 3 日。後續旁白須用 6 月 3 日，不把編者錯誤當歧見或把「暗影」直接判成已證實的現代單一光學機制。
- B 案的 5 月象限儀失竊會牽涉英國人扣船／拘押酋長，不能以輕鬆神探語氣省略殖民強制，故推薦 A。雲端仍無 S52 逐句稿、語音、插圖、影片或上傳；任何 8–11 分鐘只是企劃目標。
- 2026-10-20 R2：R1 題材獨立覆核僅對 A 的觀測處段 HOLD；作者在 R02、A 故事線與節拍補明一名大溪地人於 4 月 15 日被英國留守隊開槍打死，Cook 當時不在帳篷現場。精確固定 URL、來源層次、畫面邊界與 `brief.md`／`research.md` SHA 見 [`r2-author-freeze.md`](../../docs/videos/curio-s52/review/r2-author-freeze.md)。待**另一人**核 R2 差分；作者未簽獨立 PASS，亦未寫逐句稿或製作媒體。
- 2026-10-20 R2 獨立覆核已對當時題材／大綱 PASS：[`r2-feasibility-independent.md`](../../docs/videos/curio-s52/review/r2-feasibility-independent.md)。上條保留當時待核快照，不能把其舊 hash 沿用為 R3 逐句 PASS。
- 2026-10-20 R3 作者凍結：[`r3-author-freeze.md`](../../docs/videos/curio-s52/review/r3-author-freeze.md) 記目前 `brief/research/claims/video/script` 五檔 SHA、固定來源 SHA、139／139 逐句對齊、136 景中 132 張插畫／4 卡、17 loops、lint 0／0，以及正文 250／300／325 CPM 估 627.7／543.0／513.4 秒。5 秒片頭及 21 秒片尾只作製作規劃；未做付費媒體，未取得 R3 獨立查核、站台稿核准或任何成片／Studio 驗收。下一手先按 R3 hash 審稿，再逐關製作。
- 2026-10-20 R3 獨立逐句史料／書面畫面覆核 [`r3-source-independent.md`](../../docs/videos/curio-s52/review/r3-source-independent.md) 為**限縮 HOLD**。固定 Cook／Kippis 原文 SHA 與五檔 R3 hash 均核對；139 句對齊、132/136 插圖提示詞、17 loops、lint 0／0、最快正文 8:33.37 均通過。須先修 `s52019` 對派船者「互相比較」目的的超證據說法、`s52028` 畫出的近旁屋舍與 Cook 原文衝突、`s52117` 把 Kippis 表前 `According to Mr. Green` 說成表頭及連帶提示詞；另建議收窄 `s52135` 來源層級並校正 `s52076` 的四月畫面日期。完成 R4 作者凍結後需另人核 R4 精確差分及兩位隔離盲讀；R3 不得進政策／媒體關卡。
- 2026-10-20 R3 [正式雙人敘事](../../docs/videos/curio-s52/review/r3-official-panel.md) **FAIL**：共同 `chapters_link`、`no_recap` No；另有 4 月岸界段過長及 `s52065→66` 假回收的單讀者異議。R4 作者已按這些診斷及上述來源 HOLD 定點修稿，精確五檔 hash、17 處改句、9 個刪除景、8 個書面提示詞差分及估時見 [`r4-author-freeze.md`](../../docs/videos/curio-s52/review/r4-author-freeze.md)。R4 130/130 對齊、123 插圖／4 卡、17 loops、lint 0／0、最快估時正文 8:06.87；這些都是**作者本地檢查**。下一手先做 R4 獨立來源／畫面與兩位全新盲讀；其後才可做全稿政策、站台劇本卡、實測 TTS／音檢及付費畫圖。
- 2026-10-20 R4 [獨立史料／書面畫面覆核](../../docs/videos/curio-s52/review/r4-source-independent.md) 對精確五檔 **PASS／PASS**：重開固定 Cook／Kippis 全文核驗 R3 HOLD 修正、4 月 15 日庫克不在場的致命開槍、6 月 3 日凌日與 Kippis 表前散文；另核 130/130 主張對齊、123 張插圖提示詞、17 loops、lint 0／0、最快估時正文 8:06.87。`s52014` 複合場景列為生成圖驗收 WATCH。兩位 R4 新讀者盲評及後續政策、網站、真實音檢與媒體關卡仍各自待驗。
- 2026-10-20 R4 [全新隔離盲讀 A](../../docs/videos/curio-s52/review/r4-fresh-panel-a.md) 只讀精確 `script.md` SHA `89d271cea67b1e355f343f21fc90793218edc6d3880c2f0c50858fea3d818996` 與固定 13 題，答 **12/13 Yes**；必答 `no_recap` No，因 `s52131` 又說 `s52118` 已明講的「三人差幾秒算不出」，未點名回呼也無新結果。須等第二位真正隔離讀者同版答案及正式合併；A 單答不作最終敘事裁決。政策、媒體維持待驗。
- 2026-10-20 R4 [正式雙盲合併](../../docs/videos/curio-s52/review/r4-official-panel.md) **敘事 FAIL**：A 12/13、B 10/13，共同必答 `no_recap` No；B 另指出 4 月岸界佔用第二條主線及首章標題抽象。R5 [作者凍結](../../docs/videos/curio-s52/review/r5-author-freeze.md)把四月章壓成 14 景，開場不再問岸界，片尾刪去重述及岸界回拉；加上同一人表內兩段接觸間隔而不冒稱三人秒差。R5 121 句、114 插畫、4 卡、19 loops、lint 0／0，300 CPM 正文估 8:01.80、325 CPM 估 7:35.20；後者不足 8 分鐘，須真實 TTS 實測並視結果補充有來源的新內容。R5 尚未獲獨立來源／畫面、雙盲、政策或媒體放行。
- 2026-10-20 R5 [獨立來源／書面畫面覆核](../../docs/videos/curio-s52/review/r5-source-independent.md) 對凍結五檔為 **HOLD／HOLD**。格林表內上午 18:22、午後 18:02、相差 20 秒及跨 6:06:28 均重算正確，未當三人差；四月十五日開槍死亡與庫克非現場目擊也有據。須修 `s52204` 口播的「三點三十二分十分秒」為「三點三十二分十秒」、`s52205` 主張表補 Cook L5963–5975 引用，以及 `s52074` 畫面 `late afternoon light` 與清早離岸相反。作者修後重生劇本、另凍結 hash 再交獨立覆核；R5 尚不放行雙盲以後的關卡，真實語音八分鐘硬關仍待驗。
- 2026-10-20 R6 [作者定點修補](../../docs/videos/curio-s52/review/r6-author-freeze.md)只改上述 `s52204` 精確秒數口播／主張、`s52205` 主張表增加 Cook 原文引用、`s52074` 提示詞改六月二日清早光線，重生劇本；brief／research 僅同步目前版本與審核狀態。121 句、114 插畫、4 卡、19 loops，lint 0／0；估 300 CPM 正文 8:01.60、325 CPM 7:35.00，仍須實測 TTS。R6 不沿用 R4 PASS 或 R5 HOLD 作獨立簽核，未做任何 S52 付費媒體。
- 2026-10-20 R6 [獨立逐句來源／書面畫面覆核](../../docs/videos/curio-s52/review/r6-source-independent.md) 對精確五檔 **PASS／PASS**：Kippis 15:32:10 已口播成「三點三十二分十秒」，`s52205` 同引 Kippis 四格和 Cook 內接觸難判，`s52074` 清早光線與 Cook 6 月 2 日相符。逆轉這三處後的 `video.json`、`claims.md`、工具重生劇本均精確還原 R5 SHA，無其他逐句／提示詞漂移。格林同一人表內 18:22、18:02、20 秒差與四月十五日 Cook 非目擊界線仍成立；121/121 對齊、19 loops、lint 0／0。兩位 R6 新隔離讀者、政策／網站、真實 TTS 八分鐘及媒體關卡仍各自待辦；沒有付費媒體。
- 2026-10-20 R6 [兩名新讀者正式合併](../../docs/videos/curio-s52/review/r6-official-panel.md) **敘事 FAIL**：A 9/13、B 8/13，共同 `chapters_link`、`payoffs`、`no_recap`、`no_detour` 四項 No；B 另認為開場先洩漏結果。R6 來源／畫面 PASS 只綁原五檔，不可挪給 R7。
- 2026-10-20 R7 [作者修稿凍結](../../docs/videos/curio-s52/review/r7-author-freeze.md)：四月死亡事件明列企劃、研究與說明欄，旁白刪去支線但保留當地人在場及庫克對溝通的不確定；各章起句回應前章具體問題，分遣隊「成功」與秒差疑問逐一回收，片尾改為史料閱讀動作。119/119 主張對齊、113 插畫／3 卡／1 片尾、18 loops、lint 0／0，300 CPM 正文 8:06.20，325 CPM 7:38.97；需真實 TTS 實測八分鐘。R7 尚待另一人獨立來源／畫面及兩名新讀者盲讀，沒有付費媒體。
- 2026-10-20 R7 [獨立來源／書面畫面覆核](../../docs/videos/curio-s52/review/r7-source-independent.md)：精確五檔主張 119/119 與書面畫面 113 插畫／3 卡均 PASS，但整關 **HOLD**：`s52069` 章名把 6 月 1、2 日兩支隊伍誤寫成同日出發，YouTube 說明「格林四個時刻只見於 Kippis」未限定本集來源範圍，`claims.md` `s52127` 殘留重複裸網址。作者修三處後重新凍結 hash、另人核差分；兩名新讀者盲讀、政策／網站／真實 TTS 及媒體關卡仍待辦。R7 本輪未產生付費媒體。
- 2026-10-20 R7 [正式雙人敘事合併](../../docs/videos/curio-s52/review/r7-merged-narrative.md) **FAIL**：A 12/13、B 9/13；合併 `no_spoiler`、`chapters_link`、`no_recap`、`no_detour` 四項 No。開場已說完整觀測、後文重說，接觸章第一句重述模糊邊緣，岸上炮位／界線／溝通段未推進讀秒主線。
- 2026-10-20 R8 [作者修稿凍結](../../docs/videos/curio-s52/review/r8-author-freeze.md)：開場只等接觸，不先說無雲或觀測結果；接觸章首句直接回答暗影對讀時的影響；四月旁白刪去炮位、溝通與隔日移船，保留當地人圍觀、設站，接到 5 月 17 日同處木星衛星食受雲阻礙及 5 月 30 日備援準備。修章名為 6 月 1–2 日、說明欄限縮格林四格來源、主張表去重複網址；5 月 31 日長艇完工補出發銜接。119/119 主張對齊、113 插畫／3 卡／1 片尾、18 loops、lint 0／0，300 CPM 開場 38.20 秒、正文 8:10.00；325 CPM 正文 7:42.53，仍須真實 TTS。R8 尚未獲獨立來源／畫面或雙盲通過，沒有付費媒體。
- 2026-10-20 R8 [獨立史料／書面畫面](../../docs/videos/curio-s52/review/r8-source-independent.md) **HOLD／HOLD**：Cook 文中 `[April 1769.]` 在 L5049，4 月 15、16、17 日連續記載在 L5370–5457，而 `[May 1769.]` 到 L5592 才開始；R8 新 `s52307` 卻說 5 月 17 日，`s52307/08` 兩個提示詞同寫 May 17，brief／research／claims 亦傳播錯月。其餘逐句與提示詞、公開章名與說明欄修訂、119/119 對齊、18 loops、lint 0／0 均已核，不能因此放行 R8。R9 把錯月統一修為 **4 月 17 日**，重生劇本、凍結五檔、另人再核。作者 R8 舊快照與上條舊敘述保留作歷史紀錄；未做 S52 政策、語音或付費媒體。
- 2026-10-20 R8 [雙人正式敘事合併](../../docs/videos/curio-s52/review/r8-merged-narrative.md) **FAIL**：A 13/13、B 10/13，合併 `payoffs`、`no_recap`、`no_detour` 三題 No。`s52078` 問全部外派讀時而 `s52128` 只答這段日誌，`s52132` 重述 `s52118` 的缺口，`s52036` 無武器與 `s52206` 曝曬溫度計高溫未推進讀時主線。R8 來源 HOLD 與敘事 FAIL 都綁舊五檔。
- 2026-10-20 R9 [作者修稿凍結](../../docs/videos/curio-s52/review/r9-author-freeze.md)：四月十七日同步至口播、主張、兩幅提示詞與企劃／研究；刪 `s52036`、`s52132`，改 `s52206` 為晴天至圓邊判讀的轉折，`s52078→s52128` 改為來源範圍清楚的問題與回收。115 景＝111 插畫／3 卡／1 片尾，117/117 對齊、18 loops、lint 0／0；300 CPM 正文 8:05.60、325 CPM 7:38.27，真實 TTS 八分鐘硬關仍待驗。影片文件測試 236/236；R9 尚無獨立史料／畫面、雙人盲讀、政策、網站或付費媒體通過。
- 2026-10-20 R9 [獨立史料／書面畫面覆核](../../docs/videos/curio-s52/review/r9-source-independent.md)對作者凍結的精確五檔為 **PASS／PASS**：重算五檔與固定 Cook／Kippis 全文 SHA；Cook 四月／五月月份邊界證明 4 月 17 日木星衛星食，旁白、主張、兩幅畫面、企劃與研究均已同步；外派隊逐人四格問題限於本集固定文本，4 月 15 日死亡及 Cook 非現場目擊仍清楚標示。117/117 句與主張同序同字、111 幅提示詞、3 卡、8 章、18 loops、lint 0／0。兩位新讀者正式盲評及後續關卡仍待辦；真實 TTS 必須驗證八分鐘正文，動畫、成片和 Studio 可點連結尚未製作或驗收。

- 2026-10-20 R9 [雙人正式敘事合併](../../docs/videos/curio-s52/review/r9-official-panel.md) **FAIL**：A/B 都是 10/13，合併 `chapters_link`、`no_recap`、`no_detour` 三項 No。R10 已處理三處章界、重複分遣理由、同行者姓名旁枝及表格間隔口算；不要把 R9 PASS 的來源稽核當作 R10 媒體放行。
- 2026-10-20 R10 [作者修稿凍結](../../docs/videos/curio-s52/review/r10-author-freeze.md)：103 景＝100 插畫／2 卡／1 片尾，105/105 主張對齊、18 loops、lint 0／0；300 CPM 正文 7:14、325 CPM 6:49，尚未達八分鐘保守估計。現有來源與畫面書面包／新雙人盲讀須按 R10 hash 另行驗證；本輪無付費媒體。

- 2026-10-20 R11 [作者修稿凍結](../../docs/videos/curio-s52/review/r11-author-freeze.md)：新增 1771 原報固定 OCR，避免 R10 未滿八分鐘時回填被否決的旁枝；現有稿 120 句、115 插畫／2 卡／1 片尾、lint 0／0，300／325 CPM 正文 8:53／8:23。原報分列三人，但 OCR 表格排版混亂，不算精確秒差。須另一人按 R11 精確 hash 重新覆核來源與全新雙盲，再做政策、站台及真實 TTS；此輪無付費媒體。
- 2026-10-20 R12 [作者畫面定點修正](../../docs/videos/curio-s52/review/r12-author-freeze.md)：R11 獨立史料 PASS、書面畫面唯一 HOLD 是 `s52128` 誤畫三支外派隊；只將提示詞 `three` 改 `two`，`script.md`／主張／企劃／研究四檔 SHA 均未變，lint 0／0、最快估算正文 8:22.63。須由另一人對 R12 精確 `video.json` 做畫面差分覆核；沒有付費媒體。
- 2026-10-20 R12 [獨立來源／書面畫面](../../docs/videos/curio-s52/review/r12-source-independent.md) PASS／PASS；[兩位真正隔離的盲讀合併](../../docs/videos/curio-s52/review/r12-merge.md)為 12／13，唯一共同否決 `no_recap`。R13 [作者定點修稿](../../docs/videos/curio-s52/review/r13-author-freeze.md)只改 `s52053`、`s52116`、`s52316` 的旁白與三列主張，0 lint error／warning，最快估算正文 8:18；R13 尚待獨立來源／畫面與全新隔離盲評，真實 TTS／付費媒體均未開始。
- 2026-10-20 R14 [作者單景時序修正](../../docs/videos/curio-s52/review/r14-author-freeze.md)：獨立畫面閱讀指出 `s52053` 的 `late May` 與下一句原報 5 月 10 日儀器完成不合；提示詞只改 `early May`，劇本、主張、研究、企劃原雜湊未動，lint 0／0。需另人對 R14 精確差分核章界畫面，R13 敘事文字仍需全新隔離盲讀；無媒體。
- 2026-10-20 R14 [隔離雙盲正式合併](../../docs/videos/curio-s52/review/r14-isolated-merge.md)為 12／13，唯一共同否決 `no_recap`，相鄰 `s52122`／`s52315` 重說原報分列三位觀測者。R15 [作者最小刪除](../../docs/videos/curio-s52/review/r15-author-freeze.md)僅刪後句場景和主張，將 `s52007` 伏筆回答點指向 `s52122`；重生劇本、lint 0／0，最快估算正文 8:12.37。需新 hash 的獨立來源／書面畫面與全新隔離雙盲；未做付費媒體。
- 2026-10-20 R15 [完整驗證與音檢](../../docs/videos/curio-s52/verify-15.md)：五檔凍結 SHA 未改；獨立史料／書面畫面 PASS／PASS、兩位隔離敘事各 13／13 與正式合併 13／13、lint 0／0。首次政策因站台尚未註冊 S52 而錯套 `tutorial` 示範題 FAIL；`review-push --report-only` 註冊現有 `category: explainer` 後，相同 `policyRequest` SHA `fe9d19820038a4ef9eae279fb2624062743f0b5c80a1ba5ed003952b22c7225b` 以正確 `explainer` 題組 PASS。網站 outline／script／audio 三卡均待站主；本機僅 outline／script 有依常設委託記的委派編輯批准，未冒稱網站核准。Gemini Sulafat 初配 117 requests／2,571 字，兩輪只對官方旗標定點重配 30／705 字與 12／309 字；最終正文 18,699 frames／30 fps＝**10:23.30**、開場 43.87 秒、整段 11:24.97，WAV SHA `7f9ff69bfc3d709ba73d822767070254a2d0955457eb5697fb002f7a0c1a8c95`、timeline SHA `4c60f8f5e3b1ed502421c2bf10228c79a48d995c1dca7300490f3845e6c505a8`。正式全檢三輪 119／119，旗標 **30→20→18**；最終 `check.json` SHA `879e5813b7e967528c17f8c293dd5550b7b79d2127e432fb426a92f2afa8a6be`、原樣 `check-flags.json` SHA `a3f691fd4d79d9e626c4d807364e32787b3396916db8f63ac3f034de0efe8d85`。逐句音檔路徑／SHA、原文／ASR、暫定 7 語義文本差異與 11 疑似近音誤判見 [18 句待聽清單](../../docs/videos/curio-s52/review/r15-audio-final-flag-review.json)；分類沒有獨立聲學聽證。**音訊 HOLD，禁止第三輪重配或付費插圖；下一手先獨立聽辨現有 18 個 WAV、讓站主處理網站音訊卡，再決定是否需修句及重跑相關關卡。**
- 2026-10-20 [R15 音訊獨立技術核對](../../docs/videos/curio-s52/review/r15-audio-final-independent.md)：18 個現行 WAV 的 SHA、PCM 格式與解碼、逐句轉寫與時間格均核對；此工作階段的音訊輸入不支援模型聽音，**18／18 聲學判定仍 HOLD**。報告逐句區分 ASR 文本風險與未證實的口播，沒有重配或改稿。待可真正聽音的審稿者按原 SHA 逐句判定，音訊關及後續媒體仍不得放行。
- 2026-10-20 [R16 作者口播易辨改稿](../../docs/videos/curio-s52/review/r16-author-audio-clarity.md)：18 句僅改措辭與對應主張，基皮斯等易誤轉人名以有來源層級的「後來的庫克傳記」承接，秒數／三處逐人／原報／內接觸等以明確語境展開；同一秒的開場懸念、後出單人表與 1771 原報分列三人、外派兩隊資料界線仍保留。`brief.md`／`research.md` 未改，五檔 SHA 與全差分見凍結檔；119／119 主張對齊、lint 0／0，最快正文 8:25.43。R15 舊 WAV 與 18 旗標聲學 HOLD 不屬於 R16；作者未簽新稿獨立 PASS，未做 TTS 或付費插圖。下一手先做獨立審稿，再按新雜湊處理政策、劇本與受影響語音。
