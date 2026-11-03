// Round 5: the chosen hosts (A in the trench, B in the camel coat) in close-ups and travel
// scenes, each drawn with the round-4 sheet as a character reference, to check the face holds.
// usage (paired video tool token): node docs/videos/pilots/ai-host-lipsync/character/draw-scenes.mjs [id...]
import path from "node:path";
import fs from "node:fs";
const repo = "/home/user/travel_scanner";
const { readCredentials } = await import(`${repo}/tools/video/tts/credentials.mjs`);
const client = await import(`${repo}/tools/video/media/client.mjs`);

const { site, token } = readCredentials();
if (!token) throw new Error("no video tool token; pair first");
const opts = { site, token };
const SLUG = "ai-host-lipsync-pilot";
const HERE = path.dirname(new URL(import.meta.url).pathname);
const OUT = path.join(HERE, "scenes");
const SHEETS = { a: "host-a-trench-r4-s1.png", b: "host-b-smart-r4-s1.png" };

const A = "the same young woman as in the reference image, keep exactly her face, see-through bangs, long wavy chestnut hair, pearl stud earrings, and her outfit: open beige trench coat, black ribbed turtleneck, cream wide-leg trousers, white sneakers, small black top-handle bag";
const B = "the same young man as in the reference image, keep exactly his face, side-swept black hair, and his outfit: open camel wool overcoat, black crewneck sweater, charcoal trousers, dark brown chelsea boots, slim black leather crossbody bag, watch with a black strap";
const STYLE = "Style: photorealistic travel vlog frame, shot on a full-frame camera with a 35mm lens, natural light, true-to-life colour, gentle film grain, shallow depth of field. No text, no readable signs, no logos, no brand names";
const NEGATIVE = "text, letters, readable signs, watermark, logo, brand names, cartoon, anime, 3d render, plastic skin, airbrushed, extra fingers, extra limbs, deformed hands, distorted face, a different face from the reference, celebrity likeness";

const SCENES = {
  "a-closeup": { who: "a", prompt: `Medium close-up, head and shoulders, eye level, of ${A}, looking straight into the camera and talking to the viewer mid-sentence with a warm smile, lips slightly parted, as a travel host presenting. Background: a softly blurred tree-lined city street in late autumn afternoon, warm sunlight from the side` },
  "a-street": { who: "a", prompt: `Medium wide shot of ${A}, walking toward the camera along a narrow old shopping street with small shops and hanging paper lanterns, early evening, she turns her head to the camera and points to something off frame, smiling. Warm shop light mixes with blue dusk light` },
  "a-cafe": { who: "a", prompt: `Medium shot of ${A}, sitting by a large window in a cosy wooden cafe, holding a ceramic cup of latte in both hands, talking to the camera across the table with a bright smile, a slice of cake on a plate in front of her. Soft window daylight from the left` },
  "a-station": { who: "a", prompt: `Medium wide shot of ${A}, standing on a clean railway platform beside a stopped silver commuter train with its doors open, holding a paper ticket, looking at the camera with an excited smile, morning light through the platform roof` },
  "b-closeup": { who: "b", prompt: `Medium close-up, head and shoulders, eye level, of ${B}, looking straight into the camera and talking to the viewer mid-sentence with a confident friendly smile, lips slightly parted, as a travel host presenting. Background: a softly blurred riverside promenade in late autumn afternoon, warm sunlight from the side` },
  "b-street": { who: "b", prompt: `Medium wide shot of ${B}, walking along a lively night market street with food stalls and warm string lights, holding a small paper tray of grilled skewers, turning to the camera with a grin. Warm stall light and evening blue sky` },
  "b-cafe": { who: "b", prompt: `Medium shot of ${B}, sitting at a small marble table in a bright minimalist cafe, a cup of black coffee and a folded paper map on the table, leaning slightly forward and explaining something to the camera, one hand gesturing. Soft daylight from a large window on the right` },
  "b-station": { who: "b", prompt: `Medium wide shot of ${B}, standing in a modern airport departure hall with large glass windows and an aircraft visible outside, one hand on the handle of a dark grey hard-shell suitcase, looking at the camera with a relaxed smile, bright morning daylight` },
  "duo": { who: "ab", prompt: `Medium shot of two travel hosts side by side facing the camera on a scenic hillside viewpoint above a city at golden hour: on the left ${A}; on the right ${B}. Both smiling and talking to the camera like co-hosts, she gestures toward the view behind them. Warm low sunlight from behind, soft rim light on their hair` },
};

const ids = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(SCENES);
fs.mkdirSync(OUT, { recursive: true });
const shaOf = {};
for (const key of Object.keys(SHEETS)) shaOf[key] = (await client.putFile({ slug: SLUG, file: path.join(HERE, SHEETS[key]), ...opts })).sha256;
for (const id of ids) {
  const scene = SCENES[id];
  const references = [...scene.who].map((key) => ({ sha256: shaOf[key], role: "character" }));
  const request = { slug: SLUG, purpose: "keyframe", shot_id: `host-${id}`, aspect: "16:9", prompt: `${scene.prompt}. ${STYLE}`, negative_prompt: NEGATIVE, seed: 1, image_model: "gemini-3-pro-image", references, idempotency_key: `host-scene-${id}-r5` };
  try {
    const job = await client.runJob({ submit: client.submitImage, request, ...opts });
    console.log(id, job.status, "usd", job.usd_estimate, job.error ? JSON.stringify(job.error) : "");
    if (job.status === "ready" && job.file?.sha256) await client.downloadFile({ slug: SLUG, sha256: job.file.sha256, file: path.join(OUT, `${id}.png`), ...opts });
  } catch (e) { console.log(id, "ERROR", e.code ?? "", e.message); }
}
