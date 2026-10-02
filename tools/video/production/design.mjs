// A source-bound director's plan travels inside the approved setting book. No network,
// media generation or approvals here: this module only checks and selects planning data.
import { createHash } from "node:crypto";
import { audioDetailProblems, audioForEpisode, productionPronunciations } from "./audio-contract.mjs";

export const designHash = (value) => createHash("sha256").update(typeof value === "string" ? value : JSON.stringify(value)).digest("hex");
const text = (value) => typeof value === "string" && value.trim().length > 0;
const strings = (value) => Array.isArray(value) && value.every(text);
const array = (value) => Array.isArray(value) ? value : [];
const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
// The prebuilt Gemini choices verified against the speech-generation guide, 2026-10-01.
export const PRODUCTION_VOICES = new Set([
  "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede", "Callirrhoe",
  "Autonoe", "Enceladus", "Iapetus", "Umbriel", "Algieba", "Despina", "Erinome", "Algenib",
  "Rasalgethi", "Laomedeia", "Achernar", "Alnilam", "Schedar", "Gacrux", "Pulcherrima",
  "Achird", "Zubenelgenubi", "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat",
]);

export function designProblems(design, source, profile) {
  const errors = [];
  if (design?.schema_version !== 1) return ["production design schema_version must be 1"];
  if (design.slug !== source.series.slug) errors.push("production slug does not match the story");
  if (design.source_binding?.source_sha256 !== designHash(source)) errors.push("production design is for another source revision");
  if (profile?.subtitles?.burn_in !== false || profile?.subtitles?.delivery !== "closed-captions") errors.push("delivery must use CC without burned-in dialogue");
  if (profile?.phases?.primary?.locale !== "zh-TW" || profile?.phases?.localization?.start_after !== "approved-chinese-final") errors.push("Chinese must finish before localization starts");
  if (JSON.stringify(profile?.phases?.localization?.locales) !== JSON.stringify(["ja", "ko", "en"]) || profile?.phases?.localization?.automatic_generation_now !== false) errors.push("Japanese, Korean and English stay planned for the Chinese-final handoff");
  if (profile?.video?.model !== "veo-3.1-lite-generate-preview" || profile.video.resolution !== "1080p" || profile.video.generation_seconds !== 8) errors.push("Veo Lite 1080p requires the verified model and eight-second sources");
  if (profile?.visual_tier !== "clips") errors.push("the animation delivery profile requires generated motion shots");
  if (design.review_status !== "design-only-not-render-tested") errors.push("the design must not claim rendered or audio acceptance");
  for (const key of ["style", "screen_direction", "performance", "continuity"]) if (!text(design.visual_direction?.[key])) errors.push(`visual_direction.${key} is required`);
  for (const key of ["motifs", "perspective", "dynamic_rules", "locale_constraints"]) if (!strings(design.audio_plan?.[key]) || !design.audio_plan[key].length) errors.push(`audio_plan.${key} is required`);
  const cast = new Set(source.setting.characters.map((character) => character.id));
  const episodes = source.chapters.flatMap((chapter) => chapter.episodes);
  const numbers = new Set();
  for (const episode of array(design.episodes)) {
    if (!object(episode)) { errors.push("each episode must be an object"); continue; }
    if (numbers.has(episode.episode)) errors.push(`duplicate episode ${episode.episode}`);
    numbers.add(episode.episode);
    const original = episodes.find((entry) => entry.number === episode.episode);
    if (!original) { errors.push(`unknown episode ${episode.episode}`); continue; }
    if (episode.title !== original.title) errors.push(`episode ${episode.episode}: title differs from source`);
    if (episode.video_constraints && (!object(episode.video_constraints) || episode.video_constraints.veo_lite_i2v !== "unverified-minor-on-screen" || !text(episode.video_constraints.reason))) errors.push(`episode ${episode.episode}: invalid explicit provider limitation`);
    if (!strings(episode.characters) || episode.characters.some((id) => !cast.has(id))) errors.push(`episode ${episode.episode}: unknown cast`);
    if (JSON.stringify(array(episode.characters).toSorted()) !== JSON.stringify([...original.characters].sort())) errors.push(`episode ${episode.episode}: production cast must match the episode contract`);
    if (!strings(episode.locations) || JSON.stringify(array(episode.locations).toSorted()) !== JSON.stringify([...original.locations].sort())) errors.push(`episode ${episode.episode}: locations differ from source`);
    if (!text(episode.hero_shot?.action) || !text(episode.hero_shot?.camera) || !text(episode.hero_shot?.sound)) errors.push(`episode ${episode.episode}: missing playable hero shot`);
    if (!Array.isArray(episode.risk_controls) || !episode.risk_controls.length || episode.risk_controls.some((entry) => !object(entry) || !text(entry.risk) || !text(entry.solution))) errors.push(`episode ${episode.episode}: missing risk and shooting solution`);
    for (const key of ["source_refs", "prop_checks", "voice_notes", "cc_notes"]) if (!strings(episode[key]) || !episode[key].length) errors.push(`episode ${episode.episode}: ${key} must carry specific production guidance`);
  }
  if (numbers.size !== episodes.length || episodes.some((entry) => !numbers.has(entry.number))) errors.push("the design must cover every episode exactly once");
  let end = 0;
  const ids = new Set();
  for (const shot of array(design.opening_30s)) {
    if (!object(shot)) { errors.push("each opening shot must be an object"); continue; }
    if (!text(shot.id) || ids.has(shot.id)) errors.push("opening shot ids must be unique");
    ids.add(shot.id);
    if (shot.in_s !== end || !Number.isFinite(shot.out_s) || shot.out_s <= shot.in_s || shot.out_s - shot.in_s > 8) errors.push(`opening ${shot.id}: contiguous cuts of at most eight seconds required`);
    end = shot.out_s;
    if (!strings(shot.characters) || shot.characters.some((id) => !cast.has(id)) || shot.characters.length > 3) errors.push(`opening ${shot.id}: at most three known characters per shot`);
    if (array(shot.characters).some((id) => !episodes.find((episode) => episode.number === 1)?.characters.includes(id))) errors.push(`opening ${shot.id}: cast must belong to the first episode`);
    for (const key of ["action", "scale", "camera", "sound", "dialogue_intent"]) if (!text(shot[key])) errors.push(`opening ${shot.id}: missing ${key}`);
    if (!strings(shot.source_refs) || !shot.source_refs.length) errors.push(`opening ${shot.id}: missing story evidence`);
  }
  if (end !== 30) errors.push("opening must cover exactly zero to thirty planned seconds");
  const named = new Set();
  const voiceNames = new Set();
  for (const character of array(design.characters)) {
    if (!object(character)) { errors.push("each character must be an object"); continue; }
    if (!cast.has(character.id) || named.has(character.id)) errors.push(`unknown or duplicate character ${character.id}`);
    named.add(character.id);
    if (character.video_constraints && (!object(character.video_constraints) || !Number.isInteger(character.video_constraints.min_visual_age_years) || character.video_constraints.min_visual_age_years < 1 || character.video_constraints.min_visual_age_years >= 18 || character.video_constraints.veo_lite_i2v !== "not-verified-under-18")) errors.push(`${character.id}: invalid visual-age provider limitation`);
    if (!PRODUCTION_VOICES.has(character.voice_name) || !text(character.performance)) errors.push(`${character.id}: missing supported selected voice or performance`);
    if (voiceNames.has(character.voice_name)) errors.push(`${character.id}: production actors need distinguishable voice selections`);
    voiceNames.add(character.voice_name);
    if (`台灣國語，自然台灣口音；${character.performance ?? ""}`.length > 400) errors.push(`${character.id}: production voice style exceeds 400 characters; shorten explicitly`);
    if (character.pronunciation_status !== "proposed-native-listen-required") errors.push(`${character.id}: pronunciation must not pretend to have been auditioned`);
    for (const locale of ["zh-TW", "ja", "ko", "en"]) if (!text(character.pronunciations?.[locale])) errors.push(`${character.id}: missing ${locale} pronunciation proposal`);
    const looks = new Set();
    for (const look of array(character.look_states)) {
      if (!object(look)) { errors.push(`${character.id}: each look must be an object`); continue; }
      if (typeof look.id !== "string" || !/^[a-z][a-z0-9-]{1,23}$/.test(look.id) || looks.has(look.id) || !text(look.appearance) || look.appearance.length > 800) errors.push(`${character.id}: invalid named shot look`);
      looks.add(look.id);
      if (!Array.isArray(look.episodes) || look.episodes.some((number) => !numbers.has(number))) errors.push(`${character.id}/${look.id}: look refers to an unknown episode`);
      if (array(look.episodes).some((number) => !episodes.find((entry) => entry.number === number)?.characters.includes(character.id))) errors.push(`${character.id}/${look.id}: look used outside this character's approved appearances`);
      if (!strings(look.source_refs) || !look.source_refs.length || !text(look.cue)) errors.push(`${character.id}/${look.id}: missing source or switching cue`);
    }
    if (looks.size > 20) errors.push(`${character.id}: maximum twenty named shot looks`);
    if (!looks.size) errors.push(`${character.id}: missing complete base appearance`);
  }
  if (named.size !== cast.size) errors.push("every cast member needs a production voice and identity plan");
  if (!strings(design.acceptance_checks) || !design.acceptance_checks.length) errors.push("missing finished-film acceptance checks");
  if (!Array.isArray(design.prop_rules) || !design.prop_rules.length || !Array.isArray(design.unresolved)) errors.push("missing prop rules or honest unresolved checks");
  return [...errors, ...audioDetailProblems(design, source)];
}

/** Only the current episode's plan is sent to the writer, checker and listener. */
export function productionForEpisode(setting, number) {
  const design = setting?.production_design;
  if (!design || design.schema_version !== 1) return null;
  const episode = design.episodes?.find((entry) => entry.episode === number);
  if (!episode) throw new Error(`production design has no episode ${number}`);
  return {
    profile: design.profile,
    narrator: design.narrator,
    source_binding: design.source_binding,
    visual_direction: design.visual_direction,
    opening_30s: number === 1 ? design.opening_30s : [],
    characters: design.characters.filter((entry) => episode.characters.includes(entry.id)).map((entry) => ({
      ...entry,
      ...(entry.performance_states ? { performance_states: entry.performance_states.filter((state) => state.episodes.includes(number)) } : {}),
    })),
    prop_rules: design.prop_rules,
    episode,
    pronunciation_hints: setting.lexicon ?? {},
    tts_instructions: [
      "pronunciation_hints 由已審設定發音表固定提供，只作 metadata；不改 CC text、不把拼音注音唸成台詞。",
      "只在來源要求同一 take 重播時，後續 line 設 audio_ref 為前文未引用的原始 line id；保留獨立 id、text、pause_after_ms。speaker、有效 voice 與實際唸法必須相同；不得自指、前向或串接 reference。",
      "同聲線不同台詞分錄；同句不同表演分錄。audio_cues 與 performance_states 是待製作指示，不是逐字台詞或已驗收音訊。",
    ],
    audio_plan: audioForEpisode(design.audio_plan, number),
    acceptance_checks: design.acceptance_checks,
  };
}

/** Add direction to a new review bundle, leaving the original story and receipts unchanged. */
export function productionSetting(setting, design, profile) {
  const selected = new Map(design.characters.map((entry) => [entry.id, entry]));
  const characters = setting.body_json.characters.map((character) => {
    const direction = selected.get(character.id);
    const style = `台灣國語，自然台灣口音；${direction.performance}`;
    if (style.length > 400) throw new Error(`${character.id}: production voice style exceeds 400 characters; shorten explicitly`);
    const catalog = (direction.look_states ?? []).map(({ id, appearance }) => ({ id, appearance }));
    return {
      ...character,
      voice: { ...character.voice, provider: "gemini", name: direction.voice_name, style },
      ...(catalog.length ? { shot_looks: catalog } : {}),
    };
  });
  const narrator = productionNarrator(setting.body_json, design);
  const production = { ...design, profile, narrator };
  const appendix = [
    "", "<!-- BEGIN GENERATED PRODUCTION DIRECTION -->", "", "## 動畫攝製規格（2026-10-02，配音與細節待審版本）", "",
    "先完成繁中台灣口音版本。所有對白字幕為可開關 CC；正片不燒錄字幕。日／韓／英的音軌與 CC 在中文版核准鎖定後製作。",
    "Veo 3.1 Lite 1080p：八秒生成素材，一鏡一個動作，依配音實測剪接。正片使用獨立配音，排除片段原生人聲。",
    "此製作資料包含分鏡、角色聲線與命名造型目錄；試音、畫面與成片尚未驗收。造型按鏡頭選擇，角色身分與聲音不更換。",
    `旁白固定 Gemini ${narrator.voice_name}；${narrator.performance}。不和角色共用聲線，尚未試聽。`,
    ...design.characters.flatMap((character) => [
      `- ${setting.body_json.characters.find((entry) => entry.id === character.id)?.name ?? character.id}（${character.id}）：${character.voice_name}；${character.performance}。中文讀音候選：${character.pronunciations["zh-TW"]}。造型：${(character.look_states ?? []).map((look) => `${look.id}（${look.cue}）`).join("；") || "固定基底"}。`,
      ...(character.performance_states ?? []).map((state) => `  - 聲音狀態 ${state.id}／第 ${state.episodes.join("、")} 集，${state.cue}：${state.instructions.join("；")}。來源：${state.source_refs.join("、")}。尚未試聽。`),
    ]),
    "", "## 配音與錄音線索", "",
    "發音表只提供配音 metadata，不改 CC 原字，也不把注音／拼音唸成台詞。旁白與角色各自套用當句命中的提示。來源敘述是排戲語境，不是逐字對白。",
    "只有來源明確要求完全同一 take 重播，才在後續台詞設 audio_ref 為前文原始 line id；保留各自 line id、原文與停頓。說話者、有效聲線與實際唸法必須相同，不得自指、前向引用或引用另一個重播。相同角色說不同台詞須分錄；同句不同表演也須分錄。",
    "audio_cues 是待製作的聲音計畫，尚未自動產生或混入所有情節音效。敲擊、倒數、歌詞與重播線索需要另做時間軸及聽校；配樂不可仿造必要線索。",
    ...(design.audio_plan.audio_cues ?? []).map((cue) => `- ${cue.id}／第 ${cue.episodes.join("、")} 集，${cue.source_kind}，說話者 ${cue.speaker_ids.join("、") || "無人聲"}：${cue.instructions.join("；")}。來源：${cue.source_refs.join("、")}。待製作與聽審。`),
    ...(design.audio_plan.audition_scenes ?? []).map((scene) => `- 接戲試音 ${scene.id}／第 ${scene.episode} 集：${scene.instructions.join("；")}。聽審：${scene.acceptance.join("；")}。來源：${scene.source_refs.join("、")}。尚未試聽。`),
    "", "## 每集攝製重點", "",
    ...design.episodes.map((episode) => `- 第 ${episode.episode} 集：${episode.hero_shot.action}｜${episode.hero_shot.camera}｜聲音：${episode.hero_shot.sound}｜配音：${episode.voice_notes.join("；")}｜CC：${episode.cc_notes.join("；")}｜${episode.risk_controls.map((control) => `${control.risk}：${control.solution}`).join("；")}`),
    "", "<!-- END GENERATED PRODUCTION DIRECTION -->", "",
  ].join("\n");
  return { body_md: setting.body_md + appendix, body_json: { ...setting.body_json, characters, lexicon: productionPronunciations(setting.body_json, design), production_design: production } };
}

export function productionNarrator(settingBody, design) {
  const used = new Set(design.characters.map((entry) => entry.voice_name));
  const description = settingBody.world?.narrator;
  const suggested = typeof description === "string"
    ? [...PRODUCTION_VOICES].find((name) => description.includes(name))
    : description?.name;
  const voice = [suggested, "Erinome", "Schedar", "Charon", "Iapetus", "Rasalgethi"]
    .find((name) => PRODUCTION_VOICES.has(name) && !used.has(name));
  if (!voice) throw new Error("no separate narrator voice is available");
  return { voice_name: voice, performance: "第三人稱貼近當集主角，語氣清楚克制；只講角色已知的必要資訊，不搶角色對白，情緒轉折留出呼吸", voice_status: "selected-not-auditioned" };
}
