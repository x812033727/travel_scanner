---
id: 2026-10-19-curio-s26-marie-antoinette-brioche-attribution
title: Curio S26 Marie Antoinette brioche attribution episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s26
claimed_at: 2026-10-19T19:10:41Z
created_at: 2026-10-19T19:10:38Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s26
---

# Curio S26 Marie Antoinette brioche attribution episode

## Why

站主要求在 S34 之後依推薦持續製作 S 軸歷史影片。S26 的常見問句「沒有麵包就吃蛋糕，瑪麗皇后真的說過嗎？」需要把盧梭《懺悔錄》的匿名「公主」、法文 *brioche*、瑪麗・安東尼的生平，以及十九世紀已帶懷疑語氣的歸屬文字分開核對；題庫的寫作年份不能逕當成已證事實。

## Definition of done

- [x] `docs/videos/curio-s26` 有估 8.7 分鐘劇本、固定來源筆記、逐句事實表、83 張靜圖分鏡。
- [x] 獨立史料覆核與確切雜湊盲讀：語音措辭改寫稿第八輪 12/13，刪真重複後第九輪 13/13，固定四來源及 82 句覆核通過；媒體品管與成片待完成。

## Steps

- [x] 檢查 S26 無其他活躍認領、遠端 PR 或 main 既有落地，建立窄 scope。
- [x] 固定盧梭法文摘錄與完整英譯、Campan 生年／赴法記錄、Karr 1841 與 1843 年文字；標示一手敘述和後來轉述的界線。
- [x] 完成 brief、research、claims、video.json、script.md；獨立史料讀者已完成初次與增量覆核。
- [x] 首次全新盲讀完成 11/13；針對長段落失去懸念、糕點店岔線修稿，見 `verify-3.md`。
- [x] 第二次全新盲讀 10/13；連同獨立增量史料覆核指出的過度推論與畫面暗示，一次作結構修訂，見 `verify-4.md`。
- [x] 第三次全新盲讀 9/13；再修重複、章首與流程式句子，見 `verify-5.md`。
- [x] 第四次全新盲讀 12/13，固定原件及新增句史料覆核通過；刪去兩處真重複並收窄哺乳詞義，見 `verify-6.md`。
- [x] 第五次全新盲讀 12/13，刪相鄰的國王承諾重述；婦人不能哺乳明確歸於自述，見 `verify-7.md`。
- [x] 第六次全新盲讀 12/13，刪卡爾布里歐修引語的重述；修兩處馬車旁人群畫面，見 `verify-8.md`。
- [x] 本次精確雜湊由第七位新讀者判 13/13，固定來源再核通過；見 `verify-9.md`。
- [x] 第八輪對語音措辭修復稿判 12/13，固定來源差分通過；刪去一組重複問答並修緊鉤子，見 `verify-11.md`。
- [x] 第九輪對修訂稿判 13/13，固定來源與 81 張提示覆核通過；劇本關卡提交時只規整尾部序號與校驗字串，見 `verify-12.md`。
- [x] 現行 82 句語音已合成並逐句通過，`check-audio` 82/82、0 標記；正文實測 8:18.57，劇本與音訊 gate 已依持續委託透明記錄，見 `verify-13.md`。
- [x] 511 秒配樂已生成，媒體帳簿 US$0.08。
- [x] 首輪 81/81 張、第二輪 33/33 張、六張史實補圖及後續定點種子已完成，見 `verify-16.md` 至 `verify-19.md`。
- [ ] 清除最後 10 景材料／機評阻擋，完成站主分鏡審核、成片與上架包。
- [ ] 跑文件測試、記錄最後交接。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s26`；`node tools/video/cli.mjs narrative --slug curio-s26`；`npm run test:docs-videos`；`npm run check:tasks`。

## Notes

與其他集共用 `codex/curio-s34-endurance-20261019`，本票只改 `docs/videos/curio-s26`。早期原件可讀 GitHub 固定提交：TEI 對《懺悔錄》法文摘錄、GITenberg 完整英譯、Campan 回憶錄、Karr《Les Guêpes》。Karr 1841 年稱名言「真假未定」，1843 年又提其找到一部 1760 年書將話歸給托斯卡納公爵夫人；後者只可稱「Karr 自述」，尚未獨立找到該書。盧梭原文未指名瑪麗；不能把題庫的約 1765 年寫作日期或匿名公主身分寫成已證。

第七輪受審稿 narrative hash `15270e565c5bca98`、`script.md` SHA-256 `acadd5d68adc18b4063cc54957436dfa2880b2ce1b4684675feccf3d9a50fab3`，84 句、83 張靜圖、估 8.6 分鐘；lint 0 錯 0 警告。早稿獨立史料覆核見 `verify-1.md`、`verify-2.md`；前六次全新盲讀在逐步修稿中得 11/13、10/13、9/13、12/13、12/13、12/13，原始阻擋及源流分見 `verify-3.md` 至 `verify-8.md`。第七次確切雜湊 13/13，固定來源相符，見 `verify-9.md`。outline／script 關卡均依站主的持續製作委託記錄代理核准，明示站主未逐篇審讀；**舊稿語音實測已達 8 分鐘但品質未過，插圖支出仍為 US$0.00**。

上段是第七次盲讀時的舊稿紀錄。第八輪語音措辭修復稿 SHA-256 `1847738eb6cb8410b3034e4147bde198dca73355062b3679755946c40926e3ea` 判 12/13，13 句來源差分全通過，唯一阻擋為重複匿名公主稱呼；見 `verify-10.md`、`verify-11.md`。第九輪原審稿 SHA-256 `389f04150f976ff2e46ca1dbc6b4a53e5e511a9ce95c06c11e44338f5297a5ab` 判 13/13；script gate 將尾部生成性元資料規整後，現行 `script.md` SHA-256 `261d15365e96538bf7fb498170463e1b81836a657e7bd0b5636df37f5a19a20e`，82 句、81 靜圖，口播文字未變，lint 0/0，詳見 `verify-12.md`。舊稿語音正文實測 504.03 秒；現行稿仍待重錄與語音審核，插圖支出 US$0.00。

其後 `ma022` 兩次合成仍因「改／該」同音被標記，改用無歧義句子並由新讀者對 SHA-256 `730769bbadd807eeeb511f1ccac967cac0a53f93a24982b770ed4228b763bdcb` 判 13/13，來源差分通過。最終 82/82 音訊檢查 0 標記，正文 498.57 秒；詳見 `verify-13.md`。插圖生成仍等共享額度。

2026-10-20 03:12 UTC：81 景中 20 景提示詞修訂完成，去除 1841 年錯時道具與虛構手稿欄位，釐清食物、年齡及 1840 年代銀行畫面；獨立全景及定點覆核 PASS。現行 `video.json` SHA `08df3fb33789cc96a900639af76efa64d13751ecfd49a835d8505335e68578c6`，lint 0／0，僅 prompt 變動，開圖仍待共享時窗與逐張驗收。見 [開畫前覆核](../../docs/videos/curio-art-preflight-2026-10-20.md)。

2026-10-20 03:22 UTC：`keyframes --dry-run` 報 81 張、每張最多三次插圖加評審約 US$3.28；已產生配樂 US$0.08，**整集總上限約 US$3.36**（以精確每次 US$0.0135 計為 US$3.3605，帳簿硬停上限 US$3.37）。先前交接提及的 US$3.32 是 S06 的 80 張報價，不能套用 S26。首輪只設兩次嘗試，修復仍以整集上限計；在根代理調度共用每小時額度前不送付費請求。

2026-10-20 04:13 UTC：第二次全 81 景來源／視覺風險檢視完成；76 景只修 `data.prompt`，最終 `video.json` SHA `a9ec285dd9932d1b7feefc514d2ff7af86bff97a9498b40c9022ae984be6a186`。獨立工作者對確切雜湊重新覆核 PASS；匿名公主、瑪麗三個年齡、1789 馬車人群、卡爾 1843 年自稱所見但未找回的 1760 書分層清楚。`script.md`／`claims.md` 未變；lint 0 errors、4 個有意保留的連續性／無字來源用詞 warnings，`--takes 2 --dry-run` 顯示 81 張約 US$2.19 圖像費。帳簿仍只有配樂 US$0.08，沒有付費圖像。詳見 [開圖前全景覆核](../../docs/videos/curio-s26/verify-14.md)；等待根代理安排共用 MiniMax 時段，再逐張全尺寸驗收。

2026-10-20：最後七個史料道具提示詞移去 Campan／Karr 作者姓名，保留後出回憶錄與 1841／1843 雜誌的物件／年代；`video.json` 新 SHA `62cd30fb3bc2cfa261e97fa43783ab4c12abf501dcb66fbecb573535c973d116`。獨立審查者對新精確雜湊七景與 81 組合提示詞 **PASS**；82 句旁白與音訊不變、lint 0／4。三輪插圖上界約 US$3.28，加已支配樂 US$0.08，小於 US$3.37 硬上限。先只開 81 景首輪 `--takes 1`，之後逐張原尺寸與帳簿核對再定點補畫；共用近 60 分鐘圖像時窗尚須 S05／S40 結束並留足 81 張。詳 [verify-15.md](../../docs/videos/curio-s26/verify-15.md)。

2026-10-20 07:48 UTC：共享時窗釋出後，S26 首輪 **81/81** 插圖完成，帳簿 US$1.1735（含音樂）、保留額 0；首輪 manifest SHA `dd5897913ec74bd92d74a1c799a97483941ff2cd5dd4ea63f4c9e19ea4acca56`。前後兩位原尺寸讀圖者把清楚史實／年代矛盾與可留的卡通簡化分開，合併 40 張待處理。七張改成有出處的名字／年代／短引文卡，其餘 33 張做正向史料／年代提示詞修補；獨立精確差分審查 PASS，新 `video.json` SHA `8fb5922dbae506b3fd713fbd216915d6f6004a2abbc2f2fcb0b7f37bbfe89a79`，82 句旁白不動、插圖 74/81、連卡最多一張、lint 0／5。下一步只送 33 張各一次，逐張再次原尺寸核對，維持 US$3.37 整集上限。詳 [verify-16.md](../../docs/videos/curio-s26/verify-16.md)。後台分鏡仍未送審；卡片令 narrative hash 變更，須用真正的新盲讀收據，不能沿用舊版。

2026-10-20 08:18 UTC：第二輪 33 張定點圖已完成；`ma084` 的暫時 HTTP 502 由原 job id 冪等恢復，圖片未重買。選圖 manifest SHA `ee39c2d7e1c7b095080bc78362ce163737c150c780a7b0a5dfb2c245b17b7844`，帳簿 US$1.619、保留額 0。兩位讀圖者逐張原尺寸覆看後合併六張史實／年代硬傷與 14 張機評未過，交集二張，待處理 **18 張**。只先把六景正向修圖 prompt 納入 `video.json`，新 SHA `9752652025b4027aa05953e0862d13480545a78e76b4642788746833be14e6b3`；獨立 exact SHA 來源與差分審查 PASS、lint 0／5、口播／字卡不變。全新劇本盲讀 13/13 已由正式 CLI 記錄 PASS。第三輪先送六張各一次，讀圖後再決定機評第二 seed；詳 [verify-17.md](../../docs/videos/curio-s26/verify-17.md)。

2026-10-20 08:30 UTC：第三輪六張各一次完成，帳簿 US$1.700、保留額 0；原尺寸四張史料與機評可留，`ma013` 僅機評未過，`ma009` 的空盤旁酒瓶出現假字標籤。只對 `ma009` 改為素面酒杯加空盤，新 `video.json` SHA `32a23d36fedf55ba41f0cb99c801584d79e8dfbab6235e48b7bd2c124fcade47`，獨立史料審查 PASS、lint 0／5；下一步限一張 `ma009` 補圖，再驗 13 張純機評待修，維持分鏡站主 gate 真實狀態。詳 [verify-18.md](../../docs/videos/curio-s26/verify-18.md)。

2026-10-20 08:49 UTC：`ma009` 素杯空盤一次及其後 14 景第二 seed 已完成、無重買 seed1；原尺寸 74/74 選圖雜湊核對。帳簿 US$1.9025／US$3.37、保留額 0。官方剩七景未過，另有 `ma009` 麵包、`ma102` 後世四馬凱旋門、`ma101` 1841 電檯燈三張「機評過但史實硬錯」，合併十景。十欄 prompt-only 修補已獨立來源／年代 PASS，現行 `video.json` SHA `e6e2d8fc45ec03131b5c5260027daf6b456110eaf2928311fc3e2f574374d34a`；lint 0／5，十景一次 dry-run 約 US$0.135，仍需付費補圖及全尺寸覆看。S26 `format: drama` 不容 `--accept-best`，不可用人工 WATCH 竄改正式機評。分鏡後台仍未送審，站主核准不可假造。詳 [verify-19.md](../../docs/videos/curio-s26/verify-19.md)。
