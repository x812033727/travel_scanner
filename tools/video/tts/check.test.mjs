import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { UsageError } from "../core/paths.mjs";
import { eachLine, spokenText, textHash } from "../core/schema.mjs";
import { SAMPLE_RATE, SAMPLES_PER_FRAME } from "../core/timeline.mjs";
import {
  checkFiles,
  comparable,
  DUB_LOCALES,
  dubLexicon,
  dubLines,
  GIVE_UP_AFTER,
  hintTerms,
  judgeBatches,
  lexiconFor,
  matchKind,
  matches,
  MAX_HINT_TERMS,
  MAX_INTENDED_CHARACTERS,
  parseDubLocale,
  reading,
  spokenForm,
  trackFiles,
} from "./check.mjs";
import { concatSamples, downsample, encodeWav } from "./wav.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"t".repeat(43)}`;
const sine = (rate, hz, seconds) => Int16Array.from({ length: Math.round(rate * seconds) }, (_, index) => Math.round(8000 * Math.sin((2 * Math.PI * hz * index) / rate)));
const rms = (samples, from = 0, to = samples.length) => {
  let sum = 0;
  for (let index = from; index < to; index++) sum += samples[index] ** 2;
  return Math.sqrt(sum / (to - from));
};

test("comparison ignores punctuation, spacing and case, and knows the dictionary's spoken forms", () => {
  assert.equal(comparable("用 AI 挑模型，對吧？"), comparable("用ai挑模型對吧"));
  const lexicon = { schema_version: 1, terms: { AI: "A I", LLM: "L L M" } };
  const line = { id: "k7p2", text: "用 AI 挑模型。" };
  assert.equal(spokenForm(line, lexicon), "用 A I 挑模型。");
  assert.ok(matches("用AI挑模型", line, lexicon));
  assert.ok(matches("用 A I 挑模型", line, lexicon));
  assert.ok(!matches("用 AI 調模型", line, lexicon));
  const said = { id: "p5vs", text: "2026/9/24 上架", say: "二〇二六年九月二十四日上架", say_for: "x" };
  assert.ok(matches("二〇二六年九月二十四日上架", said, lexicon));
});

test("same-sound characters and added filler words pass without Jev; a different sound or tone does not", () => {
  const lexicon = { schema_version: 1, terms: {} };
  const line = (text) => ({ id: "k7p2", text });
  // Pairs the pilot's transcripts produced on 2026-09-24.
  assert.equal(matchKind("重要的是你知道他考的不是你的工作", line("重要的是，你知道它考的不是你的工作。"), lexicon), "sound");
  assert.equal(matchKind("吉蓮大多數只要一次", line("級聯大多數只要一次。"), lexicon), "sound");
  assert.equal(matchKind("三成的升級比例啊，是示範用的假設", line("三成的升級比例，是示範用的假設。"), lexicon), "filler");
  assert.equal(matchKind("極廉平均下來啊，大約一分錢誒", line("級聯平均下來，大約一分錢。"), lexicon), "sound");
  assert.equal(matchKind("單一期間就是一次呼叫的時間", line("單一旗艦，就是一次呼叫的時間。"), lexicon), null, "旗 qí and 期 qī differ in tone");
  assert.equal(matchKind("先用小模型，答不好再換旗艦咒語", line("先用小模型，答不好再換旗艦救援。"), lexicon), null);
  assert.equal(matchKind("那我我自己實際上怎麼用", line("那我自己，實際上怎麼用？"), lexicon), null, "a repeated word is not a filler");
  assert.equal(reading("它"), reading("他"));
  // Pairs competition-20261002's transcripts produced on 2026-10-02 (L002, WR-E01-L026), which
  // went to Jev because pinyin-pro reads 妳 as nai3.
  assert.equal(matchKind("字簽了 你也就沒用了", line("字簽了，妳也就沒用了。"), lexicon), "sound");
  assert.equal(matchKind("棠棠，你連我也信不過？", line("棠棠，妳連我也信不過？"), lexicon), "sound");
  assert.equal(matchKind("唐唐,你連我也信不過?", line("棠棠，妳連我也信不過？"), lexicon), "sound");
  assert.equal(reading("妳"), reading("你"));
});

test("Taiwanese particles the voice adds pass as fillers; a closing 餒 or 耶 only when the script lacks it", () => {
  const lexicon = { schema_version: 1, terms: {} };
  const line = (text) => ({ id: "k7p2", text });
  // Pairs the Google student video's transcripts produced on 2026-09-25.
  assert.equal(matchKind("我的看法是齁，這一年免費，算下來大概兩千元", line("我的看法是，這一年免費，算下來大概兩千元。"), lexicon), "filler");
  assert.equal(matchKind("同一頁三種說法，Google自己都沒兜起來耶", line("同一頁，三種說法，Google 自己都沒兜起來。"), lexicon), "filler");
  assert.equal(matchKind("官方自己也沒有給出一句肯定答案餒。", line("官方自己也沒有給出一句肯定答案。"), lexicon), "filler");
  assert.equal(matchKind("他其實很氣", line("他其實很氣餒。"), lexicon), null, "a word that ends in 餒 still needs it");
  assert.equal(matchKind("耶很好", line("很好。"), lexicon), null, "耶 counts only at the end");
});

test("hintTerms lists each English word a line says once, as the script spells it", () => {
  assert.deepEqual(hintTerms({ id: "am2h", text: "那付錢的 Go 呢？" }), ["Go"]);
  assert.deepEqual(hintTerms({ id: "4vai", text: "比較起來，Plus 大約是 Go 的兩倍半，Go 還可能有廣告。" }), ["Plus", "Go"]);
  assert.deepEqual(hintTerms({ id: "k7p2", text: "用 AI 看 MMLU-Pro 與 p95，比 GPT-5.5 準。" }), ["AI", "MMLU-Pro", "p95", "GPT-5.5"]);
  assert.deepEqual(hintTerms({ id: "c2x8", text: "8 × 31.855 ≈ 255" }), [], "numbers are not words");
  assert.deepEqual(hintTerms({ id: "p5vs", text: "Node.js 很快。", say: "Node JS 很快。", say_for: "x" }), ["Node", "JS"], "the spoken form is what is heard");
  const many = { id: "m4ny", text: Array.from({ length: 25 }, (_, index) => `W${index}`).join(" ") };
  assert.equal(hintTerms(many).length, MAX_HINT_TERMS);
});

test("--locale takes a dub's locale and nothing else", () => {
  assert.deepEqual(DUB_LOCALES, ["en", "ja", "ko", "zh-CN"]);
  for (const locale of DUB_LOCALES) assert.equal(parseDubLocale(locale), locale);
  for (const bad of ["zh-TW", "fr", "EN", "zh-cn", ""]) assert.throws(() => parseDubLocale(bad), UsageError, bad);
});

test("a dub's clips, timeline, transcript cache and flags file are its own, beside the narration's", () => {
  assert.deepEqual(trackFiles(), { audio: "audio", timeline: "timeline.json" });
  assert.deepEqual(trackFiles("zh-CN"), { audio: path.join("dubs", "zh-CN", "audio"), timeline: path.join("dubs", "zh-CN", "timeline.json") });
  assert.deepEqual(checkFiles(), { cache: path.join("review", "check.json"), flags: path.join("review", "check-flags.json") });
  assert.deepEqual(checkFiles("ja"), { cache: path.join("review", "check.ja.json"), flags: path.join("review", "check-flags.ja.json") });
});

test("a dub applies only the dictionary's aliases without CJK characters; the narration applies them all", () => {
  const lexicon = { schema_version: 1, terms: { API: "A P I", p95: "P 九十五", NotebookLM: "Notebook L M", AI: null } };
  assert.deepEqual(dubLexicon(lexicon).terms, { API: "A P I", p95: null, NotebookLM: "Notebook L M", AI: null });
  const line = { id: "k7p2", text: "The API keeps p95 under a second." };
  assert.equal(spokenForm(line, lexiconFor(lexicon, "en")), "The A P I keeps p95 under a second.");
  assert.equal(spokenForm(line, lexiconFor(lexicon)), "The A P I keeps P 九十五 under a second.");
  assert.equal(lexiconFor(lexicon), lexicon, "the narration's dictionary is untouched");
  assert.deepEqual(dubLexicon(undefined).terms, {});
});

test("an English dub hints only the dictionary's terms; the other dubs hint every Latin word", () => {
  const lexicon = { schema_version: 1, terms: { GPT: null, Go: null, "MMLU-Pro": null, p95: "P 九十五" } };
  const line = { id: "k7p2", text: "Compared with Go, GPT-5.5 keeps p95 low on MMLU-Pro, e.g. in a test." };
  assert.deepEqual(hintTerms(line, { locale: "en", lexicon }), ["Go", "GPT-5.5", "p95", "MMLU-Pro"]);
  assert.deepEqual(hintTerms({ id: "m4qa", text: "Every time a new model comes out, I switch." }, { locale: "en", lexicon }), []);
  assert.deepEqual(hintTerms({ id: "x9fe", text: "Go と GPT-5.5 を比べると、p95 が低い。" }, { locale: "ja", lexicon }), ["Go", "GPT-5.5", "p95"]);
  assert.deepEqual(hintTerms(line), hintTerms(line, { locale: "zh-TW", lexicon }));
  assert.ok(hintTerms(line).includes("Compared"), "the narration hints every Latin word, as before");
});

test("outside Chinese a transcript passes only when its words match after case, width, spacing and punctuation", () => {
  const lexicon = { schema_version: 1, terms: { AI: null } };
  const en = { id: "k7p2", text: "Every time a new model comes out, the leaderboard has a new number one." };
  assert.equal(matchKind("every time a new model comes out the leaderboard has a new number one", en, lexicon, "en"), "exact");
  assert.equal(matchKind("Every time a new model comes out, the leaderboard has a new number 1.", en, lexicon, "en"), null, "digits against words are Jev's call");
  assert.equal(matchKind("Um, every time a new model comes out, the leaderboard has a new number one.", en, lexicon, "en"), null, "English has no filler rule");
  assert.ok(matches("It's the leaderboard's.", { id: "a1b2", text: "its the leaderboards" }, lexicon, "en"));
  const ja = { id: "m4qa", text: "新しいモデルが出るたびに、AI ランキングの1位が変わります。" };
  assert.equal(matchKind("新しいモデルが出るたびにＡＩランキングの１位が変わります", ja, lexicon, "ja"), "exact", "NFKC folds full-width letters and digits");
  assert.equal(matchKind("新しいモデルが出るたびに、AI ランキングの一位が変わります。", ja, lexicon, "ja"), null);
  const ko = { id: "x9fe", text: "새 모델이 나올 때마다 순위표 1위가 바뀝니다." };
  assert.equal(matchKind("새모델이 나올때마다 순위표 1위가 바뀝니다", ko, lexicon, "ko"), "exact", "the transcriber and the translator space words differently");
  assert.equal(matchKind("새 모델이 나올 때마다 순위표 1위가 바뀝니다.".normalize("NFD"), ko, lexicon, "ko"), "exact", "decomposed Hangul composes again");
  assert.equal(matchKind("새 모델이 나올 때마다 순위표 2위가 바뀝니다.", ko, lexicon, "ko"), null);
});

test("zh-CN keeps the same-sound and filler rules, in Simplified characters", () => {
  const lexicon = { schema_version: 1, terms: {} };
  const line = (text) => ({ id: "k7p2", text });
  assert.equal(matchKind("重要的是你知道他考的不是你的工作", line("重要的是，你知道它考的不是你的工作。"), lexicon, "zh-CN"), "sound");
  assert.equal(matchKind("吉莲大多数只要一次", line("级联大多数只要一次。"), lexicon, "zh-CN"), "sound");
  assert.equal(matchKind("三成的升级比例诶，是示范用的假设", line("三成的升级比例，是示范用的假设。"), lexicon, "zh-CN"), "filler");
  assert.equal(matchKind("官方自己也没有给出一句肯定答案馁", line("官方自己也没有给出一句肯定答案。"), lexicon, "zh-CN"), "filler");
  assert.equal(matchKind("单一期间就是一次呼叫的时间", line("单一旗舰，就是一次呼叫的时间。"), lexicon, "zh-CN"), null, "旗 qí and 期 qī differ in tone");
});

test("a dub's lines follow its timeline and say their translation; a line without one stops the check", () => {
  const timeline = { lines: [{ id: "m4qa", scene: "hook" }, { id: "k7p2", scene: "hook" }] };
  const translation = { lines: { k7p2: { text: "First" }, m4qa: { text: "Second" } } };
  assert.deepEqual(dubLines(timeline, translation, "en", "s"), [
    { scene: "hook", line: { id: "m4qa", text: "Second" } },
    { scene: "hook", line: { id: "k7p2", text: "First" } },
  ]);
  assert.throws(() => dubLines(timeline, { lines: { k7p2: { text: "First" } } }, "en", "s"), /m4qa has no en translation.*dub --slug s --locale en/);
  assert.throws(() => dubLines(timeline, null, "ko", "s"), UsageError);
});

test("downsampling keeps what 16 kHz can carry and removes what it cannot", () => {
  const low = downsample(sine(48_000, 1000, 0.1), 3);
  const ideal = sine(16_000, 1000, 0.1);
  assert.equal(low.length, ideal.length);
  let worst = 0;
  for (let index = 100; index < low.length - 100; index++) worst = Math.max(worst, Math.abs(low[index] - ideal[index]));
  assert.ok(worst <= 16, `largest error ${worst} of 8000`);
  // 12 kHz is above the new 8 kHz Nyquist frequency: it must not fold back as a 4 kHz tone.
  const aliased = downsample(sine(48_000, 12_000, 0.1), 3);
  assert.ok(rms(aliased, 100, aliased.length - 100) < 0.02 * rms(sine(48_000, 12_000, 0.1)));
});

test("Jev's questions go out 40 to a call, each once and in order", () => {
  // A brand story: 90 one-line shot scenes, every line in doubt.
  const questions = Array.from({ length: 90 }, (_, index) => ({ id: `ln${String(index + 1).padStart(3, "0")}` }));
  const batches = judgeBatches(questions);
  assert.deepEqual(batches.map((batch) => batch.length), [40, 40, 10], "three calls, not 90");
  assert.deepEqual(batches.flat(), questions, "every question once, in order");
  assert.deepEqual(judgeBatches([]), [], "no questions, no call");
  assert.deepEqual(judgeBatches(questions.slice(0, 40)), [questions.slice(0, 40)], "exactly 40 is one call");
  assert.throws(() => judgeBatches(questions, 0), RangeError, "calls of no lines would never end");
});

/** A site that synthesizes tones, transcribes clips in narration order, and judges with Jev. */
function site({ heardFor, noul, fails = () => false }) {
  const calls = { speech: 0, transcribe: [], hints: [], languages: [], judge: [], judgeLanguages: [], failed: 0 };
  const tone = (milliseconds) => sine(SAMPLE_RATE, 440, milliseconds / 1000);
  const quiet = (milliseconds) => new Int16Array(Math.round((milliseconds / 1000) * SAMPLE_RATE));
  const fetchImpl = async (url, init) => {
    if (url.endsWith("/speech/status")) {
      return Response.json({ configured: true, region: "eastasia", voices: ["zh-TW-HsiaoChenNeural"], output_format: "riff-48khz-16bit-mono-pcm", max_request_characters: 1500, monthly_limit: 0, used: 0, remaining: null });
    }
    const body = JSON.parse(init.body);
    if (url.endsWith("/speech/transcribe")) {
      const wav = Buffer.from(body.audio, "base64");
      assert.equal(wav.readUInt32LE(24), 16_000, "clips go out at 16 kHz");
      if (fails()) {
        calls.failed += 1;
        return Response.json(
          { code: "video_speech_upstream_busy", detail: "Gemini 暫時無法轉寫（Gemini answered HTTP 503 UNAVAILABLE），請稍後重試" },
          { status: 503, headers: { "Retry-After": "20" } },
        );
      }
      calls.transcribe.push(wav.length);
      calls.hints.push(body.terms);
      calls.languages.push(body.language);
      return Response.json({ text: heardFor(calls.transcribe.length - 1) });
    }
    if (url.endsWith("/speech/judge")) {
      calls.judge.push(body.lines);
      calls.judgeLanguages.push(body.language);
      return Response.json({ results: body.lines.map((line) => ({ id: line.id, noul: noul(line) })) });
    }
    calls.speech += 1;
    const audio = concatSamples(body.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 60), quiet(segment.break_after_ms)]));
    return new Response(encodeWav(audio), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { calls, fetchImpl };
}

function context(box, fetchImpl) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
      home: box.base,
      fetch: fetchImpl,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-24T05:00:00Z"),
      sleep: async () => {},
    },
  };
}

test("check-audio flags only the line Jev doubts, writes a redo file, and reuses its work", async () => {
  const box = sandbox();
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  const lexicon = fixtureLexicon();
  const wrong = lines[2].id;
  // Line 0 comes back in the spoken form, line 1 without punctuation, line 2 with a word missing.
  const heardFor = (count) => {
    const index = count % lines.length;
    if (index === 0) return spokenForm(lines[0], lexicon);
    if (index === 1) return spokenText(lines[1]).replace(/[，。？、]/g, "");
    if (index === 2) return spokenText(lines[2]).slice(0, 4);
    return spokenText(lines[index]);
  };
  const server = site({ heardFor, noul: (line) => (line.id === wrong ? 0.08 : 0.95) });

  const synth = context(box, server.fetchImpl);
  assert.equal(await main(["tts", "--slug", box.slug], synth.ctx), EXIT.ok, synth.out.stderr);

  const first = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], first.ctx), EXIT.lint, first.out.stderr);
  assert.equal(server.calls.transcribe.length, lines.length);
  assert.ok(server.calls.languages.every((language) => language === undefined), "the narration's requests carry no language field");
  assert.equal(server.calls.judge.length, 1, "one Jev call for the one line with a difference");
  assert.deepEqual(server.calls.judge[0].map((line) => line.id), [wrong]);
  assert.deepEqual(server.calls.judgeLanguages, [undefined]);
  const flags = JSON.parse(readFileSync(path.join(box.workdir, "review", "check-flags.json"), "utf8"));
  assert.deepEqual(flags.flags, [wrong]);
  assert.match(flags.notes[wrong], /Jev 0\.08/);
  assert.match(first.out.stdout, new RegExp(`${lines.length} of ${lines.length} lines checked: ${lines.length - 1} match`));
  assert.match(first.out.stdout, /--redo/);

  const again = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], again.ctx), EXIT.lint);
  assert.equal(server.calls.transcribe.length, lines.length, "unchanged clips are not transcribed again");
  assert.equal(server.calls.judge.length, 1, "judged lines are not asked again");

  const forced = context(box, server.fetchImpl);
  await main(["check-audio", "--slug", box.slug, "--force"], forced.ctx);
  assert.equal(server.calls.transcribe.length, lines.length * 2);
});

test("check-audio tells the transcriber each line's English words, and redoes transcripts made without them", async () => {
  const box = sandbox();
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  const english = lines.filter((line) => hintTerms(line).length);
  assert.ok(english.length && english.length < lines.length, "the fixture has lines with and without English words");
  const server = site({ heardFor: (count) => spokenText(lines[count % lines.length]), noul: () => 0.95 });
  const synth = context(box, server.fetchImpl);
  assert.equal(await main(["tts", "--slug", box.slug], synth.ctx), EXIT.ok, synth.out.stderr);

  const first = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stdout);
  lines.forEach((line, index) => {
    const terms = hintTerms(line);
    assert.deepEqual(server.calls.hints[index], terms.length ? terms : undefined, `${line.id} sends its words, and no field without any`);
  });

  // A cache from before hints existed: the lines with English words are transcribed again.
  const cacheFile = path.join(box.workdir, "review", "check.json");
  const cache = JSON.parse(readFileSync(cacheFile, "utf8"));
  for (const entry of Object.values(cache.lines)) delete entry.terms;
  writeFileSync(cacheFile, JSON.stringify(cache));
  const again = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], again.ctx), EXIT.ok);
  assert.equal(server.calls.transcribe.length, lines.length + english.length);
});

test("check-audio skips a line Gemini will not transcribe, keeps the rest, and picks it up on the next run", async () => {
  const box = sandbox();
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  // Requests arrive in narration order; the second line's five tries are requests 1 to 5.
  let failing = new Set();
  let request = 0;
  const server = site({ heardFor: (count) => spokenText(lines[count < 1 ? count : count + 1]), noul: () => 0.95, fails: () => failing.has(request++) });
  const synth = context(box, server.fetchImpl);
  assert.equal(await main(["tts", "--slug", box.slug], synth.ctx), EXIT.ok, synth.out.stderr);

  failing = new Set([1, 2, 3, 4, 5]);
  const first = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], first.ctx), EXIT.external, first.out.stderr);
  assert.equal(server.calls.failed, 5, "the client's five tries, then the line is skipped");
  assert.equal(server.calls.transcribe.length, lines.length - 1);
  assert.match(first.out.stdout, new RegExp(`${lines.length - 1} of ${lines.length} lines checked: ${lines.length - 1} match`));
  assert.ok(first.out.stdout.includes(`${lines[1].id}  Gemini 暫時無法轉寫（Gemini answered HTTP 503 UNAVAILABLE）`), first.out.stdout);
  assert.match(first.out.stdout, /1 lines not checked yet/);

  const recovered = site({ heardFor: () => spokenText(lines[1]), noul: () => 0.95 });
  const retry = context(box, recovered.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], retry.ctx), EXIT.ok, retry.out.stdout);
  assert.equal(recovered.calls.transcribe.length, 1, "only the skipped line is transcribed again");
});

test("check-audio stops when Gemini fails line after line, instead of retrying every line left", async () => {
  const box = sandbox();
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  let down = false;
  const server = site({ heardFor: (count) => spokenText(lines[count % lines.length]), noul: () => 0.95, fails: () => down });
  const synth = context(box, server.fetchImpl);
  assert.equal(await main(["tts", "--slug", box.slug], synth.ctx), EXIT.ok, synth.out.stderr);
  assert.ok(lines.length > GIVE_UP_AFTER, "the fixture has lines left after the give-up point");

  down = true;
  const run = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], run.ctx), EXIT.external);
  assert.equal(server.calls.failed, GIVE_UP_AFTER * 5, "five tries for each line before it gives up");
  assert.match(run.out.stdout, new RegExp(`Gemini failed ${GIVE_UP_AFTER} lines in a row`));
});

/**
 * A dub of the fixture, the way `dub` leaves it: the translation in the repository, and one clip
 * per line plus a timeline under dubs/<locale>/ in the work directory.
 */
function writeDub(box, locale, texts) {
  const lines = [...eachLine(fixture())];
  const translation = { locale, lines: Object.fromEntries(lines.map(({ line }) => [line.id, { source_hash: textHash(line.text), text: texts[line.id] }])) };
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", `${locale}.json`), JSON.stringify(translation));
  const audioDir = path.join(box.workdir, "dubs", locale, "audio");
  mkdirSync(audioDir, { recursive: true });
  const timeline = { locale, speech_hash: "speech0000000000", translation_hash: "translation00000", total_frames: 0, lines: [] };
  for (const { scene, line } of lines) {
    const samples = sine(SAMPLE_RATE, 440, 0.3);
    writeFileSync(path.join(audioDir, `${line.id}.wav`), encodeWav(samples));
    const frames = Math.ceil(samples.length / SAMPLES_PER_FRAME) + 9;
    timeline.lines.push({ id: line.id, scene: scene.id, start_frame: timeline.total_frames, end_frame: timeline.total_frames + frames, audio_samples: samples.length, tempo: 1 });
    timeline.total_frames += frames;
  }
  writeFileSync(path.join(box.workdir, "dubs", locale, "timeline.json"), JSON.stringify(timeline));
  return timeline;
}

const ENGLISH = [
  "Every time a new model comes out, the leaderboard has a new number one. Do you really switch every time?",
  "Today, three questions help you decide which AI model to use in five minutes.",
  "The first question is what work you want it to do.",
  "The second question is how long you can wait for it to think before it answers.",
  "The third question is how much you are willing to pay for it each month.",
  "Write those three answers down, then look at the leaderboard: the choice becomes clear.",
  "The full comparison table is in the article linked in the description. See you in the next video.",
];

test("check-audio --locale checks a dub against its translation, in its language, with its own cache and flags", async () => {
  const box = sandbox();
  const ids = [...eachLine(fixture())].map(({ line }) => line.id);
  const texts = Object.fromEntries(ids.map((id, index) => [id, ENGLISH[index]]));
  const wrong = ids[2];
  // The last scene's first line is longer than Jev's field takes.
  const long = ids[5];
  texts[long] = "Write those three answers down and look again at the leaderboard, ".repeat(8).trim();
  assert.ok([...texts[long]].length > MAX_INTENDED_CHARACTERS);
  const timeline = writeDub(box, "en", texts);
  // Line 0 comes back in lower case without punctuation, the wrong line says something else,
  // the long line is cut short, and the rest come back as written.
  const heardFor = (count) => {
    const id = ids[count % ids.length];
    if (id === ids[0]) return texts[id].toLowerCase().replace(/[,.?]/g, "");
    if (id === wrong) return "Today, three questions decide it.";
    if (id === long) return texts[long].slice(0, 100);
    return texts[id];
  };
  const server = site({ heardFor, noul: (line) => (line.id === wrong ? 0.1 : 0.9) });

  const first = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--locale", "en"], first.ctx), EXIT.lint, first.out.stderr);
  assert.equal(server.calls.transcribe.length, ids.length);
  assert.deepEqual([...new Set(server.calls.languages)], ["en"], "every clip is transcribed as English");
  ids.forEach((id, index) => assert.deepEqual(server.calls.hints[index], texts[id].includes("AI") ? ["AI"] : undefined, `${id} hints only dictionary terms`));
  assert.deepEqual(server.calls.judgeLanguages, ["en"], "one Jev call for the two lines with a difference, in English");
  assert.deepEqual(server.calls.judge.map((batch) => batch.map((line) => line.id)), [[wrong, long]], "lines of two scenes share the call, in narration order");
  const judged = server.calls.judge.flat();
  assert.deepEqual(judged.map((line) => line.id).sort(), [wrong, long].sort());
  assert.equal([...judged.find((line) => line.id === long).intended].length, MAX_INTENDED_CHARACTERS, "an over-long line is cut to what Jev takes");
  assert.match(first.out.stdout, new RegExp(`${long}  is longer than Jev takes`));
  assert.match(first.out.stdout, /en dub: 7 of 7 lines checked: 5 match the script word for word, 0 differ only by same-sound/);
  assert.match(first.out.stdout, /1 judged fine by Jev, 1 flagged/);
  assert.match(first.out.stdout, new RegExp(`dub --slug ${box.slug} --locale en --redo`));

  const flags = JSON.parse(readFileSync(path.join(box.workdir, "review", "check-flags.en.json"), "utf8"));
  assert.deepEqual(flags.flags, [wrong]);
  assert.equal(flags.locale, "en");
  assert.equal(flags.translation_hash, timeline.translation_hash);
  assert.match(flags.notes[wrong], /Jev 0\.10/);
  assert.ok(existsSync(path.join(box.workdir, "review", "check.en.json")));
  assert.ok(!existsSync(path.join(box.workdir, "review", "check.json")), "the narration's cache is not touched");
  assert.ok(!existsSync(path.join(box.workdir, "review", "check-flags.json")));
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.equal(state.runs.at(-1).stage, "check-audio");
  assert.equal(state.runs.at(-1).locale, "en");
  assert.equal(state.runs.at(-1).lines, ids.length);

  const again = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--locale", "en"], again.ctx), EXIT.lint);
  assert.equal(server.calls.transcribe.length, ids.length, "unchanged clips are not transcribed again");
  assert.equal(server.calls.judge.length, 1, "judged lines are not asked again");
});

test("check-audio --locale asks for dub first when there is no dub, with the usage exit code", async () => {
  const box = sandbox();
  const server = site({ heardFor: () => "", noul: () => 1 });
  const missing = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--locale", "ja"], missing.ctx), EXIT.usage);
  assert.match(missing.out.stderr, new RegExp(`no ja dub yet: run dub --slug ${box.slug} --locale ja first`));
  assert.equal(server.calls.transcribe.length, 0);
  const narration = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--locale", "zh-TW"], narration.ctx), EXIT.usage);
  assert.match(narration.out.stderr, /--locale must be one of en, ja, ko, zh-CN/);
});

test("a second transcript clears a line only Gemini misheard; one that misses the same words keeps the flag", async () => {
  const box = sandbox();
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  const [misheard, mispoken] = [lines[2], lines[4]];
  // Gemini cuts both lines short. The second transcriber hears the first as written and the second
  // wrong as well, which is what a voice that really said something else sounds like.
  const heardFor = (count) => {
    const line = lines[count % lines.length];
    return line === misheard || line === mispoken ? spokenText(line).slice(0, 4) : spokenText(line);
  };
  const server = site({ heardFor, noul: (question) => (question.heard === question.intended ? 0.9 : 0.1) });
  const script = path.join(box.base, "second.mjs");
  const log = path.join(box.base, "second.log");
  const canned = { [`${misheard.id}.wav`]: spokenText(misheard), [`${mispoken.id}.wav`]: "完全不同的一句話" };
  writeFileSync(
    script,
    [
      'import { appendFileSync, readFileSync } from "node:fs";',
      'import path from "node:path";',
      "const [locale, ...files] = process.argv.slice(2);",
      'const hints = process.env.VIDEO_SECOND_OPINION_HINTS ? JSON.parse(readFileSync(process.env.VIDEO_SECOND_OPINION_HINTS, "utf8")) : {};',
      `appendFileSync(${JSON.stringify(log)}, \`\${locale} \${files.length} \${Object.keys(hints).sort().join(",")}\\n\`);`,
      `const canned = ${JSON.stringify(canned)};`,
      'for (const file of files) console.log(`${path.basename(file)} ${canned[path.basename(file)] ?? ""}`);',
    ].join("\n"),
  );
  const flag = `${process.execPath} ${script}`;
  const calls = () => (existsSync(log) ? readFileSync(log, "utf8").trim().split("\n") : []);

  const synth = context(box, server.fetchImpl);
  assert.equal(await main(["tts", "--slug", box.slug], synth.ctx), EXIT.ok, synth.out.stderr);
  const first = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--second-opinion", flag], first.ctx), EXIT.lint, first.out.stderr);
  const hinted = [`${misheard.id}.wav`, `${mispoken.id}.wav`].sort().join(",");
  assert.deepEqual(calls(), [`zh-TW 2 ${hinted}`], "one run of the second transcriber, with the locale, the two doubted clips and their hints file");
  const flags = JSON.parse(readFileSync(path.join(box.workdir, "review", "check-flags.json"), "utf8"));
  assert.deepEqual(flags.flags, [mispoken.id]);
  assert.match(first.out.stdout, /, 1 cleared by a second transcript, 1 flagged/);
  assert.match(first.out.stdout, new RegExp(`${misheard.id}  cleared by second\\.mjs \\(matches the script\\)`));
  assert.match(first.out.stdout, /second\.mjs: 完全不同的一句話/);
  assert.ok(server.calls.judge.flat().some((question) => question.id === mispoken.id && question.heard === "完全不同的一句話"), "Jev reads the second transcript that differs");
  assert.ok(!server.calls.judge.flat().some((question) => question.id === misheard.id && question.heard === spokenText(misheard)), "a second transcript that matches needs no Jev call");
  const cache = JSON.parse(readFileSync(path.join(box.workdir, "review", "check.json"), "utf8"));
  assert.equal(cache.lines[misheard.id].second.by, "second.mjs");
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.equal(state.runs.at(-1).cleared, 1);

  // The clearance belongs to the clip: a rerun does not ask again, with or without the flag.
  const again = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--second-opinion", flag], again.ctx), EXIT.lint);
  assert.deepEqual(calls(), [`zh-TW 2 ${hinted}`]);
  const plain = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], plain.ctx), EXIT.lint);
  assert.match(plain.out.stdout, /1 cleared by a second transcript, 1 flagged/);

  // A transcriber that fails leaves the flags as they were.
  const broken = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--second-opinion", `${process.execPath} ${path.join(box.base, "missing.mjs")}`], broken.ctx), EXIT.lint);
  assert.match(broken.out.stdout, /the second transcriber failed/);
  assert.deepEqual(JSON.parse(readFileSync(path.join(box.workdir, "review", "check-flags.json"), "utf8")).flags, [mispoken.id]);
});
