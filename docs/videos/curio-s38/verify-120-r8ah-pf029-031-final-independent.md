# S38 R8ah PF029／PF031 最後提示詞獨立增量紙審

2026-10-22 UTC。審者 `/root/s38_pf021_last_paper`，未撰寫verify119兩個修訂。結論：**PAPER PASS 2／2**，限兩個新提示詞及verify118已通過字卡的沿用性；原生圖仍待驗收，兩景各僅剩第三／最後一張實際原生圖。沒有媒體、creative檔案修改或Git提交。

## 精確版本及差分

現稿 `video.json` SHA-256 **`2b435f0ee955ffa798f3c44e01c504e47e5fae1eb7d4bbfcdc2a0c4aa904bc6b`**；`script.md`仍 `e0fed6c437b27db0e15db7e872eee9d7e306c36286ea4753f48e6effd369b3c9`，`claims.md`仍 `2bae39a299bc21889d1ac5211437d48cd221f65ff8c0d97e2344662ce77b57ed`。verify119精確差分SHA `3e68ec8b42f84cf042d7de3826a6fccf85e0e38780bc7ebe629eaf8b18ad58c8`。

我將且只將兩個new字串反填old，逐位元組回復verify118所審video SHA `4c1ca150f55af9b08a597123fd38cbe5d6fb8ab605df19651e875120fb2da592`；解析前後JSON僅PF029、PF031的`data.prompt`不同，PF028來源卡完整物件及其正確L65860–65866行錨未變。全片112個口播ID／文字與Git HEAD逐項相等；script／claims檔案與verify118完全相同。因此verify118的中文譯文、日期、說話人及112句證明可沿用至本稿，不能把其舊video hash當本稿hash。其他83景中除這兩個prompt外無新改動，PF024–PF027及新入選PF030／PF032也未變。

## 固定來源與兩景判斷

重讀固定Pepys日記1666年9月2日L65860–65866（全文SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`）。市長在Canningstreet抱怨自己精疲力竭、人們不聽從、拆屋趕不上火；他說不需更多士兵、熬夜後得休息，隨後彼此離開。

| 景 | 旁白／新畫面與判斷 |
| --- | --- |
| PF029 | 既定旁白是日記記下市長抱怨「人不服從，火又追得太快」。新prompt讓1666英國市長面帶疲憊、向書記說話；只保留簡單灰牆、煙及羊毛披風／白頸巾，避免原圖的現代交通標誌。原文有市長說話、疲憊及頸邊手帕，衣料與牆面是年代相容插畫選擇，不聲稱日記記錄了精確顏色／材質或表情。**PASS**。 |
| PF031 | 既定旁白是市長說不需更多士兵後轉身離開。新prompt側面畫他穿長披風離去，書記觀看，背景簡化成橡木門與石鋪地，避免原圖的黃線瀝青路。它沒有增添他去了哪裡、已睡下或誰勝任拆屋的結局。門、石地、衣飾是概念構圖，不是存世街景重建。**PASS**。 |

兩景都保留原主要動作與對話／離開先後，只縮小現代背景生成空間；沒有style／negative／look改動。原圖驗收依curio規則：judge通過後只因材料性旁白／來源矛盾或畫風漂移退件，不因匿名卡通的非關鍵服飾、年齡細節或道具與prompt不完全一致而重畫。

## 私人守衛快照與放行界線

本次重新讀取時，active manifest SHA `f327d168773fa4e246a5e691c7341909b2c78a01d82ff1b0d34656333b74f7ae`，**22張KEEP**；全部完整場景與前版相等、實檔SHA符合選圖條目、judge PASS且無needs_review。PF028／PF029／PF031已不在active入選圖單。STOP在位、jobs空，與verify118審查期間的運轉中快照不同；本次以已停妥狀態覆核。

Ledger SHA `577dc57ccb0c63f95ce7620613ed2a1bd972fca4f7baa8b32ea4c1f843e73982`：實付US$1.1330／78image／78judge／1music，另保留舊US$0.0035 reservation。逐筆計數PF029、PF031各有**兩張**ready原生image；各最多再一張，不得因新prompt重算次數或購第四張。正式lint exit0，**0 errors／0 warnings**。

本票支持在STOP下安全離線回綁現稿visual hash、驗22張舊KEEP實檔／key／judge stamp，並重新查live模型、餘額、單價、dry-run與整集US$4.58 cap後，依既有授權各做第三／最後一張。它不自行解除STOP，也不把紙審等同實圖KEEP；其他未畫景承接既有整集來源鏈與有界流程，已耗盡景及來源卡不重開。
