import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, spokenText } from "../core/schema.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { comparable, GIVE_UP_AFTER, hintTerms, MAX_HINT_TERMS, matchKind, matches, reading, spokenForm } from "./check.mjs";
import { concatSamples, downsample, encodeWav } from "./wav.mjs";

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

/** A site that synthesizes tones, transcribes clips in narration order, and judges with Jev. */
function site({ heardFor, noul, fails = () => false }) {
  const calls = { speech: 0, transcribe: [], hints: [], judge: [], failed: 0 };
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
      return Response.json({ text: heardFor(calls.transcribe.length - 1) });
    }
    if (url.endsWith("/speech/judge")) {
      calls.judge.push(body.lines);
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
  assert.equal(server.calls.judge.length, 1, "one Jev call for the one scene with a difference");
  assert.deepEqual(server.calls.judge[0].map((line) => line.id), [wrong]);
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
