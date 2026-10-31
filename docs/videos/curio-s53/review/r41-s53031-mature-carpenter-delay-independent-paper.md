# S53 R41｜`s53031` 成熟木匠與供屋延遲獨立書面覆核

2026-10-22 UTC。**PASS，限 R41 下列精確稿件的史料與書面畫面概念。**我不是 R41 prompt／claims 作者；直接核固定 Survey D、[R41 作者收據](r41-s53031-mature-carpenter-delay-author.md)、[可逆差分](r41-s53031-mature-carpenter-delay-structured-diff.json)、[原提示詞 HOLD 預檢](r41-s53031-unchanged-prompt-preflight.md)、Curio 系列規則及私有圖單／停線記錄。本紙審不驗收尚不存在的 `s53031` 原生圖，沒有改作者稿、離線回綁、購圖、judge、Git 暫存或 PR 操作。

## 固定來源與畫面界線

固定 1913 年 *San Francisco Relief Survey* `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865)記載小屋取代帳棚、1906 年 9 月 10 日開工、9 月 16 日漢密爾頓廣場已有 20 棟完工，且至少另經兩三個月，才有相當數量小屋備妥供難民使用。因此原句「大批小屋，得再過兩三個月才備妥。」有直接來源；來源沒有指認某位木匠、特定營地、某塊木板的工序或住戶的入住日，也沒有說 9 月 16 日全部小屋都未完工。

R41 prompt 改為稍後 1906 年的裸地公共廣場帳棚營地：一位有灰髮、面紋與當時工作襯衫的明顯成年木匠，用手將一片粗木板抵在一座低矮、未完工的小屋木架；遠處只有一頂帳棚與另一座低矮未完工木架。提示詞明排除屋內住戶、大型完工郊區住宅、鋪面道路、路牌、硬帽、電動工具與現代機具。claims 同行明列先完工的 20 棟、相當數量仍待備妥，以及畫面人物、工位、工序與時間為匿名原創概念。這個單一施工時刻沒有聲稱所有小屋仍在施工，亦沒有把概念插圖當史料照片。

原預檢建議明寫 9 月 16 日以後的秋季；新 prompt 的 `later in 1906` 較寬，沒有可見日期。就此紙面候選而言，一座在建小屋在 1906 年後期與 Survey 記載相容，claims 也不指稱確切施工或入住日，因此沒有形成史實矛盾。實際原生圖仍須原尺寸檢查，尤其是成年人、低矮在建屋架、帳棚、無完成郊區大宅及 2D 系列畫風。

依 `.agents/skills/curio-episode/SKILL.md` 的提示與插圖規則，這是單一主要人物做一件事的內容相關插圖；`look` 仍只有 `{"preset":"cute-mystery"}`，prompt 沒加 cartoon／chibi 等畫風詞或可讀文字，使用柔和陰天光。提示內排除現代物件屬畫面限制，沒有改 `look.negative` 或系列畫風。插圖是原創示意，驗收仍看來源／旁白矛盾和畫風漂移。

## 精確差分與系列檢查

| 固定輸入 | SHA-256 |
| --- | --- |
| `video.json` R41 | `56854934253b38463c3ab37cc283cb8dfdc9992dff7c81991fcd17484b622173` |
| `claims.md` R41 | `d6736f0a1126b773038223159e60e5fe4680b56c5abd34594e5088e6c29ea0e8` |
| R41 可逆差分 | `f10442b1adad2e34bdea1f8581ca9cf8baa484711682b8d4a6bfaf0757444c75` |
| 未改 `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 未改 `timeline.json`／`narration.wav` | `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`／`08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` |

實檔 `s53031` 場景完整等於差分 `after`；`claims.md` 的新整行恰出現一次。只將場景 `data.prompt` 反填 `before`，完整 `video.json` 逐位元組回 R40 SHA `65bec2d34c7d8443b9e45112e1193c6645feee86e676c0552d78b79f2335c312`；只反填 claims 整行，完整 `claims.md` 回 R40 SHA `68c2ab442dd0b20daef0b39977360f6b03a0974132bfd5967d90a2a07db53a0c`。因此除這一 prompt 與一行 claims 外，其他 123 景、`id`／`template`／`lines`／`camera`／`visual`、126 句口播均不變。`speechHash=05c4d9a79a8708b4`，R41 `visualHash=cfbe5fb638b9afd6`。

實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0、**0 errors／0 warnings／126 lines**。正文 **111／123 shot（90.2%）**，最長連續卡片 **2**，符合系列至少 70% 插圖、最多 3 張連續卡片；`s53031` prompt 為 503 字元。

## KEEP、費用與停線

正式私有 `keyframes/manifest.json` SHA-256 `87c6150128b00a2a383d59ccc3ed450625c090877ad050a82abac3fade9c8ee3`，仍綁 R40 `visual_hash=5818abc588740097`。19 筆所選檔案 SHA 全與磁碟吻合，judge 均 `passed=true`、`needs_review=false`；前 18 筆的 ID／所選路徑／SHA／request key 逐筆等於 [R40 KEEP inventory](r40-s53030-second-native-keep-inventory.json) SHA `5e97e26735227f0c4cff39438574fe39f2d0c033db88f29e269610276779a416`，第 19 筆 `s53030` 亦等於該清單的入選值。圖單沒有 `s53031`。

`media/ledger.json` SHA-256 `d8cddfc8aa1bac91ca9e20dc820ae3915921ea5c060878c12841c912cdfccbd9`；105 筆重加與記錄同為 **US$0.7020／53 images／52 judges／0 reservations**，低於已記錄整集上限 US$4.78。`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`，`STOP` 在位。R41 新 visualHash 尚未回綁，這份 PASS 只結束新 prompt 的書面覆核；任何後續原生圖與 judge 都須另過停線、即時模型／額度／預算預檢及原尺寸驗收。
