// What to ask the narration server for: one request per scene, or per run of lines when a scene is
// longer than the server takes at once, with dictionary terms marked by their spoken forms.
import { createHash } from "node:crypto";

import { substitutions } from "../core/lexicon.mjs";
import { spokenText } from "../core/schema.mjs";
import { spokenUnits } from "../core/timeline.mjs";

// Mirrors MAX_REQUEST_CHARACTERS in apps/api/app/video_speech/admin_api.py.
export const MAX_REQUEST_CHARACTERS = 1500;
// The break between sentences inside one request: long enough to find, and trimmed away afterwards
// (the timeline adds each line's own pause).
export const SPLIT_BREAK_MS = 800;
const CJK = /[㐀-䶿一-鿿豈-﫿]/gu;

const escapeRegExp = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/**
 * The text as parts, with each dictionary term that has a spoken form carrying it as `alias`.
 * Terms match whole words only, longest first, so "Claude Code" wins over "Claude" and "API"
 * inside "APIs" is left alone.
 */
export function spokenParts(text, lexicon) {
  const entries = substitutions(lexicon);
  if (!entries.length) return [{ text }];
  const pattern = new RegExp(`(?<![A-Za-z0-9])(${entries.map(([term]) => escapeRegExp(term)).join("|")})(?![A-Za-z0-9])`, "gu");
  const spoken = new Map(entries);
  const parts = [];
  let last = 0;
  for (const match of text.matchAll(pattern)) {
    if (match.index > last) parts.push({ text: text.slice(last, match.index) });
    parts.push({ text: match[0], alias: spoken.get(match[0]) });
    last = match.index + match[0].length;
  }
  if (last < text.length) parts.push({ text: text.slice(last) });
  return parts;
}

const partsLength = (parts) => parts.reduce((sum, part) => sum + part.text.length, 0);

/** Every request for a video, in narration order. */
export function planRequests(doc, lexicon) {
  const requests = [];
  for (const scene of doc.scenes) {
    let chunk = [];
    let characters = 0;
    const flush = () => {
      if (!chunk.length) return;
      const segments = chunk.map((line, index) => ({ parts: line.parts, break_after_ms: index < chunk.length - 1 ? SPLIT_BREAK_MS : 0 }));
      const body = { voice: doc.voice.name, rate: doc.voice.rate ?? "+0%", segments };
      const key = createHash("sha256").update(JSON.stringify([chunk.map((line) => line.id), body])).digest("hex").slice(0, 16);
      requests.push({ id: `${scene.id}#${requests.filter((request) => request.scene === scene.id).length}`, scene: scene.id, lines: chunk, body, key });
      chunk = [];
      characters = 0;
    };
    for (const line of scene.lines) {
      const parts = spokenParts(spokenText(line), lexicon);
      const length = partsLength(parts);
      if (length > MAX_REQUEST_CHARACTERS) throw new Error(`line ${line.id} has ${length} characters; the server takes ${MAX_REQUEST_CHARACTERS} at once`);
      if (characters + length > MAX_REQUEST_CHARACTERS) flush();
      chunk.push({ id: line.id, parts, weight: Math.max(1, spokenUnits(spokenText(line))) });
      characters += length;
    }
    flush();
  }
  return requests;
}

/** Billable characters the server will count for a request: its SSML inside <voice>. */
export function billableForRequest(body) {
  let markup = 0;
  for (const segment of body.segments) {
    for (const part of segment.parts) {
      const text = part.text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      markup += part.alias ? `<sub alias="${part.alias}">${text}</sub>`.length + (part.alias.match(CJK)?.length ?? 0) : text.length;
      markup += text.match(CJK)?.length ?? 0;
    }
    if (segment.break_after_ms) markup += `<break time="${segment.break_after_ms}ms"/>`.length;
  }
  if (body.rate && !["+0%", "-0%"].includes(body.rate)) markup += `<prosody rate="${body.rate}"></prosody>`.length;
  if (!body.voice.startsWith("zh-TW-")) markup += '<lang xml:lang="zh-TW"></lang>'.length;
  return markup;
}
