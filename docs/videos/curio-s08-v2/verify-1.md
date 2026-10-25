# curio-s08-v2 查核第一輪（沿用第一版的查核）

- 這一集的查核是第一版（`curio-s08`，Codex 2026-10-19）寫在 Codex 資料夾的 `research.md`（S08 史料筆記：木牛流馬與運糧）與 `verify-1.md`（固定文本抽核），
  repo 裡沒有 `topic-checks/S08.md`。`research.md` 逐字核讀固定 Git commit 的古籍轉錄：Ancient-China-Books《三國志》commit `10a0b1ab3019d8821262f7402366d14fb4aaa102`（卷 33〈後主傳〉、卷 35〈諸葛亮傳〉與裴松之注）、
  《三國演義》commit `761813427eb5685c395804493f9fbd7ad8dc7d8d`（毛評本第 102 回），並以 daizhigev20 commit `4a6d6f2088825f132521d848c2ea86cf9c9a7620` 的第二轉錄交叉核對；
  第一版另有一位獨立讀者對固定文本抽核，結論是「No material conflict found」。
- **第二版（2026-10-25）沒有新增查核**，新加的句子只用下面這張表與〈交叉轉錄與來源層次〉裡原本就有的字；每一句旁白對到哪一列，見 [`claims.md`](claims.md)。
- 這份檔案只是把第一版的史料表與抽核表照抄過來，讓成片品管（`tools/video/qa/facts.mjs`）讀得到；兩邊不一致時以第一版 `research.md` 為準。表裡沒有任何一列判為 NOT FOUND。
- 沒有採用的線索（照抄第一版）：Needham《Science and Civilisation in China》vol. 4 pt. 2 只是書目線索，**沒核到書中說法與頁碼**，旁白不用；不以「獨輪車派」「四腳派」描述學界定論，
  也不說一千八百年來沒有任何人做出被一致接受的模型。

## 史料表（抄自第一版 `research.md`，查核 2026-10-19）

| 代號 | 固定文本 | 原文與可說範圍 |
| --- | --- | --- |
| [HZ33-231] | [《三國志》卷 33〈後主傳〉p10](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/033.htm#L23) | 「九年春二月，亮復出軍圍祁山，始以木牛運。……夏六月，亮糧盡退軍。」建興九年即 231 年；說使用木牛，也說該次終因糧盡退軍。**不能由此斷定木牛無效**；運補能力與戰役總需求不同。 |
| [HZ33-232] | [同卷 p11](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/033.htm#L24) | 「十年，亮休士勸農於黃沙，作流馬木牛畢，教兵講武。」建興十年即 232 年；字面記製作完成，但不能說兩者這時才被發明，因前一年已記木牛運糧。製成多少台、改過哪些結構，這句未說。 |
| [HZ33-234] | [同卷 p13](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/033.htm#L26) | 「十二年春二月，亮由斜谷出，始以流馬運。」建興十二年即 234 年；此處首次明說以流馬運，不等於世上第一台流馬在當月才造出。 |
| [ZG35-231] | [卷 35〈諸葛亮傳〉p13](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/035.htm#L26) | 「九年，亮復出祁山，以木牛運……糧盡退軍。」與後主傳對照。後文裴注另引他書談戰役，影片運糧主張不混作陳壽本文。 |
| [ZG35-234] | [同卷 p14](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/035.htm#L27) | 「十二年春，亮悉大衆由斜谷出，以流馬運，據武功五丈原……亮每患糧不繼，是以分兵屯田，爲乆駐之基。」使用流馬，同時仍苦軍糧不繼並安排屯田；不能說流馬因而失敗或完全解決補給。 |
| [ZG35-FORM] | [同卷 p17 陳壽正文與裴注](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/035.htm#L30) | 正文：「亮性長於巧思，損益連弩，木牛流馬，皆出其意」。**裴松之注**引「亮集載作木牛流馬法曰」，木牛「方腹曲頭，一脚四足……牛仰雙轅，人行六尺，牛行四步。載一歲糧，日行二十里」，其後「流馬尺寸之數」列肋、前後軸孔、前後杠、方囊等尺寸。「腳／足」是原文名稱，不是現代可確定的活動腿；「軸孔」亦不能單獨定輪數。轉錄沒有附原圖或成品，不能聲稱原圖絕不存在於所有時空。 |
| [YY102] | [毛評本《三國演義》第 102 回](https://github.com/Ancient-China-Books/sanguoyanyi/blob/761813427eb5685c395804493f9fbd7ad8dc7d8d/OEBPS/Text/481.html#L63) | 小說把木牛流馬寫成近乎活物的運糧器具，加入司馬懿仿造、轉舌令它停止等戲劇情節；頁面混有毛宗崗評語，核故事時須排除評語。只作後世小說版本，不當 231／234 年實錄。 |

## 交叉轉錄與來源層次（抄自第一版 `research.md`）


[第二轉錄 daizhigev20《三國志》](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E5%8F%B2%E8%97%8F/%E6%AD%A3%E5%8F%B2/%E4%B8%89%E5%9B%BD%E5%BF%97.txt#L1838) 的使用紀年及 [形制段](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E5%8F%B2%E8%97%8F/%E6%AD%A3%E5%8F%B2/%E4%B8%89%E5%9B%BD%E5%BF%97.txt#L1941) 可核對主要語句；本機檔 SHA256 `1180137e666366039465d794f24ab0d5dd83a70e844e9ec209afdd078c1b15b4`。稀字如木牛部件名有 OCR 異文，逐字引文以 Ancient-China-Books 固定本為主。

「陳壽正文說出於諸葛亮之意」和「裴注引《諸葛亮集》保留形制文字」是兩層來源；裴注引用不表示裴親自見過機器，文字也沒有在此附原畫。木牛「一脚四足」與流馬「前後四脚」屬兩段不同描述，不應拼成一個機器所有部件同時具有；沒有明確構件連接圖，不能由這幾字確定獨輪、雙輪或機械步行。

**逐字歸屬易混處：**卷 35 的裴注引文寫「載一歲糧，日行二十里，而人不大勞」，**沒有**「牛不飲食」；小說第 102 回另寫「人不大勞，牛馬不食」。兩層文字不可拼接成古文引句。裴注引文的開頭是「亮集載作木牛流馬法曰」，不能把「作木牛流馬法」逕稱固定書名或正式篇題。流馬前軸孔的原句是「前軸孔分墨去頭四寸，徑中二寸」：能指出孔位數字；「前軸孔／前脚孔／前杠孔」等名字也指出對應的部件類別，**但仍不能由此決定輪數或完整接合次序**。

## 固定文本抽核（抄自第一版 `verify-1.md`，2026-10-19）

| Check | Primary text and result |
| --- | --- |
| 231 / 建興九年 | 〈後主傳〉 says “九年春二月，亮復出軍圍祁山，始以木牛運” and “夏六月，亮糧盡退軍.” Script 51–95 accurately pairs use and later shortage without calling wood ox useless. |
| 232 / 建興十年 | The next 〈後主傳〉 entry says “亮休士勸農於黃沙，作流馬木牛畢，教兵講武.” Script 105–137 treats 畢 as completion and leaves invention date, quantity, and revisions open; that boundary is justified by the prior year's wood ox use. |
| 234 / 建興十二年 | 〈後主傳〉 says “十二年春二月，亮由斜谷出，始以流馬運.” 〈諸葛亮傳〉 says he moved to 五丈原, “每患糧不繼,” then “分兵屯田,” with cultivators among 渭濱 residents and people at peace. Script 9–13 and 143–195 follows these entries, without claiming either the flowing horse or farming fed the entire army. |
| Chen Shou versus Pei quote | Chen Shou's main text says “木牛流馬，皆出其意”; Pei's annotation separately introduces “亮集載作木牛流馬法曰.” Script 209–229 keeps the authorship and description layers distinct and does not turn Pei into an eyewitness. |
| Wood ox tongue versus novel operation | The quoted 《諸葛亮集》 text says “舌著於腹” and later “垂者爲牛舌.” It does not say that twisting it stops a device. Chapter 102 of the later novel explicitly has soldiers “將木牛流馬口內舌頭扭轉，牛馬就不能行動,” then twist it back; soldiers cannot drag or lift the stopped devices, and disguised “神兵” deploy smoke. Script 249–253 and 347–375 preserves this distinction. |
| Ancient units and parts | The Pei quote has “特行者數十里，羣行者二十里,” “人行六尺，牛行四步,” and “載一歲糧，日行二十里.” The separate “流馬尺寸之數” has front/rear axle holes, “前後四脚,” and two square sacks, “每枚受米二斛三斗.” Script 261–329 does not convert these into modern mass, speed, wheel count, or a total supply capacity. |
| Mechanical form | The wood ox “一脚四足” and flowing horse “前後四脚” are in different paragraphs. The fixed transcription provides part names and measurements, not a checkable assembly drawing or a complete account of joint motion. Script 273 limits the no-drawing statement to this transcription; 321 and 337–401 appropriately refuse a unique original form. The stronger universal claim that no drawing ever existed is absent. |

**Source verdict:** No material conflict found in these sampled claims.（第一版原文；同一份檔案裡的盲評結果屬於第一版的稿子，第二版不沿用。）
