// `package`: everything the owner uploads, in <VIDEO_WORKDIR>/<slug>/upload/, once final.mp4 has
// been approved exactly as it is. metadata.json carries the disclosure answer (the same the
// quality check writes), and the package is checked as soon as it is written
// (docs/videos/HANDS-OFF.md §上傳包與「可以上架」); the publish review sends that check.
import { copyFileSync, existsSync, linkSync, mkdirSync, readdirSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { approvalState } from "../core/approvals.mjs";
import { appliedBranding, brandingCurrent, presentationTimeline, readBranding } from "../core/branding.mjs";
import { compilationChecksCurrent, isCompilation } from "../core/compilation.mjs";
import { COMPILATION_REVIEW_FILE, publicTexts, reviewCurrent } from "../core/compilation-review.mjs";
import { illustrated, isDrama, keyframesHash, lookHash, mixHash, sfxHash, subtitlesHash } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkBase, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { LOCALES, NARRATION_LOCALE, narrationLocale } from "../core/schema.mjs";
import { captionLocalesOf, dubLocalesOf, dubsForUpload, metadataLocalesOf, readLanguages, runCaptions } from "../core/stages.mjs";
import { approvedEpisodes, ARTIFACTS, loadProject, recordStage } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { disclosureDecision } from "../qa/checks.mjs";
import { readPackageReport } from "./check.mjs";
import { composeMetadata, uploadChecklist } from "./metadata.mjs";

/**
 * Why a locale has no caption file, for metadata.json's skipped_caption_locales: the line ids
 * the captions stage left out (missing or older than zh-TW), or that no translation exists at
 * all. The package check accepts either as a reason. `locales` are the caption locales wanted.
 */
export function skippedCaptionLocales(manifest, written, { locales = LOCALES, compilation = false } = {}) {
  const skipped = {};
  for (const locale of locales) {
    if (written.includes(`captions/${locale}.srt`)) continue;
    const lines = manifest?.skipped?.[locale];
    // A compilation's manifest lists the episodes that have no file for the locale instead.
    if (compilation) skipped[locale] = Array.isArray(lines) && lines.length ? `no caption file in episodes ${lines.join(", ")}` : "no caption file merged";
    else skipped[locale] = Array.isArray(lines) && lines.length ? lines : `no translation (i18n/${locale}.json missing)`;
  }
  return skipped;
}

/**
 * Whether the caption manifest was cut for this narration and for exactly the caption locales
 * wanted now: the owner's choice may have grown or shrunk since the captions were last written.
 * A locale with no translation at all cannot have been written; the narration's always is.
 */
export function captionsCurrent(manifest, speech, wanted, translations, brandingHash = null, narration = NARRATION_LOCALE) {
  if (!manifest || manifest.speech_hash !== speech || (manifest.branding_hash ?? null) !== brandingHash) return false;
  const have = Object.keys(manifest.locales ?? {});
  if (have.some((locale) => !wanted.includes(locale))) return false;
  return wanted.every((locale) => manifest.locales?.[locale] || manifest.skipped?.[locale] || (locale !== narration && !translations[locale]));
}

/**
 * A compilation's final.mp4 is gigabytes, so upload/ holds a hard link to it rather than a
 * copy; a file system that refuses the link (another volume) gets the copy.
 */
export function linkOrCopy(source, target) {
  try {
    linkSync(source, target);
    return "linked";
  } catch {
    copyFileSync(source, target);
    return "copied";
  }
}

/**
 * Whether checks.json describes the final video of this very script: its narration and
 * pictures, and for a drama its look, clips, subtitles and music as well.
 */
export function checksCurrent(doc, lexicon, checks, clips = null, keyframes = null) {
  if (!checks?.ok || checks.speech_hash !== speechHash(doc, lexicon) || checks.visual_hash !== visualHash(doc)) return false;
  // Any format binds its cut to the sound effects it names; a drama's mix hash is always there.
  if (doc.sfx && checks.sfx_hash !== sfxHash(doc)) return false;
  if (isDrama(doc)) {
    return checks.look_hash === lookHash(doc) && checks.subtitles_hash === subtitlesHash(doc) && checks.mix_hash === mixHash(doc) && Boolean(clips?.clips_hash) && checks.clips_hash === clips.clips_hash;
  }
  if (doc.music && checks.mix_hash !== mixHash(doc)) return false;
  // Illustrated slides (docs/videos/ILLUSTRATED.md): the very pictures, as the keyframes manifest holds them now.
  if (illustrated(doc)) return checks.look_hash === lookHash(doc) && Boolean(keyframes) && checks.pictures_hash === keyframesHash(doc, keyframes);
  return true;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" } }, strict: true }).values;
  if (!values.slug && !values.file) throw new UsageError("package needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc, lexicon } = project;
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  // A series' compilation (docs/videos/BINGE.md): its checks and captions are compile's, bound
  // to the episodes' approved cuts, and its final.mp4 is linked rather than copied.
  const compilation = isCompilation(doc);
  const episodes = compilation ? approvedEpisodes(doc, resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home })) : null;
  const speech = compilation ? null : speechHash(doc, lexicon);
  const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
  const applied = appliedBranding(checks);
  const bodyTimeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const brandingMatches = brandingCurrent(checks, readBranding(workdir)) && (!applied || (applied.body_frames === bodyTimeline?.total_frames
    && checks.metrics?.frames === applied.intro_frames + applied.body_frames + applied.outro_frames
    && (compilation ? checks.compilation_hash === bodyTimeline?.compilation_hash : checks.speech_hash === bodyTimeline?.speech_hash)));
  const clips = isDrama(doc) && !compilation ? readJson(path.join(workdir, ARTIFACTS.clips), null) : null;
  const keyframes = illustrated(doc) ? readJson(path.join(workdir, ARTIFACTS.keyframes), null) : null;
  const current = compilation ? compilationChecksCurrent(doc, checks, episodes) : checksCurrent(doc, lexicon, checks, clips, keyframes);
  if (!brandingMatches) {
    ctx.stderr.write(`final.mp4 does not match the selected branding; run ${compilation ? "compile" : "assemble"} again before package\n`);
    return EXIT.usage;
  }
  if (!existsSync(path.join(workdir, ARTIFACTS.video)) || !current) {
    ctx.stderr.write(compilation ? "final.mp4 is missing, failed its checks, or was joined from other cuts or cards; run compile first\n" : "final.mp4 is missing, failed its checks, or is older than the script; run assemble first\n");
    return EXIT.usage;
  }
  const approval = await approvalState({ gate: "final", docDir: project.dir, workdir });
  if (approval.status !== "approved") {
    const why = approval.status === "stale" ? "changed after it was approved" : "has not been approved";
    ctx.stderr.write(`final.mp4 ${why}: the owner watches review/final.html, then node tools/video/cli.mjs approve --slug ${doc.slug} --gate final\n`);
    return EXIT.owner;
  }

  // The owner's language choice (docs/videos/LANGUAGES.md): which locales get a description, a
  // caption file and a dub track; without one, every translated locale, as before. The
  // narration's own locale and zh-TW always get captions and a description (alwaysLocales).
  const languages = readLanguages(workdir);
  const narration = narrationLocale(doc);
  const captionLocales = captionLocalesOf(languages, narration);
  const metadataLocales = metadataLocalesOf(languages, narration);
  const dubLocales = dubLocalesOf(languages, doc);
  const timeline = presentationTimeline(bodyTimeline, applied);
  const captionsManifest = readJson(path.join(workdir, ARTIFACTS.captions), null);
  let captions;
  if (compilation) {
    if (captionsManifest?.compilation_hash !== checks.compilation_hash || (captionsManifest?.branding_hash ?? null) !== (applied?.hash ?? null)) {
      ctx.stderr.write("captions/manifest.json is missing or was merged for other cuts; run compile again\n");
      return EXIT.usage;
    }
    captions = captionsManifest;
  } else captions = captionsCurrent(captionsManifest, speech, captionLocales, project.translations, applied?.hash ?? null, narration) ? captionsManifest : runCaptions({ slug: values.slug, file: values.file, root: ctx.root, workdir, now: ctx.now() });
  const { problems, metadata } = composeMetadata({ doc, timeline, translations: project.translations, pack: project.pack ?? null, locales: metadataLocales });
  if (problems.length) {
    for (const problem of problems) ctx.stdout.write(`ERROR ${problem}\n`);
    return EXIT.lint;
  }

  if (compilation) {
    const context = readJson(path.join(project.dir, "compilation.json"), null)?.spoiler_context;
    if (!Array.isArray(context?.mysteries)) {
      ctx.stderr.write("the compilation's mystery context is unknown; resume the worker to restore it and review the public text before package\n");
      return EXIT.usage;
    }
    if (context.mysteries.length) {
      const receipts = readJson(path.join(project.dir, COMPILATION_REVIEW_FILE), null);
      const fields = publicTexts({ doc, translations: project.translations, timeline, plan: readJson(path.join(project.dir, "metadata-plan.json"), null), pack: project.pack ?? null });
      const locales = [metadata.default_language, ...Object.keys(metadata.localizations)];
      const unreviewed = locales.filter((locale) => !reviewCurrent(receipts, context, locale, fields[locale]));
      if (unreviewed.length) {
        ctx.stderr.write(`the compilation's public text needs a current spoiler review for ${unreviewed.join(", ")}; resume the worker before package\n`);
        return EXIT.owner;
      }
    }
  }

  const upload = path.join(workdir, "upload");
  rmSync(upload, { recursive: true, force: true });
  mkdirSync(path.join(upload, "captions"), { recursive: true });
  const finalHow = compilation ? linkOrCopy(path.join(workdir, ARTIFACTS.video), path.join(upload, "final.mp4")) : "copied";
  if (!compilation) copyFileSync(path.join(workdir, ARTIFACTS.video), path.join(upload, "final.mp4"));
  const thumbnail = existsSync(path.join(workdir, "thumbnail.jpg"));
  if (thumbnail) copyFileSync(path.join(workdir, "thumbnail.jpg"), path.join(upload, "thumbnail.jpg"));
  const captionFiles = [];
  for (const name of readdirSync(path.join(workdir, "captions")).filter((file) => file.endsWith(".srt") && captionLocales.includes(path.basename(file, ".srt"))).sort()) {
    copyFileSync(path.join(workdir, "captions", name), path.join(upload, "captions", name));
    captionFiles.push(`captions/${name}`);
  }
  atomicWrite(path.join(upload, `description.${metadata.default_language}.txt`), `${metadata.title}\n\n${metadata.description}\n`);
  for (const [locale, fields] of Object.entries(metadata.localizations)) {
    atomicWrite(path.join(upload, `description.${locale}.txt`), `${fields.title}\n\n${fields.description}\n`);
  }
  // The dub tracks the owner picked and the worker finished (docs/videos/DUBS.md); a locale the
  // worker gave up on is named with its reason, so the owner knows not to wait for it.
  const { dubs: tracks, skipped: skippedDubs } = compilation ? { dubs: [], skipped: {} } : dubsForUpload(project, workdir, speech, dubLocales);
  const dubs = tracks.map((dub) => {
    mkdirSync(path.join(upload, "dubs"), { recursive: true });
    copyFileSync(dub.file, path.join(upload, "dubs", path.basename(dub.file)));
    return { ...dub, file: `dubs/${path.basename(dub.file)}` };
  });
  // The disclosure answer goes last, in this order: the quality check writes the same two keys
  // the same way, so a qa run after package leaves metadata.json byte for byte as it is.
  const disclosure = disclosureDecision(doc);
  // A compilation's card on the site offers the file for download instead of holding a copy
  // (docs/videos/BINGE.md): the record says where, how big, and which cuts went in.
  const compiled = compilation ? { compilation: true, download: "upload/final.mp4", size_bytes: statSync(path.join(upload, "final.mp4")).size, episodes: readJson(path.join(workdir, ARTIFACTS.compilation), null)?.episodes ?? checks.metrics?.episodes ?? [] } : null;
  const record = {
    ...metadata,
    final_sha256: approval.sha256,
    ...(applied ? { branding_hash: applied.hash } : {}),
    thumbnail: thumbnail ? "thumbnail.jpg" : null,
    captions: captionFiles,
    skipped_caption_locales: skippedCaptionLocales(captions, captionFiles, { locales: captionLocales, compilation }),
    dubs,
    skipped_dub_locales: skippedDubs,
    // What the owner chose per language (docs/videos/LANGUAGES.md), for youtube-sync and the card; null without a choice.
    language_choice: languages ? languages.locales : null,
    ...(compiled ?? {}),
    contains_synthetic_media: disclosure.synthetic,
    disclosure_reason: disclosure.reason,
  };
  atomicWrite(path.join(upload, "metadata.json"), `${JSON.stringify(record, null, 2)}\n`);
  atomicWrite(path.join(upload, "UPLOAD.md"), uploadChecklist({ metadata: record, captions: captionFiles, thumbnail, drama: isDrama(doc), disclosure, dubs, skippedDubs, compilation: compiled ? { episodes: compiled.episodes.length, size_bytes: compiled.size_bytes } : null }));
  recordStage(workdir, "package", { locales: [metadata.default_language, ...Object.keys(metadata.localizations)], captions: captionFiles.length, dubs: dubs.map((dub) => dub.locale), ...(compiled ? { compilation: true, final: finalHow, size_bytes: compiled.size_bytes } : {}) }, ctx.now());
  ctx.stdout.write(`upload package: ${upload}\n  final.mp4${compiled ? ` (${finalHow}, ${(compiled.size_bytes / 1024 ** 3).toFixed(2)} GB, ${compiled.episodes.length} episodes)` : ""}, ${thumbnail ? "thumbnail.jpg, " : ""}${captionFiles.length} caption files, ${1 + Object.keys(metadata.localizations).length} locales of title and description${dubs.length ? `, ${dubs.length} dub tracks (${dubs.map((dub) => dub.locale).join(", ")})` : ""}\n  follow ${path.join(upload, "UPLOAD.md")}\n`);
  const { report } = await readPackageReport(workdir);
  for (const each of report.items) ctx.stdout.write(`  [${each.ok ? "x" : " "}] ${each.id}: ${each.detail}\n`);
  if (!report.ok) {
    ctx.stderr.write(`the upload package failed ${report.items.filter((each) => !each.ok).length} of its ${report.items.length} checks; fix them and run package again\n`);
    return EXIT.lint;
  }
  ctx.stdout.write(`package check: ${report.items.length} of ${report.items.length} passed (metadata.json sha256 ${report.final_sha256.slice(0, 12)})\n`);
  return EXIT.ok;
}
