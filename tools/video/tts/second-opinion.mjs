// A second, independent transcript for the lines check-audio still flags (docs/videos/DUBS.md).
//
// Gemini's transcriber pulls unfamiliar product versions, years and prices toward ones it knows,
// so a line can stay flagged through every retake while the voice says it right. A second
// transcriber that never sees the script (Whisper on the owner's machine or the worker, set with
// --second-opinion or VIDEO_SECOND_OPINION) settles it: a line is cleared when that transcript
// matches the script, or Jev passes it; when both transcripts miss the same words, the voice
// really said them wrong and the flag stays.
//
// The program runs once per check with the locale and every clip to recheck appended to its
// arguments, and prints one line per clip: "<clip file name> <transcript>".
import { execFile } from "node:child_process";
import path from "node:path";
import { promisify } from "node:util";

export const SECOND_OPINION_ENV = "VIDEO_SECOND_OPINION";
const TIMEOUT_MS = 30 * 60 * 1000;

/** The program and its arguments from the flag or the environment, split on spaces; null when unset. */
export function secondOpinionCommand(flag, env = {}) {
  const value = String(flag ?? env[SECOND_OPINION_ENV] ?? "").trim();
  return value ? value.split(/\s+/) : null;
}

/** How the check and the review card name the transcriber: its script's file name, else the program's. */
export function secondOpinionName(command) {
  const script = command.slice(1).find((arg) => /\.(py|mjs|js|sh)$/i.test(arg));
  return path.basename(script ?? command[0]);
}

/** The transcript of each clip, keyed by the clip's file name; clips the program printed nothing for are left out. */
export async function secondTranscripts(command, locale, files, { run = promisify(execFile) } = {}) {
  const [program, ...args] = command;
  const { stdout } = await run(program, [...args, locale, ...files], { maxBuffer: 16 * 1024 * 1024, timeout: TIMEOUT_MS, windowsHide: true });
  const wanted = new Set(files.map((file) => path.basename(file)));
  const heard = new Map();
  for (const line of String(stdout).split(/\r?\n/)) {
    const match = /^(\S+)\s+(.+)$/.exec(line.trim());
    if (match && wanted.has(match[1])) heard.set(match[1], match[2].trim());
  }
  return heard;
}
