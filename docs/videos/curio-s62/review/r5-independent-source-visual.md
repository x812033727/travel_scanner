# S62 R5｜獨立固定史料與書面畫面覆核

2026-10-22 UTC。**PASS：R5 的史料、逐句主張、書面畫面及 R4→R5 差分。** 我沒有參與本輪作者修改，也沒有讀 R5 敘事盲讀票。本票只涵蓋凍結的文字與提示詞；不是敘事、語音、生成圖片或成片核准。

| R5 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `5d87a5bbaaf69375f941610ee09befdb3e75b29dc1462b115e512448a8cdc24c` |
| `research.md` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` |
| `video.json` | `e7d14243eefff747d94ed2f28193ab93c0af97646b2ff55de935161c7643067a` |
| `script.md` | `2d92a72e535f03b53c70c3aa3b52c218c035c1ee53eb1ca82d3d0a802a6cc091` |
| `claims.md` | `d1f2280234a7f393403e6aa97d36e24e8305d8d5788fbce69c581193b7f3bf36` |
| [R5 結構差分](r5-author-structured-diff.json) | `b420a6bd1a17a4c9420aa102db52d2c7242d2b525a4320bca61e72eb7c1809ed` |
| [R5 文字差分](r5-author-text-diff.json) | `0bb3f01e8854d1667f9b157fe9079f8af041714050bc376c98a14e6d9025d137` |

固定史料是 Galileo 1610 年出版的 *Sidereus Nuncius*，透過 Edward Stafford Carlos 的 **1880 年英譯及編註**閱讀：[GITenberg 固定 commit `6672b6c62a0f30e9bb9b84410ef48c6698c37ea5`](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt)。重新核對本機 raw `/tmp/curio-s62-sidereal.txt` SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。`research.md` 及 `youtube.description` 明列譯者和 1880 年，沒有把譯者註解、後世「衛星」用語或這份英譯冒稱 1610 年原始手稿。

## R5 新寫句的史料核對

- `s62046`：原文 [L1311–1315](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1311-L1315)說 1 月 10 日所見兩點與木星沿黃道同一直線。前一景把被木星遮住的第三點明說是**他的猜測**，沒有移作 1 月 7 日首夜的確證。
- `s62080`：1 月 23 日兩個近點不見，以及作者「我推測」被木星擋住，見 [L1468–1477](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1468-L1477)。新問句只問他如何解釋，下一句 `s62081` 用「猜」回答，沒有假稱知道實際去向。
- `s62083–s62084`：原文 [L1479–1489](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1479-L1489)逐項記下 1 月 24 日第六時辰兩個可見點與木星排成直線，較近點距木星 **3′**、另一點再向外 **2′**；另說先前中間兩點「若我沒弄錯」似乎合看為一點。旁白把新角距當那晚記述，沒有畫成完整現代軌道。
- `s62105–s62106`：書末先承認尚未從這批觀測算出軌道 [L1800–1803](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1800-L1803)，再以最外**軌道**小天體重返相似位置的機會，謹慎試估周期「半個月」[L1820–1826](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1820-L1826)。旁白的「試著」「似乎」「試估」及卡片「作者試估週期」保留這層不確定性；「最外側那點」須理解為作者推想的最外軌道，不應在成片指定某一夜最遠的一點或現代衛星身份。
- `s62111–s62113`：作者邀其他天文學家用足夠準確的鏡筒續定周期見 [L1258–1265](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1258-L1265)。已有最外軌道半月試估，尚無四點各自的精確周期／軌道；`research.md` 新 G15 的限定因此成立。`s62113` 是逐夜相對位置可續查的合理收束，沒有新增觀測結果。
- 研究表 G08 新補的 1 月 16 日東西分布亦直接見 [L1393–1397](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1393-L1397)。其餘未改句與提示詞承接 [R4 獨立覆核](r4-independent-source-visual.md)的已核範圍。

## 書面畫面、差分與時長

R4→R5 的 `video.json` **恰好 13 個 leaf**：8 句旁白、3 個原創插圖提示詞、同一張資訊卡的 `text`／`sub` 兩欄。按結構差分逐葉正向重播得到 R5，反向逐葉還原 R4 `video.json` SHA `abed73ef3b14dcfc1b8ff1804f0234919d2f03cffa70a0b4c901a72ce6b14f92`；JSON 封裝的文字差分抽出後 `git apply -R --check` exit 0。場景順序與其他葉未改。

`s62083–s62084` 的籌碼只象徵兩點拉開和共線，沒有可讀數字或精密比例；`s62106` 用無字夜誌表現反覆比較，沒有假造可讀 1610 手稿。`s62105` 卡片的「1610 年原書」指作者出版的主張，仍須和說明欄列出的 1880 英譯分清。`s62046` 沿用留白圖表提示，與上一句第三點未見相容，但原圖驗收時不可畫成已認出的第三點。後續原圖另須核星點數、現代器件、年代人物、無字文件及卡通畫風。

逐項重驗 **114／114** `video.json` 場景 ID、旁白、`script.md` 和 `claims.md` 的順序與文字完全相同；**133** 個 G01–G15 主張錨點均連到同一固定 commit 的有效行號，每句至少一錨。**110／114 = 96.49%** 是互不重複的原創插圖提示，另四張資訊卡，最多連續一張卡；畫面欄與場景提示／卡片文字逐項相同。官方 `lint --slug curio-s62 --json`：exit 0、**0 errors／0 warnings**、114 lines。

用官方 `estimateTimeline` 另算正文（從第 2 章開始，濃縮開場與固定品牌動畫不補正文）：**250 CPM 10.157 分鐘，325 CPM 8.235 分鐘**；即使扣最後訂閱句，分別仍有 **10.058／8.152 分鐘**。開場另為 47.47／38.37 秒。這是文字預估，實際 TTS 時長及原生圖片仍待各自驗收；本票沒有批准付費媒體。
