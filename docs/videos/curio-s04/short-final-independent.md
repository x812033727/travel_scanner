# S04 Short 1 成片獨立查核：PASS

- 查核日：2026-10-20 UTC
- 對象：`/workspace/.video-work/curio-s04-short-1/e89657a84d2c3596-1792522794968`
- 結論：**六拍史料、原鏡頭、成片抽幀及四語字幕 PASS**。本結論只適用於下列雜湊綁定的檔案。

| 檔案 | SHA-256 |
| --- | --- |
| `docs/videos/curio-s04/shorts.json` | `ad4b76c3ee6a57db4abe85554ce027c1aa1ea2d3e68dc3e89251cd65a25283c4` |
| `docs/videos/curio-s04/short-preflight-3.md` | `b65b9d8f774c4600fba5f407bbd38b226ca4281516a74190423e21f19cea0d76` |
| 候選 `script.json` | `110eb081f873c34c15aef84c1d1fef09bd74d31a1fcbb780c2e24bfa4284f56b` |
| 候選 `verify.json` | `8aca90d26252e5d16d6b519ea3ad9395c29832d345935b49c4b2274351f7777d` |
| `upload/final.mp4` | `e3f496b0ad6b9cab5b338b62724991d1ad1b840312f7ad0544572a245938242a` |
| `contact-sheet.png` | `4da798d05fd1d74fd6951f27e342777ef5b6d4a51c8de08b5b428303667cc8d5` |

## 史料與鏡頭

逐拍比對原企劃與生成 `script.json`：六個 beat 的旁白、標題、順序及鏡頭素材一致。`verify.json` 的 `document_sha256` 等於上表的 `script.json` 雜湊，六項史料聲明均為 `ok: true`。第三版獨立預檢對讀固定版《三國志》卷五十四及《三國演義》第 57 回，確認「巴丘病卒」出自史傳、諸葛亮來信及臨終長嘆屬小說，並把病名未知的範圍限於所引史料。六張長片原關鍵影格均存在，逐張 SHA-256 與 `script.json` 的 `evidence` 欄相符。

候選 `check.json` 記錄六句語音均通過聽辨、零句標記；`checks.json` 記錄證據影格核驗通過、1080 × 1920、30 fps、880 幀、29.333 秒及六景動態。這裡引用的是工具檢查紀錄，沒有另做人工全片聽辨。

## 成片畫面

以原尺寸檢視 `contact-sheet.png`，另從 `final.mp4` 原生擷取並檢視 2.0、12.5、21.5、27.0 秒四幀。標題及繁體中文字幕清楚可讀，位置避開直式短片上下介面安全區；人物、書本及場景屬卡通示意，沒有可被誤認為史料原件的偽造可讀文書。接轉瞬間的標題有淡入效果，抽看的實際成片幀能見完整標題。畫面抽查無待修項。

## 字幕

本地 `caption-validation.json` 逐 cue 對照 `timeline.json`：繁中、英、日、韓各六句，起點皆為 0 毫秒、末句止於 29,333 毫秒，四語時間碼均與 30 fps 時間軸相符，錯誤數為 0。繁中六句與原旁白一致；三種譯文保留小說與史傳的區別、巴丘病卒、未載病名及史料未把諸葛亮列為發病原因。英文第 4、6 句的語意歧義已在此版本修正，現寫明「four Chinese characters」及「do not name the illness」。

| 字幕 | SHA-256 |
| --- | --- |
| `upload/zh-TW.srt` | `d5b5b5c973fb26d8e97615196bf7ba0aca4ef98bb74e10fe471e308286dfb6d9` |
| `upload/en.srt` | `52e88cd61198e487d248e702908571f7ae9c6bdfd15309c76c31b6704401776e` |
| `upload/ja.srt` | `0dcdc0bb421261dd976eb7f1f4afa50a88d49239f60aebd8a1cc39ac1d773c1c` |
| `upload/ko.srt` | `f4c91e893b1189d23e36db5587b88265146dc1ae74711bc3e42f83d6689251e1` |

此 PASS 只涵蓋上述候選成片、史料與字幕；站台短片 QA、長片連結與發佈狀態須依各自的實際讀回及檢查結果記錄。
