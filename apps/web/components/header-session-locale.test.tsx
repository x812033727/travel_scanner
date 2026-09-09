import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useNavigationGuard } from "@/lib/navigation-guard";
import { HeaderSessionProvider, useHeaderSession } from "./header-session";

const mocks = vi.hoisted(() => ({
  router: { replace: vi.fn(), push: vi.fn(), refresh: vi.fn() },
}));
vi.mock("next-intl", () => ({ useLocale: () => "en" }));
vi.mock("@/i18n/navigation", () => ({
  usePathname: () => "/admin/site-pages",
  useRouter: () => mocks.router,
}));
vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams("page=privacy&content=hotel%3Afixture"),
}));

const user = { id: "fixture-admin", email: "admin@example.com", preferred_locale: "zh-TW" };
const route = "/en/admin/site-pages?page=privacy&content=hotel%3Afixture#preview";
let originalUrl: string;

beforeEach(() => {
  vi.clearAllMocks();
  window.sessionStorage.clear();
  originalUrl = window.location.href;
  window.history.replaceState({ __NA: true, tree: "preserved" }, "", route);
  document.cookie = "travel_locale=en; path=/";
  // Consume the real guard's same-URL history entry synchronously, without a jsdom race.
  const states: unknown[] = [window.history.state];
  let position = 0;
  vi.spyOn(window.history, "state", "get").mockImplementation(() => states[position]);
  vi.spyOn(window.history, "pushState").mockImplementation((state) => {
    states.splice(position + 1);
    states.push(state);
    position++;
  });
  vi.spyOn(window.history, "back").mockImplementation(() => {
    if (position > 0) {
      position--;
      window.dispatchEvent(new PopStateEvent("popstate", { state: states[position] }));
    }
  });
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
  window.sessionStorage.clear();
  document.cookie = "travel_locale=; path=/; max-age=0";
  window.history.replaceState(null, "", originalUrl);
});

function SessionProbe({ dirty, requestLeave }: {
  dirty: boolean;
  requestLeave: (proceed: () => void) => boolean;
}) {
  const session = useHeaderSession();
  useNavigationGuard(dirty, requestLeave);
  return <>
    <p>{session.status}</p>
    <p>{session.user?.id}</p>
    <p>{session.sessionIdentity ? "session identity present" : "no session identity"}</p>
    <button onClick={session.clearSession}>Clear session</button>
  </>;
}

function pendingAuthentication(requestLeave: (proceed: () => void) => boolean) {
  let finish!: (response: Response) => void;
  const fetchMock = vi.fn(() => new Promise<Response>((resolve) => { finish = resolve; }));
  vi.stubGlobal("fetch", fetchMock);
  const view = render(<HeaderSessionProvider>
    <SessionProbe dirty={false} requestLeave={requestLeave} />
  </HeaderSessionProvider>);
  expect(screen.getByText("loading")).toBeTruthy();
  // The editor becomes dirty while its shared header's one auth request is still pending.
  view.rerender(<HeaderSessionProvider>
    <SessionProbe dirty requestLeave={requestLeave} />
  </HeaderSessionProvider>);
  return {
    fetchMock,
    complete: () => act(async () => { finish(new Response(JSON.stringify(user))); }),
  };
}

describe("stored header locale respects draft navigation protection", () => {
  it("keeps authentication and makes no cookie or route writes when the active guard denies leaving", async () => {
    const requestLeave = vi.fn(() => false);
    const cookieWrite = vi.spyOn(document, "cookie", "set");
    const authentication = pendingAuthentication(requestLeave);
    await authentication.complete();
    expect(requestLeave).toHaveBeenCalledOnce();
    expect(screen.getByText("authenticated")).toBeTruthy();
    expect(screen.getByText(user.id)).toBeTruthy();
    expect(screen.getByText("session identity present")).toBeTruthy();
    expect(screen.queryByText("unavailable")).toBeNull();
    expect(cookieWrite).not.toHaveBeenCalled();
    expect(document.cookie).toContain("travel_locale=en");
    expect(mocks.router.replace).not.toHaveBeenCalled();
    expect(mocks.router.push).not.toHaveBeenCalled();
    expect(authentication.fetchMock).toHaveBeenCalledOnce();
  });

  it("writes the cookie and preserves the full path, query and fragment only after approval", async () => {
    let approve: (() => void) | undefined;
    const requestLeave = vi.fn((proceed: () => void) => { approve = proceed; return false; });
    const cookieWrite = vi.spyOn(document, "cookie", "set");
    const authentication = pendingAuthentication(requestLeave);
    await waitFor(() => expect(window.history.pushState).toHaveBeenCalledOnce());
    await authentication.complete();
    expect(requestLeave).toHaveBeenCalledOnce();
    expect(cookieWrite).not.toHaveBeenCalled();
    expect(mocks.router.replace).not.toHaveBeenCalled();
    expect(approve).toBeTypeOf("function");
    act(() => approve?.());
    expect(cookieWrite).toHaveBeenCalledExactlyOnceWith(
      "travel_locale=zh-TW; path=/; max-age=31536000; samesite=lax",
    );
    expect(mocks.router.replace).toHaveBeenCalledExactlyOnceWith(
      "/admin/site-pages?page=privacy&content=hotel%3Afixture#preview", { locale: "zh-TW" },
    );
    expect(window.history.back).toHaveBeenCalledOnce();
    expect(screen.getByText("authenticated")).toBeTruthy();
    expect(authentication.fetchMock).toHaveBeenCalledOnce();
  });

  it("does not apply a deferred stored preference after the session is cleared", async () => {
    let approve: (() => void) | undefined;
    const cookieWrite = vi.spyOn(document, "cookie", "set");
    const authentication = pendingAuthentication((proceed) => { approve = proceed; return false; });
    await authentication.complete();
    fireEvent.click(screen.getByRole("button", { name: "Clear session" }));
    expect(screen.getByText("signed_out")).toBeTruthy();
    expect(approve).toBeTypeOf("function");
    act(() => approve?.());
    expect(cookieWrite).not.toHaveBeenCalled();
    expect(mocks.router.replace).not.toHaveBeenCalled();
    expect(screen.getByText("signed_out")).toBeTruthy();
    expect(authentication.fetchMock).toHaveBeenCalledOnce();
  });
});
