// First image-to-video test of the AI hosts through the site's clip route (MiniMax H3, 768p).
// usage (paired video tool token): node docs/videos/pilots/ai-host-lipsync/clips/draw-clips.mjs [id...]
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
const SCENES = path.join(HERE, "..", "character", "scenes");

const CLIPS = {
  // Does H3's native audio make her speak a Mandarin line with matching lips?
  "a-closeup-talk": {
    frame: "a-closeup.png", seconds: 8, native_audio: true,
    prompt: "Locked camera, eye-level medium close-up. The young woman looks straight into the lens and speaks to the viewer in Taiwanese Mandarin with a bright, friendly voice, her lips moving clearly with each word: 「大家好，今天帶你們來逛秋天的銀杏大道，真的超級漂亮！」 She smiles, blinks naturally, tilts her head slightly and lifts one hand in a small wave on the last word. Behind her the yellow leaves sway gently and a few drift down. Ambient sound: soft street ambience, light breeze, distant footsteps. No music.",
  },
  // Plain motion: walking, the paper tray, the crowd.
  "b-street-walk": {
    frame: "b-street.png", seconds: 8, native_audio: false,
    prompt: "Slow handheld follow, the camera eases back as the man walks forward toward it through the night market at an easy pace, holding the paper tray of grilled skewers in his right hand. After two steps he raises the tray a little toward the camera and grins, then takes a bite of one skewer and nods happily while chewing. Smoke drifts from the grill on the left, string lights glow, people in the crowd keep moving naturally in the background.",
  },
};

const ids = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(CLIPS);
for (const id of ids) {
  const clip = CLIPS[id];
  const { sha256 } = await client.putFile({ slug: SLUG, file: path.join(SCENES, clip.frame), ...opts });
  const request = { slug: SLUG, shot_id: `host-${id}`, prompt: clip.prompt, first_frame: sha256, seconds: clip.seconds, resolution: "768p", native_audio: clip.native_audio, seed: 1, idempotency_key: `host-clip-${id}-v1` };
  try {
    const job = await client.runJob({ submit: client.submitClip, request, timeoutMs: 40 * 60_000, ...opts });
    console.log(id, job.status, job.model, "usd", job.usd_estimate, job.error ? JSON.stringify(job.error) : "");
    if (job.status === "ready" && job.file?.sha256) {
      fs.mkdirSync(HERE, { recursive: true });
      await client.downloadFile({ slug: SLUG, sha256: job.file.sha256, file: path.join(HERE, `${id}.mp4`), ...opts });
    }
  } catch (e) { console.log(id, "ERROR", e.code ?? "", e.message); }
}
