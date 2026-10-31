# S49 R26｜第二章首八景中六個提示詞窄修

2026-10-22 UTC。這是作者候選，**待非作者重新紙審八景；沒有付費試圖**。[R25 八景獨立紙審](r25-next-chapter-eight-prompt-independent.md)確認 `moon032–039` 的固定來源／逐句主張 8／8 PASS，但只有 `moon033/039` 的提示詞 PASS；其餘六景有把虛構光學方案畫成真器材、後世工程圖、未定年代實驗室與少年讀者等風險。R26 只修這六景的 `data.prompt` 及 [claims.md](../claims.md) 同列畫面欄；`moon033/039`、全部台詞、劇本、研究、章節、運鏡、卡片與先前首章都不動。

| 景 | R26 畫面改法 |
| --- | --- |
| `moon032` | 成年 1835 讀者看一張無字、扁平的物鏡圓／暗室方形概念墨線；沒有已架設的高處器材。 |
| `moon034` | 兩名 1830 年代成年人看單頁兩個明暗不同的簡單圓，表示倍率增高時光少的討論；沒有真望遠鏡實測。 |
| `moon035` | 成年讀者帶疑問手勢，看單頁無字焦點點與兩道鬆散光線；非真設計圖。 |
| `moon036` | 兩名成年人的木桌討論，其中一人在無字白紙畫簡單 V 形入射角；不是現代實驗室。 |
| `moon037` | 成年角色從木椅急起、面向另一成年人，承載虛構 Brewster 反應；不以鏡片圖冒充成果。 |
| `moon038` | 1835 成年讀者拿無字折紙露出疑問神情，承載「真的解決了嗎」；無學生、對話框或原報複製。 |

[逐字可逆結構差分](r26-next-chapter-six-prompt-structured-diff.json)記錄每格 prompt 與 claims 整列前後文。R24 `video.json` SHA-256 `98e00e94079f0725068ecdc44be124934fc69540c0d9be62a0c8340d2222d13c` → R26 **`57027ce7870f736e8662b6774ed4f6e85922d153e6ac864fb8a9ca1cf389ca22`**；`claims.md` `e6a8115bc1b9c14078e99059b836cb6d15027f67fe073671de1daa45d9d54190` → **`ced02136c94ec5f93f34a62ad5bddfd635b8fde8af93297cff531f91ae40bbcc`**。六項 `new→old` 回填逐位元還原 R24 雙檔；JSON 遞迴比較只變 `scenes[28/30/31/32/33/34].data.prompt`，claims 只變第 35／37–41 行同列畫面欄。`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 不變。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` exit **0**、**0 errors／0 warnings**、131 句；[stdout](r26-next-chapter-six-lint.stdout.json)、[stderr](r26-next-chapter-six-lint.stderr.txt)、[exit](r26-next-chapter-six-lint.exit.txt)同目錄保存。修稿後沒有碰私人媒體：現行 manifest SHA `4f40a7ad117ed6393b4fea39e4cfbd206ee0312b1c6c9b25ba8e3bc48e72c611` 仍保留首章 26 張已驗收圖，卻尚綁 R24 視覺稿；R26 提示詞只影響八張未畫景，下一次繪圖前須安全重綁並核先前選圖。ledger SHA `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`，**US$0.9990／74 image／74 judge／0 預約**，低於整集 US$5.30，`STOP` 在位。本輪零新圖、零 judge、零音樂；第二章及全片分鏡、網站卡、人耳與成片皆未獲核准。
