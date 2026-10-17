# H11 英文翻譯獨立審稿（第 1 輪）

日期：2026-10-16（Asia/Taipei）。審核對象為工作區 `curio-h11/i18n/en.todo.json`，SHA-256 `6C82B8EC215D0816AE9A883F3D9B450E91DE2389229F9FF0F2272DD08A4082DB`；繁中 `video.json` SHA-256 `FED1B627BD30491F9356FA7D9E061E9A872B9E7FFB8EE7B446409D4678363316`。審稿員未撰寫或改動英文工作表、繁中劇本或媒體。

**結論：HOLD。** 英文工作表與目前繁中稿逐欄對齊，但 `v0e564e3` 忠實翻出繁中稿的「四頁」時，與現行原始定年報告的「四葉」衝突。此處須先由主協調者處理繁中源稿與既有核准關卡，再更新英文；其餘五處也須修正後重審。未合併翻譯、配音或送語言審核。

## 必修項目

| ID | 類別與問題 | 現有英文 | 最小修法 |
| --- | --- | --- | --- |
| `v0e564e3` | **事實／源稿衝突。** 繁中「從四頁取下四份樣本」及英文 `four pages` 均與 [Greg Hodgins 給 Yale 的 2009 年原始報告](https://www.voynich.nu/papers/Carbon_GH_2009.pdf) 不符：PDF 第 1 頁標題指明 leaves 8、26、47、68，第 2 頁再次稱 four leaves。這一集先前還特別區分「葉」與「頁」（`v8949601`、`v2405e28`）。 | Researchers took one thin strip from each of four pages: four samples in all. | 繁中經核准流程改為「研究人員從四葉羊皮紙各取下一份樣本，每份都只有細細一小條。」；之後英文改成 `Researchers took one thin strip from each of four leaves: four samples in all.`。不能只改英文，否則字幕／配音與已核准繁中旁白不一致。 |
| `vc25d396` | **證據界線。** 「That is no paper retraction」像是獨立斷定論文狀態；繁中只說不能**因撤下新聞稿**就宣稱論文撤稿。[Bristol 原聲明](https://www.bristol.ac.uk/news/2019/may/voynich-manuscript.html) 也只說移除網站上的報導。 | It removed the news release, not the paper. That is no paper retraction. | `The news release was removed; that alone does not mean the paper was retracted.` |
| `v965353b` | **提前揭曉。** 繁中先說首頁右邊有「幾欄痕跡」，下一句 `v81627c3` 才揭曉是三欄；英文在本句提前說 `three columns`。 | The opening search leads to three columns on the first page's right margin. | `The opening search now points to columns of marks on the first page's right margin.` |
| `vaa3669c` | **字幕分段順序。** 繁中第一 cue 是後來讀者的頁邊字，第二 cue 才談分清時期；英文把「分析正文以前」放到第一 cue 前頭。 | Before studying the text, researchers separate later notes in the margins. | `Later readers added margin notes. Separate traces from different periods before studying the text.` |
| `v7cfdf05` | **字幕分段順序／語氣。** 繁中先回到前面找到的規律，再問能造出相似文字說明多少；英文先講造字，並把「說明」加強為 `prove`。 | If someone can make similar writing, what do those text patterns prove? | `What of those earlier text patterns? If similar writing can be made, what do they tell us?` |
| `vfc824ec` | **書名。** [2013 年研究原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066344) 的書名是 *On the Origin of Species*，現稿省掉 `On the`。 | They compared Chinese Shiji, English Origin of Species, and Latin texts. | `They compared Shiji in Chinese, On the Origin of Species in English, and Latin texts.` |

## 其餘核對

- 75／75 句的 ID 與繁中原句、7／7 章名、標題、說明、標籤與縮圖來源欄，均與目前 `video.json` 逐字相符；工作表 `parts` 為 `metadata,captions`。29 句有分段邊界；上表以外未見條件倒轉或 cue 順序問題。
- 75／75 英文句子皆未超過各自 `max_chars`；最長 97 字，5 句超過「約 80 字」建議值，但均低於配音硬上限，其中較長的三句有兩個字幕 cue，因此不另提為阻擋項。英文標題 69 字（≤100）、7 章名各 ≤30 字、標籤合計 93 字（≤500）。
- 專名 `Voynich`、`Davis`、`Marci`、`Greshko`、`Naibbe`、`MS 408` 形式一致；[Yale 館方介紹](https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript)、[Davis 本人研究紀錄](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/)及 [Greshko 作者 README](https://raw.githubusercontent.com/greshko/naibbe-cipher/main/README.md) 支持目前的姓名／模型名。Davis 的 Marci 筆跡比對仍寫成初步判讀；Naibbe 仍是作者提出的模型，未聲稱解出原稿。定年句保留羊皮紙而非墨水的界線。
- 英文標題及標籤未加自行發明的頻道英譯名，符合 `caption-translate.md` 的站主規則。說明保留 README、未重跑模型／未讀受限全文、AI 插畫與當代研究者肖像的揭露。縮圖三處文字都有譯文，保留原本換行與 `**` 強調。

修正後請重產工作表 SHA、逐句查上表六處，並在繁中源稿／媒體關卡處理完畢後才讓此輪英文結論轉為 PASS。
