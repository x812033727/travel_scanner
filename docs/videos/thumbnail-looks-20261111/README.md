# 縮圖新版樣張（2026-11-11）

站主看過樣張後定的兩種新版型，這幾張是用 `tools/video/render/browser.mjs` 加 `templates.mjs` 的 `thumbnailHtml` 實際畫出來的（票 `tasks/open/2026-11-11-bright-explainer-and-drama-thumbnails.md`）。

| 檔案 | 版型 | 說明 |
| --- | --- | --- |
| `drama-zhong-tian-qu-qi-e003.jpg` | AI 劇 layout `f` | 滿版關鍵影格、下三分之一黃字黑邊大字、左上種田橘色劇名條、右上 MOKAAIR |
| `drama-tai-nainai-e018.jpg` | AI 劇 layout `f` | 同上，祖媽紅色劇名條；含淚特寫是這個版型要的那種臉 |
| `drama-long-headline-balanced.jpg` | AI 劇 layout `f` | 7 字標題平均斷成兩行（聘禮是／三塊肥皂），不會斷成 5＋2 |
| `drama-en.jpg` | AI 劇 layout `f` | 英文版：劇名條與標題都換成譯文，長字自動縮 |
| `sothatswhy-p14-no-keyframe.jpg` | 原來如此亮底 | 沒有關鍵影格：天藍到夕陽橘漸層、墨藍白邊大字、芥末黃強調、墨藍副標色塊 |
| `sothatswhy-over-a-keyframe.jpg` | 原來如此亮底 | 鋪在關鍵影格上：字那側奶油色遮罩。示範用的底圖是祖媽 c14；主體在中間時會被字壓到，正式出圖用主體在右側的鏡頭，或 `data.subject: "right"` |
| `sothatswhy-subject-right.jpg` | 原來如此亮底 | `data.subject: "right"`：圖縮到右側 38%，字與人分開 |
| `sothatswhy-en.jpg` | 原來如此亮底 | 英文版：三行內排得下，副標一行，太長就縮字 |

紅色「原來如此」印章放在左下、系列字樣旁邊：放在字欄右上時，第一行 5 個字以上或英文標題會被它蓋住，圖縮到右側時也會蓋到圖。

底圖：種田 `s33`、祖媽 `c14` 取自站主雲端硬碟的製作檔。種田這張表情偏平，正式挑 `data.shot` 時選情緒最強的臉。

## 站主定案（2026-11-11）

另一個 session（P06／P18／P21 那條，`claude/p06-p18-handoff-d2av3g`）把同三集用 main 與這個分支各畫一次給站主比：

- `sothatswhy-old-vs-bright.jpg`：左舊（墨藍遮罩）、右亮底（5a0a1996，印章在右上）。站主：「新版比較好，P06 P18 也換新版」。
- `sothatswhy-stamp-top-vs-bottom.jpg`：左 5a0a1996（印章右上）、右 4eb899d（印章左下）。站主選右邊：**原來如此縮圖就此定案，用印章在左下的這一版。**
- `sothatswhy-p06-final.jpg`、`-p18-final.jpg`、`-p21-final.jpg`：定案版畫在 P06、P18、P21 實際的縮圖鏡頭上（都寫 `data.subject: "right"`）。

這個 PR 合併後，P06、P18 要重 render 縮圖並重送上架關卡（已核准的縮圖是舊版），P21 直接用新版；由那條 session 處理。
