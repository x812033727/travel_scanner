---
id: 2026-10-10-history-curiosity-pilot
title: 歷史與奇異：站主選畫風與前三題後，本機做兩集試片並記實測
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-10T16:20:00Z
completed_at:
branch:
depends_on:
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

- [ ] 站主在 `README.md` §選定紀錄 填了系列名、畫風（A／B／C／D）、歷史人物能不能畫成卡通、前三題；沒填的先用企劃的提案並註明。
- [ ] 兩集做完（建議 H01 瑪麗賽勒斯特號、U02 51 區）：`brief.md`、`video.json`（`format: "slides"`、`category: "explainer"`、選定的 `look`、`shot` 與卡片交錯、至少 3 張登記在 `assets[]` 的公有領域或圖庫照片）、`claims.md`、兩輪獨立查核、旁白（Whisper 第二轉寫）、`keyframes`（`--dry-run` 印出 `minimax image-01`）、`render`、`assemble`、`captions`、`qa` 11 項、`package`、`review-push` 到上架確認。
- [ ] 每集記在 `docs/videos/curio-<id>/production-record.md`：插圖張數與重做次數、照片張數與來源、媒體花費、審圖分數分布、旁白長度與成片長度、站主審片分鐘數。
- [ ] `README.md` §成本與產能 改成實測；`topics.json` 做過的題改 `scripted`／`published`，查核過的事實回寫 `facts_to_verify` 的結果。

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

- 2026-10-10 開票。樣張 16 張（四種畫風 × 四個場景）畫在 `mokaair-work/videos/_audition/look-20261010-curio/`，約 US$0.22。
- 含金量六條（規矩 11）是教學投影片的規則，這個系列是說書，不套；8 分鐘下限照常。
- 主機的解說路線還吃不了這個系列的畫風與 MiniMax，所以先本機做；主機路線的改法在 `2026-10-10-explainer-route-takes-a-series-look`。
