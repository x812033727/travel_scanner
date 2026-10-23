# C16《Bialetti》新版劇本與配鏡獨立覆核

審查者：`codex-c16-v2-independent`，不是 PR #1704 的劇本作者，也不是舊版 85 句的審查裁決者。審查日期：2026-10-23。對象為草稿 [PR #1704](https://github.com/x812033727/travel_scanner/pull/1704) 的精確作者 head `a7303b2fa6feeaa374625f0b4629837b96ceb454`；本審查分支以該 head 為基底，只新增本收據及本任務票。舊版 85/85 PASS 不沿用到這份重寫的 81 句。

## 裁決

**HOLD：80/81 句來源與敘述邊界 PASS，80/81 組配鏡文字 PASS；`c160601` 一句及其配鏡需同步收窄。** 不能以此收據宣稱新版劇本／逐鏡整體 PASS，也不能開始付費、匯入、上傳或發布。待作者在原 PR 修改後，須以新四檔雜湊差異重核；兩名新版純旁白盲讀者及站主劇本核准另屬後續關卡。

| 凍結輸入（作者 head 的原始檔案 bytes） | bytes | SHA-256 |
| --- | ---: | --- |
| `script.md` | 13863 | `398029F77DAEA0AC861C34184D89F42B5233544853B76562E6F1D3FFCE0376A1` |
| `script-source-notes.md` | 8110 | `EAB56335270C22055F4450BCA95BEEB2223ABE21FA471EAA2DCDE227D89A77C0` |
| `visual-plan.md` | 14989 | `08C9592BFD9E9079C6101DC280B8CFD304C0AFA1EC91F5A067CA849397F9BF33` |
| `visual-plan.json` | 21236 | `4B76CFF72832BCA2527CB59D126DDC4512C9EDC35B5DAAE3C4D8287C7047604F` |

已直接讀新版 81 句、逐句依據、81 列 Markdown 及 81 筆 JSON 配鏡，並回讀以下一手發行者資料。81 個旁白 ID、81 個 Markdown ID、81 個 JSON ID 各自唯一且同序；Markdown 的類型、景別／字卡、提示詞／備註與 JSON **81/81 逐欄相同**。候選插圖 72 張、後製字卡 9 張、插圖提示詞 72 個互異、最長連卡 2 張；JSON 設定 `MiniMax image-01` 與唯一 `cute-mystery` preset，片頭 5 秒接 `c160108`、v4 片尾 21 秒接 `c160610`。這些是文字與數量預檢；真實配音秒數及插圖畫面時間占比仍未量測。

## 直接來源核讀

| 故事範圍 | 一手定位與本輪判斷 |
| --- | --- |
| 1919 鋁工坊、1933 後來設計標示、1950 年代廣告投入 | [Bialetti 2007 上市公開說明書](https://www.borsaitaliana.it/prospetti-informativi/926pros_1_it.pdf)印刷頁 68 §5.1.6；[Museo Omero 人物頁](https://museoomero.it/opere/autori/alfonso-bialetti/)第 9–12 行。`c160202`、`c160301`、`c160501–504`、`c160512` 分別標清公司／館方回顧，不報無憑產量。 |
| 舊式家庭壺、摩卡結構、後來持續生產與改良 | [Museo Omero〈Moka〉](https://museoomero.it/en/opere/moka/)的 Description、Original 欄。`c160205–211`、`c160306–314`、`c160401–407`、`c160603–607` 與其描述及可見器具構造相符；沒有把館藏 1956 年物件說成 1933 年原件。 |
| 1950／1951 實用新型、洗衣鍋傳說、咖啡館宣傳願望 | [ADI／義大利專利商標局參與的《Italia Geniale》圖錄](https://www.adi-design.org/upl/ADI%20MOSTRE%20CATALOGHI/Italia_Geniale_CATALOGO-CATALOGUE.pdf)印刷頁 154–157，圖錄目前可由發行者索引逐頁讀到 #34833／1950-07-05、#37736／1951-05-05、`Legend has it` 與後頁「像咖啡館」廣告語。`c160303–304` 說傳說；`c160506–507` 明定兩筆是後期登記；`c160412–415` 不把行銷句當沖煮等同。圖錄 PDF 直接開啟在本輪逾時，索引的同一官方 PDF 頁面與矩陣定位相互核對；未聲稱讀到 1933 原始專利。 |
| 壓力水路、未達常壓沸點時開始萃取、與機器義式濃縮不同 | [Navarini 等原始熱工研究全文](https://prokofe.ru/files/public/1545073690_16273_FT107421_experimental_investigation_of_steam_pressure_coffee_extraction_in_a_stove-top_coffee_maker_l.navarini_navarini2009.pdf)摘要與 §1。`c160401–415` 不填固定壓力、溫度、時間或飲品等號。 |
| 1957 年印刷廣告 | [Fondazione Fiera Milano 在 Google Arts & Culture 發布的館藏頁](https://artsandculture.google.com/asset/pubblicit%C3%A0-moka-express-bialetti/MgG9-eGz81X0-Q?hl=en)記 1957 年 4 月、《Fiera di Milano》雜誌第 16 頁及展場花壇照片；原站同件頁本輪逾時。`c160106`、`c160508–511` 的旁白與無字雜誌配鏡符合，沒有改成展場直立海報，也沒有用廣告推銷量。此館藏頁沒有記載該頁後來被放入什麼容器，見下方 HOLD。 |
| 1958 電視廣告與 Paul Campani | [Bialetti 官方歷史年表](https://bialettiafrica.com/pages/our-history)的 1958 節；[義大利文化部檔案局回顧](https://archivi.cultura.gov.it/archivio-notizie/notizia?cHash=b4df0ebe9d75773a99c305c144cf217c&tx_news_pi1%5Baction%5D=detail&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Bnews%5D=2168)可見的官方索引。`c160513–517` 只採公司年表的電視節點，不說角色在那一年才第一次畫出。 |

M16 的小鬍子角色究竟像 Alfonso 或 Renato，MoMA 與 Museo Omero 的後來說明不同；本稿只稱品牌角色及畫者，圖也不畫角色。M17 的發明、權屬、訴訟未由目前可讀原件裁定；本稿不說 Alfonso 唯一發明原理、1933 年已見原始專利，或哪一方勝訴。以上仍是來源邊界，並非把未解事實判成 PASS。

## 精確 HOLD 與修訂界線

| ID | 目前文字／畫面 | 為何停線 | 最小修法 |
| --- | --- | --- | --- |
| `c160601` | 旁白：「那頁印刷廣告**最後被收進檔案盒**」；JSON／Markdown 畫匿名手把無字雜誌頁收進檔案盒。 | [館藏頁](https://artsandculture.google.com/asset/pubblicit%C3%A0-moka-express-bialetti/MgG9-eGz81X0-Q?hl=en)能證明雜誌廣告頁及館藏記錄，沒有記載後來的容器或「被收進去」的動作。旁白與配鏡同步把編輯場景說成物件保存史。 | 旁白改為該印刷廣告「如今仍能在館藏記錄中找到」之類可證的說法；配鏡用素面雜誌頁與概念館藏目錄卡，勿演出具體入盒過程。同步更新逐句依據、兩份分鏡，保持 ID 對應。 |

## 81 句／鏡覆蓋與邊界

| 章及覆蓋 ID | 旁白來源 | 同 ID 畫面 | 核讀要點 |
| --- | :---: | :---: | --- |
| hook `c160101–c160108`（8） | 8 PASS | 8 PASS | 開場現代廚房及工坊為標明的概念場景；年份尚未揭示，最後一句為本集問句。 |
| origin `c160201–c160212`（12） | 12 PASS | 12 PASS | 1919 工坊與先存家庭壺分開；設計問題與未見試作順序不冒充當年日誌。 |
| idea `c160301–c160314`（14） | 14 PASS | 14 PASS | 1933 是後來的設計標示；洗衣鍋只呈現在故事冊與傳說卡，成品零件依館方結構。 |
| engine `c160401–c160418`（18） | 18 PASS | 18 PASS | 水路、安全閥與熱工研究相合；摩卡與機器義式濃縮不畫等號，早期產量不給確數。 |
| turn `c160501–c160519`（19） | 19 PASS | 19 PASS | 1950／1951 登記、1957 雜誌廣告及 1958 公司年表電視節點分明；無真人肖像、原廣告重製或品牌角色。 |
| now `c160601–c160610`（10） | 9 PASS，`601` HOLD | 9 PASS，`601` HOLD | `602–610` 對公司意見／館方沿革有歸屬；`608` 為質性故事結論，無身分／權屬定論。 |

舊版的兩位純旁白讀者 [#1713](https://github.com/x812033727/travel_scanner/pull/1713) 與 [#1714](https://github.com/x812033727/travel_scanner/pull/1714) 都 HOLD；新版不能借用舊盲讀。本審查不替代兩位新版純旁白讀者、站主劇本及逐鏡核准或付費整支估價。正文長度與插圖時間占比均只能在實際音軌及鏡頭排程後判定。
