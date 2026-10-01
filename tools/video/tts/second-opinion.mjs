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
export const SECOND_OPINION_TIMEOUT_ENV = `${SECOND_OPINION_ENV}_TIMEOUT_MS`;
// The whole batch shares one time limit: a base for starting the program and loading its model,
// plus an allowance per clip. Whisper medium on a slow Windows ARM64 machine takes about a minute
// a clip, so two minutes a clip leaves room; VIDEO_SECOND_OPINION_TIMEOUT_MS (milliseconds) sets
// the whole limit on a machine that needs more or less.
export const TIMEOUT_BASE_MS = 10 * 60 * 1000;
export const TIMEOUT_PER_CLIP_MS = 2 * 60 * 1000;

/** The time limit for one run over `clips` clips: the environment's value, else base plus per clip. */
export function secondOpinionTimeout(clips, env = {}) {
  const raw = String(env[SECOND_OPINION_TIMEOUT_ENV] ?? "").trim();
  if (!raw) return TIMEOUT_BASE_MS + TIMEOUT_PER_CLIP_MS * clips;
  const value = Number(raw);
  if (!Number.isInteger(value) || value <= 0) throw new Error(`${SECOND_OPINION_TIMEOUT_ENV} must be a positive whole number of milliseconds, not "${raw}"`);
  return value;
}

function duration(ms) {
  return ms < 60000 ? `${Number((ms / 1000).toFixed(1))} s` : `${Number((ms / 60000).toFixed(1))} min`;
}

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

/**
 * The transcript of each clip, keyed by the clip's file name; clips the program printed nothing for
 * are left out. `hints` names the file (JSON, { "<clip file name>": ["Veo", ...] }) with the English
 * words each line says, the same hints Gemini gets; the program finds it in VIDEO_SECOND_OPINION_HINTS
 * and may use it for spelling. The script itself is never passed. A run that outlives its time limit
 * (secondOpinionTimeout) is killed, and the error says so with the clip count and the limit.
 */
export async function secondTranscripts(command, locale, files, { run = promisify(execFile), hints = null, env = process.env } = {}) {
  const [program, ...args] = command;
  const childEnv = hints ? { ...env, [`${SECOND_OPINION_ENV}_HINTS`]: hints } : env;
  const timeout = secondOpinionTimeout(files.length, env);
  let stdout;
  try {
    ({ stdout } = await run(program, [...args, locale, ...files], { maxBuffer: 16 * 1024 * 1024, timeout, windowsHide: true, env: childEnv }));
  } catch (error) {
    // execFile kills the child on its timeout and on a full output buffer; only the first is a timeout.
    if (error?.killed && error.code !== "ERR_CHILD_PROCESS_STDIO_MAXBUFFER") {
      throw new Error(
        `timed out after ${duration(timeout)} on ${files.length} clip${files.length === 1 ? "" : "s"}; ` +
          `set ${SECOND_OPINION_TIMEOUT_ENV} or a smaller WHISPER_MODEL, and run one check-audio at a time`,
        { cause: error },
      );
    }
    throw error;
  }
  const wanted = new Set(files.map((file) => path.basename(file)));
  const heard = new Map();
  for (const line of String(stdout).split(/\r?\n/)) {
    const match = /^(\S+)\s+(.+)$/.exec(line.trim());
    if (match && wanted.has(match[1])) heard.set(match[1], match[2].trim());
  }
  return heard;
}
