import assert from "node:assert/strict";
import test from "node:test";

import { existsSync, mkdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";

import { EXIT, main } from "../cli.mjs";
import { runtimePolicyHash } from "../core/anime-policy.mjs";
import { approve, sha256File } from "../core/approvals.mjs";
import { presentationTimeline } from "../core/branding.mjs";
import { compilationDocument, compilationLayout, compilationTimeline } from "../core/compilation.mjs";
import { lookHash, mixHash, subtitlesHash } from "../core/drama.mjs";
import { dramaFixture, fixture, fixtureLexicon, sandbox, tempDir, writeAudioFixture } from "../core/fixtures/load.mjs";
import { DESCRIPTION_MAX_BYTES } from "../core/metadata.mjs";
import { eachLine } from "../core/schema.mjs";
import { buildTimeline, estimateTimeline, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from "../core/timeline.mjs";
import { audioReviewHtml, finalReviewHtml } from "../review/pages.mjs";
import { compilationSandbox, compileContext, EPISODE_FRAMES, EPISODES, fakeFfmpeg, writeTranslations } from "../compile/fixture.mjs";
import { localizedThumbnailHash, thumbnailSourceHash } from "../core/translations.mjs";
import { compilationSection, composeMetadata, localizedThumbnailSteps, uploadChecklist } from "./metadata.mjs";
import { captionsCurrent, checksCurrent, linkOrCopy, localeThumbnails, skippedCaptionLocales } from "./cli.mjs";

const doc = fixture();
const timeline = { ...estimateTimeline(doc), speech_hash: "abc123" };

function longAnimeDoc() {
  const anime = dramaFixture();
  Object.assign(anime, {
    category: "anime", production_policy: "long-anime-v1", target_minutes: [22, 22],
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { slug: "fantasy", episode: 1, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false },
  });
  anime.look.preset = "anime-2d";
  delete anime.music;
  for (const scene of anime.scenes) delete scene.data.fit;
  return anime;
}

// Synthetic measured sample counts and a labelled local byte fixture; no generated media calls.
function measuredAnimeTimeline(anime, frames = 39_600) {
  const samples = Object.fromEntries([...eachLine(anime)].map(({ line }) => [line.id, 5 * SAMPLE_RATE]));
  const last = [...eachLine(anime)].at(-1).line.id;
  samples[last] += (frames - buildTimeline(anime, samples).total_frames) * SAMPLES_PER_FRAME;
  return { ...buildTimeline(anime, samples), speech_hash: speechHash(anime, fixtureLexicon()) };
}

function animeChecks(anime, body, finalSha256) {
  const shots = anime.scenes.filter((scene) => scene.template === "shot").map((scene) => {
    const timing = body.scenes.find((placed) => placed.id === scene.id);
    const frames = timing.end_frame - timing.start_frame;
    return { shot: scene.id, kind: "clip", fit: { available: frames, mode: "auto", speed: 1, source_frames: frames, stretched: frames, pad: 0, trim: 0 } };
  });
  return {
    ok: true, speech_hash: body.speech_hash, visual_hash: visualHash(anime),
    runtime_policy_hash: runtimePolicyHash(anime), final_sha256: finalSha256, narration_sha256: body.audio_evidence?.narration_sha256,
    look_hash: lookHash(anime), subtitles_hash: subtitlesHash(anime), mix_hash: mixHash(anime), clips_hash: "fixture-clips",
    metrics: { fps: 30, frames: body.total_frames, shots },
  };
}

test("a changed anime runtime budget invalidates checks while preserving unchanged voice clips", () => {
  const anime = longAnimeDoc();
  const body = measuredAnimeTimeline(anime);
  const checks = animeChecks(anime, body, "f".repeat(64));
  const clips = { clips_hash: "fixture-clips" };
  assert.equal(checksCurrent(anime, fixtureLexicon(), checks, clips), true);
  const changed = { ...anime, runtime_spec: { ...anime.runtime_spec, op_ed_budget_seconds: 120, slot_reserve_seconds: 360 } };
  assert.equal(speechHash(changed, fixtureLexicon()), body.speech_hash);
  assert.equal(visualHash(changed), checks.visual_hash);
  assert.equal(checksCurrent(changed, fixtureLexicon(), checks, clips), false);
  assert.equal(checksCurrent(anime, fixtureLexicon(), { ...checks, runtime_policy_hash: undefined }, clips), false);
  assert.equal(checksCurrent({ ...anime, production_policy: "future-policy" }, fixtureLexicon(), checks, clips), false);
});

test("direct package rejects short, estimated or stale anime evidence even when the local final file is approved", async (t) => {
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const anime = longAnimeDoc();
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(anime));
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ ...anime.series, category: anime.category, production_policy: anime.production_policy, runtime_spec: anime.runtime_spec, target_minutes: 22, style_preset: "anime-2d", characters: anime.characters }));
  mkdirSync(path.join(box.workdir, "clips"), { recursive: true });
  writeFileSync(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify({ clips_hash: "fixture-clips" }));
  const finalFile = path.join(box.workdir, "final.mp4");
  writeFileSync(finalFile, "local fixture, not real media");
  const finalSha256 = await sha256File(finalFile);
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir });
  // Silent takes and narration of the measured body carry its audio evidence.
  const body = writeAudioFixture(measuredAnimeTimeline(anime), box.workdir);
  const checks = animeChecks(anime, body, finalSha256);
  const save = (nextBody, nextChecks) => {
    if (nextBody) writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(nextBody));
    else rmSync(path.join(box.workdir, "timeline.json"), { force: true });
    writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify(nextChecks));
  };
  for (const [name, nextBody, nextChecks, expectedExit, expected] of [
    ["two-minute body", measuredAnimeTimeline(anime, 3_600), animeChecks(anime, measuredAnimeTimeline(anime, 3_600), finalSha256), EXIT.lint, /body is 3600 frames/],
    ["missing body", null, checks, EXIT.lint, /current actual body timeline/],
    ["estimated body", { ...body, timing_basis: "estimated" }, checks, EXIT.lint, /measured/],
    ["stale body speech", { ...body, speech_hash: "old" }, checks, EXIT.lint, /current actual body timeline/],
    ["stale body policy", { ...body, runtime_policy_hash: "old" }, checks, EXIT.lint, /another runtime policy/],
    ["missing checks policy", body, { ...checks, runtime_policy_hash: undefined }, EXIT.usage, /run assemble first/],
    ["stale frames", body, { ...checks, metrics: { ...checks.metrics, frames: body.total_frames - 1 } }, EXIT.lint, /checked final frames/],
    ["missing shot fits", body, { ...checks, metrics: { ...checks.metrics, shots: [] } }, EXIT.lint, /shot|clip|fit/i],
    ["slowed shot", body, { ...checks, metrics: { ...checks.metrics, shots: checks.metrics.shots.map((shot, index) => index === 0 ? { ...shot, fit: { ...shot.fit, speed: 0.85 } } : shot) } }, EXIT.lint, /shot|clip|fit|speed/i],
    ["padded shot", body, { ...checks, metrics: { ...checks.metrics, shots: checks.metrics.shots.map((shot, index) => index === 0 ? { ...shot, fit: { ...shot.fit, pad: 1 } } : shot) } }, EXIT.lint, /shot|clip|fit|pad/i],
    ["missing final SHA", body, { ...checks, final_sha256: undefined }, EXIT.lint, /current final.mp4 SHA-256/],
    ["stale final SHA", body, { ...checks, final_sha256: "f".repeat(64) }, EXIT.lint, /current final.mp4 SHA-256/],
  ]) {
    save(nextBody, nextChecks);
    const { ctx, out } = compileContext(box, fakeFfmpeg());
    assert.equal(await main(["package", "--slug", box.slug], ctx), expectedExit, `${name}: ${out.stderr}`);
    assert.match(out.stderr, expected, name);
    assert.ok(!existsSync(path.join(box.workdir, "upload")), `${name} is rejected before producing a delivery package`);
  }
  // A new owner approval for changed bytes still cannot make an older assemble receipt current.
  writeFileSync(finalFile, "replacement local fixture, not real media");
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir });
  save(body, checks);
  const replaced = compileContext(box, fakeFfmpeg());
  assert.equal(await main(["package", "--slug", box.slug], replaced.ctx), EXIT.lint);
  assert.match(replaced.out.stderr, /current final.mp4 SHA-256/);
  assert.ok(!existsSync(path.join(box.workdir, "upload")));

  const currentSha256 = await sha256File(finalFile);
  save(body, { ...checks, final_sha256: currentSha256 });
  const valid = compileContext(box, fakeFfmpeg());
  assert.equal(await main(["package", "--slug", box.slug], valid.ctx), EXIT.ok, valid.out.stderr + valid.out.stdout);
  const metadata = JSON.parse(readFileSync(path.join(box.workdir, "upload", "metadata.json"), "utf8"));
  assert.equal(metadata.production_policy, "long-anime-v1");
  assert.deepEqual(metadata.runtime_spec, anime.runtime_spec);
  assert.equal(metadata.runtime_proof.basis, "measured");
  assert.equal(metadata.runtime_proof.policy_hash, runtimePolicyHash(anime));
  assert.equal(metadata.runtime_proof.final_sha256, currentSha256);
  assert.equal(metadata.final_sha256, currentSha256);
  assert.equal(metadata.runtime_proof.body_seconds, 1320);
  assert.equal(metadata.runtime_proof.op_ed_seconds, 0, "the budget does not require extra bookend footage");
  assert.equal(metadata.runtime_proof.presentation_seconds, 1320, "reserve is never rendered");
});

test("branded metadata shifts later chapters five seconds while retaining a valid opening chapter", () => {
  const applied = { hash: "a".repeat(64), intro_frames: 150, outro_frames: 90 };
  const presented = presentationTimeline(timeline, applied);
  const { metadata, problems } = composeMetadata({ doc, timeline: presented, translations: { en: { title: "Title", description: "Body", chapters: { hook: "Opening" } } } });
  assert.deepEqual(problems, []);
  assert.equal(metadata.chapters.length, timeline.chapters.length, "no invalid five-second standalone brand chapter");
  assert.deepEqual(metadata.chapters[0], { at: "00:00", title: "開場" });
  assert.match(metadata.localizations.en.description, /Chapters\n00:00 Opening\n/);
  assert.equal(presented.chapters[1].start_frame, timeline.chapters[1].start_frame + 150);
  const expectedSeconds = Math.floor(timeline.chapters[1].start_frame / 30) + 5;
  const stamp = `${Math.floor(expectedSeconds / 60).toString().padStart(2, "0")}:${(expectedSeconds % 60).toString().padStart(2, "0")}`;
  assert.equal(metadata.chapters[1].at, stamp);
  assert.ok(metadata.description.includes(`\n${stamp} `));
});

test("caption reuse is bound to the applied brand, including transitions to and from legacy cuts", () => {
  const manifest = { speech_hash: "speech", locales: { "zh-TW": {} }, skipped: {} };
  assert.equal(captionsCurrent(manifest, "speech", ["zh-TW"], {}), true);
  assert.equal(captionsCurrent(manifest, "speech", ["zh-TW"], {}, "brand-a"), false);
  const branded = { ...manifest, branding_hash: "brand-a" };
  assert.equal(captionsCurrent(branded, "speech", ["zh-TW"], {}, "brand-a"), true);
  assert.equal(captionsCurrent(branded, "speech", ["zh-TW"], {}, "brand-b"), false);
  assert.equal(captionsCurrent(branded, "speech", ["zh-TW"], {}), false);
});

test("zh-TW metadata carries the composed description with chapters and sources", () => {
  const { problems, metadata } = composeMetadata({ doc, timeline });
  assert.deepEqual(problems, []);
  assert.equal(metadata.default_language, "zh-TW");
  assert.equal(metadata.privacy_status, "private");
  assert.match(metadata.description, /章節\n00:00 開場\n/);
  assert.match(metadata.description, /參考資料\n範例來源：https:\/\/example\.com\/models/);
  assert.deepEqual(metadata.localizations, {});
  assert.deepEqual(metadata.chapters.map((chapter) => chapter.title), ["開場", "三個問題", "結論"]);
});

test("translated locales get their own title, description, chapter titles and article link", () => {
  const translations = {
    en: { title: "How to pick an AI model", description: "Three questions.", tags: ["AI models", "AI 模型"], chapters: { hook: "Intro" } },
    ja: { title: "", description: "incomplete" },
  };
  const pack = { slug: "ai-workflow-cost-quality-latency", kind: "life", locales: { "zh-TW": {}, en: {} } };
  const { metadata } = composeMetadata({ doc: { ...doc, source_guide: pack.slug }, timeline, translations, pack });
  assert.deepEqual(Object.keys(metadata.localizations), ["en"]);
  assert.match(metadata.localizations.en.description, /Chapters\n00:00 Intro\n/);
  assert.match(metadata.localizations.en.description, /https:\/\/mokaair\.com\/en\/life\/ai-workflow-cost-quality-latency\?utm_source=youtube/);
  assert.match(metadata.description, /https:\/\/mokaair\.com\/zh-TW\/life\//);
  assert.deepEqual(metadata.tags, ["AI 模型", "模型選擇"], "translated tags stay in their translation file, not in the upload's list");
  const many = { ...doc, youtube: { ...doc.youtube, tags: Array.from({ length: 14 }, (_, n) => `tag${n}`) } };
  assert.deepEqual(composeMetadata({ doc: many, timeline }).metadata.tags, many.youtube.tags.slice(0, 10), "video.json's order, cut to ten");
});

test("a description over YouTube's byte limit is a problem, named by locale", () => {
  const long = { ...doc, youtube: { ...doc.youtube, description: "字".repeat(1700) } };
  const { problems } = composeMetadata({ doc: long, timeline });
  assert.match(problems.join("\n"), /zh-TW\.description: \d+ bytes/);
});

test("UPLOAD.md keeps only the Studio steps: private first, the disclosure as metadata.json says, no self-check list", () => {
  const { metadata } = composeMetadata({ doc, timeline });
  const slides = uploadChecklist({ metadata, captions: ["captions/zh-TW.srt"], thumbnail: true, disclosure: { synthetic: false, reason: "slides read by a stock TTS voice" } });
  assert.match(slides, /瀏覽權限先選「私人」/);
  assert.match(slides, /captions\/zh-TW\.srt/);
  assert.match(slides, /「變造或合成內容」：不用勾。`metadata\.json` 的 `contains_synthetic_media` 是 `false`（slides read by a stock TTS voice）/);
  assert.match(slides, /貼上 YouTube 網址/);
  assert.doesNotMatch(slides, /- \[ \]/, "the self-check list moved into the automatic checks");
  assert.doesNotMatch(slides, /非原創內容政策|AI 使用揭露|youtube-sync/);
  const drama = uploadChecklist({ metadata: { ...metadata, contains_synthetic_media: true, disclosure_reason: "AI-generated shots and voices" }, captions: [], thumbnail: false, drama: true });
  assert.match(drama, /「變造或合成內容」：勾「是」。`metadata\.json` 的 `contains_synthetic_media` 是 `true`（AI-generated shots and voices）/);
  assert.match(drama, /還沒有字幕檔/);
});

test("the audio review page lists every line with its clip and exports flags with the timeline version", () => {
  const html = audioReviewHtml(doc, timeline);
  for (const line of doc.scenes.flatMap((scene) => scene.lines)) assert.ok(html.includes(`src="../audio/${line.id}.wav"`), line.id);
  assert.match(html, /唸成：完整的比較表，放在說明欄的文章裡/);
  assert.match(html, /"speech_hash":"abc123"/);
  assert.match(html, /download="flags\.json"|link\.download="flags\.json"/);
});

test("review pages escape the script's text", () => {
  const hostile = structuredClone(doc);
  hostile.youtube.title = "<script>alert(1)</script>";
  hostile.scenes[0].lines[0].text = "</script><img src=x onerror=alert(1)>";
  for (const html of [audioReviewHtml(hostile, timeline), finalReviewHtml(hostile, timeline, { problems: [] })]) {
    assert.doesNotMatch(html, /<script>alert/);
    assert.doesNotMatch(html, /<img src=x/);
  }
});

test("the final review page plays final.mp4 and seeks from chapters and lines", () => {
  const html = finalReviewHtml(doc, timeline, { problems: [], metrics: { loudness: { integrated: -14 } } });
  assert.match(html, /<video id="video" controls preload="metadata" src="\.\.\/final\.mp4">/);
  assert.equal((html.match(/class="cue"/g) ?? []).length, 3 + 7);
  assert.match(html, /自動檢查全部通過/);
  assert.match(finalReviewHtml(doc, timeline, { problems: ["loudness off"] }), /自動檢查有問題：loudness off/);
});

test("with the owner's choice, metadata holds the chosen locales and names a chosen one not translated yet", () => {
  const translations = {
    en: { title: "How to pick an AI model", description: "Three questions." },
    ja: { title: "AI モデルの選び方", description: "三つの質問。" },
  };
  const chosen = composeMetadata({ doc, timeline, translations, locales: ["ja"] });
  assert.deepEqual(chosen.problems, []);
  assert.deepEqual(Object.keys(chosen.metadata.localizations), ["ja"], "en is translated but not chosen");
  const missing = composeMetadata({ doc, timeline, translations, locales: ["ko", "en"] });
  assert.deepEqual(missing.problems, ["ko: the title and description are not translated yet (i18n-sheet --locale ko --parts metadata, then i18n-merge)"]);
  assert.deepEqual(Object.keys(missing.metadata.localizations), ["en"]);
  assert.deepEqual(composeMetadata({ doc, timeline, translations, locales: [] }).metadata.localizations, {}, "Traditional Chinese only");
  const steps = uploadChecklist({ metadata: composeMetadata({ doc, timeline }).metadata, captions: [], thumbnail: false, dubs: [{ locale: "en", file: "dubs/en.m4a", format: "m4a", tempo_max: 1 }] });
  assert.match(steps, /「語言」卡片按「已在 Studio 上傳配音」/);
  assert.match(uploadChecklist({ metadata: composeMetadata({ doc, timeline }).metadata, captions: [], thumbnail: false }), /勾那個語言的「配音」/);
});

test("a compilation's metadata keys its chapters on episode slugs and falls back to 「第 N 集」 when eighty titles would not fit", () => {
  const episodes = Array.from({ length: 80 }, (_, index) => ({ slug: `wuxia-ep-${index + 1}`, number: index + 1, title: "山海經最倔強的一隻鳥到底為什麼要填海呢這是第一部的長標題" }));
  const long = compilationDocument({ series: "wuxia", episodes, voice: doc.voice });
  long.youtube.title = "仙門風雲 全集";
  long.youtube.description = "第一部的每一集。";
  const compiled = compilationTimeline(compilationLayout(long, long.compilation.episodes.map((slug) => ({ slug, frames: 7200 }))), long.compilation.titles);
  const translations = { en: { title: "Part one", description: "All of part one.", tags: ["wuxia"], chapters: Object.fromEntries(episodes.map((episode) => [episode.slug, `Episode ${episode.number}: a long English title that goes on and on and on`])) } };
  const { problems, metadata } = composeMetadata({ doc: long, timeline: compiled, translations });
  assert.deepEqual(problems, []);
  assert.ok(Buffer.byteLength(metadata.description, "utf8") <= DESCRIPTION_MAX_BYTES);
  assert.match(metadata.description, /\n00:00 第 1 集\n04:02 第 2 集\n/);
  assert.match(metadata.localizations.en.description, /Chapters\n00:00 Episode 1\n/);
  assert.deepEqual(metadata.chapters.slice(0, 2), [{ at: "00:00", title: "第 1 集" }, { at: "04:02", title: "第 2 集" }]);
  assert.equal(metadata.chapters.length, 80);
  // Three episodes fit: the titles stay, in zh-TW and in the translation keyed by slug.
  const short = compilationDocument({ series: "wuxia", episodes: episodes.slice(0, 3), voice: doc.voice });
  short.youtube.title = "仙門風雲 全集";
  const three = compilationTimeline(compilationLayout(short, short.compilation.episodes.map((slug) => ({ slug, frames: 7200 }))), short.compilation.titles);
  const fits = composeMetadata({ doc: short, timeline: three, translations: { en: { ...translations.en, chapters: { "wuxia-ep-2": "Episode 2: The Library" } } } });
  assert.match(fits.metadata.description, /00:00 第 1 集 山海經/);
  assert.match(fits.metadata.localizations.en.description, /04:02 Episode 2: The Library\n08:04 第 3 集 山海經/);
  assert.equal(fits.metadata.chapters[0].title, "第 1 集 山海經最倔強的一隻鳥到底為什麼要填海呢這是第一部的長標題");
});

test("UPLOAD.md of a compilation says the file is downloaded from the site and the chapters are in the description", () => {
  const { metadata } = composeMetadata({ doc, timeline });
  const text = uploadChecklist({ metadata: { ...metadata, download: "upload/final.mp4" }, captions: ["captions/zh-TW.srt"], thumbnail: true, drama: true, disclosure: { synthetic: true, reason: "a drama" }, compilation: { episodes: 40, size_bytes: 2.5 * 1024 ** 3 } });
  assert.match(text, /## 合集\n\n- 這支是 40 集的合集：每集一章，章節時間戳已經在說明欄裡（`metadata\.json` 的 `chapters` 有 3 章）/);
  assert.match(text, /約 2\.50 GB，不走審核檔案區：到 \/admin\/videos 這支的「可以上架」卡片下載（`upload\/final\.mp4`），再照第 1 節在 Studio 上傳，瀏覽權限一樣先選「私人」/);
  assert.match(text, /## 1\. 上傳/);
  assert.doesNotMatch(uploadChecklist({ metadata, captions: [], thumbnail: false }), /## 合集/);
  assert.match(compilationSection({ chapters: [] }, {}), /0 集的合集/);
  assert.deepEqual(skippedCaptionLocales({ skipped: { ja: ["ep-2"] } }, ["captions/zh-TW.srt"], { compilation: true }), { en: "no caption file merged", ja: "no caption file in episodes ep-2", ko: "no caption file merged" });
});

test("package links a compilation's final.mp4, records the download, the size and the episodes, and passes its check", async () => {
  const box = compilationSandbox();
  writeTranslations(box, box.doc);
  const total = EPISODES.reduce((sum, slug) => sum + EPISODE_FRAMES[slug], 0) + EPISODES.length * 60 + 120;
  const compiled = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["compile", "--slug", box.slug], compiled.ctx), EXIT.ok, compiled.out.stderr);
  const before = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["package", "--slug", box.slug], before.ctx), EXIT.owner, "the cut is not approved yet");
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir, now: new Date("2026-09-27T06:00:00Z") });
  const { out, ctx } = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["package", "--slug", box.slug], ctx), EXIT.ok, out.stderr + out.stdout);
  const upload = path.join(box.workdir, "upload");
  const final = path.join(upload, "final.mp4");
  assert.equal(statSync(final).ino, statSync(path.join(box.workdir, "final.mp4")).ino, "a hard link, not a copy");
  const metadata = JSON.parse(readFileSync(path.join(upload, "metadata.json"), "utf8"));
  assert.equal(metadata.compilation, true);
  assert.equal(metadata.download, "upload/final.mp4");
  assert.equal(metadata.size_bytes, statSync(final).size);
  assert.deepEqual(metadata.episodes.map((episode) => [episode.slug, episode.start_frame]), [["wuxia-ep-1", 60], ["wuxia-ep-2", 4441], ["wuxia-ep-3", 8401]]);
  assert.equal(metadata.episodes[0].sha256, box.episodes["wuxia-ep-1"].sha256);
  assert.deepEqual(metadata.captions, ["captions/en.srt", "captions/zh-TW.srt"]);
  assert.deepEqual(metadata.skipped_caption_locales, { ja: "no caption file in episodes wuxia-ep-1, wuxia-ep-2, wuxia-ep-3", ko: "no caption file in episodes wuxia-ep-1, wuxia-ep-2, wuxia-ep-3" });
  assert.equal(metadata.contains_synthetic_media, true);
  assert.deepEqual(Object.keys(metadata).slice(-2), ["contains_synthetic_media", "disclosure_reason"], "the disclosure stays last, so qa's rewrite leaves the bytes alone");
  assert.deepEqual(metadata.chapters.map((chapter) => chapter.title), ["第 1 集 初入山門", "第 2 集 夜探藏經閣", "第 3 集 劍冢之約"]);
  assert.match(metadata.localizations.en.description, /00:00 en wuxia-ep-1\n/, "translated chapters are read by episode slug");
  const md = readFileSync(path.join(upload, "UPLOAD.md"), "utf8");
  assert.match(md, /## 合集\n\n- 這支是 3 集的合集/);
  assert.ok(existsSync(path.join(upload, "description.ko.txt")));
  assert.match(out.stdout, /final\.mp4 \(linked, 0\.00 GB, 3 episodes\)/);
  assert.match(out.stdout, /package check: 4 of 4 passed/);
  // Without compile's captions for these cuts, package refuses rather than cutting captions itself.
  const manifest = path.join(box.workdir, "captions", "manifest.json");
  const saved = readFileSync(manifest, "utf8");
  writeFileSync(manifest, JSON.stringify({ compilation_hash: "stale", locales: {}, skipped: {} }));
  const stale = compileContext(box, fakeFfmpeg({ total }));
  assert.equal(await main(["package", "--slug", box.slug], stale.ctx), EXIT.usage);
  assert.match(stale.out.stderr, /merged for other cuts; run compile again/);
  writeFileSync(manifest, saved);
  assert.equal(linkOrCopy(path.join(box.workdir, "final.mp4"), path.join(box.workdir, "copy.mp4")), "linked");
});

test("each language's own thumbnail goes into the package only when render drew it from the words i18n has now", () => {
  const workdir = tempDir("video-thumbs-");
  mkdirSync(path.join(workdir, "thumbnails"));
  for (const locale of ["en", "ja"]) writeFileSync(path.join(workdir, "thumbnails", `${locale}.jpg`), "jpeg");
  const merged = (headline) => ({ thumbnail: { tag: "Picking a model", headline }, source_hashes: { thumbnail: thumbnailSourceHash(doc) } });
  const translations = { en: merged("No. 1 is not always best"), ja: merged("一位が最適とは限らない"), ko: merged("1위가 최선은 아니다") };
  const drawn = (locale, translation) => ({ file: `thumbnails/${locale}.jpg`, hash: localizedThumbnailHash(doc, translation) });
  const manifest = {
    thumbnail_locales: { en: drawn("en", translations.en), ja: drawn("ja", merged("an older headline")) },
    thumbnail_locale_gaps: { ko: "no bundled font has \"최\" U+CD5C" },
  };
  const { files, skipped } = localeThumbnails({ doc, translations, manifest, workdir, locales: ["en", "ja", "ko"] });
  assert.deepEqual(files, { en: "thumbnails/en.jpg" });
  assert.deepEqual(Object.keys(skipped), ["ja", "ko"]);
  assert.match(skipped.ja, /drawn from other words than i18n has now; run render/);
  assert.match(skipped.ko, /no bundled font has/);
  // A video packaged before render drew any keeps working: every language is a note.
  assert.deepEqual(localeThumbnails({ doc, translations: {}, manifest: null, workdir, locales: ["en"] }), { files: {}, skipped: { en: "i18n/en.json has no thumbnail words (i18n-sheet --locale en --parts metadata, then i18n-merge)" } });
  assert.deepEqual(localeThumbnails({ doc, translations, manifest: { thumbnail_locales: { en: drawn("en", translations.en) } }, workdir, locales: ["en", "ko"] }).skipped.ko, "not drawn yet; run render");
});

test("UPLOAD.md gets a language thumbnails section with Studio's steps only when there is something to say", () => {
  const { metadata } = composeMetadata({ doc, timeline });
  const withThumbs = uploadChecklist({ metadata, captions: ["captions/zh-TW.srt"], thumbnail: true, thumbnails: { en: "thumbnails/en.jpg" }, skippedThumbnails: { ja: "i18n/ja.json has no thumbnail words" } });
  assert.match(withThumbs, /## 4\. 各語言的縮圖/);
  assert.match(withThumbs, /`thumbnails\/en\.jpg`（en）/);
  assert.match(withThumbs, /「語言」→ 這支影片 → 點那個語言的名稱 →「縮圖」旁的「新增」→ 選對應的檔案 →「更新」/);
  assert.match(withThumbs, /長片（不含 Shorts）/);
  assert.match(withThumbs, /- ja：i18n\/ja\.json has no thumbnail words/);
  assert.match(withThumbs, /## 5\. 上傳之後/);
  const plain = uploadChecklist({ metadata, captions: [], thumbnail: true });
  assert.doesNotMatch(plain, /各語言的縮圖/);
  assert.match(plain, /## 4\. 上傳之後/);
  assert.equal(localizedThumbnailSteps({}, {}), "");
  assert.doesNotMatch(uploadChecklist({ metadata, captions: [], thumbnail: false, skippedThumbnails: { ja: "x" } }), /各語言的縮圖/, "no thumbnail.jpg, nothing to localize");
});
