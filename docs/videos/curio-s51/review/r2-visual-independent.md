# S51 R2｜獨立書面畫面差分覆核

2026-10-20 UTC。覆核對象是 [R2 作者候選版](../verify-2.md)的 137 個正文 `shot` 提示詞；逐景連同旁白讀過，並直接對照 [R1 獨立覆核](r1-source-independent.md)、R1 凍結 JSON、逐句主張表及三份固定原文。這是**生成前的書面畫面審核**，不等於已看過插畫、聲音或成片。

**結論：畫面 HOLD。** R1 指出的主要夜景光線、夜船橋與事後調查混場、Beesley 著書視角、虛構無線電儀表已修正；但 `cal133` 的接艇時天色與同一份正式調查明文相反，`cal040–041` 新增沒有來源的船燈遮板示意，`cal064` 仍可能把白星點求救火箭畫成泛稱的 flare。按下表修提示詞後重新固定版本，再由另一位覆核者核對差分。未改的 140 句旁白沿用 R1 **史料 PASS**；R1 兩名盲讀者的敘事 **FAIL** 仍須 R3 修稿及重盲，這份畫面覆核不將其升級為 PASS。

## 凍結與獨立重算

| 檔案 | R2 SHA-256 |
| --- | --- |
| `brief.md` | `82a2e4a3d7a240dd0f249eeeec3b3dffdf1446d9eb049432320e72fe6b6a1023` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `21dd50280e0d89ca998a9cf5a0820589b6ae5ffbf233e49ba988aa6dd477dad1` |
| `script.md` | `5b6c6d0924670033b379c40a00f4ae3991d920661a5479631e5ba2e3143de42b` |
| `video.json` | `8242a57797308952e2be39483acfc65895b43814bbb77f9e7bc01248d42d610d` |

固定轉錄本 SHA 也重算相符：[G，1912 年英國正式調查](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt) `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；[B，Beesley 1912 年自述](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt) `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`；[A，Gracie 1913 年自述](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt) `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。本輪讀取 R1 覆核者留在 `/tmp/s51-independent-sources/` 的固定轉錄本；沒有重下載，也沒有把電子轉錄當成原件掃描。

直接以 SHA `1639fd758d59f44b7dbae66603f1148c3abf7dd6229f16b32b3c5b34bdcf20df` 的 `/tmp/s51-r1-video.json` 比對目前 JSON：**只有 75 個 `scenes[*].data.prompt` 值不同**，其餘欄位深度相等；[R2 差分表](../verify-2.md#精確提示詞差分)的 75 個 ID、R1 字串、R2 字串逐一精確吻合。移除全部 `data.prompt` 後，兩版正規化 JSON SHA 均為 `8f95f35957fb4bb2a35f193842c9960de90ac3f84ca4ca66e4168dacc8ecfdf3`。`video.json`／`claims.md`／`script.md` 的 **140／140** 個 ID、順序及旁白字面相同、無重複 ID；137／137 正文景都是有非空提示詞的 `shot`。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s51 --json` 回報 **0 errors／0 warnings**。最快時長僅為工具估算，尚非 TTS 實長。

## R1 問題與全景掃描

- `cal004/008/016/028/032/040/044/052/064/068/072/076/080/088/092` 的「夜間＋`pale dawn light`」已解除；其餘夜景的陰天日光亦改為暗夜、船橋燈或艙燈。約 04:00 新船的 `cal007/098` 不再宣稱 `first light`；約 06:00 無線電與出航畫面改為早晨。`cal093–101` 仍用黎明前暗景；此處船鐘和兩艘船的曙光時刻不宜再當精確定值。
- `cal067/089/091/092/102/106` 現把事後資料桌放到獨立日間場景，沒有把調查員放在加州人號夜間船橋。`cal118–119` 是私人閱讀桌上的匿名回憶錄，不再把 Beesley 的書中保留意見畫成他在 1912 年英國聽證席發言。這與 B [L2612–2659](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt#L2612-L2659) 的事後文字層級相符。
- `cal028/052` 已去掉無來源的 `wireless needle`／`signal meter`，改為電鍵、耳機及空白紙。全景未見可讀的假文件、命名人物肖像、Lord 的可辨肖像、Gracie／Beesley 肖像、固定五英里海圖位置或確定救出人數。`cal068` 的乘客明示無肖像細節；「young sailor」僅為匿名角色，不指定歷史人物年齡。`look.preset` 仍為 `cute-mystery`，畫面定位為卡通示意。
- `cal005/074` 的淡白遠光符合船橋看見白火箭的示意；`cal062/065` 的緊急艇旁發射座有 G [L3182–3189](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3189) 直接支持。全景沒有要求彩色煙火、精確八枚同框或可量出的火箭軌跡。

## 仍須修正的提示詞

| ID | 來源與畫面衝突 | 可直接執行的修法 |
| --- | --- | --- |
| `cal133` | 現寫 `before dawn`、`dark calm water`，畫的是卡帕西亞號 04:10 接第一艇。G [L3207–3221](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3207-L3221) 說 04:10 接上首艇時 **`it was just daylight`**。R2 把 R1 的 `at dawn` 改成相反的「黎明前」。 | 改成 `at first daylight`／「天剛亮」的昏淡晨光，保留首艇與登船示意；不要給未引證的精確日出鐘點。 |
| `cal040–041` | R2 新增 `unmarked/loose light shutter` 並放在船模旁。G [L3390–3393](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3390-L3393) 說 Groves 承認**轉向可能使部分燈從視角被遮住**；它沒有指認船上有遮燈機構。現詞易把幾何遮蔽畫成器材操作。 | 移除 `light shutter`，用桌上無字船模相對固定觀察視線轉向、模型部分甲板燈離開視野示意；保留「可能」而非確證熄燈。 |
| `cal064` | 旁白是白色求救火箭，現提示詞只寫 `releases one flare upward`；G [L3182–3189](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3189) 寫火箭由 1 號緊急艇旁 socket 發射，空中爆成**白星點**。泛稱 `flare` 未約束顏色、裝置與形態，可能生成手持或彩色煙火，與 `cal062/065` 的發射座脫節。 | 明寫「一枚白色求救火箭從緊急艇旁固定發射座升空／白光星點」，不指定精確彈道或總枚數。 |

`cal104–105` 約 06:00 寫 `at dawn` 可在下一次提示詞修補時改為 `early morning daylight`，避免把「約六點才得知消息」畫成第一道曙光；這是穩健用語建議，**不另列獨立 HOLD**，因 G 沒有明記加州人號該刻天色。實際生成圖仍需核色彩、人物、文件文字與船燈表現；本輪沒有生成圖或音，也未作網站、付費媒體及發布關卡。
