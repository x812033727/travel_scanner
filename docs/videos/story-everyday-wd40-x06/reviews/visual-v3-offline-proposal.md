# X06 WD-40｜第三輪兩鏡視覺修正提案

第二批畫面檢查後，`x06-b03-s07` 的三次 MiniMax take 都被圖審判退：
每張右下角都有紅色簽名樣 watermark，最高分 9.41 也不能入片。
`x06-b03-s12` 雖得 judge 9.29 PASS，右上角店招有清楚的漢字樣
筆畫；本次製作和獨立抽看均判 **HOLD**。原圖、圖審與費用仍保存於
媒體工作區。主 `STOP` 不移除，也不以 `accept-best` 或未改 prompt
的第 4 次 take 繞過驗收。

這次只改下列兩個 `data.prompt`。先前已審 `video.json` SHA-256 為
`d1ac6f93e15396813dda6ac2d76028f6539be2d746d647d1fd44e4790dd5d0c5`；
新 SHA-256 為
`931efad38297c832fd11a2aedfc12cc2ef5c61373e36632a1fcd916dbdf0fc68`。
以場景 ID 對照並刪除所有 `shot.data.prompt` 後，93 景的其餘 JSON
深度相等：口播、來源、卡片、look、時間線與其它 76 個提示詞均未變。

| 鏡頭 | 舊 prompt | 新 prompt | 目的 |
| --- | --- | --- | --- |
| `x06-b03-s07` | `Medium shot at a uncluttered shipping table, one planner slides a smooth metal cylinder along several branching carved wooden tracks, morning light` | `Close-up at a bare distribution table, one planner's hand slides a palm-sized smooth metal cylinder along a blank Y-shaped groove in a wooden board while the other branch stays empty; frame tightly around the hand, cylinder and grooves, no shelves, labels, logos, signatures or watermark, morning light` | 只留路線分岔與尚空的一支；填滿畫面並明確排除簽名、水印和背景貨架，不增添歷史主張。 |
| `x06-b03-s12` | `Wide shot inside a uncluttered neighborhood market, one shopkeeper sets a small smooth glass oil bottle on an empty wooden counter, soft daylight` | `Medium close-up in a plain planning room, one adult planner sets a palm-sized unlabeled glass oil sample beside a small blank wooden scale model of a shop counter; empty wall only, no real shop, signs, banners, mascots, labels, logos or writing, soft daylight` | 改成計畫室的樣品與空白櫃台模型，不再畫成產品已在新興市場銷售；移除誘發假中文字的招牌、海報和吉祥物。 |

新提示詞仍只是旁白的可愛示意，不宣稱 1997 年某國已實際上架；
`x06-b03-s07` 問的是通路能否把原產品送入未賣市場，
`x06-b03-s12` 說的是計畫在新興市場賣較易負擔的小包裝滴油；
畫面只呈現規劃室中的樣品與模型，不宣稱實際售出。
原始來源審查和兩份盲讀若要沿用，必須由獨立審查者再核對上述
兩鏡、精確 SHA 與之前的 prompt-only 審查鏈。已暫可用的 32 鏡
prompt／take 不可因這次差異被替換；舊失敗影格也不可因新提示詞
自動過關。只有新差異審查 PASS、舊 take 綁定安全遷移、即時站點
額度與 US$25 硬上限核對後，才能在隔離 allowlist 限這兩鏡
各最多 3 次重新送圖；主工作區 STOP 保留。
