# S07 Short 1：橋不是喊聲震斷

2026-10-20 的零付費文稿預檢。腳本為 [shorts.json](shorts.json)，SHA-256 `c2f33fbcfdd192d017a23bf24021c3e55570e4c7b5fa3c1e036bde6d600bbd5b`；來源長片 `video.json` SHA-256 `ba6bfc13ad087665a9f68eec94f33cb46b795e6ed5eaf91164a08d73705b2426`。本檢查不生成短片旁白、圖像或影片。

## 單一事實與文本界線

核心只回答「張飛是不是把橋吼斷？」。[research.md](research.md) 的固定《三國志》〈張飛傳〉原文有二十騎斷後、「據水斷橋」、報名邀敵決死、敵不敢近；沒有聲音震橋、拆橋時刻或施工者。固定《三國演義》第四十二回才敘退敵後張飛**命人拆橋**，又寫劉備責備這一拆讓曹操知道林後沒有伏兵。Short 每次換文本都明指史書或小說，不把兩書拼成一趟可重建的實際戰場。兩條固定史料連結已列於腳本的 `links`。

主代理另請未參與這支短片撰稿的讀者對照 [claims.md](claims.md) 與 [research.md](research.md) 進行來源抽核，結果 PASS：二十騎、斷橋、單句挑戰屬 [SG36-ZF]，退敵後拆橋與劉備憂心露餡屬 [YY42]；短片沒有把小說動作說成正史。此結果只核文稿，不代表未生成的影格或成片已驗收。

7 景依次使用原片 `bridge-032`、`031`、`033`、`037`、`075`、`078`、`032`。`bridge-075`、`078` 的插圖提示詞含小說書頁框；其餘史書橋頭與現代查書示意不冒充現場影像。全部 ID 都存在於原片的 `shot` 場景。

## 預檢結果與待補關卡

- 純 `validate` 與 Curio 單支 `episodeShortsProblems` 都是 0 問題；6 拍依序且有回環。7 景、8 句、138 個含標點字元，句長最多 20 字，第一張字卡標題 8 字；按已核長片口播字速推估約 35 秒，正式 25–55 秒仍須等 TTS 測量。
- 沒有被禁用的按讚、訂閱、點連結等呼籲。以有效長片 URL 模擬合成後設資料，`metadataProblems` 0 項、繁中說明 785 UTF-8 bytes；正式說明欄第一行完整影片 URL 仍待長片私人上傳並取得 YouTube ID。
- S07 尚無 `keyframes/manifest.json`。待 S26 釋出共用生圖時窗、S07 正片 86 景完成全尺寸驗收後，才跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/shorts/cli.mjs from-episode --slug curio-s07 --check` 綁定影格雜湊。Short 的 server TTS／build 應在正片站上成片關卡及語音預算可用後進行。
