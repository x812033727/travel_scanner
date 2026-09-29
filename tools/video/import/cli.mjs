// `import`: a long video finished by another tool, sent to /admin/videos (import.mjs).
import path from "node:path";
import { parseArgs } from "node:util";

import { ToolMissing } from "../assemble/ffmpeg.mjs";
import { UsageError } from "../core/paths.mjs";
import { SiteError } from "../shorts/site.mjs";
import { importLong } from "./import.mjs";

export async function run(_command, args, ctx) {
  const values = parseArgs({ args, options: { from: { type: "string" }, workdir: { type: "string" }, force: { type: "boolean" } }, strict: true }).values;
  if (!values.from) throw new UsageError("import needs --from DIR holding final.mp4 and meta.json (zh-TW.srt and thumbnail.png are optional)");
  try {
    const result = await importLong({
      from: path.resolve(values.from),
      workdir: values.workdir,
      env: ctx.env,
      home: ctx.home,
      force: Boolean(values.force),
      log: (line) => ctx.stdout.write(`${line}\n`),
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
