# 第三片：官方片頭尾、完整1080p及EN／雙語CC已交付

截至本輪文件快照，新版官方5秒片頭與21秒片尾已加入，完整1080p、經當前音檔核驗的EN M4A、繁中與EN的SRT／VTT／標題說明已直接送到[該片Mokaair後台](https://mokaair.com/zh-TW/admin/videos?video=claude-formal-verification-255)並authenticated讀回。當前為外語EN1/8，final `e66d6661-c991-42fc-abde-30e942c9fe5b` 仍manual pending；**原生QA真實false10/11，只有captions未過，整片與八語DOD尚未完成**。

| 版本項目 | 實際結果 |
|---|---|
| 來源與旁白 | source e6e87e77…c2b99f，claims527048b6…fa9c6，speech8028c7320d9cab29；105個當前zh-TW原始WAV／完整intended與ASR綁定維持PASS，master19ae…7373。 |
| 新版主片 | `b635269e24134b2c2c0e300a77d03f51ce4c15f2a9bc31cd6e61c0ec87c1162a`，54,578,838B，1920×1080／30fps／17,593frames＝586.433333秒畫面；AAC586.510秒，尾差0.076667秒另列。 |
| 正式素材 | package416c8768…63e88；placed branding39d34ab0…eda64。150frames片頭在正文frame732後插入，frame882回到正文；frame16963起630frames片尾。root實看九接點及最後影格。 |
| 原正文保護 | 新build/body.mp4完整bytes等於原BODY c8f4…ed5／48,226,281B；原正文扣冷開／舊outro後523.733333秒，未因新片頭尾改稿或新增旁白TTS。 |
| 新版EN M4A | `af7c3d50693e7231513bdb57e4f404b9491d449dddcad9c12d7c5e931c3a799a`，15,391,038B，586.510秒／AAC48kHz stereo／−14.1LUFS／TP−2.1；101原fit視窗max1.15不變，105當前raw／intended／ASR全PASS。 |
| 當前QA | false10/11，a458…edcad；Jev stance.83／demo.91／advice.01／sponsor.04。JA舊dub不符新版branding，另有ES4／PT2／ID2共8速度advisories；原JA14旗不清除。 |
| 當前附件 | 23roles＝原生預覽／contact／主縮圖／EN4項＋主片／EN下載2項＋7個舊版history引用＋10個ZH／EN字幕說明引用。六個當前小文字blob，ZH106cues／EN108cues，各覆蓋105source IDs，選定兩語零速度提醒。 |

[當前交付摘要](branding-v4/delivery-summary.json)、[主片／EN／歷史媒體安全projection](branding-v4/main-EN-history-actual-delivery.safe-projection.json)及[雙語CC實際收據](branding-v4/CC-title-description-actual-delivery-receipt.json)分列範圍。05:55:27.601Z正常9blob處理及同pending補件完成，06:40:36.548Z再完成6textblob／10roles正常補件。這是normal server組裝SHA／大小或既有content-addressed blob完成收據，加authenticated角色metadata讀回；沒有遠端binary GET後重算SHA，也沒有atomic CAS、server批准或正式languages batch。

## 原BODY與歷史決策保留

舊review `00f2b388-712e-4886-9849-64e12e0f6bec` 由正常新final提交自然從pending成為superseded；其12refs、完整payload、原BODY QA11及null choice／note／decision均逐欄保留。七個舊獨有blob（BODY、preview、EN M4A、SRT、VTT、metadata TXT、EN縮圖）經正常PUT恢復，並由新版普通history附件提供live引用。只保留舊JSON不保證物理blob留存，因此另有[真實九hash map](branding-v4/history-actual-nine-blob-map.json)與[原生TEMP aged-GC證據](branding-v4/history-native-nine-blob-TEMP-GC.json)；沒有製造reserved renewal或伺服器核准。

舊BODY QA11、原EN94d4／560.505秒及其早期CC不被冒充成新版證據。舊[主體QA](qa-main-body-initial.json)、[EN歷次重錄／修詞](localization/en-production-history-snapshot.json)、[歷史字幕收據](localization/en-caption-assets-delivery-verification.json)原文保留；更新前23份文件與當時progress／result／task／index已[逐bytes封存](history/before-official-v4-docs/identity.json)。

## 當前音訊與字幕的驗收界線

EN以原來105個accepted raw快取做原生零新TTS包裝，100request groups重用；body.m4a完整SHA仍94d4、bodyPCM09df不變。實測fullAAC的586.510秒與較短bodyPCM560.433333秒分開，沿用原生一frame＋AAC padding規則；不是把推導的fullpresentation格點當作實測PCM。實際一次cached native check仍105 accepted／零旗／零unchecked，**沒有新ASR或Jev呼叫**；不冒稱整軌人工逐秒聽校。見[獨立105當前proof](branding-v4/EN-current-independent-proof.json)、[零TTS完成](branding-v4/EN-zero-new-TTS-native-completion.json)、[cached check完成](branding-v4/EN-cached-check-native-completion.json)。

ZH／EN新字幕採當前正式presentation一次位移，第二章原生00:29；EN用當前dub時間，ZH用narration，fullmetadata精確等於目前native pending payload。JA新manifest跟narration，保留一項stale harderror；ES4／PT2／ID2共8CPS亦保留。新版本這輪未另交EN縮圖，舊EN縮圖留在舊12refs與新history引用中，不把history縮圖稱成當前thumbnail_en。

## 尚未完成

EN完成一種外語的當前M4A／CC／標題說明增量交付；JA原句R1仍105checked／91accepted／14flags／0unchecked，未ready，其他六語音訊未完成。使用者預設八語是製作要求；真實歷史server `locales`快照仍為空物件，沒有偽造已勾八語或寫入任何choice。正式batch、全片QA通過及整體DOD都尚未成立。

敘事R1兩位fresh9/13 false及三項必要NO／章名advisory，與後續知情delta採用的教學取捨保留；官方239／123與公開release60／25、no halts proof只限公開release、未跑vendor Rocq、本地guard／loop兩個獨立例子等範圍未改。研究與YT文字快照未冒稱今日新查核或實看節奏。

更新文件前，source/native609檔及canonical1865檔均fullSHA重核相同；dirty JA i18n檔亦只記hash、不改不stage。文件更新後的progress／result／task等會有新hash；[舊609基線](branding-v4/before-documentation-source-and-canonical-preservation.json)與原026f／9ff／0be5嚴格helper保持歷史delivery scope，不宣稱它們的整份公共文件hash仍是新文件狀態。沒有任何paid、auth／API、媒體／state／cache／approval、合併／部署或YouTube操作。
