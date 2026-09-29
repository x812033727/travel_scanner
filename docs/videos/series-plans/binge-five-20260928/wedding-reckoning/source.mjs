export default {
  "series": {
    "slug": "wedding-reckoning",
    "title": "喜宴未散，清算開始",
    "premise": "上一世，沈知棠在婚禮上交出母親留下的公司，最後死於一場被偽裝成意外的大火。重生回簽字前，她當著賓客撕掉授權書，決定以自己的營運能力、可驗證的證據與重新建立的姐妹信任，讓每個拿走她人生的人承擔責任。",
    "genre": "rebirth-revenge",
    "lead": "female",
    "tone": "no-romance",
    "note": "封閉結局，原創架空城市與物流企業。重生只帶來已經歷的記憶，不會揭示前世未知的秘密；對手會因她的改變而提前行動。女主靠營運、分散證據與協作，不靠霸總戀愛救援。10/20/30集改變局勢，40集以自主共同簽約回收。每集兩次具體回報，第一回報規劃30秒內；關閉合集逐集章節卡與重複前情。所有節奏秒數需日後TTS及成片實測。"
  },
  "setting": {
    "world": {
      "place": "架空沿海城市澄港，棠行物流總部與舊倉區",
      "period": "當代架空，故事主行動十日；尾聲數月後。",
      "conflict_engine": "家族公司把愛與授權綁在一起，掌握財務的人能安排誰被看見、誰被辭退；查明帳目會直接威脅控制者利益。",
      "factions": [
        {
          "name": "沈崇岳與關聯供應商",
          "want": "保持內部資訊與資金控制",
          "secret": "供應商侵吞及母親火災利益鏈"
        },
        {
          "name": "顧承川財務端",
          "want": "以婚姻委任取得長期地位",
          "secret": "資料轉移和空殼採購本人參與"
        },
        {
          "name": "一線與獨立查核",
          "want": "保住安全、生計、可被信任的紀錄",
          "secret": "各自握一部分舊紀錄，怕家屬受牽連"
        }
      ],
      "visual_language": "婚宴象牙白與冰藍；倉區土灰與橘色安全線；每次獲得主動就讓文件與人物同框，不拍無限數字面板。",
      "narrator": "第三人稱貼近知棠；只在記憶片段標示前世，不說她尚未查到的秘密。"
    },
    "rules": [
      "只有女主記得前世，且只記得她當時親歷的內容；不能憑記憶知道藏帳位置或秘密會談。",
      "重生一次，不能再次讀檔；今生改變後其他人會調整行動。",
      "撕掉未簽文件只阻止該次簽署，不能魔法般撤銷其他既有法律關係；由稽核與適格專業逐項處理。",
      "證據至少有來源、持有人與取得過程；錄音、帳號登入或重生記憶都不能獨立替代完整查證。",
      "知夏的沉默有保護動機，也造成實際傷害；完整解釋和道歉後才有合作。",
      "安全修繕在11集啟動、26集完成並驗收，35集才兌現；現場救援由專業者接手，不美化徒手闖火。",
      "私人可動用資產有限，只足以支付聚焦調查等必要費用，不瞬間填平整家公司虧空。",
      "反派的配合與悔意不抹除已做行為，具體責任由調查與司法程序處理，尾聲給出結果。"
    ],
    "characters": [
      {
        "id": "zhitang",
        "name": "沈知棠",
        "role": "母親創辦的棠行物流股東、營運主管",
        "age": 28,
        "appearance": "East Asian woman, 28, oval face, straight shoulder-length black hair tucked behind the left ear, dark brown eyes, small silver rectangular watch; ivory tailored trouser suit after the opening ivory wedding dress, no veil after episode 1.",
        "personality": "擅長現場判斷，遇到家人卻容易把服從當信任。",
        "want": "拿回決定權、保住員工與妹妹。",
        "fear": "再次因自己的簽名害死別人。",
        "secret": "記得上一世的死亡，但沒有當時看不到的幕後資訊。",
        "speech": "先問數字，決定後短句不解釋。",
        "voice": {
          "provider": "gemini",
          "name": "Kore",
          "style": "台灣國語；清晰沉著，受傷時降低音量，不變尖銳。"
        },
        "relationships": [
          {
            "with": "zhixia",
            "kind": "由懷疑到共同經營"
          },
          {
            "with": "chengchuan",
            "kind": "拒絕被控制的未婚妻"
          },
          {
            "with": "chongyue",
            "kind": "逐步識破的晚輩"
          },
          {
            "with": "xuwen",
            "kind": "由她決策、他查證的合作人"
          }
        ]
      },
      {
        "id": "zhixia",
        "name": "沈知夏",
        "role": "妹妹、公司資料助理",
        "age": 23,
        "appearance": "East Asian woman, 23, round face, short black bob with one copper hair clip on the right, warm brown eyes, dark teal cardigan and cream shirt, plain canvas shoulder bag.",
        "personality": "敏感、固執，習慣獨自扛下不被理解的責任。",
        "want": "守住母親留下的原始資料與證人。",
        "fear": "姐姐再次把自己的沉默當成背叛。",
        "secret": "匯款是在照顧受脅迫司機的家屬；她保管的資料原本被叔父監控。",
        "speech": "先說沒事，再把最重要的話留到最後。",
        "voice": {
          "provider": "gemini",
          "name": "Aoede",
          "style": "台灣國語；年輕、克制，敢說真話後語速放穩。"
        },
        "relationships": [
          {
            "with": "zhitang",
            "kind": "被誤解的妹妹，後成共同決策者"
          },
          {
            "with": "qide",
            "kind": "替他家屬安排生活"
          },
          {
            "with": "chongyue",
            "kind": "受其以證人安全脅迫"
          }
        ]
      },
      {
        "id": "chengchuan",
        "name": "顧承川",
        "role": "未婚夫、財務主管",
        "age": 31,
        "appearance": "East Asian man, 31, narrow clean-shaven face, neat side-part black hair, navy three-piece suit, brushed gold tie clip, polished shoes; controlled smile and immaculate cuffs.",
        "personality": "擅長安撫與轉移問題，危急時首先保自己。",
        "want": "透過授權書取得女主名下表決權，換取升任控制者。",
        "fear": "失去體面，或成為叔父唯一的代罪者。",
        "secret": "協助轉移帳目；前世在火場放棄女主，今生也準備犧牲知夏。",
        "speech": "句首先叫暱稱，再把要求說成替妳著想。",
        "voice": {
          "provider": "gemini",
          "name": "Puck",
          "style": "台灣國語；親和表面下帶算計，不以低吼演反派。"
        },
        "relationships": [
          {
            "with": "zhitang",
            "kind": "以婚姻交換控制權"
          },
          {
            "with": "chongyue",
            "kind": "被允諾利益也被握住把柄"
          }
        ]
      },
      {
        "id": "chongyue",
        "name": "沈崇岳",
        "role": "叔父、棠行物流董事長",
        "age": 57,
        "appearance": "East Asian man, 57, square face, salt-and-pepper hair brushed back, thin metal glasses, charcoal mandarin-collar jacket, amber cuff button on right wrist.",
        "personality": "能等、懂交易，相信家族名聲比人的命更重要。",
        "want": "保住歷年侵吞與火災真相，維持公司控制權。",
        "fear": "原始出貨與採購帳相互勾稽。",
        "secret": "以空殼供應商侵吞資產，曾指使焚毀母親查到的帳證。",
        "speech": "先叫大家坐下，從不主動把命令說完整。",
        "voice": {
          "provider": "gemini",
          "name": "Charon",
          "style": "台灣國語；低、緩、像在談家常；敗局才出現呼吸失序。"
        },
        "relationships": [
          {
            "with": "zhitang",
            "kind": "假監護者與真正控制者"
          },
          {
            "with": "chengchuan",
            "kind": "財務代理人，必要時可捨棄"
          },
          {
            "with": "zhixia",
            "kind": "以證人家屬安全控制資料持有人"
          }
        ]
      },
      {
        "id": "xuwen",
        "name": "許聞",
        "role": "外部稽核員",
        "age": 34,
        "appearance": "East Asian man, 34, lean face, short slightly wavy black hair, rectangular black glasses, light grey shirt with rolled sleeves, canvas document satchel, blue mechanical pencil.",
        "personality": "重程序，不以猜測代替證據。",
        "want": "把可以驗證的紀錄交到合法調查與外部保管。",
        "fear": "一份未查清的指控害了無辜者。",
        "secret": "曾因追查供應商遭公司停止委任，保留的是自己的工作底稿，不是萬能祕密。",
        "speech": "把知道、推測、還不知道分開說。",
        "voice": {
          "provider": "gemini",
          "name": "Orus",
          "style": "台灣國語；平穩中低音，數字咬字清楚。"
        },
        "relationships": [
          {
            "with": "zhitang",
            "kind": "提供查證與風險，由她作選擇"
          },
          {
            "with": "shuyun",
            "kind": "核對工作紀錄的夥伴"
          }
        ]
      },
      {
        "id": "qide",
        "name": "周啟德",
        "role": "舊車隊司機",
        "age": 52,
        "appearance": "East Asian man, 52, weathered broad face, close-cropped greying hair, navy work jacket with orange seam, old brown leather key pouch on belt, no visible injury initially.",
        "personality": "寡言，保護家人比自保更積極。",
        "want": "家人安全、說出當年實際運送內容。",
        "fear": "被當成唯一放火者。",
        "secret": "火災當晚運走過帳箱，但不是縱火者；保存了車輛過磅紙。",
        "speech": "用路線與時間回答，不下判斷。",
        "voice": {
          "provider": "gemini",
          "name": "Fenrir",
          "style": "台灣國語；粗啞但不誇張，關鍵時間慢說。"
        },
        "relationships": [
          {
            "with": "zhixia",
            "kind": "受到其援助但怕連累她"
          },
          {
            "with": "zhitang",
            "kind": "從不敢信任到願意作證"
          }
        ]
      },
      {
        "id": "shuyun",
        "name": "杜淑雲",
        "role": "老廠維修員",
        "age": 49,
        "appearance": "East Asian woman, 49, sturdy build, tied low ponytail with grey streak, faded olive utility shirt, red fabric tool pouch, small crescent scar on left eyebrow.",
        "personality": "相信看得見的零件與簽收，說話直。",
        "want": "讓老廠的人能安全離開工作場所。",
        "fear": "她早年被忽略的維修報告再次變成死傷。",
        "secret": "留著前後兩版門鎖更換工單，能分辨正常維修與事後改裝。",
        "speech": "先問誰驗收，再伸手檢查。",
        "voice": {
          "provider": "gemini",
          "name": "Sulafat",
          "style": "台灣國語；沉著、成熟、台灣國語，像可信的師傅。"
        },
        "relationships": [
          {
            "with": "zhitang",
            "kind": "以實際修繕建立信任"
          },
          {
            "with": "qide",
            "kind": "核對火災前後現場變化"
          }
        ]
      },
      {
        "id": "yunhe",
        "name": "沈雲禾",
        "role": "已故母親、公司創辦人",
        "age": 46,
        "appearance": "East Asian woman in archival recordings, 46, long black hair in low bun, pale blue blouse, silver rectangular watch identical to the lead heirloom, soft square face; archival wardrobe never changes.",
        "personality": "重視一線員工，不願用親情掩飾帳目。",
        "want": "留下可追查的紀錄並保護兩個女兒。",
        "fear": "查帳牽連無辜的工人。",
        "secret": "生前已把帳冊拆成不同保管來源，錄音本身只是線索。",
        "speech": "先說人，再談數字。",
        "voice": {
          "provider": "gemini",
          "name": "Sulafat",
          "style": "台灣國語；與杜淑雲同基礎聲音但更輕柔的錄音質地；開拍前需試聽確認可辨。"
        },
        "relationships": [
          {
            "with": "zhitang",
            "kind": "母親與她自主判斷的起點"
          },
          {
            "with": "zhixia",
            "kind": "交付日常照顧與資料保管的女兒"
          }
        ]
      }
    ],
    "locations": [
      {
        "id": "banquet",
        "name": "酒店婚宴廳",
        "description": "象牙白花牆、深藍長桌、中央簽署席；文件與金色領帶夾為視覺重點。"
      },
      {
        "id": "meeting",
        "name": "玻璃會議室／外部會談室",
        "description": "長方桌、百葉窗、藍色鉛筆與一個外部保管文件箱；不以陌生豪宅救場。"
      },
      {
        "id": "archive",
        "name": "資料室",
        "description": "低矮紙本櫃與一張終端桌，索引分色、每份原件有封套。"
      },
      {
        "id": "depot",
        "name": "車隊裝卸場",
        "description": "橘色地面動線、灰色貨車、簽收台與大型機械時鐘。"
      },
      {
        "id": "warehouse",
        "name": "舊倉庫與安全警戒外圍",
        "description": "同一座二層倉庫，主門、兩條已標示安全出口、外側點名區；火災鏡頭不改空間方向。"
      }
    ],
    "mysteries": [
      {
        "id": "m01",
        "question": "婚禮附件到底轉走什麼？",
        "answer": "表決權委託與對外授權串聯，讓財務代理能轉移資料；單靠撕紙不能撤銷其他已簽文件，所以需要逐項查核。",
        "planted": 1,
        "advanced": [
          2,
          3,
          8,
          18,
          34
        ],
        "revealed": 18,
        "reserved": false,
        "payoff_episodes": [
          3,
          18,
          34
        ]
      },
      {
        "id": "m02",
        "question": "被辭退的司機為何不能出面？",
        "answer": "周啟德被以家屬生活與偽證要脅，匯款是知夏保護他的生活費；他留有獨立過磅單。",
        "planted": 4,
        "advanced": [
          6,
          7
        ],
        "revealed": 9,
        "reserved": false,
        "payoff_episodes": [
          7,
          9
        ]
      },
      {
        "id": "m03",
        "question": "妹妹的秘密匯款與沉默是否代表背叛？",
        "answer": "知夏援助司機家屬、分散保管帳冊，因證人受威脅而沉默，仍需為隱瞞道歉。婚禮前安全聯絡約定讓知棠重新理解第5、15集親歷的前世片段：妹妹當時曾試著留下、報地點求救，並非背叛；不以跨時間線的物證或妹妹知道重生來解題。",
        "planted": 5,
        "advanced": [
          9,
          15,
          25,
          26
        ],
        "revealed": 25,
        "reserved": false,
        "payoff_episodes": [
          9,
          15,
          25,
          26
        ]
      },
      {
        "id": "m04",
        "question": "母親火災是事故還是滅證？",
        "answer": "封門工單、過磅單、供應商款項與錄音互相印證，證明沈崇岳安排焚帳；任何單一錄音都不直接定罪。",
        "planted": 7,
        "advanced": [
          10,
          11,
          19
        ],
        "revealed": 20,
        "reserved": false,
        "payoff_episodes": [
          10,
          19,
          20
        ]
      },
      {
        "id": "m05",
        "question": "營運考驗為何注定失敗？",
        "answer": "財務端刻意壓住合作運力並安排高價空殼採購，女主以現場調度及獨立簽收破局。",
        "planted": 8,
        "advanced": [
          12
        ],
        "revealed": 14,
        "reserved": false,
        "payoff_episodes": [
          12,
          14
        ]
      },
      {
        "id": "m06",
        "question": "母親的完整帳證藏在哪裡？",
        "answer": "母親錄音給查核方法，知夏保管索引、司機持運送紀錄、稽核員持工作底稿，交叉才形成完整證據。",
        "planted": 10,
        "advanced": [
          15,
          17,
          19
        ],
        "revealed": 24,
        "reserved": false,
        "payoff_episodes": [
          15,
          19,
          24
        ]
      },
      {
        "id": "m07",
        "question": "兩次火場為何有人出不去？",
        "answer": "舊廠逃生門遭改裝；淑雲在11集登記、26集完成合法修繕並教知夏辨認安全出口，今生不再重演。",
        "planted": 11,
        "advanced": [
          12,
          26,
          29
        ],
        "revealed": 35,
        "reserved": false,
        "payoff_episodes": [
          12,
          26,
          35
        ]
      },
      {
        "id": "m08",
        "question": "叔父為何不願把營運真的交給女主？",
        "answer": "侵吞與火災紀錄依賴持續控制內部資訊；女主越能營運，越能看穿虧空。",
        "planted": 14,
        "advanced": [
          18,
          20,
          21,
          28,
          31
        ],
        "revealed": 36,
        "reserved": false,
        "payoff_episodes": [
          20,
          21,
          28,
          31,
          36,
          38
        ]
      },
      {
        "id": "m09",
        "question": "證據被奪是否又會一切歸零？",
        "answer": "17集已談分散保管，24集完成有持有人與簽收的副本；31集委託外部按既定條件交付，不靠臨時黑客或自動全網直播。",
        "planted": 17,
        "advanced": [
          24,
          28,
          31
        ],
        "revealed": 34,
        "reserved": false,
        "payoff_episodes": [
          24,
          28,
          31,
          34
        ]
      },
      {
        "id": "m10",
        "question": "重新信任是否等同再交出控制權？",
        "answer": "姐妹以彼此知情、權責可查的新協議共同經營；不把戀愛或血緣當成免審查憑據。",
        "planted": 1,
        "advanced": [
          16,
          25,
          26,
          28,
          39
        ],
        "revealed": 40,
        "reserved": false,
        "payoff_episodes": [
          16,
          25,
          26,
          28,
          39,
          40
        ]
      }
    ],
    "naming": [
      "企業、城市、供應商均虛構，不借用現實公司商標。",
      "人名全程固定，妹妹只在親近對話稱姐姐；稽核表使用完整姓名。"
    ],
    "never": [
      "不要霸總或神祕富豪解決資金問題。",
      "不要用重生記憶充作能直接定罪的證據。",
      "不要連續受辱拖時間，不用羞辱性別製造爽感。",
      "不要把道歉寫成免責，不把職業救援省略。",
      "不要在第40集留下新敵人、新火災或下一次重生。"
    ],
    "lexicon": {
      "沈知棠": "shěn zhī táng",
      "沈知夏": "shěn zhī xià",
      "顧承川": "gù chéng chuān",
      "沈崇岳": "shěn chóng yuè",
      "許聞": "xǔ wén",
      "周啟德": "zhōu qǐ dé",
      "杜淑雲": "dù shú yún",
      "沈雲禾": "shěn yún hé",
      "棠行": "táng xíng",
      "澄港": "chéng gǎng"
    },
    "ending": "叔父與顧承川依各自行為承擔責任，母親平反但公司仍需重整。知棠與知夏在權責透明、知情可查的協議上共同簽字，最後一句「這次，我們一起簽。」；無新主線。",
    "opening_30_seconds": [
      {
        "seconds": "0–5",
        "picture": "火光映在簽署筆的金屬面，知棠貼住封閉的門。",
        "audio": "知棠：這支筆，上一世害死了我。"
      },
      {
        "seconds": "5–11",
        "picture": "門外未婚夫只露出金色領帶夾與一半側臉。",
        "audio": "顧承川：妳簽完字，就沒有用了。"
      },
      {
        "seconds": "11–20",
        "picture": "硬切婚宴簽署席，完好的筆停在相同附件前。",
        "audio": "顧承川催簽；她停止下筆。"
      },
      {
        "seconds": "20–30",
        "picture": "她撕掉尚未簽名的授權頁，握住完整副本。",
        "audio": "沈知棠：結婚可以。拿走我母親的公司，不行。"
      }
    ]
  },
  "chapters": [
    {
      "number": 1,
      "title": "先把自己的命拿回來",
      "theme": "信任不能取代看清文件。",
      "start_state": "婚禮上即將交出決定權。",
      "end_state": "保存授權與運送證據，火災疑點首次成立。",
      "turn": "母親死亡不再是背景，而是可查的人為事件。",
      "stakes": "自己的人身與公司決定權",
      "question": "她能不簽字，卻能不能找出誰替她安排了人生？",
      "episodes": [
        {
          "number": 1,
          "title": "這次不簽",
          "logline": "顧承川催她把表決權交給自己，她在火場記憶與現場賓客間穩住呼吸。她看見附件頁碼與前世一致，先停止簽名，再請現場保留整份文件。",
          "timeline": "present",
          "hook": "這支筆，上一世害死了我。",
          "hook_type": "line",
          "conflict": "顧承川催她把表決權交給自己，她在火場記憶與現場賓客間穩住呼吸。",
          "turn": "她看見附件頁碼與前世一致，先停止簽名，再請現場保留整份文件。",
          "cliffhanger": {
            "type": "reveal",
            "text": "顧承川收起笑容：附件別給外人看。"
          },
          "setups": [
            "m01",
            "m10"
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
            "zhitang",
            "chengchuan",
            "zhixia"
          ],
          "locations": [
            "banquet"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "在眾人面前停筆，保住尚未交出的授權。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "要求保存文件副本，讓對方無法悄悄換頁。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生當日婚禮後",
            "knowledge": "她知道自己重生，其他人只知她臨時拒簽。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "授權原件留在公證見證桌，女主拍下頁碼；知夏握著未送出的禮袋。",
            "carry_forward": "從文件用途開始查，不假裝已有犯罪鐵證。"
          },
          "closed_ending": false
        },
        {
          "number": 2,
          "title": "替妳著想",
          "logline": "顧承川說附件只是替她省事，還要把拒簽說成羞辱家族。女主逐條讓他念出授權對象，逼他承認涵蓋婚姻以外的公司決策。",
          "timeline": "present",
          "hook": "愛我，為什麼要拿走我的票？",
          "hook_type": "question",
          "conflict": "顧承川說附件只是替她省事，還要把拒簽說成羞辱家族。",
          "turn": "女主逐條讓他念出授權對象，逼他承認涵蓋婚姻以外的公司決策。",
          "cliffhanger": {
            "type": "danger",
            "text": "叔父說願意解釋，但要所有人先關掉相機。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "zhitang",
            "chengchuan",
            "chongyue"
          ],
          "locations": [
            "banquet"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "把私人感情問題拉回可查的文字。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "留下由誰提供文件的明確說法。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生當日婚禮後",
            "knowledge": "女主知道未婚夫急於簽名；叔父知道她開始看文件。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "附件副本由女主持有，原件未被拿走。",
            "carry_forward": "請獨立稽核員核對附件，不在婚宴現場宣布對方有罪。"
          },
          "closed_ending": false
        },
        {
          "number": 3,
          "title": "藏在附件裡",
          "logline": "許聞指出主文與附件交叉授權，撕掉其中一頁不能處理既有委任。女主查清自己過去簽過的範圍，正式要求停止新增委任並留存送達紀錄。",
          "timeline": "present",
          "hook": "正文沒寫的，都在這一頁。",
          "hook_type": "image",
          "conflict": "許聞指出主文與附件交叉授權，撕掉其中一頁不能處理既有委任。",
          "turn": "女主查清自己過去簽過的範圍，正式要求停止新增委任並留存送達紀錄。",
          "cliffhanger": {
            "type": "choice",
            "text": "她必須選：保住婚禮體面，還是讓查核進公司。"
          },
          "setups": [],
          "payoffs": [
            "m01"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "xuwen",
            "chengchuan"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "看懂真正的控制方式。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "停止未完成的委任，保留對既有文件逐項處理的程序。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生當日婚禮後",
            "knowledge": "許聞只知道文件風險，不知道她重生；顧知道委任無法順利擴大。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "完整文件與停止新增委任通知由許聞存底。",
            "carry_forward": "女主決定查核，先找到前世被清掉的一線證人。"
          },
          "closed_ending": false
        },
        {
          "number": 4,
          "title": "先別辭職",
          "logline": "周啟德已收到離職通知，拒絕談母親火災，只想取回家人照片。女主先保住他的工作交接與合法聯絡方式，不逼他當場作證。",
          "timeline": "present",
          "hook": "今天被辭退的人，先留下。",
          "hook_type": "danger",
          "conflict": "周啟德已收到離職通知，拒絕談母親火災，只想取回家人照片。",
          "turn": "女主先保住他的工作交接與合法聯絡方式，不逼他當場作證。",
          "cliffhanger": {
            "type": "reveal",
            "text": "照片背面是妹妹的手機號碼。"
          },
          "setups": [
            "m02"
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
            "zhitang",
            "qide",
            "xuwen"
          ],
          "locations": [
            "depot"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "阻止口頭趕人，保留他的交接紀錄。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "讓司機自主選擇安全的會面地點。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生後第1–2日",
            "knowledge": "女主發現司機與妹妹有聯繫；司機不信任沈家的人。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "司機持舊鑰匙包與家人照片，女主只保管通知副本。",
            "carry_forward": "追查匯款但不以私人猜測公開指控妹妹。"
          },
          "closed_ending": false
        },
        {
          "number": 5,
          "title": "那筆錢",
          "logline": "女主在公司報支附件看見知夏的個人匯款憑證，以為她收買司機。短閃回只用知棠親眼所見：前世老倉火起、顧封門前，知夏攔著他說「我陪她留下，你先走」；知棠站在妹妹斜後方，看見她背在身後的手機仍在通話，當時誤以為妹妹正與顧串通。知夏承認匯款，卻拒絕交出家屬住址；女主先核實錢不是公司轉出。",
          "timeline": "present",
          "hook": "妳每個月，都給他匯款？",
          "hook_type": "reversal",
          "conflict": "女主在公司報支附件看見知夏的個人匯款憑證，以為她收買司機。短閃回只用知棠親眼所見：前世老倉火起、顧封門前，知夏攔著他說「我陪她留下，你先走」；知棠站在妹妹斜後方，看見她背在身後的手機仍在通話，當時誤以為妹妹正與顧串通。",
          "turn": "知夏承認匯款，卻拒絕交出家屬住址；女主先核實錢不是公司轉出。",
          "cliffhanger": {
            "type": "danger",
            "text": "知夏說：妳查我可以，別把地址交給叔叔。"
          },
          "setups": [
            "m03"
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
            "zhitang",
            "zhixia",
            "chengchuan"
          ],
          "locations": [
            "archive",
            "warehouse"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "分清個人援助與公司款項，阻止錯誤指控。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "保住未公開的家屬地址。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生後第1–2日",
            "knowledge": "姐妹各有戒心；知夏不知道姐姐記得另一條人生。第5集只呈現姐姐當時的誤讀，不讓妹妹知曉前世；手機通話對象尚不可見。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "匯款憑證遮住地址存檔，原件仍由知夏保管。",
            "carry_forward": "查收款用途而不是偷走家屬資訊。"
          },
          "closed_ending": false
        },
        {
          "number": 6,
          "title": "證人要走",
          "logline": "司機突然請假離城，顧承川的書面說明聲稱他已承認做錯事；顧本人不出場、不配旁白。女主先讓許聞核對他親自簽下的陳述，發現所謂認罪只有財務端轉述。",
          "timeline": "present",
          "hook": "他連夜搬走，不是自願的。",
          "hook_type": "line",
          "conflict": "司機突然請假離城，顧承川的書面說明聲稱他已承認做錯事；顧本人不出場、不配旁白。",
          "turn": "女主先讓許聞核對他親自簽下的陳述，發現所謂認罪只有財務端轉述。",
          "cliffhanger": {
            "type": "reveal",
            "text": "周啟德在電話裡說：那晚車上裝的不是貨。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "qide",
            "xuwen"
          ],
          "locations": [
            "depot",
            "meeting"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "拆開轉述與本人陳述。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "協助司機家屬安全搬遷，換取可由他拒絕的正式訪談。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生後第1–2日",
            "knowledge": "司機願意談運送，不願猜縱火者；未婚夫不知道他已聯繫稽核員。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "訪談紀錄由許聞保存，司機仍保有自己的過磅紙。",
            "carry_forward": "回查火災前後運送，不把一句話當終局證據。"
          },
          "closed_ending": false
        },
        {
          "number": 7,
          "title": "多出的重量",
          "logline": "公司紀錄寫周啟德當晚空車離廠，舊過磅紙卻記著載重。女主找到獨立站點簽章，排除司機自己改寫的可能，逼出有人調換出貨欄位。",
          "timeline": "present",
          "hook": "空車，怎麼會重三百公斤？",
          "hook_type": "question",
          "conflict": "公司紀錄寫周啟德當晚空車離廠，舊過磅紙卻記著載重。",
          "turn": "女主找到獨立站點簽章，排除司機自己改寫的可能，逼出有人調換出貨欄位。",
          "cliffhanger": {
            "type": "reversal",
            "text": "帳箱運出後，母親的辦公室才起火。"
          },
          "setups": [
            "m04"
          ],
          "payoffs": [
            "m02"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "qide",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "以第三方紙本拆穿空車說法。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "保住司機非縱火承認書的證詞邊界。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生後第1–2日",
            "knowledge": "三人知有資料被移走，仍不知誰下令。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "過磅原紙封存，影本記持有人及取得日期。",
            "carry_forward": "回到妹妹匯款與搬遷地址，確認她知道多少。"
          },
          "closed_ending": false
        },
        {
          "number": 8,
          "title": "故意輸掉的單",
          "logline": "叔父交出限時大單考驗女主，財務端卻把合作車隊的款項扣住。她先查出是付款條件阻塞，不接受把責任推給司機，決定用可承擔的小批次履約。",
          "timeline": "present",
          "hook": "這張單，根本沒留車給我。",
          "hook_type": "image",
          "conflict": "叔父交出限時大單考驗女主，財務端卻把合作車隊的款項扣住。",
          "turn": "她先查出是付款條件阻塞，不接受把責任推給司機，決定用可承擔的小批次履約。",
          "cliffhanger": {
            "type": "choice",
            "text": "若她接單失敗，營運權就要正式收回。"
          },
          "setups": [
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
            "zhitang",
            "chongyue",
            "xuwen"
          ],
          "locations": [
            "meeting",
            "depot"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "辨認真瓶頸而非責怪現場。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "拿到部分可執行的運力承諾，保住選項。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生後第1–2日",
            "knowledge": "女主知道考驗不公平，叔父要她公開承諾結果。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "訂單、付款時間與授權附件交叉標記。",
            "carry_forward": "以能力履約，同時不放棄證人追查。"
          },
          "closed_ending": false
        },
        {
          "number": 9,
          "title": "匯款的另一端",
          "logline": "女主核對知夏提供的遮罩收據，發現款項對應家屬生活與搬遷。司機自己證明妹妹曾提醒他保留原紙，但知夏仍不肯解釋全部。",
          "timeline": "present",
          "hook": "她付的，是證人孩子的學費。",
          "hook_type": "danger",
          "conflict": "女主核對知夏提供的遮罩收據，發現款項對應家屬生活與搬遷。",
          "turn": "司機自己證明妹妹曾提醒他保留原紙，但知夏仍不肯解釋全部。",
          "cliffhanger": {
            "type": "emotion",
            "text": "女主第一次把責問改成：妳還瞞了什麼危險？"
          },
          "setups": [],
          "payoffs": [
            "m02",
            "m03"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "zhixia",
            "qide"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "收款用途獲證人與收據交叉確認。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "姐妹停止一次錯誤爭吵，保護證人線未斷。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生後第1–2日",
            "knowledge": "女主知道妹妹至少在保護證人，不等於已完全互信。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "匯款收據和周的證詞分別存檔，住址不入公開資料。",
            "carry_forward": "查母親火災，知夏可交出部分索引。"
          },
          "closed_ending": false
        },
        {
          "number": 10,
          "title": "不是意外",
          "logline": "女主找到火災索引，維修與出貨紀錄在同一天被抽走。她把過磅時間與關門時間對齊，第一次確認事故說法存在人為安排。",
          "timeline": "present",
          "hook": "起火前，逃生門先被換了。",
          "hook_type": "reversal",
          "conflict": "女主找到火災索引，維修與出貨紀錄在同一天被抽走。",
          "turn": "她把過磅時間與關門時間對齊，第一次確認事故說法存在人為安排。",
          "cliffhanger": {
            "type": "reversal",
            "text": "索引最後一頁是母親手寫：不要只查財務。"
          },
          "setups": [
            "m06"
          ],
          "payoffs": [
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
            "zhitang",
            "xuwen",
            "zhixia"
          ],
          "locations": [
            "archive"
          ],
          "theme": "信任不能取代看清文件。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "把兩條獨立時間線對上。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "找出可聯絡的原維修承辦人，讓疑點變成下一步。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "重生後第1–2日",
            "knowledge": "三人知滅證可能性升高，但未指認下令者。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "知夏交出索引影本，原帳仍分散藏存。",
            "carry_forward": "找維修員杜淑雲，避免只靠錄音猜兇手。"
          },
          "closed_ending": false
        }
      ]
    },
    {
      "number": 2,
      "title": "抓到的只是替人辦事",
      "theme": "能力與可驗證的資料，讓反擊站得住。",
      "start_state": "知道火災有疑點，但未婚夫仍是最明顯的敵人。",
      "end_state": "叔父的利益與授意鏈被辨明，對手全面反制。",
      "turn": "家族恩人正是必須面對的幕後者。",
      "stakes": "員工生計與母親清白",
      "question": "她能否分清看得見的執行者與真正控制者？",
      "episodes": [
        {
          "number": 11,
          "title": "修過兩次的門",
          "logline": "杜淑雲不願再被拿來背書，她曾報告異常卻被撤換。女主請她對比兩版工單，發現正常修繕後又有人追加改裝，先簽下如今必須修復的安全清單。修復清單同時列出安全出口旁的固定緊急對講及備援電源；此集只列項，尚未修妥。",
          "timeline": "present",
          "hook": "同一扇門，為什麼驗收兩次？",
          "hook_type": "line",
          "conflict": "杜淑雲不願再被拿來背書，她曾報告異常卻被撤換。",
          "turn": "女主請她對比兩版工單，發現正常修繕後又有人追加改裝，先簽下如今必須修復的安全清單。修復清單同時列出安全出口旁的固定緊急對講及備援電源；此集只列項，尚未修妥。",
          "cliffhanger": {
            "type": "reveal",
            "text": "追加工單用的是財務核准章。"
          },
          "setups": [
            "m07"
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
            "zhitang",
            "shuyun",
            "xuwen"
          ],
          "locations": [
            "warehouse"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "分清維修員原施工與事後改裝。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "當場安排現場檢查，開始消除仍存在的危險。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "淑雲知道女主願意真正修，女主知道核准端與財務相連。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "兩版工單由淑雲保原、許聞存副本；修繕尚未完成。固定對講納入同一修復工單，待第26集實測。",
            "carry_forward": "營運履約與門修繕並行，不能在高潮才忽然有安全門。"
          },
          "closed_ending": false
        },
        {
          "number": 12,
          "title": "第一批到了",
          "logline": "顧承川傳來的書面期限通知施壓，女主必須避免為面子超接能力；顧不在現場、不新增聲音。她調整裝卸順序，以多批獨立簽收完成已允諾部分，再以客戶同意的新排程補齊。",
          "timeline": "present",
          "hook": "他們說沒車，我就拆成三批。",
          "hook_type": "question",
          "conflict": "顧承川傳來的書面期限通知施壓，女主必須避免為面子超接能力；顧不在現場、不新增聲音。",
          "turn": "她調整裝卸順序，以多批獨立簽收完成已允諾部分，再以客戶同意的新排程補齊。",
          "cliffhanger": {
            "type": "reversal",
            "text": "車到了，網上卻開始傳她挪用公司救自己的名聲。"
          },
          "setups": [],
          "payoffs": [
            "m05",
            "m07"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "qide",
            "shuyun"
          ],
          "locations": [
            "depot"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "第一批可驗收貨物準時抵達。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "拿到客戶而非家族內部的履約確認。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "一線人員知道她能做事，財務端改用名譽攻擊。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "客戶簽收留外部副本；淑雲帶回門檢查結果。",
            "carry_forward": "用資料回應抹黑，不安排一段空轉辱罵。"
          },
          "closed_ending": false
        },
        {
          "number": 13,
          "title": "失控的人",
          "logline": "顧承川以擔心健康為由要女主停止工作，剪輯婚宴片段證明她不理性。她拒絕在鏡頭前自證情緒，改以履約和付款紀錄提出可查的質疑。",
          "timeline": "present",
          "hook": "說我失控的人，先把帳打開。",
          "hook_type": "image",
          "conflict": "顧承川以擔心健康為由要女主停止工作，剪輯婚宴片段證明她不理性。",
          "turn": "她拒絕在鏡頭前自證情緒，改以履約和付款紀錄提出可查的質疑。",
          "cliffhanger": {
            "type": "choice",
            "text": "叔父的書面核准函送到：同意公開看帳，卻指定只看一張總表；不插入他的發聲鏡頭。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "chengchuan",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "取得完整婚宴見證紀錄，拆穿剪輯順序。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "把討論轉到可核對的採購明細。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "外部只見雙方爭議，不能寫成群眾立刻全信女主。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "完整影像由見證人交付稽核，總表與明細待對照。",
            "carry_forward": "讓採購回扣在下一集以具體數字證明。"
          },
          "closed_ending": false
        },
        {
          "number": 14,
          "title": "第一次平反",
          "logline": "財務總表看似平衡，女主須在限定說明時間指出具體錯誤。她用客戶簽收、實際車隊請款與空殼供應商款項勾稽，證明多付的一筆未提供服務。",
          "timeline": "present",
          "hook": "同一車貨，怎麼付了兩次？",
          "hook_type": "danger",
          "conflict": "財務總表看似平衡，女主須在限定說明時間指出具體錯誤。",
          "turn": "她用客戶簽收、實際車隊請款與空殼供應商款項勾稽，證明多付的一筆未提供服務。",
          "cliffhanger": {
            "type": "reveal",
            "text": "空殼供應商的往來簽章，出自叔父辦公室。"
          },
          "setups": [
            "m08"
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
            "zhitang",
            "xuwen",
            "chongyue"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "公開證明營運考驗被人為加價。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "讓稽核範圍擴大到關聯供應商，完成首次公開平反。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "女主知道叔父有關聯但未證明火災指使；叔父知道她查得懂。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "對帳表有三方來源，簽章影本待驗。",
            "carry_forward": "妹妹判斷可合作，交出帳冊線索。"
          },
          "closed_ending": false
        },
        {
          "number": 15,
          "title": "母親留下的空格",
          "logline": "知夏只給索引不給原帳，女主認為又被阻攔。妹妹說出分散保管的安排，交付可驗證的一段對應碼；女主照碼找到一筆被刪去的交易。妹妹要求先保護持有人，引出知棠對同一次前世火災的第二段短記憶：她親耳聽見知夏朝背後仍連線的手機重複「老倉東側」，當時卻當成向顧報出姐姐所在；鏡頭只回到知棠當年看得到的位置。",
          "timeline": "present",
          "hook": "缺的那一頁，在妹妹手裡。",
          "hook_type": "reversal",
          "conflict": "知夏只給索引不給原帳，女主認為又被阻攔。",
          "turn": "妹妹說出分散保管的安排，交付可驗證的一段對應碼；女主照碼找到一筆被刪去的交易。妹妹要求先保護持有人，引出知棠對同一次前世火災的第二段短記憶：她親耳聽見知夏朝背後仍連線的手機重複「老倉東側」，當時卻當成向顧報出姐姐所在；鏡頭只回到知棠當年看得到的位置。",
          "cliffhanger": {
            "type": "choice",
            "text": "知夏要求她答應：先保護持有人，再拿原件。"
          },
          "setups": [],
          "payoffs": [
            "m03",
            "m06"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "zhixia",
            "xuwen"
          ],
          "locations": [
            "archive",
            "warehouse"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "對應碼導向確實存在的外部憑證。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "姐妹約定取證前先確認持有人安全。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "女主知道完整證據需要多源拼合，許聞知道不能一口氣曝光持有人。觀眾已見妹妹留在姐姐身邊和持續報地點兩個片段，仍不知道通話對象。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "索引新增對應碼，原件位置仍由各持有人掌握。",
            "carry_forward": "女主下一步需在利益與員工之間作具體選擇。"
          },
          "closed_ending": false
        },
        {
          "number": 16,
          "title": "不能拿人填帳",
          "logline": "叔父要求停發一線費用美化財報，稱這是穩住股東唯一方法。女主縮減自己主導的宣傳支出、縮小營運承諾，把有限資金優先放在已有勞務與安全需求。",
          "timeline": "present",
          "hook": "報表好看了，工人怎麼活？",
          "hook_type": "line",
          "conflict": "叔父要求停發一線費用美化財報，稱這是穩住股東唯一方法。",
          "turn": "女主縮減自己主導的宣傳支出、縮小營運承諾，把有限資金優先放在已有勞務與安全需求。",
          "cliffhanger": {
            "type": "danger",
            "text": "她失去叔父的財務支持，只剩自己能負擔的調查。"
          },
          "setups": [],
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
            "zhitang",
            "chongyue",
            "qide"
          ],
          "locations": [
            "meeting",
            "depot"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "阻止把已發生的人力成本悄悄抹掉。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "提出有支出來源的短期安排，員工不必盲信口號。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "工人知道她願承擔利益損失，叔父決定切斷協助。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "資金用途與她自負的費用分開入帳，沒有無限財富。",
            "carry_forward": "調查必須縮小範圍，引真正保管人出手。"
          },
          "closed_ending": false
        },
        {
          "number": 17,
          "title": "讓他來拿",
          "logline": "資料存取端一直有人監看，直接找原件會暴露證人。女主與許聞放出僅涉及副本的查核日程，先設定存取紀錄保全及外部保管流程。",
          "timeline": "present",
          "hook": "想知道誰怕，就讓他來拿。",
          "hook_type": "question",
          "conflict": "資料存取端一直有人監看，直接找原件會暴露證人。",
          "turn": "女主與許聞放出僅涉及副本的查核日程，先設定存取紀錄保全及外部保管流程。",
          "cliffhanger": {
            "type": "reveal",
            "text": "財務帳號半夜登入了不屬於它的檔案區。"
          },
          "setups": [
            "m09"
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
            "zhitang",
            "xuwen",
            "zhixia"
          ],
          "locations": [
            "archive"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "識別監看的權限入口。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "把誘餌限制為已有副本，不拿證人安全冒險。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "三人知道有人越權，不知是未婚夫親自還是代用帳號。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "誘餌副本有雜湊與借閱登記；真正分散證據未搬動。",
            "carry_forward": "需要人與帳號實際動作的交叉證明。"
          },
          "closed_ending": false
        },
        {
          "number": 18,
          "title": "他親手搬走",
          "logline": "顧承川把異常登入推給部屬，女主不能只靠帳號認人。門禁簽收與庫房借閱紀錄對上他親自搬箱子的時間，授權附件也解釋他如何取得權限。",
          "timeline": "present",
          "hook": "登入的人，還帶走了紙本。",
          "hook_type": "image",
          "conflict": "顧承川把異常登入推給部屬，女主不能只靠帳號認人。",
          "turn": "門禁簽收與庫房借閱紀錄對上他親自搬箱子的時間，授權附件也解釋他如何取得權限。",
          "cliffhanger": {
            "type": "choice",
            "text": "他不再說愛，只問她願不願意談條件。"
          },
          "setups": [],
          "payoffs": [
            "m01"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "chengchuan",
            "xuwen"
          ],
          "locations": [
            "archive",
            "meeting"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "用三種紀錄排除代登的說法。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "收回不當擴張的資料存取，正式保全搬移清單。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "未婚夫知道女主握有本人行動證明；叔父仍假裝置身事外。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "原檔和紙本保全清單交由許聞複核，不在家族私下交換。",
            "carry_forward": "把母親錄音當查核提示，再對照舊帳。"
          },
          "closed_ending": false
        },
        {
          "number": 19,
          "title": "錄音不是答案",
          "logline": "錄音提到叔父，但部分聲音受損，女主急於相信自己已找到兇手。許聞提醒她把一句話拆成日期、款項與現場三件可驗證的事；三者逐一對上。",
          "timeline": "present",
          "hook": "母親說的名字，還要查證。",
          "hook_type": "danger",
          "conflict": "錄音提到叔父，但部分聲音受損，女主急於相信自己已找到兇手。",
          "turn": "許聞提醒她把一句話拆成日期、款項與現場三件可驗證的事；三者逐一對上。",
          "cliffhanger": {
            "type": "reveal",
            "text": "改門核准、轉帳與移帳箱，都指向同一個辦公室。"
          },
          "setups": [],
          "payoffs": [
            "m04",
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
            "zhitang",
            "xuwen",
            "yunhe"
          ],
          "locations": [
            "archive"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "找到錄音內容對應的獨立日期證據。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "避免把受損錄音剪成情緒性指控，保住證據可信度。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "母親以舊錄音出場；女主開始用證據取代重生確信。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "錄音原檔封存，修復僅作輔助，原始與處理版本分存。",
            "carry_forward": "需要把叔父的授意鏈與利益動機完整連起來。"
          },
          "closed_ending": false
        },
        {
          "number": 20,
          "title": "真正的主人",
          "logline": "女主把財務、門改裝與車隊紀錄交叉，叔父以維護公司名聲要求私下處理。她確認未婚夫只是執行與得利者；母親當年被阻止的，是對叔父侵吞的查核。",
          "timeline": "present",
          "hook": "他們都在替叔叔清場。",
          "hook_type": "reversal",
          "conflict": "女主把財務、門改裝與車隊紀錄交叉，叔父以維護公司名聲要求私下處理。",
          "turn": "她確認未婚夫只是執行與得利者；母親當年被阻止的，是對叔父侵吞的查核。",
          "cliffhanger": {
            "type": "reversal",
            "text": "叔父說：妳那套查帳辦法，從今天起就沒用了。"
          },
          "setups": [],
          "payoffs": [
            "m04",
            "m08"
          ],
          "tension": [
            4,
            3,
            5,
            4,
            5
          ],
          "characters": [
            "zhitang",
            "chongyue",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "能力與可驗證的資料，讓反擊站得住。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "拼出三條獨立證據的共同指向。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "拒絕家族內部和解，將調查交給適格外部專業處理。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第3–6日",
            "knowledge": "女主識破幕後者；叔父只看出她提前防備，不知道重生真相。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "原件持有人清單由許聞保密管理，外部調查已啟動但非即刻判決。",
            "carry_forward": "對手不照前世行動，女主必須即時判斷。"
          },
          "closed_ending": false
        }
      ]
    },
    {
      "number": 3,
      "title": "未來不再照記憶走",
      "theme": "選擇可信的人，比記得未來重要。",
      "start_state": "女主已知敵人，卻失去前世時間表與公司資源。",
      "end_state": "證據分散保全、姐妹合作成立，倉庫火場再現。",
      "turn": "危險重演，但她這次提前修好了一條路。",
      "stakes": "妹妹生命與是否犧牲證人",
      "question": "沒有先知優勢時，她願意靠什麼贏？",
      "episodes": [
        {
          "number": 21,
          "title": "明天提前來了",
          "logline": "原本以為還有兩日的資料清理提前啟動，女主趕到時舊辦公室已封。她用17集保全的存取紀錄及搬移清單找到新去向，承認記憶只是線索不是時間表。",
          "timeline": "present",
          "hook": "前世明天的事，今天就發生了。",
          "hook_type": "line",
          "conflict": "原本以為還有兩日的資料清理提前啟動，女主趕到時舊辦公室已封。",
          "turn": "她用17集保全的存取紀錄及搬移清單找到新去向，承認記憶只是線索不是時間表。",
          "cliffhanger": {
            "type": "danger",
            "text": "新的命令先切資金，才動資料。"
          },
          "setups": [],
          "payoffs": [
            "m08"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "xuwen",
            "chengchuan"
          ],
          "locations": [
            "archive"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "保住搬移追蹤鏈，沒有因時間變動全部歸零。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "立即改以現況排調查優先次序。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "女主獨知前世優勢有限；許聞只見她願意修正判斷。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "搬移清單仍有副本，封存現況留紀錄。",
            "carry_forward": "解決現實費用缺口，不憑空取得巨額資金。"
          },
          "closed_ending": false
        },
        {
          "number": 22,
          "title": "沒錢的查核",
          "logline": "公司停止支付外部查核費用，許聞不能無限提供人力，證人安置也有壓力。女主列出已取得證據與最低必要支出，縮掉可延後項，讓調查不依賴叔父授權。",
          "timeline": "present",
          "hook": "他不是不付錢，是要我們閉嘴。",
          "hook_type": "question",
          "conflict": "公司停止支付外部查核費用，許聞不能無限提供人力，證人安置也有壓力。",
          "turn": "女主列出已取得證據與最低必要支出，縮掉可延後項，讓調查不依賴叔父授權。",
          "cliffhanger": {
            "type": "choice",
            "text": "她能立即變現的，只剩原定婚禮的私人資產。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "xuwen",
            "zhixia"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "分清必做與可停項，保住核心調查。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "約定專業服務範圍與費用，不要求同伴無條件奉獻。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "姐妹知道資源有限，沒有忽然出現富豪相助。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "費用預算與公司帳務隔離。",
            "carry_forward": "用有限私人資產支撐查核，不承諾付全公司工資。"
          },
          "closed_ending": false
        },
        {
          "number": 23,
          "title": "賣掉那枚戒指",
          "logline": "未婚夫以歸還珠寶為條件要求她撤回指控，女主需確認自己的財產與調查費來源。她只處分明確屬於自己的婚禮支出退款與資產，付出可驗證的調查、保管和安置費。",
          "timeline": "present",
          "hook": "這枚戒指，先換證人平安。",
          "hook_type": "image",
          "conflict": "未婚夫以歸還珠寶為條件要求她撤回指控，女主需確認自己的財產與調查費來源。",
          "turn": "她只處分明確屬於自己的婚禮支出退款與資產，付出可驗證的調查、保管和安置費。",
          "cliffhanger": {
            "type": "reveal",
            "text": "知夏帶來最後一位願意核對原件的持有人。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "zhitang",
            "chengchuan",
            "zhixia"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "不接受以費用交換沉默。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "完成必要費用支付，使資料保全可繼續。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "未婚夫知道金錢勒索無效；妹妹看到姐姐實際付出。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "退款與服務收據留存，戒指不是一枚換整家公司。",
            "carry_forward": "組合原始來源，不能只靠複印文件堆積。"
          },
          "closed_ending": false
        },
        {
          "number": 24,
          "title": "三份不一樣的原件",
          "logline": "不同保管人的日期與記號不一，女主必須證明它們講的是同一筆事。索引、過磅單、稽核底稿對上，並由各持有人確認；另做封存副本與交付紀錄。",
          "timeline": "present",
          "hook": "不是一份神帳，是三個人。",
          "hook_type": "danger",
          "conflict": "不同保管人的日期與記號不一，女主必須證明它們講的是同一筆事。",
          "turn": "索引、過磅單、稽核底稿對上，並由各持有人確認；另做封存副本與交付紀錄。",
          "cliffhanger": {
            "type": "reversal",
            "text": "叔父能拿走一箱，卻拿不走所有人的證詞。"
          },
          "setups": [],
          "payoffs": [
            "m06",
            "m09"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "xuwen",
            "qide",
            "zhixia"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "拼出完整但可追溯來源的證據鏈。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "完成分散外部保管，失去單一原件不會全盤失效。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "持有人知道自己交出了哪一份，不暴露彼此住址。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "許聞保存來源表；各保管端收到副本與交付簽收。",
            "carry_forward": "知夏能終於解釋前世看似背叛的沉默。"
          },
          "closed_ending": false
        },
        {
          "number": 25,
          "title": "不是站在他那邊",
          "logline": "姐妹翻看母親紀錄，知夏出示婚禮前就與周啟德約好的安全聯絡紙：若家屬或姐姐受威脅，先穩住施壓者，保持通話並重複所在地，請周向正式救援求助。她承認為保護持有人曾向叔父承諾沉默，卻讓姐姐承受錯誤資訊。知棠在內心將第5、15集自己見過的片段拼回：那句留下和連線報地點，是妹妹曾試圖拖時間救她。她只確認這個意圖，不知道前世電話另一端實際做了什麼，也沒有把另一條人生告訴妹妹；知夏只解釋婚禮前已有的約定。姐妹各為隱瞞和錯怪道歉，改成共同決策。",
          "timeline": "present",
          "hook": "原來那句留下，是替我求救。",
          "hook_type": "reversal",
          "conflict": "姐妹翻看母親紀錄，知夏出示婚禮前就與周啟德約好的安全聯絡紙：若家屬或姐姐受威脅，先穩住施壓者，保持通話並重複所在地，請周向正式救援求助。她承認為保護持有人曾向叔父承諾沉默，卻讓姐姐承受錯誤資訊。",
          "turn": "知棠在內心將第5、15集自己見過的片段拼回：那句留下和連線報地點，是妹妹曾試圖拖時間救她。她只確認這個意圖，不知道前世電話另一端實際做了什麼，也沒有把另一條人生告訴妹妹；知夏只解釋婚禮前已有的約定。姐妹各為隱瞞和錯怪道歉，改成共同決策。",
          "cliffhanger": {
            "type": "emotion",
            "text": "女主把資料夾推給妹妹：這一次，妳也決定。"
          },
          "setups": [],
          "payoffs": [
            "m03",
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
            "zhitang",
            "zhixia"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "知棠看見早於婚禮的聯絡約定，重新理解兩次已演過的前世片段：妹妹試過救她，而非只求顧帶自己離開。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "說清匯款與沉默的因果後，姐妹各自承擔錯誤，把單方保護改成共同決定。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "只有知棠擁有前世記憶；知夏不知道重生，只說明婚禮前即已存在的安全約定。前世求救是否接通救援、周做了什麼均不冒充已證事實。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "婚禮前的安全聯絡紙與母親索引留存；它不是另一條時間線的通話紀錄，前世救人意圖由知棠對親歷片段重新理解。",
            "carry_forward": "共同安排證人和場地安全，給26集行動而非只和解。"
          },
          "closed_ending": false
        },
        {
          "number": 26,
          "title": "一起走一遍",
          "logline": "姐妹預備最後取證與撤場，發現老倉庫仍有人想用舊權限阻擋修繕。女主拿既有安全修復單讓杜淑雲完成驗收，知夏親自走過兩條可行撤離路線。她在修好出口旁以固定緊急對講呼叫安全側值班點的淑雲，完成備援供電下的通話測試；另約好交接後以手機報平安，手機中斷時向已測試的固定通話點移動。",
          "timeline": "present",
          "hook": "這扇門，今天真的打得開。",
          "hook_type": "line",
          "conflict": "姐妹預備最後取證與撤場，發現老倉庫仍有人想用舊權限阻擋修繕。",
          "turn": "女主拿既有安全修復單讓杜淑雲完成驗收，知夏親自走過兩條可行撤離路線。她在修好出口旁以固定緊急對講呼叫安全側值班點的淑雲，完成備援供電下的通話測試；另約好交接後以手機報平安，手機中斷時向已測試的固定通話點移動。",
          "cliffhanger": {
            "type": "danger",
            "text": "叔父突然傳來書面要求：只准知夏送副本到場；訊息保留，不插入未登記角色發聲。"
          },
          "setups": [],
          "payoffs": [
            "m03",
            "m07",
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
            "zhitang",
            "zhixia",
            "shuyun"
          ],
          "locations": [
            "warehouse"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "修復11集已記錄的危險，不等火起才找出口。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "rescue",
              "text": "妹妹掌握現場路線，有能力自救與救別人。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "姐妹與淑雲知道修好的出口；叔父仍以為她們只能走舊門。姐妹和淑雲都知道兩種聯絡方式及手機失聯時的約定。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "修繕完成簽收與出口示意圖存入外部保管。固定對講與備援電源驗收完成；淑雲保管外側通話點，交接名單註明知夏預定位置。",
            "carry_forward": "評估會面風險，原件不會全部帶去。"
          },
          "closed_ending": false
        },
        {
          "number": 27,
          "title": "他要買一句原諒",
          "logline": "顧承川願意供出叔父，卻要求女主承諾不追究他的行為。她同意把供述交給調查者評估，拒絕私下保證免責，也不拿感情交換證據。",
          "timeline": "present",
          "hook": "我說對不起，妳就放過我？",
          "hook_type": "question",
          "conflict": "顧承川願意供出叔父，卻要求女主承諾不追究他的行為。",
          "turn": "她同意把供述交給調查者評估，拒絕私下保證免責，也不拿感情交換證據。",
          "cliffhanger": {
            "type": "reveal",
            "text": "他說叔父已準備最後一次倉庫交接。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "chengchuan",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "把合作與責任分開，拆掉情緒勒索。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "取得可供驗證的交接安排，而非只聽口供。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "未婚夫知道不能靠道歉洗白；女主得到新的會面風險。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "供述留完整紀錄，交接通知有來源可查。",
            "carry_forward": "女主必須拒絕把責任轉嫁給司機的提議。"
          },
          "closed_ending": false
        },
        {
          "number": 28,
          "title": "不用他的命換",
          "logline": "叔父提出讓司機承擔全部責任、歸還部分控制權的交易。女主拿分散證據反駁司機不可能單獨完成整套行為，明確拒絕保自己棄他人。",
          "timeline": "present",
          "hook": "要我安全，就得先害他？",
          "hook_type": "image",
          "conflict": "叔父提出讓司機承擔全部責任、歸還部分控制權的交易。",
          "turn": "女主拿分散證據反駁司機不可能單獨完成整套行為，明確拒絕保自己棄他人。",
          "cliffhanger": {
            "type": "danger",
            "text": "知夏傳來文字訊息：倉庫裡還有未撤出的工人。"
          },
          "setups": [],
          "payoffs": [
            "m08",
            "m09",
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
            "zhitang",
            "chongyue",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "保住一名容易被犧牲的證人。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "女主明說已有分散副本；叔父不再相信能只奪一箱解決，卻仍押注她未交到調查端、可逼她撤回。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第7–9日",
            "knowledge": "叔父已聽到分散保管的說法，但未見正式移交收據，仍以為可逼女主收回外部保管；他不知道每份保管的確切位置。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "拒絕交易與相關通信保存；安置名單不公開。",
            "carry_forward": "準備撤人，會面只處理可替代資料。"
          },
          "closed_ending": false
        },
        {
          "number": 29,
          "title": "最後的交接",
          "logline": "知夏到老倉庫交接已核對的副本，同時確認未撤工人；叔父要求改走舊門，將她手機封在會面桌的袋內，不再讓她以手機報平安。她按26集約定只交副本，先讓工人往已修好的安全動線集合；煙起後按事先走過的路前往固定通話點，暫時仍未與安全側接通。淑雲留在外側值班點，沒有跟進倉庫。",
          "timeline": "present",
          "hook": "他指定的門，正好最難出去。",
          "hook_type": "danger",
          "conflict": "知夏到老倉庫交接已核對的副本，同時確認未撤工人；叔父要求改走舊門，將她手機封在會面桌的袋內，不再讓她以手機報平安。",
          "turn": "她按26集約定只交副本，先讓工人往已修好的安全動線集合；煙起後按事先走過的路前往固定通話點，暫時仍未與安全側接通。淑雲留在外側值班點，沒有跟進倉庫。",
          "cliffhanger": {
            "type": "reveal",
            "text": "排風停了，走廊有第一縷煙。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "zhixia",
            "chongyue",
            "shuyun"
          ],
          "locations": [
            "warehouse"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "沒有把唯一證據帶進陷阱。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "提前移動人員，讓下一集救援有起點。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "第10日17:58，知夏在倉庫，知棠在倉區外部交接點等候。",
            "knowledge": "知夏知道路線異常；知棠在約定手機回報時間過後察覺失聯，尚不知道倉內新位置。",
            "character_state": "知棠無新傷；姐妹互信依該集行動累積。",
            "evidence": "副本與封袋手機留在會面桌；真正原件仍在保管端。固定對講在修好出口旁，知夏尚未抵達。",
            "carry_forward": "火勢初起，接30集困境不突然瞬移所有角色。"
          },
          "closed_ending": false
        },
        {
          "number": 30,
          "title": "這次火來得更早",
          "logline": "知棠等不到妹妹的手機回報，又接到安全側淑雲報告冒煙；前世恐懼使她想獨自衝回去，此刻妹妹尚未從固定通話點回覆。她先呼叫正式救援並讓許聞按既定安排保全資料，再以第26集交接名單確認妹妹最後已知位置；不把失聯期間的位置當成即時定位。",
          "timeline": "present",
          "hook": "這把火，我見過。",
          "hook_type": "reversal",
          "conflict": "知棠等不到妹妹的手機回報，又接到安全側淑雲報告冒煙；前世恐懼使她想獨自衝回去，此刻妹妹尚未從固定通話點回覆。",
          "turn": "她先呼叫正式救援並讓許聞按既定安排保全資料，再以第26集交接名單確認妹妹最後已知位置；不把失聯期間的位置當成即時定位。",
          "cliffhanger": {
            "type": "reversal",
            "text": "她發現熟悉的大門又被封住，但另一條路已修好。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            4,
            3,
            5,
            4,
            5
          ],
          "characters": [
            "zhitang",
            "xuwen",
            "zhixia",
            "shuyun"
          ],
          "locations": [
            "warehouse",
            "meeting"
          ],
          "theme": "選擇可信的人，比記得未來重要。",
          "lead_arc": "mixed",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "即時啟動救援，避免因恐懼延誤。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "以已完成的修繕取得不同於前世的生路。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "18:02告警；這段救援從多視角交錯呈現，不是每集順延三分鐘。",
            "knowledge": "女主確知重演風險；外部救援只掌握現場情報，不需要知道重生。",
            "character_state": "知夏仍在現場，知棠配合救援不獨闖；具體位置依本集。",
            "evidence": "淑雲由安全側電話告警；妹妹手機仍封在會面桌，最後已知位置來自交接名單，不是憑空恢復通話。",
            "carry_forward": "先把指揮和資料責任交出去，再進行安全範圍內撤離。"
          },
          "closed_ending": false
        }
      ]
    },
    {
      "number": 4,
      "title": "不用別人的命換勝利",
      "theme": "自主是能信任，也能追問。",
      "start_state": "火場與滅證威脅同時到來。",
      "end_state": "姐妹生還、舊案平反、各方責任有結果，重新共同經營。",
      "turn": "第一集剝奪權利的簽名，變成兩人知情自願的選擇。",
      "stakes": "生命、清白與未來合作方式",
      "question": "她能否同時救人、保住證據，且不重演控制？",
      "episodes": [
        {
          "number": 31,
          "title": "讓證據先出去",
          "logline": "現場急迫，叔父傳來文字，要求撤回外部交付才肯交出門控資訊。女主拒絕單點交換，許聞按24集的保管約定將相關資料交付調查，現場由救援與淑雲指揮撤離。",
          "timeline": "present",
          "hook": "救人，和交證據，一起做。",
          "hook_type": "line",
          "conflict": "現場急迫，叔父傳來文字，要求撤回外部交付才肯交出門控資訊。",
          "turn": "女主拒絕單點交換，許聞按24集的保管約定將相關資料交付調查，現場由救援與淑雲指揮撤離。",
          "cliffhanger": {
            "type": "reveal",
            "text": "叔父以為能關的那扇門，已經不控制所有人。"
          },
          "setups": [],
          "payoffs": [
            "m08",
            "m09"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "xuwen",
            "shuyun"
          ],
          "locations": [
            "warehouse",
            "meeting"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "證據按既定流程交付，不靠即興全網直播。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "rescue",
              "text": "把現場救人與外部查證分給不同專業者。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "18:02–18:04，與第30集並行：外部交付和救援啟動。",
            "knowledge": "觀眾與許聞已見資料正式交付；叔父只知道她聲稱有副本，尚未見已完成移交的收據，仍誤以為能以門控資訊逼她撤回。",
            "character_state": "知夏仍在現場，知棠配合救援不獨闖；具體位置依本集。",
            "evidence": "第24集是外部保管簽收，本集才依既定條件完成向調查端移交並取得收據；消防救援已到場。",
            "carry_forward": "女主只能按可安全接近的路線協助，不指導危險入火。"
          },
          "closed_ending": false
        },
        {
          "number": 32,
          "title": "照著貨線走",
          "logline": "煙讓熟悉倉庫也失去方向，工人想回頭取私人物品。女主利用平日區域標記協助點名，讓專業救援按淑雲提供的已驗動線接人。",
          "timeline": "present",
          "hook": "以前運貨的路，今天先送人。",
          "hook_type": "question",
          "conflict": "煙讓熟悉倉庫也失去方向，工人想回頭取私人物品。",
          "turn": "女主利用平日區域標記協助點名，讓專業救援按淑雲提供的已驗動線接人。",
          "cliffhanger": {
            "type": "danger",
            "text": "最後一名未點到的，是知夏。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "zhitang",
            "shuyun",
            "qide"
          ],
          "locations": [
            "warehouse"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "第一批人員確認離場而非只拍奔跑畫面。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "核對名單找到確切失聯者，避免漫無目的搜救。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "18:04–18:07，安全側點名與現場撤離。",
            "knowledge": "各組知道誰已出去、誰尚未確認，女主不獨闖濃煙。",
            "character_state": "知夏仍在現場，知棠配合救援不獨闖；具體位置依本集。",
            "evidence": "點名紙交給救援端，出口圖與現場一致。",
            "carry_forward": "知夏仍在可接近區域，下一集交代誰把她留住。"
          },
          "closed_ending": false
        },
        {
          "number": 33,
          "title": "他先走了",
          "logline": "顧承川想帶走帳箱，要求知夏替他拿落下的文件，自己先走。知夏拒絕替顧收拾落下的文件，讓他自行提走已抱著的副本箱。她帶工人抵達第26集測試過的固定緊急對講點，首次重新接通安全側淑雲，報出自己與顧的移動位置，由淑雲轉告已到場救援。",
          "timeline": "present",
          "hook": "他先走了，把人留在裡面。",
          "hook_type": "image",
          "conflict": "顧承川想帶走帳箱，要求知夏替他拿落下的文件，自己先走。",
          "turn": "知夏拒絕替顧收拾落下的文件，讓他自行提走已抱著的副本箱。她帶工人抵達第26集測試過的固定緊急對講點，首次重新接通安全側淑雲，報出自己與顧的移動位置，由淑雲轉告已到場救援。",
          "cliffhanger": {
            "type": "reversal",
            "text": "顧承川出去時，手上只有一箱誰都有副本的紙。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhixia",
            "chengchuan",
            "shuyun"
          ],
          "locations": [
            "warehouse"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "妹妹主動拒絕被再次支配。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "把人的位置交代清楚，證明救命比保帳箱優先。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "18:04–18:07，同時段另一側：知夏拒絕搬帳箱；淑雲始終在安全側以通訊引導。",
            "knowledge": "未婚夫自保行為被現場多人看見，無法靠一句悔意洗白。",
            "character_state": "知夏仍在現場，知棠配合救援不獨闖；具體位置依本集。",
            "evidence": "顧帶走副本箱，妹妹手機仍封在會面桌；知夏使用固定對講，淑雲在安全側接收位置並轉報專業救援。",
            "carry_forward": "叔父在安全外圍接到副本箱，仍押注外部移交可被停止；下一集以已完成移交的正式收據擊破最後僥倖。"
          },
          "closed_ending": false
        },
        {
          "number": 34,
          "title": "燒不掉的帳",
          "logline": "叔父在安全外圍接到副本箱，威脅連同現有文件一起毀掉，仍想逼女主撤回尚未見收據的外部移交。許聞亮出第31集已完成的調查端收據編號，與第24集分散保管簽收互相核對；女主指出這箱只是副本，即使毀掉，也不能取消已被獨立接收的證據。",
          "timeline": "present",
          "hook": "燒掉這箱，也燒不掉簽收。",
          "hook_type": "danger",
          "conflict": "叔父在安全外圍接到副本箱，威脅連同現有文件一起毀掉，仍想逼女主撤回尚未見收據的外部移交。",
          "turn": "許聞亮出第31集已完成的調查端收據編號，與第24集分散保管簽收互相核對；女主指出這箱只是副本，即使毀掉，也不能取消已被獨立接收的證據。",
          "cliffhanger": {
            "type": "danger",
            "text": "叔父最後一個談判籌碼失效，轉身想逃。"
          },
          "setups": [],
          "payoffs": [
            "m01",
            "m09"
          ],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "chongyue",
            "xuwen"
          ],
          "locations": [
            "warehouse"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "把第24集保管與第31集正式移交的收據並列，讓叔父確認移交已完成，不是女主虛張聲勢。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "讓救援不再受證據威脅綁住。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "18:07–18:09，安全外圍的滅證威脅失效。",
            "knowledge": "叔父終於見到正式移交憑據，不能再假設她可私下撤回；女主沒有臨時多出一個備份。",
            "character_state": "知夏仍在現場，知棠配合救援不獨闖；具體位置依本集。",
            "evidence": "來源、原件、副本鏈均能查，火場文件僅為副本。",
            "carry_forward": "接妹妹最後脫困，不以抓反派壓過救人。"
          },
          "closed_ending": false
        },
        {
          "number": 35,
          "title": "她知道另一扇門",
          "logline": "知夏在固定對講點旁看見出口內側倒落物，向安全側淑雲回報；知棠在外側聽到消息，一度以為路也失效。知夏指出第26集走過的備用出口，淑雲在固定對講中完成位置確認後交給專業救援接應；知夏離開通話點，跟隨救援人員撤離，不靠一支從未取回的手機沿路通話。",
          "timeline": "present",
          "hook": "姐，這條路我走過。",
          "hook_type": "reversal",
          "conflict": "知夏在固定對講點旁看見出口內側倒落物，向安全側淑雲回報；知棠在外側聽到消息，一度以為路也失效。",
          "turn": "知夏指出第26集走過的備用出口，淑雲在固定對講中完成位置確認後交給專業救援接應；知夏離開通話點，跟隨救援人員撤離，不靠一支從未取回的手機沿路通話。",
          "cliffhanger": {
            "type": "emotion",
            "text": "姐妹站到同一條警戒線外，知棠手機卻跳出叔父的文字：「只是意外。」不新增叔父聲音。"
          },
          "setups": [],
          "payoffs": [
            "m07"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "zhitang",
            "zhixia",
            "shuyun"
          ],
          "locations": [
            "warehouse"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "rescue",
              "text": "妹妹以自己的知識辨認安全動線。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "rescue",
              "text": "姐妹都活著離場，前世結果被實際改變。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "18:07–18:10，與第34集並行的最後脫困。",
            "knowledge": "姐妹知道彼此平安；救援接手現場，沒有返回火場追人。",
            "character_state": "知夏有輕微擦傷和煙霧刺激，接受評估並休息；其他主角生還。",
            "evidence": "固定對講的定位已交接救援；封袋手機留待現場採證。知棠收到叔父文字並保存，妹妹先接受傷勢與煙霧刺激評估。",
            "carry_forward": "現場鑑識與帳務證據分開取得，再交叉印證。"
          },
          "closed_ending": false
        },
        {
          "number": 36,
          "title": "意外需要證據",
          "logline": "叔父聲稱停電與起火都是老舊設備造成，女主不能用前世記憶指控今生。現場通信、門控變動紀錄與既有侵吞動機交由調查者比對，形成可追查的新案線。",
          "timeline": "present",
          "hook": "你說是意外，時間卻對不上。",
          "hook_type": "line",
          "conflict": "叔父聲稱停電與起火都是老舊設備造成，女主不能用前世記憶指控今生。",
          "turn": "現場通信、門控變動紀錄與既有侵吞動機交由調查者比對，形成可追查的新案線。",
          "cliffhanger": {
            "type": "reveal",
            "text": "他準備離場，卻被要求留下接受調查。"
          },
          "setups": [],
          "payoffs": [
            "m08"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "chongyue",
            "xuwen"
          ],
          "locations": [
            "warehouse",
            "meeting"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "保全當晚現場紀錄而非事後補造。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "讓母親舊案與今夜事件依獨立證據互相印證。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "18:10後外圍移交，先保存紀錄，不當場完成鑑識。",
            "knowledge": "調查者取得證據，公眾只知事件待查，不直接宣判。",
            "character_state": "知夏有輕微擦傷和煙霧刺激，接受評估並休息；其他主角生還。",
            "evidence": "原始通信及救援紀錄由適格單位保存；知夏治療後休息。",
            "carry_forward": "第37集是依法調查控制，不是女主私刑。"
          },
          "closed_ending": false
        },
        {
          "number": 37,
          "title": "不能再替你簽",
          "logline": "叔父最後要求女主替他說明一切只是家族誤會，以母親名聲相逼。她拒絕代答，把完整資料與持有人交由調查程序，叔父失去以家族身份支配她的能力。",
          "timeline": "present",
          "hook": "你的名字，這次你自己負責。",
          "hook_type": "question",
          "conflict": "叔父最後要求女主替他說明一切只是家族誤會，以母親名聲相逼。",
          "turn": "她拒絕代答，把完整資料與持有人交由調查程序，叔父失去以家族身份支配她的能力。",
          "cliffhanger": {
            "type": "choice",
            "text": "許聞收到顧承川透過書面提出的交易：供出叔父，換取免責；顧仍分開接受詢問，不在此場發聲。"
          },
          "setups": [],
          "payoffs": [],
          "tension": [
            4,
            3,
            5,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "chongyue",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "女主不再為權威承擔不屬於自己的說法。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "相關人被分開詢問，串供與私下交易空間縮小。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "倉庫事件後數日，分開調查與詢問。",
            "knowledge": "各方知道後續由調查與司法判斷，不由女主決定刑責。",
            "character_state": "知夏有輕微擦傷和煙霧刺激，接受評估並休息；其他主角生還。",
            "evidence": "資料交接收據與合法程序留存，沒有事後刪去不利部分。",
            "carry_forward": "處理未婚夫自己的行為，避免一句協助調查就洗白。"
          },
          "closed_ending": false
        },
        {
          "number": 38,
          "title": "原諒不是免責",
          "logline": "顧承川向女主道歉並要求她公開稱他也是受害者。她只確認已驗證的合作，不替他否認轉移資料與棄人行為；許聞把有利與不利內容一起交付。",
          "timeline": "present",
          "hook": "你能說真話，不能買無罪。",
          "hook_type": "image",
          "conflict": "顧承川向女主道歉並要求她公開稱他也是受害者。",
          "turn": "她只確認已驗證的合作，不替他否認轉移資料與棄人行為；許聞把有利與不利內容一起交付。",
          "cliffhanger": {
            "type": "emotion",
            "text": "女主把婚禮合照收進箱底，第一次不需要撕毀它。"
          },
          "setups": [],
          "payoffs": [
            "m08"
          ],
          "tension": [
            5,
            3,
            4,
            3,
            5
          ],
          "characters": [
            "zhitang",
            "chengchuan",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "把坦白與免責的界線說清。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "未婚夫的責任不再由女主的愛恨決定。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "倉庫事件後數日，顧承川要求交換免責。",
            "knowledge": "公眾可知查核過程，具體刑責待時間推進後交代。",
            "character_state": "知夏有輕微擦傷和煙霧刺激，接受評估並休息；其他主角生還。",
            "evidence": "完整供述持續留存；妹妹傷勢恢復但仍有疤痕。",
            "carry_forward": "時間跳轉數月，交代案件結果與公司現實代價。"
          },
          "closed_ending": false
        },
        {
          "number": 39,
          "title": "把名字還給她",
          "logline": "數月後調查與審理確認叔父侵吞及相關火災責任，顧承川按各自行為承擔結果；公司仍有虧損待填。姐妹以公開查核摘要說清母親曾阻止的事，同時公布重整範圍，不以勝利抹掉員工損失。",
          "timeline": "present",
          "hook": "母親的名字，回到門上了。",
          "hook_type": "danger",
          "conflict": "數月後調查與審理確認叔父侵吞及相關火災責任，顧承川按各自行為承擔結果；公司仍有虧損待填。",
          "turn": "姐妹以公開查核摘要說清母親曾阻止的事，同時公布重整範圍，不以勝利抹掉員工損失。",
          "cliffhanger": {
            "type": "reveal",
            "text": "新的經營協議留了兩個簽名位置。"
          },
          "setups": [],
          "payoffs": [
            "m10"
          ],
          "tension": [
            4,
            2,
            4,
            3,
            4
          ],
          "characters": [
            "zhitang",
            "zhixia",
            "qide"
          ],
          "locations": [
            "depot"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "母親得到有依據的平反，反派付出法律與職位代價。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "public_vindication",
              "text": "公司承認尚待修復的損失，員工能查新的承諾。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "數月後，調查及審理有結果",
            "knowledge": "眾人知道母親並非失職釀災，姐妹仍要面對營運挑戰而非新懸案。",
            "character_state": "知夏恢復、留輕微疤痕；姐妹獨立決策又能合作。",
            "evidence": "平反文件、判決摘要與重整計畫留存；母親舊表被知棠戴著。",
            "carry_forward": "最後一集回收簽字意象，只處理共同決策的情感結果。"
          },
          "closed_ending": false
        },
        {
          "number": 40,
          "title": "這次一起簽",
          "logline": "知夏擔心再次代姐姐保管秘密會重演誤解，知棠也不再想靠一個人控制全部。她們讀完權責、查閱與退出條款，選擇在彼此知情的前提下簽名；母親的表放在桌中央。",
          "timeline": "present",
          "hook": "這次，我們一起簽。",
          "hook_type": "reversal",
          "conflict": "知夏擔心再次代姐姐保管秘密會重演誤解，知棠也不再想靠一個人控制全部。",
          "turn": "她們讀完權責、查閱與退出條款，選擇在彼此知情的前提下簽名；母親的表放在桌中央。",
          "cliffhanger": {
            "type": "reversal",
            "text": "兩人一同落筆。知棠：這次，我們一起簽。"
          },
          "setups": [],
          "payoffs": [
            "m10"
          ],
          "tension": [
            4,
            3,
            4,
            5,
            5
          ],
          "characters": [
            "zhitang",
            "zhixia",
            "xuwen"
          ],
          "locations": [
            "meeting"
          ],
          "theme": "自主是能信任，也能追問。",
          "lead_arc": "wins",
          "satisfaction": [
            {
              "beat": "opening",
              "type": "reversal",
              "text": "妹妹有權提問並修改條款，不只是被賞賜一個位置。",
              "planned_seconds": 22
            },
            {
              "beat": "second_half",
              "type": "reversal",
              "text": "最初象徵剝奪的簽名，變成自願而可查的合作。",
              "planned_seconds": 118
            }
          ],
          "state": {
            "time": "數月後，重整協議簽署日",
            "knowledge": "所有主要秘密與案件已交代，彼此信任不再依靠隱瞞。",
            "character_state": "知夏恢復、留輕微疤痕；姐妹獨立決策又能合作。",
            "evidence": "兩份相同協議各自持有；不再出現反派電話或新火災。",
            "carry_forward": "主線完結，停在兩人簽完後的相視，不接下集預告。"
          },
          "closed_ending": true
        }
      ]
    }
  ],
  "packaging": {
    "titles": [
      "重生回婚禮當天，我撕了股權書，害死我的人卻急了",
      "前世他們拿走我的公司，這次我要他們親手交出證據",
      "她沒有逃婚，她從婚禮開始清算所有背叛者"
    ],
    "description": "她以為婚禮是一段人生的開始，上一世卻在那張授權書上交出了自己的未來。再次睜眼，沈知棠回到簽字前。她保住文件、找回被辭退的司機，也查到妹妹不願說出口的秘密。當家族最值得信任的人開始阻止查帳，她必須選擇：只救自己，還是連被犧牲的人一起帶出去？\n原創 AI 漫劇《喜宴未散，清算開始》四十集完整故事，約兩小時。架空人物與企業；繁中配音、五語字幕於成片完成後提供。",
    "tags": [
      "漫劇",
      "AI漫劇",
      "一口氣看完",
      "重生復仇",
      "女主逆襲",
      "姐妹",
      "喜宴未散清算開始"
    ],
    "thumbnail_variants": [
      {
        "id": "A",
        "headline": "這次不簽",
        "composition": "左側知棠直視鏡頭，前景斷開的授權頁，右側未婚夫笑容凝住；象牙白與深藍，文字避開臉。",
        "episode": 1,
        "scene": "婚宴撕掉未簽授權頁",
        "promise": "前三十秒確實拒簽，並開始索取完整文件。"
      },
      {
        "id": "B",
        "headline": "附件有鬼",
        "composition": "知棠指向附件頁碼，稽核員藍色筆圈住授權範圍，後方金色領帶夾只露一角。",
        "episode": 3,
        "scene": "會談室核對附件",
        "promise": "第3集解釋具體授權風險，而非泛指全家有罪。"
      },
      {
        "id": "C",
        "headline": "婚禮變清算",
        "composition": "婚宴花牆前女主站立，叔父與未婚夫坐著，文件位於三人之間；不畫火場犧牲者。",
        "episode": 2,
        "scene": "公開詢問文件用途",
        "promise": "婚宴開始追問，完整清算在全片逐步完成。"
      }
    ],
    "audience": "喜歡女主復仇與家族懸念的成年華語觀眾；情感重心為姐妹、信任與自主，不以戀愛取代成長。",
    "visual_identity": "女主銀色方表貫穿；未婚夫金色領帶夾；妹妹銅髮夾。冷白婚宴、灰橘倉區、暖灰尾聲形成三段視覺，不為炫技新增世界。",
    "music": "婚宴鋼琴在撕紙時停掉；查帳用低脈衝，重要證據句留乾聲；火場減少煽情旋律以保留通訊可辨；最後回到簡單雙音鋼琴。",
    "release_order": 1,
    "pinned_comment": "如果重新選一次，你會先追究背叛的人，還是先找回那個沒聽完的解釋？哪個伏筆讓你改變了對知夏的看法？"
  },
  "continuity_notes": [
    "前世僅在第1集開場及第5、15集短閃回出現，不另用整集重述。第5、15集只演知棠當時親眼所見、親耳所聞；第25集只在當前會談中由知棠內心回讀，不另重播火場，也不演她無法知道的前世電話另一端。",
    "「股權書」為標題口語稱呼；劇內正確使用表決權委託、授權附件，拒簽不等於撤銷一切既有文件。",
    "叔父20集只評論眼前查帳辦法；只有女主知道重生，反派沒有知曉前世的台詞。",
    "29集原定交接為副本及撤場協調，有安全安排；對手新增火災仍形成危險，但女主不是主動送唯一證據入火。",
    "31集交付是24集已完成保管的執行，不是火起才突然備份。",
    "35集脫困依靠11、26集修繕與專業救援，知夏受傷狀態沿用到38集。",
    "母親只透過錄音與紀錄出場；同基礎聲音角色需正式試聽後確認區別，尚未試聽。",
    "所有法務與調查描寫為架空敘事，不給操作性法律建議；不宣稱看片可自行處理真實案件。",
    "火場通訊鏈：第11集列入修繕，第26集驗收固定對講與備援供電；第29集妹妹手機封在會面桌，第30集由外側淑雲告警，第33集妹妹才在固定點恢復聯絡，第35集交由救援帶離後不再遠端通話。",
    "叔父第28集已聽過副本說法，第31集觀眾看見正式移交，第34集叔父才看到可核對的完成收據。反應由懷疑、企圖撤回到最後失敗，不重複第一次得知備份。",
    "第6、12、13、26、35、37集標明不在場角色的訊息為文字，不臨時加發聲角色。"
  ]
};
