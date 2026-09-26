// `review`: write review/audio.html (after tts) and review/final.html (after assemble).
import { existsSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, loadProject } from "../core/state.mjs";
import { speechHash } from "../core/timeline.mjs";
import { audioReviewHtml, finalReviewHtml, lookReviewHtml } from "./pages.mjs";
import { reviewPull, reviewPush } from "./sync.mjs";

export async function run(command, args, ctx) {
  if (command === "review-push") return reviewPush(args, ctx);
  if (command === "review-pull") return reviewPull(args, ctx);
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" } }, strict: true }).values;
  if (!values.slug && !values.file) throw new UsageError("review needs --slug (or --file for an example outside docs/videos)");
  const { doc, lexicon } = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  // A drama's character sheets come before its narration, so their page needs no timeline.
  const characters = readJson(path.join(workdir, ARTIFACTS.characters), null);
  if (characters?.characters) {
    const lookPage = path.join(workdir, "review", "look.html");
    atomicWrite(lookPage, lookReviewHtml(doc, characters));
    ctx.stdout.write(`choose: ${lookPage}\n`);
  }
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  if (!timeline || timeline.speech_hash !== speechHash(doc, lexicon)) {
    if (characters?.characters) return EXIT.ok;
    ctx.stderr.write("timeline.json is missing or was built for an older script; run tts first\n");
    return EXIT.usage;
  }
  const audioPage = path.join(workdir, "review", "audio.html");
  atomicWrite(audioPage, audioReviewHtml(doc, timeline));
  ctx.stdout.write(`listen: ${audioPage}\n`);
  if (existsSync(path.join(workdir, ARTIFACTS.video))) {
    const finalPage = path.join(workdir, "review", "final.html");
    atomicWrite(finalPage, finalReviewHtml(doc, timeline, readJson(path.join(workdir, ARTIFACTS.checks), null)));
    ctx.stdout.write(`watch: ${finalPage}\n`);
  }
  return EXIT.ok;
}
