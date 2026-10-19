# S24 R3 獨立盲讀、來源與畫面覆核｜2026-10-19

## 凍結劇本與盲讀

- 凍結的 [`script.md`](script.md) SHA-256：`232d24e94abccafa1501a3924f86bd3f4bacacab745a75e27c489637119dd185`。本輪覆核未修改劇本或 `video.json`。
- 讀者先讀奇聞檔案局 skill、凍結劇本、`video.json` 的當前旁白及現行 13 題敘事評審題目，然後把逐題原始答案封存為 [`blind-r3-answers.json`](blind-r3-answers.json)，SHA-256：`f081ba7795064603f266c2079a5706133aff5f39678521159f760cf5fbbac96e`。封存前沒有讀 `claims.md`、`research.md`、舊版 `verify-*.md`、舊評審內容或任務票；先前的檔案列表僅露出一個舊評審檔名。
- 13 題均答「是」。執行 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s24 --answers /tmp/curio-s24-r3-blind-answers.json`，工具回報通過；收據另存 [`narrative-r3-verdict.json`](narrative-r3-verdict.json)，SHA-256：`c56a53674444304274c5f9695765ee3d6b1a94c59c92109dbcb1fd80bafc6dd2`。收據 `passed: true`，`failed: []`，`advisory: []`；13 題全部為 `yes: true`。

## 固定來源重新核對

讀者獨立下載三個固定 commit 的原文，重新核對檔案 SHA-256 並逐行讀取所引段落：

| 來源 | 固定段落 | 下載檔 SHA-256 |
| --- | --- | --- |
| 維特魯威《建築十書》英譯 | [E8011–8054](https://github.com/GITenberg/The-Ten-Books-on-Architecture_20239/blob/67fd1f31ae255b0f32efe423a950203d9b25bbe8/20239.txt#L8011-L8054) | `7daafe23aeef2377fe9a99bc285c5dfc0673440487ab43f78387312b6799304d` |
| 同書拉丁文 | [L27275–27310](https://github.com/GITenberg/Vitruvii-De-architectura-libri-decem_51812/blob/78eb1eed88044d5cac42a3dd811d5806e4e04cfb/51812-0.txt#L27275-L27310) | `b4fce89b0c304c7d1f26b299bf2dfcddbab8529c883f43ad1e75fae564daa861` |
| 普魯塔克〈馬塞勒斯傳〉英譯 | [P19090–19131](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L19090-L19131) | `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1` |

- E8014–8027／L27277–27286 說皇冠等重、事後有人指控金被等重銀替換、希羅求助阿基米德；旁白保留了「指控」與後來作者的歸屬。
- E8027–8033／L27286–27292 敘述浴盆溢水、奔回家與反覆喊話。L27292 確有 `ευρηκα ευρηκα`；L27294 的 `dicitur` 則在製作兩塊等重金屬的句子，不在奔跑喊話句。英譯與拉丁文屬同一本書，不能算兩位目擊者。
- E8035–8054／L27294–27310 的順序是等重銀塊、金塊、皇冠依次入滿水容器。尤其 E8040–8042／L27298–27300 是**取出銀塊後，用定量量器把水補回盆緣**，不是用量杯量水線到盆緣的距離。金塊與皇冠也從滿水起點比較。原文給銀比金排水多、皇冠比等重金排水多的方向，沒有可重算金量的量測數值，也沒有皇冠相對銀塊的數值。
- P19092–19097 說希羅請阿基米德把幾何想法用於機械；P19113–19125 說他坐在遠處用滑輪拖船。**所讀 P19090–19131 段落**沒有金冠、浴盆或喊話；這份沉默沒有被旁白拿來否定維特魯威故事。

[`claims.md`](claims.md) 的 102 行與 `video.json` 的 102 句旁白在 ID、文字、順序上逐行完全相符，且兩邊的 102 個 ID 都唯一。127 個來源連結（E 101、L 18、P 8）的顯示行號、URL 錨點、commit 和檔名一致，均在上述固定段落內。逐句判讀沒有找到缺少來源、來源與說法矛盾，或把物理推論寫成維特魯威實測數字的情況。

## 畫面與時長

- 檢閱 99 個 `shot` 提示詞與各自旁白；另有 1 個 `outro`。`look` 僅為 `cute-mystery`，插圖提示詞沒有要求模型畫可讀的希臘字。沒有發現具實質誤導性的旁白與畫面矛盾。
- 量水關鍵配對：`crown-041` 裝水到盆緣；`crown-r2-018` 使銀塊全沒入；`crown-047` 明寫把量杯內的水**倒回容器直到盆緣**；`crown-051`／`crown-059` 在金塊／皇冠輪前重設滿水線。`crown-048` 檢查水線時量杯在旁，應連同前一景閱讀；其提示詞並未要求量水線距離。
- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s24 --json`：0 errors、0 warnings。
- 依 `estimateTimeline` 的 30 fps 腳本估算：全片 `16573` 幀＝552.43 秒；開場首章 `1230` 幀＝41.00 秒；片尾 `585` 幀＝19.50 秒；**正文 `14758` 幀＝491.93 秒（8 分 11.93 秒）**，比 480 秒下限多 11.93 秒。這是腳本估算；當前沒有錄製旁白，正式 8 分鐘正文門檻仍須在 TTS 後以實際音訊時間驗證。

本輪結論：凍結稿的獨立敘事盲讀、固定來源、逐句映射與畫面提示詞覆核**通過**。錄音後須再核實實際正文時長。未產生或購買語音、插圖、配樂。
