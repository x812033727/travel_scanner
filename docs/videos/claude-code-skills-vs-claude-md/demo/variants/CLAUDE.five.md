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

## 記一筆更新紀錄

1. 只改 CHANGELOG.md，其他檔案都不要動。
2. 在「## Unreleased」底下加一行，開頭用 [fix]、[feat]
   或 [docs] 標出種類。
3. 不要新增版本標題，不要搬動已經有的項目。

## 新增換算函式

只動 src/units.mjs 和 CHANGELOG.md。

1. 函式加在 src/units.mjs 的最後面，名稱用 aToB 的寫法
   （例如 kgToLb），寫成 export function。
2. 結果四捨五入到小數點後兩位，寫法照 kmToMiles。
3. 不加相依套件，不新增檔案。
4. CHANGELOG.md：在「## Unreleased」底下加一行
   「- [feat] Add 函式名稱.」。
5. 回覆的最後一行固定寫：下一步：補一個測試

## 處理回報的錯誤

1. 先讀 src/units.mjs 裡出錯的那個函式，讀完再改。
2. 回覆的開頭寫「重現：」，後面接輸入和實際的輸出。
3. 只改出錯的那個函式，其他函式不要順手整理。
4. CHANGELOG.md：在「## Unreleased」底下加一行，
   用「- [fix] 」開頭，寫修了什麼。
5. 版號不要動，README.md 不要動。
6. 回覆的最後一行固定寫：下一步：請回報的人確認

## README 的使用範例

1. 只改 README.md，其他檔案都不要動。
2. 範例放在「## Usage」底下；沒有這個標題，就加在
   「Latest release:」那一行的上面。
3. 每個範例一個程式碼區塊，第一行是 import。
4. 範例裡的數字要真的算過，結果寫在同一行的註解。
5. 「Latest release:」那一行不要動。
