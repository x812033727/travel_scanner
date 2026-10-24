# S49 R26｜第二章首八景非作者書面覆核

2026-10-22 UTC。對 [R25 八景 HOLD／PASS 回條](r25-next-chapter-eight-prompt-independent.md)後的 R26 作者凍結作差分重審。**固定史料與逐句主張 8／8 PASS；現行 `moon032–039` 八個提示詞 8／8 書面 PASS。** 這只放行八張受控原圖測試，不是原生圖、整章或整集分鏡通過。

## 精確綁定

- R26 `video.json` SHA-256 `57027ce7870f736e8662b6774ed4f6e85922d153e6ac864fb8a9ca1cf389ca22`、`claims.md` `ced02136c94ec5f93f34a62ad5bddfd635b8fde8af93297cff531f91ae40bbcc`。`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 不變。CLI lint exit 0、0 errors／0 warnings、131 句。
- 獨立以 [作者結構差分](r26-next-chapter-six-prompt-structured-diff.json)逐一核 `before/after`：解析後只六個 scene 的 `data.prompt` 變動（`moon032/034/035/036/037/038`），`moon033/039` 及全部其餘 scene、台詞、運鏡、章界不變；claims 只改這六列畫面欄。將六項 `after→before` 逐字逆放後，`video.json` 恢復 R24 SHA `98e00e94079f0725068ecdc44be124934fc69540c0d9be62a0c8340d2222d13c`，`claims.md` 恢復 `e6a8115bc1b9c14078e99059b836cb6d15027f67fe073671de1daa45d9d54190`，與 R24 分支原檔相同。
- 重開固定 L（1859 重印本，原文 SHA `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`）[L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)及 J（1902 Jacoby，原文 SHA `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`）[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)。兩者使「無鏡筒高物鏡／暗室反射、光量、人工照明、入射角、Brewster 起身、蚊幼蟲比喻」均限於虛構報導，不能畫成 Herschel 真器材或實際月球實驗。

## 八景結果

| 景 | 結論與紙面依據 | 原生圖必查 |
| --- | --- | --- |
| `moon032` | **PASS**。1835 成年讀者看單頁無字扁平物鏡圓與暗室方形，呈現虛構構想，撤掉 R25 的已架設高鏡。 | 不得變成立體已建高架、真天文台、原件工程圖或可讀字。 |
| `moon033` | **PASS，提示詞未變**。想像 1830 年代成年學者、暗室素面反射鏡與 L 的對話一致。 | 拒絕現代工作室／白袍、孩童、已建巨鏡。 |
| `moon034` | **PASS**。兩個明暗不同的無字圓只作光量下降的概念對照，撤掉真望遠鏡目鏡；成年 1830 年代人物明確。 | 不得變成實測紀錄、現代儀器或相互矛盾的量測數字。 |
| `moon035` | **PASS**。成年讀者對單頁無字焦點與鬆散光線墨線提出疑問，沒有後世設計圖／控制器。 | 墨線須維持抽象概念，不可像原件或可讀公式。 |
| `moon036` | **PASS**。成年 1830 年代人物在木桌畫無字 V 形角度，符合「折射、入射角」的虛構對話；撤掉未定年代實驗室。 | 不得出現白袍、現代設備或把討論畫成已做實驗。 |
| `moon037` | **PASS**。成年人物從木椅急起面向另一人，對應 L 的虛構 Brewster 反應；撤掉宣稱結果的鏡片圖。 | 拒絕少年／現代服飾、多肢體，以及不合 1830 年代的椅室。 |
| `moon038` | **PASS**。1835 成年灰髮讀者拿無字折紙而疑問，承載 Jacoby 對光學詞語拼貼的懷疑；無學生或漫畫對話框。 | 折紙不能像可核驗的《太陽報》原版，也不可生成可讀字。 |
| `moon039` | **PASS，提示詞未變**。L 以蚊幼蟲水滴作顯微鏡比喻，旁白明說是作者拿來打比方。 | 拒絕孩童、電子顯微鏡、白袍，以及把幼蟲當真月面發現。 |

八景均在 R24 `moon031` 來源字卡後同一章「不存在的巨鏡被寫得像工程記錄」，按目前場景順序最先未畫，沒有跳過來源或換題。上表是書面意圖，不可用機器 judge 分數代替 1280×720 原生圖與裁圖的歷史、人物年齡、字樣、邊框逐張驗收；若相近故障連續出現，依 STOP 規則停批窄修。

## 私人圖單與付費界線

現行 manifest SHA-256 `4f40a7ad117ed6393b4fea39e4cfbd206ee0312b1c6c9b25ba8e3bc48e72c611`，其中 26 張先前 KEEP 的選圖檔 SHA 全部再核相符、`moon031` 退圖已移除；其 `visual_hash=30ca7d69acc3fc9a` 尚綁 **R24**，R26 應為 `5781d6810538eb41`。在任何下次繪圖前須安全重綁，保留 26 張原圖／judge 結論，不可借舊 binding 宣稱 R26 全片 storyboard ready。全片 120 張 `shot` 尚有 **94 張**未畫（包含本八景）。ledger SHA `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`，**US$0.9990／74 image／74 judge／0 reservations**，低於 US$5.30；`STOP` 在位。本輪沒有媒體呼叫或費用。
