// Owner-initiated replacement of an approved long cut. Staging never reports or submits a
// review; the owner imports its receipt on /admin/videos or deliberately runs `submit`.
import { createHash } from "node:crypto";
import { closeSync, copyFileSync, existsSync, mkdirSync, openSync, readFileSync, readSync, realpathSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { sha256File } from "../core/approvals.mjs";
import { appliedBranding, brandingCurrent, presentationTimeline, readBranding, validateBranding } from "../core/branding.mjs";
import { toSrt } from "../core/captions.mjs";
import { isCompilation } from "../core/compilation.mjs";
import { atomicWrite, isInside, readJson, UsageError } from "../core/paths.mjs";
import { LOCALES as VIDEO_LOCALES, NARRATION_LOCALE, narrationLocale } from "../core/schema.mjs";
import { captionLocalesOf, currentDub, dubLocalesOf, dubRole, dubsForUpload, localeCues, localeTexts, metadataLocalesOf, readLanguages } from "../core/stages.mjs";
import { speechHash, FPS } from "../core/timeline.mjs";
import { composeMetadata } from "../package/metadata.mjs";

const HASH = /^[a-f0-9]{64}$/;
const UUID = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;
const LOCALES = VIDEO_LOCALES.filter((locale) => locale !== NARRATION_LOCALE);
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const requireThat = (condition, message) => { if (!condition) throw new UsageError(message); };
const identity = (row) => ({ review_id: row.id, content_sha256: row.content_sha256 });
const latest = (rows, gate) => rows.find((row) => row.gate === gate && !row.subject);
const choices = (locales) => Object.fromEntries(LOCALES.map((locale) => {
  const entry = locales?.[locale] ?? {};
  return [locale, { metadata: entry.metadata === true, captions: entry.captions === true || entry.dub === true, dub: entry.dub === true }];
}));

/** Long finals are hashed as streams and sent in bounded parts, never buffered whole. */
export async function uploadCandidate(client, slug, file, role) {
  const sha256 = await sha256File(file), size = statSync(file).size;
  const partBytes = 4 * 1024 * 1024, parts = Math.ceil(size / partBytes);
  requireThat(size > 0, "empty candidate attachment");
  const handle = openSync(file, "r");
  let complete = false;
  try {
    for (let part = 0; part < parts; part++) {
      const bytes = Buffer.alloc(Math.min(partBytes, size - part * partBytes));
      requireThat(readSync(handle, bytes, 0, bytes.length, part * partBytes) === bytes.length, "attachment changed during staging");
      const result = await client.part(slug, sha256, bytes, { part: String(part), parts: String(parts), size: String(size) });
      if (result.complete === true) { complete = true; break; }
    }
  } finally { closeSync(handle); }
  requireThat(complete && await sha256File(file) === sha256, "attachment upload was incomplete or its source changed; no receipt created");
  const types = { ".mp4": "video/mp4", ".json": "application/json", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".srt": "application/x-subrip" };
  return { role, sha256, size, content_type: types[path.extname(file)] ?? "text/plain" };
}

/** The server's rows are newest first; a newer pending/rejected review must never be skipped. */
export function renewedFinal(remote) {
  const final = latest(remote?.reviews ?? [], "final");
  return final?.payload?._final_renewal ? final : null;
}

function origin(value) {
  const url = new URL(value);
  requireThat(!url.username && !url.password && !url.search && !url.hash && ["", "/"].includes(url.pathname), "site must be an origin without credentials, path, query or fragment");
  requireThat(url.protocol === "https:" || (url.protocol === "http:" && ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname)), "owner credentials require HTTPS (or loopback HTTP)");
  return url.origin;
}

/** No retry, no redirects and no stored/logged credentials for consequential owner writes. */
export function ownerClient({ site = "https://mokaair.com", session, fetch: fetchImpl = globalThis.fetch } = {}) {
  const base = origin(site);
  requireThat(typeof session === "string" && session.length > 0 && !/[;\s\r\n]/.test(session), "set MOKAAIR_OWNER_SESSION to the owner's current session; prefer the website receipt control");
  return async (method, slug, body) => {
    requireThat(/^[a-z0-9][a-z0-9-]{0,79}$/.test(slug), "invalid video slug");
    const response = await fetchImpl(`${base}/api/travel/admin/videos/${slug}/final-renewal`, {
      method, redirect: "error", headers: { Cookie: `travel_access=${session}`, Origin: base, "Content-Type": "application/json" },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
    const data = await response.json();
    requireThat(response.ok, `renewal refused (${response.status}, ${data.code ?? "unknown"}); reload the owner page before another attempt`);
    return data;
  };
}

export function validateCandidate(receipt, slug, site) {
  requireThat(receipt?.schema_version === 1 && receipt.kind === "long-final-renewal" && receipt.slug === slug, "not a renewal receipt for this video");
  requireThat(origin(receipt.site) === origin(site), "the candidate was staged on another site");
  const review = receipt.review;
  requireThat(review?.gate === "final" && !review.subject && HASH.test(review.content_sha256 ?? "") && !review.payload?._final_renewal, "invalid candidate review");
  requireThat(HASH.test(receipt.source?.final_sha256 ?? "") && UUID.test(receipt.source.final_review_id ?? "") && HASH.test(receipt.source.body_sha256 ?? ""), "missing original cut or retained-body identity");
  requireThat(HASH.test(receipt.candidate?.branding_hash ?? "") && review.payload?.branding_hash === receipt.candidate.branding_hash && receipt.candidate.final_sha256 === review.content_sha256, "candidate branding/final identity differs");
  requireThat(review.content_sha256 !== receipt.source.final_sha256, "the candidate is the original cut");
  requireThat(Array.isArray(review.files) && review.files.length > 0 && review.files.length <= 48, "invalid candidate files");
  requireThat(new Set(review.files.map((file) => file.role)).size === review.files.length, "duplicate candidate file roles");
  for (const file of review.files) requireThat(HASH.test(file.sha256 ?? "") && Number.isSafeInteger(file.size) && file.size > 0, "invalid candidate file proof");
  requireThat(review.files.some((file) => file.role === "preview" && file.content_type === "video/mp4") && review.files.some((file) => file.role === "final" && file.content_type === "video/mp4" && file.sha256 === review.content_sha256 && file.size === receipt.candidate.final_bytes), "candidate needs its actual final and preview attachments");
  return receipt;
}

/** The candidate can be old, but its original final cannot have changed in the meantime. */
export async function submitRenewal({ receipt, reason, request, site }) {
  validateCandidate(receipt, receipt.slug, site);
  requireThat(typeof reason === "string" && reason.trim().length > 0 && reason.length <= 2000, "a renewal reason is required (at most 2000 characters)");
  const state = await request("GET", receipt.slug);
  requireThat(state.final_review_id === receipt.source.final_review_id && state.final_sha256 === receipt.source.final_sha256 && HASH.test(state.version ?? ""), "the original final changed; stage a new candidate against the current owner state");
  const result = await request("POST", receipt.slug, {
    expected_version: state.version, expected_final_review_id: state.final_review_id,
    expected_final_sha256: state.final_sha256, reason: reason.trim(), review: receipt.review,
  });
  requireThat(result.status === "pending" && result.payload?.manual_review === true && result.content_sha256 === receipt.review.content_sha256, "unexpected renewal result; inspect the owner page, do not retry");
  const persisted = await request("GET", receipt.slug);
  requireThat(persisted.final_review_id === result.id && persisted.final_sha256 === result.content_sha256, "renewal not confirmed by read-back; inspect the owner page, do not retry");
  return result;
}

/** Snapshot only into a new directory. No approval, pin, package or canonical file is changed. */
export async function stageRenewal({ from, out, original, body, branding, client, measure, encode, upload, env = process.env }) {
  const sourceDir = realpathSync(from);
  const destination = path.resolve(out);
  requireThat(!existsSync(destination) && !isInside(destination, sourceDir), "out must be a new directory outside the candidate source");
  const { readMeta, finalReview, measureCut, measureProblems, encodePreview } = await import("../import/import.mjs");
  const { siteClient } = await import("../shorts/site.mjs");
  const site = client ?? siteClient({ env, attempts: 1 });
  const inspect = measure ?? measureCut;
  const send = upload ?? uploadCandidate;
  const meta = readMeta(readJson(path.join(sourceDir, "meta.json"), null));
  const remote = await site.project(meta.slug);
  const old = latest(remote?.reviews ?? [], "final");
  requireThat(old && (old.status === "approved" || old.payload?._final_renewal), "no approved original final or active owner renewal");
  requireThat(!remote.youtube_video_id && !remote.youtube_sync && !remote.youtube_publish_at && !remote.youtube_removed_at && !remote.dropped_at && !remote.shorts_line && remote.format !== "shorts", "uploaded, scheduled, withdrawn or short videos cannot be staged for long renewal");
  const oldSha = await sha256File(original);
  requireThat(oldSha === old.content_sha256, "original file does not match the site's current final review");
  const bodySha = await sha256File(body);
  const pin = validateBranding(readJson(branding, null), { base: path.dirname(path.resolve(branding)) });
  requireThat(pin, "a branding package is required");
  for (const role of ["intro", "outro"]) requireThat(await sha256File(pin[role].file) === pin[role].sha256, `${role} bytes do not match the branding pin`);
  const final = path.join(sourceDir, "final.mp4");
  const finalSha = await sha256File(final);
  requireThat(finalSha !== oldSha, "candidate must contain a new cut");
  const bodyMeasurement = measureProblems(...await inspectArgs(inspect, body, env));
  const candidateMeasurement = measureProblems(...await inspectArgs(inspect, final, env));
  const expectedSeconds = bodyMeasurement.seconds + (pin.intro.frames + pin.outro.frames) / FPS;
  requireThat(bodyMeasurement.seconds > 0 && Math.abs(candidateMeasurement.seconds - expectedSeconds) <= 0.1, "candidate duration does not match retained body plus the new bookends");
  mkdirSync(destination, { recursive: true });
  const snapshot = path.join(destination, "final.mp4");
  copyFileSync(final, snapshot);
  requireThat(await sha256File(snapshot) === finalSha && await sha256File(original) === oldSha && await sha256File(body) === bodySha, "source changed during staging");
  const preview = path.join(destination, "preview.mp4");
  await (encode ?? encodePreview)(snapshot, preview, env);
  const files = [await send(site, meta.slug, snapshot, "final"), await send(site, meta.slug, preview, "preview")];
  const thumbnail = ["thumbnail.png", "thumbnail.jpg", "thumbnail.jpeg"].find((name) => existsSync(path.join(sourceDir, name)));
  for (const [name, role] of [...(thumbnail ? [[thumbnail, "thumbnail"]] : []), ["zh-TW.srt", "captions_zh-TW"]]) {
    const source = path.join(sourceDir, name);
    if (!existsSync(source)) continue;
    const target = path.join(destination, name);
    copyFileSync(source, target);
    files.push(await send(site, meta.slug, target, role));
  }
  const source = { final_review_id: old.id, final_sha256: oldSha, body_sha256: bodySha };
  const candidate = { final_sha256: finalSha, branding_hash: pin.hash, final_bytes: statSync(snapshot).size };
  const review = finalReview({ meta, sha256: finalSha, ...candidateMeasurement, captions: files.some((file) => file.role === "captions_zh-TW") });
  review.payload = { ...review.payload, manual_review: true, branding_hash: pin.hash, renewal_candidate: { source, candidate, body_seconds: bodyMeasurement.seconds, intro_frames: pin.intro.frames, outro_frames: pin.outro.frames } };
  const receipt = { schema_version: 1, kind: "long-final-renewal", site: origin(site.site), slug: meta.slug, source, candidate, review: { ...review, files } };
  validateCandidate(receipt, meta.slug, site.site);
  atomicWrite(path.join(destination, "renewal-candidate.json"), `${JSON.stringify(receipt, null, 2)}\n`);
  return receipt;
}

async function inspectArgs(inspect, file, env) { const result = await inspect(file, env); return [result.probe, result.loudness]; }

/** A renewal id is not enough: bind it only after verifying the current local package bytes. */
export async function bindRenewalSubmission({ body, remote, project, workdir, request, upload }) {
  const final = renewedFinal(remote);
  if (!final || !["publish", "languages", "dubs"].includes(body.gate)) return body;
  if (readJson(path.join(workdir, "renewal-handoff.json"), null)?.mode === "manual-import") {
    const { bindManualSubmission, bindManualLanguageSubmission } = await import("./renewal-handoff.mjs");
    return body.gate === "publish" ? bindManualSubmission({ body, remote, workdir }) : bindManualLanguageSubmission({ body, remote, workdir, project, request, upload });
  }
  requireThat(final.status === "approved", "the renewed final still needs the owner's review");
  requireThat(!isCompilation(project.doc), "renewed compilation packages need an episode-source handoff; keep this project held for the owner");
  const metadataFile = path.join(workdir, "upload", "metadata.json");
  const metadataBytes = readFileSync(metadataFile);
  const metadata = JSON.parse(metadataBytes);
  const finalFile = path.join(workdir, "upload", "final.mp4");
  const checks = readJson(path.join(workdir, "checks.json"), null);
  const applied = appliedBranding(checks);
  const timeline = readJson(path.join(workdir, "timeline.json"), null);
  const brand = final.payload.branding_hash ?? null;
  requireThat(await sha256File(finalFile) === final.content_sha256 && metadata.final_sha256 === final.content_sha256, "upload package still contains another final cut");
  requireThat(brandingCurrent(checks, readBranding(workdir)) && (applied?.hash ?? null) === brand && (metadata.branding_hash ?? null) === brand, "upload package still contains another branding version");
  requireThat(timeline && (!applied || applied.body_frames === timeline.total_frames), "upload package has another body timeline");
  requireThat(isCompilation(project.doc) ? timeline.compilation_hash && checks.compilation_hash === timeline.compilation_hash : timeline.speech_hash === speechHash(project.doc, project.lexicon) && checks.speech_hash === timeline.speech_hash, "the final was built for another script/timeline");
  const { checksCurrent } = await import("../package/cli.mjs");
  requireThat(checksCurrent(project.doc, project.lexicon, checks, readJson(path.join(workdir, "clips", "manifest.json"), null), readJson(path.join(workdir, "keyframes", "manifest.json"), null)), "the renewed package has stale visual/audio checks");
  const languages = readLanguages(workdir);
  requireThat(languages && JSON.stringify(choices(languages.locales)) === JSON.stringify(choices(remote.locales)) && JSON.stringify(choices(metadata.language_choice)) === JSON.stringify(choices(remote.locales)), "language choice changed; rebuild the package");
  const selected = Object.fromEntries(Object.entries(choices(languages.locales)).filter(([, choice]) => choice.metadata || choice.captions || choice.dub));
  requireThat(Object.keys(metadata.language_choice ?? {}).length === Object.keys(selected).length && Object.keys(selected).every((locale) => Object.keys(metadata.language_choice[locale]).length === 3 && Object.entries(selected[locale]).every(([part, value]) => metadata.language_choice[locale][part] === value)), "metadata language choice is not the current compact choice; rebuild the package");
  const presented = presentationTimeline(timeline, applied);
  const narration = narrationLocale(project.doc);
  const wantedDubs = dubLocalesOf(languages, project.doc);
  const expectedMetadata = composeMetadata({ ...project, timeline: presented, locales: metadataLocalesOf(languages, narration) });
  requireThat(expectedMetadata.problems.length === 0 && JSON.stringify(metadata.chapters) === JSON.stringify(expectedMetadata.metadata.chapters) && metadata.description === expectedMetadata.metadata.description && JSON.stringify(metadata.localizations) === JSON.stringify(expectedMetadata.metadata.localizations), "the package description/chapters still use another presentation timeline");
  const { texts, skipped } = localeTexts(project.doc, project.translations);
  const defaultLocale = expectedMetadata.metadata.default_language;
  requireThat(metadata.default_language === defaultLocale && texts[defaultLocale], "the package changed the narration language");
  const defaultCaption = toSrt(localeCues(presented, texts, defaultLocale, narration).cues);
  requireThat(readFileSync(path.join(workdir, "upload", "captions", `${defaultLocale}.srt`), "utf8") === defaultCaption, "the narration captions still use another presentation timeline");
  const captionManifest = readJson(path.join(workdir, "captions", "manifest.json"), null);
  const expectedCaptions = { [defaultLocale]: defaultCaption };
  for (const locale of captionLocalesOf(languages, narration).filter((locale) => locale !== defaultLocale)) {
    requireThat(captionManifest?.speech_hash === timeline.speech_hash && (captionManifest.branding_hash ?? null) === brand && texts[locale] && !skipped[locale]?.length, `${locale} captions need regeneration for this timeline`);
    const dub = wantedDubs.includes(locale) ? currentDub(project, workdir, locale, timeline.speech_hash) : null;
    requireThat(!dub?.stale, `${locale} dub is stale`);
    // As runCaptions cut them: a translation under the narration moves its cue changes onto the
    // narration's measured ones.
    expectedCaptions[locale] = toSrt(localeCues(presented, texts, locale, narration, dub).cues);
    requireThat(readFileSync(path.join(workdir, "upload", "captions", `${locale}.srt`), "utf8") === expectedCaptions[locale], `${locale} caption bytes have stale offsets or text`);
  }
  const payload = { ...body.payload, ...(body.gate !== "publish" ? { locales: structuredClone(body.payload.locales ?? {}) } : {}), final_review_id: final.id };
  if (body.gate === "publish") {
    requireThat(body.files.some((file) => file.role === "metadata" && file.sha256 === hash(metadataBytes)) && body.content_sha256 === hash(metadataBytes) && body.payload.package?.ok === true, "publish proof no longer matches the package");
    for (const [locale, expected] of Object.entries(expectedCaptions)) requireThat(body.files.some((file) => file.role === `captions_${locale}` && file.sha256 === hash(expected)), `${locale} published caption attachment is stale`);
  }
  const rows = remote.reviews ?? [];
  const publish = latest(rows, "publish");
  requireThat(body.gate === "publish" || publish?.status === "approved", "the renewed publish package must be approved before its languages");
  const script = project.doc.format === "drama" && !isCompilation(project.doc) ? latest(rows, "script") : null;
  requireThat(!script || script.status === "approved", "the source screenplay is not approved");
  requireThat(project.doc.format !== "drama" || isCompilation(project.doc) || script, "the source screenplay review is missing");
  const files = [...body.files];
  for (const [locale, choice] of Object.entries(languages.locales)) {
    const entry = payload.locales?.[locale] ?? {};
    if (choice.dub && locale === narration) {
      requireThat(!files.some((file) => file.role === dubRole(locale)), "the narration's original audio must not be submitted as a duplicate dub");
      if (body.gate !== "publish") {
        const skipped = { status: "skipped", reason: "This language is the original narration; no duplicate dub is generated." };
        payload.locales[locale] = body.gate === "dubs" ? skipped : { ...entry, dub: skipped };
      }
    }
    if (body.gate === "dubs") {
      if (!wantedDubs.includes(locale)) continue;
      const current = currentDub(project, workdir, locale, timeline.speech_hash);
      requireThat(entry.status === "skipped" && typeof entry.reason === "string" && entry.reason.trim() || entry.status === "ready" && current && !current.stale && (current.branding_hash ?? null) === brand && await sha256File(current.file) === entry.sha256 && files.some((file) => file.role === entry.file_role && file.sha256 === entry.sha256), `${locale} dub needs regeneration for the renewed final`);
      continue;
    }
    if (choice.metadata) {
      const localized = locale === defaultLocale ? metadata : metadata.localizations?.[locale];
      requireThat((body.gate === "publish" || entry.metadata === "ready") && localized, `${locale} metadata is not ready`);
      const expected = `${localized.title}\n\n${localized.description}\n`;
      requireThat(files.some((file) => file.role === `description_${locale}` && file.sha256 === hash(expected)), `${locale} description bytes differ from metadata`);
    }
    if (choice.captions) {
      requireThat(body.gate === "publish" || entry.captions === "ready", `${locale} captions are not ready`);
      requireThat(files.some((file) => file.role === `captions_${locale}` && file.sha256 === hash(expectedCaptions[locale])), `${locale} caption bytes have stale offsets or text`);
    }
    if (wantedDubs.includes(locale) && entry.dub === "ready") {
      const current = currentDub(project, workdir, locale, timeline.speech_hash);
      requireThat(current && !current.stale && files.some((file) => file.role === entry.file_role && file.sha256 === entry.sha256) && await sha256File(current.file) === entry.sha256 && current.branding_hash === brand, `${locale} dub has another timeline`);
    }
    if (body.gate === "publish" && wantedDubs.includes(locale)) {
      const available = dubsForUpload(project, workdir, timeline.speech_hash, [locale]);
      const current = available.dubs.find((dub) => dub.locale === locale);
      const skippedReason = metadata.skipped_dub_locales?.[locale];
      const recorded = metadata.dubs?.find((dub) => dub.locale === locale);
      const packaged = current ? path.join(workdir, "upload", "dubs", path.basename(current.file)) : null;
      requireThat(typeof skippedReason === "string" && skippedReason.trim() && skippedReason === available.skipped[locale] || current && current.branding_hash === brand && recorded?.file === `dubs/${path.basename(current.file)}` && recorded.branding_hash === brand && existsSync(packaged) && await sha256File(packaged) === await sha256File(current.file), `${locale} published dub needs regeneration or an explicit skip for the renewed final`);
    }
  }
  if (body.gate === "publish") return { ...body, payload };
  const metadataEntry = await upload(request, project.doc.slug, metadataFile, "metadata", "application/json");
  requireThat(metadataEntry.sha256 === hash(metadataBytes), "metadata changed while staging language proof");
  files.push(metadataEntry);
  const manifest = { schema_version: 1, slug: project.doc.slug, source: { publish: identity(publish), final: identity(final), script: script ? identity(script) : null, branding_hash: brand, speech_hash: timeline.speech_hash ?? null, compilation_hash: timeline.compilation_hash ?? null }, choice: { locales: selected, decided_at: languages.decided_at }, locales: payload.locales, files };
  const manifestFile = path.join(workdir, "review", `renewal-languages-${hash(JSON.stringify(manifest))}.json`);
  atomicWrite(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`);
  const proof = await upload(request, project.doc.slug, manifestFile, "languages_manifest", "application/json");
  // review-pull checks the canonical gate artifact, so its bytes must be this very proof.
  const canonical = path.join(workdir, body.gate === "dubs" ? "dubs/manifest.json" : "review/languages.json");
  atomicWrite(canonical, readFileSync(manifestFile));
  return { ...body, content_sha256: proof.sha256, payload, files: [...files, proof] };
}

export async function renewalMain(args, env = process.env) {
  const [command, ...rest] = args;
  const { values } = parseArgs({ args: rest, options: Object.fromEntries(["from", "out", "original", "body", "branding", "receipt", "reason"].map((key) => [key, { type: "string" }])) });
  if (command === "stage") {
    for (const key of ["from", "out", "original", "body", "branding"]) requireThat(values[key], `stage requires --${key}`);
    const receipt = await stageRenewal({ ...values, env });
    return `${receipt.slug}: candidate staged; select ${path.resolve(values.out, "renewal-candidate.json")} on the owner page. No review was submitted.`;
  }
  requireThat(command === "submit" && values.receipt && values.reason, "usage: renewal.mjs stage --from DIR --out NEW_DIR --original MP4 --body MP4 --branding JSON; or submit --receipt JSON --reason TEXT");
  const site = env.MOKAAIR_SITE ?? "https://mokaair.com";
  const receipt = readJson(values.receipt, null);
  const result = await submitRenewal({ receipt, reason: values.reason, site, request: ownerClient({ site, session: env.MOKAAIR_OWNER_SESSION }) });
  return `${receipt.slug}: ${result.id} is pending human review; old decisions and attachments are retained. No approval or publication occurred.`;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  renewalMain(process.argv.slice(2)).then((message) => process.stdout.write(`${message}\n`)).catch((error) => { process.stderr.write(`${error instanceof UsageError ? error.message : "renewal failed; inspect the owner page before retrying"}\n`); process.exitCode = 1; });
}
