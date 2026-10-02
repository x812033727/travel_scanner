// Offline director-plan checks and review bundles. Never calls an AI or production API.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import { pathToFileURL } from "node:url";
import { UsageError } from "../core/paths.mjs";
import { designHash, designProblems, productionSetting } from "./design.mjs";
import { storyboardHtml } from "./preview.mjs";
import { buildAuditionPlan } from "./voice-audit.mjs";

const BATCHES = ["binge-five-20260928", "claude-binge-five-20260928"];
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;

export async function loadDesigns(root, wanted = null) {
  const base = path.join(root, "docs", "videos", "series-plans");
  const directory = path.join(base, "production-20261001");
  const profile = JSON.parse(readFileSync(path.join(directory, "profile.json"), "utf8"));
  const works = [];
  for (const batch of BATCHES) {
    const builder = await import(pathToFileURL(path.join(base, batch, "build.mjs")));
    for (const slug of builder.SLUGS) {
      if (wanted && !wanted.includes(slug)) continue;
      const source = await builder.loadSource(slug);
      const design = JSON.parse(readFileSync(path.join(base, batch, slug, "production-design.json"), "utf8"));
      works.push({ batch, slug, source, design, files: builder.compile(source) });
    }
  }
  if (wanted && works.length !== new Set(wanted).size) throw new UsageError("--slug includes an unknown work");
  return { profile, directory, works };
}

export function buildBundle(work, profile) {
  const original = JSON.parse(work.files["documents.json"]);
  const documents = original.documents.map((document) => document.kind === "setting"
    ? { ...document, ...productionSetting(document, work.design, profile) }
    : document);
  const bundle = { slug: work.slug, status: "prepared-not-submitted", documents };
  const request = { ...JSON.parse(work.files["series-request.json"]), visual_tier: "clips" };
  const manifest = {
    schema_version: 1,
    slug: work.slug,
    source_sha256: designHash(work.source),
    design_sha256: designHash(work.design),
    profile_sha256: designHash(profile),
    documents_sha256: designHash(json(bundle)),
    series_request_sha256: designHash(json(request)),
    status: "new-production-review-bundle-not-imported",
    historical_receipts_modified: false,
    generation_performed: false,
    audition_performed: false,
    approval_granted: false,
    model_route_status: work.design.characters.some((entry) => entry.video_constraints) || work.design.episodes.some((entry) => entry.video_constraints)
      ? "requires-minor-animation-route" : "requires-pilot-acceptance",
  };
  return { bundle, request, manifest };
}

function auditions(work, profile, folder, root) {
  const plan = buildAuditionPlan(work, profile);
  for (const entry of plan.entries) {
    if (entry.synthesis_allowed === false || !entry.transcript?.trim()) continue;
    const file = path.join(folder, `${entry.id}.txt`);
    const transcript = `${entry.transcript.trim()}\n`;
    writeFileSync(file, transcript, "utf8");
    const style = entry.audition_style;
    if (!style || style.length > 400) throw new UsageError(`${work.slug}/${entry.id}: audition style exceeds TTS limits`);
    entry.text_sha256 = designHash(transcript);
    entry.args = ["audition", "--text-file", path.relative(root, file).split(path.sep).join("/"), "--voices", `gemini:${entry.voice}`, "--style", style];
  }
  return plan;
}

export async function run(command, args, ctx) {
  const options = parseArgs({ args, options: { slug: { type: "string" }, out: { type: "string" } }, strict: true }).values;
  const { profile, directory, works } = await loadDesigns(ctx.root, options.slug?.split(","));
  const results = works.map((work) => ({ slug: work.slug, episodes: work.design.episodes?.length ?? 0, errors: designProblems(work.design, work.source, profile) }));
  const failures = results.flatMap((result) => result.errors.map((error) => `${result.slug}: ${error}`));
  for (const failure of failures) ctx.stderr.write(`${failure}\n`);
  if (failures.length) return ctx.EXIT.lint;
  if (command === "production-build") {
    const out = options.out ? path.resolve(options.out) : directory;
    mkdirSync(out, { recursive: true });
    const receipt = [];
    for (const work of works) {
      const folder = path.join(out, "bundles", work.slug);
      mkdirSync(folder, { recursive: true });
      const { bundle, request, manifest } = buildBundle(work, profile);
      writeFileSync(path.join(folder, "documents.json"), json(bundle));
      writeFileSync(path.join(folder, "series-request.json"), json(request));
      writeFileSync(path.join(folder, "manifest.json"), json(manifest));
      const auditionFolder = path.join(folder, "auditions");
      mkdirSync(auditionFolder, { recursive: true });
      writeFileSync(path.join(folder, "audition-plan.json"), json(auditions(work, profile, auditionFolder, ctx.root)));
      receipt.push(manifest);
    }
    writeFileSync(path.join(out, "build-receipt.json"), json({ status: "local-build-not-imported", works: receipt }));
    writeFileSync(path.join(out, "readiness.json"), json({
      status: "planning-valid-not-approved-for-generation", chinese_audio_accepted: false,
      chinese_final_accepted: false, localization_started: false,
      works: works.map((work, index) => ({ slug: work.slug, title: work.source.series.title,
        route_status: receipt[index].model_route_status,
        minor_characters: work.design.characters.filter((entry) => entry.video_constraints).map((entry) => ({ id: entry.id, ...entry.video_constraints })),
        episodes_with_unnamed_children: work.design.episodes.filter((entry) => entry.video_constraints).map((entry) => ({ episode: entry.episode, ...entry.video_constraints })),
        remaining_pilot_questions: work.design.unresolved,
      })),
    }));
    writeFileSync(path.join(out, "storyboard.html"), storyboardHtml(works, profile));
    ctx.stdout.write(`built ${works.length} review bundles, audition plans and storyboard.html in ${out}\n`);
  } else if (command !== "production-check") throw new UsageError(`unknown production command ${command}`);
  ctx.stdout.write(`${works.length} works, ${results.reduce((total, result) => total + result.episodes, 0)} episode designs: no design errors; audio and films remain untested\n`);
  const limited = works.filter((work) => work.design.characters.some((entry) => entry.video_constraints) || work.design.episodes.some((entry) => entry.video_constraints));
  if (limited.length) ctx.stdout.write(`${limited.length} works need a separately verified route for minor characters before whole-film production\n`);
  return ctx.EXIT.ok;
}
