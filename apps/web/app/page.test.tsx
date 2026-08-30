import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import Home from "./page";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }) }));

describe("home", () => {
  it("shows the primary trip search", () => {
    render(<Home />);
    expect(screen.getByRole("button", { name: /開始規劃/ })).toBeTruthy();
  });
});

