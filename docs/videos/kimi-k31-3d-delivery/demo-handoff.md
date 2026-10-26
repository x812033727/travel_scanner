# 原創 STL 教具與實際來源畫面交接

2026-10-26。已完成可攜的原創教具、實際本機檢查與五張 1920×1080 來源畫面；
這是本片素材，**不是 Kimi 生成／匯出測試、成片、旁白或八語媒體交付**。
沒有執行模型、付費語音、原生影片製作、後台寫入、合併、部署或 YouTube 上傳。

## 可直接使用的檔案

- [離線檢視頁](demo/index.html)：完整內嵌實際 STL，無網路、CDN、登入或外部套件。
- [中性開場頁](demo/intro.html)：同一份網格的大幅側視，只顯示名義規格，沒有檢查結論。
- [操作與完整指令](demo/README.md)：Python 3 標準函式庫；原創檔案依 [CC0](demo/LICENSE.txt) 釋出。
- 短指令入口：[check.py](demo/check.py)、[ring.stl](demo/ring.stl)、[filled.stl](demo/filled.stl)、[spec.json](demo/spec.json)。
  四者都是原長檔名的完全相同副本；[來源對照](demo/provenance.json) 保留完整 SHA-256。

在 `demo/` 目錄執行，指令均可完整放入 64 字元字卡：

```sh
python3 check.py --stl ring.stl --spec spec.json
python3 check.py --stl filled.stl --spec spec.json
```

兩個短指令已真正執行且正常結束，輸出數值與原長檔名結果相同；
詳見 [短指令收據](demo/results/short-command-verification.json)。
程式 exit 0 是完成計算；幾何是否通過要讀 JSON 的 `accepted_for_this_limited_spec`。

## 已擷取並實際看過的畫面

五張都是 Chromium 打開本片原創頁面、讀取真實三角形後的截圖，沒有套 Kimi 介面或商標。
作者已逐張開啟實檔核對，ROOT 的獨立觀看仍是另一個步驟。

| 圖片 | 畫面用途 | SHA-256 |
| --- | --- | --- |
| [00 中性側視開場](demo/figures/00-neutral-side-intro.png) | 前段先出現真實幾何；無通過／失敗、射線、體積或最小淨空結論 | `569b6bd06455d340de64ad07c7bcea90a94ce5b51494f9ac2f63d90f6e5162ff` |
| [01 立體比較](demo/figures/01-oblique-comparison.png) | 同一規格，兩份真實網格；可拖曳旋轉 | `3713cf79544d1fae0a79af8ee699fc58c41852d835df550a630c833bba90d22e` |
| [02 俯視](demo/figures/02-top-view.png) | 有孔與刻意填孔的外形對照 | `624dc84b89548fb163d68ce35a5f1fc4e5726f939af3ff115175b54ceb063115` |
| [03 水平剖面](demo/figures/03-horizontal-section.png) | 兩圈／一圈交線、中心材料差異；嚴格最小淨空 16 mm 的反例 | `c672c7c82da8d0d304405ba28951a784551afbc8c19b0c873b97099c0bba29eb` |
| [04 側視](demo/figures/04-side-view.png) | 外部尺寸與厚度相同，仍不能證明指定孔存在 | `85d284ed7e933d22dae85a11407d3f8114f272f7413e331678b584236767f378` |

逐圖尺寸、bytes、實際瀏覽器與數值對照在
[browser-verification.json](demo/results/browser-verification.json)，
另有 [中性開場圖收據](demo/results/neutral-intro-verification.json)，
實檔觀看記錄在 [visual-review.json](demo/results/visual-review.json)。
影片可引用這些原創頁面作 `screenshot` 素材；它們不是官方產品截圖或模型輸出。

## 真正核對的結果與限制

原始兩 STL、規格與 Python 檢查器均原樣複製，沒有演算法／路徑修補：
checker SHA-256 為 `f930e4c88b2f147a28d5304cb4a4691e42b2df8e8388c8b23327ce678e9f2be7`。
A 有 512 個三角形，B 有 256；兩者外部尺寸均 40×40×5，邊網格均封閉且方向一致。
33 條指定孔軸射線在 A 受阻 0 條、B 受阻 33 條；A 網格體積 5269.401464 mm³，
B 為 6273.096981 mm³；名義環形規格解析體積 5277.875658 mm³。
原檢查器的限定結果在 [A](demo/results/ring.json)／[B](demo/results/filled-hole-counterexample.json)。

獨立幾何原收據 `3faf79eddb4716de8959081afcf036624eab52db980af23c465af0e0f2b8d0a3`，
凍結清單 `7d53e4fc84c49113451a4e76f72cf516dc07a8ed61c58d0c3daf0d23163d17e6` 保持原狀。
它確認五層剖面；本頁由實際三角形重算中間剖面：A 兩圈、中心空；B 一圈、中心有材料。
紅虛線只標外部規格的名義孔圈，**不是 B 的真實孔邊**。

單位是外部規格假設 mm，STL 自己不含單位。64 段近似使 A 的名義孔徑 16 mm，
最小中心淨開口約 15.980727 mm；**若新需求是最小淨空至少 16 mm，A 也不合格**。
原有限 checker 沒有這個嚴格最小淨空門檻，通過不等於圓孔精度、公差、任意孔形、
自交、壁厚、材料、承重、切片或實際列印認證。沒有親測 Kimi STL 匯出或拿教具列印。

介面上傳僅支援 XY 置中、底面 z=0、孔軸沿 Z 的限定座標；平移的測試檔會被明確拒收，
而不當成零件物理失敗。載入其他檔時不沿用原 A 的孔／64 段／名義 16 結論，
下載的是目前實際載入的位元組；重設恢復原教具。

## 實際驗證與保留的問題

正常 Chromium 真實執行完成 20 項檢查：兩份網格與原 Python 結果相符、四種視角、
1920×1080 無頁面溢出且幾何不碰 Canvas 邊、拖曳改變畫面、三個預設下載逐位元組相符、
上傳 B 正確取代 A／重算與下載、平移拒收、改規格後正確下載、錯單位拒收、重設，
及 390px 無水平溢出。手機頁面依正常內容縱向捲動。
沒有頁面例外或外部網路請求。

獨立讀者另對實際頁面原始碼、嵌入檔案和純幾何函式復核，主頁審查收據 SHA-256 為
`cff284644bf32bc2a78b4e7a725577fbe43f788ec69f1bf55651b2be15d1511d`；
中性開場追加審查為 `7fe49f2aadf4b3b864d092f3da1617a67355c968f8e3a498aade17bec4c332b7`。
這兩份是獨立原始碼／純計算審查，瀏覽器實跑和實檔觀看仍依上述作者的真實紀錄區分。
完整私有審查保留供 ROOT 檢視；這些雜湊不代表官方模型測試或製造核准。

ROOT 實際看過原四圖後指出：四圖都提前揭露孔檢查結果，不適合最早的幾何鏡頭。
因此只補一張 `00-neutral-side-intro.png`：真實解析 512／256 三角形、同色大幅側視，
只顯外部名義規格／單位假設和「檢查結果尚未展開」。新頁面沒有改動原檢查、旗標或結果；
另外一次正常 Chromium 實跑核對 1920×1080、無溢出、幾何不碰邊和可見文字沒有結果提示。
作者已實際開圖看過；原四 PNG 的 bytes／SHA-256 保持不變。

原始失敗與修正未假裝不存在：初始版高度溢出、上傳結論硬字、瀏覽器 selector 衝突、
本機檔案下載逾時，以及視覺檢查才看見的 Canvas 底邊裁切，均記在
[production-history.json](demo/results/production-history.json)。失敗原始收據與舊模板／中間圖留在私有工作區；
初始 layout 的截圖及 JSON 檔名曾在修正時重用，未冒稱保留其原始二進位。
正式來源圖是修正後重新擷取並逐張實際觀看的版本。

CC0 只適用本目錄自行創作檔案。研究中的 Kimi／Moonshot 官方文字、權重、商標或其他第三方素材，
不在這個 CC0 授權內。這份交接不改動既有語音額度、全域 ASR、未知計費或審核規則。
