import { useEffect } from "react";
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderSessionProvider, useHeaderSession } from "./header-session";

vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams() }));

const user = { id: "admin-a", email: "admin@example.com", preferred_currency: "TWD", is_admin: true };
type Session = ReturnType<typeof useHeaderSession>;
function SessionProbe({ report }: { report: (value: Session) => void }) {
  const session = useHeaderSession();
  useEffect(() => report(session), [session, report]);
  return <>
    <p>{session.status}</p>
    <button onClick={() => session.user && session.setUser({ ...session.user, preferred_currency: "USD" })}>Currency</button>
    <button onClick={() => session.user && session.setUser({ ...session.user, email: "profile@example.com" })}>Profile</button>
    <button onClick={session.clearSession}>Clear</button>
    <button onClick={() => void session.logout()}>Logout</button>
    <button onClick={() => session.setUser({ ...user })}>Login same account</button>
    <button onClick={() => session.setUser({ ...user, id: "admin-b" })}>Switch account</button>
  </>;
}

function setup() {
  const report = vi.fn<(value: Session) => void>();
  const rendered = render(<HeaderSessionProvider><SessionProbe report={report} /></HeaderSessionProvider>);
  return { ...rendered, current: () => report.mock.calls.at(-1)![0] };
}

async function authenticatedSession(view: ReturnType<typeof setup>) {
  await screen.findByText("authenticated");
  // DOM text can commit before SessionProbe's passive effect reports that render.
  // Wait for the probe itself before capturing or comparing login identities.
  await waitFor(() => {
    expect(view.current().status).toBe("authenticated");
    expect(view.current().sessionIdentity).toBeTruthy();
  });
  return view.current();
}

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("HeaderSession login identity", () => {
  it("stays stable across currency and profile updates without additional authentication reads", async () => {
    const fetchMock = vi.fn(async () => new Response(JSON.stringify(user)));
    vi.stubGlobal("fetch", fetchMock);
    const view = setup();
    const initial = await authenticatedSession(view);
    fireEvent.click(screen.getByRole("button", { name: "Currency" }));
    await waitFor(() => {
      expect(view.current().user?.preferred_currency).toBe("USD");
      expect(view.current().user).not.toBe(initial.user);
      expect(view.current().sessionIdentity).toBe(initial.sessionIdentity);
    });
    fireEvent.click(screen.getByRole("button", { name: "Profile" }));
    await waitFor(() => {
      expect(view.current().user?.email).toBe("profile@example.com");
      expect(view.current().sessionIdentity).toBe(initial.sessionIdentity);
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it.each(["Clear", "Logout"])("rotates identity after %s and a new login to the same account", async (action) => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(user))));
    const view = setup();
    const original = (await authenticatedSession(view)).sessionIdentity;
    fireEvent.click(screen.getByRole("button", { name: action }));
    await screen.findByText("signed_out");
    await waitFor(() => {
      expect(view.current().status).toBe("signed_out");
      expect(view.current().sessionIdentity).toBeNull();
      expect(view.current().user).toBeNull();
    });
    fireEvent.click(screen.getByRole("button", { name: "Login same account" }));
    await screen.findByText("authenticated");
    await waitFor(() => {
      expect(view.current().status).toBe("authenticated");
      expect(view.current().user?.id).toBe(user.id);
      expect(view.current().sessionIdentity).toBeTruthy();
      expect(view.current().sessionIdentity).not.toBe(original);
    });
  });

  it("rotates identity when the authenticated principal changes", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(user))));
    const view = setup();
    const original = (await authenticatedSession(view)).sessionIdentity;
    fireEvent.click(screen.getByRole("button", { name: "Switch account" }));
    await waitFor(() => {
      expect(view.current().user?.id).toBe("admin-b");
      expect(view.current().sessionIdentity).toBeTruthy();
      expect(view.current().sessionIdentity).not.toBe(original);
    });
  });

  it("does not revive the old identity from an auth response arriving after logout", async () => {
    let finish!: (response: Response) => void;
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>((resolve) => { finish = resolve; })));
    const view = setup();
    fireEvent.click(screen.getByRole("button", { name: "Clear" }));
    await act(async () => { finish(new Response(JSON.stringify(user))); });
    await waitFor(() => {
      expect(view.current().status).toBe("signed_out");
      expect(view.current().sessionIdentity).toBeNull();
      expect(view.current().user).toBeNull();
    });
  });
});
