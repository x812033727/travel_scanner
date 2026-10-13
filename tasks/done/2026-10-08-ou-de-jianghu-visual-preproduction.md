---
id: 2026-10-08-ou-de-jianghu-visual-preproduction
title: 《偶的江湖》補齊角色美術前期規格與任務鏈
status: done
priority: P1
area: docs
owner: codex-ou-de-jianghu-art
claimed_at: 2026-10-08T10:47:09Z
created_at: 2026-10-08T10:47:02Z
completed_at: 2026-10-08T10:59:08Z
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on: []
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development
---

# 《偶的江湖》補齊角色美術前期規格與任務鏈

## Why

站主要《偶的江湖》先建立角色造型與畫像，讓後續動畫沿用固定人物；本輪明確選擇「先補齊任務、造型規格與畫像製作清單」。既有劇本及試播票缺少獨立美術資產任務，需沿正典補出可執行清單，不能把文字規格當成已生成圖片。

## Definition of done

- [x] 整理24位角色聯集、第一集9人、共用cast19人與16種命名造型的來源、輪廓／配色／身份錨點、時態與防劇透規格。
- [x] 完成畫像、多視圖、表情、姿態、局部／道具參照的用途、分批、驗收與來源SHA清冊，全部圖片狀態保留待製作。
- [x] 建立8張有scope、依賴、完成條件、驗證及交接的待辦，覆蓋前置包、定調、畫像、動畫參照、後續造型、場景道具、外部圖匯入與試播交接。
- [x] 完成任務／來源／連結驗證及獨立審查；不修改其他持有人的試播、第8集劇本或production來源。

## Steps

- [x] 核讀matching skills、現有任務、分支／worktree／遠端／PR及正典，不重開既有劇本或試播。
- [x] 以專用 visual-development 子目錄保存總覽、造型規格、製作清單與source-bound inventory；新增後續待辦。
- [x] 完成review與驗證，保存可審閱交付。

## How to verify

- `npm run check:tasks`
- `node docs/videos/series-plans/ou-de-jianghu/build.mjs --check`
- `node docs/videos/series-plans/ou-de-jianghu/validate.mjs`
- 核對 inventory 的24個唯一ID、19個production角色、9個首集角色、16個命名造型、12份來源SHA與JSON pointers；檢查新增Markdown相對連結。
- `git diff --check`；獨立代理對照cast／setting與現有集鏡審閱。

## Notes

- 2026-10-08：使用者明確只要求本輪補任務、規格、清單；沒有生成／核准／匯入媒體，沒有正式站操作或新增付款。
- 成果入口：[visual-development/README.md](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)。20位setting人物與19位cast去重後共24位；cast多4名配角，setting還有5位未進cast。第一季23位，褚無常正臉在第二季，第一集黑風獨立列效果。
- 現有look無PNG匯入，shot_looks僅文字覆寫、keyframes用基底圖，已開外部匯入能力票；不手寫runtime manifest或approval。
- production README仍寫14人，後續交接票修正；本輪未修改既有已claim票的depends_on，不能宣稱已機械阻擋試播。第8集及傳單知情票維持原責任。
- 驗證：check:tasks通過（只有5張既有過期claim警告）；原企劃build --check、validate、16項validate.test通過；24/19/9/16清冊、12份來源SHA、JSON pointers、55個新增文件本機連結通過。獨立review逐項核對角色使用鏡數／首末鏡、來源及依賴，無阻擋問題。
- 本票done只代表前期文件與8張待辦補齊；8張製作／整合票仍open，圖像與動畫仍未製作。
