# S60 R4｜片尾刪修的獨立史料與畫面覆核

2026-10-22 UTC。**PASS，限 R4 固定稿的史料、逐句對應與書面畫面；敘事雙盲、站台、語音、原生圖及成片關卡仍另算。**我未參與 R4 作者刪修。

## 凍結與精確範圍

| 檔案 | R4 SHA-256 |
| --- | --- |
| `brief.md` | `f177fe4e14067efb7cc8b6d0d1b817343c38ce5343271383ae8f9f7a48d4c8e1` |
| `research.md` | `e4ec4ac5abb2628d8c3efcabcf3a5beb8f33c5d2ce3ab92113e473a6bebd7689` |
| `claims.md` | `3a1bc97deb2be249b4b5fe2a90fd51f0d4ac8625c2e5fbc73a02e921276d6a88` |
| `script.md` | `f09ce432bfdec71135e44bc9ed3ad6f48119e95e01b2acd318fda13f8bda9dd1` |
| `video.json` | `c0a474072ffa37604dfe2acb9a46f600cac37c9815da5b4b692e213f560fd8ac` |

我以已推送的 R3 commit `97541461a` 獨立重算 [R3→R4 可逆差分](r4-author-structured-diff.json)各檔前後 SHA，並逐欄位比較 JSON：**唯一刪掉的場景是 s60107**（其旁白與書桌比較畫面一同移除）；唯一其他 JSON 改動是 s60008 的 loop payoff 由 s60107 指向仍存在的 s60106。其餘 108 個舊場景、另 10 個 loop、`brief.md`、`research.md` 和所有其他頂層設定逐字不變；沒有孤立的場景或伏筆 ID。R4 中 109／109 個 `video.json` 旁白、`claims.md` 列與 `script.md` 逐字相合；103 張插圖景、6 張卡。

## 留下的證據界線

Amundsen 固定 1912 全文 SHA-256 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`，L13063–13069 明記在小帳袋中留下給國王的信及給 Scott 的短箋。Scott 固定 1913 全文 SHA-256 `ddf48b1e0fc296b4862bad161bada2797a964ac6e6c7a0a7306a0a73940f8b26`，L16026–16028 明記自己**收下**阿蒙森的短箋和轉寄請求；L17316–17325 又記遺體與日記後來被找到。兩份固定文本都未在這些段落證明國王最終收到信。R4 保留 s60101「史考特收下短箋」與 s60106「兩份文本沒有追到國王信的最終送達」，刪去相鄰的 s60107 重述後，故事仍沒有把「收下請求」誤說成「送達國王」。s60106 的搜救者取日記畫面與文本所記日記被找到相符，未畫出不存在的送信結果。開場 s60008 的證據終點提問仍可回收到 s60106。

實跑 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s60 --json`：**0 errors／0 warnings**，109 句，10.6178 分鐘正文估算，第二章 00:46 開始，故濃縮開場仍估 46 秒。原生語音的實際長度尚未量測。R4 是否解決唯一剩餘的 `no_recap` 敘事票，須由未見 R4 改稿的新讀者正式評定。
