# 五支新版片頭濃縮稿

日期：2026-10-12。依站主選擇製作新版完整影片，之後重新上傳；本檔只記錄本次新增片頭的編輯決策與查核。`intro-specs.json` 是繁中、英文、日文、韓文的旁白輸入，四語逐句共用 `intro01` 起的 ID 與同一來源 scene。原完整稿與原片不在本次撰稿範圍內修改。

## 結構與交付邊界

- 每支 7–8 句。繁中約 130–150 個非標點字；英文約 90–100 詞。撰稿目標為自然說書 30–60 秒；H02 四語片頭已合成並對齊為 41.5666667 秒，其他影片的字數估計仍不能當成音訊實測。
- 第一秒直接落鉤，前兩句有標題的名字、日期或數字。取出正文已有的具體事件，留住兩到三個懸念；不唸章節目錄，不在片頭邀請訂閱。
- 每句都指定凍結完整稿中存在的 scene，並連到該場景的實際渲染片段。獨立覆核後，H02 生日句與 U02 名字／地圖句的素材對應已修正，詳見下方覆核紀錄；不是只憑場景名稱推測畫面內容。
- 新片頭取代原第一章，接原第二章。片頭問句與原第二章的內容相接；原第二章首句保留，沒有宣稱已逐字改成同一個問句。
- 翻譯保留原來的疑問與未定論，年份及數字寫成適合口播的形式。四語敘事與翻譯已完成獨立覆核；音訊的專名發音與聽感另經合成後檢查，不能用文字覆核或總字數代替。

## 獨立覆核與已套用修正

`independent_review` 已完成五支四語的敘事、翻譯與來源畫面覆核，未發現阻擋項。主協調者另讀過整份稿，套用以下修正；本檔更新時已直接讀回 `intro-specs.json` 確認這些值：

| 位置 | 已套用的結果 | 原因 |
|---|---|---|
| H02 `intro04`，四語 | `scene: route-third-birthday` | 三歲生日句改接正文中對應生日的實際渲染片段，移除出生時插圖造成的年齡歧義。 |
| U02 `intro02`，四語 | `scene: secret-compare-versions` | 名字與地圖公開的句子接原版／解密版的實際對照素材。 |
| U02 英文 `intro01` | “Why black out the name Area Fifty-One when the base was already visible in photographs?” | 明確說照片拍得到的是基地，避免 `it` 指涉成名字。 |

事實仍以五支凍結的完整稿、其中的主張與來源鏈為界；獨立覆核沒有把懸案的假說升格為結論。原片素材也保留照片、後人插圖與傳說的區別。

### 媒體進度快照（2026-10-12）

H02 四語的生成收據及 `curio-h02/intro/shared-timeline.json` 已落地。共同時間軸為 30 fps、1247 格、41.56666666666667 秒，包含繁中、英文、日文及韓文，沒有時間拉伸；七句各有相同的起迄格。此數值已從工作目錄的實際 JSON 讀回，並非字數換算。

本次更新時，H02 音訊檢查正在執行，其他影片的生成仍在進行。英文收據狀態為 `aligned-awaiting-audio-check`，`owner_listened: false`、`full_video_approved: false`。因此這裡只確認 H02 四語已生成及共同時間軸已建立，不宣稱音訊檢查通過、站主已聽、完整成片已核准或已重新上傳。

## 懸念、回收位置與第二章接口

| 影片 | 片頭懸念／正文回收 scene | 原第二章接口 |
|---|---|---|
| curio-h02 羅阿諾克 | 懷特為何高興：`return-message-rule`；讀懂卻沒到目的地：`route-last-anchor` 至 `route-england-return`；戒指認出材質卻認不出主人：`h02-find-brass-analysis`、`h02-find-owner-remains` | `hook-place-not-verdict`：「讀到刻下的文字，就知道應該去哪裡找。有去處，卻沒有人的下落。」 |
| curio-u02 五十一區 | 拍得到卻塗黑：`secret-usgs-photo`、`secret-compare-versions`；八年申請與一九六七年文件：`release-request-2005` 至 `release-memo-1967`；高空銀光引發通報：`silver-u2-sunlit` 至 `silver-steps-sighting` | `legend-chapter` 先進入流傳的版本，再對照計畫史。 |
| curio-h03 通古斯 | 中央直立樹與主坑：`two-tree-patterns`、`airburst-chain`；坑底老樹樁：`drainage-ditch`、`old-stump-bottom`；八千萬與湖泊線索：`assumption-propagates`、`cheko-evidence-table` | `date-of-flash` 回到一九〇八年六月三十日，再交代十九年後的現場。 |
| curio-l08 麥田圈 | 記者看著做卻被判非人造：`confess-sevenoaks` 至 `confess-compare`；坦白後圖形更複雜：`after-second-wave` 至 `after-swiss`；晚年後悔與為何公開：`field-regret`、`confess-why-time`、`confess-why-dave` | `legend-chapter` 回到一九八〇年代的流傳說法。 |
| curio-h01 瑪麗賽勒斯特 | 糧水在、小艇不在：`list-davits`、`list-stores`；劍上疑似血跡被推翻：`court-chemist`；九個空桶：`answer-genoa-quay`、`answer-nine-casks` | `legend-chapter` 先講熱飯菜等版本，之後再用登船紀錄逐項對照。 |

## 來源約束與措辭

### 羅阿諾克

逐句事實都來自凍結完整稿。開場不把 CROATOAN 當密碼，不宣稱全員獲救或死亡；「高興」是懷特當時對留言的解讀。克羅托安的地名、族名與約定在正文回收，戒指不被寫成確定屬於殖民者。

本次重新打開 [NPS 1590 Rescue Voyage](https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm)，確認一五九〇年八月十八日上岸、兩處刻字與未完成航程；[懷特原始敘事的數位全文](https://www.gutenberg.org/cache/epub/25645/pg25645-images.html) 可讀。[ECU 戒指分析典藏頁](https://digital.lib.ecu.edu/special/ead/findingaids/1061/) 本次回 403，戒指句保留完整稿已列的分析與未知主人兩層，未另加判斷。

### 五十一區

片頭刻意限定為「解密史書裡公開名字和地圖」，不用「政府直到二〇一三年才第一次寫出或承認名字」。一九六七年文件的既有畫面 `release-memo-1967` 本身就是反例，正文也交代這個差別。不將所有 UFO 通報解釋成偵察機。

本次重新打開 [National Security Archive 的二〇一三年解密說明](https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/)，確認二〇〇五年申請、二〇一三年六月核准與名字、地圖解密。高空反光的原始依據為完整稿所引 [CIA 計畫史第二章](https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf)，書頁 72–73；本次沒有把 CIA 史家的「半數以上」估計搬進片頭。

### 通古斯

倒樹面積保留「大約」。八千萬只作為待追查來源的流傳數字，不當作精確清點；切科湖仍是爭論線索，不稱為已證實撞擊坑。中央直立樹的機制留在正文，片頭不先揭露空爆答案。

本次重新打開 [NASA 二〇二三年專文](https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/)，確認一九〇八年、庫利克一九二七年抵達、中央仍直立但受損的樹幹與後續測繪。老樹樁、八千萬來源、切科湖爭論依完整稿的 `c` 主張及來源鏈；[二〇二五年研究評論](https://pmc.ncbi.nlm.nih.gov/articles/PMC12015480/) 本次遇 reCAPTCHA，沒有把未讀到的新資料寫進稿。

### 麥田圈

只說兩人承認自己的圓，不推論全球所有圖形都是這兩人做的。公開原因在正文保留當年報導與後來回憶兩種來源；片頭不選一個動機當唯一答案。木板、繩子、帽上鐵絲是已記錄的工具，不在片頭教人進田破壞。

本次重新打開 [TIME 一九九一年報導的課程存本](https://www2.nau.edu/~gaud/bio372/class/readings/circ.htm)，核對記者見證、研究者誤判、兩人年齡與工具。公開之後的發展與晚年後悔沿用完整稿、`research.md` 的 Smithsonian、Physics World 與訃聞來源，未新增原因。

### 瑪麗賽勒斯特

說「還能航行」，不把發現時的船寫成完全無損。劍上痕跡是疑似血而非已證實的血；九個空桶是線索，不把酒精蒸氣或拖艇斷繩當定論。韓文使用「알코올 통」，避免譯成裝可飲用酒的酒桶。

本次重新打開 [Smithsonian 的調查專文](https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/)，核對十人、失蹤小艇、半年糧水、一千七百零一桶與九個空桶。化驗與後加傳說沿用完整稿 `court-chemist`、`legend-writer` 等及 `research.md` 原始來源鏈。

## 交給整合者的注意項

1. 原 h01 的 `answer-big` 把「他們不是消失，是回不去了」說得確定；拖艇及斷繩段也有敘事確定度偏高的問題。新片頭不重複這種確定語氣，原正文維持未改；已另開 `tasks/open/2026-10-12-curio-h01-reconstruction-certainty.md` 保存後續獨立歷史查核與正文修訂工作。
2. 原 u02 片頭的「二〇一三年，CIA 才第一次正式印出 Area 51」容易與正文一九六七年文件衝突；本次替換片頭已避開絕對的第一次。
3. H02 三歲生日畫面的歧義已修正：四語 `intro04` 現在使用 `route-third-birthday`，不再使用 `farewell-newborn`。
4. h01 的傳說酒館畫面與 l08 的研究者判斷引用，須保留正文素材已有的語境；不可把傳說畫面當歷史照片。
5. 四語稿已通過獨立敘事與翻譯覆核。本文記錄稿件階段的判斷；成片、音訊與字幕的最終狀態以 `DELIVERY-REPORT.md` 及外部 `delivery-index.json` 為準，站主收看與上傳仍須分別記錄。
