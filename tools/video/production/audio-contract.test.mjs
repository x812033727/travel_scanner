import test from "node:test";
import assert from "node:assert/strict";
import { audioDetailProblems, audioForEpisode, productionPronunciations } from "./audio-contract.mjs";

const source = {
  setting: { characters: [{ id: "child", name: "小滿" }, { id: "mother", name: "蘭音" }] },
  chapters: [{ episodes: [
    { number: 13, characters: ["child", "mother"], turn: "蘭音喊：不要開門。", conflict: "紅白廣播不同話。" },
    { number: 14, characters: ["child"], turn: "小滿問：這次到家了嗎？" },
  ] }],
};
const evidence = { source_refs: ["story.mjs:1"], source_excerpt: "原文語境", instructions: ["保留固定聲線"], status: "proposed" };
const design = {
  characters: [{ id: "child", performance_states: [{ ...evidence, id: "fading", episodes: [14], cue: "仍有呼吸" }] }],
  audio_plan: {
    motifs: ["三短一長"],
    audio_cues: [
      { ...evidence, id: "different-lines", episodes: [13], source_kind: "recording", speaker_ids: ["mother"] },
      { ...evidence, id: "repeat-one-take", episodes: [14], source_kind: "recording", speaker_ids: ["child"] },
    ],
    audition_scenes: [{ ...evidence, id: "mother-channel", episode: 13, speaker_ids: ["mother"], acceptance: ["音色相同、台詞不同"], line_samples: [{ speaker: "mother", text: "不要開門。", source_field: "turn", source_kind: "dialogue" }] }],
  },
};

test("episode writer receives its applicable recording cues without later episode spoilers", () => {
  const filtered = audioForEpisode(design.audio_plan, 13);
  assert.deepEqual(filtered.audio_cues.map((entry) => entry.id), ["different-lines"]);
  assert.equal(filtered.audition_scenes.length, 1);
  assert.deepEqual(filtered.motifs, design.audio_plan.motifs);
  assert.equal(design.audio_plan.audio_cues.length, 2);
  assert.deepEqual(audioForEpisode(design.audio_plan, 14).audition_scenes, []);
});

test("a plan cannot claim audible acceptance, change the speaker, or quote invented scene dialogue", () => {
  assert.deepEqual(audioDetailProblems(design, source), []);
  for (const [mutate, message] of [
    [(d) => { d.audio_plan.audio_cues[0].speaker_ids = ["invented"]; }, /unknown speaker/],
    [(d) => { d.characters[0].performance_states[0].status = "accepted"; }, /no audio acceptance/],
    [(d) => { d.characters[0].performance_states[0].episodes = [99]; }, /unknown or missing episode/],
    [(d) => { d.audio_plan.audition_scenes[0].line_samples[0].text = "我愛你。"; }, /quote its named source/],
    [(d) => { d.audio_plan.audio_cues.push(d.audio_plan.audio_cues[0]); }, /duplicate cue/],
    [(d) => { d.audio_plan.audio_cues[0] = null; }, /must be an object/],
    [(d) => { d.characters[0].performance_states[0].speech_mode = "non-verbal"; }, /speech_mode/],
    [(d) => { d.audio_plan.audition_scenes[0].line_samples = {}; }, /line_samples must be an array/],
    [(d) => { d.audio_plan.audition_scenes[0].line_samples[0].source_kind = "writing"; }, /attributed dialogue/],
    [(d) => { d.audio_plan.audition_scenes[0].line_samples[0].source_refs = "story.mjs:1"; }, /valid source references/],
  ]) {
    const invalid = structuredClone(design);
    mutate(invalid);
    assert.ok(audioDetailProblems(invalid, source).some((messageText) => message.test(messageText)));
  }
});

test("source pronunciation remains primary, supplements fill partial hints, and missing names use short candidates", () => {
  const setting = { characters: [{ id: "wei", name: "沈亦微" }, { id: "shuyun", name: "杜淑雲" }, { id: "dou", name: "阿豆" }], lexicon: { 沈亦微: "沈姓讀ㄕㄣˇ", 杜淑雲: "dù shú yún", 普通詞: null } };
  const proposal = { characters: [
    { id: "wei", pronunciations: { "zh-TW": "沈亦微：Shěn Yìwéi。待聽校。" } },
    { id: "shuyun", pronunciations: { "zh-TW": "dù shū yún" } },
    { id: "dou", pronunciations: { "zh-TW": "阿豆：Ā Dòu。尚未實聽。" } },
  ], audio_plan: { pronunciation_terms: { 沈亦微: "微讀ㄨㄟˊ" } } };
  const result = productionPronunciations(setting, proposal);
  assert.equal(result.杜淑雲, "dù shú yún");
  assert.equal(result.沈亦微, "沈姓讀ㄕㄣˇ；微讀ㄨㄟˊ");
  assert.equal(result.阿豆, "Ā Dòu");
  assert.equal(result.普通詞, null);
  assert.deepEqual(Object.keys(setting.lexicon), ["沈亦微", "杜淑雲", "普通詞"]);
});
