import json, itertools, sys
SLUG = "sothatswhy-p02-cloud-rain"
ACC = "標準國語，咬字清楚，台北人平常說話的語調"
CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])

# scene tuples: (id, chapter or None, template, data, lines)
# shot data shorthand: ("P", prompt, chars, camera or None)
# lines: list of (speaker 'K'|'C', text, emotion or None, loop tag or None)
S = []
def shot(id, prompt, chars=(), lines=(), chapter=None, cam=None):
    S.append(dict(id=id, chapter=chapter, template="shot", data=dict(prompt=prompt, camera=cam or next(CAMS), visual="still", characters=list(chars)), lines=list(lines)))
def card(id, template, data, lines=(), chapter=None):
    S.append(dict(id=id, chapter=chapter, template=template, data=data, lines=list(lines)))
K, C = "kid", "chief"
def k(t, e=None, tag=None): return (K, t, e, tag)
def c(t, e=None, tag=None): return (C, t, e, tag)

KID = ["kid"]; CH = ["chief"]
# ---------- 開場（片頭動畫之後直接開始，不做濃縮）----------
CH0 = "陽台外那朵雲變灰了"
shot("balcony-call", "Medium shot of a girl on a small apartment balcony in the early afternoon, leaning on the railing and pointing up at the sky with wide excited eyes, laundry hanging beside her, soft daylight from above", KID,
     [k("所長！所長！我家陽台外面那朵雲，一直往上長。", "興奮，跑進來報案的語氣")], chapter=CH0)
shot("tower-greying", "Low angle wide shot of one tall puffy cloud rising over apartment rooftops in the afternoon, its top bright white and its flat bottom turning grey, a single rooftop water tank in the corner, soft light from the upper left", (),
     [k("剛剛還白白的，現在下面變成灰色了。", "疑惑", "S:grey")])
shot("chief-folder", "Medium shot of a friendly office chief at a wooden desk by a window, looking up from an open blank folder with an amused smile, a window behind her, warm lamp light on the desk", CH,
     [c("那你等一下可能要收衣服了。", "輕鬆，帶笑")])
shot("kid-puzzled", "Close-up of a girl frowning in thought, holding a small blank notebook against her chest, standing in a bright doorway, soft daylight from the side", KID,
     [k("可是我想不通。雲裡面，真的有水嗎？", "認真發問，句尾上揚")])
shot("chief-yes", "Medium close-up of the chief holding up a magnifying glass and nodding warmly, bookshelves of blank folders behind her, soft afternoon light from a window", CH,
     [c("有，而且很多。你抬頭看到的那一整片白色，裡面有很多水。", "肯定，語氣親切")])
shot("kid-why-not-fall", "Close-up of a girl with her finger on her chin and eyebrows raised, looking up and to the side as if picturing something heavy overhead, a plain wall behind her, soft light", KID,
     [k("水不是比空氣重嗎？", "不服氣"), k("那它為什麼沒有整團掉下來？", "句尾上揚", "S:nofall")])
shot("chief-window", "Medium shot of the chief standing at an open window with her hands behind her back, gazing up at a big white cloud outside, gentle afternoon light on her face", CH,
     [c("這個問題，你每年夏天其實都看過答案，只是沒有人跟你說。", "賣關子，放慢")])
shot("town-cloud-wide", "Wide shot of a small city in summer afternoon, one huge cloud tower rising behind the buildings, a single scooter rider stopped at a crossing and looking up at it, soft hazy light", (),
     [c("先猜猜看：你家外面那朵雲，大概有幾頭大象那麼重？", "賣關子", "S:elephant")])
shot("drop-on-nose", "Extreme close-up of one big raindrop landing on the tip of a girl's nose as she looks up, her eyes crossed comically, grey sky behind her", KID,
     [c("還有，它會不會變成打在你身上的雨？要多久？", "最後幾個字放慢", "S:hour")])

# ---------- 第一章 ----------
CH1 = "早上一團熱空氣往上爬"
shot("clear-morning", "Wide shot of the same apartment balcony on a clear morning, a girl hanging a towel on the laundry line, the sky completely empty of clouds, soft early light from the left", KID,
     [c("這朵雲，今天早上還不存在。那時候天空很乾淨，一朵雲都沒有。", "說故事的開頭")], chapter=CH1)
shot("hot-street", "Medium shot of a delivery rider in a helmet wiping sweat from his forehead beside his scooter on a hot city street, faint heat shimmer rising from the road, mild hazy daylight", (),
     [c("太陽把地面曬熱，地面再把貼著它的那層空氣烤熱。")])
shot("kid-vapour-guess", "Medium shot of a girl sitting on a tall stool swinging her legs and raising one hand like asking a question in class, plain background, soft light", KID,
     [k("那雲是從哪裡跑出來的？是水蒸氣嗎？", "很有把握的猜", "S:vapour")])
shot("chief-kettle", "Medium shot of the chief in a small kitchenette pointing at a steaming kettle on a stove, a mug waiting beside it, soft lamp light", CH,
     [c("很多人都這樣想。不過你先看這個。", "神秘一點")])
shot("spout-gap", "Extreme close-up of a kettle spout with a clear gap of empty air right at the opening and a white puff of mist starting a little further out, plain wall behind, soft lamp light", (),
     [c("燒開水的時候，最靠近壺嘴的那一小段，其實是透明的。")])
shot("mist-puff", "Extreme close-up of a white puff of mist curling in the air a hand's width away from a kettle spout, the air right at the spout clear, soft kitchen light", (),
     [c("白色的霧，要離開壺嘴一點點才出現。")])
shot("kid-not-vapour", "Close-up of a girl leaning in with big surprised eyes and her mouth in a small O, looking at something just off frame, soft kitchen light", KID,
     [k("所以白白的那個，不是水蒸氣？", "驚訝")])
shot("chief-explains-mist", "Medium close-up of the chief holding a mug and smiling knowingly, a faint wisp of mist above the mug, soft lamp light", CH,
     [c("對。真正的水蒸氣是看不見的。白白的，是它冷下來，又變回的小水滴。", None, "P:vapour")])
card("vapour-vs-cloud", "compare", {"title": "白白的不是水蒸氣", "left": {"heading": "水蒸氣", "points": ["氣體", "看不見"]}, "right": {"heading": "雲", "points": ["很小的水滴或冰晶", "看得見"]}, "source": "NOAA JetStream：雲的形成"},
     [c("雲也是一樣。它是很多很小的水滴，有時候是小冰晶，不是一團氣。")])
shot("kid-who-cools", "Medium shot of a girl looking up at an empty sky from a rooftop and spreading her empty hands with a puzzled shrug, soft daylight", KID,
     [k("可是天上又沒有水壺，誰把它變冷的？", "抓到漏洞的語氣")])
shot("warm-bubble", "Wide shot of a sunlit town rooftop at late morning, a large transparent shimmering bubble of warm air lifting off a hot rooftop into the sky, one pigeon on the ledge watching it, mild light", (),
     [c("答案是往上爬。被曬熱的空氣比旁邊輕，會一團一團往上浮。")])
shot("kid-balloon", "Medium shot of a girl holding the string of a red balloon and watching it pull upward, standing in a small park, soft afternoon light", KID,
     [k("就像熱氣球？", "好奇")])
shot("mountain-hike", "Medium shot of a hiker in a light jacket on a mountain trail zipping the jacket up to the chin with a shiver, a valley far below, overcast soft light", (),
     [c("有點像。而且你應該有感覺過：爬山爬得越高，就越涼。")])
shot("chief-expands", "Medium shot of the chief stretching a big rubber balloon between her hands at her desk as if showing it swell, an amused look, warm desk lamp", CH,
     [c("空氣往上走，周圍的氣壓變小，它就膨脹；一膨脹，就會變冷。")])
card("lapse-rate", "big", {"kicker": "往上爬的乾空氣", "text": "每 1 公里 **冷約 10°C**", "sub": "還沒有凝結的時候"},
     [c("在還沒有凝結之前，往上爬的空氣，每升高一公里大約冷十度。", "數字放慢")])
shot("condense-high", "Wide shot of a rising pocket of warm air high above a town turning into the first wisps of white cloud, a single paraglider drifting nearby, soft bright light", (),
     [c("冷到某個高度，水氣就飽和了，多出來的就會凝結。")])
shot("iced-cup", "Close-up of a girl's fingertip touching beads of water on the outside of a glass of iced tea on a café table, soft daylight from a window", KID,
     [c("就像你夏天拿冰飲料，杯子外面會冒出水珠。")])
shot("kid-what-to-cling", "Close-up of a girl tilting her head and squinting with one eye closed, holding the cold glass up to the light, soft café light", KID,
     [k("杯子外面有杯子給它黏，天上有什麼可以黏？", "反問，有點得意", "S:nuclei")])
shot("chief-magnifier", "Medium close-up of the chief peering through a large magnifying glass at a beam of window light full of tiny floating dust specks, delighted expression", CH,
     [c("好問題。空氣裡有很多你看不到的小顆粒：灰塵、海鹽、煙。")])
shot("nucleus-droplet", "Extreme close-up illustration of one tiny speck of sea salt floating in the air with a round water droplet forming around it, a few more specks and droplets drifting in the soft white background", (),
     [c("水氣就是在這些小顆粒上，凝結成一顆一顆小水滴。", None, "P:nuclei")])
shot("flat-bases", "Wide shot of a row of puffy clouds over green rice fields, every cloud with the same flat bottom at the same height, a single farmer in a straw hat looking up from the field, soft overcast-bright light", (),
     [c("所以你看積雲，底部常常是平的：那個高度，剛好是空氣冷到開始凝結的地方。")])
shot("kid-flat-bottoms", "Medium shot of a girl lying on her back on a grassy riverbank pointing up at the sky and laughing, her notebook beside her, soft afternoon light", KID,
     [k("真的耶，每一朵的屁股都一樣平！", "笑出來")])
shot("cauliflower-grow", "Low angle wide shot of a puffy cloud bulging upward in round lumps like a cauliflower over a hillside, one kite flying below it, soft bright afternoon light", (),
     [c("只要下面一直有熱空氣送上來，這朵雲就會一直往上長，長得像一顆花椰菜。")])
shot("kid-how-much", "Close-up of a girl writing in her small notebook with her tongue poking out in concentration, sitting on the riverbank grass, soft light", KID,
     [k("那這一大朵，總共有多少水？", "認真，章尾停住", "S:weight")])

# ---------- 第二章 ----------
CH2 = "五百公噸搭著電梯往上"
shot("chief-whiteboard", "Medium shot of the chief drawing a big cube with a marker on a blank whiteboard, glancing back over her shoulder with a grin, soft daylight", CH,
     [c("我們來算一朵普通的積雲。假設它差不多是一個長寬高各一公里的大方塊。")], chapter=CH2)
card("cloud-weight", "stats", {"title": "一朵積雲（估算）", "stats": [{"value": "1 立方公里", "label": "雲的大小"}, {"value": "約 0.5 公克", "label": "每立方公尺的水"}, {"value": "約 500 公噸", "label": "整朵雲的水"}], "source": "USGS 水科學學校：一朵雲有多重"},
     [c("雲裡的水其實很稀，每一立方公尺，大概只有半公克。", "數字放慢", None), c("可是一立方公里，有十億個立方公尺。")])
shot("kid-calc", "Close-up of a girl staring wide-eyed at her notebook full of scribbled zeros, pencil frozen in her hand, plain background, soft light", KID,
     [k("十億個半公克……那是多少？", "算不出來"), c("大約五百公噸。", "停一拍再說", "P:weight")])
shot("elephants", "Wide shot of a long parade of elephants walking across a dry plain in a single line toward the horizon, one big cloud above them, soft hazy light", (),
     [c("差不多是一百頭大象那麼重。", None, "P:elephant")])
shot("kid-elephants", "Medium shot of a girl hugging her head with both hands and looking up in mock panic, standing on the balcony, a big cloud overhead, soft afternoon light", KID,
     [k("那麼多大象浮在我家上面？！", "誇張驚嚇，好笑")])
shot("chief-laugh", "Medium close-up of the chief laughing with one hand on her belly at her desk, a mug beside her, warm lamp light", CH,
     [c("聽起來很嚇人對吧。不過你先別急著跑。", "笑著，然後收")])
shot("kid-air-heavy", "Medium shot of a girl on the balcony weighing an empty paper bag in her raised hand with a doubtful frown, soft afternoon light", KID,
     [k("等一下，空氣也有重量吧？", "突然想到")])
card("air-weight", "big", {"kicker": "同一立方公里的空氣", "text": "約 **100 萬公噸**", "sub": "雲裡的水，只占約兩千分之一"},
     [c("有，而且更重。同樣一立方公里的空氣，大約有一百萬公噸。", "數字放慢")])
shot("kid-tiny-part", "Close-up of a girl holding a pinch of sugar between two fingers above a big glass jug of water and squinting at it, soft kitchen light", KID,
     [k("所以那些水，只是混在空氣裡面的一點點？", "恍然大悟一半")])
shot("chief-second", "Medium shot of the chief holding up two fingers with a serious but kind face, standing by the whiteboard with the cube drawing, soft daylight", CH,
     [c("對。而且這些水不是一大塊，是分成非常非常多顆。", None)])
card("droplet-size", "big", {"kicker": "一顆雲滴", "text": "約 **0.02** 公釐", "sub": "比一根頭髮還細好幾倍"},
     [c("一顆普通的雲滴，直徑大約百分之二公釐，比一根頭髮還細好幾倍。", "數字放慢")])
shot("kid-no-weight", "Medium shot of a girl holding up a single strand of her own hair and studying it closely, sitting at a desk, soft window light", KID,
     [k("那它太小了，所以就沒有重量了？", "很有把握的錯猜", None)])
shot("chief-falls-slowly", "Medium close-up of the chief shaking her head gently and holding her thumb and finger very close together, warm lamp light", CH,
     [c("有重量，它也真的一直在往下掉。只是掉得非常、非常慢。", "否定但溫和")])
shot("feather-stone", "Medium shot of a girl on a balcony letting go of a feather and a pebble at the same time from her two raised hands, the pebble already lower than the feather, soft daylight", KID,
     [c("你想想看，一顆石頭和一根羽毛一起放手，哪個先落地？"), k("石頭啊。", "理所當然")])
shot("chief-air-holds", "Medium shot of the chief holding a tiny paper scrap in her palm in front of a desk fan, the scrap lifting off her palm, playful look, soft light", CH,
     [c("東西越小，空氣擋住它的力量相對就越大。小到像雲滴那樣，空氣幾乎把它托住了。")])
card("fall-speed", "compare", {"title": "在不動的空氣裡，每秒掉多少", "left": {"heading": "雲滴 0.02 公釐", "points": ["每秒約 1 公分"]}, "right": {"heading": "雨滴 2 公釐", "points": ["每秒約 6–7 公尺"]}, "source": "華盛頓大學大氣科學課程；夏威夷大學大氣教科書"},
     [c("一顆雲滴在不動的空氣裡，一秒大概只掉一公分左右。", "數字放慢")])
shot("kid-snail", "Close-up of a girl crouching on a garden path watching a snail crawl along a ruler laid on the ground, chin in her hands, soft overcast light", KID,
     [k("那跟蝸牛差不多吧！", "好笑")])
shot("chief-a-day", "Medium shot of the chief pointing at a big wall clock with a thoughtful face, her other hand holding a blank folder, soft daylight", CH,
     [c("差不多。照這個速度，從一公里高的雲底掉到地上，要超過一天。")])
shot("droplet-vanish", "Extreme close-up of one tiny water droplet drifting down through dry air and shrinking into nothing, a few faint wisps around it, soft bright background", (),
     [c("而且它還沒掉到，半路就蒸發掉了。")])
shot("kid-but-stays", "Medium shot of a girl on the balcony with her hands on her hips glaring up at a cloud that hasn't moved, soft afternoon light", KID,
     [k("可是雲一整個下午都在，它也沒有慢慢變矮啊。", "抓到漏洞")])
shot("chief-remember", "Medium close-up of the chief raising one finger and smiling as if a clue just came back to her, standing by the window, soft light", CH,
     [c("因為那朵雲裡面，空氣不是靜止的。還記得那些一直往上送的熱空氣嗎？")])
shot("updraft-section", "Wide cutaway illustration of a growing puffy cloud seen from the side, big curved arrows of rising air sweeping up through its middle, tiny droplets riding the arrows, a small town far below, soft bright light", (),
     [c("在一朵正在長高的積雲裡，往上衝的空氣，一秒可以走好幾公尺。")])
shot("kid-elevator", "Medium shot of a girl inside a bright glass elevator pointing upward with a big grin as it rises past the floors, soft daylight", KID,
     [k("那它根本是在搭電梯往上嘛！", "興奮")])
shot("chief-answer-one", "Medium close-up of the chief giving a satisfied nod with her arms folded, standing beside the whiteboard cube, soft daylight", CH,
     [c("沒錯。雲有重量，但它的水碎成數不完的小顆，每一顆都輕到被空氣托住。", "解開第一個謎，語氣篤定", "P:nofall")])
shot("kid-how-big", "Close-up of a girl holding her thumb and finger slightly apart in front of one eye and peering through the gap, sitting on a windowsill, soft light", KID,
     [k("那水滴要長到多大，空氣才托不住？", "章尾停住，句尾上揚", "S:howbig")])

# ---------- 第三章 ----------
CH3 = "一百萬顆，才夠一滴雨"
shot("palm-raindrop", "Close-up of a girl's open palm stretched out from under an arcade, one fat raindrop splashing on it, wet street blurred behind, soft overcast light", KID,
     [c("你淋過的雨滴，常見的大約兩公釐，直徑是雲滴的一百倍。")], chapter=CH3)
shot("kid-only-100", "Medium shot of a girl shrugging with a casual unimpressed face, leaning against an arcade pillar, rain falling behind her, soft overcast light", KID,
     [k("才一百倍？那還好嘛。", "不以為意", "S:million"), c("是直徑喔。體積是長、寬、高三個方向都要乘。")])
card("hundred-cubed", "big", {"kicker": "直徑大 100 倍", "text": "100 × 100 × 100", "sub": "體積大 100 萬倍"},
     [c("一百乘一百，再乘一百，等於一百萬。", "一字一頓")])
shot("kid-million", "Close-up of a girl with her mouth wide open and her notebook slipping from her hands, standing under the arcade, soft overcast light", KID,
     [k("一滴雨要那麼多顆？！", "大驚"), c("大概是這個數量級。", None, "P:million")])
shot("kid-pinch", "Medium shot of a girl pretending to squeeze an invisible ball between her palms with a cheeky grin, sitting on the office stool, soft light", KID,
     [k("那它們怎麼湊在一起的？有人在雲裡把它們捏起來嗎？", "開玩笑")])
shot("chief-no-pinch", "Medium close-up of the chief chuckling and shaking her head, holding a blank folder, warm lamp light", CH,
     [c("沒有人捏，是它們自己撞在一起。")])
shot("collision", "Extreme close-up illustration of one larger round water droplet falling and bumping into smaller droplets below it, the small ones merging into it, soft white cloud background", (),
     [c("雲裡的水滴大小不一樣。大一點的掉得比較快，就會追上、撞上下面比較小的。")])
shot("kid-snowball", "Medium shot of a girl in a snowy park pushing a growing snowball that is already as tall as her knees, puffing with effort, soft grey winter light", KID,
     [c("撞上去黏在一起，它就更大、掉得更快、撞到更多。"), k("像滾雪球！", "興奮")])
card("coalescence", "big", {"kicker": "第一條路", "text": "**碰撞合併**", "sub": "大水滴追撞小水滴，越滾越大"},
     [c("很像。這叫做碰撞合併。不過這只是其中一條路。")])
shot("cold-top", "Low angle wide shot of the icy, frosty top of a very tall cloud high in a pale blue sky, a single airliner passing far to the side, soft cold light", (),
     [c("雲爬到夠高的地方，溫度會降到零度以下。那裡會有小冰晶，")])
shot("supercooled", "Extreme close-up of tiny glittering ice crystals floating next to round liquid water droplets inside a cold cloud, a soft pale blue glow", (),
     [c("也有冷到零度以下、卻還沒結冰的小水滴。")])
shot("kid-not-frozen", "Close-up of a girl holding an ice cube up to her eye in disbelief, sitting at a desk, soft window light", KID,
     [k("零度以下還不結冰？", "不相信")])
shot("chief-ice-wins", "Medium close-up of the chief nodding with raised eyebrows, holding a frosty glass, soft lamp light", CH,
     [c("對，在雲裡很常見。而且在這種地方，冰晶比水滴更會搶水氣。")])
shot("snow-to-rain", "Wide illustration of a big six-armed snowflake drifting down out of a cloud and turning into a round raindrop as it falls past a warm layer toward green hills, soft light", (),
     [c("冰晶一邊長大一邊往下掉，掉到比較暖的低空，再融化成雨。")])
shot("kid-was-snow", "Medium shot of a girl under an umbrella looking up at summer rain with a curious smile, one hand stretched out to catch drops, soft overcast light", KID,
     [k("所以我淋到的雨，可能原本是雪？", "驚喜"), c("有可能。夏天長得很高的雷雨雲裡，兩條路都可能發生。")])
card("two-routes", "compare", {"title": "雨滴長大的兩條路", "left": {"heading": "碰撞合併", "points": ["大水滴追撞小水滴", "不夠冷的雲也能下"]}, "right": {"heading": "冰晶", "points": ["雲頂冷到零度以下", "長大落下，融化成雨"]}, "source": "USGS 水科學學校：降水與水循環"},
     [c("不管走哪一條，重點都一樣：水滴得先長到夠大。")])
shot("kid-whole-cloud", "Medium shot of a girl hugging a big fluffy cushion and pretending to drop it on the floor, sitting on a sofa, mischievous face, soft light", KID,
     [k("長大了，就會整朵雲一起掉下來嗎？", "很有把握的錯猜", "S:whole")])
shot("chief-still-there", "Medium close-up of the chief raising one eyebrow and pointing out of the window, soft afternoon light", CH,
     [c("你看雲在下雨的時候，雲還在天上，對吧？"), k("……對耶。", "愣住")])
shot("rain-shaft", "Wide shot of a grey rain curtain falling from under a big cloud onto distant fields, a girl in a rice-field path watching it from far away, the cloud itself still floating above, soft bright light where she stands", KID,
     [c("掉下來的，是一顆一顆已經長大的水滴。它們重到上升的空氣托不住，就從雲裡穿出來。", None, "P:howbig")])
shot("chief-batch", "Medium shot of the chief pouring water from a jug in a slow thin stream into a glass, a calm explaining face, soft lamp light", CH,
     [c("這樣的雨滴，一秒可以落下六、七公尺，比雲滴快好幾百倍。")])
shot("cloud-stays", "Wide shot of a big cloud still floating over a town while a curtain of rain pours from its base, a girl with an umbrella on a bridge watching, soft grey light", KID,
     [c("雲本身還在，只是裡面長大的那些，一批一批離開。", None, "P:whole")])
shot("kid-not-every", "Medium shot of a girl at a window pressing her forehead against the glass, looking at two clouds outside, one raining and one white, soft afternoon light", KID,
     [k("可是我家旁邊的雲，有的下雨，有的整天都不下。", "納悶"), k("為什麼不是每一朵都會下？", "章尾停住", "S:every")])

# ---------- 第四章 ----------
CH4 = "下午三點，熱空氣衝最高"
shot("chief-how-high", "Medium shot of the chief stretching her arm high above her head to tap the top of a tall bookshelf, looking up, soft daylight", CH,
     [c("這要回到一開始：雲能長多高、裡面的空氣往上衝得多用力。")], chapter=CH4)
shot("small-clouds", "Wide shot of a park lawn on a fine morning with small flat puffs of cloud dotted in the sky, a girl flying a paper plane, mild soft light", KID,
     [c("天氣好時那種小小、扁扁的白雲，長不高，水滴還來不及長大，雲就散掉了。")])
shot("cumulonimbus", "Low angle wide shot of an enormous storm cloud towering over a city skyline, its top spreading out far above, one tiny airliner flying near its upper part, soft afternoon light", (),
     [c("會下大雨的，是一路往上衝的雲。它的雲頂可以超過十公里，跟客機飛的高度差不多，甚至更高。", None, "P:every")])
shot("kid-ten-km", "Close-up of a girl tilting her head all the way back to look straight up, her hood falling off, soft afternoon light", KID,
     [k("那麼高！那要很多熱空氣才推得上去吧。", "讚嘆"), c("對。所以你猜，一天裡面，地面什麼時候最熱？")])
shot("kid-noon-guess", "Medium shot of a girl confidently pointing at a wall clock showing twelve, standing by a wall clock, big smug smile, soft light", KID,
     [k("中午十二點！", "很有把握的錯猜")])
shot("chief-later", "Medium close-up of the chief wagging one finger with a gentle smile, sitting at her desk, warm lamp light", CH,
     [c("很多人都這樣猜。太陽最高是中午，可是地面和空氣最熱，通常要再晚一點。", "溫和地否定")])
shot("pan-on-stove", "Medium shot of a girl standing on a step stool watching a frying pan on a gas stove, holding her hand above the pan to feel the heat, soft kitchen light", KID,
     [c("就像鍋子放上爐子，火一開，鍋子不會馬上最燙，要燒一段時間。")])
card("day-steps", "steps", {"title": "一天裡的一朵對流雲", "steps": [{"title": "早上", "detail": "太陽開始曬地面"}, {"title": "中午", "detail": "熱空氣一團一團往上送"}, {"title": "下午", "detail": "雲長到最高，常常開始下雨"}], "source": "中央氣象署：午後雷陣雨"},
     [c("所以熱空氣往上送得最兇的時候，常常落在下午。")])
shot("sea-breeze", "Wide shot of a coastline in the late morning, a moist breeze blowing in from the sea, a fisherman holding his cap on, low hills inland behind him, soft hazy light", (),
     [c("台灣的夏天還多了兩個幫手：從海上吹進陸地的濕空氣，")])
shot("mountain-clouds", "Wide shot of green mountain slopes with puffy clouds building up right on the ridges in the early afternoon, one hiker resting on a rock and looking up at them, mild soft light", (),
     [c("還有山。山坡把空氣往上抬，雲就特別容易在山邊長起來。")])
shot("kid-three-pm", "Medium shot of a girl on the balcony at three in the afternoon pointing at a darkening tall cloud and turning back toward the room, alarmed, soft grey light", KID,
     [k("所以下午三點，我家外面那朵雲就……變灰了！", "連起來了")])
shot("grey-base", "Low angle wide shot looking up at the thick dark-grey base of a huge cloud with bright white edges where sunlight still hits its sides, one bird flying underneath", (),
     [c("對，它長得又高又厚，陽光透不過來，底部看起來就是灰的。", None, "P:grey")])
shot("kid-why-stop", "Medium shot of a girl sitting on the windowsill with her knees up, watching rain outside slowly stop, puzzled, soft light", KID,
     [k("那為什麼雷陣雨常常下一下就停？", "追問", "S:stop")])
shot("chief-engine", "Medium close-up of the chief turning off a small desk fan with one finger and raising her eyebrows meaningfully, warm lamp light", CH,
     [c("因為大雨，會把自己的引擎關掉。", "賣關子")])
shot("rain-drags", "Wide cutaway illustration of heavy rain falling out of a storm cloud with big curved arrows of cool air pouring down alongside it and spreading out across the ground, a small farmhouse below, soft grey light", (),
     [c("雨落下來，會把周圍的空氣一起往下拖；雨在半路蒸發，又讓這團空氣更冷。")])
shot("cold-gust", "Medium shot of a girl on a street corner with her hair and jacket blown sideways by a sudden cool gust, leaves flying past, a dark cloud behind her, soft grey light", KID,
     [c("你在雷雨前感覺到的那陣涼風，常常就是它衝到了地面。")])
shot("kid-wind-knows", "Close-up of a girl closing her eyes and smiling as cool wind blows her hood, standing in front of an open window, soft grey light", KID,
     [k("那陣風我知道！一吹就要下雨了。", "得意")])
shot("chief-blocked", "Medium shot of the chief at the whiteboard drawing a downward arrow cutting off an upward arrow, looking back at the viewer, soft daylight", CH,
     [c("冷空氣往下灌，就把下面往上送的熱空氣擋掉了。沒有熱空氣補進來，這朵雲就慢慢沒力。", None, "P:stop")])
card("hour", "big", {"kicker": "一個單獨的雷雨胞", "text": "常常 **不到 1 小時**", "sub": "長大、下雨、散掉"},
     [c("還記得你問要多久嗎？一個單獨的雷雨雲，從長大、下雨到散掉，常常不到一個小時。", "數字放慢", "P:hour")])
shot("chief-caveat", "Medium close-up of the chief holding up an open palm in a gentle 'wait' gesture, a sincere face, soft daylight", CH,
     [c("不過要說清楚，不是每天下午都會這樣。")])
shot("dry-afternoon", "Wide shot of a hot clear afternoon over a beach town with not a single cloud in the sky, a girl eating a popsicle on a seawall, mild hazy light", KID,
     [c("空氣夠不夠濕、上面夠不夠冷、風怎麼吹，只要一個條件不對，雲就長不起來。")])
shot("kid-how-know", "Close-up of a girl chewing on her pencil and looking at a sky full of clouds through the window, thoughtful, soft afternoon light", KID,
     [k("那我要怎麼知道，今天的雲會不會下雨？", "章尾停住", "S:know")])

# ---------- 第五章 ----------
CH5 = "頭頂平掉了，涼風來了"
shot("kid-top-bubbling", "Low angle medium shot of a girl on the balcony leaning over the railing and pointing at a towering cloud whose top is still bulging upward in round lumps, soft afternoon light", KID,
     [k("所長！它的頭頂還在一直往上冒！", "實況轉播")], chapter=CH5)
shot("chief-phone-call", "Medium close-up of the chief holding a phone to her ear by the window and smiling, a blank weather map on the wall behind her, soft daylight", CH,
     [c("還記得花椰菜嗎？那就是裡面的空氣還在往上衝。預報是氣象署的事，可是你現在自己就看得到。")])
shot("sign-anvil", "Wide shot of a huge storm cloud whose flat top spreads out sideways like an anvil far above apartment rooftops, one balcony with laundry in the foreground, soft afternoon light", (),
     [k("現在頭頂變平了，往旁邊攤開！", "驚訝")])
shot("chief-anvil", "Medium close-up of the chief raising her hand flat above her head as if touching a ceiling, a knowing look, soft lamp light", CH,
     [c("像一個鐵砧。它已經長到撞上一層很難再往上的高度。")])
shot("sign-gust", "Medium shot of a girl on the balcony with laundry flapping wildly beside her in a sudden cool wind, her hands grabbing a towel, soft grey light", KID,
     [k("啊，突然好涼！衣服都飛起來了！", "叫出來")])
shot("chief-told-you", "Medium close-up of the chief chuckling and pointing at the phone in her hand, warm lamp light", CH,
     [c("還記得那陣涼風嗎？冷空氣已經跑在雨的前面了。我一開始說什麼？", "得意", "P:know")])
shot("kid-laundry-run", "Medium shot of a girl running back inside from the balcony with a laundry basket piled high in her arms, the first raindrops hitting the railing behind her, soft grey light", KID,
     [k("收衣服！", "笑，加快")])
shot("palm-big-drop", "Close-up of a girl's open palm reaching out from under the balcony roof, a fat raindrop splashing on it, soft grey light", KID,
     [k("好大顆！雨滴是不是像眼淚那樣，尖尖的？", "隨口一問", "S:shape")])
shot("chief-not-tear", "Medium close-up of the chief holding up a drawing of a teardrop on a blank card and shaking her head with a smile, soft lamp light", CH,
     [c("大家都這樣畫，可是不是。還記得空氣會擋住往下掉的東西嗎？雨滴掉得越快，空氣擋得越用力。")])
card("drop-shapes", "steps", {"title": "雨滴真正的樣子", "steps": [{"title": "小雨滴", "detail": "幾乎是圓的"}, {"title": "大一點", "detail": "底部被空氣壓扁，像漢堡麵包"}, {"title": "再更大", "detail": "被空氣扯開，碎成好幾顆"}], "source": "USGS 水科學學校；NASA GPM"},
     [c("小的幾乎是圓的。大一點的，落下時底部被空氣壓扁，像漢堡麵包。", None, "P:shape"), c("再大，就被扯開，碎成好幾顆。所以雨滴不會一直長下去。")])
shot("kid-burger", "Close-up of a girl holding a hamburger bun up next to her face and grinning, sitting at a small kitchen table, soft daylight", KID,
     [k("所以打在我手上的，是一顆漢堡麵包！", "大笑")])

# ---------- 收尾 ----------
CH6 = "雨停了，衣服收好了"
shot("rain-stops", "Wide shot of the apartment balcony after rain, wet railing glistening, the big cloud thinning and breaking up in the sky, a girl stepping back outside with her notebook, soft clearing light", KID,
     [k("衣服都收進來了，雨也停了。真的不到一個小時。", "有點不敢相信")], chapter=CH6)
shot("chief-stamp", "Medium close-up of the chief lifting a small red rubber stamp over a blank folder on her desk with a satisfied smile, warm lamp light", CH,
     [c("就像剛剛說的，引擎關掉，雲就散了。打在你手上的每一顆，都是那一百萬顆湊起來的。")])
shot("kid-notebook-done", "Close-up of a girl closing her notebook with both hands and beaming, standing on the wet balcony, soft clearing light", KID,
     [k("還記得那些被托住的小水滴嗎？原來它們不是不會掉，是一直在等長大。", "自己想通")])
card("outro", "outro", {"title": "原來如此！", "cta": "訂閱原來如此事務所", "lines": ["雲有水，但碎成數不完的小水滴"]},
     [k("原來如此！", "開心大聲"), c("你家那邊的午後雷陣雨，通常幾點開始？留言告訴我們。", "問句上揚，像聊天"), c("想一起把生活裡的為什麼找到底，就訂閱原來如此事務所。", "誠懇")])

# ---------- 2026-11-03 rewrites after the first keyframe run (judge failed all three takes) ----------
FIX = {
 "chief-yes": ("Waist-up portrait of the chief nodding warmly and holding up a magnifying glass, bookshelves of blank folders behind her, soft afternoon light", CH),
 "clear-morning": ("Wide shot of an apartment balcony on a clear blue morning, a girl standing on tiptoe pinning a striped towel onto a laundry line, her notebook tucked in her jacket pocket, an empty blue sky, soft early light", KID),
 "chief-kettle": ("Waist-up shot of the chief in a small kitchenette pointing one finger at a steaming kettle on the stove beside her, a mug next to the kettle, soft lamp light", CH),
 "mist-puff": ("Medium close-up of the chief bending down to look closely at a kettle spout, a white curl of mist floating a hand's width away from the spout and clear air right at the opening, soft kitchen light", CH),
 "chief-expands": ("Waist-up shot of the chief at her desk pulling one red balloon wide between her two hands so it stretches, an amused face, warm lamp light", CH),
 "chief-second": ("Waist-up shot of the chief holding up two fingers with a kind serious face, a whiteboard behind her, soft daylight", CH),
 "kid-no-weight": ("Close-up of the girl pinching one long strand of her own black hair between her fingers and staring at it cross-eyed, her notebook put away, soft window light", KID),
 "chief-falls-slowly": ("Head-and-shoulders close-up of the chief shaking her head gently and pinching her thumb and forefinger almost together in front of her face, warm lamp light", CH),
 "droplet-vanish": ("Close-up of the girl blowing gently on one tiny water droplet resting on her fingertip, the droplet shrinking into a faint wisp, soft bright light", KID),
 "palm-raindrop": ("Medium shot of the girl standing under a shop arcade with one open palm stretched out into the rain, a fat raindrop splashing on her palm, her notebook tucked under her other arm, soft overcast light", KID),
 "kid-only-100": ("Medium shot of the girl shrugging with both palms turned up and an unimpressed face, leaning on an arcade pillar, her notebook in her jacket pocket, rain falling in the street behind her, soft overcast light", KID),
 "kid-pinch": ("Medium shot of the girl sitting on a tall stool pressing her two empty palms together as if squeezing an invisible ball, a cheeky grin, her notebook lying on the stool beside her, soft light", KID),
 "collision": ("Close-up of the girl looking through a big magnifying glass at water droplets on a window pane, one large droplet sliding down and swallowing the smaller ones below it, soft grey light", KID),
 "kid-snowball": ("Wide shot of the girl in a snowy park leaning her whole body against a knee-high snowball and pushing it forward with both hands, puffing with effort, her notebook in her pocket, soft grey winter light", KID),
 "supercooled": ("Close-up of the chief looking through a big magnifying glass at tiny glittering ice crystals and round water droplets floating together in a cold mist, a soft pale blue glow", CH),
 "kid-not-frozen": ("Close-up of the girl holding an ice cube between two fingers right in front of one eye and squinting at it in disbelief, her notebook lying on the desk, soft window light", KID),
 "chief-ice-wins": ("Head-and-shoulders close-up of the chief raising her eyebrows and nodding, holding a frosty glass up beside her face, soft lamp light", CH),
 "snow-to-rain": ("Wide shot of the girl on a hillside looking up as one big six-armed snowflake drifts down from a cloud high above, and lower down a round raindrop falls toward her, soft light", KID),
 "kid-not-every": ("Medium shot of the girl with her forehead and both hands pressed against a window pane, looking out at two clouds, one with rain under it and one plain white, her notebook on the sill, soft afternoon light", KID),
 "small-clouds": ("Wide shot of a park lawn on a fine morning with small flat puffs of cloud dotted across the sky, the girl throwing a folded paper plane into the air with one arm, her notebook on the grass, mild soft light", KID),
 "cumulonimbus": ("Low angle wide shot of an enormous storm cloud towering over a city skyline, its top spreading out far above, one tiny airliner near the very top of the cloud, a girl on a rooftop in the foreground tipping her head back to look up at it, soft afternoon light", KID),
 "chief-engine": ("Waist-up shot of the chief pressing the switch of a small desk fan with one finger and raising her eyebrows meaningfully, warm lamp light", CH),
 "kid-how-know": ("Head-and-shoulders close-up of the girl biting the end of a pencil and gazing at a cloudy sky through a window, thoughtful, soft afternoon light", KID),
}
for sc in S:
    if sc["id"] in FIX:
        sc["data"]["prompt"], chars = FIX[sc["id"]]
        sc["data"]["characters"] = list(chars)
assert all(any(sc["id"] == k for sc in S) for k in FIX)

# second rewrite round (2026-11-03): plainer backgrounds, tighter framing, the notebook put away
FIX2 = {
 "chief-yes": ("Waist-up shot of the chief smiling and nodding with one open palm raised beside her face, a plain cream wall behind her, soft afternoon light", CH),
 "clear-morning": ("Medium shot of the girl on a balcony reaching up with both empty hands to hang a striped towel on a laundry line, her notebook in her jacket pocket, a clear sky behind her, soft morning light", KID),
 "chief-expands": ("Waist-up shot of the chief holding one round red balloon in both hands in front of her chest and squeezing it so it bulges, an amused face, a plain wall behind her, warm lamp light", CH),
 "chief-falls-slowly": ("Head-and-shoulders close-up of the chief holding her thumb and forefinger almost touching in front of one eye, a gentle smile, a plain wall behind her, warm lamp light", CH),
 "droplet-vanish": ("Medium shot of the girl on a rooftop watching a tiny water droplet in the air in front of her fade into a faint wisp, her hands in her jacket pockets, a pale bright sky", KID),
 "palm-raindrop": ("Waist-up shot of the girl holding one open hand out in front of her with a big raindrop splashing right on her palm, her other hand in her pocket, rain falling behind her, soft overcast light", KID),
 "kid-not-every": ("Medium shot of the girl leaning on a windowsill with both empty hands flat against the glass, looking out at one rain cloud and one plain white cloud, soft afternoon light", KID),
 "cumulonimbus": ("Low angle wide shot of the girl on a rooftop with her hands in her pockets tipping her head far back to look up at an enormous storm cloud towering over the city, a tiny airliner near the very top of the cloud, soft afternoon light", KID),
 "chief-engine": ("Waist-up shot of the chief pressing the button of a small desk fan with one finger, eyebrows raised, a plain wall behind her, warm lamp light", CH),
 "kid-laundry-run": ("Medium shot of the girl hurrying indoors through a balcony door carrying a laundry basket full of towels in both arms, her notebook in her pocket, soft grey light", KID),
 "chief-stamp": ("Waist-up shot of the chief holding up a small red rubber stamp in one hand with a satisfied smile, a closed plain folder on the desk in front of her, warm lamp light", CH),
}
FIX.update(FIX2)
for sc in S:
    if sc["id"] in FIX2:
        sc["data"]["prompt"], chars = FIX2[sc["id"]]
        sc["data"]["characters"] = list(chars)

# ---------- assemble ----------
scenes = []; loops_s = {}; loops_p = {}; n = 0
for sc in S:
    lines = []
    for sp, text, emo, tag in sc["lines"]:
        n += 1; lid = f"p{n:03d}"
        line = {"id": lid, "speaker": sp, "text": text}
        if emo: line["emotion"] = emo
        lines.append(line)
        if tag:
            kind, key = tag.split(":")
            (loops_s if kind == "S" else loops_p)[key] = lid
    out = {"id": sc["id"]}
    if sc["chapter"]: out["chapter"] = sc["chapter"]
    out["template"] = sc["template"]
    d = dict(sc["data"])
    if sc["template"] == "shot" and not d["characters"]: d.pop("characters")
    out["data"] = d; out["lines"] = lines
    scenes.append(out)
WHAT = {"elephant": "那朵雲有幾頭大象重", "nofall": "水比空氣重，雲為什麼沒有整團掉下來", "hour": "怎麼在一個小時以內變成大雨", "grey": "雲的底部為什麼變灰", "vapour": "雲是不是水蒸氣",
        "nuclei": "天上有什麼讓水氣凝結上去", "weight": "一朵雲總共有多少水", "howbig": "水滴要多大，空氣才托不住", "million": "一滴雨要多少雲滴",
        "whole": "是不是整朵雲一起掉下來", "every": "為什麼不是每一朵雲都下雨", "stop": "雷陣雨為什麼下一下就停", "know": "怎麼看出今天的雲會不會下雨", "shape": "雨滴是不是眼淚的形狀"}
assert set(loops_s) == set(loops_p) == set(WHAT), (set(loops_s) ^ set(loops_p))
loops = [{"setup": loops_s[key], "payoff": loops_p[key], "what": WHAT[key]} for key in WHAT]
chars = sum(len(l["text"]) for s in scenes for l in s["lines"])
kidchars = sum(len(l["text"]) for s in scenes for l in s["lines"] if l["speaker"] == "kid")
shots = sum(1 for s in scenes if s["template"] == "shot")
print(f"scenes {len(scenes)} shots {shots} cards {len(scenes)-shots} lines {n} chars {chars} kid {kidchars/chars:.0%} est {chars/4.5/60:.1f} min", file=sys.stderr)
for s in scenes:
    t = sum(len(l["text"]) for l in s["lines"])
    if t > 50: print("long scene", s["id"], t, file=sys.stderr)
json.dump({"scenes": scenes, "loops": loops}, open(sys.argv[1], "w"), ensure_ascii=False, indent=2)
