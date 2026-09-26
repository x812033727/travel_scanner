// `package`: everything the owner uploads, in <VIDEO_WORKDIR>/<slug>/upload/, once they have
// approved final.mp4 exactly as it is.
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { approvalState } from "../core/approvals.mjs";
import { isDrama, lookHash, mixHash, subtitlesHash } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { runCaptions } from "../core/stages.mjs";
import { ARTIFACTS, loadProject, recordStage } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { composeMetadata, uploadChecklist } from "./metadata.mjs";

/**
 * Whether checks.json describes the final video of this very script: its narration and
 * pictures, and for a drama its look, clips, subtitles and music as well.
 */
export function checksCurrent(doc, lexicon, checks, clips = null) {
  if (!checks?.ok || checks.speech_hash !== speechHash(doc, lexicon) || checks.visual_hash !== visualHash(doc)) return false;
  if (!isDrama(doc)) return true;
  return checks.look_hash === lookHash(doc) && checks.subtitles_hash === subtitlesHash(doc) && checks.mix_hash === mixHash(doc) && Boolean(clips?.clips_hash) && checks.clips_hash === clips.clips_hash;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" } }, strict: true }).values;
  if (!values.slug && !values.file) throw new UsageError("package needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc, lexicon } = project;
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const speech = speechHash(doc, lexicon);
  const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
  const clips = isDrama(doc) ? readJson(path.join(workdir, ARTIFACTS.clips), null) : null;
  if (!existsSync(path.join(workdir, ARTIFACTS.video)) || !checksCurrent(doc, lexicon, checks, clips)) {
    ctx.stderr.write("final.mp4 is missing, failed its checks, or is older than the script; run assemble first\n");
    return EXIT.usage;
  }
  const approval = await approvalState({ gate: "final", docDir: project.dir, workdir });
  if (approval.status !== "approved") {
    const why = approval.status === "stale" ? "changed after it was approved" : "has not been approved";
    ctx.stderr.write(`final.mp4 ${why}: the owner watches review/final.html, then node tools/video/cli.mjs approve --slug ${doc.slug} --gate final\n`);
    return EXIT.owner;
  }

  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline));
  const captionsManifest = readJson(path.join(workdir, ARTIFACTS.captions), null);
  const captions = captionsManifest?.speech_hash === speech ? captionsManifest : runCaptions({ slug: values.slug, file: values.file, root: ctx.root, workdir, now: ctx.now() });
  const { problems, metadata } = composeMetadata({ doc, timeline, translations: project.translations, pack: project.pack ?? null });
  if (problems.length) {
    for (const problem of problems) ctx.stdout.write(`ERROR ${problem}\n`);
    return EXIT.lint;
  }

  const upload = path.join(workdir, "upload");
  rmSync(upload, { recursive: true, force: true });
  mkdirSync(path.join(upload, "captions"), { recursive: true });
  copyFileSync(path.join(workdir, ARTIFACTS.video), path.join(upload, "final.mp4"));
  const thumbnail = existsSync(path.join(workdir, "thumbnail.jpg"));
  if (thumbnail) copyFileSync(path.join(workdir, "thumbnail.jpg"), path.join(upload, "thumbnail.jpg"));
  const captionFiles = [];
  for (const name of readdirSync(path.join(workdir, "captions")).filter((file) => file.endsWith(".srt")).sort()) {
    copyFileSync(path.join(workdir, "captions", name), path.join(upload, "captions", name));
    captionFiles.push(`captions/${name}`);
  }
  atomicWrite(path.join(upload, `description.${metadata.default_language}.txt`), `${metadata.title}\n\n${metadata.description}\n`);
  for (const [locale, fields] of Object.entries(metadata.localizations)) {
    atomicWrite(path.join(upload, `description.${locale}.txt`), `${fields.title}\n\n${fields.description}\n`);
  }
  const record = { ...metadata, final_sha256: approval.sha256, thumbnail: thumbnail ? "thumbnail.jpg" : null, captions: captionFiles, skipped_caption_locales: captions.skipped ?? {} };
  atomicWrite(path.join(upload, "metadata.json"), `${JSON.stringify(record, null, 2)}\n`);
  atomicWrite(path.join(upload, "UPLOAD.md"), uploadChecklist({ metadata, captions: captionFiles, thumbnail, drama: isDrama(doc) }));
  recordStage(workdir, "package", { locales: [metadata.default_language, ...Object.keys(metadata.localizations)], captions: captionFiles.length }, ctx.now());
  ctx.stdout.write(`upload package: ${upload}\n  final.mp4, ${thumbnail ? "thumbnail.jpg, " : ""}${captionFiles.length} caption files, ${1 + Object.keys(metadata.localizations).length} locales of title and description\n  follow ${path.join(upload, "UPLOAD.md")}\n`);
  return EXIT.ok;
}
