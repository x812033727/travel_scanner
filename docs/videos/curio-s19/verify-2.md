# S19 第二輪盲讀後窄修｜2026-10-19

第二版 `script.md` SHA-256：`89cc5a7e263f9d5e46fec26346d7fc28f5888bb1e3fbab0f60f1bc81ca193f48`。真正獨立的第二輪逐題判定保存在 [narrative-round2.json](narrative-round2.json)：13 題中 12 題通過；唯一未過的是 `no_recap`，因 `et003` 和 `et032` 都說「地基已下」，相隔數分鐘而後句未明確回呼。這份原判定原樣保留，沒有改寫為通過。

第三版窄修如下；原文版本與完整逐句引文仍見 [research.md](research.md)、[claims.md](claims.md)。

| 位置 | 固定來源 | 修正及理由 |
| --- | --- | --- |
| `et032`、`eiffel-032` | 1887《Le Rappel》`R132–143` | 旁白刪去第二次「地基已下」，留下契約已簽、鐵料已訂兩項原文事實；畫面只見鐵料訂單，不再重畫地基。 |
| `eiffel-033` | 同篇 `R141–143` | 訪談發生於 1887 年，提示詞改為室內施工進度表；不畫尚未開幕的世博遊客隊伍。進度表為卡通示意，不當成真實檔案。 |
| `et076` | 1913《L’Illustration》`I1676–1678`：「Une note du commandant Ferrié, présentée à l'Académie…」 | 改為「費里耶的一份報告被呈交科學院」，保留被動語態；原句沒有點名由費里耶本人提交。 |
| `eiffel-096` | 同篇 `I1676–1700` | 畫面改讀同一張 1913 年報紙剪報。短訊未交代巴黎市去留決議，不能以市府檔案簿暗示我們讀到了決議。 |

第三版 100 句、90 個插圖鏡頭，估 8.14 分鐘。`node tools/video/cli.mjs lint --slug curio-s19 --json` 為 **0 errors／0 warnings**。第三版 `script.md` 精確 SHA-256：`c9200f5a1029359d57a7ec6cc292593476296b777a112daaa2e614ae13215fa5`。這個 SHA 仍須重新獨立盲讀；第二輪的通過題不直接沿用。沒有製作付費媒體。
