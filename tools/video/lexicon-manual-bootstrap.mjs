#!/usr/bin/env node
// A standalone CLI: the worker's main cli.mjs is owned by a separate task.
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { bootstrapManualStoryLexicon, inspectManualStoryBootstrap, recoverCommittedManualBootstrap } from "./core/lexicon-manual-bootstrap.mjs";
import { resolveWorkdir, ROOT } from "./core/paths.mjs";

const usage = "Usage: node tools/video/lexicon-manual-bootstrap.mjs --slug S --workdir MEDIA_BASE --review docs/videos/S/reviews/lexicon-bootstrap.json [--json] [--apply]; or --slug S --workdir MEDIA_BASE --recover TRANSACTION_ID";

export function runManualBootstrapCli(args, { root = ROOT, stdout = process.stdout, stderr = process.stderr, now = () => new Date() } = {}) {
  let values;
  try {
    values = parseArgs({ args, options: {
      slug: { type: "string" }, workdir: { type: "string" }, review: { type: "string" },
      apply: { type: "boolean" }, recover: { type: "string" }, json: { type: "boolean" }, help: { type: "boolean" },
    }, strict: true }).values;
  } catch (error) { stderr.write(`${error.message}\n${usage}\n`); return 2; }
  if (values.help) { stdout.write(`${usage}\n`); return 0; }
  if (!values.slug || !values.workdir || Boolean(values.recover) === Boolean(values.review)
      || (values.apply && values.recover)) { stderr.write(`${usage}\n`); return 2; }
  let workdir;
  try { workdir = resolveWorkdir({ flag: values.workdir, slug: values.slug, root }); }
  catch (error) { stderr.write(`${error.message}\n`); return 2; }
  try {
    if (values.recover) {
      const result = recoverCommittedManualBootstrap({ root, slug: values.slug, workdir, transactionId: values.recover });
      const output = { slug: values.slug, status: "recovered_committed", transaction_id: values.recover, lexicon_sha256: result.lexicon_sha256 };
      stdout.write(values.json ? `${JSON.stringify(output, null, 2)}\n` : `${values.slug}: recovered committed transaction ${values.recover}; lexicon ${result.lexicon_sha256}\n`);
      return 0;
    }
    const reviewFile = path.resolve(root, values.review);
    const report = inspectManualStoryBootstrap({ root, slug: values.slug, workdir, reviewFile });
    let applied = null;
    if (values.apply && report.allowed) applied = bootstrapManualStoryLexicon({ root, slug: values.slug, workdir, reviewFile, now });
    if (values.json) stdout.write(`${JSON.stringify({ ...report, apply: Boolean(values.apply), applied: applied && {
      bootstrapped: applied.bootstrapped, lexicon_sha256: applied.lexicon_sha256, transaction_id: applied.transaction_id ?? null,
    } }, null, 2)}\n`);
    else {
      stdout.write(`${values.slug}: ${report.status}${report.lexicon_sha256 ? `; snapshot ${report.lexicon_sha256}` : ""}\n`);
      for (const check of report.checks) stdout.write(`  ${check.ok ? "ok  " : "FAIL"} ${check.id}${check.ok ? "" : ` -> ${check.code}: ${check.detail}`}\n`);
      if (report.status === "allowed" && !values.apply) stdout.write("dry run: nothing written; rerun with --apply to pin the reviewed manual draft\n");
      if (applied) stdout.write(`pinned ${values.slug}: lexicon ${applied.lexicon_sha256}; transaction ${applied.transaction_id}\n`);
    }
    return report.status === "refused" ? 1 : 0;
  } catch (error) { stderr.write(`${error.message}\n`); return 1; }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = runManualBootstrapCli(process.argv.slice(2));
}
