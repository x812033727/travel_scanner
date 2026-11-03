// Draw character sheets for the AI host pilot through the site's media API.
// usage (paired video tool token): node docs/videos/pilots/ai-host-lipsync/character/draw-sheets.mjs status | node host-sheets.mjs draw <outDir> [id...]
import path from "node:path";
import fs from "node:fs";
const repo = "/home/user/travel_scanner";
const { readCredentials } = await import(`${repo}/tools/video/tts/credentials.mjs`);
const client = await import(`${repo}/tools/video/media/client.mjs`);

const { site, token } = readCredentials();
if (!token) throw new Error("no video tool token; pair first");
const opts = { site, token };
const SLUG = "ai-host-lipsync-pilot";

const SHEET = "character design sheet of one original fictional person: front view head-and-shoulders portrait on the left, three-quarter view in the middle, full body standing on the right, side by side, the same person and outfit in all three, neutral relaxed pose, plain light grey seamless studio background, even soft studio lighting, no text, no logo";
const STYLE = (process.env.ROUND === "3" ? "Lighting: flattering soft beauty lighting with a large softbox key light and gentle fill, subtle rim light separating hair from the background, magazine-quality fashion photo. " : "") + "Style: photorealistic photograph, natural skin texture with fine pores, realistic hair strands, 50mm lens, shallow depth of field, true-to-life colour, looks like a real person photographed for a costume fitting, an original face that is not a celebrity and not any real person";
const NEGATIVE = "text, letters, watermark, logo, brand names, cartoon, anime, 3d render, plastic skin, airbrushed, heavy makeup, extra fingers, extra limbs, deformed hands, distorted face, different faces between views, celebrity likeness";

const ROUND = process.env.ROUND ?? "1";
const HOSTS_BY_ROUND = {
  "1": {
    a: "Character: a Taiwanese woman about 28 years old, friendly warm smile, oval face, natural light makeup, shoulder-length dark brown hair with a soft side part tucked behind one ear, small silver stud earrings; oatmeal knit cardigan over a plain white t-shirt, light-wash straight jeans, white canvas sneakers, small tan leather crossbody bag",
    b: "Character: a Taiwanese man about 32 years old, easygoing grin, short textured black hair, light stubble, thin black rectangular glasses; olive green cotton overshirt open over a heather grey t-shirt, beige chino trousers, brown suede desert boots, a compact camera on a dark strap across the chest",
    c: "Character: an East Asian woman about 33 years old, calm confident expression with a slight smile, black hair in a neat low ponytail with a few loose strands framing the face, straight eyebrows; light blue denim shirt with rolled sleeves, beige wide-leg linen trousers, black leather loafers, natural canvas tote bag on one shoulder",
  },
  // Round 2 (owner 2026-11-03): the women prettier, the man more handsome; fix the round-one notes.
  "2": {
    a: "Character: a strikingly pretty, photogenic Taiwanese woman about 26 years old, the look of a popular lifestyle TV travel presenter; delicate V-shaped face, large bright double-lidded eyes, softly arched brows, small refined nose, full natural rosy lips, clear luminous skin, radiant sweet smile showing a little teeth; glossy shoulder-length dark brown hair with soft waves and a side part, the left side tucked behind the ear in every view; small silver stud earrings, fresh natural makeup; slim figure; oatmeal knit cardigan over a plain white t-shirt, light-wash straight jeans, white canvas sneakers, small tan leather crossbody bag whose strap runs from her right shoulder to her left hip in every view",
    b: "Character: a very handsome, photogenic Taiwanese man about 29 years old, the look of a popular lifestyle TV travel presenter; well-defined jawline and cheekbones, straight nose, warm expressive eyes with thick dark brows, clear healthy skin, neat light stubble, charming confident smile; stylish short black hair with textured volume swept up at the front, faded sides; thin black rectangular glasses; tall athletic build with broad shoulders; olive green cotton overshirt open over a heather grey t-shirt, slim beige chino trousers, brown suede desert boots, a plain matte black mirrorless camera with no logo, no lettering and no red dot on a black strap across the chest",
    c: "Character: an elegant, beautiful East Asian woman about 30 years old, the look of a popular lifestyle TV travel presenter; graceful oval face, bright almond eyes, softly defined cheekbones, natural rosy lips, smooth glowing skin, friendly warm open smile; glossy black hair in a sleek low ponytail with a few soft face-framing strands, straight natural brows, tasteful light makeup, small gold hoop earrings; slender figure; light blue denim shirt with rolled sleeves, beige wide-leg linen trousers, black leather loafers, natural canvas tote bag on one shoulder",
  },
  // Round 3: round two still read as plain; drama-lead styling and beauty light, two seeds each.
  "3": {
    a: "Character: a gorgeous young Taiwanese woman about 25 years old who looks like the female lead of a Taiwanese idol drama; small V-shaped face, big sparkling double-lidded eyes with long lashes, softly arched brows, small high-bridged nose, plump rosy lips, flawless dewy porcelain skin, sweet dazzling smile; glossy long dark chestnut hair past the shoulders in soft salon-styled waves with airy see-through bangs; professional soft glam makeup with rosy blush and glossy lips; small pearl stud earrings; slender figure, good posture; cream fitted knit cardigan over a white t-shirt, light-wash high-waisted straight jeans, white sneakers, small tan leather crossbody bag",
    b: "Character: a strikingly handsome Taiwanese man about 28 years old who looks like the male lead of a Taiwanese idol drama; sharp V-shaped jawline, high cheekbones, straight high-bridged nose, deep warm eyes with thick dark brows, clean smooth skin, clean-shaven, charming boyish smile; salon-styled black hair with a soft comma-shaped fringe swept to one side, tapered sides; no glasses; tall slim athletic build, broad shoulders; olive green cotton overshirt open over a white t-shirt, slim beige chino trousers, brown suede desert boots, a plain matte black mirrorless camera with no logo, no lettering and no red dot on a black strap across the chest",
    c: "Character: a stunningly beautiful elegant East Asian woman about 28 years old who looks like the lead actress of a romantic drama; refined oval face, bright almond eyes with long lashes, high cheekbones, small straight nose, soft full lips, luminous flawless skin, warm radiant smile; glossy black hair in a sleek low ponytail with soft face-framing curtain strands; polished natural makeup with soft rose lips; small gold hoop earrings; tall slender model figure; light blue denim shirt with rolled sleeves tucked into beige wide-leg linen trousers, black leather loafers, natural canvas tote bag on her right shoulder in every view",
  },
};
export const HOSTS = HOSTS_BY_ROUND[ROUND];

const cmd = process.argv[2];
if (cmd === "status") {
  const s = await client.mediaStatus(opts);
  console.log(JSON.stringify(s, null, 2).slice(0, 6000));
} else if (cmd === "draw") {
  const out = process.argv[3];
  const ids = process.argv.slice(4).length ? process.argv.slice(4) : Object.keys(HOSTS);
  const seeds = (process.env.SEEDS ?? "1").split(",").map(Number);
  fs.mkdirSync(out, { recursive: true });
  for (const id of ids) for (const seed of seeds) {
    const request = { slug: SLUG, purpose: "character_sheet", aspect: "16:9", prompt: `${SHEET}. ${HOSTS[id]}. ${STYLE}`, negative_prompt: NEGATIVE, seed, image_model: "gemini-3-pro-image", idempotency_key: `host-${id}-s${seed}-r${ROUND}` };
    try {
      const job = await client.runJob({ submit: client.submitImage, request, ...opts });
      console.log(id, seed, job.status, job.model, "usd", job.usd_estimate, job.error ? JSON.stringify(job.error) : "");
      const sha = job.file?.sha256;
      if (job.status === "ready" && sha) {
        const file = path.join(out, `host-${id}${ROUND === "1" ? "" : `-r${ROUND}`}-s${seed}.png`);
        await client.downloadFile({ slug: SLUG, sha256: sha, file, ...opts });
        console.log("saved", file);
      } else console.log(JSON.stringify(job).slice(0, 800));
    } catch (e) { console.log(id, seed, "ERROR", e.code ?? "", e.message); }
  }
}
