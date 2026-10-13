# H06 獨立定點事實覆核，第 2 輪

日期：2026-10-12。覆核輸入是 listener pass 後的 `video.json` SHA256 `CC764D0F3C8077D784BCC124378B6EE7AC2AD1594A7F07FE6768E5D7EA613A61`，106 場、137 句。先讀 `listener-pass.md` 和 `verify-1.md`，再獨立回查法院判決掃描與兩篇 2009 年原始論文。本輪只針對 c05、c06、c14、c15，不重做第 1 輪全稿覆核；尚無實際音訊或影片可驗。

## 結果與必要修正

| 主張 | 原始來源直接核到的範圍 | 稿件結果 |
| --- | --- | --- |
| c05 民事請求 | [III ZR 139/67 判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) **PDF 第 13 頁、紙本第 12 頁**明列最後的三項請求：給付款項及利息；確認她以沙皇幼女、四名手足唯一生還者身分，成為位於原德意志帝國境內的遺產唯一繼承人；確認 1933 年原繼承證書有誤。PDF 第 3 頁是 Revision 駁回主文，第 5 頁是財產背景。 | `court-question-card/fba5` 和 `court-read-three-places/kvx5` 的白話概述保留；`claims.md c05`、`research.md S1` 原將三項訴請誤引為 PDF 第 3–5 頁，已改為第 13 頁。`德國境內` 是口語概括；研究筆記補出「原德意志帝國境內」的原判決限定。 |
| c06 法律審 | 同一掃描 PDF 第 3 頁駁回 1967 年漢堡高院判決的 Revision；第 143 頁討論前審是否違法行使程序裁量，並說明其餘程序異議經審查而無理由；第 144 頁維持前審「證據未證實她是安娜塔西亞」的結論。 | `court-two-years/i2rk` 改為「一九七〇年，最高法院駁回法律審；它檢查前審有沒有法律或程序錯誤。」與後續 `court-two-levels/mrsj/qyt5` 的證據衡量／法律程序區分一致。不說最高法院重問所有證人，也不把未證實公主身分改寫成判定她的另一個本名。 |
| c14 第二墓的姊妹 | [PLOS ONE 2009 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) 摘要及 Discussion 明確認出第二墓為一男一女、兩人屬於尼古拉二世夫婦的子女；Discussion 也明說本篇報告的 DNA 結果不能解決女兒是 Maria 還是 Anastasia，缺少每位姊妹個別的 DNA 參照。其表格個別人名有沿用人體測量學的慣用標記，不能拿標記推翻正文限制。 | `grave-two-children`、`grave-which-sister/ce8r/zwkk` 與字卡正確區分家族歸屬和姊妹個別墓位；不改稿。 |
| c15 五名子女 | [PNAS 2009 原文](https://www.pnas.org/doi/10.1073/pnas.0811190106) Abstract 及 Interpretation of the Data 明列兩墓樣本為父母、四女一子，作者結論為五名子女均已被辨認、無人於處決中生還。PNAS 網頁閱讀器可讀相關段落；直接 `curl` 曾回 403，故不將命令列抓取記為成功。 | `grave-two-papers`、`grave-five-children/ufh6` 只說兩墓合起來找到五名子女，未用 PNAS 圖表的暫定人名替第二墓女孩下定論；與 c14 同時保留，不改稿。 |

判決 PDF 為第三方保存的 144 頁法院判決掃描，已核本地檔 SHA256 `4D76213991CBC8F698B85FCB88E5FB8364E2E99701B3828FF51256D4AA313E59`，並對照第 3、13、143、144 頁頁面影像；其 OCR 有破字，頁碼與訴請依影像判讀。對 Revision 的說明是依該判決審查內容作給一般觀眾的概述，不是逐字翻譯法條或法院對全部案件的普遍規則。

`verify-1.md` 第 1 輪表格 #07 的 PDF 第 3–5 頁是歷史覆核紀錄，應以本報告的第 13 頁定位為準，不改舊報告。仍待製作端同步的活文件：`listener-pass.md`「訴請過於抽象」列錯寫第 3–5 頁，`brief.md` 第 27、93 行的已目視頁碼清單漏了第 13 頁。這兩份由主製作端接手，避免雙人同時改檔。

本輪修正：來源定位 1 組、旁白白話化 1 句；四項定點主張未發現其他需更改的實質事實。`video.json` 保留原 scene/line ID，完成後 SHA256 `85B97B34A73E84AC5687DDFE75DECD530709972471D3F2A3B12901B4B192FF41`。`node tools/video/cli.mjs lint --slug curio-h06`：**0 errors、0 warnings**，估時 10.7 分鐘、137 句。這只確認腳本結構，不代表旁白、畫面或成片已通過。