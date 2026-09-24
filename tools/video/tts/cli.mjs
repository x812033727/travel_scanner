// `login`, `audition` and `tts`: narration through the Mokaair server, which holds the Azure key.
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { parseArgs } from "node:util";

import { emptyLexicon } from "../core/lexicon.mjs";
import { atomicWrite, lexiconFile, readJson, resolveWorkBase, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { buildTimeline, checkChapters, formatClock, frameToSeconds, speechHash } from "../core/timeline.mjs";
import { SpeechError, speechStatus, synthesize } from "./client.mjs";
import { TOKEN_PATTERN, readCredentials, validSite, writeCredentials } from "./credentials.mjs";
import { defaultClientName, startPairing, waitForPairing } from "./pairing.mjs";
import { GEMINI_VOICE_PREFIX, MAX_REQUEST_CHARACTERS, billableForRequest, planRequests, spokenParts, voiceFields } from "./requests.mjs";
import { buildNarration, flaggedLines, synthesizeRequest } from "./synthesis.mjs";
import { encodeWav, parseWav, requireNarrationFormat } from "./wav.mjs";

const FREE_TIER = 500_000;

const escapeHtml = (text) => String(text).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);

function exitFor(error, EXIT) {
  return error.who === "owner" ? EXIT.owner : EXIT.external;
}

function clientOptions(ctx, credentials) {
  return { site: credentials.site, token: credentials.token, fetchImpl: ctx.fetch ?? globalThis.fetch, ...(ctx.sleep ? { sleep: ctx.sleep } : {}) };
}

function requireCredentials(ctx) {
  const credentials = readCredentials({ env: ctx.env, home: ctx.home });
  if (!credentials.token) {
    throw new SpeechError("no video tool token yet: run `node tools/video/cli.mjs login` and allow it on the admin card 「Azure 語音（影片旁白）」", { who: "owner" });
  }
  return credentials;
}

async function readSecret(ctx, prompt) {
  if (ctx.readSecret) return ctx.readSecret(prompt);
  if (!process.stdin.isTTY) {
    let data = "";
    for await (const chunk of process.stdin) data += chunk;
    return data.trim();
  }
  // Read without echoing, so the token does not stay on screen or in the terminal's scrollback.
  const input = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: true });
  process.stdout.write(prompt);
  input._writeToOutput = () => {};
  const answer = await new Promise((resolve) => input.question("", resolve));
  input.close();
  process.stdout.write("\n");
  return answer.trim();
}

/**
 * Pair with the site: print a code and a link to the admin card, wait for the owner to allow it,
 * and collect the token. The token is never printed, so this is safe to run for someone else.
 */
async function pairedToken(site, name, ctx) {
  const fetchImpl = ctx.fetch ?? globalThis.fetch;
  const started = await startPairing({ site, clientName: name ?? defaultClientName(), fetchImpl });
  const minutes = Math.round(started.expires_in / 60);
  ctx.stdout.write(
    `Open this link where you are signed in to the admin, check that the code matches, and choose 允許 (allow):\n` +
      `  ${site}${started.verification_path}\n` +
      `  code: ${started.user_code} (valid for ${minutes} minutes)\n` +
      `waiting for the owner to allow it...\n`,
  );
  const sleep = ctx.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
  const paired = await waitForPairing({ site, started, fetchImpl, sleep, now: ctx.now });
  ctx.stdout.write(`allowed; the admin card lists this token as 「${paired.token_name}」\n`);
  return paired.token;
}

async function login(args, ctx) {
  const values = parseArgs({
    args,
    options: { site: { type: "string" }, "token-file": { type: "string" }, paste: { type: "boolean" }, name: { type: "string" } },
    strict: true,
  }).values;
  const current = readCredentials({ env: {}, home: ctx.home });
  const site = (values.site ?? current.site).replace(/\/+$/, "");
  if (!validSite(`${site}/`)) throw new UsageError(`${site} is not an https site address`);
  let token;
  if (values["token-file"]) token = readFileSync(values["token-file"], "utf8").trim();
  else if (values.paste) token = await readSecret(ctx, "Paste the video tool token from the admin card (input is hidden): ");
  else token = await pairedToken(site, values.name, ctx);
  if (!TOKEN_PATTERN.test(token)) throw new UsageError("that does not look like a video tool token; it starts with mkv_");
  const status = await speechStatus(clientOptions(ctx, { site, token }));
  const file = writeCredentials({ site, token }, { home: ctx.home });
  ctx.stdout.write(`saved to ${file}\n`);
  ctx.stdout.write(`${site}: speech ${status.configured ? "configured" : "NOT configured yet (fill in the admin card)"}; voices ${status.voices.join(", ")}\n`);
  ctx.stdout.write(`this month: ${status.used ?? "?"} of ${status.monthly_limit || "unlimited"} billable characters\n`);
  return ctx.EXIT.ok;
}

function loadLexicon(root) {
  return readJson(lexiconFile(root), emptyLexicon());
}

/**
 * Why the server cannot narrate with this request voice right now, or null. Azure voices must be
 * on the admin card's allowlist; Gemini voices ("gemini:<name>") need only the site's Gemini key.
 */
function voiceProblem(status, voice) {
  if (voice.startsWith(GEMINI_VOICE_PREFIX)) {
    return status.gemini_configured ? null : "the site has no Gemini key yet (admin: API 與供應商設定 → AI 服務)";
  }
  if (!status.configured) return "the admin card 「Azure 語音（影片旁白）」 has no key or region yet";
  return status.voices.includes(voice) ? null : `voice ${voice} is not on the admin card's allowlist`;
}

/** Characters left this month for the provider a voice belongs to, or null when unlimited or unknown. */
function remainingFor(status, voice) {
  if (voice.startsWith(GEMINI_VOICE_PREFIX)) {
    return status.gemini_monthly_limit > 0 && status.gemini_used !== null ? status.gemini_monthly_limit - status.gemini_used : null;
  }
  return status.monthly_limit > 0 ? status.remaining : null;
}

async function audition(args, ctx) {
  const values = parseArgs({
    args,
    options: {
      "text-file": { type: "string" },
      voices: { type: "string" },
      rate: { type: "string", default: "+0%" },
      style: { type: "string" },
      model: { type: "string" },
      workdir: { type: "string" },
    },
    strict: true,
  }).values;
  if (!values["text-file"]) throw new UsageError("audition needs --text-file: a UTF-8 file with the sample narration");
  const text = readFileSync(values["text-file"], "utf8").replace(/^﻿/, "").trim();
  if (!text || text.length > MAX_REQUEST_CHARACTERS) throw new UsageError(`the sample must be 1 to ${MAX_REQUEST_CHARACTERS} characters`);
  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = await speechStatus(options);
  const voices = values.voices ? values.voices.split(",").map((voice) => voice.trim()).filter(Boolean) : status.voices;
  const problems = voices.map((voice) => voiceProblem(status, voice)).filter(Boolean);
  if (problems.length) throw new SpeechError([...new Set(problems)].join("; "), { who: "owner" });
  const stamp = ctx.now().toISOString().replace(/[:.]/g, "-");
  const out = path.join(resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home }), "_audition", stamp);
  mkdirSync(out, { recursive: true });
  const parts = spokenParts(text, loadLexicon(ctx.root));
  // "gemini:Sulafat" is not a valid Windows file name.
  const fileName = (voice) => `${voice.replace(/[^A-Za-z0-9_.-]/g, "-")}.wav`;
  let billable = 0;
  for (const voice of voices) {
    const fields = voice.startsWith(GEMINI_VOICE_PREFIX)
      ? voiceFields({ provider: "gemini", name: voice.slice(GEMINI_VOICE_PREFIX.length), style: values.style, model: values.model })
      : voiceFields({ provider: "azure", name: voice, rate: values.rate });
    const result = await synthesize({ ...options, body: { ...fields, segments: [{ parts, break_after_ms: 0 }] } });
    requireNarrationFormat(parseWav(result.wav));
    billable += result.billable;
    writeFileSync(path.join(out, fileName(voice)), result.wav);
    ctx.stdout.write(`${voice}: ${path.join(out, fileName(voice))}\n`);
  }
  const rows = voices.map((voice) => `<li><p>${escapeHtml(voice)}</p><audio controls preload="none" src="${encodeURIComponent(fileName(voice))}"></audio></li>`).join("");
  writeFileSync(
    path.join(out, "index.html"),
    `<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>試聽</title><style>body{font-family:system-ui,sans-serif;margin:2rem;max-width:48rem}li{margin:1rem 0}audio{width:100%}</style><h1>旁白試聽</h1><p>${escapeHtml(text)}</p><ol>${rows}</ol></html>\n`,
  );
  ctx.stdout.write(`${voices.length} voices, ${billable} billable characters; open ${path.join(out, "index.html")}\n`);
  return ctx.EXIT.ok;
}

function readCache(workdir) {
  return readJson(path.join(workdir, ARTIFACTS.audio, "cache.json"), { lines: {} });
}

async function tts(args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, "dry-run": { type: "boolean" }, redo: { type: "string" }, force: { type: "boolean" } },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("tts needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${project.doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const { doc, lexicon } = project;
  const voice = voiceFields(doc.voice).voice;
  const requests = planRequests(doc, lexicon);
  const estimate = requests.reduce((sum, request) => sum + billableForRequest(request.body), 0);
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const cache = readCache(workdir);
  const redo = values.redo ? flaggedLines(readJson(path.resolve(values.redo))) : new Set();
  const audioDir = path.join(workdir, ARTIFACTS.audio);
  const current = (request) =>
    !values.force && !request.lines.some((line) => redo.has(line.id)) && request.lines.every((line) => cache.lines[line.id] === request.key && existsSync(path.join(audioDir, `${line.id}.wav`)));
  const pending = requests.filter((request) => !current(request));
  const pendingEstimate = pending.reduce((sum, request) => sum + billableForRequest(request.body), 0);

  if (values["dry-run"]) {
    ctx.stdout.write(`${requests.length} requests, ${pending.length} to synthesize; about ${pendingEstimate} billable characters now (${estimate} for the whole video, ${((estimate / FREE_TIER) * 100).toFixed(1)}% of the free tier)\n`);
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    if (credentials.token) {
      const status = await speechStatus(clientOptions(ctx, credentials));
      const problem = voiceProblem(status, voice);
      const remaining = remainingFor(status, voice);
      ctx.stdout.write(`server: voice ${voice} ${problem ? `NOT ready: ${problem}` : "ready"}; ${remaining === null ? "no monthly limit" : `${remaining} characters left this month`}\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before synthesizing\n");
    }
    return EXIT.ok;
  }

  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  if (pending.length) {
    const status = await speechStatus(options);
    const problem = voiceProblem(status, voice);
    if (problem) throw new SpeechError(problem, { who: "owner" });
    const remaining = remainingFor(status, voice);
    if (remaining !== null && pendingEstimate > remaining) {
      throw new SpeechError(`about ${pendingEstimate} billable characters needed, ${remaining} left this month`, { code: "video_speech_budget_exhausted" });
    }
  }
  mkdirSync(audioDir, { recursive: true });
  let billable = 0;
  const fallbacks = [];
  for (const request of pending) {
    if (stopRequested(workdir)) {
      ctx.stdout.write(`stopped by the STOP file; ${pending.indexOf(request)} of ${pending.length} requests done, rerun to continue\n`);
      return EXIT.ok;
    }
    const result = await synthesizeRequest(request, (body) => synthesize({ ...options, body }));
    billable += result.billable;
    if (result.fallback) fallbacks.push(request.id);
    for (const [id, clip] of result.clips) {
      atomicWrite(path.join(audioDir, `${id}.wav`), encodeWav(clip));
      cache.lines[id] = request.key;
    }
    atomicWrite(path.join(audioDir, "cache.json"), `${JSON.stringify(cache, null, 2)}\n`);
    ctx.stdout.write(`${request.id}: ${request.lines.length} lines${result.fallback ? " (split did not match the text; synthesized line by line)" : ""}\n`);
  }

  const clips = new Map();
  for (const request of requests) {
    for (const line of request.lines) clips.set(line.id, requireNarrationFormat(parseWav(readFileSync(path.join(audioDir, `${line.id}.wav`)))));
  }
  const samplesById = Object.fromEntries([...clips].map(([id, clip]) => [id, Math.max(1, clip.length)]));
  const timeline = { ...buildTimeline(doc, samplesById), speech_hash: speechHash(doc, lexicon) };
  // A clip trimmed to nothing still needs one sample to sit on the grid.
  for (const [id, clip] of clips) if (clip.length === 0) clips.set(id, new Int16Array(1));
  atomicWrite(path.join(workdir, ARTIFACTS.narration), encodeWav(buildNarration(timeline, clips)));
  atomicWrite(path.join(workdir, ARTIFACTS.timeline), `${JSON.stringify(timeline, null, 2)}\n`);
  recordStage(workdir, "tts", { requests: requests.length, synthesized: pending.length, fallbacks, billable, voice: doc.voice.name }, ctx.now());

  ctx.stdout.write(`${pending.length} requests synthesized (${billable} billable characters), ${requests.length - pending.length} reused; narration ${formatClock(frameToSeconds(timeline.total_frames))}\n`);
  for (const problem of checkChapters(timeline)) ctx.stdout.write(`chapters: ${problem}\n`);
  if (fallbacks.length) ctx.stdout.write(`line-by-line fallback for: ${fallbacks.join(", ")}\n`);
  ctx.stdout.write(`next: node tools/video/cli.mjs review --slug ${doc.slug}\n`);
  return EXIT.ok;
}

export async function run(command, args, ctx) {
  try {
    if (command === "login") return await login(args, ctx);
    if (command === "audition") return await audition(args, ctx);
    return await tts(args, ctx);
  } catch (error) {
    if (!(error instanceof SpeechError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return exitFor(error, ctx.EXIT);
  }
}
