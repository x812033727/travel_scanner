# A16 正式章節格式原型

**只完成本機格式準備，尚不能交工作者製作。** 沒有外部API、主機、付費媒體、repo修改或任何production PASS。

## 已完成

- 凍結原稿 50 段／2114 編輯計數，逐字重建成95個有ID片段、83鏡。原ID、UTF-16切片、每鏡文字、全文串接完全一致，沒有增刪旁白或加pause／say。
- 六章保留67插畫、16張數字／來源卡，64個預定不同插畫；三組共圖仍是006→012、007→041、008→060。prompt／camera／image_asset_key逐字保留，沒有實際圖片。
- 16卡直接用既有native title：text→title、scope→subtitle、source→tag、cc_safe=true。官方template check 0錯，官方slideHtml的visibleText保留所有原字串。沒有新增scope；沒有做像素／手機可讀性驗收。
- 28個來源CID對應68列完整原段context claim，全部UNCHECKED。source有多個候選時保留null；C16跨FY2025算例與FY2026已公布，候選fact是5與9，未選一列冒充完整覆蓋。
- 9個loop保留完整setup／payoff段組在mapping，原生scalar取完整組的最後片段。三個開場預告之外的長掛鉤也沒有省略。
- 官方composeStory與advanceStory的本機relint分支確實執行；actual shot_reading為67鏡、0 traps，cute gate 0 errors。原始完整lint結果保留。

## 真實阻擋與限制

1. **發音字典：30處、13種詞未登錄。** Costco、Price、Club、Jim、Sinegal、Jeff、Brotman、NPR、Hebrew、National、Craig、Jelinek、Fox。這是保存的A29同一lexicon fixture檢查結果，不冒充目前正式站最新狀態。不填null或試讀未驗證的pronunciation來消音；後續需查實際字典並完成讀音／音訊驗收。
2. **模型答案parser仍不能接作者title卡。** 六章readChapterAnswer均因title被拒。compose能接受，不代表現有匯入會採用這些章檔；普通企劃匯入仍會讓writer重寫。需要精確source／row／series／six chapters雜湊的安全採用流程。
3. **估時與節奏仍待實錄。** 純旁白六章含hook估507.36–551.48秒；正式預設timeline為567.3秒，含95片段各300ms、82鏡間各700ms、最後1500ms與frame rounding，不能當TTS實測或拿間隔補長度。兩項敘事警告是91與92秒無偵測到open loop；原文保留，待實際敘事和聲音上下文審查。其餘craft warnings亦全數保留，不為旁白故事改成角色對話。
4. **統計差異不是刪字。** 編輯2114與官方1995相差119：官方忽略10個「〇」，另把Latin單詞各算2單位，比逐字計數少109。完整字串逐字一致。
5. **共圖尚未驗收。** 三組相同請求條件的seed1合成cache key一致，但每鏡judge／重畫選圖仍可能分歧；image_asset_key只能在sidecar保存，data.source只可裁先前clip，不能共用still。最後必須核對accepted檔案SHA。
6. **卡片觀眾呈現未完成。** 原卡的S2簡碼與「後製分行排版」字樣均原樣保存；正式成片前應以另次審核展開來源出版品並處理版面，不能把HTML保字稱為像素QA。長算式也需要真renderer可讀性檢查。
7. **原cast保持不動。** compiled plan仍有founder描述，凍結分鏡沒有data.characters綁定。是否需要既有設定圖、如何保持匿名示意，是正式採用前的明確決定；本包不產圖、不把generic人物綁成真人。

## 檔案

- chapters/：六章正式形狀候選，全部claim待查。
- mapping.json：逐字／原段／claim／source／fact／完整loops／共圖／卡片對照。
- compose-lint-evidence.json：官方合併及30項真lint錯誤、24 warnings；不是PASS。
- card-adapter-evidence.json：16張native title的HTML保字結果，無像素QA。
- shot-reading-evidence.json：67鏡實際工具讀法，0 traps。
- readiness.json：現存限制、未完成階段、詞彙清單和計數差異。
- remaining-schema-inventory.json：A16/A37/B14/A21只讀盤點；合計49卡scope完整、36loops的setup/payoff皆arrays。
- input-pins.json有44個主要讀取檔加1個repo voice fixture（45個檔案hash）；另保存lexicon來源hash。output-pins.json是第一次工具執行輸出索引；handoff-pins.json另涵蓋本readiness與本次交付全部檔案。

5秒片頭在hook之後，21秒片尾在全部旁白之後；沒有用假無聲scene補品牌動畫。可關閉繁中CC已在compose保持burn_in:false。正式來源查核、listener、narrative、pilot、TTS、圖片、render、owner看片與上傳均待完成。
