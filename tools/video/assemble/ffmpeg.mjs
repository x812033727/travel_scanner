// Finding and running ffmpeg / ffprobe.
//
// FFMPEG_PATH names the ffmpeg executable (or the directory holding it); otherwise PATH is tried,
// then, on Windows, the folder `winget install BtbN.FFmpeg.GPL` unpacks to, because a shell
// opened before the install does not see the new PATH yet. Playwright's bundled ffmpeg is never
// used: it is built for VP8 screencasts and has no libx264.
import { execFile } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";

const run = promisify(execFile);
const EXE = process.platform === "win32" ? ".exe" : "";

export class ToolMissing extends Error {}

function wingetCandidates(env) {
  const base = env.LOCALAPPDATA && path.join(env.LOCALAPPDATA, "Microsoft", "WinGet", "Packages");
  if (!base || !existsSync(base)) return [];
  return readdirSync(base)
    .filter((name) => name.startsWith("BtbN.FFmpeg"))
    .flatMap((name) => {
      const packageDir = path.join(base, name);
      return readdirSync(packageDir).map((inner) => path.join(packageDir, inner, "bin"));
    });
}

/** The ffmpeg and ffprobe to use, or ToolMissing with how to install them. */
export async function locateFfmpeg(env = process.env) {
  const candidates = [];
  if (env.FFMPEG_PATH) {
    const given = env.FFMPEG_PATH;
    candidates.push(existsSync(given) && !given.toLowerCase().endsWith(`ffmpeg${EXE}`) ? given : path.dirname(given));
  }
  candidates.push(null); // PATH
  if (process.platform === "win32") candidates.push(...wingetCandidates(env));
  for (const dir of candidates) {
    const ffmpeg = dir ? path.join(dir, `ffmpeg${EXE}`) : "ffmpeg";
    const ffprobe = dir ? path.join(dir, `ffprobe${EXE}`) : "ffprobe";
    if (dir && !existsSync(ffmpeg)) continue;
    try {
      const { stdout } = await run(ffmpeg, ["-hide_banner", "-encoders"], { maxBuffer: 8 * 1024 * 1024 });
      if (!/\blibx264\b/.test(stdout)) continue;
      const version = (await run(ffmpeg, ["-hide_banner", "-version"])).stdout.split("\n")[0].trim();
      return { ffmpeg, ffprobe, version };
    } catch {
      // Not here; try the next place.
    }
  }
  throw new ToolMissing(
    "ffmpeg with libx264 was not found: install it (Windows: winget install BtbN.FFmpeg.GPL; Ubuntu: apt-get install ffmpeg) or set FFMPEG_PATH",
  );
}

/** Run a tool and return stdout and stderr; failures carry the last lines of stderr. */
export async function runTool(file, args, { cwd } = {}) {
  try {
    return await run(file, args, { cwd, maxBuffer: 64 * 1024 * 1024, windowsHide: true });
  } catch (error) {
    const tail = String(error.stderr ?? "").trim().split("\n").slice(-6).join("\n");
    throw new Error(`${path.basename(file)} failed: ${tail || error.message}`);
  }
}
