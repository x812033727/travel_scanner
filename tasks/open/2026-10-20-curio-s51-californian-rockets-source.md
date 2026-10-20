---
id: 2026-10-20-curio-s51-californian-rockets-source
title: Curio S51 Titanic Californian rockets sourced preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T15:40:39Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s51
---

# Curio S51｜鐵達尼號求救火箭與加州人號

## Why

Amber Room S51 來源在本環境無法重開，因此原題暫緩，見 [Amber 來源票](2026-10-20-curio-s51-amber-room-source.md)。本票承接 S51 編號：用可固定的 1912 年正式調查與倖存者原著回答，加州人號看見求救火箭卻沒有到場的經過。要分清證詞、調查的船名歸納、距離估計與不能證實的救援反事實。

## Definition of done

- [x] `docs/videos/curio-s51` 有 A／B 企劃、固定來源研究、逐句主張表、8 分鐘以上的繁中同一故事線稿、Curio 插圖分鏡 JSON、作者自檢與內容雜湊。
- [ ] 獨立來源審核與兩位不同盲讀者審核**同一套 hash**；任何修訂後重新鎖版本。
- [ ] 網站大綱／劇本、音訊、分鏡與成片關卡完成；TTS 正文實測至少 8 分鐘、Studio 最後 16 秒元素可點。

## Steps

- [x] 檢查 S34–S50 與已認領 S01／S09／S18 的邊界；S51 題目無重複。
- [x] 從固定 Git 提交直接讀 1912 年調查、Beesley 與 Gracie；記原文 SHA 和證據限制。
- [x] 寫 137 景、140 句、12 組伏筆的 A 案；執行 lint、對齊與作者自檢。
- [x] 獨立來源人員對 `author-selfcheck.md` 的固定檔與爭點覆核；史料旁白 PASS、書面畫面 HOLD，修補後須重核畫面差分。
- [x] R1 兩位不同讀者盲讀同一版本；`chapters_link`、`payoffs`、`no_recap` 共同 No，正式 FAIL。
- [x] R2 書面畫面獨立差分覆核；四景仍 HOLD，R1 敘事 FAIL 未變。
- [x] R3 作者按兩份報告修 12 句、6 景提示詞與伏筆，凍結精確五檔雜湊；作者 lint 0／0。
- [x] R3 由未參與作者修稿的人做精確來源與書面畫面差分覆核；旁白與六景畫面 PASS，主張表 `cal061` 少一個來源錨點而整包窄 HOLD。
- [x] 只把 `claims.md` 的 `cal061` 錨點補成 R05、R07，記新雜湊。
- [x] 另一人獨立核對 `cal061` 錨點差分，來源包窄 HOLD 解除。
- [x] R3 兩位新劇本讀者均指出敘事問題；作者 R4 定點改稿並凍結 140 句與 16 組伏筆。
- [x] 另一位工作者獨立覆核 R4 精確來源及書面畫面；新增書面畫面 PASS，但 `cal107` 調查時序窄 HOLD，待作者修稿與新版差分覆核。
- [x] R4 兩位只讀劇本的新讀者共同指出 `cal135` 目錄式回頭與重述；作者 R5 修 `cal107` 報告日期、`cal135/136` 結尾回收，重凍結五檔雜湊。
- [ ] 另一位工作者對 R5 精確五檔做來源、主張與書面畫面差分覆核。
- [ ] 兩位真正隔離的新讀者只讀同版劇本做 13 題盲評，之後才走站台與媒體關卡。

## How to verify

在 repo 根目錄執行 `node tools/video/cli.mjs lint --slug curio-s51 --json`，應為 0 errors／0 warnings；`sha256sum docs/videos/curio-s51/{brief,research,claims,script}.md docs/videos/curio-s51/video.json` 與 `author-selfcheck.md` 對照。腳本、主張表與 JSON 逐句同文；`npm run check:tasks` 驗證本票。後續實際生成旁白再檢查首 8 景後的正文長度，並在私人上傳後檢查 21 秒片尾末 16 秒元素。

## Notes

- 2026-10-20：作者前製完成，精確內容與來源 SHA 見 `docs/videos/curio-s51/author-selfcheck.md`。英國調查原文承認 Stone、Gibson 與 Lord 的回報矛盾，也把船名與距離寫成調查判斷；稿子沒有把「五英里」或「能救全船」講成事實。
- lint 0 errors／0 warnings；140 句對齊，137／137 正文景為可愛歷史插畫計畫。專案估時在最快 325 CPM 時，濃縮開場約 36.2 秒，後段正文約 519.1 秒。**尚無**實際 TTS、MiniMax 圖、配樂、片頭片尾合成、網站審核或發布；不要把作者檢查當獨立簽核。
- 因後續關卡尚未完成，此票釋回供獨立查核者接手；不在本代理的共用分支上提交。
- 2026-10-20：[R1 獨立史料／書面畫面覆核](../../docs/videos/curio-s51/review/r1-source-independent.md) 重新下載三份固定原文、比對位元組 SHA，140／140 台詞三檔一致、137 個提示詞全讀、lint 0／0。**旁白史料 PASS；書面畫面 HOLD**：`cal004/008/016/028/032/040/044/052/064/068/072/076/080/088/092` 把夜間事件加 `pale dawn light`，`cal089/091/092` 把夜船橋與事後調查員混在一起，`cal118–119` 把 Beesley 的書中論述畫成當年聽證桌寫作；另查 `cal067/098` 與未引證儀表。只修提示詞並重凍結，再由另一人做畫面差分。兩位新讀者可以先盲讀現稿，但音訊／圖像／成片與站台關卡未開始。
- 2026-10-20：[R2 作者提示詞候選版](../../docs/videos/curio-s51/verify-2.md)只改 `video.json` 中 75 個 `data.prompt`；其餘故事 payload SHA 不變，140／140 句三檔同文，lint 0 errors／0 warnings。R1 視覺 HOLD 的夜景光線、船橋與後來調查混場、Beesley 聽證錯置、04:00 船影與無依據儀表均在書面提示詞修補；**須由另一人做提示詞差分覆核，這不是 PASS**。主線回報 R1 兩名敘事盲讀者對章節銜接、回收及重述均判 No，因此敘事為 FAIL，待獨立 R3 文字修稿、來源與盲讀重檢。
- 2026-10-20：[R2 獨立書面畫面差分覆核](../../docs/videos/curio-s51/review/r2-visual-independent.md)：五檔和三份固定來源 SHA 相符；R1→R2 精確只有 75 個 `data.prompt` 改動，差分表 75／75 精確，故事 payload 同 hash；140／140 旁白三檔同文、137／137 正文景皆有提示詞、lint 0／0。**畫面仍 HOLD**：`cal133` 把 G 明記 04:10 接首艇時「剛天亮」改成黎明前暗景；`cal040–041` 新增未獲證實的船燈遮板機構；`cal064` 的泛稱 flare 須約束為發射座上的白色求救火箭，避免手持／彩色煙火。R1 夜景、事後調查混場、Beesley 書中視角與無線電儀表問題已解；只修提示詞並重凍結再核，不把書面覆核當圖像驗收。敘事 FAIL 仍待 R3 與重盲。
- 2026-10-20：[R3 作者修稿](../../docs/videos/curio-s51/verify-3.md)：12 句回應 R1 的章節銜接、問題回收及重述；6 景提示詞修 R2 的遮燈裝置、白火箭與 04:10 天色，另把約 06:00 寫成一般早晨日光；14 組伏筆。精確 `video.json` SHA `70aa784c4f6175e557e3addd6550e2c0068047bac85e0a3a9690a81b1b855226`、`script.md` `734cf4d7c474cd24a7dba87db738d07575654cbbd4ec84ad7006a7ff4b795a40`；140／140 三檔同文，lint 0 error／0 warning。按 325 CPM 最快估速開場 36.17 秒、正文 530.50 秒，仍非 TTS 實長。**作者候選**；R3 獨立來源／畫面與兩名全新隔離讀者的正式雙盲未完成，不得開始 TTS、付費插畫或成片。
- 2026-10-20：[R3 獨立來源及書面畫面差分](../../docs/videos/curio-s51/review/r3-source-independent.md)重讀 G/B/A 固定原文、核 12 句改稿和 R2→R3 精確 6 景提示詞；旁白史料與書面畫面 **PASS**，140／140 三檔逐字一致、137／137 shot 有提示詞、lint 0／0。**整份來源包暫 HOLD** 僅 `claims.md` 的 `cal061` 錨點：新旁白提船橋仍有人值班，但該列只連無線電休班 R05；G 3420–3442／研究 R07 直接支持船橋及白火箭。只補成 `R05、R07`，不改 140 句口播／畫面；再由另一人核對主張表差分。敘事雙盲、網站及媒體未開始。
- 2026-10-20：作者只修 `claims.md` 的 `cal061` 一格為 R05、R07，詳[錨點收據](../../docs/videos/curio-s51/review/r3-claims-anchor-author.md)，新 claims SHA `20ffe5c07e4210a248f0ea6daa9c3ab6131165df64f75ee79fafca68f620a8c6`；台詞、腳本、視覺和固定原文雜湊未變，待另一人差分覆核。R3 兩位新讀者各自判敘事 FAIL，交集有 `chapters_link`、`payoffs`、`no_recap`；A 曾讀通用技能檔，會列隔離限制，不能把這組當 PASS。R4 須修故事後再由只讀劇本的新讀者覆核。TTS／付費圖仍停。
- 2026-10-20：[獨立單格差分](../../docs/videos/curio-s51/review/r3-claims-diff-independent.md)直接對 G 3192–3197、3420–3442 及研究 R05／R07，重建舊 claims SHA `d711c1f...`，證明新 SHA `20ffe5c...` 只添 `cal061` 的 R07 錨點；**R3 來源包窄 HOLD 解除、來源與書面畫面 PASS**。劇本雙盲仍 FAIL，故待 R4 改稿與新覆核；無語音、圖像、成片或網站核准。
- 2026-10-20：R4 [作者改稿凍結](../../docs/videos/curio-s51/verify-4.md)按兩份 R3 劇本盲讀診斷修 12 句（含 `cal008/020/022/024/061–063/106/133–136`）、兩個日間證據桌提示詞與伏筆；沒有更動固定 G/B/A 研究。精確 `video.json` SHA `fd6fc00c3db43f7da576292e62317eb61aaa685af8dcf2f59500865cb87eb492`、`script.md` `7d84f152e2051430ec5ca034e79a19f743061af221531232bb44292f94c0583c`、`claims.md` `38b59f59d0155cb8ecd82b3433a2914a810ab5e331eb0f935c3203cad60fe6f1`；140/140 逐字對齊、lint 0 errors／0 warnings，最快估速開場 36.37 秒、正文 8:58.77。這只是作者候選；R4 新來源／畫面獨立覆核與兩名真正只讀劇本的新讀者尚未做，TTS／插圖／成片仍停。
- 2026-10-20：[R4 獨立來源／書面畫面覆核](../../docs/videos/curio-s51/review/r4-source-independent.md)對三份固定原文重新驗 SHA、逐一核改句與主張表；新 `cal135/136` 畫面 PASS，140/140 逐字對齊、137/137 shot 有提示詞、lint 0/0、16 組伏筆。**旁白史料窄 HOLD 僅 `cal107`**：「幾個月後，英國正式調查……」模糊成調查幾個月後才開始，實為 4/23 任命、5/2 開庭；7/30 才是正式報告日期。作者應改為「到了七月底，英國正式調查報告逐一對照船橋證詞。」並在 R11 或 `cal107` 加 G 143–166 日期錨點，視需要改 `cal107` 畫面為後續報告桌；新版本重凍結再由另一人核對差分。未做媒體生成。
- 2026-10-20：[R4 隔離新讀者 A](../../docs/videos/curio-s51/review/r4-fresh-panel-a.md)、[B](../../docs/videos/curio-s51/review/r4-fresh-panel-b.md)共同判 `one_line`、`no_toc`、`no_recap` No，問題集中在 `cal135` 宣告「回到開頭」與重述已知事實；A 另判 `payoffs` No。這是精確 R4 的敘事 FAIL，不能沿用至 R5。
- 2026-10-20：[R5 作者修稿凍結](../../docs/videos/curio-s51/verify-5.md)：`cal107` 改七月底正式報告並加 G 日期與 5 月開庭錨點，書面畫面改日間後續報告桌；`cal135` 用史東證詞中「有新消息再派實習生」的未述細節回答通報後下一步，`cal136` 以船長記得一枚作具體回呼，畫面與兩組伏筆同步。`video.json` SHA `1e8feed428c617ced77d251a328f1b75ba8d498cf103e11bee51720a6ee59b22`、`script.md` SHA `dcebb60865b561b5b38b5bb163fdd18b9961dbb26e1676903f47167fc4abba8d`；140/140 三檔同文，lint 0/0，最快估速開場 36.37 秒、正文 8:59.90。**僅作者候選**；須他人按精確雜湊獨立核來源與畫面、兩位全新只讀劇本讀者重做盲評，站台及媒體仍待。
