# S28 Short 1：七歲究竟寫在哪一段

查核日期：2026-10-20。腳本為 [shorts.json](shorts.json)；本輪只完成文稿與已製作插圖的唯讀驗證，沒有合成 Short 旁白、組片或付費媒體呼叫。

## 事實與界線

- 鉤子只問「破甕時真是七歲？」。《宋史》卷三百三十六〈司馬光傳〉固定轉錄在 [research.md](research.md) 標為 [S]：七歲是「聞講《左氏春秋》」，後面的「光持石擊瓮破之，水迸，兒得活」沒有另記救人年歲。故結論限定為「不能確定恰好七歲」，不補事故日期。
- 鏡頭 `jar-009`、`jar-010` 是已完成長片的 AI 卡通救援示意；所畫甕的破口位置不是古書提供的實物細節。`jar-017`、`jar-019` 畫讀書，`jar-020` 畫讀者查頁。這些圖只服務敘事，不冒稱庭院目擊或宋代原畫。
- 描述欄的《宋史》連結固定到 `garychowcmu/daizhigev20` commit `4a6d6f2088825f132521d848c2ea86cf9c9a7620`。完整長片目前沒有 YouTube ID；`source.url` 留空，製作上架包時須從站上取得公開地址並放在說明欄第一行，Studio「相關影片」亦須另設。
- 主代理另請未參與本短片撰稿的讀者依 [claims.md](claims.md) 與 [research.md](research.md) 獨立核對，確認「七歲」接讀書、救人段未重標年歲，且取用的原片鏡頭不扭曲此界線；回報為 PASS。這是文稿史料覆核，並非新配音或成片的品管結論。

## 靜態驗證

| 項目 | 結果 |
| --- | --- |
| 來源長片 `video.json` SHA-256 | `e2dfad03599dfa9767ec72073cef67ba74e145ef01d59febcf2243832fc00bde` |
| 短片 `shorts.json` SHA-256 | `97c5593e6af7e66efef815e7e7fec97850df7ba17fafa1f33b3b0d06340229dd` |
| 成片使用的 keyframe manifest SHA-256 | `549576311bcea7dc29f211ba7e17058530c9b0e23cc11a91b873fa70c9e9dc90` |
| 腳本 | 1 支、6 景、8 句、127 個含標點字元；以長片配音字速估約 33 秒，正式 25–55 秒須等 TTS 實測 |
| 影格 | 6 景均為原片 shot，轉成 5 個唯一 keyframe 證據檔，逐檔 SHA-256 與 manifest 一致，無 `needs_review` |
| 格式與後設資料 | 單支 `validate` 零錯；繁中說明欄含來源與片長連結預留欄位，按已有 URL 模擬時 metadata 零錯；無被禁用的訂閱／按讚／點連結呼籲 |
| `from-episode --check` | `curio-s28: 1 Shorts valid; every keyframe matches its hash`；6 景中的 5 個唯一影格逐檔驗證通過 |

正式檢查使用已提交的 Curio 單支驗證器 `68dbe714`，命令為 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/shorts/cli.mjs from-episode --slug curio-s28 --check`；相關單元測試 7/7 通過。正式配音、字幕、QA、上架包與站上審核都尚未執行，不能把此文稿當成已完成的 Short。
