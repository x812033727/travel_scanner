# C14 CamelBak｜已核准 v8 的非付費正式專案轉換

日期：2026-10-24。本輪只把站主核准的 70 句繁中旁白與 70 鏡方向轉成影片工具可讀的文字專案；沒有合成旁白、圖片、配樂、時間軸、字幕或成片，沒有後台匯入、上傳或發布。

## 核准綁定與原件

站主決定見 `reviews/owner-script-approval.md`。現行原件的 SHA-256 與核准收據逐一相同：

| 原件 | SHA-256 |
| --- | --- |
| `script.md` | `167DB38F368484951C56972B86A9838BB92B3B0B874952A87FBBAD26B8429312` |
| `script-source-notes.md` | `EF3AA1C79AB5EB19F0C52E9B024468AD6AF7A3EDC26AF17894D8C97D81BE538C` |
| `visual-plan.md` | `75E6AD2973078B72A28E17C5B2B9B58ACA5A1A247319CE5AB298D85E6F45DC2C` |
| `visual-plan.json` | `B211410713F271459AF267CC2F8DB4E8938A7EDB9938B6048A552A1076D4C063` |

原稿頁首仍保留作者提交時的「待獨立覆核」文字；後續同雜湊的 v7 全稿來源／配鏡審查僅 N10 HOLD，v8 N10 窄修獨立審查 PASS，兩位 v8 純旁白讀者各判 PASS，站主其後核准此組精確檔案。本輪不為更新頁首而改動已核准原件。這些收據不包含聲音、生成畫面或付費核准。

## 轉檔與非付費檢查

- `build-canonical.mjs` 先核四個原件 SHA，逐行核對六章 5／9／13／11／17／15 句與 70 個唯一 ID，將每句 `text` 原樣放入 `video.json`。70 鏡同序：54 張匿名原創靜態插圖保留原英文 prompt，16 張後製字卡保留原 `post_text`，最長連卡 3。原稿的 H01–H05 是 5 秒片頭之前的冷開場；N15 後另接 21 秒 v4 片尾與 Studio 連結位。繁中 CC 不燒錄。
- `series.json` 標記 `kind: story` 與系列第 14 集；`format: drama`、`category: explainer`、`look: {"preset":"cute-mystery"}` 是現行可愛插圖與後製卡的工具相容配置。後台若日後匯入，應以實際系列讀回為準，不由分類推定。
- 18 句含拉丁品牌／人名／產品名的機器行有 `say` 和綁當前 `text` 的 `say_for`，只供未來試音的**候選讀法**；字幕和站主核准旁白文字不變。這些候選未有人耳聽審，不能當作配音合格。`sources` 只索引原稿實際引用的 S1–S4、S8–S12 九項；S5–S7 的背景排除資料不冒充本集直接採用的影片來源。
- `claims.md` 與 `verify-1.md` 是前述既有獨立來源覆核的逐句 QA 對接，**不是本輪新做的 70 項來源查核**。2003 年報導仍限預備寄送；1998／2000 年口器專利、2005／2006 年水瓶專利和 2006 年展會實物各守其文件身分；2012／2014 年比例限各年 CamelBak 毛銷售額。圖片不可仿真人、商標、原專利附圖、賽場、店面、展場或戰地。
- `build-canonical.mjs --check`、`preflight.mjs`、`node tools/video/cli.mjs lint --slug story-everyday-camelbak-c14` 均通過；lint **0 errors、9 warnings**。警告包括 10 鏡原 prompt 沒有工具辨識的景別字、`generic`／`conceptual`／`bottle` 重複、三段機器偵測的鉤子間隔 55–84 秒、兩組年份重述。它們涉及已核准旁白或逐鏡，未在轉檔時私改；視覺實物與敘事節奏仍需另看。
- 非付費預檢按 `planned_duration_s` 重算：70 鏡全段口播紙估 **496.5 秒**，片頭前冷開場 **40.3 秒**，片頭後正文 **456.2 秒**，距 480 秒實測門檻的紙上差額 **23.8 秒**。片頭後插圖紙估 **333.0／456.2 秒＝73.0%**；這不是實際語音或成片畫面比例。舊核准收據把 496.5 秒稱作「正文」，`production-quote.md` 已更正其分母；本輪不沿用舊稱呼宣稱過關。
- `factsChecks` 讀現行 `verify-1.md` 為 PASS（無仍引用 NOT FOUND 的主張）；這只驗證 QA 索引形式與既有覆核對接。schema／lint／facts 聚焦測試 **69／69 PASS**；`npm run check:tasks` exit 0（既有其他票的過期／重疊提醒）；`git diff --check` PASS。
- 另一位非轉檔作者的代理在檔案穩定後只讀重跑 `build-canonical.mjs --check` 與 `preflight.mjs`，另以獨立解析逐項比對 70 句 ID／文字、`claims`、54 個插圖 prompt 和 16 張字卡，**0 項不一致，非付費轉檔 PASS**。其覆核也確認 metadata 工具會把 `video.json.sources` 追加成說明欄來源區；這不等於已在 YouTube 或後台讀回。該代理同樣保留紙上正文短 23.8 秒、讀音候選與付費 HOLD。

## 尚未取得的製作證據

`production-quote.md` 的 US$25 是未核准提案，C14 也缺已讀回的單集可歸因預算路由、舊費用核清與正式帳戶實價。沒有整支付費上限授權，不得送第一筆 TTS、ASR、Jev、圖片、評審或配樂請求。日後若另外獲核准，須先逐句試聽並量得**片頭後正文正常語速 ≥480 秒**，不足就停在聲音，不能以冷開場、片頭片尾、慢播、重複或靜音補足；若修稿，來源／盲讀／站主精確核准須重走。圖片須在實際時間軸量得正文占比 ≥70%、連卡不超過 3，再經成片 QA 和站主看片。此收據不是付款或發布指令。
