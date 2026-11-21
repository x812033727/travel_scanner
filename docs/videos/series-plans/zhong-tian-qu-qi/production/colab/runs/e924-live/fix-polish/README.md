# 第 24 集真人版 fix-polish：上架前精修的重拍提示詞（B 共 2 鏡）

2026-11-21。依據：`review-zt/consolidated/retakes.json`（e024 的 tier A、B 只有 s24、s19，都是 B；s20、s23、s33、s34 是 C，不在這次）、
完整審片報告 `review-zt/reports/e024.txt`（N1 馬燈、N2 大盆）、畫格條 `review-zt/ep/e024/review/shots/s19.jpg`、`s24.jpg`；
分鏡 `docs/videos/zhong-tian-qu-qi-e024-r2/script.md`（〈真人版的改動〉〈獨立審稿後的修改〉）、`video.json`；挑片紀錄 `e924-live/picks-merged.tsv`。
只寫提示詞與 spec，沒有送出任何工作。種子 9249101、9249102，960×544 Ref2VA，每鏡兩支，共 4 支、26 秒。

**base 怎麼找的**：`_live-e924/.../picks.json` 兩鏡都是 `seed 9241101`、`motion_from: d1`，提示詞是
`runpod/live/d1/prompts/ref-sNN-9241101.txt`（sha256 與 `d1/colab-jobs.json` 的 `prompt_sha256` 對過；`st1/prompts/ref-s19.txt` 是更早的 pilot 版、雜湊不同，不用）。

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- | --- |
| s24 | B | 全集賣點「紅糖變白」拍成跟房間一樣寬的大陶盆，白色從中央往外擴；前一鏡 s21、後一鏡 s25 都是手掌大小的漏斗，容器與比例對不上 | `d1/prompts/ref-s24-9241101.txt`（5 秒；成片用 0–4.0） | 構圖「insert close-up … the wide mouth of one brown clay funnel … only the funnel mouth and the sugar」→ 稍俯的三分之四角插鏡，第一格就是**一個小陶漏斗**：口「約兩掌並排寬」、錐身往下插進矮凳上的一個矮陶罐、糖填到口沿下、薄薄一層黃褐泥殼；漏斗口沿與陶罐肩在畫面正中，畫左緣一個虛焦的漏斗與陶罐當比例尺、後面是虛的土牆；動作「從上往下一層層變白，乾、細、像新雪的粉」保留，加「只在漏斗口裡」與「漏斗口沿與陶罐維持同樣的褐色陶、同樣的小尺寸」。審片改寫句的 no hands／no giant basin／no liquid（否定名詞）沒照抄，「泥殼裂開」也沒寫（一鏡兩個變化會只做一個） | 照 base（`set-tangfang-jia-l1`，清晨金光的糖坊角落） | 上一輪 1102 種子是俯拍特寫、變成像化學反應的同心花紋且看不出地點；這次用三分之四角＋漏斗錐身＋陶罐＋鄰近漏斗交代比例與地點，但場景圖是整片糖坊，模型仍可能拉成廣角大盆。挑片看：第一格是不是小漏斗、白色有沒有蓋過口沿。仍是大盆的話，下一步考慮不送場景圖、背景只寫土牆與矮凳 |
| s19 | B | 夜戲的燈是玻璃罩、鐵絲提把的煤油馬燈（宋代不會有），全景裁不掉 | `d1/prompts/ref-s19-9241101.txt`（8 秒；二牛原聲 6.64 秒，維持） | 場景圖那句後面加「石盆上那盞小燈是：短陶柱上的褐色陶油燈，約前臂高，一掌寬的淺陶碟、短棉燈芯躺在油裡、一朵小小的橘色裸火」，直接把圖上的燈重新定義；場景句「the warm glow of one small oil lamp on the stone basin」→「石盆上那盞褐色陶油燈的小橘火」；結尾「the warm lamp glow」→「the small flame of the clay oil lamp」；二牛「tired, not smiling: sweat…」→ 冷臉逐部位寫（皺眉、額頭與臉頰汗亮、每個喘著的字嘴張大），動作拿掉「用手腕抹一下汗」（一鏡一個動作：兩手攪鍋＋說話），結尾寫眉一直皺著；「snow and the creek beyond it」→「地上靜靜的雪與溪」（上一支棚外右上有飄雪白點）。台詞、許硯灌漏斗、站位、漏斗口在胸口高照 base。沒有寫 lantern、glass（否定名詞會被畫出來） | **沒換**（照 base：二牛 l1＋angle-a、許硯 l1＋angle-a、`set-tangfang-ye-l1`） | **場景圖本身就有馬燈**：`set-tangfang-ye-l1` 石盆上畫的就是玻璃罩煤油馬燈（夜的裁切 `set-tangfang-ye-jia-l1` 也含這盞），refs-live 沒有這個糖坊不帶馬燈的夜圖。考慮過的換法：(a) 送清晨的 `set-tangfang-l1`（同格局、沒有燈）——金色日出光很強，夜戲可能被拍成清晨，比燈更糟；(b) 不送場景圖——第 21 集夜戲不送圖會長出夜市攤子，s20–s23 也都送夜圖。所以照用夜圖、用文字改燈，**燈仍可能照圖畫成馬燈**。最乾淨的做法是審片報告 N1c 的免費改圖：把 `set-tangfang-ye-l1` 石盆上的馬燈改成陶油燈（像第 4 篇章 `set-gucang-ye-l1` 第二輪只換燈的做法），存成新 id（例如 `set-tangfang-ye-l2` 或 `set-tangfang-ye-deng-l1`），再把 spec 的 `pictures` 第 5 張換成它、重跑 polish-build。這一步不在本任務可改的範圍（refs-live），請協調者決定要不要先改圖再送 |

## 沒有重拍、但要記得的（C 級，不在本次）

- s20、s23（以及 s21、s22 開頭）的馬燈照審片 N1b 用 vf 靠左裁；封面 thumbnail 用的是 s23 那格，必須換格或裁掉右邊（N1a，必做）。
- s19 若照這份換成陶油燈，s20–s23 裁掉燈後畫面裡就看不到燈，不會跟 s19 打架。

## 檢查（2026-11-21）

```bash
cd docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs
python3 -I _scripts/polish-build.py 24
#  e924: 2 shots, 4 drafts, 26 s -> ~/mokaair-work/videos/zhong-tian-qu-qi-e924-dh/runpod/live/fixp/colab-jobs.json
python3 -I _scripts/preflight-prompts.py ~/mokaair-work/videos/zhong-tian-qu-qi-e924-dh/runpod/live/fixp/colab-jobs.json
#  0 error(s), 0 warning(s)
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest ~/mokaair-work/videos/zhong-tian-qu-qi-e924-dh/runpod/live/fixp/colab-jobs.json
#  0 error(s), 0 warning(s)
```

- s19 的場景圖改用 `set-tangfang-ye-nolamp-l1.png`（協調者從 set-tangfang-ye-l1 用 inpaint 抹掉石盆上的玻璃煤油馬燈，免費）。
