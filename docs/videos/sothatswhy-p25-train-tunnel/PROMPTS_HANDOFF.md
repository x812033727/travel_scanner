# P25 《高鐵車頭拉這麼長，為什麼不是為了破風？》分鏡提示詞手冊

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
- **已生成並匯入：第 1 至 36 鏡（共 36 鏡）**
- **待接力生成：第 37 至 68 鏡（共 32 鏡）**

---

## 📋 待生成分鏡列表（第 37 至 68 鏡）

### 第 37 鏡: `complaint-400m`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Wide view of a mountain tunnel portal with sound wave rings reaching a small house four hundred metres away on a hillside. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot complaint-400m --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 38 鏡: `kid-compressed-feel`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Waist-up medium shot of the girl hunching her shoulders inward as if being squeezed from all sides. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-compressed-feel --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 39 鏡: `kingfisher-dive`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Close-up of a small blue-and-orange kingfisher bird diving straight down from bright sky into a clear pond with only a tiny neat ring of water droplets. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kingfisher-dive --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 40 鏡: `kid-copy-beak-q`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Head-and-shoulders close-up of the girl holding up an imaginary magnifying glass to her eye with a playful grin. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-copy-beak-q --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 41 鏡: `pipe-bullet-test`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Close-up in a laboratory of a transparent high-speed launch tube firing tiny bullet-shaped model trains while digital sensors measure shockwave pressures. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot pipe-bullet-test --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 42 鏡: `computer-matches-beak`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Close-up comparing a glowing blue paraboloid curve on a laboratory display stand beside the sleek beak-to-head profile of a kingfisher bird. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot computer-matches-beak --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 43 鏡: `kid-biologist-q`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Waist-up medium shot of the girl pointing with curious round eyes at a small model of a bird beak. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-biologist-q --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 44 鏡: `kingfisher-beak-study`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Close-up comparing sleek narrow diving kingfisher beaks gliding smoothly into water with gentle blue streamlines around the beak-to-head curve. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kingfisher-beak-study --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 45 鏡: `kid-pantograph-q`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Head-and-shoulders close-up of the girl putting one hand above her head like a roof antenna and tilting her head. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-pantograph-q --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 46 鏡: `owl-feather`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Close-up side-by-side view of a brown owl wing feather with fine comb-like serrations along its edge and a streamlined wing-shaped roof pantograph. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot owl-feather --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 47 鏡: `train-500-debut`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Wide view of a sleek all-white high-speed passenger express with a smooth unmarked body with an extra-long pointed nose and a rounded cylindrical body gliding smoothly out of a mountain tunnel beside blooming cherry trees. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot train-500-debut --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 48 鏡: `kid-why-shrink-q`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Waist-up medium shot of the girl frowning in confusion and holding both hands wide apart then bringing them closer. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-why-shrink-q --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 49 鏡: `chief-seat-tradeoff`
- **發言角色**: chief
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The young female office director (Chief), Japanese anime aesthetic, delicate warm-sepia ink outlines. Neat dark brown hair tied in a low ponytail, round tortoiseshell glasses with subtle rim reflections, a sage green knitted cardigan over a crisp white collared shirt, and a brass magnifying glass pin on her chest. Exactly 5 slender fingers on each hand, warm expressive intelligent gaze.

Action and setting: Waist-up medium shot of the chief holding her two hands like a balance scale tilting up and down. Single person in frame, Chief alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot chief-seat-tradeoff --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 50 鏡: `nose-vs-seats`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Medium shot cutaway comparison of two equal-length lead carriages: the top carriage has a very long pointed nose with fewer blue seats; the bottom carriage has a shorter duckbill nose with extra rows of blue seats. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot nose-vs-seats --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 51 鏡: `kid-alfa-x-q`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Head-and-shoulders close-up of the girl leaning forward with sparkling eyes and holding her hands very wide apart. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-alfa-x-q --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 52 鏡: `long-test-nose`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Wide view comparing three sleek unmarked high-speed noses of different lengths: a nine-metre duckbill nose, a longer fifteen-metre nose, and an extreme twenty-two-metre experimental nose. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot long-test-nose --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 53 鏡: `rtri-three-stage`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Close-up of a sleek three-stage sculpted nose model in a wind tunnel with smooth blue airflow lines. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot rtri-three-stage --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 54 鏡: `kid-taiwan-back`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Waist-up medium shot of the girl pointing at herself with both hands and a big puzzled frown on the railway platform. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-taiwan-back --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 55 鏡: `chief-700t-numbers`
- **發言角色**: chief
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The young female office director (Chief), Japanese anime aesthetic, delicate warm-sepia ink outlines. Neat dark brown hair tied in a low ponytail, round tortoiseshell glasses with subtle rim reflections, a sage green knitted cardigan over a crisp white collared shirt, and a brass magnifying glass pin on her chest. Exactly 5 slender fingers on each hand, warm expressive intelligent gaze.

Action and setting: Waist-up medium shot of the chief holding up eight fingers with a bright smile. Single person in frame, Chief alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot chief-700t-numbers --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 56 鏡: `kid-why-quiet-q`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Head-and-shoulders close-up of the girl scratching her head with one finger, eyes wide in disbelief on the railway platform. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-why-quiet-q --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 57 鏡: `tunnel-size-compare`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Close-up front cross-section comparison of two mountain tunnels with identical express carriages inside: on the left, a tight tunnel fitting closely around the carriage; on the right, a spacious tunnel with nearly fifty percent more room. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot tunnel-size-compare --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 58 鏡: `taiwan-90m2`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Wide view inside a spacious bright concrete twin-track tunnel with generous room above and around a sleek all-white high-speed passenger express with a smooth unmarked body gliding smoothly along the rails. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot taiwan-90m2 --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 59 鏡: `taiwan-tunnel-hood`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Wide view of a sleek all-white high-speed passenger express with a smooth unmarked body with an eight-metre nose entering a wide mountain tunnel portal equipped with a long angled concrete buffer hood with side vent windows on a green hillside. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot taiwan-tunnel-hood --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 60 鏡: `kid-new-train-q`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Waist-up medium shot of the girl looking down the sunny railway platform with an eager smile. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-new-train-q --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 61 鏡: `new-train-wing`
- **發言角色**: 無 (旁白/物理機制)
- **純機制鏡頭 (nobody)**: True
- **參照圖 (ImagePaths)**: []
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

Composition: Medium shot from the front three-quarter angle of a sleek all-white high-speed passenger express with a smooth unmarked body with a sleeker flatter nose and sculpted wing-like ridges curving along both sides of the nose at a modern platform. Pure mechanical/landscape shot, strictly nobody, no people, no hands or limbs.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot new-train-wing --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 62 鏡: `chief-ask-kid`
- **發言角色**: chief
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The young female office director (Chief), Japanese anime aesthetic, delicate warm-sepia ink outlines. Neat dark brown hair tied in a low ponytail, round tortoiseshell glasses with subtle rim reflections, a sage green knitted cardigan over a crisp white collared shirt, and a brass magnifying glass pin on her chest. Exactly 5 slender fingers on each hand, warm expressive intelligent gaze.

Action and setting: Waist-up medium shot of the chief smiling warmly at the girl with both hands open. Single person in frame, Chief alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot chief-ask-kid --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 63 鏡: `kid-summary-1`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Waist-up medium shot of the girl counting on her fingers with a confident beaming grin on the railway platform. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-summary-1 --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 64 鏡: `kid-summary-2`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Waist-up medium shot of the girl pointing proudly at the wide tunnel in the distance and then at the sleek express. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot kid-summary-2 --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 65 鏡: `chief-platform-tip`
- **發言角色**: chief
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The young female office director (Chief), Japanese anime aesthetic, delicate warm-sepia ink outlines. Neat dark brown hair tied in a low ponytail, round tortoiseshell glasses with subtle rim reflections, a sage green knitted cardigan over a crisp white collared shirt, and a brass magnifying glass pin on her chest. Exactly 5 slender fingers on each hand, warm expressive intelligent gaze.

Action and setting: Waist-up medium shot of the chief smiling warmly at the viewer with her hands clasped. Single person in frame, Chief alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot chief-platform-tip --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 66 鏡: `outro`
- **發言角色**: kid
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/kid/f8dac008f296a6a3.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The curious young Japanese anime girl (Kid), delicate warm-sepia ink outlines. Dark brown chin-length bob hair, straight bangs, with one cute stray hair sprout standing up on top of her head. An ochre mustard-yellow hooded jacket with white drawstring cords, and a mint-green small cross-body shoulder bag strap. Exactly 5 fingers on each hand, lively sparkling large brown eyes.

Action and setting: Head-and-shoulders close-up of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light. Single person in frame, Kid alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot outro --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 67 鏡: `outro-chief`
- **發言角色**: chief
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The young female office director (Chief), Japanese anime aesthetic, delicate warm-sepia ink outlines. Neat dark brown hair tied in a low ponytail, round tortoiseshell glasses with subtle rim reflections, a sage green knitted cardigan over a crisp white collared shirt, and a brass magnifying glass pin on her chest. Exactly 5 slender fingers on each hand, warm expressive intelligent gaze.

Action and setting: Waist-up medium shot of the chief smiling warmly while gently touching one ear with her slender fingertips, bright warm morning light. Single person in frame, Chief alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot outro-chief --file <圖檔絕對路徑> --provider external --usd 0 --force
```

### 第 68 鏡: `outro-wave`
- **發言角色**: chief
- **純機制鏡頭 (nobody)**: False
- **參照圖 (ImagePaths)**: ['/home/antigravity/x812033727/travel_scanner/docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png']
- **提示詞 (Prompt)**:
```
High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, no text, no letters, no numbers, no labels.

The young female office director (Chief), Japanese anime aesthetic, delicate warm-sepia ink outlines. Neat dark brown hair tied in a low ponytail, round tortoiseshell glasses with subtle rim reflections, a sage green knitted cardigan over a crisp white collared shirt, and a brass magnifying glass pin on her chest. Exactly 5 slender fingers on each hand, warm expressive intelligent gaze.

Action and setting: Waist-up medium shot of the chief waving goodbye with a warm smile, bright morning light. Single person in frame, Chief alone, no other people.
```
- **匯入指令**:
```bash
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --shot outro-wave --file <圖檔絕對路徑> --provider external --usd 0 --force
```
