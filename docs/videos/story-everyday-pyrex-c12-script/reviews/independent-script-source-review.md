# C12 Pyrex｜獨立逐句來源查核與逐鏡預檢

審查日：2026-10-22。範圍是草稿 PR #1692 的 80 句旁白與同序 80 鏡 Markdown 方向；查核者未參與本稿撰寫，也未修改作者的 `script.md` 或 `visual-plan.md`。本收據不是盲讀、念法審定、畫面成品驗收、配音時長實測或站主核准。

## 鎖定輸入與結論

| 輸入 | SHA-256 |
| --- | --- |
| 已採用 Treatment `docs/videos/story-everyday-pyrex-c12/treatment.md` | `0D5EFFA2C80E975057D0EE1F325C8798442CAC940BEA0DC7B67F556FD0AD3EA8` |
| 來源矩陣 `docs/videos/story-everyday-pyrex-c12/source-matrix.md` | `A89FC1AC61DBC4BA60E59F0E2AF751AC54FCC958F6E3E639B012E94F393A63A7` |
| 本次旁白 `docs/videos/story-everyday-pyrex-c12-script/script.md` | `B5A9BC757481651225639330CEAEB20D155B463AD5E2E621BE36536FED274A9A` |
| 本次逐鏡 `docs/videos/story-everyday-pyrex-c12-script/visual-plan.md` | `1CA9F4BA2E0C46A031D1781F02D65FFB6C0A2722B800FC8A3F5F90F7C328C4DF` |

**總判定：HOLD。** 80/80 句與 80/80 鏡均已逐項核對；旁白來源界線 78 PASS、2 HOLD（H04、T03），另有 I07 一處需要措辭限縮。視覺方向 79 PASS、1 HOLD（O12）。多句查核或剪輯工作語直接進了旁白，須在兩位真正盲讀前修順。修訂後重算兩份 SHA；本收據不自動轉為新版 PASS。

## 本次直接核對的原始來源

| 代號 | 原始頁及可核事實 | 證據界線 |
| --- | --- | --- |
| S1 | [Corning Museum of Glass／Rakow Library, *The Beginning of Pyrex*](https://blog.cmog.org/2015/beginning-pyrex)，第 17–35 行：Nonex 鐵路燈用途、尋找市場、兩個切下的電池罐底、海綿蛋糕試烤、幾年後調方與專利、家政推廣、五金店至百貨。 | 2015 年館方回顧，非 Bessie 當年日記或可精確定日的實驗簿。原文說鐵路燈剛成功，公司就尋找新市場；未給出鐵路成功與 Bessie 試烤之間的確切年距。 |
| S2 | [Corning Museum of Glass, 2014 exhibition release](https://press.cmog.org/2014/presents-exhibition-transformative-impact-pyrex-american)，第 90–100 行：1915 年首批十二件及品類，Rorer、Maddocks 百貨示範，1929 年 Maltby、1931 年公司測試廚房，後續新配方。 | 說「only a few years later」探索家用品，沒有逐日串連 Bessie 的那次試烤。 |
| S3 | [Corning Museum of Glass, Pyrex FAQ](https://pyrex.cmog.org/faq)：搜尋索引於本次顯示原站問答全文，明列 1915 年硼矽玻璃、美國消費烤器數十年來採熱強化鈉鈣玻璃。 | 本次直接開頁超時；命令列遭 Cloudflare challenge。故以原站搜尋索引內容核對，並用可直接開啟的 S2、S6 交叉核對，不稱已直接讀到活頁。正式錄製前宜再讀可訪問的當期原頁。 |
| S4 | [歐洲 Pyrex 品牌 history](https://www.pyrex.eu/en-eu/pages/history)，第 261–268 行：品牌回顧說雨曾令鐵路訊號燈外罩碎裂。 | 品牌回顧有宣傳語與自身 1915／1916 年節點不一致；「雨」只能歸給品牌，不能裝成館方或事故當期紀錄。 |
| S5 | [Corning, *PYREX FAQ* PDF](https://www.corning.com/catalog/cls/documents/faqs/CLS-AN-821.pdf)，第 0–5、11–26、37–39 行：現行 Corning 實驗室 PYREX 是硼矽玻璃，1998 年停止製造 cookware；實驗器具各型態操作界線不同。 | 不把實驗室溫度或熱衝擊參數套用廚房烤盤。 |
| S6 | [Corning Museum research answer, 2025-08-06](https://libanswers.cmog.org/faq/398431)，第 7–20 行：大／小寫非材料驗證、不同工廠和配方、現今美國消費餐具主要為強化鈉鈣玻璃、法國授權品仍有硼矽玻璃。 | 來源自己提醒口述史與例外；不得推成單一年份全線轉換或每件舊品鑑定。 |
| S7 | [歐洲 Pyrex 現售橢圓玻璃烤器商品頁](https://www.pyrex.eu/en/products/irresistible-plat-a-four-ovale-en-verre-prise-en-main-facile)，第 294–299 行：該件商品標 Made in France／borosilicate glass。 | 單件商品標示，只能證明該頁對該件的聲稱；頁面其他溫度欄位互有出入，本稿不採。 |

以上並非七個彼此獨立的歷史目擊者：S1、S2、S3、S6 同屬博物館，S4、S7 同屬歐洲品牌，S5 是現行實驗用品。歷史句應說「館方回顧／品牌回顧」；現行材質句應按商品類別、地區與頁面限制。

## 逐句來源判定

`P` 表示本句的事實或明示為推論的基礎在上述來源可核，`H` 表示應改字再核。為讓 80 句均有可追位置，下表逐 ID 列出，不以 Treatment 舊版 PASS 替代本次審核。

| 章 | 逐句結果 | 主要來源與界線 |
| --- | --- | --- |
| Hook | H01 P、H02 P、H03 P、**H04 H**、H05 P、H06 P | S1–S4、S6；H02 的雨已歸品牌，H03 只說風險，H05 疑問不保證不碎。H04 的年距待改。 |
| Origin | O01 P、O02 P、O03 P、O04 P、O05 P、O06 P、O07 P、O08 P、O09 P、O10 P、O11 P、O12 P | S1、S2；O02／O04／O08–O10 為物理或市場敘事推論，沒有編造特定事故、訪談或銷量。O12 的陶皿原文是 shattered after two uses。 |
| Idea | I01 P、I02 P、I03 P、I04 P、I05 P、I06 P、I07 P*、I08 P、I09 P、I10 P、I11 P、I12 P、I13 P、I14 P | S1、S2；I02 正確保留**兩個 Nonex 電池罐底**，I04 只選其一烤海綿蛋糕；I10 的 lamp chimney top 不是鐵路燈罩。I07 僅以緊接 I06 的「博物館回顧說」作限縮，見下方措辭提醒。 |
| Engine | E01 P、E02 P、E03 P、E04 P、E05 P、E06 P、E07 P、E08 P、E09 P、E10 P、E11 P、E12 P、E13 P、E14 P、E15 P、E16 P | S1、S2；E05 的 1915／十二件與 E06 品類可核；E07 將試用罐底和正式產品分開；E10、E11、E15、E16 為有標示的推論，未當成買家調查。 |
| Turn | T01 P、T02 P、**T03 H**、T04 P、T05 P、T06 P、T07 P、T08 P、T09 P、T10 P、T11 P、T12 P、T13 P、T14 P、T15 P、T16 P | S1、S2、S3、S5–S7；T02、T08、T09 人名與年份符合 S2；T13 只說後來另有配方。T03 的引號像無證據的廣告原文。 |
| Now | N01 P、N02 P、N03 P*、N04 P、N05 P、N06 P、N07 P、N08 P、N09 P、N10 P、N11 P、N12 P、N13 P、N14 P、N15 P、N16 P | S1–S7；N01–N04 分清 1915 年和現今美國且不硬定轉換年，N06／N07 限單件法國現貨，N08／N09 分開實驗用品，N11 否定大小寫驗材。N03 的 S3 活頁讀取限制見上。N15–N16 是互動文案。 |

### 必修來源與措辭

1. **H04 年距 H。** 「可是多年後」把鐵路燈成功到 Bessie 試烤的時間說得比可直接確定的更長。S1 說剛在鐵路燈用途成功便找市場，S2 只說幾年後探索家用品；兩頁均未定 Bessie 那天的年距。改為「後來，同一條玻璃研發路線……」即可保留鉤子，不推日期。
2. **T03 擬似引文 H。** 「廣告上『耐熱』兩個字」會讓觀眾以為某則當年廣告逐字印了這兩字。S1 確認廣告存在，另提早期廣告有英文 *fire-glass*；S2 確認百貨示範，沒有這句中文廣告文案。改為「觀眾在現場看到的，不只是廣告說它能進烤箱……」或其他不帶引號的意譯。
3. **I07 措辭 P*。** S1 說 Bessie 仔細記錄後續結果，並回顧第一次蛋糕比常見金屬或陶皿快；本次未見她當年的原始記錄。「這是一次家廚紀錄」可能被聽成原件證據。宜改「這只限館方回述的那次家中試烤，不能當成每件商品的烹調時間表」，並保留 I06 的來源提示。

### 口述節奏與工序語

來源成立不等於旁白自然。O07「不是後人替它補上的單一創業神話」、I03「故事不是把車站上的燈拆下來」、I13「那是形容，不是 1931 年公司的正式設施」、E02「沒有給我們一條逐日生產紀錄」、E03「不能……剪成……」是在向觀眾念查核或剪輯約束。可用正面事件關係取代：公司在找市場；Jesse 帶回的是電池罐底；後來才成立公司測試廚房；科學家隔了幾年再調方。E09–E13 反覆問家戶是否信任，也可能拉長而沒有新事實。由作者改寫後交兩位只看旁白的盲讀者確認鉤子、主線與台灣口語；本審查不是盲讀結論。

Pyrex 英文讀音在 [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/pyrex) 搜尋索引為 /ˈpaɪ.reks/；「派瑞克斯」是台灣口播提案，尚非本次聽過的錄音。Nonex「諾奈克斯」未找到可靠原廠語音，本次不簽念法 PASS。Bessie、Jesse、Rorer、Maddocks、Maltby 的英名首次出現須在配音前另作念法審核；實際 TTS 亦未生成或聽審。

## 逐鏡與成片門檻預檢

80 鏡按 H01–N16 一對一、同序。67 鏡 `I` 原創插圖、13 鏡 `C` 後製字卡；最長連續字卡是 E05–E06、T08–T09 兩張。逐項查 67 則英文插圖提示詞：未包含 Pyrex、Nonex、Corning、Littleton 或其他具名人物、logo、可讀商標／年份或重畫廣告的要求。人物匿名；雨、碎罩、家廚與百貨均作概念插畫，沒有宣稱原件照片或具體事故重建。`visual-plan.md` 尚無機器可執行 JSON，也沒有生成圖或定秒數。

| 鏡頭 | 判定與動作 |
| --- | --- |
| H01–H06、O01–O11 | P；H02 雨只沿 S4 品牌回顧，不畫可考事故。 |
| **O12** | **H：** 提示詞 `chipped ... ceramic casserole dish` 和 S1 的 `shattered in the oven, after only two uses` 不一致，而且旁白說裂、畫面僅缺角會削弱觸發點。改為匿名、無花紋的**破裂陶皿碎片示意**，仍不模仿 Bessie 的原物或確切事發構圖。 |
| I01–I14、E01–E16、T01–T16、N01–N16 | P；I02 正確顯示兩個獨立罐底，I03 把罐底與燈罩分開，E05–E06 的年與品類只在後製卡，T02／T08 人名只在後製卡，N01／N03／N06／N08／N11 材料與品牌邊界只在後製卡。 |

N14 插圖讓人物「閱讀完全空白的商品說明」會顯得不自然；可改成拿起無字器皿與摺起的空白說明紙，真正的「看商品標示／使用說明」由後製字幕呈現。這是畫面工藝建議，不是來源 H。

67/80＝83.75% 是**鏡數比**，不能稱成片插圖時間比。若 67 張各至少 5 秒、13 張純卡各最多 8 秒，規劃下界是 `335/(335+104)=76.3%`；實際仍須用配音及剪輯時間碼重算，確保插圖可見時間 ≥70%，含片頭片尾與卡片的算法依系列規則。H06 後的 5 秒片頭與 N16 後的 21 秒 v4 片尾已列出，但目前沒有實物可驗。正文 480 秒、30–45 秒鉤子間距、圖片品質、無聲／錯字、配樂、兩位盲讀、價格與站主劇本關卡均待後續獨立收據；不能用字數或本鏡數通過。

**下一步：** 作者僅修 H04、T03、I07、O12 與口述工序語，保持可核主線；新 SHA 重新逐句覆核。未經站主核准稿件和整支付費額度，不進入付費配音、插圖或影片製作。
