# H10 獨立正式劇本史料複查（第 2 輪）

查核日：2026-10-16（Asia/Taipei）。查核員與第 1 輪不同；本輪未改劇本。

- `video.json` SHA-256：`236E94B49168E52E57F6C063C9CD377FDF2086CC91FB0907932A3D13FC3389AC`。
- 先從本版 `video.json` 抽取 80 句 `text`／`say`、78 筆 `scenes[].data`、縮圖與 YouTube 上架資料至工作目錄 `_tools/fact-round2/extracted.json`。本稿沒有 `say` 覆寫。
- 第 1 輪有 78 句 `CONFIRMED`、2 句純編輯。使用固定亂數種子 `20261016` 從 78 句抽出 26 句（正好三分之一）；抽樣列號與全文保存在工作目錄 `_tools/fact-round2/sample2.json`。抽樣巧合包含本次兩句修訂；兩句仍另作必查。
- 與第 1 輪劇本版本的 Git 差異只有 `h3369d03`、`hc2e7f24` 兩句文字及同一 loop 的回收 ID／描述；78 張畫面 `data`、縮圖、標題、說明、標籤沒有改字。下表覆核全部受影響的事實與抽樣句，不把舊版 `verify-1.md` 當作新版通過憑據。

## 本輪來源與存取

用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 直接取得下列原始頁面，依同站至少間隔 1 秒；六頁及新發現頁均為 HTTP 200，正文已讀。網站更新日期與**本輪開啟日期**分開記錄。

| ID | 原始頁面 | 網站標示日期／本輪 HTTP |
| --- | --- | --- |
| S01 | [Parks Canada：Franklin's 1845 expedition](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/histoire-history/expedition) | 網站 2022-12-21；本輪 200 |
| S02 | [Canadian Museum of History：A very special piece of paper](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) | 2018 展覽文章；本輪 200，含紙條逐字轉錄 |
| S03 | [Parks Canada：Inuit traditional knowledge](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) | 網站 2024-06-27；本輪 200 |
| S04 | [Parks Canada：Finding HMS Erebus](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus) | 網站 2023-03-22；本輪 200 |
| S05 | [Parks Canada：Finding HMS Terror](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror) | 網站 2023-03-22；本輪 200 |
| S07 | [University of Waterloo：Fitzjames identified](https://uwaterloo.ca/news/media/another-franklin-expedition-crew-member-has-been-identified) | 2024 發布；本輪 200 |
| NEW26 | [University of Waterloo：four more sailors identified](https://uwaterloo.ca/news/media/dna-matches-identify-four-more-sailors-franklin-expedition) | **2026-05-06** 發布；本輪 200。見下方新鮮度阻斷。 |

## 第 2 輪主張表

`#` 對應第 1 輪逐句表，`where` 是本版 ID；來源欄的連結即本輪直接取得的 URL。問句的提問形式屬編輯，表中 `CONFIRMED` 指其中可查證的前提。未修改的列在 before → after 欄以「同句」標示。

| # | claim（本版完整朗讀文字） | where | URL／HTTP | verdict | before → after |
| ---: | --- | --- | --- | --- | --- |
| 1 | 一八四五年五月，英國格林海斯。兩艘船從碼頭出發，準備尋找穿過北極的航道。 | `h28b2255` | [S01](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/histoire-history/expedition) 200 | CONFIRMED | 同句 |
| 8 | 當初啟航時，兩船原本共有一百三十四人。返航者離開後，船上就是開場那支隊伍。 | `h3e67f13` | [S01](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/histoire-history/expedition) 200 | CONFIRMED | 同句 |
| 9 | 富蘭克林帶著留下的人，駕幽冥號和恐怖號繼續往西，想把西北航道走通。 | `h69b3e42` | [S01](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/histoire-history/expedition) 200 | CONFIRMED | 同句 |
| 14 | 他們用海軍的制式表單，記下位置和經過的地方，還留下什麼狀況？ | `h7e65daf` | [S02](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) 200 | CONFIRMED | 同句 |
| 19 | 等到同一張紙再出現新的字跡，兩艘船的任務，還能繼續嗎？ | `h049dfec` | [S02](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) 200 | CONFIRMED | 同句 |
| 23 | 而富蘭克林，早在前一年六月十一日就去世了。 | `h1d74698` | [S02](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) 200 | CONFIRMED | 同句 |
| 24 | 紙邊還記下，已經失去九名軍官，以及十五名船員。 | `h882c0b9` | [S02](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) 200 | CONFIRMED | 同句 |
| 28 | 除了這張紙，因紐特人的見聞裡，還留下了什麼？ | `h7ca6f6b` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句 |
| 31 | 他們還告訴雷，在更南邊的巴克河口附近，發現過死者。 | `hf9694ad` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句 |
| 32 | 這些消息讓棄船後的搜索有了方向，可是口述之外，還需要更多能對上的東西。 | `h771e616` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句；後半為證據界線 |
| 37 | 他叫伊努克普吉朱克。他把沉船的位置指給哈爾看，還另畫了一張圖。 | `h3a137ee` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句 |
| 39 | 這個過程也靠因紐特翻譯者協助。話能被聽懂，地點才能被記下。 | `h7290bc7` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句 |
| 40 | 當時畫的圖，還無法直接變成今天的海底座標，卻保留了往哪裡追問的依據。 | `hef75ce9` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句；不冒充現代 GPS 點位 |
| 41 | 後來有人把這些紀錄重新整理，逐段對照：哪一艘船，出現在哪一片海域。 | `h673bff9` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句；S03 記錄 Woodman 1992 整理 |
| 44 | 因紐特見聞先畫出搜尋範圍。後來是哪條現場線索，讓水下搜尋改了位置？ | `h3369d03` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200；[S04](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus) 200 | CONFIRMED | 「一句沉船的描述，怎麼變成下一次海底搜尋的位置？」→現句；S03 說口述界定範圍，S04 說 2014 岸上物件使搜尋改位 |
| 45 | 搜索隊不只往水下看，也留意岸上有沒有遠征留下的物件。 | `hc2e7f24` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200；[S04](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus) 200 | CONFIRMED | 「於是搜索不只往水下看，岸上有沒有遠征留下的物件，也成了重要問題。」→現句；移除無據的必然因果 |
| 46 | 海底的調查，則要讓聲納一次次掃過搜尋區，再檢查值得追的形狀。 | `h8be50df` | [S04](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus) 200 | CONFIRMED | 同句 |
| 50 | 它的樣子，有點像腳踏車的前叉。但它出現的地方，是北極岸邊。 | `hc9c15f2` | [S04](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus) 200 | CONFIRMED | 同句 |
| 55 | 可是，只看到船的形狀，還不能立刻說出它的名字。兩艘船都在找。 | `h3153937` | [S04](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus) 200 | CONFIRMED | 同句；聲納可見沉船，Erebus 身分另經影像與船圖比對 |
| 59 | 它所在的區域，也接上了那些被保存下來的因紐特見聞。 | `h3b4187b` | [S03](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit) 200 | CONFIRMED | 同句；S03 說沉船在 Inukpujijuk 指示地點附近 |
| 60 | 但海圖上還缺一艘。恐怖號會在附近，還是藏在另一片水裡？ | `h9ce4071` | [S05](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror) 200 | CONFIRMED | 同句；2014 後 Terror 尚待尋找 |
| 68 | 搜索隊還得拿水下看到的部件，去對照留存的船圖。 | `h83aa802` | [S05](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror) 200 | CONFIRMED | 同句 |
| 70 | 他們檢查雙舵輪、船首包覆的鐵，並和原有船圖比對。 | `h540a29e` | [S05](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror) 200 | CONFIRMED | 同句 |
| 73 | 棄船紙條寫過南行的計畫，沉船留下的是最後位置，中間還隔著沒寫完的一段。 | `h4cb7289` | [S02](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) 200；[S05](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror) 200 | CONFIRMED | 同句；不把計畫當成全程已知 |
| 74 | 還記得補記邊緣的菲茨詹姆斯嗎？船能靠構造認出，他也在等待能辨認本人的證據。 | `h93c7c04` | [S02](https://www.historymuseum.ca/blog/a-very-special-piece-of-paper/) 200；[S07](https://uwaterloo.ca/news/media/another-franklin-expedition-crew-member-has-been-identified) 200 | CONFIRMED | 同句；時序上在 2024 鑑定以前 |
| 76 | 再結合家譜，他們確認這份遺骸屬於菲茨詹姆斯。紙上那個簽名，終於對上了人。 | `hf310a51` | [S07](https://uwaterloo.ca/news/media/another-franklin-expedition-crew-member-has-been-identified) 200 | CONFIRMED | 同句 |

## 新發現、範圍與判決

- **抽樣事實：**26／26 支持（其中修訂句 2／2）；`CHANGED` 0、`NOT FOUND` 0。`scenes[43].data`、`scenes[44].data` 只是無標籤海岸圖與岸上掃視的卡通示意，沒有暗示口述直接給出精確座標；其他畫面、標題、說明與縮圖未隨本輪兩句改動。站主觀點沒有不符。
- **新鮮度 HOLD：**[Waterloo 2026-05-06 原始發布](https://uwaterloo.ca/news/media/dna-matches-identify-four-more-sailors-franklin-expedition)確認**又辨認四名船員、累計六名**，包括 Terror 的 Harry Peglar。當前片尾以 2024 Fitzjames 作「最後的新資訊」，`youtube.description` 宣稱「資料查核：2026-10-16」卻只介紹 2024 身分研究。現有台詞沒有說 Fitzjames 是唯一或最新獲辨認的人，所以它們並非直接錯誤；但本集對近況的覆蓋不足，需由主代理決定是否更新已核准大綱／正式稿，或明確限定本集只追紙條簽名者。在這個編輯決定前，**不建議把整支劇本標為已完成史料關卡並送站主劇本核准**。本查核員未替作者改動劇情。
- **建議的最小更新界線：**保留船與紙條主線及 Fitzjames 作為「紙條簽署者獲辨認」的回收；在 `hf310a51` 之後、結尾的未知行程界線之前，補一個很短的 2026 年五月身份研究後記，明說「再辨認四人、累計六人」而不推論四人的死因或完整航線。同步新增 NEW26 至 `research.md`／`claims.md`／逐句來源與 `youtube.description`，卡片只用無肖像的姓名或數字示意。若此舉改動已核准 `brief.md`，須重新走雜湊綁定的大綱核准；任何正式稿改字也須重新跑獨立史實與敘事盲評。這是更新範圍建議，不是本輪自行改稿。
- **聽眾檢查：**80 句均未超過 40 個字元；正式朗讀無拉丁字母、括號、網址及「經查證／根據官方文件／本影片」式自述。Inukpujijuk 中文人名仍須旁白試聽；本輪兩句的「範圍」與「改位」可口語理解，未提前說出岸上物件答案。純敘事的回收是否成立由另一位盲評者裁決。
- **機械檢查：**`node tools/video/cli.mjs lint --slug curio-h10 --json`：0 errors、原有 2 warnings（`historical` 32／72 張、`modern` 30／72 張提示詞），80 句、估時 9.615 分。警告屬鏡頭差異，非本輪事實改動。
- **需重跑第 2 輪的事實改動門檻：**本輪事實修改 0，未觸發「多於三處需下一輪」；但新鮮度 HOLD 仍須先解決，並對任何後續改字綁定新 SHA 重查。
