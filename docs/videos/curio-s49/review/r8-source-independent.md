# S49 R8｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS：R8 三句新旁白、相應主張錨點與 `moon122` 書面提示詞。**本結論只適用於下列精確 R8 檔案，承接 [R7 獨立來源／書面畫面 PASS](r7-source-independent.md) 中未改動的內容；不代替兩名全新 script-only 讀者的十三題敘事關卡，也不核准政策、網站劇本卡、TTS、生成插圖或成片。我未參與 R8 撰稿，直接重讀固定 L／J 的原文、三句上下文、`claims.md` 與對應 `video.json`。

固定 L 是 Locke 名下 **1859 重印本**，本地 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`；J 是 Jacoby **1902 後出評論**，本地 `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。兩者都不是已核對的 1835 原報影像。J 引用的報紙反應與 L 的選錄重合，不構成另一份獨立原報見證。

| R8 景與逐字旁白 | 原文與主張裁決 | 書面畫面裁決 |
| --- | --- | --- |
| `moon005`：「報導還留下一道望遠鏡的光線難題；紙上的人會怎麼解？」 | [L 390–460](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L460)把高倍放大缺光及藉顯微鏡注入「人工光」寫進虛構的 Herschel／Brewster 對話；[J 4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)明指它是無法解釋的光學術語拼貼。新句以「報導」「紙上的人」限定來源，未預先給出 `moon048` 的倍數或物件答案；**PASS**。 | 沿用 R7 無字望遠鏡草圖與讀者提示詞，沒有把虛構巨鏡畫成真器材；**PASS**。 |
| `moon013`：「《太陽報》卻替他換了觀測目標：從南天星空，變成月球。」 | [J 4050–4080](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4050-L4080)區分 Herschel 真實的南天研究與《太陽報》捏造的月面發現；[L 168–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L168-L254)確實把其真名放到虛構月面主張裡。「替他換」的主語是報紙，沒有說真正的 Herschel 改了工作；**PASS**。 | 沿用 R7 的 1835 年報攤讀者比較**無字**星圖與展開報紙；這是觀眾的卡通想像，並未標成原報照片或真儀器；**PASS**。生成時仍須驗收畫面不冒出可讀的假標題。 |
| `moon122`：「不能。把這則反話算進支持票，就會把重印本的選錄讀錯。」 | [L 2055–2193](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2055-L2193)把《晚郵報》翼人與虛構遊記 Peter Wilkins 並舉，放在 1859 重印本的反應選錄中；[J 4177–4215](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4177-L4215)明說 *did not fall into the trap*。新句回答 `moon121`，而且明說「重印本的選錄」，沒有把諷刺算作獨立的贊同票；**PASS**。 | 新提示詞：`Close shot in a quiet study, one historian slides a single blank paper cutout away from an open reprint book, mild window light`。這是單人移開**無字示意紙片**，不冒稱 1835 原報剪報、也不把諷刺當歷史證物；`claims.md` 同景說明與 JSON 一致；**PASS**。 |

機械覆核：`video.json` 有 133 個編號景（126 `shot`、7 `big`）及片尾，**136/136** 台詞與 `script.md` 同文同序，**133/133** `claims.md` 行的 ID／台詞與 JSON 同序，**126/126** shot 提示詞和 **7/7** big 卡三欄對齊。場景和台詞 ID 唯一；11 組 loop 的 setup／payoff ID 均存在。`lint --slug curio-s49 --json` 回報 **0 errors／0 warnings、136 lines**；`git diff --check -- docs/videos/curio-s49` 通過。依 `spokenUnits` 函式另算：開場前八景 176 units，325 units／分鐘下約 **32.49 秒**；正文 2,693 units，同速約 **497.17 秒（8:17.17）**。這是文字估算，不是媒體實測。

| R8 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `a010434fbbb2e498f6d064557b58e11cea338ccf93fc6300ab5960444f9e25e1` |
| `script.md` | `f40259db7e16da37652689f0e2d703b8e03b8364d1738d0b4c2f848043618c8b` |
| `video.json` | `1eaec3a24e656fe86e0cc5f48e5d61fa3a690b18aa7f4621960aa85f14f60baa` |

下一關是兩名未參與修稿、只讀此精確 `script.md` 與固定十三題的全新讀者各自判票，再正式合併。R7 的敘事票不可沿用。
