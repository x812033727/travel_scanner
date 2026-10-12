# H04 製作紀錄

2026-10-12，Asia/Taipei。承接站主「繼續」，製作已查核題庫的下一集，僅繁體中文。H03 已完成上傳包；本集沒有沿用 H03 的核准或媒體。

## 目前狀態

- 分支：`codex/curio-h04-production-20261012`，由當前 `origin/main` 的 `f7691d8cb` 建立。
- 任務：`2026-10-12-produce-curio-h04-dyatlov-traditional-chinese`，scope 僅本資料夾。
- 碰撞檢查：H04 沒有 active task 或 open PR；正式站 H04 GET 回 404，沒有既有製作要接手。
- 正式站頻道立場已讀回，`auto_pick_outline=true`。本次大綱套用 2、3、4、6、9。
- `brief.md` 三案已送審，站主選定 A；正式站與原生 consumer 均讀回本次雜湊的核准。
- 完整 A 案腳本與四句口語修正已落地，獨立事實與聽眾審稿均 PASS、0 未解必修；119句旁白全數機器檢查通過，正式站已核准並讀回。帳篷與弱層小樣可保留，七處足跡改為已覆核原創圖解；其餘情境插圖製作中，尚未完成成片。

## 製作界線

插圖投影片，`category: explainer`，Sulafat 旁白，系列同色盤與線條。匿名人物只用遠背影／剪影；不生成近代人物肖像，不呈現遺體或傷勢。長片10–11分鐘目標、正文及成片各至少8分鐘。繁中旁白、標題說明與可關閉字幕；其他語言不製作。

文件與論文事實另查原件，2022考察明確歸於作者報告。不將模型可行性稱當年經過已證實。原題卡的切口數、日期、溫度與在世檢察官支線已收窄。

## 2026-10-12 大綱送審收據

- 正式站已確認 `format=slides`、`category=explainer`；主工人未接手，本機接續。
- brief SHA-256：`32bf76ed25e862e3e7c9e0bf8d1d369a2f9ad625a270c5518ed0919592f32a63`。
- outline review：`d76bc11e-0d58-4983-b7d2-378d18e17bd2`，送審 `2026-10-12T04:53:24.919440Z`，狀態 `pending`，choice／decided_at 均 null。
- Jev：A 推薦機率 0.98、符合立場 0.91、有示範 0.37、建議 0.01。因 demo 低於 0.60，沒有自動核准。
- 原生 `review-push --gate outline` exit 0 僅代表送審成功；`review-pull` exit 3，明示仍等站主，不等於核准。
- `checkBrief`、`stanceProblems`、`outlineOptions` 原生檢查通過，3 選項。這是企劃檢查，完整腳本尚未完成，沒有宣稱影片 lint 已通過。
- 獨立歷史與聽眾審閱已整合；科學審閱要求不把 7.5–13.5 小時當獨立預測，送審前已刪精確範圍，保留「檢驗延遲數小時情境」。
- 已向站主送出 A／B／C 選項；繁中授權沿用，未再次詢問語言。沒有執行 TTS、生圖或合成。
- [歷史查核](research-history.md) 與 [科學查核](research-science.md) 已保存，企劃階段沒有未解 must-fix。科學報告明分官方索引正文已讀、直接 PDF 受阻、補充材料及完整推導未讀。正式稿不能把這次企劃審閱當成逐句通過。
- C 案的 `stats 延遲範圍` 是畫面類型標籤，製稿僅呈現「數小時／模型情境」，依本版示範節限制，不把精確區間放回字卡。
- 最後一次回讀為 `2026-10-12T04:56:56.492Z`，仍 pending、尚未選案。若站主選定後接續，先重新認領原任務，將選擇保存到同一 review，再 `review-pull`；保持本次 brief SHA。

這是既知的關卡適用性問題：[解說類大綱免示範任務](../../../tasks/open/2026-10-10-outline-pick-demo-exempts-explainers.md)。該修正尚未落地；本次未改共用審核或分數，不為湊 demo 門檻將歷史說書改成操作教學。已保存一次 Jev 結果，不反覆付費要求不同分數。

## 工作區與證據

### 2026-10-12 A 案核准與接續

- 站主回覆：「採用 A：沿脚印回到帳篷，再檢查雪板解釋（建議）」。繁中授權沿用。
- 同一 outline review 已於 `2026-10-12T05:19:58.330973Z` 決定為 `approved`、`choice=A`。本次沒有重送大綱或改 brief。
- `review-pull` 於 `2026-10-12T05:22:04.516Z` 正常記入 `approvals.json`；brief SHA 仍是 `32bf76ed25e862e3e7c9e0bf8d1d369a2f9ad625a270c5518ed0919592f32a63`。
- `reviews-2026-10-12T05-22-13.712Z.json` GET 200，回讀同一 review ID、雜湊與 A；`outline-approved-a.png` 保存後台畫面。先前短暫 502 與一次 pull exit 4 均保留，之後已成功讀回。
- 原任務已重新認領。撰稿、原件素材清權與獨立來源查核並行；現階段核准僅指大綱，不代表完整稿、旁白或成片核准。

### 正式稿與成本預檢

- 原稿 100 景、119 句、72 張插圖、46 項主張。原生估正文 603.4 秒，插圖占 64.3%；實際時間仍待 TTS。略低於大綱 65–75% 的插圖目標，未為比例增添空洞畫面；原生 50% 下限已滿足。
- 三頁 1959 結案書局部已整合為 `screenshot`；檔案 SHA、授權、裁切矩形與實看紀錄見 [素材登錄](asset-register.md)。整合只更改三景 template/data 與 assets，逐句旁白、voice、look 均完全保持。
- 整合後 `video.json` SHA：`74c91a6cc79b1f38a7fa3430ccad816c0907aaa34a2da26d193421c639ff50e9`。外部 `source-integration-*.json` 保存前後 SHA 與素材對應。
- 原生 lint 0 errors、4 warnings：日光、雪與置中構圖詞頻，以及首章約29秒。日光／雪是本集場域；鏡頭另有室內文書、器材與材質近景，第一句直接落鉤，未將章長當成鉤子延遲。沒有估計狀態超過8秒的警告。
- `tts --dry-run` exit 0：115 個請求、119句，約2,364計費字元；Gemini Sulafat ready，當月剩9,290,812字元。
- `keyframes --dry-run` exit 0：72張、MiniMax image-01／1K；每張一次估US$0.97，每張最多三次估US$2.92，低於有效US$80本集上限。這是圖片與judge預估，不是整片總支出；當前支出US$0。
- 沒有改聲音 style／look、共享字典、主機設定或審核門檻；不新增 Shorts 或其他語言。

媒體及執行證據只放 repo 外：`C:/Users/x8120/mokaair-work/videos/curio-h04`。

### 逐句審稿完成與旁白起跑

- [事實覆核](verify-1.md) 核對 100 景、119 句與 46 組主張；三組事實修正已回讀，0 未解必修。[口語覆核](listener-review.md) 完整回讀所有句子、卡片與 reveal，同樣 PASS。
- 兩份報告共同綁定最終 `video.json` SHA `98b2fe192185644dd7a36a3deac8c4f8c9314a54486cedf1ff23cdd85dfae2f8`；`claims.md` SHA `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。
- 審稿後僅修順三句口語及兩組卡片揭示時機，原生 lint 仍為 0 errors／4 warnings。相關 docs-videos 測試 199 passed、0 failed。
- `2026-10-12T05:40:30.268Z` 最終 TTS dry-run exit 0：115 requests、約 2,363 計費字元，Sulafat ready。隨後啟動原生 `tts`；完成、實際時長及讀音判斷另記收據，不將起跑當成完成。
- `tts-2026-10-12T05-40-37-674Z` exit 0：115 requests synthesized，2,363 計費字元，119 句均有音檔。初版正文 603.8667 秒，speech hash `d0f388eeb02c1280` 與來源一致。
- 初版實際節奏共 117 狀態、平均 5.2 秒；116 狀態符合 8 秒上限，結尾卡為 8.3 秒。待逐句檢查後縮短結尾兩句的額外空白停頓，再以原音檔重建並重新驗證；不修改共用門檻或刪旁白。
- 原生 `check-audio` 已啟動，尚未取得完整讀音結果。說明欄預檢 3,027 bytes／1,918 字元、含三張原件署名，無長度問題；章節仍需在最終片頭片尾與時間軸上定稿。
- 逐句檢查在 `yqn7` 的轉寫收據發生 Windows EPERM rename；完整 confirmed 暫存答案仍在。已確認舊程序退出，逐項核對當前音檔下採樣 SHA、request SHA 與 answer SHA，備份後提升收到的原紀錄；原生 journal replay 證明 new provider calls 0。外部 `transcript-journal-recovery-0f3cd18a1ef4/receipt.json` 保存證據；沿用既有 [Windows journal 問題票](../../../tasks/open/2026-10-09-windows-speech-journal-rename-failures.md)，未改共用工具或清除不確定請求。
- `bi2x`、`x53t` 的 `pause_after_ms` 由預設 300 改為 100；原生 `tts --refresh-evidence` exit 0，115 requests reused、0 新合成／0 計費字元。來源 SHA 現為 `f4291c340eef12bac0ba08980f9cbe7f39bba6309131a8fb50e379e8f31755c8`，事實覆核已追加 timing-only 回讀。
- 修正後正文 603.4667 秒；119 句／100 景／117 狀態，最長7.9秒、平均5.2秒、插圖占63.925%，0節奏問題。speech hash `d9e4eeb59801eac3`，timeline SHA `281d53be4eec577370a8116e7109ed68d8557ffea0fff15ad58af4c531c436eb`。原生 check-audio 已從快取續跑。

### 轉寫單次重試與三張插圖小樣

- 續跑至 `ngnu`（「這能修正整隊狂奔的想像。」、2.470秒）遇 HTTP504 answer_lost；request SHA `4c8daf9a2693a69e1d3b4041d4e4c45580efb4ba6222dfa14b8307ceb9f9193c` 被原生保護列為 held。此筆沒有可恢復 confirmed 答案。已保留 held 原件，本機 Whisper small 盲轉寫為「這能修正整對狂奔的想像。」（原生 sound 比對）；本機結果未填入 Gemini cache，也不當作 Jev 核准。
- 站主明確答覆「僅重試這一筆一次（建議）」，已先告知可能重複計費。`authorized-transcript-retry-4c8daf9a2693/` 保存原件、授權與單次釋放收據；於06:00:58 UTC釋放後啟動一次原生 check-audio。若同一筆再不確定就保留，不連續重買。
- 等待上述授權時，獨立進行已授權的插圖小樣；未核准旁白或替代其關卡。3張（空帳篷、足跡、雪層）共5 takes，原生 keyframes exit0，媒體帳本US$0.07。
- 實看即使 judge 為pass，空帳篷圖仍有近處密林與尖峰，足跡圖近似裂坑；兩者列材料性問題，先修正可見地形／鞋底形隆起提示，再批量生成。雪層小樣另由獨立覆核確認；保留所有原始take及judge，不抹除評分。

### 旁白完整初檢與小樣提示修正

- 已授權的 `ngnu` 單次重試成功，後續原生第二轉寫亦依同音規則排除疑義；授權已使用，不擴及其他不確定請求。
- `nueh` 另遇 Windows journal rename EPERM，但有完整 confirmed 暫存答案。確認程序退出並核對音檔、請求與答案 SHA 後恢復收到的原件，原生 replay 證明 0 新供應商呼叫；證據在 `transcript-journal-recovery-5f88ed3df1ea/`。
- 21 張提示完成獨立覆核後套用：14 張山坡／營地明示圓緩無樹的烏拉爾高處山坡，7 張足跡明示鞋底形壓實雪隆起。只改 `data.prompt`；來源 SHA `ae85b2c4f5c1b95ca782603725b4a162140ece65c32b7cccafd6df82f695cb35`，旁白、主張、voice、look 與運鏡未改。原小樣與 manifest 已備份到 `pilot-before-prompt-fix/`，尚待重新產生兩張材料性問題小樣。
- `check-audio-2026-10-12T06-09-24-919Z` 完成 119/119 句，exit 1：92 句逐字符合、6 句同音／語助詞符合、4 句 Jev 通過、5 句經第二轉寫排除，12 句仍標記。這是機器逐句檢查，不等於站主完整聽音。
- 12 句先備份原音檔及檢查結果，再以原稿原聲音設定僅重錄被標句；dry-run 12 requests、237 計費字元、當月剩 9,274,408 字元。沒有重錄其餘 107 句或更改共享字典。
- 第一次局部重錄 exit0：12 requests／237字元，103 requests沿用；正文601.3333秒、117狀態、最長7.7秒，0節奏問題。後續轉寫的 `c5xt` 再遇相同 Windows rename EPERM，完整答案已核對並零呼叫恢復，收據在 `transcript-journal-recovery-a309097ba6c5/`。
- 5 張足跡圖僅調整景別前綴，使原生 lint 可辨識 close-up／medium／wide；後段逐字保持。來源 SHA `169d607735c155abb988c62643db72567f9d947498d479e1d691ba98bd24a6a0`，speech hash 保持 `d9e4eeb59801eac3`；`framing-prefix-backup/receipt.json` 保存差異與回復原件。
- 新一筆 `h6hn`（「小雪板影響的範圍，也和整片山坡崩塌不同。」、4.07秒）轉寫於06:20:22 UTC送出後回HTTP502，request SHA `39e05552faf3621f1dda22da5977ad0d9d3e73c7ca6cd660711cd3b61c21ed09` 留在held。站主另行授權「僅重試這一筆一次（建議）」；兩張修正版小樣結束後才執行，不把前一筆授權延用或並行啟動兩個producer。
- `h6hn` 單次授權重試已成功，後續第二轉寫與原稿相符，原生排除疑義；`authorized-transcript-retry-39e05552faf3/` 保存同筆的授權與釋放證據。
- 原稿局部重錄共三輪：12句／237字元、9句／183字元、5句／101字元；完整119句檢查後尚標記的句數依序9、5、4。最後原稿版本正文601.7秒、117狀態、最長7.7秒；沒有繼續無上限重錄。

### 七張原創示意與四句口語修正

- 第二輪小樣帳篷圖（selected SHA `ff45b01656ddc79cd760f24657f97d955b863a8e1c1b9af6dfc7ff50e81d6391`）實看可保留；足跡圖雖原生judge通過，仍呈雲團形，獨立覆核列材料性問題。兩輪原生圖片帳本合計US$0.14，所有舊take及manifest均留在稽核備份。
- 七個足跡景改為已逐張實看的原創SVG `diagram`，標示非現場照片／未按比例；詳見[素材登錄](asset-register.md)。source `4979754cb76c36e8301ec6bab8d12b414a15f876b92459954440e95d8b6fce21`，只改七個template/data及七筆原創資產，speech hash保持；65張情境插圖仍占正文57.83%，原生節奏檢查0問題。
- 三輪原稿重錄後僅改寫仍標記的 `xzmn/c5xt/a6qq/u3tt`。獨立事實覆核及原生 `rewriteProblems` 均通過；「雪板」、九人、可能／特定條件／不能反推時刻的限制保持。已解除的 `88ft` 未套備案、未再購音訊。原生 `review/rewrites.json` 記下四句before/after/heard，不改Jev舊結果。
- 四句改寫後source `692be6289870c02c4f40e41d3c500cd00b7c3e15e6399b95c289d2cebd6e2b80`；再按獨立覆核只把 `search-objects` 提示中的用品移到帳篷內，使畫面與旁白一致。現行source `30eb4fa95a6a3737d2d3e328ae409a86158550ea40c917829762a256049634c4`、speech hash `296feca213cf8271`；claims、voice、look與其他115句保持。
- 改寫第一輪 dry-run：4 requests／91計費字元；只合成這四句，後續原生檢查仍需完成。插圖完整65張dry-run：一次各一張估US$0.88，最多三次各US$2.63（總量估算，已有兩張可沿用），低於US$80有效上限。

### 旁白通過與正式站回讀

- 四句改寫合成 exit0：4 requests／91字元，111 requests沿用。正文604.0667秒、119句、117狀態，最長7.7333秒、插圖占57.72%，原生節奏0問題。
- `check-audio-2026-10-12T06-39-06-762Z` exit0：101逐字符合、8同音／語助詞符合、4 Jev通過、6第二轉寫排除，0 flagged。新增四句全部直接符合，0新Jev calls。
- audio review `f28e20d8-8c02-4b9b-8af9-a50b8494b847`，正式站於 `2026-10-12T06:40:28.403576Z` 自動核准；content SHA `f4ab52a1e7ccceccd88576b8bbc8f273cb35f204730ec3d4bb825c251305dc82` 與timeline一致。原生 `review-pull` exit0，`reviews-2026-10-12T06-41-06.412Z.json` GET200再次讀回approved。這是來源綁定的音訊機器關卡，不等同站主完整聽音。
- 65張插圖主批次已起跑，沿用兩張正確小樣；不重買足跡圖。最新文件測試199 passed／0 failed，SVG原生預覽及增量來源覆核均完成。

### 字卡、縮圖與字幕預覽覆核

- 主批次執行期間，以相同原生 renderer、字型、主題與時間軸在外部 `_audit/card-previews/` 產出35景／52個 settled states；manifest SHA `b0acfd61bc9516150a90a5578049638a2aee2c56e6dc22cd9574f32885c89b43`，source與timeline前後不變。三組獨立覆核逐張實看並核對全部52個PNG SHA，0重大問題；正式frames、入場轉場及成片尚待製作。
- 縮圖prototype使用已覆核的空帳篷selected，1280×720與320×180均實看可讀；沒有B/C變體。原尺寸SHA `eac7d20091c50e6562dc3a660c427a5674bf5e1d85931c1f0b90d93a90957b6d`，正式thumbnail仍待render。
- 原生繁中字幕預覽119 cues、0缺句、0機械問題，已納入預計片頭150 frames；只寫 `_audit/caption-preview/`。SRT SHA `e5a657e934ee241ecbc9494e02a1e02be9723aaf94dc055db9188eba689827ad`。另做逐句語意斷行覆核；播放器CC與完整聽音均未驗證。
- 原生metadata預檢0問題，說明欄3027 bytes／1918字元，包含12項研究與文書來源及3張原件署名。章節預覽為00:00、00:35、01:45、03:53、04:54、07:29、09:17；最終以正式branding、成片與上傳包回讀為準。
- 已實看的第一批插圖有三張材料性問題待集中修正：`hook-slope` 把營地放在近處林緣低地、`journey-pack` 把背包畫成擬人角色、`search-empty-interior` 把帳門外畫成暖季綠地。完整judge與舊take保留；沒有依高分直接採用，也未以accept-best清除這三項。

### 插圖主批次修正與續製

- 第一輪完整批次已有30張selected，於07:06 UTC遇HTTP502停止。唯讀診斷確認當時正式站容器正在重建，`science-snow-slab` 精確資料庫查詢無job，local jobs亦無pending；保留已完成結果後正常接續。這不是vendor帳單稽核，未聲稱供應商零計費，也未更動主機或其他工作的部署。
- 實際像素覆核共找出八張材料性問題；修改八個prompt後產生11張候選，六張解除原問題。`hook-slope` 新圖卻在帳篷上生出臉形，`remaining-boots` 新圖帳門外呈海面，兩項另作窄範圍修正；沒有依judge高分直接當作合格。
- `hook-slope` 改成第八張原創SVG，明示高處帳篷、低處林緣與開闊雪坡，caption「位置關係示意／非現場影像・未按比例」。作者、root及獨立覆核者實看1920×1080原生預覽，0材料性／版面問題；proposal SHA `6ea4aae1bda99a279d1468c8307c9809e5f094747d5770270fa24a2f9836a7a0`，獨立報告SHA `0019b806756656bb1c6a0b40339db2462d95e46194f4b3d567c6620a8c1009c1`。
- 靴子景只將背景改成連續帆布內牆與穿布散射光，避免生成外景；此為取景限制，不宣稱1959帳門的封閉狀態。新提示已獨立覆核，selected實圖另行驗收。
- 07:23:30 UTC整合後source SHA `250e1d192dd7463cb3f73236a9eadcba52ceb0cb01b9ddb135d4428744eee5f9`、pictures hash `1cde42a6586e459b`；119句、speech hash `296feca213cf8271`、timeline SHA `f4ab52a1e7ccceccd88576b8bbc8f273cb35f204730ec3d4bb825c251305dc82` 保持。完整前版selected與take備份在 `slope-and-boots-integration/`。
- 原生lint仍0 errors／4 warnings；64張AI圖dry-run ready，全部每張最多三次估US$2.59，當時媒體帳本累計US$0.86（不是全片完整費用）。正常resume保留28張未變selected，補35張未生成圖與1張改提示靴子，未使用force。
- 繁中119條字幕語意覆核找出10處詞內斷行，已準備只改換行位置的修正及來源／時間綁定檢查；尚待正式captions輸出後套用。正式render、assemble、player字幕及完整播放／聽音仍待驗證。

### 全部插圖實看與科學畫面修正

- `keyframes-2026-10-12T07-23-37-181Z` 於07:56:45 UTC結束，exit1；產生60張候選，64個AI景均有selected，媒體帳本累計約US$1.67。exit1包括待修圖，不表示成片通過。
- 三組逐張覆核及前批修正回讀，全部64個當前selected實際看過。另確認13項材料性問題：4項改為原創圖解、9項只改提示詞。原生高分不能代替內容覆核；兩張只有輕微風格差異的圖另待原生保留程序，完整評語仍會進成片審核。
- 四個科學圖解為 `snow-over-step`、`platform-front-face`、`wind-moves-snow`、`slab-edge-displaced`。各有來源綁定提案、原生1920×1080預覽及獨立實看PASS，明示模型條件／示意／未按比例或非事故重演。舊圖的裸露巨崖、懸空雪拱、空中金色降雪和擬人滑雪者不再使用。
- 08:02:38 UTC整合收據 `_audit/science-repairs-integration/receipt.json`：source由 `250e1d192dd7463cb3f73236a9eadcba52ceb0cb01b9ddb135d4428744eee5f9` 更新為 `3f2fdb0864afaa199e994f47bb180c6662e2e46efcc74da2c307e4268353e5e0`，pictures hash `323a867570eabd15`。60個AI景、12張原創SVG，AI畫面占正文53.5371%；100景／119句／117狀態、speech hash `296feca213cf8271` 與timeline SHA `f4ab52a1e7ccceccd88576b8bbc8f273cb35f204730ec3d4bb825c251305dc82` 均未改。整合0供應商呼叫，完整前版source／selected／take／timeline／核准／媒體帳本先備份。
- 九個局部重畫景只修正物件接觸、雪塊形狀、人物誤入與地形脈絡；未動旁白、主張、look或camera。原生lint0 errors／4既有warnings，render及cadence預檢0問題。窄範圍dry-run一次估US$0.12、最多三次估US$0.36；正常keyframes續跑，不使用force，其餘51張當前AI圖沿用。新圖必須再實看，不能把提示詞審核算成圖片完成。
- 窄修批次 `keyframes-2026-10-12T08-03-20-728Z` 於08:12:52 UTC結束：16張新候選、60個AI景，圖片及judge帳本累計約US$1.89。三項native flag保留待處理；不是直接宣告全部機械通過。
- `snow-return-season` 三張均9.71分，原生同分取seed1，卻有中央吉祥物；root與獨立覆核者實看seed2、seed3均無人物，以seed2低圓雪坡最貼近用途。核對source／look／pictures／全部候選SHA、producer已退出、STOP與lease後，只把六個selected欄位改成既有seed2，0新呼叫。新圖SHA `4d1a6dde4ccf584a734a2a8f21e63fee15a932255f7c15a07f3732a4d9f54cbf`；仍保留judge.passed=false、needs_review=true、全部takes及原評語。備份收據 `snow-take-selection-2026-10-12T08-15-11-426Z/receipt.json`；共用工具後續另記[既有候選選圖任務](../../../tasks/open/2026-10-12-select-reviewed-existing-keyframe-take.md)，本集未改工具。
- 原生 `keyframes --accept-best slope-small-feature,field-weather,snow-return-season` exit0，僅3張已有實看可接受小差異的圖；重新產出聯絡表，保留所有take評語，成片明確要求站主審看。舊take的問題歷史不代表每項仍存在於目前selected。08:16覆蓋核查為60/60 AI目前SHA已實看可用、12/12 SVG預覽覆核完整、0未解material。
- storyboard review `3ba806bc-0250-4f10-9b96-35ee1c664de6` 於 `2026-10-12T08:16:23.222977Z` 送出，content SHA `9fe70948cf7fe998acdca585eb843cacb6ae3c8062fa17c15c55f80e760756c8`，60鏡／3頁聯絡表／3鏡保留。原生pull exit3及GET200讀回均pending；並未代替站主核准。繼續製作可供具體審看的成片，再請站主一併審看分鏡與成片。

`_audit/preflight-reviews.json` 與 `_audit/preflight-settings.json` 保存唯讀預檢。
`_audit/plan-check.json`、`review-push-2026-10-12T04-53-20-715Z.receipt.json`、
`reviews-2026-10-12T04-54-15.480Z.json` 與 `outline-review-pending.png` 保存當前送審、回讀與瀏覽器畫面。
本集只授權製作及上傳包；YouTube上傳、公開、PR合併和部署未執行。
