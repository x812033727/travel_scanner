# 第 14 集真人版第五波重拍（round7，最後一次，2026-11-22）

依據 `review-zt/WAVE2-BRIEF.md` 的寫法與禁止事項，從 round6 出發（`../round6/review-picks.tsv` 的建議改寫）。種子 9149701、9149702；1 鏡 2 支 12 秒 → `runpod/live/fixp7/`。沒有送出任何工作。base `fixp6/prompts/ref-s12-9149601.txt`，圖照 base（`aling-portrait-l1`、`angles/aling-angle-a-l1`、`set-xujia-zoulang-l1`）。

| 鏡 | 錯在哪 | 改了什麼設計 | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- |
| s12 | round6 兩支都轉頭露嘴：9149601 約 2.75 秒起轉成側後方、3 秒後鼻尖唇線下巴入鏡；9149602 約 2 秒起完整側臉到結尾，還整鏡飄金色火星（提示詞沒寫）。乾淨背影只有約 2.5 秒，放不下 4.64 秒錄音 | 拿掉「頭微偏向畫左」：改成從正後方的過肩背影，她正背對鏡頭望進走廊，頭與後腦從第一格到最後一格正對鏡頭，只見後腦、頭髮與耳緣，臉頰鼻嘴都在頭的另一側；許硯在畫外左、不入鏡。唯一動作改成不動頭的小動作：肩膀隨一口慢慢吐氣微微一沉，然後停住到結尾；頭、髻、簪整鏡不動。燭光寫「warm, steady」、燭火「small and steady」，空氣寫「clear, still and empty」，不提任何火星或光點。半披髮（高髻橫插木簪、下半長髮直垂到腰）與背景（木樑、灰泥牆、兩點燭火、一盞圓紙燈籠）保留。鏡長 6 秒 | 無 | 正後方背影時人往畫右半放，模型可能為了「看向走廊」把頭往左轉；吐氣的肩動作可能被放大成轉身。若兩支都還轉頭，這鏡維持現行片段或改切別的素材，不再重抽 |

## 接戲

- s11、s13 都是許硯近景、臉朝畫右；s12 阿令背對鏡頭、許硯在畫外左，軸線不變。

## 剪接表要改（同 round6）

- s12 改 `voice_off` 鋪 `audio/zq914a12.wav`，拿掉 s12 的 `clip_af 0.88`；草稿原聲（環境聲以外）不要留。

## 檢查

```
python3 -I _scripts/polish-build.py 14 7                         -> e914: 1 shots, 2 drafts, 12 s
python3 -I _scripts/preflight-prompts.py …/fixp7/colab-jobs.json -> 0 error(s), 0 warning(s)
h3r.sh check --manifest …/fixp7/colab-jobs.json                  -> 0 error(s), 0 warning(s)
```
