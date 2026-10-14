---
id: 2026-10-14-zero-root-yaozu-village-a-ten
title: Zero-root Yaozu village: a ten-season, 600-episode live-action xianxia drama plan for Hailuo
status: done
priority: P2
area: docs
owner: claude-opus-5-5-yaozu-plan
claimed_at: 2026-10-14T17:04:07Z
created_at: 2026-10-14T17:03:57Z
completed_at: 2026-10-14T23:24:58Z
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zero-root-yaozu
---

# Zero-root Yaozu village: a ten-season, 600-episode live-action xianxia drama plan for Hailuo

## Why

站主 2026-10-14 要一部能衝流量的真人修仙短劇：海螺製作、一集 50–180 秒、每集有鉤子、一季至少 60 集、規劃 10 季，取材排行榜十七部作品，但故事要連貫、看得懂。調性要狗血、狠辣、感人、恐怖、科幻炫技、特效，要有美女帥哥與身材，但不能被黃標。直接改編榜單作品會侵權，所以做成融合套路的原創長篇。

## Definition of done

- [x] 設定集、十季總綱、製作規格、寫法規則、檢查與產生腳本在 docs/videos/series-plans/zero-root-yaozu/。
- [x] season-01～10.json 共 600 集，validate.mjs 0 問題，build.mjs --check 通過。
- [x] 跨季連貫審查做完並修正。

## Steps

- [x] setting.json、outline.json、plan.json、authoring.md、validate.mjs、build.mjs、README.md
- [x] 十個子代理各寫一季
- [x] 全劇 validate、跨季接點審查、build

## How to verify

```bash
node docs/videos/series-plans/zero-root-yaozu/validate.mjs
node docs/videos/series-plans/zero-root-yaozu/build.mjs --check
```

## Notes

- 站主追加的規則：每集三個鉤子（開頭 3 秒、中段、結尾）；「讓人想繼續看的厲害之處就是每集收的點」→ cliffhanger 要收在最高點、多寫觀眾帶走的問題；60 集是保底，可以擴充（README 擴充點）。
- 榜單片名不進 repo，只寫套路。
- 季是平行寫的，所以季界用規則固定：每季最後一集收反轉、第一集不收反轉、季末主角不受挫。
- 跨季審查（三個審稿代理，各管三到四季）修了 60→61 以外的每個季界：120→121（北門）、180→181（後山滑落）、240→241（兩個審稿人反方向改撞，主代理統一成傍晚望仙鎮、大典前兩天）、300→301、360→361、480→481；並修了斷龍原是雷柱不是金曜、鯤在第八季後沉睡、雲知意第 600 集是「第一次以家人身分上桌」、狐毛每次的來源、白無咎化光在 538 集。
- 跨季重複的客串角色升到 setting.characters（柳嫂、老黃、阿杏、石大郎）；同名不同人的改名（第四季韓九、霍嶸，第十季林沁）。
- 還沒回收：夔、九嬰、相柳只在第三季出現。
- 等站主：直式或橫式、角色聲音、預算（建議先拍第一季第一篇章 10 集）、作品名。
