import "@testing-library/jest-dom/vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { TripItem } from "@/lib/trip-types";
import { OptionalStop } from "./optional-stop";
import { getStopTone, stopToneClassName, stopToneStyles } from "./stop-tone";

describe("optional stop semantic tones", () => {
  it.each([
    ["hotel_start", "hotel", "住宿據點 · 出發"],
    ["hotel_end", "hotel", "住宿據點 · 返回"],
    ["lunch", "lunch", "午餐"],
    ["dinner", "dinner", "晚餐"],
  ] as const)("keeps %s recognizable when its title is only a place name", (systemRole, tone, label) => {
    const view = render(<OptionalStop collapsed kind={tone === "hotel" ? "hotel" : "meal"} systemRole={systemRole}
      title="Place name" hint="09:00"><button>Change place</button></OptionalStop>);
    const details = view.container.querySelector("details")!;
    expect(details).toHaveAttribute("data-stop-tone", tone);
    expect(details).toHaveClass(stopToneStyles[tone], stopToneStyles.summary);
    expect(details).not.toHaveAttribute("open");
    expect(details.querySelector("summary")).toHaveTextContent(label);
    expect(details.querySelector("summary")).toHaveTextContent("Place name");
    expect(screen.getByRole("button", { name: "Change place", hidden: true })).toBeInTheDocument();
  });

  it("retains the role tone while explicitly marking a skipped meal", () => {
    const view = render(<OptionalStop collapsed kind="meal" systemRole="dinner" skipped
      title="Restaurant" hint="Skipped"><p>Saved details</p></OptionalStop>);
    const details = view.container.querySelector("details")!;
    expect(details).toHaveAttribute("data-stop-tone", "dinner");
    expect(details).toHaveAttribute("data-stop-skipped", "true");
    expect(details).toHaveClass(stopToneStyles.skipped);
    expect(details.querySelector("summary")).toHaveTextContent("晚餐");
    expect(details.querySelector("summary")).toHaveTextContent("Skipped");
  });

  it("never infers a meal role from a name or changes unrelated flight appearance", () => {
    const view = render(<OptionalStop collapsed kind="meal" title="Dinner at Noon" hint="12:00"><p>Details</p></OptionalStop>);
    expect(view.container.querySelector("details")).not.toHaveAttribute("data-stop-tone");
    view.rerender(<OptionalStop collapsed kind="flight" systemRole="outbound_flight" title="Flight" hint="09:00"><p>Details</p></OptionalStop>);
    expect(view.container.querySelector("details")).not.toHaveClass(stopToneStyles.tone);
  });

  it("does not introduce another wrapper when the caller requests expanded content", () => {
    const view = render(<OptionalStop collapsed={false} kind="meal" systemRole="lunch" title="Lunch" hint="12:00"><article>Existing card</article></OptionalStop>);
    expect(view.container.querySelector("details")).toBeNull();
    expect(screen.getByRole("article")).toHaveTextContent("Existing card");
  });

  it.each(["card", "summary", "entry", "marker", "badge"] as const)("uses the same authoritative role for the %s variant", (variant) => {
    expect(stopToneClassName("hotel_end", variant)).toContain(stopToneStyles.hotel);
    expect(stopToneClassName("lunch", variant)).toContain(stopToneStyles.lunch);
    expect(stopToneClassName("dinner", variant, true)).toContain(stopToneStyles.skipped);
    expect(stopToneClassName(null, variant)).toBe("");
  });

  it.each([null, undefined, "outbound_flight", "return_flight"] as TripItem["system_role"][])("does not give an unrelated %s role a hotel tone", (role) => {
    expect(getStopTone(role)).toBeUndefined();
  });
});

const css = readFileSync(join(import.meta.dirname, "stop-tone.module.css"), "utf8");
function palette(selector: string) {
  const offset = css.indexOf(`${selector} {`);
  expect(offset).toBeGreaterThanOrEqual(0);
  const body = css.slice(offset, css.indexOf("}", offset));
  return Object.fromEntries([...body.matchAll(/--stop-([a-z]+): (#[0-9a-f]{6});/g)].map((match) => [match[1], match[2]]));
}
function luminance(hex: string) {
  const rgb = [1, 3, 5].map((offset) => parseInt(hex.slice(offset, offset + 2), 16) / 255)
    .map((channel) => channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4);
  return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
}
function contrast(a: string, b: string) {
  const first = luminance(a), second = luminance(b);
  return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
}

describe("stop palette accessibility", () => {
  it.each(["light", "dark"] as const)("has distinct surfaces and readable primary/secondary text in %s mode", (theme) => {
    const prefix = theme === "dark" ? ':global(:root[data-theme="dark"]) ' : "";
    const values = ["hotel", "lunch", "dinner"].map((role) => palette(`${prefix}.${role}`));
    expect(new Set(values.map((value) => value.bg)).size).toBe(3);
    const skipped = palette(`${prefix}.tone.skipped`);
    for (const value of [...values, skipped]) {
      for (const surface of [value.bg, value.raised]) {
        expect(contrast(value.ink, surface)).toBeGreaterThanOrEqual(4.5);
        expect(contrast(value.muted, surface)).toBeGreaterThanOrEqual(4.5);
      }
    }
    for (const value of values) {
      expect(contrast(value.accent, value.bg)).toBeGreaterThanOrEqual(3);
      expect(contrast(value.accent, skipped.bg)).toBeGreaterThanOrEqual(4.5);
    }
  });

  it("preserves an explicit role stripe, keyboard focus and 44px touch targets", () => {
    expect(css).toContain("border-inline-start: 4px solid var(--stop-accent)");
    expect(css).toContain("min-height: 44px");
    expect(css).toContain("summary:focus-visible");
    expect(css).toContain("outline: 3px solid var(--stop-accent)");
  });

  it("keeps timeline markers grid-centered while badges use inline layout", () => {
    const sharedRule = css.match(/\.tone\.marker,\s*\.tone\.badge\s*\{([^}]+)\}/)?.[1];
    expect(sharedRule).toBeDefined();
    expect(sharedRule).not.toMatch(/display\s*:/);
    expect(css).toMatch(/(?:^|\n)\.tone\.badge\s*\{[^}]*display:\s*inline-block/);
  });
});
