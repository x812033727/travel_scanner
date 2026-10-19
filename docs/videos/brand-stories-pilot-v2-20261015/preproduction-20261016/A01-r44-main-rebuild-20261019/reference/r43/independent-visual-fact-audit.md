# A01 r43 獨立畫面史實稽核

已唯讀檢查 r43 全部 **51 景**（50 條圖片提示詞，`now-outro` 無圖片提示詞）。`manifest.json` SHA-256 為指定的 `be7fc07b…201ced`。以下是提示詞與史料的風險；尚無生成圖片可驗證實際畫面。

| 等級 | 場景與問題 | r44 修法 |
| --- | --- | --- |
| **P2** | `hook-curb` 把陡路緣與樓梯畫成同一地點的相鄰障礙；[Dash 原文](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)沒有交代地點或先後。 | 開場只畫路緣；樓梯留到 `turn-curb` 的獨立示意格。 |
| **P2** | 共用字串插值造成原型與成品混淆。[story-data.mjs](<C:/Users/x8120/.codex/worktrees/a01-branch-sync/travel_scanㄐ/docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r43/story-data.mjs:22>) 的 `early` 內含分號與否定子句，影響 `hook-crew`、`idea-record`、`idea-one-unit`、`idea-longwalk`、`idea-next`、`engine-first-eyes`；`idea-next` 另生成 `The unbranded an unbranded`。`bag` 的尾句又使 `turn-choose` 生成 `prototype's retractable handle`，錯指早期螺絲樣品有伸縮把手。`origin-garage` 把「已鎖好」的 `proto` 插進正在鎖螺絲的動作。 | 三個共用字串只保留名詞與可見特徵；原型區隔另寫完整句。車庫鏡使用尚未接合的兩件物品。重算後直接閱讀全部 50 條成品 prompt。 |
| **P2，畫面劇透風險** | `hook-curb`、`turn-dash`、`turn-choose`、`turn-curb`、`turn-corners`、`turn-fabric`、`turn-shape`、`now-cabin-edge` 在 `now-pocket` 揭示前就要求生成「可擴外袋」，且未明確遮住。這是**提示詞可能導致的風險**，不是已觀察到圖片劇透。 | 揭示前用不提外袋的產品描述，只顯示無外袋的一面；揭示後才使用外袋描述。 |
| **P2** | `now-pocket` 口播「好幾個」及多景共用描述 `several expandable…pockets` 指定了約三個以上外袋。[Dash 原文](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)對 Travelpro 只確認複數外袋；文中「several outside pockets」說的是 **American Tourister**。`now-space` 還指定多個外袋都鼓起，填裝分布未載。 | 改為不限定數量的複數外袋；畫一處或多處擴張即可，不聲稱每袋都裝滿。 |
| **P3** | `now-zipper` 指定 *main-case zipper*；Dash 只說 Rollaboard 的拉鍊沒有卡住，未指明部位。`turn-dash` 把「避免等行李轉盤」畫成記者經過轉盤、然後選箱的連續事件，來源未記此動作。 | 拉鍊用不指部位的局部示意；轉盤改作分隔的象徵畫面。 |

其餘畫面邊界大致守住來源：前方旅客的輪架可畫金屬，Plath 自己的螺絲樣品材質維持未指定；硬殼樣品與後期市售尼龍箱也分開。[ABC／USA Today 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)、[Travelpro 公司史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)及[專利](https://patents.google.com/patent/US4995487A/en)支持這些區隔。深藍箱色、記者髮型與外套、機師外套、特定人數屬插畫設定，不能當成有來源的歷史外觀；`engine-public-sight` 的「crew」也宜明確限定為來源所說的空服員。

完整定位在 [candidate/video.json](<C:/Users/x8120/.codex/worktrees/a01-branch-sync/travel_scanㄐ/docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r43/candidate/video.json:157>)；以上尚未修改候選包。
