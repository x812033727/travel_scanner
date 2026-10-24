# S53 R19｜第二章八景一次原生試畫與停批

2026-10-22 UTC。**本批已結束：6 張 KEEP、1 張原圖 REJECT、1 景供應商拒絕且無原圖。**後續同景重畫先由作者窄修、另一位工作者按新雜湊紙審；本回條不是整章插圖、分鏡站台卡或成片核准。試畫綁 `video.json` SHA-256 `62254351988dae8424e0d94bb136a6b7171e5d991f2c9962508af03fc7248c3a` 與[R19 獨立紙審](r19-next-chapter-eight-prompt-independent-pass.md)。我未改創作檔；每景以 `--shot <ID> --takes 1` 單獨呼叫，在一次呼叫前暫移本集 `STOP`，由 EXIT／`finally` 立即恢復。付費 MiniMax 端點已釋出，無背景命令或待完成 job。

每個成功產出的 **1280×720 原始 JPEG** 已逐張原尺寸檢查；`s53015/17/20` 另外檢查工具選用的裁切 JPEG。選圖檔 SHA、機器評審、八個舊首章 KEEP 的 request key 與檔案 SHA 及前後帳本逐項見[原生盤點 JSON](r19-next-chapter-eight-native-inventory.json)，SHA-256 `8757c41c6329072346813e834ffb1db394663e44e70f40432d0dba13b693ac80`。

| 景 | 機器與原圖結果 | 人工判斷 |
| --- | --- | --- |
| `s53010` | judge **FAIL 9/10**；原圖 SHA `3b467df02bfa6f78375f2105dc31cb28d64e89a20c03de8b4b2844c6b2fa2390`。 | **REJECT。**畫面前景是較一般漫畫比例的成人，背景明顯有現代汽車與街燈；1906 地震大火場景不能用。作者只窄修這景提示詞，改用近景成年住戶與煙霧、1906 街屋局部，避免能生現代車陣的長街透視；旁白、來源、運鏡不用變。 |
| `s53011` | judge **PASS 9.29/10**；原圖 SHA `812d2941450d2a57d5c11c928b5d4514859723fa491efc779a26aac11207b406`。 | **KEEP。**灰髮成人抱寢具走向廣場，旁邊有人在裸地休息，符合首夜暫居。毛毯落在地面而非搭在杆上，是提示詞動作偏差；旁白只說失居者先到公園／廣場，不因此變成相反史實。 |
| `s53014` | judge **PASS 9.29/10**；原圖 SHA `290c0b20d56f3acd3168e1c749bb243580504613c5062c48abba11cf43199b4d`。 | **KEEP。**灰髮成人在帆布帳前拉開兩片門襟，沒有照提示詞「重新繫門襟」，但帳棚可暫避雨休息的旁白仍對應；無窗光或已建小屋。 |
| `s53015` | judge **PASS 9.29/10**；原圖 SHA `c3ab77568ab17d7aedb1bd1437bbfa23424fe41755e49a2f7d9cab751a470c6d`，選用裁切 SHA `2e63e543f40b7dc000fd1a00dfd42c25f0cac7d53fd6dc58818436a589e728a9`。 | **KEEP。**灰髮成人在帳棚前，天空有雲，沒有把尚未到的雨季畫成暴雨；人物未仰頭只屬視線偏差。 |
| `s53017` | judge **PASS 9.29/10**；原圖 SHA `567441958c7a77b8110b13bf6beb6953ec8cd180c4ba41fa1cd890cc0d85f60b`，選用裁切 SHA `40170d8eb8c2b63517c8a455257a58ec377a03d24d592e1409807e7dc548f278`。 | **KEEP。**兩位成人在仍只有帳棚的空地指示位置，沒有把「決定蓋」畫成已動工或假建築圖。兩人都指、其中一人不顯灰髮，是非關鍵提示詞偏差。 |
| `s53018` | 供應商回 `input new_sensitive`；**沒有原圖、沒有 judge**，manifest `needs_review`。 | **HOLD。**未得圖，無從驗收。提示詞含英文 `South Park`；與卡通風格組合可能觸發名稱敏感過濾，這只是待測推測。作者可保留旁白「南公園」，但把畫面提示詞改成「1906 San Francisco small public relief park」等通稱，仍畫狹窄帳棚間裸地；另人紙審後再試，勿原字重送。 |
| `s53020` | judge **PASS 10/10**；原圖 SHA `85075d310d7ef026613c03a4ca970392997d6522117aa9ad69385e21e9ab0913`，選用裁切 SHA `1954d9dd33a86bfd87b6b6deda88580e0fd568b1dfd26eadc7f24c8212aa626e`。 | **KEEP。**灰髮成年職員面向群眾說明，背景只有帳棚，沒有偽公告文字或提前出現小屋。群眾造型不作可識別個案。 |
| `s53021` | judge **PASS 10/10**；原圖 SHA `2dde34b31fe93a2b676df73dc25fa8304d13413e56aa8560824f2c9cff438bc1`。 | **KEEP。**成年工作者在帳棚邊望向公共街區，沒有假地契、可讀標牌或所有權界線；「公地但不歸救濟機構」仍由旁白解釋。 |

**帳本與快取：**前 `US$0.3105／23 images／23 judges／0 reservations`，後 **US$0.4050／31 images／30 judges／0 reservations**，增加 **US$0.0945**，低於整集 **US$4.78** 上限。七景成功生成與評審各付 `US$0.0135`；`s53018` 失敗記作一次 image attempt，**US$0、無 judge**。後帳本 SHA-256 `e4761e22531131c77d9dbae201af16c822afad5c6bdf58d013395b16e6f68c69`；manifest SHA-256 `eafb17ba8426f1c6e79c263bed1bbfcb73f896bc8150b54cff3033e7cf9f0f66`，16 條目（首章 8、本批 8）。私有 `media/jobs.json` 的 `jobs` 為空，`STOP` 已恢復。首章 `s53002–09` 八個原 KEEP 的 request key 與選圖 SHA 均未變、物理檔案 SHA 核對通過；`s53007` 仍重用 `s53003`。

CLI 後六次即使本景 judge PASS 仍回 exit 1，因 `s53010` 的 `needs_review` 會使整份 manifest 回報未完成；逐景 PASS 以該景 judge、原圖及 manifest 條目為準。Playwright Chromium 版本不符令聯絡表未重生；本回條以逐張 1280×720 原圖／裁切檔驗收，未把聯絡表缺席寫成通過。這一批只有一張現代車原圖與一個無圖的供應商拒絕，尚未達「三個相關原圖缺陷」提早停批線；八景一輪結束後正常停止，下一步只修 `s53010`、`s53018` 的提示詞再交另一人紙審。
