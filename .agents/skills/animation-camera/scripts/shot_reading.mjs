#!/usr/bin/env node
// 鏡頭讀法：一個分鏡的每個鏡頭，工具裡三個關鍵字讀法各讀到什麼，以及寫法上會讓某一個讀法讀錯、
// 讓一張圖或一段素材白買的陷阱。
//
//   node .agents/skills/animation-camera/scripts/shot_reading.mjs <video.json> [--shot a,b] [--json] [--strict]
//   node .agents/skills/animation-camera/scripts/shot_reading.mjs --file <one-shot.json> [--json] [--strict]
//
// <video.json> 是一部有角色的漫劇；長度照 lint 的估法（tools/video/core/timeline.mjs
// estimateTimeline），旁邊若有 series.json 且 production.profile 存在，就用 production profile 的
// 8 秒素材規則。--file 讀單一鏡頭的 JSON：{ camera, prompt, motion, characters?, visual?, source?,
// lines?, look?, production? }；characters 可以是 id 字串，或 { id, name, appearance } 物件（有外觀
// 才算得出關鍵影格 prompt 的長度）。
//
// 每個鏡頭印一塊：id、visual（clip／still／cut from <shot>@<from_s>）、craft 的景別與類別
// （tools/video/core/craft.mjs shotSize）、craft 的運鏡（craft cameraMove）、插圖投影片的運鏡
// （tools/video/core/drama.mjs cameraMove）、assemble 的運鏡與第 0 格驗不驗 PSNR
// （tools/video/assemble/drama.mjs motionMove）、只有看（isLookOnly）、台詞數與說話的人、角色；接著
// 是找到的陷阱，每個附修法。切鏡另對來源鏡頭買到的秒數（tools/video/media/clips.mjs clipSeconds）
// 比一次：lint 放行而 clips 會 needs_review 的切鏡在這裡先報。--json 印同樣的東西成結構；
// --strict 有陷阱就以 1 結束。
// 結束碼 0；--strict 且有陷阱 1；檔案讀不到、不是漫劇、--shot 一個都不在 2。
//
// 這裡只讀文字，不買任何東西；三個讀法都是從 tools/video 匯入的那一份，所以這裡印的就是 lint、
// assemble 與 worker 會讀到的。每個數字的出處寫在它旁邊的常數上。
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { cameraMove as craftCameraMove, isLookOnly, normalize, shotSize, sizesDisagree } from "../../../../tools/video/core/craft.mjs";
import { MAX_SHOT_CHARACTERS, MAX_SOURCE_CLIP_SECONDS, cameraMove as slidesCameraMove, hasCast, isSourced, resolveLook, shotAppearancePrompt } from "../../../../tools/video/core/drama.mjs";
import { motionMove } from "../../../../tools/video/assemble/drama.mjs";
import { estimateTimeline, FPS } from "../../../../tools/video/core/timeline.mjs";
import { clipSeconds } from "../../../../tools/video/media/clips.mjs";

export { craftCameraMove, isLookOnly, motionMove, shotSize, sizesDisagree, slidesCameraMove };

// 工具規定：apps/api/app/video_media/schemas.py MAX_PROMPT_CHARS，tools/video/media/keyframes.mjs
// shotPrompt 用 .slice(0, 4000) 砍尾。
export const MAX_PROMPT_CHARS = 4000;
// 工具規定：tools/video/core/lint.mjs productionShotProblems 以 8 * FPS 限制 production profile 的
// 鏡頭與來源切段；tools/video/media/clips.mjs clipSeconds 在 veo-3.1* 配 1080p 時固定買 8 秒
// （720p 照需求貼 4/6/8）。沒有 profile 時來源買到的秒數用 clipSeconds 本人算：伺服器預設的
// gemini-omni-1.1-flash（apps/api/app/video_media/catalog.py DEFAULT_CLIP）與 H3 都是
// clamp(ceil(frames/30), 4, 10)。
export const PRODUCTION_CLIP_SECONDS = 8;
/** 來源鏡頭會買到的秒數：有 profile 固定 8，否則 clipSeconds 不帶模型（4–10）。 */
export const boughtSeconds = (seconds, production) => (production ? PRODUCTION_CLIP_SECONDS : clipSeconds(Math.ceil(seconds * FPS)));
// 工具規定：tools/video/assemble/drama.mjs MOTION_DRIFT_ZOOM；這裡只拿來寫進訊息。
const DRIFT_ZOOM_PERCENT = 4;

// craft.mjs 的分類（FACE、WIDE 沒有匯出，照抄）：臉是 ecu、cu、mcu、ots；全景或多人是 ws、group。
const FACE = new Set(["ecu", "cu", "mcu", "ots"]);
const WIDE = new Set(["ws", "group"]);
export const family = (size) => (size === null ? null : FACE.has(size) ? "face" : WIDE.has(size) ? "wide" : size);
const FAMILY_LABEL = { face: "臉", wide: "全景或多人", insert: "插鏡", ms: "中景", pov: "POV" };

// prompt 或 motion 說某人不在畫面裡的寫法（drama-craft.md 第四節：反應鏡與插鏡放畫外那個人的那一句）。
const OFF_SCREEN = /\boff[- ]?screen\b|\bout of (?:the )?frame\b|\bo\.s\.|\bv\.o\.|\bvoice[- ]?over\b|\bunseen\b|\bnot (?:in|visible in|seen in) (?:the )?(?:frame|shot|picture)\b|\boutside (?:the )?frame\b|\bfrom off\b|畫外|不在畫面/i;

// camera 行裡人的動作：主詞（代名詞、the／his／her＋人或身體部位、角色名）接一個動詞。整字讀法
// （assemble motionMove、slides cameraMove）會把其中的 pushes、rises、fixed 讀成運鏡。
const PERSON_NOUN = "(?:girl|boy|man|woman|bride|groom|witness|uncle|aunt|emperor|king|queen|father|mother|son|daughter|guard|servant|maid|child|couple|guest|crowd|figure|lady|prince|princess|bird|hands?|fingers?|face|eyes|head|gaze)";
const VERB = "(?:push|pull|ris|rose|pan|tilt|track|follow|zoom|widen|back|descend|cran|orbit|drift|mov|fix|stand|sit|turn|walk|step|enter|leav|lift|rais|lower|set|put|tak|hold|look|glanc|star|reach|grab|open|clos|tear|pour|sign|writ|read|speak|say|nod|shak|bow|kneel|run|cross|approach|lean|point|slap|throw|drop|pick|offer|giv|pass|trembl|tighten|fall|smil|frown|cri|laugh|breath|wait|paus|hesitat|wip|strik|lung)(?:e?s|es|ed|ing|e)?";
const PRONOUN_VERB = new RegExp(`\\b(she|he|they|someone|somebody)\\s+(${VERB})\\b`);
const NOUN_VERB = new RegExp(`\\b(?:the|a|his|her|their|[a-z]+['’]s)\\s+(?:[a-z'’-]+\\s+){0,2}?(${PERSON_NOUN})\\s+(${VERB})\\b`);
// 運鏡自己的字，不是人：大寫開頭的字接動詞時先排除它們。
const CAMERA_WORDS = new Set(["camera", "slow", "slowly", "gentle", "gently", "subtle", "quick", "fast", "smooth", "steady", "handheld", "low", "high", "static", "locked", "fixed", "tripod", "medium", "wide", "close", "extreme", "insert", "tight", "loose", "dolly", "crane", "steadicam", "pov", "over", "two", "three", "group", "establishing", "aerial", "overhead", "oblique", "table", "then", "and", "lens", "frame", "shot", "view", "angle", "push", "pull", "pan", "tilt", "track", "zoom", "truck", "orbit", "arc", "drift"]);
const NAME_VERB = new RegExp(`(?<!^)(?<![.;:,]\\s)\\b([A-Z][a-z]+)\\s+(${VERB})\\b`, "g");

const lower = (text) => String(text ?? "").toLowerCase();
const escapeRe = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

// 「誰在畫外」只看畫外片語在說誰：名字後面到片語之間只有這些字（「Wei off screen」「Zhao speaks
// off screen」「Zhao's voice from off screen」）才算那個人在畫外。中間有 toward／at／to 這類方向字
// （「Yan's sword toward Wei off screen right」）時，畫外的是方向字後面的東西，前面動手的人在畫面裡。
const OFF_SCREEN_BRIDGE = /^(?:['’]s\s+voice\s+)?(?:(?:is|are|stays?|stands?|waits?|remains?|sits?|speaks?|says?|talks?|calls?|shouts?|whispers?|answers?|replies?|laughs?|cries?|out|on|now|still|just|comes?|heard)\s+)*(?:from\s+)?$/i;
// 看、瞥、盯、指向畫外：動作的人在畫面裡，畫外的是他看的東西（片語後面點名的人才是畫外的）。
const OFF_SCREEN_LOOK = /^(?:(?:now|still|just|slowly|briefly|then)\s+)*(?:looks?|glances?|stares?|gazes?|watches|peers?|points?|turns?|squints?|nods?|gestures?)(?:\s+(?:up|down|back|away|again))*\s+$/i;
const OFF_SCREEN_TARGET = /\b(?:toward|towards|at|to|into|past|beyond|across|for)\b/i;
const OFF_SCREEN_AFTER = /^(?:(?:left|right|of)\s+)*$/i;

/**
 * 一個含畫外片語的子句裡，片語說的是哪個角色。
 * 回 { ids, ambiguous }：ids 是片語的主詞（名字緊接片語，或只隔說話、站著這類字）；片語前面最近的名字
 * 隔著方向字（toward、at…）時它是動手的人、不在畫外，回空；隔著別的字說不準時回那個名字並標 ambiguous，
 * 讓人看一眼，不叫人把可能入鏡的角色刪掉。沒點任何名字時 ids 是 null（交給呼叫端照說話者判斷）。
 */
export function offScreenSubjects(part, cast) {
  const phrase = OFF_SCREEN.exec(part);
  if (!phrase) return { ids: [], ambiguous: false };
  const mentions = [];
  for (const character of cast) {
    for (const label of [character.id, character.name]) {
      if (typeof label !== "string" || !label.length) continue;
      for (const match of part.matchAll(new RegExp(`(?<![\\w-])${escapeRe(label)}(?![\\w-])`, "gi"))) mentions.push({ id: character.id, start: match.index, end: match.index + match[0].length });
    }
  }
  if (!mentions.length) return { ids: null, ambiguous: false };
  const before = mentions.filter((mention) => mention.end <= phrase.index).sort((a, b) => b.end - a.end)[0];
  if (before) {
    const gap = part.slice(before.end, phrase.index);
    if (OFF_SCREEN_BRIDGE.test(gap.trim() ? `${gap.trim()} ` : "")) return { ids: [before.id], ambiguous: false };
    if (!/^from\b/i.test(phrase[0]) && OFF_SCREEN_LOOK.test(gap.trim() ? `${gap.trim()} ` : "")) {
      const after = mentions.filter((mention) => mention.start >= phrase.index + phrase[0].length).sort((a, b) => a.start - b.start)[0];
      const between = after ? part.slice(phrase.index + phrase[0].length, after.start).trim() : null;
      return { ids: after && /^(?:(?:left|right|of|at|to|toward|towards)\s*)*$/i.test(between) ? [after.id] : [], ambiguous: false };
    }
    if (OFF_SCREEN_TARGET.test(gap)) return { ids: [], ambiguous: false };
    return { ids: [before.id], ambiguous: true };
  }
  const after = mentions.filter((mention) => mention.start >= phrase.index + phrase[0].length).sort((a, b) => a.start - b.start)[0];
  if (after && OFF_SCREEN_AFTER.test(part.slice(phrase.index + phrase[0].length, after.start).trim() ? `${part.slice(phrase.index + phrase[0].length, after.start).trim()} ` : "")) return { ids: [after.id], ambiguous: false };
  return { ids: after ? [after.id] : [], ambiguous: Boolean(after) };
}

// 編輯判斷：look.motion 裡影片模型會讀成運鏡指令的字。三個讀法只讀 camera 行、看不到 look.motion；
// 是 clipPrompt（tools/video/media/clips.mjs）把它接在 camera 後面，所以鎖定的鏡頭要看的是影片模型
// 讀到的自然語言：preset 用的「camera move」「drifting camera」「push in」，與單獨出現的
// push／pull／pan／tilt／zoom／dolly／track／truck／orbit／crane／handheld／steadicam／drift。
const LOOK_MOVE_WORDS = /\bcamera (?:move|moves|movement|movements|motion|drift|drifts|drifting|pan|pans|tilt|tilts|push|pushes|zoom|zooms)\b|\b(?:drift|drifts|drifting|dolly|dollies|dollying|zoom|zooms|zooming|pan|pans|panning|tilt|tilts|tilting|push|pushes|pushing|pull|pulls|pulling|track|tracks|tracking|truck|trucks|trucking|orbit|orbits|orbiting|crane|cranes|craning|handheld|steadicam|push-in|pull-out|pull-back|pullback)\b/;

/** look.motion 裡第一個運鏡字（原文小寫），沒有就 null：鎖定的 clip 只有在這時才真的收到兩個指令。 */
export function lookMotionMove(text) {
  const word = LOOK_MOVE_WORDS.exec(lower(text));
  return word ? word[0] : null;
}

/** 像 tools/video/core/drama.mjs shotCast 一樣，把 data.characters 換成角色物件，套上 character_looks。 */
function castOf(data, castById) {
  return (Array.isArray(data.characters) ? data.characters : []).map((id) => {
    const character = castById.get(id);
    if (!character) return null;
    const chosen = data.character_looks?.[id];
    const look = Array.isArray(character.shot_looks) ? character.shot_looks.find((item) => item?.id === chosen) : null;
    return look ? { ...character, appearance: look.appearance, shot_look: look.id } : character;
  }).filter(Boolean);
}

/** 關鍵影格送出的 prompt，照 tools/video/media/keyframes.mjs shotPrompt 組（砍尾之前的長度）。 */
export function keyframePrompt(data, look, cast) {
  const labels = shotAppearancePrompt(cast);
  return `${data.prompt ?? ""}. Style: ${look.style}${data.camera ? `. Camera: ${data.camera}` : ""}${labels ? `. Characters: ${labels}` : ""}`;
}

/** camera 行裡找到的人的動作，或 null。 */
export function personClause(camera, names = []) {
  const text = String(camera ?? "");
  const low = text.toLowerCase();
  const pronoun = PRONOUN_VERB.exec(low);
  if (pronoun) return pronoun[0];
  const noun = NOUN_VERB.exec(low);
  if (noun) return noun[0];
  for (const match of text.matchAll(NAME_VERB)) {
    if (!CAMERA_WORDS.has(match[1].toLowerCase())) return match[0];
  }
  const known = names.filter((name) => /^[a-z][a-z0-9-]*$/i.test(name));
  if (known.length) {
    const named = new RegExp(`\\b(${known.map(escapeRe).join("|")})\\s+(${VERB})\\b`, "i").exec(text);
    if (named) return named[0];
  }
  return null;
}

/** 一個鏡頭的三種讀法與基本事實。`row` 是 craft.normalize 的一列，`scene` 是原始場景。 */
export function readShot(row, scene, ctx) {
  const data = row.data ?? {};
  const sourced = isSourced(scene);
  const visual = sourced ? "cut" : data.visual === "still" ? "still" : "clip";
  const assemble = motionMove(data, row.id);
  const cast = castOf(data, ctx.castById);
  const speakers = [...new Set(row.lines.map((line) => line.speaker ?? "narrator"))];
  return {
    id: row.id,
    visual,
    visual_label: sourced ? `cut from ${data.source.shot}@${data.source.from_s}s` : visual,
    seconds: +row.seconds.toFixed(2),
    silent: row.silent,
    size: { craft: shotSize(data), family: family(shotSize(data)), camera: shotSize({ camera: data.camera }), prompt: shotSize({ prompt: data.prompt }) },
    move: {
      craft: craftCameraMove(data),
      slides: slidesCameraMove(data),
      assemble: { name: assemble.name, psnr_checked: assemble.startsAtIdentity, ...(assemble.direction ? { direction: assemble.direction } : {}) },
    },
    look_only: isLookOnly(data),
    lines: row.lines.length,
    speakers,
    characters: Array.isArray(data.characters) ? [...data.characters] : [],
    keyframe_prompt_chars: keyframePrompt(data, ctx.look, cast).length,
    cast_known: cast.length === (data.characters ?? []).length,
  };
}

/** 陷阱的 id，照 shotTraps 檢查的順序；tools/animation-camera.test.mjs 要求每一個都有一個案例。 */
export const TRAP_IDS = ["size.none", "size.disagree", "still.drift", "still.locked", "camera.person", "move.disagree", "motion.empty", "motion.look", "look.motion", "cast.offscreen", "cast.speaker", "cast.count", "prompt.camera", "prompt.length", "source.shot", "source.length", "source.bought"];

/** 寫法上的陷阱：每個 { id, message, fix }。 */
export function shotTraps(reading, scene, ctx) {
  const data = scene.data ?? {};
  const camera = String(data.camera ?? "");
  const prompt = String(data.prompt ?? "");
  const motion = String(data.motion ?? "");
  const traps = [];
  const add = (id, message, fix) => traps.push({ id, message, fix });
  const { size, move, visual } = reading;
  const buysPicture = visual !== "cut";

  // 景別。
  if (size.camera === null) {
    add("size.none", size.prompt
      ? `\`camera\` 沒寫景別；craft shotSize 退而讀 prompt，讀到 ${size.prompt}（${FAMILY_LABEL[family(size.prompt)] ?? size.prompt}），圖片模型也只從 prompt 猜`
      : "`camera` 沒寫景別，prompt 也沒有明寫的景別：craft 算 unknown（size.named），圖片模型照習慣畫一個中景",
      "`camera` 第一個詞寫景別（Wide、Medium shot、Medium close-up、Close-up、Insert…），運鏡或 locked 寫在後面");
  }
  if (sizesDisagree(data)) {
    add("size.disagree", `\`camera\` 讀成 ${size.camera}（${FAMILY_LABEL[family(size.camera)] ?? size.camera}），prompt 讀成 ${size.prompt}（${FAMILY_LABEL[family(size.prompt)] ?? size.prompt}）：shotPrompt 把兩段都送給圖片模型（craft 列 size.agree）`, "景別只寫一次，寫在 camera；prompt 描述第一格的內容，不再寫景別");
  }

  // 靜圖的運鏡。
  if (visual === "still") {
    if (move.assemble.name === "drift" && !/\bdrift/i.test(camera)) {
      add("still.drift", `still 鏡頭的 \`camera\` 沒寫表裡的運鏡（${camera ? `「${camera}」` : "空的"}）：assemble motionMove 讀不到就 drift（放大 ${DRIFT_ZOOM_PERCENT}%、略往${move.assemble.direction === "left" ? "左" : "右"}）`, "寫表裡的字：push in、pull out、pan left／right、tilt up／down、drift，或 locked");
    }
    if (move.assemble.name === "locked") {
      add("still.locked", `still 鏡頭寫了鎖定：整格 ${reading.seconds} s 一動不動（zoompanExpr locked 是 z=1），看起來像定格`, "設計好的 hold 就保留並在回報說明；否則給 push in 或 drift，或改 visual clip");
    }
  }

  // camera 行裡的人，以及三個讀法的分歧。
  const clause = personClause(camera, ctx.names);
  if (clause) {
    add("camera.person", `\`camera\` 裡有人的動作「${clause}」：assemble motionMove 與 slides cameraMove 以整字讀，會把其中的運鏡字當 camera move；craft cameraMove 只認子句開頭的運鏡，讀到 ${move.craft}`, "人的動作寫進 motion；camera 只寫景別＋運鏡（或 locked）");
  }
  const craftLocked = move.craft === "locked", assembleLocked = move.assemble.name === "locked";
  if (craftLocked !== assembleLocked || (move.craft === "none" && move.assemble.name !== "drift")) {
    const reason = craftLocked && move.assemble.name === "drift"
      ? "寫了 drift 字就贏過 static／locked（assemble 的表 drift 排第一）"
      : assembleLocked && !craftLocked
        ? "fixed／static 之類的字接在 camera、frame、shot 以外的字後面：craft 不算 locked，assemble 以整字算"
        : "運鏡字接在人物或片語後面：craft 不認，assemble 以整字認";
    add("move.disagree", `craft cameraMove 讀 ${move.craft}、slides cameraMove 讀 ${move.slides}、assemble motionMove 讀 ${move.assemble.name}：${reason}`, "一行一種運鏡，用表裡的字；要鎖定就只寫 locked，要漂移就只寫 drift");
  }

  // clip 的動作與 look.motion。
  if (visual === "clip") {
    if (!motion.trim()) {
      add("motion.empty", `clip 鏡頭沒寫 motion：clipPrompt 只剩 camera 與 look.motion，買來的 ${reading.seconds} s 素材裡沒有事發生`, "寫「誰＋動詞＋對象」的一個動作");
    } else if (reading.look_only && ["ws", "ms", "group", "pov"].includes(size.craft)) {
      add("motion.look", `${size.craft} 的 clip 鏡頭只有看、呼吸或顫抖（isLookOnly），不是臉的反應鏡：買 ${reading.seconds} s 素材拍一個人站著`, "寫一個對人或對物做的動作；真的只是反應就改成臉的景別，或改 visual still");
    }
    // look.motion 沒有運鏡字（例如試拍覆寫成「One clearly motivated character or prop action per
    // clip, …」）就不是矛盾，只在第一行印出它仍會接上；有運鏡字才是兩個指令。
    const lookMove = lookMotionMove(ctx.look.motion);
    if (craftLocked && lookMove) {
      add("look.motion", `\`camera\` 鎖定（craft 讀 locked），但 look.motion「${ctx.look.motion}」含運鏡字「${lookMove}」：clipPrompt 把 motion、camera、look.motion 接成一句，影片模型同時收到鎖定與運鏡`, "這部的 look.motion 改成不含運鏡字的句子（例如 subtle natural motion, consistent character, no morphing, no cuts），在 look 跑之前改（它在 lookHash 裡）；或這個鏡頭別鎖定");
    }
  }

  // 角色。
  const listed = Array.isArray(data.characters) ? data.characters : [];
  const speaking = reading.speakers.filter((speaker) => speaker !== "narrator");
  // 畫外的句子以逗號切：「Lin lifts the cup, Zhao speaks off screen」只有後半說的是畫外的人。
  const clauses = `${prompt}. ${motion}`.split(/[.;,。；，]/).map((part) => part.trim()).filter((part) => OFF_SCREEN.test(part));
  const offScreen = new Map();
  for (const part of clauses) {
    // 句子點了名就只看畫外片語說的那個人（offScreenSubjects）；沒點名（"a voice from off screen"）才假設是在這鏡說話、又被列進畫面的人。
    const { ids, ambiguous } = offScreenSubjects(part, [...ctx.castById.values()]);
    for (const id of (ids ?? speaking).filter((id) => listed.includes(id))) {
      if (!offScreen.has(id) || offScreen.get(id).ambiguous) offScreen.set(id, { part, ambiguous: ids !== null && ambiguous });
    }
  }
  for (const [id, { part, ambiguous }] of offScreen) {
    if (ambiguous) {
      add("cast.offscreen", `「${part}」有畫外片語，但讀不出它說的是不是 ${id}（名字與片語之間隔了別的字），而 data.characters 列了 ${id}`, `${id} 在畫面裡就把畫外的人或東西寫成自己的子句（「Wei off screen right」），${id} 留在 characters；真的在畫外才從 characters 拿掉`);
    } else {
      add("cast.offscreen", `prompt 或 motion 說 ${id} 在畫外（「${part}」），但 data.characters 列了 ${id}：關鍵影格會把 ${id} 畫進畫面，judge 也會找這張臉`, `從 characters 拿掉 ${id}；台詞的 speaker 留著`);
    }
  }
  if (!clauses.length) {
    for (const id of speaking.filter((speaker) => !listed.includes(speaker))) {
      add("cast.speaker", `台詞的 speaker ${id} 不在 data.characters，prompt 也沒說 off screen：圖裡不會有 ${id}，觀眾聽到聲音卻看不到是誰`, `聽者鏡或插鏡就在 prompt 寫「${id} speaks off screen」；否則把 ${id} 加進 characters（最多 ${MAX_SHOT_CHARACTERS} 個）`);
    }
  }
  if (listed.length > MAX_SHOT_CHARACTERS) {
    add("cast.count", `data.characters 列了 ${listed.length} 個，MAX_SHOT_CHARACTERS 是 ${MAX_SHOT_CHARACTERS}（lint 拒收；每個都要一張參考圖，MAX_REFERENCES 4 還要留給 style_frames）`, "拆成兩個鏡頭，或讓多出的人成為 prompt 裡沒有臉的背景人物（不列 id）");
  }

  // prompt 與關鍵影格。
  if (buysPicture) {
    const cameraLow = camera.trim().toLowerCase().replace(/[.;,]+$/, "");
    if (cameraLow.length >= 8 && prompt.toLowerCase().includes(cameraLow)) {
      add("prompt.camera", `prompt 照抄了 camera 整行（「${camera.trim()}」）：shotPrompt 後面還會接「Camera: …」，圖片模型讀到兩次`, "prompt 刪掉那句；景別與運鏡只在 camera");
    }
    if (reading.keyframe_prompt_chars > MAX_PROMPT_CHARS) {
      add("prompt.length", `關鍵影格 prompt 組起來 ${reading.keyframe_prompt_chars} 字，超過 MAX_PROMPT_CHARS ${MAX_PROMPT_CHARS}：shotPrompt 用 slice 砍尾，先掉的是 Characters 的外觀標籤`, "精簡 prompt（lint 上限 1000）、look.style（600）與角色 appearance（800）");
    }
  }

  // 從別的鏡頭的素材切出來的鏡頭。
  if (visual === "cut") {
    const source = data.source;
    const origin = ctx.shotsById.get(source.shot);
    if (!ctx.single && (!origin || isSourced(origin) || origin.data?.visual === "still")) {
      add("source.shot", `source.shot ${source.shot} ${!origin ? "不在這份檔案裡" : isSourced(origin) ? "自己也是切出來的" : "是 still，沒有素材可切"}`, "source.shot 指向一個 visual clip、有自己素材的鏡頭");
    }
    const limit = ctx.production ? PRODUCTION_CLIP_SECONDS : MAX_SOURCE_CLIP_SECONDS;
    const end = source.from_s + reading.seconds;
    const estimated = reading.silent ? "（沒有台詞也沒有 action_seconds，以 craft 的 SILENT_SHOT_SECONDS 估）" : "";
    if (Number.isFinite(source.from_s) && end > limit) {
      add("source.length", `從 ${source.shot} 的素材 ${source.from_s} s 起切，本鏡約 ${reading.seconds} s${estimated}，結尾在 ${end.toFixed(1)} s，超過 ${limit} s（${ctx.production ? "production profile 的素材固定 8 s：lint productionShotProblems" : "MAX_SOURCE_CLIP_SECONDS：tools/video/core/drama.mjs"}）`, "from_s 提早，或縮短這個鏡頭的台詞");
    } else if ((ctx.route ?? "server") === "server" && Number.isFinite(source.from_s) && origin && !isSourced(origin) && origin.data?.visual !== "still" && ctx.secondsById.has(source.shot)) {
      // 網頁路線（--route hailuo|kling）的母鏡頭照 animation-preproduction 的 shot_plan.mjs 買到蓋住每一個切鏡，不在這裡算。
      // lint 的上限是素材「最多」幾秒；來源真正買到的是 clipSeconds 給的（沒有 profile 時 4–10），
      // clips.mjs 在來源買下之後才對它標 needs_review，這裡先算。
      const originSeconds = ctx.secondsById.get(source.shot);
      const bought = boughtSeconds(originSeconds, ctx.production);
      if (end > bought) {
        add("source.bought", `從 ${source.shot} 的素材 ${source.from_s} s 起切，本鏡約 ${reading.seconds} s${estimated}，結尾在 ${end.toFixed(1)} s；${source.shot} 約 ${originSeconds.toFixed(2)} s，伺服器預設的 Omni／H3 照 clipSeconds 只買 ${bought} s（clamp(ceil(frames/30), 4, 10)），lint 的 ${limit} s 放行，clips 要到 ${source.shot} 買下之後才把這鏡標 needs_review`, `from_s 提早到 ${Math.max(0, bought - reading.seconds).toFixed(1)} s 以內（會重播 ${source.shot} 用過的段），或把 ${source.shot} 的台詞寫長到買 ${Math.ceil(end)} s，或走 veo-3.1* 1080p（固定 8 s）`);
      }
    }
  }
  return traps;
}

/**
 * 整份 video.json 的讀法：{ file, production, look, shots: [reading + traps], summary }。
 * `series` 是旁邊的 series.json（有 production.profile 就套 8 秒規則），`only` 是要看的鏡頭 id。
 */
export function readDocument(doc, { file = "video.json", series = null, only = null, single = false, route = "server" } = {}) {
  let timeline = null;
  try {
    timeline = estimateTimeline(doc);
  } catch {
    timeline = null;
  }
  const { shots: rows } = normalize(doc, { timeline });
  const look = resolveLook(doc.look);
  const castById = new Map((Array.isArray(doc.characters) ? doc.characters : []).filter((character) => character && typeof character === "object").map((character) => [character.id, character]));
  const names = [...castById.values()].flatMap((character) => [character.id, character.name]).filter((name) => typeof name === "string");
  const shotsById = new Map(doc.scenes.filter((scene) => scene?.template === "shot").map((scene) => [scene.id, scene]));
  const secondsById = new Map(rows.filter((row) => !row.card && Number.isFinite(row.seconds)).map((row) => [row.id, row.seconds]));
  const ctx = { look, castById, names, shotsById, secondsById, single, route, production: Boolean(series?.production?.profile) };
  const shots = [];
  rows.forEach((row, index) => {
    const scene = doc.scenes[index];
    if (row.card) return;
    if (only && !only.includes(row.id)) return;
    const reading = readShot(row, scene, ctx);
    shots.push({ ...reading, traps: shotTraps(reading, scene, ctx) });
  });
  const byKind = {};
  for (const shot of shots) for (const trap of shot.traps) byKind[trap.id] = (byKind[trap.id] ?? 0) + 1;
  return {
    file,
    cast: hasCast(doc),
    production: ctx.production,
    look: { preset: look.preset, motion: look.motion, move: lookMotionMove(look.motion) },
    shots,
    summary: { shots: shots.length, traps: shots.reduce((sum, shot) => sum + shot.traps.length, 0), by_kind: byKind },
  };
}

/** --file 的單鏡 JSON 包成一部一鏡的漫劇。 */
export function shotFileDocument(shot) {
  const characters = Array.isArray(shot.characters) ? shot.characters : [];
  const cast = characters.map((each) => (typeof each === "string" ? { id: each, name: each, appearance: "" } : each)).filter((each) => each && typeof each.id === "string");
  const data = { prompt: shot.prompt ?? "", camera: shot.camera ?? "", motion: shot.motion ?? "", characters: cast.map((each) => each.id) };
  for (const key of ["visual", "source", "character_looks", "transition", "fit"]) if (shot[key] !== undefined) data[key] = shot[key];
  const scene = { id: shot.id ?? "shot", template: "shot", data, lines: Array.isArray(shot.lines) ? shot.lines.map((line, index) => ({ id: line.id ?? `line-${index}`, ...line })) : [] };
  if (Number.isFinite(shot.action_seconds)) scene.action_seconds = shot.action_seconds;
  return { doc: { format: "drama", characters: cast, look: shot.look, scenes: [scene] }, series: shot.production ? { production: { profile: true } } : null };
}

const yesNo = (value) => (value ? "yes" : "no");

/** 文字版：每個鏡頭一塊，最後一行總結。 */
export function renderReading(report) {
  const out = [];
  const kinds = report.shots.reduce((counts, shot) => { counts[shot.visual] = (counts[shot.visual] ?? 0) + 1; return counts; }, {});
  out.push(`${report.file}: ${report.shots.length} 個鏡頭（${["clip", "still", "cut"].map((kind) => `${kinds[kind] ?? 0} ${kind}`).join("、")}）；look ${report.look.preset}${report.look.motion ? `，look.motion「${report.look.motion}」${report.look.move ? `（含運鏡字「${report.look.move}」：鎖定的 clip 報 look.motion）` : "（沒有運鏡字；仍接在每支 clip 的 camera 後面）"}` : "，沒有 look.motion"}；production profile ${yesNo(report.production)}${report.cast ? "" : "；沒有角色（craft 的列不適用）"}`);
  for (const shot of report.shots) {
    out.push("");
    out.push(`[${shot.id}] ${shot.visual_label} · 約 ${shot.seconds} s${shot.silent ? "（無台詞，估）" : ""} · ${shot.lines} lines（${shot.speakers.join(", ") || "-"}） · characters: ${shot.characters.join(", ") || "-"}`);
    const where = shot.size.camera !== null ? "camera" : shot.size.prompt !== null ? "prompt" : "-";
    out.push(`  景別  craft shotSize: ${shot.size.craft ?? "-"}${shot.size.family ? `（${FAMILY_LABEL[shot.size.family] ?? shot.size.family}，family ${shot.size.family}）` : "（沒寫）"}，讀自 ${where}`);
    out.push(`  運鏡  craft cameraMove: ${shot.move.craft} | slides cameraMove: ${shot.move.slides} | assemble motionMove（still 時）: ${shot.move.assemble.name}${shot.move.assemble.direction ? ` ${shot.move.assemble.direction}` : ""}（第 0 格驗 PSNR: ${yesNo(shot.move.assemble.psnr_checked)}）`);
    out.push(`  動作  isLookOnly: ${yesNo(shot.look_only)} | 關鍵影格 prompt ${shot.keyframe_prompt_chars}/${MAX_PROMPT_CHARS} 字${shot.cast_known ? "" : "（有角色外觀未知）"}`);
    for (const trap of shot.traps) {
      out.push(`  陷阱  ${trap.id}: ${trap.message}`);
      out.push(`        修法: ${trap.fix}`);
    }
  }
  out.push("");
  const { summary } = report;
  out.push(summary.traps
    ? `讀了 ${summary.shots} 個鏡頭，${summary.traps} 個陷阱：${Object.entries(summary.by_kind).map(([id, count]) => `${id} ${count}`).join("、")}`
    : `讀了 ${summary.shots} 個鏡頭，沒有陷阱：三個讀法讀到的就是寫的；畫面好不好仍要看小樣`);
  return out.join("\n");
}

function parseArgs(argv) {
  const args = { json: false, strict: false, file: null, input: null, only: null, route: "server" };
  for (let index = 0; index < argv.length; index++) {
    const arg = argv[index];
    if (arg === "--json") args.json = true;
    else if (arg === "--strict") args.strict = true;
    else if (arg === "--file") args.file = argv[++index] ?? null;
    else if (arg === "--route") {
      args.route = argv[++index] ?? "";
      if (!["server", "hailuo", "kling"].includes(args.route)) throw new Error("--route must be server, hailuo or kling");
    } else if (arg === "--shot") args.only = String(argv[++index] ?? "").split(",").map((id) => id.trim()).filter(Boolean);
    else if (arg.startsWith("--")) throw new Error(`unknown flag ${arg}`);
    else if (args.input === null) args.input = arg;
    else throw new Error(`unexpected argument ${arg}`);
  }
  return args;
}

const USAGE = "usage: shot_reading.mjs <video.json> [--shot a,b] [--route server|hailuo|kling] [--json] [--strict] | --file <one-shot.json> [--json] [--strict]";

function main(argv) {
  let args;
  try {
    args = parseArgs(argv);
  } catch (error) {
    console.error(`${error.message}\n${USAGE}`);
    return 2;
  }
  if (!args.input && !args.file) {
    console.error(USAGE);
    return 2;
  }
  let report;
  try {
    if (args.file) {
      const shot = JSON.parse(readFileSync(args.file, "utf8"));
      if (!shot || typeof shot !== "object" || Array.isArray(shot)) throw new Error("a one-shot file is an object { camera, prompt, motion, characters?, visual?, source? }");
      const { doc, series } = shotFileDocument(shot);
      report = readDocument(doc, { file: args.file, series, single: true });
    } else {
      const doc = JSON.parse(readFileSync(args.input, "utf8"));
      const seriesFile = path.join(path.dirname(path.resolve(args.input)), "series.json");
      const series = existsSync(seriesFile) ? JSON.parse(readFileSync(seriesFile, "utf8")) : null;
      report = readDocument(doc, { file: args.input, series, only: args.only, route: args.route });
      if (args.only) {
        const found = new Set(report.shots.map((shot) => shot.id));
        const missing = args.only.filter((id) => !found.has(id));
        if (missing.length) console.error(`${args.input}: 找不到鏡頭 ${missing.join(", ")}`);
        if (!report.shots.length) return 2;
      }
    }
  } catch (error) {
    console.error(`${args.file ?? args.input}: ${error.message}`);
    return 2;
  }
  console.log(args.json ? JSON.stringify(report, null, 2) : renderReading(report));
  return args.strict && report.summary.traps > 0 ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exitCode = main(process.argv.slice(2));
