import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Home from "./page";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }), useSearchParams: () => new URLSearchParams() }));

describe("home", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(
      JSON.stringify({ detail: "not signed in" }),
      { status: 401 },
    )));
  });

  it("shows the primary trip search", async () => {
    render(await Home());
    expect(screen.getByRole("heading", { name: /不用寫完整句子/ })).toBeTruthy();
    expect(screen.getByRole("button", { name: /下一步/ })).toBeTruthy();
  });
});

