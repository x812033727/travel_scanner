# Post-mortem：一次製作或試拍收工時填的表，與 2026-10-03 試拍的填法

`run_report.mjs --slug <SLUG> --markdown` 印這張表，數字從 `media/ledger.json`、`keyframes/manifest.json`、`clips/manifest.json`、`approvals.json`、`state.json` 算出來；填不出來的欄印 `not_available`，沒檢查的寫 `not_checked`，安排了沒做完的寫 `pending`（visual-quality.md 的規矩）。人要補的是「原因分類」「站主反應」「下次改什麼」三段。一份一個檔，放在集的 `docs/videos/<slug>/` 或作品的 `episodes/` 下；素材與收據留 repo 外，表裡只放 SHA-256 與路徑的相對位置。

## 表單

```markdown
# <slug> post-mortem（<日期>）

## 範圍
- 哪幾集、哪幾鏡、跑到哪一步（`status` 的 next）、誰跑的（工人／代理／自己的 runner）
- 路線：伺服器 API（provider／model／resolution）、Hailuo 網頁（方案）、Kling MCP（方案）；混用就逐鏡列

## 買了什麼（帳本）
| 種類 | 筆數 | 單位 | US$（帳本） | 預留（站上） | 實際帳單 |
| 設定圖 | | 張 | | | |
| 關鍵影格 | | 張（含 end_frame） | | | |
| 素材 | | 秒 | | | |
| 音樂 | | 首 | | | |
| judge | | 次 | 0.01 × n | | |
| 外部片段 | | 支／秒 | 0（方案點數：<n> 點，方案 <id>） | — | — |
| 合計 | | | | | |
- 本月剩餘（`media-status`）：片段 __／3,000 秒、圖 __／1,500、judge __／3,000、音樂 __／60；單支 __／US$200

## 接受了什麼（五個數字分開）
| | 設定圖 | 關鍵影格 | 素材 |
| job ready | | | |
| QC ok（ffmpeg） | — | — | |
| judge passed | | | |
| needs_review | | | |
| 站主 accepted（關卡） | look: | storyboard: | final: |

## 浪費了什麼
- 買了沒用的：<張數／秒數／US$>；分母是「買了什麼」
- 利用率（素材）：每鏡 needed_s ÷ seconds，整集 __%；切鏡省下 __ 秒／US$__
- 白跑的輪：結束碼 2 __ 次、3 __ 次（原因）

## 重拍的原因分類（每個 needs_review 或退回的 take 一列）
| 鏡 | take | 退回的話（judge problems 或人看的） | 類別：內容／隨機／判讀／QC／工具 | 這次怎麼修 | 修了有沒有收斂 |

## 路線與方案
- 伺服器：每小時送出 __ 次、最長等待 __；expired／failed 的 job
- Hailuo：方案、用掉 __ 點、排隊最久 __、relax 隊列有沒有用、匯入幾支、assemble 過幾支
- Kling：方案、每支點數（讀自帳號）、匯入幾支

## 核准
| 關卡 | 狀態（approved／stale／missing／absent） | stale 的原因（哪個改動） |

## 時間
| 階段 | 跑了幾次 | 合計秒數（state.json runs） | 等站主多久 |

## 站主的反應
- 原話、日期、對哪一版（SHA-256）；接受／退回／沒看

## 下次改什麼（可驗證的，一條一個變數）
- 分鏡：
- prompt／camera／motion：
- 路線或模型：
- 流程（哪個檢查要提前、哪個腳本要補）：
- 不改的（為什麼）：
```

## 2026-10-03 試拍：《喜宴未散》E1／E2 填法

來源：`docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`、`visual-revision-20261003.md`、`docs/videos/series-plans/competition-20261002/cost-ledger.csv`。這一輪不是 `clips` 階段跑的，是作品自己的 runner 逐筆送（一次一筆、全域 worker 關著），所以沒有 `media/ledger.json`、manifest 與 `state.json`，數字是從收據抄的；利用率與每階段時間 `not_available`。

```markdown
# wedding-reckoning-competition-e01／e02 post-mortem（2026-10-03）

## 範圍
- E1 的 S01、S03、S04 與兩個角色的設定圖；E2 只有核准的劇本、既有配音與 S34 的 metadata 修正，沒生成影像。跑到：S01＋S03 累積 storyboard 核准；S01 R04 的五秒預覽；之後停掉付費操作。
- 路線：伺服器 API，gemini／veo-3.1-lite-generate-preview／1080p／8 秒／allow_adult（profile.json）；圖 gemini-3-pro-image。沒用 Hailuo、Kling。

## 買了什麼
| 種類 | 筆數 | 單位 | US$（帳本） | 預留（站上） | 實際帳單 |
| 設定圖 | 3（知棠 A、B；顧承川 A） | 張 | not_available | 0.402 | null |
| 關鍵影格 | 7（S01 ×2、S03 ×3、S04 ×2） | 張 | not_available | 0.938 | null |
| 素材 | 6（S01 ×4、S03 ×2） | 48 秒（每筆 8） | not_available | 3.840 | null |
| 音樂 | 0 | | | | |
| judge | 2（顧承川設定圖、S01 R04 片段） | 次 | 0.02 | 含在 manual reserve 10 內 | null |
| 外部片段 | 0 | | | | |
| 合計 | 16 jobs | | | 15.18（含 manual reserve 10） | null |
- Pilot cap US$100、E1／E2 batch cap US$350；兩筆失敗的 Lite 片段 usd_estimate 0 但預留保留。

## 接受了什麼
| | 設定圖 | 關鍵影格 | 素材 |
| job ready | 3／3 | 7／7 | 4／6（R01、R02 failed：HTTP 400 negativePrompt） |
| QC ok | 2／3（知棠 A 退：圓錶） | 4／7（S01 R02、S03 R03 過；S01 R01 門開、S03 R01 火場、S03 R02 簽名筆畫、S04 R01 景別、S04 R02 換腕退） | 1／4（S01 R04 抽樣可剪；R03 多錶多手、S03 R01 多筆多錶、S03 R02 抬筆退） |
| judge passed | 1／1（顧承川 7） | 0 次 judge（人看） | 0／1（S01 R04 6.72：「開頭睜眼」，逐幀是一次眨眼） |
| needs_review | — | — | — |
| 站主 accepted | look: 知棠 B、顧承川 A approved | storyboard: S01 R02 ＋ S03 R03 approved | final: 無；站主看了 S01 預覽給 60／100，「不會想繼續看」 |

## 浪費了什麼
- 圖 10 買 4 用（6 張、US$0.80 預留）；素材 6 買 0 用（48 秒、US$3.84）；加 manual reserve，exposure 15.18 換到 0 支可用素材。
- 利用率：not_available（沒有 clips manifest）；切鏡 0。
- 白跑：兩次 Lite 送出就失敗（參數相容，不是內容安全）。

## 重拍的原因分類
| 鏡 | take | 退回的話 | 類別 | 怎麼修 | 收斂？ |
| 知棠 sheet | A | 錶是圓的，來源是矩形銀錶 | 內容 | retake_of 寫明矩形錶、左耳露出 | B 過 |
| S01 kf | R01 | 人物後方門像開的 | 內容 | 寫明封閉鋼門 | R02 過 |
| S01 clip | R01、R02 | HTTP 400 negativePrompt（伺服器只說 refused） | 工具 | R03 拿掉欄位、避免字寫進 prompt | 送出成功 |
| S01 clip | R03 | 0.5 秒起第二只圓錶、左臂抬起持筆 | 內容 | 重拍 | R04 仍有爭議 |
| S01 clip | R04 | judge 6.72：開頭睜眼；逐幀是 0.375–0.583 秒一次眨眼 | 判讀 | 記錄差異，不改分；交站主 | 站主 60 分，整版退回 |
| S03 kf | R01、R02 | 火場帶進婚禮、筆色錯；簽名筆畫、紙筆間隙不明、英文標籤 | 內容 | 清火場；原件與展示副本分開、筆懸空 | R03 過 |
| S03 clip | R01、R02 | 第二支筆第二只錶、矩形錶變圓；抬筆到水平再轉回 | 內容 | 要重寫 motion 的幅度 | 沒收斂，停 |
| S04 kf | R01、R02 | 上半身廣鏡不是手與原件的插鏡；錶換到翻頁手 | 內容 | 景別改插鏡；寫明哪隻手 | 沒收斂，停 |

## 路線與方案
- 伺服器：一次一筆；R04 的 judge 第一次在 Windows 唯讀 descriptor 的 fsync 失敗、沒進 POST，之後一次顯式 recovery POST。
- Hailuo／Kling：沒用。

## 核准
| 關卡 | 狀態 | stale 的原因 |
| script E1、E2 | approved | — |
| look 知棠、顧承川 | approved | — |
| storyboard S01＋S03 | approved | 之後站主退回整版視覺，舊核准保留當歷史，不當有效 |
| final | absent | — |

## 時間
| 階段 | 次數 | 秒數 | 等站主 |
| 全部 | — | not_available | 文件核准 2026-10-02 18:32 UTC（台北 10-03 02:32）→ 收尾稽核 19:42 UTC，約 70 分鐘 |

## 站主的反應
- 2026-10-03：「畫面感覺60分」「不會想讓人想繼續看下去」，要 90 分，要把經驗做成 skill（visual-revision-20261003.md）。對 S01 R04 預覽（SHA-256 65128501…）。整版 rejected。

## 下次改什麼
- 分鏡：81 鏡全 locked、E1 沒有全景、插鏡 46%、開場三鏡沒事發生（drama-craft.md 的表）；先改分鏡再重拍。
- prompt／camera／motion：插鏡的 camera 第一個詞寫 Insert；識別道具寫明哪隻手；「微顫」改寫成可讀幅度的既有手筆關係；避免的字進 prompt（Lite）。
- 路線或模型：Lite 留著（profile 釘的）；`look.negative` 一開始就空。
- 流程：開拍前跑 preflight（會抓 Lite negative、judge 題目長度）；五個數字分開報；重拍兩次同一類內容問題就停。
- 不改的：judge 門檻 7、6.72 不改分；profile 的模型與解析度。
```
