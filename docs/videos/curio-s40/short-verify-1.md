# S40 單支直式精華：來源與畫面交接

2026-10-20。文稿為 [shorts.json](shorts.json)，目前 SHA-256 `3ad237565c2cd22e67eed480db913fef90a97375801fa9d45f21a4eebd92b6d6`；六幕、五個不同的長片鏡位、旁白 136 字。`episodeShortsProblems` 零問題，`from-episode --check` 在當時長片 JSON SHA-256 `2523d67d174b416a89eb9831c207ff76199e92c85fb4529bf9e91928101d18a8` 與封存影格 manifest 上通過 selected-file hash。長片修圖中，正式製作前須在**最後選定圖片**上重新執行，不能沿用此暫時結果。

來源為固定版 Plutarch, *Antony*, `674.txt` SHA-256 `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`；[無花果籃、密封信、使者所見](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L61611-L61636)及[異說、不確定性、凱旋蛇像](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L61637-L61659)。這是事後寫成的傳記英譯，不是密室錄音。中文為意譯，未冒稱古希臘原文逐字。

| 幕 | 鏡位 | 逐句來源邊界 |
| --- | --- | --- |
| hook | `cl005` | P-c 寫屋大維凱旋式有附蛇的女王形象；問句沒有把形象當目擊死因。 |
| setup | `cl002` | P-b 寫鄉人讓衛兵看籃內無花果，衛兵准送進陵墓。 |
| turn | `cl048` | P-b 寫女王寄密封信、只留兩位女伴並關門；使者開門發現女王已死。字卡「開門時已太晚」不否認兩位女伴當時仍短暫活著。 |
| proof | `cl058` | P-c 的蛇藏果籃是 `Some relate`，另說 `nor was the asp seen within the monument`；旁白只說**沒人看見**蛇，未說搜遍不見。 |
| payoff | `cl068` | P-c 原句 `what really took place is known to no one`。圖片是沒有名字或可讀文字的泛用古代讀者；旁白明指普魯塔克，沒有把 cl068 的長片狄奧段誤稱普魯塔克原圖。 |
| loop | `cl005` | 回到凱旋像並問它能否替密室最後一刻作證；這是對來源見證能力的提問。 |

獨立來源讀者對初稿六幕主張 PASS，提出三個精確性修正：把「沒人作證」字卡改成「開門時已太晚」、把「沒找到蛇」改成「沒人看見蛇」、把結尾限定為「最後一刻」；另建議以原尺寸 KEEP 的 `cl068` 代替尚未過機器評圖的 `cl082`。現稿已逐一採納；讀者對 exact SHA `3ad23756…` 的四處定點覆核 **PASS**。

**媒體 gate：** 現有 `cl005` 插畫原尺寸仍被獨立審圖判為 HARD（活女王／沒有蛇像，與旁白所說的凱旋雕像矛盾），不能因 `from-episode --check` hash 通過就開拍。等 S40 長片修圖、分鏡／成片真實核准後，先重新檢查此鏡與其他四鏡的 9:16 裁切及選圖 hash，再用頻道聲線建 Short、檢查音質、字幕、QA 與上傳包。長片沒有 YouTube ID，說明欄暫無可放的長片真實連結；不得填占位影片網址或宣稱 Short 已發布。
