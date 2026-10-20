# S24 單支 Short：喊聲留在書頁，現場證詞仍缺

2026-10-20 零付費前製。長片的精確 `script.md`／`video.json`／`claims.md` SHA-256 分別是 `2ab08047be6dbc800ef54f02b6e9321518324f9ce8e0aaea0265430242c724af`、`59624d323f19dc99bb04de6ded3e2c118b00dd11c7bf0727cfc37fae710302d7`、`84242d5002e782e6f7b6a430f3229b3906e42ec5632621cea14a562cc2640069`。本集 [shorts.json](shorts.json) SHA-256 `cf930fc1097c4e292a36d11ca380bb7ecbab5f928be891c9c6254fe9da341329`，只含 `curio-s24-short-1` 一支 `from-episode` 候選。文稿由本次撰寫者逐句對照既有長片及下列已固定原文；這是**撰寫者自查**，並非獨立成片審核。

| 短片景 | 長片插圖鏡位 | 來源與界線 |
| --- | --- | --- |
| hook | `crown-031` | 問阿基米德是否真喊；不把街景卡通當成現場證據。 |
| setup、turn | `crown-024`、`crown-030` | 維特魯威後來記入浴見水溢、奔回家連喊希臘語；每句明示這是書的敘述。 |
| proof | `crown-083` | 拉丁原文直接保留 `ευρηκα ευρηκα`；不可說英譯者發明此語，也不讓生成插圖畫假希臘字。 |
| proof | `crown-087` | 英譯與拉丁本是**同一作品**，不能冒充兩份目擊證詞。 |
| payoff | `crown-089` | 作者未交代哪位在場者是消息來源；只說目前不能證實喊聲，沒有斷言阿基米德從未喊過。 |
| loop | `crown-031` | 回到開場的兩聲，要求獨立證詞；不要求觀眾訂閱或點連結。 |

固定英譯全文 `/tmp/vitruvius-20239.txt` SHA-256 `7daafe23aeef2377fe9a99bc285c5dfc0673440487ab43f78387312b6799304d`，第 [8027–8033 行](https://github.com/GITenberg/The-Ten-Books-on-Architecture_20239/blob/67fd1f31ae255b0f32efe423a950203d9b25bbe8/20239.txt#L8027-L8033)；拉丁全文 `/tmp/vitruvius-latin-51812.txt` SHA-256 `b4fce89b0c304c7d1f26b299bf2dfcddbab8529c883f43ad1e75fae564daa861`，第 [27286–27292 行](https://github.com/GITenberg/Vitruvii-De-architectura-libri-decem_51812/blob/78eb1eed88044d5cac42a3dd811d5806e4e04cfb/51812-0.txt#L27286-L27292)。二者是同一位作者的兩種文本，不作互相獨立的史證。

格式預檢：Short `validate`、Curio 單支 `episodeShortsProblems`、六拍 `scriptGrammarProblems` 均 **0 問題**；7 景、7 句、127 個含標點字元，第一張 headline 7 字，最長一句 22 字。依同系列約 140 字草稿的預估，約 30–40 秒，正式須以頻道聲線實測 25–55 秒。無來源影片 YouTube ID，Short 說明欄未填占位連結；離線 metadata 只報「長片尚無網址」，其他字數／標籤檢查通過。

`from-episode --check` 目前以 `no keyframes/manifest.json` 停止：S24 尚未購買插圖，故沒有選定影格或 9:16 實際裁切可審。待長片音訊／圖片與成片關卡完成後，用**最新選圖雜湊**重跑、檢視原尺寸與直式安全區，再製作旁白、字幕、QA 與上傳包。此草稿沒有呼叫 TTS、生圖、配樂、網站送審或 YouTube 上傳。
