# Claude形式驗證255：繁中完整節目M4A已新增交付

2026-10-27T20:08:27.137379+00:00。已將當前官方片頭尾版的繁中完整節目M4A與實際使用說明追加到[本片後台](https://mokaair.com/zh-TW/admin/videos?video=claude-formal-verification-255)，同一待審final由23增為25附件。新音檔15950408B，SHA `f6edafd3ab0dc173a86ba4c8a9828ad2973b2ae2923f846f8e1d5791119ba42f`；AAC節目時長586.510秒，第一章後5秒片頭／21秒片尾保持。兩個新檔均完整下載後核對bytes／SHA／MIME，原23附件、完整payload／QA／choices及歷史審核保留。

從來源AAC抽出的初版M4A43e936eb…與manifest db8c735f…原樣保留。獨立解析原始MDHD／STTS發現初版容器把尾端時間正規化增加1tick；新副本只還原兩個32bit元資料欄位，實際只改offset315與586的兩個byte，其他每個byte、大小與offset不變。新檔raw STTS、MDHD時長及時間尺度、ELST／STSZ皆與來源相同；27491個AAC封包payload／時間／side-data／extradata及完整解碼PCM一致。這次沒有第二次remux、重新編碼或新旁白。

105句繁中當前音檔／完整intended／ASR接受證據只作來源繼承，沒有新ASR或逐段人工重聽。**外語仍EN1/8、JA14flags／stale、原生整片QA仍false10/11，八語與整片DOD未完成**。本次是繁中原版的新增下載格式，不計為第二種完成外語、不構成核准或語言批次。

[精確文字證據索引](receipts/original-zh-program-audio-20261027/index.json)、[還原後獨立實體查核](receipts/original-zh-program-audio-20261027/restored-physical-review.json)、[兩檔完整讀回查核](receipts/original-zh-program-audio-20261027/independent-two-file-readback-review.json)與[節目音訊說明](receipts/original-zh-program-audio-20261027/program-audio-original-timing.txt)分列範圍。以下原文是所標日期的歷史快照，23附件為先前狀態；當前新增格式見progress的`original_ZH_program_audio`。

---

# Claude形式驗證255：當前官方片頭尾版

最新核對（2026-10-27）：已補完目前待審成片全23附件的正常完整下載與ROOT實體驗證，含正式片頭尾版1080p、兩個英文M4A角色、繁中／英文實際CC與完整標題說明。105句英文現有音檢、fit與meter仍綁同一音檔；沒有新合成或核准，仍是英文1/8。[完整讀回證據](receipts/remote-binary-readback-20261027/README.md)。先前server組檔／角色metadata收據保持原日期與範圍。

[完整1080p、EN M4A與繁中／EN CC及標題說明](production-result.md)已直接交[該片Mokaair後台](https://mokaair.com/zh-TW/admin/videos?video=claude-formal-verification-255)並讀回。新main b635含官方5秒片頭／21秒片尾，current pending e66d共23roles。

**目前EN1/8；原生QA真false10/11，只captions未過。** JA14flags／stale harderror與8項CPS保持，整片與八語DOD尚未完成，沒有正式languages batch／server核准／YouTube公開。

- [當前23角色與hash](branding-v4/delivery-summary.json)、[主片／EN／歷史媒體安全摘要](branding-v4/main-EN-history-actual-delivery.safe-projection.json)、[雙語CC真實收據](branding-v4/CC-title-description-actual-delivery-receipt.json)。
- [目前QAfalse10](branding-v4/native-current-QA-false10.json)、[MASTER與EN105獨立音訊proof](branding-v4/EN-current-independent-proof.json)、[root接點實看](branding-v4/bookends-root-actual-visual-review.json)。
- [舊BODY七blob原生GC留存證據](branding-v4/history-native-nine-blob-TEMP-GC.json)、[文件更新前精確archive](history/before-official-v4-docs/identity.json)、[609來源與1865canonical保護](branding-v4/before-documentation-source-and-canonical-preservation.json)。
- [逐項progress](production-progress.json)、[語言狀態](languages-result.md)、[原文保留的本地化審查](localization-review.md)、[當前索引](public-receipt-index.branded-v4.json)。舊[索引](public-receipt-index.json)、QA11、失敗與重錄歷史保持原scope。

源e6e、claims527、speech8028、MASTER19ae與既有EN accepted targets／raw／ASR不變。原生零TTS包裝及cached105check沒有新ASR／Jev，不冒稱整軌人工逐秒聽校。Video17593/30與AAC586.510秒分列；舊bodyPCM沒有被改稱fullpresentationPCM。

使用者預設八語要求與歷史server locales{}分開記錄，沒有偽造選擇或核准。Source609文件更新前全hash相同；這裡的新progress等合法文字修改先archive，原026f／9ff／0be5收據作歷史delivery快照，不重標成整份公共檔案hash仍是current。Dirty JA只保留hash、不stage。
