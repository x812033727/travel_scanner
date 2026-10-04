import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { setPauseBeats, STORY_VOICE_STYLE } from "../../../tools/video/automation/register.mjs";
import { slidesPresetFor, resolveLook } from "../../../tools/video/core/drama.mjs";
import { estimateTimeline, chapterList, spokenUnits, speechHash } from "../../../tools/video/core/timeline.mjs";
import { slideStates, cadenceSummary, cadenceProblems, illustrationShare } from "../../../tools/video/core/cadence.mjs";
import { shotPrompt } from "../../../tools/video/media/keyframes.mjs";
const dir = new URL("./", import.meta.url);
const initialIds = ["6q3t","2ery","tcf7","bai9","fmme","zabm"];
const ids = readFileSync(new URL("line-ids.txt",dir),"utf8").trim().split(/\s+/);
const newIds = ids.filter(id=>!initialIds.includes(id));
let nextId=0, shotIndex=0;
const cameras=["push in","drift","pull out","pan left","tilt down","pan right","tilt up"];
const guards=[
"Core action fits the middle 32%. All prop faces are blank; no text, signs, logos or symbols.",
"Subjects stay centered. Every surface is unmarked; no letters, numerals, labels, signage or emblems.",
"Hands and figures fit the centre strip. Plain items lack print, writing, inscriptions or marks.",
"Gesture within the middle 32%. Bare objects carry no glyphs, captions, typography, stamps, tags or insignia."
];
const base = {
  "schema_version": 1,
  "slug": "ai-term-embedding",
  "format": "slides",
  "category": "ai-terms",
  "source_guide": "ai-term-embedding",
  "target_minutes": [
    8,
    12
  ],
  "voice": {
    "provider": "gemini",
    "name": "Sulafat",
    "style": "Relaxed, conversational tech explainer talking to a friend, in Taiwan Mandarin with a natural Taiwanese accent. Natural rise and fall in intonation, light emphasis on key words, never flat or like reading a script. Medium-brisk pace."
  },
  "youtube": {
    "category_id": 28,
    "made_for_kids": false,
    "default_language": "zh-TW",
    "title": "嵌入向量是什麼？搜尋第一名，為什麼還不能當答案｜AI 名詞十分鐘",
    "description": "理解內容表示、相似分數與必要條件的差別。用一份明示人工座標的離線示意，練習回讀搜尋結果的原文。",
    "tags": [
      "嵌入向量",
      "Embedding",
      "向量嵌入",
      "語意搜尋",
      "AI 名詞"
    ],
    "video_id": null
  },
  "thumbnail": {
    "template": "thumb",
    "data": {
      "headline": "第一名，門卻關著",
      "tag": "嵌入向量"
    }
  },
  "subtitles": {
    "burn_in": false
  },
  "sources": [
    {
      "title": "Google Embeddings",
      "url": "https://developers.google.com/machine-learning/crash-course/embeddings",
      "checked_on": "2026-10-04"
    },
    {
      "title": "Google Embedding space",
      "url": "https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space",
      "checked_on": "2026-10-04"
    },
    {
      "title": "Google Obtaining embeddings",
      "url": "https://developers.google.com/machine-learning/crash-course/embeddings/obtaining-embeddings",
      "checked_on": "2026-10-04"
    },
    {
      "title": "Sentence Transformers Semantic Textual Similarity",
      "url": "https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html",
      "checked_on": "2026-10-04"
    },
    {
      "title": "Sentence Transformers Semantic Search",
      "url": "https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html",
      "checked_on": "2026-10-04"
    },
    {
      "title": "Sentence-BERT original research",
      "url": "https://arxiv.org/html/1908.10084v1",
      "checked_on": "2026-10-04"
    },
    {
      "title": "Mokaair 嵌入向量",
      "url": "https://mokaair.com/zh-TW/life/ai-term-embedding",
      "checked_on": "2026-10-04"
    }
  ],
  "scenes": [
    {
      "id": "draft-hook",
      "chapter": "第一名，門卻關著",
      "template": "title",
      "data": {
        "title": "第一名，門卻關著",
        "subtitle": "人工座標示意，非模型實測"
      },
      "lines": [
        {
          "id": "6q3t",
          "text": "搜尋第一名就在眼前，可是門鎖著。"
        }
      ]
    },
    {
      "id": "draft-representation",
      "chapter": "內容怎麼變成表示",
      "template": "title",
      "data": {
        "title": "內容怎麼變成表示"
      },
      "lines": [
        {
          "id": "2ery",
          "text": "那些數字，怎麼把內容放在一起？"
        }
      ]
    },
    {
      "id": "draft-similarity",
      "chapter": "分數比的是什麼",
      "template": "title",
      "data": {
        "title": "分數比的是什麼"
      },
      "lines": [
        {
          "id": "tcf7",
          "text": "一組數字很接近，到底是在比什麼？"
        }
      ]
    },
    {
      "id": "draft-demo",
      "chapter": "重跑排序，回讀原文",
      "template": "title",
      "data": {
        "title": "重跑排序，回讀原文"
      },
      "lines": [
        {
          "id": "bai9",
          "text": "前兩名都不能去，還能找到哪一筆？"
        }
      ]
    },
    {
      "id": "draft-compatible",
      "chapter": "同維度還要相容",
      "template": "title",
      "data": {
        "title": "同維度還要相容"
      },
      "lines": [
        {
          "id": "fmme",
          "text": "換一套表示，舊數字還能直接照用嗎？"
        }
      ]
    },
    {
      "id": "draft-conditions",
      "chapter": "條件圈出來，未知留下來",
      "template": "title",
      "data": {
        "title": "條件圈出來，未知留下來"
      },
      "lines": [
        {
          "id": "zabm",
          "text": "相近幫你找到候選，條件還得有證據。"
        }
      ]
    }
  ]
};
base.youtube.title="嵌入向量是什麼？搜尋第一名，為什麼還不能當答案｜AI 名詞";
base.youtube.description="嵌入向量如何表示內容，為什麼最高相似分數不能替你核對條件？\n給用過搜尋、想知道第一名能不能直接採用的一般讀者。\n用作者手填座標的六筆虛構活動作離線數學示範，分開表示、比較、候選與原文條件。沒有實測任何模型；不把玩具分數當正確率。回讀第一名原文，圈出必要條件，缺資料就保留待確認。";
base.voice.style=STORY_VOICE_STYLE;
base.look={preset:slidesPresetFor(base.slug)};
base.assets=[{path:"apps/web/public/guides/ai-term-embedding/diagram-1.svg",source:"Mokaair original embedding guide diagram",license:"© Mokaair"}];
base.thumbnail.data={tag:"嵌入向量",headline:"第一名，門卻關著",sub:"相近就能相信？",shot:"closed-workshop"};
const chapters = [
  {
    "title": "第一名，門卻關著",
    "scenes": [
      {
        "id": "closed-door-hook",
        "template": "title",
        "data": {
          "title": "第一名，門卻關著",
          "subtitle": "人工座標示意，非模型實測",
          "tag": "嵌入向量"
        },
        "text": [
          {
            "id": "6q3t",
            "text": "搜尋第一名就在眼前，可是門鎖著。"
          }
        ],
        "claims": [
          "c1",
          "c10"
        ],
        "reveal": false
      },
      {
        "id": "closed-workshop",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, a covered community workshop entrance on a rainy morning. Two neighbors pause together at a closed wooden doorway; the simple metal latch is the focus. Overcast daylight enters from the walkway."
        },
        "text": [
          "先看同一份清單，把相似分數和必要條件分開檢查。"
        ],
        "claims": [
          "c1",
          "c17"
        ]
      },
      {
        "id": "toy-disclosure",
        "template": "big",
        "data": {
          "text": "人工座標示意",
          "sub": "非模型實測",
          "kicker": "原創活動與數值"
        },
        "text": [
          "這些活動和座標，都是我手填、沒有模型參與的示意資料。"
        ],
        "claims": [
          "c1",
          "c10",
          "c19"
        ],
        "reveal": false
      },
      {
        "id": "wet-shoe-pause",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the covered passage in the rain, morning. A neighbor lifts a damp shoe beside the threshold; water beads on its rubber sole. Reflected daylight from the wet pavement."
        },
        "text": [
          "真正跑的是離線計算，沒有請模型找活動。"
        ],
        "claims": [
          "c10"
        ]
      },
      {
        "id": "neighbors-compare",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the porch on an overcast morning. A neighbor points at an empty work seat while a companion watches, their hands together in the middle. Diffuse daylight from the courtyard."
        },
        "text": [
          "兩個鄰居今天想在室內做手作，也不想提前辦預約。"
        ],
        "claims": [
          "c1",
          "c11"
        ]
      },
      {
        "id": "empty-seat",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, a porch bench on a rainy morning. A visitor lays a plain cloth pouch on the empty seat, keeping the pouch centered. The covered edge receives gray daylight from the open walkway."
        },
        "text": [
          "室內、今天開放、免預約，是這次缺一不可的必要條件。"
        ],
        "claims": [
          "c1",
          "c11"
        ]
      },
      {
        "id": "need-three-conditions",
        "template": "steps",
        "data": {
          "title": "需求有條件",
          "steps": [
            {
              "title": "室內"
            },
            {
              "title": "今天開放"
            },
            {
              "title": "不需預約"
            }
          ]
        },
        "text": [
          "清單談的是室內活動，還要有資料支持今天能不能進去。",
          "今天有開也不夠，因為鄰居這次還希望不用提前辦預約。",
          "要採用結果，這些必要條件得一起有資料支持。"
        ],
        "claims": [
          "c11",
          "c21"
        ],
        "reveal": true
      },
      {
        "id": "expectation-first",
        "template": "shot",
        "data": {
          "prompt": "From behind, the workshop porch on a rainy morning. A visitor leans toward the shut entrance as if ready to enter; the doorway fills the middle. Soft weather light from outside."
        },
        "text": [
          "你以為，排在第一名就已經幫你挑好了。"
        ],
        "claims": [
          "c1",
          "c17"
        ]
      },
      {
        "id": "latch-reveal",
        "template": "shot",
        "data": {
          "prompt": "Extreme close-up, the workshop threshold on a wet morning. A hand rests below a closed metal latch without opening it; the fastened latch is centered. Overcast light falls in from the corridor."
        },
        "text": [
          "其實，這份示意清單的第一名，原文卻明確寫著今天休館。"
        ],
        "claims": [
          "c1",
          "c11",
          "c12"
        ]
      },
      {
        "id": "highest-but-closed",
        "template": "compare",
        "data": {
          "title": "第一名的兩件事",
          "left": {
            "heading": "餘弦分數",
            "points": [
              "1.0000",
              "人工向量計算"
            ]
          },
          "right": {
            "heading": "原文條件",
            "points": [
              "今天休館",
              "不能確認可參加"
            ]
          }
        },
        "text": [
          "在這六筆玩具資料裡，拼貼室的分數排最高，算出來是一。",
          "可是清單明說今天休館，分數沒有改掉這句話。"
        ],
        "claims": [
          "c11",
          "c12",
          "c16"
        ],
        "reveal": true
      },
      {
        "id": "material-but-no-class",
        "template": "shot",
        "data": {
          "prompt": "Low-angle shot, the covered workshop porch in the morning. An empty stool sits behind the closed doorway, with a folded cloth in focus. Daylight is reflected from the rain outside."
        },
        "text": [
          "就算材料看起來都準備齊了，門也沒有因此變成開放。"
        ],
        "claims": [
          "c1",
          "c17"
        ]
      },
      {
        "id": "reservation-seat",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the same covered entrance on a rainy morning. An attendant gestures toward an unused chair while a visitor waits nearby; the chair is centered. Overcast light enters from the open arcade."
        },
        "text": [
          "再看陶藝室，今天開放，卻只接已預約的人。"
        ],
        "claims": [
          "c1",
          "c11"
        ]
      },
      {
        "id": "missing-opening",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the covered passage in the morning. A visitor holds a smooth wooden block still above a cloth bag; the bare block is the focus. Daylight from the rainy walkway."
        },
        "text": [
          "木作室沒有寫今天有沒有開，也不能先當能去。"
        ],
        "claims": [
          "c11",
          "c14"
        ]
      },
      {
        "id": "three-known-statuses",
        "template": "table",
        "data": {
          "title": "回到便條",
          "columns": [
            "活動",
            "原文條件"
          ],
          "rows": [
            [
              "拼貼室",
              "今日休館"
            ],
            [
              "陶藝室",
              "需要預約"
            ],
            [
              "木作室",
              "今日未知"
            ]
          ]
        },
        "text": [
          "拼貼室的今日關閉，是這份清單明確寫下的排除條件。",
          "陶藝室需要事先預約，也和鄰居這次想直接參加的需求不同。",
          "木作室只是缺資訊，要留下待確認，不能補成開放。"
        ],
        "claims": [
          "c11",
          "c14"
        ],
        "reveal": true
      },
      {
        "id": "return-to-note",
        "template": "shot",
        "data": {
          "prompt": "Over-the-shoulder shot, the rainy porch in morning light. A neighbor holds a completely blank stiff card beside the closed doorway; the card is centered. Diffuse daylight from the courtyard."
        },
        "text": [
          "這裡先分清，主題相關和條件成立是兩回事。"
        ],
        "claims": [
          "c1",
          "c17",
          "c21"
        ]
      },
      {
        "id": "no-confidence-meter",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, the passage in the morning rain. A pair of visitors turn toward each other beside the closed workshop, holding a plain pouch between them. Overcast light enters along the covered walkway."
        },
        "text": [
          "搜尋排了順序，還沒有替你查過真實營業狀態。"
        ],
        "claims": [
          "c1",
          "c17",
          "c19"
        ]
      },
      {
        "id": "clear-role-first",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the porch in daylight. A person places a smooth small tile onto a bare ledge; the tile alone draws the eye. Reflected light from the wet pavement."
        },
        "text": [
          "要看懂這個落差，得先看它到底比較了什麼。"
        ],
        "claims": [
          "c1",
          "c6"
        ]
      },
      {
        "id": "first-chapter-question",
        "template": "big",
        "data": {
          "text": "內容怎麼變成數字？",
          "sub": "先看表示，再看條件"
        },
        "text": [
          {
            "id": "2ery",
            "text": "那些數字，怎麼把內容放在一起？"
          }
        ],
        "claims": [
          "c2"
        ],
        "reveal": false
      }
    ]
  },
  {
    "title": "內容怎麼變成表示",
    "scenes": [
      {
        "id": "embedding-representation",
        "template": "chapter",
        "data": {
          "number": "2",
          "title": "內容怎麼變成表示"
        },
        "text": [
          "嵌入先把一段內容，轉成一組數值的表示。"
        ],
        "claims": [
          "c2"
        ],
        "reveal": false
      },
      {
        "id": "market-materials",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, an outdoor craft market in late morning. Two shoppers compare a plain fabric roll held between them; the roll stays centered. Daylight falls through the awning from the open street."
        },
        "text": [
          "像走進材料市集，先辨認眼前東西有什麼關係。"
        ],
        "claims": [
          "c1",
          "c2"
        ]
      },
      {
        "id": "cloth-relationships",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a market stall in late morning. A hand touches the edge of a woven fabric sample laid at the center; rough threads catch light. Open sky light enters from the street."
        },
        "text": [
          "兩塊布名字不同，也可能適合相近的用途。"
        ],
        "claims": [
          "c1",
          "c20"
        ]
      },
      {
        "id": "basket-sorting",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, the market stall before noon. A vendor places a smooth ceramic cup in a woven basket; the cup is the focus. Sunlight is softened by the canopy."
        },
        "text": [
          "如果只比名字，一換說法，就可能找不到了。"
        ],
        "claims": [
          "c1",
          "c20"
        ]
      },
      {
        "id": "different-wording",
        "template": "compare",
        "data": {
          "title": "不同說法",
          "left": {
            "heading": "想找的內容",
            "points": [
              "雨天可以做手作嗎"
            ]
          },
          "right": {
            "heading": "便條說法",
            "points": [
              "室內創作活動"
            ]
          }
        },
        "text": [
          "雨天可以做手作嗎，和室內創作活動這兩個說法，用字不同。",
          "適合的表示可能把意思對上，實際效果還要測。"
        ],
        "claims": [
          "c2",
          "c20"
        ],
        "reveal": true
      },
      {
        "id": "task-shaped-materials",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the outdoor market at noon. A vendor offers a plain wooden spool to a shopper, their hands meeting at the center. Daylight from beyond the canopy."
        },
        "text": [
          "嵌入讓程式有一種方式，去比較內容的關係。"
        ],
        "claims": [
          "c2",
          "c20"
        ]
      },
      {
        "id": "one-bundle-focus",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a shaded market counter at noon. A customer holds a tied bundle of cloth still in both palms; its woven folds are centered. Reflected daylight from a nearby paved lane."
        },
        "text": [
          "在文字搜尋裡，常比較整句或一段文字的表示。"
        ],
        "claims": [
          "c2",
          "c3"
        ]
      },
      {
        "id": "not-characters-count",
        "template": "shot",
        "data": {
          "prompt": "From behind, the market lane at noon. A shopper bends toward a display of unmarked wooden utensils; a ladle is the focus. Light falls from the open sky."
        },
        "text": [
          "這一組數值，不是把句子裡的字數算出來。"
        ],
        "claims": [
          "c2",
          "c4"
        ]
      },
      {
        "id": "not-a-word-count",
        "template": "big",
        "data": {
          "text": "表示內容的關係",
          "sub": "不是句子長短"
        },
        "text": [
          "句子一樣長，也不能就說它們談的是同一件事。"
        ],
        "claims": [
          "c2",
          "c4"
        ],
        "reveal": false
      },
      {
        "id": "learned-not-labels",
        "template": "shot",
        "data": {
          "prompt": "Low-angle shot, an outdoor market aisle at noon. A craft worker adjusts a plain canvas awning with a partner watching; its cord is centered. Sunlight enters from the open end."
        },
        "text": [
          "真正的模型，會依訓練等方式形成內容表示。"
        ],
        "claims": [
          "c3"
        ]
      },
      {
        "id": "not-fixed-glossary",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a shaded market stand at noon. A hand smooths the crease of an unprinted cloth square; the fabric is the focus. Light from the bright lane."
        },
        "text": [
          "它不是先拿一本固定詞典，查出每句的座標。"
        ],
        "claims": [
          "c3",
          "c10"
        ]
      },
      {
        "id": "sentence-method-example",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the open market at noon. Two artisans hold separate blank fabric pieces and compare their edges, both hands centered. Soft daylight is filtered by the canopy."
        },
        "text": [
          "句子嵌入，是把句子分別編成表示的一種做法。"
        ],
        "claims": [
          "c3"
        ]
      },
      {
        "id": "architecture-scope",
        "template": "bullets",
        "data": {
          "title": "表示有不同方法",
          "items": [
            "詞與句段表示不同",
            "句子方法是一類",
            "不套用單一架構"
          ]
        },
        "text": [
          "一個詞在模型內的表示，和整句表示不是同一層。",
          "有代表研究讓各個句子分別編碼，再用相似度去比較。",
          "這是代表方法，不表示所有嵌入都用相同架構。"
        ],
        "claims": [
          "c2",
          "c3"
        ],
        "reveal": true
      },
      {
        "id": "task-changes-organizing",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, the market craft stand at noon. A vendor rearranges a plain wooden comb beside a cloth pouch; the comb is centered. Sunlight is diffused through the awning."
        },
        "text": [
          "模型在訓練時要學哪些關係，和它被設定的任務有關。"
        ],
        "claims": [
          "c3",
          "c5"
        ]
      },
      {
        "id": "same-items-other-uses",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, an outdoor market corner at midday. Two craftspeople examine a reed mat together; a folded edge fills the center. Natural daylight from above the courtyard."
        },
        "text": [
          "好比同樣的材料，為了不同用途，可以分得不同。"
        ],
        "claims": [
          "c1",
          "c5"
        ]
      },
      {
        "id": "metaphor-boundary",
        "template": "shot",
        "data": {
          "prompt": "Extreme close-up, a market stall at noon. Fingers hold a small reed loop over a plain tabletop; the loop is in the middle. Reflected sunlight enters from the walkway."
        },
        "text": [
          "擺材料只是比方，不是真正模型內部長這樣。"
        ],
        "claims": [
          "c1",
          "c10"
        ]
      },
      {
        "id": "representation-workflow",
        "template": "diagram",
        "data": {
          "svg": "apps/web/public/guides/ai-term-embedding/diagram-1.svg",
          "caption": "內容→相容表示→比較→取回原文"
        },
        "text": [
          "內容先成為表示，程式再比較，最後取回原文。"
        ],
        "claims": [
          "c2",
          "c4",
          "c7",
          "c22"
        ],
        "reveal": false
      },
      {
        "id": "query-also-represented",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the outdoor market just after noon. A customer offers a plain fabric swatch for an artisan to inspect; both people remain centered. Daylight from the open aisle."
        },
        "text": [
          "你問的問題，也要變成能跟資料比較的表示。"
        ],
        "claims": [
          "c2",
          "c7"
        ]
      },
      {
        "id": "compare-is-separate",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a market work surface at noon. A hand sets a smooth seed-shaped bead beside a woven strip; the bead is the focus. Light from the sky beyond the awning."
        },
        "text": [
          "接著程式才算分數，把資料排成候選順序。"
        ],
        "claims": [
          "c4",
          "c6"
        ]
      },
      {
        "id": "use-result-separate",
        "template": "shot",
        "data": {
          "prompt": "From behind, a sunny market lane at noon. A buyer pauses beside an unused stool with a plain basket at the center. Sunlight arrives from the open street."
        },
        "text": [
          "應用程式要怎麼用這些候選，是後面的一步。"
        ],
        "claims": [
          "c4",
          "c17"
        ]
      },
      {
        "id": "representation-not-answer",
        "template": "steps",
        "data": {
          "title": "工作分開看",
          "steps": [
            {
              "title": "形成表示",
              "detail": "內容變成數值"
            },
            {
              "title": "比較表示",
              "detail": "算分數與取候選"
            },
            {
              "title": "使用候選",
              "detail": "讀原文與核對"
            }
          ]
        },
        "text": [
          "形成表示，先讓查詢和文件能夠在相容的表示空間裡比較。",
          "比較這些數值表示，算出相似分數，還沒有直接生成完整回答。",
          "怎麼使用候選，仍要看後面的原文和判斷步驟。"
        ],
        "claims": [
          "c2",
          "c4",
          "c7",
          "c17"
        ],
        "reveal": true
      },
      {
        "id": "no-answer-from-vector",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, an outdoor craft stall in early afternoon. A shopper waits while a vendor holds a plain ceramic cup at the center. Light from the sunny market lane."
        },
        "text": [
          "一組數值不會自己開口，也不會自己查今天開門。"
        ],
        "claims": [
          "c4",
          "c17"
        ]
      },
      {
        "id": "toy-skips-encoding",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the shaded market counter in early afternoon. Fingers set a completely blank tile flat on a reed mat; the tile is centered. Reflected daylight from the street."
        },
        "text": [
          "剛剛那份示範，刻意略過模型，直接手填數值。"
        ],
        "claims": [
          "c10"
        ]
      },
      {
        "id": "real-versus-toy",
        "template": "compare",
        "data": {
          "title": "這次實算的範圍",
          "left": {
            "heading": "真實嵌入",
            "points": [
              "先形成內容表示"
            ]
          },
          "right": {
            "heading": "本次玩具",
            "points": [
              "作者手填全部座標"
            ]
          }
        },
        "text": [
          "真實嵌入需要形成表示，這個步驟我們沒有執行。",
          "這次只算已寫好的向量，不能替模型的能力打分。"
        ],
        "claims": [
          "c3",
          "c10",
          "c19"
        ],
        "reveal": true
      },
      {
        "id": "do-not-overclaim",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, a craft market exit in early afternoon. Two neighbors inspect a plain cloth parcel together; the parcel sits between their hands. Daylight is softened by a stretched canopy."
        },
        "text": [
          "所以活動排在哪裡，只是這份人工數值的結果。"
        ],
        "claims": [
          "c10",
          "c12",
          "c19"
        ]
      },
      {
        "id": "second-chapter-question",
        "template": "big",
        "data": {
          "text": "相近，到底比什麼？",
          "sub": "先看相似度公式"
        },
        "text": [
          {
            "id": "tcf7",
            "text": "一組數字很接近，到底是在比什麼？"
          }
        ],
        "claims": [
          "c6"
        ],
        "reveal": false
      }
    ]
  },
  {
    "title": "分數比的是什麼",
    "scenes": [
      {
        "id": "similarity-not-conditions",
        "template": "chapter",
        "data": {
          "number": "3",
          "title": "分數比的是什麼"
        },
        "text": [
          "相似分數，是用選好的方法，比較那兩組表示。"
        ],
        "claims": [
          "c6"
        ],
        "reveal": false
      },
      {
        "id": "courtyard-dowels",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, a community courtyard in early afternoon. Two neighbors place a plain wooden dowel on a stone bench together; the dowel is centered. Daylight filters through a tree canopy."
        },
        "text": [
          "先到庭院裡，看兩根從同處伸出去的木棒。"
        ],
        "claims": [
          "c1",
          "c6"
        ]
      },
      {
        "id": "dowel-direction",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, the courtyard stone bench in afternoon. A hand rotates a smooth wooden rod near another rod; the turning end is the focus. Tree-filtered sunlight from above."
        },
        "text": [
          "木棒的方向相近，是一種能拿來比較的關係。"
        ],
        "claims": [
          "c1",
          "c6"
        ]
      },
      {
        "id": "angle-not-venue",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the courtyard in daylight. Fingers hold the rounded end of a wooden rod just above the bench; the end is centered. Dappled sunlight enters through leaves."
        },
        "text": [
          "這個動作只是比方，木棒沒有活動開放資訊。"
        ],
        "claims": [
          "c1",
          "c10",
          "c17"
        ]
      },
      {
        "id": "cosine-chosen",
        "template": "big",
        "data": {
          "text": "餘弦看方向",
          "sub": "本例選用的比較方法"
        },
        "text": [
          "我們這次的玩具程式，選用餘弦相似度來算。"
        ],
        "claims": [
          "c6",
          "c10"
        ],
        "reveal": false
      },
      {
        "id": "equal-direction",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, a shaded community courtyard after lunch. A person aligns an unmarked short rod beside a longer rod; the nearer end stays centered. Light from the open sky."
        },
        "text": [
          "它看方向的關係，會用向量長度把數值調整。"
        ],
        "claims": [
          "c6"
        ]
      },
      {
        "id": "not-a-longer-is-truer",
        "template": "shot",
        "data": {
          "prompt": "Low-angle shot, the courtyard bench in afternoon shade. A child looks at the end of a smooth tall reed held by an adult; the reed end is centered. Sky light enters from the open lawn."
        },
        "text": [
          "不能看哪根棒子長，就直接說哪個內容可信。"
        ],
        "claims": [
          "c1",
          "c5",
          "c16"
        ]
      },
      {
        "id": "cosine-formula",
        "template": "code",
        "data": {
          "code": "cosine = dot / (length_a * length_b)",
          "caption": "人工向量的比較公式"
        },
        "text": [
          "公式把點積除以長度的乘積，沒有查任何營業欄。"
        ],
        "claims": [
          "c6",
          "c10",
          "c17"
        ],
        "reveal": false
      },
      {
        "id": "direction-versus-origin",
        "template": "shot",
        "data": {
          "prompt": "Extreme close-up, a courtyard bench in afternoon light. A hand presses a smooth unmarked pebble at the base of a wooden dowel; the pebble is centered. Sunlight is diffused through the branches."
        },
        "text": [
          "這兩個數字，在本例沒有被命名成室內或開放。"
        ],
        "claims": [
          "c5",
          "c10"
        ]
      },
      {
        "id": "axes-interpretation",
        "template": "shot",
        "data": {
          "prompt": "From behind, the community courtyard in afternoon shade. A neighbor studies a plain woven mat laid across the bench; the folded mat stays centered. Natural sky light from the garden."
        },
        "text": [
          "真實模型的一個維度，也通常沒那麼容易命名。"
        ],
        "claims": [
          "c5"
        ]
      },
      {
        "id": "not-confidence-axis",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a courtyard seat in afternoon. Fingers move an unmarked wooden slider along a bare groove; the slider is the focus. Soft sunlight falls from the open lawn."
        },
        "text": [
          "數值變大，不能就擅自把那一維叫做可信度。"
        ],
        "claims": [
          "c5"
        ]
      },
      {
        "id": "axis-careful",
        "template": "bullets",
        "data": {
          "title": "別先替維度取名",
          "items": [
            "整體表示共同作用",
            "先看任務與方法",
            "不能自己命名可信度"
          ]
        },
        "text": [
          "通常是整組數值表示共同起作用，不能只靠直覺猜一個軸。",
          "要了解模型學了哪些關係，得看它的任務和方法。",
          "如果沒有分析證據，就不能把一個座標當信心開關。"
        ],
        "claims": [
          "c3",
          "c5"
        ],
        "reveal": true
      },
      {
        "id": "metric-varies",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, a shaded courtyard in mid-afternoon. Two adults examine a coiled rope together, one holding its end in the middle. Light from the open sky."
        },
        "text": [
          "比較也不只一種，有的用內積，有的用距離。"
        ],
        "claims": [
          "c6"
        ]
      },
      {
        "id": "compatible-metric",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, a garden bench in mid-afternoon. A person lays a plain rope loop beside a smooth wooden rod, the loop centered. Daylight filters through the leaves."
        },
        "text": [
          "選哪種相似度比較方法，得和表示的設計、設定一起配合。"
        ],
        "claims": [
          "c6",
          "c9"
        ]
      },
      {
        "id": "score-context",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the courtyard in afternoon shade. A neighbor turns a bare wooden strip toward a companion for inspection; both hands are centered. Daylight arrives from the lawn."
        },
        "text": [
          "換一個方法，原來那個分數，意思也不能照搬。"
        ],
        "claims": [
          "c6",
          "c9"
        ]
      },
      {
        "id": "near-one-not-probability",
        "template": "big",
        "data": {
          "text": "0.9949 ≠ 99.49%正確",
          "sub": "人工toy數值，非模型實測"
        },
        "text": [
          "這個接近一的玩具分數，不是答對的機率。"
        ],
        "claims": [
          "c12",
          "c16"
        ],
        "reveal": false
      },
      {
        "id": "score-does-not-prove",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a courtyard stone seat in afternoon. A hand rests an unmarked wooden block beside a folded reed mat; the block alone draws the eye. Soft light comes through the tree canopy."
        },
        "text": [
          "因為這段程式比較的是向量，不是答案對不對。"
        ],
        "claims": [
          "c10",
          "c16",
          "c17"
        ]
      },
      {
        "id": "no-real-product-test",
        "template": "shot",
        "data": {
          "prompt": "From behind, the courtyard in afternoon daylight. An adult watches a child balance a plain reed hoop; the hoop is centered. Sky light enters from above the lawn."
        },
        "text": [
          "我沒有測產品，所以也不替別人的分數下結論。"
        ],
        "claims": [
          "c18",
          "c19"
        ]
      },
      {
        "id": "same-toy-score-different-condition",
        "template": "compare",
        "data": {
          "title": "分數與條件分開",
          "left": {
            "heading": "玩具比較",
            "points": [
              "只讀人工向量"
            ]
          },
          "right": {
            "heading": "條件檢查",
            "points": [
              "另讀今日開放等欄位"
            ]
          }
        },
        "text": [
          "玩具比較只讀數值，清單裡的開放欄沒有送進公式。",
          "條件檢查讀另一組欄位，兩個工作要各自看結果。"
        ],
        "claims": [
          "c10",
          "c15",
          "c17"
        ],
        "reveal": true
      },
      {
        "id": "lower-score-can-match",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, a courtyard shelter in afternoon shade. Two neighbors spread a plain folded paper shape between them; their hands stay centered. Daylight from the garden opening."
        },
        "text": [
          "紙藝桌分數不是第一名，卻可能有完整符合資料。"
        ],
        "claims": [
          "c1",
          "c11",
          "c12",
          "c13"
        ]
      },
      {
        "id": "do-not-throw-away-score",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a garden seat in afternoon light. A person steadies a smooth pebble on a woven pad; the pebble is centered. Light falls from the open sky."
        },
        "text": [
          "這不是叫你丟掉分數，而是看清它完成哪一步。"
        ],
        "claims": [
          "c17",
          "c21"
        ]
      },
      {
        "id": "third-chapter-question",
        "template": "big",
        "data": {
          "text": "候選怎麼回到條件？",
          "sub": "用同一份資料重跑"
        },
        "text": [
          {
            "id": "bai9",
            "text": "前兩名都不能去，還能找到哪一筆？"
          }
        ],
        "claims": [
          "c13"
        ],
        "reveal": false
      }
    ]
  },
  {
    "title": "重跑排序，回讀原文",
    "scenes": [
      {
        "id": "rerun-same-records",
        "template": "chapter",
        "data": {
          "number": "4",
          "title": "重跑排序，回讀原文"
        },
        "text": [
          "現在拿同一份六筆資料，分開看排序和條件。"
        ],
        "claims": [
          "c10",
          "c11"
        ],
        "reveal": false
      },
      {
        "id": "community-hall-review",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, a community hall at midday. Two neighbors inspect a plain folded paper shape together at the center. light enters from a large roof opening."
        },
        "text": [
          "兩個鄰居先把需求說清楚，再看清單原文。"
        ],
        "claims": [
          "c1",
          "c11"
        ]
      },
      {
        "id": "one-paper-object",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the hall at midday light. A hand holds a single plain folded paper form over a tabletop; its fold is the focus. Soft light from the skylight."
        },
        "text": [
          "我們只算手填數值，活動文字仍是判條件的依據。"
        ],
        "claims": [
          "c10",
          "c11"
        ]
      },
      {
        "id": "fixture-first-half",
        "template": "table",
        "data": {
          "title": "原創清單，上半",
          "columns": [
            "代號",
            "活動",
            "今日／預約"
          ],
          "rows": [
            [
              "N001",
              "室內拼貼",
              "休館／免預約"
            ],
            [
              "N002",
              "室內陶藝",
              "開放／需預約"
            ],
            [
              "N003",
              "室內紙藝",
              "開放／免預約"
            ]
          ]
        },
        "text": [
          "原文寫拼貼室今天關閉，所以現在不符合今日開放這個條件。",
          "陶藝室雖然今天有開，卻要求參加者已經預約，不能直接去。",
          "紙藝桌今天開放，不用預約，清單也寫在室內。"
        ],
        "claims": [
          "c11"
        ],
        "reveal": true
      },
      {
        "id": "one-clay-bowl",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the hall at midday. An adult offers a plain clay bowl for a neighbor to inspect, their hands together in the middle. Diffuse light from overhead glazing."
        },
        "text": [
          "陶藝那筆不是完全無關，只是少了這次要的條件。"
        ],
        "claims": [
          "c1",
          "c11",
          "c17"
        ]
      },
      {
        "id": "fixture-second-half",
        "template": "table",
        "data": {
          "title": "原創清單，下半",
          "columns": [
            "代號",
            "活動",
            "必要條件"
          ],
          "rows": [
            [
              "N004",
              "室內木作",
              "今日未知／免預約"
            ],
            [
              "N005",
              "河邊寫生",
              "戶外／免預約"
            ],
            [
              "N006",
              "器材維修公告",
              "活動條件未知"
            ]
          ]
        },
        "text": [
          "木作室的原文寫免預約，卻沒有任何資料支持它今天開放。",
          "河邊寫生今天舉行，可是清單明寫它是戶外活動。",
          "維修公告沒有這次需要的活動條件，還是未知。"
        ],
        "claims": [
          "c11",
          "c14"
        ],
        "reveal": true
      },
      {
        "id": "wood-block-wait",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, a hall work surface at midday. A person sets a smooth wooden block onto a plain cloth, with the block centered. light falls through the roof opening."
        },
        "text": [
          "明確缺一個必要條件，就不能先當它符合。"
        ],
        "claims": [
          "c11",
          "c14"
        ]
      },
      {
        "id": "read-before-run",
        "template": "shot",
        "data": {
          "prompt": "From behind, the hall at midday light. A neighbor bends toward an undecorated paper sculpture on a low table; the sculpture is centered. Roof light from above."
        },
        "text": [
          "先把這些原文分清，再看程式究竟把誰排在前面。"
        ],
        "claims": [
          "c11",
          "c12"
        ]
      },
      {
        "id": "rank-first-half",
        "template": "terminal",
        "data": {
          "title": "人工向量實算",
          "command": "python demo.py rank-first",
          "output": [
            "TOY: manual vectors; no model",
            "N001 1.0000 REJECT:closed_today",
            "N002 0.9949 REJECT:requires_reservation",
            "N004 0.9878 UNKNOWN:missing_condition"
          ],
          "ran_on": "2026-10-04",
          "tool_version": "Python 3.14.6"
        },
        "text": [
          "這是同一份作者手填的人工數值，程式先列出完整排序的前半。",
          "拼貼室雖然排在第一，可是明確條件檢查顯示它今天關閉。",
          "陶藝室雖然排在第二，明確條件檢查卻顯示它需要事先預約。",
          "木作室排第三，今日開放沒有資訊，還是未知。"
        ],
        "claims": [
          "c10",
          "c12",
          "c14"
        ],
        "reveal": true
      },
      {
        "id": "separate-rank-from-condition",
        "template": "shot",
        "data": {
          "prompt": "Extreme close-up, the hall at midday. Fingers press the edge of a plain cardboard tile beside a wooden block; the tile is the focus. Diffuse light from the roof."
        },
        "text": [
          "你看到同一行裡，分數和條件判定並排出現。"
        ],
        "claims": [
          "c10",
          "c12",
          "c14"
        ]
      },
      {
        "id": "paper-table-lower-rank",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, the community hall at midday. Two participants work together on a plain paper fold; their shared project fills the middle. light enters through the skylight."
        },
        "text": [
          "符合這次全部必要條件的紙藝桌，卻排在這些高分候選後面。"
        ],
        "claims": [
          "c1",
          "c11",
          "c12",
          "c13"
        ]
      },
      {
        "id": "rank-last-half",
        "template": "terminal",
        "data": {
          "title": "人工向量實算",
          "command": "python demo.py rank-last",
          "output": [
            "TOY: manual vectors; no model",
            "N003 0.9762 MATCH:explicit_conditions",
            "N005 0.3011 REJECT:not_indoor",
            "N006 -0.0995 UNKNOWN:missing_condition"
          ],
          "ran_on": "2026-10-04",
          "tool_version": "Python 3.14.6"
        },
        "text": [
          "排序後半還是同一份作者手填的人工資料，全程沒有使用模型。",
          "紙藝桌雖然排在第四，可是紀錄的明確欄位都符合這次需求。",
          "河邊寫生排在第五，原文明寫它是戶外，和這次室內需求不同。",
          "維修公告排最後，沒有條件資訊，也不能說符合。"
        ],
        "claims": [
          "c10",
          "c11",
          "c12",
          "c14"
        ],
        "reveal": true
      },
      {
        "id": "not-inferred-truth",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a hall activity table at midday. A neighbor steadies a plain folded paper piece with a fingertip; the crease is centered. Soft light falls from the roof opening."
        },
        "text": [
          "這個符合，只代表虛構紀錄的欄位支持了需求。"
        ],
        "claims": [
          "c14"
        ]
      },
      {
        "id": "candidate-setting",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the hall at midday light. A person places a plain fabric pouch in the middle while another watches nearby. Roof light illuminates the pouch and both hands."
        },
        "text": [
          "現在作者把候選限制成兩筆，這只是示範設定。"
        ],
        "claims": [
          "c1",
          "c13"
        ]
      },
      {
        "id": "top-two-check",
        "template": "terminal",
        "data": {
          "title": "人工向量實算",
          "command": "python demo.py top",
          "output": [
            "TOP_K: 2",
            "CANDIDATES: N001 N002",
            "ELIGIBLE: []"
          ],
          "ran_on": "2026-10-04",
          "tool_version": "Python 3.14.6"
        },
        "text": [
          "這份程式由作者設定只取前兩筆，並不是實際產品的通用建議值。",
          "前兩個候選是拼貼室和陶藝室，這個設定沒有把紙藝桌取進來。",
          "只檢查這兩筆，就沒有任何符合條件的結果。"
        ],
        "claims": [
          "c13",
          "c19"
        ],
        "reveal": true
      },
      {
        "id": "empty-result-explained",
        "template": "shot",
        "data": {
          "prompt": "Low-angle shot, the hall at midday. An unused seat sits beside a low activity table, with a plain paper fold in focus. light from the skylight."
        },
        "text": [
          "結果是空的，不表示原始清單一定沒有合用項目。"
        ],
        "claims": [
          "c13",
          "c21"
        ]
      },
      {
        "id": "expand-check-scope",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, the hall at midday. A hand unfolds one plain sheet into a broad simple shape; its centered fold is the focus. Roof light illuminates the work surface."
        },
        "text": [
          "所以另做一次對照，對完整六筆都檢查條件。"
        ],
        "claims": [
          "c10",
          "c13"
        ]
      },
      {
        "id": "all-records-check",
        "template": "terminal",
        "data": {
          "title": "人工向量實算",
          "command": "python demo.py all",
          "output": [
            "CHECK_SCOPE: ALL_6",
            "ELIGIBLE: ['N003']",
            "UNKNOWN: ['N004', 'N006']"
          ],
          "ran_on": "2026-10-04",
          "tool_version": "Python 3.14.6"
        },
        "text": [
          "這次條件檢查改看完整六筆，不只是剛才取出的前兩個候選。",
          "程式保留紙藝桌，因為紀錄中的必要條件有支持。",
          "木作室和維修公告仍是未知，缺資料沒有被補掉。"
        ],
        "claims": [
          "c13",
          "c14"
        ],
        "reveal": true
      },
      {
        "id": "exact-ranking-boundary",
        "template": "shot",
        "data": {
          "prompt": "From behind, the community hall at midday. A participant examines a plain clay vessel on an empty stool; the vessel is centered. Diffuse light comes through overhead glazing."
        },
        "text": [
          "這裡是精確全量排序，沒有測近似搜尋或資料庫。"
        ],
        "claims": [
          "c13",
          "c19"
        ]
      },
      {
        "id": "no-universal-fix",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the hall at midday light. A person lifts the end of a plain fabric strip from a low table; the edge is centered. Light from the roof opening."
        },
        "text": [
          "查更多候選可能有幫助，卻不能拿這例當通用解方。"
        ],
        "claims": [
          "c13",
          "c19",
          "c21"
        ]
      },
      {
        "id": "no-model-benchmark",
        "template": "big",
        "data": {
          "text": "只證明這份程式",
          "sub": "不是模型、向量庫或近似搜尋評測"
        },
        "text": [
          "這個排序是我手填數值安排的，不能替模型打分。"
        ],
        "claims": [
          "c10",
          "c19"
        ],
        "reveal": false
      },
      {
        "id": "same-vector-control",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the hall at midday. Two neighbors hold the same smooth wooden block between their palms for inspection; the block is centered. Roof light illuminates the shared action."
        },
        "text": [
          "還有一個對照，保持向量不動，只改今日開放欄。"
        ],
        "claims": [
          "c1",
          "c15"
        ]
      },
      {
        "id": "metadata-only-control",
        "template": "terminal",
        "data": {
          "title": "人工向量實算",
          "command": "python demo.py control",
          "output": [
            "COSINE: 1.0000 -> 1.0000",
            "CONDITION: MATCH -> REJECT"
          ],
          "ran_on": "2026-10-04",
          "tool_version": "Python 3.14.6"
        },
        "text": [
          "餘弦分數仍然同樣是一，因為我沒有改變作者手填的任何向量。",
          "條件卻從符合變拒絕，因為今日開放改成關閉。"
        ],
        "claims": [
          "c15",
          "c16"
        ],
        "reveal": true
      },
      {
        "id": "not-text-reencoding",
        "template": "shot",
        "data": {
          "prompt": "Extreme close-up, a hall tabletop at midday. A hand keeps a plain wooden block still beside an undecorated cloth; the block is centered. Diffuse light from overhead."
        },
        "text": [
          "這沒有把句子重新送進模型，也沒測否定句能力。"
        ],
        "claims": [
          "c15",
          "c19"
        ]
      },
      {
        "id": "article-at-example",
        "template": "cta",
        "data": {
          "title": "完整概念與圖解",
          "sub": "說明欄有對應文章"
        },
        "text": [
          "想把這些步驟對照著看，說明欄有完整文章。"
        ],
        "claims": [
          "c22"
        ],
        "reveal": false
      },
      {
        "id": "fourth-chapter-question",
        "template": "big",
        "data": {
          "text": "舊向量能直接搬嗎？",
          "sub": "還要看表示空間"
        },
        "text": [
          {
            "id": "fmme",
            "text": "換一套表示，舊數字還能直接照用嗎？"
          }
        ],
        "claims": [
          "c7",
          "c9"
        ],
        "reveal": false
      }
    ]
  },
  {
    "title": "同維度還要相容",
    "scenes": [
      {
        "id": "compatible-space",
        "template": "chapter",
        "data": {
          "number": "5",
          "title": "同維度還要相容"
        },
        "text": [
          "舊向量能不能直接用，得先看表示方式是否相容。"
        ],
        "claims": [
          "c7",
          "c9"
        ],
        "reveal": false
      },
      {
        "id": "tailor-patterns",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, a sewing alcove during the day. Two tailors hold a plain folded fabric panel between them for inspection; its edge is centered. Light enters through a high side window."
        },
        "text": [
          "走進裁縫工坊，同樣一塊布，可能按不同紙樣裁。"
        ],
        "claims": [
          "c1",
          "c7"
        ]
      },
      {
        "id": "different-origins",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, a sewing workbench in daytime. A hand places an unprinted paper shape beside a different blank shape; their touching edge is centered. Light falls from the side window."
        },
        "text": [
          "好比兩張起點不同的圖，不能直接把位置混在一起。"
        ],
        "claims": [
          "c1",
          "c7"
        ]
      },
      {
        "id": "length-is-not-map",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the sewing alcove in daytime. A person holds a smooth measuring strip without graduations over a cloth seam; the seam is centered. Light enters from a narrow window."
        },
        "text": [
          "就算都有同樣數量的座標，也不表示在同一張圖上。"
        ],
        "claims": [
          "c1",
          "c7"
        ]
      },
      {
        "id": "same-dimension-not-space",
        "template": "compare",
        "data": {
          "title": "別只看維度數",
          "left": {
            "heading": "同維度",
            "points": [
              "數值個數相同"
            ]
          },
          "right": {
            "heading": "相容空間",
            "points": [
              "表示關係能配合比較"
            ]
          }
        },
        "text": [
          "維度相同，只說數值個數一樣，還沒證明表示能混用。",
          "要比較內容，查詢和資料得使用相容的表示方式。"
        ],
        "claims": [
          "c7"
        ],
        "reveal": true
      },
      {
        "id": "new-map-old-data",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the sewing alcove in daytime. A tailor steadies a plain paper pattern as an apprentice compares a cloth edge; both hands are centered. Side-window light falls across the seam."
        },
        "text": [
          "新模型的問題向量，不能隨手配上舊模型的資料。"
        ],
        "claims": [
          "c7",
          "c9"
        ]
      },
      {
        "id": "number-still-computable",
        "template": "shot",
        "data": {
          "prompt": "Extreme close-up, a sewing bench in daytime. Fingers hold a plain metal thimble next to a folded fabric edge; the thimble is centered. Light from the high window."
        },
        "text": [
          "它可能仍算得出一個數字，卻不代表那個比較有效。"
        ],
        "claims": [
          "c7"
        ]
      },
      {
        "id": "check-pairing",
        "template": "shot",
        "data": {
          "prompt": "From behind, a sewing room in daytime. An apprentice studies a bare fabric panel stretched on a low stand; the panel is the focus. Side-window light illuminates its folds."
        },
        "text": [
          "換表示方法時，要重新驗證查詢和資料怎麼搭配。"
        ],
        "claims": [
          "c7",
          "c9"
        ]
      },
      {
        "id": "check-compatible-parts",
        "template": "bullets",
        "data": {
          "title": "一起核對的設定",
          "items": [
            "表示方法與版本",
            "查詢與資料入口",
            "比較方法與原文版本"
          ]
        },
        "text": [
          "先看資料用什麼表示，現在的問題又用什麼表示。",
          "再看問題和文件，是否用了這個方法要求的入口。",
          "比較方法和原文版本也要對上，不能只看數字能算。"
        ],
        "claims": [
          "c7",
          "c8",
          "c9"
        ],
        "reveal": true
      },
      {
        "id": "query-document-not-identical",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, a sewing alcove in daytime. Two artisans compare a folded fabric strip and an unprinted paper pattern; both pieces are centered. Light enters from the open side window."
        },
        "text": [
          "有些方法讓問題和文件，透過不同入口來形成表示。"
        ],
        "claims": [
          "c8"
        ]
      },
      {
        "id": "compatible-can-differ",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a sewing bench in daytime. A hand fits a plain cloth edge against a smooth curved paper shape; the join is centered. Light falls from the narrow side window."
        },
        "text": [
          "入口不同可以是設計的一部分，目的是讓它們相容。"
        ],
        "claims": [
          "c8"
        ]
      },
      {
        "id": "entry-point-nuance",
        "template": "compare",
        "data": {
          "title": "入口與相容",
          "left": {
            "heading": "部分方法",
            "points": [
              "問題、文件入口不同"
            ]
          },
          "right": {
            "heading": "仍要確認",
            "points": [
              "兩種表示能配合比較"
            ]
          }
        },
        "text": [
          "不能只因為查詢和文件用了同一個入口，就說設定一定都對了。",
          "也不能說所有模型都得用兩個入口，要看方法設計。"
        ],
        "claims": [
          "c7",
          "c8"
        ],
        "reveal": true
      },
      {
        "id": "metric-normalization",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, a sewing surface in daytime. A tailor lays a plain cord along an unmarked cloth edge; the cord is centered. Light comes through a high side window."
        },
        "text": [
          "比較方式和數值的處理，也得配合表示的設定。"
        ],
        "claims": [
          "c6",
          "c9"
        ]
      },
      {
        "id": "no-universal-cutoff",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the sewing alcove in daytime. An apprentice shows a plain cloth swatch to a tailor, who examines its edge; both are centered. Light enters through the side window."
        },
        "text": [
          "所以別拿一個門檻，直接套進每一套表示方法。"
        ],
        "claims": [
          "c9"
        ]
      },
      {
        "id": "no-dimensions-buying-rule",
        "template": "shot",
        "data": {
          "prompt": "Close-up, a sewing workbench in daytime. A person lifts a single fabric fold above an unprinted pattern sheet; the fold is centered. Light from the side window."
        },
        "text": [
          "多幾個維度，也不能單憑這件事就保證結果更好。"
        ],
        "claims": [
          "c5",
          "c9",
          "c19"
        ]
      },
      {
        "id": "keep-original-evidence",
        "template": "shot",
        "data": {
          "prompt": "From behind, a sewing alcove in daytime. A tailor sets a plain finished fabric pouch on a centered stand while an apprentice watches. Light arrives from the open side window."
        },
        "text": [
          "資料的來源和版本要留下，才能回去看原文條件。"
        ],
        "claims": [
          "c7",
          "c17",
          "c21"
        ]
      },
      {
        "id": "scope-not-deploy",
        "template": "big",
        "data": {
          "text": "表示配對，再讀原文",
          "sub": "沒有測模型或部署索引"
        },
        "text": [
          "這次不幫你選模型，先把比較成立的前提說清楚。"
        ],
        "claims": [
          "c7",
          "c19"
        ],
        "reveal": false
      },
      {
        "id": "remember-the-locked-door",
        "template": "shot",
        "data": {
          "prompt": "Low-angle shot, a sewing alcove in daytime. A plain folded cloth rests on a work stool while a person checks its seam; the fold is centered. Light enters through the side window."
        },
        "text": [
          "就算表示搭配正確，門今天開沒開，也得另有證據。"
        ],
        "claims": [
          "c17",
          "c21"
        ]
      },
      {
        "id": "fifth-chapter-question",
        "template": "big",
        "data": {
          "text": "回到第一名的原文",
          "sub": "找必要條件，不猜分數"
        },
        "text": [
          "現在看到搜尋第一名，你會回去核對哪個條件？"
        ],
        "claims": [
          "c18",
          "c21"
        ],
        "reveal": false
      }
    ]
  },
  {
    "title": "條件圈出來，未知留下來",
    "scenes": [
      {
        "id": "viewer-original-conditions",
        "template": "chapter",
        "data": {
          "number": "6",
          "title": "條件圈出來，未知留下來"
        },
        "text": [
          "回到第一名原文，把你一定需要的條件圈出來。"
        ],
        "claims": [
          "c18",
          "c21"
        ],
        "reveal": false
      },
      {
        "id": "garden-next-step",
        "template": "shot",
        "data": {
          "prompt": "Wide shot, a rooftop community garden in late afternoon. Two neighbors inspect a plain clay planting pot together, their shared pot centered. Low sunlight from the open terrace."
        },
        "text": [
          "不要只看結果的標題，先看它到底支持了哪件事。"
        ],
        "claims": [
          "c1",
          "c18",
          "c21"
        ]
      },
      {
        "id": "read-the-necessary-bit",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the terrace garden before sunset. A hand lifts the rim of a plain clay pot above a woven mat; the rim is centered. Sunlight enters from the open edge of the roof."
        },
        "text": [
          "問今天能參加，就找今日開放，還有預約等限制。"
        ],
        "claims": [
          "c11",
          "c21"
        ]
      },
      {
        "id": "one-viewer-action",
        "template": "steps",
        "data": {
          "title": "圈出必要條件",
          "steps": [
            {
              "title": "打開原文",
              "detail": "確認來源與版本"
            },
            {
              "title": "圈必要條件",
              "detail": "逐項找支持紀錄"
            },
            {
              "title": "缺資料留未知",
              "detail": "不要自己補成肯定"
            }
          ]
        },
        "text": [
          "打開原文，先確認這份資料是什麼來源、哪個版本。",
          "圈出你這次需要的必要條件，再看看原文是否真的有明確支持。",
          "沒有寫的就留待確認，最高分不能替缺資料作答。"
        ],
        "claims": [
          "c18",
          "c21"
        ],
        "reveal": true
      },
      {
        "id": "do-not-fill-empty",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the rooftop garden in late afternoon. A neighbor sets a plain empty pot beside a low planter while a companion watches; the empty pot is centered. Light from the open sky."
        },
        "text": [
          "木作室缺今天的資訊，我就先不把它說成開放。"
        ],
        "claims": [
          "c1",
          "c14",
          "c18"
        ]
      },
      {
        "id": "source-can-be-stale",
        "template": "shot",
        "data": {
          "prompt": "Overhead shot, the terrace garden in late afternoon. A hand smooths the soil in a plain clay pot; the soil surface is the focus. Angled sunlight from the roof edge."
        },
        "text": [
          "即使清單有寫，現實是否仍有效，也得看來源時效。"
        ],
        "claims": [
          "c17",
          "c21"
        ]
      },
      {
        "id": "toy-match-not-real-place",
        "template": "shot",
        "data": {
          "prompt": "From behind, the rooftop garden in late afternoon. A person watches a companion tend a plain planting pot, with the pot centered. Low sunlight enters from the open terrace."
        },
        "text": [
          "紙藝桌在虛構資料裡符合，不是現實活動的保證。"
        ],
        "claims": [
          "c1",
          "c14",
          "c19"
        ]
      },
      {
        "id": "what-the-score-did",
        "template": "shot",
        "data": {
          "prompt": "Close-up, the rooftop garden before sunset. Fingers steady a plain seedling pot on a woven pad; the pot edge is centered. Light from the open sky."
        },
        "text": [
          "我的看法是，先用相似結果定位，再用原文核對。"
        ],
        "claims": [
          "c18",
          "c21"
        ]
      },
      {
        "id": "answer-locked-door",
        "template": "shot",
        "data": {
          "prompt": "Medium shot, the terrace garden in late afternoon. Two neighbors fold a plain cloth pouch together, the pouch between their hands at the center. Sunlight from the open roof edge."
        },
        "text": [
          "那扇門還關著，玩具高分沒有改掉休館的紀錄。"
        ],
        "claims": [
          "c1",
          "c11",
          "c17"
        ]
      },
      {
        "id": "answer-and-article",
        "template": "outro",
        "data": {
          "title": "相近給候選，條件要證據",
          "cta": "完整圖解與步驟，在對應文章"
        },
        "text": [
          {
            "id": "zabm",
            "text": "相近幫你找到候選，條件還得有證據。"
          }
        ],
        "claims": [
          "c18",
          "c21",
          "c22"
        ],
        "reveal": false
      }
    ]
  }
];
function line(value,reveal=false){
 const source=typeof value==="string"?{text:value}:value;
 const id=source.id??newIds[nextId++];
 if(!id)throw new Error("No reserved id left");
 return {id,text:source.text,...(reveal?{reveal:1}:{})};
}
base.scenes=chapters.flatMap(ch=>ch.scenes.map((s,index)=>{
 const numbered=["bullets","table","steps","compare","stats","terminal"].includes(s.template)&&s.reveal!==false;
 const data={...s.data};
 if(s.template==="shot"){
  data.prompt=s.data.prompt+" "+guards[shotIndex%guards.length];
  data.camera=cameras[shotIndex%cameras.length];
  data.visual="still";
  shotIndex++;
 }
 return {id:s.id,...(index===0?{chapter:ch.title}:{}),template:s.template,data,claims:s.claims,lines:s.text.map(v=>line(v,numbered))};
}));
setPauseBeats(base);
const timeline=estimateTimeline(base);
const allLines=base.scenes.flatMap(s=>s.lines);
if(new Set(allLines.map(l=>l.id)).size!==allLines.length)throw new Error("Duplicate line ids");
const look=resolveLook(base.look);
const requests=base.scenes.filter(s=>s.template==="shot").map(s=>{
 const prompt=shotPrompt(s,look,[]);
 const combined=look.negative?prompt+". Avoid: "+look.negative:prompt;
 if(s.data.prompt.length>450||/[^\x00-\x7f]/.test(s.data.prompt)||combined.length>=1500)throw new Error("Image prompt exceeds audited bounds: "+s.id);
 return {scene:s.id,raw_length:s.data.prompt.length,request_length:prompt.length,combined_length:combined.length,combined_sha256:createHash("sha256").update(combined).digest("hex")};
});
writeFileSync(new URL("video.json",dir),JSON.stringify(base,null,2)+"\n");
const shorts = [
  {
    "schema_version": 2,
    "slug": "ai-term-embedding-short-1",
    "format": "shorts",
    "locale": "zh-TW",
    "line": "cut",
    "series": "illustrated",
    "source": {
      "slug": "ai-term-embedding"
    },
    "titles": [
      "搜尋第一名，為什麼門還關著？",
      "嵌入分數很高，先回讀原文"
    ],
    "description": "精華來自嵌入向量完整解說。活動與向量都是作者原創、手填的玩具示意，不是模型embedding或模型評測；分數不能代替原文條件。",
    "scenes": [
      {
        "shot": "closed-workshop",
        "headline": "第一名，門卻關著",
        "note": "人工座標示意，非模型實測",
        "narration": [
          "最高分的活動，今天休館。",
          "這份活動與向量，都是人工示意。"
        ]
      },
      {
        "shot": "latch-reveal",
        "headline": "高分沒有打開門",
        "big": "1.0000",
        "note": "玩具餘弦，非正確機率",
        "narration": [
          "拼貼室的分數是一，清單卻寫今天關閉。",
          "高分不能把休館變成開放。"
        ]
      },
      {
        "shot": "reservation-seat",
        "headline": "原文還有條件",
        "narration": [
          "陶藝室今天開放，卻需要預約。",
          "木作室今天有沒有開，資料還沒寫。"
        ]
      },
      {
        "shot": "what-the-score-did",
        "headline": "回讀原文，圈必要條件",
        "narration": [
          "我會先回讀原文，圈出要成立的條件。",
          "沒寫的留待確認，不用最高分去猜。"
        ]
      },
      {
        "shot": "answer-locked-door",
        "headline": "看完整解說",
        "narration": [
          "完整影片把表示、分數和條件分開看。"
        ]
      }
    ]
  },
  {
    "schema_version": 2,
    "slug": "ai-term-embedding-short-2",
    "format": "shorts",
    "locale": "zh-TW",
    "line": "cut",
    "series": "illustrated",
    "source": {
      "slug": "ai-term-embedding"
    },
    "titles": [
      "前兩筆沒匹配，清單就沒答案嗎？",
      "向量候選與條件檢查，分開看"
    ],
    "description": "精華來自嵌入向量長片的真實離線玩具計算。六筆活動與向量手填；作者指定只查前兩筆，不是通用k建議，不是ANN、向量資料庫或模型效能評測。",
    "scenes": [
      {
        "shot": "community-hall-review",
        "headline": "前兩筆都不能去",
        "note": "人工座標示意，非模型實測",
        "narration": [
          "這是手填向量的六筆活動，不是模型實測。",
          "這次作者只查排序前兩筆。"
        ]
      },
      {
        "shot": "paper-table-lower-rank",
        "headline": "前兩筆沒匹配",
        "big": "[]",
        "narration": [
          "兩筆分別是休館和需預約，檢查後沒有符合項。",
          "不表示整張清單沒有合用活動。"
        ]
      },
      {
        "shot": "one-paper-object",
        "headline": "全清單，找到紙藝桌",
        "big": "N003",
        "note": "只符合虛構欄位",
        "narration": [
          "改查完整六筆，符合欄位的是紙藝桌。",
          "木作室和維修公告仍保持未知。"
        ]
      },
      {
        "shot": "what-the-score-did",
        "headline": "候選與條件分開看",
        "narration": [
          "這是本例的候選設定，沒有測資料庫。",
          "不能當通用建議，也不是真實營業證明。"
        ]
      },
      {
        "shot": "answer-locked-door",
        "headline": "看完整的離線實算",
        "narration": [
          "完整影片讓你看到排序和原文條件怎麼分開。"
        ]
      }
    ]
  }
];
writeFileSync(new URL("shorts.json",dir),JSON.stringify(shorts,null,2)+"\n");
const lexicon=JSON.parse(readFileSync(new URL("../lexicon.json",dir),"utf8"));
const states=slideStates(base,timeline);
const metrics={status:"DRAFT_SOURCE_ONLY_NOT_FACT_CHECKED_OR_MEDIA_ACCEPTED",timing_basis:"estimated_250_cpm_not_actual_TTS",source_sha256:createHash("sha256").update(readFileSync(new URL("video.json",dir))).digest("hex"),brief_sha256:createHash("sha256").update(readFileSync(new URL("brief.md",dir))).digest("hex"),spoken_units:allLines.reduce((n,l)=>n+spokenUnits(l.text),0),line_count:allLines.length,scene_count:base.scenes.length,shot_count:requests.length,estimated_body_seconds:timeline.total_frames/timeline.fps,estimated_minutes:timeline.total_frames/timeline.fps/60,chapters:chapterList(timeline),cadence:cadenceSummary(states),estimated_state_min_seconds:Math.min(...states.map(s=>s.seconds)),estimated_states_under_five_seconds:states.filter(s=>s.seconds<5).length,illustration_share:illustrationShare(base,timeline),cadence_problems:cadenceProblems(base,timeline),estimated_hook_end_seconds:timeline.lines[0].end_frame/timeline.fps,estimated_promise_end_seconds:timeline.lines[1].end_frame/timeline.fps,first_numeric_scene:base.scenes.find(s=>s.id==="highest-but-closed")?.id,first_disclosure_scene:"toy-disclosure",known_lint_warning:"Opening chapter length heuristic; hook is the first line, not the entire chapter. Keep approved six chapters; actual runtime not yet measured.",speech_hash:speechHash(base,lexicon),preserved_initial_ids:initialIds.filter(id=>allLines.some(l=>l.id===id)),used_new_ids:nextId,reserved_unused_ids:newIds.length-nextId,prompt_requests:requests};
writeFileSync(new URL("draft-metrics.json",dir),JSON.stringify(metrics,null,2)+"\n");
console.log(JSON.stringify({spoken_units:metrics.spoken_units,lines:allLines.length,scenes:base.scenes.length,shots:requests.length,minutes:metrics.estimated_minutes,cadence:metrics.cadence,share:metrics.illustration_share,problems:metrics.cadence_problems},null,2));
