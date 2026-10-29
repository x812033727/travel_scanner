# S38 R8ac｜PF020 單景提示詞獨立紙審

2026-10-22 UTC。審者：`/root`，未撰寫 R8ac 提示詞。結論：**PASS，僅放行安全離線重綁與 PF020 下一次單張受控試畫**；PF021／PF022 不在此票範圍。此票不預判新圖會通過機器或人工驗收。

- 鎖定修訂：`video.json` SHA-256 `d8d169a010a7ffce93b3aec580e7c9580dc3a5393ffbe0bbc5909b72e8559688`；由 `b955dae2c2620b7477fcdef24606d9c1696f390c927f9fc7be10aa058d0b2ae9` 改來。實際解析前版與現版 JSON，替換 `scenes[19].data.prompt` 後全樹相等，確認只有 PF020 提示詞一葉變動。`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 未變。
- 固定原始材料：GITenberg Pepys 1666-09-02 條目 L65816–65824，全文 SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。原文 `Everybody endeavouring to remove their goods, and flinging into the river or bringing them into lighters that layoff` 支持旁白「還有人把搬不及的東西直接丟進河裡。」與單名成年居民放手讓一個家當布包越過岸緣的插畫動作。灰髮、羊毛上衣、亞麻領、石岸及布包形制是插畫選擇，未在旁白或卡片聲稱日記記載這些細節；不把人認作佩皮斯，也未添物件下落。
- 窄修針對[首圖退件](verify-98-r8ac-pf020-seed1-human-reject.md)的兩個實際錯誤：現代感第二人與抓箱子、怪桿觸水。新提示詞只要一位成年居民，改成雙手放開已在水上的布包，背景簡化為河水和陰天，動作與台詞相符；保留系列 `look: cute-mystery`，不加 `style` 或 `negative`。材質、年代描述合理，不構成額外史實宣稱。
- 風險：`releases ... with both hands` 與 `airborne` 仍可能被模型畫成手還抓著物件；請在新圖原始 1280×720 畫面逐張驗是否真的離手入水方向、是否混入現代衣飾，並遵循九題 judge。若主要動作或時代明顯錯，再退件並停線。提示詞紙審 PASS 不等於出圖 KEEP。

付費前仍須執行作者提案的完整前置檢查：確認 STOP 與 jobs 清空、12 張舊 KEEP canonical 條目與入選實檔雜湊、manifest／ledger 原樣、單景 dry-run 與 live media status、整集 US$4.58 上限；先安全離線重綁 `visual_hash` 後才可一次只畫 PF020 一張。`mokaair.com` 預檢不可達期間不得以本票代替 live 就緒證據。
