# S59 R8｜獨立史料、逐句引註與書面畫面覆核

2026-10-21 UTC。**PASS：只限本表五份凍結稿的史料、逐句引註與書面畫面。**本人不是 R8 作者；先重開固定 D／E／T 原文，再逐一核 `video.json` 的 110 句口播、`claims.md` 的 110 列、`script.md` 對應句，以及 100 條插圖提示詞和 10 張文字卡。本收據不替代敘事雙盲、正式合併、實際生成圖片驗收、旁白或站台媒體核准；未製作付費媒體，未改凍結稿。

| 凍結檔 | 審前及審後 SHA-256 |
| --- | --- |
| `research.md` | `39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d` |
| `brief.md` | `9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3` |
| `claims.md` | `aeb0cd64b8ddeb992e70c3daa813f42d475718e707e82e62f0da4a7684d95f95` |
| `video.json` | `f29d9f55dbea7ee52a19e6c885ed36f26f51b30fc7fe0fa4caa87b7ea9d3a33b` |
| `script.md` | `f0fd2a6069844fe99e994367f3fa8d27b36928231dc0695fd816762c18faf07b` |

## 重開原文與證據層級

- [D：杜蒙塞爾 1878 法文原版](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt)，raw SHA-256 `c48361e94523ebacc000172ebab34895bb20c0b7e458ac3e122f90a3cc9e717c`。本人呈交、失手及數日後重試是一手敘述；[D6999–7024](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6999-L7024) 的腹語對話、失手和秘書室重試經由他引述一名未具名現場人士的報紙來信，不是院方逐字紀錄。
- [E：Dyer／Martin 1910 傳記](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt)，raw SHA-256 `9818547c6dd15e488c1923bad5cc09cb4fa3f447641daaaf77b2f539b4d49d34`。[E5195–5238](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5238) 和 [E5262–5273](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5262-L5273) 是書中明確引出的愛迪生多年後回憶；沒有拿傳記編者 [E5175–5193](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5175-L5193) 的另段概述冒作他的話，更沒有把 E 當巴黎目擊證人。
- [T：杜蒙塞爾 1892 後出英譯](https://github.com/GITenberg/The-telephone-the-microphone-the-phonograph_75683/blob/6b0cda8809aa60bf44270a64853c9aaf9ea5c546/75683-0.txt)，raw SHA-256 `cb9e9fbeee72750d6335413a9f91a450c09b9a40377fbc1c42c7822a79c598c9`。核對 [T7040–7183](https://github.com/GITenberg/The-telephone-the-microphone-the-phonograph_75683/blob/6b0cda8809aa60bf44270a64853c9aaf9ea5c546/75683-0.txt#L7040-L7183) 的機械與試驗用語；它與 D 同作者，且較晚，沒有算作第二名證人。三個固定 raw URL 此次均重新下載並核對雜湊。

## 逐句結果

`s59001`–`s59110` 共 110 個連續、唯一的 ID；三處口播文字逐句相同。`claims.md` 每列至少有一個固定來源錨點，共 124 個 P 引註；P01–P11、P13–P16 都在列中使用，P12 是 E 的出處層級說明。逐段核對如下，**沒有發現缺少引註或超出原文的實質口播主張**：

| 句 ID | 回到原文核的事 | 判定 |
| --- | --- | --- |
| `s59001`–`s59009`、`s59070`–`s59094` | [D6995–7024](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6995-L7024)：日期、呈交、掌聲、匿名來信的腹語疑慮、杜蒙塞爾失手、普斯卡斯在院士指定條件下重試及他們滿意的結果。口播保留「有人／幾位」、來信與本人評價，不宣稱全院表決或列出不存在的條件清單。 | PASS |
| `s59010`–`s59024`、`s59026`–`s59037` | [E5195–5238](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5238)：電報**承盤**的螺旋槽、上覆紙盤的壓痕、電話薄片與紙鋸木人玩具、草圖工價、克呂西製機及初次回放。開頭明說是多年後回憶；沒有把螺旋槽移到紙盤自身。 | PASS |
| `s59025`、`s59038`–`s59055` | [D6683–6694](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6683-L6694)、[D6872–6953](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6872-L6953)：記錄與重播的差別、圓筒/箔/螺旋槽、針的彈簧與橡膠墊、嘴貼話筒、飛輪、壓痕回推薄片和角筒。句子沒有把針說成直接固定在薄片上。 | PASS |
| `s59056`–`s59069` | [E5230–5238](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5230-L5238)、[D6955–6976](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6955-L6976)、[E5262–5273](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5262-L5273)：童謠與編輯室均標愛迪生後來說；轉速、音高、歌聲、鐘錶驅動及錫箔磨損是 D 的一般器械觀察，沒有變成巴黎當日失敗的確定原因。 | PASS |
| `s59095`–`s59110` | [D7035–7049](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L7035-L7049)、[D6978–6993](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6978-L6993)：他自述嘴離太遠、後來練習成功、r/母音與 s 的清晰度差別；倒讀與電話隔開聽者是書中另述，不冒充秘書室當日程序。 | PASS |

四個 R8 重點句另核：`s59030` 的「十八美元草圖」與工價卡直接見 [E5221–5228](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5221-L5228)；`s59033` 的克呂西製圓筒機見 [E5227–5233](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5227-L5233)，「前身」沒有指認巴黎現場的實物為他親造的同一台；`s59078` 是若換人仍發聲便能減少腹語疑問的**推論句**，沒有把它寫成科學院正式實驗目的；`s59080` 的失手同時見匿名來信的 [D7013–7016](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L7013-L7016) 與當事人自己的 [D7035–7041](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L7035-L7041)。

## 書面畫面

100 條 `shot.data.prompt` 與各自口播逐一核對；10 張 `big` 卡均有 `text`／`sub`。`s59011` 標 1910 回憶，`s59072` 標 1878 未具名來信，`s59103`／`s59106` 沒把倒讀或電話驗法畫作秘書室當日操作。`s59030` 只排 `US$18` 和「草圖上的計件工價」；`s59033` 畫匿名工匠裝圓筒；`s59078` 畫交接手柄而未畫驗證成功；`s59080` 畫失手後的安靜機器。這些是原創插圖或排版示意，不是聲稱找到的 1878 照片、原信或原錄音。**書面畫面 PASS。**

一項非阻斷性文字精度提醒：`s59075` 提示詞寫 `blank unsigned letter`。D 只讓我們知道杜蒙塞爾未具名引述來信，沒有證明當年的實際信件無署名；目前畫面是無字卡通道具，口播與卡片也沒宣稱「無署名」，故不構成足以 HOLD 的史料主張。日後若改提示詞，可只留 `blank letter`。`s59004`／`s59073` 畫懷疑者而沒有畫他所看的普斯卡斯面部，是取景省略，未把懷疑原因改寫。

`brief.md`、`claims.md` 的開頭仍以 R4 作者候選描述流程狀態，`research.md` 結尾還寫 P01–P15（表內已有 P16）。這些是凍結文檔的舊流程標籤，不是本次歷史主張或畫面矛盾；本收據的 PASS 只按上表 R8 雜湊生效，不能引用舊標籤判斷現行製作關卡。

## 本地核驗

- `node tools/video/cli.mjs lint --slug curio-s59 --json`：exit 0，`errors: []`，`warnings: []`；110 句，預估 13.3739 分鐘。
- `npm run check:tasks`：exit 0，驗證 2392 張任務票；輸出有其他票的過期持有及重疊 scope 警告，沒有本票錯誤。`npm run tasks -- list --area docs` 可見本張窄 scope 獨立覆核票。
- 本次只讀原始來源及凍結創意檔，沒有生成圖、音樂、配音、成片，也沒有執行付費媒體指令。
