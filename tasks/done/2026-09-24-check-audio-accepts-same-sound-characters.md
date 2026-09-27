---
id: 2026-09-24-check-audio-accepts-same-sound-characters
title: check-audio accepts same-sound characters and filler words; tts --redo retakes only flagged lines
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T16:18:22Z
created_at: 2026-09-24T16:18:14Z
completed_at: 2026-09-25T01:20:41Z
branch: claude/video-redo-lines
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/requests.mjs
  - tools/video/tts/synthesis.mjs
  - tools/video/tts/tts.test.mjs
  - package.json
  - package-lock.json
---

# check-audio accepts same-sound characters and filler words; tts --redo retakes only flagged lines

## Why

試作片第一次完整跑 `check-audio`，157 句裡 Jev 標了 28 句。其中 8 句只是轉寫寫成同音字（它／他、付／負、計數／技術、級聯／吉蓮），Jev 自己說中文準確度沒有公布，分不出來；另有 5 句是 Gemini 的口語風格自己加的語氣詞（啊、喔、欸），站主 2026-09-25 選擇保留。這 13 句每跑一次都會被標，重錄也消不掉。

`tts --redo` 又是整個場景重合成（一個請求一個場景），cost-table 有 24 句，為了一句重錄會把其他 23 句已經通過的也換掉，Gemini 每次念得不一樣，於是永遠收斂不了。改一句的文字也一樣。

## Definition of done

- [x] 只差同音字（含聲調比對）或語氣詞的句子不送 Jev，摘要分開計數；聲調或讀音不同（旗 qí／期 qī、答／打）仍送 Jev。
- [x] `tts --redo` 與改文字只重錄那幾句，每句一個請求，同場景其他句子保留原音檔；整個場景都沒有可用音檔時才整段合成。
- [x] 舊的快取（以請求為鍵）照樣算數，並改寫成每句自己的鍵。
- [x] 試作片實際跑通：28 → 15 → 7 → 4 → 1 → 0 句被標（其中 4 句改寫措辭），重錄共 473 字。

## Steps

- [x] `check.mjs`：`matchKind`（exact／filler／sound）、`reading`（pinyin-pro，數字聲調）。
- [x] `requests.mjs`：每句的 `key`（聲音設定＋該句的 parts）。`synthesis.mjs`：`synthesizeLines`、`lineBody`。`cli.mjs`：`retakes`、快取遷移。
- [x] 測試：同音字／語氣詞／聲調不同的實例（試作片的真實配對）、`--redo` 只送一個請求且同場景的音檔位元組不變、舊快取遷移、改一句文字只送一句。
- [x] pinyin-pro 3.29.4（MIT、無相依）加到根目錄 devDependencies。

## How to verify

```bash
node --test tools/video/tts/check.test.mjs tools/video/tts/tts.test.mjs
npm run test:tools
```

## Notes

- **lockfile 手動插入**：本機 npm 11 的 `npm install` 會把 package-lock.json 裡不相干的 `libc`、`peer` 欄位改掉（88 行刪除），所以還原後只插入 pinyin-pro 的兩處（根的 devDependencies 與 `node_modules/pinyin-pro` 條目）。
- pinyin-pro 對繁體字、破音與「一」的變調處理一致（兩邊都經過同一套），實測試作片的 17 組配對判斷全對；祝／助（zhù）也算同音，檢查會放行。
- 語氣詞只收「啊喔哦欸誒嗯呃」：「耶」「吧」也是詞的一部分，不收。重複字（「那我我自己」）不是語氣詞，仍送 Jev。
- Windows 本機跑 `test:tools` 偶爾在 `atomicWrite` 的 rename 遇到 `EPERM`（防毒或索引暫時鎖檔），重跑就過；記憶體不足（Edge 截圖同時跑）時一堆不相干的測試會以 `VirtualAlloc failed` 失敗。CI 在 Linux，兩者都不會發生。
