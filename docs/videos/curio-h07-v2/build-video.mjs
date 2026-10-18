// Rebuild the separate series-look preproduction source from the approved H07 narration.
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
);

// The fresh blind narrative review found an agenda sentence at the start of
// chapter five and two repeated conclusions. Keep IDs stable for traceability;
// changed lines must get new audio and fresh locale translations.
const revisedLines = {
  "45164df0": "他記下囚犯當晚約十點去世。",
  "baeadea2": "兩份文書一對照，關鍵的落差就從名字裡冒出來。",
  "029cafbf": "下葬摹本上的拼法，和密令裡的多熱並不相同。",
  "926246b2": "面具實物沒有留下，誰也不能替伏爾泰的「鐵」做材質鑑定；剩下的，是互相競爭的身分推論。",
};
for (const scene of doc.scenes) for (const line of scene.lines) {
  if (revisedLines[line.id]) line.text = revisedLines[line.id];
}

// All prompts describe what MiniMax should draw; the series look lives only in look.preset.
// Historical documents are blank props. Dates, names, and uncertainty remain in narration/cards.
const prompt = {
  0: "Medium shot inside a Bastille records office in 1703, one middle-aged deputy writes in a blank death register, his worried eyes above the page, light from a candle after dark",
  1: "Close-up in the same records office, one deputy closes a plain death register, his brows knit above the cover, light from a candle at the side",
  2: "Overhead view of a seventeenth-century official sealing a folded blank order on an oak desk, one red wax seal beneath his hand, light from a morning window",
  3: "Medium shot in a present-day archive, one researcher lifts a blank identity card and looks puzzled, stacked files behind her, light from a high window",
  4: "Wide shot at a Bastille stone gate in afternoon light, one cloaked prisoner with a plain unadorned face covering steps through the doorway, the heavy gate behind him, light from the courtyard",
  5: "Close-up in a prison records room, one clerk leans toward a closed admission register, his puzzled eyes fixed on its cover, light from a high window",
  6: "Medium shot in an eighteenth-century writing room, one scholar raises a folded blank letter to eye level, his face curious, light from a sunny window on the left",
  7: "Close-up in an eighteenth-century study, one reader pauses over a folded letter with a questioning expression, a plain face-covering prop on a distant shelf, light from a morning window",
  8: "Wide shot in a modern archive workroom, one researcher lays a printed burial-record facsimile beside an unmistakable theatre mask prop on a worktable, light from a skylight",
  9: "Close-up in a prison records office, one deputy lowers his quill toward a blank register, his hand and startled eyes in frame, light from the window",
  11: "Medium shot in a Bastille records office at night, one deputy closes a death register on a bare table, his face solemn, light from a single candle",
  12: "Wide shot of Saint-Paul parish graveyard in afternoon light, one gravedigger lowers his spade beside an unmarked grave, church stonework behind him, light from the open sky",
  13: "Medium shot in a modern archive, one researcher lifts a closed burial-register facsimile from a records box, her hopeful expression visible, light from a window",
  14: "Close-up in the archive, one researcher frowns while comparing two blank name cards, her face above the cards, light from the left",
  15: "Overhead view of one historian lifting a blank transcription card from a closed booklet on a sunlit desk, the card filling the foreground, light from above",
  16: "Medium shot in a modern archive, one historian places a second blank name card beside two others, her uncertain face visible, light from a tall window",
  17: "Close-up in a modern archive, one researcher holds three blank name cards apart with both hands, her doubtful eyes behind them, light from a cloudy window",
  18: "Medium shot in a present-day archive, one historian reaches toward a printed transcription of a 1669 order, a blank burial facsimile beside it, light from a high window",
  19: "Close-up in a seventeenth-century office, one official presses a wax seal onto a folded blank order, his concentrated face just above it, light from a morning window",
  21: "Wide shot at a Piedmontese Alpine fortress in daylight, one courier carries a sealed packet toward its gate, mountains beyond the wall, light from a pale sky",
  22: "Medium shot inside a stone prison corridor, one sentry studies a closed cell door with a baffled expression, his hand on an empty key ring, light from a high window",
  23: "Medium shot in a French prison corridor, one elderly governor carries a covered meal tray toward a cell, his intent face visible, light from a high window",
  25: "Close-up in a prison corridor, one governor pulls a wooden cell door shut with one hand, a narrow strip of light below it, daylight from the hall",
  26: "Medium shot in a prison guardroom, one sentry steps away from a closed cell door and looks uneasy, barred window behind him, daylight from the right",
  27: "Close-up in a modern archive, one historian pauses over a blank copy of a sealed letter, brows furrowed at a single blank note card, light from a side window",
  29: "Medium shot in a modern archive, one researcher holds two blank interpretation cards apart, her thoughtful face above them, light from a tall window",
  30: "Close-up in a modern archive, one researcher closes an empty biographical folder without filling it, her disappointed face visible, light from a cloudy window",
  31: "Medium shot in a sunlit archive, one historian examines a blank copy of a seventeenth-century order with a magnifying glass, an empty mask display case behind her, light from above",
  32: "Overhead view of one researcher placing two closed archival folders far apart on a daylight reading table, their covers blank, light from a wide window",
  34: "Medium shot in a modern archive, one researcher points to the space between two separate closed folders, her questioning face visible, light from a skylight",
  35: "Medium shot in a 1698 stone fortress office, one elderly governor raises a sealed transfer order to read its blank outer face, light from a morning window",
  36: "Wide shot near Sainte-Marguerite Island in daylight, one boatman rows a small skiff away from the low Fort Royal ramparts, light from a clear sky",
  38: "Close-up in a stone fortress corridor, one governor pushes a heavy wooden gate almost shut, its narrow light gap beside him, daylight from outside",
  39: "Close-up in a fortress office, one elderly governor studies a folded transfer order with a guarded expression, light from an afternoon window",
  41: "Medium shot in a modern archive, one archivist takes a closed admission register from a shelf, eyes fixed on the cover, light from a tall window",
  44: "Wide shot of a Bastille stone vestibule by day, one elderly governor enters carrying a closed folder, the gate behind him, light from the courtyard",
  45: "Close-up in a modern archive, one researcher holds two blank evidence cards apart, lips pressed in caution, light from a morning window",
  46: "Medium shot in an eighteenth-century writing room, one scholar folds a blank letter and pauses before sealing it, thoughtful face above the desk, light from a window",
  47: "Close-up in an eighteenth-century study, one reader raises a folded letter with a puzzled expression, a closed book on a distant shelf, light from a sunny window",
  48: "Overhead view in an eighteenth-century writing room, one scholar moves a quill over a blank letter sheet, light from the left window",
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
  75: "Overhead view in a sunlit research room, one historian moves a plain prisoner token toward the first of four miniature fortress models, a clearly hypothetical route on the table, light from above",
  79: "Close-up in an archive, one historian lifts a folded sealed-order facsimile by its blank outer edge, light from a morning window",
  80: "Medium shot in a modern archive, one historian holds a blank identity card apart from a closed death-register facsimile, her cautious face visible, light from a tall window",
  81: "Medium shot in a bright present-day library, one anonymous researcher raises a blank hypothesis sheet, her questioning face visible above a sealed archive box, light from a wide window",
  82: "Overhead close-up in a modern research room, one anonymous scholar moves a plain servant token beside a closed historical folder, the setup visibly a hypothesis on a table, light from above",
  83: "Overhead view on a present-day research table, one historian arranges two small crown tokens beside a closed coin chest prop, a hypothetical diagram, light from a daylight window",
  85: "Medium shot in a modern archive, one historian separates a blank hypothesis sheet from a closed official-order facsimile, her careful face visible, light from a skylight",
  86: "Close-up in a modern archive, one historian leaves a blank identity card beside a sealed death-register facsimile, light from a cloudy window",
  87: "Medium shot in a modern archive, one researcher slides a candidate token away from a separate blank burial card, her questioning face visible, light from a window",
  88: "Medium shot in a modern archive, one historian places a closed nineteenth-century burial-register facsimile on a reading table, her hand on the binding, light from a skylight",
  91: "Close-up in a present-day archive, one historian studies a closed burial facsimile, a candidate token resting beside it, her expression uncertain, light from a morning window",
  92: "Medium shot in a modern archive, one historian pauses with a candidate token halfway toward a closed burial facsimile, his uncertain face visible, light from a high window",
  93: "Overhead view of a modern research table, one historian pushes two candidate folders onto separate paths, their covers blank, light from a sunny window",
  94: "Medium shot in a modern archive, one archivist places two intact paper profile cutouts far apart, her careful expression visible, light from a high window",
  96: "Wide shot in a present-day museum, one visitor peers into an empty mask display case, his surprised face reflected faintly in the glass, light from a skylight",
};

const cardToShot = new Set([6, 18, 31, 47, 51, 57, 61, 71, 74, 75, 82, 87, 88, 91, 96]);
// Name the actual room or light source for the research scenes. The variation is
// intentional for each shot; a blanket word swap made ungrammatical prompts.
const roomVariations = {
  8: ["modern archive", "history museum"],
  13: ["modern archive", "university reading room"],
  16: ["modern archive", "public reading room"],
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
const noTextVariations = new Set([0, 2, 3, 6, 9, 16, 18, 19, 27, 29, 31, 35]);
const roomLightVariations = {
  16: "diffuse overhead daylight",
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
  if (index === 97) {
    scene.data = {
      kicker: "最後一道查驗",
      text: "**面具實物未留**",
      sub: "無實物可驗「鐵」；身分仍未確定",
    };
  }
  if (cardToShot.has(index)) {
    scene.template = "shot";
    scene.data = {};
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
    if ([14, 30, 45, 85].includes(index)) picture = picture.replace("modern", "present-day");
    scene.data = {
      prompt: picture,
      camera: ["push in", "drift", "pull out", "pan left", "tilt up", "pan right", "tilt down"][index % 7],
      visual: "still",
    };
  }
}

const originalLines = original.scenes.flatMap((scene) => scene.lines.map(({ id, text }) => [id, text]));
const newLines = doc.scenes.flatMap((scene) => scene.lines.map(({ id, text }) => [id, text]));
if (originalLines.length !== newLines.length || originalLines.some(([id, text], index) =>
  newLines[index][0] !== id || newLines[index][1] !== (revisedLines[id] ?? text))) {
  throw new Error("unexpected narration or line id change");
}
writeFileSync(join(here, "video.json"), `${JSON.stringify(doc, null, 2)}\n`, "utf8");

// A readable narration index is kept beside the machine source. Every sentence comes from
// the approved original; the new bracketed scene types describe only the visual plan.
const script = [
  "# H07-v2｜鐵面人是誰？",
  "",
  "> 沿用 H07 的 100 個行 ID；96 句旁白逐字沿用，4 句依新版盲評修正，須重新合成與查核。方括號只標本版預定畫面。史實和查核界線見 claims.md、research.md 與原版 verify-1.md／verify-2.md。",
  "",
];
let chapter = null;
for (const [index, scene] of doc.scenes.entries()) {
  if (scene.chapter && scene.chapter !== chapter) {
    chapter = scene.chapter;
    script.push(`## ${chapter}`, "");
  }
  for (const line of scene.lines) script.push(`${index + 1}. **${line.id}** [${scene.template}] ${line.text}`);
}
script.push("", "## 來源", "", "見 [claims.md](claims.md)、[research.md](research.md)；原版視覺與史實覆核保留於 [verify-1.md](../curio-h07/verify-1.md) 和 [verify-2.md](../curio-h07/verify-2.md)。", "");
writeFileSync(join(here, "script.md"), `${script.join("\n")}\n`, "utf8");
