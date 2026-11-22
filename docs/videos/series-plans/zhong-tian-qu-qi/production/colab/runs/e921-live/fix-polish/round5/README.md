# 第 21 集真人版 fix-polish 第 5 輪（第二波，2026-11-22）

照 `/root/mokaair-work/review-zt/WAVE2-BRIEF.md`；第 4 輪挑片 `round4/review-picks.tsv` 把 s27 判 RETAKE。種子 9219501、9219502，1 鏡 2 支，草稿 12 秒。只寫提示詞與 spec，沒有送出任何工作。
接戲以現行成片 `_live-e921/.../cut/e921-live.mp4` 為準（s26 146.42、s27 153.50 起）。台詞放錄音 `audio/zq921a29.wav`（5.76 秒），這鏡原聲靜掉。

| 鏡 | 錯在哪 | base | 改了什麼設計 | 圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- |
| s27 | 第 4 輪許硯背對成功，但正面的魏少卿整鏡嘴在動、偶爾露齒笑（一支 1.5–2.0、3.75、5.75 秒），蓋上錄音會讀成魏少卿在講；許硯頭轉成側臉。原因：提示詞仍寫 `Xu Yan's voice says the line` 加台詞原句，模型把嘴給了唯一露臉的人 | `fixp4/prompts/ref-s27-9219401.txt` | 提示詞完全不放台詞、不寫任何人說話；魏少卿寫成全程閉嘴聽：唇抿成直線、下顎、兩頰、嘴角、眼慢慢瞇、眉壓，逐部位寫到最後一格，唇閉、牙不露；許硯頭固定朝前只露後腦（拿掉 `edge of one ear`、`face turned away` 這類會讓頭轉的字），唯一動作食指點紅紙一下；鏡頭由慢推改固定；拿掉 `no smile`、`no second copy` 等否定句改正面寫 | 沿用第 4 輪（`xuyan-angle-a-l1`、`weishaoqing-portrait-l1`） | (1) 沒有台詞，模型可能讓魏少卿完全不動像定格，挑片看眼與扇子有沒有活；(2) 嘴若仍會動，下一步只能讓魏少卿也出畫（只拍許硯背影與紅紙）；(3) 第 4 輪畫面有成串垂珠，接 s28 現行畫面也有，沒另寫 |

## 檢查（2026-11-22）

- `polish-build.py 21 5`：1 鏡、2 支、12 秒，0 錯。
- `preflight-prompts.py …/fixp5/colab-jobs.json`：0 error、0 warning。
- `h3r.sh check --manifest …/fixp5/colab-jobs.json`：0 error、0 warning。
