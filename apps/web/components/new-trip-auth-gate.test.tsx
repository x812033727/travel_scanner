import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { NewTripAuthGate } from "./new-trip-auth-gate";

vi.mock("./new-trip-form", () => ({ NewTripForm: () => <div>已驗證的新行程表單</div> }));

// Answers each API path with its JSON body; unknown paths get `fallbackStatus`.
function fetchByPath(bodies: Record<string, unknown>, fallbackStatus = 404) {
  return vi.fn((input: RequestInfo | URL) => {
    const path = String(input).replace(/^.*\/api\/travel/, "");
    const body = bodies[path];
    return Promise.resolve(body === undefined
      ? new Response(JSON.stringify({ detail: "unavailable" }), { status: fallbackStatus })
      : new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } }));
  });
}

afterEach(() => vi.unstubAllGlobals());

describe("NewTripAuthGate", () => {
  it("asks signed-out visitors to log in before showing the long form", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "未登入" }), { status: 401 })));
    render(<NewTripAuthGate />);
    const link = await screen.findByRole("link", { name: "前往登入" });
    expect(link.getAttribute("href")).toBe("/login?next=%2Ftrips%2Fnew");
    expect(screen.queryByText("已驗證的新行程表單")).toBeNull();
  });

  it("shows a service error instead of a login prompt for 5xx responses", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "資料庫錯誤" }), { status: 500 })));
    render(<NewTripAuthGate />);
    expect((await screen.findByRole("alert")).textContent).toContain("無法確認登入狀態");
    expect(screen.queryByRole("link", { name: "前往登入" })).toBeNull();
  });

  it("reveals the form only after authentication succeeds", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "u1" }), { status: 200 })));
    render(<NewTripAuthGate />);
    expect(await screen.findByText("已驗證的新行程表單")).toBeTruthy();
  });

  it("explains the saved-trip cap before the form when it is already reached", async () => {
    vi.stubGlobal("fetch", fetchByPath({
      "/auth/me": { id: "u1" },
      "/trips": Array.from({ length: 20 }, (_, index) => ({ id: `trip-${index}` })),
      "/usage": { limits: { saved_trips: 20, price_alerts: 20 } },
    }));
    render(<NewTripAuthGate />);
    expect(await screen.findByRole("heading", { name: "已達儲存旅程上限" })).toBeTruthy();
    expect(screen.getByText(/目前已有 20 個旅程，上限為 20 個/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "前往我的旅程" }).getAttribute("href")).toBe("/trips");
    expect(screen.queryByText("已驗證的新行程表單")).toBeNull();
  });

  it("shows the form when the cap is not reached or cannot be checked", async () => {
    vi.stubGlobal("fetch", fetchByPath({
      "/auth/me": { id: "u1" },
      "/trips": [{ id: "trip-1" }],
      "/usage": { limits: { saved_trips: 20, price_alerts: 20 } },
    }));
    const first = render(<NewTripAuthGate />);
    expect(await screen.findByText("已驗證的新行程表單")).toBeTruthy();
    first.unmount();

    vi.stubGlobal("fetch", fetchByPath({ "/auth/me": { id: "u1" }, "/usage": { limits: { saved_trips: 20 } } }, 503));
    render(<NewTripAuthGate />);
    expect(await screen.findByText("已驗證的新行程表單")).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "已達儲存旅程上限" })).toBeNull();
  });
});
