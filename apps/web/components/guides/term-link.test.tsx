import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { TermLink } from "./term-link";

const labels = { card: "名詞說明", readMore: "閱讀全文" };

function draw() {
  return render(
    <p>
      前文 <TermLink href="/zh-TW/life/ai-term-fine-tuning" text="微調" title="微調是什麼" description="用少量資料再訓練模型。" labels={labels} /> 後文
      <button type="button">別處</button>
    </p>,
  );
}

beforeEach(() => vi.useFakeTimers());
afterEach(() => { cleanup(); vi.useRealTimers(); vi.unstubAllGlobals(); });

describe("TermLink", () => {
  it("is a real link with a dotted underline and a closed card until asked", () => {
    draw();
    const link = screen.getByRole("link", { name: "微調" });
    expect(link.getAttribute("href")).toBe("/zh-TW/life/ai-term-fine-tuning");
    expect(link.className).toContain("app-term-link");
    expect(link.getAttribute("aria-expanded")).toBe("false");
    const card = document.getElementById(link.getAttribute("aria-controls")!)!;
    expect(card.hidden).toBe(true);
    expect(card.getAttribute("role")).toBe("note");
    expect(card.textContent).toContain("微調是什麼");
    expect(card.textContent).toContain("用少量資料再訓練模型。");
    expect(card.textContent).toContain("閱讀全文");
  });

  it("opens after a short hover, not on a pointer merely crossing it", () => {
    draw();
    const link = screen.getByRole("link", { name: "微調" });
    fireEvent.pointerEnter(link);
    expect(link.getAttribute("aria-expanded")).toBe("false");
    fireEvent.pointerLeave(link);
    act(() => { vi.advanceTimersByTime(200); });
    expect(link.getAttribute("aria-expanded")).toBe("false");
    fireEvent.pointerEnter(link);
    act(() => { vi.advanceTimersByTime(150); });
    expect(link.getAttribute("aria-expanded")).toBe("true");
    expect(screen.getByRole("note", { name: "名詞說明" })).toBeTruthy();
    fireEvent.pointerLeave(link);
    expect(link.getAttribute("aria-expanded")).toBe("false");
  });

  it("opens at once on focus, closes on blur, Escape and a pointer elsewhere", () => {
    draw();
    const link = screen.getByRole("link", { name: "微調" });
    fireEvent.focus(link);
    expect(link.getAttribute("aria-expanded")).toBe("true");
    const escape = new KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
    act(() => { link.dispatchEvent(escape); });
    expect(escape.defaultPrevented).toBe(true);
    expect(link.getAttribute("aria-expanded")).toBe("false");
    // A second Escape with nothing open is left for whatever is around the link.
    const again = new KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
    act(() => { link.dispatchEvent(again); });
    expect(again.defaultPrevented).toBe(false);

    fireEvent.focus(link);
    fireEvent.blur(link);
    expect(link.getAttribute("aria-expanded")).toBe("false");

    fireEvent.focus(link);
    fireEvent.pointerDown(screen.getByRole("button", { name: "別處" }));
    expect(link.getAttribute("aria-expanded")).toBe("false");
  });

  it("on a device without hover, the first tap shows the definition and the second follows the link", () => {
    vi.stubGlobal("matchMedia", vi.fn(() => ({ matches: true })));
    draw();
    const link = screen.getByRole("link", { name: "微調" });
    const first = fireEvent.click(link);
    expect(first).toBe(false); // default prevented: no navigation yet
    expect(link.getAttribute("aria-expanded")).toBe("true");
    const second = fireEvent.click(link);
    expect(second).toBe(true);
  });

  it("with hover available a click follows the link straight away", () => {
    vi.stubGlobal("matchMedia", vi.fn(() => ({ matches: false })));
    draw();
    expect(fireEvent.click(screen.getByRole("link", { name: "微調" }))).toBe(true);
  });
});
