import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import { AuthForm } from "./auth-form";

const apiMock = vi.fn();
const pushMock = vi.fn();
const refreshMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});
vi.mock("@/i18n/navigation", () => ({
  useRouter: () => ({ push: pushMock, refresh: refreshMock }),
  Link: ({ href, children }: { href: string; children: React.ReactNode }) => <a href={href}>{children}</a>,
}));

/**
 * The social buttons probe `/auth/oauth/providers` on mount, before any click, so a
 * one-shot mock value meant for the sign-in call would be consumed by that probe instead.
 * Route the probe to an empty provider list and everything else to `login`.
 */
function mockApi(login: () => Promise<unknown>) {
  apiMock.mockImplementation((path: string) => (path === "/auth/oauth/providers" ? Promise.resolve({ providers: {} }) : login()));
}

/** Signs in with `nextPath` and returns the arguments of the one `router.push` the form makes. */
async function signIn(nextPath: string, response: Record<string, unknown> = {}) {
  mockApi(() => Promise.resolve(response));
  render(<AuthForm mode="login" nextPath={nextPath} />);
  fireEvent.change(screen.getByLabelText("Email"), { target: { value: "traveler@example.com" } });
  fireEvent.change(screen.getByLabelText(/^密碼/), { target: { value: "correct-password" } });
  fireEvent.click(screen.getByRole("button", { name: "登入" }));
  await waitFor(() => expect(pushMock).toHaveBeenCalledTimes(1));
  return pushMock.mock.calls[0];
}

describe("AuthForm", () => {
  beforeEach(() => { apiMock.mockReset(); pushMock.mockReset(); refreshMock.mockReset(); });

  it("keeps email, clears password and shows Chinese authentication errors", async () => {
    apiMock.mockRejectedValue(new ApiError("Email 或密碼不正確", 401, "invalid_credentials"));
    render(<AuthForm mode="login" nextPath="/search?destination=NRT" />);
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "traveler@example.com" } });
    fireEvent.change(screen.getByLabelText(/^密碼/), { target: { value: "wrong-password" } });
    fireEvent.click(screen.getByRole("button", { name: "登入" }));
    await screen.findByRole("alert");
    expect((screen.getByLabelText("Email") as HTMLInputElement).value).toBe("traveler@example.com");
    expect((screen.getByLabelText(/^密碼/) as HTMLInputElement).value).toBe("");
    expect(screen.getByText("Email 或密碼不正確")).toBeTruthy();
  });

  it("does not hold an existing member to the new-password rule", () => {
    apiMock.mockResolvedValue({ providers: {} });
    render(<AuthForm mode="login" nextPath="/" />);

    // A member whose password predates the ten-character rule got no message at all:
    // the browser refused to submit the form and the button looked like it did nothing.
    const password = screen.getByLabelText(/^密碼/) as HTMLInputElement;
    expect(password.hasAttribute("minlength")).toBe(false);
    expect(screen.queryByText("至少 10 個字元")).toBeNull();
  });

  it("states the length rule where it applies, on the register form", () => {
    apiMock.mockResolvedValue({ providers: {} });
    render(<AuthForm mode="register" nextPath="/" />);

    const password = screen.getByLabelText(/^密碼/) as HTMLInputElement;
    expect(password.getAttribute("minlength")).toBe("10");
    expect(screen.getByText("至少 10 個字元")).toBeTruthy();
  });

  it("keeps all fields on service failures and returns to a safe local path", async () => {
    mockApi(() => Promise.reject(new ApiError("服務暫時無法使用", 503)));
    const { rerender } = render(<AuthForm mode="login" nextPath="//evil.example" />);
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "traveler@example.com" } });
    fireEvent.change(screen.getByLabelText(/^密碼/), { target: { value: "correct-password" } });
    fireEvent.click(screen.getByRole("button", { name: "登入" }));
    await screen.findByRole("alert");
    expect(screen.getByText("服務暫時無法使用")).toBeTruthy();
    expect((screen.getByLabelText(/^密碼/) as HTMLInputElement).value).toBe("correct-password");
    mockApi(() => Promise.resolve({}));
    rerender(<AuthForm mode="login" nextPath="//evil.example" />);
    fireEvent.click(screen.getByRole("button", { name: "登入" }));
    await waitFor(() => expect(pushMock).toHaveBeenCalledWith("/", { locale: "zh-TW" }));
  });

  // The localized router prefixes every push with the locale it is given, so what the form
  // hands it must not carry a prefix already: `next=/zh-TW/trips/...` used to come back as
  // `/zh-TW/zh-TW/trips/...`. These pin the exact arguments that reach `router.push`.
  it.each([
    ["/trips/seoul-transport-fixture?tab=1", "/trips/seoul-transport-fixture?tab=1", "zh-TW"],
    ["/zh-TW/trips/seoul-transport-fixture", "/trips/seoul-transport-fixture", "zh-TW"],
    ["/ja/trips/seoul-transport-fixture", "/trips/seoul-transport-fixture", "ja"],
    ["/zh-CN/trips/seoul-transport-fixture", "/trips/seoul-transport-fixture", "zh-CN"],
    ["/zh-tw/trips/seoul-transport-fixture", "/trips/seoul-transport-fixture", "zh-TW"],
    ["/en", "/", "en"],
    ["/ko?tab=alerts", "/?tab=alerts", "ko"],
    ["/japan/trips", "/japan/trips", "zh-TW"],
  ])("hands %s to the router as %s in %s, so the prefix is added exactly once", async (nextPath, pathname, locale) => {
    expect(await signIn(nextPath)).toEqual([pathname, { locale }]);
  });

  it("keeps the locale named in next over the account's preferred locale", async () => {
    // `/ja/trips/...` is a specific, valid route the visitor was on or was linked to, so it
    // is honoured as written rather than translated to the account's language; the account
    // preference decides only when `next` names no locale, as the next test pins.
    expect(await signIn("/ja/trips/seoul-transport-fixture", { user: { preferred_locale: "en" } }))
      .toEqual(["/trips/seoul-transport-fixture", { locale: "ja" }]);
  });

  it("sends a bare path to the account's preferred locale", async () => {
    expect(await signIn("/trips/seoul-transport-fixture", { user: { preferred_locale: "en" } }))
      .toEqual(["/trips/seoul-transport-fixture", { locale: "en" }]);
  });

  it.each([
    "//evil.example/path",
    "https://evil.example/path",
    "/\\evil.example/path",
    "%2F%2Fevil.example",
    "%2e%2e/admin",
    "javascript:alert(1)",
    "evil.example",
    "/zh-TW//evil.example",
    "/ja/\\evil.example",
  ])("still rejects %s and returns home", async (nextPath) => {
    expect(await signIn(nextPath)).toEqual(["/", { locale: "zh-TW" }]);
  });

  it("never decodes an encoded remainder, so it stays a path on this origin", async () => {
    expect(await signIn("/zh-TW/%2F%2Fevil.example")).toEqual(["/%2F%2Fevil.example", { locale: "zh-TW" }]);
  });
});
