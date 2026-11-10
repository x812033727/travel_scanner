# S59 R7｜獨立史料、逐句引註與書面畫面覆核

2026-10-21 UTC。**本輪來源與書面畫面 PASS；只適用於下列五檔。**我不是 R7 作者；重新取回固定原文，逐一讀了 110 句口播、逐句引註及 110 景的書面畫面，沒有依作者的 PASS 判斷，也沒有修改創作檔、生成圖片或購買媒體。本收據不代替隔離敘事盲讀、實際生成圖片驗收或站台關卡。

| 凍結檔 | 自行實測 SHA-256 |
| --- | --- |
| `research.md` | `39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d` |
| `brief.md` | `9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3` |
| `claims.md` | `73711de13ce73791e409118b923eceb9d35425a84a63b6fc8b20ddba816e1c58` |
| `video.json` | `c78a0329f901d05450440ac7244345e5a375ebbacf361c187cec1036bfcc767e` |
| `script.md` | `d024ba3a7fed6c94b90320097de6289273278b65c7e1ebaef727b86ec861e57f` |

## 方法與來源層級

重新下載 [D：杜蒙塞爾 1878 法文原版固定轉錄](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt)、[E：1910 傳記中愛迪生本人回憶](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt)、只輔助術語的 [T：杜蒙塞爾 1892 英譯](https://github.com/GITenberg/The-telephone-the-microphone-the-phonograph_75683/blob/6b0cda8809aa60bf44270a64853c9aaf9ea5c546/75683-0.txt)。三份原始檔的 SHA-256 分別為 `c48361e94523ebacc000172ebab34895bb20c0b7e458ac3e122f90a3cc9e717c`、`9818547c6dd15e488c1923bad5cc09cb4fa3f447641daaaf77b2f539b4d49d34`、`cb9e9fbeee72750d6335413a9f91a450c09b9a40377fbc1c42c7822a79c598c9`，與研究表固定值一致。以原檔行號核 E93–107、5195–5241、5262–5273，D6680–6694、6872–7049，並把 16 條 P 主張、每句口播與每景提示詞對回原文。

D 親歷呈交及自己後來的失敗檢討；腹語對話及秘書室重試的詳細敘述在他**所引匿名現場來信**中，不是官方逐字紀錄。E 第十章明示引用愛迪生，卻是三十多年後的自述，不能見證巴黎。T 是同一作者後出的譯本，沒有當作第二名證人。本版口播與說明欄維持這些層級，也沒有把童謠稱為現存原音或全球第一段錄音。

`video.json` 有唯一、連續的 `s59001–s59110`；`claims.md` 的 110 行與口播 **110／110 逐字一致**。逐句表 124 個 D／E 連結實例均指向固定 commit，P 代號及錨點與 `research.md` 的定義一致；P12 是來源身分註，沒有獨立口播行。用 `tools/video/core/screenplay.mjs` 的 `screenplay()` 對 JSON 重生文字，與 `script.md` **位元組相同**。書面分鏡為 100 個 `shot`、10 個工具排版 `big`；110 景的提示詞或卡片資料及縮圖文字均已讀。`node tools/video/cli.mjs lint --slug curio-s59 --json` 得 0 error、0 warning；lint 只作形式檢查，不能代替此處的史料判斷。

## 具名疑點與全表核對

- **紙盤與承盤，`s59013／17／27`：PASS。** [E5195–5205](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5205) 把螺旋槽明確放在旋轉承盤 *platen*；圓紙盤覆其上，電磁鐵的壓針在紙盤留下點劃凸痕，另一機的接點可讀回電報訊號。`s59013` 口播現在分清兩層，prompt 只要求在承盤上的紙盤壓點劃；`s59017` 只畫紙盤凸痕，不再寫紙盤刻槽。`s59027` 寫「沿螺旋路徑的小型凸痕」與懸停接點，沒有說紙盤自身有槽，也沒有把接點畫成已證實的人聲回放。這是愛迪生回憶中電報概念的插畫，並非巴黎器械。
- **彈簧／橡膠，P06 與 `s59040–41`：PASS。** [D6876–6886](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6876-L6886) 說針不直接固定於振動薄片，而由彈簧支承；兩者間的橡膠墊傳震且不把振動悶住，另有緩衝墊。研究 P06 已寫明前兩個關鍵中介；`s59040` 先說彈簧及非直接固定，`s59041` 用「薄片→橡膠→針」回答。後面的簡化傳動箭頭是因果方向，連同這兩句閱讀不會誤成直接鎖合。
- **回放性質與巴黎，`s59059–64`：PASS。** [D6955–6976](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6955-L6976) 分別記載錫箔多次播放後聲音變弱變糊、轉速使音高改變而腔調仍可辨、手搖唱歌常走調，以及另一種規律鐘錶機構重播二重唱令人較滿意。`s59059–64` 逐項放在機械性質的比較段；`s59064` 明說鐘錶機構是「另記」，卡片是「手搖／規律驅動」。[D6872–6875](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6872-L6875) 描述手搖模型，來信於 [D7008–7020](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L7008-L7020) 寫普斯卡斯轉動器械及後續指定條件重試；本版沒有斷言巴黎當天用了鐘錶機構，或把杜蒙塞爾失敗歸因於轉速、箔磨損。
- **腹語來信回呼，`s59098`：PASS。** [D6999–7016](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6999-L7016) 的匿名來信明說少數人盯著普斯卡斯的嘴，換杜蒙塞爾親試卻先失敗；[D7035–7049](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L7035-L7049) 是他本人說後來貼近話筒、練習後成功。`s59098` 點名那封信，將換人操作帶回原疑點；`s59099` 才講後來成功，沒有把第一次失敗倒說成成功。

其餘逐句組合亦對得上固定原文：D 的先有記痕、留聲機再發聲之別（P13），錫箔圓筒錄放與角筒（P06–07），倒讀及電話隔開聽者作為**書中另述**的性質／驗法（P15–16），科學院重試與本人距離問題（P01–05、P14）；E 的電報紙盤、紙人玩具、十八美元草圖、克呂西初機及紐約編輯室（P09–11）。全部 110 句沒有查到超出這些來源限制的確定式主張。100 張插圖提示詞是原創示意：未要求可讀原信、原錄音、真實會議照或精密剖面；書面內容沒有與旁白或固定來源相反的關鍵道具／事件。縮圖的「腹語？」保留疑問形式。

**結論：R7 固定五檔的來源、110 句引註及書面畫面 PASS，無本輪阻擋項。** 這只證成可進入後續敘事與製作關卡；圖片生成結果、旁白聲音及實際成片尚未覆核，也沒有付費媒體呼叫。
