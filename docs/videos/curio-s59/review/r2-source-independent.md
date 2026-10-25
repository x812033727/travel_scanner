# S59 R2｜獨立史料與書面畫面覆核

2026-10-21 00:10 UTC。**整體 HOLD：史料、逐句主張 PASS；書面畫面 HOLD。** 本報告只審下列凍結 R2 版，沒有修改創作檔、購買媒體或代替網站／站主核准。敘事雙盲須另行判定，不能由這份來源審查轉成敘事 PASS。

| 凍結檔 | SHA-256 |
| --- | --- |
| research.md | ad5baec33ae786da9d103eecadca9f16c9f23f00d4041bde158e1e2697958efb |
| brief.md | 90024cd567cb540e92fe9d58815cb36a0d05ade7a6739ec6851a54d6d5d10b80 |
| claims.md | b84f891c58a937cd9fd2cfffc2aab0f14c0c652fee838f6a79bfca2b40e99bc5 |
| video.json | 26844c8610bd399077be2f349b3c548168c5021d6c143a88610ca8138d16a435 |
| script.md | c74ea14ea53d7442b59d2232fd867b1ce7794aae4b2878337b693fe25a3e78a3 |

## 固定原文與逐句查核

我另行從固定 Git commit 重開 [D：杜蒙塞爾 1878 法文原版](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt)、[E：1910 愛迪生授權傳記](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt)，並核對原始位元組 SHA-256，分別為 c48361e94523ebacc000172ebab34895bb20c0b7e458ac3e122f90a3cc9e717c、9818547c6dd15e488c1923bad5cc09cb4fa3f447641daaaf77b2f539b4d49d34；[1892 英譯 T](https://github.com/GITenberg/The-telephone-the-microphone-the-phonograph_75683/blob/6b0cda8809aa60bf44270a64853c9aaf9ea5c546/75683-0.txt)的 SHA 為 cb9e9fbeee72750d6335413a9f91a450c09b9a40377fbc1c42c7822a79c598c9，只作詞義輔助，未算另一名證人。claims.md 共有 **109／109** 句與 video.json、script.md 的 ID、順序及口播文字逐字相同；121 個直接來源連結全指 D／E 的固定 commit、存在的行號範圍。現版 109 景為 100 張 shot、9 張工具字卡；lint 為 0 errors／0 warnings。

R1 的四個阻擋已修正：

1. s59018 刪去只見於 **傳記編者** [E5175–5184](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5175-L5184) 的「紙帶拉快發聲」；現句只問人聲如何留痕，可由愛迪生被引述的紙盤與電話薄片 [E5195–5221](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5221) 推出。
2. s59019 改談電話薄片隨聲震動，與愛迪生引述 E5209–5219 相合；已不把編者的接觸桿或 [E5165–5173](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5165-L5173) 明確否定的「針刺手指啟發」說法算給他。
3. s59057 現在只說「小羊」出自愛迪生多年後的回憶，沒有再斷言當日錄音載體的存世狀況，也沒把它叫作音檔。[E5220–5241](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5220-L5241)足以支持這個來源層級。
4. s59069 刪去杜蒙塞爾「站在旁邊」的無據位置，只保留他轉引未具名現場來信的事實；[D6995–7013](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6995-L7013)支持。

其餘 P01–P16 的口播來源與層級亦可追到固定原文：D6872–6976 支持圓筒、話筒、薄片、針、手柄、回放與磨損；D6978–6993 分別支持**另述的**倒讀和電話隔聽可能性；D6995–7049 支持會場、匿名來信、本人失敗、幾名院士重試和本人後來解釋。E5195–5241 支持愛迪生**晚年回憶**的紙盤、十八美元草圖、克呂西和童謠；E5262–5273 支持他所回憶的編輯室示範。劇本沒有把這兩份材料合成一名當日證人，也沒有說科學院全體投票、秘書室實做倒讀或電話隔聽。s59106 已明說後者未記於當日程序。

## 必須修的書面畫面

| 景 | 現行提示詞的問題 | 修正界線 |
| --- | --- | --- |
| s59004、s59009、s59070、s59071 | 各寫「one」名懷疑者，卻另要求他看 demonstrator's face、human profile、demonstrator's mouth 或 operator's face。這需要第二個可見人，與 [Curio 一人一動作規則](../../../../.agents/skills/curio-episode/SKILL.md)及 [brief.md](../brief.md) 自訂的單景規格衝突；模型亦可能把視線與嘴畫到錯誤人物。 | 每景保留**一位**成年懷疑者的臉與一個動作，例如注視桌上的素面話筒／手搖柄，或用空椅與器械做視線終點；旁白已講懷疑對象，無需在同張圖再畫操作員。不要造可讀的現場來信。 |
| s59017 | 提示詞仍畫「curled embossed paper strip」，但此段口播與來源明指愛迪生引述的**旋轉紙盤** [E5195–5205](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5205)；快速紙帶屬另一段傳記編者敘述，R2 已刻意移出口播。 | 改成一位發明者端看**有螺旋壓痕的圓紙盤**；不要畫紙帶或手指被針刺。 |
| s59097 | 同一位人物要「checks the stylus ... while speaking near a horn」，同時做兩件相互分心的動作，違反單人單動作的可畫性；本句主張是嘴離話筒的距離。 | 只畫一位成年操作員**靠近話筒說話**，讓薄片／針作靜態背景；或只畫他檢查針，不能兩動作並列。 |

這六景不是聲稱原件實物的來源錯誤，而是現版的**書面畫面可行性停點**。它們已在凍結 video.json 中，故 R2 不能用來源 PASS 直接開畫。新作者只需窄修這些 data.prompt，重跑 lint，請未撰詞者按新的 video.json SHA／visualHash 核對差分與來源，再進原生圖 pilot；既有 R2 書面 PASS 不會自動轉移。

書面政策預檢：現有標題、說明與口播把腹語疑慮限定為未具名來信中的部分聽眾，把愛迪生故事明列為 1910 年追述；說明欄也標示畫面為原創插圖及示意卡，未冒稱原件照片或存世音檔。預定人物均逝世逾 70 年，提示詞沒有血腥、仇恨或可讀偽造史料要求。這只排除目前書面稿中可見的誤導點；日後合成內容揭露、圖片實際呈現及上架政策仍須依成品另審。

另兩處供同一輪編務處理：thumbnail.headline 現填有字面星號「**腹語？**」，若模板當純文字繪製會顯示星號，宜改成無星號標題；brief.md 最後一段仍寫圖片評審和配樂額度已滿，已被 2026-10-20 深夜的 30,000／100 新額度取代。這兩項不改史料結論，但不能拿舊額度作實際排程依據。s59106 的遠端聽者是 D6987–6993 的假設驗法，旁白已說非當日實驗；日後原生圖仍需防止它看起來像秘書室實況。

**結論：史料／逐句主張 PASS；書面畫面 HOLD。** 新版必須重新凍結五檔，重新查六景的提示詞差分及受影響視覺雜湊；雙盲敘事、政策、旁白、插圖、配樂、成片和網站關卡均尚未由本報告放行。
