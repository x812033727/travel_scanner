import { fireEvent, render, screen } from "@testing-library/react";
import { useEffect, useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { modalFocusTargets, registerModalLayer, useModalSheet } from "./modal-sheet";
import { commitBeforePassiveEffects } from "./testing/commit-before-passive-effects";

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

/**
 * A sheet whose element is not in the first commit: `open` is true the whole time, but the
 * panel waits on data, as a sheet behind a loading state does. Nothing here is exotic -- it is
 * the shape any caller reaches for when the sheet has to fetch something before it can draw.
 */
function LateSheet({ onClose }: { onClose: () => void }) {
  const [ready, setReady] = useState(false);
  const ref = useModalSheet<HTMLDivElement>(true, onClose);
  useEffect(() => {
    let alive = true;
    void Promise.resolve().then(() => {
      if (alive) setReady(true);
    });
    return () => {
      alive = false;
    };
  }, []);
  if (!ready) return <p>loading</p>;
  return (
    <div ref={ref} role="dialog" aria-modal="true" aria-label="Late">
      <button type="button" aria-label="Close late">
        x
      </button>
    </div>
  );
}

/** A sheet a request opens: it appears when the request resolves, outside any event. */
function OpenedByRequest({ request }: { request: Promise<void> }) {
  const [open, setOpen] = useState(false);
  useEffect(() => { void request.then(() => setOpen(true)); }, [request]);
  const ref = useModalSheet<HTMLDivElement>(open, () => setOpen(false));
  return open ? <div ref={ref} role="dialog" aria-modal="true" aria-label="Choose a trip"><button type="button" aria-label="Close">×</button></div> : null;
}

/** A sheet that refuses to close while it saves, and saving ends when the request resolves. */
function SavingSheet({ request }: { request: Promise<void> }) {
  const [open, setOpen] = useState(true);
  const [saving, setSaving] = useState(true);
  useEffect(() => { void request.then(() => setSaving(false)); }, [request]);
  const ref = useModalSheet<HTMLDivElement>(open, () => { if (!saving) setOpen(false); });
  return open ? <div ref={ref} role="dialog" aria-modal="true" aria-label="Saving"><button type="button" disabled={saving}>Save</button></div> : null;
}

describe("useModalSheet", () => {
  it("includes the closed disclosure summary but excludes its hidden source link and hidden ancestors", () => {
    const { container } = render(<div><button>Close</button><details><summary>Sources</summary><a href="https://example.com">Hidden source</a></details><div hidden><button>Hidden ancestor</button></div><div style={{ display: "none" }}><button>Hidden style</button></div></div>);
    expect(modalFocusTargets(container).map((element) => element.textContent)).toEqual(["Close", "Sources"]);
  });

  it("keeps scrolling locked when an outer layer unmounts before its child", () => {
    const { container } = render(<section><div /></section>);
    const outer = container.querySelector("section")!; const inner = outer.querySelector("div")!;
    const unlockInner = registerModalLayer(inner); const unlockOuter = registerModalLayer(outer);
    unlockOuter(); expect(document.body.style.overflow).toBe("hidden");
    unlockInner(); expect(document.body.style.overflow).toBe("");
  });

  it("does not close during IME composition or an already handled Escape", () => {
    render(<Sheet />); fireEvent.click(screen.getByRole("button", { name: "Open filters" }));
    fireEvent.keyDown(document, { key: "Escape", isComposing: true });
    const event = new KeyboardEvent("keydown", { key: "Escape", cancelable: true }); event.preventDefault(); fireEvent(document, event);
    expect(screen.getByRole("dialog")).toBeTruthy();
  });
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
  // A sheet that renders after the effect has already run used to be left with no Escape, no
  // Tab trap and no scroll lock -- and said nothing about it, so it looked like a working
  // dialog and answered to none of the keyboard. `open` never changes here, so the effect's
  // one dependency never fires it again; the element itself has to be what wakes it.
  it("guards a sheet whose element arrives after the first commit", async () => {
    const onClose = vi.fn();
    render(<LateSheet onClose={onClose} />);
    expect(await screen.findByRole("dialog", { name: "Late" })).toBeTruthy();
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  // A request that opens a sheet, or ends the work a sheet was waiting on, commits before its
  // passive effects run. travel-card-actions went red in a loaded full run on the first case:
  // the sheet was on screen and its Escape listener was not attached yet.
  it("answers Escape as soon as a resolved request has drawn it", async () => {
    let respond!: () => void;
    const request = new Promise<void>((resolve) => { respond = resolve; });
    render(<OpenedByRequest request={request} />);
    await commitBeforePassiveEffects(respond, () => screen.queryByRole("dialog") !== null);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("closes by the guard it shows once a resolved request has lifted it", async () => {
    let respond!: () => void;
    const request = new Promise<void>((resolve) => { respond = resolve; });
    render(<SavingSheet request={request} />);
    const save = screen.getByRole("button", { name: "Save" }) as HTMLButtonElement;
    await commitBeforePassiveEffects(respond, () => !save.disabled);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
  });
});
