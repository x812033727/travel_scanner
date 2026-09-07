export const TRAVELPAYOUTS_DRIVE_SCRIPT_URL = "https://emrldtp.cc/NTcwMDg5.js?t=570089";

const MOKAAIR_PRODUCTION_ORIGINS = new Set([
  "https://mokaair.com",
  "https://www.mokaair.com",
]);

/**
 * The Drive code is tied to the Mokaair project in Travelpayouts. Keeping the
 * origin check server-side prevents previews and local development from
 * reporting test traffic or allowing the script to rewrite test links.
 */
export function isTravelpayoutsDriveOrigin(siteUrl: string): boolean {
  try {
    return MOKAAIR_PRODUCTION_ORIGINS.has(new URL(siteUrl).origin);
  } catch {
    return false;
  }
}
