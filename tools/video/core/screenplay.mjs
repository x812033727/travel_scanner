// The screenplay the owner reads before any image or clip is paid for (docs/videos/SERIES.md):
// docs/videos/<slug>/script.md, written from video.json. It holds the narrative only (the
// scenes in order, every line with its speaker and emotion, the cast), never the shot prompts:
// the script gate is bound to this file's hash, and the automatic prompt fixes of the look,
// keyframe and clip stages must not unsettle an approval the owner already gave. An explicit
// anime silent action is narrative: its pictured action, motion and seconds are approved too. The prompts go
// to the review page beside the lines, from `scriptScenes`.
import { createHash } from "node:crypto";
import { writeFileSync } from "node:fs";
import path from "node:path";

import { isAnimeAction } from "./anime-policy.mjs";
import { characterOf, isShot, NARRATOR } from "./drama.mjs";
import { speechHash } from "./timeline.mjs";

export const SCRIPT_FILE = "script.md";

const hash16 = (value) => createHash("sha256").update(JSON.stringify(value)).digest("hex").slice(0, 16);

/** What the owner approves: the cast's names and every line's text, speaker and emotion, in order. */
export function narrativeHash(doc) {
  return hash16({
    characters: (doc.characters ?? []).map((character) => [character.id, character.name]),
    scenes: (doc.scenes ?? []).map((scene) => [
      scene.id,
      scene.chapter ?? null,
      scene.template,
      (scene.lines ?? []).map((line) => [line.id, line.text, line.speaker ?? NARRATOR, line.emotion ?? null]),
      ...(isAnimeAction(doc, scene) ? [actionOf(doc, scene)] : []),
    ]),
  });
}

const actionOf = (doc, scene) => isAnimeAction(doc, scene) ? {
  description: scene.data?.prompt ?? "",
  motion: scene.data?.motion ?? "",
  seconds: scene.action_seconds,
} : null;

const speakerName = (doc, line) => characterOf(doc, line)?.name ?? null;

/** The scenes for the review page: the lines with their speakers, and a shot's prompt beside them. */
export function scriptScenes(doc) {
  return (doc.scenes ?? []).map((scene) => ({
    id: scene.id,
    chapter: scene.chapter ?? null,
    template: scene.template,
    prompt: isShot(scene) ? scene.data?.prompt ?? "" : null,
    ...(isAnimeAction(doc, scene) ? { action: actionOf(doc, scene) } : {}),
    lines: (scene.lines ?? []).map((line) => ({
      id: line.id,
      speaker: line.speaker ?? NARRATOR,
      name: speakerName(doc, line),
      text: line.text,
      emotion: line.emotion ?? null,
    })),
  }));
}

/** script.md: the screenplay as text, deterministic, the narrative only. */
export function screenplay(doc) {
  const title = doc.youtube?.title || doc.slug || "";
  const out = [`# ${title}`, ""];
  if (doc.series) out.push(`作品 ${doc.series.slug} · 第 ${doc.series.episode} 集（第 ${doc.series.chapter} 篇）`, "");
  const cast = doc.characters ?? [];
  if (cast.length) {
    out.push("## 角色", "");
    for (const character of cast) out.push(`- ${character.name}（${character.id}）${character.voice?.name ? `，聲音 ${character.voice.provider}:${character.voice.name}` : ""}`);
    out.push("");
  }
  out.push("## 場景", "");
  let chapter = null;
  (doc.scenes ?? []).forEach((scene, index) => {
    if (scene.chapter && scene.chapter !== chapter) {
      chapter = scene.chapter;
      out.push(`### ${chapter}`, "");
    }
    out.push(`#### ${index + 1}. ${scene.id}${isShot(scene) ? "" : `（${scene.template}）`}`, "");
    const action = actionOf(doc, scene);
    if (action) out.push(`無台詞動作（${action.seconds} 秒）：${action.description}`, `動作：${action.motion}`, "");
    for (const line of scene.lines ?? []) {
      const name = speakerName(doc, line);
      const emotion = line.emotion ? `（${line.emotion}）` : "";
      out.push(name ? `【${name}】${emotion}${line.text}` : `旁白${emotion}：${line.text}`);
    }
    out.push("");
  });
  // Pronunciation overrides and pauses affect the checked story/timing even when
  // the displayed lines do not change. Their approval must also be renewed.
  out.push(`narrative ${narrativeHash(doc)}`, `speech ${speechHash(doc, null)}`, "");
  return out.join("\n");
}

/** Write docs/videos/<slug>/script.md and return its path. */
export function writeScreenplay(dir, doc) {
  const file = path.join(dir, SCRIPT_FILE);
  writeFileSync(file, screenplay(doc));
  return file;
}
