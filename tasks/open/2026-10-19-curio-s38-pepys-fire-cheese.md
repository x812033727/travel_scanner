---
id: 2026-10-19-curio-s38-pepys-fire-cheese
title: Curio S38 Pepys fire and cheese historical episode
status: in-progress
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-22T12:34:43Z
created_at: 2026-10-19T22:34:43Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s38
---

# Curio S38 Pepys fire and cheese historical episode

## Why

為奇聞檔案局新增 S38〈倫敦大火時，佩皮斯為何把起司埋進土裡？〉。這個小動作有可重開的 1666 年日記原文，但網路轉述常加上起司大小、價值或被挖回的結局；本集按 9 月 2–6 日的行動順序講完整故事，並保留日記沒有回答的部分。

## Definition of done

- [ ] 一支經史料、敘事、旁白、插圖與輸出覆核的繁中歷史影片可提交站主發佈審核，並清楚區分佩皮斯親見、聽聞與日記留白。
- [ ] 正片至少 8 分鐘；本機影片與字幕的封裝／QA 證據可重開。

## Steps

- [x] 固定可重開的日記全文與版號，寫 [企劃](../../docs/videos/curio-s38/brief.md)、[研究](../../docs/videos/curio-s38/research.md)、[逐句主張](../../docs/videos/curio-s38/claims.md)。
- [x] 完成 R4 [影片稿](../../docs/videos/curio-s38/video.json) 與 [旁白稿](../../docs/videos/curio-s38/script.md)：112 句、111 個畫面、12 組懸念回收、估 9.995 分鐘，lint 0 error / 0 warning。劇本檔 SHA-256 `62af2f7d762b082a1e6910df28a721fac6c14cb4d081f06516f48b5511cd1411`；影片稿 SHA-256 `f497a97a9de671ba39dad98f92898671035dae6c1ccace5f8740b215a18da4e5`。
- [x] 首輪獨立 [盲讀與史料／畫面覆核](../../docs/videos/curio-s38/verify-1.md) 已留原始答案和 10/13 失敗證據；R2 已集中修正其敘事斷點、無依據的掃水方向與六處畫面問題。
- [x] R2 獨立敘事盲讀 13/13，但來源查核抓到 9 月 2 日午餐前後的事件倒置；這份 R2 劇本不得用於媒體製作。
- [x] R3 獨立敘事盲讀 13/13；史料／畫面查核發現搬走與清點混用、未記錄的寫作時刻、9 月 4 日花園討論的下午時序，以及塔樓、筆記、書面報告畫面問題。R4 已按固定日記集中修正；R3 不能作媒體製作依據。
- [x] 未參與撰稿的新讀者先只看 exact R4 劇本，獨立敘事 13/13、理解 13/13，再重開固定日記並核對 112/112 旁白及 111 提示詞；證據見 verify-4.md。正式 `narrative --answers` 已按讀者行號證據記錄通過。實際語音量測在 TTS 完成後另記。
- [ ] 劇本過門檻後按 `curio-episode` 的整集報價及審核程序製作語音、插圖、分鏡、音樂、字幕、正片，完成輸出與包裝 QA。

## How to verify

在 `/workspace/travel_scanner` 執行：

```bash
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json
sha256sum docs/videos/curio-s38/script.md docs/videos/curio-s38/video.json docs/videos/curio-s38/claims.md
npm run check:tasks
```

核對 `docs/videos/curio-s38/research.md` 中 GITenberg 固定 commit 的 1666 年 9 月 2–6 日原文，尤其 9 月 4 日兩個土坑、9 月 2 日塔樓官員轉述的起火地點、9 月 5 日局部止火和 9 月 6 日起司去向未記載。

## Notes

- 2026-10-22 R8t 作者停點：R8s PF014 [單張新原圖](../../docs/videos/curio-s38/verify-57-r8s-pf014-native-stop.md)因上下黑寬帶 REJECT，原生圖三次／兩輪局部修訂後不再購第四張。僅 PF014 改為「我為橋上的米切爾和莎拉擔心」的 1666-09-02 [佩皮斯日記譯文卡](../../docs/videos/curio-s38/verify-59-r8t-pf014-card-author.md)，不提前說其家已燒；[兩欄可逆差分](../../docs/videos/curio-s38/verify-59-r8t-pf014-card-structured-diff.json)，新 video SHA `35a23a36a8503988bdb70ff2dc2c6e3bd2f02c226891a5119f3b9756b86d2532`。Lint 0/0；正文插圖 106/111（95.5%），最長連卡 2。STOP 在位、ledger 未增（US$0.5830／38 image／37 judge／1 music，另有舊 PF003 US$0.0035 reservation），九張其他 KEEP 未改；PF014 已不再是 shot，舊 R8s 圖單不能作 R8t 合格證據。待獨立書面核對後再推 PF015–022；全片未完成。
- 2026-10-22 R8s 作者停點：R8r `pf009`／`pf013` 第三張原生圖均 [REJECT](../../docs/videos/curio-s38/verify-54-r8r-two-native-stop.md)，各景三次付費嘗試與兩輪提示詞修正已用完，不再開第四張。兩景改為 1666-09-02 [佩皮斯日記中文譯文引句卡](../../docs/videos/curio-s38/verify-55-r8s-fallback-author.md)；PF014 原圖只有煙、人物未望火，無法忠實重用作 PF013。因改卡後 PF011／PF012／PF014 連續三張 `drift`，只將 PF014 `camera` 改 `push in` 以解 lint；其 prompt／旁白未改，**但原 PF014 KEEP 圖的 request key 已失效，現為 HOLD，待獨立紙審後單景有界重畫**。R8s [五欄可逆差分](../../docs/videos/curio-s38/verify-55-r8s-fallback-structured-diff.json)，video SHA `f3f49ce1fdd64ac11189dbe8b64bb7bc486e4c03566795a500f9f8b636f3de34`，lint 0/0、正文 107/111 插圖（96.4%）、最長連卡 2；STOP 在位，ledger 未增（US$0.5695／37 image／36 judge／1 music，另有舊 US$0.0035 reservation），整集上限 US$4.58。PF001–005／PF008／PF010–012 九張已收圖未改；PF015–022 尚未畫。未完成第一章、全片分鏡或成片。
- 2026-10-22 R8r 書面覆核與原生圖：兩景 [獨立 PASS](../../docs/videos/curio-s38/verify-53-r8r-two-prompt-independent.md)後各試一次；[未裁切原圖驗收](../../docs/videos/curio-s38/verify-54-r8r-two-native-stop.md)均 REJECT。PF009 仍有黑寬帶／看不見回床動作；PF013 雖不再畫 1894 Tower Bridge，人物微笑正對觀眾且畫風割裂，不能表示塔上觀火。STOP 已恢復，ledger US$0.5695／37 image／36 judge／1 music，未試 PF015–022。
- 2026-10-22 R8r 作者停點：針對前批 PF009 的黑寬帶／偏寫實動畫與 PF013 的 1894 Tower Bridge，**僅窄修這兩個 prompt**；[可逆差分](../../docs/videos/curio-s38/verify-52-r8r-two-prompt-structured-diff.json)及[來源收據](../../docs/videos/curio-s38/verify-52-r8r-two-prompt-author.md)已落地。現行 video SHA `f02fdd2bd769e746b2e76206152492593f66cec1ea48e40a07cd7bf236aaf015`，lint 0/0、兩景 dry-run 通過；`claims.md`／`script.md` 及已收 PF010／PF011／PF012／PF014 prompt 不變。**待另一位獨立書面覆核，尚無 R8r 付費圖**。STOP 在位，ledger 仍 US$0.5425／35 image／34 judge／1 music，舊 `pf003` US$0.0035 reservation 仍在，整集 US$4.58 上限未變。
- 2026-10-22 R8q 獨立覆核／限額試畫：六景 prompt [獨立書面 PASS](../../docs/videos/curio-s38/verify-50-r8q-six-prompt-independent.md)，六景各一次[原圖逐張驗收](../../docs/videos/curio-s38/verify-51-r8q-six-native-stop.md)後 PF010／PF011／PF012／PF014 **KEEP**；PF009 因黑邊與畫風漂移、PF013 因把 1666 舊 London Bridge 畫成 1894 Tower Bridge **REJECT**，PF009 機器 FAIL 使整批 CLI 以內容關卡 exit 1，未推整集分鏡。R8q video SHA `087ae9c4…` 不變，已收 PF001–005／PF008 圖單項目及所選 SHA 不變；STOP 在位，私有 ledger US$0.5425／35 image／34 judge／1 music、舊 US$0.0035 reservation，仍低於 US$4.58 上限。先定點解 PF009 畫風／滿框、PF013 年代橋型，再依新差分另人核對；PF015–022 未畫。站台站主卡、成片與可點片尾仍待完成。
- 2026-10-22 R8q 最新接續：`pf008` R8p **seed 2** 已由[原圖驗收](../../docs/videos/curio-s38/verify-46-r8p-pf008-seed2-native-pass.md) KEEP，機器 10/10、人眼確認成年人物、睡袍、遠火與入選裁邊版畫風；舊 R8n／R8p seed 1 退件不變。第一章 `pf009`–`pf022` 的首輪批次在第六張 `pf014` 後提早 [STOP](../../docs/videos/curio-s38/verify-48-first-chapter-six-native-stop.md)：`pf009`–`pf014` 六張人眼全 REJECT（童貌、錯角色／紙本、近代建築／懸吊橋），`pf015`–`pf022` 未畫；不可拿前五張機器 PASS 充作可用分鏡。私有 STOP 在位；ledger US$0.4615／29 image／28 judge／1 music，舊 `pf003` US$0.0035 reservation 仍在，整集硬上限 US$4.58 未變。R8q 作者只窄修六個 prompt，[精確可逆差分](../../docs/videos/curio-s38/verify-49-r8q-six-prompt-structured-diff.json)及[來源收據](../../docs/videos/curio-s38/verify-49-r8q-six-prompt-author.md)已落地；現行 video SHA `087ae9c4cdbb8dea3430cd505d42624e06deca0a94b77e71c49164fbbcc2f4db`，lint 0/0、六景 dry-run 通過，**待另一位獨立紙審，未付費重試**。完整插圖、站台核准、正片／字幕／片尾可點連結仍未完成。
- 2026-10-22 R8p 畫面交接：`pf008` 成人／倫敦睡袍 prompt [獨立書面 PASS](../../docs/videos/curio-s38/verify-43-r8p-pf008-independent.md)，同一 SHA `8db80e07bffff8863f949e4a458b9fed0a891e36ed93063bce59c3915fc6e142` 的[唯一新原生圖](../../docs/videos/curio-s38/verify-44-r8p-pf008-native-stop.md)仍人工 **REJECT**：3D CGI、頂底黑邊與現代上衣，不是日記中的睡袍；機器 9/10、`passed=false`。STOP 已恢復，累計 US$0.3670（22 image／21 judge／1 music，另有舊 US$0.0035 預約），低於整集 US$4.58 上限。`pf001`–`pf005` 既有收圖不變；`pf009`／`pf010` 未開畫。另做局部提示詞及獨立紙面審查後才可單景再試；整集分鏡／成片／品牌片尾與 Studio 連結尚未完成。
固定日記：GITenberg `68fcf49f70ee793b989a6fd0464264d55beb4451`；`4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。本工單僅認領 `docs/videos/curio-s38/**`，不碰已有歸屬的 S01／S09／S18。R1 盲讀 10/13 未過；R2 敘事 13/13 卻有來源時序錯誤；R3 敘事 13/13 卻有來源／畫面問題；R4 由新讀者對同一 SHA 先盲讀 13/13，再核固定日記、112 行與 111 圖提示詞通過，詳 verify-4.md。2026-10-19 23:46 UTC：`brief.md` 補具 A／B 兩方案，Jev 選 A 0.94，主代理依站主「採推薦方案持續做完」授權本機核准；R4 精確劇本 SHA `62af2f7d762b082a1e6910df28a721fac6c14cb4d081f06516f48b5511cd1411` 送審後本機透明核准，沒有聲稱站主親讀。112 句 TTS 正在進行；付費插圖仍需語音核查及整集成本上限。另有 [題目可行性筆記](../../docs/videos/history-curiosity/source-feasible-expansion-20261019.md)：S27／S21 因同期互補資料在本雲端未能重開，暫停進入製作。

- 23:56 UTC：112 句 Gemini Sulafat 旁白完成，`timeline.json` 為 17,902 frame／30 fps，總 596.733 秒（9:56.73）。正文從 `pf006` 867 frame 到片尾 `pf112` 17,701 frame，**561.133 秒（9:21.13）**，超過 8 分鐘正文門檻；逐句 `check-audio` 正在跑，結果未出前不批准音訊與付費圖。MiniMax `keyframes --dry-run --takes 3` 對 111 圖報一輪 US$1.50、最多三輪 US$4.50；Gemini Lyria 600 秒配樂報 US$0.08，**整集插圖加配樂上限 US$4.58**，依站主廣泛推薦方案授權預先記帳。圖像仍須先過語音 gate 並排入共用每小時 240 次提交窗口。音檢持有專案鎖時試啟音樂被工具拒絕，未產生費用，待音檢結束再啟。
- 00:07 UTC：配樂已成功生成 600 秒，實支 US$0.08。第一輪音檢保存 74/112 轉寫後，第 75 個請求 `60ffa6a6e03f4a439758f04d4dc8cf51ed24b6dc06da44cfd51b793ccd68da7f` 於 00:04:02 收到無具體錯誤碼的 HTTP 502，speech journal 標 `held`。重跑原生 `check-audio` 只回傳同一 hold，沒有重送。此集非 pilot，網站的 `speech/status` 只報 TTS 月度字數，不報單次 Gemini 轉寫用量；故不能由該端點確認這一次是否計費。保留 journal、錯誤日誌與請求雜湊供核對。語音、圖片 gate 仍未核准。
- 00:09 UTC：站主已在本任務概括授權「以你推薦的就好不用問我，一直做完所有影片」。工具沒有單次轉寫計費查詢，且保留的檔案沒有完整答案。主代理據此選擇**僅對這一筆**清除 journal hold 並重送一次，接受其可能重複計費的風險；記錄原雜湊及該決策，不把重送說成免費。若再遇同類不明結果，另評估而不無限重試。
- 00:12 UTC：重送後完整 `check-audio` 112/112：85 字詞精確、8 同音／語助詞、5 經 Jev 接受、**14 旗標**。旗標 ID 為 `pf007,pf021,pf033,pf040,pf042,pf061,pf069,pf070,pf073,pf074,pf077,pf081,pf082,pf085`；已啟動只重錄這 14 句的 `tts --redo`。重錄及再檢通過之前仍不批准音訊與圖像。
- 00:17 UTC：14 句重錄後第二輪仍剩 4 旗標 `pf040,pf069,pf077,pf085`；按 [verify-5.md](../../docs/videos/curio-s38/verify-5.md) 集中改成 4 句更易聽清、史料邊界更明確的 R5 旁白，稿件 SHA `e7eca53fdb4d6fbae4c4454fc652bb33bd00ca1156f5e30e9fada26413a63cd5`、video SHA `cafb69b501d7f0d41d09d90c8650a2f7198ffb5388c57beacf15a5a88f2994ec`、claims SHA `2c0041720122040c94782054024e82f6dcf6da352e10986d1cdc71c93c594bb1`；lint 0/0。R4 盲讀／劇本核准因雜湊變更不適用於 R5；待新讀者重審與來源／畫面再核後，才能重送 R5 劇本 gate 及只合成更動句。
- 00:34 UTC：R5 新讀者盲讀 11/13，R6 再改夜間敘事後新讀者盲讀 13/13，但獨立來源查到 9 月 2 日 `pf047`–`pf050` 客人抵達／開始裝箱與月光花園／地窖搬箱的兩處先後倒置，故 R6 不得用於媒體。R7 依日記重排四句及四景，script SHA `8aeec7edaaa87f571e66894f0367fc101ec19ad70011bc0e526fef489a073a6d`、video SHA `bdbdb58148a510327bb290a80990a94d7cc4108ed7b6526a02b984e5c4f3ce32`、claims SHA `e4920984987d17ed3211f82062bca185f1c75b4f4e9a67569d46b569d992d2f4`，lint 0/0。新盲讀與全部 112 主張／111 景覆核仍需完成，見 [verify-6.md](../../docs/videos/curio-s38/verify-6.md)。此期間不重錄、不付費開畫。
- 00:37 UTC：R7 全新讀者先僅憑劇本封存 **13/13** 敘事盲評，再獨立重取固定佩皮斯日記查 112/112 主張和 111/111 靜圖提示詞，日期時序與全稿通過。正式 `narrative --answers` 依封存行號通過；兩次 `review-push` 後依站主概括授權本機核准 R7 大綱及 exact script，不稱站主親讀。`tts --dry-run` 報 112 句中只需重錄 11 句、255 個計費字元，已開始重錄；新增音訊、實測正文與零旗標音檢仍待完成，付費插圖未開始。證據見 [verify-6.md](../../docs/videos/curio-s38/verify-6.md)。
- 00:50 UTC：R7 11 句更新後 112/112 音檢只剩 `pf085`：第一次 Gemini 多聽「一」，一次重錄後把「泰晤士河」誤聽成「太湖市河」。本機 faster-whisper 取得模型遇 proxy 403，沒有第二轉寫。R8 僅將此句改成史料同義「這一次……乘船沿河往下游走」；script SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`，video `3dbe6dd23eedef3ff999801f6e548ab69ea480ee8a2b00095e78e1d48ec837b9`，claims `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。**另一位新讀者** R8 盲讀 13/13、固定日記 112/112 和靜圖提示 111/111 全通過；本機大綱／劇本重新按 exact hash 核准，僅重錄 `pf085` 24 字元，其餘 111 句快取重用。新 `timeline.json` 全片 596.2 秒，正文 `pf006`→`pf112` **560.6 秒／9 分 20.6 秒**；完整音檢 **112/112、0 旗標**，本機音訊 gate 已透明核准，未稱站主親聽。配樂已支 US$0.08、整集插圖加配樂硬上限 US$4.58；圖片尚未開畫，等共用時窗。細節見 [verify-8.md](../../docs/videos/curio-s38/verify-8.md)。
- 00:56 UTC：為省後續重畫風險，僅調整 `pf040`（橋上下游）、`pf076`（只畫寫信，不杜撰交給信差）、`pf098`（摩爾菲爾德擁擠背景）三張仍圖提示詞；script、claims、TTS、音檢均未改。新 video SHA `65ba99a5f6e28aef6dffbbe63828f080025a0c20e61120a75304d5aaf0635426`，lint 0/0。三景新提示尚待獨立定點覆核，不拿前版 111/111 回執冒認；見 [verify-9.md](../../docs/videos/curio-s38/verify-9.md)。
- 00:59 UTC：獨立定點覆核已通過，解析 JSON 僅上述三個提示詞葉節點改動；劇本／主張 SHA 不變，三景分別依固定日記 L65897–65901、L66004–66012、L66102–66109 核對，lint 0/0。[完整獨立稽核](../../docs/videos/curio-s38/verify-9-audit.md) SHA `9b78bc510f974616d2b987b192322da9e699a54bac48f296d83e751e441d5e25`。靜態圖稿可進開畫，但仍須遵守整集 US$4.58 上限、共用時窗並逐張驗收生成圖。
- 01:03–01:17 UTC：R8a 試畫 `pf001`、`pf002` 的機器 9.29／10 分均判通過，人眼卻發現東亞服飾孩童／現代衣裝及帶孔瑞士起司等與 1666 倫敦、帕馬森起司衝突，已停止後續完整開圖；兩張錯圖隔離保存。ledger 已付音樂 US$0.08 與兩張圖含判官 US$0.027，另有中斷時 `pf003` US$0.0035 未核銷保留額，仍計入整集 US$4.58 硬上限。R8b2 只改 111 張提示詞：時代人物／材質、起司外觀與依鏡頭條件出現的建材；也排除埋起司後桌上又出現起司、口頭消息配紙條、女僕無據說成「年輕」、睡袍畫成現代女式睡裙的風險。最終 video SHA `ca2bb866b0fb452607f20764f652c715f1447bc226f9df0a28bfc3b1d73cb1fc`，script、claims 不變，lint 0/0。**待獨立覆核新 JSON，再小量試畫並目視通過，才可續畫**；見 [verify-10.md](../../docs/videos/curio-s38/verify-10.md)。

- 01:41 UTC：R8b2 111/111 提示詞獨立覆核已 PASS，但兩景開圖仍出現孩童／帶孔起司而退回。主代理先改四景、再依 R8c 試畫改兩張重複起司 prompt；R8d video SHA `b7aec196479b5e08656b26afc14a56035bfece3998cd90cad9707bf919ccf5ff`，劇本／主張不變，定點史料覆核 PASS，lint 0/0。`pf001` 兩位成人與土坑合格；`pf002` 最終第二次試畫改為完整硬起司外皮、土坑與酒器，機器 9.29、人眼主代理通過。獨立讀者已另看過 `pf001` 與 `pf002` **第一張**有正確歷史物件；第二張入選圖仍需全景最終 QA 同批再看。ledger US$0.1915 含先前 `pf003` 未核銷保留額，硬上限仍 US$4.58。其餘 109 張待共用 MiniMax 額度和逐張人眼審驗；詳 [verify-12.md](../../docs/videos/curio-s38/verify-12.md)。

2026-10-20 03:17 UTC：111 張 still 的獨立史料／年代預檢無阻擋；作者只修 `pf076/080/104` 三個 prompt，以全白信紙、主動拆屋防火、進行中的滅火動作降低生成風險。第二位讀者對現行 video SHA `33eceef58a3d25414f28606b1737258b256ff8a4bd9687f739974e42c0bb12bc` 定點覆核 PASS，lint 0／0。先前兩張試畫可用，餘圖尚未購買；詳 [verify-13.md](../../docs/videos/curio-s38/verify-13.md)。

2026-10-22 R8v 第三次也是最後一次定點試圖：[獨立紙審](../../docs/videos/curio-s38/verify-69-r8v-final-three-prompt-independent.md) PASS；[原圖停線](../../docs/videos/curio-s38/verify-70-r8v-final-three-native-stop.md)判 PF016／PF017 **KEEP**，PF015 因額外第三隻手 **REJECT FINAL**，不可第四次重畫。R8w [作者同章重用候選](../../docs/videos/curio-s38/verify-71-r8w-pf015-reuse-author.md)把 PF015 改為有「剛才」回望語義的 PF010 同章已收窗景，劇本／音訊不變，lint 0／0、106／111 景仍是插圖，最多連續兩卡；[獨立紙審](../../docs/videos/curio-s38/verify-72-r8w-pf015-reuse-independent-paper.md) PASS。PF010 原圖的快取 image key 與新 PF015 精確相同，但 PF015 的 judge 情境含另一場景 ID，不能無費複製舊裁決；一次有防新 image POST 的快取重用＋單次 PF015 judge 在[站台無法連線](../../docs/videos/curio-s38/verify-73-r8w-pf015-cache-judge-upstream-hold.md)時停於 status 階段，零新圖／零費，STOP 在位。PF015 仍是舊退件圖單狀態，等服務恢復後只可重用既有圖並正式評審；PF019 已紙審但未畫。帳本維持 US$0.7045（另有舊 US$0.0035 預約），低於 US$4.58；完整分鏡及成片仍待。

R8w 站台恢復後在 image POST 阻斷下補跑一次 PF015 情境 [正式 judge](../../docs/videos/curio-s38/verify-74-r8w-pf015-cache-judge-fail.md)：快取圖重用、**0 新圖、1 judge US$0.0100**；判 **9.71／10 FAIL**，人物朝屋內而非看窗外火光，PF015 仍 `needs_review`。STOP 恢復、jobs 空、ledger US$0.7145／47 image／47 judge／1 music，另有舊 US$0.0035 reservation。R8x [作者替代方案](../../docs/videos/curio-s38/verify-75-r8x-pf015-source-card-author.md)將 PF015 換成 1666-09-02 日記「心裡滿是憂慮」引句卡，並僅將 PF012 運鏡改 `push in` 避免三張 `drift` shot 連續；旁白不變，105／111 插圖、最多連續三卡、lint 0／0，video SHA `23f0662b96ba290494b044f2cdce037ba011b5222a1137d5a38b0a5e25600615`。**待獨立紙審**，PF012 原收圖因 camera 改變須重畫一張且原圖驗收，PF019 未畫；不可當全片完成。

R8x [獨立紙審](../../docs/videos/curio-s38/verify-76-r8x-pf015-source-card-independent.md) PASS 後，PF012 seed 1 [正式 judge FAIL](../../docs/videos/curio-s38/verify-77-r8x-pf012-seed1-independent.md)；受控 seed 2 雖機器 9.29／10 PASS，獨立[原圖／裁圖目視](../../docs/videos/curio-s38/verify-78-r8x-pf012-seed2-human-reject.md)因塑膠瓶與現代衣著 **HUMAN REJECT**。R8y [作者單一提示詞窄修](../../docs/videos/curio-s38/verify-79-r8y-pf012-final-prompt-author.md)只改 PF012 上半身構圖、披衣動作與古裝／空背景限制；劇本及其他鏡不變，lint 0／0，video SHA `586c55b4328c96ab405156467ca2deb7cf294119e4043aaea579c27704404652`。**待非作者紙審；尚未畫第三張。** 私人 STOP 在位、jobs 空，ledger US$0.7415／49 image／49 judge／1 music，另有舊 US$0.0035 reservation。既有 10 張 KEEP 要在新圖單安全重綁後保留；最多僅 PF012 最後一張實際原圖及一次 judge，不能因換 prompt 開新三張。PF019 以後及完整分鏡未收。

R8y [獨立提示詞紙審](../../docs/videos/curio-s38/verify-80-r8y-pf012-final-prompt-independent.md) PASS，安全[離線圖單重綁](../../docs/videos/curio-s38/verify-81-r8y-pf012-offline-manifest-rebind.md)保留十張 KEEP、移除先前退件。最後一張 PF012 原圖經[獨立人工目視](../../docs/videos/curio-s38/verify-82-r8y-pf012-final-image-independent.md) **KEEP**：披斗篷動作可辨、未再出現塑膠瓶或現代領帶；邊角仍有小瓶形與皮帶扣，已明記但不構成可辨的年代錯物。正式 judge 9.29／10 PASS；PF012 累計三張原圖，**不再補畫**。新 manifest SHA `bff9bf2fea355340e20d1815a69c4cbd116c8fa53c6b5cde262023929a7be2d1` 有 11 張 KEEP；ledger US$0.7550／50 image／50 judge／1 music，另有舊 US$0.0035 reservation；STOP 在位、jobs 空。PF019 及後續近百張仍須按史料、付費上限及原圖人工驗收逐批製作；不得聲稱整片 storyboard 完成。

R8y PF019 首張原圖經[獨立目視](../../docs/videos/curio-s38/verify-83-r8y-pf019-seed1-human-reject.md) **REJECT**：房屋似漂浮於第二艘船上，不能承接日記的岸上燒屋；已從 active 圖單隔離，11 張 KEEP 不變。R8z 作者依 1666-09-02 固定日記改為[米切爾家已燒引句卡](../../docs/videos/curio-s38/verify-84-r8z-pf019-source-card-author.md)，[兩葉可逆差分](../../docs/videos/curio-s38/verify-84-r8z-pf019-source-card-structured-diff.json)只動 PF019 畫面模板與文案，旁白／主張不變；video SHA `4f30f598c40dcdb9a6cc3d9edd0fa2bb2117d7f455609c4dd4f2730c9f119022`，lint 0／0、104／111 景為插圖。**待非作者書面覆核，尚未重綁圖單或再開畫。** STOP 在位、jobs 空，ledger US$0.7685／51 image／51 judge／1 music，另有舊 US$0.0035 reservation；整集硬上限 US$4.58。

R8z PF019 引句卡[非作者紙審](../../docs/videos/curio-s38/verify-85-r8z-pf019-source-card-independent.md) PASS；[安全離線圖單重綁](../../docs/videos/curio-s38/verify-86-r8z-pf019-card-rebind.md)保全 11 張 KEEP、移除退件 PF019。只試 PF018 一張原生圖，機器 9.29／10 PASS，但[原圖人工 REJECT](../../docs/videos/curio-s38/verify-87-r8z-pf018-seed1-human-reject.md)：前景疑似兩名孩童，背景無人把箱子裝上平底貨船，和旁白核心動作不合；本輪未購 PF020–022。退件 PF018 已從 active 圖單隔離，11 張 KEEP 及其選圖檔 SHA 不變；STOP 在位、jobs 空，ledger **US$0.7820／52 image／52 judge／1 music**，另有舊 US$0.0035 reservation。PF018 需定點提示詞修訂及非作者紙審後才可重試，完整插圖與成片仍未完成。

R8aa 作者針對 PF018 只改[單一圖片 prompt](../../docs/videos/curio-s38/verify-88-r8aa-pf018-prompt-author.md)：明顯成年住戶把一個木箱舉過平底貨船低船舷，不再叫模型同畫佩皮斯觀察與一家人裝箱。[可逆單葉差分](../../docs/videos/curio-s38/verify-88-r8aa-pf018-prompt-structured-diff.json)綁 video SHA `e25b7163f2efa7f830c0b94e421511ceaa4662fb985b53d2290e3a715a16556b`；旁白與主張未改，lint 0／0、104／111 插圖景。**待非作者依固定日記書面覆核；舊圖單仍綁 R8z，不可直接付費重畫。**

R8aa [非作者紙審](../../docs/videos/curio-s38/verify-89-r8aa-pf018-independent-paper.md) PASS，[安全離線重綁](../../docs/videos/curio-s38/verify-90-r8aa-pf018-offline-rebind.md)保全 11 張 KEEP 後，PF018 第二張實際原圖[正式 judge FAIL、人工 REJECT](../../docs/videos/curio-s38/verify-91-r8aa-pf018-seed1-fail-stop.md)：游離線段、黑寬帶、箱子沒有可辨跨船舷動作與近代感建築；未購 PF020–022。退件已隔離，11 KEEP 完整條目不變；STOP 在位、jobs 空，ledger **US$0.7955／53 image／53 judge／1 music**，另有舊 US$0.0035 reservation。R8ab 作者只做[PF018 最後一次窄修](../../docs/videos/curio-s38/verify-92-r8ab-pf018-final-prompt-author.md)及[單葉可逆差分](../../docs/videos/curio-s38/verify-92-r8ab-pf018-final-prompt-structured-diff.json)：近取灰髮成人將箱子放進船，背景只留河水與陰天；video SHA `b955dae2c2620b7477fcdef24606d9c1696f390c927f9fc7be10aa058d0b2ae9`、lint 0／0、旁白主張未改。**待非作者書面紙審；未重綁或購第三張。**第三張若退即改已有圖或史料卡，不購第四張。

R8ab [最後提示詞獨立紙審](../../docs/videos/curio-s38/verify-93-r8ab-pf018-final-independent-paper.md) PASS、[安全離線重綁](../../docs/videos/curio-s38/verify-94-r8ab-pf018-final-rebind.md)保全 11 張 KEEP。PF018 第三張且最後一張原圖機器 9.29／10 PASS；第一位[原圖審查者](../../docs/videos/curio-s38/verify-95-r8ab-pf018-final-native-independent.md)因箱子底部已在船上、未見跨舷定格判 REJECT；未先看該票的第二位[盲審者](../../docs/videos/curio-s38/verify-96-r8ab-pf018-tiebreak-blind.md)判 KEEP，認為兩名成人在平底貨船上搬家當與旁白／史料相合。主代理依系列「評審過關、只退來源矛盾或畫風漂移」的標準[公開裁決 KEEP](../../docs/videos/curio-s38/verify-97-r8ab-pf018-final-adjudication.md)，保存異議供分鏡複檢，不宣稱精確現場重建。現行 manifest 有 **12 selected KEEP**、其餘 11 筆及實際檔 SHA 不變；PF018 累計三張、**不再重畫**。ledger **US$0.8090／54 image／54 judge／1 music**，另有舊 US$0.0035 reservation；STOP 在位、jobs 空。PF020–022 和其餘約 92 景仍待逐張原圖驗收，完整影片未完成。

R8ac PF020 首張原圖機器 7.18／10 PASS，但[1280×720 原圖人工 REJECT](../../docs/videos/curio-s38/verify-98-r8ac-pf020-seed1-human-reject.md)：主角抓硬箱、黑桿插入水面，沒有可見的拋家當動作，另一人衣著明顯近代。已留私人退件圖與產出後圖單；active manifest 只移除 PF020，**12 selected KEEP 的完整條目及實檔 SHA 不變**，STOP 在位、jobs 空。PF021／PF022 **未購圖**。帳本 US$0.8225／55 image／55 judge／1 music，另有舊 US$0.0035 reservation，低於 US$4.58 硬上限。作者只做[PF020 單一 prompt 窄修](../../docs/videos/curio-s38/verify-99-r8ac-pf020-prompt-author.md)及[可逆差分](../../docs/videos/curio-s38/verify-99-r8ac-pf020-prompt-structured-diff.json)：新 video SHA `d8d169a010a7ffce93b3aec580e7c9580dc3a5393ffbe0bbc5909b72e8559688`，lint 0／0，旁白／主張不變；改後 dry-run 因站台連線失敗而未取得。**待非作者紙審、重綁舊 KEEP 和服務預檢；不能直接付費重試**。全片插圖、分鏡、成片仍未完成。

R8ac PF020 窄修已獲[非作者固定日記紙審](../../docs/videos/curio-s38/verify-100-r8ac-pf020-prompt-independent.md) **PASS**；[安全離線重綁](../../docs/videos/curio-s38/verify-101-r8ac-pf020-offline-rebind.md)只把私人 manifest `visual_hash` 改成 `799a46f1c5720fec`，12 張 KEEP 完整條目和所選實檔 SHA 全不變，STOP／空 jobs／帳本不變。新 active manifest SHA `66b30497f3b1f7af4757716ce9d81a59f972fb3bcf5b14c8ee7086981fcc2877`。重綁後 `media-status` 及單景 dry-run 均因 `mokaair.com` 連線失敗而 exit 4；**尚未再付費購 PF020 第二張，PF021／PF022 也未購圖**。等 live status 和 dry-run 恢復並核限額後，再只試 PF020 一張、人工看原圖；任何失敗即停。整片仍未完成。

R8ac 雲端 Node fetch 加上既有環境代理後，live status 恢復、PF020 dry-run 322／1072 字且 `image-01` ready；完整精確前置斷言後只購 PF020 **seed 2 一張＋一次 judge**。[未裁切原圖與正式裁圖](../../docs/videos/curio-s38/verify-102-r8ac-pf020-seed2-keep.md)雙方人眼 **KEEP**：成年住戶已放開布包，布包懸於河面上，沒有首圖的黑桿或現代旁觀者；judge 7.88／10 PASS，但袖口粉色形狀粗糙，留下供分鏡複檢。active manifest **13 selected KEEP**，舊 12 筆 canonical SHA 與所選檔 SHA 均不變；ledger **US$0.8360／56 image／56 judge／1 music**，另有舊 US$0.0035 reservation，STOP 在位、jobs 空。PF021／PF022 尚未購圖，只能按既有書面 PASS 各受控單景試一張、檢查原圖；完整影片未完成。

R8ad PF021 首張原圖[機器 subject=0 FAIL、人工 REJECT](../../docs/videos/curio-s38/verify-103-r8ad-pf021-seed1-machine-human-reject.md)：兩名童貌人物跑離左後方的船，右屋為東亞式翹瓦簷；與 1666 倫敦居民向船跑的旁白相反。已停線並封存退件圖／產出後圖單，active manifest 隔離 PF021、**原 13 張 selected KEEP 完整條目和實檔 SHA 不變**；PF022 未購圖。ledger **US$0.8495／57 image／57 judge／1 music**，另有舊 US$0.0035 reservation；STOP 在位、jobs 空。作者只做[PF021 單景窄修](../../docs/videos/curio-s38/verify-104-r8ad-pf021-prompt-author.md)及[單葉可逆差分](../../docs/videos/curio-s38/verify-104-r8ad-pf021-prompt-structured-diff.json)：明確左側冒煙磚屋→右側木船、成年居民前腳踏上登船板；新 `video.json` SHA `c531301285fd9cbc3730f40c9c4a1d37936f00f2c7a0bfb98bf0c1ba97a7e121`、lint 0／0，旁白／主張不變。**待非作者固定日記紙審、13 KEEP 安全重綁和重新前置檢查；尚未購第二張**。PF022 和全片製作仍未完成。

2026-10-22 續作：PF021第二實圖跑離船而退件，單景改為登船動作，獨立紙審PASS後第三／最後實圖judge9.29與原圖KEEP。現14 KEEP、STOP在位、jobs空；見verify-106至109。最新video a150042d8a53b5d63a86821759a81aef934240008ad4dd82c55bb83b99060844；帳本實付US$0.8765。PF022未畫，整片未完成。

2026-10-22 剩餘整集沿用性覆核：verify-110確認PF022–111共90景與已審後續版本完整場景相同，旁白／claims不變，14 KEEP有效且0其他keyframe問題。已核live image-01與餘額、整集dry-run；90景每景最多3次、含舊預約整集最壞US$4.525＜US$4.58。採系列整集產圖流程；保留14KEEP，不為7來源卡或outro買圖，批次產出後逐張驗原圖，並非全片已完成。
