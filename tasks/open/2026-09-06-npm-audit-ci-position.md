---
id: 2026-09-06-npm-audit-ci-position
title: npm audit 排在 CI 前段，網路不穩就擋掉整輪
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-06T00:53:24Z
completed_at:
branch:
depends_on:
  - 2026-09-06-required-checks-block-merge
scope:
  - .github/workflows/ci.yml
---

# npm audit 排在 CI 前段，網路不穩就擋掉整輪

## Why

`.github/workflows/ci.yml` 的 web job 順序是：

```
47:  npm audit --audit-level=high
49:  npm run lint:web
53:  npm run test:web
54:  npm run test:tools
```

`npm audit` 要打 registry。它 503 或逾時的時候，整個 web job 直接紅，
**lint 與測試根本沒跑**，開發者看到的是一個和自己的改動完全無關的失敗。
2026-09-04 一天內就擋掉六次。

安全稽核本身該留著，但它不該是決定「我的程式碼有沒有壞」的那一關。

## Definition of done

- [ ] registry 暫時不可用時，lint 與測試仍會跑完並回報真實結果。
- [ ] 稽核失敗仍然看得見（不是靜靜吞掉）。
- [ ] 一次真實 CI 跑過確認順序生效。

## Steps

- [ ] 三選一（建議由上到下）：
  - [ ] 把 `npm audit` 移到 lint／test **之後**；
  - [ ] 或拆成獨立 job，與 web job 平行，失敗不擋合併（`continue-on-error: true` + 
        用 job summary 呈現）；
  - [ ] 或加 `--registry` 重試包裝，只在連續失敗才紅。
- [ ] 若採 `continue-on-error`，要確認結果在 PR 上仍看得到，不要變成沒人看的綠。

## How to verify

改完推一個測試分支，看 web job 的步驟順序；再故意把 registry 指到不存在的 host
（`npm audit --registry=https://127.0.0.1:1`）確認 lint／test 還是跑完。

## Notes

這是 2026-09-04～09-06 一連串 UX PR（#148、#150、#156、#158、#160、#161、#173、#174、#175、#177）
期間反覆遇到的摩擦，不是新發現的問題，只是一直沒有人動它。

同一個 job 裡 `npm run test:web` 是最慢的一步（約 4–5 分鐘），
所以把 audit 移到後面不會拖慢回饋，反而讓失敗更早出現在真正相關的步驟上。

**Scope 重疊**：`.github/workflows/ci.yml` 也在 `2026-09-06-required-checks-block-merge` 的 scope （`.github`）底下，而且那張是 P1。先讓它改完必要檢查的設定，這張再調步驟順序。
