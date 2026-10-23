---
id: 2026-10-23-write-c20-zippo-source-bound-script
title: Write C20 Zippo source-bound script and visual plan
status: done
priority: P1
area: docs
owner: codex-root-c20-script
claimed_at: 2026-10-23T05:00:28Z
created_at: 2026-10-23T04:58:21Z
completed_at: 2026-10-23T05:13:29Z
branch: codex/brand-story-zippo-c20-script
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/script.md
  - docs/videos/story-everyday-zippo-c20/script-source-notes.md
  - docs/videos/story-everyday-zippo-c20/visual-plan.md
  - docs/videos/story-everyday-zippo-c20/visual-plan.json
  - docs/videos/story-everyday-zippo-c20/reviews/author-script-receipt.md
---

# Write C20 Zippo source-bound script and visual plan

## Why

C20 Zippo 的六章企劃與 M01–M13 來源矩陣已在草稿 PR #1708，獨立 Treatment 覆核在 #1710 PASS；站主在 2026-10-23 採用方向。下一關是把「1933 年商品承諾、早期專利構件、現行英美維修邊界」寫成一條可聽的故事，而不是把企劃核准誤當逐句劇本核准。

## Definition of done

- [x] 六章繁中旁白逐句對應一鏡，含 30–60 秒濃縮開場、既有 5 秒片頭位置、21 秒 v4 片尾位置、故事鉤子與三句結尾。
- [x] 所有可查主張逐句標原件與可說界線，英國內膽／寄件和美國外觀保固分別歸屬；不由產量推保修帶動銷量。
- [x] 插圖預排一律是 MiniMax `image-01` 的原創 `cute-mystery` 概念畫面，與旁白逐句相符；不畫商標、真人、吸菸、火焰操作或冒充史料的圖。
- [x] 只把作者草稿送交獨立來源／配鏡覆核與兩位只讀旁白盲讀；本票不宣稱站主稿件、付費或發布核准，也不以紙上字數取代 TTS 480 秒。

## Steps

- [x] 讀站主採用收據、企劃、矩陣，以及 brand-story、curio-episode、youtube-video 和 task-board 規則。
- [x] 重開公司史、原始專利、英美維修條款、日期碼、Arc 內膽及第六億支原件。
- [x] 起草 `script.md`、逐句 `script-source-notes.md`、`visual-plan.md`、`visual-plan.json`；保持逐句 ID 同序。
- [x] 作者自檢敘事、主張、禁詞、配鏡與結構；記精確 SHA-256 及不足的實測關卡。
- [x] 跑 `npm run check:tasks`、受影響的影片檢查與 `git diff --check`，開獨立 draft PR，貼 `no-auto-merge`。

## How to verify

核對四檔 SHA-256，從 `script.md` 擷取旁白 ID 與 `visual-plan.md`／JSON 的 `line_id` 比對同數同序；所有 `image` 提示詞不得有品牌、可讀字、火焰操作或精確商標形狀。執行 `npm run check:tasks`、`git diff --check`。稿件到 PR 後由**另一代理**逐句重開一手來源、看 paired visual；兩位讀者只看純旁白投影。真正正文時長至少 480 秒與插圖正文時間至少 70% 只能在配音／成片後量。

## Notes

本任務從已採用的 C20 Treatment PR #1708 head `0058e61d0` 分出 `codex/brand-story-zippo-c20-script`。`treatment.md` 首行仍有舊的「待採用」狀態字樣，因站主核准綁定 Treatment 精確雜湊，本票不改它；以 `reviews/owner-treatment-adoption.md` 與 PR body 的採用收據為準。舊版美國維修網址會轉址，內膽替換與保價可追蹤寄件只用仍可讀的英國頁；美國外觀不在終身保固只用美國知識庫。1997 年博物館 Repair Clinic 是本稿新增的公司史 1990s 段主張，須獨立逐句覆核。

2026-10-23 作者文字自檢：68 句／68 鏡、58 插圖／10 後製字卡，無相鄰字卡；開場紙上 55.9 秒，片頭後正文紙上 568.6 秒，均非真實 TTS。`npm run check:tasks` PASS（全板原有提示）；`npm run test:docs-videos` 131 PASS／6 FAIL，失敗均因本工作樹沒有安裝 `pinyin-pro`，與 C20 新增四份企劃稿無關，未因 C 槽僅餘約 174 MB 而安裝依賴。後續照收據要求獨立查核。

2026-10-23 作者草稿已送出 draft PR #1728，基底是已採用企劃分支，PR 文字有 `no-auto-merge`，遠端讀回 `isDraft=true` 且 `autoMergeRequest=null`。作者任務止於送審，獨立查核與站主核稿仍在後續關卡。
