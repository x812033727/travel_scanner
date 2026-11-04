# sothatswhy-p02-cloud-rain 八語字幕與上架文字審稿紀錄

審稿者：獨立審稿代理（Claude Opus 5.5，未參與翻譯）　日期：2026-11-04

範圍：`/root/mokaair-work/videos/sothatswhy-p02-cloud-rain/i18n/{en,ja,ko,es,pt,id,vi,th}.todo.json` 的 lines、標題、說明、章節、標籤、縮圖字。

原則：本片只有 CC 與標題說明，沒有配音，所以 `max_chars` 不再是硬限制；凡是為了塞進 max_chars 而掉了意思、限定詞（常常、可能、相對、只）、比較對象、數字或笑點的句子，一律補回，超過 max_chars 也接受。好的句子不動。`boundaries` 裡的句子（p031、p033、p035、p062、p072、p094、p100、p110、p118）改寫時都保留原本的兩段順序。p139 一律改成各語完整口號（ko、es、pt、vi 原本就對）。

數字核對（八語逐一對過）：500 公噸、每立方公尺 0.5 公克、約 1 cm/s、6–7 m/s、約一百萬顆、不到一小時、超過 10 km、0.02 mm、2 mm、每公里約 10 °C、約 100 頭大象、空氣約一百萬公噸。八語原譯都沒有數字錯誤。標題、說明、章節、標籤、縮圖字八語都合理，未更動；系列名在各語內前後一致。

合併：`node tools/video/cli.mjs i18n-merge --slug sothatswhy-p02-cloud-rain --locale en,ja,ko,es,pt,id,vi,th` 一次成功，八語各寫出 141 行到 `docs/videos/sothatswhy-p02-cloud-rain/i18n/<locale>.json`。

## en（英文）— 改 19 句

**結論**：整體準確自然，數字全對；主要是補回被 max_chars 壓掉的「常常」「相對」「午後」等限定詞，與幾句太縮的句子（p115、p136、p138）。可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p001 | 所長！所長！我家陽台外面那朵雲，一直往上長。 | Chief! Chief! The cloud by my balcony keeps growing up! | Chief! Chief! The cloud outside my balcony keeps growing taller! | 補回「一直往上長」的自然說法（growing up 會被讀成「長大」） |
| p009 | 水不是比空氣重嗎？ | Water's heavier than air! | Isn't water heavier than air? | 原文是反問句 |
| p012 | 太陽把地面曬熱，地面再把貼著它的那層空氣烤熱。 | The sun heats the ground; the ground heats the air above it. | The sun heats the ground; the ground heats the layer of air touching it. | 補回「貼著它的那層空氣」 |
| p022 | 就像熱氣球？ | Like a balloon? | Like a hot-air balloon? | 熱氣球，不是普通氣球 |
| p041 | 那麼多大象浮在我家上面？！ | 100 elephants over my house?! | That many elephants floating over my house?! | 補回「浮在」 |
| p046 | 對。而且這些水不是一大塊，是分成非常非常多顆。 | Right. And the water isn't one big lump. It's split into tons of bits. | Right. And the water isn't one big lump. It's split into a huge number of tiny bits. | tons 會和公噸混淆 |
| p052 | 東西越小，空氣擋它的力量相對越大。 | Smaller things, the more air resists. | The smaller something is, the more the air holds it back, for its size. | 補回「相對」，原句文法不完整 |
| p089 | 這樣的雨滴，一秒可以落下六、七公尺，比雲滴快好幾百倍。 | Raindrops fall 6 to 7 m a second, hundreds of times faster than droplets. | Raindrops like these can fall 6 to 7 m a second, hundreds of times faster than cloud droplets. | 補回「這樣的雨滴」與「可以」 |
| p095 | 會下大雨的，是一路往上衝的雲。 | Heavy rain comes from tall clouds. | Heavy rain comes from clouds that shoot all the way up. | 補回「一路往上衝」 |
| p102 | 所以熱空氣往上送得最兇的時候，常常落在下午。 | So warm air rises hardest in the afternoon. | So warm air often rises hardest in the afternoon. | 補回「常常」 |
| p108 | 那為什麼雷陣雨常常下一下就停？ | Why do storms often stop so fast? | So why do thunderstorms often stop so soon? | 雷陣雨用詞一致 |
| p109 | 因為一場大雨，會把自己的引擎關掉。 | Because a big rain turns off its engine. | Because a big rain turns off its own engine. | 補回「自己的」 |
| p114 | 沒有熱空氣補進來，雲就慢慢沒力。 | No warm air, so the cloud runs down. | With no warm air coming in, the cloud slowly runs out of steam. | 補回「補進來」「慢慢」 |
| p115 | 還記得你問要多久嗎？ | Recall: how long? | Remember when you asked how long it takes? | 原句 Recall: how long? 不自然 |
| p121 | 還記得花椰菜嗎？那代表裡面的空氣還在往上衝。 | The cauliflower? It means air's still rising. | Remember the cauliflower? It means the air inside is still rushing up. | 補回「還記得」 |
| p126 | 還記得那陣涼風嗎？冷空氣已經跑在雨的前面了。我一開始說什麼？ | Remember that cool wind? Cold air outruns the rain. What did I say? | Remember that cool wind? The cold air is already running ahead of the rain. What did I say at the start? | 補回「一開始」，原句時態錯 |
| p136 | 引擎關掉，雲就散了。 | No engine. Poof! | The engine's off, so the cloud fades away. | Poof! 少了「雲就散了」 |
| p138 | 還記得那些小水滴嗎？它們不是不會掉，是在等長大！ | Remember the tiny drops? They do fall. They wait to grow! | Remember those tiny drops? It's not that they don't fall. They're waiting to grow! | 原句「They do fall」少了「不是不會掉」的反轉 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | When do storms start near you? Tell us below. | When do afternoon thunderstorms usually start where you live? Tell us in the comments. | 補回「午後」「通常」「幾點開始」 |

## ja（日文）— 改 7 句

**結論**：品質最好，數字、語氣（所長溫和的「〜の／わよ」、ハテナ的童言）都對；只修 7 句，含口號補成「なるほど！」。可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p062 | 沒錯。雲有重量，但它的水碎成數不完的小顆，每一顆都輕到被空氣托住。 | そのとおり。雲は重いけど、水は数えきれない小さな粒で、ひとつひとつが空気に支えられるほど軽いの。 | そのとおり。雲には重さがあるけど、水は数えきれない小さな粒で、ひとつひとつが空気に支えられるほど軽いの。 | 「雲は重い」→原文「雲有重量」 |
| p065 | 才一百倍？那還好嘛。 | たった100倍？平気じゃん。 | たった100倍？たいしたことないじゃん。 | 「平気じゃん」は意味がずれる |
| p115 | 還記得你問要多久嗎？ | で、かかる時間は？ | どれくらいかかるか、聞いてたよね？ | 補回「還記得你問」 |
| p125 | 啊，突然好涼！衣服都飛起來了！ | わっ、急に涼しい！服が飛んでいく！ | わっ、急に涼しい！洗濯物が舞い上がってる！ | 衣服＝洗濯物（伏線）、飛んでいく→舞い上がる |
| p136 | 引擎關掉，雲就散了。 | エンジン切れね。 | エンジンが止まって、雲は消えちゃったの。 | 補回「雲就散了」 |
| p139 | 原來如此！ | なるほど | なるほど！ | 系列口號完整形 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | あなたの町の夕立は何時ごろ？コメントで教えてね。 | あなたの町の夕立は、ふだん何時ごろ始まる？コメントで教えてね。 | 補回「通常」「開始」 |

## ko（韓文）— 改 40 句

**結論**：數字正確、所長半語／小問敬語分得清楚，但為了 max_chars 壓得很兇，掉了比較對象、「可能」「常常」「還記得」等；p052 原譯說成「越小阻力越大」（物理錯），已改為「相對」。修後可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p001 | 所長！所長！我家陽台外面那朵雲，一直往上長。 | 소장님! 소장님! 밖에 구름이 위로 커져요! | 소장님! 소장님! 우리 집 베란다 밖 구름이 자꾸 위로 커져요! | 補回「我家陽台」 |
| p008 | 還有，它會不會變成打在你身上的雨？要多久？ | 그게 비가 되어 내릴까? 얼마나 걸려? | 그리고 그게 비가 돼서 너한테 떨어질까? 얼마나 걸릴까? | 補回「打在你身上」 |
| p009 | 水不是比空氣重嗎？ | 물이 더 무겁잖아요? | 물은 공기보다 무겁잖아요? | 補回比較對象「空氣」 |
| p016 | 白色的霧，要離開壺嘴一點點才出現。 | 하얀 김은 조금 떨어져서 생겨. | 하얀 김은 주둥이에서 조금 떨어져야 생겨. | 補回「離開壺嘴」 |
| p019 | 雲也是一樣。它是很多很小的水滴，有時候是小冰晶，不是一團氣。 | 구름도 같아. 작은 물방울이나 얼음 알갱이지, 기체가 아니야. | 구름도 같아. 아주 작은 물방울이 잔뜩 모인 거고, 가끔은 얼음 알갱이야. 기체가 아니야. | 補回「很多」「有時候」 |
| p021 | 答案是往上爬。被曬熱的空氣比旁邊輕，會一團一團往上浮。 | 답은 위로 올라가기야. 데워진 공기는 가벼워서 덩어리째 떠올라. | 답은 위로 올라가기야. 데워진 공기는 주변보다 가벼워서 덩어리째 떠올라. | 補回比較「比旁邊輕」 |
| p041 | 那麼多大象浮在我家上面？！ | 코끼리들이 우리 집 위에?! | 그 많은 코끼리가 우리 집 위에 떠 있다고요?! | 補回「浮在」 |
| p042 | 聽起來很嚇人對吧？你家上面現在，可能也正浮著一朵。 | 무섭지? 지금 너희 집 위에도 하나 떠 있을걸. | 무섭지? 지금 너희 집 위에도 하나 떠 있을지도 몰라. | 「떠 있을걸」太肯定，原文是「可能」 |
| p043 | 等一下，空氣也有重量吧？ | 잠깐, 공기도 무겁죠? | 잠깐, 공기도 무게가 있죠? | 「무겁죠」= 很重，原文是「也有重量」 |
| p052 | 東西越小，空氣擋它的力量相對越大。 | 작을수록 공기 저항이 커져. | 물체가 작을수록 공기가 막는 힘이 상대적으로 커져. | 補回「相對」，原句說成絕對阻力變大，物理上不對 |
| p053 | 小到像雲滴，空氣幾乎把它托住了。 | 구름방울은 공기가 거의 받쳐 줘. | 구름방울만큼 작으면 공기가 거의 받쳐 줘. | 補回「小到像雲滴」 |
| p054 | 一顆雲滴在不動的空氣裡，一秒大概只掉一公分左右。 | 가만있는 공기에선 1초에 약 1센티미터만 떨어져. | 구름방울은 가만있는 공기에선 1초에 약 1센티미터만 떨어져. | 補回主詞 |
| p061 | 那它根本是在搭電梯往上嘛！ | 엘리베이터 타고 가네요! | 완전 엘리베이터 타고 올라가는 거네요! | 補回「往上」 |
| p062 | 沒錯。雲有重量，但它的水碎成數不完的小顆，每一顆都輕到被空氣托住。 | 맞아. 구름은 무겁지만 물이 무수한 작은 알갱이라 각각 공기에 받칠 만큼 가벼워. | 맞아. 구름은 무게가 있지만 물이 셀 수 없이 작은 알갱이로 쪼개져서, 하나하나가 공기에 받쳐질 만큼 가벼워. | 「무겁지만」→「有重量」 |
| p063 | 那水滴要長到多大，空氣才托不住？ | 물방울이 얼마나 커야 떨어져요? | 물방울이 얼마나 커져야 공기가 못 받쳐요? | 補回「空氣才托不住」 |
| p065 | 才一百倍？那還好嘛。 | 겨우 100배요? | 겨우 100배요? 별거 아니네요. | 補回「那還好嘛」 |
| p075 | 很像。這叫做碰撞合併。不過這只是其中一條路。 | 맞아. 이걸 충돌 병합이라고 해. 근데 이건 한 가지 길이야. | 맞아. 이걸 충돌 병합이라고 해. 근데 이건 여러 길 중 하나일 뿐이야. | 補回「只是其中一條」 |
| p081 | 所以我淋到的雨，可能原本是雪？ | 내가 맞은 비가 원래 눈? | 그럼 내가 맞은 비가 원래는 눈이었을 수도 있어요? | 補回「可能」，句子完整 |
| p088 | 重到上升的空氣托不住，就穿出雲底。 | 못 받칠 만큼 무거워져 구름 밑으로 나와. | 상승 기류가 못 받칠 만큼 무거워져서 구름 밑으로 빠져나와. | 補回「上升的空氣」 |
| p089 | 這樣的雨滴，一秒可以落下六、七公尺，比雲滴快好幾百倍。 | 빗방울은 1초에 6, 7미터 떨어져. 구름방울의 수백 배야. | 이런 빗방울은 1초에 6, 7미터를 떨어져. 구름방울보다 수백 배 빨라. | 「구름방울의 수백 배」少了「快」 |
| p091 | 可是我家旁邊的雲，有的下雨，有的整天都不下。 | 비 오는 구름도, 안 오는 구름도 있어요. | 근데 우리 집 근처 구름은, 비 오는 것도 있고 하루 종일 안 오는 것도 있어요. | 補回「我家旁邊」「整天」 |
| p093 | 這要回到一開始：雲能長多高、裡面的空氣往上衝得多用力。 | 처음 얘기야. 구름이 얼마나 높이 크고, 공기가 얼마나 세게 오르냐. | 처음 얘기로 돌아가야 해. 구름이 얼마나 높이 자라는지, 속의 공기가 얼마나 세게 올라가는지. | 原句殘缺 |
| p095 | 會下大雨的，是一路往上衝的雲。 | 큰비는 쭉쭉 큰 구름이 내려. | 큰비를 내리는 건 쭉쭉 위로 솟는 구름이야. | 「쭉쭉 큰 구름」語意不清 |
| p096 | 雲頂可以超過十公里，跟客機一樣高，甚至更高。 | 꼭대기는 10킬로미터 넘게, 여객기만큼 높아. | 꼭대기는 10킬로미터를 넘어. 여객기만큼, 아니 더 높이. | 補回「甚至更高」 |
| p098 | 對。所以你猜，一天裡面，地面什麼時候最熱？ | 맞아. 하루 중 땅이 제일 뜨거운 때는? | 맞아. 그럼 맞혀 봐. 하루 중 땅이 제일 뜨거운 때는 언제일까? | 補回「你猜」 |
| p103 | 那為什麼台灣特別多？ | 대만은 왜 많아요? | 그럼 대만엔 왜 특히 많아요? | 補回「特別」 |
| p111 | 你在雷雨前感覺到的那陣涼風，常常就是它衝到了地面。 | 뇌우 전 부는 찬 바람이 그게 땅에 닿은 거야. | 뇌우 전에 부는 그 시원한 바람이, 흔히 그게 땅에 닿은 거야. | 補回「常常」 |
| p114 | 沒有熱空氣補進來，雲就慢慢沒力。 | 더운 공기 없인 구름이 약해져. | 더운 공기가 안 들어오면 구름은 서서히 힘이 빠져. | 補回「補進來」「慢慢」 |
| p115 | 還記得你問要多久嗎？ | 시간 물었지? | 얼마나 걸리는지 물었던 거 기억나? | 補回「還記得」 |
| p119 | 那我要怎麼知道，今天的雲會不會下雨？ | 구름이 비를 내릴지 어떻게 알아요? | 그럼 오늘 구름이 비를 내릴지 어떻게 알아요? | 補回「今天」 |
| p121 | 還記得花椰菜嗎？那代表裡面的空氣還在往上衝。 | 콜리플라워지? 아직 오르는 중이야. | 콜리플라워 기억나? 속 공기가 아직 위로 솟고 있다는 뜻이야. | 補回「還記得」「代表」 |
| p125 | 啊，突然好涼！衣服都飛起來了！ | 앗, 갑자기 시원해! 옷이 날아가요! | 앗, 갑자기 시원해! 빨래가 날려요! | 衣服＝晾的衣服（伏線） |
| p126 | 還記得那陣涼風嗎？冷空氣已經跑在雨的前面了。我一開始說什麼？ | 찬 바람 기억나? 비보다 앞선 찬 공기야. 내가 뭐랬지? | 그 찬 바람 기억나? 찬 공기가 벌써 비보다 앞서 왔어. 내가 처음에 뭐랬지? | 補回「一開始」 |
| p129 | 大家都這樣畫，可是不是。 | 다들 그리지만 아냐. | 다들 그렇게 그리지만 아니야. | 補回受詞 |
| p134 | 衣服都收進來了，雨也停了。真的不到一個小時。 | 빨래도 걷고 비도 그쳤어. 한 시간 안에! | 빨래도 다 걷었는데 비도 그쳤어요. 진짜 한 시간도 안 걸렸어요! | 小問台詞補回「真的」，語氣改為對大人 |
| p136 | 引擎關掉，雲就散了。 | 엔진 꺼졌지. | 엔진이 꺼지니까 구름이 흩어졌지. | 補回「雲就散了」 |
| p137 | 打在你手上的每一顆，都是一百萬顆雲滴湊起來的。 | 네 손의 빗방울 하나는 구름방울 약 100만 개야. | 네 손에 떨어진 빗방울 하나하나가 구름방울 약 100만 개가 모인 거야. | 補回「湊起來」 |
| p138 | 還記得那些小水滴嗎？它們不是不會掉，是在等長大！ | 안 떨어지는 게 아니라 크길 기다린 거예요! | 그 작은 물방울들 기억나요? 안 떨어지는 게 아니라 크길 기다린 거예요! | 補回「還記得」 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | 너희 동네 소나기는 몇 시? 댓글로! | 너희 동네 오후 소나기는 보통 몇 시에 시작해? 댓글로 알려 줘. | 補回「通常」「開始」 |
| p141 | 想一起把生活裡的為什麼找到底，就訂閱原來如此事務所。 | 생활 속 왜를 함께 파헤치려면 그래서그랬구나 사무소 구독! | 생활 속 '왜'를 끝까지 함께 파헤치고 싶다면, 그래서그랬구나 사무소를 구독해 줘! | 原句過度壓縮 |

## es（西班牙文）— 改 50 句

**結論**：數字正確、用詞自然，但大量句子被壓成電報體（缺主詞、缺比較對象）；p018 回答否定問句用「Sí」會被讀反，p052 少了「相對」。修後可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p001 | 所長！所長！我家陽台外面那朵雲，一直往上長。 | ¡Directora! ¡La nube de mi balcón sigue creciendo! | ¡Directora! ¡Directora! ¡La nube junto a mi balcón no para de crecer hacia arriba! | 補回重複的呼喊與「往上長」 |
| p009 | 水不是比空氣重嗎？ | ¿No pesa más que el aire? | ¿Pero el agua no pesa más que el aire? | 原句缺主詞「水」 |
| p018 | 對。真正的水蒸氣是看不見的。白白的，是它冷下來，又變回的小水滴。 | Sí. El vapor real no se ve. Lo blanco es vapor que se enfrió y volvió a ser gotas. | Exacto. El vapor real no se ve. Lo blanco es vapor que se enfrió y volvió a ser gotitas. | 回答否定問句用 Sí 會被誤解 |
| p021 | 答案是往上爬。被曬熱的空氣比旁邊輕，會一團一團往上浮。 | Sube. El aire calentado pesa menos que el que lo rodea y sube en burbujas. | Subiendo. El aire calentado pesa menos que el que lo rodea y sube en burbujas. | 回答「誰把它變冷」 |
| p022 | 就像熱氣球？ | ¿Como un globo? | ¿Como un globo aerostático? | 熱氣球 |
| p024 | 空氣往上走，周圍的氣壓變小，它就膨脹；一膨脹，就會變冷。 | Al subir, la presión baja y se expande; y al expandirse, se enfría. | Al subir, la presión a su alrededor baja y el aire se expande; y al expandirse, se enfría. | 補回主詞 |
| p026 | 冷到某個高度，水氣就飽和了，多出來的就會凝結。 | A cierta altura se satura; lo que sobra se condensa. | A cierta altura el aire se satura, y el vapor que sobra se condensa. | 補回主詞 |
| p031 | 所以你看積雲，底部常常是平的：那個高度，剛好是空氣冷到開始凝結的地方。 | Por eso los cúmulos suelen ser planos abajo: ahí el aire empieza a condensarse. | Por eso los cúmulos suelen tener la base plana: esa altura es justo donde el aire se enfría lo bastante para condensarse. | 補回「剛好是空氣冷到」，保留兩段順序 |
| p037 | 可是一立方公里，有十億個立方公尺。 | Pero un kilómetro cúbico tiene mil millones. | Pero un kilómetro cúbico tiene mil millones de metros cúbicos. | 補回單位 |
| p041 | 那麼多大象浮在我家上面？！ | ¡¿Tantos elefantes sobre mi casa?! | ¡¿Tantos elefantes flotando sobre mi casa?! | 補回「浮」 |
| p052 | 東西越小，空氣擋它的力量相對越大。 | Más chico, más lo frena el aire. | Cuanto más chico es algo, más lo frena el aire, en proporción. | 補回「相對」 |
| p054 | 一顆雲滴在不動的空氣裡，一秒大概只掉一公分左右。 | En aire quieto, una gotita cae como 1 cm por segundo. | En aire quieto, una gotita cae solo como 1 cm por segundo. | 補回「只」 |
| p056 | 照這個速度，從一公里高的雲底掉到地上，要超過一天。 | Así, caer desde la base de la nube a 1 km tardaría más de un día. | A esa velocidad, caer desde la base de una nube a 1 km de altura tardaría más de un día. | 原句語意不清 |
| p063 | 那水滴要長到多大，空氣才托不住？ | ¿Cuánto crece hasta que el aire no puede? | ¿Cuánto tiene que crecer una gota para que el aire ya no la sostenga? | 原句殘缺 |
| p064 | 你淋過的雨滴，常見的大約兩公釐，直徑是雲滴的一百倍。 | Una gota de lluvia: unos 2 mm, 100 veces el diámetro de una gotita. | Las gotas de lluvia que te han mojado suelen medir unos 2 mm: 100 veces el diámetro de una gotita. | 補回「你淋過的」「常見」 |
| p072 | 雲裡的水滴大小不一樣。大一點的掉得比較快，就會追上、撞上下面比較小的。 | Las gotas varían de tamaño. Las grandes caen más rápido y chocan con las de abajo. | Las gotas de una nube no son del mismo tamaño. Las grandes caen más rápido y alcanzan y chocan a las más chicas de abajo. | 補回「比較小的」與「追上」 |
| p073 | 撞上去黏在一起，它就更大、掉得更快、撞到更多。 | Se pegan: crece, cae más rápido y choca más. | Se pegan, y la gota crece, cae más rápido y choca con más. | 補回主詞 |
| p074 | 像滾雪球！ | ¡Bola de nieve! | ¡Como una bola de nieve! | 補回「像」 |
| p075 | 很像。這叫做碰撞合併。不過這只是其中一條路。 | Igualito. Se llama colisión y coalescencia. Pero es solo un camino. | Igualito. Se llama colisión y coalescencia. Pero es solo uno de los caminos. | 「其中一條」 |
| p080 | 冰晶一邊長大一邊往下掉，掉到比較暖的低空，再融化成雨。 | Crecen al caer y, abajo, en aire más tibio, se derriten en lluvia. | Los cristales crecen mientras caen y, más abajo, en aire más tibio, se derriten y se vuelven lluvia. | 補回主詞 |
| p081 | 所以我淋到的雨，可能原本是雪？ | ¿Mi lluvia pudo ser nieve antes? | ¿Entonces la lluvia que me moja pudo ser nieve antes? | 補回「我淋到的」 |
| p082 | 有可能。夏天長得很高的雷雨雲裡，兩條路都可能發生。 | Puede ser. En las altas nubes de tormenta de verano, se dan los dos. | Puede ser. En las nubes de tormenta altas del verano, pueden darse los dos caminos. | 補回「可能」 |
| p083 | 不管走哪一條，重點都一樣：水滴得先長到夠大。 | Sea cual sea, las gotas primero deben crecer. | Sea cual sea el camino, lo importante es lo mismo: primero las gotas deben crecer lo suficiente. | 補回「重點都一樣」「夠大」 |
| p088 | 重到上升的空氣托不住，就穿出雲底。 | Pesan mucho para el aire que sube y salen por la base. | Pesan demasiado para que el aire que sube las sostenga, y salen por la base de la nube. | 原句文法不通 |
| p089 | 這樣的雨滴，一秒可以落下六、七公尺，比雲滴快好幾百倍。 | Caen de 6 a 7 m por segundo: cientos de veces más que las gotitas. | Estas gotas de lluvia caen de 6 a 7 m por segundo: cientos de veces más rápido que las gotitas. | 補回「快」 |
| p091 | 可是我家旁邊的雲，有的下雨，有的整天都不下。 | Pero cerca de casa, unas llueven y otras nunca. | Pero cerca de mi casa, unas nubes llueven y otras no llueven en todo el día. | 補回「我家」「整天」 |
| p095 | 會下大雨的，是一路往上衝的雲。 | Las de aguacero suben sin parar. | Las que dan aguaceros son las nubes que suben sin parar. | 原句主詞不清 |
| p100 | 很多人都這樣猜。太陽最高是中午，可是地面和空氣最熱，通常要再晚一點。 | Muchos lo creen. El sol sube más a mediodía; suelo y aire se calientan más después. | Mucha gente lo cree. El sol está más alto a mediodía, pero el suelo y el aire suelen estar más calientes un poco después. | 補回「通常」，保留兩段順序 |
| p102 | 所以熱空氣往上送得最兇的時候，常常落在下午。 | Por eso el aire caliente sube más fuerte en la tarde. | Por eso el aire caliente suele subir con más fuerza en la tarde. | 補回「常常」 |
| p104 | 因為台灣的夏天還多了兩個幫手：從海上吹進陸地的濕空氣， | Porque el verano en Taiwán tiene dos ayudantes más: aire húmedo del mar, | Porque el verano en Taiwán tiene dos ayudantes más: aire húmedo que sopla del mar hacia la tierra, | 補回「吹進陸地」 |
| p109 | 因為一場大雨，會把自己的引擎關掉。 | Un aguacero apaga su propio motor. | Porque un aguacero apaga su propio motor. | 補回「因為」 |
| p111 | 你在雷雨前感覺到的那陣涼風，常常就是它衝到了地面。 | La brisa previa a la tormenta suele ser ese aire que baja. | El viento fresco que sientes antes de la tormenta suele ser ese aire que llega al suelo. | 補回「你感覺到的」「衝到地面」 |
| p113 | 冷空氣往下灌，把往上送的熱空氣擋掉了。 | El aire frío baja y frena al caliente. | El aire frío baja y frena el aire caliente que sube. | 補回「往上送的」 |
| p114 | 沒有熱空氣補進來，雲就慢慢沒力。 | Sin aire caliente, la nube se apaga. | Sin aire caliente que entre, la nube se va apagando. | 補回「補進來」「慢慢」 |
| p115 | 還記得你問要多久嗎？ | ¿Y cuánto tarda? | ¿Recuerdas que preguntaste cuánto tarda? | 原句漏了「還記得你問」 |
| p116 | 一個單獨的雷雨雲，從長大到散掉，常常不到一小時。 | Una nube de tormenta sola suele durar menos de una hora. | Una sola nube de tormenta, desde que crece hasta que se deshace, suele durar menos de una hora. | 補回「從長大到散掉」 |
| p121 | 還記得花椰菜嗎？那代表裡面的空氣還在往上衝。 | ¿La coliflor? El aire aún sube adentro. | ¿Recuerdas la coliflor? Significa que el aire de adentro sigue subiendo. | 補回「還記得」「代表」 |
| p126 | 還記得那陣涼風嗎？冷空氣已經跑在雨的前面了。我一開始說什麼？ | ¿El viento fresco? El frío va antes que la lluvia. ¿Qué te dije? | ¿Recuerdas el viento fresco? El aire frío ya va delante de la lluvia. ¿Qué te dije al principio? | 補回「一開始」 |
| p127 | 收衣服！ | ¡La ropa! | ¡Recoger la ropa! | 收衣服 |
| p128 | 好大顆！雨滴是不是像眼淚那樣，尖尖的？ | ¡Qué gotota! ¿Son puntiagudas, como lágrimas? | ¡Qué gotas tan grandes! ¿Las gotas de lluvia son puntiagudas, como lágrimas? | 補回主詞 |
| p129 | 大家都這樣畫，可是不是。 | Así se dibujan, pero no. | Todos las dibujan así, pero no. | 補回「大家都」 |
| p130 | 雨滴掉得越快，空氣從下面擋得越用力。 | Más rápido cae, más la empuja el aire. | Cuanto más rápido cae una gota, más fuerte la empuja el aire desde abajo. | 原句殘缺 |
| p131 | 小的幾乎是圓的。大一點的，落下時底部被空氣壓扁，像漢堡麵包。 | Las chicas, casi redondas; las grandes, chatas abajo: pan de hamburguesa. | Las chicas son casi redondas; las más grandes se aplanan abajo al caer, como un pan de hamburguesa. | 補回「落下時」 |
| p132 | 再大，就被扯開，碎成好幾顆。所以雨滴不會一直長下去。 | Más grandes aún, se rompen en varias. Por eso no crecen sin fin. | Si son aún más grandes, se rompen en varias. Por eso las gotas no crecen sin fin. | 補回主詞 |
| p134 | 衣服都收進來了，雨也停了。真的不到一個小時。 | Ropa adentro y ya paró. ¡Menos de una hora! | Ya entramos la ropa y paró la lluvia. ¡De verdad, menos de una hora! | 補回「真的」 |
| p136 | 引擎關掉，雲就散了。 | Sin motor, adiós. | Se apagó el motor y la nube se deshizo. | 「adiós」少了「雲就散了」 |
| p137 | 打在你手上的每一顆，都是一百萬顆雲滴湊起來的。 | Cada gota en tu mano es como un millón de gotitas juntas. | Cada gota que te cayó en la mano era como un millón de gotitas juntas. | 補回「打在你手上的」 |
| p138 | 還記得那些小水滴嗎？它們不是不會掉，是在等長大！ | ¿Recuerdas las gotitas? ¡Sí caen; esperan a crecer! | ¿Recuerdas las gotitas? ¡No es que no caigan: esperan a crecer! | 「Sí caen」少了「不是不會掉」的反轉 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | ¿A qué hora caen tus tormentas? ¡Cuéntanos! | ¿A qué hora suelen empezar las tormentas de la tarde donde vives? ¡Cuéntanos en los comentarios! | 補回「午後」「通常」 |
| p141 | 想一起把生活裡的為什麼找到底，就訂閱原來如此事務所。 | ¿Quieres saber el porqué de todo? Suscríbete a La Oficina del Por Eso. | ¿Quieres llegar al fondo de los porqués de la vida diaria? Suscríbete a La Oficina del Por Eso. | 補回「一起」「生活裡」「找到底」 |

## pt（葡萄牙文）— 改 67 句

**結論**：數字正確、巴西口語自然，但是八語中壓縮最嚴重的一份：缺主詞、缺單位（p037）、p044 沒說是空氣、多句殘缺。修後可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p001 | 所長！所長！我家陽台外面那朵雲，一直往上長。 | Diretora! A nuvem da varanda não para de subir! | Diretora! Diretora! A nuvem lá fora da minha varanda não para de crescer pra cima! | 補回重複呼喊、「往上長」 |
| p003 | 那你等一下可能要收衣服了。 | Vai ter que recolher a roupa. | Daqui a pouco talvez você tenha que recolher a roupa. | 補回「等一下可能」 |
| p006 | 這件事，你每年夏天其實都看過答案，只是沒有人跟你說。 | Você vê a resposta todo verão; só ninguém te contou. | Você vê a resposta todo verão; só que ninguém te contou. | 文法修正 |
| p008 | 還有，它會不會變成打在你身上的雨？要多久？ | E vira chuva em você? Em quanto tempo? | E será que ela vira chuva e cai em você? Em quanto tempo? | 補回「會不會」 |
| p009 | 水不是比空氣重嗎？ | Água não é mais pesada? | A água não é mais pesada que o ar? | 補回主詞與比較對象 |
| p012 | 太陽把地面曬熱，地面再把貼著它的那層空氣烤熱。 | O sol esquenta o chão, e ele, o ar logo acima. | O sol esquenta o chão, e o chão esquenta a camada de ar encostada nele. | 補回「貼著它的那層」 |
| p018 | 對。真正的水蒸氣是看不見的。白白的，是它冷下來，又變回的小水滴。 | Isso. Vapor de verdade é invisível. O branco é vapor que esfriou: gotinhas. | Isso. Vapor de verdade é invisível. O branco é vapor que esfriou e voltou a ser gotinhas. | 補回「又變回」 |
| p021 | 答案是往上爬。被曬熱的空氣比旁邊輕，會一團一團往上浮。 | Ela sobe. O ar aquecido é mais leve que o em volta e sobe em bolhas. | A resposta é subir. O ar aquecido é mais leve que o ar em volta e sobe em bolhas. | 回答「誰把它變冷」 |
| p022 | 就像熱氣球？ | Tipo um balão? | Tipo um balão de ar quente? | 熱氣球 |
| p026 | 冷到某個高度，水氣就飽和了，多出來的就會凝結。 | Numa certa altura satura, e o que sobra condensa. | Numa certa altura o ar fica saturado, e o vapor que sobra condensa. | 補回主詞 |
| p028 | 杯子外面有杯子給它黏，天上有什麼可以黏？ | No copo, elas grudam no copo. E lá em cima? | No copo, elas têm o copo pra grudar. E lá no céu, grudam em quê? | 原句同義反覆、問句殘缺 |
| p031 | 所以你看積雲，底部常常是平的：那個高度，剛好是空氣冷到開始凝結的地方。 | Por isso a base do cúmulo é reta: é a altura onde o ar começa a condensar. | Por isso a base do cúmulo costuma ser reta: essa altura é justamente onde o ar esfria o bastante pra começar a condensar. | 補回「常常」「冷到」，保留兩段順序 |
| p033 | 只要下面一直有熱空氣送上來，這朵雲就會一直往上長，長得像一顆花椰菜。 | Com ar quente subindo de baixo, a nuvem cresce, que nem couve-flor. | Enquanto chegar ar quente de baixo, a nuvem continua crescendo pra cima, que nem uma couve-flor. | 補回「一直」 |
| p037 | 可是一立方公里，有十億個立方公尺。 | Mas um quilômetro cúbico tem um bilhão. | Mas um quilômetro cúbico tem um bilhão de metros cúbicos. | 補回單位 |
| p041 | 那麼多大象浮在我家上面？！ | 100 elefantes em cima de casa?! | Esse monte de elefantes flutuando em cima da minha casa?! | 補回「浮」 |
| p044 | 有，而且更重。同樣一立方公里的空氣，大約有一百萬公噸。 | Pesa mais: nesse quilômetro cúbico, cerca de um milhão de toneladas. | Pesa, e mais: esse mesmo quilômetro cúbico de ar pesa cerca de um milhão de toneladas. | 原句「nesse km³」沒說是空氣 |
| p052 | 東西越小，空氣擋它的力量相對越大。 | Quanto menor, mais o ar segura. | Quanto menor a coisa, maior é, em proporção, a força do ar que a segura. | 補回「相對」 |
| p053 | 小到像雲滴，空氣幾乎把它托住了。 | Numa gotícula, o ar quase a segura. | Quando é pequena como uma gotícula, o ar quase a segura. | 原句同義反覆 |
| p054 | 一顆雲滴在不動的空氣裡，一秒大概只掉一公分左右。 | No ar parado, a gotícula cai cerca de 1 cm por segundo. | No ar parado, a gotícula cai só cerca de 1 cm por segundo. | 補回「只」 |
| p056 | 照這個速度，從一公里高的雲底掉到地上，要超過一天。 | Assim, cair da base a 1 km de altura levaria mais de um dia. | Nessa velocidade, cair da base da nuvem, a 1 km de altura, até o chão levaria mais de um dia. | 補回「雲底」「到地上」 |
| p063 | 那水滴要長到多大，空氣才托不住？ | E quão grande, pro ar não aguentar? | E a gota tem que crescer quanto pro ar não aguentar? | 原句殘缺 |
| p064 | 你淋過的雨滴，常見的大約兩公釐，直徑是雲滴的一百倍。 | Gota de chuva: uns 2 mm, 100 vezes o diâmetro da gotícula. | As gotas de chuva que já caíram em você costumam ter uns 2 mm: 100 vezes o diâmetro da gotícula. | 補回「你淋過的」「常見」 |
| p066 | 是直徑喔。體積是長、寬、高三個方向都要乘。 | É o diâmetro. O volume multiplica nas três direções. | É o diâmetro. O volume multiplica nas três direções: comprimento, largura e altura. | 補回三個方向 |
| p072 | 雲裡的水滴大小不一樣。大一點的掉得比較快，就會追上、撞上下面比較小的。 | As gotas variam de tamanho. As maiores caem mais rápido e batem nas de baixo. | As gotas da nuvem têm tamanhos diferentes. As maiores caem mais rápido, alcançam e batem nas menores lá embaixo. | 補回「比較小的」「追上」 |
| p073 | 撞上去黏在一起，它就更大、掉得更快、撞到更多。 | Grudam: cresce, cai mais rápido, bate mais. | Grudam, e a gota cresce, cai mais rápido e bate em mais. | 補回主詞 |
| p074 | 像滾雪球！ | Bola de neve! | Que nem bola de neve! | 補回「像」 |
| p075 | 很像。這叫做碰撞合併。不過這只是其中一條路。 | Isso. Chama colisão e coalescência. Mas é só um caminho. | Isso. Chama colisão e coalescência. Mas é só um dos caminhos. | 「其中一條」 |
| p076 | 雲爬到夠高的地方，溫度會降到零度以下。那裡會有小冰晶， | Bem no alto, fica abaixo de 0 °C. Lá tem cristais de gelo, | Quando a nuvem sobe bastante, a temperatura fica abaixo de 0 °C. Lá tem cristais de gelo, | 補回主詞「雲」 |
| p077 | 也有冷到零度以下、卻還沒結冰的小水滴。 | e gotinhas abaixo de 0 °C sem congelar. | e gotinhas abaixo de 0 °C que ainda não congelaram. | 補回「還沒」 |
| p080 | 冰晶一邊長大一邊往下掉，掉到比較暖的低空，再融化成雨。 | Crescem caindo e derretem em chuva no ar mais quente de baixo. | Os cristais crescem enquanto caem e, no ar mais quente lá embaixo, derretem e viram chuva. | 補回主詞 |
| p081 | 所以我淋到的雨，可能原本是雪？ | Minha chuva já foi neve? | Então a chuva que caiu em mim pode ter sido neve? | 補回「我淋到的」「可能」 |
| p082 | 有可能。夏天長得很高的雷雨雲裡，兩條路都可能發生。 | Pode ser. Nas altas nuvens de tempestade do verão, rolam os dois. | Pode ser. Nas nuvens de tempestade altas do verão, os dois caminhos podem acontecer. | 語域較中性 |
| p083 | 不管走哪一條，重點都一樣：水滴得先長到夠大。 | Em qualquer um, a gota precisa crescer antes. | Seja qual for o caminho, o importante é o mesmo: a gota precisa crescer o bastante primeiro. | 補回「重點都一樣」「夠大」 |
| p087 | 掉下來的，是已經長大的水滴。 | Caem as gotas grandes. | O que cai são as gotas que já cresceram. | 補回「已經長大的」 |
| p088 | 重到上升的空氣托不住，就穿出雲底。 | Pesadas demais pro ar que sobe, saem pela base. | Pesadas demais pro ar que sobe segurar, elas saem pela base da nuvem. | 補回主詞 |
| p089 | 這樣的雨滴，一秒可以落下六、七公尺，比雲滴快好幾百倍。 | Caem 6 a 7 m por segundo, centenas de vezes mais que a gotícula. | Essas gotas de chuva caem 6 a 7 m por segundo, centenas de vezes mais rápido que as gotículas. | 補回「快」 |
| p091 | 可是我家旁邊的雲，有的下雨，有的整天都不下。 | Mas perto de casa, umas chovem, outras nunca. | Mas perto da minha casa, umas nuvens chovem e outras não chovem o dia inteiro. | 補回「我家」「整天」 |
| p095 | 會下大雨的，是一路往上衝的雲。 | Chove forte a que sobe muito. | As que trazem chuva forte são as nuvens que sobem sem parar. | 原句語意不清 |
| p096 | 雲頂可以超過十公里，跟客機一樣高，甚至更高。 | O topo passa de 10 km: altura de avião, ou mais. | O topo passa de 10 km: altura de avião de passageiros, ou mais. | 客機 |
| p098 | 對。所以你猜，一天裡面，地面什麼時候最熱？ | É. Então chuta: que hora o chão fica mais quente? | É. Então chuta: em que hora do dia o chão fica mais quente? | 文法修正 |
| p100 | 很多人都這樣猜。太陽最高是中午，可是地面和空氣最熱，通常要再晚一點。 | Muitos acham. O sol é mais alto ao meio-dia; chão e ar esquentam mais depois. | Muita gente acha isso. O sol fica mais alto ao meio-dia, mas o chão e o ar costumam esquentar mais um pouco depois. | 補回「通常」，保留兩段順序 |
| p102 | 所以熱空氣往上送得最兇的時候，常常落在下午。 | Por isso o ar quente sobe mais forte à tarde. | Por isso o ar quente costuma subir mais forte à tarde. | 補回「常常」 |
| p103 | 那為什麼台灣特別多？ | Por que tanto em Taiwan? | E por que tem tanta em Taiwan? | 陰性一致（tempestade） |
| p104 | 因為台灣的夏天還多了兩個幫手：從海上吹進陸地的濕空氣， | O verão de Taiwan tem mais dois ajudantes: ar úmido vindo do mar, | O verão de Taiwan tem mais dois ajudantes: ar úmido que sopra do mar pra terra, | 補回「吹進陸地」 |
| p105 | 還有山。山坡把空氣往上抬，雲就特別容易在山邊長起來。 | e as montanhas: as encostas erguem o ar, e ali nascem nuvens. | e as montanhas: as encostas empurram o ar pra cima, e as nuvens crescem fácil perto delas. | 補回「特別容易長起來」 |
| p108 | 那為什麼雷陣雨常常下一下就停？ | Por que a tempestade para tão rápido? | Então por que as tempestades costumam parar tão rápido? | 補回「常常」 |
| p109 | 因為一場大雨，會把自己的引擎關掉。 | Chuva forte desliga o próprio motor. | Porque uma chuva forte desliga o próprio motor. | 補回「因為」 |
| p110 | 雨落下來，會把周圍的空氣一起往下拖；雨在半路蒸發，又讓這團空氣更冷。 | A chuva puxa o ar pra baixo; e, evaporando no caminho, deixa ele mais frio. | A chuva, caindo, puxa o ar em volta pra baixo; e, evaporando no caminho, deixa esse ar ainda mais frio. | 補回「周圍」「更」，保留兩段順序 |
| p111 | 你在雷雨前感覺到的那陣涼風，常常就是它衝到了地面。 | O ventinho antes do temporal costuma ser esse ar. | O vento fresco que você sente antes da tempestade costuma ser esse ar chegando ao chão. | 補回「你感覺到的」「衝到地面」 |
| p113 | 冷空氣往下灌，把往上送的熱空氣擋掉了。 | O ar frio desce e barra o quente. | O ar frio desce e barra o ar quente que sobe. | 補回「往上送的」 |
| p114 | 沒有熱空氣補進來，雲就慢慢沒力。 | Sem ar quente, a nuvem enfraquece. | Sem ar quente chegando, a nuvem vai perdendo a força. | 補回「補進來」「慢慢」 |
| p115 | 還記得你問要多久嗎？ | E quanto tempo? | Lembra que você perguntou quanto tempo leva? | 原句漏了「還記得」 |
| p116 | 一個單獨的雷雨雲，從長大到散掉，常常不到一小時。 | Uma tempestade isolada costuma durar menos de uma hora. | Uma nuvem de tempestade isolada, de crescer até sumir, costuma levar menos de uma hora. | 補回「從長大到散掉」 |
| p119 | 那我要怎麼知道，今天的雲會不會下雨？ | E como sei se a nuvem de hoje chove? | E como eu sei se as nuvens de hoje vão chover? | 語句修正 |
| p121 | 還記得花椰菜嗎？那代表裡面的空氣還在往上衝。 | Lembra da couve-flor? O ar ainda sobe. | Lembra da couve-flor? Quer dizer que o ar lá dentro ainda tá subindo. | 補回「代表」 |
| p126 | 還記得那陣涼風嗎？冷空氣已經跑在雨的前面了。我一開始說什麼？ | O vento fresco? O frio chega antes da chuva. O que eu disse? | Lembra do vento fresco? O ar frio já chegou antes da chuva. O que eu disse no começo? | 補回「一開始」 |
| p127 | 收衣服！ | A roupa! | Recolher a roupa! | 收衣服 |
| p129 | 大家都這樣畫，可是不是。 | Desenham assim; não é. | Todo mundo desenha assim, mas não é. | 補回「大家都」 |
| p130 | 雨滴掉得越快，空氣從下面擋得越用力。 | Quanto mais rápido, mais o ar empurra. | Quanto mais rápido a gota cai, mais forte o ar empurra de baixo. | 原句殘缺 |
| p131 | 小的幾乎是圓的。大一點的，落下時底部被空氣壓扁，像漢堡麵包。 | As pequenas, redondinhas; as grandes, achatadas: pão de hambúrguer. | As pequenas são quase redondas; as maiores ficam achatadas embaixo ao cair, que nem pão de hambúrguer. | 補回「落下時底部」 |
| p132 | 再大，就被扯開，碎成好幾顆。所以雨滴不會一直長下去。 | Maiores, se rasgam em várias. Por isso não crescem sem fim. | Maiores ainda, se rasgam em várias. Por isso as gotas não crescem sem fim. | 補回主詞 |
| p134 | 衣服都收進來了，雨也停了。真的不到一個小時。 | Roupa dentro, chuva parou. Nem uma hora! | A roupa tá guardada e a chuva parou. Não deu nem uma hora mesmo! | 補回「真的」 |
| p136 | 引擎關掉，雲就散了。 | Sem motor, sumiu. | Desligou o motor, e a nuvem se desfez. | 補回「引擎關掉」 |
| p137 | 打在你手上的每一顆，都是一百萬顆雲滴湊起來的。 | Cada gota na sua mão era cerca de um milhão de gotículas. | Cada gota que caiu na sua mão era cerca de um milhão de gotículas juntas. | 補回「湊起來」 |
| p138 | 還記得那些小水滴嗎？它們不是不會掉，是在等長大！ | Lembra das gotinhas? Elas caem; só esperam crescer! | Lembra das gotinhas? Não é que elas não caiam; estão esperando crescer! | 「Elas caem」少了「不是不會掉」的反轉 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | Que horas cai a tempestade aí? Conta! | Que horas costuma começar a tempestade da tarde aí onde você mora? Conta nos comentários! | 補回「午後」「通常」 |
| p141 | 想一起把生活裡的為什麼找到底，就訂閱原來如此事務所。 | Quer saber os porquês? Inscreva-se no Escritório do Ah, É Por Isso. | Quer ir a fundo nos porquês do dia a dia com a gente? Inscreva-se no Escritório do Ah, É Por Isso. | 補回「一起」「生活裡」「找到底」 |

## id（印尼文）— 改 63 句

**結論**：數字正確，但壓縮嚴重：p062「Awan berat」（雲很重）與原意不同、p088 文法不通、p129「Salah」語氣太硬、口號只有「Begitu!」。修後可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p001 | 所長！所長！我家陽台外面那朵雲，一直往上長。 | Bu Kepala! Awan di luar balkonku terus meninggi. | Bu Kepala! Bu Kepala! Awan di luar balkon rumahku terus meninggi! | 補回重複呼喊 |
| p003 | 那你等一下可能要收衣服了。 | Siap-siap angkat jemuran, ya. | Sebentar lagi kamu mungkin harus angkat jemuran. | 補回「等一下可能」 |
| p008 | 還有，它會不會變成打在你身上的雨？要多久？ | Dan apa ia jadi hujan di atasmu? Berapa lama? | Dan apa ia akan jadi hujan yang menimpamu? Berapa lama lagi? | 補回「打在你身上」 |
| p009 | 水不是比空氣重嗎？ | Air kan lebih berat? | Air kan lebih berat dari udara? | 補回比較對象 |
| p012 | 太陽把地面曬熱，地面再把貼著它的那層空氣烤熱。 | Matahari memanasi tanah, lalu tanah memanasi udaranya. | Matahari memanasi tanah, lalu tanah memanasi lapisan udara yang menempel di atasnya. | 補回「貼著它的那層」 |
| p018 | 對。真正的水蒸氣是看不見的。白白的，是它冷下來，又變回的小水滴。 | Betul. Uap air tak terlihat. Yang putih itu tetes kecil dari uap yang mendingin. | Betul. Uap air tak terlihat. Yang putih itu uap yang mendingin dan kembali jadi tetes kecil. | 補回「又變回」 |
| p021 | 答案是往上爬。被曬熱的空氣比旁邊輕，會一團一團往上浮。 | Jawabannya: naik. Udara hangat lebih ringan, jadi naik gumpal demi gumpal. | Jawabannya: naik. Udara yang dipanasi matahari lebih ringan dari udara di sekitarnya, jadi naik gumpal demi gumpal. | 補回比較「比旁邊輕」 |
| p022 | 就像熱氣球？ | Kayak balon udara? | Kayak balon udara panas? | 熱氣球 |
| p023 | 有點像。而且你應該有感覺過：爬山爬得越高，就越涼。 | Mirip. Kamu pasti pernah rasa: makin tinggi mendaki gunung, makin sejuk. | Mirip. Kamu pasti pernah merasakannya: makin tinggi mendaki gunung, makin sejuk. | 文法修正 |
| p024 | 空氣往上走，周圍的氣壓變小，它就膨脹；一膨脹，就會變冷。 | Makin naik, tekanan turun, udara mengembang; itu bikin dingin. | Udara yang naik bertemu tekanan yang makin rendah, jadi mengembang; begitu mengembang, ia mendingin. | 補回「周圍的氣壓」 |
| p026 | 冷到某個高度，水氣就飽和了，多出來的就會凝結。 | Di ketinggian tertentu udara jenuh; sisanya mengembun. | Di ketinggian tertentu, uap airnya jenuh; sisanya mengembun. | 主詞修正（飽和的是水氣） |
| p028 | 杯子外面有杯子給它黏，天上有什麼可以黏？ | Di gelas ada gelasnya. Di langit, menempel ke apa? | Di gelas, ada gelas buat menempel. Di langit, menempel ke apa? | 語句修正 |
| p029 | 好問題。空氣裡有很多你看不到的小顆粒：灰塵、海鹽、煙。 | Bagus. Udara penuh butiran yang tak terlihat: debu, garam laut, asap. | Pertanyaan bagus. Udara penuh butiran yang tak terlihat: debu, garam laut, asap. | 「Bagus」→「好問題」 |
| p031 | 所以你看積雲，底部常常是平的：那個高度，剛好是空氣冷到開始凝結的地方。 | Makanya dasar kumulus sering datar: di ketinggian itu, udara mulai mengembun. | Makanya dasar kumulus sering datar: ketinggian itu pas tempat udara cukup dingin untuk mulai mengembun. | 補回「剛好」，保留兩段順序 |
| p033 | 只要下面一直有熱空氣送上來，這朵雲就會一直往上長，長得像一顆花椰菜。 | Selama udara hangat terus naik, awan ini terus tumbuh, mirip kembang kol. | Selama udara hangat terus naik dari bawah, awan ini terus tumbuh ke atas, mirip kembang kol. | 補回「下面」「往上長」 |
| p041 | 那麼多大象浮在我家上面？！ | Seratus gajah di atas rumahku?! | Gajah sebanyak itu melayang di atas rumahku?! | 補回「浮」 |
| p052 | 東西越小，空氣擋它的力量相對越大。 | Makin kecil, udara makin menahan. | Makin kecil bendanya, makin besar, secara relatif, tahanan udaranya. | 補回「相對」 |
| p053 | 小到像雲滴，空氣幾乎把它托住了。 | Tetes awan nyaris ditopang udara. | Kalau sekecil tetes awan, ia nyaris ditopang udara. | 補回「小到像」 |
| p054 | 一顆雲滴在不動的空氣裡，一秒大概只掉一公分左右。 | Di udara diam, tetes awan jatuh sekitar 1 cm per detik. | Di udara diam, tetes awan cuma jatuh sekitar 1 cm per detik. | 補回「只」 |
| p056 | 照這個速度，從一公里高的雲底掉到地上，要超過一天。 | Selaju itu, jatuh dari dasar awan 1 km butuh lebih dari sehari. | Dengan laju itu, jatuh dari dasar awan setinggi 1 km sampai ke tanah butuh lebih dari sehari. | 補回「到地上」 |
| p062 | 沒錯。雲有重量，但它的水碎成數不完的小顆，每一顆都輕到被空氣托住。 | Ya. Awan berat, tapi airnya pecah jadi butir tak terhitung, tiap butir ringan ditopang udara. | Ya. Awan punya berat, tapi airnya pecah jadi butir tak terhitung, tiap butir cukup ringan untuk ditopang udara. | 「Awan berat」→「雲有重量」 |
| p063 | 那水滴要長到多大，空氣才托不住？ | Sebesar apa tetes sampai tak tertopang? | Tetes harus sebesar apa sampai udara tak bisa menopangnya? | 語句修正 |
| p064 | 你淋過的雨滴，常見的大約兩公釐，直徑是雲滴的一百倍。 | Tetes hujan biasanya sekitar 2 mm: 100 kali diameter tetes awan. | Tetes hujan yang pernah membasahimu biasanya sekitar 2 mm: diameternya 100 kali tetes awan. | 補回「你淋過的」 |
| p071 | 沒有人捏，是它們自己撞在一起。 | Nggak ada. Mereka saling tabrak. | Nggak ada yang meremas. Mereka saling tabrak sendiri. | 補回「沒有人捏」 |
| p072 | 雲裡的水滴大小不一樣。大一點的掉得比較快，就會追上、撞上下面比較小的。 | Tetes awan beda ukuran. Yang besar jatuh lebih cepat, menyusul, menabrak yang kecil. | Tetes air di awan beda-beda ukurannya. Yang besar jatuh lebih cepat, lalu menyusul dan menabrak yang lebih kecil di bawahnya. | 補回「下面比較小的」 |
| p076 | 雲爬到夠高的地方，溫度會降到零度以下。那裡會有小冰晶， | Kalau cukup tinggi, awan di bawah 0 °C. Ada kristal es kecil, | Kalau awan naik cukup tinggi, suhunya turun di bawah 0 °C. Di sana ada kristal es kecil, | 主詞修正 |
| p080 | 冰晶一邊長大一邊往下掉，掉到比較暖的低空，再融化成雨。 | Kristal tumbuh sambil jatuh, lalu cair jadi hujan di bawah yang hangat. | Kristal es tumbuh sambil jatuh, lalu mencair jadi hujan di udara bawah yang lebih hangat. | 語句修正 |
| p081 | 所以我淋到的雨，可能原本是雪？ | Jadi hujanku dulunya bisa salju? | Jadi hujan yang kena aku dulunya bisa saja salju? | 補回「我淋到的」 |
| p083 | 不管走哪一條，重點都一樣：水滴得先長到夠大。 | Lewat mana pun, tetes harus cukup besar dulu. | Lewat jalan mana pun, intinya sama: tetes harus cukup besar dulu. | 補回「重點都一樣」 |
| p087 | 掉下來的，是已經長大的水滴。 | Yang jatuh tetes besar. | Yang jatuh adalah tetes yang sudah besar. | 補回「已經長大的」 |
| p088 | 重到上升的空氣托不住，就穿出雲底。 | Udara naik tak kuat lagi, ia menembus dasar awan. | Terlalu berat untuk ditopang udara yang naik, ia keluar menembus dasar awan. | 原句文法不通 |
| p089 | 這樣的雨滴，一秒可以落下六、七公尺，比雲滴快好幾百倍。 | Tetes hujan jatuh 6–7 m/detik, ratusan kali tetes awan. | Tetes hujan seperti ini bisa jatuh 6–7 m per detik, ratusan kali lebih cepat dari tetes awan. | 補回「快」 |
| p090 | 雲本身還在，只是裡面長大的那些，一批一批離開。 | Awannya tetap; yang sudah besar pergi bergiliran. | Awannya tetap ada; hanya tetes yang sudah besar yang pergi, gelombang demi gelombang. | 語句修正 |
| p091 | 可是我家旁邊的雲，有的下雨，有的整天都不下。 | Ada awan yang hujan, ada yang seharian tidak. | Tapi awan di dekat rumahku, ada yang hujan, ada yang seharian tidak. | 補回「我家旁邊」 |
| p095 | 會下大雨的，是一路往上衝的雲。 | Hujan lebat dari awan menjulang. | Yang membawa hujan lebat adalah awan yang terus menjulang. | 補回「一路往上衝」 |
| p096 | 雲頂可以超過十公里，跟客機一樣高，甚至更高。 | Puncaknya lewat 10 km, setinggi jet atau lebih. | Puncaknya bisa lewat 10 km, setinggi pesawat penumpang atau lebih. | 客機 |
| p097 | 那麼高！那要很多熱空氣才推得上去吧。 | Wah! Butuh banyak udara hangat, dong. | Setinggi itu! Pasti butuh banyak udara hangat untuk mendorongnya. | 補回「推得上去」 |
| p100 | 很多人都這樣猜。太陽最高是中午，可是地面和空氣最熱，通常要再晚一點。 | Tebakan umum. Matahari tertinggi jam 12, tapi tanah dan udara terpanas sesudahnya. | Banyak yang menebak begitu. Matahari tertinggi jam 12, tapi tanah dan udara biasanya paling panas agak lebih siang. | 補回「通常」，保留兩段順序 |
| p101 | 就像鍋子放上爐子，火一開，鍋子不會馬上最燙，要燒一段時間。 | Seperti panci di kompor: tak langsung panas, butuh waktu. | Seperti panci di kompor: begitu api menyala, panci tak langsung paling panas, butuh waktu. | 補回「火一開」 |
| p103 | 那為什麼台灣特別多？ | Kenapa Taiwan sering? | Terus kenapa di Taiwan sering banget? | 補回「特別多」 |
| p105 | 還有山。山坡把空氣往上抬，雲就特別容易在山邊長起來。 | dan gunung. Lereng mendorong udara naik, awan mudah tumbuh di sana. | dan gunung. Lereng gunung mendorong udara naik, jadi awan mudah tumbuh di sekitar gunung. | 語句修正 |
| p107 | 對，它長得又高又厚，陽光透不過來，底部看起來就是灰的。 | Ya. Tinggi dan tebal, cahaya tak tembus, dasarnya tampak abu-abu. | Ya. Awannya tinggi dan tebal, cahaya matahari tak tembus, jadi dasarnya tampak abu-abu. | 語句修正 |
| p108 | 那為什麼雷陣雨常常下一下就停？ | Kenapa hujan badai sering cepat berhenti? | Terus kenapa badai petir sering cepat berhenti? | 與說明、標籤的「badai petir」一致 |
| p109 | 因為一場大雨，會把自己的引擎關掉。 | Hujan deras mematikan mesinnya. | Karena hujan deras mematikan mesinnya sendiri. | 補回「自己的」 |
| p110 | 雨落下來，會把周圍的空氣一起往下拖；雨在半路蒸發，又讓這團空氣更冷。 | Hujan menyeret udara turun; yang menguap di jalan membuat udara itu makin dingin. | Hujan yang jatuh menyeret udara sekitarnya ikut turun; hujan yang menguap di jalan membuat udara itu makin dingin. | 補回「周圍」，保留兩段順序 |
| p111 | 你在雷雨前感覺到的那陣涼風，常常就是它衝到了地面。 | Angin sejuk sebelum badai sering berasal dari udara ini. | Angin sejuk yang kamu rasakan sebelum badai sering adalah udara ini yang menghantam tanah. | 補回「你感覺到的」「衝到地面」 |
| p113 | 冷空氣往下灌，把往上送的熱空氣擋掉了。 | Udara dingin menghadang udara hangat. | Udara dingin turun dan menghadang udara hangat yang naik. | 補回「往下灌」「往上送的」 |
| p114 | 沒有熱空氣補進來，雲就慢慢沒力。 | Tanpa udara hangat, awan melemah. | Tanpa pasokan udara hangat, awan pelan-pelan melemah. | 補回「補進來」「慢慢」 |
| p115 | 還記得你問要多久嗎？ | Berapa lamanya? | Ingat kamu tanya berapa lama? | 補回「還記得你問」 |
| p116 | 一個單獨的雷雨雲，從長大到散掉，常常不到一小時。 | Awan badai tunggal sering tumbuh dan hilang kurang dari sejam. | Satu awan badai petir, dari tumbuh sampai hilang, sering kurang dari sejam. | 語句修正 |
| p118 | 空氣夠不夠濕、上面夠不夠冷、風怎麼吹，只要一個條件不對，雲就長不起來。 | Lembap udaranya, dingin di atas, arah angin: satu tak pas, awan tak bisa tumbuh. | Udaranya cukup lembap atau tidak, di atas cukup dingin atau tidak, anginnya bagaimana: satu saja tak pas, awan tak bisa tumbuh. | 補回「夠不夠」，保留兩段順序 |
| p121 | 還記得花椰菜嗎？那代表裡面的空氣還在往上衝。 | Ingat kembang kol? Udaranya masih naik. | Ingat kembang kol? Itu tanda udara di dalamnya masih naik. | 補回「代表」 |
| p126 | 還記得那陣涼風嗎？冷空氣已經跑在雨的前面了。我一開始說什麼？ | Ingat anginnya? Udara dingin mendahului hujan. Aku bilang apa? | Ingat angin sejuk itu? Udara dingin sudah mendahului hujan. Tadi aku bilang apa? | 補回「一開始」 |
| p129 | 大家都這樣畫，可是不是。 | Biasa digambar. Salah. | Semua orang menggambarnya begitu, tapi bukan. | 「Salah」語氣太硬，補回「大家都這樣畫」 |
| p130 | 雨滴掉得越快，空氣從下面擋得越用力。 | Makin cepat jatuh, makin kuat udara menahan. | Makin cepat tetes jatuh, makin kuat udara menahan dari bawah. | 補回「從下面」 |
| p132 | 再大，就被扯開，碎成好幾顆。所以雨滴不會一直長下去。 | Lebih besar, ia pecah jadi beberapa. Tetes tak bisa membesar terus. | Lebih besar lagi, ia robek dan pecah jadi beberapa. Jadi tetes hujan tak bisa membesar terus. | 補回「扯開」「所以」 |
| p134 | 衣服都收進來了，雨也停了。真的不到一個小時。 | Jemuran masuk, hujan reda. Tak sampai sejam! | Jemuran sudah masuk, hujan juga reda. Benar-benar tak sampai sejam! | 補回「真的」 |
| p136 | 引擎關掉，雲就散了。 | Mesinnya mati. | Mesinnya mati, awannya pun buyar. | 補回「雲就散了」 |
| p137 | 打在你手上的每一顆，都是一百萬顆雲滴湊起來的。 | Tiap tetes di tanganmu gabungan sekitar sejuta tetes awan. | Tiap tetes yang kena tanganmu adalah gabungan sekitar sejuta tetes awan. | 語句修正 |
| p138 | 還記得那些小水滴嗎？它們不是不會掉，是在等長大！ | Tetes kecil itu bukan tak jatuh. Ia menunggu besar! | Ingat tetes kecil itu? Mereka bukan tak jatuh, tapi menunggu besar! | 補回「還記得」 |
| p139 | 原來如此！ | Begitu! | Oh, begitu! | 系列口號完整形 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | Hujan sore di sana jam berapa? Komen ya. | Hujan badai sore di tempatmu biasanya mulai jam berapa? Tulis di komentar, ya. | 補回「通常」「開始」 |
| p141 | 想一起把生活裡的為什麼找到底，就訂閱原來如此事務所。 | Mau ungkap semua 'kenapa' sehari-hari? Subscribe Kantor Oh Begitu. | Mau sama-sama mengungkap 'kenapa' dalam hidup sehari-hari sampai tuntas? Subscribe Kantor Oh Begitu. | 補回「一起」「找到底」 |

## vi（越南文）— 改 10 句

**結論**：第二好的一份，完整、口語自然、稱謂（cô／cháu）一致；只修稱謂不一致（p042）、「相對」與幾處不自然的句子。可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p042 | 聽起來很嚇人對吧？你家上面現在，可能也正浮著一朵。 | Nghe đáng sợ nhỉ? Có khi ngay lúc này cũng có một đám trên nhà bạn. | Nghe đáng sợ nhỉ? Có khi ngay lúc này trên nhà cháu cũng đang có một đám. | 所長對小問一律稱「cháu」，「bạn」不一致 |
| p043 | 等一下，空氣也有重量吧？ | Khoan, không khí cũng nặng chứ? | Khoan, không khí cũng có cân nặng chứ ạ? | 「nặng」= 很重，原文是「也有重量」 |
| p052 | 東西越小，空氣擋它的力量相對越大。 | Vật càng nhỏ, sức cản không khí càng lớn. | Vật càng nhỏ, sức cản của không khí so với nó càng lớn. | 補回「相對」 |
| p081 | 所以我淋到的雨，可能原本是雪？ | Vậy mưa cháu dính có khi vốn là tuyết? | Vậy mưa rơi vào người cháu có khi vốn là tuyết ạ? | 「mưa cháu dính」不自然 |
| p087 | 掉下來的，是已經長大的水滴。 | Rơi xuống là giọt đã lớn. | Thứ rơi xuống là những giọt đã lớn. | 語句修正 |
| p111 | 你在雷雨前感覺到的那陣涼風，常常就是它衝到了地面。 | Cơn gió mát cháu thấy trước dông thường chính là nó lao xuống mặt đất. | Cơn gió mát cháu cảm thấy trước cơn dông thường chính là khối khí đó lao xuống mặt đất. | 「nó」指涉不清 |
| p115 | 還記得你問要多久嗎？ | Nhớ cháu hỏi bao lâu? | Cháu còn nhớ cháu hỏi mất bao lâu không? | 原句不完整 |
| p125 | 啊，突然好涼！衣服都飛起來了！ | Á, tự nhiên mát quá! Quần áo bay hết rồi! | Á, tự nhiên mát quá! Quần áo bay phần phật hết rồi! | 「bay hết」像被吹走，原文是飛起來 |
| p129 | 大家都這樣畫，可是不是。 | Ai cũng vẽ thế, nhưng sai. | Ai cũng vẽ thế, nhưng không phải đâu. | 「sai」對孩子語氣太硬 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | Chỗ bạn, dông chiều thường mấy giờ? Kể bọn mình nhé. | Chỗ bạn ở, mưa dông buổi chiều thường bắt đầu lúc mấy giờ? Bình luận kể bọn mình nghe nhé. | 補回「開始」「留言」 |

## th（泰文）— 改 39 句

**結論**：數字正確，但多句壓縮：掉了「直徑」（p064，下一句靠它）、「常常」「還記得」，所長對小問的稱謂 p042 混用「คุณ」，口號只有「อ๋อ!」。系列名「สำนักงานอ๋อเป็นอย่างนี้」與口號「อ๋อ อย่างนี้นี่เอง」字面不同，但全片一致，未更動。修後可上架。

| id | 原文 | 舊 | 新 | 原因 |
|---|---|---|---|---|
| p001 | 所長！所長！我家陽台外面那朵雲，一直往上長。 | หัวหน้า! เมฆนอกระเบียงบ้านหนูสูงขึ้นเรื่อยๆ | หัวหน้า! หัวหน้า! เมฆนอกระเบียงบ้านหนูสูงขึ้นเรื่อยๆ เลย! | 補回重複呼喊 |
| p009 | 水不是比空氣重嗎？ | น้ำหนักกว่าอากาศนี่ | น้ำหนักกว่าอากาศไม่ใช่เหรอ | 原文是反問句 |
| p012 | 太陽把地面曬熱，地面再把貼著它的那層空氣烤熱。 | แดดเผาพื้นให้ร้อน พื้นก็อบอากาศที่ติดอยู่ให้ร้อน | แดดเผาพื้นให้ร้อน พื้นก็อบอากาศชั้นที่แนบพื้นให้ร้อน | 補回「貼著它的那層」 |
| p022 | 就像熱氣球？ | เหมือนบอลลูน? | เหมือนบอลลูนลมร้อนเหรอ | 熱氣球 |
| p025 | 在還沒有凝結之前，往上爬的空氣，每升高一公里大約冷十度。 | ก่อนควบแน่น อากาศที่ลอยขึ้นจะเย็นลงราว 10 องศาทุก 1 กม. | ก่อนควบแน่น อากาศที่ลอยขึ้นจะเย็นลงราว 10 องศาเซลเซียสทุก 1 กม. | 補單位 |
| p027 | 就像你夏天拿冰飲料，杯子外面會冒出水珠。 | เหมือนแก้วน้ำเย็นที่มีหยดน้ำเกาะข้างนอก | เหมือนหน้าร้อนถือแก้วน้ำเย็น แล้วมีหยดน้ำเกาะข้างนอกแก้ว | 補回「夏天」 |
| p029 | 好問題。空氣裡有很多你看不到的小顆粒：灰塵、海鹽、煙。 | ถามดี ในอากาศมีอนุภาคเล็กๆ ที่มองไม่เห็นเยอะมาก ฝุ่น เกลือทะเล ควัน | ถามดีมาก ในอากาศมีอนุภาคเล็กๆ ที่มองไม่เห็นเยอะมาก ฝุ่น เกลือทะเล ควัน | 「ถามดี」不自然 |
| p042 | 聽起來很嚇人對吧？你家上面現在，可能也正浮著一朵。 | น่ากลัวใช่ไหม ตอนนี้เหนือบ้านคุณก็อาจมีอยู่ก้อนหนึ่ง | น่ากลัวใช่ไหม ตอนนี้เหนือบ้านหนูก็อาจมีอยู่ก้อนหนึ่ง | 所長對小問稱「หนู」，「คุณ」不一致 |
| p043 | 等一下，空氣也有重量吧？ | เดี๋ยว อากาศก็มีน้ำหนักนะ | เดี๋ยว อากาศก็มีน้ำหนักใช่ไหม | 原文是問句 |
| p052 | 東西越小，空氣擋它的力量相對越大。 | ยิ่งเล็ก อากาศยิ่งต้านแรง | ยิ่งของเล็ก แรงต้านของอากาศก็ยิ่งมากเมื่อเทียบกับตัวมัน | 補回「相對」 |
| p054 | 一顆雲滴在不動的空氣裡，一秒大概只掉一公分左右。 | ในอากาศนิ่ง หยดเมฆตกวินาทีละราว 1 ซม. | ในอากาศนิ่ง หยดเมฆตกแค่ราว 1 ซม. ต่อวินาที | 補回「只」 |
| p055 | 那比走路還慢好多吧！ | ช้ากว่าเดินอีก! | ช้ากว่าเดินอีกเยอะเลย! | 補回「好多」 |
| p064 | 你淋過的雨滴，常見的大約兩公釐，直徑是雲滴的一百倍。 | เม็ดฝนทั่วไปราว 2 มม. ใหญ่กว่าหยดเมฆ 100 เท่า | เม็ดฝนที่หนูเคยโดนมักราว 2 มม. เส้นผ่านศูนย์กลางเป็น 100 เท่าของหยดเมฆ | 補回「直徑」——下一句要靠它 |
| p065 | 才一百倍？那還好嘛。 | แค่ 100 เท่าเอง? | แค่ 100 เท่าเอง? ไม่เท่าไหร่นี่ | 補回「那還好嘛」 |
| p066 | 是直徑喔。體積是長、寬、高三個方向都要乘。 | นั่นเส้นผ่านศูนย์กลาง ปริมาตรต้องคูณสามทิศ | นั่นเส้นผ่านศูนย์กลาง ปริมาตรต้องคูณทั้งสามทาง กว้าง ยาว สูง | 補回三個方向 |
| p076 | 雲爬到夠高的地方，溫度會降到零度以下。那裡會有小冰晶， | เมฆที่สูงพอ อุณหภูมิจะต่ำกว่า 0 องศา มีผลึกน้ำแข็งเล็กๆ | เมื่อเมฆขึ้นไปสูงพอ อุณหภูมิจะต่ำกว่า 0 องศา ตรงนั้นมีผลึกน้ำแข็งเล็กๆ | 語句修正 |
| p088 | 重到上升的空氣托不住，就穿出雲底。 | หนักจนลมขึ้นอุ้มไม่ไหว ก็หลุดออกจากฐานเมฆ | หนักจนอากาศที่ลอยขึ้นอุ้มไม่ไหว ก็หลุดออกจากฐานเมฆ | 「ลมขึ้น」→上升的空氣，用詞一致 |
| p091 | 可是我家旁邊的雲，有的下雨，有的整天都不下。 | แต่เมฆแถวบ้านหนู บางก้อนตก บางก้อนไม่ตกเลย | แต่เมฆแถวบ้านหนู บางก้อนตก บางก้อนไม่ตกเลยทั้งวัน | 補回「整天」 |
| p095 | 會下大雨的，是一路往上衝的雲。 | ฝนหนักมาจากเมฆที่พุ่งสูง | ที่ทำให้ฝนตกหนักคือเมฆที่พุ่งสูงขึ้นไปเรื่อยๆ | 補回「一路往上衝」 |
| p096 | 雲頂可以超過十公里，跟客機一樣高，甚至更高。 | ยอดเมฆเกิน 10 กม. สูงเท่าเครื่องบินหรือสูงกว่า | ยอดเมฆสูงเกิน 10 กม. ได้ สูงเท่าเครื่องบินโดยสารหรือสูงกว่า | 客機 |
| p097 | 那麼高！那要很多熱空氣才推得上去吧。 | สูงขนาดนั้น! ต้องใช้อากาศร้อนเยอะแน่ | สูงขนาดนั้น! ต้องใช้อากาศร้อนเยอะแน่ๆ ถึงจะดันขึ้นไปได้ | 補回「推得上去」 |
| p102 | 所以熱空氣往上送得最兇的時候，常常落在下午。 | อากาศร้อนจึงพุ่งขึ้นแรงสุดตอนบ่าย | อากาศร้อนจึงมักพุ่งขึ้นแรงสุดตอนบ่าย | 補回「常常」 |
| p103 | 那為什麼台灣特別多？ | ทำไมไต้หวันเยอะ | แล้วทำไมไต้หวันมีเยอะเป็นพิเศษ | 補回「特別」 |
| p104 | 因為台灣的夏天還多了兩個幫手：從海上吹進陸地的濕空氣， | เพราะหน้าร้อนไต้หวันมีตัวช่วยอีกสอง อากาศชื้นที่พัดจากทะเล | เพราะหน้าร้อนไต้หวันมีตัวช่วยอีกสอง อากาศชื้นที่พัดจากทะเลเข้าฝั่ง | 補回「吹進陸地」 |
| p108 | 那為什麼雷陣雨常常下一下就停？ | ทำไมพายุฝนตกแป๊บเดียวก็หยุด | แล้วทำไมพายุฝนฟ้าคะนองมักตกแป๊บเดียวก็หยุด | 補回「常常」，用詞與標籤一致 |
| p109 | 因為一場大雨，會把自己的引擎關掉。 | เพราะฝนหนักดับเครื่องตัวเอง | เพราะฝนหนักจะดับเครื่องยนต์ของตัวเอง | 語句修正 |
| p110 | 雨落下來，會把周圍的空氣一起往下拖；雨在半路蒸發，又讓這團空氣更冷。 | ฝนที่ตกลากอากาศรอบตัวลงมา ฝนระเหยกลางทาง ทำให้อากาศยิ่งเย็น | ฝนที่ตกลงมาลากอากาศรอบๆ ลงมาด้วย ฝนที่ระเหยกลางทางยังทำให้อากาศก้อนนี้ยิ่งเย็น | 補回「一起」「這團」，保留兩段順序 |
| p111 | 你在雷雨前感覺到的那陣涼風，常常就是它衝到了地面。 | ลมเย็นก่อนพายุ มักเป็นอากาศนี้ที่พุ่งถึงพื้น | ลมเย็นที่หนูรู้สึกก่อนพายุ มักเป็นอากาศก้อนนี้ที่พุ่งลงถึงพื้น | 補回「你感覺到的」 |
| p113 | 冷空氣往下灌，把往上送的熱空氣擋掉了。 | ลมเย็นพุ่งลง กันอากาศร้อนไว้ | อากาศเย็นพุ่งลง กันอากาศร้อนที่ลอยขึ้นไว้ | 補回「往上送的」 |
| p114 | 沒有熱空氣補進來，雲就慢慢沒力。 | ไม่มีอากาศร้อนเติม เมฆก็หมดแรง | ไม่มีอากาศร้อนมาเติม เมฆก็ค่อยๆ หมดแรง | 補回「慢慢」 |
| p115 | 還記得你問要多久嗎？ | นานแค่ไหนนะ | จำได้ไหมที่หนูถามว่านานแค่ไหน | 補回「還記得你問」 |
| p121 | 還記得花椰菜嗎？那代表裡面的空氣還在往上衝。 | จำกะหล่ำได้ไหม แปลว่าลมยังพุ่งขึ้น | จำดอกกะหล่ำได้ไหม แปลว่าอากาศข้างในยังพุ่งขึ้นอยู่ | 「ลม」→「อากาศข้างใน」 |
| p126 | 還記得那陣涼風嗎？冷空氣已經跑在雨的前面了。我一開始說什麼？ | จำลมเย็นได้ไหม ลมเย็นมาก่อนฝนแล้ว ตอนแรกบอกว่าอะไร | จำลมเย็นได้ไหม อากาศเย็นวิ่งนำหน้าฝนมาแล้ว ตอนแรกบอกไว้ว่าอะไรนะ | 補回「冷空氣跑在雨前面」「一開始」 |
| p129 | 大家都這樣畫，可是不是。 | วาดกันผิดนะ | ใครๆ ก็วาดแบบนั้น แต่ไม่ใช่นะ | 補回「大家都這樣畫」 |
| p132 | 再大，就被扯開，碎成好幾顆。所以雨滴不會一直長下去。 | ใหญ่กว่านั้นจะถูกฉีกแตก เม็ดฝนจึงโตไปเรื่อยๆ ไม่ได้ | ใหญ่กว่านั้นจะถูกฉีกแตกเป็นหลายเม็ด เม็ดฝนจึงโตไปเรื่อยๆ ไม่ได้ | 補回「碎成好幾顆」 |
| p136 | 引擎關掉，雲就散了。 | ดับ เมฆก็สลาย | เครื่องดับ เมฆก็สลายไป | 補回「引擎」 |
| p139 | 原來如此！ | อ๋อ! | อ๋อ อย่างนี้นี่เอง! | 系列口號完整形 |
| p140 | 你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。 | พายุบ่ายแถวบ้านคุณเริ่มกี่โมง เม้นเลย | พายุฝนฟ้าคะนองช่วงบ่ายแถวบ้านคุณมักเริ่มกี่โมง คอมเมนต์บอกเราหน่อยนะ | 補回「通常」、語氣較溫和 |
| p141 | 想一起把生活裡的為什麼找到底，就訂閱原來如此事務所。 | อยากหาคำตอบทุกทำไมในชีวิต กดติดตาม สำนักงานอ๋อเป็นอย่างนี้ | อยากตามหาคำตอบของทุก 'ทำไม' ในชีวิตไปด้วยกัน กดติดตามสำนักงานอ๋อเป็นอย่างนี้ | 補回「一起」「找到底」 |
