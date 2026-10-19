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

- [x] `docs/videos/curio-s26` 有估 9.0 分鐘劇本、固定來源筆記、逐句事實表、91 張靜圖分鏡。
- [ ] 獨立史料覆核與盲讀故事關卡通過、lint 零錯誤；媒體製作待稿子定案。

## Steps

- [x] 檢查 S26 無其他活躍認領、遠端 PR 或 main 既有落地，建立窄 scope。
- [x] 固定盧梭法文摘錄與完整英譯、Campan 生年／赴法記錄、Karr 1841 與 1843 年文字；標示一手敘述和後來轉述的界線。
- [x] 完成 brief、research、claims、video.json、script.md；獨立史料讀者已完成初次與增量覆核。
- [x] 首次全新盲讀完成 11/13；針對長段落失去懸念、糕點店岔線修稿，見 `verify-3.md`。
- [ ] 新版另交全新盲讀者判 13 題；通過後才能合成語音並進入媒體製作。
- [ ] 跑文件測試、記錄最後交接。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s26`；`node tools/video/cli.mjs narrative --slug curio-s26`；`npm run test:docs-videos`；`npm run check:tasks`。

## Notes

與其他集共用 `codex/curio-s34-endurance-20261019`，本票只改 `docs/videos/curio-s26`。早期原件可讀 GitHub 固定提交：TEI 對《懺悔錄》法文摘錄、GITenberg 完整英譯、Campan 回憶錄、Karr《Les Guêpes》。Karr 1841 年稱名言「真假未定」，1843 年又提其找到一部 1760 年書將話歸給托斯卡納公爵夫人；後者只可稱「Karr 自述」，尚未獨立找到該書。盧梭原文未指名瑪麗；不能把題庫的約 1765 年寫作日期或匿名公主身分寫成已證。

目前劇本 narrative hash `dde47e83cb6c99e1`，92 句、91 張預計靜圖、估 9.0 分鐘；lint 0 錯 0 警告。獨立史料讀者在前稿 `55ac6cdd7b2be9a8` 找出三句歸屬／譯詞錯誤及畫面細節，詳見 `verify-1.md`；後續修正已獨立增量覆核通過，見 `verify-2.md`。第一次全新盲讀於前一稿 `f7f9397ec43f28d1` 得 11/13，源文件重新抓取校驗一致且無史實阻礙；本次依故事意見修訂及作者來源自查見 `verify-3.md`。新 hash 仍待另一位盲讀；**未進行付費媒體製作**。
