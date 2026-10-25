# S58 R8｜開場時序與兩球重述窄修作者凍結

2026-10-21 UTC。**R8 作者候選，尚待非作者來源／書面畫面覆核及兩位新盲讀；沒有網站或媒體核准。** [R7 正式敘事合併](r7-merge/summary.md)保留兩位讀者共同 `no_recap` NO 的 12／13 HOLD；[R7 獨立來源 PASS](r7-source-independent.md)只適用其舊五檔。

| R8 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `35c33785728e092c6f4d4a22c9076f05cee92b7bdde36ca2563cad2db0fb142b` |
| `video.json` | `aa7415ade3e74e658a21fdf953eae7d7867c6f65cad62b224c03e203c2dbb390` |
| `script.md` | `d9bd044c1261ab76f3ad32a098e8c50aadfc05473d223aac3d61a621223afd6d` |

## 依 R7 原票修訂

- `s58006` 不再在開場說郵袋已出城；改問同一吊籃的郵袋與鴿子為何任務不同。`s58010–11` 仍先升過屋頂、再鬆開地面繩索。該景的書面提示詞也改為仍被繫住的吊籃；逐句表補了十月鴿郵 [R759–792](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L759-L792)。
- `s58034–35` 先用「另一球／自己那球」講不同負載，`s58037` 卡片才第一次給兩球名字；`s58042` 改講分裝器材沒能隨他抵圖爾這一後果，不重列郵袋、鴿子、機器。`s58042` 逐句表增 [D119–140](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L119-L140) 以連結另一球被俘的自述。
- `s58043` 刪去無從回答的另一球乘客命運旁枝，改回達格隆的球在空中準備處理壓艙沙；`s58044–45` 接舊袋能否撐住與棉布袋破裂。`s58043` 的書面畫面改為一位飛行員抓壓艙沙袋，不畫未記載的乘客傷亡。
- `s58144` 不再緊接重唸六天，改問達格隆另記的單趟鳥程長度；`s58145` 回報普瓦捷至巴黎十二小時，`s58146` 仍只說這不能量出每封私信的到達時間。

八處口播在 `video.json`、`claims.md` 和衍生 `script.md` 同步；兩處書面 shot 提示詞另隨口播修正。研究、企劃、其他場景、系列風格、20 組掛鉤、配樂及片頭片尾設定保持原內容。146 景／141 個 `shot`／5 個 `big`，濃縮開場 185 漢字，六章正文 2653 漢字；按每分鐘 325 漢字約 **8.16 分鐘正文**，最終以 TTS timeline 驗證。`lint --slug curio-s58 --json` 0 error／0 warning；`npm run test:docs-videos` 在本輪七處主要修訂後為 **236／236**，最後一處 `s58145` 只刪重複副詞並重產劇本；`npm run check:tasks` exit 0。沒有語音、插圖、配樂、合成、站台核准卡或上架。

下一關：由非作者覆核 R8 五 SHA 的來源、逐句表與所有書面提示詞，兩位新讀者只讀本版劇本投 13 題；正式固定 OR 合併前，不能沿用 R7 票或開始付費媒體。
