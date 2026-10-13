# curio-l08-v2 查核第三輪

- 查核 2026-10-13，Claude Opus 5.5（獨立查核代理）。我不是這一版的撰稿人，也沒有參與第一、二輪查核；
  這份檔案之外我沒有動任何檔案（`video.json`、`claims.md`、`NOTES.md`、`script.md` 都沒改）。
- 範圍：第一、二輪查核之後，同一天三次改寫（`NOTES.md`〈開場預告 2026-10-13〉〈盲評修正 2026-10-13〉
  〈盲評修正第二輪 2026-10-13〉）造成的每一句新的或改過的旁白，加上刪掉的句子會不會讓留下的旁白、
  標題、說明欄或縮圖失去依據、或彼此矛盾。依據是 `git diff HEAD -- docs/videos/curio-l08-v2/video.json`
  與目前 `video.json` 抽出的全片 138 句旁白。
- 方法：每一句先對 `claims.md` 與 verify-1／verify-2 判 CONFIRMED 的列；碰到人、地、時、數字、歸屬或動機
  有疑問的，回原始來源重讀。當天重開了 S1（TIME 1991 轉載）、S6（Fortean Times 371 訃聞 PDF，pdftotext）、
  S14（1996 訪問第一頁）、S16（Bower 訪問逐字稿）、S18（Women's Weekly Tully）、S19（圈內人自述），
  全部 HTTP 200；User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，
  同一主機間隔至少 1.5 秒。沒有用網路搜尋。

## 改過或新增的旁白

判定：OK＝事實有來源、歸屬與限定語都在；問題＝要改，改法寫在該列。

| id | 現在的旁白 | 依據 | 判定 |
|---|---|---|---|
| `cl1c` | 風景畫家道格和戴夫，喝完最後一杯。 | c1（S1「two land-scape painters」）；「最後一杯」沿用 `cl1b`，verify-1 已判 CONFIRMED（S16「for a pint of beer」、S4「strolled home from the pub … they created their first imitation nest」） | OK |
| `cl1e` | 照圈內人的記述，道格提著鐵棒走進麥田。 | c10（S19 單源）；限定語「照圈內人的記述」跟著鐵棒，沒掉。S16 道格自己也說「my big heavy security bar that was on my workshop door」，是道格的鐵棒 | OK |
| `cl1g` | 他們壓出一個大約九公尺的圓，要像飛碟降落過。 | c4（S6「30ft (9m)」、S19「about 30 feet」，「大約」保留）；動機 c6（S6「make it look as if a flying saucer has landed」；S16「People would think that a UFO had landed in the night」） | OK |
| `cl1m` | 但後來的事，更怪。 | 轉句，不帶事實 | OK |
| `cl1n` | 十幾年後的肯特郡，一位研究者盯著兩人壓出來的圈。 | c13：S1「They had created the Sevenoaks circle while Brough looked on」「Delgado was gazing at a large area」（1991 年九月）。「十幾年後」：起點是 `cl1a` 的七〇年代後半（1976 或 1978），到 1991 是 13–15 年；S1 自己寫「for the past 13 years」。與 `cl1a`、`cl1l`（一九九一年）、`cl7zb`、outro 卡的「十幾年」、`how-many-stats` 的「持續 13 年」都一致 | OK |
| `cl1o` | 再後來，傳說有一位醫生開著小飛機， | c28：S14「it was reported that a doctor in a private plane flew over the field」；「傳說」保留歸屬；1996 在 1991 之後，「再後來」對。「開著」沿用舊 `cl5l`，兩輪都過 | OK |
| `cl1o2` | 約四十五分鐘內，兩次飛過巨石陣旁的田。 | S14「at about 5:30 pm that day and again about 45 minutes later」「On his first pass … on his return」「in a field just south of Stonehenge」；「約」保留 | OK |
| `cl1p` | 而做這些圓的道格，晚年說他後悔一件事。 | 後悔本身有來源（c38，S6「Doug regretted … telling people about it」；「晚年說」沿用舊 `cl7t`，verify-1 已記下 S6 沒寫何時說、保留）。**但「做這些圓的」緊接在巨石陣那個預告後面**，「這些圓」聽起來包含肯特郡那個圈與巨石陣旁的圖形。巨石陣那個不是道格做的（S14b：前一晚三個人做的，第 5 章 `cl5q`–`cl5t` 也這樣講），第 5 章的揭曉又正好是「做圈的不只他們兩個」，這句等於在開場替道格認了他沒做的圖形 | **問題（中）**，見下方 1 |
| `cl2j` | 道格手上那根鐵棒，換成了一塊木板，一公尺多長。 | c10＋c11；回指 `cl1e`（已帶「照圈內人的記述」），內容與舊 `cl2i`＋`cl2j` 相同 | OK |
| `cl2b` | 開頭那個飛碟的主意，是道格從報上讀來的。 | c5／c6：S6「Doug told Dave about the mysterious 'saucer nests' he'd read about in a newspaper」；S16「I suddenly remembered this article … I told him about it and I said we could have quite a bit of fun … People would think that a UFO had landed」。讀報的是道格，不是戴夫 | OK |
| `cl2c` | 他移民澳洲那幾年，讀到一篇報導。 | S16「I saw an article in the Australian newspaper one day, about some circles in some reed and grass in Tully」，又說「this article that I read **while in Australia**」；S6 把讀報的事放在澳洲那一段。在澳洲的年份：S6 約 1958–1968，S16 1966 年回國（八年半）；Tully 事件在 1966 年一月（S18），兩種讀法都落在他住澳洲的期間。旁白不給年數，避開兩源的分歧。「他」緊接 `cl2b` 的道格，指涉清楚 | OK |
| `cl2e` | 報導寫，一九六六年，昆士蘭一個香蕉農說看到飛碟升空。 | c6：S18「On a clear morning in January 1966, banana farmer George Pedley … saw what he described as a flying saucer」，而且這件事「was eventually reported to police and printed in newspapers across the country」「became national news」；S5「a 1966 account of a UFO sighting near Tully, Queensland」。「報導寫」說的是當年全國見報的內容，香蕉農的目擊用「說」保留成他的說法 | OK |
| `cl4k` | 開頭那位研究者站在田裡說，沒有人類做得出這個。 | c13（S1「as he stood in a wheat field near Sevenoaks … "No human could have done this."」）；「開頭那位」回指 `cl1n`，是同一個人 | OK |
| `cl4x` | 那做麥田圈的，真的只有他們兩個嗎？ | 問句，不帶事實；不再暗示第 5 章會回答「木板有沒有去加拿大」（紀錄沒寫） | OK |
| `cl5b` | 做圈的不只他們兩個，那時候田裡已經有別人。 | c24：S6「By summer 1991, others had joined in … way beyond Doug and Dave's capabilities」；S13 Dickinson 第一個圈在 1991 年夏天。「那時候」接第 4 章的 1991 年九月，「已經」對 | OK |
| `cl5l` | 流傳的版本裡，傍晚五點半，那片田還什麼都沒有。 | c28：S14「about 5:30 pm」「On his first pass, the doctor later said, the formation was not there」；「流傳的版本裡」保留歸屬。少了「約」與「傍晚」對七月英國下午五點半偏鬆，都沿用舊句（verify-1 已記下保留） | OK |
| `cl5n` | 開頭那位醫生四十五分鐘後再飛過，圖形就在那裡了。 | c28：S14「again about 45 minutes later … on his return, it was」；「約」在 `cl1o2` 與 `forty-five-minutes` 卡；歸屬由前一句「流傳的版本裡」與開頭的「傳說」承接 | OK |
| `cl7t` | 開頭說他晚年後悔的那件事，是告訴了大家。 | c38：S6「Doug regretted admitting having made crop circles. Not making them, but telling people about it」 | OK |

位置移動但字沒改的 `cl2f`、`cl2g`、`cl2h`：事實照 verify-2（第 9 列等）判的，放在 `cl2e` 之後仍是同一篇報導的內容，OK。

## 刪掉的句子

| 刪掉的 | 還有沒有東西靠它 | 判定 |
|---|---|---|
| `cl1b` | 「最後一杯」併進 `cl1c`；說明欄「喝完最後一杯」仍有旁白對應 | OK |
| `cl1d`、`cl1h`、`cl1j` | 敘事句，沒有東西靠它們 | OK |
| `cl1f`（拴畫框店後門） | 說明欄只寫「提著一根鐵棒走進麥田（圈內人的記述）」，不提畫框店；限定語仍在 `cl1e` 與說明欄 | OK |
| `cl1i`（直徑大約九公尺） | 數字移進 `cl1g`，「大約」保留；說明欄「直徑大約九公尺」對得上 | OK |
| `cl2a2`（1976／78 的分歧） | 留下的旁白沒有一句落在其中一個年份：`cl1a`「七〇年代後半」、`cl1n`「十幾年後」、`cl7zb`「十幾年」都同時涵蓋兩說；`how-many-stats` 的「持續 13 年」標在 TIME 底下。沒有矛盾 | OK |
| `cl2d`（住了好幾年才回英國） | 「回英國」不再明說，但 `cl2c`「那幾年」已表示是一段有結束的時間，`cl2h` 道格把事講給戴夫聽、`cl1a` 七〇年代在英格蘭，沒有矛盾 | OK |
| `cl2i`（還記得那根鐵棒嗎） | 回指移進 `cl2j` | OK |
| `cl5k`、`cl5m` | 小飛機與醫生在 `cl1o` 講過，`cl5n` 點名；「流傳的版本」歸屬移進 `cl5l` | OK |

標題（「為什麼 1991 年兩個英國老先生，承認麥田圈是他們做的？」）、說明欄三段、縮圖（「一塊木板」「都市傳說」
「一九九一年的自白」，畫面 `all-been-conned`）都沒有依賴刪掉的事實。

## 要改的

1. **`cl1p`**（中）
   現在：「而做這些圓的道格，晚年說他後悔一件事。」
   問題：緊接在巨石陣預告之後，「這些圓」把巨石陣旁那個圖形也算成道格做的；那個圖形照片中引的製作者說法
   是前一晚三個人做的，第 5 章的揭曉也是「做圈的不只他們兩個」。
   改成：「而那晚走進麥田的道格，晚年說他後悔一件事。」
   （回指 `cl1e` 那一晚，不新增事實；loop `cl1p`→`cl7t` 不受影響。）

## 懷疑但沒改的

- `cl2c`「讀到」報導的地點只有 S16（次級來源、Bower 本人口述的轉錄）明說「while in Australia」；S6 是從上下文
  推得的。兩源一致，而且 `claims.md` c5 已經收了 S16 那一句，保留。
- 第 2 章的順序：太太發現里程（S16「seven years before my wife really found out」，約 1983 年以後）排在
  `cl2u`「一九八〇年前後，終於有一家報紙寫了」之前。這是改寫前就有的順序，旁白沒有說兩件事的先後，不改。
- `shorts.json`（未追蹤）第一支 Short 的 payoff 場景用了 `which-year` 的畫面，那個場景已經不在 `video.json`；
  `NOTES.md` 已記下要重做。兩支 Short 的旁白仍用舊句（「一個叫道格，一個叫戴夫」「他站在田裡說…」），
  事實本身都對。
- `claims.md` 的索引過期（`NOTES.md` 已列）：c4 仍寫第 2 章說「報導有的寫一九七六，有的寫七八」、c7 仍寫
  「起始年分歧已在 `which-year` 講明」、c10 仍引 `cl1f` 原句與 `nine-metres` 卡的副題，c5 的 `emigrated`、
  c28 的 `the-story-goes` 也已刪除。事實沒變，旁白沒有一句因此失去依據，但下一次動 `claims.md` 時要一起改。

## 結論

18 句改過或新增的旁白，17 句 OK，1 句要改（`cl1p`，中）。刪掉的 11 句沒有讓任何留下的旁白、標題、說明欄或
縮圖失去依據；起始年份「七〇年代後半」「十幾年後」「十幾年」三處互相一致。`cl1p` 照上面改完即可放行。
