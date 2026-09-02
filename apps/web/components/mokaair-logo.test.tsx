import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MokaairLogo } from "./mokaair-logo";

describe("MokaairLogo", () => {
  it("renders the exact accessible wordmark without decorative imagery", () => {
    render(<MokaairLogo />);
    const logo = screen.getByRole("img", { name: "Mokaair" });
    expect(logo.textContent).toBe("Mokaair");
    expect(logo.querySelector("svg")).toBeNull();
  });
});
