// Rebuild the separate series-look source from the H07 record trail.
// This reads the original but writes only curio-h07-v2/video.json. It never reuses media.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const original = JSON.parse(readFileSync(join(here, "../curio-h07/video.json"), "utf8"));
const doc = structuredClone(original);
doc.slug = "curio-h07-v2";
doc.format = "drama";
doc.look = { preset: "cute-mystery" };
doc.characters = [];
doc.youtube.video_id = null;
doc.youtube.description = doc.youtube.description.replace(
  "畫面插圖由 AI 生成；1698 年登記影像的來源與公有領域授權見圖片來源。",
  "畫面插圖由 AI 生成；史料來源見說明欄。",
).replace("資料截至 2026-10-14", "資料截至 2026-10-18");
doc.loops.find((loop) => loop.setup === "db81d592").what = "1698 年入獄登記是否留下囚犯姓名";

// The fresh blind narrative review found an agenda sentence at the start of
// chapter five and two repeated conclusions. Keep IDs stable for traceability;
// changed lines must get new audio and fresh locale translations.
const revisedLines = {
  "45164df0": "他記下囚犯當晚約十點去世。",
  "baeadea2": "兩份文書一對照，關鍵的落差就從名字裡冒出來。",
  "029cafbf": "下葬摹本上的拼法，和密令裡的多熱並不相同。",
  "926246b2": "查到最後，沒有一份現存紀錄能同時證實這名死者的本名與鐵製面具；面具實物也沒有留下。",
  "27099bdc": "哪份紀錄能把這名蒙面囚犯、他的名字，和後來那個「鐵」字真正接起來？",
  "22c31821": "伏爾泰後來的書，究竟把面具的哪個部件寫成鋼製？",
  "5c6e9a3e": "原字無從核對，無法判定哪個讀法更接近。",
  "db81d592": "那筆入獄登記，會留下他的姓名嗎？",
  "836e3743": "那封密令，有沒有寫出為何不讓他說話？",
  "3a052062": "「鐵面人」三個字傳開後，王室猜想也被寫進書裡。",
  "1648d74e": "一七七一年，一段標成編者增補的文字猜囚犯是國王兄長；作者仍有爭議。",
  "4ecf1ae5": "大仲馬後來把雙胞胎寫進小說。",
  "14d8d94f": "史家芬克布倫塔諾認為，這個名字指向馬提歐里。",
};
for (const scene of doc.scenes) for (const line of scene.lines) {
  if (revisedLines[line.id]) line.text = revisedLines[line.id];
}

// All prompts describe what MiniMax should draw; the series look lives only in look.preset.
// Historical documents are blank props. Dates, names, and uncertainty remain in narration/cards.
const prompt = {
  0: "Medium shot inside the Bastille records chamber in Paris in 1703, one French deputy in a plain period waistcoat bends over a large bound ledger with a feather quill, his worried expression and quill in focus while the page turns away from camera, light from one candle after dark",
  1: "Close-up in the same records office, one deputy closes a plain death register, his brows knit above the cover, light from a candle at the side",
  2: "Overhead view of a seventeenth-century official sealing a folded blank order on an oak desk, one red wax seal beneath his hand, light from a morning window",
  3: "Medium shot in a quiet present-day archive, one researcher lifts a sealed plain folder to chest height and looks puzzled, document bundles tied with string on a table behind her, light from a high window",
  4: "Medium shot from directly behind at the Bastille stone gate in Paris in 1698, one lone cloaked prisoner walks away into the dark stone doorway, the back of a plain loose dark hood covering the whole head and neck, simple cloth folds across the shoulders, soft afternoon courtyard light",
  5: "Close-up in a prison records room, one clerk leans toward a closed admission register, his puzzled eyes fixed on its cover, light from a high window",
  6: "Medium shot in a Paris writing room in 1738, one European male scholar in a powdered wig and plain French coat raises a folded letter to eye level, his curious face turned to the letter, soft daylight from a window on the left",
  7: "Close-up in an eighteenth-century study, one reader pauses over a folded letter with a questioning expression, his hand hovering above a bound volume on the desk, light from an open doorway",
  8: "Medium shot in a modern archive workroom, one researcher holds two separate ribbon-tied facsimile document bundles apart over a bare table, her questioning expression visible between them, soft light from a skylight",
  9: "Close-up in a prison records office, one deputy lowers his quill toward a blank register, his hand and startled eyes in frame, light from the window",
  11: "Medium shot in a Bastille records office at night, one deputy closes a death register on a bare table, his face solemn, light from a single candle",
  12: "Wide shot of Saint-Paul parish graveyard in afternoon light, one gravedigger lowers his spade beside an unmarked grave, church stonework behind him, light from the open sky",
  13: "Medium shot in a modern archive, one researcher lifts a closed burial-register facsimile from a records box, her hopeful expression visible, light from a window",
  14: "Close-up in a present-day archive, one researcher frowns while placing two folded paper reproductions face down on opposite sides of a bare table, her worried face above them, soft light from the left",
  17: "Close-up in a modern archive, one researcher places an empty identity folder beside three separate facsimile volume covers, her doubtful eyes above them, light from a cloudy window",
  18: "Medium shot in a present-day archive, one historian reaches toward a printed transcription of a 1669 order, a blank burial facsimile beside it, light from a high window",
  19: "Close-up in a seventeenth-century office, one official presses a wax seal onto a folded blank order, his concentrated face just above it, light from a morning window",
  21: "Wide shot at a Piedmontese Alpine fortress in daylight, one courier carries a sealed packet toward its gate, mountains beyond the wall, light from a pale sky",
  22: "Medium shot inside a stone prison corridor, one sentry studies a closed cell door with a baffled expression, his hand on an empty key ring, light from a high window",
  23: "Medium shot in a French prison corridor, one middle-aged governor carries a covered meal tray toward a cell, his intent face visible, light from a wall torch",
  25: "Close-up in a prison corridor, one governor pulls a wooden cell door shut with one hand, a narrow strip of light below it, daylight from the hall",
  26: "Medium shot in a prison guardroom, one sentry steps away from a closed cell door and looks uneasy, barred window behind him, daylight from the right",
  27: "Close-up in a modern archive, one historian pauses over a blank copy of a sealed letter, brows furrowed at a single blank note card, light from a side window",
  29: "Medium shot in a modern archive, one researcher holds two blank interpretation cards apart, her thoughtful face above them, light from a tall window",
  30: "Close-up in a modern archive, one researcher closes an empty biographical folder without filling it, her disappointed face visible, light from a cloudy window",
  31: "Medium shot in a sunlit archive, one historian rests both hands on the smooth lid of a shut plain archival box at the center of a bare oak table, her puzzled expression visible, soft light from above",
  32: "Overhead view of one researcher placing two closed archival folders far apart on a daylight reading table, their covers blank, light from a wide window",
  34: "Medium shot in a modern archive, one researcher points to the space between two separate closed folders, her questioning face visible, light from a skylight",
  35: "Medium shot inside a French stone fortress office in 1698, one elderly European governor in a late-seventeenth-century French coat holds a wax-sealed transfer order with its folded back facing the camera, his intent face visible, light from a morning window",
  36: "Wide shot near Sainte-Marguerite Island in daylight, one boatman rows a small skiff away from the low Fort Royal ramparts, light from a clear sky",
  38: "Close-up in a stone fortress corridor, one governor pushes a heavy wooden gate almost shut, its narrow light gap beside him, daylight from outside",
  39: "Close-up in a fortress office, one elderly governor studies a folded transfer order with a guarded expression, light from an afternoon window",
  41: "Medium shot in a modern archive, one archivist takes a closed admission register from a shelf, eyes fixed on the cover, light from a tall window",
  44: "Wide shot of a Bastille stone vestibule by day, one elderly governor enters carrying a closed folder, the gate behind him, light from the courtyard",
  45: "Close-up in a modern archive, one researcher holds two blank evidence cards apart, lips pressed in caution, light from a morning window",
  46: "Medium shot in an eighteenth-century writing room, one scholar folds a blank letter and pauses before sealing it, thoughtful face above the desk, light from a window",
  47: "Close-up in an eighteenth-century study, one reader raises a folded letter with a puzzled expression, a closed book on a distant shelf, daylight from a window",
  48: "Medium shot in a Paris writing room in 1738, one European male scholar in a dark eighteenth-century French coat and powdered wig writes with a feather quill at an oak desk, focus on his face and quill while the paper angles away, soft daylight from the left window",
  49: "Medium shot in an eighteenth-century study, one scholar closes a blank notebook, his curious face above it, daylight from a window",
  50: "Close-up in a modern archive, one researcher opens an empty interview notebook and looks disappointed, light from a rainy window",
  51: "Medium shot in a modern archive, one historian closes an empty interview notebook beside a sealed letter copy, her cautious face visible, light from a skylight",
  52: "Medium shot in a present-day library, one researcher searches a shelf of older closed books, hand reaching toward one spine, light from a high window",
  54: "Medium shot in an eighteenth-century Paris reading room, one reader picks up a newly printed closed book, his intrigued face visible, light from a bright window",
  55: "Close-up in an eighteenth-century reading room, one reader lifts a closed volume and widens his eyes, light from a tall window",
  57: "Medium shot in an unmistakable theatre workshop, one costume maker fastens a small metal spring beneath a black stage mask prop, rehearsal lights visible behind, daylight from a side window",
  58: "Wide shot in an eighteenth-century bookbinding room, one binder stacks plain closed volumes on a wooden bench, light from a noon window",
  61: "Medium shot in a present-day archive, one historian places a closed literary volume beside a separate prison register facsimile, her face focused, light from a skylight",
  62: "Medium shot in a theatre costume workshop, one craftsperson shapes a rigid mask prop on a wooden form, folded black cloth beside it, light from a workroom window",
  63: "Close-up in a present-day library, one researcher lifts a tiny paper crown prop away from a closed eighteenth-century volume, light from a window",
  66: "Medium shot in a modern archive, one researcher moves a paper crown prop away from a locked document box, her skeptical face visible, daylight from above",
  67: "Wide shot on a theatre rehearsal stage, one costume worker hangs two matching royal coats on separate racks, stage curtains behind, light from rehearsal lamps",
  68: "Medium shot on a visible theatre rehearsal stage, one actor lifts an oval stage mask before his face, two matching royal coats hanging on racks behind him, light from rehearsal lamps",
  69: "Medium shot in a nineteenth-century novelist's study, one anonymous writer closes a blank novel draft, matching royal costume sketches pinned behind him, light from a daylight window",
  70: "Wide shot in a present-day library, one archivist closes a colorful novel beside a separate plain archive box, light from a tall window",
  71: "Medium shot in a modern museum workshop, one researcher puts a theatrical metal-mask prop back into a box beside a novel, a separate archive folder beyond it, light from a skylight",
  73: "Overhead view at a modern research table, one historian holds two separate translucent profile sheets apart, the outlines unable to meet, light from a window",
  74: "Medium shot in a modern archive, one historian moves two blank candidate cards to opposite sides of a closed death-register facsimile, light from a skylight",
  75: "Medium shot in a quiet modern library, one middle-aged historian in a plain cardigan traces a curved path with one finger across a simple unmarked tabletop route diagram, his thoughtful expression visible, soft daylight from above",
  79: "Close-up in an archive, one historian lifts a folded sealed-order facsimile by its blank outer edge, light from a morning window",
  80: "Medium shot in a modern archive, one historian holds a small round wooden marker well apart from a leather-bound death ledger tied shut with ribbon, her cautious face visible, light from a tall window",
  81: "Medium shot in a bright present-day library, one anonymous researcher raises a blank hypothesis sheet, her questioning face visible above a sealed archive box, light from a wide window",
  82: "Overhead close-up in a modern research room, one anonymous scholar moves a plain servant token beside a closed historical folder, the setup visibly a hypothesis on a table, light from above",
  83: "Overhead view on a present-day research table, one historian arranges two small crown tokens beside a closed coin chest prop, a hypothetical diagram, light from a daylight window",
  85: "Medium shot in a modern archive, one historian separates a blank hypothesis sheet from a closed official-order facsimile, her careful face visible, light from a skylight",
  86: "Close-up in a modern archive, one historian leaves a blank identity card beside a sealed death-register facsimile, light from a cloudy window",
  87: "Medium shot in a modern archive, one researcher slides a candidate token away from a separate blank burial card, her questioning face visible, light from a window",
  88: "Medium shot in a modern archive, one historian places a closed nineteenth-century burial-register facsimile on a reading table, her hand on the binding, light from a skylight",
  91: "Close-up in a present-day archive, one historian studies a closed burial facsimile, a candidate token resting beside it, her expression uncertain, light from a morning window",
  92: "Medium shot in a modern archive, one historian pauses with a candidate token halfway toward a closed burial facsimile, his uncertain face visible, light from a high window",
  93: "Overhead view of a modern research table, one historian pushes two candidate folders onto separate paths, their covers blank, daylight from a window",
  94: "Medium shot in a modern archive study room with a plain wall, one archivist lays two human head-and-shoulder paper silhouette cutouts far apart on an empty table, her careful expression visible, light from a high window",
  96: "Wide shot in a present-day museum gallery, one visitor peers into a vacant glass cabinet containing only a bare velvet plinth, his surprised face reflected faintly in the glass, light from a skylight",
};

const cardToShot = new Set([6, 18, 31, 47, 51, 57, 61, 71, 74, 75, 82, 87, 88, 91, 96]);
const nameSpellingCards = new Map([
  ["h07-43592117", {
    template: "big",
    data: { kicker: "下葬名｜19 世紀轉錄", text: "**Marchioly**", sub: "Funck-Brentano 1899；堂區原簿已毀" },
  }],
  ["h07-18bcd1aa", {
    template: "compare",
    data: {
      title: "同一次下葬的不同拼讀",
      left: { heading: "堂區簿摹本", points: ["Marchialy"] },
      right: { heading: "副官邊註", points: ["Marchiel"] },
      verdict: "讀法不一；無法當作確證本名",
      source: "Topin 1870；Funck-Brentano 1899",
    },
  }],
]);
// Name the actual room or light source for the research scenes. The variation is
// intentional for each shot; a blanket word swap made ungrammatical prompts.
const roomVariations = {
  8: ["modern archive", "history museum"],
  13: ["modern archive", "university reading room"],
  18: ["present-day archive", "museum study room"],
  27: ["modern archive", "public records library"],
  31: ["sunlit archive", "museum study room"],
  34: ["modern archive", "research reading room"],
  41: ["modern archive", "museum storage room"],
  61: ["present-day archive", "public library"],
  66: ["modern archive", "research library"],
  74: ["modern archive", "library reading room"],
  79: ["an archive", "a library reading room"],
  80: ["modern archive", "library research room"],
  85: ["modern archive", "museum study room"],
  87: ["modern archive", "reading room"],
  91: ["present-day archive", "public library"],
  92: ["modern archive", "university reading room"],
};
const noTextVariations = new Set([0, 2, 3, 6, 9, 18, 19, 27, 29, 31, 35]);
const roomLightVariations = {
  18: "soft museum ceiling lights",
  29: "daylight from a skylight",
  30: "soft ceiling light",
  32: "daylight from a skylight",
  41: "bright ceiling lights",
  45: "morning light from above",
  50: "soft grey daylight from above",
  52: "diffuse overhead daylight",
  63: "light from a desk lamp",
  70: "soft ceiling light",
  73: "diffuse overhead daylight",
  79: "morning light from above",
  80: "soft ceiling light",
  81: "bright ceiling lights",
  83: "diffuse overhead daylight",
  86: "soft grey daylight from above",
  87: "daylight from a skylight",
  91: "morning light from above",
  92: "soft ceiling light",
  93: "sunlit tabletop from above",
  94: "bright ceiling lights",
};
for (const [index, scene] of doc.scenes.entries()) {
  if (scene.chapter === "第五章｜兩個候選姓名不能拼成一人") {
    scene.chapter = "第五章｜多熱路線碰上另一個下葬名";
  }
  if (scene.chapter === "第六章｜面具實物未留，死者身分未定") {
    scene.chapter = "第六章｜面具實物沒有留下";
  }
  if (index === 40) {
    // The drama renderer has no screenshot card. Keep the source-bound claim as a dated
    // evidence card; the registered public-domain photograph remains available for edit.
    scene.template = "big";
    scene.data = {
      kicker: "1698 年巴士底獄入獄登記",
      text: "**蒙面囚犯**",
      sub: "姓名、面具材質均未寫｜BnF／Commons；Funck-Brentano 1899",
    };
  }
  if (scene.id === "h07-22c31821") {
    scene.data.right = {
      heading: "1751《路易十四時代》",
      points: ["哪個部件被寫成鋼製？"],
    };
    scene.data.source = "Funck-Brentano 1899；Voltaire 1751 ch.25";
    scene.data.verdict = "書中的鋼製部件，不等於整副面具的實物鑑定";
    scene.claims = ["C03", "C13"];
  }
  if (index === 97) {
    scene.data = {
      kicker: "最後一道查驗",
      text: "**姓名與鐵，無法同時坐實**",
      sub: "沒有面具實物可驗材質；身分仍未確定",
    };
    scene.claims = ["C03", "C12", "C13", "C17"];
  }
  if (cardToShot.has(index)) {
    scene.template = "shot";
    scene.data = {};
  }
  if (nameSpellingCards.has(scene.id)) {
    const card = nameSpellingCards.get(scene.id);
    scene.template = card.template;
    scene.data = card.data;
    scene.claims = ["C05"];
  }
  if (scene.template === "shot") {
    if (!prompt[index]) throw new Error(`missing shot prompt at ${index} ${scene.id}`);
    // Keep the action and evidence mapping while varying the spaces and daylight cues.
    // This also prevents the archive desk from becoming the whole episode's scenery.
    let picture = prompt[index];
    if (roomVariations[index]) {
      const [from, to] = roomVariations[index];
      if (!picture.includes(from)) throw new Error(`room variation missing at ${index}`);
      picture = picture.replace(from, to);
    }
    if (noTextVariations.has(index)) picture = picture.replace(/\ba blank\b/g, "an unmarked").replace(/\bblank\b/g, "unmarked");
    if (roomLightVariations[index]) {
      if (!/\b(?:light|daylight) from [^,]*window[^,]*$/.test(picture)) throw new Error(`light variation missing at ${index}`);
      picture = picture.replace(/\b(?:light|daylight) from [^,]*window[^,]*$/, roomLightVariations[index]);
    }
    const lightVariation = {
      3: ["light from a high window", "light from above"],
      5: ["light from a high window", "light from the left"],
      13: ["light from a window", "light from the right"],
      17: ["light from a cloudy window", "soft daylight from the left"],
      27: ["light from a side window", "light from the right"],
    }[index];
    if (lightVariation) picture = picture.replace(...lightVariation);
    if ([14, 45].includes(index)) picture = picture.replace("her face", "her expression");
    if (index === 80) picture = picture.replace("her cautious face", "her cautious expression");
    if ([14, 30, 45, 85].includes(index)) picture = picture.replace("modern", "present-day");
    scene.data = {
      prompt: picture,
      camera: ["push in", "drift", "pull out", "pan left", "tilt up", "pan right", "tilt down"][index % 7],
      visual: "still",
    };
  }
}

// The museum's general "identity unknown" statement repeated the answer immediately
// before the conclusion. Keep its source in claims.md, but omit this one recap card.
const omittedSceneIds = new Set([
  "h07-c7a67f2d", // Repeats the final answer.
  "h07-19cabd14", "h07-7e41df5a", "h07-59982a41", "h07-d357e078",
  "h07-065e2185", "h07-22b75408", // Keep a short, sourced myth-to-record contrast.
  "h07-40285df9", "h07-f409b936", "h07-6c44c3b1", "h07-d50d4573",
  "h07-e8d89ffb", "h07-5438f7da",
  "h07-13f0cb04", // The following facsimile shot supplies the answer directly.
  "h07-7c22ba05", // Keep the 1698 admission record's first answer for chapter three.
]);
doc.scenes = doc.scenes.filter((scene) => !omittedSceneIds.has(scene.id));

// The new narrative rules need the identity trail to advance through the
// surviving records, not through more speculative biographies. These seven
// source-bound beats connect the admission, burial and candidate routes.
const addedScenes = new Map([
  ["h07-22215fc5", [{
    id: "h07-acbe0827", template: "shot",
    data: { prompt: "Medium shot in a seventeenth-century prison corridor, one middle-aged governor grips a closed sealed order beside a locked cell and looks stern, light from a high window", camera: "push in", visual: "still" },
    lines: [{ id: "acbe0827", text: "盧福瓦還命令：若多熱談起生活所需以外的事，聖馬爾就以死相威脅。" }],
    claims: ["C07"],
  }]],
  ["h07-7355e817", [{
    id: "h07-fe062c6b", template: "big",
    data: { kicker: "1698 年 9 月 18 日｜入獄登記", text: "**下午三點抵達｜晚上九點換塔**", sub: "同一筆記錄的兩個時刻｜Funck-Brentano 1899 轉錄" },
    lines: [{ id: "fe062c6b", text: "副官記他下午三點入獄，當晚九點才從第一座塔移往另一座。" }],
    claims: ["C01"],
  }, {
    id: "h07-8018f8bb", template: "shot",
    data: { prompt: "Medium shot in a Bastille tower corridor in 1698, one anonymous sergeant holds a ring of keys outside a closed cell, his alert expression above a plain coat, light from a high window", camera: "pan right", visual: "still" },
    lines: [{ id: "8018f8bb", text: "聖馬爾帶來的中士羅薩爾日，接手照看這名囚犯。" }],
    claims: ["C19"],
  }]],
  ["h07-4ee87957", [{
    id: "h07-4d05fe5b", template: "shot",
    data: { prompt: "Overhead view in a modern library reading room, one researcher aligns two separate closed plain register facsimile volumes, both covers unmarked, her focused expression visible at the table edge, light from a skylight", camera: "drift", visual: "still" },
    lines: [{ id: "4d05fe5b", text: "五年後的下葬簿，也留下羅薩爾日的簽名；兩筆記錄因此多了一個共同姓名。" }],
    claims: ["C19"],
  }]],
  ["h07-14d8d94f", [{
    id: "h07-9afd1ef2", template: "compare",
    data: {
      title: "1681 年：兩條路線分開",
      left: { heading: "聖馬爾", points: ["轉往埃克西耶"] },
      right: { heading: "馬提歐里", points: ["信稱留在皮涅羅爾"] },
      verdict: "這一趟沒有同行；後續移送仍待追查",
      source: "Topin 1870：1681 年聖馬爾信轉錄",
    },
    lines: [{ id: "9afd1ef2", text: "但一六八一年，聖馬爾轉往埃克西耶時，一封信明說馬提歐里會留在皮涅羅爾。" }],
    claims: ["C20"],
  }, {
    id: "h07-b8b073e3", template: "shot",
    data: { prompt: "Medium shot in a seventeenth-century prison office at Pignerol, one official folds an unmarked order on a bare desk, his troubled expression visible, light from an afternoon window", camera: "push in", visual: "still" },
    lines: [{ id: "b8b073e3", text: "一六九三年，一道命令仍在皮涅羅爾點名馬提歐里。" }],
    claims: ["C21"],
  }, {
    id: "h07-0231d434", template: "big",
    data: { kicker: "1693 年命令", text: "**衣袋布片上的字**", sub: "命令燒毀；是否執行、文字內容均不明｜Topin 1870" },
    lines: [{ id: "0231d434", text: "命令還要燒掉他和僕役寫過字、藏在衣服襯裡的衣袋布片。" }],
    claims: ["C21"],
  }, {
    id: "h07-3bfaa579", template: "big",
    data: { kicker: "1694 年｜再次移送", text: "**三名未具名囚犯赴島**", sub: "文件未點名其中任何一人｜Topin 1870 轉錄" },
    lines: [{ id: "3bfaa579", text: "但一六九四年，又有三名未具名囚犯送往聖瑪格麗特島；移送記述沒點出誰在其中。" }],
    claims: ["C22"],
  }]],
]);
doc.scenes = doc.scenes.flatMap((scene) => [scene, ...(addedScenes.get(scene.id) ?? [])]);

const originalLines = original.scenes
  .filter((scene) => !omittedSceneIds.has(scene.id))
  .flatMap((scene) => scene.lines.map(({ id, text }) => [id, text]));
const expectedLines = originalLines.map(([id, text]) => [id, revisedLines[id] ?? text]);
const newLines = doc.scenes.flatMap((scene) => scene.lines.map(({ id, text }) => [id, text]));
const newOriginalLines = newLines.filter(([id]) => ![...addedScenes.values()].flat().some((scene) => scene.lines[0].id === id));
if (expectedLines.length !== newOriginalLines.length || expectedLines.some(([id, text], index) =>
  newOriginalLines[index][0] !== id || newOriginalLines[index][1] !== text)) {
  throw new Error("unexpected narration or line id change");
}
// The owner-approved screenplay is produced by `tools/video/cli.mjs script`.
// Verify narration stays aligned, but never overwrite that SHA-bound approval.
const screenplay = readFileSync(join(here, "script.md"), "utf8");
const screenplayScenes = [...screenplay.matchAll(
  /^#### ([0-9]+)\. (h07-[a-z0-9-]+)(?:（[^）]+）)?\r?\n\r?\n旁白(?:（[^）]*）)?：([^\r\n]+)$/gm,
)];
if (screenplayScenes.length !== doc.scenes.length) {
  throw new Error(`screenplay has ${screenplayScenes.length} scenes, expected ${doc.scenes.length}`);
}
for (const [index, scene] of doc.scenes.entries()) {
  const [, number, sceneId, narration] = screenplayScenes[index];
  if (Number(number) !== index + 1 || sceneId !== scene.id ||
      scene.lines.length !== 1 || narration !== scene.lines[0].text) {
    throw new Error(`screenplay narration differs at scene ${index + 1} (${scene.id})`);
  }
}
writeFileSync(join(here, "video.json"), `${JSON.stringify(doc, null, 2)}\n`, "utf8");
