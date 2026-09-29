export default {
  "series": {
    "slug": "scapegoat-empress",
    "title": "朕不是你們的替死鬼",
    "premise": "群臣把一名庫房女吏扶上皇位，準備在登基第三十天讓她替饑荒與虧空陪葬。她登基後做的第一件事，是撤掉自己的御膳，先喝一口災民正在吃的粥，再把同一碗推到首輔面前。",
    "genre": "empress-rise",
    "lead": "female",
    "tone": "no-romance",
    "note": "原創架空權謀；葉穗的本事限定為糧務、帳務與現場調度。三十日危機後以數月的協商與救災成果取得正式擁立。四篇四十集閉合，不以戀愛或秘密皇族血統補救合法性。"
  },
  "setting": {
    "world": {
      "place": "架空臨朝，京城衡京及五處供糧州的商路。衡京在大河北岸：南面三州的糧走南岸大道，大車要過城南窄橋上的南糧關才能進城，小車另可繞渡口小道；北面兩州的糧先收進城北郊蕭家宗族掌握的北倉，再由北門大道入城。東公倉在城外東南的河岸，出倉的大車也要過南糧關；唐家車棧在南糧關橋外的南岸；南市施粥場在南城門內；北偏院在城北。主要畫面集中在衡京。",
      "period": "無對應真實朝代的前工業王朝；紙本帳冊、秤砣、木牘與驛傳，無魔法、重生或現代裝置。",
      "conflict_engine": "洪災與歉收使衡京糧價失控。首輔裴定衡控制內廷發文、關卡與大糧戶，以軍餉和人質綁住禁軍。他把庫房女吏葉穗偽造為先帝長姊失散之女（帝系長房），安排她追認歷年挪糧，再於登基第三十日的祭天上以失政罪處死，將責任留在一個沒有宗族支持的人身上。真正的旁支皇族蕭承越手握北倉糧契，等清除舊帳後入京接位。葉穗只能用逐批送到的糧食、可共同驗證的帳目與有期限的合作，擴大原本僅有印璽的命令效力。",
      "factions": [
        {
          "name": "內廷與首輔府",
          "want": "保住官位、欠餉挪款與侵吞鏈，將皇權維持成簽字工具。",
          "secret": "祭天罪詔與繼位草約同時起草，葉穗只是過渡的責任承受者。"
        },
        {
          "name": "禁軍與值守家戶",
          "want": "糧餉實際到手、家人安全、城內不亂。",
          "secret": "統領妹妹遭首輔以療養名義拘禁；軍糧帳同時被當成封口工具。"
        },
        {
          "name": "大糧戶與北倉皇族",
          "want": "以斷糧換取低價地契、長期免稅與登位支持。",
          "secret": "蕭承越出示的糧食援助附有排他關卡與優先償款條件。"
        },
        {
          "name": "小商戶、糧吏與街坊",
          "want": "能活下去的糧價、通路、欠款與可申訴的徵稅。",
          "secret": "各家私留的收條可拼出重複徵糧，但個別出頭都會遭報復。"
        }
      ],
      "visual_language": "宮殿冷墨綠與暗金，糧倉麻布與木屑暖褐，災民區灰藍轉向收成的土金色。龍紋只是布料紋理，不作發光權力象徵；印璽、秤砣、簽名每次都能辨認持有人。",
      "narrator": {
        "provider": "gemini",
        "name": "Sulafat",
        "style": "擬定 casting，尚未試聽；臺灣國語、成熟溫暖女聲。只交代路程與日期，不替葉穗解釋尚未取得的證據。"
      }
    },
    "rules": [
      "臨朝繼承舊制允許帝系女性後裔承位；葉穗以偽造的「先帝長姊失散之女」（帝系長房）身分被扶立，不是突然打破性別制度。她不知道身分造假，只相信養母所說的收養經過，直到第 19 集（第 14 日）才從養母口中聽到實情。",
      "首輔需要葉穗在祭天前追認舊年糧務，才能把群臣的多次違法行為包進新君承責的罪詔；這不能真的消滅商戶債權，只能藉軍政控制阻止追查。觀眾先看見處死日期，葉穗第十集才查到自己名字。",
      "御印可以啟動宮中既有糧額，不能憑空變出糧食。跨門發文要內廷副印與送達回執；葉穗逐步建立副本、公開送達、受令者回執，不能第一集就控制所有官署。",
      "葉穗會看糧色、含水、秤差、單據與車程，不會憑眼神辨忠奸。軍事行動由韓鐸決定，醫療由羅杏負責，商路信用由唐敏承擔，每次合作都有資源、風險或限制。",
      "雙重徵收一律以糧計：南糧關左右兩張徵稅桌對同一車各抽一次糧，一張收條記成稅，另一張改寫成借糧。追回的是糧，只能折給軍戶當欠餉口糧或送進粥場；商戶的貨款與車工是錢，只能用宮宴裁減省下的銀錢與宮中非印信器物的抵押支付。動用儀典糧會縮減宮宴；拆車隊要讓商戶多付車工；先發欠餉要延後另一筆款，必須在人物對話中說明。",
      "賈勳是南糧關主事，兼管東公倉出倉的驗收簽押。他經手的印要分清：南糧關左右兩張徵稅桌各有一枚關卡副印（左桌記稅、右桌記借糧，同一車蓋兩次就是雙重徵收，第 17 集藥單上蓋的是右桌那枚）；另有首輔交給他的一枚內廷副印，用來代簽公文送達回執，第 5、9 集的「副印不全」、第 8 集的簽收與 m03 的共用副印都指這一枚。他調不動禁軍，也沒有審案權：第 25 集他是以查獲關卡的主事身分具狀控告葉峻，問事由府獄官吏主持。",
      "韓鐸先保住士兵家屬再擴大合作；唐敏要求公開收條和限定貨款清償期限；街坊沈巧要求能發問與抄錄，不把救命糧等同效忠票。",
      "蕭承越的皇族血統是真的，最初受到部分官員與百姓支持，是因北倉糧契與成熟的接位方案。他不因一次辯論就失去支持，須等秘密苛約公開、替代商路運轉才失去壟斷。",
      "葉穗承認假身世後只能由臨時議約續任救災主持；第 38 集開始由供糧州、街坊代表和官署協商權限，數月後第 40 集才正式擁立。不可把一城歡呼剪成全國一致。",
      "侵吞款追還需要核帳；罪責須分別認定。解除首輔兵權不等於當場處決，蕭承越也須退還非法所得，反派間決裂不能洗去已做過的事。",
      "洪災死者不復活，失收田地不會立即豐產。結局第一批新糧只代表供應開始恢復；公開糧政、命令留檔與定期問責仍會限制葉穗。"
    ],
    "characters": [
      {
        "id": "ye-sui",
        "name": "葉穗",
        "role": "女主；庫房女吏、被扶立的假皇族、後獲擁立的女帝",
        "age": 24,
        "appearance": "A 24-year-old East Asian woman with an oval face, focused dark eyes and straight black hair secured in one compact high knot. A narrow bronze hairpin shaped like a rice leaf never changes. She wears a plain deep teal court robe with restrained antique-gold edging, practical dark boots and a short brown counting cord at her waist. Slim, upright silhouette; no heavy makeup or ornamental weapon.",
        "personality": "細心、耐餓，遇到不懂的事會問，但容易把自己也當成可消耗的糧袋。",
        "want": "讓糧食真正到人手裡，活過被安排的三十天。",
        "fear": "自己一紙命令讓別人替她送命。",
        "secret": "曾為救急挪過一天的庫房粟額，已用自己薪錢補足；懂得帳上合法未必代表現場有人活著。",
        "speech": "先問「到了沒有？」；遇到權謀會要求把代價講清楚。",
        "voice": {
          "provider": "gemini",
          "name": "Kore",
          "style": "臺灣國語；年輕女聲、低而清楚，憤怒時降低音量，未試聽。"
        },
        "relationships": [
          {
            "with": "pei-dingheng",
            "kind": "由被挑中的簽字者成為公開核帳的對手。"
          },
          {
            "with": "han-duo",
            "kind": "以交付與承責換取合作，不發展戀愛。"
          },
          {
            "with": "luo-xing",
            "kind": "養母與女兒；身世隱瞞傷害信任，羅杏第 30 集當眾以本名作證修復。"
          },
          {
            "with": "ye-jun",
            "kind": "弟弟自行救災，女主必須公正區分他的善意與犯法手段。"
          }
        ]
      },
      {
        "id": "pei-dingheng",
        "name": "裴定衡",
        "role": "首輔；主要反派",
        "age": 56,
        "appearance": "An East Asian man of 56 with a long angular face, silver at both temples and a neatly trimmed short black-grey beard. He wears a rigid black court cap and layered charcoal robes with a thin burgundy inner collar. An opaque black-stone thumb ring and an ivory tally case are his fixed identifiers. He stands still with hands folded, occupying little motion but much space.",
        "personality": "相信秩序高於人命，會給人可承受的小恩換取無法退出的大債。",
        "want": "將侵吞鏈改寫成新君失德，保住自己掌控的體系。",
        "fear": "底層各自留存的小帳能被放到同一張桌上。",
        "secret": "假血統證明、祭天罪詔與蕭承越繼位草約都出自他的書房。",
        "speech": "常說「為全局計」；越失控越要求遵循格式。",
        "voice": {
          "provider": "gemini",
          "name": "Charon",
          "style": "臺灣國語；成熟低男聲，字間留白，少吼叫，未試聽。"
        },
        "relationships": [
          {
            "with": "ye-sui",
            "kind": "挑中無宗族女吏，以為她只會數糧。"
          },
          {
            "with": "xiao-chengyue",
            "kind": "互相需要又保留能毀掉對方的副本。"
          },
          {
            "with": "jia-xun",
            "kind": "把關卡收益分給賈勳，保留隨時棄子的權力。"
          }
        ]
      },
      {
        "id": "han-duo",
        "name": "韓鐸",
        "role": "禁軍統領；軍事盟友",
        "age": 34,
        "appearance": "An East Asian man of 34 with a broad square face, weathered cheeks and short black hair tied into a small soldier knot. Matte iron lamellar armour over a dark navy tunic, a faded ochre wrist wrap and one old shallow scar across the left eyebrow are constant. A practical sheathed single-edged sabre stays at his left hip. Powerful grounded silhouette; his armour is field-worn, never polished.",
        "personality": "謹慎、重承諾，不把士兵當君主爭權的耗材。",
        "want": "保家人與城中秩序，讓值守士兵吃飽。",
        "fear": "一次選邊害死被扣的妹妹。",
        "secret": "妹妹韓芮在首輔控制的偏院，軍餉借據被用作兄妹叛逃的預製證據。",
        "speech": "「給我可走的路。」先說兵力與風險，再說立場。",
        "voice": {
          "provider": "gemini",
          "name": "Orus",
          "style": "臺灣國語；中低男聲，短句沉穩、救援時加快而不咆哮，未試聽。"
        },
        "relationships": [
          {
            "with": "han-rui",
            "kind": "兄妹；保護不等於替她作所有決定。"
          },
          {
            "with": "ye-sui",
            "kind": "從限量護糧到以公開議約支持，始終可以提出異議。"
          }
        ]
      },
      {
        "id": "luo-xing",
        "name": "羅杏",
        "role": "葉穗養母、葉峻生母、醫者、身世證人",
        "age": 52,
        "appearance": "An East Asian woman of 52 with a round lined face and dark hair streaked with grey, coiled low at the nape. She wears a faded plum cross-collar jacket, a slate skirt and a brown cloth medical satchel with a patched corner. Her hands have small old work marks. No jewellery except a plain wooden bead tied to the satchel strap.",
        "personality": "能照顧很多人，卻因害怕失去女兒而遲疑說真話。",
        "want": "讓葉穗活著，也讓自己的隱瞞不再傷人。",
        "fear": "女兒以為她把自己賣給首輔。",
        "secret": "首輔以葉峻舊年運糧罪逼她按印承認假族譜；她保留了真實收養紀錄。",
        "speech": "談政治時也會先問「手怎麼這麼冷」。",
        "voice": {
          "provider": "gemini",
          "name": "Vindemiatrix",
          "style": "臺灣國語；帶些沙質的成熟女聲，溫和、短促口語，未試聽。"
        },
        "relationships": [
          {
            "with": "ye-sui",
            "kind": "養育之情真實，皇族說法是脅迫下的謊。"
          },
          {
            "with": "ye-jun",
            "kind": "母子；擔心他的衝動，仍尊重他照顧街坊的選擇。"
          }
        ]
      },
      {
        "id": "ye-jun",
        "name": "葉峻",
        "role": "女主弟弟、民間運糧者",
        "age": 21,
        "appearance": "A 21-year-old East Asian man with a lean sun-darkened face and untidy short black hair tied with a rust-red cloth band. He wears a patched sand-coloured work jacket, dark trousers and rope-soled boots. His right sleeve has one distinctive pale rectangular repair.",
        "personality": "肯做髒活、討厭等公文，會把善意當成越界的理由。",
        "want": "把眼前的糧送到眼前的人。",
        "fear": "因姐姐穿上龍袍，自己只能沉默看人挨餓。",
        "secret": "為繞卡曾拿亡父留下的一枚過期運糧牌來用，救人是真的，冒用也是真的。",
        "speech": "「車還在，人就能走。」不擅長長篇辯解。",
        "voice": {
          "provider": "gemini",
          "name": "Puck",
          "style": "臺灣國語；明亮青年男聲，急但不油滑，未試聽。"
        },
        "relationships": [
          {
            "with": "ye-sui",
            "kind": "姐姐不能免掉他的程序責任，但可以保護他不被栽成劫糧者。"
          },
          {
            "with": "tang-min",
            "kind": "替商戶跑車，先交貨後談信用。"
          }
        ]
      },
      {
        "id": "he-jing",
        "name": "何靜",
        "role": "留守糧吏、帳目盟友",
        "age": 36,
        "appearance": "An East Asian woman of 36 with a narrow face, tired dark eyes and black hair in a tightly braided low bun. She wears an ink-blue clerk coat with pale cuffs, a small brass abacus pendant and a leather document tube across her back. Ink stains sit on the same two right fingertips; her left cuff has a neatly mended seam.",
        "personality": "極度慎重，受過上級逼迫改帳，仍留著可查的痕跡。",
        "want": "讓自己和其他糧吏有說真話的安全。",
        "fear": "新君只找一個小吏認罪。",
        "secret": "舊年被迫抄假入倉數，私留每批秤號。",
        "speech": "「這一欄能對，下一欄還不能。」不讓推測冒充結論。",
        "voice": {
          "provider": "gemini",
          "name": "Aoede",
          "style": "臺灣國語；清晰中音女聲，數字與停頓分明，未試聽。"
        },
        "relationships": [
          {
            "with": "ye-sui",
            "kind": "由怕被當替罪羊到敢當面指出女主的算錯。"
          },
          {
            "with": "shen-qiao",
            "kind": "官方紀錄與街坊收條互相核驗。"
          }
        ]
      },
      {
        "id": "tang-min",
        "name": "唐敏",
        "role": "小糧商代表、商路盟友",
        "age": 45,
        "appearance": "An East Asian woman of 45 with a strong jaw, warm brown skin and black hair bound high in a practical spiral bun. She wears a muted aubergine merchant coat over a brown apron and a broad cloth belt carrying an iron key ring. One round copper button on her left shoulder and a chipped measuring scoop identify her. Solid practical build.",
        "personality": "敢談價、不扮慈善家；珍惜夥計，討厭皇命免付帳。",
        "want": "讓糧車能通行、貨款能收回、夥計不被當成軍夫。",
        "fear": "為新君出頭後，同行與家人被大糧戶報復。",
        "secret": "手裡有北倉對小商戶的排他供貨草約，原打算簽下求生。",
        "speech": "「這筆誰出？」接著講出能接受的條件。",
        "voice": {
          "provider": "gemini",
          "name": "Pulcherrima",
          "style": "臺灣國語；較低、較厚的中年女聲，談價直接不拖泥帶水，未試聽。"
        },
        "relationships": [
          {
            "with": "ye-sui",
            "kind": "有期限、有回執的信用盟約，不靠一次感動免費供糧。"
          },
          {
            "with": "ye-jun",
            "kind": "欣賞他的送貨能力，也要求他承認冒用牌照的風險。"
          }
        ]
      },
      {
        "id": "jia-xun",
        "name": "賈勳",
        "role": "南糧關主事、兼東公倉出倉驗收；首輔執行者",
        "age": 41,
        "appearance": "An East Asian man of 41 with a thick neck, a neat pointed moustache and slick black hair under a short official cap. He wears a dark rust-brown uniform with a rectangular black chest patch and a heavy brass gate-key bundle on his right belt. One pale nick through the moustache identifies his close-ups. Stocky forward-leaning posture.",
        "personality": "對上奉承、對下嚴苛，只認能保住自己的人。",
        "want": "保住關稅抽成與官職。",
        "fear": "首輔把所有糧稅都推到他身上。",
        "secret": "同一車糧在南糧關左右兩張徵稅桌，用兩枚不同的關卡副印抽兩次糧，留暗帳用來防被棄。",
        "speech": "「沒有副印，過不得。」",
        "voice": {
          "provider": "gemini",
          "name": "Fenrir",
          "style": "臺灣國語；粗中音男聲，官腔刻意、語速偏快，未試聽。"
        },
        "relationships": [
          {
            "with": "pei-dingheng",
            "kind": "依賴首輔，也私存可保命的關卡底冊。"
          },
          {
            "with": "han-duo",
            "kind": "用家屬和欠餉牽制軍人。"
          }
        ]
      },
      {
        "id": "xiao-chengyue",
        "name": "蕭承越",
        "role": "真正皇族繼承候選、北倉糧契持有人",
        "age": 32,
        "appearance": "An East Asian man of 32 with a refined long face and carefully combed black hair in a tall formal knot. He wears ivory robes under a pale steel-blue cloak, a narrow jade belt and a signet ring carved with a three-leaf crest. Clean-shaven, composed shoulders and expensive but travel-worn boots distinguish him from palace courtiers.",
        "personality": "善於把資源交換說成天下大義，願意維持秩序但要求別人先付代價。",
        "want": "以最低風險接位，保住北倉和宗族利益。",
        "fear": "血統還在，卻已沒人必須依賴他的糧。",
        "secret": "簽過葉穗祭天後接位的草約，同意用她的罪詔抹去北倉重複債權的追查。",
        "speech": "「我能讓糧明日就到。」每句承諾後面都有條件。",
        "voice": {
          "provider": "gemini",
          "name": "Algieba",
          "style": "臺灣國語；平穩清亮男聲，禮貌的壓力勝於嘶喊，未試聽。"
        },
        "relationships": [
          {
            "with": "pei-dingheng",
            "kind": "盟約共犯，並非首輔單向操縱的傀儡。"
          },
          {
            "with": "ye-sui",
            "kind": "以婚姻與處死葉峻作交易，女主拒絕；最後退位索求也受核帳約束。"
          }
        ]
      },
      {
        "id": "han-rui",
        "name": "韓芮",
        "role": "韓鐸妹妹、被扣押的證人",
        "age": 20,
        "appearance": "A 20-year-old East Asian woman with a heart-shaped face and straight dark hair in two simple low braids. She wears a pale grey-blue short jacket, a navy skirt and a small embroidered yellow pouch at her waist. A faint pale restraint mark circles her right wrist. No court ornaments.",
        "personality": "敏銳、有耐心，懂得先保住能帶出去的訊息。",
        "want": "自己走出偏院，讓哥哥不再因她服從。",
        "fear": "救她的人為了趕時間害死院內其他病人。",
        "secret": "記下每次移送藥單上的關卡副印，能連結拘禁與軍糧公文。",
        "speech": "「我記了，不用你猜。」",
        "voice": {
          "provider": "gemini",
          "name": "Leda",
          "style": "臺灣國語；較輕柔的青年女聲，句尾堅定，未試聽。"
        },
        "relationships": [
          {
            "with": "han-duo",
            "kind": "脫困後要求以證人身分留下，不再被私下藏起。"
          },
          {
            "with": "luo-xing",
            "kind": "在換診名義下合作撤離其他病人。"
          }
        ]
      },
      {
        "id": "shen-qiao",
        "name": "沈巧",
        "role": "街坊長者、災戶代表及議約見證人",
        "age": 61,
        "appearance": "An East Asian woman of 61 with a broad lined face, silver hair wound into a small low knot and steady dark eyes. She wears a charcoal cotton jacket, faded olive skirt and a cream scarf with a single indigo stripe. A flat bamboo receipt box held against her chest is her recurring identifier. Sturdy stance and deliberate hand movement.",
        "personality": "不接受用恩情堵住提問，會照顧人也會算共同的帳。",
        "want": "每一戶的糧與申訴都有名字，不再只有一個總數。",
        "fear": "百姓被用完之後，又被要求安靜。",
        "secret": "替鄰里保存徵糧收條，明知會被搜仍藏在醫棚下。",
        "speech": "「我謝你，也要問你。」",
        "voice": {
          "provider": "gemini",
          "name": "Gacrux",
          "style": "臺灣國語；低沉年長女聲，氣息稍慢、語意清楚，未試聽。"
        },
        "relationships": [
          {
            "with": "ye-sui",
            "kind": "由受助者成為有權質問她的人，正式擁立時仍提出限制。"
          },
          {
            "with": "he-jing",
            "kind": "以民間收條校正官帳，互不盲信。"
          }
        ]
      }
    ],
    "locations": [
      {
        "id": "hall",
        "name": "承光殿",
        "description": "宮宴、朝議共用的大殿；正中御桌與側面發文案保持方位，冷綠暗金，後期增加公開抄件桌。"
      },
      {
        "id": "granary",
        "name": "東公倉",
        "description": "城外東南河岸的救急官倉，靠水運進糧，出倉的大車要過南糧關窄橋才能進城；三道木門、固定秤臺與缺角石階；有限庫存以麻袋堆高度具體呈現。"
      },
      {
        "id": "relief",
        "name": "南市施粥場",
        "description": "南城門內的空地；灰棚、兩排灶、木牌登記區；醫棚在同一場地深處，群眾無臺詞背景。"
      },
      {
        "id": "gate",
        "name": "南糧關",
        "description": "城南大河窄橋前的雙欄關卡，南岸進城的大車都要過這裡；左右各一張徵稅桌，同一車各抽一次糧，可直接看懂雙重徵收。"
      },
      {
        "id": "records",
        "name": "內廷文簿房",
        "description": "印盒、送達木牘、三層紙架與一道上鎖小門；不製造無限密室。"
      },
      {
        "id": "clinic",
        "name": "羅杏醫舍",
        "description": "簡單兩間屋與藥桌，收養紀錄藏在常用藥書夾層；家人對話的暖色空間。"
      },
      {
        "id": "depot",
        "name": "唐家車棧",
        "description": "在南糧關橋外的南岸；商路合作、車隊整備與小商戶議事的共用場景，牆上標記實際車數。"
      },
      {
        "id": "annex",
        "name": "北偏院",
        "description": "名為療養的拘禁院落；唯一車門與診療廊道相連，救援不展示複雜攻城。"
      },
      {
        "id": "prison",
        "name": "府獄問事房",
        "description": "木欄與一張訊問桌，葉峻及證人以此處理罪責，避免血腥刑罰。"
      },
      {
        "id": "altar",
        "name": "城前祭天廣場",
        "description": "石階祭臺正對百姓空地，最後改放兩張並排核帳桌；同一印璽在陽光下看得清。"
      },
      {
        "id": "field",
        "name": "近郊回耕田",
        "description": "收成時間跳躍後才出現的稻田與新糧車，不以一大片金田暗示全國已富足。"
      }
    ],
    "mysteries": [
      {
        "id": "m01",
        "question": "祭天日期旁被遮住的名字是誰，首輔為何需要她簽字？",
        "answer": "葉穗將被要求追認挪糧，再以新君失政代罪處死；首輔需要她承責而不需要她治理。",
        "planted": 1,
        "advanced": [
          3,
          7
        ],
        "revealed": 10,
        "reserved": false
      },
      {
        "id": "m02",
        "question": "官帳已收的糧，為何從未進過倉？",
        "answer": "先以偏秤短收，再用重複稅票與虛假軍糧轉撥掩蓋；首輔私倉的領糧號可與三套帳逐筆相接。",
        "planted": 3,
        "advanced": [
          4,
          9,
          14,
          24
        ],
        "revealed": 36,
        "reserved": false
      },
      {
        "id": "m03",
        "question": "御命為何出不了宮，誰在借程序改命令？",
        "answer": "內廷副印與送達編號被賈勳、首輔共用；最後的假調兵令重複用了早期被擋公文已簽收的送達號，一個號對上兩道命令，偽令因此露底。",
        "planted": 2,
        "advanced": [
          5,
          8,
          11
        ],
        "revealed": 34,
        "reserved": false
      },
      {
        "id": "m04",
        "question": "百姓的收條為何在官府變成欠債？",
        "answer": "同車重複開票，一張作徵稅、一張改成借糧；民間原件、唐家運單與官署底冊核對後可排除假借據。",
        "planted": 6,
        "advanced": [
          9,
          14,
          16
        ],
        "revealed": 33,
        "reserved": false
      },
      {
        "id": "m05",
        "question": "庫房女吏為何突然成為皇族，養母在怕什麼？",
        "answer": "首輔利用她無宗族的處境偽造長房血統，並以弟弟運糧罪迫使羅杏按印；真實收養紀錄證明她是普通孤女。",
        "planted": 1,
        "advanced": [
          8,
          15,
          19
        ],
        "revealed": 20,
        "reserved": false
      },
      {
        "id": "m06",
        "question": "韓鐸為何明知命令不合理仍不願公開反對？",
        "answer": "妹妹被拘禁，軍餉又被寫成他的私借；救出妹妹並公開借據使首輔失去兩道控制。",
        "planted": 5,
        "advanced": [
          12,
          17
        ],
        "revealed": 18,
        "reserved": false
      },
      {
        "id": "m07",
        "question": "葉峻的糧車走了什麼路，他究竟犯了什麼事？",
        "answer": "他冒用過期運糧牌繞過非法關卡救災，沒有劫糧；公開運單與受糧戶證明目的，但冒牌仍須受處分。",
        "planted": 7,
        "advanced": [
          13,
          22,
          25
        ],
        "revealed": 26,
        "reserved": false
      },
      {
        "id": "m08",
        "question": "真正皇族何時入局，他所承諾的糧要付什麼代價？",
        "answer": "蕭承越與首輔早簽繼位及北倉償款草約，婚姻提議只是保住壟斷的新版本；相互留存的附件公開後盟約崩裂。",
        "planted": 10,
        "advanced": [
          15,
          21,
          28
        ],
        "revealed": 35,
        "reserved": false
      },
      {
        "id": "m09",
        "question": "如果大糧戶一起封倉，誰還能讓糧車進城？",
        "answer": "小商戶分批信用、解除私卡、禁軍有界限的護運和公開先付款順序可組成替代商路；代價是各方押上存糧和下季收益。",
        "planted": 12,
        "advanced": [
          12,
          16,
          23,
          27,
          31
        ],
        "revealed": 32,
        "reserved": false
      },
      {
        "id": "m10",
        "question": "沒有皇族血統的人，憑什麼繼續替人作決定？",
        "answer": "救命功績不能代替同意。她先獲限期救災授權，再接受官署、街坊與五供糧州代表的公開議約，數月後以本名、受限制的權力正式被擁立。",
        "planted": 20,
        "advanced": [
          22,
          29,
          30,
          31,
          38,
          39
        ],
        "revealed": 40,
        "reserved": false
      }
    ],
    "naming": [
      "人物使用兩至三字中文姓名；主要人物同姓不暗示暗藏親緣。葉氏姐弟與韓氏兄妹之外不新增親族反轉。葉峻是羅杏與已故丈夫葉氏的兒子；女主是羅杏夫婦收養的孤女，隨葉家姓，「穗」是羅杏給的名字。",
      "國號臨朝、都城衡京；地名以職能易懂為主。承光殿是歷史上用過的殿名，只借名稱，不對應任何真實宮殿。所有具臺詞角色在本冊登記，群臣與群眾只作無臺詞背景。"
    ],
    "never": [
      "不補一段真正皇族血統救回女主身分。",
      "不讓女主用現代知識、神諭或忽然練成的武力破局。",
      "不以救人換戀愛、婚配或軍隊無條件效忠。",
      "不把饑餓者拍成只會鼓掌的群體；沈巧保留發問與否決權。",
      "不借架空古代細節宣稱真實史實；具體度量衡用本作一致的石、斗與倉秤，不比較現代公制。",
      "不把三個月新糧抵達寫成全國已無災害。"
    ],
    "lexicon": {
      "葉穗": "yè suì",
      "裴定衡": "péi dìng héng",
      "韓鐸": "hán duó",
      "羅杏": "luó xìng",
      "葉峻": "yè jùn",
      "何靜": "hé jìng",
      "唐敏": "táng mǐn",
      "賈勳": "jiǎ xūn",
      "蕭承越": "xiāo chéng yuè",
      "韓芮": "hán ruì",
      "沈巧": "shěn qiǎo",
      "糧秤": "liáng chèng",
      "衡京": "héng jīng"
    },
    "ending": "裴定衡被解除兵權、拘押調查，糧款與命令證據留存公開；蕭承越失去糧路壟斷，須退還非法收益並放棄繼位交易。葉峻就冒牌受限期停運與補登處分，沒有因皇親免責。葉穗先作限期救災主持，數月後在各方議約下以本名受擁立，承諾任命、糧政與支款均可追問。她保住位置，卻永遠失去用神秘血統壓倒異議的方便。最後沈巧問第一批新糧的分配，葉穗把帳冊移到自己與百姓之間，回答「先看帳，再叫萬歲。」",
    "opening_30_seconds": [
      {
        "seconds": "0–5",
        "picture": "冠冕扣下，首輔袖邊的祭天簿露出登基第三十日的處死日期；名字仍被印盒遮住。",
        "audio": "葉穗問：「先別叫萬歲，城外吃什麼？」處死日期只向觀眾展示，她未看見祭天簿內容。"
      },
      {
        "seconds": "5–12",
        "picture": "冷色大殿與滿桌熱食；何靜端進一碗南市災民的粥。",
        "audio": "何靜：「今早送來的，就是這個。」"
      },
      {
        "seconds": "12–24",
        "picture": "女主把自己的御膳推開，端起那碗摻沙的稀粥先喝一口，再把同一碗推到首輔面前；其他席面不動。",
        "audio": "葉穗：「我喝過了。首輔也喝一口，再說天下太平。」"
      },
      {
        "seconds": "24–30",
        "picture": "裴定衡不動筷，將宮中可發糧額單壓在女主面前。",
        "audio": "裴定衡：「吃這一碗容易。明日那一萬碗，陛下從哪裡拿？」"
      }
    ]
  },
  "chapters": [
    {
      "number": 1,
      "title": "先讓城裡的人活下來",
      "theme": "命令值多少，要看有多少人真正收到糧。",
      "start_state": "葉穗有冠冕與御印，沒有獨立官署、兵力或家族；仍相信皇族認親。",
      "end_state": "第一批救急糧送到，軍商合作仍有限；她發現祭天真正要處死的是自己。",
      "turn": "從以為自己只是被輕視的新君，轉為確認自己是被預定犧牲的簽字者。",
      "stakes": "第三十日祭天時的性命與城內斷糧倒數。",
      "question": "一枚受制於人的御印，能否換來一碗真正的粥？",
      "episodes": [
        {
          "number": 1,
          "title": "萬歲先喝這碗粥",
          "logline": "葉穗用同一碗粥讓登基宴無法繼續假裝太平，並找出自己能先動用的一筆糧。",
          "hook": "先別叫萬歲，城外吃什麼？",
          "hook_type": "question",
          "conflict": "首輔要她照禮致謝、簽下「糧政無虞」的即位首詔，她要求先看城外實況。",
          "turn": "首輔把即位首詔推到她面前，只等她簽下「糧政無虞」；葉穗擱筆不簽，拿起首輔壓在她面前的那張宮中可發糧額單，問何靜哪一筆是她自己能動的，何靜指出宮宴名下的儀典糧。",
          "cliffhanger": {
            "type": "danger",
            "text": "裴定衡不再看那碗粥，轉頭問端粥的人叫什麼名字，當眾記下「何靜」二字；殿上唯一肯對葉穗說實話的糧吏，已被首輔盯上。"
          },
          "setups": [
            "m01",
            "m05"
          ],
          "payoffs": [],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "pei-dingheng",
            "he-jing"
          ],
          "locations": [
            "hall"
          ],
          "theme": "先承受，才有資格要求。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "villain_humbled",
              "text": "女主撤掉自己的御膳，先喝一口，再把同一碗災民粥放到首輔面前。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "她拒簽糧政無虞，首詔簽名欄留白，逼何靜從宮中可發糧額單列出尚可合法支領的儀典糧。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "登基第 1 日午間",
            "knowledge": "觀眾見到處死日期，葉穗只察覺宴席背後有人安排她的命運；她仍不知血統造假。",
            "character_state": "葉穗尚無盟友，何靜因如實端粥被首輔記住。",
            "evidence": "祭天簿仍在首輔印盒下；未簽首詔由何靜收存。",
            "carry_forward": "東公倉的儀典糧成為次集第一筆可查資源。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 2,
          "title": "先削我的宮宴",
          "logline": "她以縮減宮宴為代價撥出現成糧額，卻發現御命在送達之前就被卡住。",
          "hook": "這些糧，明天拿去煮粥。",
          "hook_type": "line",
          "conflict": "首輔主張儀典不可缺，要求女主先簽總體追認才放行。",
          "turn": "何靜找出既有的宮宴裁減條款，葉穗只動用自己能決定的份額，交換不到全城糧，卻足夠維持一天。",
          "cliffhanger": {
            "type": "choice",
            "text": "領糧牘有御印、沒有內廷副印；葉穗要等待，還是親自到倉驗收？"
          },
          "setups": [
            "m03"
          ],
          "payoffs": [],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "pei-dingheng",
            "he-jing"
          ],
          "locations": [
            "hall",
            "records"
          ],
          "theme": "節省要先從自己開始。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主先裁自己的十日宮宴，不給首輔扣她只讓別人犧牲的理由。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "何靜拿到有御印與明確數額的單項領糧牘，救急第一次有可執行的憑證。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 1 日傍晚",
            "knowledge": "葉穗知道御印不是送達，何靜知道副印被誰保管但尚無證據。",
            "character_state": "宮人飲食縮減，葉穗接受同份口糧。",
            "evidence": "領糧牘正本由何靜攜帶，副本留宮內。",
            "carry_forward": "帶領糧牘去東公倉查實際庫存。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 3,
          "title": "滿帳空倉",
          "logline": "帳本聲稱儀典糧充足，實際倉門後只有半垛麻袋；葉穗先把能用的糧分出，拒絕替不存在的糧簽收。",
          "hook": "帳上滿倉，袋子在哪？",
          "hook_type": "question",
          "conflict": "賈勳要求照帳領糧並簽足額，否則連剩下的也不交。",
          "turn": "葉穗用入倉秤號與袋口縫法，指出兩批紀錄其實引用同一垛糧；何靜同意當場重列。",
          "cliffhanger": {
            "type": "reveal",
            "text": "賈勳帶來的足額收訖最後一行寫著「新君盡知並承其責」；葉穗認出，這張紙要她簽下的不是糧數，是罪責。"
          },
          "setups": [
            "m02",
            "m01"
          ],
          "payoffs": [
            "m01"
          ],
          "tension": [
            4,
            3,
            5,
            4,
            5
          ],
          "characters": [
            "ye-sui",
            "he-jing",
            "jia-xun"
          ],
          "locations": [
            "granary"
          ],
          "theme": "簽字之前，要看見東西。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "葉穗只在親手點過的麻袋上畫記號，拆穿把一垛算兩次的帳法。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "villain_humbled",
              "text": "賈勳被迫允許實領實簽，剩餘救急糧不再因她拒認空數而被扣。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 2 日清晨",
            "knowledge": "局部回收 m01：她明白對手反覆逼她承責；收訖與祭天簿格式相同只有觀眾對照得出，她沒看過祭天簿，也不知道有處死日期。m02 僅確定帳物不符。",
            "character_state": "何靜首次站到女主一側，仍害怕自己的抄帳責任。",
            "evidence": "實點表由女主與何靜各存一份；疑似重複秤號抄在表邊；那張寫著承責字樣、她沒簽的足額收訖由葉穗留存。",
            "carry_forward": "必須確認當日午間分糧使用的秤是否也被做手腳。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 4,
          "title": "秤砣也會說謊",
          "logline": "葉穗公開對秤，把原本會在分糧時消失的一截重量留下，卻暴露了官倉與關卡使用不同標準。",
          "hook": "同一袋糧，怎麼越秤越輕？",
          "hook_type": "question",
          "conflict": "賈勳聲稱官秤不能被一個新君質疑，沈巧拒領不足額口糧。",
          "turn": "葉穗用封存校秤砣對照兩臺秤，不靠目測定罪，讓在場者看見偏差。",
          "cliffhanger": {
            "type": "reversal",
            "text": "少掉的重量找回了；賈勳卻說南糧關按另一臺秤抽糧，足額出倉，過了關仍可能只剩半車進城。"
          },
          "setups": [
            "m02"
          ],
          "payoffs": [
            "m02"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "jia-xun",
            "he-jing",
            "shen-qiao"
          ],
          "locations": [
            "granary"
          ],
          "theme": "標準公開，弱者才有話說。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "public_vindication",
              "text": "沈巧要求重秤被接納，女主用校秤砣證明她不是貪領。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "葉穗封存偏秤，讓何靜以校準後的份額補齊本日口糧。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 2 日午間",
            "knowledge": "m02 局部回收短收方法，尚未知去向；葉穗得知關卡另有障礙。",
            "character_state": "沈巧感謝但要求每次分糧可旁觀，女主接受。",
            "evidence": "偏秤與校砣封存東公倉，由何靜、沈巧雙方記錄。",
            "carry_forward": "要讓足額糧走過南糧關，需有限度軍隊護運。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 5,
          "title": "只護這一趟",
          "logline": "葉穗用實物口糧換得禁軍一次護車，韓鐸卻在收到一張藥單後改變原定路線。",
          "hook": "妳要兵，先讓兵吃飯。",
          "hook_type": "line",
          "conflict": "韓鐸拒絕空口軍令；賈勳以副印不全擋糧車。",
          "turn": "葉穗把已核實的糧分出值守份額並記帳，韓只答應護送一趟，要求她不把士兵拉去抄家。",
          "cliffhanger": {
            "type": "danger",
            "text": "藥單送到韓手中，他忽然停車；上面畫著妹妹隨身荷包的花樣。"
          },
          "setups": [
            "m03",
            "m06"
          ],
          "payoffs": [
            "m03"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "jia-xun"
          ],
          "locations": [
            "granary",
            "gate"
          ],
          "theme": "合作的邊界必須說清。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主先交實糧而非畫餉餅，韓鐸當場讓士兵把車推上出倉道。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "她要求賈勳寫出拒收公文的理由並留回執，御命遭擋第一次留下具名紀錄。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 3 日清晨",
            "knowledge": "m03 局部回收：卡住命令的人須承擔可追查紀錄；女主只知韓被某物威脅。",
            "character_state": "禁軍合作限一次運糧，韓的家屬危機首次可見。",
            "evidence": "拒收回執由葉穗持有；威脅藥單在韓手裡。",
            "carry_forward": "韓不能正面撞卡，需在護糧承諾內改車隊走法。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 6,
          "title": "把大車拆成小車",
          "logline": "葉穗與唐敏談妥額外車工，分批走仍開放的小道，拿到同一車糧被抽了兩次糧的收條。",
          "hook": "他攔一條路，我們分三趟。",
          "hook_type": "reversal",
          "conflict": "大車被扣，唐敏不願讓夥計白冒險，韓又不能帶兵擅闖民戶。",
          "turn": "葉穗用自己宮中可變賣的非印信器物作短期貨款抵押，唐敏才讓小車分批通行；唐敏的糧向南面三個供糧州收來，大車過不了南糧關，小車還能繞渡口小道。",
          "cliffhanger": {
            "type": "choice",
            "text": "第二張徵糧收條竟把已付的稅寫成借糧；女主能先送糧，還是扣住車立即對帳？"
          },
          "setups": [
            "m04"
          ],
          "payoffs": [],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "tang-min",
            "han-duo"
          ],
          "locations": [
            "depot",
            "gate"
          ],
          "theme": "讓人冒險之前，先付自己的部分。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "first_clear",
              "text": "女主把運輸需求拆成現有車輛做得到的三批，第一批立即出棧。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "rescue",
              "text": "韓按事先限定的巡線護送小車，粥場本日不必停火。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 3 日傍晚",
            "knowledge": "m04 埋下矛盾收條，尚未確認重複是錯誤還是系統作假。",
            "character_state": "唐敏取得抵押與付款期限，韓未越出巡防界限。",
            "evidence": "兩張同車收條由唐敏保管，葉穗只抄編號。",
            "carry_forward": "先把糧交給粥場，再由醫棚與戶籍確認誰真正收到。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 7,
          "title": "有粥，也要有人看病",
          "logline": "女主把施粥與醫棚接在一起，弟弟主動接手車工；羅杏看見那張沒簽的足額收訖上的承責用語後異常驚慌。",
          "hook": "糧到了，為什麼還有人倒？",
          "hook_type": "question",
          "conflict": "群眾排隊過長，部分人已虛弱到吃不下；女主不能只按出糧總數算成功。",
          "turn": "羅杏分開病弱與一般領糧隊伍，葉峻把小車改作送到巷口，沈巧逐戶記錄。",
          "cliffhanger": {
            "type": "emotion",
            "text": "羅杏要女兒別再碰那張寫著承責的收訖，卻說不出原因；葉穗第一次問她：「妳到底在怕誰？」"
          },
          "setups": [
            "m01",
            "m07"
          ],
          "payoffs": [
            "m01"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "luo-xing",
            "ye-jun",
            "shen-qiao"
          ],
          "locations": [
            "relief"
          ],
          "theme": "被救的人不能只是帳上的總數。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "女主停止讓虛弱者繼續排長隊，交由羅杏分流，葉峻把份額送進巷內。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "沈巧的受糧戶簿把「出倉」接到「領到」，堵住只報車數的空隙。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 4 日清晨",
            "knowledge": "m01 局部回收：承責字樣與羅杏的恐懼有關；葉穗尚未查清。葉峻胸前舊運糧牌首次清楚入鏡。",
            "character_state": "葉穗與養母親近卻產生戒心，弟弟有自己的救災工作。",
            "evidence": "受糧戶簿由沈巧保管；舊運糧牌用繩掛在葉峻胸前，未交給女主。",
            "carry_forward": "糧到了但女主發給其他粥場的命令仍未傳出宮。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 8,
          "title": "讓命令走出門",
          "logline": "葉穗利用每件公文應有的送達回執逼開文簿房封鎖，看到自己的族譜證明竟與上月檔案共用新紙。",
          "hook": "御印在這，誰敢說沒收到？",
          "hook_type": "line",
          "conflict": "內廷讓女主的公文無限停在待補副印，賈勳否認自己有權處理。",
          "turn": "何靜取出舊規，女主在公開朝議只問「現在誰保管」，逼賈勳簽名接收而不是立刻服從。",
          "cliffhanger": {
            "type": "reveal",
            "text": "為調卷查送達號，何靜翻開認親冊；號稱多年舊證的紙邊有上月新紙批記。"
          },
          "setups": [
            "m03",
            "m05"
          ],
          "payoffs": [
            "m03",
            "m05"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "he-jing",
            "jia-xun"
          ],
          "locations": [
            "records",
            "hall"
          ],
          "theme": "把「沒有人負責」改成一個名字。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "villain_humbled",
              "text": "葉穗只要求賈勳在眾目下簽收，他無法再把公文藏在無名程序裡。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "第一份帶雙方回執的分糧命令交到外署，女主得到可持續追送達的方法。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 4 日傍晚",
            "knowledge": "m03 局部解開封鎖方法；m05 僅得知族譜可能是近期謄抄，尚不能認定偽造。",
            "character_state": "何靜替女主抄回執，自身風險增加。",
            "evidence": "認親冊原件仍在文簿房，紙批記由何靜描錄；賈勳簽收的分糧命令回執載有送達號，由何靜保存。",
            "carry_forward": "新到的關卡回執要與唐敏的兩張收條核對。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 9,
          "title": "同一袋糧收兩次",
          "logline": "女主讓商家與街坊當面對收條，發現雙重徵糧是固定流程、還牽涉軍糧欄；她保住了原件，唐敏的糧車卻被扣在關內。",
          "hook": "這袋糧，你們收過兩次。",
          "hook_type": "reversal",
          "conflict": "賈勳以一張是稅、一張是借糧的說法拆開責任，試圖讓唐敏與百姓互相指責。",
          "turn": "沈巧的領糧日期與唐敏的車號相接，證明不是不同批次；葉穗再把何靜先前交來的抄頁展開，指出同日軍糧轉撥空欄。賈勳關門要索走原件，葉穗要他在核查回執上寫明「扣留持單者」並署名；他不肯署名，只得放唐敏、沈巧帶原件離開，改開前往文簿房驗底冊的傳核單。",
          "cliffhanger": {
            "type": "danger",
            "text": "人放走了，車沒有：賈勳以副印不全為由落下關門，把唐敏明早要送粥場的三車糧扣在欄內待驗。"
          },
          "setups": [
            "m02",
            "m04"
          ],
          "payoffs": [
            "m02",
            "m04"
          ],
          "tension": [
            4,
            3,
            5,
            4,
            5
          ],
          "characters": [
            "ye-sui",
            "jia-xun",
            "tang-min",
            "shen-qiao"
          ],
          "locations": [
            "gate"
          ],
          "theme": "分開的人各說各話，合起來的帳說同一件事。",
          "lead_arc": "suffers",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "public_vindication",
              "text": "葉穗讓兩名持單者同時說出車號，證明街坊沒有少繳、商人沒有虛報。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "她要求原件各自保管、只封存雙方抄件，阻止賈勳一次拿走證據。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 5 日午間",
            "knowledge": "m02 局部得知重複稅牽涉轉撥；m04 局部確定雙收不是記錯，尚需官府底冊。",
            "character_state": "唐敏與沈巧由互疑轉為共同保管證據；唐敏的三車糧被扣，對葉穗的信任打了折扣，明早的粥場少了一批糧。",
            "evidence": "唐敏保運單，沈巧保民間原條，兩人已帶原件離開；兩份互認抄件送文簿房；傳核單在葉穗手上；唐敏的三車糧扣在南糧關欄內待驗。",
            "carry_forward": "葉穗利用入文簿房查轉撥的理由追到祭天承責卷；被扣的三車糧成為首輔下一集的籌碼。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 10,
          "title": "祭天名冊上的人",
          "logline": "她順著轉撥責任找到祭天罪詔，確定自己只被留了三十天，另一份繼位草約已先備好。",
          "hook": "祭天要殺的人，是我。",
          "hook_type": "danger",
          "conflict": "裴定衡要她把救災成果一起簽成追認舊帳，說簽了，南糧關扣下的三車糧今晚就放行。",
          "turn": "何靜利用剛建立的送達紀錄定位附件，葉穗讀到自己的名字與處死日期，知道當面拒簽會讓對手提前收網；回到殿上，她不簽也不拒，只說帳還沒對完、追認留到祭天前一併簽，首輔以為時間仍在自己手上，三車糧也照樣扣著。",
          "cliffhanger": {
            "type": "reveal",
            "text": "罪詔末頁後還有一張繼位草約，上面留了旁支皇族蕭承越的接位位置。"
          },
          "setups": [
            "m08"
          ],
          "payoffs": [
            "m01"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "pei-dingheng",
            "he-jing"
          ],
          "locations": [
            "records",
            "hall"
          ],
          "theme": "知道自己被安排犧牲，才開始選擇如何活。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "first_clear",
              "text": "女主由自己留下的送達號找到罪詔，確定威脅而非繼續猜疑。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "她把原卷放回不驚動首輔，何靜帶走注明原卷頁號、蓋了騎縫押的抄錄，第一次保住對手尚不知她掌握的資訊。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 5 日夜間",
            "knowledge": "m01 完整揭曉：追認挪糧、祭天代罪相連。m08 僅看見蕭承越名字，未知北倉苛約。",
            "character_state": "葉穗恐懼但決定暫不翻桌；何靜承諾只記實證；唐敏的三車糧仍扣在關內。",
            "evidence": "罪詔原件在首輔控制的卷內；騎縫抄錄分藏女主與何靜處；追認文書她沒有簽，仍在首輔手中。",
            "carry_forward": "次集假裝配合祭天，用有限時間拓寬糧路，並把被扣的三車糧要回來。"
          },
          "timeline": "present",
          "closed_ending": false
        }
      ]
    },
    {
      "number": 2,
      "title": "每一次合作都要付帳",
      "theme": "信任不是一次表態，是每次兌現。",
      "start_state": "葉穗知道祭天殺局，但首輔仍掌握文書與糧路。",
      "end_state": "女主取得有限軍商信任並救出被扣家屬，卻確認自己連皇族身分都是偽造。",
      "turn": "她以為可以用帝王身分對抗權臣，最後發現這身分也是權臣給的繩索。",
      "stakes": "已參與救災的人會因她失敗而被追究。",
      "question": "在真正的身世被揭開以前，她能交付多少真實的承諾？",
      "episodes": [
        {
          "number": 11,
          "title": "照你們的日子祭天",
          "logline": "葉穗假意接受祭天行程，以籌備名義取得公文追送權，讓首輔把自己的祭天日程寫進紙面。",
          "hook": "祭天可以，先給我送達簿。",
          "hook_type": "line",
          "conflict": "首輔要她停止查舊帳，專心背祭文；她需要合法時間接觸各署。",
          "turn": "她答應照原定日期出席，交換每日糧務進度附在祭天準備簿中，何靜可逐筆索取回執。準備簿附的糧路圖上，五供糧州有三州的糧要過南糧關、兩州先進北倉，全城的糧路第一次攤在同一張圖上。",
          "cliffhanger": {
            "type": "choice",
            "text": "首輔只肯放開一處關卡的核查權；葉穗在糧路圖上指向扣著唐敏三車糧的南糧關。"
          },
          "setups": [
            "m03"
          ],
          "payoffs": [
            "m03"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "pei-dingheng",
            "he-jing"
          ],
          "locations": [
            "hall",
            "records"
          ],
          "theme": "可以示弱，但不能交出查證的方法。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "她用首輔要求的祭天日期換到送達簿，將被動倒數變成查帳期限。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "何靜拿到索取具名回執的書面授權，連首輔的拒絕也必須留痕。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 6 日",
            "knowledge": "m03 局部回收：公文鏈可以用對手承認的程序延伸；首輔不知道罪詔已被抄下。",
            "character_state": "葉穗表面配合，何靜須每日交公開進度避免失蹤即斷線；南市粥場因三車糧被扣，本日減半開火。",
            "evidence": "祭天準備簿與核查授權各有抄件。",
            "carry_forward": "南糧關將迎來一次有期限的現場核查。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 12,
          "title": "關卡不是誰的錢袋",
          "logline": "女主撤掉查無設立文書的臨時私卡，唐敏取得一條可談合作的商路，韓鐸的沉默也露出原因。",
          "hook": "這道關，是誰批准的？",
          "hook_type": "question",
          "conflict": "賈勳聲稱所有欄杆都屬軍事管制，韓鐸卻不能直接否認上級。",
          "turn": "葉穗只拆沒有軍令編號的臨時欄杆，扣在欄內的三車糧隨撤欄放行，比原定晚了一天送到粥場；韓承認自己從未部署該卡；唐敏吃過一次虧，只允諾先試送一車。",
          "cliffhanger": {
            "type": "danger",
            "text": "賈勳當面問韓「北偏院今天的藥送到了嗎」，韓握住刀柄，沒有拔刀。"
          },
          "setups": [
            "m06",
            "m09"
          ],
          "payoffs": [
            "m06",
            "m09"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "jia-xun",
            "han-duo",
            "tang-min"
          ],
          "locations": [
            "gate"
          ],
          "theme": "先拆掉能證明不合法的那一道。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "villain_humbled",
              "text": "賈勳拿不出臨時卡的設立文書，女主讓他自己簽下撤欄命令。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "唐敏用一車小額試運驗證通道，替代商路第一次有可量測的成本。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 7 日",
            "knowledge": "m06 局部揭示威脅源在北偏院，尚未知人質身分；m09 初步回收私卡撤除可以降低運糧成本。",
            "character_state": "韓壓下衝動，女主不逼他此刻坦白。",
            "evidence": "撤欄回執在何靜管理的文簿中，試運約由唐敏持有。",
            "carry_forward": "下一集必須讓承諾的試運糧真正抵達，不能只拍拆欄。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 13,
          "title": "讓車替命令作證",
          "logline": "當反對者聲稱撤卡只會放進劫糧者時，葉峻帶回一車可逐戶核對的救命糧。",
          "hook": "別看詔書，看車有沒有到。",
          "hook_type": "line",
          "conflict": "沈巧不願以一句皇命就排隊等待，唐敏的夥計擔心送出後收不到錢。",
          "turn": "葉穗讓運單與受糧戶簿同時公開，先付約定的首期車工，葉峻主動補上自己繞行的時間。",
          "cliffhanger": {
            "type": "reversal",
            "text": "首車到達證明通道可用；沈巧卻發現葉峻的運糧牌早已過期。葉穗只對弟弟說：「牌收起來，往後只拿唐敏的運單跑。」沒有說要呈報。"
          },
          "setups": [
            "m07"
          ],
          "payoffs": [
            "m07"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "ye-jun",
            "tang-min",
            "shen-qiao"
          ],
          "locations": [
            "relief"
          ],
          "theme": "承諾要有收貨的人。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "first_clear",
              "text": "葉穗讓第一批受糧戶當場點數，撤卡的成果落在碗裡。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "唐敏收到已約定的首期車工，小商戶不再被說成只會哄抬糧價。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 8 日",
            "knowledge": "m07 局部回收葉峻確實送糧，舊牌疑點仍在；葉穗從這一天起知道牌已過期，要他停用、只憑唐敏的新運單跑車，但沒有呈報，也還不知道他曾冒用牌的路段。",
            "character_state": "葉峻把過期牌收進衣內；沈巧把這件事照實記進受糧戶簿，沒有替他遮掩；葉穗知情未報，這筆帳記在她自己身上。",
            "evidence": "新運單正本交唐敏，受糧戶簿交沈巧，首期付款有女主簽名；過期牌由葉峻收在衣內，此後不再外露。",
            "carry_forward": "收條公開後，街坊帶來更多被改成借據的原件。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 14,
          "title": "誰欠誰的糧",
          "logline": "何靜把重複收條與所謂借據疊在一起，證明街坊遭偽造債務，追出侵吞鏈中的轉抄方法。",
          "hook": "欠糧的是官府，不是你們。",
          "hook_type": "reversal",
          "conflict": "賈勳要以未還借糧為由追收受災戶的下一季種糧。",
          "turn": "同一紙的車號與角缺對得上，何靜承認自己曾被迫抄過假欄；女主先封停追收，沒有宣佈所有借據一概作廢。",
          "cliffhanger": {
            "type": "reveal",
            "text": "被圈出的偽借據都指向同一軍糧轉撥批號，而真正的收糧人欄被撕掉了。"
          },
          "setups": [
            "m02",
            "m04"
          ],
          "payoffs": [
            "m02",
            "m04"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "he-jing",
            "jia-xun",
            "shen-qiao"
          ],
          "locations": [
            "records"
          ],
          "theme": "承認自己抄錯的那一欄，才能保住別人。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "女主依具體對上的原件暫停追收種糧，受災戶不必立刻交出下季生計。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "何靜當面承認轉抄受迫，讓沈巧的民間原條獲得與官帳同桌比對的地位。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 9 日",
            "knowledge": "m04 局部揭示借據偽造方法，尚缺完整官府底冊；m02 局部連到軍糧批號。",
            "character_state": "何靜承擔抄帳責任，葉穗答應查清各人行為而非保她無罪。",
            "evidence": "對照頁公開抄錄，撕口軍糧欄原件仍封在文簿房。",
            "carry_forward": "需要商人掌握的外部糧契，補足收糧去向。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 15,
          "title": "糧商不收空頭萬歲",
          "logline": "女主與唐敏訂下限期付款、不得強徵車工的協議，意外看見北倉條款與自己認親用紙來自同一批。",
          "hook": "這筆誰出？把名字寫下來。",
          "hook_type": "line",
          "conflict": "唐敏可提供存糧但不能押上全部家底，葉穗的御印本身已不值得信任。",
          "turn": "女主接受公開分批付款與違約時停供的條件，先用宮宴裁減省下的銀錢作有限承諾；唐敏承認自己原本打算簽下北倉排他草約求生，現在把它交出供查。",
          "cliffhanger": {
            "type": "choice",
            "text": "北倉願保全城一月供應，但要小商戶永久放棄自運；女主拒絕立刻簽下看似最快的解法。"
          },
          "setups": [
            "m05",
            "m08"
          ],
          "payoffs": [
            "m05",
            "m08"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "tang-min",
            "he-jing"
          ],
          "locations": [
            "depot"
          ],
          "theme": "公平的條件能比恩情走得更久。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主同意商戶可因未付款停供，讓唐敏有承擔風險後的退路。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "唐敏在有上限的合約下放出第二批存糧，並交出北倉草約，不再只有口頭支持。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 10 日",
            "knowledge": "m08 局部揭示北倉援糧附排他條件；m05 紙批相同增加近期共同策劃疑點，仍非血統定論。",
            "character_state": "唐敏押上本季存糧的一部分，葉穗失去任意延期還款的方便。",
            "evidence": "雙方各持簽名合約，北倉草約由何靜抄錄、唐敏保原件。",
            "carry_forward": "追回的糧與省下的銀錢都有限，下一集需選擇如何支付欠餉與貨款。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 16,
          "title": "先把欠的餉送到手",
          "logline": "葉穗把已追回的重複抽糧按公開順序折給值守軍戶當欠餉，延後的一筆貨款也當面說清。",
          "hook": "欠了三個月，今天先還一份。",
          "hook_type": "line",
          "conflict": "首輔府送來的便箋暗示，只要把追回的糧和省下的銀錢全給禁軍就能買到效忠；唐敏卻也到了約定收款日。",
          "turn": "女主先把追回的糧折成軍戶最基本的欠餉口糧，再用省下的銀錢付商戶已承諾的首款，讓餘款分期；韓與唐敏都只能拿到部分，但看見同一張支款表。",
          "cliffhanger": {
            "type": "danger",
            "text": "軍戶領到糧後，韓鐸收到新信：他的妹妹將在翌日被轉送出城。"
          },
          "setups": [
            "m04",
            "m09"
          ],
          "payoffs": [
            "m04",
            "m09"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "tang-min",
            "he-jing"
          ],
          "locations": [
            "granary"
          ],
          "theme": "不夠分的時候，更不能藏起順序。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "public_vindication",
              "text": "女主讓軍戶看見追回糧的來源，欠餉不是統領私吞的謠言先被拆掉一角。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "唐敏同意有明文截止日的餘款延後，換來下批運輸先款一半；軍戶與商戶看得見彼此分到多少，不必互相猜忌。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 11 日",
            "knowledge": "m04 局部回收：被重複抽走的糧確能追回一部分；m09 顯示替代商路靠付款信用而非免費輸血。",
            "character_state": "軍商都付出等待代價，韓的家屬危機升高。",
            "evidence": "逐筆支款表由何靜、韓、唐三方留份，轉送信在韓手中。",
            "carry_forward": "韓必須告訴女主北偏院扣著誰，才能規劃合法救人。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 17,
          "title": "統領收到的那封信",
          "logline": "韓鐸交出妹妹被扣與軍餉私借的雙重威脅，葉穗選擇先解開人質而非逼他立刻反首輔。",
          "hook": "他們扣著我妹妹。",
          "hook_type": "line",
          "conflict": "韓怕出兵救人會坐實私借軍糧與叛逃，羅杏也不能讓病人被當成攻院掩護。",
          "turn": "羅杏先依既有診療紀錄要求停止當日跨城移送，具名承諾翌日公開點名轉診；首輔府為維持療養名義，回文送到醫舍准延一天，條件是軍隊不得入院。女主拿到轉送名冊，韓交出軍餉借據接受核查。",
          "cliffhanger": {
            "type": "reveal",
            "text": "藥單副印與賈勳的雙重徵糧印相同，拘禁與糧款威脅竟在同一套公文裡。"
          },
          "setups": [
            "m06"
          ],
          "payoffs": [
            "m06"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "luo-xing"
          ],
          "locations": [
            "clinic"
          ],
          "theme": "把軟肋說出來，才可能一起承擔。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "葉穗不要求韓用妹妹性命表忠，先將救人和軍令分開規劃。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "羅杏具名接下翌日轉診責任，換得暫緩當日跨城移送及病患名單，取得一天可準備的出口。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 12 日",
            "knowledge": "m06 局部揭示妹妹與假借據雙重牽制，尚未成功解除。",
            "character_state": "韓第一次坦白，羅杏以醫者條件限定救援方式。",
            "evidence": "軍餉借據交何靜核實；當日暫緩跨城移送回執與翌日換診名單由羅杏帶往偏院。",
            "carry_forward": "次集救援必須連同其他病人安全轉送，不能只偷走韓芮。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 18,
          "title": "換診的那一天",
          "logline": "羅杏依法轉送病患，韓芮帶出移送紀錄；女主不以救命恩情索取無限兵權。",
          "hook": "名冊上每個人，都一起走。",
          "hook_type": "line",
          "conflict": "偏院以少一張副印拖住病患，韓芮拒絕自己逃走留下其他人。",
          "turn": "女主拿出公開的換診送達回執，羅杏逐名交接；韓只在已授權的院門外護送，讓阻攔者必須承擔延診責任。",
          "cliffhanger": {
            "type": "emotion",
            "text": "韓鐸要跪謝，葉穗扶住他的手：「下次我的命令錯了，你還能不能攔我？」"
          },
          "setups": [],
          "payoffs": [
            "m06"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "han-rui",
            "luo-xing"
          ],
          "locations": [
            "annex",
            "clinic"
          ],
          "theme": "救出一個人，不是買下另一個人。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "韓芮與名冊上的病患依序上車，女主兌現不以他人性命換人質的條件。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "韓芮交出藥單副印紀錄、韓公開假借據，首輔不能再同時用人和債勒住統領。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 13 日",
            "knowledge": "m06 完整回收控制機制與解除代價；韓仍受正常軍令約束。",
            "character_state": "韓芮腕部留下淡拘束痕，能步行但需休養；韓與女主有相互勸止的合作。",
            "evidence": "移送藥單由韓芮與何靜各存一份，軍餉核帳進入公開程序。",
            "carry_forward": "首輔轉而逼羅杏交出認親時留下的真實收養紀錄。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 19,
          "title": "養母沒有燒掉的紙",
          "logline": "首輔威逼羅杏交出舊紀錄，葉穗靠先前紙批線索追到醫舍，聽見養母承認認親文書有假，首輔卻帶走了能拆穿她的副本。",
          "hook": "妳把我交給他們，為什麼？",
          "hook_type": "question",
          "conflict": "羅杏怕交原件害死女兒，藏原件又可能害死被追查舊運糧罪的葉峻。",
          "turn": "她決定讓葉穗親自讀真實收養簿，拒絕繼續替首輔保持沉默；首輔只帶走她預先抄下的副本。",
          "cliffhanger": {
            "type": "danger",
            "text": "收養簿記著女主被救起的日期，比皇族失蹤案早了整整兩年；首輔帶走的副本上，也抄著同一個日期。"
          },
          "setups": [
            "m05"
          ],
          "payoffs": [
            "m05"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "luo-xing",
            "pei-dingheng"
          ],
          "locations": [
            "clinic"
          ],
          "theme": "保護若只靠謊言，終究會變成另一種綑綁。",
          "lead_arc": "suffers",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "羅杏把真簿先交女兒，不再由首輔決定她能知道多少。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "villain_humbled",
              "text": "首輔索要原件，羅杏當面要求列出收取理由，原件保住，只讓具名副本離開醫舍。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 14 日",
            "knowledge": "m05 接近答案：羅杏承認受迫按印，葉穗從這一天（第 14 日）起算自己的知情；尚需族譜、失蹤案與收養日期三方確證。",
            "character_state": "葉穗受傷的是信任，仍讓羅杏說完，不立刻原諒；首輔手上有了收養副本，隨時能搶先揭露她的身世。",
            "evidence": "真實收養簿正本由葉穗帶到文簿房，羅杏預先抄下的副本已被首輔拿走。",
            "carry_forward": "女主與何靜將三份時間證據放到同一張桌上。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 20,
          "title": "把三份日期放在一起",
          "logline": "三份可交叉核對的日期證明葉穗不是皇族，她必須決定是否繼續借謊言完成救災。",
          "hook": "連這個身分，也是他們造的。",
          "hook_type": "reversal",
          "conflict": "何靜指出公開身世會使所有依御印簽的協議被質疑，首輔手上的收養副本又隨時能搶先揭露；羅杏願獨自承擔偽證，希望女兒逃走。",
          "turn": "葉穗區分本名與假血統：葉穗是養母給的名字，偽造的是出身。她先保存真簿，再決定找出能替代血統的授權方式。",
          "cliffhanger": {
            "type": "reveal",
            "text": "首輔下一封已送出的迎駕公文寫著：真正的皇族蕭承越，明日入城。"
          },
          "setups": [
            "m10"
          ],
          "payoffs": [
            "m05"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "he-jing",
            "luo-xing"
          ],
          "locations": [
            "records"
          ],
          "theme": "身分可以被偽造，已做過的事不能。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "first_clear",
              "text": "女主用三份日期與紙批確證身世，不再把首輔的暗示當真相。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "她拒絕讓養母獨自代罪，將脅迫經過與自己從第 14 日起的知情時間一併封存，準備承擔公開後果。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 15 日夜間",
            "knowledge": "m05 全揭：普通孤女、脅迫按印、假長房血統。m10 埋下沒有血統仍能否治理的問題。",
            "character_state": "母女尚未完全和解；葉穗願留下但不再相信冠冕等同資格。",
            "evidence": "三份日期證據交叉抄存；收養簿正本由羅杏收回封存，何靜持一份騎縫抄本。",
            "carry_forward": "蕭承越帶著真正血統與能立刻供糧的籌碼入城。"
          },
          "timeline": "present",
          "closed_ending": false
        }
      ]
    },
    {
      "number": 3,
      "title": "糧車後面的條件",
      "theme": "守住位置若要出賣他人，留下來便沒有意義。",
      "start_state": "女主知道假身世，群眾仍未知；真正皇族帶北倉糧與秩序承諾入城。",
      "end_state": "葉穗拒絕婚姻與殺弟交易，搶在祭天前坦白假血統，失去以身分發令的保護。",
      "turn": "從設法保住皇權變為請眾人決定是否繼續給她救災權限。",
      "stakes": "弟弟性命、替代商路、群眾是否願意接受知情的合作。",
      "question": "若代價是犧牲自己答應保護的人，留下來還有什麼用？",
      "episodes": [
        {
          "number": 21,
          "title": "有糧的皇族",
          "logline": "蕭承越以真族譜和北倉糧入城，葉穗承認他的資源價值，同時要求把附帶條件放到桌上。",
          "hook": "他一來，就帶了三十車糧。",
          "hook_type": "image",
          "conflict": "北倉車隊從北門直接開到南市施粥場，讓百姓與官員看到立即穩定的可能，女主若只攻擊血統反而像保位。",
          "turn": "她接納按公開價格出售的救急糧，拒絕把糧款與接位承諾綁在一起；蕭承越只卸兩車展示誠意。",
          "cliffhanger": {
            "type": "choice",
            "text": "剩下二十八車可立刻卸下，只要她先簽一張排他採買約。"
          },
          "setups": [
            "m08"
          ],
          "payoffs": [
            "m08"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "xiao-chengyue",
            "tang-min",
            "shen-qiao"
          ],
          "locations": [
            "relief"
          ],
          "theme": "有用的援手，也可以帶著不公平條件。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主把公開售糧與效忠接位分開，使前兩車糧能先救急而不替皇族背書。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "唐敏在兩車單價背面標出其他車的長期代價，街坊第一次看到「有糧」之外的條件。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 16 日",
            "knowledge": "m08 局部揭示真皇族支持來自實物糧與穩定承諾，尚無共同安排祭天的確證。",
            "character_state": "部分群眾支持蕭，沈巧不因曾受葉穗幫助就拒絕便宜糧。",
            "evidence": "兩車公開買賣收條由唐敏持有，排他約未簽。",
            "carry_forward": "女主須直接聽街坊的需求與疑問，不能代替他們拒絕援助。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 22,
          "title": "讓受災的人自己說",
          "logline": "葉穗開放街坊帶收條陳情，第一次聽到有人寧願換一位有糧的君主，也看到弟弟救災路線的證人。",
          "hook": "你要謝我，也可以反對我。",
          "hook_type": "line",
          "conflict": "沈巧怕陳情變成被安排的感恩場面，葉峻想替姐姐反駁質疑。",
          "turn": "女主制止弟弟替她答話，把待解決事項按到糧日期公開；受糧戶的紀錄證明葉峻確實走過偏巷。",
          "cliffhanger": {
            "type": "emotion",
            "text": "沈巧問：「如果妳不是坐這個位置的人，這些話還算不算？」葉穗沒有用血統作答。"
          },
          "setups": [
            "m07",
            "m10"
          ],
          "payoffs": [
            "m07",
            "m10"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "ye-jun",
            "shen-qiao",
            "he-jing"
          ],
          "locations": [
            "relief"
          ],
          "theme": "被幫助不等於必須服從。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "public_vindication",
              "text": "女主讓一張批評她延遲發糧的申訴留在公開簿上，不把反對者趕走。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "何靜把申訴改成具名到糧期限，三戶漏領者當場補登，不再只是聽一場演說。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 17 日",
            "knowledge": "m07 局部補足受糧證詞；m10 首次回收民眾需要的是可追責交付，不是感恩口號。",
            "character_state": "葉峻接受姐姐也會被質問，葉穗愈難繼續隱瞞身世。",
            "evidence": "陳情簿向街坊開放抄錄，偏巷收糧日期與葉峻運單一致；過期牌仍收在葉峻衣內，胸前無牌。",
            "carry_forward": "公開需求量讓大糧戶知道斷供將造成多大壓力。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 23,
          "title": "鎖住的不是空倉",
          "logline": "豪族集體封倉，女主拒絕立即強徵，把僅剩的存糧與小商戶供應時間公開，爭取短期替代。",
          "hook": "倉裡有糧，門卻一起鎖了。",
          "hook_type": "danger",
          "conflict": "蕭承越以市價與契約為由不再卸糧，唐敏存貨只夠再撐兩天。",
          "turn": "葉穗公開削減宮廷與非必要官署配給，向各商戶訂小額批次，不假稱這些糧足以長久替代。",
          "cliffhanger": {
            "type": "danger",
            "text": "唐敏說能找到下一批糧，但軍隊若不護路，所有已借來的小車都會被截回。"
          },
          "setups": [
            "m09"
          ],
          "payoffs": [
            "m09"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "tang-min",
            "xiao-chengyue"
          ],
          "locations": [
            "depot",
            "granary"
          ],
          "theme": "資源短缺時，誠實比虛張聲勢更值錢。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主先減宮廷配給，把封倉壓力的一部分由掌權者承擔。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "唐敏以透明的短期回款表說服小商戶各出一小份，湊出兩日緩衝。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 18 日",
            "knowledge": "m09 局部回收分批小額可爭取時間，但護路與信用尚不足。",
            "character_state": "女主及官署領更少口糧，唐敏押上與同行的信用；本批僅支應第 18–19 日，後續不能沿用本批庫存。",
            "evidence": "各家短約分別保管，女主只承諾已有來源的支出。",
            "carry_forward": "首輔將從軍糧入手，逼韓鐸撤掉護路人手。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 24,
          "title": "被扣住的軍糧",
          "logline": "首輔以欠款未清卡住禁軍口糧，何靜找到軍糧其實曾被轉入同一私倉的紀錄。",
          "hook": "兵的糧，怎麼進了私倉？",
          "hook_type": "question",
          "conflict": "韓鐸不能讓士兵家屬挨餓，賈勳提議撤護糧線就立刻補發。",
          "turn": "女主讓何靜對回早期重複稅票的轉撥號，證明扣糧不是正常短缺；賈勳須歸還一批仍在關內、已核對的重複扣糧。她將這批實糧按已公開的減配表登記到軍戶與救濟戶，支應第 20–21 日，不付給上級代領。",
          "cliffhanger": {
            "type": "reveal",
            "text": "轉撥文書的私倉代號與首輔祭天籌備帳一致，仍缺實際收糧底單才能連到本人。"
          },
          "setups": [
            "m02"
          ],
          "payoffs": [
            "m02"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "he-jing",
            "jia-xun"
          ],
          "locations": [
            "granary"
          ],
          "theme": "不要把一個人的服從綁在一群人的肚子上。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "女主將有限軍戶口糧直接具名交付，值守家屬不必替統領的選邊受罰。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "何靜把看似兩筆帳的軍糧與重複稅接起來，賈勳無法再稱只是暫時週轉。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 19 日",
            "knowledge": "m02 局部揭示虛假軍糧轉撥，首輔私倉尚缺原始收據的終證。",
            "character_state": "韓只能暫維持原護線，不承諾擴兵；女主同意此限制。賈勳開始怕成為唯一被追究者。",
            "evidence": "轉撥號抄件與第 19 日歸還實糧的驗收表封存公倉；這批實糧按減配表只支應第 20–21 日。",
            "carry_forward": "首輔轉抓葉峻，用個案把救災聯盟寫成劫糧團。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 25,
          "title": "被抓的運糧人",
          "logline": "葉峻因冒用過期牌被捕，女主擋下未經核實的劫糧罪，卻留不住弟弟，自己知情未報的事也被賈勳拿去指她徇私。",
          "hook": "他送的是救命糧，不是假話。",
          "hook_type": "line",
          "conflict": "賈勳把冒牌與劫糧合寫成同一罪，要求葉穗以御命放弟弟，藉此指控徇私。",
          "turn": "女主要求分列行為、封存車單，也當眾說出自己第 8 日就知道牌已過期、只叫他停用而沒有呈報；葉峻承認那是亡父留下的舊牌、是他自己拿去用的。",
          "cliffhanger": {
            "type": "choice",
            "text": "葉穗可立刻用御印帶走弟弟，或讓他留下接受公開核帳；她把印收回衣內。"
          },
          "setups": [
            "m07"
          ],
          "payoffs": [
            "m07"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "ye-jun",
            "jia-xun",
            "he-jing"
          ],
          "locations": [
            "prison"
          ],
          "theme": "保護家人，不等於替他刪掉做過的事。",
          "lead_arc": "suffers",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主將冒牌和劫糧拆成兩項，賈勳不能把未證實的暴力搶糧一起塞進口供。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "葉峻的車單被列入必查資料，受糧戶能作證，不再只有關卡單方面的說法。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 20 日",
            "knowledge": "m07 局部揭示冒用過期牌是真的，仍待證明糧源與去向。",
            "character_state": "葉峻留押，無酷刑；葉穗不能給家人立即自由的安慰。賈勳把她知情未報寫成徇私，呈報朝議；陳情簿上當晚就有街坊撤回簽名。",
            "evidence": "過期牌在葉峻被捕時交出，與車單一併封存問事房，何靜持封件編號；獄中畫面葉峻身上無牌。",
            "carry_forward": "唐敏與沈巧須帶原件證明救災與非法獲利的區別；賈勳的徇私呈報已送進朝議。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 26,
          "title": "親人也不能免帳",
          "logline": "受糧戶與商人完成糧源去向核對，葉峻洗清劫糧罪，但接受冒牌停運與補登處分。",
          "hook": "他沒有搶糧，也不能不認錯。",
          "hook_type": "reversal",
          "conflict": "支持女主的人想讓弟弟全身而退，反對者要求把一切救災都算非法。",
          "turn": "唐敏出示貨源收款、沈巧出示領糧原條；問事結果分列無劫糧與有冒牌。唐敏也帶來自己押車送達的既有預付小單，減配後只夠第 22–23 日，顯示零星到貨仍不等於穩定通路；葉峻補畫繞卡路線。",
          "cliffhanger": {
            "type": "reversal",
            "text": "弟弟免於死罪，女主卻接到朝議傳召：群臣拿著賈勳的徇私呈報，要表決收回她的糧務處置權。"
          },
          "setups": [],
          "payoffs": [
            "m07"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "ye-jun",
            "tang-min",
            "shen-qiao"
          ],
          "locations": [
            "prison"
          ],
          "theme": "公正不會剛好讓所有自己人舒服。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "public_vindication",
              "text": "貨源、車單與受糧三方對上，劫糧栽贓被撤回。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "葉峻接受限期停運與補登義務，女主不必用徇私換弟弟活命，後續可改在粥場工作。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 21 日",
            "knowledge": "m07 完整回收：救災動機、冒牌手段、無劫糧證據與處分都明確。",
            "character_state": "葉峻獲釋但暫不能駕車，轉任施粥登記；姐弟理解彼此的界限。",
            "evidence": "結案抄件交沈巧公開保管；第 25 集封存的過期牌結案後正式收回，不發還葉峻。唐敏第 21 日押回的一批預付糧已驗收，只支應第 22–23 日。",
            "carry_forward": "首輔拿賈勳的徇私呈報與女主介入案件為由召朝議爭奪糧務權。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 27,
          "title": "不是誰的私印",
          "logline": "葉穗在朝議承認救災權需要邊界，提出有限期的公開核帳安排，保住正在運轉的小額糧約。",
          "hook": "要收我的權，先接下這些帳。",
          "hook_type": "line",
          "conflict": "裴定衡拿賈勳的徇私呈報要收回她所有糧務權，卻不願承認與商戶約定的到款日。",
          "turn": "女主先回應徇私呈報：承認第 8 日就知道牌已過期而沒有呈報，請朝議把這筆記在她自己的帳上，葉峻照問事結果受處分，不因她免責；再把未完事項、應付款與受糧數並列，韓只支持維持已公開的護線，何靜要求接管者具名承擔。",
          "cliffhanger": {
            "type": "danger",
            "text": "首輔拒絕接帳，卻留下一道威脅：明日若北倉不放糧，所有延期都由她負責。"
          },
          "setups": [
            "m09"
          ],
          "payoffs": [
            "m09"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "pei-dingheng",
            "han-duo",
            "he-jing"
          ],
          "locations": [
            "hall"
          ],
          "theme": "要權力的人也要接下責任。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "villain_humbled",
              "text": "女主要求接管者簽清單，首輔無法只取權不接逾期責任。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "韓鐸支持的是既定護路與付款公約，軍商合作第一次不完全依賴女主個人身分。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 22 日",
            "knowledge": "m09 局部回收有期限、可接管的合約能暫保商路，仍須度過封倉。",
            "character_state": "女主學會把自己的權也寫成條款，韓公開支持有限事項。",
            "evidence": "未完帳與具名接管欄在殿內公開抄錄。",
            "carry_forward": "蕭承越以北倉立即卸糧為誘因，提出更私人也更殘酷的條件。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 28,
          "title": "一場婚姻，一顆人頭",
          "logline": "蕭承越屏退旁人，提議以婚姻替她的假身世補合法性，條件是處死葉峻並追認北倉舊款。",
          "hook": "留妳做皇后，拿弟弟來換。",
          "hook_type": "danger",
          "conflict": "交易可讓糧車立即卸貨、她繼續掌事，但必須犧牲已證明無劫糧的弟弟。",
          "turn": "葉穗指出這不是救災條件而是逼她替偽證背書，拒簽；她請唐敏入殿見證，蕭承越收起身世的話，只把婚約與排他糧契擺上桌；唐敏把本日剛驗收的另一批預付小單與排他糧契並排，證明零星商路已減配撐出第 24–26 日口糧，但不能代替後續穩定護運；她見證條款，確定小商戶也會被永遠綁住。",
          "cliffhanger": {
            "type": "choice",
            "text": "蕭承越收起糧契，給她一天改口；女主留下空白婚約副本，選擇向民眾交代真正的困境。"
          },
          "setups": [
            "m08"
          ],
          "payoffs": [
            "m08"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "xiao-chengyue",
            "tang-min"
          ],
          "locations": [
            "hall"
          ],
          "theme": "不用另一個人的命替自己補資格。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主直接拒絕把已釐清的無劫糧案改判死罪，保住自己制定的規則。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "唐敏親見排他糧契與婚約綁在一起，答應把條件原文交同行判斷，而非替女主說情。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 23 日",
            "knowledge": "m08 局部揭示聯姻、殺弟、追認北倉舊款是同一交易，尚缺祭天前共同簽約原件；蕭承越只在屏退旁人時對葉穗提身世，唐敏在場時只見到婚約、殺弟條件與糧契，不知道身世是假的。",
            "character_state": "女主失去最快的供糧捷徑，唐敏承擔向同行說真話的風險；第 23 日驗收的預付糧只夠減配到第 26 日，且唐敏本人押運不可長期複製。",
            "evidence": "無簽名婚約副本與見證筆錄分藏唐敏、何靜處。",
            "carry_forward": "女主計畫公開困境，首輔也在準備祭天揭露身世。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 29,
          "title": "留給她的最後一頁",
          "logline": "首輔把真實收養副本夾入祭天罪詔的附件，女主從送達簿得知，轉而準備公開自己的完整知情時間。",
          "hook": "他要說真話，用來殺我。",
          "hook_type": "reversal",
          "conflict": "養母提議先逃，沈巧要求女主不能只公佈對自己有利的部分；葉穗怕坦白立刻斷糧。",
          "turn": "她把得知真相的日期（第 14 日聽到、第 15 日確證）、此前簽過的糧約、尚未完成的承諾，連同自己當庫房女吏時挪過一天粟額、已用薪錢補足的舊事一併寫下；羅杏同意以本名當眾作證。",
          "cliffhanger": {
            "type": "emotion",
            "text": "羅杏替她取下過重冠冕，葉穗第一次讓母親在不說「陛下」的情況下抱住自己。"
          },
          "setups": [
            "m10"
          ],
          "payoffs": [
            "m10"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "luo-xing",
            "shen-qiao",
            "he-jing"
          ],
          "locations": [
            "records",
            "clinic"
          ],
          "theme": "坦白的代價不能只由聽見真相的人承受。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "first_clear",
              "text": "何靜從已建立的送達簿發現祭天附件，首輔無法再壟斷揭露時機。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "女主把自己的延遲坦白也列在聲明裡，沈巧同意幫忙召集能提出反對的人。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 24 日",
            "knowledge": "m10 局部回收公開不是求原諒，必須讓他人重新選擇是否授權。",
            "character_state": "母女開始修復，女主不再用冠冕阻隔恐懼。",
            "evidence": "含知情時間的聲明由何靜留副本，沈巧持未完救災清單。",
            "carry_forward": "次集在群眾能聽見且可抄錄的場合提前承認假身世。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 30,
          "title": "朕有話要說",
          "logline": "葉穗提前向全城承認假血統，交出查證檔案與自己的知情責任，請大家把救災與是否留她分開決定。",
          "hook": "我不是皇族。",
          "hook_type": "line",
          "conflict": "首輔趕來要把聲明改成自請處死，沈巧不允許把全部已運作的粥場拿來陪葬。",
          "turn": "女主交出血統證據，羅杏站到桌前，以本名說出自己被迫按印的經過；葉穗聲明自己無權要求無條件服從，只請把已承諾的發糧完成；現場有支持也有背身離開的人。",
          "cliffhanger": {
            "type": "reveal",
            "text": "首輔亮出已簽發的停糧令，女主的坦白當晚就讓所有盟友必須重新選邊。"
          },
          "setups": [
            "m10"
          ],
          "payoffs": [
            "m10"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "pei-dingheng",
            "shen-qiao",
            "luo-xing"
          ],
          "locations": [
            "relief"
          ],
          "theme": "說出真相之後，別人才真正有選擇。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主搶先拿走首輔的獨家揭露，把假身世從黑函變成人人可查的檔案。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "她公佈救災出入帳，沈巧證實已到的糧是真的，普通人的成果不被假血統一筆抹消。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 25 日",
            "knowledge": "全城得知 m05 真相，以及女主自第 14 日起知情、延遲到今天才說；m10 局部回收坦白只是新授權的起點。",
            "character_state": "女主失去身分保護，部分群眾撤回信任，盟友尚未作最後選擇；羅杏當眾作證後，母女一起承擔公開的後果。",
            "evidence": "羅杏當眾出示收養簿正本，與族譜對照供人抄寫，之後交給共管封存；停糧令仍須核查送達與權限。",
            "carry_forward": "不能直接接歡呼擁立；第 31 集必須呈現分裂、撤約與剩下的救災選擇。"
          },
          "timeline": "present",
          "closed_ending": false
        }
      ]
    },
    {
      "number": 4,
      "title": "先看帳，再叫萬歲",
      "theme": "真正的支持允許提問，真正的權力承擔限制。",
      "start_state": "假身世公開、停糧令抵達，女主被質疑；小商路與現場收條仍是真實成果。",
      "end_state": "首輔被依法控制，北倉壟斷瓦解；數月後各方議約擁立葉穗，她以本名宣誓，接受持續核帳。",
      "turn": "祭天的代罪臺變成共同驗證責任的公開桌，女主不再靠別人安排的身分留在位置上。",
      "stakes": "能否在不犧牲無辜者、不偽造新血統的情況下重建供糧與政務。",
      "question": "眾人如何支持她，又如何保留攔住她的權利？",
      "episodes": [
        {
          "number": 31,
          "title": "有人留下，有人轉身",
          "logline": "部分商戶退約、百姓要求女主離開，葉穗先兌現退款與口糧清單，才提出限期共管救災。",
          "hook": "不信我，也先把糧領回去。",
          "hook_type": "line",
          "conflict": "唐敏無法替所有同行保證，沈巧要求在沒有合法君主的爭議下由各方共同掌管存糧。",
          "turn": "女主交出單獨批款權，何靜列出三方共同簽收方式；她仍能安排糧務，但不能再一人用印。",
          "cliffhanger": {
            "type": "danger",
            "text": "第 23 日到貨減配後只剩本日一日量，共管清單上還缺禁軍連續護路的簽名。"
          },
          "setups": [
            "m09",
            "m10"
          ],
          "payoffs": [
            "m09",
            "m10"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "tang-min",
            "shen-qiao",
            "he-jing"
          ],
          "locations": [
            "granary"
          ],
          "theme": "不以飯碗換表態。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "女主按原清單發糧，連當面反對她的人也沒有被扣份額。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "她交出單獨批款權，唐敏與沈巧才在限期共管單上簽名，真實的新授權開始形成。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 26 日",
            "knowledge": "m10 局部確定血統倒塌不代表糧務全無人管，但支持是有條件的；m09 局部回收：身世公開後，退款與口糧照公開清單兌現，唐敏在限期共管單上簽名，留下的商戶沒有跟著退約；尚缺禁軍連續護路。",
            "character_state": "女主接受部分商戶退出，不能把留下者稱為天下歸心。",
            "evidence": "退約與退款按可用現款分列，共管單三方各存一份。",
            "carry_forward": "韓鐸必須表明守護的是具體糧路與共同條款。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 32,
          "title": "刀守的是哪條路",
          "logline": "韓鐸拒絕用禁軍驅散領糧百姓，簽下有限護運條款，替代糧路終於送來足以解除一日倒數的新糧。",
          "hook": "我的刀守糧路，不守謊話。",
          "hook_type": "line",
          "conflict": "賈勳要求禁軍執行停糧，聲稱葉穗身分一倒所有命令都作廢。",
          "turn": "韓依自身護城職責與軍戶共同見證的護運約維持通道，並讓女主承認兵不能用來逼商戶供糧；唐敏的分批小車穿過南糧關。",
          "cliffhanger": {
            "type": "reversal",
            "text": "北倉不再是唯一入口，賈勳第一次問：「若我交出底冊，能不能按我做過的事算罪？」"
          },
          "setups": [],
          "payoffs": [
            "m09"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "tang-min",
            "jia-xun"
          ],
          "locations": [
            "gate"
          ],
          "theme": "合作的力量來自彼此都不能為所欲為。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "韓拒絕驅散領糧者，女主同時接受不得強徵商戶，現場避開軍民衝突。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "first_clear",
              "text": "多家小車按已付款與公開通行條件抵達，打破北倉封供就能餓住全城的控制。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 27 日",
            "knowledge": "m09 完整回收：替代糧路靠分批信用、付費、限權護運共同成立，仍不是永久糧源無憂。",
            "character_state": "韓公開與首輔的非法停糧要求切割，唐敏履約但耗掉本季信用額。",
            "evidence": "護運條款與抵達車單可公開查，賈勳仍保有私藏底冊。",
            "carry_forward": "有了可維持數日的糧，眾人能坐下核帳，不必靠立即承諾赦免換證據。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 33,
          "title": "三張桌拼成一本帳",
          "logline": "商人運單、街坊原條與官府底冊公開並列，假借據的全流程被查清，賈勳不能用交證換全身而退。",
          "hook": "三本帳，今天放一張桌上。",
          "hook_type": "image",
          "conflict": "每一方都怕交原件後遭修改，賈勳索求全面赦免才願交底冊。",
          "turn": "女主同意先封件、共同拆封、各存抄本，只承諾按行為分責不私刑；何靜用先前角缺與車號接上完整鏈。",
          "cliffhanger": {
            "type": "reveal",
            "text": "底冊最後一頁有首輔令轉私倉的領糧號，也有明日調走護路兵的公文號。"
          },
          "setups": [],
          "payoffs": [
            "m04"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "he-jing",
            "tang-min",
            "jia-xun"
          ],
          "locations": [
            "granary"
          ],
          "theme": "信任不是把證據交給一個好人保管。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "public_vindication",
              "text": "唐敏運單與沈巧事先封存的原條對上，已被誣欠糧的街坊列名恢復清白。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "賈勳接受沒有全赦保證的共同封件，底冊從私下保命工具變成可供各方核查的證據。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 28 日",
            "knowledge": "m04 完整回收雙收改借流程；m02 還須核對私倉實際收糧印才能歸責首輔。",
            "character_state": "何靜也被列入按行為調查，不因提供證據免責；賈勳暫受限制不得離城。",
            "evidence": "原件分封保管，三方簽頁與抄本在公倉公開桌。沈巧已簽名的原條盒在場，本人本集不出場說話。",
            "carry_forward": "次集查調兵公文，防止證據尚未完成就被斷掉護路。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 34,
          "title": "午間送到的調兵令",
          "logline": "首輔假傳調兵令，女主靠早已保存的送達回執發現新令重複用了舊送達號，韓鐸因此能有據拒令；首輔隨即讓內廷帶走何靜，把祭天提前。",
          "hook": "這個送達號，早就用過一次。",
          "hook_type": "reversal",
          "conflict": "調兵令印鑑齊全，韓若直接拒絕就可能被指兵變；女主也不能只憑猜疑命他不動。",
          "turn": "何靜把第 8 集起保存的回執與新令並排：新令的送達號，第 4 日就用在賈勳簽收的那道分糧命令上，一個號不可能發給兩道命令；韓要求首輔親自覆核再執行。",
          "cliffhanger": {
            "type": "danger",
            "text": "假令失敗，首輔改把祭天提前到明日辰時，又以私帶宮中回執出文簿房為由，讓內廷把何靜帶去問話；核完私倉帳只剩一夜，最會算帳的人卻不在桌邊。"
          },
          "setups": [],
          "payoffs": [
            "m03"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "he-jing",
            "pei-dingheng"
          ],
          "locations": [
            "records",
            "hall"
          ],
          "theme": "曾經看似笨重的留檔，會在危急時替人擋刀。",
          "lead_arc": "suffers",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主不搶著宣佈偽令，先請何靜拿出第 4 日的簽收回執，與新令上同一個送達號並排比對。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "韓有明確文書矛盾可依，拒絕把護路兵調走不再只是一句效忠女主。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 29 日午間",
            "knowledge": "m03 完整回收：封鎖、共用副印與偽令都來自同一被控制的公文鏈；假調兵令重複用了第 4 日已簽收的送達號。",
            "character_state": "韓保住護線，但無權干涉內廷問話；首輔放棄文書包裝，改用祭天速度逼局。何靜被帶走，第 11 集起每日公開的進度簿記著她的去向，她無法無聲失蹤，今夜卻不在葉穗身邊。",
            "evidence": "何靜被帶走前，已把第 4 日簽收回執與重複用號的假調兵令在殿內公開封存；首輔收到覆核要求。",
            "carry_forward": "祭天原定第 30 日午時改成辰時，倒數縮短數小時而非憑空改成另一日；葉穗得在沒有何靜的一夜裡自己對完北倉附約與底冊。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 35,
          "title": "同一張約，兩個主人",
          "logline": "女主把北倉附約與賈勳交出的底冊交叉對照，逼蕭承越面對一張原本保護他、現在會被用來代罪的共同草約。",
          "hook": "首輔要你的糧，也要你的命。",
          "hook_type": "reversal",
          "conflict": "蕭承越仍想維持與首輔的接位安排，唐敏證明他的排他糧路已失效，首輔則試圖推卸侵吞款。",
          "turn": "何靜不在，葉穗與唐敏自己逐行對照；首輔與蕭承越各亮出自己保留的附件反駁對方，最終證明他們早在葉穗登基前就約定祭天後換君；女主不許任何人以倒戈免責。",
          "cliffhanger": {
            "type": "choice",
            "text": "蕭承越失去壟斷，選擇交出帶私倉印的原始糧契保留抗辯權，或繼續替首輔守最後一扇門。"
          },
          "setups": [],
          "payoffs": [
            "m08"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "xiao-chengyue",
            "pei-dingheng",
            "tang-min"
          ],
          "locations": [
            "hall"
          ],
          "theme": "一起得利的人，也可能一起害怕分帳。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "villain_humbled",
              "text": "葉穗出示替代商路已到貨的實單，蕭承越不能再用一句斷糧讓所有人閉嘴。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "首輔與皇族為互推責任亮出各自附件，登基前就安排換君的共謀由二人的原件互證。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 29 日夜間",
            "knowledge": "m08 完整揭曉真皇族參與代罪與繼位交易；他受支持的實物優勢已被替代但血統仍真。",
            "character_state": "兩名反派決裂，蕭仍須調查，沒有洗白；女主接受交證但不私下許赦；何靜仍在內廷問話。",
            "evidence": "共謀草約已封存；蕭承越掌握最後能比對首輔私倉印的糧契。",
            "carry_forward": "蕭選擇交出原件，次集在祭臺完成三套帳與實糧印的公開核對；唐敏與沈巧以共管簽名人的身分，依每日進度簿連夜行文內廷，要求辰時祭天前交回何靜。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 36,
          "title": "祭天臺上的核帳桌",
          "logline": "女主把本來要宣讀罪詔的祭臺改成核帳桌，讓偏秤、雙稅、假軍糧和首輔私倉接成完整責任鏈。",
          "hook": "祭天之前，先把帳對完。",
          "hook_type": "line",
          "conflict": "首輔堅持先處理冒充皇族、僭位之罪，再談糧款；女主若只自辯就落入已設好的祭文。",
          "turn": "她先承認身世已公開；內廷問不出罪名，何靜依共管行文在辰時前被放回祭臺，逐筆核對賈勳底冊、民間單據，以及蕭承越前一夜交出、已封存送到祭臺的帶私倉印糧契；缺糧並非天譴而是人為轉走。",
          "cliffhanger": {
            "type": "reveal",
            "text": "最後一枚印不只證明首輔收糧，也對上他以「祭天備用」名義支走禁軍糧的親簽。"
          },
          "setups": [],
          "payoffs": [
            "m02"
          ],
          "tension": [
            5,
            3,
            5,
            4,
            5
          ],
          "characters": [
            "ye-sui",
            "pei-dingheng",
            "he-jing",
            "jia-xun"
          ],
          "locations": [
            "altar"
          ],
          "theme": "把天意的說辭還原成一筆筆人的選擇。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主先放上自己的身世聲明，讓首輔無法以重複揭露阻止糧務核帳。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "偏秤、重複票、虛轉軍糧與首輔私倉領據完整接上，百姓挨餓不再被歸咎於新君失德。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 30 日辰時",
            "knowledge": "m02 完整回收侵吞方法、去向與首輔直接責任；沒有以一聲認罪代替證據。",
            "character_state": "何靜承認自己參與抄帳的範圍，賈勳不能把所有罪推回首輔。",
            "evidence": "校砣、三套帳與帶私倉印的糧契原件在同一核帳桌，抄件已散交各方。",
            "carry_forward": "證據成立後仍須真正解除首輔兵權，不能以觀眾震驚替代控制現場。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 37,
          "title": "交出那枚調兵印",
          "logline": "韓鐸依公開證據與共同見證控制首輔，葉穗拒絕當場處死，把處罰與追回糧款留下正式程序。",
          "hook": "今天不再拿一個人祭天。",
          "hook_type": "line",
          "conflict": "首輔要殘存親隨強行帶走帳冊，蕭承越則想以交證換當場宣佈自己繼位。",
          "turn": "韓先撤走接觸帳冊的武器人手，再封調兵印；女主把對首輔、皇族、執行官的責任分列，交共管者見證。",
          "cliffhanger": {
            "type": "reversal",
            "text": "祭臺上原本給葉穗戴的罪枷被收進證物箱；她留在桌前，先簽下自己必須接受的知情審查。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            5,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "han-duo",
            "pei-dingheng",
            "xiao-chengyue"
          ],
          "locations": [
            "altar"
          ],
          "theme": "勝利不是把同一套代罪方式換一個人用。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "betrayer_punished",
              "text": "韓依據已公開的違令與侵吞證據解除首輔兵權，將人帶入看守而非讓他帶印離場。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "女主拒絕當場處死與私下赦免，連自己延遲坦白的責任也列入審查，使反派無法以報復論抹平證據。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 30 日午後",
            "knowledge": "主謀已受控制，民眾知道剩下的是分責、追款與如何治理，沒有新幕後黑手。",
            "character_state": "首輔拘押、蕭待核帳，韓維持秩序；葉穗仍是限期救災主持而非已正式獲擁立。",
            "evidence": "調兵印、罪枷、祭天罪詔與附件（含首輔手上的收養副本）與原始帳冊列入公開保管清單，多方簽封。",
            "carry_forward": "次集設立可持續核帳與命令留檔，讓權限不再取決於一個人聲望。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 38,
          "title": "讓下一道命令也能被問",
          "logline": "女主與糧吏、商戶、街坊訂立限期政務條款，同意自己的任命、支款與指令都留公開副本；知情審查給她記下一過，北面兩州也退回了邀請。",
          "hook": "我的命令，也要留下副本。",
          "hook_type": "line",
          "conflict": "糧路恢復不能立刻補足所有欠款，女主若以救災有功要求免問責就會重演首輔。",
          "turn": "她接受每旬公開核糧、爭議款暫停、商戶按期退出等限制，並向五供糧州邀請依當地公議推派的代表協商後續政務。共管會議否決了她想先還小商戶的順序；知情審查把她延遲坦白記過一次，抄進公開糧簿；向來經北倉出糧的北面兩州，以她沒有血統又剛被記過為由，把邀請原封退回。",
          "cliffhanger": {
            "type": "emotion",
            "text": "沈巧在共管條款下簽名，沒有跪下：「我願意看妳再做一段，也會繼續問。」"
          },
          "setups": [
            "m10"
          ],
          "payoffs": [
            "m10"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "he-jing",
            "tang-min",
            "shen-qiao"
          ],
          "locations": [
            "hall",
            "granary"
          ],
          "theme": "支持一個人，也要留下制止她的方法。",
          "lead_arc": "suffers",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "first_clear",
              "text": "第一份新規要求女主支款也留可查副本，昔日限制平民的格式開始限制掌權者。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "被偽造債務的戶名逐批更正，唐敏依表收到下一期款，制度承諾當集有實際交付。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 31–40 日，以日期牌明示時間推進",
            "knowledge": "m10 局部回收限期救災授權如何延續；北面兩州退回邀請，正式擁立尚待各州協商與後續成果。",
            "character_state": "葉穗不能單獨更改糧款順序，延遲坦白的記過公開在糧簿上；何靜接受定期交叉核帳；民眾意見仍可不同。",
            "evidence": "公開糧簿、任命抄件與命令回執開始定期存檔，邀請各州的文書留送達紀錄，北面兩州的退件也一併入檔。",
            "carry_forward": "數月後才看協商與供應是否站得住；退回邀請的北面兩州要靠實際成果說服，不用蒙太奇假稱災害全消失。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 39,
          "title": "第一批新糧",
          "logline": "數月後首批回耕新糧入倉，眾人看到不完整但可持續的恢復，女主也接到各方正式議約的回覆。",
          "hook": "這次的滿倉，終於不是墨水。",
          "hook_type": "image",
          "conflict": "收成只夠改善一部分供應，沈巧不讓慶功把仍需救濟的戶名塗掉；葉穗還須交代案件結果。",
          "turn": "新糧以第 4 集校砣驗收，葉峻完成停運與補登處分後恢復合法運糧；公開的案件摘要交代首輔案完成初步裁斷、追款仍在執行。",
          "cliffhanger": {
            "type": "reveal",
            "text": "五州代表帶回附有糧政與問責條款的擁立議約，支持的名字後面都有女主必須接受的限制。"
          },
          "setups": [
            "m10"
          ],
          "payoffs": [
            "m10"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            4
          ],
          "characters": [
            "ye-sui",
            "ye-jun",
            "shen-qiao",
            "luo-xing"
          ],
          "locations": [
            "field",
            "granary"
          ],
          "theme": "收成不是忘記曾經挨餓的人。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "first_clear",
              "text": "女主用同一枚校砣驗收真實新糧，早先只能點半垛袋子的困局有可見改善。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "葉峻依法完成處分領回新運糧牌；羅杏的脅迫證詞獲確認，母子不靠女主私赦恢復生活。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 120 日，明示三個月後",
            "knowledge": "m10 局部回收其他供糧州的同意是經代表協商與救災成果取得；第 38 集退回邀請的北面兩州，看過數月的公開糧簿與南路到貨後也派出代表；國家仍有困難。",
            "character_state": "葉峻掛全新有日期的合法木牌；母女信任恢復。首輔侵吞罪責成立並被拘押，追款續辦；蕭依和解中的財務條款退款、公開放棄該次繼位主張，未被封為救國英雄。",
            "evidence": "新糧驗收表、各州具名議約與案件公開摘要入檔，不口頭宣告所有債都已還清。",
            "carry_forward": "第 40 集只完成公開接受條款與本名宣誓，所有主線都已交代，不加下一季危機。"
          },
          "timeline": "present",
          "closed_ending": false
        },
        {
          "number": 40,
          "title": "先看帳，再叫萬歲",
          "logline": "葉穗在已協商完成的擁立儀式上以本名宣誓，把糧帳放在自己與民眾之間，接受第一個公開追問。",
          "hook": "這次，我用自己的名字簽。",
          "hook_type": "line",
          "conflict": "舊儀式仍準備讓人先跪拜，沈巧要確認承諾的發問權不會在冠冕戴回後消失。",
          "turn": "葉穗先逐項確認議約、簽本名，再請沈巧當場問新糧去向，何靜按簿回答，韓鐸在旁見證軍令也受留檔。",
          "cliffhanger": {
            "type": "reversal",
            "text": "沈巧沒有被要求閉嘴，葉穗把公開帳冊推到桌中央：「先看帳，再叫萬歲。」她與眾人一起低頭看糧，桌上擺著早已校準的秤砣與她簽下本名的議約。"
          },
          "setups": [],
          "payoffs": [
            "m10"
          ],
          "tension": [
            4,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "ye-sui",
            "shen-qiao",
            "he-jing",
            "han-duo"
          ],
          "locations": [
            "hall"
          ],
          "theme": "被擁立不是再也不必回答，而是終於願意一直回答。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主先簽附有權限限制的議約再戴冠冕，首集被代簽身分的人終於自願承擔責任。",
              "planned_seconds": 24
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "沈巧在正式儀式上成功追問、何靜當場翻帳回答，平民發問權不只寫在結尾字幕裡。",
              "planned_seconds": 124
            }
          ],
          "state": {
            "time": "第 121 日",
            "knowledge": "m10 完整回收：限期合作、實際成果、各州同意與公開限制共同成立正式擁立；不靠隱藏血統。",
            "character_state": "女主保住位置並接受持續問責；韓支持有界限的政務，沈巧仍可反對。所有反派、家人與盟友去向已交代。",
            "evidence": "本名議約、糧帳與送達回執公開留檔；秤砣回到公倉使用，不藏成皇室戰利品。",
            "carry_forward": "閉合結局，最後畫面完成身分與糧務回收，不留下新的威脅、神秘人物或待解罪案。"
          },
          "timeline": "present",
          "closed_ending": true
        }
      ]
    }
  ],
  "packaging": {
    "titles": [
      "他們扶我做女帝，只等三十天一到，就讓我替全城陪葬",
      "登基第一天，我撤掉自己的御膳，把災民的粥推到首輔面前",
      "庫房女吏被推上皇位，反手把首輔逼上了核帳桌"
    ],
    "description": "一名庫房女吏被扶上皇位，卻只剩三十天可活。她從一碗災民粥開始，追查空倉、假借據與被扣軍糧，也一步步查到扶她上位的人真正的打算。原創女帝權謀漫劇，適合喜歡真本事反擊、伏筆回收與完整結局的觀眾。全篇四十集合集，目標約兩小時；實際片長與章節時間待成片確認。",
    "tags": [
      "漫劇",
      "AI漫劇",
      "一口氣看完",
      "原創故事",
      "女帝崛起",
      "女主權謀",
      "糧政",
      "逆襲",
      "完整結局",
      "朕不是你們的替死鬼"
    ],
    "thumbnail_variants": [
      {
        "id": "A",
        "headline": "誰替誰死",
        "composition": "左側葉穗戴冠冕但目光直視觀眾；右側首輔袖下露出祭天日期，前景一碗含沙稀粥。大字不遮臉，冷綠與暖灰碗面對比。",
        "episode": 1,
        "scene": "首集冠冕、祭天簿日期與御桌稀粥均實際出現；縮圖可合成同場關鍵影格，不製造流血處刑。",
        "promise": "前三十秒呈現新君被安排與粥的反擊，第十集確證替死計畫。"
      },
      {
        "id": "B",
        "headline": "我喝了，換你",
        "composition": "女主把自己喝過一口的粗陶碗推向首輔，首輔一手按著糧額單、筷子擱在箸架上沒動，與女主席前未撤完的金盤形成對比。以碗為中間視覺焦點，臉部反應清楚。",
        "episode": 1,
        "scene": "登基宴上女主撤掉自己的御膳、先喝一口，再把同一碗災民粥推到首輔面前的實際場面。",
        "promise": "首集就兌現讓掌權者面對百姓正在吃的食物，不讓標題只停在旁白。"
      },
      {
        "id": "C",
        "headline": "滿帳空倉",
        "composition": "女主手持有入倉記號的帳頁，身後打開的倉門內只有半垛麻袋；賈勳的手擋住簽收欄。用空間落差表現帳物不符。",
        "episode": 3,
        "scene": "第三集實點麻袋、拒簽足額收訖的場景，不提前畫最後祭臺。",
        "promise": "第三集第一次用糧務能力拆帳，後續發展為完整公開核帳。"
      }
    ],
    "audience": "華語成年觀眾；喜歡女主逆襲、制度內的具體博弈、家人與同伴關係，不需要戀愛或全知外掛。",
    "visual_identity": "葉穗固定深青窄金邊朝袍、稻葉銅簪與數糧繩；首輔黑石扳指、賈勳腰間黃銅關鑰束、韓的舊護腕、唐敏鐵鑰匙圈與缺口量斗保持一致。群體場面以四名以內具臺詞角色加無臺詞背景演出，不靠無限新增大殿。早期冠冕遮住女主視線，結尾先簽約後戴冠，以鏡位完成回收。",
    "music": "開場細鼓與低弦，碗推到首輔面前短暫停樂；核帳場面保留紙張、算珠與秤砣聲，避免全程高音。第 20、29 集以低密度弦樂和室內聲襯托母女對話。第 36 集逐項對帳才累加節奏；第 40 集讓最後問答清楚落下再進收尾旋律。配樂為原創或授權素材的製作方向，尚未生成或取得。",
    "release_order": 4,
    "pinned_comment": "如果你是唐敏，女主連下一期車工都付不出來時，你會在什麼條件下繼續把糧交給她？"
  },
  "continuity_notes": [
    "主要順序與核定四十集一致：第 10 集代罪計畫、第 20 集假血統、第 30 集公開坦白、第 36 集核帳、第 40 集正式擁立。新增角色只承接原計畫中的商人、糧吏、皇族與街坊職能，不改主要角色或結局。",
    "首集只有觀眾看見祭天日期與被印盒遮住的姓名，女主未讀到祭天簿，開場先追問城外糧食；第10集才取得確指自己、追認舊帳及處死的完整文書。開頭剪輯不可提前讓她說出死期。第 3 集集尾的畫面可疊回首集祭天簿的版式，讓觀眾對照出兩者格式相同；這是分鏡說明，不是臺詞，她沒看過祭天簿。第 7 集羅杏看見的承責字樣，就是第 3 集那張她沒簽、由她留存的足額收訖，不是另一份文書。",
    "首集那碗粥只有一個版本：何靜只端進一碗南市災民的粥；女主撤的是自己的御膳，其他席面不動；她先喝一口，再把同一碗推到首輔面前，首輔不動筷，全集沒有任何人被迫吃下。premise、開場三十秒、第 1 集各欄、標題 B 與縮圖 B 都以此為準。首輔「明日那一萬碗」的質問只在開場 24–30 秒出現一次，集尾改以他當眾記下何靜的名字收尾。",
    "三十日的算法：登基當天算第 1 日，祭天定在第 30 日；premise、開場、臺詞與包裝說的「三十天」「三十日」「第三十日」都指第 30 日這一天，不是第 31 日。第 34 集提前的是第 30 日當天祭天時刻，從午時改到辰時，不把原倒數偷改成二十九日。第 38–40 集以明確日期交代數月恢復與擁立。",
    "女主只懂糧務與帳目，不自行帶兵、治病、判讀所有法律。何靜可糾正她；韓負責現場軍事判斷；羅杏負責病患轉送；唐敏能拒絕不合理商約。",
    "第 3 集帳物不符、第 4 集偏秤、第 9 集雙收、第 14 集假借據、第 24 集軍糧虛轉、第 36 集私倉親簽，構成分段可見的證據鏈。每次局部 payoff 都只完成當集能證明的一段。",
    "紙張新不能單獨證明血統假。第 20 集必須同時核對皇族失蹤日期、真實收養簿、被迫按印證詞與紙批，不讓女主一眼看出一切。",
    "韓的妹妹在第 18 集安全轉診，之後不再突然失蹤製造同一勒索；她留下的藥單副印紀錄繼續存在。韓支持女主是有限合作，不是救妹之後終身無條件效忠。",
    "運糧木牌是逐集道具，不寫進葉峻的固定外觀提示詞，生圖時依下列狀態另行指定：第 7 集舊牌用繩掛在胸前；第 13 集被沈巧看出過期後收進衣內，第 22 集不外露；第 25 集被捕時交出，連同車單封存問事房，第 25、26 集獄中畫面身上無牌；第 26 集結案後過期牌正式收回、受限期停運，之後留在粥場工作，不能又把木牌掛回胸前；第 39 集完成處分才戴全新的合法木牌，新舊兩個牌的顏色與刻日期必須不同。過期牌是葉峻亡父生前的運糧牌。葉穗第 13 集（第 8 日）起知道牌已過期，要他停用、只憑唐敏的新運單跑車，但沒有呈報；第 25 集她當眾說出這段知情，冒牌處分只針對葉峻此前的使用。",
    "韓芮只在第 18 集出場；右腕的淡拘束痕是偏院拘禁留下的，該集從頭到尾都在，已寫進固定外觀提示詞，不需另加集數說明。",
    "冠冕是逐集道具，不寫進葉穗的固定外觀提示詞，生圖時依下列狀態另行指定：第 1 集登基宴上戴上；第 1–29 集以新君身分出場時都戴著，宮內宮外相同；第 29 集集尾由羅杏取下；第 30–39 集不戴；第 40 集簽完本名議約後才戴回。全劇是同一頂偏重的冠冕，可以取下，不和頭髮畫成一體。第 2–28 集各集欄位沒有逐集寫到冠冕，寫定成都戴是創作補完：第 29 集她到文簿房與醫舍時仍戴著，集尾才取下。",
    "第 33 集沈巧原條盒已提前簽封在場，本人不另加臺詞；所有具臺詞角色均登記。祭天、朝議與運糧群像用無臺詞背景反應，不臨時新增會揭關鍵答案的官員。",
    "第 31 集接受的只是糧務共管，第 38 集才啟動正式議約，第 39 集經數月與各州代表交涉有回覆，第 40 集正式擁立。百姓因真實成果與可撤換的條款支持，不因她說真話就集體跪服。",
    "首輔被拘押並調查，蕭承越交證仍需退款與退出繼位交易，賈勳、何靜按行為分責；不以反派倒戈或盟友立功清空法律後果。劇本須把結果作案件摘要呈現，非主角當場獨斷所有刑度。",
    "地理與路線：衡京在大河北岸。南面三州與東公倉（城外東南河岸）的糧，大車都要過城南窄橋上的南糧關才能進城，小車可繞渡口小道；北面兩州的糧經城北郊的北倉、由北門進城，不經南糧關，所以第 21 集北倉車隊是從北門直接開到南市施粥場。唐家車棧在南糧關橋外，施粥場在南城門內，北偏院在城北。五供糧州第 6 集由唐敏的南路貨源帶出、第 11 集在祭天準備簿的糧路圖上完整出現，第 38 集才發出邀請。",
    "公開前誰知道假身世（第 30 集、第 25 日公開）：裴定衡是造假的人；蕭承越在登基前簽繼位草約時就由首輔告知；羅杏被迫按印。葉穗第 14 日（第 19 集）聽到羅杏承認、第 15 日夜（第 20 集）三方日期確證，她的知情一律從第 14 日起算，延遲坦白的期間是第 14–25 日；何靜第 15 日在場確證；沈巧第 24 日（第 29 集）由葉穗親口告知。葉峻、韓鐸、唐敏、賈勳都是第 25 日公開時才知道；第 28 集（第 23 日）蕭承越只在屏退旁人時對葉穗提身世，唐敏入殿後他沒有說破。",
    "第 10 集她沒有簽追認：當面拒簽會讓首輔提前收網，她只說帳沒對完、追認留到祭天前一併簽，首輔接受，因為他本來就要她在祭天前簽。全劇她沒有簽過首詔或追認文書；她親手簽下的第一份承責文件是第 37 集的知情審查，第 40 集簽本名議約。",
    "收養簿的持有：正本原藏羅杏醫舍的藥書夾層；第 19 集羅杏先交給葉穗讀，首輔只帶走羅杏預先抄下的具名副本；第 20 集核完後正本由羅杏收回封存，何靜另持一份騎縫抄本；第 29 集首輔把他手上的副本夾進祭天罪詔附件；第 30 集羅杏當眾出示正本供人抄寫，第 31 集共管成立後交共管封存；首輔的副本隨罪詔附件在第 37 集列入公開保管清單。",
    "主角受挫的集數與承接：第 9 集唐敏三車糧被扣（第 10 集首輔拿它逼簽、第 11 集粥場減半、第 12 集撤欄才放行，晚到一天）；第 19 集首輔拿到收養副本（第 20 集承接，第 29 集他把副本夾進罪詔附件）；第 25 集弟弟留押、賈勳以徇私呈報朝議（第 26 集朝議傳召、第 27 集朝議）；第 34 集何靜被內廷帶走、祭天提前（第 35 集葉穗與唐敏自己對帳，唐敏與沈巧連夜行文，第 36 集辰時前放回）；第 38 集記過與北面兩州退件（第 39 集兩州經數月後派代表）。首輔第 1 集記下何靜的名字，第 34 集才真正對她下手；第 11 集起的每日公開進度讓她無法無聲失蹤。",
    "呈現界線：祭天處死只以祭天簿上的日期與罪詔文字呈現，罪枷只當證物入鏡，不拍刑具加身；葉峻留押無刑求，問事房不拍體罰；韓芮的腕痕是淡痕，不拍拘束過程；饑民以排隊、空碗、灰棚呈現，不拍瘦骨或病況特寫；洪災死者只在臺詞與帳上交代。",
    "第 40 集保留高情感張力，使用 reversal 回收首集被安排的簽名：首集她拒簽別人備好的首詔，末集自願簽下本名。御膳與那碗粥只屬於首集，第 40 集不重演。最後不出現遠方來信、神秘皇族或續集危機。最後一個畫面收在校準過的秤砣與本名簽字；這是分鏡說明，不是臺詞。",
    "每集兩次 satisfaction 與時間點僅是分鏡規劃，需以實際臺詞、TTS、剪輯驗證。聲音分配尚未試聽：旁白用 Sulafat，十一個角色各用一個不重複的 Gemini 聲音（葉穗 Kore、裴定衡 Charon、韓鐸 Orus、羅杏 Vindemiatrix、葉峻 Puck、何靜 Aoede、唐敏 Pulcherrima、賈勳 Fenrir、蕭承越 Algieba、韓芮 Leda、沈巧 Gacrux），聲音性別與角色相符，沒有角色借用旁白的聲音；開拍前仍須以主機聲音池試聽確認，必要時重新 casting。",
    "標題縮圖均為文字方案，尚無生成圖片。描述中的約兩小時是成片目標；預覽、配音、字幕、五語 CC、實際章節時間與上架資料須待媒體產出才能驗收。"
  ]
};
