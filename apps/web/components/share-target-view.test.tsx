import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ShareTargetView } from "./share-target-view";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) =>
    React.createElement("a", { href, ...props }, children),
  usePathname: () => "/",
  useRouter: () => ({ push, replace: vi.fn(), refresh: vi.fn() }),
}));

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

describe("ShareTargetView", () => {
  beforeEach(() => {
    apiMock.mockReset();
    push.mockReset();
  });

  it("sends what Android shared into the chosen trip's waiting list", async () => {
    apiMock.mockImplementation(async (path: string, init?: RequestInit) => {
      if (path === "/trips") return [{ id: "trip-1", name: "東京五天" }, { id: "trip-2", name: "京都三天" }];
      if (init?.method === "POST") return { created: [], matched: 0, items: [] };
      return {};
    });
    render(<ShareTargetView shared="https://maps.app.goo.gl/abc" />);

    await screen.findByRole("option", { name: "東京五天" });
    fireEvent.change(screen.getByLabelText("行程"), { target: { value: "trip-2" } });
    fireEvent.click(screen.getByRole("button", { name: "加入待安排" }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-2"));
    const call = apiMock.mock.calls.find(([path]) => String(path).includes("/places/ingest"));
    expect(call?.[0]).toBe("/trips/trip-2/places/ingest");
    expect(JSON.parse(String((call?.[1] as RequestInit).body))).toEqual({ text: "https://maps.app.goo.gl/abc" });
  });

  it("tells an iPhone reader to paste, because there is no share sheet to use", async () => {
    apiMock.mockResolvedValue([]);
    render(<ShareTargetView shared="" />);
    expect(await screen.findByText(/iPhone 沒有分享目標/)).toBeTruthy();
  });

  it("asks a signed-out reader to sign in rather than failing silently", async () => {
    apiMock.mockRejectedValue(new Error("unauthorized"));
    render(<ShareTargetView shared="淺草寺" />);
    expect(await screen.findByText("請先登入，才能把地點加進行程。")).toBeTruthy();
  });
});
