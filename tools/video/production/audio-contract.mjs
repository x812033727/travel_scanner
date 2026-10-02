// Validate authoring evidence, not audio quality. These cues remain unrendered.
const text = (value) => typeof value === "string" && value.trim().length > 0;
const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const strings = (value) => Array.isArray(value) && value.every(text);
const array = (value) => Array.isArray(value) ? value : [];

export function audioDetailProblems(design, source) {
  const errors = [];
  const episodes = new Map(source.chapters.flatMap((chapter) => chapter.episodes).map((entry) => [entry.number, entry]));
  const cast = new Set(source.setting.characters.map((entry) => entry.id));
  const knownSpeakers = new Set([...cast, "narrator"]);
  const validate = (entry, where, numbers) => {
    if (!object(entry)) { errors.push(`${where}: must be an object`); return false; }
    if (!text(entry.id) || entry.status !== "proposed") errors.push(`${where}: a named proposed cue is required; no audio acceptance granted`);
    if (!Array.isArray(numbers) || !numbers.length || numbers.some((number) => !episodes.has(number))) errors.push(`${where}: unknown or missing episode`);
    if (!text(entry.source_excerpt) || !strings(entry.source_refs) || !entry.source_refs.length) errors.push(`${where}: missing source evidence`);
    if (!strings(entry.instructions) || !entry.instructions.length) errors.push(`${where}: missing playable instructions`);
    return true;
  };
  for (const character of array(design.characters)) {
    if (!object(character)) continue;
    if (character.performance_states !== undefined && !Array.isArray(character.performance_states)) errors.push(`${character.id}: performance_states must be an array`);
    const ids = new Set();
    for (const state of array(character.performance_states)) {
      const where = `${character.id}/performance_state`;
      if (!validate(state, where, state?.episodes)) continue;
      if (ids.has(state.id)) errors.push(`${where}: duplicate state ${state.id}`);
      ids.add(state.id);
      if (!text(state.cue)) errors.push(`${where}: missing performance switching cue`);
      if (state.speech_mode !== undefined && state.speech_mode !== "nonverbal") errors.push(`${where}: speech_mode must be omitted for speech or set to nonverbal`);
      if (array(state.episodes).some((number) => !episodes.get(number)?.characters.includes(character.id))) errors.push(`${where}: state outside the character's source appearances`);
    }
  }
  for (const key of ["audio_cues", "audition_scenes"]) {
    if (design.audio_plan?.[key] !== undefined && !Array.isArray(design.audio_plan[key])) errors.push(`audio_plan.${key}: must be an array`);
    const ids = new Set();
    for (const entry of array(design.audio_plan?.[key])) {
      const where = `audio_plan.${key}`;
      if (!validate(entry, where, key === "audition_scenes" ? [entry?.episode] : entry?.episodes)) continue;
      if (ids.has(entry.id)) errors.push(`${where}: duplicate cue ${entry.id}`);
      ids.add(entry.id);
      if (!strings(entry.speaker_ids) || entry.speaker_ids.some((id) => !knownSpeakers.has(id))) errors.push(`${where}/${entry.id}: unknown speaker`);
      if (key === "audio_cues" && !["dialogue", "recording", "message-read", "foley", "effect"].includes(entry.source_kind)) errors.push(`${where}/${entry.id}: unknown sound source kind`);
      if (key === "audition_scenes" && (!strings(entry.acceptance) || !entry.acceptance.length)) errors.push(`${where}/${entry.id}: missing listening acceptance`);
      if (entry.line_samples !== undefined && !Array.isArray(entry.line_samples)) errors.push(`${where}/${entry.id}: line_samples must be an array`);
      for (const sample of array(entry.line_samples)) {
        const episode = episodes.get(entry.episode);
        const fields = { hook: episode?.hook, turn: episode?.turn, conflict: episode?.conflict, "cliffhanger.text": episode?.cliffhanger?.text };
        if (!object(sample) || !array(entry.speaker_ids).includes(sample.speaker) || !text(sample.text) || !String(fields[sample.source_field] ?? "").includes(sample.text)) errors.push(`${where}/${entry.id}: sample must quote its named source field and speaker`);
        if (!object(sample) || sample.source_kind !== "dialogue" || sample.speaker === "narrator" || (sample.source_refs !== undefined && (!strings(sample.source_refs) || !sample.source_refs.length))) errors.push(`${where}/${entry.id}: sample must be attributed dialogue with valid source references`);
      }
    }
  }
  const terms = design.audio_plan?.pronunciation_terms;
  if (terms !== undefined && (!object(terms) || Object.entries(terms).some(([term, hint]) => !text(term) || term.length > 40 || !text(hint) || hint.length > 180))) errors.push("audio_plan.pronunciation_terms: short reviewed pronunciation supplements required");
  return errors;
}

/** Send only applicable episode cues; retain global mixing/localization directions. */
export function audioForEpisode(plan, number) {
  if (!object(plan)) return plan;
  return {
    ...plan,
    ...(plan.audio_cues ? { audio_cues: plan.audio_cues.filter((entry) => entry.episodes.includes(number)) } : {}),
    ...(plan.audition_scenes ? { audition_scenes: plan.audition_scenes.filter((entry) => entry.episode === number) } : {}),
  };
}

/** The source dictionary stays primary. Production supplements remain review proposals. */
export function productionPronunciations(setting, design) {
  const terms = { ...(setting.lexicon ?? {}) };
  for (const direction of design.characters) {
    const name = setting.characters.find((entry) => entry.id === direction.id)?.name;
    if (!name || Object.hasOwn(terms, name)) continue;
    // Keep phonetic content, excluding review prose such as pending native listening.
    const first = direction.pronunciations["zh-TW"].split("。")[0];
    terms[name] = first.startsWith(`${name}：`) ? first.slice(name.length + 1) : first;
  }
  for (const [term, hint] of Object.entries(design.audio_plan?.pronunciation_terms ?? {})) {
    terms[term] = terms[term] ? `${terms[term]}；${hint}` : hint;
  }
  return terms;
}
