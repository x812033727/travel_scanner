// An imported episode's line-by-line voice takes, packed so the upload package can carry them to
// the host's Drive backup (tasks/open/2026-11-01-zhong-tian-the-line-recordings-travel.md).
//
// The workdir that made an episode (zhong-tian-qu-qi-eNNN-dh/) keeps one wav per line in audio/
// (the zh-TW voice) and audio-<locale>/ (each dub, with a <line>.json beside it naming the text,
// style and voice it was recorded from). They are what a later fix of one line needs: a new
// recording does not sound the same. The workdir goes with the cloud session, so `import
// --publish` sends them too, as one wav a locale (every line's samples one after another, a file
// anyone can play) and a manifest that cuts it back into the original files byte for byte.
// The roles are recording_<locale> (audio/wav) and recordings_manifest (application/json):
// content types the site already takes, so no review needs a new kind of file.
//
// Since 2026-11-05 the takes as they went into the cut travel too (owner): segments-v4/lines/ (each
// zh-TW line fitted to its slot) and segments-v4/dub-<locale>/ (each line's .raw.wav and tempo-fitted
// .wav, the whole dialogue.wav and fit.json, which says where each line starts and at what tempo),
// as fit-lines.wav and fit-<locale>.wav (role recording_fit-…) in the same manifest. Without them a
// fix of one dubbed line meant refitting the episode's whole dialogue track.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";

export const MANIFEST_VERSION = 2;
const LOCALE = /^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})?$/;
const LINE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/;
// A fitted folder's files: zq35a01.wav, zq35a01.raw.wav, _s01.wav (a scene's silence), dialogue.wav.
const FITTED_LINE = /^[A-Za-z0-9_][A-Za-z0-9_-]{0,63}(?:\.raw)?$/;
// The text files a fitted folder keeps beside its wavs (fit.json), carried whole in the manifest.
const FITTED_TEXT = /^[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}\.(?:json|txt)$/;
const MAX_TEXT_BYTES = 1024 * 1024;
const SEGMENTS = /^segments(?:-v(\d+))?$/;
const FITTED_FOLDER = /^segments(?:-v\d+)?\/(?:lines|dub-[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})?)$/;
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

/** The RIFF chunks of a wav: { fmt, dataStart, dataLength } or a reason it is not one. */
export function wavParts(bytes) {
  if (bytes.length < 12 || bytes.toString("latin1", 0, 4) !== "RIFF" || bytes.toString("latin1", 8, 12) !== "WAVE") return { problem: "not a RIFF WAVE file" };
  let fmt = null;
  for (let i = 12; i + 8 <= bytes.length;) {
    const id = bytes.toString("latin1", i, i + 4);
    const size = bytes.readUInt32LE(i + 4);
    if (id === "fmt ") fmt = bytes.subarray(i + 8, i + 8 + size);
    if (id === "data") {
      if (!fmt) return { problem: "data before fmt" };
      if (i + 8 + size > bytes.length) return { problem: "data runs past the end" };
      return { fmt, dataStart: i + 8, dataLength: size };
    }
    i += 8 + size + (size & 1);
  }
  return { problem: "no data chunk" };
}

/** A wav file holding these samples in this format. */
export function wavFile(fmt, data) {
  const head = Buffer.alloc(20);
  head.write("RIFF", 0, "latin1");
  head.writeUInt32LE(4 + 8 + fmt.length + 8 + data.length, 4);
  head.write("WAVE", 8, "latin1");
  head.write("fmt ", 12, "latin1");
  head.writeUInt32LE(fmt.length, 16);
  const dataHead = Buffer.alloc(8);
  dataHead.write("data", 0, "latin1");
  dataHead.writeUInt32LE(data.length, 4);
  return Buffer.concat([head, fmt, dataHead, data]);
}

/** The recording folders of an episode workdir: [{ locale, dir }], zh-TW first. */
export function recordingDirs(workdir) {
  if (!workdir || !existsSync(workdir)) return [];
  const out = [];
  for (const name of readdirSync(workdir).sort()) {
    const dir = path.join(workdir, name);
    if (!statSync(dir).isDirectory()) continue;
    if (name === "audio") out.unshift({ locale: "zh-TW", dir });
    else if (name.startsWith("audio-") && LOCALE.test(name.slice(6))) out.push({ locale: name.slice(6), dir });
  }
  return out;
}

/**
 * The fitted folders of an episode workdir, from its newest segments folder (segments-v4 over
 * segments): [{ key, dir, folder }], key fit-lines for lines/ and fit-<locale> for dub-<locale>/,
 * folder the path from the workdir.
 */
export function fittedDirs(workdir) {
  if (!workdir || !existsSync(workdir)) return [];
  const segments = readdirSync(workdir)
    .filter((name) => SEGMENTS.test(name) && statSync(path.join(workdir, name)).isDirectory())
    .sort((a, b) => Number(SEGMENTS.exec(a)[1] ?? 0) - Number(SEGMENTS.exec(b)[1] ?? 0))
    .at(-1);
  if (!segments) return [];
  const out = [];
  for (const name of readdirSync(path.join(workdir, segments)).sort()) {
    const dir = path.join(workdir, segments, name);
    if (!statSync(dir).isDirectory()) continue;
    if (name === "lines") out.unshift({ key: "fit-lines", dir, folder: `${segments}/lines` });
    else if (name.startsWith("dub-") && LOCALE.test(name.slice(4))) out.push({ key: `fit-${name.slice(4)}`, dir, folder: `${segments}/${name}` });
  }
  return out;
}

/** One folder's wavs joined: { fmt, data, lines, texts } or null when it holds none. */
function packFolder(dir, folder, problems, { line, sidecars }) {
  const lines = [];
  const chunks = [];
  const texts = {};
  let fmt = null;
  let offset = 0;
  for (const name of readdirSync(dir).sort()) {
    if (!sidecars && FITTED_TEXT.test(name)) {
      const bytes = readFileSync(path.join(dir, name));
      if (bytes.length > MAX_TEXT_BYTES) problems.push(`${folder}/${name}: larger than 1 MB`);
      else texts[name] = bytes.toString("utf8");
      continue;
    }
    if (!name.toLowerCase().endsWith(".wav")) continue;
    const id = name.slice(0, -4);
    if (!line.test(id)) { problems.push(`${folder}/${name}: a line's name is letters, digits, - or _`); continue; }
    const bytes = readFileSync(path.join(dir, name));
    const parts = wavParts(bytes);
    if (parts.problem) { problems.push(`${folder}/${name}: ${parts.problem}`); continue; }
    if (fmt && !fmt.equals(parts.fmt)) { problems.push(`${folder}/${name}: its format differs from the folder's other lines`); continue; }
    fmt ??= Buffer.from(parts.fmt);
    const data = bytes.subarray(parts.dataStart, parts.dataStart + parts.dataLength);
    const sidecar = path.join(dir, `${id}.json`);
    lines.push({
      id,
      offset,
      length: data.length,
      head: bytes.subarray(0, parts.dataStart).toString("base64"),
      tail: bytes.subarray(parts.dataStart + parts.dataLength).toString("base64"),
      sha256: sha256(bytes),
      ...(sidecars && existsSync(sidecar) ? { sidecar: readFileSync(sidecar, "utf8") } : {}),
    });
    chunks.push(data);
    offset += data.length;
  }
  if (!lines.length) return null;
  return { fmt, data: Buffer.concat(chunks), lines, texts };
}

/**
 * Pack an episode workdir's recordings into outDir: <locale>.wav for each recording folder,
 * fit-<key>.wav for each fitted folder, and manifest.json. Returns { files: [{ file, role,
 * content_type }], manifest, problems }; nothing is written when there is a problem or no recording
 * at all.
 */
export function packRecordings(workdir, outDir) {
  const problems = [];
  const locales = {};
  const fitted = {};
  const joined = {};
  for (const { locale, dir } of recordingDirs(workdir)) {
    const packed = packFolder(dir, path.basename(dir), problems, { line: LINE, sidecars: true });
    if (!packed) continue;
    joined[locale] = wavFile(packed.fmt, packed.data);
    locales[locale] = { folder: path.basename(dir), sha256: sha256(joined[locale]), lines: packed.lines };
  }
  if (Object.keys(locales).length) {
    for (const { key, dir, folder } of fittedDirs(workdir)) {
      const packed = packFolder(dir, folder, problems, { line: FITTED_LINE, sidecars: false });
      if (!packed) continue;
      joined[key] = wavFile(packed.fmt, packed.data);
      fitted[key] = { folder, sha256: sha256(joined[key]), lines: packed.lines, ...(Object.keys(packed.texts).length ? { texts: packed.texts } : {}) };
    }
  }
  if (problems.length || !Object.keys(locales).length) return { files: [], manifest: null, problems };
  mkdirSync(outDir, { recursive: true });
  const files = [];
  for (const [key, bytes] of Object.entries(joined)) {
    const file = path.join(outDir, `${key}.wav`);
    writeFileSync(file, bytes);
    files.push({ file, role: `recording_${key}`, content_type: "audio/wav" });
  }
  const manifest = { schema_version: MANIFEST_VERSION, kind: "line-recordings", locales, ...(Object.keys(fitted).length ? { fitted } : {}) };
  const file = path.join(outDir, "manifest.json");
  writeFileSync(file, `${JSON.stringify(manifest, null, 1)}\n`);
  files.unshift({ file, role: "recordings_manifest", content_type: "application/json" });
  return { files, manifest, problems };
}

/**
 * Cut a packed folder (manifest.json, <locale>.wav and fit-<key>.wav) back into the workdir's
 * folders: every line's wav, byte for byte, its .json beside it, and a fitted folder's fit.json. Refuses a wav whose hash is not the manifest's.
 * Returns the number of files written.
 *   node tools/video/import/recordings.mjs unpack <packed dir> <episode workdir>
 */
export function unpackRecordings(packedDir, workdir) {
  const manifest = JSON.parse(readFileSync(path.join(packedDir, "manifest.json"), "utf8"));
  if (![1, MANIFEST_VERSION].includes(manifest?.schema_version) || manifest.kind !== "line-recordings") throw new Error("not a line-recordings manifest");
  let written = 0;
  const cut = (key, entry, folder, line) => {
    const joined = readFileSync(path.join(packedDir, `${key}.wav`));
    if (sha256(joined) !== entry.sha256) throw new Error(`${key}.wav is not the one the manifest names`);
    const parts = wavParts(joined);
    if (parts.problem) throw new Error(`${key}.wav: ${parts.problem}`);
    const data = joined.subarray(parts.dataStart, parts.dataStart + parts.dataLength);
    const dir = path.join(workdir, ...folder.split("/"));
    mkdirSync(dir, { recursive: true });
    for (const each of entry.lines) {
      if (!line.test(each.id)) throw new Error(`bad line ${each.id}`);
      const bytes = Buffer.concat([Buffer.from(each.head, "base64"), data.subarray(each.offset, each.offset + each.length), Buffer.from(each.tail, "base64")]);
      if (sha256(bytes) !== each.sha256) throw new Error(`${folder}/${each.id}.wav does not come back as it was`);
      writeFileSync(path.join(dir, `${each.id}.wav`), bytes);
      written++;
      if (typeof each.sidecar === "string") { writeFileSync(path.join(dir, `${each.id}.json`), each.sidecar); written++; }
    }
    for (const [name, text] of Object.entries(entry.texts ?? {})) {
      if (!FITTED_TEXT.test(name) || typeof text !== "string") throw new Error(`bad file ${folder}/${name}`);
      writeFileSync(path.join(dir, name), text);
      written++;
    }
  };
  for (const [locale, entry] of Object.entries(manifest.locales ?? {})) {
    if (!LOCALE.test(locale) && locale !== "zh-TW") throw new Error(`bad locale ${locale}`);
    const folder = path.basename(String(entry.folder));
    if (folder !== "audio" && !(folder.startsWith("audio-") && LOCALE.test(folder.slice(6)))) throw new Error(`bad folder ${entry.folder}`);
    cut(locale, entry, folder, LINE);
  }
  for (const [key, entry] of Object.entries(manifest.fitted ?? {})) {
    if (!/^fit-(?:lines|[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})?)$/.test(key)) throw new Error(`bad fitted folder ${key}`);
    const folder = String(entry.folder);
    if (!FITTED_FOLDER.test(folder)) throw new Error(`bad folder ${entry.folder}`);
    cut(key, entry, folder, FITTED_LINE);
  }
  return written;
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) {
  const [command, from, to] = process.argv.slice(2);
  if (command === "unpack" && from && to) console.log(`${unpackRecordings(from, to)} file(s) written to ${to}`);
  else if (command === "pack" && from && to) {
    const { files, problems } = packRecordings(from, to);
    if (problems.length) { console.error(problems.join("\n")); process.exit(2); }
    console.log(`${files.length} file(s) in ${to}`);
  } else {
    console.error("usage: node tools/video/import/recordings.mjs pack <episode workdir> <out dir> | unpack <packed dir> <episode workdir>");
    process.exit(2);
  }
}
