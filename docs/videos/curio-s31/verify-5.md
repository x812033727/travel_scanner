# S31 R4｜相鄰重述修稿交接（五）

2026-10-20。R3 的全新、只看文稿與官方題目的盲讀為 12/13 YES；唯一未過的 `no_recap` 指出 ly037／ly038 連續說「味未變已至京師」，以及 ly052／ly053 連續說廣州土貢荔枝。獨立回執封存在 `/tmp/curio_s31_r3_fresh_narrative_blind.md`。本頁凍結 R4 修稿，**尚待全新官方 13 題盲讀及獨立來源／96 景提示詞核查**。

## R4 exact hash

| 產物 | SHA-256 |
| --- | --- |
| script.md | `899dd8510fbd1a45e0596682df38c6ea18600c356681369ff2ffbde36d56c592` |
| video.json | `8ebe96c889a8bb20d0d2e341864e7d037232eed0da015df035a924c3c8cd0a86` |
| claims.md | `eae4a0838b10184975ec50e747934db18659befc67c8eba9a761b73d88fd970b` |

R4 沿用 [research.md](research.md) 所列固定全文、原句與證據上限，未引入新史料或指定果園、逐站路線、日數、品種或保鮮辦法。

## 兩處敘事修訂

| 位置 | 舊稿問題 | R4 句子及推進 |
| --- | --- | --- |
| ly038 | ly037 已引「味未變已至京師」，下一句又解釋抵達時味未變。 | 「我翻回杜牧的宮門：史書有沒有接上這一幕？」立即把兩頁並排，讓 ly039 查兩頁有無同一抵達場景。未把杜牧詩馬與傳記騎傳指成同一匹。 |
| ly053 | ly052 已說廣州條有土貢「荔支」，下一句又換字重說貢品事實。 | 「我把地理志和貴妃傳擺到一起，先找同批貨的記號。」進行批次核對，讓 ly054 回答廣州條不能指定貴妃收到的那批果。分鏡改為一人把兩卷閉合書卷並排，圖中不生文字。 |

## 本地核對與下一關

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`：0 errors、0 warnings；估全片 9.3 分鐘，片頭 45 秒，正文約 8 分 30 秒。
- 逐項比對 script、claims、video：97/97 ID 順序與旁白字串相同；96/96 正文 still shot；10 條不同 setup 的前向 loop。
- `npm run test:docs-videos`：236 pass、0 fail；`npm run check:tasks`：exit 0，其他工作票仍有既存警告；`git diff --check`：無空白錯誤。
- 全新、未看舊回執與研究檔的讀者須對本頁 **script SHA** 完成官方 13 題盲讀；另一位獨立讀者須對本頁 **script／video／claims SHA** 重核來源與全部提示詞。舊稿的 12/13 不能沿用。兩關未完成前不配音、生圖、配樂、合成或進行其他付費媒體。
