// Which saved narration takes still belong to the script: the rule `tts` synthesizes by, shared
// with the worker, which has to know before it asks for an evidence refresh.
import { existsSync } from "node:fs";
import path from "node:path";

import { readJson } from "../core/paths.mjs";
import { ARTIFACTS } from "../core/state.mjs";
import { planRequests } from "./requests.mjs";

export function readCache(workdir) {
  return readJson(path.join(workdir, ARTIFACTS.audio, "cache.json"), { lines: {} });
}

// A clip is current when its line's own key matches, or the key of the request it came from
// (caches written before clips had their own keys), and its WAV is still on disk.
export function takeCurrent(cache, workdir, request, line) {
  return [line.key, request.key].includes(cache.lines?.[line.id]) && existsSync(path.join(workdir, ARTIFACTS.audio, `${line.id}.wav`));
}

/** The lines whose saved take no longer matches what would be sent for synthesis today. The key
 * covers the request as sent, so a change to the channel's accent wording makes every older take
 * stale although the script, and with it the speech hash, did not change. */
export function staleTakes(doc, lexicon, workdir) {
  const cache = readCache(workdir);
  return planRequests(doc, lexicon)
    .filter((request) => !request.audio_ref)
    .flatMap((request) => request.lines.filter((line) => !takeCurrent(cache, workdir, request, line)).map((line) => line.id));
}
