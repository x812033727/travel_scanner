# 第 26 集真人版 fix-polish：上架前精修重拍（2026-11-21）

來源：`review-zt/consolidated/retakes.json` 的 e026 tier A 六鏡（沒有 tier B）、審片報告 `review-zt/reports/e026.txt`（嚴重 1、中等 3–6、輕微 13）。
種子 9269101／9269102，每鏡兩支，12 支草稿、70 秒，960×544 Ref2VA。base 是 `_live-e926/.../picks.json` 現在選中那支的提示詞（`runpod/live/<motion_from>/prompts/`）。
s38、s39 同一批：同一塊方糕、同一張芥黃紙；s38 的地點與倒地位置照 s37（許記門前）與 s40（門前街心偏左，s40 不重拍）。

| 鏡 | 審片問題 | base | 改了哪些句子（舊→新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s38（嚴重） | 換地方換人：藍冷斜坡巷、沒有許記門；倒地的人露髮髻、淺灰袍；第一格圓糕已在地上；旁人不退；慢慢跪坐再躺 | `d1/prompts/ref-s38-9261102.txt` | 地點：門前石板與長櫃→「同一條街」，左緣許記折起的淡色木門、對街紅綢、暖晨光、相機水平；景別 medium→medium-wide 站立眼高。人物：long grey robe＋cloth head wrap→灰交領袍＋**深灰布包頭蓋住全部頭髮**、背對鏡頭、站在門前街心偏左（照 s40）。首格：已彎腰、糕紙在腳邊→**站著彎腰捂肚子，半塊方糕連芥黃紙還在右手**。動作：slowly sinks→踉蹌一步、膝一軟側倒、背對鏡頭蜷著不動；糕紙此時落地。旁人：兩個灰袍客人→s40 的綠短衣黑包頭男與靛袍婦人，各往後退兩步、雙手舉在胸前 | `set-xianjie-shi-l1`（裁切就是那條斜巷）→ **`set-xianjie-l1`**（s25、s40 用的大街） | 大街圖是廣角、兩邊屋子外倒，medium-wide 可能被拉回全景；「倒下」與「旁人退」兩個動作在同一鏡（base 就是），可能只做一個；許硯不入鏡（左緣只寫木門），跟 s37／s40 他在門口不衝突，但若畫出空門洞會怪 |
| s39 | 地上是圓形有花紋的糕（像月餅） | `d1/prompts/ref-s39-9261101.txt` | one bitten small white cake→**小方塊白糕：四邊平直、方角、頂上撒細白糖、缺一角**；rough blank yellowish paper→芥黃色粗紙 | 沒換（`set-xianjie-shi-l1`，只看得到石板） | 「方塊」仍可能被畫成有壓紋的糕；只寫正面描述，沒寫 round／pattern |
| s25 | 六個同款灰袍人齊步走進門，像複製人行軍；鏡頭歪；看不到排到街尾 | `d1/prompts/ref-s25-9261101.txt` | 「六個同款 plain robes＋head wraps、faces hidden」→ 六個逐一寫衣著、性別、年紀的客人（綠短衣男、紫袍提籃婦人、灰鬍老人、赭黃短衣青年、淺藍短衣白頭巾婦人、灰袍胖男），**間隔一步從許記門口沿街往遠處排到街尾**、站著等；動作 shuffle one step forward at a walking pace→站著換腳、只有排頭往門口挪半步；加「相機水平、地平線平、牆垂直」 | 沒換 | 審片建議八人，稿子人數規則（拍法 25）寫六人，照稿子留六人；六人撐不撐得起「排到街尾」要看片 |
| s37 | 許硯起疑那句笑著說；客人手上的紙米白、跟許記白紙分不出；客人露四分之三臉 | `d1/prompts/ref-s37-9261102.txt` | `frowning, not smiling: brows knotted…`→**第一格就嚴肅：眉壓低打結、眉間深紋、眼瞇盯黃紙、臉頰不動、嘴角平、句與句之間抿回一條線，說完最後一字收回平線到最後一格**；紙 scrap of rough blank yellowish paper→巴掌大皺芥黃粗紙、在灰袖前看得出黃；糕寫小方塊撒白糖；客人 long grey robe→灰交領袍＋深灰布包頭蓋住全部頭髮，**從左肩後拍、只見後腦與左耳**，咬一口後一直嚼、嘴閉 | 沒換（許硯 l1＋angle-a＋`set-xianjie-xuji-l1`） | 許硯定妝照是平臉，沒有帶笑的圖可拿；冷臉全靠文字 |
| s32 | 賴三換臉（臉長、法令紋、像大十歲），頭巾變大塊包頭 | `d1/prompts/ref-s32-9261102.txt` | `low-angle close-up`→相機略低於下巴（少一點仰拍變形）；加「同 <Picture 1> 的年輕光滑臉、尖下巴、皮膚沒有紋」；`an old cloth head wrap below his topknot`→**一條平的灰褐布帶緊綁在額頭眉上、小髮髻露在上面，照 <Picture 1>**；拿掉近景用不到的 limping；加上唇冒汗、眉頭中間往上擠；視線落點 corner of the table→桌角的小竹籃（仍在畫外右邊） | 沒換 | 錨句裡 `an old cloth head wrap` 照規定沒動，跟構圖句的布帶寫法並存；油燈底光仍可能把臉打老 |
| s28 | 魏少卿換臉（較老、寬臉）、袍子素面、店面變木板門加布幡、高供桌加紫色糕、夥計像少年、左柱金字小牌 | `fix1/prompts/ref-s28-9261201.txt` | 景別：膝高 low wide 全身→**腰高 low medium-wide、小腿以上，臉大**（s26 膝上的那支臉是對的）；店面：加「門洞掛很多條長的紅珠串、紅綢，木牆與門柱素面、一級石階」（接 s26／s29）；桌子：long low dark table→**只到膝蓋高的矮長桌**，small dark red sugar cakes（畫成紫色）→深褐糖塊；袍子加兩肩金繡；冷臉：`teeth gritted… corners of his mouth pulled down`→眉壓平、眼瞇、嘴抿一條線、下顎咬緊；夥計：thin young man of about twenty→**二十四歲的成年瘦男、高到魏少卿的肩**，往後跳到門柱邊 | 沒換（魏少卿 l1＋`set-xianjie-weiji-l1`） | 景別拉近後翻桌可能出畫或桌子變小；紅珠串是 s26／s29 模型自己長的，參考圖上沒有，可能畫不出來；左柱小牌若再長出來仍可用 delogo |

## 三個檢查（2026-11-21）

- `polish-build.py 26`：6 鏡、12 支、70 秒，0 錯
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error、0 warning
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error、0 warning

沒有送出任何生成。
