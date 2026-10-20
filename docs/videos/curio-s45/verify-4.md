# S45｜R4 敘事與來源修訂候選

2026-10-20。這是撰稿者的**本地自查與精確送審版本**，不是獨立敘事／來源合格判定，也不是站台 `hand_pushed` 大綱或劇本核准。R3 的兩位全新盲讀者均在十三題中得到 11/13，均未通過 `payoffs` 與 `no_recap`；R3 的獨立來源／書面畫面覆核另外要求修 `bly095` 行號。R4 已針對這些具體意見修改，以下檔案須作為**同一組凍結輸入**重查。

| 檔案 | R4 SHA-256 |
| --- | --- |
| `research.md` | `3bdc2f9523a654c687dfcd739f4dac747f62711c55d8c0c6ce30f043353250de` |
| `brief.md` | `6a1c2c16705ca97ba59543947caef615fb5366dd48778d45bec5eecc40557db6` |
| `video.json` | `7c0aa9e9307f5e54038cbfd395b1338884e1f0ee30a04f0281814b5515c5f255` |
| `script.md` | `54a74400fb379bbbb0a713a6fbdd053e6af87956eacfe80ac47aa8a341c31327` |
| `claims.md` | `09f483556bf3f496d9cfd349a2fccbe2bfb179d6aed8d144c19f42714955b7ef` |

`script.md` 由此版 `video.json` 執行 `node tools/video/cli.mjs script --slug curio-s45` 產生。原文仍是 Nellie Bly, *Ten Days in a Mad-House* (1887) 的 [GITenberg 固定 commit `c3904b5064d2bafb7e13486489dfe98b560611b5`](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt)，下載本地檔 SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`。

## R3 的共同敘事問題如何更正

| R3 被問住的地方 | R4 的可驗回答 |
| --- | --- |
| `bly024` 問醫師是否識破她，原文沒有醫師內心或確切判斷 | 改問醫師第一個要求她做什麼；下一句直接說他要她伸舌，繼而檢脈搏、心跳。[第五章 L942–961](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L942-L961)。開場「檢查眼睛」的 `loops` 回收點改綁他實際查看瞳孔的句子。 |
| `bly062` 問會否得到披肩和暖意，原文只有醫師下令 | 改問醫師會怎麼**回應**她重提寒冷；下一段點名 Ingram 並說他吩咐多給病人衣物。[第十三章 L2425–2429](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2425-L2429)。旁白與研究明示醫囑，沒有宣稱衣物實際送達或病人變暖。 |
| `bly078` 問「多久」卻無確定放行日 | 改問院方是否真的放人；後文直接記 Bly 獲釋。她把院內期間稱為十天，但書中未給確定放行年月日。[第十六章 L3009–3036](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3009-L3036)。 |
| 編輯問題到律師到訪恐被讀成同一安排 | 開場改問「萬一進去，究竟怎麼出來」；`loops` 說的是後來離院途徑，並明標律師來源未交代。律師段明說 Bly 沒寫他是否受編輯所託；不把兩人連成一個因果。[第一章 L182–185](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L182-L185)、[第十六章 L3009–3014](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3009-L3014)。 |
| 「十天」連續兩句、餐桌兩次鋪墊、片尾重說日常仍需紀錄 | 信件段改成「在院裡」與「只見一封」，留「十天」在釋放回述卡。[第十五章 L2867–2870](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2867-L2870)。晚餐前第二句改為**無桌布長桌和無椅背長凳**的新事件，[第十章 L1854–1857](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1854-L1857)。片尾改給 Bly 自己的**新動機**：若不能帶給留下者自由，盼促使別人改善其生活，[第十七章 L3043–3048](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3043-L3048)。 |

## R3 行號 HOLD 與其餘來源差異

`bly095` 的「未宣誓同住女性」原本因「宣誓」命中錯誤來源分支，指向 L3039–3070。R4 `claims.md` 改為直接指向[第十七章 L3089–3112](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3089-L3112)。旁白多交代她**自述** Bly 離開後醫師來得較勤，仍然明標未宣誓，沒有當成獨立原始證言。

另補了 Bly 在暗淡後客廳至少等候二十分鐘，[第三章 L314–318](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L314-L318)；第二趟船旁白依原文說舊船「據說」停修，[第十七章 L3066–3068](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3066-L3068)；護士說曾和醫師談過訪查的事，只保留為 Bly 書中記述，[L3070–3073](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3070-L3073)。上述新增內容均不是醫療診斷、陪審團原報告或永久改革證明。

## 本地檢查與下一關

- `node tools/video/cli.mjs lint --slug curio-s45`：**0 errors、0 warnings**。99 正文景、96 插圖景（97.0%）及 3 來源卡；11 條 `loops` 均先設伏後回收。濃縮開頭估 47.9 秒，符合 30–60 秒；仍規劃第一章後插既有片頭，正片後接既有 21 秒 `v4-endscreen`，最後約 16 秒留 YouTube Studio 的影片／訂閱卡位置。
- 99/99 正文句與 canonical `script.md`、`claims.md` 逐字相同，99/99 都列固定版原文行號；新 `bly095` 直引 L3089–3112，片尾動機另在 `claims.md` 註 L3043–3048。
- 正文在 250 spoken units/minute 估 9:29；以較快的 300 估 **8:10**，整段含片尾約 9:48（250），均**不是 TTS 實測**。語音合成後必須量正文；若不足八分鐘，須依來源補寫並重跑敘事、來源與劇本關卡。
- R4 仍待另一位工作者獨立覆核來源與書面畫面，以及**兩位全新、未讀修稿過程者**對精確 `video.json`／`script.md` 做十三題盲讀。站台 `hand_pushed` 大綱／劇本關卡未完成；這份本地 A 案選擇不能冒稱站台核准。語音、插圖、音樂、站台 `review-push`、上架及 Git 提交／推送均未在本階段執行。
