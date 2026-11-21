# 第 11 集真人版 fix-polish：上架前重拍（A 2 鏡、B 4 鏡）

2026-11-21 寫。依據：`review-zt/consolidated/retakes.json`（e011 的 A、B）、`review-zt/reports/e011.txt` 第 1–5、7 項、
`zhong-tian-qu-qi-e011-r2/script.md`〈真人版的改動〉〈獨立審稿後的修改〉。每鏡都先看過畫格條與證據格。
種子 9119101、9119102；960×544 Ref2VA；6 鏡 12 支、共 92 秒。沒有送出任何工作。

base 都是 `picks.json` 現在選中那支草稿的提示詞（picks.json 沒有 `motion_from` 欄位，從 `draft` 路徑判斷是 d1 或 fix1；
s21 的 fix2 重抽沒有被選，base 仍是 d1）。

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- | --- |
| s01 | A | 開場阿令全盤髮髻、成熟臉帶笑、扯得不明顯；跟 s04 像兩個人 | `d1/prompts/ref-s01-9111102.txt` | 錨句 `long glossy black hair pinned up with a single plain wooden hairpin` → 照參考圖的半披髮（頭頂小髻橫插一支木簪、其餘長髮直垂到背）；構圖重寫一次髮型；`startled and cold … no smile` → 眉緊皺、眼睜大、咬緊牙、嘴抿成一條直線；動作改成第一秒那隻黑袖手抓住肘部的袖子猛扯，她重心往後、被拉半轉身，長髮甩過背；拿掉 `no shackles`、`no blade … no weapon` 這串否定名詞 | 不換（三張阿令＋夜院 l1） | 錨句是錯的來源，所以改了錨句的髮型那段（其他字不動）。參考圖本身是半披髮，照 refs-live README 的教訓圖會壓過字，這次字跟圖一致，應該有效；臉的年紀若仍偏成熟，只能靠挑種子 |
| s14 | A | 唐小棠背律條整句只拍到後腦勺，主角是不動的胡縣令；胡縣令帽翅空心框 | `fix1/prompts/ref-s14-9111202.txt` | 整個構圖換掉：過肩背影 → 正面中景，前景左緣只有不點名的深褐肩膀與木棍頂（秦霜，不送圖），唐小棠在畫中、腰以上、四分之三側臉朝畫右畫外的縣令；台詞改回她自己說（原聲整句），一個動作：開口時右指尖撥一顆算珠；臉逐部位寫（下巴抬、眉平、眼亮直盯他、說完嘴收緊），用系列 NOSMILE 句；審片句的 `only a faint proud corner of the mouth` 不寫（WRITING 第四節：不寫嘴角往上的字）；`steps out from behind that shoulder and stops` 不寫（轉換動作放開頭會被跳過、一鏡兩動作），開頭她已站在肩旁 | 拿掉胡縣令；加唐小棠定妝照＋角度 a、b；場景照舊夜院 l1 | 第 7–10 集她開口說話一直笑，所以真人版原本改背影錄音；這次照審片改回正面原聲，笑的風險最大，兩支都笑就退回現在的版本（KEEP）。胡縣令出畫，帽翅問題在這鏡消失；縣令的反應（抿嘴縮頭）沒了，靠 s15–s16 接 |
| s17 | B | 錄音在講「三份婚書是」時嘴幾乎閉著；片尾笑開；背景一座牌樓 | `d1/prompts/ref-s17-9111102.txt` | 說話句後加：說「有」→ 吞口水停半拍 → 低聲不情願地講完，每個字都動嘴到最後；`cornered: eyes sliding away … no smile` → 眉皺下壓、眼往旁邊下方躲、下顎繃、嘴角往下；結尾 `he stammers, then lowers his head`（第二個動作）拿掉，只留左手壓住布帶；`no smile` → `he never smiles`（lessons 對趙捕頭的寫法）；背景 `only darkness` → 竹籬笆與畫外火把；拿掉 `no torch on a stand … no brazier` 與 `no blade …` 否定名詞 | 夜院 l1 → `set-xujia-yuan-ye-nolantern-l1` | 審片句寫「左手按鐵尺」，真人版已定不拍兵器（獨立審稿：腰間只有黑布帶），照布帶寫 |
| s18 | B | 婚書整面空白沒有印；拿紙的是一雙深色粗老的手（主觀鏡角度） | `fix1/prompts/ref-s18-9111202.txt` | fix1 的「只拍紙背」整段換掉：鏡頭正對紙面，一雙年輕修長、膚色淺的手（藍灰袖口、舊灰外衣袖）拇指捏住上兩角；紙面素紅，唯一的記號是右下角一個拇指尖大的空心朱紅細線方框，框裡跟紙一樣素紅；另兩份摺好的壓在後面被擋住；臉在畫框上緣外；動作：對摺的紙一次攤平、停住；火光從背後把紙照紅（審片要的）；`no characters, no seal …` 否定名詞拿掉 | 不換（夜院 l1） | 紙面朝鏡頭有長出假字的風險（WRITING 第九節）。沒有人的鏡也要有 `never the mood. `（polish-build 要求），寫成 `The set picture fixes the place only, never the mood.` |
| s21 | B | 說「被人蒙在」時抿嘴鼓腮像憋笑；沒退步、沒抓袖；帽翅空心 | `d1/prompts/ref-s21-9111101.txt` | 臉 `eyes round, brows shooting up, mouth stammering` → 眼瞪圓、眉高挑中間皺、嘴張著發抖、臉頰鬆、額頭冒汗；抓袖改成開頭就在胸前攥著（畫得到），一鏡只剩一個動作：第一個「這」退半步；說話句加「從第一個這到最後一個字嘴都在動」；構圖加帽翅句（實心霧黑的扁橢圓翅、跟帽身一樣黑）與「頭與帽後只有夜色」；拿掉 `no torch on a stand … no brazier` | 夜院 l1 → `set-xujia-yuan-ye-nolantern-l1` | 帽翅：定妝照 `huxianling-portrait-l1` 的翅本身就是黑邊框裡一片半透明網紗，後面有亮光就透出來。改字壓不過圖；這次靠拿掉燈籠與頭後只寫暗處來避，若仍空心要另做一張只把翅塗實的定妝照 |
| s25 | B | 右帽翅變空心黑框，後面燈籠透出來（7 秒中景）；衙役腰間有刀鞘 | `d1/prompts/ref-s25-9111102.txt` | 場景句拿掉燈籠（`one blank paper lantern …`、`warm glow of the one lantern`；月亮那句拿掉，新圖沒有月亮；牆寫成素石牆）；加帽翅句；`behind him two yamen runners` → 頭與帽正後方只有虛焦的素石牆，兩個衙役在畫面左右兩緣、離頭很遠；衙役的 `no blade, no knife, no sword, no scabbard …` → 一手一支火把、另一手空垂、腰繫黑布帶；動作 `straightens his hat with both hands … flicks one wide sleeve and lifts his chin`（三個動作，手會碰帽翅）→ 說到「核查名冊」時右寬袖往畫左一甩、收回，下巴一直抬著；結尾的 lantern glow 句拿掉 | 夜院 l1 → `set-xujia-yuan-ye-nolantern-l1` | 分鏡 c25 的「把官帽扶正」拿掉了（c24 寫帽還歪著，接點少一拍，可接受）；換場景圖後 s24、s26 背景有燈籠、這鏡沒有，鏡頭近、背景虛焦，應看不出 |

## 檢查

```
python3 -I _scripts/polish-build.py 11          -> e911: 6 shots, 12 drafts, 92 s
python3 -I _scripts/preflight-prompts.py …/fixp/colab-jobs.json   -> 0 error(s), 0 warning(s)
h3r.sh check --manifest …/fixp/colab-jobs.json                    -> 0 error(s), 0 warning(s)
```

preflight 沒有 warning。自己另掃了改過的段落裡的否定詞：只剩系列固定句（`no second copy of anyone`、`never the lens`、
NOSMILE 句、`no daylight anywhere`）與結尾 clean 句，那幾句照 base 保留。

## 拍完要看的

- s01：髮型是不是半披髮（頭頂小髻＋木簪＋長髮垂背）；前 1 秒有沒有被扯；嘴角。
- s14：每 0.5 秒看嘴角有沒有上揚；有沒有對鏡頭說；前景肩膀有沒有長出第二個人的臉；原聲是不是稿子原句（聽寫）。
- s17：「三份婚書是」那段嘴有沒有動；最後 1 秒有沒有笑；背景。
- s18：紙面有沒有長字或囍字；方框是不是空的；手的膚色與年紀。
- s21、s25：兩邊帽翅是不是實心；s21 有沒有退半步、抿嘴鼓腮。
- 都不行就 KEEP 現在那支，不要寫 RETAKE。
