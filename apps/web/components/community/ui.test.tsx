import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { useState } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Dialog } from "./ui";

describe("nested Dialog", () => {
  const original = Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, "showModal");
  beforeEach(() => {
    Object.defineProperty(HTMLDialogElement.prototype, "showModal", { configurable: true, value: function (this: HTMLDialogElement) { this.open = true; } });
  });
  afterEach(() => {
    if (original) Object.defineProperty(HTMLDialogElement.prototype, "showModal", original);
    else Reflect.deleteProperty(HTMLDialogElement.prototype, "showModal");
  });

  it.each(["cancel", "close"])("%s only closes the active child, preserving the reading drawer", (type) => {
    const closeDetail = vi.fn(); const closeOrganizer = vi.fn();
    render(<Dialog title="Reading detail" onClose={closeDetail}>
      <Dialog title="Organize saved item" onClose={closeOrganizer}>Saved content</Dialog>
    </Dialog>);
    const event = new Event(type, { bubbles: false, cancelable: type === "cancel" });
    fireEvent(screen.getByRole("dialog", { name: "Organize saved item" }), event);
    expect(closeOrganizer).toHaveBeenCalledTimes(1);
    expect(closeDetail).not.toHaveBeenCalled();
    if (type === "cancel") expect(event.defaultPrevented).toBe(true);
  });

  it("still closes the outer drawer on its own Escape cancel event", () => {
    const onClose = vi.fn();
    render(<Dialog title="Reading detail" onClose={onClose}>Content</Dialog>);
    fireEvent(screen.getByRole("dialog", { name: "Reading detail" }), new Event("cancel", { cancelable: true }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("dismisses only a complete backdrop click, not padding or a drag from the content", () => {
    const onClose = vi.fn(); render(<Dialog title="Detail" onClose={onClose}>Content</Dialog>);
    const dialog = screen.getByRole("dialog");
    vi.spyOn(dialog, "getBoundingClientRect").mockReturnValue({ left: 20, top: 20, right: 200, bottom: 200 } as DOMRect);
    fireEvent(dialog, new MouseEvent("pointerdown", { bubbles: true, clientX: 50, clientY: 50 }));
    fireEvent.click(dialog, { clientX: 1, clientY: 1 }); expect(onClose).not.toHaveBeenCalled();
    fireEvent(dialog, new MouseEvent("pointerdown", { bubbles: true, clientX: 1, clientY: 1 }));
    fireEvent.click(dialog, { clientX: 1, clientY: 1 }); expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("ignores dismissal aimed at an outer layer while a child is open", () => {
    const outer = vi.fn(); render(<Dialog title="Outer" onClose={outer}><Dialog title="Inner" onClose={vi.fn()}>Child</Dialog></Dialog>);
    fireEvent(screen.getByRole("dialog", { name: "Outer" }), new Event("cancel", { cancelable: true }));
    expect(outer).not.toHaveBeenCalled();
  });

  it("unlocks scrolling and restores the opener after actual unmount", async () => {
    function Example() { const [open, setOpen] = useState(false); return <><button onClick={() => setOpen(true)}>Open</button>{open && <Dialog title="Detail" onClose={() => setOpen(false)}>Content</Dialog>}</>; }
    render(<Example />); const trigger = screen.getByRole("button", { name: "Open" }); trigger.focus(); fireEvent.click(trigger);
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent(screen.getByRole("dialog"), new Event("cancel", { cancelable: true }));
    await waitFor(() => expect(document.activeElement).toBe(trigger));
    expect(document.body.style.overflow).toBe("");
  });

  it.each([false, true])("wraps the Tab boundary (shift=%s), excluding disabled and hidden trailing controls", (shiftKey) => {
    const onClose = vi.fn();
    render(<Dialog title="Report" onClose={onClose}>
      <input aria-label="Reason" />
      <button>Submit</button>
      <button disabled>Unavailable</button>
      <div hidden><button>Hidden action</button></div>
      <button style={{ visibility: "hidden" }}>Invisible action</button>
    </Dialog>);
    const dialog = screen.getByRole("dialog", { name: "Report" });
    const first = within(dialog).getByRole("button", { name: "關閉" });
    const last = within(dialog).getByRole("button", { name: "Submit" });
    const boundary = shiftKey ? first : last;
    boundary.focus();
    const event = new KeyboardEvent("keydown", { key: "Tab", shiftKey, bubbles: true, cancelable: true });
    fireEvent(boundary, event);
    expect(document.activeElement).toBe(shiftKey ? last : first);
    expect(event.defaultPrevented).toBe(true);
    expect(onClose).not.toHaveBeenCalled();
  });

  it.each([false, true])("leaves intermediate Tab navigation to the browser (shift=%s)", (shiftKey) => {
    render(<Dialog title="Report" onClose={vi.fn()}><input aria-label="Reason" /><button>Submit</button></Dialog>);
    const middle = screen.getByRole("textbox", { name: "Reason" });
    middle.focus();
    const event = new KeyboardEvent("keydown", { key: "Tab", shiftKey, bubbles: true, cancelable: true });
    fireEvent(middle, event);
    expect(event.defaultPrevented).toBe(false);
    // jsdom does not perform native Tab navigation; the handler must leave this event alone.
    expect(document.activeElement).toBe(middle);
  });

  it("wraps only the active child and ignores Tab aimed at the outer layer", () => {
    const closeOuter = vi.fn(); const closeInner = vi.fn();
    render(<Dialog title="Reading detail" onClose={closeOuter}>
      <Dialog title="Report" onClose={closeInner}><input aria-label="Reason" /><button>Submit</button></Dialog>
      <button>Outer action</button>
    </Dialog>);
    const inner = screen.getByRole("dialog", { name: "Report" });
    const first = within(inner).getByRole("button", { name: "關閉" });
    const last = within(inner).getByRole("button", { name: "Submit" });
    for (const shiftKey of [false, true]) {
      const boundary = shiftKey ? first : last;
      boundary.focus();
      const event = new KeyboardEvent("keydown", { key: "Tab", shiftKey, bubbles: true, cancelable: true });
      fireEvent(boundary, event);
      expect(document.activeElement).toBe(shiftKey ? last : first);
      expect(event.defaultPrevented).toBe(true);
    }
    const outerAction = screen.getByRole("button", { name: "Outer action" });
    outerAction.focus();
    const event = new KeyboardEvent("keydown", { key: "Tab", bubbles: true, cancelable: true });
    fireEvent(outerAction, event);
    expect(document.activeElement).toBe(outerAction);
    expect(event.defaultPrevented).toBe(false);
    expect(closeOuter).not.toHaveBeenCalled();
    expect(closeInner).not.toHaveBeenCalled();
  });

  it("does not override a child control that already consumed Tab", () => {
    render(<Dialog title="Report" onClose={vi.fn()}><button onKeyDown={(event) => event.preventDefault()}>Submit</button></Dialog>);
    const last = screen.getByRole("button", { name: "Submit" });
    last.focus();
    const event = new KeyboardEvent("keydown", { key: "Tab", bubbles: true, cancelable: true });
    fireEvent(last, event);
    expect(event.defaultPrevented).toBe(true);
    expect(document.activeElement).toBe(last);
  });

  it("leaves composing Tab events untouched", () => {
    render(<Dialog title="Report" onClose={vi.fn()}><button>Submit</button></Dialog>);
    const last = screen.getByRole("button", { name: "Submit" });
    last.focus();
    const event = new KeyboardEvent("keydown", { key: "Tab", isComposing: true, bubbles: true, cancelable: true });
    fireEvent(last, event);
    expect(event.defaultPrevented).toBe(false);
    expect(document.activeElement).toBe(last);
  });
});
