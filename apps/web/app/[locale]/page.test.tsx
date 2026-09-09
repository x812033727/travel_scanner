import { act, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Home from "./page";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }), useSearchParams: () => new URLSearchParams() }));
vi.mock("@/lib/discovery", async (original) => ({ ...await original<typeof import("@/lib/discovery")>(), useDiscoveryStatus: () => ({ enabled: false, loading: false }) }));

describe("home", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(
      JSON.stringify({ detail: "not signed in" }),
      { status: 401 },
    )));
  });

  it("keeps the original primary trip search when discovery is resolved off", async () => {
    const home = await Home();
    await act(async () => { render(home); });
    expect(screen.getByRole("heading", { name: /不用寫完整句子/ })).toBeTruthy();
    expect(screen.getByRole("button", { name: /下一步/ })).toBeTruthy();
    expect(document.getElementById("trip-search")).toBeTruthy();
  });
});
