# X06 WD-40｜本機試看片畫面提示詞差異待獨立覆核

本文件由畫面製作代理整理**差異證據**，不自行簽署來源或盲讀 PASS。
2026-10-20 第一批 MiniMax 試畫有大量假字、疑似商標及動作錯誤；
詳細故障和原始圖檔證據見 `local-preview-art-gate.md`。因此把易誘發文字的
紙箱、罐面、倉庫牌、帳頁與貨架標籤改寫為無字實物動作，讓精確商標、
年份、金額與來源只在原生卡及字幕出現。

| 綁定項目 | SHA-256 或結果 |
| --- | --- |
| 原 `video.json` | `4c9215b06364b3fb96cd9249054c6e7c15de381b4e8717a39a11fb9ad62bf1ba` |
| 目前 `video.json` | `907f8e3ff45f3edf0bbed64a54216c761696e8e954d51c315a8a228069e204d1` |
| 原來源審查 | `2b386249fdb86d2747ef0d25f36f621da109a0890e98d2dd5ef5c909b724599c` |
| 原盲讀 A | `553c6f7bc007f36923901b675ff59844a74e5d027e1ae58eebfb10abcf8727c1` |
| 原盲讀 B | `4482bb7c207e6d4dbf8f379adebde6d77a85e6ccb1edd2bfaa21b9f177f0c7c9` |
| 構造差異 | 93 場仍為 78 個 shot、15 個 card；74 個 `data.prompt` 字串更動；其餘 JSON 移除 prompt 後完全相等 |
| 完全保留的四鏡 | `x06-b01-s01`、`x06-b01-s03`、`x06-b01-s05`、`x06-b02-s03`；可保留原 MiniMax take 和 judge 判讀 |
| speech hash | 原／新皆 `0aaf18a3b41a8319` |
| look hash | 原／新皆 `98a370ae40badbaf` |
| visual hash | `41033c16cfd81e7c` → `b2986dd79bb9039d` |

逐欄比較證實**沒有**更動繁中台詞、TTS `say`、音樂、章節、卡片
數值、故事迴環、來源 URL、說明或 Shorts。`script.md` 和
`source-matrix.md` 因 compose 重寫而僅更新所顯示的 `video.json` SHA；
原音訊 timeline 的 speech hash 仍匹配，配對的 TTS 乾跑回報 95 請求、
0 句需重合成。先前來源與兩份盲讀驗證的是原 SHA，不能假稱它們已審新 SHA；
需由獨立審查者確認此視覺差異不改口播主張／敘事界限，並將新 SHA 綁到
單獨覆核紀錄，再跑完整成片 QA。

最棘手的三鏡改動如下；三鏡也是唯一建議的下一輪付費小試範圍：

| 鏡頭 | 舊 prompt | 新 prompt | 避險與語意 |
| --- | --- | --- | --- |
| `x06-b02-s01` | `Wide shot in a modest shipping room, one anonymous clerk checks plain spray-can cartons bound for overseas shelves, morning window light` | `Wide shot in a simple shipping room with uncluttered walls, one adult clerk sets a smooth metal cylinder onto a wooden handcart, morning window light` | 拿掉會印假字的紙箱和牆牌；仍是噴劑從庫房進入出貨路線。 |
| `x06-b02-s02` | `Close shot at a home repair bench, one anonymous adult loosens a stiff metal hinge beside an plain spray can, soft daylight` | `Close shot at a home repair bench, one adult mechanic turns a stiff metal hinge with both hands, soft daylight` | 拿掉可出現假字的罐面；用卡住的鉸鏈表達產品用途。 |
| `x06-b02-s06` | `Close shot at a small port warehouse, one anonymous logistics worker checks plain cartons near a ship window, hazy daylight` | `Close shot at an open port dock, one adult worker guides a wooden handcart toward a distant cargo hull, hazy daylight` | 避開 Amazon 式箱面弧箭頭、門牌英數；碼頭貨運動作仍支援出口旁白。 |

另外 `x06-b01-s04` 的地毯與廁所清潔提問，已改由小塊地毯樣本和
馬桶刷的外形與金屬噴罐相對照，無產品包裝。全片其它 70 個更動也在
`drafts/visual-safety.mjs`，由 `compose-video.mjs` 強制要求 78 鏡都有
明確提示詞，防止舊的高風險字串回流。編輯器 lint：0 error、0 warning。

目前 STOP 仍在。三鏡乾跑預估最多九次 MiniMax image-01 與九次評審，
約 US$0.1215；當時 X06 帳已花 US$0.2835，試畫後最壞可見累計
US$0.4050。全片若四張沿用、其餘 74 鏡各最多三次，新增最多 222 張
和 222 次評審、US$2.9970，累計已知媒體費最多 US$3.2805。
因此相對使用者 US$25 **全包**上限，保留 US$21.7195 給其餘
語音、轉錄、複查、稅費或不可預期支出；不可把本站的 US$200 每片
上限誤當使用者核准額。以上是固定最多三次、沒有額外重試的上界。
新配樂月額度為零；來源可驗的舊曲只能作標明來歷的本機概念用曲。

本站最近一次查詢餘額：圖片 1,956、評審 671、新配樂 0。
若 X05 保留最多 198 次評審、X08 保留最多 339 次評審，剩餘 134 次
不足 X06 全片的 222 次最壞上界；三鏡小試最多 9 次仍可容納，但
全批必須重新確認配額與其它工作排程。
