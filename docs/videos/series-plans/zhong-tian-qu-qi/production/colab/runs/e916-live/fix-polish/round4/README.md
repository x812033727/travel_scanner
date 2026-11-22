# 第 16 集（e916）第二波重拍（round4）：s27、s32、s11

2026-11-22，照 `review-zt/WAVE2-BRIEF.md` 與 `WAVE2-CANDIDATES.md`。種子 9169401／9169402，每鏡兩支 960×544 Ref2VA。
`python3 -I ../../../_scripts/polish-build.py 16 4` 寫出 `runpod/live/fixp4/`（6 支、36 秒）。只寫提示詞，沒送出任何工作。
第 16 集另一個代理正在剪接：只讀 `_live-e916/` 的片段與舊 `cut/old-1116/final.log`，沒有改剪接表或 clips（現行 `cut/final.log` 是空的）。
新參考圖見 `assets/refs-live/README.md` 最後幾列。

| 鏡 | 錯在哪 | 改了什麼設計 | 圖 | 拿不準的 |
| --- | --- | --- | --- | --- |
| s27（C） | 插鏡的燈是日式圓球紙燈籠、背景全黑；前後鏡筏尾是長筒方燈籠、背景星空與水 | base `fix1/.../ref-s27-9161202`。燈籠逐項寫死（長筒、下窄、暖白紙面細木框、內有燭光、掛在竹竿橫木下），背景寫深藍星空、遠處黑樹林與黑水；一個動作：手把紙舉高到燈籠旁停住（拿掉轉紙）。base 沒有 `never the mood. `，補上 | `tangxiaotang-portrait-l1`（袖子）+ **`prop-fangdenglong-w2`**（s26 現行片段末格裁） | 候選清單寫「背景是牆」，但現行 s26、s28 都是竹筏、星空與水，照現行片段寫。錄音照舊，沒有嘴 |
| s32（C） | 唐小棠一個光滑大圓髻（s29 新片、s33 是雙髻垂長緞帶）；書生排成一列不看紙（fix1 寫 lean in 也沒演） | base `fix1/.../ref-s32-9161202`。髮型用 s33 背影圖鎖：兩個圓髻、各一條垂到背上的長粉緞帶；書生減成三人（高瘦、圓臉、短鬚年長），第一格就彎腰湊在紙前、臉朝紙抬起（終態開場）；她一個動作：把紙往陽光斜舉、讓光透過去 | 加 **`tangxiaotang-back-shuangji-w2`**（s33 現行片段裁）+ `set-shuyuan-l2` | 背景圖仍是書院街景，三人以外可能多畫路人；稿子是五六人，減成三人是為了臉看得清楚 |
| s11（B） | 石木匠說話時直視鏡頭約 4 秒 | base `d1/.../ref-s11-9161102`。改過許硯肩的反打：許硯後腦與左肩在左前景、佔畫面四分之一，石木匠在右中、整個身體與臉朝畫左看他，一個動作：把濕紙翻扣到紙堆上、兩掌一壓；唐小棠退到右後、小而虛、低頭看盆 | `shimujiang-portrait-l1`、`xuyan-angle-a-l1`（嚴肅的那張）、`tangxiaotang-portrait-l1`、`set-gongpeng-l3`；拿掉唐小棠兩張角度圖 | 候選清單寫「石木匠看畫右的許硯」；我照 s10（過石木匠肩拍許硯，許硯在畫左）的軸線，反打讓許硯背影在左、石木匠看畫左。三個有名字的人（一個背影、一個遠景），可能分身 |

## 檢查（2026-11-22）

- `polish-build.py 16 4`：3 鏡、6 支、36 秒
- `preflight-prompts.py …/fixp4/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp4/colab-jobs.json`：0 error(s)、0 warning(s)
