# P19 《降噪耳機開著，說話聲怎麼還在？》分鏡提示詞手冊

## 🎨 畫面風格標準（劇場級動畫光影 × 厚塗水粉質感）
- **比例與工具**：內建 `generate_image`，`AspectRatio: "16:9"`。
- **角色設定圖參照**：
  - 所長（Chief）：`docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png`
  - 小問（Kid）：`docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png`
  - 有角色的鏡頭，`ImagePaths` 必帶對應角色設定圖。
- **光影與筆觸**：暖深褐（warm-sepia）墨線，斜射暖金陽光（warm golden directional sunlight），金邊輪廓光（glowing rim light），空氣微細光塵（volumetric dust motes），奶油感淺景深散景（creamy bokeh）。
- **零文字與滿版**：100% 滿版無黑邊，全圖嚴禁任何文字、字母、數字、招牌或黑板亂碼（clean blank surfaces）。
- **手部正確**：每隻手精確 5 指，無殘肢或多指。

## 📌 目前進度
- **腳本、Gemini 中文配音、8 語系翻譯、8 語系 MiniMax 配音（全部 0 超時）全部 100% 完成！**
- **待接力生成：第 1 至 76 鏡（共 76 鏡）**

---

## 📋 待生成分鏡列表（第 1 至 76 鏡）

### 第 1 鏡: `kid-wear-headphones`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl putting on sleek matte-black over-ear headphones, eyes lighting up with amazement.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-wear-headphones --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 2 鏡: `kid-hear-chief-talk`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl looking sideways with a puzzled blink.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-hear-chief-talk --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 3 鏡: `chief-knowing-smile`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief sitting at a wooden desk with a gentle knowing smile.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-knowing-smile --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 4 鏡: `kid-sponge-guess`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl squeezing a small yellow foam earplug between her fingers.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-sponge-guess --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 5 鏡: `chief-foam-limit`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief shaking her head calmly with one finger raised.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-foam-limit --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 6 鏡: `subway-car-rumble`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Medium shot of passengers sitting inside a vibrating commuter train car, blurred dark tunnel rushing past the glass window.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot subway-car-rumble --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 7 鏡: `foam-absorb-compare`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up of a soft foam pad: rapid tight orange ripples get trapped in tiny pores while a massive long blue wave glides right through it.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot foam-absorb-compare --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 8 鏡: `kid-passive-wonder`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl peering into the ear cup mesh with squinting curiosity.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-passive-wonder --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 9 鏡: `chief-reveal-second-sound`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief leaning forward with bright engaged eyes.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-reveal-second-sound --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 10 鏡: `kid-two-sounds-shock`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl throwing both hands up in total disbelief.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-two-sounds-shock --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 11 鏡: `chief-counter-intuition`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief smiling gently in warm morning sunlight.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-counter-intuition --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 12 鏡: `kid-eager-how`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl clutching her mug with excited anticipation.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-eager-how --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 13 鏡: `chief-explain-wave`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief using two hands to trace gentle wavy curves in the air.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-explain-wave --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 14 鏡: `air-molecules-pressure`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up of air particles forming alternating dense compressed zones and loose expanded bands pushing forward.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot air-molecules-pressure --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 15 鏡: `kid-eardrum-listen`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl touching the side of her ear thoughtfully.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-eardrum-listen --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 16 鏡: `chief-anti-phase-hands`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief holding two palms opposite each other, mirroring motions in reverse.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-anti-phase-hands --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 17 鏡: `waves-cancel-diagram`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up of an incoming blue wave crest aligning with a red wave trough, colliding and flattening into a smooth calm level line.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot waves-cancel-diagram --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 18 鏡: `kid-cancel-cheer`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl clapping hands with a joyful realization.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-cancel-cheer --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 19 鏡: `chief-energy-clarify`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief gesturing gently with palms opening outward.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-energy-clarify --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 20 鏡: `kid-energy-puzzle`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl scratching her forehead with an analytical frown.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-energy-puzzle --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 21 鏡: `chief-impedance-reveal`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief tapping her fingertips together insightfully.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-impedance-reveal --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 22 鏡: `radiation-impedance-cavity`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up technical diagram of an acoustic speaker driver pushing against an opposing acoustic field in a compact chamber.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot radiation-impedance-cavity --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 23 鏡: `kid-history-ask`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl tilting head with curiosity.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-history-ask --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 24 鏡: `chief-patent-history`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief smiling with warmth in golden morning sunlight.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-patent-history --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 25 鏡: `paul-lueg-patent-concept`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up in a retro physics laboratory of an acoustic tube apparatus with a vibrating diaphragm and mirrored sound wave lines.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot paul-lueg-patent-concept --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 26 鏡: `chief-dsp-arrival`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief picking up a tiny shiny black silicon microchip with tweezers.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-dsp-arrival --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 27 鏡: `kid-voice-puzzle`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl tilting her head with a furrowed brow.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-voice-puzzle --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 28 鏡: `chief-wavelength-intro`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief spreading her arms wide apart to show massive scale.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-wavelength-intro --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 29 鏡: `wavelength-visual-scale`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Wide shot comparing a giant undulating blue wave spanning three meters across a room, beside tiny dense orange ripples only centimeters long.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot wavelength-visual-scale --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 30 鏡: `kid-compare-scale`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl looking down at her own two hands with wonder.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-compare-scale --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 31 鏡: `chief-ear-chamber`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief holding thumb and index finger two centimeters apart.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-ear-chamber --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 32 鏡: `zone-of-quiet-diagram`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up cross section of an ear canal immersed in a massive smooth low-frequency wave, showing a uniform calm bubble around the eardrum.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot zone-of-quiet-diagram --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 33 鏡: `kid-quiet-bubble-delight`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl smiling with a cupped hand beside her ear.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-quiet-bubble-delight --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 34 鏡: `chief-high-pitch-risk`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief slightly leaning in with a cautionary look.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-high-pitch-risk --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 35 鏡: `wave-misalign-clash`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up of two sound waves slightly shifted out of alignment: the crests fail to cancel, stacking into a sharp double-height spike.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot wave-misalign-clash --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 36 鏡: `kid-scared-spike`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl wincing slightly and touching her ear cup.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-scared-spike --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 37 鏡: `chief-acoustic-boundary`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief placing palms together steadily.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-acoustic-boundary --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 38 鏡: `kid-turn-head-ask`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl turning her head left and right playfully.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-turn-head-ask --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 39 鏡: `chief-misalign-risk`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief holding index fingers slightly offset from each other.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-misalign-risk --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 40 鏡: `kid-ear-pressure-ask`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl blinking and swallowing to equalize ears.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-ear-pressure-ask --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 41 鏡: `chief-brain-contrast-explain`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief tapping her temple with a gentle smile.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-brain-contrast-explain --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 42 鏡: `auditory-cortex-brain`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up artistic rendering of human auditory sensory balance: sudden disappearance of low background hum causes brain to perceive false pressure.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot auditory-cortex-brain --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 43 鏡: `kid-how-to-guard`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl looking intrigued with bright eyes.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-how-to-guard --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 44 鏡: `chief-dual-mic-intro`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief holding up a disassembled headphone cup showing two tiny glowing mic dots.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-dual-mic-intro --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 45 鏡: `hybrid-anc-microphones`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up cross section of a headphone cup: outer microphone detects exterior noise, while inner microphone monitors internal sound chamber.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot hybrid-anc-microphones --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 46 鏡: `kid-inner-mic-doubt`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl peering into the inner cup mesh.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-inner-mic-doubt --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 47 鏡: `chief-feedback-howling`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief holding hands close and mimicking a speaker whistle.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-feedback-howling --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 48 鏡: `acoustic-feedback-loop`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up diagram of closed-loop signal delay inside an ear cavity causing phase shift and acoustic instability whistle.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot acoustic-feedback-loop --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 49 鏡: `kid-speed-challenge`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl tapping her chin with lively questioning eyes.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-speed-challenge --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 50 鏡: `chief-sound-speed`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief gesturing swiftly with one palm slicing through air.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-sound-speed --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 51 鏡: `chip-latency-chain`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up diagram of sound wave entering outer mic, passing through tiny glowing processor calculating phase, and outputting to inner speaker.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chip-latency-chain --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 52 鏡: `kid-breath-tight`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl holding her breath with wide focused eyes.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-breath-tight --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 53 鏡: `chief-periodic-wave`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief waving one hand in a steady rhythmic back-and-forth swing.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-periodic-wave --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 54 鏡: `periodic-vs-random-wave`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up comparing an elegant smooth repeating sine wave on the left with a chaotic spiky jagged speech waveform on the right.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot periodic-vs-random-wave --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 55 鏡: `chief-plosive-random`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief making a crisp snapping gesture with her fingers.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-plosive-random --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 56 鏡: `kid-random-realization`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl nodding rapidly in full agreement.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-random-realization --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 57 鏡: `chief-summary-bridge`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief leaning back comfortably with an approving smile.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-summary-bridge --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 58 鏡: `kid-transparency-ask`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl tapping her ear cup with curious eyes.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-transparency-ask --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 59 鏡: `chief-transparency-explain`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief opening both palms outward in bright golden morning sunlight.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-transparency-explain --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 60 鏡: `kid-clues-connected`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl with her eyes shining brightly.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-clues-connected --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 61 鏡: `kid-break-case`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl smiling brightly and ticking off points on three fingers.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-break-case --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 62 鏡: `kid-case-points-two-three`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl speaking with crisp confidence.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-case-points-two-three --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 63 鏡: `chief-proud-approval`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief smiling proudly with a warm nod.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-proud-approval --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 64 鏡: `passive-isolation-cutaway`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up cross section of an ergonomic memory foam ear cushion sealing tightly against temple skin, keeping out external high-frequency ripples.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot passive-isolation-cutaway --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 65 鏡: `office-commute-contrast`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Medium shot of a quiet open-plan office workspace where air conditioning hum is suppressed while a colleague taps on shoulder.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot office-commute-contrast --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 66 鏡: `kid-own-voice-question`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl covering both ears with her palms and speaking a word.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-own-voice-question --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 67 鏡: `chief-bone-conduction`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief gently tapping her cheek and jawbone with a knowing smile.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-bone-conduction --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 68 鏡: `bone-conduction-skull`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up profile showing sound vibrations traveling directly through the jaw and skull bones into the inner cochlea.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot bone-conduction-skull --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 69 鏡: `kid-plug-ears-try`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the girl putting two index fingers into her ears and humming.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-plug-ears-try --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 70 鏡: `chief-occlusion-experiment`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief smiling warmly with head tilted.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-occlusion-experiment --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 71 鏡: `kid-home-test-ask`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl leaning forward with playful curiosity.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-home-test-ask --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 72 鏡: `chief-home-test-guide`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief snapping fingers beside her ear with a smile.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-home-test-guide --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 73 鏡: `everyday-sounds-test`
- **出場角色**: 無 (純物理/機制鏡頭)
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Close-up split view: on the left fingers snap crisp sound waves, on the right a quiet electric fan motor running silently.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot everyday-sounds-test --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 74 鏡: `chief-safety-thought`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief leaning forward with a warm conversational gaze.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot chief-safety-thought --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 75 鏡: `kid-safety-agree`
- **出場角色**: kid
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Head-and-shoulders close-up of the girl taking off her headphones with a relieved smile.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot kid-safety-agree --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 76 鏡: `outro-chief`
- **出場角色**: chief
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, absolutely zero text, zero letters, zero numbers, zero typography, zero watermarks. Scene description: Waist-up medium shot of the chief smiling gently and adjusting her glasses in bright morning sunlight.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p19-noise-cancelling --shot outro-chief --file <圖檔絕對路徑> --provider external --usd 0 --force
```
