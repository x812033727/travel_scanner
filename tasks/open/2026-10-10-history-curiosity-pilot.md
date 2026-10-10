---
id: 2026-10-10-history-curiosity-pilot
title: 歷史與奇異：站主選畫風與前三題後，本機做兩集試片並記實測
status: review
priority: P2
area: docs
owner: claude-fable-curio
claimed_at: 2026-10-10T00:32:30Z
created_at: 2026-10-10T16:20:00Z
completed_at:
branch: claude/history-curiosity-video-series-aade32
depends_on: []
scope:
  - docs/videos/history-curiosity/
  - docs/videos/curio-h01/
  - docs/videos/curio-u02/
  - docs/videos/curio-l08/
---

# 歷史與奇異：站主選畫風與前三題後，本機做兩集試片並記實測

## Why

站主 2026-10-10 要一個「歷史與奇異」的新內容線（內容參考馬臉姐、畫面參考 cheap 的可愛插畫、插圖由 MiniMax 生成、可放實體照片）。企劃、40 個候選題、畫風規格與四種畫風樣張在 `docs/videos/history-curiosity/`，成本是估的，題目沒查核。開播前要知道一集真的花多少、節奏對不對、MiniMax 的可愛卡通一整支看起來一不一致。

## Definition of done

- [x] 站主 2026-10-10「用你建議的」：系列名奇聞檔案局、畫風第 3 版（A＋C 色盤）、過世 70 年以上的歷史人物可畫卡通、前三題 H01／U02／L08、10 分鐘；都記在 `README.md` §選定紀錄。
- [x] 三集做完（H01、U02、L08 都在 2026-10-10 做到上架確認；H01 2026-10-10 做到上架確認：旁白、分鏡、成片、上架包四關都核准，站主在 `/admin/videos` 按了分鏡與成片；U02 未開工）（原文：建議 H01 瑪麗賽勒斯特號、U02 51 區）：`brief.md`、`video.json`（`format: "slides"`、`category: "explainer"`、選定的 `look`、`shot` 與卡片交錯、至少 3 張登記在 `assets[]` 的公有領域或圖庫照片）、`claims.md`、兩輪獨立查核、旁白（Whisper 第二轉寫）、`keyframes`（`--dry-run` 印出 `minimax image-01`）、`render`、`assemble`、`captions`、`qa` 11 項、`package`、`review-push` 到上架確認。
- [x] 每集的實測記在本票 Notes 與 `docs/videos/history-curiosity/README.md` §成本與產能（沒有另寫 production-record.md）；原要求：每集記在 `docs/videos/curio-<id>/production-record.md`：插圖張數與重做次數、照片張數與來源、媒體花費、審圖分數分布、旁白長度與成片長度、站主審片分鐘數。
- [x] `README.md` §成本與產能 改成實測（2026-10-10，兩集）；`topics.json` 的 H01／U02 改 `scripted` 並在 `note` 寫查核後的更正。

## Steps

- [ ] 先 `gh pr list` 與 `npm run tasks -- list`，確認沒有別的 session 在做同一批檔；claim。
- [ ] 讀 `youtube-video` skill、`docs/videos/ILLUSTRATED.md`、`docs/videos/history-curiosity/look.md`；本機工具要先借 node_modules（含 `pinyin-pro`）與 ffmpeg。
- [ ] 企劃代理寫 `brief.md`（兩三個大綱），站主選或照建議；撰稿代理寫 `video.json` 與 `claims.md`，照 look.md 的 prompt 規則（一個主體一個動作、不寫風格、文字不畫）。
- [ ] 查核：換人一輪，改超過 3 個事實再換人；每個數字寫來源與確認日期。
- [ ] 照片：`stock search`／`stock fetch` 或維基共享資源的公有領域檔（手動下載到工作目錄、寫進 `assets[]`），先用 `screenshot` 版型放。
- [ ] `tts` → `check-audio` → `pace.mjs` → `keyframes` → `render` → `assemble` → `captions` → `qa` → `package` → `review-push`；每一關的收據留在工作目錄。
- [ ] 回寫實測與 `topics.json`；站主看成片後把要改的畫風寫回 `look.md`。

## How to verify

`node tools/video/cli.mjs status --slug curio-h01`（另一集同）顯示到上架確認；`node tools/video/cli.mjs lint --slug curio-h01` 0 errors；`PYTHONUTF8=1 python -c "import json;json.load(open('docs/videos/history-curiosity/topics.json',encoding='utf-8'))"` 可解析；README 的成本數字有實測出處。

## Notes

- 2026-10-10 Shorts：三集的 `shorts.json` 是查核前寫的，已對照查核後的稿子改過（H01 的「熱飯菜是十二年後小說加的」、U02 的「上面四萬英尺」「第一次印出」、L08 的單字詞）。`from-episode --check` 三集都過；試切 `curio-h01-short-1`：38 秒、直式裁切正常（工作區 `mokaair-work/videos/curio-h01-short-1/`，最新一版記在 `LATEST.txt`）。Shorts 的旁白檢查沒有第二轉寫，「小艇／救生艇」來回被聽錯，改了四輪還剩 1 句（救生艇被聽成「就是身體」，同一個詞前一輪聽對）。**沒有 `package`／`push`**：上架包要讀長片的 YouTube 網址導回長片，三支長片都還沒上傳；等站主上傳後再切其餘五支並送站。
- 2026-10-10：L08 成片由站主核准，上架包 4／4、上架確認自動核准。三集（H01、U02、L08）都在「可以上架」，YouTube 上傳是站主的事。本票的試片工作做完；剩下的（Shorts 切片、多語、主機路線、`policy` 的有示範）各有自己的票或未排。
- 2026-10-10 L08 `curio-l08`（麥田圈）做到成片關卡：研究 dossier（19 個來源、38 條事實、來源不一致表）→ brief A 案（Jev 自動核准，有示範 0.89）→ 撰稿 114 景／134 句（插圖 92、照片 2、卡片 20）→ 查核兩輪（4＋0 處，另由協調者改 3 句）→ 旁白 11:27（第一輪被標 21 句，全是同音字，改字後第二輪全過）→ MiniMax 插圖 92 張（US$2.83；`pub-year` 四輪仍被判畫風太寫實，用 `--accept-best` 保留，成片卡會列出）→ 成片 20,879 格（11:36）→ 品管第一次就 10／11。沒過的是 `policy`：有示範 0.12（已知），另外這集「符合立場」0.52 也低於 0.6（前兩集 0.62、0.69）。旁白關卡已核准；分鏡與成片關卡在 `/admin/videos` 等站主。
- L08 多學到的：照 U02 的教訓把插圖拉到 71% 占比、每句壓在 20／22 單位，節奏一次過；公有領域的英國麥田圈空拍照找不到（Commons 上都是 CC BY／BY-SA），用了 1678 年木刻與一張作者釋出公有領域的瑞士空拍；「做／坐」「圈／村」「圓／月」「訃聞／符文」這類單字詞一定會被聽錯，動筆時就寫「製作」「麥田圈」「圓圈」「悼念文章」；撰稿代理寫的提示詞細節太多（背影＋特寫＋三個道具）時 MiniMax 會漂成 3D，92 張第一輪過 73 張，改成「一個人一個動作」後剩 1 張。
- 2026-10-10：U02 成片由站主核准，上架包 4／4、上架確認自動核准；H01 與 U02 都在「可以上架」。兩集實測已寫進 `docs/videos/history-curiosity/README.md` §成本與產能，`topics.json` 的 H01／U02 改成 `scripted`。站主說「接著繼續」，第三題 L08（麥田圈）開工：brief 已寫，研究代理在查來源。
- 2026-10-10 U02 `curio-u02`（51 區）做到成片關卡：研究代理 dossier（7 節，CIA 計畫史逐頁引句）→ brief A 案（Jev 自動核准，有示範 0.67）→ 撰稿 92 景／126 句 → 查核兩輪（8＋1 處）→ 旁白 11:36（三輪檢查全過）→ MiniMax 插圖 61 張（US$1.36）＋公有領域照片 6 張 → 成片 21,134 格（11:44）→ 品管 10／11（只剩 `policy` 有示範 0.09）；旁白與分鏡關卡已核准，成片關卡在 `/admin/videos` 等站主；核准後 `package` → `review-push --gate publish`。
- U02 多學到的：標題不能寫「否認存在 58 年」（1995 年起的總統豁免令就寫了 Groom Lake 附近的作業地點；2013 年新的是名字與地圖的刻意正式承認）；帶語氣提示的句子先壓到 20 單位以內就不會超過 8 秒；插圖占比剛好卡 50%，卡片多的稿子要留餘裕（這集把兩張大字卡換成插圖才過）；臉部大特寫容易被畫成 3D 加黑邊，改中景；FindLaw 擋連結檢查且沒有 Wayback 存檔，換成 ELR 摘要；背景長串跑到一半遇到系統 fork 失敗會留下過期的專案鎖，重跑即可。
- 2026-10-10 20:0xZ：H01 上架包 4／4、上架確認自動核准，`upload/UPLOAD.md` 給站主上傳用；YouTube 上傳是站主的事。第二集 U02 還沒開始，claim 已釋出，接手的人照同一條流程（研究代理 → brief → 撰稿 → 兩輪查核 → tts → keyframes → render → assemble → captions → qa → 四個關卡）。
- 2026-10-10 H01 做到的（claude-fable-curio）：旁白 105 句 11:33（2,826 字）、插圖 75 張 MiniMax image-01（136 次生成含 judge，US$2.04）、照片 6 張、成片 20,922 格（11:37）、繁中 CC 118 cues；大綱（Jev 選 A）與旁白關卡自動核准；品管 9／11 → 旁白重送後應為 10／11，剩 `policy` 的「有示範」0.16（教學規則，見票 `2026-10-10-policy-demo-exempts-explainer-slides`），所以成片關卡與分鏡關卡（站上投影片分鏡沒開自動核准）都在 `/admin/videos` 等站主按核准；核准後再 `package` → `review-push --gate publish`。
- 這集學到的：MiniMax 把表情貼到物件上（帳篷、枕頭、艙蓋、繩結、帽子裡長出頭）——空景一律改成「一個人在做一件事」；三次都沒過的 11 張全是這類或 3D 漂移，改寫後 12／12 一次過；`table` 卡 6 列要用短詞、不放 `source`；結尾卡只能留一句（8 秒節奏）；旁白實際比 lint 估計長約 5%（11.0 → 11.5）；旁白檢查第一輪 5 句（小艇／測深桿／海怪／主艙口／日誌記五日）改字後全過；Smithsonian 與 Britannica 擋程式讀取，來源連結改 Wayback 快照才過連結檢查。
- 2026-10-10 進度（claude-fable-curio）：H01 `curio-h01` 以插圖投影片路線在本機做。研究代理寫 `research.md`（11 節、每條附來源）；站主同意後下載六張維基共享公有領域檔到 `photos/`（站上 Pexels／Pixabay 金鑰未設，`stock search` 不能用）；撰稿 97 景／118 句／lint 11.0 分；大綱關卡 Jev 挑 A 自動核准；查核兩輪（第一輪改 8 個事實、第二輪改 2 個，加了 Austin 勘驗與 Patron 化驗兩份一手文件當來源）；熱飯菜傳說的最早出處仍查不到，稿子改成不講先後，brief 裡「十二年後小說加的」那句與來源不符（brief 綁大綱雜湊不能改）。插圖 74 張 MiniMax image-01 一輪約 US$1；站主指示「查核完直接合成旁白，做到上架確認」。

- 2026-10-10 開票。樣張 16 張（四種畫風 × 四個場景）畫在 `mokaair-work/videos/_audition/look-20261010-curio/`，約 US$0.22。
- 含金量六條（規矩 11）是教學投影片的規則，這個系列是說書，不套；8 分鐘下限照常。
- 主機的解說路線還吃不了這個系列的畫風與 MiniMax，所以先本機做；主機路線的改法在 `2026-10-10-explainer-route-takes-a-series-look`。
