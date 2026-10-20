---
id: 2026-10-20-curio-s49-1835-moon-hoax-source
title: Curio S49 1835 Moon Hoax source-audited preproduction
status: in-progress
priority: P2
area: docs
owner: codex-s49-r15-policy-tts
claimed_at: 2026-10-20T19:49:06Z
created_at: 2026-10-20T15:07:01Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s49
---

# Curio S49 1835 Moon Hoax source-audited preproduction

## Why

站主要求持續做不重複的歷史長片，並採編輯推薦方向。原擬 1904 聖路易奧運馬拉松所需官方報告在此環境遭 egress `CONNECT 403`，不從記憶寫實；故選題庫 U30 的 1835 年《紐約太陽報》「月球大騙局」，S01–S48 沒有此題。以 1859 年 Locke 名下重印本及 Harold Jacoby 1902 天文評論寫一張報紙如何層層造出月面居民；把 1859 出版者宣傳與同時代新聞選錄分清。

## Definition of done

- [x] A／B 企劃推薦 A、固定來源 URL/SHA 與精確段落，標出重印本／後出分析界線。
- [x] 30–60 秒濃縮、原版 5 秒片頭位置、正文保守至少八分鐘的繁中逐句稿及 `video.json` 對應。
- [x] 逐句來源與書面畫面提示、lint 0 error／0 warning、作者自檢與未完成關卡交接。
- [x] R1 獨立覆核 HOLD 的來源錨點、旁白及書面畫面 R2 差分修復；作者收據記精確 SHA。
- [x] R12 精確稿經兩位全新隔離讀者的正式敘事關卡合併 PASS。

## Steps

- [x] 查 S01–S48 與題庫；確認不重複並留原馬拉松來源跟進票。
- [x] 固定下載 Locke 1859／Jacoby 1902 全文、記 SHA 與來源限制。
- [x] 生成 133 景、136 句／12 個 loops，重生 `script.md`，檢查同文與時間。
- [x] 執行 lint 與 task 檢查、記六份交付的精確 SHA 後釋出本票。
- [x] R2 對照 R1 逐項修復，重生劇本並重核 136 句逐字一致、保守正文八分鐘及畫面比例。
- [x] 另一位覆核者按 R2 精確雜湊重讀固定來源、逐句錨點與書面畫面，留下獨立結論。
- [x] R2 兩位隔離讀者對精確 payload 回答固定 13 題，封存原始答案、工具合併結果及全部分歧；結果 FAIL。
- [x] R3 作者窄修 `payoffs`、`no_recap`，重生劇本並完成受影響句子、錨點與書面畫面的差分自檢。
- [x] 另一位覆核者按 R3 精確雜湊重核受影響來源與書面畫面；僅 `moon129` 來源措辭 HOLD，書面畫面 PASS。
- [x] R4 作者窄修 `moon129` 的直接歸屬與雙來源錨點，重生逐字稿、凍結雜湊和靜態檢查。
- [x] 另一位覆核者按 R4 精確雜湊重核 `moon129`；旁白與畫面 PASS，但來源註解兩欄 HOLD。
- [x] 窄修 `research.md` 的 J／P13 歸屬，保留 R4 台詞與 claims；記新研究雜湊。
- [x] 新來源註解差分由另一人獨立覆核 PASS；R4 兩名新讀者的編輯診斷均指出敘事問題，不計正式 script-only 盲讀。
- [x] R5 作者依診斷修正故事順序、開場劇透、重述／支線與問題回收；重生稿件、對齊主張表並凍結五檔雜湊。
- [x] 另一位工作者按 R5 精確檔重核固定來源及書面畫面：旁白／主張 PASS，`moon103` 提示詞窄 HOLD。
- [x] R5 兩位新讀者重審：B 嚴格 script-only，`payoffs/no_recap` FAIL；A 也判 `no_recap` FAIL，但讀過通用指引而標示隔離限制。
- [x] R6 作者窄修 `moon049–051` 的問答重述及 `moon103` 的錯置畫面，補 P05a 來源、重生劇本並凍結精確雜湊。
- [x] 另一位工作者按 R6 精確版重核四景書面畫面、三句新旁白與 P05a；兩名全新**只讀劇本**的讀者重做正式 13 題評分；來源 PASS，兩人共同否決 `payoffs/no_recap`，A 另否決 `no_detour`。
- [x] R7 作者窄修上述共同失分與 A 支線，對齊 `claims.md`／畫面提示、重生劇本、精確凍結五檔雜湊，完成 lint、時間及測試。
- [x] 另一位工作者按 R7 精確版重核九句、三景書面提示與 P08 來源註解；兩名全新 script-only 讀者做正式十三題雙盲；來源 PASS，敘事合併 FAIL。
- [x] R8 作者窄修 `moon005/013/122` 的重述與切換句，同步一景提示詞及主張表，重生劇本、凍結 SHA、檢查八分鐘正文與 lint。
- [x] 另一位工作者按 R8 精確版重核三句的固定來源及 `moon122` 書面提示；兩名全新 script-only 讀者正式十三題雙盲。
- [x] R9 作者依 R8 兩輪音檢餘下六句旗標窄修旁白及對應 claims，重生劇本並凍結五檔 SHA。
- [x] R9 另一位工作者對六句、相應 claims 錨點／書面畫面及其餘未改內容完成獨立差分覆核；旁白／畫面 PASS，兩個 claims 直接錨點窄 HOLD。
- [x] 按 R9 窄 HOLD 只修 `moon012/015` 兩個 `claims.md` 來源錨點，凍結新 SHA；另一位工作者獨立重核 PASS。
- [x] R9 兩位全新隔離讀者正式十三題盲評合併 FAIL（12/13，兩人均否決 `no_recap`，各指出一處不同重述）。
- [x] R10 作者同時窄修 `moon014/015` 與 `moon023/026/027/029` 兩處重述，重生劇本、補直接錨點、凍結五檔 SHA，完成時間與靜態檢查。
- [x] 另一位工作者按 R10 精確版差分重核固定來源／書面畫面 PASS；兩位全新隔離讀者重做正式十三題雙盲，合併 FAIL（`payoffs`）。
- [x] R11 作者窄修 `moon019` 增刊可核答句及 `moon022` 格蘭特來信問題，對齊主張、書面畫面與劇本，完成五檔精確凍結及靜態檢查。
- [x] 另一位工作者按 R11 精確版差分重核固定來源／書面畫面 PASS。
- [x] 兩位全新隔離讀者重做 R11 正式十三題雙盲：兩人均否決 `payoffs` 與 `no_recap`，官方合併 FAIL（11/13）。
- [x] R12 作者按 R11 正式失分窄修並凍結五檔精確 SHA；保留史料範圍與圖像示意界線，lint 0/0。
- [ ] 另一位工作者按 R12 凍結檔獨立重核來源／書面畫面；兩位全新、只讀腳本的讀者正式十三題雙盲並合併 PASS，再做必要後續關卡與新稿完整音檢。

## How to verify

在 repo 根目錄跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json`、`npm run check:tasks`；R2 作者收據見 [`docs/videos/curio-s49/verify-2.md`](../../docs/videos/curio-s49/verify-2.md)，獨立來源與書面畫面結論見 [`docs/videos/curio-s49/review/r2-source-independent.md`](../../docs/videos/curio-s49/review/r2-source-independent.md)，正式雙盲敘事結論及原始 JSON 見 [`docs/videos/curio-s49/review/r2-official-panel.md`](../../docs/videos/curio-s49/review/r2-official-panel.md)。前製 lint 與獨立文字查核都不等於 TTS 或媒體實測。

## Notes

- 2026-10-20：[R11 官方雙盲](../../docs/videos/curio-s49/review/r11-official-panel.md)兩人一致給 11/13，`payoffs`／`no_recap` **FAIL**。[R12 作者窄修與五檔精確凍結](../../docs/videos/curio-s49/review/r12-author-freeze.md)把開場第二觀測問題限於本次核對的重印本與 Jacoby 評論、用 L1619–1626 的「三月新月」回收持續月面觀測的時間，並整理南行、重印書及《晚郵報》段落的重述。R12 `video.json` SHA `bfff58fdda9eb5501fb46d5211222cb135dff30a4c0a25223e7a10884d6a4c06`、`script.md` `ab8e840e2c74b283b60e65e62d62e41d79d6eea0ded323e4888a3940de80ab7e`、`claims.md` `e87359c6f7e53f6567fb82697cebbdf39e171dda423483b8ace117a5c9561658`；其餘兩檔見凍結表。133 句／130 編號景／11 loop，lint 0/0。**R12 獨立來源、兩位新盲讀及完整新音檢仍待，付費媒體停。**
- 2026-10-20：[R11 固定來源及書面畫面獨立覆核](../../docs/videos/curio-s49/review/r11-source-independent.md)按五檔精確 SHA **PASS**：`moon019` 限定本次沒查到增刊原件，L145–165 是 1859 重印，J4063–4070 是 1902 評論，沒有把 Jacoby 的紐約推測說成確定；`moon022→023` 收窄 Grant 來信問題並直接回收，L224–239 僅證明報導自稱。兩景畫面均為無字示意，沒有當成原件。133/133 劇本、130/130 claims、11 loops 對齊，lint 0/0；其後 R11 敘事結論見上項。付費媒體停。
- 2026-10-20：[R10 來源／書面畫面獨立覆核](../../docs/videos/curio-s49/review/r10-source-independent.md)依凍結五檔 **PASS**；[R10 官方雙盲](../../docs/videos/curio-s49/review/r10-official-panel.md)兩名新讀者共同否決 `payoffs`，合併 **FAIL，12/13**。兩人均指出 `moon018→019` 對被冒稱增刊的查閱位置沒有直接回答；A 另指出 `moon022→023` 問所有見證者原始材料而只回答信件。[R11 作者窄修與五檔精確凍結](../../docs/videos/curio-s49/review/r11-author-freeze.md)讓 `moon019` 明答本次沒查到增刊原件、可翻的是 1859 重印本，並把 Jacoby 1902「稿件在美國製作」明確歸屬；`moon022` 收窄為開場 Grant 來信。`moon019` 改為無字重印書示意，兩行 claims 錨點縮到 L145–165／J4063–4070／L224–239。R11 `video.json` SHA `ff048feb89d227ed88f0ddd648a746ea5d41e70fde9a432f4f4ea80d062e42b9`、`script.md` `a9fb4bcc6e271609d79e34d2f4278cdb2c797d0fc8af32b52d4f68b3b1629259`、`claims.md` `867593fb21255f4b4764471347f8ebe779241931537970294ec39cca12d2e1fb`；brief／research 沿用 R10。133/133 劇本、130/130 claims、124/124 shot、6/6 big 對齊，11 loops 有效，lint 0/0，正文最快文字估 **8:12**，docs-videos 236/236，check:tasks 成功。**R11 獨立來源／書面畫面與新正式雙盲仍待；舊音訊不代表 R11，付費媒體仍停。**
- 2026-10-20：[R9 獨立差分覆核](../../docs/videos/curio-s49/review/r9-source-independent.md)判六句旁白與書面畫面 PASS，僅 `moon012`、`moon015` 的逐句直接連結窄 HOLD。[作者錨點修補](../../docs/videos/curio-s49/review/r9-anchor-repair.md)只改這兩格，`claims.md` 當時 SHA `e008301ee9d75073bb7370bf6251ddb3eadc83032597a7f31217006f4bd66709`；劇本 `10f912c63ba438c676372469e8e44a52a8252113efc22f3af9fb74f91ae22354` 與影片 JSON `547409b2cb87e1ea5ba0133e3c140aa15ba4cce793e26a55d0cbde49fe1bb396` 未改。該版後續錨點與盲評結果見下項；R8 舊 WAV 不代表 R9 音檔，不可放行插圖。
- 2026-10-20：[R9 錨點獨立重核](../../docs/videos/curio-s49/review/r9-anchor-independent.md)已窄範圍 PASS；[R9 官方雙盲合併](../../docs/videos/curio-s49/review/r9-official-panel.md)仍 **FAIL，12/13**。A 指 `moon014/015` 緊鄰重說標題姓名；B 指 `moon023`、`moon026/027`、`moon029` 連說缺少文件。[R10 作者修復與五檔精確凍結](../../docs/videos/curio-s49/review/r10-author-freeze.md)保留 `moon023` 回收開場來信，刪除 `moon026/027/029` 三景及同三行 claims，`moon015` 改為僅問名字有無證據力，`moon028` 轉問望遠鏡如何看清月面；另補 `moon014/028` 逐句直接來源錨點。R10 `video.json` SHA `86361df066e0df920c5ae55055307eb4c6a46f1cae597c56569cb041f2732e80`、`script.md` `c6389ff27c36856a914442644b71f746c66a89ddb1bd8f0f14a3f086d09fa51c`、`claims.md` `f12b37209b51cb4888b0ff41c6f70bc5b7fecbeb721edf25a7c5fe60d189b034`，brief／research SHA 不變；133/133 劇本、130/130 claims、124/124 shot、6/6 big 同序同文，11 loop 有效，lint 0/0，正文最快文字估 8:10.71。**R10 尚待新稿獨立來源／書面畫面及兩位全新正式敘事盲評；R9 音訊 HOLD，不能用舊 WAV 放行新稿。** 未做政策、本站關卡、TTS 或付費媒體。
截至 2026-10-20，R1 獨立來源／書面畫面覆核曾為 **HOLD**；R2 精確版本已由另一人重核為**固定來源事實 PASS、書面畫面 PASS**。R2 正式雙盲敘事已完成但合併 **FAIL**；網站 A／劇本關卡、TTS、圖像、配樂與成片仍未完成。1859 重印本含出版社序與對 1835 報紙反應選錄；Jacoby 的報紙引句又取自該重印本，不構成對 1835 原紙的第二份獨立見證。六萬冊與發行量五倍只歸屬 1859 出版者。帶月面生物與巨鏡的畫面都是報導內容的卡通示意。R2 保守文字估正文 2,660 單位／325 單位每分約 8:11，須等實際音訊覆核；品牌片頭及 Studio 片尾框只有計畫。

2026-10-20 獨立來源與書面畫面覆核已落在 [`docs/videos/curio-s49/review/r1-source-independent.md`](../../docs/videos/curio-s49/review/r1-source-independent.md)，結論 **HOLD**：`moon083` 將原文「不像鳥」說反；`moon066` 與 `moon079` 書面提示分別指定無角動物、單隻翼人，與原文及當句旁白衝突；`moon123` 發行量數字連到錯的 `P13`，應改 `P02`。其餘需補的逐句錨點與用語見覆核；修正後重核，尚未生成或驗收圖片。

R2 作者修復對照 R1 全部發現，詳見 [`docs/videos/curio-s49/verify-2.md`](../../docs/videos/curio-s49/verify-2.md) 的差分、靜態檢查與 SHA。獨立重核收據是 [`docs/videos/curio-s49/review/r2-source-independent.md`](../../docs/videos/curio-s49/review/r2-source-independent.md)；**文字與書面分鏡 PASS 只對該文所列五個交付檔雜湊有效**，本站與媒體關卡均未放行。

R2 正式雙盲收據是 [`docs/videos/curio-s49/review/r2-official-panel.md`](../../docs/videos/curio-s49/review/r2-official-panel.md)：A 9／13 Yes、B 11／13 Yes；共同 No 為必答 `payoffs`、`no_recap`，故合併 **FAIL**。`one_line`、`no_toc` 是兩人的分歧，已原樣保存。精確 payload SHA-256 `c8498a352e93dee56842093c941bd3fba35e0000a0bf3ea96fd11ae059cc9eb9`，工具合併 JSON SHA-256 `a5a3bab1b729ce023e6c0e6bb172d3e654746c63846ae1d3b0ab45411ccc69f3`。R3 應先把 `[moon098]` 的驗證問題改成後文確實回答的問題，並刪減 `[moon009]`／`[moon052]`／`[moon129]` 的真旅程重述；改稿後重新做受影響的來源／畫面差分與雙盲。敘事未通過前不啟動媒體。

R3 作者差分與精確凍結見 [`docs/videos/curio-s49/verify-3.md`](../../docs/videos/curio-s49/verify-3.md)：`moon098` 現問巨鏡隔天發生什麼，`moon099`–`moon100` 接煙與鏡片聚光；`moon052`–`moon055` 改為報導內的裝機、保密與一月十日觀測；結尾引用 Jacoby 與重印本的來源關係取代重述，刪除原 `moon131`。`video.json` SHA-256 `34a47b39720958eae92c43b709cf018e6091ba12ea210b6d92ce32b54cbdef68`，`script.md` SHA-256 `6c2bb4db9e9cf15e503e15cadbd3acea52244f5f63fe756e1518ed25f0f10ca2`，`claims.md` SHA-256 `fa7eea4dad3f599762ac7f3211a4e881f1d8001175c4c2e0309d989eee8586ab`。作者 lint 0 error／0 warning、正文保守 8:07。

R3 [獨立覆核](../../docs/videos/curio-s49/review/r3-source-independent.md)於 2026-10-20 判 **固定來源事實 HOLD（僅 `moon129`）／書面畫面 PASS**：J 4178–4182 明說月球騙局正文引文出自重印本、該書也收各報意見；J 的各報摘句確能與 L 2092–2120 逐一比對，但現稿「他明說，報紙摘句都取自…」把交叉比對推論寫成 Jacoby 的直接宣告。請窄修此句與 `claims.md` 錨點、重生劇本、重核新 SHA，之後才用新精確稿做兩位全新隔離讀者的正式雙盲。媒體仍停。

R4 作者單句修復與精確凍結見 [`docs/videos/curio-s49/verify-4.md`](../../docs/videos/curio-s49/verify-4.md)：`moon129` 現說把 Jacoby 的各報引句逐一對照，也能在重印書找到；不再說他親口斷言各報摘句的來源。該列錨點同列 J4178–4205 與 L2092–2120。`video.json` SHA-256 `7c26a60db37f4e2cb866f2491a44e18dd5c458373f39677d4b350288a3578131`，`script.md` `da1dca236ce6b26d4785177f018d945df76f4fd1e149b547b808b3408d6e350d`，`claims.md` `8434bb5e2a25382d8a766759aa782ef529e0e891c44863f571bc58bc7a31d060`。作者 lint 0 error／0 warning，135 句逐字一致，正文保守 8:08；**尚無 R4 獨立來源結論或新雙盲**。媒體仍停。

R4 [獨立來源／書面畫面覆核](../../docs/videos/curio-s49/review/r4-source-independent.md)確認 `moon129`、錨點與畫面 PASS，卻發現研究表 J 與 P13 的舊歸屬過度，故**來源包 HOLD**。作者只修這兩欄，精確檔案見 [`verify-5.md`](../../docs/videos/curio-s49/verify-5.md)，`research.md` 新 SHA `7eeb561de83b136210972261724cb2fb978ccc44fd53d4b35e41291ab6c40714`；台詞、claims 和畫面版未改。第一組 R4 讀者因繼承 R2 裁決資訊，已自行撤銷正式盲讀資格，僅留非正式編輯診斷；重新交兩名無前輪上下文的讀者。新來源差分及正式雙盲結果未出前仍禁媒體。

R4 研究表 J／P13 兩欄[獨立差分覆核 PASS](../../docs/videos/curio-s49/review/r4-research-diff-independent.md)，解除來源包 HOLD。後續兩名新 R4 讀者均未接觸前輪報告，但指派時可讀 `brief.md`，故其[各自診斷](../../docs/videos/curio-s49/review/r4-fresh-panel-a.md)不計正式 script-only 雙盲；兩位都指出時間跳接、說明支線與重述等問題。R5 [作者凍結收據](../../docs/videos/curio-s49/verify-6.md)已修開場、1835→1859→1902 敘事順序、巨鏡及反應線，新增 1902 雅各比光學評論 `moon131`，不改已通過的 `research.md` 歸屬措辭。精確 R5 `video.json` SHA `38cd74741cfaf6b71e61456b6427abe73cae97b7c0a5339db643ed2604fa496f`、`script.md` `4e9277eb55f0a4c37af9736bb5053888117db84c3baed988575085ee02d1ac1b`、`claims.md` `d337719bb51353325fdf08bf0356c1732d1ac8f2b6761d420c90fa396a753f33`。Lint 0／0、136／136 句與主張表同序，保守正文 8:20。**R5 獨立來源與書面畫面、正式雙盲均待；沒有 TTS、付費圖或影片。**

R5 [獨立固定來源、逐句主張與書面畫面覆核](../../docs/videos/curio-s49/review/r5-source-independent.md)重開 L／J 位元組、讀完 136 句與 133 景後判**旁白事實／主張 PASS、書面畫面僅 `moon103` HOLD**：這景台詞強調火災只是虛構，提示詞卻寫 `at a real modest observatory` 並畫未核實的真站點開窗動作。只須窄改 `video.json` 該 prompt 與 `claims.md` 對應視覺欄，再由另一位來源／畫面讀者差分核對；R5 `script.md` SHA `4e9277eb55f0a4c37af9736bb5053888117db84c3baed988575085ee02d1ac1b` 可維持。R5 正式雙盲仍待，付費媒體仍禁。

R5 新讀者 B 嚴格只讀劇本，[13 題](../../docs/videos/curio-s49/review/r5-fresh-panel-b.md)判 `payoffs/no_recap` FAIL；A 亦判 `no_recap` FAIL，但揭露讀過通用技能檔，不能用於 R6 的正式核准。R6 [作者凍結](../../docs/videos/curio-s49/verify-7.md)把 `moon049–051` 轉成文章自述的鏡片到倫敦、器材跨海問答與高地運送，並把 `moon103` 改成讀者合上虛構火災報紙、旁放普通天文台草圖，去掉真站點開窗。新增研究 P05a 鎖 L501–568，明確不把牛隊指定為運鏡片唯一工具。R6 精確 SHA：`video.json` `5dc1602b0aeb254ea1c2b3d45ab9fbff15450fe73f80e06c202059cd6f3934b4`、`script.md` `dfc5ae984d4720f4c104edaf23cf1d7ff6bca5b05793b51fe32fdd59995fb8f8`、`claims.md` `a9f13314a1ab2776de217423b8cfc537ca5739ea09535f4d241a2d9791fc95ff`、`research.md` `73eb8e6f49f10ac4a0f275511913ccfff5c3f18eec6958cc6b25595eb20506d2`。Lint 0／0，136 台詞和 133 claims／畫面提示同文同序，開場最快估 32.49 秒、正文最快估 8:19.57；音訊未實測。**R6 獨立來源／畫面與兩名新 script-only 盲讀待辦，沒有 TTS、付費圖或成片。**

R6 [獨立固定來源／書面畫面差分覆核](../../docs/videos/curio-s49/review/r6-source-independent.md) **PASS**：直接重讀 L501–568、L1525–1564 和 J4085–4109，P05a 與三句新台詞成立；四景提示詞均保留虛構邊界，`moon103` 的 R5 畫面 HOLD 已解除。五檔雜湊仍等於作者 R6 凍結；136/136 逐字稿、133/133 主張 ID／台詞、126/126 shot 提示詞、7/7 big 字卡對齊，lint 0／0。兩名全新、只讀精確 R6 `script.md` 的正式敘事雙盲仍待；媒體仍停。

R6 兩名全新 script-only 讀者已交 [A](../../docs/videos/curio-s49/review/r6-fresh-panel-a.md)／[B](../../docs/videos/curio-s49/review/r6-fresh-panel-b.md)：兩人共同否決 `payoffs`（`moon073` 煙的提問未回答）和 `no_recap`（A 指 `moon013`、B 指 `moon095`），A 另否決 `no_detour`（`moon069` 跳到後來獨角獸講法）。R7 [作者凍結收據](../../docs/videos/curio-s49/verify-8.md)保留 133 景、136 句；以 `moon072–074` 的原文 *no doubt* 明答煙的推論，把 `moon009` 寫成開場回呼、`moon013/095` 改成向前推進，並以 L843–860 畫布與鬍子細節取代 `moon067–069` 的後世標籤支線。研究 P08 同時校正 *Valley of the Unicorn* 是山谷名。R7 `video.json` SHA `756d156dc25e390bf7e5bf771a376122f177f330df706408954616ac5d2777d6`、`script.md` `e31d202d5cb25b622839b50dab1448327585a7e5842f76d505dcb3e0994a56e3`、`claims.md` `0728ecd77e4933406db1dc72533fcdc1fd8acfd5cc4bdf886891fb6cd13943c1`、`research.md` `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3`；lint 0／0，開場 32.49 秒、正文按 325 units／分鐘 8:18.09，`test:docs-videos` 236/236，`check:tasks` 成功。**R7 獨立來源／畫面差分與兩名全新 script-only 雙盲仍待；先不要跑政策或媒體。**

R7 [獨立固定來源／書面畫面差分覆核](../../docs/videos/curio-s49/review/r7-source-independent.md)於 2026-10-20 **PASS**：固定 L／J 雜湊、九句台詞、三景提示詞及 P08 山谷名修正均核對；五檔仍等於 R7 作者凍結 SHA，136/136 劇本台詞、133/133 主張行、126/126 shot 提示詞和 7/7 字卡對齊，lint 0／0。`moon072` 的「屋頂」只可作冒煙小屋的通俗畫面，原文未指定煙囪或屋頂構造。**仍待兩名全新 script-only 讀者正式十三題雙盲**；此來源 PASS 不放行政策或媒體。

R7 [兩名全新讀者正式合併](../../docs/videos/curio-s49/review/r7-official-panel.md) A 12/13、B 11/13，兩人共同 `no_recap` No（A：`moon005/048` 小物可見重述；B：`moon122` 重新列稱讚、質疑與反諷），B 另 `no_toc` No（`moon013` 像宣告段落交接），故**敘事 FAIL**。R8 [作者窄修與精確凍結](../../docs/videos/curio-s49/verify-9.md)只動 `moon005/013/122`、`moon122` 一景書面提示詞及相應 claims，保留 133 景、136 句、11 loop；`video.json` SHA `1eaec3a24e656fe86e0cc5f48e5d61fa3a690b18aa7f4621960aa85f14f60baa`、`script.md` `f40259db7e16da37652689f0e2d703b8e03b8364d1738d0b4c2f848043618c8b`、`claims.md` `a010434fbbb2e498f6d064557b58e11cea338ccf93fc6300ab5960444f9e25e1`，brief/research 沿用 R7。Lint 0 error／0 warning，正文最快文字估 8:17.17，docs-videos 236/236。**R8 獨立來源／書面畫面及全新雙盲待辦；R7 PASS／FAIL 均不得移用。**政策、網站劇本卡及付費媒體仍未做。

R8 [獨立固定來源及書面畫面差分覆核](../../docs/videos/curio-s49/review/r8-source-independent.md)已按上述精確五檔雜湊 **PASS**：三句新旁白與 `moon122` 新示意提示詞均對應 L／J 固定原文，136/136 劇本句子、133/133 主張、126/126 shot、7/7 big 對齊，lint 0／0。仍待兩名全新 script-only 讀者正式十三題雙盲及合併；此 PASS 不放行政策或媒體。

R8 兩輪定點補錄及完整音檢見 [`verify-11.md`](../../docs/videos/curio-s49/verify-11.md)：首次 136/136、21 旗標；第一輪只補錄 21 句（509 billable characters），複檢 8 旗標；第二輪只補錄 8 句（191 billable characters），複檢仍有 **6 旗標**（`moon011/012/015/026/030/100`）。各輪完整 WAV、timeline、check、flags、被標單句 WAV 及逐檔 SHA manifest 已存 `/workspace/.video-work/curio-s49/review/r8-audio-archive/`，本次 R8 五檔文稿 SHA 未變。**音訊關 HOLD；兩輪 redo 上限已用盡，不送 audio gate、不作本機音訊核准、不啟動插畫／配樂／成片。** 下一步由作者實聽或以第二轉錄核對六句，必要時窄修並按新稿 SHA 重核下游關卡。

R9 [作者六句音訊措辭修復與凍結](../../docs/videos/curio-s49/verify-12.md)只改 `moon011/012/015/026/030/100` 的旁白及同六行 claims，CLI 重生劇本；沒有改其他 spoken text、畫面提示、loop、來源清單或片尾。精確五檔 SHA 見收據；`video.json` `547409b2cb87e1ea5ba0133e3c140aa15ba4cce793e26a55d0cbde49fe1bb396`、`script.md` `10f912c63ba438c676372469e8e44a52a8252113efc22f3af9fb74f91ae22354`、`claims.md` `34d270d19c80e8c5f81112e32ac2e79dde386839339cf708276a0626b7c8aa92`。136/136 劇本同文、133/133 claims 同文、11 loop 端點有效；開場最快估 32.49 秒、正文最快估 8:23.82。Lint 0 error／0 warning、docs-videos 236/236、check:tasks 成功。**R9 音訊關仍 HOLD；R8 舊 WAV 不等於新稿音檢。** 下一位依 R9 新 SHA 差分重核固定來源與書面畫面、做新稿正式敘事及必要後續關卡，再處理受影響音訊與 136/136 完整音檢；零旗標及必要核准前不進入付費媒體。

R9 [獨立固定來源／書面畫面差分覆核](../../docs/videos/curio-s49/review/r9-source-independent.md)按作者五檔精確 SHA 與固定 L／J 原文完成，**六句旁白事實 PASS、六景書面畫面 PASS，來源包因兩個 claims 直接錨點 HOLD**。`moon012` 的雙星／星雲在 J 4133–4137，而其可點連結只到 J 4050–4080；`moon015` 的 Herschel 標題在 L 152–165，而其可點連結只到 L 168–254。覆核收據給出兩處精確替換；只改 `claims.md` 來源欄即可，不需動 spoken text、畫面或 loop。R8→R9 JSON 只有六句 text 改動，其餘 133 景、11 loop 均相同；136/136 劇本、133/133 claims、126/126 shot、7/7 big 仍對齊，lint 0／0。作者修錨點並重凍結 claims SHA 後，需由另一位工作者差分重核方可解除來源 HOLD；新 R9 正式敘事、TTS 與 136/136 完整音檢仍待，付費媒體不放行。

R12 [作者凍結](../../docs/videos/curio-s49/review/r12-author-freeze.md)、[獨立來源／畫面](../../docs/videos/curio-s49/review/r12-source-independent.md)均 PASS；[兩名全新讀者正式合併](../../docs/videos/curio-s49/review/r12-official-panel.md)依系列規則 13/13 PASS。精確 `script.md` SHA `ab8e840e2c74b283b60e65e62d62e41d79d6eea0ded323e4888a3940de80ab7e`。完整 [政策回條](../../docs/videos/curio-s49/review/r12-policy.md) PASS（立場 0.88、業配 0.20）。網站 `review-pull` 大綱／劇本仍顯示 `waiting for the owner`；依站主常設推薦編輯委派，已為 R12 精確 brief/script SHA 記本機委派批准，兩筆註記明說網站卡沒有核准。

R12 [完整語音驗證](../../docs/videos/curio-s49/verify-13.md)：TTS 新合成 19 句／525 billable characters、重用 114 句；首輪全稿 133/133 音檢 3 旗標。兩輪定點補錄各 3 句／92 characters 後，再完整檢查兩次，旗標 **3→3→2**。最終 `moon019`「這次沒查到」與 `moon120`「引文」仍被聽錯；`moon122` 已清。最終 13:30.13 全旁白，正文 12:26.53，時長過線但**音訊 HOLD**；兩輪補錄上限已用完，不送 audio gate、不進插圖／配樂／成片。請作者只窄修 `moon019` 與 `moon120` 的易混詞並同步 claims，重做精確來源、敘事、政策、必要網站與音訊關卡；R12 既有 WAV 與音檢均不得移轉到新稿。
