// The upload package's own check (docs/videos/HANDS-OFF.md §上傳包與「可以上架」): the four items
// the site requires on a publish review before it approves the upload confirmation without the
// owner — the files, a description per locale, a caption file per locale (or a reason it was
// skipped) and the disclosure answer. The report has the shape of the quality check's
// (`{ ok, final_sha256, items }`); here `final_sha256` is the hash of upload/metadata.json, the
// file the publish gate binds to, since that is what the server compares it with.
//
// Every item is a pure function over what was read from upload/; `readPackageReport` does the
// reading and hashing. `package` runs it after writing the files, and `review-push --gate publish`
// runs it again to send a fresh report.
//
// With the owner's language choice (languages.json, docs/videos/LANGUAGES.md) a package carries
// exactly the chosen parts: a description, caption file, dub track or language thumbnail of a
// locale nobody chose fails, and so does a metadata.json written for another choice, so a broader
// package from before cannot pass as the current delivery. Without a choice (a video from before
// the panel) nothing extra is refused, as before.
import { createHash } from "node:crypto";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";

import { readApprovals, sha256File } from "../core/approvals.mjs";
import { appliedBranding, brandingCurrent, readBranding } from "../core/branding.mjs";
import { readJson } from "../core/paths.mjs";
import { LOCALES, NARRATION_LOCALE } from "../core/schema.mjs";
import { captionLocalesOf, chosenLocales, LOCALE_PARTS, metadataLocalesOf, readLanguages } from "../core/stages.mjs";

/** The four items, in the order the report lists them; the server requires every one of them. */
export const PACKAGE_ITEM_IDS = ["files", "descriptions", "captions", "disclosure"];
export const UPLOAD_DIR = "upload";
export const METADATA_FILE = "metadata.json";
export const FINAL_FILE = "final.mp4";
export const THUMBNAIL_FILE = "thumbnail.jpg";
// Reviews attach the package under these roles; the description and caption files add their locale.
const ROLE_TYPES = { final: "video/mp4", thumbnail: "image/jpeg", metadata: "application/json" };
const CAPTION_FILE = /^captions\/([A-Za-z-]+)\.srt$/;
const DESCRIPTION_FILE = /^description\.([A-Za-z-]+)\.txt$/;
// A dub track as package copies it: dubs/<locale>.<format> (docs/videos/DUBS.md).
const DUB_FILE = /^dubs\/([A-Za-z-]+)\.[A-Za-z0-9]+$/;
// A language's own thumbnail, for Studio's 「語言」 page (role thumbnail_en beside thumbnail).
const LOCALE_THUMBNAIL_FILE = /^thumbnails\/([A-Za-z-]+)\.jpg$/;
// Variants B and C for Studio's 「測試與比較」, beside thumbnail.jpg (A); render's
// thumbnailVariantFile names them. Their role keeps the file's hyphen (thumbnail-b), so the
// site's cards, which read thumbnail_<locale> as a language, never take one for a locale.
const VARIANT_THUMBNAIL_FILE = /^thumbnail-([a-z])\.jpg$/;
// YouTube's limit for a thumbnail, which every image in the package keeps.
export const THUMBNAIL_MAX_BYTES = 2 * 1024 * 1024;

/**
 * The thumbnail variants render listed in frames/manifest.json (`thumbnail_variants`), as file
 * names beside thumbnail.jpg; anything else in that list is ignored. Empty without variants.
 */
export function thumbnailVariants(framesManifest) {
  const listed = framesManifest?.thumbnail_variants;
  return Array.isArray(listed) ? listed.filter((file) => typeof file === "string" && VARIANT_THUMBNAIL_FILE.test(file)) : [];
}

/** The review role of a variant's file: thumbnail-b.jpg goes up as thumbnail-b. */
export const variantRole = (file) => path.posix.basename(file, ".jpg");

export function item(id, ok, detail) {
  return { id, ok: Boolean(ok), detail: String(detail) };
}

/** The report the server reads: { ok, final_sha256, items }, items in PACKAGE_ITEM_IDS order. */
export function packageReport(items, metadataSha256) {
  const ids = items.map((each) => each.id);
  if (ids.length !== PACKAGE_ITEM_IDS.length || ids.some((id, index) => id !== PACKAGE_ITEM_IDS[index])) {
    throw new Error(`package items must be exactly ${PACKAGE_ITEM_IDS.join(", ")}; got ${ids.join(", ")}`);
  }
  return { ok: items.every((each) => each.ok), final_sha256: metadataSha256 ?? null, items };
}

const sizeOf = (files, name) => files.get(name) ?? null;
const present = (files, name) => sizeOf(files, name) !== null;

// metadata.json as `package` writes it: an object whose lists are arrays and whose maps (locale
// → entry) are objects. A hand-edited one may break that ("captions": 5), and the check then fails
// the item that reads the field, naming it, instead of throwing out of review-push or reading a
// string's characters as entries. An absent (or null) field reads as empty, as before.
const isObject = (value) => Boolean(value) && typeof value === "object" && !Array.isArray(value);

/** Why the items cannot read metadata.json (missing, or not an object), or null when they can. */
const metadataProblem = (metadata) => (!metadata ? `${METADATA_FILE} is missing` : isObject(metadata) ? null : `${METADATA_FILE} is not an object; run package again`);

/** metadata.json's list `field`, or [] without one; a field of another type also adds a problem naming it. */
function listField(metadata, field, problems = []) {
  const value = metadata?.[field] ?? null;
  if (Array.isArray(value)) return value;
  if (value !== null) problems.push(`${METADATA_FILE} ${field} is not a list; run package again`);
  return [];
}

/** metadata.json's map `field`, or {} without one; a field of another type also adds a problem naming it. */
function mapField(metadata, field, problems = []) {
  const value = metadata?.[field] ?? null;
  if (isObject(value)) return value;
  if (value !== null) problems.push(`${METADATA_FILE} ${field} is not an object; run package again`);
  return {};
}

/** The narration locale metadata.json names as its default_language; zh-TW without a known one. */
const narrationOf = (metadata) => (LOCALES.includes(metadata?.default_language) ? metadata.default_language : NARRATION_LOCALE);

/** [locale, path] for each of `paths` that `pattern` matches, its first group being the locale. */
const localesOf = (paths, pattern) => [...paths].flatMap((file) => {
  const match = pattern.exec(String(file));
  return match ? [[match[1], file]] : [];
});

/**
 * The parts found ([locale, where]) of locales outside `allowed`, as "en (description.en.txt,
 * localizations.en)", one entry per locale in the order found; empty when every part is allowed.
 */
function unchosen(found, allowed) {
  const extra = new Map();
  for (const [locale, where] of found) if (!allowed.includes(locale)) extra.set(locale, [...new Set([...(extra.get(locale) ?? []), where])]);
  return [...extra].map(([locale, where]) => `${locale} (${where.join(", ")})`);
}
const unchosenProblem = (what, extra) => `${what} the language choice does not have: ${extra.join(", ")}; run package again`;

/** Whether `part` is ticked for `locale` in a choice's locales, read as readLanguages reads it: a dub chooses its captions. */
function ticked(locales, locale, part) {
  const choice = locales?.[locale];
  return Boolean(choice) && typeof choice === "object" && (choice[part] === true || (part === "captions" && choice.dub === true));
}

/** Whether two choices' locales tick the same parts; zh-TW, which the panel never offers, is left out as readLanguages leaves it out. */
const sameChoice = (a, b) => LOCALES.filter((locale) => locale !== NARRATION_LOCALE).every((locale) => LOCALE_PARTS.every((part) => ticked(a, locale, part) === ticked(b, locale, part)));

/**
 * With the owner's choice (`languages`, as readLanguages returns it): metadata.json records that
 * very choice in language_choice (youtube-sync and the card read it; one without the field reads
 * as a choice of nothing beyond the narration and zh-TW), and the dub tracks and the
 * language thumbnails are of chosen locales only, as package writes them. A chosen dub may be
 * absent: still being made, given up with its reason in skipped_dub_locales, or a compilation's,
 * which has none. A track or a thumbnail of a locale nobody chose may not be there, nor a track
 * metadata.json does not list. `thumbnails` is metadata.json's map as filesItem read it.
 */
function choiceProblems({ files, metadata, languages, thumbnails }) {
  const problems = [];
  if (!sameChoice(mapField(metadata, "language_choice", problems), languages.locales)) problems.push(`${METADATA_FILE} was written for another language choice; run package again`);
  const narration = narrationOf(metadata);
  const dubLocales = chosenLocales(languages, "dub").filter((locale) => locale !== narration);
  const listed = listField(metadata, "dubs", problems);
  const tracks = localesOf(files.keys(), DUB_FILE);
  for (const dub of listed) if (!present(files, dub?.file)) problems.push(`${dub?.file} is listed but missing`);
  for (const [, file] of tracks) if (!listed.some((dub) => dub?.file === file)) problems.push(`${file} is not listed in ${METADATA_FILE}`);
  const extraDubs = unchosen([...listed.map((dub) => [dub?.locale, dub?.file]), ...tracks], dubLocales);
  if (extraDubs.length) problems.push(unchosenProblem("dub tracks", extraDubs));
  // A language's own thumbnail goes with any part chosen for it (package's youtubeLocales).
  const thumbnailLocales = [...captionLocalesOf(languages, narration), ...(metadataLocalesOf(languages, narration) ?? []), ...dubLocales].filter((locale) => locale !== narration);
  const extraThumbnails = unchosen([...Object.entries(thumbnails), ...localesOf(files.keys(), LOCALE_THUMBNAIL_FILE)], thumbnailLocales);
  if (extraThumbnails.length) problems.push(unchosenProblem("language thumbnails", extraThumbnails));
  return problems;
}

/**
 * files: final.mp4 is there and is the approved final (its hash equals the final gate's and the
 * one metadata.json records), thumbnail.jpg is there when the video has one, metadata.json is
 * there. `files` maps each path under upload/ (posix, relative) to its size. With the owner's
 * choice (`languages`) the dub tracks, language thumbnails and metadata.json's language_choice
 * agree with it (choiceProblems); `unchanged` is false when upload/ changed while it was read.
 */
export function filesItem({ files, metadata: read, finalSha256, approvedSha256, brandingMatches = true, languages = null, unchanged = true }) {
  const problems = [];
  if (!unchanged) problems.push(`${UPLOAD_DIR}/ or the language choice changed while the package was being checked; check it again`);
  const unreadable = metadataProblem(read);
  if (unreadable) problems.push(unreadable);
  const metadata = unreadable ? null : read;
  if (!present(files, FINAL_FILE)) problems.push(`${FINAL_FILE} is missing`);
  else if (!approvedSha256) problems.push("no approved final to compare final.mp4 with");
  else if (finalSha256 !== approvedSha256) problems.push(`${FINAL_FILE} is not the approved final (${String(finalSha256).slice(0, 12)} vs ${approvedSha256.slice(0, 12)})`);
  else if (metadata && metadata.final_sha256 !== finalSha256) problems.push(`${METADATA_FILE} records another final (${String(metadata.final_sha256).slice(0, 12)})`);
  if (metadata?.thumbnail && !present(files, THUMBNAIL_FILE)) problems.push(`${THUMBNAIL_FILE} is missing`);
  // Each language's own thumbnail metadata.json lists is there; the languages without one are only noted.
  const thumbnails = mapField(metadata, "thumbnails", problems);
  for (const listed of Object.values(thumbnails)) if (!present(files, listed)) problems.push(`${listed} is listed but missing`);
  // So is each "Test & compare" variant, B and C beside A.
  const variants = listField(metadata, "thumbnail_variants", problems);
  for (const listed of variants) if (!present(files, listed)) problems.push(`${listed} is listed but missing`);
  // Every thumbnail stays within YouTube's 2 MB, A as much as its variants and languages.
  for (const image of [...(metadata?.thumbnail ? [THUMBNAIL_FILE] : []), ...variants, ...Object.values(thumbnails)]) {
    if (sizeOf(files, image) > THUMBNAIL_MAX_BYTES) problems.push(`${image} is ${sizeOf(files, image)} bytes; YouTube's limit is 2 MB`);
  }
  if (!brandingMatches) problems.push("the upload package does not match the selected and applied branding; rebuild the final and run package again");
  if (languages && metadata) problems.push(...choiceProblems({ files, metadata, languages, thumbnails }));
  if (problems.length) return item("files", false, problems.join("; "));
  const named = [FINAL_FILE, ...(metadata.thumbnail ? [THUMBNAIL_FILE] : []), ...variants, ...Object.values(thumbnails), METADATA_FILE];
  return item("files", true, `${named.join(", ")}; ${FINAL_FILE} is the approved final (${finalSha256.slice(0, 12)})`);
}

/** The locales a package describes: the default language and every localization (none when localizations is not an object). */
export function packageLocales(metadata) {
  return [metadata?.default_language ?? "zh-TW", ...Object.keys(mapField(metadata, "localizations"))];
}

/**
 * descriptions: a non-empty description.<locale>.txt for the default language and every
 * localization, or, with `locales` (the narration, zh-TW and the locales the owner chose titles
 * and descriptions for), for exactly those: a chosen locale without its file fails, whatever
 * metadata.json lists. `strict` (the owner's choice is known) also fails a description file, a
 * localization or a default_language of a locale outside `locales`.
 */
export function descriptionsItem({ files, metadata, locales = null, strict = false }) {
  const unreadable = metadataProblem(metadata);
  if (unreadable) return item("descriptions", false, unreadable);
  const problems = [];
  const localizations = mapField(metadata, "localizations", problems);
  const wanted = locales ?? packageLocales(metadata);
  const missing = wanted.filter((locale) => !(sizeOf(files, `description.${locale}.txt`) > 0));
  if (missing.length) problems.push(`no description for ${missing.join(", ")}`);
  if (strict && locales) {
    const found = [...localesOf(files.keys(), DESCRIPTION_FILE), ...Object.keys(localizations).map((locale) => [locale, `localizations.${locale}`]), [packageLocales(metadata)[0], "default_language"]];
    const extra = unchosen(found, locales);
    if (extra.length) problems.push(unchosenProblem("titles and descriptions", extra));
  }
  if (problems.length) return item("descriptions", false, problems.join("; "));
  return item("descriptions", true, `descriptions for ${wanted.join(", ")}`);
}

/** Why a locale has no caption file, from metadata.json's skipped_caption_locales, or null. */
export function skipReason(skipped, locale) {
  const entry = skipped?.[locale];
  if (Array.isArray(entry) && entry.length) return `${entry.length} lines missing or older than zh-TW`;
  if (typeof entry === "string" && entry.trim()) return entry.trim();
  return null;
}

/**
 * captions: an .srt per configured caption locale, or the locale listed in
 * skipped_caption_locales with a reason; and every file metadata.json lists is there. `strict`
 * (the owner's choice is known) also fails a caption file there or listed of a locale outside
 * `locales`.
 */
export function captionsItem({ files, metadata, locales = LOCALES, strict = false }) {
  const unreadable = metadataProblem(metadata);
  if (unreadable) return item("captions", false, unreadable);
  const problems = [];
  const captions = listField(metadata, "captions", problems);
  const reasons = mapField(metadata, "skipped_caption_locales", problems);
  const written = [];
  const skipped = [];
  for (const locale of locales) {
    if (sizeOf(files, `captions/${locale}.srt`) > 0) {
      written.push(locale);
      continue;
    }
    const reason = skipReason(reasons, locale);
    if (reason) skipped.push(`${locale} (${reason})`);
    else problems.push(`${locale}: no caption file and no reason in skipped_caption_locales`);
  }
  for (const listed of captions) if (!present(files, listed)) problems.push(`${listed} is listed but missing`);
  if (strict) {
    const extra = unchosen([...localesOf(files.keys(), CAPTION_FILE), ...localesOf(captions, CAPTION_FILE)], locales);
    if (extra.length) problems.push(unchosenProblem("caption files", extra));
  }
  if (problems.length) return item("captions", false, problems.join("; "));
  return item("captions", true, `caption files for ${written.join(", ") || "no locale"}${skipped.length ? `; skipped ${skipped.join(", ")}` : ""}`);
}

/** disclosure: metadata.json answers whether Studio's "altered or synthetic content" is ticked, and why. */
export function disclosureItem({ metadata }) {
  const unreadable = metadataProblem(metadata);
  if (unreadable) return item("disclosure", false, unreadable);
  const synthetic = metadata.contains_synthetic_media;
  const reason = metadata.disclosure_reason;
  if (typeof synthetic !== "boolean") return item("disclosure", false, `${METADATA_FILE} has no contains_synthetic_media answer; run package again`);
  if (typeof reason !== "string" || !reason.trim()) return item("disclosure", false, `${METADATA_FILE} has no disclosure_reason`);
  return item("disclosure", true, `${synthetic ? "tick altered or synthetic content" : "no disclosure needed"}: ${reason}`);
}

/**
 * The whole check, pure: `files` maps upload/ paths to sizes; `metadataSha256` binds the report.
 * `locales` are the caption locales wanted and `descriptionLocales` the description locales
 * (docs/videos/LANGUAGES.md: the narration and zh-TW plus what the owner chose); without a
 * choice every locale needs captions or a reason, and the descriptions are what metadata.json
 * lists. `languages` is the owner's choice as readLanguages returns it: with one, a part of a
 * locale it does not have fails (files, descriptions and captions alike), so the package holds
 * exactly the chosen parts; null leaves extra parts alone, as for a package from before the panel.
 * `unchanged` is false when upload/ changed while readPackageReport read it.
 */
export function checkPackage({ files, metadata, finalSha256, approvedSha256, metadataSha256, locales = LOCALES, descriptionLocales = null, brandingMatches = true, languages = null, unchanged = true }) {
  const strict = Boolean(languages);
  return packageReport(
    [
      filesItem({ files, metadata, finalSha256, approvedSha256, brandingMatches, languages, unchanged }),
      descriptionsItem({ files, metadata, locales: descriptionLocales, strict }),
      captionsItem({ files, metadata, locales, strict }),
      disclosureItem({ metadata }),
    ],
    metadataSha256,
  );
}

/**
 * The caption and description locales the owner's choice in the work directory asks for, around
 * the narration locale metadata.json names as its default_language (zh-TW without one); the
 * defaults without a choice.
 */
export function packageLocalesWanted(workdir, metadata = readJson(path.join(workdir, UPLOAD_DIR, METADATA_FILE), null)) {
  const languages = readLanguages(workdir);
  const narration = LOCALES.includes(metadata?.default_language) ? metadata.default_language : NARRATION_LOCALE;
  return { languages, locales: captionLocalesOf(languages, narration), descriptionLocales: metadataLocalesOf(languages, narration) };
}

/**
 * The package's files as a review attaches them: { path, role, content_type }. UPLOAD.md is the
 * owner's reading, not a file to keep; anything else unknown is left out.
 */
export function packageFiles(paths) {
  const entries = [];
  for (const file of [...paths].sort()) {
    if (ROLE_TYPES[path.posix.basename(file, path.posix.extname(file))] && !file.includes("/")) {
      const role = path.posix.basename(file, path.posix.extname(file));
      entries.push({ path: file, role, content_type: ROLE_TYPES[role] });
      continue;
    }
    const caption = CAPTION_FILE.exec(file);
    if (caption) entries.push({ path: file, role: `captions_${caption[1]}`, content_type: "text/plain" });
    const description = DESCRIPTION_FILE.exec(file);
    if (description) entries.push({ path: file, role: `description_${description[1]}`, content_type: "text/plain" });
    const thumbnail = LOCALE_THUMBNAIL_FILE.exec(file);
    if (thumbnail) entries.push({ path: file, role: `thumbnail_${thumbnail[1]}`, content_type: "image/jpeg" });
    if (VARIANT_THUMBNAIL_FILE.test(file)) entries.push({ path: file, role: variantRole(file), content_type: "image/jpeg" });
  }
  return entries;
}

/** Every file under a directory, as posix paths relative to it, with its statSync. */
function statFiles(dir) {
  const files = new Map();
  if (!existsSync(dir)) return files;
  const walk = (current, prefix) => {
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) walk(path.join(current, entry.name), relative);
      else files.set(relative, statSync(path.join(current, entry.name)));
    }
  };
  walk(dir, "");
  return files;
}

/** Every file under a directory, as posix paths relative to it, with sizes. */
export function listFiles(dir) {
  return new Map([...statFiles(dir)].map(([file, stat]) => [file, stat.size]));
}

/** Whether two statFiles listings hold the same files, each with the same size and modification time. */
const sameFiles = (before, after) => before.size === after.size && [...before].every(([file, stat]) => after.get(file)?.size === stat.size && after.get(file)?.mtimeMs === stat.mtimeMs);

/** A file's bytes, or null without the file. */
function readBytes(file) {
  try {
    return readFileSync(file);
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

const sha256 = (bytes) => (bytes ? createHash("sha256").update(bytes).digest("hex") : null);

/**
 * Read <workdir>/upload/ and check it; the approved final is the final gate's last approval, and
 * the locales are the owner's choice in the work directory unless given. Returns { report, files,
 * metadata, finalSha256 }; without metadata.json every item fails and the report has no hash,
 * since there is nothing a review could bind to.
 *
 * metadata.json is read once and the report binds the hash of those very bytes, never of a
 * second read that could be a newer file than the one checked. When anything under upload/ (or
 * the language choice) changed by the time the check is done, the files item fails, so a report
 * never vouches for bytes it did not see; the next run checks what is there then.
 */
export async function readPackageReport(workdir, given = {}) {
  const dir = path.join(workdir, UPLOAD_DIR);
  const before = statFiles(dir);
  const files = new Map([...before].map(([file, stat]) => [file, stat.size]));
  const metadataFile = path.join(dir, METADATA_FILE);
  const bytes = readBytes(metadataFile);
  const metadata = bytes ? JSON.parse(bytes.toString("utf8").replace(/^\uFEFF/, "")) : null;
  const read = sha256(bytes);
  const metadataSha256 = metadata ? read : null;
  const wanted = packageLocalesWanted(workdir, metadata);
  const locales = given.locales ?? wanted.locales;
  const descriptionLocales = given.descriptionLocales === undefined ? wanted.descriptionLocales : given.descriptionLocales;
  const finalFile = path.join(dir, FINAL_FILE);
  const finalSha256 = existsSync(finalFile) ? await sha256File(finalFile) : null;
  const approvedSha256 = readApprovals(workdir).approvals.filter((entry) => entry.gate === "final").at(-1)?.sha256 ?? null;
  const checks = readJson(path.join(workdir, "checks.json"), null);
  const brandingMatches = brandingCurrent(checks, readBranding(workdir)) && (metadata?.branding_hash ?? null) === (appliedBranding(checks)?.hash ?? null);
  const languagesNow = readLanguages(workdir);
  const unchanged = sameFiles(before, statFiles(dir)) && sha256(readBytes(metadataFile)) === read
    && Boolean(languagesNow) === Boolean(wanted.languages) && (!languagesNow || sameChoice(languagesNow.locales, wanted.languages.locales));
  const report = checkPackage({ files, metadata, finalSha256, approvedSha256, metadataSha256, locales, descriptionLocales, brandingMatches, languages: wanted.languages, unchanged });
  return { report, files, metadata, finalSha256 };
}
