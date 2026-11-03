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
const STYLE = "Style: photorealistic photograph, natural skin texture with fine pores, realistic hair strands, 50mm lens, shallow depth of field, true-to-life colour, looks like a real person photographed for a costume fitting, not a celebrity, not any real person";
const NEGATIVE = "text, letters, watermark, logo, brand names, cartoon, anime, 3d render, plastic skin, airbrushed, heavy makeup, extra fingers, extra limbs, deformed hands, distorted face, different faces between views, celebrity likeness";

export const HOSTS = {
  a: "Character: a Taiwanese woman about 28 years old, friendly warm smile, oval face, natural light makeup, shoulder-length dark brown hair with a soft side part tucked behind one ear, small silver stud earrings; oatmeal knit cardigan over a plain white t-shirt, light-wash straight jeans, white canvas sneakers, small tan leather crossbody bag",
  b: "Character: a Taiwanese man about 32 years old, easygoing grin, short textured black hair, light stubble, thin black rectangular glasses; olive green cotton overshirt open over a heather grey t-shirt, beige chino trousers, brown suede desert boots, a compact camera on a dark strap across the chest",
  c: "Character: an East Asian woman about 33 years old, calm confident expression with a slight smile, black hair in a neat low ponytail with a few loose strands framing the face, straight eyebrows; light blue denim shirt with rolled sleeves, beige wide-leg linen trousers, black leather loafers, natural canvas tote bag on one shoulder",
};

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
    const request = { slug: SLUG, purpose: "character_sheet", aspect: "16:9", prompt: `${SHEET}. ${HOSTS[id]}. ${STYLE}`, negative_prompt: NEGATIVE, seed, image_model: "gemini-3-pro-image", idempotency_key: `host-${id}-s${seed}-v1` };
    try {
      const job = await client.runJob({ submit: client.submitImage, request, ...opts });
      console.log(id, seed, job.status, job.model, "usd", job.usd_estimate, job.error ? JSON.stringify(job.error) : "");
      const sha = job.file?.sha256;
      if (job.status === "ready" && sha) {
        const file = path.join(out, `host-${id}-s${seed}.png`);
        await client.downloadFile({ slug: SLUG, sha256: sha, file, ...opts });
        console.log("saved", file);
      } else console.log(JSON.stringify(job).slice(0, 800));
    } catch (e) { console.log(id, seed, "ERROR", e.code ?? "", e.message); }
  }
}
