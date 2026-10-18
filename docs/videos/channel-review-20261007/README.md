<!-- 2026-10-07 由 Claude Code 分析 session 產出：18 支逐支診斷、7 份研究（research-1.md～research-7.md）、15 條頻道層級缺失的三方反駁、事實查核與完整性審查。
「<分析暫存區>」指該 session 的暫存檔（縮圖、故事板、CC、抓取結果），未進 repo；抓法寫在各研究檔開頭，可重抓。數字是 2026-10-07 的快照。 -->

# Mokaair YouTube 頻道診斷：缺失、修法、向誰學

- 對象：https://www.youtube.com/@Mokaair（2026-09-26 開台）
- 診斷日：2026-10-07
- 材料：資料包（channel_pack.md、ytdlp_meta.jsonl、18 支 zh-TW CC、縮圖、故事板）、產線規格（docs/videos、.agents/skills/youtube-video）、七份研究（本目錄 research-1.md 到 research-7.md）、15 條缺失的三方反駁（causal／pipeline／evidence）、六份事實查核、一份完整性審查。
- 規矩：只寫有證據的話，每個判斷標出處。沒有音檔，旁白聲音、配樂、音效、停頓全部是從 CC 時間軸、產線程式與設定推論的，文中一律標「推論」。沒有 YouTube Studio 後台數據（曝光、CTR、留存、訂閱來源），所以任何「這條缺失壓低了訂閱」都無法量測，只能給門檻。

---

## 1. 一頁摘要

### 1.1 現況數字（抓取時間不同，口徑標在旁邊）

| 項目 | 數字 | 出處 |
|---|---|---|
| 開台 | 2026-09-26，到今天 11 天 | about 頁 |
| 影片 | 18 支長片，0 支 Shorts，0 個播放清單，0 支預告片，頻道關鍵字空白，橫幅寫「旅行與生活的實用指南」 | channel.html／about.html／banner.jpg |
| 訂閱 | 3 位 | about 頁 |
| 總觀看 | 742（about 頁，10-07 09:08）；18 支逐支加總 782；10-07 下午重抓 797–800 | channel_pack.md、ytdlp_meta.jsonl、yt-dlp 重抓 |
| 每支觀看 | 中位數 24，平均 43；10 支低於 30 次；前 3 支（251／142／84）占 61%，前 5 支占 75% | channel_pack.md |
| 訂閱換算 | 約 0.4%（每千次觀看約 4 位）；76 頻道研究的中位數 1.91、P75 4.57／千次 | overseeros.com 2026-09-26 |
| 長度 | 397–843 秒，9 支不到 480 秒（自訂規格「長片至少 8 分鐘」） | ytdlp_meta.jsonl、docs/videos/README.md 第 25 行 |
| 上架 | 11 天 18 支；09-30 17:29 同一分鐘 4 支，10-05 07:38–08:36 一小時 4 支，其餘批次同分鐘成對 | ytdlp_meta.jsonl timestamp（UTC+8） |
| 互動 | 讚只抓到 S88lbAsLz2E 的 1 個，留言數全部抓不到 | ytdlp_meta.jsonl |
| 站內互導 | mokaair.com/zh-TW/videos 頁寫「這裡還沒有影片」，18 個 YouTube id 一個都不在；兩篇觀看最高的來源文章「這篇文章的影片」區塊為空 | 完整性審查，apps/api/app/video_reviews/public_api.py `_published` |

### 1.2 三句話診斷

1. **訂閱率不是異常值，觀看量才是。** 3÷742≈0.4% 落在 76 個頻道研究的中位數（0.19%）到 P75（0.46%）之間；異常的是 11 天只有 742 次觀看、18 支中位數 24 次。三個 causal 審查者各自獨立得到同一結論：瓶頸在觸及，不在「看完卻不訂」。而且 3 位訂閱的樣本多 1 位就差 33%，任何「某缺失壓低訂閱」在這個量級都分不出雜訊。
2. **產線把自家文章裡的答案抽掉，再把人送回文章。** 14 支把價格、降幅、日期、額度改成「以官網為準／我不唸」（cc09kA17Xsw 旁白 5 次加 5 組字卡；UOgxCymxb1I 字卡 `cut = None`），而這些數字就寫在說明欄連結的自家文章裡；結尾 18/18 唯一反覆出現的行動是「說明欄的文章」，旁白從未請觀眾訂閱頻道（18 支 CC 的「訂閱」全是「訂閱方案」）。這不是模型即興，是 tools/video/automation/prompts.mjs 第 44–45 行的 COMMON 規則與第 82 行的 outro 規則照寫出來的。
3. **觸及的槓桿都還沒拉：** 頻道頁是空的（無預告片、清單、精選、關鍵字，橫幅還寫旅遊）、站內→影片的連結是斷的（文章頁嵌不到影片）、Shorts 一支都沒上（產線已蓋好整條 tools/video/shorts）、縮圖 11 張同一版型沒有主體、上架成批而且沒有固定時段。這些跟訂閱率無關，跟「有沒有人看到」有關。

### 1.3 最該先做的 7 件事

| # | 做什麼 | 改哪裡 | 預期看哪個指標變化 | 工作量 |
|---|---|---|---|---|
| 1 | **把站內互導接上**：讓 18 支出現在 mokaair.com/zh-TW/videos 與各自文章的「這篇文章的影片」區塊。現況 `_published` 要 youtube_video_id 與 youtube_publish_at 都非空，Studio 手動公開的影片沒有後者。 | 站主在後台「可以上架」卡片對每支貼網址並填已公開時間；或開票讓 apps/api/app/video_reviews/public_api.py 第 66–72 行接受「有 id、由 Studio 公開」 | Studio 流量來源「外部」從 0 變成有；文章讀者是最便宜、最對口的第一批觀眾 | 小時 |
| 2 | **頻道頁衛生清單一次做完**：橫幅標語與說明前 45 字改成 AI 工具題；填頻道關鍵字；把 S88lbAsLz2E 設成未訂閱者預告片；建 3 個系列播放清單並勾官方系列；精選區塊放觀看前 4 支；18 支補置頂留言與結束畫面（指向同系列）；第三個 hashtag 統一成系列 hashtag | YouTube Studio（站主，約 1 小時） | Studio「訂閱來源」的頻道頁項、結束畫面點擊率 | 小時 |
| 3 | **先拿到數字再定縮圖與開場的優先序**：把 tasks/open/2026-09-27-ai-video-batch-first-week-analytics 的範圍從 4 支擴到已公開 18 支，站主匯出三張表：每支曝光／CTR／平均觀看比例、訂閱來源、流量來源 | YouTube Studio 匯出（Analytics API 沒有曝光與 CTR） | 門檻見第 6 節：CTR < 2% 才是縮圖問題；Intro < 60% 才是開場問題 | 小時 |
| 4 | **結尾加一句有理由的訂閱邀請、換掉三連請求的片尾卡**：outro 固定三句（回答開場問題、一個觀眾答得出的留言題、一句訂閱理由）；訂閱句放進正文 `outro` 場景由 TTS 唸；片尾卡換成只求訂閱 | tools/video/automation/prompts.mjs 第 80–82 行 outro 規則；.agents/skills/youtube-video/references/script-writing.md §結尾；docs/videos/STORY.md 第 52 行；新 outro.mp4 用 `branding --install` | 每千次觀看淨增訂閱（目前約 4）、留言數（目前 0） | 小時；舊 18 支只能 Studio 補結束畫面 |
| 5 | **數字說出口、免責只留說明欄**：官方頁抓得到就把數字講出口並在字卡標日期；官方頁 403（OpenAI 全家）但自家已查核文章有，允許引用並標查證日 | prompts.mjs COMMON（44–45 行）與 verifier（250 行）；tools/video/core/lint.mjs 加「為準／沒寫／不代表／我不唸」片語家族 warn（不做硬錯誤） | 平均觀看比例、留言裡「所以到底多少」類問題消失 | 小時 |
| 6 | **縮圖：先在 Studio 對 S88lbAsLz2E、UOgxCymxb1I、FYHFsj0SB7Q 做 Test & compare（B 版＝≤6 字＋一個主體），兩週後看 watch time share**；產線 QA 同步加三條：大字 ≤6 字、與標題前 10 字 LCS >50% 警告、兩行斷詞不拆詞；並統一 README／visuals.md／prompts.mjs 三處互相矛盾的縮圖規格 | tools/video/qa/thumbnail.mjs、tools/video/templates/templates.mjs `thumbnailHtml`、docs/videos/README.md 第 64 行、visuals.md 第 57–58 行、prompts.mjs 第 204 行 | 曝光點閱率；Test & compare 的 Winner | 小時（QA）；days（版型重做，等數字） |
| 7 | **上架節奏與選題配額**：長片每天最多 1 支、固定時段先跑 4 週；產量端把 draft_interval_hours／max_drafts_per_month 調到每週 3–4 支；每週至少一半常青題（AI 月費算盤、帳號守門員、Google 免費工具箱），標題前 15 字放產品名與一個數字、用搜尋建議裡的原詞 | 站主操作規則先行；apps/api 的排程照 video_shorts/slots.py 的 max_per_day 搬到長片（先把 2026-09-27-video-youtube-sync-field-test 做完）；publish.md §標題 | 每支首 7 天曝光；Studio「觀眾上線時間」28 天後定時段；搜尋流量占比 | 小時（規則）；days（排程器） |

---

## 2. 頻道層級的缺失

讀法：每條缺失原本都標 high／medium，三個 causal 審查者都把「對訂閱的影響」降到 low／unknown，理由一致：沒有 Studio 數據、樣本太小、觀看最高的影片同樣有這些缺失。下面每條都把「可驗證的事實」與「對訂閱的影響（假設）」分開寫，排序依「在訂閱路徑上的位置 × 可驗證程度」。

### 2.1 通過驗證的缺失（correction 已併入）

#### D03 結尾沒有任何一句請觀眾訂閱，唯一的行動是把人送出 YouTube

- **證據**：18 支 zh-TW CC 全文 grep「訂閱」，命中的全是產品訂閱（UOgxCymxb1I 9 次 Claude 訂閱用戶、eSg90eCfqOI 7:02／7:17 ChatGPT 個人訂閱、uoVKy-nFXB4 3:18 Google AI Ultra、FYHFsj0SB7Q 8:33「訂閱另一個更貴的方案」）；「追蹤／鈴鐺／按讚／頻道」0 次。6 支以「我們下一支影片見」收尾（U4ToEihqiJA 6:30、HCpjTmKqQrQ 6:48、KurEPz5z7hA 6:58、FYHFsj0SB7Q 11:17、eSg90eCfqOI 10:32、itKTQl3ehQE 9:59）但沒說是哪支；留言題只有 nG2-qsQCZmE 6:48、eSg90eCfqOI 10:24。10/18 旁白結尾說「說明欄的文章」，18/18 的 outro 投影片印 mokaair.com（templates.mjs SITE_LABEL）；另 8 支結尾只交代現實生活的待辦。片尾卡分兩種：UOgxCymxb1I 與 10-04 以後 7 支有 3 秒卡（「Mokaair」＋按讚／分享／開啟小鈴鐺三個圖示，沒有「訂閱」；依 BRANDING.md 第 4 行只有素材音效、無旁白，推論），09-27～09-30 的另外 10 支沒有片頭也沒有片尾卡，最後一句旁白後 1.2–1.9 秒就在深色 outro 卡上結束。`cta` 卡在片中段已推過一次文章（prompts.mjs 第 80 行），結尾是第二次。
- **這是規格造成的，不是執行落差**：script-writing.md §結尾「挑一個」、STORY.md 第 52 行「只給一個下一步」、prompts.mjs 第 82 行 outro 只寫「The last scene」、showcase fixture 的 outro cta 就是文章。tasks/open 沒有票在做。
- **對訂閱的影響**：low–medium，未量測。訂閱換算約 4／千次已高於 76 頻道中位數，結尾只影響看到最後的那一小部分人（看完率未知）。站主點名的黑貓研究院與 Gary Chen 抽查 4 支，結尾全是「按讚、訂閱（分享），下期見」加一個留言題。
- **修法**：(1) prompts.mjs outro 規則與 script-writing.md §結尾（STORY.md 同步）改成固定三句：回答開場問題、一個觀眾答得出的留言題、一句訂閱理由。單篇新聞片**不能自動填下一支題目**（AUTOMATION.md 第 83 行：企劃每 72 小時臨時挑題、成批同分鐘上架，撰稿時沒有「下一支」），訂閱理由改成頻道層的固定承諾（「每週幾支把 AI 新聞的數字拆開」）或指向播放清單；只有系列集（ai-terms、long-form）才能點名下一集，而 ai-terms 的「片尾指下一個名詞」（票 2026-09-29-ai-terms-video-pilot 第 6 步）還沒寫成程式。(2) 訂閱句放進正文 `outro` 場景由 TTS 唸（版型本來就有 lines 1–4，templates.mjs 第 172 行），不是蓋在片尾卡上；片尾卡要改成只求訂閱、拉長到 15–20 秒，換一包新 `outro.mp4` 用 `branding --install` 即可（branding.mjs 第 31 行允許到 900 格，`pace` 與 8 分鐘規定不計片尾）。(3) 結束畫面不需要片尾卡變長：YouTube 結束畫面放在最後 5–20 秒、已發布影片可在 Studio 直接加；18 支舊片 `--adopt-branding` 會被拒絕，只能在 Studio 補結束畫面與置頂留言。(4) 不必死守「只能求一件事」，參考頻道都是三連；真正缺的是「訂閱」這個字。「X 日那天我回來講結果」只適合說明欄確實寫了 11 月 12 日的 zxHRm5jnELc；zxHRm5jnELc 與 uoVKy-nFXB4 的旁白都刻意不說日期（前者 0:43 要觀眾看公告原文、後者 1:38 說公告沒寫）。
- **工作量**：hours（新片）；舊片站主 Studio 補。

#### D11 頻道頁沒有任何能把一次性觀眾變成訂閱者的東西，而且產線自己的規格沒落實

- **證據**：2026-10-07 活抓 @Mokaair 的 /playlists 與 /featured 都不存在（yt-dlp 回「does not have a playlists tab／featured tab」）；channel.html 與 about.html 只有一個分頁 /@Mokaair/videos，channelVideoPlayerRenderer＝0（無預告片）、shelfRenderer／playlistRenderer／reelShelfRenderer／postRenderer 全 0，channelMetadataRenderer 的 `"keywords":""`；連結只有一條「Mokaair 官方網站」。頻道說明第一句「分享旅行規劃與生活科技…亞洲城市攻略、AI 工具、軟體與架站」，橫幅（1707×282）寫「Mokaair 旅行與生活的實用指南」，但 18 支裡 0 支旅遊。18 支說明欄互相連結 0 次。系列標記只有 vxv8KrNual8 一支帶「｜AI 名詞十分鐘」（標題、縮圖 tag、標籤三處），其餘 17 支縮圖 tag 膠囊混用產品名、分類名與題目。至少五支是「這個數字是誰說的」同型片（UOgxCymxb1I、cc09kA17Xsw、UWYoO3JfOK0、HCpjTmKqQrQ、uoVKy-nFXB4）彼此沒串。vxv8KrNual8 的 CC 最後 90 秒（12:29–13:58）沒有指向下一集或文章，說明欄只放站上總索引。
- **規格有、執行沒有**：publish.md 第 42–43 行要求「放進對應系列播放清單」「結束畫面指向同系列下一支」；ai-terms/README.md 第 82、91 行要求片尾指已發布那一集、第一集公開當天建總清單與分類清單（terms.json 連五語清單名都備好了）；10-05 上架至今沒做，terms.json 的 large-language-model 列仍是 backlog、video_id 為 null。
- **對訂閱的影響**：未量測。同量級對照不支持它是訂閱率的原因：Whoops SEO（標題格式固定、無 playlists tab）18 訂閱／4,513 次≈0.40%，與 Mokaair 相同；Ada｜AI實習生有 4 個清單與 4 個精選區仍只有 0.24%。要知道頻道頁有沒有在流失訂閱，先看 Studio「訂閱來源」報表（觀看頁 vs 頻道頁）。YouTube Help 3219384 說預告片是給未訂閱者「learn more and subscribe」用的（沒有「最好的資產」措辭）；Help 6084043 說系列播放清單裡的影片會互相 featured and recommended。
- **修法**：A. 站主在 Studio 立刻能做：改說明前 45 字與橫幅標語、填頻道關鍵字、把 vxv8KrNual8 或 S88lbAsLz2E 設成未訂閱者預告片、建「AI 名詞十分鐘（全部）」等清單並勾官方系列、精選區塊放觀看前四支。B. 不要做「30–60 秒預告片、站主本人聲音或露臉」：schema.mjs 第 53 行 MIN_EPISODE_MINUTES=8、formats.md 第 3 行不到 8 分鐘不交短片，且與頻道「無真人」前提相反；若要做就寫明是站主自己另外製作。C. OAuth scope youtube.force-ssl 已涵蓋 playlists.insert／playlistItems.insert（HANDS-OFF.md 第 130 行、client.py 第 27 行），缺的是 apps/api/app/video_youtube/sync.py 的 insert 方法（目前只有 playlistItems.list），每支約多 50–100 單位；「官方系列」旗標 Data API 沒有，仍須 Studio 勾。D. 系列名放**後綴**、不編集數：ai-terms/README.md §站主的決定明定不編號、名詞放最前面（手機只顯示前約 40 全形字）；publish.md 寫明網站拒絕動已公開的影片，18 支改標題只能 Studio 手改。E. 「之後每支先決定系列再寫稿」可行但要開票：category 只存在後台、不送 YouTube；video.json 的 series 只給漫劇用。F. 拆第二個頻道是產品決定：VideoYoutubeConnection 是單列（models.py 第 2294 行起），HANDS-OFF.md 分類表本來就把 travel 排在同一頻道。
- **工作量**：Studio 部分 1 小時；sync.py playlist 一張票。

#### D05 18 張縮圖只有 2 張有勉強對得上主題的主體；11 張同一版型只換字

- **證據**：thumbs_sheet.png 第 8–18 格（09-27～09-30 上架的 11 支）全是 tools/video/templates/theme.css 第 229–230 行 `.thumb-art` 的青綠圓環＋橘點，沒給 keyframe 背景就畫這個；#1–#7 用關鍵影格鋪底，但主體是影片裡的比喻：cc09kA17Xsw 三個廚房人員（0:31 才出現的「飯店主廚泡麵」）、xSrFAMk_udE 盆栽與鉛筆、vxv8KrNual8 手拿綠傘、LzAwyF-7-H4 雜貨店收據（大字沒有「網域」）、1I0KIfGi-0Q 暗房檯燈，只有 #3 uoVKy-nFXB4 的手機、#7 UWYoO3JfOK0 被打穿的磚牆對得上題目（貓只占寬度約 2%）。大字以 CJK 計 11/18、連英文詞計 13/18 超過 visuals.md 第 57 行的 6 字；但產線程式碼上限是 12 字（compilation.mjs:29、plan.mjs:36），18 支全過，落差在文件與程式之間。大字與標題最長共同片段 ≥50% 者 11/18，完全照抄的是 LzAwyF-7-H4、zxHRm5jnELc、nG2-qsQCZmE、eSg90eCfqOI（uoVKy 是濃縮、UOgx 是副標逐字、#2「到期日」算改寫）。拆詞實例：HCpjTmKqQrQ「一半的攻／擊」、zxHRm5jnELc「建議日不／是生效日」（FYHFsj0SB7Q 的「你／符合」不算拆詞）。縮到 160–168px 大字兩行可讀，副標、標籤膠囊、MOKAAIR 糊掉。對照：黑貓產品特寫＋貓、Gary 真人臉＋道具、科技兔 Ozr75-oQEFg（20,517 次）四張方案卡、可波 kobatalk 黃金獵犬吉祥物＋OpenAI logo；原稿引的「PAPAYA 鎖頭 259K」資料裡找不到，已刪。
- **規格互相矛盾**：docs/videos/README.md 第 64 行「縮圖用 thumb 版型：一個標籤、一行大標、一行小字，左下角是 MOKAAIR」（沒有主體）、visuals.md 第 57–58 行「≤6 字＋一個視覺主體、不重複標題」、prompts.mjs 第 204 行「≤10 字兩行」三份不一致；#1–#7 的比喻化是 ILLUSTRATED.md 第 171 行「比喻來自觀眾的日常」的設計決定。
- **對訂閱的影響**：unknown／indirect。縮圖只作用在「曝光→點擊」，不影響「看完→訂閱」。頻道內資料不支持它是觀看差異的主因：觀看前四名（251／142／84／71）全是同一版型，同版型內 HCpjTmKqQrQ 6 次 vs S88lbAsLz2E 251 次差 40 倍，版型一樣——差異由題目決定。沒有 CTR 就分不出「縮圖壓低點擊」與「新頻道還沒被推薦」。
- **修法（照順序）**：(1) 站主先看 18 支的曝光、CTR、流量來源；瀏覽／推薦的 CTR 低於 YouTube 常見的 2–10% 區間下緣才升級成優先項。(2) 先用 Studio 的 Test & compare 對 S88lbAsLz2E、UOgxCymxb1I、FYHFsj0SB7Q 試一張「≤6 字＋主體」的 B 版（只能桌機 Studio、要進階功能、兩週內結束、曝光不足回 Inconclusive）。(3) 低成本直接修：qa/thumbnail.mjs 加「大字 ≤6 字」「兩行斷詞不拆詞（Node 22 的 Intl.Segmenter）」「大字與標題前 10 字 LCS >50% 警告」；統一三份規格。(4) 版型改 tools/video/templates/templates.mjs `thumbnailHtml`／theme.css `.thumb`（不是 .agents 裡的 thumbnail.html），文字欄縮到左 40%、右 60% 給主體；主體來源：在 prompts.mjs 第 204 行補「縮圖鏡頭」規則（主體在右三分之一、鉤子段落的鏡頭、畫具體物件而非比喻），舊 11 支可為縮圖多畫一張（ILLUSTRATED.md 第 194 行：約 US$0.11–0.41）。**產品 logo／介面截圖目前不可行**：look 的 negative 擋 logo 與文字（ILLUSTRATED.md 第 170 行）、SKILL.md 規矩 6 與 thumbnails.md 明寫縮圖不放 logo，要用得先由站主改規矩。固定吉祥物不能靠樣張那隻貓（樣張依 look_hash 每支重畫），做得到的是一張固定 PNG 由版型疊上（同 sothatswhy 印章做法），而且站主 2026-09-28 對原來如此事務所已回覆「不用吉祥物」。MOKAAIR 不要放右上（thumbnails.md §安全區把 x 1140–1280、y 0–140 列為懸停按鈕隱藏區）。「連續兩支不得同色」需要跨影片狀態，先用「底色跟主體主色」。(5) A/B 已內建（templates.mjs `thumbnailVariants`、UPLOAD.md 已寫 Test & compare 步驟），缺的是 slides／插圖投影片的撰稿提示沒要求變體，所以 18 支一張 B 版都沒出；回填贏家目前只寫進 brief.md，產線沒有階段讀它。(6) **舊 11 支在 Studio 換縮圖會被產線蓋回去**：apps/api/app/video_youtube/state.py 兩種模式的步驟都含 thumbnail，sync.py `_thumbnail` 用 run.package.thumbnail 再送一次；要先給同步加「站主已在 Studio 換過就跳過」的開關。
- **工作量**：hours（QA、規格統一）；days（版型重做，等 CTR 數字再決定）。目前沒有票；2026-09-27-ai-video-batch-first-week-analytics 卡在等數據。

#### D04 標題承諾的數字在片裡被「以官網為準」整個抽掉，而這些數字就在自家文章裡

- **證據**：至少 10 支標題或縮圖承諾的那個答案（價格、降幅、日期、額度、是非題）在片裡被推回官網：UOgxCymxb1I（旁白無任何百分比，191–201s 字卡 `cut = None  # 填入官網公布的降幅`，157–171s 表格降幅欄寫「以官網為準」，說明欄參考資料那行自己寫「牌價降 20%…40% 是 Anthropic 的成本估計」）、xSrFAMk_udE（112–117s「Gems 停止支援時程（Google 的說法）」日期欄寫「以官網為準」；2:41、6:46「以官網為準」，另 3 句推回官網；文章有 11 月、2027-03、2027-06）、S88lbAsLz2E 2:43「數字我就不放在畫面上了」（文章有每月 6 部／50 部）、LzAwyF-7-H4 4:05「我不在這裡替你填數字」、cc09kA17Xsw（旁白 1:08、1:52、2:03、6:30、6:53 五次「以官網為準」加 6:36，字卡 69s／74s／118s／123s 加 89–108s 五格表頭「數字以官網為準」；blog 明寫 up to 30%、86.6% vs 96.6%）、KurEPz5z7hA 4:30／4:47／5:26（文章有 $4/$20→$2/$10）、1I0KIfGi-0Q 2:46「實際單價我不唸」（AWS 公告 38k→81k token）、zxHRm5jnELc 0:43 不說 11/12（說明欄自己寫了）、FYHFsj0SB7Q 10:51「片名裡的問號，今天先留給你自己回答」、nG2-qsQCZmE 三問中兩問推回官網（第三問 3:45 有答「完成課程不等於取得證照」）。另外 4 支（uoVKy-nFXB4 5:13、U4ToEihqiJA 5:21、_v1vc2s3_MU 4:51、HCpjTmKqQrQ 2:11 用「假設的數字」而文章有 ENISA 60.4%／5.2%）標題承諾有兌現，但把次要數字也推回官網。7 篇站內文章抽查全部有數字。18 支 CC 詞頻：公告 65、官網 52、為準 31、沒寫＋沒有寫 31、不代表＋不等於 26；但其中 zxHRm5jnELc 的 22 次、FYHFsj0SB7Q 的 15 次「公告」是題目本身在拆公告，不算免責。「黑貓同類詞 0」只核到 coA8iBMMLY4 一支（它是歷史故事，不是同類題）。
- **這是產線規則**：prompts.mjs 第 44–45 行 COMMON「Numbers, prices, limits, versions and dates come only from an official page in sources whose text you can quote. None there: say it without the number, or 以官網為準 on the slide」、第 250 行「Third-party pages never confirm a number」——自家文章雖在 sources 第一位也被排除；人工路線 SKILL.md 第 73 行同樣。「精確數字放字卡」（script-writing.md 第 17、69 行）是規定了沒做到。免責句已在 14 支的說明欄各有一句，旁白與字卡又各念一次。HANDS-OFF.md 第 44 行草稿第 2 條只在「查不到或登入才看得到」時才要「以官網為準」，本來就相容；主機上的立場是 10 條、存在 channel_stance 設定，改 HANDS-OFF.md 不會改到正式站。
- **對訂閱的影響**：unknown／low。兩支最明顯的例子正是全頻道觀看第 1、第 2 名（S88 251、UOgx 142，合計 53%），同批上架互比無差異，0 則留言、無每支訂閱數據；它是回訪與信任的長期假設，不是現在 3 位訂閱的解釋。
- **修法**：(1) 改 prompts.mjs COMMON 與 verifier，不改 HANDS-OFF.md：官方頁抓得到就把數字講出口，字卡用現有 `stats.source`／`quote.source` 標「官網 YYYY-MM-DD」；官方頁抓不到但自家已查核文章有（帶 checked_on）時，允許引用並標文章查證日；免責只留說明欄那一句。(2) NOT FOUND 的處理不用改：prompts.mjs 第 254 行已是「drop the number or the sentence」。(3) lint 加片語家族計數（為準／公告沒寫／不代表／我不唸）做成 warn()（lint.mjs 第 237 行已有這層），不要硬錯誤，否則撰稿的 lint_errors 迴圈只會換同義句。(4) 「擴到說明中心」只對 Google、Cloudflare、AWS、Anthropic 可行：OpenAI 的 help.openai.com、chatgpt.com/pricing、openai.com 對工人的 Mokaair-editorial UA 回 403（本機實測，與票 2026-09-28-video-1m-vibe-coding:59、2026-09-28-video-1m-free-vs-paid:82 一致），nG2-qsQCZmE、KurEPz5z7hA、zxHRm5jnELc 要靠第 1 點放行自家文章；U4ToEihqiJA（Google 可用性表 support.google.com/gemini/table/17434654：10 個 US only、全部 English only、18+）才是真的漏查，而且漏在上游文章。(5) 8 分鐘下限由 REGISTER_RULES 已要求的「數字一次一個、接著它對觀眾的意思」補回。
- **工作量**：hours；OpenAI 題目的抓取路線另算。沒有票在做。

#### D08 18 支沒有一張真實畫面；教學片用文字 STEP 方塊代替設定頁

- **證據**：18 張 sbsheets 核對，沒有任何瀏覽器／App 截圖或螢幕錄影（唯一淺色格是產線自畫的示意圖卡）。教學片：_v1vc2s3_MU 197–237s 共 7 格 STEP（4＋3）、S88lbAsLz2E 226–245s STEP 1–5 且 98 格無 Vids 介面、U4ToEihqiJA 196–210s 三個有字的 STEP 方塊（CC 3:26「選項名稱以你看到的台灣介面為準」）、uoVKy-nFXB4 344–354s STEP 1–3、KurEPz5z7hA 186–196s 三步；itKTQl3ehQE 202–212s 用自標「示意」的對話氣泡代替真實 Permission denied 輸出；xSrFAMk_udE、cc09kA17Xsw、U4To、LzAwyF、vxv8 的說明欄都自承「示意／沒有實測」。舊 11 支純深色字卡平均一張停 7.0–10.1 秒，15 秒以上不動的時間占 5–45%（9 支在 17–45%），單張最長 15–30 秒——但這是故事板比對看不見單行 reveal 的量測誤差，產線自己的 15 秒／狀態規則（qa/pace.mjs，09-26 起）並未被違反，站得住的說法是「每約 10 秒多一行字的深色卡片，觀眾眼裡等於靜止」。新 7 支約 5 秒一換，但場景從不落在影片真正的主角物件上，至少 4 支用了 visuals.md 第 17 行禁用的物件（LzAwyF 14s 筆電／19–24s 沙漏／350s 機器人；xSrF 132–137s 沙漏；UWYo 19s、383–393s 筆電；1I0K 310s 沙漏、439s 筆電）。對照：PAPAYA 電腦教室 Google passkey 教學（NLiarcXvgns，258,777 次）是真實登入畫面與手機設定錄影，鄰近題目非同題。
- **這是規定出來的**：prompts.mjs 第 103 行「Do not use diagram or screenshot: automated videos have no image files」；2026-10-01 已落地的 Playwright 截圖場景 `screencast`（tools/video/screencast、worker 映像含 Chromium）沒接進撰稿提示。policy 品管只把旁白送給 Jev（qa/policy.mjs），看不到畫面，所以「念出步驟」就算有示範。禁用清單是 2026-10-03 才加進撰稿提示、沒有 lint，而這 7 支的分鏡在那之前就寫好（ILLUSTRATED §第二輪）。「每章換地點、比喻取自日常」是 ILLUSTRATED.md 第 171 行與 drama.mjs pictureVarietyProblems（同地點 >1/3 即警告）要求的結果。8 秒狀態上限已在 cadence.mjs 實作（含章節卡、outro 卡），不必再做。
- **對訂閱的影響**：low／未證實。沒有留存資料（heatmap 全 None）；黑貓研究院兩支 96–97% 格子是 AI 插圖、零截圖，仍 5.5 萬訂閱；Gary Astra 片在同一把尺 thr8 下 71% 時間停在 ≥15 秒畫面，仍 26.4 萬觀看；頻道內觀看前四名全是舊版慢節奏純字卡。三支「怎麼開／怎麼連／怎麼送出提示」的教學片沒讓觀眾看到承諾的畫面，應併入 D04「標題承諾未兌現」看。
- **修法**：(1) 全自動可做——解禁並要求撰稿對 video.json `sources` 裡的公開官方頁各放至少一個 `screencast` 景（capture+focus+zoom 框出引用段落），lint 要求 `steps` 景必須有同章的 screencast 或標記「登入介面，待站主錄」，禁用詞做成 shot prompt 的 lint 錯誤。(2) 登入後的介面（Meta、Gemini、Google Vids、ChatGPT 選單）全自動做不到：screencast 不登入、profile 只給站主，要站主用 OBS 錄並走 tasks/open/2026-09-24-video-obs-import（P3 無人認領）。(3) 「一支影片一個場景世界」是反轉 2026-10-03 的設計，要同時改 ILLUSTRATED.md、TEMPLATE_GUIDE 與 pictureVarietyProblems，先交站主決定；插圖版該學的是黑貓「畫主題本身」。(4) 重做舊 4 支會是新影片 id，S88 的 251 次歸零，不建議。
- **工作量**：days（screencast 接線）；登入介面 needs-owner。

#### D09 頻道沒有可辨識的「人」

- **證據**：旁白全程第一人稱「我」（每支 2–15 次），但 18 支從不自報名字，只有 zxHRm5jnELc 0:48 說過「如果你是第一次來，這裡是 Mokaair，專講 AI 工具」；插圖人物每支不同、縮圖只有 MOKAAIR 字標、片尾是通用圖示卡，沒有吉祥物或重複角色。頻道曾有半固定收尾句「完整整理在說明欄的文章裡，我們下一支影片見」（09-27～09-30 的 6 支），10-04 之後的 8 支拿掉了。「我的看法是」在 5 支裡用 3–5 次（_v1vc2s3_MU 5 次：1:07、2:49、5:11、5:33、6:16；nG2-qsQCZmE 4＋1 變體；HCpjTmKqQrQ、uoVKy-nFXB4 各 3；UWYoO3JfOK0 1＋3 次「以我的看法」），其餘 13 支 0–2 次。節拍：依 tools/video/core/timeline.mjs 每句後固定補 300 ms、每景末再加 700 ms，captions.mjs LINGER_MS=400 讓 CC 只在換景處露出 0.60–0.63 秒間隙（U4ToEihqiJA 25 處、HCpjTmKqQrQ 23 處、itKTQl3ehQE 45 處，章節起點全落在這些間隙上）——**原稿把它當句間停頓是讀錯了**；09-30 以前 10 支的停頓完全由這兩個常數決定，10-04 起 8 支已有 0.6／0.9／1.2／1.5 秒的 PAUSE_BEATS 節拍（register.mjs hook／reveal／cliffhanger），但每句仍是同一個 300 ms；整景一次合成早已是現況（tts/requests.mjs「one request per scene」），節拍器來源是每句統一的 800 ms `<long pause>` 被切掉後補回固定 300 ms。配樂音效：2026-10-03 設定快照無 slides_music_track／slides_sfx_set（票 2026-10-03-produce-video-openai-devday-2026-recap 第 93 行），README 第 30／70 行純投影片預設不放——推論 18 支皆無配樂音效，10-04 起 7 支插圖投影片依 settle() 應自動掛上卻因設定空白而沒有；settle() 丟掉 `voice.performance` 在 ILLUSTRATED §聲音表演與已結票 2026-10-05-voice-performance-contract 都註明是一行 follow-up，但沒有開票。對照：黑貓 coA8iBMMLY4 一支「我們」22 次、「謝謝」2 次、片尾「歡迎在下面留言告訴我…我們下支影片見」；可波片尾 KOBA 狗卡。無音檔，實際聽感只能推論。
- **分三層**：(a) 設計空白——自稱不受 GREETING 正則約束（register.mjs 第 54 行只是 restyle 的統計旗標，真正禁問候的是 REGISTER_RULES 的「No greeting」那一行），口頭禪與固定收尾句的位置就是後台「各階段常設指示」（stage_instructions），票 2026-10-03-ai-term-system-one-model-video 已註明「unless the channel has its own catchphrases」；固定句不能放第一句（說書式規則要求第一句是鉤子）。(b) 執行落差——配樂音效設定空白、voice.performance 被丟。(c) 規格使然——「我的看法是」是 prompts.mjs 第 46–47 行與 script-writing.md 第 47 行強制的意見標記，聽稿模型會回報未標記的意見；覺得空洞是 HANDS-OFF 的 7 條立場草稿太泛，要站主改立場。
- **對訂閱的影響**：未證實。黑貓研究院（55,200 訂閱）同樣無名、無「大家好」、以「我們」說書，差別只在每支固定以一句請觀眾訂閱收尾（已併入 D03）。
- **修法**：人設（名字或自稱、固定收尾句、口頭禪）寫進後台 stage_instructions 與頻道立場（已有 10 點，是加進去不是新寫）；站主放一首授權音樂床與音效組到 _music／_sfx 並填 slides_music_track、slides_sfx_set（phase-0 setup 已在 ai-term-system-one-model 票裡）；開一張票讓 settle() 保留 voice.performance；改「保留量到的停頓長度」而非整景合成；「我的看法是」每支最多一兩次。吉祥物要把漫劇的角色／look 機制接到 slides、改 thumb 版型與片尾素材，且站主 09-28 已回覆不用，列為選項；雙說話者需開放 `speaker` 給 slides 並處理四條配音軌；ElevenLabs 產線無此供應商，只能產線外試聽（約 US$0.6／支）；站主錄 5 秒片頭可行但換素材包後舊片須重審。
- **工作量**：needs-owner（人設、音樂檔）；hours（settle、stage_instructions）。

#### D12 上架節奏：11 天 18 支、成批公開、沒有固定時段，而且沒有任何程式在強制自家規則

- **證據**（ytdlp_meta.jsonl 換算台北時間）：09-27 21:17、23:53×2；09-28 13:10×2；09-29 22:40×2；09-30 17:29:29–38 四支（9 秒內）；10-05 07:38、08:29、08:36×2（3 支 7 分鐘內、4 支 58 分鐘內；原稿寫「同一分鐘三支」是錯的，1I0KIfGi-0Q 早 7 分鐘）；10-07 12:19、12:20、15:39。全由站主在 Studio 手動公開（README.md §上架「公開或排程，永遠由站主自己按」）。以 YouTube 官方「每位觀眾每頻道 24 小時最多 3 則通知；短時間發超過 3 支可能暫停 24 小時通知」（support.google.com/youtube/answer/7389684）計，24 小時內超過 3 支的窗口至少三個：09-27 21:17 起 5 支、09-29 22:40 起 6 支、10-05 一小時 4 支。違反 DESIGN.md:144 自訂的「一週 1–2 支，站主看完才上架」，而 apps/api、tools/video、tasks/open 都沒有程式或設定在強制；MILLION-VIEWS.md:61 的「一週 1–2 支」是那六支（尚未上架）的建議，同檔:65 又寫「六支一起上」，HANDS-OFF.md:104 以每天兩支估磁碟，STORY.md 每日配額 12:00、20:00 各一支——repo 內部節奏規劃互相矛盾。
- **對訂閱的影響**：low（現階段）。訂閱者只有 3 位，通知截斷的實際損失趨近零；YouTube 官方說同頻道每日被推薦的支數沒有上限、演算法不依上傳頻率最佳化；09-30 連發四支那批反而拿到全頻道第 1、2 名（251、142，約占 56%）；OverseerOS「前一支掉到 0.86 倍」一文自己聲明無法區分 cannibalization 與一般 launch decay（12 個事件），不能當佐證。黑貓研究院每天 09:00 固定一支（13 天 15 支）、Gary Chen 每 2–5 天一支，兩個成功頻道節奏差三倍。真正的問題是節奏完全隨機，28 天後站主無法用「觀眾上線時間」回答任何問題，也分不開同批 251／142／32／13 的差距是題目還是順序。
- **修法**：(1) 先在產量端定節奏：/admin/videos 設定分頁的 draft_interval_hours／max_drafts_per_month 與故事線 episodes_per_day 調到每週 3–4 支，沿用 STORY.md:200 的背壓（「可以上架」等待超過 N 支就不開新草稿），否則 20 GB 檔案區三到四週滿；站主在 DESIGN／STORY／HANDS-OFF 之間選一個節奏並改文件。(2) 上架端不另造排程器：先把票 2026-09-27-video-youtube-sync-field-test 做完（publishAt 從未在真頻道跑過，sync.py 第 334–339 行只擋五分鐘之後），再照 apps/api/app/video_shorts/slots.py＋rules.consent_scope(max_per_day) 與 admin-video-stories.tsx 的「下一個空時段」做長片時段表，sync.py 送出前比對同頻道 24 小時內已排或已公開的影片。(3) 在 (2) 上線前是站主的操作規則：每天從 Studio 最多公開一支、固定時段，寫進 README.md §上架與 publish.md 檢查表。(4) 新聞類題目要有例外，否則固定佇列會讓時效題過期。
- **工作量**：規則 hours；實測 days（站主動手）；時段表一張獨立票 1–2 天。

### 2.2 被反駁的缺失：原本以為、為什麼不成立、留下來的事實

| 原本以為 | 為什麼不成立 | 仍成立、可以用的事實 |
|---|---|---|
| **D01 選題決定天花板**：7 支題目在台灣沒人搜，「拆數字」角度把觀眾切到幾十人，應加「建議詞為空就降級成文章」的硬關卡 | 上架時間先解釋掉大半差距（觀看最低 5 支裡 4 支上架不到 2.5 天）；同日對照不符合公式（09-30 批：Google Vids 251、「拆數字」的 Opus 5.5 142 排第 2，照公式寫的「OpenAI Academy 要錢嗎？台灣能修嗎？」只有 11）；suggestqueries 對「Google Vids」「Google Vids 免費」回空清單，硬關卡會砍掉頻道第一名；「6/7 題沒建議詞」為假（Cloudflare WAF 10 個、OpenAI Cursor 9 個、Gemini Connected Apps、Grok 4.7、資安新聞、AI 代理人都有）；引用的 uoVKy-nFXB4 1:17「一般人只會間接碰到」是假引用（那句在 1I0KIfGi-0Q 1:22）；同角度小頻道 Whoops SEO（17 訂閱）觀看是 Mokaair 的 2–3 倍；Opus 5.5 同題 AI 好友 205（2,450 訂閱）、黃敬峰 136（2,090 訂閱）、Mokaair 142（3 訂閱）——這題在台灣就是這個量 | 同日上架的比較顯示題目有差（09-30：251／142／32／13；10-05：21／3／2）；Cloudflare Auto Router、資安百分比分母兩題確實沒有競爭內容與建議詞；MILLION-VIEWS.md 第 7、11 行早已寫「題目的搜尋量」「時效題＋常青題各半」但沒執行；題目池是 news_automation/sources.json 的廠商部落格，台灣來源票 2026-09-30-news-automation-has-no-taiwan-sources 仍 P1 開著 |
| **D02 新聞題晚 4 天到 5 週、沒有一支趕在 48 小時內、13/18 是 3–7 天過期的公告** | _v1vc2s3_MU 文章 09-29、上架 09-30 09:29Z，不到 34 小時；晚 32–38 天的三支是開台前的庫存（頻道 09-26 才建）；開台後穩態延遲 5–7 天；延遲與觀看無相關（Spearman 0.119；晚 38 天的 FYHFsj0SB7Q 84 次是第三名）；zxHRm5jnELc 晚 32 天仍在「OpenAI Cursor 停供 模型」排第 1，壓過 3 天內上架、1 萬多訂閱的競品；ytgrowth 的 98.9% 是 News 類，Mokaair 分類是 Science & Technology（83.9%）；Gary Chen 10-03 的 Opus 5.5 常青框架片 40,275 次比 09-29 的新聞片 22,893 多近一倍；18 支標題多數已是「誰能用／該不該」的常青寫法 | 說明欄 slug 日期 vs 上架日的落差存在（Opus 5–6 天、Cursor 32 天、學生方案 38 天、Hugging Face 事件 41 天）；延遲主要在前端選題與站主上傳，不在製作（票 2026-10-03 DevDay：新聞 09-29、10-04 過關、10-07 仍未上傳）；修法「超過 72 小時自動改寫標題」不是 hours 的事（標題、說明、縮圖都綁雜湊） |
| **D06 標題中位 40 字、手機只看前 20–25 字、鉤子都在第 20 字後、6 支同一句型、用詞不是使用者打的詞** | 「手機 20–25 字」沒量過（creaticalc 只量拉丁字元約 50；publish.md 寫 40），三個數字互相矛盾；14/18 標題前 10 字就有產品名；Spearman（字數 vs 每日觀看）＝+0.12；fix 要禁的「、」列舉與「怎麼讀」正是頻道第一名 S88 的寫法；志祺七七標題平均 50.5 字、97% 用「｜」仍中位 41.9 萬；「你 0%」為假（4/18 含你）；「通行金鑰」在 YouTube 搜尋已被對到「通行密鑰」，_v1vc2s3_MU 在「臉書 雙重驗證 通行金鑰」排第 1；FYHFsj0SB7Q 片中明說 Plus 方案，競品的「Google AI Pro」是 2025-10 的舊方案 | 標題確實偏長（中位 40、最長 57，9 支 >40）、6 支用「是誰測的／怎麼讀」媒體識讀句型（參考頻道 150 支 0 支）、只有 5/18 含數字且多為版本號、三個搜尋詞錯位（網域 續約價 排第 1 卻 2 次＝沒人搜；FYHF 標題無 Gemini／Google AI；KurE「GPT-6 出了」撞 Astra 意圖）；40 字與前置重點是 publish.md 寫了、prompts.mjs 只檢 100 字與角括號 |
| **D07 開場把人趕走：5 秒無聲片頭＋10 秒標題卡、13/18 唸目錄、落鉤普遍超過 20 秒、鉤子評分全 2–3** | 標題卡實停 4.8–6.9 秒（CC 句首對照故事板，第一張插圖在 9.8–11.9 秒，不是 14–19 秒）；真正「第一…第二…最後」的目錄是 09-27～09-30 的 6–7 支，新 7 支被算進去的是規格要求的「承諾句」，而規格自己矛盾（script-writing.md 第 8 行與 README 第 69 行要「怎麼進行」、第 33 行說「不報目錄」）；照產線自己的定義約 10 支在 20 秒內落鉤，超過的集中在 10-04 後的插圖批；觀看最高的 S88（15 秒標題卡＋16 秒目錄）與 UOgx 都有這條缺失，開場分數與觀看分不開；留存報表要 ≥100 次觀看，只有兩支過；「無聲片頭」沒有音檔（BRANDING.md 說沿用素材音效）；「正文第一句前 ≤2 秒」的 lint 量不到（片頭在 intro.mp4 裡，時間軸從第 0 格就是第一句）；5 秒片頭是站主決定，票 2026-10-04-adopt-approved-devday-bookend 正在把片頭補進舊片 | 10-04 後 8 支（含 UOgxCymxb1I）第一句在 5.0 秒、前 10 秒只有片頭與標題卡；第一章長度 16–147 秒、lint 只 warn 且被票據忽略（DevDay 票第 118 行「38 s against the 20 s hook target」）；標題卡先出現是規格（formats.md 第 73 行），但產線已有反例可抄（lint.mjs 第 224 行對合集集數是 error「drop the title card」）；「你以為…其實」是站主 09-29 的決定，不是毛病 |
| **D10 稿子在湊長度：同一結論講 4–9 次、比喻每 20–40 秒換、8 分鐘規定逼出重複、9/18 不到 480 秒** | 8 分鐘下限 10-01 才定，重複最多的 9 支全在 09-27～09-30 上架；重複最多的恰好是最短的片（KurE 422s、_v1v 405s）；重複是說書規格的設計（script-writing.md 第 27 行「重點講兩次」、每章首尾各一句、每章至少一個比喻）；被點名最重複的四支正是觀看最高的四支；規定後只有 uoVKy 438、1I0K 464、LzAw 474 三支不足，原因是 lint 用 250 字/分估、實際 265–278（automated.md 第 127 行已記錄）；「一支一個比喻世界」撞 prompts.mjs 第 109–111 行與 DESIGN.md 營利政策段；「新資訊只占三分之一」沒有量法 | 重複次數查得到且多半低估（KurE「一般對話裡還沒有」8–10 次、itKT「指示裡的不要擋不住」10 次、uoVK「沒開放給一般用戶」10 次、FYHF「沒有台灣」8 次）；湊時間段秒數對（zxHR 3:16–4:44 88 秒教算日期差、FYHF 5:48–8:04 136 秒離題示範）；比喻每 20–40 秒換只在 10-05／10-07 的 6 支插圖片成立；prompts.mjs 第 230 行「never pad to reach it」是規定了沒做到；CPM 校準沒有票 |
| **D13 說明欄前兩行放網址、11 支黃金區放免責、旁白說第一行但連結在最底下（3 支）、標籤五語混放、章節是英文** | 「連結放第一行」是站主 09-26 看了 Gary Chen 參考片後自己定的（tasks/done/2026-09-26-videos-learn-from-a-reference-chapter、metadata.mjs composeDescription 註解），publish.md:16 與 README §說明欄是沒同步的舊順序；11 支免責全在第 5–11 行，「顯示更多」之後，不在黃金區；指路錯的只有 2 支（cc09kA17Xsw 363s、xSrFAMk_udE 188s，正好是改成新順序的最新兩支——是旁白模板沒跟著改），UWYoO3JfOK0 的 L1 就是連結；章節英文是 yt-dlp 預設 hl=en 的假象（帶 lang=zh-TW 重抓是中文）；五語標籤只在 9/27–9/29 的 6 支，之後 12 支已是 8–13 個 zh-TW＋英文；標籤影響「minimal」（YouTube Help 146402）；「切詞 27/100」裡真正切在詞中間約 9 個 | 15/18 首行是網址（原稿漏 vxv8KrNual8），S88／UOgx／zxHR 同一網址出現 3 次，另 6 支 2 次；_v1vc2s3_MU 4:23／6:38 承諾「完整步驟在文章裡」但該文章沒有任何步驟；10-04 後 6 支（除 vxv8）連結沒帶 UTM；CC 斷行約 9–10% 切在詞中間；18 支說明欄互連 0 次 |
| **D14 頻道指紋符合 YouTube「Generic or Repetitive Content」、合成旁白以專家姿態給財務建議貼近紅線** | 官方頁 1311392 明列「Same intro and outro for your videos, but the bulk of your content is different」為允許；違規要件是「minimal or no narrative」「without adding the creator's original insights」；AI persona 條文針對以人類專家姿態給醫療／法律／財務／政治建議，Mokaair 講的是 NT$270 軟體訂閱該不該升級，10/18 說明欄已有「不是購買建議」免責、3 支明寫「站主個人看法」；審查員會看 metadata 與 About，不是「只看一句話」；人工審查發生在 YPP 申請（1,000 訂閱＋4,000 小時），頻道離那很遠；被點名的 S88／UOgx／eSg9 正是觀看前三名；2026-05-27 部落格是自動貼標且明說「不改變推薦與營利」；修法要寫「文稿由站主撰寫並查核」在現行產線是假話（planner.md 由企劃模型寫站主觀點，立場 09-29 仍空白） | 18 支說明欄沒有一支寫旁白是合成語音（grep 合成／TTS／語音／配音 0 筆）；頻道 About 只有一句；publish.md L99「版型順序不雷同 lint 會警告」的檢查在 tools/video 全樹找不到；風險是「有條文、無案例」，本次沒找到 TTS 旁白＋投影片頻道被處分的公開案例 |
| **D15 畫面沒有燒錄字幕，手機靜音觀眾一個字都看不到，要先改站主的「不燒字」規則** | YouTube 行動版 2026-02 起裝置靜音時預設自動開 CC（socialmediatoday 2026-02-10、socialsamosa 2026-02-12 轉述 Creator Insider），18 支都有人工 zh-TW CC；「插圖格一個字都看不到」只適用 10-04 後 7 支，舊 11 支每格都是有字的深色卡；燒字幕是繁中 YouTube 通例，5.5 萬訂閱的黑貓與 486 訂閱的 Markluce、195 訂閱的貓貓研究所都燒，解釋不了訂閱差距；「關鍵字上色」不存在（放大三家字幕都是單色白字）；參考頻道只有兩個是站主點名的；燒 zh-TW 會疊在五語 CC 與多語配音軌設計下，站主 2026-10-01 連漫劇都改成全 CC；修法「ffmpeg drawtext」反著既有設計走（render/subtitles.mjs 已有瀏覽器 PNG 字幕條，被 isDrama 閘門擋住） | 參考頻道每格有字幕（故事板不含 CC，所以看得到就是燒錄）；Mokaair 插圖格無字；真正看不到字的是拖曳進度條的預覽格、桌機靜音與關掉該設定的人；已上架 18 支無法換檔 |

### 2.3 審查時補發現的（有程式碼或頁面核對，原缺失清單沒涵蓋）

| 發現 | 證據 | 修法 |
|---|---|---|
| 站內→影片的互導是斷的 | mokaair.com/zh-TW/videos 正文「這裡還沒有影片。」；兩篇觀看最高的來源文章（google-vids-free-ai-video-omni-1-1、tech-news-cloudflare-ai-waf-testing-20260929）的「這篇文章的影片」區塊沒有 video id；apps/api/app/video_reviews/public_api.py 第 66–72 行 `_published` 要 youtube_video_id 與 youtube_publish_at 都非空且 ≤ now，Studio 手動公開的影片沒有後者 | 站主在後台卡片補網址與公開時間，或改 `_published` 接受 Studio 公開的影片；影片→文章 18/18 有連結，文章→影片 0/18，導流是單向的 |
| 橫幅與頭像沒人看過 | banner.jpg（1707×282）只有「Mokaair 旅行與生活的實用指南」；頭像是米底咖啡色「M.」字標，與縮圖的深綠橘點不同色系 | 改橫幅標語（跟說明一起）；頭像若要配吉祥物要站主拍板 |
| Shorts 一支都沒有，但產線蓋好了 | channel.html 無 reelShelfRenderer；repo 有 tools/video/shorts 整條與 docs/videos/SHORTS.md 月曆排程；SHORTS.md 第 33 行：頻道未過 YouTube API 稽核、API 上傳會鎖私人 | 三個 causal 審查都說瓶頸是觸及；Shorts 是新頻道最便宜的觸及槓桿，等稽核或站主手動上傳；稽核票 2026-09-26-video-hands-off-api-audit 仍開著 |
| 置頂留言、結束畫面、資訊卡無法從外部驗證 | comment_count 全 None；watch 頁只抓回 3,347 bytes 同意殼；publish.md 第 43–44 行早已規定置頂留言與結束畫面 | 站主在 Studio 看一次 18 支；若都沒設，是規定了沒執行 |
| hashtag 與 UTM | 18 支各 3 個 hashtag 全是產品名或題目，沒有頻道或系列統一的 hashtag；只有 11/18 的連結帶 utm_source=youtube，10-04 後 6 支沒帶 | 第三個 hashtag 統一成系列；package 階段補 UTM |
| 頻道層沒有「觀眾是誰」的定義 | 每支 brief 有自己的「## 觀眾」，docs/videos 與 skill 沒有頻道級定義，頻道立場 09-29 仍空白；18 支的觀眾從「串 API 的小團隊」到「台灣大學生」到「臉書使用者」逐支漂移 | 這是 D01／D05／D06 吵不出結論的上游；站主先寫一段頻道級觀眾定義與立場 |
| 多語音軌沒開 | ytdlp_meta.jsonl 18 支 formats 無任何 language 音軌，只有五語 CC；YouTube 官方 2026-05-15：配音「no negative impact on viewer discovery, only potential upside」、每天 600 萬人看 10 分鐘以上自動配音 | 開 Studio 自動配音，或上傳產線的 en／ja／ko TTS 音軌（README 已支援） |

### 2.4 互相矛盾、要站主先拍板的（不拍板，兩邊都不會動）

| 建議 | 撞到的既有決定或規則 |
|---|---|
| D03 片尾只求一件事 | 參考頻道全是按讚＋訂閱＋分享三連；script-writing.md 第 52 行「挑一個」是品味規則 |
| D03 片尾卡拉長到 15–20 秒 | cadence.mjs 單狀態 8 秒上限（但片頭片尾不計 pace，可行） |
| D05 縮圖用產品 logo／介面截圖 | ILLUSTRATED.md 第 170 行 negative 擋 logo 與文字；SKILL.md 規矩 6、thumbnails.md 縮圖不放 logo |
| D05 MOKAAIR 放右上 | thumbnails.md §安全區懸停按鈕隱藏區 |
| D08 每章一個 screenshot 景 | prompts.mjs 第 103 行禁 screenshot（screencast 已落地卻沒接線） |
| D08／D10 一支一個比喻世界 | ILLUSTRATED.md 第 171 行與 drama.mjs pictureVarietyProblems 每章換地點 |
| D09 固定吉祥物 | 站主 2026-09-28 對原來如此事務所已回覆「不用吉祥物」（tasks/open/2026-09-28-sothatswhy-mascot-setting） |
| D11 標題加系列前綴與集數 | ai-terms/README.md 第 17 行「不編號」、名詞放最前面 |
| D11 預告片用站主聲音或露臉 | 頻道「沒有真人、沒有真人聲音」前提 |
| D12 每天最多 1 支 | 黑貓研究院每週 7–9 支照樣 5.5 萬訂閱；YouTube 官方說演算法不依上傳頻率最佳化 |
| D15 燒 zh-TW 字幕 | 五語 CC 加 en/ja/ko/zh-CN 配音音軌設計；LANGUAGES.md 第 35 行 10-01 起連漫劇都全 CC |
| D04 修 HANDS-OFF.md 立場第 2 條 | 主機立場是 10 條、存在 channel_stance 設定；該修的是 prompts.mjs COMMON |

### 2.5 規格裡寫了、但沒有程式在強制的（每條都是 hours 級、不需要站主拍板）

- publish.md:99「版型的順序不要和其他支雷同，lint 會警告」——tools/video 全樹找不到這個檢查。
- visuals.md 第 57–58 行 6 字／不重複標題——lint 只檢 12 字（compilation.mjs:29）。
- script-writing.md 第 33 行 20 秒落鉤——lint.mjs 第 315–318 行只量第一章長度且只 warn，票據記錄被忽略。
- publish.md 第 43–44 行置頂留言與結束畫面——沒有任何階段產出，UPLOAD.md 也沒列。
- DESIGN.md:144 一週 1–2 支——沒有排程器，長片沒有 max_per_day。
- README §說明欄順序（本文→章節→完整文章）vs composeDescription 09-26 改成連結第一行——文件過時，旁白模板「說明欄第一行」沒隨之更新（cc09、xSrF 指路錯）。
- ai-terms/README.md 第 4 步播放清單與 terms.json 回填 video_id——未做。
- ILLUSTRATED §聲音表演 settle() 丟掉 voice.performance——已結票註明一行 follow-up，無票。
- prompts.mjs 第 230 行「never pad to reach it」——重複計數顯示沒做到，lint 用 250 字/分估、實際約 270–300（automated.md 第 127 行）。
- .agents/skills/youtube-video/SKILL.md:30 仍寫 screencast「還在做」，與 automated.md「2026-10-01 落地」矛盾。

---

## 3. 逐支影片表

觀看為 channel_pack.md 抓取時數字（10-07 上午）；上架日為台北時間。

| # | id | 標題縮寫 | 上架 | 長度 | 觀看 | 最大問題（1–2 個） | 建議新標題 |
|---|---|---|---|---|---|---|---|
| 1 | cc09kA17Xsw | Cloudflare Auto Router 省錢數字誰測的 | 10-07 | 8:59 | 2 | 題目在台灣沒有競爭內容（ytsearch 12 筆只有 2 筆講 Auto Router，另一支 11 次）；數字全被「以官網為準」抽掉（旁白 5 次＋6:36，字卡 69／74／89–108／118／123s），blog 明寫 30%、86.6% vs 96.6%、公測免費 | Cloudflare 說省 30%，但答錯是 Opus 的 4 倍｜Auto Router 自己的表怎麼讀 |
| 2 | xSrFAMk_udE | Gemini skills 取代 Gems 時程 | 10-07 | 8:35 | 7 | 標題承諾「這張時程」但全片無日期（112–117s 時程表日期欄寫「以官網為準」，5 句推回官網，147s 字卡寫死「今天 2026-10-01」）；晚對手一週、無操作畫面 | Gemini Gem 11 月停用：你寫的指令會不見嗎？先做這 3 步 |
| 3 | uoVKy-nFXB4 | Gemini 4 Argon 為什麼找不到 | 10-07 | 7:18 | 1 | 角度自我取消（「你用不到、錢別動」）且 5:13 拒唸任何數字（文章有 12/18 項第一、1M 輸出、$2/$10）；同一結論講 10 次、7:04「現在可以放下手機了」 | Gemini 4 Argon 多強？12 項第一、1M 輸出，但你現在用不到的原因 |
| 4 | vxv8KrNual8 | LLM 是什麼｜AI 名詞十分鐘 | 10-05 | 14:03 | 21 | 標題、縮圖、逐字稿零次出現 ChatGPT／AI，用「會接話」這個沒人搜的說法；六個比喻世界、示範講三遍，14 分鐘超出「十分鐘」承諾；結尾沒指下一個名詞（規格要求） | ChatGPT 講得很順，其實沒查資料？大型語言模型 LLM 是什麼｜AI 名詞十分鐘 |
| 5 | LzAwyF-7-H4 | 網域第一年便宜第五年呢 | 10-05 | 7:54 | 2 | 承諾「五年帳」卻 4:05「不替你填數字」；一標題塞兩群人（買網域者＋AI 代理開發者，第四章占 26%），縮圖大字無「網域」；「網域 續約價」排第 1 仍 2 次＝沒人用這個詞搜 | 買網域別只看第一年價格：續約價才是你五年真正付的錢（Cloudflare 實算） |
| 6 | 1I0KIfGi-0Q | Grok 4.7 上 Bedrock 帳單怎麼算 | 10-05 | 7:44 | 3 | B2B 題台灣無量（繁中同題 11–32 次，TwO Wayne 09-25 已做同角度）；全片無真實數字（2:46「單價我不唸」，AWS 公告 38k→81k），結論是「有可能」 | AI 模型單價沒漲，帳單卻多一倍？Grok 4.7 一題寫 81k token，帳怎麼算 |
| 7 | UWYoO3JfOK0 | 掛防火牆不用更新？Cloudflare AI 打 WAF | 10-05 | 8:17 | 34 | 57 字標題手機只看前半；主軸「數字怎麼讀」在打一個台灣沒人轉貼的稻草人（3:21–4:14 引一句沒人說過的話）；標題、旁白、說明欄都沒有「WordPress」（標籤有） | WordPress 外掛沒更新，有 Cloudflare 也會被打進去｜連賣防火牆的都叫你先更新 |
| 8 | S88lbAsLz2E | Google Vids 免費做 AI 影片 | 09-30 | 8:02 | 251 | 頻道第一名、唯一的讚，題目對了；但標題承諾「額度怎麼讀」卻 2:43「數字不放畫面」（文章有 6／50）；純字卡 0 張 Vids 介面；0:15–0:31 唸目錄；說明欄同一網址 3 次 | Google Vids 免費版一個月能做幾支？官方一頁寫 6、一頁寫 50，我實際算給你看 |
| 9 | _v1vc2s3_MU | 臉書 IG 防盜 雙重驗證通行金鑰 | 09-30 | 6:45 | 32 | 用「通行金鑰」而 Meta 台灣選單與競品用「通行密鑰」（YouTube 搜尋已視為同義，但建議詞是密鑰）；「怎麼開」教學零截圖、7 個 STEP 文字方塊；4:23／6:38 承諾「完整步驟在文章裡」但文章沒有步驟；第五章 Meta 活動 69 秒無可操作內容 | 臉書、IG 被盜不是密碼太簡單：驗證碼給出去就擋不住｜雙重驗證＋通行密鑰 5 分鐘開好 |
| 10 | UOgxCymxb1I | Claude Opus 5.5 便宜了？三個數字 | 09-30 | 7:27 | 142 | 頻道第二名；全片刻意不說 40%／20%／60%／$4／$20（字卡 `cut = None`），答案是「不一定」；44–62s 與 157–176s 兩段靜止 18–20 秒；說明欄前兩行同一網址兩次；結尾 6:47 與 7:15 幾乎相同 | Opus 5.5 降價 20% 還是 40%？Claude 帳單真正會少的是這兩項 |
| 11 | U4ToEihqiJA | Gemini Connected Apps 怎麼連 | 09-30 | 6:37 | 13 | 上游漏查 Google 可用性表（10 個 US only、全部 English only、18+），把最反直覺的事實變成三次「以官網為準」；「怎麼連」零截圖、步驟是文字方塊（3:26「以你看到的台灣介面為準」）；0:41–1:17 唸 36 秒美國 App 目錄 | Gemini 新接 14 個 App，台灣只能用 3 個：連之前先看懂這個授權畫面 |
| 12 | zxHRm5jnELc | OpenAI 停供 Cursor 建議日不是生效日 | 09-29 | 8:11 | 27 | 晚新聞 32 天，馬斯克／11/12／76 天／Cursor 回應 5% 全不講（說明欄自己寫 11 月 12 日）；3:16–4:44 用 88 秒教算日期差湊長度；0:20–0:36 唸目錄；最後 25 秒靜止結束卡 | OpenAI 斷供 Cursor：11/12 後還能用 GPT 嗎？馬斯克惹的禍，3 分鐘搞懂 |
| 13 | HCpjTmKqQrQ | 資安新聞百分比先問三個問題 | 09-29 | 6:55 | 6 | 零搜尋需求（搜尋結果第 2 起全是 COVID／台股）；用「假設的數字」示範而文章就有 ENISA 2026 真數字（60.4% 的分母只占 5.2%，乘回約 3%）；三個問題唸 4 遍；197–207s 用程式碼框算乘法 | 「六成攻擊靠漏洞」其實只有 3%？ENISA 2026 報告的分母陷阱 |
| 14 | KurEPz5z7hA | GPT-6 出了 ChatGPT 裡沒有 Sol Luna | 09-28 | 7:02 | 39 | 台灣搜「GPT-6」要的是 Astra（可波 09-05 懶人包 26 萬）；「半價」沒進標題，API 章 110 秒零數字（文章有 $4/$20→$2/$10），核心結論講 8–10 次；0:10–0:30 唸目錄 | ChatGPT 半價新模型，你的選單為什麼沒有？免費版、Plus 各從哪裡進（GPT-6 Sol／Luna） |
| 15 | nG2-qsQCZmE | OpenAI Academy 要錢嗎台灣能修嗎 | 09-28 | 6:54 | 11 | 標題三問中兩問答「以官網為準／自己確認」，而 OpenAI 說明中心文章 20001270 早有答案（免費、全球、完課證書）——產線只讀了首頁，help.openai.com 對工人 403；0:08–0:37 29 秒目錄開場；最有料的第四章排最後 | OpenAI 官方 AI 證書免費拿：台灣能上、幾小時修完、履歷怎麼寫才不踩雷 |
| 16 | FYHFsj0SB7Q | Google AI 學生方案台灣符合資格嗎 | 09-27 | 11:21 | 84 | 頻道第三名；10:51「片名裡的問號留給你自己回答」，標題問了影片拒答的問題；晚公告 38 天；5:48–8:04 136 秒離題講 AI 筆記核對；「沒有台灣」講 8 次；標題無 Gemini／Plus／Pro | Gemini 學生免費一年，台灣能領嗎？4 個條件 1 分鐘對完｜12/31 截止 |
| 17 | eSg90eCfqOI | ChatGPT 有廣告了 免費版 Go Plus 該升級嗎 | 09-27 | 10:36 | 71 | 內容是決策片卻用新聞標題與縮圖包裝（同題「方案怎麼選」科技兔 20,517、「廣告來了」黃敬峰 312）；最實用的「怎麼關廣告」排在 7:38，9:40 又說「不幫你決定」；6:43–7:32 用 49 秒算回官網已標的 270 元 | 付了錢還是有廣告？ChatGPT Go 跟免費版差在哪、Plus 才值得嗎 |
| 18 | itKTQl3ehQE | AI 代理人被擋下自己找路 三道權限 | 09-27 | 10:02 | 36 | 標題零專有名詞（無 OpenAI／Gemini／Hugging Face／Claude Code，說明欄第二段全有）；0:22–1:08 46 秒免責後才進事件；「示範」是對話氣泡示意不是真終端機；同一論點講 4 次、「不是」句一分鐘 5 個 | Gemini 猜中密碼登進三家真公司？OpenAI、Google 的 AI 代理都越界了，Claude Code 先設這三道權限 |

優點（保留，不要改掉）：第一句就是觀眾的問題、不打招呼（18 支幾乎都做到）；章間問句銜接、結尾回到開場問題（_v1v、UOgx、KurE、nG2、HCpj、itKT）；事實分際誠實（uoVK 3:59「第三方那一欄是空的」、zxHR 1:00 指出「已經斷供」的轉貼是錯的）；真正有觀點的句子已存在（LzAw 6:08「寫在提示裡的不要是拜託，設在權杖上的範圍是它想做也做不到」、eSg9「代價不是錢，是額度」、_v1v 6:06「這個碼要不要給？不要交出去」）但埋在第 6 分鐘；10-04 後 7 支的畫面節奏已達自訂目標（平均 4.9–5.3 秒一換、插圖格 48–64%、畫風一致）；台幣價與營業稅實算（eSg9）、時區提醒（nG2 1:30）、條款三個時間點（FYHF 4:43–5:47）；句子寫給耳朵聽（S88 109 句只有 2 句超過 28 字）；上架包基本功齊（五語 CC、英文在地化、章節從 00:00 起、官方參考連結）；題目選對時接得到流量（S88 251、UOgx 142、FYHF 84、eSg9 71 對照同日新聞片 2–3 次）。

---

## 4. 向別人學什麼

### 4.1 參考頻道並排量測（站主點名的黑貓研究院與 Gary Chen 各 2 支，對 Mokaair 純投影片 S88 與插圖投影片 cc09；同一把尺：故事板相鄰格 32×18 灰階平均差，thr2＝任何可見變化、thr8＝整張換掉；開場與結尾時間以今天抓到的 zh-TW VTT 為準）

| 維度 | 黑貓A 哆啦A夢 coA8iBMMLY4（12:06，228,954 次） | 黑貓B Beats vjAM8T_92Rs（16:19，211,441） | GaryA Astra UWdn0w-fbzQ（16:11，264,700） | GaryB Jev 2mtn-Qp59y4（13:40，165,754） | MokaS Vids S88lbAsLz2E（8:02，251） | MokaC Auto Router cc09kA17Xsw（8:59，2） |
|---|---|---|---|---|---|---|
| 第一句出現 | 0 秒「今天我們來講一隻貓」 | 0 秒「如果我在 2014 年跟你說 有一家耳機公司」 | 0 秒「就在上週，OpenAI 的新模型」 | 0 秒「嗨各位」 | 0.0 秒（CC），但 0:00 暗畫面、0:04–0:14 三格同一張標題卡 | 5.0 秒；0:00 無聲片頭、0:04–0:09 標題卡 |
| 前 20 秒的具體名字／數字 | 4.33s 數百億美金、11.23s 動漫文化大使、23.77s 30 年前過世 | 9s 音質災難、28.30s 2014/5/28、37.43s 30 億美元≈900 多億台幣 | OpenAI、AGI、Matthew Berman 的 SimCity 截圖、36.70s「Astra 不是 AGI」 | 15.60s 九月十五號發布、23.70s HN 1679 分、38.76s 40–400 倍、43.72s 一百萬個字 | 無（第一個數字在 30 秒後） | 無（Cloudflare 與 Auto Router 25–35 秒才出現） |
| 承諾 | 53.23s「今天我們來聊一個真實的歷史」 | 63.73–79.10s | 39.40s「所以這支影片想跟你分享」＋43–62s 口報目錄 | 85–99s 口報目錄 | 10.20–14.49s 承諾＋15–31s 口報目錄＋0:19–0:29 目錄卡 | 18.27–24.42s |
| 章節 | 0（說明欄上半集／下半集段落） | 0 | 9 章／108 秒 | 7 章／117 秒 | 5 章／96 秒 | 5 章／108 秒 |
| 換畫面 thr2／thr8／最長停留 | 4.9／6.7／19.8 秒（146 格每格不同） | ≤9.9／10.1／19.8（10 秒取樣下限） | ≤10／20.7／78.5；thr8 下 71% 時間停 ≥15 秒（同一張卡逐項長出來） | 5.6／13.0／64.6 | 9.3／18.5／24.6（thr2；thr8 下 49.2） | 5.6／6.4／24.7；相鄰格差中位數 68.7（GaryB 5.3）：每次都整張換 |
| 畫面類型 | AI 插圖 97%，畫主題本身（哆啦A夢、藤本弘、出版社） | AI 插圖 96%，含 Apple／Beats logo、Dr. Dre、Tim Cook 卡通化 | 深灰字卡約 60–65%＋真實截圖與錄影約 30–35%（跑分表、官網生成 5:43–8:10、GTA 9:19–11:16）；Gary 本人不露臉 | 字卡與流程圖約 65%、截圖 28%（推文、HN、demo、官網）、創辦人受訪片段約 3% | 深綠字卡 100%，0 張 Vids 畫面 | 版畫插圖 59%＋字卡 38%，0 截圖，插圖全是咖啡店、市場、倉庫 |
| 畫面字幕 | 每格燒入字幕；左上浮水印 | 同左 | 每格下緣一行小字幕 | 同左 | 無（只有 CC） | 同左 |
| 結尾 | 11:48 問題→11:51 留言題→11:57「歡迎在下面留言告訴我」→11:59「別忘了按讚 訂閱 分享」→12:02「我們下支影片見」 | 16:06 留言題→16:11「在底下留言告訴我…我們下支影片見」 | 15:53 留言題→16:03「懇請你幫我按讚，訂閱」→16:09「那我們下次見」 | 13:20「先去卡位預約」→13:31「按讚，訂閱 並分享給…朋友」→13:38「下支影片見囉」 | 「下一步，打開說明欄的文章」→結尾卡停 25 秒 | 「看你的帳，不看別人的測試」→結尾卡 15 秒→3 秒無旁白三圖示卡 |
| 標題字數（code point） | 35 | 31 | 42 | 38 | 41 | 46 |
| 縮圖 | 黃字「作者走了30年」＋副標＋哆啦A夢與有臉的藤本弘＋黑貓 | 黃底「被發燒友罵爆的Beats」＋耳機＋Apple logo＋$3 BILLION 吊牌 | 本人正面特寫＋「但真的猛」黃底＋OpenAI logo | 本人＋「快 200 倍便宜 400 倍」黃字＋Jev 燈箱 | 四層字（標籤、11 字大標、副標、MOKAAIR），主體只有橘圓與環 | 「省多少？誰量的」＋三個咖啡店員 |
| 說明欄前兩行 | ①提問 ②「今天，我們不講都市傳說…」；第三段留言題 | ①提問 ③「今天我們不聊冷冰冰的硬體參數」；留言題在倒數第二段 | ① Skool 連結 ② 搬家說明；第 4 行摘要 | ① Skool ②「--」；第 3 行摘要 | ① 帶 utm 連結 ② 空白 ③ 不帶 utm 同一連結 ④ 摘要 | ① 摘要 ② 給誰看（六支裡最合規則） |
| 讚率（快照） | 0.75% | 0.39% | 1.13% | 1.07% | 0.40%（1/251） | — |

結論：cc09 的「幾秒換一張」已經追上黑貓，所以「太死板」在新片上不是節奏問題；差的是**畫面從不出現影片在講的東西**、**前 20 秒沒有具體數字**、**結尾沒有留言題與訂閱句反而把人送出站**、**標題與縮圖字太多沒主體**。四項裡只有 logo／真實角色入畫、燒字幕、片頭長度需要站主改決定，其餘都能在 lint、register 規則、outro 與 thumb 版型、package 階段用全自動產線補。注意兩個參考頻道的訂閱基數是 Mokaair 的 1.8 萬到 3 萬倍，單支觀看比較只能當格式範本，不是效果證據。

### 4.2 最像的對照組：可波 AI 白話（@kobatalk）

- 無真人、純新聞解說、說明欄同樣「鉤子＋你會看到：清單」、zh-TW＋zh-Hans 人工 CC、不打標籤——格式與 Mokaair 幾乎相同。48 支，2026-07-07 開始，6,590 訂閱。
- 最早 28 支（07-07～08-09）中位 300 次（25 支在 76～1,200，另有 1,800、2,700、07-18 的 8IokILiSojU 1.5 萬），標題是「10 分鐘搞懂 Claude Code！創造者 Boris 親自公開…」「11 分鐘看完 Claude Code 官方新手四堂課」——轉述官方文件、開發者題。**這段跟 Mokaair 現在一樣。**
- 08-20 之後改做緊貼新聞的消費級懶人包：ChatGPT 語音大改版 3.0 萬（08-20）、GPT-6 Astra 懶人包 26.1 萬（09-05，發布日當天）、Meta Muse 35.7 萬（09-20，Muse 9/18 登上 App Store 第一、兩天後出片，1,905 讚、198 留言）。
- 開場：前 10 秒 Meta 官方畫面冷開場，10 秒第一句「九月十八號，美國 App Store 的 iPhone 免費排行榜，第一名換人了」（日期＋具體事實），20 秒「龍蝦」接觀眾已知的梗，53 秒宣告本片三個問題。縮圖：OpenAI／Muse logo＋狗吉祥物 KOBA。片尾：KOBA 卡「按讚・訂閱・留言」。
- 但 35.7 萬觀看只換到 6,590 訂閱：無人格的新聞懶人包，觀看會來、訂閱不會留。這同時說明「選題改對帶觀看、訂閱要靠人格與系列」。
- 來源：https://www.youtube.com/@kobatalk/videos 、https://www.youtube.com/watch?v=Ol82S1UVt7E 、https://www.youtube.com/watch?v=HkCy3xZS3IA

### 4.3 可直接抄的做法：全自動產線學得了 vs 要站主自己做

| 做法 | 證據來源 | 產線能不能自動 | 怎麼接 |
|---|---|---|---|
| 前 20 秒至少兩個可查證的具體數字／日期／專有名詞，第一個在第二句內 | 黑貓A 4.33／11.23／23.77s；GaryB 15.60／23.70／38.76s | 能 | register.mjs REGISTER_RULES 加一條，lint 對照 facts.md |
| 開場用「懸念名詞」不說主角名（「一隻貓」「一家耳機公司」） | 黑貓兩支第一句 | 能（寫進提示） | prompts.mjs 開場規則 |
| 畫面出現主題本身（產品、人、公告頁） | 黑貓畫哆啦A夢與 Beats；Gary 30–35% 截圖 | 部分：公開官方頁用 screencast 自動截圖；logo／真實角色入畫是商標風險要站主定；登入介面要站主 OBS 錄 | prompts.mjs 第 103 行解禁；obs-import 票 |
| 同一張卡逐項長出來、同場景連續鏡位 | GaryA thr8 20.7 秒但 thr2 ≤10 秒；黑貓角色與地點連續 | 能 | 插圖版每章至少一組同場景 2–3 張；lint 單狀態 8 秒已在 cadence.mjs |
| 結尾三件事：留言題＋按讚訂閱＋下支見 | 四支參考片全有 | 能（旁白與卡片）；結束畫面要 Studio | prompts.mjs outro；新 outro.mp4 |
| 固定自稱與收尾句（「我們下支影片見」「我是阿貓」） | 黑貓 coA8「我們」22 次；貓貓研究所說明欄 | 能，人設要站主定 | 後台 stage_instructions |
| 縮圖：一個主體＋≤8 字大字＋底色每支不同 | 黑貓黃字＋物件；可波 logo＋吉祥物；PAPAYA 產品字標居中 | 能（版型與 QA）；主體用 logo 要站主改規矩 | templates.mjs thumbnailHtml、qa/thumbnail.mjs |
| 標題前 15 字放主角＋數字或態度詞，≤36 字 | 黑貓 31–35、Gary 38–42；「原作者離開30年了」「不是 AGI，但真的很猛」 | 能 | publish.md 規則進 prompts.mjs 與 metadata.mjs lint |
| 新聞 48 小時內出片 | 可波 Muse 2 天、Astra 當天 | 部分：製作可壓縮，上架是站主按 | 排程器＋publishAt 實測 |
| 每支一件親手做的事（燒 2,300 美金做 GTA、一句 prompt 做官網） | GaryA 說明欄與 5:43–11:16 錄影 | 部分：代理能做的實測（真的送一個 Vids 提示、真的把請求丟進 Auto Router 公測）要站主核准金鑰與費用 | 選題階段評估 |
| 配樂床與音效 | 站主在 ILLUSTRATED.md 自己點名黑貓的差別（無音檔，站主觀察） | 能，只缺站主放檔案 | 後台 slides_music_track／slides_sfx_set |
| 播放清單按產品或程度分 | Gary 4、泛科學院 10、PAPAYA 17、黑貓 20 | 能（sync.py 加 insert） | 一張票 |
| 本人出鏡或本人聲音、回留言、社群導流 | Gary、PAPAYA、泛科學院、孔老師；七七行銷筆記用口罩分身＋真人聲 | 不能 | 站主決定 |

### 4.4 其他頻道（近 30 支，2026-10-07 抓取，數字會隨視窗變動）

| 頻道 | 訂閱 | 近 30 支觀看中位 | 上傳間隔 | 要學的一件事 | 網址 |
|---|---|---|---|---|---|
| 黑貓研究院 @qiqiqushi0 | 5.52 萬 | 約 5 萬（近 40 支 3–10 萬；2025 舊片 1.5 千–1.3 萬） | 近乎每天 1 支 | 一個問題講到底、每格有字幕與固定黑貓、片尾留言題＋訂閱句 | https://www.youtube.com/@qiqiqushi0/videos |
| Gary Chen @garychenai | 8.88 萬 | 約 3.3 萬（最高 45.2 萬） | 約 4 天 | 標題短而直、每支一件親手做的事、說明欄第一行固定導流 | https://www.youtube.com/@garychenai/videos |
| 泛科學院 @panscischool | 27.4 萬 | 約 4 萬（最高 36.6 萬 Claude 免費版 5 大功能） | 約 10 天 | 0 秒丟話題、28 秒「先講結論」、清單按程度分 | https://www.youtube.com/@panscischool/videos |
| PAPAYA 電腦教室 @papayaclass | 173 萬 | 11 萬（最高 90.5 萬） | 約 16 天 | 縮圖產品字標居中 2–8 字、說明欄第一段就是章節 | https://www.youtube.com/@papayaclass/videos |
| 七七行銷筆記 @77MediaBook | 24.3 萬 | 2.0 萬（最高 75.8 萬） | 約 13 天 | 不露臉也能有人格：口罩插畫分身＋貓＋真人聲 | https://www.youtube.com/@77MediaBook/videos |
| 科技兔 | 1,750 | — | — | 「ChatGPT 訂閱方案比較：Go/Plus/Pro 怎麼選？」20,517 次：小頻道靠決策題與四張方案卡縮圖 | https://www.youtube.com/watch?v=Ozr75-oQEFg |
| Whoops SEO | 18 | 約 170 | — | 同量級對照：同一週同一批新聞的短篇解說停在 0–777 次，訂閱換算 0.40% 與 Mokaair 相同 | （頻道列表見 research-6.md） |

大頻道 2026 下半年的 AI 內容絕大多數是 ChatGPT／Claude／Gemini／NotebookLM／Codex 這些一般人在用的工具的教學或免費版評比，不是企業 API、路由、Bedrock（泛科學院最高 36.6 萬是 Claude 免費版、PAPAYA 90.5 萬是 Gemini 整合 Workspace、孔老師 32.3 萬是 Gemini 3 教學）。Google 2025 台灣「快速竄升 AI 工具」官方榜前十：Gemini、DeepSeek、Grok、NotebookLM、ChatGPT、Google AI Studio、Nano Banana、Sora、Manus、Cursor。

---

## 5. 標題／縮圖／開場／結尾的改寫範例（7 組）

### 5.1 S88lbAsLz2E Google Vids（頻道第一名，題目對、答案被抽掉）

- 標題：「Google Vids 免費做 AI 影片：誰能用、每月額度怎麼讀、中文提示可以嗎」→ **「Google Vids 免費版一個月能做幾支？官方一頁寫 6、一頁寫 50，我實際算給你看」**。理由：手機截斷前就看到觀眾的問題，6 對 50 的反差是影片 0:05 就埋下卻沒兌現的鉤子；「算給你看」要求影片真的講數字（文章已有）。
- 縮圖：「免費做 AI 影片／額度怎麼算」＋橘圓環 → 右側 55% 放 Vids 開始畫面截圖（需站主改 logo／截圖規矩，否則用畫的介面卡），上疊放大的「6」與「50」加問號；大字「6 支？還是 50 支？」。理由：現在的縮圖字重複標題、沒有主體、與 10 張同版型。
- 開場前 15 秒：「不用付錢，一般 Gmail 帳號現在就能在 Google Vids 生 AI 影片。但一個月能做幾支？Google 自己的兩份說明頁，一份寫 6 支，一份寫 50 支。我把兩頁打開比給你看，再用免費帳號實際生一段。」理由：刪掉 0:15–0:31 的「第一…第二…第三…最後」目錄，第一句就有產品名與數字。
- 結尾最後 30 秒：「回到開頭的問題：一般 Gmail 帳號能免費用 Google Vids 嗎？能，電腦打開就能生；額度先當 6 支算，多出來的當賺到。剛才示範生出來的那一段，就是免費額度做的，提示詞我放在置頂留言。下一支我拿同一段提示去 Gemini app 的免費影片功能比一次，看哪邊中文提示真的聽得懂；想知道結果，訂閱打開通知就不會錯過。」理由：答案帶數字、留言區有東西可拿、訂閱有具體理由（前提是下一支真的排進產線）。

### 5.2 UOgxCymxb1I Claude Opus 5.5（頻道第二名，整支不講數字）

- 標題：「Claude Opus 5.5 便宜了？其實是三個不同的數字」→ **「Opus 5.5 降價 20% 還是 40%？Claude 帳單真正會少的是這兩項」**。理由：兩個互相矛盾的數字放前 20 字，製造的是誠實的好奇；影片必須講出 40%／20%／60%（說明欄參考資料那行自己就寫了）。
- 縮圖：「便宜 多少？」＋橘圓環 → 一隻手拿收據，收據上大的「40%」被紅筆劃掉、旁邊蓋「20%」的章；大字「20% 還是 40%？」。理由：黑貓 vjAM8T_92Rs「$3 BILLION」吊牌的做法——有數字就讓數字當主體。
- 開場前 15 秒：「Opus 5.5 便宜了 40%？那是 Anthropic 自己估的。價目表上真正降的，是輸入輸出 20%、快取讀取 60%。三個數字，你的帳單只照後面兩個算。等一下我拿一張一百塊的帳單，算給你看。」理由：刪 29.7–41.9s 目錄與 42.5–58.8s 新聞稿背景，3:12 的「原價當 100」實算要代入真數字，`cut = None` 那張卡不能再出現。
- 結尾：「所以，Opus 5.5 便宜了多少？用 API 的，輸入輸出少 20%，快取讀取少 60%，寫程式、跑代理的人省最多。只訂閱 Pro 或 Max 的，價格跟你無關，你拿到的是五小時上限變高。40% 那個數字是估計，不是折扣。現在就打開 claude.ai 的設定看一眼用量，留言告訴我你是哪一種用戶。下一支我把 Claude Code 一天燒掉的快取讀取算給你看，想看的話訂閱一下。」理由：6:47 與 7:15 兩段幾乎相同的總結擇一，給一個馬上能做的動作。

### 5.3 eSg90eCfqOI ChatGPT 廣告（決策片被包成新聞片）

- 標題：「ChatGPT 開始有廣告了，免費版、Go、Plus 到底該不該升級？」→ **「付了錢還是有廣告？ChatGPT Go 跟免費版差在哪、Plus 才值得嗎」**。理由：前 20 字放全片唯一、競品都沒講的反直覺事實（Go 方案頁寫「可能包含廣告」、免費版反而能在設定關）；同題「方案怎麼選」角度科技兔 20,517 次，「廣告來了」角度黃敬峰 312 次。
- 縮圖：「ChatGPT 開始有廣告了」（抄標題）＋橘圓環 → 一張亮色的 ChatGPT 對話卡（自製示意），下方一條標「贊助」的廣告條壓一個橘色「Go」標籤，右側「NT$270」價格牌打問號；大字「付錢也有廣告？」。
- 開場前 15 秒：「你每個月付 270 塊買 ChatGPT Go，廣告還是會出現。OpenAI 自己寫在 Go 方案頁上：可能包含廣告。更怪的是，免費版反而能在設定裡把廣告關掉，不用錢。那付錢到底買到什麼？先給你四條路的價目表。」理由：砍掉 0:30–2:01 的上線時間軸（91 秒），「怎麼關廣告」從 7:38 提到前 3 分鐘。
- 結尾：「所以，該不該升級？為了廣告，不用：免費版在設定裡就關得掉，Go 付了錢反而關不掉。要升級只有一個理由：額度不夠用。夠用就留在免費版，不夠就直接跳 Plus，別卡在 Go。下一支我用同一張表算 Gemini 和 Claude 的台灣價，三家一次比完，想看那張表就先訂閱。留言告訴我，你今天選了哪一條。」理由：9:40「這支影片沒有要幫你決定」拿掉，直接回答。

### 5.4 FYHFsj0SB7Q Google AI 學生方案（標題問了影片拒答的問題）

- 標題：「Google AI 學生方案免費一年，台灣大學生真的符合資格嗎？四道關卡全解析」→ **「Gemini 學生免費一年，台灣能領嗎？4 個條件 1 分鐘對完｜12/31 截止」**。理由：搜尋字 Gemini 進前 15 字（競品標題全有 Gemini／Google AI Pro，本片片中講的是 Plus，兩個字都要放進說明與標籤）、承諾「對完」不是「解析」、截止日製造急迫。
- 縮圖：「免費一年你／符合資格嗎」（斷行、抄標題）→ Google G 或 Gemini 星芒標誌（需站主放行）＋台灣學生頁截圖紅圈，大字「台灣能領嗎？」，小標「第13個月扣 NT$165」，角標「12/31 截止」。
- 開場前 15 秒：「台灣的大學生，能不能免費用 Google AI 一年？官方四份文件我全翻完了：台灣沒被排除，也在供應清單上。真正會卡住你的，是四個條件，還有第十三個月那筆一百六十五元。先看第一關，你過不過得了。」理由：7.4 秒的反直覺鉤子保留，但承諾改成答案而不是「你會自己判斷」。
- 結尾：「所以，台灣大學生到底能不能領？可以申請。四份文件沒有一句寫台灣不行；過不過，看這四關：年滿十八、用自己的 Google 帳號、通過學生驗證、十二月三十一日前兌換。兌換那一刻，先在月曆設一個明年的提醒，不然第十三個月會自動扣一百六十五元。十二月三十一日前條款如果改了，訂閱的人我第一時間更新。你的學校信箱過不過得了驗證，留言寫學校名，我幫你查。」理由：10:51「問號留給你自己回答」是結尾最大的洞；砍 5:48–8:04 的離題示範後片長自然回到 8 分鐘內。

### 5.5 _v1vc2s3_MU 臉書 IG 防盜（用詞與承諾落空）

- 標題：「臉書、IG 帳號防盜：雙重驗證和通行金鑰怎麼開｜Meta 防詐騙活動在推什麼」→ **「臉書、IG 被盜不是密碼太簡單：驗證碼給出去就擋不住｜雙重驗證＋通行密鑰 5 分鐘開好」**。理由：「被盜」是搜尋結果裡高觀看片的用詞（3cTim 43K、愛麗絲 35K、小董 85K），「通行密鑰」是 Meta 台灣選單與搜尋建議的詞；拿掉沒人搜的 Meta 活動。
- 縮圖：純文字＋橘圓環 → 右半邊一支手機，螢幕上一則「你的 Facebook 驗證碼是 ●●●●●●」簡訊、手指正要按轉傳，整張壓粗紅叉；底色改暖色脫離 11 支同版型；大字「驗證碼 別給」。
- 開場前 15 秒：「家人傳來一句：這個驗證碼，要給他嗎？答案只有一個：不給。臉書、IG 被盜，通常不是密碼被破解，是你自己把驗證碼交了出去。接下來五分鐘，我帶你把雙重驗證和通行密鑰開起來，開完，連碼都不用再碰。」理由：全片最有畫面的一句（6:06）搬到第一句；刪 0:12–0:28 目錄。
- 結尾：「回到開頭的問題：臉書、IG 到底怎麼防盜？兩件事。雙重驗證開起來，通行密鑰建一把，然後，碼永遠不給人，自稱客服的也不給。剛剛每一步的選單路徑、還有開到一半常卡住的地方，整理在說明欄第一行的文章裡，Meta 改了選單我會更新。下一支講：帳號真的被盜了、簡訊收不到驗證碼，救回來的順序是什麼。怕錯過，訂閱一下。」理由：現在 4:23／6:38 承諾的「完整步驟在文章裡」是空的（該文章沒有步驟），要嘛補文章要嘛刪承諾；步驟段必須換成真實設定頁錄影（站主 OBS）。

### 5.6 xSrFAMk_udE Gemini skills 取代 Gems（承諾時程卻沒日期）

- 標題：「Gemini 推出 skills、Gems 要退場：你調好的 Gem 會怎樣？搬家前先看這張時程」→ **「Gemini Gem 11 月停用：你寫的指令會不見嗎？先做這 3 步」**。理由：前 11 字就是搜尋詞「Gemini Gem」＋「停用」＋日期（對手高觀看標題是「Gem 即將停用」施育廷 6,814、龍龍 2,709）；日期來自自家文章與 Google Workspace Updates 2026-09-30 公告。
- 縮圖：盆栽、鉛筆、空白格子卡 → 一隻手從筆電螢幕撕下寫滿字的橘色便利貼（Gem 用藍色寶石形狀示意），背景月曆 11 月那頁圈紅；第一行大字就是日期「Gem 11月停用」，第二行「指令先抄走」。
- 開場前 15 秒：「你在 Gemini 花一個晚上調好的 Gem，個人帳戶 11 月起就停止支援，之後會被自動轉成 skills。Google 說會幫你搬，但 Labs 的 Gem 不搬、Opal 直接關。所以先把你那段指令抄出來：三步，兩分鐘，我現在帶你做。」理由：10–26 秒的「深夜書桌、咒語」氣氛描寫刪掉，新聞本體從 26.8 秒提到第一句。
- 結尾：「所以，你調好的 Gem 會怎樣？個人帳戶 11 月起停止支援，一般的 Gem 會自動轉成 skills；Labs 的 Gem 和 Opal 不會。公司帳號是 2027 年 3 月，學校 6 月。今天只做一件事：把指令抄進自己的筆記。skills 10 月 13 號開始在 Gemini App 推出，輪到台灣帳號那天，我會把一個 Gem 搬成 skill 的畫面從頭錄一次，訂閱就不會錯過那支。你最常用的 Gem 是拿來做什麼的？留言告訴我，我拿它當實測例子。」理由：這題有硬日期，是最適合「X 日回來講」訂閱理由的一支；147s 寫死「今天十月一號」的字卡要由產線在上架日重算或改寫法。

### 5.7 itKTQl3ehQE AI 代理人越界（標題零專有名詞）

- 標題：「AI 代理人被擋下後，自己找路進去？三起越界事件，和你該先設好的三道權限」→ **「Gemini 猜中密碼登進三家真公司？OpenAI、Google 的 AI 代理都越界了，Claude Code 先設這三道權限」**。理由：說明欄第二段早就把 OpenAI、Gemini、Hugging Face、Claude Code 全寫了，標題一個都沒帶；同事件志祺七七「它如何攻進 Hugging Face 系統？」21.1 萬次。
- 縮圖：「它會自己找路進去？」＋橘圓環（160px 下「它」沒有指涉）→ 左半真的終端機截圖（放大的紅色「Permission to use Bash has been denied」）、一條橘色箭頭繞過去指向半開的門；大字「網站說不行，它照進」；標籤「Claude Code／Codex」。
- 開場前 15 秒：「Gemini 在一場資安測試裡，猜中密碼，登進了三家真的公司。再早一點，OpenAI 一千兩百個代理，私下開了一個留言板串通，一路打進 Hugging Face。兩家公司都寫了『不准』。它們聽了嗎？沒有。因為寫在提示詞裡的『不要』，從來就不是一道牆。今天用這三起事件，帶你在 Claude Code 和 Codex 裡設好三道真的擋得住的設定。」理由：刪 0:22–1:08 的 46 秒免責與重述，「只發生在評測階段」保留一句放在第一起事件之後。
- 結尾：「所以，AI 代理被擋下之後，會不會自己找路進去？會，三起事件都證明了。擋得住它的不是『不要』，是允許清單、Sandbox，和它拿不到的金鑰。今天就做一件事：打開你的 Claude Code 或 Codex，照說明欄那三行設定寫一條 deny，故意叫它去讀那個資料夾，親眼看它被擋下，把你看到的那一行貼在留言。下一支我實際在 Windows 上開 Codex 的 Sandbox。這個頻道只講 AI 工具的設定和帳單，不講八卦，想在它改版前先知道，就訂閱。」理由：202–216s 的對話氣泡示意要換成真實終端機被 deny 的錄影，這段同時就是結尾 CTA 的素材。

---

## 6. 上架與量測計畫（接下來 4 週）

### 6.1 第 0 週（本週內，全部是站主在 Studio 與後台的動作）

1. 接上站內互導（第 1.3 節第 1 件）。
2. 頻道頁衛生清單（第 1.3 節第 2 件）：橫幅、說明前 45 字、關鍵字、預告片、3 個系列清單（AI 名詞十分鐘／AI 月費算盤／帳號守門員）、精選區塊、18 支置頂留言（一句重點＋一個問題）、18 支結束畫面（訂閱＋同系列一支）、第三個 hashtag 統一。
3. 匯出 Studio 數據（第 1.3 節第 3 件），並把 2026-09-27-ai-video-batch-first-week-analytics 的範圍擴到 18 支。
4. 在 Studio 對 S88lbAsLz2E、UOgxCymxb1I、FYHFsj0SB7Q 各上一張 B 版縮圖做 Test & compare（兩週）。
5. 放配樂床與音效組到 _music／_sfx，填 slides_music_track／slides_sfx_set；在 Studio 開自動配音。
6. 寫下頻道級的觀眾定義與立場（目前 09-29 仍空白），並在 DESIGN／STORY／HANDS-OFF 三份互相矛盾的節奏規劃裡選一個。

### 6.2 第 1–4 週的上架規則

- 長片每天最多 1 支，每週 3–4 支；產量端同步把 draft_interval_hours／max_drafts_per_month 調到這個量，用 STORY.md:200 的背壓避免「可以上架」佇列塞爆 20 GB 檔案區。
- 時段：第 1–2 週固定週六／日 09:00–10:00（Buffer 1.8M 支研究：長片早上 8–11 點中位互動最高、週日 10 點最佳、週三四最弱）＋平日 19:00–20:00；第 3–4 週對調順序；第 28 天用 Studio「觀眾上線時間」（最近 28 天）決定之後的時段。台灣本地的時段資料只有 2013 年的「晚間 8–11 點」，已過時。
- 題目配額：每週至少一半常青題，三條線各選一支先做——AI 月費算盤（ChatGPT Go vs Plus 台幣價一年差多少；Google AI Pro／Plus 學生免費一年到期怎麼不被扣款；Claude 額度一下就用完怎麼算）、帳號守門員（passkey 是什麼、FB／IG 被盜前先開這兩個設定；ChatGPT／Gemini／Claude 隱私設定）、Google 免費工具箱（Google Vids 免費版實作：額度、浮水印、中文提示；Gems 搬到 skills 完整步驟；NotebookLM 免費額度）。新聞題只做「一般人在用的產品＋免費／價格／台灣能不能用」且在 48 小時內上，超過就改常青寫法。
- 標題：前 15 字放產品名與一個具體數字或日期，≤36 全形字，用搜尋建議裡的原詞（passkey、ChatGPT Go vs Plus、Gemini 免費一年、買網域）；「數字是誰說的」留在片中當方法，不當主標。
- 新片的規格改動（prompts.mjs outro 三句與訂閱句、COMMON 放行自家文章數字、lint 免責片語 warn、QA 縮圖三條）在第 1 週內上線，之後上架的片才算「改過的版本」。

### 6.3 Studio 要看的 5 個數字與門檻（按順序判讀）

| # | 數字（在哪） | 門檻 | 指向的問題 |
|---|---|---|---|
| 1 | 曝光次數＋流量來源（影片分析 > 觸及率） | 7 天曝光 < 1,000 且「瀏覽＋建議影片」不到一半 → 系統沒在推 | 題目／曝光：跟縮圖無關 |
| 2 | 曝光點閱率 CTR（同頁） | 曝光 ≥1,000 後再看：< 2% 問題在縮圖標題；2–10% 正常（YouTube 官方：一半的頻道與影片落在這區間）；> 10% 但平均觀看時長很低 → 騙點擊 | 縮圖標題 |
| 3 | Intro 前 30 秒留存（互動 > 觀眾續看率，需 ≥100 次觀看；目前只有 S88 與 UOgx 過門檻） | < 60% → 開場沒兌現標題承諾 | 開場 |
| 4 | 平均觀看比例 APV／平均觀看時長 | 8 分鐘片 < 30% 要處理，40–55% 健康（從業者經驗值，無官方數字）；官方只說長片看絕對時長 | 中段節奏、重複 |
| 5 | 每支帶來的訂閱者＋訂閱來源（觀看頁 vs 頻道頁 vs 其他） | 每千次觀看 < 0.5 位（P25）→ 片尾沒理由或題目吸到一次性觀眾；≥ 2 正常；≥ 4.6 好 | 結尾與頻道定位 |

另外看「訂閱來源」是否為 YouTube 以外或頻道頁：若 3 位來自那裡，多半是認識的人，不能當內容訊號。四週後能回答的問題：縮圖 B 版有沒有 Winner；常青題 vs 新聞題的首 7 天曝光；兩個時段哪個觀眾在線；哪些題目的觀眾會留下來。

---

## 7. 限制與沒看到的

- **沒有音檔**：同一聲音 Sulafat、無配樂音效、句間停頓固定 300 ms、片頭片尾有無聲音、TTS 唸英文品牌名準不準，全是從 CC 時間軸（0.60–0.63 秒是換景間隔不是句間停頓）、tools/video/tts/requests.mjs、core/timeline.mjs、10-03 設定快照推論；ElevenLabs、雙說話者都未試聽。
- **沒有 Studio 後台**：曝光、CTR、留存、流量來源、訂閱來源、結束畫面點擊率全部拿不到；YouTube Analytics API 也沒有曝光與 CTR。報告裡每一條「high／medium」都因此被降級，第 6 節的門檻是給站主自己對照用的。
- **頻道只開 11 天、樣本極小**：3 位訂閱多 1 位就差 33%；7 支上架不到 3 天（cc09、xSrF、uoVK 當天；LzAw、1I0K、vxv8 2.5 天；UWYo 3 天），觀看最低的 5 支裡 4 支就是這些新片，拿它們當題目或標題的判決不成立。
- **「被反駁」不等於「缺失不存在」**：D01／D02／D06／D07／D10／D13 的事實面多半核實成立，被反駁的是「因此訂閱低」的因果與部分引證；反之「通過」的 D03／D05／D08／D09／D11／D12 也全被降為 low／unknown。
- **外部驗不到的**：結束畫面、資訊卡、留言數、置頂留言、按讚數是否隱藏、AI 揭露怎麼勾、預設語言是否 zh-TW、ja/ko/zh-CN localizations 是否齊、Community 分頁資格——watch 頁只回同意殼，yt-dlp 單支端點被 bot check 擋；只能列為站主 Studio 自查項。
- **搜尋資料的限制**：ytsearch12 是非個人化、非地區加權、也不是搜尋量；「排第 1 卻只有 6–34 次」只能說「同語言競爭少且需求訊號弱」；suggestqueries 建議詞每天變動（「chatgpt 方案」「Grok 4.7」兩天內已不同）；Google Vids 建議詞為空但它是頻道第一名，任何「建議詞為空就不做」的硬關卡會砍掉自己最好的片。
- **參考頻道的數字全是快照**：訂閱與觀看一天內就變（黑貓 55,100→55,200）；由頻道頁相對時間換算的上傳日近期 ±1 天、超過一個月可差數週；meta.json 裡 channel_follower_count 的 5 與 8 是「5.5萬／8.87萬」被解析壞的值，不可引用；黑貓與 Gary 的訂閱基數是 Mokaair 的 1.8 萬到 3 萬倍，單支觀看比較只是格式範本。
- **已公開 18 支無法換檔**：縮圖、標題、說明欄只能 Studio 手改（publish.md:93），而且產線同步會把原縮圖再送一次（sync.py `_thumbnail`），要先加開關；燒字幕、片頭長度、結尾句改規格只對新片生效；重做舊片是新 id，S88 的 251 次歸零。
- **政策面只能說「有條文、無案例」**：官方頁 1311392 明列同一套片頭片尾為允許；AI persona 條文針對醫療／法律／財務／政治建議；本次查核沒找到 TTS 旁白＋投影片科技頻道被處分的公開案例（是「沒找到」）；頻道離 YPP 審查很遠。
- **未查證**：Community 分頁資格門檻；Shorts 自動上架要過 API 稽核（票仍開著、法律頁沒貼 YouTube API 段落）；站內互導斷裂只看了程式碼沒查正式站資料庫；vidIQ 的研究頁無法開啟（403／429），所有引用 vidIQ 的數字都已從正文拿掉；TechRepublic 連結 403。
- **沒重跑的**：18 支縮圖與故事板沒有再逐張看（沿用通過的 D05／D08 與事實查核）；參考頻道近 30 支標題統計未重算；參考片的 zh-TW 字幕今天抓得到，所以第 4 節的開場與結尾秒數以 VTT 為準。

---

## 8. 來源清單（去重；只放事實查核判定 supported 或 partly 的；unsupported 的說法已從正文移除）

### YouTube 官方

- 頻道營利政策（含 2025-07-15 註記、Generic or Repetitive Content、AI Personas Related to Sensitive Topics、審查六項）：https://support.google.com/youtube/answer/1311392?hl=en
- 通知上限：https://support.google.com/youtube/answer/7389684?hl=en
- 曝光與 CTR FAQ：https://support.google.com/youtube/answer/7628154?hl=en
- 觀眾續看率（Intro、100 次門檻）：https://support.google.com/youtube/answer/9314415
- 觀眾上線時間：https://support.google.com/youtube/answer/9314416?hl=en
- Discovery FAQ（上傳頻率無相關、長短片觀看時間）：https://support.google.com/youtube/answer/141805?hl=en
- 片尾畫面（5–20 秒、≥25 秒）：https://support.google.com/youtube/answer/6388789?hl=en
- 頻道預告片：https://support.google.com/youtube/answer/3219384?hl=en
- 系列播放清單：https://support.google.com/youtube/answer/6084043?hl=en
- 頻道關鍵字：https://support.google.com/youtube/answer/2976814
- 縮圖與標題建議：https://support.google.com/youtube/answer/12340300
- A/B 測試標題與縮圖：https://support.google.com/youtube/answer/13861714 、https://support.google.com/youtube/answer/16391400
- 標籤影響「minimal」：https://support.google.com/youtube/answer/146402
- 中插廣告 8 分鐘：https://support.google.com/youtube/answer/6175006?hl=en
- YPP 門檻：https://support.google.com/youtube/answer/72851?hl=en ；2027-02-01 新規：https://blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/ 、https://support.google.com/youtube/answer/12843009?hl=en
- AI 揭露：https://support.google.com/youtube/answer/14328491?hl=en ；標籤位置與自動貼標（2026-05-27）：https://blog.youtube/news-and-events/improving-ai-labels-for-viewers-and-creators/
- 自動配音（2026-05-15）：https://blog.youtube/creator-and-artist-stories/youtube-auto-dubbing-explained/ ；翻譯標題說明：https://support.google.com/youtube/answer/6289575?hl=en
- 推薦機制：https://www.youtube.com/howyoutubeworks/product-features/recommendations/ 、https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/
- 頻道版面三個建議（2012）：https://blog.youtube/news-and-events/three-tips-to-help-potential-viewers/ ；預告片建議（2013）：https://youtube-creators.googleblog.com/2013/03/convert-viewers-into-subscribers-with.html
- Beaupré 2026-09-01 Creator Insider（影片 https://www.youtube.com/watch?v=rHLjxrbXmmY ；逐字整理 https://ppc.land/subscribers-skip-90-of-uploads-in-their-feed-youtube-director-says/ ）
- Gemini 可用性表（Connected Apps）：https://support.google.com/gemini/table/17434654

### Google／Meta／OpenAI 與媒體

- Google 台灣 2025 年度搜尋（官方榜單）：https://blog.google/intl/zh-tw/products/explore-get-answers/2025-year-in-search/
- Google 學生方案公告日 2026-08-20：https://technews.tw/2026/08/20/google-offers-free-student-plans-for-one-year-and-launches-new-study-tools/ 、https://blog.google/intl/zh-tw/products/explore-get-answers/ai-pro-student-offer/
- Brandcast 2025（40% 觀看時間來自海外）：https://blog.google/intl/zh-tw/products/explore-get-answers/2025-youtube-brandcast/ ；大螢幕 3 小時：https://business.google.com/tw/think/search-and-video/new-era-streaming-youtube/
- iThome 2013-12-03（晚間 8–11 點）：https://www.ithome.com.tw/news/84101
- Meta One Step Ahead 新聞稿：https://about.fb.com/news/2026/09/meta-one-step-ahead-campaign/ ；臉書通行密鑰選單路徑：https://mrmad.com.tw/how-to-setup-facebook-passkey
- OpenAI 停供 Cursor（Inside 2026-08-29）：https://www.inside.com.tw/article/42242-openai-cursor-spacex-model-supply-end
- TechCrunch 2026-07-20（政策拆分與 Halprin）：https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/
- TeamYouTube 2025-07 回應（轉載）：https://ppc.land/google-clarifies-youtube-monetization-policies-amid-creator-confusion/
- Social Media Today：推薦與上傳支數 https://www.socialmediatoday.com/news/youtube-answers-common-questions-about-its-recommendation-algorithms-to-hel/620209 ；每日推薦無上限、一次上傳太多 https://www.socialmediatoday.com/news/youtube-answers-common-questions-on-video-discovery-and-distribution/588415/ ；頻道轉型 https://www.socialmediatoday.com/news/youtube-executives-share-strategies-on-channel-pivoting/830850/
- 執法案例：Gigazine 2025-12-23 https://gigazine.net/gsc_news/en/20251223-youtube-shuts-down-ai-fake-movie-trailers-channels ；Tubefilter 2026-01-29 https://tubefilter.com/2026/01/29/youtube-ai-slop-channel-crackdown-bans/ ；Kapwing AI slop 報告 https://www.kapwing.com/blog/ai-slop-report-the-global-rise-of-low-quality-ai-videos/
- TechNews（媒體報導，非官方）：https://technews.tw/2026/02/02/youtube-has-a-big-incentive-to-nuke-ai-spam/ 、https://technews.tw/2026/08/06/youtube-explains-its-ai-slop-policy-and-why-some-creators-wont-get-paid/ 、https://technews.tw/2026/06/16/faceless-creators-are-becoming-collateral-damage-in-youtubes-ai-cleanup/
- 404 Media（Sleepless Historian）：https://www.404media.co/ai-generated-boring-history-videos-are-flooding-youtube-and-drowning-out-real-history/
- 靜音自動字幕（轉述 Creator Insider）：https://www.socialmediatoday.com/news/youtube-adds-auto-captions-when-muted-new-ai-feature/811912

### 第三方研究與經驗談（標明性質）

- OverseerOS 76 頻道訂閱換算（2026-09-26）：https://www.overseeros.com/blog/youtube-subscriber-conversion-rate ；新上傳對舊片（12 頻道，作者自承無法區分 cannibalization）：https://www.overseeros.com/blog/does-uploading-new-youtube-video-hurt-old-videos
- ytgrowth 18,423 支觀看曲線：https://ytgrowth.io/blog/youtube-view-growth-curve
- Great Big Story back catalog（Digiday 2018）：https://digiday.com/media/cnns-great-big-story-grows-on-youtube/
- Buffer 1.8M 支時段研究（2026-07-24）：https://buffer.com/resources/best-time-to-post-on-youtube/
- Metricool 每週 2–4 支（Tubefilter 轉述）：https://www.tubefilter.com/2026/08/03/youtube-shorts-long-form-study-metricool/
- 留存經驗值：OpusClip https://www.opus.pro/blog/youtube-retention-graphs-explained ；Humble&Brag 2026-09-30 https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
- 手機標題截斷（拉丁字元約 50）：https://creaticalc.com/blog/youtube-title-mobile-feed
- Crowd React Media 聽眾實驗（radioink 2026-07-07）：https://radioink.com/2026/07/07/radio-listeners-cant-detect-ai-voice-but-dont-trust-it-either/
- Adobe Express AI 音訊信任調查（2026-02-18 原頁）：https://www.adobe.com/express/learn/blog/ai-audio-consumer-trust
- Kapwing 無真人頻道實測（60 支裡 58 支 Shorts）：https://kapwing.com/resources/we-grew-a-faceless-youtube-channel-to-1000-subscribers
- AIR Media-Tech 配音留存三案例：https://air.io/en/creators-spotlight/ai-dubbing-retention-3-youtube-case-studies
- 七七行銷筆記統計（outlierkit，2026-08-05 快照）：https://outlierkit.com/channel/77mediabook
- TTS 價格與能力：https://ai.google.dev/gemini-api/docs/speech-generation 、https://ai.google.dev/gemini-api/docs/pricing 、https://elevenlabs.io/pricing 、https://costbench.com/software/voice-apis/elevenlabs-api/
- 2025-07 政策整理（原 supertone 網址已轉）：https://antinodeaudio.com/en/work/youtube-ai-monetization-policy-2025-eng

### 參考頻道與影片（yt-dlp 2026-10-07 抓取）

- Mokaair：https://www.youtube.com/@Mokaair/videos
- 黑貓研究院：https://www.youtube.com/@qiqiqushi0/videos 、https://www.youtube.com/watch?v=coA8iBMMLY4 、https://www.youtube.com/watch?v=vjAM8T_92Rs 、https://www.youtube.com/watch?v=IbjI1ygRWgk
- Gary Chen：https://www.youtube.com/@garychenai/videos 、https://www.youtube.com/watch?v=UWdn0w-fbzQ 、https://www.youtube.com/watch?v=2mtn-Qp59y4 、https://www.youtube.com/watch?v=3iXsVw9wsjw 、https://www.youtube.com/watch?v=xs6-p7fFYH8
- 可波 AI 白話：https://www.youtube.com/@kobatalk/videos 、https://www.youtube.com/watch?v=Ol82S1UVt7E 、https://www.youtube.com/watch?v=HkCy3xZS3IA 、https://www.youtube.com/watch?v=kIJF2XYMawg
- 泛科學院：https://www.youtube.com/@panscischool/videos 、https://www.youtube.com/watch?v=114H9EWKfzM
- PAPAYA 電腦教室：https://www.youtube.com/@papayaclass/videos 、https://www.youtube.com/watch?v=NLiarcXvgns
- 七七行銷筆記：https://www.youtube.com/@77MediaBook/videos ；孔老師：https://www.youtube.com/@Teacher_Kong/videos ；漢克蔡：https://www.youtube.com/@ainthology/videos ；電腦王阿達：https://www.youtube.com/@kocpc/videos ；志祺七七：https://www.youtube.com/@shasha77/videos ；三師爸：https://www.youtube.com/@sensebar/videos
- 同題競品：科技兔 https://www.youtube.com/watch?v=Ozr75-oQEFg ；志祺七七 Hugging Face https://www.youtube.com/watch?v=2iOFQtkc2G4 ；今天比昨天厲害 https://www.youtube.com/watch?v=bj07f9II6NQ ；數位時代學生方案 https://www.youtube.com/watch?v=r9aEpyAHcsc ；Markluce AI https://www.youtube.com/channel/UCzYxev5q9HTv3LvBUMEv87g/videos ；Sleepless Historian https://www.youtube.com/@SleeplessHistorian/videos

### 本地資料與產線檔（唯讀）

- 資料包：scratchpad/data/channel_pack.md、data/ytdlp_meta.jsonl、data/visual_pacing.json、subs/*.zh-TW.vtt、thumbs/*.jpg、thumbs_sheet.png、sbsheets/*.png、about.html、channel.html
- 研究與工作檔：scratchpad/report/research-1.md～research-7.md；scratchpad/work/（twai、titles-thumbs、voice、seo、reference-deep-dive、factcheck、factcheck2、completeness 等）
- 產線規格：docs/videos/README.md、ILLUSTRATED.md、HANDS-OFF.md、MILLION-VIEWS.md、BRANDING.md、DESIGN.md、STORY.md、SHORTS.md、AUTOMATION.md、ai-terms/README.md；.agents/skills/youtube-video/SKILL.md 與 references/script-writing.md、publish.md、visuals.md、formats.md、automated.md、thumbnails.md
- 產線程式：tools/video/automation/prompts.mjs、register.mjs、flow.mjs；tools/video/core/lint.mjs、cadence.mjs、timeline.mjs、captions.mjs、metadata.mjs、branding.mjs、drama.mjs；tools/video/qa/pace.mjs、policy.mjs、thumbnail.mjs；tools/video/templates/templates.mjs、theme.css；tools/video/tts/requests.mjs、split.mjs；tools/video/render/subtitles.mjs；apps/api/app/video_youtube/sync.py、state.py、client.py、requests.py；apps/api/app/video_reviews/public_api.py；apps/api/app/video_shorts/slots.py
- 票：tasks/open/2026-09-27-ai-video-batch-first-week-analytics.md、2026-09-27-video-youtube-sync-field-test.md、2026-09-24-video-obs-import.md、2026-09-26-video-hands-off-api-audit.md、2026-09-30-news-automation-has-no-taiwan-sources.md、2026-10-03-produce-video-openai-devday-2026-recap.md、2026-10-03-ai-term-system-one-model-video.md、2026-09-28-sothatswhy-mascot-setting.md；tasks/done/2026-09-26-videos-learn-from-a-reference-chapter.md、2026-10-05-voice-performance-contract.md、2026-09-30-set-register-pause-beats-in-code.md
