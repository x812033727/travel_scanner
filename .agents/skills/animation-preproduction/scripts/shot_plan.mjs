#!/usr/bin/env node
// 開拍前的分鏡表與每鏡製作規格表：一集在付任何點數之前，每一鏡是什麼（場、鏡位代號、景別、運鏡、角色、
// 台詞秒數）、怎麼做（clip／still／cut、走哪條路線、買幾秒、首格與末格在哪）、有多難（AI 風險級與原因、
// 預期 take）、要花多少（一次、期望、上限），以及要貼進 Hailuo／Kling 網頁的定稿正文。最後給批次順序
// （三鏡小樣、依場、母鏡頭先、高風險先）與槓桿。站主一次確認的「開拍鎖定包」就從這份表來。
//
//   node .agents/skills/animation-preproduction/scripts/shot_plan.mjs <video.json> | --slug <SLUG>
//     [--route server|hailuo|kling] [--plan hailuo:pro|kling:pro|...] [--model <server clip model>]
//     [--resolution 1080p|720p|768p|2k] [--timeline <timeline.json>] [--workdir <dir>] [--root <repo>]
//     [--handle 0.5] [--clip-takes 2] [--production] [--markdown | --csv | --json] [--strict]
//
// --slug 讀 docs/videos/<slug>/video.json 與旁邊的 series.json，工作目錄照 tools/video 的規則（VIDEO_WORKDIR，
// 或 --workdir 指的放所有影片的目錄）：有錄好的 timeline.json 就用實測秒數、有 keyframes/manifest.json 就
// 填首尾格檔名與 SHA-256。給檔案路徑時，--workdir 是這一支影片自己的工作目錄。
// 離線：不碰伺服器、不花錢、不需要 ffmpeg。結束碼：0；--strict 且有會白花錢或做不進產線的問題是 1；
// 讀不到檔或參數錯是 2。規則與每個數字的來源在 .agents/skills/animation-preproduction/SKILL.md 與
// references/（shot-risk.md 的表與 RISK_RULES 逐列一致，tools/animation-preproduction.test.mjs 盯著）。
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { cameraMove as craftMove, normalize, shotSize } from "../../../../tools/video/core/craft.mjs";
import { CAMERA_MOVES, isSourced, lookHash, resolveLook, shotCast, shotProblems } from "../../../../tools/video/core/drama.mjs";
import { productionShotProblems } from "../../../../tools/video/core/lint.mjs";
import { validateVideo } from "../../../../tools/video/core/schema.mjs";
import { readJson, resolveWorkdir, ROOT } from "../../../../tools/video/core/paths.mjs";
import { estimateTimeline, FPS, speechHash, visualHash } from "../../../../tools/video/core/timeline.mjs";
import { loadProject } from "../../../../tools/video/core/state.mjs";
import { clipPrompt } from "../../../../tools/video/media/clips.mjs";
import { DEFAULT_CLIP_MODEL, estimateEpisode, KLING_CLIP_SECONDS, MAX_CLIP_TAKES, MAX_KEYFRAME_TAKES, PLANS, PRICES, secondsBought } from "../../animation-production/scripts/episode_estimate.mjs";

export const ROUTES = ["server", "hailuo", "kling"];
// 編輯判斷：網頁路線每鏡多買的尾巴把手。第 0 格必須是這一鏡的關鍵影格（assemble 對它算 PSNR ≥ 22），
// 頭不能留把手；模型的動作常拖到最後一兩格才收，尾巴留半秒讓剪點落在收勢之後。伺服器路線買幾秒由
// clipSeconds 決定，把手不適用。
export const DEFAULT_HANDLE_S = 0.5;
// 編輯判斷：各風險級預期要幾個 take 才有一支可用；C 等於 take 上限（照計畫買，大概會用完）。依據是 2026-10-03
// 試拍：S03 的兩個 take 都在手與筆上出錯、用完上限、0 支可用；S01 第一個真的生成的 take 也是同一類錯
// （model-misreads.md 第一節）。期望值不會超過 take 上限（--clip-takes）。
export const EXPECTED_TAKES = { A: 1.2, B: 1.5, C: 2 };
const GRADE_ORDER = { A: 0, B: 1, C: 2 };
// 網頁 H3／VIDEO 3.0 的秒數範圍（hailuoai.video 設定面板 2026-10-04 實測 4–15；Kling 官方 user guide 3–15）。
export const HAILUO_CLIP_SECONDS = [4, 15];

// 子句：動詞跟它的對象要在同一個子句裡（逗號、分號、句點、then、while、as 斷開）。
const clauses = (text) => String(text ?? "").toLowerCase().split(/[,;:.]|\b(?:then|while|as)\b/).map((part) => part.trim()).filter(Boolean);
const words = (list) => new RegExp(`\\b(?:${list})\\b`);
// 拿小東西做事的動詞（寫完整的字形，不用開放字尾：stable、drawer、pressure 才不會被讀成動作）。
const HANDLE_VERB = words("lifts?|lifting|picks? up|picking up|pours?|pouring|writes?|writing|signs?|signing|ties?|tying|unties?|untying|threads?|threading|inserts?|inserting|unfolds?|unfolding|folds?|folding|hands? over|handing over|passes|passing|gives?|giving|offers?|offering|takes?|taking|twists?|twisting|taps?|tapping|counts?|counting|flips?|flipping|unscrews?|tears?|tearing|stamps?|stamping|seals?|sealing|opens?|opening|pockets?|pocketing|lights?|lighting");
const SMALL_PROP_WORDS = "pens?|brush(?:es)?|needles?|keys?|coins?|rings?|chopsticks?|teacups?|cups?|bowls?|spoons?|papers?|notes?|letters?|envelopes?|cards?|buttons?|lighters?|matches|phones?|teapots?|kettles?|bottles?|cigarettes?|scrolls?|tokens?|pages?|books?|tickets?|contracts?|documents?|tea|wine|ink|seal";
const SMALL_PROP = words(SMALL_PROP_WORDS);
// 武器在手上做的動作。
const WEAPON_VERB = words("draws?|drawing|sheathes?|sheathing|unsheathes?|twirls?|twirling|spins?|spinning|tosses|tossing|throws?|throwing|catches|catching|lifts?|lifting|raises?|raising|flips?|flipping");
const WEAPON_WORDS = "swords?|blades?|sabres?|sabers?|staffs?|staves|spears?|daggers?|knives|knife|fans?|bows?|arrows?|whips?|axes?|hilts?";
const WEAPON = words(WEAPON_WORDS);
// 兩個人之間的接觸：強動詞要有對象（人、別人的東西、武器或身體部位）；抱、推、拉、扛這類只算直接接人。
const CONTACT_VERB = words("hugs?|hugging|embraces?|embracing|kiss(?:es)?|kissing|slaps?|slapping|punch(?:es)?|punching|hits?|hitting|strikes?|striking|grabs?|grabbing|seizes?|seizing|shoves?|shoving|stabs?|stabbing|thrusts?|thrusting|slash(?:es)?|slashing|cuts?|cutting|pierces?|piercing|kicks?|kicking|blocks?|blocking|parr(?:y|ies|ying)|clash(?:es)?|clashing|tackles?|tackling|strangles?|strangling|chokes?|choking|wrestles?|wrestling|collides?|colliding|deflects?|deflecting|meets?|meeting");
const CONTACT_TARGET = words("him|her|them|each other|one another|swords?|blades?|sabres?|sabers?|staffs?|spears?|shields?|daggers?|fists?|arms?|wrists?|hands?|chests?|shoulders?|faces?|necks?|throats?|backs?|guards?|shafts?|weapons?");
const DIRECT_CONTACT = /\b(?:holds?|holding|pushes|pushing|pulls?|pulling|carr(?:y|ies|ying)|lifts?|lifting|catch(?:es)?|catching|throws?|throwing|drags?|dragging)\s+(?:him|her|them|each other|one another)\b/;
const PERSON_NOUN = "man|woman|men|women|guard|guards|soldier|soldiers|servant|maid|stranger|figure|girl|boy|child|old man|old woman|messenger|monk|elder|officer|warrior";
const ENTERING = "enters?|entering|walks? in|walks? into (?:the )?(?:frame|room|shot)|steps? into (?:the )?(?:frame|room|shot)|comes? through the door|appears? (?:in|at) the door(?:way)?";
const escapeRe = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/**
 * AI 片段與關鍵影格的風險：每條 { id, grade, applies, test(data, ctx), why, redesign }。
 * applies "clip" 只看要買素材的鏡頭，主要讀 `motion`（這一鏡發生什麼；`prompt` 寫的是首格裡有什麼，畫面上的
 * 髮繩、錶、劍不等於有人在動它）；"image" 連 still 的關鍵影格也看，讀 `prompt`。
 * references/shot-risk.md 的表與這裡逐列一致（id、級、適用），tools/animation-preproduction.test.mjs 盯著。
 */
export const RISK_RULES = [
  {
    id: "hands.small-prop",
    grade: "C",
    applies: "clip",
    // 同一個子句裡：拿小東西做事的動詞，後面接那個東西。
    test: (data) => clauses(data.motion).some((part) => { const verb = HANDLE_VERB.exec(part); return Boolean(verb) && SMALL_PROP.test(part.slice(verb.index)); }),
    why: "手指拿小道具：多一隻手、道具換手、多一支筆或一只錶（2026-10-03 試拍：生成出來的 4 個 take 有 3 個在手與道具上出錯，S03 兩次上限用完、0 支可用）",
    redesign: "拆成兩鏡：手與道具的插鏡只做一個位移（抬起 20 厘米就停），反應放到下一鏡；或把接觸前一刻做成 still 加推近；寫清楚哪隻手、幾件道具、腕上有什麼",
  },
  {
    id: "contact.two-person",
    grade: "C",
    applies: "clip",
    // 畫面裡至少兩個人，同一個子句有接觸的動詞，後面接人、某人的東西、武器或身體部位；或直接抱、推、拉、扛人。
    test: (data, ctx) => ctx.characters >= 2 && clauses(data.motion).some((part) => {
      if (DIRECT_CONTACT.test(part)) return true;
      const verb = CONTACT_VERB.exec(part);
      if (!verb) return false;
      const after = part.slice(verb.index + verb[0].length);
      return CONTACT_TARGET.test(after) || (ctx.names ?? []).some((name) => new RegExp(`\\b${escapeRe(name)}(?:'s)?\\b`).test(after));
    }),
    why: "兩個人在同一支素材裡接觸：肢體穿插、手臂融合、接觸點漂移，一支裡兩個身份都要守住",
    redesign: "切在接觸前後：A 出手（只有 A）→ 接觸點的插鏡或閃光 → B 受力的反應鏡；兩人同框只留接觸前的對峙或接觸後的結果",
  },
  {
    id: "eat-drink",
    grade: "C",
    applies: "clip",
    test: (data) => words("eats?|eating|drinks?|drinking|sips?|sipping|bites? into|biting into|chews?|chewing|swallows?|swallowing").test(String(data.motion ?? "").toLowerCase()),
    why: "吃喝要嘴、手、器皿與液體同時對：模型常讓杯子穿過臉、液體不減、嘴不動",
    redesign: "拍放下杯子之後的反應，或杯子在嘴邊停住的 still；真的要喝就做插鏡只拍杯緣與手",
  },
  {
    id: "transform",
    grade: "C",
    applies: "clip",
    test: (data) => words("transforms?|transforming|morphs?|morphing|turns? into|turning into|shape-?shifts?|shape-?shifting|dissolves? into|grows? into").test(String(data.motion ?? "").toLowerCase()),
    why: "變身與形變正是 judge 扣分的 morphing；首格以外的形體模型自己編，身份守不住",
    redesign: "用首尾格：首格是變之前、末格是變之後（end_frame），或在閃光／特效遮罩處切成兩鏡",
  },
  {
    id: "text.readable",
    grade: "C",
    applies: "image",
    test: (data) => /\b(?:signboard|sign reading|lettering|handwriting|written on|writing on|text on|labels? (?:on|reading)|calligraphy|newspaper|headline|plaque|banner reading|words on|title card)\b|\breads ["“']/.test(String(data.prompt ?? "").toLowerCase()),
    why: "要讀得出的字：圖與片段模型都會寫錯或亂碼，judge 的 no_text 也會扣",
    redesign: "畫面上的紙寫成 blank 或背對鏡頭；要讀的字在剪接時另外合成（字卡、CC），不叫模型寫",
  },
  {
    id: "speech.visible-mouth",
    grade: "B",
    applies: "clip",
    test: (data, ctx) => ctx.face && ctx.speakerVisible,
    why: "說話的人在臉的景別裡、嘴看得見：產線沒有對嘴（docs/videos/DRAMA.md），模型的嘴型跟配音對不上",
    redesign: "台詞放在聽者的反應鏡、從說話者背後拍的過肩或插鏡上；說話者的臉鏡留給台詞前後那一拍，嘴閉著",
  },
  {
    id: "reaction.micro",
    grade: "B",
    applies: "clip",
    test: (data) => words("trembles?|trembling|twitch(?:es)?|twitching|clench(?:es)?|clenching|tightens?|tightening|quivers?|quivering|shivers?|shivering|flinch(?:es)?|flinching").test(String(data.motion ?? "").toLowerCase()),
    why: "微小反應會被放大：試拍把「手指收緊」「筆微顫」做成抬筆、多一隻手（model-misreads.md 第一節）",
    redesign: "改成 still 加 push in，或寫幅度與結束狀態（the pen tip moves less than a finger's width and returns; one hand, one pen）",
  },
  {
    id: "hands.weapon",
    grade: "B",
    applies: "clip",
    test: (data) => clauses(data.motion).some((part) => { const verb = WEAPON_VERB.exec(part); return Boolean(verb) && WEAPON.test(part.slice(verb.index)); }),
    why: "手上的武器在動（出鞘、抬起、轉、拋接）：握法、手指數與武器的長短最容易在中途變",
    redesign: "寫明哪隻手、握在哪裡、幅度與停在哪；出鞘這類細節拍成插鏡只做一個位移，或用 still 加推近交代蓄勢",
  },
  {
    id: "action.fast",
    grade: "B",
    applies: "clip",
    test: (data) => words("runs?|running|sprints?|sprinting|leaps?|leaping|jumps?|jumping|spins? around|whirls?|whirling|dodges?|dodging|fights?|fighting|chases?|chasing|tumbles?|tumbling|kicks?|kicking|somersaults?|dash(?:es)?|dashing|lunges?|lunging|charges?|charging|vaults?|vaulting|rolls? (?:aside|away|over)").test(String(data.motion ?? "").toLowerCase()),
    why: "快速大動作：四肢糊、穿模、落地位置與下一鏡接不上",
    redesign: "只拍起勢與落點，中間用特效、閃光或速度線一拍帶過；一支一個方向",
  },
  {
    id: "entrance",
    grade: "B",
    applies: "clip",
    // 只算人走進來：主詞是角色名字、代名詞或「人」的名詞；一道光、一支槍頭「進入畫面」不算，離開畫面也不算。
    test: (data, ctx) => {
      const subject = [...(ctx.names ?? []).map(escapeRe), "he", "she", "they", `(?:a|an|the|another|one) (?:\\w+ )?(?:${PERSON_NOUN})`].join("|");
      return new RegExp(`\\b(?:${subject})\\s+(?:\\w+\\s+){0,2}?(?:${ENTERING})\\b`).test(String(data.motion ?? "").toLowerCase());
    },
    why: "首格裡沒有的人進畫面：模型沒有參考，臉和衣服是它編的",
    redesign: "進來的人先站進首格（門口的剪影或背影），或拍「門被推開」再接他的中近景",
  },
  {
    id: "physics.fluid",
    grade: "B",
    applies: "clip",
    // 液體、玻璃、鏡面；火、煙、雷、能量這類特效不算（參考片拿它們遮動作，見 shot-risk.md）。
    test: (data) => words("splash(?:es)?|splashing|pours?|pouring|spills?|spilling|shatters?|shattering|mirrors?|reflections?|ripples?|rippling|waterfall").test(String(data.motion ?? "").toLowerCase()),
    why: "液體、碎玻璃、鏡面：量與方向常不對，杯裡的水不減、鏡中影像和本人對不上",
    redesign: "結果當畫面：倒完的杯、碎了的鏡用 still；鏡面拍成看不到倒影的角度",
  },
  {
    id: "crowd",
    grade: "B",
    applies: "image",
    test: (data) => words("crowds?|audience|guests|army|armies|soldiers|villagers|onlookers|spectators|many people|dozens of people").test(String(data.prompt ?? "").toLowerCase()),
    why: "一群人：臉糊、人數與站位每張都不同，下一鏡接不上",
    redesign: "群眾留在虛焦背景或剪影；主角前景佔畫面",
  },
  {
    id: "cast.three",
    grade: "B",
    applies: "image",
    test: (data, ctx) => ctx.characters >= 3,
    why: "三個角色同框：每人一張參考圖、一題 identity，任何一張臉走樣整張重做",
    redesign: "拆成兩人鏡＋單人反應；三人同框只給重新交代空間的全景",
  },
  {
    id: "camera.complex",
    grade: "B",
    applies: "clip",
    test: (data, ctx) => words("orbits?|orbiting|arcs? around|crane|cranes|craning|whip pan|whip|handheld|tracking|follows?|following|trucks?|trucking").test(ctx.camera) || ctx.moves > 1,
    why: "環繞、跟拍、搖臂或一鏡兩個運鏡：主體與背景的透視要一起算，最容易變形",
    redesign: "一鏡一個運鏡，用八組字裡的推、拉、搖、俯仰或鎖定；需要環繞就拆鏡",
  },
  {
    id: "long.take",
    grade: "B",
    applies: "clip",
    test: (data, ctx) => ctx.buySeconds > 8,
    why: "超過 8 秒的一支：越後面越漂（臉、衣服、道具位置），而成片通常只用 2–5 秒",
    redesign: "拆成兩鏡，或確定後段真的會被切去用（母鏡頭）再買長",
  },
];

/** 一鏡的風險：{ grade, reasons: [{ id, grade, why, redesign }], expected_takes }。visual 是 clip、still 或 cut。 */
export function shotRisk(data, visual, ctx, expected = EXPECTED_TAKES) {
  if (visual === "cut") return { grade: "A", reasons: [], expected_takes: 0 };
  const reasons = [];
  for (const rule of RISK_RULES) {
    if (rule.applies === "clip" && visual !== "clip") continue;
    if (rule.test(data ?? {}, ctx)) reasons.push({ id: rule.id, grade: rule.grade, why: rule.why, redesign: rule.redesign });
  }
  const grade = reasons.reduce((worst, reason) => (GRADE_ORDER[reason.grade] > GRADE_ORDER[worst] ? reason.grade : worst), "A");
  const takes = visual === "clip" ? Math.min(expected[grade], ctx.clipTakes ?? Infinity) : 0;
  return { grade, reasons, expected_takes: takes };
}

/** 一鏡是 clip、still 還是切素材（cut）：有 source 是切、visual "still" 是 still，其餘要買素材。 */
export const visualKindOf = (scene) => (isSourced(scene) ? "cut" : scene?.data?.visual === "still" ? "still" : "clip");

// ---------- 連戲鎖 ----------
// 「連戲鎖」（continuity locks）是 drama-skills（MIT）與 shuohao-skills（Apache-2.0）兩個中文漫劇技能包在分鏡表裡要人填的
// 欄位：依賴鏡頭、道具鎖、服裝鎖、時間鎖；這裡只借名字與想法，沒有看它們的碼。video.json 的鏡頭欄位是封閉集合
// （drama.mjs SHOT_KEYS），所以鎖的字從 `prompt`（首格裡有什麼）抓出來、由 plan_lock.mjs 寫進 plan/lock.json，
// drama_preflight.mjs 再對照現在的 prompt。三類詞表：道具（武器、小道具、場景道具）、服裝、時刻。道具與服裝要同一場
// 至少兩鏡寫到同一個字才鎖（一鏡獨有的插鏡道具不是連戲線）；時刻每寫一次就鎖（一句 at dusk 定了整場的光）。鎖的是
// prompt 裡原樣的字（小寫）：名詞本身，加上緊接在前的一個形容詞連名詞（jade hair cord 改成 red hair cord 才抓得到），
// 所以每一鏡的錨點要寫一樣的字。
const SCENE_PROP_WORDS = "lanterns?|torch(?:es)?|candles?|umbrellas?|baskets?|bags?|bundles?|satchels?|pouch(?:es)?|flags?|banners?|mirrors?|maps?|pebbles?|boats?|horses?|carts?|canes?|pipes?|flutes?|drums?|bells?|ropes?|chains?|nets?";
const COSTUME_WORDS = "hair cords?|hair ribbons?|hair ?pins?|hair ties?|shoulder clasps?|sleeve cuffs?|robes?|cloaks?|hoods?|capes?|cowls?|armou?r|breastplates?|sash(?:es)?|belts?|cuffs?|sleeves?|collars?|headbands?|hats?|veils?|gloves?|boots?|scar(?:f|ves)|masks?|crowns?|helmets?|brooch(?:es)?|clasps?|pendants?|earrings?|bracelets?|necklaces?|suits?|dress(?:es)?|coats?|jackets?|uniforms?|aprons?|tunics?|gowns?|shawls?|hanfu|kimonos?|qipaos?|skirts?|trousers|shirts?|vests?|cords?";
const TIME_WORDS = "early morning|late afternoon|golden hour|blue hour|dawn|daybreak|sunrise|morning|noon|midday|afternoon|dusk|sunset|twilight|nightfall|evening|midnight|night";
export const CONTINUITY_TERMS = { prop: `${WEAPON_WORDS}|${SMALL_PROP_WORDS}|${SCENE_PROP_WORDS}`, costume: COSTUME_WORDS, time_of_day: TIME_WORDS };
export const CONTINUITY_CATEGORIES = Object.keys(CONTINUITY_TERMS);
export const CONTINUITY_LABELS = { prop: "道具", costume: "服裝", time_of_day: "時刻" };
// 不算形容詞的前一個字：冠詞、數量、代名詞、介系詞、畫面位置；所有格（shen's）由正則擋掉。
const NOT_A_DESCRIPTOR = new Set(["a", "an", "the", "one", "two", "three", "four", "five", "her", "his", "their", "its", "my", "your", "our", "same", "single", "only", "no", "with", "of", "in", "on", "at", "and", "or", "to", "from", "this", "that", "these", "those", "each", "every", "both", "another", "other", "any", "some", "still", "visible", "intact", "own", "first", "second", "left", "right", "upper", "lower", "front", "back"]);

/** prompt 裡的連戲字：{ prop, costume, time_of_day }，每類是 prompt 裡原樣的小寫字（名詞，和形容詞＋名詞）。 */
export function continuityTerms(prompt) {
  const text = String(prompt ?? "").toLowerCase();
  const found = {};
  for (const category of CONTINUITY_CATEGORIES) {
    const terms = new Set();
    for (const match of text.matchAll(new RegExp(`(?<![\\w-])(?:${CONTINUITY_TERMS[category]})(?![\\w-])`, "g"))) {
      terms.add(match[0]);
      if (category === "time_of_day") continue;
      const before = /(?:^|[^\w'-])([a-z][a-z-]*)\s+$/.exec(text.slice(0, match.index))?.[1];
      if (before && !NOT_A_DESCRIPTOR.has(before)) terms.add(`${before} ${match[0]}`);
    }
    found[category] = [...terms];
  }
  return found;
}

/**
 * 每鏡的連戲鎖：Map id → { depends_on, locks: { prop, costume, time_of_day } }。locks 是這一鏡 prompt 裡被鎖的字；
 * depends_on 是同一場更早、跟它共用至少一個鎖定字的鏡頭，加上 source.shot（切自它的素材）與 start_frame.shot
 * （接它的末格）。shots 是 planEpisode 的列（index、id、chapter、scene）。
 */
export function continuityLocks(shots) {
  const terms = new Map(shots.map((shot) => [shot.id, continuityTerms(shot.scene?.data?.prompt)]));
  const out = new Map();
  for (const shot of shots) {
    const siblings = shots.filter((each) => each.chapter === shot.chapter && each.id !== shot.id);
    const own = terms.get(shot.id);
    const locks = {};
    for (const category of CONTINUITY_CATEGORIES) locks[category] = own[category].filter((term) => category === "time_of_day" || siblings.some((each) => terms.get(each.id)[category].includes(term)));
    const shares = (each) => CONTINUITY_CATEGORIES.some((category) => terms.get(each.id)[category].some((term) => locks[category].includes(term)));
    const data = shot.scene?.data ?? {};
    const dependsOn = new Set(siblings.filter((each) => each.index < shot.index && shares(each)).map((each) => each.id));
    if (data.source?.shot) dependsOn.add(data.source.shot);
    if (data.start_frame?.shot) dependsOn.add(data.start_frame.shot);
    dependsOn.delete(shot.id);
    out.set(shot.id, { depends_on: [...dependsOn], locks });
  }
  return out;
}

/**
 * Hailuo 網頁上能選的模型（hailuoai.video 訂閱頁的方案表、2026-10-04 讀；H3 的秒數面板 2026-10-04 實測）。
 * H3：4–15 秒整數、768P 7 點／秒、2K 12 點／秒（2K 實測、768P 由頁面「每月秒數」與 UI 的「Video: 12 Credits/s」推得），
 * 有首尾格，輸出 2K 2560×1440、768P 1344×768，24 fps。Hailuo 2.3：只有 6 或 10 秒，一支計價（768p 6 秒 25 點、
 * 10 秒 50 點、1080p 6 秒 80 點，訂閱頁 FAQ），沒有首尾格（API 的 fl2v 只有 Hailuo-02），1080p 是原生 1920×1080；
 * Max 方案點數用完之後 2.3 在 relax 佇列無限生成（tooltip；H3 不在內，排多久沒量）。
 */
export const HAILUO_MODELS = {
  h3: { label: "Hailuo H3", seconds: [4, 15], per_second: { "2k": 12, "768p": 7 }, default_resolution: "2k", end_frame: true, output: { "2k": "2560×1440", "768p": "1344×768" } },
  "2.3": { label: "Hailuo 2.3", per_clip: { "768p": { 6: 25, 10: 50 }, "1080p": { 6: 80 } }, default_resolution: "1080p", end_frame: false, output: { "1080p": "1920×1080", "768p": "未量" }, unlimited_on_max: true },
};

/**
 * camera 行在網頁上怎麼寫。group 是 tools/video/core/drama.mjs cameraMove 的八組，加上跟拍（沒寫任何運鏡字是 null）。
 * - Hailuo H3：官方 H3 提示指南（huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md，
 *   2026-10-04 讀）要「運鏡種類＋幅度＋速度」寫成句子（The camera pushes in with small amplitude at slow speed），
 *   不堆標籤；方括號指令官方只寫給 2.3／02／Director。
 * - Hailuo 2.3：方括號指令（platform.minimax.io 的 i2v 文件與 hailuoai.video 的運鏡小抄，2026-10-04 讀），
 *   [Static shot] 再補一句 the camera stays completely still。
 * - Kling 3.0：自然語言（官方 3.0 user guide 的 dolly in、pan left 這類字）。
 * pan 的方向照攝影機：我們的 `pan left` 是攝影機往左搖，Hailuo 的 Pan left 也是。
 */
const H3_SENTENCE = { locked: "The camera is a static shot and stays completely still", "push in": "The camera pushes in", "pull out": "The camera pulls out", "pan left": "The camera pans left", "pan right": "The camera pans right", "tilt up": "The camera tilts up", "tilt down": "The camera tilts down", track: "The camera is a tracking shot that follows the subject", drift: "The camera trucks right with small amplitude at slow speed" };
const HAILUO_BRACKET = { locked: "[Static shot]", "push in": "[Push in]", "pull out": "[Pull out]", "pan left": "[Pan left]", "pan right": "[Pan right]", "tilt up": "[Tilt up]", "tilt down": "[Tilt down]", track: "[Tracking shot]" };
const KLING_PHRASE = { locked: "locked-off camera, no camera movement", "push in": "the camera pushes in", "pull out": "the camera pulls back", "pan left": "the camera pans left", "pan right": "the camera pans right", "tilt up": "the camera tilts up", "tilt down": "the camera tilts down", track: "the camera tracks alongside the subject", drift: "the camera drifts very slightly" };
// 運鏡字但不在八組裡（沒方向的 pan／tilt、crane、單獨的 zoom、orbit、truck、handheld、whip…）：網頁正文不替你猜。
const OFF_TABLE_MOVE = /\b(?:pans?|panning|tilts?|tilting|cranes?|craning|pedestal|zooms?|zooming|orbits?|orbiting|arcs? around|trucks?|trucking|handheld|steadicam|whip|dolly out)\b/;
export function webMove(camera) {
  const text = String(camera ?? "").toLowerCase();
  const tracking = /\btrack(?:s|ing)?\b|\bfollow(?:s|ing)?\b/.test(text);
  // 直接讀 drama.mjs 的八組正則，不用 cameraMove 的預設值（它把讀不出來的都當 drift）。
  let group = tracking ? "track" : CAMERA_MOVES.find(([, pattern]) => pattern.test(text))?.[0] ?? null;
  if (group === null) {
    const craft = craftMove({ camera: text });
    if (craft === "push") group = "push in";
    else if (craft === "pull") group = "pull out";
  }
  const unsupported = group === null ? OFF_TABLE_MOVE.exec(text)?.[0] ?? null : null;
  const slow = /\b(?:slow|slowly|gentle|gently|subtle|subtly)\b/.test(text);
  const moving = group !== null && group !== "locked" && group !== "drift";
  return {
    group,
    slow,
    unsupported,
    h3: group === null ? null : `${H3_SENTENCE[group]}${moving ? (slow ? " with small amplitude at slow speed" : " at a steady speed") : ""}`,
    hailuo: group === null ? null : HAILUO_BRACKET[group] ?? null,
    kling: group === null ? null : KLING_PHRASE[group] ?? null,
  };
}

// 官方 H3 圖生影片格式的第一行（同上的 H3 提示指南；首格當 Picture 1、在第 0 秒完整參照）。
export const H3_FIRST_LINE = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.";
// 守住首格與單鏡的一句（animation-camera/references/budaimiao-style.md 第四節的寫法）。「單鏡、不切、不加字」是給模型的
// 生成指令，Kling 官方範例也這樣寫（a single unbroken shot with no cuts）；「正面寫」的規矩管的是畫面內容的狀態。
export const WEB_KEEP = "Keep the supplied first frame's composition, character identities, costumes and props; one continuous shot with no cuts and no on-screen text.";
// 收尾的標點：已經以句號、問號、驚嘆號、刪節號或引號結束的不再補句點。
const clean = (text) => String(text ?? "").trim().replace(/[.。\s]+$/, "");
const sentence = (text) => (text ? (/[.!?。！？…"”'’)]$/.test(text) ? text : `${text}.`) : "");

/**
 * 要貼進網頁（或伺服器送出）的動態正文：{ route, model, text, negative, chars, sha256, notes }。
 * 網頁的 text 不帶 look.negative：H3 的 API 沒有負面欄（官方），網頁有沒有沒驗；否定句又常被畫成正向（試拍把
 * already closed 畫成開著的門）。negative 另外列，表單真的有負面欄才貼。sha256 是 text 的，鎖定檔與收據都記它。
 */
export function webPrompt(route, scene, look, cast, { hailuoModel = "h3" } = {}) {
  const data = scene.data ?? {};
  const notes = [];
  let text;
  let negative = null;
  if (route === "server") {
    text = clipPrompt(scene, look, cast);
  } else {
    const move = webMove(data.camera);
    const motion = sentence(String(data.motion ?? "").trim());
    const lookMotion = sentence(clean(look.motion));
    negative = clean(look.negative) || null;
    if (move.unsupported) notes.push(`camera 行的「${move.unsupported}」不在八組運鏡字裡：正文不寫運鏡；改成 push in、pull out、pan left／right、tilt up／down、locked 或 drift`);
    else if (move.group === null) notes.push("camera 行沒有運鏡字：正文不寫運鏡，模型自己決定（要鎖定就寫 locked）");
    if (route === "hailuo" && hailuoModel === "h3") {
      const body = [`[Shot 1] ${motion}`.trim()];
      if (move.h3) body.push(`${move.h3}.`);
      if (lookMotion) body.push(lookMotion);
      body.push(WEB_KEEP);
      text = `${H3_FIRST_LINE}\n\nintegrated_multimodal_description: ${body.join(" ")}\noverall_soundscape: N/A\nnon_diegetic_music: N/A`;
    } else if (route === "hailuo") {
      const parts = [`${move.hailuo ? `${move.hailuo} ` : ""}${motion}`.trim()];
      if (move.group === "locked") parts.push("The camera stays completely still.");
      else if (move.group === "drift") parts.push("A very subtle, slow camera drift.");
      else if (move.slow && move.hailuo) parts.push("The camera moves slowly.");
      if (lookMotion) parts.push(lookMotion);
      parts.push(WEB_KEEP);
      text = parts.join(" ");
      if (move.group === "drift") notes.push("Hailuo 2.3 沒有 drift 的方括號指令：正文用自然語言");
    } else {
      const camera = move.kling ? `Single continuous shot, ${move.slow && move.group !== "locked" ? move.kling.replace("the camera ", "the camera slowly ") : move.kling}.` : "Single continuous shot.";
      const parts = [camera];
      if (motion) parts.push(motion);
      if (lookMotion) parts.push(lookMotion);
      parts.push(WEB_KEEP);
      text = parts.join(" ");
    }
    if (cast.length >= 2) {
      const names = cast.flatMap((character) => [character.name, character.id]).filter((label) => typeof label === "string" && /^[A-Za-z][\w-]+$/.test(label));
      const named = names.filter((label) => new RegExp(`(?<![\\w-])${escapeRe(label)}(?![\\w-])`, "i").test(motion));
      if (named.length) notes.push(`同框兩人、正文用了名字（${[...new Set(named)].join("、")}）：影片模型不認得名字，看的是首格；寫成畫面位置或外觀（the woman on screen left）比較不會認錯人`);
    }
  }
  return { route, model: route === "hailuo" ? hailuoModel : null, text, negative, chars: text.length, sha256: createHash("sha256").update(text).digest("hex"), notes };
}

const round2 = (value) => Math.round(value * 100) / 100;
const round4 = (value) => Math.round(value * 10_000) / 10_000;
const sum = (items, pick) => items.reduce((total, item) => total + (pick(item) ?? 0), 0);
const setupKey = (data) => `${String(data?.camera ?? "").trim().toLowerCase()}|${String(data?.prompt ?? "").split(/[,.;]/)[0].trim().toLowerCase()}`;
const FACE = new Set(["ecu", "cu", "mcu", "ots"]);
const letter = (index) => (index < 26 ? String.fromCharCode(65 + index) : `Z${index - 25}`);

function routeOf(options) {
  const planId = options.plan ?? null;
  const plan = planId ? PLANS[planId] : null;
  if (planId && !plan) throw new Error(`unknown plan "${planId}": one of ${Object.keys(PLANS).join(", ")}`);
  const route = options.route ?? plan?.vendor ?? "server";
  if (!ROUTES.includes(route)) throw new Error(`--route must be one of ${ROUTES.join(", ")}`);
  if (plan && plan.vendor !== route) throw new Error(`--plan ${planId} is a ${plan.vendor} plan; --route is ${route}`);
  const defaultPlan = route === "hailuo" ? "hailuo:pro" : route === "kling" ? "kling:pro" : null;
  return { route, planId: planId ?? defaultPlan, plan: plan ?? (defaultPlan ? PLANS[defaultPlan] : null) };
}

/**
 * 整集的開拍計畫。options：route、plan、model、resolution、timeline（錄好的 timeline.json）、manifest
 * （keyframes/manifest.json）、series（series.json）、handle、clipTakes、production。
 * 回 { route, plan, model, resolution, basis, conditions, chapters, shots, totals, batches, levers, problems, notes }。
 */
export function planEpisode(doc, options = {}) {
  if (!Array.isArray(doc?.scenes)) throw new Error("not a video.json: no scenes[]");
  const { route, planId, plan } = routeOf(options);
  const profile = options.series?.production?.profile ?? null;
  const production = Boolean(options.production || profile);
  const model = options.model ?? profile?.video?.model ?? DEFAULT_CLIP_MODEL;
  if (!PRICES[model] || PRICES[model].kind !== "clip") throw new Error(`unknown clip model "${model}"`);
  const wanted = options.resolution ? String(options.resolution).toLowerCase() : null;
  const serverResolution = PRICES[model].resolutions?.includes(wanted) ? wanted : profile?.video?.resolution ?? PRICES[model].default_resolution ?? null;
  const hailuoModel = route === "hailuo" ? options.hailuoModel ?? "h3" : null;
  if (hailuoModel && !HAILUO_MODELS[hailuoModel]) throw new Error(`--hailuo-model must be one of ${Object.keys(HAILUO_MODELS).join(", ")}`);
  const hailuo = hailuoModel ? HAILUO_MODELS[hailuoModel] : null;
  const webTable = hailuo ? hailuo.per_second ?? hailuo.per_clip : plan?.credits_per_second ?? null;
  if (route !== "server" && wanted && webTable && !Object.hasOwn(webTable, wanted)) throw new Error(`--resolution ${wanted} is not sold by ${hailuo?.label ?? "Kling VIDEO 3.0"}: one of ${Object.keys(webTable).join(", ")}`);
  const webResolution = webTable ? (wanted && Object.hasOwn(webTable, wanted) ? wanted : hailuo?.default_resolution ?? plan.default_resolution) : null;
  const handle = route === "server" ? 0 : Number.isFinite(options.handle) ? options.handle : DEFAULT_HANDLE_S;
  const clipTakes = options.clipTakes ?? MAX_CLIP_TAKES;
  const expectedTakes = options.expectedTakes ?? EXPECTED_TAKES;
  const measured = Boolean(options.timeline);
  let timeline = options.timeline ?? null;
  if (!timeline) {
    try {
      timeline = estimateTimeline(doc);
    } catch {
      timeline = null;
    }
  }
  const look = resolveLook(doc.look);
  const { shots: rows } = normalize(doc, { timeline });
  const framesOf = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, scene.end_frame - scene.start_frame]));
  const sceneById = new Map(doc.scenes.map((scene) => [scene.id, scene]));
  const manifest = options.manifest ?? null;
  const manifestBound = Boolean(manifest) && manifest.look_hash === lookHash(doc) && manifest.visual_hash === visualHash(doc);

  // 場：chapter 開一場，之後的鏡頭都屬它，直到下一個 chapter。
  const chapterOf = new Map();
  let chapter = null;
  for (const scene of doc.scenes) {
    if (typeof scene.chapter === "string" && scene.chapter.trim()) chapter = scene.chapter.trim();
    chapterOf.set(scene.id, chapter ?? "（無章節）");
  }

  // 每秒的價（伺服器 US$、網頁點數）；Hailuo 2.3 是一支計價，rate 為 null，costOf 查表。
  const rate = route === "server" ? PRICES[model].usd_per_second : hailuo?.per_clip ? null : hailuo ? hailuo.per_second[webResolution] : plan.credits_per_second[webResolution];
  const costOf = (seconds) => (rate !== null ? seconds * rate : hailuo.per_clip[webResolution][seconds] ?? 0);
  const usdPerCredit = plan ? plan.fee_usd / plan.credits : null;
  const setupCodes = new Map();
  const castNames = (Array.isArray(doc.characters) ? doc.characters : []).flatMap((character) => [character?.id, character?.name]).filter((label) => typeof label === "string" && /^[A-Za-z][\w -]*$/.test(label)).map((label) => label.toLowerCase());
  const shots = rows.filter((row) => !row.card).map((row, index) => {
    const scene = sceneById.get(row.id);
    const data = row.data ?? {};
    const frames = framesOf.get(row.id) ?? Math.round(row.seconds * FPS);
    const visual = visualKindOf(scene);
    const chapterName = chapterOf.get(row.id);
    const codes = setupCodes.get(chapterName) ?? new Map();
    setupCodes.set(chapterName, codes);
    const key = setupKey(data);
    if (!codes.has(key)) codes.set(key, letter(codes.size));
    const cast = shotCast(doc, scene);
    const speakers = [...new Set(row.lines.map((line) => line.speaker))];
    const size = shotSize(data);
    return {
      index,
      id: row.id,
      chapter: chapterName,
      setup: codes.get(key),
      setup_key: key,
      camera: data.camera ?? "",
      size,
      move: { craft: craftMove(data), web: webMove(data.camera) },
      characters: cast.map((character) => character.id),
      speakers,
      lines: row.lines.map((line) => ({ speaker: line.speaker, text: line.text })),
      action_seconds: Number.isFinite(scene.action_seconds) ? scene.action_seconds : null,
      need_s: round2(frames / FPS),
      frames,
      visual,
      source: visual === "cut" ? { shot: data.source.shot, from_s: Number(data.source.from_s ?? 0) } : null,
      end_frame_planned: visual === "clip" && Boolean(data.end_frame?.prompt),
      scene,
      cast,
      // 只拍眼睛的大特寫看不到嘴。
      face: FACE.has(size) && !(size === "ecu" && /\beyes?\b/i.test(String(data.prompt ?? "").split(/[,.;]/)[0])),
    };
  });

  // 母鏡頭：被切的 clip 要涵蓋每一個切鏡的 from_s＋鏡長。
  const byId = new Map(shots.map((shot) => [shot.id, shot]));
  for (const shot of shots) {
    if (!shot.source) continue;
    const origin = byId.get(shot.source.shot);
    if (!origin || origin.visual !== "clip") continue;
    origin.cut_need_s = Math.max(origin.cut_need_s ?? 0, round2(shot.source.from_s + shot.need_s));
    (origin.cuts ??= []).push(shot.id);
  }

  const problems = [];
  const notes = [];
  for (const shot of shots) {
    const need = Math.max(shot.need_s, shot.cut_need_s ?? 0);
    if (shot.visual === "clip") {
      if (route === "server") {
        shot.buy_s = secondsBought(shot.frames, model, serverResolution);
      } else if (hailuo?.per_clip) {
        // Hailuo 2.3 只賣固定長度：挑最短的一個蓋得住需要＋把手的。
        const lengths = Object.keys(hailuo.per_clip[webResolution]).map(Number).sort((a, b) => a - b);
        shot.buy_s = lengths.find((each) => each >= need + handle - 1e-9) ?? lengths.find((each) => each >= need - 1e-9) ?? lengths.at(-1);
        if (need > lengths.at(-1) + 1e-9) problems.push({ level: "waste", shot: shot.id, what: `需要 ${need.toFixed(1)} s（含把手 ${handle} s），${hailuo.label} ${webResolution} 一支只有 ${lengths.join("／")} s`, fix: "拆成兩鏡，或改用 H3（4–15 秒）" });
        if (shot.end_frame_planned) problems.push({ level: "waste", shot: shot.id, what: `${hailuo.label} 沒有首尾格，計畫的 end_frame 用不上`, fix: "這一鏡改用 H3，或拿掉 end_frame" });
      } else {
        const [low, high] = route === "hailuo" ? hailuo.seconds : KLING_CLIP_SECONDS;
        shot.buy_s = Math.min(high, Math.max(low, Math.ceil(need + handle - 1e-9)));
        if (need > high + 1e-9) problems.push({ level: "waste", shot: shot.id, what: `需要 ${need.toFixed(1)} s，網頁一支最多 ${high} s`, fix: "拆成兩鏡，或少切幾次這個母鏡頭" });
        else if (need + handle > high + 1e-9) notes.push(`${shot.id}：需要 ${need.toFixed(1)} s，買到上限 ${high} s，尾巴把手不到 ${handle} s`);
      }
      if (shot.cut_need_s && shot.cut_need_s > shot.buy_s + 1e-9) problems.push({ level: "waste", shot: shot.id, what: `切鏡 ${shot.cuts.join("、")} 要用到這支的 ${shot.cut_need_s.toFixed(1)} s，但這條路線只買 ${shot.buy_s} s`, fix: route === "server" ? "伺服器路線的秒數由 clipSeconds 決定：from_s 提早，或改網頁路線買長一點的母鏡頭" : "from_s 提早，或縮短切鏡的台詞" });
    } else {
      shot.buy_s = 0;
    }
    if (shot.visual === "cut" && !byId.get(shot.source.shot)) problems.push({ level: "waste", shot: shot.id, what: `source.shot ${shot.source.shot} 不在這份檔案裡`, fix: "指向一個更早的 clip 鏡頭" });
    // 從說話者背後拍的過肩（「from behind <speaker>」「over <speaker>'s shoulder」）看不到他的嘴。
    const behind = (id) => {
      const character = shot.cast.find((each) => each.id === id);
      const labels = [id, character?.name].filter((label) => typeof label === "string" && label.length).map((label) => label.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
      const text = `${shot.camera} ${shot.scene.data?.prompt ?? ""}`.toLowerCase();
      return labels.some((label) => new RegExp(`\\bfrom behind ${label}\\b|\\bover ${label}'s (?:\\w+ )?shoulder\\b|\\bbehind ${label}'s (?:\\w+ )?(?:shoulder|back|head)\\b`).test(text));
    };
    const ctx = {
      characters: shot.characters.length,
      names: castNames,
      face: shot.face,
      speakerVisible: shot.speakers.some((speaker) => speaker !== "narrator" && shot.characters.includes(speaker) && !behind(speaker)) && shot.lines.length > 0,
      camera: String(shot.camera).toLowerCase(),
      moves: new Set((String(shot.camera).toLowerCase().match(/\b(?:push|pull|pan|tilt|zoom|dolly|crane|orbit|track)(?:s|es|ed|ing)?\b/g) ?? []).map((word) => word.replace(/(?:es|s|ed|ing)$/, ""))).size,
      buySeconds: shot.buy_s,
      clipTakes,
    };
    shot.risk = shotRisk(shot.scene.data ?? {}, shot.visual, ctx, expectedTakes);
    const unitCost = shot.visual === "clip" ? costOf(shot.buy_s) : 0;
    shot.cost = {
      unit: route === "server" ? "usd" : "credits",
      one: round2(unitCost),
      expected: round2(unitCost * shot.risk.expected_takes),
      cap: round2(unitCost * clipTakes),
    };
    if (usdPerCredit !== null) shot.cost.usd_fee = { one: round4(unitCost * usdPerCredit), expected: round4(unitCost * shot.risk.expected_takes * usdPerCredit), cap: round4(unitCost * clipTakes * usdPerCredit) };
    const entry = manifest?.shots?.[shot.id] ?? null;
    shot.first_frame = shot.visual === "cut"
      ? { kind: "source", note: `${shot.source.shot} 的素材第 ${shot.source.from_s} s（assemble 對那一格算 PSNR）` }
      : entry?.file
        ? { kind: manifestBound && !entry.needs_review ? "drawn" : manifestBound ? "needs_review" : "stale", file: entry.file, sha256: entry.sha256 ?? null }
        : { kind: "to-draw" };
    shot.end_frame = shot.end_frame_planned ? { planned: true, file: entry?.end_frame?.file ?? null, sha256: entry?.end_frame?.sha256 ?? null } : { planned: false };
    shot.prompt = shot.visual === "clip" ? webPrompt(route, shot.scene, look, shot.cast, { hailuoModel: hailuoModel ?? undefined }) : null;
    if (shot.visual === "clip" && shot.move.web.unsupported) problems.push({ level: "review", shot: shot.id, what: `camera 行的「${shot.move.web.unsupported}」不在八組運鏡字裡，定稿正文沒寫運鏡`, fix: "改成 push in、pull out、pan left／right、tilt up／down、locked 或 drift（animation-camera 的「寫 camera」）" });
  }

  // 承諾與連戲鎖，鎖定時寫進 plan/lock.json（plan_lock.mjs lockOf）。承諾是這一鏡答應做成什麼：類型、買幾秒、路線、fit——
  // 「交付承諾」（delivery promise）是 OpenMontage 的叫法（AGPL，只借想法）；鎖定後答應的 clip 變成 still、切或 fit freeze，
  // drama_preflight.mjs 以 exit 1 擋到站主的變更單為止。
  const continuity = continuityLocks(shots);
  for (const shot of shots) {
    shot.promise = { visual_kind: shot.visual, buy_s: shot.buy_s, route, fit: shot.scene.data?.fit ?? "auto" };
    shot.continuity = continuity.get(shot.id);
  }

  // lint 會擋的鏡頭問題：schema 的鏡頭欄位、鏡長與切素材上限、production profile 的規則。照 lint 的估法量（lint 本來就是）。
  try {
    for (const error of validateVideo(doc).filter((each) => /^scenes\[/.test(each.path ?? ""))) problems.push({ level: "refuse", shot: /\(([^)]+)\)/.exec(error.path)?.[1] ?? (doc.scenes[Number(/^scenes\[(\d+)\]/.exec(error.path)?.[1])]?.id ?? null), what: `lint：${error.path} ${error.message}`, fix: "lint 會擋：照訊息改劇本" });
    const linted = estimateTimeline(doc);
    for (const error of shotProblems(doc, linted).errors) problems.push({ level: "refuse", shot: /\(([^)]+)\)/.exec(error.path)?.[1] ?? null, what: `lint：${error.message}`, fix: "lint 會擋：照訊息改劇本" });
    const profiled = options.series?.production?.profile ? options.series : production ? { production: { profile: {} } } : null;
    for (const error of productionShotProblems(doc, profiled, timeline)) problems.push({ level: "refuse", shot: /\(([^)]+)\)/.exec(error.path)?.[1] ?? null, what: `production profile：${error.message}`, fix: "照訊息改劇本" });
  } catch (error) {
    notes.push(`lint 的鏡頭檢查沒跑完（${error.message}）：先跑 tools/video/cli.mjs lint`);
  }
  if (hailuo?.unlimited_on_max) notes.push(`${hailuo.label}：Max 方案的點數用完之後，它在 relax 佇列無限生成（訂閱頁 tooltip，2026-10-04 讀；H3 不在內，排多久沒量）；這裡的點數是用點數跑的價`);
  if (route !== "server" && production) problems.push({ level: "refuse", shot: null, what: "這集有 series.production.profile：clips import 一律以結束碼 3 拒收外部片段（tools/video/media/clips.mjs importClip），Hailuo／Kling 做的片段進不了這集", fix: "走伺服器路線，或等「有 profile 的作品走外部路線」那張票" });
  if (options.timelineStale) notes.push("工作目錄的 timeline.json 是改台詞之前錄的（speech_hash 對不上）：秒數改用 lint 的估法；重跑 tts 之後再出一次表");
  if (hailuoModel === "h3" && webResolution === "2k") notes.push("Hailuo H3 2K 輸出 2560×1440（實測 2026-10-04），assemble 等比縮成 1920×1080");
  if (hailuoModel === "h3" && webResolution === "768p") notes.push("Hailuo H3 768P 是 1344×768（官方自架指南的畫布），assemble 要放大成 1920×1080，畫質沒驗");
  if (route !== "server" && webResolution === "720p") notes.push("Kling 720p 要放大成 1920×1080（clips import 的下限剛好是 1280×720），畫質沒驗");

  // 批次：三鏡小樣（同一場、連續、風險最高），再依場：母鏡頭、C、B、A。
  const clipShots = shots.filter((shot) => shot.visual === "clip");
  const score = (shot) => (shot.visual === "clip" ? 1 + GRADE_ORDER[shot.risk.grade] * 2 : 0);
  let pilot = [];
  if (Array.isArray(options.pilot) && options.pilot.length) {
    pilot = options.pilot.map((id) => byId.get(id));
    const missing = options.pilot.filter((id, at) => !pilot[at]);
    if (missing.length) throw new Error(`--pilot names shots that are not in the file: ${missing.join(", ")}`);
  } else {
    let best = null;
    for (let i = 0; i + 2 < shots.length; i++) {
      const window = shots.slice(i, i + 3);
      if (new Set(window.map((shot) => shot.chapter)).size > 1) continue;
      const clips = window.filter((shot) => shot.visual === "clip");
      if (clips.length < 2) continue;
      // 代表性（youtube-video 的 animation-production.md：小樣要有聽得清的對話、一個有接觸或重量的動作）：買素材的鏡頭裡
      // 有台詞鏡、也有無聲動作拍的各加一分；同分時買得多的、C 多的先，再來是前面的。
      const total = sum(window, score) + (clips.some((shot) => shot.lines.length) ? 1 : 0) + (clips.some((shot) => shot.action_seconds !== null) ? 1 : 0);
      const key = [total, clips.length, clips.filter((shot) => shot.risk.grade === "C").length];
      const better = !best || (() => {
        for (let at = 0; at < key.length; at++) if (key[at] !== best.key[at]) return key[at] > best.key[at];
        return false;
      })();
      if (better) best = { key, window };
    }
    pilot = best?.window ?? clipShots.slice(0, 3);
  }
  const pilotIds = new Set(pilot.map((shot) => shot.id));
  for (const shot of pilot) if (shot.source && !pilotIds.has(shot.source.shot)) pilotIds.add(shot.source.shot);
  for (const shot of clipShots) if (shot.risk.grade === "C" && !pilotIds.has(shot.id)) problems.push({ level: "review", shot: shot.id, what: `C 級（${shot.risk.reasons.filter((reason) => reason.grade === "C").map((reason) => reason.id).join(", ")}）不在小樣裡`, fix: "照 shot-risk.md 重設計；劇情非要不可就用 --pilot 把它放進小樣先驗" });
  const batches = [];
  if (pilotIds.size) {
    const members = shots.filter((shot) => pilotIds.has(shot.id));
    batches.push({ name: "小樣", why: options.pilot?.length ? "鎖定包指定的小樣鏡頭：先驗身份、動作、剪接與匯入，站主看過才放量" : "同一場連續三鏡、風險最高的一段：先驗身份、動作、剪接與匯入，站主看過才放量", shots: members.map((shot) => shot.id), buys: members.filter((shot) => shot.visual === "clip").map((shot) => shot.id), cost_one: round2(sum(members, (shot) => shot.cost.one)) });
  }
  const chapters = [...new Set(shots.map((shot) => shot.chapter))];
  chapters.forEach((name, number) => {
    const members = shots.filter((shot) => shot.chapter === name && !pilotIds.has(shot.id));
    if (!members.length) return;
    const buys = members.filter((shot) => shot.visual === "clip").sort((a, b) => Number(Boolean(b.cuts?.length)) - Number(Boolean(a.cuts?.length)) || GRADE_ORDER[b.risk.grade] - GRADE_ORDER[a.risk.grade] || a.index - b.index);
    batches.push({
      name: `第 ${number + 1} 場：${name}`,
      why: number === 0 ? "母鏡頭先（切鏡等它）、高風險先（早失敗）；這一場做完先停下來看漂移與連戲，再開下一場" : "母鏡頭先、高風險先",
      shots: members.map((shot) => shot.id),
      buys: buys.map((shot) => shot.id),
      cost_one: round2(sum(buys, (shot) => shot.cost.one)),
      checkpoint: number === 0,
    });
  });

  const estimate = estimateEpisode(doc, { model, resolution: serverResolution, timeline: measured ? timeline : undefined, production, clipTakes });
  const judgePrice = PRICES.judge.usd_per_call;
  const serverSide = {
    // 網頁路線也要伺服器的設定圖、關鍵影格（含 judge）與音樂；片段的 judge 只有 clips import --judge 才問。
    usd_one: round4(estimate.stages.look.usd_one + estimate.stages.keyframes.usd_one + (estimate.stages.look.judge_one + estimate.stages.keyframes.judge_one) * judgePrice + estimate.stages.music.usd),
    usd_cap: round4(estimate.stages.look.usd_cap + estimate.stages.keyframes.usd_cap + (estimate.stages.look.judge_cap + estimate.stages.keyframes.judge_cap) * judgePrice + estimate.stages.music.usd),
  };
  const counts = { shots: shots.length, clips: clipShots.length, stills: shots.filter((shot) => shot.visual === "still").length, cuts: shots.filter((shot) => shot.visual === "cut").length, A: clipShots.filter((shot) => shot.risk.grade === "A").length, B: clipShots.filter((shot) => shot.risk.grade === "B").length, C: clipShots.filter((shot) => shot.risk.grade === "C").length };
  const needSeconds = sum(clipShots, (shot) => shot.need_s) + sum(shots.filter((shot) => shot.visual === "cut"), (shot) => shot.need_s);
  const boughtSeconds = sum(clipShots, (shot) => shot.buy_s);
  const totals = {
    seconds: round2(sum(shots, (shot) => shot.need_s)),
    clip_seconds: boughtSeconds,
    utilisation: boughtSeconds ? round4(needSeconds / boughtSeconds) : null,
    clip: { unit: route === "server" ? "usd" : "credits", one: round2(sum(clipShots, (shot) => shot.cost.one)), expected: round2(sum(clipShots, (shot) => shot.cost.expected)), cap: round2(sum(clipShots, (shot) => shot.cost.cap)) },
    server_side_usd: serverSide,
    setups: chapters.map((name) => ({ chapter: name, setups: setupCodes.get(name)?.size ?? 0, shots: shots.filter((shot) => shot.chapter === name).length })),
  };
  if (usdPerCredit !== null) {
    totals.clip.usd_fee = { one: round4(totals.clip.one * usdPerCredit), expected: round4(totals.clip.expected * usdPerCredit), cap: round4(totals.clip.cap * usdPerCredit) };
    totals.plan_share = { one: round4(totals.clip.one / plan.credits), expected: round4(totals.clip.expected / plan.credits), cap: round4(totals.clip.cap / plan.credits) };
    if (totals.clip.expected > plan.credits) problems.push({ level: "waste", shot: null, what: `片段期望 ${totals.clip.expected} credits，超過 ${plan.label} 一個月的 ${plan.credits}`, fix: "換方案、分兩個月做，或用槓桿（still、切鏡、拆掉 C 級鏡頭）" });
  }
  const drop = (shot) => {
    const { scene, cast, frames, face, ...rest } = shot;
    return rest;
  };
  return {
    route,
    plan: plan ? { id: planId, label: plan.label, credits: plan.credits, fee_usd: plan.fee_usd, resolution: webResolution, credits_per_second: rate, model: hailuo?.label ?? "Kling VIDEO 3.0", per_clip: hailuo?.per_clip?.[webResolution] ?? null } : null,
    model: route === "server" ? model : null,
    resolution: route === "server" ? serverResolution : webResolution,
    basis: measured ? "錄好的 timeline.json" : "lint 的估法（estimateTimeline）",
    handle_s: handle,
    clip_takes: clipTakes,
    expected_takes: expectedTakes,
    keyframe_takes: MAX_KEYFRAME_TAKES,
    conditions: { production, import_ok: route === "server" || !production, manifest: manifest ? (manifestBound ? "bound" : "stale") : "absent" },
    counts,
    shots: shots.map(drop),
    totals,
    batches,
    levers: estimate.levers,
    problems,
    notes,
  };
}

// ---------- 輸出 ----------
const KIND = { clip: "clip", still: "still", cut: "切" };
const FRAME = { drawn: "已畫", needs_review: "要看", stale: "過期", "to-draw": "待畫", source: "來源" };
const money = (plan, value) => (plan.route === "server" ? `US$${value.toFixed(2)}` : `${Math.round(value)} 點`);
const cell = (text) => String(text ?? "").replace(/\|/g, "／").replace(/\n/g, " ");

export function renderMarkdown(plan, file = "video.json") {
  const out = [];
  const price = plan.plan?.per_clip ? Object.entries(plan.plan.per_clip).map(([seconds, credits]) => `${seconds} 秒 ${credits} 點`).join("、") : `${plan.plan?.credits_per_second} 點／秒`;
  const routeName = plan.route === "server" ? `伺服器 ${plan.model} ${plan.resolution ?? ""}` : `${plan.plan.label}，${plan.plan.model} ${plan.resolution}（${price}）`;
  out.push(`# 分鏡表與製作規格：${file}`);
  out.push("");
  out.push(`- 路線：${routeName}；秒數依據：${plan.basis}；${plan.route === "server" ? "買幾秒照 clipSeconds" : `尾巴把手 ${plan.handle_s} s`}；clip take 上限 ${plan.clip_takes}`);
  out.push(`- ${plan.counts.shots} 鏡：clip ${plan.counts.clips}、still ${plan.counts.stills}、切 ${plan.counts.cuts}；clip 風險 A ${plan.counts.A}、B ${plan.counts.B}、C ${plan.counts.C}；約 ${plan.totals.seconds.toFixed(1)} s`);
  const clip = plan.totals.clip;
  const fee = clip.usd_fee ? `（月費攤 US$${clip.usd_fee.one.toFixed(2)}／${clip.usd_fee.expected.toFixed(2)}／${clip.usd_fee.cap.toFixed(2)}；占月額 ${(plan.totals.plan_share.one * 100).toFixed(0)}%／${(plan.totals.plan_share.expected * 100).toFixed(0)}%／${(plan.totals.plan_share.cap * 100).toFixed(0)}%）` : "";
  out.push(`- 片段：買 ${plan.totals.clip_seconds} s，利用率 ${plan.totals.utilisation === null ? "—" : `${Math.round(plan.totals.utilisation * 100)}%`}；一次 ${money(plan, clip.one)}、期望 ${money(plan, clip.expected)}、上限 ${money(plan, clip.cap)}${fee}`);
  out.push(`- 伺服器端（設定圖、關鍵影格與其 judge、音樂）：一次 US$${plan.totals.server_side_usd.usd_one.toFixed(2)}、上限 US$${plan.totals.server_side_usd.usd_cap.toFixed(2)}`);
  out.push(`- 鏡位：${plan.totals.setups.map((each) => `${each.chapter} ${each.setups} 個鏡位／${each.shots} 鏡`).join("；")}`);
  out.push(`- 關鍵影格 manifest：${{ bound: "綁著現在的劇本", stale: "過期（look 或 visual hash 變了）", absent: "還沒畫" }[plan.conditions.manifest]}${plan.conditions.import_ok ? "" : "；**外部片段進不了這集（production profile）**"}`);
  out.push("");
  out.push("## 分鏡表");
  out.push("");
  out.push("| 鏡 | 場／鏡位 | 景別、運鏡 | 角色 | 台詞 | 秒 | 類型 | 買 | 首格 | 末格 | 風險 | 一次／期望／上限 |");
  out.push("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |");
  for (const shot of plan.shots) {
    const lines = shot.lines.length ? shot.lines.map((line) => `${line.speaker}：${line.text}`).join(" ／ ") : shot.action_seconds ? `（動作 ${shot.action_seconds} s）` : "";
    const risk = shot.visual === "cut" ? "—" : `${shot.risk.grade}${shot.risk.reasons.length ? ` ${shot.risk.reasons.map((reason) => reason.id).join(", ")}` : ""}`;
    const cost = shot.visual === "clip" ? `${money(plan, shot.cost.one)}／${money(plan, shot.cost.expected)}／${money(plan, shot.cost.cap)}` : "—";
    const kind = shot.visual === "cut" ? `切自 ${shot.source.shot} @${shot.source.from_s}s` : KIND[shot.visual];
    out.push(`| ${shot.id} | ${cell(shot.chapter)}／${shot.setup} | ${cell(shot.camera)} | ${shot.characters.join(", ") || "—"} | ${cell(lines)} | ${shot.need_s.toFixed(1)} | ${kind}${shot.cuts?.length ? `（母鏡頭：${shot.cuts.join(", ")}）` : ""} | ${shot.buy_s || "—"} | ${FRAME[shot.first_frame.kind]} | ${shot.end_frame.planned ? (shot.end_frame.file ? "已畫" : "待畫") : "—"} | ${risk} | ${cost} |`);
  }
  const risky = plan.shots.filter((shot) => shot.risk.reasons.length);
  if (risky.length) {
    out.push("");
    out.push("## 風險與重設計");
    out.push("");
    for (const shot of risky) {
      out.push(`- **${shot.id}（${shot.risk.grade}）**`);
      for (const reason of shot.risk.reasons) out.push(`  - ${reason.id}（${reason.grade}）：${reason.why}。改法：${reason.redesign}`);
    }
  }
  out.push("");
  out.push("## 承諾與連戲鎖（鎖定時寫進 plan/lock.json）");
  out.push("");
  out.push(`- 承諾（類型、買幾秒、路線、fit）：${plan.shots.map((shot) => `${shot.id} ${KIND[shot.visual]}${shot.buy_s ? ` ${shot.buy_s} s` : ""}${shot.promise.fit !== "auto" ? ` fit ${shot.promise.fit}` : ""}`).join("、")}。鎖定後 clip 改成 still、切或 fit freeze，drama_preflight.mjs 以 exit 1 擋，直到站主的變更單`);
  const locked = plan.shots.filter((shot) => shot.continuity.depends_on.length || CONTINUITY_CATEGORIES.some((category) => shot.continuity.locks[category].length));
  if (locked.length) for (const shot of locked) out.push(`- ${shot.id}：${shot.continuity.depends_on.length ? `接 ${shot.continuity.depends_on.join("、")}；` : ""}${CONTINUITY_CATEGORIES.filter((category) => shot.continuity.locks[category].length).map((category) => `${CONTINUITY_LABELS[category]} ${shot.continuity.locks[category].map((term) => `「${term}」`).join("")}`).join("、") || "沒有鎖定字（只接前一鏡的素材或末格）"}`);
  else out.push("- 沒有鏡頭共用道具、服裝或時刻的字：連戲只靠 look 與人設圖；prompt 裡把錨點（髮繩、袖扣、時刻）每鏡寫一樣的字才鎖得住");
  const clips = plan.shots.filter((shot) => shot.prompt);
  if (clips.length) {
    out.push("");
    out.push(plan.route === "server" ? "## 送出的片段提示（clipPrompt）" : "## 定稿正文（照貼；鎖定後改字要走變更單）");
    out.push("");
    const negative = clips.find((shot) => shot.prompt.negative)?.prompt.negative;
    if (plan.route !== "server" && negative) {
      out.push(`負面欄（網頁真的有負面欄才貼；沒有就不貼，否定句會被畫成正向）：\`${negative}\``);
      out.push("");
    }
    for (const shot of clips) {
      const frame = shot.first_frame.file ? `首格 ${shot.first_frame.file}${shot.first_frame.sha256 ? `（sha256 ${shot.first_frame.sha256.slice(0, 12)}…）` : ""}` : "首格：待畫";
      out.push(`### ${shot.id}：買 ${shot.buy_s} s，${frame}${shot.end_frame.planned ? `，末格 ${shot.end_frame.file ?? "待畫"}` : ""}`);
      out.push("");
      out.push("```text");
      out.push(shot.prompt.text);
      out.push("```");
      out.push("");
      out.push(`${shot.prompt.chars} 字，sha256 ${shot.prompt.sha256.slice(0, 16)}`);
      for (const note of shot.prompt.notes) out.push(`- ${note}`);
      out.push("");
    }
  }
  out.push("## 批次順序");
  out.push("");
  for (const batch of plan.batches) out.push(`- **${batch.name}**：買 ${batch.buys.join(", ") || "（不買片段）"}；鏡頭 ${batch.shots.join(", ")}；一次 ${money(plan, batch.cost_one)}。${batch.why}${batch.checkpoint ? "【檢查點】" : ""}`);
  const { levers } = plan;
  const leverLines = [
    ...levers.cuts.map((cut) => `- 可切：${cut.shot} 從 ${cut.from_shot} 的素材 ${cut.from_s} s 切（data.source），省一支${cut.picture_differs ? "；同鏡位但畫面不同，要人看" : ""}`),
    ...levers.merges.map((merge) => `- 可併：${merge.shots.join(" + ")}（同鏡位同角色，合起來 ${merge.seconds} s）`),
    ...levers.long.map((shot) => `- 超過 8 秒：${shot.id}（${shot.seconds} s）`),
  ];
  if (leverLines.length) {
    out.push("");
    out.push("## 槓桿（episode_estimate 的找法，伺服器模型下算）");
    out.push("");
    out.push(...leverLines);
  }
  if (plan.problems.length || plan.notes.length) {
    out.push("");
    out.push("## 問題與註記");
    out.push("");
    for (const problem of plan.problems) out.push(`- 【${problem.level === "refuse" ? "做不進產線" : "會白花"}】${problem.shot ? `${problem.shot}：` : ""}${problem.what}。改法：${problem.fix}`);
    for (const note of plan.notes) out.push(`- 註：${note}`);
  }
  return out.join("\n");
}

const CSV_COLUMNS = ["id", "chapter", "setup", "camera", "characters", "need_s", "visual", "source", "buy_s", "first_frame", "end_frame", "risk", "risk_reasons", "expected_takes", "cost_one", "cost_expected", "cost_cap", "prompt_sha256", "fit", "depends_on", "locks"];
export function renderCsv(plan) {
  const quote = (value) => (/[",\n]/.test(String(value)) ? `"${String(value).replace(/"/g, '""')}"` : String(value));
  const rows = plan.shots.map((shot) => [
    shot.id, shot.chapter, shot.setup, shot.camera, shot.characters.join(" "), shot.need_s, shot.visual,
    shot.source ? `${shot.source.shot}@${shot.source.from_s}` : "", shot.buy_s, shot.first_frame.file ?? shot.first_frame.kind,
    shot.end_frame.planned ? shot.end_frame.file ?? "to-draw" : "", shot.risk.grade, shot.risk.reasons.map((reason) => reason.id).join(" "),
    shot.risk.expected_takes, shot.cost.one, shot.cost.expected, shot.cost.cap, shot.prompt?.sha256 ?? "",
    shot.promise.fit, shot.continuity.depends_on.join(" "), CONTINUITY_CATEGORIES.flatMap((category) => shot.continuity.locks[category].map((term) => `${category}:${term}`)).join("; "),
  ].map(quote).join(","));
  return [CSV_COLUMNS.join(","), ...rows].join("\n");
}

const number = (value, flag) => {
  if (value === undefined) return undefined;
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) throw new Error(`${flag} must be a number ≥ 0`);
  return parsed;
};

/**
 * 讀一集：{ doc, series, lexicon, dir, timeline, timeline_stale, manifest, file, workdir }。--slug 走 tools/video 的
 * 路徑規則（loadProject、resolveWorkdir）；給檔案時 --workdir 是這支影片自己的工作目錄。錄好的 timeline.json
 * 只在它的 speech_hash 等於現在的劇本時才用（否則是改台詞之前的秒數，退回 lint 的估法並標 timeline_stale）。
 */
export function loadInputs({ file, slug, workdir: workdirFlag, root, timeline: timelineFile, env = process.env, home }) {
  const repo = root ?? ROOT;
  if (!file && !slug) throw new Error("give a video.json or --slug");
  const project = loadProject({ slug, file, root: repo });
  const { doc } = project;
  const workdir = slug ? resolveWorkdir({ flag: workdirFlag, env, slug: doc.slug ?? slug, root: repo, home }) : workdirFlag ? path.resolve(workdirFlag) : null;
  const timelinePath = timelineFile ?? (workdir ? path.join(workdir, "timeline.json") : null);
  const recorded = timelinePath && existsSync(timelinePath) ? readJson(timelinePath, null) : null;
  let current = Boolean(recorded?.scenes);
  if (current && recorded.speech_hash) {
    try {
      current = recorded.speech_hash === speechHash(doc, project.lexicon);
    } catch {
      current = false;
    }
  }
  const manifest = workdir ? readJson(path.join(workdir, "keyframes", "manifest.json"), null) : null;
  return { doc, series: project.series, lexicon: project.lexicon, dir: project.dir, timeline: current ? recorded : null, timeline_stale: Boolean(recorded?.scenes) && !current, manifest, file: project.file, workdir };
}

/** --expected-takes A,B,C（例如 1.5,2,3）：換掉 EXPECTED_TAKES 的三個數，看預算對 take 率有多敏感。 */
export function expectedTakesFlag(value) {
  if (value === undefined) return undefined;
  const parts = String(value).split(",").map(Number);
  if (parts.length !== 3 || parts.some((each) => !Number.isFinite(each) || each < 1)) throw new Error("--expected-takes wants three numbers >= 1 for A,B,C");
  return { A: parts[0], B: parts[1], C: parts[2] };
}

/** 三支腳本共用的規劃旗標：plan_lock 與 animatic 收同一組，鎖定的就是 shot_plan 算的那一份。 */
export const PLAN_FLAGS = {
  route: { type: "string" },
  plan: { type: "string" },
  model: { type: "string" },
  resolution: { type: "string" },
  timeline: { type: "string" },
  handle: { type: "string" },
  "clip-takes": { type: "string" },
  "hailuo-model": { type: "string" },
  "expected-takes": { type: "string" },
  pilot: { type: "string" },
  production: { type: "boolean" },
};
export const PLAN_USAGE = "[--route server|hailuo|kling] [--plan hailuo:pro|kling:pro|...] [--hailuo-model h3|2.3] [--model <server clip model>] [--resolution 1080p|720p|768p|2k] [--timeline <timeline.json>] [--handle 0.5] [--clip-takes 2] [--expected-takes 1.2,1.5,2] [--pilot s04,s05,s06] [--production]";

/** parseArgs 的值 → planEpisode 的選項（只有使用者真的給了的）。 */
export function planOptions(values) {
  const options = {};
  if (values.route !== undefined) options.route = values.route;
  if (values.plan !== undefined) options.plan = values.plan;
  if (values.model !== undefined) options.model = values.model;
  if (values.resolution !== undefined) options.resolution = values.resolution;
  if (values.handle !== undefined) options.handle = number(values.handle, "--handle");
  if (values["clip-takes"] !== undefined) {
    options.clipTakes = number(values["clip-takes"], "--clip-takes");
    if (!Number.isInteger(options.clipTakes) || options.clipTakes < 1) throw new Error("--clip-takes must be a whole number >= 1");
  }
  if (values["hailuo-model"] !== undefined) options.hailuoModel = values["hailuo-model"];
  if (values["expected-takes"] !== undefined) options.expectedTakes = expectedTakesFlag(values["expected-takes"]);
  if (values.pilot !== undefined) options.pilot = String(values.pilot).split(",").map((id) => id.trim()).filter(Boolean);
  if (values.production) options.production = true;
  return options;
}

export function main(argv, stdout = process.stdout, stderr = process.stderr) {
  let values;
  let positionals;
  try {
    ({ values, positionals } = parseArgs({
      args: argv,
      options: {
        ...PLAN_FLAGS,
        slug: { type: "string" },
        workdir: { type: "string" },
        root: { type: "string" },
        markdown: { type: "boolean" },
        csv: { type: "boolean" },
        json: { type: "boolean" },
        strict: { type: "boolean" },
      },
      allowPositionals: true,
      strict: true,
    }));
  } catch (error) {
    stderr.write(`${error.message}
`);
    return 2;
  }
  if (!positionals[0] && !values.slug) {
    stderr.write(`usage: shot_plan.mjs <video.json> | --slug <SLUG> [--workdir <dir>] ${PLAN_USAGE} [--markdown|--csv|--json] [--strict]
`);
    return 2;
  }
  let plan;
  let inputs;
  try {
    inputs = loadInputs({ file: positionals[0], slug: values.slug, workdir: values.workdir, root: values.root, timeline: values.timeline });
    plan = planEpisode(inputs.doc, { ...planOptions(values), timeline: inputs.timeline, manifest: inputs.manifest, series: inputs.series, timelineStale: inputs.timeline_stale });
  } catch (error) {
    stderr.write(`${positionals[0] ?? values.slug}: ${error.message}
`);
    return 2;
  }
  const label = path.relative(process.cwd(), inputs.file) || inputs.file;
  stdout.write(`${values.json ? JSON.stringify({ file: label, ...plan }, null, 2) : values.csv ? renderCsv(plan) : renderMarkdown(plan, label)}
`);
  return values.strict && plan.problems.length ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exitCode = main(process.argv.slice(2));
