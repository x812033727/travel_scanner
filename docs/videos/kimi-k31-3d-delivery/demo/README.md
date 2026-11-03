# 原創 STL 交付檢查教具

這兩份網格、規格、程式與畫面由本片編輯自行製作，**不是 Kimi 生成結果**。
刻意填孔的 B 是對照教具，不能當成 Kimi 的失誤、模型評測或實際列印紀錄。

用途是練習：把需要的零件寫成外部規格，打開真實檔案，再讀懂有限檢查能回答什麼。

## 離線打開實際網格

直接在瀏覽器開啟 [index.html](index.html)。它內嵌兩份實際 ASCII STL 的完整文字，
由三角形座標畫出模型與水平剖面；沒有外部網路、CDN、套件或登入需求。
可拖曳旋轉，切換俯視、側視與水平剖面，下載目前 A 檔及外部規格。

1. 先讀頁面上方的外部規格與單位假設。
2. 分別看兩份網格的外部尺寸、封閉邊、指定孔內射線與體積。
3. 切到「水平剖面」，看真實三角形切出的交線，再回到使用目的作判斷。

「載入 ASCII STL」會替換 A；「載入規格 JSON」會重新計算兩份檔案。
上傳檔只留在瀏覽器記憶體，不送往伺服器。下載連結會使用目前載入的檔案；
「重設教具」恢復本包原始檔。此介面只支援 **XY 置中、底面 z=0、孔軸沿 Z**
的限定範例，其他位置先在 CAD 對齊；拒收不代表模型本身物理不合格。
這不是一般 CAD、任意孔徑量測器或製造檢驗軟體。

影片開場另用 [intro.html](intro.html) 呈現同一份真實網格的中性大幅側視，
只顯示外部名義規格與原創教具聲明，檢查結果尚未展開；後續才切到完整檢查頁。

## 用 Python 重跑同一套有限檢查

只需要 Python 3 標準函式庫；從 repo 根目錄執行：

```sh
cd docs/videos/kimi-k31-3d-delivery/demo
python3 check.py --stl ring.stl --spec spec.json
python3 check.py --stl filled.stl --spec spec.json
```

`check.py`、`ring.stl`、`filled.stl`、`spec.json` 是原長檔名的**逐位元組相同副本**，
方便完整顯示操作指令。檢查器與原研究版本完全相同，沒有調整演算法或門檻；
逐檔對照在 [provenance.json](provenance.json)。它會讀真正 STL 頂點，檢查邊使用次數、
邊方向、退化三角形、正體積、外部尺寸、33 條固定軸向射線，以及規格解析體積的 1% 範圍。

執行成功會輸出 JSON；**程式 exit 0 不等於驗收通過**。讀
`accepted_for_this_limited_spec` 和各項 `checks`：

| 教具 | 三角形 | 外部尺寸（假設 mm） | 封閉／邊方向一致 | 孔內受阻射線 | 網格體積 mm³ | 本例有限檢查 |
| --- | ---: | --- | --- | ---: | ---: | --- |
| A `ring.stl` | 512 | 40 × 40 × 5 | 是 | 0 / 33 | 5269.401464 | 通過 |
| B `filled.stl` | 256 | 40 × 40 × 5 | 是 | 33 / 33 | 6273.096981 | 未通過孔與體積 |

已執行的原結果在 [results/ring.json](results/ring.json) 與
[results/filled-hole-counterexample.json](results/filled-hole-counterexample.json)。
兩者共用名義外徑 40、名義孔徑 16、厚度 5 的規格，規格解析體積為 5277.875658 mm³。
這套檢查的固定射線從 z=-1 向上，只對 0 到規格厚度的範圍作判定；
CLI 不會自動找孔軸或重定位網格。對自己檔案重跑前，也必須先明確設定單位、座標與適用範圍。

若要保存可讀結果：

```sh
python3 check.py --stl ring.stl --spec spec.json > ring-result.json
python3 check.py --stl filled.stl --spec spec.json > filled-result.json
```

## 名義 16 mm 不等於最小淨空至少 16 mm

STL 不包含實體單位。本包是在外部 `spec.json` 宣告 mm，不能從座標猜測列印器設定。
原規格在此教具中使用**名義圓孔**；圓周以 64 段近似，因此 A 內圈頂點的名義直徑是 16，
實際網格邊的最小中心淨開口約 **15.980727 mm**。

獨立網格復核以五個高度的剖面確認：A 有兩圈閉合交線、中央不是材料；B 只有外圈、中央是材料。
其原收據 SHA-256 為 `3faf79eddb4716de8959081afcf036624eab52db980af23c465af0e0f2b8d0a3`，
凍結清單為 `7d53e4fc84c49113451a4e76f72cf516dc07a8ed61c58d0c3daf0d23163d17e6`。
本頁以實際中間剖面的交線重算，顯示同一個四捨五入結果。

**如果你的新需求是「最小淨空至少 16 mm」，A 也不合格。**
原檢查器的「通過」只代表上面的有限規格檢查，沒有包含最小淨空的嚴格 16 mm 門檻。
不要把它當成精確圓孔、裝配公差、任意孔形、自交、壁厚、材料、承重、切片或實際列印認證。
本片沒有親測 Kimi 下載何種副檔名，也沒有把這兩份檔案拿去列印。

## 重建頁面與來源畫面

若修改自己的 STL／規格，先保留原檔再重建：

```sh
python3 build_viewer.py
python3 build_intro.py
```

此步從原長檔名的 STL／規格讀取完整內容，套入 `viewer.template.html` 產生自包含 `index.html`。
它不會呼叫模型或網路。要修改短別名時，請一併更新對應原長檔名並重新檢查；
不要把修改後檔案仍稱為本包固定原教具。

`figures/` 是實際在 1920×1080 Chromium 打開頁面後擷取的本片原創來源畫面，
不是 AI 補畫、Kimi 介面或模型生成證據。頁面與瀏覽器驗證結果另記在
[results/browser-verification.json](results/browser-verification.json)，
中性開場圖另見 [results/neutral-intro-verification.json](results/neutral-intro-verification.json)。

## 授權

本目錄我們自行創作的程式、STL、規格、文件、結果和截圖依 [CC0-1.0](LICENSE.txt) 釋出。
官方 Kimi／Moonshot 文字、商標、模型權重及其他第三方素材沒有納入此授權；
研究目錄中的官方引文保留其原權利，不能因引用本包就宣稱已取得相同授權。
