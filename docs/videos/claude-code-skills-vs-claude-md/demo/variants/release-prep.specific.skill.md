---
name: release-prep
description: 準備發版：改版號、CHANGELOG、README，寫發版單。
when_to_use: 使用者說某一版要出了、要出新版、要 bump 版號時。
---

# 發版準備

版號用使用者指定的那一版，下面寫成 X.Y.Z。
只動下面列的檔案，不改 src/。五步照順序做完。

1. package.json：version 改成 X.Y.Z。
2. CHANGELOG.md：在「## Unreleased」下面加一個標題
   「## vX.Y.Z (YYYY-MM-DD)」，日期用今天；把 Unreleased
   底下的項目搬到新標題底下。Unreleased 標題留著。
3. README.md：「Latest release:」那一行改成 vX.Y.Z。
4. 新增 releases/vX.Y.Z.md：照 [template.md](template.md)
   的三個標題寫，標題一個字都不要改。
5. 回覆的最後一行固定寫：下一步：git tag vX.Y.Z
