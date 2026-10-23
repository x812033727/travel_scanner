# H05 `burial-edge` 實驗對照圖卡候選（2026-10-14）

狀態：**免費、隔離候選**。只新增原創 [`burial-edge-control-candidate.svg`](diagrams/burial-edge-control-candidate.svg)，沒有接入正式 `video.json`、重排句子、寫入正式音訊／判圖 manifest／帳本，也沒有啟動 MiniMax。這張卡是對 `h5v101`「在埋沙後再灌水的對照裡，小藻只鑽進紙邊幾毫米」的來源限制補充，不是當年贖鈔、河岸或實驗照片的重建。

## 來源與圖面界線

[Kaye、Meltzer（2020）原論文](https://www.nature.com/articles/s41598-020-70015-z)方法段寫：兩疊各五張**現代鈔票**乾燥埋於約 9 公斤沙中；一疊平放、一疊直立；把矽藻土以 **1 kg/L** 混入水，將約 15 公升的高濃度混合水通過沙箱。結果段寫，滲入通常限於鈔票邊緣內約 **3–4 mm**，更內側無矽藻。2026-10-14 查閱；卡面只列兩疊現代鈔票、先埋沙再灌水、濃度及觀察範圍，避免把對照條件混成當時的天然河水或原始贖鈔。未複製論文圖表或顯微照。

SVG 為 1600×900，內部奶油色矩形只延至 800 高，事實文字集中在上方。**正式 `.t-diagram .paper` 仍有鋪滿整張卡的奶油色背景；單改 SVG 矩形高度並沒有替 CC 創造不同底色的留白。** 圖面標出「研究對照示意」「Kaye、Meltzer（2020）」「非原始贖鈔」「非天然河水或案發現場」。SVG SHA-256 `46ff8ce3ae34f5d32168d5ec0e86127a8d770faf1fc65038119ad2ecffb27f51`。

## 隔離版面與時間窗檢查

以倉庫的 `slideHtml` 與正式 headless Chromium `openRenderer` 畫 1920×1080 靜格，再用 ffmpeg Lanczos 縮至 1280×720。以實際 `h5v101` 文字疊上代表性兩行 CC，兩尺寸目視：來源、濃度、結果及限制均可辨讀，CC 覆蓋的是沒有事實文字的卡片下緣，**沒有壓住來源腳註或其他事實文字**；但外層奶油色面板仍延伸到字幕背後，視覺留白問題尚未解決。兩次 Chromium capture 的 `layout_problems=[]`，SVG `svgProblems=[]`。這是靜格與模擬 CC 的局部品檢；正式成片採可開關 CC，播放器位置和有聲剪接仍須另驗。

隔離檔位於 `<home>/mokaair-work/videos/_offline-h05-burial-edge-20261014/`；其中 `render-candidate.mjs` 可重畫，`render-qa.json` 保留機械結果。PNG SHA-256：`burial-edge-1080.png` `47420923719316199aef0b6ff21b3f162eeb8be5d6f10fbd2175200982875c7e`；`burial-edge-cc-1080.png` `e823dd0242d6bf953e6d53195ad36051418cc709df45f3b4140d36f7db6f6e78`；`burial-edge-720.png` `b2231c81aba8a56a4f6c036c98f5aff6a1400a5e3c87d4a5eb63e996b7aa03a7`；`burial-edge-cc-720.png` `b32a4794d15dec40cf17964a5bcb0fecac6f9fd4eecca6660692b4310011db26`。

現行正式 `timeline.json` SHA-256 `fd724a0c4318fe76fcb4a1811dadbf09f0aeff47d0849bfc025ceb03fed50fbc`：`burial-edge` 為半開影格 **14,474–14,679**，205 格／30 fps＝6.833 秒。若只把這景的 `shot` 改為 `diagram`，保持此時間窗與其餘景數不變，規劃插圖占比由 8,519／15,912＝53.5382% 降為 **8,314／15,912＝52.2499%**，高於 50% 門檻 358 格。這只是模板配置的算術，並不證明其他 `shot` 已通過人工驗圖。正式接入會改動分鏡／時間軸雜湊；應重新計算、做敘事與聲畫檢查，並對新雜湊取得站主音訊核准，舊核准不可沿用。
