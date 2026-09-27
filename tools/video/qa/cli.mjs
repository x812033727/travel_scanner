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
import { approvalState, sha256File } from "../core/approvals.mjs";
import { burnIn, isDrama, subtitlesHash } from "../core/drama.mjs";
import { checkYoutubeFields } from "../core/metadata.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { captionLocalesOf, chosenLocales, readLanguages } from "../core/stages.mjs";
import { ARTIFACTS, dubArtifacts, lintProject, loadProject } from "../core/state.mjs";
import { chapterList, checkChapters, estimateTimeline, speechHash, visualHash } from "../core/timeline.mjs";
import { checksCurrent } from "../package/cli.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { THUMBNAIL_FILE } from "../render/cli.mjs";
import { assembleItem, captionsItem, disclosureDecision, disclosureItem, item, metadataItem, narrationItem, qaReport, renderItem } from "./checks.mjs";
import { factsChecks, VERIFY_FILE } from "./facts.mjs";
import { checkLinks, descriptionUrls, linkChecker, linksDetail } from "./links.mjs";
import { paceDetail, paceProblems, slideStates } from "./pace.mjs";
import { policyRequest, policyVerdict } from "./policy.mjs";
import { thumbnailChecks } from "./thumbnail.mjs";

export const QA_FILE = path.join("review", "qa.json");

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
  const inWork = (name) => path.join(workdir, name);
  const drama = isDrama(doc);
  const speech = speechHash(doc, lexicon);
  const visual = visualHash(doc);

  // What the stages left behind.
  const timeline = readJson(inWork(ARTIFACTS.timeline), null);
  const timelineCurrent = Boolean(timeline) && timeline.speech_hash === speech;
  const checks = readJson(inWork(ARTIFACTS.checks), null);
  const clips = drama ? readJson(inWork(ARTIFACTS.clips), null) : null;
  const finalFile = inWork(ARTIFACTS.video);
  const finalExists = existsSync(finalFile);
  const finalSha256 = finalExists ? await sha256File(finalFile) : null;
  const frames = readJson(inWork(ARTIFACTS.frames), null);
  const cache = readJson(inWork(path.join("frames", "cache.json")), null);
  const captions = readJson(inWork(ARTIFACTS.captions), null);
  const approval = await approvalState({ gate: "audio", docDir: project.dir, workdir });
  const thumbnailFile = inWork(THUMBNAIL_FILE);
  const reports = readdirSync(project.dir).filter((name) => VERIFY_FILE.test(name));
  // The owner's language choice (docs/videos/LANGUAGES.md): the captions and metadata items look
  // at zh-TW and the chosen locales; a dub track given up on only warns.
  const languages = readLanguages(workdir);
  const captionLocales = captionLocalesOf(languages);
  const skippedDubs = Object.fromEntries((chosenLocales(languages, "dub") ?? []).map((locale) => [locale, readJson(dubArtifacts(workdir, locale).skipped, null)]).filter(([, gaveUp]) => gaveUp).map(([locale, gaveUp]) => [locale, gaveUp.reason ?? ""]));
  const { problems: metadataProblems, metadata } = composeMetadata({ doc, timeline: timelineCurrent ? timeline : estimateTimeline(doc), translations: project.translations, pack: project.pack ?? null, locales: chosenLocales(languages, "metadata") });
  const descriptions = [metadata.description, ...Object.values(metadata.localizations).map((fields) => fields.description)];

  const items = [];
  let who = null;
  items.push(assembleItem({ checks, current: checksCurrent(doc, lexicon, checks, clips), finalExists }));
  items.push(renderItem({ manifest: frames, cache, visual, speech, subtitles: drama ? subtitlesHash(doc) : null, burnIn: drama && burnIn(doc), hasThumbnail: Boolean(doc.thumbnail) }));
  items.push(narrationItem({ approval, current: timelineCurrent }));
  if (!timelineCurrent) {
    items.push(item("pace", false, "timeline.json is missing or was built for an older script; run tts"));
  } else {
    try {
      const states = slideStates(doc, timeline);
      const problems = paceProblems(states);
      items.push(item("pace", problems.length === 0, paceDetail(states, problems)));
    } catch (error) {
      items.push(item("pace", false, error.message));
    }
  }
  items.push(captionsItem({ lintWarnings: lint.warnings, manifest: captions, current: captions?.speech_hash === speech, locales: captionLocales, hasCaptionFile: (locale) => existsSync(inWork(path.join("captions", `${locale}.srt`))), skippedDubs }));
  items.push(metadataItem({
    problems: metadataProblems,
    tagProblems: checkYoutubeFields({ title: "", description: "", tags: metadata.tags }, "youtube"),
    chapterProblems: timelineCurrent ? checkChapters(timeline) : [],
    locales: [metadata.default_language, ...Object.keys(metadata.localizations)],
    chapters: timelineCurrent ? chapterList(timeline).length : 0,
    timelineCurrent,
  }));
  const last = reports.length ? reports.sort((a, b) => Number(VERIFY_FILE.exec(b)[1]) - Number(VERIFY_FILE.exec(a)[1]))[0] : null;
  const facts = factsChecks({ report: last ? { name: last, markdown: readFileSync(path.join(project.dir, last), "utf8") } : null, doc });
  items.push(item("facts", facts.ok, facts.detail));
  const links = await checkLinks(descriptionUrls(descriptions), linkChecker({ fetchImpl: ctx.fetch ?? globalThis.fetch, sleep: ctx.sleep, now: () => Number(ctx.now ? ctx.now() : Date.now()) }));
  items.push(item("links", links.every((result) => result.ok), linksDetail(links)));
  if (!doc.thumbnail) items.push(item("thumbnail", false, "video.json has no thumbnail; add one with the thumb template"));
  else if (!existsSync(thumbnailFile)) items.push(item("thumbnail", false, `${THUMBNAIL_FILE} is missing; run render`));
  else {
    const verdict = thumbnailChecks({ bytes: readFileSync(thumbnailFile), headline: doc.thumbnail.data?.headline });
    items.push(item("thumbnail", verdict.ok, verdict.detail, verdict.warnings));
  }
  const policy = await policyItem(ctx, policyRequest({ doc, brief: project.brief }));
  items.push(policy.item);
  who = policy.who ?? null;
  const decision = disclosureDecision(doc);
  items.push(disclosureItem(decision, recordDisclosure(inWork(ARTIFACTS.upload), decision)));

  const report = qaReport(items, finalSha256);
  const file = inWork(QA_FILE);
  atomicWrite(file, `${JSON.stringify(report, null, 2)}\n`);
  for (const each of report.items) {
    ctx.stdout.write(`  [${each.ok ? "x" : " "}] ${each.id}: ${each.detail}\n`);
    for (const warning of each.warnings ?? []) ctx.stdout.write(`        warning: ${warning}\n`);
  }
  const passed = report.items.filter((each) => each.ok).length;
  ctx.stdout.write(`${doc.slug}: ${passed} of ${report.items.length} checks passed${finalSha256 ? ` (final.mp4 sha256 ${finalSha256.slice(0, 12)})` : ""}; ${file}\n`);
  if (who === "owner") return EXIT.owner;
  if (who === "service") return EXIT.external;
  return report.ok ? EXIT.ok : EXIT.lint;
}
