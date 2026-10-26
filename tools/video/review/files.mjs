// `review-files`: copy a video's live review attachments from the site back to this machine.
//
// A video made in a cloud container keeps its work directory only as long as the session; once
// that is gone, its approved cut, captions, descriptions, thumbnails and dub tracks live only in
// the site's review store. On 2026-10-26 the approved ollama-phonon-local-speech-language-gap
// needed its channel bookends and nobody held its files, so the API grew a read route for the
// video tool token (GET /api/video/reviews/<slug>/files/<sha256>, apps/api/app/video_reviews/
// tool_files.py). This command lists the video's reviews, keeps the files of the pending and
// approved ones (newest review first, one file per gate and role), downloads each, checks its
// SHA-256 and size against the review, and writes a manifest. The files are what an external-cut
// import (`import --from DIR`, docs/videos/IMPORT.md) or a renewal starts from; this command
// changes nothing on the site.
import { createHash } from "node:crypto";
import { createWriteStream, existsSync, mkdirSync, readFileSync, renameSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { Readable, Transform } from "node:stream";
import { pipeline } from "node:stream/promises";
import { parseArgs } from "node:util";

import { atomicWrite, UsageError } from "../core/paths.mjs";
import { USER_AGENT } from "../tts/client.mjs";
import { readCredentials } from "../tts/credentials.mjs";

const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const SHA256 = /^[0-9a-f]{64}$/;
const ROLE = /^[a-z][A-Za-z0-9_-]{0,39}$/;
const LIVE = new Set(["pending", "approved"]);
// The content types the review store takes (ContentType in apps/api/app/video_reviews/schemas.py).
export const EXTENSIONS = {
  "video/mp4": ".mp4",
  "audio/mp4": ".m4a",
  "audio/mpeg": ".mp3",
  "audio/wav": ".wav",
  "image/png": ".png",
  "image/jpeg": ".jpg",
  "application/x-subrip": ".srt",
  "text/vtt": ".vtt",
  "text/plain": ".txt",
  "application/json": ".json",
};
const ATTEMPTS = 4;

/**
 * The files to fetch: every file of a pending or approved review, newest review first, one per
 * gate and role, at <gate>/<role><ext> under the output directory. A file the site lists twice
 * (a final the publish gate repeats) is fetched once per place it is named, from the same hash.
 */
export function liveFiles(project) {
  const reviews = [...(project?.reviews ?? [])]
    .filter((review) => LIVE.has(review.status))
    .sort((a, b) => String(b.created_at ?? "").localeCompare(String(a.created_at ?? "")));
  const seen = new Set();
  const out = [];
  for (const review of reviews) {
    if (!/^[a-z]+$/.test(String(review.gate))) continue;
    for (const file of review.files ?? []) {
      if (!SHA256.test(String(file.sha256)) || !ROLE.test(String(file.role))) continue;
      const key = `${review.gate}/${file.role}`;
      if (seen.has(key)) continue;
      seen.add(key);
      const ext = EXTENSIONS[file.content_type] ?? ".bin";
      out.push({ gate: review.gate, status: review.status, review_id: review.id, role: file.role, sha256: file.sha256, size: file.size, content_type: file.content_type, file: `${key}${ext}` });
    }
  }
  return out;
}

function sha256Of(file) {
  return createHash("sha256").update(readFileSync(file)).digest("hex");
}

export async function reviewFiles(args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, out: { type: "string" }, gate: { type: "string", multiple: true }, "dry-run": { type: "boolean" } }, strict: true }).values;
  if (!values.slug || !SLUG.test(values.slug)) throw new UsageError("review-files needs --slug with a video's slug");
  if (!values.out && !values["dry-run"]) throw new UsageError("review-files needs --out DIR (or --dry-run to only list the files)");
  const credentials = readCredentials({ env: ctx.env, home: ctx.home });
  if (!credentials.token) {
    ctx.stderr.write("no video tool token yet: run `node tools/video/cli.mjs login`\n");
    return EXIT.owner;
  }
  const fetchImpl = ctx.fetch ?? globalThis.fetch;
  const sleep = ctx.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
  const base = `${credentials.site}/api/video/reviews/${values.slug}`;
  const headers = { Authorization: `Bearer ${credentials.token}`, "User-Agent": USER_AGENT };

  async function get(url, accept) {
    let last;
    for (let attempt = 0; attempt < ATTEMPTS; attempt++) {
      let response;
      try {
        response = await fetchImpl(url, { headers: { ...headers, Accept: accept } });
      } catch (error) {
        last = { status: 0, message: `cannot reach ${credentials.site}: ${error.message}` };
        if (attempt < ATTEMPTS - 1) await sleep(2 ** attempt * 1000);
        continue;
      }
      if (response.ok) return { response };
      const problem = await response.json().catch(() => ({}));
      last = { status: response.status, message: problem.detail || problem.code || `HTTP ${response.status}` };
      if (!(response.status === 429 || response.status >= 500) || attempt === ATTEMPTS - 1) return { error: last };
      await sleep(Math.min(Number(response.headers.get("retry-after")) || 2 ** attempt, 30) * 1000);
    }
    return { error: last };
  }

  const listed = await get(base, "application/json");
  if (listed.error) {
    ctx.stderr.write(`cannot read ${values.slug}: ${listed.error.message}\n`);
    return listed.error.status === 401 || listed.error.status === 403 ? EXIT.owner : listed.error.status === 404 ? EXIT.usage : EXIT.external;
  }
  const project = await listed.response.json();
  let files = liveFiles(project);
  if (values.gate?.length) files = files.filter((file) => values.gate.includes(file.gate));
  if (!files.length) {
    ctx.stderr.write(`${values.slug} has no pending or approved review with files${values.gate?.length ? ` at ${values.gate.join(", ")}` : ""}\n`);
    return EXIT.missing;
  }
  if (values["dry-run"]) {
    for (const file of files) ctx.stdout.write(`${file.file}  ${file.status}  ${file.size} bytes  ${file.sha256}\n`);
    return EXIT.ok;
  }

  const out = path.resolve(values.out);
  const failed = [];
  for (const file of files) {
    const target = path.join(out, file.file);
    if (existsSync(target) && statSync(target).size === file.size && sha256Of(target) === file.sha256) {
      ctx.stdout.write(`kept ${file.file} (already here)\n`);
      continue;
    }
    mkdirSync(path.dirname(target), { recursive: true });
    const partial = `${target}.part`;
    const fetched = await get(`${base}/files/${file.sha256}`, "*/*");
    if (fetched.error) {
      failed.push(`${file.file}: ${fetched.error.message}`);
      continue;
    }
    const hash = createHash("sha256");
    const tap = new Transform({ transform(chunk, _encoding, done) { hash.update(chunk); done(null, chunk); } });
    try {
      await pipeline(Readable.fromWeb(fetched.response.body), tap, createWriteStream(partial));
    } catch (error) {
      rmSync(partial, { force: true });
      failed.push(`${file.file}: the download broke off (${error.message})`);
      continue;
    }
    const digest = hash.digest("hex");
    const size = statSync(partial).size;
    if (digest !== file.sha256 || size !== file.size) {
      rmSync(partial, { force: true });
      failed.push(`${file.file}: got ${size} bytes with SHA-256 ${digest}, the review lists ${file.size} bytes with ${file.sha256}`);
      continue;
    }
    renameSync(partial, target);
    ctx.stdout.write(`got ${file.file} (${size} bytes)\n`);
  }
  atomicWrite(path.join(out, "review-files.json"), `${JSON.stringify({ slug: values.slug, site: credentials.site, fetched_at: new Date().toISOString(), files, not_fetched: failed }, null, 2)}\n`);
  if (failed.length) {
    for (const line of failed) ctx.stderr.write(`not fetched: ${line}\n`);
    return EXIT.external;
  }
  ctx.stdout.write(`${files.length} files in ${out}, listed in review-files.json\n`);
  return EXIT.ok;
}
