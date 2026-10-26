# C06｜category metadata 獨立差分查核

查核日：2026-10-26。查核者：`/root/approved_visual_source_delta`，未參與作者稿。

**SOURCE PASS／WRITTEN VISUAL PASS／METADATA DELTA PASS。** 現稿163句、138景（137 shot、1 outro）。本輪只審 `category: explainer → story`，沒有新敘事判定；`actualasset_verified=false`，未實測TTS或12–14分鐘。

## 本次四輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `aac065fb5663fd1a75dbac064470ceaefea43eac08a162ba3be96d9130724d11` |
| script.md | `a5a00dab26911197bbd96faaf5fef760396d3eaabd68e45a3072bff350683817` |
| narration-only.json | `4773cd50bd7c5a21910106a57b02b48ce7a7f24111a69698657ce25cf341b70b` |
| claims.json | `270cf9419dc401d2a6381363fbd187cb0bf09f01cdc5c3a114eb8eb10d10e926` |

image-reuse-plan.json SHA：`5d6f9c6bc6e91d960b5575652b263f7d55bd3ff785162ac2d12801a0891d5523`。本輪完整獨立收據：[reviews/source-teaser-story-category-independent.json](reviews/source-teaser-story-category-independent.json)。

## 不可變來源基線與差分

即前來源／書面圖PASS基線在 `history/teaser-plan-before-story-category`：video SHA `0636c34a4ebbefa2b5fe5f354c08097c736783b1349e1959d1b1e98f46cc76ca`；原plan SHA `567791635dbe5240461ec41f5bc3546e4363a48bf624dd6023235dd7e941ff18`；原獨立報告 SHA `abfaa703a0daa7429d81eb549f95975d719698ec75a24bf70c13d688ceff3a40`；原verify SHA `c77bd25f53b0f53051c018a52ec78eee5c22c03b7ea1e4fd57c09ff8ee32f1a4`。原報告仍逐bytes保留，未覆寫。

遞迴比較全部video物件，僅一個 `/category` 葉節點改變。163句的ID、scene、文字SHA逐句全同；138景完整物件、prompt/camera、scene順序、chapter、loops、voice、look、subtitles、其他metadata完全相同。script/narration/claims JSON、claims.md、brief、series、原件表及anchors逐bytes相同，來源與書面圖按原精確PASS繼承，不聲稱本輪重開全部原件。計畫只更新source SHA／revision／category差分說明，pair request及停止條件完整物件未變。56個archive、78個auxiliary、17個runtime檔、11個media狀態檔及批舊53個原檔實SHA核對全同。

## 原生讀值

官方screenplay新舊及已批runtime逐bytes相同，SHA `e00fd07d54ef284a5577327f999f4e46222aef455417f3fc878c1a91f11b124e`。現有runtime唯讀字典 SHA `88d56a0e7edfdd645d605193f653640121702d2fc2c819731966c8f545499416`；narrative、speech、look、pictures、mix五項原生hash全同。既存native record只作 `narrativeReviewMatches`，新舊均true；未讀新盲票、未重判敘事。producer的變動只有category常值；只在記憶體回放，四輸入與claims.md逐bytes精確重現。

完整字典、未變brief/series及八語context下，**native lint為0 errors、19 soft warnings，原版為17**。新增soft warnings原文：

- `about 16.2 minutes; the target is 12-14`
- `the outro has 2 sentences; the close is 3: the answer with its number, a comment question, a subscribe invitation with a reason`

前者為工具估計，不是實際音訊；後者保留為原生提示，不以本輪metadata審查代發敘事判定或改寫旁白。137 shot與outro在story schema下均合法，未改模板。

## 共圖 request 與停線

| pair | 完整composed prompt SHA | seed1 1K key | seed1 2K key |
| --- | --- | --- | --- |
| small-hands-firm-clay | `ca2d9db260953b4f58278b23def291651e49c94fc2f4b5dae9e75aa0c87bf33d` | `132306c2f7b44c85` | `00295b1753b9796e` |
| modeled-bouquet-before-finishing | `6e1d50ec239a618cd43cea29d86a797fd2e4a346fcff4810605777fa0f56e8f6` | `310552f52e4fb3c6` | `f2c7373fe2c7100e` |

原生resolveLook、完整composeShotPrompt、camera/cast/references/size/seed與Stage.imageKey新舊及每pair兩端均相同。四個planned key的live cache仍全missing，**第二條teaser命令必須停，不得新派送或另購**。正式製片仍須先正常驗收payoff，再於第二命令前核對live cache與accepted實檔SHA；兩端judge/retake差異停pair；trim後selected衍生檔、官方manifest、render/assembly引用與實檔SHA全同才可記實際共圖。

此category是本地來源metadata選擇。官方sync/server分類契約僅作背景，不在本輪聲稱或變更任何後台category；作者「避免覆寫既有後台分類」的理由不當作證據。沒有runtime、approval、後台、Git或付費操作。

## 既有原件來源表

未變事實依精確來源基線逐句接鏈，不冒稱本輪重開全部原件。

| 代號 | 原件 | 定位與範圍 |
| --- | --- | --- |
| H1-scale | https://newsroom.hasbro.com/node/34691 | 2024公告About PLAY-DOH：over500Mcans shipped a year。；公司年出貨罐數口徑，不是使用人數、營收或零售成交。 |
| H2-birthday | https://corp.hasbro.com/news-releases/news-release-details/hasbro-trademarks-favorite-smell-childhood-play-doh-scent | 2018公告：brand inception in1956。；公司回顧的品牌生日，不是本次已見首單發票。 |
| H3-display | https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience | 2026-07-09公告：首個專為成人設計系列、adult crafting/home decor、preserved/displayed與finishing spray幫助維持結構數月。；成人線定位與保存數月均保留公司公告歸屬，非本次實測或銷售成功；不聲稱經典材料全改成永久保存。 |
| H3-kit | https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience | 2026-07-09公告：shaping individual petals to arranging a finished bouquet；tools/molds/vase/spray；每款how-to videos。；限該花藝套件的公司介紹；匿名假想手作動作不是親測或歷史重建。 |
| K1-cleo | https://www.kutol.com/kutols-story/ | 公司史Cleo被派清算卻買下生意、Kroger壁紙清潔用品段。；企業多年後的回顧，不是同期合約或交易帳簿。 |
| K1-kay | https://www.kutol.com/kutols-story/ | 公司史Joseph的sister-in-law Kay Zufall、kindergarten、材料受歡迎與Rainbow分支段。；教師姓名與身分來自本公司回顧；M2的a teacher不獨自承擔Kay身分。 |
| M1-kroger | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | 2016回顧1933 Kroger合同段，含從前未做過壁紙清潔材料。；館方明轉引Tim Walsh後出書籍，不是本次已讀1933原始合約。 |
| M1-noah | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | 1933段：brother Noah, a product developer、winning formula及malleable clay-like compound。；館方回顧的開發分工；不倒推1965專利配方為1933原配方。 |
| M1-wall | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | 壁紙清潔用途與煤灰需求段：wallpaper cleaner、soot residue。；柔軟清潔材料與壁紙用途；觀眾壓、捏是明示假想動作，不聲稱已見當年操作影片或性能測試。 |
| M1-1949 | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | Following Cleo death in1949, son Joseph took over。；館方回顧；本稿置於1950年代需求改變之前。 |
| M1-demand | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | early1950s sales plummet、二戰後家庭由coal-based furnaces轉oil/gas、減少soot residue段。；館方回顧的需求變化，不升格成帳本驗證或唯一破產原因。 |
| M1-kay | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | 1955 Kay schoolteacher提出handicraft/play、Joseph拜訪看作品、reformulate/repurpose並沿用設備空間。；公司/館方回顧，非同期教室紀錄；不補洗劑/香料改配方細節。 |
| M1-brand | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | 1956 Rainbow Crafts subsidiary、repackaged Play-Doh、向Cincinnati elementary schools行銷段。；公司與推廣脈絡，不宣稱1956是已證第一筆出售。 |
| M1-colors | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | By1957 available in three new colors red/yellow/blue。；館方回顧顏色加入，不推1956所有色系或現代全配方。 |
| M1-television | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | 1956/1957發展段後：缺大筆廣告預算、Captain Kangaroo主持人安排至少每週使用一次。；館方回顧的推廣動作，沒有精確合作日/費率，不宣稱本次驗證全國銷量因果。 |
| M1-factory | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | In1960 two engineers、multiple ways、Fun Factory minimal force extrude shapes/designs段。；1960工具功能的館方回顧；配鏡為匿名一般槓桿/出口示意，無現代兩軌倒配。 |
| M2-hard | https://www.toyhalloffame.org/toys/play-doh/ | Joe learned from a teacher、kids usually found modeling clay too hard to manipulate、送材料試用與學校反應。；M2不具名的teacher；Kay姓名由K1/M1補，非正式兒童試驗/療效。 |
| M2-colors | https://www.toyhalloffame.org/toys/play-doh/ | 1957 softer version in primary colors段。；同The Strong機構回顧，不當另一個獨立同期見證。 |
| P1-header | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF1標頭：NoahW./JosephS.、assignors to Rainbow、Filed May17,1960、Patented Jan26,1965；文首兒童用途。；申請與核發分開。後來核發的文本不充當1955實際配方或現代每罐的規格。 |
| P1-shape | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF4印刷欄7–8 claim9：moldable into any desired shape、consistency to retain its shape；特性段。；專利主張/設計要求，不是作者獨立性能試驗。注意原件是claim9，不沿用r1作者表的claim8誤定位。 |
| P1-goals | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF1文首objects：soft/pliable、slow drying、re-worked/re-molded。；該文本的設計目標；匿名假想變形不代表歷史或現代產品全數實測。 |
| P1-clean | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF1 objects：cleanliness、notsticky/non-staining；後段特性。；設計主張，非當代安全/可食或本次效果保證。 |
| P1-film | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF1印刷欄2：It is believed hydrocarbon distillate thin film around solid particles；coated flour particles濕熱糊化與thin film滑順不黏段。；保留作者認為/文件描述的假說層級；概念模型不是顯微實測或1933配方。 |
| P1-mixing | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF3印刷欄6：preferred method、ordinary bakery dough mixer、熱水與材料混合成homogenous mass、type of mixer not critical。 同PDF3印刷欄6製法結尾：混成可塑團塊後immediately placed in air tight containers。；專利描述的一種製法；不列比例/溫度/時間作DIY配方，不稱親見工廠實際照此生產。 |
| P1-color | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF1 objects：different colors incorporated without affecting moldable consistency。；加色與可塑性兼顧的設計要求，不證1957工廠實際色方或當代全系列同方。 |
| P1-store | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF4印刷欄7：normally stored in air tight container、玩後可放回、此方式聲稱工作特性up to3years。；1965核發文本對該組成的保存主張，非本次三年試驗/今日產品保存期限；正文保留文本聲稱。 |
| P1-dry | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF3–4印刷欄6–7：open air幾天乾硬、painted with oil/water/poster paints、once thoroughly dry not reclaimed、乾硬後crayons。；該文本的描述及不可重塑取捨；不稱所有現代產品同一乾燥時間或永久保存。 |
| P1-binding | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 核發PDF1–2：hardener/astringent為可選成分，其功能bind components into cohesive mass；另見claims的binder說明。；該文本的可選黏結作用主張，不宣稱每一當代產品必含或本次獨立實驗證實。 |

本查核沒有付費、後台呼叫、runtime/approval/media或Git操作；不授權發布。生成圖QA、實際共圖、12–14分鐘媒體實長與成片驗收仍未完成。
