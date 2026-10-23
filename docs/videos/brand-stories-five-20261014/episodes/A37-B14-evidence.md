# A37／B14 新系列 episode row 草稿收據

建立日期：2026-10-15。這兩份 JSON 是 `brand-stories-curio-five` 的**單列草稿**；目前已有各自綁定新 hash 的獨立審稿，五列亦已在本機編成含 `series` 的 `stories.json`，尚未匯入主機或製作影片。A01／B18 試作與站主驗收仍排在五集之前。

| 題目 | 母題庫 `story_sha256`／原審稿綁定值 | 母故事檔 SHA-256 | 母審稿檔 SHA-256 | 新單列檔 SHA-256 | 新故事內容 hash（已綁新審稿） |
| --- | --- | --- | --- | --- | --- |
| A37 | `11ee451c1ea68170ee90a71321b854bbf6286330faf4a62b3db2a8cfcdbffbde` | `e673720fd4c4c88139e600aba40600007f94f289fdc797639e5472b8d4ecdd10` | `eb743e579a1bbc00920d4423ff7153e53bfdfc43abcc6b5c4af3a4dbdb0c75c4` | `73e68dac337cd0afa5c558b3a3cf59f6e3afebe1cd234dd3663fe8deaa553177` | `5de6cdd40023bd20b1d67ad4fc5f033bf7825828bbddc12ee2ac6ee47cf1160f` |
| B14 | `a1b9369a312f6b00367680586bc4d34f383a827e967123939091e023c4351133` | `3bd93e937fbd03c6afcc2ee460b507e87367f64137a4cb58eba506c68a09f8c6` | `3df84dbe985cf1c9a3f59776fa4ef9301cc22b03fad6cbea788d2850f451f3bc` | `b0b1a5697bafd0e54f70980f46f98e943b7ec51682c8f62492a39754281d4818` | `1fd6c2317579ebcefb5b65a22f16a9c256e3110046825c7d4a9647f8a63edaa0` |

母檔：[A37 故事](../../story-plans/brand-stories-100/stories/A37.json)／[審稿](../../story-plans/brand-stories-100/reviews/A37.json)、[B14 故事](../../story-plans/brand-stories-100/stories/B14.json)／[審稿](../../story-plans/brand-stories-100/reviews/B14.json)。兩列由當前母題庫編譯檔 `stories.json` 抽出，該檔 SHA-256 為 `c8fb18102634459c62f556022139e0bdc733ef432321c412ff810faed0ac0194`。

## 本次草稿更動

- A37：原第 47 集改為新系列第 3 集，`publish` 暫排第 3 天 `12:00`，slug 改成 `story-five-adidas-puma-brothers`。標題、logline 與問題改成可由紀錄回答的「如何分家、如何影響小鎮」；六個 `point` 改為 1924 登記冷開場 → 登記後賽場發展與 1928 奧運 → 1948 RUDA 與拆夥 → 1948–49 兩公司登記 → 1954 賽場與鎮民選邊 → 2009 和平日球賽。私人爭執原因仍不作定論。原 `must_verify[1]` 的 Owens 確定穿鞋說已改為 Adidas 官方證據未定的界線；`must_verify[3]`、`[8]` 改以 PUMA／Adidas 官方年表與 PUMA 2009 原始新聞稿核時序，新增四筆官方來源並更新 `caveats`。
- B14：原第 8 集改為新系列第 4 集，`publish` 暫排第 4 天 `12:00`，slug 改成 `story-five-ajinomoto-chip-film`。標題與 logline 配合片長與主問題；六個 `point` 改為 1907 昆布場景冷開場 → 1908–09 鮮味商品化 → 1969 安全疑問及與其無已證因果的材料支線 → 舊液態絕緣工序 → 1999 ABF 與 2026 特定市場公司說法 → 材料與調配能力回扣。第三章現將 FDA 的現行 GRAS 判斷與 1990 年代 FASEB 審查分句敘述，不替 GRAS 指定年份。
- 兩列的 `names`、`cast`、`image_notes`、`sensitivity`、`related_guide`、`thumbnail` 沿用母編譯列；B14 的 `must_verify`、`sources` 與 `caveats` 也沿用母列。沒有改母 100 題、原排程或原審稿。用 `storyProblems` 檢查兩份新故事欄位均為零錯誤。這是機械結構檢查，**不是新 row 的獨立事實審核**。

## 審稿結論與匯入前門檻

1. 母審稿 SHA 只綁母故事，不能覆用。新標題、logline、問題與章點已由另一位審稿者逐章核對 treatment、母來源、`must_verify` 與 `caveats`；[A37 review](reviews/A37.json) 和 [B14 review](reviews/B14.json) 已分別綁上表新 hash。`build.mjs` 本機編譯五列通過，但這不代表主機匯入或影片已製作。
2. A37 新 row 已把 `must_verify[1]` 改成 Adidas 官方的證據未定說法；PUMA 官方年表與 2009 年新聞稿仍較肯定地聲稱 Owens 穿兄弟鞋。獨立審稿須核這項**官方來源彼此不一致**的界線，不可在旁白把較肯定版本當確證；墓園、鎮民看鞋仍是媒體記述。2009 年官方新聞稿只證實兩家公司公開合作，不能說已故兄弟本人和好。
3. B14 `must_verify[7]` 的「1980 年起 FDA 等機構認可」是味之素社史的說法，FDA 官方頁面沒有提供 1980 年；約 95% 也是 2026 年公司受訪者對特定封裝市場的說法。獨立審稿須確保這些歸屬進入旁白，不得泛化為所有晶片或把食品安全爭議寫成研發 ABF 的原因。
4. 本工作樹的故事計畫與 API 匯入驗證已有約 10 分鐘、MiniMax `image-01`／`cute-mystery` 路徑；本機 `build.mjs` 已驗五列連號及單列結構，`uv run pytest tests/test_video_story_import.py tests/test_video_story_series.py -q` 為 9 passed。仍須在主機做 `video-story-import` **dry-run** 並核 live slug、ID 與在製狀態。此收據不代表可直接 apply 或啟動工人。
