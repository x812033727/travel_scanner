// Stock photos for the slides (docs/videos/ILLUSTRATED.md §圖庫照片): `stock search` lists Pexels
// and Pixabay candidates with the credit each vendor asks for, and `stock fetch` has the server
// download one into the media store, copies it to <workdir>/stock/<sha256>.<ext> and writes its
// credit into video.json's assets[], where package's description reads it (core/metadata.mjs
// pictureCredits). The vendors' keys stay on the site; the tool sends its video tool token.
//
// Free at both vendors: nothing is booked in the ledger and no budget is reserved; the server's
// per-hour limit is the only brake. The picture is named by its bytes, so fetching the same photo
// twice writes one file and one entry, and a slide that shows it (`screenshot`, image
// "stock/<sha256>.<ext>") is redrawn when those bytes change (render/plan.mjs).
import { existsSync, statSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { sha256File } from "../core/approvals.mjs";
import { atomicWrite, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { loadProject } from "../core/state.mjs";
import { isStockPath } from "../templates/templates.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { MediaError, downloadFile, stockFetch, stockSearch } from "./client.mjs";

export const STOCK_DIR = "stock";
export const PROVIDERS = ["pexels", "pixabay"];
export const ORIENTATIONS = ["landscape", "portrait", "square"];
// Mirror MAX_STOCK_PER_PAGE, MAX_STOCK_QUERY_CHARS and STOCK_ID_PATTERN in apps/api/app/video_media/schemas.py.
export const MAX_PER_PAGE = 40;
export const MAX_QUERY_CHARS = 100;
const PHOTO_ID = /^[0-9]{1,20}$/;
const DEFAULT_PER_PAGE = 15;
// What each vendor's API terms ask to be shown wherever its results are used (ILLUSTRATED.md §授權與標示).
export const VENDOR_NOTICES = {
  pexels: "Photos provided by Pexels (https://www.pexels.com)",
  pixabay: "Images from Pixabay (https://pixabay.com)",
};
// The server stores a stock photo only as one of these (stock.py IMAGE_TYPES).
const EXTENSIONS = { "image/png": "png", "image/jpeg": "jpg", "image/webp": "webp" };

/** Where the tool keeps its copy of a fetched photo, relative to the work directory. */
export function stockFile(sha256, contentType) {
  const extension = EXTENSIONS[String(contentType).split(";")[0].trim().toLowerCase()];
  if (!extension) throw new MediaError(`the server stored a ${contentType || "file of unknown type"}, not a png, jpeg or webp`, { code: "video_media_unsupported_type", who: "tool" });
  const file = `${STOCK_DIR}/${sha256}.${extension}`;
  if (!isStockPath(file)) throw new MediaError(`${sha256} is not a SHA-256 the screenshot template accepts`, { code: "video_media_hash_mismatch", who: "tool" });
  return file;
}

/** The assets[] entry of a fetched photo (core/metadata.mjs ASSET_FIELDS), from the credit the server returned. */
export function assetEntry(credit, file) {
  return { path: file, source: credit.text, license: credit.license, author: credit.author, url: credit.url };
}

/** `assets` with `asset` added, or replaced where an entry already has its path; the rest untouched. */
export function withAsset(assets, asset) {
  const list = Array.isArray(assets) ? assets : [];
  const at = list.findIndex((entry) => entry?.path === asset.path);
  if (at < 0) return [...list, asset];
  return list.map((entry, index) => (index === at ? asset : entry));
}

/** The document with its assets[] replaced; a document without one gets it before `scenes`, where a reader looks. */
export function withAssets(doc, assets) {
  if (Object.hasOwn(doc, "assets")) return { ...doc, assets };
  const out = {};
  for (const [key, value] of Object.entries(doc)) {
    if (key === "scenes") out.assets = assets;
    out[key] = value;
  }
  if (!Object.hasOwn(out, "assets")) out.assets = assets;
  return out;
}

const shape = (width, height) => (width > height * 1.05 ? "landscape" : height > width * 1.05 ? "portrait" : "square");

/** The candidates as `stock search` prints them, with the notices the vendors ask for. */
export function candidateText(answer, slug = "<slug>") {
  const lines = [];
  for (const candidate of answer.candidates ?? []) {
    lines.push(`${candidate.provider} ${candidate.id}  ${candidate.width}×${candidate.height} ${shape(candidate.width, candidate.height)}  ${candidate.credit.text}  ${candidate.credit.url}`);
    if (candidate.alt) lines.push(`  ${candidate.alt}`);
  }
  const totals = Object.entries(answer.total ?? {});
  if (!lines.length) lines.push(`no photos for "${answer.query}"${totals.length ? "" : " (no vendor answered)"}`);
  if (totals.length) lines.push(`matches: ${totals.map(([provider, count]) => `${provider} ${count.toLocaleString("en-US")}`).join(", ")}`);
  for (const problem of answer.problems ?? []) lines.push(`note: ${problem}`);
  const notices = PROVIDERS.filter((provider) => Object.hasOwn(answer.total ?? {}, provider)).map((provider) => VENDOR_NOTICES[provider]);
  if (notices.length) lines.push(notices.join(" · "));
  if (Object.hasOwn(answer.total ?? {}, "pixabay")) lines.push("Pixabay's preview links expire after a day; fetch what you choose soon.");
  if (answer.candidates?.length) lines.push(`next: node tools/video/cli.mjs stock fetch --slug ${slug} --provider ${answer.candidates[0].provider} --id ${answer.candidates[0].id}`);
  return `${lines.join("\n")}\n`;
}

/** The size as a person reads it. */
const megabytes = (bytes) => `${(bytes / (1024 * 1024)).toFixed(1)} MB`;

/**
 * A stock call on a site whose web app does not forward the stock routes answers 404
 * `video_media_route_unknown`, which would read as the tool's mistake; it is the owner's deploy.
 */
async function stockCall(call) {
  try {
    return await call();
  } catch (error) {
    if (error instanceof MediaError && error.code === "video_media_route_unknown") {
      throw new MediaError("the site does not serve the stock photo routes yet (POST /api/video/media/stock/search): deploy a build whose web app forwards them (docs/videos/ILLUSTRATED.md §圖庫照片)", { status: error.status, code: error.code, who: "owner" });
    }
    throw error;
  }
}

const positive = (value, name, max) => {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 1 || number > max) throw new UsageError(`${name} must be 1 to ${max}`);
  return number;
};

async function cmdSearch(args, ctx) {
  const values = parseArgs({
    args,
    options: { query: { type: "string" }, provider: { type: "string" }, orientation: { type: "string" }, "per-page": { type: "string" }, page: { type: "string" }, slug: { type: "string" }, json: { type: "boolean" } },
    strict: true,
  }).values;
  const query = (values.query ?? "").split(/\s+/).filter(Boolean).join(" ");
  if (!query) throw new UsageError('stock search needs --query "<a few English words>"');
  if ([...query].length > MAX_QUERY_CHARS) throw new UsageError(`--query is at most ${MAX_QUERY_CHARS} characters`);
  if (values.provider !== undefined && !PROVIDERS.includes(values.provider)) throw new UsageError(`--provider must be ${PROVIDERS.join(" or ")}`);
  if (values.orientation !== undefined && !ORIENTATIONS.includes(values.orientation)) throw new UsageError(`--orientation must be one of ${ORIENTATIONS.join(", ")}`);
  const request = { query, per_page: values["per-page"] === undefined ? DEFAULT_PER_PAGE : positive(values["per-page"], "--per-page", MAX_PER_PAGE), page: values.page === undefined ? 1 : positive(values.page, "--page", 50) };
  if (values.provider) request.provider = values.provider;
  if (values.orientation) request.orientation = values.orientation;
  const credentials = requireCredentials(ctx);
  const answer = await stockCall(() => stockSearch({ request, ...clientOptions(ctx, credentials) }));
  if (values.json) ctx.stdout.write(`${JSON.stringify(answer, null, 2)}\n`);
  else ctx.stdout.write(candidateText(answer, values.slug));
  return ctx.EXIT.ok;
}

/**
 * `stock fetch`: the server fetches the photo into the media store; the tool downloads it to
 * <workdir>/stock/<sha256>.<ext> (verified by hash as it arrives, skipped when the file is already
 * there with the right hash) and writes the credit into video.json's assets[]. Returns
 * { file, asset, fetched, downloaded }.
 */
export async function fetchStock({ project, workdir, provider, id, options }) {
  const { doc } = project;
  const fetched = await stockCall(() => stockFetch({ request: { slug: doc.slug, provider, id }, ...options }));
  const file = stockFile(fetched.sha256, fetched.content_type);
  const target = path.join(workdir, file);
  let downloaded = false;
  if (!existsSync(target) || (await sha256File(target)) !== fetched.sha256) {
    await downloadFile({ slug: doc.slug, sha256: fetched.sha256, file: target, ...options });
    downloaded = true;
  }
  const asset = assetEntry(fetched.credit, file);
  const updated = withAssets(doc, withAsset(doc.assets, asset));
  atomicWrite(project.file, `${JSON.stringify(updated, null, 2)}\n`);
  return { file, asset, fetched, downloaded, assets: updated.assets.length };
}

async function cmdFetch(args, ctx) {
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, provider: { type: "string" }, id: { type: "string" }, workdir: { type: "string" }, json: { type: "boolean" } },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("stock fetch needs --slug (or --file for an example outside docs/videos)");
  if (!PROVIDERS.includes(values.provider)) throw new UsageError(`stock fetch needs --provider ${PROVIDERS.join("|")}, as stock search printed it`);
  if (!PHOTO_ID.test(values.id ?? "")) throw new UsageError("stock fetch needs --id, the photo's number as stock search printed it");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: project.doc.slug, root: ctx.root, home: ctx.home });
  const credentials = requireCredentials(ctx);
  const result = await fetchStock({ project, workdir, provider: values.provider, id: values.id, options: clientOptions(ctx, credentials) });
  if (values.json) {
    ctx.stdout.write(`${JSON.stringify({ file: result.file, asset: result.asset, width: result.fetched.width, height: result.fetched.height, size: result.fetched.size, downloaded: result.downloaded }, null, 2)}\n`);
    return ctx.EXIT.ok;
  }
  const { fetched, asset } = result;
  const size = existsSync(path.join(workdir, result.file)) ? statSync(path.join(workdir, result.file)).size : fetched.size;
  ctx.stdout.write(`${result.file}  ${fetched.width}×${fetched.height} ${shape(fetched.width, fetched.height)}, ${megabytes(size)}${result.downloaded ? "" : " (already in the work directory)"}\n`);
  ctx.stdout.write(`${asset.source} · ${asset.license} · ${asset.url}\n`);
  ctx.stdout.write(`assets[]: ${path.relative(ctx.root, project.file)} now lists ${result.assets} pictures; package writes the credit into the description\n`);
  ctx.stdout.write(`next: give a screenshot scene "image": "${result.file}" (a "credit" on the slide is optional), then lint and render\n`);
  return ctx.EXIT.ok;
}

export async function run(command, args, ctx) {
  const [sub, ...rest] = args;
  if (sub === "search") return cmdSearch(rest, ctx);
  if (sub === "fetch") return cmdFetch(rest, ctx);
  throw new UsageError('stock takes a subcommand: stock search --query "Seoul skyline" [--provider P] [--orientation O] [--per-page N] [--page N] [--json], or stock fetch --slug S --provider P --id N [--workdir D] [--json]');
}
