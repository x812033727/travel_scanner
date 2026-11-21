// Every actual assembly through this batch's wrapper must verify both formal bookends.
import { readFileSync, realpathSync } from "node:fs";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const here = path.dirname(fileURLToPath(import.meta.url));

export function requiredAssemblyArguments(root, args, { runPreflight = spawnSync } = {}) {
  const required = JSON.parse(readFileSync(path.join(here, "required-branding.json"), "utf8"));
  const { values } = parseArgs({
    args, strict: true, allowPositionals: false,
    options: {
      slug: { type: "string" }, workdir: { type: "string" },
      force: { type: "boolean" },
      "adopt-branding": { type: "boolean" }, "intro-after-condensation": { type: "boolean" },
    },
  });
  if (!values.slug || !/^story-[a-z0-9-]+-remake-20261025$/.test(values.slug)) {
    throw new Error("Assembly requires this batch's exact remake slug.");
  }
  if (values.workdir && path.resolve(values.workdir) !== required.media_base) {
    throw new Error("Assembly workdir must match the verified branding media base.");
  }
  const preflightArgs = [
    path.join(here, "preflight.mjs"), "--project-root", root, "--slug", values.slug,
    ...(values["adopt-branding"] ? ["--adopt-branding"] : []),
  ];
  const checked = runPreflight(process.execPath, preflightArgs, {
    encoding: "utf8", env: { ...process.env, NODE_USE_ENV_PROXY: "1" },
    maxBuffer: 1024 * 1024,
  });
  if (checked.error || checked.status !== 0) {
    throw new Error(`Required branding preflight failed; assembly was not invoked. ${checked.error?.message || checked.stderr || checked.stdout || ""}`);
  }
  const report = JSON.parse(checked.stdout), canonicalRoot = realpathSync(root);
  const projectDirectory = path.join(canonicalRoot, "docs", "videos", values.slug);
  const hash = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");
  const same = (actual, expected, field) => {
    if (actual !== expected) throw new Error(`Required branding preflight proof mismatch: ${field}`);
  };
  same(report.passed, true, "passed");
  for (const [field, expected] of Object.entries({
    root: canonicalRoot, slug: values.slug, selector: null,
    intro_at: required.intro_at, selected_hash: required.placed_hash,
    adopt_current: Boolean(values["adopt-branding"]),
    source_sha256: hash(path.join(projectDirectory, "video.json")),
    series_sha256: hash(path.join(projectDirectory, "series.json")),
  })) same(report.project?.[field], expected, `project.${field}`);
  for (const [field, expected] of Object.entries({
    id: required.id, hash: required.package_hash, media_base: required.media_base,
  })) same(report.package?.[field], expected, `package.${field}`);
  for (const role of ["intro", "outro"]) {
    for (const field of ["sha256", "frames", "size"]) {
      same(report.package?.[role]?.[field], required[role][field], `package.${role}.${field}`);
    }
  }
  return [
    ...args,
    ...(!values.workdir ? ["--workdir", required.media_base] : []),
    ...(!values["intro-after-condensation"] ? ["--intro-after-condensation"] : []),
  ];
}
