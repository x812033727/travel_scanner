import { fireEvent, render, screen, waitFor } from "@testing-library/react";
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
});
