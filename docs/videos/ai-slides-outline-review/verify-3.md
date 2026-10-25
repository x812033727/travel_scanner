# 第四片獨立事實核驗 3 — REVISE

RESULT: REVISE

查核日：2026-10-25 UTC。查核者：`news_verify`，未撰寫本片。這是R2三句口白、兩張對應字卡、刪除一個章節標籤及其依賴的窄範圍獨立核驗；不是重做全片外部事實研究、敘事盲讀或媒體驗收。未修改source、claims、brief、資料、素材、聲音、字典、後臺或git；沒有付費／登入／生成操作。

## 固定版本與結論

- 本輪video SHA256：`5c762406b378be00cfad56936a634399954185aabce05d4b95287fb40e632490`。
- 本輪claims SHA256：`6f31b4ed577dc8f7523f4df4679e9958a602a88e008316a98d8fb228c26f0526`。
- 實讀R1備份video SHA256：`4c4bc567a7e1d053f17046f79ac0e3bcef20e7cca72a992bfe67fe830d3a915b`；claims：`ece95ef98c2cdf06d78b710cc6bb458edba94fd93a90cbb8cf1b0786f8ab1d93`。位置：`/workspace/work/ai-tech-next/fourth-before-r2/`。
- R1獨立`verify-2.md`的PASS及bytes保持不變，SHA256：`976641249d5027774cc9e7cc11b87e146313fa7a9b6d63d71c83a9ade4dfc382`；初版`verify-1.md`的REVISE保持不變，SHA256：`8861a2673576e025a569dd417fe8323d7c06e2fd8ecf1081b0ca0ba01d91f749`。

**本輪REVISE，唯一必修F1是claims可追溯性回歸。** 三句改寫、兩張字卡與章節合併本身未發現新增事實錯誤；但R2的131列claims每列都被刪掉原最後一格，超出三句quote／evidence的預期變動。120列遺失scene，另外11列原本末格為查核日期，連日期也遺失。表頭仍列7欄，當前120列只有6格，11列只有5格。不可把尚未修復的這組source／claims標成PASS。

最低修法：按claim ID恢復R1原有末格，保留當前R2三句quote與相應evidence；不要回退R2旁白。11列原本未列scene的資料可以明確補`—`維持7欄，但不能捏造外部查核或新場景。修後必須以新claims SHA另立收據；本報告保持原REVISE。

## 完整差異與本輪主張表

以真正兩份JSON逐欄比較，共**10個葉節點差異**：3個line.text、兩張字卡共6個文字欄位、刪1個chapter。90個scene ID與順序、118個line ID與順序均相同；其餘115個完整line物件相同。沒有新增／刪除scene或line。完整機讀差異、131列claims的原始前後整列／欄位／行號，均保存在`/workspace/work/ai-tech-next/fourth-r2/verify-3-diff.json`。

下表的HTTP200是重用今日21:20原獨審保存的正常UA GET收據，逐份重算raw bytes與SHA相符，**不是本查核者重新發出的GET**。本輪沒有新增外部事實，因此沒有重複網路請求。LOCAL指實讀本片原創資料及其manifest。

| # | where／claim | before → current | URL／證據 | HTTP | verdict／理由 |
|---|---|---|---|---|---|
| 1 | `source-report/sk7r`，c8 | 輸入是Stanford二〇二六年AI指數報告的經濟章。→輸入是Stanford AI指數報告的經濟章。 | https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_economy.pdf ；同一原PDF及data/page-citation-manifest.json | 200 cached／LOCAL | CONFIRMED。只刪此句重複年份，沒有把來源改成其他報告。原`source-report.data`仍列2026經濟章與2025資料；`immj`仍完整口述2026報告／2025資料。 |
| 2 | `concentrated-feedback-b/i8qv`，c54 | 最後交可編輯檔、PDF和逐頁引用清單。→最後按剛才的交付清單，把成品和引用紀錄一起交齊。 | https://github.com/x812033727/travel_scanner/tree/c8308b78321ad3ebc23bf516d1828203d07a40a8/docs/videos/ai-slides-outline-review/data ；三卡全文、review-feedback.json、既有PDF／PPTX／manifest | LOCAL；既有公開三檔GET200收據 | CONFIRMED。回呼先前`2knx`的完整三種交付，不是刪除可編輯檔要求；三張完整prompt卡及metadata全文逐值相同。 |
| 3 | `concentrated-feedback-b.data.keys[2]` | 交付成品、可編輯檔與來源→按既有交付清單一起交齊 | 同上；prompt-card-three及既有三檔 | LOCAL | CONFIRMED。回呼既有清單，無新增產品交付實測。 |
| 4 | 同場景`data.steps[2].title` | 最後交可編輯檔、PDF→最後按剛才的交付清單， | 同上 | LOCAL | CONFIRMED。與i8qv及下一detail合讀相符。 |
| 5 | 同場景`data.steps[2].detail` | 和逐頁引用清單。→把成品和引用紀錄一起交齊。 | 同上 | LOCAL | CONFIRMED。沒有更改既有清單、資料包或原產出歷史。 |
| 6 | `goal-not-tied-to-menu/p2we`，c114 | 這份需求還留著聽眾和講述範圍，能換成你要交付的內容。→確認自己帳號的審大綱選項後，用同一份需求改寫聽眾和篇幅。 | https://support.google.com/gemininotebook/answer/16757456?hl=en ；https://workspaceupdates.googleblog.com/2026/10/gain-more-creative-control-over-slide-Decks-and-Video-Overviews-in-Gemini-Notebook.html ；本片完整三卡、未變skdk／qtzp | 200 cached／LOCAL | CONFIRMED（前提及可複用欄位）／OUT OF SCOPE（觀眾祈使動作）。以觀眾先確認自身選項為前提，未聲稱作者已操作、免費必有、差異已解或所有帳號可用。聽眾與頁數／講述時間在原需求中都有。 |
| 7 | 同場景`data.key` | 從這份需求改成自己的交付→從帳號確認接到自己的交付需求 | 同上 | 200 cached／LOCAL | CONFIRMED／編輯回呼。承接skdk的確認要求，不是新實測結果。 |
| 8 | 同場景`data.sub` | 聽眾與講述範圍，可以換成你的內容→確認帳號選項後，改成你的聽眾與篇幅 | 同上 | 200 cached／LOCAL | CONFIRMED／編輯回呼。保留確認前提與可替換欄位。 |
| 9 | 同場景`data.text` | 需求裡留下欄位→沿用同一份需求 | 本片未變完整三卡及data/input-brief.json | LOCAL | CONFIRMED／編輯指令。沒有宣稱觀眾已使用或額外跑過產品。 |
| 10 | 同場景`chapter` | 需求留下了可替換的欄位→刪除章節標籤 | 實際source JSON及原生chapterList／composeMetadata | LOCAL | OUT OF SCOPE（敘事結構），依賴CONFIRMED。只把此段併入前章；內容、場景、後續適配需求及三句CTA保留。當前6章均真實輸出。 |
| 11 | c8／c54／c114 quote、evidence | 各改為當前三句及對應回呼說明 | 當前video與claims逐字、scene.claims引用 | LOCAL | CONFIRMED。三句quote精確相同；除了每列末欄回歸，只有這3列的quote與evidence cells改動。 |
| 12 | F1：全部131列claims最後一格 | R1原末格→全部遺失 | R1／R2實際claims bytes；完整前後整列在verify-3-diff.json的`claims.dropped_rows_full_before_after` | LOCAL | **REVISE／CHANGED REQUIRED**。120個scene與11個checked_on日期遺失；表頭仍7欄。這是本輪唯一阻擋項，未直接改檔。 |

### F1完整證據定位與具體修法

`verify-3-diff.json`逐一保存131個claim ID、兩版原始Markdown整列、兩版每格內容、before/current行號、兩版格數、被刪原末格及其種類。沒有只記抽樣，也沒有用作者delta宣稱沒有其他變動。

| 分組 | claim ID | R1 → R2 | 修法 |
|---|---|---|---|
| 120列丟scene | 全118句對應claim，加c121、c133 | 原7格→6格；例如c8丟`source-report`、c54丟`concentrated-feedback-b`、c114丟`goal-not-tied-to-menu` | 按ID恢復各列原scene；保留當前三句quote/evidence。 |
| 11列丟查核日期 | c122、c123、c124、c125、c126、c127、c128、c129、c130、c131、c132 | 原6格→5格；原末格均為`2026-10-25` | 恢復原日期；沒有既存scene者以`—`明示，勿把日期錯放scene。 |

本輪仍能由line ID及video.scene.claims獨立確認118/118口白皆有唯一claim，quote精確且claim ID在正確scene.claims中；這**不能代替恢復實際claims表格的查核日期與scene**，也不會把F1降成PASS。

## 依賴實核與範圍保留

| 項目 | 本輪實際結果 |
|---|---|
| 完整三卡 | prompt-card-one／two／three整個scene物件與R1完全相同，共11句；來源、一般同事、4頁、約3分鐘目標、先大綱不先生成、資料欄位、雙頁碼、子集／未解政策、一次全部修改、可編輯檔／PDF／逐頁引用清單均保留。各完整scene canonical SHA在scratch收據。 |
| 報告年／資料年 | `immj`完整line及scene ID相同；source-report表格2026與2025來源標記不變。原PDF SHA仍`6654b484b0c20213ead6ed8388f3145928c2dde9bca86e16a5b7efe9a00d8269`，6,450,805 bytes、60頁；實讀頁8的2026章首／2025資料及本地manifest。沒有把2025統計說成新調查。 |
| 五值與限定 | fpqu／uyre／qa92／f6fw／hxni／frra／9xhq／iswb／dp4j等完整line物件相同。581.69與344.66仍為同單位企業總額／私人子集、不相加；285.88／12.41仍同2025私人融資；88%仍為受訪者自報組織至少一項業務使用AI。這是相同bytes與既有證據鏈依賴核對，非本輪新增五項研究。 |
| 70／79未解 | g84b／e9xt／cwpj／iek7／aywh完整line物件及原manifest相同；仍只作兩處來源觀察，不選唯一採用率、不判報告錯誤。 |
| 本地原創界線 | jyx8、h58h、z84y及description完整相同；未試用Notebook、作者安排、同次產出保存、無真實停等仍保留。沒有產品AI回應、登入或互動生成證據。 |
| 帳號前提 | qtzp、skdk完整line物件與對應限制相同；公告範圍與Ultra help差異仍未用帳號試用消解。p2we要求觀眾確認，沒有宣稱已消解。 |
| R1已修的頁碼範圍 | 8arj及manifest相同：S1作者問題總覽；S2–S4才接原報告位置。未把所有四頁都改稱有精確PDF／印刷頁／圖號。 |
| 本地產物／圖資bytes | 當前20份copied-file-manifest檔逐份實際bytes／SHA全吻合；R1新增四頁縮覽與縮圖的4個SVG／PNG fullSHA亦逐份等於R1獨審收據。未重渲染或重看未變PNG來冒充新媒體驗收。 |
| top-level | youtube、thumbnail、sources、assets、voice、subtitles、loops及所有其他top-level欄位逐值完全相同。沒有改授權、URL、語音風格或素材記錄。 |
| 三種交付URL | 未變公開pinned資料包及既有public-data-verification.json：PDF、PPTX、page-citation-manifest.json原GET200與本機SHA一致；本輪又實核三個本機SHA。未冒稱此輪重下載遠端整包，也未冒稱PowerPoint原生渲染。 |

### 今日primary bytes重用收據

原收據：`/workspace/work/ai-tech-next/fourth-root-facts/independent/fetch-receipt.json`，正常UA，2026-10-25T21:20:40.953Z至21:20:47.922Z；此輪逐份重算以下完整raw SHA與bytes相符。

| 來源 | HTTP | bytes | raw SHA256 |
|---|---|---:|---|
| Google 10/19產品公告 | 200 | 971380 | c07431b438e6899ec2565e2123e9e78c23fba0d3cecc3de91d9afffcca579e0d |
| Workspace 10/21公告 | 200 | 205874 | a8decf4181b06c82ee70d726ee4a766c8d93f34d35454f5f072c2cad74ddf5db |
| Slide Deck help | 200 | 1539401 | ff573b75c9924dff2838f43ae5af831652c7003d425a039b31916479d98a4091 |
| Video help | 200 | 1543604 | 1f8414ed098769bd0840aee9da5405df8b4f626831c662131b8080d005821f0c |
| Stanford經濟章PDF | 200 | 6450805 | 6654b484b0c20213ead6ed8388f3145928c2dde9bca86e16a5b7efe9a00d8269 |
| McKinsey調查 | 200 | 263168 | f7198eded72b12f20953c9679e9766ce0da299fe9a2c649ec20e823f4e4d526f |

## 原生輸出、聽眾及限制

實際以本repo的loadProject／estimateTimeline／composeMetadata／creditedAssets執行唯讀檢查，完整輸出存`/workspace/work/ai-tech-next/fourth-r2/verify-3-native.json`。原生組成description **3129 UTF-8 bytes**，metadata problems `[]`，creditBytes **272**，實際creditedAssets仍是**1**筆具author／URL的s1；9筆assets的source／license記錄均未變，不冒稱9筆可輸出credit。

六章確實存在於原生metadata與description，估時計時如下，**不是實際TTS／成片時間**：

| estimated at | chapter |
|---|---|
| 00:00 | 我從公開報告寫下簡報需求 |
| 00:25 | 來源紀錄把金額與使用比例分開 |
| 02:10 | 完整需求交出後，作者初稿仍擠在兩頁 |
| 04:03 | 集中修改讓四頁各自有了任務 |
| 07:08 | 第二到第四頁接回原報告 |
| 09:13 | Google公告新增生成前的大綱審查 |

完整description仍包含原完整三卡提示、6個官方來源URL與原pinned資料包URL、原本地作者／未試用／同次產出／PowerPoint未原生渲染等限制。description SHA256：`68b24ac0e94060a585da3fba66ef1b459cc675407a6a05acc82f8eaff0c3b0ea`。7→6章並未刪除第七段內容或相應CTA。

本輪實跑：`node /workspace/work/ai-tech-next/run-video-slides.mjs lint --slug ai-slides-outline-review`，exit 0，**0 errors、2 warnings**。warnings是約25秒冷開，以及`immj／f6fw／cwpj`的2025必要重現；不把它們改成無警告。原生估118句、2323 spoken units、658.2333秒（11.0分鐘），不是實際音長。全118句的超40字、網址／括號、未知Latin詞、制式查核口白檢查皆0；此靜態結果不等於音檢或新盲讀PASS。

## 收尾

- 本輪核驗10個實際JSON差異、3句語義及其依賴；118/118當前口白quote／scene.claims引用精確；131/131表格末格回歸保存完整證據。
- 新增外部事實錯誤：0；待修群組：1（F1表格日期／scene可追溯性）。未直接修改，沒有將它記成已CHANGED完成。
- 超過3項實質事實更正觸發第二人再查：否；本輪未更正外部事實。F1仍需修復後以新claims SHA另外確認。
- 意見／brief立場：未變，這輪無新增立場不符。未變字卡／素材不冒稱重新完成全篇查核。
- 易過期項目仍是帳號／方案／功能推出範圍；保留2026-10-25所讀日期與沒有帳號結果的限制，R2沒有新增可用性保證。
- 未執行Notebook試用、PowerPoint原生渲染、TTS、音檢、成片QA、八語、M4A或發佈操作。本報告不證明上述完成，不替其他SHA或敘事評分背書。

本報告只綁本文所列`5c7624…`／`6f31b4…`。R1 PASS、初版REVISE及本次REVISE均保持各自歷史效力；尚未修復的claims不可自動沿用R1 PASS。
