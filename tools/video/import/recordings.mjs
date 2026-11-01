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
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";

export const MANIFEST_VERSION = 1;
const LOCALE = /^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})?$/;
const LINE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/;
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
 * Pack an episode workdir's recordings into outDir: <locale>.wav for each folder and manifest.json.
 * Returns { files: [{ file, role, content_type }], manifest, problems }; nothing is written when
 * there is a problem or no recording at all.
 */
export function packRecordings(workdir, outDir) {
  const problems = [];
  const locales = {};
  const joined = {};
  for (const { locale, dir } of recordingDirs(workdir)) {
    const lines = [];
    const chunks = [];
    let fmt = null;
    let offset = 0;
    for (const name of readdirSync(dir).sort()) {
      if (!name.toLowerCase().endsWith(".wav")) continue;
      const id = name.slice(0, -4);
      if (!LINE.test(id)) { problems.push(`${path.basename(dir)}/${name}: a line's name is letters, digits, - or _`); continue; }
      const bytes = readFileSync(path.join(dir, name));
      const parts = wavParts(bytes);
      if (parts.problem) { problems.push(`${path.basename(dir)}/${name}: ${parts.problem}`); continue; }
      if (fmt && !fmt.equals(parts.fmt)) { problems.push(`${path.basename(dir)}/${name}: its format differs from the folder's other lines`); continue; }
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
        ...(existsSync(sidecar) ? { sidecar: readFileSync(sidecar, "utf8") } : {}),
      });
      chunks.push(data);
      offset += data.length;
    }
    if (!lines.length) continue;
    joined[locale] = wavFile(fmt, Buffer.concat(chunks));
    locales[locale] = { folder: path.basename(dir), sha256: sha256(joined[locale]), lines };
  }
  if (problems.length || !Object.keys(locales).length) return { files: [], manifest: null, problems };
  mkdirSync(outDir, { recursive: true });
  const files = [];
  for (const [locale, bytes] of Object.entries(joined)) {
    const file = path.join(outDir, `${locale}.wav`);
    writeFileSync(file, bytes);
    files.push({ file, role: `recording_${locale}`, content_type: "audio/wav" });
  }
  const manifest = { schema_version: MANIFEST_VERSION, kind: "line-recordings", locales };
  const file = path.join(outDir, "manifest.json");
  writeFileSync(file, `${JSON.stringify(manifest, null, 1)}\n`);
  files.unshift({ file, role: "recordings_manifest", content_type: "application/json" });
  return { files, manifest, problems };
}

/**
 * Cut a packed folder (manifest.json and <locale>.wav) back into the workdir's folders: every line's
 * wav, byte for byte, and its .json beside it. Refuses a wav whose hash is not the manifest's.
 * Returns the number of files written.
 *   node tools/video/import/recordings.mjs unpack <packed dir> <episode workdir>
 */
export function unpackRecordings(packedDir, workdir) {
  const manifest = JSON.parse(readFileSync(path.join(packedDir, "manifest.json"), "utf8"));
  if (manifest?.schema_version !== MANIFEST_VERSION || manifest.kind !== "line-recordings") throw new Error("not a line-recordings manifest");
  let written = 0;
  for (const [locale, entry] of Object.entries(manifest.locales ?? {})) {
    if (!LOCALE.test(locale) && locale !== "zh-TW") throw new Error(`bad locale ${locale}`);
    const joined = readFileSync(path.join(packedDir, `${locale}.wav`));
    if (sha256(joined) !== entry.sha256) throw new Error(`${locale}.wav is not the one the manifest names`);
    const parts = wavParts(joined);
    if (parts.problem) throw new Error(`${locale}.wav: ${parts.problem}`);
    const data = joined.subarray(parts.dataStart, parts.dataStart + parts.dataLength);
    const folder = path.basename(String(entry.folder));
    if (folder !== "audio" && !(folder.startsWith("audio-") && LOCALE.test(folder.slice(6)))) throw new Error(`bad folder ${entry.folder}`);
    const dir = path.join(workdir, folder);
    mkdirSync(dir, { recursive: true });
    for (const line of entry.lines) {
      if (!LINE.test(line.id)) throw new Error(`bad line ${line.id}`);
      const bytes = Buffer.concat([Buffer.from(line.head, "base64"), data.subarray(line.offset, line.offset + line.length), Buffer.from(line.tail, "base64")]);
      if (sha256(bytes) !== line.sha256) throw new Error(`${folder}/${line.id}.wav does not come back as it was`);
      writeFileSync(path.join(dir, `${line.id}.wav`), bytes);
      written++;
      if (typeof line.sidecar === "string") { writeFileSync(path.join(dir, `${line.id}.json`), line.sidecar); written++; }
    }
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
