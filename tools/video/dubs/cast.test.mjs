// So That's Why's dialogue explainer is dubbed with one foreign voice per character (owner,
// 2026-11-04): the host and the kid keep their own Gemini voices, in the locale's language.
import assert from "node:assert/strict";
import test from "node:test";
import { spokenByCharacter } from "./cli.mjs";
import { dubCharacterVoice, dubLanguage, dubScript } from "./plan.mjs";
import { voiceFor } from "../core/drama.mjs";
import { dramaFixture } from "../core/fixtures/load.mjs";
import { CHANNEL_ACCENT } from "../core/accent.mjs";

const ACCENT = CHANNEL_ACCENT;
const dialogue = () => ({
  slug: "sothatswhy-dialogue",
  format: "drama",
  category: "explainer",
  look: { preset: "cute-cartoon" },
  voice: { provider: "gemini", name: "Sulafat", style: `${ACCENT}。說故事` },
  characters: [
    { id: "chief", name: "所長", appearance: "a host", voice: { provider: "gemini", name: "Sulafat", style: `${ACCENT}。事務所的所長，溫和` } },
    { id: "kid", name: "小問", appearance: "a girl", voice: { provider: "gemini", name: "Leda", style: `${ACCENT}；八歲小女孩的聲音，好奇` } },
  ],
  scenes: [{ id: "s1", template: "shot", data: { prompt: "p", camera: "drift", visual: "still" }, lines: [
    { id: "a1", speaker: "kid", text: "雲裡真的有水嗎？" },
    { id: "a2", speaker: "chief", text: "有，而且很多。" },
  ] }],
});

test("dubLanguage reads each locale's language from its dub style", () => {
  assert.equal(dubLanguage("en"), "clear, natural English");
  assert.match(dubLanguage("th"), /Central Thai/);
  assert.throws(() => dubLanguage("xx"), /no dub style/);
});

test("a character's dub voice keeps its name and persona, drops the Mandarin accent and asks for the locale's language", () => {
  const voice = dubCharacterVoice(dialogue().characters[1], "ja");
  assert.equal(voice.name, "Leda");
  assert.equal(voice.provider, "gemini");
  assert.ok(!voice.style.includes(ACCENT), voice.style);
  assert.match(voice.style, /^角色：八歲小女孩的聲音，好奇。Speak only in natural standard Japanese/);
});

test("a dialogue explainer's dub script reads each line in its own character's voice; other dramas keep their cast as written", () => {
  const doc = dialogue();
  const translation = { lines: Object.fromEntries(doc.scenes[0].lines.map((line) => [line.id, { text: `EN ${line.id}`, source_hash: null }])) };
  const { doc: script } = dubScript(doc, translation, "en");
  const [kidLine, chiefLine] = script.scenes[0].lines;
  assert.equal(voiceFor(script, kidLine).name, "Leda");
  assert.equal(voiceFor(script, chiefLine).name, "Sulafat");
  assert.match(voiceFor(script, kidLine).style, /Speak only in clear, natural English/);
  const drama = dramaFixture();
  assert.deepEqual(dubScript(drama, null, "en").doc.characters, drama.characters, "a drama's cast is not re-voiced");
});

test("spokenByCharacter lets a dialogue explainer through and still stops a drama whose characters speak", () => {
  assert.equal(spokenByCharacter(dialogue()), null);
  const unvoiced = dialogue();
  unvoiced.characters[1].voice = { provider: "azure", name: "zh-TW-HsiaoChenNeural" };
  assert.equal(spokenByCharacter(unvoiced)?.speaker, "kid", "a character without a Gemini voice cannot speak another language");
  assert.ok(spokenByCharacter(dramaFixture()), "an ordinary drama with speaking characters is still refused");
});
