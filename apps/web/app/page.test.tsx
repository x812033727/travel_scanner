import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Home from "./page";

describe("home", () => {
  it("shows the primary trip search", () => {
    render(<Home />);
    expect(screen.getByRole("button", { name: /開始規劃/ })).toBeTruthy();
  });
});

