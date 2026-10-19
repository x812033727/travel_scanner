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
- [ ] 旁白、插圖、分鏡、配樂、成片、字幕與上架包依 `curio-episode` 關卡製成；媒體與站台權杖留在工作目錄。
- [ ] 若後續製作受核准或站台關卡限制，在此票留下確切狀態、來源及可續作指令。

## Steps

- [x] 查無 S03 同題認領，認領窄 scope，只持有 `docs/videos/curio-s03`；不編輯 S01／S09／S18 或共用 `topics.json`。
- [x] 固定《三國志》裴注、魏書相關紀年及《三國演義》原文；研究和另一人獨立覆核。
- [x] 起草 A 案企劃、`video.json`／`script.md`、逐句主張對照、十個回收懸念。
- [x] 跑敘事盲讀並修稿；定稿 13/13 通過，系列 lint 0 errors／0 warnings。
- [ ] Gemini Sulafat 旁白合成、`check-audio` 後續媒體製作。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s03`；`node tools/video/cli.mjs script --slug curio-s03`；`npm run test:docs-videos`。媒體製作後依序 `status`、`check-audio`、`keyframes`、`qa`、`package`。

## Notes

2026-10-19：`raw.githubusercontent.com` 可取殆知閣《三國志》全書轉錄，郭沖三事與裴松之的反駁同在〈諸葛亮傳〉，來源 repo HEAD `4a6d6f2088825f132521d848c2ea86cf9c9a7620`。當前轉錄有缺字與 OCR 異文，關鍵引文需另一轉錄交叉覆核。郭沖版有開四門、掃地、司馬懿退兵，**沒有彈琴**；裴松之說當時司馬懿鎮宛城，並提出戰術、魏延領兵、司馬駿態度等疑點。《三國演義》的琴只能作小說畫面，不可說成史實。原文官方網站在雲端網路政策下部分回 403，已找到可讀 GitHub 備援。2026-10-19 站主要求下一支直接用推薦題目持續做；先做無付費前製。

2026-10-19：獨立來源覆核改用 Ancient China Books 固定版本，核《三國志》卷35／卷3、《晉書》卷1及《三國演義》毛評本第95回；詳細引文、SHA、敘事邊界在 `docs/videos/curio-s03/research.md`、`verify-1.md`。A 案全文 103 句、89 張插畫、約 9.1 分鐘；`claims.md` 覆蓋 ef001–ef103，十個懸念，`lint` 0 errors／0 warnings。`script --slug curio-s03` 已寫 `script.md`，`npm run test:docs-videos` 236 passed；`npm run check:tasks` 驗證 2070 票通過（警告是其他既有任務）。MiniMax `keyframes --takes 3 --dry-run` 報 89 張、一次約 US$1.20、最多三次約 **US$3.60**，本集目前 US$0，沒有付費生圖。**下一步：**獨立讀者只讀劇本做十三題盲讀；修正後重跑 lint、script，依站主「以你推薦的就好不用問我」授權記錄大綱／劇本關卡，再 TTS、check-audio。付費插圖須按站主的全集成本界線與主代理排程協調，切勿與 S34 付費生圖並發。

2026-10-19：第一位獨立盲讀者 13 題中有 8 題指出問題：開場未點名地點且提早說出結局、後段重演小說場面、追問寫成序號、章節銜接、懸念回收與重複句。已逐項修正：開場點明**小說西城縣**而停在司馬懿勒馬，留下四個未解疑問；後段只補小說原文的扮裝、童子及退兵；刪掉清單口吻並接好章末與章首；魏延方案合併，誤把琴認成史實的推理寫明。新版仍是 103 句、89 張插畫、約 9.2 分鐘，`lint` 0 errors／0 warnings，`script.md` narrative hash `0e0d8d79b8d65961`。**等待另一位完全獨立讀者只看新版旁白做第二輪十三題；此版尚未核准，也未付費合成。**

2026-10-19：定稿完成。獨立逐句史料覆核另抓出裴注位置、郭沖的一萬守城者、隔天探子回報及沒有來源的夜晚／試探城門等問題，已一次修正；最新精度抽查 PASS。全新盲讀者只見定稿旁白，**13/13 通過**；完整證據與改稿邊界見 `docs/videos/curio-s03/verify-2.md`、`narrative-answers.json`。現行 `script.md` SHA256 `16fb728987aa09da8526c94cd401cc28bc72b287bea6c63c6f6d3dcfe0b0a0dd`，narrative hash `c588d2a432d8039a`；103 句、89 張插畫、約 9.2 分鐘、`lint` 0 errors／0 warnings。依站主 2026-10-19「以你推薦的就好不用問我」「一直做完所以影片」的委託，製作方選 A 案並在本機記錄 `outline`／`script` 檔案雜湊關卡；記錄註明站主沒有逐字看此 S03 定稿。最終 TTS dry-run 為 101 requests、2,190 Gemini 字元、佔每月免費額 0.4%；**18:44 UTC 已開始實際 Gemini Sulafat TTS**，下一步 `check-audio`。付費 keyframes 尚未開始，89 張最多三次估 US$3.60，待主代理協調 S34 成本與排程。媒體與站台權杖只在 `/workspace/.video-work/curio-s03/` 工作目錄，不入 Git。
