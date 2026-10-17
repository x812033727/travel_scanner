import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Offline visual-only proposal. All source material stays in the pinned pacing candidate.
const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../B18-pacing-candidate-20261016');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const pins = {
  'series.json': '54152ce70772ffb1890ef83fdc0dec8dfd8071afe75db976b7b08975cfea5c97',
  'chapters/hook.json': '370baea920b35bd5c774bfc4e199d920a9c406f0f470d32c4e2430a300955388',
  'chapters/origin.json': '27a112e43e1c4dcac704b1aab4b5c2a0e5364eb2990e3ad3f5909fdf70196587',
  'chapters/idea.json': 'f4c1d60c6eeabe43bbca30ff507d8ad0b17c07a6c4fb59012cffa580f13f067b',
  'chapters/engine.json': '776a6bacf30acee4f124c8a53f3e3922f30117cfb0abad556bd2aea91617f4f1',
  'chapters/turn.json': 'e9ee024b6a4a83db3519679b2bcbf25c18437ebd09ed598054c9046fba2f3c4a',
  'chapters/now.json': 'a4b592f267938e570875d717942e3e9f95eabeab7aa419ef5b52367e30df8570',
};
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => fs.readFileSync(file, 'utf8');
for (const [name, expected] of Object.entries(pins)) {
  assert.equal(sha(fs.readFileSync(path.join(base, name))), expected, `pacing input drift: ${name}`);
}
const series = JSON.parse(read(path.join(base, 'series.json')));
const previous = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(path.join(base, 'chapters', `${key}.json`)))]));
const chapters = structuredClone(previous);

// Prompt order follows the story, not a reusable visual template. Each describes one
// illustrative instant. Anonymous figures must never be presented as source portraits.
const prompts = {
  'hook-s001': `Wide shot of an illustrative 1948 bottling floor in Suita, Japan, one anonymous attendant guiding an unlabelled glass bottle onto a straight conveyor, the bottle line receding under tall factory windows, pale overcast daylight from the left.`,
  'hook-s002': `Medium shot inside an illustrative postwar Japanese bottling hall, one anonymous restaurant visitor gripping a simple rail as he follows the moving bottles with wide, curious eyes, rows of blank glass bottles crossing below him, soft window light from above.`,
  'hook-s003': `Close-up behind a narrow late-1940s Osaka sushi counter, one tired anonymous chef stretching his arm across the gap with a single plate, his worried face just beyond his hand, a waiting stool opposite, low window light from the right.`,
  'hook-s004': `Medium shot at a simplified 1950s Japanese workshop bench, one anonymous maker lunging to steady a plate tilting at a tight conveyor bend, overlapping belt pieces crowding the corner beneath it, soft light from a side window.`,
  'hook-s005': `Wide shot of a plain temporary sushi counter at an illustrative 1970 Osaka exhibition, one visitor hesitating at the aisle entrance as a wooden sushi tub approaches on the moving belt, simple pavilion walls behind, diffused daylight from above.`,
  'hook-s006': `Medium shot at an illustrative early-1970s Japanese office desk, one anonymous restaurant operator sliding a closed blank rights folder away from a small plain conveyor sketch, an empty plate near the opposite edge, muted window light from the left.`,
  'hook-s007': `Wide shot inside an illustrative postwar Osaka standing sushi shop, one exhausted chef passing a plate over a long narrow counter while unserved places continue behind it, his outstretched arm draws the eye, daylight through the front window.`,

  'origin-s008': `Wide shot of a modest illustrative 1947 restaurant frontage in Fuse, Osaka, one anonymous newcomer lifting a plain travel bag toward a doorway under an empty signboard, a short counter visible through the open door, soft morning light from the street.`,
  'origin-s009': `Medium shot at a postwar Osaka standing sushi counter, one young factory worker setting a plain lunch bag at his feet while leaning toward one freshly served plate, simple work clothes and a bare wooden counter, gentle light from the shop entrance.`,
  'origin-s011': `Medium shot in an illustrative late-1940s Osaka sushi shop, one anonymous attendant raising a blank price board above a standing counter, a single small plate below and his hopeful expression visible in profile, grey daylight from the front window.`,
  'origin-s014': `Medium shot from behind an illustrative postwar sushi counter, one chef straining to hand a prepared plate across to an empty stool while more plates wait by his elbow, the distance his arm must cover fills the frame, soft window light.`,
  'origin-s015': `Close-up at a late-1940s Osaka preparation bench, one weary chef placing another prepared plate beside several waiting dishes, his furrowed face above the growing row, simple wood and ceramic surfaces, light from a small side window.`,
  'origin-s016': `Wide shot of an illustrative postwar restaurant back room, one young kitchen worker carrying a neatly folded plain apron toward the exit, a vacant preparation station in the foreground, afternoon light falling through the half-open door.`,
  'origin-s019': `Wide shot along a narrow Osaka sushi counter in the late 1940s, one chef stopping halfway through a long walk with a plate in both hands, empty stools stretching away from him, a strip of window light marking the remaining route.`,
  'origin-s020': `Medium shot in an illustrative Osaka shop after 1948, one anonymous operator tracing the curved edge of a small blank counter model with one finger, empty plates arranged around its rim, his face intent on the corner, soft overhead light.`,
  'origin-s021': `Medium shot of a conceptual 1950s Japanese counter model, one seated diner reaching only a short distance to take a plate from a simple moving route, the chef's working area left open behind the belt, gentle light from a side window.`,
  'origin-s022': `Close-up over a 1950s Japanese workshop bench, one maker lifting an empty plate just above the junction where a straight conveyor meets a tight turn, the unsupported inner edge clearly visible, mild daylight from a high window.`,

  'idea-s023': `Medium shot at an illustrative 1950s Osaka workshop table, one mechanic leaning toward a plate balanced awkwardly on a cramped conveyor corner, eyebrows raised as the straight section continues behind it, grey light from a side window.`,
  'idea-s024': `Close-up at a simplified 1950s conveyor bend, one technician's hand catching an empty plate before it slips from a pinched inner edge, layered belt segments pressing together beneath the rim, soft light from above.`,
  'idea-s025': `Wide shot of an illustrative small Osaka metalworking shop in the 1950s, one anonymous maker carrying a plain sushi plate toward an unfinished conveyor frame on a workbench, scattered ordinary tools kept in the background, daylight through workshop windows.`,
  'idea-s026': `Close-up at a plain mid-century Japanese tabletop, one anonymous hand opening a fan of thin blank rectangular sheets, their widening outer edges echoing the shape of a conveyor corner sketched without marks nearby, gentle side light.`,
  'idea-s028': `Close-up at an illustrative mid-century Japanese household table, one anonymous child smiling while fanning face-up playing cards across the wood, simple heart and spade suit symbols visible on the cards, soft daylight from a nearby window.`,
  'idea-s029': `Medium shot at a separate illustrative mid-century Japanese work desk, one anonymous adult spreading blank business cards into a neat fan beside a closed plain notebook, the hands and overlapping card corners centered, diffused lamp light.`,
  'idea-s030': `Medium shot at a present-day research table, one reader moving two different blank folders apart instead of joining them, a single fan-shaped metal sample between the folders, a thoughtful expression and gentle desk-lamp light.`,
  'idea-s031': `Close-up at an illustrative 1950s Japanese metal bench, one maker fitting a fan-shaped metal plate against its neighbors to form a smooth curve, the touching plate edges and his careful fingers sharp in the foreground, light from a workshop window.`,
  'idea-s034': `Wide shot of a simplified 1957 Japanese workshop, one anonymous technician testing a compact circular conveyor table by setting an empty plate on its straight section, the finished corner visible farther around, diffused light through high windows.`,
  'idea-s035': `Close-up at an illustrative 1957 metalworking bench, one technician holding a smooth metal strip beside a rust-speckled sample, the difference between their surfaces clear under a small work lamp, ordinary tools blurred behind.`,
  'idea-s037': `Close-up at an illustrative 1950s workshop desk, one anonymous restaurant operator setting a sealed blank payment envelope beside a metal sample, his open hand pauses above the material, soft lamp light on the tabletop.`,
  'idea-s040': `Medium shot inside a not-yet-open illustrative 1957 sushi shop, one worker placing an empty plate on a completed circular counter route, a closed plain entrance beyond the empty seats, quiet daylight from the front window.`,

  'engine-s042': `Wide shot of an illustrative compact 1958 counter-only sushi shop near Fuse Station, one seated customer smiling as she takes a plate from the moving belt, the tight ring of stools showing the small scale, soft daylight from the entrance.`,
  'engine-s043': `Medium shot behind an illustrative 1958 Osaka sushi counter, one chef releasing a prepared plate onto the moving belt and watching it leave his hand, his relieved face above the worktop, gentle light from the shop window.`,
  'engine-s046': `Wide shot from the pavement outside an illustrative late-1950s Osaka sushi shop, one passerby stopping at a broad plain window to watch a plate travel past inside, blank storefront sign above him, soft afternoon street light.`,
  'engine-s047': `Medium shot at an illustrative circa-1960 Japanese restaurant office, one anonymous shop operator studying a simple unmarked drawing of a circulating counter with a concerned expression, a glimpse of ordinary street shops through the window, muted daylight.`,
  'engine-s048': `Wide shot in an illustrative Osaka shopping lane during a later expansion period, one worker raising the shutter of another plain sushi storefront, the curved counter just visible within, neighboring shop signs left blank, soft morning light.`,
  'engine-s050': `Close-up at an illustrative 1960s Japanese engineering desk, one technician pointing to a simple blank diagram of a conveyor built into a counter while a separate sushi plate sits outside the paper, the device drawing lit by a desk lamp.`,
  'engine-s052': `Wide shot inside an illustrative 1960s Japanese legal office, one office professional placing a closed unmarked warning envelope beside a simplified conveyor-table sketch, rows of plain folders behind, subdued daylight from a high window.`,
  'engine-s053': `Close-up at an illustrative 1960s conveyor sushi counter, one delighted diner's face following a single plate as it glides past, the unmistakable moving route just below the face, a soft pool of light from the shop window.`,
  'engine-s054': `Wide shot of an ordinary late-1960s Osaka street, one pedestrian stopping beneath a small blank sushi sign while the shop's circulating counter is visible deep inside, most of the street continuing beyond it, overcast daylight.`,
  'engine-s055': `Wide shot of an illustrative 1970 Osaka exhibition forecourt, one visitor turning from a plain pavilion aisle toward a temporary sushi counter in the distance, simple hanging bunting and an unsigned entrance, soft open-air daylight.`,
  'engine-s056': `Medium shot in an illustrative 1970 Osaka restaurant office, one operator opening a plain invitation envelope above an unmarked exhibition floor sketch, his alert face and the opened flap nearest the viewer, gentle window light.`,
  'engine-s057': `Wide shot beside an illustrative 1970 exhibition station walkway in Osaka, one passenger leaving the raised platform and walking toward a temporary unsigned sushi frontage below, the clear footpath between them, hazy daylight.`,
  'engine-s058': `Medium shot behind an illustrative 1970 temporary sushi counter, one kitchen worker quickly filling a plain serving tub at a crowded preparation bench, his tense face above a row of waiting tubs, soft overhead pavilion light.`,
  'engine-s060': `Close-up at an illustrative 1970 exhibition counter, one cook using both hands to settle a plain wooden sushi tub securely onto a moving conveyor, a smaller ordinary plate held back on the work surface, diffused pavilion light.`,
  'engine-s062': `Wide shot along an illustrative 1970 exhibition sushi counter, one worker withdrawing his hands as a filled plain tub travels toward a waiting seat, the moving route cutting through the busy space, soft light from the pavilion roof.`,

  'turn-s065': `Medium shot at an illustrative 1970 Osaka exhibition sushi counter, one traveler setting a plain suitcase beside a stool before reaching for an arriving wooden tub, the belt crossing the foreground, diffused daylight from the pavilion entrance.`,
  'turn-s076': `Medium shot in an illustrative early-1970s Japanese restaurant office, one shop operator lifting an unmarked rights folder over a small conveyor-table model, his uncertain face turned toward the blank cover, soft light from a side window.`,
  'turn-s077': `Medium shot at a separate illustrative early-1970s Japanese records desk, one clerk closing a plain application binder beside a simplified counter diagram, the binder's worn blank tab nearest the viewer, quiet desk-lamp light.`,
  'turn-s079': `Wide shot of an illustrative 1970s Japanese commercial street, one pedestrian walking toward a newly opened unsigned conveyor sushi shop while a different modest counter frontage stands farther back, separate doorways clear in overcast daylight.`,
  'turn-s080': `Medium shot outside an illustrative later-era Japanese sushi restaurant, one worker fastening a fresh blank signboard above a familiar conveyor counter visible through the doorway, his hands on the new board, soft morning light.`,
  'turn-s081': `Close-up at an illustrative late-1970s restaurant office table, one operator separating a plain exhibition booklet from a different blank branch folder, the two paper histories kept apart beside a single plate, warm desk-lamp light.`,
  'turn-s070': `Close-up at an illustrative early-1970s Japanese sushi counter, one diner lifting an empty ceramic teacup and looking toward a small counter-mounted spout, a sushi plate waiting beside the cup, gentle overhead light.`,
  'turn-s072': `Medium shot at an illustrative early-1970s Japanese sushi counter, one diner pressing a plain ceramic cup beneath a simple built-in tea spout, his surprised smile visible above the cup, soft light from the dining room.`,
  'turn-s075': `Wide shot at an illustrative mid-1970s Japanese equipment demonstration counter, one technician aligning a simple tea dispenser with a separate conveyor route, the cup landing point and plate path both clear, mild overhead light.`,
  'turn-s083': `Medium shot from an illustrative early-1980s Japanese dining room toward the kitchen opening, one cook setting a plate onto a straight conveyor that leads directly out of the back room, its uninterrupted path toward a seat, soft indoor light.`,
  'turn-s084': `Wide shot inside a different illustrative early-1980s sushi dining room, one diner stretching an arm to a plate on a long straight conveyor beside the tables, the route passing without a bend, diffuse daylight from broad windows.`,
  'turn-s085': `Medium shot in an illustrative 1980s restaurant storeroom, one operator turning a differently colored plain plate in his hands while a closed fish crate rests behind him, his calculating expression above the plate rim, mild window light.`,
  'turn-s086': `Wide shot at an illustrative 1980s Japanese fish cooperative loading area, one restaurant buyer lifting a plain fish crate from the dock toward an unmarked handcart, the short path from source to buyer visible, grey morning light.`,
  'turn-s087': `Close-up at an illustrative 1980s Japanese sushi service counter, one attendant arranging three plainly different plate colors beside a blank price board, the contrasting rims lined up at hand height, soft overhead light.`,
  'turn-s088': `Medium shot at an illustrative 1980s conveyor sushi counter, one diner smiling as she selects a plate by its colored rim while other dishes continue past, the chosen rim and her expression clear, light from a side window.`,
  'turn-s089': `Wide shot outside an illustrative mid-1980s suburban Japanese sushi restaurant, one attendant unlocking broad glass entrance doors, a larger dining room visible through them and a plain blank sign overhead, soft late-afternoon daylight.`,
  'turn-s090': `Wide shot inside an illustrative late-1980s suburban sushi restaurant, one attendant placing a child seat beside a family-sized table near the conveyor, the extra floor space around the table visible, mellow indoor light.`,
  'turn-s091': `Medium shot in an illustrative late-1980s sushi dining room, one operator sliding a chair toward a table served by a straight conveyor, a plain fish crate and a few colored plates kept small in the background, gentle ceiling light.`,
  'turn-s092': `Close-up at an illustrative 1991 Japanese reading desk, one reader opening a thick plain dictionary beside an empty sushi plate, his curious face reflected in the desk lamp's light, blank page surfaces facing the viewer.`,

  'now-s096': `Close-up on a simple demonstration workbench, one fan-shaped metal sample representing an early turn plate lying apart from a small simplified model of a later conveyor, open tabletop between the two plain objects, soft overhead light.`,
  'now-s097': `Medium shot at an illustrative 2023 research desk, one reader unfolding a plain report beside a blank notepad, an unlettered chart shape on the paper without numbers, thoughtful expression under a simple desk lamp.`,
  'now-s099': `Medium shot at a present-day research table, one reader closing the older blank market report while glancing toward a small plain model of an old counter, the two objects separated by empty tabletop, soft light from the left.`,
  'now-s100': `Close-up at a present-day unbranded Japanese sushi counter, one diner's hand reaching just as a single plate comes around the belt, the short last gap between plate and fingertips clear, warm light from a hanging lamp.`,
  'now-s101': `Wide overhead shot of one present-day unbranded Japanese sushi counter, one diner reaching toward a plate that has just rounded a visible corner, open seats and the continuing belt leading toward a plain exit, gentle ceiling light.`,
  'now-s101b': `Wide street-level shot of an illustrative 2023 Japanese shopping block, one passerby pausing at an unsigned conveyor sushi entrance, the belt visible through its window amid varied ordinary neighboring shops, soft overcast daylight.`,
  'now-s102': `Medium shot from behind one diner at a present-day unbranded sushi counter, their hand hovering above a nearby plate while a smiling profile follows another plate approaching on the belt, the choice held in a single moment, warm lamp light.`,
  'now-s103': `Wide shot of one present-day unbranded sushi counter, one diner setting down an empty plate with a satisfied smile as the belt continues around the corner, a broad plain wall left clear at upper right for end-screen graphics, soft evening lamp light.`,
};

// These scene-specific nouns keep the route and food legible without making every
// location the same "sushi counter" and every object the same "plate".
const diction = {
  'hook-s003': [['sushi counter', 'serving counter']],
  'hook-s005': [['sushi counter', 'food counter']],
  'hook-s006': [['an empty plate', 'an empty ceramic dish']],
  'origin-s011': [['sushi shop', 'restaurant'], ['a single small plate', 'a small serving dish']],
  'origin-s014': [['sushi counter', 'standing counter']],
  'origin-s015': [['prepared plate', 'serving dish']],
  'origin-s019': [['sushi counter', 'serving counter']],
  'origin-s020': [['empty plates', 'small ceramic dishes']],
  'idea-s025': [['sushi plate', 'ceramic serving dish']],
  'idea-s034': [['an empty plate', 'a ceramic dish']],
  'idea-s040': [['sushi shop', 'restaurant'], ['an empty plate', 'a ceramic dish']],
  'engine-s042': [['sushi shop', 'restaurant']],
  'engine-s043': [['sushi counter', 'moving-belt counter']],
  'engine-s046': [['sushi shop', 'restaurant']],
  'engine-s048': [['sushi storefront', 'restaurant frontage']],
  'engine-s050': [['sushi plate', 'serving dish']],
  'engine-s053': [['sushi counter', 'dining counter'], ['single plate', 'single ceramic dish']],
  'engine-s054': [['sushi sign', 'restaurant sign']],
  'engine-s055': [['sushi counter', 'food counter']],
  'engine-s057': [['sushi frontage', 'restaurant entrance']],
  'engine-s058': [['sushi counter', 'dining counter']],
  'engine-s060': [['ordinary plate', 'serving dish']],
  'engine-s062': [['sushi counter', 'dining counter']],
  'turn-s065': [['sushi counter', 'dining counter']],
  'turn-s070': [['sushi counter', 'dining counter'], ['sushi plate', 'small serving dish']],
  'turn-s075': [['plate path', 'dish path']],
  'turn-s081': [['single plate', 'single ceramic dish']],
  'turn-s083': [['a plate', 'a ceramic dish']],
  'turn-s084': [['a plate', 'a serving dish']],
  'turn-s085': [['plate in his hands', 'dish in his hands'], ['plate rim', 'dish rim']],
  'turn-s087': [['three plainly different plate colors', 'three differently colored ceramic dishes']],
  'turn-s091': [['colored plates', 'colored dishes']],
  'turn-s092': [['sushi plate', 'small serving dish']],
};

const changes = [];
const shots = keys.flatMap((key) => chapters[key].scenes.filter((scene) => scene.template === 'shot').map((scene) => [key, scene]));
assert.equal(shots.length, 71, 'pacing shot count drift');
assert.equal(Object.keys(prompts).length, shots.length, 'must provide one prompt for every shot');
for (const [chapter, scene] of shots) {
  let after = prompts[scene.id]
    ?.replace(/\ban illustrative (?=(?:early|ordinary|Osaka)\b)/gi, 'an ')
    .replace(/\ban illustrative /gi, 'a ')
    .replace(/\billustrative /gi, '');
  for (const [before, replacement] of diction[scene.id] ?? []) {
    assert(after.includes(before), `wording anchor drift: ${scene.id}/${before}`);
    after = after.replace(before, replacement);
  }
  assert.equal(typeof after, 'string', `missing visual prompt: ${scene.id}`);
  assert(after.trim().length >= 100 && after.length <= 900, `prompt length: ${scene.id}`);
  assert(!/\b(?:generic|neutral|focal|cartoon|chibi|cinematic|photorealistic)\b/i.test(after), `look or repetitive boilerplate: ${scene.id}`);
  assert(!/\bno (?:text|logo|brand|numerals|people)\b/i.test(after), `use positive blank props: ${scene.id}`);
  assert.notEqual(after, scene.data.prompt, `unchanged prompt: ${scene.id}`);
  changes.push({ chapter, scene: scene.id, field: 'data.prompt', before: scene.data.prompt, after });
  scene.data.prompt = after;
}
assert.deepEqual(shots.map(([, scene]) => scene.id).sort(), Object.keys(prompts).sort(), 'unknown visual ID');
const withoutPrompts = (input) => {
  const clone = structuredClone(input);
  for (const key of keys) for (const scene of clone[key].scenes) if (scene.template === 'shot') delete scene.data.prompt;
  return clone;
};
assert.deepEqual(withoutPrompts(chapters), withoutPrompts(previous), 'non-prompt chapter data changed');

const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(root, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs')).href);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline visual build must not fetch'); };
const slug = 'story-conveyor-belt-sushi-v2';
const authored = path.resolve(base, '../B18-authored-chapters-candidate');
const voice = JSON.parse(read(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'video.json'))).voice;
const originalDoc = composeStory({ slug, info: series, chapters: previous, voice, drama: { music_enabled: false }, root });
const doc = composeStory({ slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-visual-'));
let lint;
try {
  const shelf = path.join(tmp, 'docs', 'videos');
  const dir = path.join(shelf, slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'video.json'), canonical(doc));
  fs.writeFileSync(path.join(dir, 'series.json'), canonical(series));
  fs.copyFileSync(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'brief.md'), path.join(dir, 'brief.md'));
  fs.copyFileSync(path.join(authored, 'fixtures/lexicon.json'), path.join(shelf, 'lexicon.json'));
  lint = lintProject(loadProject({ slug, root: tmp }));
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
assert.deepEqual(lint.errors, [], `official lint errors: ${JSON.stringify(lint.errors)}`);
assert.deepEqual(cuteStoryVisualProblems(doc), [], 'cute visual lint errors');
assert.equal(externalCalls, 0, 'external call count');
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
assert.equal(doc.subtitles.burn_in, false);
const stripDocPrompts = (input) => {
  const clone = structuredClone(input);
  for (const scene of clone.scenes) if (scene.template === 'shot') delete scene.data.prompt;
  return clone;
};
assert.deepEqual(stripDocPrompts(doc), stripDocPrompts(originalDoc), 'composed document changed outside prompt');
assert.equal(doc.scenes.length, 90);
assert.equal(doc.scenes.filter((scene) => scene.template === 'shot').length, 71);
assert.equal(keys.flatMap((key) => chapters[key].claims).length, 65);
assert(keys.every((key) => chapters[key].claims.every((claim) => claim.verdict === 'UNCHECKED')));
const estimatedBodySeconds = estimateTimeline(doc).total_frames / 30;
assert.equal(estimatedBodySeconds, 573, 'pacing estimate changed');
const speech = keys.flatMap((key) => chapters[key].scenes.flatMap((scene) => scene.lines.map((line) => line.text)));
const story = [
  '# B18 畫面指向候選逐鏡表（離線、未審）', '',
  '這些提示詞只供 MiniMax image-01 的單格示意插畫；人物與場景不是真實照片、史料重建或館藏實物。',
  '旁白、65 筆 UNCHECKED 主張、來源、懸念、鏡頭次序與估時全沿用節奏版。', '',
  ...keys.flatMap((key) => [
    `## ${key}｜${chapters[key].title}`, '',
    ...chapters[key].scenes.flatMap((scene) => [
      `### ${scene.id} [${scene.template}]`, '',
      `旁白：${scene.lines.map((line) => line.text).join('')}`, '',
      ...(scene.template === 'shot' ? [`鏡位：${scene.data.camera}`, '', `畫面：${scene.data.prompt}`, ''] : []),
    ]),
  ]),
].join('\n');
const result = {
  schema_version: 1,
  status: 'OFFLINE_VISUAL_DIRECTION_CANDIDATE_NOT_REVIEWED',
  base_pins: pins,
  scenes: doc.scenes.length,
  lines: speech.length,
  claims_unchecked: 65,
  illustrations: 71,
  cards: 19,
  prompt_changes: changes.length,
  camera_changes: 0,
  non_prompt_changes: 0,
  estimated_body_seconds: estimatedBodySeconds,
  estimated_total_seconds_with_assumed_animations: estimatedBodySeconds + 26,
  measured_body_seconds: null,
  lint_errors: lint.errors,
  cute_errors: [],
  lint_warnings: lint.warnings.length,
  generic_prompt_count: doc.scenes.filter((scene) => scene.template === 'shot' && /\bgeneric\b/i.test(scene.data.prompt)).length,
  neutral_prompt_count: doc.scenes.filter((scene) => scene.template === 'shot' && /\bneutral\b/i.test(scene.data.prompt)).length,
  focal_prompt_count: doc.scenes.filter((scene) => scene.template === 'shot' && /\bfocal\b/i.test(scene.data.prompt)).length,
  external_calls: externalCalls,
  worker_pass: false,
  images_generated: 0,
};
const output = new Map([
  ['series.json', canonical(series)],
  ['delta.json', canonical({ schema_version: 1, status: result.status, base_pins: pins, changes })],
  ['READABLE-SHOTLIST.md', `${story.trimEnd()}\n`],
  ['lint-warnings.json', canonical(lint.warnings)],
  ['verification.json', canonical(result)],
]);
for (const key of keys) output.set(`chapters/${key}.json`, canonical(chapters[key]));
const hashes = Object.fromEntries([
  ['build.mjs', sha(fs.readFileSync(path.join(here, 'build.mjs')))],
  ['README.md', sha(fs.readFileSync(path.join(here, 'README.md')))],
  ['VISUAL-REVIEW.md', sha(fs.readFileSync(path.join(here, 'VISUAL-REVIEW.md')))],
  ...[...output].map(([name, content]) => [name, sha(content)]),
]);
output.set('sha256.json', canonical({ schema_version: 1, files: hashes }));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of output) {
  const file = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  } else assert.equal(read(file), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify({ scenes: result.scenes, prompt_changes: result.prompt_changes, non_prompt_changes: 0, estimated_body_seconds: estimatedBodySeconds, lint_errors: 0, cute_errors: 0, lint_warnings: result.lint_warnings, generic_prompt_count: 0, neutral_prompt_count: 0, focal_prompt_count: 0 }, null, 2));
