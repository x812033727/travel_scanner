# S08 現行劇本精確版本複核與旁白續作

2026-10-19。現行 [`script.md`](script.md) SHA-256 **`54974b5cb36c0f3ecbc889fe4bc84c185a4bcd53f75964a47d684e1d307c4113`**，`video.json` SHA-256 `721671fbce11eb96d6d3d502505a7ab83a2e100d5f06db5deff12e1fdf1e63d4`；93 句、87 張插圖、4 張資料卡，`lint` 0 errors／0 warnings。另一位此前未看此稿的新讀者先封存 13 題原始答案 `/tmp/s08-r4-blind-raw.json`，再登錄到 `/workspace/.video-work/curio-s08/review/narrative.json`，round 4 **13／13 全過**。讀者前後核對確切檔案雜湊，並沒有改稿。上一版 `6499e852…` 的 12／13 與更早 `6a9218…` 的 12／13 保留在 [`verify-9.md`](verify-9.md)，沒有改寫成成功紀錄。

關鍵 `no_recap`：開場 `ox007` 的「一腳四足」在 `ox057` 明說「開頭那句」並補出其位於木牛段、緊接「方腹曲頭」；`ox061` 再回扣這句，但新增文字無法證明零件會前後屈伸的界線。`ox066` 問「載一歲糧」能否換算重量，`ox068` 直接答「不能」，新增史料未交代供幾人吃。`ox079` 問第一個接點，`ox094` 明說「剛才問」並指出連接次序不完整。固定[《三國志》卷三十五裴注](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/035.htm#L30)確有「木牛者，方腹曲頭，一脚四足」，同段有「舌著於腹」「載一歲糧」及流馬孔位名稱；引用屬裴注引《諸葛亮集》，不能把文字說成完整復原圖，亦不能把小說的轉舌即停當古文操作。改寫句的來源範圍和前幾輪查核見 [`research.md`](research.md)、[`claims.md`](claims.md)、[`verify-9.md`](verify-9.md)。

`review-push --gate script` 已把此版送站台；手動製作片在站台仍待審。依站主於本對話明確委託「以你推薦的就好不用問我」「一直做完所以影片」，製作方在本機 `approve --gate script` 綁定上述確切 SHA，備註明寫**站主沒有親自逐字審此次改稿**。TTS dry-run：原有 93 請求中只有 6 句變動，需新合成約 166 個 Gemini 計費字元；此後已啟動同聲線 Sulafat 的變動句重念。新稿音檔 `check-audio` 通過前不能說旁白合格；S08 付費插圖仍未啟動。
