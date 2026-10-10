---
id: 2026-10-10-sothatswhy-minimax-images
title: 原來如此事務所：插圖改由 MiniMax 生成，畫風改成可愛卡通家族
status: in-progress
priority: P2
area: docs
owner: claude-opus-stw-minimax
claimed_at: 2026-10-10T12:52:22Z
created_at: 2026-10-10T16:20:00Z
completed_at:
branch: claude/sothatswhy-b26
depends_on: []
scope:
  - docs/videos/so-thats-why/README.md
  - docs/videos/so-thats-why/look.md
  - docs/videos/so-thats-why/operations.md
  - docs/videos/sothatswhy-b26/
---

# 原來如此事務所：插圖改由 MiniMax 生成，畫風改成可愛卡通家族

## Why

站主 2026-10-10 決定：「原來如此系列之後也改成這樣用 MiniMax 產生圖」，不用 Claude 或 Codex 產生。第二季已做的 T26、T27 是 Claude／Codex 手繪的原創 SVG（`docs/videos/sothatswhy-t26/vector-art/` 157 張、T27 130 張），之後的集數不再這樣做。README 與 look.md 2026-10-10 已記下決定與對照表，但畫風的最終文字、片頭三張圖、每日工作流裡「插圖」那一步還是舊寫法。

## Definition of done

- [x] 站主 2026-10-10 選了 A 大頭卡通；`look.md` 的 `look` JSON 已改成 A 的文字加色盤句、`negative: ""`。
- [x] 借站上的 slides slug 用這個 `look` 畫 4 張超市場景樣張（2026-10-10，`mokaair-work/videos/_audition/look-20261010-curio/stw-a/`）：4／4 一次過、各 9.29，色盤句沒讓畫風漂；`look_hash` `a5910f9c047dbeff`。
- [x] 片頭不重畫：站主 2026-10-02 已核准系列的 6.9 秒片頭（`docs/videos/branding-release/2026-10-02-sothatswhy-intro-approval.md`，bookends `mokaair-sothatswhy-bookends-v1`），`look.md` 2026-09-28 的三張關鍵影格片頭已被它取代；新做法的集數沿用核准的片頭。
- [x] `operations.md` 的 D−2「關鍵影格」一列改寫成 MiniMax 的做法（`keyframes --dry-run` 必須印出 `minimax image-01`；每月張數上限在後台漫劇分頁）。
- [ ] 下一集（第二季順序提案的下一個，或站主指定）用新做法做完一集並記實測，README §成本與產能 的插圖一列改成實測。
- [ ] 主機解說路線（`flat-explainer`）指定 MiniMax 的改法不在這張票：那是 `2026-10-10-explainer-route-takes-a-series-look`。

## Steps

- [ ] claim 前 `gh pr list` 看有沒有別的 session 在改 so-thats-why 的文件。
- [x] 站主選了 A；色盤句已併進 `look.md` 的 JSON。`keyframes --dry-run` 看 prompt budget 沒超。
- [ ] 借站上已有的 slides slug 畫片頭三張與 4 張章節場景樣張（`keyframes --file <copy>/video.json --workdir <dir> --shot … --takes 1`），站主看過再定。
- [ ] 改三份文件；做一集。

## How to verify

`look.md` 的 JSON 可解析、`negative` 是空字串；片頭三張的 SHA-256 與 repo 外檔案一致；新做的那集 `status --slug` 到上架確認、`keyframes/manifest.json` 的模型是 `image-01`。

## Notes

- 2026-10-10 B26 稿子（claude-opus-stw-minimax）：`docs/videos/sothatswhy-b26/`。brief A 案「兩條路線，一個冷藏櫃」→ 撰稿 132 景（插圖 116、卡片 16）／144 句 → 獨立查核一輪：47 列主張確認 38、事實改 3 處（「一共有三件事」→「我分成三件事來說」、「有三個人提到」→「列出三個人的說法」、來源欄不寫公關的雇用關係），未超過三處所以沒有第二輪 → 開拍前預檢：改寫 52 句容易被聽錯的旁白（單字詞、句首兩字詞、「了」結尾、被吃掉的虛詞）、54 個插圖提示詞（25 個只補 plain／blank，29 個改內容），插圖占估計片長 82.5%、最長畫面狀態 6.6 秒。lint 0 錯，估 11.5 分鐘（合成後約 12 分鐘）。來源四個網址當天都回 200；S1 用查核包記的 NPR Illinois 入口（NCPR 原入口 403）。
- 大綱關卡 2026-10-10 送出：Jev 挑 A（1.00），但「有示範 0.33」低於 0.6 沒自動過，等站主在 `/admin/videos` 選。PR #1424 只讓成片的 `policy` 不問解說類影片「有示範」，大綱挑選（`judge_outline`／`outline_pick_passed`）還是每支都問；另開票 `2026-10-10-outline-pick-demo-exempts-explainers`。
- 系列片頭：投影片格式拿不到系列片頭（見上一則），這次在第一次 `assemble` 前把 `_branding/series/sothatswhy/current.json` 的選擇用 `pinBranding` 寫進 B26 的工作目錄（`branding.json`，`mokaair-sothatswhy-bookends-v1`，357＋90 格），`selectBrandingForBuild` 會先讀這個 pin。
- 2026-10-10（claude-opus-stw-minimax）：下一集選第二季順序提案的第一個 B26〈為什麼超市常把牛奶放在最裡面？〉（T26、T27 已做）。本機插圖投影片路線（`format: "slides"`、`shot` 由 MiniMax image-01 畫、卡片放對照與步驟），稿子只用 `season2/B26.md` 製作包裡標為可用的主張。企劃、撰稿、兩輪查核與開拍前預檢由一個 workflow 串起來跑；預檢是這次新加的一步（先把會被聽錯的單字詞與 MiniMax 畫不好的提示詞改掉，再花錢）。
- 片頭的坑：`tools/video/core/branding.mjs` 的 `readDefaultBranding` 只在 `isExplainer(doc)`（漫劇格式＋`flat-explainer`）時選系列片頭；投影片格式的原來如此（T27、這次的 B26）拿到的是全頻道片頭，T27 當時是用 `--adopt-branding` 加一個只含本集的 work base 才換成系列片頭。主機解說路線那張票（`2026-10-10-explainer-route-takes-a-series-look`）加新畫風預設時要一起處理：`cute-cartoon` 與 `sothatswhy-` 開頭的投影片應選系列片頭，`cute-mystery`（奇聞檔案局）不能選到。

- 2026-10-10 開票。T26、T27 已完成的成片不重做。
- MiniMax 不吃畫風樣張與 negative，一致性全靠 `look.style` 文字：見 `docs/videos/history-curiosity/look.md` §MiniMax 的事實。
