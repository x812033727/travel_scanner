# E2 替妳著想｜完整繁中聲音與剪輯交接

## 故事前提

接E1附件疑問。知棠逼承川讀出受託人與表決權，確認文件由他提供；見證人員封存含附件完整未簽原件、交保管收據並帶回保管。知棠保有E1完整副本，未交許聞。舅舅最後同意解釋，但要求先關掉相機，未演出眾人服從。

## 角色

知棠28歲Kore、承川31歲Puck、崇岳57歲Charon。完整基底、voice style、shot_looks直接由productionSetting產生，Kore/Puck與E1完全一致。Charon沿低緩家常表演及各句emotion；本集無旁白台詞。知棠每個現世鏡頭都是婚紗無頭紗，唯一銀方錶留腕；見證人員僅既有成人手部、沒有speaker。知夏、禮袋、母親、許聞皆不入鏡不出聲。

## 站主觀點

先優化並製作前兩集繁中影片與可開關繁中CC。完整繁中全片與CC必須由使用者本人確認後，才啟動日韓英；兩集、pilot或自動品管均不能代替全片確認。錄音與計畫不是動畫成片，正常演出較短就縮短，不加速、不停格、不慢唸、不添同義台詞填秒。

## 執行

本voice文件只有34句、34個有聲scene，供既有TTS CLI使用；原41鏡與7個無台詞動作鏡仍保留在episode-02-dialogue.json。原件核對、封袋、填收據、收據交接與見證人保管去向不可因不在voice runtime而從影片刪除，也不能替無聲鏡頭製造假台詞。178秒是完整editorial規劃，不能當成聲音測量。

root把episode-02-voice.video.json、episode-02-brief.md、episode-02-series.json複製至repo外runtime/episode-02/的video.json、brief.md、series.json，核對來源及費用守門後執行CLI --file。逐句runtime_id固定映射在episode-02-dialogue.json；無audio_ref，不借E1錄音替本集新句。

畫風沿E1 anime-2d、線稿／克制賽璐璐與同一象牙白冰藍婚宴場景。對白、音效、環境和音樂分軌，CC可關、無燒字。本地轉檔未發出付費請求；本稿不代表後台已採用、動畫可直接render、聲音或字幕已驗收。
