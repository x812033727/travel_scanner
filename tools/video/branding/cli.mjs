// Install the owner's fixed media outside git. An installed default affects first builds only;
// existing unapproved cuts opt in through assemble/compile --adopt-branding.
import { constants, copyFileSync, existsSync, mkdirSync, realpathSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { verifyBrandingAssets } from "../assemble/branding.mjs";
import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { sha256File } from "../core/approvals.mjs";
import { CURRENT_BRANDING_FILE, readCurrentBranding, validateBranding } from "../core/branding.mjs";
import { atomicWrite, isInside, readJson, resolveWorkBase, UsageError } from "../core/paths.mjs";

/** Read a selected package without trusting the descriptive/provenance fields as media proof. */
export function packageSelection(directory) {
  const base = realpathSync(path.resolve(directory));
  const manifest = readJson(path.join(base, "manifest.json"));
  const selected = { schema_version: manifest.schema_version, id: manifest.package_id ?? manifest.id };
  for (const role of ["intro", "outro"]) {
    const clip = Array.isArray(manifest.assets) ? manifest.assets.find((asset) => asset.role === role) : manifest[role];
    if (!clip || typeof clip.file !== "string") throw new UsageError(`package has no ${role} file`);
    const file = path.resolve(base, clip.file);
    if (!isInside(file, base) || !existsSync(file) || !isInside(realpathSync(file), base)) throw new UsageError(`package ${role} must be a file inside the package directory`);
    selected[role] = { file, sha256: String(clip.sha256 ?? "").toLowerCase(), frames: clip.frames };
  }
  return validateBranding(selected);
}

export async function installPackage({ directory, workBase, dryRun = false, now = new Date(), tools, exec = runTool }) {
  const selection = packageSelection(directory);
  await verifyBrandingAssets(selection, { tools, exec });
  if (dryRun) return { selection, installed: false };
  const brandingDir = path.join(workBase, "_branding");
  const packageDir = path.join(brandingDir, selection.hash);
  mkdirSync(packageDir, { recursive: true });
  const current = { schema_version: 1, id: selection.id, hash: selection.hash, installed_at: now.toISOString() };
  for (const role of ["intro", "outro"]) {
    const clip = selection[role];
    const destination = path.join(packageDir, `${role}.mp4`);
    if (!existsSync(destination)) copyFileSync(clip.file, destination, constants.COPYFILE_EXCL);
    if (await sha256File(destination) !== clip.sha256) throw new UsageError(`installed ${role} hash differs; refusing to overwrite immutable branding assets`);
    current[role] = { ...clip, file: `${selection.hash}/${role}.mp4` };
  }
  const currentFile = path.join(workBase, CURRENT_BRANDING_FILE);
  const before = readJson(currentFile, null);
  if (before) {
    const old = validateBranding(before, { base: brandingDir });
    const historyId = old?.hash ?? "disabled";
    atomicWrite(path.join(brandingDir, "history", `${now.toISOString().replace(/[:.]/g, "-")}-${historyId}.json`), `${JSON.stringify(before, null, 2)}\n`);
  }
  atomicWrite(currentFile, `${JSON.stringify(current, null, 2)}\n`);
  return { selection: readCurrentBranding(workBase), installed: true };
}

export async function run(command, args, ctx) {
  const values = parseArgs({ args, options: { install: { type: "string" }, workdir: { type: "string" }, "dry-run": { type: "boolean" }, json: { type: "boolean" } }, strict: true }).values;
  if (values["dry-run"] && !values.install) throw new UsageError("branding --dry-run needs --install DIR");
  const workBase = resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
  try {
    let result;
    if (values.install) {
      const tools = await (ctx.ffmpeg?.locate ?? locateFfmpeg)(ctx.env);
      result = await installPackage({ directory: values.install, workBase, dryRun: values["dry-run"], now: ctx.now(), tools, exec: ctx.ffmpeg?.run ?? runTool });
    } else result = { selection: readCurrentBranding(workBase), installed: false };
    if (values.json) ctx.stdout.write(`${JSON.stringify({ work_base: workBase, ...result }, null, 2)}\n`);
    else if (!result.selection) ctx.stdout.write("No channel branding default is installed.\n");
    else {
      const { selection } = result;
      ctx.stdout.write(`${values["dry-run"] ? "Validated" : result.installed ? "Installed" : "Current"}: ${selection.id} (${selection.hash})\n`);
      ctx.stdout.write(`intro ${selection.intro.frames / 30}s, outro ${selection.outro.frames / 30}s; first long-video builds adopt this package.\n`);
      if (result.installed) ctx.stdout.write("Existing cuts keep their pinned choice; rebuild a selected unapproved cut with assemble/compile --adopt-branding.\n");
    }
    return ctx.EXIT.ok;
  } catch (error) {
    if (error instanceof ToolMissing) { ctx.stderr.write(`${error.message}\n`); return ctx.EXIT.missing; }
    throw error;
  }
}
