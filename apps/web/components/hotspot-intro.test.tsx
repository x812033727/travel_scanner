import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { HotspotIntro, approximateColumns } from "./hotspot-intro";

describe("approximateColumns", () => {
  it("counts a CJK character as twice a Latin one", () => {
    expect(approximateColumns("abcd")).toBe(4);
    expect(approximateColumns("淺草寺")).toBe(6);
    expect(approximateColumns("浅草寺は")).toBe(8);
    expect(approximateColumns("명동")).toBe(4);
    // Mixed text adds up rather than picking one rule.
    expect(approximateColumns("Senso-ji 淺草寺")).toBe(9 + 6);
  });

  it("treats full-width punctuation as wide and ASCII punctuation as narrow", () => {
    expect(approximateColumns("，。")).toBe(4);
    expect(approximateColumns(",.")).toBe(2);
  });
});

describe("HotspotIntro", () => {
  it("renders nothing at all when there is no approved paragraph", () => {
    const { container } = render(<HotspotIntro text={null} />);
    expect(container.firstChild).toBeNull();
    const blank = render(<HotspotIntro text="   " />);
    expect(blank.container.firstChild).toBeNull();
  });

  it("never offers a toggle when the caller asked for the whole paragraph", () => {
    render(<HotspotIntro text={"字".repeat(300)} clamp={false} />);
    expect(screen.queryByRole("button")).toBeNull();
    expect(screen.getByText("專門介紹")).toBeTruthy();
  });

  it("clamps an English paragraph only once it is genuinely long", () => {
    // Same character count, different widths: 120 Latin characters fit three lines,
    // 120 CJK characters do not.
    const { unmount } = render(<HotspotIntro text={"a".repeat(120)} />);
    expect(screen.queryByRole("button", { name: "展開全文" })).toBeNull();
    unmount();

    render(<HotspotIntro text={"字".repeat(120)} />);
    expect(screen.getByRole("button", { name: "展開全文" })).toBeTruthy();
  });
});
