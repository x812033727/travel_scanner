// Whether the bookends this machine is about to pin are the ones the site's worker builds with
// (docs/videos/BRANDING.md §本機成片要跟正式站同一包). Five 奇聞檔案局 recuts assembled locally on
// 2026-10-13 pinned an older 3-second outro, and three cloud cuts of 2026-10-19 pinned none at all,
// and nothing said so. assemble and compile ask GET /api/video/media/branding before they encode
// and say when the packages differ; they still build, and an unreachable site only says so.
import { explainerSeries } from "../core/drama.mjs";
import { brandingStatus } from "../media/client.mjs";
import { readCredentials } from "../tts/credentials.mjs";

const COMPARE_TIMEOUT_MS = 10_000;
// The worker builds with no bookends for these: none installed, or switched off.
const NO_PACKAGE = new Set(["video_branding_not_installed", "video_branding_disabled"]);

/**
 * The package the site's worker would pin for this video, the way readDefaultBranding chooses
 * here: its series' when the series has a registry (switched off means none), else the channel's.
 * Null when the worker has none.
 */
export async function sitePackage(doc, client) {
  const series = explainerSeries(doc);
  if (series) {
    try {
      return await brandingStatus({ ...client, series });
    } catch (error) {
      if (error.code === "video_branding_disabled") return null;
      if (error.code !== "video_branding_not_installed") throw error;
    }
  }
  try {
    return await brandingStatus(client);
  } catch (error) {
    if (NO_PACKAGE.has(error.code)) return null;
    throw error;
  }
}

const named = (branding) => (branding ? `${branding.id} (${branding.hash.slice(0, 12)})` : "no bookends");

/**
 * One line for the build's output when `local` (this machine's current package for the video,
 * null when none is installed) is not the site worker's, or when they could not be compared;
 * null when they are the same. It never throws and never stops the build.
 */
export async function siteBrandingNotice({ doc, local, ctx, timeoutMs = COMPARE_TIMEOUT_MS }) {
  let remote;
  try {
    // Inside the try: a credentials file that does not parse must not stop a build either.
    const { site, token } = readCredentials({ env: ctx.env, home: ctx.home });
    if (!token) return "branding: not compared with the site's worker (no video tool token; run `node tools/video/cli.mjs login`)";
    const fetchImpl = ctx.fetch ?? globalThis.fetch;
    const client = {
      site, token, attempts: 1, sleep: async () => {},
      fetchImpl: (url, init) => fetchImpl(url, { ...init, signal: AbortSignal.timeout(timeoutMs) }),
    };
    remote = await sitePackage(doc, client);
  } catch (error) {
    return `branding: could not compare with the site's worker (${error.message}); check with \`node tools/video/cli.mjs branding --pull --dry-run\``;
  }
  if ((remote?.hash ?? null) === (local?.hash ?? null)) return null;
  const fix = remote
    ? "to match it, stop and run `node tools/video/cli.mjs branding --pull`, then build again"
    : "it has none installed or has them switched off; check `branding --json` on the host";
  return `WARN branding: this build pins ${named(local)} but the site's worker uses ${named(remote)}; ${fix}`;
}
