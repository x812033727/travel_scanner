// Offline audition planning only. A plan is not speech, a listening receipt or approval.
import { castFrom } from "../automation/series.mjs";
import { voiceFor } from "../core/drama.mjs";
import { designHash, productionSetting } from "./design.mjs";

export const CALIBRATION_SAMPLES = [
  { id: "controlled", direction: "平靜對峙；有對手、先吸氣再說，語尾收住", line: "我聽清楚了。你先別急，把話說完。" },
  { id: "quiet", direction: "近距離低聲；氣息清楚、低音量但不含糊", line: "先別出聲。看著我，跟著我走。" },
  { id: "turn", direction: "情緒反轉；先忍住再作決定，不嘶吼、不破音", line: "這一次，我不會再讓你替我作決定。" },
];
const unique = (items) => [...new Set(items)];
const accept = ["人名正確", "聲線可辨識且符合角色", "狀態改變仍為同一人", "低聲仍清晰", "無破音與多餘字", "指示與原文敘述沒有被唸出"];
const sourceField = (episode, field) => {
  if (!["hook", "conflict", "turn", "cliffhanger.text"].includes(field)) throw new Error(`unsupported audition source field: ${field}`);
  return field === "cliffhanger.text" ? episode.cliffhanger?.text : episode[field];
};

/**
 * Pure, deterministic plan for the CLI to write. Never extracts quoted prose into speech:
 * source_excerpt is context only, and story lines require a separately attributed line_sample.
 * The caller writes entry.transcript to entry.id.txt and may later request an audition explicitly.
 */
export function buildAuditionPlan(work, profile) {
  const { source, design } = work;
  const sourceHash = designHash(source);
  if (design.source_binding?.source_sha256 !== sourceHash) throw new Error("audition source binding mismatch");
  const binding = { source_sha256: sourceHash, design_sha256: designHash(design), profile_sha256: designHash(profile) };
  const original = JSON.parse(work.files["documents.json"]).documents.find((document) => document.kind === "setting");
  if (!original) throw new Error("audition plan needs the compiled setting document");
  const setting = productionSetting(original, design, profile).body_json;
  const episodes = source.chapters.flatMap((chapter) => chapter.episodes);
  const byEpisode = new Map(episodes.map((episode) => [episode.number, episode]));
  const plans = new Map(design.episodes.map((episode) => [episode.episode, episode]));
  const baseCast = new Map(castFrom(setting).map((character) => [character.id, character]));
  const episodeCast = new Map(episodes.map((episode) => [episode.number, new Map(castFrom(setting, episode.number)
    .filter((character) => episode.characters.includes(character.id)).map((character) => [character.id, character]))]));
  const narrator = setting.production_design.narrator;
  const narratorCast = { id: "narrator", name: "旁白", voice: { provider: "gemini", name: narrator.voice_name, style: `台灣國語，自然台灣口音；${narrator.performance}` } };
  const entries = [];
  const add = ({ id, kind, actor, numbers = [], transcript, refs, direction = "", context = {}, hint = "", ...rest }) => {
    if (!refs?.length) throw new Error(`${id}: missing audition source references`);
    const line = { id, speaker: actor.id, text: transcript, emotion: direction };
    const auditionVoice = voiceFor({ pronunciation_hints: setting.lexicon ?? {}, characters: [actor], voice: actor.voice }, line);
    if ((auditionVoice.style ?? "").length > 400) throw new Error(`${id}: audition direction exceeds 400 characters`);
    entries.push({
      id, kind, character: actor.id, voice: actor.voice.name, provider: actor.voice.provider,
      effective_style: actor.voice.style ?? "", episodes: numbers, transcript: `${transcript.trim()}\n`,
      audition_style: auditionVoice.style ?? "", synthesis_allowed: true,
      text_sha256: designHash(`${transcript.trim()}\n`), pronunciation_hint: hint,
      direction, context, source_refs: unique(refs), source_binding: binding,
      status: "not-synthesized", accept, ...rest,
    });
  };
  const actors = [...design.characters.map((direction) => ({ direction, actor: baseCast.get(direction.id) })),
    { direction: { id: "narrator", pronunciations: { "zh-TW": "" }, look_states: [] }, actor: narratorCast }];
  for (const { direction, actor } of actors) {
    if (!actor?.voice) throw new Error(`${direction.id}: missing effective audition voice`);
    const appearances = episodes.filter((episode) => actor.id === "narrator" || episode.characters.includes(actor.id)).map((episode) => episode.number);
    const refs = direction.look_states?.flatMap((look) => look.source_refs ?? []) ?? [];
    const baseRefs = refs.length ? refs : plans.get(appearances[0])?.source_refs;
    const hint = direction.pronunciations?.["zh-TW"] ?? "";
    for (const sample of CALIBRATION_SAMPLES) add({ id: `${actor.id}-${sample.id}`, kind: "calibration", actor,
      transcript: `${actor.name}。${sample.line}`, refs: baseRefs, direction: sample.direction, hint,
      delivery_scope: "offscreen-calibration-not-story",
      purpose: "non-story calibration; these words are not added to an episode" });
    if (actor.id !== "narrator") add({ id: `${actor.id}-name`, kind: "pronunciation", actor,
      transcript: `${actor.name}。`, refs: baseRefs, hint,
      purpose: "isolated name pronunciation calibration, not character dialogue" });

    // Group only episodes in which the actor is actually credited. Clothing alone does not
    // create a voice state, while source looks.voice_style overrides must remain audible here.
    const states = new Map();
    for (const number of appearances) {
      const effective = actor.id === "narrator" ? narratorCast : episodeCast.get(number).get(actor.id);
      const key = JSON.stringify(effective.voice);
      if (!states.has(key)) states.set(key, { actor: effective, numbers: [] });
      states.get(key).numbers.push(number);
    }
    let index = 0;
    for (const state of states.values()) {
      const stateDirections = (direction.performance_states ?? []).filter((entry) => entry.episodes.some((number) => state.numbers.includes(number)));
      add({ id: `${actor.id}-state-${++index}`, kind: "effective-voice-state", actor: state.actor, numbers: state.numbers,
        transcript: CALIBRATION_SAMPLES[0].line, refs: state.numbers.flatMap((number) => plans.get(number)?.source_refs ?? []), hint,
        direction: "先比較同一角色各集實際聲線；逐鏡演技指示列在 context，不能把不同場景的指示一口氣疊上。",
        context: { performance_states: stateDirections },
        purpose: "non-story calibration of the effective productionSetting + castFrom voice; no episode dialogue is invented" });
    }
    for (const performance of direction.performance_states ?? []) {
      const number = performance.episodes.find((number) => appearances.includes(number));
      if (number === undefined) throw new Error(`${performance.id}: performance state has no credited episode`);
      const effective = episodeCast.get(number).get(actor.id);
      const id = `${actor.id}-performance-${performance.id}`;
      const stateContext = { performance_state: performance, selected_episode: number };
      if (performance.speech_mode === "nonverbal") {
        entries.push({ id, kind: "nonverbal-performance-check", character: actor.id, voice: effective.voice.name,
          provider: effective.voice.provider, effective_style: effective.voice.style ?? "", audition_style: null,
          episodes: performance.episodes, transcript: null, synthesis_allowed: false, status: "not-synthesized",
          context: stateContext, source_refs: performance.source_refs, source_binding: binding,
          purpose: "Breath, silence and written-word narrator routing review; do not send invented speech to TTS.",
          accept: ["角色無可辨詞", "字義由指定旁白讀出", "呼吸不構成新台詞"] });
      } else add({ id, kind: "performance-state-calibration", actor: effective, numbers: performance.episodes,
        transcript: CALIBRATION_SAMPLES[0].line, refs: performance.source_refs, hint,
        direction: `${performance.cue}；${performance.instructions.find((instruction) => !instruction.startsWith("source_excerpt")) ?? performance.cue}`, context: stateContext,
        delivery_scope: "offscreen-calibration-not-story",
        purpose: "Non-story acting comparison for one proposed state; never insert the calibration line into the episode." });
    }
  }

  // Aliases and clue terms need their own executable pronunciation samples too.
  // The source reference is the exact dictionary field in the hash-bound source object.
  const actorNames = new Set(setting.characters.map((actor) => actor.name));
  for (const [term, reading] of Object.entries(setting.lexicon ?? {})) {
    if (!reading || actorNames.has(term)) continue;
    add({ id: `term-${designHash(term).slice(0, 12)}`, kind: "pronunciation-term", actor: narratorCast,
      transcript: `${term}。`, refs: [`${work.slug}:source.setting.lexicon[${JSON.stringify(term)}]`],
      direction: "單獨確認詞語讀音，不加說明或解釋。", hint: reading,
      context: { source_field: `setting.lexicon.${term}`, canonical_reading: reading },
      delivery_scope: "offscreen-calibration-not-story",
      purpose: "Isolated canonical alias or clue-term pronunciation, not added narration." });
  }

  const scenes = (design.audio_plan.audition_scenes ?? []).map((scene) => {
    const episode = byEpisode.get(scene.episode);
    if (!episode) throw new Error(`${scene.id}: unknown audition episode`);
    const voices = scene.speaker_ids.map((id) => {
      const actor = id === "narrator" ? narratorCast : episodeCast.get(scene.episode).get(id);
      if (!actor) throw new Error(`${scene.id}: speaker ${id} is not in episode ${scene.episode}`);
      return { character: id, voice: actor.voice.name, effective_style: actor.voice.style ?? "" };
    });
    const entryIds = [];
    for (const [index, sample] of (scene.line_samples ?? []).entries()) {
      // Narrative and written evidence may contain quotes. Requiring explicit dialogue
      // attribution prevents a narrator, palm-written word or letter from acquiring an actor.
      if (sample.source_kind !== "dialogue" || sample.speaker === "narrator") throw new Error(`${scene.id}: story samples need explicitly attributed character dialogue`);
      if (!scene.speaker_ids.includes(sample.speaker)) throw new Error(`${scene.id}: line speaker is outside audition scene`);
      const field = sourceField(episode, sample.source_field);
      if (typeof sample.text !== "string" || !sample.text.trim() || typeof field !== "string" || !field.includes(sample.text)) throw new Error(`${scene.id}: line is not verbatim in its source field`);
      const actor = episodeCast.get(scene.episode).get(sample.speaker);
      const character = design.characters.find((entry) => entry.id === sample.speaker);
      const id = `${scene.id}-line-${index + 1}`;
      add({ id, kind: "story-excerpt", actor, numbers: [scene.episode], transcript: sample.text,
        refs: sample.source_refs ?? scene.source_refs, hint: character.pronunciations["zh-TW"],
        direction: scene.instructions.join("；"), context: { source_excerpt: scene.source_excerpt, source_field: sample.source_field, attribution: "explicitly-reviewed-dialogue" },
        purpose: "verbatim attributed story dialogue for this audition; preserve source speaker and reveal order" });
      entryIds.push(id);
    }
    return { ...scene, status: "not-synthesized", source_binding: binding, voices, entry_ids: entryIds,
      material_kind: entryIds.length ? "attributed-story-excerpts" : "context-only-no-story-transcript",
      fallback: entryIds.length ? null : "Use the separate controlled/quiet/turn calibration entries; source_excerpt is not a TTS transcript." };
  });
  const cues = (design.audio_plan.audio_cues ?? []).map((cue) => ({ ...cue,
    status: "not-synthesized", source_binding: binding, material_kind: "sound-direction-only-not-tts-text" }));
  return { schema_version: 1, slug: work.slug, locale: "zh-TW", status: "samples-prepared-not-synthesized",
    source_binding: binding, generation_performed: false, audition_performed: false, approval_granted: false,
    entries, scenes, cues };
}
