# S47｜R3 敘事退稿與 R4 作者修訂

日期：2026-10-20。[R3 來源／書面畫面獨立查核](review/r3-source-independent.md)對當版判 **PASS**，但兩位真正全新的盲讀者在相同 R3 SHA 上分別答 [A 9/13](review/r3-blind-a.md)、[B 10/13](review/r3-blind-b.md)。兩人共同把必答 `no_spoiler` 和 `no_recap` 判 **No**；A 另判 `one_line`、`payoffs` No，B 另判 `no_toc` No。正式規則下 **R3 敘事 FAIL**，理由及原版 SHA 見 [verify-4.md](verify-4.md)。R3 的來源 PASS 不能移用給 R4。

R4 只修同一條順時序故事的鉤子與重複，固定 W／N 文本及「小冊轉錄電報 57 秒、奧維爾後述 59 秒」的不同見證層次不變。

| R4 改動 | 作者自查的來源與敘事界線 |
| --- | --- |
| `wr004→wr030` | 開場改停在 1903 年返營後馬達初次裝機帶動螺旋槳，問那批軸能否撐住；`wr030` 才報最初軸的缺陷。開場畫完整的軸，不預演裂痕、延期或後來的第二次斷軸。1902→1903 的「隔年」接 [W590–605](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L590-L605)；初次裝機試轉接 [W648–658](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L648-L658)。 |
| `wr005→wr048` | 開場只見 12 月 14 日威爾伯俯臥在坡上的**動力機**，問落點；坡上抬頭與落得比起點低等結果留到正文。書面畫面標明雙層翼、後槳、滑橇，不畫成無動力滑翔機。[W713–748](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L713-L748)。 |
| `wr008`、推薦 A | 開場接回「誰能替他們造出合用的引擎」的一個未解問題，不再羅列引擎、斷軸、大風等後續章題。`brief.md` 推薦 A 的鉤子同步改到結果之前。其餘相機／電報問題也只問而不先揭結果。 |
| `wr014` | `wr010` 已給八匹／兩百磅門檻；此處改講兄弟先前僅造過一具**帶動車行機械**的汽油機，新增工作經驗限制，不再重說門檻。書面畫面只示意店內馬達。[W527–535](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L527-L535)。 |
| `wr086–087` | `wr086` 交代前舵支架破損、主體未傷；`wr087` 才給奧維爾「一兩天可修」的當時估計，並問是否還有下一趟。後景不再重複損傷，也不預演已修理；陣風在 `wr088` 才打斷計畫。[W852–859](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L852-L859)。 |
| `wr093→wr095` | 問題縮為「後述的最長時間與小冊轉錄電報相同嗎」，下一句明答 **59 比 57 多兩秒**，再把「傳送時弄錯」明歸於小冊作者。手上未核 1903 年電報原紙，不能據此判兩份文本哪份原件更準。[W852–853](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L852-L853)、[N1613–1634](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1613-L1634)。 |

## R4 凍結候選

| 檔案 | SHA-256 |
| --- | --- |
| [brief.md](brief.md) | `66e12a21ae3db888465b89c8f44fb3ad526fbef579cbb1f10df95058161c53c8` |
| [research.md](research.md) | `493d6bf8e73d9832c05300b2c9643e7e53c1448ac2215c54e2f32f9ad10fa357` |
| [script.md](script.md) | `05ed37be99315eacc277ba2edc492745f20ee33ea332dcdc6c36977f0a2b93c3` |
| [video.json](video.json) | `0257b051d4df91a73626a8cf37368363286db4cc1a149f8fb1aff51c4085556b` |
| [claims.md](claims.md) | `6a087fba94b520c78b3d2ba636a7041e6f51cca23ded1b1a32365072278eadf1` |

固定參考文本未變：W `/tmp/s47-wright-25420.txt` SHA `1cbdc94a6e6851df735fb7171e7ed8d08608c44964237266fac93c2f71e2308c`，N `/tmp/s47-wright-nps57725.txt` SHA `546d76a2ea15dfa0317427b56e0b31e42d3f867f7ef465c82e70e3971e7d1d5f`；其可重取版本見 [research.md](research.md)。

作者機械自查：已從上表 `video.json` 重生 `script.md`；97/97 正文景有 `shot`，100/100 句（含三句片尾）與 `claims.md` 按 ID、順序及口播逐字一致；115 個 W/N 固定行段連結均在文本範圍內；14 組伏筆的設置與回收 ID 均存在且先後有效。`lint --slug curio-s47 --json` **0 errors／0 warnings**；`git diff --check` 無格式錯誤。靜態開場按 250 口播單位／分鐘含停頓估 **57.33 秒**，按 325 估 **45.97 秒**；後者正文 `wr009` 到片尾前約 **492.5 秒（8:12.5）**，純正文口播 2178 單位按 250 估 **522.72 秒（8:42.72）**。這是靜態估算，**尚無 TTS 實測**；原創 5 秒片頭、21 秒片尾及最後約 16 秒推薦／訂閱框仍為製作規格，未組片或啟用連結。`npm run check:tasks` 驗證 2117 份任務檔；既有任務持有時間與範圍重疊警告未指向 S47。

R4 **只完成作者修稿與自查**。仍須另一人對上述**精確 R4 SHA** 重做來源及書面畫面差分，再由兩位真正全新、互不相見的讀者各按官方 13 題盲讀；不可沿用 R3 評語。推薦 A 只存本機企劃，S47 尚無網站大綱／劇本核准，也沒有付費語音、原生插圖、配樂、成片或上傳。
