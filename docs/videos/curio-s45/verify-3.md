# S45｜R3 來源修正與送獨立覆核候選

2026-10-20。這是 R3 撰稿者的**本地修正紀錄**，不是來源查核員的合格判定，也不是站台大綱／劇本核准。R2 精確版本收到獨立來源／書面畫面 **HOLD**；覆核報告 `/tmp/s45-r2-source-independent.md` SHA-256 `a8bcb4a8999890a8baf34a680d250d5ab2115e827920e120b4294efb66c3ff15`。R1、R2 的任何審閱結果都不能代替 R3 的新審閱。

## R3 凍結稿

| 檔案 | SHA-256 |
| --- | --- |
| `research.md` | `1b25c7025a0d11dab9cf999e0a7ec84d2a92a7f06984c665670c7e2545fd2f5f` |
| `brief.md` | `85f1e65f0b33774d3d8ea06fd05979b3d8bbef42b469c44528d6fc6259cba005` |
| `video.json` | `b292150dcec1563877f292ba8ef7fdd5948c41acd1a967c4e722d0418410fa8c` |
| `script.md` | `892494e434a2c4704d4f1e2dc74c37e780ef12a7422dab37d99c338f04a530e2` |
| `claims.md` | `3712f080c243f8e38dbbbb87e2f8ab71ad83329dfc02d9f56ed0d98a1722cfe8` |

`script.md` 是由本版 `video.json` 執行 `node tools/video/cli.mjs script --slug curio-s45` 的輸出。唯一用於敘事的原文仍是 Nellie Bly, *Ten Days in a Mad-House* (1887)，[GITenberg 固定 commit `c3904b5064d2bafb7e13486489dfe98b560611b5`](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt)，本地 SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`。

## R2 HOLD 逐項更正

| 爭點 | R3 處理與固定原文位置 |
| --- | --- |
| `bly027`「只說」抹掉其他回答，且引用範圍錯 | 改為她仍假扮，同時說自己沒生病、想找行李與回家；逐景引用直指[第五章 L945–985](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L945-L985)。不說她只講行李，也不把她的說法當獨立診斷。 |
| `bly033` 把醫師的「牆上人臉」改成影子 | 改為醫師問「牆上有沒有人臉、周圍有沒有聲音」；[第七章 L1397–1405](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1397-L1405)。 |
| `bly047` 誤讓醫師量身高、畫成文書職員 | 旁白區分醫師先問、護士調整量尺、醫師最後讀數字；插圖只畫一位成年護士調整量尺；逐景引用[第九章 L1694–1750](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1694-L1750)。 |
| `bly029` 讓 Bly 自己拉窗簾 | 改為一位醫師在急救車內放下窗簾；[第五章 L1013–1019](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1013-L1019)。 |
| `bly055` 畫立式鋼琴 | 改為舊式方形鋼琴；她曾被安排坐在此鋼琴前，[第九章 L1775–1780](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1775-L1780)，晚餐後彈奏而另一名女性唱歌，[第十章 L1894–1897](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1894-L1897)。 |
| `bly068` 畫 Bly 拿信歸檔 | 改為一位成年病人望向病房門，不推定 Bly 拿過信；原文只說她見**一封信交到病患手裡**，[第十五章 L2867–2870](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2867-L2870)。 |
| `bly093` 對新盆、床鋪的推論引錯段落 | 逐景引用改為[第十七章 L3114–3120](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3114-L3120)；「一次返訪不能確定何時更換」仍明示為由有限觀察導出的界線。 |

另外刪去 `bly015`、`bly018` 來源未證的實體行李道具；`bly090` 與 `bly095` 的護士／同住女性問話改在普通島上病房，不暗示法院另有聽證室。`bly095` 旁白仍稱該同住女性**未宣誓**，見[第十七章 L3089–3110](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3089-L3110)。`loops` 把編輯疑問的回收改成「後來的離院途徑；律師來源未交代」，`brief.md` 改成律師**來訪並提出友人照護，她後來獲釋**；[第一章 L182–185](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L182-L185)與[第十六章 L3009–3033](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3009-L3033)沒有交代誰聯繫律師。新圖稿也都明寫一位成年人／成年角色，避免年齡不明的人物；不要求 AI 畫可讀紙件或有名者肖像。

## 本地驗證與未過關項目

- `node tools/video/cli.mjs lint --slug curio-s45`：**0 errors、0 warnings**。99 正文景，96 張插圖景（97.0%）、3 張來源卡；11 條先設伏後回收的 `loops`。第一章濃縮開場估 47 秒，片頭仍需接在第一章後，片尾仍規劃既有 21 秒 `v4-endscreen` 與 Studio 可點影片／訂閱位置。
- 程式比對 99/99 景旁白與 canonical `script.md`、`claims.md` 逐字一致；99/99 逐景列有固定版原文行號。核對了上述三筆關鍵行號、96 張插圖都描述一位成年角色，並掃描無行李箱、立式鋼琴、獨立聽證室、Bly 持信歸檔等已知失實元素。
- 正文估計 9:26（250 spoken units/minute），以較快 300 units/minute 估計 8:07，仍**不是實測 TTS**。若後續實測正文短於八分鐘，需依來源補寫並重跑查核與劇本關卡。
- **仍待 R3 獨立來源差異／書面畫面覆核與兩位全新盲讀者的十三題敘事檢查**，之後才可送站台 A/B 大綱和劇本核准；語音、圖像、配樂、`review-push`、上架與 Git 提交／推送均未由本工作者執行。
