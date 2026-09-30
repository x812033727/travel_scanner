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
import { existsSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

import { readApprovals, sha256File } from "../core/approvals.mjs";
import { appliedBranding, brandingCurrent, readBranding } from "../core/branding.mjs";
import { readJson } from "../core/paths.mjs";
import { LOCALES, NARRATION_LOCALE } from "../core/schema.mjs";
import { captionLocalesOf, chosenLocales, readLanguages } from "../core/stages.mjs";

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

/**
 * files: final.mp4 is there and is the approved final (its hash equals the final gate's and the
 * one metadata.json records), thumbnail.jpg is there when the video has one, metadata.json is
 * there. `files` maps each path under upload/ (posix, relative) to its size.
 */
export function filesItem({ files, metadata, finalSha256, approvedSha256, brandingMatches = true }) {
  const problems = [];
  if (!metadata) problems.push(`${METADATA_FILE} is missing`);
  if (!present(files, FINAL_FILE)) problems.push(`${FINAL_FILE} is missing`);
  else if (!approvedSha256) problems.push("no approved final to compare final.mp4 with");
  else if (finalSha256 !== approvedSha256) problems.push(`${FINAL_FILE} is not the approved final (${String(finalSha256).slice(0, 12)} vs ${approvedSha256.slice(0, 12)})`);
  else if (metadata && metadata.final_sha256 !== finalSha256) problems.push(`${METADATA_FILE} records another final (${String(metadata.final_sha256).slice(0, 12)})`);
  if (metadata?.thumbnail && !present(files, THUMBNAIL_FILE)) problems.push(`${THUMBNAIL_FILE} is missing`);
  if (!brandingMatches) problems.push("the upload package does not match the selected and applied branding; rebuild the final and run package again");
  if (problems.length) return item("files", false, problems.join("; "));
  const named = [FINAL_FILE, ...(metadata.thumbnail ? [THUMBNAIL_FILE] : []), METADATA_FILE];
  return item("files", true, `${named.join(", ")}; ${FINAL_FILE} is the approved final (${finalSha256.slice(0, 12)})`);
}

/** The locales a package describes: the default language and every localization. */
export function packageLocales(metadata) {
  return [metadata?.default_language ?? "zh-TW", ...Object.keys(metadata?.localizations ?? {})];
}

/**
 * descriptions: a non-empty description.<locale>.txt for the default language and every
 * localization, or, with `locales` (zh-TW and the locales the owner chose titles and descriptions
 * for), for exactly those: a chosen locale without its file fails, whatever metadata.json lists.
 */
export function descriptionsItem({ files, metadata, locales = null }) {
  if (!metadata) return item("descriptions", false, `${METADATA_FILE} is missing`);
  const wanted = locales ?? packageLocales(metadata);
  const missing = wanted.filter((locale) => !(sizeOf(files, `description.${locale}.txt`) > 0));
  if (missing.length) return item("descriptions", false, `no description for ${missing.join(", ")}`);
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
 * skipped_caption_locales with a reason; and every file metadata.json lists is there.
 */
export function captionsItem({ files, metadata, locales = LOCALES }) {
  if (!metadata) return item("captions", false, `${METADATA_FILE} is missing`);
  const problems = [];
  const written = [];
  const skipped = [];
  for (const locale of locales) {
    if (sizeOf(files, `captions/${locale}.srt`) > 0) {
      written.push(locale);
      continue;
    }
    const reason = skipReason(metadata.skipped_caption_locales, locale);
    if (reason) skipped.push(`${locale} (${reason})`);
    else problems.push(`${locale}: no caption file and no reason in skipped_caption_locales`);
  }
  for (const listed of metadata.captions ?? []) if (!present(files, listed)) problems.push(`${listed} is listed but missing`);
  if (problems.length) return item("captions", false, problems.join("; "));
  return item("captions", true, `caption files for ${written.join(", ") || "no locale"}${skipped.length ? `; skipped ${skipped.join(", ")}` : ""}`);
}

/** disclosure: metadata.json answers whether Studio's "altered or synthetic content" is ticked, and why. */
export function disclosureItem({ metadata }) {
  if (!metadata) return item("disclosure", false, `${METADATA_FILE} is missing`);
  const synthetic = metadata.contains_synthetic_media;
  const reason = metadata.disclosure_reason;
  if (typeof synthetic !== "boolean") return item("disclosure", false, `${METADATA_FILE} has no contains_synthetic_media answer; run package again`);
  if (typeof reason !== "string" || !reason.trim()) return item("disclosure", false, `${METADATA_FILE} has no disclosure_reason`);
  return item("disclosure", true, `${synthetic ? "tick altered or synthetic content" : "no disclosure needed"}: ${reason}`);
}

/**
 * The whole check, pure: `files` maps upload/ paths to sizes; `metadataSha256` binds the report.
 * `locales` are the caption locales wanted and `descriptionLocales` the description locales
 * (docs/videos/LANGUAGES.md: zh-TW plus what the owner chose); without a choice every locale
 * needs captions or a reason, and the descriptions are what metadata.json lists.
 */
export function checkPackage({ files, metadata, finalSha256, approvedSha256, metadataSha256, locales = LOCALES, descriptionLocales = null, brandingMatches = true }) {
  return packageReport(
    [filesItem({ files, metadata, finalSha256, approvedSha256, brandingMatches }), descriptionsItem({ files, metadata, locales: descriptionLocales }), captionsItem({ files, metadata, locales }), disclosureItem({ metadata })],
    metadataSha256,
  );
}

/** The caption and description locales the owner's choice in the work directory asks for; the defaults without one. */
export function packageLocalesWanted(workdir) {
  const languages = readLanguages(workdir);
  const metadata = chosenLocales(languages, "metadata");
  return { languages, locales: captionLocalesOf(languages), descriptionLocales: metadata ? [NARRATION_LOCALE, ...metadata] : null };
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
  }
  return entries;
}

/** Every file under a directory, as posix paths relative to it, with sizes. */
export function listFiles(dir) {
  const files = new Map();
  if (!existsSync(dir)) return files;
  const walk = (current, prefix) => {
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) walk(path.join(current, entry.name), relative);
      else files.set(relative, statSync(path.join(current, entry.name)).size);
    }
  };
  walk(dir, "");
  return files;
}

/**
 * Read <workdir>/upload/ and check it; the approved final is the final gate's last approval, and
 * the locales are the owner's choice in the work directory unless given. Returns { report, files,
 * metadata, finalSha256 }; without metadata.json every item fails and the report has no hash,
 * since there is nothing a review could bind to.
 */
export async function readPackageReport(workdir, given = {}) {
  const wanted = packageLocalesWanted(workdir);
  const locales = given.locales ?? wanted.locales;
  const descriptionLocales = given.descriptionLocales === undefined ? wanted.descriptionLocales : given.descriptionLocales;
  const dir = path.join(workdir, UPLOAD_DIR);
  const files = listFiles(dir);
  const metadataFile = path.join(dir, METADATA_FILE);
  const metadata = readJson(metadataFile, null);
  const finalFile = path.join(dir, FINAL_FILE);
  const finalSha256 = existsSync(finalFile) ? await sha256File(finalFile) : null;
  const approvedSha256 = readApprovals(workdir).approvals.filter((entry) => entry.gate === "final").at(-1)?.sha256 ?? null;
  const metadataSha256 = metadata ? await sha256File(metadataFile) : null;
  const checks = readJson(path.join(workdir, "checks.json"), null);
  const brandingMatches = brandingCurrent(checks, readBranding(workdir)) && (metadata?.branding_hash ?? null) === (appliedBranding(checks)?.hash ?? null);
  return { report: checkPackage({ files, metadata, finalSha256, approvedSha256, metadataSha256, locales, descriptionLocales, brandingMatches }), files, metadata, finalSha256 };
}
