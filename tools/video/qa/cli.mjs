import { assembledAudioProblems, audioEvidenceProblems } from "../core/audio-evidence.mjs";
// `qa`: the eleven checks of a finished cut, collected into <workdir>/<slug>/review/qa.json
// (docs/videos/HANDS-OFF.md §自動品管). Most of them read what assemble, render, captions, lint
// and the approvals already recorded; pace, links, thumbnail and facts are computed here; policy
// asks the site's judge. `review-push --gate final` sends the file as the review's payload, and
// the server compares final_sha256 with the review's own hash before it trusts a pass.
//
// Every check is a pure function over files already on disk (checks.mjs and its neighbours);
// this file does the reading, the one network call per link, the judge call, and the writing.
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { AutomationError, automationClient } from "../automation/client.mjs";
import { animeRuntimeContext, hasAnimePolicy, runtimePolicyHash } from "../core/anime-policy.mjs";
import { approvalState, sha256File } from "../core/approvals.mjs";
import { appliedBranding, brandingCurrent, presentationTimeline, readBranding } from "../core/branding.mjs";
import { compilationChecksCurrent, compilationHash, estimatedCompilationTimeline, isCompilation } from "../core/compilation.mjs";
import { cadenceProblems, cadenceSummary, illustrationShare, MAX_PICTURE_SECONDS, MIN_ILLUSTRATION_SHARE } from "../core/cadence.mjs";
import { burnIn, drawnShotScenes, illustrated, isDrama, needsMinimumLength, subtitlesHash } from "../core/drama.mjs";
import { checkYoutubeFields } from "../core/metadata.mjs";
import { atomicWrite, readJson, resolveWorkBase, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { LOCALES, minEpisodeMinutes, narrationLocale } from "../core/schema.mjs";
import { captionLocalesOf, chosenLocales, metadataLocalesOf, readLanguages } from "../core/stages.mjs";
import { approvedEpisodes, ARTIFACTS, dubArtifacts, lintProject, loadProject } from "../core/state.mjs";
import { chapterList, checkChapters, estimateTimeline, speechHash, visualHash } from "../core/timeline.mjs";
import { checksCurrent } from "../package/cli.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { THUMBNAIL_FILE } from "../render/cli.mjs";
import { assembleItem, captionsItem, COMPILATION_ITEM_IDS, compilationCaptionsItem, disclosureDecision, disclosureItem, item, metadataItem, narrationItem, qaReport, renderItem } from "./checks.mjs";
import { factsChecks, VERIFY_FILE } from "./facts.mjs";
import { checkLinks, descriptionUrls, linkChecker, linksDetail } from "./links.mjs";
import { paceDetail, paceProblems, slideStates } from "./pace.mjs";
import { policyRequest, policyVerdict } from "./policy.mjs";
import { thumbnailChecks } from "./thumbnail.mjs";
import { thumbnailSeries } from "../render/plan.mjs";
import { localizedThumbnail } from "../core/translations.mjs";

export const QA_FILE = path.join("review", "qa.json");
// How many kept pictures the assemble item's warning names before it counts the rest, as many as
// a review's summary does (review/sync.mjs SUMMARY_PICTURE_IDS).
export const WARNING_PICTURE_IDS = 5;

/**
 * The assemble item's warning for the pictures kept with the judge's remarks: how many there are
 * and the first few by id, in one line whatever their number. The report travels in the final
 * review's payload, which the server limits (review/sync.mjs fitPayload), and what the judge said
 * of each picture is already there, in accepted_pictures; keyframes/manifest.json has it whole.
 */
export function keptPicturesWarning(ids) {
  const named = ids.slice(0, WARNING_PICTURE_IDS).join(", ");
  const more = ids.length - WARNING_PICTURE_IDS;
  return `${ids.length} ${ids.length === 1 ? "picture" : "pictures"} kept with the judge's remarks after the prompt fixes (${more > 0 ? `${named} and ${more} more` : named}); the owner decides on the cut, and keyframes/manifest.json has what the judge said of each`;
}

/** The disclosure answer, kept in upload/metadata.json for youtube-sync. Idempotent: the publish gate hashes that file. */
function recordDisclosure(file, decision) {
  if (!existsSync(file)) return null;
  const metadata = readJson(file);
  if (metadata.contains_synthetic_media === decision.synthetic && metadata.disclosure_reason === decision.reason) return false;
  atomicWrite(file, `${JSON.stringify({ ...metadata, contains_synthetic_media: decision.synthetic, disclosure_reason: decision.reason }, null, 2)}\n`);
  return true;
}

/**
 * The judge call. A 404 means the endpoint is not deployed yet and a 409 that the channel stance
 * is still blank: both are failed items, never a pass. Anything else (a spent Jev budget, Jev
 * down, a revoked token) says who can fix it, and the exit code carries that.
 */
async function policyItem(ctx, request) {
  let api;
  try {
    api = automationClient(ctx);
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    return { item: item("policy", false, error.message), who: error.who };
  }
  try {
    const verdict = policyVerdict(await api.judgePolicy(request));
    return { item: item("policy", verdict.ok, verdict.detail) };
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    if (error.status === 404) return { item: item("policy", false, "judge endpoint not available") };
    if (error.status === 409 && error.code === "video_judge_not_enabled") return { item: item("policy", false, "channel stance is blank; the judge has nothing to judge against") };
    return { item: item("policy", false, `the judge call failed: ${error.message}`), who: error.who ?? "service" };
  }
}

/** Write review/qa.json and print it; the exit code is the caller's, since policy may set it. */
function writeReport(ctx, doc, workdir, report, finalSha256) {
  const file = path.join(workdir, QA_FILE);
  atomicWrite(file, `${JSON.stringify(report, null, 2)}\n`);
  for (const each of report.items) {
    ctx.stdout.write(`  [${each.ok ? "x" : " "}] ${each.id}: ${each.detail}\n`);
    for (const warning of each.warnings ?? []) ctx.stdout.write(`        warning: ${warning}\n`);
  }
  const passed = report.items.filter((each) => each.ok).length;
  ctx.stdout.write(`${doc.slug}: ${passed} of ${report.items.length} checks passed${finalSha256 ? ` (final.mp4 sha256 ${finalSha256.slice(0, 12)})` : ""}; ${file}\n`);
}

/**
 * The thumbnail item, from the file render drew; then the same check once for each language's
 * own thumbnail render drew (frames/manifest.json thumbnail_locales). Those are extras the owner
 * uploads by hand on Studio's 「語言」 page, so what is wrong with one is a warning, never a fail:
 * the language still has the video's own thumbnail. A compilation's headline is its series'
 * name by design (docs/videos/BINGE.md: 「仙門風雲 全集」 under a title that starts the same way),
 * so the title-repeat warning is not asked of it.
 */
export function thumbnailItem(doc, workdir, translations = {}) {
  const thumbnailFile = path.join(workdir, THUMBNAIL_FILE);
  if (!doc.thumbnail) return item("thumbnail", false, "video.json has no thumbnail; add one with the thumb template");
  if (!existsSync(thumbnailFile)) return item("thumbnail", false, `${THUMBNAIL_FILE} is missing; run render`);
  const series = thumbnailSeries(doc);
  const titleOf = (fields) => (isCompilation(doc) ? null : fields?.title ?? null);
  const verdict = thumbnailChecks({ bytes: readFileSync(thumbnailFile), headline: doc.thumbnail.data?.headline, title: titleOf(doc.youtube), series });
  const warnings = [...verdict.warnings];
  const checked = [];
  for (const [locale, drawn] of Object.entries(readJson(path.join(workdir, ARTIFACTS.frames), null)?.thumbnail_locales ?? {})) {
    const file = path.join(workdir, drawn.file);
    if (!existsSync(file)) {
      warnings.push(`${locale} thumbnail: ${drawn.file} is missing; run render`);
      continue;
    }
    const own = thumbnailChecks({ bytes: readFileSync(file), headline: localizedThumbnail(doc, translations[locale])?.data.headline, title: titleOf(translations[locale]), series, locale });
    checked.push(locale);
    if (!own.ok) warnings.push(`${locale} thumbnail (${drawn.file}): ${own.detail}`);
  }
  const detail = checked.length ? `${verdict.detail}; language thumbnails checked: ${checked.join(", ")}` : verdict.detail;
  return item("thumbnail", verdict.ok, detail, warnings);
}

/**
 * The six checks of a series' compilation (docs/videos/BINGE.md): the join is of the cuts the
 * owner approved and passed its checks, the captions were merged from every episode, every
 * locale's metadata fits with all its chapters, the links open, the thumbnail reads, the
 * disclosure is written. No judge: the episodes' narration went past Jev one by one.
 */
async function compilationQa(ctx, { project, lint, workdir, workBase }) {
  const { EXIT } = ctx;
  const { doc } = project;
  const inWork = (name) => path.join(workdir, name);
  const episodes = approvedEpisodes(doc, workBase);
  const uncleared = episodes.filter((episode) => !episode.sha256).map((episode) => episode.slug);
  const expected = uncleared.length ? null : compilationHash(doc, episodes);
  const checks = readJson(inWork(ARTIFACTS.checks), null);
  const applied = appliedBranding(checks);
  const finalFile = inWork(ARTIFACTS.video);
  const finalExists = existsSync(finalFile);
  const finalSha256 = finalExists ? await sha256File(finalFile) : null;
  const timeline = readJson(inWork(ARTIFACTS.timeline), null);
  const brandingMatches = brandingCurrent(checks, readBranding(workdir)) && (!applied || (applied.body_frames === timeline?.total_frames && checks.compilation_hash === timeline?.compilation_hash));
  const timelineCurrent = Boolean(timeline) && Boolean(expected) && timeline.compilation_hash === expected;
  const presented = presentationTimeline(timeline, brandingMatches ? applied : null);
  const captions = readJson(inWork(ARTIFACTS.captions), null);
  const { problems: metadataProblems, metadata } = composeMetadata({ doc, timeline: timelineCurrent ? presented : estimatedCompilationTimeline(doc), translations: project.translations, pack: null });
  if (!brandingMatches) metadataProblems.push("selected branding differs from the final cut; run compile again");
  const descriptions = [metadata.description, ...Object.values(metadata.localizations).map((fields) => fields.description)];
  const items = [];
  items.push(assembleItem({
    checks,
    current: compilationChecksCurrent(doc, checks, episodes) && brandingMatches && (!applied || checks.metrics?.frames === presented?.total_frames),
    finalExists,
    command: "compile",
    stale: `other cuts or cards${!brandingMatches ? ", or another branding selection" : ""}${uncleared.length ? ` (episodes not cleared for upload: ${uncleared.join(", ")})` : ""}`,
  }));
  items.push(compilationCaptionsItem({ lintWarnings: lint.warnings, manifest: captions, current: Boolean(expected) && captions?.compilation_hash === expected && brandingMatches && (captions?.branding_hash ?? null) === (applied?.hash ?? null), locales: LOCALES, hasCaptionFile: (locale) => existsSync(inWork(path.join("captions", `${locale}.srt`))) }));
  items.push(metadataItem({
    problems: metadataProblems,
    tagProblems: checkYoutubeFields({ title: "", description: "", tags: metadata.tags }, "youtube"),
    chapterProblems: timelineCurrent ? checkChapters(presented) : [],
    locales: [metadata.default_language, ...Object.keys(metadata.localizations)],
    chapters: timelineCurrent ? chapterList(presented).length : 0,
    timelineCurrent,
    command: "compile",
  }));
  const links = await checkLinks(descriptionUrls(descriptions), linkChecker({ fetchImpl: ctx.fetch ?? globalThis.fetch, sleep: ctx.sleep, now: () => Number(ctx.now ? ctx.now() : Date.now()) }));
  items.push(item("links", links.every((result) => result.ok), linksDetail(links)));
  items.push(thumbnailItem(doc, workdir, project.translations));
  const decision = disclosureDecision(doc);
  items.push(disclosureItem(decision, recordDisclosure(inWork(ARTIFACTS.upload), decision)));
  const report = qaReport(items, finalSha256, COMPILATION_ITEM_IDS);
  writeReport(ctx, doc, workdir, report, finalSha256);
  return report.ok ? EXIT.ok : EXIT.lint;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, workdir: { type: "string" } }, strict: true }).values;
  if (!values.slug) throw new UsageError("qa needs --slug");
  const project = loadProject({ slug: values.slug, root: ctx.root });
  const { doc, lexicon } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  if (isCompilation(doc)) return compilationQa(ctx, { project, lint, workdir, workBase: resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home }) });
  const inWork = (name) => path.join(workdir, name);
  const drama = isDrama(doc);
  const speech = speechHash(doc, lexicon);
  const visual = visualHash(doc);

  // What the stages left behind.
  const timeline = readJson(inWork(ARTIFACTS.timeline), null);
  const timelineCurrent = Boolean(timeline) && timeline.speech_hash === speech && !audioEvidenceProblems(timeline, workdir).length;
  const checks = readJson(inWork(ARTIFACTS.checks), null);
  const audioCurrent = !assembledAudioProblems(timeline, checks, workdir).length;
  const applied = appliedBranding(checks);
  const brandingMatches = brandingCurrent(checks, readBranding(workdir)) && (!applied || (applied.body_frames === timeline?.total_frames && checks.speech_hash === timeline?.speech_hash));
  const presented = presentationTimeline(timeline, brandingMatches ? applied : null);
  const clips = drama ? readJson(inWork(ARTIFACTS.clips), null) : null;
  const pictures = illustrated(doc);
  const keyframes = pictures ? readJson(inWork(ARTIFACTS.keyframes), null) : null;
  const music = doc.music ? readJson(inWork(ARTIFACTS.music), null) : null;
  const finalFile = inWork(ARTIFACTS.video);
  const finalExists = existsSync(finalFile);
  const finalSha256 = finalExists ? await sha256File(finalFile) : null;
  const frames = readJson(inWork(ARTIFACTS.frames), null);
  const cache = readJson(inWork(path.join("frames", "cache.json")), null);
  const captions = readJson(inWork(ARTIFACTS.captions), null);
  const approval = await approvalState({ gate: "audio", docDir: project.dir, workdir });
  const reports = readdirSync(project.dir).filter((name) => VERIFY_FILE.test(name));
  // The owner's language choice (docs/videos/LANGUAGES.md): the captions and metadata items look
  // at the narration, zh-TW and the chosen locales; a dub track given up on only warns.
  const languages = readLanguages(workdir);
  const captionLocales = captionLocalesOf(languages, narrationLocale(doc));
  const skippedDubs = Object.fromEntries((chosenLocales(languages, "dub") ?? []).map((locale) => [locale, readJson(dubArtifacts(workdir, locale).skipped, null)]).filter(([, gaveUp]) => gaveUp).map(([locale, gaveUp]) => [locale, gaveUp.reason ?? ""]));
  const { problems: metadataProblems, metadata } = composeMetadata({ doc, timeline: timelineCurrent ? presented : estimateTimeline(doc), translations: project.translations, pack: project.pack ?? null, locales: metadataLocalesOf(languages, narrationLocale(doc)) });
  if (!brandingMatches) metadataProblems.push("selected branding differs from the final cut; run assemble again");
  const descriptions = [metadata.description, ...Object.values(metadata.localizations).map((fields) => fields.description)];

  const items = [];
  let who = null;
  const assemble = assembleItem({ checks, current: audioCurrent && checksCurrent(doc, lexicon, checks, clips, keyframes) && brandingMatches && (!applied || checks.metrics?.frames === presented?.total_frames), finalExists, doc, timeline, presented, timelineCurrent, finalSha256, minMinutes: needsMinimumLength(doc) ? minEpisodeMinutes() : 0, stale: !brandingMatches ? "another branding selection" : pictures ? "an older script, look, pictures, music or effects" : undefined });
  // Pictures kept with the judge's remarks once their prompt fixes were spent (keyframes
  // --accept-best) ride on the assemble item as one warning: the cut is of them, the items are the
  // server's fixed eleven, and the owner decides on the cut (the review goes up for a manual review).
  const acceptedPictures = pictures ? drawnShotScenes(doc).filter((scene) => Array.isArray(keyframes?.shots?.[scene.id]?.accepted_with_problems)).map((scene) => scene.id) : [];
  items.push(acceptedPictures.length ? { ...assemble, warnings: [...(assemble.warnings ?? []), keptPicturesWarning(acceptedPictures)] } : assemble);
  items.push(renderItem({ manifest: frames, cache, visual, speech, subtitles: drama ? subtitlesHash(doc) : null, burnIn: drama && burnIn(doc), hasThumbnail: Boolean(doc.thumbnail) }));
  items.push(narrationItem({ approval, current: timelineCurrent }));
  if (!timelineCurrent) {
    items.push(item("pace", false, "timeline.json is missing or was built for an older script; run tts"));
  } else {
    try {
      const states = slideStates(doc, timeline);
      if (pictures) {
        // Illustrated slides (docs/videos/ILLUSTRATED.md) are measured on the cadence: a picture
        // held past the limit or too little of the runtime illustrated fails; a slow average only shows.
        const cadence = cadenceProblems(doc, timeline);
        const failing = cadence.filter((problem) => problem.kind !== "average");
        const summary = cadenceSummary(states);
        const share = Math.round(illustrationShare(doc, timeline) * 100);
        const figures = `${summary.count} pictures, the longest ${summary.longest} s, a new one every ${summary.average} s on average, ${share}% of the runtime illustrated (limits: ${MAX_PICTURE_SECONDS} s, ${Math.round(MIN_ILLUSTRATION_SHARE * 100)}%)`;
        items.push(item("pace", failing.length === 0, failing.length ? `${figures}; ${failing.map((problem) => `${problem.path}: ${problem.message}`).join("; ")}` : figures, cadence.filter((problem) => problem.kind === "average").map((problem) => problem.message)));
      } else {
        const problems = paceProblems(states);
        items.push(item("pace", problems.length === 0, paceDetail(states, problems)));
      }
    } catch (error) {
      items.push(item("pace", false, error.message));
    }
  }
  items.push(captionsItem({ lintWarnings: lint.warnings, manifest: captions, current: captions?.speech_hash === speech && brandingMatches && (captions?.branding_hash ?? null) === (applied?.hash ?? null), locales: captionLocales, hasCaptionFile: (locale) => existsSync(inWork(path.join("captions", `${locale}.srt`))), skippedDubs }));
  items.push(metadataItem({
    problems: metadataProblems,
    tagProblems: checkYoutubeFields({ title: "", description: "", tags: metadata.tags }, "youtube"),
    chapterProblems: timelineCurrent ? checkChapters(presented) : [],
    locales: [metadata.default_language, ...Object.keys(metadata.localizations)],
    chapters: timelineCurrent ? chapterList(presented).length : 0,
    timelineCurrent,
  }));
  const last = reports.length ? reports.sort((a, b) => Number(VERIFY_FILE.exec(b)[1]) - Number(VERIFY_FILE.exec(a)[1]))[0] : null;
  const facts = factsChecks({ report: last ? { name: last, markdown: readFileSync(path.join(project.dir, last), "utf8") } : null, doc });
  items.push(item("facts", facts.ok, facts.detail));
  const links = await checkLinks(descriptionUrls(descriptions), linkChecker({ fetchImpl: ctx.fetch ?? globalThis.fetch, sleep: ctx.sleep, now: () => Number(ctx.now ? ctx.now() : Date.now()) }));
  items.push(item("links", links.every((result) => result.ok), linksDetail(links)));
  items.push(thumbnailItem(doc, workdir, project.translations));
  const policy = await policyItem(ctx, policyRequest({ doc, brief: project.brief }));
  items.push(policy.item);
  who = policy.who ?? null;
  const decision = disclosureDecision(doc, { musicSource: music?.source ?? (doc.music?.track ? "track" : doc.music ? "generated" : null) });
  items.push(disclosureItem(decision, recordDisclosure(inWork(ARTIFACTS.upload), decision)));

  const report = { ...qaReport(items, finalSha256), ...(hasAnimePolicy(doc) ? { policy_hash: runtimePolicyHash(doc), runtime_spec: { ...doc.runtime_spec }, runtime_context: animeRuntimeContext(doc) } : {}) };
  writeReport(ctx, doc, workdir, report, finalSha256);
  if (who === "owner") return EXIT.owner;
  if (who === "service") return EXIT.external;
  return report.ok ? EXIT.ok : EXIT.lint;
}
