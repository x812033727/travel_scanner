# B18 法院 PDF 分源與爭議年份降級候選：獨立審稿請求

請由**沒有撰寫本候選的人**對 `B18.json` 的 canonical story SHA-256 `7a598d16c9efcd9014f3554531dfe5569408cb1542cbeb1f90fdfbff4b0975e5` 重新查核。先核對 [父版與本版的差異](delta.json)及 [65 筆逐景映射](claim-coverage.json)，不能只從舊 `reviews/B18.json` 複製結論。

1. 直接開啟[日本法院 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)：分清當事人「事實／主張」和法院「理由」。理由 P8 L466–474 是否認定第 579776 號於 1962 年登錄？P10 L574–578 是否認定這**一項**實用新案 1972 年期滿，且其後已有與原告無關的多家企業經營？確認沒有把被告對另一權利第 851953 號的答辯誤當法院獨立認定。
2. 打開[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)與[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)，逐句核對各自 1978 年版本與 J-Net21 的律師警告、加盟店獨立。這些網頁不能代替 PDF 的 1972 年認定，也不能確定完整權利鏈。
3. 核對十筆 row 事實中 `must_verify[4].sources=[3]`、`must_verify[5].sources=[0]` 且標為 `attributed`；所有其他八筆與父版相同。確認 `t8` 改指法院 fact 4；`e8/t9` 保留直接 J-Net21 來源與 `fact:5`，該事實只寫律師警告、部分加盟店獨立，沒有把 1978 年版本當作這兩段口播的依據。確認 row/series 的 caveat 明寫本片不口播 1978 年。另逐字核對 `turn-s079` 唯一修改的口播、`t8` 主張和企劃 `turn.point`：從「在元祿之外」收窄為「與原告無關」，符合判決「原告とは無関係」，不暗示所有經營者均在元祿之外。檢查 `sources[3].supports` 只記 P5 被告答辯提及另一第 851953 號權利，沒有捏造該權利的期滿日。逐景 65 筆仍全為 `UNCHECKED`。
4. 查看 `turn-s077` 的 1962 年登錄畫面與 `turn-s079` 的 1972 年後不定日期街景：兩者不可視覺暗示 1970 年代初才登錄、1972 年到期當年即開新店或到期是新店的唯一原因；這只檢查兩個被改動的提示，不等於整集視覺審核。
5. 若法院 PDF 確實經獨立核讀、row 主張精確，而且當前正式工人讀源仍無法擷取 PDF 正文，再為**新 SHA**製作獨立 `reviews/B18.json`，將 `reviewer_only:[4]` 列於新收據；保留 PDF 人工核讀位置與工人無法讀正文的界線。若 PDF 可讀或任何主張不符，依實際證據修正並重新審稿，不要先標 PASS。

這項審查只針對企劃資料列與來源映射。正式六章 worker 查核、聽眾審稿、敘事關卡、實測 TTS、MiniMax 圖、可關閉繁中 CC、成片與站主觀看仍各自待驗。
