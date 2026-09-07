import type { Page } from "@playwright/test";

/**
 * Stubbing `/auth/me` is no longer enough to look signed in.
 *
 * The locale layout reads the session cookie on the server and tells both session
 * providers not to ask when there is none, so a browser with no cookie renders the
 * signed-out header no matter what the API would have answered. A test that means to
 * be signed in has to carry the cookie a signed-in browser carries.
 */
export async function pretendSignedIn(page: Page) {
  await page.context().addCookies([
    { name: "travel_access", value: "e2e-session", domain: "127.0.0.1", path: "/" },
  ]);
}
