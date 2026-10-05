---
id: 2026-10-04-ou-de-jianghu-e002-e005-scripts
title: 《偶的江湖》第 2–5 集劇本：鯨背嶼、三十六魂、裂山秘錄、封功（22 分鐘長篇動畫）
status: done
priority: P2
area: docs
owner: claude
claimed_at: 2026-10-04T23:34:11Z
created_at: 2026-10-04T23:34:07Z
completed_at: 2026-10-05T12:17:34Z
branch: claude/vibrant-cray-mdpjzx
depends_on: []
scope:
  - docs/videos/ou-de-jianghu-e002
  - docs/videos/ou-de-jianghu-e003
  - docs/videos/ou-de-jianghu-e004
  - docs/videos/ou-de-jianghu-e005
  - docs/videos/series-plans/ou-de-jianghu
---

# 《偶的江湖》第 2–5 集劇本：鯨背嶼、三十六魂、裂山秘錄、封功（22 分鐘長篇動畫）

## Why

站主要接著第 1 集〈幽皇之女〉（`docs/videos/ou-de-jianghu-e001/`），把第一季第 2–5 集的 22 分鐘劇本寫出來，照企劃包 `docs/videos/series-plans/ou-de-jianghu/season-01.json` 的細綱。四集要和第 1 集已寫出的台詞、道具、角色外觀連得上，同一角色在每一集的角色檔逐字相同（設定圖共用）。

## Definition of done

- [x] `docs/videos/ou-de-jianghu-e00{2,3,4,5}/` 各有 `video.json`、`series.json`、`script.md`、`brief.md`、`review.md`；long-anime-v1，正文估算約 1,404 秒。
- [x] 每集 lint 0 錯誤、`drama_craft_check.mjs` 全達標、`shot_reading.mjs` 0 陷阱；`script.md` 與 `video.json` 一致。
- [x] 四集的懸念類型照細綱（reveal、choice、reversal、emotion），兩段高張力在對的半場；跨集連戲（時間線、人物位置、物證流向、誰知道什麼）經獨立審稿。
- [x] 同一角色在第 1–5 集的角色物件逐字相同；新角色與詩號列在各集 `brief.md` 等站主核定；原作名稱掃描 0 筆。

## Steps

- [x] 1. 企劃包殘留舊名：`setting.json` 竹虛外觀的「red maple iron」、派系 id `youdu-qisha`；重建並驗證企劃包。
- [x] 2. 全系列角色表（新角色、`shot_looks`、暫定聲音），第 1 集同步（姬無霜基本外觀拿掉手背印記）。
- [x] 3. 四集分場表：撰寫、連戲審與戲劇審、修訂、跨集審。
- [x] 4. 二十幕分鏡：每幕自我檢查，每集整集審與修。
- [x] 5. 合併、`script.md`、最後對抗審稿、`brief.md` 與 `review.md`。

## How to verify

```bash
for n in 2 3 4 5; do
  s=ou-de-jianghu-e00$n
  node tools/video/cli.mjs lint --slug $s
  node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/$s/video.json
  node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/$s/video.json
done
D=docs/videos/series-plans/ou-de-jianghu
node $D/build.mjs --check && node $D/validate.mjs && node --test $D/validate.test.mjs
npm run check:tasks
```

## Notes

- 做法沿用第 1 集：分場表 → 每集五幕各一個代理 → 合併檢查 → 讀全集台詞修連戲。工作檔（角色表、分場表、各幕、檢查與合併腳本、審稿意見）在 `docs/videos/series-plans/ou-de-jianghu/production/`，README 寫了怎麼改某一集、怎麼寫下一集。
- 第 1 集的角色檔變動（姬無霜基本外觀、`shot_looks`、金印形狀）屬試播票 `2026-10-04-clip-route-pilot-comparison` 的 scope，記在那張票。
- 2026-10-05 角色表：14 人（第 1 集九人，加竹虛 zhuxu、柳不活 liu-buhuo、書院長老 shuyuan-elder、玄門執事長老 xuanmen-steward、客院盟兵 alliance-guard），新角色聲音暫定 Umbriel、Enceladus、Orus、Charon、Sadachbia；`shot_looks` 管狀態變化（寂聞中箭／封功、姬無霜背弓、柳不活受傷／投敵、竹虛回程、包三錢落海、殷無聲斷髮、聶孤鐵釘傷）。姬無霜基本外觀拿掉手背印記，第 2 集起兩道印只寫在插鏡 prompt。
- 2026-10-05 分場表四份各經連戲審、戲劇審、修訂與跨集審。主編定案：旁白一律用相對時間，不報「第幾日」；第 1 集名句（「你知道的，我都要知道」「瞞得過一天，是一天」「幽都殺人，用不著走門」）不在後面的集數逐字重用，前者只留給第 5 集寂聞「你做到了嗎？」；島底陣上的符一律說「盟符」，不說「三宗的符」（避免跟她手背的三宗印混淆）；物證（斷弦、鐵釘、拓片、備用封條）收在沈歸鶴書齋案的抽屜；押差官改押解官、萬教通緝改九洲通緝（企劃包已同步）。
- 2026-10-05 站主決定：燕迴的外號由「斷浪」改成「赤纓」（取自他刀上的紅刀穗；「斷浪」與漫畫《風雲》的主要角色同名）。企劃包、路線圖人名表（含後面時代的招式「斷浪八式」→「赤纓八式」）、全系列角色表與第 1 集都已改。
- 2026-10-05 雲端 session 額度用盡前備份：第 2、3 集五幕寫完，第 4 集 a01–a03，第 5 集未開寫（PR #1213 只含到第 1 集劇本的快照；之後的 commit 留在分支上）。
- 2026-10-05 本機 session 接手（同一條分支）：
  - 合併 `origin/main` 時 13 個檔案是 add/add 衝突（main 上是 #1213 的舊快照），全部取分支版本。
  - 製作腳本改成從自己的位置找 repo、動態 import 用 file URL（Windows 才跑得動）、每幕各自的 `tmp-<label>/` 暫存（五幕平行檢查不互相覆蓋）、`dialogue.py` 指定 UTF-8。
  - 第 4 集 a04、a05 與第 5 集 a01–a05 各由一個代理寫成並過單幕檢查（每幕 272–292 秒）。四集各一位整集審（`epN/review-findings.json`：第 2 集 2 major 9 minor、第 3 集 8 minor、第 4 集 7 minor、第 5 集 7 minor）、一位修訂、一位對抗驗收；第 3 集與第 5 集各多一輪（`review-findings-2.json`）。
  - 跨集連戲審三個鏡頭（時間線與位置、物證與知情、台詞與口吻）提 7 條，每條兩位反駁人；成立 2 條並已修：第 2 集 a05-s054、s055 的兩道印補上形狀定句（a slanted brush stroke and a small curling cloud hook），第 5 集 a03-s050、s052、s055 的書齋抽屜移到書案右端（照第 3 集 a01-s073）。被反駁的 5 條：第 4 集冷開場傳單（燕迴在 a01-s015 自己撕了一張）、第 3 集「第一次下山入座」（必留句且不矛盾）、第 5 集防務令上的盟印（第 4 集已把盟印小匣交到書院長老手邊）、第 5 集執事改口「玄門長老」（第 4 集死訊揭穿後他自己就改口了）、「X，比人老實」句式（第 4 集那句是柳不活與姬無霜自己的線）。
  - 主控裁定：(1) 第 5 集定格鏡 a01-s027 維持 `slow push in`（分場表第五節寫 locked；`shot_reading.mjs` 把 still＋locked 判成陷阱，第 1 集三個詩號定格也都是 slow push in）。(2) 第 5 集前情 a01-s010「通緝暫緩，人押在玄門。」視為第 4 集交接要求「九洲通緝，」「暫緩。」的等價句，不改（第 4 集分場表第十一節已記）。(3) 第 5 集的「二十一天」、三集的青瓷藥瓶、cast-notes 的 look 表都已核過一致。(4) 第 1 集 a03-s054、a03-s087 的一道印補成「one faint gold seal mark, a slanted brush stroke」，與第 2–5 集同一套形狀。
  - 原作名稱掃描：站主的 1,011 筆私人對照表不在本機，改用本機重建的 607 筆（霹靂、金光與東離的人名、門派、境界、招式、兵器、劇名、公司與人名、詩號首句，只在 session scratchpad，不進 repo）掃四集的 `video.json`、`series.json`、`script.md`、`brief.md`、`review.md` 與製作檔：0 筆（「白金光」「無名劍客」兩個子字串誤報不算；後者來自企劃包第 6 集 logline，main 上已有）。站主若要用原本那份表再掃一次，檔案清單在各集 `review.md`。
  - 縮圖鏡：第 4 集 a05-s004（headline「見者可殺」）、第 5 集 a01-s027（定格鏡，headline「怒目佛封功」）；第 2、3 集沿用 a01-s005、a01-s013。
  - 片長：四集估算 1,393.7／1,404.6／1,400.0／1,404.5 秒，刻意高於 1,380 秒（lint 用每分 250 字估，實際配音約 300 字）；各集 `review.md` 有語速換算表與太長時的刪減順序。
- 還沒有答案、留給企劃包擁有者：第 4 集 a01 沈歸鶴點出「寫傳單的人怎麼比玄門先知道秘錄不見」，本集沒有人答；要向企劃包確認第 8 集細作的答案（例如第 1 集當夜玄門長老身上那把經閣鑰匙的下落），寫進第 8 集的交接。`season-01.json` 第 8 集的 state 目前只寫「傳單紙的筆跡比對」與「兩名被收買的客院盟兵」。
- 等站主核定（各集 `brief.md` 最上面）：名台詞等價句、四個新角色與說書人以外的暫定聲音（Umbriel、Enceladus、Orus、Charon、Sadachbia）、第 5 集招式名「千重自封」；核定前不要跑 TTS。劇本關卡要後台先建原生長篇動畫作品與各集集數列（見試播票）。
