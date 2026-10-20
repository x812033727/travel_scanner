# S45｜本地史料與前製驗證（非站台核准）

2026-10-20。這是製作人的**原文自查**，沒有冒充獨立查核員或盲讀者。S45 A/B 大綱、劇本的站台關卡仍待決；未做 `review-push`、語音、插圖、配樂或網站發佈。

## 固定版與凍結稿

- 來源：Nellie Bly, *Ten Days in a Mad-House* (1887)，[GITenberg 固定 commit `c3904b5064d2bafb7e13486489dfe98b560611b5`](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt)。重新下載後為 220,228 bytes、4,320 行，SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`。
- `research.md` SHA-256 `f5d2fd6315fc5693f74ef7ad84f9c30ea238ddaf38e8eec844928480abf6930a`。
- `brief.md` SHA-256 `324fa17e4037debfdcee4ee095cc3703689196a9458a673b79e4c3175890adbb`。
- `video.json` SHA-256 `a17da9c8ddcedc3cad6ac6b89b5431d226fd80bbd2a9b838b3c5133b39a9ca3c`。
- `script.md` SHA-256 `5556eab631e2cb05e7896d1000e6e2a8f3e713663960c76e8581d293ff74b6a2`，由 `node tools/video/cli.mjs script --slug curio-s45` 從同一版 `video.json` 產生。
- `claims.md` SHA-256 `cec26eaab7d45f71154ff287cba6e78e67212e7e7e27eae265d270b6ea87de01`。

## 容易說錯的原文錨點

| 爭點 | 原文直接可核到的文字／位置 | 本稿處理 |
| --- | --- | --- |
| 編輯是否已有保證出口 | Bly 問「How will you get me out」，編輯答「I do not know … but we will get you out」，[第一章 L182–199](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L182-L199)。 | 有接人承諾，沒有預定可保證的辦法。 |
| 是否無人檢查 | 她寫醫師看舌頭、摸脈、聽心、查瞳孔，還問用藥，[第五章 L945–979](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L945-L979)；Bellevue 又有問話。 | 旁白明講檢查，沒有做醫療水準判定。 |
| 9 月 25 日是否已上島 | 書中明寫「Sunday morning, Sept. 25」仍在 Bellevue，[第七章 L1365–1375](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1365-L1375)；「On Monday morning … taken away at 1.30」，[L1477–1505](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1477-L1505)。1887 年日曆 9/26 是星期一。 | 9/25 是 Bellevue；9/26 是登島日。日期由原文的相鄰星期推得，時間線卡註明。 |
| 入院後是否坦白完整身分 | Bly 寫入島後按平常言行，仍「refuse to tell who I was or where my home was」，[第八章 L1681–1685](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1681-L1685)。 | 不說她完全表明身分，亦不把「照常說話」當可診斷他人的證據。 |
| 那封信是何種證據 | 「I saw but one letter given a patient while I was there」，[第十五章 L2867–2870](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2867-L2870)。 | 是她十天裡看見的一封，沒有說全院只有一封，也不說來信是家書。 |
| 如何離開 | 律師 Peter A. Hendricks 告知有朋友願接手照顧；她同意，放行來得比預期早，[第十六章 L3009–3033](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3009-L3033)。 | 說她書中稱院內十天，不補確定放行日期。 |
| 為何再回去，能否算調查證實 | 她說陪審團傳喚、宣誓、要她同行，[第十七章 L3043–3056](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3043-L3056)；又寫廚房、麵包、寢具與洗臉盆差異，[L3114–3128](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3114-L3128)；陪審團報告與百萬美元預算都是她的說法，[L3143–3150](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3143-L3150)。 | 只說「她記載」，不說本片取得陪審團報告、不宣稱全部指控獲證、不採一百萬美元或永久改革。 |

## 本地形式與故事檢查

- `node tools/video/cli.mjs lint --slug curio-s45`：**0 errors / 0 warnings**，估計 9.4 分鐘、98 條旁白（含 3 條片尾）；開場第一章估 47 秒。
- `video.json` 共 95 正文景：**92 張 `shot`（96.8%）、3 張標來源的版型卡**；沒有連續卡片。11 條 `loops` 皆先設伏後回收；每段鉤子間隔通過 45 秒 lint。片頭應由品牌組片設成 `after_first_chapter`，片尾用既有 21 秒 `v4-endscreen`，可點元素要到 Studio 才設定。
- 95/95 旁白句與 `script.md`、`claims.md` 完全一致；95/95 景附固定版來源行號；插圖提示詞未使用 Nellie/Bly 的名字或面貌要求，普通房間、船岸與一名成年人單一動作為主，紙張留白。圖與媒體**尚未生成**。
- 這是自查，還欠一位未參與寫稿者的逐景來源與圖文覆核，及同一個凍結劇本的兩位新敘事盲讀者。若有人要改一字，重新計算劇本雜湊並重做盲讀與站台劇本關卡。

## 下一關

讓獨立查核員只根據固定原文覆核 95/95 句和三張卡，再讓兩位新讀者只讀 `node tools/video/cli.mjs narrative --slug curio-s45 --json` 的旁白與十三題，各自提供可審核證據。兩類查核過關後，仍需走站台 A/B 大綱與劇本的實際關卡；此前不做語音、MiniMax 圖、配樂、`review-push` 或上架。
