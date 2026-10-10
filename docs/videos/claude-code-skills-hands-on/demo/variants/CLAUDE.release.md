# unit-kit 專案慣例

## 發版準備

版號用使用者指定的那一版，下面寫成 X.Y.Z。
只動下面列的檔案，不改 src/。五步照順序做完。

1. package.json：version 改成 X.Y.Z。
2. CHANGELOG.md：在「## Unreleased」下面加一個標題
   「## vX.Y.Z (YYYY-MM-DD)」，日期用今天；把 Unreleased
   底下的項目搬到新標題底下。Unreleased 標題留著。
3. README.md：「Latest release:」那一行改成 vX.Y.Z。
4. 新增 releases/vX.Y.Z.md：照下面的三個標題寫，
   標題一個字都不要改。
5. 回覆的最後一行固定寫：下一步：git tag vX.Y.Z

發版單的三個標題：

    ## 這一版改了什麼
    ## 升級要注意
    ## 怎麼確認
