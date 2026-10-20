# S45｜R2 前製候選與來源差異自查

2026-10-20。此檔保留 R2 **送審前**的精確候選。`verify-1.md` 所列 R1 曾通過獨立來源／書面畫面覆核，但兩位新讀者各自判定章節銜接、問題回收和重複解說不合格；R1 的來源覆核與盲讀結果都不自動沿用到 R2。以下是撰稿者對 R2 的本地自查，**不是獨立來源核准或站台 A/B／劇本核准**。

## 凍結檔案

| 檔案 | SHA-256 |
| --- | --- |
| `research.md` | `936df434ed854e2486eaaccbaac0afc9445c70feba0293d971179f50899225f2` |
| `brief.md` | `48a8466a5f457305cba5e4fb3a6cfc86ba9fb67519cacf86b8b3d35432a39591` |
| `video.json` | `fea704c8135296b97c384fc74124d8e3f995addaf1e164a7756b73655f9fcae3` |
| `script.md` | `49cd87abd4300f58b54ec419636105014ed175342eff6ca123dd744397e87a35` |
| `claims.md` | `5d208a3363a470bf97554bd28e8e2e873cc17b12885ab009ea68de7df5d7d432` |

`script.md` 由 `node tools/video/cli.mjs script --slug curio-s45` 從同一版 `video.json` 重新產生。固定原文是 Nellie Bly, *Ten Days in a Mad-House* (1887) 的 [GITenberg commit `c3904b5064d2bafb7e13486489dfe98b560611b5`](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt)；本地原文 SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`。**9 月 25 日仍在 Bellevue，星期一 9 月 26 日才轉往島上**，見[第七章 L1365–1375、L1477–1505](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1477-L1505)。

## R1 盲讀問題如何修

| R1 問題 | R2 具體修訂 |
| --- | --- |
| 章尾問出口，下一章卻先進安靜病房 | 安靜病房與後期不得見訪客留在前章；章尾問「仍在等出口的她，會等到誰？」；下一章**第一句**即律師來訪。 |
| 編輯與律師被暗示有未證因果 | 保留編輯沒有確定辦法與律師提出友人照護；旁白明說「書裡沒說他是否由編輯找來」。 |
| 船上其他乘客知不知道目的地、誰能替兩趟作證、陪審團離開後平常是哪種麵包，皆無來源答案 | 船上問句改為 Bly 最後下船；德語女性的問句改問醫師是否理解並以臨時翻譯回答；返訪問句由**Bly 書中一位未宣誓同住女性的話**回答；結尾不用無法回答的麵包問句，改說第二次所見不能代替其後每日紀錄。 |
| 十天限定、返訪麵包、片尾重述過近 | 各只說一次；片尾改以「同一見證者能比較兩次，往後日常仍需更多紀錄」作來源範圍的結論。 |
| 晚餐章是三個主題的目錄；歌與信拖慢路線 | 章名換成事件「那一晚，她沒吃下晚餐」；歌只留一句以保存人的日常，信仍回收濃縮開場。 |

## R2 新增或改動的原文錨點

下列爭點可在固定 1887 原文直接重看；每一段旁白的行號亦在 `claims.md`。本集未取得其他病患診斷、醫院原始記錄、陪審團原件或後續追蹤資料。

| 爭點 | 原文直接可核內容 | 本稿界線 |
| --- | --- | --- |
| 約七十美分 | 她說只帶「about seventy cents」，錢用完可能促使住處請她走，[第三章 L325–336](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L325-L336)。 | 說「約」而不寫確定金額；是她策略的回述。 |
| 法庭先問暫留，再檢查 | Duffy 先問女子暫住處能否再留她；她怕被送回，接著隨車醫師查舌、脈、心跳、瞳孔並問藥，[第五章 L932–985](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L932-L985)。 | 校正事件順序，絕不說「沒有人檢查」。 |
| Bellevue 第二次身體動作檢查 | 星期日午後 Field 醫師要求伸手、動手指，[第七章 L1451–1456](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1451-L1456)。 | 只述動作，不替當時檢查作現代診斷判斷。 |
| 德語女性的問話 | 有人被請來轉譯，最後只問出丈夫的職業；Bly 隨後決定照常舉止但繼續隱瞞姓名與住處，[第八章 L1644–1685](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1644-L1685)。 | 不下其他病患診斷、不說全無問診或 Bly 完全坦白。 |
| 餐後病人做事與筆記本 | Bly 寫有人鋪床、有人清掃；她帶的筆記本與鉛筆被拿走，要求歸還未成，[第十一章 L2137–2165](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2137-L2165)。 | 畫面為普通房間、一名成年人物；不重演具體傷害，紙件無生成可讀字。 |
| 信件的來源與作用 | 她只見一封信交到病患手上，眾人圍來問話；沒寫寄件人，[第十五章 L2867–2870](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2867-L2870)。 | 開場與回收都問**為何**受注意，不問未知的誰寄來；「只見一封」不是全院統計。 |
| 求離開、換病房、律師 | 她寫多次請求離開，談後被換往安靜病房，[第十六章 L2929–2964](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2929-L2964)；又寫後期不得見訪客，律師以友人照護提出接走，[L3009–3034](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3009-L3034)。 | 不補編輯找律師的因果或確定釋放日。 |
| 返訪的不同層次 | Bly 寫陪審團問護士而聽到相異說法，[第十七章 L3070–3075](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3070-L3075)；一位同住女性**未宣誓**而說 Bly 離開後衣物和餐食變了，[L3089–3110](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3089-L3110)；乾淨廚房、展出麵包、床鋪與新盆是她的返訪描寫，[L3114–3120](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3114-L3120)。 | 不把未宣誓話語說成宣誓證言；**她沒說第一次看過廚房**，只說展出麵包與吃過的不同；陪審團報告與長期改革未獨立核對。 |

## 本地形式驗證與下一關

- `node tools/video/cli.mjs lint --slug curio-s45`：**0 errors、0 warnings**。99 正文景 + 3 句片尾，96 個插圖景（96/99 = 97.0%）、3 張來源文字卡；無連續卡片。11 條 `loops` 均先設伏後回收，30–45 秒鉤子節奏通過本機 lint。
- 程式比對 99/99 正文句與 `script.md`、`claims.md` 完全一致，99/99 都有固定版原文行號；插圖提示詞均避開人名與可讀生成紙件。第一次與返訪船景已改為普通**木製河船甲板**提示，需在實際出圖前看原尺寸圖。
- 正文估計 9:21（預設 250 字單位／分鐘）；以較快 300 單位／分鐘估計為 8:03。這**不是實測語音時長**，後續 TTS 要再量正文是否確實至少八分鐘，未達則依來源補寫並重跑門檻。
- 第一章濃縮開場估 47 秒，之後才接既有 5 秒片頭；正片後規劃既有 21 秒 `v4-endscreen`，最後約 16 秒預留 YouTube Studio 可點影片／訂閱位置。可點元素需完成私人上傳後設定，不能宣稱已可點。
- 下一關：另一位工作者逐景核 R2 原文與書面畫面，**兩位未見 R1 意見的新讀者**對這個精確 `video.json`／`script.md` 做十三題盲讀。兩類覆核過關後才進站台 A/B 大綱和劇本核准；未做語音、MiniMax 圖、配樂、站台 `review-push`、上架或 Git 推送。
