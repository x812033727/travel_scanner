# U09 四鏡定向補圖與資料卡退路（2026-10-16）

## 本輪費用與逐圖判定

- 依 [四鏡修圖計畫](keyframes-repair-plan-3.md)只對 `brief-window`、`more-marks`、`line-of-sight`、`beam-away` 跑最多三次 MiniMax image-01 與 Gemini 圖評。共享停手帳本先預留 US$0.1620，實際本機媒體帳本增加 7 張圖／7 次圖評，估算 US$0.0945；預留已核銷。媒體帳本累計 US$3.5235，整集共享估算 US$4.2235／US$6，沒有未結預留。這些是工具估算，不是供應商最終帳單。
- 補圖後舊 `keyframes/manifest.json` SHA-256 為 `27D15BE1122355682178C1289CB0312E89FDF7426B0411DCC9FFE7A327F7A4F7`；`media/ledger.json` SHA-256 為 `88DEBFCD5D00E413BA5389DC545EADED41331B9A1682D87CD7D10BA3DD0F9D3A`，都在 repo 外的 `<home>/mokaair-work/videos/curio-u09/`。逐張看原尺寸後，只接受其中兩張：

| 鏡頭 | 舊 manifest 選圖與 SHA-256 | 結論 |
| --- | --- | --- |
| `brief-window` | `brief-window-2.jpg` `4DA82C766A150DACA8F063D55902A229C8E54954833013EC94482255D65351FC` | take 2 圖評通過，冷機房操作儀器與短暫觀測的旁白相符；原尺寸可用。 |
| `more-marks` | `more-marks-1-trim.jpg` `3ADF83FEE23625D7FC2560B21C8D0F80B2A1FA4B24BDCB2CFE392BBC01F6125C` | 圖評總分 9.29 且標 `passed`，但評語明載紙帶空白、沒有兩處墨跡、與卷軸分離；原尺寸確認與「同一卷紙帶兩處怪痕」相反，**退回**。 |
| `line-of-sight` | `line-of-sight-1-trim.jpg` `3BADF101EAFDC2FD42A09328A5AC15BE6FB228AACA3CF0E2D1FE2E6AE8162920` | take 1 圖評通過，原尺寸可見星體模型波束掃到地球儀，與旁白相符；可用。 |
| `beam-away` | `beam-away-2-trim.jpg` `C7B8AC37BA121ABFFA874F60670E52511BDCCE11032A1E6324D0027B8363B5E8` | 三 take 都未過；選圖主光源是檯燈，並非星體發出且轉向別處的波束，**退回**。 |

兩個退回鏡頭已超過系列規則建議的補圖輪數，因此停止付費重畫。`more-marks` 改為一張 `stats` 卡，只寫「同一卷紙帶／2 處相隔很遠的怪痕跡」；[Bell Burnell 1977 第一人稱記述](https://www.bigear.org/vol1no1/burnell.htm)說同一張圖紙上在不同位置又出現兩處痕跡。`beam-away` 改為一張 `compare` 卡，對照波束掃過地球時記到一次脈衝、轉開時暫收不到；[NASA Science〈Pulsars〉](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-pulsars/)支持視線與脈衝的關係。兩張卡皆不假裝是已生成插畫，也不引入新的口播史實。

目前正文 100 景中保留 89 張獨立插畫，插畫比例 89%；連續內容卡最多兩張，符合系列底線。這兩張卡使舊 manifest 與後續修訂的 `video.json` 不相容；本收據定稿時的 `video.json` SHA-256 為 `A54C8962F3941599A0FCBDC8DCDB74A1B72F315A873384C3BF76EFAC1F1C2F7F`。劇本哈希也因卡片型別及定向修稿改變；目前**沒有新版劇本核准，也沒有有效的新分鏡核准**。待獨立敘事、史料及站主劇本關卡通過，再以當版重建 manifest、檢查 89 張圖與兩張卡的逐景綁定，製作新版聯絡表送站主。
