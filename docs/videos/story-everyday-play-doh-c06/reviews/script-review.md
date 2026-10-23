# C06 Play-Doh｜逐句獨立來源查核

- 審核：獨立來源查核代理 `codex-gpt6-c06-source-review`，2026-10-22。
- 結論：**PASS，94／94 句**。六章逐句對照列出的來源；`video.json` 的 94 個旁白 ID 與文字和 `script.md` 完全相同。這是劇本事實關卡，並非盲讀、實際配音長度、站主劇本核准或付費製作核准。
- `script.md` SHA256：`80671FCE0CC1D03E46B68361173FB547B156C255F1AF10468E3011389E08232F`
- `video.json` SHA256：`666CD45A5E126D7F17DD95CCE1CACE213B07EAA2597340D3661D5CC3C3C4CBFA`

狀態欄更新驗證：把 `script.md` 的「逐字稿審稿版，逐句來源查核及兩位盲讀已通過；尚待站主劇本核准」唯一一處換回先前「逐字稿初稿，尚待逐句來源查核、兩位盲讀與站主劇本核准」，重算所得 SHA256 正好是前次通過的 `2C76345588E5A1F8A34D69ECA196A0491F140152515A0B8F81C5D8CF4748EE3A`；94／94 旁白 ID 與文字仍和 `video.json` 完全相同。因此本次更新不改動事實查核結論。

畫面修正複核：新 `video.json` 仍有 94 個場景、94 個旁白 ID，與 `script.md` 逐字相符。`c060413` 字卡只顯示「1955／正式推出」；`c060416` 另顯示「1956／向大辛辛那提學校推廣」。兩張卡分別對應 The Strong 的敘述，不聲稱首筆交易日期。`c060305`、`c060308` 新提示詞只以匿名教室桌面與較硬材料示意，沒有新增可識別的歷史人物、對話或精確事件主張。

上架說明草稿複核：`video.json` 的 `youtube.description` 已將 1955 年正式推出及 1956 年向學校行銷分作不同里程碑，並明說首筆成交年份未明；94 個旁白 ID／文字及上述兩張字卡未變。此為文案查核，不表示影片已上傳或發布。

最後提示詞修正驗證：把 `c060305` 的 `plain modeling tools` 還原成 `plain craft tools`，並把 `c060308` 的 `plain desk mat` 還原成 `craft mat`，整份 `video.json` 的 SHA256 恰好回到前次已通過的 `C10D53CBE2E0AA92A927D28358E636FD01BB7A070B14E8EDBE4DDB7A98FFF5E8`。新版僅此兩處匿名示意畫面措辭改變；旁白 94／94、兩張年份卡與上架說明未變，事實判定維持 PASS。

## 逐章判定

| 章 | 旁白 ID | 判定 | 核對重點 |
| --- | --- | --- | --- |
| hook | c060101–c060108 | 8／8 PASS | 清潔膏舊用途、教師轉用有回顧來源；專利確實晚於玩具化。教師路徑明確歸給 Kutol。 |
| origin | c060201–c060214 | 14／14 PASS | Kutol 1912 年起點、路易維爾至辛辛那提、Cleo 與 Kroger 合作均依公司史；1933 年、Noah 早期配方與產品撐起生意均依 The Strong 後來回顧，未冒充原合約或原配方。 |
| idea | c060301–c060316 | 16／16 PASS | The Strong 記 Cleo 1949 年過世、1950 年代初銷售衰退及煤改油／瓦斯；普通黏土偏硬依同機構玩具名人堂，教師帶入教室依 Kutol 版本。問題句與編輯歸納沒有新增精確歷史主張。 |
| engine | c060401–c060418 | 18／18 PASS | 教室、Joseph 到校及重新配方歸於相應的後來回顧。1955 年教室試用與「正式推出」、1956 年子公司向學校行銷被表述為不同里程碑，沒有推定首筆交易年份。 |
| turn | c060501–c060520 | 20／20 PASS | 教育展示、百貨業者、1957 年三色、兒童電視節目、1960 年 Fun Factory 均有來源；未把電視曝光推算成可核實的銷售歸因。 |
| now | c060601–c060618 | 18／18 PASS | 專利申請 1960-05-17、發明人及兒童用途、較早 1958 年申請、1965-01-26 核准公布由專利原文支持；The Strong 的 1964 年年出貨逾百萬罐另列為回顧數字；1965 年出售 Rainbow Crafts 而非 Kutol 全公司、Kenner 與 Hasbro 後續，以及 Hasbro 2026 年新品均按來源描述。 |

## 來源與保留界線

- [Kutol 公司沿革](https://www.kutol.com/kutols-story/)：1912 年創立、Cleo 與 Kroger、Kay Zufall 的公司版本、Rainbow Crafts 子公司與 Kutol 後續業務。
- [The Strong 2016 年 Play-Doh 歷史](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)：1933 年、1950 年代需求、1955–56 年轉用與推廣、重新配方、1957 年顏色、1960 年配件、1964 年出貨及 1965 年出售。早期敘述部分轉引後出的玩具史書，並非同時期帳簿。
- [The Strong 玩具名人堂條目](https://www.toyhalloffame.org/toys/play-doh/)：黏土偏硬、教育展示與百貨業者。它與上項屬同一機構，沒有當作第二份獨立原件。
- [美國專利 US3167440A](https://patents.google.com/patent/US3167440A/en)：1960 年申請、1965 年公布的直接文件；提及 1958 年較早申請，但不能倒推 1930 年代清潔膏配方或首售日期。
- [Hasbro 2026 年新品公告](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience)：只支持當代品牌仍有新品，不倒寫為早期商業轉折。

仍未取得 1933 年 Kroger 原合約、Kay 教室同時期紀錄、早期清潔膏原配方、首批玩具成交紀錄或 1964 年原始出貨帳。稿件保留歸屬和年份界線；若上述兩個綁定檔案有任何更動，這份 PASS 必須重審。
