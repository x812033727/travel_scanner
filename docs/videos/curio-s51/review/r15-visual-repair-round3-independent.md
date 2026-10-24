# S51 R15｜第三輪三景提示詞獨立來源與差分覆核

2026-10-20 UTC。**PASS（僅書面提示詞／來源）；實圖及整集分鏡仍 HOLD。** 我未撰寫本輪提示詞，也未生成圖片。對照[第二輪定點選圖目視紀錄](r15-native-art-pilot2.md)、[作者第三輪修訂](r15-visual-repair-round3.md)、[固定研究](../research.md)及 SHA-256 `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd` 的英國調查固定全文。

| 檔案 | 第二輪 SHA-256 | 第三輪 SHA-256 |
| --- | --- | --- |
| `brief.md` | `bea6a0ff26ddfed12ee2b9d077b2359a12392c301bf9032c69e66a403337a0e3` | 同左 |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` | 同左 |
| `script.md` | `cbc5a1891deacd029e081b61eb316e076e422cdb45ebceb4b072fa875e55ce83` | 同左 |
| `claims.md` | `c9dc1ec402f48f3ee55e663c6a988872ca286c55994f766106fa29a006a23e69` | `8ed2a82a193ad95f4111af0136fb3da8892e1ebbbff5e16d1be6a1707140bdf1` |
| `video.json` | `6e387d19cf4562be1a34b75c0177a20de3a3ce67a583bcf4aba1cb84a1f26634` | `f67295e932e1733470e5e23dbc311bc4fdae075ced530d35bfeeaf61ffed08ba` |

把現檔三條新 prompt 換回第二輪原文，逐位元重得第二輪 `video.json` 與 `claims.md` 的上述 SHA。兩版 JSON 深層差分**只有** `cal005/015/018` 的三個 `scene.data.prompt`；兩版 claims 差分**只有**末段同三個畫面備註。原 131 條旁白／來源列逐位元相同，原表前綴仍為 R15 初版 SHA `78a401c52ca7b0bbf4393a4f354dab07393d454f852c38c21acc77d292f63a4b`；131/131 行 ID 與旁白同 `video.json` 對齊，全部 13 條畫面備註與同 ID prompt 逐字一致。章節、鏡頭其他欄位及全部口播均未改。

| 景 | 固定來源與新畫面界線 |
| --- | --- |
| `cal005` | [R06](../research.md#可說的事與不能跨越的推論)及 G L3182–3187 記火箭從發射座升空、在空中爆開並撒出白星點；[R07](../research.md#可說的事與不能跨越的推論)及 G L3428–3440 記加州人號船員稱見白火箭。單枚小白光自海平面向上、短直尾跡是讓觀眾辨認「升起」的示意，沒有精確宣稱歷史軌跡，也不指認畫面中發射船。 |
| `cal015` | [R01](../research.md#可說的事與不能跨越的推論)及 G L3292–3298 記加州人號是未載客貨船；G L3362–3364、L3399–3401 記夜間船橋值班。單名匿名值班員在木船橋、窗外黑海符合時間及事件；三扇窗、桌子和制服造型只作插畫布景，不是已查證的船橋布局或某人的肖像。 |
| `cal018` | [R04](../research.md#可說的事與不能跨越的推論)及 G L3366–3373 記 **Groves 自述**看到兩盞桅燈，據此認為遠船是客輪。把兩盞高低白燈置於**同一艘無名遠船**剪影上，清楚呈現這段目擊；燈高低與單船構圖是可讀性示意，不宣稱量得燈高或當夜海面只有一艘船。沒有把他對客輪的判斷或後來調查的船名結論寫成當夜已證事實。 |

主工作目錄 `narration.wav` SHA-256 `7df974a903ba671b05312599c525c070a4f8d74454e90adb2a2e2ddc08a98c0c`、`timeline.json` `2c431b002119cecd79744cb425b064786d97a7b8c753cfc3c0d0c094cdf8088b`，均與 [R15 音訊收據](../verify-15.md)相同；沒有重做音檢。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s51 --json` 回 **0 errors／0 warnings／131 lines**，`git diff --check` 通過。

這三條新描述的來源層級成立，且未新增遠船身分或救援結果的確定性。第三輪新 JPEG 仍須正式評審及逐張目視；首 23 景之外尚未開畫，站台分鏡卡也未核准。不能把本次書面 PASS 或舊圖的機器 PASS 作為插圖／分鏡關卡通過。
