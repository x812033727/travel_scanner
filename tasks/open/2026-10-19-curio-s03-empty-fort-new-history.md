---
id: 2026-10-19-curio-s03-empty-fort-new-history
title: Curio S03 Empty Fort new history episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-s03
claimed_at: 2026-10-19T17:51:28Z
created_at: 2026-10-19T17:51:25Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s03
---

# Curio S03 Empty Fort new history episode

## Why

站主要求在 S34 後繼續製作新的歷史影片，選題與執行採推薦方案，不再逐步詢問。S01 赤壁、S09 桶狹間、S18 拿破崙另有工作者認領。S03「空城計那天，司馬懿根本不在那裡？」是未認領的 S 軸候選；《三國志》裴注收郭沖故事，也收裴松之逐點反駁，可以把一個傳說如何被檢驗寫成約十分鐘單線故事。

## Definition of done

- [x] 企劃、大綱、逐句有據的繁中劇本、兩層史料查核與盲讀通過，系列 lint 0 errors／0 warnings。
- [x] 旁白、插圖、分鏡、配樂、成片、繁中字幕與上架包依 `curio-episode` 關卡製成；媒體與站台權杖留在工作目錄。
- [x] 站台審核與其餘語言尚需續作的狀態、來源及路徑已記錄在此票。

## Steps

- [x] 查無 S03 同題認領，認領窄 scope，只持有 `docs/videos/curio-s03`；不編輯 S01／S09／S18 或共用 `topics.json`。
- [x] 固定《三國志》裴注、魏書相關紀年及《三國演義》原文；研究和另一人獨立覆核。
- [x] 起草 A 案企劃、`video.json`／`script.md`、逐句主張對照、十個回收懸念。
- [x] 跑敘事盲讀並修稿；定稿 13/13 通過，系列 lint 0 errors／0 warnings。
- [x] Gemini Sulafat 旁白合成與 `check-audio`：終稿 101/101 句核對、0 flagged、旁白 09:36。
- [x] 依主代理排程製作插圖、分鏡、配樂、繁中字幕、成片與上架包。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s03`；`node tools/video/cli.mjs script --slug curio-s03`；`npm run test:docs-videos`。媒體製作後依序 `status`、`check-audio`、`keyframes`、`qa`、`package`。

## Notes

2026-10-19：`raw.githubusercontent.com` 可取殆知閣《三國志》全書轉錄，郭沖三事與裴松之的反駁同在〈諸葛亮傳〉，來源 repo HEAD `4a6d6f2088825f132521d848c2ea86cf9c9a7620`。當前轉錄有缺字與 OCR 異文，關鍵引文需另一轉錄交叉覆核。郭沖版有開四門、掃地、司馬懿退兵，**沒有彈琴**；裴松之說當時司馬懿鎮宛城，並提出戰術、魏延領兵、司馬駿態度等疑點。《三國演義》的琴只能作小說畫面，不可說成史實。原文官方網站在雲端網路政策下部分回 403，已找到可讀 GitHub 備援。2026-10-19 站主要求下一支直接用推薦題目持續做；先做無付費前製。

2026-10-19：獨立來源覆核改用 Ancient China Books 固定版本，核《三國志》卷35／卷3、《晉書》卷1及《三國演義》毛評本第95回；詳細引文、SHA、敘事邊界在 `docs/videos/curio-s03/research.md`、`verify-1.md`。A 案全文 103 句、89 張插畫、約 9.1 分鐘；`claims.md` 覆蓋 ef001–ef103，十個懸念，`lint` 0 errors／0 warnings。`script --slug curio-s03` 已寫 `script.md`，`npm run test:docs-videos` 236 passed；`npm run check:tasks` 驗證 2070 票通過（警告是其他既有任務）。MiniMax `keyframes --takes 3 --dry-run` 報 89 張、一次約 US$1.20、最多三次約 **US$3.60**，本集目前 US$0，沒有付費生圖。**下一步：**獨立讀者只讀劇本做十三題盲讀；修正後重跑 lint、script，依站主「以你推薦的就好不用問我」授權記錄大綱／劇本關卡，再 TTS、check-audio。付費插圖須按站主的全集成本界線與主代理排程協調，切勿與 S34 付費生圖並發。

2026-10-19：第一位獨立盲讀者 13 題中有 8 題指出問題：開場未點名地點且提早說出結局、後段重演小說場面、追問寫成序號、章節銜接、懸念回收與重複句。已逐項修正：開場點明**小說西城縣**而停在司馬懿勒馬，留下四個未解疑問；後段只補小說原文的扮裝、童子及退兵；刪掉清單口吻並接好章末與章首；魏延方案合併，誤把琴認成史實的推理寫明。新版仍是 103 句、89 張插畫、約 9.2 分鐘，`lint` 0 errors／0 warnings，`script.md` narrative hash `0e0d8d79b8d65961`。**等待另一位完全獨立讀者只看新版旁白做第二輪十三題；此版尚未核准，也未付費合成。**

2026-10-19：定稿完成。獨立逐句史料覆核另抓出裴注位置、郭沖的一萬守城者、隔天探子回報及沒有來源的夜晚／試探城門等問題，已一次修正；最新精度抽查 PASS。全新盲讀者只見定稿旁白，**13/13 通過**；完整證據與改稿邊界見 `docs/videos/curio-s03/verify-2.md`、`narrative-answers.json`。現行 `script.md` SHA256 `16fb728987aa09da8526c94cd401cc28bc72b287bea6c63c6f6d3dcfe0b0a0dd`，narrative hash `c588d2a432d8039a`；103 句、89 張插畫、約 9.2 分鐘、`lint` 0 errors／0 warnings。依站主 2026-10-19「以你推薦的就好不用問我」「一直做完所以影片」的委託，製作方選 A 案並在本機記錄 `outline`／`script` 檔案雜湊關卡；記錄註明站主沒有逐字看此 S03 定稿。最終 TTS dry-run 為 101 requests、2,190 Gemini 字元、佔每月免費額 0.4%；**18:44 UTC 已開始實際 Gemini Sulafat TTS**，下一步 `check-audio`。付費 keyframes 尚未開始，89 張最多三次估 US$3.60，待主代理協調 S34 成本與排程。媒體與站台權杖只在 `/workspace/.video-work/curio-s03/` 工作目錄，不入 Git。

2026-10-19 19:19 UTC：以上為第一版核准稿的歷程；**現行終稿**在旁白覆核後改為 101 句、88 張插畫，`script.md` SHA256 `2234d642112d0e8322555d46c37ddd08ab978db614b76c45d5b3229128a624b1`，narrative hash `11a95e26a6291430`，`lint` 0 errors／0 warnings。兩輪音檔訂正與兩位全新盲讀者的精確版本 13/13 通過詳見 `docs/videos/curio-s03/verify-3.md`；`narrative-answers.json` 已換成現行稿答案。本機 script 關卡重綁新 SHA，註明站主未逐字審稿。Gemini Sulafat 旁白已完成 09:36，`check-audio` **101/101、0 flagged**。MiniMax 最終 dry-run 88 張，一輪約 US$1.19、最多三輪 US$3.56；尚未付費生圖。**後續指令：**與主代理協調後在同一 `VIDEO_WORKDIR` 先執行 `keyframes --slug curio-s03 --takes 3`，再依 `curio-episode` 關卡做 `review`／`music`／`build`／`qa`／`package`。不要用 `/tmp/s03-build.py` 重生已核准稿；目前媒體與站台權杖仍留在 `/workspace/.video-work/curio-s03/`，未進 Git。

2026-10-19 19:21 UTC：主代理依站主既有委託授權啟動 S03 完整媒體製作。`review-push --gate audio` 已送後台，手動製作片呈 pending；本機 audio 關卡另以站主廣泛委託記錄，明寫**站主未親聽**，綁 timeline SHA `8095d6521249…`。88 張 `keyframes --takes 3` 正在執行，exec session `89956`，完整進度日誌 `/workspace/.video-work/curio-s03/keyframes-run.log`；本集圖像費用尚待命令完成後核 ledger。勿在生成時編輯 `video.json`。若中斷重跑同一 keyframes 指令，已通過圖像吃快取；結束後只修評審三次失敗的景，再送 storyboard 關卡、配樂與後製。

2026-10-19 20:01 UTC：MiniMax 執行中，`keyframes/manifest.json` 已記 47／88 張；`fort-032`、`fort-045` 三次評審未過，`media/ledger.json` 合計約 US$0.935。人工抽查前 55 景已見幾處**會誤導時代的已通過畫面**：`fort-018` 的 228 年撤軍竟有現代推車和領帶，`fort-040` 的漢中山路成了有標線的公路；`fort-001` 的琴形與撫弦動作、`fort-038` 的裴松之執筆場景也待局部重畫。等整批結束後一次改提示詞，重新執行同一 `keyframes --takes 3` 命令；舊圖快取避免重收其他景。固定小說連結的文字檔已補足 40 字 commit；`video.json` 的來源 URL 待影格工作退出時連同提示詞一次修正，避免中途更動設定。

2026-10-19 20:09 UTC：首輪生圖於 `fort-062` 通過後遇網站 `請求過於頻繁，請稍後再試`，exec session `89956` **退出碼 4**；三集同時觸發站台頻率限制，主代理統一協調恢復。S03 manifest 有 **54／88** 張（51 通過、`fort-032`／`fort-045`／`fort-056` 三張待修），ledger **US$1.08**。人工逐格檢查已完成這 54 張：另九張評審雖過、畫面卻有錯誤琴形、現代推車／領帶、現代公路、世界地圖、鳥居、擬人狗或高樓背景，會誤導旁白。已只改這 12 張的 `video.json` 提示詞，並補正毛評本小說來源的完整 40 字 commit；**旁白逐句文字沒有改動**，`script.md` SHA256 仍為 `2234d642112d0e8322555d46c37ddd08ab978db614b76c45d5b3229128a624b1`，`video.json` 新 SHA256 `916d9e6072b9a2ea7132fd7a08d9d7314bdec246000caffc6f9b555536b86bf5`。`lint` 0 errors／0 warnings，狀態仍認得劇本與旁白核准，dry-run 88 張／三輪上限 US$3.56。**下一步：**等主代理通知站台限流恢復，再於同一工作目錄重跑 `keyframes --slug curio-s03 --takes 3`；未改提示詞的已通過畫面應吃快取。後續新圖仍須逐格檢查，通過才進 storyboard／music／render／clips／assemble／captions／QA／package。**目前沒有啟動第二輪付費。**

2026-10-19 20:31 UTC：等候共享 MiniMax 時段時，把先前九張誤畫顯出的**同型風險**預先處理在六個尚未生成的鏡頭：`fort-064/070/079/096` 的大地圖或城標改為局部古代路線卷、圓木標或實際城門；`fort-080/085` 的琴明確寫成橫放桌上的七弦木製古琴，避免再畫成現代樂器。未增加鏡頭或費用，`script.md` SHA256 不變；`video.json` SHA256 現為 `d16729063a2542447af0105f5138139d54c9b7191557677aecf3d0c44533b519`。`lint` 仍 0 errors／0 warnings；S03 仍在等主代理安排的下一個生圖時段，沒有啟動續跑。

2026-10-19 21:21 UTC：MiniMax 續跑及十三張局部修復後，**88／88 張通過**，本集影像累計 **US$2.17**，低於已授權 US$3.56。人工覆核另排除了現代公路、教室、電燈、誤畫樂器及未扮百姓的軍人等會誤導的已通過畫面；細節見 `docs/videos/curio-s03/verify-4.md`。旁白仍是 101／101 核音通過，script SHA256 `2234d642112d0e8322555d46c37ddd08ab978db614b76c45d5b3229128a624b1`，lint 0／0。`review-push --gate storyboard` 已送站台；代理依站主廣泛委託於本機核准影像 manifest SHA 前綴 `ee0d1d3ae047`，**未稱站主親自看過**。`music` 已完成 582 秒背景音樂，總花費約 US$2.25；`render` 完成，`clips` manifest 記錄 88 張靜圖、0 動畫片段。21:22 UTC 已與主代理協調並開始獨占 CPU 的 `assemble`，日誌 `/workspace/.video-work/curio-s03/assemble.log`；完成後依序 `captions`、`qa`、`package` 並釋放 CPU 時段。

2026-10-19 21:42 UTC：S03 繁中版本完整製作。成片 09:36.73（17,302 影格）、-14 LUFS，SHA256 `1d20204f5d20bde4cbbfe20998f78eb40587d61a5e06c33ddc4515b780669059`，`check-audio` 101／101、`qa` **11／11**、`package` **4／4**。封面副標孤字換行已人工修正為「城門大開，史官質疑」；只改封面文字，keyframes 重建 **0 新圖**、分鏡重核後重新合成 **0 段重編**，最終片雜湊仍相同。完整視覺／成片紀錄見 `docs/videos/curio-s03/verify-4.md`。`review-push --gate final` 已送站台且本機依站主委託核准，備註明寫站主未親自觀看／聆聽。上架包 `/workspace/.video-work/curio-s03/upload/` 含成片、封面、繁中 CC、標題說明與合成內容揭露；英／日／韓字幕留待最終語言階段，**尚未在 YouTube 上架**。`review-push --gate publish` 正在傳送上架包到站台；若此步驟失敗可按同指令重送，不重造媒體。媒體與權杖仍不在 Git。
