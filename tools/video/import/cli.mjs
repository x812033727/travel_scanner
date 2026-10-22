// `import`: a long video finished by another tool, sent to /admin/videos (import.mjs).
import path from "node:path";
import { parseArgs } from "node:util";

import { ToolMissing } from "../assemble/ffmpeg.mjs";
import { UsageError } from "../core/paths.mjs";
import { SiteError } from "../shorts/site.mjs";
import { importLanguages, importLong, importPublish } from "./import.mjs";

export async function run(_command, args, ctx) {
  const values = parseArgs({ args, options: { from: { type: "string" }, workdir: { type: "string" }, force: { type: "boolean" }, languages: { type: "boolean" }, publish: { type: "boolean" } }, strict: true }).values;
  if (!values.from) throw new UsageError("import needs --from DIR holding final.mp4 and meta.json (zh-TW.srt and thumbnail.png are optional); --languages then sends its description.<l>.txt, <l>.srt and dub.<l>.m4a; --publish, after the owner approved the cut, its upload package");
  if (values.languages && values.publish) throw new UsageError("--languages and --publish are two steps: send the languages first, then the package");
  const log = (line) => ctx.stdout.write(`${line}\n`);
  try {
    if (values.publish) {
      const result = await importPublish({ from: path.resolve(values.from), workdir: values.workdir, env: ctx.env, home: ctx.home, log });
      for (const [part, locales] of Object.entries(result.skipped)) for (const [locale, why] of Object.entries(locales)) ctx.stdout.write(`  ${locale} ${part} skipped: ${why}\n`);
      ctx.stdout.write(`${result.slug}: on /admin/videos, the upload package ${result.status === "pending" ? "waits for the owner" : result.status}\n`);
      return ctx.EXIT.ok;
    }
    if (values.languages) {
      const result = await importLanguages({ from: path.resolve(values.from), workdir: values.workdir, env: ctx.env, home: ctx.home, log });
      if (result.missing.length) ctx.stdout.write(`  ticked on the panel, not in the folder (still working): ${result.missing.join(", ")}\n`);
      if (result.unticked.length) ctx.stdout.write(`  in the folder, not ticked (not sent): ${result.unticked.join(", ")}\n`);
      return ctx.EXIT.ok;
    }
    const result = await importLong({
      from: path.resolve(values.from),
      workdir: values.workdir,
      env: ctx.env,
      home: ctx.home,
      force: Boolean(values.force),
      log,
    });
    for (const problem of result.problems) ctx.stdout.write(`  ${problem}\n`);
    ctx.stdout.write(`${result.slug}: on /admin/videos, the final cut ${result.status === "pending" ? "waits for the owner" : result.status}\n`);
    return ctx.EXIT.ok;
  } catch (error) {
    if (error instanceof ToolMissing) {
      ctx.stderr.write(`${error.message}\n`);
      return ctx.EXIT.missing;
    }
    if (!(error instanceof SiteError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return error.who === "owner" ? ctx.EXIT.owner : ctx.EXIT.external;
  }
}
