---
id: 2026-10-10-sothatswhy-minimax-images
title: 原來如此事務所：插圖改由 MiniMax 生成，畫風改成可愛卡通家族
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
  - docs/videos/so-thats-why/README.md
  - docs/videos/so-thats-why/look.md
  - docs/videos/so-thats-why/operations.md
---

# 原來如此事務所：插圖改由 MiniMax 生成，畫風改成可愛卡通家族

## Why

站主 2026-10-10 決定：「原來如此系列之後也改成這樣用 MiniMax 產生圖」，不用 Claude 或 Codex 產生。第二季已做的 T26、T27 是 Claude／Codex 手繪的原創 SVG（`docs/videos/sothatswhy-t26/vector-art/` 157 張、T27 130 張），之後的集數不再這樣做。README 與 look.md 2026-10-10 已記下決定與對照表，但畫風的最終文字、片頭三張圖、每日工作流裡「插圖」那一步還是舊寫法。

## Definition of done

- [ ] 站主從 `docs/videos/history-curiosity/look.md` 的候選裡選了原來如此用的畫風（提案 A 大頭卡通或 B 軟繪本），`look.md` 的 `look` JSON 改成選定的 `style` 加色盤句、`negative: ""`，並記 `look_hash`。
- [ ] 片頭三張關鍵影格（門、信、蓋章）用 MiniMax 重畫一次，`look.md` §選定紀錄 填檔名與 SHA-256。
- [ ] `operations.md` 的 D−2「關鍵影格」一列改寫成 MiniMax 的做法（`keyframes --dry-run` 必須印出 `minimax image-01`；每月張數上限在後台漫劇分頁）。
- [ ] 下一集（第二季順序提案的下一個，或站主指定）用新做法做完一集並記實測，README §成本與產能 的插圖一列改成實測。
- [ ] 主機解說路線（`flat-explainer`）指定 MiniMax 的改法不在這張票：那是 `2026-10-10-explainer-route-takes-a-series-look`。

## Steps

- [ ] claim 前 `gh pr list` 看有沒有別的 session 在改 so-thats-why 的文件。
- [ ] 站主選畫風；把候選文字加「warm cream paper ground, ink navy, stamp red only on the answer, mustard yellow」那一句，`keyframes --dry-run` 看 prompt budget 沒超。
- [ ] 借站上已有的 slides slug 畫片頭三張與 4 張章節場景樣張（`keyframes --file <copy>/video.json --workdir <dir> --shot … --takes 1`），站主看過再定。
- [ ] 改三份文件；做一集。

## How to verify

`look.md` 的 JSON 可解析、`negative` 是空字串；片頭三張的 SHA-256 與 repo 外檔案一致；新做的那集 `status --slug` 到上架確認、`keyframes/manifest.json` 的模型是 `image-01`。

## Notes

- 2026-10-10 開票。T26、T27 已完成的成片不重做。
- MiniMax 不吃畫風樣張與 negative，一致性全靠 `look.style` 文字：見 `docs/videos/history-curiosity/look.md` §MiniMax 的事實。
