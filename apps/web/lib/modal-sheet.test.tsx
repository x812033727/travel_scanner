import { fireEvent, render, screen } from "@testing-library/react";
import { useState } from "react";
import { describe, expect, it } from "vitest";
import { useModalSheet } from "./modal-sheet";

/**
 * Measured on the live site before this hook existed: the filter panel on /hotspots reported
 * `role: null`, left focus on the button that opened it, ignored Escape, and let Tab walk out
 * into the page behind the scrim. Each test below is one of those four.
 */
function Sheet({ onOpenChange }: { onOpenChange?: (open: boolean) => void } = {}) {
  const [open, setOpen] = useState(false);
  const close = () => {
    setOpen(false);
    onOpenChange?.(false);
  };
  const ref = useModalSheet<HTMLFormElement>(open, close);
  return (
    <div>
      <button type="button" onClick={() => setOpen(true)}>
        Open filters
      </button>
      <button type="button">Behind the sheet</button>
      <form
        ref={ref}
        aria-label="Filters"
        {...(open ? { role: "dialog" as const, "aria-modal": true } : {})}
      >
        <button type="button" aria-label="Close filters" onClick={close}>
          ×
        </button>
        <input aria-label="Search" />
        <button type="submit">Apply</button>
      </form>
    </div>
  );
}

describe("useModalSheet", () => {
  it("is not a dialog until it opens", () => {
    render(<Sheet />);
    // On a wide screen this same form is the filter bar in the page. Calling that a modal
    // would be a lie to a screen reader.
    expect(screen.queryByRole("dialog")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    expect(screen.getByRole("dialog", { name: "Filters" })).toBeTruthy();
  });

  it("moves focus into the sheet, to the way out", () => {
    render(<Sheet />);
    const trigger = screen.getByRole("button", { name: "Open filters" });
    trigger.focus();
    fireEvent.click(trigger);
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "Close filters" }));
  });

  it("closes on Escape", () => {
    const seen: boolean[] = [];
    render(<Sheet onOpenChange={(open) => seen.push(open)} />);
    fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(seen).toEqual([false]);
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("gives focus back to whatever opened it", () => {
    render(<Sheet />);
    const trigger = screen.getByRole("button", { name: "Open filters" });
    trigger.focus();
    fireEvent.click(trigger);
    fireEvent.keyDown(document, { key: "Escape" });
    // Escape used to leave focus on <body>, which returns a keyboard reader to the top of
    // the document, several tabs from the control they had just used.
    expect(document.activeElement).toBe(trigger);
  });

  it("wraps Tab at the end of the sheet instead of letting it out", () => {
    render(<Sheet />);
    fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    const apply = screen.getByRole("button", { name: "Apply" });
    apply.focus();
    fireEvent.keyDown(document, { key: "Tab" });
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "Close filters" }));
  });

  it("wraps Shift+Tab at the start", () => {
    render(<Sheet />);
    fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    screen.getByRole("button", { name: "Close filters" }).focus();
    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "Apply" }));
  });

  it("pulls focus back when it is already outside the sheet", () => {
    render(<Sheet />);
    fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    // What a click on the scrim leaves behind: focus on the body, or on the page beneath.
    screen.getByRole("button", { name: "Behind the sheet" }).focus();
    fireEvent.keyDown(document, { key: "Tab" });
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "Close filters" }));
  });

  it("leaves ordinary tabbing inside the sheet alone", () => {
    render(<Sheet />);
    fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    const search = screen.getByRole("textbox", { name: "Search" });
    search.focus();
    fireEvent.keyDown(document, { key: "Tab" });
    // Not the first element: the browser's own Tab handling should still run.
    expect(document.activeElement).toBe(search);
  });

  it("locks the page behind it and gives the scroll back", () => {
    render(<Sheet />);
    fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(document.body.style.overflow).toBe("");
  });
});
