import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { READER_SUPPORT_URL, SupportLink } from "./support-link";

const labels = { text: "If this article helped, you can chip in.", action: "Support Mokaair", newTab: "opens in a new tab" };

describe("SupportLink", () => {
  it("renders nothing until the owner sets an address", () => {
    expect(READER_SUPPORT_URL).toBeNull();
    const { container } = render(<SupportLink labels={labels} />);
    expect(container.innerHTML).toBe("");
  });

  it("is a plain first-party link: new tab, no referrer, no widget", () => {
    const { container, getByRole } = render(<SupportLink labels={labels} url="https://www.buymeacoffee.com/example" />);
    const link = getByRole("link", { name: "Support Mokaair · opens in a new tab" });
    expect(link.getAttribute("href")).toBe("https://www.buymeacoffee.com/example");
    expect(link.getAttribute("target")).toBe("_blank");
    expect(link.getAttribute("rel")).toBe("noopener noreferrer");
    expect(container.textContent).toContain(labels.text);
    expect(container.querySelector("script, iframe")).toBeNull();
  });
});
