# S53 R22｜地震日來源卡與南公園窄景作者候選

2026-10-22 UTC。R21 [兩張原生圖停線](r21-two-native-stop.md)後，只改 `s53010` 與 `s53018` 的畫面欄及 `claims.md` 對應兩列。**作者候選，待非作者以新雜湊重開史料及書面畫面覆核；沒有新付費呼叫。** 126 句台詞、`script.md`、章界、其餘 122 景、畫風與配樂設定均不變。三張已拒收的 `s53010` 原圖和兩張已拒收的 `s53018` 原圖不能當作合格圖。

| 景 | R21 原生圖結論 | R22 方案與來源界線 |
| --- | --- | --- |
| `s53010` | 第三／最後一張原生圖有上下黑邊；裁圖雖去黑邊，人物靠右且未佔主要畫幅，正式 judge 9／10 FAIL。此景不再買第四張。 | 曾比較同章六張 KEEP：`s53011` 是災後首夜、`s53014/15/17/20/21` 是較後的夏季營地或建屋安排，套在 **4 月 18 日清晨** 會混淆時點。因此改為 `big` 資訊卡「1906 年 4 月 18 日｜舊金山／地震之後，又起大火／1913 年《舊金山救濟調查》回顧」。固定 1913 年原文 [L1438–1465](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L1438-L1465)直接記 1906-04-18 05:12 地震及火勢；卡片不冒充現場畫面或當年文件。 |
| `s53018` | 第二張原生圖為卡通人物配照片質感帳棚、人物正面全身、通道寬，正式 judge 9／10 FAIL；人工 REJECT。 | 新提示詞只留一名銀髮成年工作者、一個側身擠過兩道相鄰素色帳棚牆的動作、近景胸肩與帳棚佔滿邊界；減少帆布細節和遠景，以避免 R21 的照片質感及寬通道。固定原文 [L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)只支持南公園面積不足以容納分開小屋；狹縫是明示的原創概念示意，不主張實際帳棚間距或營地平面圖。書面覆核若通過，最多再做 **一張第三／最後原生圖**，逐張看 1280×720 原圖和裁圖。若仍失敗，停畫並由另一人評估同章已收圖重用或來源卡。 |

固定 1913 年 *San Francisco Relief Survey* 原檔 `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，與 [research.md](../research.md) 相同。`s53010` 卡片引文是旁白概括，未加未見於原文的具體火災地點或人物；`s53018` 提示詞不把概念示意當原始照片。請獨立審者直接重開這兩段及兩張先前原圖；作者判斷不等於獨立 PASS。

[可逆精確差分](r22-two-scene-structured-diff.json)含兩個場景完整舊／新物件與 `claims.md` 兩行舊／新文字；用新字串反向替換可逐位元組重建 R21 `video.json` SHA `4ac9a518d7387ea66918a89946636ee7dd6412f4926fbe7c5ccbb5a5a249f64a` 與 `claims.md` SHA `02ee7918a362ce130bed4a9e2c1491f0da80880207d7c57d6aa9eae1820a3022`。R22 `video.json` SHA **`49bdd04e5ebb88ff98cd207c6da0545faf1d1721834a0dc099d514a2daf9fa99`**、`claims.md` SHA **`34f765eee27fb0ff083413e3e209b42d5dd09b5a2a7a89f16d14556ce1cac44b`**；`script.md` 仍 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。`lint --slug curio-s53 --json` exit 0、0 errors／0 warnings；114／123 正文場景為插圖（92.7%），最多連續卡片 1 張。

私有 `keyframes/manifest.json` SHA `72399b433a156ee5064f35ee2da318f2495afea8a0eacd9c7ad8b891d7df5164`、`media/ledger.json` SHA `786794fa452fc6049b428726516d86d4e1e7a84aca90fa772658fe26e3081499`、`media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`；14 張既有 KEEP 候選因未執行 keyframes 而未動，STOP 在位。帳本仍 US$0.4590／35 image／34 judge／0 預約，低於整集 US$4.78 上限。R21 manifest 綁舊畫面雜湊，**獨立紙審後才可重綁並驗收候選圖**；網站卡、人耳、配樂、長短片及 Studio 可點連結仍未完成。
