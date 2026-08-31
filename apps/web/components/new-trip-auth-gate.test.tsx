import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { NewTripAuthGate } from "./new-trip-auth-gate";

vi.mock("./new-trip-form", () => ({ NewTripForm: () => <div>已驗證的新行程表單</div> }));

afterEach(() => vi.unstubAllGlobals());

describe("NewTripAuthGate", () => {
  it("asks signed-out visitors to log in before showing the long form", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "未登入" }), { status: 401 })));
    render(<NewTripAuthGate />);
    expect(await screen.findByRole("link", { name: "前往登入" })).toBeTruthy();
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
});
