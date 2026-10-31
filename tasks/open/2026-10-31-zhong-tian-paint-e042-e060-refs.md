---
id: 2026-10-31-zhong-tian-paint-e042-e060-refs
title: Zhong-tian: paint the 25 portraits and set pictures e042-e060 need, and audition the shared voices
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-31T10:49:51Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-dh
  - docs/videos/series-plans/zhong-tian-qu-qi/production/assets/SHA256SUMS
  - docs/videos/series-plans/zhong-tian-qu-qi/production/assets/README.md
---

# Zhong-tian: paint the 25 portraits and set pictures e042-e060 need, and audition the shared voices

## Why

e041-e060 are written (PR #1955); 25 Ref2VA reference pictures do not exist yet, so most shots of e042-e060 cannot be
made. The list per episode, with which shots each picture blocks, is
docs/videos/series-plans/zhong-tian-qu-qi/production/s01-e043-e060-registry.md (plus e042's four from the
e041-e042 ticket).

## Definition of done

- [ ] 10 portraits: xudalang, zhouyuanwai, chengshanzhang, fengxuezheng, weixun, dutie, chuzhifu, dengyasi, lengtie,
      changgonggong (`refs-dh/<id>-portrait-t1.png`, the 3D donghua look of the existing portraits, appearance from
      production/cast.json).
- [ ] 15 sets: zhou-kezhan, gongyuan, shuyuan-zhai, haoshe, mifeng-fang, bangfang, jiusi, zhou-jie, zhoufu-tang,
      zhoufu-houtang, zhou-kezhan-yuan, beidu-qiantan, hetan, liaowangtai, cundao (`refs-dh/set-<id>-t1.png`).
- [ ] Each added to assets/refs-dh, SHA256SUMS recomputed, its source written in assets/README.md, committed the same day.
- [ ] Owner auditions the shared voices of the 8 new characters (registry lists them) before their first dub.

## How to verify

`ref2manifest.mjs` for each of e042-e060 reports no missing picture; `cd production/assets && sha256sum -c SHA256SUMS`.

## Notes

- Paint e043's six first (chengshanzhang, fengxuezheng, weixun, shuyuan-zhai, haoshe, mifeng-fang), then zhou-kezhan
  (e044, e045, e050-e052).
