# verify-3：ag125 同義改詞後的獨立來源 rebind

查核日期：2026-10-07；實際 source／input readback UTC `2026-10-07T13:04:48.382602+00:00`。本 reviewer 未撰寫原稿或套用改詞，只寫本收據。**目前 142 句的來源／語意查核可沿用 verify-2，ag125 的已套用同義改詞另經覆核。** 這不是音訊聽驗、TTS fit、字幕重算、final、owner acceptance 或發布核准。

`<repo>` 表示本次 `codex/ai-agent-continuation-20261007` worktree；`<home>` 表示使用者家目錄。這份最新 round 沒有覆寫 verify-2，也沒有把舊 source 的完整 SHA 倒填成新 source。

## 完整 source 與原收據 binding

| 輸入 | Bytes | SHA-256 |
| --- | ---: | --- |
| current `<repo>/docs/videos/ai-agent-vs-chatbot/video.json` | 36757 | `6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235` |
| before `<home>/mokaair-work/ai-agent-continuation-20261007/listener-rewrite1/source-before.json` | 36751 | `905ac35021688b7ca80264f12afd6f8973b959317438538e2199bdb4536a058c` |
| `<repo>/docs/videos/ai-agent-vs-chatbot/verify-2.md`（完整原件未改） | 46827 | `4ae41e498d256f55553db30db691813cd83d6e1f6bde2cd82ce4e778a6782580` |
| `<repo>/docs/videos/ai-agent-vs-chatbot/claims.md` | 3609 | `92cf526c83ea45596918e16fa3d734a34e3c2112ba3572e1e193c767880c7f59` |
| `<repo>/docs/videos/ai-agent-vs-chatbot/brief.md` | 4564 | `9093fcc62ad70a60bfcd8680389c833d85de87aba090a8028f0302a11976ba23` |
| `<repo>/docs/videos/ai-agent-vs-chatbot/demo-log.md` | 1690 | `423fe1ff42b63f6139dac925e8263556636c21ca8024d25717769bbe76267042` |
| `<repo>/docs/videos/lexicon.json` | 3406 | `862d277aaf4359e9e07b5f3281f59eabb240f5ea3227c174f692cf2d0237f675` |
| `<home>/mokaair-work/ai-agent-continuation-20261007/listener-rewrite1/applied.json` | 831 | `924c893c8338a46d941d42e96fdf7f6ef534e4691a67a8b0915121743bbcc783` |

before source 完整 SHA 與 verify-2 visual-only appendix 所釘的 source 相同。此 round 對 before／current 的**整個 parsed JSON** 做遞迴比較，唯一差異為 `/scenes/17/lines/2/text`，對應 `specific-date / ag125`；雙方都是 36 場景、142 句，句 ID 與順序相同。其他 141 個完整 line objects、ag125 的 id／reveal、全部 voice、pause／hint 等語音欄位、scene templates／data／reveals、sources／checked_on、YouTube fields、thumbnail、format、source_guide 及其餘非語音欄位完全相同。將 current ag125.text 反轉為 before text 後，整個 parsed source 深度相等，沒有藉單句 rebind 覆蓋別的改稿。

`applied.json` 記錄 root 於 UTC `2026-10-07T13:03:29.330Z` 套用 first listener rewrite，native protected rewrite problems 空，沒有寫 approval；本 reviewer 重新讀取實際 source 確認上述唯一變動，不只信這份敘述。它記錄的三次既有重錄屬 root 的製作歷程，不是本 reviewer 額外執行或逐次聽驗的證明。

## 唯一改詞與判定

| Claim／line | before | current | 判定 | 來源及理由 |
| --- | --- | --- | --- | --- |
| A4／ag125 | 交付物要保留日期和館名，不能只寫週一可去。 | 交付物要保留日期和館名，不能只寫週一可以參觀。 | CHANGED | 同義用詞已套用並 readback。保留日期、館名與「不能只寫」；把模糊的「去」說清楚為本歷史博物館任務的參觀。此句仍是編輯性交付規格，不是新增的開館事實。 |

相鄰 ag124 仍是「九月二十八日開館，不代表所有週一都開。」；scene 字卡仍明列「別把特例講成通則」「這一天開，不代表每週一都開」「日期與館名要一起保留」。因此「週一可以參觀」位於不能只寫的否定範圍，不能從此句推成每個週一都開館或已確定可入館。日期、館名、數字、Latin／dictionary proper terms、一般週一與指定日期的適用範圍沒有改變；沒有新增現場實測、訂票、付款或成行聲明。

這是同義的 listener 用詞調整，**確實改變 spoken text**，不是 visual-only rebind。純 native `loadProject`／`speechHash` 在同一 lexicon 下計算 before 為 `80b70c13bcc03e34`，current 為 `ef2d1ce1ef5e5ea2`。舊 timeline／QA／metadata／caption／movie 不能只換 source SHA 就當成新語音已通過；root 必須按實際重錄與 retiming 結果另綁定。

## 四個官方來源：沿用同日保存證據

此 round 沒有重新 GET、搜尋或 provider request。沿用 verify-2 同日實際讀取成功的四個官方 primary URLs；完整 metadata 在 `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/collection.json`，7,627 B，SHA `36b3cbde3369ed8ac671022b5422e2c30783ee5032cc644b800133ac7a2d2257`。本次重新讀取四份 HTML 與四份 text，共八個保存檔案，bytes／完整 SHA 全部符合 collection。下列 SHA 是保存檔案身分，不是宣稱動態網站永久保持同一頁面內容。

| ID／title／publisher | URL | 原 GET HTTP／retrieved UTC |
| --- | --- | --- |
| S1／Building effective agents／Anthropic | <https://www.anthropic.com/engineering/building-effective-agents> | 200／2026-10-07T10:50:35.553Z |
| S2／開放時間與票價／國立臺灣博物館 | <https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444> | 200／2026-10-07T10:50:36.146Z |
| S3／2026 年節日開閉館公告／National Taiwan Museum | <https://www.ntm.gov.tw/en/News_Content.aspx?n=5713&s=251424> | 200／2026-10-07T10:50:41.115Z |
| S4／本館交通資訊／國立臺灣博物館 | <https://www.ntm.gov.tw/cp.aspx?n=5445> | 200／2026-10-07T10:50:38.710Z |

檔案相對根為 `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit`。

| 保存檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `sources/anthropic-effective-agents.html` | 174660 | `dd21017fd0dd6b72f020bbeaf69a3faf2ba7246c447144f452a34200e51ec3fe` |
| `sources/anthropic-effective-agents.text.txt` | 20126 | `900c44e2f04d8d0a17ce0138c6e5ba704b4e7040820c38646ea0d1ca7aedc0f4` |
| `sources/ntm-hours.html` | 143207 | `b3477bef03781b7147b1f8a5ed25ded0cb1545e393a67f2cb23c5b592ee21653` |
| `sources/ntm-hours.text.txt` | 9721 | `9047834e8bce08b42157c3ae6e38163552c4ae7fb93771189fec37901fd56956` |
| `sources/ntm-2026-holidays.html` | 97852 | `02c414a7607f8af3f3f498b13d2b93fa89c71196e364fa334dcb174d64d888a9` |
| `sources/ntm-2026-holidays.text.txt` | 4334 | `21488406f032aa436a3114d254c4f4c792cc4b09362083bbe7d557c544afc93a` |
| `sources/ntm-main-address.html` | 142729 | `2d615b7e8b789f1e42e0cdfac64b16ad62177eedd287c978c97e543b4b7563f3` |
| `sources/ntm-main-address.text.txt` | 7382 | `b26081992739a21927887c61a4d445391cb5ffd8008bceec32cd3d86a9403796` |

S2 的一般週一休館與假日例外，和 S3 的指定 `September 28 (Mon)`／Teacher’s Day／Open，仍共同支持日期例外不可外推的界線。S1 的固定 workflow／回饋選路 agent 工程區分與 S4 的本館地址、館方步行建議都未受 ag125 改詞影響。ag018 的歷史查詢／規劃日期、ag097「館方有步行建議，但我們未實測，也沒查天氣」保持原文。verify-2 對工程建議、自製示意、無原始不可改寫 9/27 request 的歷史聲明、公告安排不等於實際入館／付款，以及不曾現場實測的限制全部沿用，沒有把 OUT OF SCOPE 升格為外部事實。

## 四語 ag125 的文字覆核範圍

本 round 只覆核這一行的既有／候選文字是否仍忠實於 source，不宣稱已完成新的四份翻譯檔、全部 568 entries、SRT timing 或 dub fit rebind。EN 原句 `The deliverable must name the date and museum, not just say Mondays work.`、簡中原句 `交付成果必须写明日期和馆名，不能只说周一能去。` 可沿用文字，日期／館名與 not just／不能只說的否定範圍保留；仍須正常 native merge 更新 source_hash。

JA 的最小候選 `成果物には日付と館名を残し、「月曜も行ける」とだけ書きません。`（31／39 字硬預算）與 KO 的最小候選 `결과물에는 날짜와 관명을 남기고 '월요일 가능'만 쓰지 않습니다.`（36 字）已獨立判定文字忠實。比原 JA／KO 加上「只寫」更明確，沒有宣稱所有週一可入館。只有 root 實際 merge／重產後的檔案才能作 delivery artifact；這裡的候選字數不等於配音實測或 owner 語言選擇。

## Native facts check 與完成界線

此 round 沒有新增需移除的外部事實，ag125 原本的編輯性用途仍在相同範圍。完整 142 句的來源判定以保留的 verify-2 全表及本次唯一變動的同義覆核共同成立，不另複製一份表冒充重新進行 142 次外部查詢。

寫入後以純 native `lastVerifyReport`／`factsChecks({ report, doc })` 讀 current source 與本檔：最新 report 為 `verify-3.md`，結果 `ok=true`、detail `verify-3.md marks no claim NOT FOUND`。這項機械 check 只處理最新查核表中仍被引用的未找到主張，不能證明官方頁面重抓、歷史工具執行、TTS／音訊辨識、聽音、字幕、成片、owner acceptance 或上架。沒有用 native CLI 製作、provider、production request 或 approval mutation 來得到此結論。

後續 current source、ag125／其他語音欄位、來源事實或 metadata 再變動時，須按實際差異重驗／另記 source binding。現有 narration／final／languages／upload gates、`locales={}`、無 dubs／未上傳 YouTube 的 owner 界線沒有由本文件改變；其他 citation ci037 未知 sent／STOP 及 Embedding hold 完全不在本 round 的操作範圍。
