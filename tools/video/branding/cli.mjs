// Install the owner's fixed media outside git. An installed default affects first builds only;
// existing unapproved cuts opt in through assemble/compile --adopt-branding. --pull fetches the
// package the site's worker builds with, so a machine without it (a cloud container) gets the same.
import { constants, copyFileSync, existsSync, mkdirSync, realpathSync, rmSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { verifyBrandingAssets } from "../assemble/branding.mjs";
import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { sha256File } from "../core/approvals.mjs";
import { currentBrandingFile, readCurrentBranding, validateBranding } from "../core/branding.mjs";
import { atomicWrite, isInside, readJson, resolveWorkBase, UsageError } from "../core/paths.mjs";
import { clientOptions, exitFor, requireCredentials } from "../media/cli.mjs";
import { brandingStatus, downloadBrandingFile, MediaError } from "../media/client.mjs";

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

export async function installPackage({ directory, workBase, series = null, dryRun = false, now = new Date(), tools, exec = runTool }) {
  const currentFile = path.join(workBase, currentBrandingFile(series));
  const currentDir = path.dirname(currentFile);
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
    current[role] = { ...clip, file: path.relative(currentDir, destination).split(path.sep).join("/") };
  }
  const before = readJson(currentFile, null);
  if (before) {
    const old = validateBranding(before, { base: currentDir });
    const historyId = old?.hash ?? "disabled";
    atomicWrite(path.join(currentDir, "history", `${now.toISOString().replace(/[:.]/g, "-")}-${historyId}.json`), `${JSON.stringify(before, null, 2)}\n`);
  }
  atomicWrite(currentFile, `${JSON.stringify(current, null, 2)}\n`);
  return { selection: readCurrentBranding(workBase, { series }), installed: true };
}

const SHA256 = /^[a-f0-9]{64}$/;

/**
 * Install the package the site's worker builds with (GET /api/video/media/branding): nothing when
 * this work directory already has it, else both files fetched by SHA-256 into a scratch package
 * and put through --install's checks. The worker's hash must come out of the files as well, or
 * nothing is installed. The scratch package is removed either way.
 */
export async function pullPackage({ workBase, series = null, dryRun = false, now = new Date(), tools, exec = runTool, client }) {
  const remote = await brandingStatus({ ...client, series });
  // The hash names a scratch folder that is deleted, and each SHA-256 goes into a URL.
  if (![remote?.hash, remote?.intro?.sha256, remote?.outro?.sha256].every((value) => SHA256.test(value ?? ""))) {
    throw new MediaError("the site's branding answer has no package hash or file SHA-256", { who: "tool" });
  }
  const local = readCurrentBranding(workBase, { series });
  if (local?.hash === remote.hash && existsSync(local.intro.file) && existsSync(local.outro.file)) {
    return { remote, selection: local, installed: false, current: true };
  }
  const directory = path.join(workBase, `_branding-pull-${remote.hash}`);
  rmSync(directory, { recursive: true, force: true });
  try {
    const assets = [];
    for (const role of ["intro", "outro"]) {
      const { sha256, frames } = remote[role];
      await downloadBrandingFile({ ...client, sha256, file: path.join(directory, `${role}.mp4`) });
      assets.push({ role, file: `${role}.mp4`, frames, sha256 });
    }
    atomicWrite(path.join(directory, "manifest.json"), `${JSON.stringify({ schema_version: 1, package_id: remote.id, assets }, null, 2)}\n`);
    const hash = packageSelection(directory).hash;
    if (hash !== remote.hash) throw new UsageError(`the site's package ${remote.id} is ${remote.hash.slice(0, 12)}, but its files hash to ${hash.slice(0, 12)}; nothing installed`);
    return { remote, ...(await installPackage({ directory, workBase, series, dryRun, now, tools, exec })), current: false };
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

export async function run(command, args, ctx) {
  const values = parseArgs({ args, options: { install: { type: "string" }, pull: { type: "boolean" }, series: { type: "string" }, workdir: { type: "string" }, "dry-run": { type: "boolean" }, json: { type: "boolean" } }, strict: true }).values;
  const series = values.series ?? null;
  currentBrandingFile(series);
  if (values.install && values.pull) throw new UsageError("branding takes --install DIR or --pull, not both");
  if (values["dry-run"] && !values.install && !values.pull) throw new UsageError("branding --dry-run needs --install DIR or --pull");
  const workBase = resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
  try {
    let result;
    if (values.install || values.pull) {
      const tools = await (ctx.ffmpeg?.locate ?? locateFfmpeg)(ctx.env);
      const options = { workBase, series, dryRun: values["dry-run"], now: ctx.now(), tools, exec: ctx.ffmpeg?.run ?? runTool };
      result = values.pull
        ? await pullPackage({ ...options, client: clientOptions(ctx, requireCredentials(ctx)) })
        : await installPackage({ ...options, directory: values.install });
    } else result = { selection: readCurrentBranding(workBase, { series }), installed: false };
    if (values.json) ctx.stdout.write(`${JSON.stringify({ work_base: workBase, series, ...result }, null, 2)}\n`);
    else if (!result.selection) ctx.stdout.write(`No ${series ?? "channel"} branding default is installed.\n`);
    else {
      const { selection } = result;
      if (result.current) ctx.stdout.write("The site's worker uses the same package.\n");
      const verb = result.current ? "Current" : values["dry-run"] ? "Validated" : result.installed ? "Installed" : "Current";
      ctx.stdout.write(`${verb}: ${selection.id} (${selection.hash})\n`);
      ctx.stdout.write(`intro ${selection.intro.frames / 30}s, outro ${selection.outro.frames / 30}s; first ${series ? `${series} ` : ""}long-video builds adopt this package.\n`);
      if (result.installed) ctx.stdout.write("Existing cuts keep their pinned choice; rebuild a selected unapproved cut with assemble/compile --adopt-branding.\n");
    }
    return ctx.EXIT.ok;
  } catch (error) {
    if (error instanceof ToolMissing) { ctx.stderr.write(`${error.message}\n`); return ctx.EXIT.missing; }
    if (error instanceof MediaError) { ctx.stderr.write(`branding --pull: ${error.message}\n`); return exitFor(error, ctx.EXIT); }
    throw error;
  }
}
