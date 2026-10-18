// Generates one Lyria cue through the site's media API (about US$0.08) into <out>.
//   node music-zt.mjs <repo root> <slug> <seconds> <out.mp3> <prompt>
import path from "node:path";
import { pathToFileURL } from "node:url";
const [root, slug, seconds, out, prompt] = process.argv.slice(2);
const mod = (p) => import(pathToFileURL(path.join(root, "tools/video", p)).href);
const { readCredentials } = await mod("tts/credentials.mjs");
const { mediaStatus, runJob, submitMusic, downloadFile } = await mod("media/client.mjs");
const { site, token } = readCredentials();
const options = { site, token, fetchImpl: globalThis.fetch };
const status = await mediaStatus(options);
console.log("music", status.music_enabled, status.music?.provider, status.music?.model);
const job = await runJob({ submit: submitMusic, request: { slug, prompt, seconds: Number(seconds), idempotency_key: `${slug}-${path.basename(out)}` }, ...options, timeoutMs: 15 * 60_000 });
console.log(job.status, job.usd_estimate, job.file?.sha256);
if (!job.file?.sha256) { console.log(JSON.stringify(job).slice(0, 600)); process.exit(1); }
await downloadFile({ slug, sha256: job.file.sha256, file: out, ...options });
console.log("saved", out);
