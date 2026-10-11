---
name: add-converter
description: 在 src/units.mjs 新增一個單位換算函式。
when_to_use: 使用者要加新的單位換算、新的換算函式時。
---

# 新增換算函式

只動 src/units.mjs 和 CHANGELOG.md。

1. 函式加在 src/units.mjs 的最後面，名稱用 aToB 的寫法
   （例如 kgToLb），寫成 export function。
2. 結果四捨五入到小數點後兩位，寫法照 kmToMiles。
3. 不加相依套件，不新增檔案。
4. CHANGELOG.md：在「## Unreleased」底下加一行
   「- [feat] Add 函式名稱.」。
5. 回覆的最後一行固定寫：下一步：補一個測試
