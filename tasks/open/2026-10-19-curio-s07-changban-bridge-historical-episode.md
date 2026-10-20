---
id: 2026-10-19-curio-s07-changban-bridge-historical-episode
title: Curio S07 Changban bridge historical episode
status: in-progress
priority: P2
area: docs
owner: codex-s07
claimed_at: 2026-10-19T18:26:17Z
created_at: 2026-10-19T18:26:13Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s07
---

# Curio S07 Changban bridge historical episode

## Why

題庫把《演義》說成「喝斷橋」，但《三國志·張飛傳》原已有「據水斷橋」；小說也只寫張飛退敵後命人拆橋。需要一集讓觀眾看懂劉備敗走、張飛二十騎拒後的正史核心，以及後來小說增加的疑兵、三喝和拆橋後果。

## Definition of done

- [x] 8 分鐘以上可審閱企劃、固定史料、逐句主張、`video.json`、`script.md`。
- [x] `lint` 為 0 errors、0 warnings，故事長度至少 8 分鐘。
- [x] 完成獨立盲讀與來源覆核，再交由系列負責者決定付費媒體步驟。

## Steps

- [x] 核對固定《三國志》卷 32／36、《三國演義》第 41／42 回及建安十三年紀年。
- [x] 寫六章 99 句、90 張插圖的可愛漫劇旁白和分鏡。
- [x] 為每句建立史料或小說層級對照，避免把五千騎畫成橋頭實數。
- [x] 由未讀企劃與史料的讀者盲讀旁白，修正故事節奏並記錄回執。

## How to verify

在 `/workspace/travel_scanner` 執行：

```sh
node tools/video/cli.mjs lint --slug curio-s07
node tools/video/cli.mjs script --slug curio-s07
node tools/video/cli.mjs narrative --slug curio-s07
```

2026-10-19 已執行首兩項：0 errors、0 warnings，估算 9.5 分鐘／120 句／1932 spoken units；劇本雜湊 `1827d1f677db0f72`。

2026-10-19：上述初版獨立盲讀僅 8／13，舊稿有返回橋頭重講、宣告「換一本書」、章首脫節、未回收敵人不敢近的原因，以及結尾重述事實等阻斷。已重構史書橋後劉備逃向漢津與小說橋後拆橋再追的後果鏈，避開總結重述。另依來源覆核刪去小說不支持的曹操「先看清楚」、曹軍「面面相看」字句；史書斷橋不指定施工者和橋材、小說在退敵後才拆橋。修訂詳 [`verify-1.md`](../../docs/videos/curio-s07/verify-1.md)。目前 **99 句／90 插圖／六章、估 8.4 分鐘、lint 0 errors / 0 warnings、script SHA-256 `8b459182e0726732487df2ccddead4cbd15bb404a74b3943500ff193f49da216`**；逐句表 99 句同步。仍待新雜湊的真正獨立盲讀與來源查核，沒有啟動付費媒體。

2026-10-19：上列版的新來源隔離盲讀 **12/13**，`one_line` 再次否決史書與小說重走同一趟橋頭；兩名讀者同題均否，故改成一次前進的時間線，把史書挑戰原句放在小說三喝的同一動作處。讀者的七組固定史料抽查通過，另提示舊 `eb094` 未明確區分原文先後與真實拆橋時點；現稿已釐清，並補第 42 回關羽截兵的固定行號。**現版 96 句／88 插圖／六章、估 8.2 分鐘、lint 0 errors / 0 warnings、script SHA-256 `93eaaf928a3853b84a0231d313ce8eff8af6fb13c04f05b396d0da956a709a03`**，逐句表同步。原始回執與改稿見 [`verify-2.md`](../../docs/videos/curio-s07/verify-2.md)；下一位獨立讀者須看此確切雜湊，媒體仍暫停。

2026-10-19：在新讀者開始前，作者再刪去小說章首「第二次來到橋頭」的說法，讓它直接新增橋東樹林的動作。最終待讀版 **SHA-256 `da7f4441442e48c2438c36853bb940df603b37070bef784b4109a3702bda8a12`**；仍為 96 句／88 插圖／估 8.2 分、lint 0/0，詳細說明見 [`verify-2.md`](../../docs/videos/curio-s07/verify-2.md)。此雜湊尚未取得新盲讀，不可沿用前版 12/13 結果。

## Notes

固定版本：`Ancient-China-Books/sanguozhi@10a0b1ab3019d8821262f7402366d14fb4aaa102` 與 `Ancient-China-Books/sanguoyanyi@761813427eb5685c395804493f9fbd7ad8dc7d8d`，直接段落連結見 `research.md`。`topics.json` 的未核句子有誤，此票不碰共享題庫；以本集已核文本為準。沒有呼叫 TTS、圖片或其他付費生成。協作分工只包含 `docs/videos/curio-s07/` 與此票，不改其他集。

2026-10-19：上一凍結稿 `da7f4441…` 的新獨立來源隔離盲讀得必要題 8/12、選答 1/1，不通過；四個阻斷為劇透、史書／小說時間線折返、開場二十騎回收太弱、結尾重複。固定史料主幹通過，另修小說挑戰字句與聲勢、露天窗光。集中改稿現版 `script.md` SHA-256 `59904ee2f975ac2353a612551de7521d888cd04e4ab1e3d5a327cf57c4d3e78d`，95 句／86 插圖／六章、估 8.1 分、lint 0 errors / 0 warnings，逐句表同步。原始回執與改稿見 [`verify-3.md`](../../docs/videos/curio-s07/verify-3.md)；尚待新的確切雜湊獨立盲讀和改句來源覆核，不啟動付費媒體。

2026-10-19：上一版 `59904ee2…` 真正來源隔離盲讀必要題 10/12、選答 1/1，僅 `no_spoiler` 開場透露敵不敢近及劉備責備、`no_recap` 二十騎重複無回呼。固定史料主幹全過，視覺另指出六處小說鏡頭缺書頁邊框，曹操傘蓋後切本傳欠先行口頭來源標示，夏侯傑的「將領」軍階不宜取自毛評夾註。現稿已精準修正，**新 script SHA-256 `0dc3ae9aeb4fddab7d8063cfe26b5f0a237d40716d50eb3eee9d54a64326190b`**，95 句／86 插圖／六章，估 8.1 分、lint 0/0，逐句表同步。原始回執及改稿見 [`verify-4.md`](../../docs/videos/curio-s07/verify-4.md)；仍待新獨立盲讀／來源覆核，媒體暫停。

2026-10-19：`0dc3…` 新來源隔離盲讀必要題 11/12、選答 1/1，僅開場最後一問沒有銜接下一章劉表去世；固定史料主幹通過，唯曹操撤傘蓋後仍在傘下的畫面提示應改。現已改開場為「劉備一行為什麼會被追到這座橋前？」並把敘事掛鉤接到曹操追擊，畫面改露天。**待讀新劇本 SHA-256 `837364aec8522270db48b65f4fd25734573f01d62b877732803ccea7d94602e0`**，95 句／86 插圖／六章、估 8.1 分、lint 0/0；逐句表同步。詳 [`verify-5.md`](../../docs/videos/curio-s07/verify-5.md)、[`blind-5.json`](../../docs/videos/curio-s07/blind-5.json)、[`source-5.json`](../../docs/videos/curio-s07/source-5.json)。仍待新確切雜湊盲讀，付費媒體暫停。

2026-10-19：`837364…` 新來源隔離盲讀必要題 10/12、選答 1/1：兩個章節銜接點問後未直接接續、相鄰重念五千。史料主幹無矛盾，但舊開場問「劉備全隊到橋前」超出傳記；撤傘蓋後畫面已合。現稿改成追兵到當陽長坂的問題，下一句直接接劉表之死；小說章問曹操是否親來、下一句回答；橋前人數限制不再重念五千。掛鉤改回收到長坂追及 `eb029`。**新劇本 SHA-256 `6cbbd4a1290e169310d77c076712cce5e941f1492e36ca019cfdca9cf349ff88`**，95 句／86 插圖／六章、估 8.1 分、lint 0/0。原始回執與修訂見 [`verify-6.md`](../../docs/videos/curio-s07/verify-6.md)、[`blind-6.json`](../../docs/videos/curio-s07/blind-6.json)、[`source-6.json`](../../docs/videos/curio-s07/source-6.json)。待新確切雜湊盲讀，付費媒體暫停。

2026-10-19：`6cbb…` 兩位真正來源隔離讀者同版雙讀分別 **13/13** 與 **12/13**；後者唯一 `no_toc` 不接受章首「得從…說起」，其餘章節銜接與無重複均過。固定史料抽核無主張阻斷。為消除單一爭議，章首改成直接事件句，兩個敘事掛鉤改指實際回答，兩張畫面移除第二人暗示。**新劇本 SHA-256 `2aecf1a65647b9ee23b22658250c03fb18edc3e9c5f6d1cfe066ef8da390c822`**，95 句／86 插圖／六章、估 8.1 分、lint 0/0。詳 [`verify-7.md`](../../docs/videos/curio-s07/verify-7.md)、兩份原始盲讀與來源表；待新確切雜湊盲讀，不啟動付費媒體。

2026-10-19：`2aec…` 新來源隔離讀者確切雜湊盲讀 **13/13**，固定《三國志》卷 32/35/36 與《演義》第 41/42 回抽核無阻斷。`eb070` 掛鉤 metadata 微調到實際回答的 `eb071`，重產劇本 SHA 與 narrative hash 均維持不變、lint 0/0。現版 outline/script 已依使用者既有授權本機核准；Gemini／Sulafat 95 句旁白合成已開始，須等待實際片長和 `check-audio`。**S07 插圖仍暫停**。原始十三題及 CLI 通過回執、史料抽核見 [`verify-8.md`](../../docs/videos/curio-s07/verify-8.md)、[`blind-8.json`](../../docs/videos/curio-s07/blind-8.json)、[`narrative-8.json`](../../docs/videos/curio-s07/narrative-8.json)。

2026-10-19：初版旁白 95 句實長 09:04.6，首輪 `check-audio` 六句誤辨；定點重錄後仍有三句同音混淆。僅改 `eb061/065/071` 辨音詞，新劇本完整 SHA-256 **`73ace39d6b07a68d59bf077b6bd6e30a565fb5d86baed910d6f774183eb169b2`**，95 句／86 鏡頭／lint 0/0。新的來源隔離讀者 raw **13/13**、CLI round 5 通過，固定《演義》第 42 回對改句抽核成立；原始證據及處理見 [`verify-9.md`](../../docs/videos/curio-s07/verify-9.md)、[`blind-9.json`](../../docs/videos/curio-s07/blind-9.json)、[`narrative-9.json`](../../docs/videos/curio-s07/narrative-9.json)。已依站主持續授權重核准劇本，只新配三句，最終旁白 **09:04.3**，`check-audio` **95/95、0 旗標**；後台 audio 審聽 pending，本機代記核准不冒稱站主親聽。Lyria 配樂花 US$0.08，實檔 177.633 秒、組片須循環並查接縫。**S07 插圖尚未啟動**，等系列負責者排共享配額。

2026-10-20 03:12 UTC：86 景中 35 景提示詞修訂完成，刪掉夏侯傑落馬無傷的無據結果，晚漢衣甲與同一橋頭光線連續；獨立全景及定點覆核 PASS。現行 `video.json` SHA `07cf926883aa0d5de6f7758984afe04a4cdb5be42ec3a06f0d6b621c5143467b`，lint 0／0，僅 prompt 變動；畫完須查書頁黑框與假字。見 [開畫前覆核](../../docs/videos/curio-art-preflight-2026-10-20.md)。

2026-10-20：付費開畫前精算整集圖樂硬上限為 **US$3.57**。86 張插圖每張至多三次，單次圖片與評審合計 US$0.0135，最壞情況 `86 × 3 × 0.0135 + 0.08 = US$3.563`，須向上取至分，不能用 US$3.56 作硬停值。`keyframes --dry-run --takes 2` 報圖片至多 US$2.32；三次報價約 US$3.48。現行媒體帳簿只有一筆已完成的 Lyria 配樂 **US$0.08**，圖片 0 張、評審 0 次、預留 US$0.00，故尚可用於圖片的核准上限為 **US$3.49**。生成圖須逐張全尺寸檢查，仍受共用 MiniMax 時窗約束；精算與帳簿見 [`verify-10.md`](../../docs/videos/curio-s07/verify-10.md)。

2026-10-20：第二輪開畫前提示詞定點加固完成。**精確 `video.json` SHA-256 `7ff83907df8418f927d5410e1e3533fb1a07aea4cf7610abd2b912502171ea95`**；相對上一凍結稿，結構化比對證明僅 62／86 張 `data.prompt` 改動，95 句旁白、來源、卡片與分鏡其餘欄位均未動。成人晚漢人物服飾、張飛／劉備跨鏡連續性、當代史料對讀、小說書頁邊框、夏侯傑落馬與橋材不明等邊界經**獨立全 86 景覆核 PASS**，lint **0 errors／0 warnings**。`check:tasks` 及 `test:docs-videos` 通過；媒體帳簿仍只有已批准配樂 **US$0.08**，圖片／判圖 0，硬上限 **US$3.57**。這一輪沒有任何新圖片、判圖或音樂請求；成圖後仍須全尺寸視覺審查。詳 [`verify-11.md`](../../docs/videos/curio-s07/verify-11.md)。

2026-10-20：現行 `video.json` 與已核准劇本雜湊未變；`review-pull --gate audio` 對現行時間軸回覆 **already recorded**，95 句音檢未解旗標 0。現行 86 景 `keyframes --dry-run --takes 3` 報 `image-01` 1K、提示詞無超長、單輪約 US$1.16、三輪至多約 US$3.48；帳簿仍只花配樂 US$0.08，圖片／判圖／預留 0，精確最壞總額 US$3.563，硬上限 US$3.57。**尚未請求付費插圖**；等 S05／S40 共用每小時時窗空出才啟動，成圖後所有選定檔逐張原尺寸檢查，任何三輪失敗景不得自動購買第四輪。詳 [`verify-12.md`](../../docs/videos/curio-s07/verify-12.md)。

2026-10-20：上架文字對照 S34 現行包，修正 S07 描述的「對象」行，避免工具把 AI 插圖聲明錯排在開頭；原文與頻道 URL 均由上傳包附上。只改 `youtube.description`，`video.json` 新完整 SHA-256 **`ba6bfc13ad087665a9f68eec94f33cb46b795e6ed5eaf91164a08d73705b2426`**；86 景視覺 hash `8a732ad1b399d32b`、look hash `98a370ae40badbaf`、劇本與旁白時間軸未變，lint 0/0、音訊核准仍有效。預演說明有頻道 URL 1 條、固定史料 URL 5 條；濃縮開場 35.6 秒後插入 5 秒片頭，預估 21 秒片尾最後 16 秒需 Studio 匯入可點元素。開畫後至上架的逐步指令、時碼及驗收在 [`verify-13.md`](../../docs/videos/curio-s07/verify-13.md)。**S07 仍維持插圖 0 費用**，等 S26 製作者明確釋出共用 MiniMax 時窗才付款開畫。
