# WD-40 X06｜三張 HOLD 鏡頭 v4 離線提示詞提案

**僅為審查提案，尚未修改 `video.json`，也未核准新圖。** 提案以 v3
主片 SHA-256 `931efad38297c832fd11a2aedfc12cc2ef5c61373e36632a1fcd916dbdf0fc68`
為基礎；獨立 v3 prompt-only 審查 SHA-256
`5ab635105dc384bbec80b4f32346697247c0ebdcdcff539391674f7b436c84a7`。
主媒體帳本截至停批為 US$1.1105／83 張圖／82 次圖審、未結 0，
SHA-256 `f74f080e0c970330826a0176f719f537ab9208fe2fc41cb6655df799a2d16679`；
manifest SHA-256 `efd4feabc68b8567104b3169308751a4f40d0aa84d2303521725c94818de5422`；
主工作區 STOP 在位。原 34 張暫可用插畫及其提示詞均不得變更。

## `x06-b03-s12`：未來式不能畫成現場成交

旁白 `x060312`：「公司計畫在新興市場賣小包裝滴油，當成較買得起的入門品。」
已付費 v3 圖 SHA-256
`e87f305702162306a9f2c7e59219603cf4008edbc035d48e20d8c677c29cb5c0`
雖 judge PASS，實圖是成人向有兩個孩童樣人物的完整店櫃展示瓶子，
有已在現場賣出的錯覺；人工與獨立抽看都 HOLD。

**舊 `data.prompt`（精確原文）**

> Medium close-up in a plain planning room, one adult planner sets a palm-sized unlabeled glass oil sample beside a small blank wooden scale model of a shop counter; empty wall only, no real shop, signs, banners, mascots, labels, logos or writing, soft daylight

**建議新 `data.prompt`（精確候選）**

> Top-down close-up on a bare planning table in an empty room, only one adult planner's hand places a tiny unlabeled glass dropper sample beside a larger plain glass bottle; both remain closed, no counter, shop, other people, faces, creatures, signs, packaging, labels, logos, symbols, letters, numbers or writing, soft daylight

一張手邊**樣品對照**支持「計畫推出較小的滴油入門品」，不畫市場
已經成交，也不畫新興市場的未經證實具體國別或銷量；避免任何
櫃檯、購物者和吉祥物。真正產品大小或價格只由口播與來源卡承擔。

## `x06-b03-s16`：把提問保持為品類對照

旁白 `x060316`：「可這三樣仍在修理工具。公司下一步為何連洗手和清地毯的東西都買？」
三次 v3 圖全部 judge FAIL：海綿變紙袋、加兩個人物，末張還有浮水印／
游離物件。入選但仍 HOLD 的舊圖 SHA-256
`1a2cdbbd31db99256078870bf3e2179593118d769825413fed47c75aa95c9109`。

**舊 `data.prompt`（精確原文）**

> Wide shot in a bare storeroom, one buyer lifts an unwrapped cleaning sponge onto a shelf beside a metal cylinder, cool overhead light

**建議新 `data.prompt`（精確候選）**

> Top-down close-up on a bare wooden comparison table, one smooth metal repair cylinder on the left, one unwrapped hand-soap bar and a small plain rug swatch with a carpet brush on the right; no people, shelves, sacks, packaging, signs, labels, logos, symbols, letters, numbers or writing, cool diffuse light

只有修理品與洗手／地毯用品的無字對照，呼應口播的「為何」；不畫出
答案、財務成果、收購已完成的具體交易現場或未列於來源的產品外觀。
移除模型反覆畫錯的上架手勢、第二個人與倉庫包裝。

## `x06-b04-s02`：原來的兩種通路

旁白 `x060402`：「第一個洗手品牌原在超市和藥店賣；」三次 v3 圖
全部 judge FAIL：人物未做放肥皂的動作，後兩張加了別的購物者、
紙包及黑邊。入選但仍 HOLD 的舊圖 SHA-256
`ede0dd5e07feb1e3677834be7bc9ad28ab13f7e96e4f22ef60a53b90b387d658`。

**舊 `data.prompt`（精確原文）**

> Medium shot in a quiet grocery aisle, one shopper drops an unwrapped soap bar into a wicker basket, overhead light

**建議新 `data.prompt`（精確候選）**

> Close-up of two plain retail shelf cubbies side by side, each holding one unwrapped hand-soap bar; a wicker grocery basket below one and a plain white mortar and pestle below the other, no shoppers, packets, letterbox bars, signs, labels, logos, symbols, letters, numbers or writing, soft overhead light

籃子與無字藥師用具分別提示超市、藥店，不需人物購買動作，
也不指稱它在某一家具名通路販售。避免藥瓶標籤、商店招牌、
可讀包裝或任何提前揭曉下一句五金／汽車通路的畫面。

## 審查與停線邊界

此輪**僅**提議改上述三鏡的 `data.prompt`。93 景 ID、95 句口播、來源、
數字卡、look、鏡頭、Shorts、片頭片尾、音訊與其它 75 個插畫提示詞
都應原樣保留；來源稽核及兩份盲讀只可在非提示詞欄位深比相等、
獨立視覺差異審查 PASS 後承接。`x06-b04-s02b` 已付費但未評審的原圖
SHA-256 `cab2a38a2df9292c6ccad99d128866a3a16540c51a59a46511945f3a8eeb1b2d`
只作證據；此提案不改它的 prompt，也不准直接選用它。三鏡舊 take
與 US$1.1105 總帳保留原 SHA，不以新提示詞重判舊圖。

獨立審查若接受此提案，才可逐字套入 `video.json` 和
`drafts/visual-safety.mjs`，凍結新影片及視覺 SHA，再安全橋接
34 張未改提示詞的已通過圖；每鏡仍須最多三次的隔離 allowlist、
即時 US$25 全包與跨集配額核算、judge 和人工原尺寸雙關卡。
目前站點 judge 剩 246；X06 對 41 未試和三個 HOLD 的剩餘最壞估計
132 次，X09 至少需 99，僅剩 15 次共享緩衝。這是停線原因之一，
不是付費授權。正式 5 秒／21 秒頻道動畫、Studio 可點片尾連結及
完成 MP4 均不存在。
