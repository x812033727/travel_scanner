// The approved-language contract between review-push's language batch and YouTube sync
// (docs/videos/APPROVED-LANGUAGE-PACKAGE.md). The real `package` and `review-push` run on fixture
// videos against a double of the site that keeps reviews the way the server does; what the site
// then holds (its review rows and stored files) is written to
// apps/api/tests/fixtures/video_language_contract/, which
// apps/api/tests/test_video_youtube_language_contract.py feeds to the real consumer.
// language-contract.test.mjs fails while that copy is not what the producer emits now; write it
// again with `LANGUAGE_CONTRACT_WRITE=1 node --test tools/video/review/language-contract.test.mjs`
// (the fixture videos run seconds, which only the test runner lets through, core/schema.mjs
// minEpisodeMinutes).
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { writeLanguages } from "../core/stages.mjs";
import { dubArtifacts, loadProject } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { dubFingerprint, dubScript, translationHash } from "../dubs/plan.mjs";
import { siteChoice } from "./sync.mjs";

export const CONTRACT_DIR = fileURLToPath(new URL("../../../apps/api/tests/fixtures/video_language_contract", import.meta.url));
export const TOKEN = `mkv_${"l".repeat(43)}`;
export const NOW = new Date("2026-10-01T00:00:00Z");
// The owner's first save of the language panel; it never moves afterwards (LANGUAGES.md).
export const DECIDED_AT = "2026-10-01T01:00:00.000000Z";
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");

/** Review ids are UUIDs on the site, and the consumer compares them as text. */
const uuid = (n) => `00000000-0000-4000-8000-${String(n).padStart(12, "0")}`;
// apps/api/app/video_reviews/admin_service.py languages_need_owner: a batch with a ready dub waits;
// one without is approved on arrival with LANGUAGES_AUTO_APPROVED_NOTE.
const AUTO_APPROVED = "這一批沒有要你上傳的配音，依規則自動核准";
const needsOwner = (payload) => Object.values(payload?.locales ?? {}).some((entry) => entry?.dub === "ready" || entry?.dub?.status === "ready");

/**
 * The site as review-push sees it (apps/api/app/video_reviews/admin_service.py submit_review):
 * rows newest first, a review sent again with the same gate and content answered with the one it
 * has (updated in place only while pending), a new one superseding the gate's pending ones, a
 * language batch without a ready dub approved on arrival, and stored files kept by hash.
 */
export function languageSite({ slug, format = "slides" }) {
  const state = { files: new Map(), reviews: [], project: { slug, format, locales: {}, locales_decided_at: null }, posts: 0, clock: 0 };
  const stamp = () => new Date(NOW.getTime() + ++state.clock * 60_000).toISOString();
  const fetchImpl = async (url, init = {}) => {
    if (!url.startsWith("https://mokaair.com/")) return new Response("", { status: 200 });
    const { pathname, searchParams } = new URL(url);
    if (pathname.startsWith("/api/video/automation/judge/")) return Response.json({ detail: "Not Found" }, { status: 404 });
    const route = pathname.replace("/api/video/reviews/", "");
    if (init.method === "PUT" && route.includes("/files/")) {
      const hash = route.split("/files/")[1];
      const parts = state.files.get(hash)?.parts ?? [];
      parts[Number(searchParams.get("part"))] = Buffer.from(init.body);
      const complete = parts.filter(Boolean).length === Number(searchParams.get("parts"));
      state.files.set(hash, { parts, bytes: complete ? Buffer.concat(parts) : null });
      if (complete && sha(Buffer.concat(parts)) !== hash) return Response.json({ detail: "hash mismatch" }, { status: 422 });
      return Response.json({ received: parts.map((_, index) => index), complete });
    }
    if (init.method === "PUT") return Response.json({ ...JSON.parse(init.body), reviews: [], pending: 0 });
    if (init.method === "POST") {
      state.posts += 1;
      const body = JSON.parse(init.body);
      const missing = body.files.filter((file) => !state.files.get(file.sha256)?.bytes);
      if (missing.length) return Response.json({ code: "video_review_files_missing", detail: "files missing" }, { status: 409 });
      const subject = body.subject ?? null;
      const same = state.reviews.find((row) => row.gate === body.gate && row.subject === subject && row.content_sha256 === body.content_sha256);
      if (same && same.status !== "pending") return Response.json(same, { status: 201 });
      const auto = body.gate === "languages" && !needsOwner(body.payload);
      const decide = (row) => Object.assign(row, auto ? { status: "approved", decided_at: row.created_at, note: AUTO_APPROVED } : {});
      if (same) return Response.json(decide(Object.assign(same, { summary: body.summary, payload: body.payload, files: body.files })), { status: 201 });
      for (const row of state.reviews) if (row.gate === body.gate && row.subject === subject && row.status === "pending") row.status = "superseded";
      const row = { id: uuid(state.reviews.length + 1), gate: body.gate, subject, content_sha256: body.content_sha256, summary: body.summary, payload: body.payload, files: body.files, status: "pending", choice: null, note: null, decided_at: null, created_at: stamp() };
      state.reviews.unshift(decide(row));
      return Response.json(row, { status: 201 });
    }
    return Response.json({ ...state.project, reviews: state.reviews });
  };
  /** A review the tool does not send in these fixtures (a final or screenplay), as the owner decided it. */
  const seed = (gate, content_sha256, payload = {}) => {
    const created_at = stamp();
    state.reviews.unshift({ id: uuid(state.reviews.length + 1), gate, subject: null, content_sha256, summary: gate, payload, files: [], status: "approved", choice: null, note: null, decided_at: created_at, created_at });
    return state.reviews[0];
  };
  const decide = (row, status) => Object.assign(row, { status, decided_at: status === "pending" ? null : stamp() });
  const choose = (locales) => Object.assign(state.project, { locales: siteChoice(locales), locales_decided_at: state.project.locales_decided_at ?? DECIDED_AT });
  return { state, fetchImpl, seed, decide, choose, newest: (gate) => state.reviews.find((row) => row.gate === gate && !row.subject) ?? null };
}

export function toolContext(box, fetchImpl) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
      home: box.base,
      fetch: fetchImpl,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => NOW,
      sleep: async () => {},
    },
  };
}

/** Each language's title, description, tags and lines, as i18n-merge writes them. */
function writeTranslations(box, doc, locales) {
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  for (const locale of locales) {
    const lines = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, { text: `${locale} ${line.id}`, source_hash: textHash(line.text) }]));
    const translation = { title: `${locale} title of ${doc.slug}`, description: `${locale} description of ${doc.slug}.`, tags: [`${locale} tag`], lines };
    writeFileSync(path.join(box.dir, "i18n", `${locale}.json`), `${JSON.stringify(translation, null, 2)}\n`);
  }
}

/**
 * A fixture video cut, checked and approved, its translations merged: `package` writes its
 * upload package from here, and review-push sends it. `name` is a core fixture (minimal is
 * narrated in zh-TW, en in English).
 */
export async function languageVideo({ name = "minimal", slug = name === "en" ? "fixture-en" : "fixture-minimal", translated = ["en", "ja", "ko"] } = {}) {
  const box = sandbox(slug, name);
  mkdirSync(box.workdir, { recursive: true });
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const lexicon = JSON.parse(readFileSync(path.join(box.videos, "lexicon.json"), "utf8"));
  writeTranslations(box, doc, translated);
  const timeline = writeSyntheticNarration(doc, lexicon, box.workdir);
  writeFileSync(path.join(box.workdir, "final.mp4"), Buffer.from(`the finished cut of ${slug}`));
  writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify({ ok: true, speech_hash: speechHash(doc, lexicon), narration_sha256: timeline.audio_evidence.narration_sha256, visual_hash: visualHash(doc), problems: [] }));
  writeFileSync(path.join(box.workdir, "thumbnail.jpg"), Buffer.from(`thumbnail of ${slug}`));
  mkdirSync(path.join(box.workdir, "frames"), { recursive: true });
  writeFileSync(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visualHash(doc), thumbnail: "thumbnail.jpg" }));
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir, now: NOW });
  return { ...box, doc };
}

/** The tool command, failing loudly: a fixture that cannot be built is not a contract. */
export async function tool(box, site, args) {
  const run = toolContext(box, site.fetchImpl);
  const code = await main(args, run.ctx);
  if (code !== EXIT.ok) throw new Error(`${args.join(" ")} exited ${code}: ${run.out.stderr}${run.out.stdout}`);
  return run.out;
}

/**
 * A dub track the dub command made for `locale` (dubs/<locale>/ and dubs/<locale>.<format>): each
 * line a few frames after the narration's, at its words' and voice's current hashes.
 */
function writeDub(box, locale, format) {
  const project = loadProject({ slug: box.slug, root: box.root });
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  const files = dubArtifacts(box.workdir, locale);
  const lines = timeline.lines.map((line) => ({ id: line.id, start_frame: line.start_frame + 5, end_frame: line.start_frame + 5 + Math.ceil(line.audio_samples / 2 / 1600), audio_samples: Math.floor(line.audio_samples / 2), tempo: 1 }));
  const words = translationHash(dubScript(project.doc, project.translations[locale], locale).doc);
  const dub = { locale, format, file: `${locale}.${format}`, speech_hash: timeline.speech_hash, translation_hash: words, speech_fingerprint: dubFingerprint(project, locale), total_frames: timeline.total_frames, tempo_max: 1.05, windows: [], lines };
  mkdirSync(files.dir, { recursive: true });
  writeFileSync(files.timeline, JSON.stringify(dub));
  writeFileSync(files.track(format), `the ${locale} dub of ${box.slug}, as ${format}`);
}

/**
 * A video whose upload confirmation the owner approved before choosing languages (the package
 * then carried zh-TW only), and the owner's choice: the worker writes the package again with
 * the chosen languages and sends their batch, as automation/flow.mjs languages() does. A dub is
 * either given up (`skippedDubs`, with its reason) or made (`readyDubs`, in its format).
 */
export async function confirmedVideo({ name, chosen, skippedDubs = {}, readyDubs = {}, translated } = {}) {
  const box = await languageVideo({ name, translated });
  const site = languageSite({ slug: box.slug, format: box.doc.format ?? "slides" });
  site.seed("final", sha(readFileSync(path.join(box.workdir, "final.mp4"))));
  writeLanguages(box.workdir, { locales: {}, decided_at: DECIDED_AT });
  site.choose({});
  await tool(box, site, ["package", "--slug", box.slug]);
  await tool(box, site, ["review-push", "--slug", box.slug, "--gate", "publish"]);
  site.decide(site.newest("publish"), "approved");
  for (const [locale, reason] of Object.entries(skippedDubs)) {
    mkdirSync(path.join(box.workdir, "dubs", locale), { recursive: true });
    writeFileSync(path.join(box.workdir, "dubs", locale, "skipped.json"), JSON.stringify({ reason }));
  }
  for (const [locale, format] of Object.entries(readyDubs)) writeDub(box, locale, format);
  writeLanguages(box.workdir, { locales: chosen, decided_at: DECIDED_AT });
  site.choose(chosen);
  await tool(box, site, ["package", "--slug", box.slug]);
  return { box, site };
}

// The cases the Python consumer reads: a zh-TW video with one language's title and description
// alone, one's captions alone, and one with a skipped dub; one with a dub track (mp3, the owner
// approving the batch once it is up in Studio); and an English-narrated one whose own language is
// chosen as well (its title, captions and dub are the video's own).
export const CONTRACT_CASES = {
  "zh-tw-narration": { name: "minimal", chosen: { en: { metadata: true, captions: true }, ja: { captions: true }, ko: { metadata: true, dub: true } }, skippedDubs: { ko: "配音字數超出時間軸，改用字幕" } },
  "zh-tw-dubbed": { name: "minimal", chosen: { ja: { captions: true, dub: true } }, readyDubs: { ja: "mp3" } },
  "en-narration": { name: "en", chosen: { en: { metadata: true, captions: true, dub: true }, ja: { metadata: true, captions: true } }, translated: ["zh-TW", "ja", "ko"] },
};

/** One case as the site holds it after the batch: the project, its review rows and every stored file. */
export async function emitCase(spec) {
  const { box, site } = await confirmedVideo(spec);
  try {
    await tool(box, site, ["review-push", "--slug", box.slug, "--gate", "languages"]);
    // A batch with a dub track waits for the owner, who approves it once the track is up in Studio.
    const batch = site.newest("languages");
    if (batch.status === "pending") site.decide(batch, "approved");
    const files = new Map([...site.state.files].filter(([, file]) => file.bytes).map(([hash, file]) => [hash, file.bytes]).sort(([a], [b]) => (a < b ? -1 : 1)));
    const record = { project: site.state.project, reviews: site.state.reviews };
    const text = `${JSON.stringify(record, null, 2)}\n`;
    for (const value of [text, ...[...files.values()].map((bytes) => bytes.toString("latin1"))]) {
      if (value.includes(box.base)) throw new Error("a sandbox path reached the contract fixture; it would not be the same on another machine");
    }
    return { record: text, files };
  } finally {
    rmSync(box.base, { recursive: true, force: true });
  }
}

export async function emitContract() {
  const cases = {};
  for (const [name, spec] of Object.entries(CONTRACT_CASES)) cases[name] = await emitCase(spec);
  return cases;
}

// The committed copy: <case>/case.json and <case>/files/<sha256>, beside the .gitattributes that
// keeps git from normalising a hash-named file.
const caseDirs = (dir) => (existsSync(dir) ? readdirSync(dir, { withFileTypes: true }).filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort() : []);

export function readContract(dir = CONTRACT_DIR) {
  return Object.fromEntries(caseDirs(dir).map((name) => {
    const filesDir = path.join(dir, name, "files");
    const files = new Map(readdirSync(filesDir).sort().map((hash) => [hash, readFileSync(path.join(filesDir, hash))]));
    return [name, { record: readFileSync(path.join(dir, name, "case.json"), "utf8"), files }];
  }));
}

export function writeContract(cases, dir = CONTRACT_DIR) {
  for (const name of caseDirs(dir)) rmSync(path.join(dir, name), { recursive: true, force: true });
  for (const [name, { record, files }] of Object.entries(cases)) {
    mkdirSync(path.join(dir, name, "files"), { recursive: true });
    writeFileSync(path.join(dir, name, "case.json"), record);
    for (const [hash, bytes] of files) writeFileSync(path.join(dir, name, "files", hash), bytes);
  }
}
