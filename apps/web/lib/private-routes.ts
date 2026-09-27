import { TRAVELPAYOUTS_DRIVE_SCRIPT_URL } from "@/lib/travelpayouts-drive";

/**
 * Sections where no third-party script may share the document.
 *
 * Their pages show a reader's own data (trips, saved items, alerts, the admin console), take a
 * password, or carry a secret in the URL itself: a shared trip's token, the one-time LINE link.
 * A script from another origin running in that document can read all of it. The AdSense root
 * already keeps its tag to published articles (`lib/adsense.ts`); this is the same rule for the
 * two scripts the ordinary layout loads, Travelpayouts Drive and GA4's `gtag.js`.
 */
const PRIVATE_SECTIONS = [
  "account",
  "admin",
  "alerts",
  "forgot-password",
  "line",
  "login",
  "my",
  "register",
  "share",
  "share-target",
  "trips",
];

const privateRoute = new RegExp(`^/(?:(?:en|ja|ko|zh-TW|zh-CN)/)?(?:${PRIVATE_SECTIONS.join("|")})(?:/|$)`);

export function isPrivateRoute(pathname: string): boolean {
  return privateRoute.test(pathname);
}

const THIRD_PARTY_SCRIPT_ORIGINS = [
  new URL(TRAVELPAYOUTS_DRIVE_SCRIPT_URL).origin,
  "https://www.googletagmanager.com",
];

/**
 * Whether this document has already loaded one of those scripts.
 *
 * Unmounting the React `<Script>` does not unload what it ran (the reason Stay22 got its own
 * root, `docs/stay22-module-switch.md`), so once this is true the only clean way into a private
 * page is a new document.
 */
export function hasThirdPartyScript(): boolean {
  return Array.from(document.scripts).some((script) =>
    THIRD_PARTY_SCRIPT_ORIGINS.some((origin) => script.src.startsWith(`${origin}/`)),
  );
}

/** Leaving the current document. An object so tests can observe it: jsdom's Location cannot be stubbed. */
export const documentNavigation = {
  assign(url: string) {
    location.assign(url);
  },
  reload() {
    location.reload();
  },
};
